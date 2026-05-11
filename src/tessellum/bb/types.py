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
from typing import Literal, Sequence


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
# contradiction into a typed regularity. The 10-edge core narrative does
# not declare this edge; the design trail flags it as a schema-extension
# opportunity (R-P's productive half).
#
# Including it here makes the FSM type-check DKS's step 6 cleanly. This
# tuple is the canonical place to record runtime-driven schema growth
# that the static palette would otherwise miss.
BB_SCHEMA_DKS_EXTENSIONS: tuple[EpistemicEdgeType, ...] = (
    EpistemicEdgeType(
        BBType.COUNTER_ARGUMENT, BBType.MODEL, "pattern_of_failure"
    ),
)


# ── BB_SCHEMA_USER_EXTENSIONS — event-sourced runtime growth ──────────────


# Schema growth is *event-sourced*. Meta-DKS proposes schema edits as
# :class:`SchemaEditEvent`s; the current active set
# ``BB_SCHEMA_USER_EXTENSIONS`` is the fold over an append-only event
# log. Retractions are first-class events; the log itself is never
# rewritten.
#
# The package ships with an empty default event log. Real events land
# via ``tessellum dks meta --apply`` and live at
# ``runs/dks/meta/schema_events.jsonl`` — outside the package and the
# vault, in the same shape as the warrant_history.jsonl trace.


SCHEMA_EDIT_KIND = Literal["added", "retracted", "refined"]


@dataclass(frozen=True)
class SchemaEditEvent:
    """One typed event in the schema's append-only edit log.

    Per D3 (`plan_dks_expansion`): schema state is retractable, schema
    history is append-only. Each event records one transformation of
    the active ``BB_SCHEMA_USER_EXTENSIONS`` set.

    - ``"added"``: a new edge enters the active set.
    - ``"retracted"``: an existing edge leaves the active set. The
      historical event stays in the log; corpus edges that
      instantiated the retracted edge become *untyped* (TESS-005
      surfaces them as a migration signal).
    - ``"refined"``: an edge is replaced by a narrower / broader
      version (e.g., changing a label). ``superseded_by`` carries the
      replacement's identity so a reader can follow the chain.

    ``motivating_failure`` is the FZ ID (or short description) of the
    cycle-level observation or counter that drove this edit. Anchors
    the dialectical justification; meta-DKS's argument generator
    cites this when proposing the edit.
    """

    timestamp: str  # UTC ISO-8601
    kind: SCHEMA_EDIT_KIND
    edge: EpistemicEdgeType
    motivating_failure: str = ""
    superseded_by: str | None = None


def fold_schema_events(
    events: Sequence[SchemaEditEvent],
) -> tuple[EpistemicEdgeType, ...]:
    """Compute the active ``BB_SCHEMA_USER_EXTENSIONS`` from a log of edits.

    Walks events in order. ``added`` puts the edge in the set;
    ``retracted`` removes it; ``refined`` removes the old edge + adds
    the new one. Same-edge re-additions are no-ops (already in the set).

    Returns a stable-ordered tuple (insertion order, deduplicated).
    """
    active: list[EpistemicEdgeType] = []

    def _key(e: EpistemicEdgeType) -> tuple:
        return (e.source, e.target, e.label)

    seen: set[tuple] = set()

    for event in events:
        k = _key(event.edge)
        if event.kind == "added":
            if k not in seen:
                active.append(event.edge)
                seen.add(k)
        elif event.kind == "retracted":
            if k in seen:
                active = [e for e in active if _key(e) != k]
                seen.discard(k)
        elif event.kind == "refined":
            # Refined: drop the prior version (matched by source+target,
            # any label) and add the new one. Label changes are the
            # typical case.
            base_key = (event.edge.source, event.edge.target)
            active = [
                e for e in active if (e.source, e.target) != base_key
            ]
            seen = {x for x in seen if (x[0], x[1]) != base_key}
            active.append(event.edge)
            seen.add(k)

    return tuple(active)


# Default event log: empty. The log grows when ``tessellum dks meta
# --apply`` runs. Override via :func:`set_user_extensions_from_events`
# for tests + CLI integration.
_SCHEMA_EVENT_LOG: list[SchemaEditEvent] = []

# Active user-extensions set — folded from the event log at module
# load. Recomputed via :func:`refresh_user_extensions`.
BB_SCHEMA_USER_EXTENSIONS: tuple[EpistemicEdgeType, ...] = ()


def set_user_extensions_from_events(
    events: Sequence[SchemaEditEvent],
) -> None:
    """Replace the in-memory schema-event log + recompute the active set.

    Used by the CLI on startup to load past events from
    ``runs/dks/meta/schema_events.jsonl``, and by tests to seed
    deterministic schemas. The module-level :data:`BB_SCHEMA` is also
    rebuilt to include the refreshed user extensions.
    """
    global _SCHEMA_EVENT_LOG, BB_SCHEMA_USER_EXTENSIONS, BB_SCHEMA, BB_SCHEMA_VERSION
    _SCHEMA_EVENT_LOG = list(events)
    BB_SCHEMA_USER_EXTENSIONS = fold_schema_events(_SCHEMA_EVENT_LOG)
    # Invalidate the per-version cache — event log identity has changed.
    _SCHEMA_AT_VERSION_CACHE.clear()
    BB_SCHEMA = (
        *BB_SCHEMA_EPISTEMIC,
        *BB_SCHEMA_NAVIGATION,
        *BB_SCHEMA_DKS_EXTENSIONS,
        *BB_SCHEMA_USER_EXTENSIONS,
    )
    # Version bumps once per landed `added` or `retracted` event
    # (refined edits don't grow the version separately — they're the
    # composition of a retract + add).
    BB_SCHEMA_VERSION = 1 + sum(
        1 for e in _SCHEMA_EVENT_LOG if e.kind in ("added", "retracted")
    )


def schema_event_log() -> tuple[SchemaEditEvent, ...]:
    """Return the in-memory event log (defensive copy)."""
    return tuple(_SCHEMA_EVENT_LOG)


# ── BB_SCHEMA_AT_VERSION — version-aware schema reconstruction ─────────────


def BB_SCHEMA_AT_VERSION(
    version: int,
) -> tuple[EpistemicEdgeType, ...]:
    """Reconstruct the BB_SCHEMA tuple as of a specific version.

    The frozen-at-creation D8 discipline (every captured note records
    its ``bb_schema_version`` in YAML frontmatter) is only useful if
    callers can ask: *what did the schema look like at version N?*
    This helper answers that question by folding the prefix of
    ``_SCHEMA_EVENT_LOG`` whose post-fold version number is ``≤ version``.

    The core epistemic + navigation + DKS extensions are constant
    across all versions (they live in module-level tuples that no
    runtime event can mutate per D4). Only the
    :data:`BB_SCHEMA_USER_EXTENSIONS` portion varies with the event
    log; this function folds it at the requested version.

    Args:
        version: Integer ≥ 1. Version 1 = the core static schema with
            no user extensions; each ``added`` or ``retracted`` event
            bumps the version by 1.

    Returns:
        The full ``BB_SCHEMA`` tuple as of the requested version.

    Raises:
        ValueError: ``version < 1``.

    Memoised per ``(version, len(_SCHEMA_EVENT_LOG))`` — repeated calls
    at the same version against the same event log return cached
    results. Cache resets implicitly whenever the event log replaces
    (via :func:`set_user_extensions_from_events`).
    """
    if version < 1:
        raise ValueError(f"version must be >= 1; got {version}")
    cache_key = (version, len(_SCHEMA_EVENT_LOG), id(_SCHEMA_EVENT_LOG))
    cached = _SCHEMA_AT_VERSION_CACHE.get(cache_key)
    if cached is not None:
        return cached
    # Fold the prefix of the event log whose post-fold version is
    # ``<= version``. v=1 means zero events applied; v=N means the
    # first (N-1) added/retracted events applied.
    target_event_count = version - 1
    applied = 0
    truncated_events: list[SchemaEditEvent] = []
    for event in _SCHEMA_EVENT_LOG:
        if event.kind in ("added", "retracted"):
            if applied >= target_event_count:
                break
            applied += 1
        truncated_events.append(event)
    user_extensions = fold_schema_events(truncated_events)
    schema = (
        *BB_SCHEMA_EPISTEMIC,
        *BB_SCHEMA_NAVIGATION,
        *BB_SCHEMA_DKS_EXTENSIONS,
        *user_extensions,
    )
    _SCHEMA_AT_VERSION_CACHE[cache_key] = schema
    return schema


_SCHEMA_AT_VERSION_CACHE: dict[tuple, tuple[EpistemicEdgeType, ...]] = {}


# ── BB_SCHEMA_VERSION — bumps on every landed event ────────────────────────


# Version 1 = the core static schema with the project's initial DKS
# extensions. Every ``added`` or ``retracted`` event from meta-DKS
# bumps the version. Corpus notes record their ``bb_schema_version``
# at creation, and TESS-005 validates against that recorded version
# (not the current one) for frozen-at-creation semantics.
BB_SCHEMA_VERSION: int = 1


# ── BB_SCHEMA — the complete schema graph ─────────────────────────────────


# Composed from four sources:
#
#   - BB_SCHEMA_EPISTEMIC (8): the FZ 1 epistemic edges
#   - BB_SCHEMA_NAVIGATION (7): NAV → X indexing edges
#   - BB_SCHEMA_DKS_EXTENSIONS (1+): runtime-driven edits the project
#     team commits to via the package source (e.g. CTR → MOD)
#   - BB_SCHEMA_USER_EXTENSIONS (0+): event-sourced meta-DKS edits
#     loaded from runs/dks/meta/schema_events.jsonl at CLI startup
BB_SCHEMA: tuple[EpistemicEdgeType, ...] = (
    *BB_SCHEMA_EPISTEMIC,
    *BB_SCHEMA_NAVIGATION,
    *BB_SCHEMA_DKS_EXTENSIONS,
    *BB_SCHEMA_USER_EXTENSIONS,
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
    "BB_SCHEMA_USER_EXTENSIONS",
    "BB_SCHEMA",
    "BB_SCHEMA_AT_VERSION",
    "BB_SCHEMA_VERSION",
    "SCHEMA_EDIT_KIND",
    "SchemaEditEvent",
    "fold_schema_events",
    "set_user_extensions_from_events",
    "schema_event_log",
    "find_edge_type",
    "edges_from",
    "edges_to",
    "is_valid_transition",
]
