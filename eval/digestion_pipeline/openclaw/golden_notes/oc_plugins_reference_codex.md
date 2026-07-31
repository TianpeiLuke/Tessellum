---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw codex plugin
  - codex app-server harness
  - codex model provider
  - codex-managed gpt catalog
  - "@openclaw/codex package"
  - codex provider surface
  - mediaunderstandingproviders migrationproviders websearchproviders
  - codex plugin install npm clawhub
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/codex
access_control_group: ["general"]
---

# OpenClaw — Codex Plugin Reference

## Overview

This procedure note is the reference card for the OpenClaw **Codex plugin**, mirroring the `plugins/reference/codex` source page. The card states what the plugin is, how to install it (its **Distribution** package and install route), and which contract **Surface** it registers — the facts an operator needs to discover, install, or audit which plugin owns the Codex capability. The Codex plugin is an **OpenClaw Codex app-server harness and model provider plugin with a Codex-managed GPT catalog**: it brings up the Codex app-server runtime as a harness and simultaneously registers a model provider exposing a Codex-managed catalog of GPT models. The card's `Related docs` pointer hands off the deeper harness internals (configuration, runtime behavior) to the Codex harness page; this note links to that deeper page in `## Related Notes` rather than duplicating it.

## Distribution

- **Package**: `@openclaw/codex`
- **Install route**: npm; ClawHub

The plugin is distributed as the npm package `@openclaw/codex` and can be installed either from npm or from ClawHub (OpenClaw's plugin registry). The source card does not specify a ClawHub `clawhub:` install slug, default-enabled status, or version pinning — *(not specified in source)*.

## Surface

The Codex plugin registers the following contract surfaces (verbatim from the card):

```
providers: codex; contracts: mediaUnderstandingProviders, migrationProviders, webSearchProviders
```

- **`providers: codex`** — it registers the `codex` model provider, which feeds the Codex-managed GPT catalog into OpenClaw's model layer (making those GPT models selectable/routable once the provider is registered).
- **`contracts: mediaUnderstandingProviders`** — a media-understanding contract surface (e.g., image/media interpretation capability) contributed by the harness.
- **`contracts: migrationProviders`** — a migration contract surface (migration-helper capability) contributed by the harness.
- **`contracts: webSearchProviders`** — a web-search contract surface, registering Codex as a web-search provider.

Because the plugin is both a harness and a provider, a single install both stands up the Codex app-server runtime and registers these provider + contract surfaces. The source card does not enumerate per-contract configuration keys; those live in the deeper Codex harness page linked below — *(not specified in source)*.

**Source**: OpenClaw documentation — `plugins/reference/codex` (mirror `inbox/openclaw_docs/plugins/reference/codex.md`)
**Last Updated**: 2026-06-22
**Status**: Active
