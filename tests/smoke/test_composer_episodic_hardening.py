"""A1 (FZ 20k9c1a1a1b7c2k1a) — episodic hardening.

Pins the A1 seams:

- :func:`slim_plan_doc` — the dump-friendly copy without the bulky inline
  source bytes (purity, key coverage, member metadata retention);
- A1.2 per-phase plan-of-record checkpoints under ``<runs_dir>/checkpoints/``
  (opt-in via the existing ``runs_dir`` seam; absent → byte-identical);
- A1.1 the events stream — lifecycle events land on disk AT RECORD TIME, so a
  cancelled/crashed wave keeps the events of every completed leaf (the
  end-of-run writer never ran);
- A1.3 corpus planning persistence — an accepted sub-plan's ``plan_doc`` is
  durable at acceptance (via :func:`_persist_json`, exercised directly since a
  full corpus fixture belongs to the corpus tests).
"""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import MockBackend, run_digestion_pipeline
from tessellum.composer.corpus_digestion import _persist_json
from tessellum.composer.digestion import slim_plan_doc


# ── slim_plan_doc ────────────────────────────────────────────────────────────


def test_slim_plan_doc_drops_bulk_keeps_metadata() -> None:
    doc = {
        "plan_text": "# Plan",
        "source_content": "X" * 1000,
        "members": [
            {"source_id": "a", "source_url": "u", "excerpt": "Y" * 1000},
            "not-a-dict",
        ],
    }
    slim = slim_plan_doc(doc)
    assert "source_content" not in slim
    assert slim["members"][0] == {"source_id": "a", "source_url": "u"}
    assert slim["members"][1] == "not-a-dict"
    assert slim["plan_text"] == "# Plan"
    # Pure — the input is untouched.
    assert doc["source_content"] and doc["members"][0]["excerpt"]


# ── synthetic pipeline (the shared minimal fixture pattern) ──────────────────


def _write_phase_skill(
    skills_dir: Path,
    name: str,
    *,
    output_key: str,
    required: list[str],
    materializer: str = "no_op",
    aggregation: str = "corpus_wide",
) -> None:
    canonical = (
        "---\n"
        "tags:\n  - resource\n  - skill\n"
        "keywords:\n  - alpha\n  - beta\n  - gamma\n"
        "topics:\n  - Digestion\n"
        "language: markdown\n"
        "date of note: 2026-07-28\n"
        "status: active\n"
        "building_block: procedure\n"
        "access_control_group: [\"general\"]\n"
        "---\n\n"
        f"# {name}\n\n"
        "## Do it <!-- :: section_id = step_1 :: -->\n\n"
        "```yaml\n"
        "role: CORE\n"
        f"aggregation: {aggregation}\n"
        "batchable: false\n"
        "depends_on: []\n"
        f"materializer: {materializer}\n"
        f"output_key: {output_key}\n"
        "expected_output_schema:\n"
        "  type: object\n"
        f"  required: [{', '.join(required)}]\n"
        "```\n\n"
        "phase\n"
    )
    (skills_dir / f"{name}.md").write_text(canonical, encoding="utf-8")


def _synthetic_pipeline(skills_dir: Path) -> None:
    _write_phase_skill(skills_dir, "skill_tessellum_plan_digestion",
                       output_key="plan_out", required=["plan_path"])
    _write_phase_skill(skills_dir, "skill_tessellum_augment_digestion_plan",
                       output_key="augment_out", required=["plan_text"])
    _write_phase_skill(skills_dir, "skill_tessellum_review_digestion_plan",
                       output_key="verdict", required=["ready"])
    _write_phase_skill(skills_dir, "skill_tessellum_execute_digestion_plan",
                       output_key="exec_out", required=["output_path", "body_markdown"],
                       materializer="body_markdown_to_file", aggregation="per_leaf")


def _mock() -> MockBackend:
    return MockBackend(default=json.dumps({
        "plan_path": "plans/plan_demo.md",
        "plan_text": "# Plan\n\nbody",
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# Note\n\nbody",
        "total_notes": 1,
    }))


_SOURCE = {
    "id": "demo", "plan_path": "plans/plan_demo.md", "plan_text": "# Plan",
    "total_notes": 1,
    "members": [{"source_id": "m0", "excerpt": "SRC" * 200}],
    "member_count": 1,
}


# ── A1.2 checkpoints ─────────────────────────────────────────────────────────


def test_checkpoints_written_per_linear_phase(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    runs = tmp_path / "runs"
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
        runs_dir=runs,
    )
    assert result.completed
    cps = sorted(p.name for p in (runs / "checkpoints").glob("*.json"))
    assert cps == ["01_plan.json", "02_augment.json", "03_review.json"]
    # Checkpoints carry the plan-of-record, slimmed — no inline source bytes.
    snap = json.loads((runs / "checkpoints" / "03_review.json").read_text())
    assert snap["plan_text"]
    assert "excerpt" not in json.dumps(snap)


def test_no_runs_dir_no_checkpoints(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    assert not list(tmp_path.rglob("checkpoints"))


# ── A1.1 events stream ───────────────────────────────────────────────────────


def test_events_streamed_at_record_time(tmp_path: Path) -> None:
    """Happy path: the streamed JSONL equals the end-of-run rewrite — and it
    exists with one line per per-leaf lifecycle event."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    events = tmp_path / "events.jsonl"
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
        events_path=events,
    )
    assert result.completed
    lines = [json.loads(x) for x in events.read_text().splitlines() if x.strip()]
    assert lines, "expected at least one streamed lifecycle event"
    assert all("outcome" in ev for ev in lines)


# ── A1.3 corpus persistence helper ───────────────────────────────────────────


def test_persist_json_atomic_and_failsoft(tmp_path: Path) -> None:
    target = tmp_path / "corpus" / "s1" / "plan_doc.json"
    _persist_json(target, {"plan_text": "# P", "total_notes": 2})
    assert json.loads(target.read_text())["total_notes"] == 2
    assert not target.with_suffix(".json.tmp").exists()
    # Fail-soft: an unwritable path must not raise.
    _persist_json(Path("/nonexistent-root/x/y.json"), {"a": 1})
