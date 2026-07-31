---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - quickstart
keywords:
  - hermes first chat
  - choose a provider
  - hermes setup portal
  - 64k context minimum
  - verify sessions resume
  - secrets vs config storage
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
access_control_group: ["general"]
---

# Hermes Agent — Quickstart: Your First Chat

## Overview

This is the zero-to-working-chat procedure for Hermes Agent: install the CLI, choose a provider, run a first conversation, and verify that sessions resume. It is the first of two quickstart notes (the second, [next layer](hermes_quickstart_next_layer.md), covers feature layering and recovery). The governing rule is **get one clean conversation working before adding anything else** — gateway, cron, skills, voice, and routing all come later. By the end you have a CLI that responds, can call a tool, and can be resumed with `hermes --continue`.

## The Fastest Path

Pick the row that matches your goal — each is a "do this first, then this" pair:

| Goal | Do this first | Then do this |
|---|---|---|
| I just want Hermes working on my machine | `hermes setup` | Run a real chat and verify it responds |
| I already know my provider | `hermes model` | Save the config, then start chatting |
| I want a bot or always-on setup | `hermes gateway setup` after CLI works | Connect Telegram, Discord, Slack, or another platform |
| I want a local or self-hosted model | `hermes model` → custom endpoint | Verify the endpoint, model name, and context length |
| I want multi-provider fallback | `hermes model` first | Add routing and fallback only after the base chat works |

**Rule of thumb:** if Hermes cannot complete a normal chat, do not add more features yet. Get one clean conversation working first, then layer on gateway, cron, skills, voice, or routing.

## 1. Install Hermes Agent

On macOS or Windows the recommended path is the **Hermes Desktop installer**, which installs both the command-line and desktop applications. For a command-line-only install without Hermes Desktop, use the one-line installer (Linux / macOS / WSL2 / Android Termux):

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On native Windows, run in PowerShell: `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`. After it finishes, reload your shell with `source ~/.bashrc` (or `source ~/.zshrc`). Installing on a phone uses the dedicated Termux path instead — see [Termux install](hermes_install_termux_android.md). For full installation options, prerequisites, and troubleshooting, see the [Installation guide](hermes_installation.md).

## 2. Choose a Provider

This is the single most important setup step. Use `hermes model` to walk through the choice interactively:

```bash
hermes model
```

**Easiest path — Nous Portal.** One subscription covers 300+ models plus the Tool Gateway (web search, image generation, TTS, cloud browser). On a fresh install, a single command logs you in, sets Nous as your provider, and turns on the Tool Gateway:

```bash
hermes setup --portal
```

Good defaults the source highlights: **Nous Portal** (subscription, zero-config, OAuth login), **OpenAI Codex** (ChatGPT device-code OAuth), and **Anthropic** (Claude directly — Max plan + extra credits via OAuth, or an API key for pay-per-token). The full provider catalog — 30+ providers with their env vars and OAuth/API-key setup steps — is documented separately; see [Providers](hermes_inference_providers_cloud.md). You can switch providers at any time with `hermes model` (no lock-in).

:::caution Minimum context: 64K tokens Hermes Agent requires a model with **at least 64,000 tokens of context**. Models with smaller windows cannot maintain enough working memory for multi-step tool-calling workflows and are rejected at startup. Most hosted models (Claude, GPT, Gemini, Qwen, DeepSeek) meet this easily. For a local model, set its context size to at least 64K (e.g. `--ctx-size 65536` for llama.cpp, `-c 65536` for Ollama). :::

### How settings are stored

Hermes separates secrets from normal config:

- **Secrets and tokens** → `~/.hermes/.env`
- **Non-secret settings** → `~/.hermes/config.yaml`

The easiest way to set values correctly is through the CLI, which routes the right value to the right file automatically:

```bash
hermes config set model anthropic/claude-opus-4.6
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...
```

## 3. Run Your First Chat

Hermes ships with two terminal interfaces that share the same sessions, slash commands, and config — the classic `prompt_toolkit` CLI and a newer TUI with modal overlays, mouse selection, and non-blocking input:

```bash
hermes            # classic CLI
hermes --tui      # modern TUI (recommended)
```

You'll see a welcome banner with your model, available tools, and skills. Use a prompt that's specific and easy to verify, for example: *"Summarize this repo in 5 bullets and tell me what the main entrypoint is."*

**What success looks like:** the banner shows your chosen model/provider; Hermes replies without error; it can use a tool if needed (terminal, file read, web search); and the conversation continues normally for more than one turn. If that works, you're past the hardest part.

## 4. Verify Sessions Work

Before moving on, make sure resume works:

```bash
hermes --continue    # Resume the most recent session
hermes -c            # Short form
```

That should bring you back to the session you just had. If it doesn't, check whether you're in the same profile and whether the session actually saved. This matters later when you're juggling multiple setups or machines.

## Quick Reference

The core commands this quickstart exercises:

| Command | Description |
|---------|-------------|
| `hermes` | Start chatting |
| `hermes model` | Choose your LLM provider and model |
| `hermes tools` | Configure which tools are enabled per platform |
| `hermes setup` | Full setup wizard (configures everything at once) |
| `hermes doctor` | Diagnose issues |
| `hermes update` | Update to latest version |
| `hermes gateway` | Start the messaging gateway |
| `hermes --continue` | Resume last session |

Once the base chat is verified, continue to [Add the Next Layer](hermes_quickstart_next_layer.md) for features (terminal, slash commands, gateway, skills, MCP, voice, ACP) and the failure-mode / recovery toolkit.

**Source**: `inbox/hermes_agent_docs/getting-started/quickstart.md` · https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
**Last Updated**: 2026-06-19
**Status**: Active
