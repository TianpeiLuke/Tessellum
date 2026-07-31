---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - plugin_policy
keywords:
  - strictknownmarketplaces
  - strictpluginonlycustomization
  - blockedmarketplaces
  - managed settings only
  - marketplace allowlist
  - plugin-only customization
  - exact source matching
  - customization supply chain
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

# Claude Code — Managed Plugin & Marketplace Policy Settings

## Overview

Three plugin-related `settings.json` keys are **managed-settings-only** governance controls that an organization deploys to lock down the plugin supply chain: `strictKnownMarketplaces` (an allowlist of marketplace sources users may add), `blockedMarketplaces` (a blocklist of sources), and `strictPluginOnlyCustomization` (a surface lockdown forcing skills/agents/hooks/MCP to come only from plugins or managed settings). All three can only be set in `managed-settings.json`, sit at the highest precedence, and cannot be overridden by user or project settings. This note covers their procedural mechanics — source-type matching rules, allowlist/blocklist semantics, and how they combine to control the full customization supply chain. User-facing marketplace documentation lives in [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces); the related but user-configurable `enabledPlugins` and `extraKnownMarketplaces` keys are covered in [cc_subagent_and_plugin_settings.md](cc_subagent_and_plugin_settings.md).

## `strictKnownMarketplaces` — marketplace allowlist

**Managed settings only.** Controls which plugin marketplaces users are allowed to add and install plugins from, giving administrators strict control over marketplace sources. Configurable only in `managed-settings.json` at the standard managed locations:

- **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
- **Linux and WSL**: `/etc/claude-code/managed-settings.json`
- **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

### Key characteristics

- Only available in managed settings (`managed-settings.json`).
- Cannot be overridden by user or project settings (highest precedence).
- Enforced **BEFORE** network/filesystem operations — blocked sources never execute.
- Uses **exact matching** for source specifications (including `ref`, `path` for git sources), except `hostPattern` and `pathPattern`, which use regex matching.

### Allowlist behavior

- `undefined` (default): No restrictions — users can add any marketplace.
- Empty array `[]`: Complete lockdown — users cannot add any new marketplaces.
- List of sources: Users can only add marketplaces that match exactly.

### Supported source types

The allowlist supports multiple marketplace source types. Most use exact matching; `hostPattern` and `pathPattern` use regex matching against the marketplace host and filesystem path respectively:

| Source type | Required field | Optional fields | Matching |
|---|---|---|---|
| `github` | `repo` | `ref` (branch/tag/SHA), `path` (subdirectory) | exact |
| `git` | `url` | `ref`, `path` | exact |
| `url` | `url` | `headers` (HTTP headers for authenticated access) | exact |
| `npm` | `package` (supports scoped packages) | — | exact |
| `file` | `path` (absolute path to `marketplace.json`) | — | exact |
| `directory` | `path` (absolute path to dir containing `.claude-plugin/marketplace.json`) | — | exact |
| `hostPattern` | `hostPattern` (regex against marketplace host) | — | regex |
| `pathPattern` | `pathPattern` (regex against `file`/`directory` `path`) | — | regex |

Host extraction for `hostPattern`: `github` always matches against `github.com`; `git` and `url` extract the hostname from the URL (git supports HTTPS and SSH formats); `npm`, `file`, and `directory` are not supported for host-pattern matching. Use `hostPattern` to allow all marketplaces from a specific host (e.g. an internal GitHub Enterprise or GitLab server) without enumerating each repository, and `pathPattern` to allow filesystem-based marketplaces (set `".*"` to allow all local paths).

### Exact matching requirements

For git-based sources (`github` and `git`), a user's addition is allowed only if the source matches **exactly**, including all optional fields: the `repo` or `url` must match exactly, the `ref` field must match exactly (or both be undefined), and the `path` field must match exactly (or both be undefined). Sources that differ only by `ref` or `path` are treated as DIFFERENT and will not match.

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" },
    { "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" },
    { "source": "url", "url": "https://plugins.example.com/marketplace.json" },
    { "source": "npm", "package": "@acme-corp/compliance-plugins" }
  ]
}
```

### Comparison with `extraKnownMarketplaces`

`strictKnownMarketplaces` is a **policy gate**: it controls what users may add but does not register any marketplaces. `extraKnownMarketplaces` (covered in [cc_subagent_and_plugin_settings.md](cc_subagent_and_plugin_settings.md)) is a team-convenience auto-installer. They differ across these axes:

| Aspect | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
|---|---|---|
| Purpose | Organizational policy enforcement | Team convenience |
| Settings file | `managed-settings.json` only | Any settings file |
| Behavior | Blocks non-allowlisted additions | Auto-installs missing marketplaces |
| When enforced | Before network/filesystem operations | After user trust prompt |
| Can be overridden | No (highest precedence) | Yes (by higher precedence settings) |
| Source format | Direct source object | Named marketplace with nested source |
| Use case | Compliance, security restrictions | Onboarding, standardization |

`strictKnownMarketplaces` uses **direct source objects** (`[{ "source": "github", "repo": "..." }]`), whereas `extraKnownMarketplaces` requires **named marketplaces** with a nested source. To both restrict and pre-register a marketplace for all users, set both in `managed-settings.json`. With only `strictKnownMarketplaces` set, users can still add the allowed marketplace manually via `/plugin marketplace add`, but it is not available automatically.

### Enforcement notes

- Restrictions are checked BEFORE any network requests or filesystem operations.
- When blocked, users see clear error messages indicating the source is blocked by managed policy.
- The restriction is enforced on marketplace add and on plugin install, update, refresh, and auto-update. A marketplace added before the policy was set cannot be used to install or update plugins once its source no longer matches the allowlist.
- Managed settings have the highest precedence and cannot be overridden.

## `blockedMarketplaces` — marketplace blocklist

**Managed settings only.** A blocklist of marketplace sources (the inverse of the `strictKnownMarketplaces` allowlist). Enforced on marketplace add and on plugin install, update, refresh, and auto-update, so a marketplace added before the policy was set cannot be used to fetch plugins. Blocked sources are checked before downloading, so they never touch the filesystem. Example: `[{ "source": "github", "repo": "untrusted/plugins" }]`.

## `strictPluginOnlyCustomization` — surface lockdown

**Managed settings only.** Blocks skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings. Combine it with `strictKnownMarketplaces` to control the **full customization supply chain**: the marketplace allowlist controls which plugins users can install, and this setting blocks everything that doesn't come from a plugin or from managed settings.

> Requires Claude Code v2.1.82 or later. Earlier versions ignore the key and keep loading user and project customizations, so the lockdown isn't enforced until clients update.

The value is either `true` to lock all four surfaces, or an array naming the surfaces to lock:

```json
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}
```

For each locked surface, Claude Code skips user-level and project-level sources and loads only plugin-provided and managed sources:

| Surface | Blocked when locked | Still loads |
|---|---|---|
| `skills` | `~/.claude/skills/`, `.claude/skills/` | Plugin skills, bundled skills, skills in the managed policy directory |
| `agents` | `~/.claude/agents/`, `.claude/agents/` | Plugin agents, built-in agents, agents in the managed policy directory |
| `hooks` | Hooks in user, project, and local `settings.json` | Plugin hooks, hooks in managed settings |
| `mcp` | Servers in `~/.claude.json` and `.mcp.json` | Plugin MCP servers, [`managed-mcp.json`](https://code.claude.com/docs/en/managed-mcp) servers |

Surface names that a Claude Code version doesn't recognize are ignored rather than failing the settings file, so you can add new surface names before all clients have updated.

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
