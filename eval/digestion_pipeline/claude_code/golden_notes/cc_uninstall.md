---
tags:
  - resource
  - documentation
  - claude_code
  - setup
  - uninstall
keywords:
  - uninstall claude code
  - remove claude code binary
  - conflicting installation
  - remove configuration files
  - npm uninstall
  - homebrew uninstall cask
  - remove ~/.claude
  - mcp server configurations
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

# Claude Code — Uninstall

## Overview

This note is the per-install-method procedure for removing Claude Code. To uninstall, follow the steps that match how you installed it (native installer, Homebrew, WinGet, apt/dnf/apk, or npm), then optionally remove the configuration files. If `claude` still runs after you remove the binary, you likely have a second installation or a leftover shell alias from an older installer — see [Check for conflicting installations](cc_install_diagnostics.md) to find and remove it.

Removing the binary and the configuration files are separate steps. Deleting configuration is destructive: it removes all your settings, allowed tools, MCP server configurations, and session history, and several Anthropic editor integrations recreate `~/.claude/` if they are still installed.

## Remove the binary by install method

Follow the instructions for your installation method.

### Native installation

Remove the Claude Code binary and version files. On macOS, Linux, and WSL:

```bash theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

On Windows PowerShell, remove `$env:USERPROFILE\.local\bin\claude.exe` and the `$env:USERPROFILE\.local\share\claude` directory with `Remove-Item ... -Force` (use `-Recurse -Force` for the directory).

### Homebrew installation

Remove the Homebrew cask you installed. If you installed the stable cask, run `brew uninstall --cask claude-code`. If you installed the latest cask, run `brew uninstall --cask claude-code@latest` instead.

### WinGet installation

Remove the WinGet package:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### apt / dnf / apk

Remove the package and the repository configuration. For apt:

```bash theme={null}
sudo apt remove claude-code
sudo rm /etc/apt/sources.list.d/claude-code.list /etc/apt/keyrings/claude-code.asc
```

For dnf, run `sudo dnf remove claude-code` then `sudo rm /etc/yum.repos.d/claude-code.repo`. For apk, run `apk del claude-code`, delete the repository line from `/etc/apk/repositories`, and `rm /etc/apk/keys/claude-code.rsa.pub`.

### npm

Remove the global npm package:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

## Remove configuration files

Removing configuration files will delete all your settings, allowed tools, MCP server configurations, and session history.

The VS Code extension, the JetBrains plugin, and the Desktop app also write to `~/.claude/`. If any of them is still installed, the directory is recreated the next time it runs. To remove Claude Code completely, uninstall the VS Code extension, the JetBrains plugin, and the Desktop app before deleting these files.

To remove Claude Code settings and cached data (macOS, Linux, WSL):

```bash theme={null}
# Remove user settings and state
rm -rf ~/.claude
rm ~/.claude.json

# Remove project-specific settings (run from your project directory)
rm -rf .claude
rm -f .mcp.json
```

On Windows PowerShell, use `Remove-Item` on `$env:USERPROFILE\.claude` (with `-Recurse -Force`), `$env:USERPROFILE\.claude.json`, the project `.claude` directory, and `.mcp.json`.

**Source**: https://code.claude.com/docs/en/setup
**Last Updated**: 2026-06-13
**Status**: Active
