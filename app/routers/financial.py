import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_session
from app.models.financial import FinancialProduct, FarmerRiskScore, ProductEligibility
from app.seed_data import SEED_FARMERS, DEFAULT_FARMER
from app.services.risk_scorer import compute_risk_score
from app.services.product_matcher import SEED_PRODUCTS, get_eligible_products

logger = logging.getLogger("limi.financial")

router = APIRouter()


@router.get("/products", response_model=list[FinancialProduct])
async def list_products():
    """List all active financial products."""
    return [p for p in SEED_PRODUCTS if p.active]


@router.get("/products/{farmer_id}", response_model=ProductEligibility)
async def eligible_products(farmer_id: str):
    """Get financial products eligible for a specific farmer."""
    farmer = SEED_FARMERS.get(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    risk = compute_risk_score(farmer)
    result = get_eligible_products(
        farm_type=farmer.farm_type.value,
        province=farmer.province,
        farm_size_ha=farmer.farm_size_ha,
        risk_score=risk.score,
    )
    result.farmer_id = farmer_id
    return result


@router.get("/risk-score/{farmer_id}", response_model=FarmerRiskScore)
async def farmer_risk_score(farmer_id: str):
    """Get or compute a farmer's risk score."""
    farmer = SEED_FARMERS.get(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    risk = compute_risk_score(farmer)
    risk.farmer_id = farmer_id
    return risk
