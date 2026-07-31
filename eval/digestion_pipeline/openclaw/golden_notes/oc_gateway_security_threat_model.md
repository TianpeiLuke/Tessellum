---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - security
keywords:
  - openclaw threat model
  - personal assistant security model
  - gateway node trust domain
  - trust boundary matrix
  - access control before intelligence
  - not vulnerabilities by design
  - command authorization model
  - control plane tools risk
topics:
  - OpenClaw
  - Gateway Security
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/gateway/security
access_control_group: ["general"]
---

# OpenClaw — Gateway Security Threat Model & Trust Boundaries

## Overview

This note argues OpenClaw's **personal-assistant security model**: the conceptual frame that the rest of the Gateway security corpus cites. It mirrors the threat-model sections of the `gateway/security` source page — the single-trusted-operator scope, the Gateway/node trust domain, the trust-boundary matrix, the "not vulnerabilities by design" triage stance, the stated threat model, the "access control before intelligence" core concept, the command authorization model, and the control-plane-tool risk. The hardening recipes, audit, prompt-injection, and data-protection material those sections imply live in sibling `oc_*` notes; this note states the position, not the procedures.

## Scope first: personal-assistant security model

OpenClaw security guidance assumes a **personal assistant** deployment: **one trusted operator boundary, potentially many agents**. The source frames this as a hard premise rather than a configuration choice — OpenClaw is *not* a hostile multi-tenant security boundary for multiple adversarial users sharing one agent or gateway. The supported posture is one user/trust boundary per gateway (prefer one OS user/host/VPS per boundary); the explicitly unsupported posture is one shared gateway/agent used by mutually untrusted or adversarial users. If adversarial-user isolation is required, the prescribed response is to **split by trust boundary** (separate gateway + credentials, ideally separate OS users/hosts), not to harden one shared instance. A load-bearing corollary: if multiple untrusted users can message one tool-enabled agent, they are treated as **sharing the same delegated tool authority** for that agent. The page hardens within this model and makes no claim of hostile multi-tenant isolation on one shared gateway.

### Deployment and host trust

The model treats the host and config boundary as trusted. If someone can modify Gateway host state/config (`~/.openclaw`, including `openclaw.json`), they are by definition a **trusted operator**. Running one Gateway for multiple mutually untrusted/adversarial operators is not a recommended setup; mixed-trust teams split trust boundaries with separate gateways (or at minimum separate OS users/hosts). The recommended default is one user per machine/host (or VPS), one gateway for that user, and one or more agents in that gateway. Two distinctions anchor the rest of the model: inside one Gateway instance, **authenticated operator access is a trusted control-plane role, not a per-user tenant role**; and **session identifiers (`sessionKey`, session IDs, labels) are routing selectors, not authorization tokens**. Per-user session/memory isolation helps privacy but does not convert a shared agent into per-user host authorization — if several people can message one tool-enabled agent, each can steer that same permission set.

### Shared Slack workspace vs company-shared agent

The page contrasts two shared-inbox shapes. A **shared Slack workspace** ("everyone in Slack can message the bot") is a real risk because the core hazard is delegated tool authority: any allowed sender can induce tool calls (`exec`, browser, network/file tools) within the agent's policy; prompt/content injection from one sender can drive actions affecting shared state, devices, or outputs; and a shared agent holding sensitive credentials/files lets any allowed sender potentially drive exfiltration. The remedy is separate agents/gateways with minimal tools for team workflows, keeping personal-data agents private. A **company-shared agent** is an *acceptable* pattern when everyone using it is in the same trust boundary (e.g. one company team) and the agent is strictly business-scoped — run on a dedicated machine/VM/container, with a dedicated OS user + dedicated browser/profile/accounts, and never sign that runtime into personal Apple/Google accounts or personal password-manager/browser profiles. Mixing personal and company identities on the same runtime collapses the separation and increases personal-data exposure risk.

## Gateway and node trust concept

OpenClaw treats **Gateway and node as one operator trust domain** with different roles. The **Gateway** is the control plane and policy surface (`gateway.auth`, tool policy, routing); the **node** is the remote execution surface paired to that Gateway (commands, device actions, host-local capabilities). A caller authenticated to the Gateway is trusted at Gateway scope; after pairing, node actions are trusted operator actions on that node. Direct loopback backend clients authenticated with the shared gateway token/password can make internal control-plane RPCs without presenting a user device identity — but this is not a remote or browser pairing bypass: network clients, node clients, device-token clients, and explicit device identities still go through pairing and scope-upgrade enforcement. The model restates its anchors here: `sessionKey` is routing/context selection, not per-user auth; exec approvals (allowlist + ask) are guardrails for operator intent, not hostile multi-tenant isolation. OpenClaw's product default for trusted single-operator setups is that host exec on `gateway`/`node` is allowed without approval prompts (`security="full"`, `ask="off"` unless tightened) — **intentional UX, not a vulnerability by itself**. Exec approvals bind exact request context and best-effort direct local file operands; they do not semantically model every runtime/interpreter loader path, so sandboxing and host isolation are the strong boundaries. If hostile-user isolation is needed, split trust boundaries by OS user/host and run separate gateways.

## Trust boundary matrix

The source offers this matrix as the quick model when triaging risk — pairing each boundary/control with what it means and the common misread that should be rejected:

| Boundary or control | What it means | Common misread |
| --- | --- | --- |
| `gateway.auth` (token/password/trusted-proxy/device auth) | Authenticates callers to gateway APIs | "Needs per-message signatures on every frame to be secure" |
| `sessionKey` | Routing key for context/session selection | "Session key is a user auth boundary" |
| Prompt/content guardrails | Reduce model abuse risk | "Prompt injection alone proves auth bypass" |
| `canvas.eval` / browser evaluate | Intentional operator capability when enabled | "Any JS eval primitive is automatically a vuln in this trust model" |
| Local TUI `!` shell | Explicit operator-triggered local execution | "Local shell convenience command is remote injection" |
| Node pairing and node commands | Operator-level remote execution on paired devices | "Remote device control should be treated as untrusted user access by default" |
| `gateway.nodes.pairing.autoApproveCidrs` | Opt-in trusted-network node enrollment policy | "A disabled-by-default allowlist is an automatic pairing vulnerability" |

## Not vulnerabilities by design

The model explicitly closes a set of recurring reports as no-action unless a real boundary bypass is demonstrated. These out-of-scope patterns are:

- Prompt-injection-only chains without a policy, auth, or sandbox bypass.
- Claims that assume hostile multi-tenant operation on one shared host or config.
- Claims that classify normal operator read-path access (e.g. `sessions.list` / `sessions.preview` / `chat.history`) as IDOR in a shared-gateway setup.
- Localhost-only deployment findings (e.g. HSTS on a loopback-only gateway).
- Discord inbound webhook signature findings for inbound paths that do not exist in this repo.
- Reports that treat node pairing metadata as a hidden second per-command approval layer for `system.run`, when the real execution boundary is still the gateway's global node command policy plus the node's own exec approvals.
- Reports that treat configured `gateway.nodes.pairing.autoApproveCidrs` as a vulnerability by itself. It is disabled by default, requires explicit CIDR/IP entries, only applies to first-time `role: node` pairing with no requested scopes, and does not auto-approve operator/browser/Control UI, WebChat, role upgrades, scope upgrades, metadata changes, public-key changes, or same-host loopback trusted-proxy header paths unless loopback trusted-proxy auth was explicitly enabled.
- "Missing per-user authorization" findings that treat `sessionKey` as an auth token.

## The threat model

The page states the threat model plainly. Your AI assistant can: execute arbitrary shell commands; read/write files; access network services; and send messages to anyone (if you give it WhatsApp access). People who message you can: try to trick your AI into doing bad things; social engineer access to your data; and probe for infrastructure details. The asymmetry — a powerful, tool-bearing agent reachable by potentially manipulable senders — is what the rest of the model is built to contain.

## Core concept: access control before intelligence

OpenClaw's stance is that **most failures here are not fancy exploits — they are "someone messaged the bot and the bot did what they asked."** The model is therefore ordered as a three-layer stack:

- **Identity first:** decide who can talk to the bot (DM pairing / allowlists / explicit "open").
- **Scope next:** decide where the bot is allowed to act (group allowlists + mention gating, tools, sandboxing, device permissions).
- **Model last:** assume the model can be manipulated; design so manipulation has limited blast radius.

The deliberate ordering — access control *before* model intelligence — is the principle the audit, hardening, and prompt-injection notes all enforce downstream.

## Command authorization model

Slash commands and directives are only honored for **authorized senders**. Authorization is derived from channel allowlists/pairing plus `commands.useAccessGroups`. A critical edge case: if a channel allowlist is empty or includes `"*"`, commands are effectively **open** for that channel. `/exec` is a session-only convenience for authorized operators — it does **not** write config or change other sessions.

## Control plane tools risk

Two built-in tools can make persistent control-plane changes, making them the highest-risk surface in the model. The `gateway` tool can inspect config with `config.schema.lookup` / `config.get`, and make persistent changes with `config.apply`, `config.patch`, and `update.run`. The `cron` tool can create scheduled jobs that keep running after the original chat/task ends. The runtime constrains the agent-facing `gateway` tool: it still refuses to rewrite `tools.exec.ask` or `tools.exec.security` (legacy `tools.bash.*` aliases are normalized to the same protected exec paths before the write), and agent-driven `gateway config.apply` / `config.patch` edits are **fail-closed by default** — only a narrow set of low-risk runtime tuning, mention-gating, and visible-reply paths are agent-tunable, while global model defaults and prompt overlays stay operator-controlled. New sensitive config trees are therefore protected unless deliberately added to the allowlist. For any agent/surface that handles untrusted content, the page prescribes denying these by default:

```json5
{
  tools: {
    deny: ["gateway", "cron", "sessions_spawn", "sessions_send"],
  },
}
```

Note that `commands.restart=false` only blocks restart actions; it does not disable `gateway` config/update actions.

**Source**: OpenClaw documentation — `gateway/security` (mirror `inbox/openclaw_docs/gateway/security.md`)
**Last Updated**: 2026-06-22
**Status**: Active
