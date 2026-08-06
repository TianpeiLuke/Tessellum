"""Parse a Tessellum note from disk or memory into a typed :class:`Note`.

A lightweight regex-based frontmatter parser over PyYAML. Captures the
raw frontmatter text in addition to the parsed mapping so downstream
checks can scan the YAML source (e.g. for forbidden wiki/markdown
links inside field values).

Public API:

- :func:`parse_note` — read + parse a file from disk.
- :func:`parse_text` — parse an in-memory string.
- :class:`Note` — typed result with ``frontmatter``, ``body``, and
  ``raw_frontmatter`` plus convenience properties for the common
  fields (``tags``, ``building_block``, ``folgezettel``, etc.).
- :class:`FrontmatterParseError` — raised when frontmatter can't be
  parsed as a YAML mapping.
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

# A Folgezettel ID is a prefix encoding: each parent→child step appends one
# segment, and the segment alternates class (a run of digits, then a run of
# letters, then digits, …). So the parent is the ID minus its trailing segment
# — a pure substring. See derive_folgezettel_parent.
_FZ_LAST_SEGMENT_RE = re.compile(r"([0-9]+|[a-z]+)$")


def derive_folgezettel_parent(fz: str | None) -> str | None:
    """Return the parent Folgezettel of ``fz``, derived from its prefix.

    The Folgezettel ID *is* the trail path: ``20`` → ``20l`` → ``20l2`` →
    ``20l2a``. Each child appends one segment — a maximal run of digits or of
    letters — and the class alternates at each step (digit↔letter boundary). The
    parent is therefore ``fz`` with its trailing segment removed, a pure
    substring; no separate ``folgezettel_parent`` field is needed.

    Examples: ``20l2`` → ``20l``; ``20l`` → ``20``; ``9h10`` → ``9h``;
    ``9h`` → ``9``. A single-segment (root) ID such as ``20`` or ``9`` has no
    parent → ``None``. ``None``/empty in → ``None`` out.
    """
    if not fz:
        return None
    m = _FZ_LAST_SEGMENT_RE.search(fz)
    if not m:
        return None
    parent = fz[: m.start()]
    return parent or None


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
        """The parent Folgezettel, DERIVED from this note's ``folgezettel``
        prefix (see :func:`derive_folgezettel_parent`).

        ``folgezettel_parent``/``fz_parent`` is no longer an authored YAML field
        — it is redundant with the prefix-encoded ID. A stray one in the
        frontmatter is ignored; the derived value is authoritative.
        """
        return derive_folgezettel_parent(self.folgezettel)


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
