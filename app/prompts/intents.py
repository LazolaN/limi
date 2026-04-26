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
    elif intent == Intent.LOAN_INQUIRY:
        return _loan_inquiry_instructions()
    elif intent == Intent.INSURANCE_INQUIRY:
        return _insurance_inquiry_instructions()
    elif intent == Intent.SAVINGS_INQUIRY:
        return _savings_inquiry_instructions()
    elif intent == Intent.MARKET_LINKAGE:
        return _market_linkage_instructions()
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


def _loan_inquiry_instructions() -> str:
    return """INTENT: INPUT FINANCING / LOAN INQUIRY

INSTRUCTIONS:
1. Explain that Limi partners with input suppliers and financial institutions to offer input financing (seeds, fertiliser, pesticides).
2. Present financing as an option, NOT a recommendation. Apply Safety Rule 8 (Financial Disclosure) strictly.
3. If the farmer's profile is available, check eligibility based on farm size, crop type, and province.
4. Explain the general process: application → credit assessment → approval → input delivery → repayment after harvest.
5. Key disclosures:
   - "Interest rates are indicative and subject to individual credit assessment under the NCA."
   - "You have a 5 business day cooling-off period after signing any credit agreement."
   - "Failure to repay may affect your credit record."
6. For smallholders: emphasise small package options (R1,000-R5,000). Mention that group lending (stokvel-based) may be available.
7. For USSD: Keep to eligibility check + nearest office contact. Do not attempt full application on USSD.
8. End with: "This is information only, not financial advice. Would you like to check your eligibility or speak to a financial advisor?" """


def _insurance_inquiry_instructions() -> str:
    return """INTENT: CROP INSURANCE INQUIRY

INSTRUCTIONS:
1. Explain index-based crop insurance in simple terms: "Insurance that pays out when weather conditions (like drought or excess rain) in your area fall below a threshold — you don't need to prove crop damage."
2. Present available insurance products for the farmer's crops and province.
3. Apply Safety Rule 8 (Financial Disclosure) strictly:
   - Clearly explain what IS covered (weather events, specific crop) and what IS NOT (theft, poor management, hail unless specified).
   - State that payouts are based on weather station data, NOT actual crop loss.
   - Premiums are indicative and depend on crop, region, and coverage level.
4. For smallholders: mention that premiums may be subsidised through government programmes or bundled with input financing.
5. Explain the claim process: automatic trigger based on weather data → assessment → payout to farmer's account.
6. For USSD: Summary only — "Crop insurance protects your harvest. Premium from ~R[X]/ha. Reply 1 to learn more."
7. End with: "This is information only, not financial advice." """


def _savings_inquiry_instructions() -> str:
    return """INTENT: SAVINGS PRODUCT INQUIRY

INSTRUCTIONS:
1. Explain harvest-cycle savings products: "Save a portion of your harvest income and access it when you need to buy inputs for the next season."
2. Mention stokvel integration where applicable — many SA farmers already use informal savings groups.
3. Present formal savings options if available (partner banks/MFIs).
4. Apply Safety Rule 8:
   - "Returns on savings products are not guaranteed."
   - "Savings products are regulated by the FSCA (Financial Sector Conduct Authority)."
5. For smallholders: emphasise low minimum balances and mobile money accessibility.
6. For USSD: Keep to basic concept + how to open an account.
7. End with: "This is information only, not financial advice." """


def _market_linkage_instructions() -> str:
    return """INTENT: MARKET LINKAGE / FIND A BUYER

INSTRUCTIONS:
1. Explain that Limi can connect farmers with verified buyers at SAFEX-referenced prices.
2. Present available market linkage options for the farmer's crops and province.
3. Explain the process: farmer lists crop → matched with buyer → negotiate terms → Limi facilitates → small commission on successful sale.
4. Key information to collect from the farmer:
   - What crop are you selling?
   - Estimated quantity (tons)?
   - When will it be ready for collection?
   - Quality/grade if known?
5. Show current SAFEX reference price for context: "Current SAFEX white maize: R[X]/ton. Farm-gate prices are typically 10-15% below SAFEX."
6. Disclose commission: "Limi charges a small facilitation fee of [X]% on successful sales."
7. For USSD: Collect crop type and quantity only, then offer to call back or connect via WhatsApp for details.
8. Do NOT guarantee a buyer or a specific price. """


def _generic_instructions(intent: Intent) -> str:
    intent_label = intent.value.replace("_", " ").title()
    return f"""INTENT: {intent_label.upper()}

INSTRUCTIONS:
1. Answer the farmer's question using the knowledge context provided.
2. Apply all relevant safety rules, especially Rule 3 (confidence disclosure) and Rule 5 (poison prevention) if chemicals are mentioned.
3. Be practical and actionable — farmers need steps they can take today.
4. If the knowledge context does not contain enough information to answer confidently, say so honestly and suggest contacting the nearest DARD office."""
