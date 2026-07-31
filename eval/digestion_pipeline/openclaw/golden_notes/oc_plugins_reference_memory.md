---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - memory
keywords:
  - openclaw memory plugins
  - memory-core plugin
  - memory-lancedb plugin
  - memory-wiki plugin
  - lancedb long-term memory
  - auto-recall auto-capture vector search
  - obsidian knowledge vault
  - plugin distribution surface contracts
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/memory-core
access_control_group: ["general"]
---

# OpenClaw — Memory Plugins (memory-core, memory-lancedb, memory-wiki)

## Overview

This note models OpenClaw's three first-party **memory plugins** as plugin-reference cards, mirroring the `plugins/reference/memory-core`, `plugins/reference/memory-lancedb`, and `plugins/reference/memory-wiki` source pages. Each plugin is an `@openclaw/<name>` package described by two fixed reference-card facets — its **Distribution** (package name + install route) and its **Surface** (the declared contract types the plugin contributes). The three cards together form OpenClaw's "memory plugin family": `memory-core` adds agent-callable memory tools, `memory-lancedb` adds a LanceDB-backed long-term memory store with auto-recall / auto-capture / vector search, and `memory-wiki` is a persistent wiki compiler that maintains an Obsidian-friendly knowledge vault. The long-form `/plugins/memory-lancedb` and `/plugins/memory-wiki` guide pages are linked (under References) rather than duplicated — this card series covers only the `plugins/reference/*` summary cards.

## Memory Core (`@openclaw/memory-core`)

Per the `memory-core` card, the plugin summary is **"Adds agent-callable tools."** — it contributes the baseline memory tool surface that the agent can call directly.

- **Distribution** — Package: `@openclaw/memory-core`; Install route: **included in OpenClaw** (bundled, no separate install step).
- **Surface** — contracts: **tools**. The plugin's declared contract surface is the `tools` contract, i.e. it registers agent-callable tools.

The card carries no further config, requirements, or troubleshooting content beyond Distribution and Surface; deeper memory internals live in the code-side memory subsystem (linked under Related Notes), not in this reference card.

## Memory LanceDB (`@openclaw/memory-lancedb`)

Per the `memory-lancedb` card, the plugin is the **"OpenClaw LanceDB-backed long-term memory plugin with auto-recall, auto-capture, and vector search."** It backs long-term memory with **LanceDB** (a vector database) and provides three named capabilities — **auto-recall**, **auto-capture**, and **vector search**.

- **Distribution** — Package: `@openclaw/memory-lancedb`; Install route: **npm; ClawHub** (distributed via npm and the ClawHub plugin registry, i.e. NOT bundled — it is an opt-in install).
- **Surface** — contracts: **tools**. Its declared contract surface is the `tools` contract.
- **Related docs** — the card links the long-form guide `memory-lancedb` at `/plugins/memory-lancedb`; that guide page (LanceDB internals, vector-search configuration) is owned by the long-form plugins guide series and is referenced under References, not duplicated here.

LanceDB itself is the vector store backing this plugin; the embedding and similarity-recall mechanics it relies on are the vector-database / embedding / information-retrieval concepts linked under Related Notes (this card documents only the plugin's distribution and contract surface, not LanceDB internals).

## Memory Wiki (`@openclaw/memory-wiki`)

Per the `memory-wiki` card, the plugin is a **"Persistent wiki compiler and Obsidian-friendly knowledge vault for OpenClaw."** — it compiles a persistent wiki and maintains a knowledge vault whose layout is compatible with Obsidian.

- **Distribution** — Package: `@openclaw/memory-wiki`; Install route: **included in OpenClaw** (bundled).
- **Surface** — contracts: **tools; skills**. This plugin declares **two** contract surfaces — the `tools` contract (agent-callable tools) **and** the `skills` contract (packaged agent skills) — making it the broadest-surface card of the three memory plugins.
- **Related docs** — the card links the long-form guide `memory-wiki` at `/plugins/memory-wiki`; that guide page is owned by the long-form plugins guide series and is referenced under References, not duplicated here.

## Card Comparison

The three cards share the fixed `## Distribution` / `## Surface` reference-card schema; the only differences are package name, install route, and the declared contract surface(s):

| Plugin | Package | Install route | Contract surface |
|---|---|---|---|
| Memory Core | `@openclaw/memory-core` | included in OpenClaw | tools |
| Memory LanceDB | `@openclaw/memory-lancedb` | npm; ClawHub | tools |
| Memory Wiki | `@openclaw/memory-wiki` | included in OpenClaw | tools; skills |

Two of the three (`memory-core`, `memory-wiki`) are bundled with OpenClaw, while `memory-lancedb` is the opt-in npm/ClawHub install; `memory-wiki` is the only one of the three declaring the `skills` contract in addition to `tools`. The cards record no version numbers, no config keys, and no defaults beyond the above — any such value would be fabrication and is *not specified in source*.

**Source**: OpenClaw documentation — `plugins/reference/memory-core`, `plugins/reference/memory-lancedb`, `plugins/reference/memory-wiki` (mirror `inbox/openclaw_docs/plugins/reference/memory-*.md`)
**Last Updated**: 2026-06-22
**Status**: Active
