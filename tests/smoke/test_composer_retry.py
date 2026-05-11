"""Phase A smoke — retry-budgeted executor + retry-aware prompts.

v0.0.60 of plan_composer_dks_robustness §A. Covers:

  - Logic-failure retry succeeds on attempt 2 (Pattern 2)
  - Same-error short-circuit fires after 3 identical failures (R-7)
  - Crash budget separate from logic budget (Pattern 2 / R-1)
  - {{retry.attempt}} and {{retry.error}} placeholders substitute (Pattern 5)
  - Scheduler keeps running after a step exhausts its retry budgets
    (back-compat: downstream still gets `<missing upstream.X>` sentinels
    rather than crashing the pipeline)
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
    execute_step_with_retry,
    run_pipeline,
)
from tessellum.composer.executor import (
    MAX_CRASH_RECOVERIES,
    MAX_LOGIC_RETRIES,
)
from tessellum.composer.llm import LLMRequest, LLMResponse


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
    date of note: 2026-05-11
    status: active
    building_block: procedure
    pipeline_metadata: ./skill_retry.pipeline.yaml
    ---

    # Demo

    ## Step 1: extract <!-- :: section_id = step_1 :: -->

    Extract from {{leaf.id}}. Attempt {{retry.attempt}}. Prior: {{retry.error}}.
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
        expected_output_schema:
          type: object
          required: [facets]
        prompt_template: "Extract."
        output_key: facets
    """
)


@pytest.fixture
def compiled(tmp_path: Path):
    skill = tmp_path / "skill_retry.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_retry.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return compile_skill(skill)


# ── Helper: a backend that returns a scripted sequence of responses ────────


class _SequenceBackend:
    """MockBackend variant — returns responses in order. Optionally raises
    on specific attempts (for crash testing)."""

    backend_id = "sequence"

    def __init__(
        self,
        responses: list[str] | None = None,
        raise_on_attempts: list[int] | None = None,
    ) -> None:
        self.responses: list[str] = list(responses or [])
        self.raise_on_attempts: list[int] = list(raise_on_attempts or [])
        self.calls: list[LLMRequest] = []
        self._attempt = 0

    def call(self, request: LLMRequest) -> LLMResponse:
        self._attempt += 1
        self.calls.append(request)
        if self._attempt in self.raise_on_attempts:
            raise RuntimeError(f"simulated crash on attempt {self._attempt}")
        if self.responses:
            content = self.responses[
                min(self._attempt - 1, len(self.responses) - 1)
            ]
        else:
            content = "{}"
        return LLMResponse(
            content=content,
            elapsed_ms=0.0,
            backend_id=self.backend_id,
            metadata={"attempt": self._attempt},
        )


# ── A.3 tests ──────────────────────────────────────────────────────────────


def test_executor_retries_logic_failure_succeeds_on_attempt_2(
    compiled, tmp_path: Path
) -> None:
    """First call returns invalid JSON (schema-validation failure); second call
    returns a valid payload. Retry budget covers it; result.error is None."""
    backend = _SequenceBackend(
        responses=[
            "{}",  # missing required `facets` → logic failure
            json.dumps({"facets": ["a", "b"]}),  # ok
        ]
    )
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert isinstance(result, StepResult)
    assert result.error is None
    assert result.attempts == 2
    assert result.retry_kind_history == ("logic", "success")
    # Backend was called twice
    assert len(backend.calls) == 2


def test_executor_retries_same_error_short_circuits(
    compiled, tmp_path: Path
) -> None:
    """3 consecutive identical errors (same hash) → short-circuit before
    exhausting the budget. Budget is 3 logic retries (4 attempts total),
    but same-error loop fires at attempt 3."""
    backend = _SequenceBackend(responses=["{}"] * 10)
    # Note: 10 responses queued but only 3 should be consumed before the
    # loop detector short-circuits.
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is not None
    assert "same-error loop" in result.error
    # Same-error fires when history has 3 identical entries — attempt 3 makes
    # the history length 3, so attempt 3 short-circuits.
    assert result.attempts == 3
    assert result.retry_kind_history == ("logic", "logic", "logic")
    assert len(backend.calls) == 3


def test_executor_crash_recovery_separate_from_logic(
    compiled, tmp_path: Path
) -> None:
    """Backend raises on attempts 1 + 2 (crashes), then returns clean response.
    Logic budget untouched; crash budget consumed by 2."""
    backend = _SequenceBackend(
        responses=["", "", json.dumps({"facets": ["ok"]})],
        raise_on_attempts=[1, 2],
    )
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is None
    assert result.attempts == 3
    assert result.retry_kind_history == ("crash", "crash", "success")


def test_executor_crash_budget_exhausted(compiled, tmp_path: Path) -> None:
    """Backend raises on every call — crash budget exhausts after
    MAX_CRASH_RECOVERIES (2). Returns clean StepResult with error set."""
    backend = _SequenceBackend(
        responses=["x"] * 10,
        raise_on_attempts=list(range(1, 11)),
    )
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is not None
    # Same-error short-circuit fires before budget — every crash has the
    # same error message, so 3 identical hashes triggers the loop guard.
    # Either short-circuit OR budget-exhausted is acceptable; both are
    # correct safety behaviours.
    assert "crash" in result.error.lower() or "loop" in result.error.lower()
    assert result.attempts >= 3


def test_executor_retry_context_substitutes(compiled, tmp_path: Path) -> None:
    """{{retry.attempt}} and {{retry.error}} appear in the rendered prompt
    on the retry attempt. First-call prompt has attempt=1 + empty error;
    second-call prompt has attempt=2 + the prior error message."""
    backend = _SequenceBackend(
        responses=[
            "{}",  # first call fails schema validation
            json.dumps({"facets": []}),  # second call succeeds
        ]
    )
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is None
    # First call: attempt=1, empty error
    first_prompt = backend.calls[0].user_prompt
    assert "Attempt 1" in first_prompt
    # Second call: attempt=2, prior error mentioned
    second_prompt = backend.calls[1].user_prompt
    assert "Attempt 2" in second_prompt
    # The schema-validation error mentions "facets"
    assert "facets" in second_prompt.lower()
    # And the system prompt on retry has the [Retry attempt N:...] prefix
    assert "[Retry attempt 2:" in backend.calls[1].system_prompt


def test_executor_no_retry_when_first_call_succeeds(compiled, tmp_path: Path) -> None:
    """When the first attempt succeeds, attempts=1 and retry_kind_history is
    just ('success',)."""
    backend = _SequenceBackend(responses=[json.dumps({"facets": ["a"]})])
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is None
    assert result.attempts == 1
    assert result.retry_kind_history == ("success",)


# ── A.3 scheduler-level test: failed step does not cascade ─────────────────


_TWO_STEP_CANONICAL = textwrap.dedent(
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
    date of note: 2026-05-11
    status: active
    building_block: procedure
    pipeline_metadata: ./skill_chained.pipeline.yaml
    ---

    # Chained

    ## Step 1: produce <!-- :: section_id = step_1 :: -->

    Produce data for {{leaf.id}}.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    Consume upstream: {{upstream.produced}}.
    """
)


_TWO_STEP_SIDECAR = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        expected_output_schema:
          type: object
          required: [produced]
        prompt_template: "Produce."
        output_key: produced
      - section_id: step_2
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: [step_1]
        materializer: no_op
        prompt_template: "Consume."
        output_key: consumed
    """
)


def test_scheduler_failed_step_does_not_crash_downstream(tmp_path: Path) -> None:
    """When step_1 exhausts its retry budget (all same-error → short-circuit
    at attempt 3), step_2 still runs but its {{upstream.produced}} resolves
    to the missing-sentinel. Pipeline returns with error_count >= 1, not a
    crash."""
    skill = tmp_path / "skill_chained.md"
    skill.write_text(_TWO_STEP_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_chained.pipeline.yaml").write_text(
        _TWO_STEP_SIDECAR, encoding="utf-8"
    )
    compiled = compile_skill(skill)
    # step_1 always returns invalid JSON; step_2 returns ok.
    backend = MockBackend(
        responses={
            "Produce": "{}",  # always fails schema for produced
            "Consume": json.dumps({"consumed": "ok"}),
        }
    )
    result = run_pipeline(
        compiled,
        leaves=[{"_id": "leaf_0", "id": "x"}],
        backend=backend,
        vault_root=tmp_path,
    )
    # Pipeline did NOT crash.
    assert result.error_count >= 1
    # step_2 still ran (downstream sees missing sentinel but doesn't crash).
    section_ids = [r.section_id for r in result.step_results]
    assert "step_2" in section_ids
    # step_1's result has the same-error-loop error
    step_1_results = [r for r in result.step_results if r.section_id == "step_1"]
    assert step_1_results
    assert step_1_results[0].error is not None


# ── Defaults ───────────────────────────────────────────────────────────────


def test_executor_module_constants_present():
    assert MAX_LOGIC_RETRIES == 3
    assert MAX_CRASH_RECOVERIES == 2
