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

__version__ = "0.0.1"

__all__ = [
    "__version__",
]
