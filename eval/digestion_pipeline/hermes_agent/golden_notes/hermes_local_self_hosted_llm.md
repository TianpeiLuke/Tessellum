---
tags:
  - resource
  - documentation
  - hermes_agent
  - inference_providers
  - self_hosted
keywords:
  - custom openai-compatible endpoint
  - self-hosted llm
  - ollama vllm sglang llama.cpp lm studio
  - 64k context minimum
  - wsl2 networking
  - local model troubleshooting
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

# Hermes Agent — Local & Self-Hosted LLM Providers

## Overview

This is the self-hosted half of the Hermes Agent providers page: the procedure for pointing Hermes at **any OpenAI-compatible API endpoint** so it can drive a locally-run or self-served model instead of a cloud API. Because Hermes only needs a server that implements `/v1/chat/completions`, the same `provider: custom` pattern covers Ollama, vLLM, SGLang, llama.cpp/llama-server, LM Studio, and any other compatible server — you change only the URL, key, and model name. Two constraints recur across every server: Hermes requires at least **64,000 tokens** of context for agent use, and most servers need an explicit per-server flag to turn on native tool calling. The page closes with WSL2 networking (for Windows users running a model server on the Windows host) and a troubleshooting matrix common to all local servers.

## General Setup

Hermes Agent works with any OpenAI-compatible API endpoint. There are three ways to configure a custom endpoint.

Interactive setup (recommended):

```bash
hermes model
# Select "Custom endpoint (self-hosted / VLLM / etc.)"
# Enter: API base URL, API key, Model name
```

Manual config in `~/.hermes/config.yaml`:

```yaml
model:
  default: your-model-name
  provider: custom
  base_url: http://localhost:8000/v1
  api_key: your-key-or-leave-empty-for-local
```

Both approaches persist to `config.yaml`, which is the source of truth for model, provider, and base URL. Legacy `LLM_MODEL` in `.env` is **removed**; `OPENAI_BASE_URL` is still honored but **only** for the `openai-api` provider. For other providers and custom endpoints, use `hermes model` or set `model.base_url` directly — stale `.env` entries are cleared automatically on the next `hermes setup` or config migration.

## Switching Models with `/model`

`hermes model` (run from your terminal, outside any chat session) is the full provider setup wizard — add providers, run OAuth flows, enter API keys, configure custom endpoints. `/model` (typed inside an active session) only switches between providers and models you have **already** set up; it cannot add providers, run OAuth, or prompt for API keys. To add a new provider, exit the session (`Ctrl+C` or `/quit`), run `hermes model`, set it up, then start a new session.

Once at least one custom endpoint is configured, switch models mid-session:

```
/model custom:qwen-2.5           # Switch to a model on your custom endpoint
/model custom                    # Auto-detect the model from the endpoint
/model openrouter:claude-sonnet-4 # Switch back to a cloud provider
```

With **named custom providers** configured, use the triple syntax (e.g. `/model custom:local:qwen-2.5`). Bare `/model custom` queries the endpoint's `/models` API and auto-selects the model if exactly one is loaded — useful for local servers running a single model. When switching providers Hermes persists the base URL and provider to config; switching away from a custom endpoint clears the stale base URL.

## Ollama — Local Models, Zero Config

[Ollama](https://ollama.com/) runs open-weight models locally with one command, supports tool calling via the OpenAI-compatible API, and is best for quick local experimentation, privacy-sensitive work, and offline use. Pull/serve a model, then point Hermes at `http://localhost:11434/v1` via `hermes model` → Custom endpoint (skip the API key) or in `config.yaml`:

```yaml
model:
  default: qwen2.5-coder:32b
  provider: custom
  base_url: http://localhost:11434/v1
  context_length: 64000   # See warning below
```

**Ollama defaults to very low context lengths** — it does not use the model's full window by default. The VRAM-dependent default is 4,096 tokens (<24 GB), 32,768 (24–48 GB), or 256,000 (48+ GB). Hermes requires at least 64,000 tokens and rejects smaller windows at startup. You **cannot** set context length through the OpenAI-compatible API — it must be configured server-side (`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`, a systemd `Environment=` entry, or baked into a Modelfile with `PARAMETER num_ctx 64000`). Verify with `ollama ps` (the `CONTEXT` column shows the configured value). This is the #1 source of confusion when integrating Ollama with tools.

## vLLM, SGLang, and llama.cpp — GPU & Local Inference Servers

[vLLM](https://docs.vllm.ai/) is the standard for production GPU serving (maximum throughput, large models, continuous batching). Serve with a tool-calling parser, then point Hermes at `http://localhost:8000/v1`:

```bash
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --port 8000 \
  --max-model-len 65536 \
  --tensor-parallel-size 2 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes
```

vLLM reads `max_position_embeddings` by default; set `--max-model-len` (or `--max-model-len auto`) if it exceeds GPU memory, and `--gpu-memory-utilization 0.95` to squeeze more context into VRAM. **Tool calling requires explicit flags:** `--enable-auto-tool-choice` (for the default `tool_choice: "auto"`) plus `--tool-call-parser <name>` — supported parsers include `hermes` (Qwen 2.5, Hermes 2/3), `llama3_json`, `mistral`, `deepseek_v3`, `deepseek_v31`, `xlam`, `pythonic`. Without them, tool calls are emitted as text.

[SGLang](https://github.com/sgl-project/sglang) is a vLLM alternative using RadixAttention for KV-cache reuse — best for multi-turn (prefix caching), constrained decoding, and structured output. Launch with `--context-length 65536`, `--tp 2` (tensor parallelism), and `--tool-call-parser` (`qwen`/`llama3`/`llama4`/`deepseekv3`/`mistral`/`glm`); set `SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1` to exceed the model's declared maximum. SGLang defaults to only **128 max output tokens** — if responses look truncated, set `--default-max-tokens` or pass `max_tokens` in requests.

[llama.cpp / llama-server](https://github.com/ggml-org/llama.cpp) runs quantized GGUF models on CPU, Apple Silicon (Metal), and consumer GPUs — best for no-datacenter-GPU, Mac, and edge deployment. The context flag `-c` defaults to `0` (reads the GGUF training context), which can OOM on 128k+ models; set `-c` to at least 64,000, and note that parallel slots (`-np`) divide the total (e.g. `-c 64000 -np 4` gives each slot only 16k, below Hermes' minimum). `--jinja` is **required** for tool calling — without it, llama-server ignores the `tools` parameter and the model writes tool-call JSON as plain text. Verify tool support at `http://localhost:8080/props` (the `chat_template` field should be present). Q4_K_M quantization offers the best balance of quality vs. memory.

## LM Studio — Desktop App with Local Models

[LM Studio](https://lmstudio.ai/) is a desktop app for running local models with a GUI — best for users who prefer a visual interface, quick model testing, and developers on macOS/Windows/Linux. Start the server from the app (Developer tab → Start Server) or via the CLI:

```bash
lms server start                        # Starts on port 1234
lms load qwen2.5-coder --context-length 64000
```

Then select **LM Studio** in `hermes model`, accept the default `http://localhost:1234/v1`, and pick a discovered model (enter `LM_API_KEY` if server auth is enabled). Hermes automatically loads an LM Studio model with 64K context. To change context length, use the gear icon next to the model picker (set ≥64000 and reload), `lms load model-name --context-length 64000` (add `--estimate-only` to check fit), or My Models → gear → context size for persistent per-model defaults. Tool calling is supported since LM Studio 0.3.6; models with native tool-calling training (Qwen 2.5, Llama 3.x, Mistral, Hermes) are auto-detected and badged.

## WSL2 Networking (Windows Users)

Windows users run Hermes inside WSL2 (a Unix environment is required). If the model server runs on the **Windows host**, `localhost` inside WSL2 refers to the Linux VM, not Windows — you must bridge the gap. (If the server also runs inside WSL2, as is common for vLLM/SGLang/llama-server, they share a namespace and `localhost` works; skip this section.)

- **Option 1 — Mirrored mode (recommended, Windows 11 22H2+):** add `networkingMode=mirrored` under `[wsl2]` in `%USERPROFILE%\.wslconfig`, run `wsl --shutdown`, reopen the terminal — `localhost` now reaches Windows services bidirectionally. If the Hyper-V firewall still blocks it, allow inbound via `Set-NetFirewallHyperVVMSetting` in an Admin PowerShell.
- **Option 2 — Windows host IP (Windows 10 / older):** find the WSL2 default-gateway IP with `ip route show | grep -i default | awk '{ print $3 }'` and use it as `base_url` (e.g. `http://172.29.192.1:11434/v1`). The IP can change on restart — grab it dynamically into `$WSL_HOST`, or use the host's mDNS name (`$(hostname).local`, requires `libnss-mdns`).
- **Server bind address (required for NAT/Option 2):** the Windows server must listen beyond `127.0.0.1`. Defaults and fixes: Ollama `OLLAMA_HOST=0.0.0.0`; LM Studio "Serve on Network"; llama-server / SGLang `--host 0.0.0.0`; vLLM already binds `0.0.0.0`. In mirrored mode the default `127.0.0.1` binding works.
- **Windows Firewall:** WSL2 is a separate network in both modes; add an inbound TCP rule for the server port (Ollama `11434`, vLLM `8000`, SGLang `30000`, llama-server `8080`, LM Studio `1234`) via `New-NetFirewallRule`.

Verify from inside WSL2 with `curl http://localhost:11434/v1/models` (mirrored) or the host-IP URL (NAT); a JSON model list means you can use that URL as `base_url`.

## Troubleshooting Local Models

These issues affect **all** local inference servers used with Hermes:

- **"Connection refused" from WSL2 to a Windows-hosted server** — default NAT networking blocks `http://localhost:<port>`; apply the WSL2 Networking fix above.
- **Tool calls appear as text instead of executing** — the server lacks tool calling or the model is unsupported. Fix per server: llama.cpp `--jinja`; vLLM `--enable-auto-tool-choice --tool-call-parser hermes`; SGLang `--tool-call-parser qwen` (or appropriate); Ollama on by default (check `ollama show model-name`); LM Studio 0.3.6+ with a native-tool model.
- **Model forgets context / incoherent responses** — the context window is too small (Hermes' system prompt + tool schemas alone use 4k–8k tokens). Diagnose against the startup `Context limit: X tokens` line and the server's actual context (`ollama ps`, `curl .../props | jq '.default_generation_settings.n_ctx'`, or vLLM `--max-model-len`); set context to at least 64,000.
- **"Context limit: 2048 tokens" at startup** — Hermes auto-detects from `/v1/models`; if the server reports a low/absent value, set `model.context_length: 64000` explicitly in `config.yaml`.
- **Responses cut off mid-sentence** — either a low server output cap (SGLang's 128-token default → set `--default-max-tokens` or `model.max_tokens`; this is unrelated to history length) or context exhaustion (raise `model.context_length` or enable context compression).

**Source**: `inbox/hermes_agent_docs/integrations/providers.md` · https://hermes-agent.nousresearch.com/docs/integrations/providers
**Last Updated**: 2026-06-19
**Status**: Active
