"""Phase 1 smoke tests for the DKS core runtime.

Covers:
  - FZ allocator (three modes: fresh / extend / branch)
  - DKSCycle single-cycle dispatch
  - Closed-loop property
  - Short-circuit when A and B agree
  - 5-node FZ subtree deposition when the loop closes
  - Parent-child FZ relationships within the cycle's subtree
"""

from __future__ import annotations

import json

import pytest

from tessellum.composer import MockBackend
from tessellum.dks import (
    DKSArgument,
    DKSCycle,
    DKSCycleResult,
    DKSObservation,
    DKSWarrant,
    allocate_cycle_fz,
)


# ── FZ allocator ──────────────────────────────────────────────────────────


def test_allocate_fresh_first_root_is_1() -> None:
    assert allocate_cycle_fz((), mode="fresh") == "1"


def test_allocate_fresh_skips_used_roots() -> None:
    existing = ("1", "1a", "1a1", "2", "2a", "3")
    assert allocate_cycle_fz(existing, mode="fresh") == "4"


def test_allocate_fresh_finds_gap() -> None:
    existing = ("1", "3", "5")
    assert allocate_cycle_fz(existing, mode="fresh") == "2"


def test_allocate_fresh_handles_empty_strings() -> None:
    existing = ("", "1", "", "2", "")
    assert allocate_cycle_fz(existing, mode="fresh") == "3"


def test_allocate_extend_first_child_is_a() -> None:
    existing = ("1",)
    fz = allocate_cycle_fz(existing, mode="extend", parent_fz="1")
    assert fz == "1a"


def test_allocate_extend_next_sibling_letter() -> None:
    existing = ("1", "1a", "1b")
    fz = allocate_cycle_fz(existing, mode="extend", parent_fz="1")
    assert fz == "1c"


def test_allocate_extend_deep_descent() -> None:
    existing = ("1", "1a", "1a1", "1a1a", "1a1a1")
    # Branching off 1a1 with no other letter children of 1a1
    fz = allocate_cycle_fz(existing, mode="extend", parent_fz="1a1")
    assert fz == "1a1b"  # 1a1a is taken; next letter is b


def test_allocate_branch_same_machinery_as_extend() -> None:
    existing = ("1", "1a")
    # Branch is mechanically the same as extend at the allocator layer
    fz_extend = allocate_cycle_fz(existing, mode="extend", parent_fz="1")
    fz_branch = allocate_cycle_fz(existing, mode="branch", parent_fz="1")
    assert fz_extend == fz_branch == "1b"


def test_allocate_requires_parent_for_extend() -> None:
    with pytest.raises(ValueError, match="parent_fz"):
        allocate_cycle_fz((), mode="extend")


def test_allocate_requires_parent_for_branch() -> None:
    with pytest.raises(ValueError, match="parent_fz"):
        allocate_cycle_fz((), mode="branch")


# ── DKSCycle: short-circuit (A and B agree) ──────────────────────────────


def _arg_response(claim: str = "A", warrant: str = "W", evidence: str = "E") -> str:
    return json.dumps(
        {
            "claim": claim,
            "data": "D",
            "warrant": warrant,
            "evidence": evidence,
            "backing": "",
            "qualifier": "",
        }
    )


def test_cycle_short_circuits_when_args_agree() -> None:
    """If A and B produce the same claim, no contradiction → 3-node cycle."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response(claim="Same claim", warrant="W1"),
            "exploratory": _arg_response(claim="Same claim", warrant="W2"),
        }
    )
    obs = DKSObservation(folgezettel="5", summary="test observation")
    cycle = DKSCycle(observation=obs, warrants=(), backend=backend)
    result = cycle.run()

    assert isinstance(result, DKSCycleResult)
    assert result.contradicts is None
    assert result.counter is None
    assert result.pattern is None
    assert result.rule_revision is None
    assert result.closed_loop is False
    # 3 FZ nodes: observation + 2 arguments
    assert len(result.folgezettel_nodes) == 3
    assert result.folgezettel_nodes == ("5", "5a", "5b")


# ── DKSCycle: full closed loop ────────────────────────────────────────────


def _counter_response() -> str:
    return json.dumps(
        {
            "broken_component": "warrant",
            "counter_claim": "Warrant fails because of edge case X",
            "reason": "edge case the warrant doesn't cover",
            "strength": "moderate",
        }
    )


def _pattern_response() -> str:
    return json.dumps(
        {
            "description": "warrant assumes uniform behaviour but reality has tails",
            "observed": ["tail-1", "tail-2"],
        }
    )


def _revision_response() -> str:
    return json.dumps(
        {
            "claim": "Revised claim accommodating edge cases",
            "data": "D",
            "warrant": "Revised warrant W'",
            "supersedes": "5a",
        }
    )


def _full_cycle_backend() -> MockBackend:
    """Backend that produces a closed-loop cycle with claims that disagree."""
    return MockBackend(
        responses={
            "conservative": _arg_response(claim="claim-A", warrant="W-A"),
            "exploratory": _arg_response(claim="claim-B", warrant="W-B"),
            "counter-argument": _counter_response(),
            "pattern discovery": _pattern_response(),
            "rule revision": _revision_response(),
        }
    )


def test_cycle_closes_loop_when_args_disagree() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="5", summary="something happened")
    cycle = DKSCycle(observation=obs, warrants=(), backend=backend)
    result = cycle.run()

    assert result.contradicts is not None
    assert result.counter is not None
    assert result.pattern is not None
    assert result.rule_revision is not None
    assert result.closed_loop is True


def test_cycle_produces_6_fz_nodes_when_closed() -> None:
    """Closed cycle deposits 6 typed atomic notes (the disagreement is an
    edge, not a node, so it doesn't get its own FZ). Per FZ 2a1 mapping."""
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="5", summary="something happened")
    result = DKSCycle(obs, (), backend).run()

    nodes = result.folgezettel_nodes
    assert len(nodes) == 6
    assert nodes[0] == "5"      # observation = cycle root
    assert nodes[1] == "5a"     # argument A
    assert nodes[2] == "5b"     # argument B
    # nodes[3]: counter under attacked argument (5a → 5aa)
    # nodes[4]: pattern under counter (5aa → 5aaa)
    # nodes[5]: revision under pattern (5aaa → 5aaaa) — the leaf


def test_cycle_folgezettel_nodes_count_matches_components() -> None:
    """folgezettel_nodes contains every component that fired (excludes the
    contradicts edge which is a link, not a node)."""
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="5", summary="x")
    result = DKSCycle(obs, (), backend).run()
    # obs + arg_a + arg_b + counter + pattern + revision = 6 nodes
    # (the contradicts edge is not counted; that's the spatial distinction
    # named in thought_dks_fz_integration.md)
    assert len(result.folgezettel_nodes) == 6


# ── FZ subtree parent-child relationships ────────────────────────────────


def test_cycle_argument_fzs_descend_from_observation() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()

    # argument_a and argument_b both start with the observation FZ
    assert result.argument_a.folgezettel.startswith("7")
    assert result.argument_b.folgezettel.startswith("7")
    assert result.argument_a.folgezettel != result.argument_b.folgezettel


def test_cycle_counter_descends_from_attacked_argument() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()

    assert result.counter is not None
    # By default B attacks A; counter descends from arg_a's FZ
    assert result.counter.attacked_fz == result.argument_a.folgezettel
    assert result.counter.folgezettel.startswith(result.argument_a.folgezettel)


def test_cycle_pattern_descends_from_counter() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()

    assert result.pattern is not None and result.counter is not None
    assert result.pattern.folgezettel.startswith(result.counter.folgezettel)


def test_cycle_revision_descends_from_pattern() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()

    assert result.rule_revision is not None and result.pattern is not None
    assert result.rule_revision.folgezettel.startswith(
        result.pattern.folgezettel
    )


# ── Toulmin classification ───────────────────────────────────────────────


def test_counter_broken_component_constrained_to_literal() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="9", summary="x")
    result = DKSCycle(obs, (), backend).run()

    assert result.counter is not None
    assert result.counter.broken_component in (
        "premise",
        "warrant",
        "counter-example",
        "undercutting",
    )


def test_counter_broken_component_falls_back_on_garbage() -> None:
    """If the LLM returns an unknown broken_component, fall back to 'warrant'."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response(claim="A"),
            "exploratory": _arg_response(claim="B"),
            "counter-argument": json.dumps(
                {
                    "broken_component": "nonsense-value",
                    "counter_claim": "x",
                    "reason": "x",
                    "strength": "moderate",
                }
            ),
            "pattern discovery": _pattern_response(),
            "rule revision": _revision_response(),
        }
    )
    obs = DKSObservation(folgezettel="9", summary="x")
    result = DKSCycle(obs, (), backend).run()
    assert result.counter is not None
    assert result.counter.broken_component == "warrant"  # safe fallback


# ── Result metadata ──────────────────────────────────────────────────────


def test_cycle_records_elapsed_ms() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()
    assert result.elapsed_ms >= 0


def test_cycle_records_backend_id() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()
    assert result.backend_id == "mock"


# ── DKSWarrant serialisation ─────────────────────────────────────────────


def test_warrant_is_frozen_dataclass() -> None:
    w = DKSWarrant(claim="c", data="d", warrant="w")
    with pytest.raises(Exception):  # FrozenInstanceError
        w.claim = "modified"  # type: ignore[misc]


def test_argument_carries_full_warrant() -> None:
    backend = _full_cycle_backend()
    obs = DKSObservation(folgezettel="7", summary="x")
    result = DKSCycle(obs, (), backend).run()
    assert isinstance(result.argument_a, DKSArgument)
    assert isinstance(result.argument_a.warrant, DKSWarrant)
    assert result.argument_a.warrant.claim == "claim-A"
