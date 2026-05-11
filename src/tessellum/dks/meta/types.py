"""Meta-DKS types — the meta-meta-schema + dataclasses.

D4 resolution: ``META_SCHEMA`` lives in code, PR-gated. The meta-FSM
the meta-cycle walks is *itself* a tiny schema (5 states + 4
transitions); it does not need event-sourcing because it does not
mutate at runtime — only via PR amendments to this module.

Why human-author the meta-meta-schema and not bootstrap it like
BB_SCHEMA: the recursion has to stop somewhere or we have an
infinite tower of meta-meta-meta-schemas. The architectural
commitment per D4: one level up from cycle-level DKS is the limit;
the meta-level itself is hand-authored at the project layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from tessellum.bb.types import BBType, EpistemicEdgeType


# ── META_SCHEMA — the meta-meta-schema (D4) ────────────────────────────────


META_STATES: tuple[str, ...] = (
    "meta_observation",   # q₀: the telemetry-derived anchor
    "meta_argument",      # an SchemaEditProposal
    "meta_counter",       # attack on a proposal
    "meta_pattern",       # cross-proposal regularity
    "meta_revision",      # the landed SchemaEditEvent (terminal)
)


@dataclass(frozen=True)
class MetaEdgeType:
    """One transition in the meta-FSM. Same shape as
    :class:`tessellum.bb.types.EpistemicEdgeType` but for meta-states."""

    source: str  # one of META_STATES
    target: str  # one of META_STATES
    label: str


# The 4 transitions the meta-cycle walks. Closed; not event-sourced.
# PR review is the only path to amend.
META_SCHEMA: tuple[MetaEdgeType, ...] = (
    MetaEdgeType("meta_observation", "meta_argument", "proposing"),
    MetaEdgeType("meta_argument", "meta_counter", "attacking"),
    MetaEdgeType("meta_counter", "meta_pattern", "aggregating"),
    MetaEdgeType("meta_pattern", "meta_revision", "landing"),
)


# ── MetaObservation — telemetry-derived anchor ─────────────────────────────


@dataclass(frozen=True)
class MetaObservation:
    """Aggregated telemetry from past cycle-level DKS runs.

    Three signal channels feed the meta-cycle's reasoning:

    1. **Top attacked warrants**: warrant FZs that have been
       superseded (revised) frequently. Implies "this warrant shape
       is contested; perhaps the schema is missing a constraint."
    2. **Toulmin failure distribution**: counts of each
       ``broken_component`` value across counter-arguments. A
       lopsided distribution (e.g. 80% ``counter-example``) suggests
       the schema lacks a specific edge or constraint relevant to
       that failure mode.
    3. **Unrealised schema edges**: BB-pairs in ``BB_SCHEMA`` with
       zero realised instances in the corpus. Could mean the edge is
       wrong (retract candidate) or the runtime never walks it (no
       action needed).

    The dataclass is the *input* the MetaCycle reasons over. The
    runtime builds it by reading cycle-level traces under
    ``runs/dks/``.
    """

    timestamp: str  # UTC ISO-8601 of when this observation was assembled
    cycles_examined: int
    top_attacked_warrants: tuple[tuple[str, int], ...] = ()  # (fz, count) tuples
    toulmin_failure_counts: dict[str, int] = field(default_factory=dict)
    unrealised_schema_edges: tuple[EpistemicEdgeType, ...] = ()


# ── SchemaEditProposal — the meta-cycle's argument ─────────────────────────


SCHEMA_EDIT_PROPOSAL_KIND = Literal["add", "retract", "refine"]


@dataclass(frozen=True)
class SchemaEditProposal:
    """A typed proposal to mutate ``BB_SCHEMA_USER_EXTENSIONS``.

    Plays the role of an *argument* in the meta-cycle. v0.0.52's
    minimum-viable proposal generator emits these from rule-based
    heuristics (e.g. "if Toulmin failure ``counter-example`` exceeds
    50% of counters, propose adding a ``scope_assertion`` edge").
    Phase 11+ will replace the heuristic with an LLM-driven
    proposer.

    Maps to a :class:`tessellum.bb.types.SchemaEditEvent` if the
    proposal survives meta-DKS dialectic and lands via
    ``tessellum dks meta --apply``.
    """

    kind: SCHEMA_EDIT_PROPOSAL_KIND
    edge: EpistemicEdgeType
    motivating_observation: str = ""  # narrative justification
    expected_impact: str = ""         # what the proposer predicts will improve
    supersedes: EpistemicEdgeType | None = None  # for "refine" only


__all__ = [
    "META_STATES",
    "MetaEdgeType",
    "META_SCHEMA",
    "MetaObservation",
    "SchemaEditProposal",
    "SCHEMA_EDIT_PROPOSAL_KIND",
]
