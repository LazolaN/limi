import re
from app.models.enums import ContentType, Intent, Language, RiskLevel

# Keyword groups for rule-based classification.
# Each tuple: (list of keywords, intent, risk_level).
# Checked in order — first match wins.
_KEYWORD_RULES: list[tuple[list[str], Intent, RiskLevel]] = [
    (
        ["price", "cost", "rand", "safex", "intengo", "ixabiso", "r/"],
        Intent.MARKET_PRICE,
        RiskLevel.LOW,
    ),
    (
        [
            "disease", "sick plant", "spots", "blight", "fungus",
            "isifo sesitshalo", "amabala", "leaf", "iqabunga",
            "brown", "yellow leaves", "wilting", "rot",
        ],
        Intent.CROP_DISEASE_ID,
        RiskLevel.HIGH,
    ),
    (
        [
            "cow", "cattle", "goat", "sheep", "chicken", "pig",
            "inkomo", "imbuzi", "imvu", "inkukhu",
            "sick animal", "vet", "limping", "not eating",
            "foam", "bleeding", "fever", "diarrhoea", "swelling",
            "shaking", "convulsions", "down",
        ],
        Intent.LIVESTOCK_HEALTH,
        RiskLevel.HIGH,
    ),
    (
        ["plant", "sow", "when to", "season", "calendar", "tshala", "tyala", "nini"],
        Intent.PLANTING_CALENDAR,
        RiskLevel.MEDIUM,
    ),
    (
        ["pest", "insect", "worm", "aphid", "spray", "isinambuzane", "fafaza", "stalk borer"],
        Intent.PEST_MANAGEMENT,
        RiskLevel.HIGH,
    ),
    (
        ["weather", "rain", "frost", "drought", "isimo sezulu", "imvula", "iqhwa", "isomiso"],
        Intent.WEATHER_FORECAST,
        RiskLevel.LOW,
    ),
    (
        ["soil", "fertiliser", "fertilizer", "manure", "ph", "umhlabathi", "umanyolo", "lime"],
        Intent.SOIL_FERTILITY,
        RiskLevel.MEDIUM,
    ),
    (
        ["irrigat", "water", "ukunisela", "amanzi", "drip", "sprinkler"],
        Intent.IRRIGATION_ADVICE,
        RiskLevel.MEDIUM,
    ),
    (
        ["expert", "help", "human", "extension officer", "umeluleki", "speak to someone"],
        Intent.HUMAN_ESCALATION,
        RiskLevel.LOW,
    ),
]


def classify_intent(
    text: str,
    content_type: ContentType,
    language: Language,
) -> tuple[Intent, RiskLevel]:
    """
    Rule-based intent classification (MVP).

    Priority:
    1. Image content → always CROP_DISEASE_ID
    2. Audio content → GENERAL_AGRI (transcription TBD)
    3. Keyword matching on text (case-insensitive, first match wins)
    4. Default → GENERAL_AGRI
    """
    if content_type == ContentType.IMAGE:
        return Intent.CROP_DISEASE_ID, RiskLevel.HIGH

    if content_type == ContentType.AUDIO:
        return Intent.GENERAL_AGRI, RiskLevel.LOW

    text_lower = text.lower()

    for keywords, intent, risk_level in _KEYWORD_RULES:
        for keyword in keywords:
            if keyword in text_lower:
                return intent, risk_level

    return Intent.GENERAL_AGRI, RiskLevel.LOW
