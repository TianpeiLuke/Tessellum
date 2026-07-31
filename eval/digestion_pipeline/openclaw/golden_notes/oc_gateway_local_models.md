---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - local_models
keywords:
  - openclaw local models
  - self-hosted llm openclaw
  - lm studio responses api
  - openai-compatible local proxy
  - local model hardware floor
  - prompt injection local model
  - hosted primary local fallback
  - tool_choice required override
  - local model troubleshooting
topics:
  - OpenClaw
  - Local Models
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/local-models
access_control_group: ["general"]
---

# OpenClaw — Running on Self-Hosted Local Models

## Overview

This note is the procedure for running OpenClaw against self-hosted local LLMs — LM Studio, vLLM, LiteLLM, MLX, SGLang, Ollama, ds4, and custom OpenAI-compatible endpoints — mirroring the `gateway/local-models` source page. It covers the hardware floor and prompt-injection safety bar, backend selection, the recommended LM-Studio-Responses-API config plus hosted-fallback hybrids and regional routing, OpenAI-compatible proxy configuration (compat flags, exact-origin trust, tool-call forcing), the smaller/stricter-backend narrowing ladder, and a troubleshooting checklist. For servers that should start only when a selected model needs them, the page defers to [Local model services](https://docs.openclaw.ai/gateway/local-model-services).

## Hardware Floor

Local models are doable but raise the bar on hardware, context size, and prompt-injection defense: small or aggressively quantized cards truncate context and leak safety. Aim high — **≥2 maxed-out Mac Studios or an equivalent GPU rig (~$30k+)** for a comfortable agent loop. A single **24 GB** GPU works only for lighter prompts at higher latency. Always run the **largest / full-size variant you can host**; small or heavily quantized checkpoints raise prompt-injection risk. For lowest-friction onboarding the page points to LM Studio or Ollama plus `openclaw onboard`.

## Pick a Backend

Choose the backend by workflow. The source page's selection table:

| Backend | Use when |
| --- | --- |
| ds4 | Local DeepSeek V4 Flash on macOS Metal with OpenAI-compatible tool calls |
| LM Studio | First-time local setup, GUI loader, native Responses API |
| LiteLLM / OAI-proxy / custom OpenAI-compatible proxy | You front another model API and need OpenClaw to treat it as OpenAI |
| MLX / vLLM / SGLang | High-throughput self-hosted serving with an OpenAI-compatible HTTP endpoint |
| Ollama | CLI workflow, model library, hands-off systemd service |

Use the Responses API (`api: "openai-responses"`) when the backend supports it (LM Studio does); otherwise use Chat Completions (`api: "openai-completions"`). A WSL2 warning applies to **WSL2 + Ollama + NVIDIA/CUDA users**: the official Ollama Linux installer enables a systemd service with `Restart=always`, and on WSL2 GPU setups autostart can reload the last model during boot and pin host memory; if the WSL2 VM repeatedly restarts, the page links the `WSL2 crash loop` provider note.

## Recommended: LM Studio + Large Local Model (Responses API)

This is the page's "best current local stack." Load a large model in LM Studio (for example a full-size Qwen, DeepSeek, or Llama build), enable the local server (default `http://127.0.0.1:1234`), and use the Responses API to keep reasoning separate from final text. The recommended provider config:

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/my-local-model" },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "lmstudio/my-local-model": { alias: "Local" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "my-local-model",
            name: "Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

**Setup checklist**: install LM Studio at `https://lmstudio.ai`; download the **largest model build available** (avoid "small"/heavily quantized variants), start the server, and confirm `http://127.0.0.1:1234/v1/models` lists it; replace `my-local-model` with the actual model ID shown in LM Studio; keep the model loaded (cold-load adds startup latency); adjust `contextWindow`/`maxTokens` if your build differs; and for WhatsApp stick to the Responses API so only final text is sent. Keep hosted models configured even when running local and use `models.mode: "merge"` so fallbacks stay available.

### Hybrid Config: Hosted Primary / Local-First with Safety Net

Reuse the recommended block's `models.providers.lmstudio` entry and `models.mode: "merge"`, but set `agents.defaults.model.primary: "anthropic/claude-sonnet-4-6"` with `fallbacks: ["lmstudio/my-local-model", "anthropic/claude-opus-4-6"]` (and aliases `Sonnet`/`Local`/`Opus`). For **local-first with a hosted safety net**, swap the primary and fallback order — keep the same providers block and `models.mode: "merge"` so you can fall back to Sonnet or Opus when the local box is down.

### Regional Hosting / Data Routing

Hosted MiniMax/Kimi/GLM variants also exist on OpenRouter with region-pinned endpoints (e.g., US-hosted); pick the regional variant there to keep traffic in your chosen jurisdiction while still using `models.mode: "merge"` for Anthropic/OpenAI fallbacks. Local-only remains the strongest privacy path; hosted regional routing is the middle ground when you need provider features but want control over data flow.

## Other OpenAI-Compatible Local Proxies

MLX (`mlx_lm.server`), vLLM, SGLang, LiteLLM, OAI-proxy, or custom gateways work if they expose an OpenAI-style `/v1/chat/completions` endpoint. Use the Chat Completions adapter unless the backend documents `/v1/responses` support. Replace the LM Studio provider block with your endpoint and model ID:

```json5
{
  agents: {
    defaults: {
      model: { primary: "local/my-local-model" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      local: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "sk-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        models: [ { id: "my-local-model", name: "Local Model", reasoning: false, input: ["text"], cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }, contextWindow: 120000, maxTokens: 8192 } ],
      },
    },
  },
}
```

If `api` is omitted on a custom provider with a `baseUrl`, OpenClaw defaults to `openai-completions`. Custom/local provider entries trust their exact configured `baseUrl` origin for guarded model requests (loopback, LAN, tailnet, and private DNS hosts); requests to other private origins still need `request.allowPrivateNetwork: true`, and metadata/link-local origins remain blocked without explicit opt-in. Set it to `false` to opt out of exact-origin trust.

The `models.providers.<id>.models[].id` value is provider-local — do not include the provider prefix there. For example, an MLX server started with `mlx_lm.server --model mlx-community/Qwen3-30B-A3B-6bit` uses catalog id `models.providers.mlx.models[].id: "mlx-community/Qwen3-30B-A3B-6bit"` and model ref `agents.defaults.model.primary: "mlx/mlx-community/Qwen3-30B-A3B-6bit"`. Set `input: ["text", "image"]` on local or proxied vision models so image attachments are injected into agent turns; onboarding infers common vision model IDs (use `--custom-image-input` for unknown vision IDs or `--custom-text-input` for a known-looking model that is text-only behind your endpoint).

Use `models.providers.<id>.timeoutSeconds` for slow servers before raising `agents.defaults.timeoutSeconds`; the provider timeout applies only to model HTTP requests (connect, headers, body streaming, and the total guarded-fetch abort), and if the agent or run timeout is lower you must raise that ceiling too because provider timeouts cannot extend the whole agent run. For custom providers, a non-secret local marker such as `apiKey: "ollama-local"` is accepted when `baseUrl` resolves to loopback, a private LAN, `.local`, or a bare hostname — OpenClaw treats it as a valid local credential; use a real value for any provider that accepts a public hostname.

For local/proxied `/v1` backends the source flags three behaviors: OpenClaw treats these as proxy-style OpenAI-compatible routes, not native OpenAI endpoints; native OpenAI-only request shaping does not apply (no `service_tier`, no Responses `store`, no OpenAI reasoning-compat payload shaping, no prompt-cache hints); and hidden OpenClaw attribution headers (`originator`, `version`, `User-Agent`) are not injected on these custom proxy URLs.

### Compatibility Notes for Stricter Backends

Some servers accept only string `messages[].content` on Chat Completions, not structured content-part arrays — set `models.providers.<provider>.models[].compat.requiresStringContent: true` for those endpoints. Some local models emit standalone bracketed tool requests as text, such as `[tool_name]` followed by JSON and `[END_TOOL_REQUEST]`; OpenClaw promotes those into real tool calls only when the name exactly matches a registered tool for the turn, otherwise the block is hidden from user-visible replies. If a model emits JSON, XML, or ReAct-style text that looks like a tool call but the provider did not emit a structured invocation, OpenClaw leaves it as text and logs a warning (run id, provider/model, detected pattern, tool name when available) — treat that as provider/model tool-call incompatibility, not a completed tool run.

If tools appear as assistant text instead of running (raw JSON, XML, ReAct syntax, or an empty `tool_calls` array in the provider response), first verify the server uses a tool-call-capable chat template/parser. For OpenAI-compatible Chat Completions backends whose parser works only when tool use is forced, set a per-model request override instead of relying on text parsing:

```json5
{
  agents: {
    defaults: {
      models: {
        "local/my-local-model": {
          params: {
            extra_body: {
              tool_choice: "required",
            },
          },
        },
      },
    },
  },
}
```

Use this only for models/sessions where every normal turn should call a tool — it overrides OpenClaw's default proxy value of `tool_choice: "auto"`. Replace `local/my-local-model` with the exact provider/model ref shown by `openclaw models list`; the equivalent CLI form is `openclaw config set agents.defaults.models '{"local/my-local-model":{"params":{"extra_body":{"tool_choice":"required"}}}}' --strict-json --merge`. If a custom OpenAI-compatible model accepts OpenAI reasoning efforts beyond the built-in profile, declare them on that model entry's `compat` block — adding `"xhigh"` to `compat.supportedReasoningEfforts` with a `compat.reasoningEffortMap: { xhigh: "xhigh" }` entry exposes the level via `/think xhigh`, session pickers, Gateway validation, and `llm-task` validation for that configured provider/model ref.

## Smaller or Stricter Backends

If the model loads cleanly but full agent turns misbehave, work top-down — confirm transport first, then narrow the surface:

1. **Confirm the local model responds** (no tools, no agent context): `openclaw infer model run --local --model <provider/model> --prompt "Reply with exactly: pong" --json`.
2. **Confirm Gateway routing**: `openclaw infer model run --gateway --model <provider/model> --prompt "Reply with exactly: pong" --json`. This sends only the supplied prompt — skipping transcript, AGENTS bootstrap, context-engine assembly, tools, and bundled MCP servers — but still exercises Gateway routing, auth, and provider selection.
3. **Try lean mode.** If both probes pass but real agent turns fail with malformed tool calls or oversized prompts, enable `agents.defaults.experimental.localModelLean: true`. It drops the three heaviest default tools (`browser`, `cron`, `message`) and defaults larger tool catalogs behind structured Tool Search controls, except for runs that must keep direct `message` delivery.
4. **Disable tools entirely as a last resort.** If lean mode is not enough, set `models.providers.<provider>.models[].compat.supportsTools: false` for that entry; the agent then operates without tool calls on that model.
5. **Past that, the bottleneck is upstream** — after lean mode and `supportsTools: false`, remaining failures on larger runs are usually upstream model/server capacity (context window, GPU memory, kv-cache eviction, or a backend bug), not OpenClaw's transport layer.

## Troubleshooting

The page's checklist: confirm the Gateway can reach the proxy with `curl http://127.0.0.1:1234/v1/models`; if an LM Studio model is unloaded, reload it (cold start is a common "hanging" cause). If the local server says `terminated`, `ECONNRESET`, or closes the stream mid-turn, OpenClaw records a low-cardinality `model.call.error.failureKind` plus the OpenClaw process RSS/heap snapshot in diagnostics — for LM Studio/Ollama memory pressure, match that timestamp against the server log or macOS crash/jetsam log to confirm whether the model server was killed.

On context, OpenClaw derives preflight thresholds from the detected model window (or the uncapped window when `agents.defaults.contextTokens` lowers the effective window): it warns below 20% with an **8k** floor, and hard blocks use the 10% threshold with a **4k** floor, capped to the effective context window so oversized model metadata cannot reject an otherwise valid user cap — if you hit that preflight, raise the server/model context limit or choose a larger model. For plain context errors, lower `contextWindow` or raise your server limit. If a server returns `messages[].content ... expected a string`, add `compat.requiresStringContent: true`; if it returns `validation.keys` or says message entries only allow `role` and `content`, add `compat.strictMessageKeys: true`.

If direct tiny `/v1/chat/completions` calls work but `openclaw infer model run --local` fails on Gemma or another model, check the provider URL, model ref, auth marker, and server logs first (local `model run` does not include agent tools); if local `model run` succeeds but larger agent turns fail, reduce the tool surface with `localModelLean` or `compat.supportsTools: false`. If tool calls show up as raw JSON/XML/ReAct text, or the provider returns an empty `tool_calls` array, do not add a proxy that blindly converts assistant text into tool execution — fix the server chat template/parser first, and if the model only works when tool use is forced, add the per-model `params.extra_body.tool_choice: "required"` override above. On safety: local models skip provider-side filters, so keep agents narrow and compaction on to limit prompt-injection blast radius.

**Source**: OpenClaw documentation — `gateway/local-models` (mirror `inbox/openclaw_docs/gateway/local-models.md`)
**Last Updated**: 2026-06-22
**Status**: Active
