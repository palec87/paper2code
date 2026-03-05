"""Deterministic mock providers used in tests and local development."""

from paper2code.interfaces import ExplanationLLM
from paper2code.interfaces import ExtractionLLM
from paper2code.interfaces import PlanningLLM
from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.models import WorkflowUncertainty


class MockExtractionProvider(ExtractionLLM):
    """Simple deterministic extraction provider for repeatable tests."""

    def extract(self, document_text: str) -> list[PaperArtifact]:
        """Produce one text artifact from raw publication input."""
        return [
            PaperArtifact(
                artifact_id="artifact-1",
                artifact_type="text",
                source_path="full_text",
                content=document_text,
                confidence=1.0,
            )
        ]


class MockPlanningProvider(PlanningLLM):
    """Simple deterministic planning provider for repeatable tests."""

    def plan(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Plan one workflow step when artifacts are present."""
        if not artifacts:
            return []
        return [
            WorkflowStep(
                step_id="step-1",
                description="Run baseline reproducible analysis.",
                tools=("python", "docker"),
                expected_outputs=("metrics.json", "report.md"),
                uncertainty_level=WorkflowUncertainty.LOW,
                confidence_score=0.9,
            )
        ]

    def plan_with_outputs(
        self,
        artifacts: list[PaperArtifact],
    ) -> tuple[list[WorkflowStep], list[IntermediateOutput]]:
        """Plan workflow steps and return reasoning outputs."""
        steps = self.plan(artifacts)
        outputs = [
            IntermediateOutput(
                output_id="step-1-rationale",
                step_id="step-1",
                name="rationale",
                location="Selected baseline reproducible analysis.",
            )
        ]
        if not steps:
            return [], []
        return steps, outputs


class MockExplanationProvider(ExplanationLLM):
    """Deterministic explanation provider for traceability checks."""

    def explain(self, claim: str, evidence: str) -> str:
        """Build a stable explanation sentence."""
        return f"Claim: {claim} | Evidence: {evidence}"
