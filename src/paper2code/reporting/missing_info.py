"""Missing-information reporting primitives."""

from paper2code.models import MissingInfoItem


class MissingInfoReporter:
    """Builds report entries for missing or ambiguous publication details."""

    def report_item(
        self,
        item_id: str,
        category: str,
        severity: str,
        description: str,
        suggested_action: str,
    ) -> MissingInfoItem:
        """Create a single missing-information report item."""
        return MissingInfoItem(
            item_id=item_id,
            category=category,
            severity=severity,
            description=description,
            suggested_action=suggested_action,
        )
