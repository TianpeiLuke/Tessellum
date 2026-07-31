---
tags:
  - resource
  - documentation
  - claude_code
  - admin
  - managed_settings
keywords:
  - server-managed settings
  - endpoint-managed settings
  - claude.ai admin console
  - settings precedence
  - fail-closed startup
  - security approval dialog
  - audit logging
  - managed policy delivery
topics:
  - Claude Code
  - Admin
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/server-managed-settings
access_control_group: ["general"]
---

# Claude Code — Server-Managed Settings

## Overview

Server-managed settings let an administrator centrally configure Claude Code for an organization through a web interface on Claude.ai, **without requiring device-management infrastructure**. Claude Code clients automatically receive the settings when users authenticate with their organization credentials, making this approach the choice for organizations that lack an MDM, or that need to manage settings for users on unmanaged devices.

This note is the procedure for delivering managed policy from the admin console: the requirements, the server-vs-endpoint choice, how to configure and verify the JSON, the precedence and fetch/caching model, fail-closed startup, security-approval dialogs, platform availability, audit logging, and the client-side-control caveats. Server-managed settings are available for Claude for Teams and Claude for Enterprise customers.

## Requirements

To use server-managed settings, you need:

- Claude for Teams or Claude for Enterprise plan
- Claude Code version 2.1.38 or later for Claude for Teams, or version 2.1.30 or later for Claude for Enterprise
- Network access to `api.anthropic.com`

## Choose Between Server-Managed and Endpoint-Managed Settings

Claude Code supports two approaches for centralized configuration. Server-managed settings deliver configuration from Anthropic's servers at authentication time; [endpoint-managed settings](https://code.claude.com/docs/en/settings) are deployed directly to devices through native OS policies (macOS managed preferences, Windows registry) or managed settings files.

| Approach | Best for | Security model |
| :--- | :--- | :--- |
| **Server-managed settings** | Organizations without MDM, or users on unmanaged devices | Settings delivered from Anthropic's servers at authentication time |
| **Endpoint-managed settings** | Organizations with MDM or endpoint management | Settings deployed to devices via MDM configuration profiles, registry policies, or managed settings files |

If devices are enrolled in an MDM or endpoint-management solution, endpoint-managed settings provide **stronger security guarantees** because the settings file can be protected from user modification at the OS level.

## Configure Server-Managed Settings

1. **Open the admin console** — in Claude.ai, navigate to **Admin Settings > Claude Code > Managed settings**.
2. **Define your settings** — add configuration as JSON. All settings available in `settings.json` are supported except those restricted to OS-level policy delivery (see Current limitations). This includes hooks, environment variables, and managed-only settings like `allowManagedPermissionRulesOnly`.
3. **Save and deploy** — clients receive the updated settings on their next startup or hourly polling cycle.

This example enforces a permission deny list, prevents users from bypassing permissions, and restricts permission rules to those defined in managed settings:

```json theme={null}
{
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "disableBypassPermissionsMode": "disable"
  },
  "allowManagedPermissionRulesOnly": true
}
```

Hooks use the same format as in `settings.json`. This example runs an audit script after every file edit across the organization:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
        ]
      }
    ]
  }
}
```

To configure the auto-mode classifier so it knows which repos, buckets, and domains your organization trusts, deliver an `autoMode.environment` array (e.g., source-control hosts, trusted cloud buckets, and trusted internal domains). Because hooks execute shell commands, users see a [security approval dialog](#security-approval-dialogs) before they're applied.

### Verify Settings Delivery

To confirm settings are being applied, ask a user to restart Claude Code. If the configuration includes settings that trigger the security approval dialog, the user sees a prompt describing the managed settings on startup. You can also verify that managed permission rules are active by having a user run `/permissions` to view their effective permission rules.

### Access Control

The roles that can manage server-managed settings are **Primary Owner** and **Owner**. Restrict access to trusted personnel, since settings changes apply to all users in the organization.

### Managed-Only Settings

Most settings keys work in any scope. A handful of keys are **only read from managed settings** and have no effect in user or project settings files (see [managed-only settings](https://code.claude.com/docs/en/permissions) for the full list). Any setting not on that list can still be placed in managed settings and takes the highest precedence.

### Current Limitations

- Settings apply **uniformly to all users** in the organization — per-group configurations are not yet supported.
- A `managed-mcp.json` file cannot be distributed through server-managed settings. Deliver the `allowedMcpServers` and `deniedMcpServers` policy keys instead.
- Settings restricted to OS-level policy sources, such as `policyHelper` and `wslInheritsWindowsSettings`, are not honored. Deploy them through MDM or a system `managed-settings.json` file instead.

## Settings Delivery

### Settings Precedence

Server-managed and endpoint-managed settings both occupy the **highest tier** in the Claude Code [settings hierarchy](https://code.claude.com/docs/en/settings). No other settings level can override them, **including command-line arguments**. Within the managed tier, the first source that delivers a non-empty configuration wins: server-managed settings are checked first, then endpoint-managed. **Sources do not merge** — if server-managed settings deliver any keys at all, endpoint-managed settings are ignored entirely; if server-managed settings deliver nothing, endpoint-managed settings apply.

If you clear server-managed configuration in the admin console intending to fall back to an endpoint-managed plist or registry policy, note that cached settings persist on client machines until the next successful fetch. Run `/status` to see which managed source is active.

### Fetch and Caching Behavior

Claude Code fetches settings from Anthropic's servers at startup and polls for updates hourly during active sessions.

- **First launch without cached settings**: fetch happens asynchronously; if it fails, Claude Code continues without managed settings; there is a brief window before settings load where restrictions are not yet enforced.
- **Subsequent launches with cached settings**: cached settings apply immediately at startup, fresh settings are fetched in the background, and cached settings persist through network failures.

Settings updates apply automatically without a restart, except advanced settings like OpenTelemetry configuration, which require a full restart.

### Invalid Entries in Delivered Settings

Delivered payloads parse tolerantly with the same rules as the other managed sources. When a payload contains an entry that fails schema validation, Claude Code strips that entry, surfaces a validation error, and applies every remaining valid setting (requires Claude Code v2.1.169 or later). Server-managed delivery adds these behaviors:

- The cache at `~/.claude/remote-settings.json` stores the salvaged payload with invalid entries removed; the raw invalid payload is never persisted.
- When no field can be salvaged, Claude Code keeps the last-accepted cached settings and records a fatal error.
- The security approval dialog evaluates the salvaged payload, so a stripped invalid entry is never presented for approval and never executes.

To debug delivery issues, run `claude --debug-file <path>` and search the log for `Remote settings`. Validate a payload change with `claude doctor` on a test machine before rolling it out to the organization.

### Enforce Fail-Closed Startup

By default, if the remote-settings fetch fails at startup, the CLI continues without managed settings. For environments where this brief unenforced window is unacceptable, set `forceRemoteSettingsRefresh: true`:

```json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

When active, the CLI blocks at startup until remote settings are freshly fetched; if the fetch fails, the CLI **exits** rather than proceeding without policy. The setting self-perpetuates: once delivered from the server it is cached locally so subsequent startups enforce the same behavior even before the first successful fetch of a new session. Before enabling it, ensure network policies allow connectivity to `api.anthropic.com` — if that endpoint is unreachable, the CLI exits at startup and users cannot start Claude Code. As of v2.1.139, the `claude auth` subcommands such as `claude auth login` are exempt from this check, so users can re-authenticate when expired credentials are the reason the fetch fails.

### Security Approval Dialogs

Certain settings that could pose security risks require explicit user approval before being applied:

- **Shell command settings**: settings that execute shell commands
- **Custom environment variables**: variables not in the known-safe allowlist
- **Hook configurations**: any hook definition

When these settings are present, users see a security dialog explaining what is being configured and must approve to proceed. If a user rejects the settings, Claude Code exits. In non-interactive mode with the `-p` flag, Claude Code **skips** security dialogs and applies settings without user approval.

## Platform Availability

Server-managed settings require a direct connection to `api.anthropic.com` and are **not available** when using third-party model providers:

- Amazon Bedrock
- Google Vertex AI
- Microsoft Foundry
- Custom API endpoints via `ANTHROPIC_BASE_URL` or LLM gateways

## Audit Logging

Audit log events for settings changes are available through the compliance API or audit log export — contact your Anthropic account team for access. Audit events include the type of action performed, the account and device that performed the action, and references to the previous and new values.

## Security Considerations

Server-managed settings provide centralized policy enforcement but operate as a **client-side control**. On unmanaged devices, users with admin or sudo access can modify the Claude Code binary, filesystem, or network configuration.

| Scenario | Behavior |
| :--- | :--- |
| User edits the cached settings file | Tampered file applies at startup, but correct settings restore on the next server fetch |
| User deletes the cached settings file | First-launch behavior occurs: settings fetch asynchronously with a brief unenforced window |
| API is unavailable | Cached settings apply if available, otherwise managed settings are not enforced until the next successful fetch. With `forceRemoteSettingsRefresh: true`, the CLI exits instead of continuing, except for `claude auth` subcommands |
| User authenticates with a different organization | Settings are not delivered for accounts outside the managed organization |
| User configures a third-party model provider | Server-managed settings are bypassed. This includes setting `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_MANTLE`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY`, or a non-default `ANTHROPIC_BASE_URL` |

To detect runtime configuration changes, use `ConfigChange` hooks to log modifications or block unauthorized changes before they take effect. For stronger enforcement guarantees, use endpoint-managed settings on devices enrolled in an MDM solution.

**Source**: https://code.claude.com/docs/en/server-managed-settings
**Last Updated**: 2026-06-13
**Status**: Active
