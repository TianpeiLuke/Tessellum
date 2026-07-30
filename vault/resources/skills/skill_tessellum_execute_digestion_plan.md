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
---

# Procedure: tessellum-execute-digestion-plan (Canonical Body)

This is the canonical body for the `tessellum-execute-digestion-plan` skill — **Phase 4 (EXECUTE)** of the plan → augment → review → execute digestion pipeline. It pairs with [`skill_tessellum_execute_digestion_plan.pipeline.yaml`](skill_tessellum_execute_digestion_plan.pipeline.yaml), the typed Composer contract.

The plan is the through-line artifact. A single reviewed plan doc (`status: ready`) flows through five corpus-wide reasoning steps and one per-leaf write step: the master orchestrator preflights the plan, boots + amends it against the live source, extracts per-batch sub-agent contracts, dispatches one writer per planned note (the fan-out wave), then runs an independent post-hoc sweep before the run is called complete. Use AFTER `tessellum-review-digestion-plan` returns READY.

## Preflight — Verify the Plan Is Ready <!-- :: section_id = preflight :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on: []
materializer: no_op
output_key: preflight_report
expected_output_schema:
  type: object
  required:
  - plan_path
  - status
  - ready
  - planned_note_count
  properties:
    plan_path:
      type: string
      description: Vault/plans-relative path of the sub-plan being executed
    status:
      enum:
      - ready
      - pending
      - in-progress
      - unknown
      description: Measured plan frontmatter status; only `ready` may proceed
    ready:
      type: boolean
      description: "Go/no-go verdict \u2014 true only if status=ready, Planned Notes table\
        \ present, source reachable"
    planned_note_count:
      type: integer
      description: Rows in the plan's Planned Notes table (== number of dispatch_notes leaves)
    refusal_reason:
      type:
      - string
      - 'null'
      description: Why the run was refused, or null when ready
inputs:
- name: leaf.plan_path
  required: false
```

You are the master orchestrator verifying that a digestion plan is
ready to execute.

LEAF METADATA
- plan_path: {{leaf.plan_path}}

Follow this procedure:

Confirm the plan is executable before any agent runs. The plan file must exist and its frontmatter must declare `status: ready`. Refuse to start if the status is `pending` or `in-progress` (review sign-off has not happened), if the plan is missing its Planned Notes table (or, for a master plan, its Sub-Plans Index table), or if a HEAD-check on one or two source URLs shows they are unreachable. A master plan is never executed directly — this skill operates on exactly ONE ready sub-plan at a time, in priority order. Emit a structured go/no-go verdict recording the plan path, its measured status, the planned-note count, and any refusal reason. Note the entry-point timing rule: for master+sub-plans, the dedicated `entry_<slug>.md` hub is created as a standalone pre-step BEFORE the first sub-plan executes, so every new note can receive its back-link. Confirm the plan exists, its
frontmatter status is `ready`, it has a Planned Notes table, and its
source URLs HEAD-check reachable. Return ONLY the JSON object
specified by expected_output_schema; no prose.

## Boot and Amend — Master Reads Plan, Spot-Checks Source, Corrects <!-- :: section_id = boot_and_amend :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- preflight
materializer: no_op
output_key: boot_report
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - pages_spot_checked
  - amendments
  - boot_report_written
  properties:
    pages_spot_checked:
      type: array
      description: Densest source pages the master re-read, with measured vs. planned word
        counts
      items:
        type: object
        required:
        - source_ref
        - measured_words
        - planned_words
        properties:
          source_ref:
            type: string
          measured_words:
            type: integer
          planned_words:
            type: integer
    amendments:
      type: array
      description: Auto-applied plan amendments (density/BB/reference corrections), each traced
        to an observation
      items:
        type: object
        required:
        - section
        - original
        - amended
        - rationale
        properties:
          section:
            type: string
          original:
            type: string
          amended:
            type: string
          rationale:
            type: string
    pending_approvals:
      type: array
      description: PAUSE-for-user amendments (re-route / drop / source change / new note)
        awaiting approval
      items:
        type: string
    boot_report_written:
      type: boolean
      description: 'True once the ## Plan Boot Report + ## Plan Amendments sections are appended
        to the plan'
inputs:
- name: upstream.preflight_report
  required: true
```

You are the master orchestrator booting the plan and applying
pre-fan-out amendments.

PREFLIGHT_REPORT (from the preflight step)
{{upstream.preflight_report}}

Follow this procedure:

The master orchestrator reads the ready plan start to finish AND spot-checks one or two of the densest source pages with the same tool the plan used, then records a Plan Boot Report (pages spot-checked, measured word count vs. the plan's estimate, and any defects such as placeholder strings, mismatched section counts, or missing required fields). The master then applies amendments the plan author could not have foreseen. Density corrections (split or merge a note), building-block re-classification, and reference-mapping corrections are auto-applied and recorded in a `## Plan Amendments` table, each traced to a concrete observation (never a stylistic preference). Re-routing to a different directory, dropping a planned note, changing a source URL, or adding a brand-new note are PAUSE-for-user-approval actions — report and wait. The rule is correct the plan, do not redesign it: if the plan's structure is fundamentally wrong (e.g. wrong source of truth), stop and route back to augment/plan rather than patching it here. Read the prior preflight verdict from `{{upstream.preflight_report}}`. Read the plan end to end,
spot-check the densest source page(s), and auto-apply density / BB /
reference-mapping corrections (recording each in ## Plan Amendments);
queue re-route / drop / source-change / new-note changes for user
approval. Correct the plan, do NOT redesign it. Return ONLY the JSON
object specified by expected_output_schema; no prose.

## Extract Contracts — Derive Per-Batch Sub-Agent Contracts <!-- :: section_id = extract_contracts :: -->

```yaml
role: CORE
aggregation: corpus_wide
batchable: false
depends_on:
- boot_and_amend
materializer: no_op
output_key: batch_contracts
max_tokens: 32000
timeout_seconds: 900
expected_output_schema:
  type: object
  required:
  - shared_contract_path
  - batches
  properties:
    shared_contract_path:
      type: string
      description: Path of the one-per-run shared contract extracted from the plan (YAML template,
        gates, absolute rules, return schema, pilot path)
    batches:
      type: array
      description: Per-batch assignment briefs projected faithfully from the plan
      items:
        type: object
        required:
        - batch_id
        - contract_path
        - notes
        properties:
          batch_id:
            type: string
          contract_path:
            type: string
          notes:
            type: array
            description: 'Per-note rows: note, target path, source ref, related notes, inlinks'
            items:
              type: object
              required:
              - note
              - target_path
              - source_ref
              properties:
                note:
                  type: string
                target_path:
                  type: string
                source_ref:
                  type: string
                related_notes:
                  type: array
                  items:
                    type: string
                inlinks:
                  type: array
                  items:
                    type: string
    missing_from_plan:
      type: array
      description: Required fields absent from the plan (empty => faithful projection possible;
        non-empty => return to boot_and_amend)
      items:
        type: string
inputs:
- name: upstream.boot_report
  required: true
```

You are the master orchestrator extracting per-batch sub-agent
contracts from the amended plan.

BOOT_REPORT (from the boot_and_amend step)
{{upstream.boot_report}}

Follow this procedure:

Project the amended plan into the self-contained briefs each writer sub-agent will actually receive. Build one shared contract per run by extracting the plan's Note Format Definition (the YAML template + forbidden fields), Pacing Rules, per-phase Gate tables, Important Constraints (BB atomicity, density caps, no fabrication, verbatim code), source provenance with measured word counts, and the worked-example pilot path that anchors quality. Add the non-negotiable absolute rules (read source first; no fabrication — use the sanctioned honest markers when a fact is absent; no forbidden placeholder strings; return split-needed rather than writing an over-dense or mixed-BB note) and the structured return schema each sub-agent must emit. Then, for each batch in the plan's batch table, extract the per-note rows (note, target path, source path/URL, related notes, inlinks) into a per-batch assignment. Extraction is a faithful projection only: it may NOT introduce content absent from the plan — if a required cross-reference is missing, return to the amend step and fix the plan first. Read the boot report from `{{upstream.boot_report}}`. Build the one-per-run shared
contract (YAML template + forbidden fields, pacing rules, gate spec,
absolute rules, structured return schema, pilot worked-example path)
and one assignment brief per batch. Faithful projection only — if a
required cross-reference is missing from the plan, list it in
missing_from_plan and stop. Return ONLY the JSON object specified by
expected_output_schema; no prose.

## Dispatch Notes — Write Each Planned Note (Fan-Out Wave) <!-- :: section_id = dispatch_notes :: -->

```yaml
role: CORE
aggregation: per_leaf
batchable: false
depends_on:
- extract_contracts
materializer: body_markdown_frontmatter_to_file
output_key: note_body
timeout_seconds: 600
expected_output_schema:
  type: object
  required:
  - output_path
  properties:
    output_path:
      type: string
      description: Vault-relative .md path for this planned note
      pattern: ^[a-z0-9_/]+\.md$
inputs:
- name: leaf.note
  required: false
- name: leaf.target_path
  required: false
- name: leaf.source_ref
  required: false
- name: leaf.owned_sections_md
  required: false
- name: artifact.plan_text
  required: true
- name: artifact.source_excerpt
  required: true
- name: leaf.related_references_md
  required: false
- name: leaf.type_contract_md
  required: false
- name: upstream.batch_contracts
  required: true
```

You are a writer sub-agent producing exactly one planned note. One
agent per note; isolate your context to a single source.

LEAF METADATA
- note: {{leaf.note}}
- target_path: {{leaf.target_path}}
- source_ref: {{leaf.source_ref}}

YOUR ASSIGNED SECTIONS (code-measured: the coverage-map rows THIS note
owns, joined with the source ledger's measured pages. These sections are
your scope — cover them in this note. An empty block means the plan
carried no per-note coverage rows; fall back to the plan's own mapping):
{{leaf.owned_sections_md}}

PLAN OF RECORD (read by reference from the run's working store — use it
for cross-note context and the format definition; NEVER re-emit it):
{{artifact.plan_text}}

SOURCE MATERIAL (read by reference from the run's working store — read
this FIRST and ground every claim in it; it is the single of-record
source copy all writers share):
{{artifact.source_excerpt}}

RELATED NOTES (retrieved per-note by relevance to THIS note's thesis;
each is an EXISTING vault note with a path already resolved relative to
this note's target_path — ready to paste as a markdown link):
{{leaf.related_references_md}}

NOTE-TYPE CONTRACT (resolved from this note's target_path → its template
flavor; the required `## H2` sections + reference rule for THIS note's
type. An empty block means the type could not be resolved — fall back to
the plan's format definition and the pilot worked example):
{{leaf.type_contract_md}}

PER-BATCH CONTRACTS (from the extract_contracts step — read your
shared contract + batch assignment + pilot worked example)
{{upstream.batch_contracts}}

Follow this procedure:

This is the write phase and the ONLY per-leaf step: one sub-agent per planned note, dispatched as a wave (this is the step that maps onto `run_pipeline_dynamic`'s wave-parallel scheduler). Each agent receives the shared contract plus its per-batch assignment plus the worked-example pilot, reads its assigned source page(s) FIRST, and writes exactly one note that matches the pilot's shape and the plan's format definition — verbatim code, honest inferred/not-in-source markers, one building_block per note. Concurrency is auto-capped; the wave runs enrich → validate → bounded fix (at most two rounds) with a master validator that runs the gate script, does a live-source faithfulness spot-check, checks cross-reference integrity, and confirms the domain completeness invariant. Source-reading agents fail closed: an auth failure sets `source_fetch_ok=false` and status `auth_blocked` rather than falling back to memory. Read the per-batch contracts from `{{upstream.batch_contracts}}`.

RELATED NOTES → `## Related Notes` (knowledge-graph edges). The note MUST end with a `## Related Notes` section that links relevance-selected EXISTING vault notes — these links are how the knowledge graph is built (the indexer turns each `[title](relative/path.md)` into an edge). This is the vault's canonical graph-edge convention: use `## Related Notes` for internal note-to-note links, NOT `## References` (a `## References` section is reserved for external-URL citations when present). Use the `RELATED NOTES` block above (`{{leaf.related_references_md}}`): it was retrieved per-note by relevance to this note's thesis, and each path is ALREADY resolved relative to this note's `target_path`, so paste the links as-is. You MAY drop a suggestion that is genuinely irrelevant to this note and MAY add a link you know is relevant that retrieval missed, but do NOT invent paths — only link notes that exist. If the block is empty (retrieval found nothing / no index yet), still add a `## Related Notes` section with any relevant links you can ground from the plan's cross-reference mapping. Keep every link a relative markdown link ending in `.md`.

NOTE-TYPE CONTRACT → required sections. The `NOTE-TYPE CONTRACT` block above (`{{leaf.type_contract_md}}`) names this note's type (resolved from its `target_path`) and the `## H2` sections that type requires — treat that section list as a FLOOR for this note (include each one; you MAY add type-appropriate sections beyond it). This is why the writer produces the right shape per type in one run: a term note gets Definition/Examples/References, a how-to gets Setup/Steps/Validation/References, an argument gets Claim/Reason/Evidence/References, and so on. If the block is empty (the type could not be resolved from the path), fall back to the plan's format definition and the pilot worked example. The section contract is advisory guidance, not a substitute for faithful, non-fabricated content.

OUTPUT FORMAT — markdown with YAML frontmatter (NOT JSON). The frontmatter MUST contain the coordination key `output_path` (the vault-relative `.md` path for this note) AND the note's full vault frontmatter — every required field: `tags` (a list; `tags[0]` = the PARA bucket e.g. `resource`, `tags[1]` = the note's second-category/type, plus topical tags — every tag lowercase letters/digits/UNDERSCORES only, never hyphens: `active_memory`, not `active-memory`), `keywords` (≥5), `topics` (≥2), `language` (`markdown`), `date of note`, `status` (`active`), `building_block` (exactly one, from the closed 8-type enum — matching this note's declared type), `access_control_group` (a list; default `["general"]`), and any type-specific fields (e.g. `source_url` for a documentation note). The frontmatter MUST NOT contain any of the FORBIDDEN legacy keys — `title` (the note's title lives in the H1, never a frontmatter key), `created`, `updated`, `source`, `parent`, `category`, `note_second_category` — the eval's N2 check and the vault validator reject a note carrying any of them. Everything after the closing `---` IS the note body, written verbatim. Read your assigned source
page(s) FIRST, then write one note matching the pilot's shape and the
plan's format definition: verbatim code, honest inferred / not-in-
source markers, one building_block per note. If the source fetch
returns a login page / 403 / empty body, do NOT fall back to memory —
fail closed.

OUTPUT FORMAT — markdown with YAML frontmatter (NOT JSON). The
frontmatter MUST contain the coordination key `output_path` AND the
note's full vault frontmatter (do NOT emit `output_path` alone):
  output_path: <vault-relative .md path for this note>
  tags: [<PARA bucket>, <second-category/type>, <topical...>]
  keywords: [<≥5 search phrases>]
  topics: [<≥2>]
  language: markdown
  date of note: <YYYY-MM-DD>
  status: active
  building_block: <one of the closed 8-type enum, matching this note's type>
  access_control_group: ["general"]
  # + any type-specific fields (e.g. source_url for documentation)
Everything after the closing `---` IS the note body, written verbatim.

BODY STRUCTURE — the note body MUST open with a `## Overview` section (a short thesis/orientation paragraph) and MUST end with the `## Related Notes` section described above. These two are UNIVERSAL across every note type and frame the type-specific sections the `NOTE-TYPE CONTRACT` block requires in between (e.g. `## Overview` → Definition/Examples → `## Related Notes` for a term note; `## Overview` → Claim/Reason/Evidence → `## Related Notes` for an argument). So the H2 order is: `## Overview` first, the type-contract sections next, `## Related Notes` last.

## Verify — Independent Post-Hoc Sweep <!-- :: section_id = verify :: -->

```yaml
role: CORE
aggregation: cross_leaf
batchable: false
depends_on:
- dispatch_notes
materializer: no_op
output_key: verify_report
expected_output_schema:
  type: object
  required:
  - notes_created
  - format_errors
  - broken_links
  - ghost_references
  - graph_island_notes
  - outbound_reference_gaps
  - overall_ok
  properties:
    notes_created:
      type: integer
      description: Notes actually written on disk
    notes_planned:
      type: integer
      description: Planned-note count from preflight, for the N/M rollup
    format_errors:
      type: integer
      description: Format-check errors across all new notes (must be 0)
    broken_links:
      type: integer
      description: Vault-wide broken links (must be 0)
    ghost_references:
      type: integer
      description: Ghost references from the new notes (must be 0)
    graph_island_notes:
      type: integer
      description: New notes with 0 inbound links from outside their folder (G8; must be 0)
    outbound_reference_gaps:
      type: integer
      description: New notes with no resolvable outbound `## Related Notes` link (must be 0) — related notes build the graph
    dedup_findings:
      type: array
      description: Duplicate / coverage findings surfaced by the independent sweep
      items:
        type: string
    overall_ok:
      type: boolean
      description: True only if all counts are 0 and coverage is complete
inputs:
- name: upstream.note_body
  required: true
- name: leaf.related_references_md
  required: false
```

You are running the independent post-hoc verification sweep over the
full output set — the backstop that does not trust the wave's
self-report.

WRITTEN NOTES (from the per-leaf dispatch_notes step)
{{upstream.note_body}}

Follow this procedure:

The wave's "all batches passed" is a claim, not proof; this cross-leaf step is the independent backstop that runs once over the full output set on disk, regardless of what any in-loop validator reported. Re-run the plan's full gate suite across ALL new notes (not per batch), run the format check, run the broken-link check (must report zero), rebuild the database and query for ghost references from the new notes (must be zero), and run the G8 discoverability check (every new note must have at least one inbound link from OUTSIDE its own folder — any graph-island note fails). ALSO run the OUTBOUND-reference check: every new note must have a `## Related Notes` section with at least one resolvable relative markdown link to an existing vault note (these outbound links are what the indexer turns into knowledge-graph edges) — a note with an empty/absent `## Related Notes` section is an `outbound_reference_gap` and must be patched by adding the relevant links the enrichment surfaced (`{{leaf.related_references_md}}`) or grounded from the plan's cross-reference mapping. Deduplication, ghost-reference, and coverage findings are surfaced here. Any residual issue is patched in place and re-verified; the run is NOT complete while broken, ghost, format, graph-island, or outbound-reference issues remain. Emit a `verify_report` rollup (notes created vs. planned, gate results, broken-link count, ghost count, graph-island count, outbound-reference-gap count, and an overall pass/fail) so the orchestrator has an auditable completion record. Read the written note set from `{{upstream.note_body}}`. Re-run the plan's full gate
suite across ALL new notes, run the format check, the broken-link
check, rebuild the DB and query ghost references, and run the G8
outside-folder inbound-link check; surface dedup / coverage findings.
Patch any residual issue in place and re-verify. Return ONLY the JSON
object specified by expected_output_schema; no prose.

## Related skills <!-- :: section_id = related_skills :: -->

The four phases of the plan → augment → review → execute digestion pipeline:

- [`skill_tessellum_plan_digestion.md`](skill_tessellum_plan_digestion.md) — Phase 1 — produces the plan_doc.
- [`skill_tessellum_augment_digestion_plan.md`](skill_tessellum_augment_digestion_plan.md) — Phase 2 — enriches the plan_doc with gates + cross-ref contract.
- [`skill_tessellum_review_digestion_plan.md`](skill_tessellum_review_digestion_plan.md) — Phase 3 — the read-only READY/NOT-READY sign-off gate.
- [`skill_tessellum_execute_digestion_plan.md`](skill_tessellum_execute_digestion_plan.md) — Phase 4 — writes the notes from a ready plan. ← this skill
