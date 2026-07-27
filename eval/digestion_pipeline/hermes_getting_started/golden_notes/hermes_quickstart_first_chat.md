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

## Related Notes

**Terms**
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the agent this page onboards; relevance: page's whole purpose is a first working chat.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: §The fastest path frames Hermes as autonomous, not a copilot.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: `hermes setup --portal`/Codex/Anthropic OAuth login covered in §2.
- [term_context_window](../../term_dictionary/term_context_window.md) — model context size; relevance: the 64K-token minimum-context caution.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — provider/model list; relevance: §2 provider table + `hermes model` picker.
- [term_llm](../../term_dictionary/term_llm.md) — underlying model; relevance: every provider row selects an LLM.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — saved sessions; relevance: §4 `hermes --continue` resume verification.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapter; relevance: each catalog row is a provider plugin.

**Code-Repos**
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI entrypoints; relevance: implements `hermes`, `hermes setup`, `hermes model`, `--tui`, `--continue` invoked throughout.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters + OAuth; relevance: backs the §2 provider catalog and `setup --portal` login.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — conversation loop + session store; relevance: runs the §3 first chat and §4 resume.
- [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — TUI front-end; relevance: implements `hermes --tui` offered in §3.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level repo; relevance: the installed package this quickstart drives end-to-end.

**Snippets**
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — `hermes setup` wizard; relevance: §1/§2 the wizard `setup --portal` invokes.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: §1 one-line install.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — OAuth login; relevance: §2 portal/Codex/Anthropic OAuth login.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — `hermes model` entry; relevance: §2 provider picker.
- [snippet_hermes_agent_cli_models_picker](../../code_snippets/snippet_hermes_agent_cli_models_picker.md) — interactive model list; relevance: §2 model selection UI.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: backs the §2 provider catalog rows.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `hermes config set`; relevance: §How settings are stored (right file routing).
- [snippet_hermes_agent_cli_hermescli_session_handlers](../../code_snippets/snippet_hermes_agent_cli_hermescli_session_handlers.md) — session handlers; relevance: §4 `--continue` resume.
- [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — session persistence; relevance: §4 saved-session verification.
- [snippet_hermes_agent_cli_main_cmd_chat](../../code_snippets/snippet_hermes_agent_cli_main_cmd_chat.md) — `hermes` chat command; relevance: §3 first chat (`hermes`/`--tui`).

**Docs**
- [hermes_installation](hermes_installation.md) — full install ref; relevance: §1 link-out.
- [hermes_quickstart_next_layer](hermes_quickstart_next_layer.md) — sibling part 2; relevance: continues after first chat.
- [hermes_learning_path](hermes_learning_path.md) — reader router; relevance: next-steps.
- [hermes_configuration](hermes_config_files_precedence.md) — config/secrets split; relevance: §How settings are stored.
- [hermes_cli_interface](hermes_cli_interface.md) — CLI/TUI guide; relevance: §3 interface choice.
- [hermes_providers](hermes_inference_providers_cloud.md) — full provider catalog; relevance: §2 table link-out.
- [cc_quickstart](../claude_code/cc_quickstart.md) — analogous agent-tool quickstart; relevance: same zero-to-working-chat arc.
- [cc_install](../claude_code/cc_install.md) — analogous install; relevance: parallel one-line install step.
- [cc_model_selection](../claude_code/cc_model_selection.md) — analogous model picker; relevance: maps to `hermes model`.
- [cc_authentication](../claude_code/cc_authentication.md) — analogous auth/OAuth; relevance: maps to `setup --portal` login.

**Source**: `inbox/hermes_agent_docs/getting-started/quickstart.md` · https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
**Last Updated**: 2026-06-19
**Status**: Active
