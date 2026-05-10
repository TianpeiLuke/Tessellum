---
tags:
  - resource
  - terminology
  - incident_management
  - operational_excellence
  - documentation
  - reflection
keywords:
  - COE
  - Correction of Errors
  - post-incident analysis
  - root cause analysis
  - 5 whys
  - blameless postmortem
  - continuous improvement
topics:
  - Incident Management
  - Continuous Improvement
  - Reflection Practice
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
---

# COE — Correction of Errors

## Definition

A **Correction of Errors (COE)** is a structured post-incident analysis document that captures what went wrong, why it went wrong, and what will be done to prevent recurrence. The term refers interchangeably to:

1. **The method** — a disciplined post-incident analysis process
2. **The document** — the structured output produced by that process
3. **The practice** — making the method routine after any meaningful failure

In a Tessellum vault, every COE is a typed atomic note with `building_block: argument` (it claims a root cause and a path to prevention) stored under `resources/analysis_thoughts/` with filename `coe_<descriptive_slug>.md`.

## Why a COE exists

Every system fails. The question is whether the organization that ran the system *learns* from the failure. The COE practice answers yes by making four commitments:

| Commitment | What it means |
|---|---|
| **Systemic, not individual** | The analysis targets systems, processes, and procedures. *Not* people. "Operator error" is never a root cause — it is a symptom of a missing check, a misleading interface, or an unclear procedure. |
| **Root cause, not symptom** | The analysis keeps asking *why* until it reaches something actionable. Five iterations is the minimum, not the maximum. |
| **Action items, not just analysis** | Every root cause produces at least one SMART action item with an owner and a due date. |
| **Shared, not buried** | The published COE is read by people who weren't in the incident. The whole team learns from each team member's mistakes. |

These commitments are what separate a COE from a venting session.

## The Five Whys

The load-bearing technique. Given a visible symptom, ask *why* and write down each answer as a factual statement (not speculation, not "should have known"). Iterate until the answer reveals something *the system or process did or didn't do* — that's the systemic root cause.

```
Symptom         : X failed.
Why?            : Because Y happened.
Why?            : Because Z was assumed.
Why?            : Because the code used pattern W.
Why?            : Because the procedure didn't cover edge case V.
Why?            : Because no validation existed for V.
Root cause     : Missing validation for V.
Action item    : Add validation for V (owner, due date).
```

**Best practices**:

- ✓ Go beyond 5 iterations when needed. Five is a floor, not a ceiling.
- ✓ Branch the causal tree. Most incidents have multiple root causes; document each branch.
- ✓ Include *recovery* analysis (why did mitigation take so long?), not just *cause* analysis.
- ✓ Document communication gaps, not just technical gaps.
- ✓ Stay on systems and processes; never blame people.

**Stop signs** — if you land on any of these, ask another *why*:

- ❌ "Operator error" — what allowed the error to be possible? Why wasn't it caught?
- ❌ "Resource exhaustion" (CPU / memory / disk) — what caused the consumption pattern? Why wasn't there a limit or alarm?
- ❌ "Dependency failed" — why wasn't the system resilient to that failure? What's the retry / fallback?
- ❌ "I should have known" — that's blame. Replace with: what check / pre-condition was missing?

## Document Sections

A COE has nine required sections. The order is not negotiable — a reader should be able to scan the document top-to-bottom and reach completeness without backtracking.

### 1. Summary
1-2 paragraphs that an outsider can read. What service / activity, when, who was affected, what happened, what was the resolution, what are the most important action items.

### 2. Customer / User Impact
Specific numbers. How many users affected, what proportion of the user base, what duration, what was *not* affected (the blast radius). If there was data loss or corruption, quantify it.

### 3. Timeline
Chronological narrative. Each row: a timestamp + an event. Include the triggering event, detection, escalation, mitigation attempts (including failed ones), and final resolution. Use consistent timezones.

### 4. Root Cause Analysis (5 Whys)
The why chain from above. Each level a factual statement. Branch when multiple paths apply.

### 5. What Went Wrong
Per-failure-pattern subsections. Each pattern named, described, and tied to which step in the timeline exposed it.

### 6. What Went Well
What prevented worse outcomes — version control that allowed rollback, alarms that triggered, tools that helped detect, communication that worked. Naming the wins is not self-congratulation; it tells future readers what to preserve.

### 7. Lessons Learned
A numbered list. Each lesson must be:

- **Specific** — not "be more careful." Name the check that was missing.
- **Actionable** — can be turned into a rule, a validation, or a procedural change.
- **Preventive** — addresses a *class* of error, not just this particular instance.

### 8. Action Items
A table: `# | Action | Owner | Priority | Due | Status`. Each action item is SMART:

| Letter | Stands for |
|---|---|
| S | **Specific** — names a single change |
| M | **Measurable** — can be checked complete or not |
| A | **Assignable** — has exactly one owner |
| R | **Realistic** — can actually be done by the due date |
| T | **Time-related** — has a due date |

Priorities (one common convention; adapt to your context):

| Priority | Due | Purpose |
|---|---|---|
| **High** | 30 days | Direct root-cause mitigation; pre-empts unrelated work |
| **Medium** | 60 days | System / process improvements |
| **Low** | 90 days | Architectural improvements; preventative maintenance |
| **None** | 365 days | Long-term refactors that improve the substrate |

### 9. References
Links to related documents — earlier COEs of similar shape, the relevant how-to or skill, the procedure that was being run, the term notes that describe the affected systems.

## Anti-patterns to avoid

| Anti-pattern | Why it's a problem |
|---|---|
| Blaming individuals | Wastes the analysis on something unfixable; suppresses honest reporting next time |
| Stopping at "operator error" | The system *allowed* the error — fix the system |
| Action items without owners | An action item without an owner doesn't happen |
| Action items with unrealistic dates | A 12-month due date for high priority is the same as "not happening" |
| Open-ended action items only ("investigate X") | Every investigation should resolve into a concrete fix or a documented "no action needed" |
| Cherry-picking the timeline | Include the failed mitigation attempts; they're the record of what didn't work |
| Skipping the "what went well" | Future readers need to know what to preserve |
| Reading speculation as fact | Each "why" answer is a factual claim; if it's speculation, label it and pursue the missing evidence |

## When to write a COE

The exact bar varies by organization, but common triggers:

- A user-visible failure of any meaningful duration.
- A data-loss or data-corruption event, even if no user noticed.
- A near-miss that *would have been* a major incident if not for luck or one careful intervention.
- A recurring small failure (the third occurrence of "same thing again" is a signal that the second occurrence should have been a COE).
- A surprise — the system behaved in a way nobody predicted.

When in doubt, write the COE. The cost is small (a few hours of structured thinking); the cost of *not* writing it is paid later, when the same incident recurs and nobody remembers what was learned the first time.

## Tessellum integration

COEs in a Tessellum vault are typed atomic notes — `building_block: argument`, stored under `resources/analysis_thoughts/coe_<slug>.md`. The skill `skill_tessellum_write_coe` ([canonical](../skills/skill_tessellum_write_coe.md)) automates the writing through a 6-step Composer pipeline:

1. Gather incident details (passed in as leaf metadata)
2. Perform 5 Whys root cause analysis
3. Write the COE note (with all 9 required sections)
4. Check for duplicate / related COEs in the vault
5. Verify the note's structure
6. Update the COE entry point ([`entry_coes`](../../0_entry_points/entry_coes.md)) with the new row

The skill compiles cleanly via `tessellum composer compile` and can run against any backend (MockBackend for offline; AnthropicBackend for real LLM via the `[agent]` extras).

## Related Terms

- [`term_dialectic_knowledge_system`](term_dialectic_knowledge_system.md) — DKS's 7-component closed loop *is* a COE-style review machine running continuously over the typed substrate. A COE is one application of the same shape: observation → root cause (counter-argument) → action items (revised procedures).
- [`term_building_block`](term_building_block.md) — COE notes are `building_block: argument` (they claim a root cause); the action items they produce are `building_block: procedure` (they prescribe an action).
- [`term_epistemic_function`](term_epistemic_function.md) — the COE practice operationalises *refuting* (counter-argument) and *doing* (procedure) — two of the eight epistemic functions.

## See Also

- [`skill_tessellum_write_coe`](../skills/skill_tessellum_write_coe.md) — the agent-executable skill canonical
- [`entry_coes`](../../0_entry_points/entry_coes.md) — entry point indexing all COEs in this vault
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — research trails (a counter-argument descent over a COE finding is one shape an FZ trail can take)

---

**Last Updated**: 2026-05-10
**Status**: Active
