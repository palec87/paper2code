"""Typed data models used across the paper2code workflow."""

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class PaperArtifact:
    """Represents one extracted artifact from a publication."""

    artifact_id: str
    artifact_type: str
    source_path: str
    content: str
    confidence: float = 1.0


@dataclass(slots=True, frozen=True)
class WorkflowStep:
    """Describes a planned step in the executable workflow."""

    step_id: str
    description: str
    tools: tuple[str, ...]
    expected_outputs: tuple[str, ...]
    uncertainty_note: str | None = None


@dataclass(slots=True, frozen=True)
class IntermediateOutput:
    """Represents a persisted intermediate output of a workflow step."""

    output_id: str
    step_id: str
    name: str
    location: str


@dataclass(slots=True, frozen=True)
class AgreementCheck:
    """Stores agreement metrics between implementation and publication."""

    check_id: str
    metric_name: str
    expected: str
    observed: str
    passed: bool
    details: str = ""


@dataclass(slots=True, frozen=True)
class MissingInfoItem:
    """Captures a gap or ambiguity found in the publication."""

    item_id: str
    category: str
    severity: str
    description: str
    suggested_action: str


@dataclass(slots=True, frozen=True)
class ToolRecord:
    """Defines a reusable tool stored in the registry."""

    tool_id: str
    name: str
    modality: str
    input_contract: str
    output_contract: str
    confidence: float


@dataclass(slots=True, frozen=True)
class OntologyNode:
    """Represents an ontology entity extracted from publications."""

    node_id: str
    label: str
    node_type: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class OntologyEdge:
    """Represents an ontology relation between two nodes."""

    edge_id: str
    source_node_id: str
    target_node_id: str
    relation_type: str
