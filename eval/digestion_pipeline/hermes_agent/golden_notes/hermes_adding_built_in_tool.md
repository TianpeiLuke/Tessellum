---
tags:
  - resource
  - documentation
  - hermes_agent
  - tools
  - developer_guide
keywords:
  - adding a built-in tool
  - tools/your_tool.py
  - registry.register
  - toolsets.py
  - check_fn requires_env
  - async and task_id handlers
  - skill vs tool decision
topics:
  - Hermes Agent
  - Developer Guide
  - Tool Authoring
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools
access_control_group: ["general"]
---

# Hermes Agent — Adding a Built-in Tool

## Overview

This is the developer procedure for shipping a new **built-in core tool** into the Hermes Agent repository — a JSON-schema function-call handler that the agent can invoke during its loop. Before writing one, the source's first instruction is a decision, not a step: **should this be a [skill](hermes_creating_skill_format.md) instead?** Make it a **Skill** when the capability can be expressed as instructions + shell commands + existing tools (arXiv search, git workflows, Docker management, PDF processing). Make it a **Tool** when it requires end-to-end integration with API keys, custom processing logic, binary data handling, or streaming (browser automation, TTS, vision analysis). And the page is explicit that built-in is the *less* common path — for a personal, project-local, or otherwise custom tool that does not modify Hermes core, you should use the **plugin route** instead and "default to plugins for most custom tool creation." Only follow this page when you explicitly want to ship a new built-in tool in `tools/` and `toolsets.py`.

Adding a built-in tool touches **2 files**:

1. **`tools/your_tool.py`** — handler, schema, check function, and a `registry.register()` call.
2. **`toolsets.py`** — add the tool name to `_HERMES_CORE_TOOLS` (or a specific toolset).

Any `tools/*.py` file with a top-level `registry.register()` call is **auto-discovered at startup** by `discover_builtin_tools()` in `tools/registry.py` — there is no manual import list to maintain.

## Step 1: Create the Built-in Tool File

Every tool file follows the same structure: an availability **check function**, a **handler**, a
**schema**, and a **registration** call. The example below registers a `weather` tool gated on a
`WEATHER_API_KEY` environment variable:

```python
# tools/weather_tool.py
"""Weather Tool -- look up current weather for a location."""

import json
import os
import logging

logger = logging.getLogger(__name__)


# --- Availability check ---

def check_weather_requirements() -> bool:
    """Return True if the tool's dependencies are available."""
    return bool(os.getenv("WEATHER_API_KEY"))


# --- Handler ---

def weather_tool(location: str, units: str = "metric") -> str:
    """Fetch weather for a location. Returns JSON string."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return json.dumps({"error": "WEATHER_API_KEY not configured"})
    try:
        # ... call weather API ...
        return json.dumps({"location": location, "temp": 22, "units": units})
    except Exception as e:
        return json.dumps({"error": str(e)})


# --- Schema ---

WEATHER_SCHEMA = {
    "name": "weather",
    "description": "Get current weather for a location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name or coordinates (e.g. 'London' or '51.5,-0.1')"
            },
            "units": {
                "type": "string",
                "enum": ["metric", "imperial"],
                "description": "Temperature units (default: metric)",
                "default": "metric"
            }
        },
        "required": ["location"]
    }
}


# --- Registration ---

from tools.registry import registry

registry.register(
    name="weather",
    toolset="weather",
    schema=WEATHER_SCHEMA,
    handler=lambda args, **kw: weather_tool(
        location=args.get("location", ""),
        units=args.get("units", "metric")),
    check_fn=check_weather_requirements,
    requires_env=["WEATHER_API_KEY"],
)
```

### Key Rules

The page flags four contract rules as **Important** — they are the difference between a working tool and a silently-broken one:

- Handlers **MUST** return a JSON string (via `json.dumps()`), never raw dicts.
- Errors **MUST** be returned as `{"error": "message"}`, never raised as exceptions.
- The `check_fn` is called when building tool definitions — if it returns `False`, the tool is
  silently excluded (this is how `requires_env` gating shows up at runtime).
- The `handler` receives `(args: dict, **kwargs)` where `args` is the LLM's tool-call arguments.

## Step 2: Add the Built-in Tool to a Toolset

In `toolsets.py`, register the tool name either on the universal core toolset (available everywhere) or as a new standalone toolset:

```python
# If it should be available on all platforms (CLI + messaging):
_HERMES_CORE_TOOLS = [
    ...
    "weather",  # <-- add here
]

# Or create a new standalone toolset:
"weather": {
    "description": "Weather lookup tools",
    "tools": ["weather"],
    "includes": []
},
```

> **Step 3 (Add Discovery Import) is no longer needed.** Tool modules with a top-level
> `registry.register()` call are auto-discovered by `discover_builtin_tools()` in `tools/registry.py`.
> There is no manual import list — create the file in `tools/` and it is picked up at startup.

## Async Handlers

If the handler needs async code, mark the registration with `is_async=True`; the registry calls `_run_async()` automatically and handles async bridging transparently — you never call `asyncio.run()` yourself:

```python
async def weather_tool_async(location: str) -> str:
    async with aiohttp.ClientSession() as session:
        ...
    return json.dumps(result)

registry.register(
    name="weather",
    toolset="weather",
    schema=WEATHER_SCHEMA,
    handler=lambda args, **kw: weather_tool_async(args.get("location", "")),
    check_fn=check_weather_requirements,
    is_async=True,  # registry calls _run_async() automatically
)
```

## Handlers That Need task_id

Tools that manage per-session state receive `task_id` via `**kwargs`. Pull it out of the kwargs dict inside a wrapper handler and pass it through to the tool function:

```python
def _handle_weather(args, **kw):
    task_id = kw.get("task_id")
    return weather_tool(args.get("location", ""), task_id=task_id)

registry.register(
    name="weather",
    ...
    handler=_handle_weather,
)
```

## Agent-Loop Intercepted Tools

A small set of tools — `todo`, `memory`, `session_search`, and `delegate_task` — need access to
**per-session agent state** that the plain registry does not hold. These are **intercepted by
`run_agent.py` before reaching the registry**. The registry still holds their schemas (so the model sees them), but `dispatch()` returns a fallback error if the intercept is somehow bypassed. When authoring a tool that needs live agent state rather than just request arguments, this interception layer (covered in depth by the agent-loop internals) is the mechanism to mirror.

## Optional: Setup Wizard Integration

If the tool requires an API key, surface it in the first-run setup wizard by adding an entry to `OPTIONAL_ENV_VARS` in `hermes_cli/config.py`. This drives the interactive prompt, marks the value as a password, and ties the key back to the tools that consume it:

```python
OPTIONAL_ENV_VARS = {
    ...
    "WEATHER_API_KEY": {
        "description": "Weather API key for weather lookup",
        "prompt": "Weather API key",
        "url": "https://weatherapi.com/",
        "tools": ["weather"],
        "password": True,
    },
}
```

## Checklist

The page closes with a ship-it checklist:

- [ ] Tool file created with handler, schema, check function, and registration.
- [ ] Added to the appropriate toolset in `toolsets.py`.
- [ ] Confirmed this really should be a built-in/core tool and **not** a plugin.
- [ ] Handler returns JSON strings; errors returned as `{"error": "..."}`.
- [ ] Optional: API key added to `OPTIONAL_ENV_VARS` in `hermes_cli/config.py`.
- [ ] Optional: added to `toolset_distributions.py` for batch processing.
- [ ] Tested with `hermes chat -q "Use the weather tool for London"`.

**Source**: `inbox/hermes_agent_docs/developer-guide/adding-tools.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools
**Last Updated**: 2026-06-19
**Status**: Active
