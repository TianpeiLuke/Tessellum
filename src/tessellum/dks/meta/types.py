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

from tessellum.bb.types import EpistemicEdgeType


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

    Three signal channels enrich the basic counts so the LLM proposer
    can reason from specifics rather than aggregates alone:

    - ``counter_strength_breakdown``: ``{component: {strength: count}}``
      stratifies the Toulmin distribution by counter strength.
      Supports "one strong outweighs two weak" weighting.
    - ``sample_counter_quotes``: ``{component: (quote, ...)}`` carries
      verbatim counter-argument quotes per Toulmin component.
    - ``observation_source_metadata``: free-form description of where
      the cycle-level observations came from (vault dogfood / live
      capture / synthetic). Lets the LLM proposer assess
      input-bias risk.

    The dataclass is the *input* the MetaCycle reasons over. The
    runtime builds it by reading cycle-level traces under
    ``runs/dks/``.
    """

    timestamp: str  # UTC ISO-8601 of when this observation was assembled
    cycles_examined: int
    top_attacked_warrants: tuple[tuple[str, int], ...] = ()  # (fz, count) tuples
    toulmin_failure_counts: dict[str, int] = field(default_factory=dict)
    unrealised_schema_edges: tuple[EpistemicEdgeType, ...] = ()
    # Enrichment signals (optional; default empty).
    counter_strength_breakdown: dict[str, dict[str, int]] = field(default_factory=dict)
    sample_counter_quotes: dict[str, tuple[str, ...]] = field(default_factory=dict)
    observation_source_metadata: str = ""
    # DKS silent-failure rate. Telemetry only — doesn't change the
    # decide_escalation semantics.
    silent_failure_count: int = 0
    """Aggregate count of silent backend-call failures across the
    cycle traces that produced this :class:`MetaObservation`.

    Populated by the CLI's ``_run_dks_meta`` builder from each cycle
    trace's ``silent_failures`` field. The LLMProposer's prompt
    surfaces this: when ``silent_failure_count > 0``, the proposer
    should factor degraded-backend likelihood into its proposals
    (a backend that's silently failing every other call may be
    producing misleading Toulmin distributions)."""

    # Per-perspective stratification for multi-perspective DKS runs.
    per_perspective_breakdown: dict[str, dict[str, int]] = field(default_factory=dict)
    """Per-perspective Toulmin failure distribution.

    Maps ``{argument_perspective: {broken_component: count}}``. Each
    entry counts the failures attributed to arguments produced under
    that perspective (i.e., counters whose attacked argument's
    perspective matched the key).

    Populated by the CLI from per-cycle traces when the
    ``argument_perspective`` field is present on the attacked
    argument. Empty when the cycle traces did not record perspectives.

    The LLMProposer prompt renders this as a stratified breakdown so
    the proposer can reason about perspective-specific schema gaps."""


# ── SchemaEditProposal — the meta-cycle's argument ─────────────────────────


SCHEMA_EDIT_PROPOSAL_KIND = Literal["add", "retract", "refine"]


@dataclass(frozen=True)
class SchemaEditProposal:
    """A typed proposal to mutate ``BB_SCHEMA_USER_EXTENSIONS``.

    Plays the role of an *argument* in the meta-cycle. Emitted by a
    :class:`tessellum.dks.meta.runtime.Proposer` — either the
    rule-based :class:`HeuristicProposer` or the LLM-driven
    :class:`LLMProposer`.

    Maps to a :class:`tessellum.bb.types.SchemaEditEvent` if the
    proposal survives meta-DKS dialectic and lands via
    ``tessellum dks meta --apply``.
    """

    kind: SCHEMA_EDIT_PROPOSAL_KIND
    edge: EpistemicEdgeType
    motivating_observation: str = ""  # narrative justification
    expected_impact: str = ""         # what the proposer predicts will improve
    supersedes: EpistemicEdgeType | None = None  # for "refine" only


# ── MetaCounterArgument — the meta-cycle's attack ──────────────────────────


META_ATTACK_KIND = Literal[
    "insufficient_evidence",
    "input_bias",
    "overgeneralisation",
    "collides_with_existing",
    "weak_signal",
]
"""Closed vocabulary for meta-counter attack kinds. Mirrors the
``attack_kind`` field on the meta-cycle skill canonical's step 2.

``input_bias`` fires when a proposal is responding to input bias
rather than a real schema gap.
"""

META_COUNTER_STRENGTH = Literal["weak", "moderate", "strong"]
"""Same Toulmin-style strength vocabulary used by cycle-level
:class:`tessellum.dks.core.DKSCounterArgument`."""


@dataclass(frozen=True)
class MetaCounterArgument:
    """A typed attack against a :class:`SchemaEditProposal`.

    Plays the role of a *counter-argument* in the meta-cycle.
    :class:`tessellum.dks.meta.runtime.LLMAttacker` emits these from
    LLM responses; :class:`tessellum.dks.meta.runtime.NoOpAttacker`
    (the default) emits none.

    Attacks reference proposals by their index in the build-stage
    output (matches the wire format the skill canonical specifies).
    """

    attacked_proposal_index: int
    attack_kind: META_ATTACK_KIND
    reason: str
    strength: META_COUNTER_STRENGTH = "moderate"


# ── Survive threshold ───────────────────────────────────────────────────────


SURVIVE_THRESHOLD = Literal["strict", "majority", "permissive"]
"""Aggregation policy for the meta-cycle's survive stage.

- ``strict``: a proposal survives iff zero attacks fire against it.
- ``majority`` (default): a proposal survives iff
  ``len(strong_attacks) <= 1 and len(moderate_attacks) <= 2``.
- ``permissive``: a proposal survives iff no ``strong`` attacks fire
  (any number of ``moderate`` / ``weak`` is tolerated).
"""


__all__ = [
    "META_STATES",
    "MetaEdgeType",
    "META_SCHEMA",
    "MetaObservation",
    "SchemaEditProposal",
    "SCHEMA_EDIT_PROPOSAL_KIND",
    # Attack types
    "MetaCounterArgument",
    "META_ATTACK_KIND",
    "META_COUNTER_STRENGTH",
    "SURVIVE_THRESHOLD",
]
