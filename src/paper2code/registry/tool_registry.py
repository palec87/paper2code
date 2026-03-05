"""In-memory phase-1 tool registry placeholder."""

from typing import Protocol

from paper2code.models import ToolRecord


class ToolRegistryProtocol(Protocol):
    """Common protocol used by all registry backends."""

    def add_tool(self, record: ToolRecord) -> None:
        """Add one tool to the registry."""

    def list_tools(self) -> list[ToolRecord]:
        """Return all known tool records."""


class InMemoryToolRegistry(ToolRegistryProtocol):
    """Stores reusable tool records in memory."""

    def __init__(self) -> None:
        """Initialize an in-memory list for tool records."""
        self._records: list[ToolRecord] = []

    def add_tool(self, record: ToolRecord) -> None:
        """Add one tool to the registry."""
        self._records.append(record)

    def list_tools(self) -> list[ToolRecord]:
        """Return all known tool records."""
        return list(self._records)


ToolRegistry = InMemoryToolRegistry
