---
tags:
  - resource
  - documentation
  - claude_code
  - setup
  - installation
keywords:
  - install claude code
  - native installer
  - system requirements
  - windows wsl
  - alpine musl
  - verify installation
  - claude doctor
  - authenticate account
topics:
  - Claude Code
  - Setup
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/setup
access_control_group: ["general"]
---

# Claude Code — Install Claude Code

## Overview

This note is the install procedure for Claude Code: the supported platforms and hardware, the recommended native installer (plus Homebrew, WinGet, and Linux package managers), the Windows native-vs-WSL decision, the extra dependencies musl-based distributions need, how to verify the install, and the account prerequisites for authentication. Native installations are the recommended path and auto-update in the background; Homebrew, WinGet, and Linux package-manager installs require manual updates.

For version pinning, the signed Linux repositories, the npm install path, and binary-integrity verification, see [Advanced installation and verification](cc_advanced_install_and_verification.md). For updates and release channels see [Update and release channels](cc_update_and_release_channels.md). If anything fails, see [Install diagnostics](cc_install_diagnostics.md) and the [Install failures reference](cc_install_failures_reference.md).

## System Requirements

Claude Code runs on the following platforms and configurations:

- **Operating system**:
  - macOS 13.0+
  - Windows 10 1809+ or Windows Server 2019+
  - Ubuntu 20.04+
  - Debian 10+
  - Alpine Linux 3.19+
- **Hardware**: 4 GB+ RAM, x64 or ARM64 processor
- **Network**: internet connection required. See [network configuration](https://code.claude.com/docs/en/network-config).
- **Shell**: Bash, Zsh, PowerShell, or CMD.
- **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

### Additional dependencies

- **ripgrep**: usually included with Claude Code. If search fails, see [search troubleshooting](https://code.claude.com/docs/en/troubleshooting#search-and-discovery-issues).

## Install Claude Code

Use one of the following methods. The native install is recommended and auto-updates in the background.

**Native install — macOS, Linux, WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Native install — Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Native install — Windows CMD:**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

**Homebrew** offers two casks: `brew install --cask claude-code` (the `claude-code` cask) tracks the **stable** release channel (typically about a week behind, skipping releases with major regressions), and `claude-code@latest` tracks the **latest** channel. **WinGet** uses `winget install Anthropic.ClaudeCode`. Homebrew and WinGet installations do not auto-update. You can also install with [apt, dnf, or apk](cc_advanced_install_and_verification.md) on Debian, Fedora, RHEL, and Alpine.

After installation completes, open a terminal in the project you want to work in and start Claude Code with `claude`.

### Set up on Windows

You can run Claude Code natively on Windows or inside WSL. Pick based on where your projects are located and which features you need:

| Option | Requires | [Sandboxing](https://code.claude.com/docs/en/sandboxing) | When to use |
| --- | --- | --- | --- |
| Native Windows | None; Git for Windows is optional | Not supported | Windows-native projects and tools |
| WSL 2 | WSL 2 enabled | Supported | Linux toolchains or sandboxed command execution |
| WSL 1 | WSL 1 enabled | Not supported | If WSL 2 is unavailable |

**Native Windows**: run the install command from PowerShell or CMD — you do not need to run as Administrator. [Git for Windows](https://git-scm.com/downloads/win) is optional; it enables the Bash tool by providing Git Bash. Without Git for Windows, Claude Code runs shell commands via the PowerShell tool. With Git for Windows, Claude Code uses Git Bash for the Bash tool; if it can't find Git Bash, set `CLAUDE_CODE_GIT_BASH_PATH` in your [settings.json](https://code.claude.com/docs/en/settings). When Git for Windows is installed, the PowerShell tool is rolling out progressively as an additional option (opt in with `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`).

**WSL**: open your WSL distribution and run the Linux installer above. You install and launch `claude` inside the WSL terminal, not from PowerShell or CMD. WSL setups do not need Git for Windows.

### Alpine Linux and musl-based distributions

The native installer on Alpine and other musl/uClibc-based distributions requires `libgcc`, `libstdc++`, and `ripgrep`. Install these using your distribution's package manager, then set `USE_BUILTIN_RIPGREP=0`. On Alpine:

```bash
apk add libgcc libstdc++ ripgrep
```

Then set `USE_BUILTIN_RIPGREP` to `"0"` in the `env` key of your [`settings.json`](https://code.claude.com/docs/en/settings) file.

## Verify Your Installation

After installing, confirm Claude Code is working:

```bash
claude --version
```

If this fails with `command not found` or another error, see [Install diagnostics](cc_install_diagnostics.md) and the [Install failures reference](cc_install_failures_reference.md). For a more detailed check of your installation and configuration, run `claude doctor` (debug-your-config tooling covered separately at [debug your config](https://code.claude.com/docs/en/troubleshooting#get-more-help)).

## Authenticate

Claude Code requires a **Pro, Max, Team, Enterprise, or Console** account. The free Claude.ai plan does not include Claude Code access. You can also use Claude Code with a third-party API provider like [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry).

After installing, log in by running `claude` and following the browser prompts. See [Authentication](https://code.claude.com/docs/en/authentication) for all account types and team setup options.

**Source**: https://code.claude.com/docs/en/setup
**Last Updated**: 2026-06-13
**Status**: Active
