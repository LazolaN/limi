import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FarmerDB(Base):
    __tablename__ = "farmers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(128))
    language: Mapped[str] = mapped_column(String(4))
    province: Mapped[str] = mapped_column(String(64), index=True)
    district: Mapped[str] = mapped_column(String(128))
    farm_type: Mapped[str] = mapped_column(String(20))
    crops: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    livestock: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    farm_size_ha: Mapped[float] = mapped_column(Float)
    tier: Mapped[str] = mapped_column(String(20), default="free")
    nearest_dard_office: Mapped[str] = mapped_column(String(128), default="")
    nearest_dard_phone: Mapped[str] = mapped_column(String(20), default="")
    state_vet_phone: Mapped[str] = mapped_column(String(20), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_farmers_province_district", "province", "district"),
    )


class QueryLogDB(Base):
    __tablename__ = "query_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id: Mapped[str] = mapped_column(String(64), index=True)
    message_id: Mapped[str] = mapped_column(String(128))
    session_id: Mapped[str] = mapped_column(String(128))
    intent: Mapped[str] = mapped_column(String(32), index=True)
    confidence: Mapped[str] = mapped_column(String(8))
    risk_level: Mapped[str] = mapped_column(String(8))
    channel: Mapped[str] = mapped_column(String(16))
    language: Mapped[str] = mapped_column(String(4))
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    sources_count: Mapped[int] = mapped_column(Integer, default=0)
    pipeline_duration_ms: Mapped[float] = mapped_column(Float, default=0.0)
    llm_model_used: Mapped[str] = mapped_column(String(64), default="")
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd_cents: Mapped[float] = mapped_column(Float, default=0.0)
    cache_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_query_logs_farmer_created", "farmer_id", "created_at"),
        Index("ix_query_logs_intent_created", "intent", "created_at"),
        Index("ix_query_logs_channel_created", "channel", "created_at"),
    )


class ConversationDB(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id: Mapped[str] = mapped_column(String(64), index=True)
    session_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    channel: Mapped[str] = mapped_column(String(16))
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_message_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    message_count: Mapped[int] = mapped_column(Integer, default=0)
