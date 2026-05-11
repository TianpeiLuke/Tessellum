"""DKS finite-state-machine dispatcher — Phase 8 of plan_dks_expansion.

The deferred FZ 2a2 work: replaces the 7 hand-coded ``_step_*``
methods on :class:`tessellum.dks.core.DKSCycle` with a generic walker
over ``BB_SCHEMA``. The walker drives the FSM ⟨Q, Σ, δ, q₀, F⟩
formalised in FZ 2a2:

  Q  = the 8 BBTypes
  δ  = the 16-edge BB_SCHEMA (epistemic + navigation + DKS extensions)
  q₀ = BBType.EMPIRICAL_OBSERVATION (every cycle starts here)
  F  = {procedure, concept, argument-when-gated}

This module is **additive** — it does not break the existing
``DKSCycle`` API. ``DKSCycle.run()`` continues to drive the 7 hand-
coded step methods unchanged. ``DKSStateMachine.walk()`` is the
alternative dispatcher path that any future second walker (meta-DKS,
the Phase 10 multi-perspective expansion, etc.) consumes.

Per D7 (`plan_dks_expansion`): termination uses Dung grounded
labelling internally (the multi-perspective case generalises N=2's
adequacy). The ``closed_loop`` query is preserved on
:class:`tessellum.dks.core.DKSCycleResult` as a derived property
(``True`` iff the surviving warrant's grounded label is ``in`` and a
rule revision was emitted).

For v0.0.51 this lands as a *thin* dispatcher around the same step
logic ``DKSCycle`` uses — proving the FSM walker is equivalent to the
hand-coded path. The transition-handler registry surface lets a
future caller (meta-DKS, Phase 9) inject custom handlers for one BB
edge without touching the cycle-level code.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol

from tessellum.bb.types import BBType, EpistemicEdgeType
from tessellum.composer.llm import LLMBackend
from tessellum.dks.core import (
    DKSCycle,
    DKSCycleResult,
    DKSObservation,
    DKSWarrant,
)


# ── BBPath — the FSM's walk record ─────────────────────────────────────────


@dataclass(frozen=True)
class BBPathStep:
    """One step on a BBPath: the (edge, produced-node) pair.

    ``edge`` is None for the initial state q₀ (the cycle root, before
    any transition has fired). All later steps carry a non-None edge
    naming the transition that produced ``node``.
    """

    edge: EpistemicEdgeType | None
    node: object  # BBNode subclass — typed by the BB type produced


@dataclass(frozen=True)
class BBPath:
    """Ordered record of an FSM walk.

    ``steps`` is the chronological list of (transition, produced-node)
    pairs starting from q₀. The walk's *length* is the number of
    transitions (which equals ``len(steps) - 1``, since step 0 is the
    initial observation with no transition).

    ``terminal_state`` is the BB type the walk ended at — must be in
    the FSM's accepting set ``F``.
    """

    steps: tuple[BBPathStep, ...]
    terminal_state: BBType
    elapsed_ms: float = 0.0

    @property
    def transition_count(self) -> int:
        """Number of transitions taken (excluding the initial state)."""
        return max(0, len(self.steps) - 1)

    @property
    def nodes(self) -> tuple[object, ...]:
        """All BBNode-typed instances along the walk, in order."""
        return tuple(s.node for s in self.steps)


# ── Transition handler protocol ────────────────────────────────────────────


class TransitionHandler(Protocol):
    """A function that produces the next BBNode given the cycle context.

    Handler signature: ``(context: dict, edge: EpistemicEdgeType) -> BBNode``.
    The context dict carries observation, prior nodes, warrants, and
    any backend access. Handlers are pure-functional with respect to
    the FSM (no side effects expected beyond returning a typed BBNode).
    """

    def __call__(
        self,
        context: dict,
        edge: EpistemicEdgeType,
    ) -> object:  # returns a BBNode subclass
        ...


# ── DKSStateMachine — the FSM walker ───────────────────────────────────────


@dataclass
class DKSStateMachine:
    """Drives one DKS cycle as a walk over BB_SCHEMA.

    For v0.0.51 the walker delegates to the existing
    :class:`DKSCycle` for the actual step logic — this proves the
    FSM dispatcher is *equivalent* to the hand-coded path before any
    future caller (meta-DKS, multi-perspective debate) builds on top.

    The transition-handler registry (`handlers`) is wired but
    unused by the default walk path: a future caller can register
    custom handlers for specific BB edges (e.g. meta-DKS replacing
    the standard step-6 pattern-discovery with a schema-edit-proposal
    handler) without touching the cycle-level DKS.

    Construction mirrors :class:`DKSCycle`:

        - ``backend``: LLMBackend (required)
        - ``confidence_model``: optional gate
        - ``confidence_threshold``: optional override
        - ``retrieval_client``: optional Phase 7 retrieval
        - ``semantic_disagreement``: optional Phase 7 step-4 mode
        - ``handlers``: optional registry for handler overrides

    ``walk(observation, warrants)`` returns the typed :class:`BBPath`.
    The corresponding :class:`DKSCycleResult` is also accessible via
    :meth:`last_result` for back-compat with v0.0.50 callers.
    """

    backend: LLMBackend
    confidence_model: object | None = None
    confidence_threshold: float | None = None
    retrieval_client: object | None = None
    semantic_disagreement: bool = False
    handlers: dict[tuple[BBType, BBType], TransitionHandler] = field(default_factory=dict)
    _last_result: DKSCycleResult | None = field(default=None, init=False, repr=False)

    def walk(
        self,
        observation: DKSObservation,
        warrants: tuple[DKSWarrant, ...] = (),
    ) -> BBPath:
        """Drive the FSM from q₀=OBS to a terminal state.

        v0.0.51 delegates to :class:`DKSCycle.run()` and lifts the
        per-component result into a :class:`BBPath`. Subsequent versions
        replace the delegate with a true handler-registry-driven walk;
        the BBPath shape stays stable.
        """
        start = time.monotonic()
        cycle = DKSCycle(
            observation,
            warrants,
            self.backend,
            confidence_model=self.confidence_model,
            confidence_threshold=self.confidence_threshold,
            retrieval_client=self.retrieval_client,
            semantic_disagreement=self.semantic_disagreement,
        )
        result = cycle.run()
        self._last_result = result

        steps = _result_to_steps(result)
        terminal = _terminal_state_from_result(result)
        elapsed_ms = (time.monotonic() - start) * 1000.0
        return BBPath(steps=steps, terminal_state=terminal, elapsed_ms=elapsed_ms)

    @property
    def last_result(self) -> DKSCycleResult | None:
        """The :class:`DKSCycleResult` from the most recent :meth:`walk`."""
        return self._last_result


# ── Result-to-path conversion ─────────────────────────────────────────────


def _result_to_steps(result: DKSCycleResult) -> tuple[BBPathStep, ...]:
    """Lift a :class:`DKSCycleResult` into the BBPath step sequence.

    Edge labels match BB_SCHEMA / BB_SCHEMA_DKS_EXTENSIONS:

        OBS → ARG (testing-collapsed)        step 2 + step 3
        ARG → CTR (challenging)              step 5
        CTR → MOD (pattern_of_failure)       step 6
        MOD → PRO|CON (codifying|reverse)    step 7

    Step 4 (contradicts edge) is *not* a state transition — it's an
    annotation on the existing ARG nodes. It does not appear as a
    BBPathStep.
    """
    from tessellum.bb.types import find_edge_type

    steps: list[BBPathStep] = []
    # q₀: observation
    steps.append(BBPathStep(edge=None, node=result.observation))

    # ARG transitions (step 2; optionally step 3 if not gated)
    obs_to_arg = find_edge_type(BBType.HYPOTHESIS, BBType.ARGUMENT)
    # The schema edge HYP→ARG carries label "testing"; OBS→ARG goes
    # *through* the implicit HYP collapse in DKS's compressed cycle.
    # We surface "testing" as the step-2 edge label for parity with
    # FZ 2a2's mapping table.
    steps.append(BBPathStep(edge=obs_to_arg, node=result.argument_a))
    if result.argument_b is not None:
        steps.append(BBPathStep(edge=obs_to_arg, node=result.argument_b))

    # Counter (step 5) — ARG → CTR via "challenging"
    if result.counter is not None:
        arg_to_ctr = find_edge_type(BBType.ARGUMENT, BBType.COUNTER_ARGUMENT)
        steps.append(BBPathStep(edge=arg_to_ctr, node=result.counter))

    # Pattern (step 6) — CTR → MOD via "pattern_of_failure" (DKS extension)
    if result.pattern is not None:
        ctr_to_mod = find_edge_type(BBType.COUNTER_ARGUMENT, BBType.MODEL)
        steps.append(BBPathStep(edge=ctr_to_mod, node=result.pattern))

    # Rule revision (step 7) — MOD → PRO|CON
    if result.rule_revision is not None:
        # The revision is a DKSRuleRevision; its corpus realisation
        # is either a procedure or a concept. The BBPathStep uses
        # the "codifying" edge (MOD→PRO) by convention; a future
        # MOD→CON variant lands when DKSRuleRevision exposes its
        # target BB type explicitly.
        mod_to_pro = find_edge_type(BBType.MODEL, BBType.PROCEDURE)
        steps.append(BBPathStep(edge=mod_to_pro, node=result.rule_revision))

    return tuple(steps)


def _terminal_state_from_result(result: DKSCycleResult) -> BBType:
    """Pick the FSM's terminal state from the result shape.

    Per FZ 2a2: F = {procedure, concept, argument-when-gated}.

    - rule_revision present → terminal at PROCEDURE (or CONCEPT —
      mapped to procedure today; future BB-typed revision distinguishes)
    - argument_b None (gated) → terminal at ARGUMENT
    - otherwise (short-circuit on A/B agreement) → terminal at ARGUMENT
    """
    if result.rule_revision is not None:
        return BBType.PROCEDURE
    return BBType.ARGUMENT


__all__ = [
    "BBPath",
    "BBPathStep",
    "TransitionHandler",
    "DKSStateMachine",
]
