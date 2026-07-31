---
tags:
  - resource
  - documentation
  - hermes_agent
  - cli
  - slash_commands
keywords:
  - hermes interactive cli slash commands
  - command_registry autocomplete
  - dynamic skill slash commands
  - quick commands
  - custom model aliases
  - alias resolution prefix matching
  - admin user command split
topics:
  - Hermes Agent
  - CLI Reference
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/reference/slash-commands
access_control_group: ["general"]
---

# Hermes Agent — Interactive CLI Slash Commands

## Overview

This is the reference catalog for the **interactive CLI slash-command surface** — the in-chat `/command` menu you reach by typing `/` in the Hermes CLI. Hermes has two slash-command surfaces, both driven by a single central `COMMAND_REGISTRY` in `hermes_cli/commands.py`: the **interactive CLI** surface dispatched by `cli.py` (with autocomplete pulled from the registry), and the **messaging** surface dispatched by `gateway/run.py` (cataloged in the sibling note [hermes_slash_commands_messaging](hermes_slash_commands_messaging.md)). Installed skills are also exposed as dynamic `/<skill-name>` commands on both surfaces — including bundled skills like `/plan`, which opens plan mode and saves markdown plans under `.hermes/plans/` relative to the active workspace.

This note lists the command surface (names, grouping, key arguments) and the registry/permission/alias rules that govern it; it does **not** re-explain the behavior the commands drive — the goal loop, voice mode, skills, kanban, and config each have their own feature page (linked under Related Notes). Built-in commands are **case-insensitive**.

## Permissions and admin/user split

Every messaging platform with a per-user allowlist (Telegram, Discord, Slack, Matrix, Mattermost, Signal, …) also supports a two-tier slash-command split that the registry honors: **admins** get every registered command, while **regular users** only get the names listed in `user_allowed_commands` (plus the always-allowed floor `/help` and `/whoami`). Configure `allow_admin_from` and `user_allowed_commands` (and the per-group equivalents `group_allow_admin_from` / `group_user_allowed_commands`) inside each platform's `extra:` block in `~/.hermes/gateway-config.yaml`. If `allow_admin_from` is unset for a scope, that scope stays in unrestricted backward-compat mode — every allowed user can run every command. Per-platform ACL examples live in the messaging platform docs.

## Interactive CLI slash commands

Type `/` to open the autocomplete menu. The built-in commands are grouped in five families:

**Session** — manage conversation state and flow:

| Command | What it does |
|---------|--------------|
| `/new [name]` (alias `/reset`) | Start a fresh session (new ID + history); `[name]` sets the title; append `now`/`--yes`/`-y` to skip the confirm modal. |
| `/clear` | Clear screen and start a new session. |
| `/history`, `/save`, `/title` | Show history, save the conversation, set the session title. |
| `/retry`, `/undo` | Resend the last message; remove the last user/assistant exchange. |
| `/compress [here [N] \| focus topic]` | Manually compress context (flush memories + summarize); `here [N]` keeps the most recent N exchanges (default 2) verbatim. |
| `/rollback [number]` | List or restore filesystem checkpoints. |
| `/snapshot [create\|restore <id>\|prune]` (alias `/snap`) | Create/restore/prune Hermes config-and-state snapshots. |
| `/stop`, `/queue <prompt>` (alias `/q`), `/steer <prompt>` | Kill background processes; queue a prompt for next turn; inject a mid-run note after the next tool call (no interrupt). |
| `/goal <text>`, `/subgoal <text>` | Set a standing goal (the Ralph loop) with a judge-checked DONE/CONTINUE budget (`goals.max_turns`, default 20); append/list/remove mid-loop criteria. |
| `/resume [name]`, `/sessions` (TUI alias `/switch`), `/branch [name]` (alias `/fork`) | Resume a named session; browse/switch sessions; branch the current session. |
| `/status`, `/agents` (alias `/tasks`), `/redraw` | Show session info + local **Session recap** (no LLM call); list active agents/tasks; force a UI repaint. |
| `/background <prompt>` (alias `/bg`, `/btw`) | Run a prompt in a separate background session. |
| `/handoff <platform>` | **CLI only** — hand the session off to a messaging platform; the gateway re-binds it to your `session_id`. |

**Configuration** — `/config`, `/model [model-name]`, `/codex-runtime`, `/personality`, `/verbose`, `/fast [normal\|fast\|status]`, `/reasoning`, `/skin`, `/statusbar` (alias `/sb`), `/voice [on\|off\|tts\|status]`, `/yolo`, `/footer`, `/busy [queue\|steer\|interrupt\|status]`, `/indicator`. Notably, `/model` can only switch between **already-configured** providers (and accepts `provider:model`, `custom:…`, and user aliases, with `--global` to persist) — to add a new provider, exit and run `hermes model` from the terminal.

**Tools & Skills** — `/tools [list\|disable\|enable]`, `/toolsets`, `/browser [connect\|disconnect\|status]`, `/skills` (search/install/inspect + the write-approval review surface: `/skills pending\|diff <id>\|approve <id>\|reject <id>\|approval on\|off`), `/memory [pending\|approve\|reject\|approval]`, `/bundles`, `/cron`, `/curator`, `/kanban <action>` (the full board surface: `list`/`show`/`create`/`comment`/`unblock`/`dispatch` plus multi-board `boards …`), `/reload-mcp`, `/reload-skills`, `/reload`, `/plugins`.

**Info** — `/help`, `/version`, `/usage`, `/insights`, `/platforms` (alias `/gateway`), `/platform <list\|pause\|resume>`, `/paste`, `/copy [number]`, `/image <path>`, `/debug`, `/profile`, `/gquota`.

**Exit** — `/quit` (also `/exit`).

> The CLI prompts before the destructive commands `/clear`, `/new` / `/reset`, `/undo`, and `/exit --delete` / `/quit --delete` (three-choice modal, with inline `now`/`--yes`/`-y` skip and the `approvals.destructive_slash_confirm` toggle) — documented in detail in [hermes_slash_commands_messaging](hermes_slash_commands_messaging.md).

## Dynamic CLI slash commands

Beyond the built-ins, every installed skill is exposed as an on-demand `/<skill-name>` command:

| Command | What it does |
|---------|--------------|
| `/<skill-name>` | Load any installed skill as a command — e.g. `/gif-search`, `/github-pr-workflow`, `/excalidraw`. |
| `/skills …` | Search, browse, inspect, install, audit, publish, and configure skills from registries and the official optional-skills catalog. |

## Quick Commands

User-defined quick commands map a short slash command to a shell command (`type: exec`) or another slash command (`type: alias`). Configure them under `quick_commands:` in `~/.hermes/config.yaml`:

```yaml
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
  deploy:
    type: exec
    command: scripts/deploy.sh
  inbox:
    type: alias
    target: /gmail unread
```

Then type `/status`, `/deploy`, or `/inbox` in the CLI or a messaging platform. Quick commands resolve at dispatch time and may not appear in every built-in autocomplete/help table. **String-only prompt shortcuts are not supported** — put longer reusable prompts in a skill, or use `type: alias` to point at an existing slash command.

## Custom model aliases

Define short names for models you use often, then reach them with `/model <alias>` in the CLI or any messaging platform. Aliases work identically on both surfaces, for session-only (default) and `--global` switches. **Full form** pins an exact model, provider, and optional base URL in `~/.hermes/config.yaml`:

```yaml
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  grok:
    model: grok-4
    provider: x-ai
  ollama-qwen:
    model: qwen3-coder:30b
    provider: custom
    base_url: http://localhost:11434/v1
```

**Short form** uses `provider/model` in one string, set from the shell without editing YAML:

```bash
hermes config set model.aliases.fav anthropic/claude-opus-4.6
hermes config set model.aliases.grok x-ai/grok-4
```

User aliases take precedence over built-in short names (an alias named `sonnet`, `kimi`, or `opus` shadows the built-in), and alias names are case-insensitive.

## Alias Resolution

Commands support **prefix matching**: typing `/h` resolves to `/help`, `/mod` resolves to `/model`. When a prefix is ambiguous (matches multiple commands), the **first match in registry order** wins. Full command names and registered aliases always take priority over prefix matches.

**Source**: `inbox/hermes_agent_docs/reference/slash-commands.md` · https://hermes-agent.nousresearch.com/docs/reference/slash-commands
**Last Updated**: 2026-06-19
**Status**: Active
