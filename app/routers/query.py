import logging
import time

from fastapi import APIRouter, HTTPException

from app.models.messages import InDabaMessage, QueryResponse
from app.seed_data import SEED_FARMERS, DEFAULT_FARMER
from app.services.claude_service import query_indaba

logger = logging.getLogger("indaba.query_router")

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def advisory_query(message: InDabaMessage) -> QueryResponse:
    """
    Main advisory endpoint.

    Accepts an InDabaMessage, looks up the farmer profile,
    runs the full advisory pipeline, and returns a QueryResponse.
    """
    request_start = time.monotonic()

    # Look up farmer profile (MVP: hardcoded seed data with fallback)
    farmer = SEED_FARMERS.get(message.farmer_id, DEFAULT_FARMER)

    try:
        response = await query_indaba(message, farmer)
    except Exception as error:
        logger.error("Advisory query failed: %s", error)
        raise HTTPException(
            status_code=500,
            detail="Failed to process advisory query. Please try again.",
        )

    duration_ms = (time.monotonic() - request_start) * 1000
    logger.info(
        "Request completed in %.1fms for farmer=%s intent=%s",
        duration_ms,
        message.farmer_id,
        response.intent,
    )

    return response
