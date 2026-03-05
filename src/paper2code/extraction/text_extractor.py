"""Text extraction helpers for publication content."""

import re

from paper2code.models import PaperArtifact


_SECTION_RE = re.compile(r"^(#+\s+)?([A-Za-z][A-Za-z\s]{2,40}):?$")


class TextSectionExtractor:
    """Extract section-like artifacts from plain text documents."""

    def extract(self, text: str, source_path: str) -> list[PaperArtifact]:
        """Extract section chunks and return typed artifacts."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        artifacts: list[PaperArtifact] = []
        section_name = "full_text"
        buffer: list[str] = []

        def flush(current_section: str, chunk: list[str]) -> None:
            if not chunk:
                return
            chunk_text = "\n".join(chunk)
            index = len(artifacts) + 1
            confidence = 0.9 if current_section != "full_text" else 0.8
            artifacts.append(
                PaperArtifact(
                    artifact_id=f"text-{index}",
                    artifact_type="text",
                    source_path=source_path,
                    content=chunk_text,
                    confidence=confidence,
                    source_format="text",
                    extraction_method="section_parser",
                )
            )

        for line in lines:
            match = _SECTION_RE.match(line)
            if match and len(buffer) >= 2:
                flush(section_name, buffer)
                section_name = match.group(2).strip().lower().replace(" ", "_")
                buffer = []
                continue
            buffer.append(line)
        flush(section_name, buffer)
        return artifacts
