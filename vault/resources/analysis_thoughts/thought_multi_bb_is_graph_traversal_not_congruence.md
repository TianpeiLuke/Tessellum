---
tags:
  - resource
  - analysis
  - argument
  - epistemic_congruence
  - building_blocks
  - slipbot
keywords:
  - vector congruence
  - graph traversal
  - multi-BB demand
  - congruence revision
  - retrieval routing
  - scalar congruence
  - synthesis
topics:
  - retrieval evaluation
  - knowledge management
language: markdown
date of note: 2026-04-23
status: active
building_block: argument
folgezettel: "5l1a1b2"
folgezettel_parent: "5l1a1b"
author: lukexie
---

# ★ Synthesis: Multi-BB Demand Is a Graph Traversal Problem, Not a Congruence Problem (FZ 5l1a1b2)

## Thesis

[FZ 5l1a1b](counter_scalar_congruence_collapses_multi_bb_demand.md) proposed replacing scalar BB congruence with vector congruence to handle multi-BB questions. [FZ 5l1a1b1](analysis_multi_bb_demand_in_slipbot_questions.md) found 75% of questions are multi-BB. [FZ 5l1a1b1a](counter_multi_bb_demand_classification_inflated.md) challenged this through per-question human review, revising the rate to **30%** — and crucially, identified that all 6 confirmed multi-BB questions share a single pattern: **they require tracing typed edges across different note types** (intent→MDS, product→team, models→features→data source).

This synthesis sharpens the original request: **the problem is not that congruence scoring needs a vector — it's that 30% of questions require multi-hop graph traversal across BB-typed nodes, and the retrieval pipeline has no routing mechanism to detect and handle them.**

## The Dialectic

| Note | Claim | Status |
|---|---|---|
| **5l1a1b** | Scalar congruence is lossy; need vector demand/supply | **Partially accepted** — the observation is real but the solution is mislocated |
| **5l1a1b1** | 75% of questions are multi-BB | **Revised to 30%** — emp_obs inflation, hypothesis-as-nature, navigation-subsumes-concept |
| **5l1a1b1a** | Classification inflated; many secondary demands are embedded | **Accepted** — 5 deflation principles established by human review |

## What the Human Review Revealed

### Five Deflation Principles

1. **emp_obs is almost never an independent demand** — metrics and impact data are either embedded in concept/model notes or not actually requested. Users asking "What is X?" want the definition, not the launch metrics.

2. **"hypothesis" is a question nature, not a BB demand** — when a question is exploratory ("How can X help with Y?"), the demand is still concept/model/navigation. The hypothesis framing indicates the user needs DKS trail traversal, not a hypothesis-type note.

3. **Model → procedure dependency** — "Can X be done?" is a model question (capability confirmation), not a procedure question (how-to). Procedure demand only arises after model confirms the capability exists.

4. **Navigation subsumes concept for enumeration** — glossary and entry point notes contain concept summaries. "Explore X methods" is navigation, not navigation + concept.

5. **Well-written notes of type X naturally contain supporting content of type Y** — a concept note includes metrics, a procedure note includes architecture, a model note includes definitions. These are not independent retrieval demands.

### The 30% That ARE Multi-BB

| Q | Pattern | Graph Traversal Required |
|---|---|---|
| Q06 | concept → model → navigation | "3D models for abuse" → find models → find features → find data sources with 3D info |
| Q13 | concept → model → model | "RnR data source" → what is RnR? → what intent? → what upstream MDS/ETL? |
| Q14 | model → navigation | "Team for blurbs" → what product handles blurbs? → which team owns it? |
| Q18 | concept → model → navigation | "Pending actions" → define concept → find intents → list intents with pending actions |
| Q19 | model → model → model | "Routing to human queues" → intent → URES mechanism → queueing mechanism |
| Q20 | navigation → model → concept | "Models using CS chat" → list models → find features → identify CS chat (dialogue, not CAP) |

**Common pattern**: Every multi-BB question requires following a **chain of typed relationships** across the knowledge graph. The BB types in the chain are not independent demands to be measured by congruence — they are **hops in a retrieval path**.

## Revised Recommendation

### What to Keep from 5l1a1b

- **Store BB demand as the primary type** (scalar) — sufficient for 70% of questions
- **The congruence matrix M[i][j] is correct** — it measures whether the answer's BB type matches the question's primary demand
- **The $F \times E$ quality formula is correct** — factual fidelity × epistemic congruence captures the two independent failure modes

### What to Change

Instead of vector congruence, add a **retrieval routing classifier** that detects multi-hop questions and switches the retrieval strategy:

| Question Type | Detection Signal | Retrieval Strategy | Congruence |
|---|---|---|---|
| **Single-BB** (70%) | Single entity, definitional, "What is X?" | Standard: keyword → top-K notes | Scalar E (existing) |
| **Multi-BB graph traversal** (30%) | Dependency chain, "X behind Y", "which Z does W?", exploratory | Graph traversal: BFS/DFS across typed edges | **Path congruence**: did retrieval follow the correct edge types? |

### Path Congruence (New Metric for Multi-BB)

For graph traversal questions, congruence should measure whether the retrieval path followed the correct BB-typed edges, not whether the final answer matches a single demand type:

```
path_congruence = (correct_hops / total_hops_needed)
```

Where:
- `total_hops_needed` = number of typed edges in the ideal retrieval path (from human review)
- `correct_hops` = number of edges the answer actually traversed correctly

Example Q13: "Data source behind RnR intent"
- Ideal path: concept(RnR) → model(intent) → model(MDS/ETL) = 2 hops
- If answer found intent but not MDS: $C_{\text{path}} = \frac{1}{2} = 0.5$
- If answer found both: $C_{\text{path}} = \frac{2}{2} = 1.0$

### DB Schema Change (Minimal)

```sql
-- Add to existing schema (no vector columns needed)
bb_demand TEXT,              -- keep scalar (primary type)
demand_is_multi_hop BOOLEAN, -- NEW: flag for graph traversal questions
demand_hop_count INTEGER,    -- NEW: number of typed edges needed
path_congruence REAL,        -- NEW: correct_hops / total_hops (for multi-hop only)
```

3 new columns instead of the 2 JSON vector columns proposed in 5l1a1b. Simpler, more interpretable, and directly actionable for retrieval routing.

### Review Skill Change (Minimal)

In Step 3.5, after classifying BB demand, add:

```
Is this a multi-hop question requiring graph traversal across BB types?
If yes: identify the hop chain (e.g., concept→model→model) and count hops.
Set demand_is_multi_hop = true, demand_hop_count = N.
```

In Step 4.5, for multi-hop questions, compute path_congruence instead of (or alongside) scalar E.

## Connection to Existing Work

- **[FZ 5g: BB as Question Complexity Lens](thought_building_block_as_question_complexity_lens.md)** — confirmed: complexity $\propto$ hop count, not BB count. A 3-hop model→model→model question (Q19) is complex despite being single-BB-type.
- **[FZ 5e1: Retrieval Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md)** — the benchmark already tests graph traversal strategies (BFS, DFS, PPR). Multi-hop detection would route questions to these strategies.
- **[FZ 5k2d: Two-Axis Benchmark](thought_two_axis_multi_hop_benchmark_synthesis.md)** — the vertical axis (cross-BB ontology edges) directly measures what path congruence captures.

## Open Questions

- **OQ-S1**: Should path_congruence replace scalar E for multi-hop questions, or be stored alongside it? (Recommendation: alongside — scalar E still captures whether the final synthesis matches the primary demand.)
- **OQ-S2**: Can multi-hop detection be automated from question text, or does it require human classification? (The dependency chain signals — "behind", "which X does Y", exploratory framing — suggest partial automation is feasible.)
- **OQ-S3**: Does the 70/30 split hold for the full 532-question corpus, or is it biased by the first 20 questions? (Need to sample 50+ questions to validate.)

## Related Notes

### Cross-Trail Convergence (Architecture Trail)
- **[FZ 7g1a1a1a1a1: ★ Synthesis — The Vault Is a CQRS Knowledge System](thought_synthesis_two_systems_cqrs_value_proposition.md)** — cites this note as one of 13 Phase 3 syntheses that independently arrived at the same anti-conflation pattern: separating two problems that share vocabulary. This synthesis applied the same discipline to the QA review system that the architecture trail later applied to ontology vs retrieval.

### Within Phase 3 Trail
- **Parent**: [FZ 5l1a1b: Counter: Scalar Congruence Collapses Multi-BB Demand](counter_scalar_congruence_collapses_multi_bb_demand.md)
- **Sibling**: [FZ 5l1a1b1: Empirical: 75% Multi-BB](analysis_multi_bb_demand_in_slipbot_questions.md) — the data this synthesis reinterprets
- [FZ 5l1a1b1a: Counter: Classification Inflated](counter_multi_bb_demand_classification_inflated.md) — the human review that revised 75%→30%
- [FZ 5l1a1: Review v3.0 Implementation](thought_review_v3_trace_first_implementation.md) — the v3.0 design this extends
- [FZ 5g: BB as Question Complexity Lens](thought_building_block_as_question_complexity_lens.md) — complexity $\propto$ hop count
- [FZ 5k2d: Two-Axis Benchmark](thought_two_axis_multi_hop_benchmark_synthesis.md) — vertical axis = path congruence
- **Child**: [FZ 5l1a1b2a: Counter: Question Difficulty Hierarchy — Fourth Purpose](counter_question_difficulty_hierarchy_fourth_purpose.md) — multi-BB detection reveals L1-L4 difficulty hierarchy; difficult questions expose system limitations, not knowledge gaps
