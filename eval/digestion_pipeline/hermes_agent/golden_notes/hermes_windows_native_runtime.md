---
tags:
  - resource
  - documentation
  - hermes_agent
  - windows
  - runtime
keywords:
  - windows native runtime
  - git bash resolution
  - utf-8 console shim
  - ctrl+enter newline
  - editor notepad default
  - process management internals
  - windows common pitfalls
  - feature matrix native vs wsl2
topics:
  - Hermes Agent
  - Windows Native
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/windows-native
access_control_group: ["general"]
---

# Hermes Agent — Windows Native Runtime

## Overview

This note is the **day-to-day native-Windows runtime surface** of Hermes Agent: how the harness actually runs shell commands, renders Unicode, edits text, and manages its gateway process once it is installed (the install/deploy arc lives in [hermes_install_windows_native](hermes_install_windows_native.md)). Everything except the dashboard's embedded terminal pane runs natively on Windows 10/11 — no WSL, no Cygwin, no Docker. The page documents the Windows-specific knobs you touch when something surprises you: Git Bash `bash.exe` resolution for the terminal tool, the `configure_windows_stdio` UTF-8/CP65001 shim, the `EDITOR=notepad` default, `Ctrl+Enter` newline, the `agent-browser` `.cmd` resolution, Windows environment variables, the `os.kill(pid, 0)`→`CTRL_C_EVENT` footgun, and a common-pitfalls table. For a real POSIX environment instead, see [hermes_install_windows_wsl2](hermes_install_windows_wsl2.md).

## Feature matrix

Everything except the dashboard's embedded terminal pane runs natively on Windows.

| Feature | Native Windows | WSL2 |
|---|---|---|
| CLI (`hermes chat`, `hermes setup`, `hermes gateway`, …) | ✓ | ✓ |
| Interactive TUI (`hermes --tui`) | ✓ | ✓ |
| Messaging gateway (Telegram, Discord, Slack, WhatsApp, 15+ platforms) | ✓ | ✓ |
| Cron scheduler | ✓ | ✓ |
| Browser tool (Chromium via Node) | ✓ | ✓ |
| MCP servers (stdio and HTTP) | ✓ | ✓ |
| Local Ollama / LM Studio / llama-server | ✓ | ✓ (via WSL networking) |
| Web dashboard (sessions, jobs, metrics, config) | ✓ | ✓ |
| Dashboard `/chat` embedded terminal pane | ✗ (needs POSIX PTY) | ✓ |
| Auto-start at login | ✓ (schtasks) | ✓ (systemd) |

The dashboard's `/chat` tab embeds a real terminal via a POSIX PTY (`ptyprocess`). Native Windows has no equivalent primitive; Python's `pywinpty` / Windows ConPTY would work but is a separate implementation — treat as future work. **The rest of the dashboard works natively** — only that one tab shows a "use WSL2 for this" banner. (The dashboard feature itself is documented in SP10 `hermes_web_dashboard`; the WSL2 path in [hermes_install_windows_wsl2](hermes_install_windows_wsl2.md).)

## How Hermes runs shell commands on Windows

Hermes's terminal tool runs commands through **Git Bash**, same strategy Claude Code uses. This sidesteps the POSIX-vs-Windows gap without rewriting every tool.

Resolution order for `bash.exe`:

1. `HERMES_GIT_BASH_PATH` environment variable if set.
2. `%LOCALAPPDATA%\hermes\git\usr\bin\bash.exe` (installer-managed PortableGit).
3. `%LOCALAPPDATA%\hermes\git\bin\bash.exe` (older Git-for-Windows layout).
4. System Git-for-Windows install (`%ProgramFiles%\Git\bin\bash.exe`, etc.).
5. MSYS2, Cygwin, or any `bash.exe` on PATH as a last resort.

The installer sets `HERMES_GIT_BASH_PATH` explicitly so fresh PowerShell sessions don't have to re-discover. Override it if you want Hermes to use a specific bash — for example, your system Git Bash or a WSL-hosted bash via a symlink.

**Pitfall:** MinGit's layout is different from the full Git-for-Windows installer — bash lives under `usr\bin\bash.exe`, not `bin\bash.exe`. Hermes checks both. If you're manually unpacking a MinGit zip, make sure you pick the **non-busybox** variant (`MinGit-*-64-bit.zip`, not `MinGit-*-busybox*.zip`) — busybox builds ship `ash` instead of `bash` and most coreutils are missing.

## UTF-8 console on Windows

Python's default stdio on Windows uses the console's active code page (usually cp1252 or cp437). Hermes's banner, slash-command list, tool feed, Rich panels, and skill descriptions all contain Unicode. Without intervention, any of that crashes with `UnicodeEncodeError: 'charmap' codec can't encode character…`.

The fix is in `hermes_cli/stdio.py::configure_windows_stdio()`, called early in every entry point (`cli.py::main`, `hermes_cli/main.py::main`, `gateway/run.py::main`). It:

1. Flips the console code page to CP_UTF8 (65001) via `kernel32.SetConsoleCP` / `SetConsoleOutputCP`.
2. Reconfigures `sys.stdout` / `sys.stderr` / `sys.stdin` to UTF-8 with `errors='replace'`.
3. Sets `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` (via `setdefault`, so explicit user values win) so child Python subprocesses inherit UTF-8.
4. Sets `EDITOR=notepad` if neither `EDITOR` nor `VISUAL` is set (see the Editor section below).

Idempotent. No-op on non-Windows.

**Opt out:** `HERMES_DISABLE_WINDOWS_UTF8=1` in the environment falls back to the legacy cp1252 stdio path. Useful for bisecting an encoding bug; unlikely to be the right setting in normal operation.

## The editor (`Ctrl-X Ctrl-E`, `/edit`)

Pre-#21561, pressing `Ctrl-X Ctrl-E` or typing `/edit` silently did nothing on Windows. prompt_toolkit has a hardcoded POSIX-absolute fallback list (`/usr/bin/nano`, `/usr/bin/pico`, `/usr/bin/vi`, …) that never resolves on Windows — even with full Git for Windows installed.

Hermes's Windows stdio shim now sets `EDITOR=notepad` as a default. Notepad ships with every Windows install and works as a blocking editor — `subprocess.call(["notepad", file])` blocks until the window closes.

**User overrides still win** (they're checked before the setdefault):

| Editor | PowerShell command |
|---|---|
| VS Code | `$env:EDITOR = "code --wait"` |
| Notepad++ | `$env:EDITOR = "'C:\Program Files\Notepad++\notepad++.exe' -multiInst -nosession"` |
| Neovim | `$env:EDITOR = "nvim"` |
| Helix | `$env:EDITOR = "hx"` |

The `--wait` flag on VS Code is critical — without it the editor returns immediately and Hermes gets a blank buffer back. Set it permanently in your PowerShell profile:

```powershell
# In $PROFILE
$env:EDITOR = "code --wait"
```

Or as a User environment variable in System Settings so every new shell picks it up.

## `Ctrl+Enter` for newline in the CLI

Windows Terminal passes `Ctrl+Enter` through as a dedicated key sequence. Hermes binds it to "insert newline" so you can compose multi-line prompts in the CLI without falling back to `Esc`-then-`Enter`. Works in Windows Terminal, VS Code integrated terminal, and any modern Windows console host that honors VT escape sequences.

On legacy `cmd.exe` consoles `Ctrl+Enter` collapses to plain `Enter` — use `Esc Enter` instead, or upgrade to Windows Terminal (it's free and installed by default on Windows 11).

## Browser tool

The browser tool uses `agent-browser` (a Node helper) to drive Chromium. On Windows:

- The installer puts `agent-browser` on PATH via npm.
- `shutil.which("agent-browser", path=...)` picks up the `.cmd` shim automatically — `CreateProcessW` can't execute an extensionless shebang, so Hermes always resolves to the `.CMD` wrapper. Don't manually invoke the shebang script; always go through the `.cmd`.
- Playwright Chromium is auto-installed on first run (`npx playwright install chromium`). If installation fails, `hermes doctor` surfaces it with a fix-it hint.

(Browser tool behavior in general is owned by SP08 — this note documents only the Windows `.cmd` resolution specifics.)

## Running Hermes on Windows — practical notes

### PATH after install

The installer adds `%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts` to your **User PATH** via `[Environment]::SetEnvironmentVariable`. Existing terminals don't pick this up — open a new PowerShell window (or Windows Terminal tab) after installation. Close-and-reopen, don't `$env:PATH += …` by hand unless you know what you're doing. Verify:

```powershell
Get-Command hermes        # should print C:\Users\<you>\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe
hermes --version
```

### Environment variables

Hermes honors both `$env:X` (process-scope) and User environment variables (permanent, set in System Properties → Environment Variables). Setting API keys in `%LOCALAPPDATA%\hermes\.env` (your `HERMES_HOME`) is the normal path — same as Linux:

```
OPENROUTER_API_KEY=sk-or-...
TELEGRAM_BOT_TOKEN=...
```

Don't put secrets in User environment variables unless you specifically want every Windows process to see them (it isn't what you want).

### Windows-specific env vars

These only affect native Windows installs:

| Variable | Effect |
|---|---|
| `HERMES_GIT_BASH_PATH` | Override bash.exe discovery. Point at any bash — full Git-for-Windows, WSL bash via symlink, MSYS2, Cygwin. The installer sets this automatically. |
| `HERMES_DISABLE_WINDOWS_UTF8` | Set to `1` to disable the UTF-8 stdio shim and fall back to the locale code page. Useful for bisecting an encoding bug. |
| `EDITOR` / `VISUAL` | Your editor for `/edit` and `Ctrl-X Ctrl-E`. Hermes defaults to `notepad` if both are unset. |

## Process management internals

This is background material — skip unless you're debugging an "it's killing itself" weirdness.

On Linux and macOS, the POSIX idiom `os.kill(pid, 0)` is a no-op permission check: "is this PID alive and can I signal it?" On Windows, Python's `os.kill` maps `sig=0` to `CTRL_C_EVENT` — they collide at integer value 0 — and routes it through `GenerateConsoleCtrlEvent(0, pid)`, which broadcasts Ctrl+C to the **entire console process group** containing the target PID. That's [bpo-14484](https://bugs.python.org/issue14484), open since 2012. It won't be fixed because changing it would break scripts that depend on the current behavior.

Consequence: any codepath that said "check if this PID is alive" via `os.kill(pid, 0)` on Windows was silently killing the target. Hermes migrated every such site (14 across 11 files) to `gateway.status._pid_exists()`, which uses `psutil.pid_exists()` (which in turn uses `OpenProcess + GetExitCodeProcess` on Windows — no signals). If you're writing a plugin or patch, use `psutil.pid_exists()` directly or `gateway.status._pid_exists()` — never `os.kill(pid, 0)`. This is why `hermes gateway status` is idempotent — calling it never accidentally kills the gateway.

`scripts/check-windows-footguns.py` enforces this in CI: any new `os.kill(pid, 0)` call fails the `Windows footguns (blocking)` check unless the line carries a `# windows-footgun: ok — <reason>` marker.

## Common pitfalls

- **`hermes: command not found` right after install.** Open a new PowerShell window. The installer added `%LOCALAPPDATA%\hermes\bin` to User PATH, but existing shells need to be restarted to pick it up. In the meantime you can run `& "$env:LOCALAPPDATA\hermes\bin\hermes.cmd"`.
- **`WinError 193: %1 is not a valid Win32 application` when running a tool.** You hit a shebang-script invocation that bypassed the `.cmd` shim. Hermes resolves commands through `shutil.which(cmd, path=local_bin)` so PATHEXT picks up `.CMD` — if you're invoking the tool via a hardcoded path instead, switch to the `.cmd` variant (e.g., `npx.cmd`, not `npx`).
- **`[scriptblock]::Create(...)` fails with `The assignment expression is not valid`.** Your download of `install.ps1` picked up a UTF-8 BOM. The `irm | iex` form strips BOMs automatically; `[scriptblock]::Create((irm ...))` does not. Re-run with the simple `irm | iex` form, or save the script without a BOM.
- **Gateway won't stay running after restart.** Check `hermes gateway status` — it merges the schtasks entry, the Startup-folder shortcut (if used), and the live PID. If schtasks is registered but not running, group policy may be blocking `ONLOGON` triggers. Run `schtasks /Query /TN HermesGateway /V /FO LIST` to see the task's failure reason, or fall back to the Startup-folder path by reinstalling with `HERMES_GATEWAY_FORCE_STARTUP=1`.
- **`/edit` still does nothing after setting `$env:EDITOR`.** You set it in the current process only; close and reopen the shell, or set it at User scope in System Properties → Environment Variables. Verify with `echo $env:EDITOR` in a new PowerShell window.
- **Browser tool launches but tools time out.** Chromium is auto-installed on first run. If the install failed (rate-limited GitHub, Playwright CDN hiccup), run `hermes doctor` — it surfaces the missing Chromium and prints the exact `npx playwright install chromium` command to fix it.
- **`agent-browser` fails with a weird Node version error.** The installer provisions Node 22 at `%LOCALAPPDATA%\hermes\node` but your PATH may have an older system Node 18 first. Either move Hermes's node dir earlier on PATH, or delete the system install if you don't use Node elsewhere.
- **Chinese / Japanese / Arabic characters show as `?` in the CLI.** The UTF-8 stdio shim didn't activate. Check that `HERMES_DISABLE_WINDOWS_UTF8` is NOT set. If it's empty and you still see `?`, the console host (very old `cmd.exe`) may not support UTF-8 at all — switch to Windows Terminal.
- **Gateway can't send Telegram photos — "`BadRequest: payload contains invalid characters`".** Usually means your file path contains unescaped backslashes in a JSON body. Pass the Hermes-provided normalized path, not a raw Windows path, from a custom plugin.
- **"Works on my other machine" encoding weirdness after `git pull`.** If you edited config/skill files with a non-UTF-8 editor, a BOM may have been saved. A BOM inside a folded YAML scalar (`description: >`) silently breaks YAML parsing — re-save the file as plain UTF-8 without BOM.

**Source**: `inbox/hermes_agent_docs/user-guide/windows-native.md` · https://hermes-agent.nousresearch.com/docs/user-guide/windows-native
**Last Updated**: 2026-06-19
**Status**: Active
