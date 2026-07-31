---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - audit
keywords:
  - openclaw security audit
  - security audit --deep
  - security audit --fix
  - security audit --json
  - audit findings priority order
  - checkid severity classes
  - insecure or dangerous flags
  - config.insecure_or_dangerous_flags
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

# OpenClaw — Running the `openclaw security audit`

## Overview

This note is the operator procedure for running OpenClaw's built-in security diagnostic, `openclaw security audit`, mirroring the quick-check, "what the audit checks", checklist, glossary, and insecure-flags sections of the `gateway/security` source page. It covers the four invocation modes (`--deep`, `--fix`, `--json`), what the audit inspects across inbound access / tool blast radius / network exposure / disk hygiene / plugins / policy drift, the recommended priority order for remediating findings, the structured `checkId` severity classes, and the `config.insecure_or_dangerous_flags` summary of debug switches to keep unset in production. The full per-`checkId` reference catalog (severity, fix key, auto-fix support) is in **[OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md)** (note 7); this note is the operator-facing summary.

## Quick check: `openclaw security audit`

Run the audit regularly — especially after changing config or exposing network surfaces. The four invocation modes are:

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
openclaw security audit --json
```

- Plain `openclaw security audit` flags common footguns: Gateway auth exposure, browser control exposure, elevated allowlists, filesystem permissions, permissive exec approvals, and open-channel tool exposure.
- `--deep` additionally attempts a best-effort live Gateway probe (and runs the code-safety scan for plugins/skills).
- `--fix` stays intentionally narrow: it flips common open group policies to allowlists, restores `logging.redactSensitive: "tools"`, tightens state/config/include-file permissions, and uses Windows ACL resets instead of POSIX `chmod` when running on Windows.
- `--json` emits machine-readable output for tooling.

The audit also cross-links [Formal Verification (Security Models)](https://docs.openclaw.ai/security/formal-verification). OpenClaw is both a product and an experiment — wiring frontier-model behavior into real messaging surfaces and real tools — so **there is no "perfectly secure" setup.** The goal is to be deliberate about who can talk to your bot, where the bot is allowed to act, and what the bot can touch; start with the smallest access that still works, then widen it as you gain confidence.

## What the audit checks (high level)

The audit inspects these surfaces:

- **Inbound access** (DM policies, group policies, allowlists): can strangers trigger the bot?
- **Tool blast radius** (elevated tools + open rooms): could prompt injection turn into shell/file/network actions?
- **Exec filesystem drift**: are mutating filesystem tools denied while `exec`/`process` remain available without sandbox filesystem constraints?
- **Exec approval drift** (`security=full`, `autoAllowSkills`, interpreter allowlists without `strictInlineEval`): are host-exec guardrails still doing what you think they are? Note `security="full"` is a broad posture warning, not proof of a bug — it is the chosen default for trusted personal-assistant setups, and you tighten it only when your threat model needs approval or allowlist guardrails.
- **Network exposure** (Gateway bind/auth, Tailscale Serve/Funnel, weak/short auth tokens).
- **Browser control exposure** (remote nodes, relay ports, remote CDP endpoints).
- **Local disk hygiene** (permissions, symlinks, config includes, "synced folder" paths).
- **Plugins** (plugins load without an explicit allowlist).
- **Policy drift/misconfig**: sandbox docker settings configured but sandbox mode off; ineffective `gateway.nodes.denyCommands` patterns (matching is exact command-name only, e.g. `system.run`, and does not inspect shell text); dangerous `gateway.nodes.allowCommands` entries; global `tools.profile="minimal"` overridden by per-agent profiles; plugin-owned tools reachable under permissive tool policy.
- **Runtime expectation drift**: e.g. assuming implicit exec still means `sandbox` when `tools.exec.host` now defaults to `auto`, or explicitly setting `tools.exec.host="sandbox"` while sandbox mode is off.
- **Model hygiene**: warns when configured models look legacy (not a hard block).

If you run `--deep`, OpenClaw also attempts a best-effort live Gateway probe.

## Security audit checklist (priority order)

When the audit prints findings, treat this as a priority order for remediation:

1. **Anything "open" + tools enabled**: lock down DMs/groups first (pairing/allowlists), then tighten tool policy/sandboxing.
2. **Public network exposure** (LAN bind, Funnel, missing auth): fix immediately.
3. **Browser control remote exposure**: treat it like operator access (tailnet-only, pair nodes deliberately, avoid public exposure).
4. **Permissions**: make sure state/config/credentials/auth are not group/world-readable.
5. **Plugins**: only load what you explicitly trust.
6. **Model choice**: prefer modern, instruction-hardened models for any bot with tools.

## Security audit glossary (`checkId` classes)

Each audit finding is keyed by a structured `checkId` (for example `gateway.bind_no_auth` or `tools.exec.security_full_configured`). Common critical severity classes are:

- `fs.*` — filesystem permissions on state, config, credentials, auth profiles.
- `gateway.*` — bind mode, auth, Tailscale, Control UI, trusted-proxy setup.
- `hooks.*`, `browser.*`, `sandbox.*`, `tools.exec.*` — per-surface hardening.
- `plugins.*`, `skills.*` — plugin/skill supply chain and scan findings.
- `security.exposure.*` — cross-cutting checks where access policy meets tool blast radius.

The full catalog — with severity levels, fix keys, and auto-fix support — is captured as **[OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md)** (source page `gateway/security/audit-checks`).

## Insecure or dangerous flags summary

`openclaw security audit` raises `config.insecure_or_dangerous_flags` when known insecure/dangerous debug switches are enabled. Keep these unset in production. Each enabled flag is reported as its own finding. If audit suppressions are configured, `security.audit.suppressions.active` remains in the active audit output even when matching findings move to `suppressedFindings`.

**Flags tracked by the audit today:**

- `gateway.controlUi.allowInsecureAuth=true`
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true`
- `gateway.controlUi.dangerouslyDisableDeviceAuth=true`
- `security.audit.suppressions configured (<count>)`
- `hooks.gmail.allowUnsafeExternalContent=true`
- `hooks.mappings[<index>].allowUnsafeExternalContent=true`
- `tools.exec.applyPatch.workspaceOnly=false`
- `plugins.entries.acpx.config.permissionMode=approve-all`

**All `dangerous*` / `dangerously*` keys in the config schema** (broader than the tracked-today list above) span: Control UI and browser (`gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback`, `gateway.controlUi.dangerouslyDisableDeviceAuth`, `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`); channel name-matching for bundled and plugin channels and per-`accounts.<accountId>` where applicable (`channels.discord.dangerouslyAllowNameMatching`, `channels.slack.dangerouslyAllowNameMatching`, `channels.googlechat.dangerouslyAllowNameMatching`, `channels.msteams.dangerouslyAllowNameMatching`, the plugin channels `channels.synology-chat.dangerouslyAllowNameMatching`, `channels.synology-chat.dangerouslyAllowInheritedWebhookPath`, `channels.zalouser.dangerouslyAllowNameMatching`, `channels.irc.dangerouslyAllowNameMatching`, `channels.mattermost.dangerouslyAllowNameMatching`); network exposure (`channels.telegram.network.dangerouslyAllowPrivateNetwork`, also per account); and sandbox Docker defaults + per-agent (`agents.defaults.sandbox.docker.dangerouslyAllowReservedContainerTargets`, `agents.defaults.sandbox.docker.dangerouslyAllowExternalBindSources`, `agents.defaults.sandbox.docker.dangerouslyAllowContainerNamespaceJoin`).

**Source**: OpenClaw documentation — `gateway/security` (audit sections) (mirror `inbox/openclaw_docs/gateway/security.md`)
**Last Updated**: 2026-06-22
**Status**: Active
