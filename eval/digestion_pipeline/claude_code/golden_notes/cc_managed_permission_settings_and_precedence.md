---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - managed_settings
keywords:
  - managed settings
  - policy settings
  - settings precedence
  - managed-only settings
  - deny wins
  - allowManagedPermissionRulesOnly
  - disableBypassPermissionsMode
  - permissions and sandboxing
  - defense in depth
  - autoAllowBashIfSandboxed
topics:
  - Claude Code
  - Permissions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/permissions
access_control_group: ["general"]
---

# Managed Permission Settings & Precedence

## Overview

For organizations that need centralized control, administrators can deploy **managed settings** — policy settings that cannot be overridden by user or project settings. They follow the same format as regular settings files and are delivered through MDM/OS-level policies, managed settings files, or server-managed settings. A subset of keys are **managed-only**: they are read solely from managed settings and have no effect in user or project files.

Permission rules follow Claude Code's standard **settings precedence** — a five-level hierarchy where managed settings win and deny wins at any level: if a tool is denied at any level, no other level can allow it. Managed settings and permission rules are also one half of a **defense-in-depth** pairing with sandboxing: permissions decide what Claude attempts, sandboxing provides OS-level enforcement on the Bash tool. This note digests the permissions page's "How permissions interact with sandboxing", "Managed settings" (and Managed-only settings), "Settings precedence", and "Example configurations" sections.

## How permissions interact with sandboxing

Permissions and [sandboxing](https://code.claude.com/docs/en/sandboxing) are complementary security layers:

- **Permissions** control which tools Claude Code can use and which files or domains it can access. They apply to all tools (Bash, Read, Edit, WebFetch, MCP, and others).
- **Sandboxing** provides OS-level enforcement that restricts the Bash tool's filesystem and network access. It applies only to Bash commands and their child processes.

Use both for defense-in-depth:

- Permission deny rules block Claude from even attempting to access restricted resources.
- Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude's decision-making.
- Filesystem restrictions in the sandbox combine the `sandbox.filesystem` settings with Read and Edit deny rules; both are merged into the final sandbox boundary.
- Network restrictions combine WebFetch permission rules with the sandbox's `allowedDomains` and `deniedDomains` lists.

When sandboxing is enabled with `autoAllowBashIfSandboxed: true` (the default), sandboxed Bash commands run without prompting even if your permissions include a bare `Bash` ask rule, or the equivalent `Bash(*)` form: the sandbox boundary substitutes for that whole-tool prompt. Content-scoped ask rules like `Bash(git push *)` still force a prompt, explicit deny rules still apply, and `rm` or `rmdir` commands that target `/`, your home directory, or other critical system paths still trigger a prompt. Commands that won't run sandboxed, such as excluded commands, respect the bare `Bash` ask rule as usual. The sandbox-mode mechanics that change this behavior are documented on the [sandboxing](https://code.claude.com/docs/en/sandboxing) page.

## Managed settings

Administrators deploy managed (policy) settings that cannot be overridden by user or project settings. These policy settings follow the same format as regular settings files and can be delivered through:

- MDM/OS-level policies,
- managed settings files, or
- [server-managed settings](https://code.claude.com/docs/en/server-managed-settings).

The [settings files](https://code.claude.com/docs/en/settings) reference documents the delivery mechanisms and file locations.

### Managed-only settings

The following settings are **only read from managed settings**. Placing them in user or project settings files has no effect.

| Setting | Description |
| :--- | :--- |
| `allowAllClaudeAiMcps` | When `true`, claude.ai connectors load alongside a deployed `managed-mcp.json` instead of being suppressed by its exclusive control. |
| `allowedChannelPlugins` | Allowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Requires `channelsEnabled: true`. |
| `allowManagedHooksOnly` | When `true`, only managed hooks, SDK hooks, and hooks from plugins force-enabled in managed settings `enabledPlugins` are loaded. User, project, and all other plugin hooks are blocked. |
| `allowManagedMcpServersOnly` | When `true`, only `allowedMcpServers` from managed settings are respected. `deniedMcpServers` still merges from all sources. |
| `allowManagedPermissionRulesOnly` | When `true`, prevents user and project settings from defining `allow`, `ask`, or `deny` permission rules. Only rules in managed settings apply. Does not affect the MCP server allowlist; for that, set `allowManagedMcpServersOnly`. |
| `blockedMarketplaces` | Blocklist of marketplace sources. Blocked sources are checked before downloading, so they never touch the filesystem. |
| `channelsEnabled` | Allow channels for the organization. |
| `forceRemoteSettingsRefresh` | When `true`, blocks CLI startup until remote managed settings are freshly fetched and exits if the fetch fails (fail-closed enforcement). |
| `pluginTrustMessage` | Custom message appended to the plugin trust warning shown before installation. |
| `sandbox.filesystem.allowManagedReadPathsOnly` | When `true`, only `filesystem.allowRead` paths from managed settings are respected. `denyRead` still merges from all sources. |
| `sandbox.network.allowManagedDomainsOnly` | When `true`, only `allowedDomains` and `WebFetch(domain:...)` allow rules from managed settings are respected. Non-allowed domains are blocked automatically without prompting the user. Denied domains still merge from all sources. |
| `strictKnownMarketplaces` | Controls which plugin marketplace sources users can add and install plugins from. |
| `strictPluginOnlyCustomization` | Block skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings. `true` locks all four surfaces; an array such as `["skills", "hooks"]` locks only the named ones. |
| `wslInheritsWindowsSettings` | When `true` in the Windows HKLM registry key or `C:\Program Files\ClaudeCode\managed-settings.json`, WSL reads managed settings from the Windows policy chain in addition to `/etc/claude-code`. |

`disableBypassPermissionsMode` is typically placed in managed settings to enforce organizational policy, but it works from any scope. A user can set it in their own settings to lock themselves out of bypass mode. (Its companion `disableAutoMode` likewise disables [auto mode](cc_auto_mode.md) and is most useful in managed settings where it cannot be overridden.)

On Team and Enterprise plans, an admin enables or disables Remote Control and web sessions organization-wide in Claude Code admin settings. Remote Control can additionally be disabled per device with the `disableRemoteControl` managed setting; web sessions have no per-device managed settings key.

## Settings precedence

Permission rules follow the same [settings precedence](https://code.claude.com/docs/en/settings) as all other Claude Code settings:

1. **Managed settings**: cannot be overridden by any other level, including command line arguments
2. **Command line arguments**: temporary session overrides
3. **Local project settings** (`.claude/settings.local.json`)
4. **Shared project settings** (`.claude/settings.json`)
5. **User settings** (`~/.claude/settings.json`)

**Deny wins at any level.** If a tool is denied at any level, no other level can allow it. For example, a managed settings deny cannot be overridden by `--allowedTools`, and `--disallowedTools` can add restrictions beyond what managed settings define. If user settings allow a permission and project settings deny it, the deny rule blocks it; the reverse is also true — a user-level deny blocks a project-level allow, because deny rules from any scope are evaluated before allow rules.

Embedding hosts can supply additional managed policy via the SDK `managedSettings` option when `parentSettingsBehavior` is set to `"merge"`; embedder values can tighten policy but not loosen it.

## Example configurations

The [anthropics/claude-code examples repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) includes starter settings configurations for common deployment scenarios. Use these as starting points and adjust them to fit your needs.

**Source**: https://code.claude.com/docs/en/permissions
**Last Updated**: 2026-06-13
**Status**: Active
