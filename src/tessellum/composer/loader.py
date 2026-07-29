"""Load + validate a skill's pipeline from its single-file canonical.

A skill is one markdown note: each pipeline step is an H2 section carrying a
``<!-- :: section_id = X :: -->`` anchor and a leading ``​```yaml`` contract
block. This module reads those per-section contract blocks (via
:mod:`tessellum.composer.skill_extractor`), assembles them into a
``Pipeline``, and validates it. There is no separate ``.pipeline.yaml``
sidecar.

Public API:

    load_pipeline(skill_path) -> Pipeline | None
        Reads every step section's contract block from the canonical (in
        document order), validates each against ``pipeline.schema.json`` and
        the Pydantic models here, and returns a parsed ``Pipeline``. Returns
        ``None`` if the canonical has no step sections (no ``​```yaml``
        contract blocks) — the skill has no Composer dispatch.

    Pipeline           — top-level model (version + steps).
    PipelineStep       — one step entry, from a section's contract block.
    PipelineValidationError — raised on schema or model drift.

Two-stage validation (per step):

    Stage 1: jsonschema (structural — required keys, enum membership,
             pattern match). Surfaces the broadest class of errors first.
    Stage 2: Pydantic V2 model construction (typed access + immutability).
             Catches anything jsonschema's draft-07 doesn't (e.g. cross-
             field dependencies enforced via Pydantic validators).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
from pydantic import BaseModel, ConfigDict, Field

from tessellum.composer.skill_extractor import (
    SkillExtractionError,
    iter_step_sections,
)

_SCHEMA_PATH = Path(__file__).parent / "schemas" / "pipeline.schema.json"


class PipelineValidationError(ValueError):
    """Raised on any skill-pipeline drift — schema, model, or extraction."""


# ── Pydantic models mirroring pipeline.schema.json ─────────────────────────


class MCPDependency(BaseModel):
    """One entry in a step's ``mcp_dependencies`` list."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    calls: tuple[str, ...] = ()
    required: bool = True


class Query(BaseModel):
    """A declarative query for ``applies_to_files_query`` resolution.

    Resolved by the compiler against the unified index DB at compile
    time. Step contracts may declare the field even when the index is
    unavailable — the loader accepts it; resolution happens later in
    the compiler.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: str
    max_files: int | None = None
    exclude_dirs: tuple[str, ...] = ()


class StepInput(BaseModel):
    """R1.1 (FZ 20k9c1a1a1b7c2k2a1a): one declared informational input of a
    step — the input-manifest half of the contract symmetry (steps always
    declared outputs; inputs lived as untyped template holes plus prose, the
    root of the J3 tool-role-play class). ``name`` is the fully-qualified
    binding (``leaf.X`` / ``upstream.Y`` / ``artifact.Z``); ``required`` marks
    bindings whose empty/sentinel rendering should refuse dispatch (R1.3);
    ``role`` is a one-line human note."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    required: bool = False
    role: str = ""


class PipelineStep(BaseModel):
    """One inline step contract with typed access to the ``Step`` schema."""

    model_config = ConfigDict(frozen=True, extra="allow")

    section_id: str
    role: str  # "CORE" | "DEFERRED" | "INFRA" — schema enforces enum
    aggregation: str  # "per_leaf" | "cross_leaf" | "corpus_wide"
    batchable: bool
    depends_on: tuple[str, ...] = ()
    materializer: str | None = None
    wire_format: str | None = None
    operation_verb: str | None = None
    applies_to_files: tuple[str, ...] = ()
    applies_to_files_query: Query | None = None
    expected_output_schema: dict[str, Any] | None = None
    prompt_template: str | None = None
    output_key: str | None = None
    mcp_dependencies: tuple[MCPDependency, ...] = ()
    inputs: tuple[StepInput, ...] = ()
    """R1.1: the step's declared informational inputs — audited for closure
    against the prompt's actual template holes by
    :func:`tessellum.composer.compiler.audit_input_closure`."""
    # Robustness fields. All optional.
    timeout_seconds: float | None = None
    """Per-step watchdog timeout. None → use executor default (120s)."""
    max_prompt_chars: int | None = None
    """Per-step hard cap on rendered prompt size. None → use
    compiler.HARD_PROMPT_CAP_CHARS (150K)."""
    max_tokens: int | None = None
    """Per-step cap on the LLM RESPONSE length. None → use the LLMRequest
    default (16000). The big-output writer steps (a full plan body, an
    augmented plan carrying the coverage map + gate tables + per-note
    cross-reference contract) exceed the global default and truncate mid-JSON;
    they declare a larger per-step cap here rather than raising the global
    (which just moves the truncation threshold for every other step)."""
    max_tokens_per_note: int | None = None
    """P12 (FZ 20k9c1a1a1b7c2e): a per-declared-note RESPONSE-token coefficient.
    A step whose output scales with the plan's note count declares this so the
    driver DERIVES an effective ``max_tokens`` at runtime (``max_tokens`` becomes
    a FLOOR, the derived value only raises it) from ``total_notes`` — a NEW large
    plan is then self-budgeting instead of inheriting a hand-set constant tuned
    for a small one. None → no scaling (the static ``max_tokens`` alone)."""
    timeout_seconds_per_note: float | None = None
    """P12: a per-declared-note WATCHDOG-seconds coefficient, analogous to
    :attr:`max_tokens_per_note`. None → no scaling (the static
    ``timeout_seconds`` alone)."""


class Pipeline(BaseModel):
    """Assembled pipeline model: version plus ordered inline steps."""

    model_config = ConfigDict(frozen=True, extra="allow")

    version: str = Field(default="1.0")
    pipeline: tuple[PipelineStep, ...] = Field(...)


# ── Loader ─────────────────────────────────────────────────────────────────


def load_pipeline(skill_path: Path | str) -> Pipeline | None:
    """Load + validate a skill's pipeline from its single-file canonical.

    Args:
        skill_path: Path to the skill canonical markdown.

    Returns:
        Parsed ``Pipeline`` instance, OR ``None`` if the canonical has no
        step sections (no ``​```yaml`` contract blocks) — the skill has no
        Composer dispatch.

    Raises:
        PipelineValidationError: any drift — malformed contract block,
            schema violation, or Pydantic validation failure. The step's
            ``section_id`` always comes from its anchor, so section_id /
            contract mismatch is structurally impossible.
    """
    skill_path = Path(skill_path)
    try:
        step_sections = iter_step_sections(skill_path)
    except SkillExtractionError as e:
        raise PipelineValidationError(str(e)) from e

    if not step_sections:
        return None

    schema = _load_schema()
    defs = schema.get("$defs") or schema.get("definitions") or {}
    step_def = defs.get("Step")
    # Validate each step against the Step definition, but keep the top-level
    # ``definitions``/``$defs`` in scope so its internal ``$ref``s (Query,
    # MCPDependency) still resolve.
    step_schema = None
    if step_def is not None:
        step_schema = dict(step_def)
        if "$defs" in schema:
            step_schema["$defs"] = schema["$defs"]
        if "definitions" in schema:
            step_schema["definitions"] = schema["definitions"]

    steps: list[dict[str, Any]] = []
    for sec in step_sections:
        # The section_id comes from the anchor — never the contract block —
        # so a step can never reference a section that doesn't exist.
        step_data = dict(sec.contract)
        step_data["section_id"] = sec.section_id

        # Stage 1: JSON Schema validation (per step, against the Step def).
        if step_schema is not None:
            try:
                jsonschema.validate(instance=step_data, schema=step_schema)
            except jsonschema.ValidationError as e:
                raise PipelineValidationError(
                    f"{skill_path.name} step {sec.section_id!r} fails schema "
                    f"validation:\n  {e.message}\n  at path: "
                    f"/{'/'.join(str(p) for p in e.absolute_path)}"
                ) from e
        steps.append(step_data)

    # Stage 2: Pydantic model construction (whole pipeline).
    try:
        pipeline = Pipeline(pipeline=steps)
    except Exception as e:  # ValidationError + others
        raise PipelineValidationError(
            f"{skill_path.name} fails Pydantic validation: {e}"
        ) from e

    return pipeline


_schema_cache: dict[str, Any] | None = None


def _load_schema() -> dict[str, Any]:
    """Read pipeline.schema.json once and cache."""
    global _schema_cache
    if _schema_cache is None:
        try:
            _schema_cache = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        except OSError as e:
            raise PipelineValidationError(
                f"cannot read pipeline schema at {_SCHEMA_PATH}: {e}"
            ) from e
    return _schema_cache
