---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugins
  - extension_surfaces
keywords:
  - specialized plugin types
  - model provider platform memory context-engine image-gen
  - non-python extension surfaces
  - mcp gateway-hooks shell-hooks skill-taps tts-stt
  - register_provider register_platform register_memory_provider
  - pip nixos distribution
topics:
  - Hermes Agent
  - Plugins
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
access_control_group: ["general"]
---

# Hermes Plugin Types & Extension Surfaces

## Overview

This is the **extension-surface map** for Hermes Agent: the catalog of every pluggable interface beyond the general tool/hook plugin built in the [calculator tutorial](hermes_build_plugin_tutorial.md). Hermes exposes two families of extension. First, **five specialized Python plugin types** — model-provider, platform adapter, memory provider, context engine, and image-generation backend — each a directory under `plugins/<category>/<name>/` (bundled) or `~/.hermes/plugins/<category>/<name>/` (user) with its own `register_*` contract. Second, **config-driven and drop-in non-Python surfaces** — MCP servers, gateway event hooks, shell hooks, skill taps, and TTS/STT command templates — that extend Hermes with no Python plugin at all. Picking the right surface is the first decision when extending Hermes: the general plugin guide adds custom tools/hooks/commands; everything else routes to one of these specialized contracts or drop-in styles. The note closes with pip + NixOS distribution and the common-mistakes checklist.

## If you want to add… (routing map)

Hermes has several distinct pluggable interfaces — some use Python `register_*` APIs, others are config-driven or drop-in directories. This map is the first thing to consult:

| If you want to add… | Surface |
|---|---|
| Custom tools, hooks, slash commands, skills, or CLI subcommands | The general plugin surface (the [build-plugin tutorial](hermes_build_plugin_tutorial.md) + [extras/hooks](hermes_plugin_extensions_hooks.md)) |
| An **LLM / inference backend** (new provider) | Model Provider Plugins |
| A **gateway channel** (Discord/Telegram/IRC/Teams/etc.) | Platform Adapters |
| A **memory backend** (Honcho/Mem0/Supermemory/etc.) | Memory Provider Plugins |
| A **context-compression engine** | Context Engine Plugins |
| An **image-generation backend** | Image Generation Provider Plugins |
| A **TTS / STT backend** (any CLI) | Config-driven command templates — no Python needed |
| **External tools via MCP** | Declare `mcp_servers.<name>` in `config.yaml` |
| **Gateway event hooks** | Drop `HOOK.yaml` + `handler.py` into `~/.hermes/hooks/<name>/` |
| **Shell hooks** (run a shell command on events) | Declare under `hooks:` in `config.yaml` |
| **Additional skill sources** | `hermes skills tap add <repo>` |

The specialized Python types use `register_*` APIs; the config-driven (TTS, STT, MCP, shell hooks) and drop-in directory (gateway hooks) styles use no Python.

## Specialized plugin types

Hermes has five specialized plugin types beyond the general surface. Each ships as a directory under `plugins/<category>/<name>/` (bundled) or `~/.hermes/plugins/<category>/<name>/` (user). The contract differs by category — pick the one you need, then read its full guide.

**Model provider plugins — add an LLM backend.** Drop a profile into `plugins/model-providers/<name>/`. The profile is lazy-discovered the first time anything calls `get_provider_profile()` or `list_providers()` — `auth.py`, `config.py`, `doctor.py`, `models.py`, `runtime_provider.py`, and the chat_completions transport auto-wire to it. User plugins override bundled ones by name. Overridable hooks include `prepare_messages`, `build_extra_body`, `build_api_kwargs_extras`, and `fetch_models`.

```python
# plugins/model-providers/acme/__init__.py
from providers import register_provider
from providers.base import ProviderProfile

register_provider(ProviderProfile(
    name="acme",
    aliases=("acme-inference",),
    display_name="Acme Inference",
    env_vars=("ACME_API_KEY", "ACME_BASE_URL"),
    base_url="https://api.acme.example.com/v1",
    auth_type="api_key",
    default_aux_model="acme-small-fast",
    fallback_models=("acme-large-v3", "acme-medium-v3"),
))
```

**Platform plugins — add a gateway channel.** Drop an adapter subclassing `BasePlatformAdapter` into `plugins/platforms/<name>/`, then call `ctx.register_platform(...)`. The manifest needs `kind: platform`. `env_enablement_fn` auto-populates `PlatformConfig.extra` from env so env-only setups appear in `hermes gateway status`, and `cron_deliver_env_var` opts the platform into cron delivery (`deliver=<name>`). `plugins/platforms/irc/` is the stdlib-only reference example.

```python
# plugins/platforms/myplatform/adapter.py
from gateway.platforms.base import BasePlatformAdapter

class MyPlatformAdapter(BasePlatformAdapter):
    async def connect(self): ...
    async def send(self, chat_id, text): ...
    async def disconnect(self): ...

def register(ctx):
    ctx.register_platform(
        name="myplatform",
        label="MyPlatform",
        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),
        check_fn=lambda: bool(__import__("os").environ.get("MYPLATFORM_TOKEN")),
        required_env=["MYPLATFORM_TOKEN"],
        cron_deliver_env_var="MYPLATFORM_HOME_CHANNEL",
        emoji="💬",
        platform_hint="You are chatting via MyPlatform. Keep responses concise.",
    )
```

**Memory provider plugins — add a cross-session knowledge backend.** Implement the `MemoryProvider` ABC (`name`, `is_available`, `initialize`, `sync_turn`, `prefetch`, `get_tool_schemas`) in `plugins/memory/<name>/`, then `ctx.register_memory_provider(...)`. Memory providers are **single-select** — only one is active at a time, chosen via `memory.provider` in `config.yaml`, and are auto-detected as `kind: exclusive`.

```python
# plugins/memory/my-memory/__init__.py
from agent.memory_provider import MemoryProvider

class MyMemoryProvider(MemoryProvider):
    @property
    def name(self) -> str:
        return "my-memory"

    def is_available(self) -> bool:
        import os
        return bool(os.environ.get("MY_MEMORY_API_KEY"))

    def sync_turn(self, user_content, assistant_content, *,
                  session_id="", messages=None) -> None: ...

    def prefetch(self, query, *, session_id="") -> str: ...

    def get_tool_schemas(self) -> list[dict]:
        return []   # required @abstractmethod

def register(ctx):
    ctx.register_memory_provider(MyMemoryProvider())
```

**Context engine plugins — replace the context compressor.** Implement the `ContextEngine` ABC (`name`, `update_from_response`, `should_compress`, `compress`) and `ctx.register_context_engine(...)`. Also **single-select** — chosen via `context.engine` in `config.yaml`.

**Image-generation backends.** Implement the `ImageGenProvider` ABC (`name`, `is_available`, `generate`) in `plugins/image_gen/<name>/` and `ctx.register_image_gen_provider(...)`; `generate()` returns `success_response(...)`/`error_response(...)`. Reference examples: `plugins/image_gen/openai/`, `plugins/image_gen/openai-codex/`, `plugins/image_gen/xai/`.

## Non-Python extension surfaces

Hermes also accepts extensions that aren't Python plugins at all. The sections below sketch each authoring style.

**MCP servers — register external tools.** Model Context Protocol servers register their own tools into Hermes without any Python plugin. Declare them in `~/.hermes/config.yaml`; Hermes connects at startup, lists each server's tools, and registers them alongside built-ins — the LLM sees them exactly like any other tool.

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    timeout: 120

  linear:
    url: "https://mcp.linear.app/sse"
    auth:
      type: "oauth"
```

**Gateway event hooks — fire on lifecycle events.** Drop a manifest + handler into `~/.hermes/hooks/<name>/`. Events include `gateway:startup`, `session:start`, `session:end`, `session:reset`, `agent:start`, `agent:step`, `agent:end`, and wildcard `command:*`. Errors in hooks are caught and logged — they never block the main pipeline.

```yaml
# ~/.hermes/hooks/long-task-alert/HOOK.yaml
name: long-task-alert
description: Send a push notification when a long task finishes
events:
  - agent:end
```

**Shell hooks — run a shell command on tool calls.** To run a script when a tool fires (notifications, audit logs, desktop alerts, auto-formatters), use shell hooks in `config.yaml` — no Python required. Supports the same events as Python plugin hooks (`pre_tool_call`, `post_tool_call`, `pre_llm_call`, `post_llm_call`, `on_session_start`, `on_session_end`, `pre_gateway_dispatch`) plus structured JSON output for `pre_tool_call` blocking decisions.

```yaml
hooks:
  - event: post_tool_call
    command: "notify-send 'Tool ran: {tool_name}'"
    when:
      tools: [terminal, patch, write_file]
```

**Skill sources — add a custom skill registry.** Add a GitHub repo of skills (or a community index beyond the built-in sources) as a **tap**: `hermes skills tap add myorg/skills-repo`, then `search`/`install` with `--source`/by full path. Publishing your own tap is just a GitHub repo with `skills/<skill-name>/SKILL.md` directories — no server or registry signup needed.

**TTS / STT via command templates.** Any CLI that reads/writes audio or text can be plugged in through `config.yaml` — no Python code. A `tts` provider of `type: command` runs a templated shell command; for STT, point `HERMES_LOCAL_STT_COMMAND` at a shell template. Supported placeholders: `{input_path}`, `{output_path}`, `{format}`, `{voice}`, `{model}`, `{speed}` (TTS); `{input_path}`, `{output_dir}`, `{language}`, `{model}` (STT). Any path-interacting CLI is automatically a plugin.

## Distribute via pip

For sharing plugins publicly, add an entry point to your Python package — under `[project.entry-points."hermes_agent.plugins"]` in `pyproject.toml`, map a plugin name to its package module (e.g. `my-plugin = "my_plugin_package"`). The plugin is auto-discovered on the next `hermes` startup.

## Distribute for NixOS

NixOS users can install your plugin declaratively. **Entry-point plugins** (recommended for distribution) require a `pyproject.toml` with entry points and are added via `services.hermes-agent.extraPythonPackages` (a `buildPythonPackage` with `format = "pyproject"`). **Directory plugins** need no `pyproject.toml` and are added via `services.hermes-agent.extraPlugins` (a `fetchFromGitHub`). See the Nix Setup guide for complete documentation including overlay usage and collision checking.

## Common mistakes

The recurring authoring errors across plugin types:

- **Handler doesn't return a JSON string** — return `json.dumps({"result": 42})`, not a raw dict.
- **Missing `**kwargs` in the handler signature** — `def handler(args, **kwargs)`, not `def handler(args)`; Hermes may pass extra context in the future.
- **Handler raises exceptions** — catch all and return error JSON instead of letting the exception propagate and fail the tool call.
- **Schema description too vague** — `"Does stuff"` gives the model nothing; describe exactly what the tool does and when to use it (operators, functions, units) so the LLM routes to it correctly.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
**Last Updated**: 2026-06-19
**Status**: Active
