---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw voyage plugin
  - voyage-provider
  - memory embedding provider
  - memoryEmbeddingProviders contract
  - voyage embedding support
  - bundled provider plugin
  - openclaw memory embeddings
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/voyage
access_control_group: ["general"]
---

# OpenClaw — Voyage Plugin (`@openclaw/voyage-provider`) Descriptor

## Overview

This note is the plugin-descriptor card for the OpenClaw **Voyage plugin**, mirroring the `plugins/reference/voyage` source page. It captures the plugin's identity — its npm package, install route, and the single contract surface it registers — as the load-bearing facts: the Voyage plugin "Adds memory embedding provider support" by registering a `memoryEmbeddingProviders` surface, which wires Voyage AI embeddings into OpenClaw's memory subsystem. The source page is intentionally compact (a descriptor stub with two H2 sections — `## Distribution` and `## Surface`, no "Related docs" section), so this card states only the package + surface and defers the deeper memory/embedding behavior to the linked memory-concept and embedding-provider docs rather than redefining it here.

## Distribution

- **Package:** `@openclaw/voyage-provider`
- **Install route:** included in OpenClaw

The Voyage plugin ships bundled — its install route is "included in OpenClaw", meaning it is part of the base distribution and is not separately installed from npm or ClawHub the way add-on plugins are. The package identifier is `@openclaw/voyage-provider`.

## Surface

The plugin registers one contract surface:

- **contracts: memoryEmbeddingProviders**

This `memoryEmbeddingProviders` contract is the capability the plugin adds: it contributes a Voyage embedding provider to OpenClaw's memory layer, so that text stored in or queried against OpenClaw memory can be embedded with Voyage AI's embedding models. As the page summary states, the plugin "Adds memory embedding provider support." The deeper behavior of how embeddings are generated, indexed, and searched within OpenClaw memory belongs to the memory/embedding concept docs (linked under Related Notes), not to this descriptor card.

**Source**: OpenClaw documentation — `plugins/reference/voyage` (mirror `inbox/openclaw_docs/plugins/reference/voyage.md`)
**Last Updated**: 2026-06-22
**Status**: Active
