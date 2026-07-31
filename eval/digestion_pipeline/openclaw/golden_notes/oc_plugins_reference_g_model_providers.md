---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw github copilot provider plugin
  - openclaw gmi cloud provider plugin
  - openclaw google plugin gemini vertex
  - openclaw groq provider plugin
  - openclaw model provider install route
  - openclaw providers contracts surface
  - clawhub provider plugin
  - openclaw g model provider plugins
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/github-copilot
access_control_group: ["general"]
---

# OpenClaw — `g*` Model / Inference Provider Plugins (GitHub Copilot, GMI, Google, Groq)

## Overview

This note consolidates the four alphabetically-contiguous `g*` model/inference **provider plugins** from the OpenClaw plugin-reference inventory — `github-copilot`, `gmi`, `google`, and `groq` — mirroring the four cards `plugins/reference/github-copilot.md`, `plugins/reference/gmi.md`, `plugins/reference/google.md`, and `plugins/reference/groq.md`. Each card is a thin install-inventory entry stating only three things: the npm package name, the install route (included-in-OpenClaw vs npm/ClawHub), and the capability surface the plugin registers (`providers:` ids plus any extra `contracts:`). The durable content here is the per-plugin **package → install-route → registered-surface → deep-dive-page** mapping; the conceptual depth of each integration lives on its `/providers/<id>` deep-dive page (owned by other sub-plans), linked from References, not duplicated here. This is a `procedure` note: how to install and enable each `g*` provider plugin so it registers its provider/contract surface with the OpenClaw host.

## GitHub Copilot Provider Plugin

Adds GitHub Copilot model provider support to OpenClaw.

- **Package**: `@openclaw/github-copilot-provider`
- **Install route**: included in OpenClaw (no separate install — ships with the host; enable/configure rather than add).
- **Surface**: `providers: github-copilot`; `contracts: memoryEmbeddingProviders`.

Because it is included in OpenClaw, no npm or ClawHub add step is required; the plugin is present and only needs to be enabled and credentialed. Beyond the `github-copilot` provider id, it also registers the `memoryEmbeddingProviders` contract (i.e. it can serve embeddings for memory/retrieval, not only chat completions). The deep-dive for configuration and auth is `/providers/github-copilot`.

## GMI (GMI Cloud) Provider Plugin

OpenClaw GMI Cloud provider plugin.

- **Package**: `@openclaw/gmi-provider`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/gmi-provider`.
- **Surface**: `providers: gmi, gmi-cloud, gmicloud`.

GMI is **not** built in — install it from npm (`@openclaw/gmi-provider`) or via ClawHub (`clawhub:@openclaw/gmi-provider`). A single plugin package registers three provider id aliases — `gmi`, `gmi-cloud`, and `gmicloud` — all resolving to the same GMI Cloud inference backend (a config convenience so different model strings/configs can reference any of the three). It registers no extra `contracts:` beyond the model-provider ids. The deep-dive is `/providers/gmi`.

## Google Provider Plugin (Google / Gemini CLI / Vertex)

Adds Google, Google Gemini CLI, Google Vertex model provider support to OpenClaw.

- **Package**: `@openclaw/google-plugin`
- **Install route**: included in OpenClaw.
- **Surface**: `providers: google, google-gemini-cli, google-vertex`; `contracts: imageGenerationProviders, mediaUnderstandingProviders, memoryEmbeddingProviders, musicGenerationProviders, realtimeVoiceProviders, speechProviders, videoGenerationProviders, webSearchProviders`.

The Google plugin is the broadest of the four: a single included-in-OpenClaw package registers **three provider ids** — `google` (the generative-language/Gemini API path), `google-gemini-cli` (the Gemini CLI auth/path), and `google-vertex` (Google Cloud Vertex AI) — plus **eight** capability contracts spanning embeddings (`memoryEmbeddingProviders`), media understanding (`mediaUnderstandingProviders`), generation across modalities (`imageGenerationProviders`, `videoGenerationProviders`, `musicGenerationProviders`, `speechProviders`), realtime voice (`realtimeVoiceProviders`), and `webSearchProviders`. This makes the Google plugin a multi-contract media provider, not just a chat-completion provider. The deep-dive is `/providers/google`.

## Groq Provider Plugin

Adds Groq model provider support to OpenClaw.

- **Package**: `@openclaw/groq-provider`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/groq-provider`.
- **Surface**: `providers: groq`; `contracts: mediaUnderstandingProviders`.

Like GMI, Groq is not built in — install from npm (`@openclaw/groq-provider`) or via ClawHub (`clawhub:@openclaw/groq-provider`). It registers the single `groq` provider id and additionally the `mediaUnderstandingProviders` contract (so Groq models can be used for media-understanding tasks, not only text inference). The deep-dive is `/providers/groq`.

## Install-Route and Surface Summary

The four cards split two ways on distribution: **`github-copilot` and `google` are included in OpenClaw** (present by default; enable + credential, no add step), while **`gmi` and `groq` are external** and added via `npm` or ClawHub (`clawhub:@openclaw/gmi-provider`, `clawhub:@openclaw/groq-provider`). On surface breadth, `gmi` (3 provider id aliases, no extra contracts) and `groq` (1 provider id + `mediaUnderstandingProviders`) are narrow model-inference providers; `github-copilot` adds embeddings (`memoryEmbeddingProviders`); and `google` is the broad multi-modal provider (3 provider ids + 8 contracts). In every case the operator action is the same procedure shape — install (if external) then enable/configure the plugin — after which the plugin registers its declared `providers:` ids and `contracts:` with the host, and the named deep-dive page (`/providers/<id>`) carries the per-provider auth and model-config detail.

**Source**: OpenClaw documentation — `plugins/reference/{github-copilot,gmi,google,groq}` (mirror `inbox/openclaw_docs/plugins/reference/`)
**Last Updated**: 2026-06-22
**Status**: Active
