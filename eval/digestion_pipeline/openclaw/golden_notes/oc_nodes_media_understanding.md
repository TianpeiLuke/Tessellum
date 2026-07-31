---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - media_understanding
keywords:
  - openclaw media understanding
  - tools.media config
  - inbound media pre-digest
  - provider cli fallback order
  - auto-detect media understanding
  - media maxbytes maxchars
  - provider support matrix
  - attachment policy untrusted content
topics:
  - OpenClaw
  - Media Understanding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes/media-understanding
access_control_group: ["general"]
---

# OpenClaw — Configuring Inbound Media Understanding

## Overview

This note is the procedure for configuring OpenClaw **media understanding**: the optional step that summarizes inbound image/audio/video into short text before the reply pipeline runs, so routing and command parsing improve while the original files/URLs are still always delivered to the model. It mirrors the `nodes/media-understanding` source page — the `tools.media` config, provider-vs-CLI model entries with ordered fallback, auto-detect order, defaults/limits, proxy-env support, the provider support matrix, attachment policy, and config examples. Vendor-specific media behavior is registered by vendor plugins; OpenClaw core owns the shared `tools.media` config, fallback order, and reply-pipeline integration.

## Goals

Media understanding is **optional** and exists to: pre-digest inbound media into short text for faster routing plus better command parsing; always preserve original media delivery to the model; support both **provider APIs** and **CLI fallbacks**; and allow multiple models with ordered fallback on error/size/timeout. When off, models still receive the originals.

## High-level behavior

The pipeline runs five ordered steps per inbound message: (1) **Collect attachments** — gather inbound `MediaPaths`, `MediaUrls`, `MediaTypes`; (2) **Select per-capability** — for each enabled capability (image/audio/video), select attachments per policy (default **first**); (3) **Choose model** — the first eligible model entry by size + capability + auth; (4) **Fallback on failure** — if a model fails or media is too large, fall back to the next entry; (5) **Apply success block** — `Body` becomes an `[Image]`, `[Audio]`, or `[Video]` block, audio also sets `{{Transcript}}` (command parsing uses caption text if present, else the transcript), and captions are preserved as `User text:` inside the block. If understanding fails or is disabled, the reply flow continues with the original body plus attachments.

## Config overview

`tools.media` supports **shared models** plus per-capability overrides. Top-level keys: `tools.media.models` (shared model list, gate per-entry with `capabilities`); `tools.media.image` / `tools.media.audio` / `tools.media.video`, each holding defaults (`prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`), provider overrides (`baseUrl`, `headers`, `providerOptions`), Deepgram audio options via `tools.media.audio.providerOptions.deepgram`, audio transcript echo controls (`echoTranscript`, default `false`; `echoFormat`), an optional per-capability `models` list (preferred before shared models), an `attachments` policy (`mode`, `maxAttachments`, `prefer`), and an optional `scope` (gate by channel/chatType/session key); and `tools.media.concurrency` — max concurrent capability runs (default **2**).

### Model entries (provider / CLI)

Each `models[]` entry is either a **provider** entry (`type: "provider"`, default if omitted) or a **CLI** entry (`type: "cli"`). The provider shape:

```json5
{
  type: "provider", // default if omitted
  provider: "openai",
  model: "gpt-5.5",
  prompt: "Describe the image in <= 500 chars.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // optional, used for multi-modal entries
  profile: "vision-profile",
  preferredProfile: "vision-fallback",
}
```

A **CLI** entry instead names `command` + `args` (with the same `maxChars` / `maxBytes` / `timeoutSeconds` limits, e.g. `command: "gemini"`, `maxBytes: 52428800`, `timeoutSeconds: 120`) and **should set `capabilities` explicitly** to avoid surprising matches. CLI `args` templates can substitute `{{MediaPath}}`, `{{MaxChars}}`, `{{MediaDir}}` (media file's directory), `{{OutputDir}}` (scratch dir for this run), and `{{OutputBase}}` (scratch file base path, no extension); a full CLI entry appears in the shared-models config example below.

### Provider credentials (`apiKey`)

Provider media understanding uses the **same provider auth resolution as normal model calls**: auth profiles, then environment variables, then `models.providers.<providerId>.apiKey`. The `tools.media.*.models[]` entries do **not** accept an inline `apiKey` field — the `provider` value (such as `openai` or `moonshot`) must have credentials via one of those standard sources. A minimal credential block sets `models.providers.openai.apiKey` and `models.providers.moonshot.apiKey`. For the full provider auth reference (profiles, environment variables, custom base URLs), see Tools and custom providers in the OpenClaw docs.

## Defaults and limits

Recommended defaults: `maxChars` is **500** for image/video and **unset** for audio (full transcript unless limited); `maxBytes` defaults are **10MB** image, **20MB** audio, **50MB** video. Rules: media exceeding `maxBytes` skips that model and tries the **next**; audio under **1024 bytes** is treated as empty/corrupt and skipped before transcription (the reply context gets a deterministic placeholder transcript); output over `maxChars` is trimmed; `prompt` defaults to "Describe the {media}." plus the `maxChars` guidance (image/video only); if the active primary image model supports vision natively, OpenClaw skips the `[Image]` block and passes the original image to the model; if a Gateway/WebChat primary model is text-only, image attachments are preserved as offloaded `media://inbound/*` refs so image/PDF tools or a configured image model can still inspect them; explicit `openclaw infer image describe --model <provider/model>` runs that provider/model directly (including Ollama refs like `ollama/qwen2.5vl:7b`); and if `<capability>.enabled: true` but no models are configured, OpenClaw uses the **active reply model** when its provider supports the capability.

### Auto-detect media understanding (default)

If `tools.media.<capability>.enabled` is **not** `false` and you haven't configured models, OpenClaw auto-detects in this order and **stops at the first working option**: (1) the **active reply model** when its provider supports the capability; (2) `agents.defaults.imageModel` primary/fallback refs (image only — prefer `provider/model` refs; bare refs qualify from configured image-capable provider entries only when the match is unique); (3) **local CLIs** for audio only, if installed — `sherpa-onnx-offline` (requires `SHERPA_ONNX_MODEL_DIR` with encoder/decoder/joiner/tokens), `whisper-cli` (`whisper-cpp`; uses `WHISPER_CPP_MODEL` or the bundled tiny model), `whisper` (Python CLI; auto-downloads models); (4) the **`gemini` CLI** using `read_many_files`; (5) **provider auth** — configured `models.providers.*` entries supporting the capability are tried before the bundled order, image-only config providers with an image-capable model auto-register even when not a bundled vendor plugin, and Ollama image understanding is available when selected explicitly. The bundled fallback order: **Audio** — OpenAI → Groq → xAI → Deepgram → OpenRouter → Google → SenseAudio → ElevenLabs → Mistral; **Image** — OpenAI → Anthropic → Google → MiniMax → MiniMax Portal → Z.AI; **Video** — Google → Qwen → Moonshot. To disable auto-detection, set the capability `enabled: false`:

```json5
{
  tools: { media: { audio: { enabled: false } } },
}
```

Binary detection is best-effort across macOS/Linux/Windows; ensure the CLI is on `PATH` (OpenClaw expands `~`), or set a CLI model with a full command path.

### Proxy environment support (provider models)

When provider-based **audio** and **video** media understanding is enabled, OpenClaw honors standard outbound proxy environment variables for provider HTTP calls: `HTTPS_PROXY`, `HTTP_PROXY`, `ALL_PROXY`, `https_proxy`, `http_proxy`, `all_proxy`. With no proxy env vars set, media understanding uses direct egress; a malformed proxy value logs a warning and falls back to direct fetch.

## Capabilities (optional)

If you set `capabilities`, the entry only runs for those media types. For shared lists, OpenClaw infers defaults per provider: `openai`, `anthropic`, `minimax`, `minimax-portal`, `zai` → **image**; `moonshot`, `qwen` → **image + video**; `openrouter` → **image + audio**; `google` (Gemini API) → **image + audio + video**; `mistral`, `groq`, `xai`, `deepgram` → **audio**; and any `models.providers.<id>.models[]` catalog with an image-capable model → **image**. For CLI entries, **set `capabilities` explicitly**; if omitted, the entry is eligible for the list it appears in.

## Provider support matrix (OpenClaw integrations)

| Capability | Provider integration | Notes |
| ---------- | -------------------- | ----- |
| Image | OpenAI, OpenAI Codex OAuth, Codex app-server, OpenRouter, Anthropic, Google, MiniMax, Moonshot, Qwen, Z.AI, config providers | Vendor plugins register image support; `openai/*` can use API-key or Codex OAuth routing; `codex/*` uses a bounded Codex app-server turn; MiniMax and MiniMax OAuth both use `MiniMax-VL-01`; image-capable config providers auto-register. |
| Audio | OpenAI, Groq, xAI, Deepgram, OpenRouter, Google, SenseAudio, ElevenLabs, Mistral | Provider transcription (Whisper/Groq/xAI/Deepgram/OpenRouter STT/Gemini/SenseAudio/Scribe/Voxtral). |
| Video | Google, Qwen, Moonshot | Provider video understanding via vendor plugins; Qwen video understanding uses the Standard DashScope endpoints. |

MiniMax note: `minimax`, `minimax-cn`, `minimax-portal`, and `minimax-portal-cn` image understanding comes from the plugin-owned `MiniMax-VL-01` media provider, and automatic image routing keeps using `MiniMax-VL-01` even if legacy MiniMax M2.x metadata claims image input.

## Model selection guidance

Prefer the strongest latest-generation model per capability when quality and safety matter; for tool-enabled agents handling untrusted inputs, avoid older/weaker media models; keep at least one fallback per capability (a quality model plus a faster/cheaper one); CLI fallbacks (`whisper-cli`, `whisper`, `gemini`) help when provider APIs are unavailable; and a `parakeet-mlx` note — with `--output-dir`, OpenClaw reads `<output-dir>/<media-basename>.txt` when output format is `txt` (or unspecified), while non-`txt` formats fall back to stdout.

## Attachment policy

Per-capability `attachments` controls which are processed: `mode` (`"first" | "all"`, default `first`) processes the first selected attachment or all; `maxAttachments` (number, default `1`) caps the count; and `prefer` (`"first" | "last" | "path" | "url"`) sets selection preference among candidates. When `mode: "all"`, outputs are labeled `[Image 1/2]`, `[Audio 2/2]`, etc. File-attachment extraction: extracted file text is wrapped as **untrusted external content** before being appended to the media prompt, using explicit boundary markers `<<<EXTERNAL_UNTRUSTED_CONTENT id="...">>>` / `<<<END_EXTERNAL_UNTRUSTED_CONTENT id="...">>>` plus a `Source: External` metadata line; this path intentionally omits the long `SECURITY NOTICE:` banner to avoid bloating the prompt (the markers and metadata remain); a file with no extractable text injects `[No extractable text]`; and a PDF that falls back to rendered page images keeps the placeholder `[PDF content rendered to images; images not forwarded to model]`, since this step forwards text blocks, not rendered PDF images.

## Config examples

The source documents four config tabs (shared models + overrides, audio + video only, image-only, multi-modal single entry). The **shared models + overrides** tab is reproduced below — a shared list mixing two provider entries and one CLI entry, with a per-capability audio attachments override and a video `maxChars`:

```json5
{
  tools: {
    media: {
      models: [
        { provider: "openai", model: "gpt-5.5", capabilities: ["image"] },
        { provider: "google", model: "gemini-3-flash-preview",
          capabilities: ["image", "audio", "video"] },
        { type: "cli", command: "gemini",
          args: ["-m", "gemini-3-flash", "--allowed-tools", "read_file",
            "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters."],
          capabilities: ["image", "video"] },
      ],
      audio: { attachments: { mode: "all", maxAttachments: 2 } },
      video: { maxChars: 500 },
    },
  },
}
```

The other three tabs follow the same shape: **image-only** sets `tools.media.image` (`enabled: true`, `maxBytes: 10485760`, `maxChars: 500`) with a `models` list of `openai/gpt-5.5`, an `anthropic/claude-opus-4-6` fallback, then a `gemini` CLI fallback; **audio + video only** sets per-capability `enabled: true` `models` lists (audio: `gpt-4o-mini-transcribe` + a `whisper --model base` CLI; video: a Gemini provider + `gemini` CLI); and **multi-modal single entry** references one shared Gemini entry with `capabilities: ["image", "video", "audio"]` from each capability.

## Status output

When media understanding runs, `/status` includes a short per-capability summary line showing outcomes and chosen provider/model:

```
📎 Media: image ok (openai/gpt-5.4) · audio skipped (maxBytes)
```

## Notes

Understanding is **best-effort** — errors do not block replies; attachments are still passed to models even when disabled; use `scope` to limit where it runs (e.g. DMs only).

**Source**: OpenClaw documentation — `nodes/media-understanding` (mirror `inbox/openclaw_docs/nodes/media-understanding.md`)
**Last Updated**: 2026-06-22
**Status**: Active
