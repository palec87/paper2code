"""PDF extraction helpers for publication inputs."""

import importlib

from paper2code.models import PaperArtifact


class PDFExtractor:
    """Extract text, tables, and figure cues from PDF files."""

    def extract(self, pdf_path: str) -> list[PaperArtifact]:
        """Extract artifacts from a PDF file.

        Uses pypdf when available and degrades gracefully when missing.
        """
        try:
            pypdf = importlib.import_module("pypdf")
        except ImportError:
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

        reader = pypdf.PdfReader(pdf_path)
        artifacts: list[PaperArtifact] = []
        for page_index, page in enumerate(reader.pages, start=1):
            page_text = (page.extract_text() or "").strip()
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
            if "figure" in page_text.lower() or "fig." in page_text.lower():
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
        return artifacts
