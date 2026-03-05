"""Core functionality for paper2code."""

__version__ = "0.1.0"

from paper2code.pipeline import PaperToCodePipeline
from paper2code.pipeline import PipelineResult
from paper2code.providers import MockExplanationProvider
from paper2code.providers import MockExtractionProvider
from paper2code.providers import MockPlanningProvider


def hello() -> str:
    """Return a greeting message."""
    return "Hello from paper2code!"


__all__ = [
    "MockExplanationProvider",
    "MockExtractionProvider",
    "MockPlanningProvider",
    "PaperToCodePipeline",
    "PipelineResult",
    "__version__",
    "hello",
]
