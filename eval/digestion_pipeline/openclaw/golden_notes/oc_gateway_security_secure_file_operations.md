---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - fs_safe
keywords:
  - openclaw fs-safe
  - secure file operations
  - root-bounded file access
  - OPENCLAW_FS_SAFE_PYTHON_MODE
  - python helper off by default
  - library guardrail not sandbox
  - path escape rejection
  - fd-relative mutation hardening
topics:
  - OpenClaw
  - Secure File Operations
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/security/secure-file-operations
access_control_group: ["general"]
---

# OpenClaw — Secure File Operations (`@openclaw/fs-safe`)

## Overview

This note explains the OpenClaw **secure file operations** concept: the `@openclaw/fs-safe` library that trusted Gateway code uses when it receives untrusted path names, and why its optional POSIX Python helper is off by default. It mirrors the `gateway/security/secure-file-operations` source page, covering the four source sections — the no-Python default, the Node-only protections that always apply, what the Python helper adds, and the plugin/core usage guidance.

OpenClaw uses [`@openclaw/fs-safe`](https://github.com/openclaw/fs-safe) for security-sensitive local file operations: root-bounded reads/writes, atomic replacement, archive extraction, temp workspaces, JSON state, and secret-file handling. The goal is a consistent **library guardrail** for trusted OpenClaw code that receives untrusted path names. It is *not a sandbox*. Host filesystem permissions, OS users, containers, and the agent/tool policy still define the real blast radius.

## Default: No Python Helper

OpenClaw defaults the fs-safe POSIX Python helper to **off**. The reasons the source gives are: the gateway should not spawn a persistent Python sidecar unless an operator opted into it; many installs do not need the extra parent-directory mutation hardening; and disabling Python keeps package/runtime behavior more predictable across desktop, Docker, CI, and bundled app environments.

OpenClaw only changes the default — if you explicitly set a mode, fs-safe honors it. The mode is selected through the `OPENCLAW_FS_SAFE_PYTHON_MODE` environment variable, with an optional explicit interpreter via `OPENCLAW_FS_SAFE_PYTHON`:

```bash
# Default OpenClaw behavior: Node-only fs-safe fallbacks.
OPENCLAW_FS_SAFE_PYTHON_MODE=off

# Opt into the helper when available, falling back if unavailable.
OPENCLAW_FS_SAFE_PYTHON_MODE=auto

# Fail closed if the helper cannot start.
OPENCLAW_FS_SAFE_PYTHON_MODE=require

# Optional explicit interpreter.
OPENCLAW_FS_SAFE_PYTHON=/usr/bin/python3
```

The generic fs-safe names also work: `FS_SAFE_PYTHON_MODE` and `FS_SAFE_PYTHON`.

## What Stays Protected Without Python

With the helper off, OpenClaw still uses fs-safe's Node paths for the following protections:

- rejecting relative-path escapes such as `..`, absolute paths, and path separators where only names are allowed;
- resolving operations through a trusted root handle instead of ad-hoc `path.resolve(...).startsWith(...)` checks;
- refusing symlink and hardlink patterns on APIs that require that policy;
- opening files with identity checks where the API returns or consumes file contents;
- atomic sibling-temp writes for state/config files;
- byte limits for reads and archive extraction;
- private modes for secrets and state files where the API requires them.

These protections cover the normal OpenClaw threat model: trusted gateway code handling untrusted model/plugin/channel path input inside a single trusted operator boundary.

## What Python Adds

On POSIX, fs-safe's optional helper keeps one persistent Python process and uses fd-relative filesystem operations for parent-directory mutations such as rename, remove, mkdir, stat/list, and some write paths. That narrows same-UID race windows where another process can swap a parent directory between validation and mutation. It is defense in depth for hosts where untrusted local processes can modify the same directories OpenClaw is operating in.

If your deployment has that risk and Python is guaranteed to exist, use `require`:

```bash
OPENCLAW_FS_SAFE_PYTHON_MODE=require
```

Use `require` rather than `auto` when the helper is part of your security posture; `auto` intentionally falls back to Node-only behavior if the helper is unavailable.

## Plugin and Core Guidance

The source page closes with usage guidance for plugin and core code:

- Plugin-facing file access should go through `openclaw/plugin-sdk/*` helpers, not raw `fs`, when a path comes from a message, model output, config, or plugin input.
- Core code should use the local fs-safe wrappers under `src/infra/*` so OpenClaw's process policy is applied consistently.
- Archive extraction should use the fs-safe archive helpers with explicit size, entry-count, link, and destination limits.
- Secrets should use OpenClaw secret helpers or fs-safe secret/private-state helpers; do not hand-roll mode checks around `fs.writeFile`.
- If you need hostile local-user isolation, do not rely on fs-safe alone. Run separate gateways under separate OS users/hosts or use sandboxing.

**Source**: OpenClaw documentation — `gateway/security/secure-file-operations` (mirror `inbox/openclaw_docs/gateway/security/secure-file-operations.md`)
**Last Updated**: 2026-06-22
**Status**: Active
