---
tags:
  - resource
  - terminology
  - openclaw
  - sandbox
  - openshell
  - process-isolation
  - cli-wrapper
keywords:
  - OpenShell
  - openshell sandbox backend
  - sandbox extension
  - workspace mirror
  - fs-bridge
  - mode mirror remote
topics:
  - Sandbox backends
  - Process isolation
  - OpenClaw security architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/tree/main/extensions/openshell
access_control_group: ["general"]
---

# OpenShell

## Definition

**OpenShell** is OpenClaw's pluggable **sandbox-backend extension** that delegates agent code execution to a remote sandbox managed by the `openshell` CLI binary, bridged over SSH. Implemented as a TypeScript plugin under `extensions/openshell/`, it satisfies the `SandboxBackendFactory` interface and is selected when an agent profile declares `agents.defaults.sandbox.backend: "openshell"` — sitting as a sister to the in-process Docker and SSH backends. The backend wraps the `openshell sandbox create / get / ssh-config / exec` subcommands so OpenClaw can stand up an isolated remote workspace per agent scope, then ship every `exec`, `read`, `write`, `edit`, and `apply_patch` call across that boundary.

OpenShell sits in the same conceptual space as **firejail** and **bubblewrap** (Linux namespaces + seccomp for unprivileged process isolation) and Docker's rootless sandboxes — all four restrict an untrusted process so a crash, exploit, or hostile AI-generated command cannot reach the host filesystem, network, or kernel. Where firejail/bubblewrap isolate locally via kernel primitives and Docker isolates via a containerized engine, OpenShell isolates **remotely**: the sandbox lives on another host (or microVM), reached over SSH, so even kernel-level escapes never land on the agent operator's machine.

## Context

In OpenClaw's sandbox-backend taxonomy, OpenShell is one of three pluggable choices: **Docker** (local containers, no remote hop), **SSH** (BYO remote host, OpenClaw runs commands there), and **OpenShell** (managed remote sandboxes, OpenClaw delegates lifecycle to the `openshell` CLI). The plugin registers under `extensions/openshell/` with an `openclaw.plugin.json` manifest and is consumed by user config blocks like `plugins.entries.openshell.config.mode: "mirror"` plus `agents.defaults.sandbox.backend: "openshell"`. It reuses the generic SSH transport from `extensions/ssh-sandbox/` plus the workspace-mirror utilities, then layers openshell-specific lifecycle (`sandbox create`, `sandbox ssh-config`) on top.

The backend exposes two **workspace modes**. In `mirror` mode (default) the local workspace stays canonical — `prepareExec` re-uploads it before every exec and `finalizeExec` syncs remote changes back, so the host directory always reflects sandbox writes. In `remote` mode the remote workspace becomes canonical after a one-shot seed on `sandbox create`; subsequent execs trust the remote state and skip the round-trip, trading exec-time mirror cost for first-class remote semantics.

## Key Characteristics

- **Backend-plugin factory + closure** — `createOpenShellSandboxBackendFactory(pluginConfig)` returns an async `(createParams) => SandboxBackend` so the plugin host can instantiate one backend per agent scope from a single resolved config; the closure captures `pluginConfig` by value to keep registration sync and side-effect free.
- **Single-flight `ensurePromise` with `remoteSeedPending` flag** — concurrent execs for the same scope share one `sandbox get` / `sandbox create` call; the promise is cached on success and cleared only on failure, while a separate boolean ensures the first post-create exec seeds the remote workspace exactly once.
- **Deterministic sandbox name** — `buildOpenShellSandboxName(scopeKey)` produces `openclaw-<safe-prefix>-<djb2hex>`; the prefix is lowercased/regex-sanitized and length-capped at 32 chars, while the 8-char djb2 hash is computed from the *original* scope key so two scopes that sanitize to the same prefix never collide.
- **Managed-remote-root enforcement** — `normalizeOpenShellRemotePath` (config layer) accepts only paths under `/sandbox` or `/agent` after `path.posix.normalize` collapses `..` escapes, so a misconfigured `remoteWorkspaceDir: "/etc"` cannot trick the mirror code into wiping system directories.
- **Bundled-binary resolution with memoization** — `resolveBundledOpenShellCommand` uses `require.resolve("openshell/package.json")` to locate the bundled CLI, with a tri-state cache (`undefined`/`null`/string) so the resolver runs at most once per process and degrades gracefully when the binary is absent.
- **Local↔remote workspace mirror** — `mode: "mirror"` runs a symlink-free `copyTreeWithoutSymlinks` walker with a 16-way `runLimitedFs` concurrency gate and a default exclude list (`hooks`, `git-hooks`, `.git`) so secrets and version-control state never cross the boundary.
- **fs-bridge for sandboxed reads/writes** — `createOpenShellFsBridge` exposes read/write/list/stat over the same SSH transport, with `assertLocalPathSafety` walking each path segment and rejecting symlink escapes so agent inputs and outputs traverse the boundary safely.

## Related Terms


## Related Code Snippets

- [Snippet: OpenShell Sandbox Backend + Config](../code_snippets/snippet_openclaw_security_openshell_backend.md) — factory closure, mode-conditional preflight, single-flight ensurePromise, deterministic sandbox name, managed-remote-root enforcement (backend.ts + config.ts)
- [Snippet: OpenShell CLI Invocation](../code_snippets/snippet_openclaw_security_openshell_cli.md) — bundled-binary resolution, base argv assembly, timeout-bound subprocess runner, SSH session bootstrap via exit-code translation (cli.ts)
- [Snippet: OpenShell Workspace Mirror](../code_snippets/snippet_openclaw_security_openshell_mirror.md) — module-scope policy constants, exclude-matcher, FS concurrency limiter, symlink-free tree copy, replace-vs-stage entry points (mirror.ts)
- [Snippet: OpenShell Filesystem Bridge](../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — factory + class shell, pinned-fsRoot read, local-then-remote write, dual-target rename, container-vs-host path routing, canonical-root symlink walk (fs-bridge.ts)

## Related Analysis (FZ 15)


## References

- [Bubblewrap (containers/bubblewrap)](https://github.com/containers/bubblewrap) — Class-1 sibling sandbox technology: low-level unprivileged sandboxing via Linux namespaces, powers Flatpak. Same isolation goal as OpenShell, different mechanism (local namespaces vs remote SSH).
- [Docker (software) — Wikipedia](https://en.wikipedia.org/wiki/Docker_(software)) — Class-1 reference for containerized sandbox isolation; OpenShell's Docker-backend sister covers this case directly.
- [Linux namespaces — Wikipedia](https://en.wikipedia.org/wiki/Linux_namespaces) — Class-1 reference for the kernel primitive underlying firejail, bubblewrap, and Docker isolation that OpenShell substitutes via remote SSH.
- [Docker rootless mode docs](https://docs.docker.com/engine/security/rootless/) — Class-2 reference for unprivileged container isolation; the local-backend analog to OpenShell's remote-managed-sandbox approach.
- [OpenClaw openshell extension source](https://github.com/openclaw/openclaw/tree/main/extensions/openshell) — Primary upstream: backend.ts, cli.ts, config.ts, mirror.ts, fs-bridge.ts plus tests.
