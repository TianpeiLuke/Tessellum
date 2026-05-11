"""Smoke tests for the `tessellum dks` CLI subcommand.

Phase 3 deliverable (v0.0.43). Loads a JSONL of observations, runs N
cycles via ``DKSRunner``, writes per-cycle + aggregate trace JSON to
``--runs-dir``. These tests exercise the argument parsing, JSONL loading,
trace writing, and exit codes against MockBackend.

Lifted from ``tessellum composer dks`` to top-level ``tessellum dks`` in
v0.0.43 — DKS is a peer runtime to Composer, not a Composer feature.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main


# ── Mock response builders (mirror tests/smoke/test_dks_multi_cycle.py) ─────


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


_FULL_CYCLE_RESPONSES = {
    "conservative": _arg_response("A-claim"),
    "exploratory": _arg_response("B-claim"),
    "counter-argument": json.dumps(
        {
            "broken_component": "warrant",
            "counter_claim": "fails here",
            "reason": "scope mismatch",
            "strength": "moderate",
        }
    ),
    "pattern discovery": json.dumps(
        {"description": "pattern", "observed": ["t1"]}
    ),
    "rule revision": json.dumps(
        {
            "claim": "Revised",
            "data": "D",
            "warrant": "Revised warrant",
            "supersedes": "",
        }
    ),
}


_SHORT_CIRCUIT_RESPONSES = {
    "conservative": _arg_response("same-claim"),
    "exploratory": _arg_response("same-claim"),
}


@pytest.fixture
def obs_jsonl(tmp_path) -> Path:
    """3-observation JSONL — every cycle gets a fresh trail root."""
    p = tmp_path / "obs.jsonl"
    lines = [
        json.dumps({"summary": "obs one", "mode": "fresh"}),
        json.dumps({"summary": "obs two", "mode": "fresh"}),
        json.dumps({"summary": "obs three", "mode": "fresh"}),
    ]
    p.write_text("\n".join(lines) + "\n")
    return p


@pytest.fixture
def mock_responses_full(tmp_path) -> Path:
    p = tmp_path / "responses.json"
    p.write_text(json.dumps(_FULL_CYCLE_RESPONSES))
    return p


@pytest.fixture
def mock_responses_short(tmp_path) -> Path:
    p = tmp_path / "responses.json"
    p.write_text(json.dumps(_SHORT_CIRCUIT_RESPONSES))
    return p


# ── Argument parsing + invocation errors ────────────────────────────────────


def test_cli_dks_missing_file_returns_2(tmp_path, capsys):
    """A non-existent observations path is an invocation error."""
    code = main(
        ["dks",str(tmp_path / "missing.jsonl")]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_cli_dks_invalid_jsonl_returns_2(tmp_path, capsys):
    bad = tmp_path / "bad.jsonl"
    bad.write_text("not json at all\n")
    code = main(["dks",str(bad)])
    assert code == 2
    err = capsys.readouterr().err
    assert "invalid JSON" in err


def test_cli_dks_jsonl_missing_summary_returns_2(tmp_path, capsys):
    p = tmp_path / "obs.jsonl"
    p.write_text(json.dumps({"timestamp": "2026-05-10"}) + "\n")
    code = main(["dks",str(p)])
    assert code == 2
    err = capsys.readouterr().err
    assert "summary" in err


def test_cli_dks_invalid_mode_returns_2(tmp_path, capsys):
    p = tmp_path / "obs.jsonl"
    p.write_text(json.dumps({"summary": "x", "mode": "weird"}) + "\n")
    code = main(["dks",str(p)])
    assert code == 2
    err = capsys.readouterr().err
    assert "invalid mode" in err


def test_cli_dks_extend_mode_requires_parent_fz(tmp_path, capsys):
    p = tmp_path / "obs.jsonl"
    p.write_text(json.dumps({"summary": "x", "mode": "extend"}) + "\n")
    code = main(["dks",str(p)])
    assert code == 2
    err = capsys.readouterr().err
    assert "FZ allocation" in err


# ── Empty observation file ──────────────────────────────────────────────────


def test_cli_dks_empty_jsonl_returns_0(tmp_path, capsys):
    p = tmp_path / "empty.jsonl"
    p.write_text("")
    code = main(["dks",str(p), "--no-trace"])
    assert code == 0
    out = capsys.readouterr().out
    assert "nothing to run" in out


def test_cli_dks_blank_lines_skipped(tmp_path, mock_responses_full, capsys):
    p = tmp_path / "obs.jsonl"
    p.write_text("\n\n" + json.dumps({"summary": "x"}) + "\n\n")
    code = main(
        [
            "dks",str(p),
            "--mock-responses", str(mock_responses_full),
            "--no-trace",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "1 cycle" in out


# ── End-to-end mock run ─────────────────────────────────────────────────────


def test_cli_dks_3_obs_writes_3_cycle_traces_plus_aggregate(
    obs_jsonl, mock_responses_full, tmp_path, capsys
):
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks",str(obs_jsonl),
            "--mock-responses", str(mock_responses_full),
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0

    cycle_files = sorted(runs_dir.glob("*_cycle_*.json"))
    aggregate_files = sorted(runs_dir.glob("*_aggregate.json"))

    assert len(cycle_files) == 3, f"expected 3 per-cycle traces, found {len(cycle_files)}"
    assert len(aggregate_files) == 1, f"expected 1 aggregate trace, found {len(aggregate_files)}"

    # Aggregate trace structure
    agg = json.loads(aggregate_files[0].read_text())
    assert agg["cycle_count"] == 3
    assert agg["closed_loop_count"] == 3
    assert agg["summary"]["added"] == 3
    assert len(agg["cycle_traces"]) == 3
    assert len(agg["final_warrants"]) == 3


def test_cli_dks_per_cycle_trace_has_expected_shape(
    obs_jsonl, mock_responses_full, tmp_path
):
    runs_dir = tmp_path / "runs"
    main(
        [
            "dks",str(obs_jsonl),
            "--mock-responses", str(mock_responses_full),
            "--runs-dir", str(runs_dir),
        ]
    )

    cycle_files = sorted(runs_dir.glob("*_cycle_*.json"))
    one = json.loads(cycle_files[0].read_text())
    for field in (
        "cycle_id", "mode", "closed_loop", "elapsed_ms",
        "folgezettel_nodes", "observation", "argument_a", "argument_b",
        "contradicts", "counter", "pattern", "rule_revision",
    ):
        assert field in one, f"per-cycle trace missing field {field!r}"

    # Closed loop → 6 FZ nodes
    assert one["closed_loop"] is True
    assert len(one["folgezettel_nodes"]) == 6


def test_cli_dks_no_trace_skips_runs_dir(
    obs_jsonl, mock_responses_full, tmp_path
):
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks",str(obs_jsonl),
            "--mock-responses", str(mock_responses_full),
            "--runs-dir", str(runs_dir),
            "--no-trace",
        ]
    )
    assert code == 0
    assert not runs_dir.exists()


def test_cli_dks_fresh_mode_allocates_sequential_roots(
    mock_responses_full, tmp_path
):
    """Three `fresh` observations → three trails (FZ 1, 2, 3)."""
    p = tmp_path / "obs.jsonl"
    p.write_text(
        "\n".join(
            json.dumps({"summary": f"obs-{i}", "mode": "fresh"}) for i in range(1, 4)
        )
        + "\n"
    )
    runs_dir = tmp_path / "runs"
    main(
        [
            "dks",str(p),
            "--mock-responses", str(mock_responses_full),
            "--runs-dir", str(runs_dir),
        ]
    )
    agg = json.loads(next(runs_dir.glob("*_aggregate.json")).read_text())
    cycle_ids = tuple(
        json.loads(Path(tp).read_text())["cycle_id"] for tp in agg["cycle_traces"]
    )
    assert cycle_ids == ("1", "2", "3")


def test_cli_dks_short_circuit_cycle_reports_zero_changes(
    tmp_path, mock_responses_short, capsys
):
    """When A and B agree the cycle short-circuits → 0 warrant changes."""
    p = tmp_path / "obs.jsonl"
    p.write_text(json.dumps({"summary": "x"}) + "\n")
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks",str(p),
            "--mock-responses", str(mock_responses_short),
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "0 closed loop" in out
    assert "0 added" in out

    agg = json.loads(next(runs_dir.glob("*_aggregate.json")).read_text())
    assert agg["closed_loop_count"] == 0
    assert agg["summary"]["added"] == 0


# ── --format json + --initial-warrants ──────────────────────────────────────


def test_cli_dks_json_output_payload_shape(
    obs_jsonl, mock_responses_full, capsys, tmp_path
):
    code = main(
        [
            "dks",str(obs_jsonl),
            "--mock-responses", str(mock_responses_full),
            "--runs-dir", str(tmp_path / "runs"),
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    for field in (
        "cycle_count", "closed_loop_count", "duration_seconds",
        "summary", "cycles", "warrant_changes", "trace_paths",
        "aggregate_path",
    ):
        assert field in payload
    assert payload["cycle_count"] == 3


def test_cli_dks_initial_warrants_file(
    obs_jsonl, mock_responses_full, tmp_path, capsys
):
    w_path = tmp_path / "warrants.json"
    w_path.write_text(
        json.dumps(
            [
                {
                    "claim": "seed-claim",
                    "data": "seed-data",
                    "warrant": "seed-warrant",
                }
            ]
        )
    )
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks",str(obs_jsonl),
            "--mock-responses", str(mock_responses_full),
            "--initial-warrants", str(w_path),
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0
    agg = json.loads(next(runs_dir.glob("*_aggregate.json")).read_text())
    # initial(1) + 3 revisions = 4 final
    assert len(agg["final_warrants"]) == 4
    assert agg["final_warrants"][0]["warrant"] == "seed-warrant"


def test_cli_dks_initial_warrants_missing_file_returns_2(
    obs_jsonl, mock_responses_full, tmp_path, capsys
):
    code = main(
        [
            "dks",str(obs_jsonl),
            "--mock-responses", str(mock_responses_full),
            "--initial-warrants", str(tmp_path / "missing.json"),
            "--no-trace",
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "initial-warrants" in err


def test_banner_lists_dks(capsys):
    """The DKS subcommand is a top-level peer of `composer`/`fz`; verify
    the banner advertises it."""
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum dks" in out
