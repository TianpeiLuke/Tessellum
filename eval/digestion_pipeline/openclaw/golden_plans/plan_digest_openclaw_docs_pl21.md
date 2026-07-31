---
title: Sub-Plan pl21 — OpenClaw Docs: Plugins (Reference twitch…voyage)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/twitch", "plugins/reference/venice", "plugins/reference/vercel-ai-gateway", "plugins/reference/vllm", "plugins/reference/voice-call", "plugins/reference/volcengine", "plugins/reference/voyage"]
---

# Sub-Plan pl21: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`) / format (YAML order, `## Overview` + `## Related Notes` + `## References` + bold footer) / dedup (term_dictionary + documentation/ + repo_openclaw*) / 9-GATE / cross-refs / `entry_openclaw_docs.md` wiring are ALL inherited from the master.

## Scope

The 7 alphabetical plugin-reference pages `twitch` → `voyage` from `plugins/reference/`. Each is a uniform
**plugin descriptor card** (one OpenClaw plugin: its npm package, install route, and the contract surface it
registers — channels / providers / tools / speechProviders / memoryEmbeddingProviders), with a pointer to the
deeper channel/provider/tool doc. The 7 plugins: **twitch** (Twitch chat/moderation channel), **venice**
(Venice LLM provider), **vercel-ai-gateway** (Vercel AI Gateway LLM-aggregator provider), **vllm** (vLLM
self-hosted inference-server provider), **voice-call** (Twilio/Telnyx/Plivo telephony tool plugin),
**volcengine** (Volcengine LLM + speech provider), **voyage** (Voyage memory-embedding provider). **Priority P3**
(Phase C — plugin reference sprawl; runs after the conceptual/operational core and the feature/provider docs).
These descriptor cards are the plugin-packaging view of capabilities documented in depth by the channels /
providers / tools / concepts sub-plans, which they LINK rather than redefine.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| twitch | plugins/reference/twitch | 57 | 0 | 3 | 0 | concept (channel plugin descriptor) |
| venice | plugins/reference/venice | 54 | 0 | 3 | 0 | concept (provider plugin descriptor) |
| vercel-ai-gateway | plugins/reference/vercel-ai-gateway | 62 | 0 | 3 | 0 | concept (provider plugin descriptor) |
| vllm | plugins/reference/vllm | 54 | 0 | 3 | 0 | concept (provider plugin descriptor) |
| voice-call | plugins/reference/voice-call | 61 | 0 | 3 | 0 | concept (tool plugin descriptor) |
| volcengine | plugins/reference/volcengine | 61 | 0 | 3 | 0 | concept (provider plugin descriptor) |
| voyage | plugins/reference/voyage | 45 | 0 | 2 | 0 | concept (memory-embedding provider descriptor) |

**Total: 7 pages, 394 measured words, 0 code fences.** Uniform H2 set per page: `## Distribution`,
`## Surface`, `## Related docs` (voyage omits `## Related docs` — 2 H2). All far below the 2,500-word / 6-code
split caps.

## Content Strategy

- **Prioritize:** the descriptor identity of each plugin — npm package name, install route (npm+ClawHub vs
  bundled "included in OpenClaw"), and the **contract surface** it registers (the `channels:` / `providers:` /
  `contracts:` line, which is the load-bearing fact: it tells you *what capability the plugin adds and under
  which contract*). Capture the "Related docs" pointer as a `## Related Notes`/`## References` cross-link.
- **Split:** NONE. Every page is a 45–62-word single-BB descriptor card — far below the word/code caps and a
  single building block (a plugin's identity + surface). 1 page = 1 note.
- **Link-out (do NOT redefine):** the deeper capability each plugin packages is documented by other sub-plans —
  Twitch channel behavior (`channels/twitch`, ch05), the Venice/Vercel-AI-Gateway/vLLM/Volcengine provider
  config (`providers/*`, pr05–09), voice-call telephony (`plugins/voice-call`, pl25), Voyage embeddings
  (memory/embedding concepts). Link those as Related Notes / References; this card only states the package +
  surface. Term vocabulary (vLLM, voice-call, embedding, content-moderation) links existing `term_dictionary`
  notes — never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_twitch.md` | concept | plugins/reference/twitch.md: Distribution, Surface, Related docs | 220 | The `@openclaw/twitch` channel plugin: npm + ClawHub install route, the `channels: twitch` surface it registers for chat and moderation workflows, and the pointer to the Twitch channel doc. |
| 2 | `oc_plugins_reference_venice.md` | concept | plugins/reference/venice.md: Distribution, Surface, Related docs | 200 | The `@openclaw/venice-provider` plugin (bundled in OpenClaw): registers the `providers: venice` LLM provider surface, with a pointer to the Venice provider config doc. |
| 3 | `oc_plugins_reference_vercel_ai_gateway.md` | concept | plugins/reference/vercel-ai-gateway.md: Distribution, Surface, Related docs | 210 | The `@openclaw/vercel-ai-gateway-provider` plugin (bundled): registers the `providers: vercel-ai-gateway` aggregator-gateway provider surface, pointing to the Vercel AI Gateway provider doc. |
| 4 | `oc_plugins_reference_vllm.md` | concept | plugins/reference/vllm.md: Distribution, Surface, Related docs | 200 | The `@openclaw/vllm-provider` plugin (bundled): registers the `providers: vllm` self-hosted inference-server provider surface, pointing to the vLLM provider doc. |
| 5 | `oc_plugins_reference_voice_call.md` | concept | plugins/reference/voice-call.md: Distribution, Surface, Related docs | 220 | The `@openclaw/voice-call` plugin (npm + ClawHub): registers a `contracts: tools` surface for Twilio/Telnyx/Plivo phone calls, with a pointer to the voice-call plugin doc. |
| 6 | `oc_plugins_reference_volcengine.md` | concept | plugins/reference/volcengine.md: Distribution, Surface, Related docs | 220 | The `@openclaw/volcengine-provider` plugin (bundled): registers `providers: volcengine, volcengine-plan` and a `contracts: speechProviders` surface, pointing to the Volcengine provider doc. |
| 7 | `oc_plugins_reference_voyage.md` | concept | plugins/reference/voyage.md: Distribution, Surface | 180 | The `@openclaw/voyage-provider` plugin (bundled): registers a `contracts: memoryEmbeddingProviders` surface adding Voyage embedding support for OpenClaw memory. |

**7 planned notes, all `concept` BB.** (Master's per-sub-plan estimate was 11 notes; these 7 pages are uniform
45–62-word descriptor stubs with no internal split, so the locked count is **7 notes = 7 pages**, one card per
plugin. No padding, no synthetic notes.)

## Section Coverage Map

Every source page's H2 sections map to exactly one planned note. No orphans.

```
plugins/reference/twitch.md
├── ## Distribution (Package @openclaw/twitch; npm; ClawHub) ─ → note 1 (oc_plugins_reference_twitch) Overview/body
├── ## Surface (channels: twitch) ──────────────────────────── → note 1
└── ## Related docs ([twitch](/channels/twitch)) ───────────── → note 1 (Related Notes / References → ch05 + repo_openclaw_channels)
plugins/reference/venice.md
├── ## Distribution (@openclaw/venice-provider; included) ──── → note 2 (oc_plugins_reference_venice)
├── ## Surface (providers: venice) ─────────────────────────── → note 2
└── ## Related docs ([venice](/providers/venice)) ──────────── → note 2 (→ pr08 + repo_openclaw_extensions_llm_providers)
plugins/reference/vercel-ai-gateway.md
├── ## Distribution (@openclaw/vercel-ai-gateway-provider) ─── → note 3 (oc_plugins_reference_vercel_ai_gateway)
├── ## Surface (providers: vercel-ai-gateway) ──────────────── → note 3
└── ## Related docs ([vercel-ai-gateway](/providers/…)) ────── → note 3 (→ pr08 + repo_openclaw_extensions_llm_providers)
plugins/reference/vllm.md
├── ## Distribution (@openclaw/vllm-provider; included) ────── → note 4 (oc_plugins_reference_vllm)
├── ## Surface (providers: vllm) ───────────────────────────── → note 4
└── ## Related docs ([vllm](/providers/vllm)) ──────────────── → note 4 (→ pr09 + term_vllm + repo_openclaw_extensions_llm_providers)
plugins/reference/voice-call.md
├── ## Distribution (@openclaw/voice-call; npm; ClawHub) ───── → note 5 (oc_plugins_reference_voice_call)
├── ## Surface (contracts: tools) ──────────────────────────── → note 5
└── ## Related docs ([voice-call](/plugins/voice-call)) ────── → note 5 (→ pl25 + repo_openclaw_channels_voice_phone)
plugins/reference/volcengine.md
├── ## Distribution (@openclaw/volcengine-provider) ────────── → note 6 (oc_plugins_reference_volcengine)
├── ## Surface (providers: volcengine, volcengine-plan; contracts: speechProviders) → note 6
└── ## Related docs ([volcengine](/providers/volcengine)) ──── → note 6 (→ pr09 + repo_openclaw_extensions_llm_providers/_voice_speech)
plugins/reference/voyage.md
├── ## Distribution (@openclaw/voyage-provider; included) ──── → note 7 (oc_plugins_reference_voyage)
└── ## Surface (contracts: memoryEmbeddingProviders) ───────── → note 7 (→ term_embedding + repo_openclaw_memory)
```

No orphaned sections. The `[slug](/path)` "Related docs" pointers become Related Notes / References cross-links
to the deeper channels/providers/tools/memory notes (other sub-plans), not new content here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 45–62-word single-BB descriptor cards, far below the 2,500-word / 6-code split caps; each is one plugin's identity + surface ⇒ 1 page = 1 note, no split. |

## Summary Statistics & Building Block Distribution

- **Source pages:** 7 (394 words total, avg ~56 w/page; 0 code fences).
- **New `oc_*` notes:** 7. **New `term_dictionary` notes:** 0 (Undigested Terms Plan below).
- **BB distribution:** concept ×7 (every page is a plugin descriptor card — identity + registered surface).
- **Est. digest words:** ~1,450 (avg ~207/note). Each note is intentionally short (Overview + Distribution +
  Surface + Related Notes/References) — well under all density caps. No source code to reproduce.
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** each note's mapping meets **≥8
  relevancy-selected `term_dictionary` terms · ≥10 code_snippets · ≥10 docs**, plus relevant `repo_openclaw*`
  series) marked "(planned)". See **## Per-Note Related Notes Mapping (LOCKED)** below for the per-note lists.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> FROM a note at `resources/documentation/openclaw/oc_X.md` (term → `../../term_dictionary/`; snippet →
> `../../code_snippets/`; other doc → `../<folder>/`; sibling oc_ → `oc_Y.md`; repo →
> `../../../areas/code_repos/`). Sibling `oc_*` cards (this series) do NOT exist yet → marked

### oc_plugins_reference_twitch (12t · 12s · 11d)

The `@openclaw/twitch` channel plugin (npm + ClawHub) registering the `channels: twitch` surface for chat and
moderation workflows. Subject = a messaging/channel plugin descriptor; mapping draws the channel-adapter
machinery, the messaging-channel doc corpus, and the abuse/moderation bridge.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this plugin extends; relevance: the product the `@openclaw/twitch` package plugs into.
- [Chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent on a chat platform; relevance: a Twitch channel bot IS a chatbot.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — automated detection/removal of policy-violating chat content; relevance: the plugin's stated purpose is "chat and moderation workflows".
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — bot operating a real-time conversational channel; relevance: peer channel-agent surface to the Twitch chat bot.
- [npm](../../term_dictionary/term_npm.md) — Node package manager / registry; relevance: the plugin's primary install route ("npm; ClawHub").
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol for tool/capability exposure; relevance: channel plugins surface agent capabilities the same MCP-style contract describes.
- [Function Calling](../../term_dictionary/term_function_calling.md) — structured tool invocation by an LLM agent; relevance: a moderation bot acts via tool/function calls on chat events.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex live transport; relevance: Twitch chat (IRC-over-WebSocket) is the channel's live event stream.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — abstraction normalizing a platform into the gateway's channel contract; relevance: the `channels: twitch` surface is exactly a channel adapter.
- [Slack](../../term_dictionary/term_slack.md) — peer chat platform with a channel plugin; relevance: closest documented sibling messaging channel for moderation/bot patterns.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — WebSocket connection mode for chat events (Slack); relevance: structurally analogous to Twitch's live-chat socket transport.
- [Social Identity](../../term_dictionary/term_social_identity.md) — account/identity signals in social platforms; relevance: moderation workflows key off chatter identity/trust.

**Docs**
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — the plugin contract-surface taxonomy (channels/providers/tools) in the sibling Hermes agent; relevance: defines the same `channels:` surface this card registers.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin install/registration system; relevance: the npm+marketplace install model mirrored by ClawHub.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — how a messaging channel is docked into the gateway; relevance: explains the runtime the `channels: twitch` plugin attaches to.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — a concrete chat-channel plugin setup; relevance: closest documented analog for a chat/moderation channel.
- [hermes_discord_setup](../hermes_agent/hermes_discord_setup.md) — Discord chat-channel plugin setup; relevance: another live-chat moderation-capable channel peer.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram channel plugin setup; relevance: peer messaging-channel descriptor pattern.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — Claude Code channel concept overview; relevance: the cross-agent "channel" abstraction this Twitch card instantiates.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — how to set up a Claude Code channel; relevance: the install-and-register flow parallel to npm+ClawHub.
- [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — running a coding agent inside a chat channel; relevance: the chat-bot deployment shape Twitch mirrors.
- [oc_channels_twitch](oc_channels_twitch.md) (planned, this series) — the deeper Twitch channel behavior doc (ch05); relevance: the "[twitch](/channels/twitch)" Related-docs pointer this card defers to.
- [oc_plugins_reference_voice_call](oc_plugins_reference_voice_call.md) (planned, this series) — peer npm+ClawHub plugin card; relevance: same install route + contract-surface descriptor pattern.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the OpenClaw channels package home; relevance: source home of the Twitch channel plugin.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: where chat-channel adapters like Twitch live.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: umbrella code home the plugin ships within.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel-adapter interface every channel plugin implements; relevance: the contract the `channels: twitch` surface satisfies.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how a registered channel plugin like twitch is keyed.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/routing of inbound channel events; relevance: routes Twitch chat events to the agent.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel-kernel event dispatch; relevance: the dispatch path a Twitch message takes.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — socket-mode live chat ingestion (Slack); relevance: structurally identical to Twitch's live-chat socket.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram message dispatcher; relevance: peer chat-channel dispatcher pattern.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord gateway intents/event filtering; relevance: chat-event subscription analog for Twitch.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — message-to-agent match resolution; relevance: decides which agent handles a Twitch chat message.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/thread resolution; relevance: groups Twitch chat into conversations for the agent.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reaction emission to a channel; relevance: how a moderation bot signals on Twitch.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — security audit of channel message sources; relevance: trust/moderation gating on inbound chat.
- [snippet_hermes_agent_plugins_platform_irc](../../code_snippets/snippet_hermes_agent_plugins_platform_irc.md) — IRC platform plugin (Hermes); relevance: Twitch chat is IRC-protocol; closest transport analog.

### oc_plugins_reference_venice (10t · 12s · 11d)

The `@openclaw/venice-provider` plugin (bundled "included in OpenClaw") registering the `providers: venice` LLM
provider surface. Subject = an LLM provider-plugin descriptor; mapping draws the provider-registry / model-catalog
machinery and the provider doc corpus across the sibling coding-agents.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this provider plugin extends; relevance: the product the venice provider plugs into.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Venice is an LLM model provider.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — externally-hosted GenAI APIs; relevance: Venice is an external GenAI provider the plugin fronts.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model provider; relevance: this card IS a provider plugin.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the registry of available models per provider; relevance: registering venice contributes its models to the catalog.
- [Model Router](../../term_dictionary/term_model_router.md) — selects which provider/model serves a request; relevance: the provider must be selectable by the router.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing logic across registered providers; relevance: venice participates in provider routing once registered.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI; relevance: the capability class Venice supplies.
- [Function Calling](../../term_dictionary/term_function_calling.md) — structured tool invocation by the model; relevance: a provider must surface tool/function-calling for agent use.
- [Claude](../../term_dictionary/term_claude.md) — reference LLM provider model; relevance: peer model the catalog also exposes, for provider-comparison.

**Docs**
- [hermes_plugin_llm_access](../hermes_agent/hermes_plugin_llm_access.md) — how a provider plugin grants LLM access; relevance: the exact `providers:` surface this card registers.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — the provider runtime that loads provider plugins; relevance: the runtime venice attaches to.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider catalog; relevance: Venice is one such cloud provider.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a new inference provider; relevance: the bundled-provider registration this card embodies.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: where the venice provider's models land.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing and proxying; relevance: how requests reach the venice upstream.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom model provider (Pi); relevance: cross-agent analog of provider-plugin registration.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud provider list; relevance: provider-catalog peer for a hosted LLM service.
- [band_adapter_catalog](../band/band_adapter_catalog.md) — the Band adapter (provider) catalog; relevance: cross-agent provider-registry analog.
- [oc_providers_venice](oc_providers_venice.md) (planned, this series) — the deeper Venice provider config doc (pr08); relevance: the "[venice](/providers/venice)" Related-docs pointer this card defers to.
- [oc_plugins_reference_vllm](oc_plugins_reference_vllm.md) (planned, this series) — peer bundled provider-plugin card; relevance: same `providers:` descriptor pattern.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-providers extensions package; relevance: source home of the venice provider plugin.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extensions/plugins package; relevance: umbrella home for bundled provider plugins.

**Snippets**
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a concrete OpenClaw provider plugin (Anthropic); relevance: exact peer implementation of the venice provider.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: peer hosted-LLM provider implementation.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider plugin; relevance: provider-plugin variant venice sits beside.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — the model catalog assembly; relevance: where venice's models are registered.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: planning which provider/model is available.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalization; relevance: normalizing venice's model list into the catalog.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: shaping venice's model schema.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: pricing wiring a provider's models inherit.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — the provider plugin registry (Hermes); relevance: the registry a provider plugin registers into.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin scaffold; relevance: the shape of a provider plugin like venice.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the interface a venice provider must implement.

### oc_plugins_reference_vercel_ai_gateway (11t · 12s · 11d)

The `@openclaw/vercel-ai-gateway-provider` plugin (bundled) registering the `providers: vercel-ai-gateway`
aggregator/gateway provider surface. Subject = an aggregator-gateway provider-plugin descriptor; mapping adds the
api-gateway/reverse-proxy/router vocabulary on top of the shared provider machinery.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this provider plugin extends; relevance: the product the vercel-ai-gateway provider plugs into.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the provider serves LLM requests.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a single entry that fronts/aggregates upstream APIs; relevance: Vercel AI Gateway IS an LLM API gateway.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server fronting upstream backends; relevance: the gateway reverse-proxies upstream model providers.
- [Model Router](../../term_dictionary/term_model_router.md) — routes requests across providers/models; relevance: the gateway routes across multiple upstream LLMs.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing across registered providers; relevance: the aggregator's core function.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: the gateway aggregates many external GenAI services.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a model provider; relevance: this card IS a provider plugin (registering the gateway as one provider).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: the gateway contributes its aggregated models to the catalog.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — a gateway fronting tool/capability access; relevance: structural analog to an LLM aggregator gateway.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI; relevance: the capability class the gateway aggregates.

**Docs**
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing and proxying; relevance: the exact aggregator/proxy behavior this gateway provides.
- [hermes_plugin_llm_access](../hermes_agent/hermes_plugin_llm_access.md) — provider-plugin LLM access surface; relevance: the `providers:` surface this card registers.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime loading provider plugins; relevance: the runtime the gateway provider attaches to.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider catalog; relevance: gateway is one cloud-aggregator entry.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding an inference provider; relevance: the bundled-provider registration pattern.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: the gateway's upstream credential surface.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom provider (Pi); relevance: cross-agent provider-plugin registration analog.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — model override/compat layer (Pi); relevance: aggregator overrides/maps upstream model ids.
- [band_creating_adapters_patterns](../band/band_creating_adapters_patterns.md) — adapter (provider) patterns (Band); relevance: aggregator-adapter design analog.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) (planned, this series) — the deeper Vercel AI Gateway provider config doc (pr08); relevance: the Related-docs pointer this card defers to.
- [oc_plugins_reference_venice](oc_plugins_reference_venice.md) (planned, this series) — peer bundled provider-plugin card; relevance: same `providers:` descriptor pattern.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-providers extensions package; relevance: source home of the gateway provider plugin.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extensions package; relevance: umbrella home for bundled provider plugins.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters in Hermes; relevance: cross-agent aggregator-adapter implementation.

**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — an aggregator provider plugin (OpenRouter); relevance: exact peer of the Vercel AI Gateway aggregator.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — aggregator pricing via OpenRouter/LiteLLM; relevance: how an aggregator-gateway's per-model pricing is resolved.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: alias resolution across aggregated upstreams.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: a typical upstream the gateway fronts.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider plugin; relevance: another upstream behind the aggregator.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — the model catalog assembly; relevance: where the gateway's aggregated models register.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalization; relevance: discovering the gateway's downstream model list.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxied client connection; relevance: the proxy hop an aggregator gateway introduces.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter aggregator provider (Hermes); relevance: cross-agent aggregator-provider peer.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: the registry the gateway provider registers into.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the interface the gateway provider implements.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — provider adapter client; relevance: the upstream-client layer an aggregator wraps.

### oc_plugins_reference_vllm (11t · 12s · 12d)

The `@openclaw/vllm-provider` plugin (bundled) registering the `providers: vllm` self-hosted inference-server
provider surface. Subject = a self-hosted OpenAI-compatible inference-server provider-plugin descriptor; mapping
adds vLLM serving internals (KV cache, structured output) and the rich AWS-SageMaker vLLM deployment corpus.

**Terms**
- [vLLM](../../term_dictionary/term_vllm.md) — high-throughput LLM inference/serving engine; relevance: the exact subject of this plugin card.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this provider extends; relevance: the product the vllm provider plugs into.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: vLLM serves LLMs.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a model provider; relevance: this card IS a provider plugin.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external/self-hosted GenAI endpoints; relevance: a vLLM server is a self-hosted OpenAI-compatible GenAI endpoint.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: the vLLM-served models register into the catalog.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — cached attention keys/values for fast decode; relevance: vLLM's paged-KV-cache (PagedAttention) is its defining serving optimization.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reusing prefix computation across requests; relevance: a vLLM serving optimization layered on KV cache.
- [Structured Output](../../term_dictionary/term_structured_output.md) — constrained/JSON-schema generation; relevance: vLLM supports guided/structured decoding.
- [Model Router](../../term_dictionary/term_model_router.md) — selects provider/model per request; relevance: the vLLM provider must be selectable by the router.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing across providers; relevance: vLLM participates in provider routing once registered.

**Docs**
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — a local/self-hosted model provider (Ollama); relevance: closest analog to a self-hosted vLLM provider.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding an inference provider; relevance: the registration pattern for the vllm provider.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime; relevance: the runtime the vllm provider attaches to.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — inference provider catalog; relevance: vLLM is an OpenAI-compatible inference endpoint in this class.
- [sagemaker_dlc_vllm_models](../aws_sagemaker/sagemaker_dlc_vllm_models.md) — vLLM-served models on SageMaker DLC; relevance: deep treatment of the exact engine this plugin fronts.
- [sagemaker_dlc_vllm_sagemaker](../aws_sagemaker/sagemaker_dlc_vllm_sagemaker.md) — deploying vLLM on SageMaker; relevance: a concrete vLLM serving deployment behind the provider.
- [sagemaker_dlc_vllm_config](../aws_sagemaker/sagemaker_dlc_vllm_config.md) — vLLM serving configuration; relevance: the server config a vLLM provider connects to.
- [sagemaker_dlc_vllm_ec2](../aws_sagemaker/sagemaker_dlc_vllm_ec2.md) — vLLM on EC2; relevance: self-hosted vLLM deployment shape.
- [sagemaker_dlc_images_vllm](../aws_sagemaker/sagemaker_dlc_images_vllm.md) — vLLM DLC container images; relevance: the runtime image serving the vLLM endpoint.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud/self-hosted provider list (Pi); relevance: cross-agent provider-catalog analog including local endpoints.
- [oc_providers_vllm](oc_providers_vllm.md) (planned, this series) — the deeper vLLM provider config doc (pr09); relevance: the "[vllm](/providers/vllm)" Related-docs pointer this card defers to.
- [oc_plugins_reference_volcengine](oc_plugins_reference_volcengine.md) (planned, this series) — peer bundled provider-plugin card; relevance: same `providers:` descriptor pattern.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-providers extensions package; relevance: source home of the vllm provider plugin.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extensions package; relevance: umbrella home for bundled provider plugins.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters in Hermes; relevance: cross-agent local/self-hosted provider implementation.

**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — a local/self-hosted provider plugin (Ollama); relevance: closest peer to a self-hosted vLLM provider.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: vLLM exposes the OpenAI-compatible API this implements.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider plugin; relevance: peer provider-plugin implementation.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: where vLLM-served models register.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalization; relevance: discovering models from a vLLM endpoint.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: shaping vLLM model schemas.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: a self-hosted vLLM endpoint sits in the fallback chain.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — provider failover on error; relevance: failover when a self-hosted vLLM server is down.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin scaffold; relevance: the shape of a self-hosted provider plugin.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Ollama provider plugin (Hermes); relevance: cross-agent local-model provider peer.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the interface the vllm provider implements.

### oc_plugins_reference_voice_call (12t · 12s · 12d)

The `@openclaw/voice-call` plugin (npm + ClawHub) registering a `contracts: tools` surface for Twilio/Telnyx/Plivo
phone calls. Subject = a telephony tool-plugin descriptor; mapping draws the voice-call runtime, the speech (TTS/STT)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the product the voice-call plugin plugs into.
- [Voice Call](../../term_dictionary/term_voice_call.md) — agent-driven real-time phone call; relevance: the exact subject of this plugin card.
- [VoIP](../../term_dictionary/term_voip.md) — voice over IP telephony; relevance: Twilio/Telnyx/Plivo are VoIP carriers the plugin integrates.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — bot conducting a voice conversation; relevance: the agent persona on a voice call.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — real-time voice interaction mode; relevance: the interaction surface a phone call exposes.
- [npm](../../term_dictionary/term_npm.md) — Node package manager/registry; relevance: the plugin's install route ("npm; ClawHub").
- [SMS](../../term_dictionary/term_sms.md) — short message service; relevance: peer carrier-based messaging channel (Twilio also serves SMS).
- [Function Calling](../../term_dictionary/term_function_calling.md) — structured tool invocation; relevance: the plugin registers under the `tools` contract, invoked via function calls.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing speech from text; relevance: the agent's voice on the call is TTS-generated.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribing speech to text; relevance: the caller's audio is STT-transcribed for the agent.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming live transcription; relevance: a live phone call needs streaming STT.

**Docs**
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI usage (Hermes); relevance: the voice interaction surface analog.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — using voice mode; relevance: how a user drives an agent voice session.
- [hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice over a Discord voice channel; relevance: another real-time voice transport peer.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription; relevance: the STT half of the call pipeline.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the TTS half of the call pipeline.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio settings; relevance: audio handling config a voice call needs.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin contract-surface taxonomy; relevance: the `contracts: tools` surface this card registers.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — plugin install/registration system; relevance: the npm+marketplace install model the plugin uses.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — channel/integration concept overview; relevance: the cross-agent integration abstraction.
- [oc_plugins_voice_call](oc_plugins_voice_call.md) (planned, this series) — the deeper voice-call plugin doc (pl25); relevance: the "[voice-call](/plugins/voice-call)" Related-docs pointer this card defers to.
- [oc_plugins_reference_volcengine](oc_plugins_reference_volcengine.md) (planned, this series) — peer plugin card with a speechProviders surface; relevance: shared speech-capability descriptor pattern.
- [oc_plugins_reference_twitch](oc_plugins_reference_twitch.md) (planned, this series) — peer npm+ClawHub plugin card; relevance: same install-route descriptor pattern.

**Repos**
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — the voice/phone channel package; relevance: source home of the voice-call plugin.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: the TTS/STT machinery a call uses.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: umbrella code home.

**Snippets**
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — the voice-call manager; relevance: the runtime entry point of this exact plugin.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: the runtime the plugin's tool contract drives.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — media-stream admission control; relevance: admitting a phone call's audio stream.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — call audio media stream; relevance: the bidirectional call audio path.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — in-call transcription stream; relevance: live STT on the call.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — carrier webhook signature verification; relevance: validating Twilio/Telnyx/Plivo callbacks.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay-cache; relevance: dedupe of carrier webhook events.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS integration; relevance: the agent voice rendered on the call.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT integration; relevance: transcribing the caller's speech.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay through the gateway; relevance: routing call transcripts to the agent.
- [snippet_hermes_agent_gw_platform_sms](../../code_snippets/snippet_hermes_agent_gw_platform_sms.md) — SMS platform handler (Hermes); relevance: peer carrier-channel (Twilio SMS) implementation.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool (Hermes); relevance: cross-agent voice tool-contract peer.

### oc_plugins_reference_volcengine (11t · 12s · 11d)

The `@openclaw/volcengine-provider` plugin (bundled) registering `providers: volcengine, volcengine-plan` AND a
`contracts: speechProviders` surface. Subject = a dual LLM-provider + speech-provider plugin descriptor; mapping
spans both the provider-registry machinery and the speech (TTS/STT) corpus.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the product the volcengine plugin plugs into.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Volcengine is an LLM model provider.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a model provider; relevance: this card registers two provider entries (volcengine, volcengine-plan).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Volcengine is an external GenAI provider.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the `speechProviders` contract supplies TTS.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: the `speechProviders` contract supplies STT.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — voice-conversation agent; relevance: the consumer of the speech providers this plugin registers.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: Volcengine's models register into the catalog.
- [Model Router](../../term_dictionary/term_model_router.md) — selects provider/model; relevance: volcengine and volcengine-plan must be router-selectable.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing across providers; relevance: both volcengine entries participate.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI; relevance: the capability class Volcengine supplies.

**Docs**
- [hermes_plugin_llm_access](../hermes_agent/hermes_plugin_llm_access.md) — provider-plugin LLM access; relevance: the `providers:` surface this card registers.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime; relevance: the runtime the volcengine provider attaches to.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding an inference provider; relevance: the bundled-provider registration pattern.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider catalog; relevance: Volcengine is a cloud LLM provider entry.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the speechProviders (TTS) surface this card also registers.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription; relevance: the speechProviders (STT) side.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing/proxying; relevance: how requests reach the volcengine upstreams.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom provider (Pi); relevance: cross-agent provider-registration analog.
- [band_adapter_catalog](../band/band_adapter_catalog.md) — adapter (provider) catalog (Band); relevance: cross-agent provider-registry analog.
- [oc_providers_volcengine](oc_providers_volcengine.md) (planned, this series) — the deeper Volcengine provider config doc (pr09); relevance: the "[volcengine](/providers/volcengine)" Related-docs pointer this card defers to.
- [oc_plugins_reference_voice_call](oc_plugins_reference_voice_call.md) (planned, this series) — peer plugin card touching the speech/voice surface; relevance: shared speech-capability descriptor pattern.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-providers extensions; relevance: source home of the volcengine LLM provider.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: source home of the volcengine speechProviders surface.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extensions package; relevance: umbrella home for bundled plugins.

**Snippets**
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a concrete provider plugin; relevance: peer LLM-provider implementation for volcengine.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: peer hosted-LLM provider implementation.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: where Volcengine's models register.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalization; relevance: discovering Volcengine's two provider entries.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a TTS speech-provider integration; relevance: peer of the volcengine TTS speechProvider.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — an STT speech-provider integration; relevance: peer of the volcengine STT speechProvider.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — the speech pipeline; relevance: where a speechProvider plugs in.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — a local TTS speech-provider; relevance: another speechProviders implementation peer.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: the registry both volcengine entries register into.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-region provider cluster (Hermes); relevance: Volcengine (ByteDance) is a China-region provider peer.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing (Hermes); relevance: routing across speech providers like volcengine TTS.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the interface the volcengine providers implement.

### oc_plugins_reference_voyage (10t · 12s · 11d)

The `@openclaw/voyage-provider` plugin (bundled) registering a `contracts: memoryEmbeddingProviders` surface,
adding Voyage embedding support for OpenClaw memory. Subject = a memory-embedding provider-plugin descriptor;
mapping draws the embedding/vector-memory/retrieval corpus.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: the product the voyage plugin plugs into.
- [Embedding](../../term_dictionary/term_embedding.md) — dense vector representation of text; relevance: Voyage adds embedding support — the exact subject.
- [Vector Database](../../term_dictionary/term_vector_database.md) — store + ANN index over embeddings; relevance: embeddings power OpenClaw's vector memory search.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a provider; relevance: this card IS a provider plugin (embedding provider).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Voyage AI is an external embedding provider.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: embeddings drive the retrieval step over memory.
- [Similarity Search](../../term_dictionary/term_similarity_search.md) — nearest-neighbor search over vectors; relevance: what Voyage embeddings enable in memory.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — retrieving relevant items from a corpus; relevance: the memory-search task embeddings serve.
- [Dense Retrieval](../../term_dictionary/term_dense_retrieval.md) — embedding-based retrieval; relevance: the retrieval mode Voyage embeddings provide.
- [Word Embedding](../../term_dictionary/term_word_embedding.md) — foundational text-embedding concept; relevance: the lineage of the embedding vectors Voyage produces.

**Docs**
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — the memory provider plugin surface (Hermes); relevance: the exact `memoryEmbeddingProviders` analog this card registers.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory provider catalog; relevance: where an embedding/memory provider like Voyage registers.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — persistent agent memory; relevance: the memory subsystem Voyage embeddings index.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — session search/storage; relevance: embedding-backed search over stored sessions.
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho memory provider; relevance: peer memory-provider plugin implementation.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — the agent memories API (Band); relevance: cross-agent memory-store analog backed by embeddings.
- [aws_bedrock/bedrock_kb_supported_models_regions](../aws_bedrock/bedrock_kb_supported_models_regions.md) — Bedrock knowledge-base embedding models/regions; relevance: external managed-embedding-provider analog to Voyage.
- [aws_bedrock/bedrock_overview](../aws_bedrock/bedrock_overview.md) — Bedrock overview; relevance: managed-model-provider context for an embedding provider.
- [oc_concepts_memory](oc_concepts_memory.md) (planned, this series) — the deeper OpenClaw memory/embedding concept doc (co03/co04); relevance: the memory subsystem this embedding provider extends.
- [oc_plugins_reference_venice](oc_plugins_reference_venice.md) (planned, this series) — peer bundled provider-plugin card; relevance: same provider-plugin descriptor pattern.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — the OpenClaw memory package; relevance: the subsystem the voyage embedding provider feeds.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM/embedding providers extensions; relevance: source home of the voyage provider plugin.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extensions package; relevance: umbrella home for bundled plugins.

**Snippets**
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — memory embedding input prep; relevance: the inputs a voyage embedding provider consumes.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host-side embedding generation; relevance: where the embedding-provider contract is invoked.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory engine; relevance: the engine embeddings index into.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: the runtime the embedding provider plugs into.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — memory schema; relevance: how embedded memory records are stored.
- [snippet_openclaw_memory_host_internal_chunking](../../code_snippets/snippet_openclaw_memory_host_internal_chunking.md) — chunking before embedding; relevance: the pre-embedding step feeding the provider.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent memory search; relevance: the query side using Voyage embeddings.
- [snippet_otf_embedding_vector_text](../../code_snippets/snippet_otf_embedding_vector_text.md) — text-to-embedding vector pipeline; relevance: the embedding-vector pipeline shape Voyage feeds.

## Undigested Terms Plan (Step 4e)

pl21 creates **0 new `term_dictionary` notes** (per master design decision: OpenClaw vocabulary is digested as
`oc_*` doc notes; the only `term_dictionary` interaction is LINKING existing terms).

| Term (appears in source) | Disposition |
|---|---|
| OpenClaw (product) | Link existing `term_openclaw`. |
| Twitch / chat moderation | Subject of note 1 (`oc_plugins_reference_twitch`); link `term_chatbot`, `term_content_moderation`. Not a new term. |
| Venice (provider) | Provider name documented as note 2 (`oc_plugins_reference_venice`); link `term_llm` / `term_third_party_genai_services`. Provider names are NOT promoted to term notes (master precedent). |
| Vercel AI Gateway | Note 3; link `term_api_gateway`, `term_reverse_proxy`. Not a new term. |
| vLLM | Note 4; link existing `term_vllm`. Not a new term (already in DB). |
| voice-call / telephony (Twilio/Telnyx/Plivo) | Note 5; link existing `term_voice_call`, `term_voip`. Provider/vendor names not promoted. |
| Volcengine / Volcengine Plan / speech providers | Note 6; link `term_text_to_speech`, `term_speech_to_text`. Provider names not promoted. |
| Voyage / memory embedding provider | Note 7; link existing `term_embedding`, `term_vector_database`. Vendor name not promoted. |
| Plugin / Distribution / Surface / contract (channels/providers/tools/speechProviders/memoryEmbeddingProviders) | OpenClaw plugin-system vocabulary → digested as the `oc_*` cards themselves; link existing `term_provider_plugin`, `term_plugin_manifest`, `term_plugin_sdk`, `term_mcp`. Cross-cutting plugin-architecture terms are owned by pl01–pl04 (plugins architecture/manifest/SDK), not duplicated here. |
| ClawHub / npm (install routes) | Install-route vocabulary; link existing `term_npm`. ClawHub is owned by the ClawHub sub-plans (cw01–cw03); not a new term here. |

**New-term candidates:** none. No genuinely reusable cross-cutting term lacks an existing note. If augment's
Step 2d re-scan surfaces one (not expected), it would be captured via `/tessellum-capture-term-note` + added to
the agentic/LLM `acronym_glossary_*.md` per master W5 — but the expectation is **0**.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl21 authors zero `term_dictionary` notes; it only links existing terms. (Multi-source
research mandate / glossary-update requirement inherited from master would apply only if a new term were
proposed — none is.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). All gates must pass before commit.

| Gate | Name | Check |
|------|------|-------|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` — YAML field order, required `## Overview`/`## Related Notes`, bold footer, indexed `[text](path.md)` links. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/plugins/reference/<page>.md` — package name, install route, surface line, related-docs pointer reproduced faithfully; no invented config. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks; one `building_block` per note; every source H2 mapped (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevancy-selected `term_dictionary` terms + repo_openclaw* + sibling `oc_*` + `entry_openclaw_docs`, each an indexed link with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` — 0 broken relative paths after reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island) — satisfied via `entry_openclaw_docs.md` + the candidate inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
OC="the vault/$GATE_DIR"
NOTES="oc_plugins_reference_twitch oc_plugins_reference_venice oc_plugins_reference_vercel_ai_gateway oc_plugins_reference_vllm oc_plugins_reference_voice_call oc_plugins_reference_volcengine oc_plugins_reference_voyage"
for n in ${=NOTES}; do
  f="$OC/$n.md"
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # at least one sibling oc_ cross-link (SIBLING_PREFIX)
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING $SIBLING_PREFIX LINK in $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$OC"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_twitch | concept | 220 | 0 | ✅ |
| 2 | oc_plugins_reference_venice | concept | 200 | 0 | ✅ |
| 3 | oc_plugins_reference_vercel_ai_gateway | concept | 210 | 0 | ✅ |
| 4 | oc_plugins_reference_vllm | concept | 200 | 0 | ✅ |
| 5 | oc_plugins_reference_voice_call | concept | 220 | 0 | ✅ |
| 6 | oc_plugins_reference_volcengine | concept | 220 | 0 | ✅ |
| 7 | oc_plugins_reference_voyage | concept | 180 | 0 | ✅ |

No note approaches the caps (all ≤220 w, 0 code). These are intentionally compact descriptor cards; the risk is
under-padding, not over-compression — the Related Notes / References cross-links (to the deeper channel/provider
/tool docs) carry the discoverability load, not inflated body text.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step, W1) under the **Plugins →
Reference** cluster (pl21 segment, `twitch`…`voyage`). Each note receives its entry-point back-link at
finalization. No separate entry point for this sub-plan (master `entry_openclaw_docs.md` is the single hub for
all 105 sub-plans).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution; each new note needs ≥1):

- `entry_openclaw_docs.md` (planned, master pre-step) → all 7 notes (primary anti-island inbound).
- `areas/code_repos/repo_openclaw_channels.md` → note 1 (twitch). [verified]
- `areas/code_repos/repo_openclaw_extensions_llm_providers.md` → notes 2, 3, 4, 6 (LLM providers). [verified]
- `areas/code_repos/repo_openclaw_channels_voice_phone.md` → note 5 (voice-call). [verified]
- `areas/code_repos/repo_openclaw_extensions_voice_speech.md` → notes 5, 6 (speech). [verified]
- `areas/code_repos/repo_openclaw_memory.md` → note 7 (voyage embeddings). [verified]
- `resources/term_dictionary/term_vllm.md` → note 4. [verified]
- `resources/term_dictionary/term_voice_call.md` → note 5. [verified]
- `resources/term_dictionary/term_embedding.md` → note 7. [verified]
- `resources/term_dictionary/term_openclaw.md` → any/all (umbrella). [verified]

## Pacing Rules (inherited from master)

Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script; single phase (7 notes) so one
wave. Reindex incrementally after the wave; verify `note_links` + 0 broken links before commit;
`git pull --rebase --autostash` first; commit+push per wave; **no Claude co-author trailer**. Re-read each
source page at execute (Step 1 of execute); reproduce package/surface lines verbatim; one BB per note.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of pl21 (7 plugin-reference descriptor cards, `twitch`…`voyage`). Re-read all 7 source
pages under `inbox/openclaw_docs/plugins/reference/` (twitch 425B, venice 408B, vercel-ai-gateway 507B, vllm
390B, voice-call 456B, volcengine 523B, voyage 362B); confirmed the plan's measured stats (45–62 words, 0 code,
2–3 H2 each) and grounding (package name, install route, surface line, Related-docs pointer all reproduced
faithfully). No splits, no omissions, no over-compression — all 7 are uniform single-BB cards far below caps.

**What was LOCKED:** replaced `## Candidate Cross-References` with `## Per-Note Related Notes Mapping (LOCKED —
xref-augment 2026-06-21)` at the raised floors **≥8 terms · ≥10 snippets · ≥10 docs** per note, every link
`term_pra_product_review_abuse`, `term_self_serving_bias`, `term_stylometry`, `term_merchant_risk`,

**Per-note locked counts (terms / snippets / docs-existing+planned / repos):**

| Note | Terms | Snippets | Docs (existing + planned = total) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_twitch | 12 | 12 | 9 + 2 = 11 | 3 | ✅ |
| oc_plugins_reference_venice | 10 | 12 | 9 + 2 = 11 | 3 | ✅ |
| oc_plugins_reference_vercel_ai_gateway | 11 | 12 | 9 + 2 = 11 | 3 | ✅ |
| oc_plugins_reference_vllm | 11 | 12 | 10 + 2 = 12 | 3 | ✅ |
| oc_plugins_reference_voice_call | 12 | 12 | 9 + 3 = 12 | 3 | ✅ |
| oc_plugins_reference_volcengine | 11 | 12 | 9 + 2 = 11 | 3 | ✅ |
| oc_plugins_reference_voyage | 10 | 12 | 9 + 2 = 11 | 3 | ✅ |

**New-term candidates:** **none.** Step 2d re-scan of all 7 pages surfaced no genuinely reusable cross-cutting
term lacking an existing note. Every vocabulary item is either (a) the subject of the `oc_*` card itself
(plugin-packaging view), (b) owned by another sub-plan (Twitch channel → ch05, providers → pr08/pr09, voice-call
→ pl25, embeddings/memory → co03/co04, plugin architecture → pl01–pl04, ClawHub → cw01–cw03), or (c) an existing
`term_vector_database`, `term_provider_plugin`, `term_third_party_genai_services`, `term_api_gateway`,
(Venice, Volcengine, Voyage, Twilio/Telnyx/Plivo) are NOT promoted to term notes (master precedent). Best-fit
glossary if a candidate ever surfaced: `acronym_glossary_agentic_llm_*.md` (per master W5) — **0 expected, 0
found.** `term_voyager` was evaluated for note 7 and **dropped** (it is the unrelated Voyager LLM-agent paper, not
the Voyage embedding service — a name collision, not a relevance match), per dedup/collision discipline.

**Term-Note Authoring Requirements:** N/A — pl21 authors 0 new term_dictionary notes; it only LINKS existing
terms (master design decision). The multi-source-research / glossary-update mandate would apply only to a new
term; none is proposed.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 mandatory checkpoints. Source pages spot-checked (CP7) by direct re-read of all 7
mirror files.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7/G8 Discoverability; single execution phase (7 notes) so 1 gate table for 1 phase. |
| CP3 | Entry point update specified (inherited) | **PASS** | `## Entry Point Decision` — contributes 7 rows to `entry_openclaw_docs.md` (CREATED as master pre-step W1, >30-note hub for all 105 sub-plans); confirmed `entry_openclaw_docs.md` does NOT yet exist (planned W1) so correctly inherited, not duplicated. |
| CP4 | Plan size (≤30 or split) | **PASS** | 7 planned notes ≤ 30; sub-plan of a master+sub-plan structure. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (same source type); YAML field order + `## Overview`/`## Related Notes`/`## References`/bold footer match existing `documentation/openclaw/` siblings (e.g. cc_/pi_). Forbidden-field list inherited. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment` — all 7 notes ≤220 words, 0 code; none borderline; risk is under-padding (mitigated by the rich Related Notes mapping), not over-compression. No splits needed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 mirror pages re-read 2026-06-21; measured 45–62 words/0 code each, matching the plan's Source table exactly (ratio ≈1.0, well within ±30%). No under-estimation. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present with per-row Disposition (all "link existing" / "owned by sub-plan X"); 0 new terms; `## Term-Note Authoring Requirements` present as N/A (0 new terms) with the inherited-mandate note. must-language used. |
| CP8f | Term-slug + all-notes dedup/collision audit | **PASS** | Collision audit run across `term_dictionary/` AND `documentation/`: all 7 `oc_*` slugs are unique (no existing note); `term_voyager` collision caught and dropped from note 7 (unrelated Voyager agent, not Voyage embeddings); provider/vendor names not promoted (no new-slug duplicates of existing terms). No too-general slugs (every slug is `oc_plugins_reference_<plugin>`, maximally specific). |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps ≥1 outside-folder inbound for every note (entry_openclaw_docs → all 7; repo_openclaw_channels → twitch; repo_openclaw_extensions_llm_providers → venice/vercel/vllm/volcengine; repo_openclaw_channels_voice_phone + _extensions_voice_speech → voice-call/volcengine; repo_openclaw_memory → voyage; term_vllm/term_voice_call/term_embedding/term_openclaw inbound); G7/G8 in the gate table; inlinks specified as an execution-phase task, not "recommended". |

**RESULT: 9/9 pass → READY FOR EXECUTION.** All 7 notes meet the raised floors (≥8 terms · ≥10 snippets · ≥10
docs); 0 ghost references; format/entry-point/discoverability inherited from master are present and correct.
Status advanced `pending → ready`.
