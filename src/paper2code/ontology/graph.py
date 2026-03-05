"""In-memory ontology graph for argument and data reasoning."""

from paper2code.models import OntologyEdge
from paper2code.models import OntologyNode


class OntologyGraph:
    """Stores ontology nodes and edges for MVP reasoning use-cases."""

    def __init__(self) -> None:
        """Initialize empty graph state."""
        self._nodes: dict[str, OntologyNode] = {}
        self._edges: dict[str, OntologyEdge] = {}

    def add_node(self, node: OntologyNode) -> None:
        """Add or replace an ontology node by identifier."""
        self._nodes[node.node_id] = node

    def add_edge(self, edge: OntologyEdge) -> None:
        """Add or replace an ontology edge by identifier."""
        self._edges[edge.edge_id] = edge

    def list_nodes(self) -> list[OntologyNode]:
        """Return all nodes currently in the graph."""
        return list(self._nodes.values())

    def list_edges(self) -> list[OntologyEdge]:
        """Return all edges currently in the graph."""
        return list(self._edges.values())
