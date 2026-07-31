---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - cron
keywords:
  - hermes cron create
  - scheduled automation blueprints
  - nightly backlog triage
  - uptime monitor script
  - silent pattern
  - cron schedule syntax
  - delivery targets
topics:
  - Hermes Agent
  - Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
access_control_group: ["general"]
---

# Hermes Agent — Scheduled Automation Blueprints

## Overview

These are the **schedule-triggered** copy-paste blueprints from the Hermes Automation Blueprints page: ready-to-run `hermes cron create` recipes that fire on a cadence (hourly, nightly, weekly) rather than on an external event. Each blueprint is a single CLI command whose body is a natural-language prompt the agent runs unattended at the scheduled time, optionally fed by a precomputed `--script`, and delivered to a channel. They cover the recurring-work surface — development hygiene (backlog triage, docs-drift, dependency audit), monitoring (uptime), and research/intelligence (competitor scout, news/paper digest, revenue summary) — and close with the cron-syntax, delivery-target, and `[SILENT]`-suppression reference tables. The event-driven (`webhook`) counterparts live in the sibling [event blueprints](hermes_automation_blueprints_event.md) note; this note owns only the time-triggered family.

Every blueprint works with **any model** (not locked to one provider). Time-based triggers run on Hermes's built-in cron scheduler; the same blueprints can be created interactively with the `/cron` slash command instead of the `cronjob` tool.

## Three Trigger Types

The source opens by distinguishing three trigger families; **this note covers only the first** (the other two route to the event note):

| Trigger | How | Tool |
|---------|-----|------|
| **Schedule** | Runs on a cadence (hourly, nightly, weekly) | `cronjob` tool or `/cron` slash command |
| **GitHub Event** | Fires on PR opens, pushes, issues, CI results | Webhook platform (`hermes webhook subscribe`) |
| **API Call** | External service POSTs JSON to your endpoint | Webhook platform (config.yaml routes or `hermes webhook subscribe`) |

All three support delivery to Telegram, Discord, Slack, SMS, email, GitHub comments, or local files.

## Development Workflow

**Nightly Backlog Triage** — label, prioritize, and summarize new GitHub issues every night, delivering a digest to a team channel. The prompt lists open issues via `gh`, identifies issues opened in the last 24h, suggests priority + category labels and a one-line triage note per issue, then summarizes totals; the `[SILENT]` close suppresses delivery on quiet runs.

```bash
hermes cron create "0 2 * * *" \
  "You are a project manager triaging the NousResearch/hermes-agent GitHub repo.

1. Run: gh issue list --repo NousResearch/hermes-agent --state open --json number,title,labels,author,createdAt --limit 30
2. Identify issues opened in the last 24 hours
3. For each new issue:
   - Suggest a priority label (P0-critical, P1-high, P2-medium, P3-low)
   - Suggest a category label (bug, feature, docs, security)
   - Write a one-line triage note
4. Summarize: total open issues, new today, breakdown by priority

Format as a clean digest. If no new issues, respond with [SILENT]." \
  --name "Nightly backlog triage" \
  --deliver telegram
```

**Docs Drift Detection** — a weekly (`0 9 * * 1`) scan of merged PRs that flags code changes (tool schemas, CLI commands, config options, env vars) whose corresponding docs page was not updated in the same PR. Reports the gaps, or `[SILENT]` if everything is in sync.

**Dependency Security Audit** — a daily (`0 6 * * *`) run that `cd`s into the project, runs `pip audit` / `npm audit`, flags CVEs with CVSS ≥ 7.0 (listing package/version/CVE/severity, upgrade availability, direct-vs-transitive), and reports `[SILENT]` when clean.

## DevOps & Monitoring (schedule-triggered)

**Uptime Monitor** — checks endpoints every 30 minutes and only notifies on an outage. This is the one blueprint that uses `--script`: a precomputed Python check runs first and prints either `OUTAGE DETECTED` (with details) or `NO_ISSUES`, then the agent prompt interprets that output.

```python title="~/.hermes/scripts/check-uptime.py"
import urllib.request, json, time

ENDPOINTS = [
    {"name": "API", "url": "https://api.example.com/health"},
    {"name": "Web", "url": "https://www.example.com"},
    {"name": "Docs", "url": "https://docs.example.com"},
]

results = []
for ep in ENDPOINTS:
    try:
        start = time.time()
        req = urllib.request.Request(ep["url"], headers={"User-Agent": "Hermes-Monitor/1.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        elapsed = round((time.time() - start) * 1000)
        results.append({"name": ep["name"], "status": resp.getcode(), "ms": elapsed})
    except Exception as e:
        results.append({"name": ep["name"], "status": "DOWN", "error": str(e)})

down = [r for r in results if r.get("status") == "DOWN" or (isinstance(r.get("status"), int) and r["status"] >= 500)]
if down:
    print("OUTAGE DETECTED")
    for r in down:
        print(f"  {r['name']}: {r.get('error', f'HTTP {r[\"status\"]}')} ")
    print(f"\nAll results: {json.dumps(results, indent=2)}")
else:
    print("NO_ISSUES")
```

```bash
hermes cron create "every 30m" \
  "If the script reports OUTAGE DETECTED, summarize which services are down and suggest likely causes. If NO_ISSUES, respond with [SILENT]." \
  --script ~/.hermes/scripts/check-uptime.py \
  --name "Uptime monitor" \
  --deliver telegram
```

(The Deploy Verification and Alert Triage blueprints in this same source section are *webhook*-triggered → see [event blueprints](hermes_automation_blueprints_event.md).)

## Research & Intelligence

**Competitive Repository Scout** — a daily (`0 8 * * *`) job that scouts named AI-agent repos (`anthropics/claude-code`, `openai/codex`, `All-Hands-AI/OpenHands`, `Aider-AI/aider`) for the last 24h of notable PRs/issues, skips routine dependency bumps and CI fixes, and organizes findings by repo. Uses `--skill competitive-pr-scout`.

```bash
hermes cron create "0 8 * * *" \
  "Scout these AI agent repositories for notable activity in the last 24 hours:

Repos to check:
- anthropics/claude-code
- openai/codex
- All-Hands-AI/OpenHands
- Aider-AI/aider

For each repo:
1. gh pr list --repo <repo> --state all --json number,title,author,createdAt,mergedAt --limit 15
2. gh issue list --repo <repo> --state open --json number,title,labels,createdAt --limit 10

Focus on:
- New features being developed
- Architectural changes
- Integration patterns we could learn from
- Security fixes that might affect us too

Skip routine dependency bumps and CI fixes. If nothing notable, respond with [SILENT].
If there are findings, organize by repo with brief analysis of each item." \
  --skill competitive-pr-scout \
  --name "Competitor scout" \
  --deliver telegram
```

**AI News Digest** — a weekly (`0 9 * * 1`) web/GitHub/arXiv roundup structured into Headlines / Notable Papers / Open Source / Industry Moves, under 600 words.

**Paper Digest with Notes** — a daily (`0 8 * * *`) arXiv scan that picks 3 papers on "language model reasoning" / "tool-use agents" and writes one Obsidian note each (title, authors, abstract summary, key contribution, relevance), using `--skill arxiv --skill obsidian` and `--deliver local`.

**Daily Revenue Summary** — a daily (`0 8 * * *`) morning briefing that web-searches BTC/ETH prices, S&P 500 status, and recent tech/AI news into 3–4 bullets.

## Multi-Skill Workflows (schedule-triggered)

Two weekly multi-skill pipelines are schedule-triggered: the **Security Audit Pipeline** (`0 3 * * 0`, `--skill codebase-security-audit`) that checks dependency CVEs, scans for security anti-patterns, reviews recent commits, and writes a severity-categorized report; and the **Content Pipeline** (`0 10 * * 3`) that researches a trending AI-agent topic and drafts a ~300-word blog outline saved to `~/drafts/`. (The webhook-triggered multi-skill pipelines live in the [event blueprints](hermes_automation_blueprints_event.md) note.)

## Quick Reference

**Cron Schedule Syntax** — Hermes accepts both human shorthand (`every 30m`, `every 2h`) and standard 5-field cron:

| Expression | Meaning |
|-----------|---------|
| `every 30m` | Every 30 minutes |
| `every 2h` | Every 2 hours |
| `0 2 * * *` | Daily at 2:00 AM |
| `0 9 * * 1` | Every Monday at 9:00 AM |
| `0 9 * * 1-5` | Weekdays at 9:00 AM |
| `0 3 * * 0` | Every Sunday at 3:00 AM |
| `0 */6 * * *` | Every 6 hours |

**Delivery Targets** — `--deliver` controls where a job's output lands:

| Target | Flag | Notes |
|--------|------|-------|
| Same chat | `--deliver origin` | Default — delivers to where the job was created |
| Local file | `--deliver local` | Saves output, no notification |
| Telegram | `--deliver telegram` | Home channel, or `telegram:CHAT_ID` for specific |
| Discord | `--deliver discord` | Home channel, or `discord:CHANNEL_ID` |
| Slack | `--deliver slack` | Home channel |
| SMS | `--deliver sms:+15551234567` | Direct to phone number |
| Specific thread | `--deliver telegram:-100123:456` | Telegram forum topic |

**The `[SILENT]` Pattern** — when a cron job's response contains `[SILENT]`, delivery is suppressed. End the prompt with a line like "If nothing noteworthy happened, respond with [SILENT]." so you are only notified when the agent has something to report — the idiom every quiet-on-success blueprint above uses.

## Related Notes

**Terms**
- [term_cron](../../term_dictionary/term_cron.md) — scheduled-job concept; relevance: every blueprint here is a `cron create` job that fires on the scheduled cadence.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — terminal coding agent; relevance: each scheduled prompt runs the autonomous agent unattended.
- [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — agent run/loop coordination; relevance: each cron job invokes the agent orchestration loop on its prompt.
- [term_skills](../../term_dictionary/term_skills.md) — on-demand procedural knowledge; relevance: blueprints lean on installed `--skill` packs (scout, security-audit, arxiv) for repeatable work.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the agent execution harness; relevance: the cron-triggered run executes inside the harness.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated child agent; relevance: heavier blueprints can delegate parallel workstreams.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: blueprint prompts call tools (`gh`, web search, scripts) via function calling.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable-without-side-effects property; relevance: the `[SILENT]` pattern makes recurring runs idempotently quiet on no-change. (+fin: term_persistent_goal [own SP06a])

**Code-Repos**
- [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — cron scheduler/CRUD/tick + `--script` execution; relevance: every `hermes cron create` recipe in this note is implemented here.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes cron` command surface; relevance: the CLI flags (`--schedule`/`--script`/`--deliver`) the recipes type.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — delivery-target routing + `[SILENT]`; relevance: cron runs deliver via the gateway to a channel/DM.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent run each cron job invokes; relevance: each blueprint prompt runs the AIAgent loop.
- [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills the blueprints invoke (triage/digest/audit); relevance: blueprints lean on installed skills for repeatable work.

**Snippets**
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron job create/read/update/delete; relevance: the `cron create` recipes land a job through this CRUD code.
- [snippet_hermes_agent_cron_job_schema](../../code_snippets/snippet_hermes_agent_cron_job_schema.md) — cron job schema; relevance: defines the schedule/prompt/deliver fields each recipe fills.
- [snippet_hermes_agent_cron_job_validate](../../code_snippets/snippet_hermes_agent_cron_job_validate.md) — cron job validation; relevance: validates the cron expression + flags the recipes supply.
- [snippet_hermes_agent_cli_cron](../../code_snippets/snippet_hermes_agent_cli_cron.md) — `hermes cron` CLI command; relevance: the command surface the recipes are typed into.
- [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — cron job execution; relevance: runs the blueprint prompt when the schedule fires.
- [snippet_hermes_agent_cron_run_job_setup](../../code_snippets/snippet_hermes_agent_cron_run_job_setup.md) — cron run setup; relevance: prepares the run context (including `--script` output) for execution.
- [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — scheduler tick loop; relevance: the cadence clock that triggers each scheduled blueprint.
- [snippet_hermes_agent_gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — gateway cron runner; relevance: bridges a fired cron job to a gateway-delivered run.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: the `--deliver` target routing + `[SILENT]` suppression.
- [snippet_hermes_agent_core_run_agent_cli](../../code_snippets/snippet_hermes_agent_core_run_agent_cli.md) — agent-run entry point; relevance: each blueprint prompt enters the agent run here.

**Docs**
- [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event-driven blueprints; relevance: the webhook-triggered sibling to these schedule-triggered recipes.
- [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: cost/security tips for unattended cron runs.
- [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: the installed skills (triage/digest/audit) the blueprints invoke.
- [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: the programmatic batch alternative to a cron job.
- [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the MCP tools the blueprint prompts use inside cron jobs.
- [cc_routines_overview](../claude_code/cc_routines_overview.md) — CC scheduled-routine model; relevance: closest analogue to `hermes cron`.
- [cc_create_routine](../claude_code/cc_create_routine.md) — creating a CC scheduled routine; relevance: analogue to `cron create`.
- [cc_routine_triggers](../claude_code/cc_routine_triggers.md) — schedule/trigger config; relevance: analogue to cron syntax + delivery targets.
- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — how scheduled tasks execute; relevance: analogue to the cron `--script` run model.
- [cc_automate_and_scale](../claude_code/cc_automate_and_scale.md) — CC automation patterns; relevance: analogue to the blueprint cookbook.
- [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — CC recurring/loop scheduled tasks; relevance: analogue to the recurring nightly/daily cron blueprints.
- [cc_manage_routines](../claude_code/cc_manage_routines.md) — CC routine CRUD/management; relevance: analogue to `hermes cron list/delete` lifecycle.

**Source**: `inbox/hermes_agent_docs/guides/automation-blueprints.md` · https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
**Last Updated**: 2026-06-19
**Status**: Active
