import logging
from typing import Dict, Any
import uuid
import time

from app.services import preprocessor, scraper, matcher
from app.models.schemas import VerificationRequest

logger = logging.getLogger(__name__)


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


def verify_claim(request: VerificationRequest) -> Dict[str, Any]:
    """
    Main orchestrator for verifying claims:
    1. Preprocess claim
    2. Fetch articles
    3. Match semantically
    4. Score based on matches
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

    # Step 4: Score - New Computation Logic
    logger.info("\n🎯 [STEP 4] Calculating Truth Score...")

    # New Logic: x = articles with same meaning/intent, y = total contextual articles
    # For now, we'll use supporting articles as "same meaning" and total as contextual
    x = len(support)  # Articles that report the same thing (same meaning and intent)
    y = len(support) + len(contradict)  # Total articles within context (70% threshold)

    # Truth Score = x/y * 100
    truth_score = (x / y * 100) if y > 0 else 0.0

    # Confidence Score Logic
    if y >= 10:
        confidence_score = 100.0
    else:
        confidence_score = (y / 10) * 100

    logger.info(f"📊 Supporting articles (x): {x}")
    logger.info(f"📊 Total contextual articles (y): {y}")
    logger.info(f"🎯 Truth Score: {truth_score:.1f}%")
    logger.info(f"🎯 Confidence Score: {confidence_score:.1f}%")

    # Verdict Calculation based on new criteria
    verdict = calculate_verdict(confidence_score, truth_score)
    logger.info(f"⚖️ Verdict: {verdict}")

    # Transform articles to match ArticleInfo schema
    def transform_article(article):
        return {
            "url": article.get("link", ""),
            "title": article.get("title", ""),
            "content": article.get("snippet", ""),  # Use snippet as content for now
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
        "truth_score": round(truth_score / 100, 4),  # Convert back to 0-1 scale for API compatibility
        "confidence": round(confidence_score / 100, 2),  # Convert back to 0-1 scale for API compatibility
        "verdict": verdict,
        "matching_articles": transformed_support,
        "contradicting_articles": transformed_contradict,
        "processing_time": round(pre_elapsed + match_elapsed, 2)
    }
