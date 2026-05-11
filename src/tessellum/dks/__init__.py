"""Dialectic Knowledge System (DKS) — public API.

DKS is the closed-loop dialectic runtime that turns Tessellum's typed
substrate into a learning knowledge system. Each cycle takes an
observation, generates two arguments from different perspectives,
detects disagreement, captures a counter-argument naming the broken
Toulmin component, discovers a pattern, and emits a revised warrant —
depositing a 6-node Folgezettel subtree per closed loop. See
``plans/plan_dks_implementation.md`` for the full design and
``vault/resources/analysis_thoughts/thought_dks_design_synthesis.md``
(FZ 2a) + ``thought_dks_fz_integration.md`` (FZ 2a1) for the typed
ontology + spatial mapping.

DKS uses the Composer LLM-backend abstractions (``MockBackend`` /
``AnthropicBackend``) but is otherwise an independent module — peer to
``tessellum.composer`` (the contract-pipeline executor),
``tessellum.retrieval`` (the read side), and ``tessellum.indexer`` (the
write-side substrate). Built on Composer primitives; not owned by it.

Per the plan:

  - Phase 1 (v0.0.40): single-cycle core + FZ allocator (this module)
  - Phase 2 (v0.0.42): tessellum-dks-cycle skill canonical + sidecar
  - Phase 3 (v0.0.43): multi-cycle DKSRunner + tessellum dks CLI
  - Phase 4 (v0.0.44): P-side retrieval client + TESS-004 validator
  - Phase 5 (v0.0.45): confidence gating + warrant persistence
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
    # Multi-cycle (Phase 3)
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
    # P-side R-Cross client (Phase 4)
    RetrievalClient,
    RetrievalHit,
)
from tessellum.dks.confidence import (
    # Phase 5 — confidence gating
    DEFAULT_CONFIDENCE_THRESHOLD,
    ConstantConfidence,
    DKSConfidenceModel,
    EscalationDecision,
    decide_escalation,
    # Phase 7 — learned confidence + calibration
    DEFAULT_RECENCY_HALFLIFE_CYCLES,
    DEFAULT_TARGET_FALSE_GATE_RATE,
    CalibratedConfidence,
    CalibrationResult,
    calibrate_from_traces,
)
from tessellum.dks.persistence import (
    # Phase 5 — warrant persistence
    HistoryEntry,
    WarrantHistory,
    WarrantRegistry,
    load_warrants_from_vault,
)
from tessellum.dks.fsm import (
    # Phase 8 — FSM dispatcher (deferred FZ 2a2 work)
    BBPath,
    BBPathStep,
    DKSStateMachine,
    TransitionHandler,
)
from tessellum.dks.dung import (
    # Phase 10 — Dung abstract argumentation framework + grounded semantics
    DungAF,
    DungLabel,
    grounded_extension,
    grounded_labelling,
)
from tessellum.dks.meta import (
    # Phase 9 — meta-DKS (schema-mutation runtime)
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
    # P-side retrieval (Phase 4)
    "RetrievalClient",
    "RetrievalHit",
    # FSM dispatcher (Phase 8 — deferred FZ 2a2 work)
    "BBPath",
    "BBPathStep",
    "DKSStateMachine",
    "TransitionHandler",
    # Dung AF (Phase 10)
    "DungAF",
    "DungLabel",
    "grounded_extension",
    "grounded_labelling",
    # Confidence gating (Phase 5)
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DKSConfidenceModel",
    "ConstantConfidence",
    "EscalationDecision",
    "decide_escalation",
    # Learned confidence + calibration (Phase 7)
    "DEFAULT_RECENCY_HALFLIFE_CYCLES",
    "DEFAULT_TARGET_FALSE_GATE_RATE",
    "CalibratedConfidence",
    "CalibrationResult",
    "calibrate_from_traces",
    # Warrant persistence (Phase 5)
    "WarrantRegistry",
    "WarrantHistory",
    "HistoryEntry",
    "load_warrants_from_vault",
    # Meta-DKS (Phase 9 — schema-mutation runtime)
    "DEFAULT_MIN_CYCLES",
    "META_SCHEMA",
    "MetaCycle",
    "MetaCycleResult",
    "MetaEdgeType",
    "MetaObservation",
    "Proposer",
    "HeuristicProposer",
    "LLMProposer",
    # v0.0.53 Phase B.3 — Attacker
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
