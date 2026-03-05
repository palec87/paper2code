"""Agreement report generation utilities."""

from dataclasses import dataclass
from uuid import uuid4

from paper2code.models import AgreementCheck
from paper2code.models import AgreementReport
from paper2code.models import IntermediateOutput
from paper2code.models import WorkflowStep


@dataclass(slots=True)
class TraceabilityInput:
    """Input row for claim-to-step traceability checks."""

    claim_id: str
    claim_text: str
    evidence_text: str
    step_id: str


class AgreementReportGenerator:
    """Generates agreement checks and wraps them in a report."""

    def numerical_tolerance_check(
        self,
        check_id: str,
        metric_name: str,
        expected: float,
        observed: float,
        tolerance: float,
    ) -> AgreementCheck:
        """Check whether observed value is within tolerance."""
        difference = abs(expected - observed)
        passed = difference <= tolerance
        details = f"difference={difference:.6g}; tolerance={tolerance:.6g}"
        return AgreementCheck(
            check_id=check_id,
            metric_name=metric_name,
            expected=str(expected),
            observed=str(observed),
            passed=passed,
            details=details,
        )

    def workflow_completeness_check(
        self,
        check_id: str,
        steps: list[WorkflowStep],
        outputs: list[IntermediateOutput],
    ) -> AgreementCheck:
        """Check if expected step outputs are present among outputs."""
        expected_names: list[str] = []
        for step in steps:
            expected_names.extend(step.expected_outputs)
        observed_names = {output.name for output in outputs}
        found = sum(1 for name in expected_names if name in observed_names)
        total = len(expected_names)
        passed = found == total
        details = f"found={found}/{total} expected outputs"
        return AgreementCheck(
            check_id=check_id,
            metric_name="workflow_completeness",
            expected=str(total),
            observed=str(found),
            passed=passed,
            details=details,
        )

    def traceability_checks(
        self,
        rows: list[TraceabilityInput],
    ) -> tuple[list[AgreementCheck], dict[str, tuple[str, ...]]]:
        """Create claim traceability checks and map claim to step ids."""
        checks: list[AgreementCheck] = []
        traceability_map: dict[str, tuple[str, ...]] = {}
        for index, row in enumerate(rows, start=1):
            evidence = row.evidence_text.strip()
            passed = bool(evidence)
            details = "evidence linked" if passed else "missing evidence"
            checks.append(
                AgreementCheck(
                    check_id=f"traceability-{index}",
                    metric_name="claim_traceability",
                    expected="non-empty evidence",
                    observed=evidence or "",
                    passed=passed,
                    details=details,
                )
            )
            traceability_map[row.claim_id] = (row.step_id,)
        return checks, traceability_map

    def generate_report(
        self,
        run_id: str,
        paper_id: str,
        checks: list[AgreementCheck],
        traceability_map: dict[str, tuple[str, ...]],
    ) -> AgreementReport:
        """Aggregate checks into an immutable agreement report."""
        passed_count = sum(1 for check in checks if check.passed)
        summary = f"{passed_count}/{len(checks)} checks passed"
        return AgreementReport(
            report_id=str(uuid4()),
            run_id=run_id,
            paper_id=paper_id,
            checks=tuple(checks),
            summary=summary,
            traceability_map=traceability_map,
        )
