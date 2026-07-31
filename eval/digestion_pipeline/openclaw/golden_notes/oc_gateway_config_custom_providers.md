---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - providers
keywords:
  - openclaw custom provider
  - models.providers config
  - baseurl override
  - openai-compatible endpoint
  - self-hosted llm provider
  - provider api adapter
  - models mode merge replace
  - openclaw provider examples
topics:
  - OpenClaw
  - Gateway Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-tools
access_control_group: ["general"]
---

# OpenClaw — Custom Providers and Base URLs

## Overview

This note is the procedure for registering custom model providers and overriding base URLs in OpenClaw's `models.providers.*` config. It mirrors the "Custom providers and base URLs" half of the `gateway/config-tools` source page — the provider top-level catalog (`models.mode`, `models.providers`), connection/auth fields (`api`, `apiKey`, `auth`, `baseUrl`, `headers`, `timeoutSeconds`), request transport overrides (`request.headers`/`auth`/`proxy`/`tls`/`allowPrivateNetwork`), model-catalog entries (`models[]` + `compat.*` hints), and the worked provider examples (Cerebras, Kimi, MiniMax, Moonshot, OpenCode, Synthetic, Z.AI). The companion tool-policy half of the same page is [oc_gateway_config_tools_policy](oc_gateway_config_tools_policy.md).

## Registering a Custom Provider

Provider plugins publish their own model catalog rows. Add custom providers via `models.providers` in config or `~/.openclaw/agents/<agentId>/agent/models.json`. Per the source, "Configuring a custom/local provider `baseUrl` is also the narrow network trust decision for model HTTP requests: OpenClaw allows that exact `scheme://host:port` origin through the guarded fetch path, without adding a separate config option or trusting other private origins." A minimal custom provider — an OpenAI-compatible proxy fronting a self-hosted Llama model — looks like this:

```json5
{
  models: {
    mode: "merge", // merge (default) | replace
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions", // openai-completions | openai-responses | anthropic-messages | google-generative-ai
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            contextTokens: 96000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

## Auth and Merge Precedence

Use `authHeader: true` + `headers` for custom auth needs, and override the agent config root with `OPENCLAW_AGENT_DIR`. For matching provider IDs the source defines this merge precedence: non-empty agent `models.json` `baseUrl` values win; non-empty agent `apiKey` values win only when that provider is not SecretRef-managed in the current config/auth-profile context; SecretRef-managed provider `apiKey` and header values are refreshed from source markers (`ENV_VAR_NAME` for env refs, `secretref-managed` for file/exec refs; `secretref-env:ENV_VAR_NAME` for env header refs) instead of persisting resolved secrets; empty or missing agent `apiKey`/`baseUrl` fall back to `models.providers` in config; matching model `contextWindow`/`maxTokens` use the higher value between explicit config and implicit catalog values; matching model `contextTokens` preserves an explicit runtime cap when present. Provider-plugin catalogs are stored as generated plugin-owned catalog shards under the agent's plugin state. Use `models.mode: "replace"` when you want config to fully rewrite `models.json` and active plugin catalog shards. Marker persistence is source-authoritative — markers are written from the active source config snapshot (pre-resolution), not from resolved runtime secret values.

## Provider Field Details

**Top-level catalog.** `models.mode` sets provider catalog behavior (`merge` or `replace`); `models.providers` is the custom provider map keyed by provider id. For safe additive edits, use `openclaw config set models.providers.<id> '<json>' --strict-json --merge` or `openclaw config set models.providers.<id>.models '<json-array>' --strict-json --merge`; `config set` refuses destructive replacements unless you pass `--replace`.

**Provider connection and auth.** `models.providers.*.api` selects the request adapter (`openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative-ai`, etc). For self-hosted `/v1/chat/completions` backends such as MLX, vLLM, SGLang, and most OpenAI-compatible local servers, use `openai-completions`; a custom provider with `baseUrl` but no `api` defaults to `openai-completions`, and `openai-responses` should be set only when the backend supports `/v1/responses`. Other connection fields: `apiKey` (provider credential — prefer SecretRef/env substitution); `auth` (auth strategy — `api-key`, `token`, `oauth`, `aws-sdk`); `contextWindow`, `contextTokens`, and `maxTokens` (provider-level defaults applied when a model entry omits them); `timeoutSeconds` (per-provider model HTTP request timeout in seconds, covering connect, headers, body, and total request abort handling); `injectNumCtxForOpenAICompat` (for Ollama + `openai-completions`, inject `options.num_ctx` into requests, default `true`); `authHeader` (force credential transport in the `Authorization` header); `baseUrl` (upstream API base URL); and `headers` (extra static headers for proxy/tenant routing).

**Request transport overrides.** `models.providers.*.request` overrides model-provider HTTP transport: `request.headers` (extra headers merged with provider defaults; values accept SecretRef); `request.auth` (override modes `"provider-default"`, `"authorization-bearer"` with `token`, `"header"` with `headerName`/`value`/optional `prefix`); `request.proxy` (`"env-proxy"` using `HTTP_PROXY`/`HTTPS_PROXY`, or `"explicit-proxy"` with `url`, both accepting an optional `tls` sub-object); `request.tls` (`ca`, `cert`, `key`, `passphrase` — all accept SecretRef — plus `serverName`, `insecureSkipVerify`); and `request.allowPrivateNetwork` (when `true`, allow requests to private/CGNAT/similar ranges through the provider HTTP fetch guard; custom/local base URLs already trust the exact configured origin except metadata/link-local origins; set `false` to opt out of exact-origin trust; WebSocket reuses `request` headers/TLS but not the fetch SSRF gate; default `false`).

**Model catalog entries.** `models.providers.*.models` lists explicit catalog entries; `models.*.input` sets modalities (`["text"]` text-only, `["text", "image"]` native vision — image attachments are injected only when the selected model is image-capable); `models.*.contextWindow` and `models.*.contextTokens` override the provider-level defaults (the latter caps the effective context budget below the native window; `openclaw models list` shows both when they differ). The `compat.*` hints tune OpenAI-compatible backends: `supportsDeveloperRole` (forced `false` at runtime for `api: "openai-completions"` with a non-empty non-native `baseUrl`); `requiresStringContent` (flatten pure-text `messages[].content` arrays to plain strings); `strictMessageKeys` (strip outgoing Chat Completions messages to `role` and `content`); `thinkingFormat` (`"together"`, `"qwen"`, or `"qwen-chat-template"` for Qwen-family servers such as vLLM); and `requiresReasoningContentOnAssistantMessages` (preserve `reasoning_content` on outgoing assistant messages for DeepSeek-style backends; default `false`).

**Amazon Bedrock discovery.** `plugins.entries.amazon-bedrock.config.discovery` is the Bedrock auto-discovery root: `enabled` (toggle), `region` (AWS region), `providerFilter` (optional provider-id filter), `refreshInterval` (polling interval), `defaultContextWindow`, and `defaultMaxTokens` (fallbacks for discovered models).

Interactive custom-provider onboarding infers image input for common vision model IDs (GPT-4o, Claude, Gemini, Qwen-VL, LLaVA, Pixtral, InternVL, Mllama, MiniCPM-V, GLM-4V) and skips the extra question for known text-only families; unknown model IDs still prompt. Non-interactive onboarding uses the same inference — pass `--custom-image-input` to force image-capable metadata or `--custom-text-input` to force text-only.

## Provider Examples

The source supplies worked `json5` recipes per provider. **Cerebras** (GLM 4.7 / GPT OSS) is configurable via `openclaw onboard --auth-choice cerebras-api-key`; explicit config is only for overriding defaults (`baseUrl: "https://api.cerebras.ai/v1"`, `api: "openai-completions"`). **Kimi Coding** is an Anthropic-compatible built-in provider (`model.primary: "kimi/kimi-for-coding"`; shortcut `openclaw onboard --auth-choice kimi-code-api-key`). **Local models (LM Studio)** are covered by the Local Models page — run a large local model via the LM Studio Responses API and keep hosted models merged for fallback. **MiniMax M3 (direct)** uses `baseUrl: "https://api.minimax.io/anthropic"`, `api: "anthropic-messages"`, `MINIMAX_API_KEY`; MiniMax M2.x thinking is disabled by default on the Anthropic-compatible streaming path unless `thinking` is set, while MiniMax-M3/M3.x stays on the omitted/adaptive thinking path, and `/fast on` (or `params.fastMode: true`) rewrites `MiniMax-M2.7` to `MiniMax-M2.7-highspeed`. **Moonshot AI (Kimi)** uses `baseUrl: "https://api.moonshot.ai/v1"` (China: `https://api.moonshot.cn/v1`), `api: "openai-completions"`, `MOONSHOT_API_KEY`. **OpenCode** uses `opencode/...` refs (Zen catalog) or `opencode-go/...` (Go catalog) with `OPENCODE_API_KEY`/`OPENCODE_ZEN_API_KEY`. **Synthetic** is Anthropic-compatible (`baseUrl: "https://api.synthetic.new/anthropic"`, `api: "anthropic-messages"`) and the base URL should omit `/v1` because the Anthropic client appends it. **Z.AI (GLM-4.7)** uses canonical `zai/*` refs with `ZAI_API_KEY`; its general endpoint is `https://api.z.ai/api/paas/v4` and the default coding endpoint is `https://api.z.ai/api/coding/paas/v4` — define a custom provider with the base-URL override to use the general endpoint.

**Source**: OpenClaw documentation — `gateway/config-tools` (mirror `inbox/openclaw_docs/gateway/config-tools.md`), "Custom providers and base URLs" section
**Last Updated**: 2026-06-22
**Status**: Active
