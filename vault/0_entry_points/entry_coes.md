---
tags:
  - entry_point
  - index
  - navigation
  - coe
  - incident_management
  - reflection
keywords:
  - COE index
  - Correction of Errors
  - incident log
  - post-mortem catalog
  - reflection
topics:
  - Incident Management
  - Continuous Improvement
  - Reflection Practice
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Entry: Correction of Errors (COE) Index

## Purpose

This page indexes every **Correction of Errors (COE)** note in the vault. A COE is a structured post-incident analysis — what went wrong, why, and what's being done to prevent recurrence. The method, the document shape, and the writing discipline are defined in [`term_coe`](../resources/term_dictionary/term_coe.md); the agent-executable skill that writes COEs is [`skill_tessellum_write_coe`](../resources/skills/skill_tessellum_write_coe.md).

This entry point is updated by step 6 of the write-coe skill (or by hand when you author a COE outside the skill). New COEs land at the top of the index — latest first.

## Quick Stats

| | |
|---|---|
| **Total COEs** | 0 |
| **Latest Updated** | 2026-05-10 |
| **Open (status: investigating)** | 0 |
| **Resolved (status: active)** | 0 |

(The skill increments these counters automatically when it adds a new row.)

## COE Index

| Date | Title | Root Cause | Impact |
|---|---|---|---|

*(No COEs yet — your first one will land here once you run `tessellum composer run vault/resources/skills/skill_tessellum_write_coe.md`.)*

## Recurring Patterns

A "recurring pattern" is a class of failure that has produced two or more COEs. Track them here so future incidents can be cross-referenced.

*(No recurring patterns yet — they emerge as the vault grows.)*

## How to Write a COE

Two paths:

### Path 1 — Author by hand

1. Create `resources/analysis_thoughts/coe_<descriptive_slug>.md`.
2. Use the section structure from [`term_coe`](../resources/term_dictionary/term_coe.md) (Summary → Customer Impact → Timeline → 5 Whys → What Went Wrong → What Went Well → Lessons Learned → Action Items → References).
3. `tessellum format check` your file (`building_block: argument`).
4. Append a row to the COE Index table above.
5. Bump the Total count + Last Updated date in Quick Stats.

### Path 2 — Use the skill (Composer pipeline)

1. Provide the incident details as the leaf metadata: a short `title` + a free-text `summary` of what happened.
2. Run the 6-step skill:

   ```bash
   tessellum composer run vault/resources/skills/skill_tessellum_write_coe.md \
     --leaves leaves.json
   ```

   Where `leaves.json` is:

   ```json
   [{"title": "Brief incident name", "summary": "What happened, in 2-3 sentences"}]
   ```

3. The pipeline performs the 5 Whys analysis, drafts the COE note with all 9 sections, checks for related COEs, verifies the structure, and updates this entry point with the new row — automatically.

Both paths produce the same result: a `coe_*.md` note in `resources/analysis_thoughts/` and a row here.

## Authoring discipline

Before adding a COE row, make sure the note actually satisfies the COE bar:

- [ ] The Root Cause is *systemic* (not "operator error" or "should have known").
- [ ] At least 3 lessons learned, each specific + actionable + preventive.
- [ ] At least 2 action items, each SMART with an owner and a due date.
- [ ] Timeline includes the *failed* mitigation attempts, not just the fix.
- [ ] No individuals are blamed. The analysis targets systems and processes.

The [`term_coe`](../resources/term_dictionary/term_coe.md) note has the full anti-pattern checklist; the skill's `step_5_verify` automates most of it.

## Related Entry Points

- [`entry_master_toc`](entry_master_toc.md) — vault navigation root
- [`entry_folgezettel_trails`](entry_folgezettel_trails.md) — research trails (a counter-argument descent over a COE finding is one shape an FZ trail can take)
- [`entry_building_block_index`](entry_building_block_index.md) — BB picker (COEs are `building_block: argument`)

## Related Terms

- [`term_coe`](../resources/term_dictionary/term_coe.md) — the method, the document shape, the discipline
- [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) — DKS is a continuously-running review machine in the same shape as the COE process

---

**Last Updated**: 2026-05-10
**Status**: Active — 0 COEs indexed (seed; grows as users add them)
