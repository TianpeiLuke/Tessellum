---
tags:
  - resource
  - documentation
  - hermes_agent
  - lifecycle_hooks
  - extensibility
keywords:
  - event hooks
  - gateway hooks
  - plugin hooks
  - shell hooks
  - HOOK.yaml handler.py
  - hooks emit lifecycle events
topics:
  - Hermes Agent
  - Event Hooks
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
access_control_group: ["general"]
---

# Hermes Agent — Event Hooks

## Overview

Event hooks are Hermes' mechanism for running **custom code at key lifecycle points** — logging activity, sending alerts, posting to webhooks, intercepting tool calls, injecting context, or enforcing guardrails — without editing the agent core. Hermes ships **three distinct hook systems**, each registered differently, running in a different scope, and aimed at a different use case:

| System | Registered via | Runs in | Use case |
|--------|---------------|---------|----------|
| **Gateway hooks** | `HOOK.yaml` + `handler.py` in `~/.hermes/hooks/` | Gateway only | Logging, alerts, webhooks |
| **Plugin hooks** | `ctx.register_hook()` in a plugin | CLI + Gateway | Tool interception, metrics, guardrails |
| **Shell hooks** | `hooks:` block in `~/.hermes/config.yaml` pointing at shell scripts | CLI + Gateway | Drop-in scripts for blocking, auto-formatting, context injection |

The unifying invariant across all three: **every system is non-blocking — errors in any hook are caught and logged, never crashing the agent.** This note is the conceptual model for the three systems plus the gateway and shell configuration surfaces. The 14 plugin-hook callback signatures (the `pre_tool_call … transform_llm_output` reference) and the gateway BOOT.md / shell-hook worked examples live in the companion procedure note [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md).

## Gateway Event Hooks

Gateway hooks fire automatically during gateway operation (Telegram, Discord, Slack, WhatsApp, Teams) without blocking the main agent pipeline. They are gateway-only — the CLI does not load them.

### Creating a Hook

Each hook is a directory under `~/.hermes/hooks/` containing two files — a `HOOK.yaml` declaring which events to listen for, and a `handler.py` with the Python handler function:

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # Declares which events to listen for
    └── handler.py     # Python handler function
```

```yaml
name: my-hook
description: Log all agent activity to a file
events:
  - agent:start
  - agent:end
  - agent:step
```

```python
async def handle(event_type: str, context: dict):
    """Called for each subscribed event. Must be named 'handle'."""
    ...
```

The `events` list determines which events trigger the handler; any combination is allowed, including wildcards like `command:*`. **Handler rules:** the function must be named `handle`; it receives `event_type` (string) and `context` (dict); it can be `async def` or regular `def` (both work); and errors are caught and logged, never crashing the agent.

### Available Events

| Event | When it fires | Context keys |
|-------|---------------|--------------|
| `gateway:startup` | Gateway process starts | `platforms` (list of active platform names) |
| `session:start` | New messaging session created | `platform`, `user_id`, `session_id`, `session_key` |
| `session:end` | Session ended (before reset) | `platform`, `user_id`, `session_key` |
| `session:reset` | User ran `/new` or `/reset` | `platform`, `user_id`, `session_key` |
| `agent:start` | Agent begins processing a message | `platform`, `user_id`, `session_id`, `message` |
| `agent:step` | Each iteration of the tool-calling loop | `platform`, `user_id`, `session_id`, `iteration`, `tool_names` |
| `agent:end` | Agent finishes processing | `platform`, `user_id`, `session_id`, `message`, `response` |
| `command:*` | Any slash command executed | `platform`, `user_id`, `command`, `args` |

**Wildcard matching:** handlers registered for `command:*` fire for any `command:` event (`command:model`, `command:reset`, etc.), so a single subscription can monitor all slash commands. (Worked gateway-hook examples — the Telegram long-task alert, command-usage logger, session webhook, and the BOOT.md startup-checklist tutorial — are in [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md).)

### How It Works

1. On gateway startup, `HookRegistry.discover_and_load()` scans `~/.hermes/hooks/`.
2. Each subdirectory with `HOOK.yaml` + `handler.py` is loaded dynamically.
3. Handlers are registered for their declared events.
4. At each lifecycle point, `hooks.emit()` fires all matching handlers.
5. Errors in any handler are caught and logged — a broken hook never crashes the agent.

> Gateway hooks only fire in the **gateway** (Telegram, Discord, Slack, WhatsApp, Teams). The CLI does not load gateway hooks. For hooks that work everywhere, use plugin hooks (registered via `ctx.register_hook()`).

## Plugin Hooks (system boundary)

Plugins can register hooks that fire in **both CLI and gateway** sessions, registered programmatically via `ctx.register_hook()` inside the plugin's `register()` function. They are the cross-surface, in-process hook system. Two of the plugin hooks' return values affect behavior — `pre_tool_call` can **block** a tool, and `pre_llm_call` can **inject context** into the LLM call — while all others are fire-and-forget observers. General rule: callbacks receive **keyword arguments**, so always accept `**kwargs` for forward compatibility, and a crashing callback is logged and skipped without breaking the agent. The 14-hook callback reference (signatures, fires-when, return contracts) is the procedure note [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md).

## Shell Hooks

Shell hooks let you declare shell-script hooks in `config.yaml` and have Hermes run them as **subprocesses** whenever the corresponding plugin-hook event fires — in both CLI and gateway sessions, with **no Python plugin authoring required**. Use them for a drop-in, single-file script (Bash, Python, anything with a shebang) to block a tool call, run after a tool call (auto-format, log, trigger CI), inject context into the next LLM turn, or observe lifecycle events. They are registered by calling `agent.shell_hooks.register_from_config(cfg)` at both CLI startup (`hermes_cli/main.py`) and gateway startup (`gateway/run.py`), and they compose naturally with Python plugin hooks — both flow through the same dispatcher.

### Comparison at a glance

| Dimension | Shell hooks | Plugin hooks | Gateway hooks |
|-----------|-------------|--------------|---------------|
| Declared in | `hooks:` block in `~/.hermes/config.yaml` | `register()` in a `plugin.yaml` plugin | `HOOK.yaml` + `handler.py` directory |
| Lives under | `~/.hermes/agent-hooks/` (by convention) | `~/.hermes/plugins/<name>/` | `~/.hermes/hooks/<name>/` |
| Language | Any (Bash, Python, Go binary, …) | Python only | Python only |
| Runs in | CLI + Gateway | CLI + Gateway | Gateway only |
| Events | `VALID_HOOKS` (incl. `subagent_stop`) | `VALID_HOOKS` | Gateway lifecycle (`gateway:startup`, `agent:*`, `command:*`) |
| Can block a tool call | Yes (`pre_tool_call`) | Yes (`pre_tool_call`) | No |
| Can inject LLM context | Yes (`pre_llm_call`) | Yes (`pre_llm_call`) | No |
| Consent | First-use prompt per `(event, command)` pair | Implicit (Python plugin trust) | Implicit (dir trust) |
| Inter-process isolation | Yes (subprocess) | No (in-process) | No (in-process) |

### Configuration schema

```yaml
hooks:
  <event_name>:                  # Must be in VALID_HOOKS
    - matcher: "<regex>"         # Optional; used for pre/post_tool_call only
      command: "<shell command>" # Required; runs via shlex.split, shell=False
      timeout: <seconds>         # Optional; default 60, capped at 300

hooks_auto_accept: false         # See "Consent model" below
```

Event names must be one of the plugin hook events; typos produce a "Did you mean X?" warning and are skipped. Unknown keys inside a single entry are ignored; a missing `command` is a skip-with-warning; `timeout > 300` is clamped with a warning.

### JSON wire protocol

Each time the event fires, Hermes spawns a subprocess for every matching hook (matcher permitting), pipes a JSON payload to **stdin**, and reads **stdout** back as JSON.

```json
{
  "hook_event_name": "pre_tool_call",
  "tool_name":       "terminal",
  "tool_input":      {"command": "rm -rf /"},
  "session_id":      "sess_abc123",
  "cwd":             "/home/user/project",
  "extra":           {"task_id": "...", "tool_call_id": "..."}
}
```

`tool_name` and `tool_input` are `null` for non-tool events (`pre_llm_call`, `subagent_stop`, session lifecycle). The `extra` dict carries all event-specific kwargs (`user_message`, `conversation_history`, `child_role`, `duration_ms`, …); unserialisable values are stringified rather than omitted. On **stdout**, a script may return a block directive (`{"decision": "block", "reason": …}` Claude-Code style or `{"action": "block", "message": …}` Hermes-canonical — both accepted and normalised), a context injection (`{"context": …}` for `pre_llm_call`), or any empty/non-matching output for a silent no-op. Malformed JSON, non-zero exit codes, and timeouts log a warning but never abort the agent loop. (Worked shell-hook scripts — auto-format, block `rm -rf`, inject `git status`, log subagent completions — are in [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md).)

### Consent model

Each unique `(event, command)` pair prompts the user for approval the **first time** Hermes sees it, then persists the decision to `~/.hermes/shell-hooks-allowlist.json`; subsequent runs (CLI or gateway) skip the prompt. Three escape hatches bypass the interactive prompt — any one is sufficient: the `--accept-hooks` CLI flag, the `HERMES_ACCEPT_HOOKS=1` environment variable, or `hooks_auto_accept: true` in config. Non-TTY runs (gateway, cron, CI) need one of these three — otherwise a newly-added hook silently stays un-registered and logs a warning. **Script edits are silently trusted:** the allowlist keys on the exact command string, not the script's hash, so editing the script on disk does not invalidate consent; `hermes hooks doctor` flags mtime drift so you can spot edits and decide whether to re-approve.

### The `hermes hooks` CLI

| Command | What it does |
|---------|--------------|
| `hermes hooks list` | Dump configured hooks with matcher, timeout, and consent status |
| `hermes hooks test <event> [--for-tool X] [--payload-file F]` | Fire every matching hook against a synthetic payload and print the parsed response |
| `hermes hooks revoke <command>` | Remove every allowlist entry matching `<command>` (takes effect on next restart) |
| `hermes hooks doctor` | For every configured hook: check exec bit, allowlist status, mtime drift, JSON output validity, and rough execution time |

### Security

Shell hooks run with **your full user credentials** — the same trust boundary as a cron entry or a shell alias — so the `hooks:` block in `config.yaml` is privileged configuration: only reference scripts you wrote or fully reviewed; keep scripts inside `~/.hermes/agent-hooks/` so the path is easy to audit; re-run `hermes hooks doctor` after pulling a shared config to spot newly-added hooks before they register; and if `config.yaml` is version-controlled across a team, review PRs that change the `hooks:` section the way you would review CI config.

### Ordering and precedence

Both Python plugin hooks and shell hooks flow through the same `invoke_hook()` dispatcher. Python plugins are registered first (`discover_and_load()`), shell hooks second (`register_from_config()`), so Python `pre_tool_call` block decisions take precedence in tie cases. **The first valid block wins** — the aggregator returns as soon as any callback produces `{"action": "block", "message": str}` with a non-empty message.

**Source**: `inbox/hermes_agent_docs/user-guide/features/hooks.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
**Last Updated**: 2026-06-19
**Status**: Active
