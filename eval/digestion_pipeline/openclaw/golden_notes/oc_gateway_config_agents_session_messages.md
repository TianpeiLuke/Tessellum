---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - config_agents
keywords:
  - openclaw session config
  - session scope dmScope reset
  - messages responsePrefix ackReaction
  - inbound debounce queue
  - messages tts config
  - talk voice mode config
  - elevenlabs tts provider
  - realtime voice transport
topics:
  - OpenClaw
  - Agent Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-agents
access_control_group: ["general"]
---

# OpenClaw — Session, Messages, and Talk Configuration

## Overview

This note is the configuration procedure for the `session.*`, `messages.*`, and `talk.*` keys of OpenClaw's `gateway/config-agents` reference page — the session-grouping/reset/maintenance block, the message-delivery block (response prefix, ack reaction, inbound debounce, queue, and TTS), and the Talk (voice) mode block. It covers how to scope and reset sessions, how to shape and acknowledge replies, how rapid inbound messages are batched, and how text-to-speech and Talk voice providers are configured. The model/media, runtime-resilience, and routing keys of the same page are covered by sibling notes; this note owns only `## Session`, `## Messages`, and `## Talk`.

## Session

The `session.*` block controls how messages are grouped into sessions, when sessions reset, cross-channel identity links, store location, maintenance/retention, and thread bindings.

```json5
{
  session: {
    scope: "per-sender",
    dmScope: "main", // main | per-peer | per-channel-peer | per-account-channel-peer
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      mode: "daily", // daily | idle
      atHour: 4,
      idleMinutes: 60,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    maintenance: {
      mode: "enforce", // enforce (default) | warn
      pruneAfter: "30d",
      maxEntries: 500,
      resetArchiveRetention: "30d", // duration or false
      maxDiskBytes: "500mb", // optional hard budget
      highWaterBytes: "400mb", // optional cleanup target
    },
    threadBindings: {
      enabled: true,
      idleHours: 24, // default inactivity auto-unfocus in hours (`0` disables)
      maxAgeHours: 0, // default hard max age in hours (`0` disables)
    },
    mainKey: "main", // legacy (runtime always uses "main")
    agentToAgent: { maxPingPongTurns: 5 },
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

### Scoping and identity

`scope` is the base session-grouping strategy for group-chat contexts: `per-sender` (default) gives each sender an isolated session within a channel context, and `global` makes all participants in a channel context share a single session (use only when shared context is intended). `dmScope` controls how DMs are grouped: `main` shares the main session across all DMs, `per-peer` isolates by sender id across channels, `per-channel-peer` isolates per channel + sender (recommended for multi-user inboxes), and `per-account-channel-peer` isolates per account + channel + sender (recommended for multi-account). `identityLinks` maps canonical ids to provider-prefixed peers for cross-channel session sharing; dock commands such as `/dock_discord` use the same map to switch the active session's reply route to another linked channel peer. `mainKey` is a legacy field — the runtime always uses `"main"` for the main direct-chat bucket.

### Reset, send policy, and agent-to-agent

`reset` is the primary reset policy: `daily` resets at `atHour` local time, `idle` resets after `idleMinutes`, and when both are configured whichever expires first wins. Daily-reset freshness uses the session row's `sessionStartedAt`; idle-reset freshness uses `lastInteractionAt`. Background/system-event writes (heartbeat, cron wakeups, exec notifications, gateway bookkeeping) can update `updatedAt` but do NOT keep daily/idle sessions fresh. `resetByType` sets per-type overrides for `direct`, `group`, and `thread` (legacy `dm` is accepted as an alias for `direct`). `sendPolicy` matches by `channel`, `chatType` (`direct|group|channel`, with legacy `dm` alias), `keyPrefix`, or `rawKeyPrefix`, and the first deny wins. `agentToAgent.maxPingPongTurns` caps reply-back turns between agents during agent-to-agent exchanges (integer, range `0`-`20`, default `5`; `0` disables ping-pong chaining).

### Maintenance and thread bindings

`maintenance` controls session-store cleanup + retention: `mode` is `enforce` (applies cleanup, default) or `warn` (warnings only); `pruneAfter` is the age cutoff for stale entries (default `30d`); `maxEntries` is the maximum number of entries in `sessions.json` (default `500`, with `openclaw sessions cleanup --enforce` applying the cap immediately); `resetArchiveRetention` is retention for `*.reset.<timestamp>` transcript archives (defaults to `pruneAfter`, set `false` to disable); `maxDiskBytes` is an optional sessions-directory disk budget (logs in `warn` mode, removes oldest artifacts/sessions first in `enforce` mode); and `highWaterBytes` is the optional target after budget cleanup (defaults to `80%` of `maxDiskBytes`). The deprecated `rotateBytes` is ignored and removed by `openclaw doctor --fix`. `threadBindings` sets global defaults for thread-bound sessions: `enabled` is the master default switch (providers can override; Discord uses `channels.discord.threadBindings.enabled`); `idleHours` is the default inactivity auto-unfocus in hours (`0` disables); `maxAgeHours` is the default hard max age in hours (`0` disables); `spawnSessions` gates creating thread-bound work sessions from `sessions_spawn` and ACP thread spawns (defaults to `true` when thread bindings are enabled); and `defaultSpawnContext` is the default native-subagent context for thread-bound spawns (`"fork"` or `"isolated"`, defaulting to `"fork"`).

## Messages

The `messages.*` block shapes reply delivery: response prefix, ack reaction, the inbound/queue debounce settings, and TTS.

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions", // group-mentions | group-all | direct | all
    removeAckAfterReply: false,
    queue: {
      mode: "followup", // steer | followup | collect | interrupt
      debounceMs: 500,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: { whatsapp: "followup", telegram: "followup" },
    },
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: { whatsapp: 5000, slack: 1500 },
    },
  },
}
```

### Response prefix

Per-channel/account overrides are `channels.<channel>.responsePrefix` and `channels.<channel>.accounts.<id>.responsePrefix`. Resolution (most specific wins) is account → channel → global; `""` disables and stops the cascade, and `"auto"` derives `[{identity.name}]`. The template variables are `{model}` (short model name, e.g. `claude-opus-4-6`), `{modelFull}` (full model identifier, e.g. `anthropic/claude-opus-4-6`), `{provider}` (provider name, e.g. `anthropic`), `{thinkingLevel}` (current thinking level, e.g. `high`, `low`, `off`), and `{identity.name}` (agent identity name, same as `"auto"`). Variables are case-insensitive, and `{think}` is an alias for `{thinkingLevel}`.

### Ack reaction

The ack reaction defaults to the active agent's `identity.emoji`, otherwise `"👀"`; set `""` to disable. Per-channel overrides are `channels.<channel>.ackReaction` and `channels.<channel>.accounts.<id>.ackReaction`, and the resolution order is account → channel → `messages.ackReaction` → identity fallback. `ackReactionScope` is `group-mentions` (default), `group-all`, `direct`, or `all`. `removeAckAfterReply` removes the ack after reply on reaction-capable channels such as Slack, Discord, Telegram, WhatsApp, and iMessage. `messages.statusReactions.enabled` enables lifecycle status reactions on Slack, Discord, Telegram, and WhatsApp — on Slack and Discord, unset keeps status reactions enabled when ack reactions are active, while on Telegram and WhatsApp it must be set explicitly to `true`. `messages.statusReactions.emojis` overrides lifecycle emoji keys (`queued`, `thinking`, `compacting`, `tool`, `coding`, `web`, `deploy`, `build`, `concierge`, `done`, `error`, `stallSoft`, and `stallHard`); Telegram allows only a fixed reaction set, so unsupported configured emoji fall back to the nearest supported status variant for that chat.

### Inbound debounce

Inbound debounce batches rapid text-only messages from the same sender into a single agent turn. Media/attachments flush immediately, and control commands bypass debouncing. `messages.inbound.debounceMs` defaults to `2000` (`0` disables), with per-channel overrides under `messages.inbound.byChannel` (e.g. `whatsapp: 5000`, `slack: 1500`).

### TTS (text-to-speech)

```json5
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all
      provider: "elevenlabs",
      summaryModel: "openai/gpt-5.4-mini",
      modelOverrides: { enabled: true },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      providers: {
        elevenlabs: {
          apiKey: "elevenlabs_api_key",
          baseUrl: "https://api.elevenlabs.io",
          speakerVoiceId: "voice_id",
          modelId: "eleven_multilingual_v2",
        },
        microsoft: {
          speakerVoice: "en-US-AvaMultilingualNeural",
          lang: "en-US",
          outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        },
        openai: {
          apiKey: "openai_api_key",
          baseUrl: "https://api.openai.com/v1",
          model: "gpt-4o-mini-tts",
          speakerVoice: "alloy",
        },
      },
    },
  },
}
```

`auto` controls the default auto-TTS mode (`off`, `always`, `inbound`, or `tagged`); `/tts on|off` can override local prefs, and `/tts status` shows the effective state. `summaryModel` overrides `agents.defaults.model.primary` for auto-summary. `modelOverrides` is enabled by default, and `modelOverrides.allowProvider` defaults to `false` (opt-in). API keys fall back to `ELEVENLABS_API_KEY`/`XI_API_KEY` and `OPENAI_API_KEY`. Bundled speech providers are plugin-owned, so if `plugins.allow` is set you must include each TTS provider plugin you want to use (for example `microsoft` for Edge TTS; the legacy `edge` provider id is accepted as an alias for `microsoft`). `providers.openai.baseUrl` overrides the OpenAI TTS endpoint, with resolution order config → `OPENAI_TTS_BASE_URL` → `https://api.openai.com/v1`; when it points to a non-OpenAI endpoint, OpenClaw treats it as an OpenAI-compatible TTS server and relaxes model/voice validation.

## Talk

`talk.*` configures Talk mode defaults for macOS/iOS/Android, including the voice provider, voice aliases, locale/timing, and the realtime voice transport.

```json5
{
  talk: {
    provider: "elevenlabs",
    providers: {
      elevenlabs: {
        speakerVoiceId: "elevenlabs_voice_id",
        voiceAliases: { Clawd: "EXAVITQu4vr4xnSDxMaL", Roger: "CwhRBWXzGAHq8TQ4Fs17" },
        modelId: "eleven_v3",
        outputFormat: "mp3_44100_128",
        apiKey: "elevenlabs_api_key",
      },
      mlx: { modelId: "mlx-community/Soprano-80M-bf16" },
      system: {},
    },
    consultThinkingLevel: "low",
    consultFastMode: true,
    speechLocale: "ru-RU",
    silenceTimeoutMs: 1500,
    interruptOnSpeech: true,
    realtime: {
      provider: "openai",
      providers: { openai: { model: "gpt-realtime-2", speakerVoice: "cedar" } },
      instructions: "Speak warmly and keep answers brief.",
      mode: "realtime",
      transport: "webrtc",
      brain: "agent-consult",
    },
  },
}
```

`talk.provider` must match a key in `talk.providers` when multiple Talk providers are configured. Legacy flat Talk keys (`talk.voiceId`, `talk.voiceAliases`, `talk.modelId`, `talk.outputFormat`, `talk.apiKey`) are compatibility-only, and `openclaw doctor --fix` rewrites persisted config into `talk.providers.<provider>`. Voice IDs fall back to `ELEVENLABS_VOICE_ID` or `SAG_VOICE_ID`; `providers.*.apiKey` accepts plaintext strings or SecretRef objects; and the `ELEVENLABS_API_KEY` fallback applies only when no Talk API key is configured. `providers.*.voiceAliases` lets Talk directives use friendly names. `providers.mlx.modelId` selects the Hugging Face repo used by the macOS local MLX helper (defaulting to `mlx-community/Soprano-80M-bf16`), and macOS MLX playback runs through the bundled `openclaw-mlx-tts` helper when present, or an executable on `PATH` (`OPENCLAW_MLX_TTS_BIN` overrides the helper path for development).

`consultThinkingLevel` controls the thinking level for the full OpenClaw agent run behind Control UI Talk realtime `openclaw_agent_consult` calls (leave unset to preserve normal session/model behavior), and `consultFastMode` sets a one-shot fast-mode override for those consults without changing the session's normal fast-mode setting. `speechLocale` sets the BCP 47 locale id used by iOS/macOS Talk speech recognition (unset uses the device default), and `silenceTimeoutMs` controls how long Talk mode waits after user silence before sending the transcript (unset keeps the platform default pause window — 700 ms on macOS and Android, 900 ms on iOS). `realtime.instructions` appends provider-facing system instructions to OpenClaw's built-in realtime prompt so voice style can be configured without losing default `openclaw_agent_consult` guidance, and `realtime.consultRouting` controls Gateway relay fallback when the realtime provider produces a final user transcript without `openclaw_agent_consult`: `provider-direct` preserves direct provider replies, while `force-agent-consult` routes the finalized request through OpenClaw.

**Source**: OpenClaw documentation — `gateway/config-agents` §§ Session / Messages / Talk (mirror `inbox/openclaw_docs/gateway/config-agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
