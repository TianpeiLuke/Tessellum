"""Deterministic per-note owned-section coverage — the phase-3 residue
(FZ 20k9c1a1a1b7c2k2a3a): completeness as a WRITTEN-NOTE property.

Pins the high-precision contract: a paraphrased section survives (heading
mention OR one signal is enough), a SKIPPED signal-rich section self-
announces, a prose-only section abstains (unverifiable) — and the wave
wiring: advisory by default (composite passes, WARNING carried), blocking
under strict, identity extension without a coverage map.
"""

from __future__ import annotations

from pathlib import Path

from tessellum.composer.gates import build_wave_gate
from tessellum.composer.note_coverage import (
    compute_note_coverage,
    extend_wave_gate_with_note_coverage,
    make_note_coverage_predicate,
    name_match,
    owned_sections_for,
    section_signals,
    split_sections,
)
from tessellum.format import Severity

_SOURCE = (
    "# Guide\n\nintro prose\n\n"
    "## Quick Start\n\nRun `tool --init-vault` then set `MEMORY_ROOT` and "
    "`agents.defaults.memory` in the config.\n\n"
    "## Concepts\n\nPlain prose about ideas, no code at all.\n\n"
    "### Deep Dive\n\nUse `--verbose-trace`, `TRACE_LEVEL`, `log.sink.path`.\n"
)


def test_split_sections_h1_to_h3() -> None:
    sections = split_sections(_SOURCE)
    assert set(sections) == {"guide", "quick start", "concepts", "deep dive"}
    assert "intro prose" in sections["guide"]
    assert "--init-vault" in sections["quick start"]


_FENCED = (
    "# Real Title\n\nprose\n\n"
    "## Setup\n\nRun this:\n\n```bash\n# Basic syntax\ntool add x\n# Real example\ntool add y\n```\n\ntail prose\n\n"
    "## Next\n\nmore\n"
)


def test_f12_in_fence_comments_are_not_headings() -> None:
    from tessellum.composer.note_coverage import extract_headings

    assert extract_headings(_FENCED) == ["Real Title", "Setup", "Next"]


def test_f12_sections_keep_their_code_blocks_whole() -> None:
    sections = split_sections(_FENCED)
    assert set(sections) == {"real title", "setup", "next"}
    # the fence-blind splitter truncated "Setup" at `# Basic syntax`
    assert "tool add y" in sections["setup"] and "tail prose" in sections["setup"]


def test_f12_ledger_headings_fence_aware() -> None:
    from tessellum.composer.digestion import compute_source_ledger

    ledger = compute_source_ledger([{"source_id": "p", "excerpt": _FENCED}])
    assert ledger[0]["headings"] == ["Real Title", "Setup", "Next"]
    assert ledger[0]["code_blocks"] == 1


def test_name_match_is_boundary_aware() -> None:
    assert name_match("a.md", "a.md")
    assert name_match("howto_a.md", "a.md")
    assert not name_match("10d1e1a8a1a40", "10d1e1a8a1a4")


def test_owned_sections_resolve_by_note_name() -> None:
    sections = split_sections(_SOURCE)
    cmap = [
        {"source_section": "Quick Start", "maps_to_note": "notes/start.md"},
        {"source_section": "Deep Dive", "maps_to_note": "notes/dive.md"},
        {"source_section": "Ghost Section", "maps_to_note": "notes/start.md"},
    ]
    owned = owned_sections_for("start.md", cmap, sections)
    assert set(owned) == {"quick start"}  # the ghost row is PLAN-006's, skipped


def test_section_signals_come_from_code_only() -> None:
    signals = section_signals(split_sections(_SOURCE)["quick start"])
    assert {"--init-vault", "MEMORY_ROOT", "agents.defaults.memory"} <= signals
    assert section_signals("Plain prose about ideas, no code at all.") == set()


def test_coverage_heading_mention_covers() -> None:
    owned = {"quick start": split_sections(_SOURCE)["quick start"]}
    covered, uncovered, unv = compute_note_coverage(
        "# Note\n\nThe Quick Start flow, paraphrased entirely.", owned
    )
    assert covered == ["quick start"] and not uncovered and not unv


def test_coverage_one_signal_covers() -> None:
    owned = {"quick start": split_sections(_SOURCE)["quick start"]}
    covered, uncovered, unv = compute_note_coverage(
        "# Note\n\nInitialize with `tool --init-vault`.", owned
    )
    assert covered == ["quick start"] and not uncovered


def test_coverage_skipped_signal_rich_section_flags() -> None:
    owned = {"quick start": split_sections(_SOURCE)["quick start"]}
    covered, uncovered, unv = compute_note_coverage(
        "# Note\n\nEntirely unrelated content.", owned
    )
    assert uncovered == ["quick start"] and not covered and not unv


def test_coverage_prose_only_section_abstains() -> None:
    owned = {"concepts": split_sections(_SOURCE)["concepts"]}
    covered, uncovered, unv = compute_note_coverage(
        "# Note\n\nEntirely unrelated content.", owned
    )
    assert unv == ["concepts"] and not uncovered  # cannot prove absence


def _write_note(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_predicate_advisory_warning_and_strict_error(tmp_path: Path) -> None:
    plan_doc = {
        "section_coverage_map": [
            {"source_section": "Quick Start", "maps_to_note": "start.md"}
        ]
    }
    note = _write_note(tmp_path, "start.md", "# Note\n\nUnrelated.")
    advisory = make_note_coverage_predicate(plan_doc, _SOURCE)
    issues = list(advisory([note]))
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING
    assert issues[0].rule_id == "WAVE-002" and "quick start" in issues[0].message
    strict = make_note_coverage_predicate(plan_doc, _SOURCE, strict=True)
    assert list(strict([note]))[0].severity is Severity.ERROR


def test_predicate_skips_unowned_and_unreadable(tmp_path: Path) -> None:
    plan_doc = {
        "section_coverage_map": [
            {"source_section": "Quick Start", "maps_to_note": "start.md"}
        ]
    }
    other = _write_note(tmp_path, "other.md", "# Other\n\nUnrelated.")
    pred = make_note_coverage_predicate(plan_doc, _SOURCE)
    assert list(pred([other, tmp_path / "missing.md"])) == []


def test_wave_gate_extension_advisory_passes_with_findings(tmp_path: Path) -> None:
    plan_doc = {
        "section_coverage_map": [
            {"source_section": "Quick Start", "maps_to_note": "start.md"}
        ]
    }
    note = _write_note(tmp_path, "start.md", "# Note\n\nUnrelated.")
    suite = extend_wave_gate_with_note_coverage(build_wave_gate(), plan_doc, _SOURCE)
    assert [g.gate_id for g in suite.gates] == ["dedup", "note_coverage", "link_resolution"]
    composite = suite.evaluate([str(note)], short_circuit=False)
    assert composite.passed  # advisory: WARNING never blocks
    cov = next(r for r in composite.results if r.gate_id == "note_coverage")
    assert cov.passed and len(cov.issues) == 1  # ...but the finding is carried


def test_wave_gate_extension_without_map_adds_only_link_sweep() -> None:
    """W4 changed the no-map identity: the link_resolution sweep is added
    UNCONDITIONALLY (it needs only written paths); note_coverage still
    requires the map + source."""
    base = build_wave_gate()
    for suite in (
        extend_wave_gate_with_note_coverage(base, {}, _SOURCE),
        extend_wave_gate_with_note_coverage(base, {"section_coverage_map": []}, _SOURCE),
        extend_wave_gate_with_note_coverage(base, {"section_coverage_map": [{"source_section": "X"}]}, ""),
    ):
        assert [g.gate_id for g in suite.gates] == ["dedup", "link_resolution"]


def test_link_resolution_sweep_flags_unresolved_after_wave(tmp_path: Path) -> None:
    from tessellum.composer.gates import link_resolution_predicate

    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nsee [B](b.md) and [ghost](missing.md)\n", encoding="utf-8")
    b.write_text("# B\n\nback to [A](a.md)\n", encoding="utf-8")
    issues = list(link_resolution_predicate([a, b]))
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING and "missing.md" in issues[0].message
