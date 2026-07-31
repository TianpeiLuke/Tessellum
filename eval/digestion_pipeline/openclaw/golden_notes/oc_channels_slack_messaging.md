---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - slack
keywords:
  - openclaw slack messaging
  - slack threading sessions reply tags
  - slack ack reaction ackreactionscope
  - channels.slack.streaming partial block progress
  - slack typing reaction fallback
  - slack media chunking textchunklimit
  - slack attachment vision mediamaxmb
  - slack thread_ts session suffix
topics:
  - OpenClaw
  - Slack Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/slack
access_control_group: ["general"]
---

# OpenClaw — Slack Channel Messaging Runtime (Threading, Reactions, Streaming, Media, Vision)

## Overview

This note documents the Slack channel's messaging-runtime behavior in OpenClaw once setup and access control are configured: how Slack threads map to agent sessions and how reply tags are honored, the acknowledgement-reaction emoji and its scope, live text-streaming preview modes, the typing-reaction fallback, inbound/outbound media chunking and delivery, and the full attachment-vision inbound pipeline (supported types, size/download/model limits, known limits). It mirrors the `channels/slack` source page sections from "Threading, sessions, and reply tags" through "Attachment vision reference." Setup/transport is covered in `oc_channels_slack_setup`, the token/access model in `oc_channels_slack_security_access`, and slash/interactivity/config/troubleshooting in `oc_channels_slack_interactivity`.

## Threading, Sessions, and Reply Tags

Slack routes by conversation type: DMs route as `direct`, channels as `channel`, and MPIMs (multi-person IMs / group DMs) as `group`. Slack route bindings accept raw peer IDs plus Slack target forms such as `channel:C12345678`, `user:U12345678`, and `<@U12345678>`. With the default `session.dmScope=main`, Slack DMs collapse to the agent main session, while channel sessions use the key `agent:<agentId>:slack:channel:<channelId>`.

Ordinary top-level channel messages stay on the per-channel session even when `replyToMode` is non-`off`. Slack thread replies use the parent Slack `thread_ts` for session suffixes (`:thread:<threadTs>`), even when outbound reply threading is disabled with `replyToMode="off"`. OpenClaw seeds an eligible top-level channel root into `agent:<agentId>:slack:channel:<channelId>:thread:<rootTs>` when that root is expected to start a visible Slack thread, so the root and later thread replies share one OpenClaw session. This applies to `app_mention` events, explicit bot or configured mention-pattern matches, and `requireMention: false` channels with non-`off` `replyToMode`.

Thread history is governed by three keys: `channels.slack.thread.historyScope` default is `thread`; `channels.slack.thread.inheritParent` default is `false`; and `channels.slack.thread.initialHistoryLimit` controls how many existing thread messages are fetched when a new thread session starts (default `20`; set `0` to disable). `channels.slack.thread.requireExplicitMention` (default `false`): when `true`, it suppresses implicit thread mentions so the bot only responds to explicit `@bot` mentions inside threads, even when the bot already participated in the thread. Without it, replies in a bot-participated thread bypass `requireMention` gating.

Reply threading controls are `channels.slack.replyToMode` (`off|first|all|batched`, default `off`), `channels.slack.replyToModeByChatType` (per `direct|group|channel`), and the legacy fallback for direct chats `channels.slack.dm.replyToMode`. Manual reply tags are supported: `[[reply_to_current]]` and `[[reply_to:<id>]]`. For explicit Slack thread replies from the `message` tool, set `replyBroadcast: true` with `action: "send"` and `threadId` or `replyTo` to ask Slack to also broadcast the thread reply to the parent channel; this maps to Slack's `chat.postMessage` `reply_broadcast` flag and is only supported for text or Block Kit sends, not media uploads. When a `message` tool call runs inside a Slack thread and targets the same channel, OpenClaw normally inherits the current Slack thread according to `replyToMode`; set `topLevel: true` on `action: "send"` or `action: "upload-file"` to force a new parent-channel message instead, and `threadId: null` is accepted as the same top-level opt-out.

Note that `replyToMode="off"` disables outbound Slack reply threading, including explicit `[[reply_to_*]]` tags, but it does not flatten inbound Slack thread sessions: messages already posted inside a Slack thread still route to the `:thread:<threadTs>` session. This differs from Telegram, where explicit tags are still honored in `"off"` mode; Slack threads hide messages from the channel while Telegram replies stay visible inline.

## Ack Reactions

`ackReaction` sends an acknowledgement emoji while OpenClaw is processing an inbound message, and `ackReactionScope` decides *when* that emoji is actually sent.

### Emoji (`ackReaction`)

The resolution order is `channels.slack.accounts.<accountId>.ackReaction`, then `channels.slack.ackReaction`, then `messages.ackReaction`, then the agent identity emoji fallback (`agents.list[].identity.emoji`, else `"eyes"` / 👀). Slack expects shortcodes (for example `"eyes"`). Use `""` to disable the reaction for the Slack account or globally.

### Scope (`messages.ackReactionScope`)

The Slack provider reads scope from `messages.ackReactionScope` (default `"group-mentions"`). There is no Slack-account or Slack-channel-level override today; the value is global to the gateway. The values are: `"all"` (react in DMs and groups); `"direct"` (react in DMs only); `"group-all"` (react on every group message, no DMs); `"group-mentions"` (default — react in groups, but only when the bot is mentioned or in group mentionables that opted in, with DMs excluded); and `"off"` / `"none"` (never react). Because the default scope (`"group-mentions"`) does not fire ack reactions in direct messages, set `messages.ackReactionScope` to `"direct"` or `"all"` to see the configured `ackReaction` on inbound Slack DMs. `messages.ackReactionScope` is read at Slack provider startup, so a gateway restart is needed for the change to take effect.

```json5
{
  messages: {
    ackReaction: "eyes",
    ackReactionScope: "all", // react in DMs and groups
  },
}
```

## Text Streaming

`channels.slack.streaming` controls live preview behavior. The modes are: `off` (disable live preview streaming); `partial` (default — replace preview text with the latest partial output); `block` (append chunked preview updates); and `progress` (show progress status text while generating, then send final text). Two sub-keys refine this: `streaming.preview.toolProgress` (when draft preview is active, route tool/progress updates into the same edited preview message; default `true`; set `false` to keep separate tool/progress messages) and `streaming.preview.commandText` / `streaming.progress.commandText` (set to `status` to keep compact tool-progress lines while hiding raw command/exec text; default `raw`).

```json
{
  "channels": {
    "slack": {
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

`channels.slack.streaming.nativeTransport` controls Slack native text streaming when `channels.slack.streaming.mode` is `partial` (default `true`). Slack native progress task cards are opt-in for progress mode: set `channels.slack.streaming.progress.nativeTaskCards` to `true` with `channels.slack.streaming.mode="progress"` to send a Slack-native plan/task card while work is running, then update the same task card at completion; without this flag, progress mode keeps the portable draft-preview behavior.

Native streaming has constraints. A reply thread must be available for native text streaming and Slack assistant thread status to appear (thread selection still follows `replyToMode`). Channel, group-chat, and top-level DM roots can still use the normal draft preview when native streaming is unavailable or no reply thread exists. Top-level Slack DMs stay off-thread by default, so they do not show Slack's thread-style native stream/status preview; OpenClaw posts and edits a draft preview in the DM instead. Media and non-text payloads fall back to normal delivery; media/error finals cancel pending preview edits while eligible text/block finals flush only when they can edit the preview in place; and if streaming fails mid-reply, OpenClaw falls back to normal delivery for remaining payloads.

```json5
{
  channels: {
    slack: {
      streaming: {
        mode: "partial",
        nativeTransport: false, // use draft preview instead of Slack native streaming
      },
    },
  },
}
```

Several legacy aliases still read for compatibility: `channels.slack.streamMode` (`replace | status_final | append`) is a legacy runtime alias for `channels.slack.streaming.mode`; boolean `channels.slack.streaming` is a legacy alias for `channels.slack.streaming.mode` and `channels.slack.streaming.nativeTransport`; and legacy `channels.slack.nativeStreaming` is a runtime alias for `channels.slack.streaming.nativeTransport`. Run `openclaw doctor --fix` to rewrite persisted Slack streaming config to the canonical keys.

## Typing Reaction Fallback

`typingReaction` adds a temporary reaction to the inbound Slack message while OpenClaw is processing a reply, then removes it when the run finishes. This is most useful outside of thread replies, which use a default "is typing..." status indicator. The resolution order is `channels.slack.accounts.<accountId>.typingReaction` then `channels.slack.typingReaction`. Slack expects shortcodes (for example `"hourglass_flowing_sand"`). The reaction is best-effort and cleanup is attempted automatically after the reply or failure path completes.

## Media, Chunking, and Delivery

**Inbound attachments.** Slack file attachments are downloaded from Slack-hosted private URLs (a token-authenticated request flow) and written to the media store when fetch succeeds and size limits permit. File placeholders include the Slack `fileId` so agents can fetch the original file with `download-file`. Downloads use bounded idle and total timeouts; if Slack file retrieval stalls or fails, OpenClaw keeps processing the message and falls back to the file placeholder. The runtime inbound size cap defaults to `20MB` unless overridden by `channels.slack.mediaMaxMb`.

**Outbound text and files.** Text chunks use `channels.slack.textChunkLimit` (default `4000`); `channels.slack.chunkMode="newline"` enables paragraph-first splitting; file sends use Slack upload APIs and can include thread replies (`thread_ts`); and the outbound media cap follows `channels.slack.mediaMaxMb` when configured, otherwise channel sends use MIME-kind defaults from the media pipeline.

**Delivery targets.** The preferred explicit targets are `user:<id>` for DMs and `channel:<id>` for channels. Text/block-only Slack DMs can post directly to user IDs; file uploads and threaded sends open the DM via Slack conversation APIs first because those paths require a concrete conversation ID.

## Attachment Vision Reference

Slack can attach downloaded media to the agent turn when Slack file downloads succeed and size limits permit. Image files can be passed through the media understanding path or directly to a vision-capable reply model; other files are retained as downloadable file context rather than treated as image input.

### Supported Media Types

| Media type | Source | Current behavior | Notes |
| --- | --- | --- | --- |
| JPEG / PNG / GIF / WebP images | Slack file URL | Downloaded and attached to the turn for vision-capable handling | Per-file cap: `channels.slack.mediaMaxMb` (default 20 MB) |
| PDF files | Slack file URL | Downloaded and exposed as file context for tools such as `download-file` or `pdf` | Slack inbound does not convert PDFs into image-vision input automatically |
| Other files | Slack file URL | Downloaded when possible and exposed as file context | Binary files are not treated as image input |
| Thread replies | Thread starter files | Root-message files can be hydrated as context when the reply has no direct media | File-only starters use an attachment placeholder |
| Multi-image messages | Multiple Slack files | Each file is evaluated independently | Slack processing is capped at eight files per message |

### Inbound Pipeline

When a Slack message with file attachments arrives: (1) OpenClaw downloads the file from Slack's private URL using the bot token; (2) the file is written to the media store on success; (3) downloaded media paths and content types are added to the inbound context; (4) image-capable model/tool paths can use image attachments from that context; and (5) non-image files remain available as file metadata or media references for tools that can handle them.

### Thread-Root Attachment Inheritance

When a message arrives in a thread (has a `thread_ts` parent): if the reply itself has no direct media and the included root message has files, Slack can hydrate the root files as thread-starter context; direct reply attachments take precedence over root-message attachments; and a root message that has only files and no text is represented with an attachment placeholder so the fallback can still include its files.

### Multi-Attachment Handling

When a single Slack message contains multiple file attachments: each attachment is processed independently through the media pipeline; downloaded media references are aggregated into the message context; processing order follows Slack's file order in the event payload; and a failure in one attachment's download does not block others.

### Size, Download, and Model Limits

The **size cap** defaults to 20 MB per file and is configurable via `channels.slack.mediaMaxMb`. For **download failures**, files that Slack cannot serve, expired URLs, inaccessible files, oversize files, and Slack auth/login HTML responses are skipped instead of being reported as unsupported formats. For the **vision model**, image analysis uses the active reply model when it supports vision, or the image model configured at `agents.defaults.imageModel`.

### Known Limits

| Scenario | Current behavior | Workaround |
| --- | --- | --- |
| Expired Slack file URL | File skipped; no error shown | Re-upload the file in Slack |
| Vision model not configured | Image attachments are stored as media references, but not analyzed as images | Configure `agents.defaults.imageModel` or use a vision-capable reply model |
| Very large images (> 20 MB by default) | Skipped per size cap | Increase `channels.slack.mediaMaxMb` if Slack allows |
| Forwarded/shared attachments | Text and Slack-hosted image/file media are best-effort | Re-share directly in the OpenClaw thread |
| PDF attachments | Stored as file/media context, not automatically routed through image vision | Use `download-file` for file metadata or the `pdf` tool for PDF analysis |

**Source**: OpenClaw documentation — `channels/slack` (mirror `inbox/openclaw_docs/channels/slack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
