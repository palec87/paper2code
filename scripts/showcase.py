"""Showcase script for paper2code end-to-end MVP pipeline."""

from paper2code.extraction import CompositeExtractionProvider
from paper2code.extraction import ExtractionAgent
from paper2code.logging import Logger
from paper2code.logging import get_logger
from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.models import WorkflowUncertainty
from paper2code.pipeline import PaperToCodePipeline
from paper2code.planning import PlanningAgent
from paper2code.reduction import ReductionStrategy
from paper2code.reporting import TraceabilityInput


Logger.configure(level="INFO")
logger = get_logger(__name__)


class DemoPlanningProvider:
    """Simple planner used by the showcase script."""

    def plan(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Generate one step from extracted artifacts."""
        if not artifacts:
            return []
        return [
            WorkflowStep(
                step_id="step-1",
                description="Run reproducible analysis workflow.",
                tools=("python", "docker"),
                expected_outputs=("rationale",),
                uncertainty_level=WorkflowUncertainty.MEDIUM,
                confidence_score=0.88,
                uncertainty_note="Figure parsing is heuristic.",
            )
        ]

    def plan_with_outputs(
        self,
        artifacts: list[PaperArtifact],
    ) -> tuple[list[WorkflowStep], list[IntermediateOutput]]:
        """Generate one rationale output for the showcase."""
        steps = self.plan(artifacts)
        if not steps:
            return [], []
        return steps, [
            IntermediateOutput(
                output_id="step-1-rationale",
                step_id="step-1",
                name="rationale",
                location=(
                    "Selected reproducible baseline "
                    "from extracted methods."
                ),
            )
        ]


def main() -> None:
    """Run a short end-to-end demonstration on inline paper text."""
    logger.info("Starting showcase script")
    extraction_agent = ExtractionAgent(provider=CompositeExtractionProvider())
    planning_agent = PlanningAgent(provider=DemoPlanningProvider())
    reduction_strategy = ReductionStrategy()
    pipeline = PaperToCodePipeline(
        extraction_agent=extraction_agent,
        planning_agent=planning_agent,
        reduction_strategy=reduction_strategy,
    )

    sample_text = (
        "Methods\n"
        "We compared a baseline model against a treatment model.\n"
        "Results\n"
        "Figure 1 shows improved performance of the treatment group."
    )
    traceability_rows = [
        TraceabilityInput(
            claim_id="claim-1",
            claim_text="Treatment outperforms baseline.",
            evidence_text="Figure 1 indicates higher performance.",
            step_id="step-1",
        )
    ]

    result = pipeline.run_with_agreement(
        document_text=sample_text,
        run_id="showcase-run",
        paper_id="showcase-paper",
        expected_value=0.75,
        observed_value=0.76,
        tolerance=0.02,
        traceability_rows=traceability_rows,
    )

    logger.info("Showcase pipeline run complete")
    print("paper2code showcase")
    print(f"artifacts: {len(result.artifacts)}")
    print(f"workflow steps: {len(result.workflow_steps)}")
    print(f"intermediate outputs: {len(result.intermediate_outputs)}")
    if result.agreement_report is not None:
        logger.info("Agreement summary: %s", result.agreement_report.summary)
        print(f"agreement: {result.agreement_report.summary}")
        print("traceability:")
        for claim_id, step_ids in (
            result.agreement_report.traceability_map.items()
        ):
            joined_steps = ", ".join(step_ids)
            print(f"  {claim_id} -> {joined_steps}")
    logger.info("Showcase script finished")


if __name__ == "__main__":
    main()
