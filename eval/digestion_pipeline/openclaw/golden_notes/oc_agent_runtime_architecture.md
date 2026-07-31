---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - agent_runtime
keywords:
  - openclaw agent runtime architecture
  - src/agents embedded-agent-runner
  - packages/agent-core
  - openclaw/plugin-sdk barrels
  - core vs plugin boundaries
  - resource package manifests
  - runtime selection openclaw auto
  - plugin harness runtime id
topics:
  - OpenClaw
  - Agent Runtime Architecture
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/agent-runtime-architecture
access_control_group: ["general"]
---

# OpenClaw — Built-in Agent Runtime Architecture

## Overview

This note describes the **built-in OpenClaw agent runtime** that OpenClaw owns directly — its module layout, the core-vs-plugin boundaries it enforces, the resource-package manifests that declare extensions/skills/prompts/themes, and how a runtime id is selected. It mirrors the top-level `agent-runtime-architecture` source page, which frames the runtime as code under `src/agents/`, model/provider helpers under `src/llm/`, and plugin-facing contracts exposed through `openclaw/plugin-sdk/*` barrels. The runtime is a `concept` note: it documents the structural layout and rules of the runtime, not a step-by-step procedure or a single algorithm.

## Runtime Layout

OpenClaw owns the built-in agent runtime directly. The runtime code lives under `src/agents/`, model/provider helpers live under `src/llm/`, and plugin-facing contracts are exposed through `openclaw/plugin-sdk/*` barrels. The page enumerates the following modules of the layout:

- **`src/agents/embedded-agent-runner/`** — the built-in agent attempt loop, provider stream adapters, compaction, model selection, and session wiring.
- **`src/agents/sessions/`** — session persistence, extension loading, resource discovery, skills, prompts, themes, and TUI-backed tool renderers.
- **`packages/agent-core/`** — the reusable agent core: lower-level harness types, messages, compaction helpers, prompt templates, and tool/session contracts.
- **`src/agents/runtime/`** — the OpenClaw facade for `@openclaw/agent-core` plus local proxy utilities.
- **`src/agents/agent-tools*.ts`** — OpenClaw-owned tool definitions, schemas, policy, before/after hook adapters, and host edit support.
- **`src/agents/agent-hooks/`** — built-in runtime hooks such as compaction safeguards and context pruning.
- **`src/llm/`** — the model/provider registry, transport helpers, and provider-specific stream implementations.

## Boundaries

Two boundary rules separate core code from plugins. Core code calls the built-in runtime through OpenClaw modules and SDK barrels, **not** through old external agent packages. Plugins use documented `openclaw/plugin-sdk/*` entrypoints and **do not import `src/**` internals**.

One third-party exception is called out explicitly: `@earendil-works/pi-tui` remains a third-party TUI dependency. It is used as a terminal component toolkit by the local TUI and session renderers; internalizing it would be a separate vendoring effort.

## Manifests

Resource packages declare OpenClaw resources in package metadata. The manifest is an `openclaw` key in the package metadata that maps each resource type to a glob list:

```json
{
  "openclaw": {
    "extensions": ["extensions/index.ts"],
    "skills": ["skills/*.md"],
    "prompts": ["prompts/*.md"],
    "themes": ["themes/*.json"]
  }
}
```

Beyond the explicit manifest, the package manager also discovers conventional `extensions/`, `skills/`, `prompts/`, and `themes/` directories, so a resource package can rely on either declared globs or directory conventions.

## Runtime Selection

The default built-in runtime id is `openclaw`. Plugin harnesses can register additional runtime ids. The `auto` id selects a supporting plugin harness when one exists and otherwise uses the built-in OpenClaw runtime.

**Source**: OpenClaw documentation — `agent-runtime-architecture` (mirror `inbox/openclaw_docs/agent-runtime-architecture.md`)
**Last Updated**: 2026-06-22
**Status**: Active
