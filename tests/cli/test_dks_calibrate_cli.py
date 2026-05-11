"""Smoke tests for `tessellum dks --calibrate` + Phase 7 CLI wiring.

Three surfaces:
- `--calibrate` mode reads past traces, reports false-gate rate, suggests threshold.
- `--confidence-model {constant,calibrated}` switches the model.
- `--retrieval-db <path>` builds a RetrievalClient.
- `--semantic-disagreement` flag is forwarded into DKSCycle.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main


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
    "pattern discovery": json.dumps(
        {"description": "p", "observed": ["t"]}
    ),
    "rule revision": json.dumps(
        {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
    ),
}


@pytest.fixture
def obs_jsonl(tmp_path) -> Path:
    p = tmp_path / "obs.jsonl"
    p.write_text(json.dumps({"summary": "obs one"}) + "\n")
    return p


@pytest.fixture
def mock_responses(tmp_path) -> Path:
    p = tmp_path / "responses.json"
    p.write_text(json.dumps(_FULL_LOOP_RESPONSES))
    return p


# ── --calibrate mode ───────────────────────────────────────────────────────


def test_cli_calibrate_empty_runs_dir(tmp_path, capsys):
    """No traces → friendly message, exit 0."""
    code = main(
        [
            "dks", "--calibrate",
            "--runs-dir", str(tmp_path / "missing"),
            "--no-trace",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "0 cycles examined" in out


def test_cli_calibrate_reports_false_gate_rate(tmp_path, capsys):
    """Seed runs_dir with synthetic cycle traces; --calibrate replays them."""
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    # One cycle that would gate (conf=0.9 > 0.5) AND closed_loop=True (false gate).
    (runs_dir / "20260101T000000Z_cycle_1.json").write_text(
        json.dumps({"confidence_score": 0.9, "closed_loop": True, "cycle_id": "1"})
    )
    # One cycle that wouldn't gate (conf=0.3 < 0.5).
    (runs_dir / "20260101T000000Z_cycle_2.json").write_text(
        json.dumps({"confidence_score": 0.3, "closed_loop": False, "cycle_id": "2"})
    )

    code = main(
        [
            "dks", "--calibrate",
            "--runs-dir", str(runs_dir),
            "--gate-threshold", "0.5",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["cycles_examined"] == 2
    assert payload["would_gate_count"] == 1
    assert payload["false_gate_count"] == 1
    assert payload["false_gate_rate"] == 1.0


def test_cli_calibrate_custom_target_rate(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    (runs_dir / "20260101T000000Z_cycle_1.json").write_text(
        json.dumps({"confidence_score": 0.95, "closed_loop": False, "cycle_id": "1"})
    )

    code = main(
        [
            "dks", "--calibrate",
            "--runs-dir", str(runs_dir),
            "--target-false-gate-rate", "0.05",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["target_false_gate_rate"] == 0.05


# ── --confidence-model {calibrated} integration ───────────────────────────


def test_cli_confidence_model_calibrated_uses_calibrated_confidence(
    obs_jsonl, mock_responses, tmp_path
):
    """--confidence-model=calibrated wires CalibratedConfidence reading
    warrant_history.jsonl. Empty history → baseline 0.5 → not gated at
    default threshold 0.85."""
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--confidence-model", "calibrated",
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0
    # Check the cycle trace recorded a confidence score
    cycle_trace = next(runs_dir.glob("*_cycle_*.json"))
    payload = json.loads(cycle_trace.read_text())
    # Phase 5's confidence_score is set when a model is wired
    assert payload["confidence_score"] == 0.5


# ── --retrieval-db ────────────────────────────────────────────────────────


def test_cli_retrieval_db_missing_returns_2(obs_jsonl, mock_responses, tmp_path, capsys):
    code = main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--retrieval-db", str(tmp_path / "missing.db"),
            "--no-trace",
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "retrieval-db" in err


def test_cli_retrieval_db_present_runs_clean(
    obs_jsonl, mock_responses, tmp_path
):
    """A real --retrieval-db points the runner at a valid index."""
    from tessellum.indexer import build as build_index

    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_one.md").write_text(
        textwrap.dedent("""\
        ---
        tags: [resource, terminology]
        keywords: [a, b, c]
        topics: [Tx, Ty]
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: concept
        ---

        # One

        Body.
        """)
    )
    retrieval_db = tmp_path / "tess.db"
    build_index(v, retrieval_db, with_dense=False)

    code = main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--retrieval-db", str(retrieval_db),
            "--no-trace",
        ]
    )
    assert code == 0


# ── --semantic-disagreement flag forwarding ───────────────────────────────


def test_cli_semantic_disagreement_flag_runs_clean(
    obs_jsonl, mock_responses, tmp_path
):
    """The flag is wired into DKSRunner; the run completes."""
    code = main(
        [
            "dks", str(obs_jsonl),
            "--mock-responses", str(mock_responses),
            "--semantic-disagreement",
            "--no-trace",
        ]
    )
    # With --semantic-disagreement, the runner does an extra LLM call.
    # mock_responses doesn't have a "semantic disagreement check" handler;
    # the cycle falls back to string-compare. Run completes.
    assert code == 0


# ── --calibrate skips observations positional ────────────────────────────


def test_cli_calibrate_without_observations(tmp_path):
    """--calibrate doesn't require the observations positional."""
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    code = main(
        [
            "dks", "--calibrate",
            "--runs-dir", str(runs_dir),
        ]
    )
    assert code == 0
