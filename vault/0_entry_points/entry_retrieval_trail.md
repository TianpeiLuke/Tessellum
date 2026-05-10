---
tags:
  - entry_point
  - folgezettel
  - argument_trail
  - retrieval
  - system_d
  - benchmark
keywords:
  - retrieval trail
  - benchmark history
  - hybrid RRF
  - best-first BFS
  - unified index engine
  - PPR vs BFS
topics:
  - Retrieval
  - System D
  - Folgezettel Trails
  - Experimental History
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Entry: Retrieval Trail (FZ 3) — How the Retrieval System Was Tested Into Shape

## Purpose

The Retrieval trail is the experimental descent that produced Tessellum's retrieval design: **one unified SQLite + sqlite-vec + FTS5 engine** + **hybrid RRF as the default** + **best-first BFS as the graph surface** + **direct metadata filter** + **no PPR**. The design isn't theory-driven — it's the survivor of a 14-strategy bake-off across 4,823 questions plus a sequence of follow-up experiments that rejected three plausible-looking alternatives.

This trail does two things at once: it records *which experiments were run and why* (so a contributor knows the answer to "why hybrid and not pure dense?" or "why no PPR?"), and it demonstrates the FZ convention by being a real research-trail example (so a user growing an experimental thread can copy its shape).

*"Which retrieval strategy should Tessellum ship as the default?"* → *"Hybrid RRF over a unified engine, with best-first BFS for graph traversal, and validation on answer quality not Hit@K."*

## ASCII Tree

```
3     How the Retrieval System Was Tested Into Shape  (8-step experimental descent)
└── 3a   ★ Retrieval System Design Synthesis  (4 surfaces + 1 metadata filter over a unified engine)
```

Linear, two nodes. The trail roots at FZ 3 with no parent (`folgezettel_parent: ""`); 3a descends from 3. The depth-2 shape is deliberate — extended experimental trails (each step's individual experiment, each ablation, each failure analysis) live in the source vault (FZ 5e1*–5e2b* in AbuseSlipBox) but don't need to ship to Tessellum users. What ships is the *summary* + the *synthesis*.

## FZ Table

| FZ ID | Note | BB | Role |
|-------|------|----|------|
| **3** | [`thought_retrieval_evolution`](../resources/analysis_thoughts/thought_retrieval_evolution.md) | argument | **Narrative** — 8 steps: foundational benchmark (Dense wins 0.815, graph Pareto-dominated) → shared LIKE bottleneck → gold-design confound → unified-engine hypothesis → parity test (BM25 fails ρ=0.85; Plan B triggered) → Plan B + hybrid RRF (+12pp lift) → priority-graph rescues PPR on Hit@K → ★ Hit@K-to-answer-quality disconnect rules out PPR for production. |
| **3a** | [`thought_retrieval_synthesis`](../resources/analysis_thoughts/thought_retrieval_synthesis.md) | argument | **★ Synthesis** — the shipped design: one substrate (SQLite + sqlite-vec + FTS5 in one file), four retrieval surfaces (hybrid RRF default, BM25, dense, best-first BFS) + one parallel metadata-filter surface (`tessellum filter`). Five operational rules + a 2×2 of question shapes mapping to surfaces. |

## Summary of experimental progress

Eight experimental moves, each rejecting one inadequate framing:

| # | Move | What changed | Source step in FZ 3 |
|--:|------|--------------|--------|
| 1 | Small-sample PPR-best reading → 4,823-Q benchmark | Sampling artifact; Dense wins at scale | Step 1 |
| 2 | "Graph is intrinsically bad" → "shared LIKE bottleneck" | The seed-resolution layer is the limit, not graph traversal | Step 2 |
| 3 | "Graph is zero value" → "single-note gold sets confound the verdict" | ~80% of gold sets graph-blind by construction | Step 3 |
| 4 | "Four artifacts are operationally fine" → "consolidate to one unified engine" | Three production failure modes; sync-script COE demonstrated all three | Step 4 |
| 5 | "SQLite + sqlite-vec + FTS5 drop-in replacement" → "BM25 parity fails (ρ=0.47); Plan B needed" | FTS5 tokenizer + baked-in k1 don't match `rank_bm25` | Step 5 |
| 6 | "Plan B: rank_bm25 as SQLite UDF" → "one-SQL hybrid RRF wins by +12pp" | Hybrid Hit@5 32/67 vs best single Dense 24/67 across all 11 question types | Step 6 |
| 7 | "PPR loses to Dense" → "priority-graph PPR beats Dense on multi-hop by +11pp Hit@K" | Friend-of-a-friend paradox; hub-aware PPR closes 98.5% of synth gap | Step 7 |
| 8 | "PPR wins on Hit@K so we should ship it" → ★ "Hit@K-to-answer-quality correlation is ρ=0.37; ship best-first BFS" | Hit@K and answer quality are different optimization problems | Step 8 |

After move 8, the design holds together: every shipped surface is justified by an experimental result, every rejected alternative has a documented reason, and the operating rule (*validate on answer quality, not Hit@K*) is encoded in the v0.2 eval pipeline.

## What's shipped in Tessellum

The retrieval port is complete (v0.0.13–v0.0.18). Five waves landed:

| Wave | Version | Module | Surface |
|---|---|---|---|
| 1 | v0.0.13 | `retrieval/bm25.py` + `notes_fts` schema | `tessellum search --bm25` |
| 2 | v0.0.14 | `retrieval/dense.py` + `notes_vec` schema (`distance_metric=cosine`) | `tessellum search --dense` |
| 3 | v0.0.15 | `retrieval/hybrid.py` | `tessellum search` (default — hybrid RRF) |
| 4 | v0.0.16 | `retrieval/graph.py` (best-first BFS only — no PPR) | `tessellum search --bfs` |
| 5 | v0.0.17–18 | `retrieval/router.py`, `retrieval/metadata.py` | `tessellum filter` + skill orchestration |

## What this trail rejects

Five experimental framings the descent considered and rejected:

- **"PPR is the best graph strategy."** True on Hit@K, false on answer quality. The benchmark and the production goal are different optimization problems.
- **"Hybrid hurts because of false positives."** False — the +12pp lift held across all 11 question types. RRF's rank-blending absorbs hybrid's failure modes rather than compounding them.
- **"Four artifacts are fine if we're careful."** Operationally untenable. The 2026-04-29 sync COE was the empirical disproof.
- **"Graph traversal is intrinsically zero value."** Reframed: the seed-resolution layer (`LIKE`-bound) loses to content-aware retrieval. Best-first BFS over content-aware seeds is the salvaged graph surface.
- **"Domain-specific term boosts add value."** Maybe in the parent domain; not in a generic public slipbox. The boosts were stripped during the port.

## Reading order

The trail is two notes — both worth reading once, in order:

- **First read (~30 min)** — start at FZ 3 (the experimental descent). By the end you understand both *which alternatives were tested* and *why they were rejected*.
- **Then FZ 3a (~15 min)** — the synthesis. Names the shipped design: one substrate, four surfaces, one metadata filter, five operating rules.
- **Re-reads (~5 min)** — start at FZ 3a (the synthesis); drop to FZ 3 only when you need to remember which experiment justified a particular design choice.

## Related Trails

- [`entry_architecture_trail`](entry_architecture_trail.md) — Trail 1 (Architecture / CQRS) — locates retrieval as System D in the read/write split. The retrieval trail operates within that commitment; it doesn't re-litigate it.
- [`entry_dialectic_trail`](entry_dialectic_trail.md) — Trail 2 (Dialectic / DKS) — DKS reads retrieval results for context but never invokes writes. The read/write asymmetry is the CQRS commitment Trail 3 lives inside.

## Related Terms

- [`term_cqrs`](../resources/term_dictionary/term_cqrs.md) — the architectural split retrieval lives on the D side of
- [`term_building_block`](../resources/term_dictionary/term_building_block.md) — the typed substrate retrieval operates over
- [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md) — the trail mechanism

## Related Entry Points

- [`entry_folgezettel_trails`](entry_folgezettel_trails.md) — the master FZ trail map (this trail is one of three so far)
- [`entry_building_block_index`](entry_building_block_index.md) — BB picker (each trail node declares a `building_block:`)

## Source plan

- `plans/plan_retrieval_port.md` — the port plan whose five waves this trail's synthesis arrived at

---

**Last Updated**: 2026-05-10
**Status**: Active — Retrieval trail (FZ 3) — 2 nodes, depth 2 (linear)
