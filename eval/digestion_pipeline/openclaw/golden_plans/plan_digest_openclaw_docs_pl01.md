---
title: Sub-Plan pl01 — OpenClaw Docs: Plugins (Architecture, Building, Bundles, Backends)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/adding-capabilities", "plugins/admin-http-rpc", "plugins/architecture", "plugins/architecture-internals", "plugins/building-plugins", "plugins/bundles", "plugins/cli-backend-plugins"]
---

# Sub-Plan pl01: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*` prefix), Format Definition, dedup-before-create, 9-GATE
> validation, cross-reference policy, Undigested-Terms ownership, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 foundational **plugin-system** pages of the OpenClaw docs: how the public capability model works
(`architecture`), the internal load pipeline / registry / runtime-hook mechanics (`architecture-internals`),
the first-plugin tutorial (`building-plugins`), how to add a new capability across the provider/harness seams
(`adding-capabilities`), CLI inference backend plugins (`cli-backend-plugins`), third-party plugin bundle
adoption (`bundles`), and the gateway admin HTTP-RPC plugin-management surface (`admin-http-rpc`). These define
the plugin/capability/registry vocabulary that the entire `pl02`–`pl25` plugin-reference sprawl depends on, so
within the P3 plugins band this is the priority sub-plan. The CODE-side counterparts
(`repo_openclaw`, `repo_openclaw_extensions`, `repo_openclaw_extensions_llm_providers`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **16,746 measured words** (Step 2, mirror `inbox/openclaw_docs/plugins/`).
**Planned: 10 notes** (master index estimated 11; measured splits lock at 10 — see Summary Statistics).
Priority **P3** (master Phase C).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| adding-capabilities | /plugins/adding-capabilities | 747 | 0 | 9 | 0 | procedure |
| admin-http-rpc | /plugins/admin-http-rpc | 1,003 | 7 | 11 | 0 | procedure |
| architecture | /plugins/architecture | 3,508 | 1 | 8 | 12 | concept (split: capability model vs ownership/contracts/execution) |
| architecture-internals | /plugins/architecture-internals | 6,987 | 18 | 15 | 9 | model + concept (split ×3: load/registry, runtime hooks/helpers, gateway/SDK/catalog reference) |
| building-plugins | /plugins/building-plugins | 1,440 | 8 | 10 | 0 | procedure |
| bundles | /plugins/bundles | 1,542 | 2 | 10 | 2 | procedure |
| cli-backend-plugins | /plugins/cli-backend-plugins | 1,519 | 5 | 9 | 1 | procedure |

*(Code = raw ``` fence count ÷ 2. Totals: 16,746 words, ~41 code blocks.)*

## Content Strategy

- **Prioritize**: the public **capability model** (every reference plugin in pl02–pl25 registers a capability;
  this is the most-referenced concept) and the **load pipeline / registry** internals (explains how a manifest
  becomes a live registration — the mental model for debugging plugin load order). These are P3's conceptual core.
- **Split** the two oversized pages: `architecture` (3,508w > 2,500w cap) → 2 concept notes (public capability
  model + plugin shapes/compatibility; then ownership / contracts / execution / export boundary). `architecture-internals`
  (6,987w, 18 code blocks, 15 H2 spanning load pipeline → registry → runtime hooks → HTTP routes → SDK paths →
  schemas → catalogs → packs → context-engine → add-a-capability) → 3 notes (load+registry model; runtime hooks +
  helpers; gateway HTTP routes / SDK import paths / message-tool & catalog reference). See Split Decisions.
- **Keep 1:1** the four focused procedure pages: `adding-capabilities`, `building-plugins`, `bundles`,
  `cli-backend-plugins`, `admin-http-rpc` (each ≤1,600w, single BB, single task cluster).
- **Link-out, do not redefine**: plugin-reference pages (pl02–pl25), `tools/plugin` end-user guide (to06),
  `cli/plugins` command (cl06), `gateway/*` config (gw0x), SDK pages (`plugins/sdk-*`, pl23–25); terms
  `term_mcp` / `term_function_calling` / `term_provider_plugin` / `term_plugin_sdk` / `term_plugin_manifest`
  linked, never inlined. No `term_dictionary` definition is reproduced in any `oc_*` note (master decision).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_architecture_capability_model.md` | concept | architecture.md: Public capability model, External compatibility stance, Plugin shapes, Legacy hooks, Compatibility signals, Architecture overview | 650 | The public native-plugin capability model: the capability-type table (text/CLI/embeddings/speech/media/image/music/video/web/channel/discovery), plugin shapes (plain/hybrid/hook-only/non-capability), legacy-hook compatibility stance, and the four-layer architecture overview. |
| 2 | `oc_plugins_architecture_ownership_contracts.md` | concept | architecture.md: Capability ownership model (layering, multi-capability example, video-understanding example), Contracts and enforcement, Execution model, Export boundary, Internals and reference | 650 | The capability ownership and enforcement model: capability layering, multi-capability "company" plugins, what belongs in a contract, contract enforcement, the execution model, and the public export boundary between core and plugins. |
| 3 | `oc_plugins_architecture_internals_load_registry.md` | concept | architecture-internals.md: Load pipeline (manifest-first behavior, plugin cache boundary), Registry model | 600 | The plugin load pipeline and registry model: startup discovery → manifest read → safety gates → enablement → native module load (native loader vs Jiti fallback) → `register(api)` → registry exposure; manifest-first control-plane behavior, plugin cache boundary, and the registry record shape. |
| 4 | `oc_plugins_architecture_internals_runtime_hooks.md` | concept | architecture-internals.md: Conversation binding callbacks, Provider runtime hooks (hook order and usage, provider example, built-in examples, `api.runtime.imageGeneration`), Runtime helpers, Adding a new capability (checklist, template) | 700 | The plugin runtime hook surface: conversation-binding callbacks, provider runtime hooks (hook order/usage, `before_model_resolve` / `before_prompt_build`, `api.runtime.*` accessors), runtime helpers, and the internal checklist+template for adding a new capability. |
| 5 | `oc_plugins_architecture_internals_gateway_sdk_reference.md` | model | architecture-internals.md: Gateway HTTP routes, Plugin SDK import paths, Message tool schemas, Channel target resolution, Config-backed directories, Provider catalogs (channel catalog metadata), Read-only channel inspection, Package packs, Context engine plugins | 700 | Reference tables for the plugin internals: gateway HTTP routes, SDK import subpaths, message-tool schemas, channel target resolution, config-backed directories, provider/channel catalog metadata, read-only channel inspection, package packs, and context-engine plugins. |
| 6 | `oc_plugins_building_plugins.md` | procedure | building-plugins.md: Requirements, Choose the plugin shape, Quickstart, Registering tools, Import conventions, Pre-submission checklist, Test against beta releases, Next steps | 600 | First-plugin tutorial: requirements, choosing a plugin shape, the smallest working manifest + quickstart, registering tools, import conventions, the pre-submission checklist, and testing against beta releases. |
| 7 | `oc_plugins_adding_capabilities.md` | procedure | adding-capabilities.md: When to create a capability, The standard sequence, What goes where, Provider and harness seams, File checklist, Worked example (image generation), Embedding providers, Review checklist | 500 | How to add a brand-new capability type across the provider/harness seams: when to create one, the standard implementation sequence, what goes where, the file checklist, a worked image-generation example, embedding providers, and the review checklist. |
| 8 | `oc_plugins_cli_backend_plugins.md` | procedure | cli-backend-plugins.md: What the plugin owns, Minimal backend plugin, Config shape, Advanced backend hooks (`ownsNativeCompaction`), MCP tool bridge, User configuration, Verification, Checklist | 600 | CLI inference backend plugins: what the plugin owns, the minimal `registerCliBackend` plugin, config shape, advanced backend hooks (`ownsNativeCompaction` opt-out), the MCP tool bridge, user configuration, and verification. |
| 9 | `oc_plugins_bundles.md` | procedure | bundles.md: Why bundles exist, Install a bundle, What OpenClaw maps from bundles (supported now / detected-but-not-executed), Bundle formats, Detection precedence, Runtime dependencies and cleanup, Security, Troubleshooting | 600 | Third-party plugin bundles: why they exist, installing a bundle, what OpenClaw maps from a bundle manifest (supported vs detected-not-executed), bundle formats, detection precedence, runtime-dependency cleanup, security posture, and troubleshooting. |
| 10 | `oc_plugins_admin_http_rpc.md` | procedure | admin-http-rpc.md: Before you enable it, Enable, Verify the route, Authentication, Security model, Request, Response, Allowed methods, WebSocket comparison, Troubleshooting | 600 | The gateway admin HTTP-RPC surface for plugin/gateway management: enabling the route, verifying it, authentication, the security model, request/response shape, the allowed-method allowlist, the WebSocket comparison, and troubleshooting. |

*(Note 4 + Note 5 together cover the back half of `architecture-internals.md`; see Section Coverage Map for the exact H2→note split.)*

## Section Coverage Map

```
adding-capabilities.md
├── When to create a capability ─────────────────── → note 7 (oc_plugins_adding_capabilities)
├── The standard sequence ───────────────────────── → note 7
├── What goes where ─────────────────────────────── → note 7
├── Provider and harness seams ──────────────────── → note 7
├── File checklist ──────────────────────────────── → note 7
├── Worked example: image generation ────────────── → note 7
├── Embedding providers ─────────────────────────── → note 7
├── Review checklist ────────────────────────────── → note 7
└── Related ─────────────────────────────────────── → (mapped into note 7 Related Notes)
admin-http-rpc.md
├── Before you enable it / Enable / Verify the route → note 10 (oc_plugins_admin_http_rpc)
├── Authentication / Security model ─────────────── → note 10
├── Request / Response / Allowed methods ────────── → note 10
├── WebSocket comparison / Troubleshooting ──────── → note 10
└── Related ─────────────────────────────────────── → (note 10 Related Notes)
architecture.md
├── Public capability model ─────────────────────── → note 1 (oc_plugins_architecture_capability_model)
│   ├── External compatibility stance ───────────── → note 1
│   ├── Plugin shapes ───────────────────────────── → note 1
│   ├── Legacy hooks ────────────────────────────── → note 1
│   └── Compatibility signals ───────────────────── → note 1
├── Architecture overview ───────────────────────── → note 1
├── Capability ownership model ──────────────────── → note 2 (oc_plugins_architecture_ownership_contracts)
│   ├── Capability layering ─────────────────────── → note 2
│   ├── Multi-capability company plugin example ──── → note 2
│   └── Capability example: video understanding ──── → note 2
├── Contracts and enforcement (What belongs in a contract) → note 2
├── Execution model ─────────────────────────────── → note 2
├── Export boundary / Internals and reference ───── → note 2
└── Related ─────────────────────────────────────── → (notes 1+2 Related Notes)
architecture-internals.md
├── Load pipeline ───────────────────────────────── → note 3 (oc_plugins_architecture_internals_load_registry)
│   ├── Manifest-first behavior ─────────────────── → note 3
│   └── Plugin cache boundary ───────────────────── → note 3
├── Registry model ──────────────────────────────── → note 3
├── Conversation binding callbacks ──────────────── → note 4 (oc_plugins_architecture_internals_runtime_hooks)
├── Provider runtime hooks ──────────────────────── → note 4
│   ├── Hook order and usage ────────────────────── → note 4
│   ├── Provider example / Built-in examples ─────── → note 4
│   └── `api.runtime.imageGeneration` ───────────── → note 4
├── Runtime helpers ─────────────────────────────── → note 4
├── Adding a new capability (Capability checklist, Capability template) → note 4
├── Gateway HTTP routes ─────────────────────────── → note 5 (oc_plugins_architecture_internals_gateway_sdk_reference)
├── Plugin SDK import paths ─────────────────────── → note 5
├── Message tool schemas ────────────────────────── → note 5
├── Channel target resolution ───────────────────── → note 5
├── Config-backed directories ───────────────────── → note 5
├── Provider catalogs (Channel catalog metadata) ── → note 5
├── Read-only channel inspection ────────────────── → note 5
├── Package packs ───────────────────────────────── → note 5
├── Context engine plugins ──────────────────────── → note 5
└── Related ─────────────────────────────────────── → (notes 3+4+5 Related Notes)
building-plugins.md
├── Requirements / Choose the plugin shape ──────── → note 6 (oc_plugins_building_plugins)
├── Quickstart / Registering tools ──────────────── → note 6
├── Import conventions / Pre-submission checklist ─ → note 6
├── Test against beta releases / Next steps ─────── → note 6
└── Related ─────────────────────────────────────── → (note 6 Related Notes)
bundles.md
├── Why bundles exist / Install a bundle ────────── → note 9 (oc_plugins_bundles)
├── What OpenClaw maps from bundles ─────────────── → note 9
│   ├── Supported now ───────────────────────────── → note 9
│   └── Detected but not executed ───────────────── → note 9
├── Bundle formats / Detection precedence ───────── → note 9
├── Runtime dependencies and cleanup ────────────── → note 9
├── Security / Troubleshooting ──────────────────── → note 9
└── Related ─────────────────────────────────────── → (note 9 Related Notes)
cli-backend-plugins.md
├── What the plugin owns / Minimal backend plugin ─ → note 8 (oc_plugins_cli_backend_plugins)
├── Config shape / Advanced backend hooks ───────── → note 8
│   └── `ownsNativeCompaction` ──────────────────── → note 8
├── MCP tool bridge / User configuration ────────── → note 8
├── Verification / Checklist ────────────────────── → note 8
└── Related ─────────────────────────────────────── → (note 8 Related Notes)
```
**No orphaned sections.** Each page's `## Related` block folds into the target note(s)' Related Notes. The
inter-page Card/redirect links (`tools/plugin`, `cli/plugins`, `plugins/sdk-*`) are link-outs to other sub-plans,
not in-pl01 content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `architecture.md` (3,508w, 8 H2 / 12 H3, concept) | notes 1 + 2 | Exceeds the 2,500-word cap. Two distinct conceptual clusters: (a) the public capability **model** + plugin shapes + compatibility stance (what a plugin IS), vs (b) the capability **ownership / contracts / execution / export boundary** (how capabilities are governed). Splitting keeps each note one focused concept and ≤700w. |
| `architecture-internals.md` (6,987w, 18 code blocks, 15 H2 / 9 H3, mixed concept+model) | notes 3 + 4 + 5 | Far exceeds the 2,500-word AND 6-code-block caps (18 fences). Three distinct subsystems: (3) load pipeline + registry **model**, (4) runtime **hooks/helpers + add-a-capability** procedure-flavored concept, (5) gateway HTTP routes / SDK import paths / message-tool & catalog **reference schemas** (model BB). Three-way split keeps each ≤700w and ≤6 code blocks per note. |

All other pages (`adding-capabilities`, `building-plugins`, `bundles`, `cli-backend-plugins`, `admin-http-rpc`)
are below the word cap, single-BB, single task cluster → **1 note each** (no split).

## Summary Statistics & Building Block Distribution

- Source pages: **7** (16,746 measured words, ~41 code blocks). New `oc_*` notes: **10** (master index estimated
  11 at ~1.5 notes/page; the measured split — `architecture` ×2, `architecture-internals` ×3, the other 5 pages
  ×1 = 10 — is the faithful lock). New `term_dictionary` notes: **0** (expected — OpenClaw plugin vocabulary is
  documented as `oc_*` doc notes per master decision).
- **BB distribution:** **concept ×4** (notes 1, 2, 3, 4) · **model ×1** (note 5) · **procedure ×5** (notes 6, 7,
  8, 9, 10). Note 4 carries an add-a-capability checklist but is classified concept (its primary subject is the
  runtime-hook surface). One building_block per note is enforced. (Notes are numbered 1–10 in the table; the
  master's "11" est. reflects an extra split allowance — pl01 locks at **10 notes**.)
- Est. digest words ~**6,800** (avg ~620/note), well under the per-note 2,500 cap. The ~41 source code fences
  distribute across the procedure/model notes; each note kept ≤6 (reference schemas in note 5 reproduced
  selectively; large internals page's 18 fences spread across notes 3/4/5).
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** each note's Related Notes mapping meets the raised floors
  **≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (relevance-selected, no padding), PLUS additional
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> pi `pi_*`, band `band_*` coding-agent corpora). Repos are listed as ADDITIONAL beyond the floors. Relative paths
> are FROM `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`; sibling → `oc_Y.md`; other
> doc → `../<folder>/`; repo → `../../../areas/code_repos/`; snippet → `../../code_snippets/`; entry →
> `../../../0_entry_points/`. `entry_openclaw_docs` is **(planned — master W1 pre-step)**.

### oc_plugins_architecture_capability_model (8t · 10s · 10d) — concept

**Terms** (8, existing):
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model/media provider backend; relevance: every capability row in the public model registers via a provider-shaped `api.register*Provider(...)` method.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the typed `OpenClawPluginApi` registration surface; relevance: the `api.registerProvider/registerSpeechProvider/registerImageGenerationProvider` capability methods ARE the SDK's public surface.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the `openclaw.plugin.json` discovery descriptor; relevance: a plugin's classified shape (plain/hybrid/hook-only/non-capability) is derived from manifest + actual registration behavior.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — protocol-level advertisement of what a participant can do; relevance: OpenClaw's capability-type table is exactly a host-side capability-negotiation model for plugins.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool/function invocation; relevance: registering tools/providers is how a plugin exposes callable capabilities to the agent loop.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol capability/tool advertisement; relevance: the native capability model is the in-process analogue of MCP's external capability advertisement.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the "Text inference" capability (`api.registerProvider`) fronts an LLM backend (`openai`, `anthropic`).
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — image/media generative model; relevance: the "Image generation" capability (`api.registerImageGenerationProvider`, e.g. `fal`, `minimax`) backs onto diffusion models.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_ownership_contracts](oc_plugins_architecture_ownership_contracts.md) (planned, this series) — capability ownership/contracts; relevance: directly continues this concept (what a plugin IS → how capabilities are governed).
- [oc_plugins_architecture_internals_load_registry](oc_plugins_architecture_internals_load_registry.md) (planned, this series) — load pipeline + registry; relevance: shows how a registered capability becomes a live registry record.
- [oc_plugins_building_plugins](oc_plugins_building_plugins.md) (planned, this series) — first-plugin tutorial; relevance: the practical entry point for registering a capability.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin/extension capability framework; relevance: the closest sibling-ecosystem capability/extension model for comparison.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin types and registration surfaces; relevance: parallel "what kinds of plugin surfaces exist" taxonomy.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — Pi extension/plugin model overview; relevance: another coding-agent host's capability/extension registration model.
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model; relevance: the upstream Claude Code plugin concepts OpenClaw can map as bundles.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes model-provider plugin; relevance: provider-capability registration in a sibling system.
- [hermes_integrations_overview](../hermes_agent/hermes_integrations_overview.md) — Hermes integrations/capability surface map; relevance: how capabilities compose across an agent host.
- [band_sdk_reference_adapters](../band/band_sdk_reference_adapters.md) — Band SDK adapter/capability reference; relevance: adapter-as-capability registration analogue.

**Repos** (additional): [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/capability framework; [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — text-inference + embedding capability implementations; [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core registry host.

**Snippets** (10, existing):
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — OpenClaw plugin lifecycle; relevance: shows the register-against-capability lifecycle the model describes.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `definePluginEntry` SDK entries; relevance: the SDK entry shape that registers capabilities.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: how a package declares its plugin/capability surface.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: the hybrid-capability `openai` plugin (text/speech/image) named in the model table.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider plugin; relevance: the `anthropic` text-inference capability example.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregator; relevance: a multi-model provider-capability registration.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs speech provider; relevance: the speech capability (`registerSpeechProvider`) implementation.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: how capability-registered providers populate the catalog.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — Hermes plugin SDK architecture; relevance: cross-ecosystem comparison of the capability/SDK layering.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — Hermes provider registry; relevance: analogous provider-capability registry.

### oc_plugins_architecture_ownership_contracts (8t · 10s · 10d) — concept

**Terms** (8, existing):
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-backed plugin; relevance: ownership model says one company/vendor plugin owns all its provider surfaces.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `OpenClawPluginApi` contract surface; relevance: "what belongs in a contract" is defined relative to `OpenClawPluginApi`/`api.runtime`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: contracts govern which registered tools/providers a plugin owns.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — hook/event-based control flow; relevance: contract enforcement and the execution model run through registration hooks and the agent loop.
- [Multimodal](../../term_dictionary/term_multimodal.md) — combined image/audio/video understanding; relevance: the worked video-understanding capability is the canonical multi-capability ownership example.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: the execution model section states native plugins are NOT sandboxed (in-process trust boundary) — the export boundary discussion.
- [Access Control](../../term_dictionary/term_access_control.md) — who may do what; relevance: capability ownership = which plugin may own a capability slot (`plugins.allow` trusts plugin ids).
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — capability advertisement/ownership; relevance: the layering model (core contract vs vendor vs channel) is a capability-ownership negotiation.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_capability_model](oc_plugins_architecture_capability_model.md) (planned, this series) — capability model; relevance: its prerequisite (what a plugin IS).
- [oc_plugins_architecture_internals_runtime_hooks](oc_plugins_architecture_internals_runtime_hooks.md) (planned, this series) — runtime hooks; relevance: where contract enforcement is implemented at runtime.
- [oc_plugins_adding_capabilities](oc_plugins_adding_capabilities.md) (planned, this series) — adding a capability; relevance: the contributor workflow that creates new core contracts.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin ownership model; relevance: sibling-ecosystem ownership/boundary framing.
- [hermes_integrations_overview](../hermes_agent/hermes_integrations_overview.md) — Hermes integration/ownership surface; relevance: how vendor surfaces are owned across an agent host.
- [pi_extensions_api_methods](../pi/pi_extensions_api_methods.md) — Pi extension API contract methods; relevance: the typed-contract surface analogue for ownership.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — Claude Code enforcement/policy controls; relevance: contract-enforcement / policy-boundary analogue.
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin ownership model; relevance: upstream plugin ownership concepts.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes provider-plugin ownership; relevance: vendor-owns-its-surface analogue.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — Band coding-agent deployment/ownership; relevance: cross-system ownership-boundary perspective.

**Repos** (additional): [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/capability framework; [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — enforces contracts in core; [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — vendor-owned provider implementations.

**Snippets** (10, existing):
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: where duplicate-ownership/registration enforcement happens.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: the `@openclaw/<id>` package-ownership rule the doc states.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI multi-capability provider; relevance: the canonical multi-capability "company plugin owns all surfaces" example.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs single-capability speech; relevance: the single-capability vendor ownership example (`elevenlabs` owns speech).
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call feature plugin manager; relevance: the `voice-call` feature plugin that consumes shared capabilities (not vendor code).
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call media stream; relevance: feature plugin consuming shared speech/transcription contracts.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: core-owned contract surface that vendor plugins populate.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — Hermes provider registry; relevance: analogous duplicate-id ownership enforcement.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — Hermes Anthropic provider; relevance: vendor-owns-its-surface analogue.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — Hermes tool registry; relevance: contract-registry ownership model for tools.

### oc_plugins_architecture_internals_load_registry (8t · 10s · 10d) — concept

**Terms** (8, existing):
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json` descriptor; relevance: the manifest is the control-plane source of truth read first in the load pipeline.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — registration API; relevance: `register(api)` (legacy alias `activate`) is the data-plane step that collects registrations.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-backed plugin; relevance: provider/CLI-backend ownership is one of the registry records the snapshot tracks.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — central tool/registration store; relevance: the plugin registry IS the central registry collecting tools/hooks/channels/providers/routes.
- [TypeScript](../../term_dictionary/term_typescript.md) — TS language/toolchain; relevance: third-party local-source TS loads via the emergency Jiti fallback loader.
- [Node.js](../../term_dictionary/term_node_js.md) — Node runtime; relevance: built bundled modules load through native Node `require`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation/safety boundary; relevance: path-safety gates (escape-root, world-writable, ownership) run BEFORE runtime execution.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — capability discovery/planning; relevance: activation planning narrows which plugins are relevant to a command/provider/channel before loading.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_internals_runtime_hooks](oc_plugins_architecture_internals_runtime_hooks.md) (planned, this series) — runtime hooks; relevance: what runs after `register(api)` collects registrations.
- [oc_plugins_architecture_internals_gateway_sdk_reference](oc_plugins_architecture_internals_gateway_sdk_reference.md) (planned, this series) — gateway/SDK reference; relevance: the registry surfaces consumed downstream.
- [oc_plugins_bundles](oc_plugins_bundles.md) (planned, this series) — bundles; relevance: detection precedence (native-first vs bundle) is part of this load pipeline.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin load/registry system; relevance: analogous plugin discovery → register → registry lifecycle.
- [hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin enable/disable management; relevance: analogous enablement/validation stage.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — Pi extension load model; relevance: another agent host's discovery/registration model.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — Claude Code plugin install/discovery; relevance: discovery-roots / install-index analogue.
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model; relevance: upstream discovery/enablement concepts.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin surfaces; relevance: what the registry exposes to core.
- [band_adapter_setup](../band/band_adapter_setup.md) — Band adapter discovery/setup; relevance: adapter discovery/registration analogue.

**Repos** (additional): [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — load pipeline + registry host; [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled extension packages discovered from `extensions/*`; [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — install/discovery surfaces.

**Snippets** (10, existing):
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — gateway plugin runtime load; relevance: the exact startup load → register → expose-registry path.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: the discover → enable → load → register lifecycle.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK plugin entries; relevance: the `register`/`activate` entry resolved by the loader.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: how the installed index / package metadata feeds discovery.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest planner; relevance: the `PluginMetadataSnapshot`/`PluginLookUpTable` planning the doc describes.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: registry-record normalization for channels.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — Hermes plugin namespace init; relevance: analogous plugin discovery/init.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — Hermes plugin discovery; relevance: analogous candidate-root discovery.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — Hermes provider registry; relevance: analogous central registration store.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — Hermes ACP registry manifest; relevance: manifest-driven registry construction analogue.

### oc_plugins_architecture_internals_runtime_hooks (8t · 11s · 10d) — concept

**Terms** (8, existing):
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — hook/callback control flow; relevance: the 40+ ordered provider runtime hooks + conversation-binding callbacks form a hook chain.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-backed plugin; relevance: the hook order/usage table is the provider-plugin runtime extension surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `normalizeToolSchemas`/`inspectToolSchemas` hooks shape the tools the model can call.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — image generative model; relevance: the `api.runtime.imageGeneration.generate(...)` helper backs onto image-gen (diffusion) providers.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `api.runtime` helper surface; relevance: runtime helpers (`api.runtime.tts/mediaUnderstanding/subagent/webSearch/imageGeneration`) are the SDK runtime accessors.
- [LLM](../../term_dictionary/term_llm.md) — language model; relevance: model-resolution hooks (`resolveDynamicModel`, `normalizeResolvedModel`) govern which LLM the runner uses.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript compaction; relevance: conversation-binding callbacks + context-engine compaction intersect the runtime helper surface.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS synthesis; relevance: `api.runtime.tts.textToSpeech/textToSpeechTelephony/listVoices` is a primary runtime helper.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_internals_load_registry](oc_plugins_architecture_internals_load_registry.md) (planned, this series) — load pipeline; relevance: provides the registry these hooks fire against.
- [oc_plugins_adding_capabilities](oc_plugins_adding_capabilities.md) (planned, this series) — adding a capability; relevance: the public version of the in-doc add-a-capability checklist.
- [oc_plugins_architecture_ownership_contracts](oc_plugins_architecture_ownership_contracts.md) (planned, this series) — contracts; relevance: the hooks are where contract behavior is enforced at runtime.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes provider runtime hooks; relevance: the closest analogue to OpenClaw's provider runtime-hook table.
- [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes plugin hooks; relevance: sibling-ecosystem hook surface.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — Pi custom streaming/provider hooks; relevance: stream-wrapping / model-resolution hook analogue.
- [cc_hook_handler_types](../claude_code/cc_hook_handler_types.md) — Claude Code hook handler types; relevance: hook-type taxonomy for an agent host.
- [cc_hooks_advanced_types](../claude_code/cc_hooks_advanced_types.md) — Claude Code advanced hooks; relevance: ordered-hook lifecycle analogue.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS providers; relevance: the TTS runtime-helper / speech-provider parallel.
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — Hermes image generation; relevance: image-generation runtime-helper parallel.


**Snippets** (11, existing):
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: implements the `api.runtime.tts` / `registerSpeechProvider` helper path.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: another TTS runtime helper backend.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: the `api.runtime.stt`/mediaUnderstanding transcription helper.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider hooks; relevance: implements provider runtime hooks (catalog, auth, model resolution).
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider hooks; relevance: provider runtime-hook implementation.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: dynamic-model resolution hook (`resolveDynamicModel`) example.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — subagent registry announce; relevance: the `api.runtime.subagent.run` helper surface.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: the trusted-caller / allowModelOverride policy on `api.runtime.subagent`.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — Hermes TTS routing; relevance: analogous TTS runtime-helper routing.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — Hermes image gen; relevance: analogous `imageGeneration.generate` runtime helper.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — Hermes transcription; relevance: analogous media-understanding transcribe helper.

### oc_plugins_architecture_internals_gateway_sdk_reference (8t · 11s · 10d) — model

**Terms** (8, existing):
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON-RPC protocol; relevance: gateway HTTP routes + RPC handlers dispatch JSON-RPC-shaped method calls.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: `api.registerHttpRoute` + gateway RPC handlers are the plugin RPC surface.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema language; relevance: message-tool schema contributions (`describeMessageTool`) and `extractStructuredWithModel` `jsonSchema` are JSON-Schema-typed.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — SDK import subpaths; relevance: the `openclaw/plugin-sdk/<subpath>` import-path table is the core of this reference note.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model catalog; relevance: `registerModelCatalogProvider` + `catalog.run/catalog.order` provider-catalog tables.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — context assembly/compaction; relevance: context-engine plugins (`registerContextEngine`, `assemble`/`compact`/`ingest`) are a reference subsystem.
- [Message Queue](../../term_dictionary/term_message_queue.md) — message routing/dispatch; relevance: channel target resolution + the shared `message` tool dispatch surface.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — gateway routing layer; relevance: gateway HTTP routes (`auth: gateway|plugin`, `match: exact|prefix`) are the plugin route surface on the gateway.

**Docs** (10; existing ≥5):
- [oc_plugins_admin_http_rpc](oc_plugins_admin_http_rpc.md) (planned, this series) — admin HTTP-RPC; relevance: the public gateway HTTP-RPC surface that this internal route table backs.
- [oc_plugins_architecture_internals_load_registry](oc_plugins_architecture_internals_load_registry.md) (planned, this series) — registry; relevance: the registry from which these reference surfaces are exposed.
- [oc_plugins_architecture_internals_runtime_hooks](oc_plugins_architecture_internals_runtime_hooks.md) (planned, this series) — runtime hooks; relevance: the runtime helpers reachable through these SDK subpaths.
- [hermes_mcp_config_reference](../hermes_agent/hermes_mcp_config_reference.md) — Hermes MCP config reference; relevance: analogous schema/config reference table.
- [hermes_programmatic_integration](../hermes_agent/hermes_programmatic_integration.md) — Hermes programmatic/HTTP integration; relevance: gateway HTTP-route / RPC integration analogue.
- [pi_extensions_api_methods](../pi/pi_extensions_api_methods.md) — Pi extension API methods; relevance: the typed SDK method reference analogue.
- [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — Claude Code tool catalog; relevance: tool/schema reference-table analogue.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — Claude Code settings reference; relevance: config-backed-directories / reference-schema analogue.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — Band A2A gateway; relevance: gateway HTTP-route/RPC reference analogue.
- [band_rest_api_introduction](../band/band_rest_api_introduction.md) — Band REST API; relevance: HTTP route/method reference analogue.

**Repos** (additional): [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway HTTP routes host; [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — SDK subpaths + context-engine plugins; [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — channel catalog / target resolution; [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider catalogs.

**Snippets** (11, existing):
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — gateway HTTP plugin routing; relevance: the `api.registerHttpRoute` gateway-route dispatch this note tables.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway HTTP/WS listener; relevance: the gateway listener the plugin routes attach to.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: the gateway method handlers plugin RPC dispatches to.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: the shared `message` tool dispatch surface.
- [snippet_openclaw_context_engine_registry_factories](../../code_snippets/snippet_openclaw_context_engine_registry_factories.md) — context-engine registry factories; relevance: `registerContextEngine(id, factory)` the doc shows.
- [snippet_openclaw_context_engine_delegate](../../code_snippets/snippet_openclaw_context_engine_delegate.md) — context-engine delegate; relevance: `delegateCompactionToRuntime` for engines not owning compaction.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model-catalog planner; relevance: provider-catalog `catalog.order` merge reference.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: `registerModelCatalogProvider` row shape.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — channel conversation resolution; relevance: channel target/session route resolution.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway channel WS; relevance: gateway channel transport reference.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI route registration; relevance: the two-phase root-command CLI registrar reference.

### oc_plugins_building_plugins (8t · 10s · 10d) — procedure

**Terms** (8, existing):
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: the smallest working manifest (id, `contracts.tools`, `activation.onStartup`, `configSchema`) is the tutorial core.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `definePluginEntry`/`api.register*`; relevance: the tutorial registers via `definePluginEntry` + `api.registerTool`.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/channel/CLI plugin shapes; relevance: "Choose the plugin shape" routes to channel/provider/CLI-backend/tool plugins.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool registration store; relevance: "Registering tools" (`api.registerTool` + manifest `contracts.tools` + `tools.allow`).
- [TypeScript](../../term_dictionary/term_typescript.md) — TS/ESM; relevance: requirements mandate TypeScript ESM modules + Node 22.19.
- [npm](../../term_dictionary/term_npm.md) — npm/pnpm package manager; relevance: `pnpm install`, `clawhub:`/npm install, package metadata.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: registered tools are typed functions the model can call after policy checks.
- [Node.js](../../term_dictionary/term_node_js.md) — Node runtime; relevance: Node 22.19+ requirement and the runtime that loads built JS entries.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_capability_model](oc_plugins_architecture_capability_model.md) (planned, this series) — capability model; relevance: the conceptual model the tutorial implements.
- [oc_plugins_adding_capabilities](oc_plugins_adding_capabilities.md) (planned, this series) — adding a capability; relevance: the contributor counterpart to the external-plugin tutorial.
- [oc_plugins_cli_backend_plugins](oc_plugins_cli_backend_plugins.md) (planned, this series) — CLI backend plugins; relevance: one of the "choose the shape" branches.
- [oc_plugins_bundles](oc_plugins_bundles.md) (planned, this series) — bundles; relevance: the non-native alternative to building a plugin.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes build-plugin tutorial; relevance: the closest sibling first-plugin tutorial.
- [cc_plugin_quickstart](../claude_code/cc_plugin_quickstart.md) — Claude Code plugin quickstart; relevance: upstream first-plugin quickstart analogue.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — Pi extension overview; relevance: another agent host's plugin-authoring entry point.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin types; relevance: choosing the plugin shape analogue.
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — Claude Code plugin CLI; relevance: `plugins inspect`/install command analogue.
- [band_adapter_setup](../band/band_adapter_setup.md) — Band adapter setup; relevance: package/manifest setup analogue.

**Repos** (additional): [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-plugin `extensions/*` packages; [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core that loads the plugin; [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — analogous build/register flow.

**Snippets** (10, existing):
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `definePluginEntry` entries; relevance: the exact entry primitive the tutorial uses.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package.json `openclaw` contract; relevance: the package metadata block in the quickstart.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: how the registered tool is loaded at startup.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — manifest format; relevance: the manifest schema fields the tutorial declares.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — Hermes plugin SDK; relevance: analogous SDK entry/architecture for a first plugin.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — Hermes web plugin example; relevance: a concrete tool-registering plugin analogue.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — Hermes tool registry; relevance: `registerTool`-equivalent registration.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — Hermes plugin install command; relevance: the `plugins install` step analogue.
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — Hermes config schema; relevance: `configSchema` validation analogue.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — Hermes config validate; relevance: the pre-submission `pnpm check` validation analogue.

### oc_plugins_adding_capabilities (8t · 10s · 10d) — procedure

**Terms** (8, existing):
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-backed plugin; relevance: the provider + harness seams are where new capability implementations register.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `OpenClawPluginApi`/`api.runtime`; relevance: step 2 extends `OpenClawPluginApi`/`api.runtime` with the new typed capability surface.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — image generative model; relevance: the worked image-generation example (`registerImageGenerationProvider`, `runtime.imageGeneration.generate`).
- [Embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: the `embeddingProviders` capability section (broader than memory).
- [Vector Database](../../term_dictionary/term_vector_database.md) — vector store; relevance: embeddings feed search/retrieval/memory vector stores.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: new capabilities are exposed to consumers through typed runtime helpers/tools.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — manifest descriptors; relevance: the file checklist touches `src/plugins/*` + manifest contract surfaces.
- [Multimodal](../../term_dictionary/term_multimodal.md) — image/audio/video understanding; relevance: media-understanding is the shared multi-modal capability the guide generalizes from.

**Docs** (10; existing ≥5):
- [oc_plugins_building_plugins](oc_plugins_building_plugins.md) (planned, this series) — building plugins; relevance: the external-plugin tutorial this contributor guide complements.
- [oc_plugins_architecture_internals_runtime_hooks](oc_plugins_architecture_internals_runtime_hooks.md) (planned, this series) — runtime hooks; relevance: the internal add-a-capability checklist + template live there.
- [oc_plugins_architecture_ownership_contracts](oc_plugins_architecture_ownership_contracts.md) (planned, this series) — contracts; relevance: "define the contract first" is the guide's core rule.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes add-inference-provider guide; relevance: the closest analogous "add a provider capability" contributor guide.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — Pi custom provider registration; relevance: add-a-provider-capability analogue.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes model-provider plugin; relevance: registering a vendor implementation against a contract.
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugins overview; relevance: capability/extension authoring concepts.
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — Hermes image generation; relevance: the worked image-generation capability analogue.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — Hermes memory/embedding provider catalog; relevance: the embedding-providers capability analogue.
- [pi_extensions_api_methods](../pi/pi_extensions_api_methods.md) — Pi extension API methods; relevance: extending the typed plugin API surface.

**Repos** (additional): [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — capability framework; [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider + embedding seams; [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core contract host.

**Snippets** (10, existing):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: a vendor registering against a core capability contract.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: another vendor implementation against the text-inference contract.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: the worked image-generation capability dispatch analogue.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: the "core contract + vendor register + consumer" capability pattern.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image gen tool; relevance: consumer side of the image-generation capability.
- [snippet_hermes_agent_plugins_memory_discovery](../../code_snippets/snippet_hermes_agent_plugins_memory_discovery.md) — memory/embedding discovery; relevance: the embedding-providers capability seam.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregator; relevance: wiring multiple vendors behind one capability contract.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where new-capability registrations are collected.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entries; relevance: the typed registration surface a new capability extends.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video gen tool; relevance: feature/channel consumer of a media capability.

### oc_plugins_cli_backend_plugins (8t · 10s · 10d) — procedure

**Terms** (8, existing):
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — local AI CLI coding agents; relevance: a CLI backend wraps a local coding-agent CLI as a text-inference backend (`acme-cli/model`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-shaped capability; relevance: `api.registerCliBackend(...)` is a provider-family capability registration.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the MCP tool bridge (`bundleMcp`/`bundleMcpMode`) exposes OpenClaw tools to the CLI.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript compaction; relevance: `ownsNativeCompaction` opts the backend out of OpenClaw's safeguard summarizer.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: the MCP bridge + `nativeToolMode`/`sideQuestionToolMode` govern the CLI's tool layer.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Claude Code CLI; relevance: `claude-cli` is the named backend that declares `ownsNativeCompaction` (compacts internally).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: the manifest declares `cliBackends` + `setup.cliBackends` ownership before runtime loads.
- [LLM](../../term_dictionary/term_llm.md) — language model backend; relevance: a CLI backend is a text-inference (LLM) backend in the model fallback chain.

**Docs** (10; existing ≥5):
- [oc_plugins_building_plugins](oc_plugins_building_plugins.md) (planned, this series) — building plugins; relevance: package + manifest basics this CLI-backend guide builds on.
- [oc_plugins_architecture_capability_model](oc_plugins_architecture_capability_model.md) (planned, this series) — capability model; relevance: "CLI inference backend" is a row in the capability table.
- [oc_plugins_adding_capabilities](oc_plugins_adding_capabilities.md) (planned, this series) — adding capabilities; relevance: provider/harness seam decision (CLI backend vs provider vs agent harness).
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Hermes Codex runtime setup; relevance: wiring a coding-agent CLI/runtime as a backend analogue.
- [band_adapter_codex](../band/band_adapter_codex.md) — Band Codex adapter; relevance: adapting a coding-agent CLI as a backend analogue.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — Band coding-agents deployment; relevance: deploying CLI coding agents as backends.
- [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — Claude Code MCP transports; relevance: the MCP tool-bridge transport (`claude-config-file`/`codex-config-overrides`) analogue.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud providers + fallback; relevance: model fallback/provider-chain analogue (`fallbacks: ["acme-cli/large"]`).
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — Hermes fallback providers; relevance: the model fallback runner a CLI backend plugs into.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth; relevance: CLI-owned local login state / auth-profile preference (`defaultAuthProfileId`).


**Snippets** (10, existing):
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — openshell CLI backend; relevance: an OpenClaw CLI/shell backend registration analogue.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider plugin; relevance: provider-family registration the CLI backend mirrors.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — gateway MCP loopback; relevance: the loopback MCP tool bridge the CLI backend opts into.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: the `ownsNativeCompaction` defer/handoff path.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compaction reset; relevance: the compaction lifecycle a backend can own.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Hermes Codex provider; relevance: a coding-agent CLI/provider backend analogue.
- [snippet_hermes_agent_cli_codex_switch](../../code_snippets/snippet_hermes_agent_cli_codex_switch.md) — Hermes Codex switch; relevance: switching/routing to a CLI coding-agent backend.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — Hermes CLI config loading; relevance: user-config merge over backend defaults (`agents.defaults.cliBackends.<id>`).
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — CLI auth resolve provider; relevance: `defaultAuthProfileId`/`authEpochMode` auth-profile resolution.
- [snippet_hermes_agent_core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — runtime switch client; relevance: routing a turn to a CLI backend client.

### oc_plugins_bundles (8t · 10s · 10d) — procedure

**Terms** (8, existing):
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — manifest/markers; relevance: bundle detection reads `.codex-plugin/`/`.claude-plugin/`/`.cursor-plugin/plugin.json` markers + native `openclaw.plugin.json` precedence.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI ecosystems; relevance: bundles adopt Codex/Claude/Cursor third-party plugin ecosystems.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation/trust boundary; relevance: bundles have a narrower trust boundary — no in-process runtime load; boundary-checked skill/hook paths.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — native plugin contrast; relevance: the doc contrasts content-pack bundles with native SDK-registered plugins.
- [npm](../../term_dictionary/term_npm.md) — npm/pnpm dependencies; relevance: runtime-dependency cleanup (`openclaw doctor --fix`, no startup `npm install`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — native plugin shape; relevance: bundles map to native features but cannot register arbitrary provider capabilities.
- [Access Control](../../term_dictionary/term_access_control.md) — allow/deny gates; relevance: bundle security (`tools.deny: ["bundle-mcp"]`, boundary checks, enabled-gate).
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: bundle MCP config is merged into embedded OpenClaw `mcpServers` and exposed as `serverName__toolName`.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_internals_load_registry](oc_plugins_architecture_internals_load_registry.md) (planned, this series) — load pipeline; relevance: detection precedence (native-first) lives in the load pipeline.
- [oc_plugins_building_plugins](oc_plugins_building_plugins.md) (planned, this series) — building plugins; relevance: the native-plugin alternative to a bundle.
- [oc_plugins_architecture_capability_model](oc_plugins_architecture_capability_model.md) (planned, this series) — capability model; relevance: why bundles can't register arbitrary capabilities (content-pack limit).
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — Claude Code marketplaces/install; relevance: the Claude marketplace bundle source (`<plugin>@<marketplace>`).
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugins overview; relevance: the Claude bundle format OpenClaw detects (`.claude-plugin/`, `settings.json`, `.mcp.json`, `.lsp.json`).
- [band_adapter_codex](../band/band_adapter_codex.md) — Band Codex adapter; relevance: the Codex bundle format analogue (`.codex-plugin/`, `HOOK.md`+`handler.ts`).
- [hermes_use_mcp_guide](../hermes_agent/hermes_use_mcp_guide.md) — Hermes MCP usage; relevance: how mapped bundle MCP tools are consumed.
- [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — Claude Code MCP quickstart; relevance: the MCP server config (stdio/HTTP) bundles contribute.
- [hermes_mcp_config_reference](../hermes_agent/hermes_mcp_config_reference.md) — Hermes MCP config reference; relevance: the stdio/streamable-http transport shape the bundle MCP config uses.
- [band_adapter_setup](../band/band_adapter_setup.md) — Band adapter setup; relevance: installing/mapping external-ecosystem content analogue.

**Repos** (additional): [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundle mapping/extension code; [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — bundle detection + native-first precedence; [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — bundle security posture / boundary checks.

**Snippets** (10, existing):
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skills manifest format; relevance: bundle skill-root mapping into OpenClaw skills.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: native-vs-bundle detection (package.json `openclaw.extensions` = native).
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP HTTP loopback; relevance: how mapped bundle MCP servers (stdio/HTTP) are launched/connected.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: where bundle detection/enablement sits in the lifecycle.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — Hermes skills install; relevance: installing skill-content packs analogue.
- [snippet_hermes_agent_skills_canonical_loading_runtime](../../code_snippets/snippet_hermes_agent_skills_canonical_loading_runtime.md) — Hermes skill loading runtime; relevance: loading bundle skill roots through the skill loader.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — Hermes plugin install command; relevance: `openclaw plugins install ./bundle` analogue.
- [snippet_hermes_agent_cli_plugins_cmd_remove](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_remove.md) — Hermes plugin remove command; relevance: bundle cleanup / `doctor --fix` analogue.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — ACP registry manifest; relevance: manifest-marker detection analogue.

### oc_plugins_admin_http_rpc (8t · 10s · 10d) — procedure

**Terms** (8, existing):
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON-RPC protocol; relevance: `POST /api/v1/admin/rpc` dispatches Gateway RPC method calls in JSON-RPC shape (`{method, params}` → `{ok, payload}`).
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: admin HTTP RPC is an HTTP request/response surface over the Gateway control-plane RPC methods.
- [Authentication](../../term_dictionary/term_authentication.md) — auth verification; relevance: the route uses Gateway HTTP auth (token/password/trusted-proxy/none modes).
- [WebSocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: the WebSocket-comparison section contrasts the preferred WS RPC client with this HTTP surface.
- [Access Control](../../term_dictionary/term_access_control.md) — scopes/allowlist; relevance: the security model + allowed-method allowlist + `x-openclaw-scopes` handling are access-control rules.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — gateway routing; relevance: the plugin registers a route on the Gateway HTTP listener.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: `Authorization: Bearer <gateway-token>` shared-secret auth.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — trusted ingress/proxy; relevance: `trusted-proxy` auth mode + "keep on loopback/tailnet/private trusted ingress" deployment guidance.

**Docs** (10; existing ≥5):
- [oc_plugins_architecture_internals_gateway_sdk_reference](oc_plugins_architecture_internals_gateway_sdk_reference.md) (planned, this series) — gateway/SDK reference; relevance: the internal gateway HTTP-route + RPC-method table this public surface exposes.
- [oc_plugins_architecture_internals_load_registry](oc_plugins_architecture_internals_load_registry.md) (planned, this series) — load/registry; relevance: the bundled plugin is enabled/registered through this load pipeline (route registered on plugin startup).
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes remote/dashboard auth; relevance: gateway remote-auth / trusted-ingress analogue.
- [hermes_programmatic_integration](../hermes_agent/hermes_programmatic_integration.md) — Hermes programmatic HTTP integration; relevance: HTTP control-plane RPC integration analogue.
- [cc_remote_control](../claude_code/cc_remote_control.md) — Claude Code remote control; relevance: remote control-plane access + trust-boundary analogue.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication; relevance: bearer/token auth-mode analogue.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — Claude Code web security/limits; relevance: HTTP surface security posture + body-size limit analogue.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — Band A2A gateway; relevance: gateway control-plane HTTP/RPC analogue.
- [band_rest_api_introduction](../band/band_rest_api_introduction.md) — Band REST API; relevance: HTTP request/response method-allowlist analogue.
- [band_websocket_overview](../band/band_websocket_overview.md) — Band WebSocket overview; relevance: the WS-vs-HTTP control-plane comparison analogue.

**Repos** (additional): [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway hosting the admin route; [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/scope/security-model enforcement; [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core gateway method handlers.

**Snippets** (10, existing):
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — gateway HTTP plugin routing; relevance: how the `admin-http-rpc` plugin route is registered/dispatched.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: the allowlisted Gateway methods (`health`, `config.*`, `channels.*`, `cron.*`) dispatched.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway HTTP/WS listener; relevance: the shared listener serving both the WS RPC and this HTTP route.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — gateway chat send handler; relevance: a gateway method handler reachable via the RPC dispatch.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway channel WS; relevance: the WebSocket RPC path the doc compares against.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: another gateway RPC/server surface with its own auth.
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — Hermes API server routes; relevance: analogous HTTP API route registration.
- [snippet_hermes_agent_gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — Hermes API auth middleware; relevance: the HTTP-auth gate before method dispatch.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — Hermes JSON-RPC server; relevance: the JSON-RPC request/response shape analogue.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — Hermes webhook route; relevance: plugin-managed HTTP route + auth verification analogue.

## Undigested Terms Plan

> Per master: OpenClaw plugin vocabulary is digested **as `oc_*` doc notes by this sub-plan**, NOT as new
> `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms. Expected
> **0 new term captures**. Augment re-runs the Step 2d new-term scan.

| Term (vocabulary appearing in the 7 pages) | Disposition |
|---|---|
| capability / capability model / capability type | → `oc_plugins_architecture_capability_model` (note 1) — concept, not a term note |
| plugin shape (plain/hybrid/hook-only/non-capability) | → note 1 (documented inline as a model concept) |
| capability ownership / capability layering | → `oc_plugins_architecture_ownership_contracts` (note 2) |
| contract / contract enforcement / export boundary | → note 2 |
| load pipeline / registry model / manifest-first | → `oc_plugins_architecture_internals_load_registry` (note 3) |
| runtime hook / conversation-binding callback / `before_model_resolve` | → `oc_plugins_architecture_internals_runtime_hooks` (note 4) |
| package pack / context-engine plugin / channel catalog | → `oc_plugins_architecture_internals_gateway_sdk_reference` (note 5) |
| CLI backend / `registerCliBackend` / `ownsNativeCompaction` | → `oc_plugins_cli_backend_plugins` (note 8) |
| bundle / bundle format / detection precedence | → `oc_plugins_bundles` (note 9) |
| admin HTTP-RPC / allowed methods | → `oc_plugins_admin_http_rpc` (note 10) |
| plugin / extension / plugin SDK | LINK existing `term_plugin_sdk` (+ `term_plugin_manifest`, `term_provider_plugin`); do NOT recreate |
| MCP / function calling / RPC / JSON-RPC / JSON Schema | LINK existing `term_mcp` / `term_function_calling` / `term_rpc` / `term_json_rpc` / `term_json_schema` |
| LLM / Claude / Claude Code / Codex / Pi / coding agent | LINK existing `term_llm` / `term_claude` / `term_claude_code` / `term_pi_agent` / `term_autonomous_coding_agents` (verify `term_autonomous_coding_agents` at augment) |
| image / music / video / speech / embedding generation | LINK existing `term_diffusion_model` / `term_text_to_speech` / `term_speech_to_text` / `term_embedding` / `term_multimodal` / `term_vector_database` |
| OAuth / token / authentication / WebSocket / access control | LINK existing `term_oauth` / `term_oauth_token` / `term_authentication` / `term_websocket` / `term_access_control` |
| compaction / context engineering / message queue | LINK existing `term_compaction` / `term_context_engineering` / `term_message_queue` |

**New-term candidates (provisional, near-0 expected):** none promoted at plan stage. If augment's Step 2d finds a
genuinely cross-cutting, vault-reusable term with no doc-page home AND no existing note (candidate watch:
`plugin capability` as a generic software-design concept distinct from OpenClaw's model; `lifecycle hook` as a
generic pattern), it would be captured via `/tessellum-capture-term-note` and added to `acronym_glossary_a.md`
(agentic/dev-tooling glossary). Current judgment: both are sufficiently covered by the `oc_*` concept notes +
existing `term_event_driven_architecture` / `term_plugin_sdk`, so **0 new terms** is the expected outcome.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. If augment promotes a new term, the
master's multi-source-research term-authoring mandate applies (research internal + external sources, full
frontmatter, acronym-glossary entry, ≥1 inbound link), inherited verbatim from `plan_digest_openclaw_docs_master.md`.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (10 notes, P3). All gates must PASS before commit.

| Gate | Name | Check |
|------|------|-------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` PASS (YAML field order/tags, `## Overview` + `## Related Notes`, bold `**Source**`/`**Last Updated**`/`**Status**` footer). |
| G2 | Grounding | Each note diffs faithfully against its `inbox/openclaw_docs/plugins/<page>.md` source section(s); no hallucinated capability types/routes/hooks. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, ONE building_block per note; every mapped H2/H3 covered. |
| G6 | Broken-link | 0 broken links (`/tessellum-fix-broken-links` after incremental reindex). |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` + repo/term inlinks. |
| G8 | In-degree ≥1 | `note_links` confirms in-degree ≥1 per new note after reindex. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_architecture_capability_model oc_plugins_architecture_ownership_contracts oc_plugins_architecture_internals_load_registry oc_plugins_architecture_internals_runtime_hooks oc_plugins_architecture_internals_gateway_sdk_reference oc_plugins_building_plugins oc_plugins_adding_capabilities oc_plugins_cli_backend_plugins oc_plugins_bundles oc_plugins_admin_http_rpc"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1: format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density: words (frontmatter stripped) + code-block count
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words words, $cb code blocks)"
  # at least one sibling oc_ Related link
  grep -qE "\($SIBLING_PREFIX[a-z0-9_]+\.md\)" "$f" || echo "$n NO sibling oc_ Related link"
done

# YAML frontmatter sweep across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6 after incremental reindex
bash scripts/update_notes_database.sh
# (then /tessellum-fix-ghost-references and /tessellum-fix-broken-links per master)
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_architecture_capability_model | concept | 650 | ≤2 | ✅ |
| 2 | oc_plugins_architecture_ownership_contracts | concept | 650 | ≤2 | ✅ |
| 3 | oc_plugins_architecture_internals_load_registry | concept | 600 | ≤4 | ✅ |
| 4 | oc_plugins_architecture_internals_runtime_hooks | concept | 700 | ≤6 | ✅ |
| 5 | oc_plugins_architecture_internals_gateway_sdk_reference | model | 700 | ≤6 | ✅ |
| 6 | oc_plugins_building_plugins | procedure | 600 | ≤6 | ✅ |
| 7 | oc_plugins_adding_capabilities | procedure | 500 | ≤2 | ✅ |
| 8 | oc_plugins_cli_backend_plugins | procedure | 600 | ≤5 | ✅ |
| 9 | oc_plugins_bundles | procedure | 600 | ≤2 | ✅ |
| 10 | oc_plugins_admin_http_rpc | procedure | 600 | ≤6 | ✅ |

No note approaches the caps. The two code-heavy pages (`architecture-internals.md` 18 fences →
notes 3/4/5; `building-plugins.md` 8 fences → note 6) split / select so each note stays ≤6 code blocks
(schemas + manifests reproduced verbatim but selectively).

## Entry Point Decision (inherited from master)

Contributes its **10 rows** to `0_entry_points/entry_openclaw_docs.md` (CREATED as the master W1 pre-step before
any sub-plan executes; >30-note corpus ⇒ dedicated entry point required). Rows grouped under a **"Plugins —
Architecture & Building (pl01)"** cluster; each new note receives its entry-point back-link at finalization
(satisfies G7/G8). No new entry point created by pl01 itself.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + apply at execution; all sources DB-confirmed-existing):

- `entry_openclaw_docs.md` (planned, master W1) → **all 10 notes** (primary anti-island guarantee).
- `repo_openclaw` → notes 1, 3, 6, 8, 9, 10.
- `repo_openclaw_extensions` → notes 1, 2, 3, 4, 6, 7, 9.
- `repo_openclaw_extensions_llm_providers` → notes 1, 4, 5, 7, 8.
- `repo_openclaw_gateway` → notes 5, 10.
- `repo_openclaw_channels_messaging` → note 5.
- `repo_openclaw_security` → notes 9, 10.
- `repo_hermes_agent_plugins` → notes 3, 6 (analogous plugin load/registry + build flow).
- `term_plugin_sdk` → notes 1, 3, 6, 7.
- `term_plugin_manifest` → notes 1, 3, 6, 9.
- `term_provider_plugin` → notes 1, 2, 4, 7, 8.
- `term_mcp` → note 8 (MCP tool bridge).
- `term_json_rpc` → notes 5, 10.

## Pacing Rules (inherited from master)

One execution phase (10 notes). Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the
dispatch script. Re-read each source page before authoring; reproduce config/manifest/schema snippets verbatim
but selectively (≤6 code blocks/note). One BB per note. `git pull --rebase --autostash` first; commit+push per
wave with NO Claude co-author trailer; reindex incrementally and verify `note_links` + 0 broken links before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: Per-Note Related Notes Mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending (plan now `status: ready`) |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** xref-augment — built and LOCKED the `## Per-Note Related Notes Mapping` for all
10 planned notes at the RAISED floors (**≥8 terms · ≥10 code_snippets · ≥10 docs per note**), each link
relevance-selected against a fresh re-read of the 7 source pages under `inbox/openclaw_docs/plugins/` and
Cross-References` section. Updated the Summary Statistics cross-ref line and the G4 gate to the locked floors.

**Source re-read + measurement (Step 2a):** all 7 pages re-read in full / strategically (architecture-internals
sampled by section). Measured `wc -w` / code-fence counts EXACTLY match the plan's Source table —
adding-capabilities 747w/0cb, admin-http-rpc 1003w/7cb, architecture 3508w/1cb, architecture-internals
6987w/18cb, building-plugins 1440w/8cb, bundles 1542w/2cb, cli-backend-plugins 1519w/5cb (total 16,746w). No
density estimation failure; existing split decisions (architecture ×2, architecture-internals ×3) confirmed.

**Per-note locked counts (all floors MET):**

| Note | terms | snippets | docs | repos | floors met |
|---|---:|---:|---:|---:|---|
| oc_plugins_architecture_capability_model | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_architecture_ownership_contracts | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_architecture_internals_load_registry | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_architecture_internals_runtime_hooks | 8 | 11 | 10 | 4 | ✅ |
| oc_plugins_architecture_internals_gateway_sdk_reference | 8 | 11 | 10 | 4 | ✅ |
| oc_plugins_building_plugins | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_adding_capabilities | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_cli_backend_plugins | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_bundles | 8 | 10 | 10 | 3 | ✅ |
| oc_plugins_admin_http_rpc | 8 | 10 | 10 | 3 | ✅ |

  band `band_*`); the remainder are sibling `oc_*` marked **(planned, this series)** toward the 10-doc floor.

**New-term scan (Step 2d) — re-read findings:** the re-read surfaced two EXISTING, highly-relevant terms the
2, 3 — OpenClaw's capability-type table + activation planning IS a host-side capability-negotiation model) and
The plan's provisional new-term watch (`plugin capability`, `lifecycle hook`) is confirmed **NOT promoted**:
`plugin capability` is covered by `term_capability_negotiation` + the `oc_plugins_architecture_capability_model`
concept note; `lifecycle hook` is covered by `term_event_driven_architecture` + `term_plugin_sdk` +
`oc_plugins_architecture_internals_runtime_hooks`. **Net new `term_dictionary` captures: 0** (matches master
decision — OpenClaw plugin vocabulary is digested as `oc_*` doc notes, never inlined or recreated as terms).

**New-term candidate → best-fit glossary (if ever promoted):** none promoted. Had one been required, the best-fit
glossary is `acronym_glossary_a.md` (agentic / dev-tooling). Per master W5, capture would be via
`/tessellum-capture-term-note` + glossary entry. Not triggered.

**Dedup/collision audit (Step 10.5f, generalized to ALL planned notes):** none of the 10 planned `oc_*` slugs
exist in the DB (0 collisions). No existing `term_*` or `documentation/` note substantively duplicates any
planned plugin-system concept note — existing `term_plugin_sdk` / `term_plugin_manifest` / `term_provider_plugin`
/ `term_capability_negotiation` / `term_hermes_plugin` are LINKED (master decision), not recreated. `term_codex`
confirmed absent (plan correctly cites `term_autonomous_coding_agents` / `term_claude_code` instead).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_pl01.md` — reviewed against the 9 mandatory checkpoints.

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note has 8 terms / ≥10 snippets / ≥10 docs, each link carries a `relevance:` statement (not a bare link). |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (raised floors), G5 Ghost-reference (`/tessellum-fix-ghost-references`), G6 Broken-link (`/tessellum-fix-broken-links`), G7 Discoverability, G8 In-degree≥1. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 10 rows to `entry_openclaw_docs.md`, CREATED as master W1 pre-step (>30-note corpus ⇒ dedicated entry point); per-note back-link at finalization (G7/G8). |
| CP4 | Plan size (≤30 notes or split) | **PASS** | 10 notes — single execution phase, well under 30. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master `## Format Definition (Shared)`, derived from existing `claude_code/`(`cc_*`) + `pi/`(`pi_*`) doc corpora: `## Overview` + `## Related Notes` + bold `**Source**`/`**Last Updated**`/`**Status**` footer; forbidden-field list present. |
| CP6 | Density (borderline → split promoted) | **PASS** | `## Density Re-Assessment` — all 10 notes ≤700w, ≤6 code blocks; the two oversized pages already split (architecture ×2, architecture-internals ×3). No borderline note unaddressed. |
| CP7 | Source word counts measured | **PASS** | Re-measured `wc -w`/code-fence counts EXACTLY match the Source table (16,746w total, ~41 fences); ratio 1.00 on all 7 pages. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all vocabulary routed to an `oc_*` owner note or an existing-term LINK; 0 new captures expected); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; master's multi-source-research mandate inherited if augment ever promotes one). |
| CP8f | Slug specificity / collision audit | **PASS** | Collision audit run for ALL planned notes across `term_dictionary/` AND `documentation/`: 0 collisions (none of the 10 `oc_*` slugs exist; no doc-note duplicates an existing term). Naming: `oc_plugins_*` slugs are specific (page-scoped), no too-general slug. |
| CP9 | Discoverability / inlinks (G8 executed) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 10, plus repo/term inlinks); G8 In-degree≥1 is in the phase gate table as an EXECUTED+verified gate (not "recommended"). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
