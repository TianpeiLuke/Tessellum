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
]
