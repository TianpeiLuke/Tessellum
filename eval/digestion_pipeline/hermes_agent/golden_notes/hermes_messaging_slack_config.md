---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - slack
keywords:
  - slack config.yaml reference
  - reply_to_mode threading
  - require_mention strict_mention
  - allowed_channels allowlist
  - multi-workspace slack_tokens.json
  - per-channel prompts and skill bindings
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack
access_control_group: ["general"]
---

# Hermes Slack Bot — Configuration Reference

## Overview

This is the `~/.hermes/config.yaml` behavior reference for the Hermes Slack bot — the ongoing tuning surface that sits on top of the one-time app-creation procedure in [hermes_messaging_slack](hermes_messaging_slack.md). Where Step 8 of the setup page wires the required environment variables (`SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_ALLOWED_USERS`), this page documents the knobs that shape *how* the bot replies and *who* it answers: threading/reply modes, per-user session isolation, mention vs free-response gating, the channel allowlist, unauthorized-DM handling, multi-workspace token lists plus the `slack_tokens.json` OAuth file, voice transcription, a default home channel, and per-channel prompts and skill bindings.

All Slack-specific settings live under a `slack:` block (mention/trigger/allowlist behavior) and a `platforms.slack:` block (reply/threading + token), with a few global toggles (`group_sessions_per_user`, `unauthorized_dm_behavior`, `stt_enabled`) that apply across all platforms but can be overridden per-platform. Nothing here is required to get the bot running — the defaults are sensible — but each knob exists to fit Hermes into a busier or more restricted Slack workspace.

## Thread & Reply Behavior

`reply_to_mode` controls how multi-part responses are threaded; the `extra` keys control whether channel replies thread at all and whether they broadcast to the channel.

```yaml
platforms:
  slack:
    # Controls how multi-part responses are threaded
    # "off"   — never thread replies to the original message
    # "first" — first chunk threads to user's message (default)
    # "all"   — all chunks thread to user's message
    reply_to_mode: "first"

    extra:
      # Whether to reply in a thread (default: true).
      # When false, channel messages get direct channel replies instead
      # of threads. Messages inside existing threads still reply in-thread.
      reply_in_thread: true

      # Also post thread replies to the main channel
      # (Slack's "Also send to channel" feature).
      # Only the first chunk of the first reply is broadcast.
      reply_broadcast: false
```

| Key | Default | Description |
|-----|---------|-------------|
| `platforms.slack.reply_to_mode` | `"first"` | Threading mode for multi-part messages: `"off"`, `"first"`, or `"all"`. |
| `platforms.slack.extra.reply_in_thread` | `true` | When `false`, channel messages get direct replies instead of threads. Messages inside existing threads still reply in-thread. |
| `platforms.slack.extra.reply_broadcast` | `false` | When `true`, thread replies are also posted to the main channel. Only the first chunk is broadcast. |

## Session Isolation

The global `group_sessions_per_user: true` setting (top-level, applies to Slack and all other platforms) controls session isolation. When `true` (the default), each user in a shared channel gets their own isolated conversation session — two people talking to Hermes in `#general` have separate histories and contexts. Set to `false` for a collaborative mode where the entire channel shares one conversation session; the source warns this means users share context growth and token costs, and one user's `/reset` clears the session for everyone. This is a global gateway knob, not Slack-specific. The per-user/thread session-key derivation behind it is documented in the gateway concepts (see [hermes_messaging_gateway_index](hermes_messaging_gateway_architecture.md)).

## Mention & Trigger Behavior

The `slack:` block controls when the bot engages in channels. `require_mention` is the default channel gate; `strict_mention` disables Slack's thread auto-engagement; `mention_patterns` adds custom trigger phrases; `reply_prefix` prepends text to every outgoing message.

```yaml
slack:
  # Require @mention in channels (this is the default behavior;
  # the Slack adapter enforces @mention gating in channels regardless,
  # but you can set this explicitly for consistency with other platforms)
  require_mention: true

  # Prevent thread auto-engagement: only reply to channel messages that
  # contain an explicit @mention. With this OFF (default), Slack can
  # "auto-engage" — remembering past mentions in a thread and following
  # up on bot-message replies, and resuming active sessions without a
  # fresh mention. With strict_mention ON, every new channel message
  # must @mention the bot before Hermes will respond.
  strict_mention: false

  # Custom mention patterns that trigger the bot
  # (in addition to the default @mention detection)
  mention_patterns:
    - "hey hermes"
    - "hermes,"

  # Text prepended to every outgoing message
  reply_prefix: ""
```

Source guidance: set `strict_mention: true` in busy workspaces where Slack's default "the bot remembers this thread" behavior surprises users (e.g., a long tech-support thread where the bot helped at the start and you'd rather it stay silent unless explicitly pinged again); DMs and active interactive sessions are unaffected. Conversely, you can **opt specific channels out of the mention requirement** via `SLACK_FREE_RESPONSE_CHANNELS` (comma-separated channel IDs) or `slack.free_response_channels` in `config.yaml`. Once the bot has an active session in a thread, subsequent thread replies do not require a mention; in DMs the bot always responds without a mention.

## Channel allowlist (`allowed_channels`)

Restrict the bot to a fixed set of Slack channels — useful when the bot is invited to many channels but should respond in only a few. When set, messages from channels NOT in the list are **silently ignored**, even if the bot is `@mentioned`. **DMs are exempt** from this filter, so authorized users can always reach the bot in a direct message.

```yaml
slack:
  allowed_channels:
    - "C0123456789"   # #ops
    - "C0987654321"   # #incident-response
```

Or via env var (comma-separated): `SLACK_ALLOWED_CHANNELS="C0123456789,C0987654321"`.

Behavior:

- Empty / unset → no restriction (fully backward compatible).
- Non-empty → the channel ID must be on the list, or the message is dropped **before any other gating** (mention requirement, `free_response_channels`, etc.) runs.
- Slack channel IDs start with `C` (public), `G` (private), or `D` (DM). Look them up via the Slack UI's "Open channel details" → "About" panel, or via the API.

## Unauthorized User Handling

The `slack.unauthorized_dm_behavior` key decides what happens when an unauthorized user (not in `SLACK_ALLOWED_USERS`) DMs the bot: `"pair"` prompts them for a pairing code (the default), `"ignore"` silently drops the message. This can also be set globally for all platforms (`unauthorized_dm_behavior: "pair"` at the top level), and the platform-specific setting under `slack:` takes precedence over the global one. The pairing-code handshake itself is a gateway concept (see [hermes_messaging_gateway_index](hermes_messaging_gateway_architecture.md)).

## Voice Transcription

The global `stt_enabled: true` setting (top-level) enables/disables automatic transcription of incoming voice messages. When `true` (the default), incoming audio messages are automatically transcribed using the configured STT provider before being processed by the agent. The STT provider options (local `faster-whisper`, Groq Whisper, OpenAI Whisper) and the media config cluster are owned by the SP08/SP02 media-settings docs ([hermes_messaging_media_settings](hermes_messaging_media_settings.md)); see also the Voice Messages section below.

## Full Example

```yaml
# Global gateway settings
group_sessions_per_user: true
unauthorized_dm_behavior: "pair"
stt_enabled: true

# Slack-specific settings
slack:
  require_mention: true
  unauthorized_dm_behavior: "pair"

# Platform config
platforms:
  slack:
    reply_to_mode: "first"
    extra:
      reply_in_thread: true
      reply_broadcast: false
```

## Home Channel

Set `SLACK_HOME_CHANNEL=C01234567890` (an env var) to a channel ID where Hermes delivers scheduled messages, cron job results, and other proactive notifications. Find the channel ID via right-click the channel name → **View channel details** → scroll to the bottom. Make sure the bot has been **invited to the channel** (`/invite @Hermes Agent`). The proactive/cron delivery destination this feeds is described in the gateway index and the SP06 cron docs.

## Multi-Workspace Support

Hermes can connect to **multiple Slack workspaces** simultaneously from a single gateway instance; each workspace is authenticated independently with its own bot user ID. Provide multiple bot tokens as a **comma-separated list** in `SLACK_BOT_TOKEN` (one per workspace), while a single app-level token is still used for the Socket Mode connection. The same list can be set in config under `platforms.slack.token: "xoxb-workspace1-token,xoxb-workspace2-token"`.

### OAuth Token File

In addition to environment/config tokens, Hermes loads tokens from an **OAuth token file** at `~/.hermes/slack_tokens.json` — a JSON object mapping each team ID (e.g. `"T01ABC2DEF3"`) to a token entry with a `token` (`xoxb-...`) and `team_name`. Tokens from this file are merged with any tokens from `SLACK_BOT_TOKEN`; duplicate tokens are automatically deduplicated. How it works: the **first token** in the list is the primary token used for the Socket Mode connection (AsyncApp); each token is authenticated via `auth.test` on startup, and the gateway maps each `team_id` to its own `WebClient` and `bot_user_id`. When a message arrives, Hermes uses the correct workspace-specific client to respond, and the primary `bot_user_id` (from the first token) is used for backward compatibility with features that expect a single bot identity.

## Voice Messages

Hermes supports voice on Slack: **incoming** voice/audio messages are automatically transcribed using the configured STT provider (local `faster-whisper`, Groq Whisper via `GROQ_API_KEY`, or OpenAI Whisper via `VOICE_TOOLS_OPENAI_KEY`), and **outgoing** TTS responses are sent as audio file attachments. The STT/TTS provider configuration is owned by the SP08 media/voice docs.

## Per-Channel Prompts

Assign ephemeral system prompts to specific Slack channels. The prompt is injected at runtime on every turn — never persisted to transcript history — so changes take effect immediately.

```yaml
slack:
  channel_prompts:
    "C01RESEARCH": |
      You are a research assistant. Focus on academic sources,
      citations, and concise synthesis.
    "C02ENGINEERING": |
      Code review mode. Be precise about edge cases and
      performance implications.
```

Keys are Slack channel IDs (find them via channel details → "About" → scroll to bottom). All messages in the matching channel get the prompt injected as an ephemeral system instruction.

## Per-Channel Skill Bindings

Auto-load a skill whenever a new session starts in a specific channel or DM. Unlike per-channel prompts (injected on every turn), skill bindings inject the skill content as a user message at **session start** — it becomes part of the conversation history and does not need to be reloaded on subsequent turns. This is ideal for DMs or channels with a dedicated purpose (flashcards, a domain-specific Q&A bot, a support triage channel) where you don't want the model's own skill selector to decide whether to load on every short reply.

```yaml
slack:
  channel_skill_bindings:
    # DM channel — always runs in "german-flashcards" mode
    - id: "D0ATH9TQ0G6"
      skills:
        - german-flashcards
    # Research channel — preload multiple skills in order
    - id: "C01RESEARCH"
      skills:
        - arxiv
        - writing-plans
    # Short form: single skill as a string
    - id: "C02SUPPORT"
      skill: hubspot-on-demand
```

Notes from the source:

- The binding matches by channel ID. For threaded messages in a bound channel, the thread inherits the parent channel's binding.
- The skill is loaded only at session start (new session or after auto-reset). If you change the binding, run `/new` or wait for the session to auto-reset for it to take effect.
- Combine with `channel_prompts` for per-channel tone/constraints on top of the skill's instructions.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/slack.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack
**Last Updated**: 2026-06-19
**Status**: Active
