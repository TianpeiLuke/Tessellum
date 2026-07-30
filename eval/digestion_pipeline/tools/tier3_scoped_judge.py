"""Phase-1 instrument fix (FZ 20k9c1a1a1b7c2k2a3a): the PER-NOTE-SCOPED
Tier-3 judge — the discriminating test both open gradients demand.

The b7c4-comparable judge scores every note against the ENTIRE corpus, which
structurally penalizes narrow notes on wide heterogeneous sources. This judge
scores each note against ITS OWNED SECTIONS (the run's own coverage map ⨝ the
measured source, E2.3's spans), falling back to the whole corpus only when no
owned sections resolve. Same 6 dimensions, same judge model — so scoped and
whole-corpus scores are comparable per dimension.

Usage: PYTHONPATH=src python3 runs/eval/tier3_scoped_judge.py <run_root> <job_id> <notes_dir> [out_json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from tessellum.composer import AnthropicBackend
from tessellum.composer.eval import LLMJudge

DIMENSIONS = (
    "relevance", "completeness", "accuracy",
    "clarity", "structural_integrity", "epistemic_congruence",
)
_HEADING_RE = re.compile(r"(?m)^(#{1,3})\s+(.+)$")


def _norm(s: str) -> str:
    return " ".join(s.lower().split())


def _name_match(a: str, b: str) -> bool:
    if a == b:
        return True
    if len(a) > len(b) and a.endswith(b):
        return a[-len(b) - 1] in ("_", "-", "/", ".")
    return False


def _split_sections(corpus: str) -> dict[str, str]:
    """Heading (normalized) → its section text (heading line up to the next
    heading of ANY level — the same H1–H3 family the code ledger measures)."""
    matches = list(_HEADING_RE.finditer(corpus))
    out: dict[str, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(corpus)
        out.setdefault(_norm(m.group(2)), corpus[m.start():end])
    return out


def main() -> int:
    run_root, job_id, notes_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    out_path = (Path(sys.argv[4]) if len(sys.argv) > 4
                else run_root / "tier3_scoped_report.json")

    plan = json.loads(
        (run_root / "runs/runtime/artifacts" / job_id / "plan.json").read_text()
    )
    src_dir = run_root / "runs/runtime/archive" / job_id / "source"
    corpus = "\n\n".join(p.read_text(encoding="utf-8") for p in sorted(src_dir.iterdir()))
    sections = _split_sections(corpus)
    cmap = plan.get("section_coverage_map") or []

    FULL_SOURCE_CAP = 30_000

    def owned_span(note_name: str) -> tuple[str, int]:
        base = note_name
        parts = []
        for row in cmap:
            if not isinstance(row, dict):
                continue
            target = str(row.get("maps_to_note") or row.get("note") or "").strip()
            target = target.rsplit("/", 1)[-1]
            if not target or not (_name_match(base, target) or _name_match(target, base)):
                continue
            sec = sections.get(_norm(str(row.get("source_section") or "")))
            if sec:
                parts.append(sec)
        return ("\n\n".join(parts), len(parts)) if parts else (corpus, 0)

    judge = LLMJudge(AnthropicBackend(model="claude-sonnet-4-6"))
    notes = sorted(notes_dir.glob("*.md"))
    per_note = []
    for note in notes:
        span, n_owned = owned_span(note.name)
        # DUAL CONTEXT (the first scoped run's own finding): slice-only
        # judging marked legitimately-sourced content from OUTSIDE the owned
        # sections as fabrication (mcp accuracy 4.4 whole-corpus -> 2.9
        # slice-only). Scope dimensions judge against the owned slice;
        # accuracy fact-checks against the full source.
        expected = (
            "A faithful, atomic Zettelkasten note digested from a source "
            "document. TWO CONTEXTS ARE PROVIDED:\n"
            "1. THE NOTE'S OWNED SLICE — the sections this note is responsible "
            "for per the plan's coverage map. Judge RELEVANCE and COMPLETENESS "
            "against THIS slice only (the note is not responsible for content "
            "outside it).\n"
            "2. THE FULL SOURCE — for fact-checking. Judge ACCURACY against "
            "the full source: a claim supported ANYWHERE in it is accurate; "
            "only claims supported NOWHERE in the full source are fabrication."
            "\n\n=== OWNED SLICE ===\n" + span
            + "\n\n=== FULL SOURCE (fact-check) ===\n" + corpus[:FULL_SOURCE_CAP]
        )
        # max_retries=0 on the client means OUR code owns retries (the F5
        # principle applied to eval scripts): 3 attempts, simple backoff.
        import time as _time
        for _attempt in range(3):
            try:
                scores = judge.score(
                    expected_description=expected,
                    actual_output=note.read_text(encoding="utf-8"),
                    dimensions=DIMENSIONS,
                )
                break
            except Exception as exc:
                if _attempt == 2:
                    # persistent server failure on THIS note: skip it and
                    # report honestly rather than losing the whole slice.
                    print(f"  SKIPPED {note.name} ({exc})", file=sys.stderr)
                    scores = None
                    break
                print(f"  retry {note.name} ({exc})", file=sys.stderr)
                _time.sleep(10 * (_attempt + 1))
        if scores is None:
            per_note.append({"note": note.name, "skipped": True,
                             "owned_sections": n_owned})
            continue
        row = {
            "note": note.name, "owned_sections": n_owned,
            "scores": {s.dimension: s.score for s in scores},
        }
        row["mean"] = round(sum(row["scores"].values()) / len(DIMENSIONS), 3)
        per_note.append(row)
        print(f"  {note.name}: {row['mean']} (owned={n_owned})", file=sys.stderr)

    scored = [r for r in per_note if not r.get("skipped")]
    dims = {d: round(sum(r["scores"][d] for r in scored) / len(scored), 3)
            for d in DIMENSIONS}
    overall = round(sum(dims.values()) / len(DIMENSIONS), 3)
    report = {
        "mode": "per-note-scoped-dual-context", "notes_scored": len(scored),
        "notes_skipped": len(per_note) - len(scored),
        "dimensions": dims, "overall": overall,
        "overall_pct": round(overall / 5 * 100, 1),
        "notes_with_owned_spans": sum(1 for r in scored if r["owned_sections"]),
        "per_note": per_note,
    }
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in
                      ("overall", "overall_pct", "notes_with_owned_spans")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
