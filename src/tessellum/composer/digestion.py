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
import hashlib
import json
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ContextManager

from tessellum.composer.compiler import (
    HARD_PROMPT_CAP_CHARS,
    CompiledPipeline,
    compile_skill,
)
from tessellum.composer.context_assembler import ContextAssembler, WindowedAssembler
from tessellum.composer.contracts import (
    _ARTIFACT_KEYS,
    ArtifactRef,
    PlanDoc,
    mandatory_section_stems,
)
from tessellum.composer.credential_pool import ErrorClassBreaker, RunBudget
from tessellum.composer.executor import (
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_TRUNCATION_BASE_TOKENS,
    MAX_TRUNCATION_CEILING_TOKENS,
    _stringify,
    upstream_placeholder_keys,
)
from tessellum.composer.gates import (
    PLAN_NOTE_MAX_WORDS,
    PLAN_OVERSPLIT_MIN_WORDS,
    build_plan_gate,
    duplicate_target_predicate,
)
from tessellum.composer.knowledge_plan import (
    NoteIntentGraph,
    project_note_intent_graph,
)
from tessellum.composer.llm import LLMBackend
from tessellum.composer.note_coverage import (
    extend_wave_gate_with_note_coverage,
    extract_headings,
)
from tessellum.composer.note_coverage import name_match as nc_name_match
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
        run_id: The run identity this pipeline invocation carried (A0, FZ
            20k9c1a1a1b7c2k1a) — the ``run_id`` named param, or the
            pre-existing ``execute_kwargs["run_id"]`` calling convention when
            that was used instead. ``None`` when the caller supplied neither
            (byte-identical pre-A0 behaviour).
    """

    completed: bool
    stopped_at: str | None
    sign_off: SignOffResult | None
    phases: tuple[PhaseOutcome, ...]
    plan_doc: dict = field(default_factory=dict)
    under_produced: bool = False
    review_rounds: int = 0
    run_id: str | None = None
    contradicted_failures: tuple[str, ...] = ()


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


_FENCE_RE = re.compile(r"^```", re.MULTILINE)


def compute_source_ledger(members: list) -> list[dict[str, Any]]:
    """The CODE-COMPUTED source ledger (issue 11, FZ 20k9c1a1a1b7c2k1a1b).

    The eval runs proved the model-"measured" ``pages[]`` is an estimate that
    varies run to run (r3 said 3,150 words where ``wc -w`` says 2,919), so
    every downstream consumer inherited a guess. This computes the ledger
    deterministically from the members' inline text — one code-owned
    convention: ``measured_words`` = whitespace-token count,
    ``code_blocks`` = fence-pair count, ``headings`` = H1–H3 lines in order.
    Members without inline text contribute no ledger row (fail-soft — a
    URL-only member cannot be measured here and must not be guessed at).
    """
    ledger: list[dict[str, Any]] = []
    for m in members or []:
        if not isinstance(m, dict):
            continue
        text = m.get("excerpt") or m.get("source_content") or ""
        if not isinstance(text, str) or not text.strip():
            continue
        fences = len(_FENCE_RE.findall(text))
        ledger.append({
            "url": m.get("source_url") or m.get("url") or m.get("source_id") or "",
            "source_id": m.get("source_id") or m.get("name") or "",
            "measured_words": len(text.split()),
            "code_blocks": fences // 2,
            # F12: fence-aware — an in-fence `# comment` is code, not a
            # heading; the fence-blind regex inflated the ledger (21 of 67
            # on the mcp corpus) and PLAN-006 then demanded coverage of
            # pseudo-headings.
            "headings": extract_headings(text),
        })
    return ledger


def slim_plan_doc(plan_doc: dict[str, Any]) -> dict[str, Any]:
    """A shallow, dump-friendly copy of ``plan_doc`` without the bulky inline
    source bytes (A1.2/A1.5, FZ 20k9c1a1a1b7c2k1a).

    Drops ``source_content``, each ``members[].excerpt``, and (A3.1) the
    joined ``source_excerpt`` — the source bytes are already durable elsewhere
    (the runtime's ``source_leaf.json`` / spool; the CLI's ``--source`` file;
    the excerpt is paged to the durable artifact store with its digest
    recorded in ``plan.json``'s ``_artifact_refs``, from which promote
    restores it verified), so re-serializing them into every checkpoint and
    ``plan.json`` just multiplies durable copies of the same payload (the
    dedup smell the vault-memory design removes). Every other key passes
    through by reference; member dicts keep their metadata (``source_id``,
    ``source_url``, …). Pure — never mutates the input.
    """
    slim = {
        k: v for k, v in plan_doc.items()
        if k not in ("source_content", "source_excerpt")
    }
    members = slim.get("members")
    if isinstance(members, list):
        slim["members"] = [
            {k: v for k, v in m.items() if k != "excerpt"} if isinstance(m, dict) else m
            for m in members
        ]
    return slim


def _checkpoint_plan_doc(
    runs_dir: Path | str, seq: int, phase: str, plan_doc: dict[str, Any]
) -> None:
    """A1.2 (FZ 20k9c1a1a1b7c2k1a): durably snapshot the plan-of-record after a
    phase fold — ``<runs_dir>/checkpoints/<NN>_<phase>.json``, atomic
    (tmp+rename), slimmed via :func:`slim_plan_doc`. Fail-soft: checkpointing
    is episodic recording and must never fail the run. Opt-in via the existing
    ``runs_dir`` seam (P20) — no ``runs_dir``, no checkpoints, byte-identical.
    """
    try:
        cp_dir = Path(runs_dir) / "checkpoints"
        cp_dir.mkdir(parents=True, exist_ok=True)
        name = f"{seq:02d}_{phase}.json"
        tmp = cp_dir / (name + ".tmp")
        tmp.write_text(
            json.dumps(slim_plan_doc(plan_doc), indent=2, sort_keys=True, default=str)
            + "\n",
            encoding="utf-8",
        )
        tmp.replace(cp_dir / name)
    except Exception:
        pass


def load_latest_checkpoint(
    runs_dir: Path | str,
) -> tuple[int, str, dict[str, Any]] | None:
    """Phase 4 (FZ 20k9c1a1a1b7c2k2a3a): the read side of A1.2 — the
    highest-sequence checkpoint under ``<runs_dir>/checkpoints/``, as
    ``(seq, phase, plan_doc)``, or ``None`` when there is nothing to resume.

    Fail-soft mirror of the writer: an unreadable/corrupt checkpoint file is
    skipped (the next-best one wins), never an error — resume is an
    optimization and the caller can always start fresh."""
    cp_dir = Path(runs_dir) / "checkpoints"
    best: tuple[int, str, dict[str, Any]] | None = None
    try:
        candidates = sorted(cp_dir.glob("*_*.json"))
    except OSError:
        return None
    for path in candidates:
        stem = path.stem
        seq_s, _, phase = stem.partition("_")
        if not (seq_s.isdigit() and phase):
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(doc, dict):
            continue
        seq = int(seq_s)
        if best is None or seq > best[0]:
            best = (seq, phase, doc)
    return best


def _build_artifact_store(
    plan_doc: dict[str, Any], durable_dir: Path | None = None
) -> dict[str, Any]:
    """The by-reference artifact store the driver injects into each phase's
    prompts (P21-full; FZ 20k9c1a1a1b7c2j). Snapshots the current durable value
    of each allowlisted artifact key (``_ARTIFACT_KEYS``) from the — already
    ``_normalize_plan_doc_keys``-normalized — ``plan_doc``, so a consumer reads
    ``{{artifact.plan_text}}`` by reference instead of a prior step re-emitting
    it. Only present, non-empty values are included (an absent key → a
    ``<missing artifact.X>`` sentinel at render, same debug affordance as
    ``{{leaf.X}}``).

    A2 (FZ 20k9c1a1a1b7c2k1a): with ``durable_dir`` set, each artifact is
    ALSO paged to disk — serialized with the executor's own stringifier
    (byte-identical prompt text on deref), written atomically to
    ``<durable_dir>/<key>``, and the store carries an :class:`ArtifactRef`
    instead of the value. Latest-write-wins per phase: the file always holds
    the CURRENT of-record value. Fail-soft per artifact: if the durable write
    fails, the in-RAM value is kept (correctness preserved, durability
    degraded) — while a corrupted durable READ stays loud
    (:class:`ArtifactIntegrityError` at deref)."""
    store: dict[str, Any] = {}
    for key in _ARTIFACT_KEYS:
        val = plan_doc.get(key)
        if val in (None, "", [], ()):
            continue
        if durable_dir is None:
            store[key] = val
            continue
        try:
            payload = _stringify(val).encode("utf-8")
            durable_dir.mkdir(parents=True, exist_ok=True)
            target = durable_dir / key
            # Unique tmp per write (review finding 5): concurrent builders
            # sharing a dir must never interleave on one tmp path.
            tmp = durable_dir / f".{key}.{uuid.uuid4().hex[:8]}.tmp"
            tmp.write_bytes(payload)
            tmp.replace(target)
            store[key] = ArtifactRef(
                path=target,
                sha256=hashlib.sha256(payload).hexdigest(),
                size=len(payload),
            )
        except Exception:
            # Fail-soft to the in-RAM value — and best-effort remove any STALE
            # durable bytes from a prior phase (review finding 7), so the file
            # never silently misrepresents the of-record value.
            try:
                (durable_dir / key).unlink(missing_ok=True)
            except Exception:
                pass
            store[key] = val
    return store


def page_plan_artifacts(
    plan_doc: dict[str, Any], durable_dir: Path
) -> dict[str, Any]:
    """J2 (FZ 20k9c1a1a1b7c2k2): the public persist seam for runtime callers —
    page the FINAL plan-of-record's heavy fields (``_ARTIFACT_KEYS``) to the
    durable store and return the store dict (an :class:`ArtifactRef` per
    successfully paged key; the raw in-RAM value where the durable write
    fail-softed). The runtime executor records the returned refs' digests in
    ``plan.json`` as ``_artifact_refs`` so promote can prove the bytes it
    executes are the bytes the human approved."""
    return _build_artifact_store(plan_doc, durable_dir)


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


_ORPHAN_CLAIM_RE = re.compile(
    r"orphan|unmapped|absent from the (coverage )?map|missing from the (coverage )?map"
    r"|not (mapped|covered)|coverage map is (materially )?incomplete",
    re.IGNORECASE,
)

# E3.3: failures attributed to the QUALITATIVE checkpoints (CP5 derivation
# faithfulness, CP6 borderline atomicity) — advisory-until-calibrated. The
# review skill's failure strings are CP-prefixed by its own contract.
_ADVISORY_CLAIM_RE = re.compile(r"(?i)^cp[56]\b")

# E3.1 (FZ 20k9c1a1a1b7c2k1a1b1): the figure-mismatch claim domain — dropped
# only when EVERY ledger figure is verbatim-present in the plan text.
# Review F3: the domain is LEDGER-scoped — the claim must reference the
# measured/ledger/source-page figures, so a genuine per-note density or
# summary-statistics critique (not checkable against page figures) is never
# dropped by page-figure presence.
_FIGURE_CLAIM_RE = re.compile(
    r"(measured|ledger|source[ -]pages?)"
    r".{0,120}?(mismatch|outside tolerance|understat|overstat|far (below|above)|does not match|incorrect)"
    r"|(word.count|figures?)"
    r".{0,80}?(outside tolerance|understat|overstat)"
    r".{0,80}?(measured|ledger)",
    re.IGNORECASE | re.DOTALL,
)
def _figure_present(figure: int, text: str) -> bool:
    """Digit-boundary AND thousands-separator-tolerant figure match (J3
    finding 3, FZ 20k9c1a1a1b7c2k2): the ledger says ``12813``, a
    human-formatted plan writes ``12,813`` — run 3's revise loop exhausted on
    exactly that, the exhibit reporting the reconciled figure NOT FOUND. The
    CODE side absorbs the rendering; a reviewer must never reject over a
    comma. Boundary guards preserved (review F7: ``10`` must not match inside
    ``2100``)."""
    pattern = r"(?<!\d)" + r",?".join(str(figure)) + r"(?!\d)"
    return bool(re.search(pattern, text))


def _figures_all_present(plan_doc: dict) -> bool:
    """Every code-measured page figure appears — boundary-matched and
    separator-tolerant (:func:`_figure_present`) — in the plan text."""
    pages = plan_doc.get("pages")
    plan_text = plan_doc.get("plan_text") or ""
    if not isinstance(pages, list) or not isinstance(plan_text, str) or not plan_text:
        return False
    figs = [
        pg.get("measured_words") for pg in pages
        if isinstance(pg, dict) and isinstance(pg.get("measured_words"), int)
    ]
    return bool(figs) and all(_figure_present(f, plan_text) for f in figs)


def _norm_heading(s: object) -> str:
    return " ".join(str(s).lower().split())


def compute_coverage_orphans(plan_doc: dict) -> list[str] | None:
    """The deterministic coverage set-difference (issue 9, FZ
    20k9c1a1a1b7c2k1a1b): ledger headings (``pages[].headings``) MINUS the
    sections the ``section_coverage_map`` names — normalized exact OR
    substring-either-way match (the same leniency an honest reviewer applies).
    Returns ``None`` when either side is absent/non-list (nothing computable —
    callers must not treat that as "zero orphans")."""
    pages = plan_doc.get("pages")
    cmap = plan_doc.get("section_coverage_map")
    if not isinstance(pages, list) or not isinstance(cmap, list):
        return None
    ledger = [
        str(h).strip()
        for pg in pages if isinstance(pg, dict)
        for h in (pg.get("headings") or []) if str(h).strip()
    ]
    if not ledger:
        return None
    mapped = {
        _norm_heading(r.get("source_section", ""))
        for r in cmap if isinstance(r, dict)
    }
    mapped.discard("")
    orphans = []
    for h in ledger:
        n = _norm_heading(h)
        if n in mapped or any(n in m or m in n for m in mapped):
            continue
        orphans.append(h)
    return orphans


def compute_assessment_violations(plan_doc: dict) -> list[str] | None:
    """R4.1 (FZ 20k9c1a1a1b7c2k2a1d): deterministic cross-checks of
    LLM-emitted ASSESSMENTS against the artifacts they describe — the
    schema-valid-fabrication defense (J3's F2 round 1 PASSED by fabricating a
    plausible draft assessment from nothing; gates that validate shape can
    never catch well-formed output about nothing).

    Checks (all lenient-normalized, the same tolerance the coverage orphans
    use — the F3 lesson says the CODE side absorbs rendering variance):

    - ``sections_present`` claims ⊆ the REAL H2 scan of ``plan_text``;
    - coverage-map rows name only REAL ledger headings (invented sections);
    - ``plan_structure == "master"`` requires a Sub-Plans Index in the text.

    Returns ``None`` when nothing is computable (no plan_text), else the
    violation list. Rendered as the ASSESSMENTS exhibit — the reviewer
    judges over it; promotion to a ladder-blocking error is the E3.3
    advisory-vs-gating decision, not this function's."""
    plan_text = plan_doc.get("plan_text")
    if not isinstance(plan_text, str) or not plan_text:
        return None
    violations: list[str] = []
    real_h2 = {_norm_heading(h) for h in re.findall(r"(?m)^##\s+(.+)$", plan_text)}
    claimed = plan_doc.get("sections_present")
    if isinstance(claimed, list) and claimed and real_h2:
        for c in claimed:
            n = _norm_heading(c)
            if not n:
                continue
            if n in real_h2 or any(n in h or h in n for h in real_h2):
                continue
            violations.append(
                f"sections_present claims {str(c)!r} but no matching H2 "
                f"exists in plan_text"
            )
    if plan_doc.get("_pages_code_measured"):
        ledger = {
            _norm_heading(h)
            for pg in (plan_doc.get("pages") or []) if isinstance(pg, dict)
            for h in (pg.get("headings") or [])
        }
        cmap = plan_doc.get("section_coverage_map")
        if isinstance(cmap, list) and ledger:
            for row in cmap:
                if not isinstance(row, dict):
                    continue
                sec = _norm_heading(row.get("source_section", ""))
                if not sec:
                    continue
                if sec in ledger or any(sec in h or h in sec for h in ledger):
                    continue
                violations.append(
                    f"coverage map names {row.get('source_section')!r} which "
                    f"is NOT a measured source heading (invented section)"
                )
    if plan_doc.get("plan_structure") == "master" and "sub-plans index" not in plan_text.lower():
        violations.append(
            "plan_structure claims 'master' but plan_text has no "
            "Sub-Plans Index table"
        )
    return violations


def compute_review_exhibits(plan_doc: dict) -> str:
    """Render the deterministic review EXHIBITS (issue 9 / mechanism 1 of FZ
    20k9c1a1a1b7c2k1a1b): quantities the driver computes exactly, injected so
    the reviewer JUDGES over them instead of re-counting (an LLM re-count of a
    long text confabulates — the r3 false rejection). SECTIONS/GATES render
    from ``plan_text`` alone, so any plan-carrying run gets exhibits; only a
    plan-less doc renders the empty string."""
    parts: list[str] = []
    orphans = compute_coverage_orphans(plan_doc)
    if orphans is not None:
        pages = [pg for pg in plan_doc.get("pages", []) if isinstance(pg, dict)]
        total_headings = sum(len(pg.get("headings") or []) for pg in pages)
        rows = plan_doc.get("section_coverage_map") or []
        parts.append(
            f"COVERAGE (computed): ledger headings={total_headings}, "
            f"coverage-map rows={len(rows)}, UNMAPPED={len(orphans)}"
            + (f" -> {orphans}" if orphans else " (every ledger heading is mapped)")
        )
        plan_text = plan_doc.get("plan_text") or ""
        fig = []
        for pg in pages:
            mw = pg.get("measured_words")
            if isinstance(mw, int):
                fig.append(
                    f"{pg.get('source_id') or pg.get('url') or '?'}: measured_words={mw} "
                    f"{'PRESENT' if _figure_present(mw, plan_text) else 'NOT FOUND'} in plan_text"
                )
        if fig:
            parts.append("FIGURES (computed): " + "; ".join(fig))
        # ASSESSMENTS (R4.1, FZ 20k9c1a1a1b7c2k2a1d): fabrication defense —
        # LLM assessments cross-checked against the artifacts they describe.
        assess = compute_assessment_violations(plan_doc)
        if assess is not None:
            parts.append(
                "ASSESSMENTS (computed): "
                + (f"{len(assess)} mismatch(es) between emitted assessments "
                   f"and the artifacts they describe -> {assess}"
                   if assess else
                   "all cross-checked assessment fields consistent with the artifacts")
            )
    plan_text = plan_doc.get("plan_text") or ""
    if isinstance(plan_text, str) and plan_text:
        # SECTIONS — the deterministic scan against the single-sourced list
        # (E1.1/E1.3): the P7 residual and the E18 "section absent" false-
        # reject class are both countable, so code counts them.
        low = plan_text.lower()
        present, absent = [], []
        for stem in mandatory_section_stems():
            (present if stem.lower() in low else absent).append(stem)
        n_all = len(present) + len(absent)
        passes = len(present) >= 0.9 * n_all  # the eval P7 threshold
        parts.append(
            f"SECTIONS (computed): {len(present)}/{n_all} mandatory sections "
            f"present — {'MEETS' if passes else 'BELOW'} the >=90% threshold"
            + (f"; stems not found: {absent} (section NAMES vary by "
               f"convention — judge whether an equivalent section exists "
               f"under another name before failing)" if absent else "")
        )
        # GATES — distinct G1–G8 tokens named anywhere in the plan.
        gates = sorted(set(re.findall(r"\bG[1-8]\b", plan_text)))
        missing_gates = [g for g in ("G1","G2","G3","G4","G5","G6","G7","G8") if g not in gates]
        parts.append(
            f"GATES (computed): {len(gates)}/8 distinct gate tokens named"
            + (f"; MISSING: {missing_gates}" if missing_gates else " (G1-G8 all named)")
        )
    # INVENTORY — the one-inventory parity (the r4 18-vs-8 class).
    notes = plan_doc.get("planned_notes")
    if isinstance(notes, (list, tuple)) and notes:
        total = plan_doc.get("total_notes")
        table_rows = None
        if isinstance(plan_text, str) and plan_text:
            # score.py's exact convention (review F6): H2-anchored/terminated.
            m = re.search(r"(?mi)^##\s+Planned Notes", plan_text)
            if m:
                rest = plan_text[m.end():]
                nxt = re.search(r"(?m)^##\s+", rest)
                section = rest[: nxt.start()] if nxt else rest
                table_rows = len(re.findall(r"(?m)^\|\s*\d+\s*\|", section))
        parts.append(
            f"INVENTORY (computed): planned_notes list={len(notes)}, "
            f"total_notes={total}"
            + (f", Planned-Notes table rows={table_rows}" if table_rows is not None else "")
            + (" — MISMATCH (one inventory expected)"
               if (isinstance(total, int) and total != len(notes)
                   and plan_doc.get("plan_shape") != "master_plus_subplans")
               or (table_rows is not None and table_rows != len(notes))
               else " (consistent)")
        )
        # DENSITY — per-note declared words vs the gate band.
        words = sorted(
            w for n in notes if isinstance(n, dict)
            for w in [n.get("approx_words")] if isinstance(w, int) and w > 0
        )
        if words:
            mid = words[len(words) // 2]
            parts.append(
                f"DENSITY (computed): approx_words min={words[0]} median={mid} "
                f"max={words[-1]} over {len(words)} notes "
                f"(ceiling {PLAN_NOTE_MAX_WORDS}, over-split floor "
                f"{PLAN_OVERSPLIT_MIN_WORDS})"
            )
        # BALANCE (W1.3, FZ k2a4) — per-note OWNED-SPAN size: the run-13
        # residual (a note owning 17 sections dilutes at cap). Advisory:
        # the reviewer judges over it; PLAN-010 warns at 2× the ceiling.
        cmap = plan_doc.get("section_coverage_map")
        source = plan_doc.get("source_excerpt")
        if isinstance(cmap, list) and cmap and isinstance(source, str) and source:
            from tessellum.composer.note_coverage import owned_span_words

            spans = owned_span_words(notes, cmap, source)
            if spans:
                heavy = {n: ws for n, ws in spans.items()
                         if ws[0] > 2 * PLAN_NOTE_MAX_WORDS}
                sizes = sorted(ws[0] for ws in spans.values())
                parts.append(
                    f"BALANCE (computed): owned-span words per note "
                    f"min={sizes[0]} max={sizes[-1]} over {len(spans)} notes"
                    + (f"; OVER 2x ceiling ({2 * PLAN_NOTE_MAX_WORDS}): "
                       + ", ".join(f"{n}={ws[0]}w/{ws[1]}sec"
                                   for n, ws in sorted(heavy.items()))
                       if heavy else " (balanced)")
                )
    return "\n".join(parts)


def _review_verdict(plan_doc: dict) -> tuple[bool, list]:
    """Extract the review phase's typed ``(ready, failures)`` verdict from
    ``plan_doc`` — the single reader used by both the sign-off program gate and
    the P15 revise loop (FZ 20k9c1a1a1b7c2h), so the two agree on what "ready"
    means. The review skill's ``step_4_report_verdict`` merges ``{ready,
    failures}`` at the top level; a nested ``verdict`` dict is also honoured."""
    verdict = plan_doc.get("verdict")
    if isinstance(verdict, dict):
        ready, failures = bool(verdict.get("ready")), list(verdict.get("failures") or [])
    else:
        ready, failures = bool(plan_doc.get("ready")), list(plan_doc.get("failures") or [])
    # Issue 9 loop guard (FZ 20k9c1a1a1b7c2k1a1b, mechanism 3): DROP a failure
    # the deterministic evidence contradicts. The r3 run burned both revise
    # rounds on a fabricated "~30 headings unmapped" claim while the computed
    # set-difference was ZERO in every round — a loop amplifies its gate's
    # errors, so a coverage-orphan claim only stands when the computed
    # set-difference is non-empty. Dropped claims are preserved on
    # ``plan_doc["contradicted_failures"]`` (surfaced, never silently lost).
    # Scoped to the coverage-orphan domain — the one empirically observed
    # fabrication class; other failure text passes through untouched.
    if failures:
        # Review F4: a drop is only as sound as the evidence's PROVENANCE —
        # every domain gates on the pages[] ledger being CODE-computed
        # (``_pages_code_measured``, set by the driver). Model-emitted pages
        # (a caller outside run_digestion_pipeline, or a source with no
        # inline text) can never ground a drop.
        code_measured = bool(plan_doc.get("_pages_code_measured"))
        orphans = compute_coverage_orphans(plan_doc) if code_measured else None
        orphan_safe = orphans is not None and len(orphans) == 0
        figures_safe = code_measured and _figures_all_present(plan_doc)
        kept, dropped = [], []
        for f in failures:
            sf = str(f)
            if orphan_safe and _ORPHAN_CLAIM_RE.search(sf):
                dropped.append(sf)
            elif figures_safe and _FIGURE_CLAIM_RE.search(sf):
                dropped.append(sf)
            else:
                kept.append(f)
        if dropped:
            plan_doc["contradicted_failures"] = dropped
            failures = kept
            if not failures:
                ready = True
        else:
            # Review F8: never carry a PRIOR round's drops into this verdict.
            plan_doc.pop("contradicted_failures", None)
    # E3.3 (FZ 20k9c1a1a1b7c2k1a1b1, decided 2026-07-29 on r5 + J3 evidence):
    # advisory-vs-gating. GATING checkpoints are the deterministic-backed ones
    # (CP1–CP4, CP7, CP8 — each has a computed exhibit or gate behind it);
    # CP5 (derivation faithfulness) and CP6 (borderline atomicity) are
    # QUALITATIVE and uncalibrated — r5's CP5 bootstrap-posture false-reject
    # and the calibration principle ("uncalibrated judgements demote to
    # advisory") put them below the loop-gating bar until the P8 calibration
    # path promotes them. A verdict whose ONLY failures are advisory-prefixed
    # flips ready for the LOOP; the advisory failures are preserved on
    # ``plan_doc["advisory_failures"]`` and still surface at sign-off — the
    # reviewer's voice is demoted, never silenced.
    if not ready and failures:
        advisory, gating = [], []
        for f in failures:
            (advisory if _ADVISORY_CLAIM_RE.match(str(f).strip()) else gating).append(f)
        if advisory and not gating:
            plan_doc["advisory_failures"] = [str(f) for f in advisory]
            return True, []
        plan_doc.pop("advisory_failures", None)
    return ready, failures


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


def _joined_source_excerpt(plan_doc: dict) -> tuple[str, list[str]]:
    """The single joined source text + refs the execute wave grounds writers
    in. Members' excerpts joined under ``# SOURCE:`` headers; a member-less
    single-doc leaf (the runtime M0 shape) falls back to the top-level
    ``source_content`` — the same pseudo-member symmetry
    :func:`compute_source_ledger` applies (E3.1 review F4), closing the latent
    empty-source gap on that path (before A3 the projection read ONLY members,
    so a single-doc runtime job's writers received an empty source)."""
    members = plan_doc.get("members")
    source_refs: list[str] = []
    parts: list[str] = []
    if isinstance(members, list) and members:
        for m in members:
            if not isinstance(m, dict):
                continue
            ex = m.get("excerpt") or m.get("source_content") or ""
            ref = m.get("source_url") or m.get("ref") or m.get("source_id") or ""
            if ref:
                source_refs.append(str(ref))
            parts.append(f"# SOURCE: {m.get('source_id') or ref}\n\n{ex}")
    source_excerpt = "\n\n".join(parts)
    if not source_excerpt.strip():
        sc = plan_doc.get("source_content")
        if isinstance(sc, str) and sc.strip():
            name = plan_doc.get("source_name") or plan_doc.get("source_url") or "source"
            source_excerpt = f"# SOURCE: {name}\n\n{sc}"
    if not source_refs:
        su = plan_doc.get("source_url")
        source_refs = list(su) if isinstance(su, list) else ([str(su)] if su else [])
    return source_excerpt, source_refs


def _ensure_source_excerpt(plan_doc: dict) -> None:
    """A3.1 (FZ 20k9c1a1a1b7c2k1a): make the joined source excerpt a
    ``plan_doc`` field so the artifact store pages ONE durable copy every
    writer reads by reference (``{{artifact.source_excerpt}}``) instead of N
    inline copies riding every leaf. Idempotent; never overwrites an existing
    non-empty value (a promote path may have restored it from the verified
    durable store — that copy is the of-record)."""
    if not plan_doc.get("source_excerpt"):
        excerpt, _refs = _joined_source_excerpt(plan_doc)
        if excerpt:
            plan_doc["source_excerpt"] = excerpt


def _existing_notes_context(
    plan_doc: dict, related_notes_db: "Path | str | None", vault_root: Path
) -> str:
    """W3.2 (FZ 20k9c1a1a1b7c2k2a4): the plan phase's SEMANTIC-tier read —
    a retrieval sample from the live index (titles + paths keyed on the
    source head, plus one sibling note's head as a format sample) rendered
    for the `route`/`cross_references` steps, replacing the "search the
    vault" role-play their prose used to demand. "" on a bootstrap vault
    (no index) or any retrieval failure — fail-soft, the prose handles an
    empty block explicitly."""
    if related_notes_db is None:
        return ""
    try:
        from tessellum.composer.related_notes import enrich_related_notes

        source = str(plan_doc.get("source_excerpt") or plan_doc.get("source_content") or "")
        query = source[:500] or str(plan_doc.get("source_name") or "")
        if not query.strip():
            return ""
        result = enrich_related_notes(
            thesis=query,
            target_path="resources/documentation/context.md",
            db_path=related_notes_db,
        )
        rows = list(getattr(result, "related", ()) or ())[:10]
        if not rows:
            return ""
        lines = ["EXISTING NOTES (top retrieval matches — title, vault path):"]
        sample_text = ""
        for r in rows:
            name = getattr(r, "note_name", None) or getattr(r, "note_id", "")
            nid = getattr(r, "note_id", "")
            lines.append(f"- {name} ({nid})")
            if not sample_text and nid:
                candidate = vault_root / nid
                try:
                    sample_text = candidate.read_text(encoding="utf-8")[:1500]
                except OSError:
                    sample_text = ""
        if sample_text:
            lines.append("")
            lines.append("SIBLING FORMAT SAMPLE (head of the top match — copy "
                         "its YAML field order and H2 conventions):")
            lines.append(sample_text)
        return "\n".join(lines)
    except Exception:
        return ""


def _owned_source_slice(filename: str, plan_doc: dict) -> str:
    """W1 (FZ 20k9c1a1a1b7c2k2a4): the VERBATIM text of the sections this
    note owns — coverage map ⨝ the fence-aware section split of the joined
    source, via the one canonical join in :mod:`note_coverage`. Returns ""
    when the plan has no usable map/source or no sections resolve (the
    caller's prompt falls back to the full source)."""
    cmap = plan_doc.get("section_coverage_map")
    source = plan_doc.get("source_excerpt")
    if not (isinstance(cmap, list) and cmap and isinstance(source, str) and source):
        return ""
    from tessellum.composer.note_coverage import owned_sections_for, split_sections

    owned = owned_sections_for(filename, cmap, split_sections(source))
    return "\n\n".join(owned.values())


def _owned_sections_md(filename: str, plan_doc: dict) -> str:
    """E2.3 (FZ 20k9c1a1a1b7c2k1a1b1): the per-note ledger slice — the
    ``section_coverage_map`` rows this note owns, joined with the code-measured
    ``pages[]`` ledger, rendered as the writer's assigned-sections block. The
    writer learns exactly which MEASURED sections it owns instead of
    re-deriving its scope from the whole plan. Empty string when the plan
    carries no usable map (never a ``<missing>`` sentinel — the projection
    stamps the key unconditionally)."""
    cmap = plan_doc.get("section_coverage_map")
    if not isinstance(cmap, list) or not cmap:
        return ""
    heading_pages: dict[str, tuple[str, Any]] = {}
    pages = plan_doc.get("pages")
    if isinstance(pages, list):
        for pg in pages:
            if not isinstance(pg, dict):
                continue
            page_name = str(pg.get("page") or pg.get("source_id") or "")
            for h in pg.get("headings") or []:
                heading_pages[_norm_heading(str(h))] = (page_name, pg.get("words"))
    # Boundary-aware suffix match (`tessellum_a.md` owns rows naming `a.md`;
    # `data.md` must NOT match `a.md`) — ONE implementation, canonical in
    # note_coverage since the F12 consolidation.
    _name_match = nc_name_match

    base = filename.rsplit("/", 1)[-1]
    lines: list[str] = []
    for row in cmap:
        if not isinstance(row, dict):
            continue
        target = str(row.get("maps_to_note") or row.get("note") or "").strip()
        target = target.rsplit("/", 1)[-1]
        if not target or not (_name_match(base, target) or _name_match(target, base)):
            continue
        section = str(row.get("source_section") or "").strip()
        if not section:
            continue
        page, words = heading_pages.get(_norm_heading(section), ("", None))
        if page and words:
            lines.append(f"- {section} (source: {page}, {words} measured words on page)")
        elif page:
            lines.append(f"- {section} (source: {page})")
        else:
            lines.append(f"- {section}")
    if lines:
        # Phase 3 (FZ b7c2k2a3a): the code-block budget rides the slice —
        # N5's cap made explicit where the writer decides what to include.
        lines.append(
            "- BUDGET: at most 6 code blocks in this note — select the "
            "REPRESENTATIVE snippets from your sections, do not transcribe "
            "every block."
        )
    return "\n".join(lines)


def _reconcile_planned_notes_table(plan_doc: dict[str, Any]) -> None:
    """F11 (FZ 20k9c1a1a1b7c2k2a — the openclaw sweep, closing b7c4's oldest
    residual): the prose ``## Planned Notes`` table is a PROJECTION of the
    structured ``planned_notes`` list, regenerated by CODE after every fold —
    the two inventories CANNOT drift, because only one exists. Every prior
    defense was detection (the INVENTORY exhibit, the one-inventory prose
    mandate, F4's revise conditioning) and the drift kept recurring: b7c4's
    23-vs-13, run 8's 16-vs-10, hermes' 15-vs-11, openclaw run 6's 12-vs-9
    (which burned both revise rounds). Write-time binding ends the class.
    Replaces only the contiguous table block inside the section, preserving
    surrounding prose; no section or no structured list → no-op."""
    notes = plan_doc.get("planned_notes")
    pt = plan_doc.get("plan_text")
    if not (isinstance(notes, list) and notes and isinstance(pt, str) and pt):
        return
    m = re.search(r"(?mi)^##\s+Planned Notes.*$", pt)
    if not m:
        return
    start = m.end()
    nxt = re.search(r"(?m)^##\s+", pt[start:])
    end = start + (nxt.start() if nxt else len(pt) - start)
    section = pt[start:end]
    rows = [
        "",
        "| # | Note | Building Block | Approx Words | Description |",
        "|---|---|---|---|---|",
    ]
    for i, n in enumerate(notes, 1):
        if not isinstance(n, dict):
            continue
        desc = str(n.get("description", "")).replace("|", "/").replace("\n", " ")
        rows.append(
            f"| {i} | {n.get('filename', '')} | {n.get('building_block', '')} "
            f"| {n.get('approx_words', '')} | {desc} |"
        )
    table = "\n".join(rows) + "\n"
    lines = section.split("\n")
    first = last = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("|"):
            if first is None:
                first = i
            last = i
    if first is None:
        new_section = table + section
    else:
        new_section = (
            "\n".join(lines[:first]) + table + "\n".join(lines[last + 1:])
        )
    plan_doc["plan_text"] = pt[:start] + new_section + pt[end:]


def _replace_or_none(pt: str, heading_prefix: str, body: str) -> str | None:
    """Replace the BODY of the first H2 whose normalized title starts with
    ``heading_prefix`` (name variants included) with ``body`` — heading line
    normalized to ``body``'s own first line. ``None`` when no such section
    exists (caller appends instead)."""
    for m in re.finditer(r"(?m)^##\s+(.+?)\s*$", pt):
        title = " ".join(m.group(1).lower().split())
        if not title.startswith(heading_prefix):
            continue
        start = m.start()
        nxt = re.search(r"(?m)^##\s+", pt[m.end():])
        end = m.end() + (nxt.start() if nxt else len(pt) - m.end())
        return pt[:start] + body + "\n" + pt[end:]
    return None


def _reconcile_generated_sections(plan_doc: dict[str, Any]) -> None:
    """F13 + F15 (FZ 20k9c1a1a1b7c2k2a3a — sweep runs 9 and 11, the F11 class
    generalized then completed): mandatory sections whose content is
    DETERMINISTIC DATA are code-generated projections.

    Run 9 (F13): the writer reliably authored the ten judgment sections and
    reliably OMITTED the four derivable ones, through F8 conditioning that
    NAMED them — so the derivable sections are generated when missing. Run
    11 (F15): generate-if-missing was NOT enough for the strictly-data
    sections — the writer AUTHORED a "Summary Statistics" section carrying
    invented tallies ("Digest notes planned: 26" against the of-record 9),
    and the incomplete authored section beat the complete generated one. So
    the two PURE-DATA sections (``Source Pages``, ``Summary Statistics &
    Building Block Distribution``) are now REGENERATED ALWAYS — authored
    bodies replaced, heading normalized to the canonical stem (F11's
    write-time binding, whole-section scope); the two boilerplate sections
    (``Per-Phase Validation Gate``, ``Review Sign-Off``) stay
    generate-if-missing, since an authored version can carry legitimate
    plan-specific content.

    Scoped like PLAN-009: coverage-map-bearing plans only (the full
    digestion contract); no plan_text → no-op.
    """
    pt = plan_doc.get("plan_text")
    cmap = plan_doc.get("section_coverage_map")
    if not (isinstance(pt, str) and pt and isinstance(cmap, list) and cmap):
        return

    pages = plan_doc.get("pages")
    if isinstance(pages, list) and pages:
        rows = ["## Source Pages", "",
                "| Source | Measured Words | Code Blocks | Headings |",
                "|---|---|---|---|"]
        for pg in pages:
            if not isinstance(pg, dict):
                continue
            rows.append(
                f"| {pg.get('source_id') or pg.get('url') or ''} "
                f"| {pg.get('measured_words', '')} "
                f"| {pg.get('code_blocks', '')} "
                f"| {len(pg.get('headings') or [])} |"
            )
        rows.append("")
        rows.append("(code-measured ledger — the of-record `pages[]`)")
        block = "\n".join(rows)
        replaced = _replace_or_none(pt, "source pages", block)
        pt = replaced if replaced is not None else (
            pt.rstrip("\n") + "\n\n" + block + "\n"
        )

    notes = plan_doc.get("planned_notes")
    if isinstance(notes, list) and notes:
        bb: dict[str, int] = {}
        for n in notes:
            if isinstance(n, dict):
                key = str(n.get("building_block") or "unspecified")
                bb[key] = bb.get(key, 0) + 1
        lines = ["## Summary Statistics & Building Block Distribution", "",
                 f"Total planned notes: {len(notes)}", ""]
        lines += [f"- {k}: {v}" for k, v in sorted(bb.items())]
        lines.append("")
        lines.append("(derived from the structured `planned_notes` inventory)")
        block = "\n".join(lines)
        replaced = _replace_or_none(pt, "summary statistics", block)
        pt = replaced if replaced is not None else (
            pt.rstrip("\n") + "\n\n" + block + "\n"
        )

    plan_doc["plan_text"] = pt
    low = pt.lower()
    blocks: list[str] = []

    if "per-phase validation gate" not in low:
        blocks.append(
            "## Per-Phase Validation Gate\n\n"
            "Deterministic gates enforced by the pipeline (not authored "
            "here): plan scope — structure, mandatory sections (PLAN-009), "
            "coverage (PLAN-006), density band (PLAN-004/PLAN-008) at "
            "sign-off; session scope — format + grounding at each note's "
            "close gate; wave scope — dedup + owned-section coverage after "
            "the wave."
        )

    if "review sign-off" not in low:
        blocks.append(
            "## Review Sign-Off\n\n"
            "Pending — decided by the sign-off ladder (deterministic plan "
            "gate + the review skill's typed verdict); the decision is "
            "recorded on the run's sign-off result, not authored in this "
            "plan."
        )

    if blocks:
        plan_doc["plan_text"] = (
            pt.rstrip("\n") + "\n\n" + "\n\n".join(blocks) + "\n"
        )


def _reconcile_section_assessment(plan_doc: dict[str, Any]) -> None:
    """F16 (FZ 20k9c1a1a1b7c2k2a3a — sweep run 12): ``sections_present`` /
    ``sections_missing`` are SELF-ASSESSMENTS of ``plan_text`` — 100%
    code-derivable, so code owns them.

    Run 12 burned all three review rounds on exactly this class: the
    model-emitted registry claimed labels ('Inlink mapping', 'Entry Point
    specifics') that matched no real H2 ('## Inlinks', '## Entry Point
    Decision'), the reviewer correctly blocked per exhibit-wins, and each
    revise round produced a NEW label mismatch. R4.1's ASSESSMENTS check
    detects the class; this ends it (the F11→F13→F15 law again):
    ``sections_present`` is overwritten with the REAL fence-aware H2 scan
    and ``sections_missing`` with the mandatory stems absent from the text.
    Only keys the model actually emitted are overwritten — a doc without
    the assessment channel is untouched."""
    pt = plan_doc.get("plan_text")
    if not (isinstance(pt, str) and pt):
        return
    if "sections_present" not in plan_doc and "sections_missing" not in plan_doc:
        return
    real_h2: list[str] = []
    in_fence = False
    for line in pt.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            real_h2.append(m.group(1))
    if "sections_present" in plan_doc:
        plan_doc["sections_present"] = real_h2
    if "sections_missing" in plan_doc:
        from tessellum.composer.contracts import mandatory_section_stems

        low = pt.lower()
        plan_doc["sections_missing"] = [
            s for s in mandatory_section_stems() if s.lower() not in low
        ]


def _rematerialize_plan_file(
    plan_doc: dict[str, Any],
    vault_root: Path,
    effect_guard: "Callable[[], ContextManager[None]] | None",
    effect_recorder: "Callable[[Path], None] | None",
) -> None:
    """Phase-1 instrument fix (FZ 20k9c1a1a1b7c2k2a3a): the on-disk plan file
    is a PROJECTION of the of-record ``plan_doc`` and must track it. The final
    revise round's materializer writes the file BEFORE the fold, so F11's
    reconciled inventory (and every fold-time normalization) never reached the
    last round's file — openclaw's Tier-1 scored stale prose because of
    exactly this seam. Called after SIGN-OFF APPROVAL: if the approved
    ``plan_text`` differs from the file at ``plan_path``, rewrite it through
    the same effect machinery the original write used (journaled, guarded).
    Fail-soft: a projection refresh must never fail an approved run."""
    try:
        plan_path = plan_doc.get("plan_path")
        plan_text = plan_doc.get("plan_text")
        if not (isinstance(plan_path, str) and plan_path
                and isinstance(plan_text, str) and plan_text):
            return
        target = (Path(vault_root) / plan_path).resolve()
        try:
            target.relative_to(Path(vault_root).resolve())
        except ValueError:
            return  # never write outside the vault
        if not target.is_file():
            return  # the run never materialized a plan file (e.g. tests)
        if target.read_text(encoding="utf-8") == plan_text:
            return
        if effect_recorder is not None:
            effect_recorder(target)
        ctx = effect_guard() if effect_guard is not None else None
        if ctx is not None:
            with ctx:
                target.write_text(plan_text, encoding="utf-8")
        else:
            target.write_text(plan_text, encoding="utf-8")
    except Exception:
        pass


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
    keys on), and the ``source_ref``.

    A3.1/A3.3 (FZ 20k9c1a1a1b7c2k1a): the leaves are METADATA-ONLY — the
    heavy ``source_excerpt`` + ``plan_text`` travel ONCE via the wave's
    artifact store (``{{artifact.source_excerpt}}`` / ``{{artifact.plan_text}}``
    in the execute skill), not N× inline (the old O(plan×N) input carry).
    Each leaf instead carries ``artifact_refs`` (key → sha256 of the
    stringified of-record value), so the scheduler's ``_task_identity`` leaf
    hash binds the CONTENT by reference — resume identity is sha256-of-refs.
    E2.3: each leaf also carries its ``owned_sections_md`` slice (coverage map
    ⨝ measured ledger). Mutates ``plan_doc`` only via
    :func:`_ensure_source_excerpt` (idempotent). Fail-soft: a
    ``planned_notes`` that is missing, not a list, or has no usable
    ``filename`` yields ``[]`` so the caller falls through to the whole-plan
    leaf.
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

    # A3.1: the joined source becomes a plan_doc field (paged ONCE by the
    # artifact store), and the leaves carry content DIGESTS instead of bytes.
    _ensure_source_excerpt(plan_doc)
    _excerpt, source_refs = _joined_source_excerpt(plan_doc)
    plan_text = str(plan_doc.get("plan_text") or "")
    artifact_refs = {
        key: hashlib.sha256(_stringify(val).encode("utf-8")).hexdigest()
        for key, val in (
            ("plan_text", plan_text),
            ("source_excerpt", plan_doc.get("source_excerpt") or ""),
        )
        if val
    }

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
            },
            "artifact_refs": dict(artifact_refs),
            "owned_sections_md": _owned_sections_md(name, plan_doc),
            # W1 (FZ 20k9c1a1a1b7c2k2a4): the writer's NEEDLE — the verbatim
            # text of the sections this note owns, resolved with the same
            # canonical fence-aware join the coverage sweep and scoped judge
            # use. Slices are near-disjoint across notes, so the total inline
            # bytes ≈ one source copy (not the O(plan×N) re-carry A3 killed).
            # Empty when sections don't resolve — the writer falls back to
            # the full source, byte-identical to pre-W1.
            "owned_source_slice": _owned_source_slice(name, plan_doc),
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
    # P21-full + A3.2: the writer leaves are metadata-only (the A3.1
    # projection), so the artifact channel is now the LOAD-BEARING path — the
    # execute skill reads {{artifact.plan_text}} / {{artifact.source_excerpt}}
    # from this store (one copy, durable under --durable-artifacts) instead of
    # each leaf re-carrying the bytes. _ensure_source_excerpt guarantees the
    # store has the joined source even for direct callers (corpus / runtime
    # promote) that skip the pipeline's early ensure.
    _ensure_source_excerpt(plan_doc)
    # Phase-3 residue (FZ 20k9c1a1a1b7c2k2a3a): when a wave gate is on and the
    # plan carries a coverage map, extend it with the deterministic per-note
    # owned-section coverage sweep (ADVISORY — WARNINGs reach the run events,
    # nothing blocks until the check is calibrated strict). Identity when the
    # caller passed no wave gate or the plan has no map — parity preserved.
    incoming_wave_gate = execute_kwargs.get("wave_gate")
    if incoming_wave_gate is not None:
        coverage_source, _refs = _joined_source_excerpt(plan_doc)
        execute_kwargs["wave_gate"] = extend_wave_gate_with_note_coverage(
            incoming_wave_gate, plan_doc, coverage_source
        )
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
    run_id: str | None = None,
    durable_artifact_dir: Path | None = None,
    resume_from_checkpoint: bool = False,
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
        resume_from_checkpoint: **Phase 4 (FZ 20k9c1a1a1b7c2k2a3a)** — when
            ``True`` and ``runs_dir`` holds A1.2 checkpoints whose
            code-measured ledger matches THIS source, fold the latest
            checkpoint and skip the already-paid linear phases (a ready
            review fold goes straight to sign-off). Source mismatch or no
            checkpoint → fresh start, byte-identical. Default ``False``.
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
    # A0 (FZ 20k9c1a1a1b7c2k1a): hoist run identity to the pipeline level. The
    # execute wave already accepted run_id via **execute_kwargs (manifest
    # owner-fencing; corpus isolation via _RUN_SCOPED_EXECUTE_KWARGS) — the
    # named param makes it first-class and surfaced on the result. No-clobber:
    # an explicit execute_kwargs["run_id"] (the pre-A0 calling convention)
    # wins, and the surfaced identity is whatever the wave actually uses.
    if run_id is not None:
        execute_kwargs.setdefault("run_id", run_id)
    run_id = execute_kwargs.get("run_id")
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
    # Issue 11 (FZ 20k9c1a1a1b7c2k1a1b): the source ledger is CODE-COMPUTED
    # from the members' inline text — the model may not author measurements.
    # Computed once here; re-asserted after every phase fold so an LLM
    # re-emission of pages[] never survives (measured-by-code, k1a1a).
    ledger_members = plan_doc.get("members") or []
    if not ledger_members:
        # Review F4: the runtime + CLI single-doc paths carry the source as a
        # top-level ``source_content`` with EMPTY members — synthesize a
        # pseudo-member so the ledger is code-measured on the primary path
        # too (else the model's estimates become the "evidence").
        sc = plan_doc.get("source_content")
        if isinstance(sc, str) and sc.strip():
            ledger_members = [{
                "source_id": plan_doc.get("source_name")
                or plan_doc.get("id") or "source",
                "excerpt": sc,
            }]
    code_ledger = compute_source_ledger(ledger_members)
    if code_ledger:
        plan_doc["pages"] = code_ledger
        plan_doc["_pages_code_measured"] = True
        # Issue 15 (FZ 20k9c1a1a1b7c2k1a1b1a): prose bands do not bind — give
        # the PLANNER the computed count band (mechanism 2 reaching its last
        # producer). Derived from the same arithmetic the PLAN-004/PLAN-008
        # gates enforce, so round 0 plans inside what sign-off will accept.
        total = sum(pg.get("measured_words", 0) for pg in code_ledger)
        if total > 0:
            lo = max(1, -(-total // PLAN_NOTE_MAX_WORDS))
            hi = max(lo, -(-total // PLAN_OVERSPLIT_MIN_WORDS))
            plan_doc["note_count_band"] = (
                f"{lo}..{hi} notes (measured {total} words; density ceiling "
                f"{PLAN_NOTE_MAX_WORDS}, over-split floor {PLAN_OVERSPLIT_MIN_WORDS} "
                f"— the PLAN-004/PLAN-008 gates enforce this band at sign-off)"
            )
    # A3.1 (FZ 20k9c1a1a1b7c2k1a): derive the joined source excerpt ONCE from
    # the input (members / source_content — invariant across folds) so every
    # artifact store built from here pages one durable of-record copy the
    # writers read by reference. Captured for re-assertion after every fold —
    # same guard the code ledger has: a phase EMITTING a `source_excerpt` key
    # would otherwise clobber the code-joined source with a lossy LLM
    # re-emission (the E12/E16 class under a new key).
    _ensure_source_excerpt(plan_doc)
    code_source_excerpt = plan_doc.get("source_excerpt")
    # W3.2 (FZ 20k9c1a1a1b7c2k2a4): the plan phase's semantic-tier read —
    # retrieval-backed existing-notes context for route/cross_references,
    # replacing their "search the vault" role-play. "" without an index.
    plan_doc.setdefault(
        "existing_notes_context",
        _existing_notes_context(plan_doc, related_notes_db, Path(vault_root)),
    )
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
    # A1.2 (FZ 20k9c1a1a1b7c2k1a): monotonic checkpoint counter — one durable
    # plan-of-record snapshot per phase fold (revise rounds included), so a
    # crash mid-run resumes from the last accepted fold instead of restarting.
    checkpoint_seq = 0

    # Phase 4 (FZ 20k9c1a1a1b7c2k2a3a): checkpoint-resume — the claim path
    # consumes the A1.2 checkpoints instead of re-paying the linear phases
    # (two external kills + the credit wall each re-ran ~15 min of work the
    # checkpoints already contained). Opt-in; guarded by SOURCE IDENTITY —
    # the checkpoint's code-measured ledger must equal the one just computed
    # from THIS source (deterministic ⇒ same source, same ledger), so a
    # runs_dir reused across different sources refuses the resume and starts
    # fresh (fail-soft). The resumed doc is re-stamped with the code-owned
    # keys (ledger, source excerpt, reconciled table) — the checkpoint never
    # overrides measured-by-code. Revise-round budget resets on resume (a
    # fresh attempt gets a fresh budget, deliberately).
    resumed_phase: str | None = None
    if resume_from_checkpoint and linear_runs_dir is not None:
        loaded = load_latest_checkpoint(linear_runs_dir)
        if loaded is not None:
            cp_seq, cp_phase, cp_doc = loaded
            cp_pages = cp_doc.get("pages")
            same_source = (
                bool(code_ledger)
                and isinstance(cp_pages, list)
                and [
                    (p.get("source_id"), p.get("measured_words"))
                    for p in cp_pages if isinstance(p, dict)
                ]
                == [
                    (p.get("source_id"), p.get("measured_words"))
                    for p in code_ledger
                ]
            )
            if same_source:
                plan_doc.update(cp_doc)
                _normalize_plan_doc_keys(plan_doc)
                plan_doc["pages"] = code_ledger
                plan_doc["_pages_code_measured"] = True
                if code_source_excerpt:
                    plan_doc["source_excerpt"] = code_source_excerpt
                _reconcile_planned_notes_table(plan_doc)
                _reconcile_generated_sections(plan_doc)
                _reconcile_section_assessment(plan_doc)
                checkpoint_seq = cp_seq
                resumed_phase = cp_phase
                plan_doc["_resumed_from_checkpoint"] = {
                    "seq": cp_seq, "phase": cp_phase,
                }

    def _run_one_phase(phase: str, leaf: dict) -> RunResult | None:
        """Run one linear phase; append its outcome; merge + normalize. Returns
        the RunResult, or None if it errored (caller returns a halt result)."""
        nonlocal checkpoint_seq
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
            runs_dir=linear_runs_dir,
            artifacts=_build_artifact_store(plan_doc, durable_artifact_dir),
        )
        phases.append(
            PhaseOutcome(phase=phase, ran=True, error_count=run.error_count, run=run)
        )
        plan_doc.update(_collect_structured(run))
        _normalize_plan_doc_keys(plan_doc)
        if code_ledger:
            plan_doc["pages"] = code_ledger
        if code_source_excerpt:
            plan_doc["source_excerpt"] = code_source_excerpt
        # F11: the prose Planned-Notes table is regenerated from the
        # structured list after EVERY fold — one inventory, by construction.
        _reconcile_planned_notes_table(plan_doc)
        # F13: the deterministic mandatory sections (Source Pages, Summary
        # Statistics, Per-Phase Validation Gate, Review Sign-Off) are
        # code-generated when the writer omits them — run 9 burned all three
        # rounds failing to author sections whose content is plan_doc data.
        _reconcile_generated_sections(plan_doc)
        # F16: the section self-assessment is code-computed from the text.
        _reconcile_section_assessment(plan_doc)
        if linear_runs_dir is not None:
            checkpoint_seq += 1
            _checkpoint_plan_doc(linear_runs_dir, checkpoint_seq, phase, plan_doc)
        return None if run.error_count else run

    def _halt(phase: str) -> DigestionResult:
        return DigestionResult(
            completed=False, stopped_at=phase, sign_off=None,
            phases=tuple(phases), plan_doc=plan_doc, review_rounds=review_rounds, run_id=run_id,
            contradicted_failures=tuple(plan_doc.get("contradicted_failures") or ()),
        )

    # plan (once) — skipped on resume: any checkpoint implies a plan fold.
    if resumed_phase is None:
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

    # Phase 4 fast path: a resumed REVIEW fold whose typed verdict is ready
    # AND whose deterministic plan gate passes (both re-checked here, free —
    # no LLM) goes straight to sign-off; anything less re-enters the loop,
    # with the checkpointed failures conditioning the first re-augment.
    skip_revise_loop = False
    if resumed_phase == "review":
        ready, failures = _review_verdict(plan_doc)
        if ready and build_plan_gate().evaluate(plan_doc).passed:
            skip_revise_loop = True
        elif failures:
            review_failures = failures

    while not skip_revise_loop:
        aug_leaf = dict(plan_doc)
        if review_failures:
            # P15.2: condition the re-augment on the prior review's specific gaps.
            aug_leaf["review_failures"] = "\n".join(f"- {f}" for f in review_failures)
        if _run_one_phase("augment", aug_leaf) is None:
            return _halt("augment")
        review_leaf = dict(plan_doc)
        exhibits = compute_review_exhibits(plan_doc)
        if exhibits:
            review_leaf["review_exhibits"] = exhibits
        if _run_one_phase("review", review_leaf) is None:
            return _halt("review")

        ready, failures = _review_verdict(plan_doc)
        # F8 (FZ 20k9c1a1a1b7c2k2a — the openclaw sweep): a reviewer may
        # UNDER-enforce against its own cited exhibit (it approved a plan whose
        # COVERAGE exhibit named 4 computed orphans; the deterministic
        # sign-off gate then rejected TERMINALLY with revise rounds unused).
        # The design's own rule — only verified quantities drive control flow
        # — applies to the LOOP's continue-condition too: when the reviewer
        # says ready but the DETERMINISTIC plan gate fails and rounds remain,
        # the gate's blocking issues become the revise conditioning instead of
        # a doomed sign-off. The gate is the authority in BOTH directions now:
        # it vetoes false accepts here exactly as the contradiction guard
        # vetoes fabricated rejects.
        if ready and review_rounds < max_review_rounds:
            composite = build_plan_gate().evaluate(plan_doc)
            if not composite.passed:
                gate_failures = [str(i) for i in composite.blocking_issues] or [
                    str(composite.first_failure_cause)
                ]
                ready = False
                failures = gate_failures
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
            review_rounds=review_rounds, run_id=run_id,
            contradicted_failures=tuple(plan_doc.get("contradicted_failures") or ()),
        )

    # Phase-1 instrument fix (FZ b7c2k2a3a): the APPROVED plan_doc is the
    # of-record; refresh the on-disk plan file so every projection (the file
    # the scorer reads, the file a human inspects) carries the reconciled
    # plan_text — F11's single inventory included.
    _rematerialize_plan_file(plan_doc, vault_root, effect_guard, effect_recorder)

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
            review_rounds=review_rounds, run_id=run_id,
            contradicted_failures=tuple(plan_doc.get("contradicted_failures") or ()),
        )

    # ── execute: the fan-out wave (one leaf per planned note) ───────────────
    if cancellation_check is not None and cancellation_check():
        raise InterruptedError("digestion cancelled before execute")
    try:
        # A2 (FZ 20k9c1a1a1b7c2k1a): page the final of-record artifacts to the
        # durable working store and hand the wave ArtifactRefs via the existing
        # execute_kwargs['artifacts'] seam (no-clobber: an explicit caller-
        # provided store wins).
        if durable_artifact_dir is not None and "artifacts" not in execute_kwargs:
            execute_kwargs["artifacts"] = _build_artifact_store(
                plan_doc, durable_artifact_dir
            )
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
            review_rounds=review_rounds, run_id=run_id,
            contradicted_failures=tuple(plan_doc.get("contradicted_failures") or ()),
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
        review_rounds=review_rounds, run_id=run_id,
            contradicted_failures=tuple(plan_doc.get("contradicted_failures") or ()),
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
