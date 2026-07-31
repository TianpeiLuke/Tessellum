---
title: Hermes Agent Docs Digestion — Sub-Plan 19b — Developer: Provider & Engine Plugin Authoring
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/
pages:
  - developer-guide/model-provider-plugin.md
  - developer-guide/web-search-provider-plugin.md
  - developer-guide/image-gen-provider-plugin.md
  - developer-guide/memory-provider-plugin.md
  - developer-guide/video-gen-provider-plugin.md
  - developer-guide/context-engine-plugin.md
---

# Sub-Plan 19b: Developer — Provider & Engine Plugin Authoring

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP19b's note
> filenames/BBs/coverage are defined. Part **b** of the SP19 split (SP19a = adding tools/providers/
> adapters + creating-skills + extend-cli + programmatic + contributing).

## Scope

The provider/engine plugin-authoring surface of the Hermes developer guide: how a third party drops a
directory under `$HERMES_HOME/plugins/<kind>/` to add a new inference backend, web-search backend,
image-gen backend, memory backend, video-gen backend, or context-compression engine — with zero repo
edits. Source = 6 mirrored pages in `inbox/hermes_agent_docs/developer-guide/`, all substantive, each a
self-contained authoring guide that follows the same "declare a profile/subclass an ABC, register(),
drop a `plugin.yaml`, distribute via pip" pattern. **P3 / developer** — these are the plugin extension
points; they link DOWN to the existing `repo_hermes_agent_plugins`/`repo_hermes_agent_providers_adapters`
code layer and the `plugins_provider_*` / `plugins_*_dispatch` snippet corpus that implements each ABC.

## Content Strategy

- **One BB per note — all six are `procedure`** (step-by-step "build a plugin of kind X" guides). Each
  page is ≤1600 words / ≤11 code blocks → **1 note per page, no splits** (densest is model-provider at
  1600w/9code; smallest context-engine at 847w/9code).
- **Do NOT duplicate** the concept notes these procedures extend → **link-outs**, not copied content:
  the *concept* of a provider plugin is `term_provider_plugin` (SP09/14 territory); the *concept* of a
  context engine is `term_context_engine` (SP18 territory); the *concept* of cross-session memory is
  `term_agentic_memory` / forward-ref `term_honcho` (SP05). The user-facing FEATURE pages each backend
  services (web-search SP08, image-generation SP08, memory SP05, providers SP14) are link-outs.
- **The general plugin-authoring guide** (`guides/build-a-hermes-plugin.md`, tools/hooks/CLI plugins) is
  owned by **SP17**, and `developer-guide/plugin-llm-access.md` by **SP18** — link, do not re-cover.
- **Adding-providers / adding-tools / adding-platform-adapters / creating-skills** are owned by **SP19a**
  → forward-ref link-outs (intra-series, resolve at finalization).

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — wc)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| developer-guide/model-provider-plugin.md | 1600 | 9 | procedure | 1 |
| developer-guide/web-search-provider-plugin.md | 1366 | 9 | procedure | 1 |
| developer-guide/image-gen-provider-plugin.md | 1302 | 7 | procedure | 1 |
| developer-guide/memory-provider-plugin.md | 1137 | 11 | procedure | 1 |
| developer-guide/video-gen-provider-plugin.md | 1000 | 4 | procedure | 1 |
| developer-guide/context-engine-plugin.md | 847 | 9 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **6 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_model_provider_plugin.md` | procedure | model-provider-plugin §How discovery works, §Directory structure, §Minimal example, §ProviderProfile fields, §Overridable hooks (+hook reference examples), §User overrides, §api_mode selection, §Auth types, §Discovery timing, §Testing, §General PluginManager integration, §Distribute via pip | ~1500 | Authoring an inference-backend plugin: drop `plugins/model-providers/<name>/` with an `__init__.py` that `register_provider(ProviderProfile(...))`, the 3-tier discovery + last-writer-wins override, the `ProviderProfile` field reference, the four `api_mode` values + URL auto-detection, six auth types, overridable hooks (`prepare_messages`/`build_extra_body`/`build_api_kwargs_extras`/`fetch_models`), and pip distribution. |
| 2 | `hermes_web_search_provider_plugin.md` | procedure | web-search-provider-plugin §How discovery works, §Directory structure, §The WebSearchProvider ABC, §plugin.yaml, §ABC reference, §Response shape, §Capability flags, §How Hermes wires it into the tools, §Lazy-installing optional dependencies, §Reference implementations, §Distribute via pip | ~1300 | Authoring a web-search/extract/crawl backend: subclass `WebSearchProvider`, implement `name`/`is_available()`/`search()`/`extract()`, the `kind: backend` + `provides_web_providers` manifest, capability-flag routing (`supports_search`/`supports_extract`), the fixed success/error response envelope, sync-or-async dispatch, lazy SDK install, and pip distribution. |
| 3 | `hermes_image_gen_provider_plugin.md` | procedure | image-gen-provider-plugin §How discovery works, §Directory structure, §The ImageGenProvider ABC, §plugin.yaml, §ABC reference, §Response format, §Handling base64 vs URL output, §User overrides, §Testing, §Reference implementations, §Distribute via pip | ~1250 | Authoring an image-generation backend: subclass `ImageGenProvider`, implement `name`/`generate()` (+`list_models`/`default_model`/`get_setup_schema`), the `success_response`/`error_response` helpers, base64-vs-URL output via `save_b64_image()`, `hermes plugins enable` opt-in for user plugins, and pip distribution. |
| 4 | `hermes_memory_provider_plugin.md` | procedure | memory-provider-plugin §Directory Structure, §The MemoryProvider ABC, §Required Methods (core lifecycle/config/optional hooks), §Config Schema, §Save Config, §Plugin Entry Point, §plugin.yaml, §Threading Contract, §Profile Isolation, §Testing, §Adding CLI Commands, §Single Provider Rule | ~1150 | Authoring a cross-session memory backend: implement the `MemoryProvider` ABC (`initialize`/`get_tool_schemas`/`handle_tool_call` + lifecycle hooks `prefetch`/`sync_turn`/`on_pre_compress`/`on_session_end`), the config-schema-driven `hermes memory setup`, the non-blocking `sync_turn` threading contract, `hermes_home` profile isolation, convention-based `cli.py` subcommands, and the single-active-provider rule. |
| 5 | `hermes_video_gen_provider_plugin.md` | procedure | video-gen-provider-plugin §The unified surface, §How discovery works, §Directory structure, §The VideoGenProvider ABC, §The plugin manifest, §The video_generate schema, §Model families and endpoint routing (FAL pattern), §Selection precedence, §Response shape, §Where to save artifacts, §Testing | ~1000 | Authoring a video-generation backend: subclass `VideoGenProvider` (mirrors image-gen) plus a `capabilities()` declaration and the `image_url`-presence routing convention (text-to-video vs image-to-video through one tool), the FAL model-family/endpoint pattern, the 5-level model-selection precedence, `save_b64_video`/`save_bytes_video` artifact handling, and smoke tests. |
| 6 | `hermes_context_engine_plugin.md` | procedure | context-engine-plugin §How it works, §Directory structure, §The ContextEngine ABC (+required methods, class attributes, optional methods), §Engine tools, §Registration, §Lifecycle, §Configuration, §Testing | ~850 | Authoring a context engine that replaces the built-in `ContextCompressor`: implement the `ContextEngine` ABC (`name`/`update_from_response`/`should_compress`/`compress`) + the token-counter class attributes, optional session-lifecycle hooks, engine-exposed tools via `get_tool_schemas`/`handle_tool_call`, directory-vs-`register_context_engine` registration, the explicit config-driven single-engine selection, and the ABC contract test. |

**SP19b totals:** 6 notes · procedure 6 · concept 0 (the provider-plugin/context-engine concepts are existing
term notes). 6 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 6 · procedure 6 · concept 0 · model 0 (the plugin-system *concepts* are existing `term_*` notes).
- Source: 6 digested pages (~7.3K words) → ~6.0K words of notes (modest compression via link-outs to the
  feature pages each backend services + the concept terms).
- BB mix: procedure 100% (all six are "how to author a plugin of kind X" guides).

## Section Coverage Map

```
model-provider-plugin.md (1600w)
├── intro + :::tip (three provider-plugin kinds) ─────────── → Note 1 (links to Notes 4/6)
├── How discovery works / Directory structure ───────────── → Note 1
├── Minimal example / ProviderProfile fields ────────────── → Note 1
├── Overridable hooks / Hook reference examples ─────────── → Note 1
├── User overrides / api_mode selection / Auth types ────── → Note 1 (oauth→SP15 guides)
├── Discovery timing / Testing / General PluginManager ──── → Note 1
├── Distribute via pip ──────────────────────────────────── → Note 1 (general plugin→SP17)
└── Related pages ───────────────────────────────────────── → Note 1 Related Notes (provider-runtime→SP18; adding-providers→SP19a)
web-search-provider-plugin.md (1366w)
├── intro + :::tip (backend plugin kinds) ───────────────── → Note 2 (links Notes 1/3/4/5/6)
├── How discovery works / Directory structure ───────────── → Note 2
├── The WebSearchProvider ABC / plugin.yaml / ABC reference → Note 2
├── Response shape / Capability flags ───────────────────── → Note 2
├── How Hermes wires it into the tools ──────────────────── → Note 2 (web_tools→SP08)
├── Lazy-installing optional dependencies ───────────────── → Note 2 (security model→SP17 build-plugin)
├── Reference implementations / Distribute via pip ──────── → Note 2
└── Related pages ───────────────────────────────────────── → Note 2 Related Notes (web-search feature→SP08; plugins overview→SP06b)
image-gen-provider-plugin.md (1302w) ── all sections ─────── → Note 3 (image-generation feature→SP08; build-plugin→SP17)
memory-provider-plugin.md (1137w) ── all sections ────────── → Note 4 (memory feature/honcho→SP05; context-engine cross-ref→Note 6)
video-gen-provider-plugin.md (1000w) ── all sections ─────── → Note 5 (image-gen mirror→Note 3; vision/media→SP08)
context-engine-plugin.md (847w) ── all sections ──────────── → Note 6 (compression internals→SP18; memory analogue→Note 4)
```

No source H2/H3 orphaned. All 6 pages fully covered; feature-page + concept-term detail intentionally
routed to owning SPs / existing term notes as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| (none) | — | All 6 pages are ≤1600w / ≤11 code and each is a single cohesive `procedure` BB → 1 note/page, no splits. Code-heavy pages (memory 11 blocks, model/web/context 9 blocks) curate to ≤6 load-bearing examples, summarizing the rest in prose. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_model_provider_plugin`, `hermes_web_search_provider_plugin`, `hermes_image_gen_provider_plugin`, `hermes_video_gen_provider_plugin` | `term_provider_plugin.md` (79L, `building_block: concept`, active) | **NOT a dup** — `term_provider_plugin` is the *concept* of a provider plugin; these four notes are distinct *procedure* authoring guides per backend kind (model/web/image/video) | CREATE all 4; LINK `term_provider_plugin` from each. |
| `hermes_context_engine_plugin` | `term_context_engine.md` (81L, `building_block: concept`, active) | **NOT a dup** — `term_context_engine` is the *concept* (pluggable context-management strategy); this note is the *procedure* for authoring one (subclass the ABC) | CREATE; LINK `term_context_engine`. |
| `hermes_memory_provider_plugin` | `term_agentic_memory.md` (active), `term_honcho` (forward-ref, not yet created) | **NOT a dup** — `term_agentic_memory` is the cross-session-memory concept; this note is the procedure for authoring a memory backend | CREATE; LINK `term_agentic_memory`; `term_honcho` is a +fin forward-ref (SP05-owned). |
| all 6 | no `resources/documentation/hermes_agent/` doc note exists yet (DB query 2026-06-15 returned 0); no `term_*` note covers a per-kind authoring *procedure* | NEW | CREATE all 6. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0
substantive same-concept duplicates** — the two LIKE hits (`term_provider_plugin`, `term_context_engine`)
are `building_block: concept` term notes, a different BB from these `procedure` authoring guides (the
canonical concept-vs-procedure non-dup case). New `hermes_agent/` folder → no doc-doc collisions (SP19a +
other SPs not yet executed; intra-series links resolve at finalization).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19 (user directive — supersedes the 2026-06-14 master floor AND the
> interim 3-floor wording):** each note's `## Related Notes` carries **ALL FOUR counted groups**, every
> entry relevancy-selected to the note's actual content and rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   SOURCE-CODE layer whose modules implement what the note documents; primarily the 13
>   `repo_hermes_agent_*` notes),
>   implementation corpus whose CODE this note documents; **this is now a COUNTED floor, promoted from the
>   prior bonus group and raised from 8 → ≥10**, NO LONGER a bonus),
> - **≥10 documentation notes** (`../../documentation/`, sibling `hermes_*` in this series + analogous
>   `claude_code/cc_*` agent-tool docs + other relevant existing docs).
>
> (re-queried 2026-06-19; the 13 `repo_hermes_agent_*` notes + every cited `snippet_hermes_agent_*` + every
> cited `cc_*` analogue all confirmed active). Intra-series sibling `hermes_*` doc links (incl.
> SP19a/SP18/SP05/SP06b/SP08 forward-refs) resolve at finalization (G5/G8) and are allowed un-verified now
> (they do not exist yet — DB query 2026-06-19 returned 0 `resources/documentation/hermes_agent/` notes).
> New Hermes-specific terms owned by other SPs (`term_hermes_plugin`→SP06b, `term_honcho`→SP05,
> `term_context_compression`→SP18, `term_fallback_provider`/`term_provider_routing`→SP09) are ADDITIONAL
> forward-refs (+fin), NOT counted to the ≥8 term floor (they don't exist yet).

**Note 1 `hermes_model_provider_plugin`**
- Terms (9): term_provider_plugin, term_model_catalog, term_llm, term_oauth_token, term_authentication, term_function_calling, term_multimodal, term_agent_harness, term_autonomous_coding_agents — relevance: a model-provider plugin declares an inference backend (provider-plugin concept) with a model catalog (`fetch_models`/`fallback_models`), api-key/OAuth auth_types, and an OpenAI-compatible (function-calling) surface the agent harness routes `AIAgent` calls through; multimodal/aux-model fields cover vision/compression. (+fin: term_hermes_plugin, term_fallback_provider, term_provider_routing)
- Code-Repos (5): repo_hermes_agent_providers_adapters — the `providers/` package: `ProviderProfile`, `register_provider`, `_discover_providers`, and the api_mode transport adapters this guide subclasses; repo_hermes_agent_plugins — the general `PluginManager` that records the `kind: model-provider` manifest + entry-point (pip) discovery; repo_hermes_agent_agent_core — `agent/model_metadata.py` URL reverse-mapping, `agent/auxiliary_client.py`, and the chat-completions transport that consumes the profile hooks; repo_hermes_agent_cli — `hermes_cli/auth.py`/`runtime_provider.py`/`models.py`/`doctor.py`/`config.py` the auto-wire table lists; repo_hermes_agent — top-level `$HERMES_HOME/plugins/model-providers/` discovery layout and the bundled-vs-user override rule.
- Snippets (12): providers_base_abc, providers_init_dispatch, plugins_provider_registry, plugins_provider_openrouter, plugins_provider_bedrock, plugins_provider_custom, plugins_provider_nous, cli_providers_registry, cli_models_fetch, core_agent_init_api_mode_resolution, cli_doctor_api_connectivity, core_auxiliary_auth_resolution — relevance: the `ProviderProfile` base + last-writer-wins registry, lazy `_discover_providers` dispatch, reference provider plugins (openrouter aggregator / bedrock no-REST / custom Ollama quirks / nous attribution), the `--provider` registry, live `fetch_models` catalog fetch, the `api_mode` URL-auto-detect precedence, the `hermes doctor` `/models` probe, and the auxiliary-model auth resolution this guide drives.
- Docs (12): hermes_web_search_provider_plugin, hermes_image_gen_provider_plugin, hermes_memory_provider_plugin, hermes_video_gen_provider_plugin, hermes_context_engine_plugin (sibling per-kind authoring guides, this series); cc_model_selection (analogous model-config doc), cc_fallback_models (mirror of `fallback_models`), cc_configure_advisor_model (auxiliary/advisor model = `default_aux_model`), cc_amazon_bedrock_setup (analogue of the `bedrock` provider plugin + `aws_sdk` auth), cc_authentication (analogous credential/OAuth surface), cc_llm_gateway (proxy/base-url override analogue), cc_proxy_and_gateway_config (user `*_BASE_URL` override analogue).

**Note 2 `hermes_web_search_provider_plugin`**
- Terms (9): term_provider_plugin, term_function_calling, term_rest, term_idempotency, term_caching, term_rate_limiting, term_json_schema, term_agent_harness, term_autonomous_coding_agents — relevance: a web-search backend services the `web_search`/`web_extract` tool calls (function-calling, JSON-schema tool result) via a REST/HTTP `httpx` surface with a fixed success/error response envelope; the agent harness routes calls by `supports_*` capability flags, honoring rate-limit/caching/idempotency on the backend side. (+fin: term_hermes_plugin)
- Code-Repos (5): repo_hermes_agent_plugins — the `plugins/web/<name>/` backend-loading path, `kind: backend`/`provides_web_providers` manifest routing, and `register(ctx)`/`ctx.register_web_search_provider`; repo_hermes_agent_tools — `tools/web_tools.py` (the `web_search`/`web_extract` wrappers), `tools/lazy_deps.py`, and `tools/xai_http.py` the reference plugins reuse; repo_hermes_agent_agent_core — `agent/web_search_provider.py` (the ABC) and `agent/web_search_registry.py` (the active-provider registry); repo_hermes_agent_cli — `hermes tools` selection UX + `hermes plugins install` credential prompt; repo_hermes_agent — `$HERMES_HOME/plugins/web/` discovery + `plugins.enabled` opt-in layout.
- Snippets (11): tools_web_tools, plugins_web, plugins_interfaces_abcs, plugins_manifest_schema, plugins_provider_registry, tools_lazy_deps, cli_plugins_discover, cli_plugins_install, cli_plugins_cmd_install, cli_plugins_cmd_list_info, plugins_namespace_init — relevance: the `web_search`/`web_extract` tool wrapper (`tools/web_tools.py`), the web-backend dispatch + ABC + registry, the `kind: backend`/`provides_web_providers` manifest schema, the `lazy_deps.ensure` security-gated SDK install (DDGS pattern), and the plugin discover/install/list/credential-prompt code this guide describes.
- Docs (12): hermes_model_provider_plugin, hermes_image_gen_provider_plugin, hermes_video_gen_provider_plugin, hermes_memory_provider_plugin, hermes_context_engine_plugin (sibling per-kind authoring guides, this series); cc_plugins_overview (analogous plugin-system overview = "Plugins overview" link-out), cc_plugin_components (analogous plugin-component model), cc_plugin_manifest_schema (mirror of `plugin.yaml`/`kind`), cc_plugin_marketplaces_and_install (analogue of the pip/`hermes plugins install` distribution), cc_plugin_cli_commands (analogue of `hermes plugins`/`hermes tools` CLI), cc_built_in_tools (analogous built-in-tool catalog the backend services), cc_web_overview (analogous agent web-access doc).

**Note 3 `hermes_image_gen_provider_plugin`**
- Terms (9): term_provider_plugin, term_multimodal, term_diffusion_model, term_gan, term_computer_vision, term_function_calling, term_base64, term_agent_harness, term_autonomous_coding_agents — relevance: an image-gen backend services the `image_generate` tool (function-calling) producing multimodal/diffusion/GAN outputs; the ABC `generate()` + `success_response`/`error_response` helpers are the contract, with `save_b64_image()` handling base64-vs-URL output the gateway renders, and `capabilities()` declaring text/image (computer-vision) modalities. (+fin: term_hermes_plugin)
- Code-Repos (5): repo_hermes_agent_plugins — the `plugins/image_gen/<name>/` directory + `kind: backend` manifest + `register(ctx)`/`ctx.register_image_gen_provider`, and the reference `openai`/`xai`/`openai-codex` plugins; repo_hermes_agent_tools — the `image_generate` tool wrapper that asks the registry for the active provider and dispatches; repo_hermes_agent_agent_core — `agent/image_gen_provider.py` (the `ImageGenProvider` ABC + `save_b64_image`/`resolve_aspect_ratio` helpers) and `agent/image_gen_registry.py`; repo_hermes_agent_cli — `hermes tools` model picker + `hermes plugins enable`/`install`; repo_hermes_agent_gateway_messaging — gateway delivery of URL/absolute-path images (Telegram photo bubble, Discord attachment).
- Snippets (11): tools_image_gen, plugins_image_gen_dispatch, tools_vision_dispatch, tools_vision_input, plugins_interfaces_abcs, plugins_manifest_schema, plugins_provider_registry, cli_plugins_install, cli_plugins_cmd_install, cli_plugins_cmd_list_info, plugins_namespace_init — relevance: the `image_generate` tool wrapper, the image-gen registry/dispatch, the vision dispatch/input path multimodal outputs flow into, the plugin ABC + manifest schema + registry, and the `hermes plugins enable`/install/list path this guide drives.
- Docs (12): hermes_video_gen_provider_plugin (its line-for-line mirror), hermes_model_provider_plugin, hermes_web_search_provider_plugin, hermes_memory_provider_plugin, hermes_context_engine_plugin (sibling per-kind authoring guides, this series); cc_plugins_overview (analogous plugin-system overview), cc_plugin_components (analogous component model), cc_plugin_manifest_schema (mirror of `plugin.yaml`/`kind`), cc_plugin_marketplaces_and_install (analogue of pip distribution), cc_plugin_cli_commands (analogue of `hermes plugins enable`/`hermes tools`), cc_built_in_tools (analogous built-in-tool catalog), cc_tools_catalog (analogous tool reference).

**Note 4 `hermes_memory_provider_plugin`**
- Terms (9): term_agentic_memory, term_episodic_memory, term_provider_plugin, term_vector_database, term_function_calling, term_pii, term_dense_retrieval, term_agent_harness, term_autonomous_coding_agents — relevance: a memory provider gives cross-session (agentic/episodic) memory via tool calls (function-calling), often a vector/dense-retrieval backend; the lifecycle hooks (`prefetch`/`sync_turn`/`on_pre_compress`/`on_session_end`) persist conversation, and the threading + PII off-device-data contract govern what workspace content (file paths, command output) leaves the device. (+fin: term_honcho, term_hermes_plugin, term_context_compression)
- Code-Repos (5): repo_hermes_agent_plugins — the `plugins/memory/<name>/` directory + `register(ctx)`/`ctx.register_memory_provider` + the `honcho`/`supermemory` reference plugins (incl. convention-based `cli.py`); repo_hermes_agent_agent_core — `agent/memory_provider.py` (the `MemoryProvider` ABC + config schema) and `agent/memory_manager.py` (the `MemoryManager`, single-provider rule, `sync_all`/`shutdown_all`); repo_hermes_agent_tools — the memory tool schemas the provider returns via `get_tool_schemas`/`handle_tool_call`; repo_hermes_agent_cli — `hermes memory setup` config wizard + convention-based `discover_plugin_cli_commands()` subcommand tree; repo_hermes_agent_gateway_messaging — gateway-side memory monitor + cross-session/profile boundaries the threading contract serves.
- Snippets (11): tools_memory, plugins_memory_discovery, cli_memory_setup, honcho_session_lifecycle, honcho_session_query, honcho_session_messages, gw_memory_monitor, core_agent_init_memory_ollama, plugins_interfaces_abcs, plugins_manifest_schema, cli_plugins_cmd_list_info — relevance: the memory tool wrapper, memory-plugin discovery, `hermes memory setup`, the Honcho reference implementation (lifecycle/query/messages — the page's cited 13-subcommand example), memory init the ABC plugs into, plus the plugin ABC/manifest surfaces (`hooks:` list) and `hermes plugins` introspection.
- Docs (12): hermes_context_engine_plugin (the analogous single-select plugin the page cross-refs), hermes_model_provider_plugin, hermes_web_search_provider_plugin, hermes_image_gen_provider_plugin, hermes_video_gen_provider_plugin (sibling authoring guides, this series); cc_auto_memory (analogous agentic-memory feature), cc_memory_overview (analogous memory subsystem doc), cc_troubleshoot_memory (analogous memory operational doc), cc_plugin_components (analogous plugin-component model), cc_plugin_manifest_schema (mirror of `plugin.yaml`/`hooks`), cc_plugin_user_config_and_env (analogue of the secret/`.env` config-schema split), cc_what_survives_compaction (analogue of `on_pre_compress` save-before-discard).

**Note 5 `hermes_video_gen_provider_plugin`**
- Terms (9): term_provider_plugin, term_multimodal, term_diffusion_model, term_gan, term_computer_vision, term_function_calling, term_base64, term_agent_harness, term_autonomous_coding_agents — relevance: a video-gen backend services the `video_generate` tool (function-calling) producing multimodal/diffusion/GAN video; the ABC mirrors image-gen plus a `capabilities()` declaration (modalities/aspect-ratios/durations) and the `image_url`-presence routing convention (text-to-video vs image-to-video through one tool), with `save_b64_video`/`save_bytes_video` base64/bytes artifact handling. (+fin: term_hermes_plugin)
- Code-Repos (5): repo_hermes_agent_plugins — the `plugins/video_gen/<name>/` directory + `kind: backend` manifest + `register(ctx)`/`ctx.register_video_gen_provider` + the `xai`/`fal` reference plugins (the FAL family/endpoint pattern); repo_hermes_agent_tools — the `video_generate` tool wrapper + the dynamically-rebuilt tool schema driven by `capabilities()`; repo_hermes_agent_agent_core — `agent/video_gen_provider.py` (the `VideoGenProvider` ABC + `save_b64_video`/`save_bytes_video`/`success_response`/`error_response` helpers) and the video-gen registry; repo_hermes_agent_cli — `hermes tools` → Video Generation selection + the 5-level model-selection precedence; repo_hermes_agent_gateway_messaging — gateway delivery of remote video URLs / cached artifacts.
- Snippets (11): tools_video_gen, plugins_video_gen_dispatch, tools_image_gen, plugins_image_gen_dispatch, tools_vision_dispatch, plugins_interfaces_abcs, plugins_manifest_schema, plugins_provider_registry, cli_plugins_install, cli_plugins_cmd_install, plugins_namespace_init — relevance: the `video_generate` tool wrapper + registry/dispatch, the analogous image-gen tool/dispatch (the page is "image-gen line-for-line"), the vision dispatch path, the plugin ABC + manifest schema + registry, and the install path.
- Docs (12): hermes_image_gen_provider_plugin (the line-for-line mirror it derives from), hermes_model_provider_plugin, hermes_web_search_provider_plugin, hermes_memory_provider_plugin, hermes_context_engine_plugin (sibling authoring guides, this series); cc_plugins_overview (analogous plugin-system overview), cc_plugin_components (analogous component model), cc_plugin_manifest_schema (mirror of `plugin.yaml`/`kind`), cc_plugin_marketplaces_and_install (analogue of pip distribution), cc_plugin_cli_commands (analogue of `hermes tools`/`hermes plugins`), cc_built_in_tools (analogous built-in-tool catalog), cc_tools_catalog (analogous tool reference).

**Note 6 `hermes_context_engine_plugin`**
- Terms (9): term_context_engine, term_context_window, term_progressive_summarization, term_knowledge_graph, term_dag, term_provider_plugin, term_function_calling, term_agent_harness, term_autonomous_coding_agents — relevance: a context engine replaces the built-in `ContextCompressor` (context-window management via summarization or a knowledge-DAG); it tracks token counters, decides `should_compress`, can expose agent-callable engine tools (function-calling) and is single-select like the other provider plugins. (+fin: term_context_compression)
- Code-Repos (5): repo_hermes_agent_agent_core — `agent/context_engine.py` (the `ContextEngine` ABC), the built-in `ContextCompressor`, the conversation-loop compression trigger, and `update_from_response`/`should_compress`/`compress` the engine overrides; repo_hermes_agent_plugins — the `plugins/context_engine/<name>/` directory discovery + `register(ctx)`/`ctx.register_context_engine` single-engine rule; repo_hermes_agent_tools — the engine-exposed tools injected via `get_tool_schemas`/`handle_tool_call` (e.g. `lcm_grep`); repo_hermes_agent_cli — `hermes plugins` → Context Engine selection + `config.yaml` `context.engine` editing; repo_hermes_agent — the `$HERMES_HOME/plugins/context_engine/` layout + explicit (never-auto-activated) config-driven selection.
- Snippets (11): core_context_engine_abc, plugins_context_engine_discovery, core_conversation_compression_entry, core_conversation_compression_strategy, core_manual_compression_feedback, core_conversation_loop_context_overflow, gw_session_context, plugins_interfaces_abcs, plugins_manifest_schema, plugins_provider_registry, cli_plugins_cmd_list_info — relevance: the `ContextEngine` ABC + directory discovery, the built-in compressor entry/strategy this engine replaces, manual `/compress <focus>` feedback (the `focus_topic` arg), the conversation-loop overflow trigger driving `should_compress`, session-context boundaries the lifecycle hooks serve, and the plugin ABC/manifest/registry + `hermes plugins` introspection surfaces.
- Docs (12): hermes_memory_provider_plugin (the analogous single-select plugin the page cross-refs), hermes_model_provider_plugin, hermes_web_search_provider_plugin, hermes_image_gen_provider_plugin, hermes_video_gen_provider_plugin (sibling authoring guides, this series); cc_what_survives_compaction (analogue of compaction strategy), cc_context_window_anatomy (analogous context-window model), cc_context_cost_by_feature (analogue of token-budget accounting), cc_agent_sdk_context_window (analogous SDK context-management surface), cc_extended_context_1m (analogous large-context handling), cc_plugin_components (analogous plugin-component model), cc_plugin_manifest_schema (mirror of the engine `plugin.yaml`).

All 6 notes meet the FOUR-FLOOR standard: **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**. Snippet IDs
`resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by G5/G8).
**Candidate IDs caught + replaced at finalization before lock-in** (none survive in the clean lists above):
`plugins_provider_gemini` (DOES NOT exist — replaced with `plugins_provider_custom`/`plugins_provider_bedrock`);
non-existent term slugs `term_rest_api`/`term_rest_api_design`/`term_api`/`term_inference`/`term_summarization`/`term_text_to_image`/`term_generative_ai`/`term_generative_ai_models`/`term_video_generation`/`term_image_generation`/`term_web_search`

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 6 source pages from `inbox/hermes_agent_docs/developer-guide/`; measured counts match the
Source Pages table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 model-provider-plugin | procedure | 1500 | ≤6 (curate from 9: minimal example + ProviderProfile + one hook + override + pip) | ✓ |
| 2 web-search-provider-plugin | procedure | 1300 | ≤6 (curate from 9: ABC subclass + manifest + response envelope + register) | ✓ |
| 3 image-gen-provider-plugin | procedure | 1250 | 6 (from 7: ABC + manifest + response + base64 + pip) | ✓ |
| 4 memory-provider-plugin | procedure | 1150 | ≤6 (curate from 11: ABC + config schema + sync_turn threading + cli.py + register) | ✓ |
| 5 video-gen-provider-plugin | procedure | 1000 | 4 | ✓ |
| 6 context-engine-plugin | procedure | 850 | ≤6 (curate from 9: ABC + engine tools + register + lifecycle) | ✓ |

No splits needed — all 6 notes are ≤1500w and a single cohesive `procedure` BB. Code-heavy pages
(memory 11, model/web/context 9) curate to ≤6 load-bearing blocks (kept verbatim), summarizing the rest in
prose. If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what
it IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in
YAML. Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP19b)

**SP19b owns 0 new term captures.** Per the master's corpus-wide ownership sweep + a fresh augment-time
owned by another sub-plan (forward-ref, +fin). The six pages are *procedure* authoring guides; their
underlying *concepts* (`term_provider_plugin`, `term_context_engine`, `term_agentic_memory`) are existing
substantive term notes, and no genuinely-new reusable concept survives the collision audit (the per-kind
backend ABCs are implementation surfaces documented by the procedure notes themselves, not standalone
glossary concepts).

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_hermes_plugin` | LINK only (forward-ref, +fin) [own→SP06b] | SP06b | plugin-system concept (tools/hooks/providers); SP19b authors specific provider-kind plugins, SP06b owns the umbrella concept. |
| `term_honcho` | LINK only (forward-ref, +fin) [own→SP05] | SP05 | the page's cited reference memory provider; concept home is SP05 knowledge/memory. |
| `term_context_compression` | LINK only (+fin) | SP18 | the built-in compressor a context-engine plugin replaces; developer-internals concept owned by SP18. |
| `term_fallback_provider`, `term_provider_routing` | LINK only (+fin) | SP09 | model-provider plugins feed the routing/fallback chain; concepts owned by SP09 protocols/providers. |

### Renamed (general → specific)

— (audit performed; SP19b owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP19b links; all are already scope-qualified by their owners.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_provider_plugin` (would duplicate) | `term_provider_plugin.md` (79L, concept, active) | Not captured — link the existing concept term from Notes 1/2/3/5. |
| `term_context_engine` (would duplicate) | `term_context_engine.md` (81L, concept, active) | Not captured — link the existing concept term from Note 6. |
| `term_memory_provider` / `term_video_generation` / `term_image_generation` (would be too-specific procedure-surfaces, or duplicate `term_agentic_memory`/`term_multimodal`) | `term_agentic_memory.md`, `term_multimodal.md`, `term_diffusion_model.md` (active) | Not captured — these are per-kind authoring surfaces documented by the procedure notes; link the existing concept terms. |

## Term-Note Authoring Requirements

N/A (inherited) — SP19b owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP05/06b/09/18). The full Term-Note
MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12, backlink expansion,
>200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (pilot — the densest provider guide):** Note 1 (`hermes_model_provider_plugin`). Pilot first →
  reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (backend provider plugins):** Notes 2, 3, 5 (web-search, image-gen, video-gen — same
  `kind: backend` shape). GATE G1–G8.
- **Phase 3 (single-select engine plugins):** Notes 4, 6 (memory, context-engine — single-active-provider
  rule). GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, not just planned):** add the inlink-table edges (G8). Run AFTER notes pass.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/developer-guide/<page>`
(code verbatim for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost
(Script 4, DB-verify every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** ·
G7 single-BB · **G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*provider_plugin.md "$TARGET"/${PREFIX}context_engine_plugin.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*provider_plugin.md "$TARGET"/${PREFIX}context_engine_plugin.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_model_provider_plugin hermes_web_search_provider_plugin hermes_image_gen_provider_plugin hermes_memory_provider_plugin hermes_video_gen_provider_plugin hermes_context_engine_plugin; do
```

## Entry Point Decision (inherited)

Contributes 6 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Developer: Provider & Engine Plugin Authoring" section (shared with SP19a under
the broader "Developer: Extending" group). Parent hub back-link in `entry_research_and_ai_hub.md` is handled
at master level. SP19b does NOT create a separate entry point — the >30-note corpus shares the single
master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_providers_adapters.md` | → `hermes_model_provider_plugin` | provider/adapter repo ↔ model-provider authoring doc |
| `repo_hermes_agent_plugins.md` | → `hermes_web_search_provider_plugin`, `hermes_image_gen_provider_plugin`, `hermes_video_gen_provider_plugin`, `hermes_memory_provider_plugin`, `hermes_context_engine_plugin` | plugin-system repo ↔ per-kind backend/engine authoring docs |
| `repo_hermes_agent_agent_core.md` | → `hermes_context_engine_plugin`, `hermes_memory_provider_plugin` | agent core (compression/memory) ↔ engine/memory authoring docs |
| `term_provider_plugin.md` | → `hermes_model_provider_plugin`, `hermes_web_search_provider_plugin` | concept term → per-kind authoring guides |
| `term_context_engine.md` | → `hermes_context_engine_plugin` | concept term → authoring guide |
| `term_agentic_memory.md` | → `hermes_memory_provider_plugin` | concept term → memory-backend authoring guide |
| `entry_code_snippets_hermes_agent.md` | → `hermes_model_provider_plugin`, `hermes_context_engine_plugin` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 6 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_model_provider_plugin`) → reindex → verify format/ghost/in-degree BEFORE authoring the
rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each
note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6
load-bearing examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and
split. If multi-agent: agents return note content, master writes serially where there is write-contention;
≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP19b lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 6 rows to
  the master-created entry point; backfill the `repo_hermes_agent_plugins` / `repo_hermes_agent_providers_adapters`
  / `term_*` inlinks (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- Cross-link the SP19b authoring guides bidirectionally with the SP19a `adding-providers`/`adding-tools`
  docs and the SP17 `build-a-hermes-plugin` general guide once those land.
- Consider one `thought_` note comparing Hermes' five-ABC plugin extension model (provider/web/image/video/
  memory/context-engine) vs the code-digestion findings in `snippet_hermes_agent_plugins_sdk_architecture`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (2 concept-vs-procedure LIKE non-dups confirmed by reading
  `term_provider_plugin`/`term_context_engine`), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5
  `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  ≥5 from the 13 `repo_hermes_agent_*`. All 6 notes re-levelled additively (no relevant cross-ref dropped).
- Density re-read: counts match measured (model 1600, web 1366, image 1302, memory 1137, video 1000,
  context 847); **no splits** — all 6 are single-BB procedure pages ≤1600w; code-heavy pages curated ≤6.
- Collision audit: **0 removals** — `term_provider_plugin` (concept) + `term_context_engine` (concept) +
  `term_agentic_memory` are all LINK-not-dup vs these procedure notes; no doc note duplicates an existing
  term/doc note.
- Term/snippet placeholder catch: caught + replaced before lock-in — `plugins_provider_gemini` (non-existent
  snippet) and 11 non-existent term slugs (`term_rest_api`/`term_rest_api_design`/`term_api`/`term_inference`/
  `term_summarization`/`term_text_to_image`/`term_generative_ai`/`term_generative_ai_models`/`term_video_generation`/
- Undigested terms surfaced at augment: **0 new** (SP19b owns 0 captures; all concepts owned by other SPs or
  existing terms).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs
(derived) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms
Plan ✓ Capture Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs
(N/A-inherited) ✓ invokes capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug
Specificity (N/A — 0 owned; audit noted) ✓ Slug Collision (2 concept-vs-procedure LIKE non-dups + 12 non-existent
IDs caught) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in
every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓). Term-capture items are N/A-pass (SP19b
owns 0 captures); dedup/collision items are substantively PASS (audit performed on all 6 doc notes).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**
**Independently re-reviewed 2026-06-19 (FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases + Phase 3b inlinks, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (6 rows under a Provider/Engine Plugin Authoring section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 6 notes ≤30; master holds the corpus-level split; this is part b of the SP19 split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | All 6 pages ≤1600w / ≤11 code → 1 note/page, no splits; code-heavy pages curated ≤6; each is a cohesive single-BB procedure, KEEP justified. |
| CP7 | Source counts measured | PASS | Reviewer independently re-measured all 6 inbox pages 2026-06-19 (body-word + code-fence/2): model 1600w/9, web-search 1366w/9, image-gen 1302w/7, memory 1137w/11, video-gen 1000w/4, context-engine 847w/9 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP19b owns 0 term captures (concepts owned by SP05/06b/09/18 or existing terms); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 6 doc notes (term_dictionary AND documentation/); 2 concept-vs-procedure LIKE non-dups confirmed by reading the term files (`term_provider_plugin` 79L concept, `term_context_engine` 81L concept = LINK not dup); 12 non-existent term/snippet IDs caught + replaced; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 6 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |


## Re-Sync Note (2026-06-19)

Mirror re-downloaded from NousResearch/hermes-agent `website/docs/` at main HEAD `c253b07` (was pinned
`95715dc`); independently re-measured each owned page (body-word + code-fence/2 convention). One changed page
in this sub-plan:

- `developer-guide/image-gen-provider-plugin.md` — 1181w/7code -> 1302w/7code (+121w, code unchanged)

Spot-re-measured 3 unchanged pages to confirm stability: model-provider-plugin (1600w/9), video-gen-provider-plugin
(1000w/4), context-engine-plugin (847w/9) — all unchanged.

**Density re-decision:** Note 3 (`hermes_image_gen_provider_plugin`, procedure) re-evaluated against caps.
New raw 1302w is far below the 2500w cap (and the page's ≤6-code curation from 7 blocks is unaffected); the
post-link-out planned estimate was nudged 1150→1250w. **Outcome: NO split** — Note 3 stays a single cohesive
procedure note, 1 note/page. No other planned-note density decision was affected. No new term/snippet/doc
captures triggered.

**Cross-ref floor raised 2026-06-19 (FOUR-FLOOR):** all 6 notes now carry ≥8 term + ≥5 code-repo + ≥10
snippet + ≥10 doc (snippets promoted from bonus to a counted floor and raised 8→≥10; doc floor raised
5→≥10; ≥5 code-repo from the 13 `repo_hermes_agent_*`). No planned-note filename, BB type, or gate altered;
re-levelling was additive (no relevant cross-ref dropped). **Plan remains READY for execution.**

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented FOUR-FLOOR 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed FOUR-FLOOR 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/developer-guide/{model-provider-plugin,web-search-provider-plugin,image-gen-provider-plugin,memory-provider-plugin,video-gen-provider-plugin,context-engine-plugin}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
