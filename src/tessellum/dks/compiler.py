"""tessellum.dks.compiler — deterministic DKSCycleResult → NoteIntentGraph.

P3 of the DKS refactor plan (decisions b1a + b5a). Turns a completed DKS cycle
into an atomic, replayable vault transaction — **building only the compiler and
reusing the dynamic-digestion substrate wholesale** (P5): the resulting
``NoteIntentGraph`` flows through the shipped ``project_note_intent_graph`` →
``write_closure`` → ``overlay`` → ``publication.py`` PREPARED→PUBLISHED→
ACKNOWLEDGED + snapshot-CAS path. This module re-derives NONE of that.

A3.1 — the mechanical mapping (NO LLM call; the prose is already in the cycle
result):

- observation      → ``empirical_observation`` intent (spans + t_event)
- surviving argument → ``argument`` intent (Toulmin fields)
- defeated attack  → ``counter_argument`` intent (typed edge back to the attacked)
- candidate regularity → ``hypothesis``/``pattern`` intent — a MODEL, never an
  empirical fact by default (a discovered regularity is provisional)
- warrant proposal → versioned warrant intent (``procedure``) with ``supersedes``

The compiler is PURE and byte-stable: the same ``DKSCycleResult`` always yields
the same ``NoteIntentGraph`` (deterministic target paths + ordering), which is
what makes the downstream promotion replayable.
"""

from __future__ import annotations

from tessellum.composer.knowledge_plan import (
    ClaimProvenance,
    NoteIntent,
    NoteIntentGraph,
)
from tessellum.dks.core import DKSCycleResult

# Where each BB role's notes live in the vault. Deterministic + role-keyed so a
# compiled FZ node always maps to the same target path (replay stability).
_ROLE_DIR = {
    "empirical_observation": "resources/analysis_thoughts",
    "argument": "resources/analysis_thoughts",
    "counter_argument": "resources/analysis_thoughts",
    "model": "areas/models",
    "hypothesis": "resources/analysis_thoughts",
    "procedure": "resources/analysis_thoughts",
}


def _target_path(role: str, fz: str) -> str:
    """A deterministic vault-relative path for a compiled node. FZ is embedded
    so two cycles never collide and the path is reproducible from the result."""
    directory = _ROLE_DIR.get(role, "resources/analysis_thoughts")
    safe_fz = fz.replace("/", "_")
    return f"{directory}/dks_{role}_{safe_fz}.md"


def _provenance_for(cycle: DKSCycleResult, extra_span: str | None = None) -> tuple[ClaimProvenance, ...]:
    """Every compiled note cites the cycle's observation as its source span
    (P1 provenance floor). A non-empty tuple is required by NoteIntent."""
    obs_fz = cycle.observation.folgezettel
    src = f"dks-cycle://{cycle.cycle_id}#observation:{obs_fz}"
    span_id = extra_span or obs_fz
    return (ClaimProvenance(span_id=span_id, source_ref=src),)


class DKSNoteCompiler:
    """Compile a completed ``DKSCycleResult`` into a typed ``NoteIntentGraph``.

    Pure — no LLM, no I/O. ``compile(cycle)`` returns a ``NoteIntentGraph``
    ready for the shipped substrate; ``compile`` is byte-stable across calls."""

    def compile(self, cycle: DKSCycleResult) -> NoteIntentGraph:
        intents: list[NoteIntent] = []

        # 1. the observation → empirical_observation (create).
        obs_fz = cycle.observation.folgezettel
        intents.append(NoteIntent(
            note_id=_target_path("empirical_observation", obs_fz),
            thesis=cycle.observation.summary or "observation",
            building_block="empirical_observation",
            target_path=_target_path("empirical_observation", obs_fz),
            provenance=_provenance_for(cycle),
        ))

        # 2. the arguments → argument intents (each cites the observation).
        args = cycle.arguments or tuple(
            a for a in (cycle.argument_a, cycle.argument_b) if a is not None
        )
        for arg in args:
            intents.append(NoteIntent(
                note_id=_target_path("argument", arg.folgezettel),
                thesis=arg.warrant.claim or "argument",
                building_block="argument",
                target_path=_target_path("argument", arg.folgezettel),
                provenance=_provenance_for(cycle, extra_span=arg.folgezettel),
                # the argument depends on (extends) the observation it reasons from
                depends_on=(_target_path("empirical_observation", obs_fz),),
            ))

        # 3. the defeated attack → counter_argument (typed edge to the attacked).
        if cycle.counter is not None:
            attacked_path = _target_path("argument", cycle.counter.attacked_fz)
            intents.append(NoteIntent(
                note_id=_target_path("counter_argument", cycle.counter.folgezettel),
                thesis=cycle.counter.counter_claim or "counter-argument",
                building_block="counter_argument",
                target_path=_target_path("counter_argument", cycle.counter.folgezettel),
                provenance=_provenance_for(cycle, extra_span=cycle.counter.folgezettel),
                depends_on=(attacked_path,),  # the counter attacks this argument
            ))

        # 4. the candidate regularity → a MODEL/hypothesis, never an empirical
        #    fact by default (a discovered pattern is provisional). It depends
        #    on the counter it aggregates (the realized COUNTER_ARGUMENT → MODEL
        #    "pattern_of_failure" schema edge) so the whole cycle stays ONE
        #    invariant-closed transaction (a cycle is atomic — it must not
        #    partition into disjoint capsules).
        pattern_path: str | None = None
        if cycle.pattern is not None:
            pattern_path = _target_path("model", cycle.pattern.folgezettel)
            pattern_deps: tuple[str, ...] = ()
            if cycle.counter is not None:
                pattern_deps = (
                    _target_path("counter_argument", cycle.counter.folgezettel),
                )
            intents.append(NoteIntent(
                note_id=pattern_path,
                thesis=cycle.pattern.description or "candidate regularity",
                building_block="model",
                target_path=pattern_path,
                provenance=_provenance_for(cycle, extra_span=cycle.pattern.folgezettel),
                depends_on=pattern_deps,
            ))

        # 5. the warrant proposal(s) → versioned warrant intent. Each revision
        #    depends on the pattern it closes (pattern → revision) so it joins
        #    the single cycle capsule; a revision that supersedes a PRIOR
        #    cycle's warrant additionally depends on that warrant's path
        #    (cross-cycle coupling; the disposition stays "create" — a new
        #    versioned note).
        rev_fzs_this_cycle = {rev.folgezettel for rev in cycle.rule_revisions}
        for rev in cycle.rule_revisions:
            deps: list[str] = []
            if pattern_path is not None:
                deps.append(pattern_path)
            if rev.supersedes and rev.supersedes not in rev_fzs_this_cycle:
                deps.append(_target_path("procedure", rev.supersedes))
            intents.append(NoteIntent(
                note_id=_target_path("procedure", rev.folgezettel),
                thesis=rev.revised_warrant.warrant or "revised warrant",
                building_block="procedure",
                target_path=_target_path("procedure", rev.folgezettel),
                provenance=_provenance_for(cycle, extra_span=rev.folgezettel),
                depends_on=tuple(deps),
            ))

        return NoteIntentGraph(
            objective_id=f"dks-cycle:{cycle.cycle_id}",
            intents=tuple(intents),
        )


__all__ = ["DKSNoteCompiler"]
