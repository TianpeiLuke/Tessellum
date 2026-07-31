---
title: Sub-Plan pl16 — OpenClaw Docs: Plugins (nvidia, oc-path, ollama, open-prose, openai, opencode, opencode-go)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/nvidia", "plugins/reference/oc-path", "plugins/reference/ollama", "plugins/reference/open-prose", "plugins/reference/openai", "plugins/reference/opencode", "plugins/reference/opencode-go"]
---

# Sub-Plan pl16: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_` prefix) / format (YAML + `## Overview` + `## Related Notes`) / dedup (3-way vs term_dictionary + documentation + repo_openclaw*) / 9-GATE / cross-refs / entry-point (`entry_openclaw_docs.md`) / undigested-terms (OpenClaw vocab → `oc_` notes, link existing terms) are ALL inherited from the master.

## Scope

The 7 `plugins/reference/` pages alphabetically nvidia → opencode-go. These are the **plugin-inventory reference
stubs** — one short page per built-in OpenClaw plugin package, each listing: a one-line summary, the npm
`Package` name, the `Install route` (all "included in OpenClaw"), the `Surface` it contributes (model
`providers:` IDs, capability `contracts:`, or `skills` / `plugin`), and `Related docs` pointers. Five of the
seven are **model-provider plugins** (nvidia, ollama, openai, opencode, opencode-go); one is a **CLI/path
plugin** (oc-path → `oc://` workspace addressing); one is a **skills pack** (open-prose → `/prose` slash
command). Priority **P3** (Phase C plugin-reference sprawl) — these reference the provider docs (pr-series)
and the plugin-system docs (pl01–pl04) that land in earlier phases.

**Source**: OpenClaw docs, 7 pages, **411 measured words** (avg ~59 w/page), **0 code fences**. **Planned: 3 notes**
(consolidated by surface type — see Content Strategy + Split Decisions; the master's 11-note estimate is an
aggregate ceiling that does not fit these ~60-word stubs).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| NVIDIA plugin | plugins/reference/nvidia | 54 | 0 | 3 | 0 | model |
| Oc Path plugin | plugins/reference/oc-path | 61 | 0 | 3 | 0 | concept |
| Ollama plugin | plugins/reference/ollama | 64 | 0 | 3 | 0 | model |
| Open Prose plugin | plugins/reference/open-prose | 54 | 0 | 2 | 0 | concept |
| OpenAI plugin | plugins/reference/openai | 62 | 0 | 3 | 0 | model |
| OpenCode plugin | plugins/reference/opencode | 56 | 0 | 3 | 0 | model |
| OpenCode Go plugin | plugins/reference/opencode-go | 60 | 0 | 3 | 0 | model |

H2 set per page is fixed: `## Distribution` (Package + Install route), `## Surface` (providers/contracts/skills),
`## Related docs` (omitted only on open-prose). No H3 on any page. Each page carries a 1-line lead paragraph
identical to its front-matter `summary`.

## Content Strategy

- **Consolidate, do NOT 1-note-per-page.** Each page is a ~60-word, 0-code stub of identical shape; an
  individual `oc_*` note per page would be a thin near-duplicate (Overview + 6 related-terms scaffolding would
  dwarf the ~60 words of real content, and 7 sibling stubs all repeating "package / install route / surface"
  is the anti-atomicity pattern the dedup policy guards against). Group the 7 by **Surface type** into 3
  BB-coherent reference notes.
- **Prioritize** the model-provider bundle: nvidia/ollama/openai/opencode/opencode-go are the operationally
  relevant ones (they wire model providers + capability contracts the agent runtime consumes) and the natural
  pivot to the pr-series provider docs.
- **Split out by surface** the two non-provider plugins: oc-path (CLI/`oc://` URI plugin) and open-prose
  (skills pack / `/prose` command) — different surfaces, different BB, do not belong in the provider bundle.
- **Link-out, do not redefine**: the per-provider configuration/auth lives in the `providers/*` docs (pr-series,
  e.g. `providers/nvidia`, `providers/ollama`, `providers/openai`, `providers/opencode`, `providers/opencode-go`)
  — these stubs only point there (`Related docs`); the provider names link `term_third_party_genai_services` /
  `term_llm` / `term_ollama`(no note → not promoted) etc., never inline a provider definition; the plugin
  *system* (manifest, install routes, contracts, distribution) lives in pl01–pl04 and is linked, not restated.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugin_reference_model_providers_nvidia_to_opencode_go.md` | model | nvidia.md, ollama.md, openai.md, opencode.md, opencode-go.md (all: Distribution, Surface, Related docs) | 700 | The five built-in model-provider plugins (NVIDIA, Ollama+Ollama-Cloud, OpenAI, OpenCode, OpenCode-Go): each plugin's npm package, "included in OpenClaw" install route, the provider IDs it registers, and the extra capability contracts (embedding, image/video gen, speech, transcription, realtime voice, media-understanding, web-search) it backs. A reference table mapping plugin → package → provider IDs → contracts, with pointers to each provider's config doc. |
| 2 | `oc_plugin_reference_oc_path.md` | concept | oc-path.md (Distribution, Surface, Related docs) | 350 | The `oc-path` plugin (`@openclaw/oc-path`): adds the `openclaw path` CLI and the `oc://` workspace-file addressing scheme. Surface = `plugin` (not a provider); included in OpenClaw. What `oc://` URIs are for and where the deeper docs live. |
| 3 | `oc_plugin_reference_open_prose.md` | concept | open-prose.md (Distribution, Surface) | 350 | The `open-prose` plugin (`@openclaw/open-prose`): an OpenProse VM skill pack that exposes a `/prose` slash command. Surface = `skills`; included in OpenClaw. What the skill pack provides and how it relates to OpenClaw's skills/slash-command system. |

Filename rule applied: `oc_` + slug with `/` and `-` → `_`. The consolidated note (#1) uses an aspect suffix
`_model_providers_nvidia_to_opencode_go` per the master split-suffix convention; the two single-page notes use
the page slug directly (`plugins/reference/oc-path` → `oc_plugin_reference_oc_path`; `…/open-prose` →
`oc_plugin_reference_open_prose`). One BB per note (model ×1, concept ×2).

## Section Coverage Map

```
plugins/reference/nvidia.md
├── (lead: "Adds NVIDIA model provider support") → note 1
├── ## Distribution (@openclaw/nvidia-provider; included) → note 1
├── ## Surface (providers: nvidia) ──────────────────── → note 1
└── ## Related docs ([nvidia](/providers/nvidia)) ───── → note 1 (link-out to pr-series)
plugins/reference/ollama.md
├── (lead: "Adds Ollama, Ollama Cloud model provider support") → note 1
├── ## Distribution (@openclaw/ollama-provider; included) → note 1
├── ## Surface (providers: ollama, ollama-cloud; contracts: memoryEmbeddingProviders, webSearchProviders) → note 1
└── ## Related docs ([ollama], [ollama-cloud]) ─────── → note 1 (link-out)
plugins/reference/openai.md
├── (lead: "Adds OpenAI model provider support") ───── → note 1
├── ## Distribution (@openclaw/openai-provider; included) → note 1
├── ## Surface (providers: openai; contracts: imageGenerationProviders, mediaUnderstandingProviders,
│   memoryEmbeddingProviders, realtimeTranscriptionProviders, realtimeVoiceProviders, speechProviders,
│   videoGenerationProviders) ──────────────────────── → note 1
└── ## Related docs ([openai](/providers/openai)) ──── → note 1 (link-out)
plugins/reference/opencode.md
├── (lead: "Adds OpenCode model provider support") ─── → note 1
├── ## Distribution (@openclaw/opencode-provider; included) → note 1
├── ## Surface (providers: opencode; contracts: mediaUnderstandingProviders) → note 1
└── ## Related docs ([opencode](/providers/opencode)) → note 1 (link-out)
plugins/reference/opencode-go.md
├── (lead: "Adds OpenCode Go model provider support") → note 1
├── ## Distribution (@openclaw/opencode-go-provider; included) → note 1
├── ## Surface (providers: opencode-go; contracts: mediaUnderstandingProviders) → note 1
└── ## Related docs ([opencode-go](/providers/opencode-go)) → note 1 (link-out)
plugins/reference/oc-path.md
├── (lead: "Adds the openclaw path CLI for oc:// workspace file addressing") → note 2
├── ## Distribution (@openclaw/oc-path; included) ──── → note 2
├── ## Surface (plugin) ─────────────────────────────── → note 2
└── ## Related docs ([oc-path](/plugins/oc-path)) ──── → note 2 (link-out to pl-series oc-path doc)
plugins/reference/open-prose.md
├── (lead: "OpenProse VM skill pack with a /prose slash command") → note 3
├── ## Distribution (@openclaw/open-prose; included) ─ → note 3
└── ## Surface (skills) ─────────────────────────────── → note 3
    (no ## Related docs on this page)
```
No orphaned sections. Per-provider config/auth (pr-series `providers/*`) and the plugin-system pages
(pl01–pl04: manifest, install-overrides, plugin-inventory) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| nvidia.md + ollama.md + openai.md + opencode.md + opencode-go.md (5 stubs, ~296w total, 0 code) | note 1 (single consolidated reference) | All five are the same "model-provider plugin" surface; each is ~60w. Merging into one BB-coherent reference table (plugin → package → provider IDs → contracts) avoids 5 thin near-duplicate notes (anti-atomicity / dedup-policy violation). Stays ~700w, ≤2500w cap, 0 code. |
| oc-path.md (61w) | note 2 (standalone) | Different surface (`plugin` = CLI/`oc://` URI scheme, not a provider) and different BB (concept). Belongs neither in the provider bundle nor the skills note. |
| open-prose.md (54w) | note 3 (standalone) | Different surface (`skills` pack / `/prose` command) and different BB (concept). Distinct from providers and from the CLI/path plugin. |

Net: 7 source pages → **3 notes** (1 consolidation of 5, 2 standalones). No page exceeds 2,500w; consolidation
is driven by under-density + same-surface coherence, not over-density.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (411 words, 0 code fences). New `oc_` notes: **3**. New `term_dictionary` notes: **0**.
- BB distribution: **model ×1** (note 1, the provider bundle) · **concept ×2** (notes 2–3).
- Est. digest words ~1,400 (note 1 ~700; notes 2–3 ~350 each). 0 source code fences → notes carry at most a
  small surface/contract table (not a code block); all ≤6 code-block cap trivially.
- **Cross-refs — LOCKED at RAISED floors (xref-augment 2026-06-21): ≥8 term_dictionary terms · ≥10
  repo_openclaw* + planned sibling oc_*). Per-note counts: note 1 = 12t/14s/12d; note 2 = 10t/11s/11d;
  docs alone (≥10 each); `entry_openclaw_docs` + sibling `oc_*` are planned (W1 / this series) and not

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


note_id='…'"`). Relative paths are FROM a note at `resources/documentation/openclaw/oc_X.md`: terms
`../../term_dictionary/term_Y.md`; snippets `../../code_snippets/snippet_Y.md`; docs (other folders)
`../<folder>/<file>.md`; repos `../../../areas/code_repos/repo_Y.md`; entry points
`../../../0_entry_points/entry_Y.md`; sibling oc docs (this series, not yet created) `oc_Y.md`. `entry_openclaw_docs`
and the two sibling `oc_*` notes are **planned (not yet in DB)** — cited toward the 10-doc floor as
(≥5 required, all notes have ≥10 existing).

### oc_plugin_reference_model_providers_nvidia_to_opencode_go (12t · 14s · 12d)

Source: the five model-provider plugin stubs (nvidia / ollama / openai / opencode / opencode-go) — npm package,
"included in OpenClaw" install route, registered provider IDs, capability contracts (embedding, image/video gen,
speech, transcription, realtime voice, media-understanding, web-search), related-docs pointers.

**Terms (12):**
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers model provider IDs (package → providers); the exact canonical concept for all five stubs.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — these are OpenClaw's built-in plugin packages; the parent product whose runtime loads them.
- [term_llm](../../term_dictionary/term_llm.md) — every plugin here registers a model provider fronting one or more LLMs.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — NVIDIA, OpenAI, OpenCode(-Go) are external GenAI services these plugins connect to.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — installing these plugins populates the runtime's available-model catalog with each provider's models.
- [term_vllm](../../term_dictionary/term_vllm.md) — Ollama is a local/self-hosted inference server in the same class as vLLM; both back local model providers.
- [term_quantization](../../term_dictionary/term_quantization.md) — Ollama serves quantized open-weight models locally; relevant to the local-provider (ollama) entry.
- [term_embedding](../../term_dictionary/term_embedding.md) — the ollama + openai plugins back the `memoryEmbeddingProviders` contract (embedding generation for memory search).
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — the openai plugin backs `realtimeTranscriptionProviders` / `speechProviders` (transcription).
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — the openai plugin backs `speechProviders` / `realtimeVoiceProviders` (TTS / realtime voice).
- [term_multimodal](../../term_dictionary/term_multimodal.md) — `mediaUnderstandingProviders` (opencode, opencode-go, openai) + `imageGenerationProviders`/`videoGenerationProviders` (openai) are multimodal contracts.
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — the openai provider plugin fronts OpenAI's Responses/Chat APIs.

**Docs (12):** _≥10 floor met on 10 existing + 2 planned-sibling_
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — the sibling coding-agent's "model provider plugin" doc: the closest existing analog of this note's exact subject (plugin → registered provider).
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — Hermes' built-in/bundled plugin inventory, the analog of OpenClaw's "included in OpenClaw" plugin reference.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud model-provider catalog (OpenAI/NVIDIA/etc. families), the provider configs these stubs point to.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama provider setup, the deeper config for the ollama plugin documented here.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted/local LLM serving (Ollama-class), context for the ollama + opencode local providers.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider plugin, the analog of the openai plugin's `imageGenerationProviders` contract.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text/transcription, the analog of the openai plugin's `realtimeTranscriptionProviders`/`speechProviders`.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS provider configuration, analog of the openai plugin's `speechProviders`/`realtimeVoiceProviders`.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — how the Pi coding agent registers a custom model provider, parallel to how these plugins register provider IDs.
- [band_adapter_opencode](../band/band_adapter_opencode.md) — the Band OpenCode adapter, a cross-corpus counterpart to the opencode/opencode-go provider plugins.
- [oc_plugin_reference_oc_path](oc_plugin_reference_oc_path.md) — (planned, this series) sibling plugin-reference note (CLI/path plugin).

**Repos:**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the code-side package implementing exactly these LLM-provider extensions (nvidia/ollama/openai/opencode).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework that loads provider plugins via contracts.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agent runtime that consumes the registered providers + capability contracts.

**Snippets (14):**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — concrete local-Ollama provider config (the code form of the ollama plugin's surface).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — concrete OpenAI-compatible provider definition matching the openai plugin.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — sibling built-in provider-plugin definition; same package→provider shape as these five.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — an aggregator provider plugin, same provider-registration pattern across many models.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — the plugin package/contract shape (package → surface) these stubs describe.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — how a plugin declares its entry points/surface, the SDK form of `## Surface`.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — how registered providers feed the model catalog these plugins populate.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a speech/TTS provider implementation, the code form of the openai plugin's speech contracts.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Ollama-Cloud provider plugin in the sibling agent (the openclaw ollama plugin registers `ollama-cloud`).
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — generic custom provider-plugin skeleton; the package→provider pattern these five follow.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — the provider registry that maps provider IDs to plugins, what `providers:` in `## Surface` populates.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — a coding-model provider plugin (codex/opencode class), analog of the opencode/opencode-go plugins.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch wiring, how registered providers are loaded at startup.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch, code form of the openai plugin's `imageGenerationProviders`/`videoGenerationProviders`.

### oc_plugin_reference_oc_path (10t · 11s · 11d)

Source: oc-path.md — `@openclaw/oc-path`, included; Surface = `plugin`; the `openclaw path` CLI + `oc://`
workspace-file addressing scheme; Related docs → `/plugins/oc-path`.

**Terms (10):**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — `oc://` is OpenClaw's workspace URI scheme; this plugin is part of OpenClaw's CLI surface.
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin declares its CLI/`plugin` surface via its manifest, the mechanism this stub abbreviates as `## Surface`.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — oc-path is built on the OpenClaw plugin SDK that lets a plugin add a CLI/path capability.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — `oc://` addressing scopes file access to the agent workspace/sandbox, the boundary it resolves paths within.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — the workspace/file backend the `oc://` scheme resolves paths against.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — `oc://` paths are how tools/file-ops reference workspace files in tool calls.
- [term_openshell](../../term_dictionary/term_openshell.md) — OpenClaw's CLI/shell surface that the `openclaw path` command extends.
- [term_node_js](../../term_dictionary/term_node_js.md) — the plugin ships as an npm package (`@openclaw/oc-path`) run on the Node/Bun runtime.
- [term_npm](../../term_dictionary/term_npm.md) — distributed as an npm package; the `Package` field is its npm name.

**Docs (11):** _≥10 floor met on 9 existing + 2 planned-sibling_
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — the sibling agent's plugin system; how a bundled plugin contributes a `plugin`/CLI surface (oc-path's surface type).
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — enumerates plugin surface types (provider/skills/plugin), placing oc-path's `plugin` surface in context.
- [hermes_cli_interface](../hermes_agent/hermes_cli_interface.md) — the agent CLI surface; analog of the `openclaw path` CLI command oc-path adds.
- [hermes_context_references](../hermes_agent/hermes_context_references.md) — referencing workspace files/context by path, the analog of the `oc://` addressing scheme.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — terminal/CLI backends, context for a CLI-surface plugin like oc-path.
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — Claude Code plugin CLI commands, the cross-corpus analog of a plugin adding a CLI command.
- [cc_plugin_directory_structure](../claude_code/cc_plugin_directory_structure.md) — plugin package layout (the package→surface mapping oc-path's `## Distribution`/`## Surface` express).
- [cc_permissions_hooks_and_working_directories](../claude_code/cc_permissions_hooks_and_working_directories.md) — working-directory/path scoping, the cross-corpus analog of `oc://` workspace addressing.
- [pi_packages](../pi/pi_packages.md) — how the Pi agent packages/installs plugins, parallel to oc-path's npm-package distribution.
- [oc_plugin_reference_model_providers_nvidia_to_opencode_go](oc_plugin_reference_model_providers_nvidia_to_opencode_go.md) — (planned, this series) sibling plugin-reference note.

**Repos:**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the main OpenClaw repo where the bundled `oc-path` plugin lives.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — OpenClaw's CLI layer, the surface `oc-path` extends with the `openclaw path` command.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension framework that registers `oc-path`'s `plugin` surface.

**Snippets (11):**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — the package→surface contract describing how `oc-path` declares a `plugin` surface.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — the plugin load/lifecycle this bundled plugin follows.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — how a plugin declares entry points/surface (oc-path's `plugin`/CLI entry).
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — the CLI bootstrap that loads bundled CLI plugins like the `openclaw path` command.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing, how `openclaw path` would be dispatched.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — the workspace/file backend a `plugin`-surface tool like oc-path resolves paths against.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — how bundled plugins/imports are wired into setup, including CLI-surface plugins.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — the plugin SDK architecture oc-path's `plugin` surface is built on.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — the plugin manifest schema that declares a `plugin`/CLI surface (what `## Surface` abbreviates).
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — CLI plugin list/info command; how a bundled CLI plugin is surfaced.
- [snippet_hermes_agent_plugins_interfaces_abcs](../../code_snippets/snippet_hermes_agent_plugins_interfaces_abcs.md) — the plugin interface/ABCs a `plugin`-surface plugin implements.

### oc_plugin_reference_open_prose (10t · 11s · 11d)

Source: open-prose.md — `@openclaw/open-prose`, included; Surface = `skills`; an OpenProse VM skill pack that
exposes a `/prose` slash command (page has no Related docs).

**Terms (10):**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — open-prose is a built-in OpenClaw skill pack; OpenClaw's skills/slash-command system hosts it.
- [term_skills](../../term_dictionary/term_skills.md) — the surface this plugin contributes is `skills`; this is the canonical concept for a skill pack.
- [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — a skill pack declares its skills + `/prose` command via a skill manifest, what `## Surface: skills` abbreviates.
- [term_skills_hub](../../term_dictionary/term_skills_hub.md) — the registry/hub that loads and exposes skill packs like open-prose.
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin manifest declares the `skills` surface; oc-path/open-prose differ only by declared surface.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — open-prose is built on the OpenClaw plugin SDK's skills/slash-command surface.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — a skill pack extends what the coding agent can do (here prose/long-form writing) via a slash command.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — slash commands/skills are surfaced by the agent harness that runs the OpenClaw agent.
- [term_node_js](../../term_dictionary/term_node_js.md) — shipped as an npm package (`@openclaw/open-prose`) on the Node/Bun runtime.
- [term_npm](../../term_dictionary/term_npm.md) — distributed via npm; `Package` is its npm name.

**Docs (11):** _≥10 floor met on 9 existing + 2 planned-sibling_
- [hermes_skills_system](../hermes_agent/hermes_skills_system.md) — the sibling agent's skills system; how a `skills`-surface pack is loaded and run (open-prose's surface type).
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — using skills/skill packs end-to-end, the user-facing analog of installing open-prose.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — the skills hub that manages/exposes skill packs, analog of where open-prose registers.
- [hermes_skill_md_format_bundles](../hermes_agent/hermes_skill_md_format_bundles.md) — the skill bundle/SKILL.md format a skill pack like open-prose ships in.
- [hermes_creating_skill_format](../hermes_agent/hermes_creating_skill_format.md) — authoring a skill pack, the build-side of what open-prose is.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — slash commands surfaced in the CLI, the analog of open-prose's `/prose` command.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — Claude Code skill authoring, the cross-corpus analog of a `skills`-surface pack.
- [cc_sdk_slash_commands](../claude_code/cc_sdk_slash_commands.md) — registering slash commands, the cross-corpus analog of the `/prose` command.
- [pi_skills](../pi/pi_skills.md) — the Pi agent's skills mechanism, parallel skill-pack surface in another coding agent.
- [oc_plugin_reference_oc_path](oc_plugin_reference_oc_path.md) — (planned, this series) sibling plugin-reference note.

**Repos:**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw's skills subsystem that loads/exposes skill packs like open-prose.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the main repo bundling the `open-prose` plugin.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework registering the skill-pack plugin.

**Snippets (11):**
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — how OpenClaw plans/loads skills, the runtime side of a `skills`-surface pack.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — the skills manifest format a skill pack like open-prose declares.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — the package→surface contract describing how open-prose declares a `skills` surface.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — how a plugin exposes entry points (a `/prose` slash command, a `skills` surface).
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — the plugin load/lifecycle a bundled skill pack follows.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — the skills-vs-plugins distinction; open-prose is a plugin that contributes a `skills` surface.
- [snippet_hermes_agent_skills_canonical_loading_runtime](../../code_snippets/snippet_hermes_agent_skills_canonical_loading_runtime.md) — skill canonical loading at runtime, how a pack's skills become callable.
- [snippet_hermes_agent_core_skill_commands_discovery](../../code_snippets/snippet_hermes_agent_core_skill_commands_discovery.md) — discovery of skill/slash commands, how `/prose` would be found and registered.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — the plugin manifest schema that declares a `skills` surface (what `## Surface: skills` abbreviates).
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — the plugin SDK architecture open-prose's `skills` surface is built on.
- [snippet_hermes_agent_optional_skills_migration_openclaw](../../code_snippets/snippet_hermes_agent_optional_skills_migration_openclaw.md) — migrating OpenClaw skills, directly references OpenClaw's skill-pack surface.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_` doc notes (these reference stubs), NOT new
`term_dictionary` entries; the only term interaction is **linking existing** terms. Expected new
`term_dictionary` captures: **0**.

| Term (appears in source) | Disposition |
|---|---|
| NVIDIA / OpenAI / OpenCode / OpenCode-Go / Ollama (provider names) | Documented as plugin/provider config inside `oc_` notes; NOT promoted to term notes. Link `term_third_party_genai_services` / `term_llm`; per-provider config is the pr-series provider docs. |
| Ollama (as local-inference engine) | No `term_ollama` exists; NOT promoted (it is a provider name documented in-note). Link `term_vllm` (closest existing local-inference concept) + `term_quantization`. |
| model provider / provider plugin | Link existing `term_provider_plugin`. |
| capability contracts (memoryEmbeddingProviders, webSearchProviders, imageGenerationProviders, videoGenerationProviders, mediaUnderstandingProviders, realtimeTranscriptionProviders, realtimeVoiceProviders, speechProviders) | OpenClaw-internal contract vocabulary → described in `oc_` note 1; concepts link existing `term_embedding`, `term_speech_to_text`, `term_text_to_speech`, `term_multimodal`. Not promoted (too OpenClaw-specific / not a single reusable cross-cutting concept). |
| `oc://` / openclaw path CLI | OpenClaw workspace URI scheme → documented in `oc_` note 2; link `term_sandbox`. Not a reusable cross-vault term. |
| OpenProse / `/prose` slash command / skill pack | OpenClaw feature → documented in `oc_` note 3; link `term_autonomous_coding_agents`, `term_agent_harness`. Not promoted. |
| npm package / "included in OpenClaw" install route | Link existing `term_npm` / `term_node_js`. |

**New-term candidates: none.** No genuinely reusable cross-cutting term lacking an existing note appears in
these 7 stubs (all vocabulary is OpenClaw-specific plugin/provider/contract naming covered by `oc_` notes or
linkable to existing terms). If augment's Step 2d re-scan surfaces one, it would route to
`acronym_glossary_agentic_ai.md` (best fit) — not anticipated.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master: OpenClaw
vocabulary → `oc_` doc notes; existing terms linked only).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (3 notes, P3). All gates must pass before commit.

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order/values correct (tags lead `resource`/`documentation`/`openclaw`); `## Overview` + `## Related Notes` present; footer present; itemized keyword/topic lists; no forbidden YAML fields. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/plugins/reference/<page>.md`) | Every package name, provider ID, contract name, install route reproduced faithfully; no invented surfaces/contracts. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2500 words / ≤6 code blocks; one BB per note; every source H2/H3 mapped (Section Coverage Map, no orphans). |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken links after incremental reindex. |
| G7 | Discoverability — outbound | Each note links out (provider/plugin-system docs, terms, repos). |
| G8 | Discoverability — inbound (in-degree ≥1) | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` rows + repo/term inlinks). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugin_reference_model_providers_nvidia_to_opencode_go oc_plugin_reference_oc_path oc_plugin_reference_open_prose"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec] in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # sibling-prefix sanity (note filename carries series prefix)
  case "$n" in ${SIBLING_PREFIX}*) ;; *) echo "BAD PREFIX: $n" ;; esac
  # density caps (≤2500 words, ≤6 code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G2 grounding spot-check (package/provider IDs present in source)
for p in nvidia oc-path ollama open-prose openai opencode opencode-go; do
  echo "== $p =="; grep -E 'Package:|providers:|contracts:|skills' "inbox/openclaw_docs/plugins/reference/$p.md"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugin_reference_model_providers_nvidia_to_opencode_go | model | 700 | 0 (1 surface table) | ✅ (≤2500w / ≤6 code / ≤400L) |
| 2 | oc_plugin_reference_oc_path | concept | 350 | 0 | ✅ |
| 3 | oc_plugin_reference_open_prose | concept | 350 | 0 | ✅ |

No note approaches caps; the risk for this sub-plan is **under-density**, not over-density — addressed by
consolidation (note 1 merges 5 stubs into one ~700w reference rather than 5 thin ~200w notes). 0 source code
fences, so each note has at most one small surface/contract table.

## Entry Point Decision (inherited from master)

Contributes **3 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **Plugins →
Reference** cluster (pl-series). Each new note gets the entry-point back-link at finalization (supplies the
G7/G8 inbound link, anti-island). No new entry point is created by this sub-plan.

| Note | Entry-point cluster | Row gist |
|---|---|---|
| oc_plugin_reference_model_providers_nvidia_to_opencode_go | Plugins → Reference (providers) | 5 built-in model-provider plugins (nvidia/ollama/openai/opencode/opencode-go): package, provider IDs, contracts. |
| oc_plugin_reference_oc_path | Plugins → Reference (cli/path) | `oc-path` plugin: `openclaw path` CLI + `oc://` workspace addressing. |
| oc_plugin_reference_open_prose | Plugins → Reference (skills) | `open-prose` plugin: OpenProse skill pack + `/prose` slash command. |

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all targets below confirmed present
2026-06-20):

- `entry_openclaw_docs.md` (master pre-step) → all 3 notes (primary anti-island inbound).
- `repo_openclaw_extensions_llm_providers.md` → note 1 (code-side counterpart of the model-provider plugins).
- `repo_openclaw_extensions.md` → notes 1, 2, 3 (the plugin/extension framework that loads all three).
- `repo_openclaw_skills.md` → note 3 (skills subsystem hosting open-prose).
- `repo_openclaw_cli_wizard.md` → note 2 (CLI layer that `oc-path` extends).
- `term_provider_plugin.md` → note 1; `term_openclaw.md` → all 3 (reciprocal term backlinks).

DB-verify command (run per cited EXISTING note_id before locking, per master G5):
```bash
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
# (suffix-match form used during authoring: note_id LIKE '%/<stem>.md')
```

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page; reproduce package/provider/contract
names verbatim. One BB per note. Cap dynamic-workflow fan-out at ~30 agents/run; commit+push after the phase
(`git pull --rebase --autostash` first; no Claude co-author trailer); incremental reindex + verify `note_links`
+ 0 broken links before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope:** per-note Related Notes mapping locked at RAISED floors (≥8 terms · ≥10 snippets · ≥10 docs per
note), replacing the inherited ≥6-term draft. The 7 source stubs were re-read verbatim from
`inbox/openclaw_docs/plugins/reference/{nvidia,oc-path,ollama,open-prose,openai,opencode,opencode-go}.md`;
grounding confirmed (every package name, provider ID, and contract name in the plan matches source exactly —
e.g. openai's 7 contracts, ollama's `providers: ollama, ollama-cloud; contracts: memoryEmbeddingProviders,
webSearchProviders`).


| Note | Terms | Snippets | Docs (existing + planned) | Repos | Floors met (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_plugin_reference_model_providers_nvidia_to_opencode_go | 12 | 14 | 12 (10 existing + 2 planned) | 3 | YES |
| oc_plugin_reference_oc_path | 10 | 11 | 11 (9 existing + 2 planned) | 3 | YES |
| oc_plugin_reference_open_prose | 10 | 11 | 11 (9 existing + 2 planned) | 3 | YES |

2 planned entries per note (`entry_openclaw_docs` at W1 + one sibling `oc_*`) are cited for completeness but
docs — the closest sibling coding-agent corpus), `claude_code/cc_*`, `pi/pi_*`, `band/band_*`, `aws_bedrock/`,
docs) surfaced by BM25 were discarded.

**DB-verification:** every cited EXISTING note_id verified via
intentionally-planned ones: `0_entry_points/entry_openclaw_docs.md` (W1 master pre-step) and the two sibling
`oc_plugin_reference_*` notes (this series), all explicitly marked "(planned …)".

**New-term candidates:** NONE. The 7 stubs contain only OpenClaw-specific plugin/provider/contract vocabulary
(provider names → linked to `term_third_party_genai_services`/`term_llm`; contract names → linked to
`term_embedding`/`term_multimodal`/`term_speech_to_text`/`term_text_to_speech`; `oc://`/`/prose`/skill-pack →
documented in-note). No genuinely cross-cutting, vault-reusable term lacking an existing note appears. Step 2d
re-scan surfaced 0 new terms (consistent with the master's "OpenClaw vocab → `oc_` docs, link existing terms;
expected new term captures = 0" design). Best-fit glossary if one ever surfaces: `acronym_glossary_agentic_ai.md`.

**Undigested-terms / authoring requirements:** unchanged — N/A (0 new `term_dictionary` notes; the
Term-Note Authoring Requirements section remains N/A per master design).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | Per-Note Related Notes Mapping (LOCKED) present; every note ≥8 terms (12/10/10), ≥10 snippets (14/11/11), ≥10 docs (12/11/11), each link carries a relevance statement; raised floors locked. |
| CP2 | 9-GATE present per batch (G1-G6, G7/G8) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table has G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (updated to raised floors), G5 ghost-detect, G6 broken-link, G7 outbound, G8 inbound — single execution phase, all gates present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | Entry Point Decision + Inlinks sections name `entry_openclaw_docs.md` (master W1 pre-step) as the anti-island inbound for all 3 notes; 3 rows under Plugins → Reference cluster; sub-plan correctly creates no new entry point. |
| CP4 | Size | **PASS** | 3 notes — far ≤30; no sub-plan split needed. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` + `## Related Notes` + footer; YAML field order; forbidden-field list); not invented. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 3 notes well under caps (700/350/350 w, 0 code fences); the risk here is under-density (addressed by consolidating 5 stubs into note 1), not over-density; no borderline note. |
| CP7 | Sources measured | **PASS** | All 7 source pages re-read this session (verbatim cat); measured ~54-64 w/page, 0 code fences each — matches the plan's Source table (411 total words) within ±0; no under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | Undigested Terms Plan present (disposition table: all OpenClaw vocab → `oc_` notes / link existing terms; 0 promotions); Term-Note Authoring Requirements present as N/A (0 new terms) per master design; new-term candidates = none. |
| CP8f | Slug/collision audit | **PASS** | 0 new term slugs to audit (0 captures). Note-filename collision audit: the 3 `oc_plugin_reference_*` slugs do not exist in DB (verified — they are the to-be-created targets) and do not duplicate existing `term_*`/doc notes; provider/contract concepts are LINKED to existing notes, not recreated. |
| CP9 | Discoverability / inlinks | **PASS** | Inlinks section maps ≥1 outside-folder inbound per note (`entry_openclaw_docs` → all 3; `repo_openclaw_extensions` → all 3; `repo_openclaw_extensions_llm_providers` → note 1; `repo_openclaw_skills` → note 3; `repo_openclaw_cli_wizard` → note 2; term backlinks); G8 in the gate table marks inlinks as an EXECUTED phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
