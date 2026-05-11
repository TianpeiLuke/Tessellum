"""Dialectic Knowledge System (DKS) — public API.

DKS is the closed-loop dialectic runtime that turns Tessellum's typed
substrate into a learning knowledge system. Each cycle takes an
observation, generates arguments from N perspectives, detects
disagreement (pairwise contradicts edges), captures a counter-argument
naming the broken Toulmin component, discovers a pattern, and emits
revised warrants — depositing a Folgezettel subtree per closed loop.

See ``thought_dks_design_synthesis`` (FZ 2a) + ``thought_dks_fz_integration``
(FZ 2a1) in the seed vault for the typed ontology + spatial mapping.

DKS uses the Composer LLM-backend abstractions
(:class:`tessellum.composer.MockBackend` /
:class:`tessellum.composer.AnthropicBackend`) but is otherwise an
independent module — peer to :mod:`tessellum.composer` (the contract-
pipeline executor), :mod:`tessellum.retrieval` (the read side), and
:mod:`tessellum.indexer` (the write-side substrate). Built on
Composer primitives; not owned by it.

Public-API capability map:

  - **Core cycle** — :class:`DKSCycle`, :class:`DKSRunner`,
    :func:`allocate_cycle_fz`, the seven component-output dataclasses.
  - **Confidence gating** — :class:`ConstantConfidence` /
    :class:`CalibratedConfidence` + :func:`decide_escalation`.
  - **Multi-perspective + Dung labelling** — N-argument support on
    :class:`DKSCycle` via the ``perspectives`` kwarg, plus the
    :class:`DungAF` / :func:`grounded_labelling` standalone module.
  - **Meta-DKS** — schema-mutation runtime under
    :mod:`tessellum.dks.meta`.
  - **Telemetry** — warrant history, silent-failure observability,
    multi-revision authoring.
"""

from tessellum.dks.core import (
    # Type aliases
    CounterStrength,
    CycleMode,
    ToulminComponent,
    WarrantChangeKind,
    # Component-output dataclasses
    DKSArgument,
    DKSContradicts,
    DKSCounterArgument,
    DKSCycleResult,
    DKSObservation,
    DKSPattern,
    DKSRuleRevision,
    DKSWarrant,
    # Multi-cycle
    DKSRunResult,
    WarrantChange,
    # Allocator
    allocate_cycle_fz,
    # Runtime
    DKSCycle,
    DKSRunner,
    # Helpers
    aggregate_warrant_changes,
)
from tessellum.dks.retrieval_client import (
    # P-side retrieval client (warrant-grounding evidence fetch)
    RetrievalClient,
    RetrievalHit,
)
from tessellum.dks.confidence import (
    # Confidence gating
    DEFAULT_CONFIDENCE_THRESHOLD,
    ConstantConfidence,
    DKSConfidenceModel,
    EscalationDecision,
    decide_escalation,
    # Learned confidence + calibration
    DEFAULT_RECENCY_HALFLIFE_CYCLES,
    DEFAULT_TARGET_FALSE_GATE_RATE,
    CalibratedConfidence,
    CalibrationResult,
    calibrate_from_traces,
)
from tessellum.dks.persistence import (
    # Warrant persistence
    HistoryEntry,
    WarrantHistory,
    WarrantRegistry,
    load_warrants_from_vault,
)
from tessellum.dks.fsm import (
    # FSM dispatcher over the BB schema
    BBPath,
    BBPathStep,
    DKSStateMachine,
    TransitionHandler,
)
from tessellum.dks.dung import (
    # Dung abstract argumentation framework + grounded semantics
    DungAF,
    DungLabel,
    grounded_extension,
    grounded_labelling,
)
from tessellum.dks.meta import (
    # Meta-DKS (schema-mutation runtime)
    Attacker,
    DEFAULT_MIN_CYCLES,
    HeuristicProposer,
    LLMAttacker,
    LLMProposer,
    META_ATTACK_KIND,
    META_SCHEMA,
    MetaCounterArgument,
    MetaCycle,
    MetaCycleResult,
    MetaEdgeType,
    MetaObservation,
    NoOpAttacker,
    Proposer,
    SchemaEditProposal,
    SCHEMA_EDIT_PROPOSAL_KIND,
    SURVIVE_THRESHOLD,
    load_event_log,
    write_event_log,
)


__all__ = [
    # Types
    "ToulminComponent",
    "CycleMode",
    "CounterStrength",
    "WarrantChangeKind",
    # Dataclasses
    "DKSObservation",
    "DKSWarrant",
    "DKSArgument",
    "DKSContradicts",
    "DKSCounterArgument",
    "DKSPattern",
    "DKSRuleRevision",
    "DKSCycleResult",
    "WarrantChange",
    "DKSRunResult",
    # Allocator
    "allocate_cycle_fz",
    # Runtime
    "DKSCycle",
    "DKSRunner",
    # Helpers
    "aggregate_warrant_changes",
    # P-side retrieval
    "RetrievalClient",
    "RetrievalHit",
    # FSM dispatcher over the BB schema
    "BBPath",
    "BBPathStep",
    "DKSStateMachine",
    "TransitionHandler",
    # Dung AF
    "DungAF",
    "DungLabel",
    "grounded_extension",
    "grounded_labelling",
    # Confidence gating
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DKSConfidenceModel",
    "ConstantConfidence",
    "EscalationDecision",
    "decide_escalation",
    # Learned confidence + calibration
    "DEFAULT_RECENCY_HALFLIFE_CYCLES",
    "DEFAULT_TARGET_FALSE_GATE_RATE",
    "CalibratedConfidence",
    "CalibrationResult",
    "calibrate_from_traces",
    # Warrant persistence
    "WarrantRegistry",
    "WarrantHistory",
    "HistoryEntry",
    "load_warrants_from_vault",
    # Meta-DKS (schema-mutation runtime)
    "DEFAULT_MIN_CYCLES",
    "META_SCHEMA",
    "MetaCycle",
    "MetaCycleResult",
    "MetaEdgeType",
    "MetaObservation",
    "Proposer",
    "HeuristicProposer",
    "LLMProposer",
    # Attacker
    "Attacker",
    "NoOpAttacker",
    "LLMAttacker",
    "MetaCounterArgument",
    "META_ATTACK_KIND",
    "SURVIVE_THRESHOLD",
    "SchemaEditProposal",
    "SCHEMA_EDIT_PROPOSAL_KIND",
    "load_event_log",
    "write_event_log",
]
