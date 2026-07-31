---
tags:
  - resource
  - documentation
  - openclaw
  - automation
  - cron
keywords:
  - openclaw cron scheduling
  - cron schedule types at every cron
  - day-of-month day-of-week or logic croner
  - isolated vs in-session execution style
  - command payload cron job
  - cron delivery announce webhook none
  - openclaw cron cli managing jobs
  - model selection precedence isolated cron
topics:
  - OpenClaw
  - Cron Scheduling
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/automation/cron-jobs
access_control_group: ["general"]
---

# OpenClaw — Defining Cron Jobs: Schedules, Execution Styles, and the `oc cron` CLI

## Overview

This note is the procedure for defining and managing OpenClaw **cron jobs** — the Gateway's built-in scheduler that persists jobs, wakes the agent at the right time, and delivers output to a chat channel or webhook. It mirrors the scheduling half of the `automation/cron-jobs` source page: quick start, how cron runs inside the Gateway, the three schedule types (`at` / `every` / `cron`) plus the day-of-month/day-of-week OR-logic gotcha, the four execution styles (main / isolated / current / custom) with command payloads and isolated-job payload options, delivery/output modes, output-language control, the `openclaw cron` CLI, and listing/editing/running/removing jobs. The event-trigger surfaces (webhooks, Gmail PubSub), the `cron` config block, and troubleshooting live in the sibling note `oc_automation_cron_jobs_triggers_config`.

## Quick start

Add a one-shot reminder, then inspect with `openclaw cron list` / `get <job-id>` / `show <job-id>` and `openclaw cron runs --id <job-id>` (see Managing jobs):

```bash
openclaw cron create "2026-02-01T16:00:00Z" \
  --name "Reminder" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run
```

## How cron works

- Cron runs **inside the Gateway** process (not inside the model). Job definitions, runtime state, and run history persist in OpenClaw's shared SQLite state database so restarts do not lose schedules.
- On upgrade, `openclaw doctor --fix` imports legacy `~/.openclaw/cron/jobs.json`, `jobs-state.json`, and `runs/*.jsonl` into SQLite (renaming them `.migrated`; malformed rows go to `jobs-quarantine.json`). After import, editing that JSON no longer changes active jobs — use `openclaw cron add|edit|remove` or the Gateway cron RPC methods.
- All cron executions create [background task](oc_automation_tasks_lifecycle.md) records. One-shot jobs (`--at`) auto-delete after success by default. On Gateway startup, overdue isolated agent-turn jobs are rescheduled out of the channel-connect window instead of replaying immediately.
- Isolated runs best-effort close tracked browser tabs/processes for their `cron:<jobId>` session on completion, and a run with the narrow self-cleanup grant can read scheduler status / its own job / that job's run history without broader cron mutation access. On `timeoutSeconds`, cron aborts the run and gives a short cleanup window; if it does not drain, Gateway-owned cleanup force-clears the run's session ownership before recording the timeout. Stalls before the runner starts or before the first model call record phase-specific timeouts (e.g. `setup timed out before runner start`), capped independently from long `timeoutSeconds`.
- If an external scheduler runs `openclaw agent`, wrap it with hard-kill escalation (GNU `timeout -k 60 600 ...`; systemd `SIGTERM` + `TimeoutStopSec`). Reusing a `--run-id` while the original Gateway run is still active reports the duplicate as in-flight rather than starting a second run.

Task reconciliation is runtime-owned first, durable-history-backed second: an active cron task stays live while the runtime still tracks the job as running; once it stops owning the job and the 5-minute grace window expires, maintenance checks persisted run logs for the matching `cron:<jobId>:<startedAt>` run, finalizing from a terminal durable result or else marking the task `lost`.

## Schedule types

| Kind | CLI flag | Description |
| --- | --- | --- |
| `at` | `--at` | One-shot timestamp (ISO 8601 or relative like `20m`) |
| `every` | `--every` | Fixed interval |
| `cron` | `--cron` | 5-field or 6-field cron expression with optional `--tz` |

Timestamps without a timezone are treated as UTC; add `--tz America/New_York` for local wall-clock scheduling. Recurring top-of-hour expressions are automatically staggered by up to 5 minutes to reduce load spikes — use `--exact` to force precise timing or `--stagger 30s` for an explicit window.

### Day-of-month and day-of-week use OR logic

Cron expressions are parsed by [croner](https://github.com/Hexagon/croner). When both the day-of-month and day-of-week fields are non-wildcard, croner matches when **either** field matches — not both (standard Vixie cron behavior). The example `0 9 15 * 1` is intended as "9 AM on the 15th, only if Monday" but actually fires "9 AM on every 15th, AND every Monday" (~5–6×/month, not 0–1). To require both, use croner's `+` modifier (`0 9 15 * +1`) or guard one field in the job's prompt.

## Execution styles

| Style | `--session` value | Runs in | Best for |
| --- | --- | --- | --- |
| Main session | `main` | Dedicated cron wake lane | Reminders, system events |
| Isolated | `isolated` | Dedicated `cron:<jobId>` | Reports, background chores |
| Current session | `current` | Bound at creation time | Context-aware recurring work |
| Custom session | `session:custom-id` | Persistent named session | Workflows that build on history |

**Main session** jobs enqueue a system event into a cron-owned run lane and optionally wake the heartbeat (`--wake now` or `--wake next-heartbeat`); they do not append routine cron turns to the human chat lane or extend daily/idle reset freshness, and do NOT auto-include the heartbeat prompt's "Read HEARTBEAT.md" (say it in the event text if needed). **Isolated** jobs run a dedicated agent turn with a fresh session — a new transcript/session id per run, carrying safe preferences (thinking/fast/verbose, labels, explicit model/auth overrides) but NOT ambient context (channel/group routing, send/queue policy, elevation, origin, ACP runtime binding); teardown best-effort cleans up browser tabs and bundled MCP runtime instances. **Custom sessions** (`session:xxx`) persist context across runs (e.g. daily standups); use `current` or `session:<id>` to deliberately build on the same conversation context.

### Command payloads

Use command payloads for deterministic scripts that run inside the Gateway scheduler without a model-backed agent turn. Command jobs execute on the Gateway host, capture stdout/stderr, record the run in cron history, and reuse the `announce`/`webhook`/`none` delivery modes. Command cron is an operator-admin surface, not an agent `tools.exec` call: creating, editing, removing, or manually running cron jobs requires `operator.admin`, and scheduled command runs execute inside the Gateway process as that admin-authored automation (agent exec policy like `tools.exec.mode` governs model-visible exec tools, not command cron payloads).

```bash
openclaw cron create "*/15 * * * *" \
  --name "Queue depth probe" \
  --command "scripts/check-queue.sh" \
  --command-cwd "/srv/app" \
  --announce \
  --channel telegram \
  --to "-1001234567890"
```

`--command <shell>` stores `argv: ["sh", "-lc", <shell>]`; use `--command-argv '["node","scripts/report.mjs"]'` for exact argv without shell parsing. Optional `--command-env KEY=VALUE`, `--command-input`, `--timeout-seconds`, `--no-output-timeout-seconds`, and `--output-max-bytes` control environment, stdin, and output bounds. Non-empty stdout is the delivered result (else stderr; if both, a `stdout:` / `stderr:` block). Zero exit records `ok`; non-zero exit, signal, timeout, or no-output timeout records `error`. A command printing only `NO_REPLY` uses silent-token suppression and posts nothing.

### Payload options for isolated jobs

Isolated jobs take these payload fields: `--message` (prompt text, required), `--model` (override; uses the selected allowed model), `--clear-model` (on `cron edit`, removes the per-job override — cannot combine with `--model`), `--thinking` (thinking level), `--light-context` (skip workspace bootstrap file injection), and `--tools` (restrict tools, e.g. `--tools exec,read`).

`--model` is the job's primary model, NOT a chat-session `/model` override: configured fallback chains still apply on failure, and if the model is not allowed or cannot be resolved cron fails the run with an explicit validation error rather than silently falling back. Payload-level `fallbacks` replaces the configured chain; `fallbacks: []` is a strict run trying only the selected model. Model-selection precedence is: (1) Gmail hook model override (when the run came from Gmail and is allowed); (2) per-job payload `model`; (3) stored cron-session model override; (4) agent/default selection. Fast mode follows the resolved selection (`params.fastMode`, unless a stored session `fastMode` override wins). On a live model-switch handoff, cron retries with the switched provider/model, bounded to the initial attempt plus 2 switch retries.

## Delivery and output

| Mode | What happens |
| --- | --- |
| `announce` | Fallback-deliver final text to the target if the agent did not send |
| `webhook` | POST finished event payload to a URL |
| `none` | No runner fallback delivery |

Use `--announce --channel telegram --to "-1001234567890"` for channel delivery. Telegram forum topics use `-1001234567890:topic:123`; Slack/Discord/Mattermost targets use explicit prefixes (`channel:<id>`, `user:<id>`); Matrix room IDs are case-sensitive (`room:!room:server`). When announce uses `channel: "last"` or omits `channel`, a provider-prefixed target like `telegram:123` can select the channel before falling back to session history; if `delivery.channel` is explicit the target prefix must name the same provider. For isolated jobs chat delivery is shared — the agent can use the `message` tool even under `--no-deliver`, and OpenClaw skips the fallback announce if the agent already sent to the target. DM pairing-store approvals are not fallback recipients — set `delivery.to` or the channel `allowFrom` entry to proactively DM.

## Output language

Cron jobs do not infer a reply language from channel, locale, or previous messages — put the language rule in the scheduled message or template:

```bash
openclaw cron edit <jobId> \
  --message "Summarize the updates. Respond in Chinese; keep URLs, code, and product names unchanged."
```

For template files, keep the language instruction in the rendered prompt and verify placeholders like `{{language}}` are filled. Failure notifications follow a separate path: `cron.failureDestination` is the global default, `job.delivery.failureDestination` overrides per job, and if neither is set but the job already delivers via `announce` failures fall back to that announce target (`delivery.failureDestination` is only supported on `sessionTarget="isolated"` jobs unless delivery is `webhook`). `failureAlert.includeSkipped: true` opts into repeated skipped-run alerts.

## CLI examples

```bash
# One-shot reminder
openclaw cron add --name "Calendar check" --at "20m" --session main \
  --system-event "Next heartbeat: check calendar." --wake now

# Recurring isolated job
openclaw cron create "0 7 * * *" "Summarize overnight updates." \
  --name "Morning brief" --tz "America/Los_Angeles" --session isolated \
  --announce --channel slack --to "channel:C1234567890"

# Model and thinking override
openclaw cron add --name "Deep analysis" --cron "0 6 * * 1" \
  --tz "America/Los_Angeles" --session isolated \
  --message "Weekly deep analysis of project progress." \
  --model "opus" --thinking high --announce

# Webhook output (POSTs the finished payload; see the sibling triggers/config note)
openclaw cron create "0 18 * * 1-5" "Summarize today's deploys as JSON." \
  --name "Deploy digest" --webhook "https://example.invalid/openclaw/cron"
```

## Managing jobs

```bash
openclaw cron list                       # List all jobs
openclaw cron get <jobId>                 # Get one stored job as JSON
openclaw cron show <jobId>                # Show one job, including resolved delivery route
openclaw cron edit <jobId> --message "Updated prompt" --model "opus"
openclaw cron run <jobId>                 # Force run a job now
openclaw cron run <jobId> --wait --wait-timeout 10m --poll-interval 2s
openclaw cron run <jobId> --due           # Run only if due
openclaw cron runs --id <jobId> --limit 50
openclaw cron runs --id <jobId> --run-id <runId>
openclaw cron remove <jobId>              # Delete a job
openclaw cron create "0 6 * * *" "Check ops queue" --name "Ops sweep" --session isolated --agent ops
openclaw cron edit <jobId> --clear-agent
```

`openclaw cron run <jobId>` returns after enqueueing; `--wait` blocks until the queued run finishes, polling the returned `runId` and exiting `0` for `ok`, non-zero for `error`/`skipped`/wait-timeout. The agent `cron` tool returns compact summaries (`id`, `name`, `enabled`, `nextRunAtMs`, `scheduleKind`, `lastRunStatus`) from `cron(action: "list")`; use `cron(action: "get", jobId: "...")` for one full definition (Gateway callers can pass `compact: true` to `cron.list`). `openclaw cron create` aliases `cron add`, and new jobs accept a positional schedule (`"0 9 * * 1"`, `"every 1h"`, `"20m"`, or ISO timestamp) plus a positional prompt. `--webhook <url>` on `cron add|create|edit` POSTs the finished run payload and cannot combine with chat-delivery flags (`--announce`, `--channel`, `--to`, `--thread-id`, `--account`). On `cron edit`, `--clear-channel`/`--clear-to`/`--clear-thread-id`/`--clear-account` unset routing fields individually (distinct from `--no-deliver` disabling runner fallback delivery); API `cron.update` patches can set `model: null` to clear a stored model override.

**Source**: OpenClaw documentation — `automation/cron-jobs` (mirror `inbox/openclaw_docs/automation/cron-jobs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
