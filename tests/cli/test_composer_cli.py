"""Smoke tests for the ``tessellum composer validate`` CLI subcommand.

Single-file skill format: a skill is ONE markdown note. Each pipeline step is
an H2 section carrying a ``<!-- :: section_id = X :: -->`` anchor plus a
leading fenced ``​```yaml`` **contract block**; the prompt prose follows. There
is no ``.pipeline.yaml`` sidecar and no ``pipeline_metadata`` frontmatter
field. A skill with zero contract-block sections compiles to an empty pipeline
(the ``pipeline_metadata: none`` equivalent).
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main

# Frontmatter shared by every fixture skill. No ``pipeline_metadata`` field —
# the pipeline lives in per-section contract blocks now.
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

# One valid step section: the anchor supplies section_id, the leading
# ```yaml``` block supplies the contract, and the prose after it is the
# prompt (the old sidecar's ``prompt_template: "Do something."``).
_SKILL_CANONICAL = _FRONTMATTER + textwrap.dedent(
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

    Do something.
    """
)

# Same skill, but the section is prose-only (no contract block), so the loader
# finds zero pipeline steps → ``load_pipeline`` returns None → the CLI prints
# the ``pipeline_metadata: none`` label. This is the single-file equivalent of
# the old ``pipeline_metadata: none``.
_SKILL_NO_PIPELINE = _FRONTMATTER + textwrap.dedent(
    """\

    # Demo

    ## Step 1 <!-- :: section_id = step_1 :: -->

    Body for step 1.
    """
)

# A step whose inline contract block has a bad ``role`` enum value — a schema
# violation surfaced by ``load_pipeline`` as PipelineValidationError.
_SKILL_BAD_ROLE = _SKILL_CANONICAL.replace("role: CORE", "role: INVENTED_ROLE")

# A step whose inline contract block is not valid YAML (unclosed flow list).
# ``split_contract_and_prompt`` raises before schema validation.
_SKILL_MALFORMED_CONTRACT = _FRONTMATTER + textwrap.dedent(
    """\

    # Demo

    ## Step 1 <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    depends_on: [a, b, c
    ```

    Do something.
    """
)


@pytest.fixture
def skill_dir(tmp_path):
    """A directory with one valid single-file skill."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
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


def test_validate_bad_role_enum_returns_1(tmp_path, capsys):
    """A step's inline contract block with an invalid ``role`` enum fails.

    (Single-file equivalent of the old orphan-section_id test: section_id now
    comes from the anchor so it can never orphan — but a malformed inline
    contract still fails validation with a non-zero exit.)
    """
    skill = tmp_path / "skill_bad_role.md"
    skill.write_text(_SKILL_BAD_ROLE, encoding="utf-8")
    code = main(["composer", "validate", str(skill)])
    assert code == 1
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "schema validation" in out


def test_validate_malformed_contract_block_returns_1(tmp_path, capsys):
    """A step whose inline contract block is not valid YAML fails.

    (Single-file equivalent of the old missing-sidecar test: there is no
    sidecar to be missing anymore, so the failure now comes from a malformed
    inline contract block instead.)
    """
    skill = tmp_path / "skill_malformed.md"
    skill.write_text(_SKILL_MALFORMED_CONTRACT, encoding="utf-8")
    code = main(["composer", "validate", str(skill)])
    assert code == 1
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "not valid YAML" in out


def test_validate_directory_recurses(skill_dir, capsys):
    # Add a second clean skill in the dir to exercise recursion through
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
    skill = tmp_path / "skill_malformed.md"
    # A malformed inline contract block → validation failure.
    skill.write_text(_SKILL_MALFORMED_CONTRACT, encoding="utf-8")
    code = main(["composer", "validate", "--format", "json", str(skill)])
    assert code == 1
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["summary"]["failed"] == 1
    assert payload["skills"][0]["status"] == "fail"
    assert payload["skills"][0]["error"] is not None


def test_validate_real_skill_canonical():
    """The shipped skill_tessellum_format_check.md has no contract-block
    sections, so it validates as a no-pipeline skill (exit 0)."""
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
