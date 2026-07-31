---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - document_extract
keywords:
  - openclaw document extract plugin
  - document-extract-plugin
  - documentExtractors contract
  - extract text from attachments
  - fallback page images
  - included in openclaw plugin
  - clawhub plugin surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/document-extract
access_control_group: ["general"]
---

# OpenClaw — Document Extract Plugin

## Overview

This note is the reference card for the OpenClaw **Document Extract plugin**, mirroring the `plugins/reference/document-extract` source page. The plugin extracts text and fallback page images from local document attachments, so attachment content becomes available to the agent run. The page is a thin per-plugin identity card with three sections — `## Distribution` (the npm package name and install route), `## Surface` (the contract IDs the plugin implements), and `## Related docs` (a pointer to the full feature doc) — and this note reproduces each of those facts faithfully while linking the richer tool/concept docs rather than duplicating them.

## Distribution

The plugin's npm package is `@openclaw/document-extract-plugin`. Its install route is **included in OpenClaw** — it is a bundled plugin shipped with OpenClaw rather than a separately-installed npm/ClawHub package, so no explicit install step is documented on this page.

## Surface

The plugin's declared surface is the `documentExtractors` contract: `contracts: documentExtractors`. By implementing this contract the plugin registers a document-extractor that turns local document attachments into extracted text plus fallback page images for downstream consumption. No other contracts, channels, skills, tools, or configuration keys are listed in the source for this plugin.

**Source**: OpenClaw documentation — `plugins/reference/document-extract` (mirror `inbox/openclaw_docs/plugins/reference/document-extract.md`)
**Last Updated**: 2026-06-22
**Status**: Active
