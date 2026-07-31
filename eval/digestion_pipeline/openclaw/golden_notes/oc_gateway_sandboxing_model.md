---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - sandboxing
keywords:
  - openclaw sandboxing model
  - what gets sandboxed
  - sandbox modes off non-main all
  - sandbox scope agent session shared
  - tools.elevated escape hatch
  - sandbox tool policy precedence
  - multi-agent sandbox overrides
  - session.mainKey non-main
topics:
  - OpenClaw
  - Sandboxing
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/sandboxing
access_control_group: ["general"]
---

# OpenClaw — The Sandboxing Model (What, Modes, Scope, Escape Hatches)

## Overview

This note models OpenClaw **sandboxing**: an optional, configuration-driven mechanism that runs tool execution inside isolated sandbox backends to reduce blast radius while the Gateway process itself stays on the host. It mirrors the conceptual half of the `gateway/sandboxing` source page — **what gets sandboxed** vs what stays on host, the `mode` axis (when sandboxing applies), the `scope` axis (how many containers), how **tool policy and escape hatches** (`tools.elevated`) layer on top, and how **multi-agent overrides** redefine the model per agent. The companion note `oc_gateway_sandboxing_backends` covers the procedural backend setup (Docker/SSH/OpenShell, workspace access, bind mounts, images, `setupCommand`) and is not repeated here. As the source warns, sandboxing "is not a perfect security boundary, but it materially limits filesystem and process access when the model does something dumb."

## What Gets Sandboxed

Sandboxing is **optional** and controlled by configuration (`agents.defaults.sandbox` or `agents.list[].sandbox`). If sandboxing is off, tools run on the host. The Gateway stays on the host; tool execution runs in an isolated sandbox only when enabled. The model has a clear in/out boundary.

**Sandboxed when enabled:**

- Tool execution — `exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.
- Optional sandboxed browser — `agents.defaults.sandbox.browser`.

The sandboxed browser has its own controls: it auto-starts by default (ensuring CDP is reachable) when the browser tool needs it, tuned via `agents.defaults.sandbox.browser.autoStart` and `agents.defaults.sandbox.browser.autoStartTimeoutMs`; sandbox browser containers use a dedicated Docker network (`openclaw-sandbox-browser`) instead of the global `bridge` network, configurable with `agents.defaults.sandbox.browser.network`; `agents.defaults.sandbox.browser.cdpSourceRange` restricts container-edge CDP ingress with a CIDR allowlist (for example `172.21.0.1/32`); noVNC observer access is password-protected by default (a short-lived token URL serves a local bootstrap page and opens noVNC with the password in the URL fragment, not query/header logs); `agents.defaults.sandbox.browser.allowHostControl` lets sandboxed sessions target the host browser explicitly; and optional allowlists (`allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`) gate `target: "custom"`.

**Not sandboxed:**

- The Gateway process itself.
- Any tool explicitly allowed to run outside the sandbox (e.g. `tools.elevated`). Elevated exec bypasses sandboxing and uses the configured escape path (`gateway` by default, or `node` when the exec target is `node`). If sandboxing is off, `tools.elevated` does not change execution (already on host) — see Elevated Mode (`/tools/elevated`).

## Modes — When Sandboxing Applies

`agents.defaults.sandbox.mode` controls **when** sandboxing is used. There are three values:

- `off` — No sandboxing.
- `non-main` — Sandbox only **non-main** sessions (the default choice if you want normal chats on host). `"non-main"` is based on `session.mainKey` (default `"main"`), **not** agent id. Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.
- `all` — Every session runs in a sandbox.

The `non-main` semantics are the subtle part of the model: because the decision keys off `session.mainKey` rather than agent identity, any session whose key differs from `"main"` — including group and channel sessions — is treated as non-main and sandboxed.

## Scope — How Many Containers

`agents.defaults.sandbox.scope` controls **how many containers** are created:

- `agent` (default) — one container per agent.
- `session` — one container per session.
- `shared` — one container shared by all sandboxed sessions.

Scope is orthogonal to mode: `mode` decides *whether* a given session is sandboxed, while `scope` decides *how container instances are partitioned* across the sessions that do get sandboxed.

## Tool Policy and Escape Hatches

Tool allow/deny policies still apply **before** sandbox rules. If a tool is denied globally or per-agent, sandboxing does not bring it back — the deny gate has higher precedence than any sandbox behavior. This precedence rule is the key interaction between the two layers: sandboxing decides *where* a permitted tool runs, but tool policy decides *whether* the tool is permitted at all.

`tools.elevated` is an explicit **escape hatch** that runs `exec` outside the sandbox (`gateway` by default, or `node` when the exec target is `node`). `/exec` directives only apply for authorized senders and persist per session; to hard-disable `exec`, use a tool policy deny rather than relying on sandboxing (see Sandbox vs Tool Policy vs Elevated, `/gateway/sandbox-vs-tool-policy-vs-elevated`).

For debugging the composed model:

- Use `openclaw sandbox explain` to inspect the effective sandbox mode, tool policy, and fix-it config keys.
- See Sandbox vs Tool Policy vs Elevated (`/gateway/sandbox-vs-tool-policy-vs-elevated`) for the "why is this blocked?" mental model.

The source's closing guidance for this layer is simply: "Keep it locked down."

## Multi-Agent Overrides

Each agent can override the sandbox and tool model: `agents.list[].sandbox` and `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools` for sandbox tool policy). This is what lets the global `agents.defaults.sandbox` model be selectively redefined per agent. Precedence between the global defaults and per-agent overrides is documented in Multi-Agent Sandbox & Tools (`/tools/multi-agent-sandbox-tools`).

**Source**: OpenClaw documentation — `gateway/sandboxing` (mirror `inbox/openclaw_docs/gateway/sandboxing.md`), sections: What gets sandboxed, Modes, Scope, Tool policy and escape hatches, Multi-agent overrides
**Last Updated**: 2026-06-22
**Status**: Active
