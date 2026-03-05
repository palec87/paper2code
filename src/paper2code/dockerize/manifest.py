"""Manifest model for deterministic Docker runs."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DockerRunManifest:
    """Captures deterministic execution metadata for one run."""

    image_tag: str
    command: str
    input_mount: str
    output_mount: str
    dependency_lock: str
