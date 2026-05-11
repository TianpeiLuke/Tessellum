"""Smoke tests for the ``tessellum index build`` CLI subcommand."""

from __future__ import annotations

import textwrap

import pytest

from tessellum.cli.main import main


_VALID_NOTE = textwrap.dedent(
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

    Body.
    """
)


@pytest.fixture
def vault(tmp_path):
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_demo.md").write_text(_VALID_NOTE)
    return v


def test_cli_index_build_creates_db(vault, tmp_path, capsys):
    db_path = tmp_path / "out.db"
    code = main(
        ["index", "build", "--vault", str(vault), "--db", str(db_path)]
    )
    assert code == 0
    assert db_path.is_file()
    out = capsys.readouterr().out
    assert "built index at" in out
    assert "notes indexed" in out


def test_cli_index_build_refuses_overwrite(vault, tmp_path, capsys):
    db_path = tmp_path / "out.db"
    main(["index", "build", "--vault", str(vault), "--db", str(db_path)])
    code = main(
        ["index", "build", "--vault", str(vault), "--db", str(db_path)]
    )
    assert code == 1
    err = capsys.readouterr().err
    assert "already exists" in err


def test_cli_index_build_force_overwrites(vault, tmp_path, capsys):
    db_path = tmp_path / "out.db"
    main(["index", "build", "--vault", str(vault), "--db", str(db_path)])
    code = main(
        [
            "index", "build",
            "--vault", str(vault),
            "--db", str(db_path),
            "--force",
        ]
    )
    assert code == 0


def test_cli_index_build_missing_vault(tmp_path, capsys):
    code = main(
        [
            "index", "build",
            "--vault", str(tmp_path / "nope"),
            "--db", str(tmp_path / "out.db"),
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "vault path" in err


def test_banner_lists_index_build(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum index build" in out
