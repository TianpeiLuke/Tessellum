"""Decision-tree router across the five retrieval surfaces.

The ``skill_tessellum_search_notes`` canonical encodes a decision tree
in markdown for an LLM agent. This module provides the same logic as a
plain Python function so non-agent callers (CI scripts, ablation tests,
the agent runtime once Composer ships) can use it without rendering the
canonical.

Five surfaces, ranked by specificity (most specific → most general):

    1. metadata    "show me all concept notes"
                   ⇢ tessellum.retrieval.metadata_search
    2. bfs         "what links to <seed_note>?"
                   ⇢ tessellum.retrieval.best_first_bfs
    3. bm25        "find the term <exact_token>"
                   ⇢ tessellum.retrieval.bm25_search
    4. dense       "explain the relationship between X and Y"
                   ⇢ tessellum.retrieval.dense_search
    5. hybrid      anything else (default)
                   ⇢ tessellum.retrieval.hybrid_search

The router is **heuristic** — short of a full intent classifier, simple
regex / structural cues route the query. Users (and Composer) can
override by calling the primitive directly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from tessellum.retrieval.bm25 import BM25Hit, bm25_search
from tessellum.retrieval.dense import DenseHit, dense_search
from tessellum.retrieval.graph import GraphHit, best_first_bfs
from tessellum.retrieval.hybrid import HybridHit, hybrid_search
from tessellum.retrieval.metadata import MetadataHit, metadata_search

Strategy = Literal["metadata", "bfs", "bm25", "dense", "hybrid"]

# A query that is just a vault-relative .md path → BFS from that seed.
_NOTE_PATH_RE = re.compile(r"^[a-z0-9_/\-]+\.md$", re.IGNORECASE)

# A query that is a single token (no spaces, ≤ 30 chars, identifier-like)
# → BM25 lexical lookup. Beyond ~30 chars it's almost always a phrase.
_SINGLE_TOKEN_RE = re.compile(r"^[a-z0-9_\-]{1,30}$", re.IGNORECASE)

# Trailing-question-mark questions are usually multi-hop / conceptual
# → hybrid (the default). Cheap heuristic; not load-bearing.


@dataclass(frozen=True)
class RouterDecision:
    """The router's classification of a query.

    Attributes:
        strategy: Which retrieval surface to use.
        reason: Short human-readable explanation of why this strategy
            was picked. Useful for debugging and for the agent
            consuming the search-notes skill.
    """

    strategy: Strategy
    reason: str


def classify_query(query: str) -> RouterDecision:
    """Heuristic intent classification: query → recommended strategy.

    Pure function; no DB access. Returns a ``RouterDecision`` the agent
    (or programmatic caller) can act on. Override by calling the
    primitive directly when intent is mis-classified.
    """
    q = query.strip()
    if not q:
        return RouterDecision("hybrid", "empty query — falling back to hybrid")

    # 1. Vault-relative .md path → graph traversal from a seed.
    if _NOTE_PATH_RE.match(q) and "/" in q:
        return RouterDecision("bfs", f"query looks like a vault path: {q!r}")

    # 2. Single token / identifier → BM25 lexical lookup.
    if _SINGLE_TOKEN_RE.match(q):
        return RouterDecision(
            "bm25",
            f"single token {q!r}: lexical retrieval beats fusion overhead",
        )

    # 3. Question mark / sentence-shaped → hybrid (semantic + lexical).
    if q.endswith("?") or len(q.split()) >= 4:
        return RouterDecision(
            "hybrid",
            "multi-word / question-shaped: hybrid wins on real answer-quality",
        )

    # 4. Otherwise → hybrid (the default — Wave 3's +12pp winner).
    return RouterDecision("hybrid", "default: hybrid covers most cases")


def route(
    db_path: Path | str,
    query: str,
    *,
    k: int = 20,
) -> tuple[
    RouterDecision,
    list[BM25Hit] | list[DenseHit] | list[HybridHit] | list[GraphHit] | list[MetadataHit],
]:
    """Classify ``query`` and dispatch to the recommended retrieval surface.

    Returns:
        ``(decision, hits)`` — the router's classification *and* the
        returned hits. Caller can render both: the decision is useful
        feedback ("we ran BM25 because…"); the hits are the actual
        results.

    Raises:
        FileNotFoundError: ``db_path`` doesn't exist.
        sqlite3.OperationalError: index missing required tables.
    """
    decision = classify_query(query)

    if decision.strategy == "bfs":
        hits = best_first_bfs(db_path, query, k=k)
    elif decision.strategy == "bm25":
        hits = bm25_search(db_path, query, k=k)
    elif decision.strategy == "dense":
        hits = dense_search(db_path, query, k=k)
    elif decision.strategy == "metadata":
        # The router never picks metadata for free-text queries — it's
        # invoked when the caller has structured filters in hand. Kept
        # in the union for completeness so route()'s return type
        # documents all five surfaces.
        hits = metadata_search(db_path, k=k)
    else:  # hybrid
        hits = hybrid_search(db_path, query, k=k)

    return decision, hits


__all__ = ["Strategy", "RouterDecision", "classify_query", "route"]
