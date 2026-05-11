---
tags:
  - resource
  - analysis
  - retrieval
  - knowledge_management
  - building_blocks
  - information_retrieval
  - pre_retrieval
  - reranking
keywords:
  - BB demand reranking
  - post-retrieval reranking
  - BB demand classification
  - context assembly
  - dense retrieval reranking
  - building block priority
  - trail-ordered context
  - multi-block assembly
topics:
  - retrieval evaluation
  - knowledge building blocks
  - information retrieval
  - query understanding
language: markdown
date of note: 2026-04-21
status: active
building_block: argument
folgezettel: "5h1a"
folgezettel_parent: "5h1"
author: lukexie
---

# Sharpened Position: BB Demand Classification Adds Value for Re-Ranking and Context Assembly, Not Strategy Routing (FZ 5h1a)

## The Sharpened Claim

> **BB demand classification (κ=0.711, 78% exact match) remains a valid and feasible capability — but its application shifts from pre-retrieval strategy routing (refuted by v2 benchmark) to post-retrieval re-ranking and context assembly. Specifically: (1) re-ranking dense retrieval's top-N candidates by BB demand alignment, (2) ordering context windows by BB trail logic for multi-block questions, and (3) providing a "BB demand filter" that deprioritizes retrieved notes whose building block mismatches the question's demand.**

This preserves FZ 5h's classification machinery while redirecting it to a stage where it can compete with (rather than be dominated by) dense retrieval.

## How BB Demand Classification Survived

### The v2 Refutation (FZ 5h1)

The v2 benchmark eliminated the routing target: dense retrieval at Hit@5=0.815 dominates all strategies uniformly. FZ 5h's routing table — mapping question types to specialized strategies — is strictly dominated. The classification step (Stage 1.5) has no actionable output because there is only one strategy to "select."

### The Classification Capability Itself Is Untouched

The refutation targets the *application* of BB demand classification (routing), not the *capability* itself:

| Property | Status |
|---|---|
| BB demand classifiable from question text | Confirmed (κ=0.711, FZ 5g1a) |
| Question type → BB demand lookup table | Valid descriptive mapping |
| Multi-block vs single-block demand distinction | Valid structural insight |
| Trail depth estimation heuristic | Valid (count entities, add for relationships) |
| **BB demand → strategy selection** | **Refuted** |

The classification signal exists and is reliable — it just needs a new consumer.

## Three Post-Retrieval Applications

### Application 1: BB-Aware Re-Ranking of Dense Retrieval Candidates

Dense retrieval returns candidates ranked by semantic similarity. But semantic similarity conflates *topical relevance* with *epistemological relevance*. A concept definition and a procedure for the same topic both embed close to the same query — yet one may be what the user needs while the other is not.

**Proposed re-ranking formula**:

```
final_score = α × dense_similarity + (1 - α) × bb_alignment

where:
  bb_alignment = 1.0 if candidate_bb == question_demand_bb
               = 0.5 if candidate_bb is partially aligned (from congruence matrix)
               = 0.0 if candidate_bb mismatches demand
  α = 0.7 (dense similarity still dominates, BB alignment is a secondary signal)
```

This is lightweight (no additional retrieval, just a score adjustment) and can only improve precision — it re-orders candidates that dense retrieval already found, never removes them.

**Why this could work**: Dense retrieval's 18.5% failure rate may include cases where the gold note was retrieved but ranked below position 5 because a topically-similar-but-wrong-BB note outranked it. BB-aware re-ranking would promote the correctly-typed note.

### Application 2: Trail-Ordered Context Assembly for Multi-Block Questions

FZ 5h's most promising concept — multi-block trail demands — applies not to which strategies to run, but to how to assemble context from dense retrieval's candidates:

| Question Demand | Trail Order | Context Assembly Logic |
|---|---|---|
| Architectural ("How does X work?") | model → concept → procedure | Lead with area/system notes, then definitions, then SOPs |
| Relational ("How is X related to Y?") | model → argument | Lead with both entity notes, then connecting reasoning |
| Multi-hop ("Why does X cause Y through Z?") | argument → concept → model → empirical | Lead with reasoning chain, ground in definitions, verify with data |
| Factual-in-context ("What metric for X in system Y?") | empirical_observation + model | Lead with the metric, then the system context |

The trail defines the **presentation order** of dense retrieval's candidates in the LLM's context window. Cognitive science suggests that information order affects synthesis quality — leading with the primary BB demand gives the LLM the most relevant frame first.

This application preserves FZ 5h's trail plans (§Multi-Block Demand, Table) but applies them at Stage 4 (Context Assembly) instead of Stage 2 (Retrieval).

### Application 3: BB Demand as Quality Filter for Working Memory

The working memory stage (Stage 3) accumulates candidates from dense retrieval and optionally from supplementary strategies. BB demand classification can serve as a **quality filter**:

- For single-block demands: boost candidates whose BB matches; do not remove mismatches (FZ 5h's "never reduce recall" constraint still applies)
- For multi-block demands: ensure the working memory contains at least one candidate per required BB in the trail — if dense retrieval didn't surface a procedure note for a procedural sub-demand, trigger a supplementary metadata-filtered search

This is the "cascade" fallback from FZ 5h (§Handling Ambiguity) applied at the working memory stage rather than the routing stage.

## Updated Pipeline Integration

```
Stage 1: Query Expansion
  → original_terms, expanded_terms, intent, resolved_term_ids

Stage 1.5: BB Demand Classification (RETAINED from FZ 5h)
  → bb_demand: {primary, secondary, demand_type}
  → trail_plan: [{bb, priority}, ...]
  (but NO strategy_config — no routing)

Stage 2: Dense Retrieval (SINGLE STRATEGY — no routing needed)
  → top-50 candidates by semantic similarity

Stage 3: Working Memory (NOW BB-AWARE)
  → Apply bb_alignment re-ranking to dense candidates
  → Check trail coverage: does candidate set include all demanded BBs?
  → If coverage gap: trigger supplementary retrieval for missing BB type

Stage 4: Context Assembly (NOW TRAIL-ORDERED)
  → Order notes in context window by trail plan
  → Primary BB first, secondary BB second, supporting last
  → Token budget allocation weighted by BB demand priority

Stage 5: Synthesis → Stage 6: Evaluation (with epistemic congruence from FZ 5g3a)
```

The key structural change: BB demand classification moves from controlling Stage 2 (routing) to informing Stages 3 and 4 (filtering and assembly).

## Testable Predictions

**P1**: BB-aware re-ranking (α=0.7 dense + 0.3 BB alignment) will improve Hit@5 by 1-3 percentage points over pure dense retrieval ranking for procedural and architectural questions — types where BB demand is unambiguous and topical similarity alone is insufficient.

**P2**: Trail-ordered context assembly will improve answer quality (measured by epistemic congruence + factual fidelity) for multi-block demand questions compared to relevance-ordered assembly. The improvement will be strongest for architectural questions (model → concept trail) because the LLM benefits from seeing the system structure before component definitions.

**P3**: BB demand coverage check (Application 3) will identify 5-10% of queries where dense retrieval's top-20 lacks a required BB type — triggering supplementary retrieval that recovers 2-4% of the 18.5% dense retrieval failure rate.

**P4**: The overhead of BB demand classification (rule-based lookup from question type → BB demand table) will be negligible (<5ms), making the total pipeline cost approximately equal to dense retrieval alone (58.7ms + 5ms ≈ 64ms).

## Connection to the Epistemic Congruence Framework

This sharpened position and FZ 5e2a's evaluation redirect are complementary:
- FZ 5e2a shows BB typing adds value at **evaluation time** (measuring answer quality)
- This note (FZ 5h1a) shows BB typing adds value at **assembly time** (constructing the answer)
- Together they establish that BB demand classification has a full post-retrieval lifecycle: classify → assemble → evaluate

The pre-retrieval routing step from FZ 5h is dead. But BB demand classification lives on as a post-retrieval intelligence layer.

---

## Related Notes

### Cross-Trail Convergence (Architecture Trail)
- **[FZ 7g1a1a1a1a1: ★ Synthesis — The Vault Is a CQRS Knowledge System](thought_synthesis_two_systems_cqrs_value_proposition.md)** — names this note's pattern as the **R-D rule**: System P artifacts (BB demand classification) belong at System D's stages 3–4 (re-rank, assembly), never at stage 1 (candidate generation). Same pattern recurs in FZ 5e2a, 5i1a, 5g3a — all converge on the CQRS architecture's stage-3/4 entry point for typed signals.

### Within Retrieval Trail (FZ 5)
- **[FZ 5h1: Counter — Uniform Retrieval Supersedes BB Pre-Routing](counter_uniform_retrieval_supersedes_bb_prerouting.md)** — the counter this note responds to
- **[FZ 5h: BB Demand as Pre-Retrieval Routing Step](thought_bb_demand_prerouting_for_retrieval.md)** — the original claim, now redirected
- **[FZ 5e2a: BB Value Redirected to Evaluation](thought_bb_structural_value_redirected_to_evaluation.md)** — sibling sharpened position for evaluation stage
- **[FZ 5g3a: Epistemic Congruence Metric](thought_epistemic_congruence_metric.md)** — the evaluation complement to this assembly-stage argument
- **[FZ 5g1a: BB Demand Inter-Annotator Agreement](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)** — κ=0.711 feasibility confirmation
- **[FZ 5e1: Retrieval Strategy Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md)** — v2 benchmark evidence
- **[FZ 5: Meta-Question — Value of Typed Knowledge](thought_meta_question_value_of_typed_knowledge.md)** — parent question
- **[Question Type Classification](../term_dictionary/term_question_type_classification.md)** — the 10-type taxonomy used as classification input
- **[Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)** — the 8-type taxonomy
