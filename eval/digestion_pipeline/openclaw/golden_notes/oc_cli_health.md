---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - health
keywords:
  - openclaw health
  - gateway health snapshot
  - health --json
  - health --verbose live probe
  - health --timeout
  - cached health snapshot refresh
  - per-agent session stores
topics:
  - OpenClaw
  - CLI Health
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/health
access_control_group: ["general"]
---

# OpenClaw — `openclaw health` CLI

## Overview

This note documents the `openclaw health` CLI procedure, which fetches a health snapshot from the running OpenClaw Gateway, mirroring the `cli/health` source page. It covers the four command flags (`--json`, `--timeout <ms>`, `--verbose`, `--debug`), the canonical usage examples, the cached-vs-live probe behavior (a fresh cached snapshot can be returned with a background refresh, while `--verbose` forces a live probe), and the per-agent session-store expansion when multiple agents are configured.

## Purpose

`openclaw health` asks the running Gateway for its health snapshot. It is a fast, read-only diagnostic for confirming a Gateway's liveness and inspecting its configured accounts and agents.

## Options

The command exposes four flags (defaults reproduced verbatim from source):

| Flag | Default | Description |
| --- | --- | --- |
| `--json` | `false` | Print machine-readable JSON instead of text. |
| `--timeout <ms>` | `10000` | Connection timeout in milliseconds. |
| `--verbose` | `false` | Verbose logging. Forces a live probe and expands per-agent output. |
| `--debug` | `false` | Alias for `--verbose`. |

## Examples

The source page lists these canonical invocations:

```bash
openclaw health
openclaw health --json
openclaw health --timeout 2500
openclaw health --verbose
openclaw health --debug
```

`openclaw health` returns the default text snapshot; `--json` emits a machine-readable payload; `--timeout 2500` sets the connection timeout to 2500 ms; `--verbose` and its alias `--debug` force a live probe with expanded per-agent output.

## Behavior Notes

The default `openclaw health` invocation asks the running gateway for its health snapshot. When the gateway already has a fresh cached snapshot, it can return that cached payload and refresh in the background. The `--verbose` flag forces a live probe, prints gateway connection details, and expands the human-readable output across all configured accounts and agents. Output includes per-agent session stores when multiple agents are configured.

**Source**: OpenClaw documentation — `cli/health` (mirror `inbox/openclaw_docs/cli/health.md`)
**Last Updated**: 2026-06-22
**Status**: Active
