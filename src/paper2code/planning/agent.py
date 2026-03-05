"""Planning agent implementation."""

from paper2code.interfaces import PlanningLLM
from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.planning.output_tracker import IntermediateOutputTracker


class PlanningAgent:
    """Builds executable workflow steps from extracted artifacts."""

    def __init__(
        self,
        provider: PlanningLLM,
        output_tracker: IntermediateOutputTracker | None = None,
    ) -> None:
        """Initialize the planning agent with a provider."""
        self._provider = provider
        self._tracker = output_tracker or IntermediateOutputTracker()

    def run(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Run workflow planning using extracted artifacts."""
        return self._provider.plan(artifacts)

    def run_with_outputs(
        self,
        artifacts: list[PaperArtifact],
    ) -> tuple[list[WorkflowStep], list[IntermediateOutput]]:
        """Run planning and emit intermediate explanation outputs."""
        steps, outputs = self._provider.plan_with_outputs(artifacts)
        persisted: list[IntermediateOutput] = []
        for output in outputs:
            persisted.append(
                self._tracker.emit_output(
                    step_id=output.step_id,
                    name=output.name,
                    content=output.location,
                )
            )
        return steps, persisted
