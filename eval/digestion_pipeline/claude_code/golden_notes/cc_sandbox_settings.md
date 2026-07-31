---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - sandbox
keywords:
  - sandbox settings
  - bash sandboxing
  - filesystem allowwrite denyread
  - network alloweddomains
  - sandbox path prefixes
  - excluding sensitive files
  - permissions deny
  - weaker sandbox
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

# Claude Code — Sandbox Settings

## Overview

The `sandbox.*` keys in `settings.json` configure Claude Code's advanced sandboxing behavior, which isolates bash commands from your filesystem and network (macOS, Linux, and WSL2). These keys turn the sandbox on, decide what happens when it cannot start, set what may run outside it, and bound which filesystem paths and network destinations sandboxed commands may reach. Sandbox filesystem paths support a small set of prefixes for absolute, home-relative, and project-relative resolution. A separate but related lever — `permissions.deny` with `Read(...)` rules — excludes sensitive files (API keys, `.env`, secrets) from Claude Code's file discovery and reads. Full sandbox mechanics are documented in [Sandboxing](https://code.claude.com/docs/en/sandboxing); this note is the settings interface to it.

## Sandbox settings

Configure advanced sandboxing behavior. Sandboxing isolates bash commands from your filesystem and network. See [Sandboxing](https://code.claude.com/docs/en/sandboxing) for details.

**Enable / availability / auto-approve:**

- `enabled` — Enable bash sandboxing (macOS, Linux, and WSL2). Default: `false`. Example `true`.
- `failIfUnavailable` — Exit with an error at startup if `sandbox.enabled` is true but the sandbox cannot start (missing dependencies or unsupported platform). When false (default), a warning is shown and commands run unsandboxed. Intended for managed-settings deployments that require sandboxing as a hard gate. Example `true`.
- `autoAllowBashIfSandboxed` — Auto-approve bash commands when sandboxed. Default: `true`.
- `excludedCommands` — Commands that should run outside of the sandbox. Example `["docker *"]`.
- `allowUnsandboxedCommands` — Allow commands to run outside the sandbox via the `dangerouslyDisableSandbox` parameter. When set to `false`, the `dangerouslyDisableSandbox` escape hatch is completely disabled and all commands must run sandboxed (or be in `excludedCommands`). Useful for enterprise policies that require strict sandboxing. Default: `true`.

**Filesystem (`filesystem.*`):**

- `filesystem.allowWrite` — Additional paths where sandboxed commands can write. Arrays are merged across all settings scopes: user, project, and managed paths are combined, not replaced. Also merged with paths from `Edit(...)` allow permission rules. Example `["/tmp/build", "~/.kube"]`.
- `filesystem.denyWrite` — Paths where sandboxed commands cannot write. Arrays merged across all settings scopes. Also merged with paths from `Edit(...)` deny permission rules. Example `["/etc", "/usr/local/bin"]`.
- `filesystem.denyRead` — Paths where sandboxed commands cannot read. Arrays merged across all settings scopes. Also merged with paths from `Read(...)` deny permission rules. Example `["~/.aws/credentials"]`.
- `filesystem.allowRead` — Paths to re-allow reading within `denyRead` regions. Takes precedence over `denyRead`. Arrays merged across all settings scopes. Use this to create workspace-only read access patterns. Example `["."]`.
- `filesystem.allowManagedReadPathsOnly` — (Managed settings only) Only `filesystem.allowRead` paths from managed settings are respected. `denyRead` still merges from all sources. Default: `false`.

**Network (`network.*`):**

- `network.allowUnixSockets` — (macOS only) Unix socket paths accessible in sandbox. Ignored on Linux and WSL2, where the seccomp filter cannot inspect socket paths; use `allowAllUnixSockets` instead. Example `["~/.ssh/agent-socket"]`.
- `network.allowAllUnixSockets` — Allow all Unix socket connections in sandbox. On Linux and WSL2 this is the only way to permit Unix sockets, since it skips the seccomp filter that otherwise blocks `socket(AF_UNIX, ...)` calls. Default: `false`.
- `network.allowLocalBinding` — Allow binding to localhost ports (macOS only). Default: `false`.
- `network.allowMachLookup` — (macOS only) Additional XPC/Mach service names the sandbox may look up. Supports a single trailing `*` for prefix matching. Needed for tools that communicate via XPC such as the iOS Simulator or Playwright. Example `["com.apple.coresimulator.*"]`.
- `network.allowedDomains` — Array of domains to allow for outbound network traffic. Supports wildcards (e.g., `*.example.com`). Example `["github.com", "*.npmjs.org"]`.
- `network.deniedDomains` — Array of domains to block for outbound network traffic. Same wildcard syntax as `allowedDomains`. Takes precedence over `allowedDomains` when both match. Merged from all settings sources regardless of `allowManagedDomainsOnly`. Example `["sensitive.cloud.example.com"]`.
- `network.allowManagedDomainsOnly` — (Managed settings only) Only `allowedDomains` and `WebFetch(domain:...)` allow rules from managed settings are respected. Domains from user, project, and local settings are ignored. Non-allowed domains are blocked automatically without prompting the user. Denied domains are still respected from all sources. Default: `false`.
- `network.httpProxyPort` — HTTP proxy port used if you wish to bring your own proxy. If not specified, Claude will run its own proxy. Example `8080`.
- `network.socksProxyPort` — SOCKS5 proxy port used if you wish to bring your own proxy. If not specified, Claude will run its own proxy. Example `8081`.

**Weaker-sandbox and managed binaries:**

- `enableWeakerNestedSandbox` — Enable weaker sandbox for unprivileged Docker environments (Linux and WSL2 only). **Reduces security.** Default: `false`.
- `enableWeakerNetworkIsolation` — (macOS only) Allow access to the system TLS trust service (`com.apple.trustd.agent`) in the sandbox. Required for Go-based tools like `gh`, `gcloud`, and `terraform` to verify TLS certificates when using `httpProxyPort` with a MITM proxy and custom CA. **Reduces security** by opening a potential data exfiltration path. Default: `false`.
- `bwrapPath` — (Managed settings only, Linux/WSL2) Absolute path to the bubblewrap (`bwrap`) binary. Overrides automatic detection via `PATH`. Only honored from managed settings. Example `/opt/admin/bwrap`.
- `socatPath` — (Managed settings only, Linux/WSL2) Absolute path to the `socat` binary used for the sandbox network proxy. Overrides automatic detection via `PATH`. Only honored from managed settings. Example `/opt/admin/socat`.

### Sandbox path prefixes

Paths in `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead`, and `filesystem.allowRead` support these prefixes:

| Prefix | Meaning | Example |
| :--- | :--- | :--- |
| `/` | Absolute path from filesystem root | `/tmp/build` stays `/tmp/build` |
| `~/` | Relative to home directory | `~/.kube` becomes `$HOME/.kube` |
| `./` or no prefix | Relative to the project root for project settings, or to `~/.claude` for user settings | `./output` in `.claude/settings.json` resolves to `<project-root>/output` |

The older `//path` prefix for absolute paths still works. If you previously used single-slash `/path` expecting project-relative resolution, switch to `./path`. This syntax differs from [Read and Edit permission rules](https://code.claude.com/docs/en/permissions#read-and-edit), which use `//path` for absolute and `/path` for project-relative. Sandbox filesystem paths use standard conventions: `/tmp/build` is an absolute path.

**Configuration example:**

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "deniedDomains": ["uploads.github.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**Filesystem and network restrictions** can be configured in two ways that are merged together:

- **`sandbox.filesystem` settings** (shown above): Control paths at the OS-level sandbox boundary. These restrictions apply to all subprocess commands (e.g., `kubectl`, `terraform`, `npm`), not just Claude's file tools.
- **Permission rules**: Use `Edit` allow/deny rules to control Claude's file tool access, `Read` deny rules to block reads, and `WebFetch` allow/deny rules to control network domains. Paths from these rules are also merged into the sandbox configuration.

## Excluding sensitive files

To prevent Claude Code from accessing files containing sensitive information like API keys, secrets, and environment files, use the `permissions.deny` setting in your `.claude/settings.json` file:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

This replaces the deprecated `ignorePatterns` configuration. Files matching these patterns are excluded from file discovery and search results, and read operations on these files are denied.

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
