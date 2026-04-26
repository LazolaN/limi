"""
Farmer risk scoring engine for financial product eligibility.

Computes a composite score (0-100) from five weighted components:
- Farm profile (25%): type, size, crop diversity
- Query engagement (25%): advisory usage frequency and breadth
- Advisory compliance (20%): confidence ratio, escalation rate
- Regional risk (15%): province-level agricultural risk
- Financial history (15%): transaction completion rate
"""

import logging
from datetime import datetime, UTC

from app.models.enums import FarmType
from app.models.financial import FarmerRiskScore
from app.models.messages import FarmerProfile

logger = logging.getLogger("limi.risk_scorer")

# Province-level agricultural risk index (higher = lower risk = better score)
# Based on rainfall reliability, infrastructure, market access
_PROVINCE_RISK_INDEX: dict[str, int] = {
    "Western Cape": 75,
    "Free State": 70,
    "North West": 65,
    "Mpumalanga": 70,
    "Gauteng": 60,
    "KwaZulu-Natal": 65,
    "Limpopo": 55,
    "Eastern Cape": 50,
    "Northern Cape": 45,
}


def compute_farm_profile_score(farmer: FarmerProfile) -> int:
    """Score based on farm characteristics (0-100)."""
    score = 0

    # Farm type
    if farmer.farm_type == FarmType.COMMERCIAL:
        score += 40
    elif farmer.farm_type == FarmType.EMERGING:
        score += 30
    else:
        score += 20

    # Farm size (log scale, capped)
    import math
    size_score = min(30, int(math.log2(max(farmer.farm_size_ha, 1)) * 5))
    score += size_score

    # Crop diversity (more crops = more resilient)
    crop_count = len(farmer.crops) if farmer.crops else 0
    score += min(30, crop_count * 10)

    return min(100, score)


def compute_engagement_score(
    query_count_90d: int,
    unique_intents: int,
    session_count: int,
) -> int:
    """Score based on advisory platform usage (0-100)."""
    if query_count_90d == 0:
        return 30  # New user gets neutral-low score

    # Query volume (up to 40 points)
    volume_score = min(40, query_count_90d * 2)

    # Intent diversity (up to 30 points)
    diversity_score = min(30, unique_intents * 10)

    # Session frequency (up to 30 points)
    frequency_score = min(30, session_count * 5)

    return min(100, volume_score + diversity_score + frequency_score)


def compute_compliance_score(
    high_confidence_count: int,
    total_queries: int,
    escalation_count: int,
) -> int:
    """Score based on advisory quality signals (0-100)."""
    if total_queries == 0:
        return 50  # Neutral for new users

    # High confidence ratio (higher = better data quality = lower risk)
    confidence_ratio = high_confidence_count / total_queries
    confidence_score = int(confidence_ratio * 60)

    # Low escalation rate is positive
    escalation_ratio = escalation_count / total_queries
    escalation_score = int((1 - escalation_ratio) * 40)

    return min(100, confidence_score + escalation_score)


def compute_regional_score(province: str) -> int:
    """Score based on province-level agricultural risk (0-100)."""
    return _PROVINCE_RISK_INDEX.get(province, 50)


def compute_financial_history_score(
    completed_transactions: int,
    total_transactions: int,
) -> int:
    """Score based on financial product history (0-100)."""
    if total_transactions == 0:
        return 50  # Neutral for new users

    completion_rate = completed_transactions / total_transactions
    return int(completion_rate * 100)


def compute_risk_score(
    farmer: FarmerProfile,
    query_count_90d: int = 0,
    unique_intents: int = 0,
    session_count: int = 0,
    high_confidence_count: int = 0,
    total_queries: int = 0,
    escalation_count: int = 0,
    completed_transactions: int = 0,
    total_transactions: int = 0,
) -> FarmerRiskScore:
    """
    Compute the composite risk score for a farmer.

    Higher score = lower risk = better eligibility for financial products.
    """
    # Component scores
    farm_score = compute_farm_profile_score(farmer)
    engagement_score = compute_engagement_score(query_count_90d, unique_intents, session_count)
    compliance_score = compute_compliance_score(high_confidence_count, total_queries, escalation_count)
    regional_score = compute_regional_score(farmer.province)
    financial_score = compute_financial_history_score(completed_transactions, total_transactions)

    # Weighted composite
    composite = int(
        farm_score * 0.25
        + engagement_score * 0.25
        + compliance_score * 0.20
        + regional_score * 0.15
        + financial_score * 0.15
    )
    composite = max(0, min(100, composite))

    components = {
        "farm_profile": farm_score,
        "engagement": engagement_score,
        "compliance": compliance_score,
        "regional": regional_score,
        "financial_history": financial_score,
    }

    logger.info(
        "Risk score computed for farmer=%s: %d (components=%s)",
        farmer.display_name,
        composite,
        components,
    )

    return FarmerRiskScore(
        farmer_id="",  # Caller sets this
        score=composite,
        components=components,
        last_computed_at=datetime.now(UTC),
    )
