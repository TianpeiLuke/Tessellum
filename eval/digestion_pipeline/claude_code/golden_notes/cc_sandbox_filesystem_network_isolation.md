---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - isolation
keywords:
  - filesystem isolation
  - network isolation
  - os-level enforcement
  - allowwrite denyread
  - sandbox path prefixes
  - seatbelt bubblewrap
  - allowed domains
  - sandbox proxy
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sandboxing
access_control_group: ["general"]
---

# Claude Code — Sandbox Filesystem & Network Isolation

## Overview

The sandboxed Bash tool turns "which files and network domains can a command touch" into an OS-enforced boundary applied to every Bash command and its child processes. By default, sandboxed commands can **write** only to the current working directory and the session temp directory, and can **read** the entire computer except explicitly denied directories. You widen or narrow this boundary through `sandbox.filesystem.*` settings (path-prefix syntax) and `allowedDomains`, while a proxy outside the sandbox controls network egress. Because enforcement happens at the OS level — Seatbelt on macOS, bubblewrap on Linux/WSL2 — the boundary holds on the running process regardless of what the model chose to run, and all subprocesses inherit it.

## Configure sandboxing (paths)

Sandbox behavior is customized through `settings.json` (full reference: [Settings — sandbox settings](https://code.claude.com/docs/en/settings)). By default, sandboxed commands can write only to the current working directory and the session temp directory. When subprocess commands like `kubectl`, `terraform`, or `npm` need to write outside those directories, grant access with `sandbox.filesystem.allowWrite`:

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

These paths are enforced at the OS level, so all commands inside the sandbox (including child processes) respect them — the recommended approach when a tool needs write access to a specific location, rather than excluding the tool entirely with `excludedCommands`. When the same filesystem array is defined in multiple settings scopes, the arrays are **merged**: paths from every scope are combined, not replaced.

**Path prefixes** control how paths resolve:

| Prefix | Meaning | Example |
| :--- | :--- | :--- |
| `/` | Absolute path from filesystem root | `/tmp/build` stays `/tmp/build` |
| `~/` | Relative to home directory | `~/.kube` becomes `$HOME/.kube` |
| `./` or no prefix | Relative to the project root for project settings, or to `~/.claude` for user settings | `./output` in `.claude/settings.json` resolves to `<project-root>/output` |

This syntax differs from Read/Edit permission rules (which use `//path` for absolute and `/path` for project-relative); sandbox filesystem paths use standard conventions, so `/tmp/build` is absolute. You can also deny access with `sandbox.filesystem.denyWrite` and `sandbox.filesystem.denyRead`, then re-allow specific paths within a denied region using `sandbox.filesystem.allowRead`. The example below blocks reading the entire home directory while still allowing reads from the current project — placed in the project's `.claude/settings.json`, because `.` resolves to the project root only when the configuration lives in project settings:

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

The `.` in `allowRead` resolves to the project root because this config lives in project settings. Placed in `~/.claude/settings.json` instead, `.` would resolve to `~/.claude` and project files would stay blocked by the `denyRead` rule.

## How sandboxing works

### Filesystem isolation

The sandboxed Bash tool restricts filesystem access to specific directories:

- **Default write behavior**: read and write access to the current working directory and its subdirectories, plus the session temp directory that `$TMPDIR` points to.
- **Default read behavior**: read access to the entire computer, except certain denied directories. This default still allows reading credential files such as `~/.aws/credentials` and `~/.ssh/` — add them to `denyRead` to block them.
- **Blocked access**: cannot modify files outside the working directory and session temp directory without explicit permission, including shell config files such as `~/.bashrc` and system binaries in `/bin/`.
- **Git worktrees**: when the working directory is a linked git worktree, the sandbox also allows writes to the main repository's shared `.git` directory so commands such as `git commit` can update refs and the index. Writes to `hooks/` and `config` inside that directory remain denied.
- **Configurable**: define custom allowed and denied paths through settings.

Grant write access to additional paths with `sandbox.filesystem.allowWrite`. These restrictions are enforced at the OS level, so they apply to all subprocess commands (e.g. `kubectl`, `terraform`, `npm`), not just Claude's file tools.

### Network isolation

Network access is controlled through a proxy server running outside the sandbox:

- **Domain restrictions**: no domains are pre-allowed. The first time a command needs a new domain, Claude Code prompts for approval. Pre-allow domains with `allowedDomains` to avoid the prompt.
- **Managed lockdown**: if `allowManagedDomainsOnly` is set in managed settings, non-allowed domains are blocked automatically instead of prompting, and only `allowedDomains` from managed settings are honored.
- **Custom proxy support**: advanced users can implement custom rules on outgoing traffic.
- **Comprehensive coverage**: restrictions apply to all scripts, programs, and subprocesses spawned by commands.

The built-in proxy enforces the allowlist based on the requested hostname and does **not** terminate or inspect TLS traffic. See [Sandbox Limitations & Troubleshooting](cc_sandbox_limitations_and_troubleshooting.md) for the implications of this design, and the org-enforcement note's custom proxy configuration if your threat model requires TLS inspection.

### OS-level enforcement

The sandboxed Bash tool leverages operating system security primitives:

- **macOS**: uses Seatbelt for sandbox enforcement.
- **Linux**: uses bubblewrap for isolation.
- **WSL2**: uses bubblewrap, same as Linux.

WSL1 is not supported because bubblewrap requires kernel features only available in WSL2. These OS-level restrictions ensure that all child processes spawned by Claude Code's commands inherit the same security boundaries. The same primitives are available as the standalone `@anthropic-ai/sandbox-runtime` package, which the comparison note covers as a separate approach for wrapping the entire Claude Code process (see [Sandbox Runtime & Containers](cc_sandbox_runtime_and_containers.md)).

**Source**: https://code.claude.com/docs/en/sandboxing
**Last Updated**: 2026-06-13
**Status**: Active
