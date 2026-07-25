"""DKS refactor P5 — autonomy loop: frontier + VOI stop + authority ladder.

Gate-to-P6/P7 deliverables:
 - a crafted divergent inquiry halts in `blocked` (never livelock);
 - a converging inquiry reaches understood with a strictly-decreasing Φ;
 - the VOI stop distinguishes understood (fixpoint / retired-below-λ) from
   truncated (budget);
 - the agent can never both select a move AND issue its own certificate
   (ACCEPT/RECONCILE capped below auto permanently).
"""

from __future__ import annotations

from tessellum.composer.planner_loop import Deficit, LoopPolicy, Revision
from tessellum.dks import (
    AuthorityLadder,
    AuthorityLadderError,
    EpistemicObligation,
    InquiryFrontier,
    run_bounded_inquiry,
    voi_stop_decision,
)


def _frontier(*eigs: float) -> InquiryFrontier:
    f = InquiryFrontier()
    for i, e in enumerate(eigs):
        f.add(EpistemicObligation(f"o{i}", f"q{i}", expected_information_gain=e))
    return f


# ── A5.1 frontier ranking ───────────────────────────────────────────────────


def test_frontier_ranks_by_voi_index() -> None:
    f = _frontier(0.2, 0.9, 0.5)
    assert [o.obligation_id for o in f.open()] == ["o1", "o2", "o0"]  # EIG desc


def test_frontier_deficit_counts_open_obligations() -> None:
    f = _frontier(0.9, 0.9)
    assert f.deficit().total == 2
    f.resolve("o0")
    assert f.deficit().total == 1


# ── A5.2 VOI-indexed stopping (understood vs truncated) ─────────────────────


def test_voi_stop_fixpoint_when_frontier_empty() -> None:
    d = voi_stop_decision(InquiryFrontier(), lambda_cost=0.5)
    assert d.should_stop and d.reason == "fixpoint" and d.understood


def test_voi_stop_retired_below_lambda() -> None:
    # every open obligation's EIG < λ → understood (not worth another write).
    d = voi_stop_decision(_frontier(0.1, 0.2), lambda_cost=0.5)
    assert d.should_stop and d.reason == "retired_below_lambda" and d.understood


def test_voi_does_not_stop_while_high_value_obligation_open() -> None:
    d = voi_stop_decision(_frontier(0.1, 0.9), lambda_cost=0.5)
    assert not d.should_stop and not d.understood


# ── A5.3 bounded scheduler (reuse planner_loop) ─────────────────────────────


def test_converging_inquiry_reaches_understood() -> None:
    # deficits 3 -> 2 -> 1 -> 0 (obligations discharged one per cycle).
    seq = iter([
        Revision("r1", "dks-inquiry", Deficit(undigested_terms=2)),
        Revision("r2", "dks-inquiry", Deficit(undigested_terms=1)),
        Revision("r3", "dks-inquiry", Deficit(undigested_terms=0)),
    ])
    res = run_bounded_inquiry(
        _frontier(0.9, 0.9, 0.9),  # deficit starts at 3
        propose=lambda prev: next(seq, None),
        policy=LoopPolicy(frozen_universe=True),
    )
    assert res.outcome == "complete"
    assert res.deficit_trace == (3, 2, 1, 0)


def test_divergent_inquiry_halts_blocked_not_livelock() -> None:
    # each proposal adds obligations (deficit grows) — frozen-universe halts it.
    n = iter([
        Revision("r1", "dks-inquiry", Deficit(undigested_terms=4)),
        Revision("r2", "dks-inquiry", Deficit(undigested_terms=5)),
    ])
    res = run_bounded_inquiry(
        _frontier(0.9, 0.9, 0.9),  # deficit 3
        propose=lambda prev: next(n, None),
        policy=LoopPolicy(frozen_universe=True),
    )
    assert res.outcome == "blocked"  # terminal, not a livelock


def test_bounded_inquiry_budget_stop_is_truncation() -> None:
    # a never-completing planner is halted by the fuel budget (truncated).
    res = run_bounded_inquiry(
        _frontier(0.9),
        propose=lambda prev: Revision("r", f"sig{id(prev)}", Deficit(undigested_terms=1)),
        policy=LoopPolicy(frozen_universe=False, fuel=3, depth_ceiling=999,
                          oscillation_window=999),
    )
    assert res.outcome == "blocked"
    assert "fuel" in res.reason


# ── A5.4 authority ladder: the mover is never the judge ─────────────────────


def test_execute_can_reach_auto() -> None:
    lad = AuthorityLadder()
    lad.set_rung("EXECUTE", "auto")
    assert lad.can_act_autonomously("EXECUTE")


def test_accept_and_reconcile_capped_below_auto_permanently() -> None:
    lad = AuthorityLadder()
    for stage in ("ACCEPT", "RECONCILE"):
        try:
            lad.set_rung(stage, "auto")
            raise AssertionError(f"{stage} should not reach auto")
        except AuthorityLadderError:
            pass
        # they CAN be autonomous-in-ODD, but never fully auto.
        lad.set_rung(stage, "auto_in_odd")
        assert lad.can_act_autonomously(stage)


def test_odd_exit_and_kill_switch_demote_to_suggest() -> None:
    lad = AuthorityLadder()
    lad.set_rung("PROPOSE", "auto")
    lad.set_rung("EXECUTE", "auto_in_odd")
    lad.odd_exit()
    assert lad.rung_for("PROPOSE") == "suggest"
    assert lad.rung_for("EXECUTE") == "suggest"
    # kill switch forces suggest even if rungs are set high.
    lad2 = AuthorityLadder()
    lad2.set_rung("EXECUTE", "auto")
    lad2.kill()
    assert lad2.rung_for("EXECUTE") == "suggest"
    assert not lad2.can_act_autonomously("EXECUTE")


def test_cap_is_a_class_invariant_not_just_the_setter() -> None:
    # Review nit (medium): constructing a ladder directly with a capped stage
    # at 'auto' must be rejected — the cap is a class invariant.
    try:
        AuthorityLadder(rungs={"ACCEPT": "auto"})
        raise AssertionError("constructing ACCEPT=auto should raise")
    except AuthorityLadderError:
        pass


def test_rung_for_defensively_recaps_direct_mutation() -> None:
    # even if .rungs is mutated past the setter, a capped stage never REPORTS
    # full auto (defensive re-cap in rung_for).
    lad = AuthorityLadder()
    lad.rungs["RECONCILE"] = "auto"  # bypass the setter
    assert lad.rung_for("RECONCILE") == "auto_in_odd"  # clamped on read
    # a capped stage therefore can never be fully autonomous via direct mutation
    assert lad.rung_for("RECONCILE") != "auto"


def test_unknown_rung_rejected_early() -> None:
    lad = AuthorityLadder()
    try:
        lad.set_rung("EXECUTE", "SUPER_AUTO")  # not in the enum
        raise AssertionError("unknown rung should raise")
    except AuthorityLadderError:
        pass


def test_agent_cannot_both_select_and_self_certify() -> None:
    # PROPOSE/EXECUTE (the mover) may be auto; ACCEPT (the judge) may not — so
    # no configuration lets the agent both choose a move and certify it.
    lad = AuthorityLadder()
    lad.set_rung("PROPOSE", "auto")
    lad.set_rung("EXECUTE", "auto")
    assert lad.can_act_autonomously("PROPOSE")
    # ACCEPT can never be pushed to full auto → the certificate is never
    # self-authorized by the same autonomous loop.
    try:
        lad.set_rung("ACCEPT", "auto")
        raise AssertionError("ACCEPT reached auto")
    except AuthorityLadderError:
        pass
