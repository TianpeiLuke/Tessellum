---
title: Hermes Agent Docs Digestion — Sub-Plan 14 — Inference Providers & Integrations
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/integrations/
pages:
  - integrations/providers.md
  - integrations/nous-portal.md
  - integrations/index.md
---

# Sub-Plan 14: Inference Providers & Integrations

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP14's note
> filenames/BBs/coverage are defined.

## Scope

"Inference Providers & Integrations" — how Hermes Agent connects to an LLM and to external systems.
Source = 3 mirrored pages in `inbox/hermes_agent_docs/integrations/`. **P1 / foundational** — every
other sub-plan assumes a provider is configured; `providers.md` is the single largest integrations
page (~9.5K words, 87 code blocks) and MUST split by provider class. SP14 OWNS the `term_nous_portal`
capture (the Nous subscription / Tool-Gateway billing concept used corpus-wide, 25+ pages). Downstream
sub-plans link back to `hermes_inference_providers_cloud`, `hermes_local_self_hosted_llm`, and
`hermes_nous_portal_subscription`.

## Content Strategy

- **One BB per note.** `providers.md` mixes (a) the cloud/first-class API-key provider catalog,
  (b) local & self-hosted servers + WSL2 networking, and (c) custom/named providers + multi-provider
  proxies + OpenRouter routing/fallback/context-length detection → split into 3 procedure notes by
  provider class (see Split Decisions). `nous-portal.md` → 1. `integrations/index.md` → 1 (navigation).
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content:
  provider-routing/fallback/credential-pool *feature internals* (SP09), the Tool Gateway feature page
  (SP05), config.yaml model/aux blocks (SP02), per-provider setup *guides* (SP15: ollama/gemini/grok/
  minimax/bedrock/azure/nemotron/nous-portal), web-search backends (SP08), MCP (SP09), ACP (SP09/18),
  API server (SP09), memory providers (SP05), messaging platforms (SP11-13).
- **Collision (augment): `term_nous_portal` does NOT exist; the LIKE hits (`term_api_gateway`,
  `term_mcp_gateway`, `term_nat_gateway`, `term_agentcore_gateway`, `term_authportal`) are ALL
  different concepts** (AWS/network/MCP gateways, a generic auth portal) — classic master-caution
  false-positives confirmed by reading the slugs. SP14 CAPTURES `term_nous_portal`.
- **Most provider names are products, not concepts** — OpenRouter, vLLM, Ollama, AWS Bedrock, Gemini,
  Groq, etc. are link-only references inside notes. `term_vllm` EXISTS (active) → LINK it; the rest are
  product names cited inline, not standalone term captures.

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| integrations/providers.md | 9458 | 87 | MIXED procedure (3 provider classes) | 3 (split) |
| integrations/nous-portal.md | 2030 | 14 | procedure | 1 |
| integrations/index.md | 929 | 1 | navigation | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **5 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_inference_providers_cloud.md` | procedure | providers §AI Providers (intro+catalog table), §Two Commands for Model Management, §Nous Portal (summary→Note 4), §Anthropic (Native), §GitHub Copilot, §First-Class API-Key Providers, §xAI Grok, §NovitaAI, §Ollama Cloud, §AWS Bedrock, §Qwen Portal OAuth, §Alibaba Coding Plan, §MiniMax OAuth, §NVIDIA NIM, §GMI Cloud, §StepFun, §Hugging Face, §Google Gemini OAuth | ~2400 | Cloud + first-class providers: the `hermes model` vs `/model` split, the OAuth-vs-API-key provider catalog (Nous, Anthropic, Copilot, xAI, Gemini, Bedrock, NVIDIA, Qwen/MiniMax OAuth, Chinese providers, HF), per-provider auth modes + base-URL overrides. Catalog table curated; per-provider deep setup → SP15 guides. |
| 2 | `hermes_local_self_hosted_llm.md` | procedure | providers §Custom & Self-Hosted LLM Providers (General Setup, Switching with /model), §Ollama, §vLLM, §SGLang, §llama.cpp, §LM Studio, §WSL2 Networking, §Troubleshooting Local Models | ~2300 | Self-hosted inference: the OpenAI-compatible custom-endpoint pattern, Ollama/vLLM/SGLang/llama.cpp/LM Studio setup, the universal 64K-context-minimum + per-server tool-calling flags, WSL2 networking (mirrored vs NAT, bind address, firewall), and the local-model troubleshooting matrix. |
| 3 | `hermes_provider_routing_proxies.md` | procedure | providers §LiteLLM Proxy, §ClawRouter, §Other Compatible Providers, §Context Length Detection, §Named Custom Providers, §Cookbook (Together/Groq/Perplexity), §Choosing the Right Setup, §Optional API Keys, §OpenRouter Provider Routing, §OpenRouter Pareto Code Router, §Fallback Providers | ~2400 | Routing/proxy layer: multi-provider gateways (LiteLLM, ClawRouter), other OpenAI-compatible endpoints, the 9-source context-length resolution chain, named `custom_providers[]` + `extra_body`/vision/api_mode, the cookbook recipes, OpenRouter `provider_routing` + Pareto Code router, and the `fallback_providers[]` chain. Feature internals (routing/fallback) → SP09 link-outs. |
| 4 | `hermes_nous_portal_subscription.md` | procedure | nous-portal §What's in the subscription (300+ models, Tool Gateway, Nous Chat, no-creds, parity), §A note on Hermes 4, §Setup (fresh/existing/headless/profile), §Using the Portal (inspect/switch/mixing/manage), §Configuration reference, §Token handling, §Troubleshooting | ~1500 | The recommended one-OAuth subscription gateway: `hermes setup --portal`, the 300+ OpenRouter-proxied model catalog, the five Tool-Gateway backends, JWT token handling + quarantine, the `config.yaml` shape, and per-tool gateway mixing. Tool Gateway feature page → SP05; setup guide → SP15. |
| 5 | `hermes_integrations_overview.md` | navigation | index §Integrations intro, §AI Providers & Routing, §Tool Servers (MCP), §Web Search Backends, §Browser Automation, §Voice & TTS, §IDE (ACP), §Programmatic Access, §Memory & Personalization, §Messaging, §Home Automation, §Plugins, §Training & Evaluation | ~900 | Integrations router: indexes every external-system class Hermes connects to (inference, MCP, web-search, browser, voice/TTS, ACP/IDE, API server, memory, messaging, home-automation, plugins, batch) with link-outs to the owning sub-plans. |

**SP14 totals:** 5 notes · procedure 4 · navigation 1 · concept 0 (the Nous-Portal concept becomes the
captured `term_nous_portal`). 3 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 5 · procedure 4 · navigation 1 · concept 0.
- Source: 3 digested pages (~12.4K words) → ~9.5K words of notes (compression via heavy link-outs to SP09/SP15).
- BB mix: procedure 80%, navigation 20%.
- New term captures: 1 (`term_nous_portal`, SP14-owned).

## Section Coverage Map

```
providers.md (9458w, 87 code)
├── # AI Providers intro + ## Inference Providers (catalog table) ───── → Note 1 (per-provider setup→SP15)
├── Nous Portal (summary block + tips) ─────────────────────────────── → Note 1 summary → Note 4 (full)
├── Two Commands for Model Management ──────────────────────────────── → Note 1
├── Anthropic (Native) / GitHub Copilot / First-Class API-Key Providers → Note 1
├── xAI (Grok) / NovitaAI / Ollama Cloud / AWS Bedrock ─────────────── → Note 1 (bedrock/grok deep→SP15)
├── Qwen Portal OAuth / Alibaba Coding Plan / MiniMax OAuth ─────────── → Note 1 (minimax-oauth guide→SP15)
├── NVIDIA NIM / GMI Cloud / StepFun / Hugging Face / Google Gemini OAuth → Note 1 (gemini/nemotron→SP15)
├── ## Custom & Self-Hosted LLM Providers (General Setup, /model switch) → Note 2
├── Ollama / vLLM / SGLang / llama.cpp / LM Studio ─────────────────── → Note 2 (ollama/mac guides→SP15)
├── WSL2 Networking (mirrored/NAT/bind/firewall/verify) ───────────── → Note 2 (windows-native→SP03)
├── Troubleshooting Local Models ──────────────────────────────────── → Note 2
├── LiteLLM Proxy / ClawRouter / Other Compatible Providers ────────── → Note 3
├── Context Length Detection (9-source chain) / Named Custom Providers → Note 3 (compression→SP02/SP18)
├── Cookbook (Together/Groq/Perplexity) / Choosing the Right Setup ─── → Note 3
├── Optional API Keys / Self-Hosting Firecrawl ────────────────────── → Note 3 (web-search→SP08; firecrawl→SP08)
├── OpenRouter Provider Routing / OpenRouter Pareto Code Router ────── → Note 3 (provider-routing feature→SP09)
├── Fallback Providers ────────────────────────────────────────────── → Note 3 (fallback feature→SP09)
└── See Also (Configuration / Env Vars) ───────────────────────────── → Note 3 (link-out SP02/SP21)
nous-portal.md (2030w, 14 code)
├── intro + fastest path / What's in the subscription (models/gateway/chat/no-creds/parity) → Note 4
├── A note on Hermes 4 ────────────────────────────────────────────── → Note 4
├── Setup (fresh/existing/headless-SSH/profile) ───────────────────── → Note 4 (oauth-over-ssh→SP15; profiles→SP04)
├── Using the Portal (inspect/switch/mixing/manage) ──────────────── → Note 4 (tool-gateway→SP05)
├── Configuration reference / Token handling / Troubleshooting ────── → Note 4
└── See also ──────────────────────────────────────────────────────── → Note 4 (link-outs SP05/08/09/15)
integrations/index.md (929w, 1 code) ── ALL sections ──────────────── → Note 5 (link-outs across SP05/08/09/11-13)
```

No source H2/H3 orphaned. All 3 pages fully covered; feature/guide detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| providers.md (9458w, 87 code, MIXED) | Note 1 (cloud/first-class providers) + Note 2 (local & self-hosted + WSL2) + Note 3 (proxies/routing/fallback/context-detection) | >9000w → 3 notes by provider CLASS (each a distinct procedural arc); the 87 source code blocks are curated to ≤6 load-bearing examples per note, rest summarized in prose (kept blocks verbatim). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_nous_portal` (SP14-owned capture) | `term_api_gateway` (active), `term_mcp_gateway` (active), `term_nat_gateway` (active), `term_agentcore_gateway` (active), `term_authportal` (active) | **NOT a dup** — all 5 are DIFFERENT concepts (AWS API/network gateways, MCP gateway, AgentCore gateway, generic auth portal); none covers the Nous subscription/billing gateway. Master-caution false-positives confirmed by reading slugs. | CAPTURE `term_nous_portal`. |
| `hermes_inference_providers_cloud`, `hermes_local_self_hosted_llm`, `hermes_provider_routing_proxies`, `hermes_nous_portal_subscription`, `hermes_integrations_overview` | no substantive term/doc note covers these procedures; no `hermes_agent/` doc notes exist yet (folder empty, DB-confirmed) | NEW | CREATE. |
| `hermes_local_self_hosted_llm` | `term_vllm.md` (active) | **NOT a dup** — `term_vllm` is the component product concept the note uses | CREATE; LINK `term_vllm`. |
| `hermes_provider_routing_proxies` | `term_provider_routing`, `term_fallback_provider`, `term_credential_pool` (all MISSING — owned by SP09 as forward-refs) | **NOT a dup** — those are SP09-owned feature concepts; this note holds the config-side procedure | CREATE; forward-ref-LINK at finalization (+fin). |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0
substantive same-concept duplicates** (the 5 LIKE hits on `term_nous_portal` are false-positives confirmed
by reading the slugs). New `hermes_agent/` folder is empty (DB-confirmed) → no doc-doc collisions; intra-series
links resolve at finalization (G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Four-floor standard set 2026-06-19 (user directive, supersedes the prior 2026-06-14 ≥8/≥8/≥5 floor — snippets
> are NO LONGER a "bonus" group, they are now a COUNTED floor raised to ≥10):** each note's `## Related Notes`
> repo digests whose modules implement what the note describes), ≥10 snippet notes
> note documents), ≥10 documentation notes (`../../documentation/`, sibling `hermes_*` in this series +
> `- [Name](path.md) — what-it-is; relevance: why`.
> finalization (G5/G8). New Hermes-specific terms owned by other SPs (`term_provider_routing`/
> `term_fallback_provider`/`term_credential_pool`→SP09, `term_tool_gateway`→SP05, `term_messaging_gateway`→SP11)
> and SP14's own `term_nous_portal` (created in Phase 0) are ADDITIONAL forward-refs (+fin), NOT counted to the
> ≥8 term floor for notes authored before their target lands.

**Note 1 `hermes_inference_providers_cloud`**
- Terms (10): term_provider_plugin — provider-adapter abstraction the catalog is built from; relevance: each catalog row is a registered provider plugin. term_model_catalog — the curated provider/model list; relevance: the page IS the cloud-provider catalog. term_llm — the inference target; relevance: every provider connects Hermes to an LLM. term_oauth_token — browser-OAuth credential; relevance: Anthropic/Copilot/Qwen/MiniMax/Gemini/xAI OAuth providers mint and store OAuth tokens. term_authentication — credential verification; relevance: the page is organized by auth mode (OAuth vs API-key vs AWS-chain). term_prompt_caching — server-side prompt reuse; relevance: xAI auto-enables prompt caching via `x-grok-conv-id`. term_multimodal — vision/image input; relevance: Hermes auto-detects per-provider vision capability. term_model_failover — switching on provider error; relevance: HF Inference Providers and Copilot do automatic backend failover. term_openai_responses_api — the Responses transport; relevance: xAI Grok-4 and GPT-5+ Copilot route through the Responses API. term_converse_api — Bedrock's model-agnostic API; relevance: the Bedrock provider translates requests to the Converse API. (+fin: term_nous_portal, term_provider_routing)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the provider-adapter/plugin source; relevance: implements every cloud provider in the catalog (Anthropic, Copilot, Bedrock, Gemini, China cluster). [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes model`/`hermes auth` CLI; relevance: the setup wizard + OAuth flows the catalog rows invoke. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the core LLM-call adapters; relevance: holds the Anthropic-OAuth, Bedrock-credentials, Gemini-CloudCode adapters. [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the plugin registry; relevance: providers register as plugins with provider IDs/aliases. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties the provider, CLI, and core layers together.
- Snippets (10): cli_providers_registry — provider-ID/alias registry; relevance: the canonical list of catalog rows. cli_model_switch_entry — `/model` entry point; relevance: the `hermes model` vs `/model` split the page documents. cli_model_switch_swap — provider/model swap logic; relevance: mid-session provider switching. cli_model_catalog — catalog assembly; relevance: builds the per-provider model list. cli_models_picker — interactive picker; relevance: `hermes model` model-selection UI. plugins_provider_registry — plugin-provider registration; relevance: how each first-class provider self-registers. plugins_provider_anthropic — Anthropic adapter; relevance: the §Anthropic (Native) three-auth-mode flow. plugins_provider_copilot — Copilot adapter; relevance: the §GitHub Copilot token-priority + 401-recovery flow. plugins_provider_china_cluster — Chinese-provider cluster; relevance: z.ai/Kimi/MiniMax/Xiaomi/Tencent first-class providers. plugins_provider_codex — OpenAI Codex adapter; relevance: the device-code Codex provider. (+ plugins_provider_bedrock, core_bedrock_adapter_credentials, core_gemini_cloudcode_adapter_auth, plugins_provider_xai_oauth for the per-provider deep paths)
- Docs (15): hermes_nous_portal_subscription — the recommended OAuth subscription; relevance: Note 1 summarizes Portal then links here. hermes_provider_routing_proxies — proxy/routing layer; relevance: where multi-provider routing lives. hermes_local_self_hosted_llm — local/custom endpoints; relevance: the complementary self-hosted half of providers.md. hermes_integrations_overview — integrations router; relevance: indexes the AI-Providers class. hermes_configuring_models_dashboard — (sibling, +fin) model-config doc; relevance: config-side of the catalog. [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: analogous catalog/model-picker doc. [cc_authentication](../claude_code/cc_authentication.md) — CC auth modes; relevance: analogous OAuth/API-key auth surface. [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — CC Bedrock setup; relevance: analogous AWS-credential-chain provider. [cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md) — CC Bedrock model config; relevance: analogous Bedrock model/region config. [cc_google_vertex_ai](../claude_code/cc_google_vertex_ai.md) — CC Vertex provider; relevance: analogous Google/Gemini cloud provider doc. [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — CC admin model restriction; relevance: analogous to curating which catalog providers/models a deployment may select. [cc_amazon_bedrock_features](../claude_code/cc_amazon_bedrock_features.md) — CC Bedrock capability features; relevance: analogous per-feature Bedrock behavior the Hermes Bedrock provider exposes. [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env-var reference; relevance: analogous to the per-provider API-key/base-URL env-var overrides the catalog documents. [bedrock_converse_api_overview](../aws_bedrock/bedrock_converse_api_overview.md) — AWS Bedrock Converse API; relevance: the exact model-agnostic API the Hermes §AWS Bedrock provider translates requests to. [bedrock_api_keys_generate](../aws_bedrock/bedrock_api_keys_generate.md) — AWS Bedrock API-key generation; relevance: the API-key credential path for the API-key (non-OAuth) Bedrock auth mode in the catalog.

**Note 2 `hermes_local_self_hosted_llm`**
- Terms (10): term_vllm — high-throughput GPU server; relevance: the §vLLM canonical local-server setup. term_llm — the served model; relevance: all local servers expose an OpenAI-compatible LLM. term_context_window — total token budget; relevance: the universal 64K-context-minimum is the note's central constraint. term_provider_plugin — the `custom` provider adapter; relevance: local endpoints reuse the OpenAI-compatible custom-provider path. term_quantization — weight compression; relevance: llama.cpp/LM Studio run Q4_K_M-quantized GGUF models. term_kv_cache — attention cache; relevance: SGLang's RadixAttention reuses KV cache; `-c` sizes the KV-cache allocation. term_tensor_parallelism — multi-GPU sharding; relevance: vLLM `--tensor-parallel-size` / SGLang `--tp`. term_model_catalog — discovered model list; relevance: `/v1/models` auto-detection of a local single-loaded model. term_capability_negotiation — runtime feature probe; relevance: tool-calling flags (`--jinja`/`--enable-auto-tool-choice`) gate native tool support. term_computer_vision — image-input handling; relevance: `supports_vision` routes images natively for vision-capable local models. (+fin: term_messaging_gateway)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: implements the `custom`/Ollama-Cloud adapters local servers use. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes model`/`hermes doctor`; relevance: the custom-endpoint wizard + connectivity-doctor the note walks through. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — core inference + context; relevance: holds context-overflow + context-length resolution for local models. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool/vision toolset; relevance: vision-input dispatch + capability probe for self-hosted models. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: the OpenAI-compatible-endpoint contract every local server targets.
- Snippets (10): plugins_provider_custom — the `custom` provider; relevance: the OpenAI-compatible custom-endpoint pattern all local servers use. plugins_provider_ollama_cloud — Ollama Cloud adapter; relevance: the cloud-vs-local Ollama distinction. cli_models_fetch — `/v1/models` fetch; relevance: bare `/model custom` auto-detect of a single loaded model. cli_models_normalize — model-ID normalization; relevance: preserving `model:tag` notation through normalization. cli_config_schema — config.yaml schema; relevance: the `model.base_url`/`provider: custom`/`context_length` block. cli_config_set — `hermes config set`; relevance: setting `FIRECRAWL_API_URL`/local config. cli_doctor_api_connectivity — doctor connectivity probe; relevance: diagnosing "Connection refused" from WSL2. model_tools_capability_probe — capability probe; relevance: detecting tool-calling/vision support per local server. cli_config_validate — config validation; relevance: the context-limit/`Unknown provider` validator. core_conversation_loop_context_overflow — context-overflow handling; relevance: the "forgets context"/truncation troubleshooting matrix. (+ cli_config_loading, tools_vision_input for the load + native-image paths)
- Docs (13): hermes_inference_providers_cloud — cloud providers; relevance: the complementary cloud half of providers.md. hermes_provider_routing_proxies — local proxies (LiteLLM/ClawRouter); relevance: routing in front of local servers. hermes_nous_portal_subscription — Portal alternative; relevance: the managed-vs-self-hosted tradeoff. hermes_integrations_overview — integrations router; relevance: indexes the AI-Providers class. hermes_config_files_precedence — (sibling, +fin) config precedence; relevance: where `config.yaml` model/base_url settings live. [cc_model_selection](../claude_code/cc_model_selection.md) — CC model selection; relevance: analogous custom-model selection. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — CC proxy/gateway config; relevance: analogous base-URL/proxy override for self-hosted endpoints. [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — CC LLM gateway; relevance: analogous OpenAI-compatible-endpoint indirection. [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — CC env config; relevance: analogous env-var/base-URL setup the WSL2 section parallels. [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — CC config debugging; relevance: analogous to the local-model troubleshooting matrix. [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env-var reference; relevance: analogous to the `base_url`/`OPENAI_API_BASE`-style env overrides that point Hermes at a local server. [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — CC network/TLS access; relevance: analogous to the WSL2 networking + bind-address/firewall connectivity section. [cc_settings_files](../claude_code/cc_settings_files.md) — CC settings-file layering; relevance: analogous to the `config.yaml` `provider: custom`/`context_length` block this note edits.

**Note 3 `hermes_provider_routing_proxies`**
- Terms (10): term_model_failover — switch-on-error; relevance: `fallback_providers[]` swaps model+provider mid-session. term_failover — generic failover; relevance: HF auto-failover + the fallback chain semantics. term_round_robin — rotation scheduling; relevance: credential-pool rotation across keys. term_context_window — total budget; relevance: the 9-source context-length detection chain resolves this. term_provider_plugin — provider adapter; relevance: OpenRouter is a registered provider plugin. term_throughput — tok/s sorting key; relevance: OpenRouter `sort: "throughput"` / `:nitro`. term_latency — response-time key; relevance: LiteLLM latency-based routing / `sort: "latency"`. term_reverse_proxy — gateway-in-front pattern; relevance: LiteLLM/ClawRouter are OpenAI-compatible reverse proxies. term_load_balancer — request distribution; relevance: LiteLLM load-balances 100+ providers behind one API. term_rate_limiting — error→backoff trigger; relevance: fallback activates on rate-limit/429 errors. (+fin: term_provider_routing, term_fallback_provider, term_credential_pool)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: the OpenRouter adapter + Pareto/`provider_routing` body fields. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — core chat loop + error classifier; relevance: fallback activation, error→retry classification, credential-pool rotation. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes fallback`/`hermes doctor`; relevance: the interactive fallback config + `Unknown provider` validation. [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin registry; relevance: named `custom_providers[]` register as plugins. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: wires the routing/proxy/fallback layer into the agent.
- Snippets (10): plugins_provider_openrouter — OpenRouter adapter; relevance: `provider_routing`/Pareto Code router/`:nitro`/`:floor`. core_chat_helpers_activate_fallback — fallback activation; relevance: one-shot mid-session fallback swap. core_error_classifier_provider_maps — error→provider classification; relevance: which errors trigger fallback. core_error_classifier_backoff — backoff schedule; relevance: retry timing before fallback advances. core_credential_pool_selection — pool key selection; relevance: round-robin credential rotation. core_credential_pool_seeding — pool seeding; relevance: building the credential pool from sources. core_auxiliary_proxy_url — proxy-URL resolution; relevance: base-URL override for proxy/custom endpoints. providers_init_dispatch — provider dispatch; relevance: routing a request to the resolved provider. core_credential_pool_dataclass — pool data model; relevance: the credential-pool structure rotation operates on. cli_config_schema — config.yaml schema; relevance: the `provider_routing`/`fallback_providers`/`custom_providers` YAML blocks. (+ core_credential_pool_entry, cli_config_validate for entry-shape + validator)
- Docs (13): hermes_inference_providers_cloud — cloud providers; relevance: the providers routed/failed-over to. hermes_local_self_hosted_llm — local endpoints; relevance: proxies often front local servers. hermes_nous_portal_subscription — Portal; relevance: Portal routes through OpenRouter under the hood. hermes_integrations_overview — integrations router; relevance: indexes Provider-Routing + Fallback. hermes_model_aux_provider_config — (sibling, +fin) aux/model provider config; relevance: per-task Pareto routing for auxiliary tasks. [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — CC LLM gateway; relevance: analogous multi-provider gateway. [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — CC LiteLLM gateway; relevance: the same LiteLLM proxy, Claude-Code side. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — CC proxy/gateway config; relevance: analogous base-URL/proxy routing config. [cc_fallback_models](../claude_code/cc_fallback_models.md) — CC fallback models; relevance: analogous fallback-provider chain. [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — CC auth/network errors; relevance: analogous error→retry/fallback triggers. [cc_claude_platform_on_aws_proxy_and_sdk](../claude_code/cc_claude_platform_on_aws_proxy_and_sdk.md) — CC AWS proxy/SDK platform; relevance: analogous reverse-proxy-in-front-of-providers gateway pattern. [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — CC network/TLS access; relevance: analogous to the proxy connectivity/TLS surface routing traffic to backends. [cc_github_actions_cloud_providers](../claude_code/cc_github_actions_cloud_providers.md) — CC cloud-provider routing in CI; relevance: analogous selecting/routing among multiple cloud inference providers.

**Note 4 `hermes_nous_portal_subscription`**
- Terms (10): term_oauth_token — the one Portal credential; relevance: `hermes setup --portal` mints/stores a refresh token at `~/.hermes/auth.json`. term_authentication — login/credential mgmt; relevance: the single-OAuth-replaces-many-keys premise. term_model_catalog — the 300+ model list; relevance: the Portal proxies a curated agentic-model catalog. term_llm — the inference target; relevance: Portal is the recommended way to reach an LLM. term_provider_plugin — the `nous` provider; relevance: Portal registers as the `nous` provider plugin. term_prompt_caching — cached prompt reuse; relevance: routing through OpenRouter inherits its caching behavior. term_multimodal — image/vision via gateway; relevance: the Tool Gateway's FAL image-generation backend. term_reverse_proxy — proxy-through-OpenRouter; relevance: Portal reverse-proxies model traffic through OpenRouter. term_capability_negotiation — client-tag/JWT scoping; relevance: scoped `inference:invoke` JWTs + `client=hermes-client-v<version>` tag. term_load_balancer — multi-backend routing; relevance: Portal's gateway routes five tool backends under one login. (+fin: term_nous_portal, term_tool_gateway, term_provider_routing)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes setup --portal`/`hermes portal`/`hermes auth add nous`; relevance: the entire Portal onboarding + inspection CLI. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the `nous` provider adapter; relevance: implements Portal inference + JWT minting. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — core auth resolution + credential sources; relevance: token-refresh/quarantine/credential resolution per request. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — Tool Gateway tool routing (web/image/TTS/browser); relevance: the five gateway backends the subscription unlocks. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties Portal provider + gateway + auth together.
- Snippets (10): cli_nous_subscription — Nous-subscription setup; relevance: the `hermes setup --portal`/`hermes portal` flow. plugins_provider_nous — Nous provider adapter; relevance: the `provider: nous` + `base_url` config the page shows. cli_auth_provider_state — auth-state introspection; relevance: `hermes portal info` login/routing status. cli_auth_resolve_provider — provider resolution; relevance: resolving Nous as the active inference provider. core_auxiliary_auth_resolution — aux-call auth resolution; relevance: Portal auth on auxiliary/compression/extraction calls. core_credential_sources — credential source precedence; relevance: refresh-token-at-`auth.json` source resolution. tools_tts_routing — TTS backend routing; relevance: the Portal OpenAI-TTS gateway backend. cli_main_provider_flows — main provider flows; relevance: Portal as one of several configurable providers. cli_auth_storage — auth.json token storage; relevance: refresh-token persistence + quarantine on revoke. cli_tools_config — `hermes tools` per-tool config; relevance: mixing gateway backends per tool (web/image/browser/TTS). (+ core_credential_sources, tools_credential_files for the no-creds-in-dotfiles design)
- Docs (13): hermes_inference_providers_cloud — cloud-provider catalog; relevance: Note 1 summarizes Portal then links here. hermes_provider_routing_proxies — routing/proxy layer; relevance: Portal proxies through OpenRouter routing. hermes_integrations_overview — integrations router; relevance: the "start here" Portal recommendation. hermes_local_self_hosted_llm — local alternative; relevance: managed-Portal-vs-self-hosted tradeoff. hermes_configuring_models_dashboard — (sibling, +fin) model config; relevance: the `model.provider: nous` config block. [cc_authentication](../claude_code/cc_authentication.md) — CC auth/subscription login; relevance: analogous one-OAuth subscription login. [cc_model_selection](../claude_code/cc_model_selection.md) — CC model selection; relevance: analogous `/model` switching across the catalog. [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — CC login troubleshooting; relevance: analogous to the "not logged in"/re-auth troubleshooting. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — CC proxy/gateway config; relevance: analogous subscription-gateway base-URL routing. [cc_configure_advisor_model](../claude_code/cc_configure_advisor_model.md) — CC auxiliary/advisor model; relevance: analogous to the auxiliary-model routing the Portal warning covers. [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — CC model-restriction policy; relevance: analogous to the Portal's curated 300+ agentic-model allowlist. [cc_settings_reference](../claude_code/cc_settings_reference.md) — CC settings reference; relevance: analogous to the `config.yaml` Portal/`provider: nous` configuration reference. [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env-var reference; relevance: analogous to the headless/SSH token + `client=hermes-client-v<version>` env handling the Portal setup uses.

**Note 5 `hermes_integrations_overview`** (navigation)
- Terms (10): term_provider_plugin — provider adapter; relevance: the AI-Providers row points at the provider class. term_model_catalog — model list; relevance: inference integrations expose a catalog. term_mcp — Model Context Protocol; relevance: the Tool-Servers (MCP) integration class. term_mcp_gateway — MCP server fronting; relevance: the external tool-server connection surface. term_multimodal — voice/vision; relevance: the Voice & TTS + browser-vision integration classes. term_subagent — delegated agent; relevance: the agent surface integrations attach to. term_autonomous_coding_agents — agent-tool category; relevance: the IDE/ACP + API-server programmatic-access classes. term_agent_harness — the agent runtime; relevance: every integration attaches to the harness. term_batch_processing — parallel run mode; relevance: the Training & Evaluation (batch-processing) integration row. term_acp_agent_client_protocol — IDE protocol; relevance: the IDE & Editor (ACP) integration class. (+fin: term_nous_portal, term_messaging_gateway, term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: the router indexes every subsystem this repo composes. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: the AI-Providers row. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP toolsets; relevance: the Tool-Servers (MCP) row. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — messaging gateway; relevance: the 27+ Messaging-Platforms row. [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — ACP server; relevance: the IDE & Editor (ACP) row. (+ repo_hermes_agent_tools — the Web-Search/Browser/Voice/Home-Automation tool rows)
- Snippets (10): cli_providers_registry — provider registry; relevance: AI-Providers class. plugins_provider_registry — plugin-provider registration; relevance: the provider-plugin surface. cli_mcp_config — MCP config; relevance: Tool-Servers (MCP) class. tools_mcp_oauth_manager — MCP OAuth; relevance: authenticated MCP tool servers. cli_tools_config — `hermes tools` config; relevance: web-search/voice/browser backend selection. model_tools_introspection — toolset introspection; relevance: indexing the available tool classes. gw_runner_provider_boot — gateway provider boot; relevance: the messaging-gateway subsystem. providers_base_abc — provider base ABC; relevance: the common provider contract integrations share. mcp_serve_hermes_as_server — Hermes-as-MCP-server; relevance: the Programmatic-Access/API-server class. tools_tts_routing — TTS routing; relevance: the Voice & TTS class. (+ tools_vision_dispatch, cli_web_config_schema for the browser-vision + web-search rows)
- Docs (13): hermes_inference_providers_cloud — cloud providers; relevance: the AI-Providers link-out target. hermes_nous_portal_subscription — Portal; relevance: the "start here" recommendation. hermes_provider_routing_proxies — routing/proxies; relevance: the Provider-Routing link-out. hermes_local_self_hosted_llm — local LLMs; relevance: the self-hosted-inference link-out. hermes_learning_path — (sibling, +fin) learning path; relevance: navigation hub sibling. [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — CC MCP overview; relevance: analogous MCP tool-server integration. [cc_model_selection](../claude_code/cc_model_selection.md) — CC model selection; relevance: analogous inference-provider integration. [cc_authentication](../claude_code/cc_authentication.md) — CC auth; relevance: analogous integration auth surface. [cc_settings_reference](../claude_code/cc_settings_reference.md) — CC settings reference; relevance: analogous integration-config index. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — CC proxy/gateway config; relevance: analogous gateway-integration config. [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — CC MCP quickstart; relevance: analogous to the Tool-Servers (MCP) integration-class row this router indexes. [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — CC MCP server management; relevance: analogous to managing the external tool-server connections the router lists. [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env-var reference; relevance: analogous to the per-integration env-var/config surface every row links out to.

All 5 notes meet the four-floor standard: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc. Per-note Docs counts now
carry margin above the ≥10 floor — Note 1: 15, Note 2: 13, Note 3: 13, Note 4: 13, Note 5: 13. Term/code-repo/snippet
active 2026-06-19, and the added `aws_bedrock/bedrock_converse_api_overview`/`bedrock_api_keys_generate` doc IDs are
finalization (verified by G5/G8).
**Placeholder term slugs caught + excluded at finalization (DO NOT exist — confirmed MISSING in DB):
`term_openrouter`, `term_inference`, `term_aws_bedrock`, `term_gemini`, `term_groq`, `term_api_key`,
`term_load_balancing`, `term_jwt`, `term_cost_optimization`, `term_self_hosted`, `term_gpu`** — each note's

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 3 source pages from `inbox/hermes_agent_docs/integrations/`; measured counts match the Source
Pages table (no >50% estimate misses — providers 9458, nous-portal 2030, index 929). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 cloud-providers | procedure | 2400 | ≤6 (curate from ~40 catalog/auth blocks; catalog table in prose) | ✓ |
| 2 local-self-hosted | procedure | 2300 | ≤6 (curate from ~30 server/WSL2 blocks; one canonical block per server) | ✓ |
| 3 routing-proxies | procedure | 2400 | ≤6 (curate from ~25 proxy/routing/fallback YAML blocks) | ✓ |
| 4 nous-portal | procedure | 1500 | ≤6 (from 14 source blocks) | ✓ |
| 5 integrations-overview | navigation | 900 | ≤1 | ✓ |

No further splits needed — all 5 notes are ≤2500w. Notes 1-3 (the providers.md cluster) are dense but each is
a single provider-class procedure ≤2500w; the 87 source code blocks are curated to ≤6 load-bearing examples per
note, with the rest summarized in prose (kept blocks verbatim). Borderline notes (1/2/3 at ~2300-2400w) were
checked for further split: each is one topically-cohesive provider class with no BB mixing → KEEP (per review
CP6 default-to-keep justification). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
verified field order against `cc_admin_enforcement_controls.md` and `cc_sandbox_modes.md`): YAML field order
`tags → keywords → topics → language → date of note → status → building_block → source_url →
access_control_group`; body `# Title → ## Overview (opener leading with what it IS, NOT ## Definition) →
source-mirrored H2s → ## Related Notes (indexed markdown links, each `- [Name](path.md) — what-it-is;
relevance: …`; FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer **Source** / **Last Updated** / **Status: Active**
(plain bold, no heading)`. One BB/note; caps ≤2500w/≤6 code/≤400 lines. Forbidden YAML fields per master
(`title`, `category`, `created`, `updated`, `source`, `parent`, `author`, `related_wiki`,
`note_second_category`). Year tags quoted. No wiki/markdown links in YAML. Not invented — matches existing
`cc_` notes.

## Undigested Terms Plan (SP14)

**SP14 owns 1 new term capture: `term_nous_portal`.** Per the master's corpus-wide ownership sweep (DF 25+,
owner SP14), the Nous subscription / Tool-Gateway billing concept is captured here BEFORE writing SP14's digest
notes (Phase 0, via `/tessellum-capture-term-note` — NOT inline). All other Hermes-specific concepts SP14 touches
are owned by other sub-plans (link at finalization) or are existing verified terms. Most provider names
(OpenRouter, vLLM, Ollama, Bedrock, Gemini, Groq, …) are PRODUCTS, not concept captures — `term_vllm` exists
(link it); the rest are inline prose references.

| Term slug | Decision | Owner | Capture Phase | Stub/Full | Best-fit glossary | Source page | DF |
|-----------|----------|-------|---------------|-----------|-------------------|-------------|---:|
| `term_nous_portal` | **CAPTURE** (DB-confirmed MISSING; 5 LIKE hits are different concepts) | **SP14** | Phase 0 (before digest notes) | full (moderate, 10 Related Terms) | acronym_glossary_tools | nous-portal.md, providers.md | 25+ |
| `term_provider_routing`, `term_fallback_provider`, `term_credential_pool` | LINK only (forward-ref, +fin) | SP09 | — | — | — | providers.md | — |
| `term_tool_gateway` | LINK only (+fin) | SP05 | — | — | — | nous-portal.md | — |
| `term_messaging_gateway` | LINK only (+fin) | SP11 | — | — | — | index.md | — |
| `term_nemotron` | LINK only (+fin) | SP15 | — | — | — | providers.md | — |
| existing verified (`term_vllm`, `term_llm`, `term_model_catalog`, `term_provider_plugin`, `term_model_failover`, `term_oauth_token`, `term_prompt_caching`, `term_context_window`, `term_sandbox_backend`, `term_authentication`, `term_multimodal`, `term_failover`, `term_round_robin`, `term_throughput`, `term_latency`, `term_reverse_proxy`, `term_quantization`, `term_kv_cache`, `term_mcp`, `term_mcp_gateway`, `term_subagent`, `term_autonomous_coding_agents`, `term_agent_harness`, `term_self_evolving_agent`) | LINK (do NOT recreate) | — | — | — | — | all | — |

### Renamed (general → specific)

| Original candidate slug | Renamed to | Reason |
|---|---|---|
| `term_portal` / `term_subscription` | `term_nous_portal` | one-word generic noun ("portal"/"subscription") collides with auth portals / billing in general; the captured concept is the Nous-specific subscription+Tool-Gateway billing gateway → scope-qualified slug. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_vllm` | `resources/term_dictionary/term_vllm.md` (active) | Not captured — LINK the existing term from `hermes_local_self_hosted_llm`. |
| `term_openrouter`, `term_inference`, `term_aws_bedrock`, `term_gemini`, `term_groq` (product names) | none substantive (all DB-confirmed MISSING) | No removal — these are PRODUCT names, intentionally inline prose references, not term captures (master Undigested-Terms guidance: low-value product names are link-only). |

## Term-Note Authoring Requirements

`term_nous_portal` is authored via **`/tessellum-capture-term-note "Nous Portal"`** (Phase 0, NOT inline),
following the master's `/tessellum-capture-term-note` canonical spec in full. Load-bearing requirements:

- **YAML**: `building_block: concept`; required fields (`tags` incl. `terminology` + domain tags, `keywords`
  incl. "Nous Portal" / "Nous subscription gateway" / "Tool Gateway", `topics`, `language: markdown`,
  `date of note`, `status: active`, `access_control_group: ["general"]`, `related_wiki`); forbidden-field list
  per master. No `term_*.md` links in YAML.
- **H1 + H2 order**: `# Nous Portal` → `## Definition` → `## Context` → `## Key Characteristics`
  → `## Performance / Metrics` (omit if none) → `## Related Terms` (**moderate depth → ≥10 links**, ≥3
  in-domain + ≥3 cross-domain, INDEXED bold markdown links) → `## References` (EXTERNAL URLs only — no `.md`).
  (portal.nousresearch.com, Nous Research blog/docs, OpenRouter docs) + vault cross-reference
  (`/tessellum-search-notes`). Single-source (digest-doc-only) capture → FAIL.
- **Related Terms cross-domain diversity**: in-domain (`term_oauth_token`, `term_provider_plugin`,
  `term_model_catalog`, `term_reverse_proxy`, `term_prompt_caching`) + cross-domain
  (`term_api_gateway` as a contrast, `term_mcp_gateway`, `term_authentication`, `term_subagent`) — verified links.
- **Fleeting-content guard**: genericize bare model-version lists / dollar amounts / dated catalogs.
- **Glossary**: update `0_entry_points/acronym_glossary_tools.md` with the exact 4-5-sentence Description
  template (bold the single distinguishing fact, no metrics).
- **Backlink expansion (Step 6e)**: add `term_nous_portal` to 5-10 existing in/cross-domain term notes'
  `## Related Terms` (e.g. `term_oauth_token`, `term_provider_plugin`, `term_model_catalog`).
- **>200-line decomposition**: if the note exceeds 200 lines, decompose per Step 7 (Procedure→`sop_*`,
  Model/Argument→`thought_*`; concept+navigation stay in parent).
  OR mark `status: stub` + `research_pending: true` — do NOT silently emit a digest-doc-only stub.

The full Term-Note Authoring Requirements (YAML spec, H1/H2 order, multi-source mandate, cross-domain
diversity, MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12, backlink
expansion, >200-line decomposition, acceptance failure conditions) are inherited verbatim from the master /
`/tessellum-capture-term-note` canonical and apply to this capture.

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (term capture, FIRST):** `/tessellum-capture-term-note "Nous Portal"` → `term_nous_portal.md`
  (+ glossary update + backlink expansion). Reindex so the term resolves before digest notes link it.
- **Phase 1 (providers cluster, P1-hub pilot):** Notes 1, 2, 3. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (portal + router):** Notes 4, 5. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/integrations/<page>`
(code verbatim for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4,
DB-verify every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** ·
G7 single-BB · **G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_inference_providers_cloud hermes_local_self_hosted_llm hermes_provider_routing_proxies hermes_nous_portal_subscription hermes_integrations_overview; do
```

## Entry Point Decision (inherited)

Contributes 5 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c, >30-note
series) under an "Inference Providers & Integrations" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP14 does NOT create a separate entry point — the
>30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_providers_adapters.md` | → `hermes_inference_providers_cloud`, `hermes_local_self_hosted_llm`, `hermes_provider_routing_proxies` | provider-adapter repo ↔ provider-catalog/local/routing usage docs |
| `repo_hermes_agent.md` | → `hermes_integrations_overview` | implementation root ↔ integrations router |
| `term_vllm.md` | → `hermes_local_self_hosted_llm` | concept term → the self-hosted-server doc that documents vLLM setup |
| `term_provider_plugin.md` | → `hermes_inference_providers_cloud`, `hermes_provider_routing_proxies` | provider-plugin concept → catalog + routing docs |
| `term_model_catalog.md` | → `hermes_nous_portal_subscription`, `hermes_inference_providers_cloud` | catalog concept → Portal 300+ catalog + cloud-provider docs |
| `term_oauth_token.md` | → `hermes_nous_portal_subscription` | OAuth concept → Portal one-OAuth subscription doc |
| `term_nous_portal.md` (new, Phase 0) | → `hermes_nous_portal_subscription`, `hermes_inference_providers_cloud` | new concept term → its user-facing docs |
| `entry_code_snippets_hermes_agent.md` | → `hermes_inference_providers_cloud`, `hermes_integrations_overview` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 5 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution phase
(Phase 2b), not a recommendation.

## Pacing Rules (inherited)

Phase 0 term capture FIRST (so `term_nous_portal` resolves before notes link it). Pilot Note 1
(`hermes_inference_providers_cloud`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note —
do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6 load-bearing
examples (one canonical block per provider/server), summarize the rest in prose. If a note exceeds 350 lines
during writing, STOP and split. If multi-agent: agents return note content, master writes serially where there
is write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP14 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 5 rows to the
  master-created entry point; backfill the `repo_hermes_agent_providers_adapters` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1 wave: bidirectionally cross-link the SP09 feature pages (provider-routing/fallback/credential-pools/
  subscription-proxy) and SP15 per-provider setup guides (ollama/gemini/grok/minimax/bedrock/azure/nemotron/
  nous-portal) once those SPs land — config-side (SP14) ↔ feature/guide.
- Consider one `thought_` note comparing Hermes' docs-stated provider model vs the code-digestion findings in
  `snippet_hermes_agent_plugins_provider_*` and `snippet_hermes_agent_core_*_adapter_*`.

## Augmentation Report

- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  raised to ≥10; a new ≥5 code-repo floor (the `repo_hermes_agent_*` source-code digests) was added; the doc
  floor was raised from ≥5 to ≥10 (sibling `hermes_*` + analogous `claude_code/cc_*`). All source pages re-read.
- Doc-floor margin pass 2026-06-19 (fix): every planned note's Docs line was re-read against the owned source
  specific `relevance:` clause) — Note 1 10→15 (added `cc_restrict_model_selection`, `cc_amazon_bedrock_features`,
  `cc_environment_variables`, `aws_bedrock/bedrock_converse_api_overview`, `aws_bedrock/bedrock_api_keys_generate`),
  Notes 2/3/4/5 each 10→13 (added more analogous `cc_*` env/network/proxy/MCP/settings docs). Terms/Code-Repos/
  Snippets lines were NOT touched (they already pass). No existing doc link was dropped; `status:` unchanged.
- Sections added/updated: Collision&Dedup Audit (5 LIKE false-positives on `term_nous_portal` confirmed by
  reading slugs), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc, all
  confirmed), G5 ghost + G8 scripts, Inlinks, Undigested Terms Plan + Term-Note Authoring Requirements (SP14 owns
  `term_nous_portal`).
- Density re-read: counts match measured (providers 9458, nous-portal 2030, index 929); **no additional splits**
  beyond the planned 3 (providers→3). All 5 notes ≤2500w; code-heavy provider notes curated to ≤6 blocks.
- Collision audit: **0 removals** (product names intentionally inline; `term_vllm` LINK-not-dup); `term_nous_portal`
  CAPTURE confirmed (5 LIKE hits are different concepts).
- Term placeholder catch: **11 non-existent term slugs caught at finalization** (`term_openrouter`,
  `term_inference`, `term_aws_bedrock`, `term_gemini`, `term_groq`, `term_api_key`, `term_load_balancing`,
  active terms only.
- Undigested terms surfaced at augment: **1 owned** (`term_nous_portal`, Phase 0).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (FOUR-FLOOR
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (Phase 0, `term_nous_portal`) ✓ best-fit glossary (acronym_glossary_tools) ✓ Term-Note Auth Reqs
(present, multi-source mandate) ✓ invokes capture-term-note (`/tessellum-capture-term-note "Nous Portal"`) ✓
Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (Renamed table: portal/subscription→nous_portal)
✓ Slug Collision (5 LIKE false-positives + 11 placeholders caught; product-name removals noted) ✓ dedup
generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks
EXECUTED (Phase 2b) ✓ Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases (0/1/2), each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (5 rows under an Inference Providers section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 5 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | providers.md→3; all notes ≤2500w; code-heavy notes curated ≤6; dense provider notes (1-3) checked → cohesive single-class procedures, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15: providers 9458 (largest integrations page), nous-portal 2030, index 929 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP14 owns 1 capture (`term_nous_portal`, Phase 0, acronym_glossary_tools, full); Term-Note Authoring Requirements present with multi-source MUST-language mandate; invokes `/tessellum-capture-term-note`. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 5 doc notes + the captured term (term_dictionary AND documentation/); 5 LIKE false-positives on `term_nous_portal` confirmed (gateways/auth-portal = different concepts); 11 placeholder term slugs caught + excluded; Renamed (portal/subscription→nous_portal) + Removed (product names) sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 5 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 2b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

---

**Independent Re-Review 2026-06-19 (FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).**

Independent read-only review of the 2026-06-19 four-floor re-augmentation. CP1 evaluated against ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per planned note. Anti-fabrication DB spot-check run via `.venv/bin/python` (config.py needs 3.10+).

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes — FOUR-FLOOR | PASS | All 5 notes counted: each has 10 term + 5 code-repo + 10 snippet + ≥10 doc (Note 1: 15 doc, Notes 2-5: 13 doc each — ≥8/≥5/≥10/≥10 met with margin after the 2026-06-19 doc-floor margin pass). Every entry carries a ` — what-it-is; relevance: …` clause; no bare links. `+fin`/`(+ …)` parentheticals correctly NOT counted to floors. Forward-ref terms (`term_nous_portal`/`term_provider_routing`/`term_fallback_provider`/`term_credential_pool`/`term_tool_gateway`/`term_messaging_gateway`) correctly relegated to `+fin` (DB-confirmed MISSING, not counted). |
| CP2 | 8-GATE per batch (G1-G8 incl G5/G6/G8) | PASS | 3 phases (0/1/2), each G1–G8 incl G5-ghost (Script 4, DB-verify every ref) + G6-broken-links + G8-in-degree≥1-from-outside-folder. |
| CP3 | Entry point + size | PASS | Shares master-created `entry_hermes_agent_docs.md` (5 rows), >30-note threshold; entry point at master level — correct per master Step 4c. |
| CP4 | Plan size manageable | PASS | 5 planned notes (≤30); plan file 446 lines. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md`; FOUR-FLOOR minimum stated in the spec (line 218). |
| CP6 | Borderline density → split | PASS | providers.md (9458w/87code) split 3-ways by provider class; all 5 notes ≤2500w; code curated ≤6/note; KEEP justification for dense notes 1-3. |
| CP7 | Source counts measured (re-measured) | PASS | Independently re-measured from `inbox/hermes_agent_docs/integrations/`: providers body=9458w (matches), nous-portal=2030w/14code (matches exactly), index=929w/1code (matches exactly). providers code blocks = 82 (col0 fences) / 87 (incl. indented fences, plan's method) — either count is ≫ the ≤6/note cap, no material impact. Ratio 1.00. |
| CP8f | Slug specificity + collision/dedup audit | PASS | 5 LIKE false-positives on `term_nous_portal` confirmed different concepts; 11 placeholder term slugs DB-confirmed MISSING and correctly excluded; `term_vllm` LINK-not-dup; Renamed + Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 5 notes from repo_*/term_*/entry_* outside the folder; gated Phase 2b. |

Anti-fabrication DB spot-check (`.venv/bin/python`, `note_status LIKE 'active%'`): **55/55 cited snippet barenames active**, **all 31 distinct terms active**, **all 9 code-repos active**, **all distinct `cc_*` docs active** (the original 16 + the doc-floor-margin additions `cc_restrict_model_selection`/`cc_amazon_bedrock_features`/`cc_environment_variables`/`cc_network_tls_and_access`/`cc_settings_files`/`cc_claude_platform_on_aws_proxy_and_sdk`/`cc_github_actions_cloud_providers`/`cc_mcp_quickstart`/`cc_mcp_server_management`), and the **2 added `aws_bedrock/*` docs active** (`bedrock_converse_api_overview`, `bedrock_api_keys_generate`). Zero MISSING among required (term/code-repo/snippet/doc) IDs. `term_nous_portal` + 5 forward-ref terms + 11 placeholders all correctly MISSING (consistent with `+fin`/excluded treatment). Sibling `hermes_*` doc IDs absent (exempt — created at execution per G5/G8).

Minor (non-blocking, not fixed — out of scope, inherited series-wide): the embedded Validation Scripts block invokes `python3` (system 3.9.6) for the `config.py` import, which fails on 3.10+ syntax; execution must use `.venv/bin/python`. Does not affect any cross-ref/floor correctness.

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-synced from upstream `NousResearch/hermes-agent`
main from pinned commit `95715dc` to `c253b07` on 2026-06-19. All of SP14's owned pages were
independently re-measured (BODY-only word count after stripping YAML frontmatter; code-block count =
fenced-line count ÷ 2) and the word/code counts are **UNCHANGED**:

- `integrations/providers.md` — 9458w / 87code (unchanged)
- `integrations/nous-portal.md` — 2030w / 14code (unchanged)
- `integrations/index.md` — 929w / 1code (unchanged)

No planned-note, split, density, or cross-ref decision is affected (all 3 pages re-confirmed against the
Source Pages table, ratio 1.00; providers.md still splits 3-ways, all 5 notes ≤2500w). Plan remains **READY**.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented FOUR-FLOOR 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; independent re-review FOUR-FLOOR 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19 (counts unchanged)

**Source**: `inbox/hermes_agent_docs/integrations/{providers,nous-portal,index}.md`
**Last Updated**: 2026-06-15 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
