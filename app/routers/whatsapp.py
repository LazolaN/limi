import logging

from fastapi import APIRouter, Query, Request, HTTPException

from app.config import settings
from app.seed_data import DEFAULT_FARMER, SEED_FARMERS
from app.services.claude_service import query_indaba
from app.webhooks.whatsapp_handler import parse_whatsapp_message, format_whatsapp_response

logger = logging.getLogger("indaba.whatsapp")

router = APIRouter()


@router.get("/whatsapp")
async def whatsapp_verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """WhatsApp webhook verification endpoint."""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified successfully")
        return int(hub_challenge) if hub_challenge else ""

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Receive and process incoming WhatsApp messages.

    MVP: Processes the message and returns the response in the HTTP response body.
    Production: Would send the response asynchronously via WhatsApp Cloud API.
    """
    payload = await request.json()

    message = parse_whatsapp_message(payload)
    if not message:
        return {"status": "ok", "detail": "No actionable message in payload"}

    farmer = SEED_FARMERS.get(message.farmer_id, DEFAULT_FARMER)

    try:
        response = await query_indaba(message, farmer)
    except Exception as error:
        logger.error("WhatsApp query failed: %s", error)
        return {"status": "error", "detail": "Failed to process message"}

    # In production, we'd send this via WhatsApp Cloud API.
    # For MVP, return in the HTTP response.
    formatted = format_whatsapp_response(response.response_text, message.farmer_id)

    return {
        "status": "ok",
        "response": formatted,
        "metadata": {
            "intent": response.intent,
            "confidence": response.confidence,
            "escalated": response.escalated,
        },
    }
