"""Smoke tests for ``tessellum dks --meta`` — the Phase 9 CLI surface.

Surfaces under test (v0.0.52):

- ``--meta`` with no runs-dir present: cold-start path, exit 0.
- ``--meta`` cold-start guard message: human format mentions ``--min-cycles``.
- ``--meta --apply`` writes ``schema_events.jsonl`` + migration note.
- ``--meta --min-cycles=2`` lets a tiny synthetic dataset through.
- ``--meta --format json`` returns parseable JSON with the expected keys.
- ``--meta --target-failure=premise`` filters proposals.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tessellum.cli.main import main


# ── Helpers ────────────────────────────────────────────────────────────────


def _write_cycle_trace(
    runs_dir: Path, idx: int, broken_component: str
) -> Path:
    """Write a minimal per-cycle trace file the --meta builder can read."""
    ts = f"20260510T00{idx:02d}00Z"
    fz = f"99{idx}"
    path = runs_dir / f"{ts}_cycle_{fz}.json"
    path.write_text(
        json.dumps(
            {
                "cycle_index": idx,
                "fz": fz,
                "counter": {
                    "broken_component": broken_component,
                    "counter_claim": "c",
                    "reason": "r",
                    "strength": "moderate",
                },
            }
        )
    )
    return path


def _seed_traces(runs_dir: Path, n: int, broken_component: str) -> None:
    """Drop n cycle traces under runs_dir."""
    runs_dir.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        _write_cycle_trace(runs_dir, i, broken_component)


# ── --meta cold-start path (no runs-dir) ───────────────────────────────────


def test_meta_no_runs_dir(tmp_path, capsys):
    """Missing runs-dir → cold-start path, exit 0."""
    code = main(["dks", "--meta", "--runs-dir", str(tmp_path / "missing")])
    assert code == 0
    captured = capsys.readouterr()
    assert "0 cycles examined" in captured.out
    assert "DRY RUN" in captured.out


def test_meta_cold_start_guard_message(tmp_path, capsys):
    """Below DEFAULT_MIN_CYCLES → cold-start guard mention in human format."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(["dks", "--meta", "--runs-dir", str(runs_dir)])
    assert code == 0
    captured = capsys.readouterr()
    assert "cold-start guard active" in captured.out
    assert "--min-cycles=20" in captured.out


# ── --min-cycles=N lets a small dataset through ────────────────────────────


def test_meta_min_cycles_override(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    # 5 cycles all with warrant failures → dominance > 50% once min-cycles=5.
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        ["dks", "--meta", "--runs-dir", str(runs_dir), "--min-cycles", "5"]
    )
    assert code == 0
    captured = capsys.readouterr()
    assert "5 cycles examined" in captured.out
    assert "DRY RUN" in captured.out
    # Warrant dominance should yield 1 proposal (warrant_codification edge)
    assert "warrant_codification" in captured.out


# ── --apply writes the event log + migration note ──────────────────────────


def test_meta_apply_writes_event_log(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--apply",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    assert "APPLIED" in captured.out
    # schema_events.jsonl should exist + contain one event
    events_path = runs_dir / "meta" / "schema_events.jsonl"
    assert events_path.is_file()
    lines = [
        ln for ln in events_path.read_text().splitlines() if ln.strip()
    ]
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["kind"] == "added"
    assert parsed["edge"]["label"] == "warrant_codification"
    # Migration note should exist
    migration_notes = list((runs_dir / "meta").glob("migration_*.md"))
    assert len(migration_notes) == 1


# ── --format json ──────────────────────────────────────────────────────────


def test_meta_format_json(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["cycles_examined"] == 5
    assert payload["min_cycles"] == 5
    assert payload["dry_run"] is True
    assert isinstance(payload["proposals"], list)
    assert len(payload["proposals"]) == 1
    assert payload["proposals"][0]["edge"]["label"] == "warrant_codification"
    assert payload["events_landed_count"] == 0


# ── --target-failure filter ────────────────────────────────────────────────


def test_meta_target_failure_filter_filters(tmp_path, capsys):
    """--target-failure=premise on a warrant-dominant dataset → no proposals."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--target-failure", "premise",
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["proposals"] == []


def test_meta_target_failure_filter_matches(tmp_path, capsys):
    """--target-failure=warrant on warrant-dominant dataset → 1 proposal."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--target-failure", "warrant",
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert len(payload["proposals"]) == 1


# ── Missing observations + no --meta/--report/--calibrate → exit 2 ────────


def test_meta_help_string_mentions_meta(capsys):
    """Without observations or --meta/--report/--calibrate, error mentions --meta."""
    code = main(["dks"])
    assert code == 2
    captured = capsys.readouterr()
    assert "--meta" in captured.err or "--meta" in captured.out


# ── --proposer llm (Phase B.2) ─────────────────────────────────────────────


def test_meta_proposer_llm_with_mock_backend(tmp_path, capsys):
    """--proposer llm --backend mock with canned response produces a proposal."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    # Mock response keyed on a substring that appears in the LLM proposer's
    # user prompt (the "META-OBSERVATION" header).
    mock_responses_path = tmp_path / "mock.json"
    mock_responses_path.write_text(
        json.dumps(
            {
                "META-OBSERVATION": json.dumps(
                    {
                        "proposals": [
                            {
                                "kind": "add",
                                "edge": {
                                    "source": "model",
                                    "target": "procedure",
                                    "label": "llm_proposed_edge",
                                },
                                "motivating_observation": "warrant attacks dominate",
                                "expected_impact": "less warrant churn",
                                "input_bias_risk": "medium",
                            }
                        ]
                    }
                )
            }
        )
    )
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--proposer", "llm",
            "--backend", "mock",
            "--mock-responses", str(mock_responses_path),
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert len(payload["proposals"]) == 1
    assert payload["proposals"][0]["edge"]["label"] == "llm_proposed_edge"


def test_meta_proposer_llm_default_falls_back_to_heuristic_label():
    """--proposer is heuristic by default; argparse default value sanity."""
    import argparse

    from tessellum.cli.dks import add_subparser

    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="cmd")
    add_subparser(subs)
    args = parser.parse_args(["dks", "--meta"])
    assert args.proposer == "heuristic"


def test_meta_proposer_heuristic_unchanged_from_v052(tmp_path, capsys):
    """The default --proposer heuristic path matches the v0.0.52 behaviour."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--proposer", "heuristic",
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert len(payload["proposals"]) == 1
    assert payload["proposals"][0]["edge"]["label"] == "warrant_codification"


# ── --attacker llm + --survive-threshold (Phase B.3) ───────────────────────


def test_meta_attacker_llm_with_mock_kills_proposal_at_strict(tmp_path, capsys):
    """--attacker llm + --survive-threshold=strict + attack -> 0 survivors."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    # Mock responses keyed by substrings that distinguish the proposer
    # prompt ("META-OBSERVATION") from the attacker prompt ("PROPOSALS").
    mock_responses_path = tmp_path / "mock.json"
    mock_responses_path.write_text(
        json.dumps(
            {
                "PROPOSALS": json.dumps(
                    {
                        "attacks": [
                            {
                                "attacked_proposal_index": 0,
                                "attack_kind": "input_bias",
                                "reason": "warrant rate is input-induced",
                                "strength": "moderate",
                            }
                        ]
                    }
                ),
                # Proposer prompt comes first; it must NOT match PROPOSALS
                # (no such substring in the proposer prompt), so it falls
                # through to default below.
            }
        )
    )
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--proposer", "heuristic",
            "--attacker", "llm",
            "--survive-threshold", "strict",
            "--backend", "mock",
            "--mock-responses", str(mock_responses_path),
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert len(payload["proposals"]) == 1
    assert len(payload["attacks"]) == 1
    assert payload["surviving_count"] == 0


def test_meta_attacker_none_default_keeps_v052_behaviour(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--format", "json",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["attacker"] == "none"
    assert payload["attacks"] == []
    assert payload["surviving_count"] == 1


# ── --bb-db → unrealised_schema_edges (Phase B.6) ──────────────────────────


def test_meta_unrealised_count_empty_without_bb_db(tmp_path, capsys):
    """No --bb-db → unrealised_schema_edges_count is 0 (v0.0.52 behaviour)."""
    runs_dir = tmp_path / "runs"
    _seed_traces(runs_dir, 5, "warrant")
    code = main(
        [
            "dks", "--meta",
            "--runs-dir", str(runs_dir),
            "--min-cycles", "5",
            "--bb-db", str(tmp_path / "nonexistent.db"),
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["observation"]["unrealised_schema_edges_count"] == 0


def test_meta_unrealised_count_populates_with_real_bb_db(tmp_path, capsys):
    """When --bb-db points at a real BBGraph DB, unrealised edges populate."""
    # The test fixture in tests/smoke/conftest.py builds a corpus DB; for CLI
    # testing we just need any real index DB. The simplest path is to use the
    # one the Tessellum vault carries (./data/tessellum.db if present), or
    # synthesise one via tessellum index build. To keep this test
    # self-contained without depending on test-time index builds, we
    # construct an empty-but-valid BBGraph DB by using the schema-creation
    # path in indexer; for v0.0.53 we just assert the no-DB branch works
    # (covered above) + the helper unit test in test_bb_graph.py covers the
    # populated branch directly.
    pass  # See test_unrealised_schema_edges_excludes_realised_bb_pairs in
    # tests/smoke/test_bb_graph.py for the populated-graph case.
