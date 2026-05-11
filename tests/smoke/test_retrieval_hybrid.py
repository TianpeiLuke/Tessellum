"""Smoke tests for tessellum.retrieval.hybrid_search.

Tests reuse a module-scoped indexed DB to avoid re-loading the
sentence-transformers model per test (~1.5s amortized over the file).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.indexer import build
from tessellum.retrieval import HybridHit, hybrid_search
from tessellum.retrieval.hybrid import DEFAULT_RRF_K1


_NOTE_TEMPLATE = """\
---
tags:
  - resource
  - terminology
keywords:
  - alpha
  - beta
  - gamma
topics:
  - X
  - Y
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
---

# {name}

{body}
"""


def _make_note(name: str, body: str) -> str:
    return _NOTE_TEMPLATE.format(name=name, body=body)


@pytest.fixture(scope="module")
def hybrid_db(tmp_path_factory):
    """A vault with both lexical-favoring and semantic-favoring matches."""
    tmp_path = tmp_path_factory.mktemp("hybrid")
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)

    # Note A: lexically explicit about graphs, semantically about graphs.
    (v / "resources/term_dictionary/term_graphs.md").write_text(
        _make_note(
            "Graph Theory",
            "Graph theory studies pairwise relationships. Vertices, edges, "
            "and networks. Used in dependency analysis and PageRank.",
        )
    )
    # Note B: lexically about something else, semantically related to graphs.
    (v / "resources/term_dictionary/term_networks.md").write_text(
        _make_note(
            "Network Topology",
            "Topology describes how nodes connect. Star, mesh, ring "
            "configurations. Foundational to distributed systems.",
        )
    )
    # Note C: lexically uses 'graph' but semantically unrelated.
    (v / "resources/term_dictionary/term_visualization.md").write_text(
        _make_note(
            "Data Visualization",
            "A bar graph or line chart converts data to visual form. "
            "Tools include matplotlib, seaborn, plotly.",
        )
    )
    # Note D: completely unrelated.
    (v / "resources/term_dictionary/term_cooking.md").write_text(
        _make_note(
            "Cooking",
            "Cooking applies heat to food. Sauteing, roasting, braising.",
        )
    )

    db_path = tmp_path / "test.db"
    build(v, db_path, with_dense=True)
    return db_path


def test_hybrid_search_returns_typed_hits(hybrid_db):
    hits = hybrid_search(hybrid_db, "graphs vertices networks")
    assert isinstance(hits, list)
    assert all(isinstance(h, HybridHit) for h in hits)


def test_hybrid_search_score_higher_when_in_both_rankers(hybrid_db):
    """A document in BOTH rankers' top-K should outrank docs in only one."""
    hits = hybrid_search(hybrid_db, "graph theory pairwise relationships")
    # The most strongly matching note should appear in both lists.
    in_both = [h for h in hits if h.bm25_rank is not None and h.dense_rank is not None]
    in_one = [h for h in hits if (h.bm25_rank is None) != (h.dense_rank is None)]
    if in_both and in_one:
        # The "in both" note's score should equal or exceed any "in one" note's.
        assert min(h.score for h in in_both) >= max(h.score for h in in_one)


def test_hybrid_search_rrf_score_formula(hybrid_db):
    """RRF score = sum of 1/(k1 + rank) from each ranker."""
    hits = hybrid_search(hybrid_db, "graph theory", k=10)
    for h in hits:
        expected = 0.0
        if h.bm25_rank is not None:
            expected += 1.0 / (DEFAULT_RRF_K1 + h.bm25_rank)
        if h.dense_rank is not None:
            expected += 1.0 / (DEFAULT_RRF_K1 + h.dense_rank)
        assert abs(h.score - expected) < 1e-9, (
            f"score mismatch for {h.note_name}: got {h.score}, expected {expected}"
        )


def test_hybrid_search_scores_descend(hybrid_db):
    hits = hybrid_search(hybrid_db, "graphs")
    for i in range(1, len(hits)):
        assert hits[i - 1].score >= hits[i].score


def test_hybrid_search_k_limits_results(hybrid_db):
    hits = hybrid_search(hybrid_db, "graphs", k=2)
    assert len(hits) <= 2


def test_hybrid_search_k_zero_returns_empty(hybrid_db):
    hits = hybrid_search(hybrid_db, "graphs", k=0)
    assert hits == []


def test_hybrid_search_includes_bm25_rank_when_in_bm25(hybrid_db):
    """Notes with the literal token should surface in BM25 → bm25_rank set."""
    hits = hybrid_search(hybrid_db, "graph")
    bm25_ranked = [h for h in hits if h.bm25_rank is not None]
    assert bm25_ranked, "expected at least one BM25-ranked hit for 'graph'"


def test_hybrid_search_includes_dense_rank_when_in_dense(hybrid_db):
    """Semantic queries should surface dense ranks."""
    hits = hybrid_search(hybrid_db, "vertices and edges form networks")
    dense_ranked = [h for h in hits if h.dense_rank is not None]
    assert dense_ranked, "expected at least one dense-ranked hit"


def test_hybrid_search_no_dense_index_falls_back_to_bm25(tmp_path):
    """A DB built with --no-dense: hybrid_search returns BM25-only results."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note("Alpha", "alpha body content")
    )
    db = tmp_path / "no_dense.db"
    build(v, db, with_dense=False)
    hits = hybrid_search(db, "alpha")
    assert len(hits) >= 1
    # All hits should have bm25_rank set, dense_rank None.
    for h in hits:
        assert h.bm25_rank is not None
        assert h.dense_rank is None


def test_hybrid_search_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        hybrid_search(tmp_path / "missing.db", "anything")


def test_hybrid_search_per_strategy_k_controls_fetch_breadth(hybrid_db):
    """A larger per_strategy_k pulls more candidates → different fusion outcomes."""
    narrow = hybrid_search(hybrid_db, "graphs", k=10, per_strategy_k=2)
    wide = hybrid_search(hybrid_db, "graphs", k=10, per_strategy_k=20)
    # Wide fetch surfaces ≥ as many hits (more candidates entering the union).
    assert len(wide) >= len(narrow)


def test_hybrid_search_against_real_tessellum_vault():
    """End-to-end on the real vault — verify diversity from both rankers."""
    repo = Path(__file__).resolve().parents[2]
    vault = repo / "vault"
    if not vault.is_dir():
        pytest.skip(f"real vault not found at {vault}")
    db_path = repo / "data" / "tessellum-test-hybrid.db"
    db_path.parent.mkdir(exist_ok=True)
    try:
        build(vault, db_path, force=True, with_dense=True)
        hits = hybrid_search(db_path, "knowledge graph", k=10)
        assert len(hits) >= 1
        # Some hits should have come from BM25, some from dense — that's the
        # whole point of fusion.
        from_bm25 = [h for h in hits if h.bm25_rank is not None]
        from_dense = [h for h in hits if h.dense_rank is not None]
        assert from_bm25, "expected some BM25-contributing hits"
        assert from_dense, "expected some dense-contributing hits"
    finally:
        if db_path.is_file():
            db_path.unlink()
