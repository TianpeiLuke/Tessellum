"""Validate a Tessellum note against the YAML frontmatter spec.

Public API:
    validate(target)  -> list[Issue]   — full report (errors + warnings)
    is_valid(target)  -> bool          — True iff zero ERROR-severity issues

Closed-enum and soft-minimum constants live in ``frontmatter_spec``; parsing
lives in ``parser``. This module is pure validation — no I/O beyond what
``parse_note`` does when given a path.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from tessellum.format.frontmatter_spec import (
    DATE_FORMAT_REGEX,
    FORBIDDEN_FIELDS,
    MIN_KEYWORDS_RECOMMENDED,
    MIN_TAGS_REQUIRED,
    MIN_TOPICS_RECOMMENDED,
    REQUIRED_FIELDS,
    TAG_FORMAT_REGEX,
    VALID_BUILDING_BLOCKS,
    VALID_PARA_BUCKETS,
    VALID_STATUSES,
)
from tessellum.format.parser import Note, parse_note


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Issue:
    severity: Severity
    field: str | None
    message: str

    def __str__(self) -> str:
        loc = f"[{self.field}]" if self.field else ""
        return f"{self.severity.value.upper()}{loc}: {self.message}"


_DATE_RE = re.compile(DATE_FORMAT_REGEX)
_TAG_RE = re.compile(TAG_FORMAT_REGEX)


def validate(target: Path | str | Note) -> list[Issue]:
    """Validate a Tessellum note. Returns issues in field order; empty = clean.

    Accepts a path (``str`` or ``Path``) or a pre-parsed ``Note``. Errors
    indicate spec violations; warnings indicate soft-minimum shortfalls
    (keywords/topics counts).
    """
    note = target if isinstance(target, Note) else parse_note(target)
    fm = note.frontmatter
    issues: list[Issue] = []

    for field_name in REQUIRED_FIELDS:
        if field_name not in fm:
            issues.append(
                Issue(Severity.ERROR, field_name, f"required field '{field_name}' is missing")
            )

    issues.extend(_check_tags(fm.get("tags")))
    issues.extend(_check_list_min(fm.get("keywords"), "keywords", MIN_KEYWORDS_RECOMMENDED))
    issues.extend(_check_list_min(fm.get("topics"), "topics", MIN_TOPICS_RECOMMENDED))
    issues.extend(_check_enum(fm.get("building_block"), "building_block", VALID_BUILDING_BLOCKS))
    issues.extend(_check_enum(fm.get("status"), "status", VALID_STATUSES))
    issues.extend(_check_date(fm.get("date of note")))
    issues.extend(_check_folgezettel_pair(fm))
    issues.extend(_check_forbidden(fm))

    return issues


def is_valid(target: Path | str | Note) -> bool:
    """True iff validate() returns no ERROR-severity issues. Warnings allowed."""
    return not any(i.severity == Severity.ERROR for i in validate(target))


def _check_tags(tags: object) -> list[Issue]:
    if tags is None:
        return []
    if not isinstance(tags, list):
        return [Issue(Severity.ERROR, "tags", f"must be a list, got {type(tags).__name__}")]
    issues: list[Issue] = []
    if len(tags) < MIN_TAGS_REQUIRED:
        issues.append(
            Issue(
                Severity.ERROR,
                "tags",
                f"must have at least {MIN_TAGS_REQUIRED} entries (PARA bucket + second category)",
            )
        )
    elif tags[0] not in VALID_PARA_BUCKETS:
        issues.append(
            Issue(
                Severity.ERROR,
                "tags[0]",
                f"'{tags[0]}' is not a valid PARA bucket; "
                f"must be one of {sorted(VALID_PARA_BUCKETS)}",
            )
        )
    for i, tag in enumerate(tags):
        if not isinstance(tag, str):
            issues.append(
                Issue(
                    Severity.ERROR,
                    f"tags[{i}]",
                    f"must be a string, got {type(tag).__name__}: {tag!r}",
                )
            )
        elif not _TAG_RE.match(tag):
            issues.append(
                Issue(
                    Severity.ERROR,
                    f"tags[{i}]",
                    f"'{tag}' must be lowercase letters/digits/underscores only",
                )
            )
    return issues


def _check_list_min(value: object, name: str, minimum: int) -> list[Issue]:
    if value is None:
        return []
    if not isinstance(value, list):
        return [Issue(Severity.ERROR, name, f"must be a list, got {type(value).__name__}")]
    if len(value) < minimum:
        return [
            Issue(
                Severity.WARNING,
                name,
                f"recommended ≥{minimum} entries; got {len(value)}",
            )
        ]
    return []


def _check_enum(value: object, name: str, allowed: frozenset[str]) -> list[Issue]:
    if value is None:
        return []
    if not isinstance(value, str):
        return [Issue(Severity.ERROR, name, f"must be a string, got {type(value).__name__}")]
    if value not in allowed:
        return [
            Issue(
                Severity.ERROR,
                name,
                f"'{value}' is not a valid {name}; must be one of {sorted(allowed)}",
            )
        ]
    return []


def _check_date(value: object) -> list[Issue]:
    if value is None:
        return []
    date_str = str(value)
    if not _DATE_RE.match(date_str):
        return [
            Issue(
                Severity.ERROR,
                "date of note",
                f"'{date_str}' must match YYYY-MM-DD",
            )
        ]
    return []


def _check_folgezettel_pair(fm: dict) -> list[Issue]:
    has_fz = "folgezettel" in fm
    has_parent = "folgezettel_parent" in fm or "fz_parent" in fm
    if has_fz and not has_parent:
        return [
            Issue(
                Severity.ERROR,
                "folgezettel_parent",
                "folgezettel: is set but folgezettel_parent: is missing (both-or-neither rule)",
            )
        ]
    if has_parent and not has_fz:
        return [
            Issue(
                Severity.ERROR,
                "folgezettel",
                "folgezettel_parent: is set but folgezettel: is missing (both-or-neither rule)",
            )
        ]
    return []


def _check_forbidden(fm: dict) -> list[Issue]:
    issues: list[Issue] = []
    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in fm:
            if forbidden == "note_second_category":
                msg = (
                    "field is forbidden — tags[1] is the canonical source of truth "
                    "for second category; the indexer reads it from tags[1] automatically"
                )
            else:
                msg = "field is forbidden by the spec"
            issues.append(Issue(Severity.ERROR, forbidden, msg))
    return issues
