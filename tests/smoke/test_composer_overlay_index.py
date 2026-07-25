"""P3 — OverlayIndex read-through over ``base ⊕ delta`` (A3.1/A3.2).

Proves the overlay is a correct read surface for create/update/delete + ghost
resolution + dedup — the semantics a naive ``base UNION delta`` gets wrong:
  1. a staged CREATE is visible over the base (read-your-writes);
  2. a staged UPDATE SHADOWS the base row (delta wins, not both);
  3. a staged DELETE TOMBSTONES the base row (gone from every query) and turns
     a base link pointing at it into a fresh ghost;
  4. a staged note RESOLVES a pre-existing base ghost (broken link → resolved);
  5. links_from/links_to/all_links/counts merge deterministically;
  6. staged inbound backlinks from unwritten notes (absent from base) are seen.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer.overlay_index import OverlayIndex
from tessellum.indexer import Database, build
from tessellum.indexer.db import LinkRow, NoteRow


_NOTE = """\
---
tags:
  - resource
  - terminology
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
building_block: concept
---

# {name}

{body}
"""


def _write(vault: Path, rel: str, name: str, body: str) -> None:
    p = vault / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_NOTE.format(name=name, body=body), encoding="utf-8")


@pytest.fixture
def base_db(tmp_path: Path) -> Database:
    """A tiny base vault: alpha -> beta (resolved). NOTE: the shipped indexer
    DROPS broken links at build time, so a dangling reference only exists in
    the overlay as a staged link (b2), never as a base row."""
    vault = tmp_path / "v"
    _write(
        vault,
        "resources/term_dictionary/term_alpha.md",
        "Term: Alpha",
        "See [Beta](term_beta.md).",
    )
    _write(vault, "resources/term_dictionary/term_beta.md", "Term: Beta", "Body.")
    db_path = tmp_path / "index.db"
    build(vault, db_path)
    return Database(db_path)


def _note_row(note_id: str, name: str) -> NoteRow:
    return NoteRow(
        note_id=note_id, note_name=name, note_location="resources/term_dictionary",
        note_category="resource", note_second_category="terminology",
        note_status="active", note_creation_date="2026-05-10", note_update_date=None,
        file_path=note_id, file_size_bytes=10, tags=("resource", "terminology"),
        keywords=("a", "b", "c"), topics=("X",), language="markdown",
        building_block="concept", folgezettel=None, folgezettel_parent=None,
        indexed_at=None, last_indexed_mtime=None,
    )


def _link(src: str, tgt: str) -> LinkRow:
    return LinkRow(
        link_id=0, source_note_id=src, target_note_id=tgt,
        link_context=None, link_type="markdown", created_at=None,
    )


# note_id is the vault-relative path in this index
_ALPHA = "resources/term_dictionary/term_alpha.md"
_BETA = "resources/term_dictionary/term_beta.md"
_GHOST = "resources/term_dictionary/term_ghost.md"
_GAMMA = "resources/term_dictionary/term_gamma.md"


def test_base_visible_and_read_your_writes(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    assert ix.exists(_ALPHA)
    assert ix.note_count() == 2
    # 1. staged create is visible over the base (read-your-writes).
    ix.stage_add(_note_row(_GAMMA, "Term: Gamma"))
    assert ix.exists(_GAMMA)
    assert ix.note_count() == 3
    assert ix.note_by_id(_GAMMA).note_name == "Term: Gamma"


def test_update_shadows_base_not_duplicates(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    updated = _note_row(_BETA, "Term: Beta v2")
    ix.stage_update(_BETA, updated)
    # 2. shadow: delta wins, base row does NOT also appear (count unchanged).
    assert ix.note_count() == 2
    assert ix.note_by_id(_BETA).note_name == "Term: Beta v2"
    names = [n.note_name for n in ix.all_notes() if n.note_id == _BETA]
    assert names == ["Term: Beta v2"]  # exactly one, shadowed


def test_delete_tombstones_and_creates_ghost(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    # base has alpha -> beta (resolved). Delete beta.
    ix.stage_delete(_BETA)
    # 3. tombstone: beta gone from every query.
    assert not ix.exists(_BETA)
    assert ix.note_count() == 1
    assert _BETA not in {n.note_id for n in ix.all_notes()}
    # the base link alpha -> beta is now a fresh ghost (target no longer exists).
    ghosts = {(g.source_note_id, g.target_note_id) for g in ix.ghost_links()}
    assert (_ALPHA, _BETA) in ghosts


def test_staged_note_resolves_staged_ghost(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    # Stage a link alpha -> ghost whose target doesn't exist yet: it's a ghost.
    ix.stage_link(_link(_ALPHA, _GHOST))
    assert (_ALPHA, _GHOST) in {
        (g.source_note_id, g.target_note_id) for g in ix.ghost_links()
    }
    assert ix.resolves_ghost(_GHOST) is False  # target not staged yet
    # Stage the target note → the dangling reference resolves.
    ix.stage_add(_note_row(_GHOST, "Term: Ghost"))
    assert ix.resolves_ghost(_GHOST) is True
    assert (_ALPHA, _GHOST) not in {
        (g.source_note_id, g.target_note_id) for g in ix.ghost_links()
    }


def test_links_merge_and_backlink_from_unwritten(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    base_link_count = base_db.link_count()
    # 6. an inbound backlink from a not-yet-written note (gamma -> alpha) is
    # absent from the base index; staging it makes it visible over the overlay.
    ix.stage_add(_note_row(_GAMMA, "Term: Gamma"))
    ix.stage_link(_link(_GAMMA, _ALPHA))
    assert ix.link_count() == base_link_count + 1
    incoming_alpha = {lk.source_note_id for lk in ix.links_to(_ALPHA)}
    assert _GAMMA in incoming_alpha
    # 5. deterministic ordering: all_links is sorted by (source, target).
    keys = [(lk.source_note_id, lk.target_note_id) for lk in ix.all_links()]
    assert keys == sorted(keys)


def test_delta_is_isolated_from_base(base_db: Database) -> None:
    # The overlay must NEVER mutate the base index.
    ix = OverlayIndex(base_db)
    ix.stage_add(_note_row(_GAMMA, "Term: Gamma"))
    ix.stage_delete(_BETA)
    # base is untouched: still 2 notes, beta still present.
    assert base_db.note_count() == 2
    assert base_db.note_by_id(_BETA) is not None
    assert base_db.note_by_id(_GAMMA) is None


def test_rename_tombstones_old_and_adds_new(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    new_id = "resources/term_dictionary/term_beta_renamed.md"
    ix.stage_update(_BETA, _note_row(new_id, "Term: Beta"))
    assert not ix.exists(_BETA)  # old path tombstoned
    assert ix.exists(new_id)  # new path present
    assert ix.note_count() == 2  # net zero (one out, one in)


# ── Regression: link semantics under delete/rename/dup (review nits) ────────


def test_deleted_source_drops_its_outbound_links(base_db: Database) -> None:
    # base: alpha -> beta. Deleting alpha must drop alpha's outbound link
    # (a deleted note authors nothing), not leave it dangling.
    ix = OverlayIndex(base_db)
    assert ix.link_count() == 1
    ix.stage_delete(_ALPHA)
    assert ix.link_count() == 0
    assert ix.links_from(_ALPHA) == []
    assert ix.links_to(_BETA) == []


def test_delete_note_and_target_no_phantom_ghost(base_db: Database) -> None:
    # Deleting BOTH endpoints of alpha -> beta must not report a phantom ghost
    # (the link's source is gone, so the edge is gone — nothing dangling).
    ix = OverlayIndex(base_db)
    ix.stage_delete(_ALPHA)
    ix.stage_delete(_BETA)
    assert ix.ghost_links() == []
    assert ix.link_count() == 0


def test_rename_does_not_double_count_outbound_link(base_db: Database) -> None:
    # Rename alpha -> alpha2 and re-stage its re-parsed outbound link.
    ix = OverlayIndex(base_db)
    alpha2 = "resources/term_dictionary/term_alpha2.md"
    ix.stage_update(_ALPHA, _note_row(alpha2, "Term: Alpha2"))
    ix.stage_link(_link(alpha2, _BETA))
    # exactly one outbound edge (alpha2 -> beta); the tombstoned alpha's base
    # edge is gone (no phantom), no double-count.
    assert ix.link_count() == 1
    keys = {(lk.source_note_id, lk.target_note_id) for lk in ix.all_links()}
    assert keys == {(alpha2, _BETA)}
    assert {lk.source_note_id for lk in ix.links_to(_BETA)} == {alpha2}


def test_identical_base_and_staged_edge_dedups(base_db: Database) -> None:
    # A same-path update re-materializes the SAME alpha -> beta edge. It must
    # collapse to one row (published note_links has UNIQUE(source,target)).
    ix = OverlayIndex(base_db)
    ix.stage_link(_link(_ALPHA, _BETA))  # duplicate of the base edge
    assert ix.link_count() == 1
    assert len(ix.links_to(_BETA)) == 1
    assert len(ix.links_from(_ALPHA)) == 1


def test_stage_unlink_retracts_edge(base_db: Database) -> None:
    ix = OverlayIndex(base_db)
    assert ix.link_count() == 1
    ix.stage_unlink(_ALPHA, _BETA)
    assert ix.link_count() == 0
    assert ix.links_from(_ALPHA) == []


def test_restage_after_unlink_is_read_your_writes(base_db: Database) -> None:
    # BUG1 regression: unlink then re-stage the SAME edge → it must reappear
    # (read-your-writes; symmetric with create-after-delete un-tombstoning).
    ix = OverlayIndex(base_db)
    ix.stage_unlink(_ALPHA, _BETA)
    assert ix.link_count() == 0
    ix.stage_link(_link(_ALPHA, _BETA))
    assert ix.link_count() == 1
    assert {(lk.source_note_id, lk.target_note_id) for lk in ix.all_links()} == {
        (_ALPHA, _BETA)
    }


def test_clear_then_restage_update_pattern(base_db: Database) -> None:
    # BUG1 regression (the natural writer pattern): a same-path update clears
    # its old edges then re-stages the current ones; an UNCHANGED edge that is
    # cleared+restaged must survive, a new edge is added.
    ix = OverlayIndex(base_db)
    gamma = "resources/term_dictionary/term_gamma.md"
    ix.stage_add(_note_row(gamma, "Term: Gamma"))  # target for the new edge
    ix.stage_unlink(_ALPHA, _BETA)            # clear old
    ix.stage_link(_link(_ALPHA, _BETA))       # restage unchanged
    ix.stage_link(_link(_ALPHA, gamma))       # add new
    keys = {(lk.source_note_id, lk.target_note_id) for lk in ix.all_links()}
    assert keys == {(_ALPHA, _BETA), (_ALPHA, gamma)}


def test_create_after_delete_does_not_resurrect_base_edges(base_db: Database) -> None:
    # BUG2 regression: delete alpha (drops its base edge), then re-create a new
    # note at the same path whose content does NOT link beta. The stale base
    # edge alpha->beta must NOT come back.
    ix = OverlayIndex(base_db)
    ix.stage_delete(_ALPHA)
    assert ix.links_from(_ALPHA) == []
    ix.stage_add(_note_row(_ALPHA, "Alpha v2 — no link to beta"))
    assert ix.links_from(_ALPHA) == []  # re-created note carries only staged edges
    assert ix.link_count() == 0


def test_reauthored_note_uses_only_staged_edges(base_db: Database) -> None:
    # A same-path update (alpha re-authored) declares its own edges: base
    # alpha->beta is superseded; only the staged edge (alpha->gamma) remains.
    ix = OverlayIndex(base_db)
    gamma = "resources/term_dictionary/term_gamma.md"
    ix.stage_add(_note_row(gamma, "Term: Gamma"))
    ix.stage_update(_ALPHA, _note_row(_ALPHA, "Alpha v2"))  # re-authored, same path
    ix.stage_link(_link(_ALPHA, gamma))
    keys = {(lk.source_note_id, lk.target_note_id) for lk in ix.links_from(_ALPHA)}
    assert keys == {(_ALPHA, gamma)}  # base alpha->beta NOT inherited
