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
| Pick a template to copy | [`templates/README.md`](../resources/templates/README.md) — 12 ready-to-fill skeletons (one per BB type + skill / experiment / entry-point / acronym-glossary specializations) + 1 YAML reference |
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

## Templates — Copy-and-Fill Skeletons

The canonical executable form of the YAML frontmatter spec. Pick the template matching your BB type, copy it, fill placeholders. The validator checks the templates against the spec, so they cannot drift apart.

| Template | BB Type | Common Destination |
|---|---|---|
| [`template_yaml_header`](../resources/templates/template_yaml_header.md) | (reference) | YAML frontmatter spec — 7 required fields, closed enums, open vocabularies, type-specific extensions |
| [`template_concept`](../resources/templates/template_concept.md) | concept | `vault/resources/term_dictionary/` |
| [`template_procedure`](../resources/templates/template_procedure.md) | procedure | `vault/resources/how_to/` |
| [`template_skill`](../resources/templates/template_skill.md) | procedure (skill flavor) | `vault/resources/skills/` |
| [`template_model`](../resources/templates/template_model.md) | model | `vault/areas/code_repos/` |
| [`template_argument`](../resources/templates/template_argument.md) | argument | `vault/resources/analysis_thoughts/` |
| [`template_counter_argument`](../resources/templates/template_counter_argument.md) | counter_argument | `vault/resources/analysis_thoughts/` |
| [`template_hypothesis`](../resources/templates/template_hypothesis.md) | hypothesis | `vault/resources/analysis_thoughts/` |
| [`template_empirical_observation`](../resources/templates/template_empirical_observation.md) | empirical_observation (inline) | `vault/resources/analysis_thoughts/` |
| [`template_experiment`](../resources/templates/template_experiment.md) | empirical_observation (full pre-reg) | `vault/archives/experiments/` |
| [`template_navigation`](../resources/templates/template_navigation.md) | navigation (generic) | `vault/0_entry_points/` or anywhere in the vault |
| [`template_entry_point`](../resources/templates/template_entry_point.md) | navigation (entry-point shape) | `vault/0_entry_points/entry_*.md` |
| [`template_acronym_glossary`](../resources/templates/template_acronym_glossary.md) | navigation (acronym glossary shape) | `vault/0_entry_points/acronym_glossary_*.md` |

See [`templates/README.md`](../resources/templates/README.md) for full guidance.

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
