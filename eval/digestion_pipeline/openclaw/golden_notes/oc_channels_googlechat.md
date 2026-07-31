---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - googlechat
keywords:
  - openclaw google chat channel
  - google chat webhook setup
  - googlechat service account audience
  - tailscale funnel webhook public url
  - audienceType app-url project-number
  - googlechat 405 method not allowed
  - googlechat dm pairing group mention
  - googlechat botUser typingIndicator
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/googlechat
access_control_group: ["general"]
---

# OpenClaw — Connecting Google Chat (Webhook-Only Channel)

## Overview

This note is the end-to-end procedure for docking a **Google Chat** app to an OpenClaw gateway, mirroring the `channels/googlechat` source page. Google Chat support ships as a **downloadable plugin** that serves DMs and spaces over the **Google Chat API webhooks (HTTP only)** — there is no persistent socket. The procedure covers installing the plugin, the beginner Quick setup (Cloud project + Service Account + JSON key + Chat app config + audience), adding the bot in Google Chat, exposing a public HTTPS webhook URL three ways (Tailscale Funnel, Caddy reverse proxy, Cloudflare Tunnel), how inbound POSTs are authenticated and routed, delivery targets, the `channels.googlechat` config highlights, and the `405 Method Not Allowed` troubleshooting path. Access-control internals (`groupPolicy`, mention gating, pairing) appear here only as configured here; the cross-surface model lives in the sibling group notes.

## Install

Install the Google Chat plugin **before** configuring the channel:

```bash
openclaw plugins install @openclaw/googlechat
```

When running from a git checkout, install the local copy instead:

```bash
openclaw plugins install ./path/to/local/googlechat-plugin
```

## Quick setup (beginner)

1. **Create a Google Cloud project and enable the Google Chat API** at the [Google Chat API Credentials](https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials) page; enable the API if not already enabled.
2. **Create a Service Account** — press **Create Credentials** > **Service Account**, name it (e.g. `openclaw-chat`), leave permissions blank (**Continue**), and leave principals with access blank (**Done**).
3. **Create and download the JSON Key** — click the service account, open the **Keys** tab, click **Add Key** > **Create new key**, select **JSON**, and press **Create**.
4. **Store the JSON file on your gateway host** (e.g. `~/.openclaw/googlechat-service-account.json`).
5. **Create a Google Chat app** in the [Chat Configuration](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat) console: fill in **Application info** (**App name** e.g. `OpenClaw`, **Avatar URL** e.g. `https://openclaw.ai/logo.png`, **Description** e.g. `Personal AI Assistant`); enable **Interactive features**; under **Functionality** check **Join spaces and group conversations**; under **Connection settings** select **HTTP endpoint URL**; under **Triggers** select **Use a common HTTP endpoint URL for all triggers** and set it to your gateway's public URL followed by `/googlechat` (run `openclaw status` to find the public URL); under **Visibility** check **Make this Chat app available to specific people and groups in `<Your Domain>`** and enter your email (e.g. `user@example.com`); click **Save**.
6. **Enable the app status** — refresh the page, find the **App status** section, change it to **Live - available to users**, and **Save** again.
7. **Configure OpenClaw with the service account path + webhook audience** — set env `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`, or config `channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`.
8. **Set the webhook audience type + value** so it matches your Chat app config (see *How it works* below).
9. **Start the gateway.** Google Chat will POST to your webhook path.

## Add to Google Chat

Once the gateway is running and your email is on the visibility list: go to [Google Chat](https://chat.google.com/), click the **+** icon next to **Direct Messages**, and in the search bar type the **App name** you configured. The bot will **not** appear in the "Marketplace" browse list because it is a private app — you must search for it by name. Select the bot from the results, click **Add** or **Chat** to start a 1:1 conversation, and send "Hello" to trigger the assistant.

## Public URL (webhook-only)

Google Chat webhooks require a **public HTTPS endpoint**. For security, **only expose the `/googlechat` path** to the internet and keep the OpenClaw dashboard and other sensitive endpoints on your private network. Three options are documented.

### Option A: Tailscale Funnel (recommended)

Use Tailscale **Serve** for the private dashboard and **Funnel** for the public webhook path — this keeps `/` private while exposing only `/googlechat`. First check what address the gateway is bound to (note the IP, e.g. `127.0.0.1`, `0.0.0.0`, or a Tailscale IP like `100.x.x.x`), expose the dashboard to the tailnet only on port `8443`, then expose only the webhook path publicly:

```bash
# 1. Check the gateway's bound address
ss -tlnp | grep 18789

# 2. Expose the dashboard to the tailnet only (port 8443)
tailscale serve --bg --https 8443 http://127.0.0.1:18789        # localhost-bound
tailscale serve --bg --https 8443 http://100.106.161.80:18789   # Tailscale-IP-bound

# 3. Expose only the webhook path publicly
tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat        # localhost-bound
tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat   # Tailscale-IP-bound

# 5. Verify
tailscale serve status
tailscale funnel status
```

If prompted (step 4), visit the authorization URL shown in the output to enable Funnel for this node in your tailnet policy. The public webhook URL is then `https://<node-name>.<tailnet>.ts.net/googlechat` and the private dashboard stays tailnet-only at `https://<node-name>.<tailnet>.ts.net:8443/`. Use the public URL (without `:8443`) in the Google Chat app config. This configuration persists across reboots; to remove it later run `tailscale funnel reset` and `tailscale serve reset`.

### Option B: Reverse proxy (Caddy)

With a reverse proxy like Caddy, only proxy the specific path so requests to `your-domain.com/` are ignored or returned as 404 while `your-domain.com/googlechat` is safely routed to OpenClaw:

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

### Option C: Cloudflare Tunnel

Configure the tunnel's ingress rules to route only the webhook path: **Path** `/googlechat` → `http://localhost:18789/googlechat`, with a **Default Rule** of HTTP 404 (Not Found).

## How it works

1. Google Chat sends webhook **POSTs** to the gateway; each request includes an `Authorization: Bearer <token>` header. OpenClaw **verifies bearer auth before reading/parsing full webhook bodies** when the header is present. Google Workspace Add-on requests carrying `authorizationEventObject.systemIdToken` in the body are supported via a stricter pre-auth body budget.
2. OpenClaw verifies the token against the configured `audienceType` + `audience`: `audienceType: "app-url"` → audience is your HTTPS webhook URL; `audienceType: "project-number"` → audience is the Cloud project number.
3. Messages are routed by space — DMs use session key `agent:<agentId>:googlechat:direct:<spaceId>` and spaces use session key `agent:<agentId>:googlechat:group:<spaceId>`.
4. **DM access is pairing by default.** Unknown senders receive a pairing code; approve with `openclaw pairing approve googlechat <code>`.
5. **Group spaces require @-mention by default.** Use `botUser` if mention detection needs the app's user name.
6. When an exec or plugin approval request starts from Google Chat and a stable `users/<id>` approver is configured, OpenClaw posts a **native Google Chat approval card** in the originating space or thread; the card buttons use opaque callback tokens, and the manual `/approve <id> <decision>` prompt is shown only when native approval delivery is unavailable.

## Targets

Use these identifiers for delivery and allowlists: direct messages use `users/<userId>` (recommended); raw email `name@example.com` is mutable and only used for direct allowlist matching when `channels.googlechat.dangerouslyAllowNameMatching: true`; the deprecated `users/<email>` form is treated as a user id, not an email allowlist; spaces use `spaces/<spaceId>`.

## Config highlights

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      // or serviceAccountRef: { source: "file", provider: "filemain", id: "/channels/googlechat/serviceAccount" }
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; helps mention detection
      allowBots: false,
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          enabled: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Short answers only.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Key notes from the source: service account credentials can also be passed inline with `serviceAccount` (a JSON string); `serviceAccountRef` is supported (env/file SecretRef), including per-account refs under `channels.googlechat.accounts.<id>.serviceAccountRef`. The default `webhookPath` is `/googlechat` if unset. `dangerouslyAllowNameMatching` re-enables mutable email principal matching for allowlists (break-glass compatibility mode). Reactions are available via the `reactions` tool and `channels action` when `actions.reactions` is enabled. Native approval cards use Google Chat `cardsV2` button clicks (not reaction events); approvers come from `dm.allowFrom` or `defaultTo` and must be stable numeric `users/<id>` values. Message actions expose `send` for text and `upload-file` for explicit attachment sends — `upload-file` accepts `media` / `filePath` / `path` plus optional `message`, `filename`, and thread targeting. `typingIndicator` supports `message` (default), `none`, and `reaction` (reaction requires user OAuth). Attachments are downloaded through the Chat API and stored in the media pipeline (size capped by `mediaMaxMb`). Bot-authored Google Chat messages are ignored by default; if you set `allowBots: true`, accepted bot-authored messages use shared bot loop protection — configure `channels.defaults.botLoopProtection`, then override with `channels.googlechat.botLoopProtection` or `channels.googlechat.groups.<space>.botLoopProtection` when a space needs a different budget.

## Troubleshooting

### 405 Method Not Allowed

If Google Cloud Logs Explorer shows `status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed`, the webhook handler is not registered. Common causes and fixes:

```bash
# 1. Channel not configured — channels.googlechat section missing
openclaw config get channels.googlechat
# "Config path not found" → add the configuration (see Config highlights)

# 2. Plugin not enabled
openclaw plugins list | grep googlechat
# "disabled" → add plugins.entries.googlechat.enabled: true

# 3. Gateway not restarted after config change
openclaw gateway restart

# Verify the channel is running
openclaw channels status
# Should show: Google Chat default: enabled, configured, ...
```

### Other issues

Check `openclaw channels status --probe` for auth errors or missing audience config. If no messages arrive, confirm the Chat app's webhook URL and event subscriptions. If mention gating blocks replies, set `botUser` to the app's user resource name and verify `requireMention`. Use `openclaw logs --follow` while sending a test message to see if requests reach the gateway.

**Source**: OpenClaw documentation — `channels/googlechat` (mirror `inbox/openclaw_docs/channels/googlechat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
