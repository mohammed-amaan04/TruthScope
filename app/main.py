import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
