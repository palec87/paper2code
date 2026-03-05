"""Extraction agent implementation."""

from paper2code.interfaces import ExtractionLLM
from paper2code.logging import get_logger
from paper2code.models import PaperArtifact


logger = get_logger(__name__)


class ExtractionAgent:
    """Extracts publication artifacts with an injected provider."""

    def __init__(self, provider: ExtractionLLM) -> None:
        """Initialize the extraction agent with a provider."""
        self._provider = provider

    def run(self, document_text: str) -> list[PaperArtifact]:
        """Run extraction for text blobs or file-path based inputs."""
        logger.info("Extraction agent started")
        artifacts = self._provider.extract(document_text)
        logger.info("Extraction agent produced %d artifacts", len(artifacts))
        return artifacts
