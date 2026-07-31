---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - sandbox
keywords:
  - openclaw sandbox vs tool policy vs elevated
  - three containment controls
  - sandbox where tools run
  - tool policy deny always wins
  - elevated exec run on host
  - openclaw sandbox explain
  - tool groups group:runtime group:fs
  - sandbox jail fixes
topics:
  - OpenClaw
  - Gateway Security
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated
access_control_group: ["general"]
---

# OpenClaw — Sandbox vs Tool Policy vs Elevated (Three Orthogonal Containment Controls)

## Overview

This note explains the conceptual model behind why an OpenClaw tool is blocked or runs where it does: three **related but different** controls compose to govern tool execution — **sandbox** (where tools run), **tool policy** (which tools exist / are callable), and **elevated** (an exec-only escape hatch to run on host). It mirrors the `gateway/sandbox-vs-tool-policy-vs-elevated` source page: the quick-debug inspector, each control's config-key surface and decision rules, and the common "sandbox jail" fixes. The full sandbox matrix (modes, scopes, backends, images) is deferred to the Sandboxing pages; this note frames the mental model and the exact config key to change.

## The Three Controls

OpenClaw has three related (but different) controls, each keyed by its own config namespace:

1. **Sandbox** (`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`) decides **where tools run** (sandbox backend vs host).
2. **Tool policy** (`tools.*`, `tools.sandbox.tools.*`, `agents.list[].tools.*`) decides **which tools are available/allowed**.
3. **Elevated** (`tools.elevated.*`, `agents.list[].tools.elevated.*`) is an **exec-only escape hatch** to run outside the sandbox when you're sandboxed (`gateway` by default, or `node` when the exec target is configured to `node`).

These are orthogonal: sandbox does not decide which tools exist, tool policy does not decide where they run, and elevated only relaxes *where* `exec` runs (never *which* tools are allowed). A blocked tool is therefore diagnosed by asking which of the three layers stopped it.

## Quick Debug

Use the inspector to see what OpenClaw is *actually* doing:

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

It prints: the effective sandbox mode/scope/workspace access; whether the session is currently sandboxed (main vs non-main); the effective sandbox tool allow/deny (and whether it came from agent/global/default); and the elevated gates plus fix-it key paths. This single command resolves the composed state of all three controls for a given session or agent, which is why it is the recommended starting point for any "why is this blocked" investigation.

## Sandbox: Where Tools Run

Sandboxing is controlled by `agents.defaults.sandbox.mode`, which selects which sessions are sandboxed:

- `"off"`: everything runs on the host.
- `"non-main"`: only non-main sessions are sandboxed (a common "surprise" for groups/channels).
- `"all"`: everything is sandboxed.

The full matrix — scope, workspace mounts, images — lives in the Sandboxing reference (`/gateway/sandboxing`); this note only surfaces the mode axis and the bind-mount security quick-check below.

### Bind Mounts (Security Quick Check)

Bind mounts pierce the sandbox filesystem, so they are the most common way an otherwise-isolated sandbox gains host access:

- `docker.binds` *pierces* the sandbox filesystem: whatever you mount is visible inside the container with the mode you set (`:ro` or `:rw`).
- Default is read-write if you omit the mode; prefer `:ro` for source/secrets.
- `scope: "shared"` ignores per-agent binds (only global binds apply).
- OpenClaw validates bind sources twice: first on the normalized source path, then again after resolving through the deepest existing ancestor. Symlink-parent escapes do not bypass blocked-path or allowed-root checks.
- Non-existent leaf paths are still checked safely. If `/workspace/alias-out/new-file` resolves through a symlinked parent to a blocked path or outside the configured allowed roots, the bind is rejected.
- Binding `/var/run/docker.sock` effectively hands host control to the sandbox; only do this intentionally.
- Workspace access (`workspaceAccess: "ro"`/`"rw"`) is independent of bind modes.

## Tool Policy: Which Tools Exist / Are Callable

Tool policy decides *which* tools are available, and it composes from several layers (base allowlists plus allow/deny overrides):

- **Tool profile**: `tools.profile` and `agents.list[].tools.profile` (base allowlist)
- **Provider tool profile**: `tools.byProvider[provider].profile` and `agents.list[].tools.byProvider[provider].profile`
- **Global/per-agent tool policy**: `tools.allow`/`tools.deny` and `agents.list[].tools.allow`/`agents.list[].tools.deny`
- **Provider tool policy**: `tools.byProvider[provider].allow/deny` and `agents.list[].tools.byProvider[provider].allow/deny`
- **Sandbox tool policy** (only applies when sandboxed): `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` and `agents.list[].tools.sandbox.tools.*`

Rules of thumb that govern how these layers resolve:

- `deny` always wins.
- If `allow` is non-empty, everything else is treated as blocked.
- Tool policy is the hard stop: `/exec` cannot override a denied `exec` tool.
- Tool policy filters tool availability by name; it does not inspect side effects inside `exec`. If `exec` is allowed, denying `write`, `edit`, or `apply_patch` does not make shell commands read-only.
- `/exec` only changes session defaults for authorized senders; it does not grant tool access.
- Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.4`).
- Gateway logs include `agents/tool-policy` audit entries when a tool policy step removes tools or a sandbox tool policy blocks a call. Use `openclaw logs` to see the rule label, config key, and affected tool names.

### Tool Groups (Shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools:

```json5
{
  tools: {
    sandbox: {
      tools: {
        allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],
      },
    },
  },
}
```

Available groups:

- `group:runtime`: `exec`, `process`, `code_execution` (`bash` is accepted as an alias for `exec`)
- `group:fs`: `read`, `write`, `edit`, `apply_patch` — for read-only agents, deny `group:runtime` as well as mutating filesystem tools unless sandbox filesystem policy or a separate host boundary enforces the read-only constraint.
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `sessions_yield`, `subagents`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:web`: `web_search`, `x_search`, `web_fetch`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `heartbeat_respond`, `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- `group:agents`: `agents_list`, `update_plan`
- `group:media`: `image`, `image_generate`, `music_generate`, `video_generate`, `tts`
- `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)
- `group:plugins`: all loaded plugin-owned tools, including configured MCP servers exposed through `bundle-mcp`

For sandboxed MCP servers, the sandbox tool policy is a **second** allow gate. If `mcp.servers` is configured but sandboxed turns only show built-in tools, add `bundle-mcp`, `group:plugins`, or a server-prefixed MCP tool name/glob such as `outlook__send_mail` or `outlook__*` to `tools.sandbox.tools.alsoAllow`, then restart/reload the gateway and recapture the tool list. Server globs use the provider-safe MCP server prefix: non-`[A-Za-z0-9_-]` characters become `-`, names that do not start with a letter get an `mcp-` prefix, and long or duplicate prefixes may be truncated or suffixed. `openclaw doctor` currently checks this shape for OpenClaw-managed servers in `mcp.servers`; MCP servers loaded from bundled plugin manifests or Claude `.mcp.json` use the same sandbox gate, but this diagnostic does not enumerate those sources yet — use the same allowlist entries if their tools disappear in sandboxed turns.

## Elevated: Exec-Only "Run on Host"

Elevated does **not** grant extra tools; it only affects `exec`:

- If you're sandboxed, `/elevated on` (or `exec` with `elevated: true`) runs outside the sandbox (approvals may still apply).
- Use `/elevated full` to skip exec approvals for the session.
- If you're already running direct, elevated is effectively a no-op (still gated).
- Elevated is **not** skill-scoped and does **not** override tool allow/deny.
- Elevated does not grant arbitrary cross-host overrides from `host=auto`; it follows the normal exec target rules and only preserves `node` when the configured/session target is already `node`.
- `/exec` is separate from elevated. It only adjusts per-session exec defaults for authorized senders.

The elevated gates (the keys that enable and scope it):

- Enablement: `tools.elevated.enabled` (and optionally `agents.list[].tools.elevated.enabled`)
- Sender allowlists: `tools.elevated.allowFrom.<provider>` (and optionally `agents.list[].tools.elevated.allowFrom.<provider>`)

## Common "Sandbox Jail" Fixes

### "Tool X blocked by sandbox tool policy"

Fix-it keys (pick one):

- Disable sandbox: `agents.defaults.sandbox.mode=off` (or per-agent `agents.list[].sandbox.mode=off`)
- Allow the tool inside sandbox: remove it from `tools.sandbox.tools.deny` (or per-agent `agents.list[].tools.sandbox.tools.deny`), or add it to `tools.sandbox.tools.allow` (or per-agent allow).
- Check `openclaw logs` for the `agents/tool-policy` entry. It records the sandbox mode and whether the allow or deny rule blocked the tool.

### "I thought this was main, why is it sandboxed?"

In `"non-main"` mode, group/channel keys are *not* main. Use the main session key (shown by `sandbox explain`) or switch mode to `"off"`.

**Source**: OpenClaw documentation — `gateway/sandbox-vs-tool-policy-vs-elevated` (mirror `inbox/openclaw_docs/gateway/sandbox-vs-tool-policy-vs-elevated.md`)
**Last Updated**: 2026-06-22
**Status**: Active
