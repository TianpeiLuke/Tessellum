"""Smoke tests for `tessellum dks --report` and Phase 5 CLI extras.

Phase 5 (v0.0.45) wires three new CLI surfaces:

  - ``--gate-confidence`` + ``--gate-threshold`` — force a
    ConstantConfidence model into the runner.
  - ``--report`` (+ ``--report-last``) — inter-cycle telemetry across
    past aggregate traces.
  - Warrant history JSONL log at ``<runs-dir>/warrant_history.jsonl``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tessellum.cli.main import main


# ── Shared fixtures ─────────────────────────────────────────────────────────


def _arg_response(claim: str) -> str:
    return json.dumps(
        {
            "claim": claim,
            "data": "D",
            "warrant": "W",
            "backing": "",
            "qualifier": "",
            "evidence": "E",
        }
    )


_FULL_LOOP_RESPONSES = {
    "conservative": _arg_response("A"),
    "exploratory": _arg_response("B"),
    "counter-argument": json.dumps(
        {
            "broken_component": "warrant",
            "counter_claim": "cc",
            "reason": "r",
            "strength": "moderate",
        }
    ),
    "pattern discovery": json.dumps({"description": "p", "observed": ["t"]}),
    "rule revision": json.dumps(
        {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
    ),
}


@pytest.fixture
def obs_jsonl(tmp_path) -> Path:
    p = tmp_path / "obs.jsonl"
    p.write_text(
        "\n".join(
            json.dumps({"summary": f"obs-{i}", "mode": "fresh"})
            for i in range(1, 4)
        )
        + "\n"
    )
    return p


@pytest.fixture
def mock_responses(tmp_path) -> Path:
    p = tmp_path / "responses.json"
    p.write_text(json.dumps(_FULL_LOOP_RESPONSES))
    return p


# ── --gate-confidence + --gate-threshold ────────────────────────────────────


def test_cli_high_gate_confidence_gates_every_cycle(obs_jsonl, mock_responses, tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--gate-confidence", "0.95",
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    # 3 gated, 0 closed
    assert "3 gated" in out
    assert "0 closed" in out

    # Aggregate trace reflects this
    agg = json.loads(next(runs_dir.glob("*_aggregate.json")).read_text())
    assert agg["cycle_count"] == 3
    assert agg["closed_loop_count"] == 0


def test_cli_low_gate_confidence_runs_full_loops(obs_jsonl, mock_responses, tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--gate-confidence", "0.0",
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "3 closed" in out
    assert "0 gated" in out


def test_cli_gate_threshold_overrides_default(obs_jsonl, mock_responses, tmp_path):
    """Constant confidence 0.7 + threshold 0.6 → gated (default 0.85 → full)."""
    runs_dir = tmp_path / "runs"
    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--gate-confidence", "0.7",
            "--gate-threshold", "0.6",
            "--runs-dir", str(runs_dir),
        ]
    )
    agg = json.loads(next(runs_dir.glob("*_aggregate.json")).read_text())
    cycles = []
    for tp in agg["cycle_traces"]:
        cycles.append(json.loads(Path(tp).read_text()))
    assert all(c["escalation_decision"] == "gated" for c in cycles)


def test_cli_gate_confidence_out_of_range_returns_2(obs_jsonl, capsys):
    code = main(
        ["dks", str(obs_jsonl), "--gate-confidence", "1.5", "--no-trace"]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "must be in [0.0, 1.0]" in err


# ── Warrant history JSONL ──────────────────────────────────────────────────


def test_cli_writes_warrant_history(obs_jsonl, mock_responses, tmp_path):
    """3-observation closed-loop run → 3 'added' entries in warrant_history.jsonl."""
    runs_dir = tmp_path / "runs"
    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--runs-dir", str(runs_dir),
        ]
    )
    history_path = runs_dir / "warrant_history.jsonl"
    assert history_path.is_file()

    lines = history_path.read_text().strip().splitlines()
    assert len(lines) == 3
    entries = [json.loads(line) for line in lines]
    assert all(e["kind"] == "added" for e in entries)
    assert all("timestamp" in e for e in entries)


def test_cli_gated_run_writes_no_history(obs_jsonl, mock_responses, tmp_path):
    """Gated cycles don't produce warrant revisions → no history file."""
    runs_dir = tmp_path / "runs"
    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--gate-confidence", "0.95",
            "--runs-dir", str(runs_dir),
        ]
    )
    history_path = runs_dir / "warrant_history.jsonl"
    assert not history_path.exists()


# ── --report mode ───────────────────────────────────────────────────────────


def test_cli_report_empty_runs_dir(tmp_path, capsys):
    """No runs dir → exit 0, friendly message."""
    code = main(
        ["dks", "--report", "--runs-dir", str(tmp_path / "missing")]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "no runs directory" in out


def test_cli_report_aggregates_across_runs(obs_jsonl, mock_responses, tmp_path, capsys):
    """Two runs land in the same --runs-dir; --report aggregates both.

    Trace filenames use ``%Y%m%dT%H%M%SZ`` second-granularity timestamps,
    so back-to-back runs in the same second would collide. Rename the
    first aggregate before the second run lands.
    """
    runs_dir = tmp_path / "runs"
    # First run — full loops
    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--runs-dir", str(runs_dir),
        ]
    )
    # Rename the first aggregate + cycle traces to a distinct timestamp.
    for p in list(runs_dir.glob("*_cycle_*.json")) + list(
        runs_dir.glob("*_aggregate.json")
    ):
        p.rename(p.with_name("19990101T000000Z_" + p.name.split("_", 1)[1]))

    # Second run — gated
    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--gate-confidence", "0.95",
            "--runs-dir", str(runs_dir),
        ]
    )

    # Rewrite the first aggregate's `cycle_traces` to point at the renamed
    # per-cycle files (so --report can resolve their `gated` fields).
    first_agg_path = next(runs_dir.glob("19990101T000000Z_aggregate.json"))
    first_agg = json.loads(first_agg_path.read_text())
    first_agg["cycle_traces"] = [
        str(runs_dir / f"19990101T000000Z_cycle_{i}.json") for i in (1, 2, 3)
    ]
    first_agg_path.write_text(json.dumps(first_agg))

    capsys.readouterr()  # clear
    code = main(
        ["dks", "--report", "--runs-dir", str(runs_dir), "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["run_count"] == 2
    assert payload["total_cycles"] == 6
    assert payload["closed_loop_count"] == 3
    assert payload["gated_count"] == 3
    assert payload["warrant_changes"]["added"] == 3


def test_cli_report_no_observations_required(tmp_path, capsys):
    """--report skips the observations-positional requirement."""
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    code = main(["dks", "--report", "--runs-dir", str(runs_dir)])
    assert code == 0


def test_cli_report_last_filters(obs_jsonl, mock_responses, tmp_path, capsys):
    """--report --report-last 1 restricts to the most recent aggregate."""
    runs_dir = tmp_path / "runs"
    # Run twice to produce 2 aggregate files. Add a tiny mtime separation
    # by touching the first aggregate to an earlier mtime.
    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--runs-dir", str(runs_dir),
        ]
    )
    import os
    import time

    first_aggregates = sorted(runs_dir.glob("*_aggregate.json"))
    # Backdate by 10 seconds so the second run is unambiguously newer.
    old_t = time.time() - 10
    for p in first_aggregates:
        os.utime(p, (old_t, old_t))

    main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--gate-confidence", "0.95",
            "--runs-dir", str(runs_dir),
        ]
    )

    capsys.readouterr()
    code = main(
        [
            "dks", "--report",
            "--runs-dir", str(runs_dir),
            "--report-last", "1",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["run_count"] == 1
    # The newest run is the gated one
    assert payload["gated_count"] == 3
    assert payload["closed_loop_count"] == 0


# ── Observations + --report mutual exclusivity ──────────────────────────────


def test_cli_no_observations_and_no_report_errors(tmp_path, capsys):
    code = main(["dks", "--no-trace"])
    assert code == 2
    err = capsys.readouterr().err
    assert "missing observations file" in err
