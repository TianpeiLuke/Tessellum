---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - providers
keywords:
  - openclaw official provider plugins
  - openclaw model providers
  - provider model ref provider/model
  - api key rotation openclaw
  - anthropic openai gemini provider setup
  - codex oauth chatgpt subscription
  - openclaw models auth login onboard
  - bundled provider plugins table
topics:
  - OpenClaw
  - Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/model-providers
access_control_group: ["general"]
---

# OpenClaw — Configuring Official / Bundled Provider Plugins

## Overview

This note is the **procedure** for configuring OpenClaw's official (bundled) LLM provider plugins — not chat channels like WhatsApp/Telegram. It mirrors the first half of the `concepts/model-providers` source page: quick rules for model refs and CLI helpers, why provider logic lives in plugins, multi-key API-key rotation, and per-provider auth/model/CLI setup for OpenAI, Anthropic, ChatGPT/Codex OAuth, OpenCode, Google Gemini, Vertex/Gemini CLI, Z.AI, Vercel AI Gateway, and the other bundled plugins, ending with CLI examples. The companion `oc_concepts_model_providers_custom` covers custom/base-URL providers; selection lives in `oc_concepts_models_selection` and failover in `oc_concepts_model_failover_*`.

## Quick Rules (Model Refs and CLI Helpers)

Model refs use the form `provider/model` (example: `opencode/claude-opus-4-6`). When set, `agents.defaults.models` acts as an **allowlist**. The core CLI helpers are `openclaw onboard`, `openclaw models list`, and `openclaw models set <provider/model>`. Provider-level context defaults are set with `models.providers.*.contextWindow` / `contextTokens` / `maxTokens`, and `models.providers.*.models[].contextWindow` / `contextTokens` / `maxTokens` override them per model. Fallback rules, cooldown probes, and session-override persistence are documented separately under Model failover.

**Adding provider auth does not change your primary model.** `openclaw configure` preserves an existing `agents.defaults.model.primary` when you add or reauth a provider, and `openclaw models auth login` does the same unless you pass `--set-default`. A plugin may return a recommended default model, but OpenClaw treats that as "make this model available" when a primary already exists, not "replace the current primary." To switch the default, use `openclaw models set <provider/model>` or `openclaw models auth login --provider <id> --set-default`.

**OpenAI provider/runtime split.** OpenAI-family routes are prefix-specific: `openai/<model>` uses the native Codex app-server harness for agent turns by default (the usual ChatGPT/Codex subscription setup); legacy Codex model refs are legacy config that doctor rewrites to `openai/<model>`; and `openai/<model>` plus `agentRuntime.id: "openclaw"` uses OpenClaw's built-in runtime for explicit API-key or compatibility routes. Plugin auto-enable follows the same boundary — `openai/*` agent refs enable the Codex plugin for the default route, and explicit `agentRuntime.id: "codex"` or legacy `codex/<model>` refs also require it.

**CLI runtimes** use the same split: choose canonical refs such as `anthropic/claude-*` or `google/gemini-*`, then set runtime policy to `claude-cli` or `google-gemini-cli` for a local CLI backend. Legacy `claude-cli/*` and `google-gemini-cli/*` refs migrate back to canonical refs with the runtime recorded separately; legacy `codex-cli/*` refs migrate to `openai/*` on the Codex app-server route (no bundled Codex CLI backend remains).

## Plugin-Owned Provider Behavior

Most provider-specific logic lives in provider plugins (`registerProvider(...)`) while OpenClaw keeps the generic inference loop. Plugins own onboarding, model catalogs, auth env-var mapping, transport/config normalization, tool-schema cleanup, failover classification, OAuth refresh, usage reporting, and thinking/reasoning profiles. The full list of provider-SDK hooks and bundled-plugin examples lives in the Provider plugins reference; a provider needing a totally custom request executor is a deeper extension surface. Provider-owned runner behavior lives on explicit provider hooks (replay policy, tool-schema normalization, stream wrapping, transport/request helpers) — the legacy `ProviderPlugin.capabilities` static bag is compatibility-only and no longer read by shared runner logic.

## API Key Rotation

**Key sources and priority** — configure multiple keys via (highest to lowest): `OPENCLAW_LIVE_<PROVIDER>_KEY` (single live override, highest priority); `<PROVIDER>_API_KEYS` (comma or semicolon list); `<PROVIDER>_API_KEY` (primary key); and `<PROVIDER>_API_KEY_*` (numbered list, e.g. `<PROVIDER>_API_KEY_1`). For Google providers, `GOOGLE_API_KEY` is also included as fallback. Key selection order preserves priority and deduplicates values.

**When rotation kicks in** — requests are retried with the next key **only on rate-limit responses** (e.g. `429`, `rate_limit`, `quota`, `resource exhausted`, `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, `workers_ai ... quota limit exceeded`, or periodic usage-limit messages). Non-rate-limit failures fail immediately with no rotation; when all candidate keys fail, the final error from the last attempt is returned.

## Official Provider Plugins

Official provider plugins publish their own model catalog rows, so these providers require **no** `models.providers` entries: enable the plugin, set auth, pick a model. Use `models.providers` only for explicit custom providers or narrow request settings such as timeouts.

### OpenAI

Provider `openai`; auth `OPENAI_API_KEY`; optional rotation `OPENAI_API_KEYS`, `OPENAI_API_KEY_1`, `OPENAI_API_KEY_2`, plus `OPENCLAW_LIVE_OPENAI_KEY`. Example models: `openai/gpt-5.5`, `openai/gpt-5.4-mini`. CLI: `openclaw onboard --auth-choice openai-api-key`; verify availability with `openclaw models list --provider openai`. Default transport is `auto`; override per model via `agents.defaults.models["openai/<model>"].params.transport` (`"sse"`, `"websocket"`, or `"auto"`). Priority processing uses `params.serviceTier`; `/fast` and `params.fastMode` map direct `openai/*` Responses requests to `service_tier=priority` on `api.openai.com`. Hidden attribution headers (`originator`, `version`, `User-Agent`) apply only on native OpenAI traffic to `api.openai.com`, not generic proxies; native routes also keep Responses `store`, prompt-cache hints, and reasoning-compat shaping, while proxy routes do not. `openai/gpt-5.3-codex-spark` is available through ChatGPT/Codex OAuth subscription auth when your account exposes it; OpenClaw suppresses direct OpenAI API-key and Azure API-key routes for it because those transports reject it.

```json5
{
  agents: { defaults: { model: { primary: "openai/gpt-5.5" } } },
}
```

### Anthropic

Provider `anthropic`; auth `ANTHROPIC_API_KEY`; optional rotation `ANTHROPIC_API_KEYS`, `ANTHROPIC_API_KEY_1`, `ANTHROPIC_API_KEY_2`, plus `OPENCLAW_LIVE_ANTHROPIC_KEY`. Example model: `anthropic/claude-opus-4-6`. CLI: `openclaw onboard --auth-choice apiKey`. Direct public Anthropic requests (API-key and OAuth traffic to `api.anthropic.com`) support the shared `/fast` toggle and `params.fastMode`, which OpenClaw maps to Anthropic `service_tier` (`auto` vs `standard_only`). The preferred Claude CLI config keeps the model ref canonical and selects the CLI backend separately: `anthropic/claude-opus-4-8` with model-scoped `agentRuntime.id: "claude-cli"`; legacy `claude-cli/claude-opus-4-7` refs still work. Per the source Note, Anthropic staff told OpenClaw that OpenClaw-style Claude CLI usage is allowed again, so OpenClaw treats Claude CLI reuse and `claude -p` as sanctioned unless Anthropic publishes a new policy; the Anthropic setup-token remains supported, but OpenClaw now prefers Claude CLI reuse and `claude -p` when available.

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

### OpenAI ChatGPT/Codex OAuth

Provider `openai`; auth OAuth (ChatGPT). The native Codex app-server harness ref is `openai/gpt-5.5`; legacy model refs are `codex/gpt-*`. Plugin boundary: `openai/*` loads the OpenAI plugin, and the native Codex app-server plugin is selected by the Codex harness runtime. CLI: `openclaw onboard --auth-choice openai` or `openclaw models auth login --provider openai`. Default transport is `auto` (WebSocket-first, SSE fallback); override via `params.transport`. `params.serviceTier` is forwarded on native Codex Responses requests (`chatgpt.com/backend-api`), where hidden attribution headers are also attached (not on generic proxies); it shares the same `/fast`/`params.fastMode` toggle as direct `openai/*`. `openai/gpt-5.5` uses the Codex catalog native `contextWindow = 400000` and default runtime `contextTokens = 272000`; override the runtime cap with `models.providers.openai.models[].contextTokens`. OpenAI Codex OAuth is explicitly supported for external tools/workflows like OpenClaw. For the common subscription-plus-native-Codex route, sign in with `openai` auth and configure `openai/gpt-5.5` (OpenAI agent turns select Codex by default); use `agentRuntime.id: "openclaw"` only for the built-in route. Legacy Codex GPT refs are legacy state, not a live route — run `openclaw doctor --fix` to migrate to canonical `openai/*`.

```json5
{
  plugins: { entries: { codex: { enabled: true } } },
  agents: {
    defaults: {
      model: { primary: "openai/gpt-5.5" },
    },
  },
}
```

### Other Subscription-Style Hosted Options

The source page surfaces three additional subscription-style hosted options as cards: **Z.AI (GLM)** (Coding Plan or general API endpoints), **MiniMax** (Coding Plan OAuth or API key access), and **Qwen Cloud** (Qwen Cloud provider surface plus Alibaba DashScope and Coding Plan endpoint mapping).

### OpenCode

Auth `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`); Zen runtime provider `opencode`, Go runtime provider `opencode-go`. Example models: `opencode/claude-opus-4-6`, `opencode-go/kimi-k2.6`. CLI: `openclaw onboard --auth-choice opencode-zen` or `--auth-choice opencode-go`.

```json5
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

### Google Gemini (API key)

Provider `google`; auth `GEMINI_API_KEY`; optional rotation `GEMINI_API_KEYS`, `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, `GOOGLE_API_KEY` fallback, and `OPENCLAW_LIVE_GEMINI_KEY` (single override). Example models: `google/gemini-3.1-pro-preview`, `google/gemini-3-flash-preview`. Compatibility: legacy `google/gemini-3.1-flash-preview` normalizes to `google/gemini-3-flash-preview`; alias `google/gemini-3.1-pro` normalizes to the live id `google/gemini-3.1-pro-preview`. CLI: `openclaw onboard --auth-choice gemini-api-key`. Thinking: `/think adaptive` uses Google dynamic thinking — Gemini 3/3.1 omit a fixed `thinkingLevel`, Gemini 2.5 sends `thinkingBudget: -1`. Direct Gemini runs accept `params.cachedContent` (or legacy `cached_content`) to forward a provider-native `cachedContents/...` handle; cache hits surface as OpenClaw `cacheRead`.

Providers `google-vertex` and `google-gemini-cli`; Vertex auth uses gcloud ADC, Gemini CLI uses its OAuth flow. The source **warns** that Gemini CLI OAuth in OpenClaw is an **unofficial integration** (some users reported Google account restrictions after using third-party clients; review Google terms and use a non-critical account). Gemini CLI OAuth ships in the bundled `google` plugin. Setup steps: install Gemini CLI (`brew install gemini-cli` or `npm install -g @google/gemini-cli`); enable the plugin (`openclaw plugins enable google`); log in (`openclaw models auth login --provider google-gemini-cli --set-default`, default model `google-gemini-cli/gemini-3-flash-preview` — no client id/secret goes in `openclaw.json`, the CLI login flow stores tokens in auth profiles on the gateway host); and, if requests fail after login, set `GOOGLE_CLOUD_PROJECT` or `GOOGLE_CLOUD_PROJECT_ID` on the gateway host. Gemini CLI uses `stream-json` by default; OpenClaw normalizes `stats.cached` into `cacheRead`, while legacy `--output-format json` overrides still read reply text from `response`.

```bash
openclaw plugins enable google
openclaw models auth login --provider google-gemini-cli --set-default
```

### Z.AI (GLM)

Provider `zai`; auth `ZAI_API_KEY`; example model `zai/glm-5.2`; CLI `openclaw onboard --auth-choice zai-api-key`. Model refs use the canonical `zai/*` id. The `zai-api-key` choice auto-detects the matching endpoint, while `zai-coding-global`, `zai-coding-cn`, `zai-global`, and `zai-cn` force a specific surface.

### Vercel AI Gateway

Provider `vercel-ai-gateway`; auth `AI_GATEWAY_API_KEY`. Example models: `vercel-ai-gateway/anthropic/claude-opus-4.6`, `vercel-ai-gateway/moonshotai/kimi-k2.6`. CLI: `--auth-choice ai-gateway-api-key`.

### Other Bundled Provider Plugins

| Provider | Id | Auth env | Example model |
|---|---|---|---|
| BytePlus | `byteplus` / `byteplus-plan` | `BYTEPLUS_API_KEY` | `byteplus-plan/ark-code-latest` |
| Cohere | `cohere` | `COHERE_API_KEY` | `cohere/command-a-03-2025` |
| GitHub Copilot | `github-copilot` | `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN` | - |
| Hugging Face Inference | `huggingface` | `HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN` | `huggingface/deepseek-ai/DeepSeek-R1` |
| MiniMax | `minimax` / `minimax-portal` | `MINIMAX_API_KEY` / `MINIMAX_OAUTH_TOKEN` | `minimax/MiniMax-M3` |
| Mistral | `mistral` | `MISTRAL_API_KEY` | `mistral/mistral-large-latest` |
| Moonshot | `moonshot` | `MOONSHOT_API_KEY` | `moonshot/kimi-k2.6` |
| NVIDIA | `nvidia` | `NVIDIA_API_KEY` | `nvidia/nvidia/nemotron-3-ultra-550b-a55b` |
| NovitaAI | `novita` | `NOVITA_API_KEY` | `novita/deepseek/deepseek-v3-0324` |
| Ollama Cloud | `ollama-cloud` | `OLLAMA_API_KEY` | `ollama-cloud/kimi-k2.6` |
| OpenRouter | `openrouter` | OpenRouter OAuth or `OPENROUTER_API_KEY` | `openrouter/auto` |
| Qwen OAuth | `qwen-oauth` | `QWEN_API_KEY` | `qwen-oauth/qwen3.5-plus` |
| Together | `together` | `TOGETHER_API_KEY` | `together/meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| Venice | `venice` | `VENICE_API_KEY` | - |
| Vercel AI Gateway | `vercel-ai-gateway` | `AI_GATEWAY_API_KEY` | `vercel-ai-gateway/anthropic/claude-opus-4.6` |
| Volcano Engine (Doubao) | `volcengine` / `volcengine-plan` | `VOLCANO_ENGINE_API_KEY` | `volcengine-plan/ark-code-latest` |
| xAI | `xai` | SuperGrok/X Premium OAuth or `XAI_API_KEY` | `xai/grok-4.3` |
| Xiaomi | `xiaomi` / `xiaomi-token-plan` | `XIAOMI_API_KEY` / `XIAOMI_TOKEN_PLAN_API_KEY` | `xiaomi/mimo-v2-flash` / `xiaomi-token-plan/mimo-v2.5-pro` |

**Quirks worth knowing** (from the source page's accordions):

- **OpenRouter** — applies app-attribution headers and Anthropic `cache_control` markers only on verified `openrouter.ai` routes. DeepSeek/Moonshot/ZAI refs are cache-TTL eligible for OpenRouter-managed prompt caching but get no Anthropic cache markers. As a proxy-style OpenAI-compatible path it skips native-OpenAI-only shaping (`serviceTier`, Responses `store`, prompt-cache hints, reasoning-compat); Gemini-backed refs keep proxy-Gemini thought-signature sanitation only.
- **Kilo Gateway** — Gemini-backed refs follow the same proxy-Gemini sanitation; `kilocode/kilo/auto` and other proxy-reasoning-unsupported refs skip proxy reasoning injection.
- **MiniMax** — API-key onboarding writes explicit M3 and M2.7 chat model definitions; image understanding stays on the plugin-owned `MiniMax-VL-01` media provider.
- **NVIDIA** — model ids use a `nvidia/<vendor>/<model>` namespace (e.g. `nvidia/nvidia/nemotron-...`, `nvidia/moonshotai/kimi-k2.5`); pickers preserve the literal composition while the canonical API key stays single-prefixed.
- **xAI** — uses the xAI Responses path; recommended auth is SuperGrok/X Premium OAuth, API keys work via `XAI_API_KEY`, and Grok `web_search` reuses the same auth profile before API-key fallback. `grok-4.3` is the bundled default and `grok-build-0.1` is selectable for build/coding work. `/fast` or `params.fastMode: true` rewrites `grok-3`, `grok-3-mini`, `grok-4`, and `grok-4-0709` to their `*-fast` variants. `tool_stream` defaults on; disable via `params.tool_stream=false`.

## CLI Examples

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-6
openclaw models list
```

**Source**: OpenClaw documentation — `concepts/model-providers` (mirror `inbox/openclaw_docs/concepts/model-providers.md`)
**Last Updated**: 2026-06-22
**Status**: Active
