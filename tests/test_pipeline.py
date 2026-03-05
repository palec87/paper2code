"""Tests for phase-1 paper-to-code pipeline orchestration."""

from paper2code.extraction import ExtractionAgent
from paper2code.pipeline import PaperToCodePipeline
from paper2code.planning import PlanningAgent
from paper2code.providers import MockExtractionProvider
from paper2code.providers import MockPlanningProvider
from paper2code.reduction import ReductionStrategy


def test_pipeline_run_produces_artifacts_and_steps() -> None:
    """Pipeline should return extraction and planning outputs."""
    extraction_agent = ExtractionAgent(provider=MockExtractionProvider())
    planning_agent = PlanningAgent(provider=MockPlanningProvider())
    reduction_strategy = ReductionStrategy()
    pipeline = PaperToCodePipeline(
        extraction_agent=extraction_agent,
        planning_agent=planning_agent,
        reduction_strategy=reduction_strategy,
    )

    result = pipeline.run("Methods section text")

    assert len(result.artifacts) == 1
    assert len(result.reduced_artifacts) == 1
    assert len(result.workflow_steps) == 1
    assert result.workflow_steps[0].step_id == "step-1"
