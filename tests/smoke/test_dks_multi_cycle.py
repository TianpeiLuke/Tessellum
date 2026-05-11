"""Phase 3 smoke tests for the DKS multi-cycle orchestrator.

Phase 1 (v0.0.40) shipped `DKSCycle` — one observation, one cycle.
Phase 3 (v0.0.43) wraps N cycles together via `DKSRunner` and adds
warrant-revision diffing via `aggregate_warrant_changes`. These tests
cover:

  - Single-cycle and multi-cycle DKSRunner over MockBackend
  - Warrant threading: cycle N+1 sees cycle N's revised warrant
  - WarrantChange classification (added / revised / superseded)
  - aggregate_warrant_changes count helper
  - Initial warrant set is honoured
  - Short-circuit cycles do not emit warrant changes
"""

from __future__ import annotations

import json

import pytest

from tessellum.composer import (
    DKSObservation,
    DKSRunner,
    DKSRunResult,
    DKSWarrant,
    MockBackend,
    WarrantChange,
    aggregate_warrant_changes,
)


# ── Mock backend builders ───────────────────────────────────────────────────


def _arg_response(claim: str, warrant: str) -> str:
    return json.dumps(
        {
            "claim": claim,
            "data": "D",
            "warrant": warrant,
            "backing": "",
            "qualifier": "",
            "evidence": "E",
        }
    )


def _counter_response() -> str:
    return json.dumps(
        {
            "broken_component": "warrant",
            "counter_claim": "warrant fails here",
            "reason": "scope mismatch",
            "strength": "moderate",
        }
    )


def _pattern_response() -> str:
    return json.dumps(
        {
            "description": "warrant assumes uniform but reality has tails",
            "observed": ["tail-1"],
        }
    )


def _revision_response(supersedes: str = "") -> str:
    return json.dumps(
        {
            "claim": "Revised claim",
            "data": "D",
            "warrant": "Revised warrant",
            "backing": "",
            "qualifier": "",
            "supersedes": supersedes,
        }
    )


def _full_cycle_backend(supersedes: str = "") -> MockBackend:
    """Returns canned responses for one full closed-loop cycle."""
    return MockBackend(
        responses={
            "conservative": _arg_response(claim="A-claim", warrant="W-A"),
            "exploratory": _arg_response(claim="B-claim", warrant="W-B"),
            "counter-argument": _counter_response(),
            "pattern discovery": _pattern_response(),
            "rule revision": _revision_response(supersedes=supersedes),
        }
    )


def _short_circuit_backend() -> MockBackend:
    """Returns canned responses where A and B agree → cycle short-circuits."""
    return MockBackend(
        responses={
            "conservative": _arg_response(claim="same-claim", warrant="W"),
            "exploratory": _arg_response(claim="same-claim", warrant="W"),
        }
    )


# ── DKSRunner: single cycle ─────────────────────────────────────────────────


def test_runner_single_cycle_returns_run_result() -> None:
    obs = (DKSObservation(folgezettel="1", summary="obs-1"),)
    runner = DKSRunner(observations=obs, backend=_full_cycle_backend())
    result = runner.run()

    assert isinstance(result, DKSRunResult)
    assert result.cycle_count == 1
    assert result.closed_loop_count == 1
    assert len(result.cycles) == 1


def test_runner_single_cycle_records_added_warrant() -> None:
    """First cycle with empty initial_warrants and no supersedes → 'added'."""
    obs = (DKSObservation(folgezettel="1", summary="obs-1"),)
    result = DKSRunner(observations=obs, backend=_full_cycle_backend()).run()

    assert len(result.warrant_changes) == 1
    change = result.warrant_changes[0]
    assert change.kind == "added"
    assert change.warrant is not None
    assert change.warrant.warrant == "Revised warrant"
    assert change.superseded_fz is None


def test_runner_records_revised_and_superseded_pair_when_supersedes_set() -> None:
    """Cycle that supersedes a prior FZ → two changes: revised + superseded."""
    obs = (DKSObservation(folgezettel="1", summary="obs-1"),)
    backend = _full_cycle_backend(supersedes="0a")
    result = DKSRunner(observations=obs, backend=backend).run()

    # 2 entries: one 'revised' carrying the new warrant; one 'superseded' carrying the retired FZ.
    assert len(result.warrant_changes) == 2
    kinds = {c.kind for c in result.warrant_changes}
    assert kinds == {"revised", "superseded"}

    revised = next(c for c in result.warrant_changes if c.kind == "revised")
    superseded = next(c for c in result.warrant_changes if c.kind == "superseded")

    assert revised.warrant is not None
    assert revised.superseded_fz == "0a"
    assert superseded.warrant is None
    assert superseded.superseded_fz == "0a"


# ── DKSRunner: multi-cycle ──────────────────────────────────────────────────


def test_runner_multi_cycle_runs_each_observation() -> None:
    """Three observations → three cycles in order."""
    obs = (
        DKSObservation(folgezettel="1", summary="obs-1"),
        DKSObservation(folgezettel="2", summary="obs-2"),
        DKSObservation(folgezettel="3", summary="obs-3"),
    )
    result = DKSRunner(observations=obs, backend=_full_cycle_backend()).run()

    assert result.cycle_count == 3
    assert tuple(c.cycle_id for c in result.cycles) == ("1", "2", "3")


def test_runner_threads_warrants_into_subsequent_cycles() -> None:
    """Cycle N+1's input warrant set must contain cycle N's revised warrant.

    Since MockBackend produces the same revision text for every cycle, we
    check that ``final_warrants`` grew by one per cycle (3 cycles, 0 initial → 3 final).
    """
    obs = (
        DKSObservation(folgezettel="1", summary="o1"),
        DKSObservation(folgezettel="2", summary="o2"),
        DKSObservation(folgezettel="3", summary="o3"),
    )
    result = DKSRunner(
        observations=obs,
        backend=_full_cycle_backend(),
        initial_warrants=(),
    ).run()

    assert len(result.final_warrants) == 3
    # Each revised warrant has the same canned text → all 3 final warrants match.
    assert all(w.warrant == "Revised warrant" for w in result.final_warrants)


def test_runner_honors_initial_warrants() -> None:
    """A starting warrant set is preserved through to ``final_warrants``."""
    starting = (
        DKSWarrant(
            claim="seed-claim",
            data="seed-data",
            warrant="seed-warrant",
        ),
    )
    obs = (DKSObservation(folgezettel="1", summary="o1"),)
    result = DKSRunner(
        observations=obs,
        backend=_full_cycle_backend(),
        initial_warrants=starting,
    ).run()

    # final_warrants = initial (1) + 1 revision = 2
    assert len(result.final_warrants) == 2
    assert result.final_warrants[0].warrant == "seed-warrant"
    assert result.final_warrants[1].warrant == "Revised warrant"


def test_runner_short_circuit_cycle_yields_no_warrant_change() -> None:
    """When A and B agree the cycle short-circuits — no rule_revision, no
    warrant_changes entry."""
    obs = (DKSObservation(folgezettel="1", summary="o1"),)
    result = DKSRunner(observations=obs, backend=_short_circuit_backend()).run()

    assert result.cycle_count == 1
    assert result.closed_loop_count == 0
    assert result.warrant_changes == ()
    assert result.final_warrants == ()


def test_runner_mixed_short_circuit_and_closed_loop() -> None:
    """A backend that closes every cycle: 3 obs → 3 changes, all 'added'."""
    obs = tuple(
        DKSObservation(folgezettel=str(i), summary=f"obs-{i}") for i in range(1, 4)
    )
    result = DKSRunner(observations=obs, backend=_full_cycle_backend()).run()

    assert result.closed_loop_count == 3
    assert len(result.warrant_changes) == 3
    assert all(c.kind == "added" for c in result.warrant_changes)


# ── aggregate_warrant_changes helper ────────────────────────────────────────


def test_aggregate_returns_zero_counts_for_empty_input() -> None:
    counts = aggregate_warrant_changes(())
    assert counts == {"added": 0, "revised": 0, "superseded": 0}


def test_aggregate_counts_each_kind() -> None:
    changes = (
        WarrantChange(cycle_id="1", kind="added"),
        WarrantChange(cycle_id="2", kind="added"),
        WarrantChange(cycle_id="3", kind="revised"),
        WarrantChange(cycle_id="3", kind="superseded"),
        WarrantChange(cycle_id="4", kind="added"),
    )
    counts = aggregate_warrant_changes(changes)
    assert counts == {"added": 3, "revised": 1, "superseded": 1}


# ── Empty observations input ────────────────────────────────────────────────


def test_runner_empty_observations_returns_empty_run() -> None:
    result = DKSRunner(observations=(), backend=_full_cycle_backend()).run()
    assert result.cycle_count == 0
    assert result.closed_loop_count == 0
    assert result.warrant_changes == ()
    assert result.final_warrants == ()


def test_runner_records_elapsed_time() -> None:
    obs = (DKSObservation(folgezettel="1", summary="o1"),)
    result = DKSRunner(observations=obs, backend=_full_cycle_backend()).run()
    assert result.elapsed_ms >= 0
