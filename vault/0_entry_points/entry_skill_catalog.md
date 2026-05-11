---
tags:
  - entry_point
  - index
  - skills
  - agentic_ai
  - automation
keywords:
  - skill catalog
  - agent skills
  - tessellum skills
  - composer pipeline
topics:
  - Agentic Workflow
  - Knowledge Management Tooling
language: markdown
date of note: 2026-05-11
status: active
building_block: navigation
---

# Entry Point: Tessellum Skill Catalog

## Purpose

Navigation index for Tessellum's agent-invocable skills. Each skill is a *canonical body* (the markdown procedure agents read) paired with an *optional sidecar* (the Composer pipeline YAML that makes it programmatically dispatchable). Skills live under `vault/resources/skills/`; their corresponding sidecars are co-located with the same stem and `.pipeline.yaml` extension.

For the underlying composer pipeline runtime, see [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) (the most complex Composer-driven skill — the DKS cycle) and `tessellum.composer` (the executor).

For the BB-type framing each skill operates on, see [`entry_building_block_index`](entry_building_block_index.md).

## Quick reference — "I want to..."

| I want to... | Skill |
|---|---|
| Run one DKS cycle from an observation | [`tessellum-dks-cycle`](../resources/skills/skill_tessellum_dks_cycle.md) |
| Run a meta-DKS cycle that proposes schema edits | [`tessellum-meta-dks-cycle`](../resources/skills/skill_tessellum_meta_dks_cycle.md) |
| Classify raw content into BB types | [`tessellum-classify-content`](../resources/skills/skill_tessellum_classify_content.md) |
| Route classified content to vault paths | [`tessellum-route-content`](../resources/skills/skill_tessellum_route_content.md) |
| Capture a code repository as a model-typed note | [`tessellum-capture-code-repo-note`](../resources/skills/skill_tessellum_capture_code_repo_note.md) |
| Capture a code snippet as a procedure-typed note | [`tessellum-capture-code-snippet`](../resources/skills/skill_tessellum_capture_code_snippet.md) |
| Answer a question from vault knowledge | [`tessellum-answer-query`](../resources/skills/skill_tessellum_answer_query.md) |
| Search vault notes (hybrid retrieval) | [`tessellum-search-notes`](../resources/skills/skill_tessellum_search_notes.md) |
| Traverse a Folgezettel trail (ancestors / descendants / siblings) | [`tessellum-traverse-folgezettel`](../resources/skills/skill_tessellum_traverse_folgezettel.md) |
| Append a note to a Folgezettel trail | [`tessellum-append-to-trail`](../resources/skills/skill_tessellum_append_to_trail.md) |
| Manage Folgezettel trails (list, find next ID, detect duplicates) | [`tessellum-manage-folgezettel`](../resources/skills/skill_tessellum_manage_folgezettel.md) |
| Check note format compliance (TESS-001..005) | [`tessellum-format-check`](../resources/skills/skill_tessellum_format_check.md) |
| Write a Correction of Errors (COE) note from an incident | [`tessellum-write-coe`](../resources/skills/skill_tessellum_write_coe.md) |

## Skill organisation

Tessellum's skills fall into five clusters, each operating at a different layer of the substrate:

### 1. DKS runtime (2 skills)

Dialectic Knowledge System — the closed-loop runtime that turns the typed substrate into a learning knowledge system.

| Skill | Phase | Purpose |
|---|---|---|
| [`tessellum-dks-cycle`](../resources/skills/skill_tessellum_dks_cycle.md) | Phase 2-10 | One full 7-component DKS cycle from an observation to a revised warrant. Multi-perspective N-argument support since v0.0.54. |
| [`tessellum-meta-dks-cycle`](../resources/skills/skill_tessellum_meta_dks_cycle.md) | Phase 9 (v0.0.52+) | One meta-DKS cycle — proposes + attacks + lands schema-edit events. Cold-start guard at 20 cycles. |

### 2. Capture-side helpers (4 skills)

Skills that segment, classify, route, or convert raw content before it enters the substrate.

| Skill | Purpose |
|---|---|
| [`tessellum-classify-content`](../resources/skills/skill_tessellum_classify_content.md) | Segment raw content by topic boundaries and label each segment with its Building Block + content domain. Pure analysis. |
| [`tessellum-route-content`](../resources/skills/skill_tessellum_route_content.md) | Take a classification report and decide each segment's vault sub-category + target path. Uses the 3-criterion novelty framework (source / operational task / maintenance). |
| [`tessellum-capture-code-repo-note`](../resources/skills/skill_tessellum_capture_code_repo_note.md) | Author a model-typed note describing a code repository's structure. |
| [`tessellum-capture-code-snippet`](../resources/skills/skill_tessellum_capture_code_snippet.md) | Author a procedure-typed note documenting one algorithm or component. |

### 3. Search / answer (2 skills)

| Skill | Purpose |
|---|---|
| [`tessellum-search-notes`](../resources/skills/skill_tessellum_search_notes.md) | Hybrid retrieval (BM25 + dense + graph) over the vault. Returns ranked note paths. |
| [`tessellum-answer-query`](../resources/skills/skill_tessellum_answer_query.md) | Answer a natural-language question by retrieving relevant notes and synthesising a response. Wraps `tessellum-search-notes`. |

### 4. Trail management (3 skills)

Skills that read or write the Folgezettel argumentative-trail structure.

| Skill | Purpose |
|---|---|
| [`tessellum-traverse-folgezettel`](../resources/skills/skill_tessellum_traverse_folgezettel.md) | Walk a FZ trail — ancestors, descendants, siblings. Returns ordered note paths. |
| [`tessellum-append-to-trail`](../resources/skills/skill_tessellum_append_to_trail.md) | Add a note to an existing FZ trail. Finds the proposed parent, assigns the next FZ ID, updates frontmatter. |
| [`tessellum-manage-folgezettel`](../resources/skills/skill_tessellum_manage_folgezettel.md) | List trails, find next available FZ ID for a parent, detect duplicates, surface orphaned FZ IDs. |

### 5. Maintenance + format (2 skills)

| Skill | Purpose |
|---|---|
| [`tessellum-format-check`](../resources/skills/skill_tessellum_format_check.md) | Validate notes against TESS-001..005 + YAML frontmatter + link rules. |
| [`tessellum-write-coe`](../resources/skills/skill_tessellum_write_coe.md) | Author a Correction of Errors (COE) note from an incident — structured 9-section format documenting what went wrong, why, and what's being changed. |

**Total: 13 skills.** Each has a canonical body under `vault/resources/skills/` plus an optional Composer-pipeline sidecar (the `.pipeline.yaml` file with the same stem).

## How to invoke a skill

Three options, depending on context:

1. **As a Composer pipeline** — `tessellum composer run <skill-name>` runs the skill's sidecar pipeline. The agent answers each step's prompt; the orchestrator handles validation, retry, and trace persistence.
2. **As a chat-context skill** — an agent loaded into Claude Code / a CLI session can read the canonical body directly and apply its procedure step-by-step. No pipeline runtime needed.
3. **As Python API** — for runtime skills (`tessellum-dks-cycle`, `tessellum-meta-dks-cycle`), the underlying `tessellum.dks` / `tessellum.dks.meta` API is directly callable.

The canonical body always wins as the *source of truth*. When the canonical and the sidecar disagree, fix the canonical first.

## How to author a new skill

1. Run `tessellum capture skill <slug>` — scaffolds the canonical (`skill_<slug>.md`) + sidecar (`skill_<slug>.pipeline.yaml`) pair under `vault/resources/skills/`.
2. Fill the canonical's H2 sections: `Skill description`, `Setup`, `Resources`, one section per pipeline step, `Error Handling`, `Important Constraints`, `Related Entry Point`.
3. Fill the sidecar's `pipeline:` array — one entry per step the canonical defines. Each step needs `section_id`, `expected_output_schema`, and either a `prompt_template` (LLM step) or `materializer: deterministic_no_llm` (mechanical step).
4. Run `tessellum composer compile vault/resources/skills/skill_<slug>.md` — validates that the canonical + sidecar shapes agree.
5. Add the skill to the table above + the seed manifest (`src/tessellum/data/_seed_manifest.py`).

## Related Entry Points

- [`entry_master_toc`](entry_master_toc.md) — vault navigation root
- [`entry_building_block_index`](entry_building_block_index.md) — the 8-BB picker matrix every skill ultimately operates on
- [`entry_folgezettel_trails`](entry_folgezettel_trails.md) — FZ trail master index (trail-management skills produce/consume FZ subtrees)

## Related Terms

- [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) — DKS canonical
- [`term_format_spec`](../resources/term_dictionary/term_format_spec.md) — YAML frontmatter + link rules every skill's output must satisfy
- [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md) — the FZ trail mechanism

---

**Last Updated**: 2026-05-11
**Status**: Active — Tessellum skill catalog v0.0.58. 13 skills in 5 clusters (DKS runtime / capture helpers / search & answer / trail management / maintenance & format).
