"""tessellum.retrieval — query layer for the indexed vault.

System D's read surface. Reads the SQLite DB built by
:func:`tessellum.indexer.build` and answers user queries via one or more
retrieval strategies. Per ``plans/plan_retrieval_port.md``:

  Wave 1 — BM25 (v0.0.13)                         ✓
  Wave 2 — Dense + sqlite-vec (this release)      ✓
  Wave 3 — Hybrid RRF (default; v0.0.15)
  Wave 4 — Best-first BFS (v0.0.16)        — no PPR (FZ 5e2b1c)
  Wave 5 — Skill orchestration (v0.0.17)

Public API:

    bm25_search(db_path, query, *, k=20, snippet_length=30) -> list[BM25Hit]
        Lexical retrieval via FTS5. Hits ranked by descending BM25 score.

    dense_search(db_path, query, *, k=20) -> list[DenseHit]
        Semantic retrieval via sqlite-vec. Hits ranked by descending
        cosine similarity (= ascending distance).

    BM25Hit, DenseHit — frozen dataclasses with ``score`` ("higher = better").
"""

from tessellum.retrieval.bm25 import BM25Hit, bm25_search
from tessellum.retrieval.dense import DenseHit, dense_search

__all__ = [
    "bm25_search",
    "BM25Hit",
    "dense_search",
    "DenseHit",
]
