"""Typed corpus-plan model + plan-shape decision — the hierarchy above a flat plan.

Phases **M1 + M2** of the multi-document corpus-digestion plan (FZ
20k9c1a1a1b7b1). This module is the typed layer that sits ABOVE the flat
:class:`tessellum.composer.knowledge_plan.NoteIntentGraph`: a corpus of source
documents (admitted as ONE :class:`~tessellum.composer.knowledge_plan.SourceBundle`)
is decomposed, above a volume threshold, into a **master plan (a pure index)
plus N self-contained sub-objectives**, each of which owns a slice of the
bundle and later projects to its OWN flat ``NoteIntentGraph`` — the shipped
per-note transaction substrate is reused one level down, unchanged.

Action items realized here (all pure — no clock, no randomness, no I/O
anywhere in this module):

* **M1 (A-shape)** — a typed :class:`PlanShape` decision + the pure
  :func:`classify_plan_shape` classifier. The plan shape is a value the plan
  skill's ``source_assessment`` step already emits as free text
  (``skill_tessellum_plan_digestion.md`` enum ``single_plan`` /
  ``single_plan_phased`` / ``master_plus_subplans``) but which NO engine code
  consumes today. This gives it a typed home and a deterministic classifier so
  the driver can branch on it. Thresholds are ported VERBATIM from the skill
  §1d (≤10k words / ≤15 notes → single; 10k–30k / 15–30 → phased; >30k / >30 →
  master+subplans).

* **M2** — frozen pydantic-v2 :class:`SubObjective` / :class:`CorpusPlan`
  typed models. Style mirrors
  :class:`tessellum.composer.knowledge_plan.NoteIntent` /
  :class:`~tessellum.composer.knowledge_plan.NoteIntentGraph`
  (``ConfigDict(frozen=True, extra="forbid")`` + immutable ``tuple[...]`` +
  ``Literal`` discriminators). A :class:`SubObjective` owns a slice of the
  bundle (``member_ordinals``), carries a ``priority`` for wave ordering, and
  declares ``depends_on`` edges to sibling sub-objectives. A :class:`CorpusPlan`
  holds the master index (derivable PURELY from the sub-objectives — the
  "master plan is a pure index, never duplicates note tables" invariant) plus
  the corpus-wide term-ownership inventory and shared cross-references.

The per-``SubObjective`` ``NoteIntentGraph`` is populated LATER (M3, the
sub-plan planning wave); this module carries only the corpus skeleton and the
slice/priority/dependency structure, so it stays pure and off the live path.

Content-id reuse (no reinvented hashing): :func:`corpus_plan_content_id`
reuses :func:`tessellum.composer.proposals.canonical_json_bytes` (float-ban +
NFC-normalized + sorted keys), so the id is order- and process-stable. This
module imports ONLY from :mod:`tessellum.composer.proposals` (plus stdlib +
pydantic) — no runtime, no materializer — keeping the composer import DAG
acyclic (composer never imports runtime).
"""

from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tessellum.composer.proposals import canonical_json_bytes

# ── M1 — the plan-shape decision ────────────────────────────────────────────

PlanShape = Literal["single_plan", "single_plan_phased", "master_plus_subplans"]
"""How a source (single doc or a corpus) should be planned. Values match the
plan skill's ``source_assessment`` enum verbatim
(``skill_tessellum_plan_digestion.md``):

- ``single_plan``: ≤ ~10,000 words / ≤15 notes → one flat plan.
- ``single_plan_phased``: 10,000–30,000 words / 15–30 notes → one flat plan
  executed in phases (still ONE ``NoteIntentGraph``, no sub-plans).
- ``master_plus_subplans``: > ~30,000 words / >30 notes → a pure-index master
  plan plus N self-contained sub-objectives.

Only ``master_plus_subplans`` triggers the :class:`CorpusPlan` hierarchy; the
other two keep the shipped single-``NoteIntentGraph`` path byte-identical."""

# Thresholds ported VERBATIM from skill §1d. Word thresholds are the primary
# axis (the skill measures words); the note-count band is the derived proxy.
SINGLE_PLAN_MAX_WORDS = 10_000
PHASED_MAX_WORDS = 30_000
SINGLE_PLAN_MAX_NOTES = 15
PHASED_MAX_NOTES = 30


def classify_plan_shape(total_words: int, est_note_count: int) -> PlanShape:
    """Decide the plan shape from measured aggregate volume (M1) — pure.

    Ports the skill §1d decision verbatim. The two axes (words, est notes) are
    combined by the STRONGER signal: if EITHER axis crosses a band boundary the
    larger shape is chosen, so a word-dense-but-few-notes corpus and a
    many-small-notes corpus are both decomposed. ``master_plus_subplans`` wins
    if either axis is over its phased ceiling; ``single_plan_phased`` wins if
    either is over its single ceiling; else ``single_plan``.

    Both inputs must be non-negative ints (floats are banned from the hashed
    payload downstream; negative volume is a caller bug).
    """
    if total_words < 0 or est_note_count < 0:
        raise ValueError(
            f"volume inputs must be non-negative: "
            f"total_words={total_words}, est_note_count={est_note_count}"
        )
    if total_words > PHASED_MAX_WORDS or est_note_count > PHASED_MAX_NOTES:
        return "master_plus_subplans"
    if total_words > SINGLE_PLAN_MAX_WORDS or est_note_count > SINGLE_PLAN_MAX_NOTES:
        return "single_plan_phased"
    return "single_plan"


# ── M2 — the sub-objective ──────────────────────────────────────────────────

SubObjectivePriority = Literal["P1", "P2", "P3"]
"""Wave-ordering priority for a sub-objective. ``P1`` foundational sub-plans
(concepts others reference) commit first, then ``P2`` operational, then ``P3``
specialized — matching the skill's execution-order rule. Same-priority,
no-dependency sub-objectives may run concurrently."""


class SubObjective(BaseModel):
    """One sub-plan within a corpus decomposition (M2).

    Mirrors the :class:`~tessellum.composer.knowledge_plan.NoteIntent` idiom:
    ``frozen=True`` blocks reassignment, ``extra="forbid"`` rejects unknown
    fields (closed model), every collection is an immutable ``tuple[...]``.

    A sub-objective owns a SLICE of the parent bundle (``member_ordinals``,
    referencing :attr:`~tessellum.composer.knowledge_plan.BundleMember.ordinal`)
    and is planned/executed as its OWN snapshot-pinned, invariant-closed
    knowledge transaction (the shipped per-note substrate, reused one level
    down). Its ``NoteIntentGraph`` is populated later (M3); this model carries
    only the skeleton.

    Attributes:
        sub_id: Stable corpus-local id; ``depends_on`` edges + the master index
            reference it.
        topic: Human-readable domain/chapter label (e.g. "Permissions").
        priority: Wave-ordering rung (``P1`` foundational → ``P3`` specialized).
        member_ordinals: The bundle-member ordinals this sub-objective owns.
            REQUIRED, non-empty, unique, ascending-normalized.
        est_note_count: Expected notes this sub-objective produces (skill
            heuristic: 4–10; a value >15 signals it should be split further).
        depends_on: Sibling ``sub_id`` refs this sub-objective's cross-links
            resolve against (so a foundational sub-plan commits first).

    Validators (``model_validator(mode="after")``):
        - ``member_ordinals`` non-empty, unique, and re-sorted ascending.
        - self-dependency guard: ``sub_id`` may not appear in ``depends_on``.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    sub_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    priority: SubObjectivePriority = "P2"
    member_ordinals: tuple[int, ...] = Field(..., min_length=1)
    est_note_count: int = Field(ge=0)
    depends_on: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _check_slice_and_deps(self) -> "SubObjective":
        if any(o < 0 for o in self.member_ordinals):
            raise ValueError("member_ordinals must be non-negative")
        if len(set(self.member_ordinals)) != len(self.member_ordinals):
            raise ValueError(
                f"SubObjective {self.sub_id!r} has duplicate member_ordinals"
            )
        ordered = tuple(sorted(self.member_ordinals))
        if ordered != self.member_ordinals:
            object.__setattr__(self, "member_ordinals", ordered)
        if self.sub_id in self.depends_on:
            raise ValueError(
                f"SubObjective {self.sub_id!r} cannot depend on itself"
            )
        return self


# ── M2 — the term-ownership + shared-cross-ref rows ─────────────────────────


class TermOwnerRow(BaseModel):
    """One row of the corpus-wide term-ownership inventory (M2, feeds the M6
    gate). Each undigested term the corpus introduces is OWNED by exactly one
    sub-objective (or a dedicated capture sub-plan) so no cross-cutting term is
    orphaned — the machine-checked form of the skill §4e.4 sweep."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    term: str = Field(min_length=1)
    owner_sub_id: str = Field(min_length=1)


class SharedCrossRef(BaseModel):
    """One shared cross-reference resolved once at corpus scope and threaded
    into every sub-plan (M2, feeds M7) — a vault note all sub-plans link."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    target: str = Field(min_length=1)
    relationship: str = ""


# ── M2 — the corpus plan ────────────────────────────────────────────────────


class CorpusPlan(BaseModel):
    """A hierarchical corpus decomposition: a master index + N sub-objectives.

    Mirrors :class:`~tessellum.composer.knowledge_plan.NoteIntentGraph` one
    level up: ``frozen=True`` + ``extra="forbid"`` + immutable tuples. Where a
    ``NoteIntentGraph`` is a flat set of note intents under one objective, a
    ``CorpusPlan`` is a set of :class:`SubObjective`s under one bundle, each of
    which will itself carry a ``NoteIntentGraph``.

    The **master index is not stored** — it is DERIVED purely from the
    sub-objectives via :meth:`master_index`, enforcing the "master plan is a
    pure index, never duplicates note tables" invariant by construction (there
    is no place to duplicate a note table).

    Attributes:
        bundle_id: The parent :class:`~tessellum.composer.knowledge_plan.SourceBundle`
            content id this plan decomposes.
        objective: The user's requested corpus-digestion outcome.
        plan_shape: The decided shape. A ``CorpusPlan`` is only well-formed for
            ``master_plus_subplans`` (the flat shapes use a plain
            ``NoteIntentGraph``); the validator enforces this.
        sub_objectives: ORDERED tuple of :class:`SubObjective` — unique
            ``sub_id``, acyclic ``depends_on``, and (with ``bundle_member_count``
            supplied) a partition witness over the bundle ordinals.
        term_ownership: The corpus-wide term-owner inventory (M6 gate input).
        shared_cross_refs: Links common to all sub-plans (M7 input).
        bundle_member_count: If > 0, the number of members in the parent bundle;
            enables the partition check (every ordinal in ``[0, count)`` owned
            by ≥1 sub-objective, none out of range). ``0`` = unknown → the
            range/coverage check is skipped (uniqueness + acyclicity still run).

    Validators (``model_validator(mode="after")``):
        - ``plan_shape == "master_plus_subplans"`` (else use a flat graph).
        - ``sub_objectives`` non-empty with unique ``sub_id``.
        - every ``depends_on`` ref resolves to a known ``sub_id`` and the
          dependency graph is acyclic (topological order exists for the wave).
        - ``term_ownership`` owners resolve to known ``sub_id``.
        - if ``bundle_member_count > 0``: ordinals stay in ``[0, count)`` and
          every member is owned by at least one sub-objective (no orphan doc).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    bundle_id: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    plan_shape: PlanShape = "master_plus_subplans"
    sub_objectives: tuple[SubObjective, ...] = Field(..., min_length=1)
    term_ownership: tuple[TermOwnerRow, ...] = ()
    shared_cross_refs: tuple[SharedCrossRef, ...] = ()
    bundle_member_count: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _check_corpus(self) -> "CorpusPlan":
        if self.plan_shape != "master_plus_subplans":
            raise ValueError(
                "CorpusPlan is only well-formed for plan_shape="
                "'master_plus_subplans'; single_plan / single_plan_phased use "
                "a flat NoteIntentGraph"
            )
        ids = [s.sub_id for s in self.sub_objectives]
        seen: set[str] = set()
        for sid in ids:
            if sid in seen:
                raise ValueError(f"duplicate sub_id in CorpusPlan: {sid!r}")
            seen.add(sid)
        id_set = set(ids)

        # dependency edges resolve + are acyclic (a wave order must exist).
        adjacency: dict[str, tuple[str, ...]] = {}
        for sub in self.sub_objectives:
            for dep in sub.depends_on:
                if dep not in id_set:
                    raise ValueError(
                        f"SubObjective {sub.sub_id!r} depends_on unknown "
                        f"sub_id {dep!r}"
                    )
            adjacency[sub.sub_id] = sub.depends_on
        _assert_acyclic(adjacency)

        # term owners resolve to a real sub-objective.
        for row in self.term_ownership:
            if row.owner_sub_id not in id_set:
                raise ValueError(
                    f"term {row.term!r} owned by unknown sub_id "
                    f"{row.owner_sub_id!r}"
                )

        # bundle partition (only when the member count is known).
        if self.bundle_member_count > 0:
            owned: set[int] = set()
            for sub in self.sub_objectives:
                for ordinal in sub.member_ordinals:
                    if ordinal >= self.bundle_member_count:
                        raise ValueError(
                            f"SubObjective {sub.sub_id!r} references ordinal "
                            f"{ordinal} outside bundle range "
                            f"[0, {self.bundle_member_count})"
                        )
                    owned.add(ordinal)
            missing = set(range(self.bundle_member_count)) - owned
            if missing:
                raise ValueError(
                    f"bundle members {sorted(missing)} owned by no "
                    f"sub-objective (orphaned source docs)"
                )
        return self

    def master_index(self) -> tuple["SubObjectiveRow", ...]:
        """Derive the master-plan index PURELY from the sub-objectives (M2).

        The master plan is an index, never a note-table duplicate: this returns
        one lightweight row per sub-objective (id / topic / note count /
        priority), in declared order. There is nowhere to store a divergent
        index, so the "pure index" invariant holds by construction.
        """
        return tuple(
            SubObjectiveRow(
                sub_id=s.sub_id,
                topic=s.topic,
                est_note_count=s.est_note_count,
                priority=s.priority,
            )
            for s in self.sub_objectives
        )

    def wave_order(self) -> tuple[str, ...]:
        """A deterministic wave order over the sub-objectives (M5 preview).

        Priority-major (``P1`` → ``P2`` → ``P3``), then dependency-respecting
        (a sub-objective never precedes one it ``depends_on``), ties broken by
        ``sub_id`` for determinism. Pure — reads only the frozen model. The
        acyclicity validator guarantees this order exists.
        """
        rank = {"P1": 0, "P2": 1, "P3": 2}
        by_id = {s.sub_id: s for s in self.sub_objectives}
        remaining = set(by_id)
        order: list[str] = []
        while remaining:
            ready = [
                sid
                for sid in remaining
                if all(dep not in remaining for dep in by_id[sid].depends_on)
            ]
            # Ready set is non-empty (acyclic); pick priority-major, id-minor.
            ready.sort(key=lambda sid: (rank[by_id[sid].priority], sid))
            chosen = ready[0]
            order.append(chosen)
            remaining.discard(chosen)
        return tuple(order)


class SubObjectiveRow(BaseModel):
    """One derived master-index row (see :meth:`CorpusPlan.master_index`).
    Pure projection — not independently constructed by callers."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    sub_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    est_note_count: int = Field(ge=0)
    priority: SubObjectivePriority


# ── content id (reuses P0 canonical hashing — no reinvention) ───────────────


def corpus_plan_content_id(plan: CorpusPlan) -> str:
    """Stable content id for a :class:`CorpusPlan` — pure, no clock/random/IO.

    ``sha256`` over :func:`proposals.canonical_json_bytes` of the plan's
    JSON-mode dump (float-ban + NFC-normalized + sorted keys), so the id is
    order- and process-stable. Reuses the P0 canonicalizer rather than
    reinventing hashing, exactly like
    :func:`tessellum.composer.knowledge_plan.note_intent_content_id`.
    """
    return hashlib.sha256(
        canonical_json_bytes(plan.model_dump(mode="json"))
    ).hexdigest()


# ── internal: acyclicity check ──────────────────────────────────────────────


def _assert_acyclic(adjacency: dict[str, tuple[str, ...]]) -> None:
    """Raise ``ValueError`` if the ``depends_on`` graph has a cycle.

    Peels nodes whose dependencies are all already peeled (a source-removal
    topological pass); if a round finds no peelable node while some remain,
    the residual set is a cycle.
    """
    remaining = set(adjacency)
    while remaining:
        ready = [n for n in remaining if all(d not in remaining for d in adjacency[n])]
        if not ready:
            raise ValueError(
                f"cyclic depends_on among sub-objectives: {sorted(remaining)!r}"
            )
        for n in ready:
            remaining.discard(n)


__all__ = [
    # M1
    "PlanShape",
    "SINGLE_PLAN_MAX_WORDS",
    "PHASED_MAX_WORDS",
    "SINGLE_PLAN_MAX_NOTES",
    "PHASED_MAX_NOTES",
    "classify_plan_shape",
    # M2
    "SubObjectivePriority",
    "SubObjective",
    "TermOwnerRow",
    "SharedCrossRef",
    "CorpusPlan",
    "SubObjectiveRow",
    "corpus_plan_content_id",
]
