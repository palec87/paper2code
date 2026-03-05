"""PDF extraction helpers for publication inputs."""

import importlib
import logging

from paper2code.logging import get_logger
from paper2code.models import PaperArtifact


logger = get_logger(__name__)


class PDFExtractor:
    """Extract text, tables, and figure cues from PDF files."""

    def extract(self, pdf_path: str) -> list[PaperArtifact]:
        """Extract artifacts from a PDF file.

        Uses pypdf when available and degrades gracefully when missing.
        """
        logger.info("Starting PDF extraction: %s", pdf_path)
        try:
            pypdf = importlib.import_module("pypdf")
        except ImportError:
            logger.warning(
                "Missing optional dependency 'pypdf'; "
                "returning unsupported artifact"
            )
            return [
                PaperArtifact(
                    artifact_id="pdf-unsupported",
                    artifact_type="text",
                    source_path=pdf_path,
                    content=(
                        "pypdf is not installed; "
                        "PDF text extraction unavailable."
                    ),
                    confidence=0.0,
                    source_format="pdf",
                    extraction_method="missing_dependency",
                )
            ]

        # Reduce noisy internal warnings from corrupted/odd PDF streams.
        pypdf_logger = logging.getLogger("pypdf")
        filters_logger = logging.getLogger("pypdf.filters")
        previous_pypdf_level = pypdf_logger.level
        previous_filters_level = filters_logger.level
        pypdf_logger.setLevel(logging.ERROR)
        filters_logger.setLevel(logging.ERROR)

        reader = pypdf.PdfReader(pdf_path)
        logger.debug("Loaded PDF with %d pages", len(reader.pages))
        artifacts: list[PaperArtifact] = []
        try:
            for page_index, page in enumerate(reader.pages, start=1):
                try:
                    page_text = (page.extract_text() or "").strip()
                except Exception as error:  # pragma: no cover
                    logger.warning(
                        "Failed to extract page %d from %s: %s",
                        page_index,
                        pdf_path,
                        error,
                    )
                    continue

                logger.debug(
                    "Processing PDF page %d with %d chars",
                    page_index,
                    len(page_text),
                )
                if page_text:
                    artifacts.append(
                        PaperArtifact(
                            artifact_id=f"pdf-text-{page_index}",
                            artifact_type="text",
                            source_path=pdf_path,
                            content=page_text,
                            confidence=0.85,
                            source_format="pdf",
                            extraction_method="pypdf",
                        )
                    )
                if "table" in page_text.lower():
                    logger.debug("Detected table cue on page %d", page_index)
                    artifacts.append(
                        PaperArtifact(
                            artifact_id=f"pdf-table-{page_index}",
                            artifact_type="table",
                            source_path=pdf_path,
                            content=page_text,
                            confidence=0.6,
                            source_format="pdf",
                            extraction_method="keyword_detection",
                        )
                    )
                has_figure = (
                    "figure" in page_text.lower()
                    or "fig." in page_text.lower()
                )
                if has_figure:
                    logger.debug("Detected figure cue on page %d", page_index)
                    artifacts.append(
                        PaperArtifact(
                            artifact_id=f"pdf-figure-{page_index}",
                            artifact_type="figure",
                            source_path=pdf_path,
                            content=page_text,
                            confidence=0.6,
                            source_format="pdf",
                            extraction_method="keyword_detection",
                        )
                    )
        finally:
            pypdf_logger.setLevel(previous_pypdf_level)
            filters_logger.setLevel(previous_filters_level)

        if not artifacts:
            logger.warning("No extractable text found in PDF: %s", pdf_path)
            artifacts.append(
                PaperArtifact(
                    artifact_id="pdf-no-text",
                    artifact_type="text",
                    source_path=pdf_path,
                    content=(
                        "No extractable text found in PDF. "
                        "Document may require OCR preprocessing."
                    ),
                    confidence=0.1,
                    source_format="pdf",
                    extraction_method="no_extractable_text",
                )
            )

        logger.info(
            "Finished PDF extraction for %s with %d artifacts",
            pdf_path,
            len(artifacts),
        )
        return artifacts
