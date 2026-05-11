---
tags:
  - area
  - code_repos
  - model
  - tessellum
  - architecture
keywords:
  - Tessellum repository structure
  - tessellum package layout
  - build system
  - hatch
  - PyPI distribution
  - seed vault manifest
topics:
  - Tessellum
  - Repository Architecture
  - Python Package Layout
language: markdown
date of note: 2026-05-11
status: active
building_block: model
bb_schema_version: 1
folgezettel: ""
folgezettel_parent: ""
---

# Repo: Tessellum

> **What this note is**: a `model`-typed note answering *how is Tessellum structured?* — its repository layout, runtime modules, build system, and the seed-vault-in-the-wheel discipline. Models are *relational structures*; this one decomposes Tessellum's repo into 8 first-class components and names how they compose.

## Architecture

```
Tessellum/
├── src/tessellum/        — the runtime package (shipped to PyPI)
│   ├── bb/               — BB ontology: BBType, BB_SCHEMA, BBGraph
│   ├── capture.py        — typed-template note creation
│   ├── cli/              — `tessellum <subcommand>` entry points
│   ├── composer/         — pipeline executor + LLM backends
│   ├── dks/              — Dialectic Knowledge System runtime
│   │   ├── core.py       — 7-component DKSCycle + DKSRunner
│   │   ├── dung.py       — Dung grounded labelling (Phase 10)
│   │   ├── fsm.py        — FSM dispatcher on BB_SCHEMA (Phase 8)
│   │   └── meta/         — meta-DKS schema-mutation runtime (Phase 9)
│   ├── format/           — YAML frontmatter + link validators (TESS-001..005)
│   ├── indexer/          — SQLite + FTS5 + sqlite-vec
│   ├── retrieval/        — hybrid BM25 + dense + graph
│   ├── mcp/              — MCP server (v0.1.0+, currently placeholder)
│   └── data/             — wheel-shipped templates + seed-vault manifest
├── vault/                — the dogfooded seed vault (force-included in wheel)
│   ├── 0_entry_points/   — navigation indices
│   ├── areas/            — ongoing structured systems (this note lives here)
│   ├── projects/         — timed deliverables
│   ├── resources/        — reference material (term_dictionary, papers, skills, …)
│   └── archives/         — inactive items
├── tests/                — pytest smoke + CLI tests
├── plans/                — markdown plan files
├── scripts/              — auxiliary scripts (curation, indexing)
└── .github/workflows/    — CI (ruff + pytest + format + build)
```

## Components

| Component | Module | Role | Phase shipped |
|---|---|---|---|
| **BB ontology** | `tessellum.bb` | Source of truth for the 8 BB types + 16-edge schema | v0.0.47 |
| **Capture** | `tessellum.capture` | Typed-template note creation; auto-populates `bb_schema_version` | v0.0.47 (B.4 v0.0.53) |
| **Composer** | `tessellum.composer` | Pipeline executor + Mock/Anthropic backends | v0.0.41+ |
| **Indexer** | `tessellum.indexer` | SQLite + FTS5 + sqlite-vec; one-file unified backend | v0.0.42+ |
| **Retrieval** | `tessellum.retrieval` | Hybrid BM25 + dense + best-first BFS over note_links | v0.0.43+ |
| **DKS** | `tessellum.dks` | 7-component closed-loop dialectic runtime + meta-DKS + Dung labelling | v0.0.40 – v0.0.54 |
| **Format** | `tessellum.format` | YAML + link validators (TESS-001..005); version-aware TESS-005 | v0.0.45+ (I.2 v0.0.55) |
| **CLI** | `tessellum.cli` | `tessellum dks / bb / capture / composer / format / fz / index / init / search` | v0.0.43+ |

The components are **peer modules**, not layered. DKS uses Composer's `LLMBackend` abstraction but isn't owned by Composer; meta-DKS uses BB's `BB_SCHEMA_AT_VERSION` helper but isn't owned by BB. The dependency graph is explicit in each module's `__init__.py`.

## Relationships

Three load-bearing inter-component flows:

1. **Capture writes; Indexer reads.** `tessellum.capture` produces typed atomic notes; `tessellum.indexer.build` reads the vault and emits the SQLite index. The vault is the single source of truth; the index is a *derived* artifact (R-P discipline — see [`thought_cqrs_r_cross_rules`](../../resources/analysis_thoughts/thought_cqrs_r_cross_rules.md), FZ 1a1b).
2. **DKS walks BB_SCHEMA.** Every DKS cycle's 7-component output instantiates exactly one BB-typed node per step (per Phase 8's D1 — subclass-per-BBType frozen dataclasses). The cycle's `_step_*` methods walk the schema graph; meta-DKS proposes additions to the user-extensions tuple.
3. **CLI dispatches everything.** `tessellum dks <jsonl>`, `tessellum bb audit`, `tessellum composer run <pipeline>`, etc. — every user-facing entry point lives in `src/tessellum/cli/`. Internal modules don't import from `cli/`; the dependency arrow points outward.

## Build system

| Aspect | Choice | Why |
|---|---|---|
| Build backend | `hatchling` | Modern PEP-517; supports `force-include` for the seed vault |
| Distribution | PyPI wheel + sdist | `pip install tessellum`; templates ship under `tessellum/data/templates/` |
| Optional extras | `[agent]`, `[mcp]`, `[papers]`, `[ingest]`, `[dev]` | Heavy/optional deps don't bloat the base install |
| Python versions | 3.11 + 3.12 (matrix-tested) | Modern type-hinting; matches CI matrix |
| CI | GitHub Actions: ruff + pytest + format-check + build | Every PR gets regression detection (v0.0.56) |
| Seed vault | Force-included into wheel at `tessellum/data/templates/` (templates) + per-file grafts via `hatch_build.py:SeedManifestHook` (seed notes) | `pip install tessellum` users get the canonical vault skeleton; `tessellum init` materialises it |

## Versioning

Tessellum follows semver, currently in 0.0.x alpha. Each minor version is one *phase* of the active plan (`plan_dks_expansion.md` Phases 6-10 → v0.0.48..54; `plan_meta_dks_validation_and_polish.md` V+B → v0.0.53; `plan_v01_completion_roadmap.md` Phases I-VI → v0.0.55..0.1.0). The phase mapping lets `__about__.py:__status__` carry a contribution summary for every release.

The 0 → 0.1.0 transition is the alpha → public-beta cut. After 0.1.0, the API contract tightens; before, internals can move freely.

## Why this note is `building_block: model`

| Field | This note | Contrast with `concept` |
|---|---|---|
| **Question answered** | *How is it structured?* | *What is it called?* |
| **Stance** | relational decomposition | atomic definition |
| **Content shape** | components + connections + workflows | term + heritage + when-to-use |
| **PARA bucket** | `area` (ongoing) — the repo is structurally maintained, not a one-off project | `resource` (reference) |
| **Default directory** | `areas/code_repos/` | `resources/term_dictionary/` |

A `concept` answers *"what does this name mean?"*; a `model` answers *"how do these pieces fit together?"*. The repo's structure isn't a definition — it's a composition. That makes it a model, not a concept.

## Related Notes

- [`term_format_spec`](../../resources/term_dictionary/term_format_spec.md) — the YAML frontmatter schema this repo's notes conform to (also `model`-typed; mislocation pending cleanup)
- [`thought_dks_runtime_integration`](../../resources/analysis_thoughts/thought_dks_runtime_integration.md) — FZ 2b, the runtime-integration argument grounded in this structure
- [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — uses this note as the canonical `model` exemplar

## See Also

- [`entry_master_toc`](../../0_entry_points/entry_master_toc.md) — vault's navigation root
- `pyproject.toml` — declarative source of the build system + extras

---

**Last Updated**: 2026-05-11
**Status**: Active — canonical `model` exemplar; describes Tessellum's own repository structure as a structured system
