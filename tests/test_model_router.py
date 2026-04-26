from app.models.enums import Channel, ConfidenceLevel, Intent, RiskLevel
from app.services.model_router import select_model


def test_haiku_for_simple_ussd():
    model, tokens = select_model(Intent.GENERAL_AGRI, RiskLevel.LOW, None, Channel.USSD)
    assert "haiku" in model.lower()
    assert tokens == 512


def test_haiku_for_weather_sms():
    model, tokens = select_model(Intent.WEATHER_FORECAST, RiskLevel.LOW, None, Channel.SMS)
    assert "haiku" in model.lower()


def test_sonnet_for_disease_id():
    model, tokens = select_model(Intent.CROP_DISEASE_ID, RiskLevel.HIGH, None, Channel.WHATSAPP)
    assert "sonnet" in model.lower()
    assert tokens == 1024


def test_sonnet_for_loan_inquiry():
    model, tokens = select_model(Intent.LOAN_INQUIRY, RiskLevel.MEDIUM, None, Channel.WEB)
    assert "sonnet" in model.lower()


def test_opus_for_high_risk_low_confidence():
    model, tokens = select_model(Intent.LIVESTOCK_HEALTH, RiskLevel.HIGH, ConfidenceLevel.LOW, Channel.WHATSAPP)
    assert "opus" in model.lower()
    assert tokens == 2048


def test_opus_for_human_escalation():
    model, tokens = select_model(Intent.HUMAN_ESCALATION, RiskLevel.LOW, None, Channel.WEB)
    assert "opus" in model.lower()


def test_sonnet_default_for_whatsapp():
    """Complex intents on WhatsApp should use Sonnet even if low risk."""
    model, _ = select_model(Intent.GENERAL_AGRI, RiskLevel.LOW, None, Channel.WHATSAPP)
    assert "sonnet" in model.lower()


def test_financial_intents_use_sonnet():
    for intent in [Intent.LOAN_INQUIRY, Intent.INSURANCE_INQUIRY, Intent.MARKET_LINKAGE]:
        model, _ = select_model(intent, RiskLevel.MEDIUM, None, Channel.WHATSAPP)
        assert "sonnet" in model.lower(), f"{intent} should route to Sonnet"
