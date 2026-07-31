---
tags:
  - resource
  - documentation
  - claude_code
  - jetbrains
  - ide
keywords:
  - jetbrains plugin
  - intellij pycharm webstorm
  - claude code ide integration
  - /ide command
  - diff viewing selection sharing
  - wsl2 mirrored networking
  - remote development plugin
  - auto-edit security
topics:
  - Claude Code
  - JetBrains
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/jetbrains
access_control_group: ["general"]
---

# Claude Code — JetBrains IDE Plugin

## Overview

Claude Code integrates with JetBrains IDEs through a dedicated plugin that adds interactive diff viewing, selection-context sharing, file-reference shortcuts, and diagnostic sharing on top of the `claude` CLI. The plugin does **not** bundle its own CLI — it runs the `claude` command in the IDE's integrated terminal and connects to it, so you install both the CLI and the plugin.

This procedure note covers the supported IDEs and feature set, the two-piece installation, how to use the plugin from the IDE or an external terminal (the `/ide` command), `/config` and plugin settings, special configurations for Remote Development and WSL2, troubleshooting, and the auto-edit security consideration.

## Supported IDEs

The Claude Code plugin works with most JetBrains IDEs, including IntelliJ IDEA, PyCharm, Android Studio, WebStorm, PhpStorm, and GoLand.

## Features

- **Quick launch**: use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open Claude Code directly from your editor, or click the Claude Code button in the UI.
- **Diff viewing**: code changes can be displayed directly in the IDE diff viewer instead of the terminal.
- **Selection context**: the current selection or tab in the IDE is automatically shared with Claude Code. `Read` deny rules block this sharing for matching files (see [Deny-First](../../term_dictionary/term_deny_first.md)).
- **File reference shortcuts**: use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Linux/Windows) to insert file references such as `@src/auth.ts#L1-99`.
- **Diagnostic sharing**: diagnostic errors from the IDE, such as lint and syntax errors, are automatically shared with Claude as you work.

## Installation

The plugin runs the `claude` command in your IDE's integrated terminal and connects to it. It does not bundle its own copy of the CLI, so install both pieces:

1. **Install the Claude Code CLI** — follow the quickstart to install the CLI if you haven't already. The plugin shows a "Cannot launch Claude Code" notification when `claude` isn't on your PATH.
2. **Install the JetBrains plugin** — install the Claude Code plugin from the JetBrains Marketplace and restart your IDE.

If `claude` is installed somewhere your IDE can't find, set the full path in the plugin's Claude command setting (see Plugin settings below).

Claude Code works with any paid Claude subscription (Pro, Max, Team, or Enterprise) or a Claude Console account, and no API key is required. You'll be prompted to log in the first time you run `claude`. After installing the plugin, you may need to restart your IDE completely for it to take effect.

## Usage

### From your IDE

Run `claude` from your IDE's integrated terminal, and all integration features will be active.

### From external terminals

Use the `/ide` command in any external terminal to connect Claude Code to your JetBrains IDE and activate all features:

```text theme={null}
/ide
```

If you want Claude to have access to the same files as your IDE, start Claude Code from the same directory as your IDE project root.

## Configuration

### Claude Code settings

Configure IDE integration through Claude Code's settings:

1. Run `claude`
2. Enter the `/config` command
3. Set the diff tool to `auto` to show diffs in the IDE, or `terminal` to keep them in the terminal

### Plugin settings

Configure the Claude Code plugin by going to **Settings → Tools → Claude Code [Beta]**. The general settings are:

- **Claude command**: specify a custom command to run Claude, for example `claude`, `/usr/local/bin/claude`, or `npx @anthropic-ai/claude-code`.
- **Suppress notification for Claude command not found**: skip notifications about not finding the Claude command.
- **Enable using Option+Enter for multi-line prompts**: macOS only. When enabled, Option+Enter inserts new lines in Claude Code prompts. Disable if the Option key is being captured unexpectedly. Requires a terminal restart.
- **Enable automatic updates**: automatically check for and install plugin updates, applied on restart.

For WSL users, set `wsl -d Ubuntu -- bash -lic "claude"` as your Claude command (replace `Ubuntu` with your WSL distribution name).

**ESC key configuration** — if the ESC key doesn't interrupt Claude Code operations in JetBrains terminals, go to **Settings → Tools → Terminal** and either uncheck "Move focus to the editor with Escape", or click "Configure terminal keybindings" and delete the "Switch focus to Editor" shortcut, then apply the changes.

## Special configurations

### Remote development

When using JetBrains Remote Development, you must install the plugin in the remote host via **Settings → Plugin (Host)**. The plugin must be installed on the remote host, not on your local client machine (see [SSH](../../term_dictionary/term_ssh.md) for the remote-host development model).

### WSL configuration

If you're using Claude Code on WSL2 with a JetBrains IDE and see "No available IDEs detected", the cause is usually WSL2's NAT networking or Windows Firewall blocking the connection between WSL2 and the IDE running on the Windows host. WSL1 uses the host's network directly and isn't affected.

**Allow WSL2 traffic through Windows Firewall** (the recommended fix because it keeps your existing WSL2 networking mode):

1. Find your WSL2 IP address — from inside your WSL shell, run `hostname -I` and note the subnet (for example `172.21.123.45` is in `172.21.0.0/16`).
2. Create a firewall rule — open PowerShell as Administrator and run the following, adjusting the IP range to match your subnet:

```powershell theme={null}
New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
```

3. Restart your IDE and Claude Code so the new rule takes effect.

**Switch WSL2 to mirrored networking** (requires Windows 11 22H2 or later; on Windows 10 use the firewall rule above instead). Add this to `.wslconfig` in your Windows user directory, then restart WSL with `wsl --shutdown` from PowerShell:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

## Troubleshooting

- **Plugin not working** (installed but features don't appear): ensure you're running Claude Code from the project root directory; check that the JetBrains plugin is enabled in IDE settings; completely restart the IDE (you may need to do this multiple times); for Remote Development, ensure the plugin is installed in the remote host.
- **IDE not detected** ("No available IDEs detected"): verify the plugin is installed and enabled; restart the IDE completely; check you're running Claude Code from the integrated terminal; for WSL users, see the WSL configuration above.
- **Command not found** (clicking the Claude icon shows "command not found"): verify Claude Code is installed by running `claude --version` in a terminal; configure the Claude command path in plugin settings; for WSL users, use the WSL command format above.

## Security considerations

When Claude Code runs in a JetBrains IDE with auto-edit permissions enabled, it may be able to modify IDE configuration files that can be automatically executed by your IDE. This may increase the risk of running Claude Code in auto-edit mode and allow bypassing Claude Code's permission prompts for bash execution. When running in JetBrains IDEs, consider using manual approval mode for edits, taking extra care to ensure Claude is only used with trusted prompts, and being aware of which files Claude Code has access to modify. The permission-mode concepts behind this choice are documented in [permission modes](https://code.claude.com/docs/en/permission-modes).

**Source**: https://code.claude.com/docs/en/jetbrains
**Last Updated**: 2026-06-13
**Status**: Active
