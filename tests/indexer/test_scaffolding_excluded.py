"""Navigation and provenance sections are excluded from the INDEX, not the note.

A note's Related Notes / Source / References sections are part of the note and
are exactly what link extraction reads. They are not evidence, though, and
indexing them spends a note's share of a retrieval budget on markdown links a
reader cannot follow. Measured on a benchmark vault, excluding them from the
indexed text was worth a substantial recall gain at a fixed budget, for free.

Both halves have to hold at once, which is what makes this worth pinning:
the index must NOT see those sections, and link extraction MUST.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from tessellum.format.parser import strip_scaffolding   # noqa: E402

NOTE = """# Ad load varies with the request

The Age reported on 2023-10-22 that Google's ad load changed per request.

## Related Notes
- [Google](term_google.md) — the company
- [Ad Load](term_ad_load.md) — the metric

## Source
https://example.com/article

## References
- Some Paper, 2024
"""


def test_prose_survives():
    out = strip_scaffolding(NOTE)
    assert "The Age reported on 2023-10-22" in out
    assert out.startswith("# Ad load")


def test_navigation_and_provenance_are_dropped():
    out = strip_scaffolding(NOTE)
    for gone in ("term_google.md", "term_ad_load.md",
                 "example.com/article", "Some Paper"):
        assert gone not in out, f"{gone} should not reach the index"


def test_a_body_with_no_scaffolding_is_unchanged():
    plain = "# Title\n\nJust prose, nothing else."
    assert strip_scaffolding(plain) == plain.strip()


def test_empty_and_none_safe():
    assert strip_scaffolding("") == ""


def _write(v: Path, rel: str, text: str) -> None:
    p = v / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _fixture_vault(root: Path) -> Path:
    """Two notes. A links to B ONLY inside its Related Notes section, and A's
    prose mentions a distinctive token that must be searchable while B's
    Related-Notes-only token must not be."""
    v = root / "vault"
    _write(v, "resources/note_a.md",
           "---\ntags: [resource]\n---\n# Alpha\n\nProse about quokkalith.\n\n"
           "## Related Notes\n- [Beta](note_b.md) — zebrafrond\n")
    _write(v, "resources/note_b.md",
           "---\ntags: [resource]\n---\n# Beta\n\nProse about marmoset.\n")
    return v


def _assert_invariant(db: Path, label: str) -> None:
    import sqlite3
    con = sqlite3.connect(db)
    try:
        edges = con.execute(
            "SELECT source_note_id, target_note_id FROM note_links").fetchall()
        assert ("resources/note_a.md", "resources/note_b.md") in edges, \
            f"{label}: link extraction lost the Related-Notes-only edge"
        assert con.execute("SELECT note_id FROM notes_fts WHERE notes_fts MATCH ?",
                           ("quokkalith",)).fetchall(), f"{label}: prose token not indexed"
        assert not con.execute("SELECT note_id FROM notes_fts WHERE notes_fts MATCH ?",
                               ("zebrafrond",)).fetchall(), \
            f"{label}: Related Notes text reached the index"
    finally:
        con.close()


def test_full_build_keeps_links_and_drops_scaffolding(tmp_path: Path):
    from tessellum.indexer.build import build
    v = _fixture_vault(tmp_path)
    db = tmp_path / "full.db"
    build(v, db, with_dense=False)
    _assert_invariant(db, "full build")


def test_incremental_build_keeps_links_and_drops_scaffolding(tmp_path: Path):
    """The INCREMENTAL path is the one that broke.

    It re-reads bodies through `_load_all_note_bodies` for link extraction, and
    an earlier edit stripped that dict. A full build never touches that function,
    so a test that only ran full builds passed with the bug in place and CI
    caught it instead. Build, then change the vault, then run the incremental
    pass -- that is the path under test.
    """
    from tessellum.indexer.build import build, build_incremental
    v = _fixture_vault(tmp_path)
    db = tmp_path / "inc.db"
    build(v, db, with_dense=False)
    # a change forces the incremental walk to re-extract links for all notes
    _write(v, "resources/note_c.md",
           "---\ntags: [resource]\n---\n# Gamma\n\nProse about capybara.\n")
    build_incremental(v, db, with_dense=False)
    _assert_invariant(db, "incremental build")
