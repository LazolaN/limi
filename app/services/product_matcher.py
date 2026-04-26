"""
Match farmers to eligible financial products based on profile and risk score.
"""

from app.models.financial import FinancialProduct, ProductEligibility

# Seed financial products (MVP — will come from DB in production)
SEED_PRODUCTS: list[FinancialProduct] = [
    FinancialProduct(
        id="prod-001",
        product_type="input_financing",
        name="Limi Seed Finance",
        description="Input financing for seeds, fertiliser, and crop protection. Pay after harvest.",
        provider="Limi / MAFISA",
        min_amount=1000,
        max_amount=50000,
        interest_rate_annual=12.5,
        eligible_farm_types=["smallholder", "emerging"],
        eligible_provinces=None,  # All provinces
        min_farm_size_ha=0.5,
        max_farm_size_ha=100,
    ),
    FinancialProduct(
        id="prod-002",
        product_type="input_financing",
        name="Limi Commercial Input Credit",
        description="Seasonal input credit facility for commercial farming operations.",
        provider="Limi / ABSA AgriBusiness",
        min_amount=50000,
        max_amount=500000,
        interest_rate_annual=10.5,
        eligible_farm_types=["commercial"],
        eligible_provinces=None,
        min_farm_size_ha=50,
        max_farm_size_ha=100000,
    ),
    FinancialProduct(
        id="prod-003",
        product_type="crop_insurance",
        name="Limi Crop Shield — Maize",
        description="Index-based drought insurance for maize. Automatic payout when rainfall drops below threshold.",
        provider="Limi / Pula Advisors",
        min_amount=200,
        max_amount=5000,
        commission_pct=15.0,
        eligible_farm_types=["smallholder", "emerging", "commercial"],
        eligible_provinces=["KwaZulu-Natal", "Free State", "Mpumalanga", "North West"],
        min_farm_size_ha=0.5,
        max_farm_size_ha=100000,
    ),
    FinancialProduct(
        id="prod-004",
        product_type="market_linkage",
        name="Limi Market Connect",
        description="Connect with verified grain buyers at SAFEX-referenced prices.",
        provider="Limi",
        min_amount=0,
        max_amount=0,
        commission_pct=2.5,
        eligible_farm_types=["smallholder", "emerging", "commercial"],
        eligible_provinces=None,
        min_farm_size_ha=1.0,
        max_farm_size_ha=100000,
    ),
    FinancialProduct(
        id="prod-005",
        product_type="savings",
        name="Limi Harvest Saver",
        description="Seasonal savings account — deposit after harvest, access before planting. Higher rates than standard savings.",
        provider="Limi / TymeBank",
        min_amount=100,
        max_amount=100000,
        interest_rate_annual=8.5,
        eligible_farm_types=["smallholder", "emerging"],
        eligible_provinces=None,
        min_farm_size_ha=0,
        max_farm_size_ha=100000,
    ),
]


def get_eligible_products(
    farm_type: str,
    province: str,
    farm_size_ha: float,
    risk_score: int,
    min_risk_score: int = 25,
) -> ProductEligibility:
    """
    Filter financial products by farmer eligibility.

    Returns matching products sorted by relevance.
    """
    eligible = []
    reasons: dict[str, str] = {}

    for product in SEED_PRODUCTS:
        # Check risk score threshold
        if risk_score < min_risk_score:
            reasons[product.id] = f"Risk score {risk_score} below minimum {min_risk_score}"
            continue

        # Check farm type
        if product.eligible_farm_types and farm_type not in product.eligible_farm_types:
            reasons[product.id] = f"Farm type '{farm_type}' not eligible"
            continue

        # Check province
        if product.eligible_provinces and province not in product.eligible_provinces:
            reasons[product.id] = f"Province '{province}' not in eligible regions"
            continue

        # Check farm size
        if farm_size_ha < product.min_farm_size_ha:
            reasons[product.id] = f"Farm size {farm_size_ha}ha below minimum {product.min_farm_size_ha}ha"
            continue
        if farm_size_ha > product.max_farm_size_ha:
            reasons[product.id] = f"Farm size {farm_size_ha}ha above maximum {product.max_farm_size_ha}ha"
            continue

        eligible.append(product)

    return ProductEligibility(
        farmer_id="",  # Caller sets this
        risk_score=risk_score,
        eligible_products=eligible,
        ineligible_reasons=reasons if reasons else None,
    )
