"""P8 — bounded planner search with proven halt (A8.1-A8.3).

Proves the gate-to-P9 criteria: a crafted DIVERGENT bundle (each revision
surfaces new obligations) provably halts in `blocked` (never livelock); a
CONVERGING bundle reaches `complete` with a strictly-decreasing deterministic
deficit trace. Plus each hard stop — depth ceiling, fuel budget, oscillation,
planner-gives-up — terminates.
"""

from __future__ import annotations

import pytest

from tessellum.composer.planner_loop import (
    Deficit,
    LoopPolicy,
    Revision,
    run_planner_loop,
)


def _rev(rid, total, sig=None):
    # put the whole deficit in undigested_terms for simplicity.
    return Revision(revision_id=rid, route_signature=sig or rid,
                    deficit=Deficit(undigested_terms=total))


# ── convergence (frozen universe, strictly decreasing) ──────────────────────


def test_converging_bundle_completes_with_decreasing_trace() -> None:
    # deficits 5 -> 3 -> 1 -> 0.
    seq = iter([_rev("r1", 3, "s1"), _rev("r2", 1, "s2"), _rev("r3", 0, "s3")])

    def propose(prev):
        return next(seq, None)

    res = run_planner_loop(_rev("r0", 5, "s0"), propose=propose,
                           policy=LoopPolicy(frozen_universe=True))
    assert res.outcome == "complete"
    assert res.deficit_trace == (5, 3, 1, 0)
    # strictly decreasing until 0.
    assert all(a > b for a, b in zip(res.deficit_trace, res.deficit_trace[1:]))


def test_initial_zero_deficit_is_immediately_complete() -> None:
    res = run_planner_loop(_rev("r0", 0), propose=lambda p: None)
    assert res.outcome == "complete"
    assert res.fuel_spent == 0


# ── divergence provably halts (never livelock) ──────────────────────────────


def test_divergent_bundle_blocks_on_nondecreasing_deficit() -> None:
    # each revision surfaces MORE obligations (deficit grows) — frozen-universe
    # monotonicity catches it immediately.
    n = iter([_rev("r1", 6, "s1"), _rev("r2", 7, "s2")])

    def propose(prev):
        return next(n, None)

    res = run_planner_loop(_rev("r0", 5, "s0"), propose=propose,
                           policy=LoopPolicy(frozen_universe=True))
    assert res.outcome == "blocked"
    assert "did not strictly decrease" in res.reason


def test_divergent_search_halts_at_depth_ceiling() -> None:
    # bounded-SEARCH mode (no monotonicity assumed): an endlessly "improving-
    # looking" planner is still halted by the depth ceiling.
    counter = {"i": 0}

    def propose(prev):
        counter["i"] += 1
        # never reaches 0, always a fresh signature (no oscillation), deficit
        # wanders — only the ceiling/fuel can stop it.
        return _rev(f"r{counter['i']}", 100, f"sig{counter['i']}")

    res = run_planner_loop(_rev("r0", 100, "s0"), propose=propose,
                           policy=LoopPolicy(frozen_universe=False,
                                             depth_ceiling=5, fuel=100,
                                             oscillation_window=999))
    assert res.outcome == "blocked"
    assert "revision-depth ceiling" in res.reason
    assert len(res.revisions) - 1 == 5


def test_fuel_budget_halts_search() -> None:
    def propose(prev):
        return _rev("r", 100, "same_but_no_osc_check")  # relies on fuel

    res = run_planner_loop(_rev("r0", 100, "s0"), propose=propose,
                           policy=LoopPolicy(frozen_universe=False,
                                             depth_ceiling=999, fuel=3,
                                             oscillation_window=999))
    assert res.outcome == "blocked"
    assert "fuel budget" in res.reason
    assert res.fuel_spent == 3


def test_oscillation_detection_halts() -> None:
    # planner flip-flops between two route signatures — detected + stopped.
    sigs = iter(["A", "B", "A", "B", "A", "B"])

    def propose(prev):
        return _rev("r", 50, next(sigs))

    res = run_planner_loop(_rev("r0", 50, "start"), propose=propose,
                           policy=LoopPolicy(frozen_universe=False,
                                             depth_ceiling=999, fuel=999,
                                             oscillation_window=3))
    assert res.outcome == "blocked"
    assert "oscillation" in res.reason


def test_planner_gives_up_blocks() -> None:
    res = run_planner_loop(_rev("r0", 5, "s0"), propose=lambda p: None)
    assert res.outcome == "blocked"
    assert "declined" in res.reason


def test_deficit_total_sums_all_components() -> None:
    d = Deficit(ghosts=1, broken_links=2, undigested_terms=3, coverage_gaps=4)
    assert d.total == 10
    assert d.as_tuple() == (1, 2, 3, 4)


def test_deficit_rejects_negative_components() -> None:
    # negative components would let total hit 0 by cancellation (a false
    # complete) — the well-founded N measure must reject them.
    for kw in ({"ghosts": -1}, {"broken_links": -5}, {"undigested_terms": -1}):
        with pytest.raises(ValueError):
            Deficit(**kw)


# ── review regressions: completion-before-oscillation + stall-not-cumulative ─


def test_same_route_convergence_completes_not_falsely_blocked() -> None:
    # Review BUG1/BUG2 regression: a frozen-universe convergence 4->3->2->1->0
    # ALL on the SAME route signature (a planner fixing broken links keeps the
    # same route) must COMPLETE, not be flagged as oscillation. Default window.
    seq = iter([_rev("r1", 3, "X"), _rev("r2", 2, "X"),
                _rev("r3", 1, "X"), _rev("r4", 0, "X")])

    def propose(prev):
        return next(seq, None)

    res = run_planner_loop(_rev("r0", 4, "X"), propose=propose,
                           policy=LoopPolicy(frozen_universe=True))  # window=4
    assert res.outcome == "complete"
    assert res.deficit_trace == (4, 3, 2, 1, 0)


def test_deficit_zero_completes_even_if_signature_reused() -> None:
    # Review BUG1 regression: the discharging revision (deficit 0) reusing a
    # route signature is complete, checked BEFORE the oscillation stop.
    seq = iter([_rev("r1", 3, "X"), _rev("r2", 0, "X")])
    res = run_planner_loop(_rev("r0", 4, "X"),
                           propose=lambda p: next(seq, None),
                           policy=LoopPolicy(frozen_universe=True, oscillation_window=2))
    assert res.outcome == "complete"


def test_oscillation_counts_only_nonprogressing_stalls() -> None:
    # a planner that keeps the SAME route but keeps REDUCING the deficit is not
    # oscillating — the stall count resets on progress, so window=2 does not
    # falsely block a 5->4->3->2->1->0 same-route convergence.
    seq = iter([_rev(f"r{i}", d, "X") for i, d in enumerate([4, 3, 2, 1, 0], 1)])
    res = run_planner_loop(_rev("r0", 5, "X"),
                           propose=lambda p: next(seq, None),
                           policy=LoopPolicy(frozen_universe=True, oscillation_window=2))
    assert res.outcome == "complete"
    assert res.deficit_trace == (5, 4, 3, 2, 1, 0)
