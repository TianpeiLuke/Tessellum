---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - anthropic-vertex plugin
  - openclaw provider plugin
  - claude on google vertex ai
  - claude-fable-5 adaptive thinking
  - openclaw anthropic-vertex-provider
  - clawhub provider install
  - vertex provider surface
topics:
  - OpenClaw
  - Plugins (Reference)
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/anthropic-vertex
access_control_group: ["general"]
---

# OpenClaw — Anthropic Vertex Provider Plugin

## Overview

This note describes the OpenClaw **Anthropic Vertex plugin**, a provider plugin that serves Claude models on Google Vertex AI by registering the `anthropic-vertex` provider into the OpenClaw runtime. It captures the plugin's identity tuple from the `plugins/reference/anthropic-vertex` reference card — its distribution package and install route, the runtime surface it contributes, and the manual `Claude Fable 5` section documenting how the `claude-fable-5` model behaves under thinking/effort controls on Vertex. The card is a short stub; the durable data is the package name, install routes, the provider name, and the Fable 5 thinking/effort behavior, all reproduced verbatim below.

## Distribution

The plugin is distributed as the npm/ClawHub package `@openclaw/anthropic-vertex-provider`. The reference card lists its install routes as **npm; ClawHub** — it can be installed from the npm registry or from the ClawHub plugin registry. The card states the plugin's purpose as "OpenClaw Anthropic Vertex provider plugin for Claude models on Google Vertex AI."

## Surface

The plugin registers a single provider surface: `providers: anthropic-vertex`. That is, installing the plugin adds the `anthropic-vertex` provider name to OpenClaw, through which Claude models hosted on Google Vertex AI become available (e.g., the selectable model id `anthropic-vertex/claude-fable-5`). No `contracts:` capability and no additional surfaces are declared by this reference card.

## Claude Fable 5

The card carries a manual subsection (delimited in source by `openclaw-plugin-reference:manual-start` / `manual-end`) documenting the `claude-fable-5` model on this provider, reproduced verbatim:

- Use `anthropic-vertex/claude-fable-5` where the model is available in your Google Cloud region.
- Fable 5 always uses adaptive thinking and defaults to `high` effort.
- `/think off` and `/think minimal` use `low` effort because the model does not support disabling thinking.

In other words, `claude-fable-5` cannot have its thinking disabled; the `/think off` and `/think minimal` controls map to `low` effort rather than turning thinking off, and the model's default is `high` effort with adaptive thinking. Regional availability on Google Cloud is a precondition for using this model id.

**Source**: OpenClaw documentation — `plugins/reference/anthropic-vertex` (mirror `inbox/openclaw_docs/plugins/reference/anthropic-vertex.md`)
**Last Updated**: 2026-06-22
**Status**: Active
