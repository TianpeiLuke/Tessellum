---
tags:
  - resource
  - documentation
  - hermes_agent
  - configuration
  - messaging
keywords:
  - tts stt voice configuration
  - display and streaming settings
  - group session isolation
  - quick commands human delay
  - discord browser web search backends
  - per-platform overrides
topics:
  - Hermes Agent
  - Configuration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
access_control_group: ["general"]
---

# Hermes Agent — Messaging, Media & Display Settings

## Overview

This note is the `config.yaml` reference for Hermes Agent's **messaging-, media-, and display-facing settings** — the section cluster of the large Configuration page that governs how the agent speaks, renders, and behaves across the CLI and the 20+ messaging-gateway platforms. It collects the `tts`/`stt`/`voice` audio knobs, the `display`/`streaming` rendering knobs (skin, tool-progress verbosity, runtime footer, file-mutation verifier, UI language), and the gateway-behavior blocks: group-session isolation, unauthorized-DM handling, zero-token quick commands, human-delay pacing, and the `discord`/`browser`/`web`/`timezone` backends. Each block is one setting cluster in `~/.hermes/config.yaml`; the underlying *features* (voice mode, browser automation, web search) are documented by their owning pages (SP08/SP11) — this note is the configuration surface, not the feature deep-dive.

## TTS Configuration

The `tts` block configures both the `text_to_speech` tool and spoken replies in voice mode (`/voice tts` in the CLI or messaging gateway). `provider` selects among `edge | elevenlabs | openai | minimax | mistral | gemini | xai | neutts`, and each provider has its own voice/model sub-block.

```yaml
tts:
  provider: "edge"              # "edge" | "elevenlabs" | "openai" | "minimax" | "mistral" | "gemini" | "xai" | "neutts"
  speed: 1.0                    # Global speed multiplier (fallback for all providers)
  edge:
    voice: "en-US-AriaNeural"   # 322 voices, 74 languages
    speed: 1.0                  # Speed multiplier (converted to rate percentage, e.g. 1.5 → +50%)
  elevenlabs:
    voice_id: "pNInz6obpgDQGcFmaJgB"
    model_id: "eleven_multilingual_v2"
  openai:
    model: "gpt-4o-mini-tts"
    voice: "alloy"              # alloy, echo, fable, onyx, nova, shimmer
    speed: 1.0                  # Speed multiplier (clamped to 0.25–4.0 by the API)
    base_url: "https://api.openai.com/v1"  # Override for OpenAI-compatible TTS endpoints
  gemini:
    model: "gemini-2.5-flash-preview-tts"   # or gemini-3.1-flash-tts-preview
    voice: "Kore"               # 30 prebuilt voices: Zephyr, Puck, Kore, Enceladus, etc.
    audio_tags: false           # Hidden Gemini 3.1 TTS audio-tag insertion
  xai:
    voice_id: "eve"             # xAI TTS voice
    language: "en"              # ISO 639-1
    sample_rate: 24000
  neutts:
    model: neuphonic/neutts-air-q4-gguf
    device: cpu
```

**Speed fallback hierarchy:** provider-specific speed (e.g. `tts.edge.speed`) → global `tts.speed` → `1.0` default. Set the global `tts.speed` to apply a uniform speed across all providers, or override per-provider for fine-grained control. (Source also lists `minimax` with `speed`/optional `base_url`, and `mistral` with `model`/`voice_id` — omitted here for brevity; see source.)

## Display Settings

The `display` block controls the CLI/TUI/gateway rendering surface — tool-progress verbosity, skin, streaming, cost/timestamps, the runtime footer, and the file-mutation verifier.

```yaml
display:
  tool_progress: all      # off | new | all | verbose
  tool_progress_command: false  # Enable /verbose slash command in messaging gateway
  platforms: {}           # Per-platform display overrides (see below)
  interim_assistant_messages: true  # Gateway: send natural mid-turn assistant updates as separate messages
  skin: default           # Built-in or custom CLI skin
  personality: "kawaii"  # Legacy cosmetic field still surfaced in some summaries
  resume_display: full    # full (show previous messages on resume) | minimal (one-liner only)
  show_reasoning: false   # Show model reasoning/thinking above each response (toggle with /reasoning show|hide)
  streaming: false        # Stream tokens to terminal as they arrive (real-time output)
  show_cost: false        # Show estimated $ cost in the CLI status bar
  timestamps: false       # Prefix user/assistant labels with [HH:MM] in the CLI / TUI transcript
  tool_preview_length: 0  # Max chars for tool call previews (0 = no limit)
  runtime_footer:         # Gateway: append a runtime-context footer to final replies
    enabled: false
    fields: ["model", "context_pct", "cwd"]
  file_mutation_verifier: true    # Append an advisory footer when write_file/patch calls failed this turn
  language: en            # UI language for static messages — en | zh | zh-hant | ja | de | es | fr | tr | uk | af | ko | it | ga | pt | ru | hu
```

The four `tool_progress` modes: `off` (silent, final response only), `new` (indicator only when the tool changes), `all` (every tool call with a short preview — the default), and `verbose` (full args, results, and debug logs). In the CLI, `/verbose` cycles the modes; to use `/verbose` on a messaging platform set `display.tool_progress_command: true`.

**File-mutation verifier** (default `true`): when a `write_file` or `patch` call failed during the turn and was never superseded by a successful write to the same path, Hermes appends a one-line advisory footer to the final response — catching the "batch of parallel patches, half silently fail, model summarises success" over-claim class. Set `file_mutation_verifier: false` (or `HERMES_FILE_MUTATION_VERIFIER=0`) to suppress.

**UI language** (`display.language`): translates a small set of static user-facing messages (the CLI approval prompt, a few gateway slash-command replies). It does **not** translate agent responses, log lines, tool output, or tracebacks — those stay English. Overridable per-session with `HERMES_LANGUAGE`. Unknown values fall back to English.

**Runtime-metadata footer (gateway only):** with `display.runtime_footer.enabled: true`, Hermes appends a small footer to the **final** message of each gateway turn (supported `fields`: `model`, `context_pct`, `cwd`). The `/footer` slash command toggles it at runtime; only the final message gets the footer, interim updates stay clean.

**Per-platform progress overrides:** `display.platforms` sets per-platform `tool_progress` (and per-platform `streaming`) — platforms without an override fall back to the global value. Valid keys: `telegram`, `discord`, `slack`, `signal`, `whatsapp`, `matrix`, `mattermost`, `email`, `sms`, `homeassistant`, `dingtalk`, `feishu`, `wecom`, `weixin`, `bluebubbles`, `qqbot`. The legacy `display.tool_progress_overrides` key is deprecated and migrated into `display.platforms` on first load. Signal can save the setting but cannot edit sent messages, so keep Signal `tool_progress: off`.

## Speech-to-Text (STT) and Voice Mode

The `stt` block selects the transcription backend; the `voice` block configures CLI push-to-talk.

```yaml
stt:
  provider: "local"            # "local" | "groq" | "openai" | "mistral"
  local:
    model: "base"              # tiny, base, small, medium, large-v3
  openai:
    model: "whisper-1"         # whisper-1 | gpt-4o-mini-transcribe | gpt-4o-transcribe

voice:
  record_key: "ctrl+b"         # Push-to-talk key inside the CLI
  max_recording_seconds: 120    # Hard stop for long recordings
  auto_tts: false               # Enable spoken replies automatically when /voice on
  beep_enabled: true            # Play record start/stop beeps in CLI voice mode
  silence_threshold: 200        # RMS threshold for speech detection
  silence_duration: 3.0         # Seconds of silence before auto-stop
```

STT provider behavior: `local` uses `faster-whisper` on your machine (install separately); `groq` uses Groq's Whisper-compatible endpoint (`GROQ_API_KEY`); `openai` uses the OpenAI speech API (`VOICE_TOOLS_OPENAI_KEY`). If the requested provider is unavailable, Hermes falls back automatically in order `local → groq → openai`. Groq/OpenAI model overrides are env-driven (`STT_GROQ_MODEL`, `STT_OPENAI_MODEL`, `GROQ_BASE_URL`, `STT_OPENAI_BASE_URL`).

Use `/voice on` in the CLI to enable microphone mode, `record_key` to start/stop recording, and `/voice tts` to toggle spoken replies. The feature-level voice walkthrough is owned by SP08 ([Voice Mode](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode)).

## Streaming

Stream tokens as they arrive rather than waiting for the full response. CLI streaming and gateway streaming are configured separately.

```yaml
# CLI streaming
display:
  streaming: true         # Stream tokens to terminal in real-time
  show_reasoning: true    # Also stream reasoning/thinking tokens (optional)

# Gateway streaming (Telegram, Discord, Slack)
streaming:
  enabled: true           # Enable progressive message editing
  transport: edit         # "edit" (progressive message editing) or "off"
  edit_interval: 0.3      # Seconds between message edits
  buffer_threshold: 40    # Characters before forcing an edit flush
  cursor: " ▉"            # Cursor shown during streaming
  fresh_final_after_seconds: 0    # Opt in to fresh final (Telegram) when preview is this old
```

When CLI streaming is on, responses appear token-by-token inside a streaming box; tool calls are still captured silently, and providers without streaming fall back automatically. For gateway streaming, the bot sends a message on the first token then progressively edits it; platforms that cannot edit messages (Signal, Email, Home Assistant) are auto-detected and gracefully disabled for that session. Overflow past the platform's ~4096-char limit finalizes the current message and starts a new one.

The master `streaming.enabled` switch is `false` by default. Once enabled, streaming is decided **per platform**: Telegram ships with `display.platforms.telegram.streaming: true` and Discord with `display.platforms.discord.streaming: false`. For natural mid-turn assistant updates without progressive token editing, set `display.interim_assistant_messages: true` (gateway-only, independent of `tool_progress`).

## Group Chat Session Isolation

Two related knobs cap and shape gateway sessions. Top-level `max_concurrent_sessions: null` (canonical; `gateway.max_concurrent_sessions` is a fallback) caps active sessions across CLI, TUI/dashboard, and gateway — `null`/`0` = unlimited, a positive integer sets the cap. The cap is enforced with a local runtime lease file and is **best-effort**: Hermes fails open if the registry cannot be read or locked, so users are not stranded; it is intended for a single host/profile runtime, not a shared `$HERMES_HOME` across machines.

`group_sessions_per_user: true` (default, recommended) gives each sender their own session in Discord channels, Telegram groups, Slack channels, etc. when the platform provides a user ID. `false` reverts to shared-room behavior (users share context, token costs, and interrupt state). DMs are unaffected (keyed by chat/DM ID); threads stay isolated from their parent channel either way.

## Unauthorized DM Behavior

Top-level `unauthorized_dm_behavior` controls what Hermes does when an unknown user sends a direct message; platform sections (e.g. `whatsapp.unauthorized_dm_behavior: ignore`) override the global default. `pair` (default) denies access but replies with a one-time pairing code in DMs; `ignore` silently drops unauthorized DMs.

## Quick Commands

Under `quick_commands`, define custom commands that either run shell commands without invoking the LLM (`type: exec`, a `command` string) or alias one slash command to another (`type: alias`, a `target` slash command) — for example `status: {type: exec, command: systemctl status hermes-agent}` or `restart: {type: alias, target: /gateway restart}`. Exec quick commands are zero-token and useful from messaging platforms for quick server checks. Type `/status`, `/restart`, etc. in the CLI or any messaging platform; `exec` commands run locally on the host and return output directly — no LLM call, no tokens. Notes: **30-second timeout** (long-running commands are killed); **priority** — quick commands are checked before skill commands, so they can override skill names; quick commands are resolved at dispatch time and are **not** shown in slash-command autocomplete; only `exec` and `alias` types are supported; works everywhere (CLI, Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant). String-only prompt shortcuts are not valid quick commands.

## Human Delay

The `human_delay` block simulates human-like response pacing in messaging platforms: `mode: "off"` (default; also `natural` | `custom`), with `min_ms: 800` and `max_ms: 2500` bounding the delay in `custom` mode.

## Web Search Backends

The `web_search` and `web_extract` tools support five backend providers, configured in `config.yaml` or via `hermes tools`. Per-capability keys (`search_backend`/`extract_backend`) let you mix providers.

```yaml
web:
  backend: firecrawl    # firecrawl | searxng | parallel | tavily | exa
  search_backend: "searxng"
  extract_backend: "firecrawl"
```

The backend table: **Firecrawl** (default, `FIRECRAWL_API_KEY`, search+extract), **SearXNG** (`SEARXNG_URL`, search-only), **Parallel** (`PARALLEL_API_KEY`), **Tavily** (`TAVILY_API_KEY`), **Exa** (`EXA_API_KEY`) — all but SearXNG do both search and extract. If `web.backend` is unset, the backend is auto-detected from available API keys (single-key shortcuts: SearXNG/Exa/Tavily/Parallel; otherwise Firecrawl). SearXNG is a free self-hosted metasearch engine (no API key, search-only — set `web.extract_backend` for extraction). Self-hosted Firecrawl uses `FIRECRAWL_API_URL`. Parallel modes via `PARALLEL_SEARCH_MODE` (`fast`/`one-shot`/`agentic`, default agentic). Exa supports `category` and domain/date filters. The feature-level web-search and browser setup is owned by SP08.

## Browser

Configure browser automation behavior. The browser toolset supports multiple providers (Browserbase, Browser Use, local Chromium-family CDP) documented on the SP08 browser feature page.

```yaml
browser:
  inactivity_timeout: 120        # Seconds before auto-closing idle sessions
  command_timeout: 30            # Timeout in seconds for browser commands
  record_sessions: false         # Auto-record browser sessions as WebM videos
  cdp_url: ""                    # Optional CDP override — attach to your own Chromium-family browser
  dialog_policy: must_respond    # must_respond | auto_dismiss | auto_accept
  dialog_timeout_s: 300          # Safety auto-dismiss under must_respond (seconds)
  camofox:
    managed_persistence: false   # Camofox sessions persist cookies/logins across restarts
    adopt_existing_tab: false    # Reuse an existing tab for this identity before creating one
```

**Dialog policies** (for native JS `alert`/`confirm`/`prompt` dialogs when a CDP backend is attached): `must_respond` (default — capture, surface in `browser_snapshot.pending_dialogs`, wait for `browser_dialog(action=...)`, then auto-dismiss after `dialog_timeout_s`), `auto_dismiss` (capture + dismiss immediately), `auto_accept` (capture + accept immediately, useful for aggressive `beforeunload` prompts). Dialog policy is ignored on Camofox and default local agent-browser mode.

## Timezone

Top-level `timezone: "America/New_York"` overrides the server-local timezone with an IANA timezone string, affecting timestamps in logs, cron scheduling, and system-prompt time injection. Supported values: any IANA identifier (`America/New_York`, `Europe/London`, `Asia/Kolkata`, `UTC`). Leave empty (the `""` default) or omit for server-local time.

## Discord

The `discord` block configures Discord-specific gateway behavior. `require_mention: true` (default): the bot responds in server channels only when mentioned with `@BotName` (DMs always work). `free_response_channels: ""`: a comma-separated list of channel IDs where the bot responds to every message without a mention. `auto_thread: true` (default): mentions in channels auto-create a thread, keeping channels clean. The full Discord setup is owned by SP11.

## Privacy (link-out)

The `privacy.redact_pii` PII-redaction block (deterministic hashing of phone/user/chat IDs before the LLM, WhatsApp/Signal/Telegram only) sits beside these gateway display settings but is owned by [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — configure it there.

**Source**: `inbox/hermes_agent_docs/user-guide/configuration.md`
**Last Updated**: 2026-06-19
**Status**: Active
