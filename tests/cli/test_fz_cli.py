"""Smoke tests for the ``tessellum fz`` CLI subcommand.

Tessellum has no ``folgezettel_trails`` materialised view — the
trail topology is derived in-memory by walking ``notes.folgezettel``
and ``notes.folgezettel_parent``. These tests build a small vault
with a 4-node trail and a 2-node trail, then exercise each
sub-subcommand.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.cli.fz import fz_sort_key, fz_trail_root
from tessellum.cli.main import main
from tessellum.indexer import build


_FZ_NOTE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - analysis
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
    building_block: {bb}
    {fz_block}
    ---

    # {name}

    Body.
    """
)


def _fz_block(fz: str | None, parent: str | None) -> str:
    if fz is None:
        return ""
    lines = [f'folgezettel: "{fz}"']
    if parent is not None:
        lines.append(f'folgezettel_parent: "{parent}"')
    return "\n".join(lines)


def _write_note(vault: Path, slug: str, fz: str | None, parent: str | None, bb: str = "argument") -> None:
    p = vault / "resources/analysis_thoughts" / f"{slug}.md"
    p.write_text(
        _FZ_NOTE.format(
            name=slug.replace("_", " ").title(),
            bb=bb,
            fz_block=_fz_block(fz, parent),
        )
    )


@pytest.fixture
def fz_db(tmp_path):
    """A vault with:
        Trail 1 (4 nodes, max depth 3):
            1  ── root_one             (argument)
            └─ 1a ── child_a           (argument)
               ├─ 1a1 ── child_a_one  (counter_argument)
               └─ 1a2 ── child_a_two  (concept)
        Trail 2 (2 nodes):
            2  ── root_two             (argument)
            └─ 2a ── child_two_a       (counter_argument)
        Plus 1 orphan note (no FZ).
    """
    v = tmp_path / "v"
    (v / "resources/analysis_thoughts").mkdir(parents=True)

    _write_note(v, "root_one", "1", None, "argument")
    _write_note(v, "child_a", "1a", "1", "argument")
    _write_note(v, "child_a_one", "1a1", "1a", "counter_argument")
    _write_note(v, "child_a_two", "1a2", "1a", "concept")

    _write_note(v, "root_two", "2", None, "argument")
    _write_note(v, "child_two_a", "2a", "2", "counter_argument")

    _write_note(v, "loose_note", None, None, "concept")

    db_path = tmp_path / "fz.db"
    build(v, db_path, with_dense=False)
    return db_path


# ── sort + trail-root helpers ───────────────────────────────────────────────


def test_fz_sort_key_numeric_aware():
    """1b2 < 1b10 — numeric tokens compare as integers, not strings."""
    fzs = ["1b10", "1b2", "1b1", "1a"]
    assert sorted(fzs, key=fz_sort_key) == ["1a", "1b1", "1b2", "1b10"]


def test_fz_sort_key_letters_after_digits_at_same_position():
    fzs = ["1", "1a", "2", "10"]
    assert sorted(fzs, key=fz_sort_key) == ["1", "1a", "2", "10"]


def test_fz_trail_root_picks_leading_integer():
    assert fz_trail_root("1") == "1"
    assert fz_trail_root("1a1b") == "1"
    assert fz_trail_root("10d3a") == "10"
    assert fz_trail_root("abc") == "abc"  # no leading int → fallback to whole


# ── list / all ──────────────────────────────────────────────────────────────


def test_cli_fz_list(fz_db, capsys):
    code = main(["fz", "list", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Trail" in out
    assert "1" in out
    assert "2" in out
    # 4 nodes in trail 1, 2 in trail 2 → 6 total
    assert "6 nodes across 2 trails" in out


def test_cli_fz_all_groups_by_trail(fz_db, capsys):
    code = main(["fz", "all", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Trail 1" in out
    assert "Trail 2" in out
    # Numeric-aware order: trail 1 (members: 1, 1a, 1a1, 1a2)
    assert out.index("Trail 1") < out.index("Trail 2")
    # And 1a1 appears before 1a2 in the body
    assert out.index("1a1") < out.index("1a2")


# ── show / descendants ──────────────────────────────────────────────────────


def test_cli_fz_show_subtree(fz_db, capsys):
    code = main(["fz", "show", "1", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Subtree of FZ 1" in out
    assert "4 nodes" in out
    for fz in ("1", "1a", "1a1", "1a2"):
        assert fz in out


def test_cli_fz_show_subtree_at_inner_node(fz_db, capsys):
    """Showing 1a should produce just 1a/1a1/1a2 — 3 nodes — not the whole trail."""
    code = main(["fz", "show", "1a", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Subtree of FZ 1a" in out
    assert "3 nodes" in out
    # And the root (FZ 1) does NOT appear in the subtree
    assert "Root One" not in out


def test_cli_fz_descendants(fz_db, capsys):
    code = main(["fz", "descendants", "1", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Descendants of FZ 1" in out
    # 3 descendants (1a, 1a1, 1a2 — excludes root)
    assert "3 nodes" in out
    assert "1a1" in out
    assert "1a2" in out


def test_cli_fz_descendants_leaf_has_none(fz_db, capsys):
    code = main(["fz", "descendants", "1a1", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "No descendants" in out


# ── ancestors / path ────────────────────────────────────────────────────────


def test_cli_fz_ancestors(fz_db, capsys):
    code = main(["fz", "ancestors", "1a1", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Ancestors of FZ 1a1" in out
    # Chain length is 3 (1 → 1a → 1a1)
    assert "1 -> 1a -> 1a1" in out


def test_cli_fz_path_includes_siblings(fz_db, capsys):
    code = main(["fz", "path", "1a1", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "trail 1" in out
    assert "depth 2" in out
    # 1a2 is a sibling of 1a1 under parent 1a
    assert "Siblings" in out
    assert "1a2" in out


def test_cli_fz_path_root_has_no_siblings_section(fz_db, capsys):
    """Root FZ 1 has no parent → no siblings section."""
    code = main(["fz", "path", "1", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Siblings" not in out


# ── resolution ──────────────────────────────────────────────────────────────


def test_cli_fz_resolve_by_note_name(fz_db, capsys):
    """Querying by exact note_name (file stem) resolves to the FZ."""
    code = main(["fz", "ancestors", "child_a_one", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Ancestors of FZ 1a1" in out


def test_cli_fz_unknown_query_returns_0_with_message(fz_db, capsys):
    """Unknown FZ is not an invocation error — just an empty result."""
    code = main(["fz", "show", "999z", "--db", str(fz_db)])
    assert code == 0
    out = capsys.readouterr().out
    assert "No FZ note matching" in out


# ── error paths ─────────────────────────────────────────────────────────────


def test_cli_fz_missing_db_returns_2(tmp_path, capsys):
    code = main(["fz", "list", "--db", str(tmp_path / "missing.db")])
    assert code == 2
    err = capsys.readouterr().err
    assert "not found" in err


def test_cli_fz_no_subcommand_returns_2(capsys):
    """Bare ``tessellum fz`` (no sub-subcommand) — exits 2 with usage hint."""
    code = main(["fz"])
    assert code == 2
    err = capsys.readouterr().err
    assert "missing sub-subcommand" in err


def test_banner_lists_fz(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum fz" in out
