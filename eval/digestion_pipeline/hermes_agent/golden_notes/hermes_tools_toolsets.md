---
tags:
  - resource
  - documentation
  - hermes_agent
  - tools
  - tool_registry
keywords:
  - tools and toolsets
  - built-in tool registry
  - toolset enable disable per platform
  - terminal backends
  - background process management
  - sudo support
topics:
  - Hermes Agent
  - Tools
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools
access_control_group: ["general"]
---

# Hermes Agent — Tools & Toolsets

## Overview

**Tools** are the functions that extend the Hermes agent's capabilities, and **toolsets** are the logical groupings that can be enabled or disabled per platform. This note documents the tool-registry model: the high-level tool categories Hermes ships with (web, X search, terminal/files, browser, media, agent orchestration, memory/recall, automation/delivery, integrations), how toolsets gate which tools are available, the six terminal backends the `terminal` tool can execute in, background-process management via the `process` tool, and sudo prompting. It is the category-level map — the authoritative code-derived per-tool and per-toolset registries live in the Reference docs (link-outs below), and the per-tool feature deep-dives (browser/TTS/vision/web-search, code-execution/delegation, MCP) live in their own pages.

## Available Tools

Hermes ships with a broad built-in tool registry covering web search, browser automation, terminal execution, file editing, memory, delegation, RL training, messaging delivery, Home Assistant, and more.

> **Note:** **Honcho cross-session memory** is available as a memory provider plugin (`plugins/memory/honcho/`), not as a built-in toolset. See [Memory Providers / Honcho](hermes_memory_providers_honcho.md) for installation.

High-level categories:

| Category | Examples | Description |
|----------|----------|-------------|
| **Web** | `web_search`, `web_extract` | Search the web and extract page content. |
| **X Search** | `x_search` | Search X (Twitter) posts and threads via xAI's built-in `x_search` Responses tool — gated on xAI credentials (SuperGrok OAuth or `XAI_API_KEY`); off by default, opt in via `hermes tools` → 🐦 X (Twitter) Search. |
| **Terminal & Files** | `terminal`, `process`, `read_file`, `patch` | Execute commands and manipulate files. |
| **Browser** | `browser_navigate`, `browser_snapshot`, `browser_vision` | Interactive browser automation with text and vision support. |
| **Media** | `vision_analyze`, `image_generate`, `text_to_speech` | Multimodal analysis and generation. |
| **Agent orchestration** | `todo`, `clarify`, `execute_code`, `delegate_task` | Planning, clarification, code execution, and subagent delegation. |
| **Memory & recall** | `memory`, `session_search` | Persistent memory and session search. |
| **Automation & delivery** | `cronjob`, `send_message` | Scheduled tasks with create/list/update/pause/resume/run/remove actions, plus outbound messaging delivery. |
| **Integrations** | `ha_*`, MCP server tools | Home Assistant, MCP, and other integrations. |

For the authoritative code-derived registry, see Built-in Tools Reference and Toolsets Reference (Reference docs, owned by the reference sub-plan — link-outs, not duplicated here).

> **Tip — Nous Tool Gateway:** Paid Nous Portal subscribers can use web search, image generation, TTS, and browser automation through the [Tool Gateway](hermes_tool_gateway.md) — no separate API keys needed. Run `hermes model` to enable it, or configure individual tools with `hermes tools`.

## Using Toolsets

```bash
# Use specific toolsets
hermes chat --toolsets "web,terminal"

# See all available tools
hermes tools

# Configure tools per platform (interactive)
hermes tools
```

Common toolsets include `web`, `search`, `terminal`, `file`, `browser`, `vision`, `image_gen`, `moa`, `skills`, `tts`, `todo`, `memory`, `session_search`, `cronjob`, `code_execution`, `delegation`, `clarify`, `homeassistant`, `messaging`, `spotify`, `discord`, `discord_admin`, `debugging`, and `safe`.

The full set — including platform presets such as `hermes-cli`, `hermes-telegram`, and dynamic MCP toolsets like `mcp-<server>` — is in the Toolsets Reference (Reference docs).

## Terminal Backends

The `terminal` tool can execute commands in different environments:

| Backend | Description | Use Case |
|---------|-------------|----------|
| `local` | Run on your machine (default) | Development, trusted tasks |
| `docker` | Isolated containers | Security, reproducibility |
| `ssh` | Remote server | Sandboxing, keep agent away from its own code |
| `singularity` | HPC containers | Cluster computing, rootless |
| `modal` | Cloud execution | Serverless, scale |
| `daytona` | Cloud sandbox workspace | Persistent remote dev environments |

The backend is selected in `~/.hermes/config.yaml` under `terminal:` (the full `terminal:` config block — `backend`/`cwd`/`timeout`/`docker_image`/`container_*`/`docker_forward_env` and the per-backend credential variables — is the configuration sub-plan's owned reference). The source page's representative Docker block:

```yaml
terminal:
  backend: docker
  docker_image: python:3.11-slim
```

**Docker backend — one persistent container, shared across the whole process.** Hermes starts a single long-lived container on first use (`docker run -d ... sleep 2h`) and routes every terminal, file, and `execute_code` call through `docker exec` into that same container. Working-directory changes, installed packages, environment tweaks, and files written to `/workspace` all carry over from one tool call to the next, across `/new`, `/reset`, and `delegate_task` subagents, for the lifetime of the Hermes process. The container is stopped and removed on shutdown — so it behaves like a persistent sandbox VM, not a fresh container per command. The `container_persistent` flag controls whether `/workspace` and `/root` survive across Hermes restarts.

**SSH backend** is recommended for security — the agent can't modify its own code. Credentials (`TERMINAL_SSH_HOST`/`TERMINAL_SSH_USER`/`TERMINAL_SSH_KEY`) go in `~/.hermes/.env`. **Singularity/Apptainer** pre-builds a SIF for parallel workers; **Modal** is serverless cloud execution; both are selected via `hermes config set terminal.backend <name>`.

**Container resources & security** — all container backends (docker/singularity/modal/daytona) accept `container_cpu`/`container_memory`/`container_disk`/`container_persistent` knobs and run with security hardening: read-only root filesystem (Docker), all Linux capabilities dropped, no privilege escalation, PID limits (256 processes), full namespace isolation, and a persistent workspace via volumes rather than a writable root layer. Docker can optionally receive an explicit env allowlist via `terminal.docker_forward_env`, but forwarded variables are visible to commands inside the container and should be treated as exposed to that session.

## Background Process Management

Start background processes and manage them with the `process` tool:

```python
terminal(command="pytest -v tests/", background=true)
# Returns: {"session_id": "proc_abc123", "pid": 12345}

# Then manage with the process tool:
process(action="list")       # Show all running processes
process(action="poll", session_id="proc_abc123")   # Check status
process(action="wait", session_id="proc_abc123")   # Block until done
process(action="log", session_id="proc_abc123")    # Full output
process(action="kill", session_id="proc_abc123")   # Terminate
process(action="write", session_id="proc_abc123", data="y")  # Send input
```

PTY mode (`pty=true`) enables interactive CLI tools like Codex and Claude Code.

## Sudo Support

If a command needs sudo, you'll be prompted for your password (cached for the session). Or set `SUDO_PASSWORD` in `~/.hermes/.env`.

> **Warning:** On messaging platforms, if sudo fails, the output includes a tip to add `SUDO_PASSWORD` to `~/.hermes/.env`.

**Source**: `inbox/hermes_agent_docs/user-guide/features/tools.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/tools
**Last Updated**: 2026-06-19
**Status**: Active
