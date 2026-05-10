"""Read sections from a skill canonical and resolve its sidebar YAML.

Two public functions:

    load_skill_section(skill_path, section_id) -> str
        Reads the skill canonical, finds the
        ``<!-- :: section_id = X :: -->`` anchor matching ``section_id``,
        returns the section's body text (everything between this anchor's
        H2 heading and the next H2 / EOF).

    load_pipeline_metadata(skill_path) -> Path | None
        Returns the absolute path to the skill's ``.pipeline.yaml`` sidecar
        as declared in the canonical's frontmatter ``pipeline_metadata:``
        field. Returns ``None`` if the field is ``"none"`` (sentinel for
        "skill has no Composer dispatch") or absent.

Both raise ``SkillExtractionError`` on malformed input.
"""

from __future__ import annotations

import re
from pathlib import Path

from tessellum.format.parser import FrontmatterParseError, parse_note

# Match ``## Heading text <!-- :: section_id = X :: -->`` anywhere a heading
# can appear. We capture the section_id; the heading itself is consumed.
_SECTION_ANCHOR_RE = re.compile(
    r"^##\s+.*?<!--\s*::\s*section_id\s*=\s*([a-z0-9_]+)\s*::\s*-->\s*$",
    re.MULTILINE,
)

# Once we know a section's start line, this matches the start of the NEXT
# H2 (or EOF) so we can extract the body in between.
_NEXT_H2_RE = re.compile(r"^##\s+", re.MULTILINE)


class SkillExtractionError(ValueError):
    """Raised when a skill canonical cannot be parsed or a section is missing."""


def load_skill_section(skill_path: Path | str, section_id: str) -> str:
    """Extract the body text of a section identified by ``section_id`` anchor.

    Args:
        skill_path: Path to a skill canonical (markdown file with YAML
            frontmatter and ``<!-- :: section_id = X :: -->`` anchors).
        section_id: The anchor id to match (e.g. ``"step_2_extract_facets"``).

    Returns:
        The body text of the section, with leading/trailing whitespace
        stripped. Excludes the heading line itself.

    Raises:
        SkillExtractionError: Skill cannot be read, no anchor matches the
            section_id, or the skill has malformed structure.
    """
    skill_path = Path(skill_path)
    try:
        note = parse_note(skill_path)
    except FrontmatterParseError as e:
        raise SkillExtractionError(
            f"cannot parse skill {skill_path}: {e}"
        ) from e

    body = note.body
    matches = list(_SECTION_ANCHOR_RE.finditer(body))
    if not matches:
        raise SkillExtractionError(
            f"skill {skill_path} contains no section_id anchors. Expected "
            f"<!-- :: section_id = X :: --> markers on H2 headings."
        )

    target_match = next((m for m in matches if m.group(1) == section_id), None)
    if target_match is None:
        available = sorted({m.group(1) for m in matches})
        raise SkillExtractionError(
            f"section_id {section_id!r} not found in {skill_path}. "
            f"Available section_ids: {available}"
        )

    section_start = target_match.end()
    next_h2 = _NEXT_H2_RE.search(body, pos=section_start)
    section_end = next_h2.start() if next_h2 else len(body)

    return body[section_start:section_end].strip()


def load_pipeline_metadata(skill_path: Path | str) -> Path | None:
    """Resolve the skill's ``.pipeline.yaml`` sidecar path from its frontmatter.

    Looks at the canonical's frontmatter ``pipeline_metadata:`` field:

    - If the field is missing or set to ``"none"``, returns ``None`` (the
      skill has no Composer dispatch).
    - Otherwise interprets the value as a path. Relative paths resolve
      against the skill's parent directory (the typical case is
      ``./skill_<name>.pipeline.yaml`` colocated with the canonical).
    - Returns the resolved absolute path. Does NOT verify the file exists —
      callers (e.g. the loader) decide whether absence is an error.

    Raises:
        SkillExtractionError: skill cannot be read.
    """
    skill_path = Path(skill_path)
    try:
        note = parse_note(skill_path)
    except FrontmatterParseError as e:
        raise SkillExtractionError(
            f"cannot parse skill {skill_path}: {e}"
        ) from e

    raw = note.frontmatter.get("pipeline_metadata")
    if raw is None or (isinstance(raw, str) and raw.strip().lower() == "none"):
        return None

    if not isinstance(raw, str):
        raise SkillExtractionError(
            f"skill {skill_path} has non-string pipeline_metadata: "
            f"{type(raw).__name__}: {raw!r}. Expected a path string or 'none'."
        )

    sidecar = Path(raw.strip())
    if not sidecar.is_absolute():
        sidecar = (skill_path.parent / sidecar).resolve()
    return sidecar


def list_section_ids(skill_path: Path | str) -> list[str]:
    """Return all section_ids declared in a skill canonical, in document order.

    Useful for verifying every sidecar step's ``section_id`` matches an
    anchor in the canonical.
    """
    skill_path = Path(skill_path)
    try:
        note = parse_note(skill_path)
    except FrontmatterParseError as e:
        raise SkillExtractionError(
            f"cannot parse skill {skill_path}: {e}"
        ) from e

    return [m.group(1) for m in _SECTION_ANCHOR_RE.finditer(note.body)]
