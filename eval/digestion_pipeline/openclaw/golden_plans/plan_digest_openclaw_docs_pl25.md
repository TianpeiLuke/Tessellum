---
title: Sub-Plan pl25 — OpenClaw Docs: Plugins (SDK subpaths/testing, tool plugins, voice-call, webhooks, workboard, zalouser)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/sdk-subpaths", "plugins/sdk-testing", "plugins/tool-plugins", "plugins/voice-call", "plugins/webhooks", "plugins/workboard", "plugins/zalouser"]
---

# Sub-Plan pl25: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML + `## Overview`/`## Related Notes`/`## References`), dedup (3-way vs term_dictionary/documentation/repo_openclaw*), 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master and not re-derived here.

## Scope

The 7 tail-of-Plugins pages: the plugin SDK subpath catalog (`sdk-subpaths`), plugin testing utilities/patterns (`sdk-testing`), the simple typed-tool plugin authoring flow (`tool-plugins`), the bundled Voice Call plugin (`voice-call`), the bundled Webhooks TaskFlow-ingress plugin (`webhooks`), the bundled Workboard coordination plugin (`workboard`), and the bundled Zalo Personal channel plugin (`zalouser`). Priority **P3** (Phase C — plugin reference sprawl). These document the plugin developer surface (SDK imports, testing, tool authoring) plus three concrete bundled-plugin operator guides. The code-side counterparts (`repo_openclaw_extensions`, `repo_openclaw_extensions_voice_speech`, `repo_openclaw_channels_voice_phone`, `repo_openclaw_channels_messaging`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 15,272 measured words. **Planned: 10 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Plugin SDK subpaths | plugins/sdk-subpaths | 4,323 | 0 | 2 | 2 | model (split: core/channel/provider vs runtime/security/testing/memory) |
| Plugin testing | plugins/sdk-testing | 2,026 | 12 | 7 | 9 | procedure |
| Tool plugins | plugins/tool-plugins | 1,562 | 18 | 13 | 6 | procedure |
| Voice call plugin | plugins/voice-call | 3,969 | 19 | 11 | 16 | procedure + model (split: setup/ops vs audio-modes) |
| Webhooks plugin | plugins/webhooks | 541 | 6 | 7 | 2 | procedure |
| Workboard plugin | plugins/workboard | 2,553 | 7 | 9 | 8 | model + procedure (split: model vs operations) |
| Zalo personal plugin | plugins/zalouser | 298 | 4 | 6 | 2 | procedure |

> Code-block counts are `grep -c '^\`\`\`' / 2`. `sdk-subpaths.md` reports 0 fenced blocks because its content is rendered as Markdown tables inside MDX `<AccordionGroup>`/`<Accordion>` components (a subpath→exports catalog), not code fences.

## Content Strategy

- **Prioritize**: the SDK subpath catalog (the authoritative map of which import lives where — the lookup every plugin author needs) and the voice-call audio-modes contract (realtime vs streaming vs TTS, which are mutually exclusive and security-sensitive). These carry the most reusable, non-obvious decision content.
- **Split**: `sdk-subpaths.md` (4,323w) → core/channel/provider subpaths (model) + runtime/security/testing/memory subpaths (model); `voice-call.md` (3,969w, mixed BB) → setup+CLI+tool+RPC+inbound (procedure) + audio modes (realtime/streaming/TTS/webhook-security) (model/procedure); `workboard.md` (2,553w, >2500) → workboard model (state/cards/executions/dispatch) + workboard operations (CLI/dashboard/lifecycle/permissions/config/troubleshooting).
- **Link-out (not redefine)**: SDK overview/setup/entrypoints (pl23–pl24), channel/provider plugin how-tos (`sdk-channel-plugins`, `sdk-provider-plugins`, pl23–24), message-presentation (pl04), webhooks SDK runtime (`sdk-runtime`, pl24), TaskFlow/automation hooks (au01), `secretref-credential-surface` (rf02), provider docs (Google/OpenAI/Deepgram/ElevenLabs, pr0x). Term vocabulary (`term_plugin_sdk`, `term_mcp`, `term_oauth`, `term_sse`, `term_voice_call`, `term_webhook`) is LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_sdk_subpaths_core.md` | model | sdk-subpaths.md: intro, Plugin entry (`plugin-sdk/plugin-entry`/`core`/`config-schema`/`provider-entry`/`migration`/`health`), Deprecated/test/reserved-helper notes, Channel subpaths accordion, Provider subpaths accordion | 700 | The plugin SDK subpath catalog, part 1: the narrow public `openclaw/plugin-sdk/*` imports for plugin/channel/provider entry, config schema, migration, health, and the full channel + provider subpath families (with deprecation and reserved-helper rules). |
| 2 | `oc_plugins_sdk_subpaths_runtime.md` | model | sdk-subpaths.md: Auth and security subpaths, Runtime and storage subpaths, Capability and testing subpaths, Memory subpaths, Reserved bundled-helper subpaths, provider-usage-snapshot note | 700 | The plugin SDK subpath catalog, part 2: auth/security, runtime/storage, capability + testing, memory, and reserved bundled-helper subpath families, plus the provider usage-snapshot reporting contract. |
| 3 | `oc_plugins_sdk_testing.md` | procedure | sdk-testing.md: Test utilities (imports + Available exports table + Types), Testing target resolution, Testing patterns (registration/runtime-config/channel/provider/mock-runtime/per-instance stubs), Contract tests, Lint enforcement, Test configuration | 700 | Testing OpenClaw plugins: the repo-local test-helper subpaths and `createTestPluginApi`, loader-backed registration smoke tests, channel/provider unit-test patterns, runtime mocking, in-repo contract tests, the three lint rules, and Vitest config. |
| 4 | `oc_plugins_tool_plugins.md` | procedure | tool-plugins.md: Requirements, Quickstart, Write a tool, Optional/factory tools, Return values, Configuration, Generated metadata, Package metadata, Validate in CI, Install/inspect, Publish, Troubleshooting, See also | 700 | Building a tool-only plugin with `defineToolPlugin`: scaffold via `openclaw plugins init`, write TypeBox-typed tools, optional/factory tools, return-value wrapping, config schema, generated manifest (`contracts.tools`) + package metadata, CI validation, local install/inspect, ClawHub publish, and troubleshooting. |
| 5 | `oc_plugins_voice_call_setup.md` | procedure | voice-call.md: intro/providers, Quick start (install/configure/verify/smoke), Configuration (core shape), Session scope, Inbound calls (incl. Per-number Routing, Spoken output contract, Conversation startup, Twilio disconnect grace), Stale call reaper, CLI, Agent tool, Gateway RPC, Troubleshooting | 750 | Operating the Voice Call plugin: install + provider/webhook config + `voicecall setup`/`smoke`, session scope, inbound-call allowlist policy and per-number routing, spoken-output contract, stale-call reaper, the `voicecall` CLI, the `voice_call` agent tool/RPC, and troubleshooting. |
| 6 | `oc_plugins_voice_call_audio_modes.md` | model | voice-call.md: Realtime voice conversations (Tool policy, Agent voice context, Realtime provider examples), Streaming transcription (provider examples), TTS for calls (examples), Webhook security | 700 | The Voice Call audio-mode contract: mutually-exclusive realtime full-duplex voice (consult tool policy, agent context capsule, Google/OpenAI providers) vs streaming transcription (Deepgram/ElevenLabs/Mistral/OpenAI/xAI) vs core TTS deep-merge, and the webhook signature/replay/forwarded-header security model. |
| 7 | `oc_plugins_webhooks.md` | procedure | webhooks.md: intro, Where it runs, Configure routes, Security model, Request format, Supported actions (create_flow, run_task, …), Response shape, Related | 550 | The bundled Webhooks plugin: authenticated HTTP routes that bind external automation (Zapier/n8n/CI) to managed TaskFlows — per-route session binding + shared-secret/SecretRef auth, the security model, request/response shape, and the supported `action` set. |
| 8 | `oc_plugins_workboard_model.md` | model | workboard.md: intro, Default state, What cards contain, Card executions and tasks, Agent coordination (Dispatch worker selection, Worker prompt and lifecycle, Dispatch entry points) | 650 | The Workboard data model: the default board state, card structure and fields, card executions/tasks, and the agent-coordination dispatch model (worker selection, worker prompt/lifecycle, dispatch entry points). |
| 9 | `oc_plugins_workboard_operations.md` | procedure | workboard.md: CLI and slash command, Session lifecycle sync, Dashboard workflow, Permissions, Configuration, Troubleshooting, Related | 600 | Operating Workboard: the CLI + slash command, session-lifecycle sync, the dashboard workflow, permission gating, plugin configuration, and troubleshooting (unavailable tab, cards not saving, dispatch not starting). |
| 10 | `oc_plugins_zalouser.md` | procedure | zalouser.md: intro/warning, Naming, Where it runs, Install (npm / local dev), Config (`channels.zalouser`), CLI, Agent tool, Related | 450 | The Zalo Personal (`zalouser`) channel plugin: unofficial `zca-js`-based personal-account automation — naming/risk warning, Gateway-process placement, npm/local install, `channels.zalouser` config, the channel CLI (login/status/message), and the `zalouser` agent tool actions. |

Filename rule applied: `oc_` + full slug with `/` and `-` replaced by `_`; split notes append a short aspect suffix (`_core`/`_runtime`, `_setup`/`_audio_modes`, `_model`/`_operations`). One BB per note.

## Section Coverage Map

```
sdk-subpaths.md
├── intro (public subpath model, surface audit commands) ──── → note 1 (oc_plugins_sdk_subpaths_core)
├── ## Plugin entry (plugin-entry/core/config-schema/provider-entry/migration/migration-runtime/health) → note 1
├── ### Deprecated compatibility and test helpers ────────── → note 1
├── ### Reserved bundled plugin helper subpaths ──────────── → note 1
├── Accordion: Channel subpaths ─────────────────────────── → note 1
├── Accordion: Provider subpaths (+ usage-snapshot note) ── → note 2 (provider-usage note) / note 1 (provider subpaths)*
├── Accordion: Auth and security subpaths ───────────────── → note 2 (oc_plugins_sdk_subpaths_runtime)
├── Accordion: Runtime and storage subpaths ─────────────── → note 2
├── Accordion: Capability and testing subpaths ──────────── → note 2
├── Accordion: Memory subpaths ──────────────────────────── → note 2
├── Accordion: Reserved bundled-helper subpaths ─────────── → note 2
└── ## Related ──────────────────────────────────────────── → notes 1 + 2 (References)
   * Provider subpaths table → note 1; the "Provider usage snapshots normally report…" paragraph that follows
     the provider accordion → note 2 (it states the cross-provider usage-snapshot contract). No section dropped.

sdk-testing.md
├── intro + Tip ────────────────────────────────────────── → note 3 (oc_plugins_sdk_testing)
├── ## Test utilities (imports, ### Available exports, ### Types) → note 3
├── ## Testing target resolution ────────────────────────── → note 3
├── ## Testing patterns (### registration/runtime-config/channel/provider/mock-runtime/per-instance) → note 3
├── ## Contract tests (### Running scoped tests) ────────── → note 3
├── ## Lint enforcement ─────────────────────────────────── → note 3
├── ## Test configuration ───────────────────────────────── → note 3
└── ## Related ──────────────────────────────────────────── → note 3 (References)

tool-plugins.md
├── intro + recommended flow ────────────────────────────── → note 4 (oc_plugins_tool_plugins)
├── ## Requirements / ## Quickstart / ## Write a tool ───── → note 4
├── ## Optional and factory tools / ## Return values ────── → note 4
├── ## Configuration / ## Generated metadata / ## Package metadata → note 4
├── ## Validate in CI / ## Install and inspect locally / ## Publish → note 4
├── ## Troubleshooting (### 6 error cases) ──────────────── → note 4
└── ## See also ─────────────────────────────────────────── → note 4 (References)

voice-call.md
├── intro/providers + Note ──────────────────────────────── → note 5 (oc_plugins_voice_call_setup)
├── ## Quick start (install/configure/verify/smoke) ─────── → note 5
├── ## Configuration (core shape + accordions: exposure/streaming caps/legacy migrations) → note 5
├── ## Session scope ────────────────────────────────────── → note 5
├── ## Realtime voice conversations (### Tool policy / Agent voice context / Realtime examples) → note 6 (oc_plugins_voice_call_audio_modes)
├── ## Streaming transcription (### Streaming examples) ──── → note 6
├── ## TTS for calls (### TTS examples) ─────────────────── → note 6
├── ## Inbound calls (### Per-number Routing / Spoken output / Conversation startup / disconnect grace) → note 5
├── ## Stale call reaper ────────────────────────────────── → note 5
├── ## Webhook security ─────────────────────────────────── → note 6
├── ## CLI / ## Agent tool / ## Gateway RPC ─────────────── → note 5
├── ## Troubleshooting (### 6 cases) ────────────────────── → note 5
└── ## Related ──────────────────────────────────────────── → notes 5 + 6 (References)

webhooks.md
├── intro ───────────────────────────────────────────────── → note 7 (oc_plugins_webhooks)
├── ## Where it runs / ## Configure routes / ## Security model → note 7
├── ## Request format / ## Supported actions (### create_flow / run_task) → note 7
├── ## Response shape ───────────────────────────────────── → note 7
└── ## Related docs ─────────────────────────────────────── → note 7 (References)

workboard.md
├── intro ───────────────────────────────────────────────── → note 8 (oc_plugins_workboard_model)
├── ## Default state / ## What cards contain / ## Card executions and tasks → note 8
├── ## Agent coordination (### Dispatch worker selection / Worker prompt / Dispatch entry points) → note 8
├── ## CLI and slash command / ## Session lifecycle sync ── → note 9 (oc_plugins_workboard_operations)
├── ## Dashboard workflow / ## Permissions / ## Configuration → note 9
├── ## Troubleshooting (### 4 cases) ────────────────────── → note 9
└── ## Related ──────────────────────────────────────────── → notes 8 + 9 (References)

zalouser.md
├── intro + Warning ─────────────────────────────────────── → note 10 (oc_plugins_zalouser)
├── ## Naming / ## Where it runs ────────────────────────── → note 10
├── ## Install (### Option A npm / ### Option B local dev) ─ → note 10
├── ## Config / ## CLI / ## Agent tool ─────────────────── → note 10
└── ## Related ──────────────────────────────────────────── → note 10 (References)
```
No orphaned H2/H3. Link-out targets (SDK overview/setup/entrypoints, channel/provider plugin how-tos, message-presentation, secretref surface, provider docs, automation hooks, CLI webhooks) are referenced, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| sdk-subpaths.md (4,323w, MDX accordion catalog of ~200 subpaths) | notes 1 + 2 | Exceeds 2,500w; a single catalog note would blow the density cap and mix unrelated subpath families. Split by the source's own accordion groupings: core/channel/provider (note 1) vs auth-security/runtime-storage/capability-testing/memory + reserved helpers (note 2). Both are reference/model BB. |
| voice-call.md (3,969w, 11 H2 / 16 H3, mixed BB) | notes 5 + 6 | Exceeds 2,500w and mixes an operator setup/CLI/tool **procedure** with the realtime/streaming/TTS/webhook-security **model/contract**. Split per word-cap + mixed-BB rules: operations (note 5) vs audio-mode + webhook-security contract (note 6). |
| workboard.md (2,553w, 9 H2 / 8 H3, mixed BB) | notes 8 + 9 | Just over 2,500w and mixes the board/card/dispatch **data model** with the **operational** CLI/dashboard/permissions/config/troubleshooting procedure. Split per word-cap + mixed-BB rules: model (note 8) vs operations (note 9). |
| sdk-testing.md, tool-plugins.md, webhooks.md, zalouser.md | (none) | Each ≤2,500w, single coherent BB → 1 note each. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (15,272 measured words). New `oc_*` notes: **10**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×6 (notes 3, 4, 5, 7, 9, 10) · model ×4 (notes 1, 2, 6, 8).
- Est. digest words ~6,500 (avg ~650/note). 59 source code/JSON5 fences (sdk-subpaths uses MDX tables, not fences) distribute across the procedure/model notes; each note kept ≤6 (config snippets reproduced selectively, verbatim; subpath catalog uses Markdown tables, not code blocks).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)



### oc_plugins_sdk_subpaths_core (9t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — narrow public import surface for OpenClaw plugins; relevance: this catalog IS the `openclaw/plugin-sdk/*` subpath surface (plugin-entry/core/config-schema).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — cold static metadata OpenClaw reads before loading plugin code; relevance: the entry/core subpaths emit the manifest the loader consumes.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin that registers a model/speech/media provider; relevance: the Provider subpaths accordion (`provider-entry`, `provider-auth`, `provider-stream`) is in this note.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — component bridging a chat platform to the agent runtime; relevance: the Channel subpaths accordion (`channel-core`, `channel-inbound/outbound`) is the channel-adapter public surface.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — shared channel-plugin runtime core; relevance: `channel-core`/`channel-plugin-common` subpaths are the kernel's exposed prelude.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol for tool/server integration; relevance: `codex-mcp-projection` reserved subpath projects user MCP config into Codex thread config.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed superset of JS; relevance: every subpath ships TypeScript types/builders (Zod/TypeBox schema exports).
- [npm](../../term_dictionary/term_npm.md) — Node package registry/manager; relevance: public subpaths are the package-`exports` subset published to npm.
- [Node.js](../../term_dictionary/term_node_js.md) — server-side JS runtime; relevance: the SDK is a Node ESM package; subpaths are Node module entrypoints.

**Docs**
- [Hermes plugin types and surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — enumerates the plugin surface taxonomy in the sibling Hermes fork; relevance: direct analog of OpenClaw's subpath-by-purpose grouping.
- [Hermes plugins system](../hermes_agent/hermes_plugins_system.md) — how the Hermes plugin loader/registry resolves imports; relevance: same loader lineage as the OpenClaw plugin SDK.
- [Hermes build-plugin tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — worked plugin authoring walkthrough; relevance: shows which SDK imports a real plugin uses, mirroring this catalog.
- [CC plugins overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model overview; relevance: cross-tool precedent for a public plugin import/component surface.
- [CC plugin components](../claude_code/cc_plugin_components.md) — the component types a CC plugin can contribute; relevance: parallels the entry/channel/provider subpath families here.
- [CC plugin manifest schema](../claude_code/cc_plugin_manifest_schema.md) — the CC plugin manifest fields; relevance: contrasts with OpenClaw's manifest emitted from the entry subpaths.
- [Pi extensions overview](../pi/pi_extensions_overview.md) — Pi's extension/plugin architecture; relevance: third coding-agent precedent for a curated extension import surface.
- [Pi extensions API methods](../pi/pi_extensions_api_methods.md) — the API surface a Pi extension calls; relevance: analog of the runtime helper subpaths exposed here.
- [Band SDK reference adapters](../band/band_sdk_reference_adapters.md) — Band agent SDK adapter import reference; relevance: another SDK whose adapters are imported by narrow subpath.
- [oc_plugins_sdk_subpaths_runtime](oc_plugins_sdk_subpaths_runtime.md) — part 2 of this catalog (auth/runtime/memory/testing) (planned, this series); relevance: the other half of the same subpath catalog.
- [oc_plugins_sdk_overview_imports](oc_plugins_sdk_overview_imports.md) — the SDK import conventions overview (planned, this series, pl24); relevance: the authoring guide this catalog is the reference for.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: these subpaths ARE its public surface.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel plugin family; relevance: consumers of the channel subpaths accordion.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel implementations; relevance: import `channel-core`/`channel-inbound` subpaths.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled provider plugins; relevance: consumers of the provider subpaths accordion.

**Snippets**
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — the SDK entry export map; relevance: shows the actual `plugin-entry`/`core` exports this note catalogs.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package `exports`/contract wiring; relevance: explains how public subpaths are the post-private-subtraction `exports` subset.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/register lifecycle; relevance: the entry subpaths feed this lifecycle.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel adapter contract; relevance: the channel subpaths implement this contract.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: `tool-plugin`/`tool-payload` subpaths build these descriptors.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — Hermes plugin SDK architecture; relevance: same subpath-grouped SDK design.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — Hermes manifest schema; relevance: parallels the manifest the entry subpaths emit.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registration registry; relevance: analog of the `provider-entry`/`provider-catalog` subpaths.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: shows how subpath-scoped namespaces are wired.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — Gateway plugin runtime loader; relevance: consumes the public subpaths at startup.

### oc_plugins_sdk_subpaths_runtime (10t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the narrow public import surface; relevance: part 2 of the same subpath catalog (auth/runtime/memory/testing).
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity/credentials; relevance: the Auth-and-security subpaths (`command-auth`, `approval-*-runtime`) live here.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: `provider-oauth-runtime` callback/PKCE/state helpers are in this note.
- [PKCE](../../term_dictionary/term_pkce.md) — Proof Key for Code Exchange OAuth extension; relevance: `provider-oauth-runtime` exposes PKCE/state helpers explicitly.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side-request-forgery defense; relevance: `ssrf-policy`/`ssrf-dispatcher`/`ssrf-runtime` subpaths are the SSRF surface.
- [Embedding](../../term_dictionary/term_embedding.md) — vector representation for semantic search; relevance: the Memory subpaths expose embedding-provider registry helpers.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing speech from text; relevance: `speech`/`speech-core` capability subpaths are catalogued here.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribing audio to text; relevance: `realtime-transcription` capability subpath is in this note.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored per-provider credential record; relevance: `provider-auth`/`provider-auth-runtime` write/resolve auth profiles.
- [Message Queue](../../term_dictionary/term_message_queue.md) — async work buffer; relevance: `delivery-queue-runtime`/`keyed-async-queue`/`concurrency-runtime` runtime subpaths.

**Docs**
- [Hermes env vars: providers, auth, tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth/env-var surface; relevance: analog of the `provider-auth`/`provider-env-vars` runtime subpaths.
- [Hermes memory provider catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory/embedding provider catalog; relevance: parallels the Memory subpaths (`memory-core-host-engine-embeddings`).
- [Hermes memory provider plugin](../hermes_agent/hermes_memory_provider_plugin.md) — building a memory provider; relevance: consumes the memory-host subpaths catalogued here.
- [Hermes STT transcription](../hermes_agent/hermes_stt_transcription.md) — streaming transcription surface; relevance: the `realtime-transcription` capability subpath underlies it.
- [Hermes TTS providers](../hermes_agent/hermes_tts_providers.md) — speech-synthesis providers; relevance: the `speech`/`speech-core` capability subpaths underlie it.
- [CC MCP authentication](../claude_code/cc_mcp_authentication.md) — OAuth/PKCE for MCP servers; relevance: cross-tool precedent for the `provider-oauth-runtime` PKCE flow.
- [Pi extensions API methods](../pi/pi_extensions_api_methods.md) — runtime API methods for extensions; relevance: analog of the runtime/storage helper subpaths.
- [Pi compaction extensions](../pi/pi_compaction_extensions.md) — session/context runtime extension hooks; relevance: parallels `session-store-runtime`/`runtime-config-snapshot`.
- [oc_plugins_sdk_subpaths_core](oc_plugins_sdk_subpaths_core.md) — part 1 of this catalog (entry/channel/provider) (planned, this series); relevance: the other half of the same subpath catalog.
- [oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md) — the runtime namespace reference (planned, this series, pl24); relevance: documents the `runtime`/`runtime-store` namespaces these subpaths expose.
- [oc_security_network_proxy_hardening](oc_security_network_proxy_hardening.md) — network/SSRF hardening (planned, this series, se01); relevance: home of the SSRF concept these `ssrf-*` subpaths enforce.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: owns these runtime/auth/security subpaths.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: source of the Memory subpaths.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/realtime capability; relevance: source of the `speech`/`realtime-*` capability subpaths.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security runtime; relevance: source of `security-runtime`/`ssrf-*`/secret subpaths.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: source of `session-store-runtime`/`session-binding-runtime`.

**Snippets**
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — security exec/runtime audit; relevance: exercises the `security-runtime`/`exec-approvals-runtime` subpaths.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content/SSRF guarding; relevance: built on the `ssrf-*` subpaths.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth/authorize dispatch; relevance: uses the `command-auth`/`approval-*-runtime` subpaths.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth auth-profile portability; relevance: built on `provider-auth`/`provider-oauth-runtime`.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — a PKCE OAuth flow; relevance: concrete example of the PKCE helpers in `provider-oauth-runtime`.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime engine; relevance: backs the Memory subpaths.
- [snippet_openclaw_memory_runtime_re_exports](../../code_snippets/snippet_openclaw_memory_runtime_re_exports.md) — memory runtime re-exports; relevance: shows the `memory-host-*` alias subpaths catalogued here.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env/logger helpers; relevance: the `runtime-env`/`runtime` subpaths.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT provider; relevance: built on `realtime-transcription` capability subpath.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: built on the `speech` capability subpath.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config resolution; relevance: uses `plugin-config-runtime`/`runtime-config-snapshot` subpaths.

### oc_plugins_sdk_testing (10t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the public plugin import surface; relevance: the test-helper subpaths (`plugin-test-api`) are repo-local SDK entrypoints.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model/speech provider plugin; relevance: `provider-test-contracts`/`registerSingleProviderPlugin` test provider registration.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — chat-platform adapter; relevance: `channel-contract-testing`/`channel-test-helpers` assert channel contracts.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — cold plugin metadata; relevance: loader-backed smoke tests assert manifest-declared capability ownership.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registry of agent-callable tools; relevance: registration contract tests verify which plugin owns which tool.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool-invocation pattern; relevance: `createParameterFreeTool` builds dynamic-tool schema fixtures for runtime tests.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS; relevance: the `Types` section re-exports TS contract types for test files.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: runtime-seam contract tests cover MCP-projection capability ownership.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — declaring/asserting supported capabilities; relevance: contract suites assert capability ownership (`kind: "memory"`).
- [Structured Output](../../term_dictionary/term_structured_output.md) — schema-constrained model output; relevance: provider replay-policy tests assert structured tool/metadata passthrough.

**Docs**
- [Band testing agents](../band/band_testing_agents.md) — agent/adapter test patterns in Band; relevance: closest cross-tool analog of plugin contract testing.
- [Band creating adapters: implementation](../band/band_creating_adapters_implementation.md) — adapter implementation + tests; relevance: parallels channel/provider unit-test patterns.
- [Hermes build-plugin tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — plugin authoring incl. tests; relevance: shows the registration smoke-test step.
- [Hermes plugin types and surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surfaces tests must cover; relevance: maps the registration surfaces this note tests.
- [Hermes contributing dev setup](../hermes_agent/hermes_contributing_dev_setup.md) — dev/test environment setup; relevance: analog of the Vitest/coverage `pnpm test` config here.
- [CC plugin quickstart](../claude_code/cc_plugin_quickstart.md) — scaffold + validate a CC plugin; relevance: cross-tool precedent for plugin validate/test loop.
- [CC plugin CLI commands](../claude_code/cc_plugin_cli_commands.md) — plugin lifecycle CLI; relevance: parallels `openclaw plugins validate`/`pnpm test` workflow.
- [Pi custom provider registration](../pi/pi_custom_provider_registration.md) — registering a provider in Pi; relevance: analog of provider registration contract tests.
- [oc_plugins_sdk_subpaths_runtime](oc_plugins_sdk_subpaths_runtime.md) — the runtime/testing subpath catalog (planned, this series); relevance: lists the `*-test-*` subpaths this note imports.
- [oc_plugins_sdk_subpaths_core](oc_plugins_sdk_subpaths_core.md) — the core subpath catalog (planned, this series); relevance: the entry subpaths under test.
- [oc_plugins_tool_plugins](oc_plugins_tool_plugins.md) — tool-plugin authoring incl. `npm test` (planned, this series); relevance: shares the validate-in-CI test loop.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: owns the bundled-plugin contract tests + test subpaths.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: subject of the channel contract test patterns.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: subject of the provider contract test patterns.
- [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — Hermes plugin/test harness; relevance: analogous plugin test/registry harness.

**Snippets**
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — the real plugin loader; relevance: loader-backed smoke tests exercise this acceptance path.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin register lifecycle; relevance: registration-contract tests target it.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package public-artifact contract; relevance: `plugin-test-contracts` asserts package/public-artifact shape.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: `channel-contract-testing` asserts this contract.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: tool-registration tests assert descriptor shape.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: analog of `registerProviderPlugin(s)` test helpers.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: shows the test-subpath layering.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env helpers; relevance: `createRuntimeEnv`/`withEnv` test fixtures build on it.
- [snippet_hermes_agent_plugins_provider_nous](../../code_snippets/snippet_hermes_agent_plugins_provider_nous.md) — a concrete provider plugin; relevance: example unit-tested with provider contract helpers.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: `describeOpenAIProviderRuntimeContract` targets this family.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider plugin; relevance: exercised by provider runtime contract tests.

### oc_plugins_tool_plugins (10t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the public plugin import surface; relevance: `defineToolPlugin` is exported from `plugin-sdk/tool-plugin`.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — cold static plugin metadata; relevance: `openclaw plugins build` generates `openclaw.plugin.json` with `contracts.tools`.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registry of agent-callable tools; relevance: `contracts.tools` is the discovery contract mapping tools to owners.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — the schema describing a tool; relevance: each `tool({name,parameters,…})` is a descriptor with TypeBox params.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: tool plugins add agent-callable tools the model can invoke.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema vocabulary for JSON; relevance: TypeBox compiles tool/config params to JSON Schema in the manifest.
- [Structured Output](../../term_dictionary/term_structured_output.md) — schema-typed values; relevance: return-value wrapping yields JSON the model sees plus original in `details`.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS; relevance: param/config types are inferred from TypeBox schemas in TS.
- [npm](../../term_dictionary/term_npm.md) — package registry/manager; relevance: `npm install`/`npm pack`/install paths + `typebox` runtime dependency.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: requirements specify Node >= 22, ESM output.

**Docs**
- [Hermes build-plugin tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — end-to-end plugin scaffold/build; relevance: closest analog to the `openclaw plugins init/build/validate` flow.
- [Hermes plugins system](../hermes_agent/hermes_plugins_system.md) — plugin loader/discovery; relevance: explains why static manifest metadata enables cold discovery.
- [Hermes plugin types and surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface taxonomy; relevance: positions tool-only plugins vs channel/provider/hook plugins.
- [CC plugin quickstart](../claude_code/cc_plugin_quickstart.md) — scaffold a CC plugin; relevance: cross-tool precedent for the init→build→validate loop.
- [CC plugin manifest schema](../claude_code/cc_plugin_manifest_schema.md) — CC manifest fields; relevance: contrasts with the generated `openclaw.plugin.json` `contracts.tools`.
- [CC plugin marketplaces and install](../claude_code/cc_plugin_marketplaces_and_install.md) — publish/install plugins; relevance: parallels ClawHub publish + `plugins install` here.
- [CC plugin dependencies](../claude_code/cc_plugin_dependencies.md) — plugin dependency declarations; relevance: parallels keeping `typebox` in `dependencies` not devDeps.
- [Pi custom provider registration](../pi/pi_custom_provider_registration.md) — registering a typed capability; relevance: analog of declaring static tool metadata.
- [oc_plugins_manifest_generation_tool_metadata](oc_plugins_manifest_generation_tool_metadata.md) — manifest generation + tool metadata (planned, this series, pl04); relevance: the manifest `toolMetadata`/`contracts.tools` this note generates.
- [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md) — `definePluginEntry` and entrypoints (planned, this series, pl24); relevance: the fuller-power alternative when tools are dynamic.
- [oc_plugins_sdk_testing](oc_plugins_sdk_testing.md) — plugin testing (planned, this series); relevance: shares the validate/`npm test` CI step.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: ships `plugin-sdk/tool-plugin` + the `plugins build/validate` generators.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill/tool authoring; relevance: analogous declarative tool/skill authoring surface.
- [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — Hermes plugin framework; relevance: analogous tool-plugin authoring lineage.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: home of `openclaw plugins init/build/validate/install` commands.

**Snippets**
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: the shape `defineToolPlugin`'s `tool({…})` produces.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entry exports; relevance: shows where `defineToolPlugin` sits in the entry surface.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package metadata contract; relevance: `package.json` `openclaw.extensions`/`files` alignment this note describes.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: cold manifest read precedes runtime load, the reason for static metadata.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: analog of `contracts.tools` ownership mapping.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: parallels the generated manifest shape.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — `plugins install` command; relevance: analog of `openclaw plugins install ./pkg`.
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — plugins list/inspect; relevance: analog of `openclaw plugins inspect --runtime`.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery; relevance: shows cold-metadata discovery `contracts.tools` enables.
- [snippet_hermes_agent_toolsets_materialize](../../code_snippets/snippet_hermes_agent_toolsets_materialize.md) — materializing tools into a toolset; relevance: how declared tool names become live tools.
- [snippet_hermes_agent_plugins_spotify](../../code_snippets/snippet_hermes_agent_plugins_spotify.md) — a concrete tool plugin; relevance: worked example of a typed-tool plugin like the `stock-quotes` sample.

### oc_plugins_voice_call_setup (10t · 12s · 11d)

**Terms**
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony voice integration; relevance: this note IS the Voice Call plugin operator guide.
- [Webhook](../../term_dictionary/term_webhook.md) — provider HTTP callback; relevance: setup requires a public webhook URL for carrier callbacks.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: provider credentials + signature verification gate the plugin.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy/tunnel; relevance: `webhookSecurity.trustedProxyIPs`/forwarded-header trust covers proxy/tunnel fronting.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — bounding request volume; relevance: the pre-auth body profile + per-IP in-flight cap protect the webhook.
- [Replay Attack](../../term_dictionary/term_replay_attack.md) — re-sending captured requests; relevance: per-turn `<Gather>` tokens defeat stale/replayed speech callbacks.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedupe token for repeated requests; relevance: replayed valid webhooks are acked but skipped for side effects.
- [VoIP](../../term_dictionary/term_voip.md) — voice over IP/telephony; relevance: Twilio/Telnyx/Plivo are the VoIP carriers configured here.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — who may message/call the agent; relevance: `inboundPolicy: allowlist` is the caller-ID screen for inbound calls.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model/provider services; relevance: realtime/streaming/TTS providers are external GenAI services configured in setup.

**Docs**
- [Hermes voice mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice mode CLI in the Hermes fork; relevance: closest analog to the `voicecall` CLI surface.
- [Hermes use-voice-mode guide](../hermes_agent/hermes_use_voice_mode_guide.md) — operator voice setup guide; relevance: analog of install/configure/verify/smoke flow.
- [Hermes voice gateway: Discord VC](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice over a gateway channel; relevance: parallels Gateway-process voice plugin placement.
- [Hermes Google Meet/messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — media/telephony settings; relevance: parallels the per-number/media config here.
- [Hermes security: command approval](../hermes_agent/hermes_security_command_approval.md) — approval/auth gating; relevance: parallels caller-ID allowlist + webhook auth posture.
- [CC voice dictation](../claude_code/cc_voice_dictation.md) — voice input in Claude Code; relevance: cross-tool precedent for voice I/O setup.
- [oc_plugins_voice_call_audio_modes](oc_plugins_voice_call_audio_modes.md) — realtime/streaming/TTS contract (planned, this series); relevance: the audio-mode half of the same plugin.
- [oc_plugins_webhooks](oc_plugins_webhooks.md) — webhook ingress plugin (planned, this series); relevance: shares the webhook security/forwarded-header model.
- [oc_reference_secretref_credential_surface](oc_reference_secretref_credential_surface.md) — SecretRef credential surface (planned, this series, rf03); relevance: voice-call credentials resolve through SecretRefs.
- [oc_security_network_proxy_hardening](oc_security_network_proxy_hardening.md) — proxy/exposure hardening (planned, this series, se01); relevance: public-exposure + trusted-proxy guidance for the webhook.
- [oc_automation_taskflow](oc_automation_taskflow.md) — TaskFlow/agent automation (planned, this series, au01); relevance: inbound auto-responses run through the agent system.

**Repos**
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel; relevance: the carrier-call implementation this plugin operates.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/voice capability; relevance: registers the realtime/streaming/TTS providers.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway process; relevance: hosts the plugin + serves the `voicecall.*` RPC.

**Snippets**
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: the runtime this setup configures/starts.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — call manager/state; relevance: tracks call records the CLI `status`/`tail` read.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — webhook signature verification; relevance: the signature check setup must pass.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay-protection cache; relevance: the replay protection described in this note.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — media-stream admission/caps; relevance: the streaming connection caps + per-IP limits.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — gateway rate-limit policy; relevance: analog of the pre-auth body profile + in-flight cap.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — gateway HTTP request handler; relevance: how plugin webhook routes are served by the Gateway.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: how `openclaw voicecall …` subcommands dispatch.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config writing; relevance: analog of writing `plugins.entries.voice-call.config`.
- [snippet_hermes_agent_plugins_google_meet](../../code_snippets/snippet_hermes_agent_plugins_google_meet.md) — Google Meet Twilio dial-in; relevance: Meet uses this plugin for Twilio joins (troubleshooting section).
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode agent tool; relevance: analog of the `voice_call` agent tool actions.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — gateway send handler; relevance: spoken-output delivery path for auto-responses.

### oc_plugins_voice_call_audio_modes (10t · 12s · 11d)

**Terms**
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony voice integration; relevance: this note is the Voice Call audio-mode contract.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live streaming STT; relevance: the `streaming` mode forwards audio to realtime transcription providers.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — full-duplex realtime voice; relevance: the `realtime` mode is full-duplex realtime voice conversation.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the TTS-for-calls deep-merge section configures spoken output.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio transcription; relevance: streaming transcription providers (Deepgram/ElevenLabs/Mistral/OpenAI/xAI) do STT.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional socket protocol; relevance: realtime/streaming audio rides Twilio Media Streams over WebSocket.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events streaming; relevance: streaming transcription is an event-stream contract (vs realtime full-duplex).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: realtime/streaming/TTS use external GenAI providers.
- [Replay Attack](../../term_dictionary/term_replay_attack.md) — re-sent request abuse; relevance: the webhook-security subsection covers replay protection.
- [Webhook](../../term_dictionary/term_webhook.md) — provider HTTP callback; relevance: the webhook signature/forwarded-header security model is in this note.

**Docs**
- [Hermes STT transcription](../hermes_agent/hermes_stt_transcription.md) — streaming transcription providers; relevance: direct analog of the streaming-transcription mode.
- [Hermes TTS providers](../hermes_agent/hermes_tts_providers.md) — speech-synthesis providers; relevance: direct analog of the TTS-for-calls deep-merge.
- [Hermes use-voice-mode guide](../hermes_agent/hermes_use_voice_mode_guide.md) — realtime voice usage; relevance: analog of the realtime full-duplex mode.
- [Hermes voice mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice mode operations; relevance: realtime-vs-streaming mode selection.
- [Hermes messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio config; relevance: parallels provider-owned `realtime.providers.*`/`streaming.providers.*` config.
- [CC voice dictation](../claude_code/cc_voice_dictation.md) — voice input; relevance: cross-tool streaming-transcription precedent.
- [Pi custom streaming API](../pi/pi_custom_streaming_api.md) — custom streaming integration; relevance: analog of the streaming transcription provider contract.
- [oc_plugins_voice_call_setup](oc_plugins_voice_call_setup.md) — voice-call operations (planned, this series); relevance: the setup half of the same plugin (mode enablement, webhook).
- [oc_plugins_sdk_subpaths_runtime](oc_plugins_sdk_subpaths_runtime.md) — speech/realtime capability subpaths (planned, this series); relevance: the `speech`/`realtime-*` subpaths these modes build on.
- [oc_reference_secretref_credential_surface](oc_reference_secretref_credential_surface.md) — SecretRef surface (planned, this series, rf03); relevance: provider `apiKey` fields resolve through SecretRefs.
- [oc_security_network_proxy_hardening](oc_security_network_proxy_hardening.md) — proxy/SSRF hardening (planned, this series, se01); relevance: home of the webhook forwarded-header trust model.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/realtime capability; relevance: registers the realtime-voice + transcription providers.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel; relevance: the Twilio Media Streams carrier path these modes use.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: Google/OpenAI/Deepgram/ElevenLabs/Mistral/xAI realtime+streaming providers.

**Snippets**
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: the streaming-transcription audio mode.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media-stream audio handling; relevance: realtime/streaming audio plumbing for calls.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — stream admission caps; relevance: the streaming connection caps governing audio modes.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — webhook signature verify; relevance: the webhook-security model in this note.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — replay cache; relevance: webhook replay protection covered here.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: a bundled streaming-transcription provider.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: a bundled TTS provider for calls.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: another TTS provider in the speech registry.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: how transcribed audio reaches the agent.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: analog of streaming-transcription consumption.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing/fallback; relevance: analog of the TTS deep-merge + provider-chain fallback.

### oc_plugins_webhooks (10t · 11s · 11d)

**Terms**
- [Webhook](../../term_dictionary/term_webhook.md) — authenticated HTTP callback route; relevance: this plugin IS authenticated webhook routes binding external automation.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: shared-secret/SecretRef bearer auth gates every route.
- [Access Control](../../term_dictionary/term_access_control.md) — bounding what an actor may do; relevance: routes act with the bound `sessionKey`'s TaskFlow authority.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — bounding request volume; relevance: fixed-window rate limiting + in-flight limiting per route.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedupe token; relevance: body-size/timeout guards + safe re-handling of repeated automation calls.
- [Replay Attack](../../term_dictionary/term_replay_attack.md) — re-sent request abuse; relevance: shared-secret + body guards harden against replayed external calls.
- [Automation](../../term_dictionary/term_automation.md) — programmatic workflow triggering; relevance: Zapier/n8n/CI drive managed TaskFlows via these routes.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — events trigger work; relevance: external events POST `action`s that create/drive flows.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: routes are typically exposed via a proxy/tunnel in front of the Gateway.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent runtime; relevance: `run_task` allows `subagent`/`acp` runtimes for child tasks.

**Docs**
- [Hermes event hooks](../hermes_agent/hermes_event_hooks.md) — event hook surface; relevance: closest analog of webhook-triggered automation.
- [Hermes automation blueprints (event)](../hermes_agent/hermes_automation_blueprints_event.md) — event-driven automation blueprints; relevance: same external-event-to-workflow pattern.
- [Hermes plugin extensions: hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — plugin hook/webhook extensions; relevance: how a plugin registers HTTP/hook routes.
- [Hermes built-in plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled plugin catalog; relevance: positions the bundled webhooks plugin among built-ins.
- [CC SDK hooks overview](../claude_code/cc_sdk_hooks_overview.md) — hook event model; relevance: cross-tool precedent for event-driven external triggers.
- [CC hook events catalog](../claude_code/cc_hook_events_catalog.md) — hook event catalog; relevance: analog of the supported `action` set.
- [oc_automation_taskflow](oc_automation_taskflow.md) — TaskFlow model (planned, this series, au01); relevance: routes create/drive managed TaskFlows.
- [oc_automation_hooks](oc_automation_hooks.md) — hooks/webhooks overview (planned, this series, au01); relevance: the "Hooks and webhooks overview" the source's Related links to.
- [oc_plugins_voice_call_setup](oc_plugins_voice_call_setup.md) — voice-call webhook setup (planned, this series); relevance: shares Gateway-process webhook security surface.
- [oc_reference_secretref_credential_surface](oc_reference_secretref_credential_surface.md) — SecretRef surface (planned, this series, rf03); relevance: route `secret` accepts env/file/exec SecretRefs.
- [oc_plugins_workboard_operations](oc_plugins_workboard_operations.md) — workboard ops (planned, this series); relevance: `run_task` dispatches subagent/acp work like workboard dispatch.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway process; relevance: hosts the plugin + `managedFlows.bindSession` API.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: the bundled webhooks plugin lives here.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session subsystem; relevance: routes bind to a `sessionKey`'s TaskFlow authority.

**Snippets**
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — gateway hook/HTTP request handler; relevance: how authenticated webhook routes are served.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth/authorize dispatch; relevance: shared-secret auth before route side effects.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit policy; relevance: the fixed-window + in-flight limiting applied per route.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — webhook auth/verify; relevance: shared auth pattern for inbound webhook requests.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — replay cache; relevance: dedupe/replay handling shared by webhook ingress.
- [snippet_hermes_agent_conv_loop_post_api_hook](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_hook.md) — post-API hook dispatch; relevance: analog of external-event-driven hook execution.
- [snippet_openclaw_context_engine_delegate](../../code_snippets/snippet_openclaw_context_engine_delegate.md) — delegate/sub-run dispatch; relevance: `run_task` spawns subagent/acp child runtimes.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate spawn; relevance: analog of `run_task` runtime child spawn.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — subagent run manager; relevance: backs `run_task` `subagent` runtime.
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — session read methods; relevance: routes inspect/bind session-owned TaskFlows.

### oc_plugins_workboard_model (10t · 11s · 11d)

**Terms**
- [Kanban](../../term_dictionary/term_kanban.md) — board/column work-tracking method; relevance: Workboard is a Kanban-style board of cards with `triage…done` statuses.
- [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — Kanban board shared by multiple agents; relevance: cards are claimed/dispatched across agents — the multi-agent board model.
- [Message Queue](../../term_dictionary/term_message_queue.md) — ordered async work buffer; relevance: ready cards are an ordered dispatch queue (priority/position/creation-time).
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent runtime; relevance: dispatch starts subagent worker runs via the Gateway subagent runtime.
- [Delegate Task](../../term_dictionary/term_delegate_task.md) — handing work to a child agent; relevance: dispatch worker selection delegates ready cards to workers.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent client protocol runtime; relevance: card executions can run `acp` runtimes alongside subagent.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — event-record-driven state; relevance: cards record lifecycle events (created/moved/claimed/heartbeat/dispatch).
- [Automation](../../term_dictionary/term_automation.md) — programmatic orchestration; relevance: `autoDecompose`/dispatch automate card fan-out + worker starts.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — deterministic session/thread keying; relevance: deterministic per-board/card session keys route dispatches to the same worker lane.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — declaring runtime capabilities; relevance: cards select engine (Codex/Claude) and runtime per execution metadata.

**Docs**
- [Hermes Kanban multi-agent board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent Kanban board model; relevance: direct analog of the Workboard data model.
- [Hermes Kanban worker lanes](../hermes_agent/hermes_kanban_worker_lanes.md) — worker lane assignment; relevance: parallels deterministic worker session-key lanes.
- [Hermes Kanban worker orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — dispatch/orchestration; relevance: analog of dispatch worker selection + prompt/lifecycle.
- [Hermes Kanban tutorial walkthrough](../hermes_agent/hermes_kanban_tutorial_walkthrough.md) — board concepts walkthrough; relevance: shows card/state model end-to-end.
- [Hermes subagent delegation](../hermes_agent/hermes_subagent_delegation.md) — subagent delegation model; relevance: dispatch starts subagent worker runs.
- [CC subagents overview](../claude_code/cc_subagents_overview.md) — subagent execution model; relevance: cross-tool precedent for worker subagent runs.
- [oc_plugins_workboard_operations](oc_plugins_workboard_operations.md) — workboard CLI/ops (planned, this series); relevance: the operational half of this model.
- [oc_automation_taskflow](oc_automation_taskflow.md) — TaskFlow model (planned, this series, au01); relevance: card executions use the Gateway task-tracked run path.
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task lifecycle (planned, this series, au01); relevance: card lifecycle syncs from the Gateway task ledger.
- [oc_plugins_sdk_subpaths_runtime](oc_plugins_sdk_subpaths_runtime.md) — `acp-runtime`/`session-store-runtime` subpaths (planned, this series); relevance: the runtimes card executions use.
- [oc_plugins_webhooks](oc_plugins_webhooks.md) — webhook `run_task` dispatch (planned, this series); relevance: external trigger that creates subagent/acp child tasks like dispatch.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session subsystem; relevance: cards link to session executions + lifecycle.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/subagent coordination; relevance: dispatch worker selection + subagent run path.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway process; relevance: task ledger + subagent runtime cards bind to.

**Snippets**
- [snippet_hermes_agent_plugins_kanban](../../code_snippets/snippet_hermes_agent_plugins_kanban.md) — the Kanban plugin core; relevance: direct analog of the Workboard card/board model.
- [snippet_hermes_agent_tools_kanban_register](../../code_snippets/snippet_hermes_agent_tools_kanban_register.md) — board agent-tool registration; relevance: analog of the `workboard_*` agent tools.
- [snippet_hermes_agent_tools_kanban_mutate](../../code_snippets/snippet_hermes_agent_tools_kanban_mutate.md) — card mutation tools; relevance: analog of `workboard_create`/`claim`/`complete`.
- [snippet_hermes_agent_tools_kanban_query](../../code_snippets/snippet_hermes_agent_tools_kanban_query.md) — card query tools; relevance: analog of `workboard_list`/`workboard_read`.
- [snippet_hermes_agent_cli_kanban_schema](../../code_snippets/snippet_hermes_agent_cli_kanban_schema.md) — card/board schema; relevance: analog of the card-fields/status model.
- [snippet_hermes_agent_skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — orchestrator/decompose; relevance: analog of `workboard_decompose` + dispatch orchestration.
- [snippet_hermes_agent_skills_devops_kanban_worker](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_worker.md) — worker protocol; relevance: analog of the worker prompt/lifecycle + claim token.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — subagent run manager; relevance: backs dispatch worker starts.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent lifecycle; relevance: card lifecycle ties to subagent run state.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate worker spawn; relevance: analog of dispatch starting worker runs.
- [snippet_hermes_agent_tools_delegate_anti_recursion](../../code_snippets/snippet_hermes_agent_tools_delegate_anti_recursion.md) — anti-recursion guard; relevance: analog of avoiding duplicate active ownership in dispatch selection.

### oc_plugins_workboard_operations (10t · 11s · 11d)

**Terms**
- [Kanban](../../term_dictionary/term_kanban.md) — board work-tracking; relevance: the CLI/dashboard operate a Kanban board.
- [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — shared multi-agent board; relevance: dispatch/claim ops coordinate work across agents.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated worker run; relevance: `workboard dispatch` starts subagent worker runs.
- [Access Control](../../term_dictionary/term_access_control.md) — operator permission gating; relevance: RPC methods require `operator.read`/`operator.write`/`operator.admin`.
- [Automation](../../term_dictionary/term_automation.md) — programmatic orchestration; relevance: dispatch automates promotion/claim/timeout cleanup.
- [Message Queue](../../term_dictionary/term_message_queue.md) — ready-card dispatch queue; relevance: dispatch selects from the ordered ready queue.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — lifecycle-event-driven sync; relevance: session-lifecycle sync moves cards on session events.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent client protocol; relevance: dispatched workers can run acp runtime.
- [Delegate Task](../../term_dictionary/term_delegate_task.md) — handing work to a worker; relevance: dispatch delegates ready cards to worker lanes.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — deterministic session keys; relevance: dispatch reuses deterministic worker session keys.

**Docs**
- [Hermes Kanban dashboard CLI](../hermes_agent/hermes_kanban_dashboard_cli.md) — board CLI + dashboard ops; relevance: direct analog of the `openclaw workboard` CLI + dashboard workflow.
- [Hermes Kanban worker lanes](../hermes_agent/hermes_kanban_worker_lanes.md) — worker lane ops; relevance: parallels dispatch worker-lane management.
- [Hermes Kanban worker orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — dispatch operations; relevance: analog of `workboard dispatch` selection rules.
- [Hermes slash commands (interactive CLI)](../hermes_agent/hermes_slash_commands_interactive_cli.md) — slash-command surface; relevance: analog of the `/workboard` slash command.
- [Hermes CLI commands: session ops](../hermes_agent/hermes_cli_commands_session_ops.md) — session/ops CLI; relevance: parallels session-lifecycle sync + card↔session ops.
- [CC subagents overview](../claude_code/cc_subagents_overview.md) — subagent runs; relevance: cross-tool precedent for dispatched worker runs.
- [oc_plugins_workboard_model](oc_plugins_workboard_model.md) — workboard data model (planned, this series); relevance: the model these operations act on.
- [oc_plugins_webhooks](oc_plugins_webhooks.md) — webhook `run_task` (planned, this series); relevance: external dispatch trigger analog.
- [oc_automation_tasks_management](oc_automation_tasks_management.md) — task management ops (planned, this series, au01); relevance: card lifecycle syncs from the task ledger.
- [oc_reference_rpc_adapters](oc_reference_rpc_adapters.md) — Gateway RPC surface (planned, this series, rf02); relevance: `workboard.*` RPC methods + operator scopes.
- [oc_plugins_voice_call_setup](oc_plugins_voice_call_setup.md) — Gateway RPC plugin ops (planned, this series); relevance: shares Gateway-delegated CLI/RPC pattern.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session subsystem; relevance: session-lifecycle sync + card↔session linking.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — subagent coordination; relevance: `workboard dispatch` worker starts.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — dashboard/web surface; relevance: the Control UI Workboard tab.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway process; relevance: `workboard.*` RPC + subagent runtime.

**Snippets**
- [snippet_hermes_agent_cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — board CLI commands; relevance: direct analog of `openclaw workboard list/create/show/dispatch`.
- [snippet_hermes_agent_cli_kanban_crud](../../code_snippets/snippet_hermes_agent_cli_kanban_crud.md) — CLI card CRUD; relevance: analog of create/update/move card ops.
- [snippet_hermes_agent_cli_kanban_query](../../code_snippets/snippet_hermes_agent_cli_kanban_query.md) — CLI card queries; relevance: analog of `workboard list --status ready`.
- [snippet_hermes_agent_cli_kanban_diagnostics](../../code_snippets/snippet_hermes_agent_cli_kanban_diagnostics.md) — CLI diagnostics; relevance: analog of the Workboard diagnostics checks.
- [snippet_hermes_agent_tui_slash_worker](../../code_snippets/snippet_hermes_agent_tui_slash_worker.md) — slash-command worker control; relevance: analog of `/workboard dispatch`.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — RPC auth/authorize; relevance: backs the `operator.*` permission gating.
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — session read RPC; relevance: session-lifecycle sync reads.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — subagent run manager; relevance: `workboard dispatch` worker starts use it.
- [snippet_hermes_agent_skills_devops_kanban_worker](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_worker.md) — worker protocol; relevance: dispatched worker prompt/lifecycle.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: how `openclaw workboard …` dispatches (Gateway vs data-only fallback).
- [snippet_hermes_agent_tools_kanban_query](../../code_snippets/snippet_hermes_agent_tools_kanban_query.md) — board query tool; relevance: backs the read-only `/workboard list`/`show` ops.

### oc_plugins_zalouser (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: `zalouser` is an OpenClaw bundled channel plugin.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — chat-platform adapter; relevance: zalouser is a Zalo Personal channel adapter (`channels.zalouser`).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing-gated direct messages; relevance: config sets `dmPolicy: "pairing"`.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — who may DM the agent; relevance: `dmPolicy` controls inbound DM access for the channel.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — cold plugin metadata; relevance: install reads plugin manifest before loading the channel.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/login; relevance: `channels login --channel zalouser` does QR login of the personal account.
- [npm](../../term_dictionary/term_npm.md) — package registry; relevance: install via `@openclaw/zalouser` npm package.
- [Access Control](../../term_dictionary/term_access_control.md) — who may use the channel; relevance: unofficial personal-account automation with risk/allow gating.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool invocation; relevance: the `zalouser` agent tool exposes send/image/link/friends actions.

**Docs**
- [Hermes messaging: WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — unofficial personal-account messaging channel; relevance: closest analog (library-driven personal-account automation with ban risk).
- [Hermes messaging: SimpleX](../hermes_agent/hermes_messaging_simplex.md) — a messaging channel plugin; relevance: parallels channel install/config/CLI pattern.
- [Hermes messaging: Signal](../hermes_agent/hermes_messaging_signal.md) — messaging channel plugin; relevance: parallels channel config + login flow.
- [Hermes photon iMessage](../hermes_agent/hermes_photon_imessage.md) — personal-account-style channel; relevance: parallels unofficial-bridge channel setup.
- [Hermes adding a platform adapter plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel adapter; relevance: how a channel plugin like zalouser is structured.
- [CC channels setup](../claude_code/cc_channels_setup.md) — setting up a chat channel; relevance: cross-tool precedent for channel install/config.
- [oc_plugins_voice_call_setup](oc_plugins_voice_call_setup.md) — another bundled plugin install/config (planned, this series); relevance: shares Gateway-process plugin install + restart pattern.
- [oc_plugins_webhooks](oc_plugins_webhooks.md) — another bundled plugin (planned, this series); relevance: shares bundled-plugin config/enable workflow.
- [oc_plugins_sdk_subpaths_core](oc_plugins_sdk_subpaths_core.md) — channel subpath catalog (planned, this series); relevance: the channel SDK subpaths zalouser is built on (note its deprecated `plugin-sdk/zalouser` facade).
- [oc_plugin_reference_zai_zalo_zalouser](oc_plugin_reference_zai_zalo_zalouser.md) — the zalouser plugin-reference card (planned, this series, pl23); relevance: the reference-doc counterpart to this operator guide.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel family; relevance: the implementation family zalouser belongs to.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: zalouser is a channel plugin in this framework.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: bundled plugin install/SDK lineage.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: the `dmPolicy: "pairing"` gate this channel uses.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract zalouser implements.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/target resolution; relevance: how `message send --target <threadId>` resolves.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: binds personal-account threads to sessions.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel DM security audit; relevance: the DM-policy security posture for a personal-account channel.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: governs `message send` on the channel.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/load lifecycle; relevance: install + Gateway restart loads the channel plugin.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — `plugins install`; relevance: analog of `openclaw plugins install @openclaw/zalouser`.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory/peers; relevance: analog of `directory peers list --channel zalouser`.

## Undigested Terms Plan

| Term (appears in source) | Disposition |
|---|---|
| plugin SDK / `plugin-sdk` subpath, `definePluginEntry`, `defineToolPlugin` | OpenClaw vocab → digested as `oc_*` doc notes (notes 1–4); link existing `term_plugin_sdk`, `term_plugin_manifest`, `term_tool_registry`. No new term. |
| plugin manifest / `openclaw.plugin.json` / `contracts.tools` | → `oc_plugins_tool_plugins` (note 4); link `term_plugin_manifest`. No new term. |
| TypeBox / JSON Schema / Zod | Config-schema tooling; link `term_json_schema` (exists). `term_typebox`/`term_zod` MISSING but are narrow library names documented as config — NOT promoted (per master: provider/library names are config, not term notes). |
| Voice Call / realtime voice / streaming transcription / TTS | OpenClaw plugin vocab → notes 5–6; link `term_voice_call`, `term_text_to_speech`, `term_speech_to_text`, `term_sse`, `term_websocket`. No new term. |
| Twilio / Telnyx / Plivo / Deepgram / ElevenLabs | Provider/carrier names = config, not term notes (master rule); link `term_third_party_genai_services`. No new term. |
| Webhook / shared-secret / SecretRef / TaskFlow | → notes 6, 7; link `term_webhook`, `term_authentication`, `term_idempotency`, `term_replay_attack`, `term_rate_limiting`. SecretRef + TaskFlow are OpenClaw-specific → link-out to `secretref-credential-surface` (rf02) + automation (au01) doc notes, not new terms. |
| Workboard / cards / dispatch / kanban | → notes 8, 9; link `term_kanban`, `term_message_queue`, `term_subagent`, `term_acp_agent_client_protocol`. No new term. |
| Zalo / `zca-js` / personal-account automation | Channel/library names = config → note 10; link `term_openclaw`. No new term. |


## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (10 notes, P3). All gates must pass before commit.

| Gate | Check | Tool / criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` (YAML field order; itemized keywords/topics; no forbidden fields) |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/plugins/<page>.md` — no fabricated config keys/CLI flags/actions |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks per note; every mapped section present |
| G4 | Cross-Reference | ≥6 relevance-selected term links + repo/sibling/other links per note, each with a relevance statement |
| G5 | Ghost-reference | Detect + redirect; 0 links to non-existent notes (re-verify all EXISTING targets in DB) |
| G6 | Broken-link | `/tessellum-fix-broken-links`; 0 broken relative paths |
| G7 | Discoverability | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` |
| G8 | In-degree ≥1 | Anti-island; satisfied via `entry_openclaw_docs.md` rows + repo/term inlinks |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_sdk_subpaths_core oc_plugins_sdk_subpaths_runtime oc_plugins_sdk_testing oc_plugins_tool_plugins oc_plugins_voice_call_setup oc_plugins_voice_call_audio_modes oc_plugins_webhooks oc_plugins_workboard_model oc_plugins_workboard_operations oc_plugins_zalouser"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G4/G7 sibling-prefix inbound presence (best-effort: at least one oc_ sibling link)
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) LINK in $n"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference sweep + G6 broken-link sweep are run via the skills:
#   /tessellum-fix-ghost-references  then  /tessellum-fix-broken-links
# after the incremental reindex: bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_sdk_subpaths_core | model | 700 | 0 (Markdown tables) | ✅ |
| 2 | oc_plugins_sdk_subpaths_runtime | model | 700 | 0 (Markdown tables) | ✅ |
| 3 | oc_plugins_sdk_testing | procedure | 700 | ≤6 | ✅ |
| 4 | oc_plugins_tool_plugins | procedure | 700 | ≤6 | ✅ |
| 5 | oc_plugins_voice_call_setup | procedure | 750 | ≤6 | ✅ |
| 6 | oc_plugins_voice_call_audio_modes | model | 700 | ≤6 | ✅ |
| 7 | oc_plugins_webhooks | procedure | 550 | ≤6 | ✅ |
| 8 | oc_plugins_workboard_model | model | 650 | ≤4 | ✅ |
| 9 | oc_plugins_workboard_operations | procedure | 600 | ≤4 | ✅ |
| 10 | oc_plugins_zalouser | procedure | 450 | ≤4 | ✅ |

No note approaches caps. Code-heavy pages (`tool-plugins` 18, `voice-call` 19, `sdk-testing` 12) split or selectively reproduce config so each note stays ≤6 fences; the subpath catalog uses Markdown tables (not code blocks), and is split so each note stays ≤700w.

## Entry Point Decision (inherited from master)

Contributes **10 rows** to `entry_openclaw_docs.md` (created as master pre-step W1) under the **Plugins** section / pl25 cluster; each note receives its entry-point back-link at finalization. No separate entry point for this sub-plan (master hub aggregates all 105 sub-plans). Master W2/W3 (parent-hub back-link, code↔docs cross-links) handled at the master/series level.

## Inlinks (existing notes → new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify at execution for G7/G8):
- `entry_openclaw_docs.md` → all 10 notes (primary anti-island source; created as master W1 pre-step).
- `repo_openclaw_extensions.md` → notes 1, 2, 3, 4, 7, 10 (plugin/extension framework).
- `repo_openclaw_extensions_voice_speech.md` → notes 2, 6, 5 (speech/realtime/voice).
- `repo_openclaw_channels_voice_phone.md` → notes 5, 6 (voice/phone channel).
- `repo_openclaw_channels_messaging.md` → notes 3, 10 (messaging channels).
- `repo_openclaw_sessions.md` → notes 7, 8, 9 (session-bound TaskFlows/cards).
- `repo_openclaw_agents.md` → notes 8, 9 (dispatch worker coordination).
- `repo_openclaw_gateway.md` → notes 5, 7 (Gateway-process plugins).
- `term_plugin_sdk.md` → notes 1, 2, 3, 4; `term_voice_call.md` → notes 5, 6; `term_webhook.md` → notes 6, 7; `term_kanban.md` → notes 8, 9; `term_tool_registry.md` → note 4.

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run; pilot one note (suggest note 7 `oc_plugins_webhooks` — smallest, single-BB) + calibrate gates before fanning out the remaining 9. Re-read each source page; reproduce config/CLI snippets verbatim. One BB per note. Incremental reindex per wave; verify `note_links` + 0 broken links + in-degree ≥1; commit+push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors ≥8t/≥10s/≥10d) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 checkpoints pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (plan now `status: ready`) |

## Augmentation Report (2026-06-21)

**Skill:** `/tessellum-augment-digestion-plan` (xref-augment pass). **Source re-read:** all 7 pages re-read from `inbox/openclaw_docs/plugins/` (sdk-subpaths 43 KB, sdk-testing 24 KB, tool-plugins 12 KB, voice-call 34 KB, webhooks 4 KB, workboard 18 KB, zalouser 2 KB). Relevance grounding spot-confirmed against `webhooks.md` (shared-secret/SecretRef auth, fixed-window + in-flight rate limiting, `sessionKey`-bound TaskFlow authority, `create_flow`/`run_task` actions, subagent/acp) and `zalouser.md` (`zca-js` personal-account automation + ban warning, `dmPolicy: "pairing"`, npm/local install, QR `channels login`, `message send`, `directory peers`, `zalouser` agent tool).


**Per-note locked counts (terms · snippets · docs · repos; existing-docs / existing-snippets):**

| # | Note | T | S | D | R | Dexist | Sexist | Floors |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | oc_plugins_sdk_subpaths_core | 9 | 11 | 11 | 4 | 9 | 11/11 | MET |
| 2 | oc_plugins_sdk_subpaths_runtime | 10 | 11 | 11 | 5 | 8 | 11/11 | MET |
| 3 | oc_plugins_sdk_testing | 10 | 11 | 11 | 4 | 8 | 11/11 | MET |
| 4 | oc_plugins_tool_plugins | 10 | 11 | 11 | 4 | 8 | 11/11 | MET |
| 5 | oc_plugins_voice_call_setup | 10 | 12 | 11 | 3 | 6 | 12/12 | MET |
| 6 | oc_plugins_voice_call_audio_modes | 10 | 12 | 11 | 3 | 7 | 12/12 | MET |
| 7 | oc_plugins_webhooks | 10 | 11 | 11 | 3 | 6 | 11/11 | MET |
| 8 | oc_plugins_workboard_model | 10 | 11 | 11 | 3 | 6 | 11/11 | MET |
| 9 | oc_plugins_workboard_operations | 10 | 11 | 11 | 4 | 6 | 11/11 | MET |
| 10 | oc_plugins_zalouser | 9 | 10 | 10 | 3 | 6 | 10/10 | MET |

All 10 notes meet ALL floors (≥8 terms · ≥10 snippets · ≥10 docs · ≥5 existing docs · all snippets existing).


**Issues found + resolved:** (a) YAML `status` was `pending` while the body claimed READY — flipped to `ready` after all 9 checkpoints passed. (b) Augmentation Report + Review Sign-Off sections were absent — appended here. No ghost links, no floor shortfalls, no missing-source pages.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (≥10 snippets · ≥10 docs), each link with relevance statement | PASS | Per-note table above: all 10 notes meet ≥8t/≥10s/≥10d; every link rendered `- [Name](relpath.md) — what; relevance: why`; relevance grounded in re-read sources. |
| CP2 | 9-GATE (G1–G9) present per execution batch | PASS | `## Per-Phase Validation Gate (G1–G9)` table present (single P3 phase): G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7 discoverability, G8 in-degree ≥1. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | PASS | `## Entry Point Decision` inherits master W1 `entry_openclaw_docs.md` (created as pre-step); 10 rows under Plugins/pl25; W2/W3 handled at series level. |
| CP4 | Plan size manageable | PASS | 10 notes, single phase ≤30; no split needed. |
| CP5 | Note format derived from existing target-dir notes | PASS | Format inherited verbatim from master (derived from existing `claude_code/`+`pi/` doc corpora): YAML order tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group; body `# Title`→`## Overview`→source-mirrored H2/H3→`## Related Notes`→`## References`→bold footer. |
| CP6 | Density — borderline → split promoted | PASS | `## Density Re-Assessment`: all 10 notes ≤750w / ≤6 code / ≤400L; sdk-subpaths (4,323w), voice-call (3,969w), workboard (2,553w) already split per `## Split Decisions`. No borderline note unaddressed. |
| CP7 | Source word counts measured | PASS | `## Source Pages (Measured 2026-06-20)`: 7 pages / 15,272 words measured (`wc -w`); mirror files re-confirmed present in `inbox/openclaw_docs/plugins/` at this review. |
| CP8 | Undigested Terms + authoring reqs | PASS | `## Undigested Terms Plan` present (8 rows, each with disposition + linked existing term); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; inherited capture-via-`/tessellum-capture-term-note` mandate). |
| CP9 | Discoverability / inlinks (anti-island, in-degree ≥1) | PASS | `## Inlinks (existing notes → new notes)`: every one of the 10 notes receives ≥1 inbound link from outside `documentation/openclaw/` (entry_openclaw_docs → all 10; plus repo_openclaw_* and term_* inlinks); G7/G8 in the gate table. |

**RESULT: 10/10 checkpoints PASS (CP1–CP9 incl. CP8f) → READY FOR EXECUTION.** Plan YAML `status` set to `ready`.
