"""DKS confidence gating — decide when to run the full 7-component cycle.

The interface is a callable
``(observation, warrants) -> float in [0, 1]``. Above the threshold the
cycle short-circuits to *observation + one argument*; at or below, the
full closed loop runs.

Rationale (dialectical adequacy + cost):

  - When the observation matches a high-confidence existing warrant,
    running A vs B is wasted compute — they'll agree.
  - When the observation hits a contested warrant or a wholly new
    pattern, the full cycle is what makes the substrate *learn*.

The gate lets DKS run cheap on the easy cases and rich on the
contested ones, with telemetry on the gating decision so the threshold
itself becomes tunable from data.

Two implementations ship:

  - :class:`ConstantConfidence` — fixed score; the simplest gate.
  - :class:`CalibratedConfidence` — reads
    ``runs/dks/warrant_history.jsonl`` and scores observations against
    historical warrant-attack rates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, Sequence

from tessellum.dks.core import DKSObservation, DKSWarrant


EscalationDecision = Literal["gated", "full"]
"""Per-cycle telemetry tag: did this observation skip the full loop?"""


DEFAULT_CONFIDENCE_THRESHOLD: float = 0.85
"""Confidence above which the cycle short-circuits to observation + A.

Lean from ``plan_dks_implementation`` open questions: 0.85 — high enough
that easy cases skip the full cycle, low enough that contested cases
get the full 7-component treatment. Tunable from telemetry (see
``tessellum dks --report``).
"""


class DKSConfidenceModel(Protocol):
    """A scorer that returns confidence the existing warrants will hold.

    Inputs: the observation about to be processed, plus the current
    warrant set (initial + any prior cycle's revisions). Output:
    confidence ∈ [0, 1] that the observation is *adequately* covered
    by the existing warrants — i.e. that running the full cycle would
    return the same conclusion.

    Two built-in implementations:

    - :class:`ConstantConfidence` — fixed score; useful for tests and
      for deliberately forcing every cycle through one path.
    - :class:`CalibratedConfidence` — reads :class:`WarrantHistory`
      for a recency-weighted attack-rate signal.

    The gating *mechanism* lives in :func:`decide_escalation`; this
    protocol supplies the *signal*.
    """

    def __call__(
        self,
        observation: DKSObservation,
        warrants: Sequence[DKSWarrant],
    ) -> float:
        ...


@dataclass(frozen=True)
class ConstantConfidence:
    """Trivial confidence model — always returns the same score.

    Useful for tests (force gated vs. force full) and for callers who
    want to disable gating entirely (``ConstantConfidence(0.0)`` →
    every cycle runs the full loop; ``ConstantConfidence(1.0)`` →
    every cycle short-circuits). Both extremes are valid deployments
    while a real signal is being calibrated.
    """

    score: float = 0.0

    def __call__(
        self,
        observation: DKSObservation,
        warrants: Sequence[DKSWarrant],
    ) -> float:
        return self.score


def decide_escalation(
    confidence: float,
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> EscalationDecision:
    """Map a confidence score + threshold to an escalation decision.

    Returns ``"gated"`` when confidence > threshold (skip steps 2-7),
    ``"full"`` when confidence ≤ threshold (run the full closed loop).
    The strict-greater rule is deliberate — equality at the threshold
    falls through to the full cycle, preserving safety bias.
    """
    return "gated" if confidence > threshold else "full"


# ── CalibratedConfidence ─────────────────────────────────────────────────


DEFAULT_TARGET_FALSE_GATE_RATE: float = 0.10
"""Default tolerance for the calibration loop.

A "false gate" = a cycle the model would have gated where the full
cycle would have closed-looped (i.e. a contradiction *would* have been
found). 10% is the Pareto-balanced default. Configurable via
constructor + CLI.
"""


DEFAULT_RECENCY_HALFLIFE_CYCLES: int = 50
"""Cycles after which a historical warrant change loses half its weight.

The attack-rate signal is computed as a recency-weighted average over
``WarrantHistory``. With halflife=50, a "revised" event 50 cycles ago
weighs 0.5× a recent one; 100 cycles ago weighs 0.25×; and so on.
"""


@dataclass(frozen=True)
class CalibrationResult:
    """Output of a calibration run over past ``runs/dks/`` traces.

    Reads per-cycle traces under ``runs_dir``, looks at the recorded
    ``confidence_score`` + ``closed_loop`` fields on each cycle, and
    reports how the configured threshold would have behaved.

    - ``would_gate_count``: cycles whose recorded confidence > threshold
    - ``false_gate_count``: of those, cycles whose ``closed_loop`` was
      True (i.e. the gate would have prevented the full cycle from
      learning something the full cycle would have found)
    - ``false_gate_rate``: ``false_gate_count / would_gate_count``
    - ``suggested_threshold``: smallest threshold that achieves the
      ``target_false_gate_rate`` on past data (None if unachievable
      without gating zero cycles)
    """

    cycles_examined: int
    would_gate_count: int
    false_gate_count: int
    false_gate_rate: float
    current_threshold: float
    target_false_gate_rate: float
    suggested_threshold: float | None


@dataclass(frozen=True)
class CalibratedConfidence:
    """Confidence model that reads ``WarrantHistory`` for an attack-rate signal.

    Where :class:`ConstantConfidence` supplies the gating mechanism
    without a signal, this class supplies the minimal useful signal:
    the recency-weighted fraction of historical revisions that
    superseded a prior warrant (i.e. "attacked" it).

    Higher attack-rate → lower confidence in the current warrant set
    surviving → cycle runs the full loop. Empty history → neutral 0.5
    (no signal available; defer to the threshold).

    Future extension: combine with retrieval-similarity — observations
    similar to past closed-loop observations get lower confidence.
    Out of scope for the current confidence model.

    Args:
        warrant_history: WarrantHistory to read past events from. Empty
            history → neutral 0.5 baseline.
        recency_halflife_cycles: Halflife (in cycles) for the
            exponential decay. Default 50.
        baseline: Fallback score when history has no events. Default 0.5.
    """

    warrant_history: "WarrantHistory | None" = None  # noqa: F821 — fwd ref
    recency_halflife_cycles: int = DEFAULT_RECENCY_HALFLIFE_CYCLES
    baseline: float = 0.5

    def __call__(
        self,
        observation: DKSObservation,
        warrants: Sequence[DKSWarrant],
    ) -> float:
        if self.warrant_history is None:
            return self.baseline
        entries = self.warrant_history.all()
        if not entries:
            return self.baseline

        attack_rate = _recency_weighted_attack_rate(
            entries, halflife=self.recency_halflife_cycles
        )
        # Confidence = 1 - attack_rate, clamped.
        return max(0.0, min(1.0, 1.0 - attack_rate))


def _recency_weighted_attack_rate(
    entries: Sequence[object],  # Sequence[HistoryEntry]
    *,
    halflife: int,
) -> float:
    """Fraction of recent revisions that attack a prior warrant.

    The history records three event kinds: ``added`` (new warrant, not
    an attack), ``revised`` (replaces an old warrant — *is* an attack),
    ``superseded`` (the displaced-warrant tombstone of a ``revised``
    event; counted once via ``revised`` to avoid double-counting).

    Exponential-decay weighting: most-recent event has weight 1.0;
    each cycle older halves the weight every ``halflife`` steps.
    """
    weighted_total = 0.0
    weighted_attacks = 0.0
    # Iterate from most-recent backwards so index 0 is the latest.
    for i, entry in enumerate(reversed(entries)):
        kind = entry.change.kind  # type: ignore[attr-defined]
        if kind == "superseded":
            # The paired tombstone of "revised" — skip to avoid double-count.
            continue
        weight = 0.5 ** (i / halflife) if halflife > 0 else 1.0
        weighted_total += weight
        if kind == "revised":
            weighted_attacks += weight
    if weighted_total == 0.0:
        return 0.0
    return weighted_attacks / weighted_total


def calibrate_from_traces(
    runs_dir: "Path | str",  # noqa: F821 — fwd ref
    *,
    current_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    target_false_gate_rate: float = DEFAULT_TARGET_FALSE_GATE_RATE,
) -> CalibrationResult:
    """Replay past DKS cycle traces to assess the current threshold.

    Reads every per-cycle trace JSON under ``runs_dir`` and computes:

    1. How many cycles would have been gated at ``current_threshold``
       (recorded confidence > threshold).
    2. Of those, how many actually closed-looped — i.e. the gate would
       have been *wrong* to fire (the full cycle found a contradiction
       worth keeping).
    3. The achieved false-gate rate vs ``target_false_gate_rate``.
    4. A suggested threshold that would hit the target rate.

    The threshold-suggestion uses the per-cycle recorded confidence
    scores; it picks the smallest threshold for which the achieved
    false-gate rate is ≤ target. Returns ``suggested_threshold=None``
    when no threshold in [0, 1] achieves the target with positive
    would-gate count.

    Args:
        runs_dir: Directory containing ``*_cycle_*.json`` traces (the
            same dir ``tessellum dks`` writes to).
        current_threshold: The threshold being calibrated.
        target_false_gate_rate: Acceptable false-gate rate.
    """
    import json as _json
    from pathlib import Path as _Path

    path = _Path(runs_dir).expanduser().resolve()
    if not path.is_dir():
        return CalibrationResult(
            cycles_examined=0,
            would_gate_count=0,
            false_gate_count=0,
            false_gate_rate=0.0,
            current_threshold=current_threshold,
            target_false_gate_rate=target_false_gate_rate,
            suggested_threshold=None,
        )

    # Collect (confidence, closed_loop) tuples from every cycle trace.
    samples: list[tuple[float, bool]] = []
    for cycle_path in sorted(path.glob("*_cycle_*.json")):
        try:
            payload = _json.loads(cycle_path.read_text(encoding="utf-8"))
        except (OSError, _json.JSONDecodeError):
            continue
        score = payload.get("confidence_score")
        if score is None:
            continue
        closed_loop = bool(payload.get("closed_loop", False))
        try:
            samples.append((float(score), closed_loop))
        except (TypeError, ValueError):
            continue

    would_gate = [(s, cl) for s, cl in samples if s > current_threshold]
    false_gates = [(s, cl) for s, cl in would_gate if cl]
    false_rate = (
        len(false_gates) / len(would_gate) if would_gate else 0.0
    )

    suggested = _suggest_threshold(samples, target_false_gate_rate)

    return CalibrationResult(
        cycles_examined=len(samples),
        would_gate_count=len(would_gate),
        false_gate_count=len(false_gates),
        false_gate_rate=round(false_rate, 4),
        current_threshold=current_threshold,
        target_false_gate_rate=target_false_gate_rate,
        suggested_threshold=suggested,
    )


def _suggest_threshold(
    samples: Sequence[tuple[float, bool]],
    target_false_gate_rate: float,
) -> float | None:
    """Find the smallest threshold where (false-gates / would-gates) ≤ target.

    Searches over the unique scores in samples (ascending). For each
    candidate threshold, computes the would-gate set and the false-gate
    rate. Returns the smallest threshold meeting the constraint (which
    gates the most cycles while staying under the false-gate budget).
    Returns ``None`` when no threshold with non-empty would-gate set
    achieves the target.
    """
    if not samples:
        return None
    unique_scores = sorted({s for s, _ in samples})
    best: float | None = None
    for candidate in unique_scores:
        would_gate = [(s, cl) for s, cl in samples if s > candidate]
        if not would_gate:
            continue
        false_count = sum(1 for _, cl in would_gate if cl)
        rate = false_count / len(would_gate)
        if rate <= target_false_gate_rate:
            best = candidate
            break  # smallest acceptable threshold; gates the most
    return best


__all__ = [
    "EscalationDecision",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DEFAULT_TARGET_FALSE_GATE_RATE",
    "DEFAULT_RECENCY_HALFLIFE_CYCLES",
    "DKSConfidenceModel",
    "ConstantConfidence",
    "CalibratedConfidence",
    "CalibrationResult",
    "decide_escalation",
    "calibrate_from_traces",
]
