"""Compile a single-file skill canonical into a typed DAG.

Zero LLM calls. The compiler is pure logic:

    1. Load inline step contracts from the skill canonical.
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

Out of scope (handled elsewhere or deliberately omitted):

    - Multi-skill plan-doc instantiation — the compiler produces one
      pipeline template; the scheduler executes against concrete leaves.
    - APPLY-mode pre-fetching of ``applies_to_files`` — the
      materializer reads existing files at write time when needed.
    - ``LLMBackendContract`` validation (``requires_tool_free_backend`` /
      argv overflow) — the backend is unknown at compile time; these are
      enforced at dispatch, not here.

Since P9 (FZ 20k9c1a1a1b7c2e) the compiler DOES run the previously-advertised
integrity checks that only need compile-time data: the wire_format /
operation_verb OVERRIDE-mismatch check (HARD — a step override that contradicts
its materializer contract), and — WARN-by-default, hard behind ``strict_mcp`` /
``strict_apply`` / ``strict_field_coverage`` — MCP-dependency resolution, APPLY
ground-truth + directive, and prompt-content ⊇ required-fields. See
:func:`_contract_integrity_checks`.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tessellum.composer.contracts import (
    _ARTIFACT_KEYS,
    MATERIALIZER_CONTRACTS,
    MCP_CONTRACTS,
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
    split_contract_and_prompt,
)


class CompilerError(Exception):
    """DAG-level errors that aren't contract violations.

    Used for cycle detection, forward-reference violations, and missing
    skill-section text. Contract drift (unknown materializer key,
    missing required output field, etc.) raises ``ContractViolation``
    instead — the caller can ``except (CompilerError, ContractViolation)``
    to catch all compile-time failures.
    """


# ── Context-budget constants ────────────────────────────────────────────────


HARD_PROMPT_CAP_CHARS: int = 150_000
"""Global per-step cap on the rendered user-prompt size.

~50K tokens; Claude Sonnet 4.6's ceiling-ish without context-overflow.
Each step's rendered prompt (after `{{leaf.X}}` / `{{upstream.Y}}` /
`{{retry.X}}` substitution) is checked against this cap at runtime;
the compiler validates the *upper-bound estimate* against it at
compile time. Override per-step via the contract's `max_prompt_chars`
field.

A global cap protects against pipeline composition error (e.g., 5
upstream sources fanning in); per-upstream `max_chars` (declared on
each step's `expected_output_schema`) protects against any single
source dominating. Compile-time validation enforces sum(soft) ≤ hard.
"""


WARN_AT_PROMPT_FRACTION: float = 0.7
"""When the estimated prompt size at compile time exceeds 70% of the
hard cap, emit a warning. Caller decides what to do with warnings
(CI: treat as error; dev: log)."""


DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS: int = 25_000
"""Default soft cap per upstream output when the producer contract's
`expected_output_schema.max_chars` is not declared. Picked so 5
upstreams comfortably fit under HARD_PROMPT_CAP_CHARS with budget for
leaf metadata + prompt boilerplate."""


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
        timeout_seconds: Optional per-step watchdog timeout. ``None``
            → use the executor's default (typically 120s). When the
            backend call exceeds this value, the step result is marked
            ``error="stalled after Xs"`` and the scheduler proceeds.
            The in-flight call is not cancelled — it completes in the
            background; its eventual result is discarded.
        max_prompt_chars: Optional per-step hard cap on the rendered
            user-prompt size. ``None`` → use
            ``compiler.HARD_PROMPT_CAP_CHARS``. Runtime check: if the
            rendered prompt exceeds this, ``execute_step`` refuses to
            dispatch and surfaces a structured error
            rather than the LLM-side mystery failure.
        max_tokens: Optional per-step cap on the LLM RESPONSE length.
            ``None`` → use the ``LLMRequest`` default (16000). The big-output
            writer steps (a full plan body; an augmented plan that re-emits the
            plan PLUS the coverage map + gate tables + the per-note
            cross-reference contract) exceed the global default and truncate
            mid-JSON — they set a larger per-step cap here instead of raising the
            global, which would just move the truncation threshold for every
            other (small) step.
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
    max_tokens: int | None = None
    # P12 (FZ 20k9c1a1a1b7c2e): runtime-scaling coefficients. Pure passthrough
    # from the loader — the compiler NEVER derives (total_notes is a runtime
    # plan value, absent when compile_skill builds the one template). The driver
    # (digestion._derive_step_budgets) reads these AFTER compile, BEFORE dispatch,
    # to raise max_tokens/timeout_seconds from their static FLOOR by
    # coeff * declared_notes. None → no scaling (byte-identical to pre-P12).
    max_tokens_per_note: int | None = None
    timeout_seconds_per_note: float | None = None
    # R1.1 (FZ 20k9c1a1a1b7c2k2a1a): the declared input manifest —
    # tuple of (fully-qualified binding name, required). Empty for steps
    # authored before the manifest convention; audit_input_closure reports
    # those as the adoption worklist.
    declared_inputs: tuple[tuple[str, bool], ...] = ()


@dataclass(frozen=True)
class CompiledPipeline:
    """A single-file skill compiled to a typed DAG.

    Attributes:
        skill_path: Source canonical path.
        skill_name: Filename stem (e.g. ``"skill_tessellum_search_notes"``).
        pipeline_version: Assembled pipeline contract version.
        steps: Steps in topological order. ``steps[i].depends_on`` only
            references section_ids in ``steps[:i]``.
        compiled_at: ISO-8601 timestamp of when ``compile_skill`` ran.
        step_count: ``len(steps)`` — convenience for serialization.
        budget_warnings: Compile-time warnings about prompt-size
            estimates that exceed :data:`WARN_AT_PROMPT_FRACTION`
            (70%) of the hard cap. Each entry is a one-line
            description. Empty when no warnings; the compiler does
            not fail on warnings.
        re_emission_warnings: Compile-time warnings (P21-full;
            FZ 20k9c1a1a1b7c2j) about a ``no_op`` (DESCRIBE) step that
            CONSUMES a durable artifact (``{{...X}}`` where X is in
            :data:`~tessellum.composer.contracts._ARTIFACT_KEYS`) AND
            re-declares that same artifact as its own output — the
            E12/E16/E18 pass-through re-emission smell (it should read the
            artifact BY REFERENCE, not re-emit it through the LLM). A LINT,
            not a hard error: materializing *authors* (PRODUCE/APPLY) are never
            flagged (they legitimately write the artifact). ``compile_skill``
            appends here by default; ``strict_re_emission=True`` raises a
            ``ContractViolation`` instead.
        contract_warnings: Compile-time warnings (P9; FZ 20k9c1a1a1b7c2e) from
            the advertised-but-previously-unimplemented integrity checks —
            MCP-dependency resolution (``strict_mcp``), APPLY ground-truth +
            directive (``strict_apply``), and prompt-content ⊇ required-fields
            (``strict_field_coverage``). These ship WARN-by-default (many are
            heuristic or contradict the user-extensible MCP registry / the
            trivial-prompt test corpus); the matching ``strict_*`` flag turns a
            given family into a hard ``ContractViolation``. The wire_format /
            operation_verb OVERRIDE-mismatch check is HARD unconditionally (it
            is structural and inert — no shipped skill declares an override).
    """

    skill_path: Path
    skill_name: str
    pipeline_version: str
    steps: tuple[CompiledStep, ...]
    compiled_at: str = field(default_factory=lambda: dt.datetime.now(dt.UTC).isoformat())
    budget_warnings: tuple[str, ...] = ()
    re_emission_warnings: tuple[str, ...] = ()
    contract_warnings: tuple[str, ...] = ()

    @property
    def step_count(self) -> int:
        return len(self.steps)


# ── Re-emission lint (P21-full; FZ 20k9c1a1a1b7c2j) ──────────────────────────

# Any-namespace placeholder: {{leaf.X}} / {{upstream.X}} / {{artifact.X}}. The
# lint cares that the step CONSUMES artifact X, regardless of which channel.
# Local (not imported from executor) to avoid an import cycle — executor imports
# compiler.CompiledStep, so compiler must not import executor.
_CONSUMED_PLACEHOLDER_RE = re.compile(
    r"\{\{\s*(?:leaf|upstream|artifact)\.([a-z0-9_]+)\s*\}\}"
)


def _declared_output_keys(step: CompiledStep) -> set[str]:
    """The keys a step DECLARES as its own output — its ``output_key`` plus the
    top-level field names of its ``expected_output_schema`` (BOTH ``properties``
    AND ``required``). ``required`` is the sub-key that actually forces the LLM
    to emit a field (the schema-instruction + jsonschema.validate both key on
    it), so a step re-declaring an artifact ONLY under ``required`` (omitting
    ``properties``) still re-emits it — reading only ``properties`` would let
    that defeat the lint. This mirrors the materializer required-field check in
    ``_compile_step``, which reads ``required``."""
    keys: set[str] = set()
    if step.output_key:
        keys.add(step.output_key)
    schema = step.expected_output_schema or {}
    props = schema.get("properties")
    if isinstance(props, dict):
        keys.update(props.keys())
    required = schema.get("required")
    if isinstance(required, list):
        keys.update(k for k in required if isinstance(k, str))
    return keys


def _detect_re_emission(step: CompiledStep) -> str | None:
    """Return a lint message iff ``step`` is a pass-through re-emission of a
    durable artifact, else ``None``.

    The smell (E12/E16/E18): a ``no_op`` step CONSUMES an artifact key (in
    :data:`~tessellum.composer.contracts._ARTIFACT_KEYS`) via a ``{{...X}}``
    placeholder AND re-declares that same key as its own output — i.e. its job
    is "read X and hand it on", which it should do BY REFERENCE, not by
    re-emitting X through the LLM (lossy).

    Author-may-emit, pass-through-must-reference: a *materializing* step
    (``operation_verb`` PRODUCE / APPLY — ``body_markdown_to_file`` etc.) is the
    legitimate AUTHOR of the artifact and is NEVER flagged; only a ``no_op``
    (DESCRIBE) consumer-and-re-declarer is."""
    contract = step.materializer_contract
    # Only a no_op / DESCRIBE step can be a pass-through; a PRODUCE/APPLY author
    # legitimately emits the artifact. No contract (INFRA) → not a re-emitter.
    if contract is None or contract.operation_verb != "DESCRIBE":
        return None
    prompt = step.prompt_section_text or ""
    consumed = set(_CONSUMED_PLACEHOLDER_RE.findall(prompt))
    declared = _declared_output_keys(step)
    # The offending artifacts: consumed AND re-declared AND durable.
    offenders = sorted(set(_ARTIFACT_KEYS) & consumed & declared)
    if not offenders:
        return None
    return (
        f"step {step.section_id!r} (no_op/DESCRIBE) consumes and re-declares "
        f"artifact(s) {offenders} — a pass-through re-emission. Read the artifact "
        f"by reference (via the channel that already carries it — e.g. "
        f"{{{{artifact.X}}}} or the {{{{leaf.X}}}} it arrived on) and drop it from "
        f"this step's expected_output_schema/output_key; do not re-emit a large "
        f"artifact through the LLM. Only a materializing author may emit it."
    )


# ── P9: advertised contract-integrity checks (warn-by-default) ───────────────


def _field_mentioned_in_prompt(field: str, prompt: str) -> bool:
    """True if ``field`` (a snake_case output-field name) is mentioned in the
    prompt prose, tolerant of separators (``source_type`` ↔ ``source type`` /
    ``Source-Type``) but WORD-BOUNDARY anchored so a short field does not
    spuriously match a longer unrelated word (``edits`` must NOT match
    ``credits``; ``note`` must NOT match ``footnote``). Builds a regex that
    matches the field's ``_``/``-``-split tokens in order with flexible
    separators between them, bounded by ``\\b`` on each end."""
    tokens = [re.escape(t) for t in re.split(r"[_\-]+", field.lower()) if t]
    if not tokens:
        return False
    pattern = r"\b" + r"[\s_\-]*".join(tokens) + r"\b"
    return re.search(pattern, prompt.lower()) is not None


def _contract_integrity_checks(
    step: PipelineStep,
    compiled: CompiledStep,
    *,
    strict_mcp: bool,
    strict_apply: bool,
    strict_field_coverage: bool,
) -> list[str]:
    """The P9 advertised integrity checks the compiler previously documented but
    did not enforce (FZ 20k9c1a1a1b7c2e). Returns a list of warning strings;
    raises :class:`ContractViolation` for a family only when its ``strict_*``
    flag is set. Warn-by-default because these are either heuristic
    (field-coverage prose match), contradict the intentionally user-extensible
    MCP registry, or surface latent real-skill mis-declarations that must be
    fixed before a hard flip. (The structural wire_format / operation_verb
    OVERRIDE check is HARD and lives in ``_compile_step``.)"""
    warnings: list[str] = []
    contract = compiled.materializer_contract
    prompt = compiled.prompt_section_text or ""

    def _emit(kind: str, message: str, suggested_fix: str, strict: bool) -> None:
        if strict:
            raise ContractViolation(
                step_id=step.section_id, kind=kind, message=message,
                suggested_fix=suggested_fix,
            )
        warnings.append(f"[{kind}] {step.section_id}: {message}")

    # Check 5 — MCP resolution: every declared mcp_dependency name resolves in
    # the registry, and every declared call is one of its available_tools.
    for dep in step.mcp_dependencies:
        if dep.name not in MCP_CONTRACTS:
            _emit(
                ContractViolation.KIND_UNKNOWN_MCP,
                f"declares mcp_dependency {dep.name!r} not in the MCP registry "
                f"(known: {sorted(MCP_CONTRACTS)})",
                "Register the MCP in MCP_CONTRACTS, or correct the dependency name.",
                strict_mcp,
            )
            continue
        available = set(MCP_CONTRACTS[dep.name].available_tools)
        unknown_calls = [c for c in dep.calls if c not in available]
        if unknown_calls:
            _emit(
                ContractViolation.KIND_UNKNOWN_MCP_TOOL,
                f"mcp_dependency {dep.name!r} declares call(s) "
                f"{sorted(unknown_calls)} not in its available_tools "
                f"({sorted(available)})",
                "Correct the call name(s) or extend the MCP contract's available_tools.",
                strict_mcp,
            )

    if contract is not None:
        # Check 6/7 — APPLY ground-truth + directive, for a materializer that
        # edits EXISTING files (requires_existing_files).
        if getattr(contract, "requires_existing_files", False):
            has_literals = bool(step.applies_to_files)
            has_query = step.applies_to_files_query is not None
            if not has_literals and not has_query:
                _emit(
                    ContractViolation.KIND_APPLY_WITHOUT_GROUND_TRUTH,
                    f"materializer {step.materializer!r} edits existing files but "
                    f"the step declares neither applies_to_files nor "
                    f"applies_to_files_query",
                    "Declare applies_to_files (literal paths) or "
                    "applies_to_files_query so the ground-truth is resolvable.",
                    strict_apply,
                )
            # A LITERAL applies_to_files entry must be referenced in the prompt
            # via {{existing.<path>}}. A QUERY-declared step is satisfied by any
            # {{existing...}} block (the query resolves to a set at run time), so
            # we only demand per-path refs for literal entries.
            for path in step.applies_to_files:
                if f"{{{{existing.{path}}}}}" not in prompt:
                    _emit(
                        ContractViolation.KIND_EXISTING_PATH_NOT_REFERENCED,
                        f"applies_to_files declares {path!r} but the prompt does "
                        f"not reference {{{{existing.{path}}}}}",
                        f"Add {{{{existing.{path}}}}} to the prompt so the "
                        f"existing file content is injected before the edit.",
                        strict_apply,
                    )
        if getattr(contract, "apply_mode_directive_required", False):
            if "APPLY mode" not in prompt:
                _emit(
                    ContractViolation.KIND_MISSING_APPLY_DIRECTIVE,
                    f"materializer {step.materializer!r} requires the literal "
                    f"phrase 'APPLY mode' in the prompt (it edits files in place)",
                    "Add an 'APPLY mode' directive to the prompt so the agent "
                    "emits an edit, not a full-file rewrite.",
                    strict_apply,
                )

        # Check 1 — prompt ⊇ required-fields (PROSE side). The schema-side check
        # already runs in _compile_step; this warns when the prose ALSO fails to
        # instruct a required field. Heuristic (normalized substring), so
        # warn-by-default only. The runtime _render_output_schema_instruction
        # additionally injects the field names, so a warning here means neither
        # the authored prose NOR an obvious mention covers it — a prompt-quality
        # signal, not a hard defect.
        if step.role in ("CORE", "DEFERRED") and contract.required_output_fields:
            for f in contract.required_output_fields:
                if not _field_mentioned_in_prompt(f, prompt):
                    _emit(
                        ContractViolation.KIND_MISSING_REQUIRED_OUTPUT_FIELD,
                        f"required output field {f!r} is declared in the schema "
                        f"but not mentioned in the prompt prose",
                        f"Reference {f!r} in the prompt so the agent is instructed "
                        f"to emit it.",
                        strict_field_coverage,
                    )

    return warnings


# ── Public entry points ────────────────────────────────────────────────────


def compile_skill(
    skill_path: Path | str,
    *,
    strict_re_emission: bool = False,
    strict_mcp: bool = False,
    strict_apply: bool = False,
    strict_field_coverage: bool = False,
    warn_unmodeled_payloads: bool = False,
) -> CompiledPipeline:
    """Compile a single-file skill canonical into a typed DAG.

    Args:
        skill_path: Path to a skill canonical (``vault/resources/skills/skill_*.md``).
            Each pipeline step is an H2 section with a
            ``<!-- :: section_id = X :: -->`` anchor and a leading
            ``​```yaml`` contract block; the prose after the block is the
            step's prompt. No separate ``.pipeline.yaml`` sidecar.
        strict_re_emission: When ``True``, a detected pass-through re-emission
            (P21-full) raises a ``ContractViolation`` instead of being appended
            to ``re_emission_warnings``. Default ``False`` (warn only) — the
            design mandate: a lint, not a ban, so a legitimate ``no_op``
            consumer the heuristic misreads is never false-rejected.
        strict_mcp / strict_apply / strict_field_coverage: P9
            (FZ 20k9c1a1a1b7c2e) — turn the corresponding advertised
            integrity-check family (MCP-dependency resolution / APPLY
            ground-truth + directive / prompt-content ⊇ required-fields) from a
            ``contract_warnings`` entry into a hard ``ContractViolation``.
            Default ``False`` (warn) so the checks are truthful on the shipped
            corpus without breaking it (the MCP registry is user-extensible, the
            field-coverage match is heuristic, and two shipped skills carry
            latent APPLY mis-declarations to fix first). The structural
            wire_format / operation_verb OVERRIDE-mismatch check is HARD
            regardless (it is inert — no shipped skill declares an override).

    Returns:
        CompiledPipeline with steps in topological order.

    Raises:
        ContractViolation: An individual step's contract declarations
            don't match its materializer (unknown key, missing required
            output field, etc.); or, with ``strict_re_emission=True``, a
            pass-through re-emission.
        CompilerError: DAG-level errors — cycles, forward references,
            missing prompt-section text.
        PipelineValidationError: A contract block is schema-invalid or
            malformed (raised by the loader).
    """
    skill = Path(skill_path)
    pipeline = load_pipeline(skill)

    if pipeline is None:
        # No step sections (no ``​```yaml`` contract blocks) — the skill has
        # no Composer dispatch.
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

    # Compile-time context-budget validation.
    budget_warnings = _validate_context_budgets(compiled_steps)
    if warn_unmodeled_payloads:
        budget_warnings = list(budget_warnings) + _warn_unmodeled_payloads(
            compiled_steps
        )

    # P9: the advertised contract-integrity checks (MCP / APPLY / field-coverage).
    # Warn-by-default; each family raises only under its strict_* flag. Runs over
    # the loader step (mcp_dependencies / applies_to_files) zipped with the
    # compiled step (prompt_section_text / materializer_contract).
    contract_warnings: list[str] = []
    for step, cs in zip(sorted_steps, compiled_steps, strict=True):
        contract_warnings.extend(
            _contract_integrity_checks(
                step, cs,
                strict_mcp=strict_mcp,
                strict_apply=strict_apply,
                strict_field_coverage=strict_field_coverage,
            )
        )

    # P21-full: re-emission lint. Warn by default; raise only in strict mode.
    re_emission_warnings: list[str] = []
    for cs in compiled_steps:
        msg = _detect_re_emission(cs)
        if msg is None:
            continue
        if strict_re_emission:
            raise ContractViolation(
                step_id=cs.section_id,
                kind=ContractViolation.KIND_RE_EMISSION,
                message=msg,
                suggested_fix=(
                    "Consume the artifact by reference ({{artifact.X}}) and "
                    "remove it from this step's expected_output_schema / "
                    "output_key; only a materializing author may emit it."
                ),
            )
        re_emission_warnings.append(msg)

    return CompiledPipeline(
        skill_path=skill,
        skill_name=skill.stem,
        pipeline_version=pipeline.version,
        steps=tuple(compiled_steps),
        budget_warnings=tuple(budget_warnings),
        re_emission_warnings=tuple(re_emission_warnings),
        contract_warnings=tuple(contract_warnings),
    )


def _validate_context_budgets(steps: list[CompiledStep]) -> list[str]:
    """Estimate per-step prompt size from upstream soft caps, raise
    ``CompilerError`` on hard-cap overflow, and emit
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


# A2.4-lite (FZ 20k9c1a1a1b7c2k1a): the static budget model sums upstream soft
# caps + template text ONLY — a placeholder for a known-large runtime payload
# (the whole plan body, the inline source) is invisible to it, so the estimate
# can be wildly low exactly where the payloads are biggest (the O(plan x N)
# leaf inlining). OPT-IN (``compile_skill(warn_unmodeled_payloads=True)``) so
# shipped-skill compiles stay byte-identical — the review-skill's
# ``{{artifact.plan_text}}`` reads are the PRESCRIBED by-reference pattern and
# must not warn by default. Leaf keys are the unbounded hazard; artifact keys
# are restricted to the real ``_ARTIFACT_KEYS`` (anything else renders a
# ``<missing>`` sentinel, never a payload). The true dispatch-time bound
# arrives with A3, where ``ArtifactRef.size`` makes payloads knowable.
_LARGE_LEAF_KEYS: tuple[str, ...] = (
    "plan_text", "source_excerpt", "source_content", "members", "planned_notes",
)
_PAYLOAD_PLACEHOLDER_RE = re.compile(
    r"\{\{\s*(leaf|artifact)\s*\.\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}"
)


def _warn_unmodeled_payloads(steps: list[CompiledStep]) -> list[str]:
    warnings: list[str] = []
    for step in steps:
        template = step.prompt_section_text or ""
        found: set[str] = set()
        for m in _PAYLOAD_PLACEHOLDER_RE.finditer(template):
            ns, key = m.group(1), m.group(2)
            if ns == "leaf" and key in _LARGE_LEAF_KEYS:
                found.add(f"{{{{leaf.{key}}}}}")
            elif ns == "artifact" and key in _ARTIFACT_KEYS:
                found.add(f"{{{{artifact.{key}}}}}")
        if found:
            warnings.append(
                f"step {step.section_id!r}: references large runtime "
                f"payload(s) {', '.join(sorted(found))} not modeled by the "
                f"static budget estimate — the effective prompt may far "
                f"exceed it."
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

        # P9 (FZ 20k9c1a1a1b7c2e): a step may DECLARE a wire_format / operation_verb
        # OVERRIDE (loader.PipelineStep.wire_format / .operation_verb; the schema
        # documents them as "optional override, the contract is authoritative").
        # An override that CONTRADICTS the materializer's contract is a latent
        # E9-class defect (the exact drift executor.py fixed at runtime) — fail it
        # at compile. HARD (not warn): it is structural, not heuristic, and no
        # shipped skill declares an override, so the check is inert until real
        # drift appears.
        if step.wire_format is not None and step.wire_format != materializer_contract.wire_format:
            raise ContractViolation(
                step_id=step.section_id,
                kind=ContractViolation.KIND_WIRE_FORMAT_MISMATCH,
                message=(
                    f"step declares wire_format={step.wire_format!r} but its "
                    f"materializer {step.materializer!r} contract is "
                    f"{materializer_contract.wire_format!r}."
                ),
                suggested_fix=(
                    f"Drop the wire_format override (the contract is "
                    f"authoritative) or use a materializer whose wire_format is "
                    f"{step.wire_format!r}."
                ),
            )
        if step.operation_verb is not None and step.operation_verb != materializer_contract.operation_verb:
            raise ContractViolation(
                step_id=step.section_id,
                kind=ContractViolation.KIND_OPERATION_VERB_MISMATCH,
                message=(
                    f"step declares operation_verb={step.operation_verb!r} but its "
                    f"materializer {step.materializer!r} contract is "
                    f"{materializer_contract.operation_verb!r}."
                ),
                suggested_fix=(
                    f"Drop the operation_verb override or use a materializer whose "
                    f"operation_verb is {step.operation_verb!r}."
                ),
            )

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

    # Extract the step's PROMPT from the canonical section — the section body
    # with its leading ``​```yaml`` contract block stripped off. The contract
    # block became `step` (via the loader); what remains is the prompt prose
    # (with {{leaf.X}} / {{upstream.Y}} placeholders resolved at run time).
    try:
        section_body = load_skill_section(skill_path, step.section_id)
    except SkillExtractionError as e:
        raise CompilerError(
            f"step {step.section_id!r}: cannot extract prompt section from "
            f"{skill_path}: {e}"
        ) from e
    _, prompt_text = split_contract_and_prompt(section_body)

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
        max_tokens=step.max_tokens,
        max_tokens_per_note=step.max_tokens_per_note,
        timeout_seconds_per_note=step.timeout_seconds_per_note,
        declared_inputs=tuple((i.name, i.required) for i in step.inputs),
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


# ── R1.1 (FZ 20k9c1a1a1b7c2k2a1a): the input-closure audit ────────────────────

_INPUT_HOLE_RE = re.compile(r"\{\{\s*(leaf|upstream|artifact)\.([a-z0-9_]+)\s*\}\}")


def audit_input_closure(pipeline: "CompiledPipeline") -> list[str]:
    """The closure lint over every step's input contract (report mode).

    For each step: the prompt's actual template holes (``{{leaf.X}}`` /
    ``{{upstream.Y}}`` / ``{{artifact.Z}}`` — ``retry.*`` and ``existing.*``
    are runtime/apply-mode namespaces, not informational inputs) must equal
    the declared ``inputs`` manifest. Three finding classes:

    - ``no input manifest`` — the step predates the convention; the listed
      holes ARE its adoption worklist.
    - ``undeclared input`` — a hole the manifest does not name (the F1/F2
      class surfaces here the moment a migration misses a step).
    - ``declared but never referenced`` — a manifest entry with no hole
      (drift in the other direction).

    Pure report: returns finding strings, raises nothing — enforcement is the
    caller's policy decision (the deployment-parity canary asserts the four
    shipped skills stay clean)."""
    findings: list[str] = []
    for step in pipeline.steps:
        prompt = step.prompt_section_text or ""
        holes = {f"{ns}.{key}" for ns, key in _INPUT_HOLE_RE.findall(prompt)}
        declared = {name for name, _req in step.declared_inputs}
        if not step.declared_inputs:
            if holes:
                findings.append(
                    f"step {step.section_id!r}: no input manifest "
                    f"(holes: {sorted(holes)})"
                )
            continue
        for hole in sorted(holes - declared):
            findings.append(
                f"step {step.section_id!r}: undeclared input {{{{{hole}}}}}"
            )
        for name in sorted(declared - holes):
            findings.append(
                f"step {step.section_id!r}: input {name!r} declared but "
                f"never referenced in the prompt"
            )
    return findings
