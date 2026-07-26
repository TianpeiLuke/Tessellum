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
import json
from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tessellum.composer.knowledge_plan import SourceBundle
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

    def dependency_layers(self) -> tuple[tuple[str, ...], ...]:
        """Partition the sub-objectives into ordered dependency LAYERS (M5).

        Layer ``i`` contains exactly the sub-objectives all of whose
        ``depends_on`` are in layers ``0..i-1`` and that are not yet placed.
        Consequences, both load-bearing for M5:

        - **Cross-layer ordering is a hard barrier**: a sub-objective NEVER
          appears before one it depends on, so a dependent sub-plan's execute
          transaction runs strictly after its dependency's has committed (M4
          executes layer by layer). This is what lets a P2 sub-plan's
          cross-links resolve against a P1 sub-plan's already-published notes.
        - **Within a layer the sub-objectives are mutually independent** (no
          ``depends_on`` among them), so they MAY run concurrently — the
          precondition for the opt-in concurrent wave. Disjoint write-closures
          are the caller's separate guarantee; independence here is only the
          dependency-graph precondition.

        Within each layer, ids are sorted priority-major (``P1`` → ``P3``) then
        by ``sub_id`` for determinism. Flattening the layers reproduces a valid
        (though not necessarily identical) topological order; the strict
        priority-major single-stream order is :meth:`wave_order`. Pure; the
        acyclicity validator guarantees termination.
        """
        rank = {"P1": 0, "P2": 1, "P3": 2}
        by_id = {s.sub_id: s for s in self.sub_objectives}
        placed: set[str] = set()
        layers: list[tuple[str, ...]] = []
        while len(placed) < len(by_id):
            layer = [
                sid
                for sid in by_id
                if sid not in placed
                and all(dep in placed for dep in by_id[sid].depends_on)
            ]
            if not layer:
                # An acyclic graph always adds ≥1 per round; an empty layer with
                # nodes remaining means a cycle. The CorpusPlan validator makes
                # this unreachable, but fail LOUD (mirroring wave_order's
                # _assert_acyclic) rather than spin forever if ever called on an
                # unvalidated graph.
                raise ValueError(
                    f"cyclic depends_on among sub-objectives: "
                    f"{sorted(set(by_id) - placed)!r}"
                )
            # Acyclic → each round adds ≥1; sort for a deterministic layer.
            layer.sort(key=lambda sid: (rank[by_id[sid].priority], sid))
            layers.append(tuple(layer))
            placed.update(layer)
        return tuple(layers)


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


# ── M6 — corpus-wide term-ownership gate ────────────────────────────────────


@dataclass(frozen=True)
class TermOwnershipResult:
    """The verdict of :func:`term_ownership_gate` (M6).

    Attributes:
        passed: ``True`` iff every introduced term has exactly one owner and no
            ownership row is malformed (unknown owner / unintroduced term).
        unowned: introduced terms with NO owner row (would ship a ghost ref).
        multiply_owned: ``{term -> owner sub_ids}`` for terms owned more than
            once (ambiguous ownership).
        unknown_owner: ``{term -> owner sub_id}`` rows whose owner is not a
            sub-objective of the plan.
        orphan_ownership: owner rows for terms NOT in ``introduced_terms``
            (ownership of a term the corpus does not introduce — a stale row).
    """

    passed: bool
    unowned: tuple[str, ...] = ()
    multiply_owned: dict[str, tuple[str, ...]] = field(default_factory=dict)
    unknown_owner: dict[str, str] = field(default_factory=dict)
    orphan_ownership: tuple[str, ...] = ()

    def reason(self) -> str:
        """A short one-line cause when ``not passed`` (empty when passed)."""
        parts: list[str] = []
        if self.unowned:
            parts.append(f"unowned={sorted(self.unowned)}")
        if self.multiply_owned:
            parts.append(f"multiply_owned={sorted(self.multiply_owned)}")
        if self.unknown_owner:
            parts.append(f"unknown_owner={sorted(self.unknown_owner)}")
        if self.orphan_ownership:
            parts.append(f"orphan_ownership={sorted(self.orphan_ownership)}")
        return "; ".join(parts)


def term_ownership_gate(
    plan: "CorpusPlan", introduced_terms: tuple[str, ...] | set[str]
) -> TermOwnershipResult:
    """Assert every undigested term the corpus introduces has EXACTLY ONE owner
    sub-objective (M6) — the machine-checked form of the plan skill's §4e.4
    corpus-wide term-ownership sweep. Pure; no IO.

    ``introduced_terms`` is the corpus-wide set of undigested terms the sweep
    surfaced (the caller supplies it — the plan does not itself enumerate the
    source's terms). The gate fails closed on:

    - an introduced term with NO owner row → would ship a ghost reference
      (the exact failure §4e.4 exists to prevent);
    - a term owned by more than one sub-objective → ambiguous ownership;
    - an ownership row whose owner is not a sub-objective of ``plan``;
    - an ownership row for a term NOT in ``introduced_terms`` (a stale/orphan
      row) — surfaced so the inventory stays honest.

    Note the ``CorpusPlan`` validator already rejects an unknown-owner row at
    construction, so ``unknown_owner`` is normally empty here; the gate re-checks
    it defensively (it may run on a ``model_construct``-bypassed plan) and to
    make the corpus-scope contract self-contained.
    """
    introduced = set(introduced_terms)
    sub_ids = {s.sub_id for s in plan.sub_objectives}
    # DISTINCT owners per term (first-seen order): duplicate identical rows
    # (term_a→s1 twice) are NOT ambiguous ownership, so dedup before counting —
    # counting rows would false-flag a single-owner term as multiply_owned.
    owners: dict[str, list[str]] = {}
    for row in plan.term_ownership:
        bucket = owners.setdefault(row.term, [])
        if row.owner_sub_id not in bucket:
            bucket.append(row.owner_sub_id)

    unowned = tuple(sorted(t for t in introduced if t not in owners))
    multiply_owned = {
        term: tuple(sorted(o)) for term, o in owners.items() if len(o) > 1
    }
    # unknown-owner is reported INDEPENDENT of ownership cardinality (a term
    # with several owners that are ALL unknown sub_ids still surfaces here, not
    # only in multiply_owned) so one gate pass reports every defect on a term.
    unknown_owner = {
        term: sorted(oi for oi in o if oi not in sub_ids)[0]
        for term, o in owners.items()
        if any(oi not in sub_ids for oi in o)
    }
    orphan_ownership = tuple(sorted(t for t in owners if t not in introduced))
    passed = not (unowned or multiply_owned or unknown_owner or orphan_ownership)
    return TermOwnershipResult(
        passed=passed,
        unowned=unowned,
        multiply_owned=multiply_owned,
        unknown_owner=unknown_owner,
        orphan_ownership=orphan_ownership,
    )


# ── M0 — bundle → joint-planner leaf (the fan-in) ───────────────────────────

# Aggregate ceiling for the RENDERED corpus ``members`` block (the JSON the
# executor substitutes for ``{{leaf.members}}``). Well under the composer's
# HARD_PROMPT_CAP_CHARS (150_000) so the members block plus the rest of the
# prompt (skill prose + upstream) fits with headroom. A ContextAssembler still
# bounds the final rendered prompt; this is the pre-budget the builder targets.
DEFAULT_CORPUS_LEAF_MAX_CHARS = 60_000


def _render_members(members: list[dict]) -> str:
    """Render the ``members`` list exactly as the executor's ``_stringify``
    does when substituting ``{{leaf.members}}`` — ``json.dumps(indent=2,
    ensure_ascii=False)`` — so the builder can BUDGET the rendered size, not
    just the excerpt bodies. Kept in lockstep with
    ``tessellum.composer.executor._stringify``."""
    return json.dumps(members, indent=2, ensure_ascii=False)


def _fit_excerpt(
    skeleton: "MemberExcerpt", content: str, rendered_target: int
) -> tuple[str, bool]:
    """Window ``content`` so the member's RENDERED JSON size stays within
    ``rendered_target`` chars — accounting for JSON string escaping (a newline
    renders as ``\\n`` = 2 chars, so a raw-char budget under-counts) and the
    member's own scaffolding (keys / quoting / indentation / the 64-char hash).

    Binary-searches the RAW excerpt budget passed to :func:`_window_excerpt`
    for the largest window whose single-element-array render fits the target.
    ``_window_excerpt`` is monotonic non-decreasing in its budget, so the
    render size is too — the search is well-defined. Pure. Measuring each
    member against ``rendered_target`` (which already includes that member's
    2-char array brackets) means the aggregate stays under ``max_chars`` with
    headroom, since the outer brackets are counted once but reserved per-member.
    """

    def rendered(raw_budget: int) -> tuple[int, str, bool]:
        exc, trunc = _window_excerpt(content, raw_budget)
        member = skeleton.model_copy(
            update={"excerpt": exc, "truncated": trunc}
        ).model_dump(mode="json")
        return len(_render_members([member])), exc, trunc

    # Fast path: the full content already fits.
    full_size, exc, trunc = rendered(len(content))
    if full_size <= rendered_target:
        return exc, trunc
    # Binary-search the largest raw budget whose rendered member fits.
    lo, hi = 0, len(content)
    best: tuple[str, bool] = ("", bool(content))
    while lo <= hi:
        mid = (lo + hi) // 2
        size, exc, trunc = rendered(mid)
        if size <= rendered_target:
            best = (exc, trunc)
            lo = mid + 1
        else:
            hi = mid - 1
    return best


class MemberExcerpt(BaseModel):
    """One bundle member's bounded excerpt for the joint planning prompt (M0).

    Carries the member's identity + a HEAD/TAIL windowed excerpt of its parsed
    content (not the whole document — bounded, per the counter's "bounded
    excerpts, not whole-content injection"). ``truncated`` records whether the
    excerpt dropped a middle span."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    ordinal: int = Field(ge=0)
    source_id: str = Field(min_length=1)
    ref: str = Field(min_length=1)
    extracted_text_hash: str = Field(min_length=1)
    excerpt: str = ""
    full_char_count: int = Field(ge=0)
    truncated: bool = False


def _window_excerpt(content: str, budget: int) -> tuple[str, bool]:
    """Bound ``content`` to ``budget`` chars, HEAD + TAIL with an elision
    marker in the middle (a doc's intro + conclusion carry the most planning
    signal). Returns ``(excerpt, truncated)``. Pure."""
    if budget <= 0:
        return "", bool(content)
    if len(content) <= budget:
        return content, False
    marker = "\n\n[… excerpt elided …]\n\n"
    if budget <= len(marker):
        return content[:budget], True
    room = budget - len(marker)
    head = room - room // 2
    tail = room // 2
    return content[:head] + marker + (content[-tail:] if tail else ""), True


def build_corpus_leaf(
    bundle: SourceBundle,
    member_contents: dict[int, str],
    *,
    max_chars: int = DEFAULT_CORPUS_LEAF_MAX_CHARS,
) -> dict:
    """Build ONE joint-planning leaf from a multi-member bundle (M0) — pure.

    This is the fan-in the shipped single-doc path lacks: instead of admitting
    each member as an independent per-file job the supervisor runs one at a
    time, the whole ordered bundle is delivered to ONE planning episode so
    decomposition, cross-document dedup, and cross-document links are coherent.

    ``member_contents`` maps a member ``ordinal`` to its parsed text (the
    runtime reads the spools; this function does NO IO). ``max_chars`` budgets
    the RENDERED ``members`` JSON block (what the executor substitutes for
    ``{{leaf.members}}``), NOT just the excerpt bodies: the budget is split
    evenly across members and each member's own JSON scaffolding (keys,
    quoting, indentation, ``ref``/``extracted_text_hash``) is subtracted before
    its excerpt is windowed, so the aggregate rendered block stays ≤
    ``max_chars`` for any member count and any ref length. Each member's content
    is HEAD/TAIL windowed via :func:`_window_excerpt`.

    Degenerate case: when there are more members than ``max_chars``, the
    per-member budget floors at the scaffolding-only size (empty excerpts) —
    the rendered block is then bounded by the scaffolding, not the content, and
    a final assertion still guarantees ≤ ``max_chars`` is not silently
    exceeded (it raises rather than emitting an over-cap leaf). The downstream
    ``ContextAssembler`` remains a second bound on the FULL prompt; this keeps
    the leaf itself bounded so it never relies on that fail-soft.

    The leaf carries the multi-doc payload the plan skill's prompt references as
    ``{{leaf.members}}`` (rendered as indented JSON by the executor's
    ``_stringify``), plus corpus identity keys. Every member ordinal in the
    bundle MUST have content (a missing ordinal is a caller bug — fail loud);
    extra ordinals in ``member_contents`` are ignored.

    Returns a plain dict (not a pydantic model) so it drops straight into the
    ``source_leaf`` slot of ``run_digestion_pipeline`` / a corpus executor.
    """
    ordinals = [m.ordinal for m in bundle.members]
    missing = [o for o in ordinals if o not in member_contents]
    if missing:
        raise ValueError(
            f"bundle {bundle.bundle_id!r} missing content for member ordinals "
            f"{missing}"
        )
    # Split the RENDERED budget evenly across members, then size each member's
    # excerpt so its OWN rendered JSON (scaffolding + escaped excerpt) fits its
    # share — so the aggregate rendered block stays ≤ max_chars regardless of
    # member count, ref length, or newline density (the high-severity review
    # finding: body-only budgeting overflowed because JSON escaping + scaffolding
    # are uncounted). Each member's share already reserves its 2-char array
    # brackets, so summing shares over-reserves the single outer pair — headroom.
    per_member_rendered = max(1, max_chars // max(1, len(bundle.members)))
    excerpts: list[dict] = []
    for member in bundle.members:  # bundle.members is ascending-ordinal canonical
        content = member_contents[member.ordinal]
        skeleton = MemberExcerpt(
            ordinal=member.ordinal,
            source_id=member.source_id,
            ref=member.ref,
            extracted_text_hash=member.extracted_text_hash,
            excerpt="",
            full_char_count=len(content),
            truncated=False,
        )
        excerpt, truncated = _fit_excerpt(skeleton, content, per_member_rendered)
        excerpts.append(
            skeleton.model_copy(
                update={"excerpt": excerpt, "truncated": truncated}
            ).model_dump(mode="json")
        )
    # Defensive: fail loud if the rendered block still exceeds the budget rather
    # than emitting an over-cap leaf that trips the hard prompt cap downstream.
    # This fires only in the degenerate regime where even empty-excerpt member
    # scaffolding cannot fit max_chars (member_count too high for the budget).
    rendered = _render_members(excerpts)
    if len(rendered) > max_chars:
        raise ValueError(
            f"bundle {bundle.bundle_id!r} rendered members block "
            f"({len(rendered)} chars) exceeds max_chars ({max_chars}); "
            f"member scaffolding for {len(bundle.members)} members alone "
            f"exceeds the budget — raise max_chars or reduce the bundle"
        )
    return {
        "_id": bundle.bundle_id,
        "bundle_id": bundle.bundle_id,
        "objective": bundle.objective,
        "source_name": bundle.objective,
        "member_count": len(bundle.members),
        "members": excerpts,
    }


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
    # M6 — term-ownership gate
    "TermOwnershipResult",
    "term_ownership_gate",
    # M0 — fan-in leaf
    "DEFAULT_CORPUS_LEAF_MAX_CHARS",
    "MemberExcerpt",
    "build_corpus_leaf",
]
