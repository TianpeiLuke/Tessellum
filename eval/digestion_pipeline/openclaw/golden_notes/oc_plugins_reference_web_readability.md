---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - web_readability
keywords:
  - openclaw web readability plugin
  - web-readability-plugin
  - webContentExtractors contract
  - readable article extraction
  - local html web fetch responses
  - included in openclaw plugin
  - content extractor plugin surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/web-readability
access_control_group: ["general"]
---

# OpenClaw — Web Readability Plugin

## Overview

This note is the reference card for the OpenClaw **Web Readability plugin**, mirroring the `plugins/reference/web-readability` source page. Per the source `summary`, the plugin extracts readable article content from local HTML web-fetch responses, and the page's `read_when` cue marks it as the doc to consult when installing, configuring, or auditing the web-readability plugin. The page is a thin per-plugin identity card with two sections — `## Distribution` (the npm package name and install route) and `## Surface` (the contract it implements) — and unlike most plugin reference cards it has no `## Related docs` pointer. This note reproduces each of those facts faithfully and links the richer web-fetch tool and content-extraction docs rather than duplicating them.

## Distribution

The plugin's package is `@openclaw/web-readability-plugin`. Its install route is **included in OpenClaw** — it is a bundled plugin shipped with OpenClaw rather than a separately-installed npm or ClawHub package, so no explicit install step is documented on this page.

## Surface

The plugin's declared surface is the `webContentExtractors` contract: the source `## Surface` block reads `contracts: webContentExtractors`. By implementing this contract the plugin registers a web content extractor that turns local HTML web-fetch responses into readable article content for downstream consumption by the agent. No other contracts, channels, skills, tools, providers, or configuration keys are listed in the source for this plugin.

**Source**: OpenClaw documentation — `plugins/reference/web-readability` (mirror `inbox/openclaw_docs/plugins/reference/web-readability.md`)
**Last Updated**: 2026-06-22
**Status**: Active
