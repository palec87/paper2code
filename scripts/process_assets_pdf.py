"""Process a PDF from assets/ through the paper2code MVP pipeline."""

from pathlib import Path
import sys

from paper2code.extraction import CompositeExtractionProvider
from paper2code.extraction import ExtractionAgent
from paper2code.logging import Logger
from paper2code.logging import get_logger
from paper2code.models import IntermediateOutput
from paper2code.models import PaperArtifact
from paper2code.models import WorkflowStep
from paper2code.models import WorkflowUncertainty
from paper2code.pipeline import PaperToCodePipeline
from paper2code.planning import PlanningAgent
from paper2code.reduction import ReductionStrategy
from paper2code.reporting import TraceabilityInput


Logger.configure(level="INFO")
logger = get_logger(__name__)


class AssetsPlanningProvider:
    """Simple planning provider for asset PDF processing."""

    def plan(self, artifacts: list[PaperArtifact]) -> list[WorkflowStep]:
        """Create one workflow step when extracted artifacts exist."""
        if not artifacts:
            return []
        return [
            WorkflowStep(
                step_id="step-1",
                description="Run reproducible analysis for extracted paper.",
                tools=("python", "docker"),
                expected_outputs=("rationale",),
                uncertainty_level=WorkflowUncertainty.MEDIUM,
                confidence_score=0.85,
                uncertainty_note="Table/Figure extraction is heuristic.",
            )
        ]

    def plan_with_outputs(
        self,
        artifacts: list[PaperArtifact],
    ) -> tuple[list[WorkflowStep], list[IntermediateOutput]]:
        """Create planning outputs used by agreement checks."""
        steps = self.plan(artifacts)
        if not steps:
            return [], []
        return steps, [
            IntermediateOutput(
                output_id="step-1-rationale",
                step_id="step-1",
                name="rationale",
                location="Workflow selected from extracted publication parts.",
            )
        ]


def resolve_pdf_path() -> Path:
    """Resolve input PDF from CLI argument or assets/ folder."""
    if len(sys.argv) > 1:
        candidate = Path(sys.argv[1]).expanduser().resolve()
        if not candidate.exists() or candidate.suffix.lower() != ".pdf":
            raise FileNotFoundError(f"PDF not found: {candidate}")
        logger.info("Using PDF path from CLI: %s", candidate)
        return candidate

    assets_dir = Path("assets")
    if not assets_dir.exists():
        raise FileNotFoundError("assets/ directory does not exist")

    pdfs = sorted(assets_dir.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError("No PDF file found in assets/")
    logger.info("Using first assets PDF: %s", pdfs[0])
    return pdfs[0]


def main() -> None:
    """Run extraction, planning, and agreement checks for one asset PDF."""
    logger.info("Starting assets PDF processing script")
    pdf_path = resolve_pdf_path()

    extraction_agent = ExtractionAgent(provider=CompositeExtractionProvider())
    planning_agent = PlanningAgent(provider=AssetsPlanningProvider())
    reduction_strategy = ReductionStrategy()
    pipeline = PaperToCodePipeline(
        extraction_agent=extraction_agent,
        planning_agent=planning_agent,
        reduction_strategy=reduction_strategy,
    )

    traceability_rows = [
        TraceabilityInput(
            claim_id="claim-1",
            claim_text="Primary claim from publication.",
            evidence_text=f"Evidence extracted from {pdf_path.name}",
            step_id="step-1",
        )
    ]

    result = pipeline.run_with_agreement(
        document_text=str(pdf_path),
        run_id="assets-run",
        paper_id=pdf_path.stem,
        expected_value=0.80,
        observed_value=0.79,
        tolerance=0.03,
        traceability_rows=traceability_rows,
    )

    logger.info("Completed pipeline run for %s", pdf_path.name)
    print("paper2code assets pdf processor")
    print(f"pdf: {pdf_path}")
    print(f"artifacts: {len(result.artifacts)}")
    print(f"workflow steps: {len(result.workflow_steps)}")
    print(f"intermediate outputs: {len(result.intermediate_outputs)}")

    by_type: dict[str, int] = {}
    for artifact in result.artifacts:
        key = artifact.artifact_type
        by_type[key] = by_type.get(key, 0) + 1
    print("artifact types:")
    for artifact_type, count in sorted(by_type.items()):
        print(f"  {artifact_type}: {count}")

    if result.agreement_report is not None:
        logger.info("Agreement summary: %s", result.agreement_report.summary)
        print(f"agreement: {result.agreement_report.summary}")
    logger.info("Assets PDF processing script finished")


if __name__ == "__main__":
    main()
