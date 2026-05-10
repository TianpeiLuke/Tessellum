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
  - vault entry
topics:
  - Navigation
  - Vault Entry
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Tessellum — Master Table of Contents

> **You are inside Tessellum's dogfooded vault.** This is the project's own typed-knowledge slipbox: the same Building Block format, the same Folgezettel trails, the same format spec that `tessellum format check` enforces on every vault.
>
> This page is the navigation root. Pick a path below.

---

## I'm new — where do I start?

| If you want to... | Read |
|---|---|
| Install Tessellum and run through the basics | [`howto_first_vault`](../resources/how_to/howto_first_vault.md) — 8-step CLI walkthrough: init → capture → format check → index → search → composer |
| Look up unfamiliar vocabulary | [`acronym_glossary_tessellum_foundations`](acronym_glossary_tessellum_foundations.md) — one-line lookup for the 11 foundation terms (Z, Slipbox, FZ, PARA, BASB, CODE, Knowledge BB, BB, EF, DKS, CQRS) |
| Understand the typed substrate | [`term_building_block`](../resources/term_dictionary/term_building_block.md) — the 8 BB types + 10 directed epistemic edges |
| Pick the right BB type for a new note | [`entry_building_block_index`](entry_building_block_index.md) — the scannable matrix (BB × question × function × layer × required sections × default directory) |
| Author your first note (format rules + every validator code) | [`term_format_spec`](../resources/term_dictionary/term_format_spec.md) — YAML frontmatter contract + closed enums + tag conventions + link rules + complete issue-code reference |
| Read the architectural reasoning records | [`entry_folgezettel_trails`](entry_folgezettel_trails.md) — master FZ trail map (3 trails shipped: Architecture, Dialectic, Retrieval) |

---

## Conceptual Primer — 11 Foundation Term Notes

### Methodology lineage (what Tessellum descends from)

| Concept | Term note |
|---|---|
| **Zettelkasten** — Luhmann's atomic-note method | [`term_zettelkasten`](../resources/term_dictionary/term_zettelkasten.md) |
| **Slipbox** — the system class (Tessellum is one implementation) | [`term_slipbox`](../resources/term_dictionary/term_slipbox.md) |
| **Folgezettel** — alphanumeric trails encoding *how thinking developed* | [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md) |
| **PARA** — Forte's Projects / Areas / Resources / Archives | [`term_para_method`](../resources/term_dictionary/term_para_method.md) |
| **BASB** — Building a Second Brain (Tiago Forte) | [`term_basb`](../resources/term_dictionary/term_basb.md) |
| **CODE** — Capture / Organize / Distill / Express lifecycle | [`term_code_method`](../resources/term_dictionary/term_code_method.md) |
| **Knowledge Building Blocks** — Sascha Fast's historical taxonomy | [`term_knowledge_building_blocks`](../resources/term_dictionary/term_knowledge_building_blocks.md) |

### Tessellum-specific architecture (what's new)

| Concept | Term note |
|---|---|
| **Building Block** — Tessellum's 8-type typed atomic ontology | [`term_building_block`](../resources/term_dictionary/term_building_block.md) |
| **Epistemic Function** — what each BB *does* | [`term_epistemic_function`](../resources/term_dictionary/term_epistemic_function.md) |
| **DKS** — Dialectic Knowledge System (closed-loop dialectic) | [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) |
| **CQRS** — System P (write) ⊥ System D (read), shared substrate | [`term_cqrs`](../resources/term_dictionary/term_cqrs.md) |

### System regularization

| Note | Role |
|---|---|
| [`term_format_spec`](../resources/term_dictionary/term_format_spec.md) | The YAML / tag / link / naming contract every note must satisfy. The validator's authoritative spec in vault form, with every `TESS-NNN` / `YAML-NNN` / `LINK-NNN` issue code mapped to a fix. |

---

## Folgezettel Trails

Tessellum's design history is encoded as three Folgezettel research trails. Each trail records an argumentative descent: starting framing → counters → synthesis. Together they document how the load-bearing architectural commitments were reasoned into shape.

| Trail # | Subject | Per-trail entry | Nodes |
|--:|---|---|---:|
| **1** | From the typed BB graph to the two-system CQRS commitment | [`entry_architecture_trail`](entry_architecture_trail.md) | 4 |
| **2** | How DKS was reasoned into shape — 7-component closed loop | [`entry_dialectic_trail`](entry_dialectic_trail.md) | 2 |
| **3** | How retrieval was tested into shape — 14-strategy bake-off → unified engine + hybrid RRF | [`entry_retrieval_trail`](entry_retrieval_trail.md) | 2 |

[`entry_folgezettel_trails`](entry_folgezettel_trails.md) is the master trail index + "how to grow a trail" guide.

---

## How-To Library

| Procedure | Note |
|---|---|
| Get started (install → init → capture → format check → index → search → composer) | [`howto_first_vault`](../resources/how_to/howto_first_vault.md) |

*Additional how-to notes are added as users contribute them. The seed ships one walkthrough (`howto_first_vault`) — enough to bring a new user from `pip install` to a working vault.*

---

## Entry Points by Surface

| Entry point | Indexes |
|---|---|
| [`entry_acronym_glossary`](entry_acronym_glossary.md) | Master index of all acronym glossaries (1 Tessellum-foundations + 5 universal) |
| [`entry_building_block_index`](entry_building_block_index.md) | The 8-row BB picker matrix + the 10 epistemic edges |
| [`entry_folgezettel_trails`](entry_folgezettel_trails.md) | Master FZ trail map — every research trail in the vault |
| [`entry_architecture_trail`](entry_architecture_trail.md) | Trail 1 — Architecture / CQRS |
| [`entry_dialectic_trail`](entry_dialectic_trail.md) | Trail 2 — Dialectic / DKS |
| [`entry_retrieval_trail`](entry_retrieval_trail.md) | Trail 3 — Retrieval / System D |

---

## Acronym Glossaries

| Glossary | Entries | Domain |
|---|--:|---|
| [`acronym_glossary_tessellum_foundations`](acronym_glossary_tessellum_foundations.md) | 11 | The foundation vocabulary (Z, Slipbox, FZ, PARA, BASB, CODE, Knowledge BB, BB, EF, DKS, CQRS) |
| [`acronym_glossary_statistics`](acronym_glossary_statistics.md) | 54 | Causal inference, Bayesian methods, distributions |
| [`acronym_glossary_critical_thinking`](acronym_glossary_critical_thinking.md) | 31 | Logic, fallacies, reasoning patterns |
| [`acronym_glossary_cognitive_science`](acronym_glossary_cognitive_science.md) | 130 | Cognitive biases, dual-process theory, decision heuristics |
| [`acronym_glossary_network_science`](acronym_glossary_network_science.md) | 48 | Graph theory, centrality, community detection |
| [`acronym_glossary_llm`](acronym_glossary_llm.md) | 134 | LLM architectures, RAG, agents, evaluation |

Total: 408 entries across 6 glossaries. Start with `acronym_glossary_tessellum_foundations` to learn the project's vocabulary; the others are lookup tools for jargon resolution as you encounter it.

---

## Templates — Copy-and-Fill Skeletons

The canonical executable form of the YAML frontmatter spec. Pick the template matching your BB type, copy it (or use `tessellum capture <flavor> <slug>` to copy + rename + strip the commentary block), fill the placeholders.

| Template | BB Type | Common Destination |
|---|---|---|
| [`template_yaml_header`](../resources/templates/template_yaml_header.md) | (reference) | YAML frontmatter spec — paired-template-form companion to `term_format_spec` |
| [`template_concept`](../resources/templates/template_concept.md) | `concept` | `resources/term_dictionary/` |
| [`template_procedure`](../resources/templates/template_procedure.md) | `procedure` | `resources/how_to/` |
| [`template_skill`](../resources/templates/template_skill.md) (+ `.pipeline.yaml`) | `procedure` (skill flavor) | `resources/skills/` |
| [`template_model`](../resources/templates/template_model.md) | `model` | `resources/term_dictionary/` |
| [`template_argument`](../resources/templates/template_argument.md) | `argument` | `resources/analysis_thoughts/` |
| [`template_counter_argument`](../resources/templates/template_counter_argument.md) | `counter_argument` | `resources/analysis_thoughts/` |
| [`template_hypothesis`](../resources/templates/template_hypothesis.md) | `hypothesis` | `resources/analysis_thoughts/` |
| [`template_empirical_observation`](../resources/templates/template_empirical_observation.md) | `empirical_observation` (inline) | `resources/analysis_thoughts/` |
| [`template_experiment`](../resources/templates/template_experiment.md) | `empirical_observation` (full pre-reg) | `archives/experiments/` |
| [`template_navigation`](../resources/templates/template_navigation.md) | `navigation` (generic) | `0_entry_points/` |
| [`template_entry_point`](../resources/templates/template_entry_point.md) | `navigation` (entry-point shape) | `0_entry_points/entry_*.md` |
| [`template_acronym_glossary`](../resources/templates/template_acronym_glossary.md) | `navigation` (acronym-glossary shape) | `0_entry_points/acronym_glossary_*.md` |
| [`template_code_snippet`](../resources/templates/template_code_snippet.md) | `procedure`/`concept`/`model` (code snippet) | `resources/code_snippets/` |
| [`template_code_repo`](../resources/templates/template_code_repo.md) | `model` (code repository) | `areas/code_repos/` |

See [`templates/README.md`](../resources/templates/README.md) for full guidance.

---

## Project State (Outside the Vault)

Tessellum's project-management state — milestone plans, layout decisions, run-artifact conventions — lives in the top-level [`plans/`](../../plans/README.md) directory, separate from the typed-knowledge vault. Plans are governance documents (meta to both System P and System D); they are *not* typed atomic notes.

All v0.1 plans are **complete**:

- [`plan_v01_src_tessellum_layout`](../../plans/plan_v01_src_tessellum_layout.md) — what `src/tessellum/` ships in v0.1
- [`plan_cqrs_repo_layout`](../../plans/plan_cqrs_repo_layout.md) — repo layout via CQRS workflow framing
- [`plan_composer_port`](../../plans/plan_composer_port.md) — Composer port (6 waves)
- [`plan_retrieval_port`](../../plans/plan_retrieval_port.md) — Retrieval port (5 waves)
- [`plan_code_artifacts_port`](../../plans/plan_code_artifacts_port.md) — code-artifact capture (3 phases)
- [`plan_minimal_seed_vault`](../../plans/plan_minimal_seed_vault.md) — seed-vault content design

Pipeline runtime traces (gitignored, session-scoped) live in [`runs/`](../../runs/README.md): `capture/`, `retrieval/`, `composer/`. The Composer runtime writes traces to `runs/composer/<filesystem-safe-timestamp>_<skill>.json`.

---

## Status

Tessellum is at **v0.0.34** on PyPI (see [`CHANGELOG.md`](../../CHANGELOG.md) at the repo root for the per-release ship list). Every engine subsystem on the v0.1 plan is shipped:

| Subsystem | Versions | Status |
|---|---|---|
| Format library (validator + parser + link checker) | v0.0.2 – v0.0.4 | shipped |
| CLI scaffold (`init` + `capture` + `format check`) | v0.0.3 – v0.0.10 | shipped |
| Capture flavors (14 BB types + variants) | v0.0.8 / v0.0.24 | shipped |
| Indexer (unified SQLite + FTS5 + sqlite-vec) | v0.0.12 – v0.0.14 | shipped |
| Retrieval (BM25 + dense + hybrid RRF + best-first BFS + metadata) | v0.0.13 – v0.0.18 | shipped |
| Composer (capture → compile → execute → batch → eval, 6 waves) | v0.0.9 – v0.0.23 | shipped |
| Seed vault (11 foundation terms + format spec + walkthrough + 3 FZ trails) | v0.0.25 – v0.0.33 | shipped |
| Single-source-of-truth seed manifest | v0.0.34 | shipped |

**51 markdown files** ship in the seed vault on every `pip install tessellum && tessellum init`.

What's still on the v0.1.0 list (content, not engine): more authored example notes (one per BB type with realistic content), an extended how-to library, a public MCP server. These are user-supplied content rather than engine work.

---

**Last Updated**: 2026-05-10
**Status**: Active — v0.0.34 alpha; engine complete; seed content stable
