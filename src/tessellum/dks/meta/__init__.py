"""Meta-DKS — schema-mutation runtime.

The recursive top: a *second* DKS walker whose substrate is the
schema itself. When cycle-level DKS keeps hitting the same Toulmin
failure on the same warrant shape, meta-DKS proposes a schema edit
(add edge, retract edge, refine label). The edit is itself
dialectical — authored as a :class:`SchemaEditProposal`, attacked by
counter-proposals, possibly retracted.

Recursion stops one level up: the **meta-meta-schema**
(``META_SCHEMA``, defined in :mod:`tessellum.dks.meta.types`) is
human-authored and PR-gated per D4. Meta-DKS edits ``BB_SCHEMA`` via
:class:`tessellum.bb.types.SchemaEditEvent`; nothing edits
``META_SCHEMA`` automatically.

Architecture (FZ 2c1 design synthesis):

  - :class:`MetaObservation` — reads cycle-level telemetry (top-K
    attacked warrants, Toulmin failure distribution, unrealised
    schema edges) and packages it as the *empirical anchor* for the
    meta-cycle.
  - :class:`SchemaEditProposal` — the meta-cycle's argument shape: a
    typed proposal to add / retract / refine a schema edge, with
    motivating evidence + predicted impact.
  - :class:`MetaCounterArgument` — typed attack against a proposal,
    naming one of five closed-vocabulary attack kinds.
  - :class:`MetaCycle` — drives the meta-FSM dialectic with
    configurable :class:`Proposer` (heuristic or LLM-driven) and
    :class:`Attacker` (no-op or LLM-driven) strategies + a
    configurable survival threshold (strict / majority / permissive).
  - :data:`META_SCHEMA` — the human-authored meta-meta-schema. PR
    review is the only path to amend it.

Schema edits don't retroactively invalidate corpus notes (D8 —
frozen-at-creation discipline). Every note carries a
``bb_schema_version`` field; TESS-005 validates against that recorded
version. :data:`tessellum.bb.BB_SCHEMA_AT_VERSION` reconstructs the
schema at any past version; ``tessellum bb migrate --target-version
current`` is the opt-in tool for retroactive validation reports.
"""

from tessellum.dks.meta.types import (
    META_ATTACK_KIND,
    META_SCHEMA,
    MetaCounterArgument,
    MetaEdgeType,
    MetaObservation,
    SchemaEditProposal,
    SCHEMA_EDIT_PROPOSAL_KIND,
    SURVIVE_THRESHOLD,
)
from tessellum.dks.meta.runtime import (
    Attacker,
    DEFAULT_MIN_CYCLES,
    HeuristicProposer,
    LLMAttacker,
    LLMProposer,
    MetaCycle,
    MetaCycleResult,
    NoOpAttacker,
    Proposer,
    load_event_log,
    write_event_log,
)


__all__ = [
    # Types
    "MetaEdgeType",
    "META_SCHEMA",
    "MetaObservation",
    "SchemaEditProposal",
    "SCHEMA_EDIT_PROPOSAL_KIND",
    # Attack types (the meta-cycle's counter-argument vocabulary)
    "MetaCounterArgument",
    "META_ATTACK_KIND",
    "SURVIVE_THRESHOLD",
    # Runtime
    "DEFAULT_MIN_CYCLES",
    "MetaCycle",
    "MetaCycleResult",
    "Proposer",
    "HeuristicProposer",
    "LLMProposer",
    "Attacker",
    "NoOpAttacker",
    "LLMAttacker",
    "load_event_log",
    "write_event_log",
]
