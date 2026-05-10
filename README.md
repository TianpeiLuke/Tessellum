# Tessellum

> **Typed atomic notes in a graph — a Zettelkasten that scales.**
>
> Knowledge construction for humans and agents, built on six architectural pillars: Zettelkasten, PARA, **Building Blocks**, **Epistemic Functions**, **Dialectic Knowledge System (DKS)**, and **CQRS**.

Tessellum is a knowledge-construction system, not an agent-memory store. The unit of work is a **typed atomic note** — a *tessellum*, a small mosaic tile — that carries one epistemic claim. You write tessellae; Tessellum indexes them, retrieves them with hybrid BM25 + vector search, lets you grow Folgezettel trails that record *how thinking developed*, and runs a closed-loop Dialectic Knowledge System that updates warrants from observed disagreement. The architecture is CQRS: a typed prescriptive substrate (what you author) and a computational descriptive retrieval layer (what queries return) — read-side and write-side cleanly separated.

## Status

**v0.0.1 — namespace reservation.** Repository skeleton + this README. The v0.1 user-facing release ships the engine port + 20 essential skills + 8 BB-type example notes. See [CHANGELOG](CHANGELOG.md).

## The Six Pillars

| # | Pillar | What it gives you | Term note |
|---|---|---|---|
| 1 | **Z** — Zettelkasten | Atomic notes, bidirectional links — Luhmann's method that scaled to ~90k connected ideas | [term_zettelkasten](vault/resources/term_dictionary/term_zettelkasten.md) |
| 2 | **PARA** — Projects/Areas/Resources/Archives | Tiago Forte's organizational scheme; four-fold structure that survives growth | [term_para_method](vault/resources/term_dictionary/term_para_method.md) |
| 3 | **BB** — Building Block | 8 typed atomic units with defining epistemic functions; 10 directed edges form the dialectic cycle | [term_building_block](vault/resources/term_dictionary/term_building_block.md) |
| 4 | **EF** — Epistemic Function | Each BB has a *function* — name / structure / predict / claim / refute / observe / act / index | [term_epistemic_function](vault/resources/term_dictionary/term_epistemic_function.md) |
| 5 | **DKS** — Dialectic Knowledge System | Closed-loop protocol — arguments attract counters, counters absorbed by syntheses, warrants update from observed disagreement | [term_dialectic_knowledge_system](vault/resources/term_dictionary/term_dialectic_knowledge_system.md) |
| 6 | **CQRS** — Read/Write Split | System P (typed substrate, prescriptive — what you author) ⊥ System D (retrieval, descriptive — what queries return) | [term_cqrs](vault/resources/term_dictionary/term_cqrs.md) |

**Two supporting concepts** that bridge the pillars (also shipped as term notes):

| Concept | What it does | Term note |
|---|---|---|
| **Slipbox** | The system class — a typed atomic-note vault with a graph layer; Tessellum is one Slipbox implementation | [term_slipbox](vault/resources/term_dictionary/term_slipbox.md) |
| **Folgezettel** | The trail mechanism — alphanumeric IDs encode argument descent (1 → 1a → 1a1) so the graph remembers *how thinking developed*, not just *what relates* | [term_folgezettel](vault/resources/term_dictionary/term_folgezettel.md) |

## What Tessellum Is *Not*

| | Tessellum |
|---|---|
| **Note app** (Obsidian / Notion / Roam) | Tessellum *constructs* knowledge — typed atomicity, dialectic, CQRS — not just stores it |
| **Agent memory** (Mem0 / Letta / palinode) | Tessellum is a typed knowledge system. Memory tools focus on per-session recall; Tessellum focuses on **epistemic structure** |
| **Knowledge graph** (Neo4j / Stardog) | The graph emerges from typed wikilinks and Folgezettel trails. You write atomic markdown, not Cypher |
| **RAG framework** (LangChain / LlamaIndex) | Retrieval is hybrid BM25 + vector + PageRank + best-first BFS over a *typed* graph. Notes are typed atoms, not opaque chunks |

## Quick Start

```bash
pip install tessellum
tessellum init ~/my-vault
tessellum capture term "PageRank" --as concept
tessellum index --vault ~/my-vault
tessellum search "graph traversal"
tessellum answer "what is the difference between PageRank and PPR?"
```

## Architecture

```
                    ┌──────────────────────────────────────┐
                    │  vault/  (markdown + YAML)           │
                    │  System P — typed substrate          │
                    │   • 8 BB types × ~80 sub-kinds       │
                    │   • PARA categories                  │
                    │   • Folgezettel trails               │
                    └──────────────────┬───────────────────┘
                                       │ indexed
                                       ▼
                    ┌──────────────────────────────────────┐
                    │  data/databases/   (one .db file)    │
                    │  SQLite + sqlite-vec + FTS5          │
                    └──────────────────┬───────────────────┘
                                       │ queried
                                       ▼
                    ┌──────────────────────────────────────┐
                    │  src/tessellum/retrieval/            │
                    │  System D — descriptive retrieval    │
                    │   • Hybrid BM25 + vector via RRF     │
                    │   • PPR / Best-First BFS             │
                    │   • BB-aware re-ranking              │
                    └──────────────────┬───────────────────┘
                                       │ exposed
                                       ▼
                    ┌──────────────────────────────────────┐
                    │  Interfaces                          │
                    │   • CLI: `tessellum search/answer`   │
                    │   • MCP server (any MCP client)      │
                    │   • Composer pipeline (typed-contract│
                    │     knowledge auto-digestion)        │
                    └──────────────────────────────────────┘
```

See [vault/resources/analysis_thoughts/thought_six_pillars_architecture.md](vault/resources/analysis_thoughts/thought_six_pillars_architecture.md) for the full pillar-by-pillar deep dive.

## The Building Block Ontology

Every tessellum has a `building_block` field in YAML frontmatter — one of 8 typed roles, each with a defining epistemic function. The directed edges between types form a 10-edge epistemic ontology that drives the Dialectic Knowledge System. See [vault/resources/term_dictionary/term_building_block.md](vault/resources/term_dictionary/term_building_block.md).

## Folgezettel Trails

Wikilinks tell you what's *related*. Folgezettel trails tell you *how thinking developed* — argument → counter → response → reframe → synthesis, encoded in trail IDs (`7 → 7a → 7a1 → 7a1a`). See [vault/resources/term_dictionary/term_folgezettel.md](vault/resources/term_dictionary/term_folgezettel.md).

## Project Structure

The top-level layout maps each folder to a defined CQRS role — System P (capture), System D (retrieval), or governance/runtime that sits outside both. See [`plans/plan_cqrs_repo_layout.md`](plans/plan_cqrs_repo_layout.md) for the full workflow → folder mapping.

```
Tessellum/
├── src/tessellum/      Python code — engines for both System P (capture) and System D (retrieval)
├── vault/              Shared substrate — typed atomic notes (Tessellum dogfoods itself)
│   ├── 0_entry_points/ Master TOC + per-surface entries
│   ├── resources/
│   │   ├── term_dictionary/   Conceptual primer (BB, FZ, DKS, CQRS, Z, PARA, …)
│   │   ├── how_to/            How-to guides
│   │   ├── analysis_thoughts/ Architecture arguments + FZ trails
│   │   ├── templates/         Copy-and-fill skeletons (executable spec exemplars)
│   │   └── skills/            Skill canonical bodies + pipeline sidecars
│   └── examples/       One worked example per Building Block type
├── inbox/              System P input queue — drop zone for raw incoming (papers, drafts)
├── plans/              Governance — project-management plans (committed, top-level)
├── data/               System D build output (gitignored, regenerable: DBs + embeddings)
├── runs/               Both-system runtime traces (gitignored)
│   ├── capture/        Capture-pipeline traces
│   ├── retrieval/      Retrieval evaluation + benchmark traces
│   └── composer/       DKS chain run traces
├── experiments/        Experiment outputs
├── scripts/            Operational utilities
└── tests/              Test suite
```

**No separate `docs/` directory** — Tessellum's own documentation IS a typed-knowledge vault. Start at [`vault/0_entry_points/entry_master_toc.md`](vault/0_entry_points/entry_master_toc.md). See [DEVELOPING.md](DEVELOPING.md) for the rationale.

## Compared to Adjacent Tools

| | Tessellum | Obsidian | palinode | Mem0 |
|---|---|---|---|---|
| Typed atomic notes (8 BB types) | ✅ | — | partial (5) | — |
| Folgezettel trails | ✅ | manual | — | — |
| Dialectic / counters as first-class | ✅ | — | — | — |
| CQRS read/write split | ✅ | — | — | — |
| Hybrid BM25 + vector retrieval | ✅ | plugin | ✅ | proprietary |
| MCP server | v0.1 | plugin | ✅ | — |
| Closed-loop dialectic compaction | ✅ (DKS) | — | partial (5 ops) | — |
| Knowledge-construction (vs storage) | ✅ | — | — | — |

## License

[MIT](LICENSE) — use freely, contribute back.

## Origin

Tessellum is the public release of the typed-knowledge system originally developed inside Amazon's buyer-abuse-prevention research vault. The architecture (BB ontology, Folgezettel trails, DKS protocol, CQRS thesis) was discovered through ~14 long-running Folgezettel research trails over 2024–2026.

The name **Tessellum** is Latin: *small mosaic tile* — the atomic typed unit. A vault is the mosaic.

## Acknowledgments

- The **Zettelkasten community** (especially Sascha Fast at zettelkasten.de) for the Building Block taxonomy this work builds on
- **Niklas Luhmann** for proving typed atomic notes scale to ~90k connected ideas
- **Tiago Forte** for the PARA scheme
- The **Phasespace-Labs / palinode** project for independently validating the SQLite + sqlite-vec + FTS5 + RRF stack
- CQRS architects (Greg Young, Udi Dahan) for the read/write split applied here to typed knowledge
