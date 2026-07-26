"""E2 — wiring per-note related-notes enrichment into the execute wave.

Verifies the leaf-enrichment seam (``_enrich_leaves_with_related_notes``): each
projected note leaf gains ``related_notes`` + ``related_references_md`` when a
live index is supplied, passes through byte-identical when it is not, and
degrades fail-soft per leaf. The enrichment is keyed on EACH leaf's own thesis
(per-note relevance, not a shared query).
"""

from __future__ import annotations

from pathlib import Path

from tessellum.composer.digestion import _enrich_leaves_with_related_notes
from tessellum.composer.knowledge_plan import (
    ClaimProvenance,
    NoteIntent,
    NoteIntentGraph,
    project_note_intent_graph,
)
from tessellum.indexer.build import build


def _vault(tmp_path: Path) -> Path:
    v = tmp_path / "vault"
    (v / "resources").mkdir(parents=True)
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
    build(_vault(tmp_path), db, with_dense=False)
    return db


def _leaves() -> list[dict]:
    graph = NoteIntentGraph(
        objective_id="obj",
        intents=(
            NoteIntent(
                note_id="n1",
                thesis="the reversal BSM model computes abuse scores and recall",
                building_block="concept",
                target_path="resources/note_new_model.md",
                coverage=("reversal", "recall"),
                provenance=(ClaimProvenance(span_id="s1", source_ref="src#1"),),
            ),
        ),
    )
    return project_note_intent_graph(graph)


def test_none_db_stamps_empty_on_note_leaves() -> None:
    # With no index (db=None), note-bearing leaves are stamped with EMPTY
    # related_notes/related_references_md so the writer's placeholder renders ""
    # (a clean empty block), never a <missing …> sentinel. Fail-soft, no crash.
    leaves = _leaves()
    out = _enrich_leaves_with_related_notes(leaves, related_notes_db=None)
    assert out[0]["related_notes"] == []
    assert out[0]["related_references_md"] == ""
    # the caller's original leaf is not mutated
    assert "related_notes" not in leaves[0]


def test_enriches_each_leaf_with_related_notes(tmp_path: Path) -> None:
    db = _index(tmp_path)
    out = _enrich_leaves_with_related_notes(_leaves(), related_notes_db=db)
    leaf = out[0]
    assert "related_notes" in leaf
    assert "related_references_md" in leaf
    # at least one real vault note retrieved, keyed on THIS note's thesis
    assert leaf["related_notes"], "expected per-note related notes"
    ids = {rn["note_id"] for rn in leaf["related_notes"]}
    assert any("note_bsm_model" in i or "note_recall" in i for i in ids)
    # rendered references block is present + uses resolvable relative links
    md = leaf["related_references_md"]
    assert md.startswith("## References")
    for rn in leaf["related_notes"]:
        assert f"]({rn['rel_path']})" in md


def test_original_leaf_not_mutated(tmp_path: Path) -> None:
    db = _index(tmp_path)
    leaves = _leaves()
    _enrich_leaves_with_related_notes(leaves, related_notes_db=db)
    # the enrichment builds NEW leaf dicts; the caller's input is untouched.
    assert "related_notes" not in leaves[0]


def test_whole_plan_fallback_leaf_passes_through(tmp_path: Path) -> None:
    # A leaf with no typed ``note`` payload (the whole-plan fallback) must NOT
    # be enriched — it has no per-note thesis/target to key on.
    db = _index(tmp_path)
    fallback = [{"plan_path": "plans/p.md", "total_notes": 3}]
    out = _enrich_leaves_with_related_notes(fallback, related_notes_db=db)
    assert out[0] == fallback[0]
    assert "related_notes" not in out[0]


def test_missing_index_degrades_per_leaf(tmp_path: Path) -> None:
    # db path given but non-existent → each leaf gets an EMPTY related_notes
    # (fail-soft), never a crash.
    out = _enrich_leaves_with_related_notes(
        _leaves(), related_notes_db=tmp_path / "nope.db"
    )
    assert out[0]["related_notes"] == []
    assert out[0]["related_references_md"] == ""


def test_non_iterable_depends_on_does_not_crash(tmp_path: Path) -> None:
    # Review-fix (CONFIRMED): an opt-in execute_leaves leaf (not the typed
    # projection) could carry a non-iterable depends_on; tuple(5) would raise
    # and kill the wave. The guard must degrade that leaf, not crash.
    db = _index(tmp_path)
    bad_leaf = {
        "note": {"thesis": "reversal BSM model recall abuse", "depends_on": 5},
        "target_path": "resources/note_new.md",
    }
    out = _enrich_leaves_with_related_notes([bad_leaf], related_notes_db=db)
    assert "related_notes" in out[0]  # enriched, not crashed


def test_excludes_self_when_writing_existing_note(tmp_path: Path) -> None:
    db = _index(tmp_path)
    graph = NoteIntentGraph(
        objective_id="obj",
        intents=(
            NoteIntent(
                note_id="n1",
                thesis="the BSM BERT model computes reversal abuse scores recall",
                building_block="concept",
                target_path="resources/note_bsm_model.md",  # writing this note
                provenance=(ClaimProvenance(span_id="s1", source_ref="src#1"),),
            ),
        ),
    )
    out = _enrich_leaves_with_related_notes(
        project_note_intent_graph(graph), related_notes_db=db
    )
    ids = {rn["note_id"] for rn in out[0]["related_notes"]}
    assert "resources/note_bsm_model.md" not in ids  # never links itself
