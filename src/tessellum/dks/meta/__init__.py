"""Meta-DKS — schema-mutation runtime (Phase 9 of plan_dks_expansion).

The recursive top: a *second* DKS walker whose substrate is the
schema itself. When cycle-level DKS keeps hitting the same Toulmin
failure on the same warrant shape, meta-DKS proposes a schema edit
(add edge, retract edge, refine label). The edit is itself
dialectical — authored as a SchemaEditProposal, attacked by
counter-proposals, possibly retracted.

Recursion stops one level up: the **meta-meta-schema**
(``META_SCHEMA``, defined in :mod:`tessellum.dks.meta.types`) is
human-authored and PR-gated per D4. Meta-DKS edits ``BB_SCHEMA`` via
:class:`tessellum.bb.types.SchemaEditEvent`; nothing edits
``META_SCHEMA`` automatically.

Architecture per FZ 2c1 (design synthesis):

  - :class:`MetaObservation` — reads cycle-level telemetry (top-K
    attacked warrants, Toulmin failure distribution, unrealised
    schema edges) and packages it as the *empirical anchor* for the
    meta-cycle.
  - :class:`SchemaEditProposal` — the meta-cycle's argument shape: a
    typed proposal to add / retract / refine a schema edge, with
    motivating evidence + predicted impact.
  - :class:`MetaCycle` — drives the meta-FSM dialectic. v0.0.52 ships
    the *mechanism* with a minimum-viable proposal generator;
    learned proposal generation lands in Phase 11+.
  - :data:`META_SCHEMA` — the human-authored meta-meta-schema. PR
    review is the only path to amend it.

Per D8: schema edits don't retroactively invalidate corpus notes.
Every note carries a ``bb_schema_version`` field (defaulted to 1 for
v0.0.47-era notes); TESS-005 validates against that recorded version.
``tessellum bb migrate --target-version current`` is the opt-in tool
for retroactive validation reports.
"""

from tessellum.dks.meta.types import (
    META_SCHEMA,
    MetaEdgeType,
    MetaObservation,
    SchemaEditProposal,
    SCHEMA_EDIT_PROPOSAL_KIND,
)
from tessellum.dks.meta.runtime import (
    DEFAULT_MIN_CYCLES,
    MetaCycle,
    MetaCycleResult,
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
    # Runtime
    "DEFAULT_MIN_CYCLES",
    "MetaCycle",
    "MetaCycleResult",
    "load_event_log",
    "write_event_log",
]
