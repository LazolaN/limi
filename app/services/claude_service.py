import json
import logging
import time
import uuid

import anthropic

from app.config import settings
from app.models.enums import Intent, ContentType
from app.models.messages import (
    LimiMessage,
    FarmerProfile,
    QueryResponse,
)
from app.prompts.assembler import assemble_system_prompt
from app.services.intent_classifier import classify_intent
from app.services.confidence_scorer import score_confidence, should_escalate
from app.services.knowledge_service import retrieve_knowledge
from app.services.price_service import get_commodity_prices, format_price_data
from app.services.model_router import select_model
from app.services.cache_service import (
    is_cacheable,
    make_cache_key,
    get_cached_response,
    set_cached_response,
)
from app.services.token_tracker import estimate_cost

logger = logging.getLogger("limi.claude_service")


async def query_limi(
    message: LimiMessage,
    farmer: FarmerProfile,
) -> QueryResponse:
    """
    Main advisory pipeline:
    1. Classify intent from the message
    2. Check cache for stable intents
    3. Retrieve relevant knowledge chunks
    4. Fetch price data if needed
    5. Select optimal model tier
    6. Assemble the modular system prompt
    7. Call Claude API
    8. Score confidence and check for escalation
    9. Cache response if eligible
    10. Return structured response
    """
    pipeline_start = time.monotonic()
    input_tokens = 0
    output_tokens = 0
    cache_hit = False

    # 1. Classify intent
    query_text = message.content.get("text", "")
    intent, risk_level = classify_intent(query_text, message.content_type, message.language)

    # 2. Check cache
    if is_cacheable(intent):
        cache_key = make_cache_key(
            intent=intent.value,
            query=query_text,
            province=farmer.province,
            farm_type=farmer.farm_type.value,
            channel=message.channel.value,
        )
        cached = get_cached_response(cache_key)
        if cached:
            cache_hit = True
            pipeline_duration_ms = (time.monotonic() - pipeline_start) * 1000
            logger.info(json.dumps({
                "event": "query_completed",
                "message_id": message.message_id,
                "farmer_id": message.farmer_id,
                "intent": intent.value,
                "cache_hit": True,
                "pipeline_duration_ms": round(pipeline_duration_ms, 1),
            }))
            return QueryResponse(**cached, cache_hit=True)
    else:
        cache_key = None

    # 3. Retrieve knowledge
    knowledge_chunks = await retrieve_knowledge(query_text, intent)

    # 4. Get price data if relevant
    price_data = None
    if intent == Intent.MARKET_PRICE:
        prices = await get_commodity_prices()
        price_data = format_price_data(prices, farmer.crops)

    # 5. Select model tier (pre-LLM confidence is None — router uses risk + intent)
    llm_model, max_tokens = select_model(intent, risk_level, None, message.channel)

    # 6. Assemble system prompt
    system_prompt = assemble_system_prompt(
        farmer=farmer,
        channel=message.channel,
        intent=intent,
        knowledge_chunks=knowledge_chunks,
        vision_results=None,
        price_data=price_data,
    )

    # 7. Call Claude API
    user_content = query_text or "(No text provided — see attached media)"

    try:
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model=llm_model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
            timeout=30.0,
        )
        response_text = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

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

    # 8. Score confidence and check escalation
    confidence = score_confidence(response_text, intent, knowledge_chunks)
    escalated = should_escalate(confidence, risk_level)

    # 9. Build response
    pipeline_duration_ms = (time.monotonic() - pipeline_start) * 1000
    sources_used = [chunk.source_title for chunk in knowledge_chunks]
    cost_cents = estimate_cost(llm_model, input_tokens, output_tokens)

    query_response = QueryResponse(
        message_id=message.message_id or str(uuid.uuid4()),
        response_text=response_text,
        confidence=confidence,
        intent=intent,
        sources_used=sources_used,
        channel=message.channel,
        language=message.language,
        risk_level=risk_level,
        escalated=escalated,
        llm_model_used=llm_model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_hit=False,
    )

    # 10. Cache if eligible
    if cache_key and is_cacheable(intent) and not escalated:
        set_cached_response(
            cache_key,
            query_response.model_dump(mode="json"),
            intent,
        )

    # Log
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
        "llm_model_used": llm_model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd_cents": cost_cents,
        "cache_hit": False,
    }
    logger.info(json.dumps(log_entry))

    return query_response
