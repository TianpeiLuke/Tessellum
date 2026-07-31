---
tags:
  - resource
  - documentation
  - openclaw
  - automation
  - cron
keywords:
  - openclaw webhook triggers
  - hooks wake hooks agent
  - gmail pubsub integration
  - openclaw webhooks gmail setup
  - gog gmail watch
  - cron configuration maxconcurrentruns
  - cron retry backoff
  - openclaw cron troubleshooting
  - cron command ladder
topics:
  - OpenClaw
  - Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/automation/cron-jobs
access_control_group: ["general"]
---

# OpenClaw — Cron Triggers (Webhooks + Gmail PubSub), Configuration, and Troubleshooting

## Overview

This note covers the event-trigger and operations half of the OpenClaw cron page (`automation/cron-jobs`): how external events fire cron-style runs through Gateway HTTP **webhook** endpoints (with authentication), the **Gmail PubSub** integration that turns inbox events into agent runs (wizard / gateway-auto-start / manual setup, plus the Gmail model override), the `cron` **Configuration** block, and the **Troubleshooting** command ladder and recipes. The time-scheduling, execution-style, delivery, and CLI side of the same page lives in the sibling note [oc_automation_cron_jobs_scheduling](oc_automation_cron_jobs_scheduling.md); this note assumes that base job model and documents only the trigger + config + troubleshooting surfaces.

## Webhooks

Gateway can expose HTTP webhook endpoints for external triggers. Enable them in config:

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
  },
}
```

There are two built-in endpoints plus a mapped-hook escape hatch:

- `POST /hooks/wake` — enqueue a system event for the **main session**. Body fields: `text` (string, required — the event description) and `mode` (string, default `now`; either `now` or `next-heartbeat`). Example body: `{"text":"New email received","mode":"now"}`.
- `POST /hooks/agent` — run an **isolated agent turn**. Fields: `message` (required), `name`, `agentId`, `wakeMode`, `deliver`, `channel`, `to`, `model`, `fallbacks`, `thinking`, `timeoutSeconds`.
- `POST /hooks/<name>` — **mapped hooks**: custom hook names are resolved via `hooks.mappings` in config; mappings can transform arbitrary payloads into `wake` or `agent` actions with templates or code transforms.

Both built-in calls require the hook token (see Authentication). Example `wake` call: `curl -X POST http://127.0.0.1:18789/hooks/wake -H 'Authorization: Bearer SECRET' -H 'Content-Type: application/json' -d '{"text":"New email received","mode":"now"}'`. Example `agent` call: `curl -X POST http://127.0.0.1:18789/hooks/agent -H 'Authorization: Bearer SECRET' -H 'Content-Type: application/json' -d '{"message":"Summarize inbox","name":"Email","model":"openai/gpt-5.4"}'`.

Security hardening (from the source Warning): keep hook endpoints behind loopback, tailnet, or a trusted reverse proxy; use a dedicated hook token and do not reuse gateway auth tokens; keep `hooks.path` on a dedicated subpath (`/` is rejected); set `hooks.allowedAgentIds` to limit which effective agent a hook can target (including the default agent when `agentId` is omitted); keep `hooks.allowRequestSessionKey=false` unless caller-selected sessions are required, and if it is enabled also set `hooks.allowedSessionKeyPrefixes` to constrain allowed session key shapes; hook payloads are wrapped with safety boundaries by default.

### Authentication

Every request must include the hook token via header — `Authorization: Bearer <token>` (recommended) or `x-openclaw-token: <token>`. Query-string tokens are rejected.

## Gmail PubSub integration

This wires Gmail inbox triggers to OpenClaw via Google PubSub. Prerequisites (from the source Note): the `gcloud` CLI, `gog` (gogcli), OpenClaw hooks enabled, and Tailscale for the public HTTPS endpoint.

### Wizard setup (recommended)

```bash
openclaw webhooks gmail setup --account openclaw@gmail.com
```

This writes `hooks.gmail` config, enables the Gmail preset, and uses Tailscale Funnel for the push endpoint.

### Gateway auto-start

When `hooks.enabled=true` and `hooks.gmail.account` is set, the Gateway starts `gog gmail watch serve` on boot and auto-renews the watch. Set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to opt out.

### Manual one-time setup

Three steps perform the equivalent of the wizard by hand:

1. Select the GCP project that owns the OAuth client used by `gog`: `gcloud auth login`, `gcloud config set project <project-id>`, then `gcloud services enable gmail.googleapis.com pubsub.googleapis.com`.
2. Create the topic and grant Gmail push access: `gcloud pubsub topics create gog-gmail-watch`, then `gcloud pubsub topics add-iam-policy-binding gog-gmail-watch --member=serviceAccount:gmail-api-push@system.gserviceaccount.com --role=roles/pubsub.publisher`.
3. Start the watch: `gog gmail watch start --account openclaw@gmail.com --label INBOX --topic projects/<project-id>/topics/gog-gmail-watch`.

### Gmail model override

A `hooks.gmail` config block selects the model and thinking level used for Gmail-triggered runs:

```json5
{
  hooks: {
    gmail: {
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

This Gmail hook model override is the highest-precedence model selector for an isolated cron run that originated from Gmail (when that override is allowed), sitting above the per-job payload `model`, the user-selected stored cron-session model override, and the agent/default model selection.

## Configuration

The `cron` config block controls the scheduler globally:

```json5
{
  cron: {
    enabled: true,
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 8,
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000],
      retryOn: ["rate_limit", "overloaded", "network", "server_error"],
    },
    webhookToken: "replace-with-dedicated-webhook-token",
    sessionRetention: "24h",
    runLog: { maxBytes: "2mb", keepLines: 2000 },
  },
}
```

Key fields and behaviors:

- `maxConcurrentRuns` (default `8`) limits both scheduled cron dispatch and isolated agent-turn execution. Isolated cron agent turns use the queue's dedicated `cron-nested` execution lane internally, so raising this value lets independent cron LLM runs progress in parallel instead of only starting their outer cron wrappers. The shared non-cron `nested` lane is not widened by this setting.
- `cron.store` is a logical store key and legacy doctor import path. Run `openclaw doctor --fix` to import existing JSON stores into SQLite and archive them; future cron changes should go through the CLI or Gateway API.
- Disable cron entirely with `cron.enabled: false` or the `OPENCLAW_SKIP_CRON=1` env var.
- **Retry behavior** — *One-shot retry*: transient errors (rate limit, overload, network, server error) retry up to 3 times with exponential backoff; permanent errors disable immediately. *Recurring retry*: exponential backoff (30s to 60m) between retries, and the backoff resets after the next successful run.
- **Maintenance** — `cron.sessionRetention` (default `24h`) prunes isolated run-session entries; `cron.runLog.keepLines` limits retained SQLite run-history rows per job, while `maxBytes` is retained for config compatibility with older file-backed run logs.

## Troubleshooting

### Command ladder

A diagnostic command ladder to run when cron behaves unexpectedly:

```bash
openclaw status
openclaw gateway status
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw system heartbeat last
openclaw logs --follow
openclaw doctor
```

Common failure recipes from the source:

- **Cron not firing** — check `cron.enabled` and the `OPENCLAW_SKIP_CRON` env var; confirm the Gateway is running continuously; for `cron` schedules verify timezone (`--tz`) vs the host timezone; `reason: not-due` in run output means a manual run was checked with `openclaw cron run <jobId> --due` and the job was not due yet.
- **Cron fired but no delivery** — delivery mode `none` means no runner fallback send is expected (the agent can still send directly with the `message` tool when a chat route is available); a missing/invalid delivery target (`channel`/`to`) means outbound was skipped; for Matrix, copied or legacy jobs with lowercased `delivery.to` room IDs can fail because Matrix room IDs are case-sensitive (edit to the exact `!room:server` or `room:!room:server` value); channel auth errors (`unauthorized`, `Forbidden`) mean delivery was blocked by credentials; if the isolated run returns only the silent token (`NO_REPLY` / `no_reply`), OpenClaw suppresses direct outbound delivery and also the fallback queued summary path, so nothing is posted back; if the agent should message the user itself, check that the job has a usable route (`channel: "last"` with a previous chat, or an explicit channel/target).
- **Cron or heartbeat appears to prevent `/new`-style rollover** — daily and idle reset freshness is not based on `updatedAt`; cron wakeups, heartbeat runs, exec notifications, and gateway bookkeeping may update the session row for routing/status but do not extend `sessionStartedAt` or `lastInteractionAt`; for legacy rows created before those fields existed, OpenClaw can recover `sessionStartedAt` from the transcript JSONL session header when the file is still available, and legacy idle rows without `lastInteractionAt` use that recovered start time as their idle baseline.
- **Timezone gotchas** — cron without `--tz` uses the gateway host timezone; `at` schedules without timezone are treated as UTC; heartbeat `activeHours` uses configured timezone resolution.

**Source**: OpenClaw documentation — `automation/cron-jobs` (mirror `inbox/openclaw_docs/automation/cron-jobs.md`), Webhooks / Gmail PubSub / Configuration / Troubleshooting sections
**Last Updated**: 2026-06-22
**Status**: Active
