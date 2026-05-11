"""Phase 8 smoke tests for tessellum.dks.fsm — DKSStateMachine + BBPath.

The deferred FZ 2a2 dispatcher refactor. Covers:

  - DKSStateMachine.walk() produces a BBPath
  - The three FSM terminals (closed loop, short-circuit, gated) are reachable
  - BBPath terminal_state matches the FSM's F set
  - back-compat: same DKSCycleResult as DKSCycle.run() for matching backend
  - subclass-per-BBType dataclasses (D1) round-trip: bb_type populated correctly
  - DKSObservation/DKSArgument/DKSCounterArgument/DKSPattern inherit from
    EmpiricalObservationNode/ArgumentNode/CounterArgumentNode/ModelNode
"""

from __future__ import annotations

import json

import pytest

from tessellum.bb import (
    ArgumentNode,
    BBNode,
    BBType,
    CounterArgumentNode,
    EmpiricalObservationNode,
    ModelNode,
)
from tessellum.composer import MockBackend
from tessellum.dks import (
    BBPath,
    ConstantConfidence,
    DKSArgument,
    DKSCounterArgument,
    DKSCycle,
    DKSObservation,
    DKSPattern,
    DKSStateMachine,
    DKSWarrant,
)


# ── D1: subclass-per-BBType dataclasses ─────────────────────────────────────


def test_dks_observation_subclasses_empirical_observation_node():
    obs = DKSObservation(folgezettel="1", summary="x")
    assert isinstance(obs, EmpiricalObservationNode)
    assert isinstance(obs, BBNode)
    assert obs.bb_type is BBType.EMPIRICAL_OBSERVATION


def test_dks_argument_subclasses_argument_node():
    arg = DKSArgument(
        folgezettel="1a",
        warrant=DKSWarrant(claim="c", data="d", warrant="w"),
        evidence="e",
    )
    assert isinstance(arg, ArgumentNode)
    assert arg.bb_type is BBType.ARGUMENT


def test_dks_counter_argument_subclasses_counter_argument_node():
    ctr = DKSCounterArgument(
        folgezettel="1aa",
        attacked_fz="1a",
        broken_component="warrant",
        counter_claim="cc",
        reason="r",
        strength="moderate",
    )
    assert isinstance(ctr, CounterArgumentNode)
    assert ctr.bb_type is BBType.COUNTER_ARGUMENT


def test_dks_pattern_subclasses_model_node():
    pat = DKSPattern(folgezettel="1aaa", description="p")
    assert isinstance(pat, ModelNode)
    assert pat.bb_type is BBType.MODEL


def test_dks_node_subclasses_are_frozen():
    obs = DKSObservation(folgezettel="1", summary="x")
    with pytest.raises(Exception):  # FrozenInstanceError
        obs.bb_type = BBType.CONCEPT


def test_dks_observation_carries_bb_node_fields():
    """The parent BBNode fields (note_id, note_name, etc.) are available."""
    obs = DKSObservation(
        folgezettel="1",
        summary="x",
        note_id="archives/experiments/obs_1.md",
        note_name="obs_1",
        note_status="active",
    )
    assert obs.note_id == "archives/experiments/obs_1.md"
    assert obs.note_name == "obs_1"
    assert obs.note_status == "active"


# ── Mock backend builders ───────────────────────────────────────────────────


def _arg_response(claim: str, warrant: str = "W") -> str:
    return json.dumps(
        {
            "claim": claim, "data": "D", "warrant": warrant,
            "backing": "", "qualifier": "", "evidence": "E",
        }
    )


_FULL_LOOP_RESPONSES = {
    "conservative": _arg_response("A"),
    "exploratory": _arg_response("B"),
    "counter-argument": json.dumps(
        {
            "broken_component": "warrant",
            "counter_claim": "cc", "reason": "r", "strength": "moderate",
        }
    ),
    "pattern discovery": json.dumps({"description": "p", "observed": ["t"]}),
    "rule revision": json.dumps(
        {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
    ),
}


_SHORT_CIRCUIT_RESPONSES = {
    "conservative": _arg_response("same-claim"),
    "exploratory": _arg_response("same-claim"),
}


# ── DKSStateMachine.walk() — three terminals ────────────────────────────────


def test_walk_closed_loop_reaches_procedure_terminal():
    """Full closed-loop cycle terminates at PROCEDURE (the F state for
    rule revisions)."""
    sm = DKSStateMachine(backend=MockBackend(responses=_FULL_LOOP_RESPONSES))
    obs = DKSObservation(folgezettel="1", summary="o1")
    path = sm.walk(obs)
    assert isinstance(path, BBPath)
    assert path.terminal_state is BBType.PROCEDURE
    # Closed loop: 6 nodes (obs + A + B + counter + pattern + revision)
    assert len(path.steps) == 6


def test_walk_short_circuit_reaches_argument_terminal():
    """A == B agreement short-circuits; terminal is ARGUMENT (no revision)."""
    sm = DKSStateMachine(backend=MockBackend(responses=_SHORT_CIRCUIT_RESPONSES))
    obs = DKSObservation(folgezettel="1", summary="o1")
    path = sm.walk(obs)
    assert path.terminal_state is BBType.ARGUMENT
    # 3 nodes: obs + A + B (no counter/pattern/revision)
    assert len(path.steps) == 3


def test_walk_gated_reaches_argument_terminal():
    """Confidence-gated cycle terminates at ARGUMENT (no B, no later steps)."""
    sm = DKSStateMachine(
        backend=MockBackend(responses=_FULL_LOOP_RESPONSES),
        confidence_model=ConstantConfidence(0.99),
    )
    obs = DKSObservation(folgezettel="1", summary="o1")
    path = sm.walk(obs)
    assert path.terminal_state is BBType.ARGUMENT
    # 2 nodes: obs + A only
    assert len(path.steps) == 2


# ── BBPath structure ────────────────────────────────────────────────────────


def test_path_first_step_has_no_edge():
    """q₀ (the initial observation) has no incoming transition."""
    sm = DKSStateMachine(backend=MockBackend(responses=_SHORT_CIRCUIT_RESPONSES))
    obs = DKSObservation(folgezettel="1", summary="o1")
    path = sm.walk(obs)
    assert path.steps[0].edge is None
    assert path.steps[0].node is obs or path.steps[0].node == obs


def test_path_later_steps_have_typed_edges():
    """Steps after q₀ carry an EpistemicEdgeType."""
    sm = DKSStateMachine(backend=MockBackend(responses=_FULL_LOOP_RESPONSES))
    obs = DKSObservation(folgezettel="1", summary="o1")
    path = sm.walk(obs)
    for step in path.steps[1:]:
        assert step.edge is not None
        assert step.edge.source in set(BBType)
        assert step.edge.target in set(BBType)


def test_path_transition_count_is_steps_minus_one():
    sm = DKSStateMachine(backend=MockBackend(responses=_FULL_LOOP_RESPONSES))
    path = sm.walk(DKSObservation(folgezettel="1", summary="o1"))
    assert path.transition_count == len(path.steps) - 1


def test_path_nodes_property_returns_all_nodes_in_order():
    sm = DKSStateMachine(backend=MockBackend(responses=_FULL_LOOP_RESPONSES))
    path = sm.walk(DKSObservation(folgezettel="1", summary="o1"))
    nodes = path.nodes
    assert len(nodes) == len(path.steps)
    # First node is the observation
    assert isinstance(nodes[0], EmpiricalObservationNode)


# ── back-compat with DKSCycle.run() ────────────────────────────────────────


def test_walk_back_compat_equivalent_to_dkscycle_run():
    """For matching MockBackend responses, walk() produces the same
    cycle result as DKSCycle.run()."""
    backend = MockBackend(responses=_FULL_LOOP_RESPONSES)
    obs = DKSObservation(folgezettel="1", summary="o1")
    cycle_result = DKSCycle(obs, (), MockBackend(responses=_FULL_LOOP_RESPONSES)).run()

    sm = DKSStateMachine(backend=backend)
    sm.walk(obs)
    fsm_result = sm.last_result

    # Shape comparison: same number of FZ nodes
    assert fsm_result is not None
    assert len(cycle_result.folgezettel_nodes) == len(fsm_result.folgezettel_nodes)
    assert cycle_result.closed_loop == fsm_result.closed_loop


def test_walk_records_last_result():
    sm = DKSStateMachine(backend=MockBackend(responses=_FULL_LOOP_RESPONSES))
    assert sm.last_result is None
    sm.walk(DKSObservation(folgezettel="1", summary="o1"))
    assert sm.last_result is not None
    assert sm.last_result.closed_loop is True


# ── Transition handler registry (surface only; behaviour stays in DKSCycle) ─


def test_handlers_registry_accepts_callable():
    """The registry interface accepts custom handlers without using them."""
    sm = DKSStateMachine(
        backend=MockBackend(responses=_FULL_LOOP_RESPONSES),
        handlers={(BBType.ARGUMENT, BBType.COUNTER_ARGUMENT): lambda ctx, edge: None},
    )
    # walk still works (v0.0.51 doesn't dispatch through handlers yet)
    path = sm.walk(DKSObservation(folgezettel="1", summary="o1"))
    assert path.terminal_state is BBType.PROCEDURE
