"""R4.1–R4.3 (FZ 20k9c1a1a1b7c2k2a1d) — fabrication defense.

Assessment cross-checks (schema-valid fabrication becomes self-announcing),
verifier property tests against the judged party's rendering distribution
(the F3 class as a parametrized test, not a live incident), and the
two-sided canonical-form contract binding skill prose and matcher to one
constants owner.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer.contracts import (
    FIGURE_ABSORBED_RENDERINGS,
    FIGURE_CANONICAL_RENDERING,
)
from tessellum.composer.digestion import (
    _figure_present,
    _norm_heading,
    compute_assessment_violations,
    compute_review_exhibits,
)

REPO = Path(__file__).resolve().parents[2]
PLAN_SKILL = REPO / "vault" / "resources" / "skills" / "skill_tessellum_plan_digestion.md"


# ── R4.1: assessment cross-checks ────────────────────────────────────────────

_DOC = {
    "plan_text": "# Plan\n\n## Objective\n\nx\n\n## Coverage Map\n\ny\n",
    "sections_present": ["Objective", "Coverage Map"],
    "_pages_code_measured": True,
    "pages": [{"headings": ["Demo", "Overview"]}],
    "section_coverage_map": [
        {"source_section": "Demo", "maps_to_note": "a.md"},
        {"source_section": "Overview", "maps_to_note": "b.md"},
    ],
}


def test_consistent_assessments_produce_no_violations() -> None:
    assert compute_assessment_violations(dict(_DOC)) == []


def test_fabricated_section_claim_is_caught() -> None:
    """The F2-round-1 class: a claimed-present section that does not exist."""
    doc = dict(_DOC)
    doc["sections_present"] = ["Objective", "Totally Invented Section"]
    v = compute_assessment_violations(doc)
    assert v and "Totally Invented Section" in v[0]


def test_invented_coverage_heading_is_caught() -> None:
    doc = dict(_DOC)
    doc["section_coverage_map"] = _DOC["section_coverage_map"] + [
        {"source_section": "Ghost Chapter", "maps_to_note": "c.md"}
    ]
    v = compute_assessment_violations(doc)
    assert v and "Ghost Chapter" in v[0]


def test_master_claim_without_index_is_caught() -> None:
    doc = dict(_DOC)
    doc["plan_structure"] = "master"
    v = compute_assessment_violations(doc)
    assert v and "Sub-Plans Index" in v[0]


def test_assessments_exhibit_renders_in_review_exhibits() -> None:
    doc = dict(_DOC)
    doc["sections_present"] = ["Objective", "Totally Invented Section"]
    exhibits = compute_review_exhibits(doc)
    assert "ASSESSMENTS (computed)" in exhibits
    assert "Totally Invented Section" in exhibits


def test_no_plan_text_means_not_computable() -> None:
    assert compute_assessment_violations({}) is None


# ── R4.2: verifier property tests over the judged distribution ───────────────

@pytest.mark.parametrize("rendering,expected", [
    ("measured 12813 words", True),          # canonical
    ("measured 12,813 words", True),         # thousands commas (F3 live class)
    ("value 212813 differs", False),         # digit boundary (left)
    ("value 128,134 differs", False),        # digit boundary (right)
    ("range ~12,000-15,000 words", False),   # a range is NOT the figure
])
def test_figure_matcher_over_rendering_distribution(rendering: str, expected: bool) -> None:
    assert _figure_present(12813, rendering) is expected


@pytest.mark.parametrize("a,b,equal", [
    ("Getting  Started", "getting started", True),   # case + whitespace
    ("Setup\tGuide", "setup guide", True),           # tabs collapse
    ("Overview", "overview ", True),
    ("Overview", "Overviews", False),
])
def test_heading_normalizer_over_rendering_distribution(a: str, b: str, equal: bool) -> None:
    assert (_norm_heading(a) == _norm_heading(b)) is equal


# ── R4.3: the two-sided canonical-form contract, one owner ───────────────────

def test_canonical_figure_contract_binds_both_sides() -> None:
    """The generator side (plan-skill prose mandates the canonical form) and
    the matcher side (absorbs each declared human rendering) bound to the ONE
    contracts.py owner — either side drifting fails here."""
    assert FIGURE_CANONICAL_RENDERING == "BARE DIGITS"
    prose = PLAN_SKILL.read_text(encoding="utf-8")
    assert "BARE DIGITS" in prose  # generator pins the canonical form
    for rendering in FIGURE_ABSORBED_RENDERINGS:
        assert rendering == "thousands commas"
        assert _figure_present(12813, "12,813")  # matcher absorbs it
