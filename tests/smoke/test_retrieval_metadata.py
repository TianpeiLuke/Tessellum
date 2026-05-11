"""Smoke tests for tessellum.retrieval.metadata_search."""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.indexer import build
from tessellum.retrieval import MetadataHit, metadata_search


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
{extra_keywords}
topics:
  - X
  - Y
{extra_topics}
language: markdown
date of note: {date}
status: {status}
building_block: {bb}
{extra_yaml}
---

# {name}

Body.
"""


def _make_note(
    name: str,
    *,
    category: str = "resource",
    second: str = "terminology",
    bb: str = "concept",
    status: str = "active",
    date: str = "2026-05-10",
    extra_tags: str = "",
    extra_keywords: str = "",
    extra_topics: str = "",
    extra_yaml: str = "",
) -> str:
    return _NOTE_TEMPLATE.format(
        name=name,
        category=category,
        second=second,
        bb=bb,
        status=status,
        date=date,
        extra_tags=extra_tags,
        extra_keywords=extra_keywords,
        extra_topics=extra_topics,
        extra_yaml=extra_yaml,
    )


@pytest.fixture
def filter_db(tmp_path):
    """A small vault with diverse metadata for filter tests."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/skills").mkdir(parents=True)
    (v / "resources/analysis_thoughts").mkdir(parents=True)

    # Concept note, active, with custom tag
    (v / "resources/term_dictionary/term_alpha.md").write_text(
        _make_note(
            "Alpha",
            extra_tags="  - cqrs",
            extra_keywords="  - retrieval",
            extra_topics='  - "Knowledge Management"',
            date="2026-01-15",
        )
    )
    # Concept note, draft
    (v / "resources/term_dictionary/term_beta.md").write_text(
        _make_note("Beta", status="draft", date="2026-03-20")
    )
    # Skill note, active
    (v / "resources/skills/skill_demo.md").write_text(
        _make_note(
            "Demo",
            second="skill",
            bb="procedure",
            extra_tags="  - cqrs",
            date="2026-02-10",
        )
    )
    # Argument note in a folgezettel trail
    (v / "resources/analysis_thoughts/thought_root.md").write_text(
        _make_note(
            "Root",
            second="analysis",
            bb="argument",
            extra_yaml='folgezettel: "7"\nfolgezettel_parent: null',
            date="2026-04-01",
        )
    )
    # Argument note WITHOUT folgezettel
    (v / "resources/analysis_thoughts/thought_orphan.md").write_text(
        _make_note(
            "Orphan",
            second="analysis",
            bb="argument",
            date="2026-04-15",
        )
    )

    db_path = tmp_path / "filter.db"
    build(v, db_path, with_dense=False)
    return db_path


def test_no_filters_returns_all_notes(filter_db):
    hits = metadata_search(filter_db)
    assert len(hits) == 5


def test_filter_by_building_block(filter_db):
    hits = metadata_search(filter_db, building_block="concept")
    names = {h.note_name for h in hits}
    assert names == {"term_alpha", "term_beta"}


def test_filter_by_status(filter_db):
    hits = metadata_search(filter_db, status="draft")
    names = {h.note_name for h in hits}
    assert names == {"term_beta"}


def test_filter_by_category(filter_db):
    """All notes are tags[0]=resource in this fixture."""
    hits = metadata_search(filter_db, category="resource")
    assert len(hits) == 5


def test_filter_by_second_category(filter_db):
    hits = metadata_search(filter_db, second_category="skill")
    names = {h.note_name for h in hits}
    assert names == {"skill_demo"}


def test_filter_by_tag_uses_json_each(filter_db):
    """`tag='cqrs'` matches notes with cqrs in tags[] — exact value, not LIKE."""
    hits = metadata_search(filter_db, tag="cqrs")
    names = {h.note_name for h in hits}
    assert names == {"term_alpha", "skill_demo"}


def test_filter_by_keyword(filter_db):
    hits = metadata_search(filter_db, keyword="retrieval")
    names = {h.note_name for h in hits}
    assert names == {"term_alpha"}


def test_filter_by_topic(filter_db):
    hits = metadata_search(filter_db, topic="Knowledge Management")
    names = {h.note_name for h in hits}
    assert names == {"term_alpha"}


def test_filter_by_date_after(filter_db):
    hits = metadata_search(filter_db, date_after="2026-04-01")
    names = {h.note_name for h in hits}
    assert names == {"thought_root", "thought_orphan"}


def test_filter_by_date_before(filter_db):
    hits = metadata_search(filter_db, date_before="2026-02-15")
    names = {h.note_name for h in hits}
    assert names == {"term_alpha", "skill_demo"}


def test_filter_by_date_range(filter_db):
    hits = metadata_search(
        filter_db, date_after="2026-02-01", date_before="2026-03-31"
    )
    names = {h.note_name for h in hits}
    assert names == {"skill_demo", "term_beta"}


def test_filter_by_folgezettel_prefix(filter_db):
    hits = metadata_search(filter_db, folgezettel_prefix="7")
    names = {h.note_name for h in hits}
    assert names == {"thought_root"}


def test_filter_has_folgezettel_true(filter_db):
    hits = metadata_search(filter_db, has_folgezettel=True)
    names = {h.note_name for h in hits}
    assert names == {"thought_root"}


def test_filter_has_folgezettel_false(filter_db):
    hits = metadata_search(filter_db, has_folgezettel=False)
    names = {h.note_name for h in hits}
    # All non-trail notes
    assert names == {"term_alpha", "term_beta", "skill_demo", "thought_orphan"}


def test_filter_combines_filters_with_AND(filter_db):
    """Multiple filters AND-combine — building_block=concept AND tag=cqrs."""
    hits = metadata_search(filter_db, building_block="concept", tag="cqrs")
    names = {h.note_name for h in hits}
    assert names == {"term_alpha"}


def test_filter_no_match_returns_empty(filter_db):
    hits = metadata_search(filter_db, status="archived")
    assert hits == []


def test_filter_k_limits_results(filter_db):
    hits = metadata_search(filter_db, k=2)
    assert len(hits) == 2


def test_filter_k_zero_returns_empty(filter_db):
    hits = metadata_search(filter_db, k=0)
    assert hits == []


def test_filter_returns_typed_hits(filter_db):
    hits = metadata_search(filter_db, building_block="argument", k=1)
    assert hits, "expected at least one argument hit"
    h = hits[0]
    assert isinstance(h, MetadataHit)
    assert h.building_block == "argument"
    assert h.note_id.endswith(".md")


def test_filter_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        metadata_search(tmp_path / "missing.db", building_block="concept")


def test_filter_empty_string_folgezettel_treated_as_null(tmp_path):
    """Templates with `folgezettel: ""` shouldn't match has_folgezettel=True."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_template.md").write_text(
        _make_note(
            "Template",
            extra_yaml='folgezettel: ""\nfolgezettel_parent: ""',
        )
    )
    (v / "resources/term_dictionary/term_real.md").write_text(
        _make_note(
            "Real",
            extra_yaml='folgezettel: "1"\nfolgezettel_parent: null',
        )
    )
    db = tmp_path / "fz.db"
    build(v, db, with_dense=False)

    has_fz = metadata_search(db, has_folgezettel=True)
    names = {h.note_name for h in has_fz}
    # Empty string template should NOT appear; only real FZ note should.
    assert names == {"term_real"}


def test_filter_against_real_tessellum_vault():
    repo = Path(__file__).resolve().parents[2]
    vault = repo / "vault"
    if not vault.is_dir():
        pytest.skip(f"real vault not found at {vault}")
    db_path = repo / "data" / "tessellum-test-filter.db"
    db_path.parent.mkdir(exist_ok=True)
    try:
        build(vault, db_path, force=True, with_dense=False)
        # Concept BB filter should match all term_*.md notes (50+)
        concepts = metadata_search(db_path, building_block="concept", k=200)
        assert len(concepts) >= 30
        # FZ-trail notes are a strict subset of the vault (most notes have
        # no folgezettel; only argumentative trail nodes do). Property: ≥1
        # (trails are shipped), and a tight upper bound versus concepts.
        # We don't hard-code the exact count — the trail set grows by design
        # as new arguments descend into existing trails.
        trail = metadata_search(db_path, has_folgezettel=True, k=200)
        assert len(trail) >= 1
        assert len(trail) < len(concepts)
    finally:
        if db_path.is_file():
            db_path.unlink()
