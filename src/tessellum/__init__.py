"""Tessellum — typed atomic notes in a graph.

A knowledge-construction system built on six architectural pillars:

  Z      Zettelkasten    — atomic notes with bidirectional links
  PARA   PARA            — Projects / Areas / Resources / Archives organization
  BB     Building Block  — typed atomic units with epistemic functions
  EF     Epistemic Func  — each BB has a defining role (claim, refute, observe, ...)
  DKS    Dialectic       — closed-loop protocol updating warrants from disagreement
  CQRS   CQRS            — typed prescriptive substrate ⊥ computational descriptive retrieval

The package surface lives under sub-modules:

  tessellum.composer   v0.7 typed-contract knowledge auto-digestion pipeline
  tessellum.retrieval  bm25 / dense / ppr / best_first_bfs / hybrid (RRF)
  tessellum.indexer    SQLite + sqlite-vec + FTS5 unified backend
  tessellum.format     YAML frontmatter + note format validation
  tessellum.cli        the `tessellum` command-line entry
  tessellum.mcp        MCP server exposing v0.1 skills as tools

The vault template lives under `vault/`; the user's vault is configured via
the TESSELLUM_VAULT_PATH environment variable or `tessellum.config`.
"""

from tessellum.__about__ import __status__, __version__
from tessellum.format import (
    BB_SPECS,
    BBEdge,
    BBSpec,
    BuildingBlock,
    EPISTEMIC_EDGES,
    EpistemicLayer,
    FrontmatterParseError,
    Issue,
    Note,
    REQUIRED_FIELDS,
    Severity,
    VALID_BUILDING_BLOCKS,
    VALID_PARA_BUCKETS,
    VALID_STATUSES,
    downstream,
    get_spec,
    is_valid,
    parse_note,
    parse_text,
    types_in_layer,
    upstream,
    validate,
)

__all__ = [
    "__status__",
    "__version__",
    # Building Blocks
    "BuildingBlock",
    "EpistemicLayer",
    "BBSpec",
    "BBEdge",
    "BB_SPECS",
    "EPISTEMIC_EDGES",
    "downstream",
    "get_spec",
    "types_in_layer",
    "upstream",
    # Format spec + validator
    "Note",
    "Issue",
    "Severity",
    "validate",
    "is_valid",
    "parse_note",
    "parse_text",
    "FrontmatterParseError",
    "VALID_PARA_BUCKETS",
    "VALID_BUILDING_BLOCKS",
    "VALID_STATUSES",
    "REQUIRED_FIELDS",
]
