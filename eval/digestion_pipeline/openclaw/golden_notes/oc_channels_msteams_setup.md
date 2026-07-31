---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - msteams
keywords:
  - openclaw microsoft teams setup
  - msteams bundled plugin install
  - microsoft teams.cli quick setup
  - devtunnel ngrok tailscale funnel
  - teams app create client_id secret
  - channels.msteams config webhook
  - MSTEAMS_APP_ID env vars
  - teams app doctor
topics:
  - OpenClaw
  - Microsoft Teams Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/msteams
access_control_group: ["general"]
---

# OpenClaw — Connecting Microsoft Teams (Bundled Plugin, Quick Setup, Config, Env Vars)

## Overview

This note is the procedure for connecting Microsoft Teams to an OpenClaw gateway: installing the bundled `@openclaw/msteams` plugin, running the `@microsoft/teams.cli` quick-setup flow (login → tunnel → app create → configure → install → verify), writing the `channels.msteams` config, exposing the local bot over a dev tunnel, sending a test message, and the full `MSTEAMS_*` environment-variable list plus the setup-relevant `channels.msteams` configuration keys. It mirrors the `channels/msteams` source page sections Bundled plugin, Quick setup, Goals, Config writes, Local development (tunneling), Testing the Bot, Environment variables, and Configuration. Production federated authentication (certificate / managed identity) is in [oc_channels_msteams_federated_auth.md](oc_channels_msteams_federated_auth.md); access control, manifest/RSC/Graph, files, and messaging behavior are in [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md).

## Goals

Per the source Goals section, the connector lets you talk to OpenClaw via Teams DMs, group chats, or channels; keeps routing deterministic so replies always go back to the channel they arrived on; and defaults to safe channel behavior (mentions required unless configured otherwise). The setup below gets the bot registered and listening; the day-to-day messaging/access behavior is covered in the sibling messaging note.

## Bundled plugin

Microsoft Teams ships as a bundled plugin in current OpenClaw releases, so no separate install is required in the normal packaged build. If you are on an older build or a custom install that excludes bundled Teams, install the npm package directly, then use the bare package to follow the current official release tag (pin an exact version only when you need a reproducible install):

```bash
openclaw plugins install @openclaw/msteams
```

A local checkout (when running from a git repo) can be installed with `openclaw plugins install ./path/to/local/msteams-plugin`.

## Quick setup

The `@microsoft/teams.cli` handles bot registration, manifest creation, and credential generation in a single command. The Teams CLI is currently in preview — commands and flags may change between releases.

**1. Install and log in** — `teams status` verifies you are logged in and shows your tenant info:

```bash
npm install -g @microsoft/teams.cli@preview
teams login
teams status   # verify you're logged in and see your tenant info
```

**2. Start a tunnel** — Teams can't reach `localhost`, so the bot must be exposed over an HTTPS endpoint. Install and authenticate the devtunnel CLI, then create a persistent tunnel for port 3978. `--allow-anonymous` is required because Teams cannot authenticate with devtunnels; each incoming bot request is still validated by the Teams SDK automatically. Alternatives are `ngrok http 3978` or `tailscale funnel 3978`, but these may change URLs each session.

```bash
# One-time setup (persistent URL across sessions):
devtunnel create my-openclaw-bot --allow-anonymous
devtunnel port create my-openclaw-bot -p 3978 --protocol auto

# Each dev session:
devtunnel host my-openclaw-bot
# Your endpoint: https://<tunnel-id>.devtunnels.ms/api/messages
```

**3. Create the app** — `teams app create --name "OpenClaw" --endpoint "https://<your-tunnel-url>/api/messages"` performs the whole registration in one shot: it creates an Entra ID (Azure AD) application, generates a client secret, builds and uploads a Teams app manifest (with icons), and registers the bot (Teams-managed by default — no Azure subscription needed). The output shows `CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID`, and a **Teams App ID** — note these for the next steps; it also offers to install the app in Teams directly.

**4. Configure OpenClaw** using the credentials from the output:

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<CLIENT_ID>",
      appPassword: "<CLIENT_SECRET>",
      tenantId: "<TENANT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

Or use environment variables directly: `MSTEAMS_APP_ID`, `MSTEAMS_APP_PASSWORD`, `MSTEAMS_TENANT_ID`.

**5. Install the app in Teams** — `teams app create` prompts you to install the app; select "Install in Teams". If you skipped it, get the link later with `teams app get <teamsAppId> --install-link`.

**6. Verify everything works** — `teams app doctor <teamsAppId>` runs diagnostics across bot registration, AAD app config, manifest validity, and SSO setup.

For production deployments, consider using federated authentication (certificate or managed identity) instead of client secrets — see [oc_channels_msteams_federated_auth.md](oc_channels_msteams_federated_auth.md). Group chats are blocked by default (`channels.msteams.groupPolicy: "allowlist"`); to allow group replies set `channels.msteams.groupAllowFrom`, or use `groupPolicy: "open"` to allow any member (mention-gated) — the access model is detailed in [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md).

A manual Azure-Portal path exists when the Teams CLI can't be used (create an Azure Bot for App ID + secret + tenant ID, build a Teams app package referencing the bot with RSC permissions, upload/install it, configure `msteams` in `~/.openclaw/openclaw.json`, and start the gateway). The gateway listens for Bot Framework webhook traffic on `/api/messages` by default; the Teams channel starts automatically when the plugin is available and `msteams` config exists with credentials. The manifest/RSC details for the manual path live in [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md).

## Config writes

By default, Microsoft Teams is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`). Disable it with:

```json5
{
  channels: { msteams: { configWrites: false } },
}
```

## Local development (tunneling)

Teams can't reach `localhost`. Use a persistent dev tunnel so your URL stays the same across sessions. Alternatives are `ngrok http 3978` or `tailscale funnel 3978` (URLs may change each session). If your tunnel URL changes, update the endpoint with `teams app update <teamsAppId> --endpoint "https://<new-url>/api/messages"`.

```bash
# One-time setup:
devtunnel create my-openclaw-bot --allow-anonymous
devtunnel port create my-openclaw-bot -p 3978 --protocol auto

# Each dev session:
devtunnel host my-openclaw-bot
```

## Testing the Bot

Run `teams app doctor <teamsAppId>` to check bot registration, AAD app, manifest, and SSO configuration in one pass. To send a test message: (1) install the Teams app using the install link from `teams app get <id> --install-link`, (2) find the bot in Teams and send a DM, (3) check the gateway logs for incoming activity.

## Environment variables

All config keys can be set via environment variables instead. The setup-relevant variables are:

- `MSTEAMS_APP_ID`
- `MSTEAMS_APP_PASSWORD`
- `MSTEAMS_TENANT_ID`
- `MSTEAMS_AUTH_TYPE` (optional: `"secret"` or `"federated"`)
- `MSTEAMS_CERTIFICATE_PATH` (federated + certificate)
- `MSTEAMS_CERTIFICATE_THUMBPRINT` (optional, not required for auth)
- `MSTEAMS_USE_MANAGED_IDENTITY` (federated + managed identity)
- `MSTEAMS_MANAGED_IDENTITY_CLIENT_ID` (user-assigned MI only)

The `secret`-mode defaults (`MSTEAMS_APP_ID`/`MSTEAMS_APP_PASSWORD`/`MSTEAMS_TENANT_ID`) cover the quick-setup flow above; the federated `MSTEAMS_AUTH_TYPE`/`MSTEAMS_CERTIFICATE_PATH`/`MSTEAMS_USE_MANAGED_IDENTITY`/`MSTEAMS_MANAGED_IDENTITY_CLIENT_ID` family is described in [oc_channels_msteams_federated_auth.md](oc_channels_msteams_federated_auth.md).

## Configuration

Key settings for getting the channel running (shared channel patterns live at `/gateway/configuration`). The connection/transport keys are:

- `channels.msteams.enabled`: enable/disable the channel.
- `channels.msteams.appId`, `channels.msteams.appPassword`, `channels.msteams.tenantId`: bot credentials.
- `channels.msteams.webhook.port` (default `3978`).
- `channels.msteams.webhook.path` (default `/api/messages`).
- `channels.msteams.configWrites`: allow/deny `/config set|unset` config writes (default allowed; requires `commands.config: true`).
- `channels.msteams.textChunkLimit`: outbound text chunk size.
- `channels.msteams.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.

Access-control keys (`dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `requireMention`, `teams.<teamId>.*`, `replyStyle`, `mediaAllowHosts`, `actions.memberInfo`, `sharePointSiteId`) are documented in [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md); the authentication keys (`authType`, `certificatePath`, `certificateThumbprint`, `useManagedIdentity`, `managedIdentityClientId`, `cloud`, `serviceUrl`) are documented in [oc_channels_msteams_federated_auth.md](oc_channels_msteams_federated_auth.md). The default DM policy is `dmPolicy: "pairing"` — unknown senders are ignored until approved via the flow in [oc_channels_pairing.md](oc_channels_pairing.md).

**Source**: OpenClaw documentation — `channels/msteams` (mirror `inbox/openclaw_docs/channels/msteams.md`)
**Last Updated**: 2026-06-22
**Status**: Active
