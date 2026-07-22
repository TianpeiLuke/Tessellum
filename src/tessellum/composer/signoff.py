"""Sign-off approver — the plan→execute gate, a graduated ladder.

Composer v4, Phase 6 (sign-off half). The `review → ready` transition
(plan is sound → begin the execution wave) is a **pluggable approver**
composed cheapest-first:

1. **Program gate** — a pure structural pre-filter (the plan-scope gate's
   predicates). If it fails, the plan is rejected outright (no point
   spending an agent on a structurally-broken plan). If it passes but the
   policy demands more scrutiny, escalate.
2. **Reviewer agent** — an agent-as-judge (the ``review-digestion-plan``
   skill as an approver) that makes the semantic calls a program can't.
   Returns an approve/reject verdict + a confidence.
3. **Human interruption** — a suspend/approve/resume checkpoint, escalated
   to **only** on low agent-confidence or high blast radius. This is the
   pipeline's single human-in-the-loop seam.

Composed so the expensive rungs run only when the cheap ones are
inconclusive. The policy (which rungs are enabled + escalation thresholds)
is chosen per run. The rung callables (agent judge, human prompt) are
injected — this module owns the *ladder logic*, not the model/UI calls
(IDENT-3: the program orchestrates; the agent/human produce the verdicts).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

SignOffDecision = Literal["approved", "rejected", "needs_human"]
"""A rung's verdict. ``needs_human`` means "escalate" (only the human rung
returns a terminal approved/rejected when reached)."""

SignOffRung = Literal["program", "agent", "human"]
"""Which rung produced the terminal decision."""


@dataclass(frozen=True)
class AgentVerdict:
    """A reviewer-agent's judgment on the plan.

    Attributes:
        approved: The agent's approve/reject call.
        confidence: 0..1 confidence in that call. Low confidence escalates
            to the human rung (rather than trusting a shaky agent verdict).
        reason: Optional human-readable rationale.
    """

    approved: bool
    confidence: float
    reason: str | None = None


@dataclass(frozen=True)
class SignOffPolicy:
    """Which rungs are active + the escalation thresholds.

    Attributes:
        use_agent: Run the reviewer-agent rung when the program gate
            passes. When ``False``, a program pass is terminal (approved).
        use_human: Allow escalation to the human rung. When ``False``, a
            low-confidence or high-blast-radius case is auto-decided by
            the agent verdict (no human seam).
        min_agent_confidence: Below this the agent verdict is not trusted
            on its own → escalate to human (if enabled).
        blast_radius_threshold: A plan touching more than this many notes
            is "high blast radius" → escalate to human review even on a
            confident agent approval.
    """

    use_agent: bool = True
    use_human: bool = False
    min_agent_confidence: float = 0.7
    blast_radius_threshold: int = 50


@dataclass(frozen=True)
class SignOffResult:
    """The terminal outcome of the approver ladder.

    Attributes:
        decision: ``approved`` | ``rejected`` | ``needs_human`` (the last
            only when the human rung is required but disabled/unavailable).
        deciding_rung: Which rung produced the decision.
        escalated: The rungs that were consulted beyond the program gate.
        reason: A short rationale for the terminal decision.
    """

    decision: SignOffDecision
    deciding_rung: SignOffRung
    escalated: tuple[SignOffRung, ...] = field(default_factory=tuple)
    reason: str | None = None


# Injected rung callables:
#   program_gate() -> (passed, reason)         — pure structural pre-filter
#   agent_judge()  -> AgentVerdict             — the reviewer-agent
#   human_prompt() -> bool (approved?)         — the suspend/approve/resume seam
ProgramGate = Callable[[], "tuple[bool, str | None]"]
AgentJudge = Callable[[], AgentVerdict]
HumanPrompt = Callable[[], bool]


def run_sign_off(
    *,
    program_gate: ProgramGate,
    policy: SignOffPolicy,
    blast_radius: int = 0,
    agent_judge: AgentJudge | None = None,
    human_prompt: HumanPrompt | None = None,
) -> SignOffResult:
    """Run the graduated approver ladder cheapest-first.

    Sequence:

    1. **Program gate.** If it fails → ``rejected`` at the program rung
       (never spend an agent on a structurally-broken plan).
    2. If ``policy.use_agent`` is ``False`` → the program pass is terminal
       (``approved`` at the program rung).
    3. **Agent rung.** Run ``agent_judge``. A confident approval **and**
       an under-threshold blast radius → ``approved`` at the agent rung.
       A confident *rejection* → ``rejected`` at the agent rung.
    4. **Escalate to human** when the agent is under-confident *or* the
       blast radius is high (a big change wants a human eye even on a
       confident approve). If ``policy.use_human`` + ``human_prompt`` are
       available → the human's call is terminal at the human rung; else →
       ``needs_human`` (surfaced for an out-of-band decision).

    Args:
        program_gate: The pure structural pre-filter.
        policy: Which rungs run + thresholds.
        blast_radius: How many notes the plan touches (drives high-blast
            escalation).
        agent_judge: The reviewer-agent callable (required if
            ``policy.use_agent``).
        human_prompt: The human suspend/approve/resume callable (used only
            when escalating and ``policy.use_human``).

    Returns:
        A :class:`SignOffResult`.
    """
    passed, reason = program_gate()
    if not passed:
        return SignOffResult(
            decision="rejected",
            deciding_rung="program",
            reason=reason or "program gate failed",
        )

    if not policy.use_agent or agent_judge is None:
        return SignOffResult(
            decision="approved",
            deciding_rung="program",
            reason="program gate passed; agent rung disabled",
        )

    verdict = agent_judge()
    escalated: tuple[SignOffRung, ...] = ("agent",)

    high_blast = blast_radius > policy.blast_radius_threshold
    low_confidence = verdict.confidence < policy.min_agent_confidence

    # A confident rejection is terminal at the agent rung.
    if not verdict.approved and not low_confidence:
        return SignOffResult(
            decision="rejected",
            deciding_rung="agent",
            escalated=escalated,
            reason=verdict.reason or "agent rejected the plan",
        )

    # A confident approval on a low-blast plan is terminal at the agent rung.
    if verdict.approved and not low_confidence and not high_blast:
        return SignOffResult(
            decision="approved",
            deciding_rung="agent",
            escalated=escalated,
            reason=verdict.reason or "agent approved with confidence",
        )

    # Otherwise escalate to the human rung.
    why = (
        "low agent confidence"
        if low_confidence
        else "high blast radius"
    )
    if policy.use_human and human_prompt is not None:
        approved_by_human = human_prompt()
        return SignOffResult(
            decision="approved" if approved_by_human else "rejected",
            deciding_rung="human",
            escalated=escalated + ("human",),
            reason=f"escalated to human ({why})",
        )

    return SignOffResult(
        decision="needs_human",
        deciding_rung="agent",
        escalated=escalated,
        reason=f"needs human review ({why}); human rung unavailable",
    )


__all__ = [
    "SignOffDecision",
    "SignOffRung",
    "AgentVerdict",
    "SignOffPolicy",
    "SignOffResult",
    "ProgramGate",
    "AgentJudge",
    "HumanPrompt",
    "run_sign_off",
]
