---
tags:
  - resource
  - documentation
  - hermes_agent
  - voice
  - messaging
keywords:
  - gateway voice reply
  - discord voice channels
  - telegram voice bubble
  - privileged gateway intents
  - SSRC user mapping
  - DISCORD_ALLOWED_USERS
topics:
  - Hermes Agent
  - Voice Mode
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode
access_control_group: ["general"]
---

# Hermes Gateway Voice Reply & Discord Voice Channels

## Overview

This is the **gateway / messaging-platform half** of Hermes Agent voice mode — the second of two procedural arcs split from the source `voice-mode.md` page (the local-microphone CLI push-to-talk loop is the sibling [hermes_voice_mode_cli](hermes_voice_mode_cli.md)). It covers two distinct runtime surfaces that the messaging gateway exposes:

1. **Auto Voice Reply** — when the gateway is connected to Telegram or Discord, the agent can send a *spoken* audio reply alongside (or instead of) its text response, delivered as a native voice bubble (Opus/OGG). This works in DMs and text channels and is toggled per-conversation with `/voice` commands.
2. **Discord Voice Channels (VC)** — the most immersive feature: the bot **joins** a Discord voice channel, **listens** to each user's audio stream, **transcribes** their speech via Whisper STT, **processes** through the full agent pipeline (session, tools, memory), and **speaks** the reply back in the channel.

Both surfaces run inside `hermes gateway` (started via `hermes gateway` / `hermes gateway setup`) and reuse the same STT and TTS subsystems documented in [hermes_stt_transcription](hermes_stt_transcription.md) and [hermes_tts_providers](hermes_tts_providers.md). Per-platform bot setup (token/intents/invite) is owned by the messaging guides; the `voice:` mode config block is owned by the SP02 config note [hermes_messaging_media_settings](hermes_messaging_media_settings.md). This note documents the runtime procedure, the Discord-VC permission/intent wiring, and the gateway/VC troubleshooting rows.

## Gateway Voice Reply (Telegram & Discord)

Start the gateway to connect to your configured messaging platforms (bot setup itself — Telegram/Discord token, server invite — is covered in the platform guides; this page assumes the bots are already connected):

```bash
hermes gateway        # Start the gateway (connects to configured platforms)
hermes gateway setup  # Interactive setup wizard for first-time configuration
```

### Discord: Channels vs DMs

The bot supports two interaction modes on Discord:

- **Direct Message (DM)** — open the bot's profile → "Message". No @mention required; works immediately. Recommended for personal use — voice replies and all commands work the same as in channels.
- **Server Channel** — type in a text channel where the bot is present; the bot only responds when you @mention it (e.g. `@hermesbyt4 hello`). Select the **bot user** from the mention popup, not the role with the same name. The bot must first be invited to the server.

To disable the mention requirement in server channels, set `DISCORD_REQUIRE_MENTION=false` in `~/.hermes/.env`, or mark specific channels as free-response with `DISCORD_FREE_RESPONSE_CHANNELS=123456789,987654321`.

### Commands and Modes

The `/voice` slash commands work in both Telegram and Discord (DMs and text channels):

```
/voice          Toggle voice mode on/off
/voice on       Voice replies only when you send a voice message
/voice tts      Voice replies for ALL messages
/voice off      Disable voice replies
/voice status   Show current setting
```

These map to three persisted modes (the voice-mode setting survives gateway restarts):

| Mode | Command | Behavior |
|------|---------|----------|
| `off` | `/voice off` | Text only (default) |
| `voice_only` | `/voice on` | Speaks reply **only** when you send a voice message |
| `all` | `/voice tts` | Speaks reply to **every** message |

### Platform Delivery

The spoken reply is delivered as a native voice bubble per platform; `ffmpeg` performs MP3 → Opus conversion when needed:

- **Telegram** — voice bubble (Opus/OGG), plays inline in chat.
- **Discord** — native voice bubble (Opus/OGG), plays inline like a user voice message; **falls back to a file attachment** if the voice-bubble API fails.

## Discord Voice Channels

The bot joins a Discord voice channel, listens to users speaking, transcribes their speech, processes it through the agent, and speaks the reply back in the VC.

### Setup — 1. Discord Bot Permissions

If you already have a text-configured Discord bot, add the voice permissions in the Discord Developer Portal → your application → **Installation** → **Default Install Settings** → **Guild Install**. Add **Connect** (join voice channels, required), **Speak** (play TTS audio, required), and **Use Voice Activity** (detect speaking, recommended) on top of the existing text permissions.

The permissions integer changes from text-only `274878286912` to **text + voice `274881432640`** (text permissions plus Connect and Speak). **Re-invite** the bot with the updated permissions URL — re-inviting a bot to a server it is already in updates its permissions without removing it or losing any data/configuration:

```
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=274881432640
```

Replace `YOUR_APP_ID` with the Application ID from the Developer Portal.

### Setup — 2. Privileged Gateway Intents

In the Developer Portal → your application → **Bot** → **Privileged Gateway Intents**, enable the three intents:

| Intent | Purpose |
|--------|---------|
| **Presence Intent** | Detect user online/offline status |
| **Server Members Intent** | Resolve usernames in `DISCORD_ALLOWED_USERS` to numeric IDs (conditional) |
| **Message Content Intent** | Read text message content in channels |

**Message Content Intent is required.** **Server Members Intent is only needed if `DISCORD_ALLOWED_USERS` uses usernames** — if you use numeric user IDs you can leave it OFF. Critically, the voice-channel **SSRC → user_id mapping comes from Discord's SPEAKING opcode on the voice websocket** and does **not** require the Server Members Intent.

### Setup — 3. Opus Codec & 4. Environment Variables

The Opus codec library must be installed on the gateway host (`brew install opus` on macOS, `sudo apt install libopus0` on Ubuntu/Debian). The bot auto-loads the codec from `/opt/homebrew/lib/libopus.dylib` (macOS) or `libopus.so.0` (Linux). Then add the Discord bot env vars (STT/TTS keys optional — the local Whisper STT and Edge/NeuTTS providers need no key):

```bash
# ~/.hermes/.env
DISCORD_BOT_TOKEN=your-bot-token
DISCORD_ALLOWED_USERS=your-user-id
# GROQ_API_KEY=your-key            # Optional cloud STT (fast, free tier)
# ELEVENLABS_API_KEY=***           # Optional premium TTS
# VOICE_TOOLS_OPENAI_KEY=***       # Optional OpenAI TTS / Whisper
```

Start the gateway with `hermes gateway`; the bot comes online in Discord within a few seconds.

### VC Commands and How It Works

Use these in the Discord text channel where the bot is present (you must already be in a voice channel — the bot joins the same VC you are in):

```
/voice join      Bot joins your current voice channel
/voice channel   Alias for /voice join
/voice leave     Bot disconnects from voice channel
/voice status    Show voice mode and connected channel
```

Once joined, the per-turn loop is: (1) **Listens** to each user's audio stream independently; (2) **Detects silence** — 1.5s of silence after at least 0.5s of speech triggers processing; (3) **Transcribes** the audio via Whisper STT (local, Groq, or OpenAI); (4) **Processes** through the full agent pipeline (session, tools, memory); (5) **Speaks** the reply back in the voice channel via TTS.

### Text-Channel Integration, Echo Prevention & Access Control

While the bot is in a voice channel, transcripts appear in the text channel as `[Voice] @user: what you said`, and agent responses are sent as text in the channel **and** spoken in the VC; the text channel used is the one where `/voice join` was issued. For **echo prevention**, the bot automatically pauses its audio listener while playing TTS replies, so it does not hear and re-process its own output.

**Access control** gates the VC by user: only users listed in `DISCORD_ALLOWED_USERS` can interact via voice; other users' audio is silently ignored.

```bash
# ~/.hermes/.env
DISCORD_ALLOWED_USERS=284102345871466496
```

## Troubleshooting (Gateway & Voice Channel)

- **Bot doesn't respond in Discord server channels** — the bot requires an @mention by default in server channels. Type `@` and select the **bot user** (with the #discriminator), not the role of the same name; or use DMs (no mention needed); or set `DISCORD_REQUIRE_MENTION=false` in `~/.hermes/.env`.
- **Bot joins VC but doesn't hear me** — check your Discord user ID is in `DISCORD_ALLOWED_USERS`; make sure you are not muted in Discord; the bot needs a SPEAKING event from Discord before it can map your audio, so start speaking within a few seconds of joining.
- **Bot hears me but doesn't respond** — verify STT is available (install `faster-whisper`, no key, or set `GROQ_API_KEY` / `VOICE_TOOLS_OPENAI_KEY`); check the LLM model is configured and accessible; review gateway logs with `tail -f ~/.hermes/logs/gateway.log`.
- **Bot responds in text but not in voice channel** — the TTS provider may be failing (check API key and quota); Edge TTS (free, no key) is the default fallback; check logs for TTS errors.

**Source**: `inbox/hermes_agent_docs/user-guide/features/voice-mode.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode
**Last Updated**: 2026-06-19
**Status**: Active
