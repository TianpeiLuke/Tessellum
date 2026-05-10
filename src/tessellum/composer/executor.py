"""Single-step execution — resolve, dispatch, validate, materialize.

The executor is the unit operation that the scheduler iterates: given a
``CompiledStep`` plus a leaf and the upstream context, it:

  1. Resolves placeholders in the step's prompt section text:
     - ``{{leaf.X}}``   — looked up in the per-leaf data dict
     - ``{{upstream.Y}}`` — looked up in the running upstream context
       (Wave 3 minimum; ``{{existing.Z}}`` for APPLY-mode pre-fetch is
       deferred to a later milestone — the materializer enforces APPLY
       file existence at write time instead).
  2. Builds an ``LLMRequest`` and invokes the configured backend.
  3. Validates the response against ``expected_output_schema`` if set
     (best-effort: JSON parse + jsonschema; failures surface as
     ``StepResult.error`` rather than raising — one bad step doesn't
     kill the pipeline).
  4. Hands the response off to the materializer for the step's
     materializer key. Materializer errors also surface on
     ``StepResult.error``.

Returns a ``StepResult`` carrying the response, the materialized output,
timing, and any error.
"""

from __future__ import annotations

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


@dataclass(frozen=True)
class StepResult:
    """One step's execution outcome.

    Attributes:
        section_id: Which step ran.
        leaf_id: Identifier of the leaf for ``per_leaf`` steps; ``None``
            for ``corpus_wide`` and ``cross_leaf`` (Wave 3 collapses
            cross_leaf into corpus_wide).
        response: The raw LLM response.
        materialized: The materialized output. ``MaterializedOutput()``
            (empty) if materialization failed; ``error`` will be set.
        elapsed_ms: Wall-clock from request build through materialization.
        error: ``None`` on success; a string describing the failure
            otherwise. Soft errors (schema validation drift, materializer
            failures) populate this without raising.
    """

    section_id: str
    leaf_id: str | None
    response: LLMResponse
    materialized: MaterializedOutput
    elapsed_ms: float
    error: str | None = None


_LEAF_PLACEHOLDER_RE = re.compile(r"\{\{\s*leaf\.([a-z0-9_]+)\s*\}\}")
_UPSTREAM_PLACEHOLDER_RE = re.compile(r"\{\{\s*upstream\.([a-z0-9_]+)\s*\}\}")


def execute_step(
    step: CompiledStep,
    *,
    leaf: dict,
    upstream: dict[str, Any],
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
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
        backend: An :class:`LLMBackend` (Mock for testing; real for
            production once Wave 4 ships).
        vault_root: Root for materializer file paths.
        dry_run: Skip filesystem writes; structured payloads still flow.

    Returns:
        StepResult.
    """
    start = time.monotonic()

    if step.prompt_section_text is None:
        raise ExecutorError(
            f"step {step.section_id!r} has no prompt_section_text — was it compiled?"
        )

    prompt = _resolve_placeholders(
        step.prompt_section_text, leaf=leaf, upstream=upstream
    )

    request = LLMRequest(
        system_prompt=f"Tessellum step: {step.section_id}",
        user_prompt=prompt,
    )
    response = backend.call(request)

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
) -> str:
    """Substitute ``{{leaf.X}}`` and ``{{upstream.Y}}`` placeholders.

    Missing keys leave a clearly-marked sentinel rather than silently
    inserting empty string — easier to debug a malformed prompt than
    a mysteriously-empty LLM output.
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

    text = _LEAF_PLACEHOLDER_RE.sub(leaf_sub, text)
    text = _UPSTREAM_PLACEHOLDER_RE.sub(upstream_sub, text)
    return text


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


__all__ = ["StepResult", "ExecutorError", "execute_step"]
