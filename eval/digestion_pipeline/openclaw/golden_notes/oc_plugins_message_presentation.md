---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - message_presentation
keywords:
  - openclaw message presentation
  - messagepresentation contract
  - presentation blocks buttons selects
  - presentationcapabilities limits
  - renderpresentation outbound adapter
  - degradation fallback text
  - delivery pin replypayloaddelivery
  - presentation vs interactivereply
topics:
  - OpenClaw
  - Message Presentation
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/message-presentation
access_control_group: ["general"]
---

# OpenClaw — Message Presentation Contract

## Overview

This note models OpenClaw's **message presentation** contract: the shared, portable rich-outbound-chat-UI schema that lets agents, CLI commands, approval flows, and plugins describe a message intent once while each channel plugin renders the best native shape it can. It mirrors the `plugins/message-presentation` source page — the typed `MessagePresentation` / `MessagePresentationBlock` / `ReplyPayloadDelivery` shapes, button/select semantics, producer JSON/CLI examples, the renderer `presentationCapabilities` contract, the core render flow, degradation rules, the per-provider mapping table, the `MessagePresentation`-vs-`InteractiveReply` relationship, delivery-pin behavior, and the plugin-author checklist. Plugin authors MUST NOT add provider-native fields (Discord `components`, Slack `blocks`, Telegram `buttons`, Teams `card`, Feishu `card`) to the shared message tool — those are renderer outputs owned by the channel plugin.

## The Presentation Contract

Plugin authors import the public contract from `openclaw/plugin-sdk/interactive-runtime` (the types `MessagePresentation` and `ReplyPayloadDelivery`). A `MessagePresentation` is an optional `title?: string`, an optional `tone?: "neutral" | "info" | "success" | "warning" | "danger"`, and a required `blocks: MessagePresentationBlock[]`. Each block is one of five discriminated shapes — `{ type: "text"; text }`, `{ type: "context"; text }`, `{ type: "divider" }`, `{ type: "buttons"; buttons }`, or `{ type: "select"; placeholder?; options }`. The intended portable UI surface is text sections, small context/footer text, dividers, buttons, select menus, and a card title and tone.

```ts
type MessagePresentation = {
  title?: string;
  tone?: "neutral" | "info" | "success" | "warning" | "danger";
  blocks: MessagePresentationBlock[];
};

type MessagePresentationBlock =
  | { type: "text"; text: string }
  | { type: "context"; text: string }
  | { type: "divider" }
  | { type: "buttons"; buttons: MessagePresentationButton[] }
  | { type: "select"; placeholder?: string; options: MessagePresentationOption[] };

type MessagePresentationAction =
  | { type: "command"; command: string }
  | { type: "callback"; value: string };

type MessagePresentationButton = {
  label: string;
  action?: MessagePresentationAction;
  /** Legacy callback value. Prefer action for new controls. */
  value?: string;
  url?: string;
  webApp?: { url: string };
  /** @deprecated Use webApp. Accepted for legacy JSON payloads only. */
  web_app?: { url: string };
  priority?: number;
  disabled?: boolean;
  reusable?: boolean;
  style?: "primary" | "secondary" | "success" | "danger";
};

type MessagePresentationOption = {
  label: string;
  action?: MessagePresentationAction;
  /** Legacy callback value. Prefer action for new controls. */
  value?: string;
};

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

**Button semantics.** `action.type: "command"` runs a native slash command through core's command path (use it for built-in command buttons and menus); `action.type: "callback"` carries opaque plugin data through the channel's interaction path, and channel plugins MUST NOT reinterpret callback data as slash commands. `value` is the legacy opaque callback value — new controls should use `action` so channel plugins can map commands and callbacks without guessing from text. `url` is a link button and can exist without `value`. `webApp` describes a channel-native web app button (Telegram renders it as `web_app` and only supports it in private chats; `web_app` is still accepted in loose JSON payloads for compatibility, but TypeScript producers should use `webApp`). `label` is required and is also used in text fallback. `style` is advisory — renderers should map unsupported styles to a safe default, not fail the send. `priority` is optional — when a channel advertises action limits and controls must be dropped, core keeps higher-priority buttons first and preserves original order among equal-priority buttons, and when all controls fit, authored order is preserved. `disabled` is optional and channels must opt in with `supportsDisabled`, otherwise core degrades the disabled control to non-interactive fallback text. `reusable` is optional — channels that support reusable native callbacks may keep the action available after a successful interaction (use it for repeatable or idempotent actions such as refresh, inspect, or more details; leave it unset for normal one-shot approvals and destructive actions).

**Select semantics.** `options[].action` has the same command/callback meaning as button `action`; `options[].value` is the legacy selected application value; `placeholder` is advisory and may be ignored by channels without native select support; if a channel does not support selects, fallback text lists the labels.

## Producer Examples

Producers emit a presentation as JSON (on a `ReplyPayload`/message action) or via the `openclaw message send --presentation '<json>'` CLI flag. A simple warning card combines `text`, `context`, and a `buttons` block; URL-only link buttons need only `label` + `url`; a Telegram Mini App button uses `web_app: { url }`; a select menu carries `options` with `label` + `value`. Pinned delivery is requested either with the CLI `--pin` flag or by an explicit `delivery.pin` JSON object.

```json
{
  "title": "Deploy approval",
  "tone": "warning",
  "blocks": [
    { "type": "text", "text": "Canary is ready to promote." },
    { "type": "context", "text": "Build 1234, staging passed." },
    {
      "type": "buttons",
      "buttons": [
        { "label": "Approve", "value": "deploy:approve", "style": "success" },
        { "label": "Decline", "value": "deploy:decline", "style": "danger" }
      ]
    }
  ]
}
```

A URL-only link button omits `value`: `{ "label": "Open notes", "url": "https://example.com/release" }`. A Telegram Mini App button uses `{ "label": "Launch", "web_app": { "url": "https://example.com/app" } }`. A select block lists `{ "label": "Canary", "value": "env:canary" }` style options under `"type": "select"` with an optional `"placeholder"`. The CLI sends a presentation inline:

```bash
openclaw message send --channel slack \
  --target channel:C123 \
  --message "Deploy approval" \
  --presentation '{"title":"Deploy approval","tone":"warning","blocks":[{"type":"text","text":"Canary is ready."},{"type":"buttons","buttons":[{"label":"Approve","value":"deploy:approve","style":"success"},{"label":"Decline","value":"deploy:decline","style":"danger"}]}]}'
```

Pinned delivery uses `--pin` (e.g. `openclaw message send --channel telegram --target -1001234567890 --message "Topic opened" --pin`) or an explicit `{ "pin": { "enabled": true, "notify": true, "required": false } }` JSON object.

## Renderer Contract

Channel plugins declare render support on their outbound adapter (`ChannelOutboundAdapter`). The adapter advertises `presentationCapabilities` (capability booleans `supported` / `buttons` / `selects` / `context` / `divider`, plus an optional `limits` envelope), `deliveryCapabilities` (e.g. `pin: true`), a synchronous `renderPresentation({ payload, presentation, ctx })`, and an async `pinDeliveredMessage({ target, messageId, pin })`. Capability booleans describe what the renderer can make interactive; the optional `limits` describe the generic envelope core can adapt before calling the renderer.

```ts
const adapter: ChannelOutboundAdapter = {
  deliveryMode: "direct",
  presentationCapabilities: {
    supported: true,
    buttons: true,
    selects: true,
    context: true,
    divider: true,
    limits: {
      actions: {
        maxActions: 25,
        maxActionsPerRow: 5,
        maxRows: 5,
        maxLabelLength: 80,
        maxValueBytes: 100,
        supportsStyles: true,
        supportsDisabled: false,
      },
      selects: {
        maxOptions: 25,
        maxLabelLength: 100,
        maxValueBytes: 100,
      },
      text: {
        maxLength: 2000,
        encoding: "characters",
        markdownDialect: "discord-markdown",
      },
    },
  },
  deliveryCapabilities: {
    pin: true,
  },
  renderPresentation({ payload, presentation, ctx }) {
    return renderNativePayload(payload, presentation, ctx);
  },
  async pinDeliveredMessage({ target, messageId, pin }) {
    await pinNativeMessage(target, messageId, { notify: pin.notify === true });
  },
};
```

The full `ChannelPresentationCapabilities` type adds optional `actions.supportsLayoutHints`, a `text.supportsEdit`, the `encoding` enum `"characters" | "utf8-bytes" | "utf16-units"`, and the `markdownDialect` enum `"plain" | "markdown" | "html" | "slack-mrkdwn" | "discord-markdown"`. Core applies generic limits to semantic controls before rendering; renderers still own final provider-specific validation and clipping for native block count, card size, URL limits, and provider quirks that cannot be expressed in the generic contract. If limits remove every control from a block, core keeps the labels as non-interactive context text so the delivered message still has a visible fallback.

## Core Render Flow

When a `ReplyPayload` or message action includes `presentation`, core runs eight ordered steps: (1) normalizes the presentation payload; (2) resolves the target channel's outbound adapter; (3) reads `presentationCapabilities`; (4) applies generic capability limits such as action count, label length, and select option count when the adapter advertises them; (5) calls `renderPresentation` when the adapter can render the payload; (6) falls back to conservative text when the adapter is absent or cannot render; (7) sends the resulting payload through the normal channel delivery path; (8) applies delivery metadata such as `delivery.pin` after the first successful sent message. Core owns fallback behavior so producers can stay channel-agnostic, while channel plugins own native rendering and interaction handling.

## Degradation Rules

Presentation must be safe to send on limited channels. Fallback text includes the `title` as the first line, `text` blocks as normal paragraphs, `context` blocks as compact context lines, `divider` blocks as a visual separator, button labels (including URLs for link buttons), and select option labels. Unsupported native controls should degrade rather than fail the whole send: Telegram with inline buttons disabled sends text fallback; a channel without select support lists select options as text; a URL-only button becomes either a native link button or a fallback URL line; and optional pin failures do not fail the delivered message. The main exception is `delivery.pin.required: true` — if pinning is requested as required and the channel cannot pin the sent message, delivery reports failure.

## Provider Mapping

The current bundled renderers map the generic presentation to per-channel native targets. Provider-native payload compatibility is a transition affordance for existing reply producers and is not a reason to add new shared native fields.

| Channel | Native render target | Notes |
| --- | --- | --- |
| Discord | Components and component containers | Preserves legacy `channelData.discord.components` for existing provider-native payload producers, but new shared sends should use `presentation`. |
| Slack | Block Kit | Preserves legacy `channelData.slack.blocks` for existing provider-native payload producers, but new shared sends should use `presentation`. |
| Telegram | Text plus inline keyboards | Buttons/selects require inline button capability for the target surface; otherwise text fallback is used. |
| Mattermost | Text plus interactive props | Other blocks degrade to text. |
| Microsoft Teams | Adaptive Cards | Plain `message` text is included with the card when both are provided. |
| Feishu | Interactive cards | Card header can use `title`; body avoids duplicating that title. |
| Plain channels | Text fallback | Channels without a renderer still get readable output. |

## Presentation vs InteractiveReply

`InteractiveReply` is the older internal subset used by approval and interaction helpers; it supports text, buttons, and selects only. `MessagePresentation` is the canonical shared send contract and adds title, tone, context, divider, URL-only buttons, and generic delivery metadata through `ReplyPayload.delivery`. New code should accept or produce `MessagePresentation` directly; existing `interactive` payloads are a deprecated subset of `presentation`, with runtime support retained for older producers. When bridging older code, use helpers from `openclaw/plugin-sdk/interactive-runtime`.

```ts
import {
  adaptMessagePresentationForChannel,
  applyPresentationActionLimits,
  interactiveReplyToPresentation,
  normalizeMessagePresentation,
  presentationPageSize,
  presentationToInteractiveControlsReply,
  presentationToInteractiveReply,
  renderMessagePresentationFallbackText,
} from "openclaw/plugin-sdk/interactive-runtime";
```

The legacy `InteractiveReply*` types and conversion helpers are marked `@deprecated` in the SDK: the types `InteractiveReply`, `InteractiveReplyBlock`, `InteractiveReplyButton`, `InteractiveReplyOption`, `InteractiveReplySelectBlock`, and `InteractiveReplyTextBlock`, plus `normalizeInteractiveReply(...)`, `hasInteractiveReplyBlocks(...)`, `interactiveReplyToPresentation(...)`, `presentationToInteractiveReply(...)`, `presentationToInteractiveControlsReply(...)`, `resolveInteractiveTextFallback(...)`, and `reduceInteractiveReply(...)`. The two functions `presentationToInteractiveReply(...)` and `presentationToInteractiveControlsReply(...)` remain available as renderer bridges for legacy channel implementations, but new producer code should not call them — it should send `presentation` and let core/channel adaptation handle rendering. Approval helpers have presentation-first replacements: use `buildApprovalPresentationFromActionDescriptors(...)` instead of `buildApprovalInteractiveReplyFromActionDescriptors(...)`, `buildApprovalPresentation(...)` instead of `buildApprovalInteractiveReply(...)`, and `buildExecApprovalPresentation(...)` instead of `buildExecApprovalInteractiveReply(...)`. `renderMessagePresentationFallbackText(...)` returns an empty string for presentation blocks that have no text fallback (such as a divider-only presentation); transports that require a non-empty send body can pass `emptyFallback` to opt into a minimal body without changing the default fallback contract.

## Delivery Pin

Pinning is delivery behavior, not presentation, so producers use `delivery.pin` instead of provider-native fields such as `channelData.telegram.pin`. Semantics: `pin: true` pins the first successfully delivered message; `pin.notify` defaults to `false`; `pin.required` defaults to `false`; optional pin failures degrade and leave the sent message intact; required pin failures fail delivery; and chunked messages pin the first delivered chunk, not the tail chunk. Manual `pin`, `unpin`, and `pins` message actions still exist for existing messages where the provider supports those operations.

## Plugin Author Checklist

A channel-plugin author wiring up presentation should: declare `presentation` from `describeMessageTool(...)` when the channel can render or safely degrade semantic presentation; add `presentationCapabilities` to the runtime outbound adapter; implement `renderPresentation` in runtime code, not control-plane plugin setup code; keep native UI libraries out of hot setup/catalog paths; declare generic capability limits on `presentationCapabilities.limits` when they are known; preserve final platform limits in the renderer and tests; add fallback tests for unsupported buttons, selects, URL buttons, title/text duplication, and mixed `message` plus `presentation` sends; add delivery pin support through `deliveryCapabilities.pin` and `pinDeliveredMessage` only when the provider can pin the sent message id; and not expose new provider-native card/block/component/button fields through the shared message action schema.

**Source**: OpenClaw documentation — `plugins/message-presentation` (mirror `inbox/openclaw_docs/plugins/message-presentation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
