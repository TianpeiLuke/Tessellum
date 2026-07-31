---
tags:
  - resource
  - documentation
  - hermes_agent
  - memory
  - plugins
keywords:
  - memory provider plugin
  - MemoryProvider ABC
  - hermes memory setup
  - sync_turn threading contract
  - profile isolation hermes_home
  - convention-based cli.py subcommands
  - single provider rule
  - on_pre_compress lifecycle hook
topics:
  - Hermes Agent
  - Plugin Authoring
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin
access_control_group: ["general"]
---

# Hermes Agent — Building a Memory Provider Plugin

## Overview

A **memory provider plugin** is a self-contained directory you drop under `$HERMES_HOME/plugins/memory/<name>/` to give Hermes Agent persistent, cross-session knowledge beyond the built-in `MEMORY.md` and `USER.md` files — with zero edits to the Hermes repo. This is a step-by-step authoring procedure: you implement the `MemoryProvider` abstract base class (its `name`/`is_available()`/`initialize()`/`get_tool_schemas()`/`handle_tool_call()` core plus optional lifecycle hooks like `prefetch`/`sync_turn`/`on_pre_compress`/`on_session_end`), declare a config schema so `hermes memory setup` can prompt for credentials, expose an `__init__.py` `register()` entry point, drop a `plugin.yaml` manifest, and ship it via pip.

Memory providers are one of two **provider plugin** types in Hermes; the other is the [context engine plugin](hermes_context_engine_plugin.md). Both follow the same single-select, config-driven shape managed through `hermes plugins`: only one external memory provider can be active at a time. Two operational contracts make memory backends distinct — `sync_turn()` MUST be non-blocking (run latency-bound work in a daemon thread), and all storage paths MUST be scoped to the `hermes_home` profile, never to a hardcoded `~/.hermes`.

## Directory Structure

Each memory provider lives in `plugins/memory/<name>/`:

```
plugins/memory/my-provider/
├── __init__.py      # MemoryProvider implementation + register() entry point
├── plugin.yaml      # Metadata (name, description, hooks)
└── README.md        # Setup instructions, config reference, tools
```

## The MemoryProvider ABC

Your plugin implements the `MemoryProvider` abstract base class from `agent/memory_provider.py`:

```python
from agent.memory_provider import MemoryProvider

class MyMemoryProvider(MemoryProvider):
    @property
    def name(self) -> str:
        return "my-provider"

    def is_available(self) -> bool:
        """Check if this provider can activate. NO network calls."""
        return bool(os.environ.get("MY_API_KEY"))

    def initialize(self, session_id: str, **kwargs) -> None:
        """Called once at agent startup.

        kwargs always includes:
          hermes_home (str): Active HERMES_HOME path. Use for storage.
        """
        self._api_key = os.environ.get("MY_API_KEY", "")
        self._session_id = session_id

    # ... implement remaining methods
```

## Required Methods

The contract splits into core-lifecycle, config, and optional hooks. The core-lifecycle methods are mandatory: the `name` property, `is_available()` (checked at agent init before activation — **no network calls**), `initialize(session_id, **kwargs)` (agent startup), `get_tool_schemas()` (after init, for tool injection), and `handle_tool_call(tool_name, args, **kwargs)` (when the agent invokes your tools).

For **config**, implement `get_config_schema()` (declares the fields `hermes memory setup` prompts for) and `save_config(values, hermes_home)` (writes non-secret config to your native location — required unless the provider is env-var-only).

The **optional hooks** are where a backend persists and recalls conversation:

| Method | When Called | Use Case |
|--------|-----------|----------|
| `system_prompt_block()` | System prompt assembly | Static provider info |
| `prefetch(query, *, session_id="")` | Before each API call | Return recalled context |
| `queue_prefetch(query)` | After each turn | Pre-warm for next turn |
| `sync_turn(user, assistant, *, session_id="")` | After each completed turn | Persist conversation |
| `on_session_end(messages)` | Conversation ends | Final extraction/flush |
| `on_pre_compress(messages)` | Before context compression | Save insights before discard |
| `on_memory_write(action, target, content)` | Built-in memory writes | Mirror to your backend |
| `shutdown()` | Process exit | Clean up connections |

## Config Schema

`get_config_schema()` returns a list of field descriptors used by `hermes memory setup`:

```python
def get_config_schema(self):
    return [
        {
            "key": "api_key",
            "description": "My Provider API key",
            "secret": True,           # → written to .env
            "required": True,
            "env_var": "MY_API_KEY",   # explicit env var name
            "url": "https://my-provider.com/keys",  # where to get it
        },
        {
            "key": "region",
            "description": "Server region",
            "default": "us-east",
            "choices": ["us-east", "eu-west", "ap-south"],
        },
        {
            "key": "project",
            "description": "Project identifier",
            "default": "hermes",
        },
    ]
```

Fields with `secret: True` and `env_var` go to `.env`; non-secret fields are passed to `save_config()`. Every field is prompted during setup, so providers with many options should keep the schema minimal — only fields the user **must** configure (API key, required credentials) — and document optional settings in a config-file reference (e.g. `$HERMES_HOME/myprovider.json`) rather than prompting for them all. The Supermemory provider is the canonical example: it prompts only for the API key; all other options live in `supermemory.json`.

## Save Config

For non-secret values, implement `save_config(self, values, hermes_home)` to write them to your native location (e.g. `Path(hermes_home) / "my-provider.json"` with `json.dumps(values, indent=2)`); env-var-only providers leave the default no-op.

## Plugin Entry Point and plugin.yaml

The `__init__.py` exposes a `register(ctx)` function that the memory plugin discovery system calls, registering an instance via `ctx.register_memory_provider()`:

```python
def register(ctx) -> None:
    """Called by the memory plugin discovery system."""
    ctx.register_memory_provider(MyMemoryProvider())
```

The `plugin.yaml` manifest carries metadata plus the list of hooks you implement:

```yaml
name: my-provider
version: 1.0.0
description: "Short description of what this provider does."
hooks:
  - on_session_end    # list hooks you implement
```

## Threading Contract

**`sync_turn()` MUST be non-blocking.** If your backend has latency (API calls, LLM processing), run the work in a daemon thread:

```python
def sync_turn(self, user_content, assistant_content, *, session_id="", messages=None):
    def _sync():
        try:
            self._api.ingest(user_content, assistant_content, session_id=session_id, messages=messages)
        except Exception as e:
            logger.warning("Sync failed: %s", e)

    if self._sync_thread and self._sync_thread.is_alive():
        self._sync_thread.join(timeout=5.0)
    self._sync_thread = threading.Thread(target=_sync, daemon=True)
    self._sync_thread.start()
```

`messages` is an optional OpenAI-style conversation context as of the completed turn — when present it includes user/assistant messages, assistant tool calls, and tool result messages. Providers that do not need raw turn context can omit the parameter; Hermes keeps calling them with the legacy signature. Cloud providers should document what parts of `messages` are sent off-device: tool calls and tool results may contain file paths, command output, or other workspace data (the PII/off-device-data boundary).

## Profile Isolation

All storage paths **must** use the `hermes_home` kwarg from `initialize()`, not a hardcoded `~/.hermes`, so each profile stays isolated. Correct: derive the data directory from the active home, e.g. `get_hermes_home() / "my-provider"` (imported from `hermes_constants`). Wrong: `Path("~/.hermes/my-provider").expanduser()`, which is shared across all profiles.

## Testing

See `tests/agent/test_memory_provider.py` and adjacent memory tests (`test_memory_session_switch.py`, `test_memory_user_id.py`, `tests/run_agent/test_memory_provider_init.py`) for end-to-end patterns. The `MemoryManager` drives provider activation, tool routing, and lifecycle in tests: build one, `add_provider()`, `initialize_all(session_id=..., platform="cli")`, then exercise `handle_tool_call()`, `sync_all()`, `on_session_end([])`, and `shutdown_all()`.

## Adding CLI Commands

Memory provider plugins can register their own CLI subcommand tree (e.g. `hermes my-provider status`) via a convention-based discovery system — no core-file changes. Add a `cli.py` to the plugin directory, define a `register_cli(subparser)` that builds the argparse tree, and the memory plugin system discovers it at startup via `discover_plugin_cli_commands()`. Commands appear under `hermes <provider-name> <subcommand>`. **Active-provider gating:** your CLI commands only show when your provider is the active `memory.provider` in config — if a user hasn't configured your provider, they won't appear in `hermes --help`. The `honcho` reference plugin (`plugins/memory/honcho/cli.py`) is a full example with 13 subcommands, cross-profile management (`--target-profile`), and config read/write.

## Single Provider Rule

Only **one** external memory provider can be active at a time. If a user tries to register a second, the `MemoryManager` rejects it with a warning. This prevents tool-schema bloat and conflicting backends.

**Source**: `inbox/hermes_agent_docs/developer-guide/memory-provider-plugin.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin
**Last Updated**: 2026-06-19
**Status**: Active
