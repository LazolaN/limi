from app.models.enums import ConfidenceLevel, Intent, RiskLevel
from app.models.messages import KnowledgeChunk
from app.services.confidence_scorer import score_confidence, should_escalate


def _make_chunks(count: int) -> list[KnowledgeChunk]:
    return [
        KnowledgeChunk(
            source_title=f"Source {i}",
            source_type="DARD",
            chunk_text=f"Content {i}",
            relevance_score=0.9,
        )
        for i in range(count)
    ]


def test_extract_high_confidence():
    result = score_confidence(
        "Here is my advice. Confidence: HIGH",
        Intent.GENERAL_AGRI,
        _make_chunks(2),
    )
    assert result == ConfidenceLevel.HIGH


def test_extract_medium_confidence():
    result = score_confidence(
        "Based on limited info. Confidence: MEDIUM",
        Intent.GENERAL_AGRI,
        _make_chunks(2),
    )
    assert result == ConfidenceLevel.MEDIUM


def test_extract_low_confidence():
    result = score_confidence(
        "I'm uncertain. Confidence: LOW",
        Intent.GENERAL_AGRI,
        _make_chunks(2),
    )
    assert result == ConfidenceLevel.LOW


def test_uncertainty_phrase_forces_low():
    result = score_confidence(
        "Confidence: HIGH but I'm not sure about this treatment.",
        Intent.GENERAL_AGRI,
        _make_chunks(2),
    )
    assert result == ConfidenceLevel.LOW


def test_livestock_no_knowledge_forces_low():
    result = score_confidence(
        "Confidence: HIGH. The animal likely has...",
        Intent.LIVESTOCK_HEALTH,
        [],  # No knowledge chunks
    )
    assert result == ConfidenceLevel.LOW


def test_disease_no_knowledge_forces_low():
    result = score_confidence(
        "Confidence: MEDIUM. This looks like...",
        Intent.CROP_DISEASE_ID,
        [],
    )
    assert result == ConfidenceLevel.LOW


def test_should_escalate_low_any():
    assert should_escalate(ConfidenceLevel.LOW, RiskLevel.LOW) is True
    assert should_escalate(ConfidenceLevel.LOW, RiskLevel.HIGH) is True


def test_should_escalate_medium_high():
    assert should_escalate(ConfidenceLevel.MEDIUM, RiskLevel.HIGH) is True


def test_should_not_escalate_medium_low():
    assert should_escalate(ConfidenceLevel.MEDIUM, RiskLevel.LOW) is False


def test_should_not_escalate_high_high():
    assert should_escalate(ConfidenceLevel.HIGH, RiskLevel.HIGH) is False


def test_isizulu_confidence_labels():
    result = score_confidence(
        "Ukuqiniseka: KUPHEZULU. Fafaza nge-fungicide.",
        Intent.CROP_DISEASE_ID,
        _make_chunks(1),
    )
    assert result == ConfidenceLevel.HIGH
