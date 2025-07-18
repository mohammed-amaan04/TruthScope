"""
Enhanced Configuration settings for sophisticated LLM-based Fake News Detection System
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from root directory .env file
root_dir = Path(__file__).parent.parent  # Go up one level from LLM to root
env_path = root_dir / ".env"
load_dotenv(env_path)

# Import torch with fallback
try:
    import torch
except ImportError:
    torch = None

class Config:
    # === API Keys ===
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

    # === LLM Configuration ===
    LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "meta-llama/Llama-2-7b-chat-hf")
    PARAPHRASE_MODEL = os.getenv("PARAPHRASE_MODEL", "t5-base")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    # Device selection: use env var if set, otherwise auto-detect
    DEVICE = os.getenv("DEVICE", "cuda" if torch and torch.cuda.is_available() else "cpu")
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", "2048"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))

    # === Text Paraphrasing Settings ===
    NUM_PARAPHRASES = int(os.getenv("NUM_PARAPHRASES", "10"))
    PARAPHRASE_DIVERSITY = float(os.getenv("PARAPHRASE_DIVERSITY", "0.8"))
    MIN_PARAPHRASE_LENGTH = int(os.getenv("MIN_PARAPHRASE_LENGTH", "10"))

    # === Web Scraping Settings ===
    MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "50"))
    MAX_ARTICLES_PER_SOURCE = int(os.getenv("MAX_ARTICLES_PER_SOURCE", "10"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "8"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.75"))
    CONTENT_MIN_LENGTH = int(os.getenv("CONTENT_MIN_LENGTH", "100"))

    # === Truth Scoring Configuration ===
    NO_SOURCES_SCORE = 0.0  # 0% when no sources found
    PERFECT_MATCH_SCORE = 1.0  # 100% when 5+ sources confirm
    MIN_SOURCES_FOR_HIGH_CONFIDENCE = int(os.getenv("MIN_SOURCES_FOR_HIGH_CONFIDENCE", "5"))
    SOURCE_AGREEMENT_THRESHOLD = float(os.getenv("SOURCE_AGREEMENT_THRESHOLD", "0.8"))
    VARIATION_PENALTY_FACTOR = float(os.getenv("VARIATION_PENALTY_FACTOR", "0.1"))

    # === Regional and Temporal Analysis ===
    ENABLE_REGIONAL_ANALYSIS = os.getenv("ENABLE_REGIONAL_ANALYSIS", "true").lower() == "true"
    ENABLE_TEMPORAL_ANALYSIS = os.getenv("ENABLE_TEMPORAL_ANALYSIS", "true").lower() == "true"
    MAX_ARTICLE_AGE_DAYS = int(os.getenv("MAX_ARTICLE_AGE_DAYS", "30"))
    REGIONAL_RELEVANCE_WEIGHT = float(os.getenv("REGIONAL_RELEVANCE_WEIGHT", "0.2"))
    TEMPORAL_RELEVANCE_WEIGHT = float(os.getenv("TEMPORAL_RELEVANCE_WEIGHT", "0.15"))

    # === Content Analysis Settings ===
    ENABLE_SENTIMENT_ANALYSIS = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "true").lower() == "true"
    ENABLE_BIAS_DETECTION = os.getenv("ENABLE_BIAS_DETECTION", "true").lower() == "true"
    CONTENT_SIMILARITY_THRESHOLD = float(os.getenv("CONTENT_SIMILARITY_THRESHOLD", "0.7"))

    # === Caching Settings ===
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_EXPIRY_HOURS = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))

    # === Headers for Web Requests ===
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    # === Output Settings ===
    OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")
    VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"
    
    # === News Sources ===
    TRUSTED_SOURCES = [
        "reuters.com", "apnews.com", "bbc.com", "npr.org", "bloomberg.com",
        "ft.com", "theguardian.com", "aljazeera.com", "economist.com",
        "nytimes.com", "washingtonpost.com", "wsj.com", "dw.com",
        "thehindu.com", "indianexpress.com", "business-standard.com"
    ]
    
    # === Directories ===
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    CACHE_DIR = BASE_DIR / "cache"
    
    def __init__(self):
        # Create directories if they don't exist
        self.DATA_DIR.mkdir(exist_ok=True)
        self.MODELS_DIR.mkdir(exist_ok=True)
        self.CACHE_DIR.mkdir(exist_ok=True)

        # Validate critical API keys
        self._validate_api_keys()

    def _validate_api_keys(self):
        """Validate that critical API keys are present"""
        critical_keys = {
            'GOOGLE_API_KEY': 'Google Custom Search API',
            'GOOGLE_CSE_ID': 'Google Custom Search Engine ID',
            'NEWSAPI_KEY': 'NewsAPI'
        }

        missing_keys = []
        for key, description in critical_keys.items():
            if not getattr(self, key):
                missing_keys.append(f"{key} ({description})")

        if missing_keys:
            print("⚠️  WARNING: Missing critical API keys:")
            for key in missing_keys:
                print(f"   - {key}")
            print("   Please add these to your LLM/.env file")
            print("   System will work with limited functionality")

    def get_api_status(self):
        """Get status of all API keys"""
        apis = {
            'Google Search': bool(self.GOOGLE_API_KEY and self.GOOGLE_CSE_ID),
            'NewsAPI': bool(self.NEWSAPI_KEY),
            'Reddit': bool(self.REDDIT_CLIENT_ID and self.REDDIT_CLIENT_SECRET),
            'Twitter': bool(self.TWITTER_BEARER_TOKEN),
            'Hugging Face': bool(self.HUGGINGFACE_API_TOKEN)
        }
        return apis

# Global config instance
config = Config()
