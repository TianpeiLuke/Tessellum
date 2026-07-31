---
title: Sub-Plan pl19 — OpenClaw Docs: Plugins (reference: sglang, signal, slack, sms, stepfun, synology-chat, synthetic)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/sglang", "plugins/reference/signal", "plugins/reference/slack", "plugins/reference/sms", "plugins/reference/stepfun", "plugins/reference/synology-chat", "plugins/reference/synthetic"]
---

# Sub-Plan pl19: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_*`), format (YAML field order, `## Overview` + source-mirrored H2/H3 + `## Related Notes` + `## References` + bold footer), dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), undigested-terms ownership (OpenClaw vocab → `oc_*` doc notes, link existing terms, 0 new term captures expected), the 9-GATE table, cross-references, and entry-point wiring are ALL inherited from the master.
> This sub-plan covers 7 thin **plugin reference stub pages** (3 model-provider plugins + 4 chat-channel plugins). Each page is a 1-note `procedure` (install/configure/audit one plugin); no splits.

## Scope

The 7 plugin-reference pages `plugins/reference/{sglang, signal, slack, sms, stepfun, synology-chat, synthetic}`. Each is a one-screen reference card for a single OpenClaw plugin describing: a one-line purpose (`summary`), `read_when` audience, **Distribution** (npm package name + install route: included-in-OpenClaw / npm / ClawHub), the **Surface** it adds (a `providers:` or `channels:` capability), and a **Related docs** pointer to the corresponding provider/channel guide.

Split by surface type:
- **Model-provider plugins** (add a `providers:` surface — an LLM/inference backend): `sglang`, `stepfun` (+ `stepfun-plan`), `synthetic`.
- **Chat-channel plugins** (add a `channels:` surface — a messaging platform): `signal`, `slack`, `sms` (Twilio), `synology-chat`.

**Priority: P3** (Phase C — plugin-reference sprawl; the 1-per-plugin pages). These are pure plumbing/install references; the conceptual provider/channel knowledge lives in Phase A/B sub-plans (providers pr01–09, channels ch01–06), which these link out to. The code-side counterparts (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_channels*`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **407 measured words total**. **Planned: 7 notes** (1 per page).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| SGLang plugin | plugins/reference/sglang | 54 | 0 | 3 | 0 | procedure (provider) |
| Signal plugin | plugins/reference/signal | 62 | 0 | 3 | 0 | procedure (channel) |
| Slack plugin | plugins/reference/slack | 61 | 0 | 3 | 0 | procedure (channel) |
| Sms plugin | plugins/reference/sms | 56 | 0 | 3 | 0 | procedure (channel) |
| StepFun plugin | plugins/reference/stepfun | 59 | 0 | 3 | 0 | procedure (provider) |
| Synology Chat plugin | plugins/reference/synology-chat | 61 | 0 | 3 | 0 | procedure (channel) |
| Synthetic plugin | plugins/reference/synthetic | 54 | 0 | 3 | 0 | procedure (provider) |

Every page has the **identical 3-H2 skeleton** (`## Distribution`, `## Surface`, `## Related docs`), **0 code fences**, **0 H3**. Total 407 words. (Re-measured via `wc -w` / `grep -c '^```'` / `grep '^## '` on the mirror, 2026-06-20.)

## Content Strategy

- **Prioritize**: the load-bearing facts of each card — the npm **package name**, the **install route** (included / npm / ClawHub), and the **surface** the plugin contributes (which provider IDs or which channel). These are the only operational facts on the page.
- **Split**: none. Each page is ~55–62 words, 0 code, single BB — far below the 2,500-word / mixed-BB split thresholds. One note per page (see Split Decisions).
- **Do NOT under-fill / pad**: because the source cards are tiny, each `oc_*` note is intentionally short (~120–180 words). The `## Overview` restates the summary + surface + distribution; the source-mirrored body reproduces Distribution / Surface verbatim-faithfully; the `## Related Notes` section carries the cross-reference weight (≥6 relevancy-selected terms + sibling/planned `oc_*` + `repo_openclaw*`). No invented configuration, env vars, or steps beyond what the source states (G2 grounding).
- **Link-out (do NOT duplicate)**: the conceptual provider guide (`/providers/sglang`, `/providers/stepfun`, `/providers/synthetic`) and channel guide (`/channels/signal`, `/channels/slack`, `/channels/sms`, `/channels/synology-chat`) are owned by sub-plans **pr08** (sglang, stepfun, synthetic), **ch04** (signal), **ch05** (slack, sms, synology-chat). Each note's body links the matching planned `oc_*` guide note (cited "(planned)") and the external source URL under `## References`; the deep provider/channel setup is NOT reproduced here.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_sglang.md` | procedure | sglang.md: Distribution, Surface, Related docs | 150 | The SGLang plugin (`@openclaw/sglang-provider`, included in OpenClaw): adds the `sglang` model-provider surface for serving models via an SGLang inference backend. Distribution + surface + pointer to the SGLang provider guide. |
| 2 | `oc_plugins_reference_signal.md` | procedure | signal.md: Distribution, Surface, Related docs | 150 | The Signal plugin (`@openclaw/signal`, included in OpenClaw): adds the `signal` channel surface for sending/receiving OpenClaw messages over Signal. Distribution + surface + pointer to the Signal channel guide. |
| 3 | `oc_plugins_reference_slack.md` | procedure | slack.md: Distribution, Surface, Related docs | 160 | The Slack plugin (`@openclaw/slack`, install via npm or ClawHub): adds the `slack` channel surface for channels, DMs, slash commands, and Slack app events. Distribution + surface + pointer to the Slack channel guide. |
| 4 | `oc_plugins_reference_sms.md` | procedure | sms.md: Distribution, Surface, Related docs | 150 | The SMS plugin (`@openclaw/sms`, included in OpenClaw): a Twilio-backed `sms` channel surface for OpenClaw text messages. Distribution + surface + pointer to the SMS channel guide. |
| 5 | `oc_plugins_reference_stepfun.md` | procedure | stepfun.md: Distribution, Surface, Related docs | 160 | The StepFun plugin (`@openclaw/stepfun-provider`, npm or ClawHub `clawhub:@openclaw/stepfun-provider`): adds the `stepfun` and `stepfun-plan` model-provider surfaces. Distribution + surface + pointer to the StepFun provider guide. |
| 6 | `oc_plugins_reference_synology_chat.md` | procedure | synology-chat.md: Distribution, Surface, Related docs | 150 | The Synology Chat plugin (`@openclaw/synology-chat`, install via npm or ClawHub): adds the `synology-chat` channel surface for Synology Chat channels and direct messages. Distribution + surface + pointer to the Synology Chat channel guide. |
| 7 | `oc_plugins_reference_synthetic.md` | procedure | synthetic.md: Distribution, Surface, Related docs | 150 | The Synthetic plugin (`@openclaw/synthetic-provider`, included in OpenClaw): adds the `synthetic` model-provider surface. Distribution + surface + pointer to the Synthetic provider guide. |

Filename rule applied (master): `oc_` + full slug with `/` and `-` → `_`. `plugins/reference/sglang` → `oc_plugins_reference_sglang.md`; `plugins/reference/synology-chat` → `oc_plugins_reference_synology_chat.md`.

## Section Coverage Map

Every source page contributes its three H2 sections (Distribution / Surface / Related docs) — plus the H1 lead summary that becomes `## Overview` — to exactly one note. No orphaned sections; no H3 exist.

```
plugins/reference/sglang.md
├── (H1 lead summary) ─────── → note 1 (oc_plugins_reference_sglang) ## Overview
├── ## Distribution ───────── → note 1 (package @openclaw/sglang-provider; included in OpenClaw)
├── ## Surface ────────────── → note 1 (providers: sglang)
└── ## Related docs ───────── → note 1 (→ /providers/sglang; pr08 planned note)
plugins/reference/signal.md
├── (H1 lead summary) ─────── → note 2 (oc_plugins_reference_signal) ## Overview
├── ## Distribution ───────── → note 2 (package @openclaw/signal; included in OpenClaw)
├── ## Surface ────────────── → note 2 (channels: signal)
└── ## Related docs ───────── → note 2 (→ /channels/signal; ch04 planned note)
plugins/reference/slack.md
├── (H1 lead summary) ─────── → note 3 (oc_plugins_reference_slack) ## Overview
├── ## Distribution ───────── → note 3 (package @openclaw/slack; npm; ClawHub)
├── ## Surface ────────────── → note 3 (channels: slack)
└── ## Related docs ───────── → note 3 (→ /channels/slack; ch05 planned note)
plugins/reference/sms.md
├── (H1 lead summary) ─────── → note 4 (oc_plugins_reference_sms) ## Overview
├── ## Distribution ───────── → note 4 (package @openclaw/sms; included in OpenClaw)
├── ## Surface ────────────── → note 4 (channels: sms)
└── ## Related docs ───────── → note 4 (→ /channels/sms; ch05 planned note)
plugins/reference/stepfun.md
├── (H1 lead summary) ─────── → note 5 (oc_plugins_reference_stepfun) ## Overview
├── ## Distribution ───────── → note 5 (package @openclaw/stepfun-provider; npm; ClawHub clawhub:@openclaw/stepfun-provider)
├── ## Surface ────────────── → note 5 (providers: stepfun, stepfun-plan)
└── ## Related docs ───────── → note 5 (→ /providers/stepfun; pr08 planned note)
plugins/reference/synology-chat.md
├── (H1 lead summary) ─────── → note 6 (oc_plugins_reference_synology_chat) ## Overview
├── ## Distribution ───────── → note 6 (package @openclaw/synology-chat; npm; ClawHub)
├── ## Surface ────────────── → note 6 (channels: synology-chat)
└── ## Related docs ───────── → note 6 (→ /channels/synology-chat; ch05 planned note)
plugins/reference/synthetic.md
├── (H1 lead summary) ─────── → note 7 (oc_plugins_reference_synthetic) ## Overview
├── ## Distribution ───────── → note 7 (package @openclaw/synthetic-provider; included in OpenClaw)
├── ## Surface ────────────── → note 7 (providers: synthetic)
└── ## Related docs ───────── → note 7 (→ /providers/synthetic; pr08 planned note)
```
No orphaned sections. Conceptual provider/channel guides (pr08 / ch04 / ch05) are LINKED, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are ≤62 words, 0 code fences, single `procedure` BB — far below the 2,500-word / 6-code / mixed-BB split thresholds. Each maps 1:1 to one note. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (407 words total; per-page 54/62/61/56/59/61/54). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (3 model-provider plugins: notes 1/5/7; 4 chat-channel plugins: notes 2/3/4/6).
- Est. digest words ~**1,070** (avg ~150/note). **0 source code fences** → every note has 0–1 code blocks (at most an inline-rendered package/surface line), well under the ≤6 cap.
- **Deviation from master estimate:** master estimated 11 notes for pl19; the assigned pages are thin one-screen reference cards, so the accurate plan is **1 note per page = 7 notes**. Lower note count is driven by measured source size, not omission — every section is covered (see Section Coverage Map). Counts lock at augment.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)




### oc_plugins_reference_sglang (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this plugin extends; relevance: the umbrella product the `@openclaw/sglang-provider` package plugs into.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that adds a `providers:` surface; relevance: the SGLang plugin IS a provider plugin (its surface is `providers: sglang`).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI inference backends; relevance: SGLang is an external/self-hosted inference backend SGLang fronts.
- [vLLM](../../term_dictionary/term_vllm.md) — open-source high-throughput LLM serving engine; relevance: the closest sibling to SGLang — both are open-source inference servers for self-hosted model serving.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: SGLang serves the LLMs this provider fronts in OpenClaw.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the registry of available models a gateway exposes; relevance: SGLang-served models join OpenClaw's model catalog via this provider surface.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events streaming; relevance: inference backends like SGLang stream tokens over SSE, the provider surface's streaming transport.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — key-value attention cache for fast decoding; relevance: SGLang's RadixAttention KV-cache reuse is its defining serving optimization.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: the plugin ships as the npm package `@openclaw/sglang-provider`.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` namespace convention; relevance: the package uses the `@openclaw/` scope.

**Docs**
- [oc_providers_sglang](oc_providers_sglang.md) — conceptual SGLang provider setup guide (planned, this series, pr08); relevance: the deep `/providers/sglang` guide this reference card points to under Related docs.
- [hermes_provider_local_llm_mac](../hermes_agent/hermes_provider_local_llm_mac.md) — running a local LLM backend on Mac; relevance: closest existing analog of standing up a self-hosted inference backend like SGLang.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama provider config; relevance: parallel local/self-hosted model-provider plugin in a sibling tool.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference-provider catalog; relevance: how a sibling agent registers inference providers, the same surface SGLang adds.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — how to add a new inference provider; relevance: the generic procedure SGLang's plugin packages for OpenClaw.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types (provider/channel/tool); relevance: defines the `providers:` surface concept this plugin contributes.
- [hermes_cli_commands_chat_provider](../hermes_agent/hermes_cli_commands_chat_provider.md) — selecting a provider from the CLI; relevance: how a registered provider surface (like `sglang`) is chosen at chat time.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi's cloud-provider configuration; relevance: sibling-tool model-provider config, closest analog of configuring a provider plugin.
- [pi_custom_models](../pi/pi_custom_models.md) — registering custom/self-hosted models in Pi; relevance: SGLang serves custom self-hosted models — same registration shape.
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter setup for an inference backend; relevance: provider-adapter setup pattern mirroring the SGLang provider plugin.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the code package implementing OpenClaw provider plugins; relevance: where `@openclaw/sglang-provider` lives on the code side.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extension framework; relevance: the framework that loads provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — parallel provider-adapter layer in Hermes; relevance: sibling-ecosystem implementation of the same provider-plugin concept.

**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — OpenClaw local-model provider impl; relevance: closest code analog of a local/self-hosted provider like SGLang.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI-compatible provider; relevance: SGLang exposes an OpenAI-compatible endpoint — same provider shape.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw Anthropic provider impl; relevance: reference implementation of a provider surface this card describes.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model-catalog manifest planning; relevance: how a provider's models enter the catalog (the `providers: sglang` surface effect).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent model-catalog wiring; relevance: where SGLang-served models become selectable.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — the plugin package contract; relevance: the package shape `@openclaw/sglang-provider` conforms to.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how a provider plugin declares its surface.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the included `sglang-provider` is loaded at gateway start.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — provider fallback context; relevance: how a provider like sglang participates in failover.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-registry pattern; relevance: parallel registry where a provider surface registers.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — base provider abstract class; relevance: the contract an SGLang-style provider implements.

### oc_plugins_reference_signal (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the `@openclaw/signal` package plugs into OpenClaw.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — a plugin adding a `channels:` surface; relevance: the Signal plugin IS a channel adapter (surface `channels: signal`).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the core that dispatches messages to/from channel adapters; relevance: the Signal adapter registers with the channel kernel.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway routing messages between a platform and the agent; relevance: Signal messages flow through this gateway to the agent.
- [Chatbot](../../term_dictionary/term_chatbot.md) — an agent appearing as a bot on a platform; relevance: OpenClaw appears as a Signal bot via this plugin.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — interactive AI messaging; relevance: the send/receive interaction the Signal surface enables.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing a user's direct messages to an agent; relevance: Signal is a 1:1 DM-centric channel — pairing governs who can DM the bot.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: ships as the npm package `@openclaw/signal`.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` convention; relevance: the package uses the `@openclaw/` scope.

**Docs**
- [oc_channels_signal](oc_channels_signal.md) — conceptual Signal channel setup guide (planned, this series, ch04); relevance: the deep `/channels/signal` guide this reference card points to.
- [hermes_messaging_signal](../hermes_agent/hermes_messaging_signal.md) — Signal messaging setup in a sibling agent; relevance: closest existing analog of standing up the Signal channel.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging-gateway architecture; relevance: how a channel adapter like Signal fits the gateway.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types; relevance: defines the `channels:` surface this plugin contributes.
- [hermes_messaging_bluebubbles_imessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — a DM-centric messaging channel setup; relevance: parallel personal-messaging channel like Signal.
- [hermes_env_vars_runtime_messaging_behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — messaging runtime env vars; relevance: the kind of channel runtime config Signal needs.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — built-in/bundled plugins catalog; relevance: Signal is included-in-OpenClaw, i.e. a built-in plugin.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup in a sibling coding agent; relevance: the channel-install pattern this card abbreviates.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — extensions/plugins overview in Pi; relevance: sibling-tool view of the plugin/extension model Signal uses.
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter setup pattern; relevance: generic channel/provider adapter setup mirroring the Signal plugin.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin code package; relevance: where `@openclaw/signal` lives on the code side.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channels (Signal/Slack/SMS/Synology); relevance: the messaging-channel package Signal belongs to.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: loads channel plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel-adapter contract; relevance: the interface the Signal adapter implements.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel-kernel dispatch; relevance: how inbound Signal messages are dispatched to the agent.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how the `channels: signal` surface registers.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping Signal threads to agent conversations.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: who may DM the Signal bot (DM-centric channel).
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: routing Signal messages to the right agent binding.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package shape `@openclaw/signal` conforms to.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the included `signal` channel plugin loads at start.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — Signal platform integration code; relevance: parallel-ecosystem Signal channel implementation.
- [snippet_hermes_agent_gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Signal media handling; relevance: how Signal attachments are handled by a sibling Signal adapter.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory registry; relevance: how a channel surface like signal is catalogued.

### oc_plugins_reference_slack (11t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the `@openclaw/slack` package plugs into OpenClaw.
- [Slack](../../term_dictionary/term_slack.md) — the Slack messaging platform; relevance: the exact platform this plugin integrates (channels, DMs, slash commands, app events).
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — a plugin adding a `channels:` surface; relevance: the Slack plugin IS a channel adapter (surface `channels: slack`).
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack's WebSocket event-delivery mode; relevance: the Slack plugin commonly receives app events via Socket Mode.
- [Block Kit](../../term_dictionary/term_block_kit.md) — Slack's rich-message UI framework; relevance: Slack app messages/commands render via Block Kit on this channel.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential for app install; relevance: the Slack app is installed and authorized via OAuth tokens.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP event callback; relevance: Slack app events can arrive via webhooks (the non-Socket-Mode route).
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway routing messages; relevance: Slack messages flow through this gateway to the agent.
- [Chatbot](../../term_dictionary/term_chatbot.md) — an agent as a platform bot; relevance: OpenClaw appears as a Slack app/bot via this plugin.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: ships as `@openclaw/slack` via npm (or ClawHub).
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` convention; relevance: the package uses the `@openclaw/` scope.

**Docs**
- [oc_channels_slack](oc_channels_slack.md) — conceptual Slack channel setup guide (planned, this series, ch05); relevance: the deep `/channels/slack` guide this reference card points to.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack messaging setup in a sibling agent; relevance: closest existing analog of the full Slack channel setup.
- [cc_slack_setup_and_routing](../claude_code/cc_slack_setup_and_routing.md) — Slack setup + routing in a sibling coding agent; relevance: parallel Slack-app install + channel routing the card abbreviates.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging-gateway architecture; relevance: how the Slack channel adapter fits the gateway.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook routes + security; relevance: securing Slack event webhooks for the plugin.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types; relevance: defines the `channels:` surface Slack contributes.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup in a sibling agent; relevance: the channel-install pattern this card abbreviates.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin sources / marketplaces; relevance: the Slack plugin installs via npm or ClawHub — the multi-source install route.
- [hermes_env_vars_runtime_messaging_behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — messaging runtime env vars; relevance: Slack channel runtime config (tokens, behavior).
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter setup pattern; relevance: generic channel-adapter setup mirroring the Slack plugin.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin code package; relevance: where `@openclaw/slack` lives on the code side.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channels; relevance: the messaging-channel package Slack belongs to.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.

**Snippets**
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — OpenClaw Slack Socket Mode impl; relevance: the exact code behind this Slack plugin's event delivery.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter contract; relevance: the interface the Slack adapter implements.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reaction handling; relevance: Slack reactions/status the channel surface exposes.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel-kernel dispatch; relevance: how inbound Slack events dispatch to the agent.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how the `channels: slack` surface registers.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping Slack channels/threads/DMs to agent conversations.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package shape `@openclaw/slack` conforms to.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: routing Slack event webhooks to the plugin.
- [snippet_hermes_agent_plugins_platform_teams](../../code_snippets/snippet_hermes_agent_plugins_platform_teams.md) — a sibling enterprise-chat platform plugin; relevance: parallel app-event/command channel like Slack.
- [snippet_hermes_agent_plugins_platform_google_chat](../../code_snippets/snippet_hermes_agent_plugins_platform_google_chat.md) — Google Chat platform plugin; relevance: sibling enterprise-chat channel adapter, same surface shape.

### oc_plugins_reference_sms (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the `@openclaw/sms` package plugs into OpenClaw.
- [SMS](../../term_dictionary/term_sms.md) — short message service; relevance: the exact channel/protocol this plugin adds (text messages).
- [SMS Technology and Infrastructure](../../term_dictionary/term_sms_technology_and_infrastructure.md) — SMS delivery infrastructure; relevance: the carrier/aggregator backing (Twilio) this plugin rides on.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — a plugin adding a `channels:` surface; relevance: the SMS plugin IS a channel adapter (surface `channels: sms`).
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway routing messages; relevance: SMS messages flow through this gateway to the agent.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP event callback; relevance: inbound SMS arrives as a Twilio webhook to the gateway.
- [Chatbot](../../term_dictionary/term_chatbot.md) — an agent as a platform bot; relevance: OpenClaw answers texts as an SMS bot via this plugin.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: ships as the npm package `@openclaw/sms`.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` convention; relevance: the package uses the `@openclaw/` scope.

**Docs**
- [oc_channels_sms](oc_channels_sms.md) — conceptual SMS channel setup guide (planned, this series, ch05); relevance: the deep `/channels/sms` guide this reference card points to.
- [hermes_messaging_sms_twilio](../hermes_agent/hermes_messaging_sms_twilio.md) — Twilio SMS messaging setup in a sibling agent; relevance: closest existing analog — same Twilio-backed SMS channel.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging-gateway architecture; relevance: how the SMS channel adapter fits the gateway.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook routes + security; relevance: securing the inbound Twilio SMS webhook.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types; relevance: defines the `channels:` surface SMS contributes.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — built-in/bundled plugins; relevance: SMS is included-in-OpenClaw, i.e. a built-in plugin.
- [hermes_env_vars_runtime_messaging_behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — messaging runtime env vars; relevance: SMS channel runtime config (Twilio credentials, behavior).
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup in a sibling agent; relevance: the channel-install pattern this card abbreviates.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — extensions/plugins overview; relevance: sibling-tool view of the plugin model SMS uses.
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter setup pattern; relevance: generic channel-adapter setup mirroring the SMS plugin.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin code package; relevance: where `@openclaw/sms` lives on the code side.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channels; relevance: the messaging-channel package SMS belongs to.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channels; relevance: the phone-number-addressed sibling to the SMS text channel (same Twilio surface family).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.

**Snippets**
- [snippet_hermes_agent_gw_platform_sms](../../code_snippets/snippet_hermes_agent_gw_platform_sms.md) — Twilio SMS platform integration code; relevance: parallel-ecosystem implementation of the exact SMS channel.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter contract; relevance: the interface the SMS adapter implements.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel-kernel dispatch; relevance: how inbound SMS dispatches to the agent.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how the `channels: sms` surface registers.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping a phone number's texts to an agent conversation.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: routing SMS to the right agent binding.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package shape `@openclaw/sms` conforms to.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: routing the inbound Twilio SMS webhook to the plugin.
- [snippet_hermes_agent_gw_platform_email](../../code_snippets/snippet_hermes_agent_gw_platform_email.md) — email transport channel; relevance: a sibling non-chat-platform messaging channel (like SMS) on the gateway.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel gateway config; relevance: how an SMS channel's config block is structured.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — outbound message send dispatch; relevance: how the agent sends an outbound SMS reply.

### oc_plugins_reference_stepfun (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the `@openclaw/stepfun-provider` package plugs into OpenClaw.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin adding a `providers:` surface; relevance: the StepFun plugin IS a provider plugin (surfaces `stepfun`, `stepfun-plan`).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI inference backends; relevance: StepFun is an external GenAI model provider this plugin fronts.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: StepFun serves the LLMs this provider exposes.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-call API; relevance: StepFun models expose function-calling, the agent's tool surface.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: StepFun's `stepfun`/`stepfun-plan` models join OpenClaw's model catalog.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing requests across providers; relevance: the two StepFun surfaces participate in provider routing.
- [Model Failover](../../term_dictionary/term_model_failover.md) — falling back across model providers; relevance: a StepFun surface can be a failover target in the provider chain.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: ships as `@openclaw/stepfun-provider` via npm or ClawHub.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` convention; relevance: the package uses the `@openclaw/` scope (ClawHub ref `clawhub:@openclaw/stepfun-provider`).

**Docs**
- [oc_providers_stepfun](oc_providers_stepfun.md) — conceptual StepFun provider setup guide (planned, this series, pr08); relevance: the deep `/providers/stepfun` guide this reference card points to.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference-provider catalog; relevance: how a sibling agent registers a cloud provider like StepFun.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — how to add an inference provider; relevance: the generic procedure StepFun's plugin packages.
- [hermes_provider_aws_bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — a cloud model-provider setup; relevance: parallel cloud GenAI provider config like StepFun.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types; relevance: defines the `providers:` surface StepFun contributes (two surfaces).
- [hermes_cli_commands_chat_provider](../hermes_agent/hermes_cli_commands_chat_provider.md) — selecting a provider at the CLI; relevance: choosing `stepfun`/`stepfun-plan` at chat time.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: how StepFun API credentials are configured.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin sources / marketplaces; relevance: StepFun installs via npm OR ClawHub — the multi-source install route.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi's cloud-provider config; relevance: sibling-tool model-provider config, closest analog.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider authentication in Pi; relevance: the auth shape a cloud provider plugin like StepFun needs.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the code package implementing provider plugins; relevance: where `@openclaw/stepfun-provider` lives on the code side.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: loads provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.

**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — multi-model aggregator provider; relevance: a provider exposing multiple model surfaces, like StepFun's two (`stepfun`, `stepfun-plan`).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw cloud provider impl; relevance: reference implementation of a cloud provider surface.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw Anthropic provider; relevance: another cloud provider surface this card mirrors.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model-catalog manifest planning; relevance: how StepFun's two surfaces enter the catalog.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent model-catalog wiring; relevance: where `stepfun`/`stepfun-plan` become selectable.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package shape `@openclaw/stepfun-provider` conforms to.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how a provider plugin declares its surfaces.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the installed `stepfun-provider` loads at start.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — provider fallback context; relevance: how StepFun surfaces participate in failover.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-registry pattern; relevance: parallel registry where a provider surface registers.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: the add-a-provider pattern StepFun's plugin embodies.

### oc_plugins_reference_synology_chat (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the `@openclaw/synology-chat` package plugs into OpenClaw.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — a plugin adding a `channels:` surface; relevance: the Synology Chat plugin IS a channel adapter (surface `channels: synology-chat`).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the core dispatching to channel adapters; relevance: the Synology Chat adapter registers with the channel kernel.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway routing messages; relevance: Synology Chat messages flow through this gateway to the agent.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP event callback; relevance: Synology Chat delivers incoming messages via webhooks to the gateway.
- [Chatbot](../../term_dictionary/term_chatbot.md) — an agent as a platform bot; relevance: OpenClaw appears as a Synology Chat bot via this plugin.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — interactive AI messaging; relevance: the channels + direct-message interaction this surface enables.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: ships as `@openclaw/synology-chat` via npm or ClawHub.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` convention; relevance: the package uses the `@openclaw/` scope.

**Docs**
- [oc_channels_synology_chat](oc_channels_synology_chat.md) — conceptual Synology Chat channel setup guide (planned, this series, ch05); relevance: the deep `/channels/synology-chat` guide this reference card points to.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging-gateway architecture; relevance: how the Synology Chat channel adapter fits the gateway.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook routes + security; relevance: securing the inbound Synology Chat webhook.
- [hermes_messaging_teams_bot](../hermes_agent/hermes_messaging_teams_bot.md) — an enterprise-chat bot channel setup; relevance: parallel self-hosted-friendly team-chat channel like Synology Chat.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types; relevance: defines the `channels:` surface Synology Chat contributes.
- [hermes_messaging_simplex](../hermes_agent/hermes_messaging_simplex.md) — a niche self-hosted messaging channel; relevance: sibling self-hostable messaging platform like Synology Chat.
- [hermes_env_vars_runtime_messaging_behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — messaging runtime env vars; relevance: Synology Chat channel runtime config.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup in a sibling agent; relevance: the channel-install pattern this card abbreviates.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin sources / marketplaces; relevance: Synology Chat installs via npm or ClawHub — the multi-source install route.
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter setup pattern; relevance: generic channel-adapter setup mirroring the Synology Chat plugin.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin code package; relevance: where `@openclaw/synology-chat` lives on the code side.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channels; relevance: the messaging-channel package Synology Chat belongs to.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: loads channel plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter contract; relevance: the interface the Synology Chat adapter implements.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel-kernel dispatch; relevance: how inbound Synology Chat messages dispatch to the agent.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable channel-kernel processing; relevance: reliable delivery for a webhook channel like Synology Chat.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how the `channels: synology-chat` surface registers.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping Synology channels + DMs to agent conversations.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: routing Synology Chat messages to the right binding.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package shape `@openclaw/synology-chat` conforms to.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: routing the inbound Synology Chat webhook to the plugin.
- [snippet_hermes_agent_gw_platform_dingtalk](../../code_snippets/snippet_hermes_agent_gw_platform_dingtalk.md) — a webhook-driven enterprise-chat channel; relevance: sibling team-chat platform adapter like Synology Chat.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory registry; relevance: how a channel surface like synology-chat is catalogued.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel gateway config; relevance: how a Synology Chat channel's config block is structured.

### oc_plugins_reference_synthetic (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the `@openclaw/synthetic-provider` package plugs into OpenClaw.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin adding a `providers:` surface; relevance: the Synthetic plugin IS a provider plugin (surface `providers: synthetic`).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI inference backends; relevance: Synthetic is an external GenAI model provider this plugin fronts.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Synthetic serves the LLMs this provider exposes.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-call API; relevance: Synthetic models expose function-calling, the agent's tool surface.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: Synthetic's models join OpenClaw's model catalog via this surface.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI; relevance: Synthetic is a GenAI inference provider category.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: ships as the npm package `@openclaw/synthetic-provider`.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — the `@scope/name` convention; relevance: the package uses the `@openclaw/` scope.

**Docs**
- [oc_providers_synthetic](oc_providers_synthetic.md) — conceptual Synthetic provider setup guide (planned, this series, pr08); relevance: the deep `/providers/synthetic` guide this reference card points to.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference-provider catalog; relevance: how a sibling agent registers a cloud provider like Synthetic.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — how to add an inference provider; relevance: the generic procedure Synthetic's plugin packages.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: how a Synthetic API credential is configured.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface types; relevance: defines the `providers:` surface Synthetic contributes.
- [hermes_cli_commands_chat_provider](../hermes_agent/hermes_cli_commands_chat_provider.md) — selecting a provider at the CLI; relevance: choosing `synthetic` at chat time.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — built-in/bundled plugins; relevance: Synthetic is included-in-OpenClaw, i.e. a built-in plugin.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi's cloud-provider config; relevance: sibling-tool model-provider config, closest analog.
- [pi_custom_models](../pi/pi_custom_models.md) — registering custom models in Pi; relevance: the model-registration shape a provider plugin like Synthetic uses.
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter setup pattern; relevance: provider-adapter setup mirroring the Synthetic provider plugin.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the code package implementing provider plugins; relevance: where `@openclaw/synthetic-provider` lives on the code side.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: loads provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: hosts all plugin packages.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — parallel provider-adapter layer; relevance: sibling-ecosystem implementation of the provider-plugin concept.

**Snippets**
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw provider impl; relevance: reference implementation of a provider surface this card describes.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI-compatible provider; relevance: Synthetic exposes an OpenAI-compatible endpoint — same provider shape.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: a hosted multi-model provider, comparable to Synthetic.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model-catalog manifest planning; relevance: how Synthetic's models enter the catalog.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent model-catalog wiring; relevance: where Synthetic-served models become selectable.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package shape `@openclaw/synthetic-provider` conforms to.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how a provider plugin declares its surface.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the included `synthetic-provider` loads at start.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — provider fallback context; relevance: how the synthetic surface participates in failover.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-registry pattern; relevance: parallel registry where a provider surface registers.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: the add-a-provider pattern Synthetic's plugin embodies.


## Undigested Terms Plan (Step 4e)

pl19 creates **0 new `term_dictionary` notes** (matches the master corpus-wide decision). OpenClaw plugin/distribution vocabulary appearing on these cards is digested into the `oc_*` doc notes themselves and/or links existing terms:

| Term (appears on source) | Disposition |
|---|---|
| SGLang / StepFun / Synthetic (provider names) | Documented as config in the `oc_*` provider-plugin notes (1/5/7); NOT promoted to term notes. Link `term_third_party_genai_services` / `term_llm`. SGLang additionally relates `term_vllm`. |
| Signal / Synology Chat (platform names) | Documented inline in the `oc_*` channel-plugin notes (2/6); NOT promoted (`term_signal`/`term_synology_chat` absent in DB and not warranted — single-page references). Link `term_channel_adapter` / `term_chatbot`. |
| provider plugin / channel plugin / surface | Link EXISTING `term_provider_plugin` / `term_channel_adapter`. The "surface" concept (a `providers:`/`channels:` capability a plugin contributes) is OpenClaw-specific config vocabulary → described in the `oc_*` note bodies + owned conceptually by the Plugins-architecture sub-plans (pl01–pl04). |
| npm / ClawHub / install route | Link EXISTING `term_npm` / `term_npm_scoping`. ClawHub is the OpenClaw plugin registry → owned by the ClawHub sub-plans (cw01–cw03); link the planned `oc_clawhub_*` note, do not redefine here. |

**Term-slug collision/specificity audit:** no new slug proposed → no collision risk. Existing terms reused at their canonical slugs (`term_slack`, `term_sms`, `term_provider_plugin`, `term_channel_adapter`, `term_npm`, `term_npm_scoping`) — all confirmed substantive and DB-present; none recreated.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). Gate table identical to the master's 9-GATE definition; all must pass before commit.

| Gate | Check | Tooling |
|---|---|---|
| G1 | Format: YAML field order + `## Overview` + source-mirrored H2 + `## Related Notes` + `## References` + bold footer; no forbidden YAML fields | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every fact (package name, install route, surface) diffs against `inbox/openclaw_docs/plugins/reference/<page>.md` — no invented config/steps | manual diff vs mirror |
| G3 | Density + coverage: ≤400 lines / ≤2,500 words / ≤6 code blocks per note; all 3 H2 of each page covered; no under-fill padding | density script (below) |
| G4 | Cross-reference: ≥6 relevancy-selected term links + repo/sibling links, each with a relevance statement | manual review |
| G5 | Ghost-reference detect + redirect: every cited EXISTING target resolves in DB; planned `oc_*` marked "(planned)" | `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix: relative paths resolve | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability: each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_sglang oc_plugins_reference_signal oc_plugins_reference_slack oc_plugins_reference_sms oc_plugins_reference_stepfun oc_plugins_reference_synology_chat oc_plugins_reference_synthetic"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_ cross-link
  grep -qE "\($SIBLING_PREFIX[a-z0-9_]+\.md\)" "$f" || echo "NO SIBLING $SIBLING_PREFIX LINK in $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done

# YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_sglang | procedure | 150 | 0–1 | ✅ |
| 2 | oc_plugins_reference_signal | procedure | 150 | 0–1 | ✅ |
| 3 | oc_plugins_reference_slack | procedure | 160 | 0–1 | ✅ |
| 4 | oc_plugins_reference_sms | procedure | 150 | 0–1 | ✅ |
| 5 | oc_plugins_reference_stepfun | procedure | 160 | 0–1 | ✅ |
| 6 | oc_plugins_reference_synology_chat | procedure | 150 | 0–1 | ✅ |
| 7 | oc_plugins_reference_synthetic | procedure | 150 | 0–1 | ✅ |

No note approaches caps (all far under 2,500 words / 6 code blocks). The risk for this sub-plan is the OPPOSITE — under-fill: each note must carry real cross-reference value (≥6 relevancy terms + repo/sibling links) so it is not an orphan stub. Density gate G3 verifies coverage of all 3 H2 sections, not just word minimums.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step; the series exceeds the 30-note threshold) under the **Plugins → reference** cluster (3 provider plugins + 4 channel plugins). Each new note receives its entry-point back-link at finalization — this is the required outside-folder inbound link satisfying G7/G8. No standalone entry point for this sub-plan (it is one of 25 plugin sub-plans rolling up to the shared `entry_openclaw_docs.md`).

## Inlinks (existing notes → new notes)

Candidate inbound links from OUTSIDE `documentation/openclaw/` (for G7/G8; DB-verify + add at execution):
- `entry_openclaw_docs.md` → all 7 notes (primary anti-island link; created at master W1).
- `repo_openclaw_extensions_llm_providers` → notes 1, 5, 7 (provider-plugin code ↔ provider-plugin doc).
- `repo_openclaw_channels` / `repo_openclaw_channels_messaging` → notes 2, 3, 4, 6 (channel-plugin code ↔ channel-plugin doc).
- `repo_openclaw` → all 7 (monorepo hub).
- `term_slack` → note 3; `term_sms` → note 4; `term_provider_plugin` → notes 1, 5, 7; `term_channel_adapter` → notes 2, 3, 4, 6 (reciprocal term→doc backlinks where the term note adds a "documented in" link).

## Pacing Rules (inherited from master)

One execution phase; cap dynamic-workflow fan-out at ~30 agents/run; 8 gates before commit. Re-read each source page; reproduce package/surface facts verbatim-faithfully (G2). One BB per note. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment; per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**What was locked — per-note counts (existing-verified · planned-sibling):**

| Note | Terms | Snippets (all existing) | Docs (existing + planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_sglang | 10 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_signal | 9 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_slack | 11 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_sms | 9 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_stepfun | 10 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_synology_chat | 9 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_synthetic | 9 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |



**New-term candidates:** **NONE.** Consistent with the master corpus-wide decision (OpenClaw vocabulary → `oc_*` doc notes, link existing terms, 0 new `term_dictionary` captures). The Step 2d re-read surfaced no cross-cutting reusable term lacking both a doc-page home and an existing note. Vocabulary on these cards is provider/platform proper-nouns (SGLang, StepFun, Synthetic, Signal, Synology Chat, Twilio), OpenClaw-specific config surface (the `providers:`/`channels:` "surface" concept, owned by pl01–pl04), the ClawHub registry (owned by cw01–cw03), or already-existing terms (`term_slack`, `term_sms`, `term_provider_plugin`, `term_channel_adapter`, `term_npm`, `term_npm_scoping`).

- **Best-fit glossary for any future capture (informational):** if a provider/platform term ever warranted promotion, the agentic/LLM glossary `acronym_glossary_gen_ai.md` (providers) or the messaging/channel glossary would be the home. Not actioned this pass (0 captures).


**Dedup / collision audit (generalized to all 7 planned doc notes):** each planned `oc_plugins_reference_*` slug was checked against `resources/documentation/` and `term_dictionary/`. No existing note duplicates a plugin-reference card — the closest existing notes are the `repo_openclaw*` code notes (LINKED, not duplicated, per master dedup policy) and the sibling-tool channel/provider docs (`hermes_messaging_slack`, `hermes_messaging_signal`, `hermes_messaging_sms_twilio`, etc.) which document DIFFERENT tools (Hermes/Pi/Band), not OpenClaw plugin cards. No collision; no removals; no renames (0 new term slugs).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review per the 9-checkpoint canonical. CP7 spot-check re-read 3 source pages (slack, stepfun, sms) from the mirror.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-stated) | **PASS** | Per-Note Related Notes Mapping (LOCKED) present with an H3 per note; every note ≥8 terms (min 9, max 11), ≥10 snippets (11 each), ≥10 docs (11 each); every link carries `— <what> ; relevance: <why THIS note>`. Floors verified programmatically (all 7 floorsMet=True). |
| CP2 | 9-GATE table present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link, G7/G8 discoverability — single execution phase, all gates present. Validation Scripts section implements G1/G3/G5/G6 in bash. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)` — contributes 7 rows to `entry_openclaw_docs.md` (created master W1; series >30 notes ⇒ CREATE required); each note gets its back-link at finalization (the G7/G8 outside-folder inbound link). No standalone entry point (1 of 25 plugin sub-plans). Matches the >30 size threshold. |
| CP4 | Plan size (≤30 or split) | **PASS** | 7 planned notes — well under 30; single execution phase. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited from master Format Definition, derived from existing `resources/documentation/` notes (`cc_*`, `pi_*`, `hermes_*`): YAML field order `tags → keywords → topics → language → date of note → status → building_block → source_url → access_control_group`; body `# OpenClaw — Title` → `## Overview` → source-mirrored H2 → `## Related Notes` → `## References` → bold footer. Matches the existing `dev_tool_docs` corpus the mapping links into. |
| CP6 | Density (borderline → split promoted) | **PASS** | Density Re-Assessment table: all 7 notes ~150–160 words, 0–1 code blocks — far under caps (≤2,500w / ≤6 code / ≤400 lines). Risk is under-fill, mitigated by the locked cross-reference weight (≥8t/≥10s/≥10d). No borderline notes. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read 3 pages from mirror: slack=61w, stepfun=59w, sms=56w (within ±0% of the plan's Source table). Sum of all 7 = 407w, matches plan exactly. No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new terms, dispositions tabled); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherited multi-source mandate from master). Consistent with master corpus-wide 0-new-term decision. |
| CP8f | Slug specificity + collision audit | **PASS** | 0 new term slugs → no specificity/collision risk for term capture. Dedup audit generalized to all 7 planned doc-note slugs (Augmentation Report): no `oc_plugins_reference_*` duplicates an existing term or doc note; existing terms reused at canonical slugs (`term_slack`, `term_sms`, `term_provider_plugin`, `term_channel_adapter`, `term_npm`, `term_npm_scoping`); none recreated. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
