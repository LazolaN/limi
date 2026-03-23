import json
import logging
import time
import uuid

import anthropic

from app.config import settings
from app.models.enums import Intent, ContentType
from app.models.messages import (
    InDabaMessage,
    FarmerProfile,
    QueryResponse,
)
from app.prompts.assembler import assemble_system_prompt
from app.services.intent_classifier import classify_intent
from app.services.confidence_scorer import score_confidence, should_escalate
from app.services.knowledge_service import retrieve_knowledge
from app.services.price_service import get_commodity_prices, format_price_data

logger = logging.getLogger("indaba.claude_service")


async def query_indaba(
    message: InDabaMessage,
    farmer: FarmerProfile,
) -> QueryResponse:
    """
    Main advisory pipeline:
    1. Classify intent from the message
    2. Retrieve relevant knowledge chunks
    3. Fetch price data if needed
    4. Assemble the modular system prompt
    5. Call Claude API
    6. Score confidence and check for escalation
    7. Return structured response
    """
    pipeline_start = time.monotonic()

    # 1. Classify intent
    query_text = message.content.get("text", "")
    intent, risk_level = classify_intent(query_text, message.content_type, message.language)

    # 2. Retrieve knowledge
    knowledge_chunks = await retrieve_knowledge(query_text, intent)

    # 3. Get price data if relevant
    price_data = None
    if intent == Intent.MARKET_PRICE:
        prices = await get_commodity_prices()
        price_data = format_price_data(prices, farmer.crops)

    # 4. Assemble system prompt
    system_prompt = assemble_system_prompt(
        farmer=farmer,
        channel=message.channel,
        intent=intent,
        knowledge_chunks=knowledge_chunks,
        vision_results=None,  # Vision model integration is post-MVP
        price_data=price_data,
    )

    # 5. Call Claude API
    user_content = query_text or "(No text provided — see attached media)"

    try:
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=settings.CLAUDE_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
            timeout=30.0,
        )
        response_text = response.content[0].text

    except anthropic.RateLimitError:
        logger.error("Claude API rate limit exceeded")
        response_text = (
            "I'm receiving too many requests right now. "
            "Please try again in a few minutes, or contact your nearest DARD office "
            f"at {farmer.nearest_dard_phone} for immediate assistance."
        )
    except anthropic.APIError as api_error:
        logger.error("Claude API error: %s", api_error)
        response_text = (
            "I'm having trouble processing your request right now. "
            f"Please try again shortly, or call {farmer.nearest_dard_phone} for help."
        )
    except Exception as unexpected_error:
        logger.error("Unexpected error calling Claude: %s", unexpected_error)
        response_text = (
            "Something went wrong. Please try again, or contact your extension officer "
            f"at {farmer.nearest_dard_phone}."
        )

    # 6. Score confidence and check escalation
    confidence = score_confidence(response_text, intent, knowledge_chunks)
    escalated = should_escalate(confidence, risk_level)

    # 7. Log the query
    pipeline_duration_ms = (time.monotonic() - pipeline_start) * 1000
    sources_used = [chunk.source_title for chunk in knowledge_chunks]

    log_entry = {
        "event": "query_completed",
        "message_id": message.message_id,
        "farmer_id": message.farmer_id,
        "intent": intent.value,
        "confidence": confidence.value,
        "risk_level": risk_level.value,
        "escalated": escalated,
        "sources_count": len(knowledge_chunks),
        "channel": message.channel.value,
        "language": message.language.value,
        "pipeline_duration_ms": round(pipeline_duration_ms, 1),
    }
    logger.info(json.dumps(log_entry))

    return QueryResponse(
        message_id=message.message_id or str(uuid.uuid4()),
        response_text=response_text,
        confidence=confidence,
        intent=intent,
        sources_used=sources_used,
        channel=message.channel,
        language=message.language,
        risk_level=risk_level,
        escalated=escalated,
    )
