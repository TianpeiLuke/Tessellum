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
    LLMResponse,
    MockBackend,
    StepResult,
    compile_skill,
    execute_step,
)
from tessellum.composer.executor import classify_error


# Single-file skill: each pipeline step is an H2 section carrying a
# <!-- :: section_id = X :: --> anchor, a leading ```yaml``` contract block
# (the typed step declaration), and the prompt prose after it. There is no
# separate .pipeline.yaml sidecar and no pipeline_metadata frontmatter field.
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
    ---

    # Demo

    ## Step 1: load <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: loaded
    ```

    Loading {{leaf.id}} for upstream {{upstream.prev}}.

    ## Step 2: extract <!-- :: section_id = step_2 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: [step_1]
    materializer: no_op
    output_key: facets
    expected_output_schema:
      type: object
      required: [facets]
    ```

    Extract.
    """
)


@pytest.fixture
def compiled(tmp_path: Path):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
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


# ── Context assembler — fail-soft prompt bounding ───────────────────────────


def test_executor_context_assembler_bounds_oversized_prompt(compiled, tmp_path: Path) -> None:
    """With a context_assembler, an oversized rendered prompt is truncated +
    warned (fail-soft), NOT turned into a validation error, and the bounded
    text is what reaches the backend."""
    from tessellum.composer.context_assembler import FullSourceAssembler

    backend = MockBackend(default='{"ok": true}')
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "Z" * 5000},  # 5000-char leaf field
        upstream={"prev": "P"},
        backend=backend,
        vault_root=tmp_path,
        context_assembler=FullSourceAssembler(max_chars=200),
    )
    assert result.error is None  # degraded, not errored
    # The backend saw the bounded (≤200-char) prompt, not the full 5000.
    assert len(backend.calls[0].user_prompt) <= 200
    # A truncation warning surfaced in the response metadata.
    warnings = result.response.metadata.get("context_warnings")
    assert warnings and any("truncated" in w for w in warnings)


def test_executor_context_assembler_clean_when_under_budget(compiled, tmp_path: Path) -> None:
    """A prompt under the assembler's budget passes through with no warning."""
    from tessellum.composer.context_assembler import FullSourceAssembler

    backend = MockBackend(default='{"ok": true}')
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "small"},
        upstream={"prev": "P"},
        backend=backend,
        vault_root=tmp_path,
        context_assembler=FullSourceAssembler(max_chars=100_000),
    )
    assert result.error is None
    assert "context_warnings" not in result.response.metadata


def test_executor_no_assembler_preserves_hard_cap(compiled, tmp_path: Path) -> None:
    """Without an assembler, an oversized prompt is still the hard-cap
    validation error (parity with the pre-assembler behaviour)."""
    backend = MockBackend(default='{"ok": true}')
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "Z" * 2_000_000},  # beyond HARD_PROMPT_CAP_CHARS
        upstream={"prev": "P"},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is not None
    assert "HARD_PROMPT_CAP_CHARS" in result.error
    assert result.error_class == "validation"


# ── R3 (FZ 20k9c1a1a1b7c2g / E14): per-step max_tokens response budget ────────

_MAXTOK_CANONICAL = textwrap.dedent(
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
    date of note: 2026-07-27
    status: active
    building_block: procedure
    ---

    # MaxTok Demo

    ## Step big: writer <!-- :: section_id = big_writer :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: big
    max_tokens: 32000
    ```

    Write a large thing.

    ## Step small: classify <!-- :: section_id = small_step :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: small
    ```

    Classify.
    """
)


@pytest.fixture
def maxtok_compiled(tmp_path: Path):
    skill = tmp_path / "skill_maxtok.md"
    skill.write_text(_MAXTOK_CANONICAL, encoding="utf-8")
    return compile_skill(skill)


def test_compiled_step_carries_per_step_max_tokens(maxtok_compiled):
    """A step declaring ``max_tokens`` in its contract carries it onto the
    CompiledStep; a step omitting it stays ``None`` (inherit the default)."""
    by_id = {s.section_id: s for s in maxtok_compiled.steps}
    assert by_id["big_writer"].max_tokens == 32000
    assert by_id["small_step"].max_tokens is None


def test_executor_passes_per_step_max_tokens_to_request(maxtok_compiled, tmp_path: Path):
    """The executor threads a step's ``max_tokens`` into the LLMRequest so a
    big-output writer gets its larger response budget (the E14 fix — the
    augmented plan truncated at the 16000 global default)."""
    backend = MockBackend(default='{"ok": true}')
    big = [s for s in maxtok_compiled.steps if s.section_id == "big_writer"][0]
    execute_step(big, leaf={"_id": "corpus"}, upstream={}, backend=backend, vault_root=tmp_path)
    assert backend.calls[0].max_tokens == 32000


def test_executor_defaults_max_tokens_when_step_unset(maxtok_compiled, tmp_path: Path):
    """A step without ``max_tokens`` inherits the LLMRequest default (16000) —
    the executor must not force a value, so small steps aren't silently widened."""
    backend = MockBackend(default='{"ok": true}')
    small = [s for s in maxtok_compiled.steps if s.section_id == "small_step"][0]
    execute_step(small, leaf={"_id": "corpus"}, upstream={}, backend=backend, vault_root=tmp_path)
    assert backend.calls[0].max_tokens == 16000  # LLMRequest default, not overridden


# ── P10 (FZ 20k9c1a1a1b7c2g): truncation is a first-class diagnosis, not "invalid JSON" ──

class _TruncatingBackend:
    """A backend whose response is cut off at the token cap — carries
    ``stop_reason='max_tokens'`` + a partial (unparseable) JSON body, exactly
    what the real SDK returns on truncation."""

    backend_id = "fake-truncating"

    def call(self, request):  # noqa: ANN001 — test double
        return LLMResponse(
            content='{"facets": "the body was cut off mid-str',  # truncated JSON
            elapsed_ms=1.0,
            backend_id=self.backend_id,
            metadata={"stop_reason": "max_tokens", "output_tokens": 32000},
        )


def test_executor_diagnoses_truncation_not_invalid_json(compiled, tmp_path: Path):
    """A response truncated at the token cap must be diagnosed as TRUNCATED
    (actionable: raise max_tokens), NOT misclassified as 'not valid JSON' /
    'validation' — the E14/E15 misdiagnosis P10 fixes. step_2 consumes JSON."""
    step2 = compiled.steps[1]  # has expected_output_schema (JSON-consuming)
    result = execute_step(
        step2, leaf={"_id": "leaf_0", "id": "x"}, upstream={"prev": "P"},
        backend=_TruncatingBackend(), vault_root=tmp_path,
    )
    assert result.error is not None
    assert "truncated at max_tokens" in result.error
    assert "32000 output tokens" in result.error
    assert result.error_class == "truncated"
    # The size diagnosis wins — it must NOT read as a schema/JSON validation defect.
    assert "not valid json" not in result.error.lower()
    assert "schema validation" not in result.error.lower()


def test_classify_error_recognizes_truncation_above_validation():
    """classify_error ranks truncation above validation: a truncated payload
    also fails JSON parse, but the actionable class is 'truncated'."""
    msg = "response truncated at max_tokens (32000 output tokens) — raise the step's max_tokens or split the output"
    assert classify_error(msg) == "truncated"
