---
tags:
  - resource
  - documentation
  - hermes_agent
  - inference_providers
  - routing
keywords:
  - provider routing
  - litellm proxy
  - openrouter routing
  - fallback providers
  - context length detection
  - named custom providers
topics:
  - Hermes Agent
  - Inference Providers
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/integrations/providers
access_control_group: ["general"]
---

# Hermes Agent — Provider Routing & Proxies

## Overview

This is the routing/proxy layer of Hermes Agent's provider setup: how you put a multi-provider gateway in front of Hermes, point at other OpenAI-compatible endpoints, resolve a model's context window, name and tune multiple custom providers, and chain backup providers when the primary fails. It is the third slice of the `providers.md` page (after the cloud catalog and the local/self-hosted servers) and covers LiteLLM/ClawRouter proxies, the "Other Compatible Providers" table, the 9-source context-length resolution chain, `custom_providers[]` with `extra_body`/`api_mode`/`supports_vision`, the Together/Groq/Perplexity cookbook, OpenRouter `provider_routing` + the Pareto Code router, and the `fallback_providers[]` chain. The deep *feature internals* of provider-routing and fallback live elsewhere — this note is the config-side procedure; link-outs point at the owning feature pages.

## LiteLLM Proxy — Multi-Provider Gateway

[LiteLLM](https://docs.litellm.ai/) is an OpenAI-compatible proxy that unifies 100+ LLM providers behind a single API. Best for: switching between providers without config changes, load balancing, fallback chains, budget controls. Install and start it, then point Hermes at it with `hermes model` → Custom endpoint → `http://localhost:4000/v1`.

```yaml
model_list:
  - model_name: "best"
    litellm_params:
      model: anthropic/claude-sonnet-4
      api_key: sk-ant-...
  - model_name: "best"
    litellm_params:
      model: openai/gpt-4o
      api_key: sk-...
router_settings:
  routing_strategy: "latency-based-routing"
```

The two entries share the model name `best`, so LiteLLM load-balances and falls back across the Anthropic and OpenAI backends; `routing_strategy: "latency-based-routing"` picks the lowest-latency backend per request.

## ClawRouter — Cost-Optimized Routing

[ClawRouter](https://github.com/BlockRunAI/ClawRouter) by BlockRunAI is a local routing proxy that auto-selects models based on query complexity. It classifies requests across 14 dimensions and routes to the cheapest model that can handle the task. Payment is via USDC cryptocurrency (no API keys). Start it with `npx @blockrun/clawrouter` (port 8402), then configure Hermes with `hermes model` → Custom endpoint → `http://localhost:8402/v1` → model name `blockrun/auto`. Routing profiles trade quality for savings: `blockrun/auto` (balanced, 74-100%), `blockrun/eco` (cheapest, 95-100%), `blockrun/premium` (best quality, 0%), `blockrun/free` (free models, 100%), `blockrun/agentic` (tool-use optimized, varies). ClawRouter requires a USDC-funded wallet on Base or Solana, all requests route through BlockRun's backend API, and `npx @blockrun/clawrouter doctor` checks wallet status.

## Other Compatible Providers

Any service with an OpenAI-compatible API works. Popular options include Together AI (`https://api.together.xyz/v1`), Groq (`https://api.groq.com/openai/v1`, ultra-fast), DeepSeek (`https://api.deepseek.com/v1`), Fireworks AI (`https://api.fireworks.ai/inference/v1`), GMI Cloud (`https://api.gmi-serving.com/v1`), Cerebras (`https://api.cerebras.ai/v1`, wafer-scale), Mistral AI (`https://api.mistral.ai/v1`), OpenAI (`https://api.openai.com/v1`), Azure OpenAI (`https://YOUR.openai.azure.com/`), LocalAI (`http://localhost:8080/v1`), and Jan (`http://localhost:1337/v1`). Configure any of these with `hermes model` → Custom endpoint, or in `config.yaml` by setting `model.provider: custom`, `model.base_url` to the table's URL, `model.default` to the model ID, and `model.api_key` to the provider key (e.g. `base_url: https://api.together.xyz/v1` with `default: meta-llama/Llama-3.1-70B-Instruct-Turbo`). The Cookbook section below shows the same providers wired as named `custom_providers[]` entries.

## Context Length Detection

`context_length` is the **total context window** — the combined budget for input *and* output tokens (e.g. 200,000 for Claude Opus 4.6); Hermes uses it to decide when to compress history and to validate API requests. It is distinct from `model.max_tokens`, the **output cap** (max tokens generated in a single response — Anthropic's native API renamed it `max_output_tokens` for clarity). Hermes resolves the correct context window through a multi-source chain (highest priority first):

1. **Config override** — `model.context_length` in config.yaml
2. **Custom provider per-model** — `custom_providers[].models.<id>.context_length`
3. **Persistent cache** — previously discovered values (survives restarts)
4. **Endpoint `/models`** — queries your server's API (local/custom endpoints)
5. **Anthropic `/v1/models`** — `max_input_tokens` (API-key users only)
6. **OpenRouter API** — live model metadata
7. **Nous Portal** — suffix-matches Nous model IDs against OpenRouter metadata
8. **[models.dev](https://models.dev)** — community registry, 3800+ models across 100+ providers
9. **Fallback defaults** — broad model-family patterns (128K default)

The system is provider-aware — the same model can have different limits depending on who serves it (e.g. `claude-opus-4.6` is 1M on Anthropic direct but 128K on GitHub Copilot). Set `model.context_length` (or, per model under a custom endpoint, `custom_providers[].models.<id>.context_length`) when auto-detection gets it wrong — e.g. `custom_providers: - name: "My Local LLM"` with `base_url: "http://localhost:11434/v1"` and `models: { qwen3.5:27b: { context_length: 64000 } }`. `hermes model` prompts for context length when configuring a custom endpoint; leave it blank for auto-detection. Set it manually when using Ollama with a custom `num_ctx` below the model's maximum, when limiting context below the maximum to save VRAM, or when running behind a proxy that doesn't expose `/v1/models`.

## Named Custom Providers

If you work with multiple custom endpoints (e.g. a local dev server and a remote GPU server), define them as named custom providers in `config.yaml`. Each entry sets `base_url`, an optional `key_env`, and an `api_mode` (`chat_completions` or `anthropic_messages` for Anthropic-compatible proxies):

```yaml
custom_providers:
  - name: local
    base_url: http://localhost:8080/v1
    # api_key omitted — Hermes uses "no-key-required" for keyless local servers
  - name: work
    base_url: https://gpu-server.internal.corp/v1
    key_env: CORP_API_KEY
    api_mode: chat_completions   # set explicitly by `hermes model` → Custom Endpoint wizard; auto-detection still happens as a fallback
  - name: anthropic-proxy
    base_url: https://proxy.example.com/anthropic
    key_env: ANTHROPIC_PROXY_KEY
    api_mode: anthropic_messages  # for Anthropic-compatible proxies
```

Some OpenAI-compatible endpoints need provider-specific request body fields. Add an `extra_body` map to the matching custom provider and Hermes merges it into each chat-completions request for that endpoint (e.g. `enable_thinking: true`, `reasoning_effort: high`); vLLM Gemma and some NVIDIA NIM endpoints expect `enable_thinking` nested under `chat_template_kwargs` instead. The `hermes model` → Custom Endpoint wizard now prompts for `api_mode` explicitly and persists the answer; URL-based auto-detection (e.g. `/anthropic` paths → `anthropic_messages`) still happens as a fallback when the field is blank.

For a vision-capable model that isn't in models.dev, set `model.supports_vision: true` so Hermes routes attached images natively (as `image_url` parts) instead of pre-processing them through `vision_analyze` — a single knob, no need to also set `agent.image_input_mode: native`. The same key is honored on per-named-provider models (`custom_providers[*].models[*].supports_vision`) and accepts standard YAML booleans (`true/false/yes/no/on/off/1/0`). Switch between named providers mid-session with the triple syntax `/model custom:<name>:<model>` (e.g. `/model custom:local:qwen-2.5`, `/model custom:work:llama3-70b`), or select them from the interactive `hermes model` menu.

## Cookbook: Together AI, Groq, Perplexity

The cloud providers in Other Compatible Providers all speak OpenAI's REST dialect, so they wire up the same way under `custom_providers:` — each drops into `~/.hermes/config.yaml` with the matching API key in `~/.hermes/.env`. Together AI hosts open-weight models below first-party prices (`/v1/models` works so `hermes model` can auto-discover); Groq is ultra-fast (~500 tok/s on Llama-3.3-70B) with a small catalog; Perplexity does live web search + citation but is strict about which models are available. The three recipes compose — define all of them and switch per turn with `/model custom:<name>:<model>`:

```yaml
custom_providers:
  - name: together
    base_url: https://api.together.xyz/v1
    key_env: TOGETHER_API_KEY
  - name: groq
    base_url: https://api.groq.com/openai/v1
    key_env: GROQ_API_KEY
  - name: perplexity
    base_url: https://api.perplexity.ai
    key_env: PERPLEXITY_API_KEY

model:
  default: MiniMaxAI/MiniMax-M2.7
  provider: custom:together      # boot to Together; switch freely after
```

Troubleshooting: `hermes doctor` should print no `Unknown provider` warnings for these names; if a provider's `/v1/models` endpoint is unreachable (Perplexity is the common one), `hermes model` persists the model with a warning rather than hard-rejecting.

## Choosing the Right Setup

The page closes the provider catalog with a use-case → recommendation matrix: "just want it to work" → OpenRouter (default) or Nous Portal; local models, easy setup → Ollama; production GPU serving → vLLM or SGLang; Mac / no GPU → Ollama or llama.cpp; **multi-provider routing → LiteLLM Proxy or OpenRouter**; **cost optimization → ClawRouter or OpenRouter with `sort: "price"`**; maximum privacy → Ollama/vLLM/llama.cpp (fully local); enterprise/Azure → Azure OpenAI custom endpoint; Chinese AI models → z.ai (GLM), Kimi/Moonshot, MiniMax, Xiaomi MiMo, or Tencent TokenHub. You can switch providers at any time with `hermes model` — no restart required, and conversation history, memory, and skills carry over.

## Optional API Keys

Beyond inference providers, several feature backends take an optional API key (set in `~/.hermes/.env`): Firecrawl web scraping (`FIRECRAWL_API_KEY`, `FIRECRAWL_API_URL`), Browserbase browser automation (`BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`), FAL image generation (`FAL_KEY`), ElevenLabs premium TTS (`ELEVENLABS_API_KEY`), OpenAI TTS + transcription (`VOICE_TOOLS_OPENAI_KEY`), Mistral TTS + transcription (`MISTRAL_API_KEY`), Honcho cross-session user modeling (`HONCHO_API_KEY`), and Supermemory semantic long-term memory (`SUPERMEMORY_API_KEY`). Firecrawl can be self-hosted (Docker stack of 5 containers: API, Playwright, Redis, RabbitMQ, PostgreSQL) and pointed at via `hermes config set FIRECRAWL_API_URL http://localhost:3002` — no API key required, no rate limits, but it loses Fire-engine anti-bot bypassing and uses DuckDuckGo instead of Google. (Web-search/scraping feature details → SP08.)

## OpenRouter Provider Routing

When using OpenRouter, you can control how requests are routed across providers by adding a `provider_routing` section to `~/.hermes/config.yaml`:

```yaml
provider_routing:
  sort: "throughput"          # "price" (default), "throughput", or "latency"
  # only: ["anthropic"]      # Only use these providers
  # ignore: ["deepinfra"]    # Skip these providers
  # order: ["anthropic", "google"]  # Try providers in this order
  # require_parameters: true  # Only use providers that support all request params
  # data_collection: "deny"   # Exclude providers that may store/train on data
```

As a shortcut, append `:nitro` to any model name for throughput sorting (e.g. `anthropic/claude-sonnet-4:nitro`), or `:floor` for price sorting.

## OpenRouter Pareto Code Router

OpenRouter ships an experimental coding-model router at `openrouter/pareto-code` that auto-routes requests to the cheapest model meeting a coding-quality bar (ranked by [Artificial Analysis](https://artificialanalysis.ai/)). Pick this model and tune the `min_coding_score` knob:

```yaml
model:
  provider: openrouter
  model: openrouter/pareto-code

openrouter:
  min_coding_score: 0.65   # 0.0–1.0; higher = stronger (more expensive) coders. Default 0.65.
```

`min_coding_score` is **only** sent when `model.model` is `openrouter/pareto-code` (a no-op on any other model); set it to empty string (or remove the line) to let OpenRouter pick the strongest available coder. Selection is deterministic per score on a given day, but the chosen model can shift as the Pareto frontier moves. To use the Pareto Code router for a specific **auxiliary task** (compression, vision, etc.) instead of the main agent, set `extra_body.plugins` under that task (per-task auxiliary routing → SP02/SP18 config docs).

## Fallback Providers

Configure a chain of backup providers Hermes tries in order when the primary model fails (rate limits, server errors, auth failures). The canonical format is a top-level `fallback_providers:` list:

```yaml
fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
  - provider: anthropic
    model: claude-sonnet-4
    # base_url: http://localhost:8000/v1    # optional, for custom endpoints
    # api_mode: chat_completions           # optional override
```

The legacy single-pair `fallback_model:` dict is still accepted for back-compat. When activated, the fallback swaps the model and provider mid-session without losing your conversation; the chain is tried entry-by-entry and activation is one-shot per session. Supported providers cover the full catalog (`openrouter`, `nous`, `novita`, `openai-codex`, `copilot`, `copilot-acp`, `anthropic`, `gemini`, `google-gemini-cli`, `qwen-oauth`, `huggingface`, `zai`, the `kimi-*`/`minimax-*` families, `deepseek`, `nvidia`, `xai`, `xai-oauth`, `ollama-cloud`, `bedrock`, `azure-foundry`, `opencode-*`, `kilocode`, `xiaomi`, `arcee`, `gmi`, `stepfun`, `lmstudio`, `alibaba`, `alibaba-coding-plan`, `tencent-tokenhub`, and `custom`). Fallback is configured exclusively through `config.yaml` or interactively via `hermes fallback`; the *feature internals* — when it triggers, how the chain advances, and how it interacts with auxiliary tasks and delegation — live on the Fallback Providers feature page (→ SP09 link-out).

**Source**: `inbox/hermes_agent_docs/integrations/providers.md` · https://hermes-agent.nousresearch.com/docs/integrations/providers
**Last Updated**: 2026-06-19
**Status**: Active
