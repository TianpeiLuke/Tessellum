"""Smoke tests for ``tessellum composer compile``."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main


# Shared frontmatter for the single-file demo skills. Note there is NO
# ``pipeline_metadata`` field: a skill is one markdown note, and each pipeline
# step is an H2 section carrying a ``<!-- :: section_id = X :: -->`` anchor
# plus a leading fenced ```yaml``` contract block (the typed step declaration),
# with the step's prompt prose after the block.
_FRONTMATTER = textwrap.dedent(
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
    ---
    """
)


# Two step sections, each with its contract block folded in (formerly the
# ``.pipeline.yaml`` sidecar) and the old sidecar ``prompt_template`` as the
# prose after the block. step_2 depends on step_1.
_CANONICAL = _FRONTMATTER + textwrap.dedent(
    """\

    # Demo

    ## Step 1 <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: step_1_out
    ```

    Step 1.

    ## Step 2 <!-- :: section_id = step_2 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: [step_1]
    materializer: no_op
    output_key: step_2_out
    ```

    Step 2.
    """
)


@pytest.fixture
def demo_skill(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
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
    """A skill whose inline contract block is schema-invalid fails to compile.

    Single-file equivalent of the old malformed-sidecar case: a bad ``role``
    enum in a step's leading ```yaml``` contract block makes ``load_pipeline``
    raise ``PipelineValidationError`` ("fails schema validation"), which the
    CLI surfaces as a compile failure (exit 1).
    """
    canonical = _FRONTMATTER + textwrap.dedent(
        """\

        # Demo

        ## Step 1 <!-- :: section_id = step_1 :: -->

        ```yaml
        role: NOT_A_VALID_ROLE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        Step 1.
        """
    )
    skill = tmp_path / "skill_demo.md"
    skill.write_text(canonical, encoding="utf-8")
    code = main(["composer", "compile", str(skill)])
    assert code == 1
    captured = capsys.readouterr()
    assert "validation FAILED" in captured.out
    assert "schema validation" in captured.err


def test_compile_pipeline_none_returns_0_with_empty_pipeline(tmp_path, capsys):
    # A skill with ZERO contract-block sections compiles to an empty pipeline
    # (the single-file equivalent of the old ``pipeline_metadata: none``): the
    # step sections are prose-only, so the loader finds no steps.
    canonical = _FRONTMATTER + textwrap.dedent(
        """\

        # Demo

        ## Step 1 <!-- :: section_id = step_1 :: -->

        Body 1.

        ## Step 2 <!-- :: section_id = step_2 :: -->

        Body 2.
        """
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
