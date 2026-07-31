---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - completion
keywords:
  - openclaw completion command
  - shell completion scripts
  - zsh bash fish powershell completion
  - completion install shell profile
  - openclaw_state_dir completions
  - write-state completion cache
  - eager command tree load
  - completion install confirmation
topics:
  - OpenClaw
  - CLI Shell Completion
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/completion
access_control_group: ["general"]
---

# OpenClaw — `openclaw completion` (Shell Completion Scripts)

## Overview

This note documents the `openclaw completion` CLI command, which generates shell completion scripts and optionally installs them into your shell profile, mirroring the `cli/completion` source page. It covers the command's invocation forms, the four options (`--shell`, `--install`, `--write-state`, `--yes`), the three output behaviors (print to stdout, write a source line into the shell profile, or cache scripts under OpenClaw state), and the eager command-tree loading that ensures nested subcommands appear in completions. Use this command when you want shell completions for zsh, bash, fish, or PowerShell, or when you need to cache completion scripts under the OpenClaw state directory.

## Usage

The command runs standalone (printing to stdout) or with options that select a shell target and an install or cache destination:

```bash
openclaw completion
openclaw completion --shell zsh
openclaw completion --install
openclaw completion --shell fish --install
openclaw completion --write-state
openclaw completion --shell bash --write-state
```

## Options

The command accepts four options:

- `-s, --shell <shell>` — shell target (`zsh`, `bash`, `powershell`, `fish`; default: `zsh`).
- `-i, --install` — install completion by adding a source line to your shell profile.
- `--write-state` — write completion script(s) to `$OPENCLAW_STATE_DIR/completions` without printing to stdout.
- `-y, --yes` — skip install confirmation prompts.

## Notes

The command's behavior depends on which of the install/cache options is supplied. With `--install`, OpenClaw writes a small "OpenClaw Completion" block into your shell profile and points it at the cached script. Without `--install` or `--write-state`, the command prints the script to stdout. Completion generation eagerly loads command trees so nested subcommands are included.

**Source**: OpenClaw documentation — `cli/completion` (mirror `inbox/openclaw_docs/cli/completion.md`)
**Last Updated**: 2026-06-22
**Status**: Active
