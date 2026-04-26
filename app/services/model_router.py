from app.config import settings
from app.models.enums import Channel, ConfidenceLevel, Intent, RiskLevel

# Intents safe for the cheapest model
_HAIKU_INTENTS = {
    Intent.GENERAL_AGRI,
    Intent.WEATHER_FORECAST,
    Intent.PLANTING_CALENDAR,
    Intent.SUBSCRIPTION_MGMT,
    Intent.SAVINGS_INQUIRY,
}

# Latency-sensitive channels where Haiku's speed matters
_FAST_CHANNELS = {Channel.USSD, Channel.SMS}


def select_model(
    intent: Intent,
    risk_level: RiskLevel,
    confidence: ConfidenceLevel | None,
    channel: Channel,
) -> tuple[str, int]:
    """
    Route to the optimal Claude model based on query characteristics.

    Returns (model_name, max_tokens).

    Tier 4 (Opus):  HIGH risk + LOW confidence, or livestock emergency
    Tier 3 (Sonnet): Complex advisory, financial intents — default
    Tier 2 (Haiku):  Simple intents on fast channels with LOW risk
    """
    # Tier 4: Opus for high-stakes queries
    if risk_level == RiskLevel.HIGH and confidence == ConfidenceLevel.LOW:
        return settings.CLAUDE_MODEL_OPUS, 2048

    if intent == Intent.HUMAN_ESCALATION:
        return settings.CLAUDE_MODEL_OPUS, 2048

    # Tier 2: Haiku for simple, low-risk queries on fast channels
    if (
        intent in _HAIKU_INTENTS
        and risk_level == RiskLevel.LOW
        and channel in _FAST_CHANNELS
    ):
        return settings.CLAUDE_MODEL_HAIKU, 512

    # Tier 3: Sonnet for everything else
    return settings.CLAUDE_MODEL_SONNET, 1024
