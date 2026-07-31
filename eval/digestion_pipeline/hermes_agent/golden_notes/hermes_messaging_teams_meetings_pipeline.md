---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - teams
keywords:
  - teams meeting pipeline
  - microsoft graph webhook
  - meeting summary delivery
  - graph subscriptions
  - transcript fallback stt
  - msgraph_webhook listener
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams-meetings
access_control_group: ["general"]
---

# Hermes Microsoft Teams Meeting Summary Pipeline

## Overview

The Teams meeting pipeline is the Hermes feature that ingests Microsoft Graph meeting events, fetches a meeting transcript first (falling back to the recording plus speech-to-text when no usable transcript exists), and delivers a structured summary to downstream sinks — Notion, Linear, and Microsoft Teams. It is a setup-and-enablement procedure layered on top of the underlying Teams bot/credential setup (see [hermes_messaging_teams_bot](hermes_messaging_teams_bot.md)): you add Microsoft Graph app-only credentials, enable the `msgraph_webhook` gateway listener, configure delivery + pipeline behavior under the existing `teams` platform entry, start the gateway, and create Graph subscriptions. Operator actions stay in the CLI under the `teams-pipeline` subcommand, which is registered by the `teams_pipeline` plugin (`hermes plugins enable teams_pipeline`, or `plugins.enabled: [teams_pipeline]` in `config.yaml`). This page focuses on setup/enablement; day-2 operations, go-live checks, and the operator worksheet live in the dedicated "Operate the Teams Meeting Pipeline" guide.

## What This Feature Does

The pipeline:

1. receives Microsoft Graph webhook events
2. resolves the meeting and prefers transcript artifacts first
3. falls back to recording download plus STT when no usable transcript is available
4. stores durable job state and sink records locally
5. can write summaries to Notion, Linear, and Microsoft Teams

Operator actions stay in the CLI (the `teams-pipeline` subcommand is registered by the `teams_pipeline` plugin):

```bash
hermes teams-pipeline validate
hermes teams-pipeline list
hermes teams-pipeline maintain-subscriptions
```

## Prerequisites

Before enabling the meetings pipeline, make sure you have:

- a working Hermes install
- the existing Microsoft Teams bot setup if you want Teams outbound delivery
- Microsoft Graph application credentials with the permissions required for the meeting resources you plan to subscribe to
- a public HTTPS URL that Microsoft Graph can call for webhook delivery
- `ffmpeg` installed if you want recording-plus-STT fallback

## Step 1: Add Microsoft Graph Credentials

Add Graph app-only credentials to `~/.hermes/.env` — `MSGRAPH_TENANT_ID`, `MSGRAPH_CLIENT_ID`, and `MSGRAPH_CLIENT_SECRET`. These credentials are used by the Graph client foundation, subscription maintenance commands, meeting resolution and artifact fetches, and Graph-based Teams outbound delivery when you do not provide a dedicated Teams access token.

## Step 2: Enable the Graph Webhook Listener

The webhook listener is a gateway platform named `msgraph_webhook`. At minimum, enable it and set a client state value:

```bash
MSGRAPH_WEBHOOK_ENABLED=true
MSGRAPH_WEBHOOK_HOST=127.0.0.1
MSGRAPH_WEBHOOK_PORT=8646
MSGRAPH_WEBHOOK_CLIENT_STATE=<random-shared-secret>
MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=communications/onlineMeetings
```

The listener exposes `/msgraph/webhook` for Graph notifications and `/health` for a simple health check. You route your public HTTPS endpoint to that listener — e.g., for public domain `https://ops.example.com` the Graph notification URL is typically `https://ops.example.com/msgraph/webhook`.

## Step 3: Configure Teams Delivery and Pipeline Behavior

The meeting pipeline reads its runtime config from the existing `teams` platform entry. Pipeline-specific knobs live under `teams.extra.meeting_pipeline`; Teams outbound delivery stays on the normal Teams platform config surface. Example `~/.hermes/config.yaml`:

```yaml
platforms:
  msgraph_webhook:
    enabled: true
    extra:
      host: 127.0.0.1
      port: 8646
      client_state: "replace-me"
      accepted_resources:
        - "communications/onlineMeetings"

  teams:
    enabled: true
    extra:
      client_id: "your-teams-client-id"
      client_secret: "your-teams-client-secret"
      tenant_id: "your-teams-tenant-id"

      # outbound summary delivery
      delivery_mode: "graph" # or incoming_webhook
      team_id: "team-id"
      channel_id: "channel-id"
      # incoming_webhook_url: "https://..."

      meeting_pipeline:
        transcript_min_chars: 80
        transcript_required: false
        transcription_fallback: true
        ffmpeg_extract_audio: true
        notion:
          enabled: false
        linear:
          enabled: false
```

If you bind the listener to a non-loopback host such as `0.0.0.0`, you must also set `allowed_source_cidrs` to Microsoft's webhook egress ranges. Loopback binds (`127.0.0.1` / `::1`) are the intended dev-tunnel and local reverse-proxy setup.

## Teams Delivery Modes

The pipeline supports two Teams summary-delivery modes inside the existing Teams plugin.

- **`incoming_webhook`** — a simple webhook post into Teams without channel-message creation through Graph. Required config sets `delivery_mode: "incoming_webhook"` plus `incoming_webhook_url: "https://..."`.
- **`graph`** — post the summary through Microsoft Graph into a Teams chat or channel (see the Step 3 example). Supported targets: `chat_id`; `team_id` + `channel_id`; or `team_id` + `home_channel` fallback for the existing Teams platform.

## Step 4: Start the Gateway

Start Hermes normally after updating config (or start the gateway the same way you already do for a Docker deployment), then check the listener:

```bash
hermes gateway run
curl http://localhost:8646/health
```

## Step 5: Create Graph Subscriptions

Use the plugin CLI to create and inspect subscriptions:

```bash
hermes teams-pipeline subscribe \
  --resource communications/onlineMeetings/getAllTranscripts \
  --notification-url https://ops.example.com/msgraph/webhook \
  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"

hermes teams-pipeline subscribe \
  --resource communications/onlineMeetings/getAllRecordings \
  --notification-url https://ops.example.com/msgraph/webhook \
  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"
```

**Graph subscriptions expire in 72 hours.** Microsoft Graph caps webhook subscriptions at 72 hours and will not auto-renew them. You MUST schedule `hermes teams-pipeline maintain-subscriptions` before going live, or notifications will silently stop three days after any manual subscription creation. The operator runbook offers three renewal options — Hermes cron, systemd timer, or plain crontab.

## Validation

Run the built-in validation snapshot, with two useful companion checks:

```bash
hermes teams-pipeline validate
hermes teams-pipeline token-health
hermes teams-pipeline subscriptions
```

## Troubleshooting

| Problem | What to check |
|---------|---------------|
| Graph webhook validation fails | Confirm the public URL is correct and reachable, and that Graph is calling the exact `/msgraph/webhook` path |
| Jobs do not appear in `hermes teams-pipeline list` | Confirm `msgraph_webhook` is enabled and that subscriptions point at the right notification URL |
| Transcript-first never succeeds | Check Graph permissions for transcript resources and whether the transcript artifact exists for that meeting |
| Recording fallback fails | Confirm `ffmpeg` is installed and the Graph app can access recording artifacts |
| Teams summary delivery fails | Re-check `delivery_mode`, target IDs, and Teams auth config |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/teams-meetings.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams-meetings
**Last Updated**: 2026-06-19
**Status**: Active
