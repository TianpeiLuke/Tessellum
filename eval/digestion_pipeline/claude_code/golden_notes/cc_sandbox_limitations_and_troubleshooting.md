---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - limitations
keywords:
  - sandbox limitations
  - sandbox troubleshooting
  - tls inspection
  - domain fronting
  - privilege escalation
  - unix socket bypass
  - filesystem permission escalation
  - enableweakernestedsandbox
  - excludedcommands
  - sandbox scope
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

# Claude Code — Sandbox Limitations and Troubleshooting

## Overview

The sandboxed Bash tool **reduces risk but is not a complete isolation boundary**. The Claude Code docs spell out where it stops being a hard control — the network proxy that does not inspect TLS, privilege-escalation paths through Unix sockets and overly-broad filesystem grants, and a weaker nested mode for unprivileged containers — plus the platforms it runs on and the scope of what it actually covers. This note collects those **limitations** alongside the **troubleshooting** fixes for commands that fail inside the sandbox even though they work outside it.

The recurring theme is that the sandbox is one layer: it should be backstopped by other controls, and broad allow grants on either the filesystem or network side can undo the boundary on the other side.

## Troubleshooting

Some commands fail inside the sandbox even though they work outside it. The docs list the most common cases and their fixes:

- **Commands fail with a host-not-allowed error**: many CLI tools need to reach specific hosts. Granting permission when prompted adds the host to your allowed list so the tool runs inside the sandbox in future.
- **`jest` hangs or fails**: `watchman` is incompatible with the sandbox. Run `jest --no-watchman` instead.
- **Go-based CLIs fail TLS verification on macOS**: tools such as `gh`, `gcloud`, and `terraform` may fail TLS verification under Seatbelt. List these tools in `excludedCommands` to run them outside the sandbox. If you are using `httpProxyPort` with a MITM proxy and custom CA, set `enableWeakerNetworkIsolation` to `true` instead.
- **`docker` commands fail**: `docker` is incompatible with the sandbox. Add `docker *` to `excludedCommands` to run it outside the sandbox.
- **Bubblewrap fails to start inside a container**: in an unprivileged container, bubblewrap cannot mount a fresh `/proc` filesystem. Set `enableWeakerNestedSandbox` to `true` so the inner sandbox bind-mounts the container's existing `/proc` instead. Only use this setting when the outer container already provides the isolation boundary you need, since it exposes process information to sandboxed commands that a fresh `/proc` mount would hide.
- **Seccomp filter on Linux**: the seccomp filter is required to block Unix domain sockets. The Dependencies tab in `/sandbox` shows whether it is available. If it is missing, run `npm install -g @anthropic-ai/sandbox-runtime` to install the helper.
- **`--dangerously-skip-permissions` fails as root**: this flag is blocked when running as root or via sudo on Linux and macOS, because root access combined with no permission prompts can modify any file or service on the system. The check is skipped automatically inside a recognized sandbox. To run autonomously in a container, use the dev container configuration, which runs Claude Code as a non-root user.

## Limitations

Sandboxing reduces risk but is not a complete isolation boundary. Review the limitations below before relying on it as a hard security control.

### Security limitations

- **Network filtering**: the network filtering system operates by restricting the domains that processes are allowed to connect to. The built-in proxy does not terminate or perform TLS inspection on outbound traffic, so the contents of encrypted connections are not examined. You are responsible for ensuring that only trusted domains are allowed in your policy. Allowing broad domains such as `github.com` can create paths for data exfiltration: because the proxy makes its allow decision from the client-supplied hostname without inspecting TLS, code running inside the sandbox can potentially use [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) or similar techniques to reach hosts outside the allowlist. If your threat model requires stronger guarantees, configure a custom proxy that terminates TLS and inspects traffic, and install its CA certificate inside the sandbox. Stronger TLS-aware network isolation is an active area of development.
- **Privilege escalation via Unix sockets**: the `allowUnixSockets` configuration can inadvertently grant access to powerful system services that could lead to sandbox bypasses. For example, allowing access to `/var/run/docker.sock` effectively grants access to the host system through the Docker socket. Consider carefully any Unix sockets that you allow through the sandbox.
- **Filesystem permission escalation**: overly broad filesystem write permissions can enable privilege escalation attacks. Allowing writes to directories containing executables in `$PATH`, system configuration directories, or user shell configuration files such as `.bashrc` or `.zshrc` can lead to code execution in different security contexts when other users or system processes access these files.
- **Linux sandbox strength**: the Linux implementation provides strong filesystem and network isolation but includes an `enableWeakerNestedSandbox` mode that enables it to work inside Docker environments without privileged namespaces, or on Linux hosts where unprivileged user namespaces are disabled by sysctl. This option considerably weakens security and should only be used when additional isolation is otherwise enforced.
- **Settings files protected**: the sandbox automatically denies write access to Claude Code's `settings.json` files at every scope and to the managed settings directory, so a sandboxed command cannot modify its own policy.

### Platform and tool compatibility

- **Platform support**: supports macOS, Linux, and WSL2. WSL1 and native Windows are not supported.
- **Performance overhead**: minimal, but some filesystem operations may be slightly slower.
- **Tool compatibility**: some tools that require specific system access patterns may need configuration adjustments, or may need to be run outside the sandbox.

### Scope

The sandbox isolates Bash subprocesses. Other tools operate under different boundaries:

- **Built-in file tools**: Read, Edit, and Write use the permission system directly rather than running through the sandbox. See [Permissions](https://code.claude.com/docs/en/permissions).
- **Computer use**: when Claude opens apps and controls your screen, it runs on your actual desktop rather than in an isolated environment. Per-app permission prompts gate each application. See [computer use in the CLI](https://code.claude.com/docs/en/computer-use) or [computer use in Desktop](https://code.claude.com/docs/en/desktop).
- **Environment variables**: sandboxed Bash commands inherit the parent process environment by default, including any credentials set there. To strip Anthropic and cloud provider credentials from subprocesses, set [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](https://code.claude.com/docs/en/env-vars).
- **Subagents**: [subagents](https://code.claude.com/docs/en/sub-agents) run in the same process as the parent session and use the same sandbox configuration. Bash commands inside a subagent are sandboxed when sandboxing is enabled in the parent session.

> Effective sandboxing requires **both** filesystem and network isolation. Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys. Without filesystem isolation, a compromised agent could backdoor system resources to gain network access. When you widen the defaults, check that an `allowWrite` path, a broad `allowedDomains` entry, or an `excludedCommands` exception does not undo a restriction on the other side.

**Source**: https://code.claude.com/docs/en/sandboxing
**Last Updated**: 2026-06-13
**Status**: Active
