"""Validation helpers for publication agreement checks."""

from paper2code.models import AgreementCheck


class AgreementValidator:
    """Creates basic agreement checks for deterministic validation."""

    def numerical_tolerance_check(
        self,
        check_id: str,
        metric_name: str,
        expected: float,
        observed: float,
        tolerance: float,
    ) -> AgreementCheck:
        """Validate numeric agreement under a tolerance bound."""
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
