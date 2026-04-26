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
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FinancialProductDB(Base):
    __tablename__ = "financial_products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_type: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(128))
    min_amount: Mapped[float] = mapped_column(Float, default=0.0)
    max_amount: Mapped[float] = mapped_column(Float, default=0.0)
    interest_rate_annual: Mapped[float | None] = mapped_column(Float, nullable=True)
    commission_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    eligible_farm_types: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    eligible_provinces: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    min_farm_size_ha: Mapped[float] = mapped_column(Float, default=0.0)
    max_farm_size_ha: Mapped[float] = mapped_column(Float, default=100000.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class FarmerRiskScoreDB(Base):
    __tablename__ = "farmer_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    score: Mapped[int] = mapped_column(Integer, default=50)
    components: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    last_computed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    query_count_at_computation: Mapped[int] = mapped_column(Integer, default=0)


class TransactionDB(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id: Mapped[str] = mapped_column(String(64), index=True)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    transaction_type: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_transactions_farmer_created", "farmer_id", "created_at"),
        Index("ix_transactions_product_created", "product_id", "created_at"),
    )


class InputFinancingDB(Base):
    __tablename__ = "input_financing"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    supplier_name: Mapped[str] = mapped_column(String(128))
    input_type: Mapped[str] = mapped_column(String(32))
    repayment_term_months: Mapped[int] = mapped_column(Integer, default=6)
    status: Mapped[str] = mapped_column(String(20), default="pending")


class CropInsuranceDB(Base):
    __tablename__ = "crop_insurance"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    crop: Mapped[str] = mapped_column(String(64))
    insured_hectares: Mapped[float] = mapped_column(Float)
    premium_amount: Mapped[float] = mapped_column(Float)
    payout_trigger: Mapped[str] = mapped_column(String(256), default="")
    policy_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    policy_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")


class MarketLinkageDB(Base):
    __tablename__ = "market_linkage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    buyer_name: Mapped[str] = mapped_column(String(128))
    commodity: Mapped[str] = mapped_column(String(64))
    quantity_tons: Mapped[float] = mapped_column(Float, default=0.0)
    agreed_price_per_ton: Mapped[float] = mapped_column(Float, default=0.0)
    commission_amount: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="pending")
