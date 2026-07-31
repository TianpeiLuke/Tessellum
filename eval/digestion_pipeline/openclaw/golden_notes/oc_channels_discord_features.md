---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - discord
keywords:
  - discord interactive components
  - components v2 ui
  - discord action gates
  - discord feature details
  - replyToMode reply tags
  - agentComponents ttlMs
  - discord message actions
  - discord exec approvals
topics:
  - OpenClaw
  - Discord Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/channels/discord
access_control_group: ["general"]
---

# OpenClaw — Discord Feature Details, Interactive Components & Action Gates

## Overview

This note models the Discord channel's **feature surface** — the per-feature behavior knobs, the interactive components v2 UI, and the tool/action-gate catalog — mirroring the Feature details, Interactive components, Components v2 UI, and Tools and action gates sections of the `channels/discord` source page. It is a reference of *what* a Discord agent can send and *which knobs/gates govern each capability*. Setup, runtime/access routing, voice, and operations are sibling notes.

## Interactive Components

OpenClaw supports Discord **components v2 containers** for agent messages: an agent sends them via the message tool with a `components` payload, and interaction results route back as normal inbound messages following the existing Discord `replyToMode` settings. Supported blocks are `text`, `section`, `separator`, `actions`, `media-gallery`, and `file`; an action row allows up to 5 buttons or a single select menu; select types are `string`, `user`, `role`, `mentionable`, and `channel`. Components are single use by default — `components.reusable=true` allows buttons, selects, and forms to be reused until they expire. To restrict who can click a button, set `allowedUsers` on it (Discord user IDs, tags, or `*`); unmatched users receive an ephemeral denial.

Component callbacks expire after 30 minutes by default. `channels.discord.agentComponents.ttlMs` sets the callback registry lifetime for the default account (per account via `channels.discord.accounts.<accountId>.agentComponents.ttlMs`); the value is milliseconds, a positive integer, capped at `86400000` (24 hours). Longer TTLs help review/approval workflows but extend the window where an old message can still trigger an action, so prefer the shortest TTL that fits.

The `/model` and `/models` slash commands open an interactive model picker (provider, model, and compatible-runtime dropdowns plus a Submit step); `/models add` is deprecated and now returns a deprecation message instead of registering models from chat. The picker reply is ephemeral and only the invoking user can use it. Discord select menus are limited to 25 options, so add `provider/*` entries to `agents.defaults.models` to show dynamically discovered models only for selected providers such as `openai` or `vllm`.

**File attachments** in components: `file` blocks must point to an attachment reference (`attachment://<filename>`); provide it via `media`/`path`/`filePath` (single file) or `media-gallery` (multiple files); use `filename` to override the upload name to match the reference.

**Modal forms**: add `components.modal` with up to 5 fields (types `text`, `checkbox`, `radio`, `select`, `role-select`, `user-select`); OpenClaw adds a trigger button automatically.

Example of a full components payload (buttons with `allowedUsers`, a string select, and a modal form):

```json5
{
  channel: "discord",
  action: "send",
  to: "channel:123456789012345678",
  message: "Optional fallback text",
  components: {
    reusable: true,
    text: "Choose a path",
    blocks: [
      {
        type: "actions",
        buttons: [
          {
            label: "Approve",
            style: "success",
            allowedUsers: ["123456789012345678"],
          },
          { label: "Decline", style: "danger" },
        ],
      },
      {
        type: "actions",
        select: {
          type: "string",
          placeholder: "Pick an option",
          options: [
            { label: "Option A", value: "a" },
            { label: "Option B", value: "b" },
          ],
        },
      },
    ],
    modal: {
      title: "Details",
      triggerLabel: "Open form",
      fields: [
        { type: "text", label: "Requester" },
        {
          type: "select",
          label: "Priority",
          options: [
            { label: "Low", value: "low" },
            { label: "High", value: "high" },
          ],
        },
      ],
    },
  },
}
```

## Feature Details

Per-feature behavior; each entry is a Discord-specific capability with its governing config keys.

### Reply tags and native replies

Discord supports reply tags in agent output: `[[reply_to_current]]` and `[[reply_to:<id>]]`. Implicit reply threading is controlled by `channels.discord.replyToMode` with values `off` (default), `first`, `all`, and `batched`. `off` disables implicit reply threading but still honors explicit `[[reply_to_*]]` tags; `first` always attaches the implicit native reply reference to the first outbound message of the turn; `batched` attaches it only when the inbound event was a debounced batch of multiple messages (useful for ambiguous bursty chats). Message IDs are surfaced in context/history so agents can target specific messages.

### Link previews

Discord generates rich link embeds for URLs by default; OpenClaw suppresses those generated embeds on outbound messages by default, so agent-sent URLs stay plain links unless you opt in via `channels.discord.suppressEmbeds: false` (per-account override `channels.discord.accounts.<id>.suppressEmbeds`; a message-tool send can also pass `suppressEmbeds: false` for one message). Explicit Discord `embeds` payloads are not suppressed by the default link-preview setting.

### Live stream preview

OpenClaw can stream draft replies by sending a temporary message and editing it as text arrives. `channels.discord.streaming` takes `off` | `partial` | `block` | `progress` (default): `partial` edits a single preview message as tokens arrive; `block` emits draft-sized chunks (use `draftChunk` to tune size/breakpoints, clamped to `textChunkLimit`); `progress` keeps one editable status draft updated with tool progress until final delivery. `streamMode` is a legacy runtime alias — `openclaw doctor --fix` rewrites it to the canonical key. Set `channels.discord.streaming.mode` to `off` to disable preview edits; if block streaming is explicitly enabled, OpenClaw skips the preview stream to avoid double-streaming. Media, error, and explicit-reply finals cancel pending preview edits, and preview streaming is text-only (media replies fall back to normal delivery).

Progress-preview knobs: `streaming.preview.toolProgress` (default `true`) controls whether tool/progress updates reuse the preview message, rendering compact emoji + title + detail rows (e.g. `🛠️ Bash: run tests`); `streaming.progress.commentary` (default `false`) opts into transient assistant commentary in the progress draft; `streaming.progress.maxLineChars` sets the per-line progress budget; `streaming.preview.commandText` / `streaming.progress.commandText` controls command/exec detail with `raw` (default) or `status` (tool label only).

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          label: "auto",
          maxLines: 8,
          maxLineChars: 120,
          toolProgress: true,
          commentary: false,
        },
      },
    },
  },
}
```

### History, context, and thread behavior

Guild history context uses `channels.discord.historyLimit` (default `20`, falling back to `messages.groupChat.historyLimit`; `0` disables); DM history uses `channels.discord.dmHistoryLimit` and `channels.discord.dms["<user_id>"].historyLimit`. Threads route as channel sessions and inherit parent channel config unless overridden; a thread inherits the parent's session-level `/model` as a model-only fallback (thread-local `/model` still takes precedence, parent transcript history is not copied unless transcript inheritance is enabled); `channels.discord.thread.inheritParent` (default `false`, per-account override under `channels.discord.accounts.<id>.thread.inheritParent`) opts new auto-threads into seeding from the parent transcript; message-tool reactions can resolve `user:<id>` DM targets; and `guilds.<guild>.channels.<channel>.requireMention: false` is preserved during reply-stage activation fallback. Channel topics are injected as **untrusted** context — allowlists gate who can trigger the agent, not a full supplemental-context redaction boundary.

### Thread-bound sessions for subagents

Discord can bind a thread to a session target so follow-up messages in that thread keep routing to the same session (including subagent sessions). Commands: `/focus <target>` binds the current/new thread to a subagent/session target; `/unfocus` removes the binding; `/agents` shows active runs and binding state; `/session idle <duration|off>` and `/session max-age <duration|off>` inspect/update inactivity auto-unfocus and hard max age for focused bindings. `session.threadBindings.*` sets global defaults; `channels.discord.threadBindings.*` overrides Discord behavior; `spawnSessions` controls auto-create/bind threads for `sessions_spawn({ thread: true })` and ACP thread spawns (default `true`); `defaultSpawnContext` controls native subagent context for thread-bound spawns (default `"fork"`); deprecated `spawnSubagentSessions`/`spawnAcpSessions` keys are migrated by `openclaw doctor --fix`; and if thread bindings are disabled for an account, `/focus` and related operations are unavailable.

### Persistent ACP channel bindings

For stable "always-on" ACP workspaces, configure top-level typed ACP bindings targeting Discord conversations via `bindings[]` with `type: "acp"` and `match.channel: "discord"`. `/acp spawn codex --bind here` binds the current channel or thread in place, keeping future messages on the same ACP session (thread messages inherit the parent channel binding); in a bound channel or thread, `/new` and `/reset` reset the same ACP session in place (temporary thread bindings can override target resolution while active); `spawnSessions` gates child thread creation/binding via `--thread auto|here`.

### Reaction notifications and ack reactions

Per-guild reaction notification mode is `off`, `own` (default), `all`, or `allowlist` (uses `guilds.<id>.users`); reaction events become system events attached to the routed Discord session. Separately, `ackReaction` sends an acknowledgement emoji while processing an inbound message, resolved in order `channels.discord.accounts.<accountId>.ackReaction` → `channels.discord.ackReaction` → `messages.ackReaction` → agent identity emoji fallback (`agents.list[].identity.emoji`, else "👀"). Discord accepts unicode or custom emoji names; `""` disables the reaction for a channel or account.

### Config writes, gateway proxy, PluralKit, and mention aliases

Channel-initiated config writes are enabled by default (affecting `/config set|unset` flows when command features are enabled); disable with `channels.discord.configWrites: false`. A `channels.discord.proxy` HTTP(S) proxy routes Discord gateway WebSocket traffic and startup REST lookups (application ID + allowlist resolution), with per-account override under `channels.discord.accounts.<id>.proxy`. PluralKit support (`channels.discord.pluralkit.enabled`, optional `token` for private systems) maps proxied messages to system member identity: allowlists can use `pk:<memberId>`; display names match by name/slug only when `channels.discord.dangerouslyAllowNameMatching: true`; lookups use the original message ID and are time-window constrained; failed lookups treat proxied messages as bot messages, dropped unless `allowBots=true`. `mentionAliases` gives deterministic outbound mentions for known Discord users — keys are handles without the leading `@`, values are user IDs; unknown handles, `@everyone`, `@here`, and mentions inside Markdown code spans are left unchanged (per-account override under `channels.discord.accounts.<id>.mentionAliases`).

### Presence configuration

Presence updates apply when you set a status or activity field, or enable auto presence. The `activityType` map: 0 Playing, 1 Streaming (requires `activityUrl`), 2 Listening, 3 Watching, 4 Custom (uses the activity text as the status state; emoji optional), 5 Competing. Auto presence (`channels.discord.autoPresence`) maps runtime availability to status — healthy => online, degraded or unknown => idle, exhausted or unavailable => dnd — with optional overrides `autoPresence.healthyText`, `autoPresence.degradedText`, and `autoPresence.exhaustedText` (supports a `{reason}` placeholder).

```json5
{
  channels: {
    discord: {
      activity: "Live coding",
      activityType: 1,
      activityUrl: "https://twitch.tv/openclaw",
      autoPresence: { enabled: true, intervalMs: 30000, minUpdateIntervalMs: 15000, exhaustedText: "token exhausted" },
    },
  },
}
```

### Approvals in Discord

Discord supports button-based approval handling in DMs and can optionally post approval prompts in the originating channel, governed by `channels.discord.execApprovals.enabled`, `.approvers` (optional; falls back to `commands.ownerAllowFrom`), `.target` (`dm` | `channel` | `both`, default `dm`), and `agentFilter`/`sessionFilter`/`cleanupAfterResolve`. Native exec approvals auto-enable when `enabled` is unset or `"auto"` and at least one approver resolves (from `execApprovals.approvers` or `commands.ownerAllowFrom`); approvers are not inferred from channel `allowFrom`, legacy `dm.allowFrom`, or direct-message `defaultTo`; `enabled: false` disables Discord as a native approval client. For sensitive owner-only group commands such as `/diagnostics` and `/export-trajectory`, prompts and results are sent privately (Discord DM first when the owner has a Discord owner route, else the first owner route from `commands.ownerAllowFrom`, such as Telegram). When `target` is `channel` or `both` the prompt is visible in the channel and only resolved approvers can use the buttons (others get an ephemeral denial); prompts include the command text, so enable channel delivery only in trusted channels, and if the channel ID cannot be derived from the session key, delivery falls back to DM. Discord also renders the shared approval buttons used by other chat channels (the native adapter mainly adds approver DM routing and channel fanout); approval resolution follows the shared Gateway client contract (`plugin:` IDs via `plugin.approval.resolve`, others via `exec.approval.resolve`), and approvals expire after 30 minutes by default.

## Tools and Action Gates

Discord message actions cover messaging, channel admin, moderation, presence, and metadata. Core examples: messaging — `sendMessage`, `readMessages`, `editMessage`, `deleteMessage`, `threadReply`; reactions — `react`, `reactions`, `emojiList`; moderation — `timeout`, `kick`, `ban`; presence — `setPresence`. The `event-create` action accepts an optional `image` parameter (URL or local file path) for the scheduled event cover. Action gates live under `channels.discord.actions.*`, with these defaults:

| Action group | Default |
| --- | --- |
| reactions, messages, threads, pins, polls, search, memberInfo, roleInfo, channelInfo, channels, voiceStatus, events, stickers, emojiUploads, stickerUploads, permissions | enabled  |
| roles | disabled |
| moderation | disabled |
| presence | disabled |

## Components v2 UI

OpenClaw uses Discord components v2 for exec approvals and cross-context markers. Discord message actions can also accept `components` for custom UI (advanced; requires constructing a component payload via the discord tool); legacy `embeds` remain available but not recommended. `channels.discord.ui.components.accentColor` sets the component-container accent color (hex), per account via `channels.discord.accounts.<id>.ui.components.accentColor`. `channels.discord.agentComponents.ttlMs` sets how long sent component callbacks remain registered (default `1800000`, maximum `86400000`), per account via `channels.discord.accounts.<id>.agentComponents.ttlMs`. `embeds` are ignored when components v2 are present, and plain URL previews are suppressed by default (set `suppressEmbeds: false` on a message action to expand a single outbound link).

```json5
{
  channels: {
    discord: {
      ui: {
        components: {
          accentColor: "#5865F2",
        },
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `channels/discord` (mirror `inbox/openclaw_docs/channels/discord.md`, sections Feature details / Interactive components / Components v2 UI / Tools and action gates)
**Last Updated**: 2026-06-22
**Status**: Active
