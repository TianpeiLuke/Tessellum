---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - acp
keywords:
  - openclaw acp agents
  - agent client protocol backend
  - acpx external harness
  - acp versus sub-agents
  - supported harness targets
  - how acp runs claude code
  - bound sessions mental model
  - runtime acp sessions_spawn
topics:
  - OpenClaw
  - ACP (Agent Client Protocol)
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/acp-agents
access_control_group: ["general"]
---

# OpenClaw — ACP Agents: The External-Harness Backend

## Overview

This note explains the **ACP backend concept** in OpenClaw: what Agent Client Protocol (ACP) sessions are, why they exist as a distinct path from the native Codex runtime and from OpenClaw-native sub-agents, which external coding harnesses are supported, and the mental model for binding an ACP session to a chat surface. It mirrors the conceptual sections of the `tools/acp-agents` source page — the intro note, "Which page do I want?", "Does this work out of the box?", "Supported harness targets", "ACP versus sub-agents", "How ACP runs Claude Code", and "Bound sessions › Mental model". The operator spawn/bind workflow, the runtime delivery/controls layer, and the acpx plugin install/permission setup are split into sibling notes (`oc_tools_acp_agents_spawn_bind`, `oc_tools_acp_agents_runtime`, `oc_tools_acp_agents_setup`).

## What ACP Is

[Agent Client Protocol (ACP)](https://agentclientprotocol.com/) sessions let OpenClaw run external coding harnesses — for example Claude Code, Cursor, Copilot, Droid, OpenClaw ACP, OpenCode, Gemini CLI, and other supported ACPX harnesses — *through* an **ACP backend plugin**. Each ACP session spawn is tracked as a [background task](https://docs.openclaw.ai/automation/tasks), so an ACP run behaves like background work rather than an inline turn.

The key positioning rule: **ACP is the external-harness path, not the default Codex path.** The native Codex app-server plugin owns the `/codex ...` controls and the default `openai/gpt-*` embedded runtime for agent turns; ACP owns the `/acp ...` controls and `sessions_spawn({ runtime: "acp" })` sessions. ACP is also distinct from connecting an external editor as an MCP client: if you want Codex or Claude Code to connect as an external MCP client directly to existing OpenClaw channel conversations, you use `openclaw mcp serve` instead of ACP.

## Which Page Do I Want?

The source page opens with a routing table to disambiguate ACP from adjacent features. This note (the ACP-agents concept layer) corresponds to the "Run … *through* OpenClaw" row.

| You want to… | Use this | Notes |
| --- | --- | --- |
| Bind or control Codex in the current conversation | `/codex bind`, `/codex threads` | Native Codex app-server path when the `codex` plugin is enabled; includes bound chat replies, image forwarding, model/fast/permissions, stop, and steer controls. ACP is an explicit fallback |
| Run Claude Code, Gemini CLI, explicit Codex ACP, or another external harness *through* OpenClaw | This page (the ACP backend) | Chat-bound sessions, `/acp spawn`, `sessions_spawn({ runtime: "acp" })`, background tasks, runtime controls |
| Expose an OpenClaw Gateway session *as* an ACP server for an editor or client | `openclaw acp` (bridge mode) | IDE/client talks ACP to OpenClaw over stdio/WebSocket |
| Reuse a local AI CLI as a text-only fallback model | CLI Backends | Not ACP. No OpenClaw tools, no ACP controls, no harness runtime |

## Does This Work Out of the Box?

Yes, after installing the official ACP runtime plugin (`@openclaw/acpx`) and enabling it; source checkouts can use the local `extensions/acpx` workspace plugin after `pnpm install`, and `/acp doctor` runs a readiness check.

```bash
openclaw plugins install @openclaw/acpx
openclaw config set plugins.entries.acpx.enabled true
```

Conceptually important: OpenClaw only teaches agents about ACP spawning when ACP is **truly usable**. Four conditions must all hold — ACP must be enabled, dispatch must not be disabled, the current session must not be sandbox-blocked, and a runtime backend must be loaded. If those conditions are not met, the ACP plugin skills and `sessions_spawn` ACP guidance stay hidden, so the agent does not suggest an unavailable backend. A first-run gotcha: if `plugins.allow` is set, it acts as a restrictive plugin inventory and **must** include `acpx`, otherwise the installed ACP backend is intentionally blocked and `/acp doctor` reports the missing allowlist entry. By default, OpenClaw plugin tools and built-in OpenClaw tools are **not** exposed to ACP harnesses; the explicit MCP bridges (documented on the setup page) are enabled only when the harness should call those tools directly.

The responsibility split is the core mental hinge of the whole feature: ACP launches a real external harness process where **OpenClaw owns** routing, background-task state, delivery, bindings, and policy, while the **harness owns** its provider login, model catalog, filesystem behavior, and native tools. Before blaming OpenClaw for a failure, the page advises verifying that `/acp doctor` reports an enabled healthy backend, the target id is allowed by `acp.allowedAgents` (when that allowlist is set), the harness command can start on the Gateway host, provider auth is present for that harness, the selected model exists for that harness (model ids are *not* portable across harnesses), the requested `cwd` exists and is accessible, and the permission mode matches the work (non-interactive sessions cannot click native permission prompts).

## Supported Harness Targets

With the `acpx` backend, these harness ids are valid `/acp spawn <id>` or `sessions_spawn({ runtime: "acp", agentId: "<id>" })` targets:

| Harness id | Typical backend | Notes |
| --- | --- | --- |
| `claude` | Claude Code ACP adapter | Requires Claude Code auth on the host. |
| `codex` | Codex ACP adapter | Explicit ACP fallback only when native `/codex` is unavailable or ACP is requested. |
| `copilot` | GitHub Copilot ACP adapter | Requires Copilot CLI/runtime auth. |
| `cursor` | Cursor CLI ACP (`cursor-agent acp`) | Override the acpx command if a local install exposes a different ACP entrypoint. |
| `droid` | Factory Droid CLI | Requires Factory/Droid auth or `FACTORY_API_KEY` in the harness environment. |
| `gemini` | Gemini CLI ACP adapter | Requires Gemini CLI auth or API key setup. |
| `iflow` | iFlow CLI | Adapter availability and model control depend on the installed CLI. |
| `kilocode` | Kilo Code CLI | Adapter availability and model control depend on the installed CLI. |
| `kimi` | Kimi/Moonshot CLI | Requires Kimi/Moonshot auth on the host. |
| `kiro` | Kiro CLI | Adapter availability and model control depend on the installed CLI. |
| `opencode` | OpenCode ACP adapter | Requires OpenCode CLI/provider auth. |
| `openclaw` | OpenClaw Gateway bridge through `openclaw acp` | Lets an ACP-aware harness talk back to an OpenClaw Gateway session. |
| `qwen` | Qwen Code / Qwen CLI | Requires Qwen-compatible auth on the host. |

Custom acpx agent aliases can be configured in acpx itself, but OpenClaw policy still checks `acp.allowedAgents` and any `agents.list[].runtime.acp.agent` mapping before dispatch. A noted first-run behavior: the Codex ACP adapter is staged with the `acpx` plugin and launched locally when possible (running with an isolated `CODEX_HOME` into which OpenClaw copies trusted project entries plus safe model/provider routing config, while auth, notifications, and hooks stay on the host config), whereas other target harness adapters may still be fetched on demand with `npx` the first time you use them — and vendor auth must already exist on the host for that harness.

## ACP Versus Sub-Agents

The page draws an explicit three-way contrast for choosing a runtime. Use **ACP** when you want an external harness runtime; use **native Codex app-server** for Codex conversation binding/control when the `codex` plugin is enabled; use **sub-agents** when you want OpenClaw-native delegated runs.

| Area | ACP session | Sub-agent run |
| --- | --- | --- |
| Runtime | ACP backend plugin (for example acpx) | OpenClaw native sub-agent runtime |
| Session key | `agent:<agentId>:acp:<uuid>` | `agent:<agentId>:subagent:<uuid>` |
| Main commands | `/acp ...` | `/subagents ...` |
| Spawn tool | `sessions_spawn` with `runtime:"acp"` | `sessions_spawn` (default runtime) |

The distinguishing detail is the session-key namespace (`...:acp:<uuid>` vs `...:subagent:<uuid>`) and that both share the `sessions_spawn` tool but differ only by the `runtime` value — `runtime` defaults to `subagent`, so an ACP session requires `runtime: "acp"` to be set explicitly.

## How ACP Runs Claude Code

For Claude Code *through* ACP, the source describes a four-layer stack, illustrating the harness-vs-OpenClaw boundary concretely:

1. OpenClaw ACP session control plane.
2. Official `@openclaw/acpx` runtime plugin.
3. Claude ACP adapter.
4. Claude-side runtime/session machinery.

In that stack, "ACP Claude" is a **harness session** with ACP controls, session resume, background-task tracking, and optional conversation/thread binding. This is explicitly *not* the same as a CLI backend: CLI backends are separate text-only local fallback runtimes. The page's practical operator rule frames the choice — if you want `/acp spawn`, bindable sessions, runtime controls, or persistent harness work, use ACP; if you want simple local text fallback through the raw CLI, use CLI backends.

## Bound Sessions: Mental Model

ACP introduces four conceptually distinct surfaces that operators must keep separate when reasoning about a bound session (the spawn/bind procedure that uses this model lives in `oc_tools_acp_agents_spawn_bind`):

- **Chat surface** — where people keep talking (a Discord channel, a Telegram topic, an iMessage chat).
- **ACP session** — the durable Codex/Claude/Gemini runtime state OpenClaw routes to.
- **Child thread/topic** — an optional extra messaging surface, created only by `--thread ...`.
- **Runtime workspace** — the filesystem location (`cwd`, repo checkout, backend workspace) where the harness runs. It is independent of the chat surface.

The central idea is that the chat surface, the durable ACP session, an optional child thread, and the runtime workspace are four independent things: binding a conversation to a session does not by itself create a thread, and the workspace where code actually runs is decoupled from where the conversation happens.

**Source**: OpenClaw documentation — `tools/acp-agents` (mirror `inbox/openclaw_docs/tools/acp-agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
