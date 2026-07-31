---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - vllm
keywords:
  - openclaw vllm provider
  - vllm openai-compatible local server
  - VLLM_API_KEY
  - vllm model discovery
  - qwen thinking controls vllm
  - nemotron thinking controls
  - qwen tool calls as text
  - vllm custom base url timeout
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/vllm
access_control_group: ["general"]
---

# OpenClaw — vLLM Local Provider Setup

## Overview

This note is the step-by-step procedure for running OpenClaw against a local or LAN **vLLM** server, mirroring the `providers/vllm` source page. vLLM serves open-source (and some custom) models over an **OpenAI-compatible** HTTP API, and OpenClaw connects to it through the `openai-completions` API as a proxy-style `/v1` backend. It covers the four-step getting-started flow (`VLLM_API_KEY` opt-in, model ref, `openclaw models list` verification), implicit model discovery vs explicit manual-model config, the advanced compatibility controls (proxy-style request shaping, Qwen and Nemotron thinking formats, the Qwen tool-call-as-text workaround, custom base URL), and the troubleshooting accordions (slow/timeout, unreachable server, auth errors, no models discovered, tools rendered as text).

## Provider properties

The bundled `vllm` provider plugin is summarized by the source header table (copied verbatim):

| Property         | Value                                    |
| ---------------- | ---------------------------------------- |
| Provider ID      | `vllm`                                   |
| API              | `openai-completions` (OpenAI-compatible) |
| Auth             | `VLLM_API_KEY` environment variable      |
| Default base URL | `http://127.0.0.1:8000/v1`               |

OpenClaw treats `vllm` as a local OpenAI-compatible provider that supports streamed usage accounting, so status/context token counts can update from `stream_options.include_usage` responses. Setting `VLLM_API_KEY` (any value works if your server does not enforce auth) opts you into auto-discovery of the server's available models; using `vllm/*` in `agents.defaults.models` keeps discovery dynamic even when you configure a custom vLLM base URL.

## Getting started

The source documents a four-step setup:

1. **Start vLLM with an OpenAI-compatible server.** The base URL should expose `/v1` endpoints (e.g. `/v1/models`, `/v1/chat/completions`); vLLM commonly runs on `http://127.0.0.1:8000/v1`.
2. **Set the API key environment variable.** Any value works if your server does not enforce auth — `export VLLM_API_KEY="vllm-local"`.
3. **Select a model.** Set `agents.defaults.model.primary` to one of your vLLM model IDs as `vllm/your-model-id`.
4. **Verify the model is available** with `openclaw models list --provider vllm`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "vllm/your-model-id" },
    },
  },
}
```

## Model discovery (implicit provider)

When `VLLM_API_KEY` is set (or an auth profile exists) and you do **not** define `models.providers.vllm`, OpenClaw queries `GET http://127.0.0.1:8000/v1/models` and converts the returned IDs into model entries. If you set `models.providers.vllm` explicitly, OpenClaw uses your declared models by default; add `"vllm/*": {}` to `agents.defaults.models` when you want OpenClaw to query that configured provider's `/models` endpoint and include all advertised vLLM models.

## Explicit configuration (manual models)

Use explicit config when vLLM runs on a different host or port, you want to pin `contextWindow` or `maxTokens` values, your server requires a real API key (or you want to control headers), or you connect to a trusted loopback, LAN, or Tailscale vLLM endpoint. The block below pins a manual model row verbatim from source:

```json5
{
  models: {
    providers: {
      vllm: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "${VLLM_API_KEY}",
        api: "openai-completions",
        timeoutSeconds: 300, // Optional: extend connect/header/body/request timeout for slow local models
        models: [
          {
            id: "your-model-id",
            name: "Local vLLM Model",
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

To keep this provider dynamic without manually listing every model, add a provider wildcard to the visible model catalog — `agents.defaults.models` with `"vllm/*": {}`.

## Advanced configuration

**Proxy-style behavior.** vLLM is treated as a proxy-style OpenAI-compatible `/v1` backend, not a native OpenAI endpoint. As a result, the following are NOT applied: Native OpenAI request shaping (No), `service_tier` (Not sent), Responses `store` (Not sent), Prompt-cache hints (Not sent), OpenAI reasoning-compat payload shaping (Not applied), and Hidden OpenClaw attribution headers (Not injected on custom base URLs).

**Qwen thinking controls.** For Qwen models served through vLLM, set `compat.thinkingFormat: "qwen-chat-template"` on the configured provider model row when the server expects Qwen chat-template kwargs. Models configured this way expose a binary `/think` profile (`off`, `on`) because Qwen template thinking is an on/off request flag, not an OpenAI-style effort ladder. OpenClaw maps `/think off` to `chat_template_kwargs` with `enable_thinking: false` and `preserve_thinking: true`; non-`off` thinking levels send `enable_thinking: true`. If your endpoint expects DashScope-style top-level flags instead, use `compat.thinkingFormat: "qwen"` to send `enable_thinking` at the request root.

```json5
{
  models: {
    providers: {
      vllm: {
        models: [
          {
            id: "Qwen/Qwen3-8B",
            name: "Qwen3 8B",
            reasoning: true,
            compat: { thinkingFormat: "qwen-chat-template" },
          },
        ],
      },
    },
  },
}
```

**Nemotron 3 thinking controls.** vLLM/Nemotron 3 can use chat-template kwargs to control whether reasoning is returned as hidden reasoning or visible answer text. When an OpenClaw session uses `vllm/nemotron-3-*` with thinking off, the bundled vLLM plugin sends `chat_template_kwargs` with `enable_thinking: false` and `force_nonempty_content: true`. To customize these values, set `chat_template_kwargs` under the model params; if you also set `params.extra_body.chat_template_kwargs`, that value has final precedence because `extra_body` is the last request-body override (configured under `agents.defaults.models` as `"vllm/nemotron-3-super": { params: { chat_template_kwargs: { enable_thinking: false, force_nonempty_content: true } } }`).

**Qwen tool calls appear as text.** First make sure vLLM was started with the right tool-call parser and chat template for the model (vLLM documents `hermes` for Qwen2.5 models and `qwen3_xml` for Qwen3-Coder models). Symptoms: skills or tools never run; the assistant prints raw JSON/XML such as `{"name":"read","arguments":...}`; vLLM returns an empty `tool_calls` array when OpenClaw sends `tool_choice: "auto"`. Some Qwen/vLLM combinations return structured tool calls only when the request uses `tool_choice: "required"`, so force the OpenAI-compatible request field per-model with `params.extra_body`:

```json5
{
  agents: {
    defaults: {
      models: {
        "vllm/Qwen-Qwen2.5-Coder-32B-Instruct": {
          params: {
            extra_body: {
              tool_choice: "required",
            },
          },
        },
      },
    },
  },
}
```

Replace `Qwen-Qwen2.5-Coder-32B-Instruct` with the exact id returned by `openclaw models list --provider vllm`; the same override can be applied from the CLI via `openclaw config set agents.defaults.models '{...}' --strict-json --merge`. This is an opt-in compatibility workaround that makes every model turn with tools require a tool call, so use it only for a dedicated local model entry where that behavior is acceptable — not as a global default for all vLLM models, and not via a proxy that blindly converts arbitrary assistant text into executable tool calls.

**Custom base URL.** If your vLLM server runs on a non-default host or port, set `baseUrl` in the explicit provider config (e.g. `models.providers.vllm.baseUrl: "http://192.168.1.50:9000/v1"` with `apiKey: "${VLLM_API_KEY}"`, `api: "openai-completions"`, `timeoutSeconds: 300`, and a manual model row pinning `contextWindow`/`maxTokens`).

## Troubleshooting

**Slow first response or remote server timeout.** For large local models, remote LAN hosts, or tailnet links, set a provider-scoped request timeout (`timeoutSeconds`) on `models.providers.vllm`. `timeoutSeconds` applies to vLLM model HTTP requests only, including connection setup, response headers, body streaming, and the total guarded-fetch abort — prefer this before increasing `agents.defaults.timeoutSeconds`, which controls the whole agent run.

```json5
{
  models: {
    providers: {
      vllm: {
        baseUrl: "http://192.168.1.50:8000/v1",
        apiKey: "${VLLM_API_KEY}",
        api: "openai-completions",
        timeoutSeconds: 300,
        models: [{ id: "your-model-id", name: "Local vLLM Model" }],
      },
    },
  },
}
```

**Server not reachable.** Check that the server is running and accessible with `curl http://127.0.0.1:8000/v1/models`; if you see a connection error, verify the host, port, and that vLLM started with the OpenAI-compatible server mode. For explicit loopback, LAN, or Tailscale endpoints, OpenClaw trusts the exact configured `models.providers.vllm.baseUrl` origin for guarded model requests, while metadata/link-local origins remain blocked without explicit opt-in. Set `models.providers.vllm.request.allowPrivateNetwork: true` only when vLLM requests must reach another private origin, and set it to `false` to opt out of exact-origin trust.

**Auth errors on requests.** If requests fail with auth errors, set a real `VLLM_API_KEY` that matches your server configuration, or configure the provider explicitly under `models.providers.vllm`. If your vLLM server does not enforce auth, any non-empty value for `VLLM_API_KEY` works as an opt-in signal for OpenClaw.

**No models discovered.** Auto-discovery requires `VLLM_API_KEY` to be set. If you have defined `models.providers.vllm`, OpenClaw uses only your declared models unless `agents.defaults.models` includes `"vllm/*": {}`.

**Tools render as raw text.** If a Qwen model prints JSON/XML tool syntax instead of executing a skill, check the Qwen guidance in Advanced configuration above. The usual fix is to start vLLM with the correct parser/template for that model, confirm the exact model id with `openclaw models list --provider vllm`, and add a dedicated per-model `params.extra_body.tool_choice: "required"` override only if `tool_choice: "auto"` still returns empty or text-only tool calls.

**Source**: OpenClaw documentation — `providers/vllm` (mirror `inbox/openclaw_docs/providers/vllm.md`)
**Last Updated**: 2026-06-22
**Status**: Active
