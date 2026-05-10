"""Smoke tests for the ``tessellum composer validate`` CLI subcommand."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main

_SKILL_CANONICAL = textwrap.dedent(
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

    Body for step 1.
    """
)

_SKILL_NO_PIPELINE = _SKILL_CANONICAL.replace(
    "pipeline_metadata: ./skill_demo.pipeline.yaml",
    "pipeline_metadata: none",
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
        prompt_template: "Do something."
    """
)


@pytest.fixture
def skill_dir(tmp_path):
    """A directory with one valid skill (canonical + sidecar pair)."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    sidecar.write_text(_VALID_SIDECAR, encoding="utf-8")
    return tmp_path


@pytest.fixture
def skill_pair(skill_dir):
    return skill_dir / "skill_demo.md"


def test_validate_clean_skill_returns_0(skill_pair, capsys):
    code = main(["composer", "validate", str(skill_pair)])
    assert code == 0
    out = capsys.readouterr().out
    assert "OK" in out
    assert "1 step" in out


def test_validate_skill_with_pipeline_none(tmp_path, capsys):
    skill = tmp_path / "skill_nopipe.md"
    skill.write_text(_SKILL_NO_PIPELINE, encoding="utf-8")
    code = main(["composer", "validate", str(skill)])
    assert code == 0
    out = capsys.readouterr().out
    assert "pipeline_metadata: none" in out


def test_validate_orphan_section_id_returns_1(tmp_path, capsys):
    skill = tmp_path / "skill_orphan.md"
    skill.write_text(_SKILL_CANONICAL.replace("step_1", "step_real"), encoding="utf-8")
    sidecar = tmp_path / "skill_orphan.pipeline.yaml"
    sidecar.write_text(_VALID_SIDECAR, encoding="utf-8")  # references step_1, no anchor
    skill_text = skill.read_text(encoding="utf-8").replace(
        "skill_demo.pipeline.yaml", "skill_orphan.pipeline.yaml"
    )
    skill.write_text(skill_text, encoding="utf-8")
    code = main(["composer", "validate", str(skill)])
    assert code == 1
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "no matching anchor" in out


def test_validate_missing_sidecar_returns_1(tmp_path, capsys):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    # Don't write the sidecar.
    code = main(["composer", "validate", str(skill)])
    assert code == 1
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "does not exist" in out


def test_validate_directory_recurses(skill_dir, capsys):
    # Add a second clean skill in a subdir to exercise recursion through
    # ``glob("skill_*.md")`` (the loader takes a single dir, no rglob).
    skill_2 = skill_dir / "skill_other.md"
    skill_2.write_text(_SKILL_NO_PIPELINE, encoding="utf-8")
    code = main(["composer", "validate", str(skill_dir)])
    assert code == 0
    out = capsys.readouterr().out
    assert "validated 2 skill(s)" in out
    assert "skill_demo.md" in out
    assert "skill_other.md" in out


def test_validate_missing_path_returns_2(tmp_path, capsys):
    nonexistent = tmp_path / "nope"
    code = main(["composer", "validate", str(nonexistent)])
    assert code == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_validate_json_output_clean(skill_pair, capsys):
    code = main(["composer", "validate", "--format", "json", str(skill_pair)])
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["summary"]["passed"] == 1
    assert payload["summary"]["failed"] == 0
    assert payload["skills"][0]["status"] == "ok"
    assert payload["skills"][0]["step_count"] == 1


def test_validate_json_output_dirty(tmp_path, capsys):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    # No sidecar — will fail with missing-file error.
    code = main(["composer", "validate", "--format", "json", str(skill)])
    assert code == 1
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["summary"]["failed"] == 1
    assert payload["skills"][0]["status"] == "fail"
    assert payload["skills"][0]["error"] is not None


def test_validate_real_skill_canonical():
    """The shipped skill_tessellum_format_check.md uses pipeline_metadata: none."""
    skill = (
        Path(__file__).resolve().parents[2]
        / "vault"
        / "resources"
        / "skills"
        / "skill_tessellum_format_check.md"
    )
    if not skill.is_file():
        pytest.skip(f"real skill not found at {skill}")
    code = main(["composer", "validate", str(skill)])
    assert code == 0


def test_banner_lists_composer(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum composer validate" in out
