"""tessellum.format — note format primitives: Building Blocks, YAML
frontmatter spec, parser, validator, link checker."""

from tessellum.format.building_blocks import (
    BB_SPECS,
    BBEdge,
    BBSpec,
    BuildingBlock,
    EPISTEMIC_EDGES,
    EpistemicLayer,
    all_edges_with_navigation_complete,
    downstream,
    get_spec,
    types_in_layer,
    upstream,
)
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
from tessellum.format.parser import (
    FrontmatterParseError,
    Note,
    parse_note,
    parse_text,
)
from tessellum.format.validator import is_valid, validate

__all__ = [
    # Building Blocks
    "BuildingBlock",
    "EpistemicLayer",
    "BBSpec",
    "BBEdge",
    "BB_SPECS",
    "EPISTEMIC_EDGES",
    "all_edges_with_navigation_complete",
    "get_spec",
    "downstream",
    "upstream",
    "types_in_layer",
    # Frontmatter spec
    "VALID_PARA_BUCKETS",
    "VALID_BUILDING_BLOCKS",
    "VALID_STATUSES",
    "REQUIRED_FIELDS",
    "FORBIDDEN_FIELDS",
    "MIN_TAGS_REQUIRED",
    "MIN_KEYWORDS_RECOMMENDED",
    "MIN_TOPICS_RECOMMENDED",
    "DATE_FORMAT_REGEX",
    "TAG_FORMAT_REGEX",
    # Parser
    "Note",
    "parse_note",
    "parse_text",
    "FrontmatterParseError",
    # Issue + validator + link checker
    "Issue",
    "Severity",
    "validate",
    "is_valid",
    "check_links",
]
