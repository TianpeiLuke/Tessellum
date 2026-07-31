---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - progress_drafts
keywords:
  - openclaw progress drafts
  - streaming mode progress
  - progress draft labels
  - toolProgressDetail explain raw
  - progress maxLines maxLineChars
  - slack block kit render rich
  - progress draft finalization fallback
  - scheduleToolProgress tool progress
topics:
  - OpenClaw
  - Progress Drafts
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/progress-drafts
access_control_group: ["general"]
---

# OpenClaw — Configuring Progress Drafts

## Overview

This note is the procedure for configuring OpenClaw **progress drafts** — one visible work-in-progress chat message that OpenClaw creates after a turn proves it is doing real work, updates while the agent reads, plans, calls tools, or waits for approval, and then turns into the final answer when the channel can do so safely. It mirrors the `concepts/progress-drafts` source page end to end: the `streaming.mode: "progress"` quick start, what users see (label + progress lines), choosing among the `off` / `partial` / `block` / `progress` modes, configuring labels (`auto` pool, fixed, custom pool, hidden), controlling progress lines (`toolProgressDetail`, `maxLines`, `maxLineChars`, `render: "rich"`, `toolProgress: false`, the in-tool `scheduleToolProgress` pattern), per-channel transport behavior, finalization and its safety fallback, and troubleshooting. All config keys and code are copied verbatim from the mirror.

## Quick Start

Enable progress drafts per channel by setting `streaming.mode: "progress"` under the channel block. The minimal config is usually enough:

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
      },
    },
  },
}
```

With only that set, OpenClaw picks an automatic one-word label, waits until work lasts at least five seconds or emits a second work event, adds compact progress lines while useful work happens, and suppresses duplicate standalone progress chatter for that turn. The progress draft is created only after the turn proves it is doing real work, so quick or text-only replies stay clean.

## What Users See

A progress draft has two parts. The **Label** is a short starter/status line such as `Working` or `Shelling`. **Progress lines** are compact run updates that use the same tool icons and detail formatter as verbose output. The label appears after the agent starts meaningful work and either remains busy for five seconds or emits a second work event; it is part of the rolling progress-line list, so the starter status scrolls away once enough concrete work appears. Plain text-only replies do not show a progress draft.

Progress lines are added only when the agent emits useful work updates — for example `🛠️ Bash: run tests`, `🔎 Web Search: for "discord edit message"`, or `✍️ Write: to /tmp/file`. By default they use the same compact explain mode as `/verbose`; set `agents.defaults.toolProgressDetail: "raw"` when debugging and you also want raw commands/details appended. The final answer replaces the draft when possible; otherwise OpenClaw sends the final answer normally and cleans up or stops updating the draft according to the channel's transport.

## Choose a Mode

`channels.<channel>.streaming.mode` controls the visible in-progress behavior. The four modes and what each produces in chat:

| Mode | Best for | What appears in chat |
| --- | --- | --- |
| `off` | Quiet channels | Only the final answer. |
| `partial` | Watching answer text appear | One draft edited with the latest answer text. |
| `block` | Larger answer-preview chunks | One preview updated or appended in bigger chunks. |
| `progress` | Tool-heavy or long-running turns | One status draft, then the final answer. |

Choose `progress` when users care more about "what is happening" than watching the answer text stream token by token. Choose `partial` when the answer itself is the progress signal. Choose `block` when you want draft preview updates in larger text chunks. On Discord and Telegram, `streaming.mode: "block"` is still preview streaming, not normal block delivery — use `streaming.block.enabled` or legacy `blockStreaming` when you want normal block replies.

## Configure Labels

Progress labels live under `channels.<channel>.streaming.progress`. The default label is `auto`, which chooses from OpenClaw's built-in single-word label pool: `Working`, `Shelling`, `Scuttling`, `Clawing`, `Pinching`, `Molting`, `Bubbling`, `Tiding`, `Reefing`, `Cracking`, `Sifting`, `Brining`, `Nautiling`, `Krilling`, `Barnacling`, `Lobstering`, `Tidepooling`, `Pearling`, `Snapping`, `Surfacing`.

To use a fixed label, set `progress.label` to a string; to use your own automatic pool, keep `label: "auto"` and supply a `labels` array; to hide the label and show only progress lines, set `label: false`:

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          label: "Investigating",
        },
      },
    },
  },
}
```

The custom-pool form sets `label: "auto"` alongside `labels: ["Checking", "Reading", "Testing", "Finishing"]`, and the hidden-label form sets `label: false` (which shows only progress lines).

## Control Progress Lines

Progress lines are enabled by default in progress mode. They come from real run events: tool starts, item updates, task plans, approvals, command output, patch summaries, and similar agent activity. Tools can also emit **typed progress** while a single tool call is still running — that is how a slow fetch or search can update the visible draft before the tool returns its final result. The progress update is a partial tool result with empty model content and explicit public channel metadata:

```json
{
  "content": [],
  "progress": {
    "text": "Fetching page content...",
    "visibility": "channel",
    "privacy": "public",
    "id": "web_fetch:fetching"
  }
}
```

OpenClaw renders only the `progress.text` in the channel progress UI; the normal tool result still arrives later as `content` and `details`, and is the only part returned to the model. When adding progress to a tool, use a short, generic message and delay it until the operation has been pending long enough to be useful, via `scheduleToolProgress`:

```typescript
const clearProgressTimer = scheduleToolProgress(
  onUpdate,
  { text: "Fetching page content...", id: "web_fetch:fetching" },
  5_000,
  { signal },
);

try {
  return await runToolWork();
} finally {
  clearProgressTimer();
}
```

This pattern means fast calls do not show a progress line, long calls show one while still pending, and canceled calls clear the timer before stale progress can appear. Progress text is a public UI side channel, so it must not include secrets, raw arguments, fetched content, command output, or page text.

### Detail mode (`toolProgressDetail`)

OpenClaw uses the same formatter for progress drafts and `/verbose`, configured via `agents.defaults.toolProgressDetail` (`explain` | `raw`). `"explain"` is the default and keeps drafts stable with concise labels like `🛠️ check JS syntax for /tmp/app.js`; `"raw"` appends the underlying command/detail when available, useful while debugging but noisier in chat. For the same command, `explain` renders `🛠️ check JS syntax for /tmp/app.js` while `raw` renders `🛠️ check JS syntax for /tmp/app.js, node --check /tmp/app.js`.

### Line count and width (`maxLines`, `maxLineChars`)

`channels.<channel>.streaming.progress.maxLines` limits how many lines stay visible (the example uses `maxLines: 4`). Progress lines are compacted automatically to reduce chat-bubble reflow while the draft is edited. OpenClaw truncates long progress lines by default so repeated draft edits do not wrap differently on every update — the default per-line budget is 120 characters; prose cuts at a word boundary, while long details such as paths or raw commands are shortened with a middle ellipsis so the suffix remains visible. Tune the per-line budget with `maxLineChars` (the example uses `maxLineChars: 160`).

### Slack rich rendering (`render: "rich"`)

Slack can render progress lines as structured Block Kit fields instead of a single text body by setting `progress.render: "rich"` under the `slack` channel:

```json5
{
  channels: {
    slack: {
      streaming: {
        mode: "progress",
        progress: {
          render: "rich",
        },
      },
    },
  },
}
```

Rich rendering keeps the same plain-text fallback so channels and clients that do not support the richer shape can still show the compact progress text.

### Hide tool/task lines (`toolProgress: false`)

To keep the single progress draft but hide tool and task lines, set `progress.toolProgress: false`. With `toolProgress: false`, OpenClaw still suppresses the older standalone tool-progress messages for that turn, so the channel stays visually quiet until the final answer, except for the label if one is configured.

## Channel Behavior

Each channel uses the cleanest transport it supports:

| Channel | Progress transport | Notes |
| --- | --- | --- |
| Discord | Send one message, then edit it. | Final text edits in place when it fits one safe preview message. |
| Matrix | Send one event, then edit it. | Account-level streaming config controls account-level drafts. |
| Microsoft Teams | Native Teams stream in personal chats. | `streaming.mode: "block"` maps to Teams block delivery. |
| Slack | Native stream or editable draft post. | Thread availability affects whether native streaming can be used. |
| Telegram | Send one message, then edit it. | Older visible drafts may be replaced so final timestamps stay useful. |
| Mattermost | Editable draft post. | Tool activity is folded into the same draft-style post. |

Channels without safe edit support usually fall back to typing indicators or final-only delivery.

## Finalization

When the final answer is ready, OpenClaw tries to keep the chat clean. If the draft can safely become the final answer, OpenClaw edits it in place. If the channel uses native progress streaming, OpenClaw finalizes that stream when the native transport accepts the final text. If the final answer has media, an approval prompt, an explicit reply target, too many chunks, or a failed edit/send, OpenClaw sends the final answer through the normal channel delivery path. The fallback path is intentional: it is better to send a fresh final answer than to lose text, mis-thread a reply, or overwrite a draft with a payload the channel cannot represent safely.

## Troubleshooting

**I only see the final answer.** Check that `channels.<channel>.streaming.mode` is set to `progress` for the account or channel that handled the message. Some group or quote-reply paths may disable draft previews for a turn when the channel cannot safely edit the right message.

**I see the label but no tool lines.** Check `streaming.progress.toolProgress`. If it is `false`, OpenClaw keeps the single draft behavior but hides tool and task progress lines.

**I see a fresh final message instead of an edited draft.** That is a safety fallback. It can happen for media replies, long answers, explicit reply targets, old Telegram drafts, missing Slack thread targets, deleted preview messages, or failed native stream finalization.

**I still see standalone progress messages.** Progress mode suppresses default standalone tool-progress messages when a draft is active. If standalone messages still appear, verify that the turn is actually using progress mode and not `streaming.mode: "off"` or a channel path that cannot create a draft for that message.

**Teams behaves differently from Discord or Telegram.** Microsoft Teams uses a native stream in personal chats instead of the generic send-and-edit preview transport. Teams also treats `streaming.mode: "block"` as Teams block delivery because it does not have the same draft-preview block mode used by Discord and Telegram.

**Source**: OpenClaw documentation — `concepts/progress-drafts` (mirror `inbox/openclaw_docs/concepts/progress-drafts.md`)
**Last Updated**: 2026-06-22
**Status**: Active
