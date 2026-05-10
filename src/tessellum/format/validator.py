"""Validate a Tessellum note against the YAML frontmatter spec.

Public API:
    validate(target)  -> list[Issue]   — full report (errors + warnings + infos)
    is_valid(target)  -> bool          — True iff zero ERROR-severity issues

Issue rule-ID prefixes:
    YAML-010..099   YAML frontmatter rules (presence, type, value)
    YAML-100..199   YAML linkage rules (no wiki/markdown links inside YAML)
    LINK-001..006   Body markdown link rules (see ``link_checker``)
    TESS-001..099   Tessellum-specific rules (folgezettel pair, forbidden fields)
"""

from __future__ import annotations

import re
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
from tessellum.format.issue import Issue, Severity
from tessellum.format.link_checker import check_links
from tessellum.format.parser import Note, parse_note

_REQUIRED_FIELD_RULE_IDS: dict[str, str] = {
    "tags": "YAML-010",
    "keywords": "YAML-020",
    "topics": "YAML-030",
    "language": "YAML-040",
    "date of note": "YAML-050",
    "status": "YAML-060",
    "building_block": "YAML-062",
}

_DATE_RE = re.compile(DATE_FORMAT_REGEX)
_TAG_RE = re.compile(TAG_FORMAT_REGEX)
_WIKI_LINK_RE = re.compile(r"\[\[.*?\]\]")
_MD_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")


def validate(target: Path | str | Note) -> list[Issue]:
    """Validate a Tessellum note. Returns issues in field order; empty = clean."""
    note = target if isinstance(target, Note) else parse_note(target)
    fm = note.frontmatter
    issues: list[Issue] = []

    for field_name, rule_id in _REQUIRED_FIELD_RULE_IDS.items():
        if field_name not in fm:
            issues.append(
                Issue(
                    Severity.ERROR,
                    rule_id,
                    field_name,
                    f"required field '{field_name}' is missing",
                )
            )

    issues.extend(_check_tags(fm.get("tags")))
    issues.extend(
        _check_list_min(
            fm.get("keywords"),
            "keywords",
            MIN_KEYWORDS_RECOMMENDED,
            "YAML-021",
            "YAML-022",
        )
    )
    issues.extend(
        _check_list_min(
            fm.get("topics"),
            "topics",
            MIN_TOPICS_RECOMMENDED,
            "YAML-031",
            "YAML-032",
        )
    )
    issues.extend(
        _check_enum(
            fm.get("building_block"),
            "building_block",
            VALID_BUILDING_BLOCKS,
            "YAML-063",
        )
    )
    issues.extend(_check_enum(fm.get("status"), "status", VALID_STATUSES, "YAML-061"))
    issues.extend(_check_date(fm.get("date of note")))
    issues.extend(_check_folgezettel_pair(fm))
    issues.extend(_check_forbidden(fm))
    issues.extend(_check_yaml_links(note.raw_frontmatter))
    issues.extend(check_links(note))

    return issues


def is_valid(target: Path | str | Note) -> bool:
    """True iff validate() returns no ERROR-severity issues. Warnings + infos allowed."""
    return not any(i.severity is Severity.ERROR for i in validate(target))


def _check_tags(tags: object) -> list[Issue]:
    if tags is None:
        return []
    if not isinstance(tags, list):
        return [
            Issue(
                Severity.ERROR,
                "YAML-011",
                "tags",
                f"must be a list, got {type(tags).__name__}",
            )
        ]
    issues: list[Issue] = []
    if len(tags) < MIN_TAGS_REQUIRED:
        issues.append(
            Issue(
                Severity.ERROR,
                "YAML-012",
                "tags",
                f"must have at least {MIN_TAGS_REQUIRED} entries "
                f"(PARA bucket + second category)",
            )
        )
    elif tags[0] not in VALID_PARA_BUCKETS:
        issues.append(
            Issue(
                Severity.ERROR,
                "YAML-014",
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
                    "YAML-013",
                    f"tags[{i}]",
                    f"must be a string, got {type(tag).__name__}: {tag!r}",
                )
            )
        elif not _TAG_RE.match(tag):
            issues.append(
                Issue(
                    Severity.ERROR,
                    "YAML-015",
                    f"tags[{i}]",
                    f"'{tag}' must be lowercase letters/digits/underscores only",
                )
            )
    return issues


def _check_list_min(
    value: object,
    name: str,
    minimum: int,
    type_rule_id: str,
    count_rule_id: str,
) -> list[Issue]:
    if value is None:
        return []
    if not isinstance(value, list):
        return [
            Issue(
                Severity.ERROR,
                type_rule_id,
                name,
                f"must be a list, got {type(value).__name__}",
            )
        ]
    if len(value) < minimum:
        return [
            Issue(
                Severity.WARNING,
                count_rule_id,
                name,
                f"recommended ≥{minimum} entries; got {len(value)}",
            )
        ]
    return []


def _check_enum(
    value: object,
    name: str,
    allowed: frozenset[str],
    rule_id: str,
) -> list[Issue]:
    if value is None:
        return []
    if not isinstance(value, str):
        return [
            Issue(
                Severity.ERROR,
                rule_id,
                name,
                f"must be a string, got {type(value).__name__}",
            )
        ]
    if value not in allowed:
        return [
            Issue(
                Severity.ERROR,
                rule_id,
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
                "YAML-051",
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
                "TESS-001",
                "folgezettel_parent",
                "folgezettel: is set but folgezettel_parent: is missing "
                "(both-or-neither rule)",
            )
        ]
    if has_parent and not has_fz:
        return [
            Issue(
                Severity.ERROR,
                "TESS-002",
                "folgezettel",
                "folgezettel_parent: is set but folgezettel: is missing "
                "(both-or-neither rule)",
            )
        ]
    return []


def _check_forbidden(fm: dict) -> list[Issue]:
    issues: list[Issue] = []
    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in fm:
            if forbidden == "note_second_category":
                msg = (
                    "field is forbidden — tags[1] is the canonical source of "
                    "truth for second category; the indexer reads it from "
                    "tags[1] automatically"
                )
            else:
                msg = "field is forbidden by the spec"
            issues.append(Issue(Severity.ERROR, "TESS-003", forbidden, msg))
    return issues


def _check_yaml_links(raw_frontmatter: str) -> list[Issue]:
    """YAML-100/101: forbid wiki and markdown links inside YAML field values."""
    if not raw_frontmatter:
        return []
    issues: list[Issue] = []
    for offset, line in enumerate(raw_frontmatter.split("\n"), start=2):
        if _WIKI_LINK_RE.search(line):
            issues.append(
                Issue(
                    Severity.ERROR,
                    "YAML-100",
                    None,
                    f"wiki link [[...]] in YAML at line ~{offset}: {line.strip()}",
                )
            )
        if _MD_LINK_RE.search(line):
            issues.append(
                Issue(
                    Severity.ERROR,
                    "YAML-101",
                    None,
                    f"markdown link [...](...) in YAML at line ~{offset}: "
                    f"{line.strip()}",
                )
            )
    return issues
