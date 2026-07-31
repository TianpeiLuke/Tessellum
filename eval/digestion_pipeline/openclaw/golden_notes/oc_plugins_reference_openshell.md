---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sandbox
keywords:
  - openclaw openshell plugin
  - openshell sandbox backend
  - nvidia openshell cli
  - mirrored local workspaces
  - ssh command execution
  - openclaw/openshell-sandbox
  - clawhub plugin install
  - sandbox backend plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/openshell
access_control_group: ["general"]
---

# OpenClaw — OpenShell Sandbox-Backend Plugin

## Overview

This note models the OpenClaw **OpenShell plugin** as a plugin-reference catalog entry, mirroring the `plugins/reference/openshell` source page. The page describes it in one line: an "OpenClaw sandbox backend for the NVIDIA OpenShell CLI with mirrored local workspaces and SSH command execution." As a plugin descriptor it records what package ships the plugin (`@openclaw/openshell-sandbox`), how it is installed (npm; ClawHub), and the surface it contributes (`plugin`). The source page is a terse reference card with two sections — **Distribution** and **Surface** — and carries no `Related docs` pointer (it cross-links the gateway/sandboxing pages instead). Everything below traces verbatim to that mirror page; no flags, defaults, or configuration are invented because the source specifies none.

## Plugin Summary

The OpenShell plugin is described by the source page's one-line summary as an "OpenClaw sandbox backend for the NVIDIA OpenShell CLI with mirrored local workspaces and SSH command execution." Read as a model of what the plugin contributes, three capabilities are named in that summary: it is a **sandbox backend** (a pluggable execution backend OpenClaw can target for sandboxed agent runs); it wraps the **NVIDIA OpenShell CLI** (the external tool the backend drives); and it operates through **mirrored local workspaces** with **SSH command execution** (the agent's local workspace is mirrored and commands are run over SSH). The page's `read_when` guidance scopes the doc to operators who are "installing, configuring, or auditing the openshell plugin." No further configuration keys, environment variables, defaults, or behavior beyond this summary are specified in the source.

## Distribution

The source page's `## Distribution` section records exactly two facts:

- **Package**: `@openclaw/openshell-sandbox`
- **Install route**: npm; ClawHub

That is, the plugin ships as the npm package `@openclaw/openshell-sandbox` and can be installed through npm or through ClawHub (OpenClaw's plugin distribution hub). The source does not state whether the plugin is bundled with OpenClaw by default — unlike some reference cards that read "included in OpenClaw," this card lists only the npm/ClawHub install route, so a default-bundled status is *(inferred — not stated in source; treat as installable, not bundled)*.

## Surface

The source page's `## Surface` section names the contract surface the plugin contributes with a single token:

- `plugin`

This is the entirety of the declared surface in the mirror page. In the OpenClaw plugin model the surface enumerates the contracts a package contributes (for other reference cards these are concrete contracts such as `providers`, `webSearchProviders`, `channels`, or a sandbox-backend registration); for OpenShell the source records only the generic `plugin` surface token. The functional surface implied by the summary — a sandbox backend for the NVIDIA OpenShell CLI — is described in the one-line summary above, not enumerated as a typed contract in this section. No additional contracts, RPC names, or registration keys are specified in the source.

**Source**: OpenClaw documentation — `plugins/reference/openshell` (mirror `inbox/openclaw_docs/plugins/reference/openshell.md`)
**Last Updated**: 2026-06-22
**Status**: Active
