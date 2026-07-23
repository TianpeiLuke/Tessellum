# Tessellum — Engineering Documentation

The architecture + per-module design reference for contributors reading the **Tessellum 1.0.0** code.

> **Two documentation surfaces, by audience.** This `docs/` tree is the *engineering* reference — how the
> code is built and why. The [`vault/`](../vault/) is the *knowledge* documentation — Tessellum dogfoods
> itself, so its concepts, how-tos, and design arguments live as typed atomic notes (start at
> [`vault/0_entry_points/entry_master_toc.md`](../vault/0_entry_points/entry_master_toc.md)).

## Start here

- **[architecture.md](architecture.md)** — the system: the CQRS split (System P = the markdown `vault/`
  substrate; System D = the SQLite DB + retrieval, one-way P→D), the subsystem map and data flow, the memory
  model (vault = source of truth, DB = derived projection, resume manifest = rebuildable projection), the
  Composer v4 and DKS engines at a glance, the load-bearing `IDENT-2..5` invariants, and the `composer-ts/`
  TypeScript bridge.

## Modules

| Doc | Module | What it covers |
|---|---|---|
| [composer.md](composer.md) | `src/tessellum/composer/` | The v4 typed-contract pipeline runtime: compile (zero-LLM) → schedule (serial `run_pipeline` vs the opt-in self-claiming `run_pipeline_dynamic`) → execute (retry ladder + watchdog) → gate → fix → sign-off → observe; the resume manifest, run budgets, credential pool / `PooledBackend`, context assembler, planning pre-gate, the four LLM backends, and the `IDENT-4` serial-parity invariant. |
| [dks.md](dks.md) | `src/tessellum/dks/` | The Dialectic Knowledge System engine: the 7-component closed-loop cycle over the BB graph, the three terminal shapes, multi-perspective Dung argumentation, warrant persistence, the FSM re-expression, and the second-order **meta-DKS** that mutates the BB schema. |
| [retrieval.md](retrieval.md) | `src/tessellum/retrieval/` | The five stateless read surfaces — BM25, dense, hybrid (RRF), best-first BFS, metadata filter — plus the heuristic router. (No PageRank; that is an explicit design decision.) |
| [indexer.md](indexer.md) | `src/tessellum/indexer/` | The vault → one SQLite DB build (notes, note_links, FTS5, sqlite-vec); rebuild-from-scratch semantics, the embedding model, and the `--no-dense` fast path. |
| [bb.md](bb.md) | `src/tessellum/bb/` | The Building Block ontology: the 8 types and ~16 typed edges, the versioned + event-sourced schema graph, and the corpus (`BBGraph`) view. |
| [format.md](format.md) | `src/tessellum/format/` | The closed-enum YAML validator/parser + BB-graph-aware link checker that enforces the ontology on every note. |
| [cli.md](cli.md) | `src/tessellum/cli/` | The 11-command CLI surface and its exit-code contract. |
| [mcp.md](mcp.md) | `src/tessellum/mcp/` | The shipped MCP stdio server (7 tools) — the skills-as-tools front door for agents. |

## Conventions

- Every claim in these docs is grounded in the source (cited `module:symbol`) and was adversarially
  accuracy-checked against the code.
- When code and docs diverge, the **code is truth** — open an issue or PR against the doc.
