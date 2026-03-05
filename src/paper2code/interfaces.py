"""Provider-agnostic interfaces for LLM-backed operations."""

from typing import Protocol

from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep


class ExtractionLLM(Protocol):
    """Interface for extracting structured publication artifacts."""

    def extract(self, document_text: str) -> list[PaperArtifact]:
        """Extract structured artifacts from a publication text."""


class PlanningLLM(Protocol):
    """Interface for turning artifacts into executable workflow steps."""

    def plan(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Plan workflow steps from extracted artifacts."""

    def plan_with_outputs(
        self,
        artifacts: list[PaperArtifact],
    ) -> tuple[list[WorkflowStep], list[IntermediateOutput]]:
        """Plan workflow steps and expose intermediate outputs."""


class ExplanationLLM(Protocol):
    """Interface for generating traceability explanations."""

    def explain(self, claim: str, evidence: str) -> str:
        """Generate an explanation that links claim to evidence."""
