from app.services.token_tracker import estimate_cost


def test_haiku_cost():
    cost = estimate_cost("claude-haiku-4-5-20251001", 1000, 500)
    assert cost > 0
    assert cost < 1  # Should be very cheap in cents


def test_sonnet_cost():
    cost = estimate_cost("claude-sonnet-4-20250514", 3000, 1000)
    assert cost > 0


def test_opus_cost_higher_than_sonnet():
    sonnet_cost = estimate_cost("claude-sonnet-4-20250514", 3000, 1000)
    opus_cost = estimate_cost("claude-opus-4-20250514", 3000, 1000)
    assert opus_cost > sonnet_cost


def test_zero_tokens_zero_cost():
    cost = estimate_cost("claude-sonnet-4-20250514", 0, 0)
    assert cost == 0.0


def test_unknown_model_uses_default():
    cost = estimate_cost("unknown-model", 1000, 500)
    assert cost > 0  # Should not crash, uses default pricing
