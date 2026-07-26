"""Per-note related-notes enrichment (FZ 20k9d2 fix).

Covers: per-note query built from the note's OWN thesis+coverage, router-
dispatched retrieval (wires the orphaned router) + BFS expansion, relative-path
computation from target_path (so links resolve to real note_links edges),
self/dependency exclusion, dedup, cap, fail-soft (no db / missing / empty
query / no hits), and the ## References render shape.
"""

from __future__ import annotations

from pathlib import Path

from tessellum.composer.related_notes import (
    REFERENCES_HEADER,
    RelatedNote,
    _cap_with_term_quota,
    _deslug_title,
    enrich_related_notes,
    render_references,
)
from tessellum.indexer.build import _resolve_link, build


def _vault(tmp_path: Path) -> Path:
    """A tiny linked vault so BFS has a neighborhood to expand."""
    v = tmp_path / "vault"
    (v / "0_entry_points").mkdir(parents=True)
    (v / "resources").mkdir()
    (v / "0_entry_points" / "entry_reversal.md").write_text(
        "---\ntitle: Reversal\ntags: [entry_point]\n---\n# Reversal scoring\n"
        "The RnR BSM BERT model scores the reversal abuse domain. See "
        "[BSM model](../resources/note_bsm_model.md) and "
        "[Recall](../resources/note_recall.md).\n",
        encoding="utf-8",
    )
    (v / "resources" / "note_bsm_model.md").write_text(
        "---\ntitle: BSM model\ntags: [resource]\n---\n# BSM BERT model\n"
        "The model computes reversal abuse scores. "
        "Links [Recall](note_recall.md).\n",
        encoding="utf-8",
    )
    (v / "resources" / "note_recall.md").write_text(
        "---\ntitle: Recall\ntags: [resource]\n---\n# Recall at fixed FPR\n"
        "Recall is measured at a fixed false positive rate for the model.\n",
        encoding="utf-8",
    )
    return v


def _index(tmp_path: Path) -> Path:
    db = tmp_path / "idx.db"
    build(_vault(tmp_path), db, with_dense=False)  # BM25-only: no ML model needed
    return db


# ── fail-soft paths ─────────────────────────────────────────────────────────


def test_no_db_returns_empty_fail_soft() -> None:
    r = enrich_related_notes(thesis="reversal scoring", target_path="resources/x.md",
                             db_path=None)
    assert r.is_empty
    assert r.references_markdown == ""
    assert r.warning and "no index" in r.warning


def test_missing_index_fail_soft(tmp_path: Path) -> None:
    r = enrich_related_notes(thesis="reversal", target_path="resources/x.md",
                             db_path=tmp_path / "nope.db")
    assert r.is_empty
    assert "does not exist" in (r.warning or "")


def test_empty_query_fail_soft(tmp_path: Path) -> None:
    db = _index(tmp_path)
    # thesis with no alphanumeric tokens → empty FTS5 query → fail-soft.
    r = enrich_related_notes(thesis="---:#()", target_path="resources/x.md",
                             db_path=db, coverage=())
    assert r.is_empty
    assert "empty query" in (r.warning or "")


def test_no_hits_fail_soft(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(thesis="zzzznomatchxyzzy quuxnonsense",
                             target_path="resources/x.md", db_path=db)
    assert r.is_empty
    assert "no related notes" in (r.warning or "")


# ── happy path ──────────────────────────────────────────────────────────────


def test_retrieves_per_note_relevant(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(
        thesis="the reversal BSM model scores abuse and recall at fixed FPR",
        target_path="resources/note_new_reversal.md",
        db_path=db,
    )
    assert not r.is_empty
    ids = {rn.note_id for rn in r.related}
    assert any("note_bsm_model" in i or "note_recall" in i or "entry_reversal" in i
               for i in ids)


def test_excludes_self(tmp_path: Path) -> None:
    db = _index(tmp_path)
    # Writing note_bsm_model itself: it must never appear in its own references.
    r = enrich_related_notes(
        thesis="the BSM BERT model computes reversal abuse scores recall",
        target_path="resources/note_bsm_model.md",
        db_path=db,
    )
    assert all(rn.note_id != "resources/note_bsm_model.md" for rn in r.related)


def test_excludes_declared_dependencies(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(
        thesis="reversal BSM model recall scores abuse",
        target_path="resources/note_new.md",
        db_path=db,
        exclude_ids=("resources/note_recall.md",),
    )
    assert all(rn.note_id != "resources/note_recall.md" for rn in r.related)


def test_dedup_no_repeats(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(
        thesis="reversal model recall abuse scores fixed fpr",
        target_path="resources/note_new.md", db_path=db,
    )
    ids = [rn.note_id for rn in r.related]
    assert len(ids) == len(set(ids))


def test_cap_respected(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(
        thesis="reversal model recall abuse scores",
        target_path="resources/note_new.md", db_path=db, max_related=1,
    )
    assert len(r.related) <= 1


# ── relative-path correctness (this is what makes the edge resolve) ──────────


def test_rel_path_is_relative_to_target_dir(tmp_path: Path) -> None:
    db = _index(tmp_path)
    # New note in resources/ linking a sibling in resources/ → bare filename.
    r = enrich_related_notes(
        thesis="reversal BSM model recall abuse scores fixed fpr",
        target_path="resources/note_new.md", db_path=db,
    )
    by_id = {rn.note_id: rn for rn in r.related}
    if "resources/note_recall.md" in by_id:
        assert by_id["resources/note_recall.md"].rel_path == "note_recall.md"
    if "0_entry_points/entry_reversal.md" in by_id:
        # from resources/ up to 0_entry_points/
        assert by_id["0_entry_points/entry_reversal.md"].rel_path == \
            "../0_entry_points/entry_reversal.md"


def test_rel_path_from_deeper_target(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(
        thesis="reversal BSM model recall abuse scores",
        target_path="resources/term_dictionary/term_new.md", db_path=db,
    )
    by_id = {rn.note_id: rn for rn in r.related}
    if "resources/note_recall.md" in by_id:
        # from resources/term_dictionary/ up one to resources/
        assert by_id["resources/note_recall.md"].rel_path == "../note_recall.md"


# ── render shape (the indexer extracts these as edges) ───────────────────────


def test_render_references_shape() -> None:
    related = (
        RelatedNote("resources/note_recall.md", "note_recall", "note_recall.md",
                    0.9, "seed"),
        RelatedNote("0_entry_points/entry_reversal.md", "entry_reversal",
                    "../0_entry_points/entry_reversal.md", 0.5, "neighbor"),
    )
    md = render_references(related)
    assert md.startswith(REFERENCES_HEADER)
    # link TEXT is de-slugged (note_/entry_ prefix stripped); TARGET unchanged
    assert "- [recall](note_recall.md)" in md
    assert "- [reversal](../0_entry_points/entry_reversal.md)" in md


def test_render_empty_is_blank() -> None:
    assert render_references(()) == ""


# ── review-fix regressions ──────────────────────────────────────────────────


def test_deslug_title_strips_prefix_and_underscores() -> None:
    # Review-fix: link TEXT must be human-readable, not a raw slug.
    assert _deslug_title("term_zettelkasten") == "zettelkasten"
    assert _deslug_title("model_neat_appeal_aam") == "neat appeal aam"
    assert _deslug_title("entry_reversal_scoring") == "reversal scoring"
    # unknown/no prefix → just underscores→spaces
    assert _deslug_title("plain_note") == "plain note"
    # a bare prefix-only stem is not stripped (guard: len(body) > len(prefix))
    # but underscores still normalize, so "term_" → "term" (never empties)
    assert _deslug_title("term_") == "term"
    assert _deslug_title("") == ""


def test_render_uses_deslugged_title_but_keeps_rel_path() -> None:
    related = (
        RelatedNote("resources/term_dictionary/term_recall.md", "term_recall",
                    "../term_dictionary/term_recall.md", 0.9, "seed"),
    )
    md = render_references(related)
    # link TEXT de-slugged, link TARGET (rel_path) untouched
    assert "- [recall](../term_dictionary/term_recall.md)" in md


def test_dense_query_is_raw_prose_not_or_bag(tmp_path: Path) -> None:
    # Review-fix (CONFIRMED): the dense arm must receive the RAW thesis, not the
    # FTS5 OR-bag. Assert route() is called with dense_query = raw prose while
    # the bm25 query is the OR-joined sanitized bag.
    import tessellum.composer.related_notes as rn

    db = _index(tmp_path)
    captured = {}

    real_route = None
    from tessellum.retrieval import router as router_mod
    real_route = router_mod.route

    def spy_route(dbp, query, *, dense_query=None, k=20):
        captured["query"] = query
        captured["dense_query"] = dense_query
        return real_route(dbp, query, dense_query=dense_query, k=k)

    router_mod.route = spy_route
    try:
        rn.enrich_related_notes(
            thesis="Reversal scoring uses the BSM model",
            target_path="resources/note_new.md", db_path=db,
        )
    finally:
        router_mod.route = real_route

    assert " OR " in captured["query"]  # bm25 arm gets the sanitized OR-bag
    assert captured["dense_query"] == "Reversal scoring uses the BSM model"  # raw


def test_term_quota_pulls_term_notes_into_the_cap() -> None:
    # Review-fix: a flat top-N cut can drop term notes below the fold; the term
    # quota swaps the lowest-ranked non-term notes for the best tail term notes.
    ordered = [
        RelatedNote(f"resources/note_x{i}.md", f"note_x{i}", f"note_x{i}.md",
                    1.0 - i * 0.01, "seed")
        for i in range(6)  # 6 non-term, high scores
    ] + [
        RelatedNote(f"resources/term_dictionary/term_t{i}.md", f"term_t{i}",
                    f"../term_dictionary/term_t{i}.md", 0.5 - i * 0.01, "seed")
        for i in range(4)  # 4 term notes, lower scores
    ]
    capped = _cap_with_term_quota(ordered, max_related=6, min_term_notes=3)
    assert len(capped) == 6
    n_terms = sum(1 for r in capped if "/term_" in r.note_id)
    assert n_terms >= 3, f"term quota not honored: {[r.note_id for r in capped]}"


def test_term_quota_noop_when_enough_terms_in_head() -> None:
    ordered = [
        RelatedNote(f"resources/term_dictionary/term_t{i}.md", f"term_t{i}",
                    f"../term_dictionary/term_t{i}.md", 1.0 - i * 0.01, "seed")
        for i in range(6)
    ]
    capped = _cap_with_term_quota(ordered, max_related=4, min_term_notes=3)
    assert len(capped) == 4
    assert all("/term_" in r.note_id for r in capped)


def test_enriched_rel_paths_resolve_to_real_indexer_edges(tmp_path: Path) -> None:
    # THE load-bearing guarantee: an emitted rel_path, resolved by the ACTUAL
    # indexer (_resolve_link, which resolves relative to the authoring note's
    # own dir), yields a real 'markdown' edge — not a ghost. This is what makes
    # the related notes become knowledge-graph note_links.
    vault = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(vault, db, with_dense=False)
    # a NEW note nested one level deeper than the retrieved resources/ notes
    (vault / "resources" / "term_dictionary").mkdir(parents=True, exist_ok=True)
    target_path = "resources/term_dictionary/term_new.md"
    r = enrich_related_notes(
        thesis="reversal BSM model recall abuse scores fixed fpr",
        target_path=target_path, db_path=db,
    )
    assert not r.is_empty
    src_note_path = vault / target_path
    for rn in r.related:
        resolved, ghost = _resolve_link(rn.rel_path, vault, src_note_path)
        assert resolved == rn.note_id, (
            f"rel_path {rn.rel_path!r} did not resolve to {rn.note_id!r} "
            f"(got {resolved!r}, ghost={ghost!r}) — no edge would be created"
        )


def test_result_carries_rendered_references(tmp_path: Path) -> None:
    db = _index(tmp_path)
    r = enrich_related_notes(
        thesis="reversal BSM model recall abuse scores fixed fpr",
        target_path="resources/note_new.md", db_path=db,
    )
    if not r.is_empty:
        assert r.references_markdown.startswith(REFERENCES_HEADER)
        # every rendered link target is one of the related rel_paths
        for rn in r.related:
            assert f"]({rn.rel_path})" in r.references_markdown
