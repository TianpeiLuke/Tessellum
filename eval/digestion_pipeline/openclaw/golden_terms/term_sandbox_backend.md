---
tags:
  - resource
  - terminology
  - openclaw
  - sandbox
  - sandbox-backend
  - process-isolation
  - execution-isolation
keywords:
  - Sandbox Backend
  - sandbox provider
  - Docker sandbox
  - SSH sandbox
  - OpenShell sandbox
  - agents.defaults.sandbox.backend
topics:
  - Process isolation
  - Sandbox backends
  - OpenClaw security architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://docs.openclaw.ai/gateway/sandboxing
access_control_group: ["general"]
---

# Sandbox Backend

## Definition

A **sandbox backend** is the pluggable execution-isolation provider in an agent runtime: an abstraction layer that lets a host process delegate tool execution (shell commands, file I/O, code interpretation) to an isolated environment without coupling the host to any single isolation technology. The pattern has become load-bearing across modern coding agents because every shell command an LLM emits is a potential blast-radius event — a sandbox backend bounds that radius. Anthropic's Claude Code, for instance, ships a `sandbox-runtime` that swaps between `sandbox-exec` on macOS and `bubblewrap` on Linux behind a single bash-tool contract, reporting an 84% reduction in permission prompts when the agent works inside fixed boundaries. Cursor takes a similar plug approach (Seatbelt/sandbox-exec on macOS; Landlock + seccomp on Linux), and the broader Linux ecosystem offers Docker rootless, firejail, and bubblewrap as drop-in providers behind comparable contracts.

In **OpenClaw**, "Sandbox Backend" is the named abstraction: a `SandboxBackendFactory` produces a `SandboxBackend` handle whose `prepareExec` / `finalizeExec` / `runShellCommand` / `createFsBridge` methods every agent calls — the host stays on the user's machine, while tool execution runs against one of three provider choices selected by the `agents.defaults.sandbox.backend` config key: **Docker** (the default, container per scope via the local Docker daemon), **SSH** (a remote machine matching production OS / hardware / toolchains), or **OpenShell** (OpenClaw's signature openshell-CLI-backed remote sandbox). All three implement the same factory contract, register through the same plugin host, and produce instances at the same per-scope lifecycle — so an operator can switch backends by flipping one config value without touching any tool code.

## Context

The sandbox backend sits between the **context engine** (which assembles per-turn context for the agent) and the actual tool implementation. When an agent decides to run `bash` or read a file, the call flows: agent → tool registry → sandbox backend → isolated environment. OpenClaw's plugin host loads each backend (`extensions/openshell/`, the bundled Docker backend, the SSH adapter) at startup, asks each plugin for a `SandboxBackendFactory`, and dispatches per-scope creation when an [ACP](term_acp_agent_client_protocol.md) session opens. The factory is a closure capturing the resolved plugin config; the per-scope `createParams` (workspace dir, agent workspace dir, scope key) arrive at call time. A [subagent](term_subagent.md) inherits its parent's backend selection by default but may override it through the same `agents.defaults.sandbox.backend` key scoped to its agent profile.

The three-backend triad exists because no single isolation technology covers every use case: Docker is local and fast but requires the daemon and falls short for cloud-only environments; SSH lets agents run inside production-shaped boxes (specific OS versions, GPUs, pre-installed toolchains) but assumes the operator already runs a remote host; OpenShell wraps a managed remote runtime that handles provisioning, policy gates, and workspace mirroring without requiring operator-side container infrastructure. OpenClaw's default `docker.network = "none"` (no egress) — egress is opt-in per backend, a posture aligned with OWASP/CWE guidance on SSRF and exfiltration containment.

## Key Characteristics

- **Pluggable factory contract** — every backend implements `SandboxBackendFactory: (createParams) => Promise<SandboxBackend>`; the factory itself is sync (no startup I/O) and captures plugin config in a closure
- **Per-scope backend instances** — one backend handle per agent scope (typically per session / workspace), constructed lazily on first tool call, disposed when the scope ends
- **Mode discrimination** — at minimum `mirror` (local workspace is canonical, re-uploaded each exec) vs `remote` (remote workspace is canonical after initial seed); the mode is per-backend config, not per-call
- **Workspace mirror semantics** — `mirror` mode does a `syncWorkspaceToRemote` before every exec and `syncWorkspaceFromRemote` after; `remote` mode seeds once via `maybeSeedRemoteWorkspace` and trusts the remote thereafter; `local` collapses to direct execution
- **Exec spec contract** — `prepareExec({command, workdir, env, usePty})` returns `{argv, token}`; `finalizeExec(token)` runs after; both calls are idempotent
- **fs-bridge transport** — `createFsBridge` exposes a typed file-system facade so tool implementations stay backend-agnostic (a tool that reads a file does not know whether the bytes came from a local FS, a Docker volume, or an SSH cat)
- **Lifecycle** — `ensureSandboxExists` (single-flight via in-flight `ensurePromise`), `prepareExec`, `runShellCommand` or argv-exec, `finalizeExec`, dispose; single-flight prevents two concurrent execs from racing `sandbox create`
- **Safety floors** — `sandbox create` timeout is `max(configured, 300_000)` ms (5-minute floor for cold provisioning); managed remote roots whitelist (`/sandbox`, `/agent`) prevents `remoteWorkspaceDir: "/etc"` mistakes

## Related Terms


### Related Code Snippets

- **[OpenShell Backend](../code_snippets/snippet_openclaw_security_openshell_backend.md)**: factory + backend implementation for the OpenShell choice; the concrete reference for the contract above
- **[OpenShell CLI](../code_snippets/snippet_openclaw_security_openshell_cli.md)**: the SSH-bridged CLI invocation that executes inside the openshell sandbox
- **[OpenShell FS Bridge](../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md)**: `createFsBridge` implementation — how a backend exposes file I/O to backend-agnostic tools
- **[OpenShell Mirror](../code_snippets/snippet_openclaw_security_openshell_mirror.md)**: `syncWorkspaceToRemote` / `syncWorkspaceFromRemote` — the mirror-mode workspace synchronization semantics

### Related Analysis (FZ 15)


## References

- [Sandbox (computer security) — Wikipedia](https://en.wikipedia.org/wiki/Sandbox_(computer_security))
- [OpenClaw Sandboxing — Gateway Docs](https://docs.openclaw.ai/gateway/sandboxing)
- [Claude Code Sandboxing — Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Claude Code Sandboxing — Claude Code Docs](https://code.claude.com/docs/en/sandboxing)
- [Implementing a Secure Sandbox for Local Agents — Cursor Blog](https://cursor.com/blog/agent-sandboxing)
- [Bubblewrap — Unprivileged Sandboxing Tool](https://github.com/containers/bubblewrap)
- [OpenClaw `sandbox.ts` — Backend Registry](https://github.com/openclaw/openclaw/blob/main/src/agents/sandbox.ts)
- [OpenClaw OpenShell Backend Source](https://github.com/openclaw/openclaw/blob/main/extensions/openshell/src/backend.ts)
