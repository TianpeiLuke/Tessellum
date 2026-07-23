---
tags:
  - resource
  - skill
  - procedure
  - planning
  - digestion
keywords:
  - plan digestion
  - digestion plan
  - building block atomic notes
  - content density
  - section coverage map
topics:
  - Skill Procedures
  - Digestion Pipeline
language: markdown
date of note: 2026-07-23
status: active
building_block: procedure
pipeline_metadata: ./skill_tessellum_plan_digestion.pipeline.yaml
access_control_group: ["general"]
---

# Procedure: tessellum-plan-digestion (Canonical Body)

This is the **single canonical body** for the `tessellum-plan-digestion` skill — **Phase 1** of the plan → augment → review → execute digestion pipeline. It reads one documentation source and produces a single **digestion plan** artifact (the `plan_doc`) that decomposes the source into BB-atomic notes. The internal steps below model the phases of planning; each is a `corpus_wide` step operating on the single plan-doc through-line, chained by `depends_on`, and each reads the prior step's output via `{{upstream.X}}`. Only the final step writes a file.

## Skill description <!-- :: section_id = skill_description :: -->

Read a documentation source (wiki site, BuilderHub docs, Quip doc, PDF, or any multi-section document) and generate a structured digestion plan that decomposes the content into BB-atomic notes. Each planned note corresponds to exactly one building block type. The plan controls content density (split if a note would exceed ~400 lines, ~1800 words, or 6 code blocks), maps every source section to a note, plans cross-references and undigested-term capture, and defines the validation gates. Outputs a single plan file to `plans/`. Use when a source needs to be planned before it is digested into vault notes.

## Step 1: Identify Source and Assess Density <!-- :: section_id = identify_source :: -->

Read the source end to end, then measure it — do NOT estimate from memory.

- **Determine source type** and the right read path: internal wiki / BuilderHub / Quip / code-repo docs are read with the internal-website reader; external URLs with a web fetch; local files/PDFs with the file reader.
- **Read the root page and every leaf page.** Extract linked sub-pages and read each one; an unread page is an unmeasurable page.
- **MEASURE content size per page — not estimate.** For each page record measured word count (from the actual tool output), code-block count (``` pairs / 2), and the list of H2/H3 headings. Record these in a Source table (Page, URL, Measured Words, Code Blocks, Headings).
- **Watch the underestimation failure mode.** Agents routinely underestimate page size by 50–70% when working from training knowledge instead of a real read. If most pages read as <1500 words, or the whole multi-page source totals <5000 words, the measurements are almost certainly wrong — go back and actually read every page.
- **Assess total volume to decide the plan shape.** ≤10,000 words (≤15 notes) → single plan. 10,000–30,000 words (15–30 notes) → single plan with phased execution. >30,000 words (>30 notes) → divide-and-conquer: a pure-index master plan plus self-contained sub-plans, each producing 4–10 notes.

Emit a structured `source_assessment` (source type, per-page measured sizes, total words, estimated note count, and the plan-shape decision) for the downstream steps to build on.

## Step 2: Route — Decide Where Notes Go <!-- :: section_id = route :: -->

Read `{{upstream.source_assessment}}` and decide where the planned notes will live, so nothing is duplicated and the format matches the neighbourhood.

- **Check existing notes first** to avoid duplication — search the vault for the source's topic/keywords; any note that already covers the same ground is referenced, never re-created.
- **Determine the target directory + file prefix** by applying the routing principles: the 3-Criterion Rule (source novelty, operational tasks, maintenance cadence — 0–1 novel routes into an existing folder, 2–3 novel proposes a new subfolder), Context Affinity (notes from one source stay close), and Content TYPE over SOURCE (route by what the content IS). A sequential user guide routes to a tutorials folder; a reference/inventory routes to the platform subfolder. A cohesive series of >15 notes justifies a dedicated subfolder.
- **Derive the Note Format Definition from ≥2 existing notes** in the routed directory (or the closest sibling folder) — do NOT invent a format. Copy the exact YAML field order, the dominant H2 conventions, and the forbidden-field list, and state which example note the format was derived from.

Emit a `routing_decision` (target location, file prefix, existing notes to NOT duplicate, and the derived Note Format Definition).

## Step 3: Decompose into BB-Atomic Notes <!-- :: section_id = decompose :: -->

Read `{{upstream.routing_decision}}` and break the source into atomic notes, one building block per note.

- **Classify each source section by building block**: definitions/terminology → concept; step-by-step instructions/commands → procedure; architecture/components/data flow → model; claims-with-evidence/design rationale → argument; observed behaviour/metrics/demos → empirical_observation; testable predictions → hypothesis; limitations/risks/critiques → counter_argument; index/routing structures → navigation.
- **Group adjacent same-BB sections** into one candidate note; NEVER mix building blocks in a single note.
- **Apply density thresholds and split BEFORE writing.** First at the page level: a source page over ~1800 words cannot map to one note (1800–3600 → ≥2 notes; >3600 → ≥3 notes). Then per note: split when a note would exceed ~1800 words, ~400 lines, 6 code blocks, or 6 unrelated H2 topics, or when it mixes a procedure and a concept of >500 words each.
- **Write the Section Coverage Map**: for EVERY source H1/H2/H3, record which planned note it maps to — no section may be orphaned, no content compressed away.
- **Document Split Decisions**: for any note split beyond the initial grouping, record the original, what it split into, and why (over a threshold or mixed BB).

Emit a `note_breakdown` (the planned-notes table with filename, building block, ~words, and one-line description per note; the section coverage map; and the split-decisions table).

## Step 4: Plan Cross-References and Undigested Terms <!-- :: section_id = cross_references :: -->

Read `{{upstream.note_breakdown}}` and plan how each note connects to the rest of the vault.

- **Per-note related-notes mapping**: for each planned note, search the vault for related notes and list the top matches. Every planned note's mapping must include **≥8 relevant term-dictionary term notes**, selected by content relevancy (not padded with unrelated terms); other related notes (tools/repos/areas/entry points) are additional, not a substitute.
- **Entry-point decision, size-driven**: <15 notes → UPDATE the most relevant existing entry point (1–3 rows or a new H2). 15–30 notes → CREATE a dedicated entry point plus a back-link row in the parent hub. >30 notes → CREATE a dedicated entry point (required) mirroring the master plan's sub-plans index.
- **Inlinks**: name which existing notes should get backlinks pointing TO the new notes so the new cluster is discoverable, not an island.
- **Undigested terms (three-way pre-flight)**: scan the source for acronyms, method/estimator names, and concepts on first use; for each candidate check the term dictionary and classify it — no matching note → capture as a full term note; a stub exists → fill the stub; a substantive note exists → do NOT re-capture, just link it. Assign each undigested term a best-fit acronym glossary and a capture phase (Pattern A pre-digest stubs when ≤10 terms; Pattern B interleaved per sub-plan when >10, with a corpus-wide ownership sweep so no cross-cutting term is unowned). No term may be captured AFTER the digest — that ships ghost references.
- **Validation gates**: define the per-phase gate table (format, grounding, density, coverage, cross-ref, ghost-reference detection, broken-link repair, discoverability) that execution will enforce.

Emit a `cross_ref_plan` (per-note related-notes mapping, entry-point action, inlink plan, the Undigested Terms Plan, and the gate table).

## Step 5: Write the Plan File <!-- :: section_id = write_plan :: -->

Assemble everything into the single digestion plan and write it to `plans/plan_digest_<source_slug>.md` (single plan ≤30 notes) or a master + sub-plan set (>30 notes). This is the ONLY step that writes a file — it PRODUCEs the plan `.md`.

Read `{{upstream.source_assessment}}`, `{{upstream.routing_decision}}`, `{{upstream.note_breakdown}}`, and `{{upstream.cross_ref_plan}}`, and lay them out under the required plan sections: Objective, Routing Decision, Source (measured word-count table), Content Strategy, Section Coverage Map, Split Decisions, Planned Notes table, Content Size Assessment, Summary Statistics, Building Block Distribution, Cross-References to Add, Entry Point Decision, Undigested Terms Plan, Execution Phases (with per-phase validation gates), Note Format Definition, Validation Scripts, Pacing Rules, Density Re-Assessment, and Follow-up Recommendations.

Before finalizing, run the density re-assessment as a self-check: did any note compress too much and need a further split, was any source section omitted, does any note mix building blocks? Fix the plan before it is written.

Output the plan as a JSON object with `output_path` (the `plans/plan_digest_<source_slug>.md` path) and `body_markdown` (the complete plan file body, including its own YAML frontmatter with `status: pending` and the source URL). Do NOT call a file-write tool; the materializer writes the file from these two fields.

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **BB atomicity is non-negotiable** — each planned note gets exactly one building block type.
2. **Density thresholds are hard limits** — the plan splits before writing, not after.
3. **Section coverage is complete** — every source section maps to exactly one note.
4. **No duplication** — existing notes are referenced, not recreated.
5. **Measured, not estimated** — Source-table word counts come from real page reads, never from training knowledge.
6. **The plan is the contract** — execution follows the plan; changes require a plan update first.

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- This is Phase 1 of the plan → augment → review → execute digestion pipeline; its `plan_doc` output is the through-line the later phases read and act on.

## Related skills <!-- :: section_id = related_skills :: -->

The four phases of the plan → augment → review → execute digestion pipeline:

- [`skill_tessellum_plan_digestion.md`](skill_tessellum_plan_digestion.md) — Phase 1 — produces the plan_doc. ← this skill
- [`skill_tessellum_augment_digestion_plan.md`](skill_tessellum_augment_digestion_plan.md) — Phase 2 — enriches the plan_doc with gates + cross-ref contract.
- [`skill_tessellum_review_digestion_plan.md`](skill_tessellum_review_digestion_plan.md) — Phase 3 — the read-only READY/NOT-READY sign-off gate.
- [`skill_tessellum_execute_digestion_plan.md`](skill_tessellum_execute_digestion_plan.md) — Phase 4 — writes the notes from a ready plan.
