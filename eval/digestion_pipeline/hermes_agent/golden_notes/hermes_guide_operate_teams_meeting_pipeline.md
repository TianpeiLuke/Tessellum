---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - runbook
keywords:
  - teams meeting pipeline operator runbook
  - hermes teams-pipeline cli
  - graph subscription renewal 72 hours
  - maintain-subscriptions cron systemd crontab
  - go-live checklist failure triage
  - incoming_webhook vs graph delivery
topics:
  - Hermes Agent
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/operate-teams-meeting-pipeline
access_control_group: ["general"]
---

# Operate the Teams Meeting Pipeline

## Overview

This is the **operator runbook** for the Hermes Microsoft Teams meeting pipeline — the day-to-day CLI flows, the mandatory subscription-renewal automation, failure triage, the go-live checklist, and the rollout worksheets you fill out before changing the deployment. It assumes the feature is already enabled from the Teams Meetings setup; this page is purely about *operating* it once it is live, not configuring it from scratch. Everything is driven by the `hermes teams-pipeline` CLI subcommand family (validate / token-health / subscriptions / maintain-subscriptions / list / show / run / fetch), backed by a Microsoft Graph webhook receiver at `/msgraph/webhook` and a delivery sink (Teams chat or channel). The single most important operational fact on this page: **Microsoft Graph subscriptions expire in at most 72 hours**, so a scheduled renewal job is not optional — without it the pipeline silently stops producing meeting summaries after three days while *looking* fine.

## Core Operator Commands

The operator surface is one CLI family. Use these in roughly this order when diagnosing or changing the deployment:

- **`hermes teams-pipeline validate`** — validate the config snapshot. Run this first after any config change.
- **`hermes teams-pipeline token-health`** (add `--force-refresh`) — inspect Graph auth state; force a refresh when you suspect stale tokens.
- **`hermes teams-pipeline subscriptions`** — list current Graph subscriptions and their `expirationDateTime`.
- **`hermes teams-pipeline maintain-subscriptions`** (add `--dry-run`) — renew near-expiry subscriptions; the dry-run reports how many are expiring soon without acting.
- **`hermes teams-pipeline list`** / **`list --status failed`** / **`show <job-id>`** — inspect recent stored jobs and drill into one.
- **`hermes teams-pipeline run <job-id>`** — replay a stored job.
- **`hermes teams-pipeline fetch --meeting-id <id>`** / **`fetch --join-web-url "<url>"`** — dry-run a meeting-artifact fetch by meeting ID or join URL.

## Automating Subscription Renewal (REQUIRED for production)

Microsoft Graph subscriptions expire within 72 hours, so if nothing renews them, meeting notifications silently stop after 3 days and the pipeline looks "broken." This is the #1 operational failure mode for any Graph-backed integration. You MUST run `maintain-subscriptions` on a schedule — pick one of three options.

**Option 1 — Hermes cron** (recommended if you already run the Hermes gateway). Hermes ships a built-in cron scheduler; `--no-agent` mode runs a script instead of an LLM, and `--script` must point at a file under `~/.hermes/scripts/`. First create the script, then register a script-only job every 12 hours (6× headroom against the 72h window):

```bash
mkdir -p ~/.hermes/scripts
cat > ~/.hermes/scripts/maintain-teams-subscriptions.sh <<'EOF'
#!/usr/bin/env bash
exec hermes teams-pipeline maintain-subscriptions
EOF
chmod +x ~/.hermes/scripts/maintain-teams-subscriptions.sh

hermes cron create "0 */12 * * *" \
  --name "teams-pipeline-maintain-subscriptions" \
  --no-agent \
  --script maintain-teams-subscriptions.sh \
  --deliver local
```

Then verify registration and inspect the next run with `hermes cron list` and `hermes cron status`.

**Option 2 — systemd timer** (recommended for Linux production). Create a oneshot service and a 12-hour timer:

```ini
# /etc/systemd/system/hermes-teams-pipeline-maintain.service
[Unit]
Description=Hermes Teams pipeline subscription maintenance
After=network-online.target

[Service]
Type=oneshot
User=hermes
EnvironmentFile=/etc/hermes/env
ExecStart=/usr/local/bin/hermes teams-pipeline maintain-subscriptions
```

```ini
# /etc/systemd/system/hermes-teams-pipeline-maintain.timer
[Unit]
Description=Run Hermes Teams pipeline subscription maintenance every 12 hours

[Timer]
OnBootSec=5min
OnUnitActiveSec=12h
Persistent=true

[Install]
WantedBy=timers.target
```

Enable with `sudo systemctl daemon-reload` then `sudo systemctl enable --now hermes-teams-pipeline-maintain.timer` (inspect via `systemctl list-timers …`).

**Option 3 — plain crontab**:

```cron
0 */12 * * * /usr/local/bin/hermes teams-pipeline maintain-subscriptions >> /var/log/hermes/teams-pipeline-maintain.log 2>&1
```

The cron environment must carry the `MSGRAPH_*` credentials — simplest fix is to `source ~/.hermes/.env` at the top of a wrapper script crontab calls.

**Verify renewal is working** after the first scheduled run: `hermes teams-pipeline subscriptions` should show `expirationDateTime` advanced, and `maintain-subscriptions --dry-run` should report "0 expiring soon" most of the time. If a Graph webhook mysteriously "stops working" after ~72 hours, the first thing to check is whether the renewal job actually ran.

## Routine Runbook

**After first setup**, run in order: `validate` → `token-health --force-refresh` → `subscriptions`. Then trigger or wait for a real meeting event and confirm with `hermes teams-pipeline list` and `show <job-id>`.

**Daily/periodic checks**: run `maintain-subscriptions --dry-run`, inspect `list --status failed`, and verify the Teams delivery target is still the correct chat or channel.

**Before changing webhook URLs or delivery targets**: update the public notification URL or Teams target config, run `validate`, renew or recreate affected subscriptions, then confirm new events land in the expected sink.

## Failure Triage

Diagnose by stage:

- **No jobs being created** — check `msgraph_webhook` is enabled; the public notification URL points to `/msgraph/webhook`; the subscription client state matches `MSGRAPH_WEBHOOK_CLIENT_STATE`; subscriptions still exist remotely and are not expired.
- **Jobs stay in retry or fail before summarization** — check transcript permissions/availability, recording permissions/artifact availability, `ffmpeg` availability if recording fallback is enabled, and Graph token health.
- **Summaries produced but not delivered to Teams** — check `platforms.teams.enabled: true`, `delivery_mode`, `incoming_webhook_url` (webhook mode), `chat_id` or `team_id` + `channel_id` (Graph mode), and Teams auth config if Graph posting is used.
- **Duplicate or unexpected replays** — check whether you manually replayed a job with `run`, whether the sink record already exists for that meeting, or whether a resend path was intentionally enabled in local config.

## Go-Live Checklist

Before going live, confirm: Graph credentials present and correct; `msgraph_webhook` enabled and reachable from the public internet; `MSGRAPH_WEBHOOK_CLIENT_STATE` set and matching subscriptions; transcript subscription created; recording subscription created if STT fallback is required; `ffmpeg` installed if recording fallback is enabled; Teams outbound delivery target configured and verified; Notion and Linear sinks configured only if actually needed; `validate` returns an OK snapshot; `token-health --force-refresh` succeeds; **`maintain-subscriptions` is scheduled** (Hermes cron, systemd timer, or crontab — without this, Graph subscriptions silently expire within 72 hours); a real end-to-end meeting event has produced a stored job; and at least one summary has reached the intended delivery sink.

## Delivery-Mode Decision Guide

| Mode | Use when | Tradeoff |
|------|----------|----------|
| `incoming_webhook` | you only need simple posting into Teams | simplest setup, less control |
| `graph` | you need channel or chat posting through Graph | more control, more auth and target config |

## Operator & Change Review Worksheets

Two worksheets gate rollout and change. The **Operator Worksheet** (fill out before rollout) captures: public notification URL; Graph tenant ID; Graph client ID; webhook client state; transcript resource subscription; recording resource subscription; Teams delivery mode; Teams chat ID or team/channel; Notion database ID; Linear team ID; store-path override (if any); and the owner for daily checks. The **Change Review Worksheet** (use before changing the deployment) asks: are we changing the public webhook URL? rotating Graph credentials? changing Teams delivery mode? moving to a new Teams chat or channel? do subscriptions need to be recreated or renewed? do we need a fresh end-to-end verification run? These are kept as reference tables in the source and operationally as pre-change gates, not split into separate notes.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/operate-teams-meeting-pipeline
**Last Updated**: 2026-06-19
**Status**: Active
