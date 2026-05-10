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
pipeline_metadata: ./skill_tessellum_write_coe.pipeline.yaml
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

Extract from leaf metadata + (optionally) recent shell / editor / index state the following:

- **Task**: what the user / agent was trying to do
- **What went wrong**: the failure / surprise (specific, with verbatim error messages where available)
- **Attempts**: each failed approach with what was tried and how it failed
- **Resolution**: what finally worked (if known; otherwise mark `status: investigating`)
- **Duration**: approximate wall time from first attempt to mitigation
- **Timeline**: chronological list of events with timestamps where available

If only the user-supplied `title` + `summary` are available, derive what you can; mark unknowns explicitly rather than guessing. The 5 Whys in step 2 will surface what's missing.

## Step 2: Perform 5 Whys Root Cause Analysis <!-- :: section_id = step_2_perform_5_whys_root_cause_analysis :: -->

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

The five-iterations rule is a *floor*, not a ceiling. Go deeper if the systemic root cause isn't yet visible.

## Step 3: Write the COE Note <!-- :: section_id = step_3_write_coe_note :: -->

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

```bash
ls "$COE_DIR"/coe_*.md
tessellum search --bm25 "<key failure pattern keywords>" --k 10
```

If a closely-related COE exists, reference it in the new COE's **References** section and note:

- Is this a **recurrence** of the same root cause? → Then the previous COE's action items didn't fix the underlying issue. Flag this in **Lessons Learned**.
- Is this a **variation** on the same failure family? → Then the failure class is broader than the previous COE assumed. Update the broader pattern in **What Went Wrong**.

A recurrence is a strong signal that the previous COE's action items weren't load-bearing — escalate the priority.

## Step 5: Verify <!-- :: section_id = step_5_verify :: -->

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

If any check fails, fix the note before proceeding to step 6.

## Step 6: Update COE Entry Point <!-- :: section_id = step_6_update_coe_entry_point :: -->

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
