SAFEX_PRICES = {
    "white_maize_jul26": {"price": 4850, "change": -1.2, "unit": "R/ton"},
    "yellow_maize_jul26": {"price": 4720, "change": -0.8, "unit": "R/ton"},
    "soybeans_may26": {"price": 8920, "change": 0.5, "unit": "R/ton"},
    "wheat_jul26": {"price": 6350, "change": -0.3, "unit": "R/ton"},
    "sunflower_may26": {"price": 7800, "change": 1.1, "unit": "R/ton"},
    "date": "2026-03-22",
    "source": "SAFEX (JSE)",
}

# Map farmer crop names to SAFEX commodity keys.
_CROP_TO_COMMODITY: dict[str, list[str]] = {
    "maize": ["white_maize_jul26", "yellow_maize_jul26"],
    "soybeans": ["soybeans_may26"],
    "soya": ["soybeans_may26"],
    "wheat": ["wheat_jul26"],
    "sunflower": ["sunflower_may26"],
}


async def get_commodity_prices() -> dict:
    """Return current SAFEX commodity prices (stub with hardcoded data for MVP)."""
    return SAFEX_PRICES


def format_price_data(prices: dict, crops: list[str]) -> str:
    """Format SAFEX prices relevant to the farmer's crop list for prompt injection."""
    date = prices.get("date", "unknown date")
    source = prices.get("source", "SAFEX")

    lines = [f"SAFEX Commodity Prices ({date}, source: {source}):"]

    # Collect relevant commodities based on farmer's crops
    relevant_keys: set[str] = set()
    for crop in crops:
        crop_lower = crop.lower()
        for crop_keyword, commodity_keys in _CROP_TO_COMMODITY.items():
            if crop_keyword in crop_lower:
                relevant_keys.update(commodity_keys)

    # If no crop-specific match, show all commodities
    if not relevant_keys:
        relevant_keys = {
            key for key in prices if isinstance(prices[key], dict)
        }

    for key in sorted(relevant_keys):
        commodity_data = prices.get(key)
        if not isinstance(commodity_data, dict):
            continue

        display_name = key.replace("_", " ").title()
        price = commodity_data["price"]
        change = commodity_data["change"]
        unit = commodity_data["unit"]
        direction = "+" if change >= 0 else ""

        lines.append(f"  {display_name}: R{price:,}/{unit.split('/')[1]} ({direction}{change}%)")

    return "\n".join(lines)
