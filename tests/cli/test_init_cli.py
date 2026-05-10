"""Smoke tests for the ``tessellum init`` CLI subcommand."""

from __future__ import annotations

import pytest

from tessellum.cli.main import main


def test_cli_init_scaffolds_target(tmp_path, capsys):
    target = tmp_path / "my-vault"
    code = main(["init", str(target)])
    assert code == 0
    out = capsys.readouterr().out
    assert "scaffolded vault at" in out
    assert (target / "0_entry_points/entry_master_toc.md").is_file()


def test_cli_init_existing_non_empty_returns_1(tmp_path, capsys):
    target = tmp_path / "v"
    target.mkdir()
    (target / "stale.txt").write_text("x")
    code = main(["init", str(target)])
    assert code == 1
    err = capsys.readouterr().err
    assert "non-empty" in err


def test_cli_init_force_into_non_empty(tmp_path, capsys):
    target = tmp_path / "v"
    target.mkdir()
    (target / "stale.txt").write_text("x")
    code = main(["init", str(target), "--force"])
    assert code == 0
    assert (target / "stale.txt").is_file()
    assert (target / "resources/templates").is_dir()


def test_cli_init_target_is_file_returns_1(tmp_path, capsys):
    target = tmp_path / "vfile"
    target.write_text("not a directory")
    code = main(["init", str(target)])
    assert code == 1
    err = capsys.readouterr().err
    assert "is a file" in err


def test_banner_lists_init(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum init <dir>" in out


def test_cli_init_help_has_force_flag(capsys):
    with pytest.raises(SystemExit):
        main(["init", "--help"])
    out = capsys.readouterr().out
    assert "--force" in out
