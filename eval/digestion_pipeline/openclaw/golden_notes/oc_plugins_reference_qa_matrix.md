---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw qa-matrix plugin
  - matrix qa transport runner
  - qa substrate plugin
  - source checkout only install
  - plugin surface
  - "@openclaw/qa-matrix"
  - plugins reference registry card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/qa-matrix
access_control_group: ["general"]
---

# OpenClaw — QA Matrix Plugin (`@openclaw/qa-matrix`)

## Overview

This note models the `@openclaw/qa-matrix` plugin as a static registry entity, mirroring the `plugins/reference/qa-matrix` source card. That card is a one-screen registry entry describing the plugin in one summary line — "Matrix QA transport runner and substrate" — plus two fields: a `## Distribution` block (the npm package id and how it is installed) and a `## Surface` block (the contract the plugin contributes to the OpenClaw gateway). It is the machine-generated "what package / where from / what it exposes" descriptor, NOT the deep config or setup documentation; the substantive QA-matrix concept and the Matrix channel setup live in other OpenClaw docs cross-linked below.

The three load-bearing facts from the source are: the package is `@openclaw/qa-matrix`; its install route is **source checkout only** (the lone field value that contrasts with the npm/ClawHub route of the other reference cards in this slice); and the surface it registers is the bare `plugin` (no `providers:`, `channels:`, or `contracts:` value — distinguishing it from the provider/channel cards). The plugin's purpose, per the summary line, is to be a Matrix **QA transport runner** and the **substrate** a QA run executes over.

## Distribution

The `## Distribution` block of the source card declares two fields verbatim:

- **Package**: `@openclaw/qa-matrix`
- **Install route**: source checkout only

The install route is the distinguishing attribute of this card. "Source checkout only" means the plugin is not published to npm or distributed through ClawHub the way the sibling reference cards in this slice are (for example `@openclaw/qianfan-provider` and `@openclaw/qqbot` declare npm + ClawHub routes); it is obtained by checking out its source. *(The source card states only "source checkout only"; it does not specify a repository URL, checkout command, or build step — "Not specified in source".)*

## Surface

The `## Surface` block of the source card contains a single value: `plugin`.

This is the bare `plugin` surface — the plugin registers a generic plugin surface rather than one of the typed contract surfaces the other reference cards in this slice declare (a model `providers:` surface like qianfan/qwen, a `channels:` surface like qqbot, or a `contracts:` media/search surface like runway/searxng/senseaudio). Combined with the summary line, the card frames qa-matrix as a **QA transport runner and substrate** over the Matrix transport: the harness that drives live QA exercises across the Matrix channel rather than a model, channel, or media contract provider. *(The source card gives only the single token `plugin` for the surface; it does not enumerate specific RPC methods, hooks, or registered identifiers — "Not specified in source".)*

**Source**: OpenClaw documentation — `plugins/reference/qa-matrix` (mirror `inbox/openclaw_docs/plugins/reference/qa-matrix.md`)
**Last Updated**: 2026-06-22
**Status**: Active
