---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw channel plugin
  - channelplugin adapter surface
  - shared message tool core
  - dm policy pairing allowlist
  - approvalcapability native approvals
  - inbound mention policy gating
  - resolveinboundmentiondecision
  - bot loop protection inbound
topics:
  - OpenClaw
  - Channel Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/sdk-channel-plugins
access_control_group: ["general"]
---

# OpenClaw — How Channel Plugins Work (Adapter Model, Approvals, Mention Policy)

## Overview

This note is the conceptual model of an OpenClaw **channel plugin** — the typed adapter that connects OpenClaw to a messaging platform — drawn from the `plugins/sdk-channel-plugins` source page. It covers the core/plugin ownership split (what the shared `message` tool in core owns versus what your plugin owns), the `ChannelPlugin` adapter surfaces (config, security, pairing, session grammar, outbound, threading, heartbeat typing), the approval model and declared channel capabilities (`approvalCapability`), and the two-layer inbound mention policy that gates which inbound messages become agent turns. The procedural authoring walkthrough (package/manifest, build, wire, setup, inbound, test) lives in the sibling walkthrough note; this note holds only the design concepts that walkthrough realizes.

## Core vs Plugin Ownership

Channel plugins do not need their own send/edit/react tools. OpenClaw keeps one shared `message` tool in core, and core also owns prompt wiring, the outer session-key shape, generic `:thread:` bookkeeping, and dispatch. The plugin owns a focused set of platform-specific responsibilities:

- **Config** — account resolution and the setup wizard.
- **Security** — DM policy and allowlists.
- **Pairing** — the DM approval flow.
- **Session grammar** — how provider-specific conversation ids map to base chats, thread ids, and parent fallbacks.
- **Outbound** — sending text, media, and polls to the platform.
- **Threading** — how replies are threaded.
- **Heartbeat typing** — optional typing/busy signals for heartbeat delivery targets.

New channel plugins should expose a `message` adapter via `defineChannelMessageAdapter` from `openclaw/plugin-sdk/channel-outbound`. The adapter declares which durable final-send capabilities the native transport actually supports and points text/media sends at the same transport functions as the legacy `outbound` adapter — a capability is only declared when a contract test proves the native side effect and returned receipt. If the existing `outbound` adapter already has the right send methods and capability metadata, `createChannelMessageAdapterFromOutbound(...)` derives the `message` adapter instead of hand-writing another bridge. Adapter sends return `MessageReceipt` values; compatibility code that still needs legacy ids derives them with `listMessageReceiptPlatformIds(...)` or `resolveMessageReceiptPrimaryId(...)` rather than keeping parallel `messageIds` fields.

Preview-capable channels declare `message.live.capabilities` describing the exact live lifecycle they own — `draftPreview`, `previewFinalization`, `progressUpdates`, `nativeStreaming`, or `quietFinalization`. Channels that finalize a draft preview in place additionally declare `message.live.finalizer.capabilities` (`finalEdit`, `normalFallback`, `discardPending`, `previewReceipt`, `retainOnAmbiguousFailure`) and route runtime logic through `defineFinalizableLivePreviewAdapter(...)` plus `deliverWithFinalizableLivePreviewAdapter(...)`, kept honest by `verifyChannelMessageLiveCapabilityAdapterProofs(...)` and `verifyChannelMessageLiveFinalizerProofs(...)` tests. Inbound receivers that defer platform acknowledgements declare `message.receive.defaultAckPolicy` and `supportedAckPolicies` (covered by `verifyChannelMessageReceiveAckPolicyAdapterProofs(...)`) instead of hiding ack timing in monitor-local state.

## Session Grammar and Inbound Authorization

If a platform stores extra scope inside conversation ids, that parsing stays in the plugin via `messaging.resolveSessionConversation(...)` — the canonical hook for mapping `rawId` to the base conversation id, an optional thread id, an explicit `baseConversationId`, and any `parentConversationCandidates` (which must be ordered narrowest-parent first). Plugins with provider-specific target grammar expose `messaging.resolveOutboundSessionRoute(...)` so core gets provider-native session and thread identity without parser shims, and `openclaw/plugin-sdk/channel-route` normalizes route-like fields, compares a child thread with its parent route, and builds a stable dedupe key from `{ channel, to, accountId, threadId }` (preferred over ad hoc `String(threadId)` comparisons). Bundled plugins that need the same parsing before the channel registry boots can also expose a top-level `session-key-api.ts` file with a matching `resolveSessionConversation(...)` export, used only when the runtime plugin registry is not yet available. The legacy `messaging.resolveParentConversationCandidates(...)` remains a compatibility fallback: when both hooks exist, core uses `resolveSessionConversation(...).parentConversationCandidates` first and falls back only when the canonical hook omits them.

Channels migrating inbound authorization can use the experimental `openclaw/plugin-sdk/channel-ingress-runtime` subpath from runtime receive paths. It keeps platform lookup and side effects in the plugin while sharing allowlist state resolution, route/sender/command/event/activation decisions, redacted diagnostics, and turn-admission mapping — plugin identity normalization stays in the descriptor passed to the resolver, and raw match values from the resolved state or decision must not be serialized. Legacy reply helpers (`createChannelTurnReplyPipeline`, `dispatchInboundReplyWithBase`, `recordInboundSessionAndDispatchReply`) remain for compatibility dispatchers but should not be used for new channel code; new plugins start with the `message` adapter, receipts, and the receive/send lifecycle helpers on `openclaw/plugin-sdk/channel-outbound`.

For channels that support typing indicators outside inbound replies, `heartbeat.sendTyping(...)` is exposed on the channel plugin and called by core with the resolved heartbeat delivery target before the heartbeat model run starts (with the shared typing keepalive/cleanup lifecycle); `heartbeat.clearTyping(...)` is added when the platform needs an explicit stop signal. Channels that add message-tool params carrying media sources expose those param names through `describeMessageTool(...).mediaSourceParams` (preferably an action-keyed map such as `{ "set-profile": ["avatarUrl", "avatarPath"] }`) so core can do sandbox path normalization and outbound media-access policy without provider-specific special cases. A channel that must expose a temporary public URL for a platform-side media fetch can use `createHostedOutboundMediaStore(...)` from `openclaw/plugin-sdk/outbound-media`, keeping route parsing and token enforcement in the plugin. Provider-specific shaping for `message(action="send")` prefers `actions.prepareSendPayload(...)` (with native cards/blocks/embeds under `payload.channelData.<channel>`), using `actions.handleAction(...)` only as a compatibility fallback for payloads that cannot be serialized and retried.

## Approvals and Declared Channel Capabilities

Most channel plugins need no approval-specific code: core owns same-chat `/approve`, shared approval button payloads, and generic fallback delivery. When a channel needs approval-specific behavior, it declares one `approvalCapability` object on the channel plugin. `ChannelPlugin.approvals` is removed — approval delivery/native/render/auth facts now live on `approvalCapability`, while `plugin.auth` is login/logout only (core no longer reads approval auth hooks from it). The canonical approval-auth seam is `approvalCapability.authorizeActorAction` plus `approvalCapability.getActionAvailabilityState` (the latter used for same-chat approval auth availability). A channel exposing native exec approvals uses `approvalCapability.getExecInitiatingSurfaceState` for the initiating-surface/native-client state when it differs from same-chat approval auth; core uses that hook to distinguish `enabled` vs `disabled`, decide whether the initiating channel supports native exec approvals, and include it in native-client fallback guidance (`createApproverRestrictedNativeApprovalCapability(...)` fills this in for the common case).

The `approvalCapability` surface splits into focused seams. `approvalCapability.delivery` is only for native approval routing or fallback suppression; `approvalCapability.render` only when a channel truly needs custom approval payloads instead of the shared renderer; and `approvalCapability.nativeRuntime` carries channel-owned native approval facts (kept lazy on hot entrypoints with `createLazyChannelApprovalNativeRuntimeAdapter(...)`). `nativeRuntime` further decomposes into:

- `availability` — whether the account is configured and whether a request should be handled.
- `presentation` — map the shared approval view model into pending/resolved/expired native payloads or final actions.
- `transport` — prepare targets plus send/update/delete native approval messages.
- `interactions` — optional bind/unbind/clear-action hooks for native buttons or reactions, plus an optional `cancelDelivered` hook (implemented when `deliverPending` registers in-process or persistent state so it can be released if a handler stop cancels delivery before `bindPending` runs, or when `bindPending` returns no handle).
- `observe` — optional delivery diagnostics hooks.

Native approval delivery keeps channel code focused on target normalization plus transport/presentation facts, using `createChannelExecApprovalProfile`, `createChannelNativeOriginTargetResolver`, `createChannelApproverDmTargetResolver`, and `createApproverRestrictedNativeApprovalCapability` from `openclaw/plugin-sdk/approval-runtime`, so core owns request filtering, routing, dedupe, expiry, gateway subscription, and routed-elsewhere notices. `createNativeApprovalChannelRouteGates` (from `openclaw/plugin-sdk/approval-native-runtime`) centralizes approval config selection, `mode` handling, agent/session filters, account binding, and target matching for channels supporting both session-origin native delivery and explicit forwarding targets — but it must not create core-owned policy defaults; the channel passes its documented default mode explicitly. Native approval channels must route both `accountId` (to scope multi-account approval policy to the right bot account) and `approvalKind` (to keep exec-vs-plugin behavior available without hardcoded core branches), and must preserve the delivered approval id kind end-to-end rather than guessing or rewriting routing from channel-local state. Core also owns approval reroute notices, so channels should not send their own "approval went to DMs / another channel" follow-up messages from `createChannelNativeApprovalRuntime`; they expose accurate origin + approver-DM routing through the shared capability helpers and let core aggregate actual deliveries before posting any notice.

For same-chat approval restriction without approval-specific core logic, a channel that can infer stable owner-like DM identities uses `createResolvedApproverActionAuthAdapter` from `openclaw/plugin-sdk/approval-runtime`. Custom approval auth that intentionally allows only same-chat fallback returns `markImplicitSameChatApprovalAuthorization({ authorized: true })` from `openclaw/plugin-sdk/approval-auth-runtime` (otherwise core treats the result as explicit approver authorization), and a channel-owned native callback that resolves approvals directly checks `isImplicitSameChatApprovalAuthorization(...)` first so implicit fallback still flows through normal actor authorization. Approval kinds may intentionally expose different native surfaces — among bundled examples, Slack keeps native routing for both exec and plugin ids, while Matrix keeps the same native DM/channel routing and reaction UX for exec and plugin approvals while letting auth differ by kind. For hot entrypoints needing only one part of this family, narrower runtime subpaths exist (`approval-auth-runtime`, `approval-client-runtime`, `approval-delivery-runtime`, `approval-gateway-runtime`, `approval-handler-adapter-runtime`, `approval-handler-runtime`, `approval-native-runtime`, `approval-reply-runtime`, `channel-runtime-context`). Auth-only channels usually stop at the default path — core handles approvals and the plugin only exposes outbound/auth capabilities — while native approval channels (Matrix, Slack, Telegram, custom chat transports) use the shared native helpers instead of rolling their own approval lifecycle.

## Inbound Mention Policy

Inbound mention handling is split into two layers: **plugin-owned evidence gathering** and **shared policy evaluation**. The plugin owns logic that depends on platform specifics — reply-to-bot detection, quoted-bot detection, thread-participation checks, service/system-message exclusions, and any platform-native caches needed to prove bot participation. The shared helper owns the policy: `requireMention`, the explicit mention result, the implicit mention allowlist, command bypass, and the final skip decision. Mention-policy decisions use `openclaw/plugin-sdk/channel-mention-gating`; the broader inbound helper barrel `openclaw/plugin-sdk/channel-inbound` is used only when more inbound helpers are needed.

The preferred flow is: (1) compute local mention facts; (2) pass those facts into `resolveInboundMentionDecision({ facts, policy })`; (3) use `decision.effectiveWasMentioned`, `decision.shouldBypassMention`, and `decision.shouldSkip` in the inbound gate. The canonical shape, copied from source:

```typescript
const decision = resolveInboundMentionDecision({
  facts,
  policy: {
    isGroup,
    requireMention,
    allowedImplicitMentionKinds: requireExplicitMention ? [] : ["reply_to_bot", "quoted_bot"],
    allowTextCommands,
    hasControlCommand,
    commandAuthorized,
  },
});

if (decision.shouldSkip) return;
```

The facts object is built from helpers such as `matchesMentionWithExplicit(text, { mentionRegexes, mentionPatterns })` and `implicitMentionKindWhen("reply_to_bot", isReplyToBot)` / `implicitMentionKindWhen("quoted_bot", isQuoteOfBot)`. For bundled channel plugins that already depend on runtime injection, `api.runtime.channel.mentions` exposes the same shared mention helpers — `buildMentionRegexes`, `matchesMentionPatterns`, `matchesMentionWithExplicit`, `implicitMentionKindWhen`, and `resolveInboundMentionDecision`. A plugin that only needs `implicitMentionKindWhen` and `resolveInboundMentionDecision` imports from `openclaw/plugin-sdk/channel-mention-gating` to avoid loading unrelated inbound runtime helpers.

**Source**: OpenClaw documentation — `plugins/sdk-channel-plugins` (mirror `inbox/openclaw_docs/plugins/sdk-channel-plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
