"""tessellum.retrieval — query layer for the indexed vault.

System D's read surface. Reads the SQLite DB built by
:func:`tessellum.indexer.build` and answers user queries via one or more
retrieval strategies. Per ``plans/plan_retrieval_port.md``:

  Wave 1 — BM25 (this release, v0.0.13)        ✓
  Wave 2 — Dense + sqlite-vec  (v0.0.14)
  Wave 3 — Hybrid RRF (default; v0.0.15)
  Wave 4 — Best-first BFS (v0.0.16)        — no PPR (FZ 5e2b1c)
  Wave 5 — Skill orchestration (v0.0.17)

Public API (Wave 1):

    bm25_search(db_path, query, *, k=20, snippet_length=30) -> list[BM25Hit]
        Lexical retrieval via SQLite's built-in FTS5. Returns hits ranked
        by descending BM25 score (negation of FTS5's lower-is-better
        convention so users see "higher = more relevant").

    BM25Hit
        Frozen dataclass: note_id, note_name, score, snippet.
"""

from tessellum.retrieval.bm25 import BM25Hit, bm25_search

__all__ = ["bm25_search", "BM25Hit"]
