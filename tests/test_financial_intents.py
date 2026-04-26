from app.models.enums import ContentType, Intent, Language, RiskLevel
from app.services.intent_classifier import classify_intent


def test_loan_inquiry_english():
    intent, risk = classify_intent("I need a loan for seeds", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.LOAN_INQUIRY
    assert risk == RiskLevel.MEDIUM


def test_loan_inquiry_isizulu():
    intent, risk = classify_intent("Ngifuna imalimboleko", ContentType.TEXT, Language.ISIZULU)
    assert intent == Intent.LOAN_INQUIRY


def test_insurance_inquiry():
    intent, risk = classify_intent("Can I insure my maize crop?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.INSURANCE_INQUIRY
    assert risk == RiskLevel.MEDIUM


def test_savings_inquiry():
    intent, risk = classify_intent("How can I save money from my harvest?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.SAVINGS_INQUIRY
    assert risk == RiskLevel.LOW


def test_savings_inquiry_stokvel():
    intent, risk = classify_intent("Tell me about stokvel options", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.SAVINGS_INQUIRY


def test_market_linkage():
    intent, risk = classify_intent("I want to sell my maize, find a buyer", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.MARKET_LINKAGE
    assert risk == RiskLevel.LOW


def test_market_linkage_isizulu():
    intent, risk = classify_intent("Ngifuna umthengi wombila wami", ContentType.TEXT, Language.ISIZULU)
    assert intent == Intent.MARKET_LINKAGE


def test_price_query_still_works():
    """Ensure MARKET_PRICE isn't broken by financial intents above it."""
    intent, risk = classify_intent("What is the current maize price?", ContentType.TEXT, Language.ENGLISH)
    assert intent == Intent.MARKET_PRICE


def test_financial_disclosure_in_safety_rules():
    """Rule 8 (Financial Disclosure) must appear in assembled prompts."""
    from app.models.enums import Channel
    from app.prompts.assembler import assemble_system_prompt
    from tests.conftest import _make_farmer, _make_chunks

    farmer = _make_farmer()
    chunks = _make_chunks()

    prompt = assemble_system_prompt(
        farmer=farmer,
        channel=Channel.WHATSAPP,
        intent=Intent.LOAN_INQUIRY,
        knowledge_chunks=chunks,
    )
    assert "FINANCIAL DISCLOSURE" in prompt
    assert "National Credit Act" in prompt
    assert "cooling-off period" in prompt
