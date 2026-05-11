"""DKS confidence gating — decide when to run the full 7-component cycle.

Phase 5 of ``plans/plan_dks_implementation.md`` (v0.0.45). The plan
specifies a minimal interface: a callable
``(observation, warrants) -> float in [0, 1]``. Above the threshold the
cycle short-circuits to *observation + one argument*; at or below, the
full closed loop runs.

The rationale is dialectical adequacy + cost. From the MAD literature
(per FZ 2a):

  - When the observation matches a high-confidence existing warrant,
    running A vs B is wasted compute — they'll agree.
  - When the observation hits a contested warrant or a wholly new
    pattern, the full cycle is what makes the substrate *learn*.

The gate lets DKS run cheap on the easy cases and rich on the
contested ones, with telemetry on the gating decision so the threshold
itself becomes tunable from data.

This module ships only the *minimal* interface: a Protocol, two
trivial implementations (constant gate + constant-confidence model),
and a default threshold. The plan defers anything more sophisticated
(learned confidence, calibration, multi-model ensembles) beyond
v0.0.45.
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

    The plan's open questions defer learned/calibrated confidence to
    v0.2+. v0.0.45 ships a trivial ``ConstantConfidence`` (always
    returns the same score, useful for tests + for deliberately
    forcing every cycle through one path) so the gating *mechanism*
    is in place even when the *signal* is not.
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
    every cycle short-circuits). Both extremes are valid v0.0.45
    deployments while a real signal is being calibrated.
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


__all__ = [
    "EscalationDecision",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DKSConfidenceModel",
    "ConstantConfidence",
    "decide_escalation",
]
