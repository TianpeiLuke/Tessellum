---
title: Sub-Plan pr01 — OpenClaw Docs: Providers (alibaba, anthropic, arcee, azure-speech, bedrock, bedrock-mantle, cerebras)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/alibaba", "providers/anthropic", "providers/arcee", "providers/azure-speech", "providers/bedrock", "providers/bedrock-mantle", "providers/cerebras"]
---

# Sub-Plan pr01: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_*`), format (YAML field order + `## Overview`/`## Related Notes`/`## References` body + density caps), dedup (3-way across term_dictionary AND documentation/ AND `repo_openclaw*`), the 9-GATE, cross-references, and entry-point wiring (W1–W5) are ALL inherited from the master and applied here.

## Scope

The first 7 provider-setup pages (alphabetical block A–C): how to authenticate and configure individual
inference / media providers behind OpenClaw's model layer — **alibaba** (Wan video generation via DashScope),
**anthropic** (Claude via API key or Claude CLI backend), **arcee** (Trinity MoE, OpenAI-compatible),
**azure-speech** (Azure AI Speech text-to-speech), **bedrock** (Amazon Bedrock Converse, AWS credential chain),
**bedrock-mantle** (Bedrock Mantle OpenAI-compatible OSS endpoint), and **cerebras** (high-speed
OpenAI-compatible inference). **Priority P2 (Phase B)** per master — the provider/integration layer that the
concepts (`concepts/model-providers`, `concepts/models`) and gateway config docs reference. The code-side
counterparts (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`,
`repo_openclaw_agents`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 6,772 measured words. **Planned: 7 notes** (1 per reference page; no splits).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| alibaba | providers/alibaba | 764 | 0 | 5 | 0 | procedure |
| anthropic | providers/anthropic | 1,553 | 2 | 6 | 0 | procedure |
| arcee | providers/arcee | 557 | 1 | 6 | 0 | procedure |
| azure-speech | providers/azure-speech | 544 | 0 | 4 | 0 | procedure |
| bedrock | providers/bedrock | 1,920 | 1 | 5 | 0 | procedure |
| bedrock-mantle | providers/bedrock-mantle | 868 | 2 | 5 | 1 | procedure |
| cerebras | providers/cerebras | 566 | 6 | 6 | 0 | procedure |

Totals: 6,772 words, 12 code blocks, 37 H2 + 1 H3. Code-fence counts derive from `(grep -c '^```')/2`;
several pages additionally use MDX `<Steps>`/`<CodeGroup>`/`<Tabs>`/`<AccordionGroup>` wrappers around the
fenced blocks (the bundled config snippets are the load-bearing content to reproduce selectively).

## Content Strategy

- **Prioritize**: the auth + model-resolution mechanics of each provider — the env-var/onboarding-flag tables,
  the `models.providers.<id>` config blocks, and the discovery/auto-enable rules (these are what every model
  call depends on). For **anthropic** and **bedrock** (the two largest pages, 1,553w / 1,920w) prioritize the
  two auth routes (API key vs Claude CLI; access-keys/env-vars vs EC2/IMDS instance roles) and the
  Bedrock-specific knobs (discovery, inference profiles, service tier, guardrails, embeddings).
- **Split**: NONE. Every page is single-building-block (a provider-setup *procedure*) AND under the 2,500-word
  cap, so each page maps to exactly one `oc_provider_*` note (see Split Decisions). The two largest pages
  (anthropic 1,553w, bedrock 1,920w) stay one note each — well within caps; their accordions/tabs are flattened
  into the note's H2/H3 body rather than promoted to separate notes (a per-page provider note is the matching
  format precedent in `cc_*`/`pi_*`).
- **Link-out (do not duplicate)**: shared concepts `concepts/model-providers`, `concepts/models`, prompt
  caching mechanics (`reference/prompt-caching`), the video tool (`tools/video-generation`), the TTS tool
  (`tools/tts`), CLI backends (`gateway/cli-backends`), gateway auth (`gateway/authentication`), memory search
  (`concepts/memory-search`), and sibling providers (`providers/qwen`, `providers/openrouter`,
  `providers/openai`) are cross-linked, not redefined. Term vocabulary links existing `term_*` notes
  (`term_bedrock`, `term_claude`, `term_llm`, `term_prompt_caching`, `term_converse_api`, …) — never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_provider_alibaba.md` | procedure | alibaba.md: header table, Getting started, Built-in Wan models, Capabilities and limits, Advanced configuration (base URL, auth env priority, Qwen relationship) | 480 | Configuring the bundled Alibaba Model Studio (DashScope) Wan video-generation provider: API-key resolution (`MODELSTUDIO_API_KEY`→`DASHSCOPE_API_KEY`→`QWEN_API_KEY`), default `alibaba/wan2.6-t2v`, the five built-in Wan models, per-mode video caps, and base-URL/Qwen-overlap notes. |
| 2 | `oc_provider_anthropic.md` | procedure | anthropic.md: header, Getting started (API key / Claude CLI tabs), Thinking defaults, Prompt caching, Advanced configuration (fast mode, media, 1M context), Troubleshooting | 720 | Using Anthropic Claude in OpenClaw via API key vs Claude CLI backend: onboarding, `claude -p` billing caveats, per-model thinking defaults, prompt-cache retention values, fast mode, image/PDF media understanding, 1M context, and auth troubleshooting. |
| 3 | `oc_provider_arcee.md` | procedure | arcee.md: header, Install plugin, Getting started (Direct / OpenRouter tabs), Non-interactive setup, Built-in catalog, Supported features, Related accordions | 460 | Setting up the Arcee AI provider (Trinity MoE models, OpenAI-compatible): plugin install, direct (`ARCEEAI_API_KEY`) vs OpenRouter (`OPENROUTER_API_KEY`) auth, non-interactive onboarding, the static Trinity catalog, and supported features (streaming, tools, structured output, thinking). |
| 4 | `oc_provider_azure_speech.md` | procedure | azure-speech.md: header table, Getting started, Configuration options, Notes (auth, voice names, audio outputs, alias) | 440 | Configuring Azure AI Speech as OpenClaw's text-to-speech provider: `AZURE_SPEECH_KEY`+`AZURE_SPEECH_REGION` auth, `messages.tts` selection, the per-option config table, default voice/output formats (MP3/Ogg-Opus/mulaw), and the `azure-speech` vs `azure` alias note. |
| 5 | `oc_provider_bedrock.md` | procedure | bedrock.md: header, Getting started (access-keys / EC2-IMDS tabs), Automatic model discovery, Quick setup (AWS path), Advanced configuration (inference profiles, service tier, Opus 4.7 temperature, Fable 5, guardrails, embeddings, caveats) | 760 | Using Amazon Bedrock (Converse streaming) with OpenClaw via the AWS SDK default credential chain: access-key/env-var vs EC2 instance-role auth, IAM permissions, automatic model + inference-profile discovery, the IAM quick-setup walkthrough, service tiers, guardrails, and Bedrock embeddings for memory search. |
| 6 | `oc_provider_bedrock_mantle.md` | procedure | bedrock-mantle.md: header, Getting started (explicit bearer / IAM tabs), Automatic model discovery, Supported regions, Manual configuration, Advanced configuration (reasoning, unavailability, Anthropic Messages route, relationship to Bedrock) | 560 | Configuring the bundled Amazon Bedrock Mantle provider (OpenAI-compatible `/v1` endpoint for GPT-OSS/Qwen/Kimi/GLM): explicit `AWS_BEARER_TOKEN_BEDROCK` vs IAM-minted bearer-token auth, model discovery, supported regions, manual config, the Anthropic Messages route, and its relationship to the native Bedrock provider. |
| 7 | `oc_provider_cerebras.md` | procedure | cerebras.md: header, Install plugin, Getting started, Non-interactive setup, Built-in catalog, Manual config, Related | 460 | Setting up the Cerebras provider (high-speed OpenAI-compatible inference): plugin install, `CEREBRAS_API_KEY` onboarding/env auth, the static four-model catalog (128k context / 8,192 max-output), preview/deprecation caveats, and `mode: "merge"` manual config. |

## Section Coverage Map

```
alibaba.md
├── (header property table) ───────────────────────────── → note 1 (oc_provider_alibaba)
├── ## Getting started (set key / default video model / verify) → note 1
├── ## Built-in Wan models ────────────────────────────── → note 1
├── ## Capabilities and limits ────────────────────────── → note 1
├── ## Advanced configuration (base URL / auth env priority / Qwen relationship) → note 1
└── ## Related (links → /tools/video-generation, /providers/qwen, config-agents, faq-models) → Related Notes / References
anthropic.md
├── (header + billing Warning) ────────────────────────── → note 2 (oc_provider_anthropic)
├── ## Getting started (API key tab / Claude CLI tab + billing & claude -p) → note 2
├── ## Thinking defaults (Fable 5 / Opus 4.8 / 4.6) ───── → note 2
├── ## Prompt caching (short/long/none + Bedrock Claude notes) → note 2
├── ## Advanced configuration (fast mode / media / 1M context / Opus 4.8 1M) → note 2
├── ## Troubleshooting (401 / no key / no profile / cooldown) → note 2
└── ## Related (model-providers, cli-backends, prompt-caching, authentication) → Related Notes / References
arcee.md
├── (header property table) ───────────────────────────── → note 3 (oc_provider_arcee)
├── ## Install plugin ─────────────────────────────────── → note 3
├── ## Getting started (Direct / OpenRouter tabs) ─────── → note 3
├── ## Non-interactive setup ──────────────────────────── → note 3
├── ## Built-in catalog ───────────────────────────────── → note 3
├── ## Supported features (+ env / OpenRouter routing accordions) → note 3
└── ## Related (openrouter, model-providers) ──────────── → Related Notes / References
azure-speech.md
├── (header property table) ───────────────────────────── → note 4 (oc_provider_azure_speech)
├── ## Getting started (create resource / select tts / send) → note 4
├── ## Configuration options ──────────────────────────── → note 4
├── ## Notes (auth / voice names / audio outputs / alias) → note 4
└── ## Related (tts, configuration, providers, troubleshooting) → Related Notes / References
bedrock.md
├── (header property table) ───────────────────────────── → note 5 (oc_provider_bedrock)
├── ## Getting started (access-keys/env-vars tab / EC2-IMDS tab) → note 5
├── ## Automatic model discovery (+ discovery config options accordion) → note 5
├── ## Quick setup (AWS path) ─────────────────────────── → note 5
├── ## Advanced configuration (inference profiles / service tier / Opus 4.7 temp / Fable 5 / guardrails / embeddings / caveats) → note 5
└── ## Related (model-providers, memory-search, memory-config, troubleshooting) → Related Notes / References
bedrock-mantle.md
├── (header property table) ───────────────────────────── → note 6 (oc_provider_bedrock_mantle)
├── ## Getting started (explicit bearer tab / IAM tab) ── → note 6
├── ## Automatic model discovery ──────────────────────── → note 6
│   └── ### Supported regions ──────────────────────────── → note 6
├── ## Manual configuration ───────────────────────────── → note 6
├── ## Advanced configuration (reasoning / unavailability / Anthropic Messages route / relationship to Bedrock) → note 6
└── ## Related (bedrock, model-providers, authentication, troubleshooting) → Related Notes / References
cerebras.md
├── (header property table) ───────────────────────────── → note 7 (oc_provider_cerebras)
├── ## Install plugin ─────────────────────────────────── → note 7
├── ## Getting started (key / onboarding CodeGroup / verify) → note 7
├── ## Non-interactive setup ──────────────────────────── → note 7
├── ## Built-in catalog (+ preview/deprecation Warning) ── → note 7
├── ## Manual config (mode: merge) ────────────────────── → note 7
└── ## Related (model-providers, thinking, config-agents, faq-models) → Related Notes / References
```
No orphaned sections. Each page's `## Related` card group becomes that note's `## Related Notes` (vault links)
plus `## References` (external URLs). Cross-cutting targets (model-providers, prompt-caching, video/tts tools,
cli-backends, gateway auth, memory-search, sibling providers) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are single-building-block provider-setup *procedures* and each is under the 2,500-word cap (max = bedrock 1,920w). Per master's "most reference pages = 1 note" rule, each page → exactly one `oc_provider_*` note. The two largest (anthropic 1,553w, bedrock 1,920w) flatten their `<Tabs>`/`<AccordionGroup>` sub-sections into in-note H2/H3 rather than promoting them to separate notes — keeping the provider's setup self-contained, matching the per-provider `cc_*`/`pi_*` precedent. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (6,772 measured words, 12 fenced code blocks). New `oc_*` notes: **7**. New
  `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (all provider-setup how-tos). No concept/model/argument notes in this batch.
- Est. digest words ≈ **3,880** (avg ~554/note; range 440–760). Source fences distribute across the notes;
  each note kept ≤6 code blocks (config snippets reproduced selectively/verbatim per master density caps:
  ≤400 lines, ≤2,500 words, ≤6 code blocks, one building_block).
- Master estimated 11 notes for pr01; **measured reality = 7** (these are single-BB sub-cap reference pages,
  so the 1.5×-pages heuristic over-counts). Final count locks at augment.
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** every note maps **≥8 relevance-selected
  `aws_bedrock*` corpora), the remainder sibling `oc_provider_*` (planned, this series). See
  **`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`** for the per-note locked lists with
  per-link relevance statements.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

the 10-doc floor. Relative paths are from `resources/documentation/openclaw/oc_provider_*.md`
(`../../term_dictionary/`, `../../code_snippets/`, `../<folder>/`, `../../../areas/code_repos/`, sibling `oc_*`).
Ghost-flagged MISSING candidates (`term_extended_thinking`, `term_amazon_titan`, `term_service_tier`,
`term_tts`, `term_video_generation`, `term_streaming`, `term_embeddings`, `term_cohere`, `term_speech_synthesis`,

### oc_provider_alibaba (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this provider plugs into; relevance: the page documents OpenClaw's bundled `alibaba` plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw's pluggable model-provider abstraction; relevance: `alibaba` is a bundled, `enabledByDefault` provider plugin.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the static/discovered list of usable model refs; relevance: the page lists the five built-in Wan model refs.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI APIs; relevance: Wan runs on Alibaba Model Studio / DashScope, an external service.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — OpenClaw's stored credential/rotation unit; relevance: configured `auth.profiles` override env-var key resolution for the provider.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — base-URL indirection in front of an upstream API; relevance: `models.providers.alibaba.baseUrl` overrides the DashScope endpoint (intl vs China).
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative image/video model class; relevance: Wan text/image/reference-to-video generation is diffusion-based media synthesis.
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning text/image/video; relevance: Wan modes consume text/image/video inputs and emit video.
- [LLM](../../term_dictionary/term_llm.md) — large language / generative model umbrella; relevance: the Wan provider sits in OpenClaw's generative-model layer alongside chat LLMs.

**Docs**
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — Hermes video-generation provider-plugin doc; relevance: closest sibling-ecosystem analog of the Wan video provider plugin.
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — Hermes image-generation provider doc; relevance: parallel media-generation provider config (model ref + provider selection).
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — Hermes media tool reference; relevance: the video tool params Wan obeys mirror this media-tool surface.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud-provider setup doc; relevance: same env-var/API-key resolution pattern for a hosted provider.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — Pi custom-provider registration; relevance: how a provider plugin registers models/base-URL, paralleling the Alibaba block.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes model-provider-plugin authoring doc; relevance: the bundled-vs-installed plugin model behind `alibaba`.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model-selection doc; relevance: cross-ecosystem `provider/model` ref selection mirrors `videoGenerationModel.primary`.
- [oc_provider_anthropic](oc_provider_anthropic.md) — sibling Anthropic provider note (planned, this series); relevance: same provider-setup format and onboarding flags.
- [oc_provider_cerebras](oc_provider_cerebras.md) — sibling Cerebras provider note (planned, this series); relevance: another bundled/plugin provider with env-var auth.
- [oc_provider_azure_speech](oc_provider_azure_speech.md) — sibling media (TTS) provider note (planned, this series); relevance: the other non-chat media provider in pr01.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — OpenClaw LLM/media provider extension package; relevance: hosts the `alibaba` provider implementation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents/model-catalog host; relevance: resolves `videoGenerationModel` defaults and the model catalog.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw apps surface; relevance: media outputs are delivered through app/channel surfaces.

**Snippets**
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool code; relevance: the video tool params (duration, size, audio) Wan honors.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video provider dispatch; relevance: how a video request routes to a provider like Wan.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool code; relevance: sibling media-tool surface (reference-to-video uses image inputs).
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image provider dispatch; relevance: parallel media-provider dispatch path.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — OpenClaw model-catalog code; relevance: how the five built-in Wan model refs are registered.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the bundled-plugin registration mechanism behind `alibaba`.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry CLI; relevance: how `models list --provider alibaba` enumerates a provider's models.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential-source resolution; relevance: first-match env-var priority (`MODELSTUDIO_API_KEY`→`DASHSCOPE_API_KEY`→`QWEN_API_KEY`).
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — per-provider auth resolution; relevance: onboarding `--auth-choice` stores the key against the provider.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — media routing code; relevance: shared media-output routing pattern for generated assets.

### oc_provider_anthropic (10t · 11s · 10d)

**Terms**
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the page is the Anthropic/Claude provider setup.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's coding-agent CLI; relevance: the Claude CLI backend reuses an existing Claude Code login (`claude -p`).
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reuse of cached prompt prefixes; relevance: the page's short/long/none `cacheRetention` table.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — the attention-cache prompt caching exploits; relevance: explains the mechanism behind cache retention durations.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — step-by-step reasoning; relevance: substitute for the MISSING `term_extended_thinking`; covers Fable 5 adaptive thinking + `/think` effort levels.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — subscription/OAuth credential; relevance: the troubleshooting "token suddenly invalid / cooldown" + subscription-vs-API-key auth.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: API-key vs Claude CLI auth routes and per-agent key inheritance.
- [Context Window](../../term_dictionary/term_context_window.md) — model input token capacity; relevance: the 1M-context-window accordion (Opus 4.8/4.7/4.6, Sonnet 4.6).
- [Service Tier](../../term_dictionary/term_bedrock.md) — no `term_service_tier` exists; relevance: substitute (Bedrock note) covers the `/fast` → `service_tier: auto/standard_only` mapping.
- [LLM](../../term_dictionary/term_llm.md) — generative model umbrella; relevance: Claude is the flagship LLM in OpenClaw's model layer.

**Docs**
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth doc; relevance: API-key vs subscription/CLI auth, the same routes this page exposes.
- [cc_prompt_caching_mechanism](../claude_code/cc_prompt_caching_mechanism.md) — Claude Code prompt-caching doc; relevance: how short/long cache retention works under the hood.
- [cc_cache_lifetime_and_scope](../claude_code/cc_cache_lifetime_and_scope.md) — cache lifetime/scope doc; relevance: 5-minute vs 1-hour cache durations match the `cacheRetention` table.
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — thinking/effort doc; relevance: the `/think high|xhigh|max` effort mapping and Fable 5 adaptive thinking.
- [cc_extended_context_1m](../claude_code/cc_extended_context_1m.md) — 1M-context doc; relevance: directly parallels the 1M context-window accordion + retired beta header.
- [cc_fast_mode](../claude_code/cc_fast_mode.md) — `/fast` mode doc; relevance: the `/fast on/off` → `service_tier` mapping accordion.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider-auth doc; relevance: cross-ecosystem provider auth/credential reuse pattern.
- [oc_provider_bedrock](oc_provider_bedrock.md) — sibling Bedrock provider note (planned, this series); relevance: Claude-on-Bedrock cache pass-through is cross-referenced from this page.
- [oc_provider_bedrock_mantle](oc_provider_bedrock_mantle.md) — sibling Mantle provider note (planned, this series); relevance: Anthropic Messages route exposes Claude via Mantle.
- [oc_provider_alibaba](oc_provider_alibaba.md) — sibling provider note (planned, this series); relevance: shares the onboarding `--auth-choice`/env-var setup format.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension package; relevance: hosts the bundled Anthropic provider.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents/model defaults host; relevance: per-agent model + cache override merge order described on the page.

**Snippets**
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw Anthropic provider code; relevance: the exact provider this page documents.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt-caching code; relevance: implements the cache-retention behavior in the table.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — system-prompt cache sectioning; relevance: where cache breakpoints are inserted for Claude.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — Anthropic adapter client; relevance: how the Anthropic API client is constructed and authed.
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — Anthropic adapter endpoints; relevance: `api.anthropic.com` direct vs proxy routing (the `/fast` service-tier injection).
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — request kwargs builder; relevance: how `thinking`/`cacheRetention`/`serviceTier` params are assembled.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential sources; relevance: `ANTHROPIC_API_KEY` resolution and per-agent key handling.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: onboarding choice between API key and CLI login.
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — auth provider state; relevance: `models status` profile/cooldown surfacing in troubleshooting.
- [snippet_hermes_agent_core_error_classifier_taxonomy](../../code_snippets/snippet_hermes_agent_core_error_classifier_taxonomy.md) — error taxonomy; relevance: 401/no-key/cooldown error classes in the troubleshooting accordions.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — API-connectivity doctor; relevance: verifying Claude provider reachability after onboarding.

**Sibling oc_*: oc_provider_bedrock, oc_provider_bedrock_mantle (planned, this series) — Claude on Bedrock / Mantle Messages route.**

### oc_provider_arcee (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway hosting the provider; relevance: the page documents OpenClaw's Arcee provider plugin.
- [Mixture of Experts](../../term_dictionary/term_mixture_of_experts.md) — sparse expert routing architecture; relevance: Arcee's Trinity family are MoE models (400B params, 13B active).
- [MoE](../../term_dictionary/term_moe.md) — the MoE acronym/term note; relevance: directly names the Trinity model class.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw provider abstraction; relevance: Arcee is installed as `@openclaw/arcee-provider`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-use capability; relevance: the supported-features table lists tool use / function calling.
- [Structured Output](../../term_dictionary/term_structured_output.md) — JSON-mode/JSON-schema output; relevance: the supported-features table lists structured output.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API surface; relevance: Arcee is accessed over an OpenAI-compatible API.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — static model list; relevance: the page's static Trinity catalog (large-thinking/large-preview/mini).

**Docs**
- [cc_model_selection](../claude_code/cc_model_selection.md) — model-selection doc; relevance: choosing `arcee/trinity-*` as `model.primary`.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: same direct-vs-aggregator (OpenRouter) auth pattern.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the installed-plugin model behind Arcee.
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — auxiliary provider config; relevance: env-var/daemon-env note for `ARCEEAI_API_KEY`.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — fallback/failover providers; relevance: routing Arcee directly vs via OpenRouter.
- [pi_custom_models](../pi/pi_custom_models.md) — custom-model registration; relevance: registering an OpenAI-compatible provider's catalog.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — model overrides/compat; relevance: overriding model metadata for a static catalog.
- [oc_provider_cerebras](oc_provider_cerebras.md) — sibling provider note (planned, this series); relevance: the closest parallel — plugin-install + OpenAI-compatible + static catalog.
- [oc_provider_anthropic](oc_provider_anthropic.md) — sibling provider note (planned, this series); relevance: shared onboarding `--auth-choice` setup.
- [oc_provider_bedrock_mantle](oc_provider_bedrock_mantle.md) — sibling provider note (planned, this series); relevance: another OpenAI-compatible (`openai-completions`) provider.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension package; relevance: where the Arcee provider plugin lives.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: OpenAI-compatible adapter pattern for a third-party provider.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI-compatible provider; relevance: the API surface class Arcee uses.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: the via-OpenRouter auth route for Arcee.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider plugin; relevance: `OPENROUTER_API_KEY` routing of `arcee/*` refs.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog code; relevance: how the static Trinity catalog is registered.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry CLI; relevance: `models list` over an installed provider.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base class; relevance: the abstract provider interface Arcee implements.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — API-mode resolution; relevance: resolving the `openai-completions` API mode for Arcee.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: how `@openclaw/arcee-provider` registers on install.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — auth resolution; relevance: direct (`ARCEEAI_API_KEY`) vs OpenRouter auth-choice.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model normalization; relevance: normalizing `arcee/*` refs across direct and OpenRouter routes.

### oc_provider_azure_speech (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway hosting TTS; relevance: the page documents OpenClaw's Azure Speech TTS provider.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis from text; relevance: Azure Speech synthesizes outbound reply audio (the core of this page).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription (contrast); relevance: distinguishes this TTS-only provider from STT providers.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — conversational voice interaction; relevance: TTS output feeds voice-note/voice-mode replies.
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony channel; relevance: the page calls out 8 kHz mulaw output for Voice Call telephony.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw provider abstraction; relevance: Azure Speech is the bundled TTS provider plugin.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored credential unit; relevance: `AZURE_SPEECH_KEY`/region resolution with config-key fallbacks.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — base-URL/endpoint override; relevance: optional `endpoint`/`baseUrl` override of the region-derived TTS endpoint.

**Docs**
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS providers doc; relevance: directly parallel TTS provider config (voice, output format, `messages.tts`).
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/messaging settings; relevance: how synthesized audio is attached to outbound replies (MP3 vs voice-note).
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI; relevance: enabling voice output that consumes a TTS provider.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice-mode usage guide; relevance: end-to-end voice reply flow that Azure Speech serves.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT/transcription doc; relevance: the inbound counterpart (contrast) to outbound TTS.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation doc; relevance: cross-ecosystem voice I/O config reference.
- [oc_provider_alibaba](oc_provider_alibaba.md) — sibling media provider note (planned, this series); relevance: the other non-chat media (video) provider in pr01.
- [oc_provider_anthropic](oc_provider_anthropic.md) — sibling provider note (planned, this series); relevance: shared provider-setup format/onboarding.
- [oc_provider_cerebras](oc_provider_cerebras.md) — sibling provider note (planned, this series); relevance: shared env-var-driven provider auth pattern.
- [oc_provider_bedrock](oc_provider_bedrock.md) — sibling provider note (planned, this series); relevance: Bedrock can also serve embeddings/media — same provider config model.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — OpenClaw voice/speech extension package; relevance: hosts the Azure Speech TTS provider implementation.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel package; relevance: consumes 8 kHz mulaw TTS output for telephony.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents/messages host; relevance: `messages.tts` selection is resolved here.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider code; relevance: the closest sibling TTS provider implementation (voice + output format).
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — MLX local TTS code; relevance: another TTS provider in the same speech package.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing code; relevance: how `messages.tts.provider` selects Azure Speech.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT code; relevance: the inbound transcription counterpart (contrast).
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline code; relevance: the synthesis→delivery pipeline TTS output flows through.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: mulaw/telephony audio path that consumes synthesized audio.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call transcription stream; relevance: paired media stream (contrast) in the voice-call channel.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool code; relevance: voice-mode replies invoke a TTS provider like Azure Speech.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool code; relevance: the STT counterpart to TTS output.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: `AZURE_SPEECH_KEY`/region credential resolution with fallbacks.

### oc_provider_bedrock (12t · 12s · 11d)

**Terms**
- [Amazon Bedrock](../../term_dictionary/term_bedrock.md) — AWS managed foundation-model service; relevance: the page's subject (`amazon-bedrock` provider via Converse).
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock's unified chat API; relevance: the provider uses `bedrock-converse-stream`.
- [Inference Profile](../../term_dictionary/term_inference_profile.md) — Bedrock cross-region routing profile; relevance: discovery of regional/global inference profiles + capability inheritance.
- [Cross-Region Inference](../../term_dictionary/term_cross_region_inference.md) — multi-region request routing; relevance: regional `us.anthropic.*` profiles route cross-region automatically.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — default credential resolution order; relevance: Bedrock auth uses the AWS SDK default chain, not an API key.
- [IAM](../../term_dictionary/term_iam.md) — AWS access management; relevance: the quick-setup creates an IAM role + Bedrock invoke/list permissions.
- [SigV4](../../term_dictionary/term_sigv4.md) — AWS request signing; relevance: the signing mechanism behind SDK-chain Bedrock calls.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — Amazon's foundation models; relevance: substitute for MISSING `term_amazon_titan`; covers Amazon embed/foundation models in discovery + memory search.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Bedrock content-safety filters; relevance: the `guardrail` plugin-config accordion (`bedrock:ApplyGuardrail`).
- [Contextual Grounding](../../term_dictionary/term_contextual_grounding.md) — a Guardrails check type; relevance: named in the guardrails content-filter list.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cache-prefix reuse; relevance: Claude-on-Bedrock accepts `cacheRetention` pass-through.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models on Bedrock; relevance: the example config + Opus 4.7/Fable 5 Bedrock knobs.

**Docs**
- [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — Claude Code Bedrock setup; relevance: identical AWS credential/region setup for Bedrock model calls.
- [cc_amazon_bedrock_features](../claude_code/cc_amazon_bedrock_features.md) — Bedrock features doc; relevance: discovery, inference profiles, and Bedrock-specific knobs.
- [cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md) — Bedrock model config; relevance: the provider+model config block structure (model id, context, maxTokens).
- [bedrock_converse_api_overview](../aws_bedrock/bedrock_converse_api_overview.md) — AWS Converse API overview; relevance: authoritative reference for `bedrock-converse-stream`.
- [bedrock_converse_api_examples](../aws_bedrock/bedrock_converse_api_examples.md) — Converse API examples; relevance: request shape behind the OpenClaw Converse provider.
- [bedrock_inference_profiles](../aws_bedrock/bedrock_inference_profiles.md) — AWS inference-profiles doc; relevance: regional/global profile ids the page discovers.
- [bedrock_cross_region_overview](../aws_bedrock/bedrock_cross_region_overview.md) — cross-region inference doc; relevance: the cross-region Claude profile behavior.
- [bedrock_guardrails_overview](../aws_bedrock/bedrock_guardrails_overview.md) — Guardrails overview; relevance: the guardrail object + filter types in the accordion.
- [bedrock_inference_permissions](../aws_bedrock/bedrock_inference_permissions.md) — Bedrock IAM permissions; relevance: `bedrock:InvokeModel*`/`ListFoundationModels`/`ListInferenceProfiles` in the IAM block.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud-providers doc; relevance: cross-ecosystem AWS-credential-chain provider setup.
- [oc_provider_bedrock_mantle](oc_provider_bedrock_mantle.md) — sibling Mantle provider note (planned, this series); relevance: the OpenAI-compatible Bedrock surface, contrasted with native Converse.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension package; relevance: hosts the `amazon-bedrock` provider.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Hermes agent core; relevance: hosts the Bedrock adapter (credentials/discovery/streaming).
- [repo_pi_agent_harness_ai](../../../areas/code_repos/repo_pi_agent_harness_ai.md) — Pi AI/provider layer; relevance: cross-ecosystem Bedrock provider integration.

**Snippets**
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock provider plugin; relevance: the provider-plugin wiring this page configures.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — Bedrock adapter credentials; relevance: AWS SDK credential-chain resolution + env-marker precedence.
- [snippet_hermes_agent_core_bedrock_adapter_discovery](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_discovery.md) — Bedrock adapter discovery; relevance: `ListFoundationModels`/`ListInferenceProfiles` discovery + caching.
- [snippet_hermes_agent_core_bedrock_adapter_streaming](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_streaming.md) — Bedrock adapter streaming; relevance: the `bedrock-converse-stream` streaming path.
- [snippet_hermes_agent_core_bedrock_adapter_format](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_format.md) — Bedrock request formatting; relevance: how Converse request payloads (inferenceConfig) are built.
- [snippet_pq_patronus_flink_jobs_bedrock_invocation](../../code_snippets/snippet_pq_patronus_flink_jobs_bedrock_invocation.md) — Bedrock invocation in a Flink job; relevance: a production Bedrock invoke pattern using the credential chain.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: resolving AWS env markers vs IMDS/instance-role auth.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential sources; relevance: the credential-source ordering (`AWS_BEARER_TOKEN_BEDROCK`→keys→profile→chain).
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — request kwargs builder; relevance: assembling `serviceTier`/temperature-omission params for Bedrock.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — API-mode resolution; relevance: selecting the `bedrock-converse-stream` API mode.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — credential pool seeding; relevance: seeding/rotating Bedrock auth profiles.

### oc_provider_bedrock_mantle (10t · 11s · 10d)

**Terms**
- [Amazon Bedrock](../../term_dictionary/term_bedrock.md) — AWS managed model service; relevance: Mantle is a Bedrock-backed OpenAI-compatible surface.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: Mantle exposes `openai-completions` (`/v1/chat/completions`).
- [Converse API](../../term_dictionary/term_converse_api.md) — native Bedrock API (contrast); relevance: the page contrasts Mantle's `/v1` surface with native Bedrock Converse.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — default credential resolution; relevance: IAM path mints a Mantle bearer token from the SDK chain.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer-token credential; relevance: `AWS_BEARER_TOKEN_BEDROCK` explicit vs minted bearer auth.
- [IAM](../../term_dictionary/term_iam.md) — AWS access management; relevance: IAM credentials generate the Mantle bearer token.
- [Claude](../../term_dictionary/term_claude.md) — Claude on Mantle; relevance: the Anthropic Messages route carries Claude Opus 4.7 via Mantle.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw provider abstraction; relevance: `amazon-bedrock-mantle` is a bundled provider plugin.
- [Quantization](../../term_dictionary/term_quantization.md) — OSS model serving optimization; relevance: Mantle hosts OSS models (GPT-OSS/Qwen/Kimi/GLM) served at scale.
- [LLM](../../term_dictionary/term_llm.md) — generative-model umbrella; relevance: Mantle is OpenClaw's OSS-model inference surface.

**Docs**
- [cc_amazon_bedrock_mantle_endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — Claude Code Mantle endpoint doc; relevance: the same Mantle OpenAI-compatible endpoint, cross-ecosystem.
- [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock setup; relevance: shared AWS credential/region setup for the Bedrock-backed endpoint.
- [bedrock_chat_completions_mantle](../aws_bedrock/bedrock_chat_completions_mantle.md) — AWS Mantle chat-completions doc; relevance: authoritative reference for the `/v1/chat/completions` Mantle surface.
- [bedrock_api_keys_generate](../aws_bedrock/bedrock_api_keys_generate.md) — Bedrock API-key/bearer-token generation; relevance: how `AWS_BEARER_TOKEN_BEDROCK` is created.
- [bedrock_api_keys_manage_security](../aws_bedrock/bedrock_api_keys_manage_security.md) — Bedrock API-key security; relevance: managing/rotating the bearer token Mantle uses.
- [bedrock_messages_api](../aws_bedrock/bedrock_messages_api.md) — Bedrock Messages API; relevance: the Anthropic Messages route Mantle exposes for Claude.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud-providers doc; relevance: cross-ecosystem OpenAI-compatible + AWS-cred provider setup.
- [oc_provider_bedrock](oc_provider_bedrock.md) — sibling native Bedrock provider note (planned, this series); relevance: the page explicitly relates Mantle to native Bedrock (shared bearer token).
- [oc_provider_anthropic](oc_provider_anthropic.md) — sibling Anthropic provider note (planned, this series); relevance: Claude via the Mantle Anthropic Messages route vs direct Anthropic.
- [oc_provider_cerebras](oc_provider_cerebras.md) — sibling provider note (planned, this series); relevance: another OpenAI-compatible (`openai-completions`) OSS-model provider.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension package; relevance: hosts the `amazon-bedrock-mantle` provider.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Hermes agent core; relevance: hosts the Bedrock credential/bearer adapter shared with Mantle.

**Snippets**
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock provider plugin; relevance: shares the bearer-token credential path with Mantle.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — Bedrock adapter credentials; relevance: minting a bearer token from the AWS SDK chain.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: the `openai-completions` API surface Mantle uses.
- [snippet_hermes_agent_core_bedrock_adapter_discovery](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_discovery.md) — Bedrock discovery; relevance: querying the region `/v1/models` Mantle endpoint for discovery.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — API-mode resolution; relevance: switching a model to `anthropic-messages` vs `openai-completions` on Mantle.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — Anthropic adapter client; relevance: the Anthropic Messages route Mantle exposes for Claude.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential sources; relevance: explicit-bearer vs IAM-minted credential resolution.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: resolving the Mantle bearer-token auth path.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model normalization; relevance: normalizing discovered Mantle OSS-model refs.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: the bundled-plugin registration behind `amazon-bedrock-mantle`.

### oc_provider_cerebras (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway hosting the provider; relevance: the page documents OpenClaw's Cerebras provider plugin.
- [LLM](../../term_dictionary/term_llm.md) — generative-model umbrella; relevance: Cerebras serves high-speed LLM inference.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw provider abstraction; relevance: Cerebras installs as `@openclaw/cerebras-provider`.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — static model list; relevance: the static four-model catalog (128k context / 8,192 max-output).
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: Cerebras uses `openai-completions`.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — step-by-step reasoning; relevance: two catalog models (GLM 4.7, GPT-OSS 120B) are reasoning models.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-use capability; relevance: supported feature for the OpenAI-compatible Cerebras models.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI; relevance: Cerebras is an external hosted inference service.
- [Quantization](../../term_dictionary/term_quantization.md) — model-serving optimization; relevance: the OSS catalog (GPT-OSS, Llama, Qwen) is served on custom inference hardware.

**Docs**
- [cc_model_selection](../claude_code/cc_model_selection.md) — model-selection doc; relevance: choosing `cerebras/*` as `model.primary`.
- [cc_fast_mode](../claude_code/cc_fast_mode.md) — fast-mode/latency doc; relevance: Cerebras' value prop is high-speed inference.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: same plugin-install + env-var auth pattern.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — OpenAI-compatible local provider; relevance: the `mode: "merge"` static-catalog override pattern.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the installed-plugin model behind Cerebras.
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — auxiliary provider config; relevance: daemon-env note for `CEREBRAS_API_KEY`.
- [pi_custom_models](../pi/pi_custom_models.md) — custom-model registration; relevance: registering a static OpenAI-compatible catalog with merge mode.
- [oc_provider_arcee](oc_provider_arcee.md) — sibling provider note (planned, this series); relevance: the closest parallel — plugin-install + OpenAI-compatible + static catalog.
- [oc_provider_bedrock_mantle](oc_provider_bedrock_mantle.md) — sibling provider note (planned, this series); relevance: another OpenAI-compatible OSS-model provider.
- [oc_provider_anthropic](oc_provider_anthropic.md) — sibling provider note (planned, this series); relevance: shared onboarding `--auth-choice` env-var auth.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension package; relevance: where the Cerebras provider plugin lives.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: OpenAI-compatible adapter pattern for a third-party provider.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: the API surface class Cerebras uses.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog code; relevance: how the static four-model Cerebras catalog is registered.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local OpenAI-compatible provider; relevance: the `mode: "merge"` override pattern against a static catalog.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — cloud OpenAI-compatible provider plugin; relevance: a parallel hosted OpenAI-compatible provider plugin.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry CLI; relevance: `models list --provider cerebras` enumeration.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base class; relevance: the abstract provider interface Cerebras implements.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — API-mode resolution; relevance: resolving the `openai-completions` API mode for Cerebras.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: how `@openclaw/cerebras-provider` registers on install.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — auth resolution; relevance: `CEREBRAS_API_KEY` onboarding/env resolution.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model normalization; relevance: normalizing `cerebras/*` refs in the static catalog.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential sources; relevance: daemon-vs-interactive-shell env resolution for the API key.

> `term_extended_thinking`→`term_chain_of_thought`; `term_amazon_titan`/`term_service_tier`→`term_amazon_nova`/`term_bedrock`;
> `term_tts`/`term_speech_synthesis`→`term_text_to_speech`; `term_video_generation`→`term_diffusion_model`/`term_multimodal`;
> `term_streaming`→(prose); `term_embeddings`→`term_embedding`(not cited, used `term_amazon_nova`/`term_bedrock`);
> `term_memory_search`→`term_bedrock`; `term_cohere`→`term_amazon_nova`; `term_aws_credentials`→`term_aws_sdk_credential_chain`.

## Undigested Terms Plan

Per master's corpus-wide policy: OpenClaw provider vocabulary is the *subject* of these doc pages → digested
as the `oc_provider_*` notes themselves, NOT as new `term_dictionary` entries. Existing terms are LINKED only.

| Term | Disposition |
|---|---|
| Alibaba Model Studio / DashScope / Wan video models | Digested as `oc_provider_alibaba`; `term_video_generation` is MISSING (do NOT create — out of scope), so link the `/tools/video-generation` doc + nearest existing media term `term_text_to_speech` and concept `term_model_catalog`. No new term. |
| Anthropic / Claude CLI backend / `claude -p` billing | Digested as `oc_provider_anthropic`; link existing `term_claude`, `term_claude_code`. No new term. |
| Prompt caching (short/long/none) | Existing `term_prompt_caching` + `term_kv_cache` LINKED. No new term. |
| Adaptive / extended thinking, thinking defaults | Existing `term_chain_of_thought` LINKED (note `term_extended_thinking`/`term_streaming` are MISSING — do NOT create here; out of scope, link `term_chain_of_thought`). No new term. |
| Arcee Trinity / mixture-of-experts | Existing `term_mixture_of_experts` LINKED. No new term. |
| OpenAI-compatible API / `openai-completions` | Existing `term_openai_responses_api` LINKED (nearest existing). No new term. |
| Azure AI Speech / text-to-speech / SSML / voice ShortName | Digested as `oc_provider_azure_speech`; link existing `term_text_to_speech`, `term_speech_to_text`. No new term. |
| Amazon Bedrock / Converse API / inference profiles / cross-region / guardrails / service tier | Existing `term_bedrock`, `term_converse_api`, `term_inference_profile`, `term_cross_region_inference`, `term_guardrails`, `term_aws_sdk_credential_chain`, `term_iam`, `term_amazon_nova` LINKED. No new term. |
| Bedrock Mantle / bearer token / GPT-OSS·Qwen·Kimi·GLM | Digested as `oc_provider_bedrock_mantle`; link existing `term_bedrock`, `term_oauth_token`. No new term. |
| Cerebras / static catalog | Digested as `oc_provider_cerebras`; link existing `term_llm`, `term_model_catalog`. No new term. |
| Provider plugin / model catalog / auth profile | Existing `term_provider_plugin`, `term_model_catalog`, `term_auth_profile` LINKED. No new term. |

**Expected new `term_dictionary` captures from pr01: 0.** No genuinely cross-cutting, vault-reusable term lacks
an existing note here; all provider names map to doc notes or to existing terms. Augment re-runs the Step 2d
new-term scan to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — pr01 authors zero `term_dictionary` notes. (Inherited from master: any genuinely new
cross-cutting term would be captured via `/tessellum-capture-term-note` + added to its `acronym_glossary_*.md`,
e.g. `acronym_glossary_llm` for an LLM/provider term — not expected here.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean (YAML field order, itemized keywords/topics, no forbidden fields, `## Overview`/`## Related Notes`/`## References` + bold footer present). |
| G2 | Grounding | Each note's claims diff-verify against its `inbox/openclaw_docs/providers/<page>.md` source (no hallucinated env vars/model ids/flags). |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2,500 words / ≤6 code blocks, one building_block; every source H2/H3 mapped (Section Coverage Map, no orphans). |
| G4 | Cross-Reference | Each note's `## Related Notes` has ≥6 relevance-selected term links + sibling/repo/doc/snippet links, each an indexed `[text](path.md)` with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after reindex. |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` rows + `repo_openclaw_extensions_llm_providers`/`repo_openclaw_extensions_voice_speech`/`term_bedrock`/`term_claude` inlinks. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_provider_alibaba oc_provider_anthropic oc_provider_arcee oc_provider_azure_speech oc_provider_bedrock oc_provider_bedrock_mantle oc_provider_cerebras"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + broken-link class
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # density caps (≤2500 words, ≤6 code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # at least one sibling oc_ link present (G4 cross-ref to series)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING oc_ LINK"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code blocks (page) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_provider_alibaba | procedure | 480 | 0 (config snippets in `<Steps>`/`<Accordion>`) | ✅ |
| 2 | oc_provider_anthropic | procedure | 720 | 2 fenced (+ config in tabs/accordions) | ✅ (largest digest; ≤6 code by selective reproduction) |
| 3 | oc_provider_arcee | procedure | 460 | 1 | ✅ |
| 4 | oc_provider_azure_speech | procedure | 440 | 0 (config in `<Steps>`) | ✅ |
| 5 | oc_provider_bedrock | procedure | 760 | 1 fenced (+ many config accordions; reproduce ≤6 selectively) | ✅ (1,920w source → ≤2,500w digest; ≤6 code) |
| 6 | oc_provider_bedrock_mantle | procedure | 560 | 2 | ✅ |
| 7 | oc_provider_cerebras | procedure | 460 | 6 (`<CodeGroup>` + config) | ✅ (cap exactly 6; reproduce onboarding + one config selectively) |

No note approaches the line or word caps. Cerebras (6 fences) and the accordion-heavy bedrock/anthropic pages
are the code-density watch items — reproduce the load-bearing config block(s) verbatim and prose-summarize the
rest to stay ≤6 code blocks per note.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1, since the corpus >30
notes) under the **Providers** section / pr01 sub-cluster — one row per `oc_provider_*` note. Each note also
receives the entry-point back-link at finalization (satisfies G7/G8 in-degree ≥1). Parent-hub wiring
`repo_openclaw.md` → `entry_openclaw_docs.md`) are master W2/W3 steps, not repeated per sub-plan.

## Inlinks (existing notes → new notes)

guarantee in-degree ≥1 per note, G7/G8):

- `entry_openclaw_docs.md` (planned, master W1) → **all 7 notes** (primary anti-island guarantee).
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 2, 3, 5, 6, 7 (the LLM-provider extension package).
- `repo_openclaw_extensions_voice_speech.md` → note 4 (the speech/TTS extension package).
- `term_bedrock.md` → notes 5, 6; `term_converse_api.md` → note 5; `term_inference_profile.md` → note 5.
- `term_claude.md` → note 2; `term_claude_code.md` → note 2; `term_prompt_caching.md` → note 2.
- `term_text_to_speech.md` → note 4; `term_mixture_of_experts.md` → note 3; `term_model_catalog.md` → notes 1, 3, 7.
- `repo_openclaw_agents.md` → notes 1, 2, 4 (model-catalog / auth resolution host).

## Pacing Rules (inherited from master)

Single phase, 7 notes — well under the ~30-agent fan-out cap. Re-read each source page; reproduce config
snippets verbatim; one building_block per note. `git pull --rebase --autostash origin main` before commit;
no Claude co-author trailer; reindex incrementally and verify `note_links` + 0 broken links before commit;
commit + push as one cycle after the phase passes all 8 gates.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — 9/9 PASS → READY** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` at **RAISED floors** (master/plan-stage
floor was ≥6 terms; this xref-augment raises and locks to **≥8 terms · ≥10 code_snippets · ≥10 docs per note**,
each link relevance-selected from a fresh re-read of the 7 source pages, rendered as
`cc_*`/`hermes_*`/`pi_*`/`band_*`/`aws_bedrock*` corpora) toward the 10-doc floor, the remainder sibling `oc_*`.

**Per-note counts (terms · snippets · docs · repos — all floors met):**

| Note | Terms | Snippets | Docs (≥5 existing) | Repos | Floors (≥8/≥10/≥10)? |
|---|---:|---:|---:|---:|---|
| oc_provider_alibaba | 9 | 10 | 10 (7 existing) | 3 | ✅ |
| oc_provider_anthropic | 10 | 11 | 10 (7 existing) | 3 | ✅ |
| oc_provider_arcee | 8 | 10 | 10 (7 existing) | 3 | ✅ |
| oc_provider_azure_speech | 8 | 10 | 10 (6 existing) | 3 | ✅ |
| oc_provider_bedrock | 12 | 12 | 11 (10 existing) | 4 | ✅ |
| oc_provider_bedrock_mantle | 10 | 11 | 10 (7 existing) | 3 | ✅ |
| oc_provider_cerebras | 9 | 11 | 10 (7 existing) | 3 | ✅ |

**Ghost substitutions applied (MISSING terms NOT cited; existing substitute used):** `term_extended_thinking`
→ `term_chain_of_thought`; `term_amazon_titan` / `term_service_tier` → `term_amazon_nova` / `term_bedrock`;
`term_tts` / `term_speech_synthesis` → `term_text_to_speech`; `term_video_generation` → `term_diffusion_model`
+ `term_multimodal`; `term_streaming` → prose (no term); `term_embeddings` / `term_memory_search` /
`term_cohere` → `term_amazon_nova` / `term_bedrock`; `term_aws_credentials` → `term_aws_sdk_credential_chain`.
Newly surfaced (vs plan-stage) relevant EXISTING terms now used: `term_moe`, `term_sigv4`,
`term_contextual_grounding`, `term_voice_mode`, `term_voice_call`, `term_multimodal`, `term_diffusion_model`,
`term_quantization`.

**New-term candidates (Step 2d re-scan): 0.** Confirmed per master's corpus-wide policy — OpenClaw provider
vocabulary is the *subject* of these doc pages (digested as the `oc_provider_*` notes), so no new
`term_dictionary` entry is warranted; all provider concepts map to a doc note or an existing term. No best-fit
glossary action needed (would be `acronym_glossary_llm` if a genuinely cross-cutting LLM/provider term arose).

**Source re-read / density (CP7 measured 2026-06-21, body-only `wc -w` after YAML strip):** alibaba 724w,
anthropic 1527w, arcee 522w, azure-speech 510w, bedrock 1886w, bedrock-mantle 827w, cerebras 533w; total
6,529w (plan estimate 6,772w → 0.96×, all pages within ±30%). Cerebras = 6 fenced blocks (cap exactly 6 — the
`<CodeGroup>` onboarding triple + config; reproduce selectively). No re-split required; all 7 stay 1 note each
(single-BB provider-setup procedures, all ≤2,500w / ≤6 code).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint final review applied to this sub-plan (`status: pending`). CP7 source words measured by
actual re-read (not memory).

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, per-link relevance) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; per-note ≥8 terms · ≥10 snippets · ≥10 docs (table above); every link has a `relevance:` clause; smallest term count = 8 (arcee, azure_speech). |
| CP2 | 9-GATE per batch (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7/G8 Discoverability — all with pass criteria. |
| CP3 | Entry point update specified (inherited; `entry_openclaw_docs` planned at W1) | **PASS** | `## Entry Point Decision`: 7 rows → `entry_openclaw_docs.md` (master W1 CREATE, corpus >30 notes), Providers section / pr01 sub-cluster; back-link per note at finalization. |
| CP4 | Plan size (≤30 or split) | **PASS** | 7 planned notes — well under 30; single execution phase. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Master Format Definition derived from `claude_code/`(`cc_*`)+`pi/`(`pi_*`) corpora: YAML field order tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group; body `# OpenClaw — …`→`## Overview`→source-mirrored H2/H3→`## Related Notes`→`## References`→bold footer; forbidden fields listed; inherited verbatim here. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: no note approaches caps (max digest 760w; cerebras = 6 code, at cap, reproduce selectively); no borderline note left unaddressed; SPLIT decisions table = none (justified, single-BB sub-cap pages). |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 7 pages 2026-06-21: 724/1527/522/510/1886/827/533w (total 6,529w) vs plan 764/1553/557/544/1920/868/566 (6,772w); ratio 0.96×, all within 0.7–1.3×. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (11 rows, each "No new term" with existing-term LINK disposition); `## Term-Note Authoring Requirements` present and **N/A justified (0 new terms)** with inherited master capture-term-note path stated. |
| CP8f | Slug specificity + all-notes (term AND doc) dedup/collision audit | **PASS** | 0 new term slugs → no specificity rename needed. Dedup-before-create across `term_dictionary/` AND `documentation/` AND `repo_openclaw*` is the master Dedup Policy; the 7 `oc_provider_*` doc slugs collide with NO existing substantive vault note (no `oc_provider_*` exist yet; provider concepts are doc-subjects, terms are LINKED not recreated). Ghost-flagged MISSING candidates substituted, not created. |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` covers all 7 notes with ≥1 outside-folder inbound source (`entry_openclaw_docs` → all 7; `repo_openclaw_extensions_llm_providers` → 1/2/3/5/6/7; `repo_openclaw_extensions_voice_speech` → 4; term backlinks); G7/G8 Discoverability is in the phase gate table, marked executed at finalization (in-degree ≥1, anti-island). |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
