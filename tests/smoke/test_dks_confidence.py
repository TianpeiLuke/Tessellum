"""Smoke tests for tessellum.dks.confidence (Phase 5, v0.0.45).

Covers:

  - DEFAULT_CONFIDENCE_THRESHOLD value
  - ConstantConfidence callable shape + boundary cases
  - decide_escalation strict-greater rule
  - DKSCycle.run() with a confidence model:
      * gated path: observation + argument A only (2 FZ nodes, no B)
      * full path: standard 6-node closed loop, escalation_decision="full"
      * default behaviour unchanged when no confidence model passed
  - DKSCycleResult.gated property
  - DKSRunner threads confidence model into every cycle
"""

from __future__ import annotations

import json


from tessellum.composer import MockBackend
from tessellum.dks import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    ConstantConfidence,
    DKSCycle,
    DKSObservation,
    DKSRunner,
    DKSWarrant,
    decide_escalation,
)


# ── Constants ───────────────────────────────────────────────────────────────


def test_default_threshold_is_zero_point_eight_five():
    """Per plan_dks_implementation.md open-question lean: 0.85."""
    assert DEFAULT_CONFIDENCE_THRESHOLD == 0.85


# ── ConstantConfidence ──────────────────────────────────────────────────────


def test_constant_confidence_default_is_zero():
    obs = DKSObservation(folgezettel="1", summary="x")
    assert ConstantConfidence()(obs, ()) == 0.0


def test_constant_confidence_returns_set_score():
    obs = DKSObservation(folgezettel="1", summary="x")
    assert ConstantConfidence(0.9)(obs, ()) == 0.9
    assert ConstantConfidence(1.0)(obs, ()) == 1.0
    assert ConstantConfidence(0.5)(obs, ()) == 0.5


# ── decide_escalation ───────────────────────────────────────────────────────


def test_decide_escalation_strict_greater_threshold():
    """Equality at threshold falls through to FULL (safety bias)."""
    assert decide_escalation(0.86, 0.85) == "gated"
    assert decide_escalation(0.85, 0.85) == "full"
    assert decide_escalation(0.84, 0.85) == "full"


def test_decide_escalation_uses_default_threshold():
    assert decide_escalation(0.86) == "gated"
    assert decide_escalation(0.5) == "full"


# ── DKSCycle with confidence model ──────────────────────────────────────────


def _arg_response(claim: str, warrant: str = "W") -> str:
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


def _full_loop_backend() -> MockBackend:
    return MockBackend(
        responses={
            "conservative": _arg_response("A-claim"),
            "exploratory": _arg_response("B-claim"),
            "counter-argument": json.dumps(
                {
                    "broken_component": "warrant",
                    "counter_claim": "cc",
                    "reason": "r",
                    "strength": "moderate",
                }
            ),
            "pattern discovery": json.dumps(
                {"description": "p", "observed": ["t"]}
            ),
            "rule revision": json.dumps(
                {
                    "claim": "R",
                    "data": "D",
                    "warrant": "Rw",
                    "supersedes": "",
                }
            ),
        }
    )


def test_cycle_without_confidence_model_runs_full_loop():
    """Phase 1 behaviour: no confidence model → full closed loop."""
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(obs, (), _full_loop_backend()).run()
    assert result.escalation_decision == "full"
    assert result.confidence_score is None
    assert result.argument_b is not None  # full path produces B
    assert result.closed_loop is True
    assert result.gated is False
    assert len(result.folgezettel_nodes) == 6


def test_cycle_with_high_confidence_gates():
    """confidence > threshold → cycle skips steps 3-7."""
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(
        obs,
        (),
        _full_loop_backend(),
        confidence_model=ConstantConfidence(0.95),
    ).run()

    assert result.escalation_decision == "gated"
    assert result.gated is True
    assert result.confidence_score == 0.95
    assert result.argument_a is not None
    assert result.argument_b is None  # B skipped
    assert result.contradicts is None
    assert result.counter is None
    assert result.pattern is None
    assert result.rule_revision is None
    assert result.closed_loop is False
    # 2 FZ nodes: observation + A only
    assert len(result.folgezettel_nodes) == 2
    assert result.folgezettel_nodes == ("1", "1a")


def test_cycle_with_low_confidence_runs_full_loop():
    """confidence <= threshold → full cycle, but records the score."""
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(
        obs,
        (),
        _full_loop_backend(),
        confidence_model=ConstantConfidence(0.3),
    ).run()

    assert result.escalation_decision == "full"
    assert result.confidence_score == 0.3
    assert result.argument_b is not None
    assert len(result.folgezettel_nodes) == 6


def test_cycle_with_custom_threshold():
    """Caller can override the default threshold."""
    obs = DKSObservation(folgezettel="1", summary="x")
    # score = 0.6; default threshold 0.85 → full; custom threshold 0.5 → gated
    full = DKSCycle(
        obs, (), _full_loop_backend(),
        confidence_model=ConstantConfidence(0.6),
    ).run()
    gated = DKSCycle(
        obs, (), _full_loop_backend(),
        confidence_model=ConstantConfidence(0.6),
        confidence_threshold=0.5,
    ).run()
    assert full.escalation_decision == "full"
    assert gated.escalation_decision == "gated"


def test_cycle_at_threshold_falls_through_to_full():
    """Equality at threshold runs the full loop."""
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(
        obs,
        (),
        _full_loop_backend(),
        confidence_model=ConstantConfidence(DEFAULT_CONFIDENCE_THRESHOLD),
    ).run()
    assert result.escalation_decision == "full"
    assert result.argument_b is not None


# ── DKSRunner integration ───────────────────────────────────────────────────


def test_runner_threads_confidence_model_into_every_cycle():
    obs = tuple(
        DKSObservation(folgezettel=str(i), summary=f"o{i}") for i in range(1, 4)
    )
    result = DKSRunner(
        observations=obs,
        backend=_full_loop_backend(),
        confidence_model=ConstantConfidence(0.95),
    ).run()
    assert result.cycle_count == 3
    assert result.gated_count == 3
    assert result.closed_loop_count == 0
    # No revisions when every cycle gates
    assert result.warrant_changes == ()


# ── CalibratedConfidence (Phase 7) ──────────────────────────────────────────


def test_calibrated_confidence_empty_history_returns_baseline(tmp_path):
    """No history events → return the baseline (default 0.5)."""
    from tessellum.dks import CalibratedConfidence, WarrantHistory

    history = WarrantHistory(tmp_path / "empty.jsonl")
    model = CalibratedConfidence(warrant_history=history, baseline=0.42)
    obs = DKSObservation(folgezettel="1", summary="x")
    assert model(obs, ()) == 0.42


def test_calibrated_confidence_none_history_returns_baseline():
    """No history at all → baseline."""
    from tessellum.dks import CalibratedConfidence

    model = CalibratedConfidence(warrant_history=None, baseline=0.5)
    obs = DKSObservation(folgezettel="1", summary="x")
    assert model(obs, ()) == 0.5


def test_calibrated_confidence_all_added_returns_high_confidence(tmp_path):
    """History of only `added` events (no attacks) → confidence ≈ 1.0."""
    from tessellum.dks import (
        CalibratedConfidence,
        WarrantChange,
        WarrantHistory,
    )

    history = WarrantHistory(tmp_path / "h.jsonl")
    for i in range(5):
        history.record_change(
            WarrantChange(
                cycle_id=str(i), kind="added",
                warrant=DKSWarrant(claim=f"c{i}", data="d", warrant="w"),
            )
        )

    model = CalibratedConfidence(warrant_history=history)
    obs = DKSObservation(folgezettel="1", summary="x")
    # No attacks → attack_rate = 0 → confidence = 1.0
    assert model(obs, ()) == 1.0


def test_calibrated_confidence_all_revised_returns_low_confidence(tmp_path):
    """History of `revised` events (all attacks) → confidence ≈ 0."""
    from tessellum.dks import (
        CalibratedConfidence,
        WarrantChange,
        WarrantHistory,
    )

    history = WarrantHistory(tmp_path / "h.jsonl")
    for i in range(5):
        # Each revised event pairs with a superseded event in real runs;
        # here we record just the revised so the attack rate maxes out.
        history.record_change(
            WarrantChange(
                cycle_id=str(i), kind="revised",
                warrant=DKSWarrant(claim=f"c{i}", data="d", warrant="w"),
                superseded_fz="0a",
            )
        )

    model = CalibratedConfidence(warrant_history=history)
    obs = DKSObservation(folgezettel="1", summary="x")
    # All attacks → attack_rate = 1.0 → confidence = 0.0
    assert model(obs, ()) == 0.0


def test_calibrated_confidence_superseded_events_are_not_double_counted(tmp_path):
    """`revised` + `superseded` pair represents ONE attack; only the
    `revised` event contributes to the attack-rate signal."""
    from tessellum.dks import (
        CalibratedConfidence,
        WarrantChange,
        WarrantHistory,
    )

    history = WarrantHistory(tmp_path / "h.jsonl")
    history.record_change(WarrantChange(cycle_id="1", kind="added", warrant=DKSWarrant(claim="c", data="d", warrant="w")))
    history.record_change(WarrantChange(cycle_id="2", kind="revised", warrant=DKSWarrant(claim="c", data="d", warrant="w"), superseded_fz="0a"))
    history.record_change(WarrantChange(cycle_id="2", kind="superseded", superseded_fz="0a"))

    model = CalibratedConfidence(
        warrant_history=history, recency_halflife_cycles=10000
    )  # large halflife → roughly equal weights
    obs = DKSObservation(folgezettel="1", summary="x")
    score = model(obs, ())
    # 1 revised out of (1 added + 1 revised) = 0.5 attack rate, ignoring superseded.
    # Confidence = 1 - 0.5 = 0.5.
    assert 0.45 < score < 0.55


# ── calibrate_from_traces (Phase 7) ─────────────────────────────────────────


def test_calibrate_returns_zero_for_missing_dir(tmp_path):
    from tessellum.dks import calibrate_from_traces

    result = calibrate_from_traces(tmp_path / "missing")
    assert result.cycles_examined == 0
    assert result.would_gate_count == 0
    assert result.suggested_threshold is None


def test_calibrate_reports_recorded_false_gates(tmp_path):
    """A cycle trace with confidence=0.9 AND closed_loop=True is a false gate
    at threshold 0.5 — the model would have gated when the cycle found an
    attack."""
    import json as _json

    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()

    # Two cycle traces:
    # cycle_1: confidence=0.9 + closed_loop=True → false gate at threshold 0.5
    # cycle_2: confidence=0.3 + closed_loop=False → not gated
    (runs_dir / "20260101T000000Z_cycle_1.json").write_text(
        _json.dumps({"confidence_score": 0.9, "closed_loop": True, "cycle_id": "1"})
    )
    (runs_dir / "20260101T000000Z_cycle_2.json").write_text(
        _json.dumps({"confidence_score": 0.3, "closed_loop": False, "cycle_id": "2"})
    )

    from tessellum.dks import calibrate_from_traces

    result = calibrate_from_traces(runs_dir, current_threshold=0.5)
    assert result.cycles_examined == 2
    assert result.would_gate_count == 1  # cycle_1 has 0.9 > 0.5
    assert result.false_gate_count == 1
    assert result.false_gate_rate == 1.0


def test_runner_records_mixed_gated_and_full_when_threshold_split():
    """Custom threshold separates gated vs full at constant confidence."""
    obs = (
        DKSObservation(folgezettel="1", summary="o1"),
        DKSObservation(folgezettel="2", summary="o2"),
    )
    # Confidence 0.7, threshold 0.6 → both gated
    result_g = DKSRunner(
        observations=obs,
        backend=_full_loop_backend(),
        confidence_model=ConstantConfidence(0.7),
        confidence_threshold=0.6,
    ).run()
    assert result_g.gated_count == 2

    # Confidence 0.7, threshold 0.8 → both full
    result_f = DKSRunner(
        observations=obs,
        backend=_full_loop_backend(),
        confidence_model=ConstantConfidence(0.7),
        confidence_threshold=0.8,
    ).run()
    assert result_f.gated_count == 0
    assert result_f.closed_loop_count == 2
