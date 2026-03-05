"""In-memory phase-1 tool registry placeholder."""

from paper2code.models import ToolRecord


class ToolRegistry:
    """Stores reusable tools; PostgreSQL backend comes in a later phase."""

    def __init__(self) -> None:
        """Initialize an in-memory list for tool records."""
        self._records: list[ToolRecord] = []

    def add_tool(self, record: ToolRecord) -> None:
        """Add one tool to the registry."""
        self._records.append(record)

    def list_tools(self) -> list[ToolRecord]:
        """Return all known tool records."""
        return list(self._records)
