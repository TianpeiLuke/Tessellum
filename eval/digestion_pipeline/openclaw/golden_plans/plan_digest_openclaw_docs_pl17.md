---
title: Sub-Plan pl17 — OpenClaw Docs: Plugins (Reference O–Q)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/openrouter", "plugins/reference/openshell", "plugins/reference/perplexity", "plugins/reference/pixverse", "plugins/reference/policy", "plugins/reference/qa-channel", "plugins/reference/qa-lab"]
---

# Sub-Plan pl17: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML/body/density caps), dedup
> (term_dictionary + documentation/ + repo_openclaw*), 9-GATE validation, cross-reference floors, and
> entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master.

## Scope

The seven plugin-reference pages O–Q under `docs.openclaw.ai/plugins/reference/`: `openrouter` (LLM model
provider), `openshell` (NVIDIA OpenShell sandbox backend), `perplexity` (web-search provider), `pixverse`
(video-generation provider), `policy` (doctor health-check / config-conformance plugin), `qa-channel`
(a chat-channel surface for testing), and `qa-lab` (private debugger UI + scenario runner). Each is a
terse plugin-reference card: a one-line summary, a **Distribution** section (npm package + install route),
a **Surface** section (contracts/providers/channels the plugin contributes), and (for most) a **Related
docs** pointer to the fuller provider/tool/channel/CLI page. `policy.md` additionally carries a manually
authored **Behavior** section. **Priority P3** (Phase C — the per-plugin reference sprawl); these are
catalog stubs, so they map 1:1 to one digest note each, no splits.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| openrouter | plugins/reference/openrouter | 60 | 0 | 3 | 0 | model |
| openshell | plugins/reference/openshell | 65 | 0 | 2 | 0 | model |
| perplexity | plugins/reference/perplexity | 50 | 0 | 3 | 0 | model |
| pixverse | plugins/reference/pixverse | 52 | 0 | 3 | 0 | model |
| policy | plugins/reference/policy | 451 | 0 | 4 | 0 | concept |
| qa-channel | plugins/reference/qa-channel | 64 | 0 | 3 | 0 | model |
| qa-lab | plugins/reference/qa-lab | 59 | 0 | 2 | 0 | model |

Total measured: **801 words, 0 code fences.** Six pages are ≤65w catalog stubs; only `policy.md` (451w) carries
substantive prose (its `## Behavior` block, lines 23–73). H2s across the set are the fixed reference-card
sections: **Distribution**, **Surface**, **Related docs** (and **Behavior** on policy). No H3s anywhere.

## Content Strategy

- **Prioritize**: `policy` (the only page with real content — config-conformance/doctor-check semantics,
  posture rule families, `policy.jsonc`, scopes) gets the fullest treatment. The six stub pages each become a
  compact reference note that records the package, install route, contributed contracts/providers/channels,
  and a link-out to the canonical page.
- **Split**: none. Every page is far below all density caps (largest is 451w vs the 2,500w cap; 0 code blocks
  vs the 6-block cap), and each plugin is one atomic catalog entry. No mixed-BB page (policy is single-BB
  concept; the rest are single-BB model = a plugin/contract descriptor).
- **Link-out (do NOT duplicate)**: each `## Related docs` target is the fuller doc that lives in another
  sub-plan and is linked, not re-digested here — `openrouter` → providers `pr06`/plugin-list; `perplexity`
  → tools `to06` (`tools/perplexity-search`); `pixverse` → providers `pr07` (`providers/pixverse`); `policy`
  → CLI `cl06` (`cli/policy`); `qa-channel` → channels `ch04` (`channels/qa-channel`). `openshell` and
  `qa-lab` have no Related-docs pointer (they cross-link the gateway/web sub-plans instead). The vault's
  existing `repo_openclaw*` code notes and the hermes/pi provider docs are LINKED, never recreated.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_openrouter.md` | model | openrouter.md: Distribution, Surface, Related docs | 220 | The OpenRouter provider plugin (`@openclaw/openrouter-provider`, bundled): adds the `openrouter` model provider plus image/media-understanding/music/speech/video provider contracts via a single aggregator key. |
| 2 | `oc_plugins_reference_openshell.md` | model | openshell.md: Distribution, Surface | 230 | The OpenShell sandbox-backend plugin (`@openclaw/openshell-sandbox`, npm/ClawHub): an OpenClaw sandbox backend for the NVIDIA OpenShell CLI with mirrored local workspaces and SSH command execution. |
| 3 | `oc_plugins_reference_perplexity.md` | model | perplexity.md: Distribution, Surface, Related docs | 210 | The Perplexity plugin (`@openclaw/perplexity-plugin`, npm/ClawHub): registers a `webSearchProviders` contract so agents can run Perplexity web search; links to the `tools/perplexity-search` doc. |
| 4 | `oc_plugins_reference_pixverse.md` | model | pixverse.md: Distribution, Surface, Related docs | 210 | The PixVerse video-generation provider plugin (`@openclaw/pixverse-provider`, npm/ClawHub): contributes a `videoGenerationProviders` contract for text/image-to-video generation; links the `providers/pixverse` doc. |
| 5 | `oc_plugins_reference_policy.md` | concept | policy.md: Distribution, Surface, Behavior, Related docs | 520 | The Policy plugin (`@openclaw/policy`, bundled): policy-backed doctor checks for workspace conformance — posture rule families (channel/tool/sandbox/data-handling/ingress/secret), `policy.jsonc`, `openclaw policy check`/`compare`/`doctor --lint`, attestation hashes, and named scopes. |
| 6 | `oc_plugins_reference_qa_channel.md` | model | qa-channel.md: Distribution, Surface, Related docs | 200 | The QA Channel plugin (`@openclaw/qa-channel`, source-checkout only): adds a `qa-channel` channel surface for sending/receiving OpenClaw messages in test/QA scenarios; links the `channels/qa-channel` doc. |
| 7 | `oc_plugins_reference_qa_lab.md` | model | qa-lab.md: Distribution, Surface | 200 | The QA Lab plugin (`@openclaw/qa-lab`, source-checkout only): a private debugger UI and scenario runner for OpenClaw; declares a `webSearchProviders` contract used by its scenarios. |

**Filename note:** slug `plugins/reference/<name>` → `oc_plugins_reference_<name>.md` with `/` and `-` replaced
by `_` (so `qa-channel` → `oc_plugins_reference_qa_channel.md`, `qa-lab` → `oc_plugins_reference_qa_lab.md`).
No aspect suffixes needed (no splits). One BB per note.

## Section Coverage Map

```
plugins/reference/openrouter.md
├── (intro one-liner) ───────────── → note 1 (oc_plugins_reference_openrouter) Overview
├── ## Distribution ─────────────── → note 1
├── ## Surface ──────────────────── → note 1
└── ## Related docs ─────────────── → note 1 (link-out: providers/openrouter)
plugins/reference/openshell.md
├── (intro one-liner) ───────────── → note 2 (oc_plugins_reference_openshell) Overview
├── ## Distribution ─────────────── → note 2
└── ## Surface ──────────────────── → note 2
plugins/reference/perplexity.md
├── (intro one-liner) ───────────── → note 3 (oc_plugins_reference_perplexity) Overview
├── ## Distribution ─────────────── → note 3
├── ## Surface ──────────────────── → note 3
└── ## Related docs ─────────────── → note 3 (link-out: tools/perplexity-search)
plugins/reference/pixverse.md
├── (intro one-liner) ───────────── → note 4 (oc_plugins_reference_pixverse) Overview
├── ## Distribution ─────────────── → note 4
├── ## Surface ──────────────────── → note 4
└── ## Related docs ─────────────── → note 4 (link-out: providers/pixverse)
plugins/reference/policy.md
├── (intro one-liner) ───────────── → note 5 (oc_plugins_reference_policy) Overview
├── ## Distribution ─────────────── → note 5
├── ## Surface ──────────────────── → note 5
├── ## Behavior (lines 23–73) ───── → note 5 (full posture-rule + policy.jsonc + scopes prose)
└── ## Related docs ─────────────── → note 5 (link-out: cli/policy)
plugins/reference/qa-channel.md
├── (intro one-liner) ───────────── → note 6 (oc_plugins_reference_qa_channel) Overview
├── ## Distribution ─────────────── → note 6
├── ## Surface ──────────────────── → note 6
└── ## Related docs ─────────────── → note 6 (link-out: channels/qa-channel)
plugins/reference/qa-lab.md
├── (intro one-liner) ───────────── → note 7 (oc_plugins_reference_qa_lab) Overview
├── ## Distribution ─────────────── → note 7
└── ## Surface ──────────────────── → note 7
```
No orphaned sections — every H2 (and policy's Behavior block) maps to exactly one note. `## Related docs`
targets are link-outs to other sub-plans' pages, not new sections here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are single-BB and far below caps (max 451w / 0 code fences vs 2,500w / 6-block caps). Each plugin is one atomic catalog entry → 1 note each, no split. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (801 measured words, 0 code fences).
- New `oc_` notes: **7** (1 note per page — overrides the master's nominal 11/sub-plan estimate, which assumed
  splits; these are sub-100w stubs + one 451w page, none splittable).
- New `term_dictionary` notes: **0** (plugin/provider/channel vocabulary digested as `oc_*` doc notes; existing
  terms linked).
- BB distribution: **model ×6** (notes 1–4, 6, 7 — each a plugin/contract descriptor) · **concept ×1**
  (note 5 `policy`, the posture/conformance model).
- Est. digest words ~1,790 (avg ~256/note; the six stub notes ~210/each, policy ~520). Each note adds Overview +
  a relevance-stated `## Related Notes` block; all stay ≪ caps (≤400 lines, ≤2,500 words, ≤6 code blocks — 0 code
  blocks expected since source has none).
- Cross-refs: per-note mapping is **LOCKED at raised floors (xref-augment 2026-06-21): ≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** per note (PLUS
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` below for the exact set.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> LIKE '%/<stem>.md'"` (2026-06-21). Relative paths are FROM a note at
> `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`; sibling `oc_*`
> (this series, planned) → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo →
> `../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`. Sibling `oc_*`
> docs DO NOT exist yet → cited as **(planned, this series)** toward the 10-doc floor; ≥5 of the 10 docs per
> `term_web_search`, `term_openrouter`, `term_video_generation`, `term_nvidia`, `term_policy_as_code`,
> `term_attestation`, `term_configuration_drift` (these are plugin-contract names, not reusable vault terms).

### oc_plugins_reference_openrouter (8t · 11s · 10d)

**Terms** (8)
- [Model Router](../../term_dictionary/term_model_router.md) — component that picks a model/provider per request; relevance: OpenRouter IS an aggregating router fronting many upstream LLMs.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — strategy for selecting and ordering model providers; relevance: the openrouter plugin registers a provider entry that participates in OpenClaw's routing.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models with metadata; relevance: OpenRouter exposes a large upstream catalog through one key, populating the catalog.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted generative-AI APIs; relevance: OpenRouter is exactly such a third-party aggregator service.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin that contributes a model/media provider contract; relevance: `@openclaw/openrouter-provider` is a provider plugin in the bundled set.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the openrouter provider's primary surface is `providers: openrouter` for LLM access.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server fronting upstreams under one endpoint; relevance: OpenRouter's aggregator-key model is a reverse-proxy pattern over many model APIs.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — alternate provider used on primary failure; relevance: aggregators like OpenRouter are commonly wired as failover/fallback entries.

**Docs** (10; 6 existing + 4 planned-sibling)
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — how a model-provider plugin registers in the Hermes/OpenClaw lineage; relevance: documents the provider-plugin surface this card declares.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing/selection behavior; relevance: explains how an openrouter provider entry is chosen at runtime.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing through proxy/aggregator providers; relevance: OpenRouter is the canonical aggregator-proxy case.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — catalog of bundled/built-in plugins; relevance: openrouter ships "included in OpenClaw" (bundled), matching this list's pattern.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud LLM provider configuration in a sibling coding-agent; relevance: parallel provider-config model for cross-tool comparison.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider catalog; relevance: situates OpenRouter among cloud inference options.
- [oc_plugins_reference_pixverse](oc_plugins_reference_pixverse.md) — sibling provider-plugin card (planned, this series); relevance: also a provider plugin contributing a media-generation contract.
- [oc_plugins_reference_perplexity](oc_plugins_reference_perplexity.md) — sibling provider-plugin card (planned, this series); relevance: another contract-contributing provider plugin in the same reference cluster.
- [oc_plugins_reference_policy](oc_plugins_reference_policy.md) — sibling card (planned, this series) on provider-posture conformance; relevance: model-provider posture is a Policy rule family that governs provider plugins like openrouter.
- [oc_providers_openrouter (pr06)](../openclaw/oc_providers_openrouter.md) — the fuller Related-docs target (planned, pr06); relevance: this card's `## Related docs` links the providers/openrouter page.

**Repos** (4)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — OpenClaw LLM-provider extensions code; relevance: home of the openrouter provider implementation.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: parent of the bundled provider plugins.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapter implementations; relevance: shows the provider-adapter pattern an openrouter entry follows.

**Snippets** (11)
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — the OpenRouter aggregator provider implementation; relevance: exact code behind this plugin card.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM model-pricing resolution; relevance: pricing path for OpenRouter's aggregated catalog.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias→pricing lookup; relevance: aggregator catalogs rely on alias resolution.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly in agents; relevance: OpenRouter populates this catalog with upstream models.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest-driven model-catalog planning; relevance: how a provider plugin's models enter the catalog.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — Hermes openrouter provider plugin; relevance: sibling-ecosystem implementation of the same provider.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: how a provider plugin registers its contract (the Surface section).
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — base provider abstract interface; relevance: the contract an openrouter provider implements.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch wiring; relevance: how provider plugins are loaded and dispatched.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model-name normalization; relevance: aggregator model names must be normalized.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — sibling OpenAI provider implementation; relevance: parallel provider-plugin structure for comparison.

### oc_plugins_reference_openshell (8t · 11s · 10d)

**Terms** (8)
- [OpenShell](../../term_dictionary/term_openshell.md) — the NVIDIA OpenShell CLI / sandbox concept; relevance: this plugin is the OpenClaw backend for exactly that CLI.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — pluggable execution backend for sandboxed runs; relevance: `@openclaw/openshell-sandbox` IS a sandbox backend.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: the plugin provides a sandbox surface (Surface: plugin/sandbox backend).
- [SSH](../../term_dictionary/term_ssh.md) — secure shell remote command protocol; relevance: the page summary states "SSH command execution".
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote development over SSH; relevance: OpenShell runs commands on a remote shell over SSH.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime that executes agent tool calls; relevance: the sandbox backend is the harness execution surface for OpenClaw agents.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that edit/run code autonomously; relevance: OpenShell mirrored workspaces give such agents an execution environment.
- [Git Worktree Agents](../../term_dictionary/term_git_worktree_agents.md) — per-agent mirrored workspace pattern; relevance: OpenShell's "mirrored local workspaces" are the same mirrored-workspace technique.

**Docs** (10; 7 existing + 3 planned-sibling)
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — taxonomy of plugin surfaces (provider/channel/sandbox/tool); relevance: classifies the sandbox-backend surface this plugin contributes.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — pluggable terminal/exec backends; relevance: OpenShell is a remote terminal/exec backend.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — sandbox isolation + credential handling; relevance: governs how a sandbox backend isolates execution.
- [pi_containerization](../pi/pi_containerization.md) — containerized sandbox execution in a sibling agent; relevance: parallel sandbox-backend model.
- [pi_security_model](../pi/pi_security_model.md) — security/isolation model for a sibling coding agent; relevance: frames sandbox-backend trust boundaries.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime + container backends; relevance: comparison point for OpenShell's backend role.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — filesystem/network isolation in a sandbox; relevance: OpenShell's mirrored-workspace FS bridge is the same concern.
- [oc_plugins_reference_policy](oc_plugins_reference_policy.md) — sibling card (planned, this series); relevance: Policy's sandbox posture rules govern approved sandbox modes/backends like OpenShell.
- [oc_gateway_openshell (gw04)](../openclaw/oc_gateway_openshell.md) — the gateway OpenShell page (planned, gw04); relevance: openshell cross-links the gateway sub-plan.
- [oc_gateway_sandboxing (gw05)](../openclaw/oc_gateway_sandboxing.md) — gateway sandboxing page (planned, gw05); relevance: sandbox-backend selection is configured via gateway sandboxing.

**Repos** (4)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security/sandbox code; relevance: home of the OpenShell backend/CLI/mirror/FS-bridge implementation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agent runtime; relevance: agents run inside the OpenShell sandbox backend.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo root; relevance: the sandbox backend is part of the OpenClaw distribution.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions; relevance: parent for the openshell-sandbox npm/ClawHub package.

**Snippets** (11)
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — the OpenShell sandbox backend implementation; relevance: exact code behind this plugin card.
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — OpenShell CLI integration; relevance: the NVIDIA OpenShell CLI the backend wraps.
- [snippet_openclaw_security_openshell_mirror](../../code_snippets/snippet_openclaw_security_openshell_mirror.md) — mirrored-workspace logic; relevance: implements "mirrored local workspaces" from the summary.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — filesystem bridge for OpenShell; relevance: bridges local FS to the remote OpenShell session.
- [snippet_hermes_agent_tools_environments_ssh](../../code_snippets/snippet_hermes_agent_tools_environments_ssh.md) — SSH execution environment; relevance: the SSH command-execution mechanism OpenShell uses.
- [snippet_hermes_agent_tools_environments_base](../../code_snippets/snippet_hermes_agent_tools_environments_base.md) — base execution-environment abstraction; relevance: the interface a sandbox backend implements.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed code execution; relevance: parallel sandbox-exec pattern.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy enforcement; relevance: governs what an OpenShell sandbox may touch.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/lifecycle; relevance: how the openshell-sandbox plugin is loaded.

### oc_plugins_reference_perplexity (8t · 10s · 10d)

**Terms** (8)
- [Perplexity](../../term_dictionary/term_perplexity.md) — Perplexity web-search/answer service; relevance: this plugin registers Perplexity as a web-search provider.
- [Web Search](../../term_dictionary/term_information_retrieval.md) — retrieving documents/answers from a query (IR); relevance: the plugin's `webSearchProviders` contract performs web search/IR. (`term_web_search` is MISSING — using IR.)
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: web-search providers feed retrieved context into agent generations.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: agents invoke the web-search provider via a tool/function call.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin contributing a provider contract; relevance: `@openclaw/perplexity-plugin` contributes the `webSearchProviders` contract.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI APIs; relevance: Perplexity is a third-party search/answer API.
- [Deep Research Agent](../../term_dictionary/term_deep_research_agent.md) — agent that fans out web research; relevance: Perplexity is a common backend for deep-research web search.
- [ReAct](../../term_dictionary/term_react.md) — reason+act tool-use loop; relevance: web-search providers are invoked inside the agent's reason/act loop.

**Docs** (10; 6 existing + 4 planned/sibling)
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — the web-search provider plugin contract; relevance: documents the exact `webSearchProviders` surface this card declares.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web search + content extraction; relevance: Perplexity search returns extracted web content.
- [hermes_tool_search](../hermes_agent/hermes_tool_search.md) — search-as-a-tool wiring; relevance: how a web-search provider surfaces as an agent tool.
- [hermes_x_search_grok](../hermes_agent/hermes_x_search_grok.md) — another web-search provider (Grok/X); relevance: sibling web-search provider sharing the same contract.
- [hermes_integrations_overview](../hermes_agent/hermes_integrations_overview.md) — overview of provider/tool integrations; relevance: situates web-search providers in the integration set.
- [hermes_toolsets_reference](../hermes_agent/hermes_toolsets_reference.md) — toolset reference incl. search tools; relevance: lists the web-search tool a perplexity provider backs.
- [oc_plugins_reference_qa_lab](oc_plugins_reference_qa_lab.md) — sibling card (planned, this series); relevance: qa-lab also declares the `webSearchProviders` contract.
- [oc_plugins_reference_openrouter](oc_plugins_reference_openrouter.md) — sibling provider-plugin card (planned, this series); relevance: same provider-plugin registration pattern.
- [oc_tools_perplexity_search (to06)](../openclaw/oc_tools_perplexity_search.md) — the fuller Related-docs target (planned, to06); relevance: this card's `## Related docs` links tools/perplexity-search.
- [oc_providers_perplexity_provider (pr07)](../openclaw/oc_providers_perplexity_provider.md) — provider page (planned, pr07); relevance: the provider-side companion of the search tool.

**Repos** (3)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins; relevance: home of the perplexity-plugin package.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agent runtime; relevance: agents call the web-search provider this plugin registers.
- [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — Hermes plugin implementations; relevance: sibling-ecosystem web-search provider plugin reference.

**Snippets** (10)
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web/search plugin implementation; relevance: the web-search provider-plugin pattern this card declares.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool implementations; relevance: search tools backed by a web-search provider.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: how the search tool/contract registers.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: how a `webSearchProviders` contract is registered.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: loads and dispatches the web-search provider.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: perplexity is a custom-provider contribution.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK surface a provider plugin uses.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the Distribution/Surface declaration this card mirrors.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package→contract binding; relevance: maps `@openclaw/perplexity-plugin` to its contract.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — a provider-registration example; relevance: provider-registration pattern reused by the search provider.

### oc_plugins_reference_pixverse (8t · 10s · 10d)

**Terms** (8)
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative model class for image/video; relevance: PixVerse generates video via diffusion-style models.
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning text/image/video; relevance: text/image-to-video is a multimodal task.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video generation/transformation; relevance: PixVerse's contract is `videoGenerationProviders`.
- [Generative Model](../../term_dictionary/term_generative_model.md) — models that synthesize new content; relevance: a video-generation provider is a generative model service.
- [Stable Diffusion](../../term_dictionary/term_stable_diffusion.md) — diffusion image/video generator; relevance: the diffusion lineage PixVerse video gen builds on.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin contributing a provider contract; relevance: `@openclaw/pixverse-provider` contributes `videoGenerationProviders`.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted generative APIs; relevance: PixVerse is a third-party video-gen API.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — large pretrained generative backbone; relevance: PixVerse's video model is a hosted foundation model.

**Docs** (10; 6 existing + 4 planned/sibling)
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — the video-generation provider plugin contract; relevance: documents the exact `videoGenerationProviders` surface this card declares.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider plugin; relevance: sibling media-generation provider contract.
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — image generation feature/usage; relevance: image-to-video is the input modality for PixVerse.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — media tool reference; relevance: video-gen surfaces as a media tool.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin registration; relevance: pixverse follows the provider-plugin pattern.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled plugin catalog; relevance: lists media provider plugins like pixverse.
- [oc_plugins_reference_openrouter](oc_plugins_reference_openrouter.md) — sibling card (planned, this series); relevance: openrouter also exposes `videoGenerationProviders`.
- [oc_plugins_reference_perplexity](oc_plugins_reference_perplexity.md) — sibling provider-plugin card (planned, this series); relevance: same provider-plugin registration pattern.
- [oc_providers_pixverse (pr07)](../openclaw/oc_providers_pixverse.md) — the fuller Related-docs target (planned, pr07); relevance: this card's `## Related docs` links providers/pixverse.
- [oc_tools_video_generation (to08)](../openclaw/oc_tools_video_generation.md) — video-generation tool page (planned, to08); relevance: the tool the videoGenerationProviders contract backs.

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — OpenClaw provider extensions; relevance: home of the pixverse-provider package.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions; relevance: parent of the bundled media-provider plugins.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapter implementations; relevance: video-gen provider adapter pattern.

**Snippets** (10)
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-generation tool; relevance: the tool a `videoGenerationProviders` contract backs.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: how the pixverse provider is invoked.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool; relevance: image-to-video input pipeline.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch; relevance: sibling media-provider dispatch pattern.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision/media dispatch; relevance: media-generation routing the provider participates in.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: how the video-gen contract registers.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: loads/dispatches the pixverse provider.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider example; relevance: provider-registration pattern a media provider follows.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package→contract binding; relevance: maps `@openclaw/pixverse-provider` to its contract.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the Distribution/Surface declaration this card mirrors.

### oc_plugins_reference_policy (10t · 12s · 10d)

**Terms** (10)
- [Policy](../../term_dictionary/term_policy.md) — authored rules governing system behavior; relevance: the plugin is named "Policy" and stores rules in `policy.jsonc`.
- [Policy Engine / Governance](../../term_dictionary/term_policy_engine_governance.md) — engine that evaluates governance policy; relevance: the doctor check is a policy-conformance engine over governed workspace declarations.
- [Health Check](../../term_dictionary/term_health_check.md) — automated system-health probe; relevance: Policy contributes "doctor health checks" for conformance.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny security posture; relevance: tool/sandbox posture rules can require deny entries and disabled elevated mode.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — escalating trust/approval levels; relevance: tool posture rules require approved profiles and bounded exec ask settings.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of governed tools; relevance: tool posture rules verify governed tool metadata and `alsoAllow`/deny entries.
- [Access Control](../../term_dictionary/term_access_control.md) — who/what may access a resource; relevance: ingress/channel access posture is a Policy rule family.
- [Data Governance](../../term_dictionary/term_data_governance.md) — controls over data handling/retention; relevance: data-handling posture (redaction, retention, memory indexing) is a Policy family.
- [Data Handling](../../term_dictionary/term_data_handling.md) — rules for processing sensitive data; relevance: directly named — "data-handling posture" rules.
- [Threat Model](../../term_dictionary/term_threat_model.md) — enumeration of attack surfaces/mitigations; relevance: posture families map to the OpenClaw gateway/sandbox/secret threat surfaces.

**Docs** (10; 7 existing + 3 planned/sibling)
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin-enforced policy/config controls; relevance: closest analog to Policy's config-conformance enforcement.
- [cc_sandbox_org_enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org-level sandbox policy enforcement; relevance: parallels Policy's sandbox posture rules.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission/tool policy; relevance: matches Policy's tool-posture vs sandbox-posture split.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — a security/guidance plugin; relevance: sibling security-posture plugin pattern.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — managed plugin policy settings; relevance: config-level plugin policy, mirroring `policy.jsonc`.
- [hermes_managed_scope](../hermes_agent/hermes_managed_scope.md) — managed/scoped policy in a sibling agent; relevance: matches Policy's named `scopes.<scopeName>` selectors.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation + credential/secret posture; relevance: Policy covers secret provider/auth-profile posture.
- [oc_plugins_reference_openshell](oc_plugins_reference_openshell.md) — sibling card (planned, this series); relevance: Policy's sandbox posture rules govern approved sandbox backends like OpenShell.
- [oc_cli_policy (cl06)](../openclaw/oc_cli_policy.md) — the fuller Related-docs target (planned, cl06); relevance: this card's `## Related docs` links cli/policy (`openclaw policy check`/`compare`).
- [oc_gateway_security (gw06)](../openclaw/oc_gateway_security.md) — gateway security page (planned, gw06); relevance: Gateway exposure posture is a Policy rule family.

**Repos** (4)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security/audit code; relevance: home of the policy/doctor-check and posture-audit implementation.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: Gateway exposure posture rules check gateway config.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agent runtime; relevance: agent workspace/tool posture rules check agent declarations.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the Policy plugin is bundled ("included in OpenClaw").

**Snippets** (12)
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composes audit/doctor checks; relevance: the audit-composition path behind `openclaw policy check`.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation of audit findings; relevance: how reported drift/findings are remediated.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — agent tool-policy evaluation; relevance: implements the tool posture rules.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: workspace-only filesystem + bounded exec posture rules.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny dangerous tools; relevance: required tool deny entries posture rule.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: plugin-posture conformance the doctor check evaluates.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — emits policy findings; relevance: the "policy, evidence, findings, attestation hashes" output.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime posture audit; relevance: configured sandbox-runtime posture checks.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source posture audit; relevance: ingress/channel access posture rule.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — gateway node command policy; relevance: Gateway exposure posture enforcement.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval policy; relevance: sibling approved-profile/approval posture model.
- [snippet_hermes_agent_cli_tools_policy](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — CLI tools-policy config; relevance: parallel config-level tool-posture declaration.

### oc_plugins_reference_qa_channel (8t · 10s · 10d)

**Terms** (8)
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — core dispatch loop for channel messages; relevance: a qa-channel surface plugs into the channel kernel to send/receive messages.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway bridging chat platforms to agents; relevance: qa-channel is a channel surface the messaging gateway routes.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex socket protocol; relevance: OpenClaw channel surfaces transport messages over WebSocket.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC over JSON; relevance: channel/agent message exchange uses JSON-RPC framing.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: OpenClaw channel/tool surfaces interoperate with MCP.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client message protocol; relevance: the protocol carrying messages across an OpenClaw channel.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway/agent platform; relevance: qa-channel sends/receives OpenClaw messages.
- [Pub/Sub](../../term_dictionary/term_pub_sub.md) — publish/subscribe messaging; relevance: channel surfaces fan messages to subscribers in test scenarios.

**Docs** (10; 7 existing + 3 planned/sibling)
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how to add a channel/platform adapter plugin; relevance: qa-channel IS such a channel adapter plugin.
- [hermes_adding_platform_adapter_builtin](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — built-in platform adapter pattern; relevance: parallel channel-surface registration.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging gateway architecture; relevance: where a channel surface fits in message routing.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: how channels are dispatched inside the gateway.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: classifies the channel surface this plugin contributes.
- [band_sdk_overview](../band/band_sdk_overview.md) — channel SDK overview (sibling platform); relevance: parallel channel-plugin SDK model.
- [band_websocket_overview](../band/band_websocket_overview.md) — WebSocket channel transport; relevance: the transport an OpenClaw channel surface uses.
- [oc_plugins_reference_qa_lab](oc_plugins_reference_qa_lab.md) — sibling card (planned, this series); relevance: companion QA tooling that exercises channel scenarios.
- [oc_channels_qa_channel (ch04)](../openclaw/oc_channels_qa_channel.md) — the fuller Related-docs target (planned, ch04); relevance: this card's `## Related docs` links channels/qa-channel.
- [oc_concepts_channel_docking (co01)](../openclaw/oc_concepts_channel_docking.md) — channel-docking concept (planned, co01); relevance: explains how channel surfaces dock to the kernel.

**Repos** (4)
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — OpenClaw channels code; relevance: home of channel-surface implementations like qa-channel.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: the send/receive message plumbing a qa-channel uses.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: routes channel messages to/from agents.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: qa-channel is a source-checkout-only plugin in the tree.

**Snippets** (10)
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel-adapter contract; relevance: exactly the contract a qa-channel surface implements.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: how qa-channel messages are dispatched.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable channel kernel state; relevance: message persistence for channel surfaces.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway channel WebSocket; relevance: the WS transport a channel surface uses.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy for sessions; relevance: governs sending OpenClaw messages over a channel.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound message runner; relevance: the send-side of a channel surface.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send/dispatch tool; relevance: how a message is dispatched to a channel.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: how a channel plugin registers its namespace.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/lifecycle; relevance: loading the source-checkout qa-channel plugin.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package→contract binding; relevance: maps `@openclaw/qa-channel` to its `channels` contract.

### oc_plugins_reference_qa_lab (8t · 10s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway/agent platform; relevance: qa-lab is an OpenClaw debugger UI + scenario runner.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that run autonomously; relevance: qa-lab's scenarios exercise OpenClaw coding agents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime executing agent tool calls; relevance: the scenario runner drives agents through the harness.
- [Evaluation Harness](../../term_dictionary/term_evaluation_harness.md) — framework for running/scoring agent runs; relevance: a scenario runner IS an evaluation harness.
- [Agentic Evaluation](../../term_dictionary/term_agentic_evaluation.md) — evaluating agent behavior end-to-end; relevance: qa-lab runs e2e agent scenarios for debugging.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: scenarios invoke the `webSearchProviders` contract via tool calls.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — query→documents retrieval; relevance: qa-lab declares a web-search provider contract used by scenarios. (`term_web_search` is MISSING.)
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: the web-search contract feeds retrieved context into scenario runs.

**Docs** (10; 6 existing + 4 planned/sibling)
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — debugger/dashboard UI overview; relevance: qa-lab is a private debugger UI of the same kind.
- [hermes_skills_catalog_bundled](../hermes_agent/hermes_skills_catalog_bundled.md) — bundled tooling catalog; relevance: situates qa-lab among OpenClaw dev/test tooling.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider contract; relevance: qa-lab declares this same `webSearchProviders` contract.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled/built-in plugin catalog; relevance: classifies qa-lab as a (source-checkout) plugin.
- [band_testing_agents](../band/band_testing_agents.md) — testing coding agents (sibling platform); relevance: parallel scenario/e2e agent-testing model.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — coding-agent deployment/runtime; relevance: the runtime qa-lab scenarios drive.
- [oc_plugins_reference_qa_channel](oc_plugins_reference_qa_channel.md) — sibling card (planned, this series); relevance: companion QA tooling (test channel surface).
- [oc_plugins_reference_perplexity](oc_plugins_reference_perplexity.md) — sibling card (planned, this series); relevance: both declare the `webSearchProviders` contract.
- [oc_concepts_qa_e2e_automation (co05)](../openclaw/oc_concepts_qa_e2e_automation.md) — QA e2e automation concept (planned, co05); relevance: the e2e-automation concept qa-lab implements.
- [oc_web_control_ui (wb01)](../openclaw/oc_web_control_ui.md) — web control UI page (planned, wb01); relevance: qa-lab's debugger UI is a web control surface.

**Repos** (4)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: qa-lab is a source-checkout-only plugin in the tree.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agent runtime; relevance: the agents qa-lab scenarios exercise.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills; relevance: scenarios test skill/tool execution paths.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions; relevance: the web-search provider contract qa-lab declares lives among extensions.

**Snippets** (10)
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch path; relevance: scenario-driver dispatch into the channel/agent kernel.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser/UI dispatch; relevance: the debugger-UI dispatch surface.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web/search plugin; relevance: the `webSearchProviders` contract qa-lab declares.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tools; relevance: search tools the scenarios call.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: how qa-lab's web-search contract registers.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: the tools scenarios exercise.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/lifecycle; relevance: loading the source-checkout qa-lab plugin.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how qa-lab declares its plugin entrypoints.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK surface qa-lab builds on.

**Series-wide floor satisfaction:** all 7 notes meet ≥8 terms · ≥10 snippets · ≥10 docs. Every cited term,
executing agent copies each `- [Name](relpath.md) — desc; relevance: …` line verbatim into the note's
`## Related Notes`; G5 ghost-detect re-runs over the final set (planned siblings resolve as they are created).

## Undigested Terms Plan

> Per master: OpenClaw plugin/provider/channel vocabulary is the *subject* of these reference pages, so it is
> digested as `oc_*` doc notes by THIS sub-plan, not promoted to `term_dictionary`. The only term_dictionary
> interaction is LINKING existing terms. Expected **0 new term captures**.

| Term (page) | Disposition |
|---|---|
| OpenRouter (openrouter) | `oc_*` doc concept (note 1); link `term_llm` / `term_model_router` / `term_third_party_genai_services`. NOT a new term. |
| OpenShell / NVIDIA OpenShell CLI (openshell) | `oc_*` doc concept (note 2); link `term_sandbox` / `term_ssh`. NOT a new term. |
| sandbox backend (openshell) | Link existing `term_sandbox`. |
| Perplexity (perplexity) | Link existing `term_perplexity` (verified present); `oc_*` doc concept (note 3). NOT a new term. |
| web search provider / `webSearchProviders` contract (perplexity, qa-lab) | `oc_*` doc concept; link `term_rag` / `term_information_retrieval`. `term_web_search` MISSING but is a plugin-contract name, not a reusable cross-cutting term → NO new capture. |
| PixVerse / video generation (pixverse) | `oc_*` doc concept (note 4); link `term_diffusion_model` / `term_multimodal`. `term_video_generation` MISSING but is a provider-contract name → NO new capture. |
| Policy plugin / `policy.jsonc` / posture rules / doctor check (policy) | `oc_*` doc concept (note 5); link `term_policy` / `term_health_check` / `term_access_control` / `term_data_governance`. NOT new terms. |
| attestation hash / config-conformance drift (policy) | Described inline in note 5 prose; link `term_policy`. `term_attestation` / `term_configuration_drift` MISSING — see new-term candidate below. |
| QA Channel / channel surface (qa-channel) | `oc_*` doc concept (note 6); link `term_websocket` / `term_openclaw`. NOT a new term. |
| QA Lab / scenario runner / debugger UI (qa-lab) | `oc_*` doc concept (note 7); link `term_openclaw` / `term_autonomous_coding_agents`. NOT a new term. |

**New-term candidates (for augment review, NOT auto-captured):** none are confidently warranted from this
sub-plan. `term_policy_as_code` (would generalize the policy plugin's "authored requirements in
`policy.jsonc`, observed evidence, drift reporting, attestation hash" model — a genuinely reusable
cross-cutting governance pattern with no existing home; best-fit glossary `acronym_glossary_security.md`,
verified present) is the single borderline candidate. **Recommended disposition: defer** — describe inline
in note 5 and link the existing `term_policy`; only capture if a second OpenClaw sub-plan (e.g. `gw06`
security, `cl06` cli/policy) independently needs the same term. Augment Step 2d re-confirms.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master; provider/
plugin vocabulary → `oc_*` doc notes, existing terms linked). If augment promotes the deferred
`term_policy_as_code` candidate, it MUST follow the master's W5 requirement: capture via
`acronym_glossary_security.md` — and that becomes a separate prerequisite of execution.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). All gates must PASS before commit.

| Gate | Check | Pass condition |
|---|---|---|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order + forbidden-field absence; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` + `## References` + bold footer present. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/plugins/reference/<page>.md`) | Every fact (package, install route, contracts, behavior) traces to the source page; no fabricated config. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one BB; every source H2/Behavior mapped (see Section Coverage Map). |
| G4 | Cross-Reference | RAISED FLOOR (xref-augment 2026-06-21): ≥8 relevance-selected term links · ≥10 code_snippets · ≥10 docs per note (PLUS sibling `oc_*`/`repo_openclaw*`), each with a relevance statement — per the locked `## Per-Note Related Notes Mapping`. |
| G5 | Ghost-reference detect + redirect | 0 links to non-existent notes; MISSING candidates flagged above are NOT cited. |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken relative paths after reindex. |
| G7 | Discoverability (outside-folder inbound) | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 (anti-island) | `note_links` confirms in-degree ≥1 per new note post-reindex. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_openrouter oc_plugins_reference_openshell oc_plugins_reference_perplexity oc_plugins_reference_pixverse oc_plugins_reference_policy oc_plugins_reference_qa_channel oc_plugins_reference_qa_lab"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  echo "$REQ_SECTIONS" | tr '|' '\n' | while read -r s; do
    grep -qF "$s" "$f" || echo "MISSING SECTION '$s' in $n"
  done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_ link (G4 discoverability within series)
  grep -qE "\(${SIBLING_PREFIX}[a-z0-9_]+\.md\)" "$f" || echo "NO SIBLING ${SIBLING_PREFIX} LINK in $n"
  # G3: density caps (body only, excluding YAML)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb cb / $lines L)"
done

# G1 YAML frontmatter sweep over the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference: every (link.md) target must resolve to a real note in the DB
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"; [ -f "$f" ] || continue
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/^\]\(//; s/\)$//' | while read -r tgt; do
    base=$(basename "$tgt")
    [ -z "$hit" ] && echo "GHOST in $n -> $tgt"
  done
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_openrouter | model | 220 | 0 | ✅ |
| 2 | oc_plugins_reference_openshell | model | 230 | 0 | ✅ |
| 3 | oc_plugins_reference_perplexity | model | 210 | 0 | ✅ |
| 4 | oc_plugins_reference_pixverse | model | 210 | 0 | ✅ |
| 5 | oc_plugins_reference_policy | concept | 520 | 0 | ✅ |
| 6 | oc_plugins_reference_qa_channel | model | 200 | 0 | ✅ |
| 7 | oc_plugins_reference_qa_lab | model | 200 | 0 | ✅ |

No note approaches any cap (max 520w vs 2,500; 0 code blocks vs 6; well under 400 lines). Source has 0 code
fences, so digest notes carry no reproduced code (a short package/contract identifier may appear inline as
backticked text, not a fenced block). No borderline-density page → no split promotion needed.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step; >30-note series ⇒
required) under the **Plugins → Reference** cluster (alongside pl01–pl25). Each new note RECEIVES its inbound
back-link from `entry_openclaw_docs.md` at finalization (satisfies G7/G8). No new entry point is created by
this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all sources verified present
2026-06-20):

- `entry_openclaw_docs.md` → all 7 notes (master W1; primary anti-island guarantee).
- `repo_openclaw_extensions_llm_providers` → notes 1 (openrouter), 4 (pixverse).
- `repo_openclaw_security` → notes 2 (openshell), 5 (policy).
- `repo_openclaw_channels` / `repo_openclaw_channels_messaging` → note 6 (qa-channel).
- `repo_openclaw_extensions` → notes 3 (perplexity), 7 (qa-lab).
- `term_perplexity` → note 3 (perplexity).
- `term_policy` → note 5 (policy).
- `term_sandbox` → note 2 (openshell); `term_llm` / `term_model_router` → note 1 (openrouter).
- Existing snippets reciprocate: `snippet_openclaw_security_openshell_backend` → note 2;
  `snippet_openclaw_provider_openrouter_aggregator` → note 1;
  `snippet_openclaw_security_audit_composition` → note 5.

## Pacing Rules (inherited from master)

One execution phase (7 notes ≤ fan-out cap). 8 gates pass before commit. Re-read each source page during
execution (Step 1); reproduce package/contract identifiers verbatim. One BB per note. Reindex incrementally;
verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash` first; no
Claude co-author trailer; commit + push in the same turn.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors ≥8t/≥10s/≥10d) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augmentation:** per-note Related Notes mapping locked at RAISED FLOORS — **≥8
`term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/` per note**,
relevance-selected from a fresh re-read of all 7 source pages under
replaced by `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. G4 gate row and Summary
Statistics cross-ref line were updated to the raised floors.

**What was locked (per note):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_openrouter | 8 | 11 | 10 (6/4) | 4 | YES |
| oc_plugins_reference_openshell | 8 | 11 | 10 (7/3) | 4 | YES |
| oc_plugins_reference_perplexity | 8 | 10 | 10 (6/4) | 3 | YES |
| oc_plugins_reference_pixverse | 8 | 10 | 10 (6/4) | 3 | YES |
| oc_plugins_reference_policy | 10 | 12 | 10 (7/3) | 4 | YES |
| oc_plugins_reference_qa_channel | 8 | 10 | 10 (7/3) | 4 | YES |
| oc_plugins_reference_qa_lab | 8 | 10 | 10 (6/4) | 4 | YES |

sibling `oc_*` / cross-cluster planned pages (pr06, pr07, to06, to08, cl06, gw04, gw05, gw06, ch04, co01,

**Terms confirmed MISSING and NOT cited** (plugin-contract names, not reusable cross-cutting vault terms):
`term_web_search`, `term_openrouter`, `term_video_generation`, `term_text_to_video`, `term_generative_ai`,
`term_nvidia`, `term_npm`, `term_docker`, `term_channel`, `term_message_bus`, `term_policy_as_code`,
`term_attestation`, `term_configuration_drift`, `term_compliance`, `term_governance`. Where a missing
contract-name term was needed for coverage, a verified semantic neighbor was substituted with an explicit
relevance note (e.g. `term_information_retrieval` in place of `term_web_search`; `term_video_processing`
in place of `term_video_generation`).

**Notable finds vs the draft Candidate section:** the draft marked several terms TBD/uncertain that are in
fact PRESENT and were locked in — `term_openshell`, `term_sandbox_backend`, `term_channel_kernel`,
`term_messaging_gateway`, `term_policy_engine_governance`, `term_deny_first`, `term_graduated_trust`,
`term_tool_registry`, `term_evaluation_harness`, `term_agentic_evaluation`. The draft's note 3 worry that
"no perplexity snippet exists" is moot under the raised floor: 10 web-search/provider-registry/plugin-SDK
snippets cover the contract this card declares.

**New-term candidates (for review, NOT auto-captured):** none warranted from this sub-plan. `term_policy_as_code`
remains the single borderline candidate (would generalize the policy plugin's authored-requirements +
observed-evidence + drift-reporting + attestation-hash model). **Disposition: DEFER** — described inline in
note 5 and linked to the existing `term_policy` + `term_policy_engine_governance`; best-fit glossary if ever
captured is `acronym_glossary_security.md` (DB-verify at capture time). Capture only if a second OpenClaw
sub-plan (gw06 security or cl06 cli/policy) independently needs the same term. This matches the master's
expected-0-new-terms design (OpenClaw vocabulary is digested as `oc_*` doc notes, not promoted to
term_dictionary).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_pl17.md
Date: 2026-06-21
```

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance stmts) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (policy=10), ≥10 snippets, ≥10 docs; each link rendered `- [Name](relpath.md) — desc; relevance: …` (no bare links). RAISED floors exceed the master's ≥6-term floor. |
| CP2 | 9-GATE table present (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Ref (raised floor), G5 Ghost, G6 Broken-link, G7 Discoverability, G8 in-degree. G5/G6/G8 all present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 7 rows to `entry_openclaw_docs.md` (created as master W1 pre-step; >30-note series ⇒ required); each note RECEIVES its inbound back-link there (G7/G8). No new entry point created by this sub-plan. |
| CP4 | Size (≤30 or split) | **PASS** | 7 planned notes ≤ 30; single execution phase within fan-out cap. |
| CP5 | Format derived (from cc_/pi_/hermes_ doc corpus) | **PASS** | YAML field order + `# OpenClaw — …` H1 + `## Overview`/`## Related Notes`/`## References` + bold footer inherited verbatim from master Format Definition, which was derived from existing `claude_code/` + `pi/` doc notes (not invented). G1 row enforces it. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment table: max 520w (policy) vs 2,500w cap; 0 code blocks vs 6; all ≪ 400 lines. No borderline note; no split promotion needed. |
| CP7 | Sources measured (not guessed) | **PASS** | Source table measured 2026-06-20 (total 801w); re-read 2026-06-21 confirmed byte sizes (openrouter 579B, openshell 480B, perplexity 448B, pixverse 477B, policy 3512B, qa-channel 475B, qa-lab 405B) — consistent with the ≤65w stubs + 451w policy estimates (policy Behavior block lines 23–73 read in full). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new captures; existing terms linked) + `## Term-Note Authoring Requirements` (N/A 0 terms, with the master W5 fallback if `term_policy_as_code` is ever promoted via `/tessellum-capture-term-note` + glossary). Must-language present. |
| CP8f | Slug/collision audit | **PASS** | All 7 planned `oc_*` slugs are documentation-concept notes (no `term_*` slugs created). Collision audit: synonym search across `term_dictionary/` AND `documentation/` found NO substantive existing note duplicating a planned `oc_plugins_reference_*` card (0 existing `oc_` docs in DB confirmed). Filename normalization (`/`,`-` → `_`) documented. No duplicate/too-general slug. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` table gives each of the 7 notes ≥1 outside-folder inbound source (`entry_openclaw_docs.md` for all 7; plus repo/term/snippet reciprocals per note); G8 in-degree check is in the phase gate table and is an EXECUTED phase, not "recommended". |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
