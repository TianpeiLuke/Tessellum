"""Phase B smoke — watchdog + context budget + progress heartbeat.

v0.0.60 of plan_composer_dks_robustness §B. Covers:

  - Watchdog: stalled backend → step result marked stalled (B.1)
  - Per-step timeout override via sidecar (B.1)
  - Compiler oversized prompt estimate → CompilerError (B.3)
  - Compiler 70% threshold → budget_warnings populated (B.3)
  - Runtime: actual prompt exceeds hard cap → refuses dispatch (B.3)
  - --progress flag emits per-step lines to stderr (B.2)
"""

from __future__ import annotations

import json
import textwrap
import time
from pathlib import Path

import pytest

from tessellum.composer import (
    MockBackend,
    compile_skill,
    execute_step,
    run_pipeline,
)
from tessellum.composer.compiler import (
    DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS,
    HARD_PROMPT_CAP_CHARS,
    WARN_AT_PROMPT_FRACTION,
    CompilerError,
)
from tessellum.composer.executor import DEFAULT_TIMEOUT_SECONDS
from tessellum.composer.llm import LLMRequest, LLMResponse


# ── Watchdog (B.1) ─────────────────────────────────────────────────────────


class _SlowBackend:
    """Mock backend that sleeps before returning. For watchdog tests."""

    backend_id = "slow"

    def __init__(self, sleep_seconds: float, response: str = "{}"):
        self.sleep_seconds = sleep_seconds
        self.response = response
        self.calls: list[LLMRequest] = []

    def call(self, request: LLMRequest) -> LLMResponse:
        self.calls.append(request)
        time.sleep(self.sleep_seconds)
        return LLMResponse(
            content=self.response,
            elapsed_ms=self.sleep_seconds * 1000.0,
            backend_id=self.backend_id,
            metadata={},
        )


_TIMEOUT_CANONICAL = textwrap.dedent(
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
    pipeline_metadata: ./skill_timeout.pipeline.yaml
    ---

    # Timeout

    ## Step 1: do <!-- :: section_id = step_1 :: -->

    Do for {{leaf.id}}.
    """
)


def _make_timeout_skill(tmp_path: Path, timeout_seconds: float | None = None):
    """Helper: write a skill canonical + sidecar with an optional
    per-step timeout_seconds field."""
    skill = tmp_path / "skill_timeout.md"
    skill.write_text(_TIMEOUT_CANONICAL, encoding="utf-8")
    sidecar_lines = [
        'version: "1.0"',
        "pipeline:",
        "  - section_id: step_1",
        "    role: CORE",
        "    aggregation: per_leaf",
        "    batchable: false",
        "    depends_on: []",
        "    materializer: no_op",
        '    prompt_template: "Do."',
        "    output_key: done",
    ]
    if timeout_seconds is not None:
        sidecar_lines.append(f"    timeout_seconds: {timeout_seconds}")
    (tmp_path / "skill_timeout.pipeline.yaml").write_text(
        "\n".join(sidecar_lines) + "\n", encoding="utf-8"
    )
    return compile_skill(skill)


def test_executor_stalls_on_slow_backend(tmp_path: Path):
    """Backend sleeps 2s with 0.5s timeout → StepResult.error contains stall marker."""
    compiled = _make_timeout_skill(tmp_path, timeout_seconds=0.5)
    backend = _SlowBackend(sleep_seconds=2.0)
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is not None
    assert "stalled" in result.error.lower()


def test_executor_default_timeout_does_not_fire_on_fast_call(tmp_path: Path):
    """Default 120s timeout doesn't fire on a fast call."""
    compiled = _make_timeout_skill(tmp_path)  # no per-step timeout → 120s default
    backend = MockBackend(default=json.dumps({"done": True}))
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is None


def test_executor_kwarg_timeout_override(tmp_path: Path):
    """Explicit timeout_seconds= kwarg overrides the step's declared timeout."""
    compiled = _make_timeout_skill(tmp_path, timeout_seconds=60.0)  # step says 60s
    backend = _SlowBackend(sleep_seconds=1.5)
    result = execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "x"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
        timeout_seconds=0.5,  # kwarg overrides → fires
    )
    assert result.error is not None
    assert "stalled" in result.error.lower()


def test_default_timeout_constant_is_120():
    assert DEFAULT_TIMEOUT_SECONDS == 120.0


# ── Compile-time budget (B.3) ──────────────────────────────────────────────


def _make_budget_skill(
    tmp_path: Path,
    step_max_prompt_chars: int | None = None,
    upstream_max_chars: int | None = None,
    n_upstreams: int = 1,
):
    """Helper: write a two-step skill where step_2 depends on step_1.
    step_1's expected_output_schema declares max_chars (the soft cap);
    step_2 consumes step_1's output and optionally has its own
    max_prompt_chars."""
    canonical_lines = [
        "---",
        "tags:",
        "  - resource",
        "  - skill",
        "keywords:",
        "  - a",
        "  - b",
        "  - c",
        "topics:",
        "  - X",
        "  - Y",
        "language: markdown",
        "date of note: 2026-05-11",
        "status: active",
        "building_block: procedure",
        "pipeline_metadata: ./skill_budget.pipeline.yaml",
        "---",
        "",
        "# Budget",
        "",
    ]
    # n upstream "producer" steps + one downstream "consumer"
    for i in range(1, n_upstreams + 1):
        canonical_lines.append(f"## Step {i}: produce_{i} <!-- :: section_id = produce_{i} :: -->")
        canonical_lines.append("")
        canonical_lines.append(f"Produce output {i}.")
        canonical_lines.append("")
    canonical_lines.append(
        f"## Step {n_upstreams + 1}: consume <!-- :: section_id = consume :: -->"
    )
    canonical_lines.append("")
    canonical_lines.append("Consume " + " ".join(f"{{{{upstream.out_{i}}}}}" for i in range(1, n_upstreams + 1)) + ".")
    canonical_lines.append("")
    (tmp_path / "skill_budget.md").write_text("\n".join(canonical_lines), encoding="utf-8")

    sidecar_lines = ['version: "1.0"', "pipeline:"]
    for i in range(1, n_upstreams + 1):
        sidecar_lines.extend(
            [
                f"  - section_id: produce_{i}",
                "    role: CORE",
                "    aggregation: per_leaf",
                "    batchable: false",
                "    depends_on: []",
                "    materializer: no_op",
                f"    prompt_template: \"Produce {i}.\"",
                f"    output_key: out_{i}",
                "    expected_output_schema:",
                "      type: object",
                f"      required: [out_{i}]",
            ]
        )
        if upstream_max_chars is not None:
            sidecar_lines.append(f"      max_chars: {upstream_max_chars}")
    sidecar_lines.extend(
        [
            "  - section_id: consume",
            "    role: CORE",
            "    aggregation: per_leaf",
            "    batchable: false",
            "    depends_on: " + json.dumps([f"produce_{i}" for i in range(1, n_upstreams + 1)]),
            "    materializer: no_op",
            '    prompt_template: "Consume."',
            "    output_key: consumed",
        ]
    )
    if step_max_prompt_chars is not None:
        sidecar_lines.append(f"    max_prompt_chars: {step_max_prompt_chars}")
    (tmp_path / "skill_budget.pipeline.yaml").write_text(
        "\n".join(sidecar_lines) + "\n", encoding="utf-8"
    )
    return tmp_path / "skill_budget.md"


def test_compiler_default_budget_passes(tmp_path: Path):
    """One upstream with default 25K soft cap → consume estimate well under 150K."""
    skill = _make_budget_skill(tmp_path)
    compiled = compile_skill(skill)
    assert compiled.budget_warnings == ()


def test_compiler_oversized_prompt_raises_compiler_error(tmp_path: Path):
    """Many upstreams each with declared large max_chars → estimate > hard cap → raises."""
    # 8 upstreams × 25K = 200K (exceeds 150K hard cap)
    skill = _make_budget_skill(tmp_path, upstream_max_chars=25_000, n_upstreams=8)
    with pytest.raises(CompilerError, match="exceeds hard cap"):
        compile_skill(skill)


def test_compiler_warns_at_70pct_of_cap(tmp_path: Path):
    """5 upstreams × 25K = 125K — 83% of 150K → warning, not error."""
    skill = _make_budget_skill(tmp_path, upstream_max_chars=25_000, n_upstreams=5)
    compiled = compile_skill(skill)
    assert len(compiled.budget_warnings) >= 1
    # Warning text identifies the step
    assert any("consume" in w for w in compiled.budget_warnings)


def test_compiler_per_step_max_prompt_chars_override(tmp_path: Path):
    """A step with explicit smaller max_prompt_chars triggers compile error
    at a lower threshold than the global hard cap."""
    # 1 upstream × 25K = 25K. With max_prompt_chars=20K → error.
    skill = _make_budget_skill(
        tmp_path, upstream_max_chars=25_000, n_upstreams=1, step_max_prompt_chars=20_000
    )
    with pytest.raises(CompilerError, match="exceeds hard cap"):
        compile_skill(skill)


def test_runtime_actual_prompt_exceeds_hard_cap(tmp_path: Path):
    """Even when compile-time estimate is fine, runtime catches an upstream
    that exceeds its declared soft cap.

    Setup: upstream declares max_chars=500 (small soft cap → compile-time
    estimate ~500 chars, well under the step's 1000-char per-step cap).
    Runtime feeds an upstream output that's 5000 chars — exceeds the
    step's 1000-char cap. Runtime guard fires.
    """
    skill = _make_budget_skill(
        tmp_path,
        upstream_max_chars=500,  # small soft cap → compile-time fine
        step_max_prompt_chars=1000,
    )
    compiled = compile_skill(skill)
    # Consume step is at index 1 (steps[0] is produce_1)
    consume_step = compiled.steps[1]
    # Feed an oversized upstream (much larger than the 1000-char per-step cap)
    huge_upstream = "X" * 5000
    backend = MockBackend(default=json.dumps({"consumed": True}))
    result = execute_step(
        consume_step,
        leaf={"_id": "leaf_0"},
        upstream={"out_1": huge_upstream},
        backend=backend,
        vault_root=tmp_path,
    )
    assert result.error is not None
    assert "HARD_PROMPT_CAP_CHARS" in result.error or "cap" in result.error
    # Backend was never called
    assert len(backend.calls) == 0


def test_compiler_budget_constants_present():
    assert HARD_PROMPT_CAP_CHARS == 150_000
    assert WARN_AT_PROMPT_FRACTION == 0.7
    assert DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS == 25_000


# ── Progress heartbeat (B.2) ───────────────────────────────────────────────


def test_progress_flag_emits_per_step_lines(tmp_path: Path, capsys):
    """--progress=True logs to stderr; off → no logging."""
    skill = _make_timeout_skill(tmp_path)
    backend = MockBackend(default=json.dumps({"done": True}))
    run_pipeline(
        skill,
        leaves=[{"_id": "leaf_0", "id": "x"}],
        backend=backend,
        vault_root=tmp_path,
        progress=True,
    )
    captured = capsys.readouterr()
    # Progress lines go to stderr
    assert "step 1/1" in captured.err
    assert "step_1 starting" in captured.err
    assert "step_1 done" in captured.err


def test_progress_off_by_default(tmp_path: Path, capsys):
    skill = _make_timeout_skill(tmp_path)
    backend = MockBackend(default=json.dumps({"done": True}))
    run_pipeline(
        skill,
        leaves=[{"_id": "leaf_0", "id": "x"}],
        backend=backend,
        vault_root=tmp_path,
    )
    captured = capsys.readouterr()
    assert "step 1/1" not in captured.err
