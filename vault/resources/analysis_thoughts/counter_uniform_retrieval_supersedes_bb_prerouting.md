---
tags:
  - resource
  - analysis
  - retrieval
  - knowledge_management
  - building_blocks
  - information_retrieval
  - counter_argument
  - pre_retrieval
keywords:
  - BB demand routing refuted
  - pre-retrieval classification
  - uniform retrieval dominance
  - strategy routing unnecessary
  - dense retrieval
  - single-strategy dominance
  - routing overhead
  - BB demand classification
topics:
  - retrieval evaluation
  - knowledge building blocks
  - information retrieval
  - query understanding
language: markdown
date of note: 2026-04-21
status: active
building_block: counter_argument
folgezettel: "5h1"
folgezettel_parent: "5h"
author: lukexie
---

# Counter: Uniform Dense Retrieval Supersedes BB Demand Pre-Routing — Classification Without Actionable Routing (FZ 5h1)

## Target Claim

FZ 5h claims: *"Before executing any retrieval strategy, the answer-query pipeline should classify the building block demand of the incoming question — what type of knowledge the user seeks — and use this classification to select, parameterize, and prioritize retrieval strategies."*

This counter-argument shows that the v2 benchmark (4,823 Q × 14 strategies) **eliminates the routing target**: when one strategy dominates uniformly, there is nothing to route to.

## The Evidence

### E1: Dense Retrieval Achieves 0.77+ for ALL Question Types — No Type Needs a Different Strategy

FZ 5h's routing table maps question types to specialized strategies (definition → keyword search on `term_*`, procedural → metadata filter on `sop_*`, etc.). The v2 benchmark shows dense retrieval achieves:

| Question Type | dense_retrieval Hit@5 | FZ 5h's Routed Strategy | Routed Strategy Hit@5 |
|---|---|---|---|
| definition | 0.88 | keyword search on `term_*` | keyword_only: 0.82 |
| procedural | 0.87 | metadata filter on `sop_*` | metadata_only: 0.21 |
| enumeration | 0.93 | entry point browsing | entry_only: 0.03 |
| architectural | 0.89 | graph BFS from area/model seed | keyword_bfs: 0.48 |
| organizational | 0.94 | keyword on `team_*` | keyword_only: 0.74 |
| factual | 0.90 | keyword + date filter | keyword_only: 0.45 |
| temporal | 0.40 | date-range filter + keyword | keyword_only: 0.14 |
| relational | 0.87 | BFS/DFS from both seeds | keyword_bfs: 0.54 |
| multi_hop | 0.77 | DFS depth-4 | keyword_dfs: 0.43 |
| gold_faq | 0.98 | varies | keyword_only: 0.80 |

Dense retrieval outperforms every FZ 5h-routed strategy for every question type. The routing table is **strictly dominated**: even if the classification were perfect (100% accuracy), the routed strategies would underperform the uniform strategy.

### E2: BB Demand Classification Is Feasible But Has No Actionable Target

FZ 5h's pipeline depends on two premises:
1. **BB demand is classifiable** (FZ 5g1a: κ=0.711, 78% exact match) — **CONFIRMED**
2. **Different BB demands require different strategies** — **REFUTED**

The classification capability exists (κ=0.711 is substantial agreement), but the thing being classified into — strategy selection — has collapsed to a single option. This is like having an excellent compass in a room with only one door.

### E3: The Routing Overhead Is Negative Value

FZ 5h proposes inserting a "Stage 1.5: BB Demand Classification" between query expansion and retrieval. This adds:
- **Latency**: Classification step (LLM call or rule-based lookup) adds processing time
- **Error propagation**: ~22% of questions would be misclassified (1 - 0.78 accuracy), routing to a suboptimal strategy
- **Complexity**: Strategy parameterization logic, fallback cascades, trail plans

Meanwhile, dense retrieval at 58.7ms average latency is already a single-step strategy. Adding a routing layer on top of it would increase latency while potentially *degrading* recall if the router triggers fallback strategies that contaminate the dense retrieval results.

### E4: Predictions P1-P4 Are Refuted or Moot

| Prediction | FZ 5h Claim | v2 Result |
|---|---|---|
| P1: Routed > uniform for non-obvious BB alignment | Questions with hard alignment would benefit from routing | Dense retrieval achieves Hit@5 > 0.77 even for hardest types (multi_hop=0.77). No routing gap to exploit. |
| P2: Single-block questions complete faster | Fewer strategies needed for simple demands | Dense retrieval IS a single strategy (58.7ms). Speed advantage of routing is moot. |
| P3: Sequential trail execution improves Context Recall | model → concept → argument ordering helps multi-block | Untested but baseline is dense_retrieval Context Recall=0.786. Trail execution would need to exceed this, not the graph strategies it was designed to improve. |
| P4: No improvement for definition/procedural, improvement for architectural/relational | Current pipeline weak for cross-type questions | Architectural=0.89, relational=0.87 under dense_retrieval — no "strategy mismatch" gap exists. |

## Why the Original Claim Was Wrong

FZ 5h made a valid inference from two correct premises: (1) BB demand is classifiable, and (2) different building blocks showed different performance profiles across graph strategies (from FZ 5e's v1 analysis). The error was assuming that the **strategy differentiation observed among graph strategies** would persist when stronger baselines were introduced.

The routing algorithm is well-designed for a world where graph strategies are the only option. In a world with dense retrieval, the routing algorithm solves a problem that no longer exists — there is only one strategy to "select."

## What Survives

1. **BB demand classification itself (κ=0.711)** remains valid and potentially valuable — but for different applications than strategy routing. See FZ 5h1a.

2. **The question type → BB demand lookup table** remains a valid descriptive mapping of what knowledge different question types seek. This has pedagogical and evaluation value even without routing implications.

3. **The multi-block trail concept** (ordered retrieval across building block types) is the most promising survivor — it addresses context assembly, not initial retrieval. Whether sequential trail execution (model → concept → argument) can exceed dense retrieval's Context Recall of 0.786 remains an open empirical question.

4. **The fallback architecture** ("pre-routing step must never reduce recall") is good defensive design — applicable to any future routing system if one becomes needed.

## Scope and Limitations

This counter addresses FZ 5h's **strategy routing claim**, not its classification methodology or its descriptive taxonomy. The counter also does not rule out that BB demand classification could be useful for **re-ranking** dense retrieval results or **context assembly** (ordering retrieved notes by BB demand match). See FZ 5h1a for this redirected application.

---

## Related Notes

### Cross-Trail Use as Evidence (Architecture Trail)
- **[FZ 7g1a1a1a: FZ 5 Evidence Confirms Three-Layer + Sharpens Within-BB Recipe](thought_fz5_evidence_confirms_three_layer_and_sharpens_within_bb_recipe.md)** — cites this note as **Confirmation 2** that Layer 1 (Ontology) and Layer 2 (Retrieval) must remain non-coupled at the query path; the routing-target collapse documented here is what makes the layer boundary architecturally strict, not just a recommendation.
- **[FZ 7g1a1a1a1: ★ Synthesis — One Vault, Three Invariance Regimes](thought_synthesis_three_invariance_regimes_one_vault.md)** — uses this note's κ=0.711 + collapse finding to ground design rule R2 ("edge labels in Layer 2 do not exist; the retriever sees an unlabeled link graph").
- **[FZ 7g1a1a1a1a1: ★ Synthesis — The Vault Is a CQRS Knowledge System](thought_synthesis_two_systems_cqrs_value_proposition.md)** — promotes this note's evidence to architectural rule **R-Cross**: the query path may not cross the System P → System D boundary. The pre-routing collapse is the empirical signature of CQRS being right.

### Within Retrieval Trail (FZ 5)
- **[FZ 5h: BB Demand as Pre-Retrieval Routing Step](thought_bb_demand_prerouting_for_retrieval.md)** — target of this counter-argument
- **[FZ 5h1a: BB Demand Redirected to Re-Ranking and Context Assembly](thought_bb_demand_redirected_to_reranking.md)** — sharpened position: BB demand survives for post-retrieval
- **[FZ 5e: Question Type × Building Block Alignment](thought_question_type_building_block_retrieval_alignment.md)** — parent claim that FZ 5h operationalizes
- **[FZ 5e2: Counter — Dense Retrieval Refutes BB Strategy Routing](counter_dense_retrieval_refutes_bb_strategy_routing.md)** — sibling counter addressing FZ 5e
- **[FZ 5e1: Retrieval Strategy Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md)** — v2 benchmark providing the evidence
- **[FZ 5g1a: BB Demand Inter-Annotator Agreement](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)** — κ=0.711 classification feasibility
- **[FZ 5g3a: Epistemic Congruence Metric](thought_epistemic_congruence_metric.md)** — the evaluation-stage application of BB demand
- **[FZ 5: Meta-Question — Value of Typed Knowledge](thought_meta_question_value_of_typed_knowledge.md)** — parent question
