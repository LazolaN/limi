from app.models.enums import Channel
from app.prompts.channels import get_channel_constraints


def test_ussd_constraints():
    result = get_channel_constraints(Channel.USSD)
    assert "160 characters" in result
    assert "feature phone" in result


def test_whatsapp_constraints():
    result = get_channel_constraints(Channel.WHATSAPP)
    assert "4096 characters" in result
    assert "*bold*" in result


def test_voice_constraints():
    result = get_channel_constraints(Channel.IVR)
    assert "spoken language" in result
    assert "200 words" in result


def test_web_constraints():
    result = get_channel_constraints(Channel.WEB)
    assert "markdown" in result.lower()
    assert "2000 words" in result


def test_sms_constraints():
    result = get_channel_constraints(Channel.SMS)
    assert "160 characters" in result
    assert "Limi" in result


def test_all_channels_return_non_empty():
    for channel in Channel:
        result = get_channel_constraints(channel)
        assert len(result) > 50, f"Channel {channel} returned unexpectedly short constraints"
