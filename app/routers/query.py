import logging
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_session
from app.db.models import QueryLogDB
from app.models.messages import LimiMessage, QueryResponse
from app.seed_data import SEED_FARMERS, DEFAULT_FARMER
from app.services.claude_service import query_limi

logger = logging.getLogger("limi.query_router")

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def advisory_query(
    message: LimiMessage,
    session: AsyncSession | None = Depends(get_session),
) -> QueryResponse:
    """
    Main advisory endpoint.

    Accepts a LimiMessage, looks up the farmer profile,
    runs the full advisory pipeline, and returns a QueryResponse.
    Persists query log to DB if available.
    """
    request_start = time.monotonic()

    # Look up farmer profile (MVP: hardcoded seed data with fallback)
    farmer = SEED_FARMERS.get(message.farmer_id, DEFAULT_FARMER)

    try:
        response = await query_limi(message, farmer)
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

    # Persist query log if DB is available
    if session is not None:
        try:
            query_log = QueryLogDB(
                farmer_id=message.farmer_id,
                message_id=message.message_id,
                session_id=message.session_id,
                intent=response.intent.value,
                confidence=response.confidence.value,
                risk_level=response.risk_level.value,
                channel=message.channel.value,
                language=message.language.value,
                escalated=response.escalated,
                sources_count=len(response.sources_used),
                pipeline_duration_ms=round(duration_ms, 1),
                llm_model_used=response.llm_model_used or "",
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                cost_usd_cents=0.0,
                cache_hit=response.cache_hit,
            )
            session.add(query_log)
            await session.commit()
        except Exception as db_error:
            logger.warning("Failed to persist query log: %s", db_error)

    return response
