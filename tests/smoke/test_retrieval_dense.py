"""Smoke tests for tessellum.retrieval.dense_search.

Tests that need an embedding model run sentence-transformers in-process
(it's a core dependency). First test loads the model (~1.5s); subsequent
tests reuse the module-level singleton.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.indexer import build
from tessellum.retrieval import DenseHit, dense_search


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
def indexed_db(tmp_path_factory):
    """Build once per module — embedding generation is the slow path."""
    tmp_path = tmp_path_factory.mktemp("dense")
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_graphs.md").write_text(
        _make_note(
            "Graph Theory",
            "Graph theory studies pairwise relationships between objects. "
            "Vertices and edges form networks. Used in network analysis, "
            "social graphs, and dependency resolution.",
        )
    )
    (v / "resources/term_dictionary/term_cooking.md").write_text(
        _make_note(
            "Cooking",
            "Cooking is the art of preparing food using heat. Involves "
            "selecting ingredients, applying techniques like sauteing, "
            "roasting, and braising. Practiced in kitchens worldwide.",
        )
    )
    (v / "resources/term_dictionary/term_networks.md").write_text(
        _make_note(
            "Computer Networks",
            "Computer networks connect devices via wired or wireless links. "
            "TCP/IP, routing protocols, packet switching. Foundational to "
            "modern internet infrastructure.",
        )
    )
    db_path = tmp_path / "test.db"
    build(v, db_path, with_dense=True)
    return db_path


def test_dense_search_returns_typed_hits(indexed_db):
    hits = dense_search(indexed_db, "graphs and edges")
    assert isinstance(hits, list)
    assert all(isinstance(h, DenseHit) for h in hits)


def test_dense_search_ranks_semantically_similar_first(indexed_db):
    """A query about graphs should rank graph-related notes highest."""
    hits = dense_search(indexed_db, "graph theory networks vertices")
    assert len(hits) >= 1
    # The graph note should rank first; cooking should rank last.
    # We allow some flex because all-MiniLM-L6-v2 isn't perfect on tiny
    # corpora — but graph >> cooking on a graph query is robust.
    note_names = [h.note_name for h in hits]
    cooking_idx = note_names.index("term_cooking") if "term_cooking" in note_names else len(hits)
    graphs_idx = note_names.index("term_graphs") if "term_graphs" in note_names else len(hits)
    assert graphs_idx < cooking_idx


def test_dense_search_separates_topics(indexed_db):
    """A cooking query should rank cooking note higher than graph note."""
    hits = dense_search(indexed_db, "preparing food in the kitchen")
    note_names = [h.note_name for h in hits]
    cooking_idx = note_names.index("term_cooking") if "term_cooking" in note_names else len(hits)
    graphs_idx = note_names.index("term_graphs") if "term_graphs" in note_names else len(hits)
    assert cooking_idx < graphs_idx


def test_dense_search_score_is_cosine_similarity(indexed_db):
    """With distance_metric=cosine, score = 1 - distance ∈ [-1, 1]."""
    hits = dense_search(indexed_db, "graphs")
    assert hits, "expected at least one hit"
    for h in hits:
        assert -1.0 <= h.score <= 1.0
        assert -1.0 <= h.distance <= 2.0  # cosine distance is in [0, 2]


def test_dense_search_scores_descend(indexed_db):
    hits = dense_search(indexed_db, "graphs")
    for i in range(1, len(hits)):
        assert hits[i - 1].score >= hits[i].score


def test_dense_search_distance_ascends(indexed_db):
    """Distance is the inverse of score — should go up as score goes down."""
    hits = dense_search(indexed_db, "graphs")
    for i in range(1, len(hits)):
        assert hits[i - 1].distance <= hits[i].distance


def test_dense_search_k_limits_results(indexed_db):
    hits = dense_search(indexed_db, "graphs", k=1)
    assert len(hits) == 1


def test_dense_search_k_zero_returns_empty(indexed_db):
    hits = dense_search(indexed_db, "graphs", k=0)
    assert hits == []


def test_dense_search_returns_paths_correctly(indexed_db):
    hits = dense_search(indexed_db, "graphs")
    for h in hits:
        assert h.note_id.endswith(".md")
        assert h.note_name == Path(h.note_id).stem


def test_dense_search_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        dense_search(tmp_path / "missing.db", "anything")


def test_dense_search_no_dense_index_returns_empty(tmp_path):
    """A DB built with --no-dense has the notes_vec table (created by
    schema.sql) but no rows in it. Query returns empty results — honest
    "no matches" behavior, not an error."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note("Alpha", "alpha body")
    )
    db = tmp_path / "no_dense.db"
    build(v, db, with_dense=False)
    hits = dense_search(db, "anything")
    assert hits == []


def test_build_with_dense_false_skips_embeddings(tmp_path):
    """`with_dense=False` should populate notes + notes_fts but NOT notes_vec."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note("Alpha", "body")
    )
    db = tmp_path / "no_dense.db"
    result = build(v, db, with_dense=False)
    assert result.notes_indexed == 1
    assert result.embeddings_generated == 0


def test_build_with_dense_true_populates_embeddings(indexed_db):
    """`with_dense=True` populates notes_vec — verified by querying."""
    hits = dense_search(indexed_db, "graphs")
    assert len(hits) >= 1


def test_dense_search_against_real_tessellum_vault():
    """Smoke against the shipped Tessellum vault (with embeddings)."""
    repo = Path(__file__).resolve().parents[2]
    vault = repo / "vault"
    if not vault.is_dir():
        pytest.skip(f"real vault not found at {vault}")
    db_path = repo / "data" / "tessellum-test-dense.db"
    db_path.parent.mkdir(exist_ok=True)
    try:
        build(vault, db_path, force=True, with_dense=True)
        hits = dense_search(db_path, "knowledge organization", k=5)
        assert len(hits) >= 1
        # All returned hits should have score < 1 (not perfect identity)
        # and distance > 0.
        assert all(h.score < 1.0 for h in hits)
        assert all(h.distance > 0 for h in hits)
    finally:
        if db_path.is_file():
            db_path.unlink()
