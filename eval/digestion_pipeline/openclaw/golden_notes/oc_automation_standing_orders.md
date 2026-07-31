---
tags:
  - resource
  - documentation
  - openclaw
  - automation
  - standing_orders
keywords:
  - openclaw standing orders
  - permanent operating authority
  - standing order program anatomy
  - execute-verify-report pattern
  - multi-program architecture escalation
  - standing orders plus cron
  - AGENTS.md standing orders
  - approval gates escalation rules
topics:
  - OpenClaw
  - Standing Orders
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/automation/standing-orders
access_control_group: ["general"]
---

# OpenClaw — Standing Orders as Permanent Operating Authority

## Overview

This note argues OpenClaw's **standing orders** discipline: a convention (not a code feature) for granting an agent **permanent operating authority** over defined programs so it executes autonomously within boundaries instead of needing a fresh instruction per task. It mirrors the `automation/standing-orders` source page — the case for standing orders, how they work via auto-injected workspace files, the four-part anatomy of a program, how they pair with cron for enforcement, the worked program examples, the execute-verify-report discipline, multi-program architecture with escalation rules, and the Do/Avoid best practices. The thesis throughout is that durable, file-resident authority plus strict execution discipline is what turns an idle prompt-driven assistant into a reliable autonomous operator.

## Why standing orders

The core claim is that **standing orders move the human out of the per-task loop**. The source frames it as the difference between telling your assistant "send the weekly report" every Friday versus granting standing authority: "You own the weekly report. Compile it every Friday, send it, and only escalate if something looks wrong." Without standing orders you must prompt the agent for every task, the agent sits idle between requests, routine work gets forgotten or delayed, and you become the bottleneck. With standing orders the agent executes autonomously within defined boundaries, routine work happens on schedule without prompting, you only get involved for exceptions and approvals, and the agent fills idle time productively. The argument is therefore an availability/throughput one: persistent authority reclaims the human's attention for genuine exceptions.

## How they work

Standing orders are defined in your agent workspace files. The recommended approach is to include them directly in `AGENTS.md` (which is auto-injected every session) so the agent always has them in context; for larger configurations you can also place them in a dedicated file like `standing-orders.md` and reference it from `AGENTS.md`. Each program specifies four things: **Scope** — what the agent is authorized to do; **Triggers** — when to execute (schedule, event, or condition); **Approval gates** — what requires human sign-off before acting; and **Escalation rules** — when to stop and ask for help. The agent loads these instructions every session via the workspace bootstrap files and executes against them, combined with cron jobs for time-based enforcement. The source's Tip is load-bearing to the argument: put standing orders in `AGENTS.md` to guarantee they are loaded every session — the workspace bootstrap automatically injects `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, and `MEMORY.md`, but not arbitrary files in subdirectories. Authority that is not auto-injected is authority the agent may not actually have in context.

## Anatomy of a standing order

A program is authored as a Markdown block whose header fields encode the four contract dimensions, followed by execution steps and an explicit negative-scope section. The source's canonical example is a "Weekly Status Report" program:

```markdown
## Program: Weekly Status Report

**Authority:** Compile data, generate report, deliver to stakeholders
**Trigger:** Every Friday at 4 PM (enforced via cron job)
**Approval gate:** None for standard reports. Flag anomalies for human review.
**Escalation:** If data source is unavailable or metrics look unusual (>2σ from norm)

### Execution steps

1. Pull metrics from configured sources
2. Compare to prior week and targets
3. Generate report in Reports/weekly/YYYY-MM-DD.md
4. Deliver summary via configured channel
5. Log completion to Agent/Logs/

### What NOT to do

- Do not send reports to external parties
- Do not modify source data
- Do not skip delivery if metrics look bad - report accurately
```

The argument embedded here is that an authority grant is incomplete without an explicit "What NOT to do" boundary; permissions and prohibitions are co-equal parts of the contract.

## Standing orders plus cron jobs

Standing orders and cron are complementary by design: standing orders define **what** the agent is authorized to do, and cron jobs define **when** it happens. The source diagrams the handoff — a standing order ("You own the daily inbox triage") plus a cron job (8 AM daily: "Execute inbox triage per standing orders") yields the agent reading the standing orders, executing the steps, and reporting results. The discipline rule is that the cron job prompt should **reference** the standing order rather than duplicating it, so the authority lives in one place:

```bash
openclaw cron add \
  --name daily-inbox-triage \
  --cron "0 8 * * 1-5" \
  --tz America/New_York \
  --timeout-seconds 300 \
  --announce \
  --channel imessage \
  --to "+1XXXXXXXXXX" \
  --message "Execute daily inbox triage per standing orders. Check mail for new alerts. Parse, categorize, and persist each item. Report summary to owner. Escalate unknowns."
```

This separation is why the Best Practices section later warns that standing orders without triggers "become suggestions" — the cron trigger is what makes the authority operationally binding.

## Examples

The source supplies three worked programs that demonstrate the anatomy across different trigger cadences. **Example 1 — Content & Social Media (weekly cycle)** grants authority to draft content, schedule posts, and compile engagement reports; its approval gate requires owner review of all posts for the first 30 days, then standing approval; its trigger is a weekly cycle (Monday review → mid-week drafts → Friday brief), with content rules requiring brand-matching voice, never identifying as AI in public-facing content, including metrics when available, and focusing on audience value over self-promotion. **Example 2 — Financial Processing (event-triggered)** grants authority to process transaction data, generate reports, and send summaries, with no approval gate for analysis but recommendations requiring owner approval, triggered when a new data file is detected OR on a scheduled monthly cycle; its escalation rules are quantitative — single item > $500 triggers an immediate alert, a category > budget by 20% is flagged in the report, an unrecognizable transaction asks the owner for categorization, and failed processing after 2 retries reports failure without guessing. **Example 3 — System Monitoring (continuous)** grants authority to check system health, restart services, and send alerts, restarting services automatically but escalating if a restart fails twice, triggered every heartbeat cycle; its checks cover service health endpoints, disk space threshold, stale pending tasks (>24 hours), and delivery-channel health, governed by a response matrix:

```markdown
### Response matrix

| Condition        | Action                   | Escalate?                |
| ---------------- | ------------------------ | ------------------------ |
| Service down     | Restart automatically    | Only if restart fails 2x |
| Disk space < 10% | Alert owner              | Yes                      |
| Stale task > 24h | Remind owner             | No                       |
| Channel offline  | Log and retry next cycle | If offline > 2 hours     |
```

These examples argue that the same four-field contract scales across one-shot, event-driven, and continuous cadences, and that escalation thresholds should be concrete and condition-specific rather than discretionary.

## Execute-verify-report pattern

The source argues standing orders "work best when combined with strict execution discipline," and prescribes that every task in a standing order follow a loop: **Execute** — do the actual work (do not just acknowledge the instruction); **Verify** — confirm the result is correct (file exists, message delivered, data parsed); and **Report** — tell the owner what was done and what was verified. The execution rules are stated as hard constraints:

```markdown
### Execution rules

- Every task follows Execute-Verify-Report. No exceptions.
- "I'll do that" is not execution. Do it, then report.
- "Done" without verification is not acceptable. Prove it.
- If execution fails: retry once with adjusted approach.
- If still fails: report failure with diagnosis. Never silently fail.
- Never retry indefinitely - 3 attempts max, then escalate.
```

The page states this pattern "prevents the most common agent failure mode: acknowledging a task without completing it." The bounded-retry rule (retry once with an adjusted approach, 3 attempts max, then escalate) is the discipline that keeps an autonomous agent from looping silently or failing without diagnosis.

## Multi-program architecture

For agents managing multiple concerns, the source advises organizing standing orders as **separate programs with clear boundaries** — e.g. "Program 1: [Domain A] (Weekly)", "Program 2: [Domain B] (Monthly + On-Demand)", "Program 3: [Domain C] (As-Needed)", followed by a shared "Escalation Rules (All Programs)" block for common escalation criteria and cross-program approval gates. Each program should have its own **trigger cadence** (weekly, monthly, event-driven, continuous), its own **approval gates** (some programs need more oversight than others), and clear **boundaries** so the agent knows where one program ends and another begins. The argument is that mixing concerns dilutes accountability; per-domain isolation keeps authority, cadence, and oversight independently tunable while a single shared escalation block prevents gaps between programs.

## Best practices

The source closes with a Do/Avoid list that crystallizes the argument. **Do**: start with narrow authority and expand as trust builds; define explicit approval gates for high-risk actions; include "What NOT to do" sections (boundaries matter as much as permissions); combine with cron jobs for reliable time-based execution; review agent logs weekly to verify standing orders are being followed; and update standing orders as needs evolve since they are living documents. **Avoid**: granting broad authority on day one ("do whatever you think is best"); skipping escalation rules (every program needs a "when to stop and ask" clause); assuming the agent will remember verbal instructions (put everything in the file); mixing concerns in a single program (separate programs for separate domains); and forgetting to enforce with cron jobs (standing orders without triggers become suggestions). The throughline is graduated trust plus explicit, file-resident, cron-enforced boundaries.

**Source**: OpenClaw documentation — `automation/standing-orders` (mirror `inbox/openclaw_docs/automation/standing-orders.md`)
**Last Updated**: 2026-06-22
**Status**: Active
