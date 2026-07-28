"""Deterministic evidence for the review loop (FZ 20k9c1a1a1b7c2k1a1b).

Pins the three point fixes from the API eval runs' findings:

- issue 11 — :func:`compute_source_ledger`: the ``pages[]`` ledger is
  CODE-computed from the members' inline text (one convention: whitespace
  words, fence pairs, H1–H3 headings) and survives every phase fold — an LLM
  re-emission of ``pages`` never becomes the record;
- issue 9 — :func:`compute_coverage_orphans` / :func:`compute_review_exhibits`
  (the computed exhibits the reviewer must cite) and the `_review_verdict`
  contradiction guard: a coverage-orphan claim is DROPPED when the computed
  set-difference is empty (the r3 fabrication class), preserved on
  ``contradicted_failures`` — while genuine failures and claims backed by a
  non-empty set-difference pass through untouched.
"""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import MockBackend, run_digestion_pipeline
from tessellum.composer.digestion import (
    _review_verdict,
    compute_coverage_orphans,
    compute_review_exhibits,
    compute_source_ledger,
)

from test_composer_episodic_hardening import _synthetic_pipeline


# ── issue 11: the code-computed ledger ───────────────────────────────────────


def test_ledger_computed_from_member_text() -> None:
    text = "# Title\n\nalpha beta gamma\n\n## Section One\n\n```py\nx = 1\n```\ndelta\n"
    ledger = compute_source_ledger(
        [{"source_id": "p1", "source_url": "https://x/p1", "excerpt": text}]
    )
    assert len(ledger) == 1
    row = ledger[0]
    assert row["source_id"] == "p1"
    assert row["measured_words"] == len(text.split())
    assert row["code_blocks"] == 1
    assert row["headings"] == ["Title", "Section One"]


def test_ledger_skips_unmeasurable_members() -> None:
    assert compute_source_ledger([{"source_url": "https://only-url"}, "junk"]) == []


def test_pipeline_ledger_survives_model_reemission(tmp_path: Path) -> None:
    """The model's fold may emit its own pages[] — the code ledger must be the
    one on the final plan_doc (measured-by-code, no-clobber both ways)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    text = "# Only Heading\n\n" + "word " * 50
    blob = {
        "plan_path": "plans/p.md", "plan_text": "# Plan\n\nbody",
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# N\n\nbody",
        "total_notes": 1,
        # the model tries to overwrite the ledger with an estimate:
        "pages": [{"source_id": "fake", "measured_words": 99999, "headings": ["Invented"]}],
        # the code ledger makes PLAN-006(b) live for this run (a real heading
        # now exists) — the coverage map must map it, which is itself proof
        # the deterministic gate consumes the CODE ledger, not the fake:
        "section_coverage_map": [{"source_section": "Only Heading", "maps_to_note": "notes/n.md"}],
    }
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={
            "id": "demo", "total_notes": 1, "member_count": 1,
            "members": [{"source_id": "p1", "excerpt": text}],
        },
        backend=MockBackend(default=json.dumps(blob)),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    pages = result.plan_doc["pages"]
    assert len(pages) == 1 and pages[0]["source_id"] == "p1"
    assert pages[0]["measured_words"] == len(text.split())
    assert pages[0]["headings"] == ["Only Heading"]


def test_no_members_no_ledger_override(tmp_path: Path) -> None:
    """Byte-identity: without measurable members the model's pages[] stands."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    blob = {
        "plan_path": "plans/p.md", "plan_text": "# Plan\n\nbody",
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# N\n\nbody",
        "total_notes": 1,
        "pages": [{"source_id": "model-page", "measured_words": 123, "headings": []}],
    }
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "demo", "total_notes": 1},
        backend=MockBackend(default=json.dumps(blob)),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    assert result.plan_doc["pages"][0]["source_id"] == "model-page"


# ── issue 9: orphans, exhibits, the contradiction guard ──────────────────────


def _doc(headings, mapped, failures):
    return {
        "pages": [{"source_id": "p", "measured_words": 10, "headings": headings}],
        "section_coverage_map": [
            {"source_section": m, "maps_to_note": "n.md"} for m in mapped
        ],
        "plan_text": "text with 10 in it",
        "verdict": {"ready": False, "failures": failures},
    }


def test_orphans_zero_when_fully_mapped() -> None:
    assert compute_coverage_orphans(_doc(["A", "B"], ["A", "B"], [])) == []


def test_orphans_found_when_unmapped() -> None:
    assert compute_coverage_orphans(_doc(["A", "B"], ["A"], [])) == ["B"]


def test_orphans_none_when_uncomputable() -> None:
    assert compute_coverage_orphans({"pages": "junk"}) is None
    assert compute_coverage_orphans({}) is None


def test_guard_drops_fabricated_orphan_claim() -> None:
    d = _doc(
        ["A", "B"], ["A", "B"],
        ["CP7 FAIL — coverage map is materially incomplete: 30 headings unmapped",
         "CP5 FAIL — format not derived"],
    )
    ready, failures = _review_verdict(d)
    assert not ready  # the genuine CP5 failure stands
    assert failures == ["CP5 FAIL — format not derived"]
    assert d["contradicted_failures"] == [
        "CP7 FAIL — coverage map is materially incomplete: 30 headings unmapped"
    ]


def test_guard_flips_ready_when_all_claims_fabricated() -> None:
    d = _doc(["A"], ["A"], ["CP7 FAIL — 5 headings absent from the coverage map"])
    ready, failures = _review_verdict(d)
    assert ready and failures == []


def test_guard_keeps_claim_when_orphans_real() -> None:
    d = _doc(["A", "B"], ["A"], ["CP7 FAIL — headings unmapped in the coverage map"])
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1
    assert "contradicted_failures" not in d


def test_guard_noop_when_uncomputable() -> None:
    d = {"verdict": {"ready": False, "failures": ["CP7 — orphaned headings"]}}
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1  # cannot verify → cannot drop


def test_exhibits_render_coverage_and_figures() -> None:
    ex = compute_review_exhibits(_doc(["A"], ["A"], []))
    assert "UNMAPPED=0" in ex and "measured_words=10" in ex and "PRESENT" in ex


def test_exhibits_empty_without_ledger() -> None:
    assert compute_review_exhibits({}) == ""
