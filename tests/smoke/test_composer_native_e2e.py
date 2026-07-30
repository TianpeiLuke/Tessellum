"""P11 (FZ 20k9c1a1a1b7c2f/g) — NATIVE end-to-end: run the REAL vault skills.

Every other digestion-driver test writes SYNTHETIC one-step skills into tmp and
drives them with a MockBackend hand-tuned to satisfy each stub's schema — so any
defect at the skill↔compiler↔materializer↔gate↔backend contract boundary (where
E2/E6/E9/E10/E11/E12/E13/E16/E18 all lived) is invisible BY CONSTRUCTION. E11's
single-leaf bug was even actively MASKED by a hand-built harness.

This test closes that gap: it compiles and runs the FOUR SHIPPED
``skill_tessellum_*_digestion*`` skills through ``run_digestion_pipeline`` with a
backend whose default JSON satisfies the UNION of every real step's required
output fields. It is offline (no live model) yet exercises the real compiled
prompts, real materializers, real gates, and real key-flow — the coverage the
synthetic suite structurally cannot provide.

It asserts the FRAMEWORK is sound (the phases compile + run + thread + gate
cleanly), NOT that the golden-quality bar is met (that needs a real model).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tessellum.composer import MockBackend, run_digestion_pipeline

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "vault" / "resources" / "skills"


def _real_skills_present() -> bool:
    return all(
        (SKILLS / f"skill_tessellum_{p}.md").is_file()
        for p in ("plan_digestion", "augment_digestion_plan",
                  "review_digestion_plan", "execute_digestion_plan")
    )


# The UNION of every real step's required output fields (see each skill's
# expected_output_schema). A single default response carrying all of them
# satisfies whichever step is running — so the real skills flow end to end.
_SUPERSET_RESPONSE = {
    # plan.identify_source
    "source_type": "documentation", "pages": [], "total_words": 5000,
    "estimated_note_count": 3, "plan_shape": "single_plan_phased",
    # plan.route (note_format_definition is a nested object)
    "target_directory": "resources/documentation/demo", "file_prefix": "demo_",
    "note_format_definition": {
        "derived_from": "resources/documentation/demo/demo_existing.md",
        "yaml_field_order": ["tags", "keywords", "topics", "language",
                             "date of note", "status", "building_block"],
        "h2_conventions": ["Overview", "Related Notes"],
        "forbidden_fields": ["title", "note_second_category"],
    },
    # plan.decompose (planned_notes rows need approx_words; coverage rows need source_section)
    "planned_notes": [
        {"filename": "demo_a", "building_block": "concept", "approx_words": 800, "description": "A"},
        {"filename": "demo_b", "building_block": "concept", "approx_words": 800, "description": "B"},
    ],
    "section_coverage_map": [{"source_section": "Overview", "maps_to_note": "demo_a"}],
    # cross_references: plan.cross_references rows need note_filename+term_notes;
    # augment.add_crossref_contract rows need note+term_links. One shared row
    # carries all four (extra keys are permitted — no additionalProperties:false).
    "per_note_related_notes": [
        {"note_filename": "demo_a", "note": "demo_a",
         "term_notes": [], "term_links": [], "other_related_notes": []},
    ],
    "entry_point_action": {"action": "update", "entry_point": "entry_demo.md"},
    "undigested_terms": [], "validation_gates": ["G1", "G2"],
    # plan/augment.write_plan / write_augmented_plan (body_markdown materializer)
    "output_path": "plans/plan_digest_demo.md",
    "body_markdown": "# Plan\n\n## Objective\n\nbody\n## Scope\n## Content Strategy\n## Source Pages\n## Planned Notes\n## Section Coverage Map\n## Split Decisions\n## Summary Statistics & Building Block Distribution\n## Per-Note Related Notes Mapping\n## Density Re-Assessment\n## Undigested Terms Plan\n## Per-Phase Validation Gate\n## Entry Point Decision\n## Inlinks\n## Review Sign-Off\n",
    # augment.read_draft
    "plan_path": "plans/plan_digest_demo.md", "plan_structure": "single",
    "sections_present": ["Objective"], "sections_missing": [],
    # augment.reread_source
    "pages_measured": [], "splits_needed": [], "new_undigested_terms": [],
    # augment.add_coverage_and_gates (tree is a string; gate_tables an array)
    "section_coverage_tree": "Overview → demo_a", "per_phase_gate_tables": [],
    # augment.add_crossref_contract (undigested_terms_plan + entry_point_decision are objects)
    "undigested_terms_plan": {"terms": [], "all_rows_have_capture_phase": True},
    "entry_point_decision": {"action": "UPDATE", "matches_size_threshold": True,
                             "target_entry_point": "entry_demo.md"},
    # review.step_1_read_plan
    "status": "pending", "total_notes": 2, "plan_text": "# Plan\n\n## Objective\n\nbody\n## Scope\n## Content Strategy\n## Source Pages\n## Planned Notes\n## Section Coverage Map\n## Split Decisions\n## Summary Statistics & Building Block Distribution\n## Per-Note Related Notes Mapping\n## Density Re-Assessment\n## Undigested Terms Plan\n## Per-Phase Validation Gate\n## Entry Point Decision\n## Inlinks\n## Review Sign-Off\n",
    # review.step_2 / step_3 checkpoints — each is an object {result, gap}
    "cp1": {"result": "PASS", "gap": None}, "cp2": {"result": "PASS", "gap": None},
    "cp3": {"result": "PASS", "gap": None}, "cp4": {"result": "PASS", "gap": None},
    "cp5": {"result": "PASS", "gap": None}, "cp6": {"result": "PASS", "gap": None},
    "cp7": {"result": "PASS", "gap": None}, "cp8": {"result": "PASS", "gap": None},
    # review.step_4_report_verdict
    "ready": True, "failures": [],
    # execute.preflight
    "planned_note_count": 2,
    # execute.boot_and_amend
    "pages_spot_checked": [], "amendments": [], "boot_report_written": True,
    # execute.extract_contracts
    "shared_contract_path": "plans/contract.md", "batches": [],
    # execute.verify
    "notes_created": 2, "format_errors": 0, "broken_links": 0,
    "ghost_references": 0, "graph_island_notes": 0, "outbound_reference_gaps": 0,
    "overall_ok": True,
}


# PLAN-008 (FZ 20k9c1a1a1b7c3) code-measures the source from the members' inline
# text (compute_source_ledger), so the excerpt must carry enough real words that
# the fixture's 2-note plan is NOT over-split: 2 notes needs a measured total
# above ceil-boundary 2*1143 ≈ 2,286 words. A 3-word placeholder would trip
# PLAN-008 (2 notes for a 3-word source) and false-fail this contract test.
_DEMO_EXCERPT = ("Some source content. " * 1300)  # ~2,600 measured words → 2 notes coherent

_SOURCE_LEAF = {
    "id": "demo",
    "source_url": "https://example.com/docs",
    "source_name": "Demo Docs",
    "members": [{"source_id": "p1", "excerpt": _DEMO_EXCERPT,
                 "source_url": "https://example.com/docs/p1"}],
    "member_count": 1,
    # keys the gate/normalize read
    "plan_path": "plans/plan_digest_demo.md",
    "plan_text": "# Plan\n\n## Objective\n\nbody\n## Scope\n## Content Strategy\n## Source Pages\n## Planned Notes\n## Section Coverage Map\n## Split Decisions\n## Summary Statistics & Building Block Distribution\n## Per-Note Related Notes Mapping\n## Density Re-Assessment\n## Undigested Terms Plan\n## Per-Phase Validation Gate\n## Entry Point Decision\n## Inlinks\n## Review Sign-Off\n",
    "total_notes": 2,
}


def test_real_skills_compile_and_run_plan_through_review(tmp_path: Path) -> None:
    """The four SHIPPED skills compile and run plan→augment→review end to end on
    the real prompts + materializers + gates (stop_after='review', offline).
    Catches skill↔compiler↔gate contract breakage the synthetic suite can't."""
    if not _real_skills_present():
        pytest.skip("real vault skills not present")
    backend = MockBackend(default=json.dumps(_SUPERSET_RESPONSE))
    result = run_digestion_pipeline(
        skills_dir=SKILLS,
        source_leaf=dict(_SOURCE_LEAF),
        backend=backend,
        vault_root=tmp_path / "vault",
        stop_after="review",
    )
    # The framework ran all three linear phases with NO framework error (each
    # real skill compiled, its prompt dispatched, its output materialized + merged).
    ran = [p.phase for p in result.phases if p.ran]
    assert ran == ["plan", "augment", "review"], f"phases ran: {ran}"
    assert all(p.error_count == 0 for p in result.phases), (
        "a real skill failed to compile/run/materialize: "
        + "; ".join(f"{p.phase}={p.error_count}" for p in result.phases)
    )
    # With a ready verdict the sign-off accepts the real plan.
    assert result.stopped_at == "review_accepted"
    assert result.completed


def test_real_skills_fan_out_planned_notes_natively(tmp_path: Path) -> None:
    """E11 regression on the REAL execute skill: a 2-note plan_doc fed to the
    native execute wave fans out to 2 writer leaves (not 1 whole-plan leaf)."""
    if not _real_skills_present():
        pytest.skip("real vault skills not present")
    from tessellum.composer import run_execute_wave
    backend = MockBackend(default=json.dumps(_SUPERSET_RESPONSE))
    plan_doc = {
        "plan_path": "plans/plan_digest_demo.md",
        "plan_text": "# Plan", "total_notes": 2,
        "planned_notes": _SUPERSET_RESPONSE["planned_notes"],
        "note_dir": "resources/documentation/demo",
        "members": _SOURCE_LEAF["members"],
    }
    run = run_execute_wave(
        plan_doc, skills_dir=SKILLS, backend=backend, vault_root=tmp_path / "vault",
    )
    assert len(run.leaves) == 2, (
        f"native execute wave over the REAL execute skill fanned out to "
        f"{len(run.leaves)} leaf(es), expected 2 (E11 regression)"
    )


def test_real_execute_wave_preflight_fails_loud_on_under_production(tmp_path: Path) -> None:
    """P13 (FZ 20k9c1a1a1b7c2e) — over the REAL execute skill, a plan that
    DECLARES 2 notes but carries no planned_notes / note_intent_graph collapses
    to the single whole-plan leaf; the pre-flight now RAISES PreflightError
    before any backend call (closes the by-construction masking — pre-P13 this
    silently under-produced ~1 note)."""
    if not _real_skills_present():
        pytest.skip("real vault skills not present")
    from tessellum.composer import run_execute_wave
    from tessellum.composer.digestion import PreflightError

    backend = MockBackend(default=json.dumps(_SUPERSET_RESPONSE))
    plan_doc = {
        "plan_path": "plans/plan_digest_demo.md",
        "plan_text": "# Plan", "total_notes": 2,  # declares 2, enumerates none
        "note_dir": "resources/documentation/demo",
    }
    with pytest.raises(PreflightError) as exc:
        run_execute_wave(
            plan_doc, skills_dir=SKILLS, backend=backend, vault_root=tmp_path / "vault",
        )
    assert exc.value.result.declared == 2
    assert exc.value.result.leaf_count == 1


def test_real_review_skill_has_no_re_emission_after_migration() -> None:
    """P21-full A7: the migrated review skill reads the plan BY REFERENCE via
    {{artifact.plan_text}} and no longer re-declares plan_text as step_1's
    output, so the compiler's re-emission LINT is clean — and strict mode
    compiles without raising. This is the target the lint was built to flag;
    it documents that the migration actually removed the re-emission."""
    if not _real_skills_present():
        pytest.skip("real vault skills not present")
    from tessellum.composer import compile_skill

    compiled = compile_skill(SKILLS / "skill_tessellum_review_digestion_plan.md")
    assert compiled.re_emission_warnings == (), (
        "the migrated review skill should have zero re-emission warnings; got: "
        + "; ".join(compiled.re_emission_warnings)
    )
    # Strict mode must not raise on the migrated skill.
    compile_skill(
        SKILLS / "skill_tessellum_review_digestion_plan.md",
        strict_re_emission=True,
    )
