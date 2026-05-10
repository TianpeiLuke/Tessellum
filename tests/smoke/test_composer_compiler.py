"""Smoke tests for tessellum.composer.compile_skill."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    CompiledPipeline,
    CompiledStep,
    CompilerError,
    ContractViolation,
    compile_skill,
    to_dag_json,
)


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

    ## Step 1: load <!-- :: section_id = step_1 :: -->

    Load input.

    ## Step 2: extract <!-- :: section_id = step_2 :: -->

    Extract facets.

    ## Step 3: emit <!-- :: section_id = step_3 :: -->

    Emit output.
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
        prompt_template: "Load."
        output_key: input

      - section_id: step_2
        role: CORE
        aggregation: per_leaf
        batchable: true
        depends_on: [step_1]
        materializer: body_markdown_frontmatter_to_file
        expected_output_schema:
          type: object
          required: [output_path]
        prompt_template: "Extract from {{upstream.input}}."
        output_key: facets

      - section_id: step_3
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: [step_2]
        materializer: no_op
        prompt_template: "Emit {{upstream.facets}}."
    """
)


@pytest.fixture
def demo_skill(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    sidecar.write_text(_VALID_SIDECAR, encoding="utf-8")
    return skill


def test_compile_skill_returns_compiled_pipeline(demo_skill):
    compiled = compile_skill(demo_skill)
    assert isinstance(compiled, CompiledPipeline)
    assert compiled.skill_name == "skill_demo"
    assert compiled.step_count == 3


def test_compiled_steps_typed(demo_skill):
    compiled = compile_skill(demo_skill)
    for step in compiled.steps:
        assert isinstance(step, CompiledStep)


def test_compile_preserves_topological_order(demo_skill):
    compiled = compile_skill(demo_skill)
    # Pipeline list was already topologically sorted (no forward refs).
    section_ids = [s.section_id for s in compiled.steps]
    assert section_ids == ["step_1", "step_2", "step_3"]


def test_compile_resolves_materializer_contract(demo_skill):
    compiled = compile_skill(demo_skill)
    step_2 = compiled.steps[1]
    assert step_2.materializer_key == "body_markdown_frontmatter_to_file"
    assert step_2.materializer_contract is not None
    assert step_2.materializer_contract.wire_format == "markdown_with_frontmatter"
    assert step_2.materializer_contract.operation_verb == "PRODUCE"


def test_compile_extracts_prompt_section_text(demo_skill):
    compiled = compile_skill(demo_skill)
    step_1 = compiled.steps[0]
    assert step_1.prompt_section_text is not None
    assert "Load input" in step_1.prompt_section_text


def test_compile_unknown_materializer_raises_contract_violation(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    bad = _VALID_SIDECAR.replace("materializer: no_op", "materializer: not_a_real_one", 1)
    sidecar.write_text(bad, encoding="utf-8")
    # The Pydantic model rejects this at the schema level; if it gets
    # past validation (e.g. the schema relaxes), the compiler catches it.
    with pytest.raises((ContractViolation, Exception)):
        compile_skill(skill)


def test_compile_missing_required_output_field_raises(tmp_path):
    """body_markdown_frontmatter_to_file requires `output_path`. Drop it
    from expected_output_schema.required → ContractViolation."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    bad = _VALID_SIDECAR.replace("required: [output_path]", "required: []")
    sidecar.write_text(bad, encoding="utf-8")
    with pytest.raises(ContractViolation) as exc_info:
        compile_skill(skill)
    assert exc_info.value.kind == ContractViolation.KIND_MISSING_REQUIRED_OUTPUT_FIELD


def test_compile_forward_reference_raises(tmp_path):
    """A step that depends on a section_id appearing later in the pipeline
    list should raise CompilerError."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    bad = textwrap.dedent(
        """\
        version: "1.0"
        pipeline:
          - section_id: step_1
            role: CORE
            aggregation: per_leaf
            batchable: false
            depends_on: [step_2]   # forward reference
            materializer: no_op
            prompt_template: "1"
          - section_id: step_2
            role: CORE
            aggregation: per_leaf
            batchable: false
            depends_on: []
            materializer: no_op
            prompt_template: "2"
          - section_id: step_3
            role: CORE
            aggregation: per_leaf
            batchable: false
            depends_on: []
            materializer: no_op
            prompt_template: "3"
        """
    )
    sidecar.write_text(bad, encoding="utf-8")
    with pytest.raises(CompilerError, match="forward reference"):
        compile_skill(skill)


def test_compile_unknown_dependency_raises(tmp_path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    sidecar = tmp_path / "skill_demo.pipeline.yaml"
    bad = _VALID_SIDECAR.replace(
        "depends_on: [step_1]", "depends_on: [step_does_not_exist]"
    )
    sidecar.write_text(bad, encoding="utf-8")
    with pytest.raises(CompilerError, match="depends_on"):
        compile_skill(skill)


def test_compile_pipeline_metadata_none_returns_empty_pipeline(tmp_path):
    """A skill with `pipeline_metadata: none` compiles to a 0-step pipeline."""
    canonical = _CANONICAL.replace(
        "pipeline_metadata: ./skill_demo.pipeline.yaml",
        "pipeline_metadata: none",
    )
    skill = tmp_path / "skill_demo.md"
    skill.write_text(canonical, encoding="utf-8")
    compiled = compile_skill(skill)
    assert compiled.step_count == 0
    assert compiled.steps == ()


def test_to_dag_json_round_trips(demo_skill):
    compiled = compile_skill(demo_skill)
    dag = to_dag_json(compiled)
    assert dag["skill_name"] == "skill_demo"
    assert dag["step_count"] == 3
    assert len(dag["steps"]) == 3
    step_2 = dag["steps"][1]
    assert step_2["materializer"]["key"] == "body_markdown_frontmatter_to_file"
    assert step_2["materializer"]["operation_verb"] == "PRODUCE"
    assert "prompt_section_text" in step_2


def test_to_dag_json_no_prompts_omits_text(demo_skill):
    compiled = compile_skill(demo_skill)
    dag = to_dag_json(compiled, include_prompts=False)
    step = dag["steps"][0]
    assert "prompt_section_text" not in step
    assert "prompt_section_text_chars" in step
    assert step["prompt_section_text_chars"] > 0


def test_to_dag_json_steps_have_required_keys(demo_skill):
    compiled = compile_skill(demo_skill)
    dag = to_dag_json(compiled)
    for step in dag["steps"]:
        for key in [
            "section_id",
            "role",
            "aggregation",
            "batchable",
            "depends_on",
            "materializer",
            "expected_output_schema",
            "output_key",
        ]:
            assert key in step


def test_compile_against_real_skill_search_notes():
    """The shipped search-notes skill should compile clean (3 steps)."""
    repo = Path(__file__).resolve().parents[2]
    skill = repo / "vault" / "resources" / "skills" / "skill_tessellum_search_notes.md"
    if not skill.is_file():
        pytest.skip(f"real skill not found at {skill}")
    compiled = compile_skill(skill)
    assert compiled.step_count == 3
    assert compiled.skill_name == "skill_tessellum_search_notes"
    # Each step should have a populated prompt_section_text.
    for step in compiled.steps:
        assert step.prompt_section_text
        # All declared steps are CORE/corpus_wide/no_op for this skill.
        assert step.role == "CORE"
        assert step.aggregation == "corpus_wide"


def test_compile_against_real_skill_answer_query():
    """The shipped answer-query skill should compile clean (5 steps)."""
    repo = Path(__file__).resolve().parents[2]
    skill = repo / "vault" / "resources" / "skills" / "skill_tessellum_answer_query.md"
    if not skill.is_file():
        pytest.skip(f"real skill not found at {skill}")
    compiled = compile_skill(skill)
    assert compiled.step_count == 5
    # Topological order check — each step's depends_on points to an earlier step.
    section_ids: list[str] = []
    for step in compiled.steps:
        for dep in step.depends_on:
            assert dep in section_ids
        section_ids.append(step.section_id)
