from app.models.enums import Language

# Verified agricultural terminology for SA indigenous languages.
# Key: English term → { language_code: local_term }
AGRICULTURAL_TERMS: dict[str, dict[str, str]] = {
    "Maize": {"zu": "Umbila / Ummbila", "xh": "Umbona"},
    "Disease": {"zu": "Isifo", "xh": "Isifo"},
    "Pest / Insect": {"zu": "Isinambuzane", "xh": "Isinambuzane"},
    "Fertiliser": {"zu": "Umquba / Umanyolo", "xh": "Umanyolo"},
    "Manure (organic)": {"zu": "Umquba wemfuyo", "xh": "Umgquba"},
    "Irrigation": {"zu": "Ukunisela", "xh": "Ukunkcenkceshela"},
    "Harvest": {"zu": "Ukuvuna", "xh": "Ukuvuna"},
    "Planting / Sowing": {"zu": "Ukutshala", "xh": "Ukutyala"},
    "Soil": {"zu": "Umhlabathi / Inhlabathi", "xh": "Umhlaba"},
    "Cattle": {"zu": "Izinkomo", "xh": "Iinkomo"},
    "Goat": {"zu": "Imbuzi", "xh": "Ibhokhwe"},
    "Sheep": {"zu": "Imvu / Izimvu", "xh": "Igusha / Iigusha"},
    "Extension officer": {"zu": "Umeluleki wezolimo", "xh": "Umluleki wezolimo"},
    "Foot-and-mouth": {"zu": "Isifo somlomo nezinselo", "xh": "Isifo somlomo neenzipho"},
    "Drought": {"zu": "Isomiso", "xh": "Imbalela"},
    "Frost": {"zu": "Iqhwa / Isandulela-qhwa", "xh": "Ingqele"},
    "Weeds": {"zu": "Ukhula", "xh": "Ukhula"},
    "Seed": {"zu": "Imbewu", "xh": "Imbewu"},
    "Poison / Pesticide": {"zu": "Isihlungu / Umuthi wezinambuzane", "xh": "Ityhefu"},
}

LANGUAGE_NAMES: dict[str, str] = {
    "zu": "isiZulu",
    "xh": "isiXhosa",
}


def get_terminology_prompt(language: Language) -> str:
    """Return a terminology reference block for isiZulu or isiXhosa. Empty string for other languages."""
    lang_code = language.value

    if lang_code not in LANGUAGE_NAMES:
        return ""

    language_name = LANGUAGE_NAMES[lang_code]
    lines = [
        f"AGRICULTURAL TERMINOLOGY REFERENCE ({language_name}):",
        f"When responding in {language_name}, use these verified local agricultural terms. "
        "Do not substitute with formal/literary alternatives that farmers may not recognise.",
        "",
    ]

    for english_term, translations in AGRICULTURAL_TERMS.items():
        local_term = translations.get(lang_code, english_term)
        lines.append(f"- {english_term}: {local_term}")

    return "\n".join(lines)
