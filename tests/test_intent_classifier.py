from app.models.enums import ContentType, Intent, Language
from app.services.intent_classifier import classify_intent


def test_maize_price_query():
    intent, _ = classify_intent("What is the maize price?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.MARKET_PRICE


def test_tomato_disease_query():
    intent, _ = classify_intent("My tomato has brown spots", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.CROP_DISEASE_ID


def test_cow_not_eating():
    intent, _ = classify_intent("My cow is not eating", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.LIVESTOCK_HEALTH


def test_planting_calendar():
    intent, _ = classify_intent("When should I plant maize?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.PLANTING_CALENDAR


def test_isizulu_price_query():
    intent, _ = classify_intent("Intengo yombila", ContentType.TEXT, Language.ISIZULU)
    assert intent == Intent.MARKET_PRICE


def test_image_always_disease_id():
    intent, _ = classify_intent("", ContentType.IMAGE, Language.ENGLISH)
    assert intent == Intent.CROP_DISEASE_ID


def test_pest_query():
    intent, _ = classify_intent("How do I spray for aphids?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.PEST_MANAGEMENT


def test_weather_query():
    intent, _ = classify_intent("Will it rain this week?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.WEATHER_FORECAST


def test_soil_query():
    intent, _ = classify_intent("What is the best soil pH for maize?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.SOIL_FERTILITY


def test_escalation_request():
    intent, _ = classify_intent("I need to speak to an expert", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.HUMAN_ESCALATION


def test_default_general():
    intent, _ = classify_intent("Hello, how are you?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.GENERAL_AGRI
