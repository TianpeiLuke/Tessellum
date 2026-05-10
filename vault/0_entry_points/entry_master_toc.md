---
tags:
  - entry_point
  - navigation
  - master_toc
  - tessellum
keywords:
  - master TOC
  - start here
  - tessellum vault
  - navigation
topics:
  - Navigation
  - Vault Entry
language: markdown
date of note: 2026-05-09
status: active
building_block: navigation
---

# Tessellum — Master Table of Contents

> **You are inside a Tessellum vault.** Tessellum dogfoods itself: the project's own documentation lives here, as typed atomic notes following the same Building Block format the system asks of users.
>
> This is the entry point. Pick a path below.

---

## I'm new — where do I start?

| If you want to... | Read |
|---|---|
| Understand what Tessellum is in 5 minutes | [`thought_six_pillars_architecture.md`](../resources/analysis_thoughts/thought_six_pillars_architecture.md) — the six-pillar thesis (Z + PARA + BB + Epistemic + DKS + CQRS) |
| Install and try it | [`howto_getting_started.md`](../resources/how_to/howto_getting_started.md) — install + init vault + first capture + first query |
| Understand the typed substrate | [`term_building_block.md`](../resources/term_dictionary/term_building_block.md) — the 8 BB types + 10 directed edges |
| Author your first note | [`howto_note_format.md`](../resources/how_to/howto_note_format.md) — YAML frontmatter spec + per-BB section requirements |
| Plug Tessellum into Claude Code / Cursor / etc. | [`howto_agent_integration.md`](../resources/how_to/howto_agent_integration.md) — MCP setup recipes |

---

## Conceptual Primer (the 6 pillars)

The architecture rests on six load-bearing concepts. Read all six to understand *why* Tessellum is shaped this way:

| # | Pillar | Term note |
|---|---|---|
| 1 | Zettelkasten | [`term_zettelkasten.md`](../resources/term_dictionary/term_zettelkasten.md) |
| 2 | PARA — Projects/Areas/Resources/Archives | [`term_para_method.md`](../resources/term_dictionary/term_para_method.md) |
| 3 | Building Block ontology | [`term_building_block.md`](../resources/term_dictionary/term_building_block.md) |
| 4 | Epistemic Function | [`term_epistemic_function.md`](../resources/term_dictionary/term_epistemic_function.md) |
| 5 | Dialectic Knowledge System (DKS) | [`term_dialectic_knowledge_system.md`](../resources/term_dictionary/term_dialectic_knowledge_system.md) |
| 6 | CQRS — read/write separation | [`term_cqrs.md`](../resources/term_dictionary/term_cqrs.md) |

---

## How-To Library

| Procedure | Note |
|---|---|
| Get started (install, init, first capture, first query) | [`howto_getting_started.md`](../resources/how_to/howto_getting_started.md) |
| Author a typed atomic note (YAML + sections by BB type) | [`howto_note_format.md`](../resources/how_to/howto_note_format.md) |
| Grow a Folgezettel trail (argument descent) | [`howto_grow_a_trail.md`](../resources/how_to/howto_grow_a_trail.md) |
| Wire Tessellum into Claude Code / Cursor / OpenClaw / Kiro | [`howto_agent_integration.md`](../resources/how_to/howto_agent_integration.md) |
| Build the unified DB from scratch | [`howto_build_unified_db.md`](../resources/how_to/howto_build_unified_db.md) |

---

## Entry Points by Surface

Each entry point indexes one type of content:

| Entry point | Indexes |
|---|---|
| [`entry_skill_catalog.md`](entry_skill_catalog.md) | The 20 v0.1 skills — capture, search, answer, trail management, maintenance |
| [`entry_folgezettel_trails.md`](entry_folgezettel_trails.md) | All Folgezettel trails in this vault |
| [`entry_code_repos.md`](entry_code_repos.md) | Code-repository documentation notes |
| [`entry_code_snippets.md`](entry_code_snippets.md) | Reusable code snippets (master TOC pointing at per-package entries) |
| [`entry_dks.md`](entry_dks.md) | The Dialectic Knowledge System — protocol, agents, runtime |

---

## Examples (one per Building Block type)

Read these to see the format Tessellum asks of you:

| BB Type | Example |
|---|---|
| `concept` | [`example_concept_pagerank.md`](../examples/example_concept_pagerank.md) |
| `procedure` | [`example_procedure_unified_db_build.md`](../examples/example_procedure_unified_db_build.md) |
| `model` | [`example_model_typed_substrate.md`](../examples/example_model_typed_substrate.md) |
| `argument` | [`example_argument_cqrs_thesis.md`](../examples/example_argument_cqrs_thesis.md) |
| `counter_argument` | [`example_counter_palinode_memory.md`](../examples/example_counter_palinode_memory.md) |
| `hypothesis` | [`example_hypothesis_dense_dominance.md`](../examples/example_hypothesis_dense_dominance.md) |
| `empirical_observation` | [`example_empirical_hybrid_lift.md`](../examples/example_empirical_hybrid_lift.md) |
| `navigation` | [`example_navigation_entry_point.md`](../examples/example_navigation_entry_point.md) |

---

## Status

Tessellum is **v0.0.1 (alpha — namespace reservation)**. Many of the notes linked above are **planned for v0.1** — this Master TOC describes the *target* shape of the vault. Notes already shipped in v0.0.1:

- [`term_building_block.md`](../resources/term_dictionary/term_building_block.md) ✅

Everything else is on the v0.1 ship list — see [`CHANGELOG.md`](../../CHANGELOG.md) at the repo root for the per-release plan.

---

**Last Updated**: 2026-05-09
**Status**: Active — v0.0.1 alpha; planned content marked above
