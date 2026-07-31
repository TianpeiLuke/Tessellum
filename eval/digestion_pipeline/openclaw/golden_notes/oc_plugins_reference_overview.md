---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw plugin reference card
  - distribution surface schema
  - contract surface types
  - tools skills speechproviders
  - providers imagegenerationproviders migrationproviders
  - openclaw plugin package install route
  - plugin reference manual markers
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/memory-core
access_control_group: ["general"]
---

# OpenClaw — The Plugin-Reference Card Schema

## Overview

This note is the cross-cutting **concept** that ties together OpenClaw's `plugins/reference/*` pages — the auto-generated reference cards, one per first-party `@openclaw/*` plugin package. It abstracts the shared two-part card schema (`## Distribution` + `## Surface`) and enumerates the **contract-surface vocabulary** (`tools`, `skills`, `speechProviders`, `providers`, `imageGenerationProviders`, `migrationProviders`) that appears across the pl14 plugin families — memory (`memory-core`, `memory-lancedb`, `memory-wiki`), Microsoft (`microsoft-speech`, `microsoft-foundry`), and migration (`migrate-claude`, `migrate-hermes`). Rather than re-explaining the schema in each family card, this hub defines it once, mirroring the structure observed verbatim across all seven `plugins/reference/` mirror pages.

## What a Plugin-Reference Card Is

Each `plugins/reference/<name>` page is a compact card describing exactly one OpenClaw plugin: what package it ships as, how it is installed, and what contract surface it contributes to the agent. The cards share a fixed skeleton — a one-line `summary` and `read_when` hint in YAML frontmatter, an H1 plugin title, the summary repeated as the opening sentence, then `## Distribution` and `## Surface` sections. A card may add an optional `## Related docs` section that links to the plugin's long-form guide page (for example the `memory-lancedb` card links to the `/plugins/memory-lancedb` guide and the `memory-wiki` card links to the `/plugins/memory-wiki` guide). The `read_when` frontmatter is uniform across the family: "You are installing, configuring, or auditing the `<name>` plugin." This card is the package-and-contract index entry; the operational depth (config, requirements, troubleshooting) lives in a card only when the plugin warrants it (see Auto-Generated vs Manual Content below).

## The `## Distribution` Block — Package + Install Route

The `## Distribution` block answers "where does this plugin come from and how is it installed." It always declares two fields:

- **Package** — the npm package name, always namespaced `@openclaw/<name>`. Observed across pl14: `@openclaw/memory-core`, `@openclaw/memory-lancedb`, `@openclaw/memory-wiki`, `@openclaw/microsoft-speech`, `@openclaw/microsoft-foundry`, `@openclaw/migrate-claude`, `@openclaw/migrate-hermes`. (Note the `microsoft` card's package is `@openclaw/microsoft-speech`, not `@openclaw/microsoft`.)
- **Install route** — how the package reaches a deployment. Two values appear in pl14: `included in OpenClaw` (bundled — the default for six of the seven cards) and `npm; ClawHub` (`memory-lancedb` is the lone pl14 card distributed via npm and ClawHub rather than bundled). The bundled route means the plugin ships with OpenClaw and needs no separate install step; the `npm; ClawHub` route means it is fetched from the npm registry or the ClawHub plugin index.

The package name plus install route is the first half of the card schema — the *distribution* half. It maps to OpenClaw's plugin/extension host, which loads bundled plugins at startup and fetches npm/ClawHub plugins on demand.

## The `## Surface` Block — Declared Contract Surface

The `## Surface` block is the second half of the schema — the *contract* half. It declares what the plugin contributes to the agent runtime, written as a terse `key: value[; key: value]` line. Two declaration kinds appear: `contracts:` (capability contributions registered against a named contract) and `providers:` (a named provider this plugin registers). Across pl14, the `## Surface` values are:

- `contracts: tools` — `memory-core`, `memory-lancedb` (agent-callable tools).
- `contracts: tools; skills` — `memory-wiki` (both agent-callable tools and packaged skills).
- `contracts: speechProviders` — `microsoft-speech` (a text-to-speech provider).
- `providers: microsoft-foundry; contracts: imageGenerationProviders` — `microsoft-foundry` (registers a named model provider *and* an image-generation contract contribution).
- `contracts: migrationProviders` — `migrate-claude`, `migrate-hermes` (config/skill/credential importers).

A single plugin can declare multiple surface entries (`memory-wiki` declares two contracts; `microsoft-foundry` declares both a provider and a contract). The surface line is the machine-readable index of what a plugin plugs into; the named contract values are the shared vocabulary defined next.

## Contract-Surface Vocabulary (Cross-Family)

The contract-surface names appearing across the pl14 cards form a small enumerated vocabulary. Each name is the contract a plugin's contribution registers against in OpenClaw's plugin/extension framework:

- **`tools`** — agent-callable tools (functions the model can invoke). Declared by `memory-core`, `memory-lancedb`, and `memory-wiki`. This is the function-calling surface — the most common plugin contribution.
- **`skills`** — packaged agent capabilities (skill bundles). Declared by `memory-wiki` alongside its tools.
- **`speechProviders`** — text-to-speech provider registration. Declared by `microsoft-speech` (Azure TTS).
- **`providers`** — a named model/inference provider. Declared by `microsoft-foundry` as `providers: microsoft-foundry`.
- **`imageGenerationProviders`** — an image-generation provider contribution (the `image_generate` capability). Declared by `microsoft-foundry`.
- **`migrationProviders`** — importers that bring another agent's configuration into OpenClaw. Declared by both `migrate-claude` and `migrate-hermes`.

These six names span the breadth of plugin contributions in pl14: capability surfaces (`tools`, `skills`), modality providers (`speechProviders`, `providers`, `imageGenerationProviders`), and onboarding importers (`migrationProviders`). The individual family cards (`oc_plugins_reference_memory`, `oc_plugins_reference_microsoft_foundry`, `oc_plugins_reference_microsoft_speech`, `oc_plugins_reference_migration`) document which plugin declares which surface; this overview holds the vocabulary itself.

## Auto-Generated vs Manual Content (The `manual-*` Markers)

Most reference cards are thin auto-generated stubs — the six non-Foundry pl14 cards are 43–67 words, carrying only `summary`, H1, the one-line description, `## Distribution`, `## Surface`, and (for two memory cards) `## Related docs`. The `microsoft-foundry` card is the exception: it carries a hand-authored content block delimited by HTML comment markers — `<!-- openclaw-plugin-reference:manual-start -->` ... `<!-- openclaw-plugin-reference:manual-end -->`. Inside those markers a card may add an explicit capability summary line plus operational sections (`## Requirements`, `## Chat models`, `## MAI image generation`, `## Troubleshooting`). The markers signal which content is operator-authored and preserved across regeneration versus auto-derived from the package's declared distribution and surface. A card without `manual-*` markers is purely the auto-generated package-and-contract index entry.

## How the Schema Maps to OpenClaw's Plugin Architecture

The card schema is a documentation projection of OpenClaw's plugin/extension model: the *Distribution* half (package + install route) corresponds to how the extension host discovers and loads a plugin (bundled at startup vs npm/ClawHub on demand), and the *Surface* half (contract/provider declarations) corresponds to what the plugin registers with the runtime once loaded. The named contracts (`tools`, `skills`, `speechProviders`, `providers`, `imageGenerationProviders`, `migrationProviders`) are registration points in the framework — a plugin contributes one or more, and the agent loop, voice/speech layer, model-provider layer, image-generation path, or onboarding wizard consume them respectively. This is the same package-plus-declared-contract model that sibling coding agents (Hermes, Claude Code, Pi) expose; the cross-tool framing is captured in the related plugin-system docs below.

**Source**: OpenClaw documentation — `plugins/reference/*` cards (mirror `inbox/openclaw_docs/plugins/reference/{memory-core,memory-lancedb,memory-wiki,microsoft,microsoft-foundry,migrate-claude,migrate-hermes}.md`)
**Last Updated**: 2026-06-22
**Status**: Active
