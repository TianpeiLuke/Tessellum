# Tessellum

> **Typed atomic notes in a graph — a Zettelkasten that scales.**
>
> Knowledge construction for humans and agents, built on six architectural pillars: Zettelkasten, PARA, **Building Blocks**, **Epistemic Functions**, **Dialectic Knowledge System (DKS)**, and **CQRS**.

Tessellum is a knowledge-construction system, not an agent-memory store. The unit of work is a **typed atomic note** — a *tessellum*, a small mosaic tile — that carries one epistemic claim. You write tessellae; Tessellum indexes them, retrieves them with hybrid BM25 + vector search, lets you grow Folgezettel trails that record *how thinking developed*, and runs a closed-loop Dialectic Knowledge System that updates warrants from observed disagreement. The architecture is CQRS: a typed prescriptive substrate (what you author) and a computational descriptive retrieval layer (what queries return) — read-side and write-side cleanly separated.

## Status

**Current `main` — every engine subsystem shipped, including the Composer v4 dynamic-workflow engine and the v5 automatic runtime.** Suite: **1241 passing, 1 skipped**.

- **Composer** — a typed-contract pipeline runtime. Skill canonical (one self-contained markdown note — a typed contract block per step section) → zero-LLM compile → typed DAG → execute either **serially** (`run_pipeline`, the byte-identical reference path) or through the **v4 self-claiming, wave-parallel dynamic scheduler** (`run_pipeline_dynamic`, opt-in via `--dynamic`) with a resume manifest, a plan/session/wave gate engine, an error-class + full-jitter retry ladder, run-level budgets, a key-rotating credential pool, a fail-soft context assembler, and a pluggable sign-off approver. Four LLM backends: **Mock / Anthropic / Bedrock / Pooled**.
- **DKS** — a shipped closed-loop **Dialectic Knowledge System runtime engine** (`tessellum dks`): a 7-component cycle (observation → N arguments → contradicts edges → counter → pattern → revised warrant) over the Building-Block graph, multi-perspective Dung argumentation, confidence gating, warrant persistence, and a second-order **meta-DKS** that mutates the BB schema itself.
- **Retrieval** — BM25 (FTS5) + dense (sqlite-vec) + hybrid RRF + best-first BFS + metadata filter, over the indexed vault.
- **Indexer** — vault → one SQLite DB (notes + note_links + FTS5 + sqlite-vec, `all-MiniLM-L6-v2` 384-d).
- **Format** — closed-enum YAML validator + parser + BB-graph-aware link checker. **BB** — the 8-type, versioned, event-sourced ontology (source of truth).
- **Automatic runtime** — durable inbox admission, content-addressed spooling, leased supervision, verified Composer resume, conflict-safe vault rollback, cancellation/retry/dead-letter handling, commit-only crash recovery, atomic index publication, and replayable source acknowledgement (`tessellum runtime serve`).
- **Interfaces** — a 12-command CLI (`init / format / capture / index / search / filter / fz / bb / composer / dks / mcp / runtime`) and a **shipped MCP stdio server** (`tessellum mcp serve`, 12 tools).

See [CHANGELOG](CHANGELOG.md) for the per-release ship list, and **[`docs/`](docs/)** for the architecture + per-module design reference.

## The Six Pillars

| # | Pillar | What it gives you | Term note |
|---|---|---|---|
| 1 | **Z** — Zettelkasten | Atomic notes, bidirectional links — Luhmann's method that scaled to ~90k connected ideas | [term_zettelkasten](vault/resources/term_dictionary/term_zettelkasten.md) |
| 2 | **PARA** — Projects/Areas/Resources/Archives | Tiago Forte's organizational scheme; four-fold structure that survives growth | [term_para_method](vault/resources/term_dictionary/term_para_method.md) |
| 3 | **BB** — Building Block | 8 typed atomic units with defining epistemic functions; a versioned, event-sourced schema graph (~16 typed edges) drives the dialectic cycle | [term_building_block](vault/resources/term_dictionary/term_building_block.md) |
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
| **RAG framework** (LangChain / LlamaIndex) | Retrieval is hybrid BM25 + vector (RRF) + best-first BFS + metadata filter over a *typed* graph. Notes are typed atoms, not opaque chunks |

## Quick Start

```bash
pip install tessellum

# 1. Scaffold a new vault (templates + seed term + master TOC)
tessellum init ~/my-vault
cd ~/my-vault

# 2. Capture your first typed atomic note — 14 flavors available
tessellum capture concept page_rank --vault .        # creates resources/term_dictionary/term_page_rank.md
tessellum capture skill my_skill --vault .           # creates a single self-contained skill_*.md
tessellum capture code_snippet my_algo --vault .     # creates resources/code_snippets/snippet_*.md
tessellum capture code_repo my_repo --vault .        # creates areas/code_repos/repo_*.md
tessellum capture --help                   # full flavor list

# 3. Validate format (closed-enum YAML spec)
tessellum format check .

# 4. Index the vault (notes + links + FTS5 + sentence-transformer embeddings)
tessellum index build --vault .

# 5. Retrieve — hybrid RRF default; --bm25 / --dense / --bfs for explicit strategy
tessellum search "graph traversal"
tessellum search --bm25 "PageRank"          # lexical only
tessellum search --bfs term_page_rank.md    # graph traversal from a seed
tessellum filter --tag concept --building-block model   # direct metadata filter

# 6. Compose — typed-contract runtime for skill-driven workflows
tessellum composer validate resources/skills/                                 # all skills
tessellum composer compile  resources/skills/skill_my_skill.md                # typed DAG, zero LLM
tessellum composer run resources/skills/skill_my_skill.md --vault .           # serial mock backend
tessellum composer run resources/skills/skill_my_skill.md --vault . --backend anthropic
tessellum composer run resources/skills/skill_my_skill.md --vault . --backend bedrock
tessellum composer run resources/skills/skill_my_skill.md --vault . --dynamic --workers 8 \
    --manifest run.json --close-gate --wave-gate --max-invocations 200
tessellum composer batch    jobs.json --parallelism 8                        # parallel multi-skill
tessellum composer eval     scenarios/  --judge-backend anthropic            # structural assertions + LLMJudge rubric

# 7. DKS — run the Dialectic Knowledge System engine over observations
tessellum dks observations.jsonl --perspectives a,b,c                        # multi-cycle dialectic (N>2 → Dung)
tessellum dks --report                                                       # inter-cycle telemetry
tessellum dks --meta --apply                                                 # second-order: mutate the BB schema

# 8. Run automatic inbox digestion
tessellum runtime init
tessellum runtime serve --backend anthropic                                 # scan, lease, digest, commit

# 9. Serve tools to an agent over MCP (pip install tessellum[mcp])
tessellum mcp serve                                                          # stdio server, 12 tools
```

`tessellum --version` prints the version; bare `tessellum` prints the capability banner.

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
                    │  data/tessellum.db (one .db file)    │
                    │  SQLite + sqlite-vec + FTS5          │
                    └──────────────────┬───────────────────┘
                                       │ queried
                                       ▼
                    ┌──────────────────────────────────────┐
                    │  src/tessellum/retrieval/            │
                    │  System D — descriptive retrieval    │
                    │   • Hybrid BM25 + vector via RRF     │
                    │   • Best-first BFS + metadata filter │
                    └──────────────────┬───────────────────┘
                                       │ exposed
                                       ▼
                    ┌──────────────────────────────────────┐
                    │  Interfaces + runtimes               │
                    │   • CLI (12 cmds): init/format/      │
                    │     capture/index/search/filter/fz/  │
                    │     bb/composer/dks/mcp/runtime      │
                    │   • Composer v4: skill canonicals →  │
                    │     typed DAGs, serial or --dynamic  │
                    │     self-claiming scheduler;         │
                    │     backends Mock/Anthropic/Bedrock  │
                    │   • DKS engine: closed-loop dialectic│
                    │     over the BB graph (+ meta-DKS)   │
                    │   • MCP stdio server (shipped, 12    │
                    │     tools) + a composer-ts/ bridge   │
                    └──────────────────────────────────────┘
```

See [vault/resources/analysis_thoughts/thought_six_pillars_architecture.md](vault/resources/analysis_thoughts/thought_six_pillars_architecture.md) for the full pillar-by-pillar deep dive.

## The Building Block Ontology

Every tessellum has a `building_block` field in YAML frontmatter — one of 8 typed roles, each with a defining epistemic function. The typed edges between roles form a versioned, event-sourced schema graph (~16 edges: 8 epistemic + 7 navigation-index + 1 DKS extension) — the source of truth is `src/tessellum/bb/`, and the second-order meta-DKS can mutate it. This ontology drives the Dialectic Knowledge System. See [vault/resources/term_dictionary/term_building_block.md](vault/resources/term_dictionary/term_building_block.md) and [docs/bb.md](docs/bb.md).

## Folgezettel Trails

Wikilinks tell you what's *related*. Folgezettel trails tell you *how thinking developed* — argument → counter → response → reframe → synthesis, encoded in trail IDs (`7 → 7a → 7a1 → 7a1a`). See [vault/resources/term_dictionary/term_folgezettel.md](vault/resources/term_dictionary/term_folgezettel.md).

## Project Structure

The top-level layout maps each folder to a defined CQRS role — System P (capture), System D (retrieval), or governance/runtime that sits outside both. See [`plans/plan_cqrs_repo_layout.md`](plans/plan_cqrs_repo_layout.md) for the full workflow → folder mapping.

```
Tessellum/
├── src/tessellum/         Python code — engines for System P (capture) and System D (retrieval)
│   ├── bb/                Building Block ontology — 8-type, versioned, event-sourced schema graph (source of truth)
│   ├── format/            Validator + parser + BB-graph-aware link checker (closed-enum YAML spec)
│   ├── indexer/           Vault → one SQLite DB (notes + note_links + FTS5 + sqlite-vec; all-MiniLM-L6-v2 384-d)
│   ├── retrieval/         BM25 + dense + hybrid RRF + best-first BFS + metadata filter (+ heuristic router)
│   ├── composer/          Composer v4 runtime — compiler + scheduler (serial run_pipeline + dynamic
│   │                      run_pipeline_dynamic) + executor (retry ladder) + manifest + gates + fix +
│   │                      credential_pool + context_assembler + planning + signoff + llm
│   │                      (Mock/Anthropic/Bedrock/Pooled) + batch + eval
│   ├── dks/               Dialectic Knowledge System engine — core + fsm + dung + confidence + persistence + meta/
│   ├── runtime/           Durable automatic inbox queue, routing, leased supervisor, commit tail, and tool broker
│   ├── capture.py         14-flavor capture registry (concept, procedure, skill, model, argument,
│   │                      counter_argument, hypothesis, empirical_observation, experiment,
│   │                      navigation, entry_point, acronym_glossary, code_snippet, code_repo)
│   ├── init.py            tessellum init scaffold
│   ├── cli/               Per-subcommand dispatchers (12 commands) wired into argparse
│   ├── mcp/               Shipped MCP stdio server (12 tools) — `tessellum mcp serve`
│   └── data/              Force-included template directory + seed-vault content
├── composer-ts/           TypeScript orchestration bridge (bridge-not-port; shells the Python CLI)
├── docs/                  Architecture + per-module design reference
├── vault/                 Shared substrate — typed atomic notes (Tessellum dogfoods itself)
│   ├── 0_entry_points/    Master TOC + 5 acronym glossaries (statistics, critical thinking,
│   │                      cognitive science, network science, LLMs) + master glossary index
│   ├── resources/
│   │   ├── term_dictionary/   Conceptual primer (BB, FZ, DKS, CQRS, Z, PARA, …)
│   │   ├── how_to/            How-to guides
│   │   ├── analysis_thoughts/ Architecture arguments + FZ trails
│   │   ├── templates/         15 copy-and-fill skeletons (executable spec exemplars)
│   │   ├── skills/            Self-contained skill canonicals (per-step contract blocks inline)
│   │   ├── code_snippets/     `## Patterns`-format snippet notes (one component or algorithm)
│   │   ├── code_repos/        Repo notes (main + sub-note structure)
│   │   ├── teams/   tools/   faqs/   digest/   papers/
│   └── areas/             Code-repo notes (main + module sub-notes)
├── inbox/                 System P input queue — drop zone for raw incoming (papers, drafts)
├── plans/                 Governance — project-management plans (committed, top-level)
├── data/                  System D build output (gitignored, regenerable: DBs + embeddings)
├── runs/                  Both-system runtime traces (gitignored)
│   ├── capture/           Capture-pipeline traces (reserved; not yet wired)
│   ├── retrieval/         Retrieval evaluation + benchmark traces (reserved; not yet wired)
│   ├── composer/          Composer chain run traces (wired by `tessellum composer run/batch`)
│   └── runtime/           Durable jobs, content-addressed spool, artifacts, and source archive
├── experiments/           Experiment outputs
├── scripts/               Operational utilities (one-off migrations; not in wheel)
└── tests/                 Test suite (1241 passing, 1 skipped)
```

**Two documentation surfaces, by audience.** [`docs/`](docs/) is the **engineering reference** — the system architecture and a per-module design doc (runtime, composer, dks, retrieval, indexer, bb, format, cli, mcp) for contributors reading the code. [`vault/`](vault/) is the **knowledge documentation** — Tessellum dogfoods itself, so its concepts, how-tos, and design arguments live as typed atomic notes; start at [`vault/0_entry_points/entry_master_toc.md`](vault/0_entry_points/entry_master_toc.md). See [DEVELOPING.md](DEVELOPING.md) for the rationale.

## Compared to Adjacent Tools

| | Tessellum | Obsidian | palinode | Mem0 |
|---|---|---|---|---|
| Typed atomic notes (8 BB types) | ✅ | — | partial (5) | — |
| Folgezettel trails | ✅ | manual | — | — |
| Dialectic / counters as first-class | ✅ | — | — | — |
| CQRS read/write split | ✅ | — | — | — |
| Hybrid BM25 + vector retrieval | ✅ | plugin | ✅ | proprietary |
| MCP server | ✅ (12 tools) | plugin | ✅ | — |
| Closed-loop dialectic compaction | ✅ (DKS) | — | partial (5 ops) | — |
| Typed-contract pipeline runtime | ✅ (Composer) | — | — | — |
| Knowledge-construction (vs storage) | ✅ | — | — | — |

## License

[MIT](LICENSE) — use freely, contribute back.

## Origin

Tessellum is the public release of a typed-knowledge system originally developed inside a production research vault. The architecture (BB ontology, Folgezettel trails, DKS protocol, CQRS thesis) was discovered through ~14 long-running Folgezettel research trails over 2024–2026.

The name **Tessellum** is Latin: *small mosaic tile* — the atomic typed unit. A vault is the mosaic.

## Acknowledgments

- The **Zettelkasten community** (especially Sascha Fast at zettelkasten.de) for the Building Block taxonomy this work builds on
- **Niklas Luhmann** for proving typed atomic notes scale to ~90k connected ideas
- **Tiago Forte** for the PARA scheme
- The **Phasespace-Labs / palinode** project for independently validating the SQLite + sqlite-vec + FTS5 + RRF stack
- CQRS architects (Greg Young, Udi Dahan) for the read/write split applied here to typed knowledge
