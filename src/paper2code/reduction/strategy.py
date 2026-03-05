"""Simple reduction strategy for Phase 1 scaffolding."""

from paper2code.models import PaperArtifact


class ReductionStrategy:
    """Reduces extracted artifacts into an MVP-sized subset."""

    def reduce_to_examples(
        self,
        artifacts: list[PaperArtifact],
        max_items: int = 20,
    ) -> list[PaperArtifact]:
        """Keep up to ``max_items`` artifacts as representative examples."""
        return artifacts[:max_items]
