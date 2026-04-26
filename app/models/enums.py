from enum import StrEnum


class Channel(StrEnum):
    USSD = "ussd"
    WHATSAPP = "whatsapp"
    IVR = "ivr"
    WEB = "web"
    SMS = "sms"


class Language(StrEnum):
    ISIZULU = "zu"
    ISIXHOSA = "xh"
    SESOTHO = "st"
    AFRIKAANS = "af"
    ENGLISH = "en"


class ContentType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    LOCATION = "location"


class FarmType(StrEnum):
    SMALLHOLDER = "smallholder"
    EMERGING = "emerging"
    COMMERCIAL = "commercial"


class SubscriptionTier(StrEnum):
    FREE = "free"
    PREMIUM = "premium"


class Intent(StrEnum):
    CROP_DISEASE_ID = "crop_disease_id"
    PEST_MANAGEMENT = "pest_management"
    PLANTING_CALENDAR = "planting_calendar"
    MARKET_PRICE = "market_price"
    WEATHER_FORECAST = "weather_forecast"
    LIVESTOCK_HEALTH = "livestock_health"
    SOIL_FERTILITY = "soil_fertility"
    IRRIGATION_ADVICE = "irrigation_advice"
    INPUT_SOURCING = "input_sourcing"
    GENERAL_AGRI = "general_agri"
    SUBSCRIPTION_MGMT = "subscription_mgmt"
    HUMAN_ESCALATION = "human_escalation"
    LOAN_INQUIRY = "loan_inquiry"
    INSURANCE_INQUIRY = "insurance_inquiry"
    SAVINGS_INQUIRY = "savings_inquiry"
    MARKET_LINKAGE = "market_linkage"


class FinancialProductType(StrEnum):
    INPUT_FINANCING = "input_financing"
    CROP_INSURANCE = "crop_insurance"
    MARKET_LINKAGE = "market_linkage"
    SAVINGS = "savings"


class TransactionStatus(StrEnum):
    INQUIRY = "inquiry"
    APPLICATION = "application"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    REJECTED = "rejected"
    COMPLETED = "completed"


class ConfidenceLevel(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RiskLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
