---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw volcengine plugin
  - "@openclaw/volcengine-provider"
  - volcengine provider surface
  - volcengine-plan provider
  - speechproviders contract
  - bundled openclaw provider plugin
  - volcengine llm provider
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/volcengine
access_control_group: ["general"]
---

# OpenClaw — Volcengine Provider Plugin (`@openclaw/volcengine-provider`)

## Overview

This note captures the **Volcengine plugin** descriptor card from the `plugins/reference/volcengine` source page: a single OpenClaw plugin documented by its npm package, install route, and the contract surface it registers. The plugin "Adds Volcengine, Volcengine Plan model provider support to OpenClaw" — it is a dual-purpose descriptor that registers both LLM model providers (`providers: volcengine, volcengine-plan`) AND a speech contract (`contracts: speechProviders`). This is the plugin-packaging view of the capability; the deeper Volcengine provider configuration is documented separately and linked, not redefined here. It mirrors the page's three source sections: `## Distribution`, `## Surface`, and `## Related docs`.

## Distribution

- **Package:** `@openclaw/volcengine-provider`
- **Install route:** included in OpenClaw

The package is bundled — "included in OpenClaw" — so it ships with the gateway rather than requiring a separate npm + ClawHub install (the route used by add-on plugins such as the Twitch channel or voice-call tool plugin). The source page lists no version, no additional install command, and no configuration keys; those are documented in the deeper Volcengine provider doc this card points to.

## Surface

The plugin registers the following contract surface (verbatim from source):

> `providers: volcengine, volcengine-plan; contracts: speechProviders`

This card registers two model-provider entries — **`volcengine`** and **`volcengine-plan`** — under the `providers:` contract, plus a **`speechProviders`** entry under the `contracts:` surface. The `providers:` entries make the Volcengine models selectable by the OpenClaw model router once registered into the model catalog; the `speechProviders` entry supplies speech (TTS/STT) capability to the speech pipeline. The source states only the surface line above; the concrete model identifiers, credentials, and speech-engine settings are *Not specified in source* and live in the deeper provider doc.

**Source**: OpenClaw documentation — `plugins/reference/volcengine` (mirror `inbox/openclaw_docs/plugins/reference/volcengine.md`)
**Last Updated**: 2026-06-22
**Status**: Active
