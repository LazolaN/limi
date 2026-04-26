import uuid
from datetime import datetime

from app.models.enums import Channel, Language, ContentType
from app.models.messages import LimiMessage


def parse_whatsapp_message(payload: dict) -> LimiMessage | None:
    """
    Parse an incoming WhatsApp Cloud API webhook payload into a LimiMessage.

    Returns None if the payload doesn't contain a user message (e.g., status updates).
    """
    try:
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return None

        wa_message = messages[0]
        sender = wa_message.get("from", "unknown")
        message_type = wa_message.get("type", "text")

        # Determine content type and extract content
        if message_type == "text":
            content_type = ContentType.TEXT
            content = {"text": wa_message.get("text", {}).get("body", "")}
        elif message_type == "image":
            content_type = ContentType.IMAGE
            image_data = wa_message.get("image", {})
            content = {
                "text": image_data.get("caption", ""),
                "media_url": image_data.get("id", ""),
            }
        elif message_type == "location":
            content_type = ContentType.LOCATION
            loc = wa_message.get("location", {})
            content = {"location": {"lat": loc.get("latitude"), "lng": loc.get("longitude")}}
        elif message_type == "audio":
            content_type = ContentType.AUDIO
            content = {"media_url": wa_message.get("audio", {}).get("id", "")}
        else:
            content_type = ContentType.TEXT
            content = {"text": ""}

        return LimiMessage(
            message_id=wa_message.get("id", str(uuid.uuid4())),
            farmer_id=sender,
            channel=Channel.WHATSAPP,
            language=Language.ENGLISH,  # MVP default; real impl detects from WhatsApp profile
            content_type=content_type,
            content=content,
            session_id=f"wa-{sender}",
            timestamp=datetime.utcnow(),
        )

    except (KeyError, IndexError):
        return None


def format_whatsapp_response(response_text: str, recipient: str) -> dict:
    """Format a response for the WhatsApp Cloud API send message endpoint."""
    return {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": response_text},
    }
