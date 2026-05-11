---
tags:
  - resource
  - analysis
  - retrieval
  - benchmark_design
  - ontology
  - building_blocks
  - multi_hop
  - knowledge_management
keywords:
  - ontology-grounded multi-hop
  - building block ontology
  - epistemic reasoning cycle
  - edge recall
  - ontology edge traversal
  - dialectic chain
  - DKS benchmark
  - multi-note gold sets
  - graph retrieval evaluation
  - epistemic ordering
  - Abuse Slipbox
topics:
  - retrieval evaluation
  - information retrieval
  - benchmark design
  - knowledge management
  - epistemology
language: markdown
date of note: 2026-04-21
status: active
building_block: hypothesis
folgezettel: "5k2"
folgezettel_parent: "5k"
author: lukexie
---

# Hypothesis: Ontology-Grounded Multi-Hop QA Benchmark — Epistemic Edges Define What "Multi-Hop" Means (FZ 5k2)

## The Hypothesis

> The planned multi-note exploration benchmark ([FZ 5k1](../../archives/experiments/experiment_multi_note_exploration_benchmark.md)) defines "multi-hop" as **graph-topological** — notes within 2 hops of each other in the link graph. This is necessary but insufficient: two concept notes 1 hop apart are not a genuine multi-hop question — they are single-type retrieval with two gold notes. A genuine multi-hop question requires traversing one or more **ontology edges** from the [Building Block Ontology](thought_building_block_ontology_relationships.md) (FZ 7g), where each edge represents a distinct epistemic operation (naming, structuring, predicting, testing, challenging). The ontology's directed cycle — Observation →(naming)→ Concept →(structuring)→ Model →(predicting)→ Hypothesis →(testing)→ Argument →(challenging)→ Counter-Argument →(motivates)→ new Observation — provides a theory-grounded definition of multi-hop that the current benchmark lacks. A retrieval system that can recover full ontology paths supports [DKS](../../projects/athelas_conv/athelas_conv_dialectic_knowledge_system.md)-style reasoning; one that finds individual notes by semantic similarity cannot.

## Motivation

### The Problem with Graph-Topological Multi-Hop

FZ 5k1 samples connected subgraphs via BFS and generates questions requiring information from all notes in the subgraph. The sampling algorithm maximizes subcategory diversity and building block diversity, but the diversity constraints are **filters**, not **structural requirements**. A gold set of {concept, model, procedure} that happens to be within 2 hops satisfies the filter, but the question may not require understanding the *epistemic transition* between them — it may just require three independent facts.

The v2 benchmark's circularity ([FZ 5e1d2](analysis_benchmark_circularity_graph_sampled_questions.md)) showed that 86.6% single-note gold sets structurally disadvantage graph strategies. FZ 5k1 addresses this by requiring multi-note gold sets. But multi-note is necessary, not sufficient — the gold set must also require **crossing epistemic boundaries** to answer.

### The Ontology Provides the Missing Structure

The [FZ 7g Building Block Ontology](thought_building_block_ontology_relationships.md) defines 10 directed edges forming an epistemic reasoning cycle:

```
Observation →(naming)→ Concept →(structuring)→ Model
                                                  ↓
                                             (predicting)  (codifying)
                                                  ↓              ↓
                                             Hypothesis     Procedure
                                                  ↓              ↓
                                             (testing)    (execution)
                                                  ↓              ↓
                                              Argument ←─────────┘
                                                  ↓         (new data)
                                             (challenging)
                                                  ↓
                                           Counter-Argument
                                                  ↓
                                             (motivates)
                                                  ↓
                                          New Observation ──→ ...
```

Each edge represents a **qualitatively different epistemic operation**. Crossing an edge in a question means the answer requires a different *type* of reasoning at each hop — not just finding more notes of the same kind.

### Connection to DKS

The [Dialectic Knowledge System](../../projects/athelas_conv/athelas_conv_dialectic_knowledge_system.md) (FZ 8c5c1a) formalizes the ontology cycle as a production system. Each DKS component maps to an ontology edge:

| DKS Component | Ontology Edge | Benchmark Question Type |
|---|---|---|
| Observation source | — (input) | Naming |
| Argument generator A | Model → Hypothesis → Argument | Predicting + Testing |
| Argument generator B | Independent evidence | Structuring |
| Disagreement detection | Argument → Counter-Argument | Challenging |
| Counter-argument capture | Counter → new Observation | Dialectic chain |
| Pattern discovery | Observation → Concept → Model | Full cycle |
| Rule improvement | Full cycle completion | Full cycle |

**The benchmark tests whether retrieval can recover DKS reasoning chains from the vault.** If retrieval finds the full ontology path, it can support DKS-style reasoning. If it finds only individual notes by semantic similarity, it cannot.

## Benchmark Design

### 1. Question Taxonomy: 7 Ontology-Edge Question Types

Each question type maps to one or more ontology edges. The edge(s) define what "multi-hop" means for that question:

| Question Type | Ontology Edge(s) | Hops | Example Pattern | Gold Set |
|---|---|---|---|---|
| **Naming** | Obs → Concept | 1 | "What concept was defined from [observation X]?" | observation + concept |
| **Structuring** | Concept → Model | 1 | "What model organizes [concept X] and [concept Y]?" | 2 concepts + model |
| **Predicting** | Model → Hypothesis | 1 | "What predictions does [model X] generate?" | model + hypothesis |
| **Testing** | Hypothesis → Argument | 1 | "What evidence supports or refutes [hypothesis X]?" | hypothesis + argument |
| **Challenging** | Argument → Counter-Argument | 1 | "What are the weaknesses of [argument X]?" | argument + counter-argument |
| **Full Cycle** | Obs → Con → Mod → Hyp → Arg | 4 | "How did observation [X] lead to argument [Y]?" | 5 notes spanning the full cycle |
| **Dialectic Chain** | Arg → Counter → new Obs → Con | 3 | "How did the challenge to [argument X] produce new understanding?" | 4 notes: argument, counter, observation, concept |

### 2. Gold Set Sampling: Ontology-Constrained Subgraph Selection

Instead of random BFS subgraphs (FZ 5k1), sample gold sets by **following ontology edges in the vault's actual link graph**:

```
For each question:
  1. Select a seed note with building_block = source_type for the target edge
  2. Follow outlinks to find a note with building_block = target_type for that edge
  3. Verify the link is semantically meaningful (not just a "Related Notes" backlink)
     — check that the link appears in the note body, not only in a trailing list
  4. For multi-edge questions, chain: find A→B→C where each transition
     crosses a different ontology edge
  5. Pass the chain to LLM with prompt:
     "Given these [N] notes connected by epistemic relationships
      [edge_1, edge_2, ...], generate ONE natural question that requires
      understanding how each note leads to the next through the specified
      reasoning operation. The question should sound like something a
      researcher would actually ask."
  6. Record: question, gold_chain (ordered), edge_types traversed,
     building_block_sequence
```

**Key constraint**: The gold chain must traverse **distinct ontology edges**, not just distinct notes. A chain of 3 concept notes is NOT a 3-hop question — it is single-type retrieval. A chain of concept → model → hypothesis IS a 2-hop question because it crosses 2 ontology edges (structuring + predicting).

### 3. Metrics: Ontology-Aware Evaluation

Extend FZ 5k1's metrics with ontology-specific measures:

| Metric | Definition | What It Measures |
|---|---|---|
| **Edge Recall@K** | Fraction of gold ontology edges whose both endpoints are in top-K | Did retrieval find the *transitions*, not just the notes? |
| **Ontology Path Completeness@K** | 1 if the full gold chain (all notes) is recoverable from top-K, else 0 | Can the answer be assembled from retrieved notes? |
| **Epistemic Ordering Score** | Kendall's τ between gold chain order and retrieval rank order | Does retrieval preserve the reasoning direction? |
| **BB Diversity@K** | Number of distinct building blocks in top-K ∩ gold set | Epistemic diversity of retrieval |
| Gold Recall@K | (from 5k1) Fraction of all gold notes found in top-K | Basic multi-note coverage |
| Subcategory Coverage@K | (from 5k1) Distinct subcategories in top-K | Cross-domain reach |

**Edge Recall@K** is the key new metric. It measures whether retrieval found *pairs of notes connected by an ontology edge* — not just individual notes. A retrieval that finds the hypothesis and the counter-argument but misses the argument in between scores 0 on the Testing edge even though it found 2/3 gold notes.

### 4. Hypothesis Tests

| ID | Hypothesis | Metric | Expected |
|---|---|---|---|
| **H1** | Graph strategies outperform dense_retrieval on Edge Recall@K | Edge Recall@10 | keyword_bfs > dense_retrieval |
| **H2** | Dense retrieval still dominates Gold Recall@K for 1-edge questions | Gold Recall@5 | dense_retrieval > all graph |
| **H3** | Strategy ranking inverts between 1-edge and 4-edge (full cycle) questions | Rank correlation | Spearman ρ < 0.7 |
| **H4** | Epistemic Ordering Score is near-zero for dense retrieval | Ordering Score | dense ≈ 0, DFS > 0.3 |
| **H5** | DFS outperforms BFS on dialectic chain questions | Edge Recall@10 | keyword_dfs > keyword_bfs |
| **H6** | Hybrid (dense + graph re-ranking) achieves best Edge Recall@K | Edge Recall@10 | dense_plus_graph > all single strategies |

H2 serves as a control: if dense_retrieval dominates even Edge Recall on 1-edge questions, the ontology-grounding adds no value over FZ 5k1's approach.

### 5. Scale and Distribution

| Parameter | Value | Rationale |
|---|---|---|
| Total questions | 500 | Statistical power for per-edge-type analysis |
| 1-edge questions | 250 (50 per edge type × 5 types) | Tests each ontology edge independently |
| Multi-edge questions | 150 (full cycle: 75, dialectic chain: 75) | Tests reasoning chain discovery |
| FZ trail questions | 100 | Tests Folgezettel-specific retrieval ([FZ 5f](thought_folgezettel_trails_as_retrieval_modality.md)) |
| Min gold set size | 2 notes (1-edge) to 5 notes (full cycle) | Matches ontology edge count |
| BB diversity | ≥2 distinct building blocks per gold set | Guaranteed by ontology edge constraint |

### 6. Strategies to Evaluate

Run all 14 v2 strategies plus 3 exploration-oriented strategies:

| Strategy | Type | Rationale |
|---|---|---|
| All 14 from v2 | Baseline | Comparability with [FZ 5e1](../../archives/experiments/experiment_retrieval_strategy_benchmark.md) |
| **dense_plus_bfs** | Hybrid | Dense top-5 + BFS expansion; tests exploitation → exploration pipeline |
| **dense_plus_graph_rerank** | Hybrid | Dense top-50 + graph re-ranking ([FZ 5e1c1c](thought_hybrid_retrieval_dense_plus_graph.md)); tests ontology-aware re-ranking |
| **ontology_walk** | New | Seed from dense top-1, then follow ontology-typed edges (only traverse links where source and target have the expected building block types); tests pure ontology traversal |

The **ontology_walk** strategy is unique to this benchmark — it uses the building block ontology as a traversal filter, only following links that cross an ontology edge. This directly tests whether the ontology structure provides retrieval value.

## Predictions

- **P1**: For full-cycle questions (4 ontology edges), graph strategies will achieve Edge Recall@10 > 0.4 while dense_retrieval achieves < 0.2, because dense retrieval finds semantically similar notes regardless of edge structure.
- **P2**: For 1-edge questions, dense_retrieval will still dominate Gold Recall@5 (> 0.7), confirming that ontology-grounding matters only for multi-edge questions.
- **P3**: The ontology_walk strategy will achieve the highest Epistemic Ordering Score because it traverses edges in ontology order by construction.
- **P4**: Hybrid (dense + graph re-ranking) will achieve the best overall Edge Recall@K by combining dense retrieval's note-finding ability with graph re-ranking's edge-structure preservation.

## Open Questions

- **OQ-OG1**: Can ontology edges be reliably detected from vault links? Not all links between a concept note and a model note represent a "structuring" edge — some are incidental cross-references. What heuristics distinguish ontology-meaningful links from incidental ones?
- **OQ-OG2**: Is the ontology cycle the only valid multi-hop structure, or do cross-cycle paths (e.g., Procedure → Model, skipping the Observation feedback) also constitute genuine multi-hop?
- **OQ-OG3**: How should the benchmark handle notes with ambiguous building block assignments? The inter-annotator agreement for building blocks is κ=0.711 ([FZ 5g1a](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)) — substantial but not perfect. Empirical_observation has only 53% agreement.
- **OQ-OG4**: Does the ontology_walk strategy generalize beyond this vault, or is it specific to vaults with building block metadata?

## How This Addresses Known Problems

| Problem | Source | How This Benchmark Addresses It |
|---|---|---|
| 86.6% single-note gold sets | [FZ 5e1d2](analysis_benchmark_circularity_graph_sampled_questions.md) | Every gold set is multi-note by construction (ontology edge requires ≥2 notes of different BB types) |
| Graph strategies Pareto-dominated | [FZ 5e1](../../archives/experiments/experiment_retrieval_strategy_benchmark.md) | Edge Recall@K rewards structural retrieval that dense retrieval cannot provide |
| Hub dilution | [FZ 5j](thought_hub_dilution_bridges_topology_and_retrieval.md) | Ontology_walk filters BFS by BB type, reducing candidate explosion |
| Exploration vs exploitation conflation | [FZ 5k](thought_exploration_vs_exploitation_retrieval.md) | Ontology edges define exploration as epistemic traversal, not random neighborhood discovery |
| BB routing adds zero value | [FZ 5e2](counter_dense_retrieval_refutes_bb_strategy_routing.md) | BB types are used for gold set construction and evaluation, not strategy routing |

---

## Related Notes

### Folgezettel Trail
- **Parent [FZ 5k]**: [Exploration vs Exploitation Hypothesis](thought_exploration_vs_exploitation_retrieval.md) — this note refines "exploration" from cross-subcategory diversity to ontology-edge traversal
- **Sibling [FZ 5k1]**: [Multi-Note Exploration Benchmark](../../archives/experiments/experiment_multi_note_exploration_benchmark.md) — graph-topological multi-hop benchmark that this note extends with ontology grounding
- **Child [FZ 5k2a]**: [Empirical Trail Analysis](analysis_empirical_ontology_trails_in_vault.md) — validates this design by sampling real cross-BB trails from the vault; revises question distribution based on user-relevance review
- **Child [FZ 5k2b]**: [Real SlipBot Questions Validate Multi-Hop](thought_real_slipbot_questions_validate_multi_hop.md) — classifies 50 real SlipBot questions: 38% multi-hop, 7 ghost notes; validates that real users ask multi-hop questions matching 5k2a patterns
- **Child [FZ 5k2c]**: [Counter: Ontology Violations](counter_ontology_violations_in_real_multi_hop.md) — 74% of real multi-hop trails violate the ontology; same-type (model→model) dominates; recommends vertical + horizontal multi-hop split
- **Child [FZ 5k2d]**: [★ Synthesis: Two-Axis Multi-Hop Benchmark](thought_two_axis_multi_hop_benchmark_synthesis.md) — sharpened design synthesizing 5k2–5k2c into vertical (Edge Recall) × horizontal (Domain Recall) benchmark

### Ontology Foundation
- **[FZ 7g: Building Block Ontology](thought_building_block_ontology_relationships.md)** — the 8 types + 10 directed edges that define the epistemic reasoning cycle; the ontology diagram (`Building_Blocks_Mental_model_mermaid.png`) is the structural foundation of this benchmark
- **[FZ 7f1: 7-Phase Edge-Guided Reasoning](thought_thinking_protocol_building_block_expansion.md)** — the reasoning protocol that follows ontology edges; this benchmark tests whether retrieval can recover those edges

### DKS Connection
- **[FZ 8c5c1a: DKS Design](../../projects/athelas_conv/athelas_conv_dialectic_knowledge_system.md)** — the 7-component DKS pattern whose reasoning chains this benchmark evaluates
- **[FZ 8c5c1a4: DKS Formal Model](../../projects/athelas_conv/athelas_conv_dks_formal_model.md)** — MDP formalization; the ontology cycle is the state transition structure

### Benchmark Context
- **[FZ 5e1: Retrieval Strategy Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md)** — v2 baseline (4,823 Q × 14 strategies, dense_retrieval Hit@5=0.815)
- **[FZ 5e1d2: Benchmark Circularity](analysis_benchmark_circularity_graph_sampled_questions.md)** — the gold set design problem this benchmark addresses
- **[FZ 5e1c1c: Hybrid Retrieval](thought_hybrid_retrieval_dense_plus_graph.md)** — the dense + graph re-ranking architecture tested as a strategy here

### Validation
- **[FZ 5g1a: BB Inter-Annotator Agreement](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)** — κ=0.711 for BB classification; relevant to OQ-OG3
- **[FZ 5e1: Experiment Trail](../../0_entry_points/entry_retrieval_experiment_trail.md)** — entry point for all retrieval experiments
