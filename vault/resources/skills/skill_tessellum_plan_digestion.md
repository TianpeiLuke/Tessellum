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
access_control_group: ["general"]
---

# Procedure: tessellum-plan-digestion (Canonical Body)

This is the **single canonical body** for the `tessellum-plan-digestion` skill — **Phase 1** of the plan → augment → review → execute digestion pipeline. It reads one documentation source and produces a single **digestion plan** artifact (the `plan_doc`) that decomposes the source into BB-atomic notes. The internal steps below model the phases of planning; each is a `corpus_wide` step operating on the single plan-doc through-line, chained by `depends_on`, and each reads the prior step's output via `{{upstream.X}}`. Only the final step writes a file.

## Skill description <!-- :: section_id = skill_description :: -->

Read a documentation source (a wiki site, a documentation portal, a shared design doc, a PDF, or any multi-section document) and generate a structured digestion plan that decomposes the content into BB-atomic notes. Each planned note corresponds to exactly one building block type. The plan controls content density (split if a note would exceed the active granularity's per-note ceiling (the driver-injected words/lines/code-block caps — e.g. ~1,800 words under section, one thought per note under thought granularity)), maps every source section to a note, plans cross-references and undigested-term capture, and defines the validation gates. Outputs a single plan file to `plans/`. Use when a source needs to be planned before it is digested into vault notes.

## Step 1: Identify Source and Assess Density <!-- :: section_id = identify_source :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on: []
materializer: no_op
output_key: source_assessment
expected_output_schema:
  type: object
  required:
  - source_type
  - pages
  - total_words
  - estimated_note_count
  - plan_shape
  properties:
    source_type:
      type: string
      description: wiki | docs_portal | shared_doc | code_repo_docs | external | local_file
    pages:
      type: array
      description: One entry per page actually read + measured
      items:
        type: object
        required:
        - url
        - measured_words
        - code_blocks
        - headings
        properties:
          url:
            type: string
          measured_words:
            type: integer
          code_blocks:
            type: integer
          headings:
            type: array
            description: EVERY H1/H2/H3 heading of this page, verbatim from the
              actual source — NOT from memory. This is the content-grounding
              ledger the coverage map (decompose) and gate G3/PLAN-006 check
              against, so it must be the real section list, complete and exact.
            items:
              type: string
    total_words:
      type: integer
      description: Sum of measured_words across all pages
    estimated_note_count:
      type: integer
    plan_shape:
      type: string
      enum:
      - single_plan
      - single_plan_phased
      - master_plus_subplans
inputs:
- name: leaf.source_url
  required: false
- name: leaf.source_name
  required: false
- name: leaf.member_count
  required: false
- name: leaf.members
  required: false
- name: leaf.pages
  required: true
- name: leaf.source_excerpt
  required: true
```

You are running Phase 1, step 1 (identify_source) of tessellum-plan-digestion.

LEAF METADATA
- source_url: {{leaf.source_url}}
- source_name: {{leaf.source_name}}

CORPUS MEMBERS (a non-empty `members` list means a multi-document bundle; `member_count: 1` with an empty `members` list is the single-source path)
- member_count: {{leaf.member_count}}
- members: {{leaf.members}}

MEASURED SOURCE LEDGER (code-computed from the actual source bytes; the ground truth for every figure in this step):
{{leaf.pages}}

SOURCE CONTENT (provided inline — you have NO tools and there is nothing to fetch; a `file://` source_url is already fully included below):
{{leaf.source_excerpt}}

Follow this procedure:

- You are a single-shot model with NO tools. NEVER emit `<tool_call>` / `<tool_response>` blocks, and never role-play fetching a URL or reading a file — everything this step needs is provided above.
- **Transcribe the MEASURED SOURCE LEDGER verbatim into your `pages[]` output.** Its rows already carry `url`, `measured_words`, `code_blocks`, and the complete verbatim `headings` list, measured by code from the real bytes — do NOT re-measure, re-count, or estimate any of these figures; `total_words` is the sum of the ledger rows' `measured_words`.
- **If `members` is a non-empty list** (a multi-document bundle), you are planning a *corpus*, not a single page: the ledger has one row per member; assess the aggregate volume across ALL members to decide the plan shape. Otherwise (`member_count: 1`, empty `members`), plan the single source at `source_url` from the SOURCE CONTENT above.
- **Determine source type** from `source_url` and the content itself: wiki | docs_portal | shared_doc | code_repo_docs | external | local_file.
- **Assess total volume to decide the plan shape — governed by SOURCE WORDS, not note count (note count scales with the active granularity, so the same source yields far more notes under thought than under section; judge the shape by words).** ≤10,000 words → single plan. 10,000–30,000 words → single plan with phased execution. >30,000 words → divide-and-conquer: a pure-index master plan plus self-contained sub-plans, each covering a coherent source span (~5,000–10,000 words of source).

Emit a structured `source_assessment` (source type, the TRANSCRIBED per-page measured sizes, total words, estimated note count, and the plan-shape decision) for the downstream steps to build on.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 2: Route — Decide Where Notes Go <!-- :: section_id = route :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- identify_source
materializer: no_op
output_key: routing_decision
expected_output_schema:
  type: object
  required:
  - target_directory
  - file_prefix
  - note_format_definition
  properties:
    target_directory:
      type: string
    file_prefix:
      type: string
    existing_notes_to_not_duplicate:
      type: array
      items:
        type: string
    note_format_definition:
      type: object
      required:
      - derived_from
      - yaml_field_order
      properties:
        derived_from:
          type: string
          description: The example note the format was copied from
        yaml_field_order:
          type: array
          items:
            type: string
        h2_conventions:
          type: array
          items:
            type: string
        forbidden_fields:
          type: array
          items:
            type: string
inputs:
- name: upstream.source_assessment
  required: true
- name: leaf.existing_notes_context
  required: false
```

You are running Phase 1, step 2 (route) of tessellum-plan-digestion.

SOURCE_ASSESSMENT (from step 1)
{{upstream.source_assessment}}

EXISTING NOTES CONTEXT (a retrieval sample from the live index keyed on
this source's topic — titles, paths, and a sibling format sample; empty
on a bootstrap vault):
{{leaf.existing_notes_context}}

Follow this procedure:

Read `{{upstream.source_assessment}}` and decide where the planned notes will live, so nothing is duplicated and the format matches the neighbourhood.

- **Check existing notes first** to avoid duplication — consult the EXISTING NOTES CONTEXT block provided below (a retrieval sample from the live index keyed on this source's topic); any listed entry that already covers the same ground is referenced, never re-created. An empty block means a bootstrap vault: record an empty duplication list, never invent one.
- **Determine the target directory + file prefix** by applying the routing principles: the 3-Criterion Rule (source novelty, operational tasks, maintenance cadence — 0–1 novel routes into an existing folder, 2–3 novel proposes a new subfolder), Context Affinity (notes from one source stay close), and Content TYPE over SOURCE (route by what the content IS). A sequential user guide routes to a tutorials folder; a reference/inventory routes to the platform subfolder. A cohesive series of >15 notes justifies a dedicated subfolder.
- **Decide the target directory FIRST by the routing principles (content TYPE over source; the sample's composition is retrieval, never a recommendation), THEN take the Note Format Definition from the sample listed under YOUR CHOSEN directory in the EXISTING NOTES CONTEXT below** — do NOT invent a format, and do NOT let a flavor that dominates the sample (e.g. term notes) override the content-type decision. Copy the exact YAML field order, the dominant H2 conventions, and the forbidden-field list, and state which sample entry the format came from. An empty block means a bootstrap vault: use the flavor's documented template and state `derived_from: bootstrap`.

Emit a `routing_decision` (target location, file prefix, existing notes to NOT duplicate, and the derived Note Format Definition).
Check for existing notes to avoid duplication, choose the target
directory + file prefix via the 3-Criterion Rule / Context Affinity /
Content-TYPE-over-SOURCE, and TAKE the Note Format Definition from the provided sample of
existing notes in the routed directory (do NOT invent it) — record which
note it was derived from.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 3: Decompose into Thought-Atomic Notes <!-- :: section_id = decompose :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- route
materializer: no_op
output_key: note_breakdown
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - planned_notes
  - section_coverage_map
  properties:
    planned_notes:
      type: array
      items:
        type: object
        required:
        - filename
        - building_block
        - approx_words
        - description
        properties:
          filename:
            type: string
          building_block:
            type: string
            enum:
            - concept
            - procedure
            - model
            - argument
            - empirical_observation
            - hypothesis
            - counter_argument
            - navigation
          approx_words:
            type: integer
          description:
            type: string
    section_coverage_map:
      type: array
      description: One row per source H1/H2/H3 mapped to a planned note
      items:
        type: object
        required:
        - source_section
        - maps_to_note
        properties:
          source_section:
            type: string
          maps_to_note:
            type: string
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
            type: array
            items:
              type: string
          rationale:
            type: string
inputs:
- name: upstream.source_assessment
  required: true
- name: upstream.routing_decision
  required: true
- name: leaf.note_count_band
  required: false
- name: leaf.granularity_guidance
  required: false
```

You are running Phase 1, step 3 (decompose) of tessellum-plan-digestion.

SOURCE ASSESSMENT (from step 1 — the MEASURED source pages + their EXACT headings)
{{upstream.source_assessment}}

ROUTING_DECISION (from step 2)
{{upstream.routing_decision}}

Follow this procedure:

Read `{{upstream.routing_decision}}` and decompose the source into atomic notes — one building block AND one atomic unit (per the granularity profile below) per note. **Decompose FIRST from the CONTENT's atomic units, THEN check coverage against the source headings.** Do NOT start from the outline and emit one note per heading: the outline sets what must be COVERED, never how many notes the content yields.

- **GROUND the coverage map in the ACTUAL source sections.** The `pages[].headings` list in `{{upstream.source_assessment}}` is the authoritative, measured inventory of every real H1/H2/H3 in the source. The Section Coverage Map MUST be built from THAT list — every heading in `source_assessment.pages[].headings` appears as a covered row, mapped to at least one covering note (built AFTER decomposition — see the coverage bullet below). Do NOT invent, rename, or infer section names from your own knowledge of the topic: use the source's real headings verbatim. (This is content grounding — the plan gate PLAN-006 + gate G3 compare the coverage map against these measured headings and reject the plan if any real section is unmapped.)
- **PLAN WITHIN THE COMPUTED NOTE-COUNT BAND.** The driver derives the acceptable note-count range from the measured source and the density gates — PLANNED NOTE COUNT BAND (computed): {{leaf.note_count_band}} — plan a note count INSIDE this band; a plan outside it fails the deterministic PLAN-004/PLAN-008 gates at sign-off, so exceeding it wastes the whole run.
- **GRANULARITY — size each note per the active profile below (injected by the driver).**
{{leaf.granularity_guidance}}
- **The Planned Notes table and the `planned_notes` list are ONE inventory.** Every structured `planned_notes` entry appears as a row in the plan's Planned Notes table and vice versa — equal counts, same filenames; a divergence means the execute wave materializes a different set than the plan document promises (the r4 finding: 8 table rows, 18 materialized notes).
- **COPY the measured figures verbatim — never re-estimate — and write them as BARE DIGITS (12813, not 12,813): no thousands separators anywhere a measured figure appears.** Every word-count, code-block, and heading figure you state (the Source table, per-note `approx_words`, density decisions) MUST be copied from `source_assessment.pages[].measured_words` / `code_blocks` / `headings` — do NOT re-derive, round down, or re-estimate from memory; a Source figure below the measured value is a grounding failure the review's CP7 ledger check rejects. Per-note `approx_words` must SUM to approximately the measured total (the mapped sections' share of `measured_words`), not to an independent guess.
- **ENUMERATE THE ATOMIC UNITS FIRST — walk the content, not the outline.** Extract every atomic unit the GRANULARITY profile above defines: under the default `thought` profile, one THOUGHT (sized by the per-BB TARGET WEIGHT); under `section`, one BB/topic. Apply the profile's **SPLIT TEST** — if a candidate note would answer two DIFFERENT questions, it is two notes — and its **STOPPING RULE** — do not split when the relation between the halves cannot be stated in one line. The note COUNT is set by the atomic units present in the content, NOT by the number of headings: a rich section yields MANY notes, a thin one may yield a single note. Never cap the count at the heading count, and never fuse two distinct thoughts to land on a section boundary.
- **One building block per note; classify each unit by kind**: definitions/terminology → concept; step-by-step OUTCOMES → procedure; architecture/components/data flow → model; claims-with-evidence/design rationale → argument; observed behaviour/metrics/demos → empirical_observation; testable predictions → hypothesis; limitations/risks/critiques → counter_argument; index/routing structures → navigation. NEVER mix building blocks in a single note (PLAN-005).
- **Give every note a REAL `approx_words` inside its profile band** (bare digits, e.g. 90 not "~90"). A note at/over the active ceiling is rejected by **PLAN-004**; a plan whose note COUNT falls outside the COMPUTED NOTE-COUNT BAND above is rejected by PLAN-004/PLAN-008. Decomposing finer changes the note COUNT, not the total: the per-note `approx_words` must still SUM to approximately the mapped source's `measured_words`.
- **THEN assemble the Section Coverage Map as a completeness check over the notes you enumerated.** For EVERY heading in `source_assessment.pages[].headings` (verbatim), record at least one note that covers it. A heading MAY map to several notes — list one representative row per heading, or one row per covering note; the requirement is that NO heading is orphaned and no content compressed away, **NOT that each heading gets exactly one note**. No invented section may appear that is not in the measured headings.
- **Document Split Decisions**: for any unit you split out of a larger candidate, record the original, what it split into, and why (the SPLIT TEST, a mixed BB, or a profile-ceiling breach).
- **These are HARD, MACHINE-ENFORCED plan gates (FZ 20k9d4), not just guidance.** The plan gate fails the plan — blocking sign-off and forcing a re-plan — on any OBJECTIVE breach: **PLAN-004** a note whose `approx_words` ≥ the active granularity ceiling (so give every note a REAL per-note word estimate); **PLAN-005** a note whose `building_block` crams more than one block (e.g. `"concept, procedure"`); **PLAN-006** a source heading left uncovered (an empty/`none`/`TBD` target, or a measured heading named in no row). On failure you may remedy EITHER by splitting/consolidating notes OR by re-mapping the coverage — the gate does not prescribe which; it only requires the breach be gone. (A *subjective* "is this note truly atomic?" judgement is NOT gated — that stays the reviewer's advisory call.)

Emit a `note_breakdown` (the planned-notes table with filename, building block, ~words, and one-line description per note; the section coverage map; and the split-decisions table). Enumerate the content's atomic
units per the granularity profile (one building block each, NEVER mixed),
apply the profile's SPLIT TEST and STOPPING RULE, size each note inside its
profile band, and THEN produce a coverage map in which EVERY source heading
is covered by AT LEAST ONE note (a rich heading may map to many).

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 4: Plan Cross-References and Undigested Terms <!-- :: section_id = cross_references :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- decompose
materializer: no_op
output_key: cross_ref_plan
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - per_note_related_notes
  - entry_point_action
  - undigested_terms
  - validation_gates
  properties:
    per_note_related_notes:
      type: array
      items:
        type: object
        required:
        - note_filename
        - term_notes
        properties:
          note_filename:
            type: string
          term_notes:
            type: array
            description: 'Relevancy-selected term-dictionary notes; the floor SCALES with the active granularity (about one term link per ~150 words of note target size, min 1): SECTION ~1,100-1,600w -> >=8; THOUGHT ~40-250w -> >=1. Relevancy-selected, never padded to a large-note count.'
            items:
              type: string
          other_related_notes:
            type: array
            items:
              type: string
    entry_point_action:
      type: object
      required:
      - action
      - entry_point
      properties:
        action:
          type: string
          enum:
          - update
          - create
        entry_point:
          type: string
        parent_hub:
          type:
          - string
          - 'null'
    inlinks:
      type: array
      items:
        type: object
        required:
        - from_note
        - to_note
        properties:
          from_note:
            type: string
          to_note:
            type: string
    undigested_terms:
      type: array
      items:
        type: object
        required:
        - term_slug
        - best_fit_glossary
        - capture_phase
        - stub_or_full
        properties:
          term_slug:
            type: string
          best_fit_glossary:
            type: string
          capture_phase:
            type: string
          stub_or_full:
            type: string
            enum:
            - full
            - fill-stub
            - existing-do-not-recapture
    validation_gates:
      type: array
      items:
        type: string
inputs:
- name: upstream.note_breakdown
  required: true
- name: leaf.existing_notes_context
  required: false
- name: artifact.source_excerpt
  required: false
```

You are running Phase 1, step 4 (cross_references) of
tessellum-plan-digestion.

NOTE_BREAKDOWN (from step 3)
{{upstream.note_breakdown}}

EXISTING NOTES CONTEXT (a retrieval sample from the live index; empty on
a bootstrap vault):
{{leaf.existing_notes_context}}

SOURCE TEXT (the of-record source, for the undigested-terms scan):
{{artifact.source_excerpt}}

Follow this procedure:

Read `{{upstream.note_breakdown}}` and plan how each note connects to the rest of the vault.

- **Per-note related-notes mapping**: for each planned note, select the top matches from the EXISTING NOTES CONTEXT provided below (the execute wave enriches each writer with its own per-note retrieval; an empty block means a bootstrap vault — plan the contract, list nothing invented). Every planned note's mapping must include a relevancy-selected `term_dictionary/` term-note floor that SCALES with the ACTIVE granularity profile above — roughly one relevancy-selected term note per ~150 words of the note's target size, minimum 1: SECTION granularity (~1,100–1,600-word notes) → **≥8**; THOUGHT granularity (~40–250-word notes) → **≥1** (1–2 for a rich note). Select by content relevancy and NEVER pad a small note to a large note's count (a 95-word thought note with 8 term links is padded); other related notes (tools/repos/areas/entry points) are additional, not a substitute. Emit one mapping for EVERY planned note (N of N).
- **Entry-point decision, size-driven**: <15 notes → UPDATE the most relevant existing entry point (1–3 rows or a new H2). 15–30 notes → CREATE a dedicated entry point plus a back-link row in the parent hub. >30 notes → CREATE a dedicated entry point (required) mirroring the master plan's sub-plans index.
- **Inlinks**: name which existing notes should get backlinks pointing TO the new notes so the new cluster is discoverable, not an island.
- **Undigested terms (three-way pre-flight)**: scan the SOURCE TEXT provided below for acronyms, method/estimator names, and concepts on first use; for each candidate check the term dictionary and classify it — no matching note → capture as a full term note; a stub exists → fill the stub; a substantive note exists → do NOT re-capture, just link it. Assign each undigested term a best-fit acronym glossary and a capture phase (Pattern A pre-digest stubs when ≤10 terms; Pattern B interleaved per sub-plan when >10, with a corpus-wide ownership sweep so no cross-cutting term is unowned). No term may be captured AFTER the digest — that ships ghost references.
- **Validation gates**: define the per-phase gate table (format, grounding, density, coverage, cross-ref, ghost-reference detection, broken-link repair, discoverability) that execution will enforce.

Emit a `cross_ref_plan` (per-note related-notes mapping, entry-point action, inlink plan, the Undigested Terms Plan, and the gate table). For every planned note (N of N) build a related-
notes mapping meeting the size-scaled term-note floor (SECTION >=8; THOUGHT
>=1, about one relevancy-selected term link per ~150 words, never padded); decide the entry-
point action by digest size (update <15, create 15-30, create required
>30) with a parent-hub back-link when creating; plan inlinks; run the
three-way undigested-term pre-flight and assign every term a best-fit
glossary + capture phase (never capture AFTER the digest); and define
the per-phase validation gate table.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 5: Write the Plan File <!-- :: section_id = write_plan :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- decompose
- cross_references
materializer: body_markdown_to_file
output_key: plan_doc
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - output_path
  - body_markdown
  properties:
    output_path:
      type: string
      pattern: ^plans/plan_digest_[a-z0-9_]+\.md$
    body_markdown:
      type: string
      description: The complete digestion plan file body, including YAML frontmatter
inputs:
- name: upstream.source_assessment
  required: true
- name: upstream.note_breakdown
  required: true
- name: upstream.cross_ref_plan
  required: true
- name: upstream.routing_decision
  required: true
```

You are running Phase 1, step 5 (write_plan) of tessellum-plan-digestion.
This is the ONLY step that writes a file — it PRODUCEs the digestion plan.

SOURCE_ASSESSMENT (from step 1)
{{upstream.source_assessment}}

NOTE_BREAKDOWN (from step 3)
{{upstream.note_breakdown}}

CROSS_REF_PLAN (from step 4)
{{upstream.cross_ref_plan}}

Follow this procedure:

Assemble everything into the single digestion plan and write it to `plans/plan_digest_<source_slug>.md` (single plan for sources ≤30,000 words) or a master + sub-plan set (>30,000 words of source) — the single-vs-master split follows SOURCE WORDS, not note count, since note count scales with the active granularity. This is the ONLY step that writes a file — it PRODUCEs the plan `.md`.

Read `{{upstream.source_assessment}}`, `{{upstream.routing_decision}}`, `{{upstream.note_breakdown}}`, and `{{upstream.cross_ref_plan}}`, and lay them out under the required plan sections — using the CANONICAL section headings the review's deterministic scan checks for (Scope, Content Strategy, Source Pages (measured), Planned Notes, Section Coverage Map, Split Decisions, Summary Statistics & Building Block Distribution, Per-Note Related Notes Mapping, Density Re-Assessment, Undigested Terms Plan, Per-Phase Validation Gate, Entry Point Decision, Inlinks, Review Sign-Off) plus the working sections below: Objective, Routing Decision, Source Pages (measured word-count table — every figure COPIED VERBATIM from `source_assessment.pages[]`: `measured_words`, `code_blocks`, and the heading counts; never re-stated from memory, since the review's CP7 checks this table against the same ledger), Content Strategy, Section Coverage Map, Split Decisions, Planned Notes table, Content Size Assessment, Summary Statistics, Building Block Distribution, Cross-References to Add, Entry Point Decision, Undigested Terms Plan, Execution Phases (with per-phase validation gates), Note Format Definition, Validation Scripts, Pacing Rules, Density Re-Assessment, and Follow-up Recommendations.

Before finalizing, run the density re-assessment as a self-check: did any note compress too much and need a further split, was any source section omitted, does any note mix building blocks? Fix the plan before it is written.

Output the plan as a JSON object with `output_path` (the `plans/plan_digest_<source_slug>.md` path) and `body_markdown` (the complete plan file body, including its own YAML frontmatter with `status: pending` and the source URL). Do NOT call a file-write tool; the materializer writes the file from these two fields. Assemble the through-line into the
required plan sections (Objective, Routing Decision, Source measured
word-count table, Content Strategy, Section Coverage Map, Split
Decisions, Planned Notes, Content Size Assessment, Summary Statistics,
Building Block Distribution, Cross-References to Add, Entry Point
Decision, Undigested Terms Plan, Execution Phases with per-phase gates,
Note Format Definition, Validation Scripts, Pacing Rules, Density
Re-Assessment, Follow-up Recommendations). Run the density re-assessment
self-check and fix the plan before writing.

OUTPUT FORMAT — return ONLY a JSON object with two fields:
  - output_path: "plans/plan_digest_<source_slug>.md"
  - body_markdown: the COMPLETE plan file body, including its own YAML
    frontmatter (status: pending, source_url). Do NOT call any file-write
    tool; the materializer writes the file from these fields. No code
    fences around the JSON.

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
