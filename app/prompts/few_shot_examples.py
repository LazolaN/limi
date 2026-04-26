from app.models.enums import Intent, Language, Channel


def get_few_shot_examples(intent: Intent, language: Language, channel: Channel) -> str:
    """Return 1-2 relevant few-shot examples for the given intent, language, and channel combo."""

    # Disease ID + isiZulu + WhatsApp (with photo)
    if intent == Intent.CROP_DISEASE_ID and language == Language.ISIZULU and channel == Channel.WHATSAPP:
        return """User: [Photo] Kwenzakalani emibileni yami?
Limi: *Sawubona! Ngibheke isithombe sakho.*

*Ukuhlonza:* Northern Corn Leaf Blight (Isifo samaqabunga ommbila)
Sibangelwa yisikhunta _Exserohilum turcicum_.
*Confidence: HIGH*

*Okumele ukwenze manje:*
1. Susa amaqabunga asehlulekile ngezansi
2. Fafaza nge-fungicide ye-triazole (e.g., Abacus at 1L/ha) ngokusho kwelabela lomkhiqizo
3. Qiniseka ukuthi izitshalo zinenkundla eyanele yomoya

*Ukuphepha:*
Linda izinsuku ezingu-14 ngaphambi kokuvuna.
Gqoka amaglavu, isimfonyo, nezingubo ezinde.
Poison Info Centre: 0861 555 777

[Button: Ngitholakala kuphi?] [Button: Ukunqanda]"""

    # Livestock Emergency + English + USSD
    if intent == Intent.LIVESTOCK_HEALTH and language == Language.ENGLISH and channel == Channel.USSD:
        return """User: My cow is shaking and has foam at mouth
Limi: 1/2: [!] URGENT: These symptoms may indicate a serious condition. Do NOT move the animal. Isolate it immediately.
Reply 1 for next >

2/2: Call state vet NOW. If multiple cattle affected, may be notifiable disease. Keep others away.
0. Exit"""

    # Market Price + English + WhatsApp (commercial farmer)
    if intent == Intent.MARKET_PRICE and language == Language.ENGLISH and channel == Channel.WHATSAPP:
        return """User: What's the maize price today?
Limi: *SAFEX Prices (22 March 2026):*

*White Maize (Jul26):* R4,850/ton (-1.2%)
*Yellow Maize (Jul26):* R4,720/ton (-0.8%)

Based on your 120 ha at average yield of 5.5 tons/ha, estimated crop value is approximately R3.2M at current white maize prices.

_This is an estimate only. Past trends do not guarantee future prices._

[Button: Weekly trend] [Button: Soya price]"""

    # Low Confidence + isiZulu + USSD
    if intent == Intent.CROP_DISEASE_ID and language == Language.ISIZULU and channel == Channel.USSD:
        return """User: Isitshalo sami siyabuna kodwa ngiyasithelela
Limi: 1/2: Isitshalo esibunayo singaba nezimbangela eziningi. Yisiphi isitshalo?
1. Umbila
2. Utamatisi
3. Amazambane
4. Okunye

2/2: Ukuqiniseka: KUPHANSI.
Thumela isithombe nge-WhatsApp ku-0XX XXX XXXX.
0. Phuma"""

    # Generic disease ID example for WhatsApp English
    if intent == Intent.CROP_DISEASE_ID and channel == Channel.WHATSAPP:
        return """User: My tomato plants have brown spots on the leaves
Limi: *Looking at your description...*

This could be *Early Blight* (_Alternaria solani_) or *Septoria Leaf Spot* — both are common in South African tomato crops.

*Confidence: MEDIUM* (no photo provided)

To narrow it down, can you tell me:
1. Are the spots circular with ring patterns (like a target)?
2. Do the spots start on the lower/older leaves first?
3. Are there any dark spots on the stems as well?

For a more accurate diagnosis, please send me a photo of the affected leaves via WhatsApp.

[Button: Send photo] [Button: Describe more]"""

    # Livestock health for WhatsApp English
    if intent == Intent.LIVESTOCK_HEALTH and channel == Channel.WHATSAPP:
        return """User: My goat is limping on the front leg since yesterday
Limi: *Let me help with your goat.*

*Confidence: MEDIUM*

A few questions to assess this better:
1. Can you see any wound, swelling, or heat on the leg?
2. Is the goat still eating and drinking normally?
3. Has the goat been in contact with any new animals recently?

*In the meantime:*
- Keep the goat in a clean, dry area
- Check between the hooves for foreign objects or sores
- If there is swelling, a cold compress may help

If symptoms worsen or more animals are affected, contact your veterinarian immediately.

[Button: Wound visible] [Button: Not eating]"""

    # Loan inquiry + isiZulu + WhatsApp
    if intent == Intent.LOAN_INQUIRY and language == Language.ISIZULU and channel == Channel.WHATSAPP:
        return """User: Ngifuna imalimboleko yembewu yombila
Limi: *Sawubona! Ngingakusiza ngoxhaso lwezimali zokutshala.*

Limi inezinhlelo zokuxhasa abalimi ngezimpahla zokutshala (imbewu, umanyolo, imithi) okukhokhelwa ngemuva kokuvuna.

*Lokho okufanele ukwazi:*
- Izindleko zembewu yombila: R2,000-R8,000 ngehektare
- Ukukhokhela: izinyanga ezi-4 kuya kwezi-8 ngemva kokuvuna
- Inzalo: iqala ku-10% ngonyaka (ihlolwa ngamunye)

*Okubalulekile:*
- Izinga lenzalo nezikhokho kuya ngohlolo lokuboleka ngaphansi koMthetho Wesikweletu Kazwelonke (NCA)
- Unezinsuku eziyi-5 zokuhoxa ngemuva kokusayina

_Lokhu kuwulwazi kuphela, akuyona iseluleko sezezimali._

[Button: Hlola ukufaneleka] [Button: Khuluma nomeluleki]"""

    # Insurance inquiry + English + Web
    if intent == Intent.INSURANCE_INQUIRY and channel == Channel.WEB:
        return """User: How does crop insurance work for maize?
Limi: ## Index-Based Crop Insurance for Maize

Index-based crop insurance pays out when weather conditions in your area cross a predefined threshold — you don't need to prove actual crop damage.

### How it works
1. **You select** a crop and coverage level
2. **Premium** is calculated based on your region and crop (typically R200-R800/ha)
3. **If drought occurs** (e.g., rainfall below 200mm during Oct-Jan in KZN), the policy triggers automatically
4. **Payout** is deposited directly to your account — no claims process needed

### What IS covered
- Drought (insufficient rainfall)
- Excess moisture/waterlogging

### What is NOT covered
- Theft, fire, poor management, hail (unless specifically included)
- Actual crop loss if the weather index threshold is not triggered

### Important
- Premiums may be subsidised up to 50% for emerging farmers through government programmes
- Payouts are based on weather station data, not your specific farm

*This is information only, not financial advice. Consult a registered financial advisor for personalised recommendations.*"""

    return ""
