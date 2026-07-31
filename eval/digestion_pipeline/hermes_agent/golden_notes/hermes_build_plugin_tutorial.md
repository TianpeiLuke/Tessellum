---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugins
  - tutorial
keywords:
  - build a hermes plugin
  - plugin.yaml manifest
  - tool schemas and handlers
  - register(ctx) wiring
  - dispatch_tool
  - HERMES_PLUGINS_DEBUG discovery
topics:
  - Hermes Agent
  - Plugins
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
access_control_group: ["general"]
---

# Build a Hermes Plugin — Tutorial

## Overview

This is the **end-to-end "build your first plugin" walkthrough** for Hermes Agent: a six-step procedure that produces a working `calculator` plugin from an empty directory. It is the canonical entry point into the Hermes plugin system — the general plugin surface that registers custom tools, lifecycle hooks, slash/CLI commands, and bundled skills via Python `register_*` APIs. The tutorial builds two tools (`calculate` for math expressions, `unit_convert` for unit conversion), plus a `post_tool_call` hook that logs every call, ending in a four-file plugin directory.

The plugin lives under `~/.hermes/plugins/<plugin-name>/` and is opt-in (enabled in config). The four files separate concerns cleanly: `plugin.yaml` (manifest — what the plugin is), `schemas.py` (what the LLM reads to decide when to call), `tools.py` (the handlers that run), and `__init__.py` (the `register(ctx)` wiring that connects them). The extras surface (data files, hooks reference, command registration) and the five specialized plugin types live in the sibling notes; this note is just the tutorial arc.

The docs page opens with a routing map ("If you want to add…") that points elsewhere for LLM/inference backends, gateway channels, memory backends, context engines, image-gen backends, TTS/STT, MCP servers, gateway/shell hooks, and skill sources — the general plugin tutorial below is for **custom tools, hooks, slash commands, skills, or CLI subcommands**.

## What you're building

A **calculator** plugin with two tools:

- `calculate` — evaluate math expressions (`2**16`, `sqrt(144)`, `pi * 5**2`)
- `unit_convert` — convert between units (`100 F → 37.78 C`, `5 km → 3.11 mi`)

Plus a hook that logs every tool call, and a bundled skill file. The plugin demonstrates everything the general plugin surface supports.

## Step 1: Create the plugin directory

```bash
mkdir -p ~/.hermes/plugins/calculator
cd ~/.hermes/plugins/calculator
```

The directory layout must be `~/.hermes/plugins/<plugin-name>/plugin.yaml` (flat) or `~/.hermes/plugins/<category>/<plugin-name>/plugin.yaml` (one level of category nesting, max). Anything deeper is ignored by discovery.

## Step 2: Write the manifest

Create `plugin.yaml` — it declares what the plugin is and what it registers:

```yaml
name: calculator
version: 1.0.0
description: Math calculator — evaluate expressions and convert units
provides_tools:
  - calculate
  - unit_convert
provides_hooks:
  - post_tool_call
```

`provides_tools` and `provides_hooks` are lists of what the plugin registers. Optional fields include `author` and `requires_env` (gate loading on env vars; users are prompted interactively for missing ones during `hermes plugins install`). `requires_env` accepts a simple format (a bare var name → plugin disabled if missing) or a rich format (`name`/`description`/`url`/`secret` shown during install).

## Step 3: Write the tool schemas

Create `schemas.py` — this is what the LLM reads to decide when to call your tools. Each schema is a dict with `name`, a precise `description`, and JSON-Schema `parameters`:

```python
"""Tool schemas — what the LLM sees."""

CALCULATE = {
    "name": "calculate",
    "description": (
        "Evaluate a mathematical expression and return the result. "
        "Supports arithmetic (+, -, *, /, **), functions (sqrt, sin, cos, "
        "log, abs, round, floor, ceil), and constants (pi, e). "
        "Use this for any math the user asks about."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression to evaluate (e.g., '2**10', 'sqrt(144)')",
            },
        },
        "required": ["expression"],
    },
}
```

**Why schemas matter:** the `description` field is how the LLM decides when to use your tool — be specific about what it does and when to use it. `parameters` defines the arguments the LLM passes. (`UNIT_CONVERT` follows the same shape with `value`, `from_unit`, `to_unit` parameters.)

## Step 4: Write the tool handlers

Create `tools.py` — the code that actually executes when the LLM calls your tools. Each handler takes `args: dict`, does its work, and returns a JSON string:

```python
import json, math

def calculate(args: dict, **kwargs) -> str:
    """Evaluate a math expression safely.

    Rules for handlers:
    1. Receive args (dict) — the parameters the LLM passed
    2. Do the work
    3. Return a JSON string — ALWAYS, even on error
    4. Accept **kwargs for forward compatibility
    """
    expression = args.get("expression", "").strip()
    if not expression:
        return json.dumps({"error": "No expression provided"})
    try:
        result = eval(expression, {"__builtins__": {}}, _SAFE_MATH)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"expression": expression, "error": f"Invalid: {e}"})
```

The `calculate` handler evaluates against a `_SAFE_MATH` globals dict (no file/network access); `unit_convert` uses ratio tables for length/weight/data/time plus a temperature normalize-to-Celsius helper. The four **key rules for handlers**:

1. **Signature:** `def my_handler(args: dict, **kwargs) -> str`
2. **Return:** always a JSON string — success and errors alike.
3. **Never raise:** catch all exceptions, return error JSON instead.
4. **Accept `**kwargs`:** Hermes may pass additional context in the future.

## Step 5: Write the registration

Create `__init__.py` — this wires schemas to handlers and registers hooks. `register(ctx)` is called exactly once at startup:

```python
"""Calculator plugin — registration."""
import logging
from . import schemas, tools

logger = logging.getLogger(__name__)
_call_log = []

def _on_post_tool_call(tool_name, args, result, task_id, **kwargs):
    """Hook: runs after every tool call (not just ours)."""
    _call_log.append({"tool": tool_name, "session": task_id})
    if len(_call_log) > 100:
        _call_log.pop(0)

def register(ctx):
    """Wire schemas to handlers and register hooks."""
    ctx.register_tool(name="calculate",    toolset="calculator",
                      schema=schemas.CALCULATE,    handler=tools.calculate)
    ctx.register_tool(name="unit_convert", toolset="calculator",
                      schema=schemas.UNIT_CONVERT, handler=tools.unit_convert)
    # This hook fires for ALL tool calls, not just ours
    ctx.register_hook("post_tool_call", _on_post_tool_call)
```

**What `register()` does:** `ctx.register_tool()` puts your tool in the registry (the model sees it immediately); `ctx.register_hook()` subscribes to lifecycle events; `ctx.register_cli_command()` adds a `hermes <plugin>` subcommand; `ctx.register_command()` adds an in-session `/slash` command; and `ctx.dispatch_tool(name, arguments)` calls any other tool with the parent agent's context (approvals, credentials, `task_id`) wired up automatically. If `register()` crashes, the plugin is disabled but Hermes continues fine.

As a `dispatch_tool` example, a `/scan` slash-command handler can call `ctx.dispatch_tool("terminal", {"command": f"find . -name '{raw_args}'"})` and return the result to the chat UI. The dispatched tool goes through the normal approval, redaction, and budget pipelines — it is a real tool invocation, not a shortcut around them.

## Step 6: Test it

Start Hermes with `hermes` — you should see `calculator: calculate, unit_convert` in the banner's tool list. Try prompts like "What's 2 to the power of 16?" or "Convert 100 fahrenheit to celsius". Check status with `/plugins`, which prints `✓ calculator v1.0.0 (2 tools, 1 hooks)`.

### Debugging plugin discovery

If your plugin doesn't show up — or shows up but isn't loading — set `HERMES_PLUGINS_DEBUG=1` for verbose discovery logs on stderr (`HERMES_PLUGINS_DEBUG=1 hermes plugins list`). For every plugin source (bundled, user, project, entry-points) you see which directories were scanned, per-manifest resolved key/name/kind/source/path, skip reasons (`disabled via config`, `not enabled in config`, `exclusive plugin`, `no plugin.yaml, depth cap reached`), the one-line `register(ctx)` summary on load, and full tracebacks on parse or `register()` failure. The same logs are always written to `~/.hermes/logs/agent.log` (WARNING = failures only; DEBUG = everything when the env var is set), tailable via `hermes logs --level WARNING | grep -i plugin`.

Common reasons a plugin doesn't appear: **not enabled in config** (plugins are opt-in — run `hermes plugins enable <name>`), **wrong directory layout** (must be flat or one category level deep), **missing `__init__.py`** (need both `plugin.yaml` and `__init__.py` with `register(ctx)`), or **wrong `kind`** (gateway adapters need `kind: platform`; memory providers are auto-detected as `kind: exclusive`).

## Your plugin's final structure

```
~/.hermes/plugins/calculator/
├── plugin.yaml      # "I'm calculator, I provide tools and hooks"
├── __init__.py      # Wiring: schemas → handlers, register hooks
├── schemas.py       # What the LLM reads (descriptions + parameter specs)
└── tools.py         # What runs (calculate, unit_convert functions)
```

Four files, clear separation: the **manifest** declares what the plugin is, **schemas** describe tools for the LLM, **handlers** implement the actual logic, and **registration** connects everything.

**Source**: `inbox/hermes_agent_docs/guides/build-a-hermes-plugin.md` · https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
**Last Updated**: 2026-06-19
**Status**: Active
