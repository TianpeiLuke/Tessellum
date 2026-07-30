"""J3 (FZ 20k9c1a1a1b7c2k2): Tier-3 content-fidelity scoring for the J3
convergence run — the shipped 6-dimension ``tessellum.composer.eval.LLMJudge``
(same judge + model as the primary workspace's b7c4 first-ever Tier-3
measurement, so the scores are comparable), each generated note judged against
the full source corpus.

Usage: PYTHONPATH=src python3 runs/eval/j3_tier3_judge.py <notes_dir> <source_md> [out_json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from tessellum.composer import AnthropicBackend
from tessellum.composer.eval import LLMJudge

DIMENSIONS = (
    "relevance",
    "completeness",
    "accuracy",
    "clarity",
    "structural_integrity",
    "epistemic_congruence",
)


def main() -> int:
    notes_dir = Path(sys.argv[1])
    source_md = Path(sys.argv[2])
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else notes_dir / "tier3_report.json"

    source = source_md.read_text(encoding="utf-8")
    judge = LLMJudge(AnthropicBackend(model="claude-sonnet-4-6"))
    expected = (
        "A faithful, atomic Zettelkasten note digested from the source below. "
        "It must say true things about the right content (no fabrication), "
        "cover its mapped sections, carry exactly one building_block, and be "
        "clearly written.\n\n=== SOURCE ===\n" + source
    )

    notes = sorted(p for p in notes_dir.rglob("*.md"))
    per_note: list[dict] = []
    for note in notes:
        scores = judge.score(
            expected_description=expected,
            actual_output=note.read_text(encoding="utf-8"),
            dimensions=DIMENSIONS,
        )
        row = {
            "note": note.name,
            "scores": {s.dimension: s.score for s in scores},
            "justifications": {s.dimension: s.justification[:200] for s in scores},
        }
        row["mean"] = round(sum(row["scores"].values()) / len(DIMENSIONS), 3)
        per_note.append(row)
        print(f"  judged {note.name}: mean {row['mean']}", file=sys.stderr)

    if not per_note:
        print("no notes found", file=sys.stderr)
        return 1
    dims = {
        d: round(sum(r["scores"][d] for r in per_note) / len(per_note), 3)
        for d in DIMENSIONS
    }
    overall = round(sum(dims.values()) / len(DIMENSIONS), 3)
    report = {
        "notes_scored": len(per_note),
        "dimensions": dims,
        "overall": overall,
        "overall_pct": round(overall / 5 * 100, 1),
        "per_note": per_note,
    }
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("notes_scored", "dimensions", "overall", "overall_pct")}, indent=2))
    return 0


if __name__ == "__main__":
    main()
