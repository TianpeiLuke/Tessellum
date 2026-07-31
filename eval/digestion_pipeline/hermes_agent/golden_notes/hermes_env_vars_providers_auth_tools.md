---
tags:
  - resource
  - documentation
  - hermes_agent
  - environment_variables
  - providers
keywords:
  - hermes environment variables
  - provider api keys
  - provider oauth
  - tool api keys
  - langfuse observability
  - nous tool gateway
topics:
  - Hermes Agent
  - Environment Variables
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/reference/environment-variables
access_control_group: ["general"]
---

# Hermes Agent — Environment Variables: Providers, Auth & Tool APIs

## Overview

This is the **provider/authentication/tool-API half of the Hermes Agent environment-variable reference** — an enumeration of the env vars that tell Hermes *what to authenticate against*: the per-LLM-provider `*_API_KEY` / `*_BASE_URL` pairs, the Anthropic and Nous Portal OAuth knobs, the search / browser / image / voice tool-API keys, the Langfuse observability plugin vars, and the Nous Tool Gateway routing/billing vars. (The companion runtime/messaging/agent-behavior half lives in [hermes_env_vars_runtime_messaging_behavior](hermes_env_vars_runtime_messaging_behavior.md).) Every variable on this page goes in `~/.hermes/.env`, or can be written there with `hermes config set VAR value` — which routes secrets to `.env` and everything else to `config.yaml` automatically. The provider adapters read the `*_API_KEY`/`*_BASE_URL` vars at request time; the OAuth vars feed the credential-pool/auth-resolution core; the tool-API keys gate which built-in tools register. This is a look-up note: each provider/tool's concept and how-to is owned by its feature page (linked under Related Notes); SP21 captures the reference enumeration, not the feature prose.

## LLM Providers

The largest table on the source page. Each inference provider contributes an `*_API_KEY` (credential) and usually a `*_BASE_URL` (endpoint override, with a sensible default). The recommended default is **OpenRouter** (`OPENROUTER_API_KEY`) for breadth; `HERMES_OPENROUTER_CACHE`/`HERMES_OPENROUTER_CACHE_TTL` toggle OpenRouter response caching (overriding the `openrouter.response_cache*` config). Representative provider key/base-URL pairs (verbatim names):

- **Aggregators / portals**: `OPENROUTER_API_KEY` + `OPENROUTER_BASE_URL`; `NOUS_BASE_URL` / `NOUS_INFERENCE_BASE_URL` (Nous Portal/inference overrides, development only); `HERMES_QWEN_BASE_URL` (Qwen Portal default `https://portal.qwen.ai/v1`).
- **OpenAI-compatible / local**: `OPENAI_API_KEY` + `OPENAI_BASE_URL` (VLLM, SGLang, etc.); `LM_API_KEY` + `LM_BASE_URL` (LM Studio, default `http://localhost:1234/v1`); `OLLAMA_API_KEY` + `OLLAMA_BASE_URL` (Ollama Cloud).
- **First-party model providers**: `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL` / `ANTHROPIC_TOKEN`; `GOOGLE_API_KEY` (alias `GEMINI_API_KEY`) + `GEMINI_BASE_URL`, plus `HERMES_GEMINI_CLIENT_ID`/`_CLIENT_SECRET`/`_PROJECT_ID` for `google-gemini-cli` PKCE login; `DEEPSEEK_API_KEY`; `MISTRAL_API_KEY` (Voxtral TTS/STT); `XAI_API_KEY` (Grok chat + TTS + web search); `DASHSCOPE_API_KEY` (Qwen Cloud / Alibaba).
- **GitHub Copilot** (token priority chain): `COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN`; classic PATs (`ghp_*`) are **not supported** (OAuth `gho_*` or fine-grained `github_pat_*` only). ACP overrides: `HERMES_COPILOT_ACP_COMMAND` (alias `COPILOT_CLI_PATH`), `HERMES_COPILOT_ACP_ARGS`, `COPILOT_ACP_BASE_URL`, `COPILOT_API_BASE_URL`.
- **Regional / coding-plan providers** (each `*_API_KEY` + optional `*_BASE_URL`): `GLM_API_KEY` (z.ai; aliases `ZAI_API_KEY`/`Z_AI_API_KEY`), `KIMI_API_KEY`/`KIMI_CODING_API_KEY`/`KIMI_CN_API_KEY` (Moonshot), `ARCEEAI_API_KEY`, `GMI_API_KEY`, `MINIMAX_API_KEY`/`MINIMAX_CN_API_KEY` (**not** used by `minimax-oauth`, which uses browser login), `KILOCODE_API_KEY`, `XIAOMI_API_KEY`, `TOKENHUB_API_KEY`, `ALIBABA_CODING_PLAN_API_KEY`, `NOVITA_API_KEY`, `NVIDIA_API_KEY`, `STEPFUN_API_KEY`, `HF_TOKEN` (Hugging Face Inference Providers), `OPENCODE_ZEN_API_KEY`, `OPENCODE_GO_API_KEY`.
- **Amazon Bedrock**: `AWS_REGION` (e.g. `us-east-1`, read by boto3), `AWS_PROFILE` (named profile; unset = default boto3 credential chain), `BEDROCK_BASE_URL` (override; usually leave unset and use `AWS_REGION`).
- **Microsoft Foundry / Azure**: `AZURE_FOUNDRY_API_KEY` + `AZURE_FOUNDRY_BASE_URL`; `AZURE_ANTHROPIC_KEY` (Foundry Claude deployment); the Entra ID service-principal/workload-identity set `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_CLIENT_CERTIFICATE_PATH`, `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_AUTHORITY_HOST` (sovereign clouds), and `IDENTITY_ENDPOINT`/`MSI_ENDPOINT` (Managed Identity).
- **Cross-cutting overrides**: `CLAUDE_CODE_OAUTH_TOKEN` (explicit Claude Code token), `HERMES_MODEL` (process-level model override, used by the cron scheduler — prefer `config.yaml`), `VOICE_TOOLS_OPENAI_KEY` (preferred OpenAI speech key), `HERMES_LOCAL_STT_COMMAND`/`HERMES_LOCAL_STT_LANGUAGE` (local speech-to-text), and `HERMES_HOME` (override the `~/.hermes` config dir; also scopes the gateway PID file + systemd service name so multiple installs run concurrently).

Variables go in `~/.hermes/.env`, or set them via `hermes config set`:

```bash
hermes config set OPENROUTER_API_KEY sk-or-v1-...
hermes config set ANTHROPIC_API_KEY sk-ant-...
```

## Provider Auth (OAuth)

For native Anthropic auth, Hermes prefers Claude Code's own credential files when they exist, because those credentials can **refresh automatically**. **OAuth against Anthropic requires a Claude Max plan with purchased extra usage credits** — Hermes routes as Claude Code, drawing only from the Max plan's extra/overage credits (not the base Max allowance), and does **not** work on Claude Pro. Without Max + extra credits, use an API key. `ANTHROPIC_TOKEN` remains a useful manual override but is no longer the preferred Claude Max login path.

| Variable | Description |
|----------|-------------|
| `HERMES_PORTAL_BASE_URL` | Override Nous Portal URL (development/testing) |
| `NOUS_INFERENCE_BASE_URL` | Override Nous inference API URL |
| `HERMES_NOUS_MIN_KEY_TTL_SECONDS` | Min agent key TTL before re-mint (default: 1800 = 30 min) |
| `HERMES_NOUS_TIMEOUT_SECONDS` | HTTP timeout for Nous credential / token flows |
| `HERMES_DUMP_REQUESTS` | Dump API request payloads to log files (`true`/`false`) |
| `HERMES_PREFILL_MESSAGES_FILE` | Path to a JSON file of ephemeral prefill messages injected at API-call time |
| `HERMES_TIMEZONE` | IANA timezone override (e.g. `America/New_York`) |

## Tool APIs

Keys here gate which built-in tools register and which backend each tool calls. Grouped by tool domain:

- **Web search / extract / crawl**: `PARALLEL_API_KEY` (parallel.ai), `FIRECRAWL_API_KEY` + `FIRECRAWL_API_URL` (self-hosted), `TAVILY_API_KEY` + `TAVILY_BASE_URL`, `SEARXNG_URL` (free self-hosted, no key), `EXA_API_KEY`.
- **Browser automation**: `BROWSERBASE_API_KEY` + `BROWSERBASE_PROJECT_ID`, `BROWSER_USE_API_KEY`, `FIRECRAWL_BROWSER_TTL` (default 300 s), `BROWSER_CDP_URL` (Chrome DevTools Protocol, set via `/browser connect`), the Camofox anti-detection set (`CAMOFOX_URL`/`_USER_ID`/`_SESSION_KEY`/`_ADOPT_EXISTING_TAB`), `BROWSER_INACTIVITY_TIMEOUT`, and `AGENT_BROWSER_ARGS` (extra Chromium launch flags; Hermes auto-injects `--no-sandbox,--disable-dev-shm-usage` as root / on AppArmor-restricted namespaces).
- **Media generation & voice**: `FAL_KEY` (image generation, fal.ai); `GROQ_API_KEY` + `STT_GROQ_MODEL` (default `whisper-large-v3-turbo`) + `GROQ_BASE_URL` (Groq Whisper STT); `ELEVENLABS_API_KEY` (premium TTS); `STT_OPENAI_MODEL` (default `whisper-1`) + `STT_OPENAI_BASE_URL` (OpenAI-compatible STT).
- **Memory / sandbox / hub**: `GITHUB_TOKEN` (Skills Hub — higher rate limits, skill publish), `HONCHO_API_KEY` + `HONCHO_BASE_URL` (cross-session user modeling; no key for local), `HINDSIGHT_TIMEOUT` (default 60 s), `SUPERMEMORY_API_KEY` (semantic long-term memory), `DAYTONA_API_KEY` (cloud sandboxes).

### Langfuse Observability

Vars for the bundled `observability/langfuse` plugin — set in `~/.hermes/.env`, and the plugin must also be enabled (`hermes plugins enable observability/langfuse`) before they take effect.

| Variable | Description |
|----------|-------------|
| `HERMES_LANGFUSE_PUBLIC_KEY` | Langfuse project public key (`pk-lf-...`). Required. |
| `HERMES_LANGFUSE_SECRET_KEY` | Langfuse project secret key (`sk-lf-...`). Required. |
| `HERMES_LANGFUSE_BASE_URL` | Server URL (default `https://cloud.langfuse.com`; set for self-hosted) |
| `HERMES_LANGFUSE_ENV` | Environment tag on traces (`production`, `staging`, …) |
| `HERMES_LANGFUSE_RELEASE` | Release/version tag on traces |
| `HERMES_LANGFUSE_SAMPLE_RATE` | SDK sampling rate 0.0–1.0 (default `1.0`) |
| `HERMES_LANGFUSE_MAX_CHARS` | Per-field truncation for serialized payloads (default `12000`) |
| `HERMES_LANGFUSE_DEBUG` | `true` enables verbose plugin logging to `agent.log` |
| `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_BASE_URL` | Standard SDK names; accepted as fallbacks when the `HERMES_LANGFUSE_*` equivalents are unset |

### Nous Tool Gateway

Vars that configure the Tool Gateway for paid Nous subscribers or self-hosted gateway deployments. Most users don't set these — the gateway is configured automatically via `hermes model` or `hermes tools`.

| Variable | Description |
|----------|-------------|
| `TOOL_GATEWAY_DOMAIN` | Base domain for Tool Gateway routing (default `nousresearch.com`) |
| `TOOL_GATEWAY_SCHEME` | HTTP or HTTPS scheme for gateway URLs (default `https`) |
| `TOOL_GATEWAY_USER_TOKEN` | Auth token for the Tool Gateway (normally auto-populated from Nous auth) |
| `FIRECRAWL_GATEWAY_URL` | Override URL for the Firecrawl gateway endpoint specifically |

**Source**: `inbox/hermes_agent_docs/reference/environment-variables.md` · https://hermes-agent.nousresearch.com/docs/reference/environment-variables
**Last Updated**: 2026-06-19
**Status**: Active
