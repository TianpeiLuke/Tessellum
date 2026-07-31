---
tags:
  - resource
  - documentation
  - hermes_agent
  - cli_commands
  - navigation
keywords:
  - hermes auth credentials
  - hermes cron webhook hooks
  - hermes mcp acp plugins
  - hermes backup checkpoints logs
  - hermes update postinstall uninstall
  - hermes send whatsapp slack
topics:
  - Hermes Agent
  - CLI Commands
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/reference/cli-commands
access_control_group: ["general"]
---

# Hermes Agent — CLI Commands: Ops, Maintenance & Auth

## Overview

This is the **ops/maintenance/auth slice** of the Hermes `hermes <command>` terminal reference — the command-surface catalog for everything that manages credentials, event/automation surfaces, backups and lifecycle, rather than the chat/provider launch (its own note) or session/skills/kanban management (its own note). It enumerates each command, its subcommands, and its flags so you can answer "what command does X" without reading the feature page; the feature behavior itself lives in the owning feature note (the reference lists the command surface, the feature note explains the behavior). Concretely this note covers: credential + secret commands (`auth`, `secrets`, `pairing`), the event/automation surfaces (`cron`, `webhook`, `hooks`, `mcp`, `acp`, `plugins`), backup/checkpoint/log/migrate ops (`backup`, `import`, `checkpoints`, `logs`, `migrate`), messaging ops (`send`, `whatsapp`, `slack`), and lifecycle (`update`, `postinstall`, `uninstall`, `completion`, `dashboard`, `computer-use`, `claw`). All commands are invoked under the global `hermes [global-options] <command>` entrypoint documented in the chat/provider note. The `hermes login`/`logout` commands are **deprecated** — use `hermes auth`.

## `hermes auth`

Manages **credential pools** for same-provider key rotation and OAuth credentials (Codex/Nous/Anthropic). With no subcommand it launches the interactive management wizard. Subcommands: `add`, `list`, `remove`, `reset`, `status`, `logout`, `spotify`.

```bash
hermes auth                                              # Interactive wizard
hermes auth list                                         # Show all pools
hermes auth list openrouter                              # Show specific provider
hermes auth add openrouter --api-key sk-or-v1-xxx        # Add API key
hermes auth add anthropic --type oauth                   # Add OAuth credential
hermes auth remove openrouter 2                          # Remove by index
hermes auth reset openrouter                             # Clear cooldowns
hermes auth status anthropic                             # Show auth status for a provider
hermes auth logout anthropic                             # Log out and clear stored auth state
hermes auth spotify                                      # Authenticate Hermes with Spotify via PKCE
```

**`hermes login` / `hermes logout` are deprecated/removed** — use `hermes auth` to manage OAuth credentials, `hermes model` to select a provider, or `hermes setup` for full interactive setup.

## `hermes secrets`

Pulls API keys from an external secret manager at process startup instead of from `~/.hermes/.env`. Currently supports **Bitwarden Secrets Manager**; subcommands are under `bitwarden` (alias `bw`).

| `bitwarden`/`bw` subcommand | Description |
|---|---|
| `setup` | Interactive wizard: install the pinned `bws` binary, store an access token, pick a project. Accepts `--project-id`, `--access-token`, `--server-url` for non-interactive use. |
| `status` | Show current config, binary path/version, last fetch info. |
| `sync` | Fetch secrets now and report changes. `--apply` exports them into the current shell (default is dry-run). |
| `install` | Download and verify the pinned `bws` binary. `--force` re-downloads. |
| `disable` | Turn off the Bitwarden integration. |

## `hermes pairing`

Approve or revoke messaging pairing codes. `hermes pairing <list|approve|revoke|clear-pending>`: `list` shows pending and approved users; `approve <platform> <code>` approves a pairing code; `revoke <platform> <user-id>` revokes a user's access; `clear-pending` clears pending pairing codes.

## `hermes cron`

Inspect and tick the cron scheduler. `hermes cron <list|create|edit|pause|resume|run|remove|status|tick>`: `list` shows scheduled jobs; `create`/`add` creates a job from a prompt (attach skills via repeated `--skill`); `edit` updates schedule/prompt/name/delivery/repeat/skills (`--clear-skills`, `--add-skill`, `--remove-skill`); `pause`/`resume` toggle a job; `run` triggers on the next tick; `remove` deletes a job; `status` checks whether the scheduler is running; `tick` runs due jobs once and exits. The cron **trigger** is pluggable via the `cron.provider` config key — empty uses the built-in in-process ticker, `chronos` uses the NAS-managed provider for scale-to-zero hosted gateways (`cron.chronos.*` keys), or a custom provider under `plugins/cron/<name>/`; an unknown/unavailable provider falls back to built-in so cron is never left without a trigger.

## `hermes webhook`

Manage dynamic webhook subscriptions for event-driven agent activation. `hermes webhook <subscribe|list|remove|test>`: `subscribe`/`add` creates a route (returns URL + HMAC secret); `list`/`ls` shows agent-created subscriptions; `remove`/`rm` deletes a dynamic subscription (static config routes unaffected); `test` sends a test POST. `hermes webhook subscribe <name>` options:

| Option | Description |
|---|---|
| `--prompt` | Prompt template with `{dot.notation}` payload references. |
| `--events` | Comma-separated event types to accept (empty = all). |
| `--deliver` | Delivery target: `log` (default), `telegram`, `discord`, `slack`, `github_comment`. |
| `--deliver-only` | Skip the agent — deliver the rendered `--prompt` as the literal message (zero LLM cost). |

Subscriptions persist to `~/.hermes/webhook_subscriptions.json`, hot-reloaded without a gateway restart.

## `hermes hooks`

Inspect shell-script hooks declared in `~/.hermes/config.yaml`, test them against synthetic payloads, and manage the first-use consent allowlist. `list`/`ls` lists configured hooks with matcher/timeout/consent status; `test <event>` fires every hook matching `<event>` against a synthetic payload; `revoke`/`remove`/`rm` removes a command's allowlist entries (effective next restart); `doctor` checks each hook (exec bit, allowlist, mtime drift, JSON validity, synthetic run timing).

## `hermes mcp`

Manage MCP (Model Context Protocol) server configurations and run Hermes as an MCP server.

| Subcommand | Description |
|---|---|
| *(none)* / `picker` | Interactive catalog picker — browse Nous-approved MCPs and install/enable/disable. |
| `catalog` | List Nous-approved MCPs (scriptable plain text). |
| `install <name>` | Install a catalog entry (e.g. `hermes mcp install n8n`). |
| `serve [-v\|--verbose]` | Run Hermes as an MCP server — expose conversations to other agents. |
| `add <name> [--url URL] [--command CMD] [--auth oauth\|header] [--args ...]` | Add a custom MCP server with automatic tool discovery. `--args` passes remaining argv to the stdio command, so put it last. |
| `remove <name>` (alias `rm`) | Remove an MCP server from config. |
| `list` (alias `ls`) | List configured MCP servers. |
| `test <name>` | Test connection to an MCP server. |
| `configure <name>` (alias `config`) | Toggle tool selection for a server. |
| `login <name>` | Force re-authentication for an OAuth-based MCP server. |

## `hermes acp` & `hermes plugins`

`hermes acp` starts Hermes as an ACP (Agent Client Protocol) stdio server for editor integration. Related entrypoints `hermes-acp` and `python -m acp_adapter`; install support first with `pip install -e '.[acp]'`.

`hermes plugins [subcommand]` is unified plugin management (general plugins, memory providers, context engines). No subcommand opens a composite interactive screen.

| Subcommand | Description |
|---|---|
| *(none)* | Composite interactive UI — general plugin toggles + provider plugin configuration. |
| `install <identifier> [--force]` | Install from a Git URL or `owner/repo`. |
| `update <name>` | Pull latest changes for an installed plugin. |
| `remove <name>` (aliases `rm`, `uninstall`) | Remove an installed plugin. |
| `enable <name>` / `disable <name>` | Enable a disabled plugin / disable without removing. |
| `list` (alias `ls`) | List installed plugins with enabled/disabled status. |

Provider selections save to `config.yaml` (`memory.provider`, `context.engine`); the general disabled list lives under `plugins.disabled`.

## `hermes migrate`, `hermes claw` & `hermes computer-use`

`hermes migrate <type>` diagnoses and (optionally) rewrites the active `config.yaml` to replace retired models / deprecated settings; a timestamped backup is taken before any rewrite (skip with `--no-backup`). The `xai` subcommand scans for xAI models scheduled for retirement (May 15, 2026) and with `--apply` rewrites them in-place (defaults to dry-run). Not to be confused with `hermes claw migrate`.

`hermes claw migrate [options]` migrates an OpenClaw setup to Hermes — reads `~/.openclaw` (auto-detects legacy `~/.clawdbot`/`~/.moltbot`) and writes `~/.hermes`. Covers 30+ categories; items are directly imported or archived for manual review.

| `claw migrate` option | Description |
|---|---|
| `--dry-run` | Preview what would be migrated without writing anything. |
| `--preset <name>` | `full` (all compatible settings) or `user-data` (excludes infra config). Neither imports secrets. |
| `--migrate-secrets` | Include API keys (required even under `--preset full`). |
| `--overwrite` | Overwrite existing Hermes files on conflicts (default: refuse on conflict). |
| `--source <path>` | Custom OpenClaw directory (default `~/.openclaw`). |
| `--yes` | Skip the confirmation prompt. |

`hermes computer-use <install|status>` installs/checks the cua-driver backend (macOS Computer Use): `install` runs the upstream cua-driver installer, `install --upgrade` re-runs even if already on PATH, `status` prints PATH/version. `hermes update` re-runs the installer automatically if cua-driver is on PATH.

## `hermes backup`, `hermes import` & `hermes checkpoints`

`hermes backup [options]` creates a zip of config/skills/sessions/data (excludes the hermes-agent codebase). Uses SQLite's `backup()` API so it is WAL-safe while Hermes runs.

```bash
hermes backup                                # Full backup to ~/hermes-backup-*.zip
hermes backup -o /tmp/hermes.zip             # Full backup to specific path
hermes backup --quick                        # Quick state-only snapshot
hermes backup --quick --label "pre-upgrade"  # Quick snapshot with label
```

Options: `-o`/`--output <path>`, `-q`/`--quick` (critical state only), `-l`/`--label <name>` (with `--quick`). Excluded: `*.db-wal`/`*.db-shm`/`*.db-journal` sidecars, `checkpoints/`, and the code itself.

`hermes import <zipfile> [-f|--force]` restores a backup; all archive files overwrite existing files, and `--force` only skips the existing-installation confirmation prompt. Stop the gateway before importing.

`hermes checkpoints [COMMAND]` inspects/manages the shadow git store at `~/.hermes/checkpoints/` (the storage behind `/rollback`): `status` (default; total size, project count, per-project breakdown), `list` (alias for status), `prune` (force cleanup sweep — delete orphan/stale projects, GC, enforce size cap), `clear` (delete the entire base; `-f` skips confirm), `clear-legacy` (delete only v1→v2 `legacy-<ts>/` archives). Prune flags: `--retention-days N` (default 7), `--max-size-mb N` (default 500), `--keep-orphans`.

## `hermes logs`

View, tail, and filter agent/gateway/error log files stored in `~/.hermes/logs/`. `hermes logs [log_name] [options]` — log names: `agent` (default, `agent.log`), `errors`, `gateway`, `gui`, `desktop`, or `list`. Options: `-n`/`--lines <N>` (default 50), `-f`/`--follow` (tail -f), `--level <DEBUG|INFO|WARNING|ERROR|CRITICAL>`, `--session <ID>`, `--since <30m|1h|2d>`, `--component <gateway|agent|tools|cli|cron>`. Filters combine with AND. Uses `RotatingFileHandler`, so `hermes logs list` shows rotated files (`agent.log.1`, …).

## `hermes send`, `hermes whatsapp` & `hermes slack`

`hermes send` posts a one-shot message to a configured platform with no agent loop and no LLM — reuses the gateway's credentials so ops scripts/cron/CI/monitoring can post status. For bot-token platforms (Telegram, Discord, Slack, Signal, SMS, WhatsApp-CloudAPI) no running gateway is needed. Options: `-t`/`--to <TARGET>` (`platform`, `platform:chat_id`, `platform:#channel`), `-f`/`--file <PATH>` (text only; `MEDIA:<path>` in the message body delivers binary attachments), `-s`/`--subject <LINE>`, `-l`/`--list [platform]`, `-q`/`--quiet`, `--json`. Exit codes: `0` success, `1` delivery failure, `2` usage error.

`hermes whatsapp` runs the WhatsApp pairing/setup flow (mode selection + QR-code pairing). `hermes slack manifest [--write|--slashes-only]` generates a Slack app manifest registering every `COMMAND_REGISTRY` command as a native slash command (Discord/Telegram parity); re-run after `hermes update`.

## `hermes update`, Maintenance & `hermes completion`

`hermes update [--gateway] [--check] [--no-backup] [--backup] [--yes]` pulls the latest `hermes-agent` code and reinstalls dependencies, then re-runs post-install hooks. It auto-detects pip vs git installs (pip → `pip install --upgrade hermes-agent`; git → pull the update branch, default `main`). `--check` previews without installing, `--backup` snapshots `HERMES_HOME` first (default off). After a successful update it auto-restarts running gateway profiles. Exit codes: `0` success, `1` pull/install errors, `2` blocking working-tree changes.

Maintenance commands: `hermes version` (print version), `hermes postinstall` (internal bootstrap — installs non-Python deps Node.js/headless browser/ripgrep/ffmpeg, then triggers `hermes setup` if unconfigured; idempotent), and `hermes uninstall [--full] [--gui] [--yes]` (`--gui` removes only the desktop Chat GUI, `--full` also deletes config/data, `--yes` skips prompts).

`hermes completion [bash|zsh|fish]` prints a shell completion script to stdout for tab-completion of commands, subcommands, and profile names — source it from your shell profile (full completion surface is this command; profile-aware completions are covered in the profile-commands reference).

## `hermes dashboard`

`hermes dashboard [options]` launches the browser-based UI for managing config, API keys, and monitoring sessions (requires `pip install hermes-agent[web]`; the embedded Chat tab also needs the `pty` extra + a POSIX PTY). Options: `--port` (default `9119`), `--host` (default `127.0.0.1`), `--no-open`, `--insecure` (allow non-localhost binding), `--isolated` (per-profile server), `--stop`, `--status`.

**Source**: `inbox/hermes_agent_docs/reference/cli-commands.md` · https://hermes-agent.nousresearch.com/docs/reference/cli-commands
**Last Updated**: 2026-06-19
**Status**: Active
