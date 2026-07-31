---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - policy
keywords:
  - openclaw policy conformance layer
  - policy.jsonc authored requirements
  - observed evidence model
  - scoped overlays agentids channelids
  - policy rule reference categories
  - deny-first allow deny rules
  - strictness metadata subsets supersets
  - sandbox exec-approvals tool posture rules
topics:
  - OpenClaw
  - Policy Conformance Layer
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/cli/policy
access_control_group: ["general"]
---

# OpenClaw — Policy Conformance Layer and Rule Reference

## Overview

This note defines the concept of `openclaw policy`: an enterprise **conformance layer** over existing OpenClaw settings, provided by the bundled Policy plugin. It does NOT add a second configuration system — `policy.jsonc` declares *authored requirements*, OpenClaw *observes the active workspace as evidence*, and the final conformance signal is a clean `doctor --lint` run to which policy contributes findings. This note mirrors the `cli/policy` source page's intro, Quick start, rule-authority semantics, scoped-overlay model, and the full per-category Policy rule reference. The companion evidence/attestation contract (`policy check`/`compare`/`watch`, the attestation tuple, the findings catalog) is in **[oc_cli_policy_attestation](oc_cli_policy_attestation.md)**; enabling/hash-locking/repair lives in **[oc_cli_policy_configure](oc_cli_policy_configure.md)**.

## What Policy Is

Policy is an enterprise conformance layer over existing OpenClaw settings; it does not add a second configuration system. `policy.jsonc` defines authored requirements, OpenClaw observes the active workspace as evidence, and policy health checks report drift through `doctor --lint`. The final conformance signal is a clean `doctor --lint` run; policy contributes findings to that shared lint surface instead of creating a separate health gate.

Policy currently manages: configured channels, MCP servers, model providers, network SSRF posture, ingress/channel access posture, Gateway exposure posture, agent workspace posture, data-handling posture, OpenClaw config secret provider/auth profile posture, and governed tool declarations. For example, IT or a workspace operator can record that Telegram is not an approved channel provider, restrict MCP servers and model refs to approved entries, require private-network fetch/browser access to remain disabled, require direct-message session isolation and channel ingress posture to stay within reviewed bounds, require Gateway bind/auth/HTTP exposure to stay within reviewed bounds, require agent workspace access and tool denies to stay in a reviewed posture, require OpenClaw config SecretRefs to use managed providers, require config auth profiles to carry provider/mode metadata, require governed tools to carry risk and sensitivity metadata, require sensitive logging redaction, deny telemetry content capture, require session retention maintenance, deny session transcript memory indexing, then use `doctor --lint` as the shared conformance gate.

Use policy when a workspace needs a durable statement such as "these channels must not be enabled" or "governed tools must declare approval metadata" and a repeatable way to prove that OpenClaw still conforms to that statement. Use regular config and workspace docs alone when you only need local behavior and do not need policy findings or attestation output.

## Quick Start (minimal policy.jsonc)

Enable the bundled Policy plugin before first use: `openclaw plugins enable policy`. When policy is enabled, doctor can load policy health checks without activating arbitrary plugins. The plugin remains enabled if `policy.jsonc` is missing, so doctor can report the missing artifact. Policy is **authored, not generated** from the user's current settings. A minimal policy spanning channels, MCP servers, model providers, network posture, ingress/channel access, Gateway exposure, agent workspace posture, sandbox runtime posture, data-handling posture, secret provider/auth profile posture, exec approval file posture, and tool metadata looks like this (verbatim from source):

```jsonc
{
  "channels": {
    "denyRules": [
      { "id": "no-telegram", "when": { "provider": "telegram" },
        "reason": "Telegram is not approved for this workspace." },
    ],
  },
  "mcp": { "servers": { "allow": ["docs"], "deny": ["untrusted"] } },
  "models": { "providers": { "allow": ["openai", "anthropic"], "deny": ["openrouter"] } },
  "network": { "privateNetwork": { "allow": false } },
  "ingress": {
    "session": { "requireDmScope": "per-channel-peer" },
    "channels": { "allowDmPolicies": ["pairing", "allowlist", "disabled"],
      "denyOpenGroups": true, "requireMentionInGroups": true },
  },
  "gateway": {
    "exposure": { "allowNonLoopbackBind": false, "allowTailscaleFunnel": false },
    "auth": { "requireAuth": true, "requireExplicitRateLimit": true },
    "controlUi": { "allowInsecure": false },
    "remote": { "allow": false },
    "http": { "denyEndpoints": ["chatCompletions", "responses"], "requireUrlAllowlists": true },
  },
  "agents": { "workspace": { "allowedAccess": ["none", "ro"],
    "denyTools": ["exec", "process", "write", "edit", "apply_patch"] } },
  "dataHandling": {
    "sensitiveLogging": { "requireRedaction": true },
    "telemetry": { "denyContentCapture": true },
    "retention": { "requireSessionMaintenance": true },
    "memory": { "denySessionTranscriptIndexing": true },
  },
  "secrets": { "requireManagedProviders": true, "denySources": ["exec"], "allowInsecureProviders": false },
  "auth": { "profiles": { "requireMetadata": ["provider", "mode"], "allowModes": ["api_key", "token"] } },
  "execApprovals": { "requireFile": true, "defaults": { "allowSecurity": ["deny"] },
    "agents": { "allowSecurity": ["deny", "allowlist"], "allowAutoAllowSkills": false,
      "allowlist": { "expected": ["deploy", "status"] } } },
  "tools": {
    "requireMetadata": ["risk", "sensitivity", "owner"],
    "profiles": { "allow": ["messaging", "minimal"] },
    "fs": { "requireWorkspaceOnly": true },
    "exec": { "allowSecurity": ["deny", "allowlist"], "requireAsk": ["always"], "allowHosts": ["sandbox"] },
    "elevated": { "allow": false },
    "denyTools": ["group:runtime", "group:fs"],
  },
}
```

## Rule-Authority Semantics (observed-state evidence)

**The rules are the authority. A category block is only a namespace; checks run when a concrete rule is present.** OpenClaw reads current `channels.*`, `mcp.servers.*`, `models.providers.*`, selected agent model refs, network SSRF settings, direct-message session scope, channel DM policy, channel group policy, channel/group mention gates, Gateway bind/auth/Control UI/Tailscale/remote/HTTP posture, agent sandbox workspace access and tool deny posture, data-handling config posture, config secret provider and SecretRef provenance, config auth profile metadata, configured global/per-agent tool posture, and `TOOLS.md` declarations as evidence, then reports observed state that does not conform.

Important semantic edges from source: if a policy denies non-loopback Gateway binds, omit `gateway.bind` only when you are willing to review the runtime default — set `gateway.bind=loopback` for strict config conformance. For read-only agent posture, configure sandbox mode on the applicable defaults or agent and set `workspaceAccess` to `none` or `ro`; omitted or `off` sandbox mode does not satisfy a read-only/no-write policy. `agents.workspace.denyTools` supports `exec`, `process`, `write`, `edit`, and `apply_patch`; `group:fs` covers file mutation tools and `group:runtime` covers shell/process tools. Exec approval policy reads the named `exec-approvals.json` product artifact only when an `execApprovals` rule is present; evidence records defaults, per-agent posture, and allowlist patterns without socket tokens or last-used command text. **Policy does not enforce tool calls at runtime.** Secret evidence records provider/source posture and SecretRef metadata, never raw secret values. Policy does not read or attest per-agent credential stores such as `auth-profiles.json`; those remain owned by the existing auth and credential flows. Data-handling evidence is config-level posture only — it checks configured redaction mode, telemetry content-capture toggles, session maintenance mode, and session-transcript memory indexing settings; it does not inspect raw logs, telemetry exports, transcript contents, or memory files, nor prove that no personal data or secrets exist.

## Policy Rule Reference

Each policy field is optional; a check runs only when the matching rule is present in `policy.jsonc`. The observed state is existing OpenClaw config or workspace metadata; policy reports drift but does not rewrite runtime behavior unless a repair path is explicitly available and enabled. **Policy files are strict**: unsupported sections or rule keys are reported as `policy/policy-jsonc-invalid` instead of being ignored.

### Scoped overlays

Policy overlays keep broad top-level rules global, then let named scope blocks add stricter normal policy sections for explicit selectors. A scope name is a descriptive bucket only; matching uses the selector values inside the scope. The overlay is **additive**: global claims still run, and a scoped claim can emit its own finding against the same observed config. Use `scopes.<scopeName>` when one set of agents or channels needs stricter policy than the top-level baseline. Agent-scoped sections use `agentIds`, which supports `tools.*`, `agents.workspace.*`, `sandbox.*`, `dataHandling.memory.*`, and `execApprovals.*`. Channel-scoped ingress uses `channelIds`, which supports `ingress.channels.*`. If an `agentIds` entry is not present in `agents.list[]`, OpenClaw evaluates the scoped rule against inherited global/default posture for that runtime agent id.

```jsonc
{
  "tools": { "exec": { "allowHosts": ["sandbox", "node"] } },
  "sandbox": { "requireMode": ["all", "non-main"] },
  "scopes": {
    "release-lockdown": {
      "agentIds": ["release-agent"],
      "tools": { "exec": { "allowHosts": ["sandbox"], "allowSecurity": ["deny", "allowlist"],
        "requireAsk": ["always"] }, "denyTools": ["exec", "process", "write", "edit", "apply_patch"] },
      "sandbox": { "requireMode": ["all"], "allowBackends": ["docker"] },
      "dataHandling": { "memory": { "denySessionTranscriptIndexing": true } },
    },
    "shell-sandbox": { "agentIds": ["shell-agent"],
      "sandbox": { "allowBackends": ["openshell"], "containers": { "requireReadOnlyMounts": false } } },
    "telegram-ingress": { "channelIds": ["telegram"],
      "ingress": { "channels": { "allowDmPolicies": ["pairing"], "denyOpenGroups": true,
        "requireMentionInGroups": true } } },
  },
}
```

The same agent can appear in multiple scopes when each scope governs different fields. A repeated scoped field for the same agent must be equally or more restrictive according to policy metadata; weaker duplicate claims are rejected. **Strictness metadata treats allow-lists as subsets, deny-lists as supersets, and required booleans as fixed requirements.** Container posture policy is evaluated only against evidence OpenClaw can observe for the matched agent — if an enabled `sandbox.containers.*` rule applies to an agent whose backend cannot expose that field, policy reports `policy/sandbox-container-posture-unobservable` instead of passing. Top-level `ingress.session.requireDmScope` remains global because `session.dmScope` is not channel-attributable evidence. Every scope present in `policy.jsonc` must be valid and enforceable.

| Selector | Supported sections | Use when |
|---|---|---|
| `agentIds` | `tools`, `agents.workspace`, `sandbox`, `dataHandling.memory`, `execApprovals` | One or more runtime agents need stricter rules. |
| `channelIds` | `ingress.channels` | One or more channels need stricter ingress rules. |

### Category rule tables (condensed)

Channels, MCP servers, model providers, network — allow/deny over configured entries:

| Policy field | Observed state |
|---|---|
| `channels.denyRules[].when.provider` / `.reason` | `channels.*` provider/enabled; finding-message context |
| `mcp.servers.allow` / `mcp.servers.deny` | `mcp.servers.*` ids (allowlist / denylist) |
| `models.providers.allow` / `models.providers.deny` | `models.providers.*` ids and selected model refs |
| `network.privateNetwork.allow` | Private-network SSRF escape hatches (`false` = keep disabled) |

Ingress/channel access and Gateway exposure:

| Policy field | Observed state |
|---|---|
| `ingress.session.requireDmScope` | `session.dmScope` (DM isolation scope) |
| `ingress.channels.allowDmPolicies` | `channels.*.dmPolicy` + legacy DM policy fields |
| `ingress.channels.denyOpenGroups` | Channel/account/group ingress policy |
| `ingress.channels.requireMentionInGroups` | Channel/account/group/guild/nested mention gates |
| `gateway.exposure.allowNonLoopbackBind` | `gateway.bind` (`false` = require loopback) |
| `gateway.exposure.allowTailscaleFunnel` | Tailscale serve/funnel posture |
| `gateway.auth.requireAuth` / `.requireExplicitRateLimit` | `gateway.auth.mode` / `gateway.auth.rateLimit` |
| `gateway.controlUi.allowInsecure` | Control UI insecure auth/device/origin toggles |
| `gateway.remote.allow` | Remote Gateway mode/config |
| `gateway.http.denyEndpoints` / `.requireUrlAllowlists` | Gateway HTTP API endpoints / URL-fetch inputs |

Agent workspace, sandbox posture, data handling:

| Policy field | Observed state |
|---|---|
| `agents.workspace.allowedAccess` | `agents.defaults/list[].sandbox.workspaceAccess` (e.g. `none`/`ro`) |
| `agents.workspace.denyTools` | Global + per-agent tool deny config (`exec`/`process`/`write`/`edit`/`apply_patch`) |
| `sandbox.requireMode` | `agents.defaults.sandbox.mode` + per-agent (missing = implicit `off`) |
| `sandbox.allowBackends` | `agents.defaults.sandbox.backend` + per-agent (`docker`, etc.) |
| `sandbox.containers.denyHostNetwork` / `denyContainerNamespaceJoin` / `requireReadOnlyMounts` / `denyContainerRuntimeSocketMounts` / `denyUnconfinedProfiles` | Container-backed sandbox/browser network/mount/profile posture |
| `sandbox.browser.requireCdpSourceRange` | Sandbox browser CDP source range |
| `dataHandling.sensitiveLogging.requireRedaction` | `logging.redactSensitive` |
| `dataHandling.telemetry.denyContentCapture` | `diagnostics.otel.captureContent` |
| `dataHandling.retention.requireSessionMaintenance` | `session.maintenance.mode` (effective `enforce`) |
| `dataHandling.memory.denySessionTranscriptIndexing` | `memory.qmd.sessions.enabled` + agent `memorySearch.experimental.sessionMemory` |

Note: policy treats missing `sandbox.mode` as the implicit default `off`, so `sandbox.requireMode` reports a fresh/unconfigured sandbox as outside an allowlist such as `["all"]`.

Secrets, exec approvals, auth profiles, tool metadata, and tool posture:

| Policy field | Observed state |
|---|---|
| `secrets.requireManagedProviders` / `denySources` / `allowInsecureProviders` | Config SecretRefs + `secrets.providers.*`; source posture; insecure-provider flags |
| `execApprovals.requireFile` | Active runtime `exec-approvals.json` path (default `~/.openclaw/exec-approvals.json`; `$OPENCLAW_STATE_DIR/exec-approvals.json` when set) |
| `execApprovals.defaults.allowSecurity` | `defaults.security` (default `full`) |
| `execApprovals.agents.allowSecurity` / `allowAutoAllowSkills` | `agents.*.security` (inherits defaults); `autoAllowSkills` posture |
| `execApprovals.agents.allowlist.expected` | Aggregate `agents.*.allowlist[]` `pattern` + optional `argPattern` |
| `auth.profiles.requireMetadata` / `allowModes` | `auth.profiles.*` provider/mode metadata; `.mode` (e.g. `api_key`, `aws-sdk`, `oauth`, `token`) |
| `tools.requireMetadata` | Governed `TOOLS.md` declarations (`risk`, `sensitivity`, `owner`) |
| `tools.profiles.allow` | `tools.profile` + `agents.list[].tools.profile` (e.g. `minimal`/`messaging`/`coding`) |
| `tools.fs.requireWorkspaceOnly` | `tools.fs.workspaceOnly` + per-agent overrides |
| `tools.exec.allowSecurity` / `requireAsk` / `allowHosts` | `tools.exec.security`/`ask`/`host` + per-agent |
| `tools.elevated.allow` | `tools.elevated.enabled` + per-agent elevated posture |
| `tools.alsoAllow.expected` | `tools.alsoAllow` + per-agent (exact match; reports missing/unexpected) |
| `tools.denyTools` | `tools.deny` + `agents.list[].tools.deny` (e.g. `group:runtime`, `group:fs`) |

Exec approvals detail: actual posture rules (`execApprovals.defaults.*` / `execApprovals.agents.*`) require readable artifact evidence; a missing or invalid artifact is reported as unobservable evidence rather than a best-effort pass against synthetic runtime defaults. Once readable, omitted approval fields inherit runtime defaults: missing `defaults.security` is `full`, and missing agent security inherits that default. Evidence includes `defaults`, `agents.*`, and `agents.*.allowlist[].pattern` plus optional `argPattern`, effective `autoAllowSkills` posture, and entry source; it excludes socket path/token, `commandText`, `lastUsedCommand`, resolved paths, and timestamps.

**Source**: OpenClaw documentation — `cli/policy` (mirror `inbox/openclaw_docs/cli/policy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
