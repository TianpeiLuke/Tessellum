"""DKS refactor P0 — the four release-blocker kernel defects (gate-to-P1).

A0.1 cycle-mode preservation: mode round-trips into DKSCycleResult.mode across
     every return shape (was hard-coded "fresh").
A0.2 vault-aware FZ allocation + digit/letter alternation: 1a -> 1a1 (not 1aa).
A0.3 active-warrant supersession: a superseded warrant leaves the active set.
A0.4 N=2 computed Dung labelling: grounded_labelling comes from the solver, not
     a hard-coded {A:out, B:in}.
"""

from __future__ import annotations

import json

from tessellum.composer import MockBackend
from tessellum.dks import (
    DKSCycle,
    DKSObservation,
    DKSRunner,
    DKSWarrant,
    allocate_cycle_fz,
)
from tessellum.dks.core import _next_child_of
from tessellum.dks.dung import DungAF, grounded_labelling


# ── helpers (mirror test_dks_core's mock shapes) ────────────────────────────


def _arg_response(claim: str, warrant: str) -> str:
    return json.dumps({
        "claim": claim, "data": "D", "warrant": warrant,
        "backing": "B", "qualifier": "q", "rebuttal": "r", "evidence": "E",
    })


def _counter_response() -> str:
    return json.dumps({
        "attacked_fz": "5a", "broken_component": "warrant",
        "counter_claim": "cc", "reason": "because", "strength": "moderate",
    })


def _pattern_response() -> str:
    return json.dumps({"description": "pattern", "observed": ["5a", "5b"]})


def _revision_response(supersedes: str = "") -> str:
    return json.dumps({
        "claim": "Revised", "data": "D", "warrant": "W'",
        "supersedes": supersedes,
    })


def _full_cycle_backend() -> MockBackend:
    return MockBackend(responses={
        "conservative": _arg_response("claim-A", "W-A"),
        "exploratory": _arg_response("claim-B", "W-B"),
        "counter-argument": _counter_response(),
        "pattern discovery": _pattern_response(),
        "rule revision": _revision_response(),
    })


def _gated_backend() -> MockBackend:
    # only argument A runs under a gate; a high-confidence model short-circuits.
    return MockBackend(responses={"conservative": _arg_response("claim-A", "W-A")})


# ── A0.1 — cycle-mode preservation ──────────────────────────────────────────


def test_mode_round_trips_full_cycle() -> None:
    for mode in ("fresh", "extend", "branch"):
        obs = DKSObservation(folgezettel="5", summary="x")
        result = DKSCycle(obs, (), _full_cycle_backend(), mode=mode).run()
        assert result.mode == mode  # was hard-coded "fresh"


def test_mode_round_trips_gated_cycle() -> None:
    obs = DKSObservation(folgezettel="5", summary="x")
    result = DKSCycle(
        obs, (), _gated_backend(), mode="extend",
        confidence_model=lambda o, w: 0.99, confidence_threshold=0.85,
    ).run()
    assert result.escalation_decision == "gated"
    assert result.mode == "extend"


def test_mode_default_is_fresh() -> None:
    obs = DKSObservation(folgezettel="5", summary="x")
    assert DKSCycle(obs, (), _full_cycle_backend()).run().mode == "fresh"


def test_runner_threads_per_observation_mode() -> None:
    obs = (
        DKSObservation(folgezettel="5", summary="a"),
        DKSObservation(folgezettel="6", summary="b"),
    )
    run = DKSRunner(obs, _full_cycle_backend(), modes=("fresh", "extend")).run()
    assert [c.mode for c in run.cycles] == ["fresh", "extend"]


# ── A0.2 — FZ allocation: digit/letter alternation ──────────────────────────


def test_next_child_alternates_digit_letter() -> None:
    assert _next_child_of("1", ()) == "1a"        # digit parent -> letter child
    assert _next_child_of("1a", ()) == "1a1"      # letter parent -> DIGIT child (not "1aa")
    assert _next_child_of("1a1", ()) == "1a1a"    # digit parent -> letter child
    assert _next_child_of("1a1a", ()) == "1a1a1"  # letter parent -> digit child


def test_next_child_finds_next_unused_sibling() -> None:
    # second letter child of a digit parent
    assert _next_child_of("1", ("1a",)) == "1b"
    # second digit child of a letter parent (NOT "1aa")
    assert _next_child_of("1a", ("1a1",)) == "1a2"
    # gap-filling
    assert _next_child_of("1a", ("1a1", "1a3")) == "1a2"


def test_allocate_extend_uses_alternation() -> None:
    # allocate_cycle_fz(extend) descends via _next_child_of
    assert allocate_cycle_fz(("1a",), mode="extend", parent_fz="1a") == "1a1"


def test_allocate_against_seeded_vault_is_collision_free() -> None:
    seeded = ("1", "1a", "1a1", "2", "2a")
    fz = allocate_cycle_fz(seeded, mode="extend", parent_fz="1a")
    assert fz not in seeded
    assert fz == "1a2"  # 1a1 taken → next digit child


def test_fresh_allocation_unchanged() -> None:
    assert allocate_cycle_fz((), mode="fresh") == "1"
    assert allocate_cycle_fz(("1", "2", "3"), mode="fresh") == "4"


# ── A0.3 — active-warrant supersession ──────────────────────────────────────


def test_supersession_removes_old_warrant_from_active_set() -> None:
    # cycle 1 authors a warrant at 5.<...>; cycle 2 supersedes it. The runner
    # must drop the superseded warrant from the active (final) set.
    obs = (
        DKSObservation(folgezettel="5", summary="first"),
        DKSObservation(folgezettel="6", summary="second"),
    )
    # cycle 1 revision has no supersedes (a fresh warrant); cycle 2 supersedes
    # cycle 1's revision FZ. The revision FZ is <pattern>.a under the cycle root
    # — we don't need to predict it exactly; instead assert the count is bounded
    # and the superseded content is gone.
    b1 = MockBackend(responses={
        "conservative": _arg_response("A", "W-A"),
        "exploratory": _arg_response("B", "W-B"),
        "counter-argument": _counter_response(),
        "pattern discovery": _pattern_response(),
        "rule revision": _revision_response(supersedes=""),  # cycle 1: add
    })
    run1 = DKSRunner((obs[0],), b1).run()
    assert len(run1.final_warrants) == 1  # one active warrant after cycle 1
    rev_fz = run1.cycles[0].rule_revisions[0].folgezettel

    # now a 2-cycle run where cycle 2 supersedes cycle 1's revision FZ.
    b2 = MockBackend(responses={
        "conservative": _arg_response("A", "W-A"),
        "exploratory": _arg_response("B", "W-B"),
        "counter-argument": _counter_response(),
        "pattern discovery": _pattern_response(),
        "rule revision": _revision_response(supersedes=rev_fz),
    })
    run2 = DKSRunner(obs, b2).run()
    # cycle 1 added a warrant; cycle 2 superseded it → exactly ONE active
    # warrant remains (the replacement), the superseded one is dropped.
    assert len(run2.final_warrants) == 1
    assert run2.final_warrants[0].warrant == "W'"  # the replacement
    # the change log still records the audit trail (added + revised + superseded)
    kinds = [c.kind for c in run2.warrant_changes]
    assert "superseded" in kinds


def test_initial_warrants_seed_active_set() -> None:
    obs = (DKSObservation(folgezettel="5", summary="x"),)
    initial = (DKSWarrant(claim="c0", data="d0", warrant="w0"),)
    # gated so no revision is emitted; the initial warrant survives.
    run = DKSRunner(
        obs, _gated_backend(), initial_warrants=initial,
        confidence_model=lambda o, w: 0.99, confidence_threshold=0.85,
    ).run()
    assert any(w.warrant == "w0" for w in run.final_warrants)


# ── A0.4 — N=2 computed Dung labelling ──────────────────────────────────────


def test_n2_grounded_labelling_is_computed_not_hardcoded() -> None:
    obs = DKSObservation(folgezettel="5", summary="x")
    result = DKSCycle(obs, (), _full_cycle_backend()).run()
    assert result.contradicts is not None  # full loop ran
    # rebuild the AF the kernel builds and compare to the solver directly.
    af = DungAF(
        arguments=(result.argument_a.folgezettel, result.argument_b.folgezettel),
        attacks=((result.contradicts.attacker_fz, result.contradicts.attacked_fz),),
    )
    expected = grounded_labelling(af)
    assert result.grounded_labelling == expected
    # a single attacker->attacked edge: attacker is `in`, attacked is `out`.
    attacker = result.contradicts.attacker_fz
    attacked = result.contradicts.attacked_fz
    assert result.grounded_labelling[attacker] == "in"
    assert result.grounded_labelling[attacked] == "out"


def test_n2_solver_matches_dung_on_single_and_mutual_attack() -> None:
    # single attack: b attacks a → a out, b in
    single = grounded_labelling(DungAF(arguments=("a", "b"), attacks=(("b", "a"),)))
    assert single == {"a": "out", "b": "in"}
    # mutual attack: neither is grounded → both undec
    mutual = grounded_labelling(
        DungAF(arguments=("a", "b"), attacks=(("a", "b"), ("b", "a")))
    )
    assert mutual == {"a": "undec", "b": "undec"}
