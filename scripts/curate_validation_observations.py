"""Curate the v0.0.53 meta-DKS validation observation set.

Phase V of ``plans/plan_meta_dks_validation_and_polish.md``. Emits a
JSONL file of ~25 substantive DKS observations sourced from
``vault/resources/analysis_thoughts/`` open-questions sections. Each
observation is phrased as an *empirical claim or open situation*
(not a question), suitable as input to one DKS cycle.

Deterministic: the observation list is hardcoded below. Re-running
this script always produces the same JSONL. Provenance for each
entry lives in the ``fz_or_source`` field. The selection rationale +
Toulmin-component coverage map lives in the Phase V validation note
(``thought_meta_dks_validation_v053.md``, FZ 2c1a).

Usage::

    python scripts/curate_validation_observations.py
        --out runs/dks/validation_v0_0_53/observations.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# ── The curated observation set ────────────────────────────────────────────
# 25 entries, balanced across Trail 1 (Architecture) / Trail 2 (Dialectic) /
# Trail 3 (Retrieval). Each ``summary`` is phrased as an empirical claim or
# open situation — the input shape DKS step 1 expects.

OBSERVATIONS: list[dict] = [
    # ── Trail 1 — Architecture (8 observations) ─────────────────────────
    {
        "trail": "1",
        "fz_or_source": "FZ-1",
        "summary": "The BB ontology defines 10 directed epistemic edges, but empirical evidence from production question trails shows same-BB transitions account for ~46% of corpus traversals, with higher average quality ratings than the cross-BB transitions the schema targets — the ontology may be incomplete as a description of how typed knowledge is actually composed in real vaults.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1b",
        "summary": "The schema graph is finite at 8 nodes + 10 edges; the corpus graph is open and growing. The runtime (DKS) needs a counter_argument → model edge (pattern-of-failure aggregation) that the original 10-edge schema does not declare — whether to add this as an 11th schema edge or treat DKS's pattern step as non-epistemic plumbing is unsettled.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1c",
        "summary": "The note_second_category field (introduced for filename routing) is de-facto the sub-kind discriminator within multi-model environments, but was not originally designed for that purpose — whether to formalize it as the authoritative BB-subtype field, or introduce a separate bb_subtype: YAML field with closed enums per BB type, remains unresolved.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1c",
        "summary": "The seven architectural edge types identified in the AB analysis (Implements, Routes To, Computes, Runs On, Sources From, Reads) are domain-specific to ML-pipeline vaults; whether the architectural-edge vocabulary is a small finite closed set per domain or open-vocabulary like tags is unsettled.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1a1b",
        "summary": "The three CQRS rules (R-P, R-D, R-Cross) each have a defensive half that is rigorously held and a productive half that is deferred — specifically, R-P's productive half (schema co-evolution with runtime), R-D's productive half (BB-aware re-rank at Stage 3-4), and R-Cross's productive half (a typed P-side retrieval client) were latent in Phase 4, requiring Phase 5+ work to operationalise.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1a1b1",
        "summary": "TESS-004 (counter-argument notes must link to attacked argument notes) was proposed as a rule to promote the BB-edge relationship from declarative data to invariant, but depends on whether folgezettel_parent is the right home for that edge (making it structural) or whether the link should live in prose (See Also), which is fragile.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1a1a",
        "summary": "The CQRS architecture's core commitment is one boundary between declaration (System P) and computation (System D) with one shared substrate — but the granularity of that boundary (is the substrate the note-level vault, or note-plus-index, or note-plus-traces?) remains subtly underconstrained.",
    },
    {
        "trail": "1",
        "fz_or_source": "FZ-1a1",
        "summary": "The two-system value proposition claims that typed knowledge enables both audited construction (System P) and richer retrieval (System D) without coupling the two — but empirical measurement of whether the value is genuinely split across two independent metrics or whether one system's gains accidentally suppress the other's potential has not been conducted.",
    },
    # ── Trail 2 — Dialectic / DKS (9 observations) ──────────────────────
    {
        "trail": "2",
        "fz_or_source": "FZ-2",
        "summary": "DKS was derived from three formal foundations (Dung, Toulmin, IBIS) but introduces one novel mechanism none of them provides: the closed feedback loop where counter-arguments revise the warrants of future arguments — whether this closed loop is load-bearing for the learning claim or whether a simpler non-persistent debate mechanism (like MAD) achieves equivalent practical value is empirically untested.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2a",
        "summary": "DKS is defined as seven components corresponding to seven BB-to-BB edges, but the step count is not invariant — confidence gating can short-circuit at step 2 (gated path), or to step 4 (short-circuit on agreement), or run the full 7-component cycle — whether the seven-component count remains the defining invariant or whether the phase count should vary based on observed confidence is unsettled.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2a1",
        "summary": "DKS's FZ integration maps the 7-component cycle to a 5-node FZ subtree (step 4 produces an edge, not a node), and FZ assignment (fresh/extend/branch modes) is driven by step 1's agent decision — whether the FZ allocation logic should be a dedicated step 0 (trail selection runs before observation capture) or kept in step 1's prompt is undecided.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2a2",
        "summary": "DKS as an FSM has three terminal acceptance states (closed loop, short-circuit, gated), and the corpus-FSM carries history via a warrant thread across cycles, making it not strictly Markovian — whether to formalise this as a finite-state automaton with scratchpad or to model it as a stateful process with formal memory structure is open.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2a2",
        "summary": "Step 6 (pattern discovery) transitions via CTR → MOD (aggregating), but this edge is not in the original 10-edge schema, living instead as plumbing — whether to promote it to a fully-typed 11th epistemic edge or to keep it as a non-typed procedural operation is a Phase 4-class architectural decision.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2b",
        "summary": "DKS Phase 4-5 ships with the R-Cross productive half (P-side RetrievalClient for step 1/6 lookups), but without observable evidence of whether DKS cycles actually call retrieval at meaningful rates, or whether the client is an available interface that cycles rarely use — the operational reality of how often P actually calls D in production remains unknown.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2c",
        "summary": "The three-stage transition-model adaptation pipeline (discovery via corpus statistics, formalisation via LLM-labeling, governance via meta-DKS) is proposed for Phase 11+, but the Stage 1 frequency threshold (default 5) and Stage 2 sample size (N=5) are unvalidated heuristics — what corpus size and frequency threshold actually produces statistically meaningful schema proposals is empirically unresolved.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2c",
        "summary": "The proposed Layer B (architectural edges, same-BB sub-kind-parameterised) is intended to be corpus-induced and learnable, while Layer A (epistemic edges, cross-BB) stays human-authored — but the division of labour assumes the two layers are cleanly separable; whether a real deployment will discover an architectural edge that should be elevated to Layer A is unsettled.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2c1",
        "summary": "Meta-DKS in v0.0.52 ships with rule-based heuristics for proposal generation (Toulmin-dominance triggers hand-authored edge candidates), but the evidence bar for retraction (50+ cycles, stricter than addition's 20 cycles) is unvalidated — whether retracts should require higher evidence, and by how much, depends on production evidence that does not yet exist.",
    },
    {
        "trail": "2",
        "fz_or_source": "FZ-2c1",
        "summary": "Meta-DKS's cold-start guard (below 20 cycles, zero proposals) is intended to avoid schema edits from noise, but 20 cycles is an unvalidated minimum — whether the threshold should scale with vault size, corpus stability, or Toulmin-failure-distribution entropy is unresolved.",
    },
    # ── Trail 3 — Retrieval (8 observations) ────────────────────────────
    {
        "trail": "3",
        "fz_or_source": "FZ-3",
        "summary": "Tessellum's retrieval defaults to hybrid RRF (BM25 + dense via RRF) for a +12pp Hit@5 lift empirically measured on 4,823 questions — but the Hit@K-to-answer-quality correlation is only ρ=0.37, meaning the +12pp lift may be benchmark theater; whether the hybrid lift persists on end-to-end answer quality (independent of Hit@K) is the underlying unsettled question.",
    },
    {
        "trail": "3",
        "fz_or_source": "FZ-3a",
        "summary": "Tessellum deliberately omits Personalized PageRank from the default surface despite PPR's +11pp Hit@K advantage on multi-hop questions, choosing best-first BFS (8× faster, comparable answer quality) — but the latency/quality tradeoff is not calibrated to actual user patience thresholds, and whether 250ms vs 30ms queries materially changes user satisfaction is unvalidated.",
    },
    {
        "trail": "3",
        "fz_or_source": "FZ-5e1c1c",
        "summary": "The hybrid retrieval hypothesis proposes that graph post-processing (re-ranking via embedding similarity + graph proximity + BB alignment + link context, with weights α=0.50/β=0.20/γ=0.15/δ=0.15) will improve answer quality by 0.5-1.0 points on a 5-point scale — but the blending weights are fixed heuristics; whether they should be adaptive per question type or domain is unresolved.",
    },
    {
        "trail": "3",
        "fz_or_source": "FZ-5f",
        "summary": "Folgezettel trails constitute a fifth retrieval modality (FZ-ordered traversal) for reasoning-trace questions, orthogonal to the four content-matching strategies — but this modality is currently unrealized in the index (FZ edges live only in YAML frontmatter, not in the note_links table); whether indexing FZ edges as distinct link_type values or leveraging pre-computed entry-point indexes is the right implementation path is unsettled.",
    },
    {
        "trail": "3",
        "fz_or_source": "FZ-5j",
        "summary": "Hub dilution (the property that strong graph topology metrics causally produce weak graph retrieval performance) is formalised as a mathematical consequence of scale-free networks, but this analysis assumes the 1.5-1.8 scale-free exponent is stable — whether vault growth (e.g., 50K → 500K notes) will shift the exponent and alter the dilution dynamics is an empirical unknown.",
    },
    {
        "trail": "3",
        "fz_or_source": "FZ-5j",
        "summary": "Hub dilution predicts that in any scale-free KG with α < 2.0, BFS-based retrieval will underperform content-based retrieval — but this prediction is derived theoretically; empirical validation across 3+ distinct knowledge graphs (different domains, ontologies) has not been conducted, leaving the universality of the claim unconfirmed.",
    },
    {
        "trail": "3",
        "fz_or_source": "FZ-3a (Synthesis)",
        "summary": "The unified SQLite engine (FTS5 + sqlite-vec + metadata in one file) was chosen for atomicity and zero-coordination properties, but the build-time cost (full rebuild on schema changes) is acceptable only for small vaults; whether incremental schema migration becomes necessary at >100K notes, and when unified-engine portability breaks, is an unsolved scaling question.",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runs/dks/validation_v0_0_53/observations.jsonl"),
        help="Output JSONL path.",
    )
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        for entry in OBSERVATIONS:
            # DKSObservation requires a 'summary' string; extra fields
            # (trail, fz_or_source) are metadata for downstream
            # interpretation and are ignored by the cycle runner.
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Wrote {len(OBSERVATIONS)} observations to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
