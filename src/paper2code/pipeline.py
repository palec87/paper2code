"""High-level orchestration primitives for the MVP pipeline."""

from dataclasses import dataclass

from paper2code.extraction import ExtractionAgent
from paper2code.logging import get_logger
from paper2code.models import AgreementReport
from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.planning import PlanningAgent
from paper2code.reduction import ReductionStrategy
from paper2code.reporting import AgreementReportGenerator
from paper2code.reporting import TraceabilityInput


logger = get_logger(__name__)


@dataclass(slots=True)
class PipelineResult:
    """Container for outputs produced by one pipeline execution."""

    artifacts: list[PaperArtifact]
    reduced_artifacts: list[PaperArtifact]
    workflow_steps: list[WorkflowStep]
    intermediate_outputs: list[IntermediateOutput]
    agreement_report: AgreementReport | None = None


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
        logger.info("Pipeline run started")
        artifacts = self._extraction_agent.run(document_text)
        logger.debug("Pipeline extracted %d artifacts", len(artifacts))
        reduced = self._reduction_strategy.reduce_to_examples(
            artifacts,
            max_items=max_examples,
        )
        logger.debug("Pipeline reduced to %d artifacts", len(reduced))
        steps, outputs = self._planning_agent.run_with_outputs(reduced)
        logger.info(
            "Pipeline run completed with %d steps and %d outputs",
            len(steps),
            len(outputs),
        )
        return PipelineResult(
            artifacts=artifacts,
            reduced_artifacts=reduced,
            workflow_steps=steps,
            intermediate_outputs=outputs,
        )

    def run_with_agreement(
        self,
        document_text: str,
        run_id: str,
        paper_id: str,
        expected_value: float,
        observed_value: float,
        tolerance: float,
        traceability_rows: list[TraceabilityInput],
        max_examples: int = 20,
    ) -> PipelineResult:
        """Run pipeline and attach an agreement report."""
        logger.info("Pipeline agreement run started for paper_id=%s", paper_id)
        result = self.run(
            document_text=document_text,
            max_examples=max_examples,
        )
        reporter = AgreementReportGenerator()
        checks = [
            reporter.numerical_tolerance_check(
                check_id="numeric-1",
                metric_name="primary_metric",
                expected=expected_value,
                observed=observed_value,
                tolerance=tolerance,
            ),
            reporter.workflow_completeness_check(
                check_id="workflow-1",
                steps=result.workflow_steps,
                outputs=result.intermediate_outputs,
            ),
        ]
        trace_checks, mapping = reporter.traceability_checks(traceability_rows)
        checks.extend(trace_checks)
        report = reporter.generate_report(
            run_id=run_id,
            paper_id=paper_id,
            checks=checks,
            traceability_map=mapping,
        )
        result.agreement_report = report
        logger.info("Agreement report generated: %s", report.summary)
        return result
