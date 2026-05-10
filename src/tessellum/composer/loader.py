"""Load + validate a skill's pipeline sidecar against the schema.

Public API:

    load_pipeline(skill_path) -> Pipeline | None
        Resolves the skill canonical's ``pipeline_metadata:`` field, reads
        the sidecar YAML, validates it against ``pipeline.schema.json`` and
        the Pydantic models in this module, returns a parsed ``Pipeline``
        object. Returns ``None`` if the skill declares
        ``pipeline_metadata: none``.

    Pipeline           — top-level sidecar model (version + steps).
    PipelineStep       — one step entry in the sidecar's ``pipeline`` list.
    PipelineValidationError — raised on schema or model drift.

Two-stage validation:

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
import yaml
from pydantic import BaseModel, ConfigDict, Field

from tessellum.composer.skill_extractor import (
    SkillExtractionError,
    load_pipeline_metadata,
)

_SCHEMA_PATH = Path(__file__).parent / "schemas" / "pipeline.schema.json"


class PipelineValidationError(ValueError):
    """Raised on any sidecar drift — schema, model, or skill-extraction."""


# ── Pydantic models mirroring pipeline.schema.json ─────────────────────────


class MCPDependency(BaseModel):
    """One entry in a step's ``mcp_dependencies`` list."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    calls: tuple[str, ...] = ()
    required: bool = True


class Query(BaseModel):
    """A declarative query for ``applies_to_files_query`` resolution.

    Resolved by the compiler against the unified DB at compile time.
    Tessellum's indexer is not yet shipped (Wave 5+); v0.0.9 loaders accept
    this field but cannot resolve it.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: str
    max_files: int | None = None
    exclude_dirs: tuple[str, ...] = ()


class PipelineStep(BaseModel):
    """One step in a sidecar's ``pipeline`` list. Mirrors the JSON schema's
    ``Step`` definition with typed access."""

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


class Pipeline(BaseModel):
    """Top-level sidecar model: version + ordered list of steps."""

    model_config = ConfigDict(frozen=True, extra="allow")

    version: str = Field(default="1.0")
    pipeline: tuple[PipelineStep, ...] = Field(...)


# ── Loader ─────────────────────────────────────────────────────────────────


def load_pipeline(skill_path: Path | str) -> Pipeline | None:
    """Load + validate a skill's pipeline sidecar.

    Args:
        skill_path: Path to the skill canonical markdown.

    Returns:
        Parsed ``Pipeline`` instance, OR ``None`` if the skill's frontmatter
        declares ``pipeline_metadata: none`` (skill has no Composer dispatch).

    Raises:
        PipelineValidationError: any drift — missing sidecar file, malformed
            YAML, schema violation, Pydantic validation failure, or a
            sidecar step whose ``section_id`` has no matching anchor in the
            canonical.
    """
    skill_path = Path(skill_path)
    try:
        sidecar_path = load_pipeline_metadata(skill_path)
    except SkillExtractionError as e:
        raise PipelineValidationError(str(e)) from e

    if sidecar_path is None:
        return None

    if not sidecar_path.is_file():
        raise PipelineValidationError(
            f"skill {skill_path.name} declares pipeline_metadata: "
            f"{sidecar_path}, but that file does not exist."
        )

    try:
        raw_yaml = sidecar_path.read_text(encoding="utf-8")
    except OSError as e:
        raise PipelineValidationError(
            f"cannot read sidecar {sidecar_path}: {e}"
        ) from e

    try:
        data = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as e:
        raise PipelineValidationError(
            f"sidecar {sidecar_path} is not valid YAML: {e}"
        ) from e

    if not isinstance(data, dict):
        raise PipelineValidationError(
            f"sidecar {sidecar_path} top-level must be a mapping; "
            f"got {type(data).__name__}"
        )

    # Stage 1: JSON Schema validation.
    schema = _load_schema()
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise PipelineValidationError(
            f"sidecar {sidecar_path} fails schema validation:\n  "
            f"{e.message}\n  at path: /{'/'.join(str(p) for p in e.absolute_path)}"
        ) from e

    # Stage 2: Pydantic model construction.
    try:
        pipeline = Pipeline(**data)
    except Exception as e:  # ValidationError + others
        raise PipelineValidationError(
            f"sidecar {sidecar_path} fails Pydantic validation: {e}"
        ) from e

    # Stage 3: cross-file consistency — every step.section_id must have a
    # matching anchor in the skill canonical.
    from tessellum.composer.skill_extractor import list_section_ids

    canonical_section_ids = set(list_section_ids(skill_path))
    sidecar_section_ids = {step.section_id for step in pipeline.pipeline}
    orphans = sidecar_section_ids - canonical_section_ids
    if orphans:
        raise PipelineValidationError(
            f"sidecar {sidecar_path} declares step section_ids with no "
            f"matching anchor in {skill_path.name}: {sorted(orphans)}. "
            f"Canonical anchors: {sorted(canonical_section_ids)}."
        )

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
