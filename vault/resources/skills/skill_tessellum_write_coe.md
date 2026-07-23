---
tags:
  - resource
  - skill
  - procedure
  - capture
  - coe
  - incident_management
  - reflection
keywords:
  - write coe
  - tessellum-write-coe
  - in-vault skill canonical
  - post-incident analysis
  - 5 whys
topics:
  - Skill Procedures
  - Incident Management
  - Reflection Practice
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Procedure: tessellum-write-coe (Canonical Body)

This is the **single canonical body** for the `tessellum-write-coe` skill. This skill is invoked directly by Tessellum's composer (see `tessellum composer compile / run`); no ecosystem shims are needed.

## Skill description <!-- :: section_id = skill_description :: -->

Write a Correction of Errors (COE) note for a problem you want to learn from — a failed deploy, a corrupted output, a process gap, a surprise. Takes incident details (`title` + free-text `summary`) as leaf metadata, performs a 5-Whys root cause analysis, drafts a structured COE note (with all 9 required sections) in `resources/analysis_thoughts/`, checks for duplicate / related COEs, verifies the note's structure, and updates `entry_coes.md` with the new row. Use when you want to convert "we hit a wall" into a typed, reviewable, action-item-bearing artifact that future-you (and the rest of the team) can learn from.

The shape of the produced note follows [`term_coe`](../term_dictionary/term_coe.md); the index it appends to is [`entry_coes`](../../0_entry_points/entry_coes.md).

## Setup <!-- :: section_id = setup :: -->

```bash
VAULT_PATH="."   # run from your vault root
COE_DIR="$VAULT_PATH/resources/analysis_thoughts"
ENTRY_POINT="$VAULT_PATH/0_entry_points/entry_coes.md"
# `tessellum search` and `tessellum index build` resolve paths from CWD
```

## Resources <!-- :: section_id = resources :: -->

- **COE notes**: `$COE_DIR/coe_<slug>.md`
- **Entry point**: `$ENTRY_POINT` (`0_entry_points/entry_coes.md`)
- **Method reference**: [`term_coe`](../term_dictionary/term_coe.md) — definition, 5 Whys, 9 sections, anti-patterns
- **Required BB type**: `argument` (a COE claims a root cause and a remediation path)

## Step 1: Gather Incident Details <!-- :: section_id = step_1_gather_incident_details :: -->

```yaml
role: CORE
aggregation: per_leaf
batchable: true
depends_on: []
materializer: no_op
output_key: incident_details
expected_output_schema:
  type: object
  required:
  - task
  - what_went_wrong
  - attempts
  - resolution
  properties:
    task:
      type: string
      description: What the user / agent was trying to do
    what_went_wrong:
      type: string
      description: The error / failure / surprise (specific, with verbatim error message where
        available)
    attempts:
      type: array
      description: Each failed approach
      items:
        type: object
        required:
        - approach
        - outcome
        properties:
          approach:
            type: string
          outcome:
            type: string
    resolution:
      type: string
      description: "What finally worked \u2014 or 'investigating' if not yet resolved"
    duration_minutes:
      type:
      - integer
      - 'null'
      description: Approximate wall time from first attempt to mitigation
    timeline:
      type: array
      items:
        type: object
        required:
        - event
        properties:
          event:
            type: string
          timestamp:
            type:
            - string
            - 'null'
mcp_dependencies:
- name: session-mcp
  calls:
  - get_session_metadata
  - search_transcript
  - get_tool_uses
  - read_recent_messages
  required: false
```

You are extracting incident details for a Correction of Errors (COE)
write-up.

LEAF METADATA
- title: {{leaf.title}}
- summary: {{leaf.summary}}

Follow this procedure:

Extract from leaf metadata + (optionally) recent shell / editor / index state the following:

- **Task**: what the user / agent was trying to do
- **What went wrong**: the failure / surprise (specific, with verbatim error messages where available)
- **Attempts**: each failed approach with what was tried and how it failed
- **Resolution**: what finally worked (if known; otherwise mark `status: investigating`)
- **Duration**: approximate wall time from first attempt to mitigation
- **Timeline**: chronological list of events with timestamps where available

If only the user-supplied `title` + `summary` are available, derive what you can; mark unknowns explicitly rather than guessing. The 5 Whys in step 2 will surface what's missing.

If only `title` + `summary` are available from leaf metadata, derive
what you can. Mark unknowns explicitly (e.g., `"resolution": "unknown"`
or `"duration_minutes": null`) rather than guessing — the 5 Whys in
step 2 will surface what's missing.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 2: Perform 5 Whys Root Cause Analysis <!-- :: section_id = step_2_perform_5_whys_root_cause_analysis :: -->

```yaml
role: CORE
aggregation: per_leaf
batchable: true
depends_on:
- step_1_gather_incident_details
materializer: no_op
output_key: five_whys
expected_output_schema:
  type: object
  required:
  - why_chain
  - root_cause
  properties:
    why_chain:
      type: array
      minItems: 5
      items:
        type: object
        required:
        - level
        - why
        - because
        properties:
          level:
            type: integer
            minimum: 1
          why:
            type: string
          because:
            type: string
    branches:
      type: array
      description: "Optional \u2014 additional causal branches if multiple paths apply"
      items:
        type: object
        required:
        - from_level
        - why_chain
        properties:
          from_level:
            type: integer
            minimum: 1
          why_chain:
            type: array
            items:
              type: object
              required:
              - level
              - why
              - because
              properties:
                level:
                  type: integer
                why:
                  type: string
                because:
                  type: string
    root_cause:
      type: string
      description: "The systemic root cause \u2014 must be about a system, process, or check,\
        \ never about an individual"
```

You are performing the 5 Whys root cause analysis on the incident.

INCIDENT_DETAILS (from step 1)
{{upstream.incident_details}}

Follow this procedure:

Starting from the visible symptom, ask *why* and write each answer as a **factual statement** (not speculation, not blame). Iterate at least 5 levels. Branch the causal tree when multiple paths apply.

Example chain shape:

```
Level 1 — Why did X fail?           → Because Y happened.
Level 2 — Why did Y happen?         → Because Z was assumed.
Level 3 — Why was Z assumed?        → Because the code used pattern W.
Level 4 — Why was pattern W used?   → Because the procedure didn't cover edge case V.
Level 5 — Why didn't V have coverage? → Because no validation existed for V.
Root cause                          : Missing validation for V.
```

**Stop signs** — if you land on any of these, ask one more *why*:

- "Operator error" → what allowed the error to be possible?
- "Resource exhaustion" → what caused the consumption pattern?
- "Dependency failed" → why wasn't the system resilient to that failure?
- "I should have known" → that's blame. Replace with: what check was missing?

The five-iterations rule is a *floor*, not a ceiling. Go deeper if the systemic root cause isn't yet visible. Each level MUST be a factual statement,
not speculation and not blame. Go beyond level 5 if the systemic root
cause isn't yet visible.

Stop signs that mean you must ask one more `why`: "operator error",
"resource exhaustion", "dependency failed", "I should have known".

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 3: Write the COE Note <!-- :: section_id = step_3_write_coe_note :: -->

```yaml
role: CORE
aggregation: per_leaf
batchable: false
depends_on:
- step_1_gather_incident_details
- step_2_perform_5_whys_root_cause_analysis
materializer: body_markdown_frontmatter_to_file
output_key: coe_body
expected_output_schema:
  type: object
  required:
  - output_path
  properties:
    output_path:
      type: string
      pattern: ^resources/analysis_thoughts/coe_[a-z0-9_]+\.md$
```

You are writing the COE note for "{{leaf.title}}".

INCIDENT_DETAILS (from step 1)
{{upstream.incident_details}}

FIVE_WHYS (from step 2)
{{upstream.five_whys}}

Apply the procedure in section "step_3_write_coe_note" of
skill_tessellum_write_coe (sub-sections: yaml_frontmatter,
required_sections, writing_rules).

OUTPUT FORMAT — markdown with YAML frontmatter, NOT JSON, NOT XML.
Do NOT call any file-write tool. Do NOT wrap the output in code
fences. Return the markdown directly.

The frontmatter MUST contain:
  - output_path: resources/analysis_thoughts/coe_<descriptive_slug>.md
  - All standard fields: tags (with tags[0]=resource, tags[1]=analysis,
    tags[2]=coe), keywords, topics, language, date of note, status,
    building_block: argument

Everything after the closing `---` IS the file body, written verbatim.
Required sections in order (per skill canonical):
  1. # COE: <Title>
  2. ## Summary
  3. ## Customer / User Impact
  4. ## Timeline (table: Time | Event)
  5. ## Root Cause Analysis (5 Whys) — numbered list
  6. ## What Went Wrong — per-pattern subsections
  7. ## What Went Well
  8. ## Lessons Learned — numbered list (≥3 lessons)
  9. ## Action Items (table: # | Action | Owner | Priority | Due | Status)
  10. ## References

Authoring rules: systems and processes only (never blame individuals);
factual statements (not speculation); every lesson maps to an action
item; honest timeline (include failed attempts, not just the fix).

---

Create: `$COE_DIR/coe_<descriptive_slug>.md`

**File naming**: `coe_<lowercase_underscored_summary>.md` — slug should describe the failure pattern, not the date.

### YAML Frontmatter <!-- :: section_id = yaml_frontmatter :: -->

```yaml
---
tags:
  - resource
  - analysis
  - coe
  - <domain_tag>
keywords:
  - COE
  - <key failure concepts>
topics:
  - incident analysis
  - <domain topic>
language: markdown
date of note: <YYYY-MM-DD>
status: active
building_block: argument
output_path: resources/analysis_thoughts/coe_<slug>.md
---
```

`tags[0]` must be `resource`; `tags[1]` must be `analysis`; `tags[2]` must be `coe`. The `output_path` field tells the materializer where the file lands; it is stripped before the file is written.

### Required Sections (9 in order) <!-- :: section_id = required_sections :: -->

Every COE MUST have these sections in this order. See [`term_coe`](../term_dictionary/term_coe.md) for the full guidance on each.

```
# COE: <Concise Descriptive Title>

## Summary
1-2 paragraphs that a reader who wasn't in the incident can understand.
What activity, when, who was affected, what happened, what was the
resolution, what are the top 2-3 action items.

## Customer / User Impact
Specific numbers. How many users / files / records affected, what
duration, what was NOT affected (the blast radius).

## Timeline
| Time  | Event |
|-------|-------|
| HH:MM | Initial task started: ... |
| HH:MM | First failure: ... |
| HH:MM | Attempt 2: ... |
| HH:MM | Resolution: ... |

Chronological. Use consistent timezones. Include failed mitigation
attempts, not just the fix.

## Root Cause Analysis (5 Whys)
1. Why <symptom>? → Because <cause-1>.
2. Why <cause-1>? → Because <cause-2>.
3. Why <cause-2>? → Because <cause-3>.
4. Why <cause-3>? → Because <cause-4>.
5. Why <cause-4>? → Because <systemic root cause>.

(Branch the chain when multiple paths apply; document each branch.)

## What Went Wrong
### <Failure Pattern 1 — Name>
Description of the specific mistake pattern; reference the timeline
row(s) that exposed it.

### <Failure Pattern 2 — Name>
(if applicable)

## What Went Well
- What prevented worse outcomes (version control, alarms, validators, ...)
- What tools helped detect the issue
- What communication worked

## Lessons Learned
1. <Lesson 1>: specific, actionable, preventive — addresses a class of
   error, not just this instance.
2. <Lesson 2>: ...
3. <Lesson 3>: ...

## Action Items
| # | Action | Owner | Priority | Due | Status |
|---|--------|-------|----------|-----|--------|
| 1 | <Specific SMART action>  | <name>  | High   | <date>  | TODO |
| 2 | ...                       | ...     | Medium | ...     | TODO |

Priorities + due-date conventions: High = 30 days, Medium = 60 days,
Low = 90 days, None = 365 days. Adapt to your context.

## References
- [term_coe](../term_dictionary/term_coe.md) — method reference
- [Related COE if any]: <path>
- [Related procedure / skill / how-to]: <path>
```

### Writing Rules <!-- :: section_id = writing_rules :: -->

- **Be specific**: include exact commands, file paths, error messages.
- **No blame**: focus on systemic causes. Never name an individual as a root cause.
- **Quantify**: number of attempts, files affected, minutes spent.
- **Link every lesson to an action item**: a lesson without a corresponding action item is just a feeling.
- **Honest timeline**: include every failed mitigation attempt; the record of what *didn't* work is half the value.

## Step 4: Check for Duplicate / Related COEs <!-- :: section_id = step_4_check_for_duplicates :: -->

```yaml
role: CORE
aggregation: per_leaf
batchable: true
depends_on:
- step_3_write_coe_note
materializer: no_op
output_key: duplicate_check
expected_output_schema:
  type: object
  required:
  - duplicate_found
  properties:
    duplicate_found:
      type: boolean
    related_coe_paths:
      type: array
      items:
        type: string
    recurrence_signal:
      type:
      - string
      - 'null'
      description: "If duplicate_found and same root cause: 'recurrence \u2014 prior action\
        \ items did not load-bear'"
```

You are checking the vault for COE notes that overlap with the
just-written COE for "{{leaf.title}}".

Follow this procedure:

```bash
ls "$COE_DIR"/coe_*.md
tessellum search --bm25 "<key failure pattern keywords>" --k 10
```

If a closely-related COE exists, reference it in the new COE's **References** section and note:

- Is this a **recurrence** of the same root cause? → Then the previous COE's action items didn't fix the underlying issue. Flag this in **Lessons Learned**.
- Is this a **variation** on the same failure family? → Then the failure class is broader than the previous COE assumed. Update the broader pattern in **What Went Wrong**.

A recurrence is a strong signal that the previous COE's action items weren't load-bearing — escalate the priority. Use `tessellum search --bm25` over the
failure-pattern keywords from step 2's root cause, plus a directory
listing of existing coe_*.md files.

For each related COE found, decide: is this a recurrence (same root
cause) or a variation (related but distinct)? Recurrence is a strong
signal that the prior COE's action items did not load-bear.

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 5: Verify <!-- :: section_id = step_5_verify :: -->

```yaml
role: CORE
aggregation: per_leaf
batchable: true
depends_on:
- step_4_check_for_duplicates
materializer: no_op
output_key: verify_verdict
expected_output_schema:
  type: object
  required:
  - passes_format_check
  - all_required_sections_present
  - lessons_count
  - action_items_count
  properties:
    passes_format_check:
      type: boolean
    all_required_sections_present:
      type: boolean
    lessons_count:
      type: integer
      minimum: 0
    action_items_count:
      type: integer
      minimum: 0
    issues:
      type: array
      items:
        type: string
```

You are verifying the just-written COE note for "{{leaf.title}}".

Follow this procedure:

```bash
NOTE="$COE_DIR/coe_<slug>.md"
tessellum format check "$NOTE"
```

Required:

- [ ] YAML frontmatter parses (validator returns 0 errors)
- [ ] `building_block: argument`
- [ ] All 9 required sections present in order
- [ ] 5 Whys reaches a systemic root cause (not "operator error", not blame)
- [ ] At least 3 lessons learned (each specific + actionable + preventive)
- [ ] At least 2 action items (each SMART with owner + priority + due + status)
- [ ] Timeline includes the failed mitigation attempts, not just the fix
- [ ] **References** section links to `term_coe` + at least one related note

If any check fails, fix the note before proceeding to step 6. Required checks:
  - tessellum format check passes (0 errors)
  - building_block: argument
  - All 9 required sections present in order
  - 5 Whys reaches a systemic root cause (not blame, not "operator
    error")
  - At least 3 lessons learned, each specific + actionable + preventive
  - At least 2 action items, each SMART with owner + priority + due +
    status
  - Timeline includes failed mitigation attempts, not just the fix
  - References section links to term_coe + at least one related note

Return ONLY the JSON object specified by expected_output_schema; no
prose, no code fences.

## Step 6: Update COE Entry Point <!-- :: section_id = step_6_update_coe_entry_point :: -->

```yaml
role: DEFERRED
aggregation: cross_leaf
batchable: false
depends_on:
- step_3_write_coe_note
- step_5_verify
materializer: edits_apply_xml_tags
output_key: entry_point_updates
expected_output_schema:
  type: object
  required:
  - edits
  properties:
    edits:
      type: array
      items:
        type: object
        required:
        - file
        - content
        properties:
          file:
            type: string
          content:
            type: string
```

You are batch-updating the COE entry point with one or more newly
written COE notes from the upstream step_3_write_coe_note dispatches.

NEW_COES (one entry per affected leaf — full markdown-with-frontmatter
from each step_3 output)
{{upstream.coe_body}}

Apply the procedure in section "step_6_update_coe_entry_point" of
skill_tessellum_write_coe (sub-steps 6a-6c cover Quick Stats,
COE Index table, Recurring Patterns).

OUTPUT FORMAT — XML tag list, NOT JSON. APPLY mode: emit the COMPLETE
new file body inside <content>, verbatim (not a diff, not regex
operations, not a status report). Do NOT call any file-write tool.

Required envelope:
  <edits>
    <edit>
      <file>0_entry_points/entry_coes.md</file>
      <content>
<COMPLETE new file body — all original sections preserved + new COE
row(s) inserted at the top of the COE Index table + Quick Stats
counters bumped + Last Updated date bumped to today>
      </content>
    </edit>
  </edits>

If NEW_COES is empty (no leaves succeeded at step_3), emit
<edits></edits> (empty envelope, no error).

---

Update `$VAULT_PATH/0_entry_points/entry_coes.md` with the new COE.

### 6a. Update Quick Stats <!-- :: section_id = 6a_update_quick_stats :: -->

In the **Quick Stats** table, increment `Total COEs` by 1 and bump `Latest Updated` to today's date (YYYY-MM-DD). If the COE has `status: investigating`, also increment `Open`; otherwise increment `Resolved`.

### 6b. Add Row to COE Index Table <!-- :: section_id = 6b_add_row_to_coe_index :: -->

Insert a new row **at the top** of the COE Index table (latest first):

```markdown
| <YYYY-MM-DD> | [<COE Title>](../resources/analysis_thoughts/coe_<slug>.md) | <Root cause one-line summary> | <Impact one-line summary> |
```

### 6c. Update Recurring Patterns (if applicable) <!-- :: section_id = 6c_update_recurring_patterns :: -->

If the new COE matches an existing recurring pattern entry, update the count under **Recurring Patterns**. If it introduces a new pattern (the second or later occurrence of a failure class), add a new sub-section naming the pattern and listing the COEs that belong to it.

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Recovery |
|-------|----------|
| Incident details unclear / incomplete | Ask the user to fill in the gaps; mark unknowns explicitly in the note rather than guessing |
| Root cause is "I made a mistake" | Go deeper — why was the mistake possible? What check was missing? What did the procedure assume? |
| No clear resolution yet | Document as open COE with `status: investigating`; the action items name the next investigative steps |
| Similar COE exists with same root cause | Reference the prior COE; flag the recurrence as a strong signal in **Lessons Learned**; escalate action-item priority |
| Output_path collides with existing note | Append `_v2` to the slug, or update the existing COE if it's the same incident from a different angle |

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **Systems and processes only.** Never name an individual as a root cause. If the analysis lands on a person, the next *why* is: what gave that person an unsafe interface to operate on?
2. **Factual statements, not speculation.** Each *why* answer must be a fact you can point to in the timeline or in the system state. If you can't point to evidence, mark it as a hypothesis and add an investigative action item.
3. **Every lesson maps to an action item.** A lesson without a corresponding action item is a feeling, not a learning.
4. **The 5 Whys are a floor, not a ceiling.** Five is the minimum depth. Go deeper when the systemic cause isn't visible at level 5.
5. **The COE note's `building_block:` is always `argument`.** The note claims a root cause and a remediation path; that is an argument.

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [Master TOC](../../0_entry_points/entry_master_toc.md) — the vault's navigation root
- [Entry: COE Index](../../0_entry_points/entry_coes.md) — the index this skill updates
