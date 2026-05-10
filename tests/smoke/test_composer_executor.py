"""Wave 3 smoke — single-step executor.

Builds real CompiledStep instances via compile_skill, then exercises:

  - {{leaf.X}} and {{upstream.Y}} placeholder resolution
  - MockBackend dispatch + recorded calls
  - Schema validation surfacing on StepResult.error
  - Materializer dispatch + error surfacing
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    MockBackend,
    StepResult,
    compile_skill,
    execute_step,
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

    Loading {{leaf.id}} for upstream {{upstream.prev}}.

    ## Step 2: extract <!-- :: section_id = step_2 :: -->

    Extract.
    """
)


_SIDECAR = textwrap.dedent(
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
        output_key: loaded
      - section_id: step_2
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: [step_1]
        materializer: no_op
        expected_output_schema:
          type: object
          required: [facets]
        prompt_template: "Extract."
        output_key: facets
    """
)


@pytest.fixture
def compiled(tmp_path: Path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_demo.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return compile_skill(skill)


def test_executor_resolves_leaf_placeholder(compiled, tmp_path: Path) -> None:
    backend = MockBackend(responses={"abc-123": '{"hit": true}'})
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "abc-123"},
        upstream={"prev": "PREV"},
        backend=backend,
        vault_root=tmp_path,
    )
    assert isinstance(result, StepResult)
    assert result.error is None
    assert result.section_id == "step_1"
    assert result.leaf_id == "leaf_0"
    # Placeholder resolution: {{leaf.id}} → "abc-123" was substituted before backend call.
    assert "abc-123" in backend.calls[0].user_prompt
    assert "PREV" in backend.calls[0].user_prompt
    # MockBackend's pattern matched → JSON parsed into structured.
    assert result.materialized.structured == {"hit": True}


def test_executor_marks_missing_placeholders(compiled, tmp_path: Path) -> None:
    backend = MockBackend()
    execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0"},  # no `id` key
        upstream={},  # no `prev` key
        backend=backend,
        vault_root=tmp_path,
    )
    prompt = backend.calls[0].user_prompt
    assert "<missing leaf.id>" in prompt
    assert "<missing upstream.prev>" in prompt


def test_executor_schema_validation_failure_surfaces_on_error(
    compiled, tmp_path: Path
) -> None:
    """Step 2 declares schema with required: [facets]; the mock returns {} → error."""
    backend = MockBackend(default="{}")
    result = execute_step(
        compiled.steps[1],
        leaf={"_id": "leaf_0"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    # Soft error — populated, doesn't raise.
    assert result.error is not None
    assert "schema" in result.error.lower() or "facets" in result.error.lower()


def test_executor_schema_validation_passes_on_valid_response(
    compiled, tmp_path: Path
) -> None:
    backend = MockBackend(default=json.dumps({"facets": ["a", "b"]}))
    result = execute_step(
        compiled.steps[1],
        leaf={"_id": "leaf_0"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is None
    assert result.materialized.structured == {"facets": ["a", "b"]}


def test_executor_records_elapsed_ms(compiled, tmp_path: Path) -> None:
    backend = MockBackend(default='{"facets": []}')
    result = execute_step(
        compiled.steps[1],
        leaf={"_id": "leaf_0"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.elapsed_ms >= 0


def test_executor_stringifies_dict_upstream(compiled, tmp_path: Path) -> None:
    """When upstream value is a dict, it should be JSON-serialized in the prompt."""
    backend = MockBackend()
    execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={"prev": {"key": "value"}},
        backend=backend,
        vault_root=tmp_path,
    )
    assert '"key"' in backend.calls[0].user_prompt
    assert '"value"' in backend.calls[0].user_prompt
