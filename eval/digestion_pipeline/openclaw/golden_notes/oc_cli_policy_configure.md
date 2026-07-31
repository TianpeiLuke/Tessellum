---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - policy
keywords:
  - openclaw policy configure
  - plugins.entries.policy.config
  - workspaceRepairs
  - expectedHash expectedAttestationHash
  - doctor --fix policy repair
  - policy check compare watch exit codes
  - hash-lock policy artifact
topics:
  - OpenClaw
  - Policy CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/policy
access_control_group: ["general"]
---

# OpenClaw — Configuring and Repairing `openclaw policy`

## Overview

This note is the operational procedure for turning the OpenClaw conformance layer on and keeping it pinned: the `plugins.entries.policy.config` settings block, the gated `doctor --fix` repair path controlled by `workspaceRepairs`, and the per-command exit codes for `policy check` / `policy compare` / `policy watch`. It mirrors the **Configure policy**, **Repair**, and **Exit codes** sections of the `cli/policy` source page. The companion notes cover what the rules mean (`oc_cli_policy_model`) and the evidence/attestation contract (`oc_cli_policy_attestation`); this note is strictly the configure-and-repair workflow.

## Configure policy

Policy config lives under `plugins.entries.policy.config`. The bundled Policy plugin must already be enabled (`openclaw plugins enable policy`); this block then controls how the workspace activates, locates, locks, and (optionally) repairs against the authored `policy.jsonc` artifact.

```jsonc
{
  "plugins": {
    "entries": {
      "policy": {
        "enabled": true,
        "config": {
          "enabled": true,
          "path": "policy.jsonc",
          "workspaceRepairs": false,
          "expectedHash": "sha256:...",
          "expectedAttestationHash": "sha256:...",
        },
      },
    },
  },
}
```

The five config keys, per the source's settings table:

| Setting | Purpose |
| --- | --- |
| `enabled` | Enable policy checks even before `policy.jsonc` exists. |
| `workspaceRepairs` | Allow `doctor --fix` to edit policy-managed workspace settings. |
| `expectedHash` | Optional hash-lock for the approved policy artifact. |
| `expectedAttestationHash` | Optional hash-lock for the last accepted clean policy check. |
| `path` | Workspace-relative location of the policy artifact. |

Note the two distinct `enabled` flags: the outer `plugins.entries.policy.enabled` enables the plugin entry itself, while the inner `config.enabled` enables policy checks for the workspace. Set `plugins.entries.policy.config.enabled` to `false` to disable policy checks for a workspace while leaving the plugin installed. Tool metadata requirements are NOT set here — they are authored in `policy.jsonc` with `tools.requireMetadata`, for example `["risk", "sensitivity", "owner"]`.

### Hash-locking an accepted state

`expectedHash` and `expectedAttestationHash` are optional hash-locks that pin a reviewed-and-accepted state so later drift is caught. The accept lifecycle (detailed in `oc_cli_policy_attestation`) ends by recording these two values from a clean check: author or review `policy.jsonc`, run `openclaw policy check --json`, and if the result is clean, record `attestation.policy.hash` as `expectedHash` and `attestation.attestationHash` as `expectedAttestationHash`, then re-run `openclaw doctor --lint` in CI or release gates. When policy rules change intentionally, update both accepted hashes from a new clean check; when only workspace settings change intentionally (policy unchanged), usually only `expectedAttestationHash` changes. Enabling or upgrading `agents.workspace` rules adds `agentWorkspace` evidence to the workspace and attestation hashes, and enabling or upgrading tool posture rules adds `toolPosture` evidence the same way — after enabling either, operators should review the new evidence and refresh the accepted attestation hashes.

## Repair

Both `doctor --lint` and `policy check` are read-only — they report drift but do not mutate workspace settings. Repair is the only path that can change settings, and it is gated.

`doctor --fix` only edits policy-managed workspace settings when `workspaceRepairs` is explicitly enabled. Without that opt-in, policy checks report what they would repair and leave settings unchanged. In this version, repair can disable channels that are enabled in OpenClaw config but denied by `channels.denyRules`. Because a valid deny rule can turn off a configured channel, enable `workspaceRepairs` only after the policy file has been reviewed.

```jsonc
{
  "plugins": {
    "entries": {
      "policy": {
        "config": {
          "workspaceRepairs": true,
        },
      },
    },
  },
}
```

## Exit codes

The three policy commands return process exit codes for CI and release-gate scripting. Exit `0` is the success/clean state, exit `1` is the policy/findings failure state, and exit `2` is an argument or runtime failure (not a policy verdict).

| Command | `0` | `1` | `2` |
| --- | --- | --- | --- |
| `policy check` | No findings at the threshold. | One or more findings met the threshold. | Argument or runtime failure. |
| `policy compare` | The policy file is at least as strict as the baseline. | The policy file is invalid, missing, or weaker than baseline rules. | Argument or runtime failure. |
| `policy watch` | No findings and accepted hash is current. | Findings exist or accepted attestation is stale. | Argument or runtime failure. |

**Source**: OpenClaw documentation — `cli/policy` (mirror `inbox/openclaw_docs/cli/policy.md`), Configure policy / Repair / Exit codes sections
**Last Updated**: 2026-06-22
**Status**: Active
