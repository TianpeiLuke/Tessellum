---
tags:
  - resource
  - terminology
  - agent_systems
  - lifecycle_hooks
keywords:
  - Gateway Hooks
  - Hermes hooks
  - event hooks
  - lifecycle hooks
  - plugin hooks
  - shell hooks
  - HOOK.yaml
  - register_hook
  - pre_tool_call
  - pre_llm_call
topics:
  - Agent Extensibility
  - Lifecycle Hooks
  - Event-Driven Architecture
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Gateway Hooks - Hermes Agent Lifecycle Hooks

## Definition

**Gateway Hooks** (more precisely, the **Hermes event-hook surface**) are the three complementary systems by which the [Hermes Agent](term_hermes_agent.md) runs user- or plugin-supplied code at fixed lifecycle points of the agent loop and the messaging gateway. The umbrella covers (1) **gateway hooks** — `HOOK.yaml` + `handler.py` directories under `~/.hermes/hooks/` that fire only inside the gateway (Telegram, Discord, Slack, WhatsApp, Teams); (2) **plugin hooks** — Python callbacks registered with `ctx.register_hook()` inside a [plugin's](term_hermes_plugin.md) `register()` function, firing in both CLI and gateway; and (3) **shell hooks** — drop-in subprocess scripts declared in a `hooks:` block of `~/.hermes/config.yaml` that communicate over a JSON stdin/stdout protocol. All three are instances of the [Observer pattern](term_observer_pattern.md): handlers subscribe to named [agent lifecycle events](term_agent_lifecycle_event.md), and a dispatcher (`hooks.emit()` / `invoke_hook()`) fans each event out to every matching handler.

The hook surface solves the *extensibility-without-forking* problem: it lets operators add logging, alerts, webhooks, metrics, [guardrails](term_guardrails.md), context injection, output redaction, and tool vetoes without editing Hermes core. A defining safety property is that all three systems are **non-blocking by failure** — a handler that raises is caught and logged, never crashing the agent — and only two hooks can alter control flow at all: `pre_tool_call` (which may **block** a tool with `{"action": "block", "message": ...}`) and `pre_llm_call` (which may **inject context** into the current turn's user message). Every other hook is a fire-and-forget observer.

## Context

Gateway hooks are an extension point of the **Hermes Agent**, the personal AI agent framework from the **Nous Research team**. They sit at the seams of the agent runtime: gateway hooks fire in `gateway/run.py` on `gateway:startup`, `session:*`, `agent:*`, and `command:*` events; plugin and shell hooks fire inside `run_agent.py`'s turn loop (`pre_llm_call`/`post_llm_call`, session lifecycle) and inside `model_tools.py`'s `handle_function_call()` (`pre_tool_call`/`post_tool_call`/`transform_*`). On startup `HookRegistry.discover_and_load()` scans the hooks directory and registers each handler against its declared events; shell hooks are registered second via `register_from_config()`, so a Python plugin's block decision wins a tie.

The same architecture recurs across agent frameworks: **Claude Code** exposes the analogous `PreToolUse`/`PostToolUse`/`UserPromptSubmit`/`SessionStart`/`SubagentStop` events with the same block-and-modify contract.

## Key Characteristics

- **Three registration surfaces, one dispatcher.** Gateway hooks (`HOOK.yaml`+`handler.py`, gateway-only), plugin hooks (`ctx.register_hook()`, CLI+gateway, Python-only), and shell hooks (`hooks:` config, CLI+gateway, any language) all flow through the same `invoke_hook()` aggregator.
- **Only two hooks affect control flow.** `pre_tool_call` returns `{"action": "block", "message": str}` to veto a tool; `pre_llm_call` returns `{"context": str}` (or a plain string) to prepend ephemeral context to the user message. All others are observers whose return value is ignored.
- **Context injection preserves the prompt cache.** `pre_llm_call` always injects into the *user* message, never the system prompt, so cached system-prompt tokens stay reusable across turns; injected context is ephemeral and never persisted.
- **14 plugin-hook lifecycle points**, including the tool loop (`pre_tool_call`, `post_tool_call`), per-turn (`pre_llm_call`, `post_llm_call`), session lifecycle (`on_session_start`/`_end`/`_finalize`/`_reset`), delegation (`subagent_stop`), gateway dispatch (`pre_gateway_dispatch`, with `skip`/`rewrite`/`allow`), approval (`pre_approval_request`, `post_approval_response`), and three rewriters (`transform_tool_result`, `transform_terminal_output`, `transform_llm_output`).
- **Wildcard subscription.** Gateway handlers can subscribe to `command:*` to observe every slash command with one registration.
- **First-use consent for shell hooks.** Each unique `(event, command)` pair prompts once, then persists to `~/.hermes/shell-hooks-allowlist.json`; bypasses are `--accept-hooks`, `HERMES_ACCEPT_HOOKS=1`, or `hooks_auto_accept: true`. The allowlist keys on the command string (not a hash), so script edits are silently trusted — `hermes hooks doctor` flags mtime drift.
- **Inter-process isolation only for shell hooks.** Shell hooks run as subprocesses (a security boundary with your full user credentials); plugin and gateway hooks run in-process.
- **Ordering and precedence.** Python plugin hooks are registered before shell hooks; the aggregator returns as soon as any callback yields a non-empty block, so the first valid block wins (Python plugins win ties).

## Related Terms


## References

- [Hermes Agent — Event Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks/)
- [Hermes Agent — Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/)
- [Claude Code — Hooks](https://code.claude.com/docs/en/hooks)
- [Observer Pattern — Refactoring.Guru](https://refactoring.guru/design-patterns/observer)
