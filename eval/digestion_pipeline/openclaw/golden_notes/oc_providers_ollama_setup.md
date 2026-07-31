---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - ollama
keywords:
  - openclaw ollama setup
  - ollama native api chat
  - ollama-local marker auth
  - ollama three modes cloud local
  - ollama model discovery api tags
  - ollama_api_key
  - ollama baseurl no v1
  - implicit ollama provider
topics:
  - OpenClaw
  - Ollama Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/ollama
access_control_group: ["general"]
---

# OpenClaw — Setting Up the Ollama Provider (Modes, Auth, Discovery)

## Overview

This procedure covers connecting OpenClaw to Ollama for cloud and local models, mirroring the setup half of the `providers/ollama` source page: the integration's native `/api/chat` transport (and the forbidden `/v1` route), the three run modes, the per-host auth rules, interactive and manual onboarding, the cloud/local/hybrid mode choices, implicit model auto-discovery from `/api/tags`, and the basic/explicit/custom-base-URL configuration shapes. Vision/image understanding, advanced tuning (context windows, thinking, embeddings, web search), and troubleshooting are continued in [oc_providers_ollama_vision](oc_providers_ollama_vision.md) and [oc_providers_ollama_advanced](oc_providers_ollama_advanced.md); dedicated cloud-only routing is in [oc_providers_ollama_cloud](oc_providers_ollama_cloud.md).

## Integration Basics and the `/v1` Warning

OpenClaw integrates with Ollama's **native API** (`/api/chat`) for hosted cloud models and local/self-hosted Ollama servers. Ollama runs in **three modes**: `Cloud + Local` through a reachable Ollama host, `Cloud only` against `https://ollama.com`, or `Local only` against a reachable Ollama host. OpenClaw also registers `ollama-cloud` as a first-class hosted provider id for direct Ollama Cloud use — use refs like `ollama-cloud/kimi-k2.5:cloud` when you want cloud-only routing without sharing the local `ollama` provider id (see the dedicated [Ollama Cloud](https://docs.openclaw.ai/providers/ollama-cloud) page). Remote Ollama users must **not** use the `/v1` OpenAI-compatible URL (`http://host:11434/v1`) with OpenClaw: it breaks tool calling and models may output raw tool JSON as plain text — use the native Ollama API URL instead (`baseUrl: "http://host:11434"`, no `/v1`). Ollama provider config uses `baseUrl` as the canonical key; OpenClaw also accepts `baseURL` for compatibility with OpenAI SDK-style examples, but new config should prefer `baseUrl`.

## Auth Rules

Auth resolution is per-host, with a local marker for hosts that need no real bearer token:

- **Local and LAN hosts** — do not need a real bearer token. OpenClaw uses the local `ollama-local` marker only for loopback, private-network, `.local`, and bare-hostname Ollama base URLs.
- **Remote and Ollama Cloud hosts** — remote public hosts and Ollama Cloud (`https://ollama.com`) require a real credential through `OLLAMA_API_KEY`, an auth profile, or the provider's `apiKey`. For direct hosted use, prefer provider `ollama-cloud`.
- **Custom provider ids** — custom provider ids that set `api: "ollama"` follow the same rules. For example, an `ollama-remote` provider that points at a private LAN Ollama host can use `apiKey: "ollama-local"` and sub-agents will resolve that marker through the Ollama provider hook instead of treating it as a missing credential. Memory search can set `agents.defaults.memorySearch.provider` to that custom provider id so embeddings use the matching Ollama endpoint.
- **Auth profiles** — `auth-profiles.json` stores the credential for a provider id; put endpoint settings (`baseUrl`, `api`, model ids, headers, timeouts) in `models.providers.<id>`. Older flat auth-profile files such as `{ "ollama-windows": { "apiKey": "ollama-local" } }` are not a runtime format; run `openclaw doctor --fix` to rewrite them to the canonical `ollama-windows:default` API-key profile with a backup. A `baseUrl` in that file is compatibility noise and should be moved to provider config.
- **Memory embedding scope** — when Ollama is used for memory embeddings, bearer auth is scoped to the host where it was declared: a provider-level key is sent only to that provider's Ollama host; `agents.*.memorySearch.remote.apiKey` is sent only to its remote embedding host; and a pure `OLLAMA_API_KEY` env value is treated as the Ollama Cloud convention, not sent to local or self-hosted hosts by default.

## Getting Started

Two onboarding paths are documented: guided onboarding (recommended) and manual setup.

### Onboarding (recommended)

Run `openclaw onboard` and select **Ollama** from the provider list, then choose your mode and select a model:

```bash
openclaw onboard
```

The three mode choices are **Cloud + Local** (local Ollama host plus cloud models routed through that host), **Cloud only** (hosted Ollama models via `https://ollama.com`), and **Local only** (local models only). `Cloud only` prompts for `OLLAMA_API_KEY` and suggests hosted cloud defaults; `Cloud + Local` and `Local only` ask for an Ollama base URL, discover available models, and auto-pull the selected local model if it is not available yet. When Ollama reports an installed `:latest` tag such as `gemma4:latest`, setup shows that installed model once instead of showing both `gemma4` and `gemma4:latest` or pulling the bare alias again; `Cloud + Local` also checks whether that Ollama host is signed in for cloud access. Verify the model is available with `openclaw models list --provider ollama`. A **non-interactive** onboarding flow is also available (optionally with a custom base URL and model):

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://ollama-host:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk
```

### Manual setup

For full control: choose **Cloud + Local** (install Ollama, sign in with `ollama signin`, route cloud requests through that host), **Cloud only** (use `https://ollama.com` with an `OLLAMA_API_KEY`), or **Local only** (install Ollama from `ollama.com/download` and `ollama pull` a model such as `gemma4`, `gpt-oss:20b`, or `llama3.3`). Enable Ollama via env or config, then inspect and set the model. For `Cloud only` use your real `OLLAMA_API_KEY`; for host-backed setups any placeholder works:

```bash
# Cloud
export OLLAMA_API_KEY="your-ollama-api-key"
# Local-only
export OLLAMA_API_KEY="ollama-local"
# Or configure in your config file
openclaw config set models.providers.ollama.apiKey "OLLAMA_API_KEY"

openclaw models list
openclaw models set ollama/gemma4
```

## Cloud Models (Mode Behavior)

The three modes behave as follows during setup:

- **Cloud + Local** — uses a reachable Ollama host as the control point for both local and cloud models (Ollama's preferred hybrid flow). OpenClaw prompts for the Ollama base URL, discovers local models from that host, and checks whether the host is signed in for cloud access with `ollama signin`. When signed in, OpenClaw suggests hosted cloud defaults such as `kimi-k2.5:cloud`, `minimax-m2.7:cloud`, and `glm-5.1:cloud`. If the host is not signed in yet, OpenClaw keeps the setup local-only until you run `ollama signin`.
- **Cloud only** — runs against Ollama's hosted API at `https://ollama.com`. OpenClaw prompts for `OLLAMA_API_KEY`, sets `baseUrl: "https://ollama.com"`, and seeds the hosted cloud model list. This path does **not** require a local Ollama server or `ollama signin`. The cloud model list shown during `openclaw onboard` is populated live from `https://ollama.com/api/tags`, capped at 500 entries; if `ollama.com` is unreachable or returns no models at setup time, OpenClaw falls back to the previous hardcoded suggestions so onboarding still completes. You can also configure the first-class cloud provider directly with `openclaw onboard --auth-choice ollama-cloud` then `openclaw models set ollama-cloud/kimi-k2.5:cloud`.
- **Local only** — OpenClaw discovers models from the configured Ollama instance; this path is for local or self-hosted Ollama servers, and OpenClaw currently suggests `gemma4` as the local default.

## Model Discovery (Implicit Provider)

When you set `OLLAMA_API_KEY` (or an auth profile) and do **not** define `models.providers.ollama` or another custom remote provider with `api: "ollama"`, OpenClaw discovers models from the local Ollama instance at `http://127.0.0.1:11434`. Discovery behavior:

| Behavior | Detail |
| --- | --- |
| Catalog query | Queries `/api/tags` |
| Capability detection | Best-effort `/api/show` lookups read `contextWindow`, expanded `num_ctx` Modelfile parameters, and capabilities including vision/tools |
| Vision models | Models with a `vision` capability reported by `/api/show` are marked image-capable (`input: ["text", "image"]`), so OpenClaw auto-injects images into the prompt |
| Reasoning detection | Uses `/api/show` capabilities (including `thinking`); falls back to a model-name heuristic (`r1`, `reasoning`, `think`) when Ollama omits capabilities |
| Token limits | Sets `maxTokens` to the default Ollama max-token cap used by OpenClaw |
| Costs | Sets all costs to `0` |

This avoids manual model entries while keeping the catalog aligned with the local Ollama instance. You can use a full ref such as `ollama/<pulled-model>:latest` in local `infer model run`; OpenClaw resolves that installed model from Ollama's live catalog without a hand-written `models.json` entry. For signed-in hosts, some `:cloud` models may be usable through `/api/chat` and `/api/show` before they appear in `/api/tags`: when you explicitly select a full `ollama/<model>:cloud` ref, OpenClaw validates that exact missing model with `/api/show` and adds it to the runtime catalog only if Ollama confirms model metadata — typos still fail as unknown models instead of being auto-created. To add a new model, simply pull it with Ollama (`ollama pull mistral`) and it is automatically discovered. When you switch a conversation with `/model ollama/<model>`, OpenClaw treats that as an exact user selection: if the configured Ollama `baseUrl` is unreachable, the next reply fails with the provider error instead of silently answering from another fallback model. Isolated cron jobs do one extra local safety check — if the selected model resolves to a local, private-network, or `.local` Ollama provider and `/api/tags` is unreachable, OpenClaw records that cron run as `skipped` with the selected `ollama/<model>` in the error text; the endpoint preflight is cached for 5 minutes so multiple cron jobs pointed at the same stopped Ollama daemon do not all launch failing model requests.

```bash
# See what models are available, then live-verify local text, native stream, embeddings
ollama list
openclaw models list
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_OLLAMA=1 OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=0 \
  pnpm test:live -- extensions/ollama/ollama.live.test.ts
```

If you set `models.providers.ollama` explicitly, or configure a custom remote provider such as `models.providers.ollama-cloud` with `api: "ollama"`, auto-discovery is **skipped** and you must define models manually. Loopback custom providers such as `http://127.0.0.2:11434` are still treated as local.

## Configuration

Three configuration shapes are documented — basic implicit discovery, explicit manual models, and a custom base URL.

**Basic (implicit discovery)** — the simplest local-only enablement path is via environment variable; if `OLLAMA_API_KEY` is set you can omit `apiKey` in the provider entry and OpenClaw will fill it for availability checks:

```bash
export OLLAMA_API_KEY="ollama-local"
```

**Explicit (manual models)** — use explicit config for hosted cloud setup, when Ollama runs on another host/port, to force specific context windows or model lists, or for fully manual model definitions. **Custom base URL** — if Ollama runs on a different host or port (explicit config disables auto-discovery, so define models manually); do **not** add `/v1` to the URL, which selects unreliable OpenAI-compatible mode — use the base Ollama URL without a path suffix:

```json5
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434", // No /v1 - use native Ollama API URL
        api: "ollama", // Set explicitly to guarantee native tool-calling behavior
        timeoutSeconds: 300, // Optional: give cold local models longer to connect and stream
        models: [
          {
            id: "qwen3:32b",
            name: "qwen3:32b",
            params: {
              keep_alive: "15m", // Optional: keep the model loaded between turns
            },
          },
        ],
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `providers/ollama` (mirror `inbox/openclaw_docs/providers/ollama.md`), setup/discovery half
**Last Updated**: 2026-06-22
**Status**: Active
