---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw sglang plugin
  - sglang model provider
  - "@openclaw/sglang-provider"
  - providers sglang surface
  - sglang inference backend
  - included in openclaw plugin
  - install sglang plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/sglang
access_control_group: ["general"]
---

# OpenClaw — SGLang Plugin Reference

## Overview

This note is the install/configure/audit reference card for the OpenClaw **SGLang plugin**, mirroring the `plugins/reference/sglang` source page. The plugin's one-line purpose is: "Adds SGLang model provider support to OpenClaw." It ships as the npm package `@openclaw/sglang-provider`, is **included in OpenClaw** (no separate install step), and contributes a model-provider **Surface** of `providers: sglang` — registering an SGLang inference backend as a selectable model provider. The source page's `read_when` audience is: "You are installing, configuring, or auditing the sglang plugin." This card carries only the operational facts (package, install route, surface); the conceptual SGLang provider setup is documented separately at `/providers/sglang` (see Related docs / Related Notes).

## Distribution

- Package: `@openclaw/sglang-provider`
- Install route: included in OpenClaw

Because the install route is **included in OpenClaw**, the `@openclaw/sglang-provider` package ships with the gateway and is loaded at runtime without a separate `npm install` or ClawHub fetch — operators enable/configure the `sglang` provider surface rather than installing the package. *(Inferred — the source states only "included in OpenClaw"; no enable/config flags or env vars are listed on this page.)*

## Surface

providers: sglang

This plugin contributes a single provider surface, `sglang`. Enabling it registers an SGLang-served inference backend as an OpenClaw model provider, after which SGLang-served models become selectable in the agent's model catalog. The page does not enumerate model IDs, endpoints, auth keys, or config keys beyond the `providers: sglang` surface identifier — those belong to the conceptual provider guide.

**Source**: OpenClaw documentation — `plugins/reference/sglang` (mirror `inbox/openclaw_docs/plugins/reference/sglang.md`)
**Last Updated**: 2026-06-22
**Status**: Active
