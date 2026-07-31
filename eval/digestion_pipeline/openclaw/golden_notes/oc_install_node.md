---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - node
keywords:
  - openclaw node.js prerequisite
  - node 22.19 node 24 recommended
  - openclaw command not found
  - npm install -g eacces
  - npm prefix global bin path
  - node version manager fnm nvm mise asdf
  - per-os node install homebrew nodesource winget
topics:
  - OpenClaw
  - Node.js Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/node
access_control_group: ["general"]
---

# OpenClaw — Installing the Node.js Prerequisite

## Overview

This note is the step-by-step procedure for installing and wiring up the Node.js runtime that OpenClaw requires, mirroring the `install/node` source page. OpenClaw requires **Node 22.19 or newer**, with **Node 24 as the default and recommended runtime** for installs, CI, and release workflows (Node 22 remains supported via the active LTS line). The [installer script](https://docs.openclaw.ai/install#alternative-install-methods) will detect and install Node automatically; this page is for when you want to set up Node yourself and make sure everything is wired up correctly (versions, PATH, global installs). It covers checking your version, per-OS install (Homebrew / NodeSource / winget / Chocolatey), optional version managers, and the two classic post-install failures — `openclaw: command not found` (npm global bin not on PATH) and Linux `EACCES` errors on `npm install -g`.

## Check your version

Verify the installed Node version:

```bash
node -v
```

If this prints `v24.x.x` or higher, you're on the recommended default. If it prints `v22.19.x` or higher, you're on the supported Node 22 LTS path, but the docs still recommend upgrading to Node 24 when convenient. If Node isn't installed or the version is too old, pick an install method below.

## Install Node

The source page presents per-OS install tabs. The load-bearing command(s) per OS are reproduced below; alternatives (the platform GUI installers from [nodejs.org](https://nodejs.org/)) are prosed.

**macOS** — Homebrew is the recommended path:

```bash
brew install node
```

Alternatively, download the macOS installer from nodejs.org.

**Linux** — for Ubuntu / Debian, install via the NodeSource setup script; for Fedora / RHEL, use `dnf` (or a version manager, below):

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
```

For Fedora / RHEL the command is `sudo dnf install nodejs`.

**Windows** — winget is the recommended path; Chocolatey (`choco install nodejs-lts`) is the alternative, or download the Windows installer from nodejs.org:

```powershell
winget install OpenJS.NodeJS.LTS
```

### Using a version manager (nvm, fnm, mise, asdf)

Version managers let you switch between Node versions easily. The source page lists [**fnm**](https://github.com/Schniz/fnm) (fast, cross-platform), [**nvm**](https://github.com/nvm-sh/nvm) (widely used on macOS/Linux), and [**mise**](https://mise.jdx.dev/) (polyglot — Node, Python, Ruby, etc.). The source's example with fnm is `fnm install 24` followed by `fnm use 24`.

**Warning (from source):** make sure your version manager is initialized in your shell startup file (`~/.zshrc` or `~/.bashrc`). If it isn't, `openclaw` may not be found in new terminal sessions because the PATH won't include Node's bin directory.

## Troubleshooting

### `openclaw: command not found`

This almost always means npm's global bin directory isn't on your PATH. The source page gives a three-step fix:

1. **Find your global npm prefix** — run `npm prefix -g`.
2. **Check if it's on your PATH** — run `echo "$PATH"` and look for `<npm-prefix>/bin` (macOS/Linux) or `<npm-prefix>` (Windows) in the output.
3. **Add it to your shell startup file** — on macOS / Linux, add the following to `~/.zshrc` or `~/.bashrc`, then open a new terminal (or run `rehash` in zsh / `hash -r` in bash):

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

On Windows, add the output of `npm prefix -g` to your system PATH via Settings → System → Environment Variables.

### Permission errors on `npm install -g` (Linux)

If you see `EACCES` errors, switch npm's global prefix to a user-writable directory:

```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"
```

Add the `export PATH=...` line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

**Source**: OpenClaw documentation — `install/node` (mirror `inbox/openclaw_docs/install/node.md`)
**Last Updated**: 2026-06-22
**Status**: Active
