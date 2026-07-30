"""Phase-3 residue (FZ 20k9c1a1a1b7c2k2a3a): deterministic per-note
owned-section coverage — completeness as a WRITTEN-NOTE property.

The rescore verdict's confirmed writer gap: notes under-cover the source
sections they OWN per the plan's coverage map (openclaw completeness ~2.5
against its own owned slices). Planning-side gates (PLAN-006/009) prove the
MAP is sound; nothing verified the written note against its slice. This
module is that check, as a wave-scope sweep predicate: for each written
note, resolve its owned sections (coverage map ⨝ the heading-split source —
the same join the scoped Tier-3 judge uses, canonicalized here) and require
each section to leave a deterministic trace in the note.

High precision over recall, like identifier grounding: a section is flagged
UNCOVERED only when its normalized heading is absent from the note AND it
carries ≥3 code-like signals (from its inline/fenced code) none of which
appear — a paraphrased section survives, a SKIPPED section self-announces.
A section with fewer signals and no heading match is UNVERIFIABLE and never
flagged. Landed ADVISORY (WARNING) per the report-first cost-control rule;
``strict=True`` is the calibrated promotion path.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from tessellum.composer.note_grounding import _IDENTIFIER_RES
from tessellum.format import Issue, Severity

_HEADING_LINE_RE = re.compile(r"^#{1,3} +(.+?)\s*$")
_FENCE_RE = re.compile(r"(?ms)^```[^\n]*\n(.*?)^```\s*$")
_CODE_SPAN_RE = re.compile(r"`([^`\n]{2,200})`")

# A section must offer at least this many code-like signals before a zero-hit
# note flags it — below the floor the check abstains (unverifiable), so pure
# prose sections can never false-positive.
MIN_SIGNALS_TO_FLAG = 3


def norm_heading(s: str) -> str:
    """The one heading normalization (shared with the scoped judge)."""
    return " ".join(s.lower().split())


def name_match(a: str, b: str) -> bool:
    """Boundary-aware note-name match (the FZ-renumbering lesson): equal, or
    the longer ends with the shorter at a separator boundary."""
    if a == b:
        return True
    if len(a) > len(b) and a.endswith(b):
        return a[-len(b) - 1] in ("_", "-", "/", ".")
    return False


def extract_headings(source_text: str) -> list[str]:
    """H1–H3 heading titles in document order, FENCE-AWARE (F12): a line
    inside a ``` fenced block is code (a shell comment, not structure) and
    can never be a heading. On the mcp corpus the fence-blind regex counted
    21 in-fence ``# comment`` lines among 67 "headings"."""
    out: list[str] = []
    in_fence = False
    for line in source_text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = _HEADING_LINE_RE.match(line)
        if m:
            out.append(m.group(1))
    return out


def split_sections(source_text: str) -> dict[str, str]:
    """Normalized H1–H3 heading → its section text (heading line up to the
    next heading of ANY level — the code ledger's heading family).

    FENCE-AWARE (F12): an in-fence ``# comment`` line neither opens a
    section nor truncates the one it sits in, so a section carries its code
    blocks whole. First occurrence wins on duplicate headings."""
    out: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    in_fence = False

    def flush() -> None:
        if current is not None:
            out.setdefault(current, "\n".join(buf))

    for line in source_text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            buf.append(line)
            continue
        m = None if in_fence else _HEADING_LINE_RE.match(line)
        if m:
            flush()
            current = norm_heading(m.group(1))
            buf = [line]
        else:
            buf.append(line)
    flush()
    return out


def owned_sections_for(
    note_name: str, coverage_map: Sequence, sections: dict[str, str]
) -> dict[str, str]:
    """The note's owned slice: coverage rows whose target name-matches the
    note, resolved against the heading-split source. Rows naming a section
    absent from the source are PLAN-006's territory, skipped here."""
    base = note_name.rsplit("/", 1)[-1]
    owned: dict[str, str] = {}
    for row in coverage_map:
        if not isinstance(row, dict):
            continue
        target = str(row.get("maps_to_note") or row.get("note") or "").strip()
        target = target.rsplit("/", 1)[-1]
        if not target or not (name_match(base, target) or name_match(target, base)):
            continue
        key = norm_heading(str(row.get("source_section") or ""))
        sec = sections.get(key)
        if sec:
            owned[key] = sec
    return owned


def section_signals(section_text: str) -> set[str]:
    """Code-like tokens from the section's inline spans and fenced blocks —
    the deterministic trace a covering note is expected to carry at least one
    of. Prose is never mined (precision over recall)."""
    code = "\n".join(_CODE_SPAN_RE.findall(section_text))
    code += "\n" + "\n".join(_FENCE_RE.findall(section_text))
    out: set[str] = set()
    for pattern in _IDENTIFIER_RES:
        out.update(pattern.findall(code))
    return out


def compute_note_coverage(
    note_text: str, owned: dict[str, str]
) -> tuple[list[str], list[str], list[str]]:
    """Classify each owned section against the note: (covered, uncovered,
    unverifiable). Covered = heading mentioned OR ≥1 signal present;
    uncovered = neither, with ≥ MIN_SIGNALS_TO_FLAG signals to probe;
    unverifiable = neither, below the floor (the check abstains)."""
    covered: list[str] = []
    uncovered: list[str] = []
    unverifiable: list[str] = []
    note_norm = norm_heading(note_text)
    for heading, sec in owned.items():
        if heading in note_norm:
            covered.append(heading)
            continue
        signals = section_signals(sec)
        if any(sig in note_text for sig in signals):
            covered.append(heading)
        elif len(signals) >= MIN_SIGNALS_TO_FLAG:
            uncovered.append(heading)
        else:
            unverifiable.append(heading)
    return covered, uncovered, unverifiable


def owned_span_words(
    planned_notes: Sequence, coverage_map: Sequence, source_text: str
) -> dict[str, tuple[int, int]]:
    """W1.3 (FZ 20k9c1a1a1b7c2k2a4): per-note owned-span size — filename →
    (measured words, section count) over the note's owned slice. The
    note-count band constrains the TOTAL; nothing constrained the per-note
    allocation, and run 13 showed notes owning 11–17 sections diluting to
    ~1.7 completeness beside 4.5–5.0 for notes owning 6–8."""
    sections = split_sections(source_text)
    out: dict[str, tuple[int, int]] = {}
    for pn in planned_notes:
        if not isinstance(pn, dict):
            continue
        name = str(pn.get("filename") or pn.get("note") or "").strip()
        if not name:
            continue
        owned = owned_sections_for(name, coverage_map, sections)
        words = sum(len(sec.split()) for sec in owned.values())
        out[name] = (words, len(owned))
    return out


def make_note_coverage_predicate(plan_doc: dict, source_text: str, *, strict: bool = False):
    """A wave-scope predicate over the wave's written note paths.

    One issue per note that left ≥1 owned section uncovered, naming the
    note path and the sections (the fix-stage/diagnostics channel).
    WARNING (advisory) by default — the report-first rung; ``strict=True``
    emits ERROR, the calibrated promotion. Notes without owned sections,
    unreadable files, and unverifiable sections are all skipped — the
    predicate only speaks when it can prove absence.
    """
    sections = split_sections(source_text)
    coverage_map = plan_doc.get("section_coverage_map") or []
    severity = Severity.ERROR if strict else Severity.WARNING

    def predicate(paths: Sequence[Path | str], /, **_) -> Sequence[Issue]:
        if not sections or not isinstance(coverage_map, list) or not coverage_map:
            return []
        issues: list[Issue] = []
        for p in paths:
            path = Path(p)
            owned = owned_sections_for(path.name, coverage_map, sections)
            if not owned:
                continue
            try:
                note_text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            _cov, uncovered, _unv = compute_note_coverage(note_text, owned)
            if uncovered:
                issues.append(
                    Issue(
                        severity,
                        "WAVE-002",
                        "note_coverage",
                        f"owned sections uncovered in {path}: {uncovered}",
                    )
                )
        return issues

    return predicate


def extend_wave_gate_with_note_coverage(
    suite, plan_doc: dict, source_text: str, *, strict: bool = False
):
    """Append the post-wave sweeps to an existing wave-gate suite: the
    ``note_coverage`` sweep when the plan carries a coverage map and source
    (identity otherwise — parity for toy/degenerate plans), and the W4
    ``link_resolution`` sweep unconditionally (it needs only the written
    paths — the computed replacement for the LLM verify step's asserted
    link checking)."""
    from tessellum.composer.gates import Gate, GateSuite, link_resolution_predicate

    gates = tuple(suite.gates)
    cmap = plan_doc.get("section_coverage_map") if isinstance(plan_doc, dict) else None
    if isinstance(cmap, list) and cmap and source_text and source_text.strip():
        gates = gates + (
            Gate(
                gate_id="note_coverage",
                kind="sweep",
                scope="wave",
                predicate=make_note_coverage_predicate(
                    plan_doc, source_text, strict=strict
                ),
                cause="note_coverage",
            ),
        )
    gates = gates + (
        Gate(
            gate_id="link_resolution",
            kind="sweep",
            scope="wave",
            predicate=link_resolution_predicate,
            cause="link_resolution",
        ),
    )
    if gates == tuple(suite.gates):
        return suite
    return GateSuite(gates=gates)
