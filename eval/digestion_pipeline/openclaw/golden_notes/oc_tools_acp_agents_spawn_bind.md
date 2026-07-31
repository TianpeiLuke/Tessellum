---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - acp
keywords:
  - openclaw acp spawn
  - acp bind here thread
  - sessions_spawn runtime acp
  - persistent acp channel bindings
  - acp operator runbook
  - bindings type acp match peer
  - agents list runtime acp
  - resumeSessionId session load
topics:
  - OpenClaw
  - ACP Agents
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/acp-agents
access_control_group: ["general"]
---

# OpenClaw — ACP Agents: Spawn and Bind Operator Procedure

## Overview

This note is the operator procedure for starting and binding ACP (Agent Client Protocol) sessions in OpenClaw — the external-harness path that runs Claude Code, Cursor, Gemini CLI, explicit Codex ACP, OpenCode, and other acpx harnesses. It mirrors the `tools/acp-agents` source page sections covering the `/acp` operator runbook, current-conversation `--bind here` binds, persistent top-level `bindings[]` plus per-agent `agents.list[].runtime` defaults, the `sessions_spawn({ runtime: "acp" })` parameters, and the `--bind`/`--thread` spawn modes. The concept layer (what ACP is, ACP vs sub-agents) lives in `oc_tools_acp_agents_overview` and the delivery/sandbox/controls runtime lives in `oc_tools_acp_agents_runtime`; this note is the spawn-and-bind workflow only.

## Operator runbook (`/acp` flow from chat)

The quick `/acp` flow from chat has six steps:

1. **Spawn** — `/acp spawn claude --bind here`, `/acp spawn gemini --mode persistent --thread auto`, or explicit `/acp spawn codex --bind here`.
2. **Work** — continue in the bound conversation or thread (or target the session key explicitly).
3. **Check state** — `/acp status`.
4. **Tune** — `/acp model <provider/model>`, `/acp permissions <profile>`, `/acp timeout <seconds>`.
5. **Steer** — without replacing context: `/acp steer tighten logging and continue`.
6. **Stop** — `/acp cancel` (current turn) or `/acp close` (session + bindings).

**Lifecycle details.** Spawn creates or resumes an ACP runtime session, records ACP metadata in the OpenClaw session store, and may create a background task when the run is parent-owned. Parent-owned ACP sessions are treated as background work even when the runtime session is persistent, so completion and cross-surface delivery go through the parent task notifier rather than a normal user-facing chat session. Task maintenance closes terminal or orphaned parent-owned one-shot ACP sessions; persistent ACP sessions are preserved while an active conversation binding remains, while stale persistent sessions without an active binding are closed so they cannot be silently resumed after the owning task is done or its task record is gone. Bound follow-up messages go directly to the ACP session until the binding is closed, unfocused, reset, or expired. Gateway commands stay local: `/acp ...`, `/status`, and `/unfocus` are never sent as prompt text to a bound ACP harness. `cancel` aborts the active turn when the backend supports cancellation and does not delete the binding or session metadata, whereas `close` ends the ACP session from OpenClaw's point of view and removes the binding (a harness may still keep its own upstream history if it supports resume). Idle runtime workers are eligible for cleanup after `acp.runtime.ttlMinutes`, but stored session metadata remains available for `/acp sessions`.

**Routing note.** Natural-language requests to "bind this channel to Codex" route to the native Codex plugin when it is enabled (the default chat-control path); use explicit ACP (`/acp ...` or `runtime: "acp"`) only when you want the ACP runtime/session model. For `sessions_spawn`, `runtime: "acp"` is advertised only when ACP is enabled, the requester is not sandboxed, and an ACP runtime backend is loaded; `acp.dispatch.enabled=false` pauses automatic ACP thread dispatch but does not hide or block explicit `sessions_spawn({ runtime: "acp" })` calls.

## Current-conversation binds (`--bind here`)

`/acp spawn <harness> --bind here` pins the current conversation to the spawned ACP session — no child thread, same chat surface — while OpenClaw keeps owning transport, auth, safety, and delivery. Follow-up messages in that conversation route to the same session; `/new` and `/reset` reset the session in place; `/acp close` removes the binding. Example operator commands mixing the native Codex path and the explicit ACP fallback:

```text
/codex bind                                              # native Codex bind, route future messages here
/codex model gpt-5.4                                     # tune the bound native Codex thread
/codex stop                                              # control the active native Codex turn
/acp spawn codex --bind here                             # explicit ACP fallback for Codex
/acp spawn codex --thread auto                           # may create a child thread/topic and bind there
/acp spawn codex --bind here --cwd /workspace/repo       # same chat binding, Codex runs in /workspace/repo
```

**Binding rules and exclusivity.** `--bind here` and `--thread ...` are mutually exclusive and cannot be combined in the same `/acp spawn` call. `--bind here` only works on channels that advertise current-conversation binding; OpenClaw returns a clear unsupported message otherwise, and bindings persist across gateway restarts. On Discord, `spawnSessions` gates child thread creation for `--thread auto|here` — not `--bind here`. If you spawn to a different ACP agent without `--cwd`, OpenClaw inherits the target agent's workspace by default; missing inherited paths (`ENOENT`/`ENOTDIR`) fall back to the backend default, while other access errors (e.g. `EACCES`) surface as spawn errors. Gateway management commands stay local in bound conversations — `/acp ...` commands are handled by OpenClaw even when normal follow-up text routes to the bound ACP session, and `/status`/`/unfocus` also stay local whenever command handling is enabled for that surface.

**Thread-bound sessions.** When thread bindings are enabled for a channel adapter, OpenClaw binds a thread to a target ACP session, follow-up messages in that thread route to the bound ACP session, ACP output is delivered back to the same thread, and unfocus/close/archive/idle-timeout or max-age expiry removes the binding. Required feature flags for thread-bound ACP are `acp.enabled=true`, `acp.dispatch.enabled` on (default; set `false` to pause automatic dispatch while explicit spawns still work), and channel-adapter thread session spawns enabled (default `true`): `channels.discord.threadBindings.spawnSessions=true` and `channels.telegram.threadBindings.spawnSessions=true`. Thread binding support is adapter-specific; current built-in support is Discord threads/channels and Telegram topics (forum topics in groups/supergroups and DM topics), and plugin channels can add support through the same binding interface. If the active adapter does not support thread bindings, OpenClaw returns a clear unsupported/unavailable message.

## Persistent channel bindings

For non-ephemeral workflows, configure persistent ACP bindings as top-level `bindings[]` entries.

### Binding model

Each persistent ACP binding entry uses these fields:

- `bindings[].type` (`"acp"`) — marks a persistent ACP conversation binding.
- `bindings[].match` (object) — identifies the target conversation. Per-channel shapes: **Discord channel/thread** `match.channel="discord"` + `match.peer.id="<channelOrThreadId>"`; **Slack channel/DM** `match.channel="slack"` + `match.peer.id="<channelId|channel:<channelId>|#<channelId>|userId|user:<userId>|slack:<userId>|<@userId>>"` (prefer stable Slack ids; channel bindings also match replies inside that channel's threads); **Telegram forum topic** `match.channel="telegram"` + `match.peer.id="<chatId>:topic:<topicId>"`; **WhatsApp DM/group** `match.channel="whatsapp"` + `match.peer.id="<E.164|group JID>"` (E.164 such as `+15555550123` for direct chats, group JIDs such as `120363424282127706@g.us` for groups); **iMessage DM/group** `match.channel="imessage"` + `match.peer.id="<handle|chat_id:*|chat_guid:*|chat_identifier:*>"` (prefer `chat_id:*` for stable group bindings).
- `bindings[].agentId` (string) — the owning OpenClaw agent id.
- `bindings[].acp.mode` (`"persistent" | "oneshot"`) — optional ACP override.
- `bindings[].acp.label` (string) — optional operator-facing label.
- `bindings[].acp.cwd` (string) — optional runtime working directory.
- `bindings[].acp.backend` (string) — optional backend override.

### Runtime defaults per agent

Use `agents.list[].runtime` to define ACP defaults once per agent: `agents.list[].runtime.type="acp"`, `agents.list[].runtime.acp.agent` (harness id, e.g. `codex` or `claude`), `agents.list[].runtime.acp.backend`, `agents.list[].runtime.acp.mode`, and `agents.list[].runtime.acp.cwd`. Override precedence for ACP bound sessions: (1) `bindings[].acp.*`, (2) `agents.list[].runtime.acp.*`, (3) global ACP defaults (e.g. `acp.backend`).

### Example

A complete config wiring two ACP agents (`codex`, `claude`) with persistent Discord and Telegram bindings plus fallback `route` bindings:

```json5
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
      {
        id: "claude",
        runtime: {
          type: "acp",
          acp: { agent: "claude", backend: "acpx", mode: "persistent" },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "discord",
        accountId: "default",
        peer: { kind: "channel", id: "222222222222222222" },
      },
      acp: { label: "codex-main" },
    },
    {
      type: "acp",
      agentId: "claude",
      match: {
        channel: "telegram",
        accountId: "default",
        peer: { kind: "group", id: "-1001234567890:topic:42" },
      },
      acp: { cwd: "/workspace/repo-b" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "discord", accountId: "default" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "telegram", accountId: "default" },
    },
  ],
  channels: {
    discord: {
      guilds: {
        "111111111111111111": {
          channels: {
            "222222222222222222": { requireMention: false },
          },
        },
      },
    },
    telegram: {
      groups: {
        "-1001234567890": {
          topics: { "42": { requireMention: false } },
        },
      },
    },
  },
}
```

### Behavior

OpenClaw ensures the configured ACP session exists after channel-specific admission and before use, and messages in that channel, topic, or chat route to the configured ACP session. Configured ACP bindings own their session route — channel broadcast fan-out does not replace the configured ACP session for a matched binding. In bound conversations, `/new` and `/reset` reset the same ACP session key in place, and temporary runtime bindings (e.g. from thread-focus flows) still apply where present. For cross-agent ACP spawns without an explicit `cwd`, OpenClaw inherits the target agent workspace from agent config; missing inherited paths fall back to the backend default cwd, while non-missing access failures surface as spawn errors.

## Start ACP sessions: `sessions_spawn` parameters

Two ways to start an ACP session: the `sessions_spawn` tool (from an agent turn or tool call, requiring `runtime: "acp"` explicitly because `runtime` defaults to `subagent`) and the `/acp spawn` command (explicit operator control from chat). A minimal `sessions_spawn` call:

```json
{
  "task": "Open the repo and summarize failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
```

The full `sessions_spawn` parameter surface:

- `task` (string, required) — initial prompt sent to the ACP session.
- `runtime` (`"acp"`, required) — must be `"acp"` for ACP sessions.
- `agentId` (string) — ACP target harness id; falls back to `acp.defaultAgent` if set.
- `thread` (boolean, default `false`) — request thread binding flow where supported.
- `mode` (`"run" | "session"`, default `"run"`) — `"run"` is one-shot; `"session"` is persistent. If `thread: true` and `mode` is omitted, OpenClaw may default to persistent behaviour per runtime path. `mode: "session"` requires `thread: true`.
- `cwd` (string) — requested runtime working directory (validated by backend/runtime policy). If omitted, ACP spawn inherits the target agent workspace when configured; missing inherited paths fall back to backend defaults, while real access errors are returned.
- `label` (string) — operator-facing label used in session/banner text.
- `resumeSessionId` (string) — resume an existing ACP session instead of creating a new one. The agent replays its conversation history via `session/load`. Requires `runtime: "acp"`.
- `streamTo` (`"parent"`) — streams initial ACP run progress summaries back to the requester session as system events; accepted responses include `streamLogPath` pointing to a session-scoped JSONL log (`<sessionId>.acp-stream.jsonl`) you can tail for full relay history.
- `model` (string) — explicit model override for the ACP child session. Codex ACP spawns normalize OpenAI refs such as `openai/gpt-5.4` to Codex ACP startup config before `session/new`; slash forms such as `openai/gpt-5.4/high` also set Codex ACP reasoning effort. When omitted, it uses existing subagent model defaults (`agents.defaults.subagents.model` or `agents.list[].subagents.model`) when configured; otherwise the ACP harness uses its own default. Other harnesses must advertise ACP `models` and support `session/set_model` or OpenClaw/acpx fails clearly instead of silently falling back to the target agent default.
- `thinking` (string) — explicit thinking/reasoning effort. For Codex ACP, `minimal` maps to low effort, `low`/`medium`/`high`/`xhigh` map directly, and `off` omits the reasoning-effort startup override. When omitted, ACP spawns use existing subagent thinking defaults and per-model `agents.defaults.models["provider/model"].params.thinking`.

ACP `sessions_spawn` runs use `agents.defaults.subagents.runTimeoutSeconds` for their default child turn limit; the tool does not accept per-call timeout overrides. The `/acp spawn` command form takes key flags `--mode persistent|oneshot`, `--bind here|off`, `--thread auto|here|off`, `--cwd <absolute-path>`, and `--label <name>`.

## Spawn bind and thread modes

The `--bind here|off` modes: `here` binds the current active conversation in place and fails if none is active; `off` does not create a current-conversation binding. `--bind here` is the simplest operator path for "make this channel Codex-backed", does not create a child thread, is only available on channels that expose current-conversation binding support, and cannot be combined with `--thread` in one `/acp spawn` call.

The `--thread auto|here|off` modes: `auto` binds the active thread when in one, otherwise creates/binds a child thread when supported; `here` requires a current active thread and fails if not in one; `off` starts the session unbound. On non-thread binding surfaces, default behavior is effectively `off`. Thread-bound spawn requires channel policy support — `channels.discord.threadBindings.spawnSessions=true` and `channels.telegram.threadBindings.spawnSessions=true` — and use `--bind here` to pin the current conversation without creating a child thread.

**Source**: OpenClaw documentation — `tools/acp-agents` (mirror `inbox/openclaw_docs/tools/acp-agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
