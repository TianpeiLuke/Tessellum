"""Smoke tests for tessellum.composer.loader (single-file skill format).

A skill is one markdown canonical: each pipeline step is an H2 section
carrying a ``<!-- :: section_id = X :: -->`` anchor plus a leading fenced
``​```yaml`` contract block, with the step's prompt prose after it. There is
no ``.pipeline.yaml`` sidecar and no ``pipeline_metadata`` frontmatter field.
"""

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


def _write_skill(tmp_path, body: str, name: str = "skill_demo.md"):
    """Write a single-file skill: frontmatter + H1 + the given section body."""
    skill = tmp_path / name
    skill.write_text(
        _FRONTMATTER + "\n# Demo Skill\n\n" + textwrap.dedent(body),
        encoding="utf-8",
    )
    return skill


# A complete single-file skill with two step sections. Each step's fields live
# in a leading ```yaml``` contract block; the old sidecar prompt_template is now
# the prose after the block. section_id comes from the anchor, not the block.
_SKILL_SINGLE_FILE = textwrap.dedent(
    """\
    ## Step 1: load <!-- :: section_id = step_1_load :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: body_markdown_frontmatter_to_file
    expected_output_schema:
      type: object
      required: [output_path]
    ```

    Load the input.

    ## Step 2: extract <!-- :: section_id = step_2_extract :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: true
    depends_on: [step_1_load]
    materializer: no_op
    expected_output_schema:
      type: object
      required: [facets]
    mcp_dependencies:
      - name: my-test-mcp
        calls: [Search]
        required: false
    ```

    Extract facets from {{upstream.step_1_load}}.
    """
)

# A skill whose sections have NO contract blocks — prose only. It compiles to
# an empty pipeline (0 steps), the single-file equivalent of the old
# ``pipeline_metadata: none``. load_pipeline returns None.
_SKILL_NO_PIPELINE = textwrap.dedent(
    """\
    ## Setup <!-- :: section_id = setup :: -->

    Prose-only section. No contract block, so it is not a pipeline step.

    ## Resources <!-- :: section_id = resources :: -->

    Also prose only.
    """
)


@pytest.fixture
def demo_skill(tmp_path):
    return _write_skill(tmp_path, _SKILL_SINGLE_FILE)


@pytest.fixture
def skill_no_pipeline(tmp_path):
    return _write_skill(tmp_path, _SKILL_NO_PIPELINE, name="skill_nopipe.md")


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


def test_load_pipeline_returns_none_when_no_step_sections(skill_no_pipeline):
    # A skill with zero contract-block sections compiles to an empty pipeline
    # (0 steps) — the single-file equivalent of ``pipeline_metadata: none``.
    assert load_pipeline(skill_no_pipeline) is None


def test_load_pipeline_missing_skill_file_raises(tmp_path):
    # Single-file equivalent of the old missing-sidecar test: the pipeline
    # source (the skill canonical itself) is unreadable, which surfaces as a
    # PipelineValidationError rather than an OSError leaking out.
    missing = tmp_path / "no_such_skill.md"
    with pytest.raises(PipelineValidationError, match="cannot parse skill"):
        load_pipeline(missing)


def test_load_pipeline_invalid_yaml_raises(tmp_path):
    # A malformed leading contract block: unclosed flow-style list — a
    # definite YAML parse error surfaced by split_contract_and_prompt.
    skill = _write_skill(
        tmp_path,
        """\
        ## Step 1: load <!-- :: section_id = step_1_load :: -->

        ```yaml
        role: CORE
        depends_on: [a, b, c
        ```

        Load the input.
        """,
    )
    with pytest.raises(PipelineValidationError, match="not valid YAML"):
        load_pipeline(skill)


def test_load_pipeline_schema_violation_role_enum(tmp_path):
    skill = _write_skill(
        tmp_path,
        """\
        ## Step 1: load <!-- :: section_id = step_1_load :: -->

        ```yaml
        role: INVENTED_ROLE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        Load the input.
        """,
    )
    with pytest.raises(PipelineValidationError, match="schema validation"):
        load_pipeline(skill)


def test_load_pipeline_schema_violation_missing_required_field(tmp_path):
    # ``batchable`` is a schema-required Step field; its absence must fail
    # Stage-1 schema validation even though the section_id comes from the
    # anchor.
    skill = _write_skill(
        tmp_path,
        """\
        ## Step 1: load <!-- :: section_id = step_1_load :: -->

        ```yaml
        role: CORE
        aggregation: per_leaf
        depends_on: []
        materializer: no_op
        ```

        Load the input.
        """,
    )
    with pytest.raises(PipelineValidationError, match="schema validation"):
        load_pipeline(skill)


def test_load_pipeline_anchor_overrides_contract_section_id(tmp_path):
    """A contract block's own ``section_id`` is ignored — the anchor wins.

    The old two-file format could declare a sidecar step whose section_id had
    no matching anchor ("orphan"); single-file makes that structurally
    impossible because the step's section_id always comes from its anchor.
    This test pins that invariant: a bogus section_id in the block is
    overridden by the anchor rather than producing an orphan.
    """
    skill = _write_skill(
        tmp_path,
        """\
        ## Step 1: load <!-- :: section_id = step_1_load :: -->

        ```yaml
        section_id: step_999_orphan
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        Load the input.
        """,
    )
    pipeline = load_pipeline(skill)
    assert pipeline is not None
    assert pipeline.pipeline[0].section_id == "step_1_load"


def test_load_pipeline_contract_block_must_be_mapping(tmp_path):
    # Single-file analogue of the old "sidecar top-level must be a mapping":
    # a leading contract block whose top level is a list, not a mapping.
    skill = _write_skill(
        tmp_path,
        """\
        ## Step 1: load <!-- :: section_id = step_1_load :: -->

        ```yaml
        - just
        - a
        - list
        ```

        Load the input.
        """,
    )
    with pytest.raises(PipelineValidationError, match="must be a mapping"):
        load_pipeline(skill)
