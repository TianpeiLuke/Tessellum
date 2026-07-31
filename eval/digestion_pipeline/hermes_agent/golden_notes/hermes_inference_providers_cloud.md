---
tags:
  - resource
  - documentation
  - hermes_agent
  - inference_providers
  - cloud_apis
keywords:
  - cloud inference providers
  - first-class api-key providers
  - oauth providers
  - hermes model command
  - aws bedrock converse api
  - provider base url override
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

# Hermes Agent — Cloud & First-Class Inference Providers

## Overview

This note is the **cloud and first-class API-key provider catalog** for Hermes Agent — the half of the AI Providers page that covers managed, hosted LLM endpoints you reach with an OAuth login or an API key (as opposed to self-hosted servers, which live in [Local & Self-Hosted LLM Providers](hermes_local_self_hosted_llm.md), and routing/proxy layers, which live in [Provider Routing & Proxies](hermes_provider_routing_proxies.md)). You need at least one provider configured to use Hermes. The page is organized by **auth mode** — subscription OAuth (Nous Portal, Anthropic, Copilot, Qwen/MiniMax/Gemini/xAI OAuth), API-key-in-`.env` (the first-class providers), and the AWS credential chain (Bedrock) — and each catalog row maps to a registered provider plugin with a stable provider ID, optional aliases, and a base-URL override env var. Per-provider deep setup walkthroughs are routed to the SP15 guides; this note curates the catalog and the auth-mode mechanics.

## Inference Providers Catalog

You need at least one way to connect to an LLM. Use `hermes model` to switch providers and models interactively, or configure directly. The page ships a single catalog table mapping each provider to its setup mechanism. Rather than reproduce all ~35 rows verbatim, the catalog organizes into three auth classes:

- **OAuth / subscription (no API key):** Nous Portal (`hermes model`, OAuth, subscription), OpenAI Codex (ChatGPT OAuth, Codex models), GitHub Copilot (OAuth device-code or `COPILOT_GITHUB_TOKEN`/`GH_TOKEN`/`gh auth token`), GitHub Copilot ACP (spawns local `copilot --acp --stdio`), Anthropic (Claude Max + extra usage credits via OAuth), xAI Grok OAuth (SuperGrok/Premium+), Qwen OAuth (`qwen-oauth`, browser PKCE), MiniMax OAuth (`minimax-oauth`, browser PKCE), Google Gemini OAuth (`google-gemini-cli`, free tier, browser PKCE), Azure AI Foundry, Ollama Cloud.
- **API-key in `~/.hermes/.env`:** OpenRouter (`OPENROUTER_API_KEY`), NovitaAI (`novita`), z.ai/GLM (`zai`), Kimi/Moonshot (`kimi-coding`, `kimi-coding-cn`), Arcee AI (`arcee`), GMI Cloud (`gmi`), MiniMax (`minimax`, `minimax-cn`), xAI Grok Responses API (`xai`), Qwen Cloud/DashScope (`alibaba`), Alibaba Coding Plan (`alibaba-coding-plan`), Kilo Code, Xiaomi MiMo (`xiaomi`), Tencent TokenHub (`tencent-tokenhub`), OpenCode Zen/Go, DeepSeek, Hugging Face (`huggingface`/`hf`), Google/Gemini (`gemini`), OpenAI API direct (`openai-api`), NVIDIA Build (`nvidia`), StepFun (`stepfun`), LM Studio (`lmstudio`).
- **AWS credential chain (no API key):** AWS Bedrock (`bedrock`, standard AWS credentials via boto3).

A model-key alias applies across the table: in the `model:` config section either `default:` or `model:` works as the key name (`model: { default: my-model }` and `model: { model: my-model }` are identical).

## Two Commands for Model Management

Hermes has **two** model commands that serve different purposes:

| Command | Where to run | What it does |
|---------|-------------|--------------|
| **`hermes model`** | Your terminal (outside any session) | Full setup wizard — add providers, run OAuth, enter API keys, configure endpoints |
| **`/model`** | Inside a Hermes chat session | Quick switch between **already-configured** providers and models |

If you're trying to switch to a provider you haven't set up yet (e.g. you only have OpenRouter configured and want to use Anthropic), you need `hermes model`, not `/model`. Exit your session first (`Ctrl+C` or `/quit`), run `hermes model`, complete the provider setup, then start a new session.

## Nous Portal (Recommended)

Nous Portal is Nous Research's unified subscription gateway and **the recommended way to run Hermes Agent**. One OAuth login covers 300+ frontier agentic models plus the Tool Gateway (web search, image generation, TTS, browser automation) plus Nous Chat — billed against your Nous subscription instead of separate per-provider accounts.

```bash
hermes setup --portal     # fresh install — OAuth + provider + gateway in one command
hermes model              # existing install — pick "Nous Portal" from the list
hermes portal info        # inspect login + routing at any time
```

Every Portal request carries a `client=hermes-client-v<version>` tag (e.g. `client=hermes-client-v0.13.0`) auto-aligned to your installed release, so Portal-side telemetry can distinguish Hermes traffic. Hermes prefers scoped `inference:invoke` JWTs for Portal requests, with the legacy opaque session-key path as a fallback; credentials are managed by the OAuth flow and rotate transparently, and revoked refresh tokens are quarantined to avoid replay loops. **For full Portal details (subscription contents, model catalog, token handling, troubleshooting) see [Nous Portal Subscription](hermes_nous_portal_subscription.md).**

> Auxiliary-model note (from source): even when using Nous Portal, Codex, or a custom endpoint, some tools (vision, web summarization, MoA) use a separate "auxiliary" model; by default (`auxiliary.*.provider: "auto"`) Hermes routes these to your main chat model, overridable per task.

## Anthropic (Native)

Use Claude models directly through the Anthropic API — no OpenRouter proxy needed. Supports three auth methods: Anthropic OAuth via `hermes model` (routes as Claude Code against your account — **requires a Claude Max plan with purchased extra-usage credits**; Pro subscribers cannot use this path), an `ANTHROPIC_API_KEY` (pay-per-token, standard API pricing), and a manual setup-token (`ANTHROPIC_TOKEN`, fallback/legacy).

```bash
# With an API key (pay-per-token)
export ANTHROPIC_API_KEY=***
hermes chat --provider anthropic --model claude-sonnet-4-6

# Preferred: authenticate through `hermes model`
# Hermes will use Claude Code's credential store directly when available
hermes model

# Manual override with a setup-token (fallback / legacy)
export ANTHROPIC_TOKEN=***  # setup-token or manual OAuth token
hermes chat --provider anthropic

# Auto-detect Claude Code credentials (if you already use Claude Code)
hermes chat --provider anthropic  # reads Claude Code credential files automatically
```

When you choose Anthropic OAuth through `hermes model`, Hermes prefers Claude Code's own credential store over copying the token into `~/.hermes/.env`, keeping refreshable Claude credentials refreshable. Permanent config sets `model.provider: "anthropic"` with `model.default: "claude-sonnet-4-6"`. `--provider claude` and `--provider claude-code` are shorthand for `--provider anthropic`.

## GitHub Copilot

Hermes supports GitHub Copilot as a first-class provider with two modes: `copilot` (direct Copilot API, recommended — uses your subscription to reach GPT-5.x, Claude, Gemini, etc.) and `copilot-acp` (spawns the local Copilot CLI as a subprocess, requires the Copilot CLI in PATH and an existing `copilot login`). Authentication for `copilot` is checked in order: `COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN` → `gh auth token` CLI fallback; if no token is found, `hermes model` offers an OAuth device-code login. The Copilot API does **not** accept classic PATs (`ghp_*`) — supported types are OAuth tokens (`gho_`), fine-grained PATs (`github_pat_`, needs the Copilot Requests permission), and GitHub App tokens (`ghu_`).

On HTTP 401, Hermes performs a one-shot credential recovery before fallback: re-resolve the token via the priority chain, rebuild the shared OpenAI client with refreshed headers, then retry the request once. **API routing:** GPT-5+ models (except `gpt-5-mini`) automatically use the Responses API; all other models (GPT-4o, Claude, Gemini) use Chat Completions, with models auto-detected from the live Copilot catalog. ACP env overrides: `HERMES_COPILOT_ACP_COMMAND` (default `copilot`) and `HERMES_COPILOT_ACP_ARGS` (default `--acp --stdio`).

## First-Class API-Key Providers

These providers have built-in support with dedicated provider IDs. Set the API key in `~/.hermes/.env` and use `--provider` to select. The canonical invocation pattern is one `hermes chat --provider <id> --model <model>` line plus the matching `*_API_KEY`:

```bash
# NovitaAI Model API — NOVITA_API_KEY
hermes chat --provider novita --model moonshotai/kimi-k2.5
# z.ai / ZhipuAI GLM — GLM_API_KEY
hermes chat --provider zai --model glm-5
# Kimi / Moonshot AI (international api.moonshot.ai) — KIMI_API_KEY
hermes chat --provider kimi-coding --model kimi-for-coding
# MiniMax (global) — MINIMAX_API_KEY
hermes chat --provider minimax --model MiniMax-M2.7
# Qwen Cloud / DashScope — DASHSCOPE_API_KEY
hermes chat --provider alibaba --model qwen3.5-plus
# GMI Cloud — GMI_API_KEY (use the exact ID from GMI's /v1/models)
hermes chat --provider gmi --model zai-org/GLM-5.1-FP8
```

The full first-class set also includes `kimi-coding-cn`, `minimax-cn`, `xiaomi` (MiMo), `tencent-tokenhub` (Hy3 Preview), `arcee` (Trinity), DeepSeek, OpenCode Zen/Go, Kilo Code, and StepFun (`step-3.5-flash`). Set a provider permanently via `model.provider`/`model.default`. **Base URLs can be overridden** with `NOVITA_BASE_URL`, `GLM_BASE_URL`, `KIMI_BASE_URL`, `MINIMAX_BASE_URL`, `MINIMAX_CN_BASE_URL`, `DASHSCOPE_BASE_URL`, `XIAOMI_BASE_URL`, `GMI_BASE_URL`, `TOKENHUB_BASE_URL`, or `STEPFUN_BASE_URL`. For z.ai/GLM, Hermes auto-probes multiple endpoints (global, China, coding variants) to find one that accepts your key and caches it — no manual `GLM_BASE_URL` needed.

## xAI Grok (Responses API + Prompt Caching)

xAI is wired through the **Responses API** (`codex_responses` transport) for automatic reasoning on Grok 4 models — no `reasoning_effort` parameter needed. Set `XAI_API_KEY` and pick xAI in `hermes model`, or use `grok` as a shortcut (`/model grok-4-fast-reasoning`). SuperGrok and X Premium+ subscribers can sign in with browser OAuth instead of an API key (pick "xAI Grok OAuth (SuperGrok / Premium+)" or run `hermes auth add xai-oauth`); the OAuth bearer is reused by direct-to-xAI tools (TTS, image/video gen, transcription).

When any base URL contains `x.ai`, Hermes **automatically enables prompt caching** by sending the `x-grok-conv-id` header on every request — this routes requests to the same server within a conversation so xAI's infrastructure can reuse cached system prompts and history, reducing latency and cost for multi-turn conversations. No configuration is required. (A retired-model migration helper, `hermes migrate xai`, rewrites configs pointing at retired Grok refs; per-provider deep setup → SP15 guide.)

## OAuth Catalog: Qwen, MiniMax, Gemini

The browser-OAuth providers all persist a refresh token (typically to `~/.hermes/auth.json`) after a `hermes model` login:

- **Qwen Portal (`qwen-oauth`):** browser OAuth against Alibaba's consumer Qwen Portal (`portal.qwen.ai/v1`, override with `HERMES_QWEN_BASE_URL`); distinct from the `alibaba` DashScope API-key provider for programmatic workloads.
- **MiniMax (`minimax-oauth`):** browser OAuth, Anthropic Messages-compatible endpoint (`api.minimax.io/anthropic`); models `MiniMax-M2.7` (main) and `MiniMax-M2.7-highspeed` (default auxiliary); the OAuth path ignores `MINIMAX_API_KEY`/`MINIMAX_BASE_URL`.
- **Google Gemini OAuth (`google-gemini-cli`):** uses Google's Cloud Code Assist backend (the same API as Google's `gemini-cli`) via PKCE Authorization Code flow against `accounts.google.com`, callback at `http://127.0.0.1:8085/oauth2callback`, tokens at `~/.hermes/auth/google_oauth.json` (chmod 0600). Traffic goes to `cloudcode-pa.googleapis.com/v1internal:generateContent`; OpenAI-shaped requests are translated to Gemini's native `contents[]`/`tools[].functionDeclarations`/`toolConfig` shape and back. Free tier auto-provisions a Google-managed project; Workspace/Enterprise accounts set `HERMES_GEMINI_PROJECT_ID` or `GOOGLE_CLOUD_PROJECT`; `/gquota` shows remaining Code Assist quota. A policy warning is shown and explicit confirmation required before OAuth begins (Google considers third-party use of the Gemini CLI client a policy violation).

## AWS Bedrock

Anthropic Claude, Amazon Nova, DeepSeek, Meta Llama, and other models via AWS Bedrock. Uses the AWS SDK (`boto3`) credential chain — no API key, just standard AWS auth.

```bash
# Simplest — named profile in ~/.aws/credentials
hermes chat --provider bedrock --model us.anthropic.claude-sonnet-4-6

# Or with explicit env vars
AWS_PROFILE=myprofile AWS_REGION=us-east-1 hermes chat --provider bedrock --model us.anthropic.claude-sonnet-4-6
```

Or permanently in `config.yaml`:

```yaml
model:
  provider: "bedrock"
  default: "us.anthropic.claude-sonnet-4-6"
bedrock:
  region: "us-east-1"          # or set AWS_REGION
  # profile: "myprofile"       # or set AWS_PROFILE
  # discovery: true            # auto-discover region from IAM
  # guardrail:                 # optional Bedrock Guardrails
  #   guardrail_identifier: "your-guardrail-id"
  #   guardrail_version: "DRAFT"
```

Authentication uses the standard boto3 chain (explicit `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, `AWS_PROFILE`, IAM role on EC2/ECS/Lambda, IMDS, or SSO). Bedrock uses the **Converse API** under the hood — requests are translated to Bedrock's model-agnostic shape, so the same config works for Claude, Nova, DeepSeek, and Llama. Set `BEDROCK_BASE_URL` only for a non-default regional endpoint. (Alibaba Coding Plan `alibaba-coding-plan` is a separate billing SKU at `coding-intl.dashscope.aliyuncs.com/v1` reusing the same `DASHSCOPE_API_KEY`.)

## NVIDIA NIM, GMI Cloud, StepFun, Hugging Face, Ollama Cloud

The remaining OpenAI-compatible cloud providers follow the same API-key + optional-`*_BASE_URL` pattern:

- **NVIDIA NIM (`nvidia`):** [Nemotron](../../term_dictionary/term_nemotron.md) and other models via `build.nvidia.com` (free key, `NVIDIA_API_KEY`) or a local NIM endpoint (`NVIDIA_BASE_URL=http://localhost:8000/v1`). Hermes auto-attaches a NIM billing-origin header on every request to `build.nvidia.com`.
- **GMI Cloud (`gmi`):** OpenAI-compatible, `GMI_API_KEY`, default base URL `https://api.gmi-serving.com/v1` (`GMI_BASE_URL` override).
- **StepFun (`stepfun`):** Step-series models, `STEPFUN_API_KEY`, default `https://api.stepfun.com/v1` (`STEPFUN_BASE_URL`).
- **Hugging Face Inference Providers (`huggingface`/`hf`):** routes 20+ open models through a unified endpoint (`router.huggingface.co/v1`) with **automatic failover** to the fastest backend (Groq, Together, SambaNova). `HF_TOKEN` (enable "Make calls to Inference Providers"). Append routing suffixes `:fastest` (default), `:cheapest`, or `:provider_name`. Override with `HF_BASE_URL`.
- **Ollama Cloud (`ollama-cloud`):** managed Ollama catalog without a GPU; pick it in `hermes model`, paste `OLLAMA_API_KEY`; catalog fetched from `ollama.com/v1/models` and cached one hour; `model:tag` notation preserved. (Local Ollama is reached via the Custom Endpoint flow — see [Local & Self-Hosted LLM Providers](hermes_local_self_hosted_llm.md).)

**Source**: `inbox/hermes_agent_docs/integrations/providers.md` · https://hermes-agent.nousresearch.com/docs/integrations/providers
**Last Updated**: 2026-06-19
**Status**: Active
