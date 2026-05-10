"""Smoke tests for tessellum.composer.loader."""

from __future__ import annotations

import textwrap

import pytest

from tessellum.composer.loader import (
    MCPDependency,
    Pipeline,
    PipelineStep,
    PipelineValidationError,
    load_pipeline,
)

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

    # Demo Skill

    ## Step 1: load <!-- :: section_id = step_1_load :: -->

    Body for step 1.

    ## Step 2: extract <!-- :: section_id = step_2_extract :: -->

    Body for step 2.
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
      - section_id: step_1_load
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: body_markdown_frontmatter_to_file
        prompt_template: "Load the input."
        expected_output_schema:
          type: object
          required: [output_path]
      - section_id: step_2_extract
        role: CORE
        aggregation: per_leaf
        batchable: true
        depends_on: [step_1_load]
        materializer: no_op
        prompt_template: "Extract facets from {{upstream.step_1_load}}."
        expected_output_schema:
          type: object
          required: [facets]
        mcp_dependencies:
          - name: my-test-mcp
            calls: [Search]
            required: false
    """
)


@pytest.fixture
def demo_skill(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    sidecar.write_text(_VALID_SIDECAR, encoding="utf-8")
    return skill


@pytest.fixture
def skill_no_pipeline(tmp_path):
    skill = tmp_path / "skill_nopipe.md"
    skill.write_text(_SKILL_NO_PIPELINE, encoding="utf-8")
    return skill


def test_load_pipeline_returns_pipeline_object(demo_skill):
    pipeline = load_pipeline(demo_skill)
    assert isinstance(pipeline, Pipeline)
    assert pipeline.version == "1.0"
    assert len(pipeline.pipeline) == 2


def test_load_pipeline_steps_are_typed(demo_skill):
    pipeline = load_pipeline(demo_skill)
    step_1 = pipeline.pipeline[0]
    assert isinstance(step_1, PipelineStep)
    assert step_1.section_id == "step_1_load"
    assert step_1.role == "CORE"
    assert step_1.aggregation == "per_leaf"
    assert step_1.batchable is False
    assert step_1.depends_on == ()


def test_load_pipeline_resolves_dependencies(demo_skill):
    pipeline = load_pipeline(demo_skill)
    step_2 = pipeline.pipeline[1]
    assert step_2.depends_on == ("step_1_load",)
    assert step_2.materializer == "no_op"


def test_load_pipeline_typed_mcp_dependencies(demo_skill):
    pipeline = load_pipeline(demo_skill)
    step_2 = pipeline.pipeline[1]
    assert len(step_2.mcp_dependencies) == 1
    dep = step_2.mcp_dependencies[0]
    assert isinstance(dep, MCPDependency)
    assert dep.name == "my-test-mcp"
    assert dep.calls == ("Search",)
    assert dep.required is False


def test_load_pipeline_returns_none_for_pipeline_metadata_none(skill_no_pipeline):
    assert load_pipeline(skill_no_pipeline) is None


def test_load_pipeline_missing_sidecar_raises(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    # Don't create the sidecar.
    with pytest.raises(PipelineValidationError, match="does not exist"):
        load_pipeline(skill)


def test_load_pipeline_invalid_yaml_raises(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    # Unclosed flow-style list — definite YAML parse error.
    sidecar.write_text("pipeline: [a, b, c", encoding="utf-8")
    with pytest.raises(PipelineValidationError, match="not valid YAML"):
        load_pipeline(skill)


def test_load_pipeline_schema_violation_role_enum(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    bad = _VALID_SIDECAR.replace("role: CORE", "role: INVENTED_ROLE", 1)
    sidecar.write_text(bad, encoding="utf-8")
    with pytest.raises(PipelineValidationError, match="schema validation"):
        load_pipeline(skill)


def test_load_pipeline_schema_violation_missing_required_field(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    # Strip ``batchable: false`` from step 1 (4-space indent after dedent).
    bad = _VALID_SIDECAR.replace("    batchable: false\n", "")
    assert bad != _VALID_SIDECAR, "fixture replacement failed — indent changed"
    sidecar.write_text(bad, encoding="utf-8")
    with pytest.raises(PipelineValidationError, match="schema validation"):
        load_pipeline(skill)


def test_load_pipeline_orphan_section_id_raises(tmp_path):
    """Sidecar declares a section_id with no matching anchor in the canonical."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    bad = _VALID_SIDECAR.replace("step_2_extract", "step_999_orphan")
    sidecar.write_text(bad, encoding="utf-8")
    with pytest.raises(PipelineValidationError, match="no matching anchor"):
        load_pipeline(skill)


def test_load_pipeline_top_level_must_be_mapping(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_SKILL_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    sidecar.write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(PipelineValidationError, match="must be a mapping"):
        load_pipeline(skill)
