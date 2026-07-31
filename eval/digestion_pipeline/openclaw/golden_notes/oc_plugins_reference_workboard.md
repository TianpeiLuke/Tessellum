---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw workboard plugin
  - workboard dashboard
  - agent-owned issues and sessions
  - "@openclaw/workboard"
  - tools contract plugin
  - bundled plugin included in openclaw
  - kanban workboard
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/workboard
access_control_group: ["general"]
---

# OpenClaw — Workboard Plugin (Reference)

## Overview

This note is the plugin-reference data sheet for the OpenClaw **Workboard** plugin, mirroring the `plugins/reference/workboard` source page. The page summarizes it as a "Dashboard workboard for agent-owned issues and sessions" and is the page you read when you are installing, configuring, or auditing the workboard plugin. It captures the two load-bearing facts of a plugin reference — the **Distribution** (npm package id + install route) and the **Surface** (the OpenClaw contracts the plugin registers into) — plus the Related-docs pointer to the full workboard how-to. The Workboard plugin is bundled (included in OpenClaw) and registers via the `tools` contract, exposing a dashboard for tracking the issues and sessions an agent owns.

## Distribution

- **Package:** `@openclaw/workboard`
- **Install route:** included in OpenClaw

The package is a bundled (first-party) plugin — its install route is "included in OpenClaw", meaning it ships with the gateway rather than being fetched separately from npm or ClawHub. No additional install command is given on the source page.

## Surface

The Surface block declares the OpenClaw contract(s) the plugin registers into:

- **contracts:** `tools`

The plugin's only registered surface is the `tools` contract — the catalog of agent-callable tools. The Workboard plugin therefore contributes tool(s) the agent invokes to manage its dashboard of agent-owned issues and sessions; it does not register any provider or channel surface. (The source page lists no providers and no channels.)

**Source**: OpenClaw documentation — `plugins/reference/workboard` (mirror `inbox/openclaw_docs/plugins/reference/workboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
