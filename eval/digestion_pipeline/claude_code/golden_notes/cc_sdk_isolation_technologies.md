---
tags:
  - resource
  - documentation
  - claude_code
  - secure_deployment
  - isolation
keywords:
  - isolation technologies
  - sandbox runtime
  - hardened docker container
  - gvisor runsc
  - firecracker microvm
  - vsock
  - unix socket egress
  - cloud private subnet
topics:
  - Claude Code
  - Secure Deployment
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/secure-deployment
access_control_group: ["general"]
---

# Claude Code SDK — Isolation Technologies

## Overview

When you deploy Claude Code or the Agent SDK for hardening beyond the defaults, you choose an **isolation boundary** that the agent runs *inside* — a sandbox, container, or VM — and the security controls then restrict what the agent can access from within that boundary. The available technologies trade off **isolation strength**, **performance overhead**, and **operational complexity**, so the right choice depends on the threat model rather than picking the "most secure" option unconditionally.

This note catalogs the four isolation tiers the secure-deployment guide describes — sandbox runtime, hardened containers, gVisor, and virtual machines — plus how to combine them with cloud-native network controls. The credential-injecting proxy that all of these architectures route egress through is covered in the sibling note [`cc_sdk_credential_and_filesystem_controls`](cc_sdk_credential_and_filesystem_controls.md); the threat model and security principles that motivate isolation are in [`cc_sdk_secure_deployment_principles`](cc_sdk_secure_deployment_principles.md).

## The tradeoff table

| Technology              | Isolation strength             | Performance overhead | Complexity  |
| ----------------------- | ------------------------------ | -------------------- | ----------- |
| Sandbox runtime         | Good (secure defaults)         | Very low             | Low         |
| Containers (Docker)     | Setup dependent                | Low                  | Medium      |
| gVisor                  | Excellent (with correct setup) | Medium/High          | Medium      |
| VMs (Firecracker, QEMU) | Excellent (with correct setup) | High                 | Medium/High |

In all of these configurations the agent runs inside the isolation boundary, and the controls restrict what it can access from within.

## Sandbox runtime

For lightweight isolation without containers, [sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime) enforces filesystem and network restrictions at the OS level. Its advantage is simplicity — no Docker config, container images, or networking setup; the proxy and filesystem restrictions are built in and you supply a settings file of allowed domains and paths. It uses OS primitives (`bubblewrap` on Linux, `sandbox-exec` on macOS) for filesystem access, removes the network namespace (Linux) or uses Seatbelt profiles (macOS) to route traffic through a built-in proxy, and configures JSON-based allowlists for domains and paths:

```bash
npm install @anthropic-ai/sandbox-runtime
```

Two security considerations apply: (1) **Same-host kernel** — sandboxed processes share the host kernel, so a kernel vulnerability could theoretically enable escape; use gVisor or a VM if you need kernel-level isolation. (2) **No TLS inspection** — the proxy allowlists domains by client-supplied hostname and does not terminate or inspect encrypted traffic, so code inside the sandbox could use domain fronting or similar to reach hosts outside the allowlist; configure a TLS-terminating proxy for stronger guarantees. For many single-developer and CI/CD use cases this raises the bar significantly with minimal setup.

## Containers (Docker)

Containers provide isolation through Linux namespaces — each has its own view of filesystem, process tree, and network stack while sharing the host kernel. A security-hardened configuration:

```bash
docker run \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --security-opt seccomp=/path/to/seccomp-profile.json \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --tmpfs /home/agent:rw,noexec,nosuid,size=500m \
  --network none \
  --memory 2g \
  --cpus 2 \
  --pids-limit 100 \
  --user 1000:1000 \
  -v /path/to/code:/workspace:ro \
  -v /var/run/proxy.sock:/var/run/proxy.sock:ro \
  agent-image
```

Each flag narrows the agent's reach: `--cap-drop ALL` removes Linux capabilities like `NET_ADMIN`/`SYS_ADMIN`; `--security-opt no-new-privileges` blocks setuid escalation; `--security-opt seccomp=...` restricts syscalls (Docker's default blocks ~44, custom profiles more); `--read-only` makes the root filesystem immutable; `--tmpfs` provides writable scratch cleared on stop; `--network none` removes all network interfaces; `--memory`/`--pids-limit` cap resources and prevent fork bombs; `--user 1000:1000` runs as non-root; and the read-only `-v` mounts code (avoid mounting sensitive host dirs like `~/.ssh`, `~/.aws`, `~/.config`).

**Unix socket architecture**: with `--network none` the only path to the outside world is the mounted Unix socket connecting to a proxy on the host, which enforces domain allowlists, injects credentials, and logs traffic. Even if the agent is compromised via prompt injection, it cannot exfiltrate to arbitrary servers — only through the proxy. This is the same architecture sandbox-runtime uses. Additional hardening options include `--userns-remap` (maps container root to an unprivileged host user, limiting damage from a container escape) and `--ipc private` (isolates inter-process communication to prevent cross-container attacks).

## gVisor

Standard containers send a syscall directly to the same kernel that runs the host, so a kernel vulnerability could allow container escape. gVisor addresses this by intercepting system calls in userspace before they reach the host kernel, implementing its own compatibility layer that handles most syscalls without involving the real kernel. Malicious agent code would have to exploit gVisor's userspace implementation first, with limited access to the real kernel. To use it with Docker, install the `runsc` runtime and configure the daemon, then run with `--runtime=runsc`:

```json
// /etc/docker/daemon.json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc"
    }
  }
}
```

The added isolation costs performance: CPU-bound computation is ~0% (no syscall interception), simple syscalls ~2× slower, and file-I/O-intensive open/close patterns up to 10–200× slower. For multi-tenant environments or untrusted content the overhead is often worth it.

## Virtual machines

VMs provide hardware-level isolation through CPU virtualization extensions — each VM runs its own kernel, so a guest-kernel vulnerability doesn't directly compromise the host. VMs aren't automatically "more secure" than gVisor; security depends heavily on the hypervisor and device-emulation code. **Firecracker** is designed for lightweight microVM isolation — it can boot in under 125 ms with less than 5 MiB memory overhead, stripping unnecessary device emulation to reduce attack surface. The agent VM has no external network interface; it communicates through `vsock` (virtual sockets), and all traffic routes through vsock to a host proxy that enforces allowlists and injects credentials before forwarding.

## Cloud deployments

Combine any of the above with cloud-native network controls:

1. Run agent containers in a **private subnet** with no internet gateway.
2. Configure cloud firewall rules (AWS Security Groups, GCP VPC firewall) to **block all egress except to your proxy**.
3. Run a proxy (such as [Envoy](https://www.envoyproxy.io/) with its `credential_injector` filter) that validates requests, enforces domain allowlists, injects credentials, and forwards to external APIs.
4. Assign **minimal IAM permissions** to the agent's service account, routing sensitive access through the proxy where possible.
5. **Log all traffic** at the proxy for audit.

**Source**: https://code.claude.com/docs/en/agent-sdk/secure-deployment
**Last Updated**: 2026-06-13
**Status**: Active
