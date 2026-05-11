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
