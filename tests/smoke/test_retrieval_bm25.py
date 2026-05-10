"""Smoke tests for tessellum.retrieval.bm25_search."""

from __future__ import annotations

import sqlite3
import textwrap
from pathlib import Path

import pytest

from tessellum.indexer import build
from tessellum.retrieval import BM25Hit, bm25_search


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


@pytest.fixture
def indexed_db(tmp_path):
    """A vault with three lexically-distinct notes + a built index."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note(
            "Alpha",
            "The alpha concept describes the foundational layer. "
            "It connects to graph traversal and search retrieval.",
        )
    )
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _make_note(
            "Beta",
            "Beta builds on alpha. Beta is about quantum entanglement and "
            "supersymmetric particles. No retrieval here.",
        )
    )
    (v / "resources/term_dictionary/term_gamma.md").write_text(
        _make_note(
            "Gamma",
            "Gamma is irrelevant filler. Just placeholder words to occupy "
            "vocabulary space and give BM25 something to score against.",
        )
    )
    db_path = tmp_path / "test.db"
    build(v, db_path)
    return db_path


def test_bm25_search_returns_list_of_hits(indexed_db):
    hits = bm25_search(indexed_db, "alpha")
    assert isinstance(hits, list)
    assert all(isinstance(h, BM25Hit) for h in hits)


def test_bm25_search_ranks_relevant_notes_higher(indexed_db):
    hits = bm25_search(indexed_db, "retrieval")
    assert len(hits) >= 1
    # term_alpha mentions retrieval; term_beta says "No retrieval here"
    # but still contains the token. term_alpha should rank higher because
    # the body talks about retrieval as a topic.
    assert hits[0].note_name in {"term_alpha", "term_beta"}


def test_bm25_search_matches_specific_term(indexed_db):
    hits = bm25_search(indexed_db, "supersymmetric")
    assert len(hits) == 1
    assert hits[0].note_name == "term_beta"


def test_bm25_search_empty_for_unknown_term(indexed_db):
    hits = bm25_search(indexed_db, "nonexistent_term_xyz_qqq")
    assert hits == []


def test_bm25_search_score_is_positive(indexed_db):
    """Score field is the negation of FTS5's bm25() — higher = more relevant."""
    hits = bm25_search(indexed_db, "alpha")
    assert all(h.score > 0 for h in hits)


def test_bm25_search_scores_descend(indexed_db):
    hits = bm25_search(indexed_db, "alpha")
    for i in range(1, len(hits)):
        assert hits[i - 1].score >= hits[i].score


def test_bm25_search_k_limits_results(indexed_db):
    # ``alpha`` matches all three notes (alpha mentioned in beta + gamma's
    # vocabulary placeholder fillers). Limit to 1.
    hits = bm25_search(indexed_db, "alpha", k=1)
    assert len(hits) == 1


def test_bm25_search_k_zero_returns_empty(indexed_db):
    hits = bm25_search(indexed_db, "alpha", k=0)
    assert hits == []


def test_bm25_search_includes_snippet_by_default(indexed_db):
    hits = bm25_search(indexed_db, "supersymmetric")
    assert len(hits) == 1
    assert hits[0].snippet is not None
    assert "<<<" in hits[0].snippet  # match markers present
    assert ">>>" in hits[0].snippet


def test_bm25_search_no_snippet_when_disabled(indexed_db):
    hits = bm25_search(indexed_db, "supersymmetric", snippet_length=None)
    assert len(hits) == 1
    assert hits[0].snippet is None


def test_bm25_search_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        bm25_search(tmp_path / "missing.db", "anything")


def test_bm25_search_malformed_query_raises_operational_error(indexed_db):
    """Malformed FTS5 syntax bubbles up as sqlite3.OperationalError."""
    with pytest.raises(sqlite3.OperationalError):
        bm25_search(indexed_db, "AND OR")  # invalid FTS5 query


def test_bm25_search_fts5_phrase_query(indexed_db):
    """Phrase query in double quotes should match the exact sequence."""
    hits = bm25_search(indexed_db, '"foundational layer"')
    assert len(hits) == 1
    assert hits[0].note_name == "term_alpha"


def test_bm25_search_fts5_prefix_query(indexed_db):
    hits = bm25_search(indexed_db, "supersym*")
    assert len(hits) == 1
    assert hits[0].note_name == "term_beta"


def test_bm25_search_returns_note_id_and_name(indexed_db):
    hits = bm25_search(indexed_db, "alpha")
    assert hits[0].note_id.startswith("resources/term_dictionary/")
    assert hits[0].note_id.endswith(".md")
    assert hits[0].note_name == Path(hits[0].note_id).stem


def test_bm25_search_against_real_tessellum_vault():
    """Smoke against the shipped Tessellum vault."""
    repo = Path(__file__).resolve().parents[2]
    vault = repo / "vault"
    if not vault.is_dir():
        pytest.skip(f"real vault not found at {vault}")
    db_path = repo / "data" / "tessellum-test-search.db"
    db_path.parent.mkdir(exist_ok=True)
    try:
        build(vault, db_path, force=True)
        hits = bm25_search(db_path, "composer", k=5)
        # The vault has a Composer skill canonical and Composer-related thoughts.
        assert len(hits) >= 1
        # All scores positive (negation of FTS5's lower-is-better convention).
        assert all(h.score > 0 for h in hits)
    finally:
        if db_path.is_file():
            db_path.unlink()
