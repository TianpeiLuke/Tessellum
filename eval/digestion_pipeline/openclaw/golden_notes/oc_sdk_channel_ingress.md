---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw channel ingress api
  - resolveChannelMessageIngress
  - defineStableChannelIngressIdentity
  - channel ingress access control
  - authMode event modes
  - access groups fail closed
  - route descriptors mention activation
  - ingress redaction raw sender values
topics:
  - OpenClaw
  - Channel Ingress SDK
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-channel-ingress
access_control_group: ["general"]
---

# OpenClaw — Channel Ingress SDK (Inbound Access-Control Boundary)

## Overview

This note documents the **experimental channel ingress SDK** — the access-control boundary a messaging channel plugin uses to authorize an inbound event before the turn kernel processes it — mirroring the `plugins/sdk-channel-ingress` source page. A channel plugin imports `openclaw/plugin-sdk/channel-ingress-runtime` for receive paths; the older `openclaw/plugin-sdk/channel-ingress` subpath stays exported as a **deprecated compatibility facade** for third-party plugins. The governing split is: **plugins own platform facts and side effects**, while **core owns generic policy** — DM/group allowlists, pairing-store DM entries, route gates, command gates, event auth, mention activation, redacted diagnostics, and admission. This note covers the procedure end-to-end: calling the runtime resolver `resolveChannelMessageIngress` with a stable identity, consuming the ordered gate result projections, declaring access groups, picking an `authMode`, supplying route descriptors and mention activation, and obeying the input-only redaction rule, plus the verification commands.

## Runtime Resolver

A receive path defines a **stable identity projection** with `defineStableChannelIngressIdentity` and then calls `resolveChannelMessageIngress` once per inbound event. The identity declares the platform `key`, a `normalize` callback for the platform user id, and a `sensitivity` (e.g. `"pii"`) so raw values are treated as redactable. The resolver receives the channel id, account id, identity, the `subject` (an opaque `stableId`), the `conversation` kind (`group` or `direct`) and id, the `event` (kind + `authMode` + `mayPair`), the `policy` (DM/group policy + `groupAllowFromFallbackToAllowFrom`), the raw `allowFrom` / `groupAllowFrom` allowlists, `accessGroups`, an optional `route` descriptor, a `readStoreAllowFrom` store callback, and an optional `command` gate (`{ allowTextCommands, hasControlCommand }`):

```ts
import {
  defineStableChannelIngressIdentity,
  resolveChannelMessageIngress,
} from "openclaw/plugin-sdk/channel-ingress-runtime";

const identity = defineStableChannelIngressIdentity({
  key: "platform-user-id",
  normalize: normalizePlatformUserId,
  sensitivity: "pii",
});

const result = await resolveChannelMessageIngress({
  channelId: "my-channel",
  accountId,
  identity,
  subject: { stableId: platformUserId },
  conversation: { kind: isGroup ? "group" : "direct", id: conversationId },
  event: { kind: "message", authMode: "inbound", mayPair: !isGroup },
  policy: {
    dmPolicy: config.dmPolicy,
    groupPolicy: config.groupPolicy,
    groupAllowFromFallbackToAllowFrom: true,
  },
  allowFrom: config.allowFrom,
  groupAllowFrom: config.groupAllowFrom,
  accessGroups: cfg.accessGroups,
  route,
  readStoreAllowFrom,
  command: hasControlCommand ? { allowTextCommands: true, hasControlCommand } : undefined,
});
```

**Do not precompute effective allowlists, command owners, or command groups.** The resolver derives them itself from the raw allowlists, store callbacks, route descriptors, access groups, policy, and conversation kind. The plugin's job is to supply raw platform facts, not resolved policy.

## Result

Bundled plugins should consume the **modern projections directly** off the resolver result rather than rebuilding older shapes:

- `ingress` — ordered gate decision and admission.
- `senderAccess` — sender/conversation authorization only.
- `routeAccess` — route and route-sender projection.
- `commandAccess` — command authorization; **false when no command gate ran**.
- `activationAccess` — mention/activation result.

Event authorization is not emitted as a separate projection: it remains available on the ordered `ingress.graph` and the decisive `ingress.reasonCode`. Deprecated third-party SDK helpers may rebuild older shapes internally, but **new bundled receive paths should not translate modern results back into local DTOs**.

## Access Groups

`accessGroup:<name>` entries **stay redacted**. Core resolves static `message.senders` groups itself and calls `resolveAccessGroupMembership` only for the **dynamic groups that require a platform lookup**. Missing, unsupported, and failed groups **fail closed** (denied by default rather than admitted).

## Event Modes

The `event.authMode` selects which gates apply to the inbound event:

| `authMode`       | Meaning                                          |
| ---------------- | ------------------------------------------------ |
| `inbound`        | normal inbound sender gates                      |
| `command`        | command gates for callbacks or scoped buttons    |
| `origin-subject` | actor must match the original message subject    |
| `route-only`     | route gates only for route-scoped trusted events |
| `none`           | plugin-owned internal events bypass shared auth  |

Use `mayPair: false` for **reactions, buttons, callbacks, and native commands** (these are not first-contact messages that should establish a DM pairing).

## Routes And Activation

For room, topic, guild, thread, or nested route policy, pass a **route descriptor**:

```ts
route: {
  id: "room",
  allowed: roomAllowed,
  enabled: roomEnabled,
  senderPolicy: "replace",
  senderAllowFrom: roomAllowFrom,
  blockReason: "room_sender_not_allowlisted",
}
```

When a plugin has several optional route descriptors, use `channelIngressRoutes(...)`: it filters disabled branches while keeping route facts generic and ordered by each descriptor's `precedence`.

**Mention gating is an activation gate.** A mention miss returns `admission: "skip"` so the turn kernel does not process an observe-only turn. Most channels should leave activation **after** sender and command gates. Public chat surfaces that must quiet non-mentioned traffic before sender-allowlist noise can opt into `activation.order: "before-sender"` when text-command bypass is disabled. Channels with implicit activation — such as replies in bot threads — can pass `activation.allowedImplicitMentionKinds`; the projected `activationAccess.shouldBypassMention` then reports when command or implicit activation bypassed an explicit mention.

## Redaction

**Raw sender values and raw allowlist entries are resolver input only.** They must not appear in resolved state, decisions, diagnostics, snapshots, or compatibility facts. Downstream surfaces must use **opaque subject ids, entry ids, route ids, and diagnostic ids** instead of the raw platform values.

## Verification

Run the channel-access and ingress-runtime tests plus the plugin-SDK API surface check:

```bash
pnpm test src/channels/message-access/message-access.test.ts src/plugin-sdk/channel-ingress-runtime.test.ts
pnpm plugin-sdk:api:check
```

**Source**: OpenClaw documentation — `plugins/sdk-channel-ingress` (mirror `inbox/openclaw_docs/plugins/sdk-channel-ingress.md`)
**Last Updated**: 2026-06-22
**Status**: Active
