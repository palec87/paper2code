"""Intermediate output tracking for workflow planning."""

from pathlib import Path

from paper2code.models import IntermediateOutput


class IntermediateOutputTracker:
    """Persists planning intermediate outputs to a run directory."""

    def __init__(self, run_dir: str = "runs") -> None:
        """Initialize tracker root directory."""
        self._root = Path(run_dir)
        self._root.mkdir(parents=True, exist_ok=True)

    def emit_output(
        self,
        step_id: str,
        name: str,
        content: str,
    ) -> IntermediateOutput:
        """Persist one output and return a typed output descriptor."""
        step_dir = self._root / f"step_{step_id}"
        step_dir.mkdir(parents=True, exist_ok=True)
        file_path = step_dir / f"{name}.txt"
        file_path.write_text(content, encoding="utf-8")
        output_id = f"{step_id}-{name}"
        return IntermediateOutput(
            output_id=output_id,
            step_id=step_id,
            name=name,
            location=str(file_path),
        )
