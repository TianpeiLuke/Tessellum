---
tags:
  - resource
  - documentation
  - hermes_agent
  - profiles
  - multi_agent
keywords:
  - hermes profile
  - HERMES_HOME
  - command alias
  - clone profile
  - profile vs sandbox
  - home_mode
  - profile lifecycle
  - multiple agents one machine
topics:
  - Hermes Agent
  - Profiles
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/profiles
access_control_group: ["general"]
---

# Profiles: Running Multiple Agents

## Overview

A **profile** is a separate Hermes home directory — a self-contained state directory holding its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and state database. Profiles let you run multiple independent Hermes agents on the same machine (a coding assistant, a personal bot, a research agent) without mixing up state, API keys, or gateway tokens. The defining mechanism is the `HERMES_HOME` environment variable: when you create a profile it automatically becomes its own command (create `coder` and you instantly have `coder chat`, `coder setup`, `coder gateway start`), because the wrapper sets `HERMES_HOME` to that profile's directory before launching Hermes and 119+ files in the codebase resolve paths via `get_hermes_home()`. This note walks the full lifecycle: create (blank / `--clone` / `--clone-all` / `--clone-from`), target (alias / `-p` flag / `hermes profile use`), the profile-vs-workspace-vs-sandbox distinction, per-profile config, update skill-sync, manage/rename/export/import/delete, tab completion, and the `HERMES_HOME` vs OS `HOME` / `home_mode` boundary.

## Quick start

```bash
hermes profile create coder       # creates profile + "coder" command alias
coder setup                       # configure API keys and model
coder chat                        # start chatting
```

`coder` is now its own Hermes profile with its own config, memory, and state. The quickest first-time setup is `hermes setup --portal` inside the new profile to wire up models and tools at once.

## Creating a profile

- **Blank** — `hermes profile create mybot` creates a fresh profile with bundled skills seeded; run `mybot setup` to configure API keys, model, and gateway tokens. If the profile will act as a kanban worker, pass `--description "<role>"` at create time so the orchestrator knows what it is good at (the full auto-vs-manual routing model is owned by the Kanban guide). The description can also be set or auto-generated later with `hermes profile describe`.
- **Clone config only (`--clone`)** — copies the current profile's `config.yaml`, `.env`, `SOUL.md`, and skills, but gives fresh sessions and memory; edit `~/.hermes/profiles/work/.env` or `.../SOUL.md` to diverge.
- **Clone everything (`--clone-all`)** — copies config, API keys, personality, all memories, skills, cron jobs, and plugins (a complete working snapshot). Per-profile history is excluded (session history, `state.db`, `backups/`, `state-snapshots/`, `checkpoints/`) because it belongs to the source profile and can reach tens of GB; for a full backup including history use `hermes profile export` or `hermes backup`.
- **Clone from a specific profile (`--clone-from <source>`)** — selects the source directly and implies a config/skills/SOUL clone; combine with `--clone-all` for a full copy (`hermes profile create work --clone-from coder --clone-all`).

When Honcho memory is enabled, clone operations automatically create a dedicated AI peer for the new profile while sharing the same user workspace, so each profile builds its own observations and identity (Honcho peer details are owned by the memory-providers doc).

## Using profiles

Every profile gets a command alias at `~/.local/bin/<name>` that works with every subcommand — it is just `hermes -p <name>` under the hood. You can target a profile three ways: the alias, the explicit `-p` / `--profile=` flag (works in any position), or a sticky default via `hermes profile use`.

```bash
coder gateway start                # alias: hermes -p coder gateway start
hermes --profile=coder doctor      # explicit flag, any position
hermes profile use coder           # sticky default — plain `hermes` now targets coder
hermes profile use default         # switch back
```

Sticky default behaves "like `kubectl config use-context`". The CLI always shows which profile is active — the prompt becomes `coder ❯` instead of `❯`, the startup banner shows `Profile: coder`, and `hermes profile` reports the current profile name, path, model, and gateway status.

## Profiles vs workspaces vs sandboxing

Profiles are often confused with workspaces or sandboxes, but they are distinct:

- A **profile** gives Hermes its own state directory (`config.yaml`, `.env`, `SOUL.md`, sessions, memory, logs, cron jobs, gateway state).
- A **workspace** / **working directory** is where terminal commands start — controlled separately by `terminal.cwd`.
- A **sandbox** is what limits filesystem access. **Profiles do not sandbox the agent.** On the default `local` terminal backend the agent has the same filesystem access as your user account; a profile does not stop it from reaching folders outside the profile directory.

To start a profile in a specific project folder, set an explicit absolute `terminal.cwd` in that profile's `config.yaml`:

```yaml
terminal:
  backend: local
  cwd: /absolute/path/to/project
```

Using `cwd: "."` on the local backend means "the directory Hermes was launched from", not "the profile directory". Also: `SOUL.md` can guide the model but does not enforce a workspace boundary; `SOUL.md` changes take effect cleanly on a new session (existing sessions may keep the old prompt state); and asking the model "what directory are you in?" is not a reliable isolation test — set `terminal.cwd` explicitly when you need a predictable starting directory. (Terminal backend and `cwd`/`home_mode` config blocks are owned by the terminal-backends doc.)

## Configuring profiles

Each profile has its own `config.yaml` (model, provider, toolsets, all settings), `.env` (API keys, bot tokens), and `SOUL.md` (personality and instructions). Configure via `coder config set ...` or by editing the files directly:

```bash
coder config set model.default anthropic/claude-sonnet-4
echo "You are a focused coding assistant." > ~/.hermes/profiles/coder/SOUL.md
coder config set terminal.cwd /absolute/path/to/project
```

From the dashboard: the machine-level web dashboard can manage **any** profile's config, API keys, skills, MCPs, and model via the profile switcher in its sidebar — no per-profile dashboard needed. `coder dashboard` routes to the machine dashboard with the `coder` profile preselected, and the Chat tab follows the switcher. "Set as active" on the dashboard's Profiles page is the sticky default for future CLI/gateway runs (same as `hermes profile use`); to edit a profile from the dashboard, use the switcher. (The dashboard profile switcher is owned by the web-dashboard doc.)

## Updating, managing, and deleting

`hermes update` pulls code once (shared across all profiles) and syncs new bundled skills to **all** profiles automatically; user-modified skills are never overwritten:

```bash
hermes update
# → Code updated (12 commits)
# → Skills synced: default (up to date), coder (+2 new), assistant (+2 new)
```

Manage and delete with the `hermes profile` command tree:

```bash
hermes profile list                  # show all profiles with status
hermes profile show coder            # detailed info for one profile
hermes profile rename coder dev-bot  # rename (updates alias + service)
hermes profile export coder          # export to coder.tar.gz
hermes profile import coder.tar.gz   # import from archive
hermes profile delete coder          # stops gateway, removes service + alias, deletes data
```

`delete` asks you to type the profile name to confirm (`--yes` skips it). You cannot delete the default profile (`~/.hermes`); to remove everything use `hermes uninstall`. Tab completion is enabled via `eval "$(hermes completion bash)"` (or `zsh`) — add the line to `~/.bashrc` / `~/.zshrc` for persistence; it completes profile names after `-p`, profile subcommands, and top-level commands.

## How it works (`HERMES_HOME` vs `HOME` / `home_mode`)

Profiles use the `HERMES_HOME` environment variable. When you run `coder chat`, the wrapper script sets `HERMES_HOME=~/.hermes/profiles/coder` before launching Hermes; since 119+ files resolve paths via `get_hermes_home()`, Hermes state automatically scopes to the profile's directory — config, sessions, memory, skills, state database, gateway PID, logs, and cron jobs. This is separate from the terminal working directory: tool execution starts from `terminal.cwd` (or the launch directory when `cwd: "."` on the local backend), not from `HERMES_HOME`.

Two things are easy to mix up:

- **`HERMES_HOME` is the profile boundary** — it controls Hermes config, `.env`, memory, sessions, skills, logs, cron jobs, and gateway state.
- **`HOME` is the OS/user home that external CLIs expect.** On host installs Hermes keeps it as the real user home by default so tools like `git`, `ssh`, `gh`, `az`, `npm`, Claude Code, and Codex find the same credentials they use in your normal shell.

The tradeoff is that host profiles share normal user-level CLI state by default. For separate CLI identities per profile, set `terminal.home_mode: profile` in that profile's `config.yaml`; Hermes then launches tool subprocesses with `HOME={HERMES_HOME}/home`, and you must initialize or link the profile-specific `~/.ssh`, `~/.gitconfig`, `~/.config/gh`, cloud CLI auth, Claude/Codex auth, npm state, etc. inside that profile home. Hermes also exposes `HERMES_REAL_HOME` to subprocesses so scripts can still find the real account home when `home_mode: profile` is active. The default profile is simply `~/.hermes` itself — no migration needed; existing installs work identically.

A profile you built on one machine can be packaged as a git repository and installed with one command elsewhere (SOUL, config, skills, cron, MCP connections; credentials/memories/sessions stay per-machine) — see the profile distributions guide.

**Source**: `inbox/hermes_agent_docs/user-guide/profiles.md` · https://hermes-agent.nousresearch.com/docs/user-guide/profiles
**Last Updated**: 2026-06-19
**Status**: Active
