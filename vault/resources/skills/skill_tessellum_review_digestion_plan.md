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
pipeline_metadata: ./skill_tessellum_review_digestion_plan.pipeline.yaml
access_control_group: ["general"]
---

# Procedure: tessellum-review-digestion-plan (Canonical Body)

This is the canonical body for the `tessellum-review-digestion-plan` skill — Phase 3 of the plan → augment → review → execute digestion pipeline. It pairs with [`skill_tessellum_review_digestion_plan.pipeline.yaml`](skill_tessellum_review_digestion_plan.pipeline.yaml), the typed contract for Composer dispatch.

This skill is the **review → ready gate**. It performs a **READ-ONLY** sign-off review of the augmented digestion plan and returns a typed **READY / NOT READY** verdict that the sign-off approver consumes. It writes **no files** — every step is a `no_op` DESCRIBE step, so the skill's only vault side effect is `read_only`. Its four corpus_wide steps run against a single `plan_doc` artifact (not a per-leaf fan-out), chained by `depends_on`, each reading the prior via `{{upstream.X}}`, with the plan document flowing through as the through-line.

## Skill description <!-- :: section_id = skill_description :: -->

Final review and sign-off for a digestion plan before execution begins. This skill judges — it never mutates the plan. It runs the mandatory checkpoints across three grouped read-only passes: structure and gates (CP1 Related Notes step, CP2 all 7 GATEs per batch, CP3 entry-point specification and discoverability), then density and terms (CP4 plan size, CP5 note-format alignment, CP6 density/BB-atomicity split promotion, CP7 measured source word counts, CP8 Undigested Terms Plan and Term-Note Authoring Requirements), and finally a consolidated verdict step. The verdict is a typed object — `{ ready: boolean, failures: [string] }` — where `ready` is true only when every checkpoint passed and `failures` enumerates the specific gaps to return to augmentation. Use AFTER `tessellum-augment-digestion-plan` completes the plan augmentation. Because this is the gate immediately before execution, once the verdict is READY, execution can begin against the same `plan_doc`.

## Step 1: Read the Plan <!-- :: section_id = step_1_read_plan :: -->

Read the augmented plan file that augmentation produced. This step establishes the through-line artifact — the `plan_doc` — that every later checkpoint reads via `{{upstream.plan_doc}}`.

Confirm the plan carries `status: pending` (not already `ready`, `in-progress`, or `completed`). If it is already `ready` or `completed`, report "Plan already reviewed" and skip the remaining checkpoints. Record the plan path and its declared total-note count so downstream size and entry-point checks have the number they need.

This is a read-only load — no file is written. Emit the plan's identity (path, status, total planned notes) plus the full plan text so the structure and density passes can inspect it without re-reading from disk.

## Step 2: Check Structure & Gates (CP1–CP3) <!-- :: section_id = step_2_check_structure_and_gates :: -->

Read the `plan_doc` from `{{upstream.plan_doc}}` and run the three structural checkpoints. This step verifies the plan is wired for connectivity, validation, and discoverability. Report each checkpoint as PASS or FAIL with the specific gap.

- **CP1 — Related Notes step.** Confirm the plan includes an explicit step to add a `## Related Notes` section to every captured note. Floor: each note links to at least the required number of relevancy-selected `term_dictionary/` term notes plus one entry-point back-link, each written as an indexed markdown link with a term description AND a relevancy statement (a bare link with no relevancy note FAILs). Well-documented topics should carry more references for better graph connectivity. FAIL if there is no per-note link mapping.

- **CP2 — ALL 7 GATEs per batch.** Count execution phases (N) and GATE tables (M). Each table must contain all seven gates: G1-Format (skill-driven format check, including the no-mid-paragraph-hard-wrap prose rule), G2-Grounding (faithful to source), G3-Density (within the line/word/code-block ceilings), G3-Coverage (every source H2/H3 mapped), G4-CrossRef (links resolve + entry point + inlinks), G5-Ghost (every reference verified to exist; ghosts resolved via the fix-ghost-references skill), and G6-Broken (skill-driven broken-link check and fix). PASS only when M ≥ N and all seven gates appear in each table; otherwise FAIL and list which phases and gates are missing. Plans written before the 7-gate spec carry only G1-G4 and MUST FAIL with a recommendation to re-run augmentation.

- **CP3 — Entry point specified + discoverability.** Confirm the plan names at least one entry point to update (specific filename and the section to add/modify), and that the CREATE-vs-UPDATE decision matches the size threshold: UPDATE existing for small digests, CREATE a dedicated entry point plus UPDATE the parent hub for larger ones. Search the vault for additional related entry points a browsing user would expect to reach the new notes. Also confirm the plan's Inlink Mapping gives every new note at least one inbound link from an existing note OUTSIDE the digest folder, executed as a gated phase (not merely "recommended") so the cluster is not a graph island. FAIL with the specific gap (no entry point, size-mismatch, orphan CREATE, or notes with no planned inbound link).

## Step 3: Check Density & Terms (CP4–CP8) <!-- :: section_id = step_3_check_density_and_terms :: -->

Read the `plan_doc` from `{{upstream.plan_doc}}` and the structural findings from `{{upstream.structure_checks}}`, then run the density and term-coverage checkpoints. Report each as PASS or FAIL with the specific gap.

- **CP4 — Plan size manageable.** Count total planned notes. If it exceeds the single-plan ceiling, the plan MUST split into independently executable sub-plans with cross-references documented. PASS when within the ceiling or when sub-plans are defined; FAIL when oversized with no split strategy.

- **CP5 — Note format aligned and DERIVED.** Extract the plan's Note Format Definition (YAML template + H2 conventions) and compare it against an ACTUAL existing note in the target directory. The format must be copied from a real target-dir note, not invented. Confirm forbidden fields are excluded. FAIL if fields are misaligned or the format was written from intuition rather than derived from an existing note.

- **CP6 — Density and BB atomicity (promote splits).** Scan all planned notes for borderline cases (near the line/code-block ceilings, covering many H2 sections, or mixing building-block content). The default for a borderline note is SPLIT unless there is documented justification to keep it whole (single cohesive theme, small total word count, no BB mixing). FAIL if borderline cases are unaddressed; list each with a recommendation.

- **CP7 — Source word counts measured, not guessed.** Spot-check 2-3 source pages (prefer the densest, most-mapped ones) by re-reading them and counting actual words. Compare measured against the plan's estimates. If any page's actual count is well above the plan estimate, the plan under-estimated density and the affected notes must be re-split — FAIL and name the pages and required splits. PASS when spot-checked pages are within tolerance of their estimates. If pages cannot be read (auth required), mark CP7 DEFERRED and note which pages were unverifiable.

- **CP8 — Undigested Terms Plan + Term-Note Authoring Requirements.** Confirm the augmented plan carries both the `## Undigested Terms Plan` section (every row with a defined Capture Phase and best-fit glossary) and the `## Term-Note Authoring Requirements` section (YAML spec, required H1/H2 order, multi-source research mandate stated in MUST-language, the full-term-note mandate of enriched notes with the required related-terms floor plus external references, and per-term invocation of the term-note capture skill rather than inline authoring). Also confirm a term-slug specificity and all-notes collision/dedup audit was performed (renamed too-general slugs, removed duplicates that existing substantive notes already cover). FAIL if any section is missing, uses soft-language, ships thin stubs as final, or skipped the dedup audit — return to augmentation with the specific gap.

## Step 4: Report Verdict <!-- :: section_id = step_4_report_verdict :: -->

Read the structural findings from `{{upstream.structure_checks}}` and the density/term findings from `{{upstream.density_checks}}`, then emit the consolidated typed verdict the sign-off approver consumes. This step judges only — it writes no files and does not change the plan's status.

Aggregate every checkpoint result. Set `ready` to `true` only when ALL checkpoints passed (partial passes do not count — a plan that fails even one checkpoint is NOT READY). Populate `failures` with one human-readable string per failed checkpoint, naming the checkpoint and what must be fixed; when `ready` is `true`, `failures` is an empty array.

Return exactly `{ ready: <boolean>, failures: [<string>, ...] }`. This is the READY / NOT-READY verdict: when READY, the approver may advance the same `plan_doc` to execution; when NOT READY, the plan is returned to augmentation with the enumerated failures. This skill never mutates the plan — updating `status` to `ready` is the approver's action, not this review's.

## Related skills <!-- :: section_id = related_skills :: -->

The four phases of the plan → augment → review → execute digestion pipeline:

- [`skill_tessellum_plan_digestion.md`](skill_tessellum_plan_digestion.md) — Phase 1 — produces the plan_doc.
- [`skill_tessellum_augment_digestion_plan.md`](skill_tessellum_augment_digestion_plan.md) — Phase 2 — enriches the plan_doc with gates + cross-ref contract.
- [`skill_tessellum_review_digestion_plan.md`](skill_tessellum_review_digestion_plan.md) — Phase 3 — the read-only READY/NOT-READY sign-off gate. ← this skill
- [`skill_tessellum_execute_digestion_plan.md`](skill_tessellum_execute_digestion_plan.md) — Phase 4 — writes the notes from a ready plan.
