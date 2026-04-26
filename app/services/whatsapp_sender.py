"""WhatsApp Cloud API send service.

Sends outgoing messages to farmers via Meta's Graph API. Handles retries on 5xx,
logs structured events with hashed recipient (no raw phone numbers in logs),
and caps message length to WhatsApp's 4096-char text limit.
"""
import asyncio
import hashlib
import logging
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger("limi.whatsapp.sender")

_client: Optional[httpx.AsyncClient] = None


async def get_client() -> httpx.AsyncClient:
    """Lazy-init module-level httpx client (closed on app shutdown)."""
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=15.0)
    return _client


async def close_client() -> None:
    """Dispose the httpx client; called from FastAPI lifespan shutdown."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def _recipient_hash(recipient: str) -> str:
    """Short SHA-256 hash for log-safe recipient identification (no raw PII)."""
    return hashlib.sha256(recipient.encode()).hexdigest()[:8]


async def send_text(recipient: str, body: str) -> bool:
    """Send a text message via WhatsApp Cloud API.

    `recipient` is the E.164 phone number; leading '+' is stripped (Meta format).
    Returns True on 200; False on any failure.
    """
    if not settings.WHATSAPP_PHONE_NUMBER_ID or not settings.WHATSAPP_ACCESS_TOKEN:
        logger.error("whatsapp_send_skipped_missing_config")
        return False

    url = f"{settings.WHATSAPP_API_BASE_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient.lstrip("+"),
        "type": "text",
        "text": {"body": body[:4096]},
    }

    client = await get_client()
    rcpt = _recipient_hash(recipient)

    for attempt in range(3):
        try:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                wa_id = ""
                try:
                    wa_id = resp.json().get("messages", [{}])[0].get("id", "")
                except (ValueError, KeyError, IndexError, TypeError):
                    pass
                logger.info(
                    "whatsapp_send_ok recipient=%s wa_id=%s body_len=%d",
                    rcpt, wa_id, len(body),
                )
                return True
            if 400 <= resp.status_code < 500:
                logger.error(
                    "whatsapp_send_4xx recipient=%s status=%d body=%s",
                    rcpt, resp.status_code, resp.text[:500],
                )
                return False
            logger.warning(
                "whatsapp_send_5xx recipient=%s status=%d attempt=%d",
                rcpt, resp.status_code, attempt + 1,
            )
        except (httpx.RequestError, httpx.HTTPError) as exc:
            logger.warning(
                "whatsapp_send_net_error recipient=%s attempt=%d error=%s",
                rcpt, attempt + 1, str(exc),
            )
        if attempt < 2:
            await asyncio.sleep(0.5 * (2 ** attempt))

    logger.error("whatsapp_send_failed_after_retries recipient=%s", rcpt)
    return False


def verify_signature(body: bytes, signature_header: str, app_secret: str) -> bool:
    """Verify Meta's X-Hub-Signature-256 header against the raw request body.

    Meta sends 'sha256=<hex_digest>'. We HMAC the raw bytes with the app secret
    and constant-time compare. Returns True only on a valid signature.
    """
    import hmac
    if not signature_header or not signature_header.startswith("sha256=") or not app_secret:
        return False
    expected = hmac.new(
        app_secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
    received = signature_header[len("sha256="):]
    return hmac.compare_digest(expected, received)
