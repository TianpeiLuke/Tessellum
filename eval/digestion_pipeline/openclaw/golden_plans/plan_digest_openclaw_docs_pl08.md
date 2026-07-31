---
title: Sub-Plan pl08 — OpenClaw Docs: Plugins (Reference: cohere → deepseek)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/cohere", "plugins/reference/comfy", "plugins/reference/copilot", "plugins/reference/copilot-proxy", "plugins/reference/deepgram", "plugins/reference/deepinfra", "plugins/reference/deepseek"]
---

# Sub-Plan pl08: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format, dedup (3-way), 9-GATE, cross-refs,
> and entry-point wiring are ALL inherited from the master; only pl08-specific decisions appear below.

## Scope

The seven alphabetically-contiguous **plugin reference cards** `cohere` → `deepseek` from
`docs.openclaw.ai/plugins/reference/`. Each is a tiny machine-generated catalog stub (≈50–60 words) that
declares one OpenClaw plugin: its npm/ClawHub package, install route, and the runtime *surface* it
contributes (provider id(s) and/or capability contracts such as `imageGenerationProviders`,
`mediaUnderstandingProviders`, `speechProviders`, `realtimeTranscriptionProviders`). Five register a model
**provider** (cohere, comfy, copilot-proxy, deepinfra, deepseek), one registers the **Copilot agent
runtime** (copilot), and one is a pure-**contract** media/transcription plugin (deepgram). Priority **P3**
(Phase C — plugin reference sprawl): these cards reference the provider/runtime/contract vocabulary defined
by the P1/P2 sub-plans, so they digest last. The code-side counterparts
(`repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`, the
`snippet_openclaw_provider_*` / `snippet_openclaw_speech_*` snippets) are **LINKED, not recreated**.

**Source**: OpenClaw docs, 7 pages, 388 measured words (mirror `inbox/openclaw_docs/plugins/reference/`).
**Planned: 7 notes** (1 per page — these stubs are far too small to split or merge; the master's "11
(est.)" is revised down at authoring per the measured sizes).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| cohere | plugins/reference/cohere | 51 | 0 | 3 | 0 | model |
| comfy | plugins/reference/comfy | 58 | 0 | 3 | 0 | model |
| copilot | plugins/reference/copilot | 51 | 0 | 3 | 0 | model |
| copilot-proxy | plugins/reference/copilot-proxy | 53 | 0 | 2 | 0 | model |
| deepgram | plugins/reference/deepgram | 61 | 0 | 3 | 0 | model |
| deepinfra | plugins/reference/deepinfra | 60 | 0 | 3 | 0 | model |
| deepseek | plugins/reference/deepseek | 54 | 0 | 3 | 0 | model |

H2 set per page is fixed: `## Distribution`, `## Surface`, `## Related docs` (copilot-proxy omits
`## Related docs`). No H3, no code fences on any page. Total: **388 words**.

## Content Strategy

- **Prioritize**: the *Surface* line of each card — it is the load-bearing fact (which provider id and which
  capability contracts the plugin contributes). The Distribution line (package id + install route:
  included-in-OpenClaw / npm / ClawHub `clawhub:@openclaw/<pkg>`) is the second fact. Each note is a compact
  reference card describing one packaged plugin.
- **Split**: **none.** Every page is ~50–60 words, one BB, far below all caps; splitting would create
  sub-stub fragments. One note per page.
- **Merge**: **none.** Each plugin is a distinct distributable unit with its own package id and surface;
  merging would conflate independent ClawHub packages and break 1:1 source→note grounding (G2).
- **Link-out (do NOT inline)**: the *provider configuration* pages these cards point to
  (`/providers/cohere`, `/providers/comfy`, `/providers/deepgram`, `/providers/deepinfra`,
  `/providers/deepseek`, `/plugins/copilot`) are owned by other sub-plans (Providers `pr02`/`pr03`, Plugins
  `pl03`); cite them in `## References` as the upstream config doc, do not duplicate their content. Term
  definitions (`term_provider_plugin`, `term_llm`, `term_speech_to_text`, …) are linked, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_cohere.md` | model | cohere.md: Distribution, Surface, Related docs | 230 | Reference card for the OpenClaw Cohere provider plugin (`@openclaw/cohere-provider`): distribution/install route (bundled + npm + ClawHub) and the `cohere` provider surface it registers. |
| 2 | `oc_plugins_reference_comfy.md` | model | comfy.md: Distribution, Surface, Related docs | 240 | Reference card for the ComfyUI provider plugin (`@openclaw/comfy-provider`, bundled): registers the `comfy` provider plus image/music/video generation contracts. |
| 3 | `oc_plugins_reference_copilot.md` | model | copilot.md: Distribution, Surface, Related docs | 230 | Reference card for the Copilot plugin (`@openclaw/copilot`, npm + ClawHub): registers the GitHub Copilot agent runtime (surface `plugin`). |
| 4 | `oc_plugins_reference_copilot_proxy.md` | model | copilot-proxy.md: Distribution, Surface | 220 | Reference card for the Copilot Proxy provider plugin (`@openclaw/copilot-proxy`, bundled): registers the `copilot-proxy` model provider. |
| 5 | `oc_plugins_reference_deepgram.md` | model | deepgram.md: Distribution, Surface, Related docs | 240 | Reference card for the Deepgram plugin (`@openclaw/deepgram-provider`, bundled): contributes the media-understanding and realtime-transcription provider contracts. |
| 6 | `oc_plugins_reference_deepinfra.md` | model | deepinfra.md: Distribution, Surface, Related docs | 245 | Reference card for the DeepInfra provider plugin (`@openclaw/deepinfra-provider`, npm + ClawHub): registers the `deepinfra` provider plus image/media-understanding/embedding/speech/video contracts. |
| 7 | `oc_plugins_reference_deepseek.md` | model | deepseek.md: Distribution, Surface, Related docs | 230 | Reference card for the DeepSeek provider plugin (`@openclaw/deepseek-provider`, npm + ClawHub): registers the `deepseek` model provider. |

Filenames apply the master rule (`oc_` + full slug, `/` and `-` → `_`): `plugins/reference/copilot-proxy` →
`oc_plugins_reference_copilot_proxy.md`. No aspect suffixes (no splits).

## Section Coverage Map

```
plugins/reference/cohere.md
├── Distribution (package @openclaw/cohere-provider; bundled+npm+ClawHub) → note 1
├── Surface (providers: cohere) ──────────────────────────────────────── → note 1
└── Related docs (/providers/cohere) ────────────────────────────────── → note 1 (## References)
plugins/reference/comfy.md
├── Distribution (package @openclaw/comfy-provider; bundled) ─────────── → note 2
├── Surface (providers: comfy; contracts: image/music/video generation) → note 2
└── Related docs (/providers/comfy) ─────────────────────────────────── → note 2 (## References)
plugins/reference/copilot.md
├── Distribution (package @openclaw/copilot; npm+ClawHub) ────────────── → note 3
├── Surface (plugin — GitHub Copilot agent runtime) ─────────────────── → note 3
└── Related docs (/plugins/copilot) ─────────────────────────────────── → note 3 (## References)
plugins/reference/copilot-proxy.md
├── Distribution (package @openclaw/copilot-proxy; bundled) ──────────── → note 4
└── Surface (providers: copilot-proxy) ──────────────────────────────── → note 4
plugins/reference/deepgram.md
├── Distribution (package @openclaw/deepgram-provider; bundled) ──────── → note 5
├── Surface (contracts: mediaUnderstanding, realtimeTranscription) ───── → note 5
└── Related docs (/providers/deepgram) ──────────────────────────────── → note 5 (## References)
plugins/reference/deepinfra.md
├── Distribution (package @openclaw/deepinfra-provider; npm+ClawHub) ─── → note 6
├── Surface (providers: deepinfra; 5 contracts) ─────────────────────── → note 6
└── Related docs (/providers/deepinfra) ─────────────────────────────── → note 6 (## References)
plugins/reference/deepseek.md
├── Distribution (package @openclaw/deepseek-provider; npm+ClawHub) ──── → note 7
├── Surface (providers: deepseek) ───────────────────────────────────── → note 7
└── Related docs (/providers/deepseek) ──────────────────────────────── → note 7 (## References)
```
No orphaned sections. Every H2 of every page maps to its 1:1 note. The `Related docs` link on each page is
preserved as an external pointer in that note's `## References` (the target page is owned by another
sub-plan and is NOT duplicated).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are ~50–60 words, single-BB, 0 code fences — orders of magnitude below the ≤2500w / ≤6-code / ≤400-line caps. 1 page → 1 note; no splits, no merges. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (388 words total). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **model ×7** (reference/registry descriptor cards — each documents a packaged plugin's
  fixed schema: package id, install route, surface contracts; per the master BB skew "model = reference
  schemas"). No procedure/concept/argument notes in this sub-plan.
- Est. digest words ≈ **1,635** (avg ≈ 234/note). 0 source code fences; notes reproduce the package id and
  surface line verbatim inline (no fenced blocks needed; each note stays ≤6 code blocks trivially).
- Cross-refs (LOCKED at xref-augment 2026-06-21): each note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** (≥5 EXISTING
  `snippet_openclaw_*` code counterpart, each with a relevance statement. See **Per-Note Related Notes

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms
`../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`; repos
`../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`; entry points
candidate set. Sibling `oc_*` docs (this series) and `entry_openclaw_docs` do not exist yet → marked
(each note carries far more than 5 existing docs, so the planned siblings are pure bonus, not floor-padding).

> Terms confirmed **MISSING** (do NOT cite; would be ghosts; re-verified 2026-06-21): `term_cohere`,
> `term_github_copilot`, `term_image_generation`, `term_video_generation`, `term_music_generation`,
> `term_media_understanding`, `term_voice`, `term_ollama`, `term_anthropic`, `term_amazon_bedrock`,
> `term_clawhub`. The unrelated internal `project_tt_copilot*` notes are **TT Copilot** (not GitHub
> Copilot) — must NOT be linked from note 3. `entry_openclaw_docs` is confirmed not-yet-created (planned
> W1 master pre-step) → cited as (planned).

### oc_plugins_reference_cohere (8t · 11s · 11d)

Cohere = third-party GenAI provider plugin registering the `cohere` provider id (chat + embeddings/rerank);
bundled + npm + ClawHub. Relevance pivots: provider-plugin registration, model catalog, embeddings.

**Terms** (8)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — OpenClaw plugin that registers a model/inference provider; relevance: cohere.md's Surface line registers exactly this (`providers: cohere`).
- [LLM](../../term_dictionary/term_llm.md) — large language model served by a provider; relevance: the Cohere plugin exposes Cohere chat LLMs to OpenClaw agents.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external hosted model APIs integrated via plugins; relevance: Cohere is an external SaaS GenAI vendor the plugin wraps.
- [model catalog](../../term_dictionary/term_model_catalog.md) — registry of available models per provider; relevance: registering the cohere provider adds its models to OpenClaw's catalog.
- [embedding](../../term_dictionary/term_embedding.md) — dense vector representation of text; relevance: Cohere's headline capability is its embed/rerank models surfaced through this provider.
- [vector database](../../term_dictionary/term_vector_database.md) — store for embedding similarity search; relevance: Cohere embeddings are consumed by vector stores for retrieval/memory.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: cohere.md's Distribution lists `npm` as an install route for `@openclaw/cohere-provider`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this plugin extends; relevance: the plugin is "included in OpenClaw" and contributes to its provider surface.

**Docs** (11: 9 existing + 2 planned)
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — how a model provider plugin is structured/registered; relevance: direct analog of the cohere provider-plugin pattern.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — catalog of cloud LLM providers; relevance: Cohere is one such cloud provider integrated the same way.
- [Hermes — Plugin LLM Access](../hermes_agent/hermes_plugin_llm_access.md) — how plugins gain LLM access; relevance: the cohere provider grants agents access to Cohere LLMs.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy (providers/contracts); relevance: explains the `providers:` surface cohere.md declares.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog schema/fields; relevance: cohere models land in this catalog when the plugin registers.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — procedure to add a provider; relevance: how a provider like cohere is wired in.
- [Hermes — Env Vars (Providers/Auth/Tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider credential env vars; relevance: Cohere API key configuration for the provider.
- [pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom provider in a sibling agent; relevance: cross-tool analog of registering `cohere`.
- [pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: Cohere as a cloud provider in the broader coding-agent ecosystem.
- [oc_plugins_reference_deepinfra](oc_plugins_reference_deepinfra.md) — sibling embedding-capable provider (planned, this series); relevance: DeepInfra also surfaces `memoryEmbeddingProviders`.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code home of the LLM provider plugins; relevance: the `@openclaw/cohere-provider` source lives here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — parent extensions monorepo; relevance: container for the provider plugin packages.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw core repo; relevance: the gateway that loads the plugin.

**Snippets** (11)
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — an OpenClaw provider plugin implementation; relevance: same provider-plugin shape as cohere-provider.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider plugin; relevance: Cohere's chat API is wired with the same provider pattern.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: cohere models enter the catalog on registration.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planning; relevance: how a provider's models are planned into the catalog.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry-point declarations; relevance: cohere-provider declares its surface via these entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package.json contract; relevance: defines the `@openclaw/cohere-provider` package shape + install route.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/activate lifecycle; relevance: how the bundled cohere plugin is loaded.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding host wiring; relevance: Cohere embeddings feed memory hosts.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding input preparation; relevance: input path for Cohere embed calls.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry in a sibling agent; relevance: analog of how `cohere` registers.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin example; relevance: structural twin of the cohere-provider plugin.

### oc_plugins_reference_comfy (8t · 11s · 11d)

ComfyUI = bundled local image/music/video generation provider (diffusion-based); registers `comfy` provider
plus `imageGenerationProviders`, `musicGenerationProviders`, `videoGenerationProviders` contracts.

**Terms** (8)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a provider+contracts; relevance: comfy.md's Surface registers `providers: comfy` plus three media-gen contracts.
- [diffusion model](../../term_dictionary/term_diffusion_model.md) — iterative-denoising generative model; relevance: ComfyUI is a node-graph UI for diffusion image/video pipelines.
- [stable diffusion](../../term_dictionary/term_stable_diffusion.md) — latent diffusion image model; relevance: ComfyUI's canonical backend model family.
- [multimodal](../../term_dictionary/term_multimodal.md) — spanning text/image/audio/video; relevance: comfy contributes image + music + video generation surfaces.
- [generative model](../../term_dictionary/term_generative_model.md) — model that synthesizes new content; relevance: ComfyUI generates images/music/video.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external generative backends; relevance: ComfyUI is an external generation engine the plugin fronts.
- [model catalog](../../term_dictionary/term_model_catalog.md) — provider/model registry; relevance: the comfy provider's generation models register here.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: comfy-provider is "included in OpenClaw".

**Docs** (11: 10 existing + 1 planned)
- [Hermes — Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider plugin pattern; relevance: direct analog of comfy's `imageGenerationProviders` contract.
- [Hermes — Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin; relevance: matches comfy's `videoGenerationProviders` contract.
- [Hermes — Image Generation](../hermes_agent/hermes_image_generation.md) — image generation feature/tool; relevance: the user-facing capability comfy backs.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface/contract taxonomy; relevance: explains the three generation contracts comfy declares.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin structure; relevance: comfy registers a provider the same way.
- [Hermes — Docker Tools / Local Inference](../hermes_agent/hermes_docker_tools_local_inference.md) — running local inference services; relevance: ComfyUI is a locally hosted generation server.
- [Hermes — Local / Self-hosted LLM](../hermes_agent/hermes_local_self_hosted_llm.md) — local self-hosted model serving; relevance: comfy is the local-generation analog (self-hosted backend).
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — catalog schema; relevance: comfy generation models register into the catalog.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin system overview; relevance: how the bundled comfy plugin participates.
- [pi — Cloud Providers](../pi/pi_cloud_providers.md) — provider config in sibling agent; relevance: cross-tool view of registering a generation provider.
- [oc_plugins_reference_deepinfra](oc_plugins_reference_deepinfra.md) — sibling provider with image+video contracts (planned, this series); relevance: DeepInfra also declares image/video generation.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM/generation provider plugin code; relevance: `@openclaw/comfy-provider` source.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions monorepo; relevance: container for comfy-provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core repo; relevance: bundles the comfy plugin.

**Snippets** (11)
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch routing; relevance: how an image-gen provider like comfy is invoked.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: matches comfy's video contract.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image generation tool; relevance: user-facing tool comfy provider serves.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video generation tool; relevance: comfy backs this tool path.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local-server provider plugin; relevance: same local-backend pattern as the ComfyUI server.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — catalog assembly; relevance: comfy generation models enter catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planner; relevance: planning comfy's models into the catalog.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: comfy-provider declares its three contracts via entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: defines `@openclaw/comfy-provider` package shape.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: load/activate of the bundled comfy plugin.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: structural analog of comfy-provider.

### oc_plugins_reference_copilot (8t · 10s · 11d)

The only **agent-runtime** plugin here: registers the GitHub Copilot agent runtime (surface `plugin`, not a
model provider); npm + ClawHub. Relevance pivots: agent runtime/harness, plugin SDK, OAuth, ACP.

**Terms** (8)
- [autonomous coding agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: GitHub Copilot is the agent runtime this plugin registers.
- [agent harness](../../term_dictionary/term_agent_harness.md) — wrapper running an agent's loop; relevance: the Copilot plugin registers Copilot as a runtime/harness.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin contributing a surface; relevance: this plugin contributes the `plugin` (runtime) surface, contrasted with provider surfaces.
- [plugin SDK](../../term_dictionary/term_plugin_sdk.md) — SDK for authoring plugins; relevance: copilot.md's package is built on the plugin SDK runtime surface.
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — declares plugin metadata/surface; relevance: the copilot plugin's manifest declares its runtime registration.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — protocol bridging editors/agents; relevance: Copilot agent runtimes are surfaced via ACP-style bridging.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — delegated auth credential; relevance: GitHub Copilot auth uses OAuth tokens.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: the plugin registers the runtime into OpenClaw.

**Docs** (11: 9 existing + 2 planned)
- [Hermes — Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — runtime that hosts providers/agents; relevance: the runtime surface the Copilot plugin plugs into.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface taxonomy incl. `plugin`; relevance: explains copilot.md's bare `plugin` surface.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin system overview; relevance: how a runtime-registering plugin participates.
- [Hermes — ACP Editor Integration](../hermes_agent/hermes_acp_editor_integration.md) — ACP-based editor/agent bridging; relevance: Copilot agent runtime integration path.
- [band — Adapter: Codex](../band/band_adapter_codex.md) — coding-agent adapter example; relevance: analog of adapting an external coding agent (Copilot) as a runtime.
- [band — Creating Adapters (Implementation)](../band/band_creating_adapters_implementation.md) — how to implement a coding-agent adapter; relevance: parallels registering Copilot as a runtime.
- [band — Coding Agents Deployment](../band/band_coding_agents_deployment.md) — deploying coding agents; relevance: Copilot runtime deployment context.
- [band — Connect Remote Agent](../band/band_connect_remote_agent.md) — connecting an external agent runtime; relevance: Copilot is an external runtime connected via the plugin.
- [claude_code — Plugin Caching & Troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — coding-agent plugin operations; relevance: cross-tool plugin lifecycle analog.
- [oc_plugins_reference_copilot_proxy](oc_plugins_reference_copilot_proxy.md) — sibling Copilot integration as a provider (planned, this series); relevance: the model-provider counterpart to this runtime plugin.

**Repos** (4)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime code; relevance: where agent-runtime registration (Copilot) lands.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions monorepo; relevance: `@openclaw/copilot` plugin source.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core repo; relevance: loads the runtime plugin.

**Snippets** (10)
- [snippet_hermes_agent_plugins_provider_copilot](../../code_snippets/snippet_hermes_agent_plugins_provider_copilot.md) — Copilot provider/auth integration; relevance: closest code counterpart to the Copilot plugin.
- [snippet_hermes_agent_cli_copilot_auth](../../code_snippets/snippet_hermes_agent_cli_copilot_auth.md) — Copilot OAuth auth flow; relevance: the GitHub Copilot OAuth credentialing this plugin needs.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry declarations; relevance: the `plugin` runtime surface is declared via these entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: defines the `@openclaw/copilot` package + install route.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: load/activate of the Copilot runtime plugin.
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — ACP session init; relevance: agent-runtime session bring-up for Copilot-style runtimes.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: hosting an external agent runtime over ACP.
- [snippet_openclaw_acp_translator_cancel](../../code_snippets/snippet_openclaw_acp_translator_cancel.md) — ACP cancellation; relevance: runtime lifecycle control for agent runtimes.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent/model catalog; relevance: how runtime+model availability is catalogued.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: resolves the Copilot OAuth credential.

### oc_plugins_reference_copilot_proxy (8t · 11s · 11d)

Copilot Proxy = bundled **model provider** that proxies Copilot's models behind the `copilot-proxy` provider
id (contrast with note 3's runtime plugin). Relevance pivots: provider plugin, reverse proxy, OAuth.

**Terms** (8)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a model provider; relevance: copilot-proxy.md's Surface registers `providers: copilot-proxy`.
- [LLM](../../term_dictionary/term_llm.md) — large language model exposed by a provider; relevance: the proxy exposes Copilot's underlying LLMs as a provider.
- [reverse proxy](../../term_dictionary/term_reverse_proxy.md) — intermediary fronting an upstream service; relevance: copilot-proxy proxies Copilot's model endpoints.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — delegated credential; relevance: proxying Copilot models requires the GitHub Copilot OAuth token.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external model APIs; relevance: Copilot's models are an external GenAI backend.
- [model catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: proxied Copilot models register into the catalog.
- [model router](../../term_dictionary/term_model_router.md) — routes requests across providers/models; relevance: the proxy participates in routing requests to Copilot models.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: copilot-proxy-provider is "included in OpenClaw".

**Docs** (11: 9 existing + 2 planned)
- [Hermes — Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing and proxy patterns; relevance: copilot-proxy is exactly a provider-proxy.
- [Hermes — Subscription Proxy](../hermes_agent/hermes_subscription_proxy.md) — proxying a subscription-backed model service; relevance: Copilot is a subscription service proxied as a provider.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin structure; relevance: copilot-proxy registers a provider this way.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: proxied Copilot models appear as a cloud provider.
- [Hermes — Plugin LLM Access](../hermes_agent/hermes_plugin_llm_access.md) — plugin LLM access; relevance: the proxy grants access to Copilot LLMs.
- [Hermes — Credential Pools](../hermes_agent/hermes_credential_pools.md) — pooling provider credentials; relevance: managing the Copilot OAuth credential for the proxy.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — catalog schema; relevance: proxied models register here.
- [pi — Provider Auth](../pi/pi_provider_auth.md) — provider auth in sibling agent; relevance: OAuth-based provider auth analog for the proxy.
- [pi — Model Overrides / Compat](../pi/pi_model_overrides_compat.md) — model override/compat config; relevance: proxied Copilot models need compat overrides.
- [oc_plugins_reference_copilot](oc_plugins_reference_copilot.md) — sibling Copilot runtime plugin (planned, this series); relevance: the runtime counterpart to this provider-proxy.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugin code; relevance: `@openclaw/copilot-proxy` source.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions monorepo; relevance: container for copilot-proxy.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core repo; relevance: bundles copilot-proxy.

**Snippets** (11)
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator/proxy provider plugin; relevance: closest pattern to a proxying provider.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias/pricing lookup; relevance: proxied models need alias resolution.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a provider plugin implementation; relevance: same provider-plugin shape as copilot-proxy.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: proxied endpoints often expose an OpenAI-compatible surface.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — catalog assembly; relevance: proxied Copilot models register here.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planner; relevance: planning proxied models into the catalog.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: copilot-proxy declares its provider surface via entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: defines `@openclaw/copilot-proxy` package shape.
- [snippet_hermes_agent_cli_copilot_auth](../../code_snippets/snippet_hermes_agent_cli_copilot_auth.md) — Copilot OAuth flow; relevance: the OAuth credential the proxy reuses.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential resolution; relevance: resolving the Copilot credential for proxying.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: how `copilot-proxy` registers as a provider.

### oc_plugins_reference_deepgram (10t · 11s · 11d)

Pure-**contract** plugin (no `providers:` id): contributes `mediaUnderstandingProviders` +
`realtimeTranscriptionProviders` (STT/voice). EXACT code counterpart exists: `snippet_openclaw_speech_deepgram_stt`.

**Terms** (10)
- [speech-to-text](../../term_dictionary/term_speech_to_text.md) — audio→text transcription; relevance: Deepgram's core capability and the realtime-transcription contract.
- [realtime transcription](../../term_dictionary/term_realtime_transcription.md) — streaming live STT; relevance: deepgram.md declares `realtimeTranscriptionProviders` directly.
- [multimodal](../../term_dictionary/term_multimodal.md) — spanning audio/text/etc; relevance: media-understanding contract handles non-text media.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin contributing surfaces; relevance: deepgram contributes two capability contracts.
- [websocket](../../term_dictionary/term_websocket.md) — bidirectional streaming transport; relevance: realtime transcription streams audio over websockets.
- [SSE (Server-Sent Events)](../../term_dictionary/term_sse.md) — server push streaming; relevance: streaming transcription results to clients.
- [voice call](../../term_dictionary/term_voice_call.md) — live audio session; relevance: Deepgram transcribes voice-call media streams.
- [voice mode](../../term_dictionary/term_voice_mode.md) — agent voice interaction mode; relevance: realtime transcription powers voice-mode input.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: Deepgram is an external transcription SaaS.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: deepgram-provider is "included in OpenClaw".

**Docs** (11: 10 existing + 1 planned)
- [Hermes — STT / Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription; relevance: direct analog of Deepgram's transcription contract.
- [Hermes — TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the speech-provider family Deepgram sits alongside.
- [Hermes — Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI; relevance: realtime transcription feeds voice mode.
- [Hermes — Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice mode usage; relevance: transcription is the input half of voice mode.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface/contract taxonomy; relevance: explains the contract-only surface deepgram declares.
- [Hermes — Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — media/tool gateway; relevance: transcription is routed through the media/tool path.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin structure; relevance: deepgram is a contract-contributing plugin variant.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin system; relevance: how a contract-only plugin participates.
- [claude_code — Voice Dictation](../claude_code/cc_voice_dictation.md) — coding-agent voice dictation; relevance: cross-tool STT/voice-input analog.
- [oc_plugins_reference_deepinfra](oc_plugins_reference_deepinfra.md) — sibling provider also declaring media-understanding (planned, this series); relevance: shared `mediaUnderstandingProviders` contract.

**Repos** (4)
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension code; relevance: `@openclaw/deepgram-provider` (STT/transcription) source.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel code; relevance: consumer of realtime transcription on calls.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions monorepo; relevance: container for deepgram-provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core repo; relevance: bundles the deepgram plugin.

**Snippets** (11)
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT implementation; relevance: EXACT code counterpart of this plugin.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: realtime transcription on call media (Deepgram path).
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: transcription stage of the speech pipeline.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: relaying Deepgram transcription results.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — call media audio stream; relevance: the audio input Deepgram transcribes.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: sibling-agent transcription analog.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — TTS speech plugin; relevance: sibling speech-provider in the same voice-speech extension family.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: deepgram declares its two contracts via entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: defines `@openclaw/deepgram-provider` package shape.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice call manager; relevance: orchestrates transcription on live calls.

### oc_plugins_reference_deepinfra (10t · 11s · 11d)

Broadest surface here: provider `deepinfra` + 5 contracts (`imageGenerationProviders`,
`mediaUnderstandingProviders`, `memoryEmbeddingProviders`, `speechProviders`, `videoGenerationProviders`);
npm + ClawHub. OpenAI-compatible inference host.

**Terms** (10)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering provider+contracts; relevance: deepinfra.md registers `providers: deepinfra` plus five contracts.
- [LLM](../../term_dictionary/term_llm.md) — hosted large language model; relevance: DeepInfra hosts open LLMs as the `deepinfra` provider.
- [embedding](../../term_dictionary/term_embedding.md) — dense text vectors; relevance: deepinfra declares `memoryEmbeddingProviders`.
- [vector database](../../term_dictionary/term_vector_database.md) — embedding store; relevance: DeepInfra embeddings feed vector stores/memory.
- [speech-to-text](../../term_dictionary/term_speech_to_text.md) — audio transcription; relevance: deepinfra's `speechProviders` covers speech.
- [text-to-speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: `speechProviders` contract spans TTS.
- [multimodal](../../term_dictionary/term_multimodal.md) — across image/audio/video; relevance: deepinfra spans image gen, media understanding, video gen.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external model host; relevance: DeepInfra is an external inference SaaS.
- [model catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: deepinfra's many models register into the catalog.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: the plugin extends OpenClaw's provider surface.

**Docs** (11: 9 existing + 2 planned)
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: DeepInfra is a cloud inference host.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin structure; relevance: deepinfra registers a provider this way.
- [Hermes — Memory Provider Catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory/embedding provider catalog; relevance: deepinfra's `memoryEmbeddingProviders` contract.
- [Hermes — Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-gen provider; relevance: deepinfra's `imageGenerationProviders` contract.
- [Hermes — Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider; relevance: deepinfra's `videoGenerationProviders` contract.
- [Hermes — STT / Transcription](../hermes_agent/hermes_stt_transcription.md) — speech transcription; relevance: deepinfra's `speechProviders` contract.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface/contract taxonomy; relevance: explains deepinfra's five declared contracts.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — catalog schema; relevance: deepinfra models register into the catalog.
- [pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: DeepInfra as a cloud provider in a sibling agent.
- [oc_plugins_reference_cohere](oc_plugins_reference_cohere.md) — sibling embedding provider (planned, this series); relevance: shared embedding capability.
- [oc_plugins_reference_deepgram](oc_plugins_reference_deepgram.md) — sibling media-understanding plugin (planned, this series); relevance: shared `mediaUnderstandingProviders` contract.

**Repos** (4)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugin code; relevance: `@openclaw/deepinfra-provider` source.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension code; relevance: deepinfra's `speechProviders` contract.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions monorepo; relevance: container for deepinfra-provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core repo; relevance: loads the deepinfra plugin.

**Snippets** (11)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: DeepInfra exposes an OpenAI-compatible inference endpoint.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator/host provider; relevance: DeepInfra is a multi-model inference host like an aggregator.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding host; relevance: deepinfra's `memoryEmbeddingProviders` feeds this.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: input path for deepinfra embeddings.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: deepinfra's image-generation contract.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: deepinfra's video-generation contract.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: deepinfra's speech contract.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — catalog assembly; relevance: deepinfra's models register here.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planner; relevance: planning deepinfra's many models into the catalog.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: deepinfra declares its five contracts via entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: defines `@openclaw/deepinfra-provider` package shape.

### oc_plugins_reference_deepseek (9t · 10s · 11d)

DeepSeek = chat/reasoning **model provider** (`providers: deepseek`); npm + ClawHub. Has its own
`term_deepseek`. OpenAI-compatible API surface; strong at function-calling/reasoning.

**Terms** (9)
- [DeepSeek](../../term_dictionary/term_deepseek.md) — the DeepSeek model family/provider; relevance: this plugin registers the `deepseek` provider — exact subject match.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a provider; relevance: deepseek.md's Surface registers `providers: deepseek`.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: DeepSeek chat/reasoning LLMs exposed via the provider.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external model API; relevance: DeepSeek is an external SaaS provider.
- [model catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: DeepSeek models register into the catalog.
- [function calling](../../term_dictionary/term_function_calling.md) — structured tool invocation; relevance: DeepSeek supports function/tool calling consumed by agents.
- [model router](../../term_dictionary/term_model_router.md) — routes across models/providers; relevance: DeepSeek as a routing target/fallback.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: deepseek.md's Distribution lists npm install route.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: the plugin extends OpenClaw's provider surface.

**Docs** (11: 9 existing + 2 planned)
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin structure; relevance: deepseek registers a provider this way.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: DeepSeek is a cloud LLM provider.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — procedure to add a provider; relevance: how DeepSeek is wired in.
- [Hermes — Plugin LLM Access](../hermes_agent/hermes_plugin_llm_access.md) — plugin LLM access; relevance: deepseek provider grants access to DeepSeek LLMs.
- [Hermes — Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback/failover; relevance: DeepSeek commonly used as a low-cost fallback provider.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — catalog schema; relevance: DeepSeek models register here.
- [Hermes — Env Vars (Providers/Auth/Tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider credential env vars; relevance: DeepSeek API key configuration.
- [pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: DeepSeek as a cloud provider in a sibling agent.
- [pi — Model Overrides / Compat](../pi/pi_model_overrides_compat.md) — model override/compat; relevance: DeepSeek's OpenAI-compatible surface needs compat overrides.
- [oc_plugins_reference_deepinfra](oc_plugins_reference_deepinfra.md) — sibling provider plugin (planned, this series); relevance: adjacent provider card in the same series.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugin code; relevance: `@openclaw/deepseek-provider` source.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions monorepo; relevance: container for deepseek-provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core repo; relevance: loads the deepseek plugin.

**Snippets** (10)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: DeepSeek uses an OpenAI-compatible API surface.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator/router provider; relevance: DeepSeek frequently routed via aggregators as a cheap model.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — catalog assembly; relevance: DeepSeek models register here.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog/manifest planner; relevance: planning DeepSeek models into the catalog.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias/pricing lookup; relevance: DeepSeek model alias/pricing resolution.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: deepseek declares its provider surface via entries.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: defines `@openclaw/deepseek-provider` package shape.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: how `deepseek` registers as a provider.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: DeepSeek as a fallback provider in the chat loop.
- [snippet_hermes_agent_core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — provider error mapping; relevance: error handling for the DeepSeek provider.

non-existing references and are explicitly labeled (planned).

## Undigested Terms Plan

pl08 creates **0 new `term_dictionary` notes** (per master design: OpenClaw vocabulary lives in `oc_*` doc
notes; only existing terms are linked).

| Term | Disposition |
|---|---|
| plugin / provider plugin | Link existing `term_provider_plugin` (do NOT redefine). |
| Cohere | Provider name — documented as config in note 1; no term note. `term_cohere` MISSING → link `term_third_party_genai_services` + `term_embedding`. |
| ComfyUI | Tool/provider name — documented in note 2; link `term_diffusion_model` / `term_stable_diffusion`. |
| GitHub Copilot | Runtime/provider name — documented in notes 3/4; `term_github_copilot` MISSING → link `term_autonomous_coding_agents` + `term_agent_harness`. Do NOT link `project_tt_copilot*` (different product). |
| Deepgram | Provider name — documented in note 5; link `term_speech_to_text`. `term_media_understanding`/`term_voice` MISSING → link `term_multimodal`. |
| DeepInfra | Provider name — documented in note 6; link existing capability terms. |
| DeepSeek | Provider name — `term_deepseek` EXISTS → link it (note 7). |
| ClawHub | Distribution registry — link `entry_openclaw_docs` (planned hub); `term_clawhub` MISSING. Owned by ClawHub sub-plans (cw01–cw03), NOT promoted here. |
| capability contracts (imageGenerationProviders, mediaUnderstandingProviders, memoryEmbeddingProviders, speechProviders, realtimeTranscriptionProviders, musicGenerationProviders, videoGenerationProviders) | OpenClaw SDK vocabulary — described inline in the relevant note's Surface section; link `term_text_to_speech`/`term_speech_to_text`/`term_embedding`/`term_multimodal`. No new term notes (these are the subjects of the SDK sub-plans pl23–pl25). |

**New-term candidates: none.** All cross-cutting concepts already have a `term_dictionary` home or are
SDK-contract vocabulary owned by another sub-plan. No genuinely reusable, vault-novel, home-less term
surfaced in these 7 stub cards.

## Term-Note Authoring Requirements

**N/A (0 new terms).** Inherited from master: pl08 authors zero `term_dictionary` notes; it only links
existing terms. (If augment's Step-2d re-scan surfaces a genuinely reusable home-less term, it would be
captured via `/tessellum-capture-term-note` + added to the best-fit `acronym_glossary_*.md` — expected 0.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order + body sections (`## Overview`, `## Related Notes`, `## References`, footer) valid; 0 ERROR/LINK-003. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/plugins/reference/<page>.md`) | Package id, install route, and surface line reproduced faithfully; no invented capabilities. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2500 words / ≤6 code blocks (trivially met, ~234w); every source H2 mapped. |
| G4 | Cross-Reference | ≥8 relevance-selected term links + ≥10 snippet links + ≥10 doc links (≥5 existing) + repo/sibling links present, each with a relevance statement (per the LOCKED Per-Note Related Notes Mapping). |
| G5 | Ghost-reference detect + redirect | 0 ghost links (MISSING terms above were excluded at plan; augment re-verifies). |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken relative paths after reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks); in-degree ≥1, anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_cohere oc_plugins_reference_comfy oc_plugins_reference_copilot oc_plugins_reference_copilot_proxy oc_plugins_reference_deepgram oc_plugins_reference_deepinfra oc_plugins_reference_deepseek"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present in frontmatter
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_ link (G4/G7 wiring)
  grep -q "${SIBLING_PREFIX}" "$f" || echo "NO SIBLING ${SIBLING_PREFIX} LINK in $n"
  # G3: density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w ${cb}cb ${lines}L)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost / G6 broken: run after incremental reindex
bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_cohere | model | 230 | 0 | ✅ |
| 2 | oc_plugins_reference_comfy | model | 240 | 0 | ✅ |
| 3 | oc_plugins_reference_copilot | model | 230 | 0 | ✅ |
| 4 | oc_plugins_reference_copilot_proxy | model | 220 | 0 | ✅ |
| 5 | oc_plugins_reference_deepgram | model | 240 | 0 | ✅ |
| 6 | oc_plugins_reference_deepinfra | model | 245 | 0 | ✅ |
| 7 | oc_plugins_reference_deepseek | model | 230 | 0 | ✅ |

No note approaches any cap. Risk here is **over-expansion**, not over-compression: each source is ~50–60
words, so the digest note must stay a compact reference card (Overview + Distribution + Surface +
Related/References + the relevance-selected `## Related Notes`) and must NOT pad with invented detail or
content lifted from the linked `/providers/<x>` config pages (that would violate G2 grounding and duplicate
other sub-plans).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the W1 master pre-step before the first
sub-plan executes) under the **Plugins → Reference** cluster (alongside pl01–pl25). Each of the 7 notes
gets its entry-point back-link at finalization — this is the primary G7/G8 inbound-link source. No new
entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):
- `entry_openclaw_docs.md` (planned hub) → all 7 notes (primary anti-island source).
- `repo_openclaw_extensions_llm_providers` → notes 1, 2, 4, 6, 7 (provider plugins).
- `repo_openclaw_extensions_voice_speech` → notes 5, 6 (speech/media contracts).
- `repo_openclaw_agents` → note 3 (Copilot agent runtime).
- `term_deepseek` → note 7; `term_speech_to_text` → notes 5, 6; `term_embedding` → notes 1, 6;
  `term_provider_plugin` → notes 1, 2, 4, 6, 7; `term_diffusion_model` → note 2.
- `snippet_openclaw_speech_deepgram_stt` → note 5 (exact code counterpart back-reference).

## Pacing Rules (inherited from master)

Single phase, 7 notes, well under the ~30-agent fan-out cap. 8 gates before commit. Re-read each source
page; reproduce package id + surface line verbatim; one BB (model) per note; do NOT pad from linked
provider config pages. `git pull --rebase --autostash` first; commit + push after the phase; no Claude
co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before
commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (Per-Note Related Notes Mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** locked the Per-Note Related Notes Mapping at the RAISED FLOORS
(**≥8 terms · ≥10 snippets · ≥10 docs per note**, up from the original draft's ≥6-terms + sparse
snippet/doc lists), relevance-selected from a fresh re-read of all 7 source pages
(`inbox/openclaw_docs/plugins/reference/{cohere,comfy,copilot,copilot-proxy,deepgram,deepinfra,deepseek}.md`)

47 docs under `resources/documentation/` (hermes_agent / pi / claude_code / band / aws_bedrock corpora),
(`term_cohere`, `term_github_copilot`, `term_image_generation`, `term_video_generation`,
`term_music_generation`, `term_media_understanding`, `term_voice`, `term_ollama`, `term_anthropic`,
`term_amazon_bedrock`, `term_clawhub`) were re-confirmed absent and excluded. `entry_openclaw_docs`
re-confirmed not-yet-created (planned W1) and cited as (planned).

**Per-note locked counts (terms / snippets / docs incl. planned siblings / repos · floorsMet):**

| Note | Terms | Snippets | Docs | Repos | Floors met (≥8t/≥10s/≥10d) |
|---|---:|---:|---:|---:|---|
| oc_plugins_reference_cohere | 8 | 11 | 11 (9 existing + 2 planned) | 3 | ✅ |
| oc_plugins_reference_comfy | 8 | 11 | 11 (10 existing + 1 planned) | 3 | ✅ |
| oc_plugins_reference_copilot | 8 | 10 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_copilot_proxy | 8 | 11 | 11 (9 existing + 2 planned) | 3 | ✅ |
| oc_plugins_reference_deepgram | 10 | 11 | 11 (10 existing + 1 planned) | 4 | ✅ |
| oc_plugins_reference_deepinfra | 10 | 11 | 11 (9 existing + 2 planned) | 4 | ✅ |
| oc_plugins_reference_deepseek | 9 | 10 | 11 (9 existing + 2 planned) | 3 | ✅ |

sibling `oc_*` + `entry_openclaw_docs` references are additive, not floor-padding. All snippets are EXISTING

**New-term candidates:** NONE. The re-read (augment Step 2d) surfaced no genuinely reusable, vault-novel,
home-less term in these 7 machine-generated stub cards. Every cross-cutting concept already has a
`term_dictionary` home (linked) or is OpenClaw SDK-contract vocabulary owned by another sub-plan
(`imageGenerationProviders`, `mediaUnderstandingProviders`, `memoryEmbeddingProviders`, `speechProviders`,
`realtimeTranscriptionProviders`, `musicGenerationProviders`, `videoGenerationProviders` → pl23–pl25 SDK
sub-plans; described inline in Surface, not promoted to terms). Best-fit glossary if any such term were ever
captured: `acronym_glossary_gen_ai_dev.md` (agentic/LLM glossary) — but expected 0 per master design.
pl08 creates **0 new `term_dictionary` notes**.

**Provider-name terms intentionally NOT created** (documented inline as config, per master Undigested Terms
design): cohere, ComfyUI, GitHub Copilot, Deepgram, DeepInfra (DeepSeek is the one exception — `term_deepseek`
already EXISTS and is linked from note 7).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of the augmented plan. Source pages re-read for CP7 (all 7, measured).

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present (G1–G8 per batch) | **PASS** | Per-Phase Validation Gate table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (now ≥8t/≥10s/≥10d), G5 Ghost-detect+redirect, G6 Broken-link fix, G7/G8 Discoverability/in-degree ≥1. Single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | Entry Point Decision section: 7 rows into `entry_openclaw_docs.md` (W1 master pre-step) under Plugins → Reference; no new entry point created by pl08. Hub confirmed not-yet-created (planned). |
| CP4 | Size manageable | **PASS** | 7 notes, single phase, well under the ≤30 cap and the ~30-agent fan-out cap. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/`(`cc_*`) + `pi/`(`pi_*`) doc corpora: `## Overview` opener, `## Related Notes` reference section, `**Source**/**Last Updated**/**Status**` footer, fixed YAML field order, forbidden-field list. Matches existing target-type notes. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: all 7 notes ~220–245 words, 0 code fences, far below ≤2500w/≤6cb/≤400L caps. Risk is over-expansion, not over-compression; no splits needed (single-BB, ~50–60w sources). |
| CP7 | Sources measured (not guessed) | **PASS** | All 7 source pages re-read 2026-06-21: cohere 51w, comfy 58w, copilot 51w, copilot-proxy 53w, deepgram 61w, deepinfra 60w, deepseek 54w = 388w total — matches the plan's Source table exactly (ratio 1.00; well within 0.7–1.3×). Surface lines verified verbatim (e.g. deepinfra 5 contracts; comfy image/music/video; deepgram media-understanding+realtime-transcription). |
| CP8 | Undigested Terms + authoring reqs | **PASS** | Undigested Terms Plan present (0 new terms; each provider name + each SDK capability contract has a documented disposition: link existing term or describe inline). Term-Note Authoring Requirements N/A (0 new terms) per master; multi-source mandate inherited. New-term scan (Step 2d) → 0 candidates. |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to audit (pl08 creates none). Collision audit generalized to all 7 planned `oc_*` doc notes: each maps 1:1 to a distinct ClawHub plugin page; none duplicates an existing term/doc/repo (the related provider-config `/providers/<x>` pages are owned by pr02/pr03/pl03 and link-only). DeepSeek correctly routes to existing `term_deepseek` rather than re-creating. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | Inlinks section maps outside-folder inbound links to all 7 notes: `entry_openclaw_docs` (all 7), `repo_openclaw_extensions_llm_providers` (1,2,4,6,7), `repo_openclaw_extensions_voice_speech` (5,6), `repo_openclaw_agents` (3), term back-links, and `snippet_openclaw_speech_deepgram_stt` → note 5. G8-Discoverability/in-degree ≥1 is in the gate table as an EXECUTED check. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
