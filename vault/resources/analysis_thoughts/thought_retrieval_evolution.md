---
tags:
  - resource
  - analysis
  - argument
  - retrieval
  - benchmark
  - experiment_history
keywords:
  - retrieval evolution
  - strategy benchmark
  - PPR vs BFS
  - hybrid RRF
  - unified index engine
  - Hit@K answer-quality disconnect
  - SQLite sqlite-vec FTS5
topics:
  - Retrieval
  - Experimental History
  - Tessellum Foundations
  - Information Retrieval
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "3"
folgezettel_parent: ""
---

# How Tessellum's Retrieval System Was Tested Into Shape

## Thesis

Tessellum's retrieval design — **unified SQLite + sqlite-vec + FTS5** as the substrate, **hybrid RRF** as the default surface, **best-first BFS** as the graph strategy, **no PPR**, and **direct metadata filter** as a parallel surface — did not arrive by intuition. It was the survivor of a 14-strategy bake-off across 4,823 questions plus a long sequence of follow-up experiments that rejected three plausible-looking alternatives. This note narrates that experimental descent so a future contributor understands *why* the shipped design looks the way it does and not the obvious alternatives.

The companion synthesis [`thought_retrieval_synthesis`](thought_retrieval_synthesis.md) (FZ 3a) names the resulting design. This note narrates the path.

## The descent in seven steps

### Step 1 — The foundational benchmark: 4,823 Q × 14 strategies

The starting question was practical: *which retrieval strategy should the system default to?* The earliest evidence — a small-sample run (n=194) showing PPR as the best strategy — turned out to be a sampling artifact. The foundational benchmark ran 14 strategies against 4,823 questions:

| Strategy | Hit@5 | Position |
|---|---:|---|
| Dense (sentence-transformers) | **0.815** | winner |
| BM25 | 0.751 | second |
| Keyword-only | 0.529 | best LIKE-bound strategy |
| Various graph strategies (PPR, BFS, DFS, combined) | 0.026 – 0.527 | Pareto-dominated |

**Dense won decisively.** All graph strategies were Pareto-dominated by Dense or BM25. The small-sample PPR-best reading reversed under the larger sample.

### Step 2 — Why graph strategies lost: the shared `LIKE` bottleneck

A failure-analysis pass on the 89.5% of graph-strategy failures found a structural cause: 11 of the 14 strategies shared the same SQL `LIKE`-based seed-resolution path. The graph traversal (BFS / DFS / PPR) is *expansion*, not *retrieval* — it inherits the seed-resolution's limits. Only Dense and BM25 are *independent* seed mechanisms; the rest depend on `_resolve_terms() LIMIT 10`, which caps the expansion's input quality.

**Conclusion**: graph-as-retrieval isn't a fair test until the seeds come from a content-aware mechanism, not from `LIKE`. Independent strategies (0.751 – 0.815) beat the best LIKE-bound strategy (0.529) by 42–54 percentage points.

### Step 3 — The benchmark itself was confounded

A counter-analysis on the gold sets found that ~80% of them were *single-note*. Graph strategies were only tested on the ~10% multi-note slice. The "graph is zero value" verdict was partly an artifact of the gold-set construction: most questions had a single correct answer, so any system that found that note Won; graph expansion to neighbors was either useless (when the gold was already in seeds) or treated as a Miss (when the gold sat in a different cluster).

This didn't rescue PPR — it just reframed the verdict: *"metadata-only search loses to full-content search"* rather than *"graph is intrinsically zero value."* The bottleneck wasn't the algorithm; it was the *information access depth* (~30-80 tokens of YAML vs ~500-5000 tokens of body).

### Step 4 — Unified-engine hypothesis: push the boundary one level down

A separate diagnostic surfaced that the production stack was operationally fragile: it carried *four artifacts* (`notes.db` + `bm25.pkl` + `.npy` + `.json`), each rebuilt by its own script, with no atomicity guarantee. A real production incident (sync-script COE 2026-04-29) confirmed the fragility. The hypothesis: push the unification one level down — from query-time hybridization to *storage-layer* consolidation. **One file. One backend. SQLite + sqlite-vec + FTS5.**

### Step 5 — Parity test: a hopeful "yes" with one twist

A controlled experiment (Surface A: current 4-artifact stack; Surface B: proposed unified engine; same vault snapshot, same git SHA) tested five hypotheses:

| H | Claim | Verdict |
|---|---|---|
| H1 | FTS5 BM25 ranking parity vs `rank_bm25` (ρ ≥ 0.85) | **Failed** (ρ = 0.467, top-1 agreement 40%, Hit@5 regression −4 questions) |
| H2 | sqlite-vec p99 < 50 ms | Passed |
| H3 | Build-time variance lower on B | Passed |
| H4 | Incremental update ≥ 25× faster on B | Passed |
| H5 | Atomicity (kill -9 leaves coherent state) | Passed |

The BM25 parity failed because FTS5's tokenizer + baked-in k1=1.2 don't match rank_bm25's behavior, and FTS5 has no runtime override. The decision rule was pre-registered: H1 fail → Plan B.

### Step 6 — Plan B + the +12pp moment

**Plan B**: implement BM25 in the unified engine as a `rank_bm25`-backed SQLite UDF. Same algorithm, same parameters, same ranking — wrapped in SQL. A follow-up experiment validated Plan B end-to-end:

| H' | Claim | Verdict |
|---|---|---|
| H1' | UDF parity ρ ≥ 0.85 | **ρ = 1.0000** (perfect — same algorithm) |
| H2' | UDF overhead < 2× | 0.94× (slightly *faster* — TEMP table beats Python sort) |
| H3' | One-SQL hybrid RRF runs end-to-end | 35-line CTE; mean 32 ms, p99 93 ms |
| H4' | Hybrid Hit@5 > best single strategy | **+12pp** (32/67 vs Dense's 24/67) |

**The +12pp lift was the breakthrough.** Hybrid RRF wasn't theoretically novel — it's a known information-retrieval pattern — but it was *operationally* novel for this stack: the unified-engine consolidation made one-SQL hybrid feasible, and the empirical lift confirmed it. The decision: **ship hybrid as the default; BM25 and Dense as flags for ablation/diagnosis.**

### Step 7 — Priority-based graph search rescues *some* graph strategies

A separate counter-trail explored why all graph strategies failed in step 1. The mechanism is the **friend-of-a-friend paradox**: avg neighbor degree is 78× seed degree; hubs (1.5% of nodes) appear in 89% of 1-hop neighborhoods. Raw BFS drowns in hub noise. Three rescue knobs were proposed: edge weighting, top-k frontier selection, path aggregation.

A priority-graph benchmark tested 11 algorithms × 4,909 questions:

| Algorithm | Hit@5 | Verdict |
|---|---|---|
| Best-first BFS (priority frontier) | recovered from BFS catastrophe | useful |
| Hub-aware PPR | closes 98.5% of the synth gap | competitive on synth |
| PPR on multi-hop real questions | **+11pp over Dense** | **wins on Hit@K** |
| A* with path-cost | adds zero value | rejected |
| Pure structural walks (Pixie) | fails without semantic anchoring | rejected |
| MCTS-RAG | LLM is load-bearing piece | too slow for production |

PPR's +11pp lift on multi-hop reopened the question: *should Tessellum ship PPR after all?* The answer, in step 8, was no — and why.

### Step 8 — The Hit@K-to-answer-quality disconnect

A final experiment correlated Hit@K with end-to-end answer quality on real production queries. **Correlation: ρ = 0.37.** Hit@K and answer quality are *different optimization problems*. PPR's +11pp Hit@K lift on multi-hop barely moved the answer-rating curves. The lift was largely benchmark theater.

The criterion that mattered was: *given a query, does the system produce a good answer?* Best-first BFS, at 30 ms per query versus PPR's ~250 ms, with comparable end-to-end answer quality, was Pareto-optimal in production. **The decision: ship best-first BFS; skip PPR entirely; document the rationale.**

Two corollaries:

1. *Don't ship retrieval changes that improve Hit@K but don't improve answers.* This is the operational discipline derived from the disconnect.
2. *Future eval should measure answer quality, not Hit@K alone.* Wave 5b's eval framework (LLMJudge 5-dim) operationalizes this — the rubric measures relevance / completeness / accuracy / clarity / structural integrity, not Hit@K.

## What the descent rejects

Four framings the descent considered and rejected:

- **"PPR is the best graph strategy."** True on Hit@K, false on answer quality. The benchmark and the production goal are different optimization problems.
- **"Hybrid hurts because of false positives."** False — the +12pp lift held across all 11 question types. Hybrid's failure modes are different from BM25's and from Dense's; RRF's rank-blending absorbs them rather than compounding them.
- **"Four artifacts are fine if we're careful."** Operationally untenable. The 2026-04-29 sync COE was the empirical disproof; the unified engine was the operational fix.
- **"Graph traversal is intrinsically zero value."** Reframed: it's the *seed-resolution layer* (LIKE-bound) that loses to content-aware retrieval. With content-aware seeds (Dense top-K), graph expansion can win on multi-hop. But the answer-quality disconnect means Hit@K wins don't translate to user value — so Tessellum ships best-first BFS as a graph *surface* for users who want explicit traversal, not as a default.

## What this means for users

Tessellum's [`tessellum search`](../how_to/howto_first_vault.md) defaults to hybrid RRF for the +12pp reason. Users who want explicit single-strategy behavior use `--bm25` / `--dense` / `--bfs`. The graph surface (`--bfs <seed>`) is for traversal queries ("what's near this note?"), not for ranked retrieval over arbitrary text — that's the hybrid surface's job.

The [`tessellum filter`](../how_to/howto_first_vault.md) surface (added per user feedback mid-port) is a fourth retrieval mode: direct metadata filter (`--tag`, `--bb`, `--status`, `--date-range`). It bypasses the index entirely and queries `notes.notes` directly — the right surface when you already know the structural shape of what you're looking for.

The unified engine (SQLite + sqlite-vec + FTS5) means all of this is one SQLite file. Atomicity, portability, and zero coordination cost are downstream of step 4's hypothesis.

## Related Notes

- [`thought_retrieval_synthesis`](thought_retrieval_synthesis.md) — FZ 3a — distils the shipped design (unified engine + hybrid RRF + best-first BFS + metadata filter) and the rules that fall out
- [`thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — FZ 1 — the typed substrate retrieval operates over
- [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md) — FZ 1a1a — places retrieval as System D in the architectural split
- [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — FZ 2a — DKS (System P side) is independent of retrieval (System D side)
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — System P ⊥ System D ⊥ shared substrate

## See Also

- [`entry_retrieval_trail`](../../0_entry_points/entry_retrieval_trail.md) — per-trail entry point with reading order + summary of experimental progress
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 3 (root), Retrieval trail
