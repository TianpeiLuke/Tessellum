---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - managed_settings
keywords:
  - managed settings
  - managed-settings.json
  - mdm policy
  - drop-in directory merge
  - invalid managed entries
  - policy helper
  - enterprise configuration
  - fail-closed enforcement
topics:
  - Claude Code
  - Settings
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/settings
access_control_group: ["general"]
---

# Claude Code — Managed Settings

## Overview

**Managed settings** are the organization-controlled configuration tier that cannot be overridden by user or project settings. For organizations that need centralized control, Claude Code supports **multiple delivery mechanisms** for managed settings — all use the same JSON format. This note covers how managed settings are delivered (server-managed, MDM/OS-level policies, and file-based `managed-settings.json` plus the `managed-settings.d/` drop-in directory), how Claude Code parses invalid managed entries tolerantly, and the `policyHelper` executable that computes managed settings dynamically at startup.

Managed scope sits at the top of the [settings precedence ladder](cc_settings_scopes_and_precedence.md). The managed-only field *semantics* (permission, MCP, plugin, and login policies) are documented in their owning notes — this note covers the delivery, validation, and dynamic-computation procedures.

## Delivery mechanisms

All managed-settings mechanisms use the same JSON format and cannot be overridden by user or project settings:

* **Server-managed settings**: delivered from Anthropic's servers via the Claude.ai admin console. See [server-managed settings](https://code.claude.com/docs/en/server-managed-settings).
* **MDM/OS-level policies**: delivered through native device management on macOS and Windows:
  * macOS: `com.anthropic.claudecode` managed preferences domain. The plist's top-level keys mirror `managed-settings.json`, with nested settings as dictionaries and arrays as plist arrays. Deploy via configuration profiles in Jamf, Iru (Kandji), or similar MDM tools.
  * Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` registry key with a `Settings` value (REG_SZ or REG_EXPAND_SZ) containing JSON (deployed via Group Policy or Intune).
  * Windows (user-level): `HKCU\SOFTWARE\Policies\ClaudeCode` (lowest policy priority, only used when no admin-level source exists).
* **File-based**: `managed-settings.json` and `managed-mcp.json` deployed to system directories:
  * macOS: `/Library/Application Support/ClaudeCode/`
  * Linux and WSL: `/etc/claude-code/`
  * Windows: `C:\Program Files\ClaudeCode\`

The legacy Windows path `C:\ProgramData\ClaudeCode\managed-settings.json` is no longer supported as of v2.1.75; administrators who deployed there must migrate files to `C:\Program Files\ClaudeCode\managed-settings.json`.

Managed deployments can also restrict plugin marketplace additions using `strictKnownMarketplaces` (see [cc_managed_plugin_policy_settings](cc_managed_plugin_policy_settings.md)) and carry MCP allow/deny policy via [Managed MCP configuration](https://code.claude.com/docs/en/managed-mcp).

### Drop-in directory merge

File-based managed settings also support a **drop-in directory** at `managed-settings.d/` in the same system directory alongside `managed-settings.json`. This lets separate teams deploy independent policy fragments without coordinating edits to a single file.

Following the systemd convention, `managed-settings.json` is merged first as the base, then all `*.json` files in the drop-in directory are sorted alphabetically and merged on top. The merge rules:

* Later files override earlier ones for **scalar** values.
* **Arrays** are concatenated and de-duplicated.
* **Objects** are deep-merged.
* Hidden files starting with `.` are ignored.

Use numeric prefixes to control merge order, for example `10-telemetry.json` and `20-security.json`.

## Invalid entries in managed settings

Managed settings **parse tolerantly**. When a managed configuration contains an entry that fails schema validation, Claude Code strips that entry, records a warning, and enforces every remaining valid policy. A single typo cannot disable the rest of your organization's policy. This behavior is consistent across all three delivery mechanisms (server-managed, plist/registry MDM policies, and `managed-settings.json` files) and requires Claude Code v2.1.169 or later.

This tolerance applies **only** to managed settings. User, project, and local settings files remain strict: a file that fails validation is rejected as a whole and reported.

### Per-field handling of security-enforcement fields

Security-enforcement fields are handled per field instead of being stripped wholesale when they are present but invalid:

| Field | Behavior when present but invalid |
| :--- | :--- |
| `allowedMcpServers` | Enforced as an empty allowlist, so no MCP servers are admitted until the value is fixed. An individual invalid entry is stripped and the valid subset is enforced. |
| `allowManagedMcpServersOnly` | Treated as `true`. |
| `availableModels` | Enforced as an empty allowlist, so only the Default model is available until the value is fixed. An individual non-string entry is stripped and the valid subset is enforced. Applies in v2.1.175 and later. |
| `enforceAvailableModels` | Treated as `true`. Applies in v2.1.175 and later. |
| `forceLoginOrgUUID` | No organization is permitted to log in until the value is fixed. |
| `deniedMcpServers` | An individual invalid entry is stripped and the valid subset is enforced. A wholly invalid value is dropped with a warning, since denying every server would block servers the policy never named. |

`requiredMinimumVersion` and `requiredMaximumVersion` **fail open by design**: an invalid value is stripped rather than enforced, so a bad policy push cannot prevent Claude Code from starting.

### Where validation errors surface

Validation errors surface in three places:

* Interactive sessions show a dialog at startup listing the invalid entries.
* Headless runs with `-p` print a summary to stderr.
* `claude doctor` lists each invalid entry with its source and field.

Validate policy changes by running `claude doctor` on a test machine before deploying them fleet-wide.

## Compute managed settings with a policy helper

The `policyHelper` setting (requires v2.1.136 or later) points at an executable that **computes managed settings at startup**, so admins can derive policy from device posture, identity, or a remote service instead of a static file. Configure it from MDM or a system `managed-settings.json` file. Claude Code ignores `policyHelper` when it appears in any other scope, including user settings, project settings, the HKCU registry hive, and server-managed settings.

The setting accepts these keys:

| Key | Type | Description |
| :--- | :--- | :--- |
| `path` | string | Absolute path to the helper executable |
| `timeoutMs` | number | How long to wait for the helper before treating the run as failed |
| `refreshIntervalMs` | number | How often to re-run the helper in the background. Set to `0` to disable refresh, or to at least `60000` |

The helper writes a JSON envelope to stdout. Put the settings under a `managedSettings` key rather than at the top level, since a bare settings object parses with `managedSettings` undefined and applies nothing:

```json
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  },
  "claudeMd": "# Organization context\n...",
  "appendSystemPrompt": "Always cite the internal style guide."
}
```

When the helper emits `managedSettings`, that object **replaces** the file-based managed settings for the run. When the helper exits non-zero at startup, Claude Code prints the error and refuses to start, so a helper that needs outage resilience should serve from its own cache and exit `0`.

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
