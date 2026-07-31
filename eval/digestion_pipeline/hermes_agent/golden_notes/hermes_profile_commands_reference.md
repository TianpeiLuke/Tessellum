---
tags:
  - resource
  - documentation
  - hermes_agent
  - profiles
  - cli
keywords:
  - hermes profile commands
  - profile distribution install update info
  - distribution.yaml manifest
  - hermes -p profile override
  - profile export import clone
  - profile describe kanban routing
  - profile shell completion
topics:
  - Hermes Agent
  - Profile Commands Reference
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/reference/profile-commands
access_control_group: ["general"]
---

# Hermes Agent — Profile Commands Reference

## Overview

This note is the **command-surface catalog for Hermes profiles** — every `hermes profile` subcommand, the distribution commands that ship a profile via git, the `-p`/`--profile` global override, and the profile-aware shell completions. A Hermes profile is an isolated agent instance with its own config, sessions, skills, memories, and auth; this page enumerates how you create, inspect, move, share, and switch between them. It is a pure reference table that maps the command surface down to the `cli_*` implementation snippets and links the profile **concept** out to the SP04 profiles feature notes (the reference lists the command; the feature note explains the behavior). For general CLI commands see [CLI Commands Reference](hermes_cli_commands_chat_provider.md); the `hermes completion` listing here is the profile-completion subset of the full completion command in [Ops / Maintenance / Auth](hermes_cli_commands_ops_maintenance_auth.md).

The surface splits into four groups: **profile management** (`list`/`use`/`create`/`describe`/`delete`/`show`/`alias`/`rename`/`export`/`import`), **distributions** (`install`/`update`/`info` + the `distribution.yaml` manifest + private distributions + publishing), the **`-p`/`--profile` per-command override**, and **shell completion** for profile names and subcommands.

## `hermes profile`

`hermes profile <subcommand>` is the top-level command for managing profiles; running it without a subcommand shows help. The subcommands:

| Subcommand | Description |
|------------|-------------|
| `list` | List all profiles (active marked `*`). |
| `use` | Set the active (default) profile. |
| `create` | Create a new profile. |
| `describe` | Read or set a profile's description (used by the kanban orchestrator for routing). |
| `delete` | Delete a profile. |
| `show` | Show details about a profile. |
| `alias` | Regenerate the shell alias for a profile. |
| `rename` | Rename a profile. |
| `export` | Export a profile to a tar.gz archive. |
| `import` | Import a profile from a tar.gz archive. |
| `install` | Install a profile distribution from a git URL or local directory. |
| `update` | Re-pull a distribution-managed profile and re-apply its bundle. |
| `info` | Show distribution metadata for a profile (origin URL, commit, last update). |

- **`list`** — lists all profiles; the active one is marked with `*`. No options.
- **`use <name>`** — sets `<name>` as the active profile (all subsequent `hermes` commands without `-p` use it); `default` returns to the base profile.
- **`show <name>`** — displays a profile's Hermes home directory, configured model, gateway status, skills count, and config-file status. This is the Hermes home directory, *not* the terminal working directory (terminal commands start from `terminal.cwd`).
- **`rename <old-name> <new-name>`** — renames a profile, updating both the directory and the shell alias.

## `hermes profile create` and `describe`

`hermes profile create <name> [options]` creates a new profile. Creating a profile does **not** make its directory the default working directory — set `terminal.cwd` in that profile's `config.yaml` to start in a specific project.

| Argument / Option | Description |
|-------------------|-------------|
| `<name>` | Name for the new profile (alphanumeric, hyphens, underscores). |
| `--clone` | Copy `config.yaml`, `.env`, `SOUL.md`, and skills from the current profile. |
| `--clone-all` | Copy everything (config, memories, skills, cron, plugins) from the current profile. Excludes per-profile history (sessions, `state.db`, backups, state-snapshots, checkpoints). |
| `--clone-from <profile>` | Clone config/skills/SOUL from a specific profile. Implies `--clone` unless paired with `--clone-all`. |
| `--no-alias` | Skip wrapper script creation. |
| `--description "<text>"` | One- or two-sentence description used by the kanban orchestrator to route by role, not name. Persisted in `<profile_dir>/profile.yaml`. |
| `--no-skills` | Create an **empty** profile with zero bundled skills; writes a `.no-bundled-skills` marker so future `hermes update` won't re-seed; refuses to combine with `--clone*`. |

```bash
# Blank profile, clone config only, clone everything, clone from a named profile
hermes profile create mybot
hermes profile create work --clone
hermes profile create backup --clone-all
hermes profile create work2 --clone-from work
```

`hermes profile describe [<name>] [options]` reads or sets a profile's description, which the kanban orchestrator consumes to route tasks by capability rather than name. With no flags it prints the current description. `--text "<text>"` sets it explicitly; `--auto` auto-generates a 1-2 sentence description via the `auxiliary.profile_describer` LLM (marked `description_auto: true`); `--overwrite` replaces user-authored ones; `--all` sweeps every profile missing a description.

```bash
hermes profile describe researcher --text "Reads source code and writes findings."
hermes profile describe --all --auto   # fill in every profile missing one
```

`hermes profile delete <name>` removes a profile and its alias (`--yes`/`-y` skips the prompt). This permanently deletes the entire profile directory (config, memories, sessions, skills) and **cannot delete the currently active profile**. `hermes profile alias <name>` regenerates the wrapper script at `~/.local/bin/<name>` (`--remove` deletes it; `--name <alias>` uses a custom name).

## `hermes profile export` / `import`

`hermes profile export <name> [-o <path>]` writes a profile as a compressed tar.gz (default `<name>.tar.gz`, e.g. `hermes profile export work -o ./work-2026-03-29.tar.gz`); `hermes profile import <archive> [--name <name>]` restores one (name inferred from the archive unless overridden, e.g. `hermes profile import ./work.tar.gz --name work-restored`). These are the right commands for **local backup and restore** on your own machine — distinct from distributions, which ship a profile to *someone else* via git.

## Distribution commands

Distributions turn a profile into a shareable, versioned artifact published as a **git repository**: a recipient installs it with one command and can update in place later without touching their local memories, sessions, or credentials. `auth.json` and `.env` are never part of a distribution — they stay on the installing user's machine — and the recipient's user data is always preserved across install and updates.

- **`hermes profile install <source> [--name <name>] [--alias] [--force] [--yes]`** — installs from a git URL (`github.com/user/repo`, `https://…`, `git@…`, `ssh://`, `git://`) or a local directory containing `distribution.yaml`. The installer shows the manifest, lists required env vars, and warns about cron jobs before confirming; required env vars go into a `.env.EXAMPLE` you copy to `.env`. `--alias` also creates a shell wrapper; `--force` overwrites an existing same-name profile (user data still preserved); `-y`/`--yes` skips the preview prompt.
- **`hermes profile update <name> [--force-config] [--yes]`** — re-clones the distribution from its recorded source and applies updates. Distribution-owned files (`SOUL.md`, `skills/`, `cron/`, `mcp.json`) are overwritten; user data (memories, sessions, auth, `.env`) is never touched. `config.yaml` is preserved by default; `--force-config` resets it to the shipped config.
- **`hermes profile info <name>`** — prints the distribution manifest (name, version, required Hermes version, author, env-var requirements, source URL/path, and the `Installed:` timestamp). `hermes profile list` also shows a `Distribution` column; `show`/`delete` surface the source URL.

```bash
hermes profile install github.com/kyle/telemetry-distribution --alias
hermes profile install git@github.com:your-org/internal-assistant.git   # private: uses your SSH key
```

**Private distributions** work with no extra config — install shells out to your normal `git` binary, so existing SSH keys, `git credential` helpers, or GitHub CLI HTTPS credentials apply transparently; interactive credential prompts flow through.

Every distribution has a `distribution.yaml` at its repository root:

```yaml
name: telemetry
version: 0.1.0
description: "Compliance monitoring harness"
hermes_requires: ">=0.12.0"
author: "Your Name"
license: "MIT"
env_requires:
  - name: OPENAI_API_KEY
    description: "OpenAI API key"
    required: true
  - name: GRAPHITI_MCP_URL
    description: "Memory graph URL"
    required: false
    default: "http://127.0.0.1:8000/sse"
distribution_owned:   # optional; defaults to SOUL.md, config.yaml,
                      #   mcp.json, skills/, cron/, distribution.yaml
  - SOUL.md
  - skills/compliance/
  - cron/
```

`hermes_requires` supports `>=`, `<=`, `==`, `!=`, `>`, `<`, or a bare version (treated as `>=`); install fails with a clear error if the current Hermes version doesn't satisfy the spec. `distribution_owned` is optional — if set, only those paths are replaced on update; otherwise the listed defaults apply. **Publishing** is just a git push: create `distribution.yaml` with at least `name` and `version`, initialize/push a git repo, and tell recipients to run `hermes profile install <your-repo-url>`. Use git tags for versioned releases.

## `hermes -p` / `hermes --profile`

`hermes -p <name> <command>` (or `hermes --profile <name> <command>`) runs any Hermes command under a specific profile **without** changing the sticky default — it overrides the active profile for the duration of that one command only.

```bash
hermes -p work chat -q "Check the server status"
hermes --profile dev gateway start
hermes -p personal skills list
```

## `hermes completion`

`hermes completion <shell>` generates shell completion scripts (`bash`, `zsh`, or `fish`), including completions for profile names and profile subcommands. (This is the profile-completion subset; the general command lives in [Ops / Maintenance / Auth](hermes_cli_commands_ops_maintenance_auth.md).)

```bash
hermes completion bash >> ~/.bashrc
hermes completion zsh >> ~/.zshrc
hermes completion fish > ~/.config/fish/completions/hermes.fish
```

After installation, tab completion works for `hermes profile <TAB>` (subcommands), `hermes profile use <TAB>` (profile names), and `hermes -p <TAB>` (profile names).

**Source**: https://hermes-agent.nousresearch.com/docs/reference/profile-commands
**Last Updated**: 2026-06-19
**Status**: Active
