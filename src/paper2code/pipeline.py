"""High-level orchestration primitives for the MVP pipeline."""

from dataclasses import dataclass

from paper2code.extraction import ExtractionAgent
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.planning import PlanningAgent
from paper2code.reduction import ReductionStrategy


@dataclass(slots=True)
class PipelineResult:
    """Container for outputs produced by one pipeline execution."""

    artifacts: list[PaperArtifact]
    reduced_artifacts: list[PaperArtifact]
    workflow_steps: list[WorkflowStep]


class PaperToCodePipeline:
    """Executes extraction, reduction, and planning for one publication."""

    def __init__(
        self,
        extraction_agent: ExtractionAgent,
        planning_agent: PlanningAgent,
        reduction_strategy: ReductionStrategy,
    ) -> None:
        """Initialize pipeline dependencies."""
        self._extraction_agent = extraction_agent
        self._planning_agent = planning_agent
        self._reduction_strategy = reduction_strategy

    def run(
        self,
        document_text: str,
        max_examples: int = 20,
    ) -> PipelineResult:
        """Run the phase-1 workflow from text to planned steps."""
        artifacts = self._extraction_agent.run(document_text)
        reduced = self._reduction_strategy.reduce_to_examples(
            artifacts,
            max_items=max_examples,
        )
        steps = self._planning_agent.run(reduced)
        return PipelineResult(
            artifacts=artifacts,
            reduced_artifacts=reduced,
            workflow_steps=steps,
        )
