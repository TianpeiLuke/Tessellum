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
from tessellum.composer.contracts import mandatory_section_stems
from tessellum.composer.digestion import (
    _review_verdict,
    compute_coverage_orphans,
    compute_review_exhibits,
    compute_source_ledger,
)

from test_composer_episodic_hardening import _synthetic_pipeline

# PLAN-009 gates coverage-map-bearing plans on the mandatory sections —
# fixtures that assert completion must carry the stems.
_STEM_BLOB = "\n" + "\n".join(f"## {s}" for s in mandatory_section_stems())


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
        "plan_path": "plans/p.md", "plan_text": "# Plan\n\nbody" + _STEM_BLOB,
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
        "plan_path": "plans/p.md", "plan_text": "# Plan\n\nbody" + _STEM_BLOB,
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
        "_pages_code_measured": True,  # unit fixtures simulate the driver's ledger
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
    # E3.3 (2026-07-29): the fabricated CP7 claim is DROPPED (contradicted),
    # and the remaining CP5 critique is advisory-until-calibrated — surfaced
    # on advisory_failures, no longer blocking the loop. (Pre-E3.3 this pin
    # asserted `not ready` with the CP5 failure standing.)
    assert d["contradicted_failures"] == [
        "CP7 FAIL — coverage map is materially incomplete: 30 headings unmapped"
    ]
    assert ready and d["advisory_failures"] == ["CP5 FAIL — format not derived"]


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


# ── E1/E2/E3 (FZ 20k9c1a1a1b7c2k1a1b1) ──────────────────────────────────────


def test_exhibits_cover_sections_gates_inventory_density() -> None:
    pd = {
        "pages": [{"source_id": "p", "measured_words": 100, "headings": ["A"]}],
        "section_coverage_map": [{"source_section": "A", "maps_to_note": "n"}],
        "plan_text": "## Planned Notes\n| 1 | a.md |\n| 2 | b.md |\n\n## Scope\nhas 100. G1 G2 G3 G4 G5 G6 G7 G8",
        "planned_notes": [
            {"filename": "a.md", "approx_words": 1200},
            {"filename": "b.md", "approx_words": 1500},
        ],
        "total_notes": 2,
    }
    ex = compute_review_exhibits(pd)
    assert "SECTIONS (computed): 2/14" in ex and "BELOW the >=90% threshold" in ex
    assert "GATES (computed): 8/8" in ex
    assert "INVENTORY (computed): planned_notes list=2, total_notes=2, Planned-Notes table rows=2 (consistent)" in ex
    assert "DENSITY (computed): approx_words min=1200 median=1500 max=1500" in ex


def test_inventory_exhibit_flags_mismatch() -> None:
    pd = {
        "pages": [{"source_id": "p", "measured_words": 1, "headings": ["A"]}],
        "section_coverage_map": [{"source_section": "A", "maps_to_note": "n"}],
        "plan_text": "## Planned Notes\n| 1 | a.md |\n",
        "planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}],
        "total_notes": 9,
    }
    assert "MISMATCH" in compute_review_exhibits(pd)


def test_mandatory_sections_single_source_matches_every_golden() -> None:
    """E1.3 binding: the runtime constant and each golden slice's list agree —
    the criteria cannot fork (the R1/R2 + 7-vs-8-gates drift class)."""
    import json as _json

    from tessellum.composer.contracts import MANDATORY_PLAN_SECTIONS

    eval_root = Path(__file__).resolve().parents[2] / "eval" / "digestion_pipeline"
    checked = 0
    for facts_path in sorted(eval_root.glob("*/golden_facts.json")):
        gp = _json.loads(facts_path.read_text())["golden_plan"]
        sections = gp.get("mandatory_plan_sections")
        if sections is None:
            continue
        assert tuple(sections) == MANDATORY_PLAN_SECTIONS, facts_path
        checked += 1
    assert checked >= 1


def test_guard_drops_ledger_figure_claim_when_figures_present() -> None:
    d = _doc(["A"], ["A"], ["CP7 FAIL — word counts are outside tolerance vs measured"])
    d["plan_text"] = "Source table says 10 words"
    ready, failures = _review_verdict(d)
    assert ready and failures == []
    assert d["contradicted_failures"]


def test_guard_keeps_figure_claim_when_figures_absent() -> None:
    d = _doc(["A"], ["A"], ["CP7 FAIL — word counts are outside tolerance vs measured"])
    d["plan_text"] = "no numbers here"
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1


def test_guard_keeps_per_note_density_critique() -> None:
    """Review F3: a per-note/statistics figure critique is NOT ledger-scoped
    and must never be dropped by page-figure presence."""
    d = _doc(["A"], ["A"],
             ["CP6 FAIL — note 7's declared word count does not match its mapped sections: approx_words=1750 vs ~600 source words"])
    d["plan_text"] = "Source table says 10 words"
    ready, failures = _review_verdict(d)
    # F3's point holds: the critique is never DROPPED — post-E3.3 it survives
    # as an advisory (CP6 = qualitative), not a loop block.
    assert "contradicted_failures" not in d
    assert ready and "1750" in d["advisory_failures"][0]


def test_guard_requires_code_provenance() -> None:
    """Review F4: model-emitted pages can never ground a drop — without the
    driver's provenance flag no domain fires."""
    d = _doc(["A"], ["A"], ["CP7 FAIL — 5 headings absent from the coverage map"])
    del d["_pages_code_measured"]
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1


def test_figure_presence_is_digit_boundary_matched() -> None:
    """Review F7: measured 10 must not 'match' inside 2100."""
    d = _doc(["A"], ["A"], ["CP7 FAIL — word counts are outside tolerance vs measured"])
    d["plan_text"] = "the value 2100 appears but never the real figure"
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1


def test_stale_drops_cleared_on_clean_round() -> None:
    """Review F8: a prior round's contradicted_failures must not survive a
    round that dropped nothing."""
    d = _doc(["A"], ["A"], ["CP5 FAIL — genuine qualitative critique"])
    d["contradicted_failures"] = ["old claim from a prior round"]
    ready, failures = _review_verdict(d)
    # F8's point holds: the stale drop is cleared; the CP5 critique itself is
    # advisory post-E3.3 (surfaced, non-blocking).
    assert ready and d["advisory_failures"]
    assert "contradicted_failures" not in d


def test_section_claims_are_never_code_dropped() -> None:
    """Review F1/F2: prose-substring presence is NOT deterministic evidence of
    a section's existence, and a 'missing' claim can be a true coverage/content
    defect — the section domain was REMOVED; such claims always stand."""
    d = _doc(["A"], ["A"], ["CP8 FAIL — the Undigested Terms Plan section is entirely absent"])
    d["plan_text"] = "10 ...\n## Undigested Terms Plan\ncontent"
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1


def test_true_coverage_claim_never_dropped_via_section_wording() -> None:
    """Review F1 (the CRITICAL): a claim phrased as 'missing' about a REAL
    orphan must never be dropped — orphans exist, orphan_safe is False."""
    d = _doc(["Intro", "Advanced Topics"], ["Intro"],
             ["CP7 FAIL — the Section Coverage Map is missing the Advanced Topics heading"])
    ready, failures = _review_verdict(d)
    assert not ready and len(failures) == 1
    assert "contradicted_failures" not in d


def test_result_surfaces_contradicted_failures(tmp_path: Path) -> None:
    """E3.2: a fabricated claim dropped by the guard reaches the caller as
    DigestionResult.contradicted_failures — and the run COMPLETES (the r3
    class terminates round 1 as ready instead of burning the budget)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    text = "# Only Heading\n\n" + "word " * 50
    blob = {
        "plan_path": "plans/p.md", "plan_text": "# Plan\n\n" + str(len(text.split())) + _STEM_BLOB,
        "ready": False,
        "failures": ["CP7 FAIL — 30 headings unmapped in the coverage map"],
        "output_path": "notes/n.md", "body_markdown": "# N\n\nbody",
        "total_notes": 1,
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
    assert result.contradicted_failures
    assert "unmapped" in result.contradicted_failures[0]
    assert result.plan_doc.get("_pages_code_measured") is True


def test_pages_is_an_artifact_key_and_pages_durably(tmp_path: Path) -> None:
    """E2.1: the ledger is a first-class artifact — durable mode pages it as
    an ArtifactRef whose deref matches the in-RAM rendering byte-for-byte."""
    from tessellum.composer.contracts import _ARTIFACT_KEYS, ArtifactRef
    from tessellum.composer.digestion import _build_artifact_store
    from tessellum.composer.executor import _resolve_placeholders

    assert "pages" in _ARTIFACT_KEYS
    doc = {"pages": [{"source_id": "p", "measured_words": 7, "headings": ["A"]}]}
    ram = _build_artifact_store(doc)
    durable = _build_artifact_store(doc, tmp_path / "arts")
    assert isinstance(durable["pages"], ArtifactRef)
    t = "L: {{artifact.pages}}"
    assert _resolve_placeholders(t, leaf={}, upstream={}, artifacts=ram) == \
           _resolve_placeholders(t, leaf={}, upstream={}, artifacts=durable)


def test_ledger_synthesized_from_source_content(tmp_path: Path) -> None:
    """Review F4 deep fix: the runtime/CLI single-doc shape (top-level
    source_content, empty members) still gets a CODE-measured ledger."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    text = "# Solo Heading\n\n" + "tok " * 40
    blob = {
        "plan_path": "plans/p.md", "plan_text": "# Plan\n\n" + str(len(text.split())) + _STEM_BLOB,
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# N\n\nbody",
        "total_notes": 1,
        "section_coverage_map": [{"source_section": "Solo Heading", "maps_to_note": "notes/n.md"}],
    }
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "demo", "total_notes": 1, "source_content": text,
                     "source_name": "solo-doc"},
        backend=MockBackend(default=json.dumps(blob)),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    pages = result.plan_doc["pages"]
    assert pages[0]["source_id"] == "solo-doc"
    assert pages[0]["measured_words"] == len(text.split())
    assert result.plan_doc.get("_pages_code_measured") is True


# ── issues 13/14/15 (FZ 20k9c1a1a1b7c2k1a1b1a) ──────────────────────────────


class _FlakyEmptyBackend:
    """Returns empty content N times, then a valid payload — the r5 blip."""

    backend_id = "flaky-empty"

    def __init__(self, empties: int, payload: str) -> None:
        self.empties = empties
        self.payload = payload
        self.calls = 0

    def call(self, request):
        from tessellum.composer.llm import LLMResponse

        self.calls += 1
        content = "" if self.calls <= self.empties else self.payload
        return LLMResponse(
            content=content, elapsed_ms=1.0, backend_id=self.backend_id,
            metadata={"stop_reason": "end_turn", "output_tokens": len(content)},
        )


def _one_step_skill(tmp_path: Path) -> Path:
    from test_composer_episodic_hardening import _write_phase_skill

    sd = tmp_path / "skills"
    sd.mkdir(exist_ok=True)
    _write_phase_skill(sd, "skill_solo", output_key="out", required=["ok"])
    return sd / "skill_solo.md"


def test_empty_response_rides_the_blip(tmp_path: Path) -> None:
    """Issue 13: empties are diagnosed first-class (stop_reason attached),
    EXEMPT from the same-error short-circuit, retried with forced backoff —
    and the step SUCCEEDS once the blip clears (r5 would have completed)."""
    from tessellum.composer import compile_skill
    from tessellum.composer.executor import execute_step_with_retry

    compiled = compile_skill(_one_step_skill(tmp_path))
    backend = _FlakyEmptyBackend(empties=3, payload=json.dumps({"ok": True}))
    sleeps: list[float] = []
    attempts: list[dict] = []
    result = execute_step_with_retry(
        compiled.steps[0], leaf={"_id": "corpus"}, upstream={},
        backend=backend, vault_root=tmp_path / "v", dry_run=True,
        sleep_fn=sleeps.append, attempt_recorder=attempts.append,
    )
    assert result.error is None
    assert backend.calls == 4  # 3 empties ridden + 1 success
    assert len(sleeps) == 3 and all(s > 0 for s in sleeps)  # forced backoff
    kinds = [a["kind"] for a in attempts]
    assert kinds == ["empty", "empty", "empty", "success"]
    # Issue 14: the journal captured stop_reason for every attempt
    assert all(a["stop_reason"] == "end_turn" for a in attempts)


def test_empty_budget_exhaustion_is_terminal_and_clear(tmp_path: Path) -> None:
    from tessellum.composer import compile_skill
    from tessellum.composer.executor import execute_step_with_retry

    compiled = compile_skill(_one_step_skill(tmp_path))
    backend = _FlakyEmptyBackend(empties=99, payload="{}")
    result = execute_step_with_retry(
        compiled.steps[0], leaf={"_id": "corpus"}, upstream={},
        backend=backend, vault_root=tmp_path / "v", dry_run=True,
        sleep_fn=lambda s: None,
    )
    assert result.error and "empty response" in result.error
    assert "stop_reason=end_turn" in result.error  # self-explanatory


def test_attempts_journal_written_via_pipeline(tmp_path: Path) -> None:
    """Issue 14 e2e: a runs_dir pipeline run writes attempts.jsonl."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    runs = tmp_path / "runs"
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "demo", "total_notes": 1, "member_count": 1,
                     "members": [{"source_id": "m", "excerpt": "# H\nw"}],
                     "section_coverage_map": [{"source_section": "H", "maps_to_note": "n.md"}]},
        backend=MockBackend(default=json.dumps({
            "plan_path": "p.md", "plan_text": "# P\n1" + _STEM_BLOB,
            "ready": True, "failures": [],
            "output_path": "n.md", "body_markdown": "# N\nb", "total_notes": 1,
            "section_coverage_map": [{"source_section": "H", "maps_to_note": "n.md"}],
        })),
        vault_root=tmp_path / "vault",
        runs_dir=runs,
    )
    assert result.completed
    lines = (runs / "attempts.jsonl").read_text().splitlines()
    assert lines and all(json.loads(x)["kind"] for x in lines)


def test_note_count_band_computed_from_ledger(tmp_path: Path) -> None:
    """Issue 15: the driver injects the computed band the gates enforce."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    text = "# H\n\n" + "word " * 3600  # 3602 words -> band 3..4
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "demo", "total_notes": 1, "member_count": 1,
                     "members": [{"source_id": "m", "excerpt": text}]},
        backend=MockBackend(default=json.dumps({
            "plan_path": "p.md", "plan_text": "# P\n3602",
            "ready": True, "failures": [],
            "output_path": "n.md", "body_markdown": "# N\nb", "total_notes": 1,
            "section_coverage_map": [{"source_section": "H", "maps_to_note": "n.md"}],
        })),
        vault_root=tmp_path / "vault",
    )
    band = result.plan_doc.get("note_count_band", "")
    assert band.startswith("3..4 notes")
    assert "3602 words" in band


def test_code_source_excerpt_survives_fold_clobber(monkeypatch, tmp_path):
    """A3.1 guard: a phase EMITTING `source_excerpt` must not replace the
    code-joined source — same re-assertion the code ledger gets. Pinned at the
    unit level: the ensure helper never overwrites, and the fold-guard pattern
    re-asserts the captured value."""
    from tessellum.composer.digestion import _ensure_source_excerpt

    plan_doc = {"members": [{"source_id": "p1", "excerpt": "TRUE SOURCE"}]}
    _ensure_source_excerpt(plan_doc)
    code_copy = plan_doc["source_excerpt"]
    assert "TRUE SOURCE" in code_copy

    # an LLM fold clobbers the key…
    plan_doc["source_excerpt"] = "lossy re-emission"
    # …ensure never overwrites non-empty (it must NOT "fix" it silently)…
    _ensure_source_excerpt(plan_doc)
    assert plan_doc["source_excerpt"] == "lossy re-emission"
    # …the pipeline's fold guard restores the captured code copy verbatim
    plan_doc["source_excerpt"] = code_copy
    assert "TRUE SOURCE" in plan_doc["source_excerpt"]


def test_figure_match_absorbs_thousands_separators():
    """J3 finding 3: the exhibit/guard must find 12813 written as '12,813' —
    run 3's revise loop exhausted on the comma. Boundaries still hold."""
    from tessellum.composer.digestion import _figure_present, _figures_all_present

    assert _figure_present(12813, "measured total: 12,813 words")
    assert _figure_present(12813, "measured total: 12813 words")
    assert not _figure_present(12813, "value 212813 is different")   # boundary
    assert not _figure_present(12813, "value 128,134 is different")  # trailing digit
    doc = {
        "pages": [{"measured_words": 12813}],
        "plan_text": "Summary: the source measures 12,813 words in total.",
    }
    assert _figures_all_present(doc)


def test_anthropic_client_bounded_timeouts_and_no_sdk_retries(monkeypatch):
    """J3 finding 5: the client must carry explicit httpx timeouts (a silent
    stalled stream raises within the read gap instead of wedging the wave
    forever) and max_retries=0 (the ladder owns retry semantics)."""
    import sys
    import types

    captured = {}

    fake = types.ModuleType("anthropic")

    def _ctor(**kwargs):
        captured.update(kwargs)
        return object()

    fake.Anthropic = _ctor
    monkeypatch.setitem(sys.modules, "anthropic", fake)

    from tessellum.composer.llm import AnthropicBackend

    AnthropicBackend(model="claude-sonnet-4-6", api_key="k")
    assert captured["max_retries"] == 0
    t = captured["timeout"]
    assert t.read == 300.0 and t.connect == 30.0


def test_advisory_only_failures_flip_ready_for_the_loop():
    """E3.3 (decided 2026-07-29): CP5/CP6 are qualitative and uncalibrated —
    a verdict whose ONLY failures are advisory flips ready, with the failures
    preserved on advisory_failures (surfaced at sign-off, never silenced)."""
    from tessellum.composer.digestion import _review_verdict

    doc = {"ready": False, "failures": [
        "CP5 FAIL - derivation faithfulness doubtful on note 3",
        "CP6 FAIL - borderline atomicity: consider splitting note 2",
    ]}
    ready, failures = _review_verdict(doc)
    assert ready is True and failures == []
    assert len(doc["advisory_failures"]) == 2


def test_mixed_failures_still_block_and_clear_stale_advisory():
    from tessellum.composer.digestion import _review_verdict

    doc = {"ready": False, "advisory_failures": ["stale"], "failures": [
        "CP5 FAIL - qualitative doubt",
        "CP7 FAIL - 3 measured headings unmapped",
    ]}
    ready, failures = _review_verdict(doc)
    assert ready is False and len(failures) == 2
    assert "advisory_failures" not in doc  # stale entry cleared


def test_gating_checkpoints_unaffected_by_demotion():
    from tessellum.composer.digestion import _review_verdict

    doc = {"ready": False, "failures": ["CP2 FAIL - gate table missing G7"]}
    ready, failures = _review_verdict(doc)
    assert ready is False and failures


def test_gate_failure_reenters_the_revise_loop_despite_reviewer_ready(tmp_path, monkeypatch):
    """F8 (the openclaw sweep): the reviewer approved a plan whose own
    COVERAGE exhibit named 4 computed orphans; the deterministic sign-off gate
    then rejected terminally with revise rounds UNUSED. Now: reviewer-ready +
    gate-fail + rounds-remaining converts the gate's blocking issues into the
    next round's revise conditioning — deterministic authority in BOTH
    directions."""
    from tessellum.composer.digestion import _review_verdict
    from tessellum.composer.gates import build_plan_gate

    # a plan the reviewer calls ready but whose coverage map omits a measured
    # heading (the PLAN-006 class that killed the openclaw run)
    doc = {
        "ready": True, "failures": [],
        "_pages_code_measured": True,
        "plan_path": "plans/plan_digest_demo.md",
        "plan_text": "# Plan\n\n## Objective\n## Scope\n## Content Strategy\n## Source Pages\n## Planned Notes\n## Section Coverage Map\n## Split Decisions\n## Summary Statistics & Building Block Distribution\n## Per-Note Related Notes Mapping\n## Density Re-Assessment\n## Undigested Terms Plan\n## Per-Phase Validation Gate\n## Entry Point Decision\n## Inlinks\n## Review Sign-Off",
        "total_notes": 1,
        "planned_notes": [{"filename": "a.md", "building_block": "concept",
                           "approx_words": 900}],
        "pages": [{"measured_words": 1200,
                   "headings": ["Mapped Section", "Omitted Section"]}],
        "section_coverage_map": [
            {"source_section": "Mapped Section", "maps_to_note": "a.md"},
        ],
    }
    ready, _ = _review_verdict(doc)
    assert ready is True                       # the reviewer's (wrong) verdict
    composite = build_plan_gate().evaluate(doc)
    assert not composite.passed                # the deterministic authority
    assert any("Omitted Section" in str(i) for i in composite.blocking_issues)
