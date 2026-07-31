---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugins
  - hooks
keywords:
  - plugin lifecycle hooks
  - pre_llm_call context injection
  - register slash commands
  - lazy install dependencies
  - thread-safe singletons
  - slack block kit handlers
topics:
  - Hermes Agent
  - Plugin Development
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
access_control_group: ["general"]
---

# Hermes Plugin Extensions and Hooks

## Overview

This is the **extras surface of a Hermes plugin** — everything a plugin can register beyond its basic tools, picking up where the [calculator-plugin tutorial](hermes_build_plugin_tutorial.md) leaves off. Once a plugin has `plugin.yaml` + `__init__.py` + `schemas.py` + `tools.py` wired up, the same `register(ctx)` entry point can also: ship data files and bundled read-only skills, gate loading on environment variables, lazy-install optional Python dependencies, build thread-safe singletons, conditionally hide tools, override built-in tools, subscribe to the eight lifecycle hooks (including the one hook that injects context — `pre_llm_call`), and add CLI subcommands, in-session slash commands, and Slack Block Kit button handlers. These are the reference patterns and signatures for each, drawn from the "What else can plugins do?" half of the build-a-plugin guide. The specialized plugin *types* (provider/platform/memory/etc.) and the non-Python drop-in surfaces are catalogued separately in [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md).

## Ship data files and bundle skills

A plugin can ship arbitrary files in its directory and read them at import time (`Path(__file__).parent / "data" / "…"`). It can also bundle **skill files** the agent loads via `skill_view("plugin:skill")`. Register each `SKILL.md` from `register()`:

```python
from pathlib import Path

def register(ctx):
    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
```

The agent then loads `skill_view("my-plugin:my-workflow")` (the namespaced plugin version) versus `skill_view("my-workflow")` (the unchanged built-in). Plugin skills are **read-only** (they never enter `~/.hermes/skills/`, can't be edited via `skill_manage`), are **not** listed in the system prompt's `<available_skills>` index (opt-in explicit loads), and the namespace prevents collisions with built-in skills. The legacy `shutil.copy2` copy-into-`~/.hermes/skills/` pattern still works but risks name collisions — prefer `ctx.register_skill()`.

## Gate, lazy-install, and singleton-cache

Three loading/runtime guards keep a plugin robust:

- **Gate on env vars** — declare `requires_env` in `plugin.yaml` (simple `- WEATHER_API_KEY`, or rich format with `name`/`description`/`url`/`secret`). A missing var disables the plugin cleanly ("Plugin weather disabled (missing: WEATHER_API_KEY)") instead of crashing; `hermes plugins install` prompts interactively for missing vars and saves them to `.env`.
- **Lazy-install optional deps** — don't `import` a heavy/vendor SDK at module top. Call `tools.lazy_deps.ensure(...)` inside the handler; Hermes installs the package on first use, gated by `security.allow_lazy_installs`. The feature key must appear in the in-tree `LAZY_DEPS` allowlist (a malicious config can't coax an arbitrary install) and specs are PyPI-by-name only (no `--index-url`, `git+https://`, or file paths). When installs are disabled globally, `ensure()` raises `FeatureUnavailable` — catch it and degrade gracefully.
- **Thread-safe lazy singletons** — Hermes runs multiple threads in one process (delegated calls, background workers, the self-improvement fork), so the hand-rolled `global _client` + `is None` check + build is a TOCTOU race that leaks the loser's resource. Use the helpers in `plugins/plugin_utils.py`:

```python
from plugins.plugin_utils import lazy_singleton, SingletonSlot

# Zero-arg accessor → decorate it:
@lazy_singleton
def get_client():
    return ExpensiveClient(load_config())   # runs exactly once

# Accessor that takes a build argument → use a slot:
_slot: SingletonSlot = SingletonSlot()

def get_client(config=None):
    return _slot.get(lambda: ExpensiveClient(resolve(config)))
```

Both serialize concurrent first calls with double-checked locking and run the factory at most once; if it raises, nothing is cached and the next call retries.

## Conditional availability and overriding built-ins

A tool can be hidden from the model when its optional dependency is absent — pass `check_fn=lambda: _has_optional_lib()` to `register_tool` (a `False` return hides the tool). To replace a built-in tool (e.g. swap the default browser for a headed-Chrome CDP backend, or `web_search` for a corporate index), pass `override=True` with your own `toolset` namespace. Without `override=True`, the registry rejects any registration that would shadow an existing tool from a different toolset — preventing accidental overwrites. The override is logged at INFO level in `~/.hermes/logs/agent.log`, and plugins load after built-in tools so the registration order is correct.

## Lifecycle hooks and `pre_llm_call` context injection

A plugin subscribes to lifecycle events with `ctx.register_hook("<event>", callback)` (you may register many). The eight hooks:

| Hook | Fires when | Returns |
|------|-----------|---------|
| `pre_tool_call` | Before any tool executes | ignored |
| `post_tool_call` | After any tool returns | ignored |
| `pre_llm_call` | Once per turn, before the tool-calling loop | context injection |
| `post_llm_call` | Once per turn, after the loop (successful turns only) | ignored |
| `on_session_start` | New session created (first turn only) | ignored |
| `on_session_end` | End of every `run_conversation` + CLI exit | ignored |
| `on_session_finalize` | CLI/gateway tears down an active session | ignored |
| `on_session_reset` | Gateway swaps in a new session key (`/new`, `/reset`) | ignored |

All callbacks should accept `**kwargs` for forward compatibility; a crashing callback is logged and skipped while everything else continues. Most hooks are fire-and-forget observers — **`pre_llm_call` is the only hook whose return value matters.** When it returns a dict with a `"context"` key (or a plain string), Hermes injects that text:

```python
def recall_context(session_id, user_message, is_first_turn, **kwargs):
    """Called before each LLM turn. Returns recalled memories."""
    memories = fetch_relevant(session_id, user_message)
    if not memories:
        return None  # observer-only — nothing injected
    text = "Recalled context:\n" + "\n".join(f"- {m}" for m in memories)
    return {"context": text}

def register(ctx):
    ctx.register_hook("pre_llm_call", recall_context)
```

Injected context is appended to the **current turn's user message**, never the system prompt. This is deliberate: the system prompt stays identical across turns so Anthropic/OpenRouter cache its prefix (saving 75%+ on input tokens in multi-turn conversations) — modifying it would force a cache miss every turn. The injection is **ephemeral** (it happens at API-call time only; the stored user message and session DB are never mutated), and when multiple plugins return context, the outputs are joined with double newlines in plugin-discovery (alphabetical) order. This is the mechanism for memory plugins, RAG integrations, and guardrails.

## Register CLI commands, slash commands, and dispatch tools

A plugin extends Hermes three further ways, all from `register(ctx)`:

- **`ctx.register_cli_command(...)`** — add a `hermes <plugin> <subcommand>` argparse tree (terminal only; handler receives an argparse `Namespace`). Good for setup wizards and complex subcommands. (Memory plugins instead use convention-based `register_cli(subparser)` in `cli.py`, auto-discovered.)
- **`ctx.register_command(name, handler, description="", args_hint="")`** — add an in-session slash command typed during a conversation (`/mystatus`), working across CLI and gateway (Telegram, Discord). The handler receives the raw argument string and may be `async` (the gateway auto-awaits). It appears in autocomplete, `/help`, and the Telegram bot menu. Names conflicting with a built-in command (`help`, `model`, `new`) are silently rejected — built-ins always win.
- **`ctx.dispatch_tool(name, args, *, parent_agent=None)`** — invoke any other tool (built-in or another plugin's) from a slash-command handler with the parent agent's context (approvals, credentials, workspace, spinner, model) wired up automatically. The dispatched tool goes through the normal approval, redaction, and budget pipelines — it is a real tool invocation, not a shortcut. In CLI mode `parent_agent` resolves from the active agent; in gateway mode it degrades gracefully. This is the stable public interface — plugins should not reach into `ctx._cli_ref.agent`.

```python
def register(ctx):
    def _handle_deliver(raw_args: str):
        return ctx.dispatch_tool(
            "delegate_task",
            {"goal": raw_args, "toolsets": ["terminal", "file", "web"]},
        )
    ctx.register_command(
        "deliver",
        handler=_handle_deliver,
        description="Delegate a goal to a subagent",
    )
```

## Handle Slack Block Kit button clicks

Plugins that post Block Kit messages with interactive elements (buttons, overflow menus, datepickers) register click handlers directly with the Slack adapter — no monkey-patching of `slack_bolt.AsyncApp`:

```python
def register(ctx):
    async def _on_approve(ack, body, action):
        await ack()                       # ack within 3s — slack_bolt requirement
        sweep_id = (action.get("value") or "").split("|", 1)[-1]
        # ...deterministic work, then post a follow-up.

    ctx.register_slack_action_handler("inbox_sweep_approve", _on_approve)
```

`ctx.register_slack_action_handler(action_id, callback)` accepts whatever `slack_bolt.App.action()` accepts for `action_id` — a literal id, a compiled regex matching multiple ids, or a constraint dict. The handler is queued at plugin-load time and wired into the adapter's `AsyncApp` when Slack connects. Each callback is wrapped defensively: a raise is logged and the click best-effort-acked so Slack stops retrying. Standard slack_bolt rules apply (`await ack()` within 3 seconds, then longer work); for multi-workspace deployments use `body["team"]["id"]` to scope behaviour.

**Source**: `inbox/hermes_agent_docs/guides/build-a-hermes-plugin.md` · https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
**Last Updated**: 2026-06-19
**Status**: Active
