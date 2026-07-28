"""Digestion phase driver — the native plan → augment → review → execute flow.

This is the orchestrator that makes the four digestion SkillTools a single
pipeline (the "planning skills as phases" design realized against the
shipped composer). It sequences:

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

import dataclasses
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ContextManager

from tessellum.composer.compiler import (
    HARD_PROMPT_CAP_CHARS,
    CompiledPipeline,
    compile_skill,
)
from tessellum.composer.context_assembler import ContextAssembler, WindowedAssembler
from tessellum.composer.contracts import _ARTIFACT_KEYS, PlanDoc
from tessellum.composer.credential_pool import ErrorClassBreaker, RunBudget
from tessellum.composer.executor import (
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_TRUNCATION_BASE_TOKENS,
    MAX_TRUNCATION_CEILING_TOKENS,
    upstream_placeholder_keys,
)
from tessellum.composer.gates import build_plan_gate, duplicate_target_predicate
from tessellum.composer.knowledge_plan import (
    NoteIntentGraph,
    project_note_intent_graph,
)
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
            when sign-off rejects, and also when ``stop_after="review"`` —
            the M3 accepted-but-not-executed path).
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
        completed: ``True`` iff the pipeline reached a clean terminal state —
            either every dispatched phase was clean AND sign-off approved AND
            execute ran clean (the full path), OR ``stop_after="review"`` and
            sign-off approved (M3: the plan is ACCEPTED but deliberately NOT
            executed). Check ``stopped_at`` to distinguish: ``None`` = fully
            executed, ``"review_accepted"`` = accepted-not-executed.
        stopped_at: Where the pipeline halted: ``"review"`` on a sign-off
            rejection; a phase name on a phase error; ``"review_accepted"`` when
            ``stop_after="review"`` approved (M3); ``"execute_preflight"`` when
            the P13 pre-flight failed the plan before the execute wave dispatched
            (FZ 20k9c1a1a1b7c2e — zero notes written); ``None`` when it fully
            executed to completion.
        sign_off: The :class:`SignOffResult` from the review → ready gate
            (``None`` if the pipeline stopped before review completed).
        phases: Ordered per-phase outcomes.
        plan_doc: The final plan artifact threaded through the phases.
        under_produced: ``True`` iff the plan declared more notes than the
            execute wave produced (FZ 20k9c1a1a1b7c2b / b7c2g) — the
            silent-under-production failure mode (an N-note plan producing ~1
            note). Set on two paths: the full path when leaf-count < declared,
            AND the P13 ``execute_preflight`` halt (the plan was caught
            under-producing BEFORE dispatch — zero notes written, but the flag
            still marks the under-production the pre-flight rejected). This is
            the programmatic signal a headless orchestrator branches on (it never
            sees the RuntimeWarning). ``False`` on the full path when leaf-count ≥
            declared, and when the pipeline stopped before execute for a reason
            OTHER than the pre-flight (nothing was produced to compare).
        review_rounds: How many EXTRA review-revise rounds ran (FZ
            20k9c1a1a1b7c2h / P15). ``0`` = the plan passed review on the first
            pass (or ``max_review_rounds=0``); ``N`` = the review rejected N
            times and the plan was re-augmented from the failures before
            converging (or exhausting the round budget).
    """

    completed: bool
    stopped_at: str | None
    sign_off: SignOffResult | None
    phases: tuple[PhaseOutcome, ...]
    plan_doc: dict = field(default_factory=dict)
    under_produced: bool = False
    review_rounds: int = 0


# P12 (FZ 20k9c1a1a1b7c2e): the shared ceiling for a DERIVED response budget.
# Aligned to the executor's MAX_TRUNCATION_CEILING_TOKENS so the derived base +
# P16's 2×-per-round truncation escalation share ONE ceiling (a step derived at
# the ceiling leaves P16 no headroom → it falls through to the normal terminal
# path at 64000, exactly as a hand-set 64000 step does today).
DERIVED_MAX_TOKENS_CEILING: int = MAX_TRUNCATION_CEILING_TOKENS
# The watchdog ceiling for a derived timeout — generous (a large plan's writer
# legitimately runs long), but bounded so a runaway note count can't set an
# effectively-infinite watchdog.
DERIVED_TIMEOUT_CEILING_SECONDS: float = 1800.0


def _derive_step_budgets(
    compiled: CompiledPipeline, *, declared_notes: int
) -> CompiledPipeline:
    """Raise a step's response/watchdog budget from its static FLOOR by the
    plan's declared work (P12; FZ 20k9c1a1a1b7c2e).

    The E14/E17 fix hand-set ``max_tokens: 32000`` + ``timeout_seconds: 900`` on
    the big-output writers — which closes the SYMPTOM per step but not the CLASS:
    a plan declaring 200 notes vs 8, or a NEW large-output step, still inherits a
    constant tuned for a small plan and truncates/stalls. A step that declares a
    ``max_tokens_per_note`` / ``timeout_seconds_per_note`` coefficient is instead
    made self-budgeting here: the driver rewrites its effective budget from
    ``total_notes`` (a RUNTIME plan value, absent at compile time — which is why
    this is a driver step over the compiled pipeline, not a compile-time one).

    Invariants:
    - **Floor, never lower.** ``effective = max(static, base + coeff*notes)`` —
      a hand-set value is a FLOOR the derivation can only RAISE. A small plan on
      a ``max_tokens: 32000`` step stays exactly 32000.
    - **Ceiling.** Clamped to :data:`DERIVED_MAX_TOKENS_CEILING` (shared with
      P16) / :data:`DERIVED_TIMEOUT_CEILING_SECONDS`.
    - **Identity guard (byte-identical when unused).** A step declaring NO
      coefficient, or ``declared_notes <= 0``, is returned UNCHANGED. So the
      whole pipeline is byte-identical until a skill opts in (and the plan phase,
      whose leaf has no ``total_notes`` yet, is always a no-op — ``total_notes``
      is produced BY the plan phase).

    Composes with P16: the rewritten ``max_tokens`` becomes P16's escalation base
    (``executor`` reads ``step.max_tokens``), so the derived value is a
    right-sized START and P16 stays the last-resort self-heal. This rewrites only
    the RESPONSE-output budget — orthogonal to the compiler's
    ``_validate_context_budgets``, which bounds prompt-INPUT chars.
    """
    if declared_notes <= 0:
        return compiled  # no signal → no-op (byte-identical)

    changed = False
    new_steps = []
    for step in compiled.steps:
        mt_coeff = step.max_tokens_per_note
        to_coeff = step.timeout_seconds_per_note
        if mt_coeff is None and to_coeff is None:
            new_steps.append(step)
            continue
        replace_kwargs: dict[str, Any] = {}
        if mt_coeff is not None:
            base = step.max_tokens or DEFAULT_TRUNCATION_BASE_TOKENS
            derived = base + mt_coeff * declared_notes
            effective = min(DERIVED_MAX_TOKENS_CEILING, max(step.max_tokens or 0, derived))
            if effective != step.max_tokens:
                replace_kwargs["max_tokens"] = effective
        if to_coeff is not None:
            base_t = step.timeout_seconds or DEFAULT_TIMEOUT_SECONDS
            derived_t = base_t + to_coeff * declared_notes
            effective_t = min(
                DERIVED_TIMEOUT_CEILING_SECONDS, max(step.timeout_seconds or 0.0, derived_t)
            )
            if effective_t != step.timeout_seconds:
                replace_kwargs["timeout_seconds"] = effective_t
        if replace_kwargs:
            new_steps.append(dataclasses.replace(step, **replace_kwargs))
            changed = True
        else:
            new_steps.append(step)

    if not changed:
        return compiled
    # Rebuild the pipeline replacing ONLY the steps tuple — preserve
    # budget_warnings / re_emission_warnings / compiled_at / pipeline_version.
    return dataclasses.replace(compiled, steps=tuple(new_steps))


def _build_artifact_store(plan_doc: dict[str, Any]) -> dict[str, Any]:
    """The by-reference artifact store the driver injects into each phase's
    prompts (P21-full; FZ 20k9c1a1a1b7c2j). Snapshots the current durable value
    of each allowlisted artifact key (``_ARTIFACT_KEYS``) from the — already
    ``_normalize_plan_doc_keys``-normalized — ``plan_doc``, so a consumer reads
    ``{{artifact.plan_text}}`` by reference instead of a prior step re-emitting
    it. Only present, non-empty values are included (an absent key → a
    ``<missing artifact.X>`` sentinel at render, same debug affordance as
    ``{{leaf.X}}``)."""
    store: dict[str, Any] = {}
    for key in _ARTIFACT_KEYS:
        val = plan_doc.get(key)
        if val not in (None, "", [], ()):
            store[key] = val
    return store


def _run_phase_linear(
    skill_name: str,
    *,
    skills_dir: Path,
    leaf: dict,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool,
    budget: RunBudget | None,
    context_assembler: ContextAssembler | None,
    cancellation_check: Callable[[], bool] | None,
    effect_guard: Callable[[], ContextManager[None]] | None,
    effect_recorder: Callable[[Path], None] | None,
    runs_dir: Path | None = None,
    artifacts: dict[str, Any] | None = None,
) -> RunResult:
    """Compile + run one skill as a single linear phase over ``leaf``.

    P20 (FZ 20k9c1a1a1b7c2g): forwards ``runs_dir`` so the linear phases
    (plan / augment / review) emit the SAME per-step trace as the execute wave.
    Before P20 they passed no ``runs_dir`` and were dark — yet they hosted the
    worst blockers (E4/E5/E15's `write_plan`), so the phases that most needed
    telemetry had none. ``None`` → no trace (byte-identical to pre-P20).

    P21-full: forwards the by-reference ``artifacts`` store so a phase can read a
    large durable artifact via ``{{artifact.X}}`` instead of a prior step
    re-emitting it. ``None`` → no artifact substitution (byte-identical)."""
    compiled = compile_skill(skills_dir / f"{skill_name}.md")
    # P12: raise coefficient-bearing steps' budgets by the plan's declared work.
    # The leaf carries total_notes for aug/review (leaf = dict(plan_doc)); the
    # plan phase's leaf has none → declared_notes=0 → no-op.
    compiled = _derive_step_budgets(compiled, declared_notes=_declared_note_count(leaf))
    return run_pipeline(
        compiled,
        leaves=[leaf],
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
        budget=budget,
        artifacts=artifacts,
        context_assembler=context_assembler,
        cancellation_check=cancellation_check,
        effect_guard=effect_guard,
        effect_recorder=effect_recorder,
        runs_dir=runs_dir,
    )


# P1 seam: the typed, snapshot-pinned replacement for this last-writer-wins
# fold is :func:`tessellum.composer.proposals.merge_proposals` (fed by
# :func:`~tessellum.composer.proposals.collect_proposals`). P0 leaves this
# fold byte-identical — the typed path is additive and not called here.
def _collect_structured(run: RunResult) -> dict[str, Any]:
    """Merge every step's structured output into one dict (last-writer-wins
    per key) — the phase's contribution to the running ``plan_doc``."""
    merged: dict[str, Any] = {}
    for r in run.step_results:
        if r.error is None and isinstance(r.materialized.structured, dict):
            merged.update(r.materialized.structured)
    return merged


# The three plan-of-record guards (E6 alias bridge, longest-of plan_text, P21
# total_notes floor) now live as the validators of the typed :class:`PlanDoc`
# envelope (P22, FZ 20k9c1a1a1b7c2f). ``_normalize_plan_doc_keys`` is the thin
# in-place ADAPTER over it — it keeps ``plan_doc`` a plain mutable dict for the
# ~15 setdefault/clear/update/[]= sites (incl. the P24 snapshot-restore) while
# folding the guards through one validated construction. The alias map is the
# ``PlanDoc._PLAN_DOC_KEY_ALIASES`` classvar (single source of truth).


def _normalize_plan_doc_keys(plan_doc: dict[str, Any]) -> None:
    """Bridge plan-skill output keys to the canonical names the gate + augment/
    review steps consume, and protect the plan of record. Mutates ``plan_doc``
    in place; idempotent.

    Delegates the actual folding to :class:`PlanDoc` (P22) — which folds three
    guards into one validated construction:

    1. **E6 alias bridge** — fill an absent/empty canonical key (``plan_path`` /
       ``plan_text`` / ``total_notes``) from the write-plan materializer's alias
       (``output_path`` / ``body_markdown`` / ``planned_note_count`` /
       ``estimated_note_count``); without it the gate reads ``total_notes=0`` +
       ``plan_path=<missing>`` and rejects every plan.
    2. **Longest-of ``plan_text`` guard** (FZ 20k9c1a1a1b7c2c) — the review
       ``step_1_read_plan`` re-emits ``plan_text`` and the model returns a lossy
       SUMMARY; the authoritative ``body_markdown`` (if longer) is restored so a
       re-emission can never shrink the plan of record under last-writer-wins.
    3. **``total_notes`` floor** (P21 core, FZ 20k9c1a1a1b7c2h) — you cannot
       declare fewer notes than you enumerated in ``planned_notes``.

    In-place: only the canonical envelope keys are written back (from the
    validated envelope); every extra key the plan carries is untouched, and no
    key is removed — byte-identical to the prior imperative implementation."""
    envelope = PlanDoc.from_dict(plan_doc)
    # Write back only the canonical envelope keys, in place — never drop the
    # ~dozen extra keys (members, routing_decision, note_intent_graph, …) the
    # plan carries, and never rebind plan_doc to a new object (the ~15 dict
    # call-sites hold the same reference). Byte-identical to the prior imperative
    # version: a canonical key is written ONLY when the fold produced a real
    # value or the key already existed — an unfillable key stays ABSENT (so the
    # `<missing leaf.X>` sentinel + `in` checks behave exactly as before), never
    # created as an empty "" / 0 default.
    for key in ("plan_path", "plan_text", "total_notes"):
        new_val = getattr(envelope, key)
        if key in plan_doc or new_val not in ("", 0):
            plan_doc[key] = new_val


def _review_verdict(plan_doc: dict) -> tuple[bool, list]:
    """Extract the review phase's typed ``(ready, failures)`` verdict from
    ``plan_doc`` — the single reader used by both the sign-off program gate and
    the P15 revise loop (FZ 20k9c1a1a1b7c2h), so the two agree on what "ready"
    means. The review skill's ``step_4_report_verdict`` merges ``{ready,
    failures}`` at the top level; a nested ``verdict`` dict is also honoured."""
    verdict = plan_doc.get("verdict")
    if isinstance(verdict, dict):
        return bool(verdict.get("ready")), list(verdict.get("failures") or [])
    return bool(plan_doc.get("ready")), list(plan_doc.get("failures") or [])


def _declared_note_count(plan_doc: dict) -> int:
    """How many notes the plan declares — the single source of truth for the
    under-production check (FZ 20k9c1a1a1b7c2b / b7c2g).

    Prefers the explicit ``total_notes`` scalar, falling back to the length of
    the ``planned_notes`` list. Both the loud ``RuntimeWarning`` in
    :func:`run_execute_wave` and the ``DigestionResult.under_produced`` flag key
    on this, so a headless orchestrator and a dev watching warnings see the same
    number. Returns ``0`` when neither is present (nothing to compare against).
    """
    total = plan_doc.get("total_notes")
    if isinstance(total, int) and total > 0:
        return total
    planned = plan_doc.get("planned_notes")
    return len(planned) if isinstance(planned, list) else 0


def _project_planned_notes_to_leaves(plan_doc: dict) -> list[dict]:
    """Project an LLM-authored plan's ``planned_notes`` into per-note writer
    leaves — the native execute-wave fan-out (FZ 20k9c1a1a1b7c2b).

    The plan/augment/review skills emit ``plan_doc["planned_notes"]`` (a list of
    ``{filename, building_block, approx_words, description}``), but only the typed
    ``note_intent_graph`` path had a projector, so the native single-doc path fell
    back to a single whole-plan leaf and produced ~1 note for an N-note plan. This
    builds one leaf per planned note, symmetric with
    :func:`~tessellum.composer.knowledge_plan.project_note_intent_graph`.

    Each leaf carries the ``note`` payload the ``dispatch_notes`` writer reads
    (filename / thesis / building_block), a vault-relative ``target_path``
    (routing dir + file prefix + filename — what the E2 type-contract resolver
    keys on), the ``source_ref``, and — because the composer backend is single-
    shot with no file-reading tool — the source content inline (``source_excerpt``
    + the full ``plan_text`` for cross-note context). Pure + fail-soft: a
    ``planned_notes`` that is missing, not a list, or has no usable ``filename``
    yields ``[]`` so the caller falls through to the whole-plan leaf.
    """
    planned = plan_doc.get("planned_notes")
    if not isinstance(planned, list) or not planned:
        return []

    # Routing: where notes land + their filename prefix (best-effort from the
    # plan; default to a generic docs dir so target_path is always vault-relative).
    routing = plan_doc.get("routing_decision")
    routing = routing if isinstance(routing, dict) else {}
    note_dir = str(
        plan_doc.get("note_dir")
        or plan_doc.get("target_directory")
        or routing.get("target_directory")
        or "resources/documentation"
    ).strip("/") or "resources/documentation"
    prefix = str(plan_doc.get("file_prefix") or routing.get("file_prefix") or "")

    # Source content: the admitted members' excerpts (inline — single-shot backend).
    members = plan_doc.get("members")
    source_excerpt = ""
    source_refs: list[str] = []
    if isinstance(members, list) and members:
        parts = []
        for m in members:
            if not isinstance(m, dict):
                continue
            ex = m.get("excerpt") or m.get("source_content") or ""
            ref = m.get("source_url") or m.get("ref") or m.get("source_id") or ""
            if ref:
                source_refs.append(str(ref))
            parts.append(f"# SOURCE: {m.get('source_id') or ref}\n\n{ex}")
        source_excerpt = "\n\n".join(parts)
    if not source_refs:
        su = plan_doc.get("source_url")
        source_refs = list(su) if isinstance(su, list) else ([str(su)] if su else [])
    plan_text = str(plan_doc.get("plan_text") or "")

    leaves: list[dict] = []
    for pn in planned:
        if not isinstance(pn, dict):
            continue
        filename = str(pn.get("filename") or pn.get("note") or "").strip().strip("/")
        if not filename:
            continue
        if not filename.endswith(".md"):
            filename += ".md"
        name = filename if filename.startswith(prefix) else f"{prefix}{filename}"
        leaves.append({
            "note": {
                "filename": name,
                "thesis": str(pn.get("description") or ""),
                "building_block": pn.get("building_block"),
                "approx_words": pn.get("approx_words"),
                "source_excerpt": source_excerpt,
                "plan_text": plan_text,
            },
            "target_path": f"{note_dir}/{name}",
            "source_ref": source_refs,
        })
    return leaves


def _enrich_leaves_with_related_notes(
    leaves: list[dict],
    *,
    related_notes_db: Path | str | None,
) -> list[dict]:
    """Attach per-note relevance-ranked related notes to each execute leaf.

    FZ 20k9d2 fix — the retrieval home for knowledge-graph edges. For each
    projected note leaf, retrieve related EXISTING vault notes keyed on THAT
    note's own ``thesis`` + ``coverage`` (not a shared job-level query),
    compute links relative to its ``target_path``, and attach:

        leaf["related_notes"]        # list of {note_id, note_name, rel_path, score}
        leaf["related_references_md"] # pre-rendered ## References block

    The writer sub-agent renders these into the note's ``## References`` section
    (the execute skill), so the indexer records them as ``note_links`` edges.

    Pure + fail-soft. A leaf lacking a typed ``note`` payload (the whole-plan
    fallback leaf) passes through UNCHANGED. With ``related_notes_db=None`` (no
    index yet — e.g. the first-ever digestion) note-bearing leaves are still
    stamped with EMPTY ``related_notes`` / ``related_references_md`` so the
    writer's placeholder renders "" (a clean empty block the skill handles),
    never a ``<missing …>`` sentinel. A retrieval failure for one leaf degrades
    THAT leaf to no related notes; it never raises.
    """
    from tessellum.composer.related_notes import enrich_related_notes

    enriched: list[dict] = []
    for leaf in leaves:
        note = leaf.get("note") if isinstance(leaf, dict) else None
        target_path = leaf.get("target_path") if isinstance(leaf, dict) else None
        # Only the typed per-note projection carries a ``note`` payload with a
        # thesis; the whole-plan fallback leaf has neither → pass through.
        if not isinstance(note, dict) or not isinstance(target_path, str):
            enriched.append(leaf)
            continue
        thesis = note.get("thesis")
        if not isinstance(thesis, str) or not thesis.strip():
            # A typed note leaf with no usable thesis: stamp empty defaults so
            # the writer's {{leaf.related_references_md}} renders "" rather than
            # a <missing …> sentinel (the skill handles an empty block).
            no_related = dict(leaf)
            no_related["related_notes"] = []
            no_related["related_references_md"] = ""
            enriched.append(no_related)
            continue
        coverage = note.get("coverage") or ()
        # depends_on edges are structural (the plan already expresses them) —
        # exclude them from "related" references so we don't double-encode.
        # Guard the type symmetrically with coverage: an opt-in execute_leaves
        # leaf (not the model-validated typed projection) could carry a non-
        # iterable depends_on; tuple(5) would raise and kill the wave.
        dep = note.get("depends_on")
        exclude = tuple(dep) if isinstance(dep, (list, tuple)) else ()
        result = enrich_related_notes(
            thesis=thesis,
            target_path=target_path,
            db_path=related_notes_db,
            coverage=coverage if isinstance(coverage, (list, tuple)) else (),
            exclude_ids=exclude,
        )
        new_leaf = dict(leaf)
        new_leaf["related_notes"] = [
            {
                "note_id": r.note_id,
                "note_name": r.note_name,
                "rel_path": r.rel_path,
                "score": r.score,
            }
            for r in result.related
        ]
        new_leaf["related_references_md"] = result.references_markdown
        enriched.append(new_leaf)
    return enriched


def _enrich_leaves_with_type_contract(
    leaves: list[dict],
    *,
    enabled: bool = True,
) -> list[dict]:
    """Attach each execute leaf's NOTE-TYPE contract, resolved from its type.

    FZ 20k9d1b1a1a (P4) — the type home for the writer, the structural twin of
    :func:`_enrich_leaves_with_related_notes`. For each projected note leaf,
    reverse-resolve its ``target_path`` to a ``capture.REGISTRY`` flavor (keyed
    on the flavor, NOT ``building_block`` — the two are orthogonal, and a
    per-note BB override must not fight resolution), build that flavor's section
    contract, and attach:

        leaf["type_contract"]     # {flavor, second_category, building_block, required_sections}
        leaf["type_contract_md"]  # pre-rendered compact contract block

    The writer renders ``## H2`` sections from ``{{leaf.type_contract_md}}`` next
    to the ``## References`` block (the execute skill's ``dispatch_notes`` step).
    For a primary flavor the delivered sections match the BB-keyed ``TESS-010``
    advisory; for a ``SECTION_DIVERGENT`` flavor (or a per-note ``building_block``
    override) they differ and a conforming note may still raise TESS-010 INFOs —
    acceptable because TESS-010 is advisory, not a gate (see
    :mod:`tessellum.composer.type_contract`).

    Pure + fail-soft, mirroring the related-notes precedent. ``enabled=False`` is
    the explicit off-switch → the input list is returned UNCHANGED (byte-
    identical). A leaf lacking a typed ``note`` payload + ``target_path`` (the
    whole-plan fallback leaf) passes through UNCHANGED (no keys added). A typed
    leaf whose ``target_path`` resolves to NO flavor (a ``capture()`` override
    dir, a bare filename) is stamped with an EMPTY contract / ``""`` so the
    writer's ``{{leaf.type_contract_md}}`` renders "" rather than a ``<missing …>``
    sentinel. Resolution is wrapped fail-soft; one malformed leaf degrades to an
    empty contract, never raises into the wave-parallel run.
    """
    if not enabled:
        return leaves
    from tessellum.composer.type_contract import resolve_note_contract

    enriched: list[dict] = []
    for leaf in leaves:
        note = leaf.get("note") if isinstance(leaf, dict) else None
        target_path = leaf.get("target_path") if isinstance(leaf, dict) else None
        # Only the typed per-note projection carries a ``note`` + ``target_path``;
        # the whole-plan fallback leaf has neither → pass through unchanged.
        if not isinstance(note, dict) or not isinstance(target_path, str):
            enriched.append(leaf)
            continue
        tc = resolve_note_contract(target_path)
        new_leaf = dict(leaf)
        if tc is None:
            # Unresolvable typed leaf: stamp empty defaults so the writer's
            # {{leaf.type_contract_md}} renders "" (not a <missing …> sentinel).
            new_leaf["type_contract"] = {}
            new_leaf["type_contract_md"] = ""
        else:
            new_leaf["type_contract"] = {
                "flavor": tc.flavor,
                "second_category": tc.second_category,
                "building_block": tc.building_block,
                "required_sections": list(tc.required_sections),
            }
            new_leaf["type_contract_md"] = tc.contract_md
        enriched.append(new_leaf)
    return enriched


def _execute_fallback_strategy(skills_dir: Path | str) -> str | None:
    """The most-tolerant ``fallback_strategy`` declared by any MCP the execute
    skill depends on (P17). The compiler drops ``mcp_dependencies``, so — like
    :func:`~tessellum.composer.skill_tool.build_skill_tool` — re-read them from
    the loader and map each dep name → ``MCP_CONTRACTS[name].fallback_strategy``.

    Returns ``"degrade"`` if ANY declared MCP is ``degrade`` (the most-tolerant
    posture wins — one degradable dependency means the wave is designed to
    proceed through a soft failure); ``"fail_fast"``/``"retry_then_fail"`` when
    those are the only postures; ``None`` when no MCP is declared (the common
    case → the caller keeps the default tripping classes). Fail-soft: any load
    error → ``None`` (default posture), never raises into the execute path."""
    from tessellum.composer.contracts import MCP_CONTRACTS
    from tessellum.composer.loader import load_pipeline

    try:
        pipeline = load_pipeline(Path(skills_dir) / f"{PHASE_SKILLS['execute']}.md")
    except Exception:  # noqa: BLE001 — fail-soft to the default posture
        return None
    if pipeline is None:
        return None
    postures: set[str] = set()
    for step in pipeline.pipeline:
        for dep in step.mcp_dependencies:
            contract = MCP_CONTRACTS.get(dep.name)
            if contract is not None:
                postures.add(contract.fallback_strategy)
    if not postures:
        return None
    # Most-tolerant wins: degrade > retry_then_fail > fail_fast.
    for posture in ("degrade", "retry_then_fail", "fail_fast"):
        if posture in postures:
            return posture
    return None


# ── P13: static plan pre-flight before the execute wave dispatches ───────────


@dataclass(frozen=True)
class PreflightResult:
    """The verdict of :func:`preflight_execute_wave` — a static, pre-dispatch
    coherence check over the accepted plan + its projected leaves (P13;
    FZ 20k9c1a1a1b7c2e). ``ok`` is ``True`` iff no blocking issue was found."""

    ok: bool
    issues: tuple[str, ...]
    declared: int
    leaf_count: int

    @property
    def actionable_message(self) -> str:
        """One string joining the issues — a headless caller branches on
        ``ok`` and surfaces this rather than parsing a warning stream."""
        return "; ".join(self.issues)


class PreflightError(RuntimeError):
    """Raised by :func:`run_execute_wave` when the pre-flight fails — the
    execute wave is aborted BEFORE any backend call. Carries the
    :class:`PreflightResult`."""

    def __init__(self, result: PreflightResult) -> None:
        super().__init__(
            f"execute pre-flight failed ({len(result.issues)} issue(s)): "
            f"{result.actionable_message}"
        )
        self.result = result


def preflight_execute_wave(
    plan_doc: dict,
    execute_leaves: list[dict],
    *,
    compiled: "CompiledPipeline | None" = None,
) -> PreflightResult:
    """Statically check an accepted plan + its projected leaves BEFORE the
    execute wave burns any backend calls (P13; FZ 20k9c1a1a1b7c2e).

    The compile-time / pre-dispatch complement to the shipped P23 (which fails
    loud at RUNTIME on a missing consumed input). The retrospective
    (FZ 20k9c1a1a1b7c2i) named a pre-dispatch check as a top prevention: the
    execute wave's silent under-production (an N-note plan collapsing to the
    single whole-plan fallback leaf → ~1 note) used to only *warn*; P13 turns it
    into a fail-loud abort so the defect surfaces before N leaves of wasted work.

    Pure — no backend, no filesystem. Checks (all skipped when ``declared <= 1``,
    preserving the legitimate corpus-of-one / degenerate whole-plan fallback):

    1. **Fan-out collapse** — ``declared > 1`` but fewer leaves than declared
       (the E11 single-whole-plan-leaf failure). The promoted warning.
    2. **Silently-dropped notes** — a ``planned_notes`` row lacking a usable
       ``filename``/``note`` (the skip in ``_project_planned_notes_to_leaves``),
       or a projected leaf without a vault-relative ``target_path``.
    3. **Duplicate target paths** — two leaves writing the same note path
       (reuses the wave-gate ``duplicate_target_predicate``, pre-dispatch).
    4. **Dangling ``{{upstream.X}}``** (fail-soft) — a step referencing an
       output_key no step in the compiled pipeline produces. Best-effort; any
       introspection error skips ONLY this check.

    Does NOT re-assert plan shape the review plan gate owns (PLAN-002 plan_text,
    PLAN-003 total_notes>0) — those are checked at the review phase; P13 checks
    projection/leaf-level facts the plan gate structurally cannot see.

    Scope note: the ``declared`` count comes from ``_declared_note_count``
    (``total_notes`` / ``planned_notes``), so a typed ``note_intent_graph`` plan
    that carries NEITHER (its count lives in ``note_intent_graph.intents``) has
    ``declared == 0`` and short-circuits the fan-out check. That is acceptable —
    the graph path is the opt-in typed route: ``NoteIntentGraph.model_validate``
    already fails loud on an invalid graph, and its projection is deterministic
    (one leaf per intent), so it cannot silently collapse the way an untyped
    ``planned_notes`` plan can. The duplicate-target / dangling-upstream checks
    still run on its projected leaves when a positive count is present.
    """
    declared = _declared_note_count(plan_doc)
    leaf_count = len(execute_leaves)
    issues: list[str] = []

    # The whole-plan fallback (corpus-of-one / degenerate plan) is legitimate.
    if declared <= 1:
        return PreflightResult(ok=True, issues=(), declared=declared, leaf_count=leaf_count)

    # CHECK 1 — fan-out collapse (the core E11 case, promoted from a warning).
    if leaf_count < declared:
        detail = (
            f"execute wave projected {leaf_count} leaf(es) but the plan declares "
            f"{declared} notes"
        )
        if leaf_count <= 1 and not plan_doc.get("note_intent_graph"):
            detail += (
                " — the whole-plan fallback fired (no note_intent_graph and the "
                "planned_notes projection yielded too few leaves); the pipeline "
                "would under-produce ~1 note for an N-note plan"
            )
        issues.append(detail)

    # CHECK 2 — silently-dropped planned_notes rows + missing target_path.
    planned = plan_doc.get("planned_notes")
    if isinstance(planned, list):
        dropped = [
            i for i, pn in enumerate(planned)
            if not (isinstance(pn, dict)
                    and str(pn.get("filename") or pn.get("note") or "").strip().strip("/"))
        ]
        if dropped:
            issues.append(
                f"{len(dropped)} planned note(s) lack a usable filename/note and "
                f"would be silently dropped (rows {dropped})"
            )
    for i, leaf in enumerate(execute_leaves):
        tp = leaf.get("target_path") if isinstance(leaf, dict) else None
        # The whole-plan fallback leaf legitimately has no target_path; only flag
        # a leaf that IS a projected note (carries a typed `note`) but lacks one.
        if isinstance(leaf, dict) and leaf.get("note") and not (isinstance(tp, str) and tp.strip()):
            issues.append(f"projected note leaf {i} has no vault-relative target_path")

    # CHECK 3 — duplicate target paths (pre-dispatch reuse of the wave gate).
    target_paths = [
        leaf["target_path"] for leaf in execute_leaves
        if isinstance(leaf, dict) and isinstance(leaf.get("target_path"), str)
    ]
    for dup in duplicate_target_predicate(target_paths):
        issues.append(dup.message)

    # CHECK 4 — dangling {{upstream.X}} (fail-soft; best-effort static surfacing).
    if compiled is not None:
        try:
            produced = {s.output_key for s in compiled.steps if s.output_key}
            for step in compiled.steps:
                dangling = sorted(upstream_placeholder_keys(step) - produced)
                if dangling:
                    issues.append(
                        f"step {step.section_id!r} references {{{{upstream.X}}}} "
                        f"key(s) no step produces: {dangling}"
                    )
        except Exception:  # noqa: BLE001 — fail-soft: skip ONLY this check
            pass

    return PreflightResult(
        ok=not issues, issues=tuple(issues), declared=declared, leaf_count=leaf_count
    )


def run_execute_wave(
    plan_doc: dict,
    *,
    skills_dir: Path | str,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    execute_max_workers: int = 4,
    budget: RunBudget | None = None,
    breaker: "ErrorClassBreaker | None" = None,
    context_assembler: ContextAssembler | None = None,
    related_notes_db: Path | str | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
    **execute_kwargs: Any,
) -> RunResult:
    """Run ONLY the execute fan-out wave over an accepted ``plan_doc`` (M4 seam).

    Factored out of :func:`run_digestion_pipeline` so the corpus execute wave
    (:func:`~tessellum.composer.corpus_digestion.run_corpus_digestion`) can
    promote an ALREADY-ACCEPTED sub-plan (from an M3 ``stop_after="review"``
    run) as its own transaction WITHOUT re-planning it. Byte-identical to the
    execute half of ``run_digestion_pipeline``:

    - **P2b projection (OPT-IN):** if ``plan_doc["note_intent_graph"]`` is
      present, derive execute leaves from its deterministic projection (one
      BB-atomic leaf per note intent). A present-but-invalid graph fails loud.
    - Else fall back to ``plan_doc["execute_leaves"]`` or, absent that, a single
      leaf carrying the whole ``plan_doc`` (the execute skill fans out from the
      plan it reads).

    ``**execute_kwargs`` are forwarded to :func:`run_pipeline_dynamic` (e.g.
    ``close_gate``, ``manifest``, ``wave_gate``, ``informed_fixer``,
    ``max_fix_rounds``, ``run_id``, ``generation``).

    ``related_notes_db``: **FZ 20k9d2** — the live index DB used to enrich each
    projected note leaf with per-note relevance-ranked related notes (keyed on
    that note's own thesis + coverage, links relative to its target_path) that
    the writer renders into ``## References`` → ``note_links`` graph edges.
    ``None`` (default) → leaves pass through unchanged (byte-identical); fail-
    soft per leaf when the index is absent or retrieval errors.

    Fail-soft: when no ``context_assembler`` is passed, defaults a head+tail
    ``WindowedAssembler`` sized just under ``HARD_PROMPT_CAP_CHARS`` (the same
    default ``run_digestion_pipeline`` gives its linear phases) so an oversized
    execute prompt truncates + warns instead of tripping the hard cap and
    erroring the wave. The corpus execute path (which calls this directly) thus
    gets the same protection as the single-doc pipeline.
    """
    if context_assembler is None:
        context_assembler = WindowedAssembler(max_chars=HARD_PROMPT_CAP_CHARS - 4_096)
    compiled = compile_skill(Path(skills_dir) / f"{PHASE_SKILLS['execute']}.md")
    # P12: raise coefficient-bearing execute steps' budgets by the declared note
    # count (single-doc + corpus waves both route here). The per_leaf
    # dispatch_notes writer declares no coefficient — it is already self-budgeting
    # via the fan-out (one note per leaf), so it is never scaled by total_notes.
    compiled = _derive_step_budgets(compiled, declared_notes=_declared_note_count(plan_doc))
    graph_spec = plan_doc.get("note_intent_graph")
    if graph_spec is not None:
        graph = (
            graph_spec
            if isinstance(graph_spec, NoteIntentGraph)
            else NoteIntentGraph.model_validate(graph_spec)
        )
        execute_leaves = project_note_intent_graph(graph)
    else:
        execute_leaves = plan_doc.get("execute_leaves")
        if not isinstance(execute_leaves, list) or not execute_leaves:
            # FZ 20k9c1a1a1b7c2b: an LLM-authored plan carries `planned_notes`
            # (one dict per note) but no typed `note_intent_graph`. Project it
            # into one writer leaf per planned note — the native fan-out. Without
            # this the fallback below hands the WHOLE plan to a single per-leaf
            # writer, so an N-note plan silently produces ~1 note.
            execute_leaves = _project_planned_notes_to_leaves(plan_doc)
        if not isinstance(execute_leaves, list) or not execute_leaves:
            # Last-resort single whole-plan leaf (degenerate/malformed plan).
            execute_leaves = [dict(plan_doc)]
    # P13 (FZ 20k9c1a1a1b7c2e): static pre-flight BEFORE any backend call —
    # promotes the old no-silent-under-production WARNING to a fail-loud abort.
    # If the plan declares N notes but the wave collapsed to far fewer leaves (the
    # E11 single-whole-plan-leaf failure), or a planned note is unprojectable, or
    # two leaves target the same path, raise PreflightError so the defect surfaces
    # before N leaves of wasted work instead of silently under-producing.
    preflight = preflight_execute_wave(plan_doc, execute_leaves, compiled=compiled)
    if not preflight.ok:
        raise PreflightError(preflight)
    # FZ 20k9d2: enrich each note leaf with per-note relevance-ranked related
    # notes → the writer renders them into ## References → note_links edges.
    # No-op when related_notes_db is None (byte-identical to pre-fix).
    execute_leaves = _enrich_leaves_with_related_notes(
        execute_leaves, related_notes_db=related_notes_db
    )
    # FZ 20k9d1b1a1a (P4): stamp each note leaf with its NOTE-TYPE contract
    # (resolved from target_path → capture flavor → required sections) → the
    # writer renders {{leaf.type_contract_md}}. No-op ("" stamp) for a leaf whose
    # type can't be resolved; passthrough for the whole-plan fallback leaf.
    execute_leaves = _enrich_leaves_with_type_contract(execute_leaves)
    # P17: consult the execute skill's declared fallback_strategy — the field's
    # first live consumer. A `degrade` posture (the skill declares it tolerates
    # a degraded MCP result) NARROWS the breaker to abort only on a hard `auth`
    # wall, letting a soft rate_limit ride; `fail_fast`/`retry_then_fail`/no MCP
    # keep the default {auth, rate_limit}. The breaker is never disabled here —
    # a credential wall always aborts. No-op when no breaker is passed.
    effective_breaker = breaker
    if breaker is not None:
        posture = _execute_fallback_strategy(skills_dir)
        if posture == "degrade":
            effective_breaker = breaker.with_tripping_classes(frozenset({"auth"}))
    # P21-full: expose the plan's durable artifacts BY REFERENCE to the writer
    # leaves ({{artifact.plan_text}} etc.). The per-leaf projection already
    # inlines plan_text/source_excerpt into each leaf (the single-shot backend
    # has no file tool); the artifact channel is the additive by-reference path
    # a migrated skill can read from instead. Empty store → byte-identical.
    artifacts = execute_kwargs.pop("artifacts", None) or _build_artifact_store(plan_doc)
    return run_pipeline_dynamic(
        compiled,
        leaves=execute_leaves,
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
        max_workers=execute_max_workers,
        budget=budget,
        breaker=effective_breaker,
        artifacts=artifacts,
        context_assembler=context_assembler,
        cancellation_check=cancellation_check,
        effect_guard=effect_guard,
        effect_recorder=effect_recorder,
        **execute_kwargs,
    )


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
    budget: RunBudget | None = None,
    breaker: ErrorClassBreaker | None = None,
    context_assembler: ContextAssembler | None = None,
    related_notes_db: Path | str | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
    revision_recorder: Callable[[SignOffResult], None] | None = None,
    stop_after: str | None = None,
    max_review_rounds: int = 0,
    **execute_kwargs: Any,
) -> DigestionResult:
    """Run the native plan → augment → review → execute digestion pipeline.

    Args:
        skills_dir: Directory holding the four ``skill_tessellum_*`` phase
            skills (single-file canonicals with per-section contract blocks).
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
        revision_recorder: **P1 A1.5** — optional pass-through to
            :func:`~tessellum.composer.signoff.run_sign_off` that records a
            durable :class:`PlanRevision` decision for the review sign-off.
            Defaults to ``None`` → the shipped digestion path + its tests are
            byte-identical (the recording is strictly opt-in).
        execute_max_workers: Worker pool for the execute wave.
        stop_after: **M3** — if ``"review"``, return the APPROVED plan after
            the review→ready sign-off WITHOUT running the execute wave (a plan
            is *accepted* but not yet promoted). Used by the corpus sub-plan
            planning wave (:func:`run_corpus_planning_wave`), which plans each
            sub-objective to an accepted plan_doc here, then M4 executes them as
            separate transactions. ``None`` (default) → the shipped
            plan→augment→review→execute behavior is byte-identical.
        max_review_rounds: **P15 (FZ 20k9c1a1a1b7c2h)** — the review-revise loop
            budget. When ``>0``, a review that returns ``not ready`` re-runs
            ``augment → review`` with the review's ``failures`` injected as
            ``leaf["review_failures"]``, up to this many extra rounds, so a
            plan-quality rejection IMPROVES the plan instead of halting. Stops
            early on ``ready`` or when a round fails to shrink the failure set
            (non-convergence → escalate the residual to sign-off). ``0``
            (default) → the original single plan→augment→review pass
            (byte-identical). A framework error in any phase always halts,
            regardless of this budget.
        **execute_kwargs: Forwarded to :func:`run_pipeline_dynamic` for the
            execute phase (e.g. ``close_gate``, ``manifest``, ``budget``,
            ``wave_gate``, ``informed_fixer``).

    Returns:
        A :class:`DigestionResult`. The pipeline stops early (``execute``
        not run) on any linear-phase error or a sign-off rejection, or when
        ``stop_after="review"`` and sign-off approved (``completed=True``,
        ``stopped_at="review_accepted"``).
    """
    if stop_after not in (None, "review"):
        raise ValueError(
            f"stop_after must be None or 'review', got {stop_after!r}"
        )
    skills_dir = Path(skills_dir)
    policy = sign_off_policy or SignOffPolicy(use_agent=False, use_human=False)
    phases: list[PhaseOutcome] = []
    plan_doc: dict[str, Any] = dict(source_leaf)
    # M0: the plan skill references {{leaf.member_count}} / {{leaf.members}}
    # unconditionally; a leaf lacking them is a corpus of one. Default here at
    # the pipeline chokepoint so EVERY caller is sentinel-free, not just the
    # current producers (runtime executor / CLI / build_corpus_leaf). No-op when
    # the keys are already present → byte-identical prompts for those callers.
    plan_doc.setdefault("member_count", 1)
    plan_doc.setdefault("members", [])
    # M0 review (medium): a corpus_wide {{leaf.X}} that now resolves (the
    # _corpus_leaf fix) can render a large value — e.g. {{leaf.members}} /
    # {{leaf.source_refs}} — that, with NO assembler, trips the executor's
    # HARD_PROMPT_CAP_CHARS and HALTS the linear plan/augment/review phase
    # instead of degrading. Default a head+tail WindowedAssembler sized just
    # under the hard cap so an oversized rendered prompt truncates + warns
    # (the executor's documented fail-soft) rather than erroring. A caller that
    # passes its own assembler (the runtime executor does) is untouched.
    if context_assembler is None:
        context_assembler = WindowedAssembler(max_chars=HARD_PROMPT_CAP_CHARS - 4_096)

    # ── Linear phases: plan → (augment → review)[×revise] ───────────────────
    # P15 (FZ 20k9c1a1a1b7c2h): the review is a plan-quality IMPROVER, not just a
    # gate. `plan` runs once; then `augment → review` repeats while the review
    # verdict is `not ready` and rounds remain, each re-augment pass conditioned
    # on the prior review's `failures` (injected as leaf["review_failures"]) so
    # the LLM fixes exactly the flagged gaps. A framework error in any phase still
    # halts immediately (that is a bug, not a plan-quality signal). Same-failure
    # short-circuit: if a round doesn't shrink the failure set, stop (the LLM
    # isn't converging) and let sign-off escalate the residual. `max_review_rounds
    # =0` → the original single-pass behaviour (byte-identical).
    review_rounds = 0
    review_failures: list = []
    # P20: if the caller set a runs_dir for the execute wave, use it for the
    # linear phases too so all four phases emit the same per-step trace.
    linear_runs_dir = execute_kwargs.get("runs_dir")

    def _run_one_phase(phase: str, leaf: dict) -> RunResult | None:
        """Run one linear phase; append its outcome; merge + normalize. Returns
        the RunResult, or None if it errored (caller returns a halt result)."""
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError(f"digestion cancelled before {phase}")
        # P21-full: inject the durable artifacts (plan_text / source_excerpt /
        # planned_notes) accumulated so far BY REFERENCE, so a phase reads
        # {{artifact.plan_text}} instead of a prior step re-emitting the body.
        # Built from the already-normalized plan_doc; empty on the first (plan)
        # phase → byte-identical to pre-P21 for a prompt with no {{artifact.X}}.
        run = _run_phase_linear(
            PHASE_SKILLS[phase], skills_dir=skills_dir, leaf=leaf, backend=backend,
            vault_root=vault_root, dry_run=dry_run, budget=budget,
            context_assembler=context_assembler, cancellation_check=cancellation_check,
            effect_guard=effect_guard, effect_recorder=effect_recorder,
            runs_dir=linear_runs_dir, artifacts=_build_artifact_store(plan_doc),
        )
        phases.append(
            PhaseOutcome(phase=phase, ran=True, error_count=run.error_count, run=run)
        )
        plan_doc.update(_collect_structured(run))
        _normalize_plan_doc_keys(plan_doc)
        return None if run.error_count else run

    def _halt(phase: str) -> DigestionResult:
        return DigestionResult(
            completed=False, stopped_at=phase, sign_off=None,
            phases=tuple(phases), plan_doc=plan_doc, review_rounds=review_rounds,
        )

    # plan (once)
    if _run_one_phase("plan", dict(plan_doc)) is None:
        return _halt("plan")

    # augment → review, with the P15 revise loop
    # P24 (FZ 20k9c1a1a1b7c2h/g): revert-to-BEST — the same safety property
    # fix.py's run_fix_loop has and P15 originally lacked. The loop mutates
    # plan_doc in place each round; without this, a REGRESSING re-augment (round N
    # yields MORE failures than N-1) would leave the worse plan as the final state
    # sent to sign-off. We snapshot the best (fewest-failures) plan_doc across
    # rounds and restore it if the final round regressed. "Best" score = failure
    # count (0 = ready); lower is better.
    best_plan_doc: dict | None = None
    best_failure_count: int | None = None

    def _score(failures: list) -> int:
        return len(failures)

    while True:
        aug_leaf = dict(plan_doc)
        if review_failures:
            # P15.2: condition the re-augment on the prior review's specific gaps.
            aug_leaf["review_failures"] = "\n".join(f"- {f}" for f in review_failures)
        if _run_one_phase("augment", aug_leaf) is None:
            return _halt("augment")
        if _run_one_phase("review", dict(plan_doc)) is None:
            return _halt("review")

        ready, failures = _review_verdict(plan_doc)
        # P24 revert-to-BEST: remember the best plan_doc seen so far.
        if best_failure_count is None or _score(failures) < best_failure_count:
            best_failure_count = _score(failures)
            best_plan_doc = dict(plan_doc)
        if ready or review_rounds >= max_review_rounds:
            break
        # Same-failure short-circuit: a round that doesn't shrink the failure set
        # (the LLM isn't converging) stops the loop and lets sign-off escalate.
        if review_failures and len(failures) >= len(review_failures):
            break
        review_failures = failures
        review_rounds += 1

    # P24: if the final round regressed below the best seen, restore BEST so a
    # worse plan is never what sign-off (and any downstream execute) judges.
    if (
        best_plan_doc is not None
        and best_failure_count is not None
        and _score(_review_verdict(plan_doc)[1]) > best_failure_count
    ):
        plan_doc.clear()
        plan_doc.update(best_plan_doc)

    # ── review → ready sign-off gate ────────────────────────────────────────
    # Program rung = plan-structure pre-filter AND the review skill's typed
    # verdict (both must pass); agent/human rungs per policy.
    plan_gate = build_plan_gate()

    def _program_gate() -> tuple[bool, str | None]:
        composite = plan_gate.evaluate(plan_doc)
        if not composite.passed:
            return False, composite.first_failure_cause or "plan_structure"
        # The review phase's typed {ready, failures} verdict (shared reader so the
        # gate and the P15 revise loop agree). After the loop, this is the FINAL
        # round's verdict — still not-ready only if the loop exhausted its rounds
        # or couldn't converge, in which case sign-off escalates the residual.
        ready, failures = _review_verdict(plan_doc)
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
        revision_recorder=revision_recorder,
    )
    if sign_off.decision != "approved":
        # Rejected / needs_human → do NOT spend the execution wave. If the P15
        # revise loop ran (review_rounds>0), this is the residual after the round
        # budget was exhausted / convergence stalled — escalated, not ignored.
        return DigestionResult(
            completed=False,
            stopped_at="review",
            sign_off=sign_off,
            phases=tuple(phases),
            plan_doc=plan_doc,
            review_rounds=review_rounds,
        )

    if stop_after == "review":
        # M3: the plan is ACCEPTED but not executed — the corpus planning wave
        # captures this accepted plan_doc and M4 executes it as its own
        # transaction. completed=True marks a clean accepted plan (distinct from
        # a sign-off rejection above, which is completed=False).
        return DigestionResult(
            completed=True,
            stopped_at="review_accepted",
            sign_off=sign_off,
            phases=tuple(phases),
            plan_doc=plan_doc,
            review_rounds=review_rounds,
        )

    # ── execute: the fan-out wave (one leaf per planned note) ───────────────
    if cancellation_check is not None and cancellation_check():
        raise InterruptedError("digestion cancelled before execute")
    try:
        execute_run = run_execute_wave(
            plan_doc,
            skills_dir=skills_dir,
            backend=backend,
            vault_root=vault_root,
            dry_run=dry_run,
            execute_max_workers=execute_max_workers,
            budget=budget,
            breaker=breaker,
            context_assembler=context_assembler,
            related_notes_db=related_notes_db,
            cancellation_check=cancellation_check,
            effect_guard=effect_guard,
            effect_recorder=effect_recorder,
            **execute_kwargs,
        )
    except PreflightError:
        # P13: the plan failed the pre-dispatch coherence check — abort loud with
        # ZERO notes written, preserving the always-returns-a-DigestionResult
        # contract (a headless caller branches on stopped_at + the message).
        phases.append(PhaseOutcome(phase="execute", ran=False, error_count=1))
        return DigestionResult(
            completed=False,
            stopped_at="execute_preflight",
            sign_off=sign_off,
            phases=tuple(phases),
            plan_doc=plan_doc,
            under_produced=True,
            review_rounds=review_rounds,
        )
    phases.append(
        PhaseOutcome(
            phase="execute",
            ran=True,
            error_count=execute_run.error_count,
            run=execute_run,
        )
    )

    # Under-production signal (FZ 20k9c1a1a1b7c2g): the execute wave's leaves are
    # the writer leaves (one per note), so fewer leaves than the plan declared is
    # the silent single-whole-plan-leaf failure. run_execute_wave already warns;
    # this surfaces it on the result so a headless orchestrator can branch on it.
    declared = _declared_note_count(plan_doc)
    under_produced = declared > 1 and len(execute_run.leaves) < declared

    return DigestionResult(
        completed=execute_run.error_count == 0,
        stopped_at=None if execute_run.error_count == 0 else "execute",
        sign_off=sign_off,
        phases=tuple(phases),
        plan_doc=plan_doc,
        under_produced=under_produced,
        review_rounds=review_rounds,
    )


__all__ = [
    "PHASE_SKILLS",
    "PhaseOutcome",
    "DigestionResult",
    "PreflightResult",
    "PreflightError",
    "preflight_execute_wave",
    "run_execute_wave",
    "run_digestion_pipeline",
]
