---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - discord
keywords:
  - openclaw discord voice
  - discord voice channels vc join
  - voice mode agent-proxy stt-tts bidi
  - voice.realtime requireWakeName barge-in
  - follow users in voice
  - discord voice messages waveform
  - daveEncryption decryptionFailureTolerance
  - openclaw_agent_consult voice
topics:
  - OpenClaw
  - Discord Voice
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/discord
access_control_group: ["general"]
---

# OpenClaw — Discord Voice (Voice Channels, Follow Users, Voice Messages)

## Overview

This note is the procedure for OpenClaw's two Discord voice surfaces — realtime **voice channels** (continuous conversations) and **voice message attachments** (the waveform-preview format) — mirroring the **Voice** section of the `channels/discord` source page (its `Voice channels`, `Follow users in voice`, and `Voice messages` H3 subsections). It covers the setup checklist and `/vc` commands, the `channels.discord.voice` config block, the three conversation modes (`agent-proxy` / `stt-tts` / `bidi`), wake-name gating, barge-in/echo handling, follow-users behavior, the codec/STT-TTS pipeline, diagnostic logs, and OGG/Opus voice messages. Voice transport/provider internals (STT/TTS providers) are linked out, not redefined here.

## Voice channels — setup checklist and `/vc` commands

Discord voice is opt-in for text-only configs: set `channels.discord.voice.enabled=true` (or keep an existing `channels.discord.voice` block) to enable `/vc` commands, the voice runtime, and the `GuildVoiceStates` gateway intent. `channels.discord.intents.voiceStates` can explicitly override voice-state intent subscription (unset, it follows effective voice enablement). Setup checklist: (1) enable Message Content Intent in the Discord Developer Portal; (2) enable Server Members Intent when role/user allowlists are used; (3) invite the bot with `bot` and `applications.commands` scopes; (4) grant Connect, Speak, Send Messages, and Read Message History in the target voice channel; (5) enable native commands (`commands.native` or `channels.discord.commands.native`); (6) configure `channels.discord.voice`.

Use `/vc join|leave|status` to control sessions — the command uses the account default agent and follows the same allowlist/group-policy rules as other commands. To inspect the bot's permissions before joining, run `openclaw channels capabilities --channel discord --target channel:<voice-channel-id>`.

```bash
/vc join channel:<voice-channel-id>
/vc status
/vc leave
```

## Auto-join config and core voice fields

An auto-join `channels.discord.voice` block configures the voice model, startup auto-join channels, the residency allowlist, encryption, timeouts, and the realtime session:

```json5
{
  channels: {
    discord: {
      voice: {
        enabled: true,
        model: "openai/gpt-5.5",
        autoJoin: [
          {
            guildId: "123456789012345678",
            channelId: "234567890123456789",
          },
        ],
        allowedChannels: [
          {
            guildId: "123456789012345678",
            channelId: "234567890123456789",
          },
        ],
        daveEncryption: true,
        decryptionFailureTolerance: 24,
        connectTimeoutMs: 30000,
        reconnectGraceMs: 15000,
        realtime: {
          provider: "openai",
          model: "gpt-realtime-2",
          speakerVoice: "cedar",
        },
      },
    },
  },
}
```

Key fields: `voice.allowedChannels` is an optional residency allowlist — unset allows `/vc join` into any authorized channel; when set, `/vc join`, startup auto-join, and bot voice-state moves are restricted to the listed `{ guildId, channelId }` entries (an empty array denies all joins), and if Discord moves the bot outside it OpenClaw leaves and rejoins the configured auto-join target. With multiple `voice.autoJoin` entries for one guild, OpenClaw joins the last configured channel. `voice.connectTimeoutMs` is the initial `@discordjs/voice` Ready wait for joins (default `30000`); `voice.reconnectGraceMs` is how long OpenClaw waits for a disconnected session to reconnect before destroying it (default `15000`); `voice.daveEncryption` and `voice.decryptionFailureTolerance` pass through to `@discordjs/voice` join options (defaults `true` / `24`). `voice.model` overrides the OpenClaw agent brain for voice responses and realtime consults (unset inherits the routed agent model; separate from `voice.realtime.model`), and `voice.agentSession` controls which conversation receives voice turns — unset for the voice channel's own session, or `{ mode: "target", target: "channel:<text-channel-id>" }` to make the voice channel the mic/speaker extension of an existing text channel session. Per-channel `systemPrompt` overrides apply to voice transcript turns, which derive owner status from Discord `allowFrom` (or `dm.allowFrom`) while agent tool visibility follows the routed session's tool policy.

## Conversation modes: agent-proxy, stt-tts, bidi

`voice.mode` controls the conversation path. The default `agent-proxy` runs a realtime voice front end that handles turn timing, interruption, and playback, delegates substantive work to the routed agent through `openclaw_agent_consult`, and treats the result like a typed Discord prompt; it routes speech through `discord-voice`, preserving normal owner/tool authorization but hiding the agent `tts` tool since Discord voice owns playback. By default it gives the consult full owner-equivalent tool access for owner speakers (`voice.realtime.toolPolicy: "owner"`) and prefers consulting the agent before substantive answers (`voice.realtime.consultPolicy: "always"`); in `always` mode the realtime layer does not auto-speak filler before the consult answer, and later forced consult answers are queued until playback idles. `stt-tts` keeps the older batch STT plus TTS flow (STT uses `tools.media.audio`; `voice.model` does not affect transcription); `bidi` lets the realtime model converse directly while still exposing `openclaw_agent_consult`.

In realtime modes, `voice.realtime.provider`/`model`/`speakerVoice` configure the realtime audio session (for OpenAI Realtime 2 plus the Codex brain, use `voice.realtime.model: "gpt-realtime-2"` and `voice.model: "openai/gpt-5.5"`). `voice.tts` overrides `messages.tts` for `stt-tts` playback only — realtime modes use `voice.realtime.speakerVoice`; for an OpenAI voice set `voice.tts.provider: "openai"` and `voice.tts.providers.openai.speakerVoice` (`cedar` is a good choice on the current OpenAI TTS model). Realtime modes inject small `IDENTITY.md`, `USER.md`, and `SOUL.md` profile files into the realtime provider instructions by default so fast direct turns keep the routed agent's identity/user-grounding/persona; set `voice.realtime.bootstrapContextFiles` to a subset to customize or `[]` to disable (only those profile files are supported — `AGENTS.md` stays in normal agent context). The injected profile context does not replace `openclaw_agent_consult` for workspace work, current facts, memory lookup, or tool-backed actions.

## Wake names, barge-in, and echo handling

In OpenAI `agent-proxy` realtime mode, set `voice.realtime.requireWakeName: true` to keep realtime voice silent until a transcript starts or ends with a wake name; wake names must be one or two words, and if `voice.realtime.wakeNames` is unset OpenClaw uses the routed agent `name` plus `OpenClaw` (falling back to the agent id). Wake-name gating disables provider auto-response, routes accepted turns through the consult path, and gives a short spoken acknowledgement when a leading wake name is recognized from partial transcription. The OpenAI provider accepts current Realtime 2 event names and legacy Codex-compatible aliases, so compatible snapshots can drift without dropping audio.

`voice.realtime.bargeIn` controls whether Discord speaker-start events interrupt active realtime playback (unset follows the provider's input-audio interruption setting), and `voice.realtime.minBargeInAudioEndMs` is the minimum assistant playback duration before an OpenAI barge-in truncates audio (default `250`; `0` for immediate interruption in low-echo rooms, higher for echo-heavy setups). In `stt-tts` mode playback does not stop when another user speaks — to avoid feedback loops OpenClaw ignores new capture while TTS plays; realtime modes forward speaker starts as barge-in signals. For echo-heavy rooms set `voice.realtime.providers.openai.interruptResponseOnInputAudio: false` to stop OpenAI auto-interrupting on input audio, add `voice.realtime.bargeIn: true` if you still want speaker-start events to interrupt, and note the bridge ignores truncations shorter than `minBargeInAudioEndMs` as likely echo/noise. `voice.captureSilenceGraceMs` is how long OpenClaw waits after a speaker stops before finalizing that segment for STT (default `2000`; raise it if Discord splits pauses into choppy partial transcripts). In `agent-proxy` mode, forced consult fallback skips likely-incomplete fragments (text ending in `...` or a trailing connector) plus non-actionable closings like "be right back" or "bye", logging `forced agent consult skipped reason=...`.

## Follow users in voice

Use `voice.followUsers` when you want the voice bot to stay with one or more known Discord users instead of joining a fixed channel or waiting for `/vc join`:

```json5
{
  channels: {
    discord: {
      voice: {
        enabled: true,
        followUsersEnabled: true,
        followUsers: ["discord:123456789012345678"],
        allowedChannels: [
          {
            guildId: "123456789012345678",
            channelId: "234567890123456789",
          },
        ],
      },
    },
  },
}
```

Behavior: `followUsers` accepts raw Discord user IDs and `discord:<id>` values (both normalized before matching voice-state events); `followUsersEnabled` defaults to `true` when `followUsers` is configured (set `false` to keep the saved list but stop following). When a followed user joins an allowed channel OpenClaw joins it, moves with them, and leaves when the active followed user disconnects; if multiple followed users are in the same guild and the active one leaves, OpenClaw moves to another tracked user's channel before leaving (if several move at once, the latest voice-state event wins). `allowedChannels` still applies — a followed user in a disallowed channel is ignored. OpenClaw reconciles missed voice-state events on startup and at a bounded interval (sampling guilds, capping REST lookups per run, so very large lists may take more than one interval to converge); if Discord or an admin moves the bot while following, OpenClaw rebuilds the session and preserves follow ownership when the destination is allowed, and follow-owned sessions keep ownership through DAVE leave/rejoin recovery. Choose between join modes: `followUsers` for personal/operator setups; `autoJoin` for fixed-room bots present even with no tracked user; `/vc join` for one-off joins.

## Codec and STT-plus-TTS pipeline

OpenClaw uses the bundled `libopus-wasm` codec (pinned WebAssembly build, no native opus addons) for Discord voice receive and realtime raw PCM playback; receive logs show `discord voice: opus decoder: libopus-wasm`. Realtime playback encodes raw 48 kHz stereo PCM to Opus before handing packets to `@discordjs/voice`; file/provider-stream playback transcodes to raw PCM with ffmpeg. The `stt-tts` pipeline: Discord PCM capture → WAV temp file; `tools.media.audio` handles STT (e.g. `openai/gpt-4o-mini-transcribe`); the transcript goes through Discord ingress/routing while the response LLM runs with a voice-output policy that hides the agent `tts` tool (Discord voice owns final TTS playback); `voice.model`, when set, overrides only this turn's response LLM; and `voice.tts` merges over `messages.tts` — streaming providers feed the player directly (ElevenLabs streams from the provider response), otherwise the synthesized audio file is played. Credentials resolve per component: LLM route auth (`voice.model`), STT auth (`tools.media.audio`), TTS auth (`messages.tts`/`voice.tts`), realtime auth (`voice.realtime.providers`).

## Mode examples and agent-session targeting

With no `voice.agentSession` block, each voice channel gets its own routed OpenClaw session; the realtime model is only the front end, substantive requests go to the configured agent, and if the realtime model produces a final transcript without calling the consult tool, OpenClaw forces the consult as a fallback. A `bidi` config sets `mode: "bidi"` with a `realtime` block carrying `toolPolicy: "safe-read-only"` and `consultPolicy: "always"`; a legacy `stt-tts` config sets `mode: "stt-tts"` plus a `tts.provider`/`tts.providers.openai` block. To make a voice channel an extension of an existing channel session, set `voice.agentSession` to `{ mode: "target", target: ... }`:

```json5
{
  channels: {
    discord: {
      voice: {
        enabled: true,
        mode: "agent-proxy",
        model: "openai/gpt-5.5",
        agentSession: {
          mode: "target",
          target: "channel:123456789012345678",
        },
        realtime: {
          provider: "openai",
          model: "gpt-realtime-2",
          speakerVoice: "cedar",
        },
      },
    },
  },
}
```

In `agent-proxy` mode the bot joins the configured voice channel, but agent turns use the target channel's routed session and agent, and the realtime session speaks the result back into the voice channel. While a delegated run is active, new voice transcripts are treated as live run control — phrases like "status", "cancel that", or "when you're done also check tests" are classified as status, cancel, steering, or follow-up input and the outcomes are spoken back. Useful `target` forms: `channel:<id>` or bare `<id>` (text channel session), and `dm:<id>` or `user:<id>` (direct-message session).

## Voice diagnostics and debugging

Verbose Discord voice logs include a bounded one-line STT transcript preview per accepted speaker segment. OpenClaw watches receive decrypt failures and auto-recovers by leaving/rejoining the channel after repeated failures in a short window; if receive logs repeatedly show `DecryptionFailed(UnencryptedWhenPassthroughDisabled)` after updating, collect a dependency report and logs (the bundled `@discordjs/voice` line includes the upstream padding fix from discord.js PR #11449, which closed issue #11419). `The operation was aborted` receive events are expected when OpenClaw finalizes a captured segment — verbose diagnostics, not warnings. To debug cut-off audio, read the realtime logs as a timeline: `realtime audio playback started` → `realtime speaker turn opened` (with active playback + `bargeIn`, may be followed by `barge-in detected source=speaker-start`) → `realtime input audio started` (`outputActive=true` = mic input arrived during playback) → `barge-in detected source=active-speaker-audio` → `barge-in requested reason=...` → `realtime audio playback stopped reason=...` (`barge-in`, `player-idle`, `provider-clear-audio`, `forced-agent-consult`, `stream-close`, `session-close`) → `realtime speaker turn closed` (`hasAudio=false` = no usable audio reached the bridge; `interruptedPlayback=true` = the turn triggered barge-in). Common patterns: immediate cut-off with `source=active-speaker-audio` and small `outputAudioMs` usually means speaker echo entering the mic (raise `minBargeInAudioEndMs`, lower volume, use headphones, or disable `interruptResponseOnInputAudio`); `capture ignored during playback (barge-in disabled)` means input was dropped while assistant audio was active; and `barge-in ignored ... outputActive=false` means VAD reported speech with no active playback to interrupt.

## Voice messages

Discord voice messages show a waveform preview and require OGG/Opus audio. OpenClaw generates the waveform automatically but needs `ffmpeg` and `ffprobe` on the gateway host. Provide a **local file path** (URLs are rejected), omit text content (Discord rejects text + voice message in one payload), and note any audio format is accepted — OpenClaw converts to OGG/Opus. Send a voice message with the message tool:

```bash
message(action="send", channel="discord", target="channel:123", path="/path/to/audio.mp3", asVoice=true)
```

**Source**: OpenClaw documentation — `channels/discord` § Voice (mirror `inbox/openclaw_docs/channels/discord.md`)
**Last Updated**: 2026-06-22
**Status**: Active
