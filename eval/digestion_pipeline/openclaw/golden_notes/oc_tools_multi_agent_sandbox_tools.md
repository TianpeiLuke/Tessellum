---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - sandbox
keywords:
  - openclaw multi-agent sandbox
  - per-agent tool policy
  - agents.list tool allow deny
  - tool filtering precedence order
  - agentdir auth scoping
  - sandbox mode non-main pitfall
  - empty allowlist fail loud
  - openclaw agents list bindings
topics:
  - OpenClaw
  - Multi-Agent Sandbox and Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/multi-agent-sandbox-tools
access_control_group: ["general"]
---

# OpenClaw — Per-Agent Sandbox and Tool-Policy Overrides in a Multi-Agent Gateway

## Overview

This note is the procedure for configuring **per-agent sandbox and tool-policy overrides** in an OpenClaw multi-agent gateway, mirroring the `tools/multi-agent-sandbox-tools` source page. Each agent in a multi-agent setup can override the global sandbox and tool policy; this page covers the worked `agents.list[]` configuration examples, the sandbox-config and 8-step tool-filtering precedence chains (each level can only further restrict, never grant back denied tools), per-agent `agentDir` auth scoping, migration from a single-agent config, tool-restriction examples, the `non-main` sandbox-mode pitfall, and the testing/troubleshooting commands. It does not redefine sandbox backends/modes (those live in `gateway/sandboxing`) or the routing model (`concepts/multi-agent`) — it specializes them per agent.

## Agent auth scoping (`agentDir`)

Auth is scoped by agent: each agent has its own `agentDir` auth store at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`. Per the source warning, **never reuse `agentDir` across agents**. Agents can read through to the default/main agent's auth profiles when they do not have a local profile, but **OAuth refresh tokens are not cloned into secondary agent stores**. If you copy credentials manually, copy only portable static `api_key` or `token` profiles.

## Configuration examples

The page gives four worked `agents.list[]` configurations. Each agent object lives under `agents.list[]` with an `id`, optional `default: true`, a `workspace`, a `sandbox` block, and an optional `tools` block; `bindings[]` route a provider/peer to a specific `agentId`.

Example 1 (Personal + restricted family agent) defines a `main` agent (`default: true`, `sandbox.mode: "off"`) and a `family` agent sandboxed with `mode: "all"` / `scope: "agent"`, restricted to `tools.allow: ["read", "message"]` and denying `exec`/`write`/`edit`/`apply_patch`/`process`/`browser`, with `message.crossContext.allowWithinProvider: false` and `allowAcrossProviders: false`; a `bindings[]` entry routes a WhatsApp group peer to `family`. Its stated result: `main` runs on host with full tool access; `family` runs in Docker (one container per agent) with only `read` and current-conversation message sends.

```json
{
  "id": "family",
  "name": "Family Bot",
  "workspace": "~/.openclaw/workspace-family",
  "sandbox": { "mode": "all", "scope": "agent" },
  "tools": {
    "allow": ["read", "message"],
    "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"],
    "message": {
      "crossContext": {
        "allowWithinProvider": false,
        "allowAcrossProviders": false
      }
    }
  }
}
```

Example 2 (Work agent with shared sandbox) gives a `work` agent `sandbox.mode: "all"`, `scope: "shared"`, `workspaceRoot: "/tmp/work-sandboxes"`, allowing `read`/`write`/`apply_patch`/`exec` and denying `browser`/`gateway`/`discord`. Example 2b (Global coding profile + messaging-only agent) sets a global `tools.profile: "coding"` while a `support` agent uses `tools.profile: "messaging"` plus `allow: ["slack"]` — result: default agents get coding tools, `support` is messaging-only with the Slack tool. Example 3 (Different sandbox modes per agent) sets `agents.defaults.sandbox` to `mode: "non-main"` / `scope: "session"`, with a `main` agent overriding to `mode: "off"` and a `public` agent overriding to `mode: "all"` / `scope: "agent"` and `allow: ["read"]`.

## Configuration precedence

When both global (`agents.defaults.*`) and agent-specific (`agents.list[].*`) configs exist, the page defines two precedence chains.

### Sandbox config

Agent-specific settings override global, key-by-key:

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

Per the source Note: `agents.list[].sandbox.{docker,browser,prune}.*` overrides `agents.defaults.sandbox.{docker,browser,prune}.*` for that agent, but is **ignored when the sandbox scope resolves to `"shared"`**.

### Tool restrictions (8-step filtering order)

The tool-filtering order is, in sequence:

1. **Tool profile** — `tools.profile` or `agents.list[].tools.profile`.
2. **Provider tool profile** — `tools.byProvider[provider].profile` or `agents.list[].tools.byProvider[provider].profile`.
3. **Global tool policy** — `tools.allow` / `tools.deny`.
4. **Provider tool policy** — `tools.byProvider[provider].allow/deny`.
5. **Agent-specific tool policy** — `agents.list[].tools.allow/deny`.
6. **Agent provider policy** — `agents.list[].tools.byProvider[provider].allow/deny`.
7. **Sandbox tool policy** — `tools.sandbox.tools` or `agents.list[].tools.sandbox.tools`.
8. **Subagent tool policy** — `tools.subagents.tools`, if applicable.

Precedence rules (from the page): each level can further **restrict** tools but **cannot grant back** denied tools from earlier levels; if `agents.list[].tools.sandbox.tools` is set, it **replaces** `tools.sandbox.tools` for that agent; if `agents.list[].tools.profile` is set, it overrides `tools.profile` for that agent; provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.4`).

**Empty allowlist behavior:** if any explicit allowlist in that chain leaves the run with no callable tools, OpenClaw **stops before submitting the prompt to the model**. This is intentional — an agent configured with a missing tool such as `agents.list[].tools.allow: ["query_db"]` should fail loudly until the plugin that registers `query_db` is enabled, not continue as a text-only agent.

Tool policies support `group:*` shorthands that expand to multiple tools (see the Tool groups list on the sandbox-vs-tool-policy-vs-elevated page). Per-agent elevated overrides (`agents.list[].tools.elevated`) can further restrict elevated exec for specific agents.

## Migration from single agent

To migrate a legacy single-agent config to multi-agent: the "Before" shape uses `agents.defaults` with a `workspace` + `sandbox.mode: "non-main"` and a top-level `tools.sandbox.tools` allow/deny block; the "After" shape moves the agent into `agents.list[]` as a single `main` agent (`default: true`, `sandbox: { "mode": "off" }`). Per the source Note: legacy `agent.*` configs are migrated by `openclaw doctor`; prefer `agents.defaults` + `agents.list` going forward.

## Tool restriction examples

The page gives three representative `tools` blocks. A **Read-only agent** sets `allow: ["read"]`, `deny: ["exec", "write", "edit", "apply_patch", "process"]`. A **Shell execution with filesystem tools disabled** agent sets `allow: ["read", "exec", "process"]`, `deny: ["write", "edit", "apply_patch", "browser", "gateway"]` — but its Warning notes this disables OpenClaw filesystem tools while `exec` is still a shell that can write files wherever the host or sandbox filesystem allows; for a truly read-only agent, deny `exec` and `process`, or combine shell access with sandbox filesystem controls such as `agents.defaults.sandbox.workspaceAccess: "ro"` or `"none"`. A **Communication-only** agent sets `sessions.visibility: "tree"`, `allow: ["sessions_list", "sessions_send", "sessions_history", "session_status"]`, `deny: ["exec", "write", "edit", "apply_patch", "read", "browser"]`.

```json
{
  "tools": {
    "sessions": { "visibility": "tree" },
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

In this communication-only profile, `sessions_history` still returns a **bounded, sanitized recall view** rather than a raw transcript dump: assistant recall strips thinking tags, `<relevant-memories>` scaffolding, plain-text tool-call XML payloads (including `<tool_call>...</tool_call>`, `<function_call>...</function_call>`, `<tool_calls>...</tool_calls>`, `<function_calls>...</function_calls>`, and truncated tool-call blocks), downgraded tool-call scaffolding, leaked ASCII/full-width model control tokens, and malformed MiniMax tool-call XML before redaction/truncation.

## Common pitfall: `non-main`

`agents.defaults.sandbox.mode: "non-main"` is based on `session.mainKey` (default `"main"`), **not the agent id**. Group/channel sessions always get their own keys, so they are treated as non-main and **will be sandboxed**. If you want an agent to never sandbox, set `agents.list[].sandbox.mode: "off"`.

## Testing

After configuring multi-agent sandbox and tools, verify with these steps:

1. **Check agent resolution** — `openclaw agents list --bindings`.
2. **Verify sandbox containers** — `docker ps --filter "name=openclaw-sbx-"`.
3. **Test tool restrictions** — send a message requiring restricted tools and verify the agent cannot use denied tools.
4. **Monitor logs** — `tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"`.

## Troubleshooting

- **Agent not sandboxed despite `mode: "all"`** — check for a global `agents.defaults.sandbox.mode` that overrides it; agent-specific config takes precedence, so set `agents.list[].sandbox.mode: "all"`.
- **Tools still available despite deny list** — check the tool-filtering order (global → agent → sandbox → subagent); each level can only further restrict, not grant back; verify with the log line `[tools] filtering tools for agent:${agentId}`.
- **Container not isolated per agent** — set `scope: "agent"` in the agent-specific sandbox config; the default is `"session"`, which creates one container per session.

**Source**: OpenClaw documentation — `tools/multi-agent-sandbox-tools` (mirror `inbox/openclaw_docs/tools/multi-agent-sandbox-tools.md`)
**Last Updated**: 2026-06-22
**Status**: Active
