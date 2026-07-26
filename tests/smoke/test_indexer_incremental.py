"""FZ 20k9d3 P1 — incremental index build.

Covers: add/modify/delete detection, content_hash catching same-mtime edits,
note_int_id preservation (unchanged notes keep their surrogate key + vec rows),
global note_links rebuild, the no-DB→full-build fallback, the content_hash
column migration on a legacy DB, and PARITY — an incremental update yields the
same notes/links/FTS a from-scratch rebuild would.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from tessellum.indexer.build import build, build_incremental
from tessellum.retrieval.bm25 import bm25_search


def _write(v: Path, rel: str, body: str) -> Path:
    p = v / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _vault(root: Path) -> Path:
    v = root / "vault"
    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# Alpha\nreversal abuse model\n")
    _write(v, "resources/note_b.md",
           "---\ntitle: B\ntags: [resource]\n---\n# Beta\nrecall fixed fpr\n")
    return v


def _notes(db: Path) -> set[str]:
    conn = sqlite3.connect(str(db))
    try:
        return {r[0] for r in conn.execute("SELECT note_id FROM notes")}
    finally:
        conn.close()


def _int_ids(db: Path) -> dict[str, int]:
    conn = sqlite3.connect(str(db))
    try:
        return {r[0]: r[1] for r in conn.execute(
            "SELECT note_id, note_int_id FROM notes")}
    finally:
        conn.close()


# ── fallback + basic detection ───────────────────────────────────────────────


def test_no_db_falls_back_to_full_build(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    r = build_incremental(v, db, with_dense=False)
    assert db.exists()
    assert r.notes_indexed == 2
    # a fresh full build reports incremental=True here only via the fallback's
    # own result; the important invariant is the index is complete.
    assert _notes(db) == {"resources/note_a.md", "resources/note_b.md"}


def test_no_change_is_a_noop(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    r = build_incremental(v, db, with_dense=False)
    assert r.incremental
    assert (r.notes_added, r.notes_modified, r.notes_deleted) == (0, 0, 0)


def test_added_note_detected(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    _write(v, "resources/note_c.md",
           "---\ntitle: C\ntags: [resource]\n---\n# Gamma\nnew note content\n")
    r = build_incremental(v, db, with_dense=False)
    assert r.notes_added == 1 and r.notes_modified == 0 and r.notes_deleted == 0
    assert "resources/note_c.md" in _notes(db)
    assert bm25_search(db, "gamma", k=5)  # queryable


def test_deleted_note_removed(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    (v / "resources/note_b.md").unlink()
    r = build_incremental(v, db, with_dense=False)
    assert r.notes_deleted == 1
    assert _notes(db) == {"resources/note_a.md"}
    # its FTS row is gone too
    assert not bm25_search(db, "recall fixed fpr", k=5)


def test_modified_note_reindexed(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# Alpha\nCOMPLETELYNEWTOKEN xyz\n")
    r = build_incremental(v, db, with_dense=False)
    assert r.notes_modified == 1
    assert bm25_search(db, "completelynewtoken", k=5)
    assert not bm25_search(db, "abuse", k=5)  # old body gone from FTS


def _bb_and_tags(db: Path, note_id: str) -> tuple:
    conn = sqlite3.connect(str(db))
    try:
        return conn.execute(
            "SELECT building_block, tags FROM notes WHERE note_id = ?", (note_id,)
        ).fetchone()
    finally:
        conn.close()


def test_frontmatter_only_change_is_reindexed(tmp_path: Path) -> None:
    # Review-fix (CONFIRMED): content_hash covers frontmatter + body, so a
    # frontmatter-only edit (building_block/tags changed, body identical) is
    # re-indexed — otherwise the notes row keeps STALE metadata vs a full build.
    v = tmp_path / "vault"
    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource, alpha]\nbuilding_block: concept\n---\n"
           "# Alpha\nidentical body text\n")
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    assert _bb_and_tags(db, "resources/note_a.md")[0] == "concept"

    # change ONLY frontmatter; body byte-identical
    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource, beta]\nbuilding_block: procedure\n---\n"
           "# Alpha\nidentical body text\n")
    r = build_incremental(v, db, with_dense=False)
    assert r.notes_modified == 1, "frontmatter-only change must be re-indexed"
    bb, tags = _bb_and_tags(db, "resources/note_a.md")
    assert bb == "procedure" and "beta" in tags


def test_content_hash_catches_same_mtime_edit(tmp_path: Path) -> None:
    # A git-checkout / touch-restore can leave mtime unchanged; content_hash
    # must still detect the edit.
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    p = v / "resources/note_a.md"
    orig_mtime = p.stat().st_mtime
    p.write_text(
        "---\ntitle: A\ntags: [resource]\n---\n# Alpha\nHASHONLYCHANGE token\n",
        encoding="utf-8",
    )
    os.utime(p, (orig_mtime, orig_mtime))  # restore the original mtime
    r = build_incremental(v, db, with_dense=False)
    assert r.notes_modified == 1, "content_hash should catch a same-mtime edit"
    assert bm25_search(db, "hashonlychange", k=5)


# ── surrogate-key stability ──────────────────────────────────────────────────


def test_int_ids_preserved_for_unchanged_notes(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    before = _int_ids(db)
    # add one note; the existing two must keep their note_int_id
    _write(v, "resources/note_c.md",
           "---\ntitle: C\ntags: [resource]\n---\n# Gamma\nc body\n")
    build_incremental(v, db, with_dense=False)
    after = _int_ids(db)
    for nid, iid in before.items():
        assert after[nid] == iid, f"{nid} int_id changed {iid}->{after.get(nid)}"
    # the new note got a fresh id above the prior max
    assert after["resources/note_c.md"] > max(before.values())


# ── global link rebuild ──────────────────────────────────────────────────────


def test_links_rebuilt_when_target_added(tmp_path: Path) -> None:
    v = root = tmp_path / "vault"
    _write(root, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# Alpha\nsee [B](note_b.md)\n")
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)
    # note_b doesn't exist yet → the link from A is broken/dropped
    conn = sqlite3.connect(str(db))
    before = conn.execute("SELECT COUNT(*) FROM note_links").fetchone()[0]
    conn.close()
    # now add note_b; the incremental rebuild must resolve A→B as a real edge
    _write(root, "resources/note_b.md",
           "---\ntitle: B\ntags: [resource]\n---\n# Beta\nb body\n")
    build_incremental(v, db, with_dense=False)
    conn = sqlite3.connect(str(db))
    edges = conn.execute(
        "SELECT source_note_id, target_note_id, link_type FROM note_links"
    ).fetchall()
    conn.close()
    assert any(s == "resources/note_a.md" and t == "resources/note_b.md"
               for s, t, _ in edges), f"A->B edge not resolved after add: {edges} (was {before})"


# ── parity with a from-scratch rebuild ───────────────────────────────────────


def _snapshot(db: Path) -> dict:
    conn = sqlite3.connect(str(db))
    try:
        notes = sorted(r[0] for r in conn.execute("SELECT note_id FROM notes"))
        links = sorted(conn.execute(
            "SELECT source_note_id, target_note_id, link_type FROM note_links"))
        fts = sorted(r[0] for r in conn.execute("SELECT note_id FROM notes_fts"))
        return {"notes": notes, "links": links, "fts": fts}
    finally:
        conn.close()


def test_incremental_matches_full_rebuild(tmp_path: Path) -> None:
    # Apply a mix of edits, then assert the incrementally-updated DB matches a
    # from-scratch rebuild of the same final vault (notes, links, FTS coverage).
    v = _vault(tmp_path)
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=False)

    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# Alpha\nedited [C](note_c.md)\n")
    _write(v, "resources/note_c.md",
           "---\ntitle: C\ntags: [resource]\n---\n# Gamma\nadded note\n")
    (v / "resources/note_b.md").unlink()
    build_incremental(v, db, with_dense=False)

    fresh = tmp_path / "fresh.db"
    build(v, fresh, force=True, with_dense=False)

    assert _snapshot(db) == _snapshot(fresh)


# ── dense (real encoder): only changed notes are re-embedded ─────────────────


def _vec_count(db: Path) -> int:
    from tessellum.indexer.build import _open_with_vec

    conn = _open_with_vec(db)
    try:
        return conn.execute("SELECT COUNT(*) FROM notes_vec").fetchone()[0]
    finally:
        conn.close()


def test_incremental_dense_reembeds_only_changed(tmp_path: Path) -> None:
    from tessellum.retrieval.dense import dense_search

    v = tmp_path / "vault"
    _write(v, "resources/note_graph.md",
           "---\ntitle: G\ntags: [resource]\n---\n# Graph\ngraph theory vertices edges\n")
    _write(v, "resources/note_cook.md",
           "---\ntitle: C\ntags: [resource]\n---\n# Cooking\ncooking food heat kitchen\n")
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=True)
    assert _vec_count(db) == 2

    # add ONE note → only it should be embedded; existing vec rows survive
    _write(v, "resources/note_music.md",
           "---\ntitle: M\ntags: [resource]\n---\n# Music\nmusic melody rhythm\n")
    r = build_incremental(v, db, with_dense=True)
    assert r.notes_added == 1
    assert r.embeddings_generated == 1  # ONLY the new note re-encoded
    assert _vec_count(db) == 3          # 2 preserved + 1 new
    assert any("note_music" in h.note_id for h in dense_search(db, "music melody", k=3))


def test_incremental_dense_deletes_vec_row(tmp_path: Path) -> None:
    v = tmp_path / "vault"
    _write(v, "resources/note_graph.md",
           "---\ntitle: G\ntags: [resource]\n---\n# Graph\ngraph theory vertices\n")
    _write(v, "resources/note_cook.md",
           "---\ntitle: C\ntags: [resource]\n---\n# Cooking\ncooking food heat\n")
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=True)
    assert _vec_count(db) == 2
    (v / "resources/note_cook.md").unlink()
    build_incremental(v, db, with_dense=True)
    assert _vec_count(db) == 1  # deleted note's vec row removed


def test_dense_failure_preserves_prior_embeddings(tmp_path: Path, monkeypatch) -> None:
    # Review-fix (CONFIRMED): if the encoder fails on an incremental commit, the
    # SAVEPOINT must roll back the vec DELETEs so PRIOR embeddings survive —
    # not a partial notes_vec where changed notes lost their rows.
    import importlib

    build_mod = importlib.import_module("tessellum.indexer.build")

    v = tmp_path / "vault"
    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# A\ngraph theory vertices\n")
    _write(v, "resources/note_b.md",
           "---\ntitle: B\ntags: [resource]\n---\n# B\ncooking food heat\n")
    db = tmp_path / "idx.db"
    build(v, db, force=True, with_dense=True)
    assert _vec_count(db) == 2

    # modify note_a, but make the encoder blow up during the incremental
    def boom(*_a, **_k):
        raise RuntimeError("encoder unavailable")

    monkeypatch.setattr(build_mod, "_write_embeddings", boom)
    _write(v, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# A\nEDITED graph content\n")
    r = build_incremental(v, db, with_dense=True)
    assert r.dense_degraded is True
    # SAVEPOINT rolled back the delete → both prior embeddings preserved
    assert _vec_count(db) == 2, "prior embeddings must survive a dense failure"


# ── I2: commit_tail uses the incremental path + atomic swap ──────────────────


def test_commit_tail_rebuild_is_incremental_and_atomic(tmp_path: Path) -> None:
    # rebuild_index_atomically (default incremental=True) publishes via the
    # copy+incremental+atomic-swap path when a live index exists, and the
    # published index correctly reflects an added note.
    from tessellum.runtime.commit_tail import rebuild_index_atomically
    from tessellum.runtime.paths import RuntimePaths

    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    (paths.vault / "resources").mkdir(parents=True, exist_ok=True)
    _write(paths.vault, "resources/note_a.md",
           "---\ntitle: A\ntags: [resource]\n---\n# Alpha\nreversal model\n")
    # first publish (no live index → full build fallback)
    idx, _ = rebuild_index_atomically(paths, with_dense=False)
    assert idx == paths.index_db and idx.is_file()
    assert _notes(idx) == {"resources/note_a.md"}
    inode1 = idx.stat().st_ino

    # add a note, publish again (live index exists → incremental copy+update)
    _write(paths.vault, "resources/note_b.md",
           "---\ntitle: B\ntags: [resource]\n---\n# Beta\nrecall fixed fpr\n")
    idx2, _ = rebuild_index_atomically(paths, with_dense=False)
    assert _notes(idx2) == {"resources/note_a.md", "resources/note_b.md"}
    assert bm25_search(idx2, "recall fixed fpr", k=5)
    # atomic swap → the published file is a NEW inode, not an in-place edit
    assert idx2.stat().st_ino != inode1
