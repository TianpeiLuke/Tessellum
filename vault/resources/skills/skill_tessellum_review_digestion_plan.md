---
tags:
  - resource
  - skill
  - procedure
  - review
  - planning
  - quality
keywords:
  - review digestion plan
  - tessellum-review-digestion-plan
  - plan sign-off
  - ready not ready verdict
  - checkpoint review
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
language: markdown
date of note: 2026-07-23
status: active
building_block: procedure
related_skill_headers: []
access_control_group: ["general"]
---

# Procedure: tessellum-review-digestion-plan (Canonical Body)

This is the canonical body for the `tessellum-review-digestion-plan` skill — Phase 3 of the plan → augment → review → execute digestion pipeline. It pairs with [`skill_tessellum_review_digestion_plan.pipeline.yaml`](skill_tessellum_review_digestion_plan.pipeline.yaml), the typed contract for Composer dispatch.

This skill is the **review → ready gate**. It performs a **READ-ONLY** sign-off review of the augmented digestion plan and returns a typed **READY / NOT READY** verdict that the sign-off approver consumes. It writes **no files** — every step is a `no_op` DESCRIBE step, so the skill's only vault side effect is `read_only`. Its four corpus_wide steps run against a single `plan_doc` artifact (not a per-leaf fan-out), chained by `depends_on`, each reading the prior via `{{upstream.X}}`, with the plan document flowing through as the through-line.

## Skill description <!-- :: section_id = skill_description :: -->

Final review and sign-off for a digestion plan before execution begins. This skill judges — it never mutates the plan. It runs the mandatory checkpoints across three grouped read-only passes: structure and gates (CP1 Related Notes step, CP2 all 8 GATEs (G1–G8) per batch, CP3 entry-point specification and discoverability), then density and terms (CP4 plan size, CP5 note-format alignment, CP6 density/BB-atomicity split promotion, CP7 measured source word counts, CP8 Undigested Terms Plan and Term-Note Authoring Requirements), and finally a consolidated verdict step. The verdict is a typed object — `{ ready: boolean, failures: [string] }` — where `ready` is true only when every checkpoint passed and `failures` enumerates the specific gaps to return to augmentation. Use AFTER `tessellum-augment-digestion-plan` completes the plan augmentation. Because this is the gate immediately before execution, once the verdict is READY, execution can begin against the same `plan_doc`.

## Step 1: Read the Plan <!-- :: section_id = step_1_read_plan :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on: []
materializer: no_op
output_key: plan_identity
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - plan_path
  - status
  - total_notes
  properties:
    plan_path:
      type: string
    status:
      type: string
    total_notes:
      type: integer
```

Step 1 of tessellum-review-digestion-plan: Read the Plan (identity + status gate).

Confirm status is `pending` (if `ready`/`completed`, report "Plan already
reviewed" and stop). Record the plan's identity (path, status, total planned
notes) for the downstream size/entry-point checks. **The CP1–CP8 checkpoints
read the full plan BY REFERENCE from `{{artifact.plan_text}}` — the durable
plan-of-record the driver injects via the artifact channel (P21-full) — so this
step does NOT re-emit the plan body at all (removing that lossy LLM re-emission
is the E16/E18 cure). It emits ONLY the plan's identity (path, status, count).**

Follow this procedure:

Read the augmented plan's identity from `{{artifact.plan_text}}` (or the leaf). Confirm `status: pending` and record the plan path + declared total-note count for the downstream size and entry-point checks. **The later checkpoints (CP1–CP8) read the full plan text BY REFERENCE from `{{artifact.plan_text}}` (the durable plan-of-record the driver injects), so this step is just the identity/status gate — it does not re-emit the plan body.**

Confirm the plan carries `status: pending` (not already `ready`, `in-progress`, or `completed`). If it is already `ready` or `completed`, report "Plan already reviewed" and skip the remaining checkpoints. Record the plan path and its declared total-note count so downstream size and entry-point checks have the number they need.

This is a read-only load — no file is written. Emit ONLY the plan's identity (path, status, total planned notes). **The CP1–CP8 checkpoints read the full plan by reference from `{{artifact.plan_text}}` (the durable plan-of-record the driver injects into the review leaf), NOT from a re-emission by this step — so this step no longer carries the plan body through its output at all, which is the E16/E18 root cure (an LLM re-typing of a tens-of-thousands-of-character plan drops sections and causes false rejections). This is read-only — write no file.**

Return ONLY the JSON object specified by expected_output_schema;
no prose, no code fences.

Plan file: {{leaf.plan_path}}

## Step 2: Check Structure & Gates (CP1–CP3) <!-- :: section_id = step_2_check_structure_and_gates :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- step_1_read_plan
materializer: no_op
output_key: structure_checks
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - cp1
  - cp2
  - cp3
  properties:
    cp1:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
    cp2:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
    cp3:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
```

Step 2 of tessellum-review-digestion-plan: Check Structure & Gates.

Read the plan via {{artifact.plan_text}} and run the structural
checkpoints per section "step_2_check_structure_and_gates":
  - CP1: a Related Notes step exists with per-note link mapping.
  - CP2: every execution phase has all 8 GATEs (G1–G8, incl. G3-Coverage and the G7/G8 discoverability pair).
  - CP3: entry point specified, CREATE-vs-UPDATE matches size, and
    every new note has a planned outside-folder inbound link (no
    graph island).

This is a READ-ONLY judgment — write no file. Report each checkpoint
as PASS/FAIL with the specific gap.

Return ONLY the JSON object specified by expected_output_schema;
no prose, no code fences.

---

Read the full augmented plan **directly from `{{artifact.plan_text}}`** (the durable plan-of-record the driver injects into the leaf — NOT a re-emitted copy) and run the three structural checkpoints. Reading the of-record text avoids the lossy-re-emission failure (E16/E18): the plan can be tens of thousands of characters and must be judged in full. This step verifies the plan is wired for connectivity, validation, and discoverability. Report each checkpoint as PASS or FAIL with the specific gap.

- **CP1 — Related Notes step.** Confirm the plan includes an explicit step to add a `## Related Notes` section to every captured note. Floor: each note links to at least the required number of relevancy-selected `term_dictionary/` term notes plus one entry-point back-link, each written as an indexed markdown link with a term description AND a relevancy statement (a bare link with no relevancy note FAILs). Well-documented topics should carry more references for better graph connectivity. FAIL if there is no per-note link mapping.

- **CP2 — ALL 8 GATEs (G1–G8) per batch.** Count execution phases (N) and GATE tables (M). Each table must contain the full contiguous gate set: G1-Format (skill-driven format check, including the no-mid-paragraph-hard-wrap prose rule), G2-Grounding (faithful to source), G3-Density (within the line/word/code-block ceilings) AND G3-Coverage (every source H2/H3 mapped — two rows, one gate number), G4-CrossRef (links resolve + entry point + inlinks), G5-Ghost (every reference verified to exist; ghosts resolved via the fix-ghost-references skill), G6-Broken (skill-driven broken-link check and fix), G7-Discoverability (every new note RECEIVES ≥1 inbound link from an existing note outside the digest folder — the Inlinks mapping executed), and G8-Discoverability-verified (DB in-degree ≥1 confirmed for every note at finalization). PASS only when M ≥ N and all eight gate numbers appear in each table; otherwise FAIL and list which phases and gates are missing — a non-contiguous sequence (e.g. G6→G8 with G7 absent, or G7/G8 collapsed into one row) is a FAIL naming the gap. Plans written before the 8-gate spec carry only G1-G4 and MUST FAIL with a recommendation to re-run augmentation.

- **CP3 — Entry point specified + discoverability.** Confirm the plan names at least one entry point to update (specific filename and the section to add/modify), and that the CREATE-vs-UPDATE decision matches the size threshold: UPDATE existing for small digests, CREATE a dedicated entry point plus UPDATE the parent hub for larger ones. Search the vault for additional related entry points a browsing user would expect to reach the new notes. Also confirm the plan's Inlink Mapping gives every new note at least one inbound link from an existing note OUTSIDE the digest folder, executed as a gated phase (not merely "recommended") so the cluster is not a graph island. FAIL with the specific gap (no entry point, size-mismatch, orphan CREATE, or notes with no planned inbound link).

## Step 3: Check Density & Terms (CP4–CP8) <!-- :: section_id = step_3_check_density_and_terms :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- step_2_check_structure_and_gates
materializer: no_op
output_key: density_checks
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - cp4
  - cp5
  - cp6
  - cp7
  - cp8
  properties:
    cp4:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
    cp5:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
    cp6:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
    cp7:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
          - DEFERRED
        gap:
          type:
          - string
          - 'null'
    cp8:
      type: object
      required:
      - result
      properties:
        result:
          type: string
          enum:
          - PASS
          - FAIL
        gap:
          type:
          - string
          - 'null'
```

Step 3 of tessellum-review-digestion-plan: Check Density & Terms.

Read the plan via {{artifact.plan_text}} and the structural findings via
{{upstream.structure_checks}}, then run the checkpoints per section
"step_3_check_density_and_terms":
  - CP4: plan size within ceiling (or sub-plans defined).
  - CP5: note format aligned; derived from an existing target note WHEN the target dir has notes, else from the note-type contract (bootstrap).
  - CP6: borderline notes promoted to splits (default is SPLIT).
  - CP7: plan estimates verified against the MEASURED SOURCE LEDGER below (identify_source's pages[]); never a live fetch
    (mark DEFERRED if pages are unreadable).
  - CP8: Undigested Terms Plan + Term-Note Authoring Requirements
    present, MUST-language, dedup/collision audit performed.

This is a READ-ONLY judgment — write no file. Report each PASS/FAIL
(CP7 may be DEFERRED) with the specific gap.

Return ONLY the JSON object specified by expected_output_schema;
no prose, no code fences.

---

Read the full augmented plan **directly from `{{artifact.plan_text}}`** (the durable plan-of-record, not a re-emitted copy) and the structural findings from `{{upstream.structure_checks}}`, then run the density and term-coverage checkpoints. Report each as PASS or FAIL with the specific gap.

- **CP4 — Plan size manageable.** Count total planned notes. If it exceeds the single-plan ceiling, the plan MUST split into independently executable sub-plans with cross-references documented. PASS when within the ceiling or when sub-plans are defined; FAIL when oversized with no split strategy.

- **CP5 — Note format aligned and DERIVED (bootstrap-aware).** Extract the plan's Note Format Definition (YAML template + H2 conventions). WHEN the target directory contains existing notes: the format must be DERIVED from a real target-dir note — the plan must NAME the note and QUOTE its actual frontmatter/headers; FAIL on an invented format, and FAIL HARD if the plan cites a note it cannot quote or one that does not exist (a fabricated derivation is worse than none). WHEN the target directory is EMPTY or newly created (a bootstrap run — there is nothing to derive from): derivation from the note-type contract / format templates (the single frontmatter source of truth) PASSES — do NOT demand derivation from nonexistent notes; still confirm the required frontmatter keys are present, forbidden fields are excluded, and still FAIL a plan that CLAIMS derivation from a specific note without quoting it.

- **CP6 — Density and BB atomicity (promote splits).** A deterministic plan gate (FZ 20k9d4) ALREADY hard-fails the OBJECTIVE breaches — any note with `approx_words` ≥ 1800 (PLAN-004), a multi-BB `building_block` value (PLAN-005), or an uncovered source section (PLAN-006) — and forces a re-plan; the remedy may be a split OR a coverage-map rearrangement (the gate does not prescribe which). This checkpoint is the SUBJECTIVE layer ON TOP of that gate: scan for borderline cases the number-based gate cannot see (a note under 1800 words that still covers many unrelated H2 sections, or content that reads as mixed-BB even though the `building_block` field is a single valid token). The default for a borderline note is SPLIT unless there is documented justification to keep it whole (single cohesive theme, small total word count, no BB mixing). FAIL if borderline cases are unaddressed; list each with a recommendation (split or rearrange).

- **CP7 — Source word counts verified against the MEASURED LEDGER.** The plan phase's `identify_source` step already MEASURED every source page — the MEASURED SOURCE LEDGER injected below carries `measured_words` / `code_blocks` / `headings` per page. Verify against THIS ledger; do NOT attempt to fetch or re-read live pages (this reviewer runs single-shot with no tools — a fetch is impossible by construction, and the ledger is the grounded measurement the plan was built from). Check: (1) every page in the plan's Source section appears in the ledger; (2) the plan's per-page word-count estimates are within tolerance of `measured_words` — if any page's measured count is well above the plan's estimate, density was under-estimated and the affected notes must be re-split — FAIL naming the pages and required splits; (3) the Section Coverage Map's section names correspond to the ledger's measured `headings` (no invented sections). PASS when estimates match the ledger. Mark CP7 DEFERRED ONLY when the ledger itself is absent from the plan context (a pre-measurement plan) — never because a URL was unreachable.

- **CP8 — Undigested Terms Plan + Term-Note Authoring Requirements.** Confirm the augmented plan carries both the `## Undigested Terms Plan` section (every row with a defined Capture Phase and best-fit glossary) and the `## Term-Note Authoring Requirements` section (YAML spec, required H1/H2 order, multi-source research mandate stated in MUST-language, the full-term-note mandate of enriched notes with the required related-terms floor plus external references, and per-term invocation of the term-note capture skill rather than inline authoring). Also confirm a term-slug specificity and all-notes collision/dedup audit was performed (renamed too-general slugs, removed duplicates that existing substantive notes already cover). FAIL if any section is missing, uses soft-language, ships thin stubs as final, or skipped the dedup audit — return to augmentation with the specific gap.

MEASURED SOURCE LEDGER (identify_source's measured pages[] — verify CP7 against THIS, never a live fetch):

{{leaf.pages}}

## Step 4: Report Verdict <!-- :: section_id = step_4_report_verdict :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- step_2_check_structure_and_gates
- step_3_check_density_and_terms
materializer: no_op
output_key: verdict
expected_output_schema:
  type: object
  required:
  - ready
  - failures
  properties:
    ready:
      type: boolean
      description: true only when EVERY checkpoint passed.
    failures:
      type: array
      items:
        type: string
      description: One string per failed checkpoint; empty when ready.
```

Step 4 of tessellum-review-digestion-plan: Report Verdict.

Read the structural findings via {{upstream.structure_checks}} and the
density/term findings via {{upstream.density_checks}}. Aggregate every
checkpoint per section "step_4_report_verdict".

Set `ready` to true ONLY when all checkpoints passed (partial passes do
not count). Populate `failures` with one string per failed checkpoint
naming the checkpoint and what to fix; empty array when ready.

This is the typed READY / NOT-READY verdict the sign-off approver
consumes. This step JUDGES only — write no file, do not mutate the plan.

Return ONLY the JSON object specified by expected_output_schema;
no prose, no code fences.

---

Read the structural findings from `{{upstream.structure_checks}}` and the density/term findings from `{{upstream.density_checks}}`, then emit the consolidated typed verdict the sign-off approver consumes. This step judges only — it writes no files and does not change the plan's status.

Aggregate every checkpoint result. Set `ready` to `true` only when ALL checkpoints passed (partial passes do not count — a plan that fails even one checkpoint is NOT READY). Populate `failures` with one human-readable string per failed checkpoint, naming the checkpoint and what must be fixed; when `ready` is `true`, `failures` is an empty array.

Return exactly `{ ready: <boolean>, failures: [<string>, ...] }`. This is the READY / NOT-READY verdict: when READY, the approver may advance the same `plan_doc` to execution; when NOT READY, the plan is returned to augmentation with the enumerated failures. This skill never mutates the plan — updating `status` to `ready` is the approver's action, not this review's.

## Related skills <!-- :: section_id = related_skills :: -->

The four phases of the plan → augment → review → execute digestion pipeline:

- [`skill_tessellum_plan_digestion.md`](skill_tessellum_plan_digestion.md) — Phase 1 — produces the plan_doc.
- [`skill_tessellum_augment_digestion_plan.md`](skill_tessellum_augment_digestion_plan.md) — Phase 2 — enriches the plan_doc with gates + cross-ref contract.
- [`skill_tessellum_review_digestion_plan.md`](skill_tessellum_review_digestion_plan.md) — Phase 3 — the read-only READY/NOT-READY sign-off gate. ← this skill
- [`skill_tessellum_execute_digestion_plan.md`](skill_tessellum_execute_digestion_plan.md) — Phase 4 — writes the notes from a ready plan.
