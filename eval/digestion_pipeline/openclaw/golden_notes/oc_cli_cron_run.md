---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - cron
keywords:
  - openclaw cron run
  - cron model precedence
  - isolated cron model
  - live model switch retries
  - cron structured denials
  - silent token suppression
  - cron retention sessionRetention
  - cron runLog keepLines
  - doctor --fix migrate cron
  - cron list get show runs
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

# OpenClaw — Running and Administering `openclaw cron` Jobs

## Overview

This note documents the run-time and administration half of `openclaw cron`: per-job model selection and the isolated-cron model-precedence order, fast mode, live model-switch retries, run-output handling (stale-acknowledgement suppression, silent-token suppression, structured denials), retention/pruning config, legacy-job migration via `openclaw doctor --fix`, and the `list` / `get` / `show` / `run` / `runs` admin commands plus agent/session/delivery retargeting. It mirrors the `## Models`, `## Run output and denials`, `## Retention`, `## Migrating older jobs`, and `## Common admin commands` sections of the `cli/cron` source page. The job-authoring, session-key, delivery, and scheduling half (create/add, one-shot vs recurring, manual-run scheduling) lives in the sibling [oc_cli_cron_jobs](oc_cli_cron_jobs.md) note.

## Per-Job Model Selection

`cron add|edit --model <ref>` selects an allowed model for the job. `cron edit <job-id> --clear-model` removes the per-job model override so the job follows normal cron model-selection precedence — a stored cron-session override if present, otherwise the agent/default model. `--clear-model` cannot be combined with `--model`.

If the model is not allowed or cannot be resolved, cron fails the run with an explicit validation error instead of falling back to the job's agent or default model selection.

Cron `--model` is a **job primary**, not a chat-session `/model` override. That means:

- Configured model fallbacks still apply when the selected job model fails.
- Per-job payload `fallbacks` replaces the configured fallback list when present.
- An empty per-job fallback list (`fallbacks: []` in the job payload/API) makes the cron run strict.
- When a job has `--model` but no fallback list is configured, OpenClaw passes an explicit empty fallback override so the agent primary is not appended as a hidden retry target.
- Local-provider preflight checks walk configured fallbacks before marking a cron run `skipped`.

`openclaw doctor` reports jobs that already have `payload.model` set, including provider namespace counts and mismatches against `agents.defaults.model`. Use that check when auth, provider, or billing behavior looks different between live chat and scheduled jobs.

### Isolated cron model precedence

Isolated cron resolves the active model in this order:

1. Gmail-hook override.
2. Per-job `--model`.
3. Stored cron-session model override (when the user selected one).
4. Agent or default model selection.

### Fast mode

Isolated cron fast mode follows the resolved live model selection. Model config `params.fastMode` applies by default, but a stored session `fastMode` override still wins over config.

### Live model switch retries

If an isolated run throws `LiveSessionModelSwitchError`, cron persists the switched provider and model (and switched auth profile override when present) for the active run before retrying. The outer retry loop is bounded to two switch retries after the initial attempt, then aborts instead of looping forever.

## Run Output and Denials

### Stale acknowledgement suppression

Isolated cron turns suppress stale acknowledgement-only replies. If the first result is just an interim status update and no descendant subagent run is responsible for the eventual answer, cron re-prompts once for the real result before delivery.

### Silent token suppression

If an isolated cron run returns only the silent token (`NO_REPLY` or `no_reply`), cron suppresses both direct outbound delivery and the fallback queued summary path, so nothing is posted back to chat.

### Structured denials

Isolated cron runs use structured execution-denial metadata from the embedded run as the authoritative denial signal. They also honor node-host `UNAVAILABLE` wrappers when the nested structured error message starts with `SYSTEM_RUN_DENIED` or `INVALID_REQUEST`.

Cron does not classify final-output prose or approval-looking refusal phrases as denials unless the embedded run also provides structured denial metadata, so ordinary assistant text is not treated as a blocked command. `cron list` and run history surface the denial reason instead of reporting a blocked command as `ok`.

## Retention

Retention and pruning are controlled in config:

- `cron.sessionRetention` (default `24h`) prunes completed isolated run sessions.
- `cron.runLog.keepLines` prunes retained SQLite run-history rows per job. `cron.runLog.maxBytes` remains accepted for compatibility with older file-backed run logs.

## Migrating Older Jobs

If you have cron jobs from before the current delivery and store format, run `openclaw doctor --fix`. Doctor normalizes legacy cron fields (`jobId`, `schedule.cron`, top-level delivery fields including legacy `threadId`, payload `provider` delivery aliases) and migrates `notify: true` webhook fallback jobs from `cron.webhook` to explicit webhook delivery. Jobs that already announce to a chat keep that delivery and get a completion webhook destination. When `cron.webhook` is unset, the inert top-level `notify` marker is removed for jobs with no migration target (the existing delivery is preserved unchanged), so `doctor --fix` no longer keeps re-warning about them.

## Common Admin Commands

Manual run and inspection:

```bash
openclaw cron list
openclaw cron list --agent ops
openclaw cron get <job-id>
openclaw cron show <job-id>
openclaw cron run <job-id>
openclaw cron run <job-id> --due
openclaw cron run <job-id> --wait --wait-timeout 10m
openclaw cron run <job-id> --wait --wait-timeout 10m --poll-interval 2s
openclaw cron runs --id <job-id> --limit 50
openclaw cron runs --id <job-id> --run-id <run-id>
```

`openclaw cron list` shows all matching jobs by default. Pass `--agent <id>` to show only jobs whose effective normalized agent id matches; jobs without a stored agent id count as the configured default agent.

`openclaw cron get <job-id>` returns the stored job JSON directly. Use `cron show <job-id>` when you want the human-readable view with delivery-route preview.

`cron list --json` and `cron show <job-id> --json` include a top-level `status` field on each job, computed from `enabled`, `state.runningAtMs`, and `state.lastRunStatus`. Values: `disabled`, `running`, `ok`, `error`, `skipped`, or `idle`. This mirrors the human-readable status column so external tooling can read job state without re-deriving it.

`cron runs` entries include delivery diagnostics with the intended cron target, the resolved target, message-tool sends, fallback use, and delivered state.

Agent and session retargeting:

```bash
openclaw cron edit <job-id> --agent ops
openclaw cron edit <job-id> --clear-agent
openclaw cron edit <job-id> --session current
openclaw cron edit <job-id> --session "session:daily-brief"
```

`openclaw cron add` warns when `--agent` is omitted on agent-turn jobs and falls back to the default agent (`main`). Pass `--agent <id>` at create time to pin a specific agent.

Delivery tweaks:

```bash
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
openclaw cron edit <job-id> --webhook "https://example.invalid/openclaw/cron"
openclaw cron edit <job-id> --best-effort-deliver
openclaw cron edit <job-id> --no-best-effort-deliver
openclaw cron edit <job-id> --no-deliver
```

**Source**: OpenClaw documentation — `cli/cron` (mirror `inbox/openclaw_docs/cli/cron.md`)
**Last Updated**: 2026-06-22
**Status**: Active
