from app.models.enums import FarmType, Language, SubscriptionTier
from app.models.messages import FarmerProfile
from app.services.risk_scorer import (
    compute_risk_score,
    compute_farm_profile_score,
    compute_engagement_score,
    compute_compliance_score,
    compute_regional_score,
    compute_financial_history_score,
)


def _make_farmer(**overrides) -> FarmerProfile:
    defaults = dict(
        display_name="Test",
        language=Language.ENGLISH,
        province="KwaZulu-Natal",
        district="Test",
        farm_type=FarmType.SMALLHOLDER,
        crops=["maize"],
        livestock=[],
        farm_size_ha=4.5,
        tier=SubscriptionTier.FREE,
        nearest_dard_office="Test",
        nearest_dard_phone="000",
        state_vet_phone="000",
    )
    defaults.update(overrides)
    return FarmerProfile(**defaults)


def test_score_bounded_0_100():
    farmer = _make_farmer()
    result = compute_risk_score(farmer)
    assert 0 <= result.score <= 100


def test_commercial_scores_higher_than_smallholder():
    small = compute_farm_profile_score(_make_farmer(farm_type=FarmType.SMALLHOLDER))
    commercial = compute_farm_profile_score(_make_farmer(farm_type=FarmType.COMMERCIAL, farm_size_ha=500, crops=["maize", "wheat", "soya"]))
    assert commercial > small


def test_engagement_new_user_neutral():
    score = compute_engagement_score(0, 0, 0)
    assert score == 30


def test_engagement_active_user_higher():
    new_score = compute_engagement_score(0, 0, 0)
    active_score = compute_engagement_score(20, 5, 8)
    assert active_score > new_score


def test_compliance_high_confidence_scores_well():
    score = compute_compliance_score(high_confidence_count=18, total_queries=20, escalation_count=1)
    assert score > 70


def test_regional_kzn():
    score = compute_regional_score("KwaZulu-Natal")
    assert score == 65


def test_regional_unknown_province():
    score = compute_regional_score("Unknown Province")
    assert score == 50


def test_financial_history_perfect():
    score = compute_financial_history_score(10, 10)
    assert score == 100


def test_financial_history_new_user():
    score = compute_financial_history_score(0, 0)
    assert score == 50


def test_composite_has_all_components():
    farmer = _make_farmer()
    result = compute_risk_score(farmer, query_count_90d=5, unique_intents=3, session_count=2)
    assert result.components is not None
    assert "farm_profile" in result.components
    assert "engagement" in result.components
    assert "compliance" in result.components
    assert "regional" in result.components
    assert "financial_history" in result.components
