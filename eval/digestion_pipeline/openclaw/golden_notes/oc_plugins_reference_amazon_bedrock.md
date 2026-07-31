---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw amazon bedrock plugin
  - amazon-bedrock-provider
  - bedrock model provider plugin
  - bedrock model discovery
  - memoryEmbeddingProviders contract
  - bedrock guardrails
  - bedrock embeddings
  - openclaw plugin distribution surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/amazon-bedrock
access_control_group: ["general"]
---

# OpenClaw — Amazon Bedrock Plugin (Reference)

## Overview

This note is the generated plugin-reference descriptor for the OpenClaw **Amazon Bedrock plugin**, mirroring the `plugins/reference/amazon-bedrock` source page. The page's one-line summary describes it as the "OpenClaw Amazon Bedrock provider plugin with model discovery, embeddings, and guardrail support." As a reference-catalog entry (not a setup guide), it records exactly two load-bearing facts — the plugin's **Distribution** (npm package id + install route) and its **Surface** (the providers and contracts it registers into the agent runtime) — plus a **Related docs** pointer to the fuller Bedrock provider documentation. This is a `concept` (plugin descriptor) note: it states what the plugin is and what it registers; it does NOT enumerate model lists, config keys, AWS regions, or setup steps, none of which the source page provides.

## Distribution

The source page records the npm package identity and how the plugin is obtained:

- Package: `@openclaw/amazon-bedrock-provider`
- Install route: npm; ClawHub

The package is distributed through the public npm registry and is also discoverable/installable via ClawHub (OpenClaw's plugin marketplace/distribution channel). The page does not state a version, install command, or whether the plugin is bundled "included in OpenClaw" — only the `npm; ClawHub` install route is given.

## Surface

The **Surface** block is the contract surface the plugin registers when loaded. The source page states it verbatim as:

> providers: amazon-bedrock; contracts: memoryEmbeddingProviders

This means the plugin contributes two surface elements to the agent runtime:

- **`providers: amazon-bedrock`** — it registers a model **provider** named `amazon-bedrock`. This is the provider id used to route inference (model selection / model discovery) to Amazon Bedrock. The summary line attributes "model discovery" and "guardrail support" to this provider, but the reference page itself does not list which Bedrock models are discovered or how guardrails are configured — those belong to the fuller provider doc.
- **`contracts: memoryEmbeddingProviders`** — it implements the `memoryEmbeddingProviders` contract, supplying the **embedding** capability the summary cites ("embeddings"). This contract is the integration point through which the OpenClaw memory subsystem obtains vector embeddings from Bedrock embedding models.

The Surface is the authoritative answer to "what does this plugin actually add?": one model provider (`amazon-bedrock`) plus one embedding-contract implementation (`memoryEmbeddingProviders`). The provider name `amazon-bedrock` and the contract id `memoryEmbeddingProviders` are implementation-specific identifiers documented inline here, not separate term entries.

**Source**: OpenClaw documentation — `plugins/reference/amazon-bedrock` (mirror `inbox/openclaw_docs/plugins/reference/amazon-bedrock.md`)
**Last Updated**: 2026-06-22
**Status**: Active
