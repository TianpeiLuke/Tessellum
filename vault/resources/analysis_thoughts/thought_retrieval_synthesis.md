---
tags:
  - resource
  - analysis
  - argument
  - retrieval
  - synthesis
  - system_d
keywords:
  - retrieval synthesis
  - unified index engine
  - hybrid RRF
  - best-first BFS
  - metadata filter
  - SQLite sqlite-vec FTS5
  - System D
topics:
  - Retrieval
  - System D
  - Tessellum Design
  - Information Retrieval
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "3a"
folgezettel_parent: "3"
---

# Synthesis: Tessellum's Retrieval System Design

## Thesis

After the eight-step experimental descent in [`thought_retrieval_evolution`](thought_retrieval_evolution.md), the retrieval design compresses to one substrate, four surfaces, and one operating rule:

> **One unified SQLite file holds metadata + graph edges + FTS5 lexical index + sqlite-vec dense embeddings. Four retrieval surfaces (hybrid RRF, BM25, dense, best-first BFS) plus a parallel metadata-filter surface read from that one file. The operating rule is: optimize for end-to-end answer quality, not for Hit@K — Hit@K is a diagnostic, not a goal.**

This note is the architecture-level summary of what's shipped, what's deliberately *not* shipped, and what falls out of the design decisions. Read this when you want the destination; read [`thought_retrieval_evolution`](thought_retrieval_evolution.md) (FZ 3) when you want the journey.

## The substrate: one unified engine

One SQLite database file holds all four index modalities:

```
data/tessellum.db
├── notes              (metadata: tags, keywords, topics, BB, status, dates)
├── note_links         (edges: source → target across the typed graph)
├── notes_fts          (FTS5 virtual table: BM25 over body text)
└── notes_vec          (sqlite-vec virtual table: 384-D dense embeddings)
```

Plus a few auxiliary tables (folgezettel chain index, content-hash for incremental updates). All in **one file**.

### Why one file, not four artifacts

Four artifacts (`notes.db` + `bm25.pkl` + `.npy` + `.json`) have three operational failure modes:

| Failure mode | Symptom | Frequency in production |
|---|---|---|
| Sync drift | Notes added but embeddings stale → dense search misses recent notes | Every vault write |
| Build atomicity | One artifact builds; another fails partway → coherent on disk but inconsistent across artifacts | Whenever any build script crashes |
| Coordination cost | "Which artifacts need to rebuild on this change?" requires explicit logic | Every dependency change |

A real production incident (sync-script wipe, 2026-04-29) demonstrated all three at once. The unified engine eliminates the failure surface: there's nothing to sync across, no partial-build state, no coordination logic. `tessellum index build` either succeeds (one transaction commits) or fails (one transaction rolls back). The SQLite write-ahead-log gives crash recovery for free.

### Why SQLite + sqlite-vec + FTS5

Three properties drove the choice:

1. **Embedded, $0 cost.** No server, no managed service, no monthly fee. The whole index ships as a file the user owns.
2. **Three-way native composition.** SQLite's FTS5 extension and the sqlite-vec extension compose with regular SQL — joins, CTEs, transactions — without IPC. One SQL query can blend lexical, dense, and metadata in 35 lines. (DuckDB + vss + fts is an evaluated alternative; it failed BM25-parity in the bake-off.)
3. **Python access via stdlib + one wheel.** `sqlite3` is in the standard library; `sqlite-vec` is a single pip dependency. No transitive runtime dep tree.

The unified engine is the bottom layer; everything else is read surfaces over it.

## The four retrieval surfaces + one metadata-filter surface

Five user-facing retrieval modes, each tuned to a different intent:

### 1. Hybrid RRF (the default)

`tessellum search "graph traversal"` — no flag.

- **What it does**: runs BM25 over the body + dense vector search in parallel, blends ranks via Reciprocal Rank Fusion (RRF), returns top-K.
- **One SQL**: a 35-line CTE — `notes_fts` MATCH + `notes_vec` MATCH + FULL OUTER JOIN + `1/(rank + k1)` RRF aggregation.
- **Latency**: ~32 ms mean, ~93 ms p99 on a 9k-note vault.
- **Why default**: the empirical winner — Hit@5 lift of +12pp over the best single strategy across all 11 question types.

### 2. BM25 (the lexical ablation surface)

`tessellum search --bm25 "PageRank"`.

- **What it does**: BM25 over body text, no dense component.
- **When to use it**: looking for exact terminology; diagnosing why hybrid found / missed a specific result.
- **Why ship it**: ablation requires the components to be individually addressable. Without `--bm25`, debugging hybrid is opaque.

### 3. Dense (the semantic ablation surface)

`tessellum search --dense "what does this concept name?"`.

- **What it does**: encodes the query via sentence-transformers/all-MiniLM-L6-v2 (384-D, cosine), runs `vec0 MATCH` over `notes_vec`.
- **When to use it**: looking for semantically related notes whose vocabulary doesn't match yours; diagnosing hybrid.
- **Why this model**: small (~80 MB), fast on CPU, well-evaluated. Tessellum doesn't ship a larger model by default — users wanting one bring their own.

### 4. Best-first BFS (the graph traversal surface)

`tessellum search --bfs term_page_rank.md --depth 3`.

- **What it does**: priority-queue best-first BFS over `note_links` from a seed note, scoring nodes by in-degree-aware traversal priority.
- **When to use it**: navigational queries ("what's near this note?"), not ranked retrieval over arbitrary text.
- **Why this and not PPR**: see "What we deliberately don't ship" below.

### 5. Metadata filter (the structured-query surface)

`tessellum filter --tag concept --bb model --status active`.

- **What it does**: direct SQL filter over `notes` table — no FTS5, no embedding, no graph traversal.
- **When to use it**: you already know the structural shape of what you're looking for (a BB type, a tag, a status, a date range).
- **Why separate from `search`**: structured queries don't compose naturally with rank-based scoring; treating them as a fourth ablation flag would muddle the surface.

## What we deliberately don't ship

Three retrieval techniques tested and rejected:

### No PPR

Personalized PageRank wins on Hit@K for multi-hop queries (+11pp over Dense in the benchmark). Tessellum doesn't ship it. Reason:

- **Hit@K → answer-quality correlation is ρ = 0.37** (per the FZ 3 evolution note's step 8). Hit@K wins don't translate to user-perceived answer quality.
- **Latency**: ~250 ms per query vs best-first BFS's ~30 ms. 8× slower.
- **Cognitive overhead**: another graph algorithm to explain ("when do I use PPR vs BFS?"). Two algorithms with overlapping use cases is one too many.

Best-first BFS is Pareto-optimal in production: comparable answer quality, 8× faster, simpler to explain.

### No legacy four-artifact format

The previous-generation `bm25.pkl` + `.npy` + `.json` + `notes.db` baseline isn't supported. New installs go straight to the unified engine. No migration path is shipped — the unified engine is the only supported configuration.

### No domain-specific term boosts

The parent project (AbuseSlipBox) had Amazon-specific term boosts in its working-memory and context-assembler layers. Tessellum ships the generic blending logic; the domain knobs are dropped. Users who need them can extend the retrieval module — but they're not in the default surface.

## The five rules that fall out

Once the substrate + four surfaces + one filter are committed, five operational rules drop out:

1. **`tessellum index build` is the only write to `data/`.** Read surfaces never mutate the index; they read what `index build` produced. (System D side of the CQRS commitment — see [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md).)
2. **Hybrid is the default, single strategies are flags.** Reverses the parent project's history (where BM25 was the default and hybrid was the experimental flag). The benchmark earned the default switch.
3. **Schema migrations are destructive within v0.x.** Adding a new index column means `tessellum index build --force` — full rebuild, no incremental migration. Cost: a few seconds for a typical vault. Worth more than the maintenance burden of incremental schema migrations at this stage.
4. **Validate retrieval changes on answer quality, not Hit@K.** Encoded in `tessellum composer eval --judge-backend anthropic` — the LLMJudge 5-dim rubric measures relevance / completeness / accuracy / clarity / structural integrity, not Hit@K. Hit@K stays as a diagnostic, not as a metric retrieval changes are gated on.
5. **Track real metrics from Wave 5+.** When the answer-query skill ships (v0.2+), store every `(query, retrieved_notes, answer, rating)` tuple under `runs/retrieval/` for offline review — the substrate for the eventual eval pipeline.

## How the four surfaces compose

The four search surfaces aren't competing — they answer different question shapes. A 2×2 of "do I know what I'm looking for?" × "do I know where it lives?" maps cleanly:

|  | Don't know vocabulary | Know vocabulary |
|---|---|---|
| **Don't know structure** | `tessellum search` (hybrid RRF — semantic + lexical) | `tessellum search --bm25` (lexical only) |
| **Know structure** | `tessellum filter --bb concept` then `tessellum search` over the filtered set | `tessellum filter --tag <tag>` (no retrieval, just SQL) |

The `--bfs` surface lives outside this 2×2 — it answers a different question shape entirely: *"what's near this note in the graph?"* Used when you already have a starting note and want to traverse the neighborhood.

## What ships in Tessellum today

The retrieval port is complete (per [`plans/plan_retrieval_port.md`](../../../plans/plan_retrieval_port.md) — *status: completed*). Five waves shipped across v0.0.13–v0.0.18:

| Wave | Version | What landed |
|---:|---|---|
| 1 | v0.0.13 | BM25 over FTS5 (`tessellum search --bm25`) |
| 2 | v0.0.14 | Dense over sqlite-vec (`tessellum search --dense`) |
| 3 | v0.0.15 | Hybrid RRF as default (`tessellum search`) |
| 4 | v0.0.16 | Best-first BFS (`tessellum search --bfs`) |
| 5 | v0.0.17–18 | Skill orchestration + metadata filter (`tessellum filter`) |

The retrieval surface is feature-complete for v0.1. v0.2+ adds the eval pipeline that runs LLMJudge over recorded `(query, retrieved, answer, rating)` tuples, closing the loop the FZ 3 evolution note's step 8 motivated.

## Related Notes

- [`thought_retrieval_evolution`](thought_retrieval_evolution.md) — FZ 3 — the eight-step experimental descent this synthesis arrives at
- [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md) — FZ 1a1a — locates retrieval as System D in the architectural split
- [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) — FZ 1a1 — the two-system architecture retrieval lives on the D side of
- [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — FZ 2a — DKS reads retrieval results for context but never invokes a write; the read/write asymmetry mirrors the CQRS commitment
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — System P ⊥ System D commitment

## See Also

- [`entry_retrieval_trail`](../../0_entry_points/entry_retrieval_trail.md) — per-trail entry point with reading order + summary of experimental progress
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map
- [`howto_first_vault`](../how_to/howto_first_vault.md) — practical walkthrough that uses all five surfaces
- `plans/plan_retrieval_port.md` — the port plan this synthesis traces

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 3a, Retrieval trail
