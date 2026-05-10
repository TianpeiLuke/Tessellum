"""Smoke tests for the ``tessellum filter`` CLI subcommand."""

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
      - cqrs
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - X
      - Y
    language: markdown
    date of note: {date}
    status: {status}
    building_block: {bb}
    ---

    # {name}

    Body.
    """
)


@pytest.fixture
def filter_db(tmp_path):
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_one.md").write_text(
        _NOTE.format(name="One", status="active", bb="concept", date="2026-01-01")
    )
    (v / "resources/term_dictionary/term_two.md").write_text(
        _NOTE.format(name="Two", status="draft", bb="concept", date="2026-02-01")
    )
    db_path = tmp_path / "f.db"
    build(v, db_path, with_dense=False)
    return db_path


def test_cli_filter_by_building_block(filter_db, capsys):
    code = main(
        ["filter", "--building-block", "concept", "--db", str(filter_db)]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "FILTER" in out
    assert "term_one" in out
    assert "term_two" in out


def test_cli_filter_by_status(filter_db, capsys):
    code = main(["filter", "--status", "draft", "--db", str(filter_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "term_two" in out
    assert "term_one" not in out


def test_cli_filter_by_tag(filter_db, capsys):
    code = main(["filter", "--tag", "cqrs", "--db", str(filter_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "term_one" in out
    assert "term_two" in out


def test_cli_filter_combined_filters(filter_db, capsys):
    code = main(
        [
            "filter",
            "--building-block", "concept",
            "--status", "draft",
            "--db", str(filter_db),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "term_two" in out
    assert "term_one" not in out


def test_cli_filter_no_match_returns_0(filter_db, capsys):
    code = main(["filter", "--status", "archived", "--db", str(filter_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "no notes match" in out.lower()


def test_cli_filter_no_filters_lists_all(filter_db, capsys):
    """No filter flags → all notes in the index."""
    code = main(["filter", "--db", str(filter_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "term_one" in out
    assert "term_two" in out


def test_cli_filter_k_limit(filter_db, capsys):
    code = main(
        [
            "filter",
            "--db", str(filter_db),
            "--k", "1",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["hit_count"] == 1


def test_cli_filter_json_output_structure(filter_db, capsys):
    code = main(
        [
            "filter",
            "--building-block", "concept",
            "--db", str(filter_db),
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["filters"]["building_block"] == "concept"
    assert "hit_count" in payload
    assert isinstance(payload["hits"], list)
    if payload["hits"]:
        h = payload["hits"][0]
        for field in [
            "note_id",
            "note_name",
            "note_category",
            "note_second_category",
            "note_status",
            "building_block",
            "note_creation_date",
            "folgezettel",
        ]:
            assert field in h


def test_cli_filter_missing_db_returns_2(tmp_path, capsys):
    code = main(["filter", "--db", str(tmp_path / "missing.db")])
    assert code == 2
    err = capsys.readouterr().err
    assert "not found" in err


def test_cli_filter_has_folgezettel_mutex_with_no_folgezettel(filter_db, capsys):
    """--has-folgezettel and --no-folgezettel are mutually exclusive."""
    with pytest.raises(SystemExit):
        main(
            [
                "filter",
                "--has-folgezettel",
                "--no-folgezettel",
                "--db", str(filter_db),
            ]
        )


def test_cli_filter_date_range(filter_db, capsys):
    code = main(
        [
            "filter",
            "--date-after", "2026-01-15",
            "--date-before", "2026-02-15",
            "--db", str(filter_db),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "term_two" in out  # 2026-02-01 in range
    assert "term_one" not in out  # 2026-01-01 too early


def test_banner_lists_filter(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum filter" in out
