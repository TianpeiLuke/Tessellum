---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - config_agents
keywords:
  - openclaw agents.defaults.model
  - model primary fallbacks
  - imageMaxDimensionPx imageQuality
  - usertimezone timeformat
  - agentRuntime runtime policy
  - openclaw model aliases
  - provider model routing
  - codex claude-cli runtime
topics:
  - OpenClaw
  - Agent Defaults Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-agents
access_control_group: ["general"]
---

# OpenClaw — Agent Defaults: Model, Media, and Time Config

## Overview

This note is the procedural reference for the model-selection, media, and time keys under `agents.defaults` in OpenClaw's gateway agent configuration, plus the **Runtime policy** section that pins which execution harness (OpenClaw embedded, Codex, or a CLI backend) runs an agent turn. It mirrors the `agents.defaults.imageMaxDimensionPx`, `agents.defaults.imageQuality`, `agents.defaults.userTimezone`, `agents.defaults.timeFormat`, `agents.defaults.model`, and `### Runtime policy` sections of the `gateway/config-agents` source page. All defaults, key names, and config blocks are copied verbatim from the mirror; companion agent-defaults clusters (bootstrap/context, backends/overlays, runtime-resilience, routing, session/messages/talk) live in the sibling `oc_gateway_config_agents_*` notes.

## Image media — `imageMaxDimensionPx` and `imageQuality`

`agents.defaults.imageMaxDimensionPx` sets the max pixel size for the longest image side in transcript/tool image blocks before provider calls. Default: `1200`. Lower values usually reduce vision-token usage and request payload size for screenshot-heavy runs; higher values preserve more visual detail.

`agents.defaults.imageQuality` is the image-tool compression/detail preference for images loaded from file paths, URLs, and media references. Default: `auto`. OpenClaw adapts the resize ladder to the selected image model — for example, Claude Opus 4.8, OpenAI GPT-5.5, Qwen VL, and hosted Llama 4 vision models can use larger images than older/default high-detail vision paths, while multi-image turns are compressed more aggressively in `auto` mode to control token and latency cost. Values: `auto` (adapt to model limits and image count), `efficient` (prefer smaller images for lower token and byte usage), `balanced` (standard middle-ground ladder), `high` (preserve more detail for screenshots, diagrams, and document images).

```json5
{
  agents: {
    defaults: {
      imageMaxDimensionPx: 1200,
      imageQuality: "auto", // auto | efficient | balanced | high
    },
  },
}
```

## Time context — `userTimezone` and `timeFormat`

`agents.defaults.userTimezone` is the timezone for system prompt context (not message timestamps); it falls back to the host timezone when unset. `agents.defaults.timeFormat` is the time format in the system prompt, with default `auto` (OS preference) and accepted values `auto`, `12`, or `24`.

```json5
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

## The `model` block — `agents.defaults.model`

The `agents.defaults.model` surface configures the text model plus the media/PDF model families and the global run params. The full source example:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.7": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.7"],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      imageGenerationModel: {
        primary: "openai/gpt-image-2",
        fallbacks: ["google/gemini-3.1-flash-image-preview"],
      },
      videoGenerationModel: {
        primary: "qwen/wan2.6-t2v",
        fallbacks: ["qwen/wan2.6-i2v"],
      },
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4-mini"],
      },
      params: { cacheRetention: "long" }, // global default provider params
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
      thinkingDefault: "low",
      verboseDefault: "off",
      toolProgressDetail: "explain",
      reasoningDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      contextTokens: 200000,
      maxConcurrent: 3,
    },
  },
}
```

### Model and media-model family keys

- `model`: accepts either a string (`"provider/model"`) or an object (`{ primary, fallbacks }`). String form sets only the primary model; object form sets primary plus ordered failover models.
- `model.primary`: format `provider/model` (e.g. `openai/gpt-5.5` for OpenAI API-key or Codex OAuth access). If you omit the provider, OpenClaw tries an alias first, then a unique configured-provider match for that exact model id, and only then falls back to the configured default provider (deprecated compatibility behavior, so prefer explicit `provider/model`). If that provider no longer exposes the configured default model, OpenClaw falls back to the first configured provider/model instead of surfacing a stale removed-provider default.
- `imageModel`: string or `{ primary, fallbacks }`. Used by the `image` tool path as its vision-model config, and as fallback routing when the selected/default model cannot accept image input. Prefer explicit `provider/model` refs; bare IDs are accepted for compatibility and qualified to a provider when they uniquely match a configured image-capable entry in `models.providers.*.models`, but ambiguous matches require an explicit provider prefix.
- `imageGenerationModel`: string or `{ primary, fallbacks }`. Used by the shared image-generation capability and any future tool/plugin surface that generates images; typical values include `google/gemini-3.1-flash-image-preview`, `fal/fal-ai/flux/dev`, `openai/gpt-image-2`, or `openai/gpt-image-1.5` (transparent-background PNG/WebP). Configure matching provider auth (e.g. `GEMINI_API_KEY`/`GOOGLE_API_KEY` for `google/*`, `OPENAI_API_KEY` or OpenAI Codex OAuth for `openai/gpt-image-*`, `FAL_KEY` for `fal/*`). If omitted, `image_generate` infers an auth-backed default — current default provider first, then remaining registered providers in provider-id order.
- `musicGenerationModel`: string or `{ primary, fallbacks }`. Used by the shared music-generation capability and the built-in `music_generate` tool; typical values `google/lyria-3-clip-preview`, `google/lyria-3-pro-preview`, `minimax/music-2.6`. Same auth-backed inference and provider-auth requirement as image generation.
- `videoGenerationModel`: string or `{ primary, fallbacks }`. Used by the shared video-generation capability and the built-in `video_generate` tool; typical values `qwen/wan2.6-t2v`, `qwen/wan2.6-i2v`, `qwen/wan2.6-r2v`, `qwen/wan2.6-r2v-flash`, `qwen/wan2.7-r2v`. The official Qwen plugin supports up to 1 output video, 1 input image, 4 input videos, 10 seconds duration, and provider-level `size`, `aspectRatio`, `resolution`, `audio`, and `watermark` options.
- `pdfModel`: string or `{ primary, fallbacks }`, used by the `pdf` tool for model routing. If omitted, the PDF tool falls back to `imageModel`, then to the resolved session/default model. `pdfMaxBytesMb` is the default PDF size limit when `maxBytesMb` is not passed at call time; `pdfMaxPages` is the default maximum pages considered by extraction fallback mode.

### Defaults, params, and the model catalog

- `verboseDefault`: default verbose level (`"off"`, `"on"`, `"full"`; default `"off"`). `toolProgressDetail`: detail mode for `/verbose` tool summaries and progress-draft tool lines (`"explain"` default = compact human labels, or `"raw"` = append raw command/detail); per-agent `agents.list[].toolProgressDetail` overrides. `reasoningDefault`: default reasoning visibility (`"off"`, `"on"`, `"stream"`), only applied for owners, authorized senders, or operator-admin gateway contexts when no per-message/session override is set. `elevatedDefault`: default elevated-output level (`"off"`, `"on"`, `"ask"`, `"full"`; default `"on"`). `maxConcurrent`: max parallel agent runs across sessions (each session still serialized); default `4`.
- `models`: the configured model catalog and allowlist for `/model`. Each entry can include `alias` (shortcut) and `params` (provider-specific, e.g. `temperature`, `maxTokens`, `cacheRetention`, `context1m`, `responsesServerCompaction`, `responsesCompactThreshold`, OpenRouter `provider` routing, `chat_template_kwargs`, `extra_body`/`extraBody`). Use `provider/*` entries such as `"openai/*": {}` or `"vllm/*": {}` to show all discovered models for selected providers; add `agentRuntime` to a `provider/*` entry to set a runtime for every dynamically discovered model (exact `provider/model` policy still wins). Safe edits use `openclaw config set agents.defaults.models '<json>' --strict-json --merge`; `config set` refuses replacements that would remove existing allowlist entries unless you pass `--replace`. For direct OpenAI Responses models server-side compaction is enabled automatically — use `params.responsesServerCompaction: false` to stop injecting `context_management`, or `params.responsesCompactThreshold` to override the threshold.
- `params`: global default provider parameters applied to all models, set at `agents.defaults.params` (e.g. `{ cacheRetention: "long" }`). Merge precedence: `agents.defaults.params` (global base) < `agents.defaults.models["provider/model"].params` (per-model) < `agents.list[].params` (matching agent id), overriding by key. `params.extra_body`/`params.extraBody` is advanced pass-through JSON merged into `api: "openai-completions"` request bodies (extra body wins on collision; non-native routes still strip OpenAI-only `store`). `params.chat_template_kwargs` are vLLM/OpenAI-compatible chat-template args; `params.preserveThinking` is a Z.AI-only opt-in. `compat.thinkingFormat` (`"together"`/`"qwen"`/`"qwen-chat-template"`) and `compat.supportedReasoningEfforts` (include `"xhigh"` for endpoints that accept it) tune OpenAI-compatible reasoning payloads.
- `localService`: optional provider-level process manager for local/self-hosted model servers. When the selected model belongs to that provider, OpenClaw probes `healthUrl` (or `baseUrl + "/models"`), starts `command` with `args` if the endpoint is down, waits up to `readyTimeoutMs`, then sends the request. `command` must be an absolute path; `idleStopMs: 0` keeps the process alive until OpenClaw exits, a positive value stops the OpenClaw-spawned process after that many idle milliseconds.

> **Note:** Runtime policy belongs on providers or models, not on `agents.defaults` — see the next section. Config writers that mutate these fields (e.g. `/models set`, `/models set-image`, fallback add/remove) save canonical object form and preserve existing fallback lists when possible.

## Runtime policy

Runtime policy controls which execution harness runs a text agent turn. It belongs on providers or models, not on `agents.defaults`: use `models.providers.<provider>.agentRuntime` for provider-wide rules, or `agents.defaults.models["provider/model"].agentRuntime` / `agents.list[].models["provider/model"].agentRuntime` for model-specific rules.

```json5
{
  models: {
    providers: {
      openai: {
        agentRuntime: { id: "codex" },
      },
    },
  },
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
      models: {
        "anthropic/claude-opus-4-8": {
          agentRuntime: { id: "claude-cli" },
        },
        "vllm/*": {
          agentRuntime: { id: "openclaw" },
        },
      },
    },
  },
}
```

- `id`: `"auto"`, `"openclaw"`, a registered plugin harness id, or a supported CLI backend alias. The bundled Codex plugin registers `codex`; the bundled Anthropic plugin provides the `claude-cli` CLI backend.
- `id: "auto"` lets registered plugin harnesses claim supported turns and uses OpenClaw when no harness matches. An explicit plugin runtime such as `id: "codex"` requires that harness and fails closed if it is unavailable or fails.
- `id: "pi"` is accepted only as a deprecated alias for `openclaw` to preserve shipped configs from v2026.5.22 and earlier; new config should use `openclaw`.
- Runtime precedence is exact model policy first (`agents.list[].models["provider/model"]`, `agents.defaults.models["provider/model"]`, or `models.providers.<provider>.models[]`), then `agents.list[]` / `agents.defaults.models["provider/*"]`, then provider-wide policy at `models.providers.<provider>.agentRuntime`.
- Whole-agent runtime keys are legacy: `agents.defaults.agentRuntime`, `agents.list[].agentRuntime`, session runtime pins, and `OPENCLAW_AGENT_RUNTIME` are ignored by runtime selection. Run `openclaw doctor --fix` to remove stale values.
- OpenAI agent models use the Codex harness by default; provider/model `agentRuntime.id: "codex"` remains valid to make that explicit. For Claude CLI deployments, prefer `model: "anthropic/claude-opus-4-8"` plus model-scoped `agentRuntime.id: "claude-cli"`; legacy `claude-cli/claude-opus-4-7` model refs still work for compatibility, but new config should keep provider/model selection canonical and put the execution backend in provider/model runtime policy.
- Runtime policy only controls text agent-turn execution. Media generation, vision, PDF, music, video, and TTS still use their provider/model settings.

### Built-in alias shorthands

Aliases only apply when the model is present in `agents.defaults.models`; configured aliases always win over defaults.

| Alias               | Model                           |
| ------------------- | ------------------------------- |
| `opus`              | `anthropic/claude-opus-4-6`     |
| `sonnet`            | `anthropic/claude-sonnet-4-6`   |
| `gpt`               | `openai/gpt-5.5`                |
| `gpt-mini`          | `openai/gpt-5.4-mini`           |
| `gpt-nano`          | `openai/gpt-5.4-nano`           |
| `gemini`            | `google/gemini-3.1-pro-preview` |
| `gemini-flash`      | `google/gemini-3-flash-preview` |
| `gemini-flash-lite` | `google/gemini-3.1-flash-lite`  |

Z.AI GLM-4.x models automatically enable thinking mode unless you set `--thinking off` or define `agents.defaults.models["zai/<model>"].params.thinking` yourself; Z.AI models enable `tool_stream` by default (set `params.tool_stream` to `false` to disable). Anthropic Claude Opus 4.8 keeps thinking off by default in OpenClaw — when adaptive thinking is explicitly enabled, Anthropic's provider-owned effort default is `high`; Claude 4.6 models default to `adaptive` when no explicit thinking level is set.

**Source**: OpenClaw documentation — `gateway/config-agents` (mirror `inbox/openclaw_docs/gateway/config-agents.md`), sections imageMaxDimensionPx / imageQuality / userTimezone / timeFormat / model / Runtime policy
**Last Updated**: 2026-06-22
**Status**: Active
