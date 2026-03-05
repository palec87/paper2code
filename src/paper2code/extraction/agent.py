"""Extraction agent implementation."""

from paper2code.interfaces import ExtractionLLM
from paper2code.models import PaperArtifact


class ExtractionAgent:
    """Extracts publication artifacts with an injected provider."""

    def __init__(self, provider: ExtractionLLM) -> None:
        """Initialize the extraction agent with a provider."""
        self._provider = provider

    def run(self, document_text: str) -> list[PaperArtifact]:
        """Run artifact extraction for publication text."""
        return self._provider.extract(document_text)
