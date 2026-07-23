"""Digestion phase driver — the native plan → augment → review → execute flow.

This is the orchestrator that makes the four digestion SkillTools a single
pipeline (the FZ 20k2a "planning skills as phases" design realized against
the shipped composer). It sequences:

    plan  ──▶  augment  ──▶  review  ──[sign-off]──▶  execute

- **plan / augment / review** are *linear* phases — one skill each, run via
  :func:`run_pipeline` over the single ``plan_doc`` artifact (no fan-out;
  the plan is one thing). Each phase's output threads into the next as leaf
  context, so ``augment`` sees the plan, ``review`` sees the augmented plan.
- The **review → ready** transition is the graduated sign-off gate
  (:func:`~tessellum.composer.signoff.run_sign_off`): a pure ``plan``-scope
  program pre-filter (:func:`~tessellum.composer.gates.build_plan_gate`)
  **plus** the review skill's own typed ``ready``/``failures`` verdict form
  the program rung; the reviewer-agent + human rungs are injectable. A
  ``rejected`` sign-off **stops before execute** — the whole point of a
  gate is to not spend the execution wave on an unsound plan.
- **execute** is the fan-out phase — run via :func:`run_pipeline_dynamic`
  (the self-claiming wave), one leaf per planned note, so it inherits the
  close-gate / manifest / fix / budget machinery.

Boundary doctrine intact: this driver holds control flow + phase
sequencing; the Python compiler/contracts/gates/scheduler do the work; the
agent produces content. It is **one orchestrator, two invocation shapes**
(linear phases + the wave), sharing one artifact spine (``plan_doc``), one
gate engine, and one SkillTool model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tessellum.composer.compiler import compile_skill
from tessellum.composer.gates import build_plan_gate
from tessellum.composer.llm import LLMBackend
from tessellum.composer.scheduler import (
    RunResult,
    run_pipeline,
    run_pipeline_dynamic,
)
from tessellum.composer.signoff import (
    AgentJudge,
    HumanPrompt,
    SignOffPolicy,
    SignOffResult,
    run_sign_off,
)

# The four phase skills, in pipeline order. Resolved under a skills dir.
PHASE_SKILLS = {
    "plan": "skill_tessellum_plan_digestion",
    "augment": "skill_tessellum_augment_digestion_plan",
    "review": "skill_tessellum_review_digestion_plan",
    "execute": "skill_tessellum_execute_digestion_plan",
}


@dataclass(frozen=True)
class PhaseOutcome:
    """One phase's result within the digestion pipeline.

    Attributes:
        phase: ``"plan"`` | ``"augment"`` | ``"review"`` | ``"execute"``.
        ran: ``True`` iff the phase was dispatched (``execute`` is skipped
            when sign-off rejects).
        error_count: The phase's ``RunResult.error_count`` (0 when clean).
        run: The phase's :class:`RunResult`, or ``None`` if it didn't run.
    """

    phase: str
    ran: bool
    error_count: int = 0
    run: RunResult | None = None


@dataclass(frozen=True)
class DigestionResult:
    """The end-to-end outcome of :func:`run_digestion_pipeline`.

    Attributes:
        completed: ``True`` iff every dispatched phase was clean AND
            sign-off approved AND execute ran clean.
        stopped_at: The phase where the pipeline halted (``"review"`` on a
            sign-off rejection; a phase name on a phase error), or ``None``
            when it ran to completion.
        sign_off: The :class:`SignOffResult` from the review → ready gate
            (``None`` if the pipeline stopped before review completed).
        phases: Ordered per-phase outcomes.
        plan_doc: The final plan artifact threaded through the phases.
    """

    completed: bool
    stopped_at: str | None
    sign_off: SignOffResult | None
    phases: tuple[PhaseOutcome, ...]
    plan_doc: dict = field(default_factory=dict)


def _run_phase_linear(
    skill_name: str,
    *,
    skills_dir: Path,
    leaf: dict,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool,
) -> RunResult:
    """Compile + run one skill as a single linear phase over ``leaf``."""
    compiled = compile_skill(skills_dir / f"{skill_name}.md")
    return run_pipeline(
        compiled,
        leaves=[leaf],
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
    )


def _collect_structured(run: RunResult) -> dict[str, Any]:
    """Merge every step's structured output into one dict (last-writer-wins
    per key) — the phase's contribution to the running ``plan_doc``."""
    merged: dict[str, Any] = {}
    for r in run.step_results:
        if r.error is None and isinstance(r.materialized.structured, dict):
            merged.update(r.materialized.structured)
    return merged


def run_digestion_pipeline(
    *,
    skills_dir: Path | str,
    source_leaf: dict,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    sign_off_policy: SignOffPolicy | None = None,
    agent_judge: AgentJudge | None = None,
    human_prompt: HumanPrompt | None = None,
    execute_max_workers: int = 4,
    **execute_kwargs: Any,
) -> DigestionResult:
    """Run the native plan → augment → review → execute digestion pipeline.

    Args:
        skills_dir: Directory holding the four ``skill_tessellum_*`` phase
            skills (canonical ``.md`` + ``.pipeline.yaml`` pairs).
        source_leaf: The initial leaf context for ``plan`` (the source
            description / payload). Its keys plus each phase's structured
            output accumulate into the ``plan_doc`` threaded downstream.
        backend: LLM backend for every phase.
        vault_root: Materializer root.
        dry_run: Pass-through to the phases.
        sign_off_policy: The ``review → ready`` policy. Defaults to a
            program-gate-only policy (``use_agent=False``) so the pipeline
            runs headless without an injected reviewer; pass a policy with
            ``use_agent``/``use_human`` to add those rungs.
        agent_judge / human_prompt: Injected sign-off rungs (used per the
            policy).
        execute_max_workers: Worker pool for the execute wave.
        **execute_kwargs: Forwarded to :func:`run_pipeline_dynamic` for the
            execute phase (e.g. ``close_gate``, ``manifest``, ``budget``,
            ``wave_gate``, ``informed_fixer``).

    Returns:
        A :class:`DigestionResult`. The pipeline stops early (``execute``
        not run) on any linear-phase error or a sign-off rejection.
    """
    skills_dir = Path(skills_dir)
    policy = sign_off_policy or SignOffPolicy(use_agent=False, use_human=False)
    phases: list[PhaseOutcome] = []
    plan_doc: dict[str, Any] = dict(source_leaf)

    # ── Linear phases: plan → augment → review ──────────────────────────────
    for phase in ("plan", "augment", "review"):
        run = _run_phase_linear(
            PHASE_SKILLS[phase],
            skills_dir=skills_dir,
            leaf=dict(plan_doc),
            backend=backend,
            vault_root=vault_root,
            dry_run=dry_run,
        )
        phases.append(
            PhaseOutcome(phase=phase, ran=True, error_count=run.error_count, run=run)
        )
        plan_doc.update(_collect_structured(run))
        if run.error_count:
            # A broken linear phase halts the pipeline before the wave.
            return DigestionResult(
                completed=False,
                stopped_at=phase,
                sign_off=None,
                phases=tuple(phases),
                plan_doc=plan_doc,
            )

    # ── review → ready sign-off gate ────────────────────────────────────────
    # Program rung = plan-structure pre-filter AND the review skill's typed
    # verdict (both must pass); agent/human rungs per policy.
    plan_gate = build_plan_gate()

    def _program_gate() -> tuple[bool, str | None]:
        composite = plan_gate.evaluate(plan_doc)
        if not composite.passed:
            return False, composite.first_failure_cause or "plan_structure"
        # The review phase's typed verdict merged into plan_doc at top level
        # (its step output_key carries {ready, failures}); a nested "verdict"
        # dict is also honoured if a skill emits one that way.
        verdict = plan_doc.get("verdict")
        if isinstance(verdict, dict):
            ready = bool(verdict.get("ready"))
            failures = verdict.get("failures") or []
        else:
            ready = bool(plan_doc.get("ready"))
            failures = plan_doc.get("failures") or []
        if not ready:
            msg = "; ".join(map(str, failures)) if failures else "review verdict not ready"
            return False, f"review: {msg[:200]}"
        return True, None

    # blast_radius = how many notes execute would write (drives high-blast
    # escalation to the human rung).
    blast_radius = int(plan_doc.get("total_notes") or 0)
    sign_off = run_sign_off(
        program_gate=_program_gate,
        policy=policy,
        blast_radius=blast_radius,
        agent_judge=agent_judge,
        human_prompt=human_prompt,
    )
    if sign_off.decision != "approved":
        # Rejected / needs_human → do NOT spend the execution wave.
        return DigestionResult(
            completed=False,
            stopped_at="review",
            sign_off=sign_off,
            phases=tuple(phases),
            plan_doc=plan_doc,
        )

    # ── execute: the fan-out wave (one leaf per planned note) ───────────────
    execute_compiled = compile_skill(skills_dir / f"{PHASE_SKILLS['execute']}.md")
    execute_leaves = plan_doc.get("execute_leaves")
    if not isinstance(execute_leaves, list) or not execute_leaves:
        # Default: one leaf carrying the whole plan_doc (the execute skill's
        # per-leaf step fans out from the plan it reads).
        execute_leaves = [dict(plan_doc)]
    execute_run = run_pipeline_dynamic(
        execute_compiled,
        leaves=execute_leaves,
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
        max_workers=execute_max_workers,
        **execute_kwargs,
    )
    phases.append(
        PhaseOutcome(
            phase="execute",
            ran=True,
            error_count=execute_run.error_count,
            run=execute_run,
        )
    )

    return DigestionResult(
        completed=execute_run.error_count == 0,
        stopped_at=None if execute_run.error_count == 0 else "execute",
        sign_off=sign_off,
        phases=tuple(phases),
        plan_doc=plan_doc,
    )


__all__ = [
    "PHASE_SKILLS",
    "PhaseOutcome",
    "DigestionResult",
    "run_digestion_pipeline",
]
