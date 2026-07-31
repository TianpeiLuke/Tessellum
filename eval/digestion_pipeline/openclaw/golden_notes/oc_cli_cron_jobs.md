---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - cron
keywords:
  - openclaw cron create
  - openclaw cron add
  - cron job scheduling
  - cron webhook delivery
  - cron command jobs
  - cron session isolated main current
  - cron one-shot recurring backoff
  - cron failure delivery destination
  - cron manual run wait due
topics:
  - OpenClaw
  - Cron CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/cron
access_control_group: ["general"]
---

# OpenClaw — Authoring `openclaw cron` Jobs (Create, Sessions, Delivery, Scheduling, Edits)

## Overview

This note is the authoring half of the `openclaw cron` CLI reference (mirror `inbox/openclaw_docs/cli/cron.md`): how to create cron jobs for the OpenClaw Gateway scheduler, bind them to a session, route their output, and schedule them. It covers the `create`/`add` command (prompt vs `--webhook` vs `--command` jobs), the `--session` key choices (`main`/`isolated`/`current`/`session:<id>`) and isolated-run reset semantics, the three delivery modes (announce / webhook / none) with ownership and failure-destination resolution, one-shot vs recurring (retry backoff) vs manual (`--wait`/`--due`) scheduling, and common `cron edit` edits. The companion note [oc_cli_cron_run](oc_cli_cron_run.md) covers running and administering jobs (per-job model selection, run output/denials, retention, legacy-job migration, and the `list`/`get`/`show`/`run`/`runs` admin commands). The conceptual guide at `/automation/cron-jobs` is linked, not duplicated.

## Create jobs quickly

`openclaw cron create` is an alias for `openclaw cron add`. For new jobs, put the schedule (a cron expression) first and the prompt second:

```bash
openclaw cron create "0 7 * * *" \
  "Summarize overnight updates." \
  --name "Morning brief" \
  --agent ops
```

Use `--webhook <url>` when the job should POST the finished payload instead of delivering to a chat target:

```bash
openclaw cron create "0 18 * * 1-5" \
  "Summarize today's deploys as JSON." \
  --name "Deploy digest" \
  --webhook "https://example.invalid/openclaw/cron"
```

Use `--command` for deterministic shell-style jobs that should run inside OpenClaw cron without starting an isolated agent/model run. Per the source, command cron jobs are admin-authored Gateway automation: creating, editing, removing, or manually running them requires `operator.admin`; the scheduled run later executes in the Gateway process, not as an agent `tools.exec` tool call (`tools.exec.*` and exec approvals still govern model-visible exec tools).

```bash
openclaw cron create "*/15 * * * *" \
  --name "Queue depth probe" \
  --command "scripts/check-queue.sh" \
  --command-cwd "/srv/app" \
  --announce \
  --channel telegram \
  --to "-1001234567890"
```

`--command <shell>` stores `argv: ["sh", "-lc", <shell>]`. Use `--command-argv '["node","scripts/report.mjs"]'` for exact argv execution. Command jobs capture stdout/stderr, record normal cron history, and route output through the same `announce`, `webhook`, or `none` delivery modes as isolated jobs. A command that prints only `NO_REPLY` is suppressed.

## Sessions

`--session` accepts `main`, `isolated`, `current`, or `session:<id>`.

### Session keys

- `main` binds to the agent's main session.
- `isolated` creates a fresh transcript and session id for each run.
- `current` binds to the active session at creation time.
- `session:<id>` pins to an explicit persistent session key.

### Isolated session semantics

Isolated runs reset ambient conversation context. Channel and group routing, send/queue policy, elevation, origin, and ACP runtime binding are reset for the new run. Safe preferences and explicit user-selected model or auth overrides can carry across runs.

## Delivery

`openclaw cron list` and `openclaw cron show <job-id>` preview the resolved delivery route. For `channel: "last"`, the preview shows whether the route resolved from the main or current session, or will fail closed.

Provider-prefixed targets can disambiguate unresolved announce channels. For example, `to: "telegram:123"` selects Telegram when `delivery.channel` is omitted or `last`. Only prefixes advertised by the loaded plugin are provider selectors. If `delivery.channel` is explicit, the prefix must match that channel; `channel: "whatsapp"` with `to: "telegram:123"` is rejected. Service prefixes such as `imessage:` and `sms:` remain channel-owned target syntax.

Per the source Note: isolated `cron add` jobs default to `--announce` delivery. Use `--no-deliver` to keep output internal. `--deliver` remains as a deprecated alias for `--announce`.

### Delivery ownership

Isolated cron chat delivery is shared between the agent and the runner:

- The agent can send directly using the `message` tool when a chat route is available.
- `announce` fallback-delivers the final reply only when the agent did not send directly to the resolved target.
- `webhook` posts the finished payload to a URL.
- `none` disables runner fallback delivery.

Use `cron add|create --webhook <url>` or `cron edit <job-id> --webhook <url>` to set webhook delivery. Do not combine `--webhook` with chat delivery flags such as `--announce`, `--no-deliver`, `--channel`, `--to`, `--thread-id`, or `--account`.

`cron edit <job-id>` can unset individual delivery routing fields with `--clear-channel`, `--clear-to`, `--clear-thread-id`, and `--clear-account` (each is rejected when combined with its matching set flag). Unlike `--no-deliver`, which only disables runner fallback delivery, these remove the stored field so the job resolves that part of its route from defaults again.

`--announce` is runner fallback delivery for the final reply. `--no-deliver` disables that fallback but does not remove the agent's `message` tool when a chat route is available. Reminders created from an active chat preserve the live chat delivery target for fallback announce delivery. Internal session keys may be lowercase; do not use them as a source of truth for case-sensitive provider IDs such as Matrix room IDs.

### Failure delivery

Failure notifications resolve in this order:

1. `delivery.failureDestination` on the job.
2. Global `cron.failureDestination`.
3. The job's primary announce target (when no explicit failure destination is set).

Per the source Note: main-session jobs may only use `delivery.failureDestination` when primary delivery mode is `webhook`; isolated jobs accept it in all modes. Isolated cron runs treat run-level agent failures as job errors even when no reply payload is produced, so model/provider failures still increment error counters and trigger failure notifications. Command cron jobs do not start an isolated agent turn: a zero exit code records `ok`; non-zero exit, signal, timeout, or no-output timeout records `error` and can trigger the same failure notification path. If an isolated run times out before the first model request, `openclaw cron show` and `openclaw cron runs` include a phase-specific error such as `setup timed out before runner start` or `stalled before first model call (last phase: context-engine)`. For CLI-backed providers, the pre-model watchdog stays active until the external CLI turn starts, so session lookup, hook, auth, prompt, and CLI setup stalls are reported as pre-model cron failures.

## Scheduling

### One-shot jobs

`--at <datetime>` schedules a one-shot run. Offset-less datetimes are treated as UTC unless you also pass `--tz <iana>`, which interprets the wall-clock time in the given timezone. Per the source Note: one-shot jobs delete after success by default; use `--keep-after-run` to preserve them.

### Recurring jobs

Recurring jobs use exponential retry backoff after consecutive errors: 30s, 1m, 5m, 15m, 60m. The schedule returns to normal after the next successful run. Skipped runs are tracked separately from execution errors. They do not affect retry backoff, but `openclaw cron edit <job-id> --failure-alert-include-skipped` can opt failure alerts into repeated skipped-run notifications. For isolated jobs that target a local configured model provider, cron runs a lightweight provider preflight before starting the agent turn (loopback, private-network, and `.local` `api: "ollama"` providers are probed at `/api/tags`; local OpenAI-compatible providers such as vLLM, SGLang, and LM Studio are probed at `/models`); if the endpoint is unreachable, the run is recorded as `skipped` and retried on a later schedule, and matching dead endpoints are cached for 5 minutes to avoid many jobs hammering the same local server. Note: cron jobs, pending runtime state, and run history live in the shared SQLite state database; legacy `jobs.json`, `jobs-state.json`, and `runs/*.jsonl` files are imported once and renamed with a `.migrated` suffix, and after import you edit schedules with `openclaw cron add|edit|remove` instead of editing JSON files.

### Manual runs

`openclaw cron run <job-id>` force-runs by default and returns as soon as the manual run is queued. Successful responses include `{ ok: true, enqueued: true, runId }`. Use the returned `runId` to inspect the later result, and add `--wait` when a script should block until that exact queued run records a terminal status:

```bash
openclaw cron run <job-id>
openclaw cron runs --id <job-id> --run-id <run-id>
openclaw cron run <job-id> --wait --wait-timeout 10m --poll-interval 2s
```

With `--wait`, the CLI still calls `cron.run` first, then polls `cron.runs` for the returned `runId`. The command exits `0` only when the run finishes with status `ok`. It exits non-zero when the run finishes with `error` or `skipped`, when the Gateway response does not include a `runId`, or when `--wait-timeout` expires. `--poll-interval` must be greater than zero. Per the source Note: use `--due` when you want the manual command to run only if the job is currently due; if `--due --wait` does not enqueue a run, the command returns the normal non-run response instead of polling.

## Common edits

Update delivery settings without changing the message:

```bash
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
openclaw cron edit <job-id> --no-deliver
openclaw cron edit <job-id> --light-context
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
openclaw cron edit <job-id> --announce --channel telegram --to "-1001234567890" --thread-id 42
```

The edits above disable delivery for an isolated job (`--no-deliver`), enable lightweight bootstrap context for an isolated job (`--light-context`), announce to a specific channel (Slack channel target), and announce to a Telegram forum topic (`--thread-id 42`). `--light-context` applies to isolated agent-turn jobs only; for cron runs, lightweight mode keeps bootstrap context empty instead of injecting the full workspace bootstrap set. You can also create an isolated job with lightweight bootstrap context, or a command job with exact argv, cwd, env, stdin, and output limits:

```bash
openclaw cron create "0 7 * * *" \
  "Summarize overnight updates." \
  --name "Lightweight morning brief" \
  --session isolated \
  --light-context \
  --no-deliver

openclaw cron create "*/30 * * * *" \
  --name "Position export" \
  --command-argv '["node","scripts/export-position.mjs"]' \
  --command-cwd "/srv/app" \
  --command-env "NODE_ENV=production" \
  --command-input '{"mode":"summary"}' \
  --timeout-seconds 120 \
  --no-output-timeout-seconds 30 \
  --output-max-bytes 65536 \
  --webhook "https://example.invalid/openclaw/cron"
```

**Source**: OpenClaw documentation — `cli/cron` (mirror `inbox/openclaw_docs/cli/cron.md`)
**Last Updated**: 2026-06-22
**Status**: Active
