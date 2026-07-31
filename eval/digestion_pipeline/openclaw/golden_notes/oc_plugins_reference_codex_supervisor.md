---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - codex supervisor plugin
  - openclaw codex-supervisor
  - codex_sessions_list
  - include_stored stored sessions
  - max_stored_sessions cap
  - codex app-server supervision
  - tools contract surface
  - openclaw bundled plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/codex-supervisor
access_control_group: ["general"]
---

# OpenClaw — Codex Supervisor Plugin Reference

## Overview

This note is the procedure-level reference card for the OpenClaw **Codex Supervisor** plugin, mirroring the `plugins/reference/codex-supervisor` source page. The plugin's stated purpose is to "Supervise Codex app-server sessions from OpenClaw." It covers how to obtain and enable the plugin (its **Distribution** package and install route), the contract **Surface** it registers (`contracts: tools`), and the one operational tool it documents — the `codex_sessions_list` **Session Listing** behavior, including the `include_stored` and `max_stored_sessions` parameters and the stored-session cap. These are the load-bearing facts an operator needs to discover and audit which plugin supervises Codex sessions; the deeper Codex harness internals live on the linked codex-harness page and are reached via `## Related Notes`.

## Distribution

The plugin is published and enabled as follows (copied verbatim from the source card):

- Package: `@openclaw/codex-supervisor`
- Install route: included in OpenClaw

Because the install route is "included in OpenClaw," this is a bundled (built-in) plugin — it ships with OpenClaw and does not require a separate npm install or a ClawHub (`clawhub:`) install slug. No additional install command is documented on the source card.

## Surface

The plugin registers the following contract surface (verbatim from source):

```
contracts: tools
```

This means the Codex Supervisor contributes to the `tools` contract surface — it exposes one or more agent-callable tools (rather than a model `providers` surface or a `channels` surface). The `codex_sessions_list` tool documented under Session Listing is the concrete tool registered through this `tools` surface.

## Session Listing

The source card documents one tool and its parameters; the facts below are reproduced exactly from the page. `codex_sessions_list` defaults to **loaded Codex sessions only**. Set `include_stored` to include stored history; when `include_stored` is set, the plugin uses Codex app-server's **state-DB-only listing path** and caps stored results at **200 by default**. Pass `max_stored_sessions` to lower or raise that cap, **up to 1000**. (The page does not specify any other parameters, defaults, or return shape — *not specified in source*.)

Summarized as an operator-facing parameter reference (all values verbatim from the card):

| Parameter | Effect | Default / bound |
|---|---|---|
| (none) | `codex_sessions_list` lists loaded Codex sessions only | loaded-only by default |
| `include_stored` | Also include stored history via Codex app-server's state-DB-only listing path | stored results capped at 200 by default |
| `max_stored_sessions` | Lower or raise the stored-results cap | up to 1000 |

**Source**: OpenClaw documentation — `plugins/reference/codex-supervisor` (mirror `inbox/openclaw_docs/plugins/reference/codex-supervisor.md`)
**Last Updated**: 2026-06-22
**Status**: Active
