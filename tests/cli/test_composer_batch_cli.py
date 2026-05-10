"""Smoke tests for ``tessellum composer batch``."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main


_CANONICAL = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    pipeline_metadata: ./{name}.pipeline.yaml
    ---

    # {name}

    ## Step 1 <!-- :: section_id = step_1 :: -->

    Body.
    """
)


_SIDECAR = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "Hi."
        output_key: out
    """
)


def _make_skill(tmp_path: Path, name: str) -> Path:
    skill = tmp_path / f"{name}.md"
    skill.write_text(_CANONICAL.format(name=name), encoding="utf-8")
    (tmp_path / f"{name}.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return skill


def _make_jobs_file(
    tmp_path: Path, names: list[str], runs_dir: Path
) -> Path:
    spec = []
    for name in names:
        skill_path = _make_skill(tmp_path, name)
        spec.append(
            {
                "job_id": name,
                "skill": str(skill_path),
                "leaves": [],
                "vault": str(tmp_path / "vault"),
                "runs_dir": str(runs_dir),
            }
        )
    jobs_file = tmp_path / "jobs.json"
    jobs_file.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return jobs_file


def test_batch_human_output(tmp_path, capsys):
    jobs_file = _make_jobs_file(tmp_path, ["skill_a", "skill_b"], tmp_path / "runs")
    code = main(["composer", "batch", str(jobs_file), "--parallelism", "1"])
    assert code == 0
    out = capsys.readouterr().out
    assert "2 completed" in out
    assert "skill_a" in out
    assert "skill_b" in out


def test_batch_json_output(tmp_path, capsys):
    jobs_file = _make_jobs_file(tmp_path, ["skill_a"], tmp_path / "runs")
    code = main(
        [
            "composer",
            "batch",
            str(jobs_file),
            "--format",
            "json",
            "--parallelism",
            "1",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["completed"] == ["skill_a"]
    assert payload["failed"] == []
    assert len(payload["jobs"]) == 1


def test_batch_resume(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    jobs_file = _make_jobs_file(tmp_path, ["skill_a"], runs_dir)
    # First run.
    main(["composer", "batch", str(jobs_file), "--parallelism", "1"])
    capsys.readouterr()
    # Second run — should skip.
    code = main(
        [
            "composer",
            "batch",
            str(jobs_file),
            "--parallelism",
            "1",
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["skipped"] == ["skill_a"]


def test_batch_no_resume_reruns(tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    jobs_file = _make_jobs_file(tmp_path, ["skill_a"], runs_dir)
    main(["composer", "batch", str(jobs_file), "--parallelism", "1"])
    capsys.readouterr()
    code = main(
        [
            "composer",
            "batch",
            str(jobs_file),
            "--no-resume",
            "--parallelism",
            "1",
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["completed"] == ["skill_a"]


def test_batch_missing_jobs_file_returns_2(tmp_path, capsys):
    code = main(["composer", "batch", str(tmp_path / "nope.json")])
    assert code == 2


def test_batch_invalid_json_returns_2(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    code = main(["composer", "batch", str(bad)])
    assert code == 2


def test_batch_jobs_must_be_list_returns_2(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
    code = main(["composer", "batch", str(bad)])
    assert code == 2


def test_batch_missing_job_id_returns_2(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps([{"skill": "x.md"}]), encoding="utf-8")
    code = main(["composer", "batch", str(bad)])
    assert code == 2


def test_batch_with_compile_failure_returns_1(tmp_path, capsys):
    """A job pointing at a missing skill is marked failed → exit 1."""
    spec = [
        {
            "job_id": "bad",
            "skill": str(tmp_path / "missing.md"),
            "leaves": [],
            "vault": str(tmp_path / "vault"),
            "runs_dir": str(tmp_path / "runs"),
        }
    ]
    jobs_file = tmp_path / "jobs.json"
    jobs_file.write_text(json.dumps(spec), encoding="utf-8")
    code = main(["composer", "batch", str(jobs_file), "--parallelism", "1"])
    assert code == 1
    out = capsys.readouterr().out
    assert "FAILED" in out


def test_batch_empty_jobs_returns_0(tmp_path, capsys):
    jobs_file = tmp_path / "empty.json"
    jobs_file.write_text("[]", encoding="utf-8")
    code = main(["composer", "batch", str(jobs_file)])
    assert code == 0
    out = capsys.readouterr().out
    assert "no jobs" in out
