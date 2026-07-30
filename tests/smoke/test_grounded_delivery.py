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


# ── k2a4a: link constraint, sibling healing, code budget ────────────────────


def test_leaves_carry_siblings_and_budget():
    d = _doc()
    leaves = _project_planned_notes_to_leaves(d)
    by = {lf["note"]["filename"]: lf for lf in leaves}
    assert "- beta.md" in by["alpha.md"]["planned_siblings_md"]
    assert "alpha.md" not in by["alpha.md"]["planned_siblings_md"]
    # alpha owns Alpha+Gamma (0 fences) -> budget 0; beta owns Beta (0 fences)
    assert by["alpha.md"]["code_block_budget"] == 0


def test_code_block_budget_caps_and_counts():
    from tessellum.composer.digestion import _code_block_budget

    d = _doc()
    d["source_excerpt"] = (
        "# Alpha\n\n" + "```py\nx\n```\n\n" * 9 + "\n# Beta\n\nno code\n"
    )
    assert _code_block_budget("alpha.md", d) == 6   # capped at the rubric ceiling
    assert _code_block_budget("beta.md", d) == 0    # no padding
    d.pop("section_coverage_map")
    assert _code_block_budget("alpha.md", d) == 6   # no slice -> the cap


def test_heal_sibling_links_kebab_to_snake_unique():
    from tessellum.composer.materializer import _heal_sibling_links

    siblings = "- openclaw_memory_system.md\n- openclaw_workspace.md"
    text = (
        "see [memory](../x/openclaw-memory-system.md) and "
        "[ghost](../x/openclaw-model-selection.md) and "
        "[ok](openclaw_workspace.md)"
    )
    healed = _heal_sibling_links(text, siblings)
    assert "../x/openclaw_memory_system.md" in healed        # unique normalized match
    assert "openclaw-model-selection.md" in healed           # unmatched: left for the sweep
    assert "(openclaw_workspace.md)" in healed               # verbatim: untouched


def test_code_density_close_gate_advisory(tmp_path):
    from tessellum.composer.gates import build_close_gate, code_density_predicate
    from tessellum.composer.gates import GroundingVerdict
    from tessellum.format import Severity

    note = tmp_path / "n.md"
    note.write_text("# N\n\n" + "```\nx\n```\n\n" * 8, encoding="utf-8")
    issues = list(code_density_predicate(note))
    assert issues and issues[0].severity is Severity.WARNING and "8 fenced" in issues[0].message
    suite = build_close_gate()
    comp = suite.evaluate(note, verdict=GroundingVerdict("grounded"), short_circuit=False)
    dens = next(r for r in comp.results if r.gate_id == "code_density")
    assert dens.passed and dens.issues  # advisory: carried, never blocks
