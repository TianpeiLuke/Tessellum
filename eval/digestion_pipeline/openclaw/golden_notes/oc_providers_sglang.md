---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - sglang
keywords:
  - openclaw sglang provider
  - self-hosted openai-compatible server
  - sglang_api_key opt-in
  - auth-choice sglang onboarding
  - sglang model discovery /v1/models
  - models.providers.sglang explicit config
  - proxy-style openai-compatible backend
  - sglang/* dynamic discovery
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/sglang
access_control_group: ["general"]
---

# OpenClaw — Connecting to a Self-Hosted SGLang Server

## Overview

This note is the procedure for connecting OpenClaw to a self-hosted **SGLang** server, mirroring the `providers/sglang` source page. SGLang serves open-weight models over an OpenAI-compatible HTTP API, and OpenClaw connects to it through the `openai-completions` provider family with auto-discovery of available models. It covers the provider's property table (id, plugin, auth, API, base URL, model placeholder, streaming, pricing), the Getting-started onboarding path (`SGLANG_API_KEY` opt-in, `--auth-choice sglang`, `openclaw onboard` or a manual model), implicit-provider model discovery from `/v1/models`, explicit `models.providers.sglang` configuration for pinned context/host/auth, and the advanced proxy-style request-shaping behavior plus troubleshooting.

## Provider Properties

The `sglang` provider connects OpenClaw to an OpenAI-compatible SGLang HTTP server. The verbatim property table from the source page is:

| Property | Value |
| --- | --- |
| Provider id | `sglang` |
| Plugin | bundled, `enabledByDefault: true` |
| Auth env var | `SGLANG_API_KEY` (any non-empty value if server has no auth) |
| Onboarding flag | `--auth-choice sglang` |
| API | OpenAI-compatible (`openai-completions`) |
| Default base URL | `http://127.0.0.1:30000/v1` |
| Default model placeholder | `sglang/Qwen/Qwen3-8B` |
| Streaming usage | Yes (`supportsStreamingUsage: true`) |
| Pricing | Marked external-free (`modelPricing.external: false`) |

OpenClaw also **auto-discovers** available models from SGLang when you opt in with `SGLANG_API_KEY`. To keep discovery dynamic when you also configure a custom SGLang base URL, use `sglang/*` in `agents.defaults.models` (see Model Discovery below).

## Getting Started

Three steps connect OpenClaw to SGLang:

1. **Start SGLang.** Launch SGLang with an OpenAI-compatible server whose base URL exposes `/v1` endpoints (for example `/v1/models`, `/v1/chat/completions`). SGLang commonly runs on `http://127.0.0.1:30000/v1`.
2. **Set an API key.** Any value works if no auth is configured on your server. Exporting any non-empty value is what opts you in to model discovery.
3. **Run onboarding or set a model directly.** Run `openclaw onboard` (the matching onboarding flag is `--auth-choice sglang`), or configure the model manually in config.

Set the key (any non-empty value when the server has no auth):

```bash
export SGLANG_API_KEY="sglang-local"
```

Then either run onboarding, or pin the primary model manually:

```json5
{
  agents: {
    defaults: {
      model: { primary: "sglang/your-model-id" },
    },
  },
}
```

## Model Discovery (Implicit Provider)

When `SGLANG_API_KEY` is set (or an auth profile exists) and you **do not** define `models.providers.sglang`, OpenClaw acts as an implicit provider: it queries `GET http://127.0.0.1:30000/v1/models` and converts the returned IDs into model entries. This is the zero-config discovery path — no explicit provider block is required.

If you set `models.providers.sglang` explicitly, OpenClaw uses your declared models by default instead of discovering them. To force discovery against a configured provider's `/models` endpoint, add `"sglang/*": {}` to `agents.defaults.models`; OpenClaw will then query that provider's `/models` endpoint and include all advertised SGLang models. This `sglang/*` wildcard is also how you keep discovery dynamic when you configure a custom SGLang base URL.

## Explicit Configuration (Manual Models)

Use explicit config when SGLang runs on a different host/port, when you want to pin `contextWindow`/`maxTokens` values, or when your server requires a real API key (or you want to control headers). The explicit provider block declares the base URL, the `${SGLANG_API_KEY}` substitution, the `openai-completions` API, and a `models` array with per-model fields:

```json5
{
  models: {
    providers: {
      sglang: {
        baseUrl: "http://127.0.0.1:30000/v1",
        apiKey: "${SGLANG_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "your-model-id",
            name: "Local SGLang Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Advanced Configuration

**Proxy-style behavior.** SGLang is treated as a proxy-style OpenAI-compatible `/v1` backend, not a native OpenAI endpoint, so OpenClaw does not apply OpenAI-only request shaping to it. The source page enumerates exactly which native-OpenAI behaviors are suppressed:

| Behavior | SGLang |
| --- | --- |
| OpenAI-only request shaping | Not applied |
| `service_tier`, Responses `store`, prompt-cache hints | Not sent |
| Reasoning-compat payload shaping | Not applied |
| Hidden attribution headers (`originator`, `version`, `User-Agent`) | Not injected on custom SGLang base URLs |

**Troubleshooting.** If the *server is not reachable*, verify it is running and responding with `curl http://127.0.0.1:30000/v1/models`. For *auth errors*, set a real `SGLANG_API_KEY` that matches your server configuration, or configure the provider explicitly under `models.providers.sglang`. Note: if you run SGLang without authentication, any non-empty value for `SGLANG_API_KEY` is sufficient to opt in to model discovery.

**Source**: OpenClaw documentation — `providers/sglang` (mirror `inbox/openclaw_docs/providers/sglang.md`)
**Last Updated**: 2026-06-22
**Status**: Active
