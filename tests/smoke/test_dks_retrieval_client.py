"""Smoke tests for tessellum.dks.RetrievalClient (Phase 4).

The client is a thin adapter over ``tessellum.retrieval.hybrid_search``;
these tests build a small indexed vault, run a few searches, and
confirm:

  - Construction validates the DB path (FileNotFoundError on missing)
  - Hits map cleanly from HybridHit → RetrievalHit (typed boundary)
  - k=0 returns an empty list (no LLM / no network)
  - The class exposes no mutating surface (R-Cross defensive half)
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.dks import RetrievalClient, RetrievalHit
from tessellum.indexer import build


_NOTE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - terminology
    keywords:
      - {kw}
      - alpha
      - beta
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: concept
    ---

    # {title}

    This is the body of {title}, talking about {kw}.
    """
)


@pytest.fixture
def indexed_db(tmp_path):
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _NOTE.format(title="Alpha", kw="alpha")
    )
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _NOTE.format(title="Beta", kw="beta")
    )
    db = tmp_path / "tess.db"
    build(v, db, with_dense=False)
    return db


# ── construction ────────────────────────────────────────────────────────────


def test_client_missing_db_raises_file_not_found(tmp_path):
    """R-Cross defensive: construction fails loudly if no index DB."""
    with pytest.raises(FileNotFoundError, match="index DB not found"):
        RetrievalClient(tmp_path / "missing.db")


def test_client_accepts_str_and_path(indexed_db):
    c1 = RetrievalClient(str(indexed_db))
    c2 = RetrievalClient(indexed_db)
    assert c1.db_path == c2.db_path == indexed_db


# ── search ──────────────────────────────────────────────────────────────────


def test_search_returns_retrieval_hits(indexed_db):
    client = RetrievalClient(indexed_db)
    hits = client.search("alpha", k=5)
    assert all(isinstance(h, RetrievalHit) for h in hits)


def test_search_returns_at_least_one_hit_for_indexed_term(indexed_db):
    client = RetrievalClient(indexed_db)
    hits = client.search("alpha", k=5)
    note_names = {h.note_name for h in hits}
    assert "term_alpha" in note_names


def test_search_k_zero_returns_empty(indexed_db):
    client = RetrievalClient(indexed_db)
    assert client.search("anything", k=0) == []


def test_search_respects_k_cap(indexed_db):
    """k larger than corpus is fine; result count <= corpus."""
    client = RetrievalClient(indexed_db)
    hits = client.search("alpha beta", k=100)
    assert len(hits) <= 2  # vault has exactly 2 notes


def test_hit_fields_propagate_from_hybrid(indexed_db):
    """The typed RetrievalHit preserves the underlying HybridHit fields."""
    client = RetrievalClient(indexed_db)
    hits = client.search("alpha", k=5)
    assert len(hits) >= 1
    h = hits[0]
    assert h.note_id  # populated
    assert h.note_name  # populated
    assert h.score > 0  # RRF is always positive for a real hit
    # bm25_rank / dense_rank may be None on a --no-dense build, that's fine


# ── R-Cross defensive half: no mutating API ─────────────────────────────────


def test_client_exposes_only_search(indexed_db):
    """The client has no `index`, `update`, `delete`, etc. — P never
    mutates D through this surface."""
    client = RetrievalClient(indexed_db)
    public = {name for name in dir(client) if not name.startswith("_")}
    # Allowed public surface: db_path + search. Nothing else.
    assert public == {"db_path", "search"}, (
        f"unexpected public surface on RetrievalClient: {public - {'db_path', 'search'}}"
    )
