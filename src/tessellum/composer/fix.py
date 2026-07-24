"""Fix stage — informed, non-regressive close-gate repair.

Composer v4, Phase 4 (fix half). When a note fails its close-gate, the
fixer is asked to repair it. Two hazards this module closes:

1. **Regression.** A later fix attempt can make the note *worse* than an
   earlier one (e.g. attempt 1 fixed 3 of 4 issues; attempt 2 reintroduced
   two). Naively leaving the last attempt on disk loses the better earlier
   version. This module **checkpoints the note's bytes before each fix and
   keeps the BEST-scoring snapshot**, restoring it at the end — so a
   regressing fix can never overwrite a better earlier note (the
   checkpoint-before-risky-op + revert-to-BEST discipline).

2. **Blind retries.** A fixer that re-runs with no memory repeats the same
   mistake. :class:`FixContext` carries the structured gate ``issues`` plus
   the prior attempts' outcomes so the fixer is *informed* — it sees what
   failed and what it already tried.

Scoring is by blocking-issue count (lower is better; ``0`` = clean/passed),
so "best" is unambiguous and a pure function of the gate verdict. All I/O
is byte-level note read/write; no LLM lives here (IDENT-3) — the fixer
callable is where any model call happens, injected by the caller.
"""

from __future__ import annotations

import os
import stat
import uuid
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, ContextManager, Sequence

from tessellum.composer.credential_pool import RunBudget


@dataclass(frozen=True)
class AttemptOutcome:
    """One fix attempt's result — the memory an informed fixer reads.

    Attributes:
        round_n: 1-indexed fix round.
        score: Blocking-issue count after this attempt (0 = clean).
        causes: The failing-gate cause tags after this attempt.
    """

    round_n: int
    score: int
    causes: tuple[str, ...] = ()


@dataclass(frozen=True)
class FixContext:
    """The curated diagnostics a fixer receives (not raw logs).

    Attributes:
        note_path: The note being repaired.
        issues: The current blocking issues (the gate's structured
            findings) — what to fix *now*.
        prior_attempts: Outcomes of earlier fix rounds — what was already
            tried, so the fixer doesn't repeat a failed strategy.
    """

    note_path: Path
    issues: tuple
    prior_attempts: tuple[AttemptOutcome, ...] = ()


@dataclass
class _Snapshot:
    """A scored byte-snapshot of the note, for revert-to-BEST."""

    content: bytes
    score: int


@dataclass(frozen=True)
class FixLoopResult:
    """The outcome of the revert-to-BEST fix loop.

    Attributes:
        passed: ``True`` iff a fix round reached a clean gate (score 0).
        rounds_used: How many fix rounds ran.
        final_score: The best (lowest) blocking-issue count achieved.
        cause: The terminal failing-gate cause when ``not passed`` (else
            ``None``).
        reverted: ``True`` iff the on-disk note was rolled back to an
            earlier, better-scoring snapshot (a later fix regressed).
        attempts: The per-round outcome history.
    """

    passed: bool
    rounds_used: int
    final_score: int
    cause: str | None = None
    reverted: bool = False
    attempts: tuple[AttemptOutcome, ...] = ()


# A gate evaluator: () -> (passed, cause, issues). The caller closes over
# the note path + verifier; this module just calls it and scores the result.
GateEvaluator = Callable[[], "tuple[bool, str | None, Sequence]"]

# An informed fixer: given the FixContext, repair the note in place. Return
# value ignored (the note is mutated on disk); may raise — a raise is
# treated as a no-op fix round, not propagated.
InformedFixer = Callable[[FixContext], object]


def score_issues(issues: Sequence) -> int:
    """The gate score: number of blocking issues (lower is better)."""
    return len(issues)


def run_fix_loop(
    *,
    note_path: Path,
    evaluate: GateEvaluator,
    fixer: InformedFixer | None,
    max_rounds: int,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
) -> FixLoopResult:
    """Run the informed, non-regressive fix loop with revert-to-BEST.

    Sequence:

    1. Evaluate the note as-written; if it already passes, return
       immediately (no fix, no snapshot churn).
    2. Snapshot the current bytes + score as the running BEST.
    3. Up to ``max_rounds`` times: build a :class:`FixContext` (current
       issues + prior-attempt outcomes), run the ``fixer`` (repairs in
       place), re-evaluate + re-score. If the new score beats BEST,
       promote the new bytes to BEST. Stop early on a clean pass.
    4. If the note on disk is no longer the BEST snapshot (a later fix
       regressed), **restore the BEST bytes** so the best version wins.

    Args:
        note_path: The note file the fixer repairs (read/written here).
        evaluate: The gate evaluator — ``() -> (passed, cause, issues)``.
        fixer: The informed fixer, or ``None`` to skip the loop entirely
            (a first FAIL is terminal).
        max_rounds: Max fix rounds (``0`` also skips the loop).

    Returns:
        A :class:`FixLoopResult`.
    """
    def _check_cancelled() -> None:
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError("fix loop cancelled")

    _check_cancelled()
    passed, cause, issues = evaluate()
    if passed:
        return FixLoopResult(
            passed=True, rounds_used=0, final_score=0, cause=None
        )
    if fixer is None or max_rounds <= 0:
        return FixLoopResult(
            passed=False,
            rounds_used=0,
            final_score=score_issues(issues),
            cause=cause,
        )

    best = _Snapshot(content=_read_bytes(note_path), score=score_issues(issues))
    history: list[AttemptOutcome] = []
    last_cause = cause

    rounds = 0
    while rounds < max_rounds:
        _check_cancelled()
        rounds += 1
        ctx = FixContext(
            note_path=note_path,
            issues=tuple(issues),
            prior_attempts=tuple(history),
        )
        try:
            fixer(ctx)
        except Exception:  # noqa: BLE001 — a fixer crash is a dead round, not a raise
            _check_cancelled()
            history.append(AttemptOutcome(rounds, best.score, (last_cause,) if last_cause else ()))
            break

        _check_cancelled()
        passed, cause, issues = evaluate()
        last_cause = cause
        score = score_issues(issues)
        history.append(
            AttemptOutcome(rounds, score, (cause,) if cause else ())
        )
        if score < best.score:
            best = _Snapshot(content=_read_bytes(note_path), score=score)
        if passed:
            # The current on-disk bytes ARE the passing version.
            return FixLoopResult(
                passed=True,
                rounds_used=rounds,
                final_score=0,
                cause=None,
                reverted=False,
                attempts=tuple(history),
            )

    # Exhausted rounds without a clean pass. Ensure the BEST version is on
    # disk (a later regressing fix may have overwritten it).
    reverted = False
    current = _read_bytes(note_path)
    if current != best.content:
        _check_cancelled()
        guard = effect_guard or nullcontext
        with guard():
            if effect_recorder is not None:
                effect_recorder(note_path)
                record_postimage = getattr(
                    effect_recorder,
                    "record_postimage",
                    None,
                )
                if record_postimage is not None:
                    record_postimage(note_path, best.content)
            _write_bytes(note_path, best.content)
        reverted = True

    return FixLoopResult(
        passed=False,
        rounds_used=rounds,
        final_score=best.score,
        cause=last_cause,
        reverted=reverted,
        attempts=tuple(history),
    )


# ── A real LLM-backed informed fixer ────────────────────────────────────────


DEFAULT_FIX_SYSTEM_PROMPT = (
    "You are a note-repair assistant. You are given the FULL current text of "
    "a note that FAILED its validation gates, plus the list of blocking "
    "issues. Return the CORRECTED note text and NOTHING else — no preamble, "
    "no code fences, no commentary. Fix every listed issue while preserving "
    "the note's meaning, structure, and all correct content. Do not invent "
    "facts; only repair format/structure/links the issues call out."
)


def _default_render_fix_prompt(current: str, ctx: "FixContext") -> str:
    """Build the user prompt for the LLM fixer from the note + gate issues.

    Includes the prior-attempt history so a repeated failure nudges a
    different strategy (the *informed* part of the informed fixer).
    """
    lines: list[str] = []
    lines.append("## Blocking issues to fix")
    if ctx.issues:
        for i in ctx.issues:
            # Issue.__str__ renders "ERROR[field] RULE: message"; fall back
            # to repr for any non-Issue entry.
            lines.append(f"- {i}")
    else:
        lines.append("- (none reported — return the note unchanged)")
    if ctx.prior_attempts:
        lines.append("")
        lines.append("## Prior repair attempts (did not fully pass)")
        for a in ctx.prior_attempts:
            causes = ", ".join(a.causes) if a.causes else "—"
            lines.append(
                f"- round {a.round_n}: {a.score} issue(s) remained "
                f"(causes: {causes})"
            )
        lines.append("")
        lines.append(
            "Those attempts did not fully pass — try a different fix."
        )
    lines.append("")
    lines.append("## Current note text")
    lines.append(current)
    lines.append("")
    lines.append("Return the corrected note text only.")
    return "\n".join(lines)


def make_llm_fixer(
    backend,
    *,
    system_prompt: str = DEFAULT_FIX_SYSTEM_PROMPT,
    render_prompt: "Callable[[str, FixContext], str]" = _default_render_fix_prompt,
    max_tokens: int = 8000,
    encoding: str = "utf-8",
    budget: RunBudget | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
) -> "InformedFixer":
    """Build an informed fixer that repairs a note in place via ``backend``.

    Returns a ``FixContext -> None`` callable (the shape
    :func:`run_fix_loop` invokes). Each call reads the note's current text,
    renders a repair prompt from it + the gate's blocking issues + the
    prior-attempt history, asks ``backend`` for the corrected note, and
    writes the response back to ``ctx.note_path``. The fix loop owns the
    checkpoint-before-fix + revert-to-BEST safety, so a *worse* LLM repair
    can never overwrite a better earlier version — this fixer only has to
    attempt an improvement, not guarantee one.

    Fail-soft: an empty backend response (or an unreadable/empty note) is a
    no-op write — the loop re-gates, sees no improvement, and moves on
    (never crashes the worker; a fixer crash is already caught by the loop).

    Args:
        backend: An object with ``call(LLMRequest) -> LLMResponse`` (any
            :class:`~tessellum.composer.llm.LLMBackend`).
        system_prompt: The repair system prompt.
        render_prompt: ``(current_text, ctx) -> user_prompt`` — override to
            customize the repair instructions.
        max_tokens: Response cap (notes can be long — default 8000).
        encoding: Note file encoding.
        budget: Shared run budget charged immediately before each repair
            backend call. A refused charge leaves the note unchanged.
    """
    from tessellum.composer.llm import LLMRequest

    def _fixer(ctx: FixContext) -> None:
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError("fixer cancelled before backend dispatch")
        current = _read_bytes(ctx.note_path).decode(encoding, errors="replace")
        if not current:
            return  # nothing to repair against — no-op
        user_prompt = render_prompt(current, ctx)
        if budget is not None and not budget.try_spend(cost=1.0):
            return
        response = backend.call(
            LLMRequest(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
            )
        )
        corrected = (response.content or "").strip()
        if not corrected:
            return  # empty repair — leave the note as-is (no-op)
        if cancellation_check is not None and cancellation_check():
            raise InterruptedError("fixer cancelled before repair publication")
        guard = effect_guard or nullcontext
        with guard():
            content = corrected.encode(encoding)
            if effect_recorder is not None:
                effect_recorder(ctx.note_path)
                record_postimage = getattr(
                    effect_recorder,
                    "record_postimage",
                    None,
                )
                if record_postimage is not None:
                    record_postimage(ctx.note_path, content)
            _write_bytes(ctx.note_path, content)

    return _fixer


def _read_bytes(path: Path) -> bytes:
    try:
        return Path(path).read_bytes()
    except OSError:
        return b""


def _write_bytes(path: Path, content: bytes) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(target.stat().st_mode) if target.is_file() else None
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, target)
        try:
            descriptor = os.open(target.parent, os.O_RDONLY)
        except OSError:
            descriptor = None
        if descriptor is not None:
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    finally:
        temporary.unlink(missing_ok=True)


__all__ = [
    "AttemptOutcome",
    "FixContext",
    "FixLoopResult",
    "GateEvaluator",
    "InformedFixer",
    "score_issues",
    "run_fix_loop",
    "make_llm_fixer",
    "DEFAULT_FIX_SYSTEM_PROMPT",
]
