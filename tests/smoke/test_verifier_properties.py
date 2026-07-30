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


# ── F9: the materializer absorbs fenced-frontmatter renderings ───────────────

def test_materializer_absorbs_fenced_yaml_frontmatter(tmp_path: Path) -> None:
    """F9 (the openclaw sweep): every wave writer emitted ```yaml-fenced
    frontmatter and the retries did not converge — the fenced form is
    meaning-identical rendering variance the CODE side absorbs (R4.3 at the
    document level)."""
    from tessellum.composer.materializer import materialize

    fenced = (
        "```yaml\n"
        "output_path: platforms/openclaw/demo.md\n"
        "tags: [resource, concept]\n"
        "```\n\n# Demo\n\nBody text.\n"
    )
    materialize(
        "body_markdown_frontmatter_to_file", fenced,
        vault_root=tmp_path, dry_run=False,
    )
    written = tmp_path / "platforms/openclaw/demo.md"
    assert written.is_file()
    content = written.read_text(encoding="utf-8")
    assert content.startswith("---\n")           # canonical form on disk
    assert "# Demo" in content


def test_materializer_still_fails_loud_on_truly_missing_frontmatter(tmp_path: Path) -> None:
    import pytest as _pytest

    from tessellum.composer.materializer import MaterializerError, materialize

    with _pytest.raises(MaterializerError, match="missing YAML frontmatter"):
        materialize(
            "body_markdown_frontmatter_to_file", "# Just a body, no frontmatter\n",
            vault_root=tmp_path, dry_run=False,
        )


def test_materializer_normalizes_kebab_tags_to_the_vault_alphabet(tmp_path: Path) -> None:
    """F10 (the openclaw sweep): kebab tags from kebab-heavy sources blocked
    7/9 leaves at the close gate (YAML-015) — the same tag in a different
    rendering, absorbed deterministically at write time."""
    from tessellum.composer.materializer import materialize

    doc = (
        "---\n"
        "output_path: platforms/openclaw/demo2.md\n"
        "tags: [resource, concept, active-memory, AI Agents]\n"
        "---\n\n# D\n\nBody.\n"
    )
    materialize(
        "body_markdown_frontmatter_to_file", doc,
        vault_root=tmp_path, dry_run=False,
    )
    content = (tmp_path / "platforms/openclaw/demo2.md").read_text(encoding="utf-8")
    assert "active_memory" in content and "active-memory" not in content
    assert "ai_agents" in content


def test_planned_notes_table_reconciles_from_the_structured_list() -> None:
    """F11: the prose table is a code-generated projection of planned_notes —
    a drifted 5-row table collapses to the structured list's 2 rows after any
    fold, surrounding prose preserved; the INVENTORY exhibit reads consistent."""
    from tessellum.composer.digestion import (
        _reconcile_planned_notes_table,
        compute_review_exhibits,
    )

    doc = {
        "planned_notes": [
            {"filename": "a.md", "building_block": "concept",
             "approx_words": 900, "description": "A"},
            {"filename": "b.md", "building_block": "procedure",
             "approx_words": 800, "description": "B | pipes"},
        ],
        "total_notes": 2,
        "plan_text": (
            "# Plan\n\nIntro prose.\n\n## Planned Notes\n\nLead-in sentence.\n\n"
            "| # | Note |\n|---|---|\n| 1 | x.md |\n| 2 | y.md |\n| 3 | z.md |\n"
            "| 4 | w.md |\n| 5 | v.md |\n\nTrailing prose.\n\n## Next Section\n\nz\n"
        ),
    }
    _reconcile_planned_notes_table(doc)
    pt = doc["plan_text"]
    assert pt.count("| a.md |") == 1 and pt.count("| b.md |") == 1
    assert "x.md" not in pt and "v.md" not in pt        # drifted rows gone
    assert "Lead-in sentence." in pt and "Trailing prose." in pt
    assert "## Next Section" in pt
    assert "B / pipes" in pt                             # cell-safe description
    exhibits = compute_review_exhibits(doc)
    assert "INVENTORY" not in exhibits or "MISMATCH" not in exhibits


def test_reconcile_noop_without_section_or_list() -> None:
    from tessellum.composer.digestion import _reconcile_planned_notes_table

    doc = {"planned_notes": [], "plan_text": "# P\n\n## Planned Notes\n\n| 1 |\n"}
    _reconcile_planned_notes_table(doc)
    assert "| 1 |" in doc["plan_text"]  # empty list → untouched
    doc2 = {"planned_notes": [{"filename": "a.md"}], "plan_text": "# P\nno section\n"}
    _reconcile_planned_notes_table(doc2)
    assert doc2["plan_text"] == "# P\nno section\n"


def test_approved_plan_file_tracks_the_reconciled_plan_doc(tmp_path: Path) -> None:
    """Phase-1 instrument fix (FZ b7c2k2a3a): after approval the on-disk plan
    file is refreshed to the of-record plan_text (F11's reconciled inventory
    included) — the seam that made openclaw's T1 score stale prose."""
    from tessellum.composer.digestion import _rematerialize_plan_file

    plan_file = tmp_path / "plans" / "plan_digest_demo.md"
    plan_file.parent.mkdir(parents=True)
    plan_file.write_text("# STALE pre-fold text", encoding="utf-8")
    recorded = []
    doc = {"plan_path": "plans/plan_digest_demo.md",
           "plan_text": "# RECONCILED of-record text"}
    _rematerialize_plan_file(doc, tmp_path, None, recorded.append)
    assert plan_file.read_text(encoding="utf-8") == "# RECONCILED of-record text"
    assert recorded == [plan_file.resolve()]

    # identical content → no rewrite, no effect recorded
    recorded.clear()
    _rematerialize_plan_file(doc, tmp_path, None, recorded.append)
    assert recorded == []

    # escape attempts and absent files are no-ops
    _rematerialize_plan_file(
        {"plan_path": "../outside.md", "plan_text": "x"}, tmp_path, None, None
    )
    assert not (tmp_path.parent / "outside.md").exists()
