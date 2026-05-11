---
tags:
  - resource
  - analysis
  - retrieval
  - sqlite
  - rag
  - knowledge_management
  - information_retrieval
  - hybrid_retrieval
  - re_ranking
  - context_assembly
keywords:
  - hybrid retrieval
  - dense plus graph
  - graph re-ranking
  - BB-aware context assembly
  - post-retrieval graph processing
  - embedding plus structure
  - two-stage retrieval
  - re-ranking by graph distance
  - building block aware assembly
  - Abuse Slipbox
topics:
  - information retrieval
  - knowledge management
  - hybrid architecture
language: markdown
date of note: 2026-04-21
status: active
building_block: hypothesis
folgezettel: "5e1c1c"
folgezettel_parent: "5e1c1"
author: lukexie
---

# Hypothesis: Hybrid Retrieval (Dense + Graph Post-Processing) Can Outperform Dense Retrieval Alone (FZ 5e1c1c)

## The Hypothesis

> Dense retrieval (Hit@5=0.815) finds the most semantically relevant notes, but returns them as a flat ranked list with no structural context. Graph post-processing can **re-rank** this list using structural signals (graph distance, link context, building block type) and **assemble** the context using graph-encoded relationships (reasoning chains, BB-diverse neighborhoods, FZ-ordered sequences). The hypothesis is that the combination — dense retrieval for candidate generation + graph post-processing for re-ranking and assembly — outperforms dense retrieval alone on answer quality, even though it may not improve Hit@5. The value is not in *finding different notes* but in *organizing the found notes into better context*.

## Motivation

### The Architecture Insight from FZ 5e1c1

The parent note (FZ 5e1c1) observes that the vault's 5-stage retrieval pipeline uses embeddings only in stage 2 (candidate retrieval). Stages 3–5 (working memory scoring, context assembly, synthesis) are purely structural:

| Stage | Operation | Uses Embeddings? | Uses Graph? |
|-------|-----------|-------------------|-------------|
| 1. Query expansion | Resolve terms, expand synonyms | No | Yes (term subgraph) |
| 2. Candidate retrieval | Find top-K notes | **Yes** (dense) | Optional (BFS/PPR) |
| 3. Working memory | Score and re-rank candidates | No | **Yes** (graph distance, link context) |
| 4. Context assembly | Build token-budgeted context | No | **Yes** (BB type, FZ ordering, link chains) |
| 5. Synthesis | Generate answer | No | No (LLM) |

**The insight**: Dense retrieval's Hit@5=0.815 advantage is concentrated in stage 2. But answer quality depends on all 5 stages. Graph post-processing in stages 3–4 can improve answer quality without changing which notes are retrieved — by changing how they are **organized and presented** to the LLM in stage 5.

### Why Dense Retrieval Alone Is Insufficient

Dense retrieval returns a flat ranked list: [note_1, note_2, ..., note_K] sorted by cosine similarity. This list has three deficiencies for context assembly:

1. **No structural ordering**: Semantically similar notes cluster together. If the top-5 are all concept notes about DNR, the context is redundant. A diverse context (concept + procedure + model) would produce a richer answer.

2. **No reasoning chains**: The flat list doesn't encode that note_2 links to note_4 via note_3. The LLM receives disconnected fragments instead of a connected reasoning path.

3. **No priority by question type**: A procedural question receives the same ranked list as a conceptual question. BB-aware assembly would front-load procedures for "how to" questions and concepts for "what is" questions.

## The Hybrid Architecture

### Stage 2: Dense Retrieval (unchanged)

Use the existing `dense_retrieval` strategy (sentence-transformers/all-MiniLM-L6-v2) to retrieve top-K candidates by cosine similarity. K=50 (larger pool for post-processing to work with).

### Stage 3: Graph Re-Ranking

Re-rank the top-50 candidates using a blended score:

```
hybrid_score = α × embedding_sim + β × graph_proximity + γ × bb_alignment + δ × link_context_match

Where:
  α = 0.50 (embedding similarity — dominant signal)
  β = 0.20 (graph proximity to seed notes)
  γ = 0.15 (building block alignment with question demand)
  δ = 0.15 (link context relevance to query terms)
```

#### Graph Proximity Score

For each candidate note, compute the shortest graph distance to the query's seed notes (resolved terms from stage 1):

```sql
-- Shortest path between candidate and seed via note_links
-- Approximated by BFS depth (1-hop = 1.0, 2-hop = 0.5, 3-hop = 0.25, no path = 0.0)
```

**Why this helps**: Two notes with identical embedding similarity may differ in graph distance. The one closer to the seed term is more likely to be contextually relevant — it was authored in the same reasoning neighborhood.

#### BB Alignment Score

Classify the question's building block demand (using the κ=0.711 classifier from FZ 5g1a), then score each candidate by BB match:

| BB Demand | Candidate BB | Score |
|-----------|-------------|-------|
| Exact match | procedure → procedure | 1.0 |
| Related type | procedure → how_to | 0.7 |
| Compatible | procedure → model | 0.3 |
| Mismatch | procedure → concept | 0.1 |

The alignment matrix from FZ 5g3a (epistemic congruence) provides the scoring basis.

#### Link Context Match

For candidates that are direct neighbors of seed notes, extract the `link_context` field from `note_links`:

```sql
SELECT link_context FROM note_links
WHERE source_note_id = '<seed>' AND target_note_id = '<candidate>'
```

Score by keyword overlap between `link_context` and the query. This captures *why* the author linked these notes — a signal invisible to embeddings.

### Stage 4: BB-Aware Context Assembly

After re-ranking, assemble the context for the LLM using building block type to determine ordering:

#### Assembly Strategy by Question Intent

| Question Intent | Assembly Order | Rationale |
|----------------|---------------|-----------|
| Definition ("what is X?") | concept → model → related terms | Definition first, then architecture, then connections |
| Procedural ("how to X?") | procedure → concept → model | Steps first, then background, then architecture |
| Causal ("why does X?") | argument → evidence → counter | Thesis first, then support, then alternative views |
| Comparative ("X vs Y?") | concept_X → concept_Y → argument | Side by side, then evaluation |
| Exploratory ("tell me about X") | entry_point → concept → diverse BBs | Overview first, then depth, then breadth |
| Trail ("how did X evolve?") | FZ-ordered sequence | Authored reasoning order (FZ 5f) |

#### Token Budget Allocation

Within the total token budget (default 8,000), allocate by tier:

```
Tier 1 — Primary sources (BB-matched, graph-proximate): 50% of budget
  → Full note content for top 2-3 re-ranked candidates
Tier 2 — Supporting sources (BB-compatible, 1-2 hop): 30% of budget
  → Key sections from next 3-5 candidates
Tier 3 — Context notes (grounded terms, link context): 20% of budget
  → Definitions and relationship descriptions
```

**Key difference from flat dense retrieval**: Flat assembly allocates by similarity rank (most similar gets most tokens). BB-aware assembly allocates by **epistemic role** (the procedure gets full context even if a concept ranked higher by similarity).

## Evidence Supporting the Hypothesis

### From the Existing Pipeline

The 5-stage pipeline already implements a primitive version of this hybrid architecture:

1. Stage 1 uses SQLite metadata for query expansion (structural signal)
2. Stage 2 currently uses keyword search (but can be swapped to dense)
3. Stage 3 uses graph distance and PageRank for working memory scoring
4. Stage 4 uses BB type for context ordering

The hypothesis proposes upgrading stage 2 to dense retrieval while keeping stages 3-4's structural processing. This is not a new architecture — it is the existing architecture with a better retrieval engine.

### From Related Work

The v2 benchmark data supports the components:

- **Dense retrieval works**: Hit@5=0.815 (FZ 5e1)
- **BB classification works**: κ=0.711 inter-annotator agreement (FZ 5g1a)
- **Graph distance is computable**: BFS/PPR complete in <100ms (FZ 5e1c1)
- **BB demand predicts answer quality**: multi-block concept-primary questions score 4.60 vs 3.40 single-block (FZ 5g1b)
- **Post-retrieval is where structure helps**: stages 3-5 are purely structural (FZ 5e1c1)

### From the Counter-Evidence

FZ 5e2 shows dense retrieval uniformly dominates — but on Hit@5, not answer quality. FZ 5g1c shows vault coverage doesn't predict rating — but the rating instrument lacks a BB lens (FZ 5g3). The existing metrics may not capture the value that hybrid assembly adds.

## Predictions

- **P1**: Hybrid retrieval (dense + graph re-ranking) will match or exceed dense_retrieval on Hit@5 (it uses the same candidates, just re-ordered) and outperform on multi-note retrieval metrics (Gold Recall@K, Graph Coherence@K from FZ 5k1) by 5-10%.
- **P2**: BB-aware context assembly will improve LLM answer quality (measured by a BB-lens-equipped reviewer from FZ 5g3a) by 0.5-1.0 points on a 5-point scale, compared to similarity-ordered flat assembly.
- **P3**: The graph proximity component (β=0.20) will provide the largest re-ranking lift on multi_hop questions, where bridge notes are structurally close but semantically distant.
- **P4**: The BB alignment component (γ=0.15) will provide the largest assembly lift on procedural questions, where the distinction between concept and procedure notes most affects answer usefulness.
- **P5**: The overall hybrid system will show diminishing returns as embedding quality improves — better embeddings may implicitly capture some structural signals, narrowing the graph post-processing advantage.

## Design for FZ 5e1c Benchmark

The hybrid architecture creates a new benchmark condition for the SQLite vs RAG experiment (FZ 5e1c):

| Condition | Stage 2 | Stage 3-4 | Expected Hit@5 | Expected Answer Quality |
|-----------|---------|-----------|-----------------|------------------------|
| SQLite-only | keyword + BFS | graph + BB | 0.53 | Medium (structural assembly but poor recall) |
| Dense-only | embeddings | flat ranking | 0.82 | Medium-High (good recall but unstructured assembly) |
| **Hybrid** | **embeddings** | **graph + BB** | **0.82+** | **High (good recall + structured assembly)** |

The benchmark must measure **answer quality** (not just Hit@5) to detect the hybrid advantage. The BB-lens-equipped reviewer from FZ 5g3a provides the instrument.

## Open Questions

- **OQ-HR1**: What are the optimal blending weights (α, β, γ, δ)? Should they be fixed or adaptive per question type?
- **OQ-HR2**: Does graph re-ranking ever *hurt* — demoting a correct note that is semantically close but graph-distant (e.g., a newly added note with few links)?
- **OQ-HR3**: How does the hybrid approach compare to end-to-end learned retrieval (fine-tuned bi-encoder on the vault's query-note pairs)? The hybrid is modular; the fine-tuned model is monolithic.
- **OQ-HR4**: At what vault scale does the graph post-processing latency (<100ms at 9,108 notes) become a bottleneck? At 100K notes, BFS from a seed may produce tens of thousands of candidates.
- **OQ-HR5**: Can the BB alignment score replace the epistemic congruence metric (FZ 5g3a) at the retrieval stage, making it unnecessary at the review stage? Or are they measuring different constructs?

---

## Related Notes

### Cross-Trail Operational Use (Architecture Trail)
- **[FZ 7g1a1a1a: FZ 5 Evidence Confirms Three-Layer + Sharpens Within-BB Recipe](thought_fz5_evidence_confirms_three_layer_and_sharpens_within_bb_recipe.md)** — operationalizes this hypothesis as the **within-BB retrieval recipe v2** for the architecture trail's Layer 2. The α/β/γ/δ blending recipe described here (dense + graph_proximity + BB_alignment + link_context) is adopted directly as the re-rank stage; the BB-aware context assembly stages 4 are adopted for the assembly stage. The PPR-primary recipe of [FZ 7g1a1a](thought_within_bb_navigation_is_retrieval_not_ontology.md) v1 is replaced with this dense-primary hybrid.
- **[FZ 7g1a1a1a1: ★ Synthesis — One Vault, Three Invariance Regimes](thought_synthesis_three_invariance_regimes_one_vault.md)** — this note's stage decomposition (candidate generation → re-rank → context assembly) becomes the **internal architecture of Layer 2** in the three-regime model.

### Within Retrieval Trail (FZ 5)
- **[FZ 5e1c1: SQLite as Non-RAG Indexing Baseline](thought_sqlite_non_rag_indexing_baseline.md)**: parent note — poses the question "can hybrid retrieval outperform dense alone?" that this note answers with a concrete architecture
- **[FZ 5e1c1a: SQLite vs RAG Operational Tradeoffs](analysis_sqlite_vs_rag_operational_tradeoffs.md)**: sibling — operational cost perspective; the hybrid architecture adds graph post-processing cost (<100ms) to dense retrieval cost
- **[FZ 5e1c1b: Structural Retrieval Value Beyond Embeddings](thought_structural_retrieval_value_beyond_embeddings.md)**: sibling — identifies the three structural signals (path, ordering, BB type) that this hybrid architecture exploits
- **[FZ 5h1a: BB Demand for Re-Ranking + Context Assembly](thought_bb_demand_redirected_to_reranking.md)**: the key predecessor — redirected BB demand from pre-routing (refuted) to post-retrieval re-ranking (this note's stage 3-4)
- **[FZ 5i1a: Term Hub Value for Re-Ranking](thought_term_hub_value_for_reranking_context.md)**: term-hub diversity for context assembly — directly applicable to the hybrid architecture's stage 4
- **[FZ 5g3a: Epistemic Congruence Metric](thought_epistemic_congruence_metric.md)**: the BB alignment scoring matrix used in stage 3's γ component
- **[FZ 5g1a: BB Demand Inter-Annotator Agreement](../../archives/experiments/experiment_bb_demand_interannotator_agreement.md)**: κ=0.711 — the reliability basis for BB demand classification in stage 3
- **[FZ 5f: Folgezettel Trails as Retrieval Modality](thought_folgezettel_trails_as_retrieval_modality.md)**: FZ-ordered assembly in stage 4's trail question type
- **[FZ 5e1c: SQLite vs RAG Benchmark](../../archives/experiments/experiment_sqlite_vs_rag_benchmark.md)**: grandparent experiment — hybrid is a third condition (alongside SQLite-only and dense-only)
- **[FZ 5k1: Multi-Note Exploration Benchmark](../../archives/experiments/experiment_multi_note_exploration_benchmark.md)**: the benchmark that would test P1 (multi-note retrieval metrics)
- **[FZ 5j: Hub Dilution](thought_hub_dilution_bridges_topology_and_retrieval.md)**: the graph proximity score (β) must account for hub dilution — distance through hubs is less meaningful
- **[FZ 5e2: Counter — Dense Retrieval Refutes BB Routing](counter_dense_retrieval_refutes_bb_strategy_routing.md)**: the counter — hybrid must demonstrate value beyond Hit@5 to overcome this
- **[FZ 5e1: Retrieval Strategy Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md)**: v2 data source for all baseline numbers
