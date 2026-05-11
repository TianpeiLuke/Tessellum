"""Smoke tests for Phase 10 N>2 perspective DKSCycle support.

Covers:

- Default ``("conservative", "exploratory")`` produces same output as
  v0.0.40-era cycle (back-compat).
- 3-perspective cycle produces 3 argument nodes; pairwise contradicts.
- Grounded labelling identifies the attacked argument.
- Multi-perspective short-circuit when all arguments agree.
- ``perspectives=()`` / single perspective raises ValueError.
- Duplicate perspectives raise ValueError.
- DKSCycleResult.arguments + contradicts_edges + grounded_labelling
  populated correctly.
"""

from __future__ import annotations

import json

import pytest

from tessellum.composer.llm import MockBackend
from tessellum.dks.core import (
    DKSArgument,
    DKSContradicts,
    DKSCycle,
    DKSObservation,
    DKSWarrant,
)


def _argument_response(claim: str) -> str:
    """Mock response for ``_step_argument``."""
    return json.dumps(
        {
            "claim": claim,
            "data": f"D[{claim}]",
            "warrant": f"W[{claim}]",
            "backing": "",
            "qualifier": "",
            "evidence": f"E[{claim}]",
        }
    )


_COUNTER_RESPONSE = json.dumps(
    {
        "broken_component": "warrant",
        "counter_claim": "c",
        "reason": "r",
        "strength": "moderate",
    }
)
_PATTERN_RESPONSE = json.dumps({"description": "p", "observed": ["t"]})
_REVISION_RESPONSE = json.dumps(
    {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
)


def _build_observation(fz: str = "9") -> DKSObservation:
    return DKSObservation(folgezettel=fz, summary="test observation")


# ── Default 2-perspective back-compat ──────────────────────────────────────


def test_default_perspectives_unchanged():
    """N=2 default produces same shape as v0.0.40-era cycle."""
    obs = _build_observation()
    # Default mock returns _argument_response("X") for both calls →
    # claims match → short-circuit at step 4. v0.0.40 behaviour.
    backend = MockBackend(default=_argument_response("X"))
    cycle = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
    )
    assert cycle.perspectives == ("conservative", "exploratory")
    result = cycle.run()
    assert result.argument_a is not None
    assert result.argument_b is not None
    assert result.contradicts is None  # claims agreed → short-circuit
    assert result.counter is None
    # v0.0.54 additive fields
    assert len(result.arguments) == 2
    assert result.contradicts_edges == ()


def test_n2_disagreement_populates_grounded_labelling():
    """N=2 disagreement → grounded_labelling has 'out' for A and 'in' for B."""
    obs = _build_observation()
    responses = {
        "(conservative)": _argument_response("A"),
        "(exploratory)": _argument_response("B"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    backend = MockBackend(responses=responses)
    result = DKSCycle(observation=obs, warrants=(), backend=backend).run()
    assert result.argument_a.warrant.claim == "A"
    assert result.argument_b.warrant.claim == "B"
    assert result.contradicts is not None
    assert result.grounded_labelling == {
        result.argument_a.folgezettel: "out",
        result.argument_b.folgezettel: "in",
    }
    assert result.contradicts_edges == (result.contradicts,)


# ── N>2 happy path ─────────────────────────────────────────────────────────


def test_three_perspectives_produces_three_arguments():
    obs = _build_observation()
    responses = {
        "(conservative)": _argument_response("A"),
        "(exploratory)": _argument_response("B"),
        "(empirical)": _argument_response("C"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    backend = MockBackend(responses=responses)
    cycle = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        perspectives=("conservative", "exploratory", "empirical"),
    )
    result = cycle.run()
    assert len(result.arguments) == 3
    # FZ positions: 9a, 9b, 9c
    fzs = [arg.folgezettel for arg in result.arguments]
    assert fzs == ["9a", "9b", "9c"]
    # Claims A / B / C all differ → pairwise: (B, A), (C, A), (C, B) = 3 edges
    assert len(result.contradicts_edges) == 3
    # Grounded labelling: A out, B & C in (each unattacked)
    # Wait — pairwise (C, B) means C attacks B; so B is attacked by both C
    # and there's also (B, A) meaning B attacks A. Let me reason again.
    # Per the implementation: (i, j) with i < j → "j attacks i" (later
    # perspective is attacker). So edges are:
    #   B attacks A  (j=1, i=0)
    #   C attacks A  (j=2, i=0)
    #   C attacks B  (j=2, i=1)
    # Grounded labelling: C has no attackers → in; B attacked by C (IN) → out;
    # A attacked by B (OUT) and C (IN) → out.
    labels = result.grounded_labelling
    assert labels["9c"] == "in"
    assert labels["9b"] == "out"
    assert labels["9a"] == "out"
    # The cycle's primary contradicts targets the lex-smallest "out" arg = 9a.
    assert result.contradicts.attacked_fz == "9a"


def test_three_perspectives_all_agree_short_circuits():
    obs = _build_observation()
    backend = MockBackend(default=_argument_response("X"))
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        perspectives=("conservative", "exploratory", "empirical"),
    ).run()
    assert len(result.arguments) == 3
    # All agree → no contradicts edges
    assert result.contradicts_edges == ()
    assert result.contradicts is None
    assert result.counter is None
    # All labels are "in"
    assert all(lbl == "in" for lbl in result.grounded_labelling.values())


def test_three_perspectives_two_agree_one_dissents():
    """A and B agree; C dissents → only C-vs-A and C-vs-B edges fire.

    Edges: C attacks A, C attacks B (since claim_c != claim_a == claim_b).
    Grounded: C in, A out, B out. Primary attacked is "9a" (lex smallest).
    """
    obs = _build_observation()
    responses = {
        "(conservative)": _argument_response("agreement"),
        "(exploratory)": _argument_response("agreement"),
        "(dissenter)": _argument_response("dissent"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    backend = MockBackend(responses=responses)
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        perspectives=("conservative", "exploratory", "dissenter"),
    ).run()
    assert len(result.contradicts_edges) == 2  # C→A, C→B
    labels = result.grounded_labelling
    assert labels["9c"] == "in"
    assert labels["9a"] == "out"
    assert labels["9b"] == "out"
    assert result.contradicts.attacked_fz == "9a"


# ── Gated path with N>2 ────────────────────────────────────────────────────


def test_gated_path_with_n3_still_emits_argument_a_only():
    """Confidence-gating short-circuits regardless of perspective count."""
    obs = _build_observation()
    backend = MockBackend(default=_argument_response("A"))
    # High confidence — gate fires
    cycle = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        confidence_model=lambda obs, warrants: 0.99,
        confidence_threshold=0.6,
        perspectives=("conservative", "exploratory", "empirical"),
    )
    result = cycle.run()
    assert result.escalation_decision == "gated"
    assert result.argument_a is not None
    assert result.argument_b is None
    assert result.arguments == (result.argument_a,)
    assert result.contradicts_edges == ()


# ── Validation: perspectives kwarg ─────────────────────────────────────────


def test_single_perspective_raises():
    with pytest.raises(ValueError, match="at least 2 entries"):
        DKSCycle(
            observation=_build_observation(),
            warrants=(),
            backend=MockBackend(),
            perspectives=("only_one",),
        )


def test_duplicate_perspectives_raise():
    with pytest.raises(ValueError, match="unique"):
        DKSCycle(
            observation=_build_observation(),
            warrants=(),
            backend=MockBackend(),
            perspectives=("conservative", "conservative"),
        )


def test_empty_perspectives_raises():
    with pytest.raises(ValueError):
        DKSCycle(
            observation=_build_observation(),
            warrants=(),
            backend=MockBackend(),
            perspectives=(),
        )


# ── FZ allocator for N>2 ───────────────────────────────────────────────────


def test_fz_positions_extend_alphabetically_for_n_perspectives():
    """FZ suffixes go a, b, c, ... — matching the perspective index."""
    obs = _build_observation(fz="42")
    backend = MockBackend(default=_argument_response("X"))
    cycle = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        perspectives=("p1", "p2", "p3", "p4", "p5"),
    )
    result = cycle.run()
    fzs = [a.folgezettel for a in result.arguments]
    assert fzs == ["42a", "42b", "42c", "42d", "42e"]


# ── Result-shape invariants ────────────────────────────────────────────────


def test_arguments_tuple_is_immutable():
    obs = _build_observation()
    backend = MockBackend(default=_argument_response("X"))
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        perspectives=("p1", "p2", "p3"),
    ).run()
    assert isinstance(result.arguments, tuple)


def test_contradicts_edges_attacker_is_later_perspective():
    """For every emitted edge, attacker_fz > attacked_fz alphabetically."""
    obs = _build_observation()
    responses = {
        "(p1)": _argument_response("A"),
        "(p2)": _argument_response("B"),
        "(p3)": _argument_response("C"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    backend = MockBackend(responses=responses)
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        perspectives=("p1", "p2", "p3"),
    ).run()
    for edge in result.contradicts_edges:
        # attacker is the later-index perspective → larger suffix
        assert edge.attacker_fz > edge.attacked_fz
