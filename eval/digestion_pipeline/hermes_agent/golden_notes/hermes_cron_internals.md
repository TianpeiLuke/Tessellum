---
tags:
  - resource
  - documentation
  - hermes_agent
  - cron
  - scheduling
keywords:
  - hermes cron internals
  - scheduled task execution
  - jobs.json storage
  - scheduler tick cycle
  - skill-backed cron jobs
  - chronos managed cron
  - recursion guard
topics:
  - Hermes Agent
  - Cron Scheduling
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals
access_control_group: ["general"]
---

# Hermes Agent — Cron Internals

## Overview

The cron subsystem is Hermes Agent's **scheduled task executor** — the runtime that stores, schedules, edits, pauses, skill-loads, and delivers cron jobs. It spans the spectrum from a simple one-shot relative delay to recurring cron-expression jobs that inject skills and deliver results across 20+ messaging platforms. At its core, the model-facing surface is a single `cronjob` action tool; persistence is an atomic `jobs.json` file; the runtime is a 60-second tick cycle that runs each due job in a **completely fresh, isolated `AIAgent` session**. In gateway mode the *trigger* (deciding *when* a job fires) is a pluggable `CronScheduler` provider — the in-process ticker by default, or the managed **Chronos** provider for scale-to-zero hosting — while job *execution + delivery* always stays in the shared `scheduler.run_job()` / `_deliver_result()` path. Cross-process file locking, a recursion guard (the `cronjob` toolset is disabled inside cron runs), and provider recovery (fallback chain + credential-pool rotation) make scheduled execution safe and resilient. This note documents how the subsystem behaves; the `repo_hermes_agent_cron` repo and `snippet_hermes_agent_cron_*` corpus document how it is implemented.

## Key Files

| File | Purpose |
|------|---------|
| `cron/jobs.py` | Job model, storage, atomic read/write to `jobs.json` |
| `cron/scheduler.py` | Scheduler loop — due-job detection, execution, repeat tracking |
| `tools/cronjob_tools.py` | Model-facing `cronjob` tool registration and handler |
| `gateway/run.py` | Gateway integration — cron ticking in the long-running loop |
| `hermes_cli/cron.py` | CLI `hermes cron` subcommands |

## Scheduling Model

Four schedule formats are supported:

| Format | Example | Behavior |
|--------|---------|----------|
| **Relative delay** | `30m`, `2h`, `1d` | One-shot, fires after the specified duration |
| **Interval** | `every 2h`, `every 30m` | Recurring, fires at regular intervals |
| **Cron expression** | `0 9 * * *` | Standard 5-field cron syntax (minute, hour, day, month, weekday) |
| **ISO timestamp** | `2025-01-15T09:00:00` | One-shot, fires at the exact time |

The model-facing surface is a single `cronjob` tool with action-style operations: `create`, `list`, `update`, `pause`, `resume`, `run`, `remove`.

## Job Storage

Jobs are stored in `~/.hermes/cron/jobs.json` with atomic write semantics (write to temp file, then rename). Each job record contains:

```json
{
  "id": "a1b2c3d4e5f6",
  "name": "Daily briefing",
  "prompt": "Summarize today's AI news and funding rounds",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "display": "0 9 * * *"
  },
  "skills": ["ai-funding-daily-report"],
  "deliver": "telegram:-1001234567890",
  "repeat": {
    "times": null,
    "completed": 42
  },
  "state": "scheduled",
  "enabled": true,
  "next_run_at": "2025-01-16T09:00:00Z",
  "last_run_at": "2025-01-15T09:00:00Z",
  "last_status": "ok",
  "created_at": "2025-01-01T00:00:00Z",
  "model": null,
  "provider": null,
  "script": null
}
```

### Job Lifecycle States

Each job carries one of four states: `scheduled` (active, will fire at next scheduled time), `paused` (suspended until resumed), `completed` (repeat count exhausted, or a one-shot that has fired), and `running` (a transient state during execution).

### Backward Compatibility

Older jobs may have a single `skill` field instead of the `skills` array. The scheduler normalizes this at load time — a single `skill` is promoted to `skills: [skill]`.

## Scheduler Runtime

### Tick Cycle

The scheduler runs on a periodic tick (default: every 60 seconds):

```text
tick()
  1. Acquire scheduler lock (prevents overlapping ticks)
  2. Load all jobs from jobs.json
  3. Filter to due jobs (next_run <= now AND state == "scheduled")
  4. For each due job:
     a. Set state to "running"
     b. Create fresh AIAgent session (no conversation history)
     c. Load attached skills in order (injected as user messages)
     d. Run the job prompt through the agent
     e. Deliver the response to the configured target
     f. Update run_count, compute next_run
     g. If repeat count exhausted → state = "completed"
     h. Otherwise → state = "scheduled"
  5. Write updated jobs back to jobs.json
  6. Release scheduler lock
```

### Gateway Integration

In gateway mode, the cron **trigger** (the part deciding *when* a due job fires — "Axis B") is selected through a pluggable `CronScheduler` provider. The gateway calls `resolve_cron_scheduler()` (`cron/scheduler_provider.py`) and runs the resolved provider's `start()` in a dedicated background thread, alongside a separate gateway-housekeeping thread. The active provider is chosen by the `cron.provider` config key:

- **empty (default)** → the built-in `InProcessCronScheduler`, which runs the historical in-process loop calling `scheduler.tick()` every 60 seconds — byte-identical to the pre-provider behavior.
- **a named provider** (e.g. `chronos`, a managed-cron provider for scale-to-zero deployments) → discovered from `plugins/cron/<name>/` or `$HERMES_HOME/plugins/<name>/`.

If a named provider is missing, fails to load, or reports `is_available() == False`, the resolver falls back to the built-in with a warning — **cron is never left without a trigger.** The built-in provider lives in core (`cron/scheduler_provider.py`), not in `plugins/`, so the fallback can't be accidentally removed. What "firing" *means* (job execution + delivery) is unchanged and shared by all providers — it stays in `scheduler.run_job()` / `scheduler._deliver_result()`. A provider only controls the trigger, never execution. In CLI mode, cron jobs only fire when `hermes cron` commands are run or during active CLI sessions.

### Managed cron (Chronos) for scale-to-zero

Hosted gateways can run the **Chronos** provider (`cron.provider: chronos`) instead of the built-in ticker. Chronos lets an idle gateway **scale to zero** and still fire cron jobs: rather than a 60-second in-process loop (which would keep the process awake), it asks Nous infrastructure to arm exactly **one managed one-shot per job at that job's real next-fire time**. At fire time Nous calls the gateway back over an authenticated webhook (`POST /api/cron/fire`); the gateway runs the job through the same `run_one_job` path as the built-in, then re-arms the next one-shot. Between fires the process can be fully stopped — it wakes only on a genuine fire, never on a periodic timer. The flow (the managed scheduler is provided by Nous; the agent holds no scheduler credentials):

```
create/update a cron job
  → Chronos asks Nous to arm a one-shot at the job's next_run_at
      (authenticated with the agent's existing Nous token)
  → at fire time Nous calls the gateway: POST {callback_url}/api/cron/fire
      (authenticated with a short-lived, purpose-scoped Nous-minted JWT)
  → the gateway verifies the token, claims the job (store compare-and-set so
    multi-replica deployments fire at-most-once), runs it, and re-arms the next
    one-shot
```

The non-secret config keys (set by Nous at provision time on hosted agents) are `cron.provider` (`chronos` to activate, empty = built-in ticker), `cron.chronos.portal_url` (Nous base URL — arming + fire-token issuer), `cron.chronos.callback_url` (the gateway's own public base URL for inbound fires), `cron.chronos.expected_audience` (this agent's fire-token audience), and `cron.chronos.nas_jwks_url` (key set for verifying the inbound fire token). If Chronos is misconfigured or the agent isn't logged into Nous, `resolve_cron_scheduler()` falls back to the built-in ticker (logged warning) — cron never loses its trigger. Recurring jobs re-arm after each fire; `repeat`-N jobs stop cleanly when the count is exhausted (no orphaned one-shot). The full agent↔Nous wire contract lives in `docs/chronos-managed-cron-contract.md`.

### Fresh Session Isolation

Each cron job runs in a completely fresh agent session: no conversation history from previous runs; no memory of previous cron executions (unless persisted to memory/files); the prompt must be self-contained — cron jobs cannot ask clarifying questions; and the `cronjob` toolset is disabled (recursion guard).

## Skill-Backed Jobs

A cron job can attach one or more skills via the `skills` field. At execution time: (1) skills are loaded in the specified order, (2) each skill's SKILL.md content is injected as context, (3) the job's prompt is appended as the task instruction, and (4) the agent processes the combined skill context + prompt. This enables reusable, tested workflows without pasting full instructions into cron prompts — for example, "Create a daily funding report → attach the `ai-funding-daily-report` skill."

### Script-Backed Jobs

Jobs can also attach a Python script via the `script` field. The script runs *before* each agent turn, and its stdout is injected into the prompt as context, enabling data-collection and change-detection patterns (fetch competitor release notes, diff against the last run, print a summary to stdout — the agent then analyzes and reports). The script timeout defaults to 120 seconds. `_get_script_timeout()` resolves the limit through a layered chain: a module-level override `_SCRIPT_TIMEOUT` (for tests/monkeypatching, used only when it differs from the default), then the environment variable `HERMES_CRON_SCRIPT_TIMEOUT`, then config `cron.script_timeout_seconds` in `config.yaml` (read via `load_config()`), and finally the 120-second default.

### Provider Recovery

`run_job()` passes the user's configured fallback providers and credential pool into the `AIAgent` instance:

- **Fallback providers** — reads `fallback_providers` (list) or `fallback_model` (legacy dict) from `config.yaml`, matching the gateway's `_load_fallback_model()` pattern. Passed as `fallback_model=` to `AIAgent.__init__`, which normalizes both formats into a fallback chain.
- **Credential pool** — loads via `load_pool(provider)` from `agent.credential_pool` using the resolved runtime provider name. Only passed when the pool has credentials (`pool.has_credentials()`). Enables same-provider key rotation on 429/rate-limit errors.

This mirrors the gateway's behavior — without it, cron agents would fail on rate limits without attempting recovery.

## Delivery Model

Cron job results can be delivered to any supported platform. `origin` delivers back to the chat where the job was created, `local` saves to `~/.hermes/cron/output/`, and the remaining targets address messaging platforms by name (optionally with an address suffix): `telegram` / `telegram:<chat_id>`, `discord` / `discord:#channel`, `slack`, `whatsapp`, `signal`, `matrix`, `mattermost`, `email`, `sms`, `homeassistant`, `dingtalk`, `feishu`, `wecom`, `weixin`, `bluebubbles` (iMessage), and `qqbot` (QQ via Official API v2). For Telegram topics, use `telegram:<chat_id>:<thread_id>` (e.g. `telegram:-1001234567890:17585`).

### Response Wrapping

By default (`cron.wrap_response: true`), cron deliveries are wrapped with a header identifying the cron job name and task, and a footer noting that the agent cannot see the delivered message in conversation. The `[SILENT]` prefix in a cron response suppresses delivery entirely — useful for jobs that only need to write to files or perform side effects.

### Session Isolation

Cron deliveries are **NOT** mirrored into gateway session conversation history. They exist only in the cron job's own session. This prevents message-alternation violations in the target chat's conversation.

## Recursion Guard

Cron-run sessions have the `cronjob` toolset disabled. This prevents a scheduled job from creating new cron jobs, recursive scheduling that could explode token usage, and accidental mutation of the job schedule from within a job.

## Locking

The scheduler uses cross-process file-based locking (`fcntl.flock` on Unix, `msvcrt.locking` on Windows) to prevent overlapping ticks from executing the same due-job batch twice — even between the gateway's in-process ticker and a standalone `hermes cron` / manual `tick()` call. If the lock cannot be acquired, `tick()` returns 0 immediately.

## CLI Interface

The `hermes cron` CLI provides direct job management:

```bash
hermes cron list                    # Show all jobs
hermes cron create                  # Interactive job creation (alias: add)
hermes cron edit <job_id>           # Edit job configuration
hermes cron pause <job_id>          # Pause a running job
hermes cron resume <job_id>         # Resume a paused job
hermes cron run <job_id>            # Trigger immediate execution
hermes cron remove <job_id>         # Delete a job
```

**Source**: `inbox/hermes_agent_docs/developer-guide/cron-internals.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals
**Last Updated**: 2026-06-19
**Status**: Active
