from app.models.enums import Channel, Intent
from app.models.messages import FarmerProfile, KnowledgeChunk
from app.prompts.assembler import assemble_system_prompt


def test_safety_rules_before_knowledge(kzn_smallholder, sample_knowledge_chunks):
    """Safety rules must appear before knowledge context in the assembled prompt."""
    prompt = assemble_system_prompt(
        farmer=kzn_smallholder,
        channel=Channel.WHATSAPP,
        intent=Intent.CROP_DISEASE_ID,
        knowledge_chunks=sample_knowledge_chunks,
    )
    safety_pos = prompt.index("SAFETY RULES")
    knowledge_pos = prompt.index("KNOWLEDGE CONTEXT")
    assert safety_pos < knowledge_pos


def test_all_safety_rules_present(kzn_smallholder, sample_knowledge_chunks):
    """All 7 safety rules must be present in every assembled prompt."""
    prompt = assemble_system_prompt(
        farmer=kzn_smallholder,
        channel=Channel.WHATSAPP,
        intent=Intent.GENERAL_AGRI,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "Poison Information Centre 0861 555 777" in prompt
    assert "notifiable disease" in prompt
    assert "Confidence:" in prompt
    assert "CHEMICAL SAFETY" in prompt
    assert "VETERINARY BOUNDARIES" in prompt
    assert "NO FINANCIAL GUARANTEES" in prompt
    assert "CULTURAL SENSITIVITY" in prompt
    assert "DATA BOUNDARIES" in prompt


def test_terminology_injected_for_isizulu(kzn_smallholder, sample_knowledge_chunks):
    """isiZulu farmer should see the terminology reference section."""
    prompt = assemble_system_prompt(
        farmer=kzn_smallholder,
        channel=Channel.WHATSAPP,
        intent=Intent.GENERAL_AGRI,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "AGRICULTURAL TERMINOLOGY REFERENCE" in prompt
    assert "Umbila" in prompt  # Maize in isiZulu
    assert "Isifo" in prompt  # Disease in isiZulu
    assert "Ukunisela" in prompt  # Irrigation in isiZulu


def test_terminology_not_injected_for_english(english_farmer, sample_knowledge_chunks):
    """English farmer should NOT see the terminology reference section."""
    prompt = assemble_system_prompt(
        farmer=english_farmer,
        channel=Channel.WHATSAPP,
        intent=Intent.GENERAL_AGRI,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "AGRICULTURAL TERMINOLOGY REFERENCE" not in prompt


def test_channel_constraints_match(kzn_smallholder, sample_knowledge_chunks):
    """Each channel should inject its specific constraint text."""
    for channel, expected_text in [
        (Channel.USSD, "Maximum 160 characters"),
        (Channel.WHATSAPP, "Maximum 4096 characters"),
        (Channel.IVR, "natural spoken language"),
        (Channel.WEB, "Rich markdown supported"),
        (Channel.SMS, "outbound push alerts"),
    ]:
        prompt = assemble_system_prompt(
            farmer=kzn_smallholder,
            channel=channel,
            intent=Intent.GENERAL_AGRI,
            knowledge_chunks=sample_knowledge_chunks,
        )
        assert expected_text in prompt, f"Missing constraint for {channel}"


def test_farmer_profile_injected(kzn_smallholder, sample_knowledge_chunks):
    """Farmer profile fields must appear in the assembled prompt."""
    prompt = assemble_system_prompt(
        farmer=kzn_smallholder,
        channel=Channel.WHATSAPP,
        intent=Intent.GENERAL_AGRI,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "Sipho" in prompt
    assert "KwaZulu-Natal" in prompt
    assert "maize" in prompt
    assert "4.5 hectares" in prompt
