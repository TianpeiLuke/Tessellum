---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw provider plugins
  - minimax mistral moonshot novita
  - model provider plugin manifest
  - provider plugin surface contracts
  - openclaw-minimax-provider package
  - imageGenerationProviders speechProviders
  - mediaUnderstandingProviders memoryEmbeddingProviders
  - realtimeTranscriptionProviders webSearchProviders
  - included in OpenClaw install route
topics:
  - OpenClaw
  - Provider Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/minimax
access_control_group: ["general"]
---

# OpenClaw — Built-in Model/Media Provider Plugins (Reference Catalog)

## Overview

This note is a reference catalog of OpenClaw's four built-in **model/media provider plugins** — MiniMax, Mistral, Moonshot, and Novita — consolidating the machine-generated manifest stubs at `plugins/reference/minimax`, `plugins/reference/mistral`, `plugins/reference/moonshot`, and `plugins/reference/novita`. Each manifest page shares an identical three-H2 skeleton — `## Distribution` (npm package + install route), `## Surface` (the `providers:` identifiers the plugin registers and the typed `contracts:` it satisfies), and `## Related docs` (a pointer to the per-provider setup page under `/providers/<name>`) — preceded by a one-sentence summary. This catalog answers the index-layer question "which built-in plugin provides which model/media capability, and how is it shipped"; the substantive per-provider setup and configuration lives on the linked `/providers/<name>` pages and is NOT duplicated here.

## Distribution (Package + Install Route)

Every one of the four provider plugins ships as a scoped npm package under the `@openclaw/` namespace and is **included in OpenClaw** (bundled — no separate install step), per each page's `## Distribution` H2:

| Plugin | Package | Install route |
|---|---|---|
| MiniMax | `@openclaw/minimax-provider` | included in OpenClaw |
| Mistral | `@openclaw/mistral-provider` | included in OpenClaw |
| Moonshot | `@openclaw/moonshot-provider` | included in OpenClaw |
| Novita | `@openclaw/novita-provider` | included in OpenClaw |

All four use the identical naming convention `@openclaw/<name>-provider` and the same "included in OpenClaw" install route — these are bundled built-in provider plugins, not separately-installed npm/ClawHub packages (in contrast to the channel plugins, which install via npm/ClawHub).

## Surface (Registered Providers + Contracts)

The `## Surface` H2 of each manifest declares two facts: the `providers:` identifiers the plugin registers into OpenClaw's model catalog (model-selection aliases), and the typed `contracts:` (capability surfaces) the plugin satisfies. The provider identifiers per plugin, verbatim from source:

| Plugin | `providers:` (registered identifiers) |
|---|---|
| MiniMax | `minimax`, `minimax-portal` |
| Mistral | `mistral` |
| Moonshot | `moonshot` |
| Novita | `novita`, `novita-ai`, `novitaai` |

MiniMax registers two identifiers (`minimax`, `minimax-portal`); Novita registers three aliases (`novita`, `novita-ai`, `novitaai`) for the same provider; Mistral and Moonshot each register a single identifier.

The typed `contracts:` (Surface capabilities) each provider plugin satisfies, verbatim from source:

| Plugin | `contracts:` |
|---|---|
| MiniMax | `imageGenerationProviders`, `mediaUnderstandingProviders`, `musicGenerationProviders`, `speechProviders`, `videoGenerationProviders`, `webSearchProviders` |
| Mistral | `mediaUnderstandingProviders`, `memoryEmbeddingProviders`, `realtimeTranscriptionProviders` |
| Moonshot | `mediaUnderstandingProviders`, `webSearchProviders` |
| Novita | *(none listed — the `## Surface` H2 declares only `providers: novita, novita-ai, novitaai`)* |

MiniMax is the broadest media surface of the four, satisfying six contracts spanning image generation, media understanding, music generation, speech, video generation, and web search. Mistral is the only plugin satisfying `memoryEmbeddingProviders` (embeddings for memory search) and `realtimeTranscriptionProviders` (streaming speech-to-text). Moonshot satisfies the two text-adjacent contracts `mediaUnderstandingProviders` and `webSearchProviders`. The Novita manifest's `## Surface` lists `providers:` only and declares no `contracts:` — *(no `contracts:` are stated in the Novita source; not specified in source)*. The contract identifiers above are OpenClaw plugin-Surface vocabulary, copied character-for-character from the manifests; they are not described further here (see the linked Hermes/OpenClaw surface-taxonomy doc for what each contract means).

**Source**: OpenClaw documentation — `plugins/reference/{minimax,mistral,moonshot,novita}` (mirror `inbox/openclaw_docs/plugins/reference/*.md`)
**Last Updated**: 2026-06-22
**Status**: Active
