"""tessellum.dks.autonomy — the outer control plane (decisions b2a + b6a).

P5 of the DKS refactor plan — the thinking-machine milestone: what makes DKS
self-driving, staged behind explicit gates so a wrong autonomous decision cannot
compound. Four pieces:

- A5.1 **Inquiry frontier** — an ``EpistemicObligation`` ledger (unresolved
  obligations with priority, expected information gain, and budget).
- A5.2 **VOI-indexed stopping** — a Gittins-style per-obligation index
  discharges an obligation when the marginal expected warrant-precision gain
  drops below ``λ`` (the cost of a vault write). A first-class ranking ``Φ``
  over the ledger must strictly decrease for a cycle to be a legal discharge;
  the EIG/stop signal is computed by the INDEPENDENT evaluator (P3 — never the
  reasoning model). Paired with a hard multi-dimensional budget, recording the
  termination reason so ``understood`` is distinguished from ``truncated``.
- A5.3 **Bounded scheduler** — REUSE the shipped ``composer.planner_loop`` (its
  monotone-``Deficit`` variant + depth/fuel/oscillation stops already prove
  halting). DKS supplies an epistemic ``Deficit`` (open-obligation count +
  residual uncertainty); it does NOT re-implement the halting loop.
- A5.4 **Per-capability authority ladder** — each stage gets an independent rung
  (``suggest → auto_with_veto → auto_in_odd → auto``). ``ACCEPT``/``RECONCILE``
  are capped below ``auto`` PERMANENTLY (the certificate never self-authorizes,
  P3). An ODD-exit tripwire demotes to ``suggest``; a kill switch forces it.

All pure: no clock, no model call here (the LLM planner + the independent
evaluator are injected). Determinism where it matters: ``Φ`` and the frontier
ordering are pure functions of the ledger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from tessellum.composer.planner_loop import (
    Deficit,
    LoopPolicy,
    LoopResult,
    Revision,
    run_planner_loop,
)

# ── A5.1 the inquiry frontier ───────────────────────────────────────────────


@dataclass(frozen=True)
class EpistemicObligation:
    """One unresolved obligation on the inquiry frontier.

    ``expected_information_gain`` (EIG) is the independent evaluator's estimate
    of how much resolving this obligation would raise warrant precision;
    ``priority`` is a caller hint; ``resolved`` marks a discharged obligation.
    The VOI index (below) ranks by EIG, discharging when EIG < ``lambda_cost``.
    """

    obligation_id: str
    question: str
    expected_information_gain: float = 0.0
    priority: int = 0
    resolved: bool = False


@dataclass
class InquiryFrontier:
    """The obligation ledger (A5.1). Pure ranking; the EIG values come from the
    independent evaluator, never the reasoning model (P3)."""

    obligations: list[EpistemicObligation] = field(default_factory=list)

    def add(self, obligation: EpistemicObligation) -> None:
        self.obligations.append(obligation)

    def open(self) -> list[EpistemicObligation]:
        """Unresolved obligations, ranked by VOI index (EIG desc, then priority
        desc, then id for determinism)."""
        return sorted(
            (o for o in self.obligations if not o.resolved),
            key=lambda o: (-o.expected_information_gain, -o.priority, o.obligation_id),
        )

    def resolve(self, obligation_id: str) -> None:
        self.obligations = [
            (o if o.obligation_id != obligation_id else _resolved(o))
            for o in self.obligations
        ]

    def deficit(self) -> Deficit:
        """The frozen-universe measure fed to the bounded scheduler (A5.3): the
        count of open obligations, mapped onto the substrate ``Deficit``'s
        ``undigested_terms`` axis (an open obligation is an undischarged
        knowledge debt)."""
        return Deficit(undigested_terms=len(self.open()))


def _resolved(o: EpistemicObligation) -> EpistemicObligation:
    return EpistemicObligation(
        obligation_id=o.obligation_id, question=o.question,
        expected_information_gain=o.expected_information_gain,
        priority=o.priority, resolved=True,
    )


# ── A5.2 VOI-indexed stopping ────────────────────────────────────────────────

TerminationReason = Literal[
    "fixpoint",           # the frontier is discharged — understood
    "retired_below_lambda",  # every remaining obligation's EIG < λ — understood
    "budget_exhausted",   # a hard budget stop fired — truncated, NOT understood
]


@dataclass(frozen=True)
class StopDecision:
    should_stop: bool
    reason: TerminationReason | None
    understood: bool  # True iff the stop is a principled discharge, not truncation


def voi_stop_decision(
    frontier: InquiryFrontier,
    *,
    lambda_cost: float,
) -> StopDecision:
    """A5.2 — should the inquiry stop, and is the result ``understood``?

    Stop with ``understood=True`` when the frontier is empty (``fixpoint``) or
    every remaining obligation's expected information gain is below ``λ`` (the
    write cost — ``retired_below_lambda``); i.e. no obligation is worth another
    vault write. This is the anti-non-termination guard (the AutoGPT failure
    mode). A budget stop (handled by the scheduler, A5.3) is ``truncated`` —
    NOT understood."""
    open_obligations = frontier.open()
    if not open_obligations:
        return StopDecision(True, "fixpoint", understood=True)
    if all(o.expected_information_gain < lambda_cost for o in open_obligations):
        return StopDecision(True, "retired_below_lambda", understood=True)
    return StopDecision(False, None, understood=False)


# ── A5.3 bounded scheduler (REUSE planner_loop) ─────────────────────────────


def run_bounded_inquiry(
    frontier: InquiryFrontier,
    *,
    propose,
    policy: LoopPolicy | None = None,
) -> LoopResult:
    """Drive the bounded inquiry via the SHIPPED ``run_planner_loop`` (A5.3).

    The frontier's open-obligation count is the frozen-universe ``Deficit``;
    the shipped loop's monotone-variant + depth/fuel/oscillation stops prove
    halting (a divergent inquiry halts ``blocked``, not livelock). DKS does not
    re-implement the loop — ``propose(prev_revision) -> next_revision | None``
    is the injected planner; each proposed revision must carry a deficit whose
    total (remaining open obligations) strictly decreases to be accepted in a
    frozen-universe episode."""
    initial = Revision(
        revision_id="inquiry:start",
        route_signature="dks-inquiry",
        deficit=frontier.deficit(),
    )
    return run_planner_loop(initial, propose=propose, policy=policy or LoopPolicy())


# ── A5.4 per-capability authority ladder ─────────────────────────────────────

AuthorityRung = Literal["suggest", "auto_with_veto", "auto_in_odd", "auto"]
Stage = Literal["DETECT", "FORM_FRONTIER", "PROPOSE", "ACCEPT", "EXECUTE", "RECONCILE"]

# Stages that may NEVER reach full ``auto`` — the certificate/promotion decision
# must always have a human or an independent validator in the loop (P3: the
# mover is never the judge).
_CAPPED_STAGES: frozenset[str] = frozenset({"ACCEPT", "RECONCILE"})
_RUNG_ORDER: dict[str, int] = {
    "suggest": 0, "auto_with_veto": 1, "auto_in_odd": 2, "auto": 3,
}


class AuthorityLadderError(Exception):
    pass


def _validate_rung(rung: str) -> None:
    if rung not in _RUNG_ORDER:
        raise AuthorityLadderError(
            f"unknown authority rung {rung!r}; valid: {sorted(_RUNG_ORDER)}"
        )


def _enforce_cap(stage: str, rung: str) -> None:
    if stage in _CAPPED_STAGES and _RUNG_ORDER[rung] >= _RUNG_ORDER["auto"]:
        raise AuthorityLadderError(
            f"stage {stage!r} is capped below 'auto' permanently "
            "(the certificate never self-authorizes)"
        )


@dataclass
class AuthorityLadder:
    """Per-capability, per-stage authority (A5.4). Each stage independently
    climbs ``suggest → auto_with_veto → auto_in_odd → auto``; ``ACCEPT`` and
    ``RECONCILE`` are permanently capped BELOW ``auto``. An ODD-exit tripwire or
    the kill switch forces every stage back to ``suggest``."""

    rungs: dict[Stage, AuthorityRung] = field(default_factory=dict)
    kill_switched: bool = False

    def __post_init__(self) -> None:
        # The ACCEPT/RECONCILE cap is a CLASS INVARIANT, not just a setter
        # rule: a ladder constructed directly with a capped stage at 'auto'
        # (AuthorityLadder(rungs={"ACCEPT":"auto"})) must be rejected, else the
        # "certificate never self-authorizes" guarantee could be bypassed.
        for stage, rung in self.rungs.items():
            _validate_rung(rung)
            _enforce_cap(stage, rung)

    def rung_for(self, stage: Stage) -> AuthorityRung:
        if self.kill_switched:
            return "suggest"
        rung = self.rungs.get(stage, "suggest")
        # Defensive re-cap: even if ``rungs`` was mutated directly past the
        # setter, a capped stage can never REPORT full auto.
        if stage in _CAPPED_STAGES and _RUNG_ORDER.get(rung, 0) >= _RUNG_ORDER["auto"]:
            return "auto_in_odd"
        return rung

    def set_rung(self, stage: Stage, rung: AuthorityRung) -> None:
        """Set a stage's rung, enforcing the permanent ACCEPT/RECONCILE cap."""
        _validate_rung(rung)
        _enforce_cap(stage, rung)
        self.rungs[stage] = rung

    def can_act_autonomously(self, stage: Stage) -> bool:
        """True iff the stage may proceed without a human in the loop — i.e. its
        rung is ``auto_in_odd`` or ``auto`` and the kill switch is off. A capped
        stage can be autonomous-in-ODD but never fully ``auto``."""
        r = self.rung_for(stage)
        return _RUNG_ORDER[r] >= _RUNG_ORDER["auto_in_odd"]

    def odd_exit(self) -> None:
        """ODD-exit tripwire — demote every stage to ``suggest`` (A5.4)."""
        self.rungs = {stage: "suggest" for stage in self.rungs}

    def kill(self) -> None:
        self.kill_switched = True


__all__ = [
    "EpistemicObligation",
    "InquiryFrontier",
    "TerminationReason",
    "StopDecision",
    "voi_stop_decision",
    "run_bounded_inquiry",
    "AuthorityRung",
    "Stage",
    "AuthorityLadder",
    "AuthorityLadderError",
]
