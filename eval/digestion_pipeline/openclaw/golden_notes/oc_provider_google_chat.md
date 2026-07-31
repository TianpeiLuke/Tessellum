---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - google_gemini
keywords:
  - openclaw google gemini provider
  - gemini api key auth
  - gemini cli oauth pkce
  - GEMINI_API_KEY GOOGLE_API_KEY
  - google-gemini-cli runtime
  - gemini grounding web search
  - thinkinglevel thinkingbudget mapping
  - direct gemini cache reuse cachedContent
topics:
  - OpenClaw
  - Google Gemini Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/google
access_control_group: ["general"]
---

# OpenClaw — Configuring the Google Gemini Chat Provider

## Overview

This note is the procedure for configuring the OpenClaw **Google (Gemini) chat provider**: choosing an auth method (API key via Google AI Studio, or PKCE OAuth that reuses an existing Gemini CLI login), setting a default `google/*` model, enabling Gemini Grounding web search, controlling reasoning via the `thinkingLevel`/`thinkingBudget` mapping, and applying the advanced cache/daemon options. It mirrors the chat/auth/search half of the `providers/google` source page — the front matter, **Getting started** (both tabs), **Capabilities**, **Web search**, and **Advanced configuration** sections. The bundled Google media + voice providers (image, video, music generation, batch TTS, and realtime Live-API voice) are documented separately in **[oc_provider_google_media_voice](oc_provider_google_media_voice.md)**.

The Google plugin provides access to Gemini models through Google AI Studio, plus image generation, media understanding (image/audio/video), text-to-speech, and web search via Gemini Grounding. The provider summary fields are:

- Provider: `google`
- Auth: `GEMINI_API_KEY` or `GOOGLE_API_KEY`
- API: Google Gemini API
- Runtime option: provider/model `agentRuntime.id: "google-gemini-cli"` reuses Gemini CLI OAuth while keeping model refs canonical as `google/*`.

## Getting started — API key

Best for: standard Gemini API access through Google AI Studio. Run onboarding interactively, or pass the key directly in non-interactive mode:

```bash
openclaw onboard --auth-choice gemini-api-key

# or pass the key directly:
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY"
```

Then set a default model under `agents.defaults.model.primary` (for example `google/gemini-3.1-pro-preview`) and verify it is available with `openclaw models list --provider google`:

```json5
{
  agents: {
    defaults: {
      model: { primary: "google/gemini-3.1-pro-preview" },
    },
  },
}
```

The environment variables `GEMINI_API_KEY` and `GOOGLE_API_KEY` are both accepted — use whichever you already have configured.

## Getting started — Gemini CLI (OAuth)

Best for: reusing an existing Gemini CLI login via PKCE OAuth instead of a separate API key. The doc carries a Warning: the `google-gemini-cli` provider is an unofficial integration, some users report account restrictions when using OAuth this way, so use at your own risk.

The local `gemini` command must be available on `PATH`. OpenClaw supports both Homebrew installs and global npm installs, including common Windows/npm layouts:

```bash
# Homebrew
brew install gemini-cli

# or npm
npm install -g @google/gemini-cli
```

Log in via OAuth, then verify the model is available:

```bash
openclaw models auth login --provider google-gemini-cli --set-default
openclaw models list --provider google
```

This path resolves to: Default model `google/gemini-3.1-pro-preview`; Runtime `google-gemini-cli`; Alias `gemini-cli`. Gemini 3.1 Pro's Gemini API model id is `gemini-3.1-pro-preview`; OpenClaw accepts the shorter `google/gemini-3.1-pro` as a convenience alias and normalizes it before provider calls.

The OAuth flow reads these environment variables (or the `GEMINI_CLI_*` variants): `OPENCLAW_GEMINI_OAUTH_CLIENT_ID` and `OPENCLAW_GEMINI_OAUTH_CLIENT_SECRET`. Two failure-mode notes from the source: if Gemini CLI OAuth requests fail after login, set `GOOGLE_CLOUD_PROJECT` or `GOOGLE_CLOUD_PROJECT_ID` on the gateway host and retry; if login fails before the browser flow starts, make sure the local `gemini` command is installed and on `PATH`. Finally, `google-gemini-cli/*` model refs are legacy compatibility aliases — new configs should use `google/*` model refs plus the `google-gemini-cli` runtime when they want local Gemini CLI execution.

## Capabilities

The Capabilities matrix below is the provider overview anchor; the media/voice rows (image generation, music generation, text-to-speech, realtime voice, image/audio/video understanding) are configured in **[oc_provider_google_media_voice](oc_provider_google_media_voice.md)**, while chat completions, web search, and thinking/reasoning are configured in this note.

| Capability             | Supported                     |
| ---------------------- | ----------------------------- |
| Chat completions       | Yes                           |
| Image generation       | Yes                           |
| Music generation       | Yes                           |
| Text-to-speech         | Yes                           |
| Realtime voice         | Yes (Google Live API)         |
| Image understanding    | Yes                           |
| Audio transcription    | Yes                           |
| Video understanding    | Yes                           |
| Web search (Grounding) | Yes                           |
| Thinking/reasoning     | Yes (Gemini 2.5+ / Gemini 3+) |
| Gemma 4 models         | Yes                           |

## Web search (Gemini Grounding)

The bundled `gemini` web-search provider uses Gemini Google Search grounding. Configure a dedicated search key under `plugins.entries.google.config.webSearch`, or let it reuse `models.providers.google.apiKey` after `GEMINI_API_KEY`:

```json5
{
  plugins: {
    entries: {
      google: {
        config: {
          webSearch: {
            apiKey: "AIza...", // optional if GEMINI_API_KEY or models.providers.google.apiKey is set
            baseUrl: "https://generativelanguage.googleapis.com/v1beta", // falls back to models.providers.google.baseUrl
            model: "gemini-2.5-flash",
          },
        },
      },
    },
  },
}
```

Credential precedence is dedicated `webSearch.apiKey`, then `GEMINI_API_KEY`, then `models.providers.google.apiKey`. `webSearch.baseUrl` is optional and exists for operator proxies or compatible Gemini API endpoints; when omitted, Gemini web search reuses `models.providers.google.baseUrl`. The provider-specific tool behavior is documented at the shared Gemini search tool page (link-out, owned by the Tools sub-plan — see **[oc_tools_gemini_search](oc_tools_gemini_search.md)**).

### Thinking-level mapping (reasoning controls)

Gemini 3 models use `thinkingLevel` rather than `thinkingBudget`. OpenClaw maps Gemini 3, Gemini 3.1, and `gemini-*-latest` alias reasoning controls to `thinkingLevel` so default/low-latency runs do not send disabled `thinkingBudget` values. `/think adaptive` keeps Google's dynamic thinking semantics instead of choosing a fixed OpenClaw level: Gemini 3 and Gemini 3.1 omit a fixed `thinkingLevel` so Google can choose the level, while Gemini 2.5 sends Google's dynamic sentinel `thinkingBudget: -1`. Gemma 4 models (for example `gemma-4-26b-a4b-it`) support thinking mode — OpenClaw rewrites `thinkingBudget` to a supported Google `thinkingLevel` for Gemma 4, and setting thinking to `off` preserves thinking disabled instead of mapping to `MINIMAL`.

## Advanced configuration

### Direct Gemini cache reuse

For direct Gemini API runs (`api: "google-generative-ai"`), OpenClaw passes a configured `cachedContent` handle through to Gemini requests. Configure per-model or global params with either `cachedContent` or legacy `cached_content`; if both are present, `cachedContent` wins. An example value is `cachedContents/prebuilt-context`. Gemini cache-hit usage is normalized into OpenClaw `cacheRead` from upstream `cachedContentTokenCount`.

```json5
{
  agents: {
    defaults: {
      models: {
        "google/gemini-2.5-pro": {
          params: {
            cachedContent: "cachedContents/prebuilt-context",
          },
        },
      },
    },
  },
}
```

### Gemini CLI usage notes

When using the `google-gemini-cli` OAuth provider, OpenClaw uses Gemini CLI `stream-json` output by default and normalizes usage from the final `stats` payload; legacy `--output-format json` overrides still use the JSON parser. Specifics from the source: streamed reply text comes from assistant `message` events; for legacy JSON output, reply text comes from the CLI JSON `response` field; usage falls back to `stats` when the CLI leaves `usage` empty; `stats.cached` is normalized into OpenClaw `cacheRead`; and if `stats.input` is missing, OpenClaw derives input tokens from `stats.input_tokens - stats.cached`.

### Environment and daemon setup

If the Gateway runs as a daemon (launchd/systemd), make sure `GEMINI_API_KEY` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`).

**Source**: OpenClaw documentation — `providers/google` (mirror `inbox/openclaw_docs/providers/google.md`), chat/auth/search half
**Last Updated**: 2026-06-22
**Status**: Active
