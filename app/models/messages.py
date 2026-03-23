from datetime import datetime
from pydantic import BaseModel, Field

from app.models.enums import (
    Channel,
    Language,
    ContentType,
    FarmType,
    SubscriptionTier,
    Intent,
    ConfidenceLevel,
    RiskLevel,
)


class InDabaMessage(BaseModel):
    """Inbound message from a farmer via any channel."""

    message_id: str
    farmer_id: str
    channel: Channel
    language: Language
    content_type: ContentType
    content: dict = Field(
        description="Keys: 'text' (str), 'media_url' (str), 'location' (dict with lat/lng)"
    )
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict | None = None


class FarmerProfile(BaseModel):
    """A farmer's profile used to personalise advice."""

    display_name: str
    language: Language
    province: str
    district: str
    farm_type: FarmType
    crops: list[str]
    livestock: list[str]
    farm_size_ha: float
    tier: SubscriptionTier
    nearest_dard_office: str
    nearest_dard_phone: str
    state_vet_phone: str


class KnowledgeChunk(BaseModel):
    """A retrieved chunk from the agricultural knowledge base."""

    source_title: str
    source_type: str  # e.g. "DARD", "ARC", "SAFEX"
    chunk_text: str
    relevance_score: float


class VisionResult(BaseModel):
    """Crop disease vision model output — top-3 predictions."""

    prediction_1: str
    confidence_1: float
    prediction_2: str
    confidence_2: float
    prediction_3: str
    confidence_3: float


class QueryResponse(BaseModel):
    """Response returned to the farmer after advisory processing."""

    message_id: str
    response_text: str
    confidence: ConfidenceLevel
    intent: Intent
    sources_used: list[str]
    channel: Channel
    language: Language
    risk_level: RiskLevel
    escalated: bool = False
