"""Corpus digestion driver — plan a corpus into N accepted sub-plans (M3).

Phase **M3** of the multi-document corpus-digestion plan (FZ 20k9c1a1a1b7b1).
This is the corpus-level orchestrator that sits ABOVE the single-plan
:func:`tessellum.composer.digestion.run_digestion_pipeline`: given a decided
:class:`~tessellum.composer.corpus_plan.CorpusPlan` (the master + N
sub-objectives from M1/M2) and the parent bundle's member content, it runs the
shipped plan→augment→review linear phases over EACH sub-objective's slice of
the bundle — reusing ``run_digestion_pipeline(stop_after="review")`` one level
down — and collects one ACCEPTED plan per sub-objective.

Boundary doctrine (mirrors :mod:`tessellum.composer.digestion`): this driver
holds only the corpus control flow (iterate sub-objectives, build each slice
leaf, capture accepted-or-blocked); the single-plan pipeline does the plan /
augment / review / sign-off work; the shipped per-note transaction substrate is
reused unchanged one level down. A rejected or errored sub-plan is marked
``blocked`` and does NOT stop the other sub-objectives (a3a's partition policy:
a weak sub-plan blocks only itself). M4 will execute the accepted plans as
separate snapshot-pinned transactions; M5 orders the wave by priority.

This module imports only composer siblings (corpus_plan, digestion,
knowledge_plan, llm, credential_pool, context_assembler, scheduler) — no
runtime — keeping the composer import DAG acyclic.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ContextManager

from tessellum.composer.context_assembler import ContextAssembler
from tessellum.composer.corpus_plan import (
    CorpusPlan,
    SharedCrossRef,
    SharedCrossRefResolution,
    SubObjective,
    TermOwnershipResult,
    build_corpus_leaf,
    resolve_shared_cross_refs,
    term_ownership_gate,
)
from tessellum.composer.credential_pool import RunBudget
from tessellum.composer.digestion import (
    DigestionResult,
    run_digestion_pipeline,
    run_execute_wave,
)
from tessellum.composer.knowledge_plan import (
    BundleMember,
    NoteIntentGraph,
    SourceBundle,
)
from tessellum.composer.llm import LLMBackend
from tessellum.composer.manifest import Manifest
from tessellum.composer.scheduler import RunResult
from tessellum.composer.write_closure import write_closure
from tessellum.composer.signoff import (
    HumanPrompt,
    SignOffPolicy,
    SignOffResult,
)


@dataclass(frozen=True)
class SubPlanOutcome:
    """One sub-objective's result within the corpus planning wave (M3).

    Attributes:
        sub_id: The sub-objective's id.
        priority: Its wave-ordering rung (carried through for M5).
        accepted: ``True`` iff the plan passed review→ready sign-off; ``False``
            marks it ``blocked`` (sign-off rejection or a linear-phase error).
        status: ``"accepted"`` | ``"blocked"``.
        plan_doc: The accepted plan artifact (the sub-plan M4 will execute), or
            the partial plan_doc when blocked.
        result: The underlying :class:`DigestionResult`, or ``None`` when the
            sub-objective was blocked BEFORE the pipeline produced a result —
            i.e. slice/leaf construction or the planning pipeline raised (the
            ``except`` path sets ``result=None``, ``plan_doc={}``).
        reason: A short human-readable cause when ``blocked``.
    """

    sub_id: str
    priority: str
    accepted: bool
    status: str
    plan_doc: dict[str, Any] = field(default_factory=dict)
    result: DigestionResult | None = None
    reason: str | None = None


@dataclass(frozen=True)
class CorpusPlanningResult:
    """The end-to-end outcome of :func:`run_corpus_planning_wave` (M3).

    Attributes:
        bundle_id: The parent bundle's content id.
        objective: The corpus objective.
        sub_plans: Per-sub-objective outcomes, in the corpus plan's declared
            order (M5 will re-order the EXECUTE wave by priority; planning order
            is independent).
        all_accepted: ``True`` iff every sub-objective produced an accepted plan.
        accepted_count / blocked_count: Convenience tallies.
    """

    bundle_id: str
    objective: str
    sub_plans: tuple[SubPlanOutcome, ...]
    all_accepted: bool
    accepted_count: int
    blocked_count: int


def _slice_bundle(bundle: SourceBundle, sub: SubObjective) -> SourceBundle:
    """Build the sub-bundle a sub-objective owns — the parent members at its
    ``member_ordinals``, re-based to contiguous ordinals ``0..k-1`` so
    :func:`build_corpus_leaf`'s even-split budget is computed over just the
    slice. ``bundle.members`` is ascending-ordinal canonical, so selecting by
    ordinal preserves order. Pure."""
    by_ordinal = {m.ordinal: m for m in bundle.members}
    missing = [o for o in sub.member_ordinals if o not in by_ordinal]
    if missing:
        raise ValueError(
            f"sub-objective {sub.sub_id!r} references parent member ordinals "
            f"{missing} absent from bundle {bundle.bundle_id!r}"
        )
    selected: list[BundleMember] = []
    for new_ordinal, original in enumerate(sub.member_ordinals):
        src = by_ordinal[original]
        selected.append(
            BundleMember(
                source_id=src.source_id,
                ordinal=new_ordinal,
                ref=src.ref,
                parser_id=src.parser_id,
                extracted_text_hash=src.extracted_text_hash,
                provenance=src.provenance,
            )
        )
    return SourceBundle(
        bundle_id=f"{bundle.bundle_id}:{sub.sub_id}",
        objective=sub.topic,
        members=tuple(selected),
    )


def _slice_contents(
    bundle: SourceBundle, sub: SubObjective, member_contents: dict[int, str]
) -> dict[int, str]:
    """Map the sub-bundle's re-based ordinals ``0..k-1`` back to the parent
    member contents (keyed by the PARENT ordinal). Fails loud on a missing
    parent ordinal (a caller bug — the CorpusPlan partition validator should
    have caught it, but M3 does not trust that)."""
    missing = [o for o in sub.member_ordinals if o not in member_contents]
    if missing:
        raise ValueError(
            f"sub-objective {sub.sub_id!r} references parent member ordinals "
            f"{missing} with no content"
        )
    return {new: member_contents[orig] for new, orig in enumerate(sub.member_ordinals)}


def _thread_shared_cross_refs(
    leaf: dict, shared: tuple[SharedCrossRef, ...]
) -> dict:
    """Attach the corpus-level shared cross-references to a sub-plan's planning
    leaf (M7 resolves these once at corpus scope; M3 threads whatever is on the
    plan so the sub-planner can link them). Additive: the plan skill may read
    ``{{leaf.shared_cross_refs}}``; absent → the default sentinel-free path (the
    key is always present, possibly an empty list)."""
    leaf = dict(leaf)
    leaf["shared_cross_refs"] = [
        {"target": x.target, "relationship": x.relationship} for x in shared
    ]
    return leaf


def run_corpus_planning_wave(
    corpus_plan: CorpusPlan,
    bundle: SourceBundle,
    member_contents: dict[int, str],
    *,
    skills_dir: Path | str,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    budget: RunBudget | None = None,
    context_assembler: ContextAssembler | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    shared_cross_refs: tuple[SharedCrossRef, ...] | None = None,
) -> CorpusPlanningResult:
    """Plan every sub-objective of a corpus into an accepted sub-plan (M3).

    For each :class:`~tessellum.composer.corpus_plan.SubObjective`, builds a
    planning leaf from its slice of ``bundle`` (via
    :func:`~tessellum.composer.corpus_plan.build_corpus_leaf` over the
    re-based sub-bundle), threads the corpus's shared cross-references, and runs
    ``run_digestion_pipeline(stop_after="review")`` — the shipped plan→augment→
    review→sign-off path, reused one level down, WITHOUT executing. The accepted
    ``plan_doc`` is captured for M4 to execute as its own transaction.

    Sub-objectives are planned independently: a rejected sign-off or a
    linear-phase error marks that sub-objective ``blocked`` and the wave
    continues (a weak sub-plan blocks only itself, per the a3a partition
    policy). Planning is done in the corpus plan's declared order; the EXECUTE
    wave's priority ordering is M5.

    Args:
        corpus_plan: The decided master + sub-objectives (M1/M2).
        bundle: The parent :class:`SourceBundle` the plan decomposes.
        member_contents: Parent-ordinal → parsed member text (no IO here).
        skills_dir / backend / vault_root / dry_run / budget /
        context_assembler / cancellation_check / effect_guard: Threaded into
            each sub-objective's ``run_digestion_pipeline`` call.

    Returns:
        A :class:`CorpusPlanningResult` with one :class:`SubPlanOutcome` per
        sub-objective (declared order).
    """
    if corpus_plan.bundle_id != bundle.bundle_id:
        raise ValueError(
            f"corpus_plan.bundle_id {corpus_plan.bundle_id!r} does not match "
            f"bundle.bundle_id {bundle.bundle_id!r}"
        )
    # M7: use the corpus-resolved shared cross-refs when the driver supplies
    # them (deduped + existence-filtered once at corpus scope); else fall back
    # to the plan's raw set (unresolved) so this wave stays usable standalone.
    threaded_refs = (
        corpus_plan.shared_cross_refs if shared_cross_refs is None
        else shared_cross_refs
    )
    outcomes: list[SubPlanOutcome] = []
    for sub in corpus_plan.sub_objectives:
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError(
                f"corpus planning cancelled before sub-objective {sub.sub_id!r}"
            )
        # Slice/leaf construction is INSIDE the try so a slice-time failure of
        # ONE sub-objective (e.g. an over-budget bundle that build_corpus_leaf
        # rejects, or an out-of-bundle ordinal) blocks only that sub-objective —
        # the "a weak sub-plan blocks only itself" invariant. Without this, a
        # single bad sub-objective would raise and sink the whole corpus wave.
        try:
            sub_bundle = _slice_bundle(bundle, sub)
            sub_contents = _slice_contents(bundle, sub, member_contents)
            leaf = build_corpus_leaf(sub_bundle, sub_contents)
            leaf = _thread_shared_cross_refs(leaf, threaded_refs)
            # sub_id / priority / objective travel on the leaf so the sub-planner
            # (and downstream M4) can attribute the accepted plan to its owner.
            leaf["sub_id"] = sub.sub_id
            leaf["priority"] = sub.priority
            leaf["corpus_objective"] = corpus_plan.objective
            result = run_digestion_pipeline(
                skills_dir=skills_dir,
                source_leaf=leaf,
                backend=backend,
                vault_root=vault_root,
                dry_run=dry_run,
                budget=budget,
                context_assembler=context_assembler,
                cancellation_check=cancellation_check,
                effect_guard=effect_guard,
                stop_after="review",
            )
        except InterruptedError:
            raise
        except Exception as exc:  # a sub-plan failure must not sink the corpus
            outcomes.append(
                SubPlanOutcome(
                    sub_id=sub.sub_id, priority=sub.priority, accepted=False,
                    status="blocked", plan_doc={}, result=None,
                    reason=f"planning raised: {type(exc).__name__}: {exc}"[:200],
                )
            )
            continue
        accepted = result.completed and result.stopped_at == "review_accepted"
        outcomes.append(
            SubPlanOutcome(
                sub_id=sub.sub_id,
                priority=sub.priority,
                accepted=accepted,
                status="accepted" if accepted else "blocked",
                plan_doc=result.plan_doc,
                result=result,
                reason=None if accepted else _blocked_reason(result),
            )
        )
    accepted_count = sum(1 for o in outcomes if o.accepted)
    blocked_count = len(outcomes) - accepted_count
    return CorpusPlanningResult(
        bundle_id=bundle.bundle_id,
        objective=corpus_plan.objective,
        sub_plans=tuple(outcomes),
        all_accepted=blocked_count == 0,
        accepted_count=accepted_count,
        blocked_count=blocked_count,
    )


def _blocked_reason(result: DigestionResult) -> str:
    """A short cause for a non-accepted sub-plan (sign-off rejection or a
    linear-phase error), read from the underlying result."""
    if result.sign_off is not None and result.sign_off.decision != "approved":
        return f"sign-off {result.sign_off.decision}"
    if result.stopped_at:
        return f"phase error at {result.stopped_at}"
    return "not accepted"


# run/transaction-scoped execute kwargs that MUST be per-sub-plan-unique so N
# sibling execute waves don't collide (shared manifest → colliding index-leaf
# keys corrupt a sibling's committed record; shared run_id defeats owner-
# fencing; a shared events_path/stats_path is write_text-overwritten by the
# next sub-plan). Uniquified by sub_id in :func:`_isolate_execute_kwargs`.
_RUN_SCOPED_EXECUTE_KWARGS: tuple[str, ...] = (
    "manifest", "run_id", "events_path", "stats_path",
)


def _isolate_execute_kwargs(execute_kwargs: dict[str, Any], sub_id: str) -> dict[str, Any]:
    """Per-sub-plan-clone the run/transaction-scoped execute kwargs (M4/M5).

    Each accepted sub-plan is its OWN transaction, so run-scoped resources are
    made sub-plan-unique rather than forwarded verbatim (which would collide
    across sibling waves — and, under M5 concurrency, race):

    - ``run_id`` → ``f"{run_id}:{sub_id}"`` so owner-fencing / reclaim isolates
      each sub-plan;
    - ``events_path`` / ``stats_path`` → the ``sub_id`` inserted into the
      filename stem so one sub-plan's sidecar never overwrites another's;
    - ``manifest`` → each sub-plan gets its OWN :class:`Manifest`. A path-ful
      manifest is cloned to a ``sub_id``-suffixed path; a PATH-LESS (in-memory)
      manifest gets a fresh empty ``Manifest()`` too — NOT left shared. A shared
      in-memory manifest is unsafe on two counts the "nothing to collide"
      intuition misses: its ``entries`` dict has no internal lock (each
      ``run_pipeline_dynamic`` makes its OWN scheduler lock, so sibling waves
      don't mutually exclude — torn read-modify-write), and sibling sub-plans
      compile the SAME execute skill so their index-derived ``leaf_i`` claim
      keys (e.g. ``capture::leaf_0``) COLLIDE, silently refusing one sibling's
      leaf. A fresh per-sub-plan manifest costs nothing (a path-less manifest
      never persists / resumes) and removes both hazards.

    Returns a shallow copy with those keys rewritten; every other kwarg passes
    through unchanged. Pure w.r.t. the input dict (never mutates it).
    """
    if not any(k in execute_kwargs for k in _RUN_SCOPED_EXECUTE_KWARGS):
        return execute_kwargs
    out = dict(execute_kwargs)
    if out.get("run_id") is not None:
        out["run_id"] = f"{out['run_id']}:{sub_id}"
    for key in ("events_path", "stats_path"):
        p = out.get(key)
        if p is not None:
            p = Path(p)
            out[key] = p.with_name(f"{p.stem}.{sub_id}{p.suffix}")
    manifest = out.get("manifest")
    if manifest is not None:
        mpath = getattr(manifest, "path", None)
        if mpath is not None:
            mpath = Path(mpath)
            sub_path = mpath.with_name(f"{mpath.stem}.{sub_id}{mpath.suffix}")
            out["manifest"] = (
                Manifest.load(sub_path) if sub_path.exists()
                else Manifest(path=sub_path)
            )
        else:
            # Path-less in-memory manifest STILL must be per-sub-plan: a shared
            # entries dict has no lock and sibling execute skills mint identical
            # leaf_i claim keys. A fresh manifest never persists, so this is free.
            out["manifest"] = Manifest()
    return out


def _sub_plan_touched_notes(outcome: "SubPlanOutcome") -> frozenset[str] | None:
    """The vault notes a sub-plan's accepted plan WOULD write, from its typed
    ``note_intent_graph`` via the shipped exact ``write_closure`` (M5 gate).

    Returns ``None`` when the accepted plan carries no typed graph (the prose
    fallback path) — write targets can't be computed exactly there, so the
    disjointness gate abstains rather than guess. Pure."""
    graph_spec = outcome.plan_doc.get("note_intent_graph")
    if graph_spec is None:
        return None
    graph = (
        graph_spec
        if isinstance(graph_spec, NoteIntentGraph)
        else NoteIntentGraph.model_validate(graph_spec)
    )
    return write_closure(graph).touched_note_ids


def _write_closure_overlaps(
    outcomes: list["SubPlanOutcome"],
) -> dict[str, frozenset[str]]:
    """Detect pairwise write-closure OVERLAP among a set of sub-plans (M5 gate).

    Returns ``{sub_id -> shared_note_ids}`` for every sub-plan that shares at
    least one written note with another in the set. A sub-plan whose typed
    write-closure is unavailable (prose fallback) is skipped (cannot prove a
    conflict, so it is not blocked here). Pure — reads only the frozen plans.
    """
    touched: dict[str, frozenset[str]] = {}
    for o in outcomes:
        t = _sub_plan_touched_notes(o)
        if t is not None:
            touched[o.sub_id] = t
    conflicts: dict[str, set[str]] = {}
    ids = list(touched)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            shared = touched[a] & touched[b]
            if shared:
                conflicts.setdefault(a, set()).update(shared)
                conflicts.setdefault(b, set()).update(shared)
    return {sid: frozenset(s) for sid, s in conflicts.items()}


# ── M4 — corpus execute wave (per-sub-plan transactions) ────────────────────


@dataclass(frozen=True)
class SubPlanExecution:
    """One accepted sub-plan's EXECUTE outcome within the corpus wave (M4).

    Attributes:
        sub_id: The sub-objective's id.
        priority: Its wave rung.
        promoted: ``True`` iff the sub-plan's execute wave completed clean
            (``error_count == 0``); ``False`` marks it ``blocked``.
        status: ``"promoted"`` | ``"blocked"``.
        run: The execute :class:`RunResult` (``None`` if execution raised
            before producing one).
        reason: A short cause when ``blocked``.
    """

    sub_id: str
    priority: str
    promoted: bool
    status: str
    run: RunResult | None = None
    reason: str | None = None


@dataclass(frozen=True)
class CorpusDigestionResult:
    """The end-to-end outcome of :func:`run_corpus_digestion` (M4).

    Attributes:
        bundle_id / objective: Corpus identity.
        planning: The M3 :class:`CorpusPlanningResult` (which sub-objectives
            produced an accepted plan).
        corpus_sign_off: The whole-corpus-plan sign-off (``None`` when the
            corpus gate was not run — e.g. every sub-plan blocked at planning,
            or the default headless policy approved without a human rung).
        executions: Per-accepted-sub-plan EXECUTE outcomes. Order: any
            write-closure-overlap-blocked sub-plans first (in accepted order),
            then the executed sub-plans in dependency-LAYER order (priority-major
            within each layer). This is NOT the strict single-stream priority
            order of ``CorpusPlan.wave_order`` — a dependency-independent P3
            sub-plan runs in an earlier layer than a P1 sub-plan that depends on
            it. Read ``bundle_status`` / per-outcome ``promoted``, not position.
        term_ownership: The M6 corpus-wide term-ownership gate verdict (``None``
            when no ``introduced_terms`` were supplied → the gate did not run).
            A failed gate blocks the whole corpus (``bundle_status="blocked"``,
            nothing promoted).
        bundle_status: ``"complete"`` (every sub-objective promoted) |
            ``"partially_promoted"`` (some promoted, some blocked) |
            ``"blocked"`` (none promoted) — the a3a bundle-completion rollup.
    """

    bundle_id: str
    objective: str
    planning: "CorpusPlanningResult"
    corpus_sign_off: SignOffResult | None
    executions: tuple[SubPlanExecution, ...]
    bundle_status: str
    term_ownership: "TermOwnershipResult | None" = None
    shared_cross_refs: "SharedCrossRefResolution | None" = None


def run_corpus_digestion(
    corpus_plan: CorpusPlan,
    bundle: SourceBundle,
    member_contents: dict[int, str],
    *,
    skills_dir: Path | str,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    budget: RunBudget | None = None,
    context_assembler: ContextAssembler | None = None,
    related_notes_db: Path | str | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
    corpus_sign_off_policy: SignOffPolicy | None = None,
    human_prompt: HumanPrompt | None = None,
    introduced_terms: tuple[str, ...] | set[str] | None = None,
    shared_cross_ref_exists: Callable[[str], bool] | None = None,
    execute_max_workers: int = 4,
    max_sub_plan_workers: int = 1,
    **execute_kwargs: Any,
) -> CorpusDigestionResult:
    """Digest a whole corpus: plan every sub-objective (M3), then EXECUTE each
    accepted sub-plan as its OWN transaction (M4) — the human-supervised
    milestone.

    Sequence:

    1. **Plan** — :func:`run_corpus_planning_wave` produces one accepted (or
       blocked) plan per sub-objective (each already passed its own review→ready
       sign-off inside the sub-plan pipeline).
    2. **Corpus gate** — a WHOLE-CORPUS-PLAN sign-off over the total blast radius
       (sum of accepted sub-plans' note counts). With the default headless
       policy it approves; pass ``corpus_sign_off_policy`` with ``use_human`` +
       ``human_prompt`` to require human approval before promoting a high-blast
       corpus. A ``rejected`` / ``needs_human`` corpus gate promotes NOTHING.
    3. **Execute** — each ACCEPTED, non-overlapping sub-plan is executed via
       :func:`~tessellum.composer.digestion.run_execute_wave` as its OWN
       snapshot-pinned transaction. A sub-plan whose execute wave errors is
       ``blocked``; the others still promote (a weak sub-plan blocks only
       itself). Blocked-at-planning sub-objectives are never executed.

    **M6 term-ownership gate.** When ``introduced_terms`` (the corpus-wide
    undigested-term sweep) is supplied, :func:`term_ownership_gate` asserts every
    introduced term has exactly one owner sub-objective. It runs FIRST — before
    the planning wave — because its inputs are known at entry and not produced by
    planning, so a corpus destined to be blocked pays zero planning-wave cost; a
    failed gate promotes NOTHING (an unowned cross-cutting term would ship a
    ghost reference). Opt-in — omitted → the gate does not run.

    **M7 shared cross-refs.** The corpus's shared cross-references are resolved
    ONCE (:func:`~tessellum.composer.corpus_plan.resolve_shared_cross_refs`) —
    deduped by target and, when ``shared_cross_ref_exists`` is injected,
    existence-filtered against the pinned snapshot — then threaded into every
    sub-plan, so a broken/duplicate shared link is dropped here instead of
    re-derived and re-linked in N sub-plans. The resolution report is on the
    result's ``shared_cross_refs`` field. ``shared_cross_ref_exists`` is injected
    (composer stays vault-I/O-free); omitted → dedup only.

    **M5 scheduling.** Execution walks
    :meth:`~tessellum.composer.corpus_plan.CorpusPlan.dependency_layers` —
    ordered dependency layers, priority-major within each. Cross-layer ordering
    is a hard barrier (a dependent sub-plan's transaction runs strictly after
    its dependency's committed), so a P2 sub-plan's cross-links resolve against
    a P1 sub-plan's already-published notes. Note this LAYER order is not the
    strict single-stream :meth:`~tessellum.composer.corpus_plan.CorpusPlan.wave_order`
    of M4 (a dependency-independent P3 sub-plan runs before a P1 that depends on
    it), so the ``executions`` order differs from the pre-M5 build — read
    ``bundle_status`` / ``promoted``, not tuple position.

    **Concurrency + isolation.** ``max_sub_plan_workers`` (default ``1`` =
    sequential) opts into running the dependency-INDEPENDENT sub-plans of a
    single layer concurrently. Each sub-plan is a real transaction: run-scoped
    execute kwargs (``manifest`` / ``run_id`` / ``events_path`` / ``stats_path``)
    are per-sub-plan-isolated (:func:`_isolate_execute_kwargs`), and a
    **write-closure disjointness gate** blocks any two accepted sub-plans that
    would write the same vault note BEFORE executing (fail-closed, so neither
    silent last-writer-wins nor a concurrent race can corrupt a shared note).
    Two knobs multiply into leaf concurrency: peak backend calls ≈
    ``max_sub_plan_workers × execute_max_workers`` (each sub-plan opens its own
    ``execute_max_workers`` leaf pool), so budget the PRODUCT against the shared
    provider's rate limit. A stateful ``effect_recorder`` / ``effect_guard`` must
    be thread-safe (leaf-level and sub-plan-level concurrency both invoke it);
    the shipped ``VaultEffectJournal`` already is (internal lock).

    Returns a :class:`CorpusDigestionResult` with the planning result, the
    corpus sign-off, per-sub-plan execute outcomes, and the bundle-completion
    rollup (``complete`` | ``partially_promoted`` | ``blocked``).
    """
    # ── M6 corpus-wide term-ownership gate (fail closed, FAIL FAST) ─────────
    # When the caller supplies the corpus-wide undigested-term sweep, assert
    # every introduced term has exactly one owner sub-objective — an unowned
    # cross-cutting term would ship a ghost reference (the exact failure the
    # skill §4e.4 sweep prevents). Its inputs (corpus_plan.term_ownership +
    # introduced_terms) are known at entry and are NOT produced by planning, so
    # this runs BEFORE the planning wave: a corpus destined to be blocked pays
    # ZERO planning-wave LLM cost. The bundle_id match (normally checked inside
    # the wave) is asserted here first so a mismatch still raises before the gate.
    # Skipped when introduced_terms is None (opt-in), preserving M4/M5 behavior.
    term_ownership: TermOwnershipResult | None = None
    if introduced_terms is not None:
        if corpus_plan.bundle_id != bundle.bundle_id:
            raise ValueError(
                f"corpus_plan.bundle_id {corpus_plan.bundle_id!r} does not match "
                f"bundle.bundle_id {bundle.bundle_id!r}"
            )
        term_ownership = term_ownership_gate(corpus_plan, introduced_terms)
        if not term_ownership.passed:
            return CorpusDigestionResult(
                bundle_id=bundle.bundle_id, objective=corpus_plan.objective,
                planning=CorpusPlanningResult(
                    bundle_id=bundle.bundle_id, objective=corpus_plan.objective,
                    sub_plans=(), all_accepted=False,
                    accepted_count=0, blocked_count=0,
                ),
                corpus_sign_off=None, executions=(),
                bundle_status="blocked", term_ownership=term_ownership,
            )

    # ── M7: resolve shared cross-refs ONCE at corpus scope ──────────────────
    # Dedup by target + (when a snapshot existence check is injected) drop refs
    # to notes not in the vault, so a broken/duplicate shared link is removed
    # here instead of re-derived and re-linked in every sub-plan. The resolved
    # set is threaded into the planning wave; the report is surfaced on the
    # result. With no resolver + no shared refs this is a no-op.
    shared_resolution = resolve_shared_cross_refs(
        corpus_plan.shared_cross_refs, exists=shared_cross_ref_exists
    )

    planning = run_corpus_planning_wave(
        corpus_plan, bundle, member_contents,
        skills_dir=skills_dir, backend=backend, vault_root=vault_root,
        dry_run=dry_run, budget=budget, context_assembler=context_assembler,
        cancellation_check=cancellation_check, effect_guard=effect_guard,
        shared_cross_refs=shared_resolution.resolved,
    )
    accepted = [o for o in planning.sub_plans if o.accepted]

    # ── corpus gate: sign off the WHOLE corpus plan before any promotion ────
    # Each sub-plan already passed its own review→ready sign-off INSIDE the
    # sub-plan pipeline (M3). The corpus gate adds a whole-corpus human rung on
    # HIGH TOTAL BLAST: when the policy enables the human rung and the summed
    # note count of the accepted sub-plans exceeds the threshold, a human must
    # approve before ANY sub-plan is promoted. This is a corpus-scope escalation
    # that does not need an agent rung (the sub-plans are already program-gated),
    # so it is computed directly rather than via the agent-first sign-off ladder.
    policy = corpus_sign_off_policy or SignOffPolicy(use_agent=False, use_human=False)
    corpus_sign_off: SignOffResult | None = None
    if accepted:
        per_sub_notes = [int(o.plan_doc.get("total_notes") or 0) for o in accepted]
        total_blast = sum(per_sub_notes)
        # Fail CLOSED: if any accepted sub-plan reports no positive note count,
        # the true blast is UNKNOWN — treat the corpus as high-blast so the
        # human gate is never silently skipped on an unmeasurable corpus.
        blast_unknown = any(n <= 0 for n in per_sub_notes)
        high_blast = total_blast > policy.blast_radius_threshold or blast_unknown
        if policy.use_human and human_prompt is not None and high_blast:
            approved = bool(human_prompt())
            corpus_sign_off = SignOffResult(
                decision="approved" if approved else "rejected",
                deciding_rung="human",
                escalated=("human",),
                reason=(
                    f"corpus human gate ({total_blast} notes > "
                    f"{policy.blast_radius_threshold} threshold)"
                ),
            )
        elif policy.use_human and human_prompt is None and high_blast:
            # Human rung requested for a high-blast corpus but no prompt wired →
            # do NOT auto-promote; surface for an out-of-band decision.
            corpus_sign_off = SignOffResult(
                decision="needs_human",
                deciding_rung="program",
                reason=(
                    f"corpus high blast ({total_blast} notes) needs human "
                    "approval but no human_prompt was provided"
                ),
            )
        else:
            corpus_sign_off = SignOffResult(
                decision="approved",
                deciding_rung="program",
                reason=(
                    f"corpus program gate ({total_blast} notes ≤ "
                    f"{policy.blast_radius_threshold} threshold or human rung off)"
                ),
            )
        if corpus_sign_off.decision != "approved":
            # Corpus gate did not approve → promote NOTHING (a3a: don't spend the
            # execution wave on an unapproved corpus).
            return CorpusDigestionResult(
                bundle_id=bundle.bundle_id, objective=corpus_plan.objective,
                planning=planning, corpus_sign_off=corpus_sign_off,
                executions=(), bundle_status="blocked",
                term_ownership=term_ownership,
                shared_cross_refs=shared_resolution,
            )

    # ── write-closure disjointness gate (M5): fail CLOSED on overlap ─────────
    # Two accepted sub-plans that would write the SAME vault note cannot both be
    # promoted safely: sequentially it is a silent last-writer-wins clobber;
    # concurrently (max_sub_plan_workers>1) it is a nondeterministic race. Rather
    # than trust the caller's "disjoint write-closures" guarantee, compute each
    # sub-plan's exact touched-note set (via the shipped write_closure over its
    # typed note_intent_graph) and BLOCK every sub-plan that overlaps another —
    # across the whole accepted set, not just within a layer (cross-layer clobber
    # is equally silent). Sub-plans on the prose fallback (no typed graph) can't
    # be proven to conflict, so they are not blocked here. This is the seed of
    # the M6 term-ownership gate.
    overlaps = _write_closure_overlaps(accepted)
    accepted_by_id = {o.sub_id: o for o in accepted}
    executions: list[SubPlanExecution] = [
        SubPlanExecution(
            sub_id=o.sub_id, priority=o.priority, promoted=False,
            status="blocked", run=None,
            reason=f"write-closure overlap on {sorted(overlaps[o.sub_id])}"[:200],
        )
        for o in accepted if o.sub_id in overlaps
    ]

    def _execute_one(outcome: SubPlanOutcome) -> SubPlanExecution:
        try:
            run = run_execute_wave(
                outcome.plan_doc,
                skills_dir=skills_dir, backend=backend, vault_root=vault_root,
                dry_run=dry_run, execute_max_workers=execute_max_workers,
                budget=budget, context_assembler=context_assembler,
                related_notes_db=related_notes_db,
                cancellation_check=cancellation_check, effect_guard=effect_guard,
                effect_recorder=effect_recorder,
                **_isolate_execute_kwargs(execute_kwargs, outcome.sub_id),
            )
        except InterruptedError:
            raise
        except Exception as exc:  # one sub-plan's execute failure isolates
            return SubPlanExecution(
                sub_id=outcome.sub_id, priority=outcome.priority, promoted=False,
                status="blocked", run=None,
                reason=f"execute raised: {type(exc).__name__}: {exc}"[:200],
            )
        promoted = run.error_count == 0
        return SubPlanExecution(
            sub_id=outcome.sub_id, priority=outcome.priority, promoted=promoted,
            status="promoted" if promoted else "blocked", run=run,
            reason=None if promoted else f"{run.error_count} execute error(s)",
        )

    for layer in corpus_plan.dependency_layers():
        # accepted, non-overlapping sub-plans in this layer, in layer order.
        todo = [
            accepted_by_id[sid]
            for sid in layer
            if sid in accepted_by_id and sid not in overlaps
        ]
        if not todo:
            continue
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError(
                "corpus digestion cancelled before executing layer "
                f"{[o.sub_id for o in todo]!r}"
            )
        if max_sub_plan_workers <= 1 or len(todo) == 1:
            executions.extend(_execute_one(o) for o in todo)
        else:
            # Concurrent within the layer; results re-ordered to the layer's
            # deterministic order so the run list is reproducible.
            with ThreadPoolExecutor(max_workers=max_sub_plan_workers) as pool:
                by_sub = dict(zip(
                    (o.sub_id for o in todo),
                    pool.map(_execute_one, todo),
                ))
            executions.extend(by_sub[o.sub_id] for o in todo)

    promoted_count = sum(1 for e in executions if e.promoted)
    # bundle rollup over ALL sub-objectives (planning-blocked count against the
    # corpus): complete only if every sub-objective promoted.
    if promoted_count == len(corpus_plan.sub_objectives):
        bundle_status = "complete"
    elif promoted_count == 0:
        bundle_status = "blocked"
    else:
        bundle_status = "partially_promoted"

    return CorpusDigestionResult(
        bundle_id=bundle.bundle_id, objective=corpus_plan.objective,
        planning=planning, corpus_sign_off=corpus_sign_off,
        executions=tuple(executions), bundle_status=bundle_status,
        term_ownership=term_ownership,
        shared_cross_refs=shared_resolution,
    )


__all__ = [
    "SubPlanOutcome",
    "CorpusPlanningResult",
    "run_corpus_planning_wave",
    "SubPlanExecution",
    "CorpusDigestionResult",
    "run_corpus_digestion",
]
