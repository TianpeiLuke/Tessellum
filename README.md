# Tessellum

> **Typed atomic notes in a graph — a Zettelkasten that scales.**
>
> Knowledge construction for humans and agents, built on six architectural pillars: Zettelkasten, PARA, **Building Blocks**, **Epistemic Functions**, **Dialectic Knowledge System (DKS)**, and **CQRS**.

Tessellum is a knowledge-construction system, not an agent-memory store. The unit of work is a **typed atomic note** — a *tessellum*, a small mosaic tile — that carries one epistemic claim. You write tessellae; Tessellum indexes them, retrieves them with hybrid BM25 + vector search, lets you grow Folgezettel trails that record *how thinking developed*, and runs a closed-loop Dialectic Knowledge System that updates warrants from observed disagreement. The architecture is CQRS: a typed prescriptive substrate (what you author) and a computational descriptive retrieval layer (what queries return) — read-side and write-side cleanly separated.

## Status

**v0.0.27 — alpha, all v0.1 engine subsystems shipped.** Composer (capture → compile → execute → real LLM → batch → eval), Retrieval (BM25 + dense + hybrid RRF + best-first BFS + metadata filter), Format library (validator + parser + link checker), Capture (14 flavors), Indexer (unified SQLite + FTS5 + sqlite-vec), and Init (vault scaffold).

What's still pending for v0.1.0 (no engine work remaining — content only): 20 essential authored skills, 8 BB-type worked examples, the conceptual primer term notes (Z + PARA + BB + EF + DKS + CQRS, all defined as term notes), and a how-to library. Engine plans complete: see [`plans/plan_composer_port.md`](plans/plan_composer_port.md), [`plans/plan_retrieval_port.md`](plans/plan_retrieval_port.md), [`plans/plan_v01_src_tessellum_layout.md`](plans/plan_v01_src_tessellum_layout.md), [`plans/plan_cqrs_repo_layout.md`](plans/plan_cqrs_repo_layout.md), [`plans/plan_code_artifacts_port.md`](plans/plan_code_artifacts_port.md). See [CHANGELOG](CHANGELOG.md) for the per-release ship list.

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

# 1. Scaffold a new vault (templates + seed term + master TOC)
tessellum init ~/my-vault
cd ~/my-vault

# 2. Capture your first typed atomic note — 14 flavors available
tessellum capture concept page_rank        # creates resources/term_dictionary/term_page_rank.md
tessellum capture skill my_skill           # creates skill_*.md + paired skill_*.pipeline.yaml
tessellum capture code_snippet my_algo     # creates resources/code_snippets/snippet_*.md
tessellum capture code_repo my_repo        # creates areas/code_repos/repo_*.md
tessellum capture --help                   # full flavor list

# 3. Validate format (closed-enum YAML spec)
tessellum format check .

# 4. Index the vault (notes + links + FTS5 + sentence-transformer embeddings)
tessellum index build

# 5. Retrieve — hybrid RRF default; --bm25 / --dense / --bfs for explicit strategy
tessellum search "graph traversal"
tessellum search --bm25 "PageRank"          # lexical only
tessellum search --bfs term_page_rank.md    # graph traversal from a seed
tessellum filter --tag concept --bb model   # direct metadata filter (tags / BB / status / dates)

# 6. Compose — runtime for skill-driven workflows
tessellum composer validate vault/resources/skills/                          # all skills
tessellum composer compile  vault/resources/skills/skill_my_skill.md         # to typed DAG
tessellum composer scaffold-sidecar  skill_existing.md                       # generate sidecar from canonical's anchors
tessellum composer run      vault/resources/skills/skill_my_skill.md         # mock backend
tessellum composer run      skill_my_skill.md --backend anthropic            # real Claude (pip install tessellum[agent])
tessellum composer batch    jobs.json --parallelism 8                        # parallel multi-skill
tessellum composer eval     scenarios/  --judge-backend anthropic            # structural assertions + LLMJudge rubric
```

`tessellum --version` prints the version + capability banner.

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
                    │   • CLI: `tessellum {init,capture,   │
                    │     format,index,search,filter,      │
                    │     composer}` (shipped)             │
                    │   • Composer runtime: typed-contract │
                    │     skill canonicals → typed DAGs    │
                    │     dispatched through Mock or       │
                    │     Anthropic backend (shipped)      │
                    │   • MCP server (deferred — add when  │
                    │     a Tessellum user needs it)       │
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
├── src/tessellum/         Python code — engines for both System P (capture) and System D (retrieval)
│   ├── format/            Validator + parser + link checker (closed-enum YAML spec)
│   ├── indexer/           Vault → SQLite unified backend (notes + note_links + FTS5 + sqlite-vec)
│   ├── retrieval/         BM25 + dense + hybrid RRF + best-first BFS + metadata filter + router
│   ├── composer/          Loader + compiler + executor + scheduler + materializers + LLM (mock / Anthropic) + batch + eval
│   ├── capture.py         14-flavor capture registry (concept, procedure, skill, model, argument,
│   │                      counter_argument, hypothesis, empirical_observation, experiment,
│   │                      navigation, entry_point, acronym_glossary, code_snippet, code_repo)
│   ├── init.py            tessellum init scaffold
│   ├── cli/               Per-subcommand dispatchers wired into argparse
│   └── data/              Force-included template directory + seed-vault content
├── vault/                 Shared substrate — typed atomic notes (Tessellum dogfoods itself)
│   ├── 0_entry_points/    Master TOC + 5 acronym glossaries (statistics, critical thinking,
│   │                      cognitive science, network science, LLMs) + master glossary index
│   ├── resources/
│   │   ├── term_dictionary/   Conceptual primer (BB, FZ, DKS, CQRS, Z, PARA, …)
│   │   ├── how_to/            How-to guides
│   │   ├── analysis_thoughts/ Architecture arguments + FZ trails
│   │   ├── templates/         15 copy-and-fill skeletons (executable spec exemplars)
│   │   ├── skills/            Skill canonical bodies + pipeline sidecars
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
│   └── composer/          Composer chain run traces (wired by `tessellum composer run/batch`)
├── experiments/           Experiment outputs
├── scripts/               Operational utilities (one-off migrations; not in wheel)
└── tests/                 Test suite (~468 passing as of v0.0.27)
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
| MCP server | deferred | plugin | ✅ | — |
| Closed-loop dialectic compaction | ✅ (DKS) | — | partial (5 ops) | — |
| Typed-contract pipeline runtime | ✅ (Composer) | — | — | — |
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
