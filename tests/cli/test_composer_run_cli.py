"""Smoke tests for ``tessellum composer run``."""

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
    pipeline_metadata: ./skill_demo.pipeline.yaml
    ---

    # Demo

    ## Step 1: produce <!-- :: section_id = step_1 :: -->

    PRODUCE.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    CONSUME {{upstream.produced}}.
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
        prompt_template: "PRODUCE."
        output_key: produced
      - section_id: step_2
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: [step_1]
        materializer: no_op
        prompt_template: "CONSUME."
    """
)


@pytest.fixture
def demo_skill(tmp_path: Path) -> Path:
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_demo.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return skill


def test_run_human_output(demo_skill, tmp_path, capsys):
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "ran skill_demo" in out
    assert "step_1" in out
    assert "step_2" in out


def test_run_json_output(demo_skill, tmp_path, capsys):
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["skill_name"] == "skill_demo"
    assert payload["step_invocation_count"] == 2
    assert payload["error_count"] == 0
    assert payload["trace_path"] is None


def test_run_with_mock_responses(demo_skill, tmp_path, capsys):
    responses = tmp_path / "mock.json"
    responses.write_text(
        json.dumps({"PRODUCE": '{"produced": [1, 2, 3]}'}),
        encoding="utf-8",
    )
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--mock-responses",
            str(responses),
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 0


def test_run_with_leaves(demo_skill, tmp_path, capsys):
    """Leaves file lets per_leaf steps run multiple times — even with corpus
    pipeline, the file must parse and load."""
    leaves = tmp_path / "leaves.json"
    leaves.write_text(json.dumps([{"id": "a"}, {"id": "b"}]), encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--leaves",
            str(leaves),
            "--format",
            "json",
        ]
    )
    assert code == 0


def test_run_writes_trace(demo_skill, tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--runs-dir",
            str(runs_dir),
        ]
    )
    assert code == 0
    traces = list(runs_dir.glob("*.json"))
    assert len(traces) == 1
    payload = json.loads(traces[0].read_text(encoding="utf-8"))
    assert payload["skill_name"] == "skill_demo"


def test_run_dry_run_no_files_written(demo_skill, tmp_path, capsys):
    vault = tmp_path / "vault"
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(vault),
            "--no-trace",
            "--dry-run",
        ]
    )
    assert code == 0
    # no_op materializer wouldn't write anyway, but the vault dir should not
    # have been populated by side effects.
    assert not vault.exists() or not any(vault.iterdir())


def test_run_missing_skill_returns_2(tmp_path, capsys):
    code = main(["composer", "run", str(tmp_path / "nope.md"), "--no-trace"])
    assert code == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_run_non_md_returns_2(tmp_path, capsys):
    p = tmp_path / "not_a_skill.txt"
    p.write_text("not a skill")
    code = main(["composer", "run", str(p), "--no-trace"])
    assert code == 2
    err = capsys.readouterr().err
    assert "not a markdown" in err


def test_run_invalid_leaves_json_returns_2(demo_skill, tmp_path, capsys):
    leaves = tmp_path / "bad-leaves.json"
    leaves.write_text("not valid json", encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--leaves",
            str(leaves),
        ]
    )
    assert code == 2


def test_run_pipeline_none_returns_0(tmp_path, capsys):
    canonical = _CANONICAL.replace(
        "pipeline_metadata: ./skill_demo.pipeline.yaml",
        "pipeline_metadata: none",
    )
    skill = tmp_path / "skill_demo.md"
    skill.write_text(canonical, encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "nothing to run" in out
