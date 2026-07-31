---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - slash_commands
keywords:
  - openclaw slash command catalog
  - core built-in commands
  - dock commands
  - bundled plugin commands
  - skill commands command-dispatch tool
  - /tools /model /config /mcp /debug /plugins
  - owner-only write commands
  - /trace /btw side question
topics:
  - OpenClaw
  - Slash Commands
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/slash-commands
access_control_group: ["general"]
---

# OpenClaw — Slash Command Catalog

## Overview

This note catalogs OpenClaw's slash commands — the concrete per-command tables and the owner-only write surfaces — mirroring the **Command list** half of the `tools/slash-commands` source page plus its per-command detail sections (`/tools`, `/model`, `/config`, `/mcp`, `/debug`, `/plugins`, `/trace`, `/btw`). The complementary command MODEL (the three command types, persist-vs-inline semantics, the `commands.*` config schema, per-surface session scoping, and provider usage/status) is documented in the sibling note `oc_tools_slash_commands_model.md`; here every command is enumerated as a procedure: how to invoke it, its arguments, aliases, and what config flag (if any) it requires.

## Command Sources and Availability

Commands come from three sources: **Core built-ins** from `src/auto-reply/commands-registry.shared.ts`; **Generated dock commands** from `src/auto-reply/commands-registry.data.ts`; and **Plugin commands** registered via plugin `registerCommand()` calls. Availability of any given command depends on config flags, the channel surface, and which plugins are installed/enabled. Use `/commands` to print the generated command catalog for the current surface and `/help` for the short help summary.

## Core Commands

### Sessions and runs

| Command | Description |
| --- | --- |
| `/new [model]` | Archive the current session and start a fresh one |
| `/reset [soft [message]]` | Reset the current session in place. `soft` keeps the transcript, drops reused CLI backend session ids, and reruns startup |
| `/name <title>` | Name or rename the current session. Omit the title to see the current name and a suggestion |
| `/compact [instructions]` | Compact the session context |
| `/stop` | Abort the current run |
| `/session idle <duration\|off>` | Manage thread-binding idle expiry |
| `/session max-age <duration\|off>` | Manage thread-binding max-age expiry |
| `/export-session [path]` | Export the current session to HTML. Alias: `/export` |
| `/export-trajectory [path]` | Export a JSONL trajectory bundle for the current session. Alias: `/trajectory` |

The Control UI intercepts typed `/new` to create and switch to a fresh dashboard session, except when `session.dmScope: "main"` is configured and the current parent is the agent's main session — in that case `/new` resets the main session in place. Typed `/reset` still runs the Gateway's in-place reset. Use `/model default` to clear a pinned session model selection.

### Model and run controls

| Command | Description |
| --- | --- |
| `/think <level\|default>` | Set the thinking level or clear the session override. Aliases: `/thinking`, `/t` |
| `/verbose on\|off\|full` | Toggle verbose output. Alias: `/v` |
| `/trace on\|off` | Toggle plugin trace output for the current session |
| `/fast [status\|on\|off\|default]` | Show, set, or clear fast mode |
| `/reasoning [on\|off\|stream]` | Toggle reasoning visibility. Alias: `/reason` |
| `/elevated [on\|off\|ask\|full]` | Toggle elevated mode. Alias: `/elev` |
| `/exec host=<auto\|sandbox\|gateway\|node> security=<deny\|allowlist\|full> ask=<off\|on-miss\|always> node=<id>` | Show or set exec defaults |
| `/model [name\|#\|status]` | Show or set the model |
| `/models [provider] [page] [limit=<n>\|all]` | List configured/auth-available providers or models |
| `/queue <mode>` | Manage active-run queue behavior |
| `/steer <message>` | Inject guidance into the active run. Alias: `/tell` |

Safety notes: `/verbose` is for debugging — keep it off in normal use; `/trace` reveals only plugin-owned trace/debug lines while normal verbose chatter stays off; `/fast on|off` persists a session override (use the Sessions UI `inherit` option to clear it); `/reasoning`, `/verbose`, and `/trace` are risky in group chats because they may reveal internal reasoning or plugin diagnostics. `/model` persists the new model immediately to the session: if the agent is idle the next run uses it right away, but if a run is active the switch is marked pending and applied at the next clean retry point.

### Discovery and status

| Command | Description |
| --- | --- |
| `/help` | Show the short help summary |
| `/commands` | Show the generated command catalog |
| `/tools [compact\|verbose]` | Show what the current agent can use right now |
| `/status` | Show execution/runtime status, Gateway and system uptime, plugin health, plus provider usage/quota |
| `/status plugins` | Show detailed plugin health: load errors, quarantines, channel failures, dependency issues, compatibility notices |
| `/goal [status\|start\|pause\|resume\|complete\|block\|clear] ...` | Manage the current session's durable goal |
| `/diagnostics [note]` | Owner-only support-report flow. Asks for exec approval every time |
| `/crestodian <request>` | Run the Crestodian setup and repair helper from an owner DM |
| `/tasks` | List active/recent background tasks for the current session |
| `/context [list\|detail\|map\|json]` | Explain how context is assembled |
| `/whoami` | Show your sender id. Alias: `/id` |
| `/usage off\|tokens\|full\|cost` | Control the per-response usage footer or print a local cost summary |

### Skills, allowlists, approvals

| Command | Description |
| --- | --- |
| `/skill <name> [input]` | Run a skill by name |
| `/allowlist [list\|add\|remove] ...` | Manage allowlist entries. Text-only |
| `/approve <id> <decision>` | Resolve exec or plugin approval prompts |
| `/btw <question>` | Ask a side question without changing session context. Alias: `/side` |

### Subagents and ACP

| Command | Description |
| --- | --- |
| `/subagents list\|log\|info` | Inspect sub-agent runs for the current session |
| `/acp spawn\|cancel\|steer\|close\|sessions\|status\|set-mode\|set\|cwd\|permissions\|timeout\|model\|reset-options\|doctor\|install\|help` | Manage ACP sessions and runtime options |
| `/focus <target>` | Bind the current Discord thread or Telegram topic to a session target |
| `/unfocus` | Remove the current thread binding |
| `/agents` | List thread-bound agents for the current session |

### Owner-only writes and admin

| Command | Requires | Description |
| --- | --- | --- |
| `/config show\|get\|set\|unset` | `commands.config: true` | Read or write `openclaw.json`. Owner-only |
| `/mcp show\|get\|set\|unset` | `commands.mcp: true` | Read or write OpenClaw-managed MCP server config. Owner-only |
| `/plugins list\|inspect\|show\|get\|install\|enable\|disable` | `commands.plugins: true` | Inspect or mutate plugin state. Owner-only for writes. Alias: `/plugin` |
| `/debug show\|set\|unset\|reset` | `commands.debug: true` | Runtime-only config overrides. Owner-only |
| `/restart` | `commands.restart: true` (default) | Restart OpenClaw |
| `/send on\|off\|inherit` | owner | Set send policy |

### Voice, TTS, channel control

| Command | Description |
| --- | --- |
| `/tts on\|off\|status\|chat\|latest\|provider\|limit\|summary\|audio\|help` | Control TTS |
| `/activation mention\|always` | Set group activation mode |
| `/bash <command>` | Run a host shell command. Alias: `! <command>`. Requires `commands.bash: true` |
| `!poll [sessionId]` | Check a background bash job |
| `!stop [sessionId]` | Stop a background bash job |

## Dock Commands

Dock commands switch the active session's reply route to another linked channel. They are generated from channel plugins with native-command support: `/dock-discord` (alias `/dock_discord`), `/dock-mattermost` (alias `/dock_mattermost`), `/dock-slack` (alias `/dock_slack`), and `/dock-telegram` (alias `/dock_telegram`). Dock commands require `session.identityLinks`, and the source sender and target peer must be in the same identity group.

## Bundled Plugin Commands

| Command | Description |
| --- | --- |
| `/dreaming [on\|off\|status\|help]` | Toggle memory dreaming |
| `/pair [qr\|status\|pending\|approve\|cleanup\|notify]` | Manage device pairing |
| `/phone status\|arm ...\|disarm` | Temporarily arm high-risk phone node commands |
| `/voice status\|list\|set <voiceId>` | Manage Talk voice config. Discord native name: `/talkvoice` |
| `/card ...` | Send LINE rich card presets |
| `/codex status\|models\|threads\|resume\|compact\|review\|diagnostics\|account\|mcp\|skills` | Control the Codex app-server harness |

QQBot-only commands: `/bot-ping`, `/bot-version`, `/bot-help`, `/bot-upgrade`, `/bot-logs`.

## Skill Commands

User-invocable skills are exposed as slash commands. `/skill <name> [input]` always works as the generic entrypoint, and skills may also register as direct commands (e.g. `/prose` for OpenProse). Native skill-command registration is controlled by `commands.nativeSkills` and `channels.<provider>.commands.nativeSkills`. Command names are sanitized to `a-z0-9_` (max 32 chars), and collisions get numeric suffixes. By default a skill command routes to the model as a normal request, but a skill can declare `command-dispatch: tool` to route directly to a tool (deterministic, no model involvement) — for example `/prose` from the OpenProse plugin. For native command arguments, Discord uses autocomplete for dynamic options and button menus when required args are omitted, Telegram and Slack show a button menu for commands with choices, and dynamic choices resolve against the target session model so model-specific options like `/think` levels follow the session's `/model` override.

## `/tools` — What the Agent Can Use Now

`/tools` answers a runtime question — what this agent can use right now in this conversation — not a static config catalog. It supports `/tools` for the compact view and `/tools verbose` for short descriptions. Results are session-scoped, so changing agent, channel, thread, sender authorization, or model can change the output; for profile and override editing, use the Control UI Tools panel or config surfaces.

## `/model` — Model Selection

`/model` shows or sets the model: `/model` or `/model list` shows the picker, `/model 3` selects by number from the picker, `/model openai/gpt-5.4` or `/model opus@anthropic:default` selects an explicit model, `/model default` clears the session model selection, and `/model status` gives a detailed view with endpoint and API mode. On Discord, `/model` and `/models` open an interactive picker with provider and model dropdowns that respects `agents.defaults.models`, including `provider/*` entries.

## `/config`, `/mcp`, `/debug`, `/plugins` — Owner-Only Write Surfaces

These four write surfaces are **owner-only** and **disabled by default**; each is enabled by its respective `commands.*` flag. `/config` (enable with `commands.config: true`) reads and writes `openclaw.json` via `/config show`, `/config show <key>`, `/config get <key>`, `/config set <key>=<value>`, and `/config unset <key>`; config is validated before write, invalid changes are rejected, and `/config` updates persist across restarts. `/mcp` (enable with `commands.mcp: true`) reads and writes OpenClaw-managed MCP server config via `/mcp show`, `/mcp show <name>`, `/mcp set <name>={...}`, and `/mcp unset <name>`, storing config in OpenClaw config rather than embedded-agent project settings. `/debug` (enable with `commands.debug: true`) applies runtime-only config overrides via `/debug show`, `/debug set <key>=<value>`, `/debug unset <key>`, and `/debug reset` — overrides apply immediately to new config reads but do **not** write to disk. `/plugins` (enable with `commands.plugins: true` for writes) manages plugins via `/plugins`, `/plugins list`, `/plugin show <name>`, `/plugins enable <name>`, `/plugins disable <name>`, and `/plugins install <path>`; `/plugins enable|disable` updates plugin config and hot-reloads the Gateway plugin runtime for new agent turns, while `/plugins install` restarts managed Gateways automatically because plugin source modules changed.

## `/trace` — Plugin Trace Output

`/trace` reveals session-scoped plugin trace/debug lines without full verbose mode: `/trace` shows the current trace state, `/trace on` enables it, and `/trace off` disables it. It does not replace `/debug` (runtime overrides) or `/verbose` (normal tool output).

## `/btw` — Side Questions

`/btw` (alias `/side`) asks a quick side question about the current session context — for example `/btw what are we doing right now?` or `/side what changed while the main run continued?`. Unlike a normal message it uses the current session as background context, runs as an ephemeral Codex side thread in Codex harness sessions, does **not** change future session context, and is not written to transcript history.

**Source**: OpenClaw documentation — `tools/slash-commands` (mirror `inbox/openclaw_docs/tools/slash-commands.md`)
**Last Updated**: 2026-06-22
**Status**: Active
