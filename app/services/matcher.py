import logging
from typing import List, Tuple
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_articles(claim: str, articles: List[dict]) -> Tuple[List[dict], List[dict]]:
    if not articles:
        logger.warning("No articles provided to match.")
        return [], []

    claim_embedding = model.encode(claim, convert_to_tensor=True)
    support, contradict = [], []

    for article in articles:
        # Use 'snippet' if 'content' is not available (Google CSE returns 'snippet')
        content = article.get('content', article.get('snippet', ''))
        text = f"{article['title']} {content}"
        embedding = model.encode(text, convert_to_tensor=True)
        score = float(util.cos_sim(claim_embedding, embedding)[0])

        article["similarity_score"] = round(score, 4)

        logger.info(f"[MATCHER] '{article['title'][:50]}...' → Score: {score:.4f}")

        if score > 0.6:
            support.append(article)
        elif score < 0.4:
            contradict.append(article)

    if not support and not contradict:
        logger.warning("[MATCHER] No strong matches — returning top-N closest articles instead")
        articles.sort(key=lambda x: x["similarity_score"], reverse=True)
        return articles[:5], []

    return support, contradict
