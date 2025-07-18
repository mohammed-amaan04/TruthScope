import logging
import sys
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models.schemas import ClaimRequest, VerificationResult, TextInputRequest, SimpleVerificationResult
from app.core.dependencies import get_verifier

# Add LLM folder to path to import the sophisticated fact-checking system
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'LLM'))

try:
    from fact_check_orchestrator import verify_claim_comprehensive
except ImportError as e:
    logging.error(f"Failed to import LLM fact-checking system: {e}")
    verify_claim_comprehensive = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Singleton verifier instance
verifier = get_verifier()

@router.post("/", response_model=VerificationResult)
async def verify_claim(request: ClaimRequest):
    logger.info("🔍 [API] Received verification request")
    logger.info(f"📄 Claim Text: {request.text}")
    logger.info(f"📄 Claim Type: {request.claim_type}")
    logger.info(f"📄 Language: {request.language}")
    try:
        logger.info("🚀 Starting verification process...")
        result = verifier.verify_claim(request)
        logger.info("✅ Verification completed successfully")
        return result  # ✅ result is already a dict matching VerificationResult
    except Exception as e:
        logger.error(f"❌ [API] Verification pipeline failed: {str(e)}")
        logger.error(f"❌ [API] Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"❌ [API] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal error during verification: {e}")

@router.get("/status")
async def status_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "OK", "message": "Veritas API is running"})

@router.post("/test")
async def test_endpoint(request: dict):
    """Simple test endpoint"""
    logger.info("🧪 [TEST] Received test request")
    logger.info(f"🧪 [TEST] Request data: {request}")
    return {"message": "Test endpoint working", "received": request}


@router.post("/text", response_model=SimpleVerificationResult)
async def verify_text_input(request: TextInputRequest):
    """
    Verify text input using the fact-checking system

    This endpoint accepts text input (headlines, claims, or URLs) and processes them
    through the verification pipeline.
    """
    logger.info("🔍 [TEXT API] Received text verification request")
    logger.info(f"📄 Input Text: {request.text[:100]}...")
    logger.info(f"📄 Input Type: {request.input_type}")

    try:
        logger.info("🚀 Starting verification...")

        # Try to use the sophisticated LLM system first
        if verify_claim_comprehensive:
            try:
                result = await verify_claim_comprehensive(request.text)
                simple_result = _transform_to_simple_result(result)
                logger.info("✅ LLM verification completed successfully")
                return simple_result
            except Exception as llm_error:
                logger.warning(f"⚠️ LLM verification failed, falling back to basic verifier: {llm_error}")

        # Fallback to existing verifier
        from app.models.schemas import ClaimRequest, ClaimType
        claim_request = ClaimRequest(
            text=request.text,
            claim_type=ClaimType.headline,
            language="en"
        )

        basic_result = verifier.verify_claim(claim_request)

        # Transform basic result to simple format
        simple_result = _transform_basic_to_simple_result(basic_result, request.text)

        logger.info("✅ Basic verification completed successfully")
        logger.info(f"📊 Final Result - Truth: {simple_result.truth_score:.1%}, "
                   f"Confidence: {simple_result.confidence_score:.1%}")

        return simple_result

    except Exception as e:
        logger.error(f"❌ [TEXT API] Verification failed: {str(e)}")
        logger.error(f"❌ [TEXT API] Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"❌ [TEXT API] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Verification failed: {e}")


def _transform_to_simple_result(llm_result) -> SimpleVerificationResult:
    """Transform sophisticated LLM result to simple API format"""
    from app.models.schemas import SourceInfo

    # Extract supporting sources
    supporting_sources = []
    for source in llm_result.supporting_sources[:10]:  # Limit to 10 sources
        supporting_sources.append(SourceInfo(
            source=source,
            url=None,  # URL not available in current format
            credibility_score=None  # Could be extracted if needed
        ))

    # Extract contradicting sources
    contradicting_sources = []
    for source in llm_result.contradicting_sources[:10]:  # Limit to 10 sources
        contradicting_sources.append(SourceInfo(
            source=source,
            url=None,
            credibility_score=None
        ))

    return SimpleVerificationResult(
        truth_score=llm_result.final_truth_score,
        confidence_score=llm_result.final_confidence_score,
        verdict=llm_result.final_verdict,
        summary=llm_result.factual_summary,
        supporting_sources=supporting_sources,
        contradicting_sources=contradicting_sources,
        processing_time=llm_result.total_processing_time
    )


def _transform_basic_to_simple_result(basic_result, original_text: str) -> SimpleVerificationResult:
    """Transform basic verifier result to simple API format"""
    from app.models.schemas import SourceInfo

    # Extract supporting sources
    supporting_sources = []
    for article in basic_result.get('matching_articles', [])[:10]:
        supporting_sources.append(SourceInfo(
            source=article.get('source', 'Unknown'),
            url=article.get('url'),
            credibility_score=article.get('similarity_score')
        ))

    # Extract contradicting sources
    contradicting_sources = []
    for article in basic_result.get('contradicting_articles', [])[:10]:
        contradicting_sources.append(SourceInfo(
            source=article.get('source', 'Unknown'),
            url=article.get('url'),
            credibility_score=article.get('similarity_score')
        ))

    # Use verdict directly from the verifier (which now uses new logic)
    verdict = basic_result.get('verdict', 'INSUFFICIENT_DATA')
    truth_score = basic_result.get('truth_score', 0.0)

    # Create summary based on new verdict system
    total_sources = len(supporting_sources) + len(contradicting_sources)
    confidence_score = basic_result.get('confidence', 0.5)

    verdict_descriptions = {
        "MOST_LIKELY_TRUE": "🟢 Highly Reliable - Most Likely True",
        "LIKELY_TRUE_NEEDS_SUPPORT": "🟡 Somewhat Reliable - Likely True, but Needs More Support",
        "INCONCLUSIVE_MIXED": "🟠 Uncertain - Inconclusive / Mixed Evidence",
        "LIKELY_FALSE": "🔴 Suspicious - Likely False",
        "INSUFFICIENT_DATA": "⚫ Unverifiable - Not Enough Data to Verify"
    }

    verdict_desc = verdict_descriptions.get(verdict, verdict)

    if total_sources == 0:
        summary = f"{verdict_desc}. No reliable sources found to verify this claim."
    else:
        summary = f"{verdict_desc}. Found {len(supporting_sources)} supporting and {len(contradicting_sources)} contradicting sources. Truth: {truth_score:.1%}, Confidence: {confidence_score:.1%}"

    return SimpleVerificationResult(
        truth_score=truth_score,
        confidence_score=basic_result.get('confidence', 0.5),
        verdict=verdict,
        summary=summary,
        supporting_sources=supporting_sources,
        contradicting_sources=contradicting_sources,
        processing_time=basic_result.get('processing_time', 0.0)
    )
