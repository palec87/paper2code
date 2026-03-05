"""Composite extraction provider for text and PDF publications."""

from pathlib import Path

from paper2code.extraction.confidence_scorer import ConfidenceScorer
from paper2code.extraction.pdf_extractor import PDFExtractor
from paper2code.extraction.text_extractor import TextSectionExtractor
from paper2code.interfaces import ExtractionLLM
from paper2code.models import PaperArtifact


class CompositeExtractionProvider(ExtractionLLM):
    """Extract artifacts from either raw text payloads or filesystem paths."""

    def __init__(self) -> None:
        """Initialize extraction components."""
        self._pdf = PDFExtractor()
        self._text = TextSectionExtractor()
        self._scorer = ConfidenceScorer()

    def extract(self, document_text: str) -> list[PaperArtifact]:
        """Extract text, table, and figure artifacts from publication input."""
        path = Path(document_text)
        artifacts: list[PaperArtifact]
        if path.exists() and path.suffix.lower() == ".pdf":
            artifacts = self._pdf.extract(str(path))
        elif path.exists():
            text = path.read_text(encoding="utf-8")
            artifacts = self._text.extract(text, str(path))
        else:
            artifacts = self._text.extract(document_text, "inline_input")

        return [self._scorer.score(item) for item in artifacts]
