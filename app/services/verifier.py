import logging
from typing import Dict, Any
import uuid
import time
import os
import sys

from app.services import preprocessor, scraper, matcher
from app.models.schemas import VerificationRequest

logger = logging.getLogger(__name__)

# Add LLM folder to path to use source weighting logic
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'LLM'))
try:
    from news_source_weights import news_weights  # type: ignore
except Exception as e:
    news_weights = None  # type: ignore
    logger.warning(f"Source weighting unavailable, falling back to count-based scoring: {e}")


def calculate_verdict(confidence_score: float, truth_score: float) -> str:
    """
    Calculate verdict based on new criteria:
    🟢 Highly Reliable: Confidence ≥ 80 and Truth ≥ 80 → Most Likely True
    🟡 Somewhat Reliable: Confidence ≥ 50 and Truth ≥ 60 → Likely True, but Needs More Support
    🟠 Uncertain: Confidence ≥ 40 and Truth between 40-60 → Inconclusive / Mixed Evidence
    🔴 Suspicious: Confidence ≥ 50 and Truth < 40 → Likely False
    ⚫ Unverifiable: Confidence < 40 → Not Enough Data to Verify
    """
    if confidence_score >= 80 and truth_score >= 80:
        return "MOST_LIKELY_TRUE"
    elif confidence_score >= 50 and truth_score >= 60:
        return "LIKELY_TRUE_NEEDS_SUPPORT"
    elif confidence_score >= 40 and 40 <= truth_score <= 60:
        return "INCONCLUSIVE_MIXED"
    elif confidence_score >= 50 and truth_score < 40:
        return "LIKELY_FALSE"
    else:  # confidence_score < 40
        return "INSUFFICIENT_DATA"


def _compute_weighted_scores(claim_text: str, support: list, contradict: list) -> Dict[str, float]:
    """Compute weighted truth and confidence using source weights if available."""
    all_articles = support + contradict
    if not all_articles:
        return {"truth": 0.0, "confidence": 10.0}  # minimal confidence

    # Quantity and diversity
    unique_sources = set()
    for a in all_articles:
        domain = news_weights.extract_domain(a.get("link", a.get("url", ""))) if news_weights else None
        if domain:
            unique_sources.add(domain)

    quantity_score = min(len(all_articles) / 10.0, 1.0)  # up to 10
    diversity_score = min(len(unique_sources) / 5.0, 1.0) if unique_sources else 0.0

    # Recency avg
    recencies = []
    if news_weights:
        for a in all_articles:
            recencies.append(news_weights.calculate_recency_factor(a.get("published_date", "")))
    avg_recency = sum(recencies) / len(recencies) if recencies else 0.5

    # Weighted truth
    if news_weights:
        claim_category = news_weights.get_category_from_claim(claim_text)
        claim_region = news_weights.get_region_from_claim(claim_text)
        total_w = 0.0
        support_w = 0.0
        for a in all_articles:
            url = a.get("link", a.get("url", ""))
            w = news_weights.calculate_source_weight(url, claim_category, claim_region)
            sim = a.get("similarity_score", 0.5) or 0.5
            rec = news_weights.calculate_recency_factor(a.get("published_date", ""))
            combined = w * sim * rec
            total_w += combined
            if a in support:
                support_w += combined
        truth = (support_w / total_w * 100.0) if total_w > 0 else 0.0
    else:
        # Fallback: count-based
        s = len(support)
        t = len(support) + len(contradict)
        truth = (s / t * 100.0) if t > 0 else 0.0

    confidence = (0.4 * quantity_score + 0.3 * diversity_score + 0.3 * avg_recency) * 100.0
    return {"truth": truth, "confidence": confidence}


def verify_claim(request: VerificationRequest) -> Dict[str, Any]:
    """
    Main orchestrator for verifying claims:
    1. Preprocess claim
    2. Fetch articles
    3. Match semantically
    4. Score based on matches (weighted by credibility, expertise, region, recency)
    """
    claim_id = str(uuid.uuid4())
    logger.info(f"🆔 Verifying claim {claim_id}: {request.text}")

    # Step 1: Preprocess
    logger.info("\n🧠 [STEP 1] Preprocessing...")
    pre_start = time.time()
    preprocessing = preprocessor.preprocess_claim(request.text)
    pre_elapsed = time.time() - pre_start
    logger.info(f"⏱️ Preprocessing time: {pre_elapsed:.2f}s")

    # Step 2: Fetch Articles
    logger.info("\n🔍 [STEP 2] Fetching Articles from Google...")
    search_query = " ".join(preprocessing["keywords"])
    search_results = scraper.fetch_articles_from_google(query=search_query)
    logger.info(f"📄 Total articles collected: {len(search_results)}")

    # Step 3: Match Articles
    logger.info("\n🤖 [STEP 3] Matching Claim with Articles...")
    match_start = time.time()
    support, contradict = matcher.match_articles(request.text, search_results)
    match_elapsed = time.time() - match_start
    logger.info(f"⏱️ Matching time: {match_elapsed:.2f}s")

    # Step 4: Weighted Score
    logger.info("\n🎯 [STEP 4] Calculating Weighted Scores...")
    scores = _compute_weighted_scores(request.text, support, contradict)
    truth_score = scores["truth"]
    confidence_score = scores["confidence"]

    logger.info(f"📊 Supporting articles: {len(support)}")
    logger.info(f"📊 Contradicting articles: {len(contradict)}")
    logger.info(f"🎯 Truth Score (weighted): {truth_score:.1f}%")
    logger.info(f"🎯 Confidence Score (composite): {confidence_score:.1f}%")

    # Verdict Calculation
    verdict = calculate_verdict(confidence_score, truth_score)
    logger.info(f"⚖️ Verdict: {verdict}")

    # Transform articles to match ArticleInfo schema
    def transform_article(article):
        return {
            "url": article.get("link", ""),
            "title": article.get("title", ""),
            "content": article.get("snippet", ""),
            "source": article.get("source", "Unknown"),
            "published_date": article.get("published_date", "Unknown"),
            "author": article.get("author"),
            "similarity_score": article.get("similarity_score", 0.0)
        }

    transformed_support = [transform_article(article) for article in support]
    transformed_contradict = [transform_article(article) for article in contradict]

    return {
        "claim_id": claim_id,
        "preprocessing": preprocessing,
        "truth_score": round(truth_score / 100, 4),
        "confidence": round(confidence_score / 100, 2),
        "verdict": verdict,
        "matching_articles": transformed_support,
        "contradicting_articles": transformed_contradict,
        "processing_time": round(pre_elapsed + match_elapsed, 2)
    }
