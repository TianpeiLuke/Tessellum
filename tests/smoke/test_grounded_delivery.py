"""W1 (FZ 20k9c1a1a1b7c2k2a4): scoped source delivery — the writer's needle.

Pins: the leaf projection stamps each note's VERBATIM owned slice via the
canonical fence-aware join (empty fallback when unresolvable); PLAN-010
flags over-allocated notes as WARNING (never blocking); the BALANCE
exhibit renders for the reviewer."""

from __future__ import annotations

from tessellum.composer.digestion import (
    _owned_source_slice,
    _project_planned_notes_to_leaves,
    compute_review_exhibits,
)
from tessellum.composer.gates import build_plan_gate, plan_balance_predicate
from tessellum.format import Severity

_SOURCE = (
    "# Alpha\n\n" + "alpha words here " * 20 +
    "\n\n# Beta\n\nrun `--beta-flag` now\n\n# Gamma\n\n" + "gamma text " * 10
)


def _doc():
    return {
        "plan_text": "# Plan\n\n## Planned Notes\n",
        "total_notes": 2,
        "source_excerpt": _SOURCE,
        "planned_notes": [
            {"filename": "alpha.md", "building_block": "concept", "approx_words": 300},
            {"filename": "beta.md", "building_block": "concept", "approx_words": 300},
        ],
        "section_coverage_map": [
            {"source_section": "Alpha", "maps_to_note": "alpha.md"},
            {"source_section": "Gamma", "maps_to_note": "alpha.md"},
            {"source_section": "Beta", "maps_to_note": "beta.md"},
        ],
    }


def test_owned_source_slice_is_verbatim_and_scoped():
    d = _doc()
    alpha = _owned_source_slice("alpha.md", d)
    beta = _owned_source_slice("beta.md", d)
    assert "alpha words here" in alpha and "gamma text" in alpha
    assert "--beta-flag" not in alpha
    assert "--beta-flag" in beta and "alpha words" not in beta


def test_owned_source_slice_empty_fallbacks():
    d = _doc()
    assert _owned_source_slice("unknown.md", d) == ""
    d2 = _doc()
    d2.pop("section_coverage_map")
    assert _owned_source_slice("alpha.md", d2) == ""


def test_leaves_carry_the_slice():
    leaves = _project_planned_notes_to_leaves(_doc())
    by_name = {lf["note"]["filename"]: lf for lf in leaves}
    assert "--beta-flag" in by_name["beta.md"]["owned_source_slice"]
    assert "--beta-flag" not in by_name["alpha.md"]["owned_source_slice"]


def test_plan_balance_warns_only_over_allocated():
    d = _doc()
    # inflate Alpha's owned span far past 2x the 1800-word ceiling
    d["source_excerpt"] = "# Alpha\n\n" + "w " * 4000 + "\n\n# Beta\n\nsmall\n"
    issues = plan_balance_predicate(d)
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING and "alpha.md" in issues[0].message
    composite = build_plan_gate().evaluate(d, short_circuit=False)
    balance = next(r for r in composite.results if r.gate_id == "plan_balance")
    assert balance.passed and balance.issues  # advisory: carried, never blocks


def test_balance_exhibit_renders():
    d = _doc()
    d["pages"] = [{"source_id": "p", "measured_words": 10, "headings": ["Alpha"]}]
    d["_pages_code_measured"] = True
    ex = compute_review_exhibits(d)
    assert "BALANCE (computed):" in ex
