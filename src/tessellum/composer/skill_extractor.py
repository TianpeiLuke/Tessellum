"""Read step sections from a single-file skill canonical.

A skill is **one** markdown note. Each pipeline step is an H2 section
carrying a ``<!-- :: section_id = X :: -->`` anchor, a fenced
``​```yaml`` **contract block** (the typed step declaration), and prose
(the step's prompt, with ``{{leaf.X}}`` / ``{{upstream.Y}}`` placeholders).
There is no separate ``.pipeline.yaml`` sidecar — contract and prompt live
together in the section, which keeps the skill a first-class typed vault note
and makes cross-file drift impossible.

Public functions:

    load_skill_section(skill_path, section_id) -> str
        The section's full body text (heading excluded; contract block
        included) — the low-level accessor.

    split_contract_and_prompt(section_body) -> (dict | None, str)
        Split a section body into its parsed ``​```yaml`` contract block
        (or ``None`` if the section has no contract block) and the remaining
        prompt prose.

    iter_step_sections(skill_path) -> list[StepSection]
        The step sections in document order — each a
        ``(section_id, contract, prompt)`` triple where ``contract`` is the
        parsed yaml block. Sections with no contract block (Setup,
        Resources, skill_description, …) are skipped — they are prose, not
        pipeline steps.

    list_section_ids(skill_path) -> list[str]
        Every ``section_id`` anchor in document order (steps and prose).

All raise ``SkillExtractionError`` on malformed input.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

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

# A leading fenced ``yaml`` block — the step's typed contract. Anchored to the
# start of the (stripped) section body so only a *leading* block counts as the
# contract; ```yaml examples further down in prompt prose are left untouched.
_CONTRACT_BLOCK_RE = re.compile(
    r"\A```ya?ml\s*\n(?P<body>.*?)\n```[ \t]*(?:\n|\Z)",
    re.DOTALL,
)


class SkillExtractionError(ValueError):
    """Raised when a skill canonical cannot be parsed or a section is missing."""


@dataclass(frozen=True)
class StepSection:
    """One step section of a single-file skill canonical.

    Attributes:
        section_id: The anchor id (e.g. ``"step_2_extract_facets"``).
        contract: The parsed leading ``​```yaml`` contract block (the typed
            step declaration: role, aggregation, depends_on, materializer,
            output_key, expected_output_schema, …).
        prompt: The section prose after the contract block — the step's
            prompt, with ``{{leaf.X}}`` / ``{{upstream.Y}}`` placeholders
            resolved at execution time.
    """

    section_id: str
    contract: dict
    prompt: str


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


def split_contract_and_prompt(section_body: str) -> tuple[dict | None, str]:
    """Split a section body into its leading yaml contract block + prompt prose.

    Args:
        section_body: The body of a step section (heading excluded), as
            returned by :func:`load_skill_section`.

    Returns:
        ``(contract, prompt)`` where ``contract`` is the parsed mapping from
        the leading ``​```yaml`` fence (or ``None`` if the section has no
        leading contract block — i.e. it is prose, not a pipeline step), and
        ``prompt`` is the remaining prose after the block, stripped.

    Raises:
        SkillExtractionError: the leading yaml block is not valid YAML or is
            not a mapping.
    """
    stripped = section_body.lstrip()
    m = _CONTRACT_BLOCK_RE.match(stripped)
    if m is None:
        return None, section_body.strip()

    raw_block = m.group("body")
    try:
        contract = yaml.safe_load(raw_block)
    except yaml.YAMLError as e:
        raise SkillExtractionError(
            f"step contract block is not valid YAML: {e}"
        ) from e
    if not isinstance(contract, dict):
        raise SkillExtractionError(
            f"step contract block must be a mapping; got "
            f"{type(contract).__name__}"
        )

    prompt = stripped[m.end():].strip()
    return contract, prompt


def iter_step_sections(skill_path: Path | str) -> list[StepSection]:
    """Return the pipeline step sections of a skill, in document order.

    A section is a *step* iff it has a leading ``​```yaml`` contract block.
    Prose-only sections (Setup, Resources, skill_description, …) are skipped.

    Raises:
        SkillExtractionError: skill cannot be read, or a step's contract
            block is malformed.
    """
    skill_path = Path(skill_path)
    steps: list[StepSection] = []
    for section_id in list_section_ids(skill_path):
        body = load_skill_section(skill_path, section_id)
        contract, prompt = split_contract_and_prompt(body)
        if contract is None:
            continue  # prose section, not a pipeline step
        steps.append(
            StepSection(section_id=section_id, contract=contract, prompt=prompt)
        )
    return steps


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
