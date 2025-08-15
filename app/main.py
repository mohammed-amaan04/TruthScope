import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body

from app.api.v1 import verification, news
from app.core.config import settings

# Initialize app
app = FastAPI(
    title="Veritas - Fake News & Claim Verification API",
    description="A modular, multi-source truth verification system",
    version="1.0.0"
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.info("Starting Veritas system...")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(
    verification.router,
    prefix="/api/v1/verify",
    tags=["Verification"]
)

app.include_router(
    news.router,
    prefix="/api/v1",
    tags=["News"]
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Veritas - Fake News Detection & Claim Verification API",
        "version": app.version,
        "docs_url": "/docs"
    }

# Unified lightweight endpoint for both web and extension
@app.post("/api/fact-check")
async def fact_check(payload: dict = Body(...)):
    """Unified fact-check endpoint returning a simple, fast result."""
    from types import SimpleNamespace
    from app.services import verifier

    text = (payload.get("text") or payload.get("claim") or "").strip()
    if not text:
        return {
            "truth_score": 0.0,
            "confidence_score": 0.0,
            "verdict": "INSUFFICIENT_DATA",
            "summary": "Empty claim text",
            "supporting_sources": [],
            "contradicting_sources": [],
            "processing_time": 0.0
        }

    logger.info(f"[FACT-CHECK] Received text: {text[:120]}")

    req = SimpleNamespace(text=text)
    basic_result = verifier.verify_claim(req)

    # Build response compatible with Chrome extension expectations
    support = basic_result.get('matching_articles', [])
    contradict = basic_result.get('contradicting_articles', [])

    simple = {
        "truth_score": basic_result.get('truth_score', 0.0),
        "confidence_score": basic_result.get('confidence', 0.0),
        "verdict": basic_result.get('verdict', 'INSUFFICIENT_DATA'),
        "summary": f"Found {len(support)} supporting and {len(contradict)} contradicting sources.",
        # Chrome extension expects these field names
        "matching_articles": [
            {"source": a.get('source', 'Unknown'), "url": a.get('url'), "title": a.get('title', 'Untitled'), "similarity_score": a.get('similarity_score')}
            for a in support[:10]
        ],
        "contradicting_articles": [
            {"source": a.get('source', 'Unknown'), "url": a.get('url'), "title": a.get('title', 'Untitled'), "similarity_score": a.get('similarity_score')}
            for a in contradict[:10]
        ],
        # Keep backward compatibility
        "supporting_sources": [
            {"source": a.get('source', 'Unknown'), "url": a.get('url'), "credibility_score": a.get('similarity_score')}
            for a in support[:10]
        ],
        "contradicting_sources": [
            {"source": a.get('source', 'Unknown'), "url": a.get('url'), "credibility_score": a.get('similarity_score')}
            for a in contradict[:10]
        ],
        "processing_time": basic_result.get('processing_time', 0.0)
    }

    # Backward-compat for extension expecting 'confidence'
    simple["confidence"] = simple["confidence_score"]

    return simple
