"""Smoke tests for the ``tessellum format check`` CLI subcommand."""

from __future__ import annotations

import json
import textwrap

from tessellum.cli.main import main

# VALID has an internal link to other.md so LINK-006 (orphan) doesn't fire.
# Tests that write VALID to a directory also write a valid `other.md` so
# LINK-003 (target exists) doesn't fire either.
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
    Body. See [other](other.md) for related material.
    """
)

# Body intentionally has no internal link → produces 1 LINK-006 WARNING when
# validated, but no ERRORS. Suitable as a link target for VALID and ERRORS.
OTHER_VALID = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - terminology
    keywords:
      - one
      - two
      - three
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: concept
    ---
    Other body. (No internal links — exists only as a link target for tests.)
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
    Body. See [other](other.md) for related material.
    """
)

WARN_ONLY = VALID.replace(
    "  - alpha\n  - beta\n  - gamma",
    "  - alpha",
)


def _write_pair(dirpath, name="good.md"):
    """Write a clean note plus its `other.md` link target."""
    (dirpath / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    (dirpath / name).write_text(VALID, encoding="utf-8")
    return dirpath / name


def test_check_clean_file_returns_0(tmp_path, capsys):
    p = _write_pair(tmp_path)
    assert main(["format", "check", str(p)]) == 0
    out = capsys.readouterr().out
    assert "0 error" in out


def test_check_dirty_file_returns_1(tmp_path, capsys):
    (tmp_path / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    p = tmp_path / "bad.md"
    p.write_text(ERRORS, encoding="utf-8")
    assert main(["format", "check", str(p)]) == 1
    out = capsys.readouterr().out
    assert "ERROR" in out
    assert "building_block" in out
    assert "status" in out


def test_check_directory_recurses(tmp_path, capsys):
    (tmp_path / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    (tmp_path / "good.md").write_text(VALID, encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    (sub / "bad.md").write_text(ERRORS, encoding="utf-8")
    assert main(["format", "check", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "validated 4 file(s)" in out
    assert "sub/bad.md" in out


def test_warnings_only_returns_0(tmp_path, capsys):
    (tmp_path / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    p = tmp_path / "warn.md"
    p.write_text(WARN_ONLY, encoding="utf-8")
    assert main(["format", "check", str(p)]) == 0


def test_strict_promotes_warnings_to_failure(tmp_path, capsys):
    (tmp_path / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    p = tmp_path / "warn.md"
    p.write_text(WARN_ONLY, encoding="utf-8")
    assert main(["format", "check", "--strict", str(p)]) == 1


def test_missing_path_returns_2(tmp_path, capsys):
    nonexistent = tmp_path / "does-not-exist"
    assert main(["format", "check", str(nonexistent)]) == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_quiet_suppresses_summary_when_clean(tmp_path, capsys):
    p = _write_pair(tmp_path)
    assert main(["format", "check", "--quiet", str(p)]) == 0
    out = capsys.readouterr().out
    assert out.strip() == ""


def test_format_json_output_clean(tmp_path, capsys):
    p = _write_pair(tmp_path)
    assert main(["format", "check", "--format", "json", str(p)]) == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["summary"]["files_checked"] == 1
    assert payload["summary"]["errors"] == 0
    assert payload["files"][0]["path"].endswith("good.md")
    assert payload["files"][0]["issues"] == []


def test_format_json_output_dirty(tmp_path, capsys):
    (tmp_path / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    p = tmp_path / "bad.md"
    p.write_text(ERRORS, encoding="utf-8")
    assert main(["format", "check", "--format", "json", str(p)]) == 1
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["summary"]["errors"] >= 2
    rule_ids = {i["rule_id"] for f in payload["files"] for i in f["issues"]}
    assert "YAML-061" in rule_ids  # bad status enum
    assert "YAML-063" in rule_ids  # bad BB enum
    for issue in payload["files"][0]["issues"]:
        assert "rule_id" in issue
        assert "severity" in issue
        assert "field" in issue
        assert "message" in issue


def test_check_skips_non_note_files(tmp_path, capsys):
    (tmp_path / "other.md").write_text(OTHER_VALID, encoding="utf-8")
    (tmp_path / "good.md").write_text(VALID, encoding="utf-8")
    # These would each produce 7 missing-required-field errors if validated
    (tmp_path / "README.md").write_text("Just a readme.\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    (tmp_path / "Rank_inlinks.md").write_text("ranking data\n", encoding="utf-8")
    code = main(["format", "check", str(tmp_path)])
    assert code == 0
    out = capsys.readouterr().out
    assert "validated 2 file(s)" in out  # good.md + other.md
    assert "README" not in out
    assert "CHANGELOG" not in out
    assert "Rank_" not in out


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
