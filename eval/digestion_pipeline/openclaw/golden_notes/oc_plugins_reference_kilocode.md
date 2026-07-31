---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw kilocode plugin
  - kilocode model provider
  - openclaw kilocode-provider package
  - providers kilocode surface
  - kilocode npm clawhub install
  - openclaw provider plugin
  - kilocode coding model provider
topics:
  - OpenClaw
  - Plugin Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/kilocode
access_control_group: ["general"]
---

# OpenClaw — Kilocode Provider Plugin (`@openclaw/kilocode-provider`)

## Overview

This note is the procedure for identifying, installing, and auditing the OpenClaw **Kilocode plugin**, the catalog reference card from the `plugins/reference/kilocode` source page. The card summarizes the plugin in one line — "Adds Kilocode model provider support to OpenClaw." — and exposes exactly three load-bearing facts across its `## Distribution`, `## Surface`, and `## Related docs` sections: the npm package name `@openclaw/kilocode-provider`, the install route (npm plus a ClawHub identifier), and the single model-provider surface it contributes, `providers: kilocode`. The card is the thin catalog layer above the deeper `/providers/kilocode` provider page (owned by a separate provider sub-plan); this note reproduces the card facts verbatim and links out to that deeper config rather than re-explaining provider auth or model setup.

## Distribution

The Kilocode plugin ships as the npm package **`@openclaw/kilocode-provider`**. Unlike the bundled provider plugins, it is NOT included in OpenClaw by default — its install route is **npm**, and it is also published to ClawHub under the identifier **`clawhub:@openclaw/kilocode-provider`**. To audit whether the plugin is present in an OpenClaw deployment, look for the `@openclaw/kilocode-provider` package among installed plugins (via the npm install path or the equivalent ClawHub install of the same identifier).

## Surface

The plugin contributes a single **model-provider surface**: `providers: kilocode`. Enabling this plugin registers `kilocode` as a selectable model provider in OpenClaw, so models served by Kilocode become routable targets for the agent loop's model-resolution step. The card declares only this one surface key (no channel or speech-provider surface). The deeper details of the provider — model catalog entries, authentication, and routing configuration — live on the linked `/providers/kilocode` page, not on this reference card.

**Source**: OpenClaw documentation — `plugins/reference/kilocode` (mirror `inbox/openclaw_docs/plugins/reference/kilocode.md`)
**Last Updated**: 2026-06-22
**Status**: Active
