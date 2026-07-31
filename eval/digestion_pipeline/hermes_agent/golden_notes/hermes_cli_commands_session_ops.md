---
tags:
  - resource
  - documentation
  - hermes_agent
  - cli
  - commands
keywords:
  - hermes session commands
  - hermes config subcommands
  - hermes skills bundles curator memory
  - hermes kanban board
  - hermes tools prompt-size
  - hermes doctor dump debug
  - session analytics insights
  - skill management cli
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

# Hermes Agent — CLI Commands: Session, Config, Skills & Ops

## Overview

This is the **session / configuration / skills / diagnostics slice** of the Hermes `hermes <command>` terminal-command reference — one of three notes that split the large CLI Commands Reference page by command family (the other two cover the [chat/provider family](hermes_cli_commands_chat_provider.md) and the [ops/maintenance/auth family](hermes_cli_commands_ops_maintenance_auth.md)). It is a routing catalog: it enumerates each command, its subcommands, and its flags, then **links out** to the feature page that explains the underlying behavior (sessions, skills, kanban, curator, …). The reference lists the command surface; the feature note explains what the command does.

The family here covers: **analytics & inspection** (`hermes status`, `hermes sessions`, `hermes insights`), **configuration** (`hermes config`), **skills management** (`hermes skills`, `hermes bundles`, `hermes curator`, `hermes memory`, `hermes tools`), the **multi-profile collaboration board** (`hermes kanban`), and **diagnostics** (`hermes prompt-size`, `hermes doctor`, `hermes dump`, `hermes debug`). These all run against an already-installed Hermes home; provider setup and credentials live in the sibling families.

## `hermes status`, `hermes sessions`, `hermes insights`

`hermes status [--all] [--deep]` shows agent, auth, and platform status; `--all` renders a shareable redacted format and `--deep` runs slower deeper checks.

`hermes sessions <subcommand>` browses, exports, prunes, renames, and deletes the session store:

| Subcommand | Description |
|------------|-------------|
| `list` | List recent sessions. |
| `browse` | Interactive session picker with search and resume. |
| `export <output> [--session-id ID]` | Export sessions to JSONL. |
| `delete <session-id>` | Delete one session. |
| `prune` | Delete old sessions. |
| `stats` | Show session-store statistics. |
| `rename <session-id> <title>` | Set or change a session title. |

`hermes insights [--days N] [--source platform]` reports token/cost/activity analytics: `--days` (default 30) sets the window and `--source` filters by source tag such as `cli`, `telegram`, or `discord`.

## `hermes config`

`hermes config <subcommand>` shows, edits, migrates, and queries the configuration files:

| Subcommand | Description |
|------------|-------------|
| `show` | Show current config values. |
| `edit` | Open `config.yaml` in your editor. |
| `set <key> <value>` | Set a config value. |
| `path` | Print the config file path. |
| `env-path` | Print the `.env` file path. |
| `check` | Check for missing or stale config. |
| `migrate` | Add newly introduced options interactively. |

## `hermes skills`

`hermes skills <subcommand>` browses, installs, publishes, audits, and configures skills. Subcommands: `browse` (paginated registry browser), `search`, `install`, `inspect` (preview without installing), `list`, `check` (look for upstream updates), `update`, `audit` (re-scan installed hub skills), `uninstall`, `reset` (un-stick a `user_modified` bundled skill; `--restore` replaces with the bundled copy), `opt-out` / `opt-in` (stop / resume bundled-skill seeding via a `.no-bundled-skills` marker), `publish`, `snapshot` (export/import skill config), `tap` (manage custom skill sources), and `config` (interactive per-platform enable/disable).

```bash
hermes skills browse --source official
hermes skills search react --source skills-sh
hermes skills install official/migration/openclaw-migration
hermes skills install https://sharethis.chat/SKILL.md       # direct single-file SKILL.md URL
hermes skills opt-out --remove --yes                        # also delete UNMODIFIED bundled skills
hermes skills opt-in --sync                                 # undo: remove marker and re-seed now
```

Notes: `--force` overrides non-dangerous policy blocks for third-party skills but never a `dangerous` scan verdict; `--source` selects a registry (`skills-sh`, `well-known`, `browse-sh`); passing an `http(s)://…/*.md` URL installs a single-file SKILL.md (require `--name` on non-interactive surfaces when the frontmatter has none).

## `hermes bundles`, `hermes curator`, `hermes memory`

`hermes bundles <subcommand>` groups several skills under one `/<bundle-name>` slash command (storage: `~/.hermes/skill-bundles/<slug>.yaml`); invoking the bundle loads every referenced skill into one combined user message. Subcommands: `list` (default), `show <name>`, `create <name>` (`--skill` repeatable, `--description`, `--instruction`, `--force`), `delete <name>`, `reload`.

```bash
hermes bundles create backend-dev \
  --skill github-code-review --skill test-driven-development \
  --skill github-pr-workflow -d "Backend feature work"
```

`hermes curator <subcommand>` drives the auxiliary-model background task that reviews agent-created skills, prunes stale ones, consolidates overlaps, and archives obsolete skills (bundled and hub skills are never touched; archives are recoverable, auto-deletion never happens). Subcommands include `status`, `run` (`--background`, `--dry-run`), `backup`, `rollback` (`--list`, `--id <ts>`, `-y`), `pause` / `resume`, `pin <skill>` / `unpin <skill>`, `restore <skill>`, `archive <skill>`, `prune`, and `list-archived`. On a fresh install the first scheduled pass is deferred by one full `interval_hours` (7 days by default).

`hermes memory <subcommand>` sets up and manages external memory provider plugins (honcho, openviking, mem0, hindsight, holographic, retaindb, byterover, supermemory) — only one external provider can be active at a time, while built-in `MEMORY.md`/`USER.md` is always active. Subcommands: `setup`, `status`, `off`. An active external provider may register its own top-level `hermes <provider>` command (e.g. `hermes honcho`).

## `hermes tools` and `hermes kanban`

`hermes tools [--summary]` configures enabled tools per platform; `--summary` prints the current enabled-tools summary and exits, otherwise it launches the interactive per-platform tool-configuration UI.

`hermes kanban [--board <slug>] <action> [options]` is the human / scripting surface for the multi-profile, multi-project collaboration board. Each install hosts many boards (one per project/repo/domain), each a standalone queue with its own SQLite DB and dispatcher scope; the gateway-embedded dispatcher sweeps every board per tick. Agent workers instead drive the board through the dedicated `kanban_*` toolset rather than shelling out to `hermes kanban`.

| Action | Purpose |
|--------|---------|
| `init` | Create `kanban.db` if missing (idempotent). |
| `boards list` / `boards create <slug>` / `boards switch <slug>` / `boards show` / `boards rename` / `boards rm <slug>` | Board lifecycle. `rm` archives by default (`--delete` hard-deletes; refused for `default`). |
| `create "<title>"` | New task (`--body`, `--assignee`, `--parent`, `--workspace`, `--tenant`, `--priority`, `--triage`, `--idempotency-key`, `--max-runtime`, `--max-retries`, `--skill`). |
| `list` / `show <id>` / `assign <id> <profile>` / `link` / `unlink` / `claim <id>` / `comment <id>` | Task management (`assign … none` unassigns; `link` is cycle-detected). |
| `complete` / `block` / `schedule` / `unblock` / `archive` / `tail` / `context` | Task state and follow / context. |
| `dispatch` | One dispatcher pass (`--dry-run`, `--max N`, `--failure-limit N`, `--json`). |
| `specify <id>` / `decompose <id>` (`--all`) | Flesh out or fan out a triage task via the auxiliary LLM (`auxiliary.triage_specifier` / `auxiliary.kanban_decomposer`). |
| `gc` | Remove scratch workspaces for archived tasks. |

```bash
hermes kanban boards create atm10-server --name "ATM10 Server" --icon 🎮
hermes kanban --board atm10-server create "Restart server" --assignee ops
hermes kanban boards switch atm10-server
```

Board resolution order (highest precedence first): `--board <slug>` flag → `HERMES_KANBAN_BOARD` env var → `~/.hermes/kanban/current` file → `default`. Every action is also available as a `/kanban …` slash command with the same argument surface.

## `hermes prompt-size`, `hermes doctor`, `hermes dump`, `hermes debug`

`hermes prompt-size [--platform <name>] [--json]` reports the fixed per-call prompt budget for a fresh session — system-prompt total, the `<available_skills>` index (often the largest block), memory / user profile, prompt tiers (stable / context / volatile), and tool schemas. It runs entirely offline (no API call, no credentials needed). Shrink the prompt by disabling unused toolsets (`hermes tools`) or uninstalling skills (`hermes skills`).

`hermes doctor [--fix]` diagnoses config and dependency issues; `--fix` attempts automatic repairs where possible.

`hermes dump [--show-keys]` outputs a compact plain-text summary of the entire setup (version, environment, identity, model, terminal, API-key presence checks, features, services, workload, config overrides) designed to be copy-pasted into a bug report; `--show-keys` shows redacted key prefixes instead of `set`/`not set`.

`hermes debug share [options]` uploads a debug report (system info + recent logs) to a paste service and returns a shareable URL: `--lines <N>` (log lines per file, default 200), `--expire <days>` (default 7), `--local` (print locally instead of uploading). Keys are always redacted.

**Source**: `inbox/hermes_agent_docs/reference/cli-commands.md` · https://hermes-agent.nousresearch.com/docs/reference/cli-commands
**Last Updated**: 2026-06-19
**Status**: Active
