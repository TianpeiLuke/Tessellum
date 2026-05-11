"""Closed enums + soft minima for Tessellum's YAML frontmatter spec.

Source of truth: ``DEVELOPING.md § YAML Frontmatter Specification``. Update
this module and the spec in lockstep — the validator imports from here, and
the templates exemplify both.

Public surface:
    VALID_PARA_BUCKETS    — tags[0] enum (5 values)
    VALID_BUILDING_BLOCKS — building_block enum (8 values)
    VALID_STATUSES        — status enum (21 values)
    REQUIRED_FIELDS       — the 7 required YAML keys
    MIN_*                 — soft minimums for tags / keywords / topics
"""

from __future__ import annotations

VALID_PARA_BUCKETS: frozenset[str] = frozenset(
    {
        "resource",
        "area",
        "project",
        "archive",
        "entry_point",
    }
)

# Derived from `tessellum.bb.BBType` (v0.0.47+): BBType is the single
# source of truth for the 8 BB types. Keep the local `frozenset[str]`
# alias for back-compat with v0.0.46 consumers that import this name
# directly.
from tessellum.bb.types import VALID_BB_TYPE_VALUES as VALID_BUILDING_BLOCKS  # noqa: E402, F401

VALID_STATUSES: frozenset[str] = frozenset(
    {
        "active",
        "draft",
        "archived",
        "deprecated",
        "superseded",
        "stub",
        "placeholder",
        "template",
        "wip",
        "in_progress",
        "production",
        "proposal",
        "development",
        "planning",
        "legacy",
        "disabled",
        "research",
        "review",
        "pending",
        "completed",
        "cancelled",
    }
)

REQUIRED_FIELDS: tuple[str, ...] = (
    "tags",
    "keywords",
    "topics",
    "language",
    "date of note",
    "status",
    "building_block",
)

MIN_TAGS_REQUIRED: int = 2
MIN_KEYWORDS_RECOMMENDED: int = 3
MIN_TOPICS_RECOMMENDED: int = 2

DATE_FORMAT_REGEX: str = r"^\d{4}-\d{2}-\d{2}$"
TAG_FORMAT_REGEX: str = r"^[a-z0-9_]+$"

FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "note_second_category",
    }
)
