---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - moonshot
keywords:
  - openclaw moonshot provider
  - kimi k2 moonshot
  - moonshot vs kimi coding
  - moonshot api key kimi api key
  - kimi k2.7 code native thinking
  - kimi web search provider
  - tool call id sanitization moonshot
  - moonshot streaming usage compat
topics:
  - OpenClaw
  - Moonshot Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/moonshot
access_control_group: ["general"]
---

# OpenClaw — Configure the Moonshot AI (Kimi K2) Provider

## Overview

This note is the setup procedure for using Moonshot AI's Kimi API in OpenClaw, mirroring the `providers/moonshot` source page. Moonshot provides the Kimi API with OpenAI-compatible endpoints; you configure the provider and set the default model to `moonshot/kimi-k2.6`, or use Kimi Coding with `kimi/kimi-for-coding`. The page's load-bearing warning: **Moonshot and Kimi Coding are separate providers** — keys are not interchangeable, endpoints differ, and model refs differ (`moonshot/...` vs `kimi/...`). It covers the built-in K2 catalog and pricing, the two onboarding flows (Moonshot Open Platform intl/CN + Kimi Coding plugin), the Kimi `web_search` provider, and the advanced configuration accordions (native thinking mode, tool-call-id sanitization, streaming-usage compatibility, and the endpoint/model-ref reference).

## Built-in Model Catalog

The bundled Moonshot catalog seeds six Kimi K2 model refs. `moonshot/kimi-k2.6` (Kimi K2.6) is the onboarding default — reasoning No, input text+image, 262,144 context / 262,144 max output. `moonshot/kimi-k2.7-code` (Kimi K2.7 Code) has reasoning **Always on**, text+image input, 262,144 / 262,144. `moonshot/kimi-k2.5` (Kimi K2.5): reasoning No, text+image, 262,144 / 262,144. `moonshot/kimi-k2-thinking` (Kimi K2 Thinking): reasoning Yes, text input only, 262,144 / 262,144. `moonshot/kimi-k2-thinking-turbo` (Kimi K2 Thinking Turbo): reasoning Yes, text only, 262,144 / 262,144. `moonshot/kimi-k2-turbo` (Kimi K2 Turbo): reasoning No, text only, 256,000 context / 16,384 max output.

Bundled cost estimates for current Moonshot-hosted K2 models use Moonshot's published pay-as-you-go rates: **Kimi K2.7 Code** is $0.19/MTok cache hit, $0.95/MTok input, $4.00/MTok output; **Kimi K2.6** is $0.16/MTok cache hit, $0.95/MTok input, $4.00/MTok output; **Kimi K2.5** is $0.10/MTok cache hit, $0.60/MTok input, $3.00/MTok output. Other legacy catalog entries (`kimi-k2-thinking`, `kimi-k2-thinking-turbo`, `kimi-k2-turbo`) keep zero-cost placeholders unless you override them in config.

Kimi K2.7 Code always uses native thinking: OpenClaw exposes only the `on` thinking state for this model and omits outbound `thinking` and `reasoning_effort` controls, as required by Moonshot. OpenClaw also omits sampling overrides that K2.7 fixes to provider defaults. Kimi K2.6 remains the onboarding default.

## Getting Started

### Moonshot API (Moonshot Open Platform)

Best for Kimi K2 models via the Moonshot Open Platform. First choose your endpoint region — the auth choice determines both the endpoint and the region: `moonshot-api-key` → `https://api.moonshot.ai/v1` (International); `moonshot-api-key-cn` → `https://api.moonshot.cn/v1` (China). Then run onboarding (`openclaw onboard --auth-choice moonshot-api-key`, or `--auth-choice moonshot-api-key-cn` for China), set a default model (`{ agents: { defaults: { model: { primary: "moonshot/kimi-k2.6" } } } }`), verify availability with `openclaw models list --provider moonshot`, and optionally run a live smoke test in an isolated state dir:

```bash
OPENCLAW_CONFIG_PATH=/tmp/openclaw-kimi/openclaw.json \
OPENCLAW_STATE_DIR=/tmp/openclaw-kimi \
openclaw agent --local \
  --session-id live-kimi-cost \
  --message 'Reply exactly: KIMI_LIVE_OK' \
  --thinking off \
  --json
```

The JSON response should report `provider: "moonshot"` and `model: "kimi-k2.6"`; the assistant transcript entry stores normalized token usage plus estimated cost under `usage.cost` when Moonshot returns usage metadata. The full Moonshot provider config block sets the API key from env, the default + aliased model list, and the `models.providers.moonshot` entry (`baseUrl`, `apiKey`, `api: "openai-completions"`, and the seeded `models[]`):

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.6" },
      models: {
        "moonshot/kimi-k2.6": { alias: "Kimi K2.6" },
        "moonshot/kimi-k2.7-code": { alias: "Kimi K2.7 Code" },
        "moonshot/kimi-k2.5": { alias: "Kimi K2.5" },
        "moonshot/kimi-k2-thinking": { alias: "Kimi K2 Thinking" },
        "moonshot/kimi-k2-thinking-turbo": { alias: "Kimi K2 Thinking Turbo" },
        "moonshot/kimi-k2-turbo": { alias: "Kimi K2 Turbo" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.6",
            name: "Kimi K2.6",
            reasoning: false,
            input: ["text", "image"],
            cost: { input: 0.95, output: 4, cacheRead: 0.16, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
          {
            id: "kimi-k2.7-code",
            name: "Kimi K2.7 Code",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0.95, output: 4, cacheRead: 0.19, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
          // ...kimi-k2.5, kimi-k2-thinking, kimi-k2-thinking-turbo, kimi-k2-turbo
        ],
      },
    },
  },
}
```

### Kimi Coding

Best for code-focused tasks via the Kimi Coding endpoint. Install the official plugin then restart Gateway (`openclaw plugins install @openclaw/kimi-provider` then `openclaw gateway restart`). Kimi Coding uses a **different API key and provider prefix** (`kimi/...`) than Moonshot (`moonshot/...`). The stable API model ref is `kimi/kimi-for-coding`; legacy refs `kimi/kimi-code` and `kimi/k2p5` remain accepted and normalize to that API model id. Run onboarding with `openclaw onboard --auth-choice kimi-code-api-key`, set the default model to `kimi/kimi-for-coding`, and verify with `openclaw models list --provider kimi`. The config example:

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi/kimi-for-coding" },
      models: {
        "kimi/kimi-for-coding": { alias: "Kimi" },
      },
    },
  },
}
```

## Kimi Web Search

OpenClaw also ships **Kimi** as a `web_search` provider, backed by Moonshot web search. Run interactive setup with `openclaw configure --section web` and choose **Kimi** in the web-search section to store `plugins.entries.moonshot.config.webSearch.*`. Interactive setup prompts for the API region (`https://api.moonshot.ai/v1` international or `https://api.moonshot.cn/v1` China) and the web search model (defaults to `kimi-k2.6`). Config lives under `plugins.entries.moonshot.config.webSearch` and wires `tools.web.search.provider: "kimi"`:

```json5
{
  plugins: {
    entries: {
      moonshot: {
        config: {
          webSearch: {
            apiKey: "sk-...", // or use KIMI_API_KEY / MOONSHOT_API_KEY
            baseUrl: "https://api.moonshot.ai/v1",
            model: "kimi-k2.6",
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "kimi",
      },
    },
  },
}
```

## Advanced Configuration

### Native thinking mode

Kimi K2.7 Code always uses native thinking. Moonshot requires clients to omit the `thinking` field for this model, so OpenClaw exposes only `on` and ignores stale `off` settings. K2.7 also fixes `temperature`, `top_p`, `n`, `presence_penalty`, and `frequency_penalty`; OpenClaw omits configured overrides for those fields. Other Moonshot Kimi models support binary native thinking — `thinking: { type: "enabled" }` or `thinking: { type: "disabled" }` — configured per model via `agents.defaults.models.<provider/model>.params`. OpenClaw maps runtime `/think` levels for those models: `/think off` → `thinking.type=disabled`; any non-off level → `thinking.type=enabled`. When Moonshot thinking is enabled, `tool_choice` must be `auto` or `none`, and OpenClaw normalizes incompatible values to `auto`; this includes Kimi K2.7 Code, whose thinking mode cannot be disabled to preserve a pinned tool choice. Kimi K2.6 also accepts an optional `thinking.keep` field that controls multi-turn retention of `reasoning_content`: set it to `"all"` to keep full reasoning across turns, or omit it (or leave it `null`) to use the server default strategy. OpenClaw only forwards `thinking.keep` for `moonshot/kimi-k2.6` and strips it from other models; Kimi K2.7 Code preserves full reasoning history by default while OpenClaw omits the entire `thinking` field.

```json5
{
  agents: {
    defaults: {
      models: {
        "moonshot/kimi-k2.6": {
          params: {
            thinking: { type: "enabled", keep: "all" },
          },
        },
      },
    },
  },
}
```

### Tool call id sanitization

Moonshot Kimi serves native `tool_call` ids shaped like `functions.<name>:<index>`. For the OpenAI-completions transport, OpenClaw preserves the first occurrence of each native Kimi id and rewrites later duplicates to deterministic OpenAI-style `call_*` ids; matching tool results are remapped with the same id so replay remains unique without stripping Kimi's first native id. To force strict sanitization on a custom OpenAI-compatible provider, set `sanitizeToolCallIds: true` under `models.providers.<id>` (with `api: "openai-completions"`).

### Streaming usage compatibility

Native Moonshot endpoints (`https://api.moonshot.ai/v1` and `https://api.moonshot.cn/v1`) advertise streaming usage compatibility on the shared `openai-completions` transport. OpenClaw keys that off endpoint capabilities, so compatible custom provider ids targeting the same native Moonshot hosts inherit the same streaming-usage behavior. With the bundled K2.6 pricing, streamed usage that includes input, output, and cache-read tokens is also converted into local estimated USD cost for `/status`, `/usage full`, `/usage cost`, and transcript-backed session accounting.

### Endpoint and model ref reference

The four provider/region rows and their auth env vars: **Moonshot** → prefix `moonshot/`, endpoint `https://api.moonshot.ai/v1`, env `MOONSHOT_API_KEY`. **Moonshot CN** → prefix `moonshot/`, endpoint `https://api.moonshot.cn/v1`, env `MOONSHOT_API_KEY`. **Kimi Coding** → prefix `kimi/`, the Kimi Coding endpoint, env `KIMI_API_KEY`. **Web search** → no prefix (N/A), same as the Moonshot API region, env `KIMI_API_KEY` or `MOONSHOT_API_KEY`. Kimi web search uses `KIMI_API_KEY` or `MOONSHOT_API_KEY` and defaults to `https://api.moonshot.ai/v1` with model `kimi-k2.6`. Override pricing and context metadata in `models.providers` if needed, and if Moonshot publishes different context limits for a model, adjust `contextWindow` accordingly.

**Source**: OpenClaw documentation — `providers/moonshot` (mirror `inbox/openclaw_docs/providers/moonshot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
