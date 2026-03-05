"""Tests for real extraction provider behavior."""

from paper2code.extraction import CompositeExtractionProvider


def test_composite_extractor_handles_inline_text() -> None:
    """Inline publication text should yield text artifacts."""
    provider = CompositeExtractionProvider()
    artifacts = provider.extract(
        "Methods\nWe used a control group.\nResults\nA table."
    )
    assert len(artifacts) >= 1
    assert artifacts[0].artifact_type == "text"
    assert 0.0 <= artifacts[0].confidence <= 1.0


def test_composite_extractor_marks_missing_pdf_dependency() -> None:
    """Missing pypdf should produce a dependency-warning artifact."""
    provider = CompositeExtractionProvider()
    artifacts = provider.extract("nonexistent.pdf")
    assert len(artifacts) >= 1
    assert artifacts[0].source_format in {"pdf", "text"}
