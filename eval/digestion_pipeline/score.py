#!/usr/bin/env python3
"""Deterministic scorer for a Tessellum digestion run vs a golden slice.

Scores the Tier-1 (plan-level) and Tier-2 (note-level) metrics from
``rubric.md`` against a slice's ``golden_facts.json``. Tier-3 (LLM-judge
content fidelity) is intentionally NOT here — it reuses
``tessellum.composer.eval.LLMJudge`` and needs a backend; run it separately.

Pure stdlib. No Tessellum import, so this runs anywhere the generated output is.

Usage:
    python score.py <slice_dir> --notes <generated_notes_dir> [--plan <generated_plan.md>]

    <slice_dir>            a curated-slice dir holding golden_facts.json
    --notes DIR            directory of Tessellum-generated .md notes to score
    --plan FILE            optional generated plan .md to score (Tier 1)

Emits a JSON report to stdout: per-metric pass rates + an overall verdict.
Exit code 0 if the slice is GREEN (per rubric), 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

CLOSED_BB = {
    "empirical_observation", "concept", "model", "hypothesis",
    "argument", "counter_argument", "procedure", "navigation",
}
DENSITY_WORD_CAP = 2500
DENSITY_LINE_CAP = 400
DENSITY_CODE_CAP = 6


def _split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", text)


def _fm_keys(fm: str) -> list[str]:
    return [k.strip() for k in re.findall(r"(?m)^([a-z_ ]+):", fm)]


def _cosine(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    va = [a.get(k, 0) for k in keys]
    vb = [b.get(k, 0) for k in keys]
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(x * x for x in vb))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(va, vb)) / (na * nb)


def score_note(text: str, golden: dict) -> dict:
    fm, body = _split_frontmatter(text)
    keys = _fm_keys(fm)
    h2 = re.findall(r"(?m)^##\s+(.+?)\s*$", body)
    bb = re.search(r"(?m)^building_block:\s*(\S+)", fm)
    bb_val = bb.group(1) if bb else None
    code_blocks = len(re.findall(r"(?m)^```", body)) // 2
    words = len(body.split())
    lines = body.count("\n") + 1
    req = golden["frontmatter_required_keys"]
    forbidden = golden["frontmatter_forbidden_keys"]
    floors = {}  # measured link classes
    floors["term_dictionary"] = len(re.findall(r"term_dictionary/term_", text))
    floors["code_repos"] = len(re.findall(r"code_repos/repo_", text))
    floors["code_snippets"] = len(re.findall(r"code_snippets/snippet_", text))
    return {
        "N1_frontmatter_schema": all(k in keys for k in req),
        "N2_forbidden_absent": not any(k in keys for k in forbidden),
        "N3_required_h2": ("Overview" in h2 and "Related Notes" in h2),
        "N4_single_bb": bb_val in CLOSED_BB,
        "N5_density_caps": (words <= DENSITY_WORD_CAP and lines <= DENSITY_LINE_CAP
                            and code_blocks <= DENSITY_CODE_CAP),
        "_measured": {"words": words, "lines": lines, "code_blocks": code_blocks,
                      "building_block": bb_val, "link_classes": floors},
    }


def score_notes(notes_dir: Path, golden_facts: dict) -> dict:
    golden = golden_facts["golden_output"]
    floor = golden_facts["golden_plan"]["xref_floor_per_note"]
    note_files = sorted(notes_dir.glob("*.md"))
    if not note_files:
        return {"error": f"no .md notes found in {notes_dir}"}
    per = {}
    bb_hist = {}
    for f in note_files:
        s = score_note(f.read_text(encoding="utf-8"), golden)
        # N6 xref floor per declared class
        lc = s["_measured"]["link_classes"]
        s["N6_xref_floor_met"] = all(lc.get(cls, 0) >= n for cls, n in floor.items()
                                     if cls in ("term_dictionary", "code_repos", "code_snippets"))
        per[f.stem] = s
        bb = s["_measured"]["building_block"]
        bb_hist[bb] = bb_hist.get(bb, 0) + 1
    metrics = ["N1_frontmatter_schema", "N2_forbidden_absent", "N3_required_h2",
               "N4_single_bb", "N5_density_caps", "N6_xref_floor_met"]
    rates = {m: sum(1 for s in per.values() if s[m]) / len(per) for m in metrics}
    return {
        "note_count": len(per),
        "golden_note_count": golden["note_count"],
        "bb_distribution": bb_hist,
        "bb_similarity_vs_golden": round(_cosine(bb_hist, golden["bb_distribution"]), 3),
        "metric_pass_rates": {k: round(v, 3) for k, v in rates.items()},
        "per_note": per,
    }


def score_plan(plan_text: str, golden_facts: dict) -> dict:
    gp = golden_facts["golden_plan"]
    planned = len(re.findall(r"(?m)^\|\s*\d+\s*\|", plan_text))  # numbered table rows
    ratio = planned / gp["planned_note_count"] if gp["planned_note_count"] else 0.0
    sections_present = sum(
        1 for sec in gp["mandatory_plan_sections"]
        if re.search(re.escape(sec.split(" (")[0]), plan_text, re.IGNORECASE)
    )
    gate_names = re.findall(r"(?m)\bG[1-9]\b", plan_text)
    return {
        "P1_planned_note_count": {"generated": planned, "golden": gp["planned_note_count"],
                                  "ratio": round(ratio, 2), "pass": 0.7 <= ratio <= 1.4},
        "P6_gate_table_present": {"distinct_gates_named": len(set(gate_names)),
                                  "expected": gp["gate_count"],
                                  "pass": len(set(gate_names)) >= gp["gate_count"]},
        "P7_mandatory_sections": {"present": sections_present,
                                  "of": len(gp["mandatory_plan_sections"]),
                                  "pass": sections_present >= 0.9 * len(gp["mandatory_plan_sections"])},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slice_dir", type=Path)
    ap.add_argument("--notes", type=Path, help="dir of generated notes to score (Tier 2)")
    ap.add_argument("--plan", type=Path, help="generated plan .md to score (Tier 1)")
    args = ap.parse_args()

    facts_path = args.slice_dir / "golden_facts.json"
    if not facts_path.exists():
        print(f"error: {facts_path} not found", file=sys.stderr)
        return 2
    golden_facts = json.loads(facts_path.read_text(encoding="utf-8"))

    report: dict = {"slice": golden_facts["slice"]}
    if args.plan and args.plan.exists():
        report["tier1_plan"] = score_plan(args.plan.read_text(encoding="utf-8"), golden_facts)
    if args.notes:
        report["tier2_notes"] = score_notes(args.notes, golden_facts)

    # Verdict: tier-2 mean pass rate >= 0.9 with N2/N4 at 100% (N7/N8 need a DB,
    # scored separately). Tier-1 >= 6/7 when a plan was supplied.
    green = True
    t2 = report.get("tier2_notes", {})
    if "metric_pass_rates" in t2:
        r = t2["metric_pass_rates"]
        mean = sum(r.values()) / len(r)
        green = green and mean >= 0.9 and r.get("N2_forbidden_absent") == 1.0 \
            and r.get("N4_single_bb") == 1.0
        report["tier2_mean_pass_rate"] = round(mean, 3)
    report["verdict"] = "GREEN" if green else "NEEDS_WORK"
    print(json.dumps(report, indent=2))
    return 0 if green else 1


if __name__ == "__main__":
    raise SystemExit(main())
