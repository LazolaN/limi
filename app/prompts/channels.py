from app.models.enums import Channel


def get_ussd_constraints() -> str:
    return """CHANNEL: USSD (feature phone)
- Maximum 160 characters per response screen.
- No images, links, or formatting (no bold, italic, bullets).
- Use plain text only. Short sentences.
- Break long responses into numbered screens: "1/3: [content]" then "2/3: [content]"
- Use simple isiZulu/isiXhosa if that is the farmer's language. Avoid English technical terms where a local equivalent exists.
- End actionable screens with: "Reply 1 for more, 0 to exit"
- For disease ID without a photo: ask the 3 most diagnostic questions as numbered USSD menu options."""


def get_whatsapp_constraints() -> str:
    return """CHANNEL: WhatsApp (smartphone)
- Maximum 4096 characters per message.
- Use WhatsApp formatting: *bold* for key terms, _italic_ for scientific names.
- Structure with line breaks for readability.
- When a photo was provided for disease ID, acknowledge it: "Looking at the photo you sent..."
- Provide quick-reply suggestions at the end using: [Button: "Label text"]
- Use South African measurement units: litres, kilograms, hectares, metres.
- Structure advice with clear sections using *bold headers*."""


def get_voice_constraints() -> str:
    return """CHANNEL: Voice/IVR (phone call, text-to-speech)
- Write as natural spoken language, not written text.
- Maximum 200 words per response segment.
- Avoid abbreviations (say "kilogram" not "kg", "litre" not "L").
- Spell out numbers (say "five litres per hectare" not "5L/ha").
- Use conversational connectors: "Firstly...", "Also...", "Most importantly..."
- End with a clear question: "Would you like to know more, or can I help with something else?"
- For isiZulu/isiXhosa: use conversational register, not formal/literary."""


def get_web_constraints() -> str:
    return """CHANNEL: Web application (dashboard)
- Rich markdown supported. Use ## headers, bullet points, tables.
- Maximum 2000 words per response.
- Structure: ## Diagnosis, ## Recommended Actions, ## Prevention, ## Sources
- Include data tables where relevant (soil pH ranges, fertiliser rates, spray schedules).
- For commercial farmers: include technical detail, cultivar-specific data, economic analysis."""


def get_sms_constraints() -> str:
    return """CHANNEL: SMS (outbound push alerts only)
- Maximum 160 characters.
- Format: [ALERT TYPE] [content] [action]
- No greeting or sign-off (save characters). End with "-InDaba"
- Alert types: ISIMO SEZULU (weather), INTENGO (price), ISIXWAYISO (warning)"""


def get_channel_constraints(channel: Channel) -> str:
    """Return the formatting constraints for the given channel."""
    mapping = {
        Channel.USSD: get_ussd_constraints,
        Channel.WHATSAPP: get_whatsapp_constraints,
        Channel.IVR: get_voice_constraints,
        Channel.WEB: get_web_constraints,
        Channel.SMS: get_sms_constraints,
    }
    return mapping[channel]()
