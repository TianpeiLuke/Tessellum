"""B3b (FZ 20k9c1a1a1b7c2k2a3a, phase-3 residue): the OWNED-SECTION-SPAN
re-calibration of the grounding certificate.

Thresholds are span-method-specific by construction, so flipping the runtime
verifier from the full-source span to per-note owned-section spans (the B3
false-block caveat's mandated configuration) first requires calibrating ON
that span method. Same protocol as B3 — real golden-note sentences
(faithful) + handcrafted fabrications (unfaithful), the REAL scorer on the
designated model, ``calibrate(alpha=0.05)`` — but every claim is scored
against the OWNED SLICE of the note it belongs to: the golden coverage map
(``golden_coverage_map.json``, transcribed from the golden plan and
code-verified: every section resolves) ⨝ the FENCE-AWARE section split (F12
— calibrating on truncated spans would have baked the defect into the
threshold). Each fabrication is assigned to the note whose topic it invades,
exactly as a fabricated claim in deployment sits inside some note's slice.

Output: eval/digestion_pipeline/calibration_grounding_owned_span.json.
Usage: PYTHONPATH=src python3 runs/eval/b3b_owned_span_calibration.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from tessellum.composer import AnthropicBackend
from tessellum.composer.claim_extraction import extract_claims
from tessellum.composer.knowledge_plan import ClaimProvenance
from tessellum.composer.llm_claim_scorer import make_llm_claim_scorer
from tessellum.composer.note_coverage import (
    norm_heading,
    owned_sections_for,
    split_sections,
)
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

# Each fabrication sits inside the note whose slice it would invade.
FABRICATIONS = [
    ("Claude Code limits each project to exactly three MCP servers, and every server must re-authenticate hourly.", "cc_mcp_overview"),
    ("The MCP protocol requires a paid enterprise license before any remote server can be added.", "cc_mcp_overview"),
    ("All MCP tool results are stored permanently in Anthropic's cloud and cannot be deleted.", "cc_mcp_overview"),
    ("Windows is the only supported platform for MCP servers; macOS support was removed in 2025.", "cc_mcp_quickstart"),
    ("Each MCP server consumes a fixed 50,000 tokens of context the moment it connects.", "cc_mcp_tool_search"),
    ("Project-scope MCP configuration files must be encrypted with GPG before Claude Code will read them.", "cc_mcp_installation_scopes"),
    ("OAuth authentication for MCP servers expires after exactly seven minutes and cannot be refreshed.", "cc_mcp_authentication"),
    ("The maximum number of tools a single MCP server may expose is 12.", "cc_mcp_server_management"),
]


def main() -> int:
    corpus = "\n\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted(SLICE.glob("input_pages/*.md*"))
    )
    sections = split_sections(corpus)
    cmap = json.loads((SLICE / "golden_coverage_map.json").read_text())
    unresolved = sorted({
        str(r["source_section"]) for r in cmap
        if norm_heading(str(r["source_section"])) not in sections
    })
    assert not unresolved, f"transcription rot: {unresolved}"

    notes = sorted((SLICE / "golden_notes").glob("*.md"))
    spans: dict[str, str] = {}
    for note in notes:
        owned = owned_sections_for(note.name, cmap, sections)
        assert owned, f"no owned sections resolve for {note.name}"
        spans[note.stem] = "\n\n".join(owned.values())[:SPAN_CAP]

    def span_text_of(ref: str) -> str | None:
        return spans.get(ref)

    faithful = []
    for note in notes:
        prov = (ClaimProvenance(span_id=note.stem, source_ref=note.stem),)
        body = note.read_text(encoding="utf-8").split("---", 2)[-1]
        claims = extract_claims(body, prov, note_id=note.stem)
        usable = [c for c in claims if len(c.text.split()) >= 8]
        faithful.extend(usable[:REAL_PER_NOTE])
    fabricated = []
    for text, owner in FABRICATIONS:
        prov = (ClaimProvenance(span_id=owner, source_ref=owner),)
        fabricated.extend(extract_claims(text, prov, note_id=f"fab_{owner}"))

    backend = AnthropicBackend(model=SCORER_MODEL)
    scorer = make_llm_claim_scorer(backend, span_text_of)

    print(f"scoring {len(faithful)} faithful + {len(fabricated)} fabricated claims "
          f"against OWNED spans on {SCORER_MODEL}…", file=sys.stderr)
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

    faithful_result = certify(
        faithful[:REAL_PER_NOTE], scorer=scorer, thresholds=thresholds,
        note_domain="documentation",
    )
    mixed = faithful[:2] + [f for f in fabricated
                            if f.source_ref == "cc_mcp_overview"][:1]
    blocked_result = certify(
        mixed, scorer=scorer, thresholds=thresholds, note_domain="documentation",
    )

    artifact = {
        "scorer_model": SCORER_MODEL,
        "slice": "claude_code_mcp",
        "span_method": "owned_sections",
        "coverage_map": "golden_coverage_map.json",
        "alpha": ALPHA,
        "n_calibration": len(examples),
        "n_abstained": (len(f_scores) + len(b_scores)) - len(examples),
        "grounding_threshold": t,
        "full_source_threshold_for_comparison": 0.85,
        "span_chars": {k: len(v) for k, v in sorted(spans.items())},
        "faithful_scores": sorted(round(s.score, 3) for s in f_scores if not s.abstained),
        "fabricated_scores": sorted(round(s.score, 3) for s in b_scores if not s.abstained),
        "verification": {
            "faithful_note": faithful_result.decision,
            "note_with_fabrication": blocked_result.decision,
            "blocked_min_score": round(blocked_result.min_score, 3),
        },
        "date": "2026-07-30",
        "followup": "REFUTED - keep the full-source span: 4/32 faithful claims scored <=0.15 against their owned slice (notes carry legitimate cross-slice content); threshold collapsed 0.85 -> 0.15. Owned slices are for the coverage sweep, not the certificate.",
    }
    out = Path("eval/digestion_pipeline/calibration_grounding_owned_span.json")
    out.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: artifact[k] for k in (
        "grounding_threshold", "n_calibration", "n_abstained", "verification")}, indent=2))
    ok = (faithful_result.decision == "accept"
          and blocked_result.decision == "abstain")
    print("VERIFICATION:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
