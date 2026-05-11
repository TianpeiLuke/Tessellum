"""Single-step execution — resolve, dispatch, validate, materialize.

The executor is the unit operation that the scheduler iterates: given a
:class:`CompiledStep` plus a leaf and the upstream context, it:

  1. Resolves placeholders in the step's prompt section text:

     - ``{{leaf.X}}``     — looked up in the per-leaf data dict.
     - ``{{upstream.Y}}`` — looked up in the running upstream context.
     - ``{{retry.attempt}}`` / ``{{retry.error}}`` — substituted on
       retries (see :func:`execute_step_with_retry`).
  2. Wraps :meth:`LLMBackend.call` with a per-step watchdog
     (:data:`DEFAULT_TIMEOUT_SECONDS`, overridable per sidecar). On
     timeout, returns a stalled :class:`StepResult` without cancelling
     the in-flight call.
  3. Enforces the rendered-prompt size cap
     (:data:`tessellum.composer.compiler.HARD_PROMPT_CAP_CHARS`,
     overridable per step). Refuses to dispatch oversized prompts and
     surfaces a structured error.
  4. Validates the response against ``expected_output_schema`` if set
     (best-effort: JSON parse + jsonschema; failures surface as
     :attr:`StepResult.error` rather than raising — one bad step
     doesn't kill the pipeline).
  5. Hands the response off to the materializer for the step's
     materializer key. Materializer errors also surface on
     :attr:`StepResult.error`.

Returns a :class:`StepResult` carrying the response, the materialized
output, timing, and any error.

:func:`execute_step_with_retry` wraps :func:`execute_step` with
separate logic and crash retry budgets + same-error loop detection.
The scheduler calls the retry variant by default.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema

from tessellum.composer.compiler import CompiledStep
from tessellum.composer.llm import LLMBackend, LLMRequest, LLMResponse
from tessellum.composer.materializer import (
    MaterializedOutput,
    MaterializerError,
    materialize,
)


class ExecutorError(Exception):
    """Raised on hard executor failures — missing prompt text, etc."""


# ── Retry budgets ──────────────────────────────────────────────────────────


MAX_LOGIC_RETRIES: int = 3
"""Default cap on retries for *logic* failures (schema-validation,
materializer errors, contract violations). Each retry burns one slot
from this budget.

Separate from crash recoveries so subprocess flakes don't consume the
algorithmic retry budget."""


MAX_CRASH_RECOVERIES: int = 2
"""Default cap on retries for *crash* failures (backend.call raising
any Exception — network errors, timeouts, OOMs, etc.). Independent
budget from MAX_LOGIC_RETRIES so a flaky network can't starve the
algorithmic retry slots."""


_ERROR_HASH_PREFIX_LEN: int = 200
"""Hash the first 200 chars of the normalized error message to detect
same-error loops. 200 chars is enough to distinguish most error-payload
shapes without overfitting to a specific line/column hint."""


DEFAULT_TIMEOUT_SECONDS: float = 120.0
"""Default per-step watchdog timeout. Overridable via the sidecar's
``timeout_seconds`` field or the :func:`execute_step` /
:func:`execute_step_with_retry` ``timeout_seconds`` kwarg.

Implemented via ``concurrent.futures.ThreadPoolExecutor`` +
``Future.result(timeout=N)`` rather than asyncio: thread-based
timeout is simpler (no backend refactor required), portable (works
under any Python), and achieves the same outcome — when the wait
expires we mark the step stalled without trying to cancel the
in-flight call (it completes in the background; its result is
discarded).
"""


@dataclass(frozen=True)
class StepResult:
    """One step's execution outcome.

    Attributes:
        section_id: Which step ran.
        leaf_id: Identifier of the leaf for ``per_leaf`` steps; ``None``
            for ``corpus_wide`` and ``cross_leaf`` aggregations.
        response: The raw LLM response.
        materialized: The materialized output. ``MaterializedOutput()``
            (empty) if materialization failed; ``error`` will be set.
        elapsed_ms: Wall-clock from request build through materialization.
        error: ``None`` on success; a string describing the failure
            otherwise. Soft errors (schema validation drift, materializer
            failures) populate this without raising.
        attempts: Number of attempts that ran for this step. ``1`` for
            first-call success; ``>1`` when
            :func:`execute_step_with_retry` retried before either
            succeeding or exhausting its budgets.
        retry_kind_history: Per-attempt failure kind. Each entry is one
            of ``"logic"`` (schema / materializer / contract error),
            ``"crash"`` (backend raised), or ``"success"`` (the attempt
            that produced the returned response). The final entry is
            always ``"success"`` on a returned-clean result, or the
            last failure kind on budget-exhausted results.
    """

    section_id: str
    leaf_id: str | None
    response: LLMResponse
    materialized: MaterializedOutput
    elapsed_ms: float
    error: str | None = None
    attempts: int = 1
    retry_kind_history: tuple[str, ...] = ("success",)


_LEAF_PLACEHOLDER_RE = re.compile(r"\{\{\s*leaf\.([a-z0-9_]+)\s*\}\}")
_UPSTREAM_PLACEHOLDER_RE = re.compile(r"\{\{\s*upstream\.([a-z0-9_]+)\s*\}\}")
# Retry-aware placeholders — substituted with the previous attempt's
# response and error when execute_step_with_retry retries.
_RETRY_PLACEHOLDER_RE = re.compile(r"\{\{\s*retry\.([a-z0-9_]+)\s*\}\}")


def execute_step(
    step: CompiledStep,
    *,
    leaf: dict,
    upstream: dict[str, Any],
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    retry_attempt: int = 1,
    retry_last_error: str | None = None,
    timeout_seconds: float | None = None,
) -> StepResult:
    """Run one step against one leaf with one upstream context.

    Args:
        step: The compiled step (output of
            :func:`tessellum.composer.compile_skill`).
        leaf: Per-leaf data dict — ``{{leaf.X}}`` placeholders look up
            ``X`` here. Should include an ``"_id"`` key (the scheduler
            assigns one if absent).
        upstream: Map of ``output_key`` → structured outputs from
            previously-run steps. ``{{upstream.Y}}`` placeholders look
            up ``Y`` here.
        backend: An :class:`LLMBackend` (mock for tests; real
            backends for production runs).
        vault_root: Root for materializer file paths.
        dry_run: Skip filesystem writes; structured payloads still flow.
        retry_attempt: Attempt number (1 on first call; ≥2 on retries
            from :func:`execute_step_with_retry`). Substituted into
            ``{{retry.attempt}}`` placeholders and prefixed onto the
            system prompt when ≥2.
        retry_last_error: The previous attempt's normalized error
            message (None on first call). Substituted into
            ``{{retry.error}}`` placeholders and included in the
            system-prompt prefix when ≥2.
        timeout_seconds: Per-call watchdog timeout. ``None`` → use
            ``step.timeout_seconds`` if set, else
            :data:`DEFAULT_TIMEOUT_SECONDS`. When the backend call
            exceeds the timeout, the call is *not* cancelled — the
            executor returns a stalled StepResult and the thread
            continues in the background.

    Returns:
        StepResult.
    """
    start = time.monotonic()

    if step.prompt_section_text is None:
        raise ExecutorError(
            f"step {step.section_id!r} has no prompt_section_text — was it compiled?"
        )

    prompt = _resolve_placeholders(
        step.prompt_section_text,
        leaf=leaf,
        upstream=upstream,
        retry_attempt=retry_attempt,
        retry_last_error=retry_last_error,
    )

    # Augment the system prompt on retries so the model sees both the
    # behavioural nudge ("you're on attempt N") and the prior failure
    # context.
    system_prompt = f"Tessellum step: {step.section_id}"
    if retry_attempt > 1 and retry_last_error:
        sanitised = _sanitise_error_for_prompt(retry_last_error)
        system_prompt = (
            f"[Retry attempt {retry_attempt}: prior call failed with: "
            f"{sanitised}]\n{system_prompt}"
        )

    # Runtime hard cap on rendered prompt size. The compiler should
    # have caught oversized prompts at compile time, but actual
    # upstream outputs may exceed their declared max_chars; this is
    # the runtime safety net.
    from tessellum.composer.compiler import HARD_PROMPT_CAP_CHARS

    effective_max_prompt_chars = (
        step.max_prompt_chars
        if step.max_prompt_chars is not None
        else HARD_PROMPT_CAP_CHARS
    )
    if len(prompt) > effective_max_prompt_chars:
        elapsed_ms = (time.monotonic() - start) * 1000.0
        return StepResult(
            section_id=step.section_id,
            leaf_id=leaf.get("_id"),
            response=LLMResponse(
                content="",
                elapsed_ms=0.0,
                backend_id=getattr(backend, "backend_id", ""),
                metadata={"prompt_exceeded_cap": True},
            ),
            materialized=MaterializedOutput(
                structured={},
                notes=f"prompt exceeded hard cap ({len(prompt)} chars > {effective_max_prompt_chars})",
            ),
            elapsed_ms=elapsed_ms,
            error=(
                f"prompt exceeded HARD_PROMPT_CAP_CHARS: rendered "
                f"{len(prompt)} chars > cap {effective_max_prompt_chars}"
            ),
        )

    request = LLMRequest(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    # Watchdog. Wrap backend.call in a thread with a timeout. If the
    # timeout fires, we return a stalled StepResult but don't try to
    # cancel the in-flight call — it continues in the background and
    # its eventual result is discarded.
    effective_timeout = (
        timeout_seconds
        if timeout_seconds is not None
        else (step.timeout_seconds if step.timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS)
    )

    response = _call_backend_with_timeout(backend, request, effective_timeout)
    if response is None:
        # Timeout fired.
        elapsed_ms = (time.monotonic() - start) * 1000.0
        return StepResult(
            section_id=step.section_id,
            leaf_id=leaf.get("_id"),
            response=LLMResponse(
                content="",
                elapsed_ms=elapsed_ms,
                backend_id=getattr(backend, "backend_id", ""),
                metadata={"stalled": True, "timeout_seconds": effective_timeout},
            ),
            materialized=MaterializedOutput(
                structured={},
                notes=f"stalled after {effective_timeout}s",
            ),
            elapsed_ms=elapsed_ms,
            error=f"stalled after {effective_timeout}s",
        )

    error: str | None = None

    # Schema validation — best effort.
    if step.expected_output_schema:
        validation_error = _validate_against_schema(
            response.content, step.expected_output_schema
        )
        if validation_error:
            error = f"response failed schema validation: {validation_error}"

    # Materialize.
    materializer_key = step.materializer_key or "no_op"
    materialized: MaterializedOutput
    try:
        materialized = materialize(
            materializer_key,
            response.content,
            vault_root=vault_root,
            dry_run=dry_run,
        )
    except MaterializerError as e:
        # Don't override an earlier schema-validation error message.
        if error is None:
            error = f"materializer failed: {e}"
        else:
            error = f"{error}; materializer failed: {e}"
        materialized = MaterializedOutput(structured={}, notes=f"materializer error: {e}")

    elapsed_ms = (time.monotonic() - start) * 1000.0

    return StepResult(
        section_id=step.section_id,
        leaf_id=leaf.get("_id"),
        response=response,
        materialized=materialized,
        elapsed_ms=elapsed_ms,
        error=error,
    )


# ── Internals ──────────────────────────────────────────────────────────────


def _resolve_placeholders(
    text: str,
    *,
    leaf: dict,
    upstream: dict[str, Any],
    retry_attempt: int = 1,
    retry_last_error: str | None = None,
) -> str:
    """Substitute ``{{leaf.X}}``, ``{{upstream.Y}}``, and
    ``{{retry.X}}`` placeholders.

    Missing leaf/upstream keys leave a clearly-marked sentinel rather
    than silently inserting empty string — easier to debug a malformed
    prompt than a mysteriously-empty LLM output. The ``retry.*``
    placeholders resolve to ``retry_attempt`` (int) and
    ``retry_last_error`` (string, sanitised); unknown ``retry.X``
    keys produce a sentinel.
    """

    def leaf_sub(m: re.Match) -> str:
        key = m.group(1)
        if key in leaf:
            return _stringify(leaf[key])
        return f"<missing leaf.{key}>"

    def upstream_sub(m: re.Match) -> str:
        key = m.group(1)
        if key in upstream:
            return _stringify(upstream[key])
        return f"<missing upstream.{key}>"

    def retry_sub(m: re.Match) -> str:
        key = m.group(1)
        if key == "attempt":
            return str(retry_attempt)
        if key == "error":
            if retry_last_error is None:
                return ""
            return _sanitise_error_for_prompt(retry_last_error)
        return f"<missing retry.{key}>"

    text = _LEAF_PLACEHOLDER_RE.sub(leaf_sub, text)
    text = _UPSTREAM_PLACEHOLDER_RE.sub(upstream_sub, text)
    text = _RETRY_PLACEHOLDER_RE.sub(retry_sub, text)
    return text


def _sanitise_error_for_prompt(error_message: str) -> str:
    """Per plan R-7 + OQ-F: sanitise an error message for LLM-prompt
    inclusion.

    - Collapse Python stack-trace lines (keep error type + message only)
    - Normalise whitespace (single spaces, no trailing newlines)
    - Cap at 200 chars so the system prompt doesn't balloon

    The LLM doesn't benefit from full tracebacks; class + message
    carries enough signal to guide the retry.
    """
    # Drop lines that look like stack frames ('  File "...", line N, in ...')
    lines = [
        line
        for line in error_message.splitlines()
        if not line.startswith(("  File ", "    File "))
    ]
    flat = " ".join(line.strip() for line in lines if line.strip())
    if len(flat) > _ERROR_HASH_PREFIX_LEN:
        flat = flat[: _ERROR_HASH_PREFIX_LEN] + "..."
    return flat


def _hash_error(error_message: str) -> str:
    """Per R-7: hash the first 200 chars of the sanitised error message
    for same-error loop detection.

    Used by :func:`execute_step_with_retry` to short-circuit when 3
    consecutive failures share the same error pattern.
    """
    sanitised = _sanitise_error_for_prompt(error_message)
    return hashlib.sha256(sanitised.encode("utf-8")).hexdigest()[:16]


def _stringify(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False)
    return str(value)


def _validate_against_schema(content: str, schema: dict) -> str | None:
    """Returns an error string if validation fails, ``None`` if it passes."""
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        return f"response is not valid JSON: {e}"
    try:
        jsonschema.validate(instance=parsed, schema=schema)
    except jsonschema.ValidationError as e:
        return str(e.message)
    return None


def execute_step_with_retry(
    step: CompiledStep,
    *,
    leaf: dict,
    upstream: dict[str, Any],
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    max_logic_retries: int = MAX_LOGIC_RETRIES,
    max_crash_recoveries: int = MAX_CRASH_RECOVERIES,
) -> StepResult:
    """Retry-budgeted wrapper around :func:`execute_step`.

    - **Logic failures** (schema-validation, materializer, contract):
      counted against ``max_logic_retries``.
    - **Crash failures** (backend ``call`` raised any Exception):
      counted against ``max_crash_recoveries``, independent budget.
    - **Same-error loop detection**: 3 consecutive failures sharing
      the same error-message hash → short-circuit before exhausting
      the budget.

    Each retry injects ``retry_attempt`` (1-indexed) and the previous
    attempt's normalised error message into the step's prompt + system
    prompt (Phase A.2). The wrapper itself never raises; budget
    exhaustion + crash-budget exhaustion both surface as
    ``StepResult.error`` with ``attempts`` reflecting the count and
    ``retry_kind_history`` reflecting the failure-kind sequence.
    """
    history: list[str] = []  # error-message hashes, in attempt order
    kind_history: list[str] = []
    logic_attempts = 0
    crash_recoveries = 0
    last_error: str | None = None
    # Captured-but-unused on success path; populated on each retry.
    last_response: LLMResponse | None = None
    last_materialized: MaterializedOutput | None = None
    last_elapsed_ms: float = 0.0

    while True:
        attempt_n = len(kind_history) + 1
        try:
            result = execute_step(
                step,
                leaf=leaf,
                upstream=upstream,
                backend=backend,
                vault_root=vault_root,
                dry_run=dry_run,
                retry_attempt=attempt_n,
                retry_last_error=last_error,
            )
        except Exception as e:  # noqa: BLE001 — crash path: any backend exception
            # Crash failure (backend.call raised, or some hard executor error).
            crash_recoveries += 1
            kind_history.append("crash")
            err = f"{type(e).__name__}: {e}"
            history.append(_hash_error(err))
            last_error = err
            if crash_recoveries > max_crash_recoveries:
                # Budget exhausted; surface as a clean result.
                return StepResult(
                    section_id=step.section_id,
                    leaf_id=leaf.get("_id"),
                    response=LLMResponse(
                        content="",
                        elapsed_ms=0.0,
                        backend_id=getattr(backend, "backend_id", ""),
                        metadata={"crashed": True, "error": err},
                    ),
                    materialized=MaterializedOutput(
                        structured={},
                        notes=f"crash budget exhausted: {err}",
                    ),
                    elapsed_ms=0.0,
                    error=f"crash budget exhausted ({crash_recoveries - 1} retries): {err}",
                    attempts=attempt_n,
                    retry_kind_history=tuple(kind_history),
                )
            # Same-error short-circuit on crashes too (R-7)
            if _same_error_loop_fires(history):
                return StepResult(
                    section_id=step.section_id,
                    leaf_id=leaf.get("_id"),
                    response=LLMResponse(
                        content="",
                        elapsed_ms=0.0,
                        backend_id=getattr(backend, "backend_id", ""),
                        metadata={"crashed": True, "error": err},
                    ),
                    materialized=MaterializedOutput(
                        structured={},
                        notes=f"same-error loop: {err}",
                    ),
                    elapsed_ms=0.0,
                    error=f"same-error loop short-circuit (crash): {err}",
                    attempts=attempt_n,
                    retry_kind_history=tuple(kind_history),
                )
            continue

        if result.error is None:
            # Success — record the success attempt and return.
            kind_history.append("success")
            return StepResult(
                section_id=result.section_id,
                leaf_id=result.leaf_id,
                response=result.response,
                materialized=result.materialized,
                elapsed_ms=result.elapsed_ms,
                error=None,
                attempts=attempt_n,
                retry_kind_history=tuple(kind_history),
            )

        # Stall results are crash-class failures (infrastructure-level),
        # not logic failures. Detect by the error-prefix marker that
        # execute_step uses.
        is_stall = result.error.startswith("stalled after")
        if is_stall:
            crash_recoveries += 1
            kind_history.append("crash")
            err = result.error
            history.append(_hash_error(err))
            last_error = err
            if crash_recoveries > max_crash_recoveries:
                return StepResult(
                    section_id=result.section_id,
                    leaf_id=result.leaf_id,
                    response=result.response,
                    materialized=result.materialized,
                    elapsed_ms=result.elapsed_ms,
                    error=(
                        f"crash budget exhausted ({crash_recoveries - 1} retries, "
                        f"stalls): {err}"
                    ),
                    attempts=attempt_n,
                    retry_kind_history=tuple(kind_history),
                )
            if _same_error_loop_fires(history):
                return StepResult(
                    section_id=result.section_id,
                    leaf_id=result.leaf_id,
                    response=result.response,
                    materialized=result.materialized,
                    elapsed_ms=result.elapsed_ms,
                    error=f"same-error loop short-circuit (stall): {err}",
                    attempts=attempt_n,
                    retry_kind_history=tuple(kind_history),
                )
            continue

        # Logic failure (schema / materializer / contract).
        logic_attempts += 1
        kind_history.append("logic")
        err = result.error
        history.append(_hash_error(err))
        last_error = err
        last_response = result.response
        last_materialized = result.materialized
        last_elapsed_ms = result.elapsed_ms

        if _same_error_loop_fires(history):
            return StepResult(
                section_id=result.section_id,
                leaf_id=result.leaf_id,
                response=last_response,
                materialized=last_materialized,
                elapsed_ms=last_elapsed_ms,
                error=f"same-error loop short-circuit (logic): {err}",
                attempts=attempt_n,
                retry_kind_history=tuple(kind_history),
            )

        if logic_attempts > max_logic_retries:
            return StepResult(
                section_id=result.section_id,
                leaf_id=result.leaf_id,
                response=last_response,
                materialized=last_materialized,
                elapsed_ms=last_elapsed_ms,
                error=(
                    f"logic budget exhausted ({logic_attempts - 1} retries): "
                    f"{err}"
                ),
                attempts=attempt_n,
                retry_kind_history=tuple(kind_history),
            )
        # else: loop back for another attempt


def _same_error_loop_fires(history: list[str]) -> bool:
    """Per R-7: 3 consecutive identical error-message hashes → loop."""
    return len(history) >= 3 and history[-1] == history[-2] == history[-3]


def _call_backend_with_timeout(
    backend: LLMBackend, request: LLMRequest, timeout_seconds: float
) -> LLMResponse | None:
    """Run ``backend.call(request)`` with a timeout.

    Returns the :class:`LLMResponse` on success, or ``None`` if the
    call exceeded ``timeout_seconds``. The thread is not killed on
    timeout — it runs to completion in the background, but its
    eventual result is discarded. The ThreadPoolExecutor's daemon
    threads exit with the process.
    """
    # max_workers=1 because we want this call to be serial per
    # invocation; the scheduler handles parallelism at the leaf level.
    # The pool is local so the threads don't accumulate across calls.
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="composer-watchdog"
    ) as pool:
        future = pool.submit(backend.call, request)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            return None
        # Other exceptions propagate up — the retry layer handles them
        # as crash failures.


__all__ = [
    "StepResult",
    "ExecutorError",
    "MAX_LOGIC_RETRIES",
    "MAX_CRASH_RECOVERIES",
    "execute_step",
    "execute_step_with_retry",
]
