---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugin_system
  - extensibility
keywords:
  - hermes plugin system
  - register ctx
  - plugin.yaml manifest
  - plugin discovery
  - plugins.enabled allow-list
  - ctx.register_tool
  - inject_message
topics:
  - Hermes Agent
  - Plugins
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
access_control_group: ["general"]
---

# Hermes Plugin System

## Overview

The Hermes plugin system is the agent's primary **extension point**: a way to add custom tools, hooks, and integrations *without modifying core code*. A plugin is a directory dropped into `~/.hermes/plugins/` containing a `plugin.yaml` manifest and Python code whose top-level `register(ctx)` function wires the plugin's capabilities into Hermes through the `ctx.*` API. On startup Hermes discovers plugins from five sources, and an enabled plugin's tools appear alongside built-in tools so the model can call them immediately. This note describes what the plugin system *is* — the `register(ctx)` contract, the `ctx.*` capability surface, the discovery sources and sub-category routing, the opt-in `plugins.enabled` allow-list (and what it does not gate), the four plugin kinds, and message injection. The CLI workflow for installing/toggling/managing plugins lives in [hermes_plugins_management](hermes_plugins_management.md); the bundled in-tree catalog lives in [hermes_built_in_plugins](hermes_built_in_plugins.md); full hook callback signatures live in [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md). For one-tool/one-team/one-project custom tools this is usually the right path; built-in core tools (in `tools/` and `toolsets.py`) are authored differently.

## Quick Overview — Plugin Layout

Drop a directory into `~/.hermes/plugins/` with a `plugin.yaml` and Python code. A plugin directory has a conventional shape:

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml      # manifest
├── __init__.py      # register() — wires schemas to handlers
├── schemas.py       # tool schemas (what the LLM sees)
└── tools.py         # tool handlers (what runs when called)
```

Start Hermes — the plugin's tools appear alongside built-in tools and the model can call them. The `plugin.yaml` manifest carries fields like `name`, `version`, `description`, and optional `requires_env` (env vars prompted at install). The schema/handler split mirrors the LLM contract: schemas declare what the model sees; handlers are what runs when a tool is called.

### Minimal Working Example

A complete plugin that adds a `hello_world` tool and logs every tool call via a hook. The `__init__.py` `register(ctx)` is the only required entry point:

```python
"""Minimal Hermes plugin — registers a tool and a hook."""

import json


def register(ctx):
    # --- Tool: hello_world ---
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to greet"}
            },
            "required": ["name"],
        },
    }

    def handle_hello(params, **kwargs):
        del kwargs
        name = params.get("name", "World")
        return json.dumps({"success": True, "greeting": f"Hello, {name}!"})

    ctx.register_tool(
        name="hello_world", toolset="hello_world", schema=schema,
        handler=handle_hello,
        description="Return a friendly greeting for the given name.",
    )

    # --- Hook: log every tool call ---
    def on_tool_call(tool_name, params, result):
        print(f"[hello-world] tool called: {tool_name}")

    ctx.register_hook("post_tool_call", on_tool_call)
```

Drop the files into `~/.hermes/plugins/hello-world/`, restart Hermes, and the model can immediately call `hello_world`; the hook prints a log line after every tool invocation. Project-local plugins under `./.hermes/plugins/` are disabled by default — enable them only for trusted repos by setting `HERMES_ENABLE_PROJECT_PLUGINS=true` before starting Hermes.

## What Plugins Can Do — the `ctx.*` API

Every `ctx.*` method below is available inside a plugin's `register(ctx)` function — this is the full capability surface a plugin can register against:

| Capability | How |
|-----------|-----|
| Add tools | `ctx.register_tool(name=..., toolset=..., schema=..., handler=...)` |
| Add hooks | `ctx.register_hook("post_tool_call", callback)` |
| Add slash commands | `ctx.register_command(name, handler, description)` — adds `/name` in CLI and gateway |
| Dispatch tools from commands | `ctx.dispatch_tool(name, args)` — invokes a tool with parent-agent context |
| Add CLI commands | `ctx.register_cli_command(name, help, setup_fn, handler_fn)` — adds `hermes <plugin> <sub>` |
| Inject messages | `ctx.inject_message(content, role="user")` |
| Ship data files | `Path(__file__).parent / "data" / "file.yaml"` |
| Bundle skills | `ctx.register_skill(name, path)` — namespaced `plugin:skill`, via `skill_view("plugin:skill")` |
| Gate on env vars | `requires_env: [API_KEY]` in plugin.yaml — prompted during `hermes plugins install` |
| Distribute via pip | `[project.entry-points."hermes_agent.plugins"]` |
| Register a gateway platform | `ctx.register_platform(...)` (Discord, Telegram, IRC, …) |
| Register image/video gen backend | `ctx.register_image_gen_provider(...)` / `ctx.register_video_gen_provider(...)` |
| Register a context-compression engine | `ctx.register_context_engine(engine)` |
| Register a memory backend | Subclass `MemoryProvider` in `plugins/memory/<name>/` (separate discovery) |
| Run a host-owned LLM call | `ctx.llm.complete(...)` / `ctx.llm.complete_structured(...)` — borrow the user's model + auth |
| Register an inference backend | `register_provider(ProviderProfile(...))` in `plugins/model-providers/<name>/` |

The TTS/STT backends, MCP servers, and Skills Hub taps are *config-driven* extension surfaces handled outside the Python plugin system (see Pluggable Interfaces below). Authoring guides for platform adapters, provider/memory/context-engine plugins are covered in the developer-guide pages those rows link to.

## Plugin Discovery

Hermes discovers plugins from five sources at startup. **Later sources override earlier ones on name collision**, so a user plugin with the same name as a bundled plugin replaces it:

| Source | Path | Use case |
|--------|------|----------|
| Bundled | `<repo>/plugins/` | Ships with Hermes — see [Built-in Plugins](hermes_built_in_plugins.md) |
| User | `~/.hermes/plugins/` | Personal plugins |
| Project | `.hermes/plugins/` | Project-specific (requires `HERMES_ENABLE_PROJECT_PLUGINS=true`) |
| pip | `hermes_agent.plugins` entry_points | Distributed packages |
| Nix | `services.hermes-agent.extraPlugins` / `extraPythonPackages` | NixOS declarative installs |

### Plugin Sub-Categories

Within each source, Hermes recognizes sub-category directories that route plugins to specialized discovery systems. The root `plugins/` is handled by the general `PluginManager`; the rest are loaded one directory level deeper or by their own loaders:

| Sub-directory | What it holds | Discovery system |
|---|---|---|
| `plugins/` (root) | General plugins — tools, hooks, slash/CLI commands, bundled skills | `PluginManager` (kind: `standalone`/`backend`) |
| `plugins/platforms/<name>/` | Gateway channel adapters (`ctx.register_platform()`) | `PluginManager` (kind: `platform`) |
| `plugins/image_gen/<name>/` | Image-generation backends | `PluginManager` (kind: `backend`) |
| `plugins/memory/<name>/` | Memory providers (subclass `MemoryProvider`) | Own loader (kind: `exclusive` — one active) |
| `plugins/context_engine/<name>/` | Context-compression engines | Own loader (one active at a time) |
| `plugins/model-providers/<name>/` | LLM provider profiles (`register_provider(...)`) | Own loader (lazy on first `get_provider_profile()`) |

User plugins at `~/.hermes/plugins/model-providers/<name>/` and `~/.hermes/plugins/memory/<name>/` override bundled plugins of the same name (last-writer-wins) — drop a directory in and it replaces the built-in with no repo edits.

## Plugins Are Opt-In (with a Few Exceptions)

**General plugins and user-installed backends are disabled by default.** Discovery finds them (so they appear in `hermes plugins` and `/plugins`), but nothing with hooks or tools loads until the plugin's name is added to `plugins.enabled` in `~/.hermes/config.yaml`. This stops third-party code from running without explicit consent:

```yaml
plugins:
  enabled:
    - my-tool-plugin
    - disk-cleanup
  disabled:       # optional deny-list — always wins if a name appears in both
    - noisy-plugin
```

The three CLI toggle commands (`hermes plugins`, `... enable`, `... disable`) are documented in [hermes_plugins_management](hermes_plugins_management.md).

**What the allow-list does NOT gate.** Several plugin kinds bypass `plugins.enabled` because they are part of Hermes' built-in surface and would break basic functionality if gated off: bundled *platform* plugins are auto-loaded (the channel turns on via `gateway.platforms.<name>.enabled`); bundled *backends* (image-gen, etc.) auto-load so the default "just works" (selection via `<category>.provider`); *memory providers* and *context engines* are all discovered with exactly one active (chosen by `memory.provider` / `context.engine`); *model providers* discover/register at the first `get_provider_profile()` call (user picks via `--provider`). In short: **bundled "always-works" infrastructure loads automatically; third-party general plugins are opt-in.** Pip-installed `backend` plugins and user-installed platforms are still opt-in via `plugins.enabled`.

**Migration.** On upgrade to opt-in plugins (config schema v21+), any user plugins already under `~/.hermes/plugins/` that weren't in `plugins.disabled` are **automatically grandfathered** into `plugins.enabled`, so existing setups keep working. Bundled standalone plugins are NOT grandfathered — even existing users must opt in explicitly (bundled platform/backend plugins never needed it because they were never gated).

## Available Hooks

Plugins register callbacks for lifecycle events via `ctx.register_hook(...)`. The system exposes hooks such as `pre_tool_call` / `post_tool_call` (before/after any tool), `pre_llm_call` / `post_llm_call` (once per turn around the LLM loop — `pre_llm_call` can return `{"context": "..."}` to inject context into the user message), the session-lifecycle hooks `on_session_start` / `on_session_end` / `on_session_finalize` / `on_session_reset`, `subagent_stop` (once per child after `delegate_task`), and `pre_gateway_dispatch` (gateway received a message, before auth + dispatch — can return `{"action": "skip" | "rewrite" | "allow", ...}`). The full callback signatures, return contracts, and examples are in [hermes_plugin_hook_reference](hermes_plugin_hook_reference.md), and the broader three-system hook model in [hermes_event_hooks](hermes_event_hooks.md).

## Plugin Types

Hermes has four kinds of plugins, differing in how they are selected and where they live:

| Type | What it does | Selection | Location |
|------|-------------|-----------|----------|
| **General plugins** | Add tools, hooks, slash/CLI commands | Multi-select (enable/disable) | `~/.hermes/plugins/` |
| **Memory providers** | Replace/augment built-in memory | Single-select (one active) | `plugins/memory/` |
| **Context engines** | Replace the built-in context compressor | Single-select (one active) | `plugins/context_engine/` |
| **Model providers** | Declare an inference backend (OpenRouter, Anthropic, …) | Multi-register, picked by `--provider` | `plugins/model-providers/` |

Memory providers and context engines are **provider plugins** — only one of each type can be active at a time. Model providers are also plugins but many load simultaneously, with the user picking one via `--provider` or `config.yaml`. General plugins can be enabled in any combination.

## Pluggable Interfaces — Where to Go for Each

Within "General plugins" the `PluginContext` exposes several distinct extension points, and Hermes also accepts extensions *outside* the Python plugin system. The decision is "pick the right surface for the integration style": a **Python plugin** for tools/hooks/slash-commands/CLI-commands/bundled-skills (`ctx.register_tool/hook/command/cli_command/skill`); a **provider/platform/backend plugin** for inference backends, gateway channels, memory/context-engine/image-gen/video-gen; and **config-driven or external surfaces** for the rest — **TTS/STT** backends declared under `tts.providers`/`stt.providers` with `type: command` (any CLI becomes a plugin without Python), **external tools via MCP** declared as `mcp_servers.<name>` (Hermes auto-discovers and registers the server's tools — see [hermes_event_hooks](hermes_event_hooks.md) for the related hook surface and the MCP feature page), **additional skill sources** via `hermes skills tap add <repo>`, **gateway event hooks** via `HOOK.yaml` + `handler.py` drop-in dirs, and **shell hooks** declared under `hooks:` in `config.yaml`. Not everything is a Python plugin — some surfaces intentionally use config-driven shell commands, some are external servers, and some are drop-in directories with their own manifest format.

## Injecting Messages

Plugins can inject messages into the active conversation with `ctx.inject_message()`:

```python
ctx.inject_message("New data arrived from the webhook", role="user")
```

**Signature:** `ctx.inject_message(content: str, role: str = "user") -> bool`. If the agent is **idle**, the message is queued as the next input and starts a new turn; if **mid-turn**, it interrupts the current operation (same as the user typing a new message and pressing Enter). For non-`"user"` roles the content is prefixed with `[role]` (e.g. `[system] ...`). Returns `True` if queued successfully, `False` if no CLI reference is available. `inject_message` is **only available in CLI mode** — in gateway mode there is no CLI reference and the method returns `False`. This enables plugins like remote-control viewers, messaging bridges, or webhook receivers to feed messages in from external sources.

**Source**: `inbox/hermes_agent_docs/user-guide/features/plugins.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
**Last Updated**: 2026-06-19
**Status**: Active
