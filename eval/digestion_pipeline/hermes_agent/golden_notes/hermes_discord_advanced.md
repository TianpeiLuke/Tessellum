---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - discord
keywords:
  - discord gateway model
  - group_sessions_per_user
  - discord configuration reference
  - native slash commands for skills
  - voice_fx mixer
  - forum channels
  - allow_any_attachment
  - history backfill
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord
access_control_group: ["general"]
---

# Hermes Agent — Discord Advanced

## Overview

This note is the **operational reference for a running Hermes Discord bot** — everything past first-bot setup (see [hermes_discord_setup](hermes_discord_setup.md)). Discord is not a stateless webhook: it runs through the **full messaging gateway**, so every message flows through authorization → mention/free-response checks → session lookup → transcript load → agent execution → delivery, and behavior in a busy server depends on both Discord routing and Hermes session policy. This note documents the **session model** (`group_sessions_per_user` + interrupt/concurrency), the **`.env` + `config.yaml` configuration reference** (mention/threading/backfill/tool-progress), **slash-command access tiers** and **native skill slash-command registration**, **media send/receive** (incl. the arbitrary-file allowlist), the **`voice_fx` mixer** for voice channels, and **forum-channel handling**. The gateway model and per-chat session store this builds on live in [hermes_messaging_gateway_architecture](hermes_messaging_gateway_architecture.md); shared ops (interrupt/queue/steer, restart-resume) live in [hermes_gateway_operations](hermes_gateway_operations.md).

## Discord Gateway Model

Hermes on Discord is not a webhook that replies statelessly. It runs through the full messaging gateway, which means each incoming message goes through:

1. authorization (`DISCORD_ALLOWED_USERS`)
2. mention / free-response checks
3. session lookup
4. session transcript loading
5. normal Hermes agent execution, including tools, memory, and slash commands
6. response delivery back to Discord

That matters because behavior in a busy server depends on both Discord routing and Hermes session policy.

## Session Model in Discord

By default each DM gets its own session, each server thread its own session namespace, and each user in a shared channel their own session inside that channel — so if Alice and Bob both talk to Hermes in `#research`, those are separate conversations even in the same visible channel. This is controlled by `config.yaml`:

```yaml
group_sessions_per_user: true
```

Set it to `false` only if you want one shared conversation for the entire room. Shared sessions suit a collaborative room but mean users share context growth and token costs, one person's tool-heavy task can bloat everyone's context, and one person's in-flight run can interrupt another's follow-up in the same room.

**Interrupts and concurrency.** Hermes tracks running agents by session key. With the default `group_sessions_per_user: true`, Alice interrupting her own in-flight request only affects Alice's session, and Bob keeps talking in the same channel without inheriting Alice's history or interrupting her run. With `group_sessions_per_user: false`, the whole room shares one running-agent slot for that channel/thread, so follow-ups from different people can interrupt or queue behind each other. (The interrupt/queue/steer mechanics live in [hermes_gateway_operations](hermes_gateway_operations.md).)

## Configuration Reference

Discord behavior is controlled through two files: **`~/.hermes/.env`** for credentials and env-level toggles, and **`~/.hermes/config.yaml`** for structured settings. Environment variables always win over `config.yaml` when both are set.

Selected `.env` variables: `DISCORD_REQUIRE_MENTION` (default `true`) gates server-channel responses behind an `@mention`; `DISCORD_THREAD_REQUIRE_MENTION` (default `false`) disables the in-thread shortcut for multi-bot threads; `DISCORD_FREE_RESPONSE_CHANNELS` lists mention-free channels; `DISCORD_AUTO_THREAD` (default `true`) spins a new thread per `@mention`; `DISCORD_IGNORED_CHANNELS`/`DISCORD_ALLOWED_CHANNELS`/`DISCORD_NO_THREAD_CHANNELS` express allow/deny and inline-vs-thread routing; `DISCORD_HISTORY_BACKFILL` + `DISCORD_HISTORY_BACKFILL_LIMIT` recover missed scrollback; `DISCORD_REACTIONS` adds 👀/✅/❌ processing reactions; `DISCORD_ALLOW_ANY_ATTACHMENT` + `DISCORD_MAX_ATTACHMENT_BYTES` control arbitrary-file receive; the `DISCORD_ALLOW_MENTION_*` family controls who the bot may ping. The `discord` section in `config.yaml` mirrors these as defaults (env wins):

```yaml
# Discord-specific settings
discord:
  require_mention: true           # Require @mention in server channels
  thread_require_mention: false   # If true, require @mention in threads too (multi-bot threads)
  free_response_channels: ""      # Comma-separated channel IDs (or YAML list)
  auto_thread: true               # Auto-create threads on @mention
  reactions: true                 # Add emoji reactions during processing
  ignored_channels: []            # Channel IDs where bot never responds
  no_thread_channels: []          # Channel IDs where bot responds without threading
  history_backfill: true          # Prepend recent channel scrollback on mention (default: true)
  history_backfill_limit: 50      # Max messages to scan backwards (default: 50)
  channel_prompts: {}             # Per-channel ephemeral system prompts
  allow_mentions:                 # What the bot is allowed to ping (safe defaults)
    everyone: false               # @everyone / @here pings (default: false)
    roles: false                  # @role pings (default: false)
    users: true                   # @user pings (default: true)
    replied_user: true            # reply-reference pings the author (default: true)

# Session isolation (applies to all gateway platforms, not just Discord)
group_sessions_per_user: true     # Isolate sessions per user in shared channels
```

**`history_backfill` by surface:** in server channels (`require_mention: true`) it scans since the bot's last response; in threads it scans the thread only (Discord's `channel.history()` on a thread returns just that thread's messages); DMs and free-response channels are skipped (no mention gap). Per-user sessions also benefit — backfill fills both the missed-other-participants gap and the user's own pre-mention messages. The `history_backfill_limit` (default `50`) is a safety cap; the scan usually stops earlier, at the bot's own last message.

**`channel_prompts`** injects per-channel ephemeral system prompts on every turn in the matching channel/thread without persisting them to history. Exact thread/channel ID matches win; an unmatched thread falls back to the parent channel/forum ID. Because prompts apply ephemerally at runtime, changing one affects future turns immediately without rewriting past history.

The global `display.tool_progress` setting (default `"all"`, values `off`/`new`/`all`/`verbose`) controls whether the bot posts "Reading file…" progress messages in chat, and `display.tool_progress_command: true` exposes the `/verbose` slash command to cycle modes live without editing `config.yaml`.

## Slash Command Access Control

By default every allowed user can run every slash command. To split the allowlist into **admins** (full access) and **regular users** (only commands you enable), add `allow_admin_from` and `user_allowed_commands` to the Discord platform's `extra` block. A user in `allow_admin_from` for a scope (DM or server channel) can run **every** registered slash command — built-in and plugin-registered. A user not in it can only run commands in `user_allowed_commands` plus the always-allowed floor (`/help`, `/whoami`). Plain chat is unaffected; if `allow_admin_from` is unset for a scope, gating is disabled there (backward compatible), and DM admin status does not imply server-channel admin status. Use `/whoami` to see your active scope, tier, and runnable commands.

## Native Slash Commands for Skills

Hermes automatically registers installed skills as **native Discord Application Commands**, so skills appear in Discord's `/` autocomplete alongside built-ins. Each skill becomes a slash command (e.g. `/code-review`) accepting an optional `args` string; Discord caps a bot at 100 application commands, so skills beyond available slots are skipped with a log warning. Registration happens at startup alongside `/model`, `/reset`, and `/background` — any skill installed via `hermes skills install` registers on the next gateway restart, no extra config. If you run multiple gateways against the same Discord application (staging + production), only the primary should own global registration; turn it off on followers:

```yaml
gateway:
  platforms:
    discord:
      extra:
        slash_commands: false   # default: true
```

## Sending and Receiving Media

The Discord adapter supports native file uploads for every common media type via the `send_message` tool and inline `MEDIA:/path/to/file` tags: images (`PNG`/`JPG`/`WebP`) as native attachments with inline preview, animated GIFs via `send_animation`, video (`MP4`/`MOV`) via `send_video`, audio/voice via `send_voice`, and documents via `send_document`. Discord's per-upload size limit depends on the server's boost tier (25 MB free, up to 500 MB); on an HTTP 413 the adapter falls back to a link pointing at the local cache path rather than failing silently.

**Receiving arbitrary file types.** By default the bot only caches uploads matching a built-in allowlist (images, audio, video, PDF, text/csv/log, JSON/XML/YAML/TOML, zip, office docs); anything else is logged `Unsupported document type` and dropped. Enable `discord.allow_any_attachment` to accept any type:

```yaml
discord:
  allow_any_attachment: true
  # Optional — raise/disable the per-file size cap. Default is 32 MiB.
  # The whole file is held in memory while being cached, so unlimited
  # uploads carry a real memory cost.
  max_attachment_bytes: 33554432   # bytes; 0 = unlimited
```

With the flag on, any uploaded file is downloaded, cached under `~/.hermes/cache/documents/`, and surfaced to the agent as a `DOCUMENT`-typed event with `application/octet-stream` MIME. The agent receives a context note pointing at the local path (auto-translated for Docker/Modal sandboxed terminals via `to_agent_visible_cache_path`) and inspects it with `terminal` (`ffprobe`, `unzip`, `file`, `strings`) or `read_file` — the body is **not** inlined into the prompt, so binary uploads don't blow up the context window. Known-text formats already in the allowlist (`.txt`, `.md`, `.log`) still auto-inject contents up to 100 KiB. Equivalent env vars exist (`DISCORD_ALLOW_ANY_ATTACHMENT`, `DISCORD_MAX_ATTACHMENT_BYTES`). Disabling the cap (`0`) lets a user drop a multi-GB file the gateway buffers through memory — only set unlimited in trusted single-user installs.

## Interactive Prompts (clarify) and Home Channel

When the agent calls the `clarify` tool, Discord renders the question with **one button per choice** (e.g. `[1. Next.js] [2. Remix] [3. Astro] [Other (type answer)]`). Clicking a numbered button answers; **Other** captures your next message as a free-form answer; open-ended `clarify` calls (no preset choices) skip the buttons and just capture your next message. Buttons disable once a choice is made so duplicate clicks don't double-resolve. The timeout is `agent.clarify_timeout` (default `600` seconds); on timeout the agent unblocks with a sentinel rather than hanging.

A **home channel** is where the bot sends proactive messages (cron output, reminders, notifications). Set it with `/sethome` in any channel where the bot is present, or manually:

```bash
DISCORD_HOME_CHANNEL=123456789012345678
DISCORD_HOME_CHANNEL_NAME="#bot-updates"
```

## Voice Messages and `voice_fx`

Incoming voice messages are auto-transcribed via the configured STT provider (local `faster-whisper`, Groq Whisper, or OpenAI Whisper); `/voice tts` sends spoken audio alongside text; and Hermes can join a voice channel to listen and talk back. Full voice setup is owned by [hermes_messaging_media_settings](hermes_messaging_media_settings.md) (SP02/SP08) — link-out, not duplicated here.

**Voice channel audio effects.** In a voice channel, `voice_fx` adds a short verbal acknowledgement ("let me look into that") before work and a subtle ambient "thinking" bed while tools run, ducking and swelling like Grok voice mode. Because discord.py plays only one audio stream per connection, Hermes installs a software mixer that sums ambient loop, acknowledgements, and TTS into that single stream so they overlap. It is **off by default**:

```yaml
discord:
  voice_fx:
    enabled: true          # master switch
    ambient_enabled: true  # idle "thinking" bed while tools run
    ambient_path: ""       # custom loop file (any audio format); "" = built-in synthesised pad
    ambient_gain: 0.18     # idle bed loudness (0.0–1.0)
    duck_gain: 0.06        # ambient loudness while the bot is speaking
    speech_gain: 1.0       # TTS / acknowledgement loudness
    ack_enabled: true      # speak a short phrase before the first tool call of a turn
    ack_phrases:           # picked at random; set to [] to disable the spoken ack
      - "Let me look into that."
      - "One moment."
      - "Checking on that now."
```

The acknowledgement fires at most once per turn, only when the bot is in a voice channel with the mixer active, using your configured TTS provider. `ambient_path` accepts any file `ffmpeg` can decode (looped seamlessly); empty uses the built-in synthesised pad. All settings live in `config.yaml` (not `.env`) because they're behavioral, not secrets; with `voice_fx.enabled: false`, playback uses the original one-shot path.

## Forum Channels

Discord forum channels (type 15) don't accept direct messages — every post must be a thread. Hermes auto-detects forum channels and creates a new thread post whenever it sends there, so `send_message`, TTS, images, voice messages, and file attachments all work without special agent handling. The thread name derives from the message's first line (markdown heading stripped, capped at 100 chars; attachment-only sends use the filename). Attachments ride along on the new thread's starter message (no separate upload step). Each forum send creates a new thread, so successive sends produce separate threads. **Detection is three-layered**: the channel directory cache first, a process-local probe cache second, and a live `GET /channels/{id}` probe as a last resort (memoized for the process life). Refreshing the directory (`/channels refresh`, or a gateway restart) picks up forum channels created after the bot started.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/discord.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord
**Last Updated**: 2026-06-19
**Status**: Active
