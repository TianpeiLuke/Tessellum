---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - mattermost
keywords:
  - mattermost interactive buttons
  - openclaw inlineButtons capability
  - mattermost buttons callback_data
  - props.attachments mattermost actions
  - hmac-sha256 _token signing
  - openclaw-mattermost-interactions secret
  - mattermost direct api external scripts
  - callbackBaseUrl button reachability
  - mattermost action id alphanumeric
topics:
  - OpenClaw
  - Mattermost Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/mattermost
access_control_group: ["general"]
---

# OpenClaw — Mattermost Interactive Buttons and the Direct-API HMAC Contract

## Overview

This note models the two data contracts the OpenClaw Mattermost channel uses for **interactive buttons**: the in-agent `message` tool path (the `buttons` 2D array and the `inlineButtons` capability) and the **Direct API integration** path for external scripts and webhooks (the raw `props.attachments` payload structure plus the HMAC-SHA256 `_token` signing recipe). It mirrors the `Interactive buttons (message tool)` H2 and its `Direct API integration (external scripts)` H3 of the `channels/mattermost` source page. Channel setup, chat modes, threading, access control, preview streaming, reactions, multi-account, and troubleshooting are documented in the sibling **[oc_channels_mattermost](oc_channels_mattermost.md)** procedure note; this note covers only the button payload and signing contract.

## The `inlineButtons` Capability and the message-tool `buttons` Array

Interactive buttons let OpenClaw send a message with clickable buttons; when a user clicks a button the agent receives the selection and can respond. Normal agent replies can also carry semantic `presentation` payloads: OpenClaw renders value buttons as Mattermost interactive buttons, keeps URL buttons visible in the message text, and downgrades select menus to readable text. Buttons must be enabled by adding `inlineButtons` to the channel capabilities array — this also adds the buttons tool description to the agent system prompt:

```json5
{
  channels: {
    mattermost: {
      capabilities: ["inlineButtons"],
    },
  },
}
```

The agent emits buttons through `message action=send` with a `buttons` parameter. `buttons` is a **2D array** — an array of rows, each row an array of button objects:

```
message action=send channel=mattermost target=channel:<channelId> buttons=[[{"text":"Yes","callback_data":"yes"},{"text":"No","callback_data":"no"}]]
```

Each button object has these fields: `text` (string, required) — the display label; `callback_data` (string, required) — the value sent back on click, used as the action ID; `style` (`"default" | "primary" | "danger"`, optional) — the button style. When a user clicks a button, all buttons are replaced with a confirmation line (e.g., `✓ **Yes** selected by @user`), and the agent receives the selection as an inbound message and responds.

Implementation notes from the source: button callbacks use HMAC-SHA256 verification (automatic, no config needed for the message-tool path); Mattermost strips callback data from its API responses as a security feature, so all buttons are removed on click — partial removal is not possible; and action IDs containing hyphens or underscores are sanitized automatically (a Mattermost routing limitation).

## Button Callback Reachability and `interactions.callbackBaseUrl`

The button callback URL must be reachable from the Mattermost server. `channels.mattermost.capabilities` is the array of capability strings; add `"inlineButtons"` to enable the buttons tool. `channels.mattermost.interactions.callbackBaseUrl` is an optional external base URL for button callbacks (for example `https://gateway.example.com`); use it when Mattermost cannot reach the gateway at its bind host directly. In multi-account setups the same field can be set under `channels.mattermost.accounts.<id>.interactions.callbackBaseUrl`. If `interactions.callbackBaseUrl` is omitted, OpenClaw derives the callback URL from `gateway.customBindHost` + `gateway.port`, then falls back to `http://localhost:<port>`. `localhost` only works when Mattermost and OpenClaw run on the same host/network namespace; if the callback target is private/tailnet/internal, its host/domain must be added to Mattermost `ServiceSettings.AllowedUntrustedInternalConnections`.

## Direct API Integration (External Scripts) — Payload Structure

External scripts and webhooks can post buttons directly via the Mattermost REST API instead of going through the agent's `message` tool. The source recommends using `buildButtonAttachments()` from the plugin when possible; when posting raw JSON, the payload must follow the structure below:

```json5
{
  channel_id: "<channelId>",
  message: "Choose an option:",
  props: {
    attachments: [
      {
        actions: [
          {
            id: "mybutton01", // alphanumeric only - see below
            type: "button", // required, or clicks are silently ignored
            name: "Approve", // display label
            style: "primary", // optional: "default", "primary", "danger"
            integration: {
              url: "https://gateway.example.com/mattermost/interactions/default",
              context: {
                action_id: "mybutton01", // must match button id (for name lookup)
                action: "approve",
                // ... any custom fields ...
                _token: "<hmac>", // see HMAC section below
              },
            },
          },
        ],
      },
    ],
  },
}
```

Six critical routing rules govern this payload (each failure is silent or a non-obvious HTTP error):

1. Attachments go in `props.attachments`, **not** top-level `attachments` (a top-level field is silently ignored).
2. Every action needs `type: "button"` — without it, clicks are swallowed silently.
3. Every action needs an `id` field — Mattermost ignores actions without IDs.
4. Action `id` must be **alphanumeric only** (`[a-zA-Z0-9]`); hyphens and underscores break Mattermost's server-side action routing (returns 404), so strip them before use.
5. `context.action_id` must match the button's `id` so the confirmation message shows the button name (e.g., `Approve`) instead of a raw ID.
6. `context.action_id` is required — the interaction handler returns 400 without it.

The callback `integration.url` targets the gateway's interactions endpoint (e.g., `https://gateway.example.com/mattermost/interactions/default`), where the trailing path segment is the account id (`default` for the default account).

## HMAC-SHA256 `_token` Generation

The gateway verifies button clicks with HMAC-SHA256, so external scripts must generate `_token` values that match the gateway's verification logic. The five-step recipe is:

1. **Derive the secret from the bot token:** `HMAC-SHA256(key="openclaw-mattermost-interactions", data=botToken)`.
2. **Build the context object** with all fields **except** `_token`.
3. **Serialize with sorted keys and no spaces** — the gateway uses `JSON.stringify` with sorted keys, which produces compact output.
4. **Sign the payload:** `HMAC-SHA256(key=secret, data=serializedContext)`.
5. **Add the token:** add the resulting hex digest as `_token` in the context.

The source's Python reference implementation:

```python
import hmac, hashlib, json

secret = hmac.new(
    b"openclaw-mattermost-interactions",
    bot_token.encode(), hashlib.sha256
).hexdigest()

ctx = {"action_id": "mybutton01", "action": "approve"}
payload = json.dumps(ctx, sort_keys=True, separators=(",", ":"))
token = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

context = {**ctx, "_token": token}
```

## Common HMAC Pitfalls

The source enumerates four signing pitfalls that produce silent verification failures: Python's `json.dumps` adds spaces by default (`{"key": "val"}`), so `separators=(",", ":")` is required to match JavaScript's compact output (`{"key":"val"}`); you must always sign **all** context fields (minus `_token`) — the gateway strips `_token` then signs everything remaining, and signing a subset causes silent verification failure; use `sort_keys=True` because the gateway sorts keys before signing and Mattermost may reorder context fields when storing the payload; and the secret must be derived from the bot token (deterministic), not random bytes, so it is identical across the button-creating process and the verifying gateway. The companion `Buttons issues` troubleshooting accordion (documented in the sibling setup note) maps the runtime errors back to these rules: an `invalid _token` log line means an HMAC mismatch (subset signing, unsorted keys, or non-compact JSON), and a `missing _token in context` log line means `_token` was not included when building the integration payload.

**Source**: OpenClaw documentation — `channels/mattermost` (mirror `inbox/openclaw_docs/channels/mattermost.md`), sections "Interactive buttons (message tool)" + "Direct API integration (external scripts)"
**Last Updated**: 2026-06-22
**Status**: Active
