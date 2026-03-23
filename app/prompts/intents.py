from app.models.enums import Intent
from app.models.messages import VisionResult


def get_intent_instructions(
    intent: Intent,
    vision_results: VisionResult | None = None,
    price_data: str | None = None,
    weather_data: str | None = None,
) -> str:
    """Return intent-specific instructions for the system prompt."""

    if intent == Intent.CROP_DISEASE_ID:
        return _crop_disease_instructions(vision_results)
    elif intent == Intent.MARKET_PRICE:
        return _market_price_instructions(price_data)
    elif intent == Intent.LIVESTOCK_HEALTH:
        return _livestock_health_instructions()
    elif intent == Intent.PLANTING_CALENDAR:
        return _planting_calendar_instructions(weather_data)
    elif intent == Intent.HUMAN_ESCALATION:
        return _human_escalation_instructions()
    else:
        return _generic_instructions(intent)


def _crop_disease_instructions(vision_results: VisionResult | None) -> str:
    if vision_results:
        return f"""INTENT: CROP DISEASE IDENTIFICATION

The vision model classified the image:
Top-1: {vision_results.prediction_1} (confidence: {vision_results.confidence_1}%)
Top-2: {vision_results.prediction_2} (confidence: {vision_results.confidence_2}%)
Top-3: {vision_results.prediction_3} (confidence: {vision_results.confidence_3}%)

INSTRUCTIONS:
1. If top-1 confidence > 80%: Present diagnosis clearly. Name disease in English AND the farmer's language. Describe matching visual symptoms.
2. If top-1 confidence 50-80%: Present as most likely, mention top-2 alternative. Ask one clarifying question to distinguish between them.
3. If top-1 confidence < 50%: Do NOT present a diagnosis. Say you're unsure. Ask farmer to take a closer photo in good lighting, describe symptoms in words, or say "Expert help" to escalate.
4. For confirmed/likely diagnosis provide: cause (fungal/bacterial/viral/nutrient), immediate action (24-48 hrs), treatment options (organic first, then chemical), prevention for future seasons, risk to neighbouring crops.
5. ALWAYS apply Safety Rule 1 (chemical dosages) and Safety Rule 5 (poison prevention)."""

    return """INTENT: CROP DISEASE IDENTIFICATION (no photo provided)

The farmer described symptoms but did not send a photo.
INSTRUCTIONS:
1. Ask the farmer what crop is affected if not stated.
2. Ask 2-3 targeted diagnostic questions based on the symptoms described.
3. Provide your best assessment but clearly state: "Confidence: MEDIUM" or "Confidence: LOW" since there is no photo.
4. Strongly recommend: "For a more accurate diagnosis, send me a photo of the affected plant via WhatsApp."
5. If on USSD channel, present diagnostic questions as numbered menu options."""


def _market_price_instructions(price_data: str | None) -> str:
    data_block = price_data or "No price data currently available."
    return f"""INTENT: MARKET PRICE CHECK

Available price data:
{data_block}

INSTRUCTIONS:
1. Present the requested commodity price clearly with date and source (SAFEX or FPM).
2. Show daily change (up/down percentage).
3. If farmer grows this commodity, contextualise: "At current prices, your estimated farm at average yield could be worth approximately R[estimate]. This is a rough estimate only."
4. NEVER predict future prices. You may note trend direction but add: "Past trends do not guarantee future prices."
5. For USSD: price in 2 lines max. For WhatsApp: include a small table if multiple commodities requested."""


def _livestock_health_instructions() -> str:
    return """INTENT: LIVESTOCK HEALTH TRIAGE

INSTRUCTIONS:
1. If description is vague, ask: Which animal (species, age, sex)? How long has this been happening? How many animals affected? Any recent changes (feed, water, new animals, travel)?
2. Assess severity:
   - EMERGENCY (animal down, bleeding, convulsions, sudden death, fever >40C, multiple animals simultaneously): "Contact your vet immediately. Do NOT move the animal."
   - URGENT (off feed >24hrs, severe limping, visible discharge, swelling, difficulty breathing): Provide first-aid guidance + "Seek veterinary advice within 24 hours."
   - ROUTINE (minor wound, mild diarrhoea in single alert animal, skin condition): Provide home treatment guidance.
3. ALWAYS check for notifiable disease indicators (Safety Rule 2).
4. End ALL livestock advice with: "If symptoms worsen or more animals are affected, contact your veterinarian immediately."
5. Provide active ingredient names, NOT brand names. Include withholding periods for milk/meat."""


def _planting_calendar_instructions(weather_data: str | None) -> str:
    weather_block = ""
    if weather_data:
        weather_block = f"\n\nAvailable weather data:\n{weather_data}"

    return f"""INTENT: PLANTING CALENDAR / SEASONAL ADVICE{weather_block}

INSTRUCTIONS:
1. Base recommendations on farmer's province, district, and altitude.
2. Cross-reference with current weather forecast if available.
3. Provide specific date ranges: "Plant between 15 October and 30 November" not just "plant in spring".
4. Include soil temperature requirements where relevant.
5. If La Nina/El Nino is active, adjust and explain why.
6. For crop rotation queries, consider the farmer's current crop list."""


def _human_escalation_instructions() -> str:
    return """INTENT: HUMAN ESCALATION

The farmer has requested to speak with a human expert.

INSTRUCTIONS:
1. Acknowledge the request warmly: "I understand you'd like to speak with an expert."
2. Log this for expert review (the system will handle routing).
3. Give an SLA: "A specialist will review your query within 24 hours."
4. Provide the nearest DARD office phone number as an immediate alternative.
5. Ask if there's anything else you can help with in the meantime."""


def _generic_instructions(intent: Intent) -> str:
    intent_label = intent.value.replace("_", " ").title()
    return f"""INTENT: {intent_label.upper()}

INSTRUCTIONS:
1. Answer the farmer's question using the knowledge context provided.
2. Apply all relevant safety rules, especially Rule 3 (confidence disclosure) and Rule 5 (poison prevention) if chemicals are mentioned.
3. Be practical and actionable — farmers need steps they can take today.
4. If the knowledge context does not contain enough information to answer confidently, say so honestly and suggest contacting the nearest DARD office."""
