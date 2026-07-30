"""F13 (FZ 20k9c1a1a1b7c2k2a3a — sweep run 9): deterministic mandatory
sections are code-generated projections, and PLAN-009 reports per stem.

Run 9 burned all three revise rounds failing to author the four sections
whose content is plan_doc data, through F8 conditioning that named them.
Pins the cure at both layers: `_reconcile_generated_sections` fills the
derivable sections from the of-record data (authored sections win), and
`plan_sections_predicate` emits ONE issue per missing stem so the revise
loop's count-based convergence metric sees within-gate progress."""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import MockBackend, run_digestion_pipeline
from tessellum.composer.contracts import mandatory_section_stems
from tessellum.composer.digestion import _reconcile_generated_sections
from tessellum.composer.gates import plan_sections_predicate

from test_composer_episodic_hardening import _synthetic_pipeline

_DERIVABLE = (
    "Source Pages",
    "Summary Statistics & Building Block Distribution",
    "Per-Phase Validation Gate",
    "Review Sign-Off",
)
# the ten judgment sections a writer authors (run 9 reliably emitted these)
_AUTHORED = "\n".join(
    f"## {s}" for s in mandatory_section_stems() if s not in _DERIVABLE
)


def _doc(plan_text: str) -> dict:
    return {
        "plan_text": plan_text,
        "section_coverage_map": [
            {"source_section": "Only Heading", "maps_to_note": "notes/n.md"}
        ],
        "pages": [
            {"source_id": "p1", "measured_words": 51, "code_blocks": 2,
             "headings": ["Only Heading"]}
        ],
        "planned_notes": [
            {"filename": "a.md", "building_block": "concept"},
            {"filename": "b.md", "building_block": "procedure"},
            {"filename": "c.md", "building_block": "concept"},
        ],
    }


def test_plan_sections_one_issue_per_missing_stem() -> None:
    issues = plan_sections_predicate(_doc("# Plan\n\n" + _AUTHORED))
    assert len(issues) == len(_DERIVABLE)
    named = {s for s in _DERIVABLE for i in issues if s in i.message}
    assert named == set(_DERIVABLE)


def test_plan_sections_out_of_scope_without_map() -> None:
    d = _doc("# Plan\n\n" + _AUTHORED)
    d.pop("section_coverage_map")
    assert plan_sections_predicate(d) == []


def test_reconcile_fills_derivable_sections_from_of_record_data() -> None:
    d = _doc("# Plan\n\n" + _AUTHORED)
    _reconcile_generated_sections(d)
    text = d["plan_text"]
    for s in _DERIVABLE:
        assert f"## {s}" in text
    assert "| p1 | 51 | 2 | 1 |" in text  # Source Pages = the ledger
    assert "Total planned notes: 3" in text and "- concept: 2" in text
    assert plan_sections_predicate(d) == []  # the gate now passes


def test_f15_pure_data_sections_regenerated_always() -> None:
    """F15 (run 11): the writer AUTHORED a Summary Statistics section with
    invented tallies ('Digest notes planned: 26' vs the of-record 9) and
    generate-if-missing let it stand. Pure-data sections are now REPLACED
    with the projection, heading normalized to the canonical stem."""
    authored = (
        "# Plan\n\n## Source Pages\n\nMY OWN TABLE\n\n"
        "## Summary Statistics\n\n| Digest notes planned | 26 |\n\n" + _AUTHORED
    )
    d = _doc(authored)
    _reconcile_generated_sections(d)
    text = d["plan_text"]
    assert "MY OWN TABLE" not in text and "26" not in text
    assert text.count("## Source Pages") == 1
    assert "| p1 | 51 | 2 | 1 |" in text
    # the variant heading is normalized to the full canonical stem
    assert "## Summary Statistics & Building Block Distribution" in text
    assert "Total planned notes: 3" in text


def test_f15_boilerplate_sections_still_authored_wins() -> None:
    authored = (
        "# Plan\n\n## Per-Phase Validation Gate\n\nMY GATE TABLE\n\n" + _AUTHORED
    )
    d = _doc(authored)
    _reconcile_generated_sections(d)
    assert "MY GATE TABLE" in d["plan_text"]
    assert d["plan_text"].count("## Per-Phase Validation Gate") == 1


def test_reconcile_noop_out_of_scope() -> None:
    d = _doc("# Plan\n\n" + _AUTHORED)
    d.pop("section_coverage_map")
    before = d["plan_text"]
    _reconcile_generated_sections(d)
    assert d["plan_text"] == before


def test_pipeline_completes_when_writer_omits_derivable_sections(tmp_path: Path) -> None:
    """Run 9's exact failure shape, cured: the mock writer authors only the
    ten judgment sections; the fold generates the four derivable ones, so
    PLAN-009 passes and the run completes instead of rejecting."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    text = "# Only Heading\n\n" + "word " * 50
    blob = {
        "plan_path": "plans/p.md",
        "plan_text": "# Plan\n\n" + _AUTHORED,
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# N\n\nbody",
        "total_notes": 1,
        "planned_notes": [
            {"filename": "n.md", "building_block": "concept", "approx_words": 300}
        ],
        "section_coverage_map": [
            {"source_section": "Only Heading", "maps_to_note": "notes/n.md"}
        ],
    }
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "demo", "total_notes": 1, "member_count": 1,
                     "members": [{"source_id": "p1", "excerpt": text}]},
        backend=MockBackend(default=json.dumps(blob)),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    for s in _DERIVABLE:
        assert f"## {s}" in result.plan_doc["plan_text"]
