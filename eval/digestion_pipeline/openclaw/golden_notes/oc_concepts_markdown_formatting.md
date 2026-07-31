---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - markdown_formatting
keywords:
  - openclaw markdown formatting
  - outbound markdown intermediate representation
  - markdownToIR renderMarkdownWithMarkers chunkMarkdownIR
  - slack mrkdwn telegram html signal style ranges
  - markdown tables code bullets off
  - utf-16 style link spans
  - add a channel formatter
  - markdown chunking rules
topics:
  - OpenClaw
  - Markdown Formatting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/markdown-formatting
access_control_group: ["general"]
---

# OpenClaw — Outbound Markdown Formatting Pipeline

## Overview

This note is the procedure for OpenClaw's **outbound Markdown formatting**: how the gateway turns agent-produced Markdown into channel-specific output. OpenClaw parses Markdown once into a shared **intermediate representation (IR)** before rendering channel-specific output; the IR keeps the source text intact while carrying style/link spans so chunking and rendering stay consistent across channels. It mirrors the `concepts/markdown-formatting` source page in full — the goals, the three-step parse → chunk → render pipeline, the IR example, where it is used, table handling (`markdown.tables`), chunking rules, per-channel link policy, spoilers, the five-step "how to add or update a channel formatter" procedure, and the common gotchas.

## Goals

The pipeline has three stated goals:

- **Consistency:** one parse step, multiple renderers.
- **Safe chunking:** split text before rendering so inline formatting never breaks across chunks.
- **Channel fit:** map the same IR to Slack mrkdwn, Telegram HTML, and Signal style ranges without re-parsing Markdown.

## Pipeline

The pipeline runs in three ordered steps:

1. **Parse Markdown -> IR.** The IR is plain text plus style spans (bold/italic/strike/code/spoiler) and link spans. Offsets are **UTF-16 code units** so Signal style ranges align with its API. Tables are parsed only when a channel opts into table conversion.
2. **Chunk IR (format-first).** Chunking happens on the IR text *before* rendering. Inline formatting does not split across chunks; spans are sliced per chunk.
3. **Render per channel.** Each channel renders from the same IR:
   - **Slack:** mrkdwn tokens (bold/italic/strike/code), links as `<url|label>`.
   - **Telegram:** HTML tags (`<b>`, `<i>`, `<s>`, `<code>`, `<pre><code>`, `<a href>`).
   - **Signal:** plain text + `text-style` ranges; links become `label (url)` when the label differs.

## IR example

For the input Markdown:

```markdown
Hello **world** - see [docs](https://docs.openclaw.ai).
```

the IR is (schematic):

```json
{
  "text": "Hello world - see docs.",
  "styles": [{ "start": 6, "end": 11, "style": "bold" }],
  "links": [{ "start": 19, "end": 23, "href": "https://docs.openclaw.ai" }]
}
```

The `text` field carries the plain rendered text; `styles` and `links` are offset spans (`start`/`end` in UTF-16 code units) layered over that text, so each renderer can reapply formatting without re-parsing the original Markdown.

## Where it is used

Slack, Telegram, and Signal outbound adapters render from the IR. Other channels (WhatsApp, iMessage, Microsoft Teams, Discord) still use plain text or their own formatting rules, with Markdown table conversion applied before chunking when enabled.

## Table handling

Markdown tables are not consistently supported across chat clients, so OpenClaw exposes `markdown.tables` to control conversion per channel (and per account). The three modes are:

- `code`: render tables as code blocks (default for most channels).
- `bullets`: convert each row into bullet points (default for Matrix, Signal, and WhatsApp).
- `off`: disable table parsing and conversion; raw table text passes through.

The config keys nest under `channels.<channel>.markdown.tables`, and a per-account override nests under `channels.<channel>.accounts.<account>.markdown.tables`:

```yaml
channels:
  discord:
    markdown:
      tables: code
    accounts:
      work:
        markdown:
          tables: off
```

## Chunking rules

Chunking obeys these rules so inline formatting survives the split:

- Chunk limits come from channel adapters/config and are applied to the IR text.
- Code fences are preserved as a single block with a trailing newline so channels render them correctly.
- List prefixes and blockquote prefixes are part of the IR text, so chunking does not split mid-prefix.
- Inline styles (bold/italic/strike/inline-code/spoiler) are never split across chunks; the renderer reopens styles inside each chunk.

For more on chunking behavior across channels, the source page points to [Streaming + chunking](https://docs.openclaw.ai/concepts/streaming).

## Link policy

Link rendering is channel-specific:

- **Slack:** `[label](url)` -> `<url|label>`; bare URLs remain bare. Autolink is disabled during parse to avoid double-linking.
- **Telegram:** `[label](url)` -> `<a href="url">label</a>` (HTML parse mode).
- **Signal:** `[label](url)` -> `label (url)` unless the label matches the URL.

## Spoilers

Spoiler markers (`||spoiler||`) are parsed only for Signal, where they map to SPOILER style ranges. Other channels treat them as plain text.

## How to add or update a channel formatter

Adding or updating a channel formatter is a five-step procedure:

1. **Parse once:** use the shared `markdownToIR(...)` helper with channel-appropriate options (autolink, heading style, blockquote prefix).
2. **Render:** implement a renderer with `renderMarkdownWithMarkers(...)` and a style marker map (or Signal style ranges).
3. **Chunk:** call `chunkMarkdownIR(...)` before rendering; render each chunk.
4. **Wire adapter:** update the channel outbound adapter to use the new chunker and renderer.
5. **Test:** add or update format tests and an outbound delivery test if the channel uses chunking.

## Common gotchas

The source page calls out these recurring mistakes:

- Slack angle-bracket tokens (`<@U123>`, `<#C123>`, `<https://...>`) must be preserved; escape raw HTML safely.
- Telegram HTML requires escaping text outside tags to avoid broken markup.
- Signal style ranges depend on UTF-16 offsets; do not use code point offsets.
- Preserve trailing newlines for fenced code blocks so closing markers land on their own line.

**Source**: OpenClaw documentation — `concepts/markdown-formatting` (mirror `inbox/openclaw_docs/concepts/markdown-formatting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
