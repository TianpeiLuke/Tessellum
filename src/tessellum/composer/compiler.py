"""Composer Wave 2 — compile a skill+sidecar pair into a typed DAG.

Zero LLM calls. The compiler is pure logic:

    1. Load the skill canonical + sidecar (Wave 1a infrastructure).
    2. Validate contract integrity — every materializer key resolves
       in :data:`tessellum.composer.contracts.MATERIALIZER_CONTRACTS`,
       and every CORE/DEFERRED step's ``expected_output_schema``
       declares the materializer's ``required_output_fields``.
    3. Topologically sort by ``depends_on``.
    4. Detect cycles + forward references (a step's ``depends_on`` must
       reference a section_id defined earlier in the pipeline list).
    5. Extract each step's prompt-section text from the canonical.
    6. Return :class:`CompiledPipeline` (or raise on drift).

The output is a typed Python object plus a JSON-serializable form
(``to_dag_json``) for ``tessellum composer compile`` to write to disk.

What this Wave does NOT cover (deferred):

    - Plan-doc + leaves (multi-skill, per-leaf step instantiation).
      Wave 2 compiles a single skill into a "pipeline template"; Wave 3
      executes against concrete data.
    - APPLY-mode pre-fetching of ``applies_to_files``. Requires
      indexer-query resolution; surfaces in Wave 3.
    - LLMBackendContract / MCPContract validation. Backends + MCPs
      ship in Wave 4; the compiler will gain those checks then.
    - ``ContractViolation`` for ``apply_mode_directive_required``
      prompt-text checks. Possible at compile time but minor; defer.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tessellum.composer.contracts import (
    MATERIALIZER_CONTRACTS,
    ContractViolation,
    MaterializerContract,
)
from tessellum.composer.loader import (
    Pipeline,
    PipelineStep,
    load_pipeline,
)
from tessellum.composer.skill_extractor import (
    SkillExtractionError,
    load_skill_section,
)


class CompilerError(Exception):
    """DAG-level errors that aren't contract violations.

    Used for cycle detection, forward-reference violations, and missing
    skill-section text. Contract drift (unknown materializer key,
    missing required output field, etc.) raises ``ContractViolation``
    instead — the caller can ``except (CompilerError, ContractViolation)``
    to catch all compile-time failures.
    """


# ── Context-budget constants (Phase B.3, v0.0.60) ───────────────────────────


HARD_PROMPT_CAP_CHARS: int = 150_000
"""Global per-step cap on the rendered user-prompt size.

~50K tokens; Claude Sonnet 4.6's ceiling-ish without context-overflow.
Each step's rendered prompt (after `{{leaf.X}}` / `{{upstream.Y}}` /
`{{retry.X}}` substitution) is checked against this cap at runtime;
the compiler validates the *upper-bound estimate* against it at
compile time. Override per-step via the sidecar's `max_prompt_chars`
field.

Per plan_composer_dks_robustness R-4: a global cap protects against
pipeline composition error (e.g., 5 upstream sources fanning in);
per-upstream `max_chars` (declared on each step's
`expected_output_schema`) protects against any single source
dominating. Compile-time validation enforces sum(soft) ≤ hard.
"""


WARN_AT_PROMPT_FRACTION: float = 0.7
"""Phase B.3 (v0.0.60). When the estimated prompt size at compile
time exceeds 70% of the hard cap, emit a warning. Caller decides
what to do with warnings (CI: treat as error; dev: log)."""


DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS: int = 25_000
"""Phase B.3 (v0.0.60). Default soft cap per upstream output when
the sidecar's `expected_output_schema.max_chars` is not declared.
Picked so 5 upstreams comfortably fit under HARD_PROMPT_CAP_CHARS
with budget for leaf metadata + prompt boilerplate."""


@dataclass(frozen=True)
class CompiledStep:
    """One step in a compiled pipeline.

    Attributes:
        section_id: Anchor id matching the canonical's H2 marker.
        role: ``"CORE"`` | ``"DEFERRED"`` | ``"INFRA"``.
        aggregation: ``"per_leaf"`` | ``"cross_leaf"`` | ``"corpus_wide"``.
        batchable: Whether the scheduler may batch per_leaf instances.
        depends_on: Tuple of section_ids this step depends on. After
            compilation, this is a tuple in topological order: every
            entry refers to a step that appears EARLIER in the
            pipeline's ``steps`` list.
        materializer_key: Materializer registry key, or ``None`` if
            the step has no materializer (rare; INFRA steps may omit).
        materializer_contract: Resolved contract instance for
            ``materializer_key``, or ``None`` if no key was specified.
        expected_output_schema: JSON Schema the agent's response must
            conform to. ``None`` for INFRA steps.
        prompt_section_text: Body text of the step's section from the
            skill canonical, or ``None`` if section extraction failed
            (caught upstream and surfaced as ``CompilerError``).
        output_key: Identifier for downstream ``{{upstream.X}}``
            placeholder resolution.
        timeout_seconds: Phase B.1 (v0.0.60). Optional per-step
            watchdog timeout. ``None`` → use the executor's default
            (typically 120s). When the backend call exceeds this
            value, the step result is marked
            ``error="stalled after Xs"`` and the scheduler proceeds.
            Per R-6, the in-flight call is not cancelled — it
            completes in the background; its eventual result is
            discarded.
        max_prompt_chars: Phase B.3 (v0.0.60). Optional per-step
            hard cap on the rendered user-prompt size. ``None`` →
            use ``compiler.HARD_PROMPT_CAP_CHARS``. Runtime check:
            if the rendered prompt exceeds this, ``execute_step``
            refuses to dispatch and surfaces a structured error
            rather than the LLM-side mystery failure.
    """

    section_id: str
    role: str
    aggregation: str
    batchable: bool
    depends_on: tuple[str, ...]
    materializer_key: str | None
    materializer_contract: MaterializerContract | None
    expected_output_schema: dict[str, Any] | None
    prompt_section_text: str | None
    output_key: str | None
    timeout_seconds: float | None = None
    max_prompt_chars: int | None = None


@dataclass(frozen=True)
class CompiledPipeline:
    """A skill+sidecar pair compiled to a typed DAG.

    Attributes:
        skill_path: Source canonical path.
        skill_name: Filename stem (e.g. ``"skill_tessellum_search_notes"``).
        pipeline_version: Sidecar's ``version`` field.
        steps: Steps in topological order. ``steps[i].depends_on`` only
            references section_ids in ``steps[:i]``.
        compiled_at: ISO-8601 timestamp of when ``compile_skill`` ran.
        step_count: ``len(steps)`` — convenience for serialization.
        budget_warnings: Phase B.3 (v0.0.60). List of compile-time
            warnings about prompt-size estimates that exceed
            :data:`WARN_AT_PROMPT_FRACTION` (70%) of the hard cap.
            Each entry is a one-line description. Empty when no
            warnings; the compiler does not fail on warnings.
    """

    skill_path: Path
    skill_name: str
    pipeline_version: str
    steps: tuple[CompiledStep, ...]
    compiled_at: str = field(default_factory=lambda: dt.datetime.now(dt.UTC).isoformat())
    budget_warnings: tuple[str, ...] = ()

    @property
    def step_count(self) -> int:
        return len(self.steps)


# ── Public entry points ────────────────────────────────────────────────────


def compile_skill(skill_path: Path | str) -> CompiledPipeline:
    """Compile a skill+sidecar pair into a typed DAG.

    Args:
        skill_path: Path to a skill canonical (``vault/resources/skills/skill_*.md``).
            Must declare ``pipeline_metadata: ./<skill>.pipeline.yaml`` in
            its frontmatter; the sidecar must exist and be schema-valid.

    Returns:
        CompiledPipeline with steps in topological order.

    Raises:
        ContractViolation: An individual step's contract declarations
            don't match its materializer (unknown key, missing required
            output field, etc.).
        CompilerError: DAG-level errors — cycles, forward references,
            missing prompt-section text.
        PipelineValidationError: Upstream Wave 1a errors — sidecar
            missing, schema invalid, orphan section_id.
    """
    skill = Path(skill_path)
    pipeline = load_pipeline(skill)

    if pipeline is None:
        # ``pipeline_metadata: none`` — skill has no Composer dispatch.
        return CompiledPipeline(
            skill_path=skill,
            skill_name=skill.stem,
            pipeline_version="1.0",
            steps=(),
        )

    sorted_steps = _topological_sort(pipeline)
    compiled_steps: list[CompiledStep] = []
    for step in sorted_steps:
        compiled_steps.append(_compile_step(step, skill))

    # Phase B.3 (v0.0.60) — compile-time context-budget validation.
    budget_warnings = _validate_context_budgets(compiled_steps)

    return CompiledPipeline(
        skill_path=skill,
        skill_name=skill.stem,
        pipeline_version=pipeline.version,
        steps=tuple(compiled_steps),
        budget_warnings=tuple(budget_warnings),
    )


def _validate_context_budgets(steps: list[CompiledStep]) -> list[str]:
    """Phase B.3 (v0.0.60). Estimate per-step prompt size from upstream
    soft caps + raise ``CompilerError`` on hard-cap overflow + emit
    warnings at WARN_AT_PROMPT_FRACTION.

    Estimation model (per R-4):

      estimated_prompt_chars(step)
          = sum(upstream_soft_cap_for(dep) for dep in step.depends_on)
          + len(step.prompt_section_text)  # boilerplate + leaf-placeholder text

    Soft cap per upstream: from the producer step's
    ``expected_output_schema.max_chars`` if declared, else
    DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS.

    Hard cap: step.max_prompt_chars if set, else HARD_PROMPT_CAP_CHARS.

    Raises CompilerError when an estimate exceeds the hard cap.
    Returns the list of warning strings (estimate > 70% of hard cap).
    """
    warnings: list[str] = []
    soft_cap_by_section: dict[str, int] = {}
    for s in steps:
        soft_cap = DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS
        if s.expected_output_schema and isinstance(
            s.expected_output_schema.get("max_chars"), int
        ):
            soft_cap = int(s.expected_output_schema["max_chars"])
        soft_cap_by_section[s.section_id] = soft_cap

    for step in steps:
        hard = (
            step.max_prompt_chars
            if step.max_prompt_chars is not None
            else HARD_PROMPT_CAP_CHARS
        )
        upstream_total = sum(
            soft_cap_by_section.get(dep, DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS)
            for dep in step.depends_on
        )
        prompt_text_len = len(step.prompt_section_text or "")
        estimated = upstream_total + prompt_text_len

        if estimated > hard:
            raise CompilerError(
                f"step {step.section_id!r}: estimated prompt size "
                f"({estimated} chars: {upstream_total} upstream + "
                f"{prompt_text_len} prompt-text) exceeds hard cap "
                f"({hard}). Reduce upstream max_chars declarations or "
                f"set a larger max_prompt_chars on this step."
            )
        if estimated > hard * WARN_AT_PROMPT_FRACTION:
            warnings.append(
                f"step {step.section_id!r}: estimated prompt size "
                f"{estimated} chars is {estimated / hard:.0%} of cap "
                f"({hard}); consider tightening upstream max_chars or "
                f"declaring an explicit per-step max_prompt_chars."
            )

    return warnings


def to_dag_json(
    pipeline: CompiledPipeline,
    *,
    include_prompts: bool = True,
) -> dict[str, Any]:
    """Serialize a compiled pipeline to a JSON-friendly dict.

    Args:
        pipeline: The compiled pipeline.
        include_prompts: If False, omit ``prompt_section_text`` fields
            (compact output for log/audit pipelines that don't need
            full prompt content).

    Returns:
        A nested dict suitable for ``json.dumps(..., indent=2)``.
        Schema is stable within v0.x but may change at v0.1.0+.
    """
    return {
        "format_version": "1.0",
        "skill_path": str(pipeline.skill_path),
        "skill_name": pipeline.skill_name,
        "pipeline_version": pipeline.pipeline_version,
        "compiled_at": pipeline.compiled_at,
        "step_count": pipeline.step_count,
        "steps": [_step_to_dict(s, include_prompts) for s in pipeline.steps],
    }


# ── Internals ──────────────────────────────────────────────────────────────


def _topological_sort(pipeline: Pipeline) -> list[PipelineStep]:
    """Topologically sort the pipeline's steps by ``depends_on`` edges.

    Detects cycles and forward references. Forward references are
    treated as errors — the schema declares ``Forward references not
    allowed`` because they almost always indicate author confusion
    about step ordering.
    """
    steps_by_id = {step.section_id: step for step in pipeline.pipeline}
    if len(steps_by_id) != len(pipeline.pipeline):
        # Duplicate section_ids — shouldn't happen if schema validation
        # ran upstream, but surface it explicitly for clarity.
        seen: set[str] = set()
        for step in pipeline.pipeline:
            if step.section_id in seen:
                raise CompilerError(
                    f"duplicate section_id {step.section_id!r} in pipeline"
                )
            seen.add(step.section_id)

    # Validate depends_on references.
    for step in pipeline.pipeline:
        for dep in step.depends_on:
            if dep not in steps_by_id:
                raise CompilerError(
                    f"step {step.section_id!r} depends_on {dep!r}, but no step "
                    f"with that section_id is declared in the pipeline"
                )

    # Forward-reference check — depends_on must reference a section_id
    # that appears EARLIER in the pipeline list.
    seen_so_far: set[str] = set()
    for step in pipeline.pipeline:
        for dep in step.depends_on:
            if dep not in seen_so_far:
                raise CompilerError(
                    f"step {step.section_id!r} has forward reference: "
                    f"depends_on={dep!r} appears later in the pipeline list. "
                    f"Reorder steps so each step's dependencies are listed first."
                )
        seen_so_far.add(step.section_id)

    # Cycle detection via DFS — depths track recursion stack.
    visited: set[str] = set()
    on_stack: set[str] = set()

    def dfs(node: str) -> None:
        if node in on_stack:
            raise CompilerError(
                f"cycle detected in pipeline DAG involving step {node!r}"
            )
        if node in visited:
            return
        on_stack.add(node)
        for dep in steps_by_id[node].depends_on:
            dfs(dep)
        on_stack.remove(node)
        visited.add(node)

    for step in pipeline.pipeline:
        dfs(step.section_id)

    # The pipeline list itself is already topologically sorted (we
    # enforced no forward refs above). Return it as-is.
    return list(pipeline.pipeline)


def _compile_step(step: PipelineStep, skill_path: Path) -> CompiledStep:
    """Compile a single PipelineStep — resolves contract, extracts prompt text."""
    materializer_contract: MaterializerContract | None = None
    if step.materializer is not None:
        if step.materializer not in MATERIALIZER_CONTRACTS:
            raise ContractViolation(
                step_id=step.section_id,
                kind=ContractViolation.KIND_UNKNOWN_MATERIALIZER,
                message=(
                    f"materializer {step.materializer!r} is not registered. "
                    f"Known: {sorted(MATERIALIZER_CONTRACTS)}"
                ),
                suggested_fix=(
                    f"Use one of {sorted(MATERIALIZER_CONTRACTS)} or define a "
                    f"new MaterializerContract subclass and register it."
                ),
            )
        materializer_contract = MATERIALIZER_CONTRACTS[step.materializer]

        # Verify expected_output_schema's `required` includes the
        # materializer's required_output_fields. CORE / DEFERRED only —
        # INFRA's no_op contract has empty required fields.
        if (
            materializer_contract.required_output_fields
            and step.role in ("CORE", "DEFERRED")
        ):
            schema = step.expected_output_schema or {}
            schema_required = set(schema.get("required") or [])
            missing = set(materializer_contract.required_output_fields) - schema_required
            if missing:
                raise ContractViolation(
                    step_id=step.section_id,
                    kind=ContractViolation.KIND_MISSING_REQUIRED_OUTPUT_FIELD,
                    message=(
                        f"materializer {step.materializer!r} requires the "
                        f"agent to emit fields {sorted(missing)}, but "
                        f"step's expected_output_schema.required is "
                        f"{sorted(schema_required) or 'unset'}."
                    ),
                    suggested_fix=(
                        f"Add {sorted(missing)} to expected_output_schema.required."
                    ),
                )

    # Extract the prompt-section text from the canonical.
    try:
        prompt_text = load_skill_section(skill_path, step.section_id)
    except SkillExtractionError as e:
        raise CompilerError(
            f"step {step.section_id!r}: cannot extract prompt section from "
            f"{skill_path}: {e}"
        ) from e

    return CompiledStep(
        section_id=step.section_id,
        role=step.role,
        aggregation=step.aggregation,
        batchable=step.batchable,
        depends_on=tuple(step.depends_on),
        materializer_key=step.materializer,
        materializer_contract=materializer_contract,
        expected_output_schema=step.expected_output_schema,
        prompt_section_text=prompt_text,
        output_key=step.output_key,
        timeout_seconds=step.timeout_seconds,
        max_prompt_chars=step.max_prompt_chars,
    )


def _step_to_dict(step: CompiledStep, include_prompts: bool) -> dict[str, Any]:
    """Serialize a CompiledStep to a JSON-friendly dict."""
    materializer_block: dict[str, Any] | None = None
    if step.materializer_contract is not None:
        materializer_block = {
            "key": step.materializer_key,
            "wire_format": step.materializer_contract.wire_format,
            "operation_verb": step.materializer_contract.operation_verb,
            "required_output_fields": list(
                step.materializer_contract.required_output_fields
            ),
            "requires_tool_free_backend": step.materializer_contract.requires_tool_free_backend,
            "requires_existing_files": step.materializer_contract.requires_existing_files,
            "apply_mode_directive_required": step.materializer_contract.apply_mode_directive_required,
        }

    record: dict[str, Any] = {
        "section_id": step.section_id,
        "role": step.role,
        "aggregation": step.aggregation,
        "batchable": step.batchable,
        "depends_on": list(step.depends_on),
        "materializer": materializer_block,
        "expected_output_schema": step.expected_output_schema,
        "output_key": step.output_key,
    }
    if include_prompts:
        record["prompt_section_text"] = step.prompt_section_text
    else:
        record["prompt_section_text_chars"] = (
            len(step.prompt_section_text) if step.prompt_section_text else 0
        )
    return record


__all__ = [
    "CompiledPipeline",
    "CompiledStep",
    "CompilerError",
    "compile_skill",
    "to_dag_json",
]
