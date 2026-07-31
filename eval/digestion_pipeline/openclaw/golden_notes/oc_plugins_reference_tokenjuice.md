---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw tokenjuice plugin
  - tokenjuice reducers
  - agentToolResultMiddleware contract
  - compact exec bash tool results
  - clawhub openclaw tokenjuice
  - tool result compaction middleware
  - openclaw plugin reference card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/tokenjuice
access_control_group: ["general"]
---

# OpenClaw — Tokenjuice Plugin (Reference Card)

## Overview

This note captures the OpenClaw **Tokenjuice** plugin-reference card from the `plugins/reference/tokenjuice` ClawHub catalog page. Tokenjuice "Compacts exec and bash tool results with tokenjuice reducers." — a tool-result compaction middleware plugin. As a uniform plugin-catalog card it carries exactly three load-bearing facts: its **Distribution** (npm package id + install route), its **Surface** (the OpenClaw SDK contract it contributes), and a **Related docs** pointer to the deep feature page at `/tools/tokenjuice`. Deeper middleware behavior lives on that linked tool page (owned by a separate Tools sub-plan), not here; this card is the inventory entry that fronts it.

## Distribution

- **Package**: `@openclaw/tokenjuice`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/tokenjuice`

Tokenjuice is not bundled into OpenClaw by default — it installs from npm or via the ClawHub install identifier `clawhub:@openclaw/tokenjuice`.

## Surface

The plugin contributes a single OpenClaw SDK contract:

- **contracts: `agentToolResultMiddleware`** — a tool-result middleware hook. Tokenjuice registers a reducer on this contract so that the raw output of `exec` and `bash` tool calls is compacted before it is appended to the agent's context, conserving the token budget.

**Source**: OpenClaw documentation — `plugins/reference/tokenjuice` (mirror `inbox/openclaw_docs/plugins/reference/tokenjuice.md`)
**Last Updated**: 2026-06-22
**Status**: Active
