---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - tokenjuice
keywords:
  - openclaw tokenjuice plugin
  - compact exec bash tool results
  - tool-result middleware
  - plugins.entries.tokenjuice.enabled
  - clawhub @openclaw/tokenjuice
  - openclaw plugins install enable disable
  - context-budget tool output compaction
topics:
  - OpenClaw
  - Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/tokenjuice
access_control_group: ["general"]
---

# OpenClaw — Tokenjuice: Compacting Noisy `exec`/`bash` Tool Results

## Overview

This note is the procedure for the **Tokenjuice** plugin in OpenClaw: an optional external plugin that compacts noisy `exec` and `bash` `tool_result` output *after* the command has already run, hooking OpenClaw's tool-result middleware so trimmed output (not the command) goes back into the active harness session. It mirrors the `tools/tokenjuice` source page in full — what Tokenjuice is and what it does NOT touch, how to install/enable it (three equivalent forms plus direct config), what it changes versus what it leaves raw, how to verify it, and how to disable it.

## What Tokenjuice Is

`tokenjuice` is an optional external plugin that compacts noisy `exec` and `bash` tool results after the command has already run. It changes the returned `tool_result`, not the command itself: Tokenjuice does **not** rewrite shell input, rerun commands, or change exit codes. Today this applies to **OpenClaw embedded runs** and **OpenClaw dynamic tools in the Codex app-server harness** — Tokenjuice hooks OpenClaw's tool-result middleware and trims the output before it goes back into the active harness session.

## Enable the Plugin

Install once, then enable it. The page gives three equivalent ways to turn Tokenjuice on (the `config set` form and the `plugins enable` form are equivalent), plus a direct-config edit. Install the plugin from ClawHub:

```bash
openclaw plugins install clawhub:@openclaw/tokenjuice
```

Then enable it via config:

```bash
openclaw config set plugins.entries.tokenjuice.enabled true
```

The equivalent `plugins enable` shorthand is:

```bash
openclaw plugins enable tokenjuice
```

If you prefer editing config directly, set `plugins.entries.tokenjuice.enabled` to `true`:

```json5
{
  plugins: {
    entries: {
      tokenjuice: {
        enabled: true,
      },
    },
  },
}
```

## What Tokenjuice Changes

The page enumerates exactly what Tokenjuice does and what it deliberately leaves alone:

- Compacts noisy `exec` and `bash` results before they are fed back into the session.
- Keeps the original command execution untouched.
- Preserves exact file-content reads and other commands that tokenjuice should leave raw.
- Stays opt-in: disable the plugin if you want verbatim output everywhere.

The behavior boundary is the load-bearing point: trimming is applied to the *returned result payload* of noisy shell commands, while exact file-content reads (and other commands Tokenjuice should leave raw) are preserved verbatim, so reductions never silently alter content the model relies on byte-for-byte.

## Verify It Is Working

The page's verification procedure is a four-step check that compares a noisy command's returned result against its raw shell output:

1. Enable the plugin.
2. Start a session that can call `exec`.
3. Run a noisy command such as `git status`.
4. Check that the returned tool result is shorter and more structured than the raw shell output.

## Disable the Plugin

Tokenjuice is opt-in, so disabling it restores verbatim output everywhere. Disable it via config:

```bash
openclaw config set plugins.entries.tokenjuice.enabled false
```

Or use the `plugins disable` shorthand:

```bash
openclaw plugins disable tokenjuice
```

**Source**: OpenClaw documentation — `tools/tokenjuice` (mirror `inbox/openclaw_docs/tools/tokenjuice.md`)
**Last Updated**: 2026-06-22
**Status**: Active
