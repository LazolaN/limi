import re
from app.models.enums import ConfidenceLevel, Intent, RiskLevel
from app.models.messages import KnowledgeChunk

# Intents where lack of knowledge context should force LOW confidence.
_HIGH_RISK_INTENTS = {
    Intent.LIVESTOCK_HEALTH,
    Intent.PEST_MANAGEMENT,
    Intent.CROP_DISEASE_ID,
}

# Phrases that indicate the model itself is uncertain.
_UNCERTAINTY_PHRASES = [
    "i'm not sure",
    "i am not sure",
    "i don't have enough information",
    "i do not have enough information",
    "please consult",
    "consult your extension officer",
    "consult a specialist",
    "i cannot determine",
    "angazi",  # isiZulu: "I don't know"
]


def score_confidence(
    response_text: str,
    intent: Intent,
    knowledge_chunks: list[KnowledgeChunk],
) -> ConfidenceLevel:
    """
    Extract and validate the confidence level from Claude's response.

    1. Check for self-reported confidence label in the response text.
    2. Apply override rules based on intent, knowledge availability, and hedging language.
    """
    self_reported = _extract_self_reported_confidence(response_text)

    # Override: high-risk intent with no knowledge → force LOW
    if intent in _HIGH_RISK_INTENTS and len(knowledge_chunks) == 0:
        return ConfidenceLevel.LOW

    # Override: uncertainty phrases detected → force LOW
    response_lower = response_text.lower()
    for phrase in _UNCERTAINTY_PHRASES:
        if phrase in response_lower:
            return ConfidenceLevel.LOW

    return self_reported


def _extract_self_reported_confidence(response_text: str) -> ConfidenceLevel:
    """Extract the confidence label Claude included in its response."""
    text_upper = response_text.upper()

    # Match patterns like "Confidence: HIGH", "*Confidence:* HIGH", etc.
    match = re.search(r"CONFIDENCE:\s*\*?\s*(HIGH|MEDIUM|LOW)", text_upper)
    if match:
        label = match.group(1)
        return ConfidenceLevel(label)

    # Also match standalone labels like "Ukuqiniseka: KUPHEZULU" (isiZulu HIGH)
    if "KUPHEZULU" in text_upper:
        return ConfidenceLevel.HIGH
    if "KUPHAKATHI" in text_upper:
        return ConfidenceLevel.MEDIUM
    if "KUPHANSI" in text_upper:
        return ConfidenceLevel.LOW

    # Default if model didn't include a label
    return ConfidenceLevel.MEDIUM


def should_escalate(confidence: ConfidenceLevel, risk_level: RiskLevel) -> bool:
    """Determine whether this query should be escalated to a human expert."""
    if confidence == ConfidenceLevel.LOW:
        return True
    if confidence == ConfidenceLevel.MEDIUM and risk_level == RiskLevel.HIGH:
        return True
    return False
