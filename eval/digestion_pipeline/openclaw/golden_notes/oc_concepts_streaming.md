---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - streaming
keywords:
  - openclaw streaming
  - block streaming channel messages
  - preview streaming modes
  - EmbeddedBlockChunker chunking
  - blockStreamingDefault blockStreamingBreak
  - coalescing human-like pacing
  - tool-progress preview updates
  - channels streaming mode mapping
topics:
  - OpenClaw
  - Streaming
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/streaming
access_control_group: ["general"]
---

# OpenClaw — Streaming and Chunking

## Overview

This note describes OpenClaw's two separate outbound streaming layers, mirroring the `concepts/streaming` source page. **Block streaming** emits completed assistant blocks as normal channel messages while the assistant writes, and **preview streaming** updates a temporary preview message (on Telegram/Discord/Slack and others) during generation. A key fact: there is **no true token-delta streaming** to channel messages today — preview streaming is message-based (send + edits/appends). It covers block-stream controls and boundary semantics, the `EmbeddedBlockChunker` algorithm, coalescing, human-like pacing, the "stream chunks or everything" mapping, the four preview-streaming modes (per-channel mapping plus runtime behavior), and tool-progress preview updates.

## Block Streaming (channel messages)

Block streaming sends assistant output in coarse chunks as it becomes available — completed **blocks** emitted as normal channel messages (not token deltas). Model output produces `text_delta`/events; depending on `blockStreamingBreak`, the chunker either emits blocks as the buffer grows (`text_end`) or flushes buffered output once the assistant message finishes (`message_end`), then sends to the channel as block replies:

```
Model output
  └─ text_delta/events
       ├─ (blockStreamingBreak=text_end)
       │    └─ chunker emits blocks as buffer grows
       └─ (blockStreamingBreak=message_end)
            └─ chunker flushes at message_end
                   └─ channel send (block replies)
```

In the legend, `text_delta/events` are model stream events (may be sparse for non-streaming models), `chunker` is the `EmbeddedBlockChunker` applying min/max bounds plus break preference, and `channel send` is the outbound block replies.

**Controls** (config keys, verbatim):

- `agents.defaults.blockStreamingDefault`: `"on"`/`"off"` (default off).
- Channel overrides: `*.blockStreaming` (and per-account variants) to force `"on"`/`"off"` per channel.
- `agents.defaults.blockStreamingBreak`: `"text_end"` or `"message_end"`.
- `agents.defaults.blockStreamingChunk`: `{ minChars, maxChars, breakPreference? }`.
- `agents.defaults.blockStreamingCoalesce`: `{ minChars?, maxChars?, idleMs? }` (merge streamed blocks before send).
- Channel hard cap: `*.textChunkLimit` (e.g., `channels.whatsapp.textChunkLimit`).
- Channel chunk mode: `*.chunkMode` (`length` default, `newline` splits on blank lines / paragraph boundaries before length chunking).
- Discord soft cap: `channels.discord.maxLinesPerMessage` (default 17) splits tall replies to avoid UI clipping.

**Boundary semantics:** `text_end` streams blocks as soon as the chunker emits, flushing on each `text_end`; `message_end` waits until the assistant message finishes, then flushes the buffered output. `message_end` still uses the chunker if the buffered text exceeds `maxChars`, so it can emit multiple chunks at the end.

### Media delivery with block streaming

Streaming media must use structured payload fields such as `mediaUrl` or `mediaUrls`; streamed text is not parsed as an attachment command. When block streaming sends media early, OpenClaw remembers that delivery for the turn, and if the final assistant payload repeats the same media URL, the final delivery strips the duplicate media instead of sending the attachment again. Exact duplicate final payloads are suppressed; if the final payload adds distinct text around media that was already streamed, OpenClaw still sends the new text while keeping the media single-delivery. This prevents duplicate voice notes or files on channels such as Telegram.

## Chunking Algorithm (low/high bounds)

Block chunking is implemented by `EmbeddedBlockChunker`:

- **Low bound:** don't emit until buffer `>= minChars` (unless forced).
- **High bound:** prefer splits before `maxChars`; if forced, split at `maxChars`.
- **Break preference:** `paragraph` → `newline` → `sentence` → `whitespace` → hard break.
- **Code fences:** never split inside fences; when forced at `maxChars`, close + reopen the fence to keep Markdown valid.

`maxChars` is clamped to the channel `textChunkLimit`, so you can't exceed per-channel caps.

## Coalescing (merge streamed blocks)

When block streaming is enabled, OpenClaw can **merge consecutive block chunks** before sending them out, reducing "single-line spam" while still providing progressive output. Coalescing waits for **idle gaps** (`idleMs`) before flushing; buffers are capped by `maxChars` and will flush if they exceed it; `minChars` prevents tiny fragments from sending until enough text accumulates (the final flush always sends remaining text). The joiner is derived from `blockStreamingChunk.breakPreference` (`paragraph` → `\n\n`, `newline` → `\n`, `sentence` → space). Channel overrides are available via `*.blockStreamingCoalesce` (including per-account configs), and the default coalesce `minChars` is bumped to 1500 for Signal/Slack/Discord unless overridden.

## Human-like Pacing Between Blocks

When block streaming is enabled, you can add a **randomized pause** between block replies (after the first block) to make multi-bubble responses feel more natural. The config key is `agents.defaults.humanDelay` (override per agent via `agents.list[].humanDelay`). Modes are `off` (default), `natural` (800-2500ms), and `custom` (`minMs`/`maxMs`). The pause applies only to **block replies**, not final replies or tool summaries.

## "Stream Chunks or Everything"

This intent maps to the following config combinations:

- **Stream chunks:** `blockStreamingDefault: "on"` + `blockStreamingBreak: "text_end"` (emit as you go). Non-Telegram channels also need `*.blockStreaming: true`.
- **Stream everything at end:** `blockStreamingBreak: "message_end"` (flush once, possibly multiple chunks if very long).
- **No block streaming:** `blockStreamingDefault: "off"` (only final reply).

Block streaming is **off unless** `*.blockStreaming` is explicitly set to `true`; channels can stream a live preview (`channels.<channel>.streaming`) without block replies. As a config-location reminder, the `blockStreaming*` defaults live under `agents.defaults`, not the root config.

## Preview Streaming Modes

The canonical key is `channels.<channel>.streaming`, with four modes: `off` disables preview streaming; `partial` shows a single preview that is replaced with the latest text; `block` updates the preview in chunked/appended steps; and `progress` shows a progress/status preview during generation, with the final answer at completion. `streaming.mode: "block"` is a preview-streaming mode for edit-capable channels such as Discord and Telegram — it does not enable channel block delivery there; use `streaming.block.enabled` or the legacy `blockStreaming` channel key when you want normal block replies. Microsoft Teams is the exception: it has no draft-preview block transport, so `streaming.mode: "block"` maps to Teams block delivery instead of native partial/progress streaming.

### Channel mapping

| Channel    | `off` | `partial` | `block` | `progress`              |
| ---------- | ----- | --------- | ------- | ----------------------- |
| Telegram   | ✅    | ✅        | ✅      | editable progress draft |
| Discord    | ✅    | ✅        | ✅      | editable progress draft |
| Slack      | ✅    | ✅        | ✅      | ✅                      |
| Mattermost | ✅    | ✅        | ✅      | ✅                      |
| MS Teams   | ✅    | ✅        | ✅      | native progress stream  |

Slack-only behavior: `channels.slack.streaming.nativeTransport` toggles Slack native streaming API calls when `channels.slack.streaming.mode="partial"` (default `true`). Slack native streaming and Slack assistant thread status require a reply thread target; top-level DMs do not show that thread-style preview, but they can still use Slack draft preview posts and edits.

Legacy key migration: Telegram legacy `streamMode` and scalar/boolean `streaming` values are detected and migrated by doctor/config compatibility paths to `streaming.mode`. Discord `streamMode` + boolean `streaming` remain runtime aliases for the `streaming` enum. Slack `streamMode` remains a runtime alias for `streaming.mode`, boolean `streaming` remains a runtime alias for `streaming.mode` plus `streaming.nativeTransport`, and legacy `nativeStreaming` remains a runtime alias for `streaming.nativeTransport`. Run `openclaw doctor --fix` to rewrite persisted config.

### Runtime behavior

**Telegram:** uses `sendMessage` + `editMessageText` preview updates across DMs and group/topics; final text edits the active preview in place, and long finals reuse that message for the first chunk and send only the remaining chunks. `block` mode rotates the preview into a new message at `streaming.preview.chunk.maxChars` (default 800, capped at Telegram's 4096 edit limit); other modes grow one preview up to 4096 characters. `progress` mode keeps tool progress in an editable status draft, clears it at completion, and sends the final answer through normal delivery. If the final edit fails before the completed text is confirmed, OpenClaw uses normal final delivery and cleans up the stale preview; preview streaming is skipped when Telegram block streaming is explicitly enabled (to avoid double-streaming); and `/reasoning stream` can write reasoning to a transient preview deleted after final delivery.

**Discord:** uses send + edit preview messages; `block` mode uses draft chunking (`draftChunk`); preview streaming is skipped when Discord block streaming is explicitly enabled; final media, error, and explicit-reply payloads cancel pending previews without flushing a new draft, then use normal delivery.

**Matrix:** draft previews finalize in place when the final text can reuse the preview event; media-only, error, and reply-target-mismatch finals cancel pending preview updates before normal delivery, and an already-visible stale preview is redacted.

**Slack:** `partial` can use Slack native streaming (`chat.startStream`/`append`/`stop`) when available; `block` uses append-style draft previews; `progress` uses status preview text, then final answer. Top-level DMs without a reply thread use draft preview posts and edits instead of Slack native streaming; native and draft preview streaming suppress block replies for that turn (so a Slack reply is streamed by one delivery path only); final media/error payloads and progress finals do not create throwaway draft messages — only text/block finals that can edit the preview flush pending draft text.

**Mattermost:** streams thinking, tool activity, and partial reply text into a single draft preview post that finalizes in place when the final answer is safe to send; falls back to sending a fresh final post if the preview post was deleted or otherwise unavailable at finalize time; final media/error payloads cancel pending preview updates before normal delivery instead of flushing a temporary preview post.

### Tool-progress preview updates

Preview streaming can also include **tool-progress** updates — short status lines like "searching the web", "reading file", or "calling tool" — that appear in the same preview message while tools are running, ahead of the final reply. In Codex app-server mode, Codex preamble/commentary messages use this same preview path, so short "I am checking..." progress notes stream into the editable draft without becoming part of the final answer, keeping multi-step tool turns visually alive rather than silent. Long-running tools may emit typed progress before they return: for example, `web_fetch` arms a five-second timer when it starts — if the fetch is still pending, the preview can show `Fetching page content...`; if it finishes or is canceled before then, no progress line is emitted, and the later final tool result is still delivered normally to the model.

Supported surfaces and policy: **Discord**, **Slack**, **Telegram**, and **Matrix** stream tool-progress and Codex preamble updates into the live preview edit by default when preview streaming is active, while Microsoft Teams uses its native progress stream in personal chats. Telegram has shipped with tool-progress preview updates enabled since `v2026.4.22`, and **Mattermost** already folds tool activity into its single draft preview post. Tool-progress edits follow the active preview streaming mode; they are skipped when preview streaming is `off` or when block streaming has taken over the message. On Telegram, `streaming.mode: "off"` is final-only, so generic progress chatter is also suppressed instead of being delivered as standalone status messages, while approval prompts, media payloads, and errors still route normally. To keep preview streaming but hide tool-progress lines, set `streaming.preview.toolProgress` to `false` for that channel; to keep tool-progress lines visible while hiding command/exec text, set `streaming.preview.commandText` to `"status"` or `streaming.progress.commandText` to `"status"` (the default is `"raw"`). This policy is shared by draft/progress channels using OpenClaw's compact progress renderer, including Discord, Matrix, Microsoft Teams, Mattermost, Slack draft previews, and Telegram; to disable preview edits entirely, set `streaming.mode` to `off`. Telegram selected quote replies are an exception: when `replyToMode` is not `"off"` and selected quote text is present, OpenClaw skips the answer preview stream for that turn so tool-progress preview lines cannot render, while current-message replies without selected quote text still keep preview streaming.

To keep progress lines visible but hide raw command/exec text:

```json
{
  "channels": {
    "telegram": {
      "streaming": {
        "mode": "partial",
        "preview": {
          "toolProgress": true,
          "commandText": "status"
        }
      }
    }
  }
}
```

Use the same shape under another compact progress channel key, for example `channels.discord`, `channels.matrix`, `channels.msteams`, `channels.mattermost`, or Slack draft previews. For progress-draft mode, put the same policy under `streaming.progress`:

```json
{
  "channels": {
    "telegram": {
      "streaming": {
        "mode": "progress",
        "progress": {
          "toolProgress": true,
          "commandText": "status"
        }
      }
    }
  }
}
```

**Source**: OpenClaw documentation — `concepts/streaming` (mirror `inbox/openclaw_docs/concepts/streaming.md`)
**Last Updated**: 2026-06-22
**Status**: Active
