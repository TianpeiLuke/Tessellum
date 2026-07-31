---
tags:
  - resource
  - documentation
  - hermes_agent
  - faq
  - troubleshooting
keywords:
  - hermes faq install
  - llm provider selection
  - command not found path
  - api key rate limiting
  - context length exceeded
  - docker terminal backend
topics:
  - Hermes Agent
  - FAQ & Troubleshooting
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/reference/faq
access_control_group: ["general"]
---

# Hermes Agent — FAQ & Troubleshooting (Install, Provider & Terminal)

## Overview

This is the **first half of the Hermes FAQ & Troubleshooting reference** — the common setup questions plus the installation, provider/model, and terminal/Docker troubleshooting fixes. It answers "which LLM providers work", OS support (Windows native + WSL2, Android/Termux), data privacy, running offline/local, cost, multi-user access, the memory-vs-skills distinction, and embedding Hermes in a Python project; then it gives the step-by-step fixes for the first-run failure modes — `hermes: command not found` (PATH reload), Python-version-too-old, missing `node`/`nvm`/`pyenv` in the terminal snapshot, `uv: command not found`, permission-denied-during-install (no-sudo cleanup), `/model` only showing one provider, API-key/model-not-found errors, 429 rate limiting, context-length-exceeded (`/compress`), dangerous-command approval, `sudo` over the messaging gateway, and the Docker-backend group fix. The operate/scale half — messaging-gateway, performance, MCP troubleshooting, profiles, and workflow recipes — lives in the companion note `hermes_faq_messaging_perf_profiles_workflows`. Provider/model concepts, install steps, and terminal-backend configuration each have feature pages this FAQ links into; this note is the quick-answer enumeration. The kept command blocks below are reproduced verbatim from the source; the remaining short blocks are summarized in prose.

## Frequently Asked Questions

**What LLM providers work with Hermes?** Hermes works with any OpenAI-compatible API. Supported providers include **OpenRouter** (hundreds of models through one key, recommended for flexibility), **Nous Portal** (Nous Research's subscription gateway — 300+ models plus web/image/TTS/browser through one OAuth login, recommended for newcomers), **OpenAI** (GPT-5.4, GPT-5-codex, GPT-4.1, GPT-4o), **Anthropic** (Claude direct API, OAuth via `hermes auth add anthropic`, OpenRouter, or any compatible proxy), **Google** (Gemini via the `gemini` provider, the `google-gemini-cli` OAuth provider, OpenRouter, or proxy), **z.ai / ZhipuAI** (GLM), **Kimi / Moonshot AI**, **MiniMax** (global and China endpoints), and **local models** via Ollama, vLLM, llama.cpp, SGLang, or any OpenAI-compatible server. Set your provider with `hermes model` or by editing `~/.hermes/.env`; see the env-vars reference for all provider keys.

**Does it work on Windows?** Yes, natively — Hermes supports native Windows via the PowerShell installer (no WSL required); the installer provisions a PortableGit that backs the terminal tool's shell. WSL2 remains a fully supported alternative using the standard `install.sh` command.

**WSL2 + normal Windows Chrome?** Prefer an MCP bridge over `/browser connect`: run Hermes inside WSL2, keep using your signed-in Windows Chrome, add `chrome-devtools-mcp` as an MCP server through `cmd.exe` / `powershell.exe`, and let Hermes use the resulting MCP browser tools — more reliable than forcing the core browser transport across the WSL2/Windows boundary.

**Android / Termux?** Yes — Hermes has a tested Termux install path for Android phones (use the standard `install.sh`). Caveat: the full `.[all]` extra is not available on Android because the `voice` extra depends on `faster-whisper` → `ctranslate2`, which publishes no Android wheels; use the tested `.[termux]` extra instead.

**Is my data sent anywhere?** API calls go **only to the LLM provider you configure** (e.g. OpenRouter, your local Ollama). Hermes collects no telemetry, usage data, or analytics; conversations, memory, and skills are stored locally in `~/.hermes/`.

**Offline / local models?** Yes. Run `hermes model`, select **Custom endpoint**, and enter your server's URL, API key, model name, and context length (the Hermes minimum is 64000 — set it to match your server's actual context window). Or set it directly in `config.yaml`:

```yaml
model:
  default: qwen3.5:27b
  provider: custom
  base_url: http://localhost:11434/v1
```

Hermes persists the endpoint/provider/base-URL so it survives restarts; if your local server has exactly one model loaded, `/model custom` auto-detects it. Works with Ollama, vLLM, llama.cpp, SGLang, LocalAI, and others. Tips: if you set a custom `num_ctx` in Ollama, match the context length in Hermes (Ollama's `/api/show` reports the *maximum*, not the effective `num_ctx`); Hermes auto-relaxes streaming timeouts for local endpoints (read timeout 120s → 1800s, stale-stream detection disabled), and you can set `HERMES_STREAM_READ_TIMEOUT=1800` if you still hit timeouts on very large contexts.

**How much does it cost?** Hermes itself is **free and open-source** (MIT license); you pay only for LLM API usage from your chosen provider. Local models are free to run.

**Can multiple people use one instance?** Yes — the messaging gateway lets multiple users interact with one Hermes instance via Telegram, Discord, Slack, WhatsApp, or Home Assistant. Access is controlled through allowlists (specific user IDs) and DM pairing (first user to message claims access).

**Memory vs skills?** **Memory** stores **facts** (things the agent knows about you, your projects, preferences), retrieved automatically by relevance; **skills** store **procedures** (step-by-step instructions for how to do things), recalled when the agent meets a similar task. Both persist across sessions.

**Use it in your own Python project?** Yes — import the `AIAgent` class and use Hermes programmatically:

```python
from run_agent import AIAgent

agent = AIAgent(model="anthropic/claude-opus-4.7")
response = agent.chat("Explain quantum computing briefly")
```

## Troubleshooting — Installation Issues

**`hermes: command not found` after installation** — Cause: your shell hasn't reloaded the updated PATH. Solution: re-source your profile (`source ~/.bashrc` for bash, `source ~/.zshrc` for zsh) or open a new terminal; if it still fails, verify the install location with `which hermes` and `ls ~/.local/bin/hermes`. The installer adds `~/.local/bin` to PATH; for non-standard shell configs add `export PATH="$HOME/.local/bin:$PATH"` manually.

**Python version too old** — Cause: Hermes requires Python 3.11 or newer. Solution: check `python3 --version`, then install a newer Python (`sudo apt install python3.12` on Ubuntu/Debian, `brew install python@3.12` on macOS). The installer handles this automatically — upgrade Python first if you see this error during a manual install.

**Terminal commands say `node: command not found` (or `nvm`, `pyenv`, `asdf`, …)** — Cause: Hermes builds a per-session environment snapshot by running `bash -l` once at startup; a bash login shell reads `/etc/profile`, `~/.bash_profile`, and `~/.profile` but **does not source `~/.bashrc`**, so tools that install themselves there stay invisible (common under systemd or a minimal shell). Solution: Hermes auto-sources `~/.bashrc` by default; if that isn't enough (e.g. a zsh user whose PATH lives in `~/.zshrc`, or `nvm` from a standalone file), list extra files in `~/.hermes/config.yaml`:

```yaml
terminal:
  shell_init_files:
    - ~/.zshrc                     # zsh users: pulls zsh-managed PATH into the bash snapshot
    - ~/.nvm/nvm.sh                # direct nvm init (works regardless of shell)
    - /etc/profile.d/cargo.sh      # system-wide rc files
  # When this list is set, the default ~/.bashrc auto-source is NOT added —
  # include it explicitly if you want both:
  #   - ~/.bashrc
  #   - ~/.zshrc
```

Missing files are skipped silently; sourcing happens in bash, so zsh-only-syntax files may error (source just the PATH-setting portion, e.g. `nvm.sh`, if so). To disable auto-source entirely (strict login-shell semantics), set `terminal.auto_source_bashrc: false`.

**`uv: command not found`** — Cause: the `uv` package manager isn't installed or not in PATH. Solution: install it with `curl -LsSf https://astral.sh/uv/install.sh | sh` then `source ~/.bashrc`.

**Permission denied errors during install** — Cause: insufficient permissions to write to the install directory. Solution: **do not use `sudo` with the installer** — it installs to `~/.local/bin`. If you previously installed with sudo, clean up and re-run the standard installer:

```bash
# Don't use sudo with the installer — it installs to ~/.local/bin
# If you previously installed with sudo, clean up:
sudo rm /usr/local/bin/hermes
# Then re-run the standard installer
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

## Troubleshooting — Provider & Model Issues

**`/model` only shows one provider / can't switch providers** — Cause: `/model` (inside a chat session) can only switch between providers you've **already configured**; if you've only set up OpenRouter, that's all it shows. Solution: exit the session and run `hermes model` from your terminal to add providers (run OAuth, enter API keys, configure endpoints), then start a new chat — `/model` will list all configured providers. Quick reference: add a provider or enter/change API keys → `hermes model` (from terminal); switch model mid-session → `/model <name>`; switch to a different configured provider → `/model provider:model` (inside session).

**API key not working** — Cause: the key is missing, expired, incorrectly set, or for the wrong provider. Solution: inspect with `hermes config show`, re-configure with `hermes model`, or set it directly with `hermes config set OPENROUTER_API_KEY sk-or-v1-xxxxxxxxxxxx`. Make sure the key matches the provider (an OpenAI key won't work with OpenRouter and vice versa); check `~/.hermes/.env` for conflicting entries.

**Model not available / model not found** — Cause: the model identifier is incorrect or not available on your provider. Solution: list available models with `hermes model`, set a valid one with `hermes config set HERMES_MODEL anthropic/claude-opus-4.7`, or specify it per-session with `hermes chat --model openrouter/meta-llama/llama-3.1-70b-instruct`.

**Rate limiting (429 errors)** — Cause: you've exceeded your provider's rate limits. Solution: wait and retry; for sustained usage, upgrade your provider plan, switch to a different model/provider, or route to a different backend with `hermes chat --provider <alternative>`.

**Context length exceeded** — Cause: the conversation has grown too long for the model's context window, or Hermes detected the wrong context length. Solution: compress the current session, start fresh, or use a larger-context model:

```bash
# Compress the current session
/compress

# Or start a fresh session
hermes chat

# Use a model with a larger context window
hermes chat --model openrouter/google/gemini-3-flash-preview
```

If this happens on the first long conversation, Hermes may have the wrong context length — the CLI startup line shows the detected limit (e.g. `📊 Context limit: 128000 tokens`), and `/usage` shows it during a session. To fix detection, set `model.context_length` explicitly in `~/.hermes/config.yaml`, or for custom endpoints add a per-model `context_length` under `custom_providers`.

## Troubleshooting — Terminal Issues

**Command blocked as dangerous** — Cause: Hermes detected a potentially destructive command (e.g. `rm -rf`, `DROP TABLE`) — a safety feature. Solution: when prompted, review the command and type `y` to approve it; you can also ask the agent for a safer alternative. Hermes never silently runs destructive commands — the approval prompt shows exactly what will execute.

**`sudo` not working via messaging gateway** — Cause: the messaging gateway runs without an interactive terminal, so `sudo` cannot prompt for a password. Solution: avoid `sudo` in messaging (ask the agent for alternatives), configure passwordless sudo for specific commands in `/etc/sudoers`, or switch to the terminal interface (`hermes chat`) for administrative tasks.

**Docker backend not connecting** — Cause: the Docker daemon isn't running or the user lacks permissions. Solution: verify the daemon and add your user to the `docker` group:

```bash
# Check Docker is running
docker info

# Add your user to the docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker run hello-world
```

**Source**: `inbox/hermes_agent_docs/reference/faq.md` · https://hermes-agent.nousresearch.com/docs/reference/faq
**Last Updated**: 2026-06-19
**Status**: Active
