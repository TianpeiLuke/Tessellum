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

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ContextManager

from tessellum.composer.compiler import HARD_PROMPT_CAP_CHARS, compile_skill
from tessellum.composer.context_assembler import ContextAssembler, WindowedAssembler
from tessellum.composer.credential_pool import RunBudget
from tessellum.composer.gates import build_plan_gate
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
            ``stop_after="review"`` approved (M3); ``None`` when it fully
            executed to completion.
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
    budget: RunBudget | None,
    context_assembler: ContextAssembler | None,
    cancellation_check: Callable[[], bool] | None,
    effect_guard: Callable[[], ContextManager[None]] | None,
    effect_recorder: Callable[[Path], None] | None,
) -> RunResult:
    """Compile + run one skill as a single linear phase over ``leaf``."""
    compiled = compile_skill(skills_dir / f"{skill_name}.md")
    return run_pipeline(
        compiled,
        leaves=[leaf],
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
        budget=budget,
        context_assembler=context_assembler,
        cancellation_check=cancellation_check,
        effect_guard=effect_guard,
        effect_recorder=effect_recorder,
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


# The plan-structure gate (gates.plan_structure_predicate) and the augment/review
# skill prompts read the canonical keys ``plan_path`` / ``plan_text`` /
# ``total_notes``, but the plan skill's steps emit the write-plan materializer's
# ``output_path`` / ``body_markdown`` and a note count under
# ``planned_note_count`` / ``estimated_note_count``. Without bridging, the gate
# reads ``total_notes=0`` + ``plan_path=<missing>`` and rejects every plan, and
# the augment/review prompts render a ``<missing leaf.plan_path>`` sentinel. This
# maps the produced keys to the canonical names the gate + downstream steps read,
# in-place, never clobbering a value the plan already set under the canonical key.
_PLAN_DOC_KEY_ALIASES: dict[str, tuple[str, ...]] = {
    "plan_path": ("output_path",),
    "plan_text": ("body_markdown",),
    "total_notes": ("planned_note_count", "estimated_note_count"),
}


def _normalize_plan_doc_keys(plan_doc: dict[str, Any]) -> None:
    """Bridge plan-skill output keys to the canonical names the gate + augment/
    review steps consume. Mutates ``plan_doc`` in place; idempotent; only fills a
    canonical key that is absent or empty, from the first present alias."""
    for canonical, aliases in _PLAN_DOC_KEY_ALIASES.items():
        cur = plan_doc.get(canonical)
        if cur not in (None, "", 0):
            continue
        for alias in aliases:
            val = plan_doc.get(alias)
            if val not in (None, "", 0):
                plan_doc[canonical] = val
                break


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


def run_execute_wave(
    plan_doc: dict,
    *,
    skills_dir: Path | str,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    execute_max_workers: int = 4,
    budget: RunBudget | None = None,
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
    # No-silent-under-production backstop (FZ 20k9c1a1a1b7c2b): if the plan
    # declares N notes but the wave is about to fan out to far fewer leaves, that
    # is the single-whole-plan-leaf failure mode — surface it loudly rather than
    # silently writing ~1 note for an N-note plan.
    declared = plan_doc.get("total_notes") or len(plan_doc.get("planned_notes") or [])
    if isinstance(declared, int) and declared > 1 and len(execute_leaves) < declared:
        import warnings

        warnings.warn(
            f"execute wave fanned out to {len(execute_leaves)} leaf(es) but the "
            f"plan declares {declared} notes — the pipeline may under-produce. "
            f"Expected one writer leaf per planned note "
            f"(planned_notes projection / note_intent_graph).",
            RuntimeWarning,
            stacklevel=2,
        )
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
    return run_pipeline_dynamic(
        compiled,
        leaves=execute_leaves,
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
        max_workers=execute_max_workers,
        budget=budget,
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
    context_assembler: ContextAssembler | None = None,
    related_notes_db: Path | str | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
    revision_recorder: Callable[[SignOffResult], None] | None = None,
    stop_after: str | None = None,
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

    # ── Linear phases: plan → augment → review ──────────────────────────────
    for phase in ("plan", "augment", "review"):
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError(f"digestion cancelled before {phase}")
        run = _run_phase_linear(
            PHASE_SKILLS[phase],
            skills_dir=skills_dir,
            leaf=dict(plan_doc),
            backend=backend,
            vault_root=vault_root,
            dry_run=dry_run,
            budget=budget,
            context_assembler=context_assembler,
            cancellation_check=cancellation_check,
            effect_guard=effect_guard,
            effect_recorder=effect_recorder,
        )
        phases.append(
            PhaseOutcome(phase=phase, ran=True, error_count=run.error_count, run=run)
        )
        plan_doc.update(_collect_structured(run))
        _normalize_plan_doc_keys(plan_doc)
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
        revision_recorder=revision_recorder,
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
        )

    # ── execute: the fan-out wave (one leaf per planned note) ───────────────
    if cancellation_check is not None and cancellation_check():
        raise InterruptedError("digestion cancelled before execute")
    execute_run = run_execute_wave(
        plan_doc,
        skills_dir=skills_dir,
        backend=backend,
        vault_root=vault_root,
        dry_run=dry_run,
        execute_max_workers=execute_max_workers,
        budget=budget,
        context_assembler=context_assembler,
        related_notes_db=related_notes_db,
        cancellation_check=cancellation_check,
        effect_guard=effect_guard,
        effect_recorder=effect_recorder,
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
    "run_execute_wave",
    "run_digestion_pipeline",
]
