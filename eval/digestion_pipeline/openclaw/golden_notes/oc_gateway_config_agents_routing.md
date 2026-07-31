---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - multi_agent_routing
keywords:
  - openclaw agents.list per-agent overrides
  - multi-agent routing bindings
  - binding match fields deterministic order
  - per-agent access profiles
  - agentId match channel accountId peer
  - sessions_spawn allowAgents subagents
  - per-agent sandbox tools profile
topics:
  - OpenClaw
  - Agent Routing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-agents
access_control_group: ["general"]
---

# OpenClaw — Per-Agent Overrides and Multi-Agent Routing Config

## Overview

This note is the procedure reference for configuring **per-agent overrides** (`agents.list[]`) and **multi-agent routing** (`bindings`) on the OpenClaw gateway. It mirrors the `agents.list (per-agent overrides)`, `Multi-agent routing`, `Binding match fields`, and `Per-agent access profiles` sections of the `gateway/config-agents` source page. These keys let one gateway run multiple isolated agents and route each inbound message to the correct agent, with per-agent model, skills, identity, sandbox, and tool-access overrides. Companion notes in this config-agents split cover agent defaults (bootstrap/context, model/media, backends/overlays, runtime resilience) and the Session/Messages/Talk blocks; this note owns only the per-agent and routing surface.

## `agents.list` (per-agent overrides)

`agents.list` is an array of per-agent config entries, each keyed by a stable `id`. Any field set on an entry overrides the matching `agents.defaults` value for that agent. The example below is the source's canonical full entry shape, showing the `tts`, `identity`, `groupChat`, `sandbox`, `runtime`, `subagents`, and `tools` sub-blocks.

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Main Agent",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
        model: "anthropic/claude-opus-4-6", // or { primary, fallbacks }
        thinkingDefault: "high", // per-agent thinking level override
        reasoningDefault: "on", // per-agent reasoning visibility override
        fastModeDefault: false, // per-agent fast mode override
        params: { cacheRetention: "none" }, // overrides matching defaults.models params by key
        tts: {
          providers: {
            elevenlabs: { speakerVoiceId: "EXAVITQu4vr4xnSDxMaL" },
          },
        },
        skills: ["docs-search"], // replaces agents.defaults.skills when set
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
        groupChat: { mentionPatterns: ["@openclaw"] },
        sandbox: { mode: "off" },
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
        subagents: { allowAgents: ["*"] },
        tools: {
          profile: "coding",
          allow: ["browser"],
          deny: ["canvas"],
          elevated: { enabled: true },
        },
      },
    ],
  },
}
```

### Per-agent field semantics

The source defines each override field as follows (copied faithfully from the page):

- `id`: stable agent id (required).
- `default`: when multiple are set, first wins (warning logged). If none set, first list entry is default.
- `model`: string form sets a strict per-agent primary with no model fallback; object form `{ primary }` is also strict unless you add `fallbacks`. Use `{ primary, fallbacks: [...] }` to opt that agent into fallback, or `{ primary, fallbacks: [] }` to make strict behavior explicit. Cron jobs that only override `primary` still inherit default fallbacks unless you set `fallbacks: []`.
- `params`: per-agent stream params merged over the selected model entry in `agents.defaults.models`. Use this for agent-specific overrides like `cacheRetention`, `temperature`, or `maxTokens` without duplicating the whole model catalog.
- `tts`: optional per-agent text-to-speech overrides. The block deep-merges over `messages.tts`, so keep shared provider credentials and fallback policy in `messages.tts` and set only persona-specific values such as provider, voice, model, style, or auto mode here.
- `skills`: optional per-agent skill allowlist. If omitted, the agent inherits `agents.defaults.skills` when set; an explicit list replaces defaults instead of merging, and `[]` means no skills.
- `thinkingDefault`: optional per-agent default thinking level (`off | minimal | low | medium | high | xhigh | adaptive | max`). Overrides `agents.defaults.thinkingDefault` for this agent when no per-message or session override is set. The selected provider/model profile controls which values are valid; for Google Gemini, `adaptive` keeps provider-owned dynamic thinking (`thinkingLevel` omitted on Gemini 3/3.1, `thinkingBudget: -1` on Gemini 2.5).
- `reasoningDefault`: optional per-agent default reasoning visibility (`on | off | stream`). Overrides `agents.defaults.reasoningDefault` for this agent when no per-message or session reasoning override is set.
- `fastModeDefault`: optional per-agent default for fast mode (`true | false`). Applies when no per-message or session fast-mode override is set.
- `models`: optional per-agent model catalog/runtime overrides keyed by full `provider/model` ids. Use `models["provider/model"].agentRuntime` for per-agent runtime exceptions.
- `runtime`: optional per-agent runtime descriptor. Use `type: "acp"` with `runtime.acp` defaults (`agent`, `backend`, `mode`, `cwd`) when the agent should default to ACP harness sessions.
- `identity.avatar`: workspace-relative path, `http(s)` URL, or `data:` URI.
- `identity` derives defaults: `ackReaction` from `emoji`, `mentionPatterns` from `name`/`emoji`.

### Subagent spawn controls

The `subagents` sub-block governs which other configured agents this agent may spawn:

- `subagents.allowAgents`: allowlist of configured agent ids for explicit `sessions_spawn.agentId` targets (`["*"]` = any configured target; default: same agent only). Include the requester id when self-targeted `agentId` calls should be allowed. Stale entries whose agent config was deleted are rejected by `sessions_spawn` and omitted from `agents_list`; run `openclaw doctor --fix` to clean them up, or add a minimal `agents.list[]` entry if that target should remain spawnable while inheriting defaults.
- Sandbox inheritance guard: if the requester session is sandboxed, `sessions_spawn` rejects targets that would run unsandboxed.
- `subagents.requireAgentId`: when true, block `sessions_spawn` calls that omit `agentId` (forces explicit profile selection; default: false).

## Multi-agent routing

Multi-agent routing runs multiple isolated agents inside one Gateway. Each agent gets its own `agents.list[]` entry, and a top-level `bindings` array maps inbound traffic (by channel and account) onto a specific `agentId`.

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### Binding match fields

Each `bindings` entry has an `agentId` and a `match` object. The supported fields (verbatim from source):

- `type` (optional): `route` for normal routing (missing type defaults to route), `acp` for persistent ACP conversation bindings.
- `match.channel` (required)
- `match.accountId` (optional; `*` = any account; omitted = default account)
- `match.peer` (optional; `{ kind: direct|group|channel, id }`)
- `match.guildId` / `match.teamId` (optional; channel-specific)
- `acp` (optional; only for `type: "acp"`): `{ mode, label, cwd, backend }`

**Deterministic match order** — bindings are evaluated most-specific-first:

1. `match.peer`
2. `match.guildId`
3. `match.teamId`
4. `match.accountId` (exact, no peer/guild/team)
5. `match.accountId: "*"` (channel-wide)
6. Default agent

Within each tier, the first matching `bindings` entry wins. For `type: "acp"` entries, OpenClaw resolves by exact conversation identity (`match.channel` + account + `match.peer.id`) and does not use the route binding tier order above.

### Per-agent access profiles

Per-agent access profiles combine `sandbox` and `tools` settings on an `agents.list[]` entry to scope what an agent can do. The source documents three reference profiles.

**Full access (no sandbox):** an agent with `sandbox: { mode: "off" }` and no tool restrictions.

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

**Read-only tools + workspace:** an agent sandboxed with `workspaceAccess: "ro"` that allows only read/session tools and denies all mutating and exec tools.

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

**No filesystem access (messaging only):** an agent sandboxed with `workspaceAccess: "none"` that allows only session and messaging-channel tools (`whatsapp`, `telegram`, `slack`, `discord`, `gateway`) and denies filesystem, exec, and other tools. See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for precedence details. The full `deny` list and remaining tool keys are reproduced verbatim from the source page.

**Source**: OpenClaw documentation — `gateway/config-agents` (mirror `inbox/openclaw_docs/gateway/config-agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
