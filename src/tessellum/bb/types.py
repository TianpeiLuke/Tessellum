"""Building Block ontology — types and schema graph.

Implements the design proposed at FZ 1b (``thought_bb_ontology_as_typed_graph``)
and formalised as an FSM at FZ 2a2 (``thought_dks_as_fsm_on_bb_graph``).

This module is the *source of truth* for the BB ontology:

- :class:`BBType` — the 8 building-block types. :data:`VALID_BUILDING_BLOCKS`
  in :mod:`tessellum.format.frontmatter_spec` is derived from this enum.
- :class:`EpistemicEdgeType` — one typed transition (source BBType, target
  BBType, semantic label).
- :data:`BB_SCHEMA_EPISTEMIC` — the 8 BB→BB epistemic edges from FZ 1.
- :data:`BB_SCHEMA_NAVIGATION` — the 7 NAV→* indexing edges.
- :data:`BB_SCHEMA_DKS_EXTENSIONS` — runtime-required edges not in FZ 1's
  10-edge narrative (currently: ``counter_argument → model`` for DKS
  step 6's pattern discovery).
- :data:`BB_SCHEMA` — the full schema: ``EPISTEMIC + NAVIGATION + DKS_EXTENSIONS``.

The schema is closed and finite. Adding a BB type or edge here means
amending FZ 1 (or its successor) and re-validating the corpus. That's
exactly R-P's productive half: schema mutates only via disciplined
revision; the runtime exercises whatever the schema declares.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


# ── 8 BB types — the FSM's states ──────────────────────────────────────────


class BBType(StrEnum):
    """The 8 Building Block types.

    Source of truth for the BB enum across Tessellum:

    - :mod:`tessellum.format.frontmatter_spec` ``VALID_BUILDING_BLOCKS``
      derives from ``BBType``.
    - DKS dataclasses (``DKSObservation``, ``DKSArgument``, ...) carry a
      ``bb_type`` class-attribute pointing here.
    - The corpus's ``building_block:`` YAML field must be one of these
      values (validator rule YAML-063).

    Order is meaningful for diagram conventions but not load-bearing.
    """

    EMPIRICAL_OBSERVATION = "empirical_observation"
    CONCEPT = "concept"
    MODEL = "model"
    HYPOTHESIS = "hypothesis"
    ARGUMENT = "argument"
    COUNTER_ARGUMENT = "counter_argument"
    PROCEDURE = "procedure"
    NAVIGATION = "navigation"


# Convenience: frozenset of string values, for users who want the legacy
# ``frozenset[str]`` shape rather than the enum.
VALID_BB_TYPE_VALUES: frozenset[str] = frozenset(t.value for t in BBType)


# ── EpistemicEdgeType — one typed transition ───────────────────────────────


@dataclass(frozen=True)
class EpistemicEdgeType:
    """One typed transition in the BB ontology schema graph.

    Each edge type is the directed pair (``source``, ``target``) plus a
    semantic ``label`` naming the operation it carries (``naming``,
    ``structuring``, ``predicting``, ``codifying``, ``testing``,
    ``challenging``, ``motivates_new``, ``execution_data``, ``indexes``,
    or — for the DKS Phase-4-class extension — ``pattern_of_failure``).

    ``EpistemicEdgeType`` is a *type*, not an *instance*. A corpus edge
    (:class:`tessellum.bb.graph.BBEdge`) is one realisation of one
    ``EpistemicEdgeType``; the schema graph has ~16 such types, and the
    corpus graph can have many edges realising each type.
    """

    source: BBType
    target: BBType
    label: str


# ── BB_SCHEMA_EPISTEMIC — the 8 BB→BB epistemic edges from FZ 1 ────────────


# These eight edges form the dialectic cycle:
#
#     OBS → CON → MOD → HYP → ARG → CTR → OBS
#                  └──→ PRO → OBS
#
# See FZ 1 (``thought_building_block_ontology_relationships``) for the
# narrative and mermaid diagram. FZ 1b sharpens the closure properties.
BB_SCHEMA_EPISTEMIC: tuple[EpistemicEdgeType, ...] = (
    EpistemicEdgeType(BBType.EMPIRICAL_OBSERVATION, BBType.CONCEPT, "naming"),
    EpistemicEdgeType(BBType.CONCEPT, BBType.MODEL, "structuring"),
    EpistemicEdgeType(BBType.MODEL, BBType.HYPOTHESIS, "predicting"),
    EpistemicEdgeType(BBType.MODEL, BBType.PROCEDURE, "codifying"),
    EpistemicEdgeType(BBType.HYPOTHESIS, BBType.ARGUMENT, "testing"),
    EpistemicEdgeType(BBType.ARGUMENT, BBType.COUNTER_ARGUMENT, "challenging"),
    EpistemicEdgeType(BBType.COUNTER_ARGUMENT, BBType.EMPIRICAL_OBSERVATION, "motivates_new"),
    EpistemicEdgeType(BBType.PROCEDURE, BBType.EMPIRICAL_OBSERVATION, "execution_data"),
)


# ── BB_SCHEMA_NAVIGATION — the 7 NAV→* indexing edges ──────────────────────


# Navigation is the meta-node: it indexes the other 7 BB types without
# participating in the dialectic cycle. FZ 1's narrative collapses these
# 7 edges into a single "Navigation → all types" family for readability;
# the implementation expands them so the FSM can type-check NAV-to-X
# transitions like any other.
BB_SCHEMA_NAVIGATION: tuple[EpistemicEdgeType, ...] = tuple(
    EpistemicEdgeType(BBType.NAVIGATION, target, "indexes")
    for target in (
        BBType.EMPIRICAL_OBSERVATION,
        BBType.CONCEPT,
        BBType.MODEL,
        BBType.HYPOTHESIS,
        BBType.ARGUMENT,
        BBType.COUNTER_ARGUMENT,
        BBType.PROCEDURE,
    )
)


# ── BB_SCHEMA_DKS_EXTENSIONS — runtime-required edges not in FZ 1 ──────────


# The DKS runtime's step 6 (pattern discovery) walks an edge from a
# ``counter_argument`` to a ``model`` — the pattern aggregates the
# contradiction into a typed regularity. FZ 1's 10-edge narrative does
# not declare this edge; FZ 1b + FZ 2a2 flag it as a Phase-4-class
# schema-extension opportunity (R-P's productive half).
#
# Including it here makes the FSM type-check DKS's step 6 cleanly. The
# alternative (declaring step 6's edge as a non-typed "plumbing" link)
# was the v0.0.40–v0.0.46 status quo; this tuple is the canonical place
# to record the runtime-driven schema growth.
BB_SCHEMA_DKS_EXTENSIONS: tuple[EpistemicEdgeType, ...] = (
    EpistemicEdgeType(
        BBType.COUNTER_ARGUMENT, BBType.MODEL, "pattern_of_failure"
    ),
)


# ── BB_SCHEMA — the complete schema graph ─────────────────────────────────


BB_SCHEMA: tuple[EpistemicEdgeType, ...] = (
    *BB_SCHEMA_EPISTEMIC,
    *BB_SCHEMA_NAVIGATION,
    *BB_SCHEMA_DKS_EXTENSIONS,
)


# ── Lookup helpers ────────────────────────────────────────────────────────


def find_edge_type(
    source: BBType, target: BBType, label: str | None = None
) -> EpistemicEdgeType | None:
    """Return the EpistemicEdgeType matching ``(source, target[, label])``, if any.

    When ``label`` is None, returns the first matching ``(source, target)``
    pair (the (source, target) tuple is unique across BB_SCHEMA today, so
    "first" and "only" coincide). When ``label`` is supplied and no edge
    matches, returns None.
    """
    for edge in BB_SCHEMA:
        if edge.source is source and edge.target is target:
            if label is None or edge.label == label:
                return edge
    return None


def edges_from(source: BBType) -> tuple[EpistemicEdgeType, ...]:
    """All schema edges leaving ``source``."""
    return tuple(e for e in BB_SCHEMA if e.source is source)


def edges_to(target: BBType) -> tuple[EpistemicEdgeType, ...]:
    """All schema edges entering ``target``."""
    return tuple(e for e in BB_SCHEMA if e.target is target)


def is_valid_transition(source: BBType, target: BBType) -> bool:
    """True iff ``(source, target)`` is a declared schema edge.

    Used by corpus-edge validators (e.g. TESS-004 could be generalised to
    "every realised body-link between two BB-typed notes must instantiate
    a declared schema edge"). The current TESS-004 only enforces this for
    ``counter_argument → argument`` (the "Challenging" edge in reverse;
    DKS step 5's attacked-link rule).
    """
    return find_edge_type(source, target) is not None


__all__ = [
    "BBType",
    "VALID_BB_TYPE_VALUES",
    "EpistemicEdgeType",
    "BB_SCHEMA_EPISTEMIC",
    "BB_SCHEMA_NAVIGATION",
    "BB_SCHEMA_DKS_EXTENSIONS",
    "BB_SCHEMA",
    "find_edge_type",
    "edges_from",
    "edges_to",
    "is_valid_transition",
]
