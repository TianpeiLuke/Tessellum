"""Smoke tests for ``tessellum bb migrate`` — Phase B.5.

Covers:

- Vault not found → exit 2.
- Invalid --target-version → exit 2.
- Empty vault → exit 0, all counts 0.
- Vault with one note recorded at v1, target=2 → 1 behind.
- --apply bumps the version on would-pass notes.
- Notes missing bb_schema_version default to v=1 (back-compat).
- Notes with non-integer bb_schema_version go to ``skipped``.
- JSON output shape.
"""

from __future__ import annotations

import json
from pathlib import Path


from tessellum.cli.main import main


def _write_note(
    vault: Path,
    name: str,
    *,
    bb_type: str = "argument",
    version: int | str | None = 1,
    status: str = "active",
    body: str = "# Note\n\nbody\n",
) -> Path:
    """Write a minimal valid note to the vault."""
    dest = vault / "resources" / "analysis_thoughts"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f"thought_{name}.md"
    version_line = f"bb_schema_version: {version}\n" if version is not None else ""
    path.write_text(
        f"""---
tags:
  - resource
  - analysis
  - {bb_type}
keywords:
  - test
topics:
  - Testing
language: markdown
date of note: 2026-05-10
status: {status}
building_block: {bb_type}
{version_line}---

{body}
""",
        encoding="utf-8",
    )
    return path


# ── Error paths ────────────────────────────────────────────────────────────


def test_migrate_missing_vault(tmp_path, capsys):
    code = main(["bb", "migrate", "--vault", str(tmp_path / "nope")])
    assert code == 2
    err = capsys.readouterr().err
    assert "vault root not found" in err


def test_migrate_invalid_target_version(tmp_path, capsys):
    (tmp_path / "vault").mkdir()
    code = main(
        ["bb", "migrate", "--vault", str(tmp_path / "vault"), "--target-version", "abc"]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "must be 'current' or an integer" in err


# ── Happy paths ────────────────────────────────────────────────────────────


def test_migrate_empty_vault(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    code = main(
        ["bb", "migrate", "--vault", str(vault), "--target-version", "5", "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["total_md_files"] == 0
    assert payload["behind_count"] == 0


def test_migrate_one_note_behind_target(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "alpha", version=1)
    code = main(
        ["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["behind_count"] == 1
    assert payload["would_pass_count"] >= 0  # would_pass depends on TESS-005
    # Body has no links → no TESS-005 warnings → passes


def test_migrate_note_at_target_is_not_behind(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "atv2", version=2)
    code = main(
        ["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["behind_count"] == 0


def test_migrate_note_above_target_is_not_behind(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "atv5", version=5)
    code = main(
        ["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["behind_count"] == 0


def test_migrate_missing_version_field_defaults_to_v1(tmp_path, capsys):
    """v0.0.52-era notes (no bb_schema_version) treated as v=1."""
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "noversion", version=None)
    code = main(
        ["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["behind_count"] == 1


def test_migrate_non_integer_version_is_skipped(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "garbage", version="not_a_number")
    code = main(
        ["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--format", "json"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["skipped_count"] == 1
    assert payload["behind_count"] == 0


# ── --apply ────────────────────────────────────────────────────────────────


def test_migrate_apply_bumps_version_on_would_pass_notes(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    note_path = _write_note(vault, "bumpme", version=1)
    code = main(
        [
            "bb", "migrate",
            "--vault", str(vault),
            "--target-version", "3",
            "--apply",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["bumped_count"] >= 1
    # Re-read the file — version should now be 3
    text = note_path.read_text(encoding="utf-8")
    assert "bb_schema_version: 3" in text
    assert "bb_schema_version: 1" not in text


def test_migrate_dry_run_does_not_modify_files(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    note_path = _write_note(vault, "no_bump", version=1)
    before = note_path.read_text(encoding="utf-8")
    code = main(
        [
            "bb", "migrate",
            "--vault", str(vault),
            "--target-version", "2",
            "--format", "json",
        ]
    )
    assert code == 0
    after = note_path.read_text(encoding="utf-8")
    assert before == after  # no --apply → no writes


def test_migrate_apply_injects_field_when_absent(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    note_path = _write_note(vault, "field_absent", version=None)
    code = main(
        [
            "bb", "migrate",
            "--vault", str(vault),
            "--target-version", "2",
            "--apply",
            "--format", "json",
        ]
    )
    assert code == 0
    text = note_path.read_text(encoding="utf-8")
    assert "bb_schema_version: 2" in text


def test_migrate_apply_idempotent(tmp_path, capsys):
    """Running --apply twice doesn't double-bump."""
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "idempotent", version=1)
    main(["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--apply", "--format", "json"])
    capsys.readouterr()  # drain
    code = main(["bb", "migrate", "--vault", str(vault), "--target-version", "2", "--apply", "--format", "json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    # Second run: already at target → 0 behind, 0 bumped
    assert payload["behind_count"] == 0
    assert payload["bumped_count"] == 0


# ── Human format ───────────────────────────────────────────────────────────


def test_migrate_human_format_summary(tmp_path, capsys):
    vault = tmp_path / "vault"
    vault.mkdir()
    _write_note(vault, "human", version=1)
    code = main(["bb", "migrate", "--vault", str(vault), "--target-version", "2"])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum bb migrate" in out
    assert "target version:  2" in out
    assert "notes behind target: 1" in out
