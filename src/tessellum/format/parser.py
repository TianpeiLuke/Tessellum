"""Parse a Tessellum note from disk into a typed ``Note`` value.

Lightweight regex-based frontmatter parser using PyYAML directly. Captures
the raw frontmatter text in addition to the parsed mapping so downstream
checks can scan the YAML source (e.g. for forbidden wiki/markdown links
inside field values).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class FrontmatterParseError(ValueError):
    """Raised when a note's frontmatter cannot be parsed as a YAML mapping."""


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


@dataclass(frozen=True)
class Note:
    """A parsed Tessellum note.

    Attributes:
        path:             Source path on disk; ``None`` if parsed from a string.
        frontmatter:      YAML frontmatter as a dict (empty if absent).
        body:             Markdown body — everything after the closing ``---``.
        raw_frontmatter:  Original YAML text between ``---`` fences. Empty
                          string if the note has no frontmatter. Preserved so
                          checks can scan the raw YAML (e.g. for link prohibition).
    """

    path: Path | None
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""
    raw_frontmatter: str = ""

    @property
    def tags(self) -> list[str]:
        raw = self.frontmatter.get("tags")
        if not isinstance(raw, list):
            return []
        return [str(t) for t in raw]

    @property
    def para_bucket(self) -> str | None:
        return self.tags[0] if self.tags else None

    @property
    def second_category(self) -> str | None:
        return self.tags[1] if len(self.tags) >= 2 else None

    @property
    def building_block(self) -> str | None:
        v = self.frontmatter.get("building_block")
        return str(v) if v is not None else None

    @property
    def status(self) -> str | None:
        v = self.frontmatter.get("status")
        return str(v) if v is not None else None

    @property
    def folgezettel(self) -> str | None:
        v = self.frontmatter.get("folgezettel")
        return str(v) if v is not None else None

    @property
    def folgezettel_parent(self) -> str | None:
        v = self.frontmatter.get("folgezettel_parent")
        if v is None:
            v = self.frontmatter.get("fz_parent")
        return str(v) if v is not None else None


def parse_note(path: Path | str) -> Note:
    """Parse a note from a file path."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as e:
        raise FrontmatterParseError(f"cannot read {p}: {e}") from e
    parsed = parse_text(text)
    return Note(
        path=p,
        frontmatter=parsed.frontmatter,
        body=parsed.body,
        raw_frontmatter=parsed.raw_frontmatter,
    )


def parse_text(text: str) -> Note:
    """Parse a note from an in-memory string."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return Note(path=None, frontmatter={}, body=text, raw_frontmatter="")

    raw = m.group(1)
    body = m.group(2)
    try:
        fm = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise FrontmatterParseError(f"YAML parse error: {e}") from e

    if fm is None:
        fm = {}
    if not isinstance(fm, dict):
        raise FrontmatterParseError(
            f"frontmatter is not a YAML mapping (got {type(fm).__name__})"
        )

    return Note(path=None, frontmatter=fm, body=body, raw_frontmatter=raw)
