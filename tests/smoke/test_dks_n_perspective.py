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
    DKSCycle,
    DKSObservation,
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


# ── Multi-revision authoring (Phase I.1 — v0.0.55) ─────────────────────────


def test_n2_emits_single_rule_revision_via_tuple():
    """N=2 disagreement → rule_revisions has 1 entry; legacy field mirrors it."""
    obs = _build_observation()
    responses = {
        "(conservative)": _argument_response("A"),
        "(exploratory)": _argument_response("B"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    result = DKSCycle(
        observation=obs, warrants=(), backend=MockBackend(responses=responses)
    ).run()
    assert len(result.rule_revisions) == 1
    assert result.rule_revisions[0] is result.rule_revision


def test_n2_agreement_emits_zero_revisions():
    """Short-circuit when arguments agree → rule_revisions empty + legacy None."""
    obs = _build_observation()
    backend = MockBackend(default=_argument_response("same"))
    result = DKSCycle(observation=obs, warrants=(), backend=backend).run()
    assert result.rule_revisions == ()
    assert result.rule_revision is None


def test_gated_emits_zero_revisions():
    obs = _build_observation()
    backend = MockBackend(default=_argument_response("X"))
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        confidence_model=lambda obs, warrants: 0.99,
        confidence_threshold=0.6,
    ).run()
    assert result.rule_revisions == ()
    assert result.escalation_decision == "gated"


def test_n3_multi_survivor_emits_one_revision_per_in():
    """N=3 with one OUT (A), two IN (B, C): the rule_revisions list has 2 entries."""
    obs = _build_observation()
    # Force a specific shape: arg_a == arg_b ≠ arg_c.
    # Edges: (B,A) — claims agree, no edge; (C,A) — claims differ, edge;
    #        (C,B) — claims differ, edge.
    # Grounded: C in (no attackers), A out (attacked by IN C), B out
    # (attacked by IN C).
    # Multi-survivor: only C is IN → 1 revision.
    # To get 2 INs we need a shape where two args are unattacked. Let's
    # use the "1 dissenter attacks 2 agreeing" shape inverted:
    # arg_a ≠ arg_b ≠ arg_c, all differ → 3 edges → labels: A out, B
    # out, C in (only 1 IN). So we need a more careful shape.
    # Two INs requires two unattacked arguments. With pairwise i<j
    # attacker-is-later, the only way two args are unattacked is if
    # both are the *first* indices — impossible since only index 0 has
    # no later attackers... unless the claims of args j ≤ k AGREE with
    # earlier args, so no edge fires for them.
    # Setup: A's claim = X, B's claim = X (agrees → no edge B,A), C's
    # claim = Y (differs → edges C,A and C,B). Grounded: A unattacked
    # by IN (B didn't attack; C did — but B's defence doesn't matter
    # since C attacks A directly). A: attacked by C IN → out. B same.
    # That still gives only C as the single IN.
    # The cleanest multi-IN shape with our attacker-is-later
    # convention: A and B claims differ from each other but neither
    # attacks one another in the right direction. Actually, since
    # edges are emitted for every (i, j) with differing claims, two
    # differing-claim siblings ALWAYS produce an attack edge.
    # Multi-IN requires UNDEFENDED mutual-disagreement OR a chain.
    # With our convention there's no mutual attack — every edge goes
    # one direction.
    # The right shape: A ≠ B ≠ C ≠ A with the natural attack pattern,
    # and a 4th argument D that's a defender. But our perspectives
    # tuple drives the indices.
    # Simpler shape: 4 perspectives where 3 agree, 1 dissents.
    # arg_a = X, arg_b = X, arg_c = X, arg_d = Y. Edges: (D, A), (D,
    # B), (D, C). Grounded: D in (no attackers), A/B/C all out
    # (attacked by IN D). Still only 1 IN.
    # The minimum-arity multi-IN shape: 4 perspectives, A and B agree,
    # C and D agree, A != C. Edges: (C, A), (C, B), (D, A), (D, B).
    # (A↔B and C↔D have no edges since claims agree internally; A↔C,
    # A↔D, B↔C, B↔D have edges.) Grounded: A attacked by C and D
    # (both undec initially), B same, C attacked by ... wait, no — C
    # is at index 2 and A is at index 0; edge (C, A) means C attacks
    # A, not the reverse. C has NO attackers (only later-index
    # perspectives can attack it). D also has no attackers. So C in,
    # D in, A out, B out — TWO INs (C and D).
    responses = {
        "(persp_a)": _argument_response("X"),
        "(persp_b)": _argument_response("X"),
        "(persp_c)": _argument_response("Y"),
        "(persp_d)": _argument_response("Y"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "multi-survivor": _REVISION_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=MockBackend(responses=responses),
        perspectives=("persp_a", "persp_b", "persp_c", "persp_d"),
    ).run()
    labels = result.grounded_labelling
    # Confirm the shape we engineered
    in_labels = sorted(fz for fz, lbl in labels.items() if lbl == "in")
    assert in_labels == ["9c", "9d"]
    # Multi-revision: 2 revisions (one per IN survivor)
    assert len(result.rule_revisions) == 2
    # Each anchored to its survivor's FZ (parent_fz for the revision
    # is the survivor's FZ, so revision FZ has the survivor's prefix)
    rev_fzs = [r.folgezettel for r in result.rule_revisions]
    assert all(fz.startswith("9c") or fz.startswith("9d") for fz in rev_fzs)
    # Legacy field mirrors first
    assert result.rule_revision is result.rule_revisions[0]


def test_n3_single_survivor_still_one_revision():
    """N=3 with only one IN survivor → 1 revision (the single-survivor path)."""
    obs = _build_observation()
    responses = {
        "(p1)": _argument_response("A"),
        "(p2)": _argument_response("B"),
        "(p3)": _argument_response("C"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=MockBackend(responses=responses),
        perspectives=("p1", "p2", "p3"),
    ).run()
    # Grounded labels per the existing N=3 test: C in, A out, B out.
    # Only 1 IN → 1 revision.
    in_labels = sorted(fz for fz, lbl in result.grounded_labelling.items() if lbl == "in")
    assert len(in_labels) == 1
    assert len(result.rule_revisions) == 1


def test_folgezettel_nodes_includes_all_revisions():
    """folgezettel_nodes property includes every emitted revision's FZ."""
    obs = _build_observation()
    responses = {
        "(persp_a)": _argument_response("X"),
        "(persp_b)": _argument_response("X"),
        "(persp_c)": _argument_response("Y"),
        "(persp_d)": _argument_response("Y"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=MockBackend(responses=responses),
        perspectives=("persp_a", "persp_b", "persp_c", "persp_d"),
    ).run()
    nodes = result.folgezettel_nodes
    # All 2 revision FZs are in the node list
    for rev in result.rule_revisions:
        assert rev.folgezettel in nodes
