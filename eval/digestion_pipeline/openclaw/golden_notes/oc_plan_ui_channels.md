---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - message_presentation
keywords:
  - openclaw ui channels refactor
  - message presentation reply payload
  - channel outbound adapter capabilities
  - presentation auto-degrade text fallback
  - delivery pin metadata
  - render presentation native ui
  - block kit adaptive cards carbon flex
  - buildCrossContextComponents removal
topics:
  - OpenClaw
  - Channel Presentation Refactor
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/plan/ui-channels
access_control_group: ["general"]
---

# OpenClaw — Channel Presentation Refactor (UI-Channels Plan)

## Overview

This note captures the **argument** of OpenClaw's `plan/ui-channels` design spec: core must stop knowing native channel UI shapes, and instead emit a single **semantic** `ReplyPayload.presentation` (plus generic `delivery` metadata) that each channel's *runtime outbound adapter* renders into its native transport (Discord components-v2/Carbon, Slack Block Kit, Telegram inline keyboards, Teams Adaptive Cards, Feishu interactive cards, LINE Flex), auto-degrading to text where a feature is unsupported. It mirrors the `plan/ui-channels` source page in full — the front-matter `summary` ("Decouple semantic message presentation from channel native UI renderers") and `read_when` design context, the `## Status` (Implemented for the shared agent, CLI, plugin-capability, and outbound-delivery surfaces), the Problem/Goals/Non-goals rationale, the `MessagePresentation` + `ReplyPayloadDelivery` + `ChannelOutboundAdapter` target contracts, the per-channel mapping, the 15-step refactor sequence, the test matrix, and the open questions. Per the source, the **canonical contract/renderer/fallback guide now lives at [Message Presentation](https://docs.openclaw.ai/plugins/message-presentation)**; this plan is retained as historical implementation context and is the design-decision anchor that the runtime concept notes and the FZ-15 OpenClaw architecture analysis cite.

## The Problem — Native UI Leaks Into Core

The refactor argues that channel UI is split across several incompatible surfaces that contaminate the core. Core owns a Discord-shaped cross-context renderer hook through `buildCrossContextComponents`; Discord `channel.ts` can import native Carbon UI through `DiscordUiContainer`, which pulls runtime UI dependencies into the channel-plugin control plane; the agent and CLI expose native payload escape hatches such as Discord `components`, Slack `blocks`, Telegram/Mattermost `buttons`, and Teams/Feishu `card`; `ReplyPayload.channelData` carries both transport hints AND native UI envelopes; and the generic `interactive` model exists but is narrower than the richer layouts already used by Discord, Slack, Teams, Feishu, LINE, Telegram, and Mattermost. The stated consequence is the thesis: this makes core aware of native UI shapes, weakens plugin runtime laziness, and gives agents too many provider-specific ways to express the same message intent.

## Goals and Non-Goals

The design's goals state the desired end state directly: core decides the best semantic presentation for a message from declared capabilities; extensions declare capabilities and render semantic presentation into native transport payloads; Web Control UI remains separate from chat native UI; native channel payloads are not exposed through the shared agent or CLI message surface; unsupported presentation features auto-degrade to the best text representation; and delivery behavior such as pinning a sent message is generic delivery metadata, not presentation. The non-goals bound the refactor: NO backwards-compatibility shim for `buildCrossContextComponents`; NO public native escape hatches for `components`, `blocks`, `buttons`, or `card`; NO core imports of channel-native UI libraries; and NO provider-specific SDK seams for bundled channels.

## Target Model — `MessagePresentation`

The core argument crystallizes in a new core-owned `presentation` field on `ReplyPayload`, carrying a semantic, channel-agnostic message UI. Reproduced verbatim from the source:

```ts
type MessagePresentationTone = "neutral" | "info" | "success" | "warning" | "danger";

type MessagePresentation = {
  tone?: MessagePresentationTone;
  title?: string;
  blocks: MessagePresentationBlock[];
};

type MessagePresentationBlock =
  | { type: "text"; text: string }
  | { type: "context"; text: string }
  | { type: "divider" }
  | { type: "buttons"; buttons: MessagePresentationButton[] }
  | { type: "select"; placeholder?: string; options: MessagePresentationOption[] };

type MessagePresentationButton = {
  label: string;
  value?: string;
  url?: string;
  style?: "primary" | "secondary" | "success" | "danger";
};

type MessagePresentationOption = {
  label: string;
  value: string;
};
```

The legacy `interactive` model becomes a subset of `presentation` during migration: an `interactive` text block maps to `presentation.blocks[].type = "text"`, an `interactive` buttons block maps to `type = "buttons"`, and an `interactive` select block maps to `type = "select"`. The argument here is migration-without-breakage — the external agent and CLI schemas now use `presentation`, while `interactive` remains an internal legacy parser/rendering helper for existing reply producers; the public producer-facing API treats `interactive` as deprecated, but runtime support remains so existing approval helpers and older plugins continue to work while new code emits `presentation`.

## Delivery Metadata — Pin Is Not Presentation

A second core-owned field, `delivery`, captures send behavior that is explicitly NOT UI — the design separates "what the message looks like" (presentation) from "how it is delivered" (delivery). Reproduced verbatim:

```ts
type ReplyPayloadDelivery = {
  pin?:
    | boolean
    | {
        enabled: boolean;
        notify?: boolean;
        required?: boolean;
      };
};
```

The semantics argue for safe, degrading defaults: `delivery.pin = true` means pin the first successfully delivered message; `notify` defaults to `false`; `required` defaults to `false`, and unsupported channels or failed pinning auto-degrade by continuing delivery (a failed pin does not fail the send). Manual `pin`, `unpin`, and `list-pins` message actions remain for existing messages. As a concrete migration the spec states the current Telegram ACP topic binding should move from `channelData.telegram.pin = true` to `delivery.pin = true` — moving a provider-private envelope onto the generic delivery contract.

## Runtime Capability Contract

The design places presentation/delivery render hooks on the **runtime outbound adapter**, NOT the control-plane channel plugin — keeping native UI libraries out of the control plane (the Goals' core/edge separation). An adapter declares what it can render, supplies a `renderPresentation` hook, and optionally a `pinDeliveredMessage` hook. Reproduced verbatim:

```ts
type ChannelPresentationCapabilities = {
  supported: boolean;
  buttons?: boolean;
  selects?: boolean;
  context?: boolean;
  divider?: boolean;
  tones?: MessagePresentationTone[];
  limits?: {
    actions?: {
      maxActions?: number;
      maxActionsPerRow?: number;
      maxRows?: number;
      maxLabelLength?: number;
      maxValueBytes?: number;
      supportsStyles?: boolean;
      supportsDisabled?: boolean;
      supportsLayoutHints?: boolean;
    };
    selects?: {
      maxOptions?: number;
      maxLabelLength?: number;
      maxValueBytes?: number;
    };
    text?: {
      maxLength?: number;
      encoding?: "characters" | "utf8-bytes" | "utf16-units";
      markdownDialect?: "plain" | "markdown" | "html" | "slack-mrkdwn" | "discord-markdown";
      supportsEdit?: boolean;
    };
  };
};

type ChannelDeliveryCapabilities = {
  pinSentMessage?: boolean;
};

type ChannelOutboundAdapter = {
  presentationCapabilities?: ChannelPresentationCapabilities;

  renderPresentation?: (params: {
    payload: ReplyPayload;
    presentation: MessagePresentation;
    ctx: ChannelOutboundSendContext;
  }) => ReplyPayload | null;

  deliveryCapabilities?: ChannelDeliveryCapabilities;

  pinDeliveredMessage?: (params: {
    cfg: OpenClawConfig;
    accountId?: string | null;
    to: string;
    threadId?: string | number | null;
    messageId: string;
    notify: boolean;
  }) => Promise<void>;
};
```

The core behavior the contract drives is a fixed pipeline: resolve target channel and runtime adapter; ask for presentation capabilities; degrade unsupported blocks and apply generic capability limits BEFORE rendering; call `renderPresentation`; if no renderer exists, convert presentation to text fallback; and after a successful send, call `pinDeliveredMessage` when `delivery.pin` is requested and supported. This is the argument's operative claim — degradation and limit-clamping happen in core against declared capabilities, so adapters only ever render presentation they can support.

## Channel Mapping

The plan maps the single semantic contract onto each native renderer, demonstrating the thesis is realizable across heterogeneous channels. **Discord**: render `presentation` to components-v2 and Carbon containers in runtime-only modules, keep accent-color helpers in light modules, and remove `DiscordUiContainer` imports from channel-plugin control-plane code. **Slack**: render `presentation` to Block Kit and remove the agent/CLI `blocks` input. **Telegram**: render text/context/dividers as text, render actions and select as inline keyboards when configured and allowed for the target surface, use text fallback when inline buttons are disabled, and move ACP topic pinning to `delivery.pin`. **Mattermost**: render actions as interactive buttons where configured, and render other blocks as text fallback. **MS Teams**: render `presentation` to Adaptive Cards, keep manual pin/unpin/list-pins actions, and optionally implement `pinDeliveredMessage` if Graph support is reliable for the target conversation. **Feishu**: render `presentation` to interactive cards, keep manual pin/unpin/list-pins actions, and optionally implement `pinDeliveredMessage` for sent-message pinning if API behavior is reliable. **LINE**: render `presentation` to Flex or template messages where possible, fall back to text for unsupported blocks, and remove LINE UI payloads from `channelData`. **Plain or limited channels**: convert presentation to text with conservative formatting.

## Refactor Steps (15)

The implementation sequence the argument lays out (verbatim ordering):

1. Reapply the Discord release fix that splits `ui-colors.ts` from Carbon-backed UI and removes `DiscordUiContainer` from `extensions/discord/src/channel.ts`.
2. Add `presentation` and `delivery` to `ReplyPayload`, outbound payload normalization, delivery summaries, and hook payloads.
3. Add `MessagePresentation` schema and parser helpers in a narrow SDK/runtime subpath.
4. Replace message capabilities `buttons`, `cards`, `components`, and `blocks` with semantic presentation capabilities.
5. Add runtime outbound adapter hooks for presentation render and delivery pinning.
6. Replace cross-context component construction with `buildCrossContextPresentation`.
7. Delete `src/infra/outbound/channel-adapters.ts` and remove `buildCrossContextComponents` from channel plugin types.
8. Change `maybeApplyCrossContextMarker` to attach `presentation` instead of native params.
9. Update plugin-dispatch send paths to consume only semantic presentation and delivery metadata.
10. Remove agent and CLI native payload params: `components`, `blocks`, `buttons`, and `card`.
11. Remove SDK helpers that create native message-tool schemas, replacing them with presentation schema helpers.
12. Remove UI/native envelopes from `channelData`; keep only transport metadata until each remaining field is reviewed.
13. Migrate Discord, Slack, Telegram, Mattermost, MS Teams, Feishu, and LINE renderers.
14. Update docs for message CLI, channel pages, plugin SDK, and capability cookbook.
15. Run import fanout profiling for Discord and affected channel entrypoints.

The source records implementation status against this sequence: steps 1-11 and 13-14 are implemented for the shared agent, CLI, plugin capability, and outbound adapter contracts; step 12 remains a deeper internal cleanup pass for provider-private `channelData` transport envelopes; and step 15 remains follow-up validation if quantified import-fanout numbers beyond the type/test gate are wanted.

## Tests and Open Questions

The test matrix the plan mandates adding or updating: presentation normalization tests; presentation auto-degrade tests for unsupported blocks; cross-context marker tests for plugin dispatch and core delivery paths; channel render matrix tests for Discord, Slack, Telegram, Mattermost, MS Teams, Feishu, LINE, and text fallback; message-tool schema tests proving native fields are gone; CLI tests proving native flags are gone; a Discord entrypoint import-laziness regression covering Carbon; and delivery-pin tests covering Telegram and generic fallback. Three open questions remain unresolved in the design: whether `delivery.pin` should be implemented for Discord, Slack, MS Teams, and Feishu in the first pass or only Telegram first; whether `delivery` should eventually absorb existing fields such as `replyToId`, `replyToCurrent`, `silent`, and `audioAsVoice`, or stay focused on post-send behaviors; and whether presentation should support images or file references directly, or whether media should remain separate from UI layout for now.

**Source**: OpenClaw documentation — `plan/ui-channels` (mirror `inbox/openclaw_docs/plan/ui-channels.md`)
**Last Updated**: 2026-06-22
**Status**: Active
