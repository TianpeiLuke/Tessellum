---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - media
keywords:
  - openclaw image media support
  - whatsapp web baileys media
  - openclaw message send --media
  - media understanding caps
  - inbound media to commands
  - mediapath mediaurl templating
  - auto-reply media fan-out
  - per-type send caps
topics:
  - OpenClaw
  - Node Media Pipeline
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes/images
access_control_group: ["general"]
---

# OpenClaw — Image and Media Send/Reply Pipeline (WhatsApp Web)

## Overview

This note is the procedure for OpenClaw's **image and media handling** on the WhatsApp channel, which runs via **Baileys Web** — mirroring the `nodes/images` source page. It covers the `openclaw message send --media` CLI surface, the WhatsApp Web channel send flow (media-kind detection, per-type payload building and recompression), the auto-reply media fan-out, the inbound-media-to-command templating (`{{MediaPath}}` / `{{MediaUrl}}` plus the per-session Docker sandbox rewrite), and the two distinct caps that govern the pipeline: outbound send caps and media-understanding (transcription/description) caps.

The page documents the rules for three audiences in one media pipeline: **send** (CLI/channel outbound), **gateway** (download/understanding/templating of inbound media), and **agent replies** (auto-reply media). The WhatsApp channel-specific limits and behaviors (image/audio/video/document caps, GIF playback, MIME detection order) are recorded verbatim below.

## Goals

The page states three goals for the media pipeline:

- Send media with optional captions via `openclaw message send --media`.
- Allow auto-replies from the web inbox to include media alongside text.
- Keep per-type limits sane and predictable.

## CLI Surface

The outbound send command is `openclaw message send --media <path-or-url> [--message <caption>]`:

- `--media` is optional; the caption can be empty for media-only sends.
- `--dry-run` prints the resolved payload.
- `--json` emits `{ channel, to, messageId, mediaUrl, caption }`.

## WhatsApp Web Channel Behavior

The channel accepts a local file path **or** an HTTP(S) URL as input. The flow loads the input into a Buffer, detects the media kind, and builds the correct payload per type:

- **Images:** resize & recompress to JPEG (max side 2048px) targeting `channels.whatsapp.mediaMaxMb` (default: 50 MB).
- **Audio/Voice/Video:** pass-through up to 16 MB; audio is sent as a voice note (`ptt: true`).
- **Documents:** anything else, up to 100 MB, with filename preserved when available.

Additional channel rules: WhatsApp GIF-style playback is achieved by sending an MP4 with `gifPlayback: true` (CLI: `--gif-playback`) so mobile clients loop it inline. MIME detection prefers magic bytes, then headers, then file extension. The caption comes from `--message` or `reply.text`; an empty caption is allowed. For logging, non-verbose output shows `↩️`/`✅`, while verbose includes size and source path/URL.

## Auto-Reply Pipeline

The auto-reply path lets web-inbox replies carry media: `getReplyFromConfig` returns `{ text?, mediaUrl?, mediaUrls? }`. When media is present, the web sender resolves local paths or URLs using the same pipeline as `openclaw message send`. Multiple media entries are sent **sequentially** if provided.

## Inbound Media To Commands

When inbound web messages include media, OpenClaw downloads the media to a temp file and exposes two templating variables — `{{MediaUrl}}` (a pseudo-URL for the inbound media) and `{{MediaPath}}` (the local temp path written before running the command). When a per-session Docker sandbox is enabled, inbound media is copied into the sandbox workspace and `MediaPath`/`MediaUrl` are rewritten to a relative path like `media/inbound/<filename>`.

Media understanding (if configured via `tools.media.*` or shared `tools.media.models`) runs **before templating** and can insert `[Image]`, `[Audio]`, and `[Video]` blocks into `Body`. Within that step: audio sets `{{Transcript}}` and uses the transcript for command parsing so slash commands still work; video and image descriptions preserve any caption text for command parsing; and if the active primary image model already supports vision natively, OpenClaw skips the `[Image]` summary block and passes the original image to the model instead. By default only the first matching image/audio/video attachment is processed; set `tools.media.<cap>.attachments` to process multiple attachments.

## Limits and Errors

The page separates two distinct cap families.

**Outbound send caps (WhatsApp web send):** images go up to `channels.whatsapp.mediaMaxMb` (default: 50 MB) after recompression; audio/voice/video have a 16 MB cap; documents have a 100 MB cap. Oversize or unreadable media produces a clear error in logs and the reply is skipped.

**Media understanding caps (transcription/description):** image default is 10 MB (`tools.media.image.maxBytes`); audio default is 20 MB (`tools.media.audio.maxBytes`); video default is 50 MB (`tools.media.video.maxBytes`). Oversize media skips understanding, but replies still go through with the original body.

## Notes for Tests

The page lists test expectations: cover send + reply flows for image/audio/document cases; validate recompression for images (size bound) and the voice-note flag for audio; and ensure multi-media replies fan out as sequential sends.

**Source**: OpenClaw documentation — `nodes/images` (mirror `inbox/openclaw_docs/nodes/images.md`)
**Last Updated**: 2026-06-22
**Status**: Active
