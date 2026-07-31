---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - sandboxing
keywords:
  - openclaw tool sandbox hardening
  - hardened baseline 60 seconds
  - agents.defaults.sandbox
  - per-agent access profiles
  - browser ssrf policy
  - sub-agent delegation guardrail
  - node system.run remote execution
  - plugins trust install policy
  - read-only mode workspaceAccess
topics:
  - OpenClaw
  - Gateway Security
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/security
access_control_group: ["general"]
---

# OpenClaw — Gateway Tool, Exec, and Sandbox Hardening

## Overview

This note is the **tool/exec/sandbox blast-radius hardening procedure** for the OpenClaw Gateway — the "scope next / model last" enforcement layer of the threat model. It mirrors the hardening recipes in the `gateway/security` source page: the 60-second hardened baseline and copy/paste secure baseline, tool sandboxing (`agents.defaults.sandbox`) plus the sub-agent delegation guardrail, browser control risks and the strict browser SSRF policy, per-agent access profiles (full / read-only / no-access), read-only mode, plugin trust + install policy, dynamic-skills trust, and node `system.run` remote execution. Each control narrows what a manipulated agent or untrusted sender can reach; the network/transport controls live in the sibling network-hardening note, and on-disk data controls live in the data-protection note.

## Hardened baseline in 60 seconds

Apply this baseline first, then selectively re-enable tools per trusted agent. It keeps the Gateway local-only, isolates DMs, and disables control-plane/runtime tools by default:

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    fs: { workspaceOnly: true },
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  },
}
```

## Secure baseline (copy/paste)

A simpler "safe default" config that keeps the Gateway private, requires DM pairing, and avoids always-on group bots:

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    port: 18789,
    auth: { mode: "token", token: "your-long-random-token" },
  },
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

For "safer by default" tool execution, add a sandbox plus deny dangerous tools for any non-owner agent (see "Per-agent access profiles"). There is a built-in baseline for chat-driven agent turns: non-owner senders cannot use the `cron` or `gateway` tools.

## Sandboxing (recommended)

The dedicated deep doc is [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing). There are two complementary approaches: **run the full Gateway in Docker** (container boundary), and the **tool sandbox** (`agents.defaults.sandbox`, host gateway + sandbox-isolated tools, with Docker as the default backend). To prevent cross-agent access, keep `agents.defaults.sandbox.scope` at `"agent"` (default) or `"session"` for stricter per-session isolation; `scope: "shared"` uses a single container or workspace.

Agent workspace access inside the sandbox is controlled by `agents.defaults.sandbox.workspaceAccess`: `"none"` (default) keeps the agent workspace off-limits and tools run against a sandbox workspace under `~/.openclaw/sandboxes`; `"ro"` mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`); `"rw"` mounts it read/write at `/workspace`. Extra `sandbox.docker.binds` are validated against normalized and canonicalized source paths — parent-symlink tricks and canonical home aliases still fail closed if they resolve into blocked roots such as `/etc`, `/var/run`, or credential directories under the OS home.

`tools.elevated` is the global baseline escape hatch that runs exec **outside** the sandbox. The effective host is `gateway` by default, or `node` when the exec target is configured to `node`. Keep `tools.elevated.allowFrom` tight and do not enable it for strangers; you can further restrict elevated per agent via `agents.list[].tools.elevated`. See [Elevated mode](https://docs.openclaw.ai/tools/elevated).

### Sub-agent delegation guardrail

If you allow session tools, treat delegated sub-agent runs as another boundary decision. Deny `sessions_spawn` unless the agent truly needs delegation. Keep `agents.defaults.subagents.allowAgents` and any per-agent `agents.list[].subagents.allowAgents` overrides restricted to known-safe target agents. For any workflow that must remain sandboxed, call `sessions_spawn` with `sandbox: "require"` (the default is `inherit`); `sandbox: "require"` fails fast when the target child runtime is not sandboxed.

## Browser control risks

Enabling browser control gives the model the ability to drive a real browser. If that browser profile already contains logged-in sessions, the model can access those accounts and data — treat browser profiles as **sensitive state**:

- Prefer a dedicated profile for the agent (the default `openclaw` profile).
- Avoid pointing the agent at your personal daily-driver profile.
- Keep host browser control disabled for sandboxed agents unless you trust them.
- The standalone loopback browser control API only honors shared-secret auth (gateway token bearer auth or gateway password). It does not consume trusted-proxy or Tailscale Serve identity headers.
- Treat browser downloads as untrusted input; prefer an isolated downloads directory.
- Disable browser sync/password managers in the agent profile if possible (reduces blast radius).
- For remote gateways, assume "browser control" is equivalent to "operator access" to whatever that profile can reach.
- Keep the Gateway and node hosts tailnet-only; avoid exposing browser control ports to LAN or public Internet.
- Disable browser proxy routing when you don't need it (`gateway.nodes.browser.mode="off"`).
- Chrome MCP existing-session mode is **not** "safer"; it can act as you in whatever that host Chrome profile can reach.

### Browser SSRF policy (strict by default)

OpenClaw's browser navigation policy is strict by default: private/internal destinations stay blocked unless you explicitly opt in. The default `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` is unset, so navigation keeps private/internal/special-use destinations blocked; the legacy alias `browser.ssrfPolicy.allowPrivateNetwork` is still accepted for compatibility. Set `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork: true` to allow private/internal/special-use destinations. In strict mode, use `hostnameAllowlist` (patterns like `*.example.com`) and `allowedHostnames` (exact host exceptions, including blocked names like `localhost`) for explicit exceptions. Navigation is checked before request and best-effort re-checked on the final `http(s)` URL after navigation to reduce redirect-based pivots.

```json5
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false,
      hostnameAllowlist: ["*.example.com", "example.com"],
      allowedHostnames: ["localhost"],
    },
  },
}
```

## Browser control via node host (recommended)

If your Gateway is remote but the browser runs on another machine, run a **node host** on the browser machine and let the Gateway proxy browser actions (see [Browser tool](https://docs.openclaw.ai/tools/browser)). Treat node pairing like admin access. Recommended pattern: keep the Gateway and node host on the same tailnet (Tailscale), and pair the node intentionally — disable browser proxy routing if you don't need it. Avoid exposing relay/control ports over LAN or public Internet, and avoid Tailscale Funnel for browser control endpoints (public exposure).

## Per-agent access profiles (multi-agent)

With multi-agent routing, each agent can have its own sandbox + tool policy: use this to give **full access**, **read-only**, or **no access** per agent. See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for full details and precedence rules. Common use cases: a personal agent gets full access with no sandbox; a family/work agent is sandboxed + read-only tools; a public agent is sandboxed + no filesystem/shell tools.

**Full access (no sandbox):** set `agents.list[]` with `id: "personal"`, a dedicated `workspace`, and `sandbox: { mode: "off" }`.

**Read-only tools + read-only workspace:** for `id: "family"`, set `sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" }`, then `tools: { allow: ["read"], deny: ["write", "edit", "apply_patch", "exec", "process", "browser"] }`.

**No filesystem/shell access (provider messaging allowed):** for `id: "public"`, set `sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" }`. Session tools can reveal sensitive transcript data; by default OpenClaw limits these tools to the current session + spawned sub-agent sessions, but you can clamp further with `tools.sessions.visibility` (`self | tree | agent | all`). A representative `public` agent allows `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`, and the messaging tools (`whatsapp`, `telegram`, `slack`, `discord`), while denying `read`, `write`, `edit`, `apply_patch`, `exec`, `process`, `browser`, `canvas`, `nodes`, `cron`, `gateway`, and `image`.

## Read-only mode (via sandbox and tools)

You can build a read-only profile by combining `agents.defaults.sandbox.workspaceAccess: "ro"` (or `"none"` for no workspace access) with tool allow/deny lists that block `write`, `edit`, `apply_patch`, `exec`, `process`, etc. Additional hardening options:

- `tools.exec.applyPatch.workspaceOnly: true` (default) ensures `apply_patch` cannot write/delete outside the workspace directory even when sandboxing is off. Set to `false` only if you intentionally want `apply_patch` to touch files outside the workspace.
- `tools.fs.workspaceOnly: true` (optional) restricts `read`/`write`/`edit`/`apply_patch` paths and native prompt image auto-load paths to the workspace directory.
- Keep filesystem roots narrow: avoid broad roots like your home directory for agent workspaces/sandbox workspaces, because broad roots can expose sensitive local files (for example state/config under `~/.openclaw`) to filesystem tools.

## Plugins

Plugins run **in-process** with the Gateway — treat them as trusted code. Only install plugins from sources you trust, prefer explicit `plugins.allow` allowlists, review plugin config before enabling, and restart the Gateway after plugin changes. If you install or update plugins (`openclaw plugins install <package>`, `openclaw plugins update <id>`), treat it like running untrusted code:

- The install path is the per-plugin directory under the active plugin install root.
- OpenClaw does not run built-in local dangerous-code blocking during install/update. Use `security.installPolicy` for operator-owned local allow/block decisions and `openclaw security audit --deep` for diagnostic scanning.
- npm and git plugin installs run package-manager dependency convergence only during the explicit install/update flow. Local paths and archives are treated as self-contained plugin packages; OpenClaw copies/references them without running `npm install`.
- Prefer pinned, exact versions (`@scope/pkg@1.2.3`), and inspect the unpacked code on disk before enabling.
- `--dangerously-force-unsafe-install` is deprecated and no longer changes plugin install/update behavior.
- Configure `security.installPolicy` when operators need a trusted local command to make host-specific allow/block decisions for skill and plugin installs. This policy runs after source material is staged but before installation continues, applies to ClawHub skills too, and is not bypassed by deprecated unsafe flags. See [Plugins](https://docs.openclaw.ai/tools/plugin).

## Dynamic skills (watcher / remote nodes)

OpenClaw can refresh the skills list mid-session. The **skills watcher** means changes to `SKILL.md` can update the skills snapshot on the next agent turn, and **remote nodes** mean connecting a macOS node can make macOS-only skills eligible (based on bin probing). Treat skill folders as **trusted code** and restrict who can modify them.

## Node execution (system.run)

If a macOS node is paired, the Gateway can invoke `system.run` on that node. This is **remote code execution** on the Mac:

- Requires node pairing (approval + token). Gateway node pairing is not a per-command approval surface — it establishes node identity/trust and token issuance.
- The Gateway applies a coarse global node command policy via `gateway.nodes.allowCommands` / `denyCommands`.
- It is controlled on the Mac via **Settings → Exec approvals** (security + ask + allowlist). The per-node `system.run` policy is the node's own exec approvals file (`exec.approvals.node.*`), which can be stricter or looser than the gateway's global command-ID policy.
- A node running with `security="full"` and `ask="off"` is following the default trusted-operator model; treat that as expected behavior unless your deployment explicitly requires a tighter approval or allowlist stance.
- Approval mode binds exact request context and, when possible, one concrete local script/file operand. If OpenClaw cannot identify exactly one direct local file for an interpreter/runtime command, approval-backed execution is denied rather than promising full semantic coverage.
- For `host=node`, approval-backed runs also store a canonical prepared `systemRunPlan`; later approved forwards reuse that stored plan, and gateway validation rejects caller edits to command/cwd/session context after the approval request was created.
- If you don't want remote execution, set security to **deny** and remove node pairing for that Mac.

For triage: a reconnecting paired node advertising a different command list is not, by itself, a vulnerability if the Gateway global policy and the node's local exec approvals still enforce the actual execution boundary; reports that treat node pairing metadata as a second hidden per-command approval layer are usually policy/UX confusion, not a security boundary bypass.

**Source**: OpenClaw documentation — `gateway/security` (mirror `inbox/openclaw_docs/gateway/security.md`)
**Last Updated**: 2026-06-22
**Status**: Active
