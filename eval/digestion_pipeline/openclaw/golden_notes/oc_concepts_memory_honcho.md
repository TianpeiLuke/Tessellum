---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - memory
keywords:
  - openclaw honcho memory
  - honcho plugin cross-session memory
  - honcho_context honcho_ask tools
  - openclaw honcho setup
  - plugins.entries openclaw-honcho config
  - honcho before_prompt_build injection
  - honcho vs builtin memory
  - honcho semantic search user modeling
topics:
  - OpenClaw
  - Memory
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/memory-honcho
access_control_group: ["general"]
---

# OpenClaw — Honcho AI-Native Cross-Session Memory Plugin

## Overview

This note is the procedure for setting up and operating the **Honcho** memory backend in OpenClaw, mirroring the `concepts/memory-honcho` source page. [Honcho](https://honcho.dev) is an AI-native memory plugin that persists conversations to a dedicated service (local self-hosted or the managed `api.honcho.dev`) and builds user and agent models over time, giving an agent cross-session context that goes beyond workspace Markdown files. It walks through what the plugin provides, the registered tools the agent can call, the install + `openclaw honcho setup` flow, the `plugins.entries` config block, non-destructive migration of existing workspace memory, how persistence and the `before_prompt_build` injection work, the Honcho-vs-builtin comparison, and the `openclaw honcho` CLI commands.

## What It Provides

The Honcho plugin adds four capabilities on top of OpenClaw's workspace-Markdown memory:

- **Cross-session memory** — conversations are persisted after every turn, so context carries across session resets, compaction, and channel switches.
- **User modeling** — Honcho maintains a profile for each user (preferences, facts, communication style) and for the agent (personality, learned behaviors).
- **Semantic search** — search over observations from past conversations, not just the current session.
- **Multi-agent awareness** — parent agents automatically track spawned sub-agents, with parents added as observers in child sessions.

## Available Tools

Honcho registers tools that the agent can use during conversation, split into fast data-retrieval tools (no LLM call) and an LLM-powered Q&A tool. The data-retrieval tools are `honcho_context` (full user representation across sessions), `honcho_search_conclusions` (semantic search over stored conclusions), `honcho_search_messages` (find messages across sessions, filterable by sender and date), and `honcho_session` (current session history and summary). The Q&A tool is `honcho_ask` — ask about the user, with `depth='quick'` for facts and `depth='thorough'` for synthesis.

## Getting Started

Install the plugin, run setup, and restart the gateway:

```bash
openclaw plugins install @honcho-ai/openclaw-honcho
openclaw honcho setup
openclaw gateway --force
```

The `openclaw honcho setup` command prompts for your API credentials, writes the config, and optionally migrates existing workspace memory files. Per the source, Honcho can run entirely locally (self-hosted) or via the managed API at `api.honcho.dev`; the self-hosted option requires no external dependencies.

## Configuration

Settings live under `plugins.entries["openclaw-honcho"].config`:

```json5
{
  plugins: {
    entries: {
      "openclaw-honcho": {
        config: {
          apiKey: "your-api-key", // omit for self-hosted
          workspaceId: "openclaw", // memory isolation
          baseUrl: "https://api.honcho.dev",
        },
      },
    },
  },
}
```

The config keys are `apiKey` (omit for self-hosted), `workspaceId` (used for memory isolation, e.g. `"openclaw"`), and `baseUrl` (the Honcho service endpoint). For self-hosted instances, point `baseUrl` to your local server (for example `http://localhost:8000`) and omit the API key.

## Migrating Existing Memory

If you have existing workspace memory files (`USER.md`, `MEMORY.md`, `IDENTITY.md`, `memory/`, `canvas/`), `openclaw honcho setup` detects and offers to migrate them. Per the source, migration is **non-destructive** — files are uploaded to Honcho, and the originals are never deleted or moved.

## How It Works

After every AI turn, the conversation is persisted to Honcho. Both user and agent messages are observed, allowing Honcho to build and refine its models over time. During conversation, Honcho tools query the service in the `before_prompt_build` phase, injecting relevant context before the model sees the prompt; per the source, querying in this phase ensures accurate turn boundaries and relevant recall.

## Honcho vs Builtin Memory

The source page contrasts Honcho with the builtin/QMD workspace-Markdown memory across six dimensions:

| | Builtin / QMD | Honcho |
| --- | --- | --- |
| **Storage** | Workspace Markdown files | Dedicated service (local or hosted) |
| **Cross-session** | Via memory files | Automatic, built-in |
| **User modeling** | Manual (write to MEMORY.md) | Automatic profiles |
| **Search** | Vector + keyword (hybrid) | Semantic over observations |
| **Multi-agent** | Not tracked | Parent/child awareness |
| **Dependencies** | None (builtin) or QMD binary | Plugin install |

Honcho and the builtin memory system can work together. When QMD is configured, additional tools become available for searching local Markdown files alongside Honcho's cross-session memory.

## CLI Commands

The `openclaw honcho` command surface covers setup, status, and ad-hoc querying:

```bash
openclaw honcho setup                        # Configure API key and migrate files
openclaw honcho status                       # Check connection status
openclaw honcho ask <question>               # Query Honcho about the user
openclaw honcho search <query> [-k N] [-d D] # Semantic search over memory
```

`openclaw honcho ask` queries Honcho about the user, and `openclaw honcho search` runs a semantic search over memory with optional `-k N` (count) and `-d D` (date) flags.

**Source**: OpenClaw documentation — `concepts/memory-honcho` (mirror `inbox/openclaw_docs/concepts/memory-honcho.md`)
**Last Updated**: 2026-06-22
**Status**: Active
