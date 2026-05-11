---
tags:
  - resource
  - analysis
  - retrieval
  - knowledge_management
  - building_blocks
  - information_retrieval
  - evaluation
keywords:
  - building block value redirected
  - epistemic congruence
  - context assembly
  - post-retrieval evaluation
  - BB structural signatures
  - answer quality assessment
  - failure diagnostics
  - typed knowledge value
topics:
  - retrieval evaluation
  - knowledge building blocks
  - information retrieval
  - answer quality
language: markdown
date of note: 2026-04-21
status: active
building_block: argument
folgezettel: "5e2a"
folgezettel_parent: "5e2"
author: lukexie
---

# Sharpened Position: Building Block Structure Provides Value for Evaluation and Context Assembly, Not Strategy Routing (FZ 5e2a)

## The Sharpened Claim

> **The epistemological type of a note (its building block) does create distinctive structural signatures that are measurable and real — but these signatures provide value at the evaluation and context assembly stages, not at the strategy selection stage. Specifically: (1) epistemic congruence scoring uses BB type to detect "correct but wrong type" answers, (2) context assembly can order retrieved notes by BB demand priority, and (3) failure diagnostics can identify BB mismatch as a cause of low-quality answers.**

This is a narrower but defensible version of FZ 5e's original claim. The structural signatures survive; the routing application does not.

## How BB Structure Survived the v2 Benchmark

### The Evidence Against Strategy Routing (FZ 5e2)

The v2 benchmark showed dense retrieval (Hit@5=0.815) dominates all strategies uniformly across all building blocks. No BB requires a different strategy. The Strategy × BB heatmap that FZ 5e predicted would show "clear winners/losers per cell" instead shows a flat top row. BB-based strategy routing adds zero value at the retrieval stage.

### Three Applications Where BB Structure Still Adds Value

#### Application 1: Epistemic Congruence Scoring (FZ 5g3a)

The LLM reviewer that evaluates answer quality measures only factual correctness — it cannot detect whether an answer provides the *wrong type* of knowledge (e.g., a concept definition when the user asked for procedure steps). This is the "building block mismatch" failure mode identified in FZ 5g3.

BB typing enables **epistemic congruence**: comparing the question's BB demand (classifiable with κ=0.711 per FZ 5g1a) against the answer's BB supply. The congruence matrix from FZ 5g3a scores:

| Match | Score | Example |
|---|---|---|
| Full match (demand = supply) | 1.0 | Procedure question → procedure answer |
| Partial match (related BB) | 0.5 | Model question → concept answer (architecture partially defines components) |
| Mismatch (wrong BB) | 0.0 | Procedure question → concept answer (definition ≠ steps) |

Combined formula: `Quality = F × (0.5 + 0.5 × E)` where F = factual fidelity (1-5) and E = epistemic congruence (0.0, 0.5, 1.0). A factually correct answer (F=4) in the wrong register (E=0.0) now scores Quality = 2.0 → Rating 2 instead of 4.

This application requires BB typing but NOT at retrieval time — it operates post-synthesis, evaluating the answer after it's been generated. Dense retrieval finds the relevant notes; BB typing evaluates whether the synthesized answer used them correctly.

#### Application 2: Context Assembly Ordering

After dense retrieval returns the top-N candidates, the context assembly stage must decide:
- Which notes get full content inclusion (expensive) vs summary (cheap)?
- In what order should notes appear in the LLM's context window?

BB demand classification can inform both decisions:
- If the question demands a **procedure** (classified from question text), prioritize SOP notes in full and summarize concept notes
- If the question demands a **model** (architecture), prioritize area notes and model notes over observation notes
- Multi-block demands (FZ 5h's trail concept) can order context as: primary BB first → secondary BB → supporting BBs

This is not strategy *selection* (which strategy to run) but context *prioritization* (given dense retrieval's candidates, how to present them). The distinction matters because dense retrieval has already found the right notes — BB typing helps assemble them into the most useful context.

#### Application 3: Failure Diagnostics

When an answer scores low, BB typing provides a diagnostic dimension invisible to content-only analysis:

| Diagnostic | Without BB | With BB |
|---|---|---|
| "Answer was wrong" | Check factual accuracy against source notes | Check factual accuracy AND epistemic congruence |
| "Answer was incomplete" | Check if relevant notes were retrieved | Check if relevant notes of the *right BB type* were retrieved |
| "Answer was unhelpful" | Unclear cause | BB mismatch: retrieved concept notes when user needed procedures |

The v2 benchmark's 18.5% failure rate for dense retrieval is currently unexplained (OQ-R8). BB typing could help classify these failures: are they missing notes (retrieval failure), wrong BB type (congruence failure), or genuinely unanswerable?

## Why This Position Is Defensible

1. **The structural signatures are empirically confirmed**: Term notes receive 4.8× higher average inlinks, SOP notes cluster by `note_second_category`, model notes are densely interconnected. These are measured properties, not theoretical predictions.

2. **BB demand is classifiable**: κ=0.711 from FZ 5g1a means the classification input is feasible — this was confirmed independently of strategy routing.

3. **The evaluation gap is real**: FZ 5g3 identified that the LLM reviewer measures factual correctness only. This is a construct validity failure independent of retrieval performance. BB typing addresses it.

4. **Dense retrieval doesn't solve the assembly problem**: Finding the right notes (dense retrieval's strength) is necessary but not sufficient for a good answer. The assembly of those notes into a response is a separate stage where BB typing can add value without competing with dense retrieval.

## Testable Predictions

**P1**: Answers evaluated with epistemic congruence (Quality = F × (0.5 + 0.5 × E)) will show higher inter-rater agreement than answers evaluated with factual fidelity alone — because the congruence dimension makes implicit quality intuitions explicit.

**P2**: For the 18.5% of questions where dense retrieval fails (no gold note in top-5), BB mismatch will account for at least 20% of these failures — the retrieval succeeded but the wrong BB type was prioritized in context assembly.

**P3**: Context assembly ordering by BB demand priority (primary BB notes first) will improve answer quality scores compared to ordering by relevance score alone, specifically for multi-block demand questions.

## Scope and Limitations

This position claims BB typing adds value at the **evaluation and assembly stages only**. It explicitly concedes that BB typing adds zero value for:
- Strategy selection (which retrieval strategy to run)
- Query expansion (how to expand the search terms)
- Initial candidate scoring (how to rank dense retrieval results)

The redirected value is real but narrower than FZ 5e's original claim. The meta-question (FZ 5) answer becomes: *"Typed knowledge provides measurable value for answer quality evaluation and context assembly, not for retrieval strategy selection."*

---

## Related Notes

### Cross-Trail Convergence (Architecture Trail)
- **[FZ 7g1a1a1a1a1: ★ Synthesis — The Vault Is a CQRS Knowledge System](thought_synthesis_two_systems_cqrs_value_proposition.md)** — names this note's redirected position as the **R-D rule**: System P artifacts (BB structural signatures) belong at System D's stage 3-4 (evaluation, re-rank, assembly), never at stage 1 (candidate generation). One of 13 Phase 3 syntheses converging on the same pattern.

### Within Phase 3 (Unification) Trail
- **[FZ 5e2: Counter — Dense Retrieval Refutes BB Strategy Routing](counter_dense_retrieval_refutes_bb_strategy_routing.md)** — the counter this note responds to
- **[FZ 5e: Question Type × Building Block Alignment](thought_question_type_building_block_retrieval_alignment.md)** — the original claim, now narrowed
- **[FZ 5g3a: Epistemic Congruence Metric](thought_epistemic_congruence_metric.md)** — the primary application of this redirected value
- **[FZ 5g3b: Epistemic Congruence Skill Design](analysis_epistemic_congruence_skill_design.md)** — implementation of congruence into the review skill
- **[FZ 5g3: Counter — Rating Instrument Lacks BB Lens](counter_rating_instrument_lacks_bb_lens.md)** — the evaluation gap that BB typing fills
- **[FZ 5g1a: BB Demand Inter-Annotator Agreement](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)** — κ=0.711 feasibility
- **[FZ 5: Meta-Question — Value of Typed Knowledge](thought_meta_question_value_of_typed_knowledge.md)** — parent question, now answered more precisely
- **[Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)** — the 8-type taxonomy
