import hashlib
import json
import logging

from app.config import settings
from app.models.enums import Intent

logger = logging.getLogger("limi.cache")

# Intents whose responses are stable enough to cache
_CACHEABLE_INTENTS: dict[Intent, int] = {
    Intent.MARKET_PRICE: 3600,       # 1 hour
    Intent.PLANTING_CALENDAR: 86400, # 24 hours
    Intent.WEATHER_FORECAST: 3600,   # 1 hour
    Intent.GENERAL_AGRI: 14400,      # 4 hours
}

_redis_client = None


def _get_redis():
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not settings.REDIS_CACHE_ENABLED:
        return None
    try:
        import redis
        _redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        _redis_client.ping()
        logger.info("Redis cache connected")
        return _redis_client
    except Exception as exc:
        logger.warning("Redis unavailable, caching disabled: %s", exc)
        _redis_client = None
        return None


def is_cacheable(intent: Intent) -> bool:
    return intent in _CACHEABLE_INTENTS


def make_cache_key(
    intent: str,
    query: str,
    province: str,
    farm_type: str,
    channel: str,
) -> str:
    """Generate a deterministic cache key from query parameters."""
    normalized = " ".join(sorted(query.lower().split()))
    raw = f"{intent}:{normalized}:{province}:{farm_type}:{channel}"
    return f"limi:resp:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def get_cached_response(cache_key: str) -> dict | None:
    """Retrieve a cached response, or None if miss or Redis unavailable."""
    client = _get_redis()
    if client is None:
        return None
    try:
        data = client.get(cache_key)
        if data:
            logger.debug("Cache hit: %s", cache_key)
            return json.loads(data)
    except Exception as exc:
        logger.warning("Cache read failed: %s", exc)
    return None


def set_cached_response(cache_key: str, response_data: dict, intent: Intent) -> None:
    """Cache a response with intent-specific TTL."""
    client = _get_redis()
    if client is None:
        return
    ttl = _CACHEABLE_INTENTS.get(intent, settings.REDIS_CACHE_DEFAULT_TTL)
    try:
        client.setex(cache_key, ttl, json.dumps(response_data))
        logger.debug("Cached response: %s (TTL=%ds)", cache_key, ttl)
    except Exception as exc:
        logger.warning("Cache write failed: %s", exc)
