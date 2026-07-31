---
tags:
  - resource
  - documentation
  - claude_code
  - installation
  - troubleshooting
keywords:
  - install diagnostics
  - diagnostic checks
  - verify your path
  - conflicting installations
  - directory permissions
  - verify the binary works
  - downloads.claude.ai
  - claude doctor
topics:
  - Claude Code
  - Installation
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/troubleshoot-install
access_control_group: ["general"]
---

# Claude Code — Install Diagnostic Checks

## Overview

When a Claude Code install fails or `claude` won't run and the symptom isn't in the [error-router table](https://code.claude.com/docs/en/troubleshoot-install), work through five ordered diagnostic checks to narrow down the cause. Each check isolates one failure layer: network reachability of the download host, whether the install directory is on your `PATH`, whether multiple conflicting installations exist, whether the install directories are writable, and whether the installed binary can actually execute. The checks are designed to be run top-to-bottom — later checks assume earlier ones passed (for example, "Verify the binary works" assumes `claude` is on your `PATH`).

This note is the diagnostic procedure only. For the symptom-to-fix lookup of specific install failures, see [`cc_install_failures_reference`](cc_install_failures_reference.md); for the install procedure itself, see [`cc_install`](cc_install.md). If you exhaust the checks, the [Still stuck](#still-stuck) escalation path closes the procedure.

## Check network connectivity

The installer downloads from `downloads.claude.ai`. Verify you can reach it:

```bash theme={null}
curl -sI https://downloads.claude.ai/claude-code-releases/latest
```

In PowerShell, run `curl.exe -sI` instead. PowerShell aliases `curl` to `Invoke-WebRequest`, which rejects the `-sI` flags.

An `HTTP/2 200` line means you reached the server. If you see no output, `Could not resolve host`, or a connection timeout, your network is blocking the connection. Common causes are corporate firewalls or proxies blocking `downloads.claude.ai`, regional network restrictions (try a VPN or alternative network), and TLS/SSL issues (update your system's CA certificates, or check whether `HTTPS_PROXY` is configured).

If you're behind a corporate proxy, set `HTTPS_PROXY` and `HTTP_PROXY` to your proxy's address before installing — ask your IT team for the proxy URL, or check your browser's proxy settings. On macOS/Linux this is `export HTTP_PROXY=...` / `export HTTPS_PROXY=...` before running the install script; in Windows PowerShell it is `$env:HTTP_PROXY = '...'` / `$env:HTTPS_PROXY = '...'` before `irm https://claude.ai/install.ps1 | iex`.

## Verify your PATH

If installation succeeded but you get a `command not found` or `not recognized` error when running `claude`, the install directory isn't in your `PATH`. Your shell searches for programs in the directories listed in `PATH`, and the installer places `claude` at `~/.local/bin/claude` on macOS/Linux or `%USERPROFILE%\.local\bin\claude.exe` on Windows.

> The VS Code extension does not place `claude` at this location — it bundles a private copy of the CLI inside the extension directory for its own chat panel and does not add it to `PATH`. If you have installed only the extension, `~/.local/bin/claude` will not exist; run the standalone install to use `claude` from a terminal.

Check whether the install directory is in your `PATH` by listing your `PATH` entries and filtering for `local/bin`:

```bash theme={null}
echo $PATH | tr ':' '\n' | grep -Fx "$HOME/.local/bin"
```

If this prints `/Users/you/.local/bin` or `/home/you/.local/bin`, the directory is in your `PATH` and you can skip to [Check for conflicting installations](#check-for-conflicting-installations). If there's no output, add it to your shell configuration. For Zsh (the macOS default), append `export PATH="$HOME/.local/bin:$PATH"` to `~/.zshrc` and `source` it; for Bash (the Linux default), do the same with `~/.bashrc`; alternatively, close and reopen your terminal. For other shells such as fish or Nushell, add `~/.local/bin` to your `PATH` using that shell's own configuration syntax, then restart your terminal. On Windows, filter your `PATH` (`$env:PATH -split ';' | Select-String '\.local\\bin'` in PowerShell, or `echo %PATH% | findstr /i "local\bin"` in CMD); if empty, add `%USERPROFILE%\.local\bin` to your User `PATH` (via `[Environment]::SetEnvironmentVariable(...)` in PowerShell or System Settings → Environment Variables in CMD) and restart the terminal. In all cases, verify the fix with `claude --version`.

## Check for conflicting installations

Multiple Claude Code installations can cause version mismatches or unexpected behavior. List every `claude` binary on your `PATH`:

```bash theme={null}
which -a claude
```

If this prints nothing, no `claude` is on your `PATH` yet — go back to [Verify your PATH](#verify-your-path). On Windows PowerShell, use `where.exe claude` instead.

A `claude` binary can come from three locations. `~/.local/bin/claude` is the native installer, `~/.claude/local/` is a legacy local npm install created by older versions of Claude Code, and the npm global list (`npm -g ls @anthropic-ai/claude-code`) shows a `-g` install. Inspect each with `ls -la ~/.local/bin/claude`, `ls -la ~/.claude/local/`, and the `npm -g ls` command; if an `ls` prints `No such file or directory`, that's not an error — it just means nothing is installed there, so move to the next check.

If you find multiple installations, keep only one. The native install at `~/.local/bin/claude` on macOS/Linux (or `%USERPROFILE%\.local\bin\claude.exe` on Windows) is recommended. Remove the extras: `npm uninstall -g @anthropic-ai/claude-code` for an npm global install, `rm -rf ~/.claude/local` (or `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\local"` on Windows) for the legacy local npm install, `brew uninstall --cask claude-code` for a Homebrew install on macOS, and `winget uninstall Anthropic.ClaudeCode` for a WinGet install on Windows. (The full per-method removal procedure is in [`cc_uninstall`](cc_uninstall.md).)

## Check directory permissions

The installer needs write access to `~/.local/bin/` and `~/.claude/` on macOS and Linux. On Windows the install location is under `%USERPROFILE%`, which is writable by your user by default, so this section rarely applies there.

Check whether the directories are writable:

```bash theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

If either directory isn't writable, create the install directory and set your user as the owner:

```bash theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

## Verify the binary works

If `claude --version` prints a version but `claude` crashes or hangs on startup, run these checks to narrow down the cause. If `claude --version` says `command not found`, go to [Verify your PATH](#verify-your-path) first — the checks below assume `claude` is on your `PATH`.

First, confirm the binary exists and is executable with `ls -la "$(command -v claude)"` (on Windows, `Get-Command claude | Select-Object Source`). On Linux, check for missing shared libraries:

```bash theme={null}
ldd "$(command -v claude)" | grep "not found"
```

If `ldd` shows missing libraries, you may need to install system packages. On Alpine Linux and other musl-based distributions, see the Alpine Linux setup notes in [`cc_install`](cc_install.md). Finally, confirm the binary can execute by running `claude --version` again.

## Still stuck

If none of the above resolves your issue:

1. Check the [GitHub repository](https://github.com/anthropics/claude-code/issues) for known issues, or open a new one with your operating system, the install command you ran, and the full error output.
2. If `claude --version` works but something else is wrong, run `claude doctor` for an automated diagnostic report.
3. If you can start a session, use `/feedback` inside Claude Code to report the problem.

The `claude doctor` command and `/doctor` slash command are documented under [Debug your configuration](https://code.claude.com/docs/en/debug-your-config). For login and authentication failures (a common downstream problem once the binary itself runs), see [`cc_login_authentication_troubleshooting`](cc_login_authentication_troubleshooting.md).

**Source**: https://code.claude.com/docs/en/troubleshoot-install
**Last Updated**: 2026-06-13
**Status**: Active
