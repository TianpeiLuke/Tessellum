---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - com.openclaw.presentation
  - matrix message presentation metadata
  - openclaw matrix rich blocks
  - matrix presentation fallback body
  - matrix buttons select context divider
  - com.openclaw.approval relationship
  - matrix media event presentation
topics:
  - OpenClaw
  - Matrix Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/matrix-presentation
access_control_group: ["general"]
---

# OpenClaw — Matrix `com.openclaw.presentation` Metadata Contract

## Overview

This note models the `com.openclaw.presentation` Matrix metadata contract that OpenClaw attaches to outbound `m.room.message` events so OpenClaw-aware Matrix clients can render native rich UI (buttons, selects, context rows, dividers) on top of the normal plain-text reply. It mirrors the `channels/matrix-presentation` source page: the `MessagePresentation` event-content schema (`version` / `type` / `blocks`), the always-present plain-text `body` fallback, the four advertised block types, the fallback interaction semantics (values are slash/text commands, not Matrix callbacks), the relationship to the dedicated `com.openclaw.approval` metadata, and the per-media-event attachment rule. It is a data/protocol contract (model), not a setup procedure — the Matrix channel install/config lives in the sibling setup and behavior notes.

## What `com.openclaw.presentation` Is

OpenClaw can attach normalized `MessagePresentation` metadata to outbound Matrix `m.room.message` events under the `com.openclaw.presentation` key. Stock Matrix clients continue to render the plain text `body`, while OpenClaw-aware clients can read the structured metadata and render native UI such as buttons, selects, context rows, and dividers. The metadata is therefore an additive layer on a standard Matrix message event — it never replaces the text the message already carries.

## Event Content

The metadata is stored in Matrix event content alongside the standard `msgtype` and `body` fields. The example below shows a model-selection prompt where the structured `select` block in `com.openclaw.presentation` mirrors the human-readable options also written into `body`:

```json
{
  "msgtype": "m.text",
  "body": "Select model\n\n- DeepSeek: /model deepseek/deepseek-chat",
  "com.openclaw.presentation": {
    "version": 1,
    "type": "message.presentation",
    "title": "Select model",
    "tone": "info",
    "blocks": [
      {
        "type": "select",
        "placeholder": "Choose model",
        "options": [
          {
            "label": "DeepSeek",
            "value": "/model deepseek/deepseek-chat"
          }
        ]
      }
    ]
  }
}
```

Within `com.openclaw.presentation`, `version` is the Matrix presentation metadata schema version and `type` is a stable discriminator for OpenClaw-aware clients (here `"message.presentation"`). The example also carries a `title` (`"Select model"`), a `tone` (`"info"`), and a `blocks` array. Clients should ignore unknown `type` values, unknown versions they cannot safely interpret, and unknown block types — defensive parsing is part of the contract.

## Fallback Behavior

OpenClaw always renders a readable plain-text fallback into `body`. The structured metadata is additive and must not be required for basic Matrix interoperability. Unsupported clients should continue to show the fallback text, while OpenClaw-aware clients may prefer the structured metadata for display but must preserve the fallback text for copy, search, notifications, and accessibility.

## Supported Blocks

The Matrix outbound adapter advertises support for four block types: `buttons`, `select`, `context`, and `divider`. Clients should treat these blocks as best-effort presentation hints. Unknown fields and unknown block types should be ignored rather than causing the full message to fail rendering, so a newer OpenClaw emitting an unrecognized block never breaks an older aware client.

## Interactions

This metadata does not add Matrix callback semantics. Button and select option `value`s are fallback interaction payloads — usually slash commands or text commands. A Matrix client that wants to support interaction can send the selected value back to the room as a normal message. For example, a button with value `/model deepseek/deepseek-chat` can be handled by sending that value as an encrypted Matrix text message in the same room, so the interaction rides the ordinary message path rather than any custom callback channel.

## Relationship to Approval Metadata

`com.openclaw.presentation` is for general rich-message presentation. Approval prompts instead use the dedicated `com.openclaw.approval` metadata because approvals carry safety-sensitive state, decisions, and exec/plugin details. If both metadata keys are present on the same event, clients should prefer the dedicated approval renderer over the general presentation renderer.

## Media Messages

When a reply contains multiple media URLs, OpenClaw sends one Matrix event per media URL, and presentation metadata is attached only to the first media event so clients have one stable structured payload and duplicate renderers are avoided. Presentation metadata should be kept compact: large user-visible text should stay in `body` and use the normal Matrix text chunking path rather than being inflated into the structured payload.

**Source**: OpenClaw documentation — `channels/matrix-presentation` (mirror `inbox/openclaw_docs/channels/matrix-presentation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
