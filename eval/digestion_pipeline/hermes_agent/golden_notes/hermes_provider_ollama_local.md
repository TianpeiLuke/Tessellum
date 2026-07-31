---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - local_inference
keywords:
  - Ollama local provider
  - zero API cost
  - custom endpoint
  - gemma4 tool calling
  - Modelfile num_ctx
  - cloud fallback
topics:
  - Hermes Agent
  - Provider Setup
  - Local LLM Inference
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup
access_control_group: ["general"]
---

# Run Hermes Locally with Ollama — Zero API Cost

## Overview

This is the step-by-step procedure for running Hermes Agent entirely on your own hardware with [Ollama](https://ollama.com) as the model backend, so no API keys, no subscriptions, and no conversation data ever leave the machine. The motivation is cost: cloud LLM APIs charge per token, and a heavy coding session can run $5–20 — money saved by serving an open-weight model locally. Once configured, Hermes behaves exactly as it does on OpenRouter or Anthropic (terminal commands, file editing, web browsing, delegation), but the model runs on local CPU/GPU.

The end state is: Ollama serving one or more open-weight models, Hermes wired to Ollama as a **Custom Endpoint**, a working local agent that can edit files / run commands / browse the web, and optionally a Telegram or Discord bot powered entirely by your own hardware. The procedure walks through hardware sizing, install + model pull, the Custom-Endpoint wiring (`http://localhost:11434/v1`), extending Ollama's tiny 2048-token default context to the Hermes 64K minimum via a `Modelfile`, keep-alive / GPU-offload speed tuning, an optional gateway bot, a cloud fallback chain that only fires when the local model fails, and the local-vs-cloud capability split that defines the "sweet spot."

## What You Need

Hardware scales with model size. A 3B model runs in 8 GB RAM; a 27B+ model wants 32+ GB. A GPU is **not required** — Ollama runs CPU-only — but an NVIDIA GPU with 8+ GB VRAM speeds things up significantly.

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 8 GB (for 3B models) | 32+ GB (for 27B+ models) |
| **Storage** | 5 GB free | 30+ GB (for multiple models) |
| **CPU** | 4 cores | 8+ cores (AMD EPYC, Ryzen, Intel Xeon) |
| **GPU** | Not required | NVIDIA GPU with 8+ GB VRAM speeds things up significantly |

CPU-only works but is slower: a 9B model on a modern 8-core CPU gives ~10 tokens/sec; a 31B model on CPU is ~2–5 tokens/sec (30–120 s per response). For slow CPU-only setups, widen the API timeout via the env var (it is **not** a `config.yaml` key):

```bash
# ~/.hermes/.env
HERMES_API_TIMEOUT=1800   # 30 minutes — generous for slow local models
```

## Step 1: Install Ollama

Install with the one-line script (`curl -fsSL https://ollama.com/install.sh | sh`), then verify the daemon is up: `ollama --version` and `curl http://localhost:11434/api/tags` (should return `{"models":[]}`).

## Step 2: Pull a Model

Choose a model by hardware **and** tool-calling support. Tool calling is the load-bearing axis: Hermes is an **agentic** assistant that edits files, runs commands, and browses the web through tool calls, so a model without tool-call support can only chat — it cannot take actions. `gemma4:31b` is the recommended choice because it is the only model in the table with reliable tool calling.

| Model | Size on Disk | RAM Needed | Tool Calling | Best For |
|-------|-------------|------------|:------------:|----------|
| `gemma4:31b` | ~20 GB | 24+ GB | Yes | Best quality — strong tool use and reasoning |
| `gemma2:27b` | ~16 GB | 20+ GB | No | Conversational tasks, no tool use |
| `gemma2:9b` | ~5 GB | 8+ GB | No | Fast chat, Q&A — cannot call tools |
| `llama3.2:3b` | ~2 GB | 4+ GB | No | Lightweight quick answers only |

Pull the chosen model with `ollama pull gemma4:31b`. You can pull several and switch with `/model` inside Hermes; Ollama loads the active model on demand and unloads idle ones. Verify the OpenAI-compatible endpoint answers:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4:31b",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 50
  }'
```

A JSON response with the model's reply confirms the server works.

## Step 3: Configure Hermes

Run `hermes setup`. When prompted for a provider, select **Custom Endpoint** and enter Base URL `http://localhost:11434/v1`, API Key empty or `no-key` (Ollama needs none), and Model `gemma4:31b`. Alternatively edit `~/.hermes/config.yaml` directly:

```yaml
model:
  default: "gemma4:31b"
  provider: "custom"
  base_url: "http://localhost:11434/v1"
```

## Step 4: Start Using Hermes

Run `hermes` and you have a fully local agent. Try prompts like "List all Python files in this directory and count the lines of code in each," "Read the README.md and summarize what this project does," or "Create a Python script that fetches the weather for Ho Chi Minh City." Hermes uses the terminal tool, file operations, and the local model — no cloud calls.

## Step 5: Pick the Right Model for Your Task

Not every task needs the biggest model. For file edits, code, and terminal commands use `gemma4:31b` (the only model with reliable tool calling); for quick Q&A with no tool use, `gemma2:9b` is faster; for lightweight chat, `llama3.2:3b` is fastest but very limited. For full agentic work `gemma4:31b` is currently the best local option with tool-call support — check Ollama's model library for newer tool-calling models, as support is expanding rapidly. Switch mid-session with `/model gemma2:9b`.

## Step 6: Optimize for Speed

**Increase Ollama's context window.** Ollama defaults to a 2048-token context, but Hermes requires at least 64,000 tokens for agentic work with tools. Create a `Modelfile` that extends `num_ctx`, build a derived model, and point Hermes at it (`gemma4-64k`):

```bash
# Create a Modelfile that extends context
cat > /tmp/Modelfile << 'EOF'
FROM gemma4:31b
PARAMETER num_ctx 64000
EOF

ollama create gemma4-64k -f /tmp/Modelfile
```

**Keep the model loaded.** Ollama unloads models after 5 minutes idle; for a persistent gateway bot, set keep-alive to 24h either per request (`curl http://localhost:11434/api/generate -d '{"model":"gemma4:31b","keep_alive":"24h"}'`) or globally via `OLLAMA_KEEP_ALIVE=24h` in the systemd override.

**Use GPU offloading.** With an NVIDIA GPU, Ollama auto-offloads layers; `ollama ps` shows which model is loaded and how many GPU layers. A 31B model on a 12 GB GPU gets partial offload (~40 layers on GPU, rest on CPU), still a significant speedup.

## Step 7: Run as a Gateway Bot (Optional)

Once Hermes works locally in the CLI, expose it as a Telegram or Discord bot — still entirely on your hardware. For Telegram, create a bot via @BotFather, get the token, add a `platforms.telegram` block to `~/.hermes/config.yaml`, and start with `hermes gateway`:

```yaml
model:
  default: "gemma4:31b"
  provider: "custom"
  base_url: "http://localhost:11434/v1"

platforms:
  telegram:
    enabled: true
    token: "YOUR_TELEGRAM_BOT_TOKEN"
```

For Discord, create an application at discord.com/developers, add an analogous `platforms.discord` block (`enabled: true`, `token`), and start with `hermes gateway`. The bot then responds using the local model.

## Step 8: Set Up Fallbacks (Optional)

Local models can struggle with complex tasks. Configure a cloud `fallback_providers` chain that only activates when the local model fails, so ~90% of usage stays free (local) and only the hard tasks hit the paid API:

```yaml
model:
  default: "gemma4:31b"
  provider: "custom"
  base_url: "http://localhost:11434/v1"

fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
```

## Troubleshooting

- **"Connection refused" on startup** — Ollama is not running; start it with `sudo systemctl start ollama` or `ollama serve`.
- **Slow responses** — check model size vs RAM (if the model needs more RAM than available it swaps to disk; use a smaller model or add RAM); check `ollama ps` (no offloaded GPU layers means CPU-bound, normal for CPU-only servers); reduce context (large conversations slow inference — use `/compress` regularly or lower the compression threshold).
- **Model doesn't follow tool calls** — smaller models (3B, 7B) sometimes emit plain text instead of structured calls. Use a bigger model (`gemma4:31b`/`gemma2:27b`); Hermes has **auto-repair** that detects malformed tool calls and attempts to fix them; or set up a fallback so that if the local model fails 3 times Hermes falls back to a cloud provider.
- **Context window errors** — the default 2048-token Ollama context is too small for agentic work; increase it per Step 6.

## Cost Comparison

Based on a typical coding session (~100K input, ~20K output tokens), local serving eliminates the per-session API charge. Anthropic Claude Sonnet ≈ $0.80/session (~$24/month daily); OpenRouter GPT-4o ≈ $0.60/session (~$18/month); **Ollama (local) = $0.00**. The only real cost is electricity (~$0.01–0.05 per session depending on hardware).

## What Works Well Locally / What's Better with Cloud Models

Works well locally: file editing and code generation (models 9B+), terminal commands (Hermes wraps/runs the command and reads output regardless of model), web browsing (the browser tool fetches; the model interprets), **cron jobs and scheduled tasks work identically to cloud setups**, and the multi-platform gateway (Telegram, Discord, Slack all work with local models). Better with cloud: very complex multi-step reasoning (70B+ or Claude Opus class), long context windows (cloud offers 100K–1M tokens; local runtimes often default below Hermes' 64K minimum unless configured), and speed on large responses. The sweet spot is local for everyday tasks plus a cloud fallback for the hard stuff.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup
**Last Updated**: 2026-06-19
**Status**: Active
