"""B3 (FZ 20k9c1a1a1b7c2k1a): the grounding-gate calibration PILOT.

Pilot-before-fan-out: one slice (claude_code_mcp), per-claim labels — real
golden-note sentences (faithful=True) + handcrafted fabrications injected
against the same source span (faithful=False) — scored by the REAL LLM
entailment scorer (`make_llm_claim_scorer`, haiku as the designated scorer
model: entailment is a narrow judgment; the calibration artifact records the
model because thresholds are scorer-specific by construction). Then
`calibrate(alpha=0.05)` fixes the grounding threshold and `certify` is
verified to ADMIT a faithful claim-set and BLOCK one carrying a fabrication.

Output: eval/digestion_pipeline/calibration_grounding.json (the artifact) +
a stdout report. The runtime flip (loading this in the close gate with a
span_text_of over the note's owned sections) is the recorded follow-on.

Usage: PYTHONPATH=src python3 runs/eval/b3_calibration_pilot.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from tessellum.composer import AnthropicBackend
from tessellum.composer.claim_extraction import extract_claims
from tessellum.composer.knowledge_plan import ClaimProvenance
from tessellum.composer.llm_claim_scorer import make_llm_claim_scorer
from tessellum.composer.semantic_certificate import (
    LabeledExample,
    calibrate,
    certify,
)

SLICE = Path("eval/digestion_pipeline/claude_code_mcp")
SCORER_MODEL = "claude-haiku-4-5-20251001"
ALPHA = 0.05
REAL_PER_NOTE = 4
SPAN_CAP = 40_000

FABRICATIONS = [
    "Claude Code limits each project to exactly three MCP servers, and every server must re-authenticate hourly.",
    "The MCP protocol requires a paid enterprise license before any remote server can be added.",
    "All MCP tool results are stored permanently in Anthropic's cloud and cannot be deleted.",
    "Windows is the only supported platform for MCP servers; macOS support was removed in 2025.",
    "Each MCP server consumes a fixed 50,000 tokens of context the moment it connects.",
    "Project-scope MCP configuration files must be encrypted with GPG before Claude Code will read them.",
    "OAuth authentication for MCP servers expires after exactly seven minutes and cannot be refreshed.",
    "The maximum number of tools a single MCP server may expose is 12.",
]


def main() -> int:
    corpus = "\n\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted(SLICE.glob("input_pages/*.md*"))
    )[:SPAN_CAP]
    prov = (ClaimProvenance(span_id="corpus", source_ref="claude_code_mcp"),)

    def span_text_of(ref: str) -> str | None:
        return corpus if "claude_code_mcp" in ref else None

    notes = sorted((SLICE / "golden_notes").glob("*.md"))
    faithful = []
    for note in notes:
        body = note.read_text(encoding="utf-8").split("---", 2)[-1]
        claims = extract_claims(body, prov, note_id=note.stem)
        # sample mid-note sentences (skip headings-adjacent stubs)
        usable = [c for c in claims if len(c.text.split()) >= 8]
        faithful.extend(usable[:REAL_PER_NOTE])
    fabricated = extract_claims(" ".join(FABRICATIONS), prov, note_id="fabricated")

    backend = AnthropicBackend(model=SCORER_MODEL)
    scorer = make_llm_claim_scorer(backend, span_text_of)

    print(f"scoring {len(faithful)} faithful + {len(fabricated)} fabricated claims "
          f"on {SCORER_MODEL}…", file=sys.stderr)
    f_scores = scorer(faithful)
    b_scores = scorer(fabricated)

    examples = (
        [LabeledExample("grounding", s.score, True)
         for s in f_scores if not s.abstained]
        + [LabeledExample("grounding", s.score, False)
           for s in b_scores if not s.abstained]
    )
    thresholds = calibrate(examples, alpha=ALPHA, domains=("documentation",))
    t = thresholds.threshold_for("grounding")

    # verification: certify ADMITS the faithful set, BLOCKS a fabricated one
    faithful_result = certify(
        faithful[:REAL_PER_NOTE], scorer=scorer, thresholds=thresholds,
        note_domain="documentation",
    )
    mixed = faithful[:2] + fabricated[:1]
    blocked_result = certify(
        mixed, scorer=scorer, thresholds=thresholds, note_domain="documentation",
    )

    artifact = {
        "scorer_model": SCORER_MODEL,
        "slice": "claude_code_mcp",
        "alpha": ALPHA,
        "n_calibration": len(examples),
        "n_abstained": (len(f_scores) + len(b_scores)) - len(examples),
        "grounding_threshold": t,
        "faithful_scores": sorted(round(s.score, 3) for s in f_scores if not s.abstained),
        "fabricated_scores": sorted(round(s.score, 3) for s in b_scores if not s.abstained),
        "verification": {
            "faithful_note": faithful_result.decision,
            "note_with_fabrication": blocked_result.decision,
            "blocked_min_score": round(blocked_result.min_score, 3),
        },
        "date": "2026-07-29",
        "followup": "runtime flip: load thresholds in the close gate with span_text_of over owned sections",
    }
    out = Path("eval/digestion_pipeline/calibration_grounding.json")
    out.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: artifact[k] for k in (
        "grounding_threshold", "n_calibration", "n_abstained", "verification")}, indent=2))
    ok = (faithful_result.decision == "accept"
          and blocked_result.decision == "abstain")
    print("VERIFICATION:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
