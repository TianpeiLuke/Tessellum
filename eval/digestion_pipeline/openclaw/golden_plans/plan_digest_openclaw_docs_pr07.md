---
title: Sub-Plan pr07 — OpenClaw Docs: Providers (Perplexity, PixVerse, Qianfan, Qwen, Qwen-OAuth, Runway, SenseAudio)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/perplexity-provider", "providers/pixverse", "providers/qianfan", "providers/qwen", "providers/qwen-oauth", "providers/runway", "providers/senseaudio"]
augmented: 2026-06-21
reviewed: 2026-06-21
---

# Sub-Plan pr07: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup-before-create, 9-GATE, cross-refs,
> undigested-terms ownership (OpenClaw vocab → `oc_` doc notes, link existing terms), and entry-point wiring are
> ALL inherited from the master. This file adds the measured per-page section coverage, planned-notes table, split
> decisions, and CANDIDATE cross-references (the locked per-note Related mapping is produced later at augment).

## Scope

The 7 provider-setup reference pages assigned to pr07 — a mix of provider *types*: one web-search provider
(Perplexity), two video-generation providers (PixVerse, Runway), one audio/STT media-understanding provider
(SenseAudio), and three LLM/model providers (Qianfan, Qwen, Qwen-OAuth). Each page documents how to install/enable
the provider plugin, set the auth env var / onboarding auth-choice, pick the default model, and configure
provider-specific options (regions, modes, catalogs). **Priority P2 (Phase B)** — the provider/integration layer
that the concepts/gateway/CLI core (Phase A) references; users reach these pages when wiring a specific vendor.
The code-side counterparts (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`,
`repo_openclaw_agents`) are LINKED, not recreated (master dedup policy).

**Source**: OpenClaw docs, 7 pages, **4,370 measured words** (Step 2, 2026-06-20). **Planned: 7 notes** (1 note per
page; no page exceeds the 2,500-word / mixed-BB split threshold).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Perplexity | `providers/perplexity-provider` | 543 | 1 | 6 | 0 | procedure |
| PixVerse | `providers/pixverse` | 623 | 1 | 6 | 0 | procedure |
| Qianfan | `providers/qianfan` | 522 | 2 | 5 | 0 | procedure |
| Qwen | `providers/qwen` | 1,495 | 2 | 8 | 0 | procedure |
| Qwen OAuth / Portal | `providers/qwen-oauth` | 509 | 5 | 8 | 0 | procedure |
| Runway | `providers/runway` | 421 | 1 | 5 | 0 | procedure |
| SenseAudio | `providers/senseaudio` | 257 | 0 | 3 | 0 | procedure |

> Code counts are fence-pairs (`grep -c '^\`\`\`'` ÷ 2). All pages use H2 only (0 H3); their `<Steps>`/`<Tabs>`/
> `<AccordionGroup>`/`<Accordion>` MDX components nest sub-content under each H2 (e.g. Qwen's 6 Accordions live
> under "Advanced configuration"). No page is code-heavy enough to risk the ≤6-fence cap.

## Content Strategy

- **Prioritize**: per-provider setup essentials — install/enable command, auth env var + `--auth-choice`
  onboarding flag, default model ref, and the provider-specific config (Perplexity key-prefix transport
  auto-select; PixVerse/Runway video modes + region; Qianfan/Qwen built-in catalog + OpenAI-compatible transport;
  Qwen↔Qwen-OAuth provider-id distinction; SenseAudio `tools.media.audio` wiring).
- **Split**: NONE. Largest page (Qwen, 1,495 w) is well under the 2,500-word cap and is a single coherent
  procedure (set up the Qwen provider across plan types/endpoints, with its catalog + multimodal add-ons as
  config detail) — keep as one note. All other pages are 257–623 w.
- **Link-out (do not redefine)**: shared video tool params → `tools/video-generation` (to05/to08); audio media
  understanding → `nodes/audio` (nd01); model selection/failover → `concepts/model-providers` (co04); Perplexity
  *tool* (vs provider) → `tools/perplexity-search` (to06); gateway config reference → gw02; the Alibaba/ModelStudio
  legacy provider → `providers/alibaba` (pr01). Provider vendor names (Baidu/Alibaba/DashScope/OpenRouter) are
  documented as config, NOT promoted to new term notes — link existing `term_llm`/`term_qwen`/`term_perplexity`.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_perplexity_provider.md` | procedure | perplexity-provider.md: header table, Install plugin, Getting started, Search modes, Native API filtering, Advanced configuration, Related | 520 | Configuring Perplexity as an OpenClaw web-search provider: install `@openclaw/perplexity-plugin`, set `PERPLEXITY_API_KEY` (native `pplx-`) or `OPENROUTER_API_KEY` (Sonar `sk-or-`) with auto-transport-by-prefix, native-API filters (country/language/date/domain/budget), and daemon/OpenRouter-proxy notes. |
| 2 | `oc_providers_pixverse.md` | procedure | pixverse.md: header table, Getting started, Supported modes and models, Provider options, Configuration, Advanced configuration, Related | 590 | Setting up the `pixverse` external video-generation provider: install `@openclaw/pixverse-provider`, set `PIXVERSE_API_KEY`, choose International/CN region, make `pixverse/v6` the default video model; covers text/image-to-video modes, duration/resolution/aspect options, provider-specific keys, and `video_id` task polling. |
| 3 | `oc_providers_qianfan.md` | procedure | qianfan.md: header table, Install plugin, Getting started, Built-in catalog, Config example, Accordions (transport/catalog/troubleshooting), Related | 520 | Connecting Baidu Qianfan's OpenAI-compatible unified MaaS API: install `@openclaw/qianfan-provider`, set `QIANFAN_API_KEY` (`bce-v3/ALTAK-...`), use the built-in catalog (`qianfan/deepseek-v3.2` default, `ernie-5.0-thinking-preview`), with a full `models.providers.qianfan` config example and transport/override caveats. |
| 4 | `oc_providers_qwen.md` | procedure | qwen.md: header, Install plugin, Getting started (Coding/Standard/OAuth tabs), Plan types and endpoints, Built-in catalog, Thinking Controls, Multimodal add-ons, Advanced configuration (6 accordions), Related | 700 | The first-class `qwen` provider plugin: install + onboard across plan types (Coding Plan vs Standard pay-as-you-go vs Portal) and China/Global endpoints, the static model catalog, `enable_thinking` mapping, multimodal add-ons (Qwen-VL understanding, Wan video generation), and `modelstudio` compatibility aliasing. |
| 5 | `oc_providers_qwen_oauth.md` | procedure | qwen-oauth.md: header, Setup, Defaults, How this differs from Qwen, When to choose, Models, Migration, Troubleshooting, Related | 480 | The `qwen-oauth` Qwen Portal provider id (`portal.qwen.ai/v1`): when to use it vs the canonical `qwen` provider, setup via `--auth-choice qwen-oauth` / `QWEN_API_KEY`, the `qwen-oauth/qwen3.5-plus` default, and migration/troubleshooting for legacy Qwen Portal OAuth / Qwen CLI tokens. |
| 6 | `oc_providers_runway.md` | procedure | runway.md: header table, Getting started, Supported modes and models, Configuration, Advanced configuration, Related | 430 | The bundled (enabled-by-default) `runway` video-generation provider: set `RUNWAYML_API_SECRET`/`RUNWAY_API_KEY`, make `runway/gen4.5` the default; covers the seven models across text/image/video-to-video modes, mode-allowlist validation, aspect-ratio limits, and task-based polling. |
| 7 | `oc_providers_senseaudio.md` | procedure | senseaudio.md: header table, Getting started, Options, Related | 300 | The bundled `senseaudio` batch speech-to-text provider for inbound voice notes: set `SENSEAUDIO_API_KEY`, enable `tools.media.audio` with model `senseaudio-asr-pro-1.5-260319`, and the option table (model/language/prompt/baseUrl/headers); STT-only (realtime transcription uses streaming providers). |

Filename rule applied: `oc_` + full slug with `/` and `-` → `_` (e.g. `providers/perplexity-provider` →
`oc_providers_perplexity_provider.md`, `providers/qwen-oauth` → `oc_providers_qwen_oauth.md`). One BB per note (all
procedure). No aspect suffixes — no page split.

## Section Coverage Map

```
providers/perplexity-provider.md → note 1 (oc_providers_perplexity_provider)
├── header table (Type / Auth / Config path) ─────────── → note 1
├── ## Install plugin ────────────────────────────────── → note 1
├── ## Getting started (Set API key / Start searching) ─ → note 1
├── ## Search modes (pplx- native vs sk-or- OpenRouter) ─ → note 1
├── ## Native API filtering (country/lang/date/domain/budget) → note 1
├── ## Advanced configuration (daemon env var, OpenRouter proxy) → note 1
└── ## Related (→ tools/perplexity-search [to06], gateway config-ref [gw02]) → note 1 (link-out)

providers/pixverse.md → note 2 (oc_providers_pixverse)
├── header table (id/package/auth/flags/api/default/region) → note 2
├── ## Getting started (install / set key / default / generate) → note 2
├── ## Supported modes and models (text/image-to-video; duration/res/aspect/audio) → note 2
├── ## Provider options (seed/negativePrompt/quality/motionMode/cameraMovement/templateId) → note 2
├── ## Configuration (json5 default video model) ──────── → note 2
├── ## Advanced configuration (API region, custom baseUrl, task polling) → note 2
└── ## Related (→ tools/video-generation [to05/08], config-agents [gw01]) → note 2 (link-out)

providers/qianfan.md → note 3 (oc_providers_qianfan)
├── header table (provider/auth/api/baseUrl) ─────────── → note 3
├── ## Install plugin ────────────────────────────────── → note 3
├── ## Getting started (Baidu account / API key / onboard / verify) → note 3
├── ## Built-in catalog (deepseek-v3.2 default, ernie-5.0-thinking-preview) → note 3
├── ## Config example (full models.providers.qianfan json5) → note 3
├── (AccordionGroup) transport / catalog+overrides / troubleshooting → note 3
└── ## Related (→ concepts/model-providers [co04], config-ref [gw02], concepts/agent [co01]) → note 3 (link-out)

providers/qwen.md → note 4 (oc_providers_qwen)
├── header (provider/portal/env vars/api style) ──────── → note 4
├── ## Install plugin ────────────────────────────────── → note 4
├── ## Getting started (Tabs: Coding Plan / Standard / OAuth-Portal) → note 4
├── ## Plan types and endpoints (5-row endpoint table) ─ → note 4
├── ## Built-in catalog (10 model refs incl. qwen-oauth seed) → note 4
├── ## Thinking Controls (enable_thinking mapping) ───── → note 4
├── ## Multimodal add-ons (Qwen-VL understanding, Wan video gen) → note 4
├── ## Advanced configuration (6 accordions: media, 3.6-plus, capability plan, video details, streaming usage, multimodal regions, daemon env) → note 4
└── ## Related (→ concepts/model-providers [co04], video-generation [to05/08], providers/alibaba [pr01], help/troubleshooting [hp02]) → note 4 (link-out)

providers/qwen-oauth.md → note 5 (oc_providers_qwen_oauth)
├── intro (qwen-oauth Portal provider id, when to use) ─ → note 5
├── ## Setup (onboard --auth-choice qwen-oauth / QWEN_API_KEY) → note 5
├── ## Defaults (provider/aliases/baseUrl/env/api/default model) → note 5
├── ## How this differs from Qwen (qwen vs qwen-oauth table) → note 5
├── ## When to choose Qwen OAuth / Portal ────────────── → note 5
├── ## Models (qwen-oauth/qwen3.5-plus) ──────────────── → note 5
├── ## Migration (legacy portal OAuth → Standard) ────── → note 5
├── ## Troubleshooting (refresh failures / wrong endpoint / env confusion) → note 5
└── ## Related (→ providers/qwen [note 4], providers/alibaba [pr01], concepts/model-providers [co04], providers/index) → note 5 (link-out)

providers/runway.md → note 6 (oc_providers_runway)
├── header table (id/plugin/auth/flags/api/default) ──── → note 6
├── ## Getting started (set key / default / generate) ── → note 6
├── ## Supported modes and models (7 models × text/image/video-to-video; aspect ratios; mode allowlist) → note 6
├── ## Configuration (json5 default video model) ─────── → note 6
├── ## Advanced configuration (env var aliases, task polling) → note 6
└── ## Related (→ tools/video-generation [to05/08], config-agents [gw01]) → note 6 (link-out)

providers/senseaudio.md → note 7 (oc_providers_senseaudio)
├── header table (id/plugin/contract/auth/default model/url/site/docs) → note 7
├── ## Getting started (set key / enable audio provider / send voice note) → note 7
├── ## Options (model/language/prompt/baseUrl/headers) ── → note 7
└── ## Related (→ nodes/audio [nd01], concepts/model-providers [co04]) → note 7 (link-out)
```
No orphaned sections — every H2 (and the MDX-component sub-content nested under it) maps to exactly one note.
External `## Related` card targets are link-outs to other sub-plans' notes (to05/to06/to08, gw01/gw02, co01/co04,
nd01, hp02, pr01) or this series (note 4↔5), not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are single-BB procedures ≤1,495 w (max), well under the 2,500-word cap and the ≤6-fence cap; each maps cleanly to one provider-setup note. No mixed-BB page. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (4,370 measured words). New `oc_` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (every provider page is a setup/config how-to). 0 concept / model / argument.
- Provider-type sub-mix: web-search ×1 (Perplexity) · video-generation ×3 (PixVerse, Qwen-as-video, Runway —
  Qwen counted under LLM) · audio-STT ×1 (SenseAudio) · LLM/model ×3 (Qianfan, Qwen, Qwen-OAuth).
- Est. digest words ~3,540 (avg ~505/note; range 300–700). 12 source code fences distribute across the notes;
  every note kept ≤6 (config json5/bash snippets reproduced selectively, verbatim). No note approaches density caps.
- Cross-refs (LOCKED at xref-augment 2026-06-21, RAISED floors): per note **≥8 relevancy-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (plus relevant
  `repo_openclaw*` + sibling `oc_*`), each with a per-link relevance statement, all EXISTING targets

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

the sibling coding-agent doc corpora (`hermes_agent/hermes_*`, `pi/pi_*`, `claude_code/cc_*`, `aws_bedrock`);
sibling `oc_providers_*`/`oc_tools_*`/`oc_nodes_*` docs are this series (planned, do not exist yet) and count
toward the 10-doc floor as "(planned, this series)". `entry_openclaw_docs` is a master W1 pre-step "(planned,
W1)". Relative paths are from a note at `resources/documentation/openclaw/oc_*.md`: term →
`../../term_dictionary/`, sibling oc_ → `oc_*.md`, other doc → `../<folder>/`, repo →
`../../../areas/code_repos/`, snippet → `../../code_snippets/`.

### oc_providers_perplexity_provider (8t · 11s · 11d)

**Terms**
- [Perplexity](../../term_dictionary/term_perplexity.md) — AI-powered answer/search engine; relevance: the provider this page configures (native `pplx-` Search API or Sonar).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: the host the plugin installs into.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: Perplexity is an external web-search vendor wired via API key.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable adapter registering a vendor against a capability contract; relevance: `@openclaw/perplexity-plugin` is the provider plugin installed here.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — single entry point routing requests to backend services; relevance: OpenRouter acts as the aggregating gateway for the Sonar transport.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server fronting upstreams on the client's behalf; relevance: the `sk-or-` OpenRouter transport proxies Perplexity Sonar.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential for delegated API access; relevance: `PERPLEXITY_API_KEY`/`OPENROUTER_API_KEY` are the bearer credentials, prefix-detected.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Sonar is an LLM that synthesizes cited answers from the search.

**Docs**
- [Hermes: Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — Hermes web-search provider plugin setup; relevance: 1:1 sibling-ecosystem analog of a web-search provider plugin.
- [Hermes: Web Search and Extract](../hermes_agent/hermes_web_search_extract.md) — Hermes web search + page extraction; relevance: same capability (web search) Perplexity provides as a provider.
- [Hermes: X Search via Grok](../hermes_agent/hermes_x_search_grok.md) — alternative search provider via Grok; relevance: peer search-provider config showing the key-by-vendor pattern.
- [Hermes: Provider Routing Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing provider traffic through proxies/aggregators; relevance: parallels OpenRouter-as-proxy transport selection.
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env var reference; relevance: same env-var-credential model as `PERPLEXITY_API_KEY` for a daemon.
- [Claude Code: LLM Gateway](../claude_code/cc_llm_gateway.md) — routing model calls through a gateway; relevance: OpenRouter/Sonar is a gateway-style transport selected by key prefix.
- [Claude Code: LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM aggregating-gateway config; relevance: same aggregator pattern as the OpenRouter Sonar transport.
- [Claude Code: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway environment config; relevance: documents the proxy-transport configuration analog.
- [Claude Code: Environment Variables](../claude_code/cc_environment_variables.md) — env-var reference for keys/endpoints; relevance: the daemon-env-var caveat (`~/.openclaw/.env`) mirrors this.
- [oc_tools_perplexity_search](oc_tools_perplexity_search.md) (planned, this series — to06) — the Perplexity *tool* (how the agent invokes search); relevance: the explicit Related-card counterpart split (provider vs tool).
- [oc_providers_qianfan](oc_providers_qianfan.md) (planned, this series) — OpenAI-compatible external provider sibling; relevance: peer external-API-key provider setup in this sub-plan.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM/search provider extension code; relevance: where the Perplexity provider plugin lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: registers and loads the perplexity-plugin.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway daemon; relevance: the daemon-env-var note targets the gateway process.

**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator provider def; relevance: implements the `sk-or-` Sonar/OpenRouter transport.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — openai-completions provider def; relevance: the OpenAI-compatible transport shape the proxy path reuses.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM pricing lookup; relevance: the OpenRouter aggregator path this provider routes through.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model-ref alias resolution; relevance: maps Sonar/model refs to pricing/aliases.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential ordering across auth profiles; relevance: the key-prefix transport auto-select resolves which credential wins.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret/credential injection into calls; relevance: how `PERPLEXITY_API_KEY` reaches the request.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env resolution; relevance: the daemon-env-var caveat for launchd/systemd.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist rendering; relevance: the macOS daemon that needs the key exported.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger/env setup; relevance: the Linux daemon env-import caveat.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/restart lifecycle; relevance: `plugins install` + `gateway restart` from this page.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: gateway picks up the perplexity-plugin after restart.

### oc_providers_pixverse (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host the pixverse provider plugin installs into.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative model class behind text/image-to-video; relevance: PixVerse's video models are diffusion-based generators.
- [Video Processing](../../term_dictionary/term_video_processing.md) — operations on video data; relevance: the page configures text/image-to-video generation and output options.
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning text+image+video; relevance: image-to-video takes an image reference plus a prompt.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: PixVerse is an external hosted video vendor (Platform API v2).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — vendor adapter against a capability contract; relevance: registers `pixverse` against `videoGenerationProviders`.
- [Model Failover](../../term_dictionary/term_model_failover.md) — selecting/falling back across providers; relevance: PixVerse is one selectable default video provider among peers.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available model refs; relevance: exposes `pixverse/v6`,`c1` across modes through the shared video tool.

**Docs**
- [Hermes: Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — Hermes video-generation provider plugin; relevance: 1:1 sibling-ecosystem analog of a video-gen provider plugin.
- [Hermes: Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — Hermes image-generation provider plugin; relevance: PixVerse's template image-gen is noted as not-yet-exposed (same contract family).
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool reference; relevance: shared media/video tool surface the provider plugs into.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media output settings; relevance: parallels duration/resolution/aspect/audio output options.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — onboard a new provider; relevance: same install→key→default-model→use flow as PixVerse onboarding.
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `PIXVERSE_API_KEY` + `--auth-choice` mirror this credential model.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — configuring hosted cloud providers; relevance: PixVerse is a hosted cloud provider with region/baseUrl config.
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — choosing/defaulting a model; relevance: setting `pixverse/v6` as the default video model.
- [oc_tools_video_generation](oc_tools_video_generation.md) (planned, this series — to05/08) — shared video tool params/provider selection/async; relevance: the Related-card target this provider feeds.
- [oc_providers_runway](oc_providers_runway.md) (planned, this series) — peer bundled video-generation provider; relevance: direct sibling (modes/aspect/polling parallels).
- [oc_providers_qwen](oc_providers_qwen.md) (planned, this series) — Qwen Wan video generation; relevance: another video provider option selectable as default.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: registers the pixverse external provider.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension code; relevance: where the pixverse provider extension lives.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/contracts; relevance: owns the `videoGenerationProviders` contract and `agents.defaults.videoGenerationModel`.

**Snippets**
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline in chat; relevance: generated video flows through the media pipeline back to the user.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed media record lifecycle; relevance: handles the generated/uploaded media artifacts.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — media resize/validate; relevance: validates the image reference uploaded for image-to-video.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: the local/remote image reference passed to PixVerse.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model catalog manifest planning; relevance: exposes pixverse models across modes.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: normalizes provider-specific option bags (seed/quality/motionMode).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog; relevance: resolves `pixverse/v6` as the default video model ref.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how `@openclaw/pixverse-provider` declares the videoGenerationProviders contract.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/restart; relevance: `plugins install clawhub:@openclaw/pixverse-provider` + restart.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applies region/baseUrl/default-model config writes.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: resolves `PIXVERSE_API_KEY` for the gateway.

### oc_providers_qianfan (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host the qianfan provider plugin installs into.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Qianfan's unified MaaS API routes to many LLMs behind one key.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — open-weight reasoning LLM family; relevance: default model is `qianfan/deepseek-v3.2`.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: Baidu Qianfan is an external MaaS platform.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of model refs; relevance: built-in catalog (`deepseek-v3.2`, `ernie-5.0-thinking-preview`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — vendor adapter plugin; relevance: `@openclaw/qianfan-provider` registers the provider.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning traces; relevance: catalog models are reasoning/thinking-enabled (`reasoning: true`).
- [Context Window](../../term_dictionary/term_context_window.md) — max tokens a model accepts; relevance: catalog rows specify 98,304 / 119,000 context windows.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible request shaping; relevance: Qianfan uses the `openai-completions` OpenAI-compatible transport.

**Docs**
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider setup; relevance: Qianfan is a cloud OpenAI-compatible inference provider.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — onboard a new provider; relevance: same install→account→key→onboard→verify flow.
- [Hermes: Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog/ref reference; relevance: parallels Qianfan's built-in catalog + `qianfan/` ref prefix.
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `QIANFAN_API_KEY` (`bce-v3/ALTAK-...`) credential model.
- [pi: Custom Models](../pi/pi_custom_models.md) — defining custom model metadata; relevance: full `models.providers.qianfan` override example with custom model entries.
- [pi: Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering an OpenAI-compatible provider; relevance: registering Qianfan as an OpenAI-compatible base-URL provider.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — hosted cloud provider config; relevance: Qianfan baseUrl/api config pattern.
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — selecting a primary model; relevance: setting `qianfan/deepseek-v3.2` as the primary.
- [Claude Code: LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — unified OpenAI-compatible gateway; relevance: Qianfan's unified API routes many models behind one endpoint, like LiteLLM.
- [oc_providers_qwen](oc_providers_qwen.md) (planned, this series) — peer OpenAI-compatible Chinese MaaS provider; relevance: same OpenAI-compatible transport + static-catalog pattern.
- [oc_providers_perplexity_provider](oc_providers_perplexity_provider.md) (planned, this series) — external API-key provider sibling; relevance: peer provider-setup note in this sub-plan.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider extension code; relevance: where the qianfan provider lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: registers the qianfan-provider plugin.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — openai-completions provider def; relevance: the exact `api: "openai-completions"` transport Qianfan uses.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — anthropic provider def; relevance: contrast — native vs OpenAI-compatible request shaping (Qianfan is the latter).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog; relevance: resolves `qianfan/` model refs from the static catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: plans the built-in deepseek/ernie catalog entries.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: normalizes contextWindow/maxTokens/reasoning fields from the config example.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalization; relevance: backs `openclaw models list --provider qianfan` verification.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias lookup; relevance: the `alias: "QIANFAN"` from the config example.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI-compatible message build; relevance: builds requests over the OpenAI-compatible transport path.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/restart; relevance: `plugins install @openclaw/qianfan-provider` + restart.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how the provider plugin declares its provider id.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: resolves `QIANFAN_API_KEY` into the request path.

### oc_providers_qwen (12t · 12s · 11d)

**Terms**
- [Qwen](../../term_dictionary/term_qwen.md) — Alibaba's Qwen LLM family; relevance: the first-class provider this page configures.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host the qwen provider plugin installs into.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Qwen Cloud serves chat/coding/reasoning LLMs.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: Qwen Cloud / Alibaba DashScope is an external vendor.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of model refs; relevance: the endpoint-aware static Qwen catalog (10 model refs).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — vendor adapter plugin; relevance: `@openclaw/qwen-provider` registers `qwen` + `qwen-oauth`.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning; relevance: Thinking Controls map to DashScope's `enable_thinking` flag.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image+video models; relevance: Qwen-VL understanding + Wan video generation add-ons.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video operations; relevance: Wan video generation (`wan2.6-t2v` etc.) on Standard endpoints.
- [Context Window](../../term_dictionary/term_context_window.md) — max input tokens; relevance: catalog rows up to 1,000,000-token context.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — delegated bearer credential; relevance: the `qwen-oauth` Portal token flow exposed by this plugin.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible shaping; relevance: Qwen uses OpenAI-compatible request shapes across endpoints.

**Docs**
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider setup; relevance: Qwen is a multi-endpoint cloud inference provider.
- [Hermes: Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: parallels Qwen's endpoint-aware static catalog.
- [Hermes: Model + Aux Provider Config](../hermes_agent/hermes_model_aux_provider_config.md) — primary + auxiliary provider config; relevance: Qwen's main chat models plus VL/Wan multimodal add-ons.
- [Hermes: Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider plugin; relevance: Qwen's Wan video generation via the shared video capability.
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env vars; relevance: `QWEN_API_KEY`/`DASHSCOPE_API_KEY`/`MODELSTUDIO_API_KEY` aliasing + daemon env.
- [pi: Model Overrides / Compatibility](../pi/pi_model_overrides_compat.md) — model override + compat aliasing; relevance: `modelstudio` legacy alias compatibility for `qwen/...` refs.
- [pi: Custom Models](../pi/pi_custom_models.md) — custom model definitions; relevance: opting `qwen/qwen3.6-plus` into Coding Plan via explicit `models.providers.qwen.models`.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — hosted provider/endpoint config; relevance: the 5-row plan-type/region endpoint table.
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — selecting models; relevance: setting `qwen/qwen3.5-plus` as the primary.
- [oc_providers_qwen_oauth](oc_providers_qwen_oauth.md) (planned, this series) — the Qwen Portal provider id; relevance: the distinct `qwen-oauth` surface this page cross-references.
- [oc_tools_video_generation](oc_tools_video_generation.md) (planned, this series — to05/08) — shared video tool params; relevance: the Related-card target for Wan video generation.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider extension code; relevance: where the qwen provider plugin lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: registers the qwen-provider (both `qwen` and `qwen-oauth`).
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/contracts; relevance: owns the model catalog + videoGenerationProviders contract Qwen targets.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — openai-completions provider def; relevance: Qwen's OpenAI-compatible transport across all endpoints.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog; relevance: resolves the 10 `qwen/`+`qwen-oauth/` catalog refs.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: builds the endpoint-aware Qwen static catalog (Coding omits Standard-only models).
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: normalizes input/context/notes per catalog row.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — alias lookup; relevance: `modelstudio/...` compatibility alias resolution to `qwen/...`.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI-compatible message build; relevance: maps thinking levels to top-level `enable_thinking`.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI-compatible SSE streaming; relevance: the streaming-usage compatibility on DashScope-compatible hosts.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline; relevance: Qwen-VL understanding + Wan video flow through the media pipeline.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential ordering; relevance: `QWEN_API_KEY`/`MODELSTUDIO_API_KEY`/`DASHSCOPE_API_KEY` acceptance order.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/restart; relevance: `plugins install @openclaw/qwen-provider` + restart.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how the plugin declares both provider ids.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: daemon `QWEN_API_KEY` availability caveat.

### oc_providers_qwen_oauth (9t · 11s · 11d)

**Terms**
- [Qwen](../../term_dictionary/term_qwen.md) — Alibaba's Qwen LLM family; relevance: the underlying model family the Portal provider serves.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host that stores credentials under the `qwen-oauth` provider id.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the Qwen Portal OAuth / CLI auth surface this provider id wraps.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the Qwen Portal token (`QWEN_API_KEY`) for `portal.qwen.ai/v1`.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity/credentials; relevance: the `--auth-choice qwen-oauth` onboarding auth surface, separate from DashScope keys.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: serves `qwen-oauth/qwen3.5-plus` and the broader Qwen catalog.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — vendor adapter plugin; relevance: `qwen-oauth` is a provider id exposed by the qwen plugin.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: Qwen Portal is an external Alibaba endpoint.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model-ref registry; relevance: the catalog seeds the `qwen-oauth/qwen3.5-plus` default.

**Docs**
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth credential flow handling; relevance: parallels the Qwen Portal OAuth token onboarding/refresh model.
- [Hermes: Provider XAI Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — an OAuth-based provider setup; relevance: 1:1 analog of an OAuth-portal provider id (vs API-key provider).
- [Hermes: Provider Minimax OAuth](../hermes_agent/hermes_provider_minimax_oauth.md) — another OAuth-based provider; relevance: peer subscription/OAuth-vs-key provider decision.
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `QWEN_API_KEY` shared between `qwen` and `qwen-oauth` (the env-confusion caveat).
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: when-to-choose Portal vs Standard cloud endpoints.
- [pi: Provider Auth](../pi/pi_provider_auth.md) — subscription-vs-key auth model; relevance: the core Portal-token vs DashScope-key distinction this page draws.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — endpoint/provider config; relevance: the `portal.qwen.ai/v1` endpoint and migration to Standard ModelStudio.
- [Claude Code: Authentication](../claude_code/cc_authentication.md) — auth/credential setup; relevance: separate auth surfaces + migration when a token stops refreshing.
- [oc_providers_qwen](oc_providers_qwen.md) (planned, this series) — canonical `qwen` provider; relevance: the explicit "How this differs from Qwen" counterpart.
- [oc_providers_qianfan](oc_providers_qianfan.md) (planned, this series) — peer OpenAI-compatible provider; relevance: sibling provider-setup note in this sub-plan.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) (planned, this series — co04) — model/provider selection; relevance: the Related-card target for choosing providers.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider extension code; relevance: where the qwen plugin (incl. `qwen-oauth`) lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: registers the `qwen-oauth` provider id.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/contracts; relevance: stores auth profiles/credentials per provider id.

**Snippets**
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth auth-profile portability; relevance: keeping legacy Qwen Portal OAuth credentials addressable under a distinct id.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: migrating a legacy Qwen CLI / Portal workflow.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential ordering; relevance: `QWEN_API_KEY` stored under the selected provider id, not shared.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret/credential injection; relevance: the Portal token reaching `portal.qwen.ai/v1` requests.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — openai-completions provider def; relevance: `qwen-oauth` uses OpenAI-compatible request shapes.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog; relevance: seeds `qwen-oauth/qwen3.5-plus` default and `qwen-oauth/` refs.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — alias lookup; relevance: `qwen-portal`/`qwen-cli` aliases for the provider id.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding wizard config writes; relevance: `openclaw onboard --auth-choice qwen-oauth` flow.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import in setup; relevance: migrating legacy Portal OAuth to Standard.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how the plugin exposes the second `qwen-oauth` provider id.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: resolving the shared `QWEN_API_KEY` to the right provider id.

### oc_providers_runway (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host bundling the `runway` provider (enabled by default).
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative video model class; relevance: Runway's Gen/Veo models are diffusion-based generators.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video operations; relevance: text/image/video-to-video generation across seven models.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: Runway is an external hosted video vendor (task-based API).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — vendor adapter plugin; relevance: registers `runway` against `videoGenerationProviders`.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image+video; relevance: image-to-video and video-to-video take media reference inputs.
- [Model Failover](../../term_dictionary/term_model_failover.md) — provider selection/fallback; relevance: Runway is one selectable default video provider among peers.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model-ref registry; relevance: the seven Runway models with per-mode allowlists (`TEXT_ONLY_MODELS`/`IMAGE_MODELS`/`VIDEO_MODELS`).

**Docs**
- [Hermes: Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin; relevance: 1:1 sibling-ecosystem analog of a video-gen provider.
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool reference; relevance: shared video tool surface Runway plugs into.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media output settings; relevance: parallels aspect-ratio limits per mode.
- [Hermes: Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-gen provider plugin; relevance: image reference inputs for image-to-video (same media-contract family).
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env vars; relevance: `RUNWAYML_API_SECRET`/`RUNWAY_API_KEY` alias acceptance.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — onboard a provider; relevance: same set-key→default-model→generate flow.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — hosted provider config; relevance: Runway is a bundled hosted cloud provider.
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — selecting/defaulting models; relevance: setting `runway/gen4.5` as the default video model.
- [oc_tools_video_generation](oc_tools_video_generation.md) (planned, this series — to05/08) — shared video tool params/provider selection/async; relevance: the Related-card target this provider feeds.
- [oc_providers_pixverse](oc_providers_pixverse.md) (planned, this series) — peer external video-generation provider; relevance: direct sibling (modes/aspect/polling parallels).
- [oc_providers_qwen](oc_providers_qwen.md) (planned, this series) — Qwen Wan video generation; relevance: another video provider option selectable as default.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: the bundled runway provider is registered here.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension code; relevance: where `extensions/runway/video-generation-provider.ts` lives.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/contracts; relevance: owns the `videoGenerationProviders` contract + default video model.

**Snippets**
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline; relevance: generated video returns through the media pipeline.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed media lifecycle; relevance: handles generated/uploaded media artifacts.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: the local/remote image+video data-URI references passed to Runway.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — media resize/validate; relevance: validates reference media before submission.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: the seven Runway model refs across three modes.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: normalizes per-mode model/aspect option bags.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog; relevance: resolves `runway/gen4.5` as the default video model.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: bundled plugin `enabledByDefault: true` lifecycle.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how the bundled provider declares the videoGenerationProviders contract.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: resolves `RUNWAYML_API_SECRET`/`RUNWAY_API_KEY`.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applies the default-video-model config write.

### oc_providers_senseaudio (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host bundling the `senseaudio` STT provider (enabled by default).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribing audio into text; relevance: SenseAudio is a batch STT/ASR provider for inbound voice notes.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming live transcription; relevance: explicit contrast — SenseAudio is batch-only, realtime uses streaming providers.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing speech from text; relevance: the complementary media direction (this provider is the STT half).
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning modalities; relevance: audio understanding feeds text into the multimodal reply pipeline.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendor APIs; relevance: SenseAudio is an external hosted ASR vendor.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — vendor adapter plugin; relevance: registers `senseaudio` against `mediaUnderstandingProviders` (audio).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the transcript is injected as `{{Transcript}}` into the LLM reply pipeline.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible endpoints; relevance: posts multipart audio to an OpenAI-compatible transcription endpoint.

**Docs**
- [Hermes: STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription setup; relevance: 1:1 sibling-ecosystem analog of a batch STT provider.
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the complementary TTS direction (SenseAudio is STT-only).
- [Hermes: Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice mode end-to-end; relevance: voice notes are the inbound source SenseAudio transcribes.
- [Hermes: Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice mode CLI config; relevance: realtime/streaming STT contrast with batch SenseAudio.
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool reference; relevance: the shared `tools.media.audio` surface SenseAudio enables.
- [Hermes: Env Vars Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env vars; relevance: `SENSEAUDIO_API_KEY` credential model.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — hosted provider config; relevance: SenseAudio baseUrl/model/headers config pattern.
- [pi: Provider Auth](../pi/pi_provider_auth.md) — key-based provider auth; relevance: the env-var-key auth surface for the audio provider.
- [oc_nodes_audio](oc_nodes_audio.md) (planned, this series — nd01) — audio media understanding node; relevance: the explicit Related-card target (media understanding audio).
- [oc_concepts_model_providers](oc_concepts_model_providers.md) (planned, this series — co04) — model/provider selection; relevance: the second Related-card target on this page.
- [oc_tools_media_overview](oc_tools_media_overview.md) (planned, this series — to05) — shared media tool overview; relevance: the `tools.media.audio` pipeline context.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension code; relevance: where the SenseAudio STT provider lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: registers the bundled senseaudio provider.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel code; relevance: inbound voice-note media originates from connected channels.

**Snippets**
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — call media-stream transcription; relevance: the streaming STT path SenseAudio is contrasted against (batch-only).
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: relays transcript text into the reply pipeline as `{{Transcript}}`.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT integration; relevance: peer STT provider showing the audio-provider config shape.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the audio-understanding pipeline the transcript flows through.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — call media-stream audio handling; relevance: how inbound audio buffers are admitted to transcription.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat transcript media pipeline; relevance: injects the `[Audio]` block + transcript into the chat reply.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: the inbound multipart audio attachment posted to SenseAudio.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — openai-completions provider def; relevance: the OpenAI-compatible transcription endpoint shape.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how the bundled provider declares the `mediaUnderstandingProviders` (audio) contract.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: bundled `enabledByDefault: true` lifecycle.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: resolves `SENSEAUDIO_API_KEY`.

## Undigested Terms Plan

Per master ownership: OpenClaw provider vocabulary is the *subject of these doc pages*, so it is digested as the
`oc_` doc notes above — NOT promoted to new `term_dictionary` entries. Provider/vendor names are documented as
config and link existing terms.

| Term (as it appears in source) | Disposition |
|---|---|
| Perplexity (provider) | Digested in note 1; link existing `term_perplexity`. No new term. |
| OpenRouter / Sonar transport | Documented as config in note 1; vendor name, no term capture; link `term_api_gateway`/`term_reverse_proxy`. |
| PixVerse (provider) | Digested in note 2; vendor name documented as config; link `term_diffusion_model`/`term_video_processing`. |
| Runway (provider) | Digested in note 6; vendor name documented as config; link `term_diffusion_model`/`term_video_processing`. |
| Qianfan / Baidu MaaS | Digested in note 3; vendor/platform name documented as config; link `term_llm`/`term_deepseek`. |
| Qwen / DashScope / ModelStudio | Digested in notes 4–5; link existing `term_qwen`; DashScope/ModelStudio are endpoint names, no term capture. |
| Qwen Portal / qwen-oauth | Digested in note 5; provider-id documented as config; link `term_oauth`/`term_oauth_token`. |
| SenseAudio (provider) | Digested in note 7; vendor name documented as config; link `term_speech_to_text`. |
| video generation / text-to-video / image-to-video | Concept link-out to `tools/video-generation` (to05/08); link `term_diffusion_model`/`term_video_processing`. No `term_video_generation` exists — NOT created here (cross-cutting; defer to master W5 if ever needed). |
| batch STT / transcription | Link existing `term_speech_to_text` + `term_realtime_transcription`. No new term. |
| web search (provider) | Link `term_third_party_genai_services`/`term_api_gateway`. No `term_web_search` exists — NOT created here. |

**New `term_dictionary` captures from pr07: 0** (matches master expectation). No genuinely cross-cutting,
vault-reusable term lacks both a doc-page home and an existing note within this sub-plan's scope. (Candidates
`term_video_generation` / `term_web_search` / `term_asr` are absent but are *vendor-agnostic capability* concepts
better owned by the Tools section sub-plans (to05/to06/to08) if promoted at all — flagged here, not captured.)

## Term-Note Authoring Requirements

**N/A (0 new terms)** for pr07 — authors zero `term_dictionary` notes. Inherited from master: any future
`acronym_glossary_*.md` (W5). No inlined term definitions in any `oc_` note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). Gate table identical to the master's 9-GATE per phase.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format (YAML field order/forbidden fields, `# OpenClaw — …` H1, `## Overview`, `## Related Notes`, `## References`, bold footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traceable to `inbox/openclaw_docs/providers/<page>.md`; config snippets verbatim) | diff vs mirror page |
| G3 | Density + Coverage (≤400 lines, ≤2,500 words, ≤6 code blocks, one BB; every H2/MDX-section mapped) | word/fence count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected `term_dictionary` + repo/sibling/other, per-link relevance statement) | Candidate Cross-References (locked at augment) |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | DB existence check on every link target |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability — each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | `entry_openclaw_docs.md` rows + inlinks (below) |
| G8 | In-degree ≥1 (anti-island) | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

All 8 must pass before commit.

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_perplexity_provider oc_providers_pixverse oc_providers_qianfan oc_providers_qwen oc_providers_qwen_oauth oc_providers_runway oc_providers_senseaudio"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  echo "$REQ_SECTIONS" | tr '|' '\n' | while read -r sec; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION in $n: $sec"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
  # sibling/related linkage present
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING LINK in $n"
done

# YAML frontmatter sweep over the whole openclaw folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G8: verify every cited link target exists + in-degree after reindex (run post-write)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  echo "$n in_degree: $(sqlite3 "$DB" "SELECT in_degree FROM notes WHERE note_name='$n'")"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_providers_perplexity_provider | procedure | 520 | 1 | ✅ |
| 2 | oc_providers_pixverse | procedure | 590 | 1 | ✅ |
| 3 | oc_providers_qianfan | procedure | 520 | 2 | ✅ |
| 4 | oc_providers_qwen | procedure | 700 | 2 | ✅ |
| 5 | oc_providers_qwen_oauth | procedure | 480 | 5 | ✅ |
| 6 | oc_providers_runway | procedure | 430 | 1 | ✅ |
| 7 | oc_providers_senseaudio | procedure | 300 | 0 | ✅ |

No note approaches the ≤2,500-word / ≤6-fence / ≤400-line caps. Largest source (Qwen, 1,495 w, 6 accordions) is
condensed to one ~700-word note — config tables summarized, the 5-row endpoint table + key catalog rows kept, the 6
advanced-config accordions distilled to the load-bearing rules (Standard-vs-Coding endpoint split, multimodal on
Standard only, daemon env). Qwen-OAuth's 5 fences (mostly 1-line bash) stay ≤6.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step; >30-note series ⇒ dedicated
entry point) under the **Providers** cluster. Each new note gets its entry-point back-link at finalization (satisfies
G7/G8 — inbound link from outside `documentation/openclaw/`). No standalone entry point for pr07 alone (it is one
of 9 Providers sub-plans feeding the shared hub). W2/W3 (parent-hub + code↔docs cross-links) are master-level.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; `entry_openclaw_docs` created at W1):

- `entry_openclaw_docs.md` (planned, W1) → all 7 notes (Providers cluster rows) — primary anti-island guarantee.
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 3, 4, 5 (LLM/search provider extensions).
- `repo_openclaw_extensions.md` → all 7 (extension/plugin framework that registers these providers).
- `repo_openclaw_extensions_voice_speech.md` → note 7 (SenseAudio STT).
- `repo_openclaw_channels_voice_phone.md` → note 7 (voice media pipeline).
- `repo_openclaw_agents.md` → notes 2, 4, 6 (videoGenerationProviders / model-catalog contracts).
- `term_qwen.md` → notes 4, 5; `term_perplexity.md` → note 1; `term_speech_to_text.md` → note 7;
  `term_diffusion_model.md` → notes 2, 6; `term_deepseek.md` → note 3.

## Pacing Rules (inherited from master)

One execution phase, 7 notes (≤30 fan-out cap, no sub-batching needed). Re-read each source page during execution;
reproduce config snippets verbatim; one BB per note. Run all 8 gates before commit. `git pull --rebase --autostash`
first; commit+push the phase as one cycle; no Claude co-author trailer. Reindex incrementally; verify `note_links`
+ 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment, raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of sub-plan pr07 (7 provider-setup notes) to RAISED per-note Related-Notes floors:
**≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** (plus relevant
repos + sibling `oc_*`), relevance-selected from a fresh re-read of all 7 source pages under

**What was locked:** The former `## Candidate Cross-References` section was replaced by
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` — one grouped H3 per planned note with
**Terms / Docs / Repos / Snippets** lists, each link carrying a per-link relevance statement. The Summary
Statistics cross-ref line was updated to the raised floors.

**Per-note counts (terms / snippets / docs / repos):**

|---|---:|---:|---:|---:|---:|---|
| oc_providers_perplexity_provider | 8 | 11 | 11 | 9 | 3 | ✅ |
| oc_providers_pixverse | 8 | 11 | 11 | 8 | 3 | ✅ |
| oc_providers_qianfan | 9 | 11 | 11 | 9 | 3 | ✅ |
| oc_providers_qwen | 12 | 12 | 11 | 9 | 3 | ✅ |
| oc_providers_qwen_oauth | 9 | 11 | 11 | 8 | 3 | ✅ |
| oc_providers_runway | 8 | 11 | 11 | 8 | 3 | ✅ |
| oc_providers_senseaudio | 9 | 11 | 11 | 8 | 3 | ✅ |

(min 8). The only non-existing targets are sibling `oc_*` docs of this series (planned, do not exist yet) and
`entry_openclaw_docs` (planned, master W1) — all explicitly marked, none counted as existing.

**Source re-read (CP7):** all 7 pages re-measured (excl. YAML) — perplexity 543w, pixverse 623w, qianfan 522w,
qwen 1,495w, qwen-oauth 509w, runway 421w, senseaudio 257w — **identical to the plan's Source table** (ratio
1.00). No under-estimation; no re-split needed.

**New-term candidates:** **0 captured** (unchanged from plan). The xref re-read confirmed the plan's ABSENT-term
inventory: `term_video_generation`, `term_web_search`, `term_asr`/`term_stt`/`term_tts`, `term_openrouter`,
`term_dashscope`, `term_baidu`, `term_alibaba`, `term_image_generation`, `term_reranking`, `term_subscription`,
`term_api_key`, `term_daemon`, `term_polling`, `term_streaming` are absent. Best-fit-glossary disposition:
these are **vendor-agnostic capability** concepts (`term_video_generation`, `term_web_search`, `term_asr`) better
owned by the Tools sub-plans (to05/to06/to08) if ever promoted → glossary `acronym_glossary_ai_ml.md` /
`acronym_glossary_gen_ai_dev.md`; vendor/endpoint names (OpenRouter/DashScope/Baidu/Alibaba/ModelStudio) stay
documented as config per master ownership. **No capture obligation added to pr07.**

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|----|-----------|--------|----------|
| CP1 | Related Notes ≥8 terms + raised floors (≥10 snippets, ≥10 docs), per-link relevance | **PASS** | Per-note counts table above; min 8 terms / 11 snippets / 11 docs; every link has `— …; relevance: …`. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Ref, G5 Ghost detect+redirect, G6 Broken-link fix, G7/G8 Discoverability+in-degree. |
| CP3 | Entry point specified / inherited | **PASS** | `## Entry Point Decision` inherits `entry_openclaw_docs` (created master W1; >30-note series ⇒ dedicated); 7 Providers-cluster rows; G7/G8 anti-island guarantee. |
| CP4 | Plan size manageable | **PASS** | 7 notes (≤30); single execution phase, no sub-batching. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (same source type); `## Overview`/`## Related Notes`/`## References`, forbidden-field list present. |
| CP6 | Borderline density → split | **PASS** | `## Density Re-Assessment`: max note ~700w (Qwen, ≤6 fences); all ≤2,500w/≤6-fence/≤400-line. No borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 pages re-measured at xref-augment; ratio 1.00 vs plan Source table (see Augmentation Report). |
| CP8 | Undigested Terms Plan + Term-Note Authoring Reqs | **PASS** | `## Undigested Terms Plan` (0 new captures, per master ownership) + `## Term-Note Authoring Requirements` (N/A, inherited from master) present. |
| CP8f | Term slug specificity / collision (all-notes dedup) | **PASS** | 0 new term slugs (no collision surface). Doc-note dedup: each `oc_providers_*` slug is unique (no existing `documentation/openclaw/` notes; sibling vendor terms `term_qwen`/`term_perplexity`/`term_deepseek` LINKED not recreated). |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps `entry_openclaw_docs` → all 7 + repo/term inbound links; G8 in-degree ≥1 in gate table; inlinks are a gated execution step, not "recommended". |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
