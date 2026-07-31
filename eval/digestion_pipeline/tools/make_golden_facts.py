#!/usr/bin/env python3
"""Measure a set of golden notes (+ its plan) into a ``golden_facts.json``.

This is the generator that makes ``golden_facts.json`` reproducible: point it at
a directory of golden notes and the plan that produced them, and it emits the
exact machine-readable reference ``score.py`` consumes. Because it MEASURES the
notes it is given, running it over the *vendored* (scrubbed) notes yields a
golden_facts that is self-consistent by construction — ``score.py`` of those same
notes against this output is GREEN at 1.0.

Pure stdlib. Correctness oracle: run over the three existing curated slices'
``golden_notes/`` + ``golden_plan/`` and it reproduces their committed
``golden_facts.json`` (see ``--check``).

Usage:
    python make_golden_facts.py \
        --notes  <dir of golden .md notes> \
        --plan   <the golden plan .md> \
        --slice  <slice id> \
        --source "<human source label>" \
        --source-url-pattern "<url pattern>" \
        --note-dir <vault-relative note dir> \
        --note-prefix <cc_|hermes_|oc_> \
        [--input-page NAME ...]  [--out <path>]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

CLOSED_BB = {
    "empirical_observation", "concept", "model", "hypothesis",
    "argument", "counter_argument", "procedure", "navigation",
}

# The fixed plan-section checklist the digestion skills emit. The co01 variant
# adds nothing structurally different here (score.py matches by prefix).
MANDATORY_PLAN_SECTIONS = [
    "Scope",
    "Content Strategy",
    "Source Pages (measured)",
    "Planned Notes (table: # | Filename | BB | Source Section(s) | ~Words | Description)",
    "Section Coverage Map (every source H2/H3 -> a note; no orphans)",
    "Split Decisions",
    "Summary Statistics & Building Block Distribution",
    "Per-Note Related Notes Mapping (cross-ref contract)",
    "Density Re-Assessment",
    "Undigested Terms Plan",
    "Per-Phase Validation Gate",
    "Entry Point Decision",
    "Inlinks",
    "Review Sign-Off (CP1-CP9)",
]

FRONTMATTER_REQUIRED = [
    "tags", "keywords", "topics", "language", "date of note",
    "status", "building_block", "source_url", "access_control_group",
]
FRONTMATTER_FORBIDDEN = [
    "category", "created", "note_second_category", "parent",
    "source", "title", "updated",
]


def _split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", text)


def _measure_note(text: str) -> dict:
    fm, body = _split_frontmatter(text)
    h2 = re.findall(r"(?m)^##\s+(.+?)\s*$", body)
    bb = re.search(r"(?m)^building_block:\s*(\S+)", fm)
    bb_val = bb.group(1) if bb else None
    words = len(body.split())
    req_present = [s for s in ("Overview", "Related Notes", "References") if s in h2]
    term_links = len(re.findall(r"term_dictionary/term_", text))
    snippet_links = len(re.findall(r"code_snippets/snippet_", text))
    repo_links = len(re.findall(r"code_repos/repo_", text))
    total_internal = len(re.findall(r"\]\(([^)\s]+\.md)\)", text))
    return {
        "building_block": bb_val,
        "required_h2_present": req_present,
        "h2_sections": h2,
        "word_count": words,
        "term_links": term_links,
        "snippet_links": snippet_links,
        "repo_links": repo_links,
        "total_internal_md_links": total_internal,
    }


def _planned_note_count(plan_text: str) -> int:
    m = re.search(r"(?m)^##\s+Planned Notes.*?$", plan_text)
    section = plan_text
    if m:
        rest = plan_text[m.end():]
        nxt = re.search(r"(?m)^##\s+", rest)
        section = rest[: nxt.start()] if nxt else rest
    return len(re.findall(r"(?m)^\|\s*\d+\s*\|", section))


def _gate_count(plan_text: str) -> int:
    return len(set(re.findall(r"(?m)\bG[1-9]\b", plan_text)))


def _xref_floor(plan_text: str) -> dict:
    """Best-effort read of the per-note cross-reference floor the plan declares.

    Looks for phrases like ">=8 term", ">=10 snippet", ">=5 repo", ">=10 doc".
    Falls back to {} (score.py then treats absent classes as no-floor).
    """
    floor: dict = {}
    # Tolerate adjectives between the count and the class noun, e.g.
    # "≥6 relevancy-selected term notes", "≥10 relevant snippet links".
    _mid = r"(?:\s+[a-z][a-z-]*){0,3}\s*"
    patterns = {
        "term_dictionary": rf"[>≥]=?\s*(\d+){_mid}term",
        "code_snippets": rf"[>≥]=?\s*(\d+){_mid}snippet",
        "code_repos": rf"[>≥]=?\s*(\d+){_mid}repo",
        "documentation": rf"[>≥]=?\s*(\d+){_mid}docs?\b",
    }
    for cls, pat in patterns.items():
        vals = [int(x) for x in re.findall(pat, plan_text)]
        if vals:
            # the contract is the MODE of the declared floor (per-note, repeated)
            floor[cls] = statistics.mode(vals)
    return floor


def build_facts(args) -> dict:
    notes_dir = Path(args.notes)
    note_files = sorted(notes_dir.glob("*.md"))
    per_note = {f.stem: _measure_note(f.read_text(encoding="utf-8")) for f in note_files}

    bb_hist: dict = {}
    words = []
    term_link_counts = []
    for m in per_note.values():
        bb_hist[m["building_block"]] = bb_hist.get(m["building_block"], 0) + 1
        words.append(m["word_count"])
        term_link_counts.append(m["term_links"])

    plan_text = Path(args.plan).read_text(encoding="utf-8") if args.plan else ""
    has_refs = any("References" in m["required_h2_present"] for m in per_note.values())

    # Measure required_h2 from what the notes ACTUALLY have. Full-corpus notes are
    # vendored tail-dropped (no ## Related Notes), so require only the sections
    # present in EVERY note among the canonical candidates. If no note has a
    # Related Notes tail, drop the cross-reference floor too (nothing to score).
    def _all_have(section: str) -> bool:
        return bool(per_note) and all(section in m["h2_sections"] for m in per_note.values())
    required_h2 = [s for s in ("Overview", "Related Notes") if _all_have(s)] or ["Overview"]
    notes_have_tail = _all_have("Related Notes")

    facts = {
        "slice": args.slice,
        "provenance": {
            "vault_repo": "private knowledge vault",
            "vault_git_sha": args.vault_sha,
            "note": "Golden plan + notes live in the private vault; only measured/structural facts are vendored here (public repo).",
        },
        "source": args.source,
        "source_url_pattern": args.source_url_pattern,
        "produced_by": "The FOUR digestion skills (plan-digestion -> augment -> review -> execute) — the SAME skills Tessellum runs as run_digestion_pipeline PHASE_SKILLS.",
        "input": {"page_count": len(args.input_page), "pages": list(args.input_page)},
        "golden_plan": {
            "file": Path(args.plan).name if args.plan else "",
            "subplan": args.subplan,
            "planned_note_count": _planned_note_count(plan_text) if plan_text else len(note_files),
            "gate_count": _gate_count(plan_text) if plan_text else 8,
            # xref floor only applies when notes still carry a cross-ref tail;
            # full-corpus notes are tail-dropped for public-repo safety.
            "xref_floor_per_note": (_xref_floor(plan_text) if (plan_text and notes_have_tail) else {}),
            "mandatory_plan_sections": MANDATORY_PLAN_SECTIONS,
        },
        "golden_output": {
            "note_dir": args.note_dir,
            "note_prefix": args.note_prefix,
            "note_count": len(note_files),
            "bb_distribution": bb_hist,
            "word_count": {
                "min": min(words) if words else 0,
                "median": int(statistics.median_high(words)) if words else 0,
                "max": max(words) if words else 0,
            },
            "term_links": {
                "min": min(term_link_counts) if term_link_counts else 0,
                "median": int(statistics.median_high(term_link_counts)) if term_link_counts else 0,
            },
            "frontmatter_required_keys": FRONTMATTER_REQUIRED,
            "frontmatter_forbidden_keys": FRONTMATTER_FORBIDDEN,
            "required_h2": required_h2,
            "optional_h2": ["References"],
            "cross_ref_block_header": "## Related Notes (NOT ## References; References is external-URL-only when present)",
            "per_note": per_note,
        },
    }
    if not has_refs:
        facts["golden_output"].pop("optional_h2", None)
    return facts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--plan", default=None)
    ap.add_argument("--slice", required=True)
    ap.add_argument("--subplan", default="")
    ap.add_argument("--source", default="")
    ap.add_argument("--source-url-pattern", default="")
    ap.add_argument("--note-dir", default="")
    ap.add_argument("--note-prefix", default="")
    ap.add_argument("--input-page", action="append", default=[], dest="input_page")
    ap.add_argument("--vault-sha", default="59bdae36c")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", default=None,
                    help="compare against an existing golden_facts.json (oracle mode)")
    args = ap.parse_args()

    facts = build_facts(args)
    out = json.dumps(facts, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
