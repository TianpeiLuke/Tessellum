---
title: Sub-Plan pl05 — OpenClaw Docs: Plugins (reference index + acpx, admin-http-rpc, alibaba, amazon-bedrock, amazon-bedrock-mantle, anthropic)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference", "plugins/reference/acpx", "plugins/reference/admin-http-rpc", "plugins/reference/alibaba", "plugins/reference/amazon-bedrock", "plugins/reference/amazon-bedrock-mantle", "plugins/reference/anthropic"]
---

# Sub-Plan pl05: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order + body
> structure + density caps), dedup-before-create (term_dictionary ∧ documentation/ ∧ repo_openclaw*),
> the 9-GATE, cross-reference targets, undigested-terms ownership, and entry-point wiring are ALL inherited
> from the master and re-confirmed here against a fresh re-read of the 7 assigned pages.

## Scope

The plugin-reference **index page** plus the first six **per-plugin reference stub pages** (alphabetical
A-range) of OpenClaw's generated plugin catalog: `reference` (the index that points at Plugin Inventory),
`reference/acpx` (ACP runtime backend plugin), `reference/admin-http-rpc` (gateway admin RPC endpoint
plugin), `reference/alibaba` (video-generation provider plugin), `reference/amazon-bedrock` (Bedrock model
provider + embeddings + guardrails plugin), `reference/amazon-bedrock-mantle` (OpenAI-compatible Bedrock
routing provider plugin), and `reference/anthropic` (Anthropic model provider + media-understanding plugin).

These are **auto-generated stub pages** (50–67 words each) emitted from `extensions/*/package.json` +
`openclaw.plugin.json` by `pnpm plugins:inventory:gen`. Each carries a one-line summary, a **Distribution**
block (npm package name + install route), a **Surface** block (the providers/contracts/skills the plugin
exposes), and a **Related docs** pointer. **Priority P3** (Phase C — plugin-reference sprawl); these notes
are catalog entries that hang off the substantive provider/runtime docs digested in Phase A/B and the
existing `repo_openclaw*` code notes. Code-side counterparts (`repo_openclaw_extensions`,
`repo_openclaw_extensions_llm_providers`, `repo_openclaw_agents`, `repo_openclaw_gateway`) are LINKED, never
recreated.

**Source**: OpenClaw docs, 7 pages, **414 measured words total** (index 66 + 6 stubs averaging ~58 each).
**Planned: 7 notes** (1 per page; no splits — every page is far below all density caps).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Plugin reference (index) | `/plugins/reference` | 66 | 1 | 0 | 0 | concept (catalog index) |
| ACPx plugin | `/plugins/reference/acpx` | 58 | 0 | 3 | 0 | concept (plugin descriptor) |
| Admin Http Rpc plugin | `/plugins/reference/admin-http-rpc` | 54 | 0 | 3 | 0 | concept (plugin descriptor) |
| Alibaba plugin | `/plugins/reference/alibaba` | 50 | 0 | 3 | 0 | concept (plugin descriptor) |
| Amazon Bedrock plugin | `/plugins/reference/amazon-bedrock` | 67 | 0 | 3 | 0 | concept (plugin descriptor) |
| Amazon Bedrock Mantle plugin | `/plugins/reference/amazon-bedrock-mantle` | 63 | 0 | 3 | 0 | concept (plugin descriptor) |
| Anthropic plugin | `/plugins/reference/anthropic` | 56 | 0 | 3 | 0 | concept (plugin descriptor) |

- Code fences: only the index page has 1 fence (the `pnpm plugins:inventory:gen` regen command); the 6 stub
  pages have **0** fences. Far below the ≤6 cap everywhere.
- Each stub page has exactly 3 H2 sections (`## Distribution`, `## Surface`, `## Related docs`), 0 H3.
- These are the smallest pages in the entire corpus — content density is the inverse problem from the
  worked example (`plan_digest_pi_docs_p02_*`, 6,471 words / 3 pages). Strategy below addresses thin source.

## Content Strategy

- **Prioritize**: the **Surface contract** (what each plugin actually exposes — `providers:`, `contracts:`,
  `skills:`) and the **Distribution** facts (npm package id + install route: "included in OpenClaw" vs
  "npm; ClawHub"), because those two facts are the load-bearing reference data a reader needs.
- **No split**: every page is 50–67 words, 0–1 fences, ≤3 H2 — orders of magnitude below the ≤2500w/≤6-code/
  ≤400-line caps. Each page maps to exactly ONE note. (Master: "Most reference pages = 1 note"; here
  *every* page = 1 note.)
- **Thin-source enrichment (not padding)**: because the source is a generated stub, the note's value is the
  faithful Distribution + Surface descriptor PLUS the `## Related Notes` graph wiring to the substantive
  homes of each plugin's subject — the provider/runtime docs (digested in `pr01`/`pr05`/`cl01`/`co0x`) and
  the existing `repo_openclaw*` code notes. The Overview states what the plugin is and which contract/
  provider it registers; the body mirrors Distribution + Surface; do **not** invent setup steps,
  config keys, model lists, or behavior the page does not state (G2 grounding).
- **Link-out, never duplicate**: the page's own `Related docs` pointer (e.g. `amazon-bedrock` →
  `/providers/bedrock`, `acpx` → `/tools/acp-agents-setup`) is rendered in `## References` (external URL)
  AND mapped to the *planned* sibling doc note (e.g. `oc_providers_bedrock`, `oc_tools_acp_agents_setup`,
  owned by other sub-plans) in `## Related Notes` as "(planned, other sub-plan)". Provider concepts
  (Bedrock, Anthropic, embeddings, guardrails, video-generation, OpenAI-compatible routing, ACP) LINK the
  existing `term_*` notes; nothing is redefined inline.
- **BB**: every note is `concept` — a plugin reference page describes *what a plugin is and what surface it
  registers* (a descriptor), not a procedure to follow nor a model/schema. The index is a `concept`
  (catalog overview). No mixed-BB pages ⇒ no BB-driven splits.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference.md` | concept | `plugins/reference` (whole page: generated-index intro + `pnpm plugins:inventory:gen` regen + Plugin Inventory pointer) | 240 | The generated Plugin Reference index: how the per-plugin reference pages are produced from `extensions/*/package.json` + `openclaw.plugin.json`, regenerated with `pnpm plugins:inventory:gen`, and browsed via Plugin Inventory (128 generated pages by distribution/package/description). |
| 2 | `oc_plugins_reference_acpx.md` | concept | `plugins/reference/acpx` (Distribution, Surface, Related docs) | 200 | The `@openclaw/acpx` plugin — OpenClaw's ACP runtime backend with plugin-owned session and transport management; Surface = `skills`; install via npm / ClawHub; related to ACP-agents setup. |
| 3 | `oc_plugins_reference_admin_http_rpc.md` | concept | `plugins/reference/admin-http-rpc` (Distribution, Surface, Related docs) | 200 | The `@openclaw/admin-http-rpc` plugin — OpenClaw's admin HTTP RPC endpoint; Surface = `contracts: gatewayMethodDispatch`; included in OpenClaw; related to the admin-http-rpc plugin guide. |
| 4 | `oc_plugins_reference_alibaba.md` | concept | `plugins/reference/alibaba` (Distribution, Surface, Related docs) | 190 | The `@openclaw/alibaba-provider` plugin — adds video-generation provider support; Surface = `contracts: videoGenerationProviders`; included in OpenClaw; related to the Alibaba provider doc. |
| 5 | `oc_plugins_reference_amazon_bedrock.md` | concept | `plugins/reference/amazon-bedrock` (Distribution, Surface, Related docs) | 220 | The `@openclaw/amazon-bedrock-provider` plugin — Amazon Bedrock model provider with model discovery, embeddings, and guardrail support; Surface = `providers: amazon-bedrock; contracts: memoryEmbeddingProviders`; install via npm / ClawHub; related to the Bedrock provider doc. |
| 6 | `oc_plugins_reference_amazon_bedrock_mantle.md` | concept | `plugins/reference/amazon-bedrock-mantle` (Distribution, Surface, Related docs) | 210 | The `@openclaw/amazon-bedrock-mantle-provider` plugin — Bedrock Mantle provider for OpenAI-compatible model routing; Surface = `providers: amazon-bedrock-mantle`; install via npm / ClawHub; related to the Bedrock-Mantle provider doc. |
| 7 | `oc_plugins_reference_anthropic.md` | concept | `plugins/reference/anthropic` (Distribution, Surface, Related docs) | 200 | The `@openclaw/anthropic-provider` plugin — adds Anthropic model provider support; Surface = `providers: anthropic; contracts: mediaUnderstandingProviders`; included in OpenClaw; related to the Anthropic provider doc. |

Filename derivation (master rule: `oc_` + full slug with `/` and `-` → `_`): `plugins/reference` →
`oc_plugins_reference`; `plugins/reference/acpx` → `oc_plugins_reference_acpx`;
`plugins/reference/admin-http-rpc` → `oc_plugins_reference_admin_http_rpc`;
`plugins/reference/amazon-bedrock-mantle` → `oc_plugins_reference_amazon_bedrock_mantle`; etc.

## Section Coverage Map

```
plugins/reference (index)
├── (intro: generated from package.json + openclaw.plugin.json) ─ → note 1 (oc_plugins_reference) Overview
├── code fence: `pnpm plugins:inventory:gen` (regen command) ──── → note 1 (How it is generated)
└── Plugin Inventory pointer (128 generated pages) ───────────── → note 1 (Browsing) → ref-link /plugins/plugin-inventory

plugins/reference/acpx
├── (summary line) ──────────────────────────────────────────── → note 2 (oc_plugins_reference_acpx) Overview
├── ## Distribution (pkg @openclaw/acpx; npm; ClawHub) ───────── → note 2 (Distribution)
├── ## Surface (skills) ──────────────────────────────────────── → note 2 (Surface)
└── ## Related docs (/tools/acp-agents-setup) ───────────────── → note 2 (References + Related → planned oc_tools_acp_agents_setup)

plugins/reference/admin-http-rpc
├── (summary line) ──────────────────────────────────────────── → note 3 (oc_plugins_reference_admin_http_rpc) Overview
├── ## Distribution (pkg @openclaw/admin-http-rpc; included) ─── → note 3 (Distribution)
├── ## Surface (contracts: gatewayMethodDispatch) ──────────────→ note 3 (Surface)
└── ## Related docs (/plugins/admin-http-rpc) ───────────────── → note 3 (References + Related → planned oc_plugins_admin_http_rpc)

plugins/reference/alibaba
├── (summary line) ──────────────────────────────────────────── → note 4 (oc_plugins_reference_alibaba) Overview
├── ## Distribution (pkg @openclaw/alibaba-provider; included) ─ → note 4 (Distribution)
├── ## Surface (contracts: videoGenerationProviders) ───────────→ note 4 (Surface)
└── ## Related docs (/providers/alibaba) ────────────────────── → note 4 (References + Related → planned oc_providers_alibaba)

plugins/reference/amazon-bedrock
├── (summary line: discovery + embeddings + guardrails) ──────── → note 5 (oc_plugins_reference_amazon_bedrock) Overview
├── ## Distribution (pkg @openclaw/amazon-bedrock-provider; npm;ClawHub) → note 5 (Distribution)
├── ## Surface (providers: amazon-bedrock; contracts: memoryEmbeddingProviders) → note 5 (Surface)
└── ## Related docs (/providers/bedrock) ────────────────────── → note 5 (References + Related → planned oc_providers_bedrock)

plugins/reference/amazon-bedrock-mantle
├── (summary line: OpenAI-compatible routing) ───────────────── → note 6 (oc_plugins_reference_amazon_bedrock_mantle) Overview
├── ## Distribution (pkg @openclaw/amazon-bedrock-mantle-provider; npm;ClawHub) → note 6 (Distribution)
├── ## Surface (providers: amazon-bedrock-mantle) ──────────────→ note 6 (Surface)
└── ## Related docs (/providers/bedrock-mantle) ─────────────── → note 6 (References + Related → planned oc_providers_bedrock_mantle)

plugins/reference/anthropic
├── (summary line) ──────────────────────────────────────────── → note 7 (oc_plugins_reference_anthropic) Overview
├── ## Distribution (pkg @openclaw/anthropic-provider; included) → note 7 (Distribution)
├── ## Surface (providers: anthropic; contracts: mediaUnderstandingProviders) → note 7 (Surface)
└── ## Related docs (/providers/anthropic) ──────────────────── → note 7 (References + Related → planned oc_providers_anthropic)
```
No orphaned sections. Every H2 (Distribution / Surface / Related docs) of every stub page and every element
of the index page maps to a planned note. The `Related docs` pointers map to sibling doc notes owned by
other sub-plans (providers / tools / plugins guides) — cited as "(planned, other sub-plan)" + external URL.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 50–67 words, 0–1 code fences, ≤3 H2, single-BB (concept). Every page is ~1/40th of the 2,500-word cap. No page is over-cap or mixed-BB, so 1 page → 1 note throughout. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (414 measured words total: 66 + 58 + 54 + 50 + 67 + 63 + 56). New `oc_` notes: **7**.
  New `term_dictionary` notes: **0**.
- BB distribution: **concept ×7** (note 1 = catalog index; notes 2–7 = plugin descriptors). No procedure,
  model, or argument notes — these pages neither instruct nor define a schema; they describe a plugin's
  identity + contract surface.
- Est. digest words: **~1,460** (avg ~210/note). Each note is intentionally compact (faithful descriptor +
  graph wiring), well under the ≤2500w cap. Total digest words EXCEED total source words (414) because the
  value-add is the `## Related Notes` cross-reference graph + a short grounding Overview, NOT new claims.
- Code fences: 1 in source (index regen command), reproduced verbatim in note 1; notes 2–7 have 0 fences.
  All ≤6.
- Cross-refs (LOCKED 2026-06-21 at raised floors): each note maps **≥8 relevance-selected `term_dictionary`
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` section; sibling `oc_*` marked
  "(planned, this series/<sub-plan>)" with ≥5 EXISTING docs per note from the
  `hermes_agent`/`pi`/`claude_code`/`band` + AWS-Bedrock corpora.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> on **2026-06-21** (37 terms + 14 repos + 60+ docs + 70+ snippets all returned 1; the 9 confirmed-missing
> notes (this series + other OpenClaw sub-plans) do not exist yet → marked **(planned, this series)** /
> **(planned, <sub-plan>)**; they count toward the 10-doc floor but ≥5 of the 10 docs per note are EXISTING
> corpora + AWS-Bedrock notes. `entry_openclaw_docs` is the W1 master pre-step (not yet in DB).
>
> Relative paths FROM `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`;
> sibling oc doc → `oc_Y.md`; cross-domain doc → `../<folder>/<file>.md` (`../claude_code/cc_Y.md`,
> `../hermes_agent/hermes_Y.md`, `../pi/pi_Y.md`, `../band/band_Y.md`); repo →
> `../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`.

### oc_plugins_reference (8t · 11s · 11d)

**Terms** (8, EXISTING)
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model/media provider into an agent runtime; relevance: the index catalogs exactly these plugin descriptor pages.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the `openclaw.plugin.json` descriptor; relevance: the index is generated FROM `openclaw.plugin.json` + `package.json`.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK plugins are built against; relevance: every catalogued page is an SDK-built plugin.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: this is the OpenClaw plugin catalog index.
- [npm](../../term_dictionary/term_npm.md) — the Node package registry; relevance: each generated page records an npm package id + install route.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool surface; relevance: many catalogued plugins expose MCP/tool/skill surfaces summarized in the index.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime that loads plugins; relevance: the catalog enumerates harness-loaded extensions.
- [TypeScript](../../term_dictionary/term_typescript.md) — the language the `extensions/*` tree is written in; relevance: the generator parses TS package metadata to emit each page.

**Docs** (11; ≥5 EXISTING)
- [Hermes: Plugins System](../hermes_agent/hermes_plugins_system.md) — Hermes plugin loading/registry overview; relevance: the closest existing analog to OpenClaw's generated plugin catalog. (EXISTING)
- [Hermes: Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — the bundled plugin list; relevance: the OpenClaw index distinguishes "included in OpenClaw" vs npm distribution. (EXISTING)
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — taxonomy of plugin surfaces; relevance: the index summarizes each plugin's Surface (providers/contracts/skills). (EXISTING)
- [Hermes: Plugins Management](../hermes_agent/hermes_plugins_management.md) — managing/installing plugins; relevance: install route is a per-page field in the catalog. (EXISTING)
- [Pi: Extensions Overview](../pi/pi_extensions_overview.md) — Pi's extension model; relevance: a sibling coding-agent's equivalent of the generated extension catalog. (EXISTING)
- [Pi: Extensions API Methods](../pi/pi_extensions_api_methods.md) — extension registration API; relevance: documents the package→capability mapping the index reflects. (EXISTING)
- [Claude Code: SDK Plugins](../claude_code/cc_sdk_plugins.md) — Claude Code SDK plugin model; relevance: cross-tool precedent for SDK-built plugin catalogs. (EXISTING)
- [Hermes: Build Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — how a plugin is authored; relevance: explains the `package.json`+manifest a catalog page is generated from. (EXISTING)
- [Plugin Inventory](oc_plugins_plugin_inventory.md) — the browse view (128 generated pages); relevance: the index's primary pointer. (planned, pl04)
- [Plugins Manifest](oc_plugins_manifest.md) — the manifest doc; relevance: the catalog is generated from the manifest. (planned, pl04)
- [Plugins Architecture](oc_plugins_architecture.md) — plugin architecture; relevance: structural context for the catalog. (planned, pl01)

**Repos** (EXISTING)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the `extensions/*` tree; relevance: the catalog is generated from this tree's `package.json`/manifest files.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo root + `pnpm plugins:inventory:gen` build script; relevance: the regen command lives here.

**Snippets** (11, EXISTING)
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: shows how catalogued plugins are structured.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: the schema the generator reads to emit each page.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: registry the catalog enumerates.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: how a catalogued provider plugin is loaded.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — OpenClaw plugin SDK entrypoints; relevance: the SDK entries each catalog page corresponds to.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — OpenClaw plugin lifecycle; relevance: lifecycle of the plugins listed in the index.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/contract binding; relevance: the package→contract surface the catalog records.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest planner; relevance: manifest-driven generation analog.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skills vs plugins distinction; relevance: the index marks skills as a Surface type.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: package-namespace facts the catalog records.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform/plugin registry; relevance: registry-of-plugins pattern the catalog indexes.

### oc_plugins_reference_acpx (8t · 12s · 11d)

**Terms** (8, EXISTING)
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — the agent-client protocol; relevance: acpx IS the ACP runtime backend plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin descriptor; relevance: acpx is a runtime-backend plugin descriptor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the coding-agent runtime; relevance: acpx provides the ACP runtime backend the harness drives.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agents ACP fronts; relevance: acpx connects OpenClaw to ACP-speaking coding agents.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — SDK acpx is built on; relevance: acpx is an SDK plugin.
- [Skills](../../term_dictionary/term_skills.md) — the Surface acpx exposes; relevance: acpx's Surface is `skills`.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent runs; relevance: ACP backends spawn/manage subagent sessions.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: acpx is OpenClaw's ACP runtime backend.

**Docs** (11; ≥5 EXISTING)
- [Band: ACP Overview](../band/band_acp_overview.md) — ACP protocol overview; relevance: the protocol acpx implements as a runtime backend. (EXISTING)
- [Band: ACP Client](../band/band_acp_client.md) — ACP client side; relevance: the client acpx's runtime backend serves. (EXISTING)
- [Band: ACP Server](../band/band_acp_server.md) — ACP server side; relevance: acpx is the server/runtime backend role. (EXISTING)
- [Hermes: ACP Editor Integration](../hermes_agent/hermes_acp_editor_integration.md) — ACP editor wiring; relevance: a concrete ACP runtime-backend integration analog. (EXISTING)
- [Hermes: ACP Internals](../hermes_agent/hermes_acp_internals.md) — ACP session/transport internals; relevance: acpx owns "session and transport management". (EXISTING)
- [Hermes: Programmatic Integration](../hermes_agent/hermes_programmatic_integration.md) — programmatic ACP/agent integration; relevance: acpx is the programmatic ACP backend. (EXISTING)
- [Band: Adapter Codex](../band/band_adapter_codex.md) — an ACP coding-agent adapter; relevance: same adapter-backend role acpx fills. (EXISTING)
- [Pi: SDK Run Modes](../pi/pi_sdk_run_modes.md) — run modes incl. ACP-style runtimes; relevance: the runtime modes acpx provides. (EXISTING)
- [ACP Agents Setup](oc_tools_acp_agents_setup.md) — the page's own Related-docs target; relevance: how to set up ACP agents that acpx backs. (planned, to01)
- [Plugin Reference (index)](oc_plugins_reference.md) — the catalog index; relevance: parent index of this descriptor. (planned, this series)
- [Refactor: ACP](oc_refactor_acp.md) — the ACP refactor note; relevance: deeper ACP runtime context. (planned, rx01)

**Repos** (EXISTING)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the ACP runtime / agent backend; relevance: where the acpx runtime backend lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the `extensions/*` tree acpx ships in; relevance: acpx's home.

**Snippets** (12, EXISTING)
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — ACP runtime contract; relevance: the runtime-backend contract acpx implements.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: acpx is the ACP server/runtime backend.
- [snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md) — runtime registration; relevance: how the acpx runtime registers.
- [snippet_openclaw_acp_manager_turn_stream](../../code_snippets/snippet_openclaw_acp_manager_turn_stream.md) — turn streaming; relevance: acpx's plugin-owned transport streaming.
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — control application; relevance: acpx session control management.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached runtime; relevance: plugin-owned runtime lifecycle.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent bindings; relevance: acpx session/transport persistence.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event ledger; relevance: transport-level event tracking acpx manages.
- [snippet_hermes_agent_acp_session](../../code_snippets/snippet_hermes_agent_acp_session.md) — ACP session; relevance: plugin-owned session management.
- [snippet_hermes_agent_acp_server_init](../../code_snippets/snippet_hermes_agent_acp_server_init.md) — ACP server init; relevance: how the ACP backend starts.

### oc_plugins_reference_admin_http_rpc (8t · 11s · 10d)

**Terms** (8, EXISTING)
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — the RPC encoding; relevance: admin-http-rpc is a JSON-RPC dispatch endpoint.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: the `gatewayMethodDispatch` contract is RPC method dispatch.
- [WebSocket](../../term_dictionary/term_websocket.md) — duplex transport; relevance: gateway admin RPC rides WS/HTTP transports.
- [Authentication](../../term_dictionary/term_authentication.md) — auth gating; relevance: admin RPC endpoints are auth-gated operator surfaces.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin descriptor; relevance: admin-http-rpc is a (contract-exposing) plugin.
- [REST](../../term_dictionary/term_rest.md) — HTTP API style; relevance: the admin endpoint is an HTTP RPC surface.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — gateway fronting methods; relevance: the contract is `gatewayMethodDispatch`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: this is OpenClaw's admin HTTP RPC endpoint plugin.

**Docs** (10; ≥5 EXISTING)
- [Pi: RPC Protocol](../pi/pi_rpc_protocol.md) — the RPC protocol; relevance: the closest analog to gateway method dispatch over RPC. (EXISTING)
- [Pi: RPC Commands](../pi/pi_rpc_commands.md) — RPC commands; relevance: the method-dispatch surface admin-http-rpc exposes. (EXISTING)
- [Pi: RPC Events](../pi/pi_rpc_events.md) — RPC events; relevance: event side of the same dispatch protocol. (EXISTING)
- [Hermes: Programmatic Integration](../hermes_agent/hermes_programmatic_integration.md) — programmatic gateway/RPC access; relevance: how admin RPC clients call the gateway. (EXISTING)
- [Hermes: Dashboard REST API](../hermes_agent/hermes_dashboard_rest_api.md) — admin/dashboard HTTP API; relevance: a sibling admin HTTP RPC/REST surface. (EXISTING)
- [Band: REST API Introduction](../band/band_rest_api_introduction.md) — REST/admin API intro; relevance: HTTP admin endpoint analog. (EXISTING)
- [Band: A2A Gateway](../band/band_a2a_gateway.md) — agent gateway dispatch; relevance: gateway method dispatch analog. (EXISTING)
- [Plugins: Admin Http Rpc (guide)](oc_plugins_admin_http_rpc.md) — the fuller plugin guide this page points to; relevance: the page's Related-docs target. (planned, pl01)
- [Gateway: Protocol](oc_gateway_protocol.md) — gateway protocol; relevance: where the dispatch contract is defined. (planned, gw05)
- [Gateway: Authentication](oc_gateway_authentication.md) — gateway auth; relevance: the auth that gates the admin RPC. (planned, gw01)

**Repos** (EXISTING)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway method dispatch / admin RPC; relevance: where `gatewayMethodDispatch` is implemented.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the `extensions/*` tree; relevance: admin-http-rpc plugin's home.

**Snippets** (11, EXISTING)
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC protocol schema groups; relevance: the method-dispatch schema admin-http-rpc serves.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: the JSON-RPC envelope of the dispatch contract.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — RPC error/version codes; relevance: dispatch error semantics.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method-call gating; relevance: admin RPC methods are auth-gated.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — a dispatched gateway method handler; relevance: example of `gatewayMethodDispatch` in action.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — an admin mutation method; relevance: admin RPC method dispatch.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — gateway HTTP loopback; relevance: HTTP transport for gateway RPC.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — gateway session over WS; relevance: WS transport carrying gateway RPC.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — invoke dispatcher; relevance: client side of method dispatch.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — JSON-RPC server; relevance: JSON-RPC dispatch analog.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — gateway router; relevance: routes admin/method RPC calls.

### oc_plugins_reference_alibaba (8t · 10s · 10d)

**Terms** (8, EXISTING)
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin descriptor; relevance: alibaba is a video-generation provider plugin.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI providers; relevance: Alibaba is a third-party GenAI (video) service.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modal (incl. video) generation; relevance: video-generation is a multimodal output capability.
- [LLM](../../term_dictionary/term_llm.md) — model-provider context; relevance: the plugin registers a generative model provider.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — large generative models; relevance: Alibaba's video models are foundation models.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/contract invocation; relevance: the `videoGenerationProviders` contract is invoked as a tool surface.
- [npm](../../term_dictionary/term_npm.md) — package distribution; relevance: `@openclaw/alibaba-provider` is an npm package.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the plugin adds video-gen support to OpenClaw.

**Docs** (10; ≥5 EXISTING)
- [Hermes: Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — building a video-generation provider plugin; relevance: the exact same plugin role as alibaba. (EXISTING)
- [Hermes: Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider plugin; relevance: sibling media-generation provider contract. (EXISTING)
- [Hermes: Image Generation](../hermes_agent/hermes_image_generation.md) — media generation feature; relevance: the media-generation family alibaba's video gen belongs to. (EXISTING)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin authoring; relevance: alibaba is a provider plugin. (EXISTING)
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool surface; relevance: how generated media is delivered. (EXISTING)
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface taxonomy; relevance: alibaba's Surface is `contracts: videoGenerationProviders`. (EXISTING)
- [Pi: Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: how a provider plugin like alibaba registers. (EXISTING)
- [Providers: Alibaba](oc_providers_alibaba.md) — the page's Related-docs target; relevance: the fuller Alibaba provider doc. (planned, pr01)
- [Tools: Video Generation](oc_tools_video_generation.md) — the `videoGenerationProviders` consumer; relevance: the tool that uses alibaba's contract. (planned, to08)
- [Plugin Reference (index)](oc_plugins_reference.md) — the catalog index; relevance: parent index. (planned, this series)

**Repos** (EXISTING)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider/media-generation extensions; relevance: where the alibaba provider plugin lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the `extensions/*` tree; relevance: alibaba plugin's parent tree.

**Snippets** (10, EXISTING)
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-generation tool; relevance: the consumer of a videoGenerationProviders contract like alibaba's.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen plugin dispatch; relevance: how a video provider plugin is dispatched.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool; relevance: sibling media-generation surface.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen plugin dispatch; relevance: parallel provider-plugin dispatch pattern.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision dispatch; relevance: media-modality dispatch analog.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the alibaba provider registers.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: how alibaba's provider is initialized.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: the manifest declaring the videoGenerationProviders contract.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — a provider implementation; relevance: provider-plugin implementation pattern.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — sending media attachments; relevance: delivering generated video output.

### oc_plugins_reference_amazon_bedrock (10t · 12s · 12d)

**Terms** (10, EXISTING)
- [Amazon Bedrock](../../term_dictionary/term_bedrock.md) — AWS managed foundation-model service; relevance: this plugin IS the Amazon Bedrock model provider.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin descriptor; relevance: amazon-bedrock is a model-provider plugin.
- [Embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: the plugin's Surface is `contracts: memoryEmbeddingProviders`.
- [Guardrails](../../term_dictionary/term_guardrails.md) — content guardrails; relevance: the plugin summary cites guardrail support.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model discovery/catalog; relevance: the plugin does Bedrock model discovery.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — Bedrock-native model family; relevance: a model class the Bedrock provider serves.
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock Converse API; relevance: the API the Bedrock provider calls.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — AWS credential resolution; relevance: how the Bedrock provider authenticates.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI provider; relevance: Bedrock is the external GenAI backend.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: this is OpenClaw's Bedrock provider plugin.

**Docs** (12; ≥5 EXISTING)
- [Hermes: Provider AWS Bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — Hermes Bedrock provider; relevance: the same Bedrock provider in a sibling tool. (EXISTING)
- [Claude Code: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock setup; relevance: configuring the same Bedrock backend. (EXISTING)
- [Claude Code: Amazon Bedrock Model Config](../claude_code/cc_amazon_bedrock_model_config.md) — Bedrock model config; relevance: model discovery/selection the plugin performs. (EXISTING)
- [Claude Code: Amazon Bedrock Features](../claude_code/cc_amazon_bedrock_features.md) — Bedrock feature set; relevance: guardrails/embeddings features the plugin exposes. (EXISTING)
- [Pi: Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider config incl. Bedrock; relevance: cross-tool Bedrock provider configuration. (EXISTING)
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: Bedrock is a cloud inference provider. (EXISTING)
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a provider; relevance: how a Bedrock-style provider plugin is added. (EXISTING)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin authoring; relevance: amazon-bedrock is a model-provider plugin. (EXISTING)
- [Hermes: Env Vars Providers Auth Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: AWS credential env config for the Bedrock provider. (EXISTING)
- [Providers: Bedrock](oc_providers_bedrock.md) — the page's Related-docs target; relevance: the fuller Bedrock provider doc. (planned, pr01)
- [Plugins Reference: Amazon Bedrock Mantle](oc_plugins_reference_amazon_bedrock_mantle.md) — sibling Bedrock plugin; relevance: the Mantle/OpenAI-compatible Bedrock variant. (planned, this series)
- [Concepts: Memory](oc_concepts_memory.md) — the memory subsystem; relevance: the `memoryEmbeddingProviders` contract feeds memory. (planned, co03)

**Repos** (EXISTING)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions incl. Bedrock; relevance: where the Bedrock provider plugin lives.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Bedrock adapter; relevance: a sibling Bedrock adapter implementation.

**Snippets** (12, EXISTING)
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock provider plugin; relevance: the same provider-plugin role as amazon-bedrock.
- [snippet_hermes_agent_core_bedrock_adapter_discovery](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_discovery.md) — Bedrock model discovery; relevance: the model-discovery the plugin advertises.
- [snippet_hermes_agent_core_bedrock_adapter_streaming](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_streaming.md) — Bedrock streaming; relevance: streaming inference the provider performs.
- [snippet_hermes_agent_core_bedrock_adapter_format](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_format.md) — Bedrock request format; relevance: Converse-API request shaping.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — Bedrock credentials; relevance: AWS credential-chain auth for the provider.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model-catalog discovery; relevance: normalizing discovered Bedrock models.
- [snippet_pq_patronus_flink_jobs_bedrock_invocation](../../code_snippets/snippet_pq_patronus_flink_jobs_bedrock_invocation.md) — Bedrock invocation; relevance: invoking Bedrock models.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the Bedrock provider registers.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: how the Bedrock provider initializes.
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — request kwargs builder; relevance: building Bedrock call args.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: resolving Bedrock provider credentials.

### oc_plugins_reference_amazon_bedrock_mantle (10t · 11s · 11d)

**Terms** (10, EXISTING)
- [Amazon Bedrock](../../term_dictionary/term_bedrock.md) — AWS foundation-model service; relevance: Mantle is the Bedrock provider for OpenAI-compatible routing.
- [Model Router](../../term_dictionary/term_model_router.md) — routes requests across models; relevance: Mantle does OpenAI-compatible model routing.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy in front of a backend; relevance: Mantle is an OpenAI-compatible proxy over Bedrock.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — API fronting/translation; relevance: Mantle fronts Bedrock with an OpenAI-compatible API.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin descriptor; relevance: amazon-bedrock-mantle is a provider plugin.
- [Load Balancer](../../term_dictionary/term_load_balancer.md) — distributes across endpoints; relevance: routing-layer concept for the Mantle gateway.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI backend; relevance: Mantle routes to Bedrock GenAI.
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock Converse API; relevance: the native API Mantle translates from OpenAI-compatible calls.
- [AWS](../../term_dictionary/term_aws.md) — the cloud platform; relevance: Mantle targets AWS Bedrock.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: this is OpenClaw's Bedrock-Mantle provider plugin.

**Docs** (11; ≥5 EXISTING)
- [Claude Code: Amazon Bedrock Mantle Endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — the Mantle/OpenAI-compatible endpoint; relevance: the exact analog of this plugin's purpose. (EXISTING)
- [Hermes: Provider Routing Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing proxies; relevance: Mantle is an OpenAI-compatible routing proxy. (EXISTING)
- [Claude Code: LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — OpenAI-compatible LLM gateway; relevance: the same OpenAI-compatible routing layer pattern. (EXISTING)
- [Claude Code: LLM Gateway](../claude_code/cc_llm_gateway.md) — LLM gateway concept; relevance: gateway/proxy in front of model backends. (EXISTING)
- [Hermes: Subscription Proxy](../hermes_agent/hermes_subscription_proxy.md) — a model-access proxy; relevance: proxy-in-front-of-provider analog. (EXISTING)
- [Claude Code: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock setup; relevance: the Bedrock backend Mantle routes to. (EXISTING)
- [Pi: Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: Bedrock cloud provider config underneath Mantle. (EXISTING)
- [Pi: Model Overrides / Compat](../pi/pi_model_overrides_compat.md) — model compatibility/overrides; relevance: OpenAI-compatible model mapping. (EXISTING)
- [Providers: Bedrock-Mantle](oc_providers_bedrock_mantle.md) — the page's Related-docs target; relevance: the fuller Bedrock-Mantle provider doc. (planned, pr01)
- [Plugins Reference: Amazon Bedrock](oc_plugins_reference_amazon_bedrock.md) — sibling Bedrock plugin; relevance: the native (non-OpenAI-compatible) Bedrock variant. (planned, this series)
- [Plugins Reference: Anthropic](oc_plugins_reference_anthropic.md) — sibling provider plugin; relevance: another model-provider descriptor in this catalog. (planned, this series)

**Repos** (EXISTING)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: where the Mantle provider plugin lives.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — OpenAI-compatible routing adapters; relevance: the routing-adapter implementation pattern Mantle uses.

**Snippets** (11, EXISTING)
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock provider plugin; relevance: the Bedrock backend Mantle routes to.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the OpenAI-compatible interface Mantle presents.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregator/router; relevance: model-routing aggregation analog.
- [snippet_hermes_agent_core_bedrock_adapter_format](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_format.md) — Bedrock request format; relevance: translating OpenAI-compatible calls to Bedrock format.
- [snippet_hermes_agent_core_bedrock_adapter_streaming](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_streaming.md) — Bedrock streaming; relevance: streaming through the Mantle routing layer.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — Bedrock credentials; relevance: AWS auth Mantle uses to reach Bedrock.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — API-mode resolution; relevance: choosing OpenAI-compatible vs native API mode.
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — request kwargs builder; relevance: building routed-call args.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: where the Mantle provider registers.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: initializing the Mantle routing provider.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model-catalog discovery; relevance: enumerating models behind the OpenAI-compatible route.

### oc_plugins_reference_anthropic (10t · 11s · 11d)

**Terms** (10, EXISTING)
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the anthropic plugin serves Claude models (no `term_anthropic` exists).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin descriptor; relevance: anthropic is a model-provider plugin.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modal understanding; relevance: the plugin's Surface is `contracts: mediaUnderstandingProviders`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool use; relevance: Anthropic models support function-calling/tool use the provider exposes.
- [LLM](../../term_dictionary/term_llm.md) — language model; relevance: the plugin registers an LLM provider.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — large generative model; relevance: Claude is a foundation model.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI provider; relevance: Anthropic is the external GenAI backend.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — Anthropic prompt caching; relevance: a Claude provider feature surfaced via the plugin.
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock Converse (Claude-on-Bedrock); relevance: cross-link to the Anthropic-on-Bedrock path.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: this is OpenClaw's Anthropic provider plugin.

**Docs** (11; ≥5 EXISTING)
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: Anthropic is a cloud inference provider. (EXISTING)
- [Claude Code: Amazon Bedrock Model Config](../claude_code/cc_amazon_bedrock_model_config.md) — Claude model config (on Bedrock); relevance: Claude model configuration the provider exposes. (EXISTING)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin authoring; relevance: anthropic is a model-provider plugin. (EXISTING)
- [Hermes: Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime; relevance: how the Anthropic provider runs at inference time. (EXISTING)
- [Pi: Provider Auth](../pi/pi_provider_auth.md) — provider authentication; relevance: Anthropic API key auth for the provider. (EXISTING)
- [Pi: Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: configuring the Anthropic cloud provider. (EXISTING)
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool surface; relevance: the `mediaUnderstandingProviders` contract feeds media understanding. (EXISTING)
- [Hermes: Vision / Image Paste](../hermes_agent/hermes_vision_image_paste.md) — vision/media understanding; relevance: the media-understanding capability the Surface exposes. (EXISTING)
- [Providers: Anthropic](oc_providers_anthropic.md) — the page's Related-docs target; relevance: the fuller Anthropic provider doc. (planned, pr01)
- [Plugins Reference: Amazon Bedrock](oc_plugins_reference_amazon_bedrock.md) — Anthropic-on-Bedrock comparison; relevance: Claude is also served via the Bedrock plugin. (planned, this series)
- [Nodes: Media Understanding](oc_nodes_media_understanding.md) — the mediaUnderstandingProviders consumer; relevance: the node that uses anthropic's contract. (planned, nd02)

**Repos** (EXISTING)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: where the Anthropic provider plugin lives.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Anthropic adapter; relevance: a sibling Anthropic adapter implementation.

**Snippets** (11, EXISTING)
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw Anthropic provider; relevance: the exact provider this plugin registers.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — Anthropic provider plugin; relevance: the same provider-plugin role.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — Anthropic client adapter; relevance: the Messages-API client the provider uses.
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — Anthropic adapter endpoints; relevance: the API endpoints the provider calls.
- [snippet_hermes_agent_core_auxiliary_anthropic_adapter](../../code_snippets/snippet_hermes_agent_core_auxiliary_anthropic_adapter.md) — auxiliary Anthropic adapter; relevance: secondary Anthropic call path.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision dispatch; relevance: media-understanding contract dispatch.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision input handling; relevance: feeding media to the mediaUnderstandingProviders contract.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the Anthropic provider registers.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: initializing the Anthropic provider.
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — request kwargs builder; relevance: building Anthropic Messages-API call args.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: resolving the Anthropic API key/provider.

**DB-verification (2026-06-21):** ALL terms, repos, docs, and snippets above returned `1` from
Sibling `oc_*` (`oc_plugins_plugin_inventory`, `oc_plugins_manifest`, `oc_plugins_architecture`,
`oc_tools_acp_agents_setup`, `oc_refactor_acp`, `oc_plugins_admin_http_rpc`, `oc_gateway_protocol`,
`oc_gateway_authentication`, `oc_providers_alibaba`, `oc_tools_video_generation`, `oc_providers_bedrock`,
`oc_concepts_memory`, `oc_providers_bedrock_mantle`, `oc_providers_anthropic`, `oc_nodes_media_understanding`,
and the 6 sibling notes of this sub-plan) are NOT-yet-created planned notes (marked planned). `entry_openclaw_docs`
is the W1 master pre-step. **Confirmed MISSING terms (NOT cited; the planned `oc_*` or a verified existing term
is used instead):** `term_anthropic`, `term_alibaba`, `term_amazon_bedrock`, `term_video_generation`,
`term_session`, `term_clawhub`, `term_extension`, `term_streaming`, `term_openai`.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| plugin reference (generated index) | → note 1 (`oc_plugins_reference`); NOT a term — a doc concept. Link `term_provider_plugin`, `term_plugin_manifest`, `term_plugin_sdk`. |
| Plugin Inventory | → planned `oc_plugins_plugin_inventory` (pl04). Pointer only here. No term. |
| ACPx / ACP runtime backend | → note 2; concept owned by this doc note. Link existing `term_acp_agent_client_protocol`. No new term. |
| gatewayMethodDispatch (contract) | → note 3; contract name documented inline as the Surface. Link `term_json_rpc`. No term (impl-specific contract id). |
| admin HTTP RPC | → note 3; doc concept. Link `term_json_rpc`, `term_websocket`. No new term. |
| videoGenerationProviders (contract) | → note 4; contract name = Surface. Concept owned by planned `oc_tools_video_generation` (to08). No new term. |
| memoryEmbeddingProviders (contract) | → note 5; contract name = Surface. Link existing `term_embedding`. No new term. |
| mediaUnderstandingProviders (contract) | → note 7; contract name = Surface. Owned by planned `oc_nodes_media_understanding` (nd02). No new term. |
| amazon-bedrock / amazon-bedrock-mantle / anthropic / alibaba (provider names) | Documented as config/provider ids, NOT promoted to term notes. Link existing `term_bedrock` / `term_claude` (+ planned `oc_providers_*`). Provider names per master are documentation subjects, not term_dictionary entries. |
| guardrails / embeddings / model discovery | Link existing `term_guardrails` / `term_embedding`; `term_model_catalog` for discovery. No new terms. |
| ClawHub (install route) | Mentioned as a distribution channel; owned by ClawHub sub-plans (cw01–03). No new term (no existing `term_clawhub`; link planned `oc_clawhub_*`). |

**Expected new `term_dictionary` captures: 0.** All vocabulary is either (a) an OpenClaw doc concept owned by
an `oc_*` note, (b) an impl-specific contract/package id documented inline as the plugin's Surface, or (c) a
provider/concept already covered by an existing term note that is LINKED. No genuinely reusable cross-cutting
term lacks a home, so no new-term candidate is proposed. Augment re-runs the Step 2d scan.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master: OpenClaw
vocabulary → `oc_*` doc notes; existing terms linked, not duplicated). If `/tessellum-augment-digestion-plan`'s
re-run of Step 2d surfaces a genuinely reusable cross-cutting term with no doc-page home AND no existing
note, it is captured via `/tessellum-capture-term-note` + added to the agentic/LLM `acronym_glossary_*.md`
(per master W5) — not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). Gate table identical to the master's 9-GATE definition.

| Gate | Name | Check | Pass condition |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` on all 7 notes | YAML field order + body structure valid; 0 ERROR/LINK-003; itemized keywords/topics; quoted year tags; no forbidden fields. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/plugins/reference[/<slug>].md` | Every claim (package id, install route, Surface contracts/providers, summary) traces to the source page; no invented setup/config/behavior. |
| G3 | Density + Coverage | per-note words/code; section coverage map | ≤2500w / ≤6 code / ≤400 lines per note (all ~210w); every source H2 mapped; no orphan. |
| G4 | Cross-Reference | `## Related Notes` per note | ≥8 relevance-selected term links + ≥10 snippets + ≥10 docs + sibling `oc_*` + `repo_openclaw*`, each with a relevance statement; all existing targets resolve (per the LOCKED mapping). |
| G5 | Ghost-reference | detect + redirect | 0 ghost references; any not-yet-created sibling `oc_*`/`oc_providers_*` link is to a planned-this-run note or redirected. |
| G6 | Broken-link | `/tessellum-fix-broken-links` after reindex | 0 broken links in `note_links` for the 7 new notes. |
| G7/G8 | Discoverability | in-degree ≥1 from outside `documentation/openclaw/` | Each new note RECEIVES ≥1 inbound link from `entry_openclaw_docs.md` (W1) and/or `repo_openclaw*`/`term_*`; in-degree ≥1; anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference oc_plugins_reference_acpx oc_plugins_reference_admin_http_rpc oc_plugins_reference_alibaba oc_plugins_reference_amazon_bedrock oc_plugins_reference_amazon_bedrock_mantle oc_plugins_reference_anthropic"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections (## Overview | ## Related Notes)
  for sec in ${(s:|:)REQ_SECTIONS}; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # density caps (body words / code fences)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # sibling cross-ref present (SIBLING_PREFIX)
  grep -qE "\]\(${SIBLING_PREFIX}[a-z0-9_]+\.md\)" "$f" || echo "$n NO SIBLING ${SIBLING_PREFIX}* LINK"
done

# YAML frontmatter sweep across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# Ghost-reference + broken-link sweep after incremental reindex
bash scripts/update_notes_database.sh
# (then) /tessellum-fix-ghost-references ; /tessellum-fix-broken-links
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference | concept | 240 | 1 | ✅ (far under 2500w/6cb) |
| 2 | oc_plugins_reference_acpx | concept | 200 | 0 | ✅ |
| 3 | oc_plugins_reference_admin_http_rpc | concept | 200 | 0 | ✅ |
| 4 | oc_plugins_reference_alibaba | concept | 190 | 0 | ✅ |
| 5 | oc_plugins_reference_amazon_bedrock | concept | 220 | 0 | ✅ |
| 6 | oc_plugins_reference_amazon_bedrock_mantle | concept | 210 | 0 | ✅ |
| 7 | oc_plugins_reference_anthropic | concept | 200 | 0 | ✅ |

No note approaches any cap; the inverse risk (thin/empty stub) is mitigated by a grounded Overview +
Distribution/Surface descriptor + the relevance-selected `## Related Notes` graph. **No over-compression
risk** (source is already minimal — the digest is faithful, not lossy). No splits needed.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `0_entry_points/entry_openclaw_docs.md` (the >30-note series hub, CREATED as the
master W1 pre-step before any sub-plan executes), under a **"Plugins — Reference Catalog (A-range)"** cluster.
Each new note receives its entry-point back-link at finalization (this is the primary G7/G8 inbound-link
source). No new entry point is created by this sub-plan. Master W2/W3 (parent-hub back-links, code↔docs
cross-links) are global pre-steps, not repeated per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 in-degree ≥1):
- `entry_openclaw_docs.md` (W1) → **all 7 notes** (primary anti-island source).
- `repo_openclaw_extensions.md` → notes 1, 2, 4, 5, 6, 7 (the `extensions/*` tree these reference pages are
  generated from / where these plugins live).
- `repo_openclaw_extensions_llm_providers.md` → notes 4, 5, 6, 7 (the LLM/media provider extensions).
- `repo_openclaw_agents.md` → note 2 (ACP runtime backend).
- `repo_openclaw_gateway.md` → note 3 (gateway method dispatch / admin RPC).
- `term_bedrock.md` → notes 5, 6; `term_claude.md` → note 7; `term_provider_plugin.md` → notes 2–7;
  `term_acp_agent_client_protocol.md` → note 2; `term_json_rpc.md` → note 3.
- Reciprocal: sibling `oc_*` (note 1 index ↔ notes 2–7) provide in-folder inlinks (do NOT count toward G8,
  which requires an *outside-folder* inbound link — covered by `entry_openclaw_docs` + repos/terms above).

## Pacing Rules (inherited from master)

Single execution phase (7 notes ≪ 30-agent fan-out cap). 8 gates pass before commit. Re-read each source
page at execution; reproduce the one index code fence verbatim; one BB (concept) per note; reindex
incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase
--autostash` first; commit+push the wave; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref mapping LOCKED at raised floors; ≥8t·≥10s·≥10d per note) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the draft `## Candidate Cross-References` with a relevance-selected,
(**≥8 terms · ≥10 code_snippets · ≥10 docs per note**). Re-read all 7 source pages from
`inbox/openclaw_docs/plugins/reference[/<slug>].md` — measured stats match the plan exactly (index 1 fence
+ Plugin Inventory pointer; 6 stubs each = summary + `## Distribution` + `## Surface` + `## Related docs`,
0 fences). No over-compression / omission / undigested-term gap surfaced; no splits needed.

**DB verification.** All 37 cited terms, 14 repos, 60+ docs, and 70+ snippets returned `1` from
EXISTING cross-domain analogs (`hermes_agent`/`pi`/`claude_code`/`band` + AWS-Bedrock). Sibling `oc_*`
(this series + other sub-plans) and `entry_openclaw_docs` (W1 pre-step) are the only non-DB-cited targets,
all marked planned.

**Per-note locked counts (terms / snippets / docs / repos · floors met):**

| Note | Terms | Snippets | Docs | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---:|---:|---|
| `oc_plugins_reference` | 8 | 11 | 11 | 2 | ✅ |
| `oc_plugins_reference_acpx` | 8 | 12 | 11 | 3 | ✅ |
| `oc_plugins_reference_admin_http_rpc` | 8 | 11 | 10 | 2 | ✅ |
| `oc_plugins_reference_alibaba` | 8 | 10 | 10 | 2 | ✅ |
| `oc_plugins_reference_amazon_bedrock` | 10 | 12 | 12 | 3 | ✅ |
| `oc_plugins_reference_amazon_bedrock_mantle` | 10 | 11 | 11 | 2 | ✅ |
| `oc_plugins_reference_anthropic` | 10 | 11 | 11 | 3 | ✅ |

**New-term candidates.** None. Re-run of Step 2d on all 7 pages surfaced no genuinely reusable cross-cutting
term lacking a home: every concept is either an OpenClaw doc concept owned by an `oc_*` note (provider names
`amazon-bedrock`/`anthropic`/`alibaba`, contract ids `gatewayMethodDispatch`/`videoGenerationProviders`/
`memoryEmbeddingProviders`/`mediaUnderstandingProviders`, `ClawHub`), an impl-specific package/contract id
documented inline as the Surface, or a provider/concept already covered by an EXISTING term that is LINKED
(`term_bedrock`, `term_claude`, `term_embedding`, `term_guardrails`, `term_provider_plugin`,
`term_acp_agent_client_protocol`, `term_multimodal`, `term_model_router`, `term_reverse_proxy`). Expected new
`term_dictionary` captures: **0** (matches the master's OpenClaw-vocab → `oc_*` ownership policy). Best-fit
glossary if any future capture were needed: `0_entry_points/acronym_glossary_agentic_llm.md` (agentic/LLM).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (5 notes at 8, 3 at 10), ≥10 snippets, ≥10 docs, each link carries a `relevance:` statement; ≥1 entry-point back-link inherited via W1. |
| CP2 | 9-GATE present (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table has G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (updated to ≥8t·≥10s·≥10d), G5 Ghost, G6 Broken-link, G7/G8 Discoverability; G5/G6/G1 consolidated via `/tessellum-validate-note-gates` in Validation Scripts. |
| CP3 | Entry point inherited | **PASS** | `## Entry Point Decision` contributes 7 rows to `entry_openclaw_docs.md` (created as master W1 pre-step for the >30-note series); DB confirms `entry_openclaw_docs` not-yet-created (correct W1 timing). |
| CP4 | Size | **PASS** | 7 notes ≤30; single execution phase; no sub-plan split required. |
| CP5 | Format derived | **PASS** | YAML field order + `## Overview`/source-mirrored H2/`## Related Notes`/`## References`/footer derived from existing `cc_*`/`pi_*` doc corpora (master Format Definition); not invented. |
| CP6 | Density | **PASS** | All 7 notes ~190–240w / 0–1 fences / ≤3 H2 — orders of magnitude under ≤2500w/≤6cb/≤400-line caps; no borderline note; Density Re-Assessment confirms no splits. |
| CP7 | Sources measured | **PASS** | Re-read all 7 source pages 2026-06-21; measured index = 1 fence + Plugin Inventory pointer, 6 stubs = summary + 3 H2 + 0 fences — matches the plan's Source table exactly (ratio ≈ 1.0; no under-estimation). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (expected new captures: 0; every row dispositioned to an `oc_*` owner or EXISTING linked term); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherits `/tessellum-capture-term-note` canonical via master W5). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs → no specificity renames needed. Collision audit run across ALL 7 planned `oc_*` doc notes vs `term_dictionary/` + `documentation/`: no `oc_plugins_reference*` slug duplicates an existing term or doc note; provider/contract concepts route to EXISTING terms (linked, not recreated). |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks (existing notes → new notes)` maps `entry_openclaw_docs` (W1) → all 7 + `repo_openclaw_extensions`/`_llm_providers`/`_agents`/`_gateway` + `term_bedrock`/`term_claude`/`term_provider_plugin`/`term_acp_agent_client_protocol`/`term_json_rpc` → specific notes; G7/G8 gate requires DB in-degree ≥1 from outside `documentation/openclaw/` per note (anti-island). |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan `status` advanced `pending → ready`.
