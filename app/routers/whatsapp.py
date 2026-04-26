"""WhatsApp Cloud API webhook router.

Flow on inbound POST:
  1. Verify HMAC X-Hub-Signature-256 against raw body (skipped only when APP_SECRET is empty in dev)
  2. Parse Meta Cloud API payload → LimiMessage
  3. Schedule background task; return 200 within ~50ms (Meta's 5s SLA)
  4. Background task: STOP handler → DB lookup → language detect → query_limi → send + persist log
"""
import json
import logging
import time

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request

from app.config import settings
from app.db.engine import async_session_factory
from app.db.models import QueryLogDB
from app.models.enums import Language
from app.models.messages import LimiMessage, QueryResponse
from app.services.claude_service import query_limi
from app.services.farmer_service import (
    delete_farmer,
    detect_isixhosa,
    get_farmer_by_phone,
    is_stop_message,
)
from app.services.token_tracker import estimate_cost
from app.services.whatsapp_sender import send_text, verify_signature
from app.webhooks.whatsapp_handler import parse_whatsapp_message

logger = logging.getLogger("limi.whatsapp")

router = APIRouter()


@router.get("/whatsapp")
async def whatsapp_verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta webhook handshake. Meta GETs this with hub.challenge to verify ownership."""
    if (
        settings.WHATSAPP_VERIFY_TOKEN
        and hub_mode == "subscribe"
        and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN
    ):
        logger.info("whatsapp_webhook_verified")
        return int(hub_challenge) if hub_challenge else ""
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive WhatsApp messages from Meta. Returns 200 immediately; LLM call runs async."""
    raw = await request.body()

    if settings.WHATSAPP_APP_SECRET:
        sig = request.headers.get("x-hub-signature-256", "")
        if not verify_signature(raw, sig, settings.WHATSAPP_APP_SECRET):
            logger.warning("whatsapp_webhook_signature_invalid")
            raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {"status": "ok", "detail": "Invalid JSON ignored"}

    message = parse_whatsapp_message(payload)
    if not message:
        return {"status": "ok", "detail": "No actionable message in payload"}

    background_tasks.add_task(_handle_message, message)
    return {"status": "ok"}


async def _handle_message(message: LimiMessage) -> None:
    """Process inbound message asynchronously: STOP, lookup, language, query, send, log."""
    body = (message.content or {}).get("text", "") or ""
    phone = message.farmer_id

    # POPIA opt-out: STOP / cima / yima → delete + confirm
    if is_stop_message(body):
        deleted = await delete_farmer(phone)
        confirmation = (
            "Your data has been deleted. Reply 'molo' to start again."
            if deleted else
            "Nothing to delete. Reply 'molo' to start."
        )
        await send_text(phone, confirmation)
        return

    # DB-backed farmer lookup; reject unregistered numbers (no Anthropic tokens burned)
    farmer = await get_farmer_by_phone(phone)
    if farmer is None:
        await send_text(
            phone,
            "Sorry, this number isn't registered for the Limi pilot. "
            "Please contact the pilot operator to be added.",
        )
        return

    # isiXhosa heuristic overrides farmer profile language for this message only
    if detect_isixhosa(body):
        message.language = Language.ISIXHOSA
    else:
        message.language = farmer.language

    pipeline_start = time.monotonic()
    try:
        response = await query_limi(message, farmer)
    except Exception as exc:
        logger.error("query_limi_failed phone_suffix=%s error=%s", phone[-4:], str(exc))
        await send_text(phone, "Sorry, I'm having trouble right now. Please try again in a moment.")
        return

    pipeline_ms = (time.monotonic() - pipeline_start) * 1000

    await _persist_query_log(message, response, pipeline_ms)

    sent = await send_text(phone, response.response_text)
    if not sent:
        logger.error(
            "whatsapp_send_failed phone_suffix=%s message_id=%s",
            phone[-4:], message.message_id,
        )


async def _persist_query_log(
    message: LimiMessage,
    response: QueryResponse,
    pipeline_ms: float,
) -> None:
    """Best-effort persistence of query_log entry. No-op if DB unavailable."""
    if async_session_factory is None:
        return
    try:
        cost_cents = estimate_cost(
            response.llm_model_used or "",
            response.input_tokens,
            response.output_tokens,
        )
        async with async_session_factory() as session:
            entry = QueryLogDB(
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
                pipeline_duration_ms=round(pipeline_ms, 1),
                llm_model_used=response.llm_model_used or "",
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                cost_usd_cents=cost_cents,
                cache_hit=response.cache_hit,
            )
            session.add(entry)
            await session.commit()
    except Exception as exc:
        logger.warning("query_log_persist_failed error=%s", str(exc))
