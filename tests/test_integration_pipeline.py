"""Integration tests for end-to-end pipeline behavior."""

from paper2code.extraction import CompositeExtractionProvider
from paper2code.extraction import ExtractionAgent
from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.models import WorkflowUncertainty
from paper2code.pipeline import PaperToCodePipeline
from paper2code.planning import PlanningAgent
from paper2code.reduction import ReductionStrategy
from paper2code.reporting import TraceabilityInput


class IntegrationPlanningProvider:
    """Planning provider tailored for end-to-end integration coverage."""

    def plan(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Return one reproducible workflow step for extracted artifacts."""
        if not artifacts:
            return []
        return [
            WorkflowStep(
                step_id="step-1",
                description="Execute publication baseline analysis.",
                tools=("python", "docker"),
                expected_outputs=("rationale",),
                uncertainty_level=WorkflowUncertainty.LOW,
                confidence_score=0.95,
                uncertainty_note=None,
            )
        ]

    def plan_with_outputs(
        self,
        artifacts: list[PaperArtifact],
    ) -> tuple[list[WorkflowStep], list[IntermediateOutput]]:
        """Return both workflow steps and intermediate rationale output."""
        steps = self.plan(artifacts)
        if not steps:
            return [], []
        return steps, [
            IntermediateOutput(
                output_id="step-1-rationale",
                step_id="step-1",
                name="rationale",
                location="Evidence supports baseline execution.",
            )
        ]


def test_pipeline_run_with_agreement_end_to_end() -> None:
    """End-to-end run should return an agreement report with passing checks."""
    extraction_agent = ExtractionAgent(provider=CompositeExtractionProvider())
    planning_agent = PlanningAgent(provider=IntegrationPlanningProvider())
    reduction_strategy = ReductionStrategy()
    pipeline = PaperToCodePipeline(
        extraction_agent=extraction_agent,
        planning_agent=planning_agent,
        reduction_strategy=reduction_strategy,
    )

    text = "Methods\nWe used control and treatment cohorts.\nResults\nFigure 1"
    trace_rows = [
        TraceabilityInput(
            claim_id="claim-1",
            claim_text="Treatment improves metric.",
            evidence_text="Observed increase in Results section.",
            step_id="step-1",
        )
    ]
    result = pipeline.run_with_agreement(
        document_text=text,
        run_id="run-integration",
        paper_id="paper-integration",
        expected_value=0.80,
        observed_value=0.81,
        tolerance=0.02,
        traceability_rows=trace_rows,
    )

    assert len(result.artifacts) >= 1
    assert len(result.workflow_steps) == 1
    assert len(result.intermediate_outputs) == 1
    assert result.agreement_report is not None
    assert result.agreement_report.summary == "3/3 checks passed"
    assert result.agreement_report.traceability_map["claim-1"] == ("step-1",)
