---
tags:
  - resource
  - documentation
  - hermes_agent
  - configuration
  - cli
keywords:
  - hermes config files
  - configuration precedence
  - config.yaml env auth.json
  - environment variable substitution
  - hermes config commands
  - working directory resolution
topics:
  - Hermes Agent
  - Configuration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
access_control_group: ["general"]
---

# Hermes Agent — Config Files & Precedence

## Overview

This note is the configuration foundation for Hermes Agent: where settings live, how they are resolved, and how to manage them. Everything Hermes reads at runtime is stored under the `~/.hermes/` home directory — `config.yaml` for non-secret settings, `.env` for secrets, and `auth.json` for OAuth credentials. Settings are resolved through a fixed 4-level precedence chain (CLI arguments > `config.yaml` > `.env` > built-in defaults), `config.yaml` values may reference environment variables with `${VAR}` substitution, and the `hermes config` command family views/edits/sets/checks/migrates the files. This page covers the directory layout, the `hermes config` commands, the precedence chain, env-var substitution rules, `updates.*` behavior, and per-context working-directory resolution. The feature-specific setting clusters (terminal backends, model/provider, runtime/context, messaging/media, security/skill/memory) live in their own sibling notes.

## Directory Structure

All settings are stored in the `~/.hermes/` directory for easy access.

```text
~/.hermes/
├── config.yaml     # Settings (model, terminal, TTS, compression, etc.)
├── .env            # API keys and secrets
├── auth.json       # OAuth provider credentials (Nous Portal, etc.)
├── SOUL.md         # Primary agent identity (slot #1 in system prompt)
├── memories/       # Persistent memory (MEMORY.md, USER.md)
├── skills/         # Agent-created skills (managed via skill_manage tool)
├── cron/           # Scheduled jobs
├── sessions/       # Gateway sessions
└── logs/           # Logs (errors.log, gateway.log — secrets auto-redacted)
```

The source notes the easiest path to a working `config.yaml`: run `hermes setup --portal` — one OAuth gets you a model provider and all four Tool Gateway tools without hand-editing YAML (Portal subscribers also get 10% off token-billed providers; see the Nous Portal integration page).

## Managing Configuration

The `hermes config` command family views and edits the files:

```bash
hermes config              # View current configuration
hermes config edit         # Open config.yaml in your editor
hermes config set KEY VAL  # Set a specific value
hermes config check        # Check for missing options (after updates)
hermes config migrate      # Interactively add missing options

# Examples:
hermes config set model anthropic/claude-opus-4
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...  # Saves to .env
```

Per the source, `hermes config set` automatically routes values to the right file — API keys are saved to `.env`, everything else to `config.yaml`. `hermes config check` reports options missing after an update, and `hermes config migrate` interactively adds them.

## Configuration Precedence

Settings are resolved in this order (highest priority first):

1. **CLI arguments** — e.g., `hermes chat --model anthropic/claude-sonnet-4` (per-invocation override)
2. **`~/.hermes/config.yaml`** — the primary config file for all non-secret settings
3. **`~/.hermes/.env`** — fallback for env vars; **required** for secrets (API keys, tokens, passwords)
4. **Built-in defaults** — hardcoded safe defaults when nothing else is set

Rule of thumb (verbatim from source): secrets (API keys, bot tokens, passwords) go in `.env`. Everything else (model, terminal backend, compression settings, memory limits, toolsets) goes in `config.yaml`. When both are set, `config.yaml` wins for non-secret settings.

For org deployments, an administrator can pin specific config and secret values that a standard user cannot override, via a system-level managed directory (see the Managed Scope page — the link-out for the org-pinned managed configuration).

## Environment Variable Substitution

You can reference environment variables in `config.yaml` using `${VAR_NAME}` syntax:

```yaml
auxiliary:
  vision:
    api_key: ${GOOGLE_API_KEY}
    base_url: ${CUSTOM_VISION_URL}

delegation:
  api_key: ${DELEGATION_KEY}
```

Substitution rules, per the source:

- Multiple references in a single value work: `url: "${HOST}:${PORT}"`.
- If a referenced variable is not set, the placeholder is kept verbatim (`${UNDEFINED_VAR}` stays as-is).
- Only the `${VAR}` syntax is supported — bare `$VAR` is not expanded.

For AI provider setup (OpenRouter, Anthropic, Copilot, custom endpoints, self-hosted LLMs, fallback models, etc.), the source points to the AI Providers page. The `providers.<id>.*timeout*` knobs documented just below this section in the source are covered in the sibling [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) note (link-out — not duplicated here).

## Update Behavior

`hermes update` settings live under `updates` in `config.yaml`:

```yaml
updates:
  pre_update_backup: false       # Create a full HERMES_HOME zip before every update
  backup_keep: 5                 # Keep this many pre-update backup zips
  non_interactive_local_changes: stash  # stash | discard
```

For git installs, Hermes auto-stashes dirty tracked files and untracked files before checking out the update branch or pulling. Interactive terminal updates prompt before restoring that stash. Non-interactive updates (desktop/chat app, gateway, or `--yes`) use `updates.non_interactive_local_changes`: `stash` restores local source edits after a successful pull, while `discard` drops the update-created stash after a successful pull. Use `discard` only on managed installs where local source edits are never meant to persist.

Before that stash step, Hermes also restores tracked `package-lock.json` diffs left by npm install/build churn. Commit or manually stash intentional lockfile edits before updating. (The `hermes update` mechanics themselves are owned by SP01's getting-started/updating note — link-out.)

## Working Directory

Hermes' working directory is resolved per execution context:

| Context | Default |
|---------|---------|
| **CLI (`hermes`)** | Current directory where you run the command |
| **Messaging gateway** | `terminal.cwd` from `~/.hermes/config.yaml`; if unset, home directory `~` |
| **Docker / Singularity / Modal / SSH** | User's home directory inside the container or remote machine |

Override the working directory:

```yaml
# In ~/.hermes/config.yaml:
terminal:
  cwd: /home/myuser/projects
```

`MESSAGING_CWD` and direct `TERMINAL_CWD` entries in `~/.hermes/.env` are legacy compatibility fallbacks. New configurations should use `terminal.cwd`.

**Source**: `inbox/hermes_agent_docs/user-guide/configuration.md` · https://hermes-agent.nousresearch.com/docs/user-guide/configuration
**Last Updated**: 2026-06-19
**Status**: Active
