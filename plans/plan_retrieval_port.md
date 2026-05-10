---
tags:
  - project
  - plan
  - tessellum
  - retrieval
  - search
  - system_d
keywords:
  - retrieval port
  - hybrid retrieval
  - bm25 dense rrf
  - best-first bfs
  - five wave port
  - system d
topics:
  - Retrieval
  - System D
  - v0.1 Roadmap
  - Search
language: markdown
date of note: 2026-05-10
status: completed
building_block: procedure
---

# Plan — Retrieval Port to Tessellum (5-Wave)

## Problem

Tessellum just shipped the **System D substrate** in v0.0.12 — a 2-table SQLite index (`notes` + `note_links`) populated by `tessellum index build`. The substrate is in place; there's no QUERY layer yet.

Step 6 of `plans/plan_v01_src_tessellum_layout.md` lists "Retrieval (BM25 + dense + RRF)" as a one-line item. That under-frames the work. The parent project has a mature, experiment-driven retrieval stack (FZ trail 5e, ~100 nodes across 5 months) with hard-won lessons that change the recommended port plan. This plan codifies what to port, in what order, and — equally important — **what not to port**.

## Why retrieval matters now

Tessellum's value proposition is typed-knowledge **slipbox**, not typed-knowledge **library**. Without retrieval, users can author + validate + capture, but they can't *find* what they've authored. The CQRS substrate is half a system: System P (capture) ⊥ System D (retrieval), one shared substrate (the vault + index). Right now Tessellum's System D has the build output (the SQLite DB) but no readers. This plan builds the readers.

## Parent's retrieval architecture — three tiers

Per the FZ 5e research trail in AbuseSlipBox:

```
┌─────────────────────────────────────────────────────────┐
│ Tier 3 — Skills (orchestration)                         │
│   skill_slipbox_search_notes.md   8-strategy router     │
│   skill_slipbox_answer_query.md   5-stage QA pipeline   │
└────────────────────────┬────────────────────────────────┘
                         │ invoke
┌────────────────────────▼────────────────────────────────┐
│ Tier 2 — Scripts (retrieval primitives)                 │
│   bm25_search.py       lexical (rank_bm25 / FTS5)       │
│   dense_search.py      semantic (sentence-transformers) │
│   graph_traversal.py   BFS / DFS / PPR                  │
│   query_expansion.py   intent + acronym + term-expand   │
│   working_memory.py    multi-strategy score blending    │
│   context_assembler.py token-budgeted assembly          │
│   hybrid (one SQL UNION + RRF)                          │
└────────────────────────┬────────────────────────────────┘
                         │ read
┌────────────────────────▼────────────────────────────────┐
│ Tier 1 — Unified DB (substrate, shipped v0.0.12)        │
│   notes        +  note_links                            │
│   notes_fts    (FTS5 virtual)        ← v0.0.13          │
│   notes_vec    (sqlite-vec virtual)  ← v0.0.14          │
└─────────────────────────────────────────────────────────┘
```

Tessellum currently has Tier 1 partially (no FTS5/vec yet). Waves 1-3 below extend it; Waves 4-5 build Tiers 2-3.

## Three lessons from the parent's experiments — load-bearing

These are **non-obvious** findings. Tessellum should encode them, not re-learn them.

### 1. Hybrid RRF (+12pp) is the production winner

Per FZ 5e1c3a1a1 — a one-SQL hybrid (`UNION ALL` of BM25 + dense, ranked by Reciprocal Rank Fusion) lifted Hit@5 by **+12 percentage points** over the best single strategy (32/67 vs 24/67). The lift was **enabled by unified-engine consolidation** — RRF over four separate artifacts (`bm25.pkl` + `.npy` + `.json` + `notes.db`) was operationally untenable; with a single SQLite file containing FTS5 + sqlite-vec, hybrid becomes one SQL line. Tessellum's substrate already chose the unified-engine design — Wave 3 just executes the SQL.

**Implication for Tessellum**: hybrid is the default, BM25/dense are flags (`--bm25`, `--dense`), not the other way around.

### 2. Best-first BFS > PPR for real-world answer quality

Per FZ 5e2b1c — the **Hit@K-to-answer-quality disconnect** (correlation ρ=0.37). Hit@5 measures whether the right note is in the top-5; answer quality measures whether the LLM's response is actually good. PPR optimizes Hit@K through expensive multi-hop walks (αat 0.85, ~250ms per query). Best-first BFS is simpler (single hop, priority-queue frontier), faster (~30ms), and yields equivalent or better answer quality on real queries. PPR's "lift" is largely benchmark theater; BFS is Pareto-optimal in production.

**Implication for Tessellum**: ship best-first BFS. **Skip PPR entirely.** Save 257 LOC + the cognitive overhead of explaining when each is appropriate. Document the lesson; let users who really need PPR add it as an extension.

### 3. Validate on end-to-end answer quality, not retrieval metrics

Corollary of #2 — Hit@5 lifts of 12pp on RRF barely moved answer-rating curves. The benchmark surface and the answer-quality surface are different optimization problems. Tessellum's retrieval should be benchmarked end-to-end (a query → a response → a quality score), not just on retrieval metrics. Defer this until Wave 5+ when there's enough surface to evaluate, but encode the principle now: **don't ship retrieval changes that improve Hit@K but don't improve actual answers.**

## Design principles

1. **Unified engine.** One SQLite file holds metadata + FTS5 + sqlite-vec. The parent project's 4-artifact baseline (`notes.db` + `bm25.pkl` + `.npy` + `.json`) is a known anti-pattern; we don't replay it.
2. **Hybrid is the default.** `tessellum search <query>` runs RRF-fused BM25+dense by default. `--bm25`, `--dense` are explicit overrides for ablation/diagnosis.
3. **Skip PPR.** Best-first BFS is the production graph strategy. Document the rationale (FZ 5e2b1c) so future contributors don't re-add PPR.
4. **Read-only library + thin CLI.** The retrieval modules read the indexed DB; no mutation. CLI subcommands wrap the library calls. Mirrors `tessellum.composer.load_pipeline` + `tessellum composer validate` pattern.
5. **Schema migrations are destructive within v0.x.** Adding `notes_fts` and `notes_vec` is a schema-evolution change; users re-run `tessellum index build --force`. No incremental migrations until v0.1.0+.
6. **Track real metrics from Wave 5+.** When the answer-query skill ships, store every (query, retrieved_notes, answer, rating) tuple under `runs/retrieval/` for offline review — the substrate for the eventual eval framework.

## Proposed approach — 5 waves

| Wave | Scope | Schema change | New deps | LOC est. | Milestone |
|---|---|---|---|---|---|
| **Wave 1** | BM25 + FTS5 | adds `notes_fts` virtual table | none (rank-bm25 already declared) | ~400 | `tessellum search --bm25 <query>` works |
| **Wave 2** | Dense + sqlite-vec | adds `notes_vec` virtual table | none (sentence-transformers + sqlite-vec already declared) | ~500 | `tessellum search --dense <query>` works |
| **Wave 3** | Hybrid RRF | none (joins existing tables) | none | ~150 | `tessellum search <query>` (default) — hybrid by RRF |
| **Wave 4** | Best-first BFS | none (uses `note_links`) | none (networkx already declared) | ~400 | `tessellum search --bfs <seed_note>` traverses graph |
| **Wave 5** | Skill orchestration | none | none | ~600 (skill canonical bodies + 1 small router script) | `skill_tessellum_search_notes` + `skill_tessellum_answer_query` shipped; skills validate via Composer Wave 1b's CLI |

Total estimate: **~2050 LOC** + tests. Realistic timeline: **5 versions over 1-2 weeks** at the current cadence (one wave per release).

### Wave 1 — BM25 + FTS5 (v0.0.13)

Extend the indexer's schema and add the lexical retrieval module.

- **Schema** (`src/tessellum/indexer/schema.sql`): add `CREATE VIRTUAL TABLE notes_fts USING fts5(note_id, note_name, body, content='', tokenize='porter')`. Use FTS5's external-content / contentless mode so the FTS index is a derived view that doesn't duplicate body storage.
- **Builder** (`src/tessellum/indexer/build.py`): on each note, write a row to `notes_fts` (`note_id`, `note_name`, `body`). The body is already in memory from `parse_note`.
- **Retrieval module** (`src/tessellum/retrieval/__init__.py` + `bm25.py`): `bm25_search(db, query, k=20) -> list[BM25Hit]`. Uses FTS5's built-in BM25 ranking (`SELECT note_id, bm25(notes_fts) FROM notes_fts WHERE notes_fts MATCH ?`).
- **CLI** (`src/tessellum/cli/search.py`): `tessellum search --bm25 <query> [--k N]`. Initial CLI lands here; Wave 3 makes hybrid the default.
- **Tests**: schema valid, FTS5 query returns sensible BM25 ranking on a fixture vault, CLI exit codes.

### Wave 2 — Dense + sqlite-vec (v0.0.14)

- **Schema**: `CREATE VIRTUAL TABLE notes_vec USING vec0(note_id_int INTEGER PRIMARY KEY, embedding FLOAT[384])`. Adds `note_int_id INTEGER UNIQUE` to `notes` for the join key.
- **Builder**: lazy-loads `sentence-transformers/all-MiniLM-L6-v2` once per build, encodes each note's embedding text (`note_name + tags + keywords + topics + body[:500_lines]`), writes to `notes_vec`.
- **Retrieval** (`src/tessellum/retrieval/dense.py`): `dense_search(db, query, k=20) -> list[DenseHit]`. Encodes the query, runs `SELECT ... FROM notes_vec WHERE embedding MATCH ? AND k = ?`.
- **CLI**: `tessellum search --dense <query>` adds the dense flag.
- **Trade-off note**: first build is slow (~1.5s model load + ~10ms/note for 71-note vault → ~2s total); subsequent builds reuse the model in-process. Document this in Wave 2's CHANGELOG.

### Wave 3 — Hybrid RRF (v0.0.15)

The +12pp winner. Single SQL query — no new schema.

- **Retrieval** (`src/tessellum/retrieval/hybrid.py`): `hybrid_search(db, query, k=20, k1_rrf=60) -> list[HybridHit]`. One SQL with `UNION ALL` of BM25 and dense top-K, ranked by `1/(rank + k1_rrf)` summed across both result sets.
- **CLI**: `tessellum search <query>` (default — no flag = hybrid). `--bm25`, `--dense` remain as explicit overrides.
- **Default change**: Wave 1's CLI behaved as `--bm25`-default; Wave 3 flips it. Document in CHANGELOG.

### Wave 4 — Best-first BFS (v0.0.16)

- **Retrieval** (`src/tessellum/retrieval/graph.py`): `GraphTraverser` class wrapping the indexed DB; `best_first_bfs(seed_note_id, k=20, max_depth=3) -> list[GraphHit]`. Priority queue keyed on a heuristic (in_degree-aware, hub-skipping per FZ 5e2b research).
- **CLI**: `tessellum search --bfs <seed_note_id> [--depth N]`.
- **No PPR.** Document in CHANGELOG: "PPR was deliberately not ported — see plans/plan_retrieval_port.md § Three lessons."

### Wave 5 — Skill orchestration (v0.0.17 / v0.1.0)

The two production skills:

- **`vault/resources/skills/skill_tessellum_search_notes.md`** — multi-strategy router. Decision tree: single-token → BM25; architectural → BFS; multi-hop semantic → hybrid; else → dense. Pure markdown skill canonical with `<!-- :: section_id = X :: -->` anchors per the convention. Uses the Wave 1-4 retrieval modules. **Adapt** the parent's tree to drop PPR branches; keep the rest.
- **`vault/resources/skills/skill_tessellum_answer_query.md`** — 5-stage QA pipeline: query expansion → multi-strategy retrieval → working memory scoring → context assembly → synthesis with citations. Optional Composer sidecar (Wave 5+ Composer wires the LLM dispatch).
- **`src/tessellum/retrieval/router.py`** — small (~150 LOC) router function the search-notes skill invokes. Decision-tree implementation; no LLM dispatch.

This wave produces the **first user-visible answer-the-question capability**. After Wave 5: `tessellum search "how does composer compile?"` returns ranked, expanded, contextualized notes; the answer-query skill (when invoked by an agent runtime) produces a synthesized response with citations.

## What we're explicitly NOT porting

- **PPR** (`ppr_search.py`, ~257 LOC). Documented in design principles + Wave 4. Re-add later behind an extras flag if a real use case surfaces.
- **Legacy artifact format support** (`bm25.pkl` / `.npy` / `.json`). Tessellum starts unified; never had the four-artifact baseline.
- **Amazon-specific term boosts** in working_memory and context_assembler. Keep the generic blending logic; drop the domain knobs.
- **Hit@K-only benchmarking**. Wave 5+ ships eval infrastructure that measures answer quality, not retrieval metrics in isolation.

## Migration steps for Wave 1 (when we start)

1. Add `notes_fts` virtual table to `schema.sql` (one DDL statement).
2. Update `build.py` to populate `notes_fts` per note (one helper function).
3. Add `tests/smoke/test_indexer.py::test_fts5_index_populated` — verify FTS5 search returns expected note IDs.
4. Author `src/tessellum/retrieval/__init__.py` + `bm25.py` (~150 LOC).
5. Add `tests/smoke/test_retrieval_bm25.py` — verify BM25 ranking on fixture vault.
6. Author `src/tessellum/cli/search.py` — `tessellum search --bm25` subcommand.
7. Add `tests/cli/test_search_cli.py` — verify CLI exit codes + JSON output.
8. Update `cli/main.py` dispatcher + banner.
9. Bump to v0.0.13. CHANGELOG entry.
10. Smoke-test against the real vault: `tessellum search --bm25 'composer'` should return Composer-related notes ranked sensibly.

Subsequent waves follow the same pattern with their respective scopes.

## Open questions

- **Should `tessellum index build` populate FTS5 and sqlite-vec by default, or behind flags?** Lean: default, with `--no-fts` / `--no-dense` opt-outs for users with embedding-model constraints. Slow first build (~2s) is the tradeoff.
- **Embedding model choice — pin to `all-MiniLM-L6-v2`, or expose `--model` flag?** Lean: pin in v0.0.14, expose flag in v0.0.15+ once we have stats from the default. The parent uses MiniLM and the schema's 384-D matches.
- **`tessellum search --json`?** Yes — ship it from Wave 1 (mirrors format check / composer validate).
- **Where does the answer-query skill's run trace go?** `runs/retrieval/<timestamp>_query_<slug>.json` — already established by `plan_cqrs_repo_layout.md`.
- **Index compaction on rebuild?** v0.0.13 always rebuilds from scratch (idempotent); incremental update is v0.0.13b or v0.0.18.

## See Also

- [`plan_v01_src_tessellum_layout.md`](plan_v01_src_tessellum_layout.md) — v0.1 plan; step 6 cross-references this plan
- [`plan_composer_port.md`](plan_composer_port.md) — Composer port plan (parallel scope: System P side of CQRS)
- [`plan_cqrs_repo_layout.md`](plan_cqrs_repo_layout.md) — repo layout (where `runs/retrieval/` lives)
- [`term_cqrs.md`](../vault/resources/term_dictionary/term_cqrs.md) — the principle this plan implements (System D = the descriptive retrieval system)

---

**Last Updated**: 2026-05-10
**Status**: **Complete** — all five waves shipped, plus a metadata-filter surface added per user request mid-port.

| Wave | Version | Module | What landed |
| ---- | ------- | ------ | ----------- |
| 1    | v0.0.13 | `retrieval/bm25.py` + `notes_fts` schema | BM25 over FTS5 |
| 2    | v0.0.14 | `retrieval/dense.py` + `notes_vec` schema (`distance_metric=cosine`) | sentence-transformers/MiniLM-L6-v2, 384-D |
| 3    | v0.0.15 | `retrieval/hybrid.py` | RRF over BM25 + dense in one SQL — the +12pp winner |
| 4    | v0.0.16 | `retrieval/graph.py` | Best-first BFS over `note_links` (no PPR per FZ 5e2b1c) |
| 5    | v0.0.17 + v0.0.18 | `retrieval/router.py`, `skill_tessellum_search_notes.md`, `tessellum filter` CLI (metadata.py) | Skill orchestration; `tessellum filter` for direct YAML-meta search |

**Resolved open questions:**

- *FTS5 + sqlite-vec by default?* Yes — `tessellum index build` populates both; `--no-fts` / `--no-dense` opt-outs deferred (no user has asked).
- *Embedding model pinned?* Pinned to `all-MiniLM-L6-v2` in v0.0.14. `--model` flag deferred.
- *`tessellum search --json`?* Shipped from Wave 1.
- *Run traces*: `runs/retrieval/<timestamp>_*.json` convention established but not yet wired (no skill currently writes traces — `runs/composer/` is the active path).

**Things added beyond the plan:**

- `tessellum filter --tag/--bb/--status/...` (v0.0.17) — direct metadata filtering surfaced after the user pointed out "do not forget the simplest search based on the SQLite meta fields extracted from YAML header." Lives in `retrieval/metadata.py`. Not in the original plan; load-bearing for users who already know what they're looking for.

**What's deliberately NOT in the port** (encoded in the plan and held to):

- PPR — skipped. Saved ~257 LOC. Best-first BFS is Pareto-optimal.
- Legacy artifact format support (.pkl/.npy/.json side files).
- Amazon-specific term boosts in working-memory blending.

Test count at port closure: covered by the same 464-passed / 1-skipped suite as the Composer port.
