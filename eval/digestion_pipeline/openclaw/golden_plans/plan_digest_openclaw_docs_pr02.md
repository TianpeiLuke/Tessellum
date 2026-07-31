---
title: Sub-Plan pr02 — OpenClaw Docs: Providers (chutes, claude-max-api-proxy, cloudflare-ai-gateway, cohere, comfy, deepgram, deepinfra)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/chutes", "providers/claude-max-api-proxy", "providers/cloudflare-ai-gateway", "providers/cohere", "providers/comfy", "providers/deepgram", "providers/deepinfra"]
---

<!-- status: pending → ready (xref-augment + 9/9 review PASS, 2026-06-21) -->


# Sub-Plan pr02: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format/YAML, dedup-before-create, the 9-GATE, cross-refs, and
> entry-point wiring are ALL inherited from the master; this file holds only the measured per-page analysis, planned-note
> table, section coverage map, and candidate cross-references for these 7 provider pages.

## Scope

The seven Providers-section pages covering a heterogeneous slice of OpenClaw's provider catalog: two OpenAI-compatible
chat/LLM providers (**chutes**, **deepinfra** — both unified/aggregator APIs), two Anthropic-routing paths
(**claude-max-api-proxy** — a community subscription-as-OpenAI-endpoint proxy; **cloudflare-ai-gateway** — an analytics/
caching gateway in front of the Anthropic Messages API), one chat provider on its externalization transition
(**cohere**), and two media/speech providers (**comfy** — workflow-driven image/video/music generation;
**deepgram** — speech-to-text + Voice Call streaming). Each page is a self-contained provider setup guide (install plugin
→ auth/API key → config snippet → model catalog). **Priority P2** (Phase B — features/integration); the provider layer
is referenced by the concepts (`model-providers`), gateway (`configuration-reference`), and tools (media) docs digested in
Phase A/B. The code-side counterpart `repo_openclaw_extensions_llm_providers` (+ `_voice_speech`) is LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 4,358 measured words. **Planned: 7 notes** (one per page; no splits — all pages
single-BB and under the 2,500-word cap).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Chutes | `providers/chutes` | 570 | 4 | 7 | 0 | procedure |
| Claude Max API proxy | `providers/claude-max-api-proxy` | 722 | 6 | 7 | 0 | procedure |
| Cloudflare AI gateway | `providers/cloudflare-ai-gateway` | 463 | 6 | 5 | 0 | procedure |
| Cohere | `providers/cohere` | 283 | 4 | 3 | 0 | procedure |
| ComfyUI | `providers/comfy` | 1,264 | 14 | 6 | 2 | procedure |
| Deepgram | `providers/deepgram` | 617 | 5 | 5 | 0 | procedure |
| DeepInfra | `providers/deepinfra` | 439 | 5 | 6 | 0 | procedure |

Totals: 4,358 words · 44 code fences · 39 H2 · 2 H3. (H2/H3 counts include the page-trailing `## Related` card group, which
becomes the note's `## Related Notes`, not a digested body section.)

## Content Strategy

- **Prioritize**: the auth + onboarding path per provider (every run depends on credential setup — `openclaw onboard
  --auth-choice <provider>`, env var, and the `models.providers.*`/`plugins.entries.*` config block) and the model
  catalog / default-model behavior (static catalog vs live discovery). These are the load-bearing facts a user needs.
- **Split**: **(none).** Every page is single-BB (procedure: install → auth → config → verify) and well under the
  2,500-word cap; the largest, `comfy` (1,264w / 14 fences), stays one note but reproduces config snippets selectively to
  keep ≤6 code blocks (see Density Re-Assessment).
- **Link-out / do-not-redefine**: provider/model resolution + failover → `concepts/model-providers` (co04, link-only);
  full config schema → `gateway/configuration-reference` (gw02, link-only); media-tool pipeline (image/video/music/audio)
  → `tools/media-overview`, `tools/image-generation`, `tools/video-generation`, `tools/music-generation` (to05/to06,
  link-only); Voice Call plugin internals → `plugins/voice-call` (pl21, link-only). Provider/model names (GLM, DeepSeek,
  Kimi, Mistral, Qwen, Claude, Nova) are documented as config values, NOT promoted to term notes — link existing
  `term_llm` / `term_claude` / `term_deepseek` / `term_qwen` instead. The Anthropic-billing warning in
  claude-max-api-proxy is reproduced as a caveat, not turned into a policy/argument note.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_chutes.md` | procedure | chutes.md: Install plugin, Getting started (OAuth / API key), Discovery behavior, Default aliases, Built-in starter catalog, Config example | 480 | Configuring the OpenAI-compatible `chutes` provider: install `@openclaw/chutes-provider`, OAuth vs API-key onboarding (`CHUTES_API_KEY`/`CHUTES_OAUTH_TOKEN`), live catalog discovery with static fallback, the three default aliases, and the `chutes/zai-org/GLM-4.7-TEE` default model. |
| 2 | `oc_providers_claude_max_api_proxy.md` | procedure | claude-max-api-proxy.md: Why use this?, How it works, Getting started, Built-in catalog, Advanced configuration, Notes | 560 | Using the community `claude-max-api-proxy` to expose a Claude Max/Pro subscription as an OpenAI-compatible `localhost:3456/v1` endpoint, then pointing OpenClaw at it via `OPENAI_BASE_URL`; install/start/test steps, model-ID mapping, proxy-route caveats, and the Anthropic subscription-billing warning. |
| 3 | `oc_providers_cloudflare_ai_gateway.md` | procedure | cloudflare-ai-gateway.md: (intro/property table), Install plugin, Getting started, Non-interactive example, Advanced configuration | 470 | Routing the Anthropic Messages API through Cloudflare AI Gateway: install `@openclaw/cloudflare-ai-gateway-provider`, onboarding (account ID / gateway ID / `CLOUDFLARE_AI_GATEWAY_API_KEY`), the `cf-aig-authorization` header for authenticated gateways, prefill-stripping with extended thinking, and the daemon env-var caveat. |
| 4 | `oc_providers_cohere.md` | procedure | cohere.md: (intro/property table), Get started, Environment-only setup | 320 | Configuring the OpenAI-compatible `cohere` provider (Compatibility API) during its bundled→external-plugin transition: install `@openclaw/cohere-provider`, `COHERE_API_KEY` / `--auth-choice cohere-api-key` onboarding, environment-only daemon setup, and the `cohere/command-a-03-2025` default model. |
| 5 | `oc_providers_comfy.md` | procedure | comfy.md: What it supports, Getting started (Local / Comfy Cloud), Configuration (Shared keys, Per-capability keys), Workflow details (image/video/music/backward-compat/live-tests) | 700 | Setting up the bundled workflow-driven `comfy` provider for image/video/music generation: local vs Comfy Cloud modes, `COMFY_API_KEY`/`COMFY_CLOUD_API_KEY` auth, the `comfy/workflow` model plus shared and per-capability config keys (`workflowPath`/`promptNodeId`/`outputNodeId`), and reference-image editing. |
| 6 | `oc_providers_deepgram.md` | procedure | deepgram.md: (intro/property table), Getting started, Configuration options, Voice Call streaming STT, Notes | 560 | Using Deepgram speech-to-text in OpenClaw: batch transcription of inbound voice notes via `tools.media.audio` (`DEEPGRAM_API_KEY`, `nova-3`, language/punctuate/smart_format options) and realtime Voice Call streaming STT over the Deepgram `listen` WebSocket (G.711 u-law, 8 kHz, endpointing). |
| 7 | `oc_providers_deepinfra.md` | procedure | deepinfra.md: Install plugin, Getting an API key, CLI setup, Config snippet, Supported OpenClaw surfaces, Available models, Notes | 480 | Configuring the OpenAI-compatible DeepInfra unified provider: install `@openclaw/deepinfra-provider`, `DEEPINFRA_API_KEY` setup, the `deepinfra/<provider>/<model>` ref format, live catalog discovery, and the per-surface defaults (chat / image / video / STT / TTS / media-understanding / memory-embeddings). |

## Section Coverage Map

```
chutes.md
├── (intro + property table) ───────────────────── → note 1 (oc_providers_chutes) Overview
├── Install plugin ─────────────────────────────── → note 1
├── Getting started (OAuth tab / API key tab) ──── → note 1
├── Discovery behavior ─────────────────────────── → note 1
├── Default aliases ────────────────────────────── → note 1
├── Built-in starter catalog ───────────────────── → note 1
├── Config example (+ OAuth overrides / Notes accordions) → note 1
└── Related (cards) ────────────────────────────── → note 1 ## Related Notes
claude-max-api-proxy.md
├── (intro + Warning) ──────────────────────────── → note 2 (oc_providers_claude_max_api_proxy) Overview/caveat
├── Why use this? ──────────────────────────────── → note 2
├── How it works ───────────────────────────────── → note 2
├── Getting started (install/start/test/configure) → note 2
├── Built-in catalog ───────────────────────────── → note 2
├── Advanced configuration (proxy notes / LaunchAgent) → note 2
├── Notes ──────────────────────────────────────── → note 2
└── Related (cards) ────────────────────────────── → note 2 ## Related Notes
cloudflare-ai-gateway.md
├── (intro + property table + prefill note) ────── → note 3 (oc_providers_cloudflare_ai_gateway) Overview
├── Install plugin ─────────────────────────────── → note 3
├── Getting started ────────────────────────────── → note 3
├── Non-interactive example ────────────────────── → note 3
├── Advanced configuration (authenticated gateways / env note) → note 3
└── Related (cards) ────────────────────────────── → note 3 ## Related Notes
cohere.md
├── (intro + property table) ───────────────────── → note 4 (oc_providers_cohere) Overview
├── Get started ────────────────────────────────── → note 4
├── Environment-only setup ─────────────────────── → note 4
└── Related (links) ────────────────────────────── → note 4 ## Related Notes
comfy.md
├── (intro + property table) ───────────────────── → note 5 (oc_providers_comfy) Overview
├── What it supports ───────────────────────────── → note 5
├── Getting started (Local tab / Comfy Cloud tab) ─ → note 5
├── Configuration ──────────────────────────────── → note 5
│   ├── Shared keys (H3) ────────────────────────── → note 5
│   └── Per-capability keys (H3) ────────────────── → note 5
├── Workflow details (image/video/music/back-compat/live-tests accordions) → note 5
└── Related (cards) ────────────────────────────── → note 5 ## Related Notes
deepgram.md
├── (intro + property table) ───────────────────── → note 6 (oc_providers_deepgram) Overview
├── Getting started ────────────────────────────── → note 6
├── Configuration options ──────────────────────── → note 6
├── Voice Call streaming STT ───────────────────── → note 6
├── Notes (auth / proxy / output accordions) ───── → note 6
└── Related (cards) ────────────────────────────── → note 6 ## Related Notes
deepinfra.md
├── (intro) ────────────────────────────────────── → note 7 (oc_providers_deepinfra) Overview
├── Install plugin ─────────────────────────────── → note 7
├── Getting an API key ─────────────────────────── → note 7
├── CLI setup ──────────────────────────────────── → note 7
├── Config snippet ─────────────────────────────── → note 7
├── Supported OpenClaw surfaces ────────────────── → note 7
├── Available models ───────────────────────────── → note 7
├── Notes ──────────────────────────────────────── → note 7
└── Related (links) ────────────────────────────── → note 7 ## Related Notes
```
No orphaned sections. `concepts/model-providers`, `gateway/configuration-reference`/`configuration`, `cli/models`, the
media tools (`image-generation`/`video-generation`/`music-generation`/`media-overview`), and `providers/anthropic` /
`providers/openai` cross-references are LINKED (their own pages own them), not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are single-BB (procedure: install → auth → config → verify) and under the 2,500-word cap (max `comfy` = 1,264w). No mixed-BB or oversized page; 1 note per page. `comfy`'s 14 code fences are condensed to ≤6 in the digest (config snippets reproduced selectively) — a density measure, not a split. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (4,358 words, 44 code fences). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (every page is a provider setup guide). No concept/model/argument notes in this sub-plan.
- Est. digest words: ~3,570 (avg ~510/note; range 320–700). All notes ≤700w, ≤6 code blocks, single BB — none near caps.
- Cross-refs (LOCKED at xref-augment 2026-06-21, raised floors): each note carries **≥8 relevance-selected
  9t/10s/11d · cloudflare 9t/10s/11d · cohere 8t/10s/10d · comfy 8t/10s/11d · deepgram 8t/10s/11d · deepinfra 10t/10s/11d.
  `## Per-Note Related Notes Mapping (LOCKED)` for the full per-link relevance statements.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> docs; sibling `oc_*` docs (this series, not yet authored) are marked "(planned, this series)" and count toward the
> ≥10-doc floor only as additions on top of the ≥5 existing. `entry_openclaw_docs` is "(planned, master W1)". Relative
> paths are from `resources/documentation/openclaw/oc_*.md`: term → `../../term_dictionary/`, snippet →
> `../../code_snippets/`, sibling oc_ → `oc_*.md`, cc/pi/hermes/aws docs → `../<folder>/`, repo →
> `../../../areas/code_repos/`.

### oc_providers_chutes (10t · 10s · 11d)

**Terms** (10)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: `chutes` is an OpenClaw provider plugin, the host system this page configures.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Chutes exposes open-source LLM catalogs (GLM, DeepSeek, Kimi, Qwen) through its API.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: Chutes onboarding supports a browser OAuth flow (`--auth-choice chutes`).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential issued by OAuth; relevance: `CHUTES_OAUTH_TOKEN` carries the runtime credential and auto-refreshes.
- [Authentication](../../term_dictionary/term_authentication.md) — identity-verification step; relevance: the page is half auth setup (OAuth vs API key, `CHUTES_API_KEY`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider integration; relevance: `@openclaw/chutes-provider` is the plugin installed and restarted.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the registry of usable model refs; relevance: Chutes uses live catalog discovery with a static fallback catalog.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI APIs; relevance: Chutes is an external aggregator service OpenClaw routes to.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — open-source LLM family; relevance: the Chutes catalog and `chutes-pro` alias map to `DeepSeek-V3.2-TEE`.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored per-provider credential profile; relevance: Chutes OAuth tokens auto-refresh through OpenClaw auth profiles.

- [Pi — Provider Authentication](../pi/pi_provider_auth.md) — Pi's API-key/auth-file resolution order; relevance: same subscription-OAuth-vs-API-key tradeoff Chutes presents.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — configuring cloud-hosted providers in a sibling harness; relevance: parallel provider config-block shape.
- [Claude Code — Authentication](../claude_code/cc_authentication.md) — OAuth-vs-key login for a coding agent; relevance: same auth-choice decision a Chutes user makes.
- [Hermes — Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM provider setup in a sibling harness; relevance: directly analogous OpenAI-compatible-provider onboarding.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — how a new provider plugin is registered; relevance: the code-side counterpart to installing `chutes-provider`.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin contract; relevance: explains what a provider plugin like Chutes registers.
- [Hermes — Provider/Auth/Tool Env Vars](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — env-var reference for provider auth; relevance: same `*_API_KEY` / `*_OAUTH_TOKEN` env pattern.
- [Hermes — Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — fallback-on-failure provider config; relevance: parallel to Chutes' discovery-fails→static-catalog fallback.
- [oc_providers_deepinfra](oc_providers_deepinfra.md) — fellow OpenAI-compatible aggregator provider (planned, this series); relevance: same unified-API + live-discovery pattern.
- [oc_providers_cohere](oc_providers_cohere.md) — fellow OpenAI-compatible chat provider (planned, this series); relevance: same install→key→config flow.

**Repos** (4)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider plugin source; relevance: implements the `chutes` provider documented here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent defaults + auth-profile + model-catalog code; relevance: owns auth-profile refresh + catalog registration Chutes uses.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the `openclaw onboard` wizard; relevance: implements `--auth-choice chutes` / `chutes-api-key`.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella OpenClaw repo; relevance: parent project of the gateway and provider plugins.

- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — the OpenAI-compatible provider implementation; relevance: Chutes is OpenAI-compatible and goes through this code path.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator-provider routing; relevance: Chutes is an open-source-catalog aggregator like OpenRouter.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog registration/lookup; relevance: implements the live-discovery + static-fallback catalog Chutes registers.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias resolution; relevance: maps the `chutes-fast`/`chutes-pro`/`chutes-vision` aliases.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-entry registration; relevance: how `@openclaw/chutes-provider` is installed and entered.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding wizard config writing; relevance: `openclaw onboard --auth-choice chutes` writes provider config.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config load at gateway startup; relevance: gateway restart re-reads the chutes plugin entry.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — sibling-harness aggregator provider; relevance: parallel open-catalog aggregator implementation.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: mirrors Chutes' OAuth-vs-key resolution.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: parallel to how OpenClaw registers the chutes provider id.

### oc_providers_claude_max_api_proxy (9t · 10s · 11d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: the page configures OpenClaw to point at the proxy via `OPENAI_BASE_URL`.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the proxy exposes a Claude Max/Pro subscription as an endpoint.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's CLI coding agent; relevance: the proxy wraps `claude -p` / Claude Code CLI to convert format.
- [Authentication](../../term_dictionary/term_authentication.md) — credential setup; relevance: the proxy reuses the authenticated Claude CLI login (`claude --version`).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer subscription credential; relevance: the subscription login the CLI holds is the credential the proxy reuses.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server forwarding requests to an upstream; relevance: `claude-max-api-proxy` is a local reverse proxy fronting the Claude CLI.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the proxy serves Claude LLM completions in OpenAI format.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: OpenClaw treats the proxy as a custom OpenAI-compatible provider entry.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI endpoints; relevance: the proxy is a community, non-official third-party tool.

- [Claude Code — Authentication](../claude_code/cc_authentication.md) — Claude CLI login mechanics; relevance: the proxy requires an authenticated Claude CLI login.
- [Claude Code — Login & Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — subscription `claude -p` billing + login issues; relevance: the page's billing warning + login dependency map here.
- [Claude Code — Proxy & Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — pointing a coding agent at a proxy/gateway base URL; relevance: same `OPENAI_BASE_URL` redirection pattern.
- [Claude Code — Authentication & Network Errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network failure modes; relevance: proxy + subscription auth failure surface.
- [Pi — Provider Authentication](../pi/pi_provider_auth.md) — subscription-vs-API-key auth tradeoff; relevance: the "Why use this?" cost-route table makes the same tradeoff.
- [Hermes — Nous Portal Subscription](../hermes_agent/hermes_nous_portal_subscription.md) — subscription-as-endpoint pattern in a sibling harness; relevance: directly parallel subscription-credential-as-provider approach.
- [Hermes — Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — proxy-URL routing for providers; relevance: same local-proxy `/v1` route shaping.
- [Hermes — Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider config; relevance: the OpenAI-compatible custom-endpoint setup the proxy needs.
- [oc_providers_cloudflare_ai_gateway](oc_providers_cloudflare_ai_gateway.md) — the other Anthropic-routing path (planned, this series); relevance: gateway-fronted vs subscription-fronted Claude access.
- [oc_providers_chutes](oc_providers_chutes.md) — fellow custom OpenAI-compatible endpoint (planned, this series); relevance: same `OPENAI_BASE_URL` provider-entry shape.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — OpenClaw LLM-provider plugins; relevance: where a custom OpenAI-compatible endpoint provider lives.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: hosts the gateway env/config the proxy is wired into.

- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — the native Anthropic provider impl; relevance: contrasts the native path with the proxy path the page documents.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider impl; relevance: OpenClaw consumes the proxy through this OpenAI-compatible code path.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — proxy-URL base resolution; relevance: same `OPENAI_BASE_URL`→localhost proxy redirection.
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — Anthropic endpoint resolution; relevance: the proxy converts to Claude CLI which talks Anthropic endpoints.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — sibling Anthropic provider plugin; relevance: parallel Claude-provider integration.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — API-mode (OpenAI vs Anthropic) resolution; relevance: the proxy forces OpenAI-mode shaping (no service_tier/cache hints).
- [snippet_hermes_agent_core_auxiliary_headers](../../code_snippets/snippet_hermes_agent_core_auxiliary_headers.md) — attribution-header injection; relevance: the page notes OpenClaw attribution headers are NOT injected on the proxy URL.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom OpenAI-compatible provider; relevance: the proxy is registered as a custom `/v1` backend.
- [snippet_hermes_agent_cli_nous_subscription](../../code_snippets/snippet_hermes_agent_cli_nous_subscription.md) — subscription-credential CLI flow; relevance: parallel subscription-as-credential onboarding.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local `localhost` provider endpoint; relevance: same localhost-base-URL custom-endpoint pattern (`http://localhost:3456/v1`).

### oc_providers_cloudflare_ai_gateway (9t · 10s · 11d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: the page configures the `cloudflare-ai-gateway` OpenClaw provider.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a managed front door for backend APIs; relevance: Cloudflare AI Gateway is exactly an AI-API gateway adding analytics/caching/controls.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding server; relevance: the Gateway sits in front of and forwards to the Anthropic Messages API.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: the default model is `cloudflare-ai-gateway/claude-sonnet-4-6` over the Anthropic Messages API.
- [Authentication](../../term_dictionary/term_authentication.md) — credential setup; relevance: dual auth — provider API key plus the `cf-aig-authorization` Gateway header.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — caching of model inputs to cut cost/latency; relevance: the Gateway adds caching (and analytics) in front of the provider.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Gateway routes LLM (Claude) requests.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: `@openclaw/cloudflare-ai-gateway-provider` is the plugin installed.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — managed set of provider credentials; relevance: the daemon-env-var caveat is about making the Gateway/provider key reachable to the service.

- [Claude Code — LLM Gateway](../claude_code/cc_llm_gateway.md) — routing a coding agent through an LLM gateway; relevance: directly analogous gateway-in-front-of-provider setup.
- [Claude Code — LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — a concrete gateway proxy with analytics; relevance: same gateway-adds-analytics/caching value prop.
- [Claude Code — Proxy & Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway base-URL + header config; relevance: same `cf-aig-authorization` header + base-URL pattern.
- [Claude Code — Amazon Bedrock Mantle Endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — corporate-endpoint override for Claude; relevance: parallel "route Anthropic through an alternate gateway endpoint".
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — documents Cloudflare AI Gateway (with BYOK upstream-auth modes); relevance: the exact same Cloudflare AI Gateway provider in a sibling harness.
- [Hermes — Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing through proxies/gateways; relevance: same gateway-routing config surface.
- [Hermes — Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — a gateway abstraction in a sibling harness; relevance: parallel gateway-fronting design.
- [Hermes — Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider config including gateways; relevance: where gateway-fronted providers are configured.
- [oc_providers_claude_max_api_proxy](oc_providers_claude_max_api_proxy.md) — the other Anthropic-routing path (planned, this series); relevance: gateway-fronted vs subscription-proxy access to Claude.
- [oc_providers_deepinfra](oc_providers_deepinfra.md) — fellow API-key provider (planned, this series); relevance: same daemon-env-var key-availability caveat.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the OpenClaw gateway daemon; relevance: the daemon-env-var caveat (`~/.openclaw/.env`) is about this process.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider plugins; relevance: implements the `cloudflare-ai-gateway` provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: parent project of the gateway/provider plumbing.

- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — native Anthropic provider impl; relevance: the Gateway routes the Anthropic Messages API, the same upstream this implements.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway auth at startup; relevance: where the daemon reads `CLOUDFLARE_AI_GATEWAY_API_KEY`.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — gateway auth-ticket handling; relevance: parallel header/credential auth flow for the gateway.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config load at gateway startup; relevance: gateway restart loads the cloudflare-ai-gateway plugin entry.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator/gateway-style routing; relevance: parallel "route requests through an intermediary endpoint".
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — Anthropic endpoint resolution; relevance: the Gateway base URL replaces the Anthropic endpoint.
- [snippet_hermes_agent_core_auxiliary_headers](../../code_snippets/snippet_hermes_agent_core_auxiliary_headers.md) — custom-header injection; relevance: the `cf-aig-authorization: Bearer` header is added here.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — sibling Anthropic provider plugin; relevance: parallel Claude-via-endpoint integration.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider routing; relevance: gateway-fronted custom-endpoint registration.
- [snippet_hermes_agent_core_anthropic_adapter_normalization](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_normalization.md) — Anthropic payload normalization; relevance: the page's "strip trailing assistant prefill with extended thinking" is exactly this normalization concern.

### oc_providers_cohere (8t · 10s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: `cohere` is an OpenClaw provider configured here.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Cohere serves Command A LLM inference.
- [Authentication](../../term_dictionary/term_authentication.md) — credential setup; relevance: `COHERE_API_KEY` / `--auth-choice cohere-api-key` onboarding.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: bundled-during-transition + external `@openclaw/cohere-provider` package.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Cohere's Compatibility API is the external service.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model-ref registry; relevance: `openclaw models list --provider cohere` shows the Command A catalog.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — selecting/routing among providers; relevance: default model set "only when no primary model is already configured".

- [Claude Code — Model Selection](../claude_code/cc_model_selection.md) — choosing/setting the primary model; relevance: same "set default model only if none configured" behavior.
- [Pi — Custom Models](../pi/pi_custom_models.md) — config-file provider/model definition; relevance: the environment-only `model.primary: cohere/command-a-03-2025` setup.
- [Pi — Provider Authentication](../pi/pi_provider_auth.md) — provider auth resolution; relevance: the daemon/Docker key-availability caveat the page raises.
- [Pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: bundled→external-plugin transition mirrors custom-provider registration.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud-hosted provider config block in a sibling harness; relevance: parallel provider config-block shape for the environment-only `cohere` provider entry.
- [Hermes — Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider onboarding; relevance: directly analogous OpenAI-compatible-provider setup.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — registering a new provider; relevance: installing/restarting for the external Cohere package.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin contract; relevance: the contract the bundled/external `@openclaw/cohere-provider` plugin registers against.
- [Hermes — Provider/Auth/Tool Env Vars](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env-var reference; relevance: `COHERE_API_KEY` daemon-env availability.
- [oc_providers_chutes](oc_providers_chutes.md) — fellow OpenAI-compatible provider (planned, this series); relevance: same install→key→config→verify flow.
- [oc_providers_deepinfra](oc_providers_deepinfra.md) — fellow OpenAI-compatible aggregator (planned, this series); relevance: parallel unified-API onboarding.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider plugins; relevance: implements the bundled/external `cohere` provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: hosts the gateway the Cohere key must reach.

- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider impl; relevance: Cohere uses the `openai-completions` Compatibility API through this path.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog registration; relevance: registers the Command A catalog `openclaw models list` shows.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-entry registration; relevance: how the bundled/external cohere plugin is entered.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding config writing; relevance: `openclaw onboard --auth-choice cohere-api-key` writes config.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config load at startup; relevance: `gateway restart` re-reads the cohere plugin entry.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: parallel registry that registers a cohere-style provider id.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: mirrors `--cohere-api-key` / env-var resolution.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom OpenAI-compatible provider; relevance: the Compatibility-API base-URL provider shape.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — CLI provider registry; relevance: parallel to `openclaw models list --provider cohere`.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — bundled multi-vendor provider cluster; relevance: parallel bundled-then-external provider packaging.

### oc_providers_comfy (8t · 10s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: `comfy` is a bundled OpenClaw plugin configured here.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: the bundled `comfy` plugin registers image/video/music surfaces.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative image/video model; relevance: ComfyUI graphs run diffusion image models (FLUX) the plugin drives.
- [Stable Diffusion](../../term_dictionary/term_stable_diffusion.md) — the canonical open diffusion image model; relevance: ComfyUI is the node-graph UI built around Stable-Diffusion-family workflows.
- [Authentication](../../term_dictionary/term_authentication.md) — credential setup; relevance: none for local, `COMFY_API_KEY`/`COMFY_CLOUD_API_KEY` for Comfy Cloud.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model-ref registry; relevance: registers the single `comfy/workflow` model across capabilities.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI APIs; relevance: Comfy Cloud is the external hosted mode.
- [Sandbox](../../term_dictionary/term_sandbox.md) — network/resource isolation boundary; relevance: `allowPrivateNetwork` governs LAN/private base URLs in cloud mode.

- [Hermes — Image Generation](../hermes_agent/hermes_image_generation.md) — image-generation tool/provider; relevance: Comfy's `image_generate` surface in a sibling harness.
- [Hermes — Video Generation Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider plugin; relevance: Comfy's `video_generate` surface analog.
- [Hermes — Platform Media Tools Reference](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool reference; relevance: the shared media tools Comfy plugs into.
- [Hermes — Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media config surface; relevance: how generated media is delivered/configured.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — custom-provider config-block shape; relevance: the nested `plugins.entries.comfy.config` block shape.
- [Pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: how a bundled media provider plugin is registered.
- [oc_providers_deepinfra](oc_providers_deepinfra.md) — also exposes image/video-gen surfaces (planned, this series); relevance: alternative provider for the same media surfaces.
- [oc_tools_image_generation](oc_tools_image_generation.md) — the image-generation tool doc (planned, link-out, to05/to06 series); relevance: owns the generic image-gen tool config Comfy backs.
- [oc_tools_video_generation](oc_tools_video_generation.md) — the video-generation tool doc (planned, link-out); relevance: owns the generic video-gen tool config.
- [oc_tools_music_generation](oc_tools_music_generation.md) — the music-generation tool doc (planned, link-out); relevance: owns the `music_generate` tool Comfy registers.

**Repos** (3)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extensions source; relevance: hosts the bundled `comfy` plugin code.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-plugin source; relevance: where the comfy provider surfaces are registered.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: parent project of the bundled media plugin.

- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool impl; relevance: the `image_generate` surface Comfy backs.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-generation tool impl; relevance: the `video_generate` surface Comfy backs.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch; relevance: how an image-gen workflow request is routed to a provider plugin.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: how a video-gen request is routed.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media output pipeline; relevance: how generated image/video output is downloaded/delivered (output-node read).
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: the reference-image input + generated-output media handling.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-entry registration; relevance: `plugins.entries.comfy` is the entry shape documented.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config load; relevance: the nested per-capability config block is loaded here.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog registration; relevance: registers the `comfy/workflow` model.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision/media dispatch; relevance: parallel media-capability dispatch for reference-image editing.

### oc_providers_deepgram (8t · 10s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: Deepgram is wired into OpenClaw's media + Voice Call surfaces.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text transcription; relevance: Deepgram is the STT provider for inbound voice notes (`nova-3`).
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony/voice-call channel; relevance: Deepgram streaming STT powers Voice Call (`plugins.entries.voice-call`).
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: streaming STT forwards frames over Deepgram's `listen` WebSocket.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live partial/final transcript emission; relevance: streaming mode emits interim + final transcripts as Deepgram returns them.
- [Authentication](../../term_dictionary/term_authentication.md) — credential setup; relevance: `DEEPGRAM_API_KEY` (with config-path fallback) is the standard auth order.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: the bundled `deepgram` plugin registers batch + streaming providers.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — text→audio synthesis; relevance: the sibling media surface in the same Voice Call / media pipeline.

- [Hermes — STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription setup; relevance: directly analogous STT-provider config (batch transcription).
- [Hermes — TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the sibling speech surface in the same media subsystem.
- [Hermes — Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode operation; relevance: the realtime-voice pathway Deepgram streaming serves.
- [Hermes — Voice Gateway (Discord VC)](../hermes_agent/hermes_voice_gateway_discord_vc.md) — realtime voice over a channel; relevance: parallel realtime-audio-stream → transcript flow.
- [Hermes — Platform Media Tools Reference](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool reference; relevance: `tools.media.audio` config surface Deepgram batch transcription uses.
- [Claude Code — Voice Dictation](../claude_code/cc_voice_dictation.md) — speech-to-text in a coding agent; relevance: parallel STT-into-input pipeline.
- [Pi — Provider Authentication](../pi/pi_provider_auth.md) — provider auth resolution order; relevance: the page's "standard provider auth order" note.
- [oc_providers_deepinfra](oc_providers_deepinfra.md) — also offers STT (Whisper) (planned, this series); relevance: alternative STT provider for the same media surface.
- [oc_tools_media_overview](oc_tools_media_overview.md) — media tools overview (planned, link-out, to05); relevance: owns the audio/image/video pipeline Deepgram plugs into.
- [oc_plugins_voice_call](oc_plugins_voice_call.md) — Voice Call plugin internals (planned, link-out, pl21); relevance: owns the `voice-call` streaming config Deepgram fills.

**Repos** (4)
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension source; relevance: implements the Deepgram STT provider documented here.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony/Voice Call channel; relevance: forwards 8 kHz G.711 u-law (Twilio) frames Deepgram streaming consumes.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extensions source; relevance: hosts the bundled `deepgram` plugin.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: parent project of the media/Voice Call subsystem.

- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — the Deepgram STT implementation; relevance: this IS the code behind the page (exact provider).
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — Voice Call streaming transcription; relevance: the streaming-STT path the page's `voice-call.config.streaming` block drives.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — Voice Call audio framing; relevance: the G.711 u-law / 8 kHz frames forwarded to Deepgram.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — streaming admission control; relevance: gates streaming-STT session start (endpointing/interim).
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: relays partial/final transcripts into the reply pipeline.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — Voice Call session manager; relevance: orchestrates the Deepgram streaming provider lifecycle.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — Voice Call runtime; relevance: the runtime hosting the streaming STT provider.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — sibling-harness transcription tool; relevance: parallel batch-transcription implementation.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the realtime-voice surface Deepgram streaming serves.

### oc_providers_deepinfra (10t · 10s · 11d)

**Terms** (10)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: DeepInfra is an OpenClaw unified provider configured here.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: DeepInfra's unified API fronts the top open-source LLMs.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: `@openclaw/deepinfra-provider` registers all matching surfaces.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model-ref registry; relevance: chat/image/video catalogs refresh live from `/v1/openai/models`.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI APIs; relevance: DeepInfra is the external unified aggregator service.
- [Authentication](../../term_dictionary/term_authentication.md) — credential setup; relevance: single `DEEPINFRA_API_KEY` unlocks live discovery across surfaces.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — open-source LLM family; relevance: default model is `deepinfra/deepseek-ai/DeepSeek-V4-Flash`.
- [Qwen](../../term_dictionary/term_qwen.md) — open-source LLM family; relevance: example ref `deepinfra/Qwen/Qwen3-Max` in the model-ref docs.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text; relevance: STT surface default `openai/whisper-large-v3-turbo`.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative image/video model; relevance: image-gen default `FLUX-1-schnell`, video-gen `Pixverse-T2V`.

- [Pi — Custom Models](../pi/pi_custom_models.md) — config-file provider/model definition; relevance: the `deepinfra/<provider>/<model>` ref format + primary-model config.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud-provider config block; relevance: parallel unified-API provider config.
- [Claude Code — Model Selection](../claude_code/cc_model_selection.md) — choosing the primary model; relevance: the `agents.defaults.model` selection DeepInfra populates.
- [Hermes — Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider onboarding; relevance: directly analogous unified-provider setup.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin contract; relevance: the multi-surface contracts DeepInfra registers against.
- [Hermes — STT Transcription](../hermes_agent/hermes_stt_transcription.md) — STT provider config; relevance: DeepInfra's Whisper STT surface.
- [Hermes — TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider config; relevance: DeepInfra's Kokoro TTS surface (`messages.tts.provider`).
- [Hermes — Image Generation](../hermes_agent/hermes_image_generation.md) — image-gen provider; relevance: DeepInfra's FLUX image-gen surface.
- [oc_providers_chutes](oc_providers_chutes.md) — fellow open-catalog aggregator (planned, this series); relevance: same live-discovery + static-fallback pattern.
- [oc_providers_deepgram](oc_providers_deepgram.md) — STT provider DeepInfra's Whisper surface subsumes (planned, this series); relevance: alternative STT provider.

**Repos** (4)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider plugins; relevance: implements the `deepinfra` provider.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extensions source; relevance: hosts the multi-surface DeepInfra plugin.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella OpenClaw repo; relevance: parent project of the provider/gateway plumbing.

- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider impl; relevance: DeepInfra is OpenAI-compatible and uses this code path.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator-provider routing; relevance: DeepInfra is a unified/aggregator router like OpenRouter.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog registration/discovery; relevance: implements the live `/v1/openai/models` discovery + static fallback.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model-ref/alias resolution; relevance: resolves `deepinfra/<provider>/<model>` refs.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — sibling aggregator provider; relevance: parallel unified-API aggregator implementation.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — cloud unified-provider plugin; relevance: parallel single-key-unlocks-many-models provider.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: DeepInfra's image-gen surface (FLUX).
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: DeepInfra's video-gen surface (Pixverse).
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: DeepInfra's Whisper STT surface.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: DeepInfra's Kokoro TTS surface routing.

## Undigested Terms Plan

Per master: OpenClaw provider vocabulary is digested as `oc_*` doc notes (the page IS the subject); the only
`term_dictionary` interaction is LINKING existing terms. **Expected new `term_dictionary` captures: 0.**

| Term | Disposition |
|------|-------------|
| Chutes / DeepInfra / Cohere / ComfyUI / Deepgram / Cloudflare AI Gateway / claude-max-api-proxy (provider names) | Documented AS the `oc_providers_*` doc notes (subject of each page). NOT promoted to `term_dictionary`. |
| Model/family names: GLM, DeepSeek, Kimi, Mistral-Small, Qwen, Command A, FLUX, Claude Opus/Sonnet/Haiku, Nova | Config values, not terms. Link existing `term_llm` / `term_claude` / `term_deepseek` / `term_qwen`. No new captures. |
| OpenAI-compatible API / Compatibility API / unified API | Documented inline as provider properties. Link `term_llm` / `term_provider_plugin`. No new capture. |
| OAuth / API key / auth-choice / onboarding / auth profile | Link existing `term_oauth`, `term_oauth_token`, `term_authentication`, `term_auth_profile`. No new capture. |
| AI gateway / reverse proxy / `cf-aig-authorization` / BYOK | Link existing `term_api_gateway`, `term_reverse_proxy`. No new capture. |
| Speech-to-text / streaming STT / G.711 u-law / endpointing | Link existing `term_speech_to_text`, `term_websocket`, `term_voice_call`. No new capture. |
| Workflow JSON / promptNodeId / outputNodeId / image-video-music generation | Documented inline as `comfy` config keys. Link existing `term_diffusion_model`. No new capture. |
| Live discovery / static catalog / model refs / aliases | Documented inline as provider behavior. Link existing `term_model_catalog`. No new capture. |
| Prompt caching (Cloudflare analytics/caching; prefill-stripping) | Link existing `term_prompt_caching`. No new capture. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term with no existing note appears in these 7
pages — speech/media/gateway/auth vocabulary all map to existing `term_dictionary` notes (verified present:
`term_speech_to_text`, `term_text_to_speech`, `term_voice_call`, `term_diffusion_model`, `term_api_gateway`,
`term_reverse_proxy`, `term_prompt_caching`, `term_model_catalog`, `term_provider_plugin`). Augment Step 2d re-scans to
confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. (If augment's Step 2d re-scan surfaces a
genuinely reusable cross-cutting term with no existing note, the master's requirement applies: capture via

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). All 8 gates must PASS before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format (YAML field order + body H2 sections + footer) | `scripts/check_note_format.py` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (no claim absent from source) | diff each note vs `inbox/openclaw_docs/providers/<page>.md` |
| G3 | Density + Coverage (≤400 lines / ≤2,500 words / ≤6 code; every H2/H3 mapped) | `wc` + section-coverage-map audit |
| G4 | Cross-Reference (≥6 relevance-selected terms + repo/sibling/doc links, each indexed) | `note_links` query after reindex |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` (0 broken) |
| G7/G8 | Discoverability — each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) | satisfied via `entry_openclaw_docs.md` + repo/term inlinks; verify `in_degree` |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_chutes oc_providers_claude_max_api_proxy oc_providers_cloudflare_ai_gateway oc_providers_cohere oc_providers_comfy oc_providers_deepgram oc_providers_deepinfra"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  grep -qE "$REQ_SECTIONS" "$f" || echo "MISSING required section in $n"
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_ link
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO sibling $SIBLING_PREFIX link in $n"
  # density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Code in note (cap 6) | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_providers_chutes | procedure | 480 | 4 | ≤4 | ✅ |
| 2 | oc_providers_claude_max_api_proxy | procedure | 560 | 6 | ≤5 (drop the verbose LaunchAgent plist or trim) | ✅ |
| 3 | oc_providers_cloudflare_ai_gateway | procedure | 470 | 6 | ≤5 | ✅ |
| 4 | oc_providers_cohere | procedure | 320 | 4 | ≤4 | ✅ |
| 5 | oc_providers_comfy | procedure | 700 | 14 | ≤6 (reproduce one local + one cloud config + key tables; collapse duplicate `comfy/workflow` model snippets) | ✅ |
| 6 | oc_providers_deepgram | procedure | 560 | 5 | ≤5 | ✅ |
| 7 | oc_providers_deepinfra | procedure | 480 | 5 | ≤5 | ✅ |

No note approaches the 2,500-word / 400-line caps. Only `comfy` (14 source fences) and `claude-max-api-proxy` (verbose
plist) need selective code reproduction to stay ≤6 — both achievable without losing load-bearing config; not a split trigger.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before the first sub-plan executes)
under the **Providers** section/cluster — one row per `oc_providers_*` note (filename + 1-line description). Each new note
RECEIVES its back-link from `entry_openclaw_docs.md` at finalization, satisfying G7/G8 (≥1 outside-folder inbound link).
No new top-level entry point is created by this sub-plan (the master owns `entry_openclaw_docs.md` and the W2/W3 parent-hub
wiring).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; all sources confirmed present 2026-06-20):

- `entry_openclaw_docs.md` (planned, master W1) → **all 7** notes (primary G8 satisfier).
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 2, 3, 4, 7 (LLM/chat providers).
- `repo_openclaw_extensions_voice_speech.md` → note 6 (Deepgram STT).
- `repo_openclaw_extensions.md` → notes 5, 6, 7 (bundled `comfy`/`deepgram`/`deepinfra` plugins).
- `repo_openclaw_gateway.md` → note 3 (Cloudflare AI Gateway).
- `repo_openclaw_channels_voice_phone.md` → note 6 (Voice Call streaming STT).
- `term_openclaw.md` → all 7; `term_speech_to_text.md` → note 6; `term_api_gateway.md` → note 3;
  `term_claude.md` → note 2; `term_diffusion_model.md` → note 5; `term_deepseek.md` → notes 1, 7.
- `pi_cloud_providers.md` / `pi_provider_auth.md` (sibling-tool provider docs) → reciprocal links to notes 1–4, 7.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates PASS before commit. Re-read each source page; reproduce config snippets verbatim
(selectively for `comfy`/`claude-max-api-proxy` to stay ≤6 code blocks). One BB per note (all procedure). Cap
dynamic-workflow fan-out at ~30 agents/run; reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1
before commit; `git pull --rebase --autostash` first; no Claude co-author trailer; commit + push after the phase.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment; per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** (9/9 PASS — READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this pass:** xref-augment — re-read all 7 source pages under `inbox/openclaw_docs/providers/`, then built
and LOCKED a per-note Related Notes mapping at the RAISED floors (**≥8 terms · ≥10 snippets · ≥10 docs per note**),
replacing the PLAN-stage `## Candidate Cross-References` section with `## Per-Note Related Notes Mapping (LOCKED)`.

**What was locked (per-note counts; floors met):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_providers_chutes | 10 | 10 | 11 (8/3) | 4 | ✅ |
| oc_providers_claude_max_api_proxy | 9 | 10 | 11 (8/3) | 3 | ✅ |
| oc_providers_cloudflare_ai_gateway | 9 | 10 | 11 (8/3) | 3 | ✅ |
| oc_providers_cohere | 8 | 10 | 10 (7/3) | 3 | ✅ |
| oc_providers_comfy | 8 | 10 | 11 (6/5) | 3 | ✅ |
| oc_providers_deepgram | 8 | 10 | 11 (7/4) | 4 | ✅ |
| oc_providers_deepinfra | 10 | 10 | 11 (8/3) | 4 | ✅ |

- **DB-verify:** every cited EXISTING note_id (all terms, ALL 70 snippet citations, all existing docs, all repos) was
  planned (`oc_*` siblings in this series + `oc_tools_*`/`oc_plugins_*` link-outs + `entry_openclaw_docs`, all marked).
  exact `snippet_openclaw_speech_deepgram_stt` + the full `voice_call_media_stream_*` set; Comfy/DeepInfra draw on the
  hermes `tools_image_gen` / `tools_video_gen` / `plugins_*_gen_dispatch` media corpus).
  `hermes_agent/`, `pi/`, `claude_code/` coding-agent doc corpora; sibling `oc_*` (this series) added only on top.
- **Source re-read (CP7):** measured word counts match the plan's Source table exactly — chutes 570, claude-max 722,
  cloudflare 463, cohere 283, comfy 1264, deepgram 617, deepinfra 439 = **4,358 total** (= plan's measured total). No
  under-estimation; no re-split triggered (all single-BB procedure, all <2,500w; comfy 1,264w is the max).

**New-term candidates:** **none.** Re-scan of all 7 pages (Step 2d) confirms every provider/auth/gateway/speech/media
`term_oauth_token`, `term_authentication`, `term_provider_plugin`, `term_model_catalog`,
`term_third_party_genai_services`, `term_deepseek`, `term_auth_profile`, `term_claude`, `term_claude_code`,
`term_reverse_proxy`, `term_api_gateway`, `term_prompt_caching`, `term_credential_pool`, `term_provider_routing`,
`term_voice_call`, `term_websocket`, `term_realtime_transcription`, `term_text_to_speech`, `term_qwen`). Provider names
(Chutes, DeepInfra, Cohere, ComfyUI, Deepgram, Cloudflare AI Gateway, claude-max-api-proxy) are the SUBJECTS of the
`oc_providers_*` doc notes per the master's design decision — not promoted to `term_dictionary`. **Expected new
`term_dictionary` captures: 0** (unchanged from plan). Best-fit glossary if any term WERE captured: the agentic/LLM
glossary (`0_entry_points/acronym_glossary_*` agentic-dev) — N/A this pass.

**Issues / watch-items for execution:** none blocking. (1) `comfy` has only 6 existing docs vs others' 7-8 — still meets
the ≥5-existing floor; media-gen doc vocabulary is thinner in the vault, padded to the ≥10 floor with relevant link-out
`oc_tools_*` + sibling `oc_providers_deepinfra`. (2) Two link-out targets (`oc_tools_*`, `oc_plugins_voice_call`) are in
OTHER sub-plans (to05/to06, pl21) — they will not exist until those sub-plans execute; rendered as planned link-outs,
execution if those siblings haven't landed yet.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of `plan_digest_openclaw_docs_pr02.md` (status: pending at review start).

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link-fix, G7/G8 discoverability — single phase, all gates present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at master W1) | **PASS** | `## Entry Point Decision` inherits master W1 CREATE of `entry_openclaw_docs.md` (>30-note series → CREATE required); contributes 7 Providers rows; each note's mapping carries the `entry_openclaw_docs` back-link. |
| CP4 | Plan size (≤30 or split) | **PASS** | 7 notes — well under 30; sub-plan of a master+sub-plan structure. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited from master, derived from existing `pi/`+`cc/` doc notes; verified `pi_cloud_providers.md` YAML field order (`tags → keywords → topics → language → date of note → status → building_block → source_url → access_control_group`) + `## Overview`/`## Related Notes` body convention match the master Format Definition. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: max is comfy 1,264w/≤6 code (selective reproduction) — no note near 2,500w/400-line/6-code caps; no borderline; no split needed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 7 pages 2026-06-21: 570/722/463/283/1264/617/439 = 4,358w, EXACTLY matching the plan's measured Source table. Ratio 1.0; no >1.5× under-estimation. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned: provider names → doc notes; model/auth/media vocab → link existing terms); `## Term-Note Authoring Requirements` present (N/A — 0 new terms — with inherited-from-master capture fallback if Step 2d surfaces one). |
| CP8f | Slug specificity + all-notes collision audit | **PASS** | 0 new term slugs → no specificity renames needed. Doc-note collision audit: all 7 `oc_providers_*` slugs checked vs `term_dictionary/` + `resources/documentation/` — no existing note duplicates a planned `oc_providers_*` (provider docs are net-new; code side is `repo_openclaw*`, LINKED not duplicated). |
| CP9 | Discoverability / inlinks (G8, no islands) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound source (`entry_openclaw_docs` → all 7; `repo_openclaw_extensions_*` → relevant notes; term/`pi_*` reciprocal links); G8 in the gate table; inlinks marked as an executed/verified step (in-degree ≥1 before commit). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
