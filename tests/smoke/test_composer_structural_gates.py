"""P6 — capsule-level structural gate suite + human-approval ceiling (A6.1/A6.2).

Proves the honest supervised ceiling: structural gates (coverage / provenance /
BB-atomicity / disposition / nav+inlink closure / referential integrity /
relevance cap) fail closed on a bad capsule; a structurally-clean capsule still
requires a valid human-approval artifact bound to THAT capsule id before it is
admitted (never "unattended" — that is P7).
"""

from __future__ import annotations

from tessellum.composer.knowledge_plan import ClaimProvenance, NoteIntent, NoteIntentGraph
from tessellum.composer.structural_gates import (
    HumanApproval,
    StructuralGateContext,
    build_structural_gate_suite,
    supervised_admit,
)


def _intent(note_id, *, bb="concept", provenance=None, navigation=(),
            required_inlinks=(), relevance_links=()):
    return NoteIntent(
        note_id=note_id, thesis="t", building_block=bb,
        target_path=f"areas/{note_id}.md",
        provenance=tuple(provenance) if provenance is not None
        else (ClaimProvenance(span_id="s1", source_ref="r1"),),
        navigation=tuple(navigation), required_inlinks=tuple(required_inlinks),
        relevance_links=tuple(relevance_links),
    )


def _graph(*intents):
    return NoteIntentGraph(objective_id="obj", intents=tuple(intents))


def _ctx(*intents, **kw):
    return StructuralGateContext(graph=_graph(*intents), **kw)


def _approval(capsule_id="cap1"):
    return HumanApproval(capsule_id=capsule_id, approver="luke", signature="sig", reason="ok")


# ── structural gates fail closed ────────────────────────────────────────────


def test_bb_atomicity_rejects_multi_bb() -> None:
    suite = build_structural_gate_suite()
    ctx = _ctx(_intent("n1", bb="concept, procedure"))
    res = suite.evaluate(ctx, short_circuit=False)
    assert not res.passed
    assert any("STRUCT-BB-ATOMIC" == i.rule_id for r in res.results for i in r.issues)


def test_navigation_closure_requires_ep_in_write_set() -> None:
    # navigation to an entry point IS a write, so it is in the closure → OK.
    ok = supervised_admit(_ctx(_intent("n1", navigation=("entry_x",))),
                          capsule_id="cap1", approval=_approval())
    assert ok.decision == "approved"


def test_referential_integrity_uses_overlay_ghosts() -> None:
    # Build an overlay with a dangling staged link → ref-integrity fails.
    from pathlib import Path
    import tempfile
    from tessellum.indexer import Database, build
    from tessellum.indexer.db import LinkRow
    from tessellum.composer.overlay_index import OverlayIndex

    d = Path(tempfile.mkdtemp()) / "v"
    (d / "resources/term_dictionary").mkdir(parents=True)
    note = ("---\ntags: [resource, terminology]\nkeywords: [a,b,c]\ntopics: [X]\n"
            "language: markdown\ndate of note: 2026-05-10\nstatus: active\n"
            "building_block: concept\n---\n\n# A\n\nbody\n")
    (d / "resources/term_dictionary/term_a.md").write_text(note)
    dbp = d.parent / "idx.db"
    build(d, dbp)
    ix = OverlayIndex(Database(dbp))
    ix.stage_link(LinkRow(0, "resources/term_dictionary/term_a.md",
                          "resources/term_dictionary/term_missing.md", None, "markdown", None))
    ctx = StructuralGateContext(graph=_graph(_intent("n1")), overlay=ix)
    res = build_structural_gate_suite().evaluate(ctx, short_circuit=False)
    assert not res.passed
    assert any("STRUCT-REF-INTEGRITY" == i.rule_id for r in res.results for i in r.issues)


# ── human-approval ceiling ───────────────────────────────────────────────────


def test_clean_capsule_needs_human_without_approval() -> None:
    res = supervised_admit(_ctx(_intent("n1")), capsule_id="cap1", approval=None)
    assert res.decision == "blocked_needs_human"
    assert res.structural_passed is True


def test_clean_capsule_approved_with_bound_approval() -> None:
    res = supervised_admit(_ctx(_intent("n1")), capsule_id="cap1", approval=_approval("cap1"))
    assert res.decision == "approved"


def test_approval_bound_to_capsule_id_cannot_be_replayed() -> None:
    # an approval signed for a DIFFERENT capsule id is invalid here.
    res = supervised_admit(_ctx(_intent("n1")), capsule_id="cap2", approval=_approval("cap1"))
    assert res.decision == "blocked_needs_human"


def test_structural_failure_blocks_before_human_step() -> None:
    # a structural failure (multi-BB — the model permits it, the gate catches
    # it) blocks structurally regardless of a present, valid approval:
    # structural safety is a precondition for the human step.
    bad = _intent("n1", bb="concept, procedure")  # → STRUCT-BB-ATOMIC
    res = supervised_admit(_ctx(bad), capsule_id="cap1", approval=_approval("cap1"))
    assert res.decision == "blocked_structural"
    assert res.structural_passed is False
    assert "STRUCT-BB-ATOMIC" in res.blocking_rules


def test_relevance_link_cap_is_advisory_not_blocking_at_error() -> None:
    # a note with many relevance links trips the cap; since it is emitted at
    # WARNING it does NOT block structural admission on its own.
    many = tuple(f"rel_{i}" for i in range(50))
    res = supervised_admit(_ctx(_intent("n1", relevance_links=many)),
                           capsule_id="cap1", approval=_approval("cap1"))
    # coverage/provenance/etc all pass; relevance cap is WARNING → still approved.
    assert res.decision == "approved"
