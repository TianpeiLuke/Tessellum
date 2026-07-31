---
tags:
  - resource
  - documentation
  - hermes_agent
  - cli
  - commands
keywords:
  - hermes cli command reference
  - hermes chat one-shot
  - hermes model provider selector
  - hermes gateway lsp setup portal
  - hermes proxy fallback security
  - global entrypoint options
topics:
  - Hermes Agent
  - CLI Reference
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/reference/cli-commands
access_control_group: ["general"]
---

# Hermes Agent — CLI Commands: Chat & Provider Family

## Overview

This is the **command-reference catalog** for the chat/provider/gateway family of the `hermes` terminal CLI: the global `hermes [opts] <cmd>` entrypoint plus the commands that launch the agent, pick the provider/model, run OAuth, and stand up the messaging front-end. It is the first of three notes that split the large `cli-commands.md` reference page by command family (this note + [session/ops](hermes_cli_commands_session_ops.md) + [ops/maintenance/auth](hermes_cli_commands_ops_maintenance_auth.md)). It is a reference/navigation surface, not a feature deep-dive: each command's *behavior* is owned by its feature page (provider routing, the Tool Gateway, the messaging gateway), which this note links out to — the reference lists the command surface; the feature note explains the behavior. For the in-chat slash-command surface, see [interactive CLI slash commands](hermes_slash_commands_interactive_cli.md).

The commands covered here are: the global entrypoint and its global flags, the top-level command index, then `hermes chat` (+ the `hermes -z` scripted one-shot), `hermes model` (vs the in-session `/model`), `hermes gateway`, `hermes lsp`, `hermes setup` (+ `--portal`), `hermes portal`, `hermes proxy`, `hermes fallback`, and `hermes security`.

## Global entrypoint

```bash
hermes [global-options] <command> [subcommand/options]
```

Global options apply before the command and to every invocation:

| Option | Description |
|--------|-------------|
| `--version`, `-V` | Show version and exit. |
| `--profile <name>`, `-p <name>` | Select which Hermes profile to use for this invocation. Overrides the sticky default set by `hermes profile use` (see [profile reference](hermes_profile_commands_reference.md)). |
| `--resume <session>`, `-r <session>` | Resume a previous session by ID or title. |
| `--continue [name]`, `-c [name]` | Resume the most recent session, or the most recent matching a title. |
| `--worktree`, `-w` | Start in an isolated git worktree for parallel-agent workflows. |
| `--yolo` | Bypass dangerous-command approval prompts. |
| `--pass-session-id` | Include the session ID in the agent's system prompt. |
| `--ignore-user-config` | Ignore `~/.hermes/config.yaml`, fall back to built-in defaults (`.env` credentials still load). |
| `--ignore-rules` | Skip auto-injection of `AGENTS.md`, `SOUL.md`, `.cursorrules`, memory, and preloaded skills. |
| `--tui` / `--cli` | Force the TUI or the classic prompt_toolkit REPL (overrides `display.interface`). |
| `--dev` | With `--tui`: run the TypeScript sources via `tsx` instead of the prebuilt bundle. |

## Top-level commands

The page opens with a master index of every `hermes <command>`. The chat/provider family (this note) is `chat` · `model` · `fallback` · `gateway` · `proxy` · `lsp` · `setup` · `whatsapp` · `slack` · `portal` · `security`. The remaining commands route to the sibling notes: the session/config/skills/tools/kanban family → [session/ops](hermes_cli_commands_session_ops.md); the auth/secrets/cron/mcp/acp/backup/checkpoint/update/messaging family → [ops/maintenance/auth](hermes_cli_commands_ops_maintenance_auth.md); the `profile`/`completion` family → [profile reference](hermes_profile_commands_reference.md).

## `hermes chat`

Invocation: `hermes chat [options]`. The everyday entry point — interactive or one-shot chat. Bare `hermes` is equivalent to `hermes chat`. Key options: `-q`/`--query "…"` (one-shot, non-interactive prompt), `-m`/`--model <model>` (override the model for this run), `-t`/`--toolsets <csv>` (enable a comma-separated toolset set), `--provider <provider>` (force a provider — `auto`, `openrouter`, `nous`, `anthropic`, `openai-codex`, `gemini`, `xai`, `bedrock`, `ollama-cloud`, and ~40 others), `-s`/`--skills <name>` (preload skills), `-v`/`--verbose`, `-Q`/`--quiet` (suppress banner/spinner/tool previews), `--image <path>`, `--resume`/`--continue`, `--worktree`, `--checkpoints` (filesystem checkpoints before destructive file changes), `--yolo`, `--ignore-user-config`, `--ignore-rules`, `--safe-mode` (disable ALL customizations to isolate setup-vs-Hermes bugs), `--source <tag>` (session source tag, default `cli`), and `--max-turns <N>` (default 90).

```bash
hermes chat -q "Summarize the latest PRs"
hermes chat --provider openrouter --model anthropic/claude-sonnet-4.6
hermes chat --toolsets web,terminal,skills
hermes chat --worktree -q "Review this repo and open a PR"
hermes chat --safe-mode -q "Is this bug mine or Hermes'?"
```

### `hermes -z <prompt>` — scripted one-shot

For programmatic callers (shell scripts, CI, cron, parent processes piping in a prompt), `hermes -z` is the purest one-shot entry point: **single prompt in, final response text out, nothing else on stdout or stderr** — no banner, spinner, tool previews, or `Session:` line.

```bash
hermes -z "What's the capital of France?"          # → Paris.
answer=$(hermes -z "summarize this" < /path/to/file.txt)
```

Per-run overrides (no mutation to `config.yaml`): `-m`/`--model <model>` (≡ env `HERMES_INFERENCE_MODEL`) and `--provider <provider>`. Same agent/tools/skills as `chat`, just stripped of every interactive layer; use `hermes chat -q` instead when you also need tool output in the transcript.

## `hermes model`

Run `hermes model` (no subcommand) for the interactive provider + model selector — **the command for adding new providers, setting up API keys, and running OAuth flows** (OpenRouter, Anthropic, Copilot, Codex, Nous Portal, DeepSeek, custom endpoints). Run it from the terminal, not from inside an active session.

**`hermes model` vs `/model` — the difference:** `hermes model` (run from the terminal, outside a session) is the **full provider setup wizard** — it adds providers, runs OAuth, prompts for API keys, configures endpoints. The in-session **`/model`** slash command can only **switch between providers/models already set up** (see [interactive CLI slash commands](hermes_slash_commands_interactive_cli.md)); it cannot add providers or run OAuth. To add a provider, exit the session (`Ctrl+C` / `/quit`) and run `hermes model`. Provider setup behavior is owned by the inference-providers / Nous Portal feature docs.

## `hermes gateway`

Invocation: `hermes gateway <subcommand>`. Run or manage the messaging gateway service (the gateway *behavior* — platforms, routing — is owned by the messaging sub-plan). Subcommands: `run` (foreground; recommended for WSL/Docker/Termux), `start`/`stop`/`restart`/`status` (manage the installed systemd/launchd service), `list` (all profiles + whether each gateway is running, with PID), `install`/`uninstall` (install/remove the background service), `setup` (interactive messaging-platform setup). Options: `--all` (act on every profile's gateway on `start`/`restart`/`stop`) and `--no-supervise` (opt out of s6-overlay auto-supervision inside Docker). On WSL, prefer `hermes gateway run` (wrap in tmux) over `start`.

## `hermes lsp`

Invocation: `hermes lsp <subcommand>`. Manage the Language Server Protocol integration — runs real language servers (pyright, gopls, rust-analyzer, …) in the background and feeds diagnostics into the post-write check used by `write_file`/`patch` (gated on git-workspace detection). Subcommands: `status` (service state + configured servers), `list` (registry of supported servers; `--installed-only`), `install <id>` (eagerly install one server's binary), `install-all`, `restart` (tear down clients so the next edit re-spawns), `which <id>` (resolved binary path).

## `hermes setup`

```bash
hermes setup [model|tts|terminal|gateway|tools|agent] [--non-interactive] [--reset] [--quick] [--reconfigure] [--portal]
```

Interactive setup wizard. **Easiest path:** `hermes setup --portal` — OAuth into Nous Portal and opt into the Tool Gateway in one shot. First run launches the first-time wizard; a returning (already-configured) user drops straight into the reconfigure wizard (each prompt pre-fills the current value). Jump into one section with the positional arg (`model`/`terminal`/`gateway`/`tools`/`agent`). Options: `--quick` (only prompt for missing/unset items), `--non-interactive` (use defaults/env without prompts), `--reset` (reset to defaults first), `--reconfigure` (backwards-compat alias; bare `hermes setup` now does this by default), `--portal` (one-shot Nous Portal OAuth + Tool Gateway).

## `hermes portal`

Invocation: `hermes portal [status|open|tools]`. Inspect Nous Portal auth and Tool Gateway routing. Subcommand-less invocation runs `status`. Subcommands: `status` (default — portal auth state + per-tool Tool Gateway routing summary), `open` (open `portal.nousresearch.com/manage-subscription` in the browser), `tools` (list every Tool Gateway partner — Firecrawl, FAL, OpenAI TTS, Browser Use, Modal — and which are routed via Nous). The gateway itself is configured via the Tool Gateway feature docs / `hermes setup --portal`.

## `hermes proxy`

Invocation: `hermes proxy <subcommand>`. Run a local OpenAI-compatible HTTP server that forwards requests to an OAuth-authenticated upstream (e.g. Nous Portal, xAI): external apps point at the proxy with any bearer token; the proxy attaches your real OAuth credentials on the way out. Subcommands: `start` (foreground; flags `--provider <nous|xai>` default `nous`, `--host` default `127.0.0.1` (use `0.0.0.0` for LAN), `--port` default `8645`), `status` (which upstreams are ready), `providers` (list available upstreams). The Subscription Proxy behavior is owned by the provider/credential sub-plan.

## `hermes fallback`

Invocation: `hermes fallback <subcommand>`. Manage the fallback provider chain — providers tried in order when the primary model fails with rate-limit, overload, or connection errors. Subcommands: `list` (alias `ls`, default — show the current chain), `add` (pick a provider + model using the same picker as `hermes model` and append to the chain), `remove` (alias `rm` — pick an entry to delete), `clear` (remove all fallback entries). The fallback-routing behavior is owned by the provider sub-plan.

## `hermes security`

Invocation: `hermes security audit [flags]`. On-demand supply-chain vulnerability scan against [OSV.dev](https://osv.dev) — covers the Hermes venv (installed PyPI distributions), Python dependencies declared by plugins under `~/.hermes/plugins/`, and pinned `npx`/`uvx` MCP servers in `config.yaml` (does NOT scan globally-installed packages or editor/browser extensions). `audit` flags: `--json` (machine-readable), `--fail-on <level>` (exit non-zero at `low`/`moderate`/`high`/`critical`; default `critical`), `--skip-venv`, `--skip-plugins`, `--skip-mcp`. The deeper security-audit posture is owned by the checkpoints/security sub-plan.

> **Deprecated:** `hermes login` / `hermes logout` have been removed — use `hermes auth` (see [ops/maintenance/auth](hermes_cli_commands_ops_maintenance_auth.md)) for credentials, `hermes model` to select a provider, or `hermes setup` for full interactive setup.

**Source**: `inbox/hermes_agent_docs/reference/cli-commands.md` · https://hermes-agent.nousresearch.com/docs/reference/cli-commands
**Last Updated**: 2026-06-19
**Status**: Active
