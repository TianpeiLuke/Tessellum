"""Building Block ontology — public API.

The BB ontology is Tessellum's typed substrate. This module is the
*source of truth* for the 8 BB types + the schema graph of epistemic
edges they form. See:

- FZ 1: :doc:`thought_building_block_ontology_relationships` — the
  original 8-type / 10-edge ontology
- FZ 1b: :doc:`thought_bb_ontology_as_typed_graph` — schema-vs-corpus
  split + graph properties + data-structure proposal (the design this
  module implements)
- FZ 2a2: :doc:`thought_dks_as_fsm_on_bb_graph` — DKS as an FSM walker
  over the schema graph defined here

Two layers:

- :mod:`tessellum.bb.types` — the schema: ``BBType`` enum +
  ``EpistemicEdgeType`` + ``BB_SCHEMA_*``. Closed at 8 nodes + ~16
  typed edges; mutates only via disciplined schema revision.
- :mod:`tessellum.bb.graph` — the corpus: ``BBNode`` + ``BBEdge`` +
  ``BBGraph``. Open, growing, view-only.

Typical use::

    from tessellum.bb import BBType, BB_SCHEMA, BBGraph

    # Schema-side: enumerate valid transitions
    for edge in BB_SCHEMA:
        print(f"{edge.source.value} --[{edge.label}]--> {edge.target.value}")

    # Corpus-side: load the live graph from the index
    graph = BBGraph.from_db("data/tessellum.db")
    print(f"{graph.node_count} BB nodes, {graph.edge_count} BB edges")
    print(graph.edges_by_type())
"""

from tessellum.bb.types import (
    BB_SCHEMA,
    BB_SCHEMA_DKS_EXTENSIONS,
    BB_SCHEMA_EPISTEMIC,
    BB_SCHEMA_NAVIGATION,
    BBType,
    EpistemicEdgeType,
    VALID_BB_TYPE_VALUES,
    edges_from,
    edges_to,
    find_edge_type,
    is_valid_transition,
)
from tessellum.bb.graph import (
    ArgumentNode,
    BBEdge,
    BBGraph,
    BBNode,
    ConceptNode,
    CounterArgumentNode,
    EmpiricalObservationNode,
    HypothesisNode,
    ModelNode,
    NavigationNode,
    ProcedureNode,
    node_class_for,
)


__all__ = [
    # Types (schema-level)
    "BBType",
    "VALID_BB_TYPE_VALUES",
    "EpistemicEdgeType",
    "BB_SCHEMA_EPISTEMIC",
    "BB_SCHEMA_NAVIGATION",
    "BB_SCHEMA_DKS_EXTENSIONS",
    "BB_SCHEMA",
    # Lookups
    "find_edge_type",
    "edges_from",
    "edges_to",
    "is_valid_transition",
    # Graph (corpus-level)
    "BBNode",
    "BBEdge",
    "BBGraph",
    # Per-BBType BBNode subclasses (D1, Phase 8)
    "EmpiricalObservationNode",
    "ConceptNode",
    "ModelNode",
    "HypothesisNode",
    "ArgumentNode",
    "CounterArgumentNode",
    "ProcedureNode",
    "NavigationNode",
    "node_class_for",
]
