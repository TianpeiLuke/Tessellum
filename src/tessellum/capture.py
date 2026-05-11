"""Note capture — create a new vault note from a typed template.

Public API:

    REGISTRY                — dict[flavor: str, TemplateSpec]
    list_flavors()          — sorted list of flavor names (CLI choices)
    get_spec(flavor)        — TemplateSpec for a flavor
    capture(...)            — copy template, transform, write; returns CaptureResult

Each ``flavor`` maps to one of the 12 templates under
``vault/resources/templates/`` (excluding ``template_yaml_header`` which is a
spec reference, not a copy-and-fill skeleton). The capture step:

1. Validates the slug (lowercase letters/digits/underscores).
2. Reads the source template via ``tessellum.data.templates_dir()``.
3. Strips the leading ``<!-- HOW TO USE THIS TEMPLATE: ... -->`` HTML comment.
4. Replaces ``date of note: ...`` with today's date.
5. Replaces ``status: template`` with ``status: draft``.
6. Writes to the vault destination dir under the right filename prefix.

The resulting note still has placeholder values in fields the user must fill
(keywords, topics, body sections), but it validates against the YAML
frontmatter spec — closed enums match, required fields present, format clean.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

from tessellum.data import templates_dir


@dataclass(frozen=True)
class TemplateSpec:
    """Metadata for one capture-able template flavor."""

    flavor: str
    template_filename: str
    destination: str
    filename_prefix: str
    bb_type: str
    second_category: str
    description: str


REGISTRY: dict[str, TemplateSpec] = {
    "concept": TemplateSpec(
        flavor="concept",
        template_filename="template_concept.md",
        destination="resources/term_dictionary",
        filename_prefix="term_",
        bb_type="concept",
        second_category="terminology",
        description="Definition note for a named concept (term notes)",
    ),
    "procedure": TemplateSpec(
        flavor="procedure",
        template_filename="template_procedure.md",
        destination="resources/how_to",
        filename_prefix="howto_",
        bb_type="procedure",
        second_category="how_to",
        description="How-to guide for a procedural workflow",
    ),
    "skill": TemplateSpec(
        flavor="skill",
        template_filename="template_skill.md",
        destination="resources/skills",
        filename_prefix="skill_",
        bb_type="procedure",
        second_category="skill",
        description="Agent-executable skill canonical body",
    ),
    "model": TemplateSpec(
        flavor="model",
        template_filename="template_model.md",
        destination="areas",
        filename_prefix="model_",
        bb_type="model",
        second_category="terminology",
        description="Relational structure (architecture, schema, system model)",
    ),
    "argument": TemplateSpec(
        flavor="argument",
        template_filename="template_argument.md",
        destination="resources/analysis_thoughts",
        filename_prefix="thought_",
        bb_type="argument",
        second_category="analysis",
        description="Architectural argument (thesis + reason + evidence)",
    ),
    "counter_argument": TemplateSpec(
        flavor="counter_argument",
        template_filename="template_counter_argument.md",
        destination="resources/analysis_thoughts",
        filename_prefix="thought_counter_",
        bb_type="counter_argument",
        second_category="analysis",
        description="Counter-argument or palinode against an argument",
    ),
    "hypothesis": TemplateSpec(
        flavor="hypothesis",
        template_filename="template_hypothesis.md",
        destination="resources/analysis_thoughts",
        filename_prefix="thought_hypothesis_",
        bb_type="hypothesis",
        second_category="analysis",
        description="Falsifiable hypothesis with test design",
    ),
    "empirical_observation": TemplateSpec(
        flavor="empirical_observation",
        template_filename="template_empirical_observation.md",
        destination="resources/analysis_thoughts",
        filename_prefix="thought_observation_",
        bb_type="empirical_observation",
        second_category="analysis",
        description="Inline empirical observation (lightweight)",
    ),
    "experiment": TemplateSpec(
        flavor="experiment",
        template_filename="template_experiment.md",
        destination="archives/experiments",
        filename_prefix="experiment_",
        bb_type="empirical_observation",
        second_category="experiment",
        description="Pre-registered experiment with full methodology",
    ),
    "navigation": TemplateSpec(
        flavor="navigation",
        template_filename="template_navigation.md",
        destination="0_entry_points",
        filename_prefix="",
        bb_type="navigation",
        second_category="navigation",
        description="Generic navigation/index note",
    ),
    "entry_point": TemplateSpec(
        flavor="entry_point",
        template_filename="template_entry_point.md",
        destination="0_entry_points",
        filename_prefix="entry_",
        bb_type="navigation",
        second_category="index",
        description="Master TOC or per-surface entry point",
    ),
    "acronym_glossary": TemplateSpec(
        flavor="acronym_glossary",
        template_filename="template_acronym_glossary.md",
        destination="0_entry_points",
        filename_prefix="acronym_glossary_",
        bb_type="navigation",
        second_category="index",
        description="Acronym glossary indexing term notes by acronym",
    ),
    "code_snippet": TemplateSpec(
        flavor="code_snippet",
        template_filename="template_code_snippet.md",
        destination="resources/code_snippets",
        filename_prefix="snippet_",
        bb_type="procedure",
        second_category="code_snippets",
        description="Code snippet documenting one component or algorithm",
    ),
    "code_repo": TemplateSpec(
        flavor="code_repo",
        template_filename="template_code_repo.md",
        destination="areas/code_repos",
        filename_prefix="repo_",
        bb_type="model",
        second_category="code_repos",
        description="Code repository documentation note",
    ),
}


@dataclass(frozen=True)
class CaptureResult:
    """Outcome of a successful capture call.

    Attributes:
        path: The captured note's path (always set).
        flavor: The template flavor that was captured.
        slug: The slug used for the new note.
        sidecar_path: For ``flavor="skill"``, the paired
            ``skill_<slug>.pipeline.yaml`` Composer sidecar. ``None`` for all
            other flavors and for skills where the sidecar template is
            missing (defensive fallback).
    """

    path: Path
    flavor: str
    slug: str
    sidecar_path: Path | None = None


_SLUG_RE = re.compile(r"^[a-z0-9_]+$")

# Match the outer ``<!-- HOW TO USE ... -->`` block. The closing ``-->`` must
# be at the start of its own line (with optional indent) — otherwise we
# stop at any inline ``<!-- HOW TO USE -->`` mention inside the instructional
# text (e.g. "5. Remove this <!-- HOW TO USE --> commentary block.").
_HOW_TO_USE_RE = re.compile(
    r"<!--\s*\n?\s*HOW TO USE.*?\n\s*-->",
    re.DOTALL | re.IGNORECASE,
)
_DATE_LINE_RE = re.compile(
    r"^date of note: (?:YYYY-MM-DD|\d{4}-\d{2}-\d{2})\s*$",
    re.MULTILINE,
)
_STATUS_TEMPLATE_RE = re.compile(r"^status: template\s*$", re.MULTILINE)
_TRIPLE_NEWLINE_RE = re.compile(r"\n{3,}")

# Inject ``bb_schema_version: <N>`` immediately after the ``building_block:`` line
# unless the frontmatter already declares it. Captures the indentation (none in
# practice) + trailing newline so the inserted line slots in cleanly.
_BUILDING_BLOCK_LINE_RE = re.compile(
    r"^(building_block:\s*[a-z_]+)\s*$", re.MULTILINE
)
_BB_SCHEMA_VERSION_PRESENT_RE = re.compile(r"^bb_schema_version:", re.MULTILINE)


def list_flavors() -> list[str]:
    """Sorted list of registered flavor keys (suitable for CLI choices)."""
    return sorted(REGISTRY)


def get_spec(flavor: str) -> TemplateSpec:
    """Look up a TemplateSpec by flavor key. Raises ValueError if unknown."""
    if flavor not in REGISTRY:
        raise ValueError(
            f"unknown template flavor '{flavor}'. "
            f"Available: {', '.join(list_flavors())}"
        )
    return REGISTRY[flavor]


def capture(
    flavor: str,
    slug: str,
    vault_root: Path,
    *,
    force: bool = False,
    today: dt.date | None = None,
    destination: str | None = None,
    filename_prefix: str | None = None,
) -> CaptureResult:
    """Create a new vault note from a typed template.

    Args:
        flavor: Template flavor key (see :data:`REGISTRY`).
        slug: New note's identifier; must be lowercase letters/digits/underscores.
        vault_root: Vault root directory (the dir containing
            ``0_entry_points/``, ``resources/``, etc.).
        force: If ``True``, overwrite an existing target file.
        today: Override the date stamped into the note (default: ``date.today()``).
        destination: Override the REGISTRY-default destination directory
            (relative to ``vault_root``). Agents/callers know the
            specific note's sub-category better than the registry can:
            a ``model``-flavored note about a repo wants
            ``areas/code_repos/``; one about an algorithm wants
            ``areas/tools/``. REGISTRY's value is the *default*, not a
            constraint.
        filename_prefix: Override the REGISTRY-default filename prefix
            (e.g., ``repo_`` for repo architecture, ``tool_`` for
            algorithm/tool notes, ``team_`` for team structure).
            REGISTRY's value is the default.

    Returns:
        CaptureResult with the path of the created file.

    Raises:
        ValueError: Invalid flavor or slug.
        FileExistsError: Target file exists and ``force=False``.
        FileNotFoundError: Vault root or destination subdir missing,
            or template file missing.
    """
    if not _SLUG_RE.match(slug):
        raise ValueError(
            f"slug '{slug}' must be lowercase letters/digits/underscores only"
        )
    spec = get_spec(flavor)
    today = today or dt.date.today()

    src = templates_dir() / spec.template_filename
    if not src.is_file():
        raise FileNotFoundError(f"template not found: {src}")

    effective_destination = destination if destination is not None else spec.destination
    effective_prefix = (
        filename_prefix if filename_prefix is not None else spec.filename_prefix
    )

    dest_dir = vault_root / effective_destination
    if not dest_dir.is_dir():
        raise FileNotFoundError(
            f"destination directory does not exist: {dest_dir}. "
            f"Either create the {effective_destination} subdirectory or "
            f"pass a different destination= override."
        )

    dest = dest_dir / f"{effective_prefix}{slug}.md"
    if dest.exists() and not force:
        raise FileExistsError(
            f"target file already exists: {dest}. Pass force=True to overwrite."
        )

    text = src.read_text(encoding="utf-8")
    text = _strip_how_to_use(text)
    text = _set_date(text, today)
    text = _set_status(text, "draft")
    text = _set_bb_schema_version(text)

    sidecar_path: Path | None = None
    if flavor == "skill":
        # Operationalize the skill canonical ↔ pipeline.yaml pairing: emit a
        # paired ``skill_<slug>.pipeline.yaml`` next to the canonical, and
        # rewrite the canonical's ``pipeline_metadata: none`` placeholder to
        # point at the new sidecar. Authors who don't need Composer dispatch
        # can delete the sidecar and revert pipeline_metadata to ``none``.
        sidecar_template = templates_dir() / "template_skill.pipeline.yaml"
        if sidecar_template.is_file():
            sidecar_filename = f"{spec.filename_prefix}{slug}.pipeline.yaml"
            sidecar_path = dest_dir / sidecar_filename
            if sidecar_path.exists() and not force:
                raise FileExistsError(
                    f"target sidecar already exists: {sidecar_path}. "
                    f"Pass force=True to overwrite."
                )
            sidecar_text = sidecar_template.read_text(encoding="utf-8")
            sidecar_path.write_text(sidecar_text, encoding="utf-8")

            text = text.replace(
                "pipeline_metadata: none",
                f"pipeline_metadata: ./{sidecar_filename}",
                1,
            )
        # If the sidecar template is missing, fall through silently — the
        # canonical still ships, just without paired-sidecar emission.

    text = _TRIPLE_NEWLINE_RE.sub("\n\n", text)
    dest.write_text(text, encoding="utf-8")
    return CaptureResult(
        path=dest, flavor=flavor, slug=slug, sidecar_path=sidecar_path
    )


def _strip_how_to_use(text: str) -> str:
    return _HOW_TO_USE_RE.sub("", text, count=1)


def _set_date(text: str, date: dt.date) -> str:
    return _DATE_LINE_RE.sub(f"date of note: {date.isoformat()}", text, count=1)


def _set_status(text: str, new_status: str) -> str:
    return _STATUS_TEMPLATE_RE.sub(f"status: {new_status}", text, count=1)


def _set_bb_schema_version(text: str) -> str:
    """Inject ``bb_schema_version: <N>`` immediately after the
    ``building_block:`` line (frozen-at-creation per D8).

    Reads ``BB_SCHEMA_VERSION`` from :mod:`tessellum.bb.types` at call
    time (live value, not the package alias — per the v0.0.52
    import-aliasing quirk).

    No-op when the template already declares ``bb_schema_version:``
    (back-compat for templates that may include it explicitly) or
    when no ``building_block:`` line is found (e.g., legacy templates).
    """
    if _BB_SCHEMA_VERSION_PRESENT_RE.search(text):
        return text
    # Live read — not via package alias.
    from tessellum.bb.types import BB_SCHEMA_VERSION

    def _replace(m: re.Match[str]) -> str:
        return f"{m.group(1)}\nbb_schema_version: {BB_SCHEMA_VERSION}"

    return _BUILDING_BLOCK_LINE_RE.sub(_replace, text, count=1)
