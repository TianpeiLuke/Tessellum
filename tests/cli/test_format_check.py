"""Smoke tests for the ``tessellum format check`` CLI subcommand."""

from __future__ import annotations

import textwrap

from tessellum.cli.main import main

VALID = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - terminology
      - tessellum
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - Topic A
      - Topic B
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: concept
    ---
    Body.
    """
)

ERRORS = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - terminology
    keywords:
      - alpha
    topics:
      - Topic A
    language: markdown
    date of note: 2026-05-10
    status: shipped
    building_block: idea
    ---
    Body.
    """
)

WARN_ONLY = VALID.replace(
    "  - alpha\n  - beta\n  - gamma",
    "  - alpha",
)


def test_check_clean_file_returns_0(tmp_path, capsys):
    p = tmp_path / "good.md"
    p.write_text(VALID)
    assert main(["format", "check", str(p)]) == 0
    out = capsys.readouterr().out
    assert "0 error" in out


def test_check_dirty_file_returns_1(tmp_path, capsys):
    p = tmp_path / "bad.md"
    p.write_text(ERRORS)
    assert main(["format", "check", str(p)]) == 1
    out = capsys.readouterr().out
    assert "ERROR" in out
    assert "building_block" in out
    assert "status" in out


def test_check_directory_recurses(tmp_path, capsys):
    (tmp_path / "good.md").write_text(VALID)
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "bad.md").write_text(ERRORS)
    assert main(["format", "check", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "validated 2 file(s)" in out
    assert "sub/bad.md" in out


def test_warnings_only_returns_0(tmp_path, capsys):
    p = tmp_path / "warn.md"
    p.write_text(WARN_ONLY)
    assert main(["format", "check", str(p)]) == 0


def test_strict_promotes_warnings_to_failure(tmp_path, capsys):
    p = tmp_path / "warn.md"
    p.write_text(WARN_ONLY)
    assert main(["format", "check", "--strict", str(p)]) == 1


def test_missing_path_returns_2(tmp_path, capsys):
    nonexistent = tmp_path / "does-not-exist"
    assert main(["format", "check", str(nonexistent)]) == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_quiet_suppresses_summary_when_clean(tmp_path, capsys):
    p = tmp_path / "good.md"
    p.write_text(VALID)
    assert main(["format", "check", "--quiet", str(p)]) == 0
    out = capsys.readouterr().out
    assert out.strip() == ""


def test_bare_command_prints_banner(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "tessellum" in out
    assert "Available now" in out
    assert "format check" in out


def test_version_flag_exits_cleanly(capsys):
    import pytest as _pytest

    with _pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "tessellum" in out
