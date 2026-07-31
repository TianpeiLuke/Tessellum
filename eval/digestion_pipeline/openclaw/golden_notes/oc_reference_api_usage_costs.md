---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - api_costs
keywords:
  - openclaw api usage costs
  - features that can spend keys
  - how keys are discovered
  - status usage cost reporting
  - estimated cost active model
  - provider usage windows quotas
  - memorySearch embedding providers
  - web_search web_fetch api keys
  - elevenlabs talk spend
topics:
  - OpenClaw
  - API Usage and Costs
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/reference/api-usage-costs
access_control_group: ["general"]
---

# OpenClaw — API Usage and Costs Audit

## Overview

This note is a concept audit of every OpenClaw feature that can invoke paid API keys and where each feature's cost surfaces, mirroring the `reference/api-usage-costs` source page. It covers where costs show up (the `/status` per-session snapshot, the `/usage` per-message footer, and CLI provider usage windows), how OpenClaw discovers credentials (auth profiles, environment variables, config, and skills), and the ten spend surfaces enumerated in the source — core model responses, media understanding, image/video generation, memory embeddings, web search, web fetch, provider usage snapshots, compaction summarization, model scan, talk, and skills. The page is a cost/key map: it does not redefine provider/model config (see Models) or token-use display detail (see Token use & costs) — it points back to those pages, and this note links them rather than duplicating them.

## Where Costs Show Up (chat + CLI)

OpenClaw surfaces cost in three places — a per-session snapshot, a per-message footer, and CLI provider usage windows.

**Per-session cost snapshot.** `/status` shows the current session model, context usage, and last response tokens. When OpenClaw has usage metadata and local pricing for the active model, `/status` also shows **estimated cost** for the last reply; this can include explicitly priced non-API-key providers such as Bedrock `aws-sdk` models. If live session metadata is sparse, `/status` can recover token/cache counters and the active runtime model label from the latest transcript usage entry — existing nonzero live values still take precedence, and prompt-sized transcript totals can win when stored totals are missing or smaller.

**Per-message cost footer.** `/usage full` appends a usage footer to every reply, including **estimated cost** when local pricing is configured for the active model and usage metadata is available. `/usage tokens` shows tokens only; subscription-style OAuth/token and CLI flows still show tokens only unless that runtime supplies compatible usage metadata and an explicit local price is configured. Gemini CLI note: the default `stream-json` output and legacy JSON overrides both read usage from `stats`, normalize `stats.cached` into `cacheRead`, and derive input tokens from `stats.input_tokens - stats.cached` when needed.

**Anthropic note.** Anthropic staff told the project that OpenClaw-style Claude CLI usage is allowed again, so OpenClaw treats Claude CLI reuse and `claude -p` usage as sanctioned for this integration unless Anthropic publishes a new policy. Anthropic still does not expose a per-message dollar estimate that OpenClaw can show in `/usage full`.

**CLI usage windows (provider quotas).** `openclaw status --usage` and `openclaw channels list` show provider **usage windows** (quota snapshots, not per-message costs), with human output normalized to `X% left` across providers. The current usage-window providers are Anthropic, GitHub Copilot, Gemini CLI, OpenAI Codex, MiniMax, Xiaomi, and z.ai. MiniMax note: its raw `usage_percent` / `usagePercent` fields mean *remaining* quota, so OpenClaw inverts them before display; count-based fields still win when present, and if the provider returns `model_remains`, OpenClaw prefers the chat-model entry, derives the window label from timestamps when needed, and includes the model name in the plan label. Usage auth for those quota windows comes from provider-specific hooks when available; otherwise OpenClaw falls back to matching OAuth/API-key credentials from auth profiles, env, or config.

## How Keys Are Discovered

OpenClaw can pick up credentials from four sources:

- **Auth profiles** — per-agent, stored in `auth-profiles.json`.
- **Environment variables** — e.g. `OPENAI_API_KEY`, `BRAVE_API_KEY`, `FIRECRAWL_API_KEY`.
- **Config** — `models.providers.*.apiKey`, `plugins.entries.*.config.webSearch.apiKey`, `plugins.entries.firecrawl.config.webFetch.apiKey`, `memorySearch.*`, `talk.providers.*.apiKey`.
- **Skills** — `skills.entries.<name>.apiKey`, which may export keys to the skill process env.

## Features That Can Spend Keys

The source enumerates the spend surfaces below. (Source numbering reuses `5)` for both Web search and Web fetch; both are reproduced as the source labels them, so this audit lists eleven labeled subsections across ten conceptual surfaces.)

### 1) Core model responses (chat + tools)

Every reply or tool call uses the **current model provider** (OpenAI, Anthropic, etc.). This is the primary source of usage and cost. It also includes subscription-style hosted providers that still bill outside OpenClaw's local UI, such as **OpenAI Codex**, **Alibaba Cloud Model Studio Coding Plan**, **MiniMax Coding Plan**, **Z.AI / GLM Coding Plan**, and Anthropic's OpenClaw Claude-login path with **Extra Usage** enabled. See Models for pricing config and Token use & costs for display.

### 2) Media understanding (audio/image/video)

Inbound media can be summarized/transcribed before the reply runs, using model/provider APIs. Providers per modality: Audio — OpenAI / Groq / Deepgram / DeepInfra / Google / Mistral; Image — OpenAI / OpenRouter / Anthropic / DeepInfra / Google / MiniMax / Moonshot / Qwen / Z.AI; Video — Google / Qwen / Moonshot.

### 3) Image and video generation

Shared generation capabilities can also spend provider keys. Image generation: OpenAI / Google / DeepInfra / fal / MiniMax. Video generation: DeepInfra / Qwen. Image generation can infer an auth-backed provider default when `agents.defaults.imageGenerationModel` is unset. Video generation currently requires an explicit `agents.defaults.videoGenerationModel` such as `qwen/wan2.6-t2v`.

### 4) Memory embeddings + semantic search

Semantic memory search uses **embedding APIs** when configured for remote providers, selected via `memorySearch.provider`:

- `memorySearch.provider = "openai"` → OpenAI embeddings
- `memorySearch.provider = "gemini"` → Gemini embeddings
- `memorySearch.provider = "voyage"` → Voyage embeddings
- `memorySearch.provider = "mistral"` → Mistral embeddings
- `memorySearch.provider = "deepinfra"` → DeepInfra embeddings
- `memorySearch.provider = "lmstudio"` → LM Studio embeddings (local/self-hosted)
- `memorySearch.provider = "ollama"` → Ollama embeddings (local/self-hosted; typically no hosted API billing)
- Optional fallback to a remote provider if local embeddings fail

You can keep it local with `memorySearch.provider = "local"` (no API usage).

### 5) Web search tool

`web_search` may incur usage charges depending on the provider; each provider resolves its key from an env var and/or a `plugins.entries.*.config.webSearch.*` config path:

- **Brave Search API**: `BRAVE_API_KEY` or `plugins.entries.brave.config.webSearch.apiKey`
- **Exa**: `EXA_API_KEY` or `plugins.entries.exa.config.webSearch.apiKey`
- **Firecrawl**: `FIRECRAWL_API_KEY` or `plugins.entries.firecrawl.config.webSearch.apiKey`
- **Gemini (Google Search)**: `GEMINI_API_KEY` or `plugins.entries.google.config.webSearch.apiKey`
- **Grok (xAI)**: xAI OAuth profile, `XAI_API_KEY`, or `plugins.entries.xai.config.webSearch.apiKey`
- **Kimi (Moonshot)**: `KIMI_API_KEY`, `MOONSHOT_API_KEY`, or `plugins.entries.moonshot.config.webSearch.apiKey`
- **MiniMax Search**: `MINIMAX_CODE_PLAN_KEY`, `MINIMAX_CODING_API_KEY`, `MINIMAX_API_KEY`, or `plugins.entries.minimax.config.webSearch.apiKey`
- **Ollama Web Search**: key-free for a reachable signed-in local Ollama host; direct `https://ollama.com` search uses `OLLAMA_API_KEY`, and auth-protected hosts can reuse normal Ollama provider bearer auth
- **Perplexity Search API**: `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, or `plugins.entries.perplexity.config.webSearch.apiKey`
- **Tavily**: `TAVILY_API_KEY` or `plugins.entries.tavily.config.webSearch.apiKey`
- **DuckDuckGo**: key-free provider when explicitly selected (no API billing, but unofficial and HTML-based)
- **SearXNG**: `SEARXNG_BASE_URL` or `plugins.entries.searxng.config.webSearch.baseUrl` (key-free/self-hosted; no hosted API billing)

Legacy `tools.web.search.*` provider paths still load through the temporary compatibility shim, but they are no longer the recommended config surface. **Brave Search free credit:** each Brave plan includes $5/month in renewing free credit; the Search plan costs $5 per 1,000 requests, so the credit covers 1,000 requests/month at no charge — set a usage limit in the Brave dashboard to avoid unexpected charges. See Web tools.

### 5) Web fetch tool (Firecrawl)

`web_fetch` can call **Firecrawl** with keyless starter access; add an API key for higher limits via `FIRECRAWL_API_KEY` or `plugins.entries.firecrawl.config.webFetch.apiKey`. If Firecrawl isn't configured, the tool falls back to direct fetch plus the bundled `web-readability` plugin (no paid API); disable `plugins.entries.web-readability.enabled` to skip local Readability extraction.

### 6) Provider usage snapshots (status/health)

Some status commands call **provider usage endpoints** to display quota windows or auth health. These are typically low-volume calls but still hit provider APIs: `openclaw status --usage` and `openclaw models status --json`. See Models CLI.

### 7) Compaction safeguard summarization

The compaction safeguard can summarize session history using the **current model**, which invokes provider APIs when it runs. See Session management + compaction.

### 8) Model scan / probe

`openclaw models scan` can probe OpenRouter models and uses `OPENROUTER_API_KEY` when probing is enabled. See Models CLI.

### 9) Talk (speech)

Talk mode can invoke **ElevenLabs** when configured, via `ELEVENLABS_API_KEY` or `talk.providers.elevenlabs.apiKey`. See Talk mode.

### 10) Skills (third-party APIs)

Skills can store `apiKey` in `skills.entries.<name>.apiKey`. If a skill uses that key for external APIs, it can incur costs according to the skill's provider. See Skills.

**Source**: OpenClaw documentation — `reference/api-usage-costs` (mirror `inbox/openclaw_docs/reference/api-usage-costs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
