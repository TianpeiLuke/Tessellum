---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - policy
keywords:
  - openclaw policy check
  - policy compare baseline
  - policy watch drift
  - attestation hash audit tuple
  - policy findings catalog
  - finding target requirement
  - evidence json oc path
  - attestationHash findingsHash workspace hash
topics:
  - OpenClaw
  - Policy Attestation
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/cli/policy
access_control_group: ["general"]
---

# OpenClaw — Policy Evidence, Findings, and the Attestation Tuple

## Overview

This note models the **evidence/attestation contract** of `openclaw policy`: how the policy plugin observes the active workspace, emits findings, and produces a stable, tamper-evident attestation that an operator or supervisor records as audit evidence. It mirrors the `policy check` / `policy compare` / `policy watch` commands, the "Accept policy state" lifecycle and JSON shape, and the full Findings catalog (check-id table, the `target`/`requirement` finding model, and per-domain finding examples) from the `cli/policy` source page. The rule reference itself (what each policy field means) is the model half captured in the sibling [oc_cli_policy_model](oc_cli_policy_model.md); turning policy on and hash-locking it is the procedure in [oc_cli_policy_configure](oc_cli_policy_configure.md).

## Commands: check / compare / watch

Three read-only verbs produce or evaluate the attestation. `policy check` runs only the policy check set and emits evidence, findings, and attestation hashes; the same findings also appear in `openclaw doctor --lint` when the Policy plugin is enabled. It accepts `--json` and a `--severity-min` threshold:

```bash
openclaw policy check
openclaw policy check --json
openclaw policy check --severity-min error
```

`policy compare` compares **policy file syntax to policy file syntax** against an authored baseline. It does **not** inspect OpenClaw runtime state, evidence, credentials, or secrets. It uses the same policy rule metadata that governs scoped overlays: allowlists must stay equal or narrower, denylists must stay equal or broader, required booleans must keep their required value, ordered strings must move only toward the more restrictive end of the configured order, and exact lists must match. The baseline file can be an organization-authored policy; the checked policy can use stricter values or add extra rules. A top-level checked rule can satisfy a scoped baseline rule when it is equally or more restrictive, because top-level policy applies broadly. Scope names do not need to match — scoped comparison is keyed by selector value (`agentIds` or `channelIds`) and by the policy field being checked.

```bash
openclaw policy compare --baseline official.policy.jsonc
openclaw policy compare --baseline official.policy.jsonc --policy policy.jsonc --json
```

A clean `policy compare --json` output reports only policy-file comparison state (no evidence): `{ "ok": true, "baselinePath": "official.policy.jsonc", "policyPath": "policy.jsonc", "rulesChecked": 3, "findings": [] }`.

`policy watch` runs the same check repeatedly and reports when the current evidence no longer matches `expectedAttestationHash`. Use `--once` in CI or scripts that need a single drift evaluation; without `--once` the command polls every two seconds by default, and `--interval-ms` selects a different interval:

```bash
openclaw policy watch --json
```

## The Attestation Tuple

A clean `policy check --json` emits stable hashes that an operator or supervisor can record. The attestation object carries four parts plus a timestamp:

```json
{
  "ok": true,
  "attestation": {
    "checkedAt": "2026-05-10T20:00:00.000Z",
    "policy": { "path": "policy.jsonc", "hash": "sha256:..." },
    "workspace": { "scope": "policy", "hash": "sha256:..." },
    "findingsHash": "sha256:...",
    "attestationHash": "sha256:..."
  },
  "checksRun": 30,
  "checksSkipped": 0,
  "findings": []
}
```

The **policy hash** identifies the authored rule artifact. The **evidence block** records the observed OpenClaw state used by the checks, and `workspace.hash` identifies that evidence payload for the checked scope. The **findings hash** identifies the exact finding set returned. `checkedAt` records when the evaluation ran. The **attestation hash** identifies the stable claim — policy hash, evidence hash, findings hash, and whether the result was clean. It intentionally does **not** include `checkedAt`, so the same policy state produces the same attestation across repeated checks. Together, these form the **audit tuple** for this policy check. If a later gateway or supervisor uses policy to block, approve, or annotate a runtime action, it should record the attestation hash from the last clean policy check; `checkedAt` stays in JSON output for audit logs but is not part of the stable attestation hash.

### Evidence payload

The evidence block records observed config-level posture across the governed domains — never raw secret values. Each evidence row carries an `oc://` `source` address (see sibling [oc_cli_path_addressing](oc_cli_path_addressing.md)). The recorded domains include `channels`, `mcpServers`, `modelProviders`, `modelRefs`, `network`, `gatewayExposure`, `agentWorkspace` (with `workspaceAccess` and `toolDeny` kinds), `secrets` (provider `providerSource` and SecretRef `provenance`/`refSource`/`refProvider`, never raw secrets), `authProfiles` (`validMetadata`, `provider`, `mode`), and `tools` (`risk`, `sensitivity`, `capabilities`, sourced from `oc://TOOLS.md/...`). A representative secret evidence row:

```json
{
  "id": "oc://openclaw.config/models/providers/openai/apiKey",
  "kind": "input",
  "source": "oc://openclaw.config/models/providers/openai/apiKey",
  "provenance": "secretRef",
  "refSource": "env",
  "refProvider": "vault"
}
```

### Accept-state lifecycle

The documented lifecycle for accepting policy state:

1. Author or review `policy.jsonc`.
2. Run `openclaw policy check --json`.
3. If the result is clean, record `attestation.policy.hash` as `expectedHash`.
4. Record `attestation.attestationHash` as `expectedAttestationHash`.
5. Re-run `openclaw doctor --lint` in CI or release gates.

If policy rules change intentionally, update both accepted hashes from a clean check. If workspace settings change intentionally but policy stays the same, only `expectedAttestationHash` usually changes. Enabling or upgrading `agents.workspace` rules adds `agentWorkspace` evidence to the workspace hash and attestation hash; operators should review the new evidence and refresh accepted attestation hashes after enabling these rules. Enabling or upgrading tool posture rules adds `toolPosture` evidence the same way. (Recording these hashes into config is the procedure in [oc_cli_policy_configure](oc_cli_policy_configure.md).)

## Findings Catalog

Each check emits a finding when observed config does not conform to a present rule. The full catalog of check ids, grouped by domain:

| Domain | Check ids |
| --- | --- |
| Policy artifact | `policy/policy-jsonc-missing`, `policy/policy-jsonc-invalid`, `policy/policy-hash-mismatch`, `policy/attestation-hash-mismatch` |
| Conformance compare | `policy/policy-conformance-invalid`, `policy/policy-conformance-missing`, `policy/policy-conformance-weaker` |
| Channels | `policy/channels-denied-provider` |
| MCP servers | `policy/mcp-denied-server`, `policy/mcp-unapproved-server` |
| Model providers | `policy/models-denied-provider`, `policy/models-unapproved-provider` |
| Network | `policy/network-private-access-enabled` |
| Ingress | `policy/ingress-dm-policy-unapproved`, `policy/ingress-dm-scope-unapproved`, `policy/ingress-open-groups-denied`, `policy/ingress-group-mention-required` |
| Gateway | `policy/gateway-non-loopback-bind`, `policy/gateway-auth-disabled`, `policy/gateway-rate-limit-missing`, `policy/gateway-control-ui-insecure`, `policy/gateway-tailscale-funnel`, `policy/gateway-remote-enabled`, `policy/gateway-http-endpoint-enabled`, `policy/gateway-http-url-fetch-unrestricted` |
| Agent workspace | `policy/agents-workspace-access-denied`, `policy/agents-tool-not-denied` |
| Tool posture | `policy/tools-profile-unapproved`, `policy/tools-fs-workspace-only-required`, `policy/tools-exec-security-unapproved`, `policy/tools-exec-ask-unapproved`, `policy/tools-exec-host-unapproved`, `policy/tools-elevated-enabled`, `policy/tools-also-allow-missing`, `policy/tools-also-allow-unexpected`, `policy/tools-required-deny-missing` |
| Sandbox | `policy/sandbox-mode-unapproved`, `policy/sandbox-backend-unapproved`, `policy/sandbox-container-posture-unobservable`, `policy/sandbox-container-host-network-denied`, `policy/sandbox-container-namespace-join-denied`, `policy/sandbox-container-mount-mode-required`, `policy/sandbox-container-runtime-socket-mount`, `policy/sandbox-container-unconfined-profile`, `policy/sandbox-browser-cdp-source-range-missing` |
| Data handling | `policy/data-handling-redaction-disabled`, `policy/data-handling-telemetry-content-capture`, `policy/data-handling-session-retention-not-enforced`, `policy/data-handling-session-transcript-memory-enabled` |
| Secrets | `policy/secrets-unmanaged-provider`, `policy/secrets-denied-provider-source`, `policy/secrets-insecure-provider` |
| Auth profiles | `policy/auth-profile-invalid-metadata`, `policy/auth-profile-unapproved-mode` |
| Exec approvals | `policy/exec-approvals-missing`, `policy/exec-approvals-invalid`, `policy/exec-approvals-default-security-unapproved`, `policy/exec-approvals-agent-security-unapproved`, `policy/exec-approvals-auto-allow-skills-enabled`, `policy/exec-approvals-allowlist-missing`, `policy/exec-approvals-allowlist-unexpected` |
| Tool metadata | `policy/tools-missing-risk-level`, `policy/tools-unknown-risk-level`, `policy/tools-missing-sensitivity-token`, `policy/tools-missing-owner`, `policy/tools-unknown-sensitivity-token` |

### Finding shape: target vs requirement

Policy findings can include both `target` and `requirement`. `target` is the observed workspace thing that does not conform; `requirement` is the authored policy rule that made it a finding. Both values are addresses today, usually `oc://` paths, but the field names describe their policy role rather than the address format. A representative channels finding shows the full shape (`checkId`, `severity`, `message`, `source`, `path`, `ocPath`, `target`, `requirement`, `fixHint`):

```json
{
  "checkId": "policy/channels-denied-provider",
  "severity": "error",
  "message": "Channel 'telegram' uses denied provider 'telegram'.",
  "source": "policy",
  "path": "openclaw config",
  "ocPath": "oc://openclaw.config/channels/telegram",
  "target": "oc://openclaw.config/channels/telegram",
  "requirement": "oc://policy.jsonc/channels/denyRules/#0",
  "fixHint": "Telegram is not approved for this workspace."
}
```

Other documented per-domain examples follow the same shape with domain-specific `target`/`requirement` `oc://` addresses: a tool-metadata finding (`policy/tools-missing-risk-level`, `target: oc://TOOLS.md/tools/deploy`, `requirement: oc://policy.jsonc/tools/requireMetadata`, with a `line`); an MCP finding (`policy/mcp-unapproved-server`, `requirement: oc://policy.jsonc/mcp/servers/allow`); a model-provider finding (`policy/models-unapproved-provider`, `requirement: oc://policy.jsonc/models/providers/allow`); a network finding (`policy/network-private-access-enabled`, `requirement: oc://policy.jsonc/network/privateNetwork/allow`); a Gateway-exposure finding (`policy/gateway-non-loopback-bind`, `requirement: oc://policy.jsonc/gateway/exposure/allowNonLoopbackBind`); and an agent-workspace finding (`policy/agents-workspace-access-denied`, `requirement: oc://policy.jsonc/agents/workspace/allowedAccess`).

**Source**: OpenClaw documentation — `cli/policy` (mirror `inbox/openclaw_docs/cli/policy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
