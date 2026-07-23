---
tags:
  - resource
  - skill
  - procedure
  - execution
  - multi_agent
  - dynamic_workflow
keywords:
  - execute digestion plan
  - digestion pipeline phase 4
  - master orchestrator
  - plan amendment
  - per-batch contract extraction
  - dynamic workflow dispatch
  - independent post-hoc verification
topics:
  - Skill Procedures
  - Multi-Agent Execution
  - Knowledge Ingestion
language: markdown
date of note: 2026-07-23
status: active
building_block: procedure
access_control_group: ["general"]
pipeline_metadata: ./skill_tessellum_execute_digestion_plan.pipeline.yaml
---

# Procedure: tessellum-execute-digestion-plan (Canonical Body)

This is the canonical body for the `tessellum-execute-digestion-plan` skill — **Phase 4 (EXECUTE)** of the plan → augment → review → execute digestion pipeline. It pairs with [`skill_tessellum_execute_digestion_plan.pipeline.yaml`](skill_tessellum_execute_digestion_plan.pipeline.yaml), the typed Composer contract.

The plan is the through-line artifact. A single reviewed plan doc (`status: ready`) flows through five corpus-wide reasoning steps and one per-leaf write step: the master orchestrator preflights the plan, boots + amends it against the live source, extracts per-batch sub-agent contracts, dispatches one writer per planned note (the fan-out wave), then runs an independent post-hoc sweep before the run is called complete. Use AFTER `tessellum-review-digestion-plan` returns READY.

## Preflight — Verify the Plan Is Ready <!-- :: section_id = preflight :: -->

Confirm the plan is executable before any agent runs. The plan file must exist and its frontmatter must declare `status: ready`. Refuse to start if the status is `pending` or `in-progress` (review sign-off has not happened), if the plan is missing its Planned Notes table (or, for a master plan, its Sub-Plans Index table), or if a HEAD-check on one or two source URLs shows they are unreachable. A master plan is never executed directly — this skill operates on exactly ONE ready sub-plan at a time, in priority order. Emit a structured go/no-go verdict recording the plan path, its measured status, the planned-note count, and any refusal reason. Note the entry-point timing rule: for master+sub-plans, the dedicated `entry_<slug>.md` hub is created as a standalone pre-step BEFORE the first sub-plan executes, so every new note can receive its back-link.

## Boot and Amend — Master Reads Plan, Spot-Checks Source, Corrects <!-- :: section_id = boot_and_amend :: -->

The master orchestrator reads the ready plan start to finish AND spot-checks one or two of the densest source pages with the same tool the plan used, then records a Plan Boot Report (pages spot-checked, measured word count vs. the plan's estimate, and any defects such as placeholder strings, mismatched section counts, or missing required fields). The master then applies amendments the plan author could not have foreseen. Density corrections (split or merge a note), building-block re-classification, and reference-mapping corrections are auto-applied and recorded in a `## Plan Amendments` table, each traced to a concrete observation (never a stylistic preference). Re-routing to a different directory, dropping a planned note, changing a source URL, or adding a brand-new note are PAUSE-for-user-approval actions — report and wait. The rule is correct the plan, do not redesign it: if the plan's structure is fundamentally wrong (e.g. wrong source of truth), stop and route back to augment/plan rather than patching it here. Read the prior preflight verdict from `{{upstream.preflight_report}}`.

## Extract Contracts — Derive Per-Batch Sub-Agent Contracts <!-- :: section_id = extract_contracts :: -->

Project the amended plan into the self-contained briefs each writer sub-agent will actually receive. Build one shared contract per run by extracting the plan's Note Format Definition (the YAML template + forbidden fields), Pacing Rules, per-phase Gate tables, Important Constraints (BB atomicity, density caps, no fabrication, verbatim code), source provenance with measured word counts, and the worked-example pilot path that anchors quality. Add the non-negotiable absolute rules (read source first; no fabrication — use the sanctioned honest markers when a fact is absent; no forbidden placeholder strings; return split-needed rather than writing an over-dense or mixed-BB note) and the structured return schema each sub-agent must emit. Then, for each batch in the plan's batch table, extract the per-note rows (note, target path, source path/URL, related notes, inlinks) into a per-batch assignment. Extraction is a faithful projection only: it may NOT introduce content absent from the plan — if a required cross-reference is missing, return to the amend step and fix the plan first. Read the boot report from `{{upstream.boot_report}}`.

## Dispatch Notes — Write Each Planned Note (Fan-Out Wave) <!-- :: section_id = dispatch_notes :: -->

This is the write phase and the ONLY per-leaf step: one sub-agent per planned note, dispatched as a wave (this is the step that maps onto `run_pipeline_dynamic`'s wave-parallel scheduler). Each agent receives the shared contract plus its per-batch assignment plus the worked-example pilot, reads its assigned source page(s) FIRST, and writes exactly one note that matches the pilot's shape and the plan's format definition — verbatim code, honest inferred/not-in-source markers, one building_block per note. Concurrency is auto-capped; the wave runs enrich → validate → bounded fix (at most two rounds) with a master validator that runs the gate script, does a live-source faithfulness spot-check, checks cross-reference integrity, and confirms the domain completeness invariant. Source-reading agents fail closed: an auth failure sets `source_fetch_ok=false` and status `auth_blocked` rather than falling back to memory. Read the per-batch contracts from `{{upstream.batch_contracts}}`.

OUTPUT FORMAT — markdown with YAML frontmatter (NOT JSON). The frontmatter MUST contain the key `output_path` whose value is the vault-relative `.md` path for this note; everything after the closing `---` IS the note body, written verbatim.

## Verify — Independent Post-Hoc Sweep <!-- :: section_id = verify :: -->

The wave's "all batches passed" is a claim, not proof; this cross-leaf step is the independent backstop that runs once over the full output set on disk, regardless of what any in-loop validator reported. Re-run the plan's full gate suite across ALL new notes (not per batch), run the format check, run the broken-link check (must report zero), rebuild the database and query for ghost references from the new notes (must be zero), and run the G8 discoverability check (every new note must have at least one inbound link from OUTSIDE its own folder — any graph-island note fails). Deduplication, ghost-reference, and coverage findings are surfaced here. Any residual issue is patched in place and re-verified; the run is NOT complete while broken, ghost, format, or graph-island issues remain. Emit a `verify_report` rollup (notes created vs. planned, gate results, broken-link count, ghost count, graph-island count, and an overall pass/fail) so the orchestrator has an auditable completion record. Read the written note set from `{{upstream.note_body}}`.

## Related skills <!-- :: section_id = related_skills :: -->

The four phases of the plan → augment → review → execute digestion pipeline:

- [`skill_tessellum_plan_digestion.md`](skill_tessellum_plan_digestion.md) — Phase 1 — produces the plan_doc.
- [`skill_tessellum_augment_digestion_plan.md`](skill_tessellum_augment_digestion_plan.md) — Phase 2 — enriches the plan_doc with gates + cross-ref contract.
- [`skill_tessellum_review_digestion_plan.md`](skill_tessellum_review_digestion_plan.md) — Phase 3 — the read-only READY/NOT-READY sign-off gate.
- [`skill_tessellum_execute_digestion_plan.md`](skill_tessellum_execute_digestion_plan.md) — Phase 4 — writes the notes from a ready plan. ← this skill
