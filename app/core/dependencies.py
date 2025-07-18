"""
FastAPI dependency injection: Verifier instance
"""

import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Mock verifier for testing API endpoints
class MockVerifier:
    def verify_claim(self, request):
        """Mock verification that returns a basic response"""
        return {
            "claim_id": "mock-claim-123",
            "preprocessing": {
                "original_text": request.text,
                "cleaned_text": request.text,
                "detected_language": request.language or "en",
                "language_confidence": 0.95,
                "entities": [],
                "keywords": ["test", "mock"],
                "intent": None,
                "paraphrases": [],
                "word_count": len(request.text.split()),
                "sentence_count": 1
            },
            "truth_score": 0.5,
            "confidence": 0.7,
            "verdict": "INSUFFICIENT_DATA",
            "matching_articles": [],
            "contradicting_articles": [],
            "processing_time": 0.1,
            "explanations": []
        }

@lru_cache()
def get_verifier():
    """Return real verifier with new computation logic"""
    logger.info("Using real verifier with new computation logic")
    from app.services.verifier import verify_claim

    class RealVerifier:
        def verify_claim(self, request):
            return verify_claim(request)

    return RealVerifier()
