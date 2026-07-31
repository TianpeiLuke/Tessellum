---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - compatibility
keywords:
  - openclaw compatibility areas
  - whatsapp inbound callback flat aliases
  - whatsapp inbound admission fields
  - WebInboundMessage WebInboundCallbackMessage
  - admission envelope ingress decision
  - legacy sdk import aliases
  - plugin-sdk compat subpaths
  - 2026-08-30 removal window
topics:
  - OpenClaw
  - Plugin Compatibility Areas
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/compatibility
access_control_group: ["general"]
---

# OpenClaw — Current Plugin Compatibility Areas (SDK Aliases & WhatsApp Inbound Shims)

## Overview

This note models the **concrete per-area compatibility shims** OpenClaw tracks today: the schema-level legacy surfaces that plugins must honor (or migrate off) while named compatibility adapters keep them wired. It covers the enumerated list of current compatibility records from the `plugins/compatibility` source page's "Current compatibility areas" section, then the two detailed WhatsApp inbound shims that page documents in depth — the **WhatsApp Inbound Callback Flat Aliases** (`WebInboundMessage` flat fields vs the nested `WebInboundCallbackMessage` contexts) and the **WhatsApp Inbound Admission Fields** (top-level admission fields vs the `admission` envelope). The governing registry, plugin-inspector package, maintainer acceptance lane, deprecation policy, and release-notes process are documented in the sibling note [oc_plugins_compatibility](oc_plugins_compatibility.md); this note is the data-model companion that enumerates *what* each tracked area actually changes at the field/schema level.

## Current Compatibility Areas

OpenClaw keeps older plugin contracts wired through named compatibility adapters before removing them, protecting existing bundled and external plugins while the SDK, manifest, setup, config, and agent runtime contracts evolve. The source page enumerates the current compatibility records. New plugin code should prefer the replacement listed in the registry and in the specific migration guide; existing plugins can keep using a compatibility path until the docs, diagnostics, and release notes announce a removal window. The tracked areas are:

- **legacy broad SDK imports** such as `openclaw/plugin-sdk/compat`.
- **legacy hook-only plugin shapes** and `before_agent_start`.
- **legacy `api.on("deactivate", ...)` cleanup hook names** while plugins migrate to `gateway_stop`.
- **legacy `activate(api)` plugin entrypoints** while plugins migrate to `register(api)`.
- **legacy SDK aliases** such as `openclaw/extension-api`, `openclaw/plugin-sdk/channel-runtime`, `openclaw/plugin-sdk/command-auth` status builders, `openclaw/plugin-sdk/test-utils` (replaced by focused `openclaw/plugin-sdk/*` test subpaths), and the `ClawdbotConfig` / `OpenClawSchemaType` type aliases.
- **bundled plugin allowlist and enablement behavior.**
- **legacy provider/channel env-var manifest metadata.**
- **legacy provider plugin hooks and type aliases** while providers move to explicit catalog, auth, thinking, replay, and transport hooks.
- **legacy runtime aliases** such as `api.runtime.taskFlow`, `api.runtime.subagent.getSession`, `api.runtime.stt`, and deprecated `api.runtime.config.loadConfig()` / `api.runtime.config.writeConfigFile(...)`.
- **WhatsApp `WebInboundMessage` flat callback fields** such as `body`, `chatId`, `reply(...)`, and `mediaPath` while callback consumers migrate to the nested `WebInboundCallbackMessage` `event`, `payload`, `quote`, `group`, and `platform` contexts (detailed below).
- **WhatsApp `WebInboundMessage` top-level admission fields** such as `from`, `conversationId`, `accountId`, `accessControlPassed`, and `chatType` while callback consumers migrate to the `admission` envelope (detailed below).
- **legacy memory-plugin split registration** while memory plugins move to `registerMemoryCapability`.
- **legacy memory-specific embedding provider registration** while embedding providers move to `api.registerEmbeddingProvider(...)` and `contracts.embeddingProviders`.
- **legacy channel SDK helpers** for native message schemas, mention gating, inbound envelope formatting, and approval capability nesting.
- **legacy channel route key and comparable-target helper aliases** while plugins move to `openclaw/plugin-sdk/channel-route`.
- **activation hints** that are being replaced by manifest contribution ownership.
- **`setup-api` runtime fallback** while setup descriptors move to cold `setup.requiresRuntime: false` metadata.
- **provider `discovery` hooks** while provider catalog hooks move to `catalog.run(...)`.
- **channel `showConfigured` / `showInSetup` metadata** while channel packages move to `openclaw.channel.exposure`.
- **legacy runtime-policy config keys** while doctor migrates operators to `agentRuntime`.
- **generated bundled channel config metadata fallback** while registry-first `channelConfigs` metadata lands.
- **persisted plugin registry disable and install-migration env flags** while repair flows migrate operators to `openclaw plugins registry --refresh` and `openclaw doctor --fix`.
- **legacy plugin-owned web search, web fetch, and x_search config paths** while doctor migrates them to `plugins.entries.<plugin>.config`.
- **legacy `plugins.installs` authored config and bundled plugin load-path aliases** while install metadata moves into the state-managed plugin ledger.

## WhatsApp Inbound Callback Flat Aliases

WhatsApp runtime callbacks deliver `WebInboundMessage`: the canonical nested `event`, `payload`, `quote`, `group`, and `platform` contexts plus deprecated flat aliases for the shipped callback fields. New callback code should read the nested contexts. Code that constructs clean nested callback messages can use `WebInboundCallbackMessage`; compatibility listeners that still inject old flat test or plugin messages should use `LegacyFlatWebInboundMessage` or `WebInboundMessageInput`.

The flat aliases remain available until **2026-08-30**. That removal window applies only to flat alias access; the nested callback shape is the canonical runtime contract. The TypeScript `@deprecated` annotations on each flat alias name its exact nested replacement.

Common examples of the flat-alias → nested-context migration:

- `id`, `timestamp`, and `isBatched` move under `event`.
- `body`, `mediaPath`, `mediaType`, `mediaFileName`, `mediaUrl`, `location`, and `untrustedStructuredContext` move under `payload`.
- `to`, `chatId`, sender/self fields, `sendComposing`, `reply(...)`, and `sendMedia(...)` move under `platform`.
- `replyTo*` fields move under `quote`, and group subject/participant/mention fields move under `group`.

`payload.untrustedStructuredContext` is extracted from inbound provider payloads. Plugins should inspect the `label`, `source`, and `type` before treating its `payload` as authoritative.

## WhatsApp Inbound Admission Fields

Accepted WhatsApp callback messages now carry `admission`, a public-safe envelope for the access-control decision that admitted the message. New callback code should read admission facts from `msg.admission` instead of the older top-level admission fields.

The top-level fields remain available until **2026-08-30**. The TypeScript `@deprecated` annotations name each replacement:

- `from` and `conversationId` move to `admission.conversation.id`.
- `accountId` moves to `admission.accountId`.
- `accessControlPassed` is a derived compatibility view of `admission.ingress.decision === "allow"`; on messages that already carry `admission`, writing the legacy boolean does not rewrite the ingress graph.
- `chatType` moves to `admission.conversation.kind`.

**Source**: OpenClaw documentation — `plugins/compatibility` (mirror `inbox/openclaw_docs/plugins/compatibility.md`), "Current compatibility areas" + "WhatsApp Inbound Callback Flat Aliases" + "WhatsApp Inbound Admission Fields" sections
**Last Updated**: 2026-06-22
**Status**: Active
