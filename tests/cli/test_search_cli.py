"""Smoke tests for the ``tessellum search`` CLI subcommand."""

from __future__ import annotations

import json
import textwrap

import pytest

from tessellum.cli.main import main
from tessellum.indexer import build


_NOTE = textwrap.dedent(
    """\
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

    # Term

    The {token} concept is foundational.
    {extra_body}
    """
)


@pytest.fixture
def indexed_db(tmp_path):
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    # Cross-link the two notes so BFS has something to traverse.
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _NOTE.format(token="alpha", extra_body="See [Beta](term_beta.md).")
    )
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _NOTE.format(token="beta", extra_body="See [Alpha](term_alpha.md).")
    )
    db_path = tmp_path / "search.db"
    build(v, db_path)
    return db_path


def test_search_basic_returns_0(indexed_db, capsys):
    """v0.0.15 flips the default to hybrid; bare ``search`` runs hybrid."""
    code = main(["search", "alpha", "--db", str(indexed_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "HYBRID matches" in out
    assert "term_alpha" in out


def test_search_no_match_returns_0(indexed_db, capsys):
    """Default (hybrid) over a nonsense query: hybrid still runs both rankers
    and gets no overlap → empty fused list. Use --bm25 to force a strict
    no-match (dense always returns *something* for any query)."""
    code = main(
        ["search", "nonexistent_xyz_qqq", "--bm25", "--db", str(indexed_db)]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "no matches" in out.lower()


def test_search_missing_db_returns_2(tmp_path, capsys):
    nonexistent = tmp_path / "missing.db"
    code = main(["search", "alpha", "--db", str(nonexistent)])
    assert code == 2
    err = capsys.readouterr().err
    assert "not found" in err
    assert "tessellum index build" in err


def test_search_malformed_query_returns_2(indexed_db, capsys):
    code = main(["search", "AND OR", "--db", str(indexed_db)])
    assert code == 2
    err = capsys.readouterr().err
    assert "query failed" in err


def test_search_k_flag_limits_results(indexed_db, capsys):
    # Both notes match alpha (same body template). --k 1 returns one hit.
    code = main(
        ["search", "alpha", "--db", str(indexed_db), "--k", "1", "--format", "json"]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["hit_count"] == 1


def test_search_bm25_json_output_structure(indexed_db, capsys):
    """BM25 JSON output includes snippet field on hits."""
    code = main(
        ["search", "alpha", "--bm25", "--db", str(indexed_db), "--format", "json"]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["query"] == "alpha"
    assert payload["strategy"] == "bm25"
    assert isinstance(payload["hits"], list)
    assert payload["hit_count"] == len(payload["hits"])
    if payload["hits"]:
        h = payload["hits"][0]
        assert "note_id" in h
        assert "note_name" in h
        assert "score" in h
        assert "snippet" in h


def test_search_no_snippet_flag_omits_snippet(indexed_db, capsys):
    """--no-snippet only applies to BM25 output."""
    code = main(
        [
            "search", "alpha",
            "--bm25",
            "--db", str(indexed_db),
            "--no-snippet",
            "--format", "json",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    if payload["hits"]:
        assert payload["hits"][0]["snippet"] is None


def test_search_bm25_flag_runs_bm25(indexed_db, capsys):
    """--bm25 selects BM25-only retrieval; output labelled BM25."""
    code = main(
        ["search", "alpha", "--bm25", "--db", str(indexed_db)]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "BM25 matches" in out


def test_search_hybrid_flag_explicit(indexed_db, capsys):
    """--hybrid is the explicit form of the new default."""
    code = main(
        ["search", "alpha", "--hybrid", "--db", str(indexed_db)]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "HYBRID matches" in out


def test_search_dense_flag_uses_dense_strategy(indexed_db, capsys):
    """--dense reads the dense (vec0) index; produces DENSE-labeled output."""
    code = main(
        ["search", "alpha", "--dense", "--db", str(indexed_db), "--k", "1"]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "DENSE matches" in out


def test_search_dense_json_output_includes_distance(indexed_db, capsys):
    code = main(
        [
            "search",
            "alpha",
            "--dense",
            "--db",
            str(indexed_db),
            "--k",
            "1",
            "--format",
            "json",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["strategy"] == "dense"
    if payload["hits"]:
        assert "distance" in payload["hits"][0]
        assert "score" in payload["hits"][0]


def test_search_strategies_mutually_exclusive(indexed_db, capsys):
    """All four strategy flags are in one mutex group."""
    for combo in [
        ("--bm25", "--dense"),
        ("--bm25", "--hybrid"),
        ("--dense", "--hybrid"),
        ("--bm25", "--bfs"),
        ("--hybrid", "--bfs"),
    ]:
        with pytest.raises(SystemExit):
            main(["search", "alpha", *combo, "--db", str(indexed_db)])


def test_search_bfs_flag_uses_graph_strategy(indexed_db, capsys):
    """--bfs traverses the link graph from a seed note_id."""
    code = main(
        [
            "search",
            "resources/term_dictionary/term_alpha.md",
            "--bfs",
            "--db",
            str(indexed_db),
            "--k",
            "1",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "BFS matches" in out


def test_search_bfs_unknown_seed_returns_0(indexed_db, capsys):
    """Unknown seed produces no hits but is not an error (exit 0)."""
    code = main(
        ["search", "does/not/exist.md", "--bfs", "--db", str(indexed_db)]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "no matches" in out.lower()


def test_search_bfs_json_output_includes_path_and_depth(indexed_db, capsys):
    """BFS JSON should expose `depth` and `path` fields per hit."""
    code = main(
        [
            "search",
            "resources/term_dictionary/term_alpha.md",
            "--bfs",
            "--db",
            str(indexed_db),
            "--k",
            "1",
            "--format",
            "json",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["strategy"] == "bfs"
    if payload["hits"]:
        h = payload["hits"][0]
        assert "depth" in h
        assert "path" in h
        assert isinstance(h["path"], list)
        assert h["path"][0] == "resources/term_dictionary/term_alpha.md"


def test_search_hybrid_json_includes_per_ranker_ranks(indexed_db, capsys):
    """Hybrid JSON output should include bm25_rank + dense_rank diagnostic fields."""
    code = main(
        [
            "search",
            "alpha",
            "--hybrid",
            "--db",
            str(indexed_db),
            "--k",
            "1",
            "--format",
            "json",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["strategy"] == "hybrid"
    if payload["hits"]:
        h = payload["hits"][0]
        # Both rank fields are present (may be None if not in that ranker's top-K).
        assert "bm25_rank" in h
        assert "dense_rank" in h


def test_banner_lists_search(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum search" in out
