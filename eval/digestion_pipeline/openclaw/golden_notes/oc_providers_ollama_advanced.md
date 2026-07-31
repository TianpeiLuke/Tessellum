---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - ollama
keywords:
  - openclaw ollama advanced configuration
  - ollama common recipes config
  - ollama context window num_ctx tuning
  - ollama thinking control think levels
  - ollama memory embeddings nomic-embed-text
  - ollama web search provider
  - ollama troubleshooting wsl2 cold timeout
  - openai-compatible legacy ollama mode
  - ollama model fallbacks selection
topics:
  - OpenClaw
  - Ollama Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/ollama
access_control_group: ["general"]
---

# OpenClaw — Advanced Ollama Operation (Recipes, Tuning, Web Search, Troubleshooting)

## Overview

This note is the advanced-operation half of OpenClaw's Ollama provider page (`providers/ollama`), continuing the setup/auth/discovery note and the vision note. It procedurally covers **Common recipes** (auto-discovery, LAN host, cloud-only, signed-in cloud+local, multi-host, lean local profile), **Model selection** and provider-scoped request tuning, **Quick verification**, **Ollama Web Search** (a bundled `web_search` provider), the **Advanced configuration** cluster (legacy OpenAI-compatible mode, context windows, thinking control, reasoning models, model costs, memory embeddings, streaming), and the **Troubleshooting** runbook. The native transport is `/api/chat`; the `/v1` OpenAI-compatible route breaks tool calling and is used only deliberately as `api: "openai-completions"`.

## Common Recipes

Replace model IDs with exact names from `ollama list` or `openclaw models list --provider ollama`.

- **Local model with auto-discovery** — Ollama runs on the same machine as the Gateway and OpenClaw discovers installed models: `ollama serve`, `ollama pull gemma4`, `export OLLAMA_API_KEY="ollama-local"`, then `openclaw models list --provider ollama` and `openclaw models set ollama/gemma4`. Keeps config minimal; do **not** add a `models.providers.ollama` block unless you want manual model definitions.
- **LAN Ollama host with manual models** — use native Ollama URLs (no `/v1`), shown below.
- **Ollama Cloud only** — no local daemon: `export OLLAMA_API_KEY="your-ollama-api-key"` with a provider block pinned to `baseUrl: "https://ollama.com"`, `apiKey: "OLLAMA_API_KEY"`, `api: "ollama"`, and a `kimi-k2.5:cloud` model entry.
- **Cloud plus local through a signed-in daemon** — `ollama signin` then `ollama pull gemma4`; one `ollama` provider at `baseUrl: "http://127.0.0.1:11434"`, `apiKey: "ollama-local"`, listing a local model and a `:cloud` model, with `model.primary: "ollama/gemma4"` and `fallbacks: ["ollama/kimi-k2.5:cloud"]`.
- **Multiple Ollama hosts** — use custom provider IDs (e.g. `ollama-fast`, `ollama-large`), each with its own host, models, auth, timeout, and refs. The active provider prefix is stripped on send, so `ollama-large/qwen3.5:27b` reaches Ollama as `qwen3.5:27b`.
- **Lean local model profile** — for small models that answer simple prompts but struggle with the full agent tool surface; limit tools and context before changing global runtime settings.

The LAN-host recipe (canonical manual-model recipe; `contextWindow` is the OpenClaw-side budget and `params.num_ctx` is sent to Ollama — keep them aligned when hardware cannot run the full advertised context):

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://gpu-box.local:11434",
        apiKey: "ollama-local",
        api: "ollama",
        timeoutSeconds: 300,
        contextWindow: 32768,
        maxTokens: 8192,
        models: [
          {
            id: "qwen3.5:9b",
            name: "qwen3.5:9b",
            reasoning: true,
            input: ["text"],
            params: {
              num_ctx: 32768,
              thinking: false,
              keep_alive: "15m",
            },
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "ollama/qwen3.5:9b" },
    },
  },
}
```

For the lean local profile, set `experimental.localModelLean: true` on an agent and `compat: { supportsTools: false }` on the model entry. `localModelLean` removes the browser, cron, and message tools from the direct agent surface and defaults larger catalogs behind structured Tool Search controls (except when a run must keep direct message delivery semantics), but it does **not** change Ollama's runtime context or thinking mode — pair it with explicit `params.num_ctx` and `params.thinking: false` for small Qwen-style thinking models that loop or spend their response budget on hidden reasoning. Use `compat.supportsTools: false` only when the model or server reliably fails on tool schemas; it trades agent capability for stability.

## Model Selection and Request Tuning

Once configured, all Ollama models are available via `agents.defaults.model`, which accepts a `primary` ref plus a `fallbacks` array (e.g. `primary: "ollama/gpt-oss:20b"` with `fallbacks: ["ollama/llama3.3", "ollama/qwen2.5-coder:32b"]`). Custom Ollama provider ids are supported: when a model ref uses the active provider prefix such as `ollama-spark/qwen3:32b`, OpenClaw strips only that prefix before calling Ollama so the server receives `qwen3:32b`.

For slow local models, prefer provider-scoped request tuning before raising the whole agent runtime timeout. `timeoutSeconds` applies to the model HTTP request — including connection setup, headers, body streaming, and the total guarded-fetch abort. `params.keep_alive` is forwarded to Ollama as top-level `keep_alive` on native `/api/chat` requests; set it per model when first-turn load time is the bottleneck:

```json5
{
  models: {
    providers: {
      ollama: {
        timeoutSeconds: 300,
        models: [
          {
            id: "gemma4:26b",
            name: "gemma4:26b",
            params: { keep_alive: "15m" },
          },
        ],
      },
    },
  },
}
```

## Quick Verification

Verify the daemon is visible (`curl http://127.0.0.1:11434/api/tags`), inspect the OpenClaw catalog (`openclaw models list --provider ollama`, `openclaw models status`), and run a direct smoke turn (`openclaw infer model run --model ollama/gemma4 --prompt "Reply with exactly: ok"`). For remote hosts, replace `127.0.0.1` with the host used in `baseUrl`. If `curl` works but OpenClaw does not, check whether the Gateway runs on a different machine, container, or service account.

## Ollama Web Search

OpenClaw supports **Ollama Web Search** as a bundled `web_search` provider. The host is your configured Ollama host (`models.providers.ollama.baseUrl` when set, otherwise `http://127.0.0.1:11434`); `https://ollama.com` uses the hosted API directly. Auth is key-free for signed-in local Ollama hosts, while `OLLAMA_API_KEY` or configured provider auth is required for direct `https://ollama.com` search or auth-protected hosts. Local/self-hosted hosts must be running and signed in with `ollama signin`; direct hosted search requires `baseUrl: "https://ollama.com"` plus a real Ollama API key. Choose **Ollama Web Search** during `openclaw onboard` or `openclaw configure --section web`, or set it in config:

```json5
{
  tools: {
    web: {
      search: {
        provider: "ollama",
      },
    },
  },
}
```

For a signed-in local daemon, OpenClaw uses the daemon's `/api/experimental/web_search` proxy; for `https://ollama.com`, it calls the hosted `/api/web_search` endpoint directly. Full setup and behavior details live in the dedicated Ollama Web Search tool page.

## Advanced Configuration

**Legacy OpenAI-compatible mode** — tool calling is **not reliable** in OpenAI-compatible mode; use it only if you need OpenAI format for a proxy and do not depend on native tool calling. Set `api: "openai-completions"` explicitly against a `/v1` base URL. This mode may not support streaming and tool calling simultaneously (you may need `params: { streaming: false }`). When `api: "openai-completions"` is used with Ollama, OpenClaw injects `options.num_ctx` by default (so Ollama does not silently fall back to a 4096 context window); disable with `injectNumCtxForOpenAICompat: false` if your proxy/upstream rejects unknown `options` fields.

**Context windows** — for auto-discovered models, OpenClaw uses the context window reported by Ollama when available (including larger `PARAMETER num_ctx` from custom Modelfiles), otherwise the default. Set provider-level `contextWindow`, `contextTokens`, and `maxTokens` defaults and override per model. `contextWindow` is OpenClaw's prompt and compaction budget; native requests leave `options.num_ctx` unset unless you set `params.num_ctx`, so Ollama applies its own model, `OLLAMA_CONTEXT_LENGTH`, or VRAM-based default. To cap or force the per-request runtime context without rebuilding a Modelfile, set `params.num_ctx` (invalid, zero, negative, and non-finite values are ignored). If you upgraded an older config that used only `contextWindow`/`maxTokens`, run `openclaw doctor --fix` to copy those budgets into `params.num_ctx`. Native model entries accept common Ollama runtime options under `params` including `temperature`, `top_p`, `top_k`, `min_p`, `num_predict`, `stop`, `repeat_penalty`, `num_batch`, `num_thread`, and `use_mmap`; OpenClaw forwards only Ollama request keys, so runtime params like `streaming` are not leaked. If both a provider model entry and `agents.defaults.models["ollama/<model>"].params.num_ctx` are set, the explicit provider model entry wins.

```json5
{
  models: {
    providers: {
      ollama: {
        contextWindow: 32768,
        models: [
          {
            id: "llama3.3",
            contextWindow: 131072,
            maxTokens: 65536,
            params: {
              num_ctx: 32768,
              temperature: 0.7,
              top_p: 0.9,
              thinking: false,
            },
          }
        ]
      }
    }
  }
}
```

**Thinking control** — for native Ollama models OpenClaw forwards thinking control as top-level `think` (not `options.think`). Auto-discovered models whose `/api/show` response includes the `thinking` capability expose `/think low`, `/think medium`, `/think high`, and `/think max`; non-thinking models expose only `/think off`. You can set a model default via `agents.defaults.models["ollama/<model>"].thinking`, or use the CLI (`openclaw agent --model ollama/gemma4 --thinking off|low`). Per-model `params.think`/`params.thinking` can disable or force Ollama API thinking; OpenClaw preserves those explicit params when the active run only has the implicit default `off`, while non-off runtime commands such as `/think medium` still override the active run.

**Reasoning models** — OpenClaw treats models named like `deepseek-r1`, `reasoning`, or `think` as reasoning-capable by default (e.g. `ollama pull deepseek-r1:32b`); no additional configuration is needed.

**Model costs** — Ollama is free and runs locally, so all model costs are set to $0, for both auto-discovered and manually defined models.

**Memory embeddings** — the bundled Ollama plugin registers a memory embedding provider for memory search; it uses the configured base URL and API key, calls Ollama's `/api/embed` endpoint, and batches multiple memory chunks into one `input` request when possible. The default model is `nomic-embed-text` (auto-pulled if not present locally). Query-time embeddings use retrieval prefixes for models that require/recommend them (`nomic-embed-text`, `qwen3-embedding`, `mxbai-embed-large`); document batches stay raw so existing indexes need no migration. When `proxy.enabled=true`, embedding requests to the exact host-local loopback origin derived from `baseUrl` use OpenClaw's guarded direct path instead of the managed forward proxy — but only when the configured hostname is itself `localhost` or a loopback IP literal (DNS names that merely resolve to loopback, plus LAN/tailnet/private/public hosts, stay on the managed proxy path; redirects to another host/port do not inherit trust). Select Ollama via `agents.defaults.memorySearch.provider: "ollama"`; for a remote embedding host keep auth scoped with a `remote` block (`baseUrl`, `apiKey: "ollama-local"`, `nonBatchConcurrency`):

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "ollama",
        model: "nomic-embed-text",
        remote: {
          baseUrl: "http://gpu-box.local:11434",
          apiKey: "ollama-local",
          nonBatchConcurrency: 2,
        },
      },
    },
  },
}
```

**Streaming** — the integration uses the native Ollama API (`/api/chat`) by default, which fully supports streaming and tool calling simultaneously (no special config). For native requests `/think off` and `--thinking off` send top-level `think: false` unless an explicit `params.think`/`params.thinking` is configured; `/think low|medium|high` send the matching effort string and `/think max` maps to Ollama's highest native effort, `think: "high"`.

## Troubleshooting

- **WSL2 crash loop (repeated reboots)** — on WSL2 with NVIDIA/CUDA, the official Ollama Linux installer creates an `ollama.service` systemd unit with `Restart=always`; if it autostarts and loads a GPU-backed model during boot, Ollama can pin host memory that Hyper-V cannot reclaim, so Windows terminates the WSL2 VM and the loop repeats. Evidence: repeated WSL2 reboots/terminations from Windows, high CPU in `app.slice`/`ollama.service` shortly after startup, and SIGTERM from systemd (not a Linux OOM-killer). OpenClaw logs a startup warning when it detects WSL2 + `ollama.service` enabled with `Restart=always` + visible CUDA markers. Mitigate with `sudo systemctl disable ollama`, add `[experimental] autoMemoryReclaim=disabled` to `%USERPROFILE%\.wslconfig` (then `wsl --shutdown`), and set a shorter keep-alive (`export OLLAMA_KEEP_ALIVE=5m`) or start Ollama manually only when needed.
- **Ollama not detected** — make sure Ollama is running (`ollama serve`), that `OLLAMA_API_KEY` (or an auth profile) is set, that you did **not** define an explicit `models.providers.ollama` entry, and verify the API with `curl http://localhost:11434/api/tags`.
- **No models available** — pull the model locally (`ollama pull gemma4` / `gpt-oss:20b` / `llama3.3`) or define it explicitly in `models.providers.ollama`.
- **Connection refused** — check the port: `ps aux | grep ollama`, or restart with `ollama serve`.
- **Remote host works with curl but not OpenClaw** — verify from the Gateway's own machine/runtime (`openclaw gateway status --deep`, `curl http://ollama-host:11434/api/tags`). Common causes: `baseUrl` points at `localhost` but the Gateway runs in Docker/another host; the URL uses `/v1` (selecting OpenAI-compatible behavior); the remote host needs firewall/LAN binding changes; or the model is on your laptop's daemon but not the remote daemon.
- **Model outputs tool JSON as text** — usually OpenAI-compatible mode or a model that cannot handle tool schemas. Prefer native Ollama mode (`baseUrl: "http://ollama-host:11434"`, `api: "ollama"`); if a small local model still fails, set `compat.supportsTools: false` on that model entry and retest.
- **Kimi or GLM returns garbled symbols** — long non-linguistic symbol runs are treated as failed provider output (not a successful answer), letting retry/fallback/error handling take over without persisting corrupted text. If it recurs, capture the raw model name, the session file, and whether the run used `Cloud + Local` or `Cloud only`, then try a fresh session and a fallback model (`openclaw infer model run --model ollama/kimi-k2.5:cloud --prompt "Reply with exactly: ok" --json`; `openclaw models set ollama/gemma4`).
- **Cold local model times out** — large local models need a long first load before streaming; keep the timeout scoped to the Ollama provider (`timeoutSeconds: 300`) and optionally `params: { keep_alive: "15m" }`. `timeoutSeconds` also extends the guarded Undici connect timeout for this provider when the host is slow to accept connections.
- **Large-context model is too slow or runs out of memory** — cap both OpenClaw's budget (`contextWindow`) and Ollama's request context (`params.num_ctx`) for predictable first-token latency. Lower `contextWindow` first if OpenClaw is sending too much prompt; lower `params.num_ctx` if Ollama is loading too large a runtime context; lower `maxTokens` if generation runs too long.

**Source**: OpenClaw documentation — `providers/ollama` (mirror `inbox/openclaw_docs/providers/ollama.md`; advanced/recipes/web-search/troubleshooting sections)
**Last Updated**: 2026-06-22
**Status**: Active
