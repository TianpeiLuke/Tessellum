---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - skills
keywords:
  - open-prose plugin
  - openprose vm skill pack
  - prose slash command
  - openclaw skills surface
  - "@openclaw/open-prose"
  - included in openclaw
  - skills plugin reference
  - bundled skill pack
topics:
  - OpenClaw
  - Plugin Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/open-prose
access_control_group: ["general"]
---

# OpenClaw — The `open-prose` Plugin (OpenProse Skill Pack)

## Overview

This note documents the built-in **`open-prose`** plugin from the OpenClaw plugin-reference inventory, mirroring the `plugins/reference/open-prose` source page. `open-prose` is described in source as an "OpenProse VM skill pack with a /prose slash command" — that is, it is not a model provider but a bundled **skills pack** that contributes a `/prose` slash command to the OpenClaw agent. The page covers two of OpenClaw's fixed plugin-reference H2 sections — `## Distribution` (npm package + install route) and `## Surface` (the capability the plugin contributes); unlike the provider-plugin stubs, this page has **no `## Related docs` section**. This note records what the plugin is, how it is distributed, and the `skills` surface it adds, and links out to OpenClaw's skills / slash-command system rather than restating it.

## Distribution

From the source page's `## Distribution` section, `open-prose` is distributed as an npm package and ships with the runtime:

- **Package**: `@openclaw/open-prose`
- **Install route**: included in OpenClaw

"Included in OpenClaw" means the plugin is bundled with the OpenClaw runtime rather than installed separately — like the other plugin-reference entries, it is a built-in package that the runtime loads, so there is no extra install step to obtain the `/prose` skill pack. The `Package` field (`@openclaw/open-prose`) is the npm package name under OpenClaw's `@openclaw/` scope.

## Surface

From the source page's `## Surface` section, the single contributed surface is:

- **skills**

This is the load-bearing distinction for this plugin: where the model-provider plugins (nvidia, ollama, openai, opencode, opencode-go) contribute a `providers:` surface and `oc-path` contributes a `plugin` (CLI) surface, `open-prose` contributes a **`skills`** surface. A `skills`-surface plugin registers one or more skills into OpenClaw's skills system; here the skill pack is the "OpenProse VM skill pack" named in the lead line, and the user-facing entry point it adds is the **`/prose` slash command**. The skill pack therefore extends what the agent can do (prose / long-form writing, per the lead description) through OpenClaw's slash-command and skills mechanism, rather than by registering a model provider or a CLI subcommand. Per-skill behavior, the contents of the OpenProse VM skill pack, and the precise mechanics of how `/prose` is invoked are not specified on this reference stub; the source page carries only the package, install route, and `skills` surface declaration *(deeper skills/slash-command mechanics live in OpenClaw's skills documentation, linked below — this page links nothing of its own)*.

**Source**: OpenClaw documentation — `plugins/reference/open-prose` (mirror `inbox/openclaw_docs/plugins/reference/open-prose.md`)
**Last Updated**: 2026-06-22
**Status**: Active
