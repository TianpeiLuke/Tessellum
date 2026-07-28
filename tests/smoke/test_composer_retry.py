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
    MAX_TRUNCATION_CEILING_TOKENS,
    MAX_TRUNCATION_RETRIES,
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
    ---

    # Demo

    ## Step 1: extract <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    expected_output_schema:
      type: object
      required: [facets]
    output_key: facets
    ```

    Extract from {{leaf.id}}. Attempt {{retry.attempt}}. Prior: {{retry.error}}.
    """
)


@pytest.fixture
def compiled(tmp_path: Path):
    skill = tmp_path / "skill_retry.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
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
    ---

    # Chained

    ## Step 1: produce <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    expected_output_schema:
      type: object
      required: [produced]
    output_key: produced
    ```

    Produce data for {{leaf.id}}.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: [step_1]
    materializer: no_op
    output_key: consumed
    ```

    Consume upstream: {{upstream.produced}}.
    """
)


def test_scheduler_failed_producer_fails_consumer_loud_not_sentinel(tmp_path: Path) -> None:
    """P23 (FZ 20k9c1a1a1b7c2h/g): when step_1 (a depends_on producer of
    `produced`) exhausts its budget, step_2's required {{upstream.produced}} is
    absent — step_2 now FAILS LOUD with error_class=`missing_consumed` instead of
    silently dispatching a `<missing upstream.produced>` sentinel into its prompt
    (which produced garbage that looked like a model failure). The pipeline does
    NOT crash. Supersedes the pre-P23 sentinel-passthrough behaviour."""
    skill = tmp_path / "skill_chained.md"
    skill.write_text(_TWO_STEP_CANONICAL, encoding="utf-8")
    compiled = compile_skill(skill)
    # step_1 always returns invalid JSON (fails to produce `produced`); step_2
    # would return ok but must never be dispatched with a missing required input.
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
    assert result.error_count >= 2  # step_1 (logic) + step_2 (missing_consumed)
    by_id = {r.section_id: r for r in result.step_results}
    assert "step_1" in by_id and by_id["step_1"].error is not None
    # P23: step_2 fails loud on the missing required consumed input.
    assert "step_2" in by_id
    assert by_id["step_2"].error_class == "missing_consumed"
    assert "produced" in (by_id["step_2"].error or "")
    # It did NOT dispatch a sentinel to the backend (Consume never called).
    assert not any("Consume" in c.user_prompt for c in backend.calls)


# ── P16 (FZ 20k9c1a1a1b7c2g): truncation self-heals by escalating max_tokens ──

class _TruncateUntilBudgetBackend:
    """Returns a truncated response (stop_reason==max_tokens, unparseable body)
    until the request's max_tokens reaches ``succeed_at``, then a valid payload.
    Records the max_tokens of every call so the test can assert escalation."""

    backend_id = "truncate-until-budget"

    def __init__(self, succeed_at: int) -> None:
        self.succeed_at = succeed_at
        self.calls: list[LLMRequest] = []

    def call(self, request: LLMRequest) -> LLMResponse:
        self.calls.append(request)
        mt = request.max_tokens
        if mt is not None and mt >= self.succeed_at:
            return LLMResponse(
                content=json.dumps({"facets": ["ok"]}), elapsed_ms=0.0,
                backend_id=self.backend_id, metadata={"stop_reason": "end_turn"},
            )
        return LLMResponse(
            content='{"facets": ["cut off mid-',  # truncated JSON
            elapsed_ms=0.0, backend_id=self.backend_id,
            metadata={"stop_reason": "max_tokens", "output_tokens": mt},
        )


def test_truncation_escalates_max_tokens_and_converges(compiled, tmp_path: Path) -> None:
    """P16: a truncated response escalates max_tokens (16000→32000) and retries
    on its OWN budget, converging — NOT replaying the same cap through the logic
    path until the 3-strike loop / logic-budget exhaustion."""
    backend = _TruncateUntilBudgetBackend(succeed_at=32000)  # succeeds once escalated once (16000→32000)
    result = execute_step_with_retry(
        compiled.steps[0], leaf={"_id": "leaf_0", "id": "x"}, upstream={},
        backend=backend, vault_root=tmp_path,
    )
    assert result.error is None, f"should converge, got {result.error}"
    # first call inherits the 16000 default, the retry escalates to 32000
    caps = [c.max_tokens for c in backend.calls]
    assert caps[0] in (None, 16000)
    assert 32000 in caps, f"retry must escalate max_tokens; saw {caps}"
    assert "truncated" in result.retry_kind_history
    assert result.retry_kind_history[-1] == "success"


def test_truncation_does_not_burn_logic_budget(compiled, tmp_path: Path) -> None:
    """A step that keeps truncating past the ceiling terminates cleanly as
    `truncated` (its own bounded budget) — it must NOT be a logic-budget
    exhaustion (truncation is capacity, not a prompt defect)."""
    backend = _TruncateUntilBudgetBackend(succeed_at=10**9)  # never enough → always truncates
    result = execute_step_with_retry(
        compiled.steps[0], leaf={"_id": "leaf_0", "id": "x"}, upstream={},
        backend=backend, vault_root=tmp_path,
    )
    assert result.error is not None
    # bounded: 1 initial + MAX_TRUNCATION_RETRIES escalations, then it falls
    # through to the logic path once (which terminates) — never an unbounded loop
    assert result.error_class in ("truncated", "validation")
    assert result.retry_kind_history.count("truncated") == MAX_TRUNCATION_RETRIES
    # escalation is bounded by the ceiling, never unbounded
    assert max(c.max_tokens or 0 for c in backend.calls) <= MAX_TRUNCATION_CEILING_TOKENS


# ── Defaults ───────────────────────────────────────────────────────────────


def test_executor_module_constants_present():
    assert MAX_LOGIC_RETRIES == 3
    assert MAX_CRASH_RECOVERIES == 2
    assert MAX_TRUNCATION_RETRIES == 2
