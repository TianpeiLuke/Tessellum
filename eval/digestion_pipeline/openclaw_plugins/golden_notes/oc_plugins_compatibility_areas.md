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

## Related Notes

**Terms**

- **[Plugin Manifest](../../term_dictionary/term_plugin_manifest.md)** — manifest/SDK aliases; relevance: compatibility areas include legacy SDK imports/aliases plugins migrate from.
- **[Deprecation](../../term_dictionary/term_deprecation.md)** — deprecation window; relevance: each flat-alias/admission-field set has a dated removal window (2026-08-30).
- **[WebSocket](../../term_dictionary/term_websocket.md)** — inbound transport; relevance: WhatsApp inbound runtime callbacks (`WebInboundMessage`) carry the flat-alias fields.
- **[JSON-RPC](../../term_dictionary/term_json_rpc.md)** — structured RPC payloads; relevance: the nested callback envelope (`event`/`payload`/`platform`) is the structured contract shape.
- **[Provider Plugin](../../term_dictionary/term_provider_plugin.md)** — provider/channel plugin; relevance: areas cover legacy provider/channel hooks and env-var manifest metadata.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: subject — the concrete per-area compatibility shims OpenClaw tracks.
- **[Plugin SDK](../../term_dictionary/term_plugin_sdk.md)** — plugin SDK; relevance: areas include `openclaw/plugin-sdk/*` subpath/alias migrations.
- **[Authentication](../../term_dictionary/term_authentication.md)** — admission/access-control; relevance: WhatsApp inbound `admission` envelope wraps the access-control decision (`ingress.decision`).

**Docs**

- **[cc_plugin_components](../claude_code/cc_plugin_components.md)** — plugin components; relevance: analog for compatibility-field/component migration.
- **[cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md)** — manifest schema; relevance: analog for legacy-vs-nested schema field migration.
- **[cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md)** — channel permission relay; relevance: analog for channel admission/access-control field handling.
- **[cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md)** — channel reply tool; relevance: analog for the flat `reply(...)`/`sendMedia(...)` → `platform` context migration.
- **[hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md)** — platform/channel adapter plugin; relevance: sibling channel-adapter inbound-message contract.
- **[oc_plugins_compatibility](oc_plugins_compatibility.md)** — the registry/policy parent this details the areas of.
- **[oc_plugins_community](oc_plugins_community.md)** — published plugins must honor these schema-level shims.
- **[oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md)** — native-plugin config under the same compatibility regime.
- **[oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md)** — `agentRuntime` legacy-config migration is one tracked area.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** — runtime-alias compatibility (`api.runtime.*`) areas.

**Repos**

- **[repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md)** — channel runtime; relevance: WhatsApp inbound `WebInboundMessage`/`admission` callback contract lives here.
- **[repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md)** — plugin/extension framework; relevance: the legacy SDK aliases/import-boundary areas.

**Snippets**

- **[snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md)** — channel adapter contract; relevance: the inbound-message contract whose flat aliases are being migrated.
- **[snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md)** — conversation resolution; relevance: `conversationId`/`chatId` → `admission.conversation.*` migration.
- **[snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md)** — binding/routing; relevance: callback routing across the nested vs flat envelope.
- **[snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md)** — DM allowlist/admission; relevance: `accessControlPassed`/`admission.ingress.decision` access-control field.
- **[snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md)** — match resolver; relevance: resolving sender/group fields moving under `platform`/`group`.
- **[snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md)** — registry normalize; relevance: normalizing legacy vs registry-first channel config metadata (a tracked area).
- **[snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md)** — kernel dispatch; relevance: dispatch over the inbound callback envelope.
- **[snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md)** — thread bindings; relevance: conversation/group context fields in callbacks.
- **[snippet_openclaw_context_engine_registry_compat](../../code_snippets/snippet_openclaw_context_engine_registry_compat.md)** — registry compat shim; relevance: the named-compatibility-adapter pattern these areas use.
- **[snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md)** — SDK entries; relevance: legacy `openclaw/plugin-sdk/*` alias subpaths being migrated.

## References

- [OpenClaw Docs — Plugin compatibility](https://docs.openclaw.ai/plugins/compatibility)
- [OpenClaw Docs — Plugins reference](https://docs.openclaw.ai/plugins/reference)
- [OpenClaw Docs — Community plugins](https://docs.openclaw.ai/plugins/community)
- [OpenClaw Docs — Plugin SDK migration](https://docs.openclaw.ai/plugins/sdk-migration)

**Source**: OpenClaw documentation — `plugins/compatibility` (mirror `inbox/openclaw_docs/plugins/compatibility.md`), "Current compatibility areas" + "WhatsApp Inbound Callback Flat Aliases" + "WhatsApp Inbound Admission Fields" sections
**Last Updated**: 2026-06-22
**Status**: Active
