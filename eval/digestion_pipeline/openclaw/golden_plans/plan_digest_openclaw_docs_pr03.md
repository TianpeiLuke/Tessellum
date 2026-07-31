---
title: Sub-Plan pr03 — OpenClaw Docs: Providers (deepseek, ds4, elevenlabs, fal, fireworks, github-copilot, gmi)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
ready_date: 2026-06-21
pages:
  - providers/deepseek
  - providers/ds4
  - providers/elevenlabs
  - providers/fal
  - providers/fireworks
  - providers/github-copilot
  - providers/gmi
---

# Sub-Plan pr03: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML + `## Overview` / source-mirrored H2 / `## Related Notes` / `## References` / bold footer), dedup (3-way vs term_dictionary + documentation + repo_openclaw*), 9-GATE validation, cross-references, undigested-term ownership, and entry-point wiring are all inherited verbatim from the master and are NOT re-derived here.

## Scope

The 7 provider-setup pages for a mixed batch of model and media providers: **DeepSeek** (native OpenAI-compatible LLM provider with V4 thinking/replay), **ds4** (a local DeepSeek V4 Flash Metal server reached through the generic `openai-completions` family + `localService`), **ElevenLabs** (TTS + Scribe STT + realtime streaming STT — a media provider, not an LLM provider), **fal** (hosted image/video/music generation), **Fireworks** (OpenAI-compatible Kimi router with forced-off thinking), **GitHub Copilot** (device-flow model provider + Copilot SDK harness / proxy options + embedding provider for memory search), and **GMI Cloud** (hosted multi-vendor OpenAI-compatible aggregator). Priority **P2 (Phase B — features/integration)**: these are provider how-tos the concepts/model-providers, gateway, and CLI core (Phase A) reference. The code-side counterparts (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`, `repo_openclaw_agents`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **5,253 measured words** (mirror `inbox/openclaw_docs/providers/`). **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| DeepSeek | `providers/deepseek` | 632 | 3 | 7 | 0 | procedure |
| ds4 | `providers/ds4` | 960 | 6 | 8 | 0 | procedure |
| ElevenLabs | `providers/elevenlabs` | 457 | 4 | 5 | 0 | procedure |
| Fal | `providers/fal` | 818 | 3 | 5 | 0 | procedure |
| Fireworks | `providers/fireworks` | 767 | 5 | 5 | 0 | procedure |
| GitHub Copilot | `providers/github-copilot` | 1,129 | 3 | 5 | 2 | procedure (split: model-provider auth vs memory-search embeddings) |
| GMI Cloud | `providers/gmi` | 490 | 4 | 6 | 0 | procedure |

**Totals:** 5,253 words · 28 code fences · 41 H2 · 2 H3. No page exceeds the 2,500-word cap; one page (`github-copilot`, mixed task clusters) splits.

## Content Strategy

- **Prioritize**: each provider's auth + setup path (env var / `onboard --auth-choice` / device-login) and its
  distinguishing runtime contract — DeepSeek V4 `reasoning_content` replay, ds4 `--ctx`/`localService` sizing,
  Fireworks forced-off Kimi thinking (route to Moonshot for reasoning), Copilot device-flow + transport selection,
  GMI multi-vendor fallback positioning. These are what a user actually configures.
- **Split**: only `github-copilot.md` (1,129w, mixed task clusters) → (a) model-provider auth/setup procedure and
  (b) memory-search embedding-provider procedure. The two are distinct config surfaces (`agents.defaults.model`
  vs `agents.defaults.memorySearch`) and distinct task clusters; splitting keeps each atomic and well under caps.
  All other pages are single small reference pages → 1 note each (per master "Most reference pages = 1 note").
- **One BB per note**: every page here is a setup/config how-to ⇒ `building_block: procedure` across all 8 notes.
  ElevenLabs is a *media* provider (TTS/STT) and fal is a *generation* provider — still procedure (config tasks),
  but routed to the speech/media term + snippet cluster, not the LLM-provider cluster.
- **Link-out (do NOT duplicate)**: `concepts/model-providers`, `gateway/configuration-reference`,
  `gateway/local-model-services`, `gateway/local-models`, `gateway/authentication`, `tools/thinking`, `tools/tts`,
  `tools/image-generation`/`video-generation`/`music-generation`, `concepts/memory-search`, `providers/moonshot`,
  `plugins/copilot`/`plugins/copilot-proxy` are all OTHER sub-plans' pages — referenced as planned siblings or
  external `## References` URLs, never re-digested here. Provider/model vocabulary links existing
  `term_llm`/`term_claude`/`term_deepseek`/`term_third_party_genai_services`/`term_text_to_speech` etc.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_deepseek.md` | procedure | deepseek.md: Install plugin, Getting started, Built-in catalog, Thinking and tools, Live testing, Config example | 600 | Configure the native DeepSeek provider in OpenClaw: install `@openclaw/deepseek-provider`, onboard with `DEEPSEEK_API_KEY`, the V4 Flash/Pro/Chat/Reasoner catalog, and the V4 thinking + `reasoning_content` replay contract for multi-turn tool use. |
| 2 | `oc_providers_ds4.md` | procedure | ds4.md: Requirements, Quickstart, Full config, On-demand startup, Think Max, Test, Troubleshooting | 700 | Run OpenClaw against the local `antirez/ds4` DeepSeek V4 Flash Metal server via the generic `openai-completions` provider: `--ctx` sizing, `models.providers.ds4` config, `localService` on-demand startup, Think Max, and smoke tests. |
| 3 | `oc_providers_elevenlabs.md` | procedure | elevenlabs.md: Authentication, Text-to-speech, Speech-to-text, Streaming STT | 600 | Use ElevenLabs as OpenClaw's voice/media provider: `ELEVENLABS_API_KEY`/`XI_API_KEY` auth, `messages.tts` text-to-speech, Scribe v2 batch STT for audio attachments, and Scribe v2 Realtime streaming STT for Voice Call / Google Meet. |
| 4 | `oc_providers_fal.md` | procedure | fal.md: Getting started, Image generation, Video generation, Music generation | 650 | Configure the bundled `fal` provider for hosted generation: `FAL_KEY` auth, image models (Flux/Krea 2/GPT Image 2/Nano Banana 2) with edit + aspect-ratio rules, queue-backed video (Seedance/HeyGen), and music (`music_generate`) defaults. |
| 5 | `oc_providers_fireworks.md` | procedure | fireworks.md: Getting started, Non-interactive setup, Built-in catalog, Custom Fireworks model ids | 600 | Configure the bundled Fireworks provider: `FIREWORKS_API_KEY` auth, the two pre-cataloged Kimi routers, custom `fireworks/<id>` model refs with dynamic resolution, and why Kimi thinking is forced off (route through Moonshot for reasoning). |
| 6 | `oc_providers_github_copilot_provider.md` | procedure | github-copilot.md: Three ways to use Copilot, Optional flags, Non-interactive onboarding | 650 | Use GitHub Copilot as a model provider/runtime: built-in device-login (`models auth login-github-copilot`), the Copilot SDK harness and Copilot Proxy alternatives, env-var resolution order (COPILOT_GITHUB_TOKEN > GH_TOKEN > GITHUB_TOKEN), and transport selection. |
| 7 | `oc_providers_github_copilot_memory_search.md` | procedure | github-copilot.md: Memory search embeddings (Config, How it works) | 350 | Use a logged-in GitHub Copilot subscription as the embedding provider for OpenClaw memory search: `memorySearch.provider: "github-copilot"`, on-demand embedding-model discovery, and the token-exchange-to-`/embeddings` flow. |
| 8 | `oc_providers_gmi.md` | procedure | gmi.md: Setup, Defaults, When to choose GMI, Models, Troubleshooting | 500 | Configure GMI Cloud as a hosted multi-vendor OpenAI-compatible provider: install `@openclaw/gmi-provider`, `GMI_API_KEY` auth, the seeded multi-vendor route catalog (`gmi/<vendor>/<model>`), when to pick GMI as a fallback aggregator, and troubleshooting. |

## Section Coverage Map

```
deepseek.md
├── Install plugin ─────────────────────────── → note 1 (oc_providers_deepseek)
├── Getting started ────────────────────────── → note 1
├── Built-in catalog ───────────────────────── → note 1
├── Thinking and tools ─────────────────────── → note 1
├── Live testing ───────────────────────────── → note 1
├── Config example ─────────────────────────── → note 1
└── Related (link-out cards) ───────────────── → note 1 ## References
ds4.md
├── Requirements ───────────────────────────── → note 2 (oc_providers_ds4)
├── Quickstart ─────────────────────────────── → note 2
├── Full config ────────────────────────────── → note 2
├── On-demand startup ──────────────────────── → note 2
├── Think Max ──────────────────────────────── → note 2
├── Test ───────────────────────────────────── → note 2
├── Troubleshooting ────────────────────────── → note 2
└── Related (link-out cards) ───────────────── → note 2 ## References
elevenlabs.md
├── Authentication ─────────────────────────── → note 3 (oc_providers_elevenlabs)
├── Text-to-speech ─────────────────────────── → note 3
├── Speech-to-text ─────────────────────────── → note 3
├── Streaming STT ──────────────────────────── → note 3
└── Related (link-out) ─────────────────────── → note 3 ## References
fal.md
├── Getting started ────────────────────────── → note 4 (oc_providers_fal)
├── Image generation ───────────────────────── → note 4
├── Video generation ───────────────────────── → note 4
├── Music generation ───────────────────────── → note 4
└── Related (link-out cards) ───────────────── → note 4 ## References
fireworks.md
├── Getting started ────────────────────────── → note 5 (oc_providers_fireworks)
├── Non-interactive setup ──────────────────── → note 5
├── Built-in catalog ───────────────────────── → note 5
├── Custom Fireworks model ids ─────────────── → note 5
└── Related (link-out cards) ───────────────── → note 5 ## References
github-copilot.md
├── Three ways to use Copilot in OpenClaw ──── → note 6 (oc_providers_github_copilot_provider)
├── Optional flags ─────────────────────────── → note 6
├── Non-interactive onboarding ─────────────── → note 6
├── Memory search embeddings ───────────────── → note 7 (oc_providers_github_copilot_memory_search)
│   ├── ### Config ─────────────────────────── → note 7
│   └── ### How it works ───────────────────── → note 7
└── Related (link-out cards) ───────────────── → notes 6 + 7 ## References
gmi.md
├── Setup ──────────────────────────────────── → note 8 (oc_providers_gmi)
├── Defaults ───────────────────────────────── → note 8
├── When to choose GMI ─────────────────────── → note 8
├── Models ─────────────────────────────────── → note 8
├── Troubleshooting ────────────────────────── → note 8
└── Related (link-out) ─────────────────────── → note 8 ## References
```
No orphaned sections. Every `## Related` block becomes that note's `## References` (external URLs) + relevance-linked siblings; the link-out targets (model-providers, configuration-reference, local-model-services, tts, thinking, memory-search, moonshot, plugins/copilot, image/video/music-generation) belong to OTHER sub-plans and are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| github-copilot.md (1,129w, 5 H2 / 2 H3) | notes 6 + 7 | Two distinct task clusters on one page: using Copilot as a **model provider / agent runtime** (device-login, SDK harness, proxy, transport) vs using a Copilot subscription as an **embedding provider for memory search** (`memorySearch.provider`). Different config surfaces and different audiences; split keeps each note atomic and focused (under word-cap individually). |

All other 6 pages: **no split** — each is a single small reference page (457–960w), a single `procedure` BB, ≤6 code fences ⇒ 1 note each.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (5,253 words). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×8** (all notes — every page is a provider setup/config how-to). No concept/model/argument notes in this batch.
- Est. digest words ~4,650 (avg ~580/note). 28 source code fences distribute across the 8 notes; each note kept ≤6 (config/JSON5 snippets reproduced selectively, verbatim; ds4's 6 fences trimmed to the load-bearing config + smoke-test set).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`; repos `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`; entry points `../../../0_entry_points/entry_Y.md`. Each link rendered in the executed note as `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_providers_deepseek (10t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway being configured; relevance: this page configures DeepSeek inside OpenClaw.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — the DeepSeek model family/provider; relevance: the provider this note documents — link, do not redefine.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: DeepSeek V4 Flash/Pro/Chat/Reasoner are all LLMs selected via model refs.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted external GenAI endpoints; relevance: DeepSeek is a hosted OpenAI-compatible third-party endpoint (`api.deepseek.com`).
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning traces; relevance: V4 `thinking` + `reasoning_content` replay is the page's distinguishing runtime contract.
- [Reasoning Agent](../../term_dictionary/term_reasoning_agent.md) — agents that emit/consume reasoning state; relevance: the `/think xhigh`/`max` → `reasoning_effort` mapping and reasoner surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-call protocol; relevance: the replay contract exists specifically for multi-turn tool use after a thinking turn.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw provider extension package; relevance: `@openclaw/deepseek-provider` is the installed plugin.
- [Context Window](../../term_dictionary/term_context_window.md) — model input-token capacity; relevance: the catalog's 1,000,000 / 131,072 context columns.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model registry; relevance: the built-in static catalog (`models list --all --provider deepseek`) drives default selection.

**Docs**
- [oc_providers_ds4](oc_providers_ds4.md) (planned, this series) — local DeepSeek V4 Flash via `openai-completions`; relevance: same model family run locally vs hosted here.
- [oc_providers_fireworks](oc_providers_fireworks.md) (planned, this series) — another OpenAI-compatible provider with a thinking caveat; relevance: contrast DeepSeek's replay contract vs Kimi forced-off thinking.
- [oc_providers_gmi](oc_providers_gmi.md) (planned, this series) — GMI's `gmi/deepseek-ai/DeepSeek-V3.2` route; relevance: a multi-vendor aggregator alternative to the direct DeepSeek provider.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth/key resolution; relevance: analog to DeepSeek's `DEEPSEEK_API_KEY` + `onboard --auth-choice` flow.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model-ref selection; relevance: same provider/model-ref + default-model selection pattern.
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — thinking/effort levels; relevance: direct analog of DeepSeek `/think` → `reasoning_effort`.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM provider catalog; relevance: how a hosted OpenAI-compatible provider is registered and keyed.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — model-provider plugin anatomy; relevance: structural parallel of the DeepSeek provider plugin.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — per-model `compat`/`thinkingFormat` flags; relevance: the compat flags a DeepSeek model entry sets for reasoning.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider/model routing; relevance: how a selected `deepseek/...` ref resolves to the right adapter.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — config-file reference; relevance: analog of the `agents.defaults.model` + `env` config block.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled/official LLM provider plugins; relevance: where `@openclaw/deepseek-provider` lives.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: consumes the model + replays reasoning history across turns.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — bundled OpenAI chat-completions provider; relevance: the OpenAI-compatible provider archetype DeepSeek follows.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — bundled Anthropic provider; relevance: a second bundled-provider plugin shape for comparison.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog seed; relevance: how the DeepSeek built-in catalog rows are declared.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planning; relevance: how static catalog entries become available models.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery normalization; relevance: `models list --provider` resolution path.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registration; relevance: how a provider id registers, like the DeepSeek plugin.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom OpenAI-compatible provider with reasoning flags; relevance: the reasoning/compat fields a DeepSeek-style provider sets.
- [snippet_hermes_agent_core_lmstudio_reasoning](../../code_snippets/snippet_hermes_agent_core_lmstudio_reasoning.md) — reasoning-server handling; relevance: how a provider's `reasoning_content`/thinking surface is consumed.
- [snippet_hermes_agent_core_runtime_helpers_reasoning](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_reasoning.md) — reasoning-state runtime helpers; relevance: the replay-of-reasoning machinery DeepSeek V4 requires.
- [snippet_hermes_agent_core_think_scrubber](../../code_snippets/snippet_hermes_agent_core_think_scrubber.md) — strips/normalizes thinking blocks; relevance: analog of stripping `reasoning_content` when thinking is disabled.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — per-provider api-mode resolution; relevance: how an OpenAI-compatible provider's API type is selected.

### oc_providers_ds4 (10t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: this page wires OpenClaw to a local ds4 server.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: ds4 serves DeepSeek V4 Flash from a local Metal backend.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the locally-served `deepseek-v4-flash` is an LLM.
- [vLLM](../../term_dictionary/term_vllm.md) — local OpenAI-compatible inference server; relevance: closest analog to ds4's local `/v1` server role.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning traces; relevance: `thinkingFormat: "deepseek"`, `reasoning_effort`, and Think Max behavior.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: OpenAI-style `tools`/`tool_calls` support is a documented requirement.
- [Context Window](../../term_dictionary/term_context_window.md) — input-token capacity; relevance: the `--ctx`↔`contextWindow` alignment is the page's central operational gotcha.
- [Quantization](../../term_dictionary/term_quantization.md) — reduced-precision weights; relevance: ds4 loads a GGUF (quantized) weight file.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — attention key/value memory; relevance: larger `--ctx` allocates more KV memory at server start.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored provider credentials; relevance: ds4's `apiKey: "ds4-local"` placeholder vs real provider auth profiles.

**Docs**
- [oc_providers_deepseek](oc_providers_deepseek.md) (planned, this series) — native hosted DeepSeek provider; relevance: same models served hosted instead of local.
- [oc_providers_gmi](oc_providers_gmi.md) (planned, this series) — hosted multi-vendor alternative; relevance: when local Metal is not wanted, route DeepSeek through GMI.
- [pi_custom_models](../pi/pi_custom_models.md) — custom local-model `models.providers` entry with `compat`; relevance: direct analog of the `models.providers.ds4` config block.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a non-bundled provider; relevance: ds4 is not a bundled plugin — same custom-registration pattern.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted local LLM setup; relevance: the local-server-plus-gateway pattern ds4 implements.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama provider config; relevance: localhost `baseUrl` + ignored-key local server, like ds4.
- [hermes_provider_local_llm_mac](../hermes_agent/hermes_provider_local_llm_mac.md) — local LLM on macOS/Metal; relevance: ds4 requires macOS Metal — same platform constraints.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — `compat`/`thinkingFormat`/`supportsReasoningEffort`; relevance: the exact compat fields ds4's model entry sets.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth/key resolution; relevance: ds4's placeholder key vs normal provider auth.
- [hermes_docker_tools_local_inference](../hermes_agent/hermes_docker_tools_local_inference.md) — local inference server operation; relevance: on-demand local-service lifecycle, like `localService`.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime/lifecycle; relevance: how a `ds4/...` model selection drives provider startup at request time.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — generic `openai-completions` provider family; relevance: the provider family ds4 plugs into.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: agent turns whose tool schemas inflate context (the `--ctx` warning).

**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local OpenAI-compatible server config; relevance: localhost `baseUrl` + ignored `apiKey`, the ds4 config shape.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI chat-completions provider; relevance: ds4 uses the `openai-completions` api type.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider with base_url + reasoning flags; relevance: ds4's `baseUrl` + `compat.thinkingFormat` config.
- [snippet_hermes_agent_core_lmstudio_reasoning](../../code_snippets/snippet_hermes_agent_core_lmstudio_reasoning.md) — local reasoning-server behavior; relevance: how a local server's reasoning surface is handled.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Ollama provider plugin; relevance: a second local-family provider config for comparison.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstraction; relevance: the contract any OpenAI-compatible provider (incl. ds4) implements.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — api-mode resolution; relevance: selecting `openai-completions` for the ds4 provider.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model entry schema normalization; relevance: how the ds4 `models[]` entry (`contextWindow`, `maxTokens`, `compat`) is validated.
- [snippet_hermes_agent_core_runtime_helpers_reasoning](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_reasoning.md) — reasoning runtime helpers; relevance: `reasoning_effort`/Think Max handling.
- [snippet_hermes_agent_cli_model_switch_swap](../../code_snippets/snippet_hermes_agent_cli_model_switch_swap.md) — model-switch CLI; relevance: selecting `ds4/deepseek-v4-flash` and routing to it.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — on-demand subsystem startup; relevance: structural analog of `localService` on-demand server startup.

### oc_providers_elevenlabs (10t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: ElevenLabs is wired in as OpenClaw's voice/media provider.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: `messages.tts`/`talk` with `eleven_multilingual_v2`/`eleven_v3`.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — STT; relevance: Scribe v2 batch STT for audio attachments.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — incremental streaming STT; relevance: Scribe v2 Realtime for Voice Call / Google Meet.
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony voice channel; relevance: the streaming-STT target (Twilio 8 kHz G.711 u-law → `ulaw_8000`).
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent voice interaction mode; relevance: TTS+STT together enable voice mode over channels.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: ElevenLabs is an external media-AI provider keyed by `ELEVENLABS_API_KEY`.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multiple input/output modalities; relevance: ElevenLabs spans text→audio and audio→text surfaces.
- [SSE](../../term_dictionary/term_sse.md) — server-sent / streaming events; relevance: realtime transcription and streaming TTS are incremental event streams.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled extension package; relevance: the bundled `elevenlabs` plugin registers TTS + Scribe v2 Realtime.

**Docs**
- [oc_providers_fal](oc_providers_fal.md) (planned, this series) — the other non-LLM media (generation) provider; relevance: paired media-provider config in this batch.
- [oc_providers_deepseek](oc_providers_deepseek.md) (planned, this series) — provider auth/onboard pattern; relevance: shared `*_API_KEY` env-var + provider-block config shape.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS provider registry subsystem; relevance: direct analog of OpenClaw's `messages.tts.providers.elevenlabs` registry.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT/transcription subsystem; relevance: analog of Scribe v2 batch STT for audio attachments.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI; relevance: how TTS/STT providers are selected and exercised.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice-mode usage guide; relevance: end-to-end voice flow ElevenLabs powers.
- [hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — Discord voice channels; relevance: ElevenLabs streaming TTS endpoint for Discord voice (`optimize_streaming_latency`).
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio settings; relevance: configuring inbound audio handling for STT.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tools; relevance: the `tools.media.audio` surface Scribe v2 plugs into.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation in Claude Code; relevance: a sibling coding-agent's STT/dictation feature for contrast.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — provider-block config shape; relevance: analog of the ElevenLabs provider config block.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — bundled `elevenlabs` speech plugin; relevance: TTS/STT/realtime registration code home.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — Voice Call channel; relevance: the streaming-transcription consumer (Twilio u-law frames).

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — `extensions/elevenlabs` TTS provider; relevance: the exact ElevenLabs TTS adapter this page configures.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT provider; relevance: sibling STT provider for cross-reference vs Scribe v2.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — realtime transcription pipeline; relevance: the Voice Call streaming-STT path Scribe v2 Realtime feeds.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media-stream audio handling; relevance: the `ulaw_8000` 8 kHz frame path from Twilio.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk/transcription relay; relevance: how transcribed text re-enters the agent loop.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: how `messages.tts` selects ElevenLabs.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: batch audio→text handling like Scribe v2.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: combines TTS+STT, ElevenLabs's two roles.
- [snippet_hermes_agent_plugins_google_meet](../../code_snippets/snippet_hermes_agent_plugins_google_meet.md) — Google Meet plugin; relevance: the `realtime.transcriptionProvider` consumer set to `elevenlabs`.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS provider; relevance: a non-cloud TTS provider for contrast with ElevenLabs cloud TTS.

### oc_providers_fal (9t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: the bundled `fal` provider is configured here.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — image/video diffusion generators; relevance: Flux/Krea 2 image backends are diffusion models.
- [Stable Diffusion](../../term_dictionary/term_stable_diffusion.md) — canonical text-to-image diffusion; relevance: Stable Audio + the Flux/Krea image family are SD-lineage generators.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted external GenAI; relevance: fal is a hosted image/video/music generation API.
- [Generative Model](../../term_dictionary/term_generative_model.md) — content-generation models; relevance: fal's image/video/music models are generative, not chat LLMs.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI umbrella; relevance: image/video/music generation is the GenAI surface fal exposes.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: the shared `image_generate`/`video_generate`/`music_generate` agent tools invoke fal.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled extension; relevance: the one bundled `fal` plugin registers three generation providers.
- [Multimodal](../../term_dictionary/term_multimodal.md) — cross-modality I/O; relevance: fal spans text→image, image/text→video, text→music.

**Docs**
- [oc_providers_elevenlabs](oc_providers_elevenlabs.md) (planned, this series) — the other non-LLM media provider (voice); relevance: paired media-provider config.
- [oc_providers_deepseek](oc_providers_deepseek.md) (planned, this series) — provider auth/onboard pattern; relevance: shared `*_KEY` + `onboard --auth-choice` flow (`FAL_KEY`).
- [oc_providers_gmi](oc_providers_gmi.md) (planned, this series) — model-ref + default-model selection; relevance: same `agents.defaults.*Model.primary` selection idiom.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tools; relevance: the image/video/music tool surface fal plugs into.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media settings; relevance: media-output settings around generated assets.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model-ref selection + defaults; relevance: same `*GenerationModel.primary` selection pattern.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin anatomy; relevance: structural parallel of fal's multi-provider plugin.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider registry; relevance: how a hosted generation provider is keyed/registered.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — provider-block config shape; relevance: analog of fal's provider config.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth/key resolution; relevance: `FAL_KEY`/`FAL_API_KEY` fallback resolution.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime/lifecycle; relevance: queue-backed submit/status/result flow for long-running video jobs.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled provider plugins; relevance: where the bundled generation provider plugins register.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: agent tools that call image/video/music generation.

**Snippets**
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool; relevance: the `image_generate` params/provider selection fal serves.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch; relevance: how an image request routes to the fal provider.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-generation tool; relevance: `video_generate` (Seedance/HeyGen) reference-image params.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: queue-backed video job dispatch like fal's video flow.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision/media dispatch; relevance: routing media-generation tool calls to a provider.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — multi-provider registration; relevance: fal registers three providers from one plugin.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — bundled provider archetype; relevance: the provider-plugin registration shape fal mirrors.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how a bundled plugin declares its provider registrations.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the plugin contract fal's bundled plugin follows.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog seed; relevance: how fal's model refs (Flux/Krea/Seedance/MiniMax Music) are catalogued.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery; relevance: `models list --provider fal` enumeration.

### oc_providers_fireworks (10t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: the bundled Fireworks provider is configured here.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Fireworks fronts open-weight + routed LLMs (Kimi).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted external GenAI; relevance: Fireworks is a hosted OpenAI-compatible inference platform.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning traces; relevance: Kimi thinking is forced off — the page's central reasoning caveat.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: agent tool use over the OpenAI-compatible API.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled extension; relevance: the bundled Fireworks plugin + `thinking-policy.ts`.
- [Model Router](../../term_dictionary/term_model_router.md) — routes a ref to a backing model; relevance: Fireworks router ids (`routers/kimi-k2p5-turbo`, Fire Pass).
- [Context Window](../../term_dictionary/term_context_window.md) — input-token capacity; relevance: 256,000 / 262,144 catalog contexts.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model registry; relevance: two pre-cataloged Kimi models + dynamic id resolution.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — choosing provider/route per request; relevance: route Kimi through Moonshot for reasoning vs Fireworks for non-thinking.

**Docs**
- [oc_providers_deepseek](oc_providers_deepseek.md) (planned, this series) — sibling OpenAI-compatible provider with its own thinking contract; relevance: contrast replay-thinking (DeepSeek) vs forced-off-thinking (Fireworks/Kimi).
- [oc_providers_gmi](oc_providers_gmi.md) (planned, this series) — multi-vendor aggregator incl. `gmi/moonshotai/Kimi-K2.5`; relevance: alternate route to the same Kimi family.
- [oc_providers_github_copilot_provider](oc_providers_github_copilot_provider.md) (planned, this series) — another bundled OpenAI-compatible provider; relevance: provider-plugin + transport-selection contrast.
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — thinking/effort levels; relevance: analog of the `/think` switch and forced-off behavior.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model-ref selection; relevance: `fireworks/<id>` custom model ref selection.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — `compat`/`thinkingFormat`/`supportsReasoningEffort`; relevance: the compat flags Fireworks's policy advertises (only `off` for Kimi).
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider/model routing; relevance: routing the same model through a different provider for reasoning.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing/proxy layer; relevance: aggregator/router behavior of Fireworks routers.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: how a hosted OpenAI-compatible provider is registered/keyed.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog reference; relevance: pre-cataloged vs dynamic model id resolution like Fireworks.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin anatomy; relevance: structural parallel of the Fireworks bundled plugin + thinking policy.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: where the Fireworks provider + `thinking-policy.ts` live.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the `/think` switch + provider-policy surface.

**Snippets**
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — Kimi provider plugin (dual-endpoint, reasoning surface); relevance: concrete Kimi provider definition + reasoning-field handling.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — router/aggregator routing; relevance: analog of Fireworks router-id resolution.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — per-api-type adapter dispatch; relevance: selecting the `openai-completions` path for Fireworks.
- [snippet_hermes_agent_core_think_scrubber](../../code_snippets/snippet_hermes_agent_core_think_scrubber.md) — strips/normalizes thinking; relevance: forcing thinking off / stripping reasoning params for Kimi.
- [snippet_hermes_agent_core_runtime_helpers_reasoning](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_reasoning.md) — reasoning runtime helpers; relevance: where the advertised reasoning-effort levels are applied.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registration; relevance: how the Fireworks plugin registers `fireworks`/`fireworks-ai`.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI chat-completions provider; relevance: the OpenAI-compatible archetype Fireworks follows.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery normalization; relevance: dynamic-resolution of custom `fireworks/<id>` refs.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planning; relevance: the two pre-cataloged Kimi entries + cloning the Fire Pass template.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider plugin; relevance: another routed/aggregated provider for comparison.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — model-switch CLI entry; relevance: `/think` switch + model-ref switching to/from Fireworks.

### oc_providers_github_copilot_provider (10t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: Copilot is wired in as a model provider/runtime.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: GitHub device-flow OAuth login.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the GitHub token exchanged for short-lived Copilot API tokens.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: device-login vs token import vs env-var resolution order.
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key OAuth extension; relevance: the device/PKCE-style flow class device-login belongs to.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Copilot fronts Claude/GPT/Gemini LLMs.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: `github-copilot/claude-opus-4.7` default + Anthropic Messages transport.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent-loop runtime; relevance: the Copilot SDK harness runtime option.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: Copilot CLI/SDK owning the low-level agent loop.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI providers; relevance: Copilot as an external model provider.

**Docs**
- [oc_providers_github_copilot_memory_search](oc_providers_github_copilot_memory_search.md) (planned, this series) — the embedding half of the same page; relevance: shared token-exchange path, split companion.
- [oc_providers_fireworks](oc_providers_fireworks.md) (planned, this series) — another bundled OpenAI-compatible provider; relevance: provider-plugin + model-ref contrast.
- [oc_providers_gmi](oc_providers_gmi.md) (planned, this series) — Copilot-Claude vs `gmi/anthropic/...`; relevance: subscription-fronted vs key-fronted access to the same models.
- [cc_authentication](../claude_code/cc_authentication.md) — subscription vs key auth; relevance: direct analog of Copilot subscription-login vs API key.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/OAuth failure modes; relevance: device-login TTY/token failure troubleshooting.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network errors; relevance: token-exchange/`/models` HTTPS failure handling.
- [pi_provider_auth](../pi/pi_provider_auth.md) — subscription-login provider auth; relevance: subscription-login analog incl. env-var fallback order.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: registering a subscription-fronted provider.
- [hermes_provider_minimax_oauth](../hermes_agent/hermes_provider_minimax_oauth.md) — OAuth-login provider; relevance: a concrete OAuth-login provider parallel to Copilot device-login.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — external coding-agent runtime; relevance: analog of the Copilot SDK harness `agentRuntime`.
- [band_adapter_codex](../band/band_adapter_codex.md) — Codex coding-agent adapter; relevance: an external coding-agent harness analog to Copilot's harness.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: the built-in `github-copilot` provider + token exchange.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: agent-runtime selection (built-in vs Copilot harness).

**Snippets**
- [snippet_hermes_agent_cli_copilot_auth](../../code_snippets/snippet_hermes_agent_cli_copilot_auth.md) — GitHub Copilot device auth; relevance: direct analog of `models auth login-github-copilot`.
- [snippet_hermes_agent_plugins_provider_copilot](../../code_snippets/snippet_hermes_agent_plugins_provider_copilot.md) — Copilot provider plugin; relevance: the provider plugin that fronts Copilot models.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — login/logout credential store; relevance: where the device-login token is stored.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback server; relevance: the device/OAuth login flow mechanics.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE OAuth flow; relevance: the PKCE/device-code flow class device-login uses.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: the `COPILOT_GITHUB_TOKEN > GH_TOKEN > GITHUB_TOKEN` priority order.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: inferring the Copilot auth choice from the token flag.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential ordering in auth profiles; relevance: device-login token precedence over env vars.
- [snippet_hermes_agent_core_anthropic_adapter_oauth](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_oauth.md) — Anthropic transport + OAuth; relevance: Copilot Claude ids use the Anthropic Messages transport.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: the Copilot Proxy / external-CLI transport option.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery; relevance: on-demand `/models` catalog refresh per account entitlement.

### oc_providers_github_copilot_memory_search (9t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: Copilot is wired in as the memory-search embedding provider.
- [Embedding](../../term_dictionary/term_embedding.md) — dense vector representation; relevance: Copilot serves embedding models for memory search.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: reuses the logged-in GitHub token (no separate key).
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: subscription reuse + token exchange for embeddings.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI providers; relevance: Copilot as an external embedding provider.
- [LLM](../../term_dictionary/term_llm.md) — foundation models; relevance: the embedding models discovered via the Copilot `/models` endpoint.
- [Categorical Embedding](../../term_dictionary/term_categorical_embedding.md) — learned vector encodings; relevance: embedding-provider concept the memory index relies on.
- [SQLite-Vec](../../term_dictionary/term_sqlite_vec.md) — vector store over SQLite; relevance: where memory-search embeddings are typically stored/queried.
- [FAISS](../../term_dictionary/term_faiss.md) — vector similarity index; relevance: the nearest-neighbor retrieval embeddings feed in memory search.

**Docs**
- [oc_providers_github_copilot_provider](oc_providers_github_copilot_provider.md) (planned, this series) — the model-provider half of the same page; relevance: shared token-exchange path, split companion.
- [oc_providers_deepseek](oc_providers_deepseek.md) (planned, this series) — provider auth/onboard pattern; relevance: contrast key-based provider auth vs Copilot subscription reuse.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — external memory providers catalog; relevance: the memory-provider selection surface this page configures.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — memory-provider plugin anatomy; relevance: how a memory/embedding provider is registered.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — persistent memory subsystem; relevance: the memory store embeddings index.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — search/storage backend; relevance: where embeddings are stored and queried.
- [cc_authentication](../claude_code/cc_authentication.md) — subscription vs key auth; relevance: subscription reuse for embeddings without a separate key.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth/key resolution; relevance: GitHub token resolution reused for `/embeddings`.
- [hermes_plugin_llm_access](../hermes_agent/hermes_plugin_llm_access.md) — plugin LLM/provider access; relevance: how a subsystem (memory) requests provider calls.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Copilot registered as a cloud embedding provider.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/token troubleshooting; relevance: "no embedding models → skip provider" token/entitlement failure modes.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory-search subsystem; relevance: the consumer of Copilot embeddings.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: the Copilot provider serving `/embeddings`.

**Snippets**
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory-search path; relevance: the exact path Copilot embeddings feed.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host-side embedding provider factory; relevance: the embedding-provider abstraction Copilot plugs into.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding input assembly; relevance: what gets sent to the `/embeddings` endpoint.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: the engine that requests embeddings and ranks memories.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: runtime that selects the configured embedding provider.
- [snippet_openclaw_memory_host_backend_config](../../code_snippets/snippet_openclaw_memory_host_backend_config.md) — memory backend config; relevance: `memorySearch.provider`/`model` configuration surface.
- [snippet_hermes_agent_cli_copilot_auth](../../code_snippets/snippet_hermes_agent_cli_copilot_auth.md) — Copilot device auth; relevance: the same GitHub-token resolution reused for embeddings.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: resolving the GitHub token for the embedding token exchange.

### oc_providers_gmi (10t · 11s · 11d · 2 repos)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being configured; relevance: the `@openclaw/gmi-provider` external plugin is configured here.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: GMI fronts many vendor LLM families behind one key.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted external GenAI; relevance: GMI Cloud is a hosted inference platform.
- [Model Router](../../term_dictionary/term_model_router.md) — routes a ref to a backing model; relevance: GMI routes `gmi/<vendor>/<model>` to Google/Anthropic/OpenAI/DeepSeek/Moonshot/Z.AI.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — choosing provider/route per request; relevance: GMI vs OpenRouter/DeepInfra/Together/direct-vendor route choice.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — secondary provider on failure; relevance: GMI is positioned as a fallback/secondary provider.
- [Model Failover](../../term_dictionary/term_model_failover.md) — switching models/providers on error; relevance: GMI for model fallback when a primary is unavailable.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — extension package; relevance: `@openclaw/gmi-provider` is an official external plugin.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: `gmi/anthropic/claude-sonnet-4.6` route example.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: `gmi/deepseek-ai/DeepSeek-V3.2` route example.

**Docs**
- [oc_providers_fireworks](oc_providers_fireworks.md) (planned, this series) — another aggregator/router-style OpenAI-compatible provider; relevance: routed-model comparison.
- [oc_providers_deepseek](oc_providers_deepseek.md) (planned, this series) — direct-vendor DeepSeek provider; relevance: direct vs GMI-routed DeepSeek access.
- [oc_providers_ds4](oc_providers_ds4.md) (planned, this series) — local server alternative; relevance: GMI's "choose a local provider instead" guidance points here.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model-ref selection + failover; relevance: provider/model-ref selection + fallback idiom.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — gateway/aggregator provider config; relevance: analog of GMI's provider config block.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth/key resolution; relevance: `GMI_API_KEY` + `onboard --auth-choice gmi-api-key`.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — cross-provider resilience model; relevance: direct analog of using GMI as a fallback provider.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider/model routing; relevance: how a `gmi/...` route resolves at request time.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: registering a hosted multi-vendor aggregator.
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — auxiliary/secondary provider config; relevance: configuring GMI as a secondary provider.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog reference; relevance: GMI's seeded multi-vendor route catalog ("seed, not a promise").

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: external provider-plugin registration for `gmi`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: fallback/secondary-provider selection at request time.

**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — multi-vendor aggregator routing; relevance: direct analog of GMI's one-key/many-vendor routing.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI chat-completions provider; relevance: GMI uses OpenAI-compatible chat semantics.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registration; relevance: registering the external `gmi` provider id + aliases.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider plugin; relevance: an aggregator plugin GMI is explicitly contrasted with.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — multi-vendor provider cluster; relevance: seeding many vendor routes under one provider, like GMI's catalog.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — model fallback + cooldown; relevance: GMI-as-fallback failover behavior.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — fallback context plumbing; relevance: how a secondary provider like GMI is invoked on failure.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — activating a fallback provider; relevance: the failover step GMI participates in.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog seed; relevance: the seeded GMI route ids catalog.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery; relevance: `models list --provider gmi` enumeration vs the static seed.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the external-plugin contract `@openclaw/gmi-provider` follows.


## Undigested Terms Plan

Per master Step 4e: OpenClaw provider vocabulary is digested as `oc_*` doc notes (these 8), NOT as new `term_dictionary` entries; the only term interaction is **linking existing** terms. Expected **0 new `term_dictionary` captures**.

| Term (appearing in source) | Disposition |
|---|---|
| DeepSeek, DeepSeek V4 / `reasoning_content` replay | Digested in `oc_providers_deepseek`; link existing `term_deepseek` + `term_chain_of_thought`. No new term. |
| ds4 / `antirez/ds4` local Metal server, `localService`, `--ctx`/Think Max | Digested in `oc_providers_ds4`; product-specific config, not a reusable cross-cutting term. Link `term_vllm`/`term_quantization`/`term_context_window`. No new term. |
| ElevenLabs, Scribe v2 / Scribe v2 Realtime, `ulaw_8000` | Digested in `oc_providers_elevenlabs`; link existing `term_text_to_speech`/`term_speech_to_text`/`term_voice_call`. No new term. |
| fal, Flux / Krea 2 / Seedance / HeyGen / `music_generate` | Digested in `oc_providers_fal`; model/endpoint names = config, not promoted. Link `term_diffusion_model`. No new term. |
| Fireworks, Fire Pass / Kimi router / forced-off thinking | Digested in `oc_providers_fireworks`; link `term_model_router`/`term_chain_of_thought`. Kimi/Moonshot referenced via the (other-sub-plan) `providers/moonshot` page, not promoted here. No new term. |
| GitHub Copilot device flow / SDK harness / Copilot Proxy / transport selection | Digested in `oc_providers_github_copilot_provider`; link `term_oauth`/`term_oauth_token`/`term_authentication`/`term_agent_harness`. No new term. |
| Copilot embeddings / memory search | Digested in `oc_providers_github_copilot_memory_search`; link existing `term_embedding`. No new term. |
| GMI Cloud, `gmi/<vendor>/<model>` multi-vendor routes | Digested in `oc_providers_gmi`; link `term_model_router`/`term_third_party_genai_services`. No new term. |

No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note was found in this batch. **0 new-term candidates.** (Augment Step 2d re-scans to confirm before locking.)

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). Gate table identical to the master 9-GATE definition; all must pass before commit.

| Gate | Check | How |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` on all 8 notes (YAML field order, `## Overview`/`## Related Notes` present, footer). |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/providers/<page>.md`; no invented config keys/model ids/env vars; config snippets verbatim. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one `building_block` each; every mapped section present (Section Coverage Map). |
| G4 | Cross-Reference | Per the LOCKED mapping: **≥8 term links · ≥10 snippet links · ≥10 doc links** + repo/sibling links per note, each with a relevance statement (relevance-selected, no padding). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after incremental reindex; 0 broken links. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` rows + repo/term inlinks); anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_deepseek oc_providers_ds4 oc_providers_elevenlabs oc_providers_fal oc_providers_fireworks oc_providers_github_copilot_provider oc_providers_github_copilot_memory_search oc_providers_gmi"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density: words (strip frontmatter) + code fences
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (words=$words code=$cb lines=$lines)"
  # G4 sibling-prefix presence (cross-ref to series siblings)
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) LINK in $n"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost / G6 broken-link: run after incremental reindex
bash scripts/update_notes_database.sh
# then /tessellum-fix-ghost-references and /tessellum-fix-broken-links per master
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Within caps (≤2500w / ≤6 code / ≤400 lines)? |
|---|---|---|---:|---:|---|
| 1 | oc_providers_deepseek | procedure | 600 | 3 | yes |
| 2 | oc_providers_ds4 | procedure | 700 | 6 (trim to ≤6) | yes |
| 3 | oc_providers_elevenlabs | procedure | 600 | 4 | yes |
| 4 | oc_providers_fal | procedure | 650 | 3 | yes |
| 5 | oc_providers_fireworks | procedure | 600 | 5 | yes |
| 6 | oc_providers_github_copilot_provider | procedure | 650 | 3 (subset of page's 3) | yes |
| 7 | oc_providers_github_copilot_memory_search | procedure | 350 | 1 | yes |
| 8 | oc_providers_gmi | procedure | 500 | 4 | yes |

No note approaches caps. `ds4.md` (6 fences) and `fireworks.md` (5 fences) are the densest; ds4 keeps its load-bearing `models.providers.ds4` config + `localService` + smoke-test fences and drops the redundant duplicate curl/test fences to stay ≤6. The `github-copilot` split keeps each note's code subset small.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify and add at execution; satisfies in-degree ≥1 / anti-island):

| New note | Candidate inbound from (outside `documentation/openclaw/`) |
|---|---|
| oc_providers_deepseek | `entry_openclaw_docs` (planned), `term_deepseek`, `repo_openclaw_extensions_llm_providers` |
| oc_providers_ds4 | `entry_openclaw_docs` (planned), `term_vllm` (local-server peer), `repo_openclaw_extensions_llm_providers` |
| oc_providers_elevenlabs | `entry_openclaw_docs` (planned), `term_text_to_speech`, `repo_openclaw_extensions_voice_speech` |
| oc_providers_fal | `entry_openclaw_docs` (planned), `term_diffusion_model`, `repo_openclaw_extensions_llm_providers` |
| oc_providers_fireworks | `entry_openclaw_docs` (planned), `term_model_router`, `repo_openclaw_extensions_llm_providers` |
| oc_providers_github_copilot_provider | `entry_openclaw_docs` (planned), `term_oauth_token`, `repo_openclaw_extensions_llm_providers` |
| oc_providers_github_copilot_memory_search | `entry_openclaw_docs` (planned), `term_embedding`, `repo_openclaw_memory` |
| oc_providers_gmi | `entry_openclaw_docs` (planned), `term_third_party_genai_services`, `repo_openclaw_extensions_llm_providers` |

`entry_openclaw_docs.md` → all 8 (primary discoverability spine). Reciprocal inlinks added per `/tessellum-add-inlinks` at execution.

## Pacing Rules (inherited from master)

One execution phase (8 notes, ≤30 fan-out cap easily satisfied). Re-read each source page at execution; reproduce config/JSON5 snippets verbatim; one `building_block: procedure` per note. Run all 8 gates before commit; incremental reindex per wave; verify `note_links` populated + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash` first; commit+push after the phase; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**What was locked (per-note counts — all floors met):**

| Note | Terms | Snippets | Docs (existing + planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_providers_deepseek | 10 | 11 | 11 (8 existing + 3 sibling) | 2 | YES |
| oc_providers_ds4 | 10 | 11 | 11 (9 existing + 2 sibling) | 2 | YES |
| oc_providers_elevenlabs | 10 | 11 | 11 (9 existing + 2 sibling) | 2 | YES |
| oc_providers_fal | 9 | 11 | 11 (8 existing + 3 sibling) | 2 | YES |
| oc_providers_fireworks | 10 | 11 | 11 (8 existing + 3 sibling) | 2 | YES |
| oc_providers_github_copilot_provider | 10 | 11 | 11 (8 existing + 3 sibling) | 2 | YES |
| oc_providers_github_copilot_memory_search | 9 | 11 | 11 (9 existing + 2 sibling) | 2 | YES |
| oc_providers_gmi | 10 | 11 | 11 (8 existing + 3 sibling) | 2 | YES |



**New richness surfaced by the re-read (beyond the original draft):** the entire `resources/documentation/hermes_agent/` provider/voice/memory doc corpus is a near-exact analog for these pages and was added per note (`hermes_inference_providers_cloud`, `hermes_model_provider_plugin`, `hermes_provider_routing(_proxies)`, `hermes_fallback_providers`, `hermes_local_self_hosted_llm`, `hermes_provider_ollama_local`, `hermes_provider_local_llm_mac`, `hermes_tts_providers`, `hermes_stt_transcription`, `hermes_voice_mode_cli`, `hermes_memory_provider_catalog/_plugin`, `hermes_persistent_memory`, `hermes_codex_runtime_setup`, `band_adapter_codex`). New relevant terms added: `term_model_catalog`, `term_provider_routing`, `term_fallback_provider`, `term_model_failover`, `term_reasoning_agent`, `term_kv_cache`, `term_auth_profile`, `term_realtime_transcription`, `term_voice_mode`, `term_multimodal`, `term_generative_model`, `term_genai`, `term_stable_diffusion`, `term_pkce`, `term_categorical_embedding`, `term_sqlite_vec`, `term_faiss`.

**New-term candidates:** **0.** Step 2d re-scan over all 7 re-read pages confirms the master's design decision holds — every OpenClaw provider-vocabulary item (DeepSeek V4 replay, ds4/`localService`, Scribe v2 Realtime/`ulaw_8000`, Flux/Krea/Seedance, Fire Pass/Kimi forced-off, Copilot device-flow/embeddings, GMI multi-vendor routes) is digested as one of these 8 `oc_*` doc notes OR links an EXISTING `term_dictionary` note. No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note. Best-fit glossary N/A (0 captures). The Undigested Terms Plan + Term-Note Authoring Requirements (N/A, 0 terms) sections are unchanged and remain valid.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 mandatory checkpoints (CP7 source counts spot-checked against the re-read in the Augmentation Report).

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | LOCKED Per-Note Related Notes Mapping present; every note ≥8 terms (9–10), ≥10 snippets (11), ≥10 docs (11), each link carries a `relevance:` statement. Count verified per note (table in Augmentation Report). |
| CP2 | 9-GATE present per batch (G1–G6, G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table has G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (updated to ≥8t/≥10s/≥10d), G5 Ghost detect+redirect, G6 Broken-link fix, G7/G8 Discoverability/in-degree≥1. Single execution phase, one gate table. |
| CP4 | Plan size | **PASS** | 8 notes ≪ 30; single execution phase. |
| CP5 | Format derived (not invented) | **PASS** | YAML/body format inherited verbatim from master Format Definition, which is derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` / source-mirrored H2 / `## Related Notes` / `## References` / bold footer; `building_block: procedure`). Validation Scripts assert `## Overview`/`## Related Notes` + `source_url`. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 8 notes 350–700w, ≤6 code fences, well under ≤2500w/≤6 code/≤400 lines. ds4 (6 fences) trimmed to load-bearing config + smoke-test set. No borderline note. |
| CP7 | Sources measured | **PASS** | All 7 pages re-read 2026-06-21 (Augmentation Report); measured words match the plan's Source table (5,253w total); no page >2,500w; the one split (github-copilot, 1,129w) is on task-cluster, not size, boundary. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (8 rows, all `Disposition: link existing / No new term`); `## Term-Note Authoring Requirements` present (N/A, 0 terms, with the inherited-from-master fallback if Step 2d surfaces one). Step 2d re-scan over the re-read: 0 new-term candidates. |
| CP8f | Slug specificity / collision (all notes) | **PASS** | 0 new term slugs to specificity-audit. Collision audit generalized to all 8 planned `oc_providers_*` doc notes: none duplicates an existing `term_dictionary`/`documentation` note (provider how-tos vs `term_deepseek`/`term_openclaw` concept notes — link, not duplicate; the 8 `oc_providers_*` filenames DB-confirmed not-yet-created). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
