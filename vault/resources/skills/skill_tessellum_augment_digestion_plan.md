---
tags:
  - resource
  - skill
  - procedure
  - planning
  - quality
keywords:
  - augment digestion plan
  - tessellum-augment-digestion-plan
  - in-vault skill canonical
  - density re-assessment
  - section coverage map
  - validation gates
  - cross-reference contract
topics:
  - Skill Procedures
  - Digestion Pipeline
language: markdown
date of note: 2026-07-23
status: active
building_block: procedure
access_control_group: ["general"]
---

# Procedure: tessellum-augment-digestion-plan (Canonical Body)

This is the **single canonical body** for the `tessellum-augment-digestion-plan` skill — Phase 2 of the plan → augment → review → execute digestion pipeline. It is invoked directly by Tessellum's composer (`tessellum composer compile / run`); the paired `.pipeline.yaml` sidecar is the typed contract, this canonical is the human-readable procedure.

The skill takes an existing **draft digestion plan** (the artifact produced by Phase 1, plan-digestion) and augments it in place. The plan_doc is the through-line: it is both the input the first step reads and the output the last step rewrites. Each internal step is a `corpus_wide` phase — the plan_doc is a single artifact, not a per-leaf fan-out — chained by `depends_on`, each reading the prior via `{{upstream.X}}`.

## Skill description <!-- :: section_id = skill_description :: -->

After a draft digestion plan exists, this skill augments it with the mandatory augmentation sections: a section coverage map, split decisions, per-phase validation GATE tables, a per-note cross-reference contract, and an Undigested-Terms plan. Critically, it forces the agent to **re-read the source** to confirm no over-compression, omission, or undigested-term coverage gap slipped through, then rewrites the augmented plan file and runs a completeness checklist before the plan is handed to Phase 3 (review). Use AFTER plan-digestion creates the initial draft and BEFORE the review skill signs the plan off.

## Setup <!-- :: section_id = setup :: -->

```bash
VAULT_PATH="."          # run from your vault root
PLANS_DIR="$VAULT_PATH/plans"
PLAN_FILE="$PLANS_DIR/plan_digest_<topic>.md"   # the draft plan to augment
# `tessellum search` and `tessellum format check` resolve paths from CWD
```

## Resources <!-- :: section_id = resources :: -->

- **Plan to augment**: `$PLANS_DIR/plan_digest_<topic>.md` (must already exist — Phase 1 output)
- **Source document(s)**: the URLs / files listed in the plan's Source section, re-read for density verification
- **Vault index**: used for cross-reference search and ghost-reference (target-exists) checks
- **Required BB type**: `procedure` (this skill IS a procedure that operates on a plan artifact)

## Step 1: Read the Existing Draft Plan <!-- :: section_id = read_draft :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on: []
materializer: no_op
output_key: draft_assessment
expected_output_schema:
  type: object
  required:
  - plan_path
  - plan_structure
  - sections_present
  - sections_missing
  properties:
    plan_path:
      type: string
      description: Path to the draft plan being augmented (plans/plan_digest_<topic>.md)
    plan_structure:
      type: string
      enum:
      - single
      - master
      description: single = augment directly; master = augment each sub-plan (do NOT augment
        the index hub)
    planned_note_count:
      type:
      - integer
      - 'null'
      description: Rough count of notes the plan produces; null for a master plan
    routing_ok:
      type: boolean
      description: True iff the Routing Decision applies the 3-criterion rule + context affinity;
        else it must be fixed
    sections_present:
      type: array
      items:
        type: string
      description: Mandatory augmentation sections already present in the draft
    sections_missing:
      type: array
      items:
        type: string
      description: Mandatory augmentation sections the later steps must add
```

You are running step 1 of tessellum-augment-digestion-plan: read the
existing draft digestion plan.

LEAF METADATA
- plan_path: {{leaf.plan_path}}
- source_refs: {{leaf.source_refs}}

Follow this procedure:

Read the draft plan file at `$PLANS_DIR/plan_digest_<topic>.md`. First detect the plan's structure: a **single plan** has a Planned Notes table with concrete filenames and is augmented directly; a **master plan** has a Sub-Plans Index Table linking to sub-plan files and is NOT augmented itself (its sub-plans are augmented independently).

Then inventory which mandatory sections are PRESENT and which are MISSING — Routing Decision, Section Coverage Map, Split Decisions, Note Format Definition, Pacing Rules, Density Re-Assessment, Validation Scripts, per-phase GATE tables, per-note Related Notes mapping, Inlink mapping, Entry Point specifics, Follow-up Recommendations, Undigested Terms Plan, Term-Note Authoring Requirements, and the Entry Point Decision.

If the Routing Decision is missing or weak, apply the 3-criterion routing rule (source novelty, operational tasks, maintenance cadence), verify context affinity (same source → same folder), and confirm content TYPE outranks SOURCE. Emit a structured assessment of the draft: its structure, note count, sections present, and the list of missing sections the later steps must add. This assessment flows downstream as `{{upstream.draft_assessment}}`. Detect whether this is a single
plan (Planned Notes table with concrete filenames) or a master plan
(Sub-Plans Index Table). Inventory which mandatory augmentation sections
are PRESENT and which are MISSING, and assess the Routing Decision.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 2: Re-Read the Source — Density Verification <!-- :: section_id = reread_source :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- read_draft
materializer: no_op
output_key: density_reassessment
expected_output_schema:
  type: object
  required:
  - pages_measured
  - splits_needed
  - new_undigested_terms
  properties:
    pages_measured:
      type: array
      description: 'Per source page: actual measured density'
      items:
        type: object
        required:
        - page
        - measured_words
        properties:
          page:
            type: string
          measured_words:
            type: integer
          code_blocks:
            type:
            - integer
            - 'null'
          headings:
            type:
            - integer
            - 'null'
          plan_estimate_words:
            type:
            - integer
            - 'null'
    density_failure:
      type: boolean
      description: True iff any page's measured words exceed the plan's estimate by >50%
    splits_needed:
      type: array
      description: Notes that must be split, with rationale
      items:
        type: object
        required:
        - note
        - rationale
        properties:
          note:
            type: string
          rationale:
            type: string
    omitted_or_compressed:
      type: array
      items:
        type: string
      description: Source sections omitted from or compressed by the plan
    new_undigested_terms:
      type: array
      items:
        type: string
      description: Terms surfaced by the re-read that the original plan missed
```

You are running step 2 of tessellum-augment-digestion-plan: re-read the
source and verify density. This step is non-negotiable — you MUST read
the actual source pages, not the plan's summary.

DRAFT ASSESSMENT (from step 1)
{{upstream.draft_assessment}}

SOURCE REFS (from leaf metadata)
{{leaf.source_refs}}

Follow this procedure:

This is the most important step. You MUST re-read the original source document(s) — do NOT work from memory or from the plan's summary. Read EVERY page listed in the plan's Source section and record ACTUAL measured values: word count, code-block count, and H2/H3 heading count per page.

Compare the measured values against the plan's estimates. If any page's measured words exceed the plan's estimate by more than 50%, the plan has a density-estimation failure and its notes must be re-split. For each planned note, decide whether to SPLIT: combine >1800 words of source → split at an H2/H3 boundary; >6 code blocks → split overview from examples; a mix of step-by-step commands and conceptual explanation (>500w each) → split into a concept note plus a procedure note. Flag any source section that is OMITTED or COMPRESSED, and mark source warnings/callouts as must-preserve.

The re-read also surfaces undigested terms the original plan missed — acronyms in figure captions or code comments, method names introduced after the first heading, terms in sidebars or footnotes. Produce a density re-assessment: per-page measured counts, per-note estimated word/line counts, borderline notes, any additional splits, and newly-identified undigested terms. This flows downstream as `{{upstream.density_reassessment}}`. Record ACTUAL measured word /
code-block / heading counts per page, compare against the plan's
estimates, decide which notes must split, flag omitted or compressed
sections, and surface any undigested terms the original plan missed.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 3: Add Coverage Map, Split Decisions, and Validation Gates <!-- :: section_id = add_coverage_and_gates :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- reread_source
materializer: no_op
output_key: coverage_and_gates
expected_output_schema:
  type: object
  required:
  - section_coverage_map
  - per_phase_gate_tables
  properties:
    section_coverage_map:
      type: string
      description: ASCII tree mapping every source H2/H3 -> a planned note (or explicit SKIP+reason)
    split_decisions:
      type: array
      items:
        type: object
        required:
        - original
        - split_into
        - rationale
        properties:
          original:
            type: string
          split_into:
            type: string
          rationale:
            type: string
    validation_scripts:
      type: array
      items:
        type: string
      description: 'Bash checks: format+density, cross-link, prereq-dup, ghost-reference'
    pacing_rules:
      type: string
      description: One-phase-at-a-time, re-read-before-write, <=400 lines, verbatim code,
        split-when-dense
    per_phase_gate_tables:
      type: array
      description: One gate table per execution phase; each covers G1-G6 + G8
      items:
        type: object
        required:
        - phase
        - gates
        properties:
          phase:
            type: string
          gates:
            type: array
            items:
              type: string
```

You are running step 3 of tessellum-augment-digestion-plan: assemble the
structural-integrity sections (coverage map, split decisions, validation
scripts, pacing rules, and per-phase gate tables).

DENSITY RE-ASSESSMENT (from step 2)
{{upstream.density_reassessment}}

Follow this procedure:

Using the density re-assessment from the prior step, assemble the structural-integrity sections of the augmented plan.

Build the **Section Coverage Map**: an ASCII tree mapping every source H2/H3 heading to a planned note (or to an explicit SKIP with a documented reason). No source heading may be silently orphaned. Record the **Split Decisions** table — for every note split beyond the initial grouping, capture the original, what it split into, and the rationale (BB mixing, >1800-word threshold, >6 code blocks).

Add the **Validation Scripts** (format + density, cross-link resolution, prerequisite-duplication, and a ghost-reference/target-exists check that verifies every internal link resolves to a real vault note), the **Pacing Rules** (one phase at a time, re-read source before each note, ≤400 lines per note, verbatim code, split-when-dense), and a **per-phase GATE table** for each execution phase. Each gate table must cover G1-Format, G2-Grounding, G3-Density, G3-Coverage, G4-CrossRef, G5-Ghost (every reference exists in the vault), G6-Broken (zero broken links after the batch lands), and G8-Discoverability (every new note ends with ≥1 inbound link from an existing note outside the digest folder). Emit these sections as `{{upstream.coverage_and_gates}}` for the writer step. Build the Section Coverage Map
with zero orphaned source headings, the Split Decisions table, the
Validation Scripts, the Pacing Rules, and a per-phase GATE table that
covers G1-Format, G2-Grounding, G3-Density, G3-Coverage, G4-CrossRef,
G5-Ghost, G6-Broken, and G8-Discoverability.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 4: Add the Per-Note Cross-Reference Contract and Undigested-Terms Plan <!-- :: section_id = add_crossref_contract :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- add_coverage_and_gates
materializer: no_op
output_key: crossref_contract
expected_output_schema:
  type: object
  required:
  - per_note_related_notes
  - undigested_terms_plan
  - entry_point_decision
  properties:
    per_note_related_notes:
      type: array
      description: 'For each planned note: the relevancy-selected related-note links to embed'
      items:
        type: object
        required:
        - note
        - term_links
        properties:
          note:
            type: string
          term_links:
            type: array
            items:
              type: string
            description: '>= N relevancy-selected term_dictionary/ links, all DB-verified
              to exist'
          entry_point_backlink:
            type:
            - string
            - 'null'
    inlink_mapping:
      type: array
      description: 'Reverse links: existing notes that should link TO the new notes (G8)'
      items:
        type: object
        required:
        - existing_note
        - inlink_to_add
        properties:
          existing_note:
            type: string
          inlink_to_add:
            type: string
    undigested_terms_plan:
      type: object
      required:
      - terms
      - all_rows_have_capture_phase
      properties:
        terms:
          type: array
          items:
            type: object
            required:
            - slug
            - capture_phase
            - best_fit_glossary
            properties:
              slug:
                type: string
              capture_phase:
                type: string
              best_fit_glossary:
                type: string
        all_rows_have_capture_phase:
          type: boolean
          description: True iff no row is TBD
        specificity_renames:
          type: array
          items:
            type: string
          description: Too-general slugs renamed to specific ones
        collision_removals:
          type: array
          items:
            type: string
          description: Slugs removed because a substantive vault note already covers the concept
    entry_point_decision:
      type: object
      required:
      - action
      - matches_size_threshold
      properties:
        action:
          type: string
          enum:
          - UPDATE
          - CREATE
          - CREATE_PLUS_HUB
          description: <15 notes = UPDATE; 15-30 = CREATE_PLUS_HUB; >30 = CREATE
        matches_size_threshold:
          type: boolean
        target_entry_point:
          type:
          - string
          - 'null'
```

You are running step 4 of tessellum-augment-digestion-plan: build the
per-note cross-reference contract, the Undigested Terms Plan, the inlink
mapping, and the Entry Point Decision.

COVERAGE + GATES (from step 3)
{{upstream.coverage_and_gates}}

Follow this procedure:

Build the cross-reference contract that the executing agent will copy verbatim. For EACH planned note, search the vault and record a per-note Related Notes mapping: **at least N relevancy-selected `term_dictionary/` term-note links** (relevancy-ranked, not padded with unrelated terms), plus related tools/repos/areas/how-tos/siblings, plus **≥1 entry-point back-link**. Each listed reference must be verified to exist (this is what G5 checks). Then build the reverse **Inlink mapping** (existing notes → new notes) so every new note gains inbound discoverability (G8), and record the Follow-up Recommendations (incremental index update, add-inlinks, backlinks, sync).

Validate the **Undigested Terms Plan**: confirm the table is present, every row has a defined capture phase (no TBD), and every term maps to a best-fit glossary. Attach the Term-Note Authoring Requirements (multi-source research mandate — not just the source doc — plus term-note format compliance and the depth-scaled Related-Terms minimum), and the Documentation-Note Authoring Spec for non-term notes (derived from existing target-dir notes, not invented). Run the term-slug **specificity + collision audit**: rename too-general slugs, and remove any planned slug that a substantive vault note already covers under a different name, rerouting it to link the existing note instead. Finally validate the **Entry Point Decision** against the size threshold (<15 notes = UPDATE only; 15-30 = CREATE + parent-hub update; >30 = CREATE required). Emit this contract as `{{upstream.crossref_contract}}`. For EACH planned note, record the
relevancy-selected term links (>= the floor, all verified to exist) plus
an entry-point back-link. Build the reverse inlink mapping (G8). Validate
the Undigested Terms Plan (no TBD rows, best-fit glossary per term), run
the term-slug specificity + collision audit, and validate the Entry Point
Decision against the size threshold.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 5: Write the Augmented Plan and Run the Completeness Checklist <!-- :: section_id = write_augmented_plan :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- add_coverage_and_gates
- add_crossref_contract
materializer: body_markdown_to_file
output_key: augmented_plan
expected_output_schema:
  type: object
  required:
  - output_path
  - body_markdown
  properties:
    output_path:
      type: string
      pattern: ^plans/plan_digest_[a-z0-9_]+\.md$
      description: The plan file being rewritten in place
    body_markdown:
      type: string
      description: The full augmented plan content, written verbatim by the materializer
```

You are running step 5 of tessellum-augment-digestion-plan: rewrite the
augmented plan file in place. The plan_doc is both input and output.

DRAFT ASSESSMENT (from step 1)
{{upstream.draft_assessment}}

COVERAGE + GATES (from step 3)
{{upstream.coverage_and_gates}}

CROSS-REF CONTRACT + UNDIGESTED TERMS (from step 4)
{{upstream.crossref_contract}}

Follow this procedure:

Rewrite the plan file in place, weaving in the sections assembled by the prior steps. The plan_doc is both input and output: preserve every original section (Objective, Routing, Source, Content Strategy, Planned Notes table, Summary Statistics) and add or replace the augmentation sections — Section Coverage Map, Split Decisions, Density Re-Assessment, Validation Scripts, Pacing Rules, per-phase GATE tables, Per-Note Related Notes Mapping, Inlinks, Undigested Terms Plan, Term-Note Authoring Requirements, Documentation-Note Authoring Spec, Entry Point Decision, and Follow-up Recommendations.

Before returning, run the completeness checklist over the rewritten plan and confirm every item passes: coverage map has no orphaned source headings, every phase gate table includes G1-G6 + G8, the per-note cross-reference contract meets the term-link floor, the Undigested Terms Plan has no TBD rows and passed the specificity/collision audit, and the Entry Point Decision matches the size threshold. Only when all items pass is the plan ready for Phase 3 (review).

Write the complete rewritten plan as the file body. The `output_path` names the plan file being rewritten (`plans/plan_digest_<topic>.md`); `body_markdown` is the full augmented plan content, written verbatim by the materializer. Do NOT call any file-write tool yourself — return the structured output the materializer consumes. Preserve every original plan
section and add/replace the augmentation sections (coverage map, split
decisions, density re-assessment, validation scripts, pacing rules,
per-phase gate tables, per-note related-notes mapping, inlinks,
Undigested Terms Plan, Term-Note Authoring Requirements,
Documentation-Note Authoring Spec, Entry Point Decision, follow-up).
Run the completeness checklist before returning.

OUTPUT FORMAT — return a JSON object with:
  - output_path: the plan path from step 1 (plans/plan_digest_<topic>.md)
  - body_markdown: the COMPLETE rewritten plan, verbatim

Do NOT call any file-write tool. The materializer writes the file from
output_path + body_markdown.

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **MUST re-read source** — Step 2 is non-negotiable. Never trust the plan's word-count estimates without verifying against actual source content.
2. **Split is always preferred over compression** — when in doubt, split. An over-split plan beats an over-dense one.
3. **Plan is the contract** — all changes land in the plan file first; execution follows the plan.
4. **Verbatim code** — mark which source sections contain code that must be preserved character-for-character.
5. **No orphaned sections** — every source H2/H3 must appear in the coverage map; a documented SKIP is acceptable, silent omission is not.

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| Plan file not found | Wrong path or not yet created | Run plan-digestion (Phase 1) first |
| Source URL no longer accessible | Page moved/deleted since plan written | Ask the user for an updated URL; note in plan |
| Plan already fully augmented | Augmentation not needed | Report the checklist as fully passing and stop |
| Re-read reveals the plan is fundamentally wrong | Source structure misunderstood | Recommend rewriting the plan from scratch |

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Skill Catalog](../../0_entry_points/entry_skill_catalog.md) — the vault's skill index
- The plan → augment → review → execute pipeline: this skill is Phase 2, between plan-digestion and review-digestion-plan

## Related skills <!-- :: section_id = related_skills :: -->

The four phases of the plan → augment → review → execute digestion pipeline:

- [`skill_tessellum_plan_digestion.md`](skill_tessellum_plan_digestion.md) — Phase 1 — produces the plan_doc.
- [`skill_tessellum_augment_digestion_plan.md`](skill_tessellum_augment_digestion_plan.md) — Phase 2 — enriches the plan_doc with gates + cross-ref contract. ← this skill
- [`skill_tessellum_review_digestion_plan.md`](skill_tessellum_review_digestion_plan.md) — Phase 3 — the read-only READY/NOT-READY sign-off gate.
- [`skill_tessellum_execute_digestion_plan.md`](skill_tessellum_execute_digestion_plan.md) — Phase 4 — writes the notes from a ready plan.
