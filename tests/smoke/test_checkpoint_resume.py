"""Phase 4 (FZ 20k9c1a1a1b7c2k2a3a): checkpoint-resume at claim.

The claim path consumes the A1.2 checkpoints instead of re-paying the
linear phases. Pins the contract: the latest checkpoint wins (corrupt
files skipped); a resume with a matching code ledger skips the plan phase
— a ready review fold skips the whole linear ladder; a SOURCE MISMATCH
refuses the resume and starts fresh (the ledger is the identity)."""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import MockBackend, run_digestion_pipeline
from tessellum.composer.contracts import mandatory_section_stems
from tessellum.composer.digestion import load_latest_checkpoint

from test_composer_episodic_hardening import _synthetic_pipeline

_STEM_BLOB = "\n" + "\n".join(f"## {s}" for s in mandatory_section_stems())


def _blob(text: str) -> dict:
    return {
        "plan_path": "plans/p.md",
        "plan_text": "# Plan\n\nbody" + _STEM_BLOB,
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# N\n\nbody",
        "total_notes": 1,
        "section_coverage_map": [
            {"source_section": "Only Heading", "maps_to_note": "notes/n.md"}
        ],
    }


def _leaf(text: str) -> dict:
    return {
        "id": "demo", "total_notes": 1, "member_count": 1,
        "members": [{"source_id": "p1", "excerpt": text}],
    }


def _run(tmp_path: Path, text: str, *, resume: bool) -> object:
    sd = tmp_path / "skills"
    sd.mkdir(exist_ok=True)
    _synthetic_pipeline(sd)
    return run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=_leaf(text),
        backend=MockBackend(default=json.dumps(_blob(text))),
        vault_root=tmp_path / "vault",
        runs_dir=tmp_path / "runs",
        resume_from_checkpoint=resume,
    )


def test_load_latest_checkpoint_picks_highest_and_skips_corrupt(tmp_path: Path) -> None:
    cp = tmp_path / "checkpoints"
    cp.mkdir()
    (cp / "01_plan.json").write_text('{"a": 1}')
    (cp / "02_augment.json").write_text('{"a": 2}')
    (cp / "03_review.json").write_text("{corrupt")
    seq, phase, doc = load_latest_checkpoint(tmp_path)
    assert (seq, phase, doc) == (2, "augment", {"a": 2})
    assert load_latest_checkpoint(tmp_path / "missing") is None


def test_resume_skips_paid_phases(tmp_path: Path) -> None:
    text = "# Only Heading\n\n" + "word " * 50
    first = _run(tmp_path, text, resume=False)
    assert first.completed
    assert (tmp_path / "runs" / "checkpoints").exists()
    resumed = _run(tmp_path, text, resume=True)
    assert resumed.completed
    ran = [p.phase for p in resumed.phases]
    # the latest checkpoint is a READY review fold → the whole linear ladder
    # is skipped; only the execute wave runs.
    assert "plan" not in ran and "review" not in ran
    marker = resumed.plan_doc["_resumed_from_checkpoint"]
    assert marker["phase"] == "review"


def test_resume_refused_on_source_mismatch(tmp_path: Path) -> None:
    first = _run(tmp_path, "# Only Heading\n\n" + "word " * 50, resume=False)
    assert first.completed
    other = "# Only Heading\n\n" + "tok " * 80  # different measured ledger
    fresh = _run(tmp_path, other, resume=True)
    assert fresh.completed
    ran = [p.phase for p in fresh.phases]
    assert "plan" in ran  # resume refused → full linear ladder re-ran
    assert "_resumed_from_checkpoint" not in fresh.plan_doc


def test_no_resume_flag_is_byte_identical(tmp_path: Path) -> None:
    text = "# Only Heading\n\n" + "word " * 50
    first = _run(tmp_path, text, resume=False)
    again = _run(tmp_path, text, resume=False)
    assert first.completed and again.completed
    assert [p.phase for p in again.phases] == [p.phase for p in first.phases]
