---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - custom_models
keywords:
  - openclaw custom providers
  - models.providers base url
  - openai-completions anthropic-messages
  - local inference lmstudio ollama vllm sglang
  - litellm openai-compatible proxy
  - moonshot kimi volcengine byteplus synthetic minimax
  - proxy route shaping extra_body
  - allowprivatenetwork base url trust
topics:
  - OpenClaw
  - Custom Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/model-providers
access_control_group: ["general"]
---

# OpenClaw — Custom and Base-URL Model Providers (`models.providers`)

## Overview

This note is the procedure for adding **custom / base-URL model providers** to OpenClaw through the `models.providers` config block (or `models.json`), covering the second half of the `concepts/model-providers` source page. Use `models.providers` (or `models.json`) to add custom providers or OpenAI/Anthropic-compatible proxies. Many of the bundled provider plugins documented here already publish a default catalog, so you add explicit `models.providers.<id>` entries only when you want to override the default base URL, headers, or model list. The note walks the per-provider setup blocks (Moonshot/Kimi, Kimi coding, Volcano Engine, BytePlus, Synthetic, MiniMax) and the local-inference / proxy providers (LM Studio, Ollama, vLLM, SGLang, and OpenAI/Anthropic-compatible local proxies), then the optional-field defaults and the proxy-route shaping rules. The companion official/bundled-plugin half is in [oc_concepts_model_providers_official](oc_concepts_model_providers_official.md).

## When to Use `models.providers` vs the Allowlist

`agents.defaults.models["provider/model"]` only controls model **visibility, aliases, and per-model metadata** for agents — it does **not** register a new runtime model by itself. For custom provider models, you must **also** add `models.providers.<provider>.models[]` with at least the matching `id`. Gateway model capability checks also read explicit `models.providers.<id>.models[]` metadata: if a custom or proxy model accepts images, set `input: ["text", "image"]` on that model so WebChat and node-origin attachment paths pass images as native model inputs instead of text-only media refs. Provider- vs per-model defaults follow the order documented in the page's Quick rules: `models.providers.*.contextWindow` / `contextTokens` / `maxTokens` set provider-level defaults, and `models.providers.*.models[].contextWindow` / `contextTokens` / `maxTokens` override them per model.

## Custom OpenAI/Anthropic-Compatible Cloud Providers

Several bundled providers ship as plugins but are configured (or overridden) through `models.providers` because they expose a custom endpoint. The core fields per provider are `baseUrl`, `apiKey` (typically a `${ENV}` marker), `api` (the wire protocol — `openai-completions` or `anthropic-messages`), and a `models[]` list of `{ id, name, ... }` entries. Set `models.mode: "merge"` to add these entries on top of the built-in catalog.

- **Moonshot AI (Kimi)** — bundled plugin; use the built-in provider by default and add an explicit `models.providers.moonshot` entry only to override the base URL or model metadata. Provider `moonshot`, auth `MOONSHOT_API_KEY`, example `moonshot/kimi-k2.6`, CLI `openclaw onboard --auth-choice moonshot-api-key` (or `...-cn`). Kimi K2 model IDs include `moonshot/kimi-k2.6`, `moonshot/kimi-k2.7-code`, `moonshot/kimi-k2.5`, `moonshot/kimi-k2-thinking`, `moonshot/kimi-k2-thinking-turbo`, `moonshot/kimi-k2-turbo`.
- **Kimi coding** — uses Moonshot AI's Anthropic-compatible endpoint. Provider `kimi`, auth `KIMI_API_KEY`, example `kimi/kimi-for-coding`. Legacy `kimi/kimi-code` and `kimi/k2p5` remain accepted as compatibility model ids and normalize to Kimi's stable API model id.
- **Volcano Engine (Doubao)** — access to Doubao and other models in China. Provider `volcengine` (coding: `volcengine-plan`), auth `VOLCANO_ENGINE_API_KEY`, example `volcengine-plan/ark-code-latest`, CLI `openclaw onboard --auth-choice volcengine-api-key`. Onboarding defaults to the coding surface but registers the general `volcengine/*` catalog at the same time; pickers prefer both `volcengine/*` and `volcengine-plan/*` rows and fall back to the unfiltered catalog rather than show an empty picker.
- **BytePlus (International)** — BytePlus ARK provides the same models as Volcano Engine for international users. Provider `byteplus` (coding: `byteplus-plan`), auth `BYTEPLUS_API_KEY`, example `byteplus-plan/ark-code-latest`, CLI `openclaw onboard --auth-choice byteplus-api-key`. Same onboarding/picker behavior as Volcano Engine.
- **Synthetic** — Anthropic-compatible models behind the `synthetic` provider. Auth `SYNTHETIC_API_KEY`, example `synthetic/hf:MiniMaxAI/MiniMax-M2.5`, CLI `openclaw onboard --auth-choice synthetic-api-key`.
- **MiniMax** — configured via `models.providers` because it uses custom endpoints; auth choices `minimax-global-oauth`, `minimax-cn-oauth`, `minimax-global-api`, `minimax-cn-api`. Auth `MINIMAX_API_KEY` for `minimax`; `MINIMAX_OAUTH_TOKEN` or `MINIMAX_API_KEY` for `minimax-portal`. On MiniMax's Anthropic-compatible streaming path OpenClaw disables thinking by default for the M2.x family unless explicitly set; `MiniMax-M3`/M3.x stay on the provider's omitted/adaptive thinking path, and `/fast on` rewrites `MiniMax-M2.7` to `MiniMax-M2.7-highspeed`. Capability split: text/chat on `minimax/MiniMax-M3`, image generation `minimax/image-01` or `minimax-portal/image-01`, image understanding plugin-owned `MiniMax-VL-01`, web search on provider id `minimax`. See `/providers/minimax` for full setup.

A Moonshot `models.providers` override illustrates the standard shape (verbatim):

```json5
{
  agents: {
    defaults: { model: { primary: "moonshot/kimi-k2.6" } },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.6", name: "Kimi K2.6" }],
      },
    },
  },
}
```

Synthetic shows the `anthropic-messages` wire protocol variant (verbatim):

```json5
{
  agents: {
    defaults: { model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [{ id: "hf:MiniMaxAI/MiniMax-M2.5", name: "MiniMax M2.5" }],
      },
    },
  },
}
```

## Local Inference Servers

These bundled plugins point at a locally hosted inference server. Each is opt-in via an environment token (any value works if the server does not enforce auth) and discovers models from the server's own listing endpoint.

- **LM Studio** — bundled plugin using LM Studio's native API. Provider `lmstudio`, auth `LM_API_TOKEN`, default inference base URL `http://localhost:1234/v1`. OpenClaw uses LM Studio's native `/api/v1/models` and `/api/v1/models/load` for discovery + auto-load, with `/v1/chat/completions` for inference by default; pick a model id from `http://localhost:1234/api/v1/models`. To let LM Studio's JIT loading, TTL, and auto-evict own model lifecycle, set `models.providers.lmstudio.params.preload: false`. See `/providers/lmstudio`.
- **Ollama** — bundled plugin using Ollama's native API. Provider `ollama`, no auth required (local server), example `ollama/llama3.3`, install at `https://ollama.com/download`. Ollama is detected locally at `http://127.0.0.1:11434` when you opt in with `OLLAMA_API_KEY`, and the plugin adds Ollama directly to `openclaw onboard` and the model picker. See `/providers/ollama`.
- **vLLM** — bundled plugin for local/self-hosted OpenAI-compatible servers. Provider `vllm`, auth optional (depends on your server), default base URL `http://127.0.0.1:8000/v1`. Opt in to auto-discovery locally with `export VLLM_API_KEY="vllm-local"`, then pick a model id returned by `/v1/models`. See `/providers/vllm`.
- **SGLang** — bundled plugin for fast self-hosted OpenAI-compatible servers. Provider `sglang`, auth optional, default base URL `http://127.0.0.1:30000/v1`. Opt in with `export SGLANG_API_KEY="sglang-local"`, then pick a model id from `/v1/models`. See `/providers/sglang`.

A minimal Ollama config (verbatim):

```json5
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}
```

## Local Proxies (LM Studio, vLLM, LiteLLM, etc.)

For an OpenAI-compatible local proxy, define the full `models.providers.<id>` entry with a `models[]` array carrying explicit per-model metadata. The page's example wires LM Studio as a `lmstudio` proxy with a single fully-specified model (verbatim):

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/my-local-model" },
      models: { "lmstudio/my-local-model": { alias: "Local" } },
    },
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "${LM_API_TOKEN}",
        api: "openai-completions",
        timeoutSeconds: 300,
        models: [
          {
            id: "my-local-model",
            name: "Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### Default optional fields

For custom providers, `reasoning`, `input`, `cost`, `contextWindow`, and `maxTokens` are optional. When omitted, OpenClaw defaults to `reasoning: false`, `input: ["text"]`, `cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }`, `contextWindow: 200000`, and `maxTokens: 8192`. The page recommends setting explicit values that match your proxy/model limits.

### Proxy-route shaping rules

These rules govern how OpenClaw shapes outbound requests for non-native custom endpoints:

- For `api: "openai-completions"` on non-native endpoints (any non-empty `baseUrl` whose host is not `api.openai.com`), OpenClaw forces `compat.supportsDeveloperRole: false` to avoid provider `400` errors for unsupported `developer` roles. An explicit `compat.supportsDeveloperRole: true` is still overridden on non-native `openai-completions` endpoints for safety. If `baseUrl` is empty/omitted, OpenClaw keeps the default OpenAI behavior (which resolves to `api.openai.com`).
- Proxy-style OpenAI-compatible routes skip native-OpenAI-only request shaping: no `service_tier`, no Responses `store`, no Completions `store`, no prompt-cache hints, no OpenAI reasoning-compat payload shaping, and no hidden OpenClaw attribution headers.
- For OpenAI-compatible Completions proxies needing vendor-specific fields, set `agents.defaults.models["provider/model"].params.extra_body` (or `extraBody`) to merge extra JSON into the outbound request body.
- For vLLM chat-template controls, set `agents.defaults.models["provider/model"].params.chat_template_kwargs`. The bundled vLLM plugin automatically sends `enable_thinking: false` and `force_nonempty_content: true` for `vllm/nemotron-3-*` when the session thinking level is off.
- For slow local models or remote LAN/tailnet hosts, set `models.providers.<id>.timeoutSeconds` to extend provider model HTTP request handling (connect, headers, body streaming, total guarded-fetch abort) without increasing the whole agent runtime timeout; if `agents.defaults.timeoutSeconds` or a run-specific timeout is lower, raise that ceiling too because provider timeouts cannot extend the whole run.
- For `api: "anthropic-messages"` on non-direct endpoints (any provider other than canonical `anthropic`, or a custom `models.providers.anthropic.baseUrl` whose host is not a public `api.anthropic.com` endpoint), OpenClaw suppresses implicit Anthropic beta headers such as `claude-code-20250219`, `interleaved-thinking-2025-05-14`, and OAuth markers so custom Anthropic-compatible proxies do not reject unsupported beta flags. Set `models.providers.<id>.headers["anthropic-beta"]` explicitly if your proxy needs specific beta features.

### Private-network and origin trust

Model provider HTTP calls allow Surge, Clash, and sing-box fake-IP DNS answers in `198.18.0.0/15` and `fc00::/7` only for the configured provider `baseUrl` hostname. Custom/local provider endpoints also trust that exact configured `scheme://host:port` origin for guarded model requests, including loopback, LAN, and tailnet hosts — this is not a new config option; the `baseUrl` you configure extends the request policy only for that origin. Fake-IP hostname allowance and exact-origin trust are independent mechanisms. Other private, loopback, link-local, and metadata destinations, and different ports, still require an explicit `models.providers.<id>.request.allowPrivateNetwork: true` opt-in; set `models.providers.<id>.request.allowPrivateNetwork: false` to opt out of the exact-origin trust.

## CLI Examples

The page's CLI onboarding examples (verbatim):

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-6
openclaw models list
```

See also `/gateway/configuration` for full configuration examples.

**Source**: OpenClaw documentation — `concepts/model-providers` (mirror `inbox/openclaw_docs/concepts/model-providers.md`), section "Providers via `models.providers` (custom/base URL)" + CLI examples
**Last Updated**: 2026-06-22
**Status**: Active
