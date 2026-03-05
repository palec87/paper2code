"""Tool registry abstractions."""

from paper2code.registry.tool_registry import InMemoryToolRegistry
from paper2code.registry.tool_registry import ToolRegistry
from paper2code.registry.tool_registry import ToolRegistryProtocol

try:
    from paper2code.registry.postgres_backend import PostgreSQLToolRegistry
except ImportError:  # pragma: no cover - optional dependency
    PostgreSQLToolRegistry = None

__all__ = [
    "InMemoryToolRegistry",
    "PostgreSQLToolRegistry",
    "ToolRegistry",
    "ToolRegistryProtocol",
]
