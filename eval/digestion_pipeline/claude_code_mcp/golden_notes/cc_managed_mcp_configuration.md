---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - administration
keywords:
  - managed mcp configuration
  - managed-mcp.json
  - allowedmcpservers
  - deniedmcpservers
  - allowmanagedmcpserversonly
  - mcp allowlist denylist
  - disable mcp
  - enterprise mcp policy
topics:
  - Claude Code
  - MCP
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/managed-mcp
access_control_group: ["general"]
---

# Claude Code — Managed MCP Configuration

## Overview

By default any Claude Code user can connect any [MCP server](https://code.claude.com/docs/en/mcp) they choose; Anthropic reviews connectors against its listing criteria before adding them to the Anthropic Directory but does not security-audit or manage any MCP server. As an administrator you can restrict which servers run in your organization — from deploying a fixed approved set to disabling MCP entirely — using two mechanisms: a `managed-mcp.json` file that deploys a fixed set, and `allowedMcpServers`/`deniedMcpServers` settings that filter what users configure.

This note is the admin procedure for restricting MCP access. The MCP threat model and how to evaluate a server before approving it live on the [Security](https://code.claude.com/docs/en/security) page; MCP restrictions are also covered alongside the other administrative controls in [admin-setup](https://code.claude.com/docs/en/admin-setup#decide-what-to-enforce). The full MCP reference (transports, scopes, authentication) is in the sibling notes of this series, and the `mcp.md` "Managed MCP configuration" section is only a pointer here.

## Choose a pattern

Claude Code supports a range of restriction levels; each pattern uses one or both of the two mechanisms.

| Pattern | What it does | Configure |
|---|---|---|
| **Disable MCP** | No servers load anywhere | `managed-mcp.json` with an empty server map |
| **Fixed deployment** | Every user gets the same servers and can't add others | `managed-mcp.json` with the servers you want |
| **Approved catalog** | Publish approved servers; users add what they want, anything else blocked | `allowedMcpServers` + `allowManagedMcpServersOnly: true` |
| **Plugin servers only** | Servers can only come from plugins; users can't add their own | `strictPluginOnlyCustomization` with `mcp` in the list |
| **Soft allowlist** | Enforce an allowlist users can broaden in their own settings | `allowedMcpServers` without `allowManagedMcpServersOnly` |
| **Denylist only** | Block known-bad servers, allow everything else | `deniedMcpServers` |
| **No restrictions** | Users add anything | Don't deploy any managed MCP configuration |

Claude Code has no built-in MCP server registry users can browse and install from. For the approved-catalog pattern, share the list and its `claude mcp add` commands somewhere users will find them (an internal wiki), or distribute servers as plugins through a managed plugin marketplace so users can install from `/plugin`.

## Exclusive control with managed-mcp.json

If you deploy a `managed-mcp.json` file, Claude Code loads **only** the servers that file defines. Users cannot add, modify, or use any other MCP servers, including plugin-provided servers. The file also suppresses claude.ai connectors unless you explicitly allow them. Two further filters apply: `allowedMcpServers`/`deniedMcpServers` apply to managed servers too (a managed server that doesn't pass them won't load), and a user's own `deniedMcpServers` merges in so users can block a managed server for themselves.

`managed-mcp.json` is a standalone file, so it **cannot** be delivered through server-managed settings. Any process that can write to a system path with administrator privileges can deploy it — usually device-management tooling (Jamf or a configuration profile on macOS; Group Policy or Intune on Windows; fleet management on Linux). Claude Code looks for it at one platform-specific path:

| Platform | Path |
|---|---|
| macOS | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| Linux and WSL | `/etc/claude-code/managed-mcp.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-mcp.json` |

The file uses the same format as a project `.mcp.json` file:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.example.com"
      }
    }
  }
}
```

**Per-user credentials.** Any user on the machine can read this file, so do not store API keys in `env` blocks. Pass per-user credentials with `${VAR}` expansion, OAuth or per-user headers, or `headersHelper` (auth mechanisms detailed in the authentication sibling note).

**Validate.** On a managed machine, `claude mcp list` should show only the `managed-mcp.json` servers (if a user's own servers still appear, the file isn't being read — check path/permissions), and `claude mcp add --transport http test https://example.com/mcp` should fail with the enterprise-policy error below (the URL need not be real — the policy check rejects the command before contacting anything).

**Disable MCP entirely.** Deploy a `managed-mcp.json` with an empty server map (`{"mcpServers": {}}`) to block every server; previously-configured servers stop loading the next session with no warning that policy is the reason.

**Allow claude.ai connectors.** Deploying `managed-mcp.json` suppresses claude.ai connectors by default (including admin-console connectors). Set `"allowAllClaudeAiMcps": true` in a managed settings source (server-managed settings, MDM plist/HKLM registry, or system `managed-settings.json`) to load them alongside the managed set; allowlists/denylists still apply, and user/project settings have no effect on it (requires v2.1.149+).

## Policy-based control with allowlists and denylists

Allowlists and denylists filter which configured servers load — they are not a registry, so a server must first be added by a user, a plugin, or `managed-mcp.json` before they apply. To make the allowlist authoritative, set `allowedMcpServers` **and** `allowManagedMcpServersOnly: true` together in a managed settings source. Without `allowManagedMcpServersOnly`, allowlists from every settings source merge (including a user's `~/.claude/settings.json`), so users can broaden what your allowlist permits. **Denylists merge from every source regardless.** (`allowManagedMcpServersOnly` is separate from `allowManagedPermissionRulesOnly`, which locks down permission rules only.)

**Match by URL, command, or name.** Each `allowedMcpServers`/`deniedMcpServers` entry is an object with a single matching key:

| Key | Matches | Use for |
|---|---|---|
| `serverUrl` | A remote server URL, exact or with `*` wildcards | HTTP and SSE servers |
| `serverCommand` | The exact command and arguments that start a stdio server | Stdio servers |
| `serverName` | The user-assigned label; exact match only, no wildcards | Either type (but see warning) |

An allowlist using only `serverName` entries is **not** a security control: the name is whatever label a user assigns, so a user can call any server `github`. To enforce which servers actually run, add `serverCommand` or `serverUrl` entries. Note that leaving `allowedMcpServers` unset (all servers allowed) differs from setting it to an empty array `[]` (no servers allowed) — the populated case allows only matching servers; `deniedMcpServers` unset or `[]` blocks nothing.

**How a server is evaluated.** Before loading any server (including from `managed-mcp.json`), Claude Code runs three checks in order:

1. **Merge the lists.** Allowlist and denylist entries from every source combine into one allowlist and one denylist. When `allowManagedMcpServersOnly` is `true`, only the managed allowlist is kept; the denylist always merges from every source.
2. **Check the denylist.** A server matching any denylist entry (URL, command, or name) is blocked — nothing overrides a denylist match.
3. **Check the allowlist.** If `allowedMcpServers` is unset anywhere, every server that passed the denylist loads. If set, a remote (HTTP/SSE) server must match a `serverUrl` entry (a `serverName` match counts only when there are no `serverUrl` entries), and a stdio server must match a `serverCommand` entry (a `serverName` match counts only when there are no `serverCommand` entries).

Two matching rules apply: commands match **exactly** (every argument, in order), and URLs support `*` wildcards anywhere including the scheme (hostname matching is case-insensitive and ignores a trailing FQDN dot; paths stay case-sensitive). For example `https://mcp.example.com/*` allows all paths on a domain, `https://*.example.com/*` any subdomain, `http://localhost:*/*` any port, and `*://mcp.example.com/*` any scheme.

**Restrict the allowlist to managed settings only.** Set `allowManagedMcpServersOnly` in the managed settings file so allowlists from user, project, and local settings are ignored (the denylist still merges from all sources):

```json
{
  "allowManagedMcpServersOnly": true,
  "allowedMcpServers": [
    { "serverUrl": "https://api.githubcopilot.com/*" },
    { "serverUrl": "https://*.internal.example.com/*" }
  ]
}
```

In a mixed hard allowlist + denylist, once one `serverUrl` entry exists every remote server must match a URL pattern (and likewise for `serverCommand`), so a user cannot sneak in an unlisted remote server by giving it an allowed name; a denylist `serverName` entry like `dangerous-server` still blocks regardless of URL or command.

## How restrictions appear to users

When a restriction blocks a server, the user either sees an error from `claude mcp add` or the server silently stops loading:

| Restriction | What the user sees |
|---|---|
| `managed-mcp.json` present + user runs `claude mcp add` | `Cannot add MCP server: enterprise MCP configuration is active and has exclusive control over MCP servers` |
| Server on a denylist + user runs `claude mcp add` | `Cannot add MCP server "<name>": server is explicitly blocked by enterprise policy` |
| Server not on the allowlist + user runs `claude mcp add` | `Cannot add MCP server "<name>": not allowed by enterprise policy` |
| A previously configured server now blocked by policy | The server silently disappears from `/mcp` and `claude mcp list` with no warning |

In the last case the user gets no signal that policy is the reason, so tell affected users which servers are blocked when you roll out a new restriction.

## Monitor MCP usage

When [OpenTelemetry export](https://code.claude.com/docs/en/monitoring-usage) is configured, Claude Code can record which MCP servers and tools users invoke. Set `OTEL_LOG_TOOL_DETAILS=1` to include MCP server and tool names in tool events, then aggregate them in your collector to see which servers your users actually connect to. The full event schema is on the Monitoring page.

## Configuration summary

| Surface | What it controls | Where it lives | How to deliver |
|---|---|---|---|
| `managed-mcp.json` | Fixed server set, exclusive control | System path (`/Library/Application Support/ClaudeCode/`, `/etc/claude-code/`, or `C:\Program Files\ClaudeCode\`) | MDM, GPO, fleet management, or any admin-privileged process. Cannot be set through server-managed settings |
| `allowedMcpServers` | Allowlist of permitted servers | Any settings file; entries from every source merge unless `allowManagedMcpServersOnly` is set | For enforcement, a managed settings source (server-managed settings, `managed-settings.json`, MDM profile, or registry) |
| `deniedMcpServers` | Denylist of blocked servers | Any settings file; entries from every source merge | Same as `allowedMcpServers` |
| `allowManagedMcpServersOnly` | Locks the allowlist to managed sources only | Managed settings sources only; no effect elsewhere | Same as `allowedMcpServers` |
| `allowAllClaudeAiMcps` | Loads claude.ai connectors alongside `managed-mcp.json` | Managed settings sources only; no effect elsewhere | Same as `allowedMcpServers` |

## Related Notes

- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: this note is the admin reference for restricting which MCP servers users can connect to, so the term is the direct parent concept.
- [Access Control](../../term_dictionary/term_access_control.md) — granting/denying requests to use information services; relevance: the entire page is access control over MCP servers — fixed-set deployment, allowlists, denylists — the granting/denying this term defines.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern where actions are blocked unless explicitly allowed; relevance: `managed-mcp.json` exclusive control and an empty/populated `allowedMcpServers` implement default-deny (nothing loads unless on the list), the pattern this term names.
- [Fine-Grained Access Control (FGAC)](../../term_dictionary/term_fgac.md) — row/column/cell-level data-access controls; relevance: matching servers by exact `serverUrl`/`serverCommand`/`serverName` with wildcard URL patterns is fine-grained, per-server access control of the kind this term describes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the note details Claude Code's managed-settings precedence, system config paths, and the enterprise-policy errors users see.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — per-channel security gate deciding whether an inbound sender may interact, via allowlist; relevance: the note's `allowedMcpServers`/`deniedMcpServers` evaluation (denylist-wins, allowlist-gates) is the same allowlist/denylist gate pattern this term implements for messaging adapters.
- [Data Governance](../../term_dictionary/term_data_governance.md) — org policies/roles/standards for managing data assets securely and compliantly; relevance: centrally controlling which MCP servers (and thus which external data flows) an organization permits is a data-governance enforcement this term frames, including the OTEL usage-monitoring it recommends.

**Source**: https://code.claude.com/docs/en/managed-mcp
**Last Updated**: 2026-06-13
**Status**: Active
