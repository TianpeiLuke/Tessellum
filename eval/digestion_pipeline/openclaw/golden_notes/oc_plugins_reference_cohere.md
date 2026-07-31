---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw cohere plugin
  - cohere provider plugin
  - "@openclaw/cohere-provider"
  - clawhub cohere provider
  - providers cohere surface
  - cohere embeddings provider
  - openclaw provider plugin reference
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/cohere
access_control_group: ["general"]
---

# OpenClaw — Cohere Provider Plugin (Reference)

## Overview

This note is the reference card for the OpenClaw **Cohere provider plugin**, mirroring the `plugins/reference/cohere` source page. The page is a machine-generated catalog stub describing one distributable plugin: its package id, its install routes, and the runtime *surface* it contributes to the gateway. The source summary describes it simply as the "OpenClaw Cohere provider plugin." This card captures the two load-bearing facts — the **Distribution** line (package + install route) and the **Surface** line (which provider id the plugin registers) — and points at the upstream provider-configuration doc for setup details. The plugin's job is to register the `cohere` model provider so OpenClaw agents can reach Cohere's hosted models (chat plus Cohere's embedding/rerank line) through the standard provider surface.

## Distribution

The plugin is packaged and distributed as follows (verbatim from the source page):

- Package: `@openclaw/cohere-provider`
- Install route: included in OpenClaw; npm; ClawHub: `clawhub:@openclaw/cohere-provider`

It is therefore available three ways: bundled (included in OpenClaw), via the npm registry, and via ClawHub using the `clawhub:@openclaw/cohere-provider` reference. The `@openclaw/cohere-provider` package name is the canonical identifier for the plugin across all three routes.

## Surface

The plugin contributes one runtime surface (verbatim from the source page):

```
providers: cohere
```

Registering `providers: cohere` adds the `cohere` model provider to OpenClaw's provider/model catalog. The source page declares only this single `providers:` entry — it does not declare any capability contracts (no `imageGenerationProviders`, `mediaUnderstandingProviders`, `speechProviders`, etc.). Any per-model details, credential keys, or configuration options for the Cohere provider live on the provider-configuration page linked under Related docs and are not duplicated here.

**Source**: OpenClaw documentation — `plugins/reference/cohere` (mirror `inbox/openclaw_docs/plugins/reference/cohere.md`)
**Last Updated**: 2026-06-22
**Status**: Active
