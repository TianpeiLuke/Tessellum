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

# Derived from `tessellum.bb.BBType`: BBType is the single source of
# truth for the 8 BB types. The local ``frozenset[str]`` alias is the
# value-level view consumers import for membership checks.
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

# ── One vault frontmatter contract (P19, FZ 20k9c1a1a1b7c2g) ──────────────────
# This module is the SINGLE SOURCE OF TRUTH for the vault's frontmatter contract
# (authoritative spec: DEVELOPING.md § YAML Frontmatter). Before P19 the same
# contract was hand-maintained in FOUR places that had drifted: this validator,
# each eval slice's golden_facts.json, the execute skill's OUTPUT FORMAT prose,
# and score.py's N1/N2 — so the scorer and the shipped validator could return
# OPPOSITE verdicts on the same note. The eval + scorer now derive from here.
#
# The digestion pipeline's OUTPUT is a vault note like any other — there is ONE
# standard, not a separate "digestion spec". The prior golden facts diverged by
# ERROR, not by scope: they wrongly FORBADE `folgezettel` (a legitimate optional
# trail field, DEVELOPING.md §145-172) and `last_updated`/`author`/`related_wiki`
# (explicit OPTIONAL common fields, §135-141), and wrongly REQUIRED `source_url`
# universally (it is type-specific — required only for documentation notes). P19
# corrects the golden to derive from this contract.

# Legacy / parent-vault junk keys that must NEVER appear on a Tessellum note
# (Obsidian defaults + renamed fields). `note_second_category` is folded into
# tags[1]; `last_updated` is the canonical name (not `updated`); etc.
FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "note_second_category",  # → tags[1]
        "title",                 # → the H1
        "category",              # → tags
        "created",               # → "date of note"
        "updated",               # → "last_updated"
        "source",                # → "source_url"
        "parent",                # → "folgezettel_parent"
    }
)

# Optional COMMON fields any note may carry (DEVELOPING.md §135-141) — NOT
# required, NOT forbidden. Listed so a stricter consumer (the eval) knows these
# are permitted rather than treating their presence as a violation.
OPTIONAL_COMMON_FIELDS: frozenset[str] = frozenset(
    {
        "last_updated",
        "author",
        "related_wiki",
        "access_control_group",  # vault access tag; recommended, not universally required
    }
)

# Optional TYPE-SPECIFIC required fields: required for the named note flavors,
# omitted otherwise (DEVELOPING.md §143). Keyed by tags[1] second-category /
# flavor. A documentation note derived from an external source MUST carry
# `source_url`; a term note need not.
TYPE_SPECIFIC_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "documentation": ("source_url",),
    "aws_docs": ("source_url",),
    "dev_tool_docs": ("source_url",),
}


def required_fields_for(second_category: str | None = None) -> tuple[str, ...]:
    """The required frontmatter keys for a note of the given ``tags[1]``
    second-category — the 7 universal fields plus any type-specific ones
    (P19 single-source). ``None`` → the universal 7."""
    base = REQUIRED_FIELDS
    extra = TYPE_SPECIFIC_REQUIRED_FIELDS.get(second_category or "", ())
    return base + extra
