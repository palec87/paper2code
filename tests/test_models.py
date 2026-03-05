"""Tests for phase-1 paper2code models and utilities."""

from paper2code.models import AgreementCheck
from paper2code.models import OntologyNode
from paper2code.models import ToolRecord
from paper2code.registry import ToolRegistry
from paper2code.validation import AgreementValidator


def test_numerical_tolerance_check_passes() -> None:
    """Agreement check should pass when difference is within tolerance."""
    validator = AgreementValidator()
    check: AgreementCheck = validator.numerical_tolerance_check(
        check_id="check-1",
        metric_name="f1",
        expected=0.90,
        observed=0.895,
        tolerance=0.01,
    )
    assert check.passed is True


def test_registry_roundtrip() -> None:
    """Tool registry should store and return one inserted record."""
    registry = ToolRegistry()
    record = ToolRecord(
        tool_id="tool-1",
        name="pdf-parser",
        modality="text",
        input_contract="pdf_path",
        output_contract="artifact_list",
        confidence=0.82,
    )
    registry.add_tool(record)
    assert registry.list_tools() == [record]


def test_ontology_node_metadata_defaults_to_empty_dict() -> None:
    """Ontology node should initialize metadata with an empty dictionary."""
    node = OntologyNode(node_id="n1", label="Claim", node_type="claim")
    assert node.metadata == {}
