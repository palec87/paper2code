"""Tests for planning outputs and uncertainty propagation."""

from paper2code.models import PaperArtifact
from paper2code.planning import PlanningAgent
from paper2code.providers import MockPlanningProvider


def test_planning_agent_run_with_outputs_returns_outputs() -> None:
    """Planning should emit intermediate outputs for each run."""
    agent = PlanningAgent(provider=MockPlanningProvider())
    artifacts = [
        PaperArtifact(
            artifact_id="a1",
            artifact_type="text",
            source_path="inline",
            content="Method details",
        )
    ]
    steps, outputs = agent.run_with_outputs(artifacts)
    assert len(steps) == 1
    assert len(outputs) == 1
    assert steps[0].uncertainty_level.value == "low"
