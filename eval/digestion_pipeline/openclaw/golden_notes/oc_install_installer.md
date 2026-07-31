---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - installer
keywords:
  - openclaw installer scripts
  - install.sh install-cli.sh install.ps1
  - openclaw install flags
  - openclaw_install_method env var
  - install openclaw from github checkout
  - openclaw ci headless install
  - openclaw npm vs git install
  - openclaw doctor non-interactive
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/installer
access_control_group: ["general"]
---

# OpenClaw — Installer Script Internals (`install.sh` / `install-cli.sh` / `install.ps1`)

## Overview

This note is a procedure reference for the three official OpenClaw installer scripts served from `openclaw.ai`: `install.sh` (macOS / Linux / WSL, global npm or git), `install-cli.sh` (macOS / Linux / WSL, local-prefix `~/.openclaw` install with a pinned Node and no root), and `install.ps1` (Windows PowerShell, global npm or git). It mirrors the `install/installer` source page: quick-command invocations, each script's flow, its flags and `OPENCLAW_*` environment variables (reproduced verbatim), non-interactive CI/automation usage, and the troubleshooting catalog. It does NOT cover the generic Install overview, Updating, or Uninstall pages (siblings), nor the `openclaw onboard` / `openclaw doctor` CLI commands themselves (owned by the CLI sub-plans).

## Quick Commands

OpenClaw ships three installer scripts served from `openclaw.ai`: `install.sh` (macOS / Linux / WSL) installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding; `install-cli.sh` (macOS / Linux / WSL) installs Node + OpenClaw into a local prefix (`~/.openclaw`) with npm or git checkout modes and needs no root; `install.ps1` (Windows / PowerShell) installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding. The canonical one-line invocations are:

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Append `| bash -s -- --help` (POSIX) or `... -Tag beta -NoOnboard -DryRun` (PowerShell scriptblock form) to inspect usage or preview. If install succeeds but `openclaw` is not found in a new terminal, the source points to Node.js troubleshooting (`/install/node#troubleshooting`).

## install.sh (macOS / Linux / WSL)

Recommended for most interactive installs on macOS/Linux/WSL. The flow runs five steps. (1) **Detect OS** — supports macOS and Linux (including WSL). (2) **Ensure Node.js 24 by default** — installs Node 24 if needed (Homebrew on macOS, NodeSource setup scripts on Linux apt/dnf/yum; Homebrew is installed on macOS only when needed for Node or Git); Node 22 LTS, currently `22.19+`, stays supported; on Alpine/musl Linux it uses apk packages instead of NodeSource, and the configured Alpine repositories must provide Node `22.19+` (Alpine 3.21 or newer). (3) **Ensure Git** — installs Git if missing using the detected package manager (Homebrew on macOS, apk on Alpine). (4) **Install OpenClaw** — `npm` method (default) does a global npm install; `git` method clones/updates the repo, installs deps with pnpm, builds, then installs a wrapper at `~/.local/bin/openclaw`. (5) **Post-install tasks** — refreshes a loaded gateway service best-effort (`openclaw gateway install --force`, then restart), runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort), and attempts onboarding when appropriate (TTY available, onboarding not disabled, bootstrap/config checks pass).

### Source Checkout Detection

If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers either to use the checkout (`git`) or to use a global install (`npm`). If no TTY is available and no install method is set, it defaults to `npm` and warns. The script exits with code `2` for invalid method selection or invalid `--install-method` values.

### Examples (install.sh)

The representative invocations cover the default, skipping onboarding, a git install, pinning to the GitHub `main` checkout, and a dry run:

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash                                          # Default
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard                       # Skip onboarding
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git               # Git install
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git --version main # GitHub main checkout
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run                          # Dry run
```

### Flags Reference (install.sh)

| Flag | Description |
|------|-------------|
| `--install-method npm\|git` | Choose install method (default: `npm`). Alias: `--method` |
| `--npm` | Shortcut for npm method |
| `--git` | Shortcut for git method. Alias: `--github` |
| `--version <version\|dist-tag\|spec>` | npm version, dist-tag, or package spec (default: `latest`) |
| `--beta` | Use beta dist-tag if available, else fallback to `latest` |
| `--git-dir <path>` | Checkout directory (default: `~/openclaw`). Alias: `--dir` |
| `--no-git-update` | Skip `git pull` for existing checkout |
| `--no-prompt` | Disable prompts |
| `--no-onboard` | Skip onboarding |
| `--onboard` | Enable onboarding |
| `--dry-run` | Print actions without applying changes |
| `--verbose` | Enable debug output (`set -x`, npm notice-level logs) |
| `--help` | Show usage (`-h`) |

### Environment Variables Reference (install.sh)

| Variable | Description |
|----------|-------------|
| `OPENCLAW_INSTALL_METHOD=git\|npm` | Install method |
| `OPENCLAW_VERSION=latest\|next\|<semver>\|<spec>` | npm version, dist-tag, or package spec |
| `OPENCLAW_BETA=0\|1` | Use beta if available |
| `OPENCLAW_HOME=<path>` | Base directory for OpenClaw state and default git/onboarding paths |
| `OPENCLAW_GIT_DIR=<path>` | Checkout directory |
| `OPENCLAW_GIT_UPDATE=0\|1` | Toggle git updates |
| `OPENCLAW_NO_PROMPT=1` | Disable prompts |
| `OPENCLAW_NO_ONBOARD=1` | Skip onboarding |
| `OPENCLAW_DRY_RUN=1` | Dry run mode |
| `OPENCLAW_VERBOSE=1` | Debug mode |
| `OPENCLAW_NPM_LOGLEVEL=error\|warn\|notice` | npm log level |

## install-cli.sh (Local-Prefix, No Root)

Designed for environments where you want everything under a local prefix (default `~/.openclaw`) and no system Node dependency; npm installs by default, plus git-checkout installs under the same prefix flow. The flow runs four steps. (1) **Install local Node runtime** — downloads a pinned supported Node LTS tarball (version embedded in the script, updated independently) to `<prefix>/tools/node-v<version>` and verifies SHA-256; on Alpine/musl Linux, where Node publishes no compatible tarball for the pinned runtime, it installs `nodejs` and `npm` with `apk` and links that runtime into the prefix wrapper path (repositories must provide Node `22.19+`; use Alpine 3.21 or newer if older ones only provide Node 20 or 21). (2) **Ensure Git** — if missing, attempts install via apt/dnf/yum/apk on Linux or Homebrew on macOS. (3) **Install OpenClaw under prefix** — `npm` method (default) installs under the prefix with npm then writes a wrapper to `<prefix>/bin/openclaw`; `git` method clones/updates a checkout (default `~/openclaw`) and still writes the wrapper to `<prefix>/bin/openclaw`. (4) **Refresh loaded gateway service** — if a gateway service is already loaded from that same prefix, runs `openclaw gateway install --force`, then `openclaw gateway restart`, and probes gateway health best-effort.

### Examples (install-cli.sh)

The representative invocations cover the default, a custom prefix with a pinned version, a git install with a checkout directory, NDJSON automation output, and running onboarding after install:

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash                                                       # Default
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest         # Custom prefix + version
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --install-method git --git-dir ~/openclaw       # Git install
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw                    # Automation JSON output
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard                                       # Run onboarding
```

### Flags Reference (install-cli.sh)

| Flag | Description |
|------|-------------|
| `--prefix <path>` | Install prefix (default: `~/.openclaw`) |
| `--install-method npm\|git` | Choose install method (default: `npm`). Alias: `--method` |
| `--npm` | Shortcut for npm method |
| `--git`, `--github` | Shortcut for git method |
| `--git-dir <path>` | Git checkout directory (default: `~/openclaw`). Alias: `--dir` |
| `--version <ver>` | OpenClaw version or dist-tag (default: `latest`) |
| `--node-version <ver>` | Node version (default: `22.22.0`) |
| `--json` | Emit NDJSON events |
| `--onboard` | Run `openclaw onboard` after install |
| `--no-onboard` | Skip onboarding (default) |
| `--set-npm-prefix` | On Linux, force npm prefix to `~/.npm-global` if current prefix is not writable |
| `--help` | Show usage (`-h`) |

### Environment Variables Reference (install-cli.sh)

| Variable | Description |
|----------|-------------|
| `OPENCLAW_PREFIX=<path>` | Install prefix |
| `OPENCLAW_INSTALL_METHOD=git\|npm` | Install method |
| `OPENCLAW_VERSION=<ver>` | OpenClaw version or dist-tag |
| `OPENCLAW_NODE_VERSION=<ver>` | Node version |
| `OPENCLAW_HOME=<path>` | Base directory for OpenClaw state and default git/onboarding paths |
| `OPENCLAW_GIT_DIR=<path>` | Git checkout directory for git installs |
| `OPENCLAW_GIT_UPDATE=0\|1` | Toggle git updates for existing checkouts |
| `OPENCLAW_NO_ONBOARD=1` | Skip onboarding |
| `OPENCLAW_NPM_LOGLEVEL=error\|warn\|notice` | npm log level |

## install.ps1 (Windows / PowerShell)

The Windows flow runs five steps. (1) **Ensure PowerShell + Windows environment** — requires PowerShell 5+. (2) **Ensure Node.js 24 by default** — if missing, attempts install via winget, then Chocolatey, then Scoop; if no package manager is available, downloads the official Node.js Windows zip into `%LOCALAPPDATA%\OpenClaw\deps\portable-node` and adds it to the current process and user PATH; Node 22 LTS, currently `22.19+`, remains supported. (3) **Install OpenClaw** — `npm` method (default) does a global npm install using the selected `-Tag`, launched from a writable installer temp directory so shells opened in protected folders such as `C:\` still work; `git` method clones/updates the repo, installs/builds with pnpm, and installs a wrapper at `%USERPROFILE%\.local\bin\openclaw.cmd`, and if Git is missing it bootstraps user-local MinGit under `%LOCALAPPDATA%\OpenClaw\deps\portable-git` and adds it to PATH. (4) **Post-install tasks** — adds the needed bin directory to user PATH when possible, refreshes a loaded gateway service best-effort (`openclaw gateway install --force`, then restart), and runs `openclaw doctor --non-interactive` on upgrades and git installs (best effort). (5) **Handle failures** — `iwr ... | iex` and scriptblock installs report a terminating error without closing the current PowerShell session, while direct `powershell -File` / `pwsh -File` installs still exit non-zero for automation.

### Examples (install.ps1)

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex                                                                # Default
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git                       # Git install
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -Tag main             # GitHub main checkout
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw" # Custom git directory
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun                                  # Dry run
```

`install.ps1` has no dedicated `-Verbose` flag yet; for a debug trace, wrap the scriptblock install in `Set-PSDebug -Trace 1` / `Set-PSDebug -Trace 0`.

### Flags Reference (install.ps1)

| Flag | Description |
|------|-------------|
| `-InstallMethod npm\|git` | Install method (default: `npm`) |
| `-Tag <tag\|version\|spec>` | npm dist-tag, version, or package spec (default: `latest`) |
| `-GitDir <path>` | Checkout directory (default: `%USERPROFILE%\openclaw`) |
| `-NoOnboard` | Skip onboarding |
| `-NoGitUpdate` | Skip `git pull` |
| `-DryRun` | Print actions only |

### Environment Variables Reference (install.ps1)

| Variable | Description |
|----------|-------------|
| `OPENCLAW_INSTALL_METHOD=git\|npm` | Install method |
| `OPENCLAW_GIT_DIR=<path>` | Checkout directory |
| `OPENCLAW_NO_ONBOARD=1` | Skip onboarding |
| `OPENCLAW_GIT_UPDATE=0` | Disable git pull |
| `OPENCLAW_DRY_RUN=1` | Dry run mode |

If `-InstallMethod git` is used and Git is missing, the script tries a user-local MinGit bootstrap before printing the Git for Windows link.

## CI and Automation

For predictable runs, use non-interactive flags/env vars. On `install.sh` use `--no-prompt --no-onboard` (or set `OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1` before the pipe for a non-interactive git install); on `install-cli.sh` use `--json --prefix /opt/openclaw` to emit machine-parseable NDJSON events; on `install.ps1` pass `-NoOnboard`:

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard      # install.sh non-interactive npm
OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
  curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash                                   # install.sh non-interactive git
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw  # install-cli.sh JSON
```

## Troubleshooting

The source page documents these recurring failures. **Why is Git required?** — Git is required for the `git` install method; for `npm` installs, Git is still checked/installed to avoid `spawn git ENOENT` failures when dependencies use git URLs. **Why does npm hit EACCES on Linux?** — Some Linux setups point the npm global prefix to root-owned paths; `install.sh` can switch the prefix to `~/.npm-global` and append PATH exports to shell rc files (when those files exist). **Windows: "npm error spawn git / ENOENT"** — rerun the installer so it can bootstrap user-local MinGit, or install Git for Windows and reopen PowerShell. **Windows: "openclaw is not recognized"** — run `npm config get prefix` and add that directory to your user PATH (no `\bin` suffix needed on Windows), then reopen PowerShell. **Windows: how to get verbose installer output** — `install.ps1` does not currently expose a `-Verbose` switch; use PowerShell tracing (`Set-PSDebug -Trace 1` around the scriptblock install) for script-level diagnostics. **openclaw not found after install** — usually a PATH issue; see Node.js troubleshooting (`/install/node#troubleshooting`).

**Source**: OpenClaw documentation — `install/installer` (mirror `inbox/openclaw_docs/install/installer.md`)
**Last Updated**: 2026-06-22
**Status**: Active
