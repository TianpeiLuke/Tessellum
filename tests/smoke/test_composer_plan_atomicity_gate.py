"""FZ 20k9d4 — plan-time atomicity enforcement.

The three note-split rules (density ≥1800w, one-BB, full source coverage) are
now HARD, OBJECTIVE gates that fail-closed and force a re-plan (the planner may
split OR rearrange the coverage map — the gate does not prescribe the fix).
A subjective "is this really atomic?" read is NOT gated here.

Covers: NoteIntent's single-BB validator + approx_words field (A1), and the
plan_atomicity_predicate PLAN-004/005/006 triggers over both plan_doc shapes —
the typed note_intent_graph and the skill's planned_notes + section_coverage_map
(A2), plus the clean-plan pass and the composed build_plan_gate suite.
"""

from __future__ import annotations

import pytest

from tessellum.composer.gates import (
    PLAN_NOTE_MAX_WORDS,
    build_plan_gate,
    plan_atomicity_predicate,
)
from tessellum.composer.knowledge_plan import ClaimProvenance, NoteIntent


def _prov():
    return (ClaimProvenance(span_id="s1", source_ref="src#1"),)


# ── A1: NoteIntent model ─────────────────────────────────────────────────────


def test_note_intent_accepts_canonical_bb_and_approx_words() -> None:
    n = NoteIntent(
        note_id="n1", thesis="t", building_block="concept",
        approx_words=900, target_path="resources/n1.md", provenance=_prov(),
    )
    assert n.building_block == "concept"
    assert n.approx_words == 900


def test_note_intent_defaults_approx_words_zero() -> None:
    n = NoteIntent(note_id="n1", thesis="t", building_block="model",
                   target_path="areas/n1.md", provenance=_prov())
    assert n.approx_words == 0


def test_note_intent_model_stays_permissive_on_bb() -> None:
    # DESIGN: the model does NOT reject a multi-BB value — it stays permissive
    # so single-BB is enforced by the GATES (STRUCT-BB-ATOMIC + PLAN-005),
    # surfacing as a re-plannable failure rather than a construction error.
    n = NoteIntent(note_id="n1", thesis="t", building_block="concept, procedure",
                   target_path="resources/n1.md", provenance=_prov())
    assert n.building_block == "concept, procedure"  # accepted; the gate rejects it


def test_note_intent_rejects_negative_words() -> None:
    with pytest.raises(ValueError):
        NoteIntent(note_id="n1", thesis="t", building_block="concept",
                   approx_words=-1, target_path="resources/n1.md",
                   provenance=_prov())


# ── A2: plan_atomicity_predicate over the skill's planned_notes shape ────────


def _plan(planned=None, coverage=None, **extra):
    doc = {"plan_path": "plans/p.md", "plan_text": "x", "total_notes": 1}
    if planned is not None:
        doc["planned_notes"] = planned
    if coverage is not None:
        doc["section_coverage_map"] = coverage
    doc.update(extra)
    return doc


def test_clean_plan_passes() -> None:
    doc = _plan(
        planned=[
            {"filename": "a.md", "building_block": "concept", "approx_words": 800},
            {"filename": "b.md", "building_block": "procedure", "approx_words": 1200},
        ],
        coverage=[
            {"source_section": "Intro", "maps_to_note": "a.md"},
            {"source_section": "Steps", "maps_to_note": "b.md"},
        ],
    )
    assert plan_atomicity_predicate(doc) == []


# ── review-fix regressions ───────────────────────────────────────────────────


def test_plan004_coerces_numeric_string_words() -> None:
    # Review-fix (CONFIRMED): raw LLM JSON may deliver approx_words as "2000".
    doc = _plan(planned=[
        {"filename": "s.md", "building_block": "concept", "approx_words": "2000"},
    ])
    assert any(i.rule_id == "PLAN-004" for i in plan_atomicity_predicate(doc))


def test_plan004_coerces_float_words() -> None:
    doc = _plan(planned=[
        {"filename": "f.md", "building_block": "concept", "approx_words": 1900.0},
    ])
    assert any(i.rule_id == "PLAN-004" for i in plan_atomicity_predicate(doc))


def test_plan007_all_zero_words_is_unverifiable() -> None:
    # Review-fix (CONFIRMED): notes enumerated but no positive approx_words →
    # density unverifiable → fail-closed (IDENT-5), not a silent pass.
    doc = _plan(planned=[
        {"filename": "a.md", "building_block": "concept"},          # no words
        {"filename": "b.md", "building_block": "procedure", "approx_words": 0},
    ])
    assert any(i.rule_id == "PLAN-007" for i in plan_atomicity_predicate(doc))


def test_plan007_not_fired_when_any_words_declared() -> None:
    doc = _plan(planned=[
        {"filename": "a.md", "building_block": "concept", "approx_words": 500},
        {"filename": "b.md", "building_block": "procedure"},  # this one unknown, ok
    ])
    assert not any(i.rule_id == "PLAN-007" for i in plan_atomicity_predicate(doc))


def test_plan007_exempts_typed_graph_no_words() -> None:
    # A programmatically-compiled typed note_intent_graph (e.g. DKS) legitimately
    # carries no word estimates — PLAN-007 must NOT fire for it (density is the
    # LLM-planning concern, checked on the planned_notes shape only).
    graph = {"objective_id": "o", "intents": [
        {"note_id": "n1", "building_block": "concept"},          # no approx_words
        {"note_id": "n2", "building_block": "procedure"},
    ]}
    doc = {"plan_path": "p", "plan_text": "x", "total_notes": 2,
           "note_intent_graph": graph}
    assert not any(i.rule_id == "PLAN-007" for i in plan_atomicity_predicate(doc))


def test_plan006_omitted_section_caught_via_headings_inventory() -> None:
    # Review-fix (CONFIRMED, HIGH): a source section DROPPED from the coverage
    # map entirely (not just an empty target) is caught by set-difference
    # against the authoritative pages[].headings inventory.
    doc = _plan(
        planned=[{"filename": "a.md", "building_block": "concept", "approx_words": 500}],
        coverage=[{"source_section": "Intro", "maps_to_note": "a.md"}],  # Security dropped
        pages=[{"headings": ["Intro", "Security"]}],
    )
    issues = plan_atomicity_predicate(doc)
    p006 = [i for i in issues if i.rule_id == "PLAN-006"]
    assert any("Security" in i.message for i in p006), \
        f"omitted section not caught: {[i.message for i in issues]}"


def test_plan006_all_headings_covered_passes() -> None:
    doc = _plan(
        planned=[{"filename": "a.md", "building_block": "concept", "approx_words": 500}],
        coverage=[
            {"source_section": "Intro", "maps_to_note": "a.md"},
            {"source_section": "Security", "maps_to_note": "a.md"},
        ],
        pages=[{"headings": ["Intro", "Security"]}],
    )
    assert not any(i.rule_id == "PLAN-006" for i in plan_atomicity_predicate(doc))


def test_plan006_fails_closed_on_stringified_coverage_map() -> None:
    # Review-fix (CONFIRMED, HIGH): the augment phase re-emits section_coverage_map
    # as an ASCII-tree STRING, which used to clobber the list and silently pass.
    # A non-list coverage map with notes enumerated must now fail-closed.
    doc = _plan(
        planned=[{"filename": "a.md", "building_block": "concept", "approx_words": 500}],
    )
    doc["section_coverage_map"] = "Intro -> a.md\nSecurity -> SKIP"  # ASCII tree
    issues = plan_atomicity_predicate(doc)
    assert any(i.rule_id == "PLAN-006" for i in issues), \
        "stringified coverage map must fail closed, not silently pass"


def test_plan004_density_over_ceiling_fails() -> None:
    doc = _plan(planned=[
        {"filename": "big.md", "building_block": "concept",
         "approx_words": PLAN_NOTE_MAX_WORDS + 1},
    ])
    issues = plan_atomicity_predicate(doc)
    assert any(i.rule_id == "PLAN-004" for i in issues)


def test_plan004_exactly_at_ceiling_fails() -> None:
    # >= is the trigger: exactly 1800 is not density-atomic.
    doc = _plan(planned=[
        {"filename": "big.md", "building_block": "concept",
         "approx_words": PLAN_NOTE_MAX_WORDS},
    ])
    assert any(i.rule_id == "PLAN-004" for i in plan_atomicity_predicate(doc))


def test_plan004_under_ceiling_ok() -> None:
    doc = _plan(planned=[
        {"filename": "ok.md", "building_block": "concept",
         "approx_words": PLAN_NOTE_MAX_WORDS - 1},
    ])
    assert not any(i.rule_id == "PLAN-004" for i in plan_atomicity_predicate(doc))


def test_plan005_mixed_bb_string_fails() -> None:
    doc = _plan(planned=[
        {"filename": "m.md", "building_block": "concept, procedure",
         "approx_words": 500},
    ])
    assert any(i.rule_id == "PLAN-005" for i in plan_atomicity_predicate(doc))


def test_plan006_uncovered_section_fails() -> None:
    doc = _plan(
        planned=[{"filename": "a.md", "building_block": "concept", "approx_words": 500}],
        coverage=[
            {"source_section": "Intro", "maps_to_note": "a.md"},
            {"source_section": "Orphaned", "maps_to_note": ""},      # unmapped
            {"source_section": "AlsoOrphan", "maps_to_note": "TBD"},  # marker
        ],
    )
    issues = plan_atomicity_predicate(doc)
    p006 = [i for i in issues if i.rule_id == "PLAN-006"]
    assert len(p006) == 2
    assert any("Orphaned" in i.message for i in p006)


# ── A2: over the typed note_intent_graph shape (authoritative) ───────────────


def test_predicate_reads_typed_graph() -> None:
    graph = {
        "objective_id": "obj",
        "intents": [
            {"note_id": "n1", "building_block": "concept", "approx_words": 2500},
        ],
    }
    doc = {"plan_path": "p", "plan_text": "x", "total_notes": 1,
           "note_intent_graph": graph}
    issues = plan_atomicity_predicate(doc)
    assert any(i.rule_id == "PLAN-004" and "n1" in i.message for i in issues)


def test_typed_graph_takes_priority_over_planned_notes() -> None:
    # When both are present the typed graph is authoritative.
    graph = {"objective_id": "o", "intents": [
        {"note_id": "g1", "building_block": "concept", "approx_words": 3000}]}
    doc = {"plan_path": "p", "plan_text": "x", "total_notes": 1,
           "note_intent_graph": graph,
           "planned_notes": [{"filename": "p1.md", "building_block": "concept",
                              "approx_words": 100}]}
    issues = plan_atomicity_predicate(doc)
    assert any("g1" in i.message for i in issues)
    assert not any("p1" in i.message for i in issues)


# ── boundary / fail-soft ─────────────────────────────────────────────────────


def test_no_notes_no_atomicity_issues() -> None:
    # A plan enumerating no notes has no atomicity signal — structure gate owns
    # the shapeless/empty-plan fail-closed case, not this predicate.
    assert plan_atomicity_predicate({"plan_path": "p", "plan_text": "x",
                                     "total_notes": 0}) == []


def test_non_dict_returns_empty() -> None:
    assert plan_atomicity_predicate(None) == []


def test_missing_approx_words_not_flagged() -> None:
    # A note without approx_words (unknown) is not density-flagged — the gate
    # triggers on a KNOWN number >= ceiling, not on absence.
    doc = _plan(planned=[{"filename": "a.md", "building_block": "concept"}])
    assert not any(i.rule_id == "PLAN-004" for i in plan_atomicity_predicate(doc))


# ── composed suite ───────────────────────────────────────────────────────────


def test_build_plan_gate_includes_atomicity() -> None:
    suite = build_plan_gate()
    ids = {g.gate_id for g in suite.gates}
    assert "plan_structure" in ids and "plan_atomicity" in ids


def test_suite_fails_on_over_dense_note() -> None:
    doc = _plan(planned=[
        {"filename": "big.md", "building_block": "concept", "approx_words": 5000},
    ])
    result = build_plan_gate().evaluate(doc, short_circuit=False)
    assert not result.passed


def test_suite_passes_clean_plan() -> None:
    doc = _plan(
        planned=[{"filename": "a.md", "building_block": "concept", "approx_words": 700}],
        coverage=[{"source_section": "Intro", "maps_to_note": "a.md"}],
    )
    assert build_plan_gate().evaluate(doc).passed


# ── integration: the plan→augment flat-merge must NOT clobber the gate ───────


def test_augment_phase_does_not_clobber_coverage_gate(tmp_path) -> None:
    # Review-fix (HIGH): drive the REAL plan-Step-3 + augment-Step-3 outputs
    # through the actual no_op materializer + the flat last-writer-wins merge
    # (_collect_structured semantics), with a plan that OMITS a source section,
    # and assert PLAN-006 still fires. Before the fix, augment re-emitted
    # section_coverage_map as a string and clobbered the list → gate silently
    # passed. The rename to section_coverage_tree keeps the list authoritative.
    import json

    from tessellum.composer.materializer import materialize

    plan_step3 = json.dumps({
        "planned_notes": [
            {"filename": "a.md", "building_block": "concept", "approx_words": 700},
        ],
        "section_coverage_map": [
            {"source_section": "Intro", "maps_to_note": "a.md"},
            # "Security" heading exists in the source but is NOT mapped → omitted
        ],
    })
    augment_step3 = json.dumps({
        # the augment ASCII tree — now under section_coverage_tree, NOT _map
        "section_coverage_tree": "Intro -> a.md\nSecurity -> SKIP",
        "per_phase_gate_tables": "…",
    })

    # simulate the linear plan→augment flat merge (_collect_structured: dict.update)
    plan_doc = {"plan_path": "plans/p.md", "plan_text": "x", "total_notes": 1,
                "pages": [{"headings": ["Intro", "Security"]}]}
    for blob in (plan_step3, augment_step3):
        out = materialize("no_op", blob, vault_root=tmp_path)
        plan_doc.update(out.structured)

    # the plan's machine-readable list must have SURVIVED the augment merge
    assert isinstance(plan_doc["section_coverage_map"], list), \
        "augment must not clobber the coverage list"
    result = build_plan_gate().evaluate(plan_doc, short_circuit=False)
    assert not result.passed  # PLAN-006 fires on the omitted 'Security' section
    issues = plan_atomicity_predicate(plan_doc)
    assert any(i.rule_id == "PLAN-006" and "Security" in i.message for i in issues)
