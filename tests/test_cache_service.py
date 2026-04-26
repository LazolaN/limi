from app.models.enums import Intent
from app.services.cache_service import is_cacheable, make_cache_key


def test_market_price_is_cacheable():
    assert is_cacheable(Intent.MARKET_PRICE)


def test_planting_calendar_is_cacheable():
    assert is_cacheable(Intent.PLANTING_CALENDAR)


def test_livestock_not_cacheable():
    assert not is_cacheable(Intent.LIVESTOCK_HEALTH)


def test_disease_not_cacheable():
    assert not is_cacheable(Intent.CROP_DISEASE_ID)


def test_financial_intents_not_cacheable():
    assert not is_cacheable(Intent.LOAN_INQUIRY)
    assert not is_cacheable(Intent.INSURANCE_INQUIRY)
    assert not is_cacheable(Intent.MARKET_LINKAGE)


def test_cache_key_deterministic():
    key1 = make_cache_key("market_price", "maize price", "KZN", "smallholder", "whatsapp")
    key2 = make_cache_key("market_price", "maize price", "KZN", "smallholder", "whatsapp")
    assert key1 == key2


def test_cache_key_normalizes_query():
    """Word order shouldn't matter after normalization."""
    key1 = make_cache_key("market_price", "maize price today", "KZN", "smallholder", "whatsapp")
    key2 = make_cache_key("market_price", "today price maize", "KZN", "smallholder", "whatsapp")
    assert key1 == key2


def test_cache_key_varies_by_province():
    key1 = make_cache_key("market_price", "maize price", "KZN", "smallholder", "whatsapp")
    key2 = make_cache_key("market_price", "maize price", "Free State", "smallholder", "whatsapp")
    assert key1 != key2
