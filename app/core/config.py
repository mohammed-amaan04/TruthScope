"""
Configuration settings for Veritas system
"""

from dotenv import load_dotenv
import os
from pathlib import Path

# Get the directory where this config.py file is located
current_dir = Path(__file__).parent
# Go up to the app directory, then load .env from there
env_path = current_dir.parent / ".env"

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)


class Settings:
    # === API Configuration ===
    PROJECT_NAME: str = "Veritas"
    API_V1_PREFIX: str = "/api/v1/verify"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    GOOGLE_CSE_NUM_RESULTS: int = 10
    DEBUG: bool = True

    # === NLP and ML Models ===
    SPACY_MODEL: str = "en_core_web_sm"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # === Thresholds & Similarity ===
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", 0.75))
    MAX_BATCH_SIZE: int = int(os.getenv("MAX_BATCH_SIZE", 32))
    MAX_ARTICLES: int = 20

    # === Web Scraper Settings ===
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", 8))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 30))
    USER_AGENT: str = os.getenv("USER_AGENT", (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    ))

    # === Language Support ===
    SUPPORTED_LANGUAGES = {"en", "hi", "bn", "mr", "ta", "te"}

    # === Fallbacks ===
    ENABLE_MOCK_NEWS: bool = True


# Global settings instance
settings = Settings()
