"""Single-step execution — resolve, dispatch, validate, materialize.

The executor is the unit operation that the scheduler iterates: given a
:class:`CompiledStep` plus a leaf and the upstream context, it:

  1. Resolves placeholders in the step's prompt section text:

     - ``{{leaf.X}}``     — looked up in the per-leaf data dict.
     - ``{{upstream.Y}}`` — looked up in the running upstream context.
     - ``{{retry.attempt}}`` / ``{{retry.error}}`` — substituted on
       retries (see :func:`execute_step_with_retry`).
  2. Wraps :meth:`LLMBackend.call` with a per-step watchdog
     (:data:`DEFAULT_TIMEOUT_SECONDS`, overridable by the inline contract). On
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

import hashlib
import json
import random
import re
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, ContextManager, Literal

import jsonschema

from tessellum.composer.compiler import CompiledStep
from tessellum.composer.context_assembler import ContextAssembler
from tessellum.composer.contracts import ArtifactIntegrityError, ArtifactRef
from tessellum.composer.credential_pool import RunBudget
from tessellum.composer.error_taxonomy import REASON_TO_ERROR_CLASS, classify_reason
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


DEFAULT_TIMEOUT_SECONDS: float = 360.0
"""Default per-step watchdog timeout — DERIVED (R2.3, FZ 20k9c1a1a1b7c2k2a1b)
as the transport read timeout + 60s slack, so the watchdog can never fire
simultaneously with (or before) the transport's own bound: the panel flagged
watchdog=300 == read=300 with zero slack as a coincidental equality acting as
load-bearing structure. runtime/timing.py asserts the ordering.
Raised originally from 120s → 300s: the large-output
generation steps (``write_plan`` emits a full multi-hundred-line plan body,
``dispatch_notes`` a full note body) can legitimately take 2–4 minutes for a
single Bedrock/Anthropic call over a large source, and 120s killed them
mid-generation as a false "stall". Overridable via the step contract's
``timeout_seconds`` field or the :func:`execute_step` /
:func:`execute_step_with_retry` ``timeout_seconds`` kwarg.

Implemented with a daemon worker thread so the caller returns at the
deadline even though the synchronous backend protocol has no portable
cancellation primitive. A late result is discarded.
"""

# ── P16 (FZ 20k9c1a1a1b7c2g): truncation self-heals by escalating max_tokens ──
# A `truncated` result (stop_reason==max_tokens) is an output-SIZE condition, not
# a prompt/schema defect. The retry ladder escalates max_tokens (2× per round,
# capped) on its OWN budget instead of replaying the same cap through the logic
# path (which would re-truncate identically until the 3-strike loop fires).
MAX_TRUNCATION_RETRIES: int = 2
"""Max times a `truncated` step escalates its max_tokens and retries. Separate
from MAX_LOGIC_RETRIES — truncation is capacity, not a logic defect."""

# Issue 13: an empty response signals a transient service window — identical
# errors are the blip's NATURE, so they are exempt from the same-error
# short-circuit and retried on their own bounded budget with forced backoff.
MAX_EMPTY_RETRIES: int = 3

DEFAULT_TRUNCATION_BASE_TOKENS: int = 16000
"""Base to escalate from when a truncating step declared no explicit max_tokens
(the LLMRequest default)."""
MAX_TRUNCATION_CEILING_TOKENS: int = 64000
"""Ceiling for truncation escalation — within the model's output limit; a step
still truncating at this size is a genuine plan-quality problem (split the note),
not a budget one, so it falls through to the normal terminal path."""


ErrorClass = Literal[
    "transient", "validation", "rate_limit", "auth", "crash", "truncated",
    "missing_consumed",
]
"""Phase 1.4 (v4) — fine-grained error class returned by
:func:`classify_error`. Orthogonal to the coarse logic/crash/stall split
that :func:`execute_step_with_retry` uses for budget accounting; this is
the *diagnostic* class surfaced on :attr:`StepResult.error_class`."""


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
        error_class: The fine-grained :func:`classify_error` class of
            ``error`` (``"transient"``, ``"validation"``,
            ``"rate_limit"``, ``"auth"``, or ``"crash"``), or ``None``
            when ``error`` is ``None``. This makes validation-class
            failures distinguishable from transient/infra ones without
            breaking the coarse ``retry_kind_history`` logic/crash
            split. Defaults to ``None`` so existing frozen-dataclass
            consumers are unaffected.
    """

    section_id: str
    leaf_id: str | None
    response: LLMResponse
    materialized: MaterializedOutput
    elapsed_ms: float
    error: str | None = None
    attempts: int = 1
    retry_kind_history: tuple[str, ...] = ("success",)
    error_class: ErrorClass | None = None


def step_result_trace_dict(r: StepResult) -> dict[str, Any]:
    """The trace/telemetry record for one step — DERIVED from ``StepResult`` so
    the trace can't silently desync from the fields the executor computes (P20,
    FZ 20k9c1a1a1b7c2g). Before P20, ``_write_trace`` hand-picked 11 fields and
    dropped exactly the diagnostics the fixes added — ``error_class`` and the
    backend ``response.metadata`` (``stop_reason`` / ``output_tokens`` /
    ``context_warnings``) — so a ~25-min run's most useful signals never reached
    disk. This single builder is the one place the record is shaped; a test
    asserts every diagnostic field is present."""
    return {
        "section_id": r.section_id,
        "leaf_id": r.leaf_id,
        "elapsed_ms": r.elapsed_ms,
        "error": r.error,
        "error_class": r.error_class,  # P20 — was dropped
        "response_chars": len(r.response.content),
        "backend_id": r.response.backend_id,
        # P20 — the backend diagnostics (stop_reason / output_tokens /
        # input_tokens / context_warnings / prompt_exceeded_cap / stalled / …);
        # these were computed and stamped but never serialized.
        "metadata": dict(r.response.metadata),
        "files_written": [str(p) for p in r.materialized.files_written],
        "files_applied": [str(p) for p in r.materialized.files_applied],
        "notes": r.materialized.notes,
        "attempts": r.attempts,
        "retry_kind_history": list(r.retry_kind_history),
    }


_LEAF_PLACEHOLDER_RE = re.compile(r"\{\{\s*leaf\.([a-z0-9_]+)\s*\}\}")
_UPSTREAM_PLACEHOLDER_RE = re.compile(r"\{\{\s*upstream\.([a-z0-9_]+)\s*\}\}")
# Retry-aware placeholders — substituted with the previous attempt's
# response and error when execute_step_with_retry retries.
_RETRY_PLACEHOLDER_RE = re.compile(r"\{\{\s*retry\.([a-z0-9_]+)\s*\}\}")
# Artifact-by-reference placeholders (P21-full; FZ 20k9c1a1a1b7c2j) —
# substituted with the driver's durable artifact store so a step reads a large
# artifact (plan_text, source_excerpt, planned_notes) BY REFERENCE instead of a
# prior step re-emitting it through the LLM. Generalizes P3's {{leaf.plan_text}}.
_ARTIFACT_PLACEHOLDER_RE = re.compile(r"\{\{\s*artifact\.([a-z0-9_]+)\s*\}\}")
# Combined single-pass placeholder regex over all four namespaces. Used by
# _resolve_placeholders so every placeholder in the ORIGINAL template resolves
# exactly once — a token appearing inside a substituted VALUE is never
# re-scanned (no second-order substitution). Group 1 = namespace, group 2 = key.
_PLACEHOLDER_RE = re.compile(
    r"\{\{\s*(leaf|upstream|retry|artifact)\.([a-z0-9_]+)\s*\}\}"
)


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
    max_tokens_override: int | None = None,
    budget: RunBudget | None = None,
    artifacts: dict[str, Any] | None = None,
    context_assembler: ContextAssembler | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
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
        budget: Shared run budget charged immediately before the backend
            call. A refused charge returns ``run budget exhausted`` without
            dispatching.
        artifacts: The driver's durable artifact store (P21-full) —
            ``{{artifact.X}}`` placeholders resolve against it, so a step reads
            a large artifact BY REFERENCE. ``None`` (default) → an empty store,
            byte-identical to the pre-P21 render for a prompt with no
            ``{{artifact.X}}``.

    Returns:
        StepResult.
    """
    start = time.monotonic()

    if cancellation_check is not None and cancellation_check():
        raise InterruptedError("pipeline cancelled before backend dispatch")

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
        artifacts=artifacts,
    )

    # Deliver the output schema to the model. The compiler strips the step's
    # ```yaml``` contract block (which holds `expected_output_schema`) out of
    # the prompt prose (skill_extractor.split_contract_and_prompt), yet the
    # prose says "return the JSON object specified by expected_output_schema".
    # So without this the model is asked to match a schema it was never shown —
    # it invents close-but-wrong enum values and drops required fields, and the
    # response then fails validation. Append the schema (+ required keys) so the
    # model actually sees the contract it must satisfy.
    #
    # ONLY for steps whose materializer consumes JSON. A markdown-body
    # materializer (``body_markdown_frontmatter_to_file``) or an XML one
    # (``edits_apply_xml_tags``) wants the response in THAT format — telling the
    # model "return ONLY JSON" here directly contradicts the step's own "OUTPUT
    # FORMAT — markdown with YAML frontmatter (NOT JSON)" prose and makes the
    # materializer reject the result. Their ``expected_output_schema`` is a
    # loose validation aid (e.g. requires ``output_path``), not a JSON mandate.
    if step.expected_output_schema and _step_consumes_json(step):
        prompt = f"{prompt}\n\n{_render_output_schema_instruction(step.expected_output_schema)}"

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

    # Prompt-size handling. Two modes:
    #
    #   1. context_assembler is None (default): the crude runtime hard cap
    #      — an oversized rendered prompt is a *validation error* that
    #      halts the step. Byte-identical to the pre-assembler behaviour.
    #   2. context_assembler set: fail-soft bounding — the rendered prompt
    #      is passed through the assembler, which truncates/windows it to
    #      its char budget and *warns* rather than erroring. An oversized
    #      source degrades instead of crashing the worker. The
    #      assembler's warnings are captured to surface in the response
    #      metadata for diagnostics.
    from tessellum.composer.compiler import HARD_PROMPT_CAP_CHARS

    effective_max_prompt_chars = (
        step.max_prompt_chars
        if step.max_prompt_chars is not None
        else HARD_PROMPT_CAP_CHARS
    )
    context_warnings: tuple[str, ...] = ()
    if context_assembler is None:
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
                error_class="validation",
            )
    else:
        assembled = context_assembler.assemble(prompt)
        prompt = assembled.text
        context_warnings = assembled.warnings

    # Per-step response budget: a step may declare a larger max_tokens than the
    # global default (the big-output writers — full plan body / augmented plan
    # with coverage map + gate tables + per-note cross-ref contract — exceed
    # 16000 and truncate mid-JSON). ``max_tokens_override`` (P16) takes precedence
    # — the retry ladder escalates it when a prior attempt truncated, so a
    # truncation self-heals instead of replaying the same too-small cap.
    # None on both → inherit the LLMRequest default.
    effective_max_tokens = (
        max_tokens_override if max_tokens_override is not None else step.max_tokens
    )
    request = LLMRequest(
        system_prompt=system_prompt,
        user_prompt=prompt,
        **({"max_tokens": effective_max_tokens} if effective_max_tokens is not None else {}),
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

    if budget is not None and not budget.try_spend(cost=1.0):
        elapsed_ms = (time.monotonic() - start) * 1000.0
        return StepResult(
            section_id=step.section_id,
            leaf_id=leaf.get("_id"),
            response=LLMResponse(
                content="",
                elapsed_ms=0.0,
                backend_id=getattr(backend, "backend_id", ""),
                metadata={"budget_exhausted": True},
            ),
            materialized=MaterializedOutput(
                structured={},
                notes="run budget exhausted",
            ),
            elapsed_ms=elapsed_ms,
            error="run budget exhausted",
            attempts=0,
            retry_kind_history=(),
            error_class="crash",
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
            error_class="transient",
        )

    if cancellation_check is not None and cancellation_check():
        raise InterruptedError("pipeline cancelled before materialization")

    error: str | None = None

    # Issue 13 (FZ 20k9c1a1a1b7c2k1a1b1a): an EMPTY response is a transient
    # service condition (verified non-prompt-deterministic by reproduction —
    # the identical r5 prompt succeeds), NOT a prompt/schema defect. Diagnose
    # it FIRST with the stop_reason attached, so it never masquerades as
    # "response is not valid JSON" and the retry wrapper can ride the blip
    # with backoff instead of same-error short-circuiting inside it.
    if not response.content.strip():
        stop = response.metadata.get("stop_reason")
        return StepResult(
            section_id=step.section_id,
            leaf_id=leaf.get("_id"),
            response=response,
            materialized=MaterializedOutput(
                structured={}, notes=f"empty response (stop_reason={stop})"
            ),
            elapsed_ms=response.elapsed_ms,
            error=f"empty response (stop_reason={stop})",
            error_class="transient",
        )

    # Chat models habitually wrap a JSON/markdown response in an outer
    # ```` ```json … ``` ```` fence, which makes json.loads fail at char 0 and
    # hides the ``---`` frontmatter from the materializer. Strip a single
    # WHOLE-response fence once, here, so both validation and materialization
    # see the clean payload (inner code fences in a note body are untouched).
    parse_content = _strip_outer_code_fence(response.content)

    # P10 (FZ 20k9c1a1a1b7c2g): a response cut off at the token cap is an
    # OUTPUT-SIZE condition, not a logic/prompt defect. The backend records
    # stop_reason in metadata (llm.py); read it here and diagnose truncation
    # FIRST — otherwise the truncated JSON fails json.loads and is misclassified
    # "validation" / "not valid JSON" (the E14/E15 symptom), sending operators to
    # tune the prompt instead of the cap.
    if response.metadata.get("stop_reason") == "max_tokens":
        out_toks = response.metadata.get("output_tokens")
        error = (
            "response truncated at max_tokens"
            + (f" ({out_toks} output tokens)" if out_toks else "")
            + " — raise the step's max_tokens (a big-output writer) or split the output"
        )

    # Schema validation — best effort, and only for JSON-consuming materializers
    # (a markdown/XML materializer's output is not JSON; its own materializer
    # validates the format, so a json.loads schema check would spuriously fail).
    # Skip when truncation already diagnosed the real cause.
    if error is None and step.expected_output_schema and _step_consumes_json(step):
        validation_error = _validate_against_schema(
            parse_content, step.expected_output_schema
        )
        if validation_error:
            error = f"response failed schema validation: {validation_error}"

    # Materialize.
    materializer_key = step.materializer_key or "no_op"
    materialized: MaterializedOutput
    try:
        materialized = materialize(
            materializer_key,
            parse_content,
            vault_root=vault_root,
            dry_run=dry_run,
            effect_guard=effect_guard,
            effect_recorder=effect_recorder,
        )
    except MaterializerError as e:
        # Don't override an earlier schema-validation error message.
        if error is None:
            error = f"materializer failed: {e}"
        else:
            error = f"{error}; materializer failed: {e}"
        materialized = MaterializedOutput(structured={}, notes=f"materializer error: {e}")

    elapsed_ms = (time.monotonic() - start) * 1000.0

    # Surface any context-assembler warnings (oversized/truncated source)
    # in the response metadata for diagnostics, without mutating the
    # backend's frozen response.
    if context_warnings:
        response = LLMResponse(
            content=response.content,
            elapsed_ms=response.elapsed_ms,
            backend_id=response.backend_id,
            metadata={**response.metadata, "context_warnings": list(context_warnings)},
        )

    return StepResult(
        section_id=step.section_id,
        leaf_id=leaf.get("_id"),
        response=response,
        materialized=materialized,
        elapsed_ms=elapsed_ms,
        error=error,
        error_class=classify_error(error) if error is not None else None,
    )


# ── Internals ──────────────────────────────────────────────────────────────


def upstream_placeholder_keys(step: "CompiledStep") -> frozenset[str]:
    """The ``{{upstream.X}}`` keys a step's prompt references (P23,
    FZ 20k9c1a1a1b7c2h/g). Used by the scheduler to detect a MISSING REQUIRED
    consumed input — a producer that errored/emitted nothing leaves its
    ``output_key`` absent from ``upstream``, and the step then renders a
    ``<missing upstream.X>`` sentinel INTO its prompt and produces garbage that
    looks like a model failure. Surfacing it as a first-class
    ``missing_consumed`` error is fail-loud at the contract boundary."""
    text = step.prompt_section_text or ""
    return frozenset(m.group(1) for m in _UPSTREAM_PLACEHOLDER_RE.finditer(text))


def _resolve_placeholders(
    text: str,
    *,
    leaf: dict,
    upstream: dict[str, Any],
    retry_attempt: int = 1,
    retry_last_error: str | None = None,
    artifacts: dict[str, Any] | None = None,
) -> str:
    """Substitute ``{{leaf.X}}``, ``{{upstream.Y}}``, ``{{retry.X}}``, and
    ``{{artifact.X}}`` placeholders.

    Missing leaf/upstream keys leave a clearly-marked sentinel rather
    than silently inserting empty string — easier to debug a malformed
    prompt than a mysteriously-empty LLM output. The ``retry.*``
    placeholders resolve to ``retry_attempt`` (int) and
    ``retry_last_error`` (string, sanitised); unknown ``retry.X``
    keys produce a sentinel.

    ``{{artifact.X}}`` (P21-full; FZ 20k9c1a1a1b7c2j) resolves against the
    driver's durable artifact store — a large artifact read BY REFERENCE
    instead of a prior step re-emitting it. ``artifacts=None`` (the default)
    is treated as an empty store, so a prompt with no ``{{artifact.X}}`` is
    byte-identical to the pre-P21 render (the sub simply matches nothing).

    SINGLE-PASS: all four namespaces resolve in ONE pass over the ORIGINAL
    template (a combined regex), so a placeholder appearing INSIDE a substituted
    value is never re-scanned. This closes a second-order-substitution hazard:
    if a leaf/upstream value (e.g. digested source content) literally contains
    ``{{artifact.X}}`` / ``{{upstream.Y}}``, that token is inserted VERBATIM, not
    recursively expanded (which could inline a whole artifact into a note body).
    """
    if artifacts is None:
        artifacts = {}

    def _sub(m: re.Match) -> str:
        namespace, key = m.group(1), m.group(2)
        if namespace == "leaf":
            return _stringify(leaf[key]) if key in leaf else f"<missing leaf.{key}>"
        if namespace == "upstream":
            return _stringify(upstream[key]) if key in upstream else f"<missing upstream.{key}>"
        if namespace == "retry":
            if key == "attempt":
                return str(retry_attempt)
            if key == "error":
                return "" if retry_last_error is None else _sanitise_error_for_prompt(retry_last_error)
            return f"<missing retry.{key}>"
        if namespace == "artifact":
            if key not in artifacts:
                return f"<missing artifact.{key}>"
            val = artifacts[key]
            # A2 (FZ 20k9c1a1a1b7c2k1a): a durable working-memory artifact
            # derefs by reading its file — integrity-checked, LOUD on
            # mismatch (ArtifactIntegrityError -> step error), and
            # byte-identical to the in-RAM value (the store serialized with
            # this module's own _stringify).
            if isinstance(val, ArtifactRef):
                return val.read_text()
            return _stringify(val)
        return m.group(0)  # pragma: no cover — regex only matches the four above

    return _PLACEHOLDER_RE.sub(_sub, text)


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


# Fallback for steps whose materializer contract is unresolved (contract=None):
# the materializer keys whose response is NOT JSON. Used only when the
# authoritative ``wire_format`` (below) is unavailable. ``None``/unknown key →
# JSON (the ``no_op`` default parses JSON).
_NON_JSON_MATERIALIZERS: frozenset[str] = frozenset({
    "body_markdown_frontmatter_to_file",
    "edits_apply_xml_tags",
})


def _step_consumes_json(step: "CompiledStep") -> bool:
    """True iff the step's response is parsed as JSON — so the JSON-schema
    prompt-injection + json.loads schema validation are appropriate.

    Keys on the AUTHORITATIVE ``materializer_contract.wire_format`` declared in
    :mod:`tessellum.composer.contracts` (``json`` / ``markdown_with_frontmatter``
    / ``xml_tag_list`` / ``none``) — the single source of truth for a step's
    output shape — rather than re-deriving it from materializer names. A
    markdown/XML/none step wants THAT format, so injecting "return ONLY JSON" or
    running ``json.loads`` on it is wrong (that was the E9 defect). Falls back to
    the materializer-key name set only when the contract is unresolved."""
    contract = getattr(step, "materializer_contract", None)
    wf = getattr(contract, "wire_format", None)
    if wf is not None:
        return wf == "json"
    return (step.materializer_key or "no_op") not in _NON_JSON_MATERIALIZERS


def _render_output_schema_instruction(schema: dict) -> str:
    """Render an ``expected_output_schema`` into a prompt instruction block.

    The compiler strips the step's ``​```yaml``` contract block (which carries
    ``expected_output_schema``) out of the prompt, so the model otherwise never
    sees the required keys / enum values it is validated against. This renders
    the schema back into the prompt as an explicit, hard instruction: emit the
    literal JSON Schema plus a plain-language restatement of the required keys,
    so the model matches field names and closed enums exactly (no invented
    variants, no dropped required fields).

    Kept compact and deterministic (sorted keys) — it is appended to every
    schema-bearing step's prompt and counts against the prompt budget.
    """
    lines = [
        "OUTPUT CONTRACT — your response MUST be a single JSON object that "
        "validates against this JSON Schema. Return ONLY the JSON (no prose, "
        "no markdown code fence). Use these EXACT key names and, for any "
        "`enum`, one of the listed literal values verbatim:",
        "```json",
        json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False),
        "```",
    ]
    required = schema.get("required")
    if isinstance(required, list) and required:
        lines.append(
            "REQUIRED top-level keys (all must be present): "
            + ", ".join(str(k) for k in required)
            + "."
        )
    return "\n".join(lines)


_OUTER_FENCE_RE = re.compile(
    r"\A\s*```[^\n`]*\n(?P<body>.*?)\n?```\s*\Z",
    re.DOTALL,
)


def _strip_outer_code_fence(content: str) -> str:
    """Strip a single OUTER markdown code fence wrapping the whole response.

    Chat models (Claude, GPT, …) habitually wrap a JSON or markdown response
    in a ```` ```json … ``` ```` / ```` ```markdown … ``` ```` block, so the raw
    response begins with a backtick and ``json.loads`` fails at char 0, and the
    frontmatter materializer sees a fence instead of ``---``. This removes ONLY
    a fence that wraps the ENTIRE (trimmed) content — a response that is exactly
    one fenced block. It never touches inner fences (a note body's own ```code```
    examples are preserved), because the regex is anchored to the whole string
    and requires the closing fence at the very end.

    Returns the content unchanged when it is not a single wrapping fence.
    """
    m = _OUTER_FENCE_RE.match(content)
    return m.group("body") if m else content


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


# ── Error classification + backoff (Phase 1.4, v4) ──────────────────────────


def classify_error(error_msg: str) -> ErrorClass:
    """Classify a normalized error message into a fine-grained class.

    Pure, deterministic string-heuristic classifier — no LLM, no I/O
    (IDENT-3). Orthogonal to the coarse logic/crash/stall split used for
    retry-budget accounting: it exists so callers can *diagnose* why a
    step failed (e.g. an ``auth`` failure is worth alerting on, a
    ``rate_limit`` one is worth slowing down, a ``validation`` one is a
    logic/prompt defect).

    P18 (FZ 20k9c1a1a1b7c2f): thin projection of the canonical
    :func:`~tessellum.composer.error_taxonomy.classify_reason` — the single
    token-heuristic source the executor, credential pool, and llm auth-retry
    all share, so the three can no longer disagree (a bare ``AccessDenied`` is
    now ``auth`` here, ``auth`` in the pool, and auth for the P1 refresh).
    ``quota`` folds into this class's coarser ``rate_limit``; the unclassified
    reason maps to ``crash``.

    Args:
        error_msg: The error string (typically ``StepResult.error`` or a
            backend exception rendered as ``f"{type}: {msg}"``). ``None``
            or empty is treated as ``crash`` (fail-closed, IDENT-5).

    Returns:
        One of ``"transient"``, ``"validation"``, ``"rate_limit"``,
        ``"auth"``, ``"crash"``, ``"truncated"``, ``"missing_consumed"``.
    """
    return REASON_TO_ERROR_CLASS[classify_reason(error_msg)]  # type: ignore[return-value]


def full_jitter_backoff(
    attempt: int,
    base: float = 0.5,
    cap: float = 30.0,
    rng: random.Random | None = None,
) -> float:
    """Full-jitter exponential backoff delay (thundering-herd guard).

    Returns ``uniform(0, min(cap, base * 2**attempt))`` — the "Full
    Jitter" strategy from the AWS Architecture Blog. Because the delay
    is sampled uniformly from ``[0, ceiling]``, concurrent retriers
    de-correlate rather than all waking at the same exponential instant.

    Pure and deterministic given ``rng`` — inject a seeded
    :class:`random.Random` in tests. ``attempt`` is clamped at ``0`` so
    negative inputs can't invert the ceiling; the exponent is capped so
    ``2**attempt`` can't overflow before ``min(cap, ...)`` clamps it.

    Args:
        attempt: 0-indexed retry attempt (0 → ceiling ``base``, 1 →
            ``2*base``, …). Values ``< 0`` are treated as ``0``.
        base: Base delay in seconds.
        cap: Maximum ceiling in seconds; the sampled delay never
            exceeds this.
        rng: Injectable RNG for determinism; defaults to the module
            :mod:`random`.

    Returns:
        A float in ``[0, min(cap, base * 2**attempt)]``.
    """
    r = rng if rng is not None else random
    safe_attempt = attempt if attempt > 0 else 0
    # Clamp the exponent so base*2**attempt can't overflow for huge
    # attempts before the min() clamp runs (2**exp beyond ~1024 is
    # pointless once cap applies).
    exp = min(safe_attempt, 64)
    ceiling = min(cap, base * (2 ** exp))
    if ceiling <= 0.0:
        return 0.0
    return r.uniform(0.0, ceiling)


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
    backoff: bool = False,
    sleep_fn: Callable[[float], None] = time.sleep,
    backoff_base: float = 0.5,
    backoff_cap: float = 30.0,
    backoff_rng: random.Random | None = None,
    budget: RunBudget | None = None,
    artifacts: dict[str, Any] | None = None,
    context_assembler: ContextAssembler | None = None,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    effect_recorder: Callable[[Path], None] | None = None,
    attempt_recorder: Callable[[dict], None] | None = None,
) -> StepResult:
    """Retry-budgeted wrapper around :func:`execute_step`.

    - **Logic failures** (schema-validation, materializer, contract):
      counted against ``max_logic_retries``.
    - **Crash failures** (backend ``call`` raised any Exception):
      counted against ``max_crash_recoveries``, independent budget.
    - **Same-error loop detection**: 3 consecutive failures sharing
      the same error-message hash → short-circuit before exhausting
      the budget.
    - **Run budget**: every actual backend dispatch is atomically charged;
      refusal returns immediately without consuming a retry slot.

    Each retry injects ``retry_attempt`` (1-indexed) and the previous
    attempt's normalised error message into the step's prompt + system
    prompt (Phase A.2). The wrapper itself never raises; budget
    exhaustion + crash-budget exhaustion both surface as
    ``StepResult.error`` with ``attempts`` reflecting the count and
    ``retry_kind_history`` reflecting the failure-kind sequence.

    Phase 1.4 (v4) — additive, IDENT-4 preserving:

    - ``backoff`` (default ``False``): when ``True``, sleep
      :func:`full_jitter_backoff` seconds via ``sleep_fn`` *between*
      attempts (before each retry, never after the terminal result).
      When ``False`` (the default) **no** ``sleep_fn`` call is made at
      all, so the default behaviour is byte-identical to the pre-1.4
      wrapper.
    - ``sleep_fn`` (default :func:`time.sleep`): injectable sleep so
      tests can record/no-op the backoff without wall-clock delay.
    - ``backoff_base`` / ``backoff_cap`` / ``backoff_rng``: forwarded to
      :func:`full_jitter_backoff`; inject a seeded RNG for determinism.

    The returned :class:`StepResult` additionally carries
    :attr:`~StepResult.error_class` — the :func:`classify_error` class of
    its ``error`` (``None`` on success).

    Args:
        backoff: Opt-in flag to enable inter-attempt sleeping. Default
            ``False`` keeps the serial path byte-identical (IDENT-4).
        sleep_fn: Callable invoked with the backoff delay in seconds.
            Only called when ``backoff`` is ``True``.
        backoff_base: Base delay forwarded to
            :func:`full_jitter_backoff`.
        backoff_cap: Ceiling forwarded to :func:`full_jitter_backoff`.
        backoff_rng: Optional seeded RNG for deterministic jitter.
        budget: Shared run-level budget passed to every backend attempt.
    """
    history: list[str] = []  # error-message hashes, in attempt order
    kind_history: list[str] = []
    logic_attempts = 0
    empty_retries = 0

    def _record(kind: str, result_or_none, err: str | None) -> None:
        # Issue 14 (FZ 20k9c1a1a1b7c2k1a1b1a): per-ATTEMPT episodic capture —
        # the record must be as fine-grained as the control flow that acts on
        # it (the retry ladder decides per attempt; pre-fix it hashed each
        # attempt's evidence then discarded it). Fail-soft: recording must
        # never fail the step.
        if attempt_recorder is None:
            return
        try:
            resp = getattr(result_or_none, "response", None)
            meta = (resp.metadata if resp is not None else {}) or {}
            content = resp.content if resp is not None else ""
            attempt_recorder({
                "section_id": step.section_id,
                "leaf_id": leaf.get("_id"),
                "attempt": len(kind_history),
                "kind": kind,
                "at": time.time(),
                "error": err,
                "response_chars": len(content),
                "content_head": content[:2000],
                "stop_reason": meta.get("stop_reason"),
                "output_tokens": meta.get("output_tokens"),
                "input_tokens": meta.get("input_tokens"),
            })
        except Exception:
            pass
    # P16: escalated response budget for a truncation-retry. None until a
    # `truncated` failure bumps it; then threaded into execute_step so the retry
    # asks for more tokens instead of replaying the same too-small cap.
    truncation_max_tokens: int | None = None
    truncation_retries = 0
    crash_recoveries = 0
    last_error: str | None = None
    # Captured-but-unused on success path; populated on each retry.
    last_response: LLMResponse | None = None
    last_materialized: MaterializedOutput | None = None
    last_elapsed_ms: float = 0.0

    while True:
        attempt_n = len(kind_history) + 1
        # Phase 1.4 (v4) — full-jitter backoff *between* attempts. Only
        # sleeps on a retry (attempt_n > 1) and only when opted in via
        # ``backoff=True``; when off, ``sleep_fn`` is never called so the
        # default path is byte-identical to the pre-1.4 wrapper (IDENT-4).
        if backoff and attempt_n > 1:
            sleep_fn(
                full_jitter_backoff(
                    attempt_n - 1,
                    base=backoff_base,
                    cap=backoff_cap,
                    rng=backoff_rng,
                )
            )
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
                max_tokens_override=truncation_max_tokens,
                budget=budget,
                artifacts=artifacts,
                context_assembler=context_assembler,
                cancellation_check=cancellation_check,
                effect_guard=effect_guard,
                effect_recorder=effect_recorder,
            )
        except InterruptedError:
            raise
        except ArtifactIntegrityError as e:
            # A2 review finding 1+2 (FZ 20k9c1a1a1b7c2k1a): a corrupted
            # durable-artifact read is DETERMINISTIC — retrying re-reads the
            # same bytes — and its message carries hex digests that the P18
            # substring taxonomy could misread as auth/rate_limit, tripping
            # the P17 breaker as a fake credential wall. Terminal on first
            # sight, with an explicitly stamped NON-TRIPPING class.
            err = f"{type(e).__name__}: {e}"
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
                    notes=f"artifact integrity failure: {err}",
                ),
                elapsed_ms=0.0,
                error=f"artifact integrity failure (terminal, not retryable): {err}",
                attempts=attempt_n,
                retry_kind_history=tuple(kind_history),
                error_class="validation",
            )
        except Exception as e:  # noqa: BLE001 — crash path: any backend exception
            # Crash failure (backend.call raised, or some hard executor error).
            crash_recoveries += 1
            kind_history.append("crash")
            err = f"{type(e).__name__}: {e}"
            _record("crash", None, err)
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
                    error_class=classify_error(err),
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
                    error_class=classify_error(err),
                )
            continue

        if result.error == "run budget exhausted":
            return StepResult(
                section_id=result.section_id,
                leaf_id=result.leaf_id,
                response=result.response,
                materialized=result.materialized,
                elapsed_ms=result.elapsed_ms,
                error=result.error,
                attempts=len(kind_history),
                retry_kind_history=tuple(kind_history),
                error_class=result.error_class,
            )

        if result.error is None:
            # Success — record the success attempt and return.
            kind_history.append("success")
            _record("success", result, None)
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
                    error_class=classify_error(err),
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
                    error_class=classify_error(err),
                )
            continue

        # Issue 13 — an EMPTY response rides the blip on its own bounded
        # budget: identical empty errors are the transient window's nature, so
        # they are EXEMPT from the same-error short-circuit (which killed r5
        # inside a blip in seconds), and backoff is FORCED even when the
        # wrapper's backoff flag is off — waiting is the only correct move.
        if (
            result.error
            and result.error.startswith("empty response")
            and empty_retries < MAX_EMPTY_RETRIES
        ):
            empty_retries += 1
            kind_history.append("empty")
            _record("empty", result, result.error)
            last_error = result.error
            last_response = result.response
            last_materialized = result.materialized
            last_elapsed_ms = result.elapsed_ms
            sleep_fn(
                full_jitter_backoff(
                    empty_retries,
                    base=max(backoff_base, 1.0),
                    cap=backoff_cap,
                    rng=backoff_rng,
                )
            )
            continue

        # P16 — TRUNCATION is an output-SIZE condition, not a logic/prompt
        # defect: retrying with the same cap just re-truncates identically. So a
        # `truncated` result escalates max_tokens (2×, capped) and retries on its
        # OWN budget (MAX_TRUNCATION_RETRIES) — NOT the logic budget, which is for
        # prompt/schema defects. When the ceiling is hit, fall through to the
        # normal logic path so it terminates cleanly rather than looping.
        if result.error_class == "truncated" and truncation_retries < MAX_TRUNCATION_RETRIES:
            truncation_retries += 1
            kind_history.append("truncated")
            _record("truncated", result, result.error)
            last_error = result.error
            last_response = result.response
            last_materialized = result.materialized
            last_elapsed_ms = result.elapsed_ms
            current = truncation_max_tokens or step.max_tokens or DEFAULT_TRUNCATION_BASE_TOKENS
            truncation_max_tokens = min(current * 2, MAX_TRUNCATION_CEILING_TOKENS)
            continue

        # Logic failure (schema / materializer / contract).
        logic_attempts += 1
        kind_history.append("logic")
        _record("logic", result, result.error)
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
                error_class=classify_error(err),
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
                error_class=classify_error(err),
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
    eventual result is discarded. The daemon worker thread does not
    keep the process alive.
    """
    responses: list[LLMResponse] = []
    errors: list[BaseException] = []
    finished = threading.Event()

    def _invoke() -> None:
        try:
            responses.append(backend.call(request))
        except BaseException as exc:  # re-raised on the calling thread
            errors.append(exc)
        finally:
            finished.set()

    thread = threading.Thread(
        target=_invoke,
        name="composer-watchdog",
        daemon=True,
    )
    thread.start()
    if not finished.wait(timeout_seconds):
        return None
    if errors:
        raise errors[0]
    return responses[0]


__all__ = [
    "StepResult",
    "ErrorClass",
    "ExecutorError",
    "MAX_LOGIC_RETRIES",
    "MAX_CRASH_RECOVERIES",
    "execute_step",
    "execute_step_with_retry",
    "classify_error",
    "full_jitter_backoff",
]
