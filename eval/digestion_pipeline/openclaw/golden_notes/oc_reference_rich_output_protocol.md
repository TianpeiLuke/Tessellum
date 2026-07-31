---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - rich_output
keywords:
  - openclaw rich output protocol
  - mediaurl mediaurls structured media
  - audio_as_voice presentation hint
  - reply_to_current reply_to directive
  - embed shortcode control ui
  - canvas stored rendering shape
  - block streaming media payload
  - markdown image media reply
topics:
  - OpenClaw
  - Rich Output Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/rich-output-protocol
access_control_group: ["general"]
---

# OpenClaw — Rich Output Protocol

## Overview

This note models the OpenClaw **rich output protocol**: the small set of delivery/render directives an assistant output message can carry beyond plain text, mirroring the `reference/rich-output-protocol` source page. The protocol has two distinct halves: **delivery metadata** — the structured `mediaUrl` / `mediaUrls` attachment fields, the `[[audio_as_voice]]` audio-presentation hint, and the `[[reply_to_current]]` / `[[reply_to:<id>]]` reply directives — and the **web-only rich render path**, the `[embed ...]` shortcode plus the normalized/stored `canvas` content block the Control UI renders. It also covers the URL/path rules for media attachments, the prohibition on text-command attachments from tools/plugins/streaming, Markdown-image opt-in at channel adapters, and the block-streaming dedup rule.

## Directives an Assistant Message Can Carry

Assistant output can carry a small set of delivery/render directives: structured `mediaUrl` / `mediaUrls` fields for attachment delivery; `[[audio_as_voice]]` for audio presentation hints; `[[reply_to_current]]` / `[[reply_to:<id>]]` for reply metadata; and `[embed ...]` for Control UI rich rendering. These directives are separate: the structured media fields and the reply/voice tags are **delivery metadata**, while `[embed ...]` is the **web-only rich render path**.

## Media Attachment URL and Path Rules

Remote media attachments must be public `https:` URLs. Plain `http:`, loopback, link-local, private, and internal hostnames are **ignored as attachment directives**; server-side media fetchers still enforce their own network guards independently of this rule. Local media attachments can use absolute paths, workspace-relative paths, or home-relative `~/` paths; they still pass through the agent **file-read policy** and **media type checks** before delivery.

## Structured Media Fields vs Text Commands

Per the source page's `<Warning>`: do **not** emit text commands for attachments from tools, plugins, streaming blocks, browser output, or message actions — use the structured media fields instead. A valid message-tool payload carries the media on the structured `mediaUrl` field alongside the message text:

```json
{ "message": "Here is your image.", "mediaUrl": "/workspace/image.png" }
```

Legacy final assistant reply text may still be normalized for compatibility, but it is **not a general plugin/tool protocol** — new tool/plugin/streaming output must use the structured fields.

## Markdown Image Handling and Channel Opt-In

Plain Markdown image syntax stays text by default. Channels that intentionally map Markdown image replies to media attachments **opt in at their outbound adapter**; Telegram does this, so `![alt](url)` can still become a media reply on that channel. This is a per-channel decision at the outbound adapter, not a protocol-wide behavior.

## Block Streaming and Media Dedup

When **block streaming** is enabled, media must be carried on structured payload fields. If the same media URL is sent in a streamed block and then repeated in the final assistant payload, OpenClaw **delivers the attachment once and strips the duplicate** from the final payload — so an emitted-during-stream attachment is not delivered twice when the final payload also contains it.

## `[embed ...]`

`[embed ...]` is the **only** agent-facing rich render syntax for the Control UI. It is written as a self-closing shortcode:

```text
[embed ref="cv_123" title="Status" /]
```

The rules governing `[embed ...]`:

- `[view ...]` is **no longer valid** for new output.
- Embed shortcodes render in the **assistant message surface only**.
- Only **URL-backed** embeds are rendered — use `ref="..."` or `url="..."`.
- **Block-form inline HTML** embed shortcodes are not rendered.
- The web UI **strips the shortcode** from visible text and renders the embed inline.
- Structured media is **not** an embed alias and should not be used for rich embed rendering.

## Stored Rendering Shape

The normalized/stored assistant content block is a structured `canvas` item. Stored/rendered rich blocks use this `canvas` shape directly, and `present_view` is **not recognized**:

```json
{
  "type": "canvas",
  "preview": {
    "kind": "canvas",
    "surface": "assistant_message",
    "render": "url",
    "viewId": "cv_123",
    "url": "/__openclaw__/canvas/documents/cv_123/index.html",
    "title": "Status",
    "preferredHeight": 320
  }
}
```

**Source**: OpenClaw documentation — `reference/rich-output-protocol` (mirror `inbox/openclaw_docs/reference/rich-output-protocol.md`)
**Last Updated**: 2026-06-22
**Status**: Active
