"""Smoke tests for tessellum.indexer (build + Database)."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.indexer import BuildResult, Database, build


_NOTE_TEMPLATE = """\
---
tags:
  - {category}
  - {second}
{extra_tags}
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
{extra_yaml}
---

# {name}

{body}
"""


def _make_note(
    name: str,
    *,
    category: str = "resource",
    second: str = "terminology",
    bb: str = "concept",
    extra_tags: str = "",
    extra_yaml: str = "",
    body: str = "Body.",
) -> str:
    return _NOTE_TEMPLATE.format(
        name=name,
        category=category,
        second=second,
        bb=bb,
        extra_tags=extra_tags,
        extra_yaml=extra_yaml,
        body=body,
    )


@pytest.fixture
def vault(tmp_path):
    """A tiny vault with two terms that link to each other + one orphan."""
    v = tmp_path / "v"
    (v / "resources" / "term_dictionary").mkdir(parents=True)
    (v / "0_entry_points").mkdir(parents=True)

    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note(
            "Term: Alpha",
            body="See [Beta](term_beta.md) and [Gamma](term_gamma.md).",
        )
    )
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _make_note(
            "Term: Beta",
            body="Back to [Alpha](term_alpha.md). External: [docs](https://example.com).",
        )
    )
    (v / "resources/term_dictionary/term_orphan.md").write_text(
        _make_note(
            "Term: Orphan",
            body="No internal links.",
        )
    )
    (v / "0_entry_points/entry_master_toc.md").write_text(
        _make_note(
            "Entry: TOC",
            category="entry_point",
            second="index",
            bb="navigation",
            body="Pointers to [Alpha](../resources/term_dictionary/term_alpha.md).",
        )
    )
    return v


def test_build_creates_db(vault, tmp_path):
    db_path = tmp_path / "test.db"
    result = build(vault, db_path)
    assert isinstance(result, BuildResult)
    assert db_path.is_file()
    assert result.notes_indexed == 4  # alpha, beta, orphan, entry_master_toc
    assert result.duration_seconds > 0


def test_build_indexes_links_correctly(vault, tmp_path):
    db_path = tmp_path / "test.db"
    result = build(vault, db_path)
    # alpha -> beta, alpha -> gamma (broken — gamma doesn't exist; dropped)
    # beta -> alpha
    # entry -> alpha
    # = 3 resolvable links
    assert result.links_indexed == 3


def test_build_refuses_overwrite_without_force(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with pytest.raises(FileExistsError, match="already exists"):
        build(vault, db_path)


def test_build_force_overwrites(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    build(vault, db_path, force=True)  # should not raise
    assert db_path.is_file()


def test_build_idempotent(vault, tmp_path):
    """Two consecutive builds → same row counts."""
    db_path = tmp_path / "test.db"
    r1 = build(vault, db_path)
    r2 = build(vault, db_path, force=True)
    assert r1.notes_indexed == r2.notes_indexed
    assert r1.links_indexed == r2.links_indexed


def test_build_creates_parent_dirs(vault, tmp_path):
    db_path = tmp_path / "deep" / "nested" / "test.db"
    build(vault, db_path)
    assert db_path.is_file()


def test_build_missing_vault_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="vault path"):
        build(tmp_path / "nope", tmp_path / "test.db")


def test_database_query_all_notes(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        notes = db.all_notes()
    assert len(notes) == 4
    names = {n.note_name for n in notes}
    assert "term_alpha" in names
    assert "term_beta" in names
    assert "entry_master_toc" in names


def test_database_query_note_by_id(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        note = db.note_by_id("resources/term_dictionary/term_alpha.md")
    assert note is not None
    assert note.note_name == "term_alpha"
    assert note.note_category == "resource"
    assert note.note_second_category == "terminology"
    assert note.building_block == "concept"


def test_database_query_unknown_id_returns_none(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        assert db.note_by_id("does/not/exist.md") is None


def test_database_query_by_building_block(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        concepts = db.notes_by_building_block("concept")
        nav = db.notes_by_building_block("navigation")
    assert len(concepts) == 3  # alpha, beta, orphan
    assert len(nav) == 1


def test_database_query_by_category(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        resources = db.notes_by_category("resource")
        entry_points = db.notes_by_category("entry_point")
    assert len(resources) == 3
    assert len(entry_points) == 1


def test_database_query_by_second_category(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        terms = db.notes_by_second_category("terminology")
        indexes = db.notes_by_second_category("index")
    assert len(terms) == 3
    assert len(indexes) == 1


def test_database_links_from(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        outlinks = db.links_from("resources/term_dictionary/term_alpha.md")
    targets = {lk.target_note_id for lk in outlinks}
    assert "resources/term_dictionary/term_beta.md" in targets


def test_database_links_to(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        inlinks = db.links_to("resources/term_dictionary/term_alpha.md")
    sources = {lk.source_note_id for lk in inlinks}
    assert "resources/term_dictionary/term_beta.md" in sources
    assert "0_entry_points/entry_master_toc.md" in sources


def test_database_link_count(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        assert db.link_count() == 3


def test_database_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        Database(tmp_path / "missing.db")


def test_database_tags_keywords_topics_parsed(vault, tmp_path):
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        note = db.note_by_id("resources/term_dictionary/term_alpha.md")
    assert note is not None
    assert "resource" in note.tags
    assert "terminology" in note.tags
    assert "alpha" in note.keywords
    assert "X" in note.topics


def test_external_links_not_indexed(vault, tmp_path):
    """https://example.com from term_beta should not appear in note_links."""
    db_path = tmp_path / "test.db"
    build(vault, db_path)
    with Database(db_path) as db:
        outlinks = db.links_from("resources/term_dictionary/term_beta.md")
    targets = {lk.target_note_id for lk in outlinks}
    assert all("example.com" not in t for t in targets)


def test_broken_path_link_uses_markdown_broken_path_type(tmp_path):
    """A relative path that doesn't exist BUT whose stem uniquely names an
    existing note should be indexed with link_type='markdown_broken_path'."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/skills").mkdir(parents=True)
    # term_alpha lives in term_dictionary/
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note("Alpha", body="ok.")
    )
    # Skill links to term_alpha via WRONG path (skills/, not term_dictionary/).
    (v / "resources/skills/skill_foo.md").write_text(
        _make_note(
            "Skill",
            second="skill",
            bb="procedure",
            body="See [Alpha](term_alpha.md).",
        )
    )
    db_path = tmp_path / "test.db"
    build(v, db_path)
    with Database(db_path) as db:
        outlinks = db.links_from("resources/skills/skill_foo.md")
    assert len(outlinks) == 1
    link = outlinks[0]
    assert link.link_type == "markdown_broken_path"
    assert link.target_note_id == "resources/term_dictionary/term_alpha.md"


def test_code_block_links_ignored(tmp_path):
    """Links inside fenced code blocks must not be indexed."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note("Alpha", body="ok.")
    )
    body_with_code = textwrap.dedent(
        """
        ```python
        # this is not a real link: [Alpha](term_alpha.md)
        ```
        """
    ).strip()
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _make_note("Beta", body=body_with_code)
    )
    db_path = tmp_path / "test.db"
    result = build(v, db_path)
    # The code-block "link" should NOT appear.
    assert result.links_indexed == 0


def test_skip_non_note_files_in_vault(tmp_path):
    """README.md / CHANGELOG.md / Rank_*.md must not be indexed."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_alpha.md").write_text(_make_note("Alpha"))
    (v / "README.md").write_text("# README\n")
    (v / "CHANGELOG.md").write_text("# Changelog\n")
    (v / "Rank_inlinks.md").write_text("ranking\n")
    db_path = tmp_path / "test.db"
    result = build(v, db_path)
    assert result.notes_indexed == 1


def test_database_folgezettel_root_traversal(tmp_path):
    """notes_by_folgezettel_root('7') returns 7 + 7a + 7a1 (LIKE '7%')."""
    v = tmp_path / "v"
    (v / "resources/analysis_thoughts").mkdir(parents=True)
    for fz in ["7", "7a", "7a1", "8"]:
        extra = f'folgezettel: "{fz}"\nfolgezettel_parent: null'
        (v / f"resources/analysis_thoughts/thought_{fz}.md").write_text(
            _make_note(
                f"Thought {fz}",
                second="analysis",
                bb="argument",
                extra_yaml=extra,
                body="ok.",
            )
        )
    db_path = tmp_path / "test.db"
    build(v, db_path)
    with Database(db_path) as db:
        trail_7 = db.notes_by_folgezettel_root("7")
    assert len(trail_7) == 3
    names = {n.note_name for n in trail_7}
    assert names == {"thought_7", "thought_7a", "thought_7a1"}


def test_indexer_against_real_vault():
    """Sanity-check: build the actual Tessellum vault and verify counts."""
    repo = Path(__file__).resolve().parents[2]
    vault = repo / "vault"
    if not vault.is_dir():
        pytest.skip(f"real vault not found at {vault}")
    db_path = repo / "data" / "tessellum-test-build.db"
    db_path.parent.mkdir(exist_ok=True)
    try:
        result = build(vault, db_path, force=True)
        assert result.notes_indexed >= 50  # at least the term_dictionary
        assert result.links_indexed >= 50
        with Database(db_path) as db:
            # Spot-check: term_building_block exists and has the right BB.
            note = db.note_by_id("resources/term_dictionary/term_building_block.md")
            assert note is not None
            assert note.building_block == "concept"
    finally:
        if db_path.is_file():
            db_path.unlink()
