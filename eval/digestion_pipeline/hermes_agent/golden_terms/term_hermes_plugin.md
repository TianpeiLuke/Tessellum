---
tags:
  - resource
  - terminology
  - agent_systems
  - plugin_system
keywords:
  - Hermes Plugin
  - Hermes plugin system
  - register(ctx)
  - PluginContext
  - plugin.yaml
  - ctx.register_tool
  - ~/.hermes/plugins
topics:
  - Agent extensibility
  - Plugin systems
  - AI agent tooling
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
---

# Hermes Plugin

## Definition

A **Hermes plugin** is a drop-in Python extension that adds custom tools, lifecycle hooks, slash commands, CLI subcommands, bundled skills, and backend providers to the [Hermes Agent](https://hermes-agent.nousresearch.com) (Nous Research) **without modifying core code**. A plugin is a directory under a discovery path (e.g. `~/.hermes/plugins/<name>/`) containing a `plugin.yaml` manifest and Python code whose `__init__.py` exposes a single entry function, `register(ctx)`. At startup Hermes scans the discovery paths, loads each enabled plugin's module, and calls `register(ctx)` once — wiring the plugin's schemas to handlers so the model can call its tools alongside built-in ones immediately.

The plugin system is the primary supported extension surface for "I want a tool/hook for myself, my team, or one project" — distinct from editing Hermes' in-tree core tools. It solves the problem of letting end users grow an agent's capability set safely and incrementally: the host passes a `PluginContext` (`ctx`) object whose `ctx.*` methods are the only sanctioned registration API, and an opt-in allow-list (`plugins.enabled` in `config.yaml`) ensures arbitrary third-party code never runs without explicit consent.

## Context

Hermes plugins are used across the agent's runtime surfaces. Registered **tools** appear to the model in the same registry as built-in tools; **hooks** fire on agent/gateway/session lifecycle events; **slash commands** (`/name`) work in both the CLI and the messaging gateway; and **provider plugins** (memory, context-compression, image/video-gen, model providers) plug specialized backends into Hermes' provider registries. The bundled in-tree plugins (`disk-cleanup`, `security-guidance`, `observability/langfuse`, the kanban dashboard, etc.) use the identical surface, just maintained inside the repo. The plugin loader (`PluginManager`) and the `register(ctx)` contract are the foundation that the Hermes hook system, the kanban dashboard plugin, and the gateway platform adapters all build on.

## Key Characteristics

- **`register(ctx)` entry point**: each plugin's `__init__.py` defines `def register(ctx): ...`; Hermes calls it once at load to wire schemas to handlers. The `plugin.yaml` manifest declares `name`, `version`, `description`, optional `provides_tools`/`provides_hooks`, and `requires_env` (env-var gating, prompted at install).
- **`ctx.*` capability surface**: `register_tool`, `register_hook`, `register_command` (slash), `register_cli_command` (`hermes <plugin> <sub>`), `dispatch_tool`, `inject_message` (CLI-only), `register_skill` (namespaced `plugin:skill`), and provider registrars (`register_platform`, `register_image_gen_provider`, `register_video_gen_provider`, `register_context_engine`). `ctx.llm.complete(...)` borrows the user's active model/auth for a one-shot host-owned completion.
- **Five discovery sources** (later overrides earlier on name collision): bundled `<repo>/plugins/`, user `~/.hermes/plugins/`, project `.hermes/plugins/` (gated by `HERMES_ENABLE_PROJECT_PLUGINS=true`), pip `hermes_agent.plugins` entry points, and NixOS `extraPlugins`. Sub-category directories (`platforms/`, `image_gen/`, `memory/`, `context_engine/`, `model-providers/`) route to specialized loaders.
- **Four plugin kinds**: general plugins (multi-select), memory providers (single-select), context engines (single-select), and model providers (multi-register, one picked at a time). Memory + context engines are *provider plugins* — exactly one active each.
- **Opt-in by default**: general plugins and user backends are discovered but do not load until added to `plugins.enabled`; a `disabled` deny-list always wins. Bundled "always-works" infrastructure (platforms, default backends, providers) bypasses the allow-list and is selected via `config.yaml` keys instead. On upgrade to schema v21+, pre-existing user plugins are grandfathered into `enabled`.
- **Not the only surface**: config-driven shell commands (TTS/STT, shell hooks), external MCP servers, and drop-in gateway hooks (`HOOK.yaml`+`handler.py`) are intentionally *not* Python plugins — the docs' "pluggable interfaces" table routes each integration to the right surface.

## Related Terms


## References

- [Hermes Agent — Plugins (user guide)](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [Hermes Agent — Build a Hermes Plugin (guide)](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin)
- [Hermes Agent — Built-in Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins)
- [VS Code Extension API — contribution points and activation](https://code.visualstudio.com/api/references/contribution-points)
