---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - setup
keywords:
  - sandboxed bash tool setup
  - sandbox command panel
  - sandbox enabled setting
  - failifunavailable
  - bubblewrap socat install
  - seccomp filter
  - ubuntu 24.04 apparmor bwrap
  - wsl2 sandbox
  - settings.local.json
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/sandboxing
access_control_group: ["general"]
---

# Claude Code — Set Up the Sandboxed Bash Tool

## Overview

The Bash sandbox lets Claude run most shell commands without stopping to ask permission: instead of approving each command, you define which files and network domains commands can touch, and the operating system enforces that boundary for every Bash command and its child processes. This note is the enable/setup procedure — running `/sandbox`, choosing an approval mode, running a first sandboxed command, and the Linux/WSL2 dependency setup. The sandbox is built into Claude Code and runs on macOS, Linux, and WSL2; native Windows is not supported, so on Windows you run Claude Code inside a WSL2 distribution.

On macOS there is nothing to install — sandboxing uses the built-in Seatbelt framework. On Linux and WSL2 the sandbox relies on two packages (covered below), but even before installing them you can start with `/sandbox`, because its panel shows whether anything is missing.

## Get started

### Run `/sandbox`

Start a Claude Code session and run the `/sandbox` command:

```text
/sandbox
```

This opens the sandbox panel with three tabs:

- **Mode** — choose how sandboxed commands are approved (next step).
- **Overrides** — choose whether commands that fail under the sandbox can fall back to running unsandboxed. This is the `allowUnsandboxedCommands` setting.
- **Config** — view the resolved sandbox settings.

If the panel shows only a **Dependencies** tab, a required package is missing. Install it as described in [Set up Linux and WSL2](#set-up-linux-and-wsl2), restart Claude Code, and run `/sandbox` again.

### Choose a mode

On the **Mode** tab, select **auto-allow** or **regular permissions**. Auto-allow runs sandboxed commands without prompting; regular permissions keeps the regular permission prompts even when commands are sandboxed. See [Sandbox Modes](cc_sandbox_modes.md) for which commands still prompt in auto-allow mode.

### Run a Bash command

Ask Claude to run a command, such as a build or a test suite. By default, commands inside the sandbox can write only to the working directory and the session temp directory. The first time a command needs a new network domain, Claude Code prompts for approval. Commands that cannot run sandboxed fall back to the regular permission flow.

### Where the mode is stored, and enabling more broadly

Selecting a mode in the panel writes to your project's local settings at `.claude/settings.local.json`, which apply to the current project and are not checked into git. To enable the sandbox across all of your projects, set `sandbox.enabled` to `true` in your user settings at `~/.claude/settings.json`. To enforce sandboxing for every developer in an organization, use managed settings (see [Enforce the Sandbox Across an Organization](cc_sandbox_org_enforcement.md)).

By default, if the sandbox cannot start because dependencies are missing or the platform is unsupported, Claude Code shows a warning and runs commands without sandboxing. To make this a hard failure instead, set `sandbox.failIfUnavailable` to `true`. This is intended for managed deployments that require sandboxing as a security gate.

## Set up Linux and WSL2

On Linux and WSL2, the sandbox relies on two packages:

- `bubblewrap` — the unprivileged sandboxing tool that enforces filesystem isolation.
- `socat` — the relay used to route network traffic through the sandbox proxy.

Install them with your distribution's package manager. On Ubuntu/Debian:

```bash
sudo apt-get install bubblewrap socat
```

On Fedora, use `sudo dnf install bubblewrap socat`.

After installing, the **Dependencies** tab in `/sandbox` shows whether `ripgrep`, `bubblewrap`, `socat`, and the seccomp filter are available on your platform. Ripgrep is bundled with the native Claude Code binary. The seccomp filter is optional and adds Unix domain socket blocking; install it with `npm install -g @anthropic-ai/sandbox-runtime` if it is missing. When a required dependency is missing, the Dependencies tab is the only tab shown until you install it. The dependency check runs at startup, so **restart Claude Code after installing packages** for `/sandbox` to detect them.

### Ubuntu 24.04 and later: allow bubblewrap to create user namespaces

On Ubuntu 24.04 and later, the default AppArmor policy prevents bubblewrap from creating the user namespaces it needs for isolation. To check whether your environment enforces this restriction (including inside WSL2), run `sysctl kernel.apparmor_restrict_unprivileged_userns`. If the key does not exist or returns `0`, skip this step. If it returns `1`, add an AppArmor profile that grants `bwrap` this capability:

```bash
sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
abi <abi/4.0>,
include <tunables/global>

profile bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
  include if exists <local/bwrap>
}
EOF
```

The profile applies only to `bwrap` itself, not to the commands it runs inside the sandbox. Reload AppArmor to apply it with `sudo systemctl reload apparmor`.

### WSL2 notes

Check your WSL version with `wsl -l -v` from PowerShell. If you see `Sandboxing requires WSL2`, your distribution is running WSL1 — upgrade it to WSL2 or run Claude Code without sandboxing.

On WSL2, sandboxed commands cannot launch Windows binaries such as `cmd.exe`, `powershell.exe`, or anything under `/mnt/c/`. WSL hands these off to the Windows host over a Unix socket, which the sandbox blocks. If a command needs to invoke a Windows binary, add it to `excludedCommands` so it runs outside the sandbox.

**Source**: https://code.claude.com/docs/en/sandboxing
**Last Updated**: 2026-06-13
**Status**: Active
