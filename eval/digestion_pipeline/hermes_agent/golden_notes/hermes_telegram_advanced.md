---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - telegram
keywords:
  - telegram advanced features
  - MEDIA attachments
  - voice messages STT TTS
  - local Bot API server
  - DM topics and /topic
  - streaming transport rich messages
  - group allowlisting guest_mode
  - slash command access control
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
access_control_group: ["general"]
---

# Hermes Agent — Telegram Advanced Features

## Overview

This is the day-2 operation guide for a Telegram bot that is already set up (see [hermes_telegram_setup](hermes_telegram_setup.md) for the BotFather → config → start arc). It covers the rich-feature surface the Telegram adapter exposes once the bot is online: `MEDIA:` file delivery (and the Docker-host path gotcha), voice STT/TTS plus the local telegram-bot-api server that lifts the 20MB file ceiling to 2GB, group triggering (`require_mention` / `mention_patterns` / `exclusive_bot_mentions` / multi-bot fleets), DM and group forum **topics** as isolated sessions (`extra.dm_topics`, the user-driven `/topic` mode, and `group_topics` skill binding), Bot-API-9.5 streaming transports + rich messages, group allowlisting with `guest_mode`, slash-command access tiers, the interactive model picker, reactions, per-channel prompts, exec-approval/`clarify`, and notification volume. Most knobs live under `gateway.platforms.telegram.extra` in `~/.hermes/config.yaml`; voice/STT/TTS feature concepts, the per-chat session-store internals, and the broader media `config.yaml` knobs are owned by other sub-plans and linked out, not duplicated here.

## Sending Generated Files (`MEDIA:`)

The gateway extracts `MEDIA:/path/to/file` tags from agent replies and ships the referenced file as a platform-native attachment. **Docker-host gotcha:** when the terminal backend is `docker`, attachments are sent by the **gateway process**, not from inside the container — so the `MEDIA:/...` path must be readable on the host where the gateway runs. A file written to `/workspace/report.txt` inside Docker fails delivery because that path only exists in the container. The fix is to bind-mount a shared output directory and emit the host-visible path:

```yaml
terminal:
  backend: docker
  docker_volumes:
    - "/home/user/.hermes/cache/documents:/output"
```

Write files inside Docker to `/output/...` and emit the host path, e.g. `MEDIA:/home/user/.hermes/cache/documents/report.txt`. If a `docker_volumes:` section already exists, add the mount to the same list (YAML duplicate keys silently override). Supported `MEDIA:` extensions span Images (`png`/`jpg`/`gif`/`webp`/`svg`…), Audio (`mp3`/`wav`/`ogg`/`opus`…), Video (`mp4`/`mov`/`webm`…), Documents (`pdf`/`txt`/`md`/`csv`/`json`/`yaml`/`log`), Office (`docx`/`xlsx`/`pptx`/`odt`…), Archives (`zip`/`tar`/`gz`…), and Books/packages (`epub`/`apk`/`ipa`). On platforms without native support the tag falls back to a link or plain-text indicator.

## Voice Messages (STT / TTS)

**Incoming voice** is auto-transcribed by the configured STT provider and injected as text: `local` uses `faster-whisper` (no API key), `groq` uses Groq Whisper (`GROQ_API_KEY`), `openai` uses OpenAI Whisper (`VOICE_TOOLS_OPENAI_KEY`). To hand the raw audio to the agent instead — for diarization, a custom transcription tool, or archiving — set `stt.enabled: false` in `config.yaml`; the gateway still downloads the file into Hermes's audio cache but does not transcribe it, and the agent receives a marker like `[The user sent a voice message: /home/<user>/.hermes/cache/audio/<hash>.ogg]` to read directly. **Outgoing voice** generated via TTS is delivered as native Telegram voice bubbles; OpenAI and ElevenLabs emit Opus natively, while Edge TTS (the default free provider) outputs MP3 and needs `ffmpeg` installed to convert to Opus (without it, audio ships as a regular file with the rectangular player). Voice mode, TTS, and STT feature concepts are owned by SP08 ([hermes_messaging_media_settings](hermes_messaging_media_settings.md)).

## Large Files (>20MB) via Local Bot API Server

Telegram's **public** Bot API caps `getFile` downloads at **20 MB**. To lift the ceiling to **2 GB** (long voice memos, large videos, raw-audio archiving), run a **local** [telegram-bot-api](https://github.com/tdlib/telegram-bot-api) daemon; Hermes auto-lifts its internal cap when it sees a custom `base_url`. The flow: (1) get MTProto `api_id`/`api_hash` from [my.telegram.org/apps](https://my.telegram.org/apps); (2) run the server in `--local` mode (`TELEGRAM_LOCAL=1`, bound to `127.0.0.1` — never expose port 8081 publicly, it takes the bot token in the URL with no auth); (3) one-time `curl "https://api.telegram.org/bot<TOKEN>/logOut"` to release the bot from the public API (a bot is active on only one server at a time); (4) point Hermes at the local server:

```yaml
platforms:
  telegram:
    extra:
      base_url: "http://127.0.0.1:8081/bot"
      base_file_url: "http://127.0.0.1:8081/file/bot"
      local_mode: true        # only if the bot's data dir is readable by Hermes
```

Use `platforms.telegram.extra`, **not** a top-level `telegram.extra` — only the `platforms.<name>.extra` form is deep-merged; keys placed elsewhere are silently dropped. With `local_mode: true`, the `--local` server returns an **absolute file path** (not an HTTP URL), so Hermes must read the bytes from disk — the data dir must be mounted at the **same absolute path** the server reports (typically `/var/lib/telegram-bot-api`), with matching ownership; a permission/mount mismatch shows up as `telegram.error.InvalidToken: Not Found` in `gateway.log`. Pairs naturally with `stt.enabled: false` for downstream audio pipelines.

## Group Triggering and Multi-Bot Fleets

In group chats, **privacy mode** (Step 3 of setup) determines what the bot can see, and `TELEGRAM_ALLOWED_USERS` still gates who can trigger it. Set `telegram.require_mention: true` to keep the bot from answering ordinary chatter — group messages are then only accepted when they are replies to the bot, `@botusername` mentions, `/command@botusername` forms, or matches for a configured Python regex wake word in `telegram.mention_patterns` (case-insensitive, checked against text and media captions, invalid patterns logged-and-ignored, anchor with `^` for start-of-message). `telegram.ignored_threads` keeps Hermes silent in specific forum topics. For groups with **multiple Hermes bots**, run one bot token + one gateway per profile (Telegram rejects concurrent polling on a shared token) and keep `exclusive_bot_mentions: true` (the default) so only explicitly @mentioned bots process a message:

```yaml
telegram:
  require_mention: true
  exclusive_bot_mentions: true
  mention_patterns:
    - "^\\s*chompy\\b"
  ignored_threads:
    - 31
    - "42"
```

A message `@research_bot @ops_bot summarize this` is then handled only by those two bots; others stay silent even on reply/wake-word triggers. Run named profiles with `hermes -p <profile> gateway <action>`.

## DM Topics, `/topic`, and Group Forum Skill Binding

Telegram Bot API 9.4 added **Private Chat Topics** — forum-style threads inside a 1-on-1 DM, no supergroup needed. Each topic maps to an **isolated session key** `agent:main:telegram:dm:{chat_id}:{thread_id}`, with its own conversation history, memory flush, and context window. There are two flavors. **Operator-curated** topics are declared under `platforms.telegram.extra.dm_topics` (Hermes calls `createForumTopic` on startup for any topic missing a `thread_id`, then saves the `thread_id` back to config); a topic's optional `skill:` field auto-loads that skill whenever a new session starts in it — identical to typing `/skill-name` at the conversation start. **User-driven** multi-session mode is activated by sending `/topic` in the root DM (a ChatGPT-style flow): the user taps Telegram's **+** to create as many independent-session topics as they want, the root DM becomes a system-command lobby, bindings persist to `telegram_dm_topic_mode` / `telegram_dm_topic_bindings` SQLite tables (opt-in migration on first `/topic`), and `/topic <session-id>` restores a prior session. The user must first enable Threaded Mode in BotFather; `/topic` is gated by the bot's user-authorization check. **Group forum topics** in supergroups already get per-`thread_id` session isolation; to also auto-load a skill per topic, map them under `platforms.telegram.extra.group_topics` (admin-created `thread_id` set manually, optional `skill:` per topic). Topic/session storage internals are owned by SP02; skill loading by SP05.

## Streaming, Rich Messages, and Access Control

**Streaming transport.** With `gateway.streaming.enabled: true`, the `transport` knob picks how progressive output is delivered: `auto` (native `sendMessageDraft` token-by-token streaming on supported DMs, edit-based fallback elsewhere), `draft` (force native drafts), `edit` (legacy progressive `editMessageText` everywhere), or `off` (final reply only). Telegram restricts drafts to private chats, so groups/supergroups/topics transparently fall back to the edit path, and any failed draft frame flips that response to edit for the rest of the stream:

```yaml
gateway:
  streaming:
    enabled: true
    transport: auto    # auto | draft | edit | off
```

**Rich messages (Bot API 10.1)** send constructs the legacy MarkdownV2 path degrades — tables, task lists, collapsible `<details>`, block math — via native `sendRichMessage` using the agent's raw markdown, with transparent MarkdownV2 fallback on rejection (small pipe tables flatten to row-group bullets, larger ones to fenced code blocks). Enabled by default; disable per-platform with `extra.rich_messages: false`, suppress URL previews with `extra.disable_link_previews: true`, and keep always-code-block tables with `telegram.pretty_tables: false`. **Group allowlisting** has two orthogonal gates: sender IDs (`group_allow_from` / `TELEGRAM_GROUP_ALLOWED_USERS`, no DM access) and chat IDs (`group_allowed_chats` / `TELEGRAM_GROUP_ALLOWED_CHATS`, any member authorized); `guest_mode: true` lets non-allowlisted groups through **only** on explicit @mention, every turn (no session stickiness). **Slash-command access control** splits the allowlist into admins (`allow_admin_from` — every registered command) and regular users (`user_allowed_commands` — only listed commands, plus the always-allowed `/help` and `/whoami`); unset `allow_admin_from` for a scope means unrestricted (backward-compatible), and DM admin status does not imply group admin status. Use `/whoami` to see scope, tier, and runnable commands.

## Other Interaction Surfaces

- **Interactive model picker** — `/model` with no arguments opens an inline-keyboard provider→model picker (paginated, navigates in-place); `/model <name>` skips it, `/model <name> --global` persists across sessions.
- **Message reactions** (disabled by default; `telegram.reactions: true` / `TELEGRAM_REACTIONS=true`) add 👀 on processing-start, ✅ on success, ❌ on error; Telegram replaces all bot reactions atomically (unlike Discord's additive model).
- **Per-channel prompts** (`telegram.channel_prompts`) inject ephemeral system prompts per group/topic at runtime (never persisted to transcript); topic-level keys override group-level for forum groups.
- **Exec approval** — the agent asks in-chat before a dangerous command; reply "yes"/"y" to approve, "no"/"n" to deny.
- **`clarify`** — renders preset choices as inline-keyboard buttons (plus an "Other" free-form path), with `agent.clarify_timeout` (default `600`s) before the agent unblocks with a sentinel.
- **Notification volume** — `display.platforms.telegram.notifications: important` (default) rings only on final responses, approval prompts, and slash-command confirmations (tool progress / streaming chunks ship with `disable_notification=true`); `all` rings on everything. Status callbacks are edited in place via `send_or_update_status()`, and the triggering user message is pinned for the duration of the turn.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/telegram.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
**Last Updated**: 2026-06-19
**Status**: Active
