"""Building Block ontology — corpus graph (instances) view.

Implements the corpus side of the schema-vs-corpus split from FZ 1b.

The *schema* graph lives in :mod:`tessellum.bb.types` (8 BBType nodes +
:data:`tessellum.bb.types.BB_SCHEMA` edges). It is finite, closed,
type-level.

The *corpus* graph lives here. It is open, growing, instance-level —
the union of every BB-typed note in the vault (as :class:`BBNode`) and
every body-link / folgezettel-parent edge between them (as
:class:`BBEdge`). A corpus edge instantiates exactly one schema edge:
that's the type-check the validator + (future) BB-graph audit relies on.

Two constructors:

- :meth:`BBGraph.schema` returns a synthetic graph whose nodes are the
  8 BBTypes (one BBNode per type) and whose edges are
  :data:`tessellum.bb.types.BB_SCHEMA`. Useful for "what transitions
  are allowed?" queries that don't need the corpus.
- :meth:`BBGraph.from_db` loads the corpus graph from a built index DB
  (output of ``tessellum index build``). Streams notes + links rather
  than holding the whole DB connection.

The corpus graph is *read-only* in this module. DKS step-7 materialisers
write new notes through the format/composer pipeline; this module never
mutates the substrate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

from tessellum.bb.types import (
    BB_SCHEMA,
    BBType,
    EpistemicEdgeType,
    find_edge_type,
)


# ── BBNode + BBEdge — corpus instance dataclasses ─────────────────────────


@dataclass(frozen=True, kw_only=True)
class BBNode:
    """One BB-typed note in the corpus.

    Per design decision D1 (`plan_dks_expansion`), BBNode is the *base*
    of a subclass hierarchy: one frozen dataclass per :class:`BBType`,
    each fixing ``bb_type`` via ``field(default=..., init=False)``. This
    keeps the discriminator out of every constructor call while
    preserving static type checking — callers write
    ``ArgumentNode(note_id=..., warrant=...)`` and ``bb_type`` is
    populated automatically.

    Schema-graph synthetic nodes (one per BBType, produced by
    :meth:`BBGraph.schema`) use ``BBNode`` directly with explicit
    ``bb_type``; they're not "real" corpus instances and don't need
    the type-specific subclass machinery.
    """

    note_id: str = ""
    note_name: str = ""
    bb_type: BBType = BBType.NAVIGATION  # base default; subclasses override
    folgezettel: str | None = None
    folgezettel_parent: str | None = None
    note_status: str | None = None


# Subclass per BBType — D1 resolution. Each fixes bb_type via
# field(default=X, init=False), so callers don't pass it and the
# discriminator is statically typed by the class.


@dataclass(frozen=True, kw_only=True)
class EmpiricalObservationNode(BBNode):
    bb_type: BBType = field(default=BBType.EMPIRICAL_OBSERVATION, init=False)


@dataclass(frozen=True, kw_only=True)
class ConceptNode(BBNode):
    bb_type: BBType = field(default=BBType.CONCEPT, init=False)


@dataclass(frozen=True, kw_only=True)
class ModelNode(BBNode):
    bb_type: BBType = field(default=BBType.MODEL, init=False)


@dataclass(frozen=True, kw_only=True)
class HypothesisNode(BBNode):
    bb_type: BBType = field(default=BBType.HYPOTHESIS, init=False)


@dataclass(frozen=True, kw_only=True)
class ArgumentNode(BBNode):
    bb_type: BBType = field(default=BBType.ARGUMENT, init=False)


@dataclass(frozen=True, kw_only=True)
class CounterArgumentNode(BBNode):
    bb_type: BBType = field(default=BBType.COUNTER_ARGUMENT, init=False)


@dataclass(frozen=True, kw_only=True)
class ProcedureNode(BBNode):
    bb_type: BBType = field(default=BBType.PROCEDURE, init=False)


@dataclass(frozen=True, kw_only=True)
class NavigationNode(BBNode):
    bb_type: BBType = field(default=BBType.NAVIGATION, init=False)


_NODE_CLASS_BY_BB_TYPE: dict[BBType, type[BBNode]] = {
    BBType.EMPIRICAL_OBSERVATION: EmpiricalObservationNode,
    BBType.CONCEPT: ConceptNode,
    BBType.MODEL: ModelNode,
    BBType.HYPOTHESIS: HypothesisNode,
    BBType.ARGUMENT: ArgumentNode,
    BBType.COUNTER_ARGUMENT: CounterArgumentNode,
    BBType.PROCEDURE: ProcedureNode,
    BBType.NAVIGATION: NavigationNode,
}


def node_class_for(bb_type: BBType) -> type[BBNode]:
    """Return the typed `BBNode` subclass for a given `BBType`."""
    return _NODE_CLASS_BY_BB_TYPE[bb_type]


@dataclass(frozen=True)
class BBEdge:
    """One realised epistemic relation in the corpus graph.

    ``edge_type`` is the schema edge this corpus edge instantiates —
    or ``None`` if no matching schema edge exists (the corpus edge
    is then "untyped" and a validator-flag candidate).

    ``provenance`` records how the edge was discovered:

    - ``"body_link"`` — a markdown link in the source's body whose target
      resolves to a known BBNode.
    - ``"folgezettel_parent"`` — the source's ``folgezettel_parent:``
      field equals the target's ``folgezettel``.
    - ``"contradicts"`` — DKS step 4's edge between two argument notes
      (not present in the index yet; reserved for the v0.2+ DKS
      writer).
    """

    source_note_id: str
    target_note_id: str
    edge_type: EpistemicEdgeType | None
    provenance: str


# ── BBGraph — typed view over nodes + edges ───────────────────────────────


class BBGraph:
    """A typed graph over :class:`BBNode` and :class:`BBEdge`.

    Constructed from either the static schema (via :meth:`schema`) or
    the live corpus (via :meth:`from_db`). Two indexes are maintained
    for fast lookups:

    - ``_nodes_by_id``: ``note_id → BBNode``
    - ``_nodes_by_type``: ``BBType → tuple[BBNode]``

    All read methods are O(1) or O(|out-edges|); no global scans needed.
    """

    def __init__(self, nodes: Iterable[BBNode], edges: Iterable[BBEdge]) -> None:
        node_list = tuple(nodes)
        edge_list = tuple(edges)
        self._nodes_by_id: dict[str, BBNode] = {n.note_id: n for n in node_list}
        self._nodes_by_type: dict[BBType, tuple[BBNode, ...]] = {
            bb: tuple(n for n in node_list if n.bb_type is bb) for bb in BBType
        }
        self._edges: tuple[BBEdge, ...] = edge_list
        self._out_edges: dict[str, list[BBEdge]] = {}
        self._in_edges: dict[str, list[BBEdge]] = {}
        for e in edge_list:
            self._out_edges.setdefault(e.source_note_id, []).append(e)
            self._in_edges.setdefault(e.target_note_id, []).append(e)

    # ── Constructors ──

    @classmethod
    def schema(cls) -> "BBGraph":
        """Return the synthetic schema graph: 8 BBType nodes + BB_SCHEMA edges.

        Each synthetic node uses the BBType value as ``note_id`` and
        ``note_name``; ``folgezettel`` / ``folgezettel_parent`` /
        ``note_status`` are None.
        """
        nodes = tuple(
            BBNode(
                note_id=bb.value,
                note_name=bb.value,
                bb_type=bb,
            )
            for bb in BBType
        )
        edges = tuple(
            BBEdge(
                source_note_id=edge.source.value,
                target_note_id=edge.target.value,
                edge_type=edge,
                provenance="schema",
            )
            for edge in BB_SCHEMA
        )
        return cls(nodes, edges)

    @classmethod
    def from_db(cls, db_path: Path | str) -> "BBGraph":
        """Load the corpus graph from a built unified index DB.

        Walks ``Database.all_notes()`` to build BBNode rows for every
        note whose ``building_block:`` parses as a valid :class:`BBType`,
        then ``Database.all_links()`` to build BBEdge rows for every
        body-link between two BBNodes. The ``folgezettel_parent`` field
        contributes a second edge family (provenance="folgezettel_parent").

        Args:
            db_path: Index DB file. Must exist; raises FileNotFoundError
                otherwise.

        Returns:
            A BBGraph view over the corpus. Untyped corpus edges (no
            matching schema entry) are still included with
            ``edge_type=None`` so callers can audit them.
        """
        # Lazy import — avoids forcing every BB consumer to pay for the
        # indexer's sqlite dependency at module-load time.
        from tessellum.indexer.db import Database

        path = Path(db_path)
        with Database(path) as db:
            note_rows = db.all_notes()
            link_rows = db.all_links()

        bb_nodes: list[BBNode] = []
        fz_to_id: dict[str, str] = {}  # folgezettel → note_id
        for row in note_rows:
            bb_value = row.building_block
            if bb_value is None or bb_value not in BBType._value2member_map_:
                continue
            bb_type = BBType(bb_value)
            node_cls = _NODE_CLASS_BY_BB_TYPE[bb_type]
            node = node_cls(
                note_id=row.note_id,
                note_name=row.note_name,
                folgezettel=row.folgezettel,
                folgezettel_parent=row.folgezettel_parent,
                note_status=row.note_status,
            )
            bb_nodes.append(node)
            if row.folgezettel:
                fz_to_id[row.folgezettel] = row.note_id

        nodes_by_id = {n.note_id: n for n in bb_nodes}

        bb_edges: list[BBEdge] = []

        # Body-link edges — source/target must both be BB-typed.
        for link in link_rows:
            src = nodes_by_id.get(link.source_note_id)
            tgt = nodes_by_id.get(link.target_note_id)
            if src is None or tgt is None:
                continue
            edge_type = find_edge_type(src.bb_type, tgt.bb_type)
            bb_edges.append(
                BBEdge(
                    source_note_id=link.source_note_id,
                    target_note_id=link.target_note_id,
                    edge_type=edge_type,
                    provenance="body_link",
                )
            )

        # Folgezettel-parent edges — resolve via fz_to_id.
        for node in bb_nodes:
            if not node.folgezettel_parent:
                continue
            target_id = fz_to_id.get(node.folgezettel_parent)
            if target_id is None or target_id == node.note_id:
                continue
            target = nodes_by_id[target_id]
            edge_type = find_edge_type(node.bb_type, target.bb_type)
            bb_edges.append(
                BBEdge(
                    source_note_id=node.note_id,
                    target_note_id=target_id,
                    edge_type=edge_type,
                    provenance="folgezettel_parent",
                )
            )

        return cls(bb_nodes, bb_edges)

    # ── Queries ──

    @property
    def node_count(self) -> int:
        return len(self._nodes_by_id)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    def node(self, note_id: str) -> BBNode | None:
        """Return the BBNode with this ``note_id`` (or None if absent)."""
        return self._nodes_by_id.get(note_id)

    def nodes_of_type(self, bb_type: BBType) -> tuple[BBNode, ...]:
        """All BBNodes of the given type."""
        return self._nodes_by_type.get(bb_type, ())

    def out_edges(self, source_note_id: str) -> tuple[BBEdge, ...]:
        """Edges leaving ``source_note_id``."""
        return tuple(self._out_edges.get(source_note_id, ()))

    def in_edges(self, target_note_id: str) -> tuple[BBEdge, ...]:
        """Edges entering ``target_note_id``."""
        return tuple(self._in_edges.get(target_note_id, ()))

    def edges(self) -> tuple[BBEdge, ...]:
        """All edges in the graph (in insertion order)."""
        return self._edges

    def __iter__(self) -> Iterator[BBNode]:
        """Iterate over nodes in insertion order."""
        return iter(self._nodes_by_id.values())

    def __len__(self) -> int:
        return len(self._nodes_by_id)

    def __contains__(self, note_id: object) -> bool:
        return isinstance(note_id, str) and note_id in self._nodes_by_id

    # ── Audit helpers ──

    def untyped_edges(self) -> tuple[BBEdge, ...]:
        """Corpus edges that don't instantiate any schema edge.

        These are candidates for validator flags or schema extensions:
        either the link is wrong (LINK-003-style) or the schema is
        missing an edge type (R-P productive-half opportunity, like
        the ``counter_argument → model`` extension already declared in
        :data:`tessellum.bb.types.BB_SCHEMA_DKS_EXTENSIONS`).
        """
        return tuple(e for e in self._edges if e.edge_type is None)

    def edges_by_type(self) -> dict[str, int]:
        """Count realised edges per schema edge label.

        Returns a dict of ``label → count``. Untyped edges are grouped
        under the key ``"(untyped)"``. Useful for telemetry — a vault
        with 200 realised "naming" edges and 0 "challenging" edges has
        a structural-balance problem the BB graph makes visible.
        """
        counts: dict[str, int] = {}
        for e in self._edges:
            key = e.edge_type.label if e.edge_type is not None else "(untyped)"
            counts[key] = counts.get(key, 0) + 1
        return counts


__all__ = [
    "BBNode",
    "BBEdge",
    "BBGraph",
    # Per-BBType subclasses (D1)
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
