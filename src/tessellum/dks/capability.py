"""tessellum.dks.capability — the DKS↔runtime seam (Ports & Adapters).

P2 of the DKS refactor plan (decision b1a). The seam that makes the DKS kernel
invokable by the runtime WITHOUT the kernel importing the runtime's shapes — a
Ports-and-Adapters boundary whose ``CapabilityResult`` contract is **owned by
DKS and inverted onto the runtime** (the Dependency Rule / P1: DKS is the single
reasoning authority; the runtime and Composer are adapters).

Three pieces (all here, all pure — no runtime import, no vault write):

- ``Capability`` — the port: ``invoke(request) -> CapabilityResult``. The
  runtime depends on THIS protocol; DKS never depends on the runtime.
- ``CapabilityResult`` — a **warrant-bearing** envelope: status, effects,
  diagnostics, promotion_eligibility, the Toulmin ``warrant`` + calibrated
  ``qualifier``, and a ``replay_token``. P4 validators consume the *warrant*
  (the reason), not the internal shape.
- adapters (``adapt_cycle_result`` / ``adapt_run_result`` / a
  ``DigestionResult`` adapter is a runtime-side concern) that wrap a kernel
  result as a typed payload INSIDE a ``CapabilityResult`` — neither internal
  shape changes.
- ``DKSExecutor`` — workflow-side, NEVER writes: it invokes the kernel through
  the port, captures the result, and returns a *candidate* transaction. It
  does not rediscover a question, change the parent FZ, or continue into
  another cycle (those are P5 outer-loop decisions). This is where the
  replay-below-freeze discipline (P2/guardrail 2) is enforced: the executor
  emits an intent; deterministic downstream code (P3) renders + promotes.

The runtime registers ``dks_inquiry`` as a capability keyed on this port so the
supervisor drives the kernel through the SAME commit tail as ``native_digestion``
— adding a deployed capability (Athelas-Conv) later is a new adapter with zero
kernel change.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, runtime_checkable

from tessellum.dks.core import (
    DKSCycleResult,
    DKSRunResult,
    DKSWarrant,
)

CapabilityStatus = Literal["ok", "empty", "error"]
PromotionEligibility = Literal[
    "eligible",       # structurally sound; may proceed to gated promotion
    "needs_validation",  # requires an independent validator verdict (P4)
    "ineligible",     # a defect makes it un-promotable as-is
]


@dataclass(frozen=True)
class CapabilityEffect:
    """One proposed vault effect (a node/edge the kernel wants materialized).

    This is the runtime-neutral description; P3's ``DKSNoteCompiler`` maps it
    into the substrate's ``NoteIntentGraph``. The kernel never writes — it
    proposes effects the deterministic promotion path renders."""

    kind: str          # "note" | "edge" | "warrant" | ...
    folgezettel: str   # target FZ (or edge source for a relation)
    bb_role: str = ""  # empirical_observation | argument | counter_argument | ...
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CapabilityResult:
    """The warrant-bearing envelope a Capability returns (decision b1a).

    Carries the Toulmin ``warrant`` + calibrated ``qualifier`` so a P4 validator
    consumes the *reason* a conclusion is licensed, not the internal shape. The
    ``payload`` holds the un-changed kernel result (a ``DKSCycleResult`` /
    ``DKSRunResult`` / a ``DigestionResult``) for a typed downstream consumer.
    ``replay_token`` is the content id that makes the result deterministically
    replayable (P2 — replay reapplies bytes, never re-runs the model)."""

    status: CapabilityStatus
    effects: tuple[CapabilityEffect, ...]
    diagnostics: tuple[str, ...]
    promotion_eligibility: PromotionEligibility
    warrant: DKSWarrant | None
    qualifier: str
    replay_token: str
    payload: Any = None


@runtime_checkable
class Capability(Protocol):
    """The port. The runtime depends on this; DKS owns it (Dependency Rule)."""

    def invoke(self, request: Any) -> CapabilityResult: ...


# ── adapters: wrap a kernel result as a CapabilityResult (no shape change) ───


def _effects_from_cycle(cycle: DKSCycleResult) -> tuple[CapabilityEffect, ...]:
    """Derive the proposed vault effects from a cycle result — one per FZ node
    the cycle deposited, in FZ order. The kernel already knows its nodes via
    ``folgezettel_nodes``; we tag each with its BB role for P3's compiler."""
    effects: list[CapabilityEffect] = []
    effects.append(CapabilityEffect(
        kind="note", folgezettel=cycle.observation.folgezettel,
        bb_role="empirical_observation",
        payload={"summary": cycle.observation.summary},
    ))
    for arg in cycle.arguments or ((cycle.argument_a,) if cycle.argument_a else ()):
        if arg is None:
            continue
        effects.append(CapabilityEffect(
            kind="note", folgezettel=arg.folgezettel, bb_role="argument",
            payload={"claim": arg.warrant.claim, "evidence": arg.evidence},
        ))
    if cycle.argument_b is not None and not cycle.arguments:
        effects.append(CapabilityEffect(
            kind="note", folgezettel=cycle.argument_b.folgezettel, bb_role="argument",
            payload={"claim": cycle.argument_b.warrant.claim},
        ))
    if cycle.counter is not None:
        effects.append(CapabilityEffect(
            kind="note", folgezettel=cycle.counter.folgezettel,
            bb_role="counter_argument",
            payload={"broken_component": cycle.counter.broken_component},
        ))
    if cycle.pattern is not None:
        effects.append(CapabilityEffect(
            kind="note", folgezettel=cycle.pattern.folgezettel, bb_role="model",
            payload={"description": cycle.pattern.description},
        ))
    for rev in cycle.rule_revisions:
        effects.append(CapabilityEffect(
            kind="warrant", folgezettel=rev.folgezettel, bb_role="procedure",
            payload={"supersedes": rev.supersedes},
        ))
    return tuple(effects)


def _replay_token(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
        h.update(b"\0")
    return "dks:" + h.hexdigest()[:32]


def adapt_cycle_result(cycle: DKSCycleResult) -> CapabilityResult:
    """Wrap a single ``DKSCycleResult`` as a ``CapabilityResult`` (no change to
    the cycle). The surviving argument's warrant is the envelope's warrant; a
    gated cycle is ``empty`` (nothing was disputed)."""
    if cycle.escalation_decision == "gated":
        status: CapabilityStatus = "empty"
        eligibility: PromotionEligibility = "needs_validation"
    else:
        status = "ok"
        # a full loop revised a warrant → needs an independent validator (P4);
        # a short-circuit produced no revision → eligible to record as-is.
        eligibility = "needs_validation" if cycle.rule_revisions else "eligible"
    # the licensing warrant: the revised one if present, else argument A's.
    warrant = (
        cycle.rule_revisions[0].revised_warrant
        if cycle.rule_revisions
        else (cycle.argument_a.warrant if cycle.argument_a else None)
    )
    return CapabilityResult(
        status=status,
        effects=_effects_from_cycle(cycle),
        diagnostics=cycle.silent_failures,
        promotion_eligibility=eligibility,
        warrant=warrant,
        qualifier=warrant.qualifier if warrant else "",
        replay_token=_replay_token(
            cycle.cycle_id, cycle.mode, cycle.backend_id,
            *(e.folgezettel for e in _effects_from_cycle(cycle)),
        ),
        payload=cycle,
    )


def adapt_run_result(run: DKSRunResult) -> CapabilityResult:
    """Wrap a multi-cycle ``DKSRunResult``. Effects aggregate across cycles;
    the envelope warrant is the last active warrant (the run's net position)."""
    effects: tuple[CapabilityEffect, ...] = tuple(
        e for c in run.cycles for e in _effects_from_cycle(c)
    )
    warrant = run.final_warrants[-1] if run.final_warrants else None
    any_revision = any(c.rule_revisions for c in run.cycles)
    return CapabilityResult(
        status="ok" if run.cycles else "empty",
        effects=effects,
        diagnostics=tuple(f for c in run.cycles for f in c.silent_failures),
        promotion_eligibility="needs_validation" if any_revision else "eligible",
        warrant=warrant,
        qualifier=warrant.qualifier if warrant else "",
        replay_token=_replay_token(
            run.backend_id, *(e.folgezettel for e in effects)
        ),
        payload=run,
    )


# ── DKSExecutor — workflow-side, NEVER writes ────────────────────────────────


@dataclass(frozen=True)
class DKSCandidate:
    """A candidate transaction the executor returns — NOT a committed effect.

    Deterministic downstream code (P3's compiler + the substrate's publication
    path) turns this into a promoted vault transaction; the executor itself
    never touches the vault."""

    result: CapabilityResult
    base_snapshot_id: str | None
    parent_fz: str | None


class DKSExecutor:
    """Invoke the kernel through the port and return a candidate — never write.

    The executor pins the snapshot/version it planned against, invokes the
    kernel via a :class:`Capability`, and returns a :class:`DKSCandidate`. It
    MUST NOT rediscover a question, change the parent FZ, or continue into
    another cycle — those are P5 outer-loop decisions. Enforces P2
    (replay-below-freeze): it emits an intent; it does not promote."""

    def __init__(self, capability: Capability) -> None:
        self._capability = capability

    def execute(
        self,
        request: Any,
        *,
        base_snapshot_id: str | None = None,
        parent_fz: str | None = None,
    ) -> DKSCandidate:
        result = self._capability.invoke(request)
        return DKSCandidate(
            result=result,
            base_snapshot_id=base_snapshot_id,
            parent_fz=parent_fz,
        )


__all__ = [
    "CapabilityStatus",
    "PromotionEligibility",
    "CapabilityEffect",
    "CapabilityResult",
    "Capability",
    "adapt_cycle_result",
    "adapt_run_result",
    "DKSCandidate",
    "DKSExecutor",
]
