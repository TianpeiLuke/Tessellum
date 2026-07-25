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

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ContextManager

from tessellum.composer.context_assembler import ContextAssembler
from tessellum.composer.corpus_plan import (
    CorpusPlan,
    SharedCrossRef,
    SubObjective,
    build_corpus_leaf,
)
from tessellum.composer.credential_pool import RunBudget
from tessellum.composer.digestion import DigestionResult, run_digestion_pipeline
from tessellum.composer.knowledge_plan import BundleMember, SourceBundle
from tessellum.composer.llm import LLMBackend


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
            leaf = _thread_shared_cross_refs(leaf, corpus_plan.shared_cross_refs)
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


__all__ = [
    "SubPlanOutcome",
    "CorpusPlanningResult",
    "run_corpus_planning_wave",
]
