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

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


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
        rounds += 1
        ctx = FixContext(
            note_path=note_path,
            issues=tuple(issues),
            prior_attempts=tuple(history),
        )
        try:
            fixer(ctx)
        except Exception:  # noqa: BLE001 — a fixer crash is a dead round, not a raise
            history.append(AttemptOutcome(rounds, best.score, (last_cause,) if last_cause else ()))
            break

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


def _read_bytes(path: Path) -> bytes:
    try:
        return Path(path).read_bytes()
    except OSError:
        return b""


def _write_bytes(path: Path, content: bytes) -> None:
    Path(path).write_bytes(content)


__all__ = [
    "AttemptOutcome",
    "FixContext",
    "FixLoopResult",
    "GateEvaluator",
    "InformedFixer",
    "score_issues",
    "run_fix_loop",
]
