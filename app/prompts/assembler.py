from app.models.enums import Channel, Intent, Language
from app.models.messages import FarmerProfile, KnowledgeChunk, VisionResult
from app.prompts.identity import IDENTITY_PROMPT
from app.prompts.safety import render_safety_rules
from app.prompts.channels import get_channel_constraints
from app.prompts.intents import get_intent_instructions
from app.prompts.terminology import get_terminology_prompt
from app.prompts.few_shot_examples import get_few_shot_examples


def assemble_system_prompt(
    farmer: FarmerProfile,
    channel: Channel,
    intent: Intent,
    knowledge_chunks: list[KnowledgeChunk],
    vision_results: VisionResult | None = None,
    price_data: str | None = None,
    weather_data: str | None = None,
    financial_context: str | None = None,
) -> str:
    """
    Assemble the complete system prompt from all six modular segments.

    Assembly order is critical — identity and safety rules first to ensure
    they receive maximum attention weight in Claude's context window.
    """
    segments: list[str] = []

    # 1. Identity (who Limi is)
    segments.append(IDENTITY_PROMPT)

    # 2. Safety rules (non-negotiable, highest priority after identity)
    segments.append(render_safety_rules(
        nearest_dard_office=farmer.nearest_dard_office,
        state_vet_phone=farmer.state_vet_phone,
    ))

    # 3. Knowledge context (RAG-retrieved chunks)
    if knowledge_chunks:
        knowledge_lines = [
            "KNOWLEDGE CONTEXT (use ONLY this information for factual claims):",
            "",
        ]
        for index, chunk in enumerate(knowledge_chunks, start=1):
            knowledge_lines.append(
                f"SOURCE {index}: {chunk.source_title} ({chunk.source_type})"
            )
            knowledge_lines.append("---")
            knowledge_lines.append(chunk.chunk_text)
            knowledge_lines.append("---")
            knowledge_lines.append("")

        knowledge_lines.append(
            'CITATION RULE: When using information from a source, cite naturally: '
            '"According to DARD guidelines..." or "ARC research shows..." '
            "If the answer is NOT in these sources, say so honestly."
        )
        segments.append("\n".join(knowledge_lines))

    # 3b. Financial context (if available for financial intents)
    if financial_context:
        segments.append(f"""FINANCIAL CONTEXT (available products for this farmer):
{financial_context}
ELIGIBILITY NOTE: Present these as options, not recommendations. Apply Safety Rule 8 (Financial Disclosure) strictly.""")

    # 4. Farmer profile (personalisation)
    segments.append(_format_farmer_profile(farmer))

    # 5. Terminology reference (isiZulu / isiXhosa only)
    terminology = get_terminology_prompt(farmer.language)
    if terminology:
        segments.append(terminology)

    # 6. Channel constraints (formatting rules)
    segments.append(get_channel_constraints(channel))

    # 7. Intent-specific instructions
    segments.append(get_intent_instructions(
        intent=intent,
        vision_results=vision_results,
        price_data=price_data,
        weather_data=weather_data,
    ))

    # 8. Few-shot examples (tone and format calibration)
    examples = get_few_shot_examples(intent, farmer.language, channel)
    if examples:
        segments.append(
            f"EXAMPLE (for tone and format reference only — do not copy verbatim):\n{examples}"
        )

    return "\n\n".join(segments)


def _format_farmer_profile(farmer: FarmerProfile) -> str:
    """Format the farmer profile block for injection into the system prompt."""
    crops_list = ", ".join(farmer.crops) if farmer.crops else "none specified"
    livestock_list = ", ".join(farmer.livestock) if farmer.livestock else "none"

    return f"""FARMER PROFILE:
Name: {farmer.display_name}
Language: {farmer.language} (respond in this language)
Province: {farmer.province}
District: {farmer.district}
Farm type: {farmer.farm_type}
Crops: {crops_list}
Livestock: {livestock_list}
Farm size: {farmer.farm_size_ha} hectares
Subscription: {farmer.tier}
Nearest DARD office: {farmer.nearest_dard_office} ({farmer.nearest_dard_phone})
State veterinarian: {farmer.state_vet_phone}

PERSONALISATION RULES:
- Address the farmer by name in the first response of a session.
- Tailor advice to their specific crops and province.
- For smallholders (<10 ha): focus on low-cost, accessible solutions. Don't recommend expensive commercial inputs unless asked.
- For commercial farmers: you may discuss technical specifics, cultivar selection, precision application rates.
- For emerging farmers (10-100 ha): bridge between the two. Explain technical terms when first used."""
