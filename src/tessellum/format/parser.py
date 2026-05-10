"""Parse a Tessellum note from disk into a typed ``Note`` value.

Thin wrapper over ``python-frontmatter`` (already a dependency). Surfaces the
two structural pieces — frontmatter dict + body string — plus convenience
accessors for the most-queried fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import frontmatter


class FrontmatterParseError(ValueError):
    """Raised when a note's frontmatter cannot be parsed as a YAML mapping."""


@dataclass(frozen=True)
class Note:
    """A parsed Tessellum note.

    Attributes:
        path: Source path on disk. ``None`` if parsed from a string.
        frontmatter: YAML frontmatter as a dict. Empty dict if no frontmatter.
        body: Markdown body (everything after the closing ``---``).
    """

    path: Path | None
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @property
    def tags(self) -> list[str]:
        raw = self.frontmatter.get("tags")
        if not isinstance(raw, list):
            return []
        return [str(t) for t in raw]

    @property
    def para_bucket(self) -> str | None:
        tags = self.tags
        return tags[0] if tags else None

    @property
    def second_category(self) -> str | None:
        tags = self.tags
        return tags[1] if len(tags) >= 2 else None

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
        post = frontmatter.load(str(p))
    except Exception as e:
        raise FrontmatterParseError(f"failed to parse frontmatter in {p}: {e}") from e
    fm = dict(post.metadata) if post.metadata else {}
    return Note(path=p, frontmatter=fm, body=post.content or "")


def parse_text(text: str) -> Note:
    """Parse a note from an in-memory string. Useful for tests + library callers."""
    try:
        post = frontmatter.loads(text)
    except Exception as e:
        raise FrontmatterParseError(f"failed to parse frontmatter: {e}") from e
    fm = dict(post.metadata) if post.metadata else {}
    return Note(path=None, frontmatter=fm, body=post.content or "")
