"""Markdown-link checks for note bodies (LINK-001..006).

Rules:
    LINK-001  internal link missing ``.md`` extension
    LINK-002  internal link uses an absolute path (prefer relative)
    LINK-003  internal link target does not exist on disk
    LINK-006  note has no internal links to other notes (orphan)

Skipped (not flagged):
    - external links (``http://``, ``https://``, ``mailto:``)
    - anchor-only links (``#section``)
    - non-markdown extensions (images, pdfs, code, archives, ...)
    - placeholder targets (``<placeholder>``, ``link``, ``...``, ``-``, ...)
    - directory links (ending in ``/``)
    - links inside fenced code blocks
"""

from __future__ import annotations

import re

from tessellum.format.issue import Issue, Severity
from tessellum.format.parser import Note

_FENCED_CODE_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_EXTERNAL_RE = re.compile(r"^https?://", re.IGNORECASE)

_NON_MD_EXTS: frozenset[str] = frozenset(
    {
        # Images
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
        # Documents
        ".pdf", ".docx", ".xlsx", ".pptx", ".csv",
        # Code + data
        ".py", ".sh", ".sql", ".json", ".yaml", ".yml",
        ".xml", ".html", ".txt", ".zip", ".ipynb",
        # Configuration
        ".toml", ".cfg", ".ini", ".lock", ".env",
        # LaTeX + bibliography
        ".drawio", ".tex", ".bib", ".sty", ".cls",
    }
)

_PLACEHOLDER_TARGETS: frozenset[str] = frozenset(
    {
        "-", "link", "path", "url", "ticket_link",
        "ticket_query_link", "source", "target",
        "...", ".*?",
    }
)


def check_links(note: Note) -> list[Issue]:
    """Validate markdown links in the body. Empty body or pure-frontmatter
    notes are still checked for orphan status (LINK-006)."""
    issues: list[Issue] = []
    body_no_code = _FENCED_CODE_RE.sub("", note.body)

    has_internal_md_link = False

    for m in _LINK_RE.finditer(body_no_code):
        target = m.group(2).strip()

        if _EXTERNAL_RE.match(target):
            continue
        if target.startswith(("mailto:", "#")):
            continue

        path_part = target.split("#", 1)[0]

        if not path_part:
            continue
        if any(path_part.lower().endswith(ext) for ext in _NON_MD_EXTS):
            continue
        if path_part.endswith("/"):
            continue
        if path_part.lower() in _PLACEHOLDER_TARGETS:
            continue
        if path_part.startswith(("<", "{", "_no_")):
            continue

        if not path_part.endswith(".md"):
            issues.append(
                Issue(
                    Severity.WARNING,
                    "LINK-001",
                    "links",
                    f"internal link '{target}' is missing .md extension",
                )
            )
            continue

        if path_part.startswith("/"):
            issues.append(
                Issue(
                    Severity.WARNING,
                    "LINK-002",
                    "links",
                    f"internal link '{target}' uses an absolute path; "
                    f"prefer relative paths",
                )
            )

        has_internal_md_link = True

        if note.path is not None and not path_part.startswith("/"):
            try:
                resolved = (note.path.parent / path_part).resolve()
            except (OSError, ValueError):
                resolved = None
            if resolved is not None and not resolved.exists():
                issues.append(
                    Issue(
                        Severity.WARNING,
                        "LINK-003",
                        "links",
                        f"link target '{target}' does not exist",
                    )
                )

    if not has_internal_md_link:
        # Templates are orphans by design — they're scaffolds with
        # placeholder content meant to be copied + filled in. Skip
        # LINK-006 for status=template, matching TESS-004's authoring-
        # state exemption pattern.
        status = note.frontmatter.get("status")
        if status != "template":
            issues.append(
                Issue(
                    Severity.WARNING,
                    "LINK-006",
                    "links",
                    "note has no internal links to other notes (orphan)",
                )
            )

    return issues
