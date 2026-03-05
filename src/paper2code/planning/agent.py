"""Planning agent implementation."""

from paper2code.interfaces import PlanningLLM
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep


class PlanningAgent:
    """Builds executable workflow steps from extracted artifacts."""

    def __init__(self, provider: PlanningLLM) -> None:
        """Initialize the planning agent with a provider."""
        self._provider = provider

    def run(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Run workflow planning using extracted artifacts."""
        return self._provider.plan(artifacts)
