---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - qa
keywords:
  - qa telegram discord slack whatsapp reference
  - openclaw_qa env vars
  - slack qa driver sut app manifest
  - shared live transport cli flags
  - convex credential pool kinds
  - qa scenario catalog
topics:
  - OpenClaw
  - QA Automation
language: markdown
date of note: 2026-06-23
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/qa-e2e-automation
access_control_group: ["general"]
---

# OpenClaw — Telegram/Discord/Slack/WhatsApp QA Reference & Convex Pool

## Overview

This note is the per-channel reference half of the `concepts/qa-e2e-automation` page (split from the operator-flow / observability note [oc_concepts_qa_e2e_automation_live_transports](oc_concepts_qa_e2e_automation_live_transports.md), which holds the QA Lab flow + coverage matrix). It documents the shared live-transport CLI flags, the per-channel env vars / scenario catalogs / output artifacts for Telegram, Discord, Slack, and WhatsApp, the full Slack workspace app-setup walkthrough, and the shared Convex credential pool. Matrix has its own page because of its scenario count and Docker homeserver provisioning.

## Shared CLI Flags

The Telegram/Discord/Slack/WhatsApp lanes register through `extensions/qa-lab/src/live-transports/shared/live-transport-cli.ts` and accept the same flags:

| Flag | Default | Description |
| --- | --- | --- |
| `--scenario <id>` | - | Run only this scenario. Repeatable. |
| `--output-dir <path>` | `<repo>/.artifacts/qa-e2e/<transport>-<timestamp>` | Where reports/summaries/evidence/artifacts + output log are written (relative paths resolve against `--repo-root`). |
| `--repo-root <path>` | `process.cwd()` | Repository root when invoking from a neutral cwd. |
| `--sut-account <id>` | `sut` | Temporary account id inside the QA gateway config. |
| `--provider-mode <mode>` | `live-frontier` | `mock-openai` or `live-frontier` (legacy `live-openai` still works). |
| `--model <ref>` / `--alt-model <ref>` | provider default | Primary/alternate model refs. |
| `--fast` | off | Provider fast mode where supported. |
| `--credential-source <env\|convex>` | `env` | See Convex credential pool below. |
| `--credential-role <maintainer\|ci>` | `ci` in CI, `maintainer` otherwise | Role used when `--credential-source convex`. |

Each lane exits non-zero on any failed scenario; `--allow-failures` writes artifacts without a failing exit code.

## Telegram QA

`pnpm openclaw qa telegram` targets one real private Telegram group with two distinct bots (driver + SUT). The SUT bot must have a Telegram username; bot-to-bot observation works best when both bots have **Bot-to-Bot Communication Mode** enabled in `@BotFather`. Required env when `--credential-source env`: `OPENCLAW_QA_TELEGRAM_GROUP_ID` (numeric chat id string), `OPENCLAW_QA_TELEGRAM_DRIVER_BOT_TOKEN`, `OPENCLAW_QA_TELEGRAM_SUT_BOT_TOKEN`. Scenarios (`.../telegram/telegram-live.runtime.ts`) include `telegram-canary`, `telegram-mention-gating`, `telegram-mentioned-message-reply`, `telegram-help-command`, `telegram-commands-command`, `telegram-tools-compact-command`, `telegram-whoami-command`, `telegram-status-command`, `telegram-repeated-command-authorization`, `telegram-other-bot-command-gating`, `telegram-context-command`, `telegram-current-session-status-tool`, `telegram-reply-chain-exact-marker`, `telegram-stream-final-single-message`, `telegram-long-final-reuses-preview`, and `telegram-long-final-three-chunks`. The implicit default set covers canary, mention gating, native command replies, command addressing, and bot-to-bot group replies; `mock-openai` defaults add deterministic reply-chain and final-message streaming checks. `telegram-current-session-status-tool` is opt-in (stable only when threaded directly after canary). Output: `telegram-qa-report.md` + `qa-evidence.json` (profile/coverage/provider/channel/artifacts/result/RTT). Package runs use the same credential contract; `OPENCLAW_QA_CREDENTIAL_SOURCE=convex pnpm test:docker:npm-telegram-live` leases a `kind: "telegram"` credential, exports leased env, heartbeats the lease, and releases it on shutdown (defaults: 20 RTT checks of `telegram-mentioned-message-reply`, 30s timeout, Convex role `maintainer` outside CI; override via `OPENCLAW_NPM_TELEGRAM_RTT_SAMPLES` / `_RTT_TIMEOUT_MS` / `_RTT_MAX_FAILURES`).

## Discord QA

`pnpm openclaw qa discord` targets one real private Discord guild channel with two bots: a harness-controlled driver and a SUT started by the child OpenClaw gateway through the bundled Discord plugin. It verifies channel mention handling, native `/help` command registration, and opt-in Mantis evidence scenarios. Required env (`--credential-source env`): `OPENCLAW_QA_DISCORD_GUILD_ID`, `OPENCLAW_QA_DISCORD_CHANNEL_ID`, `OPENCLAW_QA_DISCORD_DRIVER_BOT_TOKEN`, `OPENCLAW_QA_DISCORD_SUT_BOT_TOKEN`, and `OPENCLAW_QA_DISCORD_SUT_APPLICATION_ID` (must match the SUT bot user id or the lane fails fast). Optional: `OPENCLAW_QA_DISCORD_CAPTURE_CONTENT=1` keeps message bodies; `OPENCLAW_QA_DISCORD_VOICE_CHANNEL_ID` selects the voice/stage channel for `discord-voice-autojoin`. Scenarios (`.../discord/discord-live.runtime.ts`): `discord-canary`, `discord-mention-gating`, `discord-native-help-command-registration`, `discord-voice-autojoin` (opt-in; runs alone, enables `channels.discord.voice.autoJoin`, verifies the SUT bot's voice state), and `discord-status-reactions-tool-only` (opt-in Mantis; switches the SUT to always-on tool-only guild replies with `messages.statusReactions.enabled=true`, captures a REST reaction timeline plus HTML/PNG visual artifacts). Output: `discord-qa-report.md`, `qa-evidence.json`, `discord-qa-observed-messages.json` (bodies redacted unless capture-content set), and `discord-qa-reaction-timelines.json` + `discord-status-reactions-tool-only-timeline.png` when the status-reaction scenario runs.

## Slack QA

`pnpm openclaw qa slack` targets one real private Slack channel with two distinct bots (harness driver + gateway-started SUT). Required env (`--credential-source env`): `OPENCLAW_QA_SLACK_CHANNEL_ID`, `OPENCLAW_QA_SLACK_DRIVER_BOT_TOKEN`, `OPENCLAW_QA_SLACK_SUT_BOT_TOKEN`, `OPENCLAW_QA_SLACK_SUT_APP_TOKEN`. Optional: `OPENCLAW_QA_SLACK_CAPTURE_CONTENT=1`; `OPENCLAW_QA_SLACK_APPROVAL_CHECKPOINT_DIR` enables visual approval checkpoints (writes `<scenario>.pending.json` / `.resolved.json`, waits for matching `.ack.json`); `OPENCLAW_QA_SLACK_APPROVAL_CHECKPOINT_TIMEOUT_MS` overrides the ack timeout (default `120000`). Scenarios (`.../slack/slack-live.runtime.ts`): `slack-canary`, `slack-mention-gating`, `slack-allowlist-block`, `slack-top-level-reply-shape`, `slack-restart-resume`, `slack-thread-follow-up`, `slack-thread-isolation`, plus opt-in `slack-approval-exec-native` and `slack-approval-plugin-native`. Output: `slack-qa-report.md`, `qa-evidence.json`, `slack-qa-observed-messages.json` (redacted unless capture-content set), and `approval-checkpoints/` when the Mantis checkpoint dir is set.

### Setting up the Slack workspace

The lane needs two distinct Slack apps in one workspace plus a channel both bots are members of: `channelId` (`Cxxxxxxxxxx` of a dedicated channel — the lane posts every run), `driverBotToken` (`xoxb-...` of the **Driver** app), `sutBotToken` (`xoxb-...` of the **SUT** app, a separate app so its bot user id is distinct), and `sutAppToken` (`xapp-...` of the SUT app with `connections:write`, used by Socket Mode). Prefer a QA-dedicated workspace over production. The SUT manifest below narrows the bundled Slack plugin's production install to the permissions/events the live QA suite covers (reaction scopes/events omitted — not yet covered).

**1. Create the Driver app** — at `api.slack.com/apps` → Create New App → From a manifest → pick the QA workspace → paste, then Install to Workspace:

```json
{
  "display_information": {
    "name": "OpenClaw QA Driver",
    "description": "Test driver bot for OpenClaw QA Slack live lane"
  },
  "features": { "bot_user": { "display_name": "OpenClaw QA Driver", "always_online": true } },
  "oauth_config": { "scopes": { "bot": ["chat:write", "channels:history", "groups:history", "users:read"] } },
  "settings": { "socket_mode_enabled": false }
}
```

Copy the Bot User OAuth Token (`xoxb-...`) → `driverBotToken`. The driver only posts messages and identifies itself; no events, no Socket Mode.

**2. Create the SUT app** — repeat Create New App → From a manifest in the same workspace:

```json
{
  "display_information": {
    "name": "OpenClaw QA SUT",
    "description": "OpenClaw QA SUT connector for OpenClaw"
  },
  "features": {
    "bot_user": { "display_name": "OpenClaw QA SUT", "always_online": true },
    "app_home": { "home_tab_enabled": true, "messages_tab_enabled": true, "messages_tab_read_only_enabled": false }
  },
  "oauth_config": { "scopes": { "bot": [
    "app_mentions:read", "assistant:write", "channels:history", "channels:read", "chat:write",
    "commands", "emoji:read", "files:read", "files:write", "groups:history", "groups:read",
    "im:history", "im:read", "im:write", "mpim:history", "mpim:read", "mpim:write",
    "pins:read", "pins:write", "usergroups:read", "users:read" ] } },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": { "bot_events": [
      "app_home_opened", "app_mention", "channel_rename", "member_joined_channel",
      "member_left_channel", "message.channels", "message.groups", "message.im",
      "message.mpim", "pin_added", "pin_removed" ] }
  }
}
```

Then on its settings page: Install to Workspace → copy Bot User OAuth Token → `sutBotToken`; Basic Information → App-Level Tokens → Generate Token and Scopes → add `connections:write` → copy the `xapp-...` value → `sutAppToken`. Verify the two bots have distinct user ids via `auth.test` on each token (reusing one app for both fails mention-gating immediately).

**3. Create the channel** — make a channel (e.g. `#openclaw-qa`) and `/invite @OpenClaw QA Driver` + `/invite @OpenClaw QA SUT`; copy the `Cxxxxxxxxxx` id from channel info → `channelId`. A public channel works; both apps have `groups:history` so private-channel history reads still succeed.

**4. Register the credentials** — use env vars for single-machine debugging (set the four `OPENCLAW_QA_SLACK_*` and pass `--credential-source env`), or seed the Convex pool. For the pool, write the four fields to JSON:

```json
{ "channelId": "Cxxxxxxxxxx", "driverBotToken": "xoxb-...", "sutBotToken": "xoxb-...", "sutAppToken": "xapp-..." }
```

With `OPENCLAW_QA_CONVEX_SITE_URL` and `OPENCLAW_QA_CONVEX_SECRET_MAINTAINER` exported: `pnpm openclaw qa credentials add --kind slack --payload-file slack-creds.json --note "QA Slack pool seed"`, then `pnpm openclaw qa credentials list --kind slack --status all --json` (expect `count: 1`, `status: "active"`, no `lease`).

**5. Verify end to end** — `pnpm openclaw qa slack --credential-source convex --credential-role maintainer --output-dir .artifacts/qa-e2e/slack-local`. A green run completes in well under 30s and `slack-qa-report.md` shows `slack-canary` and `slack-mention-gating` at `pass`. A ~90s hang ending in `Convex credential pool exhausted for kind "slack"` means the pool is empty or every row is leased (`qa credentials list --kind slack --status all --json` tells which).

## WhatsApp QA

`pnpm openclaw qa whatsapp` targets two dedicated WhatsApp Web accounts (harness driver + gateway-started SUT). Required env (`--credential-source env`): `OPENCLAW_QA_WHATSAPP_DRIVER_PHONE_E164`, `OPENCLAW_QA_WHATSAPP_SUT_PHONE_E164`, `OPENCLAW_QA_WHATSAPP_DRIVER_AUTH_ARCHIVE_BASE64`, `OPENCLAW_QA_WHATSAPP_SUT_AUTH_ARCHIVE_BASE64`. Optional: `OPENCLAW_QA_WHATSAPP_GROUP_JID` enables group scenarios; `OPENCLAW_QA_WHATSAPP_CAPTURE_CONTENT=1` keeps bodies. The catalog (`.../whatsapp/whatsapp-live.runtime.ts`) currently contains **35 scenarios** spanning baseline/group gating (`whatsapp-canary`, `whatsapp-pairing-block`, `whatsapp-mention-gating`, `whatsapp-top-level-reply-shape`, `whatsapp-restart-resume`, `whatsapp-group-allowlist-block`), native commands, reply/final-output behavior, inbound media (image/audio/document/location/contact/sticker), outbound Gateway/message-action coverage, access-control coverage, native approvals, and status reactions. The `live-frontier` default lane stays small at 8 scenarios for fast smoke; the `mock-openai` default runs 29 deterministic scenarios through the real WhatsApp transport while mocking only model output; approval and heavier blocking checks remain explicit by id. QA Lab imports the driver through the `@openclaw/whatsapp/api.js` package surface (not private runtime files); message content is redacted by default; outbound poll/upload coverage runs through deterministic gateway `poll` / `message.action` calls. Output: `whatsapp-qa-report.md`, `qa-evidence.json`, `whatsapp-qa-observed-messages.json` (redacted unless capture-content set).

## Convex Credential Pool

The four lanes can lease credentials from a shared Convex pool instead of reading env vars — pass `--credential-source convex` (or set `OPENCLAW_QA_CREDENTIAL_SOURCE=convex`); QA Lab acquires an exclusive lease, heartbeats it for the run, and releases it on shutdown. Pool kinds are `"telegram"`, `"discord"`, `"slack"`, `"whatsapp"`. Payload shapes the broker validates on `admin/add`:

- **Telegram** (`kind: "telegram"`): `{ groupId, driverToken, sutToken }` — `groupId` a numeric chat-id string.
- **Telegram real user** (`kind: "telegram-user"`): `{ groupId, sutToken, testerUserId, testerUsername, telegramApiId, telegramApiHash, tdlibDatabaseEncryptionKey, tdlibArchiveBase64, tdlibArchiveSha256, desktopTdataArchiveBase64, desktopTdataArchiveSha256 }` — Mantis Telegram Desktop proof only; generic QA Lab lanes must not acquire this kind.
- **Discord** (`kind: "discord"`): `{ guildId, channelId, driverBotToken, sutBotToken, sutApplicationId }`.
- **WhatsApp** (`kind: "whatsapp"`): `{ driverPhoneE164, sutPhoneE164, driverAuthArchiveBase64, sutAuthArchiveBase64, groupJid? }` — phone numbers distinct E.164 strings.
- **Slack**: shape checks currently live in the Slack QA runner rather than the broker; use `{ channelId, driverBotToken, sutBotToken, sutAppToken }`.

The Mantis Telegram Desktop proof workflow holds one exclusive `telegram-user` lease for both the TDLib CLI driver and Telegram Desktop witness, releasing it after publishing proof. Operational env vars and the Convex broker endpoint contract live in Testing → Shared Telegram credentials via Convex (the section name predates the multi-channel pool; lease semantics are shared across kinds).

**Source**: OpenClaw documentation — `concepts/qa-e2e-automation` (per-channel reference + Convex pool half; mirror `inbox/openclaw_docs/concepts/qa-e2e-automation.md`)
**Last Updated**: 2026-06-23
**Status**: Active
