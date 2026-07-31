---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - matrix push rules
  - quiet streaming finalized preview
  - com.openclaw.finalized_preview
  - matrix override push rule
  - recipient access token pushers
  - event_property_is push condition
  - synapse tuwunel quiet previews
  - openclaw matrix notifications
topics:
  - OpenClaw
  - Matrix Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/matrix-push-rules
access_control_group: ["general"]
---

# OpenClaw — Matrix Push Rules for Quiet Finalized-Preview Notifications

## Overview

This note is the operator procedure for installing per-recipient Matrix push rules so a self-hosted homeserver notifies only on the finished reply, not on every in-place preview edit, when `channels.matrix.streaming` is set to `"quiet"`. It mirrors the `channels/matrix-push-rules` source page: when quiet streaming is enabled, OpenClaw edits a single preview event in place and marks the finalized edit with a custom content flag, and Matrix clients notify on that final edit only if a per-user push rule matches the flag. The page is for operators who self-host Matrix and want to install that rule for each recipient account; if you only want stock Matrix notification behavior, use `streaming: "partial"` or leave streaming off.

## Prerequisites

The rule is keyed to two distinct accounts and the recipient's credentials, per the source `## Prerequisites`: the **recipient user** is the person who should receive the notification, and the **bot user** is the OpenClaw Matrix account that sends the reply. You use the recipient user's access token for the API calls below, and you match the `sender` condition in the push rule against the bot user's full MXID. The recipient account must already have working pushers — quiet preview rules only work when normal Matrix push delivery is healthy.

## Steps

The source `## Steps` block is a five-step `<Steps>` recipe. Step 1 — **configure quiet previews** — sets the streaming mode in OpenClaw config:

```json5
{
  channels: {
    matrix: {
      streaming: "quiet",
    },
  },
}
```

Step 2 — **get the recipient's access token** — reuse an existing client session token where possible; to mint a fresh one, POST a password login for the recipient (replace the redacted password):

```bash
curl -sS -X POST \
  "https://matrix.example.org/_matrix/client/v3/login" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "m.login.password",
    "identifier": { "type": "m.id.user", "user": "@alice:example.org" },
    "password": "REDACTED"
  }'
```

Step 3 — **verify pushers exist** — query the recipient's pushers with their bearer token; if no pushers come back, fix normal Matrix push delivery for this account before continuing:

```bash
curl -sS \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  "https://matrix.example.org/_matrix/client/v3/pushers"
```

Step 4 — **install the override push rule** — OpenClaw marks finalized text-only preview edits with `content["com.openclaw.finalized_preview"] = true`, so install a `global/override` rule that matches that marker plus the bot MXID as sender:

```bash
curl -sS -X PUT \
  "https://matrix.example.org/_matrix/client/v3/pushrules/global/override/openclaw-finalized-preview-botname" \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "conditions": [
      { "kind": "event_match", "key": "type", "pattern": "m.room.message" },
      {
        "kind": "event_property_is",
        "key": "content.m\\.relates_to.rel_type",
        "value": "m.replace"
      },
      {
        "kind": "event_property_is",
        "key": "content.com\\.openclaw\\.finalized_preview",
        "value": true
      },
      { "kind": "event_match", "key": "sender", "pattern": "@bot:example.org" }
    ],
    "actions": [
      "notify",
      { "set_tweak": "sound", "value": "default" },
      { "set_tweak": "highlight", "value": false }
    ]
  }'
```

Before running, replace the placeholders: `https://matrix.example.org` with your homeserver base URL; `$USER_ACCESS_TOKEN` with the recipient user's access token; `openclaw-finalized-preview-botname` with a rule ID unique per bot per recipient (pattern: `openclaw-finalized-preview-<botname>`); and `@bot:example.org` with your OpenClaw bot MXID, **not** the recipient's. The rule's three conditions match an `m.room.message`, the `m.replace` relation (`content.m\.relates_to.rel_type`), and the `content.com\.openclaw\.finalized_preview` flag set to `true`, combined with the bot `sender` match.

Step 5 — **verify** — read the rule back with the recipient's token, then test a streamed reply; in quiet mode the room shows a quiet draft preview and notifies once the block or turn finishes:

```bash
curl -sS \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  "https://matrix.example.org/_matrix/client/v3/pushrules/global/override/openclaw-finalized-preview-botname"
```

To remove the rule later, `DELETE` the same rule URL with the recipient's token.

## Multi-bot notes

Push rules are keyed by `ruleId`: re-running `PUT` against the same ID updates a single rule. For multiple OpenClaw bots notifying the same recipient, create one rule per bot with a distinct sender match. New user-defined `override` rules are inserted ahead of default suppress rules, so no extra ordering parameter is needed. The rule only affects text-only preview edits that can be finalized in place; media fallbacks and stale-preview fallbacks use normal Matrix delivery.

## Homeserver notes

The source `## Homeserver notes` is an `<AccordionGroup>` with one accordion per homeserver. For **Synapse**, no special `homeserver.yaml` change is required: if normal Matrix notifications already reach this user, the recipient token plus the `pushrules` call above is the main setup step. If you run Synapse behind a reverse proxy or workers, make sure `/_matrix/client/.../pushrules/` reaches Synapse correctly, and ensure the main process or `synapse.app.pusher` / configured pusher workers are healthy. The rule uses the `event_property_is` push-rule condition (MSC3758, push rule v1.10), which was added to Synapse in 2023; older Synapse releases accept the `PUT pushrules/...` call but silently never match the condition — upgrade Synapse if no notification arrives on a finalized preview edit.

For **Tuwunel**, the flow is the same as Synapse and no Tuwunel-specific config is needed for the finalized preview marker. If notifications disappear while the user is active on another device, check whether `suppress_push_when_active` is enabled; Tuwunel added this option in 1.4.2 (September 2025) and it can intentionally suppress pushes to other devices while one device is active.

**Source**: OpenClaw documentation — `channels/matrix-push-rules` (mirror `inbox/openclaw_docs/channels/matrix-push-rules.md`)
**Last Updated**: 2026-06-22
**Status**: Active
