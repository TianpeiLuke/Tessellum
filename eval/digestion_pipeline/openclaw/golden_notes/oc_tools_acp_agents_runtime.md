---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - acp
keywords:
  - acp delivery model
  - parent-owned one-shot acp session
  - acp sandbox compatibility
  - acp session target resolution
  - acp controls runtime options mapping
  - acp troubleshooting
  - sessions_send a2a delivery
  - resumeSessionId session/load
topics:
  - OpenClaw
  - ACP runtime
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/acp-agents
access_control_group: ["general"]
---

# OpenClaw — ACP Backend Runtime: Delivery, Sandbox, Controls, and Troubleshooting

## Overview

This note documents the operational runtime of the OpenClaw **ACP backend**: how a spawned external harness session delivers results, how it interacts (or not) with the OpenClaw sandbox, how `/acp` actions resolve a session target, the `/acp` controls and their runtime-options mapping, and troubleshooting. It mirrors the `tools/acp-agents` sections **Delivery model**, **Sandbox compatibility**, **Session target resolution**, **ACP controls** (with **Runtime options mapping**), the **acpx** pointer, and **Troubleshooting**. The concept layer and the spawn/bind operator workflow live in sibling notes linked below.

## Delivery Model

ACP sessions are either **interactive workspaces** or **parent-owned background work**, and the delivery path depends on that shape.

### Interactive ACP sessions

Interactive sessions keep talking on a visible chat surface, created by `/acp spawn ... --bind here` (binds the current conversation), `/acp spawn ... --thread ...` (binds a channel thread/topic), or persistent `bindings[].type="acp"` entries. Follow-ups route directly to the ACP session and ACP output is delivered back to that same channel/thread/topic.

What OpenClaw sends to the harness: bound follow-ups go as prompt text (plus attachments only when the harness/backend supports them); `/acp` management and local Gateway commands are intercepted before dispatch; completion events are materialized per target — OpenClaw agents get OpenClaw's internal runtime-context envelope while external harnesses get a plain prompt with the child result. The raw `<<<BEGIN_OPENCLAW_INTERNAL_CONTEXT>>>` envelope must never reach an external harness or ACP user transcript; transcript entries use the user-visible trigger text or plain completion prompt, and internal event metadata stays structured in OpenClaw.

### Parent-owned one-shot ACP sessions

One-shot ACP sessions spawned by another agent run are background children, like sub-agents. The parent asks for work with `sessions_spawn({ runtime: "acp", mode: "run" })`; the child runs in its own harness session on the **same background lane as native sub-agent spawns**, so a slow harness does not block unrelated main-session work. Completion reports back through the task-completion announce path — OpenClaw converts internal completion metadata into a plain ACP prompt before sending it to an external harness (so harnesses see no OpenClaw-only runtime markers), and the parent rewrites the result in normal assistant voice when a user-facing reply is useful. This is **not** a peer-to-peer chat; the child already has a completion channel back to the parent.

### `sessions_send` and A2A delivery

`sessions_send` can target another session after spawn. For normal peer sessions, OpenClaw uses an **agent-to-agent (A2A)** follow-up path after injecting the message: wait for the target's reply, optionally exchange a bounded number of follow-up turns, ask the target to produce an announce message, and deliver it to the visible channel/thread. A2A is a fallback for peer sends needing a visible follow-up; it stays enabled when an unrelated session can see and message an ACP target (e.g. broad `tools.sessions.visibility`).

OpenClaw skips A2A **only** when the requester is the parent of its own parent-owned one-shot ACP child — running A2A on top of task completion would wake the parent with the child's result, forward the reply back into the child, and create a parent/child echo loop. The `sessions_send` result then reports `delivery.status="skipped"` because the completion path already owns the result.

### Resume an existing session

Use `resumeSessionId` to continue a previous ACP session; the agent replays its history via `session/load`:

```json
{
  "task": "Continue where we left off - fix the remaining test failures",
  "runtime": "acp",
  "agentId": "codex",
  "resumeSessionId": "<previous-session-id>"
}
```

Notes on resume: `resumeSessionId` and `streamTo` only apply when `runtime: "acp"` (the default sub-agent runtime ignores them); `resumeSessionId` is a host-local ACP/harness resume id, not an OpenClaw channel session key, so OpenClaw still checks ACP spawn + target-agent policy while the backend/harness owns authorization for loading that upstream id; it restores upstream history while `thread`/`mode` still apply to the new OpenClaw session (`mode: "session"` still requires `thread: true`); the target agent must support `session/load` (Codex and Claude Code do); and an unknown id fails with a clear error — no silent fallback to a new session.

### Post-deploy smoke test

After a gateway deploy, run a live end-to-end check: verify the deployed gateway version/commit on the target host; open a temporary ACPX bridge session to a live agent; ask it to call `sessions_spawn` with `runtime: "acp"`, `agentId: "codex"`, `mode: "run"`, task `Reply with exactly LIVE-ACP-SPAWN-OK`; verify `accepted=yes`, a real `childSessionKey`, no validator error; then clean up the bridge session. Keep the gate on `mode: "run"` and skip `streamTo: "parent"` — thread-bound `mode: "session"` and stream-relay are separate passes.

## Sandbox Compatibility

ACP sessions currently run on the **host runtime, NOT inside the OpenClaw sandbox**. Security boundary: the external harness reads/writes per its own CLI permissions and the selected `cwd`; OpenClaw's sandbox policy does **not** wrap ACP harness execution; OpenClaw still enforces ACP feature gates, allowed agents, session ownership, channel bindings, and Gateway delivery policy; and `runtime: "subagent"` is the sandbox-enforced alternative for native work.

Limitations: if the requester session is sandboxed, ACP spawns are blocked for both `sessions_spawn({ runtime: "acp" })` and `/acp spawn`; and `sessions_spawn` with `runtime: "acp"` does not support `sandbox: "require"`.

## Session Target Resolution

Most `/acp` actions accept an optional session target (`session-key`, `session-id`, or `session-label`). Resolution order:

1. **Explicit target argument** (or `--session` for `/acp steer`) — tries key, then UUID-shaped session id, then label.
2. **Current thread binding** — if this conversation/thread is bound to an ACP session.
3. **Current requester session fallback.**

Current-conversation and thread bindings both participate in step 2. If no target resolves, OpenClaw returns a clear error (`Unable to resolve session target: ...`).

## ACP Controls

The `/acp` surface controls a target ACP session:

| Command | What it does | Example |
| --- | --- | --- |
| `/acp spawn` | Create ACP session; optional bind/thread. | `/acp spawn codex --bind here --cwd /repo` |
| `/acp cancel` | Cancel in-flight turn. | `/acp cancel agent:codex:acp:<uuid>` |
| `/acp steer` | Steer instruction to running session. | `/acp steer --session support inbox prioritize failing tests` |
| `/acp close` | Close session, unbind thread targets. | `/acp close` |
| `/acp status` | Show backend, mode, state, options, capabilities. | `/acp status` |
| `/acp set-mode` | Set runtime mode. | `/acp set-mode plan` |
| `/acp set` | Generic runtime config write. | `/acp set model openai/gpt-5.4` |
| `/acp cwd` | Set cwd override. | `/acp cwd /Users/user/Projects/repo` |
| `/acp permissions` | Set approval policy profile. | `/acp permissions strict` |
| `/acp timeout` | Set runtime timeout (seconds). | `/acp timeout 120` |
| `/acp model` | Set runtime model override. | `/acp model anthropic/claude-opus-4-6` |
| `/acp reset-options` | Remove runtime option overrides. | `/acp reset-options` |
| `/acp sessions` | List recent ACP sessions from store. | `/acp sessions` |
| `/acp doctor` | Backend health/capabilities/fixes. | `/acp doctor` |
| `/acp install` | Print deterministic install/enable steps. | `/acp install` |

`/acp status` shows the effective runtime options plus runtime- and backend-level session identifiers; unsupported-control errors surface clearly when a backend lacks a capability. `/acp sessions` reads the store for the current bound/requester session; target tokens resolve through gateway session discovery, including custom per-agent `session.store` roots.

### Runtime Options Mapping

Each convenience command maps to a canonical runtime option; OpenClaw sends the backend-advertised equivalent when present:

| Command | Maps to | Notes |
| --- | --- | --- |
| `/acp model <id>` | runtime key `model` | Codex ACP normalizes `openai/<model>` to the adapter model id and maps slash reasoning suffixes (`openai/gpt-5.4/high`) to `reasoning_effort`. |
| `/acp set thinking <level>` | canonical `thinking` | Prefers `thinking`, then `effort`, `reasoning_effort`, or `thought_level`. Codex ACP maps values to `reasoning_effort`. |
| `/acp permissions <profile>` | canonical `permissionProfile` | Equivalents: `approval_policy`, `permission_profile`, `permissions`, or `permission_mode`. |
| `/acp timeout <seconds>` | canonical `timeoutSeconds` | Equivalents: `timeout` or `timeout_seconds`. |
| `/acp cwd <path>` | runtime cwd override | Direct update. |
| `/acp set <key> <value>` | generic | `key=cwd` uses the cwd override path. |
| `/acp reset-options` | clears all runtime overrides | - |

## acpx Harness, Plugin Setup, and Permissions (pointer)

For acpx harness configuration (Claude Code / Codex / Gemini CLI aliases), the plugin-tools and OpenClaw-tools MCP bridges, and ACP permission modes, see `oc_tools_acp_agents_setup` (mirroring `tools/acp-agents-setup`). The `permissionMode` / `nonInteractivePermissions` knobs in Troubleshooting below are configured there.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ACP runtime backend is not configured` | Backend missing/disabled or blocked by `plugins.allow`. | Install/enable backend, add `acpx` to `plugins.allow` if set, run `/acp doctor`. |
| `ACP is disabled by policy (acp.enabled=false)` | ACP globally disabled. | Set `acp.enabled=true`. |
| `ACP dispatch is disabled by policy (acp.dispatch.enabled=false)` | Auto thread-message dispatch disabled. | Set `acp.dispatch.enabled=true`; explicit `sessions_spawn({ runtime: "acp" })` still works. |
| `ACP agent "<id>" is not allowed by policy` | Agent not in allowlist. | Use allowed `agentId` or update `acp.allowedAgents`. |
| `/acp doctor` reports backend not ready right after startup | Backend missing/disabled, blocked by allow/deny, or executable unavailable. | Install/enable backend, rerun `/acp doctor`, inspect the install/policy error. |
| Harness command not found | Adapter CLI not installed, plugin missing, or first-run `npx` fetch failed. | Run `/acp doctor`, install/prewarm the adapter on the host, or set the acpx command. |
| Model-not-found from the harness | Model id valid elsewhere but not this target. | Use a model listed by that harness, configure it there, or omit the override. |
| Vendor auth error from the harness | Target CLI/provider not logged in. | Log in or provide the provider key on the Gateway host environment. |
| `Unable to resolve session target: ...` | Bad key/id/label token. | Run `/acp sessions`, copy exact key/label, retry. |
| `--bind here requires running /acp spawn inside an active ... conversation` | No active bindable conversation. | Move to the target chat/channel, or use unbound spawn. |
| `Conversation bindings are unavailable for <channel>.` | Adapter lacks current-conversation binding. | Use `--thread ...`, configure `bindings[]`, or switch channel. |
| `--thread here requires running /acp spawn inside an active ... thread` | `--thread here` outside a thread. | Move to the thread or use `--thread auto`/`off`. |
| `Only <user-id> can rebind this channel/conversation/thread.` | Another user owns the active binding. | Rebind as owner or use a different conversation/thread. |
| `Thread bindings are unavailable for <channel>.` | Adapter lacks thread binding. | Use `--thread off` or a supported adapter. |
| `Sandboxed sessions cannot spawn ACP sessions ...` | ACP host-side; requester sandboxed. | Use `runtime="subagent"`, or spawn from a non-sandboxed session. |
| `sessions_spawn sandbox="require" is unsupported for runtime="acp" ...` | `sandbox="require"` for ACP. | Use `runtime="subagent"`, or ACP `sandbox="inherit"` from a non-sandboxed session. |
| `Cannot apply --model ... did not advertise model support` | No generic ACP model switching on target. | Use a harness advertising ACP `models`/`session/set_model`, Codex ACP refs, or set it in the harness. |
| Missing ACP metadata for bound session | Stale/deleted ACP session metadata. | Recreate with `/acp spawn`, then rebind/focus thread. |
| `AcpRuntimeError: Permission prompt unavailable in non-interactive mode` | `permissionMode` blocks writes/exec. | Set `plugins.entries.acpx.config.permissionMode` to `approve-all` and restart gateway. |
| ACP session fails early with little output | Prompts blocked by `permissionMode`/`nonInteractivePermissions`. | Check logs for `AcpRuntimeError`; set `permissionMode=approve-all` or `nonInteractivePermissions=deny`. |
| ACP session stalls indefinitely after completing work | Harness finished but session did not report completion. | Update OpenClaw; acpx cleanup reaps stale wrapper/adapter processes on close and startup. |
| Harness sees `<<<BEGIN_OPENCLAW_INTERNAL_CONTEXT>>>` | Internal envelope leaked across the ACP boundary. | Update OpenClaw and rerun; external harnesses get plain prompts only. |

Note: `Command blocked by PreToolUse hook: Native hook relay unavailable` belongs to the native Codex hook relay, not ACP/acpx — in a bound Codex chat start fresh with `/new` or `/reset`; if it works once then returns on the next native tool call, restart the Codex app-server or OpenClaw Gateway.

**Source**: OpenClaw documentation — `tools/acp-agents` (mirror `inbox/openclaw_docs/tools/acp-agents.md`), sections Delivery model · Sandbox compatibility · Session target resolution · ACP controls · Troubleshooting
**Last Updated**: 2026-06-22
**Status**: Active
