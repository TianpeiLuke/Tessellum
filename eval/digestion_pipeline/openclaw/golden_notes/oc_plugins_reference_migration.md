---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - migration
keywords:
  - openclaw migration plugins
  - migrate-claude plugin
  - migrate-hermes plugin
  - migrationProviders contract
  - import claude code config
  - import hermes config memories skills
  - bundled openclaw plugins
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/migrate-claude
access_control_group: ["general"]
---

# OpenClaw — Migration Plugins (`migrate-claude`, `migrate-hermes`)

## Overview

This note is the reference card for OpenClaw's two first-party **migration plugins** — `migrate-claude` and `migrate-hermes` — consolidating the `plugins/reference/migrate-claude` and `plugins/reference/migrate-hermes` source pages. Both are bundled (included-in-OpenClaw) plugins that import an existing coding-agent setup into OpenClaw, and both declare the same `migrationProviders` contract surface. `migrate-claude` imports Claude Code and Claude Desktop instructions, MCP servers, skills, and safe configuration; `migrate-hermes` imports Hermes configuration, memories, skills, and supported credentials. This card models each plugin's distribution (package name + install route) and its declared contract surface, exactly as the two reference-card pages declare them.

## Migrate Claude plugin

The `migrate-claude` plugin "Imports Claude Code and Claude Desktop instructions, MCP servers, skills, and safe configuration into OpenClaw." The source page's `read_when` guidance is: "You are installing, configuring, or auditing the migrate-claude plugin."

### Distribution

- **Package**: `@openclaw/migrate-claude`
- **Install route**: included in OpenClaw

### Surface

- **contracts**: `migrationProviders`

The plugin registers a `migrationProviders` contract that reads a Claude Code / Claude Desktop environment and imports four kinds of material into OpenClaw: instructions, MCP servers, skills, and safe configuration. The exact import mechanics, field-by-field mappings, and what "safe configuration" filters out are *not specified in source* (the reference card declares only the package, install route, and contract surface).

## Migrate Hermes plugin

The `migrate-hermes` plugin "Imports Hermes configuration, memories, skills, and supported credentials into OpenClaw." The source page's `read_when` guidance is: "You are installing, configuring, or auditing the migrate-hermes plugin."

### Distribution

- **Package**: `@openclaw/migrate-hermes`
- **Install route**: included in OpenClaw

### Surface

- **contracts**: `migrationProviders`

The plugin registers a `migrationProviders` contract that reads a Hermes environment and imports four kinds of material into OpenClaw: configuration, memories, skills, and supported credentials. The qualifier "supported credentials" indicates that only a subset of Hermes credential types is portable; which credential types are supported, and the precise import flow, are *not specified in source*.

## Shared Contract Surface

Both migration plugins expose the same single contract surface — `migrationProviders` — and share the same distribution model (bundled, "included in OpenClaw", no separate install route). They differ only in their source agent and the set of material each imports: `migrate-claude` reads Claude Code / Claude Desktop (instructions, MCP servers, skills, safe configuration), while `migrate-hermes` reads Hermes (configuration, memories, skills, supported credentials). Both list **skills** as a shared import target; `migrate-claude` additionally imports MCP servers, and `migrate-hermes` additionally imports memories and supported credentials. The `migrationProviders` contract surface that both declare is the schema vocabulary abstracted in the pl14 card-schema overview note; this card documents only the two migration providers' concrete declarations.

**Source**: OpenClaw documentation — `plugins/reference/migrate-claude` + `plugins/reference/migrate-hermes` (mirror `inbox/openclaw_docs/plugins/reference/migrate-claude.md`, `migrate-hermes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
