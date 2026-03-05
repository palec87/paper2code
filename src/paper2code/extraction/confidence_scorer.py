"""Confidence scoring helpers for extracted artifacts."""

from paper2code.logging import get_logger
from paper2code.models import PaperArtifact


logger = get_logger(__name__)


class ConfidenceScorer:
    """Adjust confidence by artifact quality heuristics."""

    def score(self, artifact: PaperArtifact) -> PaperArtifact:
        """Return an updated artifact with heuristic confidence applied."""
        score = artifact.confidence
        if len(artifact.content) < 40:
            score = max(0.1, score - 0.2)
        if artifact.artifact_type in {"table", "figure"}:
            score = max(0.2, score - 0.1)
        if artifact.extraction_method == "missing_dependency":
            score = 0.0
        logger.debug(
            "Scored artifact %s (%s): %.3f -> %.3f",
            artifact.artifact_id,
            artifact.artifact_type,
            artifact.confidence,
            score,
        )
        return PaperArtifact(
            artifact_id=artifact.artifact_id,
            artifact_type=artifact.artifact_type,
            source_path=artifact.source_path,
            content=artifact.content,
            confidence=round(score, 3),
            source_format=artifact.source_format,
            extraction_method=artifact.extraction_method,
        )
