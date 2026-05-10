"""Smoke tests for ``tessellum composer compile``."""

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

    ## Step 1 <!-- :: section_id = step_1 :: -->

    Body 1.

    ## Step 2 <!-- :: section_id = step_2 :: -->

    Body 2.
    """
)


_VALID_SIDECAR = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "Step 1."
      - section_id: step_2
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: [step_1]
        materializer: no_op
        prompt_template: "Step 2."
    """
)


@pytest.fixture
def demo_skill(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    sidecar.write_text(_VALID_SIDECAR, encoding="utf-8")
    return skill


def test_compile_human_output(demo_skill, capsys):
    code = main(["composer", "compile", str(demo_skill)])
    assert code == 0
    out = capsys.readouterr().out
    assert "compiled skill_demo" in out
    assert "step_1" in out
    assert "step_2" in out
    assert "← step_1" in out  # depends_on rendered


def test_compile_json_output(demo_skill, capsys):
    code = main(["composer", "compile", str(demo_skill), "--format", "json"])
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["skill_name"] == "skill_demo"
    assert payload["step_count"] == 2
    assert len(payload["steps"]) == 2


def test_compile_to_file(demo_skill, tmp_path, capsys):
    output = tmp_path / "dag.json"
    code = main(
        ["composer", "compile", str(demo_skill), "-o", str(output)]
    )
    assert code == 0
    assert output.is_file()
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["step_count"] == 2


def test_compile_no_prompts_flag(demo_skill, capsys):
    code = main(
        [
            "composer",
            "compile",
            str(demo_skill),
            "--format",
            "json",
            "--no-prompts",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    for step in payload["steps"]:
        assert "prompt_section_text" not in step
        assert "prompt_section_text_chars" in step


def test_compile_missing_skill_returns_2(tmp_path, capsys):
    code = main(["composer", "compile", str(tmp_path / "nope.md")])
    assert code == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_compile_non_md_returns_2(tmp_path, capsys):
    p = tmp_path / "not_a_skill.txt"
    p.write_text("not a skill")
    code = main(["composer", "compile", str(p)])
    assert code == 2
    err = capsys.readouterr().err
    assert "not a markdown" in err


def test_compile_validation_failure_returns_1(tmp_path, capsys):
    """A skill with a malformed sidecar fails to compile."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    sidecar.write_text("pipeline: not-a-list-but-a-string", encoding="utf-8")
    code = main(["composer", "compile", str(skill)])
    assert code == 1
    err = capsys.readouterr().err
    assert "FAILED" in capsys.readouterr().out or "validation" in err or err


def test_compile_pipeline_none_returns_0_with_empty_pipeline(tmp_path, capsys):
    canonical = _CANONICAL.replace(
        "pipeline_metadata: ./skill_demo.pipeline.yaml",
        "pipeline_metadata: none",
    )
    skill = tmp_path / "skill_demo.md"
    skill.write_text(canonical, encoding="utf-8")
    code = main(["composer", "compile", str(skill)])
    assert code == 0
    out = capsys.readouterr().out
    assert "no DAG" in out


def test_compile_real_search_notes_skill(capsys):
    """The shipped search-notes skill compiles cleanly through the CLI."""
    repo = Path(__file__).resolve().parents[2]
    skill = repo / "vault" / "resources" / "skills" / "skill_tessellum_search_notes.md"
    if not skill.is_file():
        pytest.skip(f"real skill not found at {skill}")
    code = main(["composer", "compile", str(skill), "--format", "json"])
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["skill_name"] == "skill_tessellum_search_notes"
    assert payload["step_count"] == 3
