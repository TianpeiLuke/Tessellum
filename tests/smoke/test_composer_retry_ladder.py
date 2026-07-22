"""Phase 1.4 smoke — error-class + full-jitter retry ladder.

Composer v4 §1.4. Covers, additively over the existing retry machinery:

  - classify_error maps each normalized-error shape to the right class
    (transient / validation / rate_limit / auth / crash).
  - full_jitter_backoff stays bounded in [0, min(cap, base*2**n)] with a
    seeded rng, and is deterministic given that rng.
  - execute_step_with_retry(backoff=True, sleep_fn=recorder) sleeps the
    jittered delay BETWEEN attempts and returns the same terminal result
    as the no-backoff path.
  - Default behaviour (backoff=False) makes ZERO sleep calls — the serial
    path is byte-identical to the pre-1.4 wrapper (IDENT-4).
  - The returned StepResult surfaces error_class alongside error.
"""

from __future__ import annotations

import json
import random
import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    StepResult,
    classify_error,
    compile_skill,
    execute_step_with_retry,
    full_jitter_backoff,
)
from tessellum.composer.llm import LLMRequest, LLMResponse


# ── classify_error ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "error_msg, expected",
    [
        # transient — watchdog stall marker
        ("stalled after 120.0s", "transient"),
        ("STALLED AFTER 5s", "transient"),
        # validation — schema / materializer / contract / bad JSON
        ("response failed schema validation: 'facets' is required", "validation"),
        ("materializer failed: no such key", "validation"),
        ("contract violation: missing field", "validation"),
        ("response is not valid JSON: Expecting value", "validation"),
        # rate_limit — 429 / rate limit / quota / throttle
        ("HTTP 429 Too Many Requests", "rate_limit"),
        ("rate limit exceeded, retry later", "rate_limit"),
        ("monthly quota exhausted", "rate_limit"),
        ("request was throttled by the backend", "rate_limit"),
        ("Too Many Requests", "rate_limit"),
        # auth — 401 / 403 / auth / login / expired / credential
        ("401 Unauthorized", "auth"),
        ("403 Forbidden", "auth"),
        ("authentication token expired, please login again", "auth"),
        ("invalid credential", "auth"),
        # crash — anything else, plus empty/None fall-through
        ("RuntimeError: connection reset by peer", "crash"),
        ("some unexpected explosion", "crash"),
        ("", "crash"),
    ],
)
def test_classify_error_maps_each_class(error_msg: str, expected: str) -> None:
    assert classify_error(error_msg) == expected


def test_classify_error_none_is_crash() -> None:
    # Fail-closed (IDENT-5): a falsy message never mis-classifies as clean.
    assert classify_error(None) == "crash"  # type: ignore[arg-type]


def test_classify_error_precedence_stall_beats_others() -> None:
    # 'stalled after' takes precedence even if the tail mentions other tokens.
    assert classify_error("stalled after 30s (429 upstream)") == "transient"


# ── full_jitter_backoff ─────────────────────────────────────────────────────


def test_full_jitter_backoff_bounded_with_seeded_rng() -> None:
    rng = random.Random(1234)
    for attempt in range(0, 15):
        val = full_jitter_backoff(attempt, base=0.5, cap=30.0, rng=rng)
        ceiling = min(30.0, 0.5 * 2 ** attempt)
        assert 0.0 <= val <= ceiling, (attempt, val, ceiling)


def test_full_jitter_backoff_deterministic_given_rng() -> None:
    seq_a = [
        full_jitter_backoff(n, rng=random.Random(7)) for n in range(5)
    ]
    seq_b = [
        full_jitter_backoff(n, rng=random.Random(7)) for n in range(5)
    ]
    assert seq_a == seq_b


def test_full_jitter_backoff_negative_attempt_is_nonnegative() -> None:
    # Negative attempts clamp to 0 rather than inverting the ceiling.
    val = full_jitter_backoff(-3, base=0.5, cap=30.0, rng=random.Random(0))
    assert 0.0 <= val <= 0.5


def test_full_jitter_backoff_respects_cap() -> None:
    rng = random.Random(99)
    # Huge attempt — ceiling must clamp to cap, not overflow.
    val = full_jitter_backoff(50, base=0.5, cap=2.0, rng=rng)
    assert 0.0 <= val <= 2.0


# ── execute_step_with_retry backoff wiring ──────────────────────────────────


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
    date of note: 2026-07-22
    status: active
    building_block: procedure
    pipeline_metadata: ./skill_ladder.pipeline.yaml
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
    skill = tmp_path / "skill_ladder.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_ladder.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return compile_skill(skill)


class _SequenceBackend:
    """Returns scripted responses in order (mirrors test_composer_retry)."""

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
        content = (
            self.responses[min(self._attempt - 1, len(self.responses) - 1)]
            if self.responses
            else "{}"
        )
        return LLMResponse(
            content=content,
            elapsed_ms=0.0,
            backend_id=self.backend_id,
            metadata={"attempt": self._attempt},
        )


def _recording_sleep():
    calls: list[float] = []

    def sleep_fn(seconds: float) -> None:
        calls.append(seconds)

    return sleep_fn, calls


def test_backoff_true_sleeps_jittered_values_between_attempts(
    compiled, tmp_path: Path
) -> None:
    """First call fails schema validation, second succeeds. With backoff=True
    the wrapper sleeps exactly once (before attempt 2) with a value bounded by
    the full-jitter ceiling for retry #1."""
    backend = _SequenceBackend(
        responses=["{}", json.dumps({"facets": ["a", "b"]})]
    )
    sleep_fn, sleeps = _recording_sleep()
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
        backoff=True,
        sleep_fn=sleep_fn,
        backoff_base=0.5,
        backoff_cap=30.0,
        backoff_rng=random.Random(2024),
    )
    assert result.error is None
    assert result.attempts == 2
    assert result.retry_kind_history == ("logic", "success")
    # One retry → exactly one sleep, before attempt 2 (retry index 1).
    assert len(sleeps) == 1
    ceiling = min(30.0, 0.5 * 2 ** 1)
    assert 0.0 <= sleeps[0] <= ceiling


def test_backoff_true_same_terminal_result_as_no_backoff(
    compiled, tmp_path: Path
) -> None:
    """backoff=True must not change the terminal result versus the default
    path — only add sleeps. Same-error loop short-circuits at attempt 3 in
    both cases."""
    common = dict(
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        vault_root=tmp_path,
    )
    base_backend = _SequenceBackend(responses=["{}"] * 10)
    base = execute_step_with_retry(compiled.steps[0], backend=base_backend, **common)

    sleep_fn, sleeps = _recording_sleep()
    boff_backend = _SequenceBackend(responses=["{}"] * 10)
    boff = execute_step_with_retry(
        compiled.steps[0],
        backend=boff_backend,
        backoff=True,
        sleep_fn=sleep_fn,
        backoff_rng=random.Random(1),
        **common,
    )
    # Terminal outcome identical.
    assert base.error == boff.error
    assert base.attempts == boff.attempts == 3
    assert base.retry_kind_history == boff.retry_kind_history
    # backoff slept once per retry (attempts 2 and 3 → 2 sleeps).
    assert len(sleeps) == 2
    assert all(s >= 0.0 for s in sleeps)


def test_default_backoff_false_makes_zero_sleep_calls(
    compiled, tmp_path: Path
) -> None:
    """IDENT-4: with backoff at its default (False), sleep_fn is NEVER called
    even across multiple retries — byte-identical to the pre-1.4 path."""
    sleep_fn, sleeps = _recording_sleep()
    backend = _SequenceBackend(responses=["{}"] * 10)
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
        sleep_fn=sleep_fn,  # provided, but backoff defaults to False
    )
    assert result.error is not None
    assert result.attempts == 3  # same-error short-circuit
    assert sleeps == []  # ZERO sleeps


def test_error_class_surfaced_on_step_result(compiled, tmp_path: Path) -> None:
    """A schema-validation failure that exhausts into a short-circuit carries
    error_class == 'validation'; a clean run carries error_class is None."""
    # Failing run → validation class.
    failing = _SequenceBackend(responses=["{}"] * 10)
    res_fail = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=failing,
        vault_root=tmp_path,
    )
    assert res_fail.error is not None
    assert res_fail.error_class == "validation"

    # Clean run → no error, no error_class.
    ok = _SequenceBackend(responses=[json.dumps({"facets": ["a"]})])
    res_ok = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=ok,
        vault_root=tmp_path,
    )
    assert res_ok.error is None
    assert res_ok.error_class is None


def test_error_class_crash_on_backend_exception(compiled, tmp_path: Path) -> None:
    """When the backend raises every call, the terminal result's error_class
    reflects the crash-class diagnosis."""
    backend = _SequenceBackend(
        responses=["x"] * 10, raise_on_attempts=list(range(1, 11))
    )
    result = execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is not None
    assert result.error_class == "crash"
    assert isinstance(result, StepResult)
