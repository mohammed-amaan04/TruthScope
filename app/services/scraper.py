import logging
import requests
from typing import List, Dict

from app.core.config import settings

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VeritasBot/1.0; +https://yourdomain.com/bot)"
}

def fetch_articles_from_google(query: str, num_results: int = 8) -> List[Dict]:
    """Fetches articles using Google Custom Search API"""
    logger.info(f"🌐 Querying Google CSE: {query}")

    # Debug: Check if API credentials are loaded
    logger.info(f"🔧 [SCRAPER] API Key present: {'Yes' if settings.GOOGLE_API_KEY else 'No'}")
    logger.info(f"🔧 [SCRAPER] CSE ID present: {'Yes' if settings.GOOGLE_CSE_ID else 'No'}")

    if not settings.GOOGLE_API_KEY or not settings.GOOGLE_CSE_ID:
        logger.error("❌ Google API credentials not configured properly")
        return []

    try:
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={settings.GOOGLE_API_KEY}&cx={settings.GOOGLE_CSE_ID}&q={query}"
        )

        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise HTTP errors early
        data = response.json()

        if "items" not in data:
            logger.warning(f"⚠️ No items in response. Full response: {data}")
            return []

        articles = []
        for item in data["items"][:num_results]:
            articles.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link"),
            })

        logger.info(f"✅ Retrieved {len(articles)} articles.")
        return articles

    except Exception as e:
        logger.error(f"❌ Error fetching articles: {e}")
        return []
