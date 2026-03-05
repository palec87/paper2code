"""Tests for agreement report generation."""

from paper2code.models import IntermediateOutput
from paper2code.models import WorkflowStep
from paper2code.reporting import AgreementReportGenerator
from paper2code.reporting import TraceabilityInput


def test_agreement_report_generator_builds_summary() -> None:
    """Agreement report should include check summary and traceability map."""
    generator = AgreementReportGenerator()
    numeric = generator.numerical_tolerance_check(
        check_id="n1",
        metric_name="acc",
        expected=0.9,
        observed=0.91,
        tolerance=0.02,
    )
    step = WorkflowStep(
        step_id="step-1",
        description="Run analysis",
        tools=("python",),
        expected_outputs=("rationale",),
    )
    output = IntermediateOutput(
        output_id="o1",
        step_id="step-1",
        name="rationale",
        location="path",
    )
    complete = generator.workflow_completeness_check(
        check_id="c1",
        steps=[step],
        outputs=[output],
    )
    trace_checks, mapping = generator.traceability_checks(
        [
            TraceabilityInput(
                claim_id="claim-1",
                claim_text="X improves Y",
                evidence_text="Observed 0.91 accuracy",
                step_id="step-1",
            )
        ]
    )
    checks = [numeric, complete, *trace_checks]
    report = generator.generate_report(
        run_id="run-1",
        paper_id="paper-1",
        checks=checks,
        traceability_map=mapping,
    )
    assert report.summary == "3/3 checks passed"
    assert report.traceability_map["claim-1"] == ("step-1",)
