"""Smoke tests for the ``tessellum search`` CLI subcommand."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

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
    """
)


@pytest.fixture
def indexed_db(tmp_path):
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _NOTE.format(token="alpha")
    )
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _NOTE.format(token="beta")
    )
    db_path = tmp_path / "search.db"
    build(v, db_path)
    return db_path


def test_search_basic_returns_0(indexed_db, capsys):
    code = main(["search", "alpha", "--db", str(indexed_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "BM25 matches" in out
    assert "term_alpha" in out


def test_search_no_match_returns_0(indexed_db, capsys):
    code = main(["search", "nonexistent_xyz_qqq", "--db", str(indexed_db)])
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


def test_search_json_output_structure(indexed_db, capsys):
    code = main(
        ["search", "alpha", "--db", str(indexed_db), "--format", "json"]
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
    code = main(
        [
            "search", "alpha",
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


def test_search_bm25_flag_accepted(indexed_db, capsys):
    """The --bm25 flag is accepted (forward-compat for Wave 2-3 selectors)."""
    code = main(
        ["search", "alpha", "--bm25", "--db", str(indexed_db)]
    )
    assert code == 0


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


def test_search_bm25_and_dense_mutually_exclusive(indexed_db, capsys):
    """--bm25 and --dense can't both be passed (argparse mutex group)."""
    with pytest.raises(SystemExit):
        main(
            [
                "search",
                "alpha",
                "--bm25",
                "--dense",
                "--db",
                str(indexed_db),
            ]
        )


def test_banner_lists_search(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum search" in out
