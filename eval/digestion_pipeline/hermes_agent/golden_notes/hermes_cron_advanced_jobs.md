---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - cron
keywords:
  - no-agent mode
  - wakeAgent gate
  - context_from chaining
  - enabled_toolsets
  - provider recovery
  - silent suppression
topics:
  - Hermes Agent
  - Scheduled Tasks
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
access_control_group: ["general"]
---

# Hermes Agent — Advanced Cron Jobs (Cost-Control & Data-Flow Model)

## Overview

This is the **cost-control and data-flow model** layered on top of the basic Hermes cron lifecycle (create/edit/deliver/schedule, documented in [hermes_cron_scheduling](hermes_cron_scheduling.md)). Where the scheduling note covers *how to manage a job*, this note covers *what a job does each tick once it fires* and how to keep that tick cheap and resilient. Five mechanisms shape per-tick behavior: **no-agent mode** (`no_agent=True`) runs a bare script with zero LLM involvement; the **`wakeAgent` gate** lets a `$0` pre-run script decide whether the agent should run at all; **`context_from`** wires one job's output into the next job's prompt to build multi-stage pipelines; **`enabled_toolsets`** shrinks the tool-schema prompt per job for cost control; and **provider recovery** (inherited fallback providers + credential-pool rotation) keeps high-frequency runs resilient. A final **`[SILENT]`** delivery-suppression token turns chatty monitors quiet. Each mechanism exists to answer a single question: how do you run an agent on a schedule, often, without paying for empty work or failing silently when a provider rate-limits you.

## No-Agent Mode (Script-Only Jobs)

For recurring jobs that don't need LLM reasoning — classic watchdogs, disk/memory alerts, heartbeats, CI pings — pass `no_agent=True` at creation time. The scheduler runs the script on schedule and delivers its stdout directly, skipping the agent entirely:

```bash
hermes cron create "every 5m" \
  --no-agent \
  --script memory-watchdog.sh \
  --deliver telegram \
  --name "memory-watchdog"
```

Semantics:

- Script stdout (trimmed) → delivered verbatim as the message.
- **Empty stdout → silent tick**, no delivery. This is the watchdog pattern: "only say something when something is wrong".
- Non-zero exit or timeout → an error alert is delivered, so a broken watchdog can't fail silently.
- `{"wakeAgent": false}` on the last line → silent tick (same gate LLM jobs use).
- No tokens, no model, no provider fallback — the job never touches the inference layer.

`.sh` / `.bash` files run under `/bin/bash`; anything else under the current Python interpreter (`sys.executable`). Scripts must live in `~/.hermes/scripts/` (same sandboxing rule as the pre-run script gate). The `cronjob` tool's schema exposes `no_agent` to Hermes directly, so you can describe a watchdog in chat ("Ping me on Telegram if RAM is over 85%, every 5 minutes") and Hermes writes the check script via `write_file`, then calls `cronjob(action="create", schedule="every 5m", script="memory-watchdog.sh", no_agent=True, deliver="telegram", name="memory-watchdog")`. It picks `no_agent=True` automatically when the message content is fully determined by the script.

## Script Timeout

Pre-run scripts (attached via the `script` parameter) have a default timeout of 120 seconds. If your scripts need longer — for example, to include randomized delays that avoid bot-like timing patterns — increase it by setting `cron.script_timeout_seconds` in `~/.hermes/config.yaml` (e.g. `300` for 5 minutes), or set the `HERMES_CRON_SCRIPT_TIMEOUT` environment variable. The resolution order is: env var → `config.yaml` → 120s default.

## Skipping the Agent Entirely: `wakeAgent`

If your cron job attaches a pre-check script (via `script=`), the script can decide at runtime whether Hermes should even invoke the agent. Emit a final stdout line of the form `{"wakeAgent": false}` and cron skips the agent run entirely for this tick — useful for frequent polls (every 1–5 min) that only need to wake the LLM when state actually changed, otherwise you pay for zero-content agent turns repeatedly. When `wakeAgent` is omitted, the default is `true`. A script can also pass state forward to the woken agent via a `context` key.

```python
# pre-check script
import json, sys
latest = fetch_latest_issue_count()
prev = read_state("issue_count")
if latest == prev:
    print(json.dumps({"wakeAgent": False}))   # skip this tick
    sys.exit(0)
write_state("issue_count", latest)
print(json.dumps({"wakeAgent": True, "context": {"new_issues": latest - prev}}))
```

### Recipes: Cheap Pre-Run Gates

The `wakeAgent` gate gives you a `$0` way to decide whether a scheduled job should spend any LLM tokens at all. Three patterns cover most use cases:

- **File-change gate** — only run when a watched file has new content since the last successful tick. The scheduler records each job's `last_run_at`; the script compares the file's mtime against a stored timestamp and emits `{"wakeAgent": false}` when unchanged.
- **External-flag gate** — only run when another process signalled readiness (a deploy hook drops `/tmp/new-data-ready`, a CI job sets a value in your state store); the script consumes the flag and emits `{"wakeAgent": true}`.
- **SQL-count gate** — only run when there are new rows to process; the script can also pass the count through to the agent via `context`, so the agent knows the workload without re-querying.

```python
#!/usr/bin/env python
# ~/.hermes/scripts/new-rows.py
import json, sqlite3
conn = sqlite3.connect("/home/me/data/app.db")
n = conn.execute(
    "SELECT COUNT(*) FROM messages WHERE ts > strftime('%s','now','-2 hours')"
).fetchone()[0]
if n < 1:
    print(json.dumps({"wakeAgent": False}))
else:
    print(json.dumps({"wakeAgent": True, "context": {"new_rows": n}}))
```

The same pattern works for any data source you can query from a script — Postgres, an HTTP API, your own state store — without baking a SQL evaluator into the cron subsystem. **Do not** query Hermes's own `~/.hermes/state.db` from a pre-run gate: it is an internal schema that changes between releases. Point at your own database or feed instead. The recipe set was prompted by a contributor's exploration ([#2654](https://github.com/NousResearch/hermes-agent/pull/2654)) proposing sql/file/command triggers as a parallel mechanism; the `script` + `wakeAgent` gate already covers all three cases at `$0`, so the work landed as documentation. See the [Script-Only Cron Jobs guide](hermes_guide_cron_script_only.md) for worked examples.

## Chaining Jobs with `context_from`

Cron jobs run in isolated sessions with no memory of previous runs. But sometimes one job's output is exactly what the next job needs. The `context_from` parameter wires that connection automatically — Job B's prompt gets Job A's most recent completed output prepended as context at runtime. This models a collect → triage → ship ETL pipeline across otherwise-isolated jobs:

```python
# Job 1: Collect — fetch raw data, save to a file
cronjob(action="create", name="AI News Collector", schedule="0 7 * * *",
        prompt="Fetch the top 10 AI/ML stories from Hacker News. Save them to ~/.hermes/data/briefs/raw.md ...")

# Job 2: Triage — receives Job 1's output as context
cronjob(action="create", name="AI News Triage", schedule="30 7 * * *", context_from="<job1_id>",
        prompt="Read ~/.hermes/data/briefs/raw.md. Score each story 1–10 ... Output the top 5 to ranked.md.")

# Job 3: Ship — receives Job 2's output as context
cronjob(action="create", name="AI News Brief", schedule="0 8 * * *", context_from="<job2_id>",
        prompt="Read ~/.hermes/data/briefs/ranked.md. Write 3 tweet drafts. Deliver to telegram:7976161601.")
```

**How it works:** when Job 2 fires, Hermes reads Job 1's most recent output from `~/.hermes/cron/output/{job1_id}/*.md` and prepends it to Job 2's prompt automatically — Job 2 doesn't need to hardcode "read this file". The chain can be any length (Job 1 → Job 2 → Job 3 → …). `context_from` accepts a single job ID/name string (`context_from="a1b2c3d4"`) or a list of IDs/names (`context_from=["ai-news-fetch", "github-prs-fetch"]`); outputs are concatenated in the order listed. Each upstream entry must be a valid job ID or name (see `cronjob(action="list")`). Use it for multi-stage pipelines (collect → filter → format → deliver), dependent tasks where step N depends on step N−1, and fan-out/fan-in aggregation. **Note:** chaining reads the *most recent completed* output — it does not wait for upstream jobs running in the same tick.

## Toolsets Available to Cron Jobs (`enabled_toolsets`)

Cron runs each job in a fresh agent session with no chat platform attached. By default the cron agent gets **the toolset you configured for the `cron` platform in `hermes tools`** — not the CLI default, not everything. Tighter per-job control is available via the `enabled_toolsets` field on `cronjob.create` (or on an existing job via `cronjob.update`):

```text
cronjob(action="create", name="weekly-news-summary",
        schedule="every sunday 9am",
        enabled_toolsets=["web", "file"],      # just web + file, no terminal/browser/etc.
        prompt="Summarize this week's AI news: ...")
```

When `enabled_toolsets` is set on a job it wins; otherwise the `hermes tools` cron-platform config wins; otherwise Hermes falls back to the built-in defaults. **This matters for cost control:** carrying `moa`, `browser`, `delegation` into every tiny "fetch news" job bloats the tool-schema prompt on every LLM call.

## Provider Recovery

Cron jobs inherit your configured fallback providers and credential-pool rotation. If the primary API key is rate-limited or the provider returns an error, the cron agent can:

- **Fall back to an alternate provider** if you have `fallback_providers` (or the legacy `fallback_model`) configured in `config.yaml` — concept home is [hermes_fallback_providers](hermes_fallback_providers.md).
- **Rotate to the next credential** in your credential pool for the same provider — concept home is [hermes_credential_pools](hermes_credential_pools.md).

This means cron jobs that run at high frequency or during peak hours are more resilient — a single rate-limited key won't fail the entire run.

## Silent Suppression (`[SILENT]`)

If the agent's final response contains `[SILENT]`, delivery is suppressed entirely. The output is still saved locally for audit (`~/.hermes/cron/output/`), but no message is sent to the delivery target. This is useful for monitoring jobs that should only report when something is wrong:

```text
Check if nginx is running. If everything is healthy, respond with only [SILENT].
Otherwise, report the issue.
```

Failed jobs always deliver regardless of the `[SILENT]` marker — only successful runs can be silenced. For quiet monitoring jobs, prompt the agent to reply with only `[SILENT]` when there is nothing to report.

**Source**: `inbox/hermes_agent_docs/user-guide/features/cron.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
**Last Updated**: 2026-06-19
**Status**: Active
