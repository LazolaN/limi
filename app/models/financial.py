from datetime import datetime
from pydantic import BaseModel

from app.models.enums import FinancialProductType, TransactionStatus


class FinancialProduct(BaseModel):
    """A financial product available to farmers."""

    id: str
    product_type: FinancialProductType
    name: str
    description: str
    provider: str
    min_amount: float = 0.0
    max_amount: float = 0.0
    interest_rate_annual: float | None = None
    commission_pct: float | None = None
    eligible_farm_types: list[str] | None = None
    eligible_provinces: list[str] | None = None
    min_farm_size_ha: float = 0.0
    max_farm_size_ha: float = 100000.0
    active: bool = True


class FarmerRiskScore(BaseModel):
    """A farmer's computed risk score for financial product eligibility."""

    farmer_id: str
    score: int  # 0-100
    components: dict | None = None
    last_computed_at: datetime | None = None


class Transaction(BaseModel):
    """A financial product transaction record."""

    id: str
    farmer_id: str
    product_id: str
    transaction_type: TransactionStatus
    amount: float | None = None
    created_at: datetime | None = None


class ProductEligibility(BaseModel):
    """Result of checking a farmer's eligibility for financial products."""

    farmer_id: str
    risk_score: int
    eligible_products: list[FinancialProduct]
    ineligible_reasons: dict[str, str] | None = None
