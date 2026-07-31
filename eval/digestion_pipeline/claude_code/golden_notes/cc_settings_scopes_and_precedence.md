---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - scopes
keywords:
  - configuration scopes
  - settings precedence
  - managed user project local scope
  - array merge vs scalar override
  - fallbackmodel availablemodels exception
  - what uses scopes
  - setting sources verification
  - graduated trust precedence
topics:
  - Claude Code
  - Settings
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/settings
access_control_group: ["general"]
---

# Claude Code — Settings Scopes and Precedence

## Overview

Claude Code uses a **scope system** to determine where configurations apply and who they are shared with, so the same product can be tuned for personal use, team collaboration, or enterprise deployment. There are four scopes — **Managed**, **User**, **Project**, and **Local** — each living in a distinct location and affecting a distinct audience. When the same setting appears in more than one scope, Claude Code resolves the conflict through a fixed **precedence order** in which managed settings always win and user settings are the fallback.

A key subtlety is that not all settings resolve the same way: **scalar values** from a higher-priority scope override lower scopes, but **array-valued settings merge** (concatenate and de-duplicate) across scopes, with two named exceptions (`fallbackModel` and `availableModels`). You can confirm which layers loaded for a session by running `/status` and reading the `Setting sources` line.

## Available scopes

| Scope       | Location                                                                           | Who it affects                       | Shared with team?                           |
| :---------- | :--------------------------------------------------------------------------------- | :----------------------------------- | :------------------------------------------ |
| **Managed** | Server-managed settings, plist / registry, or system-level `managed-settings.json` | All users on the machine             | Yes (deployed by IT)                        |
| **User**    | `~/.claude/` directory                                                             | You, across all projects             | No                                          |
| **Project** | `.claude/` in repository                                                           | All collaborators on this repository | Yes (committed to git)                      |
| **Local**   | `.claude/settings.local.json`                                                      | You, in this repository only         | No (gitignored when Claude Code creates it) |

On Windows, paths shown as `~/.claude` resolve to `%USERPROFILE%\.claude`.

## When to use each scope

- **Managed scope** is for security policies that must be enforced organization-wide, compliance requirements that cannot be overridden, and standardized configurations deployed by IT/DevOps.
- **User scope** is best for personal preferences you want everywhere (themes, editor settings), tools and plugins you use across all projects, and API keys and authentication (stored securely).
- **Project scope** is best for team-shared settings (permissions, hooks, MCP servers), plugins the whole team should have, and standardizing tooling across collaborators.
- **Local scope** is best for personal overrides for a specific project, testing configurations before sharing with the team, and machine-specific settings that won't work for others.

## How scopes interact

When the same setting appears in multiple scopes, Claude Code applies them in priority order:

1. **Managed** (highest) — can't be overridden by anything
2. **Command line arguments** — temporary session overrides
3. **Local** — overrides project and user settings
4. **Project** — overrides user settings
5. **User** (lowest) — applies when nothing else specifies the setting

For example, if your user settings set `spinnerTipsEnabled` to `true` and project settings set it to `false`, the project value applies. **Permission rules behave differently because they merge across scopes rather than override.**

## Settings precedence

Settings apply in order of precedence. From highest to lowest:

1. **Managed settings** (server-managed, MDM/OS-level policies, or managed-settings files)
   - Policies deployed by IT through server delivery, MDM configuration profiles, registry policies, or managed settings files
   - Cannot be overridden by any other level, including command line arguments
   - Within the managed tier, precedence is: server-managed > MDM/OS-level policies > file-based (`managed-settings.d/*.json` + `managed-settings.json`) > HKCU registry (Windows only). Only one managed source is used; sources do not merge across tiers. Within the file-based tier, drop-in files and the base file are merged together.
   - Embedding hosts such as Claude Desktop can supply policy via the SDK `managedSettings` option. By default this is ignored when any managed-settings tier is present; administrators can opt in by setting `parentSettingsBehavior` to `"merge"`, and the embedder's values are filtered so they can tighten managed policy but not loosen it.
2. **Command line arguments** — temporary overrides for a specific session. JSON passed via `--settings <file-or-json>` merges with file-based settings using the same rules as the other layers.
3. **Local project settings** (`.claude/settings.local.json`) — personal project-specific settings.
4. **Shared project settings** (`.claude/settings.json`) — team-shared project settings in source control.
5. **User settings** (`~/.claude/settings.json`) — personal global settings.

This hierarchy ensures organizational policies are always enforced while still allowing teams and individuals to customize. The same precedence applies whether Claude Code runs from the CLI, the VS Code extension, or a JetBrains IDE.

### Array merge vs scalar override

For scalar settings, the highest-precedence scope wins (e.g. if user settings set `permissions.defaultMode` to `acceptEdits` and a project's shared settings set it to `default`, the project value applies). For arrays, the rule is different:

> **Array settings merge across scopes.** When the same array-valued setting (such as `sandbox.filesystem.allowWrite` or `permissions.allow`) appears in multiple scopes, the arrays are **concatenated and deduplicated**, not replaced. Lower-priority scopes can add entries without overriding those set by higher-priority scopes, and vice versa. For example, if managed settings set `allowWrite` to `["/opt/company-tools"]` and a user adds `["~/.kube"]`, both paths are included in the final configuration.

Two exceptions to the array-merge rule:

- **`fallbackModel`** — an ordered chain where position carries meaning, so the highest-precedence file that defines it supplies the entire value.
- **`availableModels`** (as of v2.1.175) — a managed or policy value replaces lower-precedence entries entirely.

## What uses scopes

Scopes apply to many Claude Code features, each with its own per-scope storage location:

| Feature         | User location             | Project location                   | Local location                 |
| :-------------- | :------------------------ | :--------------------------------- | :----------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json`  |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                  | None                           |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                        | `~/.claude.json` (per-project) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json`  |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` or `.claude/CLAUDE.md` | `CLAUDE.local.md`              |

## Verify active settings

Run `/status` and check the `Setting sources` line on the **Status** tab. It lists every settings layer Claude Code loaded for this session:

- If a layer such as `User settings` or `Project local settings` appears, that file is being read.
- If a layer is missing, that file was not found or contains no keys.

When managed settings are in effect, the entry shows the delivery channel in parentheses, for example `Enterprise managed settings (remote)`, `(plist)`, `(HKLM)`, `(HKCU)`, or `(file)`. If a settings file has invalid JSON or a value that fails validation, Claude Code shows a setup issues notice at startup and the **Status** tab lists the affected files; run `/doctor` for per-error details. The line confirms which files are being read, **not** which layer supplied each individual key. The **Config** tab in the same dialog edits built-in toggles such as theme and verbose output, not `settings.json` contents.

## Key points about the configuration system

- **Memory files (`CLAUDE.md`)**: contain instructions and context that Claude loads at startup.
- **Settings files (JSON)**: configure permissions, environment variables, and tool behavior.
- **Skills**: custom prompts invoked with `/skill-name` or loaded by Claude automatically.
- **MCP servers**: extend Claude Code with additional tools and integrations.
- **Precedence**: higher-level configurations (Managed) override lower-level ones (User/Project).
- **Inheritance**: settings merge across scopes; scalar values from higher-priority scopes override, and arrays concatenate. Exceptions: `fallbackModel`, where the highest-precedence scope supplies the whole chain, and `availableModels`, where a managed or policy value replaces lower-precedence entries.

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
