# Anthropic pricing per million tokens (USD) as of April 2026
_MODEL_PRICING: dict[str, tuple[float, float]] = {
    # (input_per_million, output_per_million)
    "claude-haiku-4-5-20251001": (1.00, 5.00),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    "claude-opus-4-20250514": (15.00, 75.00),
}

# Fallback for unknown models
_DEFAULT_PRICING = (3.00, 15.00)


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost in USD cents for a single LLM call."""
    input_rate, output_rate = _MODEL_PRICING.get(model, _DEFAULT_PRICING)
    input_cost = (input_tokens / 1_000_000) * input_rate
    output_cost = (output_tokens / 1_000_000) * output_rate
    return round((input_cost + output_cost) * 100, 4)  # Convert to cents
