---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - cron
keywords:
  - automate with cron
  - cron automation patterns
  - website change monitor
  - script pre-check
  - silent quiet marker
  - delivery targets
  - schedule expression syntax
  - multi-skill workflow
topics:
  - Hermes Agent
  - Cron Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron
access_control_group: ["general"]
---

# Hermes Agent — Automate Anything with Cron

## Overview

This is the recipe layer that takes the [daily briefing bot starter](hermes_guide_daily_briefing_bot.md) further: **five reusable, LLM-driven cron automation patterns** you can adapt to your own workflows, plus the shared mechanics they all rely on (the `--script` pre-check, the `[SILENT]` quiet marker, the `--deliver` target matrix, and the supported schedule-expression syntax). Every pattern is a Hermes [cron](../../term_dictionary/term_cron.md) job — a scheduled task that runs in a **fresh agent session with no memory of your current chat**, so prompts must be **completely self-contained** (include every URL, repo name, command, format preference, and delivery instruction inline). For the full parameter-by-parameter cron reference, edge cases, and internals, this guide links out to the feature page rather than duplicating it.

Two zero-token escape hatches are noted up front: a recurring watchdog where the script already produces the exact message belongs in a [script-only cron job](hermes_guide_cron_script_only.md) (same scheduler, no LLM), and a one-shot from an already-running script (CI step, post-commit hook, deploy script) should use [`hermes send`](hermes_guide_pipe_script_output.md) to pipe stdout straight to a platform without a cron entry. Both keep the LLM out of the loop when no reasoning is needed.

## Pattern 1: Website Change Monitor

Watch a URL for changes and get notified only when something is different. The `--script` parameter is the key mechanic: a Python script runs *before* each execution and its stdout becomes context for the agent. The script handles the mechanical work (fetching, hashing, diffing against saved state); the agent handles the reasoning (is this change interesting?). The script saves a state hash under `~/.hermes/scripts/`, prints `CHANGE DETECTED` plus the new content when the hash differs, and prints `NO_CHANGE` otherwise — so the agent only has to reason, never fetch.

```bash
/cron add "every 1h" "If the script output says CHANGE DETECTED, summarize what changed on the page and why it might matter. If it says NO_CHANGE, respond with just [SILENT]." --script ~/.hermes/scripts/watch-site.py --name "Pricing monitor" --deliver telegram
```

The `[SILENT]` trick: instruct the agent to respond with only `[SILENT]` when nothing changed. Cron delivery treats `[SILENT]` as the quiet marker, so you only get notified when something actually happens — no spam on quiet hours. (For the full pre-check script that fetches, SHA-256-hashes, and diffs the page, see the source.)

## Pattern 2: Weekly Report

Compile information from multiple sources into one formatted summary on a fixed weekly schedule, delivered to your home channel. The prompt enumerates each source (web AI news, trending GitHub ML repos, most-discussed Hacker News posts), the output format (sectioned, with links), and a length cap — all inline, because the fresh session knows nothing.

```bash
hermes cron create "0 9 * * 1" \
  "Generate a weekly report covering the top AI news, trending ML GitHub repos, and most-discussed HN posts. Format with sections, include links, keep under 500 words." \
  --name "Weekly AI digest" \
  --deliver telegram
```

`0 9 * * 1` is a standard cron expression: 9:00 AM every Monday. The same job can be created from chat with `/cron add "0 9 * * 1" "…"`; the CLI form shown here is the equivalent for scripted setup.

## Pattern 3: GitHub Repository Watcher

Monitor a repository for new issues, PRs, or releases on an interval. Because the cron agent has no memory of previous runs or your preferences, the prompt **spells out the exact `gh` commands** to run, the time window to filter on, and the `[SILENT]` fallback when nothing is new.

```bash
/cron add "every 6h" "Check the GitHub repository NousResearch/hermes-agent for new issues, PRs, and releases in the last 6 hours.
Use the terminal to run:
  gh issue list --repo NousResearch/hermes-agent --state open --json number,title,author,createdAt --limit 10
  gh pr list --repo NousResearch/hermes-agent --state all --json number,title,author,createdAt,mergedAt --limit 10
Filter to only items from the last 6 hours. If nothing new, respond with [SILENT].
Otherwise, provide a concise summary." --name "Repo watcher" --deliver discord
```

This is the general-purpose form of the dedicated [cron-polling PR reviewer](hermes_guide_github_pr_review_cron.md), which adds a review skill and posts verdicts back.

## Pattern 4: Data Collection Pipeline

Scrape data at regular intervals, append to a history file, and detect trends over time. This pattern combines a script (mechanical collection) with the agent (analysis). A Python pre-check fetches the data (e.g. crypto prices), appends a timestamped JSON line to `~/.hermes/data/prices/history.jsonl`, then prints the current values plus the last few data points; the agent receives only that stdout.

```bash
/cron add "every 1h" "Analyze the price data from the script output. Report: current prices, trend direction over the last 6 data points (up/down/flat), and any notable movements (>5% change).
If prices are flat and nothing notable, respond with [SILENT]. If there's a significant move, explain what happened." \
  --script ~/.hermes/scripts/collect-prices.py \
  --name "Price tracker" \
  --deliver telegram
```

The script does the mechanical collection and history-tracking; the agent adds the reasoning layer. This is cheaper and more reliable than having the agent do the fetching itself — a recurring theme of the `--script` mechanic.

## Pattern 5: Multi-Skill Workflow

Chain [skills](../../term_dictionary/term_skills.md) together for complex scheduled tasks. Skills are loaded **in order** before the prompt executes, so list them in the sequence the agent should learn them. Here `arxiv` (teaches the agent how to search papers) loads first, then `obsidian` (teaches how to write notes); the prompt ties them together.

```python
cronjob(
    action="create",
    skills=["arxiv", "obsidian"],
    prompt="Search arXiv for papers on 'language model reasoning' from the past day. Save the top 3 as Obsidian notes.",
    schedule="0 8 * * *",
    name="Paper digest",
    deliver="local"
)
```

The equivalent chat form is `/cron add "0 8 * * *" "…" --skill arxiv --skill obsidian --name "Paper digest"` — repeated `--skill` flags preserve load order.

## Managing Your Jobs

The same lifecycle commands work from chat (`/cron …`) or the CLI (`hermes cron …`):

```bash
/cron list                                   # List all active jobs
/cron run <job_id>                           # Trigger immediately (for testing)
/cron pause <job_id>                         # Pause without deleting
/cron edit <job_id> --schedule "every 4h"    # Change schedule
/cron edit <job_id> --prompt "New task"      # Change prompt
/cron edit <job_id> --skill arxiv            # Add a skill (or --clear-skills)
/cron remove <job_id>                        # Delete permanently
```

Always `/cron run <job_id>` to test before waiting on the schedule — it executes immediately so you can verify the output looks right.

## Delivery Targets

The `--deliver` flag controls where results go. `origin` (the default) sends back to the chat that created the job; named platforms go to your home channel on that platform; and a `platform:chat[:thread]` form targets a specific group or topic thread.

| Target | Example | Use case |
|--------|---------|----------|
| `origin` | `--deliver origin` | Same chat that created the job (default) |
| `local` | `--deliver local` | Save to local file only |
| `telegram` / `discord` / `slack` | `--deliver telegram` | Your home channel on that platform |
| Specific chat | `--deliver telegram:-1001234567890` | A specific Telegram group |
| Threaded | `--deliver telegram:-1001234567890:17585` | A specific Telegram topic thread |

For pushing output from a script that is already running (rather than a scheduled job), route to [`hermes send`](hermes_guide_pipe_script_output.md) instead.

## Tips

- **Make prompts self-contained.** The cron agent has no memory of your conversations — include URLs, repo names, format preferences, and delivery instructions directly in the prompt.
- **Use `[SILENT]` deliberately.** For monitoring jobs, instruct "if nothing changed, respond with only `[SILENT]`." Do not ask the agent to explain the token in quiet cases — cron treats `[SILENT]` as the delivery-suppression marker.
- **Use scripts for data collection.** The `--script` parameter lets a Python script handle HTTP requests, file I/O, and state tracking; the agent only sees its stdout and applies reasoning. Cheaper and more reliable than agent-side fetching.
- **Test with `/cron run`.** Execute immediately to verify output before waiting for the schedule.
- **Schedule expressions.** Supported formats: relative delays (`30m`), intervals (`every 2h`), standard cron expressions (`0 9 * * *`), and ISO timestamps (`2025-06-15T09:00:00`). Natural language like `daily at 9am` is **not** supported — use the cron form (see [term_cron_expression](../../term_dictionary/term_cron_expression.md)). For a watchdog with no reasoning, drop to [script-only cron](hermes_guide_cron_script_only.md); if a job misbehaves, see [cron troubleshooting](hermes_guide_cron_troubleshooting.md).

**Source**: `inbox/hermes_agent_docs/guides/automate-with-cron.md` · https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron
**Last Updated**: 2026-06-19
**Status**: Active
