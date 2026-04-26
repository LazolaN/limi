from app.services.product_matcher import get_eligible_products


def test_smallholder_gets_seed_finance():
    result = get_eligible_products("smallholder", "KwaZulu-Natal", 4.5, risk_score=60)
    product_names = [p.name for p in result.eligible_products]
    assert "Limi Seed Finance" in product_names


def test_smallholder_not_eligible_for_commercial_credit():
    result = get_eligible_products("smallholder", "KwaZulu-Natal", 4.5, risk_score=60)
    product_names = [p.name for p in result.eligible_products]
    assert "Limi Commercial Input Credit" not in product_names


def test_commercial_gets_commercial_credit():
    result = get_eligible_products("commercial", "Free State", 850, risk_score=75)
    product_names = [p.name for p in result.eligible_products]
    assert "Limi Commercial Input Credit" in product_names


def test_commercial_not_eligible_for_seed_finance():
    """Commercial farmers shouldn't see smallholder products."""
    result = get_eligible_products("commercial", "Free State", 850, risk_score=75)
    product_names = [p.name for p in result.eligible_products]
    assert "Limi Seed Finance" not in product_names


def test_insurance_province_restriction():
    """Crop Shield only available in maize provinces."""
    kzn_result = get_eligible_products("smallholder", "KwaZulu-Natal", 4.5, risk_score=60)
    ec_result = get_eligible_products("smallholder", "Eastern Cape", 4.5, risk_score=60)

    kzn_names = [p.name for p in kzn_result.eligible_products]
    ec_names = [p.name for p in ec_result.eligible_products]

    assert "Limi Crop Shield — Maize" in kzn_names
    assert "Limi Crop Shield — Maize" not in ec_names


def test_low_risk_score_excludes_all():
    result = get_eligible_products("smallholder", "KwaZulu-Natal", 4.5, risk_score=10)
    assert len(result.eligible_products) == 0
    assert result.ineligible_reasons is not None


def test_market_connect_available_to_all_types():
    for farm_type in ["smallholder", "emerging", "commercial"]:
        result = get_eligible_products(farm_type, "Free State", 50, risk_score=60)
        product_names = [p.name for p in result.eligible_products]
        assert "Limi Market Connect" in product_names


def test_savings_for_emerging():
    result = get_eligible_products("emerging", "Eastern Cape", 25, risk_score=60)
    product_names = [p.name for p in result.eligible_products]
    assert "Limi Harvest Saver" in product_names
