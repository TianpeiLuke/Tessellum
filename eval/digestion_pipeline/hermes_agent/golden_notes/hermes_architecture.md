---
tags:
  - resource
  - documentation
  - hermes_agent
  - architecture
  - internals
keywords:
  - hermes architecture
  - system overview
  - major subsystems
  - data flow
  - aiagent run_agent
  - file dependency chain
  - design principles
topics:
  - Hermes Agent
  - Architecture
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
access_control_group: ["general"]
---

# Hermes Agent — Architecture

## Overview

This is the top-level map of Hermes Agent internals: the single orientation page that shows how every subsystem fits together before you dive into a subsystem-specific doc. The whole codebase converges on one class — `AIAgent` in `run_agent.py` — which six entry points (CLI, Gateway, ACP, Batch Runner, API Server, Python Library) all feed. Inside `AIAgent`, three sub-blocks do the work of each turn (a **Prompt Builder**, a **Provider Resolution** step over three API modes, and a **Tool Dispatch** path into the registry), backed by **Compression & Caching** and two backends — **Session Storage** (SQLite + FTS5) and **Tool Backends** (terminal/browser/web/MCP/file/vision). The page enumerates the ten major subsystems with a recommended reading order, six design principles that keep the core platform-agnostic, and the import-time file-dependency chain that makes tool registration happen before any agent instance exists. Use it to orient yourself in the codebase, then read the subsystem deep-dives.

## System Overview

The architecture is a layered convergence: six entry points → one `AIAgent` → three per-turn sub-blocks → two backends.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        Entry Points                                  │
│                                                                      │
│  CLI (cli.py)    Gateway (gateway/run.py)    ACP (acp_adapter/)     │
│  Batch Runner    API Server                  Python Library          │
└──────────┬──────────────┬───────────────────────┬───────────────────┘
           │              │                       │
           ▼              ▼                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     AIAgent (run_agent.py)                          │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ Prompt       │  │ Provider     │  │ Tool         │               │
│  │ Builder      │  │ Resolution   │  │ Dispatch     │               │
│  │ (prompt_     │  │ (runtime_    │  │ (model_      │               │
│  │  builder.py) │  │  provider.py)│  │  tools.py)   │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                       │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐               │
│  │ Compression  │  │ 3 API Modes  │  │ Tool Registry│               │
│  │ & Caching    │  │ chat_compl.  │  │ (registry.py)│               │
│  │              │  │ codex_resp.  │  │ 70+ tools    │               │
│  │              │  │ anthropic    │  │ 28 toolsets  │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
└─────────┴─────────────────┴─────────────────┴───────────────────────┘
           │                                    │
           ▼                                    ▼
┌───────────────────┐              ┌──────────────────────┐
│ Session Storage   │              │ Tool Backends         │
│ (SQLite + FTS5)   │              │ Terminal (6 backends) │
│ hermes_state.py   │              │ Browser (5 backends)  │
│ gateway/session.py│              │ Web (4 backends)      │
└───────────────────┘              │ MCP (dynamic)         │
                                   │ File, Vision, etc.    │
                                   └──────────────────────┘
```

## Directory Structure

The package root holds the large hot files — `run_agent.py` (the `AIAgent` conversation loop), `cli.py` (`HermesCLI` terminal UI), `model_tools.py` (tool discovery/schema collection/dispatch), `toolsets.py` (tool groupings + platform presets), `hermes_state.py` (the SQLite session/state DB with FTS5), `hermes_constants.py` (`HERMES_HOME` + profile-aware paths), and `batch_runner.py` (batch trajectory generation) — and partitions the rest into subsystem directories:

- **`agent/`** — agent internals: `prompt_builder.py` (system-prompt assembly), `context_engine.py` (the pluggable `ContextEngine` ABC), `context_compressor.py` (default lossy-summarization engine), `prompt_caching.py` (Anthropic prompt caching), `auxiliary_client.py` (auxiliary LLM for vision/summarization side tasks), `model_metadata.py` / `models_dev.py` (model context lengths + models.dev registry), `anthropic_adapter.py`, `display.py`, `skill_commands.py`, `memory_manager.py` / `memory_provider.py`, and `trajectory.py`.
- **`hermes_cli/`** — CLI subcommands and setup: `main.py` (all `hermes` subcommands), `config.py` (`DEFAULT_CONFIG`/`OPTIONAL_ENV_VARS`/migration), `commands.py` (the central `COMMAND_REGISTRY` slash-command definitions), `auth.py` (`PROVIDER_REGISTRY` + credential resolution), `runtime_provider.py` (provider → api_mode + credentials), `models.py`/`model_switch.py`, `setup.py` (interactive wizard), `plugins.py` (`PluginManager` discovery/loading/hooks), `callbacks.py` (terminal clarify/sudo/approval), and `gateway.py`.
- **`tools/`** — one file per tool, each self-registering: `registry.py` (the central registry), `approval.py` (dangerous-command detection), `terminal_tool.py`, `file_tools.py`, `web_tools.py`, `browser_tool.py` (10 browser tools), `code_execution_tool.py`, `delegate_tool.py` (subagent delegation), `mcp_tool.py`, and `environments/` (terminal backends: local, docker, ssh, modal, daytona, singularity).
- **`gateway/`** — the messaging-platform gateway: `run.py` (`GatewayRunner` dispatch), `session.py` (`SessionStore`), `delivery.py`, `pairing.py` (DM-pairing authorization), `hooks.py`, `mirror.py`, `status.py` (token locks + profile-scoped process tracking), and `platforms/` (20 adapters: telegram, discord, slack, whatsapp, signal, matrix, mattermost, email, sms, dingtalk, feishu, wecom, weixin, bluebubbles, qqbot, homeassistant, webhook, api_server, yuanbao, …).
- **`acp_adapter/`** (ACP server for VS Code/Zed/JetBrains), **`cron/`** (scheduler: `jobs.py`, `scheduler.py`), **`plugins/memory/`** + **`plugins/context_engine/`** (single-select plugin slots), **`skills/`** + **`optional-skills/`**, **`website/`** (Docusaurus docs), and **`tests/`** (~25,000 tests across ~1,250 files).

## Data Flow

There are three execution paths, all converging on `AIAgent.run_conversation()`.

```text
### CLI Session
User input → HermesCLI.process_input()
  → AIAgent.run_conversation()
    → prompt_builder.build_system_prompt()
    → runtime_provider.resolve_runtime_provider()
    → API call (chat_completions / codex_responses / anthropic_messages)
    → tool_calls? → model_tools.handle_function_call() → loop
    → final response → display → save to SessionDB

### Gateway Message
Platform event → Adapter.on_message() → MessageEvent
  → GatewayRunner._handle_message()
    → authorize user → resolve session key
    → create AIAgent with session history
    → AIAgent.run_conversation()
    → deliver response back through adapter

### Cron Job
Scheduler tick → load due jobs from jobs.json
  → create fresh AIAgent (no history)
  → inject attached skills as context
  → run job prompt → deliver response to target platform
  → update job state and next_run
```

The CLI path is interactive (one user, terminal display). The gateway path adds authorization and session-key resolution before constructing the agent with prior history. The cron path is fully isolated — a fresh `AIAgent` with no history, attached skills injected as context, and delivery to any target platform.

## Recommended Reading Order

For a reader new to the codebase, the page prescribes: (1) **this page** to orient → (2) [Agent Loop Internals](hermes_agent_loop.md) (how `AIAgent` works) → (3) [Prompt Assembly](hermes_prompt_assembly.md) → (4) [Provider Runtime Resolution](hermes_provider_runtime.md) → (5) Adding Providers (extending guide) → (6) [Tools Runtime](hermes_tools_runtime.md) → (7) [Session Storage](hermes_session_storage.md) → (8) [Gateway Internals](hermes_gateway_internals.md) → (9) [Context Compression & Prompt Caching](hermes_context_compression_caching.md) → (10) [ACP Internals](hermes_acp_internals.md).

## Major Subsystems

Ten subsystems, each with its own deep-dive:

- **Agent Loop** — the synchronous orchestration engine (`AIAgent` in `run_agent.py`): provider selection, prompt construction, tool execution, retries, fallback, callbacks, compression, and persistence across three API modes.
- **Prompt System** — `system_prompt.py` + `prompt_builder.py` assemble the ordered tiers (`stable` → `context` → `volatile`: identity/tool-guidance/skills, then context files, then memory/profile/timestamp); `prompt_caching.py` applies Anthropic cache breakpoints; `context_compressor.py` summarizes middle turns above thresholds.
- **Provider Resolution** — a shared runtime resolver used by CLI, gateway, cron, ACP, and auxiliary calls, mapping `(provider, model)` → `(api_mode, api_key, base_url)` across 18+ providers, OAuth flows, credential pools, and alias resolution.
- **Tool System** — `tools/registry.py` with 70+ tools across ~28 toolsets, each file self-registering at import time; schema collection, dispatch, availability checking, error wrapping; terminal tools support 6 backends (local, Docker, SSH, Daytona, Modal, Singularity).
- **Session Persistence** — SQLite session storage with FTS5 full-text search, lineage tracking (parent/child across compressions), per-platform isolation, and atomic writes with contention handling.
- **Messaging Gateway** — a long-running process with 20 platform adapters, unified session routing, user authorization (allowlists + DM pairing), slash-command dispatch, hooks, cron ticking, and background maintenance.
- **Plugin System** — three discovery sources (user `~/.hermes/plugins/`, project `.hermes/plugins/`, pip entry points) registering tools/hooks/CLI commands through a context API; two single-select specialized types (memory providers, context engines), configured via `hermes plugins` or `config.yaml`.
- **Cron** — first-class agent tasks (not shell tasks): JSON-stored jobs, multiple schedule formats, attachable skills/scripts, delivery to any platform.
- **ACP Integration** — exposes Hermes as an editor-native agent over stdio/JSON-RPC for VS Code, Zed, and JetBrains.
- **Trajectories** — generates ShareGPT-format trajectories from agent sessions for training-data generation.

## Design Principles

| Principle | What it means in practice |
|-----------|--------------------------|
| **Prompt stability** | System prompt doesn't change mid-conversation. No cache-breaking mutations except explicit user actions (`/model`). |
| **Observable execution** | Every tool call is visible to the user via callbacks. Progress updates in CLI (spinner) and gateway (chat messages). |
| **Interruptible** | API calls and tool execution can be cancelled mid-flight by user input or signals. |
| **Platform-agnostic core** | One `AIAgent` class serves CLI, gateway, ACP, batch, and API server. Platform differences live in the entry point, not the agent. |
| **Loose coupling** | Optional subsystems (MCP, plugins, memory providers, RL environments) use registry patterns and `check_fn` gating, not hard dependencies. |
| **Profile isolation** | Each profile (`hermes -p <name>`) gets its own `HERMES_HOME`, config, memory, sessions, and gateway PID. Multiple profiles run concurrently. |

## File Dependency Chain

```text
tools/registry.py  (no deps — imported by all tool files)
       ↑
tools/*.py  (each calls registry.register() at import time)
       ↑
model_tools.py  (imports tools/registry + triggers tool discovery)
       ↑
run_agent.py, cli.py, batch_runner.py, environments/
```

This chain means tool registration happens at import time, before any agent instance is created. Any `tools/*.py` file with a top-level `registry.register()` call is auto-discovered — no manual import list needed.

**Source**: `inbox/hermes_agent_docs/developer-guide/architecture.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
**Last Updated**: 2026-06-19
**Status**: Active
