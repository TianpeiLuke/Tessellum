"""Smoke tests for the ``tessellum capture`` CLI subcommand."""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.capture import REGISTRY
from tessellum.cli.main import main


@pytest.fixture
def vault_root(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    for spec in REGISTRY.values():
        (vault / spec.destination).mkdir(parents=True, exist_ok=True)
    return vault


def test_cli_capture_concept_creates_file(vault_root, capsys):
    code = main(["capture", "concept", "foo", "--vault", str(vault_root)])
    assert code == 0
    out = capsys.readouterr().out
    assert "term_foo.md" in out
    assert "created" in out
    expected = vault_root / "resources/term_dictionary/term_foo.md"
    assert expected.is_file()


def test_cli_capture_skill_creates_file(vault_root, capsys):
    code = main(["capture", "skill", "detect_drift", "--vault", str(vault_root)])
    assert code == 0
    expected = vault_root / "resources/skills/skill_detect_drift.md"
    assert expected.is_file()


def test_cli_capture_invalid_slug_exits_2(vault_root, capsys):
    code = main(["capture", "concept", "Bad-Slug", "--vault", str(vault_root)])
    assert code == 2
    err = capsys.readouterr().err
    assert "slug" in err.lower()


def test_cli_capture_existing_file_exits_1(vault_root, capsys):
    main(["capture", "concept", "foo", "--vault", str(vault_root)])
    code = main(["capture", "concept", "foo", "--vault", str(vault_root)])
    assert code == 1
    err = capsys.readouterr().err
    assert "already exists" in err


def test_cli_capture_force_overwrites(vault_root, capsys):
    main(["capture", "concept", "foo", "--vault", str(vault_root)])
    code = main([
        "capture", "concept", "foo",
        "--vault", str(vault_root),
        "--force",
    ])
    assert code == 0


def test_cli_capture_missing_vault_exits_2(tmp_path, capsys):
    nonexistent = tmp_path / "nope"
    code = main(["capture", "concept", "foo", "--vault", str(nonexistent)])
    assert code == 2
    err = capsys.readouterr().err
    assert "does not exist" in err.lower()


def test_cli_banner_lists_capture(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum capture" in out


def test_cli_capture_help_lists_all_flavors(capsys):
    """argparse choices= should expose all 12 flavors in help text."""
    with pytest.raises(SystemExit):
        main(["capture", "--help"])
    out = capsys.readouterr().out
    for flavor in REGISTRY:
        assert flavor in out
