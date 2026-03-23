from app.models.enums import Channel, Intent
from app.prompts.assembler import assemble_system_prompt


def test_chemical_query_includes_poison_centre(kzn_smallholder, sample_knowledge_chunks):
    """Pest management prompt must include the Poison Information Centre number."""
    prompt = assemble_system_prompt(
        farmer=kzn_smallholder,
        channel=Channel.WHATSAPP,
        intent=Intent.PEST_MANAGEMENT,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "0861 555 777" in prompt


def test_livestock_emergency_includes_vet_phone(ec_emerging, sample_knowledge_chunks):
    """Livestock health prompt must include the farmer's state vet phone."""
    prompt = assemble_system_prompt(
        farmer=ec_emerging,
        channel=Channel.WHATSAPP,
        intent=Intent.LIVESTOCK_HEALTH,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "043 707 5800" in prompt


def test_notifiable_disease_rule_present(kzn_smallholder, sample_knowledge_chunks):
    """Rule 2 about notifiable diseases must be in every livestock health prompt."""
    prompt = assemble_system_prompt(
        farmer=kzn_smallholder,
        channel=Channel.WHATSAPP,
        intent=Intent.LIVESTOCK_HEALTH,
        knowledge_chunks=sample_knowledge_chunks,
    )
    assert "notifiable disease" in prompt
    assert "Isolate affected animals" in prompt
    assert "033 845 9801" in prompt  # Sipho's state vet phone
