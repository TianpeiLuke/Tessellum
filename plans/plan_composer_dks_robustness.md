---
tags:
  - project
  - plan
  - tessellum
  - composer
  - dks
  - robustness
  - reliability
keywords:
  - composer retry budget
  - retry-aware prompts
  - watchdog stall detection
  - context budget enforcement
  - dks silent-failure observability
  - meshclaw patterns
topics:
  - Composer Runtime
  - Dialectic Knowledge System
  - Reliability Engineering
language: markdown
date of note: 2026-05-11
status: active
building_block: procedure
---

# Plan — Composer + DKS Robustness (v0.0.60)

## Problem

Tessellum's runtime is feature-complete through v0.0.59 (DKS Phase 1-10 shipped, meta-DKS shipped, MCP server shipped, how-to library shipped). But the underlying execution layer — Composer's pipeline scheduler + DKS's per-cycle dispatcher — has structural fragilities that surface only under sustained or adversarial load. They've been tolerable during dogfooding because failures are rare and the user is present to retry manually. Public-beta (v0.1.0) needs them addressed *before* external users hit them.

Four concrete gaps, validated against the actual source code in `src/tessellum/composer/` and `src/tessellum/dks/`:

1. **Composer has zero retry logic.** `scheduler.py:128-140` runs each step exactly once. A failing step yields `StepResult.error != None`, the scheduler skips storing its output in `upstream`, and downstream steps see `<missing upstream.X>` sentinels (`executor.py:188-190`) — cascading failure from a single transient LLM glitch.
2. **No watchdog; blocking `backend.call()` can hang forever.** `executor.py:122` invokes the backend synchronously with no timeout. A network stall or model-side hang halts the entire pipeline silently. The `AnthropicBackend` inherits SDK defaults — typically infinite.
3. **No context budget enforcement.** `compiler.py` validates pipeline structure but never measures rendered prompt size. Oversized prompts surface as opaque API errors at runtime, not compile-time warnings.
4. **DKS silently swallows backend failures.** Three `except Exception: return None` sites in `dks/core.py` (`_llm_check_disagreement`, `_format_retrieval_context`, and JSON parse paths) preserve graceful degradation but emit no signal — a degraded backend's effects show up only as a vague "DKS produces worse outputs."

The patterns to address these are battle-tested in AbuseSlipBox's **MeshClaw** framework (production Task Runner handling multi-day sessions over multi-thousand-leaf corpora). FZ 15 in the AB vault documents the architectural divergence between MeshClaw and OpenClaw; this plan ports the four MeshClaw-specific patterns that close Tessellum's gaps, leaving OpenClaw's distributed-gates patterns for a later release if needed.

## What Tessellum already does better than AB (don't reinvent)

Three patterns are *more* sophisticated in Tessellum than in AB and stay as-is:

| Surface | Tessellum | AB equivalent |
|---|---|---|
| Eval framework | 6-dim LLMJudge rubric (`composer/eval.py` Wave 5b): relevance / completeness / accuracy / clarity / structural_integrity / epistemic_congruence | Single LLM-judge rating |
| Typed-output contracts | Frozen `dataclass(kw_only=True)` + BB-typed subclasses with `field(default=BBType.X, init=False)` (Phase 8 D1) | Structural Python types via TypedDict |
| Schema mutability | Event-sourced meta-DKS — append-only `SchemaEditEvent` log + retract semantics (Phase 9 D3) | Concentrated runtime reliability state in `session.py` |

This plan does *not* touch these surfaces.

## Resolved decisions

| # | Question | Resolution | Rationale |
|---|----------|------------|-----------|
| **R-1** | Retry budgets: separate logic-vs-crash, or single budget? | **Separate** — `MAX_LOGIC_RETRIES = 3` for schema/materializer/validation failures; `MAX_CRASH_RECOVERIES = 2` for backend exceptions (network, OOM, timeout, etc.) | MeshClaw's experience: subprocess flakes shouldn't consume the algorithmic retry budget for actual prompt-vs-schema mismatches. Same-error loop detection (3 consecutive identical errors → fail early) prevents retry storms regardless of budget. |
| **R-2** | Retry context injection: prompt-template variables or system-prompt augmentation? | **Both: template variables `{{retry.attempt}}` and `{{retry.error}}` AND system-prompt augmentation** | The error needs to land in the user-prompt for the model to address; the attempt count is more useful as a system-prompt nudge ("you're on attempt 2"). MeshClaw injects both. |
| **R-3** | Watchdog mechanism: asyncio task with timeout, or thread + signal? | **asyncio task with `asyncio.wait_for`** | The MCP SDK is already async (used by `tessellum.mcp.server`). Going async-first across the executor is a one-time refactor that pays off when the MCP host calls into Composer. Thread + signal is harder to test + portable across OSes. |
| **R-4** | Context budget cap: per-step or global? | **Both: global `HARD_PROMPT_CAP_CHARS = 150_000` + per-upstream `max_chars` in sidecar YAML** | Global cap protects against pipeline composition error (e.g., 5 upstream sources fanning in); per-upstream caps protect against any single source dominating. Sum(soft) ≤ hard validated at compile time. |
| **R-5** | DKS silent-failure observability: change semantics or just instrument? | **Just instrument** — preserve `except: return None` semantics; add a `silent_failures: tuple[str, ...]` field on `DKSCycleResult` that records each swallowed exception | Phase 5's `decide_escalation` contract depends on graceful degradation. Changing the silent-fallback semantics would break confidence-gating in subtle ways. Telemetry is enough. |
| **R-6** | Should watchdog cancel partial work or just mark it stalled? | **Just mark stalled** (set `StepResult.error = "stalled after Xs"`); don't kill the in-flight backend call | Cancelling an in-flight HTTP request doesn't reliably free resources; the backend will eventually return. Best to let it complete in the background while the scheduler moves on, treating the result as already-discarded. |
| **R-7** | Same-error loop detection: by error message, error type, or both? | **By error message hash** (first 200 chars, normalized whitespace) | Error type alone over-fires (every JSON-parse failure shares the type); message text catches the actual pattern. 200 chars covers most error-payload distinctness. |

## What's already shipped (v0.0.59 baseline)

| Surface | Status | Where |
|---|---|---|
| Composer single-shot executor | ✓ — one call per step; no retry | `composer/executor.py:79-161` |
| Composer scheduler (linear; no error recovery) | ✓ — captures errors as data; downstream sees sentinels | `composer/scheduler.py:71-172` |
| Composer compile-time pipeline validation (structure only) | ✓ | `composer/compiler.py` |
| Composer eval framework (Wave 5b) | ✓ shipped earlier — 6-dim LLMJudge + structural assertions | `composer/eval.py` |
| LLM backends (Mock + Anthropic) | ✓ shipped Wave 4 | `composer/llm.py` |
| DKS 7-component cycle | ✓ — silent-failure fallbacks in 3 places | `dks/core.py:892-897, 1054-1056, 1073-1083` |
| DKS retrieval-grounded warrants | ✓ — silent fallback on retrieval failure | `dks/core.py:1054-1056` |
| DKS confidence gating | ✓ — depends on silent-failure semantics | `dks/confidence.py` |
| Meta-DKS event-sourced schema | ✓ shipped v0.0.52+ | `dks/meta/runtime.py` |
| **Composer retry layer** | not implemented | — |
| **Composer watchdog** | not implemented | — |
| **Composer context-budget enforcement** | not implemented | — |
| **DKS silent-failure telemetry** | not implemented | — |

## Phase A — Composer retry layer (~250 LOC + tests)

**Goal:** make a single LLM/materializer failure recoverable. A pipeline stops cascading from one transient glitch.

### A.1 — Retry budgets in the executor

New executor state (per `execute_step` invocation):

- `logic_attempts: int = 0` — incremented on schema-validation failure, materializer error, or `ContractViolation`
- `crash_recoveries: int = 0` — incremented on `backend.call()` raising any `Exception` (caught + wrapped)
- `error_history: list[str]` — most recent 3 error-message hashes for loop detection

New executor kwargs (default preserve today's behaviour):

- `max_logic_retries: int = 3`
- `max_crash_recoveries: int = 2`

Retry decision logic:

```python
def execute_step_with_retry(step, ..., max_logic_retries=3, max_crash_recoveries=2):
    history = []
    logic_attempts = 0
    crash_recoveries = 0
    while True:
        attempt_n = logic_attempts + crash_recoveries + 1
        try:
            result = execute_step_once(step, attempt=attempt_n, last_error=history[-1] if history else None, ...)
        except Exception as e:  # backend crash
            crash_recoveries += 1
            if crash_recoveries > max_crash_recoveries:
                return StepResult(..., error=f"crash budget exhausted: {e}")
            continue
        if result.error is None:
            return result  # success
        # logic failure (schema / materializer / contract)
        err_hash = _hash_error(result.error)
        if len(history) >= 2 and history[-1] == err_hash == history[-2]:
            return result  # same-error loop — fail early
        history.append(err_hash)
        logic_attempts += 1
        if logic_attempts > max_logic_retries:
            return result  # logic budget exhausted
```

Lives in `composer/executor.py`. Public `execute_step` keeps today's signature; new `execute_step_with_retry` wraps it. Scheduler calls `execute_step_with_retry`.

### A.2 — Retry-aware prompt context (Pattern 5)

`composer/executor.py:_resolve_placeholders` gains two more variables:

- `{{retry.attempt}}` — integer (1 on first call)
- `{{retry.error}}` — string (empty on first call; populated with prior failure's normalized error message on retries)

System prompt also gains a one-line prefix on retries:

```
[Retry attempt {N}: prior call failed with: {error_first_120_chars}]
```

Compiler validates that step templates using `{{retry.X}}` placeholders compile cleanly; non-retry-aware steps simply don't reference them.

### A.3 — Tests

- `test_executor_retries_logic_failure_succeeds_on_attempt_2.py` — a failing step that succeeds on retry
- `test_executor_retries_same_error_short_circuits.py` — 3 identical errors → fail before exhausting budget
- `test_executor_crash_recovery_separate_from_logic.py` — backend raises 2× then succeeds; logic budget untouched
- `test_executor_retry_context_substitutes.py` — `{{retry.attempt}}` and `{{retry.error}}` appear in prompt
- `test_scheduler_failed_step_does_not_cascade.py` — after retries exhaust, downstream still runs with documented missing-upstream marker (back-compat)

## Phase B — Composer reliability layer (~250 LOC + tests)

**Goal:** runtime never hangs; oversized prompts never reach the LLM as runtime mysteries.

### B.1 — Watchdog stall detection (Gap 2)

`composer/executor.py` migrates from sync `execute_step` to async `execute_step_async`. Wraps the backend call in `asyncio.wait_for`:

```python
async def execute_step_async(step, ..., timeout_seconds: float | None = None):
    timeout = timeout_seconds or step.timeout_seconds or 120.0  # 2 min default
    try:
        response = await asyncio.wait_for(
            backend.call_async(request),  # backends gain async variant
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        return StepResult(..., error=f"stalled after {timeout}s")
```

Both `MockBackend` and `AnthropicBackend` gain `call_async()` — `MockBackend.call_async` is trivial; `AnthropicBackend.call_async` wraps the Anthropic SDK's async client (which exists in the official SDK).

Sync `execute_step` becomes a `asyncio.run` wrapper around `execute_step_async` for back-compat — existing callers don't need to change.

Sidecar YAML gains optional `timeout_seconds` per step (default 120s; overridable per step for known-slow operations like full-corpus aggregations).

### B.2 — Background heartbeat for long pipelines

For pipelines with > 10 steps or known-long total wall-clock, scheduler emits a per-step start/finish log line to stderr:

```
[15:32:01] composer step 3/12 starting (per_leaf × 25 leaves)
[15:32:47] composer step 3/12 done — 25/25 leaves, 46.2s, 0 errors
```

Off by default; opt-in via `--progress` CLI flag on `tessellum composer run`.

### B.3 — Context budget enforcement (Gap 3)

New constants in `composer/compiler.py`:

```python
HARD_PROMPT_CAP_CHARS = 150_000  # ~50K tokens; Claude Sonnet ceiling-ish
DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS = 25_000
```

Sidecar YAML schema additions:

- Each step: optional `max_prompt_chars: int` (overrides global hard cap)
- Each step's `expected_output_schema`: optional `max_chars: int` (the soft cap when this output feeds a downstream step's `{{upstream.X}}`)

Compile-time validation in `compile_skill`:

- For each step, compute `estimated_max_prompt_chars = sum(upstream_soft_caps) + leaf_metadata_overhead`
- If estimate exceeds `hard_cap` → **error** (compilation fails)
- If estimate exceeds `0.7 × hard_cap` → **warning** (compilation succeeds but logs)

Runtime check in `execute_step` (after placeholder resolution):

- If rendered prompt length > hard cap → return `StepResult(..., error="prompt exceeds HARD_PROMPT_CAP_CHARS")` without dispatching
- This catches cases where an upstream's *actual* output exceeded its declared soft cap

### B.4 — Tests

- `test_executor_stalls_on_slow_backend.py` — backend that sleeps 10s with 1s timeout → `error="stalled"`
- `test_executor_timeout_per_step_override.py` — sidecar `timeout_seconds: 5` honored
- `test_compiler_oversized_prompt_estimate_errors.py` — sum of upstream soft caps > hard cap → compile failure
- `test_compiler_oversized_prompt_warns_at_70pct.py` — warning emitted, compilation succeeds
- `test_executor_actual_prompt_exceeds_hard_cap.py` — runtime check fires; backend not called
- `test_progress_flag_emits_per_step_lines.py` — `--progress` produces expected log shape

## Phase C — DKS silent-failure observability (~80 LOC + tests)

**Goal:** preserve graceful-degradation semantics; surface the rate of silent failures so degraded backends are visible.

### C.1 — Telemetry field on DKSCycleResult

```python
@dataclass(frozen=True)
class DKSCycleResult:
    # ... existing fields ...
    silent_failures: tuple[str, ...] = ()
    """Each entry is a one-line description of a backend call that
    raised an exception inside the cycle but was silently fallen-back
    (per Phase 5's `decide_escalation` contract). Surfaces in cycle
    traces under --runs-dir."""
```

### C.2 — Wire the three swallow sites

Each `except Exception:` site appends to a cycle-local list before the fallback return:

```python
def _llm_check_disagreement(self, ...):
    try:
        response = self.backend.call(...)
        ...
    except Exception as e:
        self._silent_failures.append(f"_llm_check_disagreement: {type(e).__name__}: {e}")
        return None
```

DKSCycle gains a `self._silent_failures: list[str] = []` instance field initialized in `__init__`; the result-construction sites pass `silent_failures=tuple(self._silent_failures)`.

### C.3 — Roll up into MetaObservation

`tessellum.dks.meta.runtime.MetaObservation` already supports the right shape. Add a new field:

```python
silent_failure_count: int = 0
```

`_run_dks_meta` in CLI counts `len(cycle.silent_failures)` across all loaded cycle traces and populates this field. LLMProposer's prompt mentions it: "if `silent_failure_count > 0`, factor degraded-backend likelihood into your proposals."

### C.4 — Tests

- `test_dks_silent_failure_recorded_on_retrieval_exception.py` — retrieval client raises → silent_failures gets one entry
- `test_dks_silent_failure_recorded_on_llm_disagreement_exception.py` — same for the disagreement check
- `test_dks_silent_failures_empty_on_clean_run.py` — successful run has no silent_failures
- `test_meta_observation_silent_failure_count_aggregates.py` — count across traces

## Phase D — Ship v0.0.60 (~50 LOC)

**Goal:** version bump + CHANGELOG + clean-venv wheel smoke + commit + push + PyPI.

- Bump `pyproject.toml` + `src/tessellum/__about__.py` to `0.0.60`
- CHANGELOG entry summarising Phases A-C with the four gap descriptions + the four MeshClaw patterns ported
- Full pytest suite (target: ~920 passed, +30 from v0.0.59's 886)
- Clean-venv wheel smoke covers the new code paths (retry executor, async backend, context-budget compile, silent_failures field)
- Commit + push + PyPI

## Integration points across phases

| Subsystem | A — Retry | B — Reliability | C — Observability | D — Ship |
|-----------|-----------|-----------------|-------------------|----------|
| `tessellum.composer.executor` | A.1 + A.2 retry budget + retry context | B.1 watchdog → async execute_step | — | — |
| `tessellum.composer.scheduler` | A.1 use execute_step_with_retry | B.2 `--progress` heartbeat | — | — |
| `tessellum.composer.compiler` | A.2 retry placeholder validation | B.3 context-budget validation | — | — |
| `tessellum.composer.llm` | — | B.1 backends gain `call_async()` | — | — |
| `tessellum.dks.core` | — | — | C.1 silent_failures field + C.2 swallow-site wiring | — |
| `tessellum.dks.meta.runtime` | — | — | C.3 silent_failure_count in MetaObservation | — |
| `tessellum.cli.composer` | — | B.2 `--progress` flag | — | — |
| sidecar YAML schema | A.2 `{{retry.attempt}}` / `{{retry.error}}` placeholders | B.1 `timeout_seconds`; B.3 `max_prompt_chars` / `max_chars` | — | — |
| `tests/` | A.3 5 new tests | B.4 6 new tests | C.4 4 new tests | — |
| `pyproject.toml` | — | — | — | D.1 bump 0.0.59 → 0.0.60 |
| `__about__.py` | — | — | — | D.1 status update |
| `CHANGELOG.md` | — | — | — | D.1 entry |

## Open questions

| # | Question | Lean |
|---|----------|------|
| **OQ-A** | Should `MAX_LOGIC_RETRIES = 3` be configurable per pipeline via sidecar YAML? | Yes — pipelines that ingest known-noisy sources may want higher; CI smoke tests may want lower for fail-fast. Add `max_logic_retries: int = 3` to sidecar root. |
| **OQ-B** | Watchdog timeout default of 120s — too long? too short? | Empirical question; 120s is a reasonable conservative starting point. Track per-step actual elapsed in traces; tune after the first 100 production runs. |
| **OQ-C** | Should `silent_failures` ever escalate to surfacing a `StepResult.error` instead of being silent? | No for v0.0.60 — preserves Phase 5 semantics. A future version could expose a `--strict-degradation` mode that converts silents to errors for CI dogfooding. |
| **OQ-D** | Async backend refactor (B.1): does it break v0.0.59 callers? | Sync `execute_step` becomes a wrapper around `execute_step_async` via `asyncio.run`; back-compat preserved. Direct callers see identical behaviour; only new tests + the MCP server benefit from async. |
| **OQ-E** | Should context-budget hard cap be model-aware (e.g., 200K for Claude 4 Opus, 150K for Sonnet)? | Defer — start with a single global cap. Per-model caps add complexity for marginal benefit until users hit the wrong-cap-for-model failure mode. |
| **OQ-F** | Should the retry-context error message be sanitised (stack traces stripped)? | Yes — the LLM doesn't need Python stack traces; strip to error class + message. Compiler-level sanitisation in `_hash_error`. |

## What this plan does NOT do

- **No async-everywhere refactor.** Only `executor.py` and the backend layer go async; the scheduler stays largely sync (with one `asyncio.run` wrapper). A full async migration is a v0.2+ concern.
- **No retry of materialization side-effects.** If a step writes a file successfully then a later step fails, the file is not rolled back. Idempotency is the materialiser's responsibility; this plan doesn't add transactional semantics.
- **No OpenClaw pattern port.** OpenClaw's distributed-gates patterns (per-layer reliability ownership) are interesting but a structural redesign — the four MeshClaw patterns here are *additive* + far smaller blast radius. OpenClaw integration would be a v0.2+ plan.
- **No new Composer features beyond robustness.** No batching, no parallel execution, no caching — orthogonal to robustness.
- **No DKS escalation tracking (MeshClaw Pattern 7).** Tessellum's DKS doesn't currently do LLM-driven replan; escalation tracking has no failure mode to prevent. Defer until DKS adds a meta-cycle that proposes its own continuation.
- **No tier-based safe-tool classifier (MeshClaw Pattern 8).** Tessellum doesn't dispatch arbitrary tools the way Claude Code does. Not applicable yet.

## Sequencing summary

```
v0.0.59 ┌─ SHIPPED (Phase V — MCP server + how-to library)
        │
v0.0.60 │   Phase A — Composer retry layer
        │   ├─ A.1 Retry budgets (logic + crash split)
        │   ├─ A.2 Retry-aware prompts ({{retry.attempt}}, {{retry.error}})
        │   └─ A.3 5 new tests
        │
        │   Phase B — Composer reliability layer
        │   ├─ B.1 Watchdog (async executor + per-step timeout)
        │   ├─ B.2 Background heartbeat (--progress flag)
        │   ├─ B.3 Context budget enforcement (compile + runtime)
        │   └─ B.4 6 new tests
        │
        │   Phase C — DKS silent-failure observability
        │   ├─ C.1 silent_failures field on DKSCycleResult
        │   ├─ C.2 Wire the three swallow sites
        │   ├─ C.3 silent_failure_count in MetaObservation
        │   └─ C.4 4 new tests
        │
        │   Phase D — Ship v0.0.60
        │   ├─ D.1 Version bump + CHANGELOG + __about__.py
        │   ├─ D.2 Full suite (~920 passed)
        │   ├─ D.3 Clean-venv wheel smoke
        │   └─ D.4 Commit + push + PyPI
        │
v0.1.0  └─ Phase VI of plan_v01_completion_roadmap.md
            (deferred from immediate-next; robustness first)
```

## Related plans

- `plan_v01_completion_roadmap.md` — Phase V shipped at v0.0.59; Phase VI (v0.1.0 public-beta cut) was the natural-next, but this plan intercepts because robustness should land before the alpha → public-beta transition.
- `plan_dks_expansion.md` — Phase 10 shipped at v0.0.54; DKS Pattern 7 (escalation tracking) is referenced here as deferred.
- `plan_meta_dks_validation_and_polish.md` — Phase B shipped at v0.0.53; the silent-failure telemetry in Phase C feeds the LLMProposer's per-MetaObservation reasoning surface.

## Heritage

This plan ports patterns from AbuseSlipBox's **MeshClaw** framework. Specifically:

- FZ 15 trail's argumentative chain (MeshClaw vs OpenClaw 9-axis divergence map)
- `snippet_meshclaw_circuit_breaker.md` — informs A.1 retry decision logic + R-1 same-error short-circuit
- `snippet_meshclaw_task_retry_recovery.md` — informs A.2 retry-aware prompts
- `snippet_meshclaw_context_budgets.md` — informs B.3 two-tier budget model
- `snippet_meshclaw_task_runner_lifecycle.md` — informs B.1 watchdog cancel-at-Xs escalation

The patterns are well-established in MeshClaw's multi-day production sessions; this plan adapts them to Tessellum's Composer + DKS shape without porting MeshClaw's vault-specific session.py concentration.

---

**Last Updated**: 2026-05-11
**Status**: Active — robustness plan for v0.0.60. Four phases; ~600 LOC total + 15 new tests. Targets the alpha→public-beta transition's main remaining structural risk.
