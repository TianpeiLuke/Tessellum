---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw copilot proxy plugin
  - copilot-proxy provider
  - "@openclaw/copilot-proxy"
  - copilot proxy model provider
  - provider plugin surface
  - included in openclaw
  - copilot model proxy
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/copilot-proxy
access_control_group: ["general"]
---

# OpenClaw — Copilot Proxy Provider Plugin (Reference Card)

## Overview

This note is the reference-card schema for the OpenClaw **Copilot Proxy** plugin, mirroring the `plugins/reference/copilot-proxy` source page. The plugin "Adds Copilot Proxy model provider support to OpenClaw" — it is a packaged unit (`@openclaw/copilot-proxy`) that registers one model provider, surfaced under the provider id `copilot-proxy`. The card has two source sections, **Distribution** (package id + install route) and **Surface** (the runtime surface the plugin contributes); this page has no `## Related docs` section, so the provider-configuration doc is not cross-linked from the source. This is the model-**provider** counterpart to the Copilot agent-runtime plugin documented in `oc_plugins_reference_copilot.md`.

## Distribution

- **Package**: `@openclaw/copilot-proxy`
- **Install route**: included in OpenClaw

The plugin ships bundled with OpenClaw (no separate npm or ClawHub install step is listed on the source page), so it is available once OpenClaw is installed.

## Surface

The plugin contributes one surface to the OpenClaw runtime:

- **providers**: `copilot-proxy`

Registering this surface adds the `copilot-proxy` model provider to OpenClaw's provider/model catalog, exposing Copilot's underlying models behind a standard provider id. Unlike the `copilot` plugin — which registers an agent **runtime** (a bare `plugin` surface) — `copilot-proxy` registers a model **provider**, so its models are selectable like any other provider's models. The provider's runtime configuration (credentials, model list, endpoint behavior) is documented on the owning `/providers/...` configuration page rather than on this catalog stub; no specific configuration keys, env vars, or defaults are given in this source page. *(Inferred — beyond the package id, install route, and provider id reproduced above, the source card specifies nothing further; runtime auth/config is not specified in source.)*

**Source**: OpenClaw documentation — `plugins/reference/copilot-proxy` (mirror `inbox/openclaw_docs/plugins/reference/copilot-proxy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
