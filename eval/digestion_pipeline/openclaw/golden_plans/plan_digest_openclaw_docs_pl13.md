---
title: "Sub-Plan pl13 — OpenClaw Docs: Plugins (reference — litellm, llama-cpp, llm-task, lmstudio, lobster, matrix, mattermost)"
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - plugins/reference/litellm
  - plugins/reference/llama-cpp
  - plugins/reference/llm-task
  - plugins/reference/lmstudio
  - plugins/reference/lobster
  - plugins/reference/matrix
  - plugins/reference/mattermost
---

# Sub-Plan pl13: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup-before-create, 9-GATE validation, undigested-terms ownership, cross-refs, and entry-point wiring are ALL inherited from the master.
> The 7 assigned pages are micro-stub plugin-inventory cards (`## Distribution` / `## Surface` / `## Related docs`, 51–62 words, 0 code each); per the atomicity + density rules they consolidate by capability-contract/BB cluster into 3 `oc_` procedure notes, not 1-per-page.

## Scope

The 7 alphabetically-contiguous `plugins/reference/*` inventory cards for the `l*`/`m*` plugins, which fall into three capability clusters: (1) **model / embedding providers** — `litellm` (LiteLLM model-provider proxy aggregator), `llama-cpp` (local GGUF embeddings via node-llama-cpp), `lmstudio` (LM Studio local model + embedding provider); (2) **workflow / structured-task tools** — `llm-task` (generic JSON-only LLM tool callable from workflows), `lobster` (typed-pipeline workflow tool with resumable approvals); (3) **chat channels** — `matrix` (Matrix rooms + DMs), `mattermost` (Mattermost send/receive surface). Each card states only the npm package name, install route (included-in-OpenClaw vs `npm`/ClawHub vs `clawhub:@openclaw/...`), the capability surface it registers (`providers:` / `channels:` / `contracts:`), and (for 5 of 7) a `## Related docs` pointer to the corresponding `providers/*`, `channels/*`, or `plugins/*` deep-dive page (out of this sub-plan's scope — owned by `pr05`, `pl03`, `ch03`, `to04`).

Priority **P3** (Phase C — plugin-reference sprawl). These cards are thin "what package provides what capability" inventory entries; their durable value is the npm-package ↔ capability-surface ↔ deep-dive-page mapping, not conceptual depth. The substantive OpenClaw code-side notes (`repo_openclaw_extensions`, `repo_openclaw_extensions_llm_providers`, `repo_openclaw_memory`, `repo_openclaw_skills`, `repo_openclaw_channels`, `repo_openclaw_channels_messaging`) and the existing `digest_lobster_dsl_openclaw` digest are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 398 measured words. **Planned: 3 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| LiteLLM plugin | plugins/reference/litellm | 56 | 0 | 3 | 0 | procedure |
| Llama Cpp plugin | plugins/reference/llama-cpp | 51 | 0 | 3 | 0 | procedure |
| LLM Task plugin | plugins/reference/llm-task | 57 | 0 | 2 | 0 | procedure |
| LM Studio plugin | plugins/reference/lmstudio | 60 | 0 | 3 | 0 | procedure |
| Lobster plugin | plugins/reference/lobster | 54 | 0 | 2 | 0 | procedure |
| Matrix plugin | plugins/reference/matrix | 58 | 0 | 3 | 0 | procedure |
| Mattermost plugin | plugins/reference/mattermost | 62 | 0 | 3 | 0 | procedure |

Totals: 398 words, 0 code fences, 19 H2 (the identical `## Distribution` + `## Surface` on all 7, plus `## Related docs` on 5 of 7 — `llm-task` and `lobster` have no `## Related docs`), 0 H3. All BBs are procedure (install/enable/configure a plugin to register a capability surface).

## Content Strategy

- **Prioritize**: the npm-package → capability-surface → deep-dive-page mapping (the only durable content), the install-route distinction (included-in-OpenClaw vs `npm` vs `clawhub:@openclaw/...`), and the capability-contract id each plugin registers (`providers:` / `channels:` / the `contracts:` list — `imageGenerationProviders`, `embeddingProviders`, `memoryEmbeddingProviders`, `tools`). These are what a user/operator actually needs from a plugin-inventory card.
- **Consolidate (not split)**: each page is a 51–62-word micro-stub — far below the 1-note atomic floor on its own. Grouping by capability cluster keeps each note a focused, single-BB "how to enable this class of `l*`/`m*` plugin" procedure while staying well under all density caps (3 notes × ≤300w). One note per page would create 7 near-empty notes that fail the substantive-content bar and bloat the graph (the same consolidation decision pl11 made for its 7 `g*` cards).
- **Link-out (owned elsewhere)**: each card's `## Related docs` pointer — `/providers/litellm` (litellm), `/plugins/llama-cpp` (llama-cpp), `/providers/lmstudio` (lmstudio), `/channels/matrix` (matrix), `/channels/mattermost` (mattermost) — is the deep-dive page for that integration, owned by other sub-plans (`pr05` for litellm + lmstudio; `pl03` for the `plugins/llama-cpp` deep-dive; `ch03` for matrix + mattermost). `llm-task` and `lobster` carry no `## Related docs` (their deep-dives are `tools/llm-task` and `tools/lobster`, owned by `to04`). This sub-plan links those as `## References` / sibling pointers and does NOT duplicate their config detail. Provider/channel/tool vocabulary links existing `term_*` notes; nothing is redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_lm_model_providers.md` | procedure | litellm.md, llama-cpp.md, lmstudio.md (all H2 each) | 290 | The three `l*` model / embedding provider plugins: LiteLLM (`@openclaw/litellm-provider`, included in OpenClaw; `providers: litellm` + `imageGenerationProviders` contract — an aggregator proxy fronting many upstream models), Llama Cpp (`@openclaw/llama-cpp-provider`, npm/ClawHub; `embeddingProviders` contract — local GGUF embeddings via node-llama-cpp), and LM Studio (`@openclaw/lmstudio-provider`, included in OpenClaw; `providers: lmstudio` + `memoryEmbeddingProviders` contract — local desktop model + memory-embedding provider). Per-plugin package, install route, registered `providers:`/`contracts:` ids, and pointer to the provider deep-dive. |
| 2 | `oc_plugins_reference_lm_workflow_tools.md` | procedure | llm-task.md, lobster.md (all H2 each) | 230 | The two `l*` workflow / structured-task tool plugins: LLM Task (`@openclaw/llm-task`, included in OpenClaw; `contracts: tools` — a generic JSON-only LLM tool callable from workflows for structured tasks) and Lobster (`@openclaw/lobster`, npm/ClawHub; `contracts: tools` — a workflow tool for typed pipelines with resumable approvals). Per-plugin package, install route, the `tools` contract they register, and the workflow/structured-output use case. |
| 3 | `oc_plugins_reference_matrix_mattermost_channels.md` | procedure | matrix.md, mattermost.md (all H2 each) | 230 | The two `m*` chat channel plugins: Matrix (`@openclaw/matrix`, ClawHub: `clawhub:@openclaw/matrix` / npm; `channels: matrix` — rooms and direct messages) and Mattermost (`@openclaw/mattermost`, included in OpenClaw; `channels: mattermost` — send/receive OpenClaw messages on a Mattermost workspace). Per-plugin package, install route, the `channels:` surface each registers, and pointer to the channel deep-dive. |

Filename convention: `oc_` + full slug with `/` and `-` → `_`. None of the 3 notes maps 1:1 to a single page slug (each is a consolidation of same-class siblings), so each takes a descriptive grouped slug marking the capability cluster (`lm_model_providers`, `lm_workflow_tools`, `matrix_mattermost_channels`) rather than any one page slug, exactly as pl11's note 1 grouped four `g*` provider cards under `oc_plugins_reference_g_model_providers`. See Split Decisions.

## Section Coverage Map

```
plugins/reference/litellm.md
├── Distribution (pkg @openclaw/litellm-provider, included in OpenClaw) ──── note 1
├── Surface (providers: litellm; contracts: imageGenerationProviders) ───── note 1
└── Related docs (/providers/litellm) ─────────────────────────────────── note 1 (References pointer; pr05)
plugins/reference/llama-cpp.md
├── Distribution (pkg @openclaw/llama-cpp-provider, npm / ClawHub) ──────── note 1
├── Surface (contracts: embeddingProviders) ───────────────────────────── note 1
└── Related docs (/plugins/llama-cpp) ─────────────────────────────────── note 1 (References pointer; pl03)
plugins/reference/lmstudio.md
├── Distribution (pkg @openclaw/lmstudio-provider, included in OpenClaw) ── note 1
├── Surface (providers: lmstudio; contracts: memoryEmbeddingProviders) ─── note 1
└── Related docs (/providers/lmstudio) ────────────────────────────────── note 1 (References pointer; pr05)
plugins/reference/llm-task.md
├── Distribution (pkg @openclaw/llm-task, included in OpenClaw) ────────── note 2
└── Surface (contracts: tools) ────────────────────────────────────────── note 2
plugins/reference/lobster.md
├── Distribution (pkg @openclaw/lobster, npm / ClawHub) ────────────────── note 2
└── Surface (contracts: tools) ────────────────────────────────────────── note 2
plugins/reference/matrix.md
├── Distribution (pkg @openclaw/matrix, ClawHub clawhub:@openclaw/matrix / npm) note 3
├── Surface (channels: matrix) ────────────────────────────────────────── note 3
└── Related docs (/channels/matrix) ───────────────────────────────────── note 3 (References pointer; ch03)
plugins/reference/mattermost.md
├── Distribution (pkg @openclaw/mattermost, included in OpenClaw) ──────── note 3
├── Surface (channels: mattermost) ────────────────────────────────────── note 3
└── Related docs (/channels/mattermost) ───────────────────────────────── note 3 (References pointer; ch03)
```

No orphaned sections: every H2 of every page maps to a planned note (19 H2 total — `## Distribution` ×7, `## Surface` ×7, `## Related docs` ×5). Each card's `## Related docs` pointer is preserved as a `## References` external link (the deep-dive page is owned by `pr05`/`pl03`/`ch03`/`to04`, not duplicated here). `llm-task` and `lobster` have no `## Related docs` H2; their deep-dive (`tools/llm-task`, `tools/lobster`) is referenced contextually.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| litellm.md + llama-cpp.md + lmstudio.md (56+51+60 = 167w combined) | **CONSOLIDATED into note 1** | Three micro-stubs of the same BB (procedure) and same capability cluster (model/embedding providers — `providers:`/`embeddingProviders`/`memoryEmbeddingProviders`/`imageGenerationProviders`) — each below the atomic floor alone; one focused "`l*` model/embedding provider plugins" note (~290w) is the correct atomic unit and stays far under all caps. NOT a split — a consolidation. |
| llm-task.md + lobster.md (57+54 = 111w combined) | **CONSOLIDATED into note 2** | Two micro-stubs, same BB (procedure), same capability contract (`contracts: tools`) and same use case (structured-task / workflow tool callable from agent workflows). Consolidated into one "`l*` workflow tool plugins" note (~230w). |
| matrix.md + mattermost.md (58+62 = 120w combined) | **CONSOLIDATED into note 3** | Two micro-stubs, same BB (procedure), same capability class (`channels:` chat surface). Consolidated into one "Matrix + Mattermost channel plugins" note (~230w). |

No page exceeds 2,500 words or mixes BBs, so no word-cap or mixed-BB *split* is needed. The only structural decisions are the inverse — consolidating same-class micro-stubs into 3 cluster notes (the same approach as pl11 / pl12).

## Summary Statistics & Building Block Distribution

- Source pages: 7 (398 words total). New `oc_` notes: **3**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×3 (notes 1–3). No concept/model/argument notes (these are install/enable cards).
- Est. digest words ~750 (avg ~250/note); max note ~290w. 0 source code fences → 0 code blocks in any note (well under the ≤6 cap; package names / contract ids rendered inline as `code`).
- Density: every note ≤290 words, ≤400 lines, 0 code blocks, single BB — no note approaches any cap. The real risk is the *opposite* (under-thin), addressed by the cluster consolidation + Overview context + cross-reference web.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`; digests `../../digest/digest_Y.md`; repos `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`.

### oc_plugins_reference_lm_model_providers (10t · 12s · 12d)

**Terms (10):**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model/embedding provider via the `providers:`/`contracts:` surface; relevance: the exact registration shape all three (`litellm`, `llama-cpp`, `lmstudio`) follow.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the models LiteLLM proxies and LM Studio serves locally.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted model providers; relevance: LiteLLM is an aggregator proxy fronting many upstream third-party providers.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the registry of available models OpenClaw can route to; relevance: LiteLLM/LM Studio plugins expand the catalog with their model entries.
- [Embedding](../../term_dictionary/term_embedding.md) — vector representation of text; relevance: llama-cpp registers `embeddingProviders` and lmstudio `memoryEmbeddingProviders`.
- [Vector Database](../../term_dictionary/term_vector_database.md) — store for embedding vectors; relevance: the destination for the embeddings these provider plugins generate (memory subsystem).
- [Quantization](../../term_dictionary/term_quantization.md) — reducing model weight precision; relevance: llama-cpp serves quantized GGUF local weights via node-llama-cpp.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: llama-cpp's install route is `npm`/ClawHub (vs included-in-OpenClaw for litellm/lmstudio).
- [Model Router](../../term_dictionary/term_model_router.md) — routes a request to the right model/provider; relevance: LiteLLM-as-aggregator is a routing/proxy layer in front of upstream models.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — backup model provider on primary failure; relevance: provider-plugin aggregators like LiteLLM are the layer that fallback ladders route across.
- (also linkable as host context: [OpenClaw](../../term_dictionary/term_openclaw.md), [MCP](../../term_dictionary/term_mcp.md) — provider-as-capability framing.)

**Docs (12 under documentation/; 11 existing + 1 planned sibling — plus 2 planned-this-series deep-dive pointers `pr05`/`pl03` not yet resolvable):**
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes' provider-plugin authoring doc; relevance: the closest structural twin to "how a model-provider plugin registers a `providers:` surface".
- [Hermes — Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud model-provider catalog; relevance: LiteLLM proxies exactly this class of cloud providers.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — step-by-step add-a-provider; relevance: the install/enable procedure these three cards summarize.
- [Hermes — Ollama Local Provider](../hermes_agent/hermes_provider_ollama_local.md) — local model provider setup; relevance: closest local-provider analog for llama-cpp/lmstudio.
- [Hermes — Local Self-Hosted LLM](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted model serving; relevance: the local-inference context llama-cpp/lmstudio operate in.
- [Hermes — Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider failover config; relevance: provider plugins are the units a fallback ladder selects across.
- [Hermes — Memory Provider Plugin](../hermes_agent/hermes_memory_provider_plugin.md) — authoring a memory/embedding provider plugin; relevance: the direct twin for llama-cpp's `embeddingProviders` and lmstudio's `memoryEmbeddingProviders` registration.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — the model-catalog schema/reference; relevance: where the models a litellm/lmstudio provider plugin registers actually land and get routed.
- [PI — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom model provider in PI; relevance: the pi-corpus analog of the exact `providers:` registration shape all three cards follow.
- [PI — Cloud Providers](../pi/pi_cloud_providers.md) — PI's cloud-provider list; relevance: the LiteLLM-aggregated provider class in the pi corpus.
- [Claude Code — LiteLLM Gateway](../claude_code/cc_llm_gateway_litellm.md) — using LiteLLM as a gateway in Claude Code; relevance: the exact LiteLLM analog elsewhere in the doc corpus.
- [OpenClaw — Workflow Tool Plugins](oc_plugins_reference_lm_workflow_tools.md) (planned, this series) — sibling `l*` plugin card (tool class); relevance: same plugin-inventory series, different contract class.
- [OpenClaw — LiteLLM/LM Studio Providers](pr05) (planned, this series — `pr05`) — the provider deep-dive for litellm + lmstudio; relevance: the `## Related docs` pointer each card carries.
- [OpenClaw — llama-cpp Plugin Deep-Dive](pl03) (planned, this series — `pl03`) — the `plugins/llama-cpp` deep-dive; relevance: llama-cpp's `## Related docs` pointer.

**Repos (additional):**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the provider-plugin package family; relevance: the codebase litellm/llama-cpp/lmstudio ship in.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — embedding/memory subsystem; relevance: consumes the `embeddingProviders`/`memoryEmbeddingProviders` these register.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: loads these provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — host repo; relevance: the product the plugins extend.

**Snippets (12):**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local-provider config; relevance: config twin for llama-cpp/lmstudio local serving.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: the OpenAI-compatible shape LiteLLM exposes to OpenClaw.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator-proxy provider impl; relevance: the aggregator pattern LiteLLM embodies (proxy fronting many models).
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a concrete provider plugin; relevance: sibling provider-plugin registration to study alongside litellm/lmstudio.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: where provider-registered models land.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery/normalize; relevance: how a provider plugin's models get discovered into the catalog.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host embedding generation; relevance: the consumer of llama-cpp/lmstudio `embeddingProviders`.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding input prep; relevance: the memory-embedding path these providers feed.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — LiteLLM/OpenRouter pricing lookup; relevance: the exact LiteLLM aggregator pricing code.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — provider/model fallback ladder; relevance: how provider plugins participate in failover routing.
- [snippet_hermes_agent_core_lmstudio_reasoning](../../code_snippets/snippet_hermes_agent_core_lmstudio_reasoning.md) — LM Studio reasoning handling; relevance: the exact LM Studio provider integration in the hermes corpus.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how a provider plugin declares its package entry.

### oc_plugins_reference_lm_workflow_tools (10t · 12s · 13d)

**Terms (10):**
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: the `tools` contract both plugins register exists to be function-called from workflows.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the registry of callable agent tools; relevance: where `contracts: tools` plugins land.
- [Structured Output](../../term_dictionary/term_structured_output.md) — schema-constrained model output; relevance: LLM Task is a JSON-only structured-task tool.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating multi-step work; relevance: Lobster is a typed-pipeline workflow tool.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step agent-driven process; relevance: both plugins are tools callable FROM agent workflows.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — human approval gate; relevance: Lobster supports resumable approvals.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-retry operations; relevance: Lobster's resumable/durable workflow steps.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — a built-in agent tool surface; relevance: sibling example of a `tools`-contract plugin to contrast against llm-task/lobster.
- [Agent as a Tool](../../term_dictionary/term_agent_as_a_tool.md) — wrapping an agent/task as a callable tool; relevance: llm-task is literally "an LLM task exposed as a tool".
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: Lobster's install route is `npm`/ClawHub (vs included-in-OpenClaw for llm-task).
- (also linkable as host context: [OpenClaw](../../term_dictionary/term_openclaw.md), [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — the plugin-registration shape.)

**Docs (12 under documentation/; 10 existing + 2 planned siblings — plus the `digest_lobster_dsl_openclaw` cross-link under `digest/` and the planned-this-series `to04` deep-dive pointer, neither counting toward the documentation/ floor):**
- [Hermes — Adding a Built-In Tool](../hermes_agent/hermes_adding_built_in_tool.md) — add a `tools`-contract plugin; relevance: structural twin to enabling llm-task/lobster.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — the surface taxonomy (providers/channels/tools); relevance: defines the `tools` surface these two register.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin loading/lifecycle; relevance: how a tool plugin gets installed/enabled.
- [Hermes — Tools Runtime](../hermes_agent/hermes_tools_runtime.md) — tool execution runtime; relevance: where the `tools` contract gets invoked at runtime.
- [Hermes — Core Tools Reference](../hermes_agent/hermes_tools_reference_core.md) — built-in tool catalog; relevance: the catalog llm-task/lobster join via `contracts: tools`.
- [Hermes — Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — the gateway that exposes/registers callable tools; relevance: the runtime surface a `tools`-contract plugin (llm-task/lobster) plugs into.
- [PI — Custom Tools Extensions](../pi/pi_extensions_custom_tools.md) — registering a custom tool; relevance: the pi-corpus analog for a tool plugin.
- [Claude Code — Tools Catalog](../claude_code/cc_tools_catalog.md) — Claude Code tool inventory; relevance: cross-tool inventory analog for the `tools` surface.
- [Claude Code — SDK Custom Tool Definition](../claude_code/cc_sdk_custom_tool_definition.md) — defining a custom callable tool in the SDK; relevance: the exact tool-registration shape llm-task exposes as "an LLM task as a tool".
- [Claude Code — Create and Run Workflows](../claude_code/cc_create_and_run_workflows.md) — authoring/running typed multi-step workflows; relevance: the cross-corpus analog of Lobster's typed-pipeline orchestration.
- [Claude Code — SDK Tool Approval Handling](../claude_code/cc_sdk_tool_approval_handling.md) — tool-call approval/gating in the SDK; relevance: the twin of Lobster's resumable human-in-the-loop approval gate.
- [OpenClaw — Model/Embedding Provider Plugins](oc_plugins_reference_lm_model_providers.md) (planned, this series) — sibling `l*` plugin card; relevance: same series, provider class.
- [OpenClaw — Matrix/Mattermost Channel Plugins](oc_plugins_reference_matrix_mattermost_channels.md) (planned, this series) — sibling card, channel class; relevance: contract-class contrast within the series.
- [OpenClaw — llm-task / lobster Tool Deep-Dive](to04) (planned, this series — `to04`) — the `tools/llm-task` + `tools/lobster` deep-dives; relevance: the tool-deep-dive owner for these two cards.

**Repos (additional):**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — tool/skill-descriptor subsystem; relevance: the subsystem that loads `contracts: tools` plugins.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: invokes the `tools` these plugins register.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: loads these tool plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — host repo; relevance: the product they extend.

**Snippets (12):**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool registry assembly; relevance: where `contracts: tools` plugins land.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool gating/approval; relevance: adjacency to Lobster's resumable approvals.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — the `tools` contract descriptor; relevance: the exact contract shape both plugins satisfy.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin contract declaration; relevance: how a plugin declares `contracts: tools`.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/enable lifecycle; relevance: the install/enable path these cards summarize.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how a tool plugin declares its entry.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — workflow/skill planning; relevance: the workflow context Lobster's typed pipelines run in.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill/tool manifest format; relevance: how a tool plugin's manifest declares its surface.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — Hermes tool registry; relevance: the cross-corpus twin of the `tools` registry.
- [snippet_hermes_agent_core_tool_executor_sequential](../../code_snippets/snippet_hermes_agent_core_tool_executor_sequential.md) — sequential tool execution; relevance: how a `tools` plugin gets executed in a workflow step.
- [snippet_hermes_agent_tools_clarify](../../code_snippets/snippet_hermes_agent_tools_clarify.md) — a structured-output / approval-style tool; relevance: structural twin for llm-task's JSON-only structured task + lobster's approval gate.

### oc_plugins_reference_matrix_mattermost_channels (10t · 12s · 11d)

**Terms (10):**
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: the bot persona behind a Matrix/Mattermost channel.
- [Bot](../../term_dictionary/term_bot.md) — automated account/integration; relevance: a channel plugin = a bot integration on that platform.
- [Slack](../../term_dictionary/term_slack.md) — Slack chat platform; relevance: sibling chat-channel analog for contrast.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback ingress/egress; relevance: a channel's send/receive transport (Mattermost incoming/outgoing).
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent realtime transport; relevance: Matrix/Mattermost realtime event streams.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway that bridges chat platforms to the agent; relevance: the subsystem these `channels:` plugins plug into.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the core channel dispatch/routing engine; relevance: the engine that normalizes/dispatches Matrix/Mattermost messages.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a capability surface; relevance: same plugin-registration shape, here registering a `channels:` surface.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — direct-message pairing/allowlist; relevance: Matrix's "rooms and direct messages" includes the DM pairing path.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: Matrix's install route is ClawHub/`npm` (vs included-in-OpenClaw for Mattermost).
- (also linkable as host context: [OpenClaw](../../term_dictionary/term_openclaw.md).)

**Docs (11; 9 existing + 2 planned):**
- [Hermes — Matrix Messaging](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel integration; relevance: the exact Matrix analog in the hermes corpus.
- [Hermes — Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Matrix end-to-end encryption; relevance: the encryption layer of the Matrix channel.
- [Hermes — Matrix Proxy Mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — Matrix proxy deployment; relevance: a Matrix-channel deployment mode.
- [Hermes — Mattermost Messaging](../hermes_agent/hermes_messaging_mattermost.md) — Mattermost channel integration; relevance: the exact Mattermost analog.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel-adapter architecture; relevance: the architecture both `channels:` plugins satisfy.
- [Hermes — Slack Messaging](../hermes_agent/hermes_messaging_slack.md) — Slack channel integration; relevance: sibling chat-channel pattern for contrast.
- [Hermes — Adding a Platform Adapter (Plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — add a channel via plugin; relevance: the install/enable procedure these two cards summarize.
- [Hermes — Adding a Platform Adapter (Built-In)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — built-in channel adapter; relevance: contrast for Mattermost's included-in-OpenClaw route.
- [Claude Code — Channels Overview](../claude_code/cc_channels_overview.md) — channel concept overview; relevance: cross-corpus framing of the `channels:` surface.
- [OpenClaw — Matrix/Mattermost Channel Deep-Dive](ch03) (planned, this series — `ch03`) — the `channels/matrix` + `channels/mattermost` deep-dives; relevance: each card's `## Related docs` pointer.
- [OpenClaw — Model/Embedding Provider Plugins](oc_plugins_reference_lm_model_providers.md) (planned, this series) — plugin-card sibling; relevance: same series, different contract class.

**Repos (additional):**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel package family; relevance: where matrix/mattermost belong.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: the runtime these channel plugins register into.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: loads these channel plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — host repo; relevance: the product they extend.

**Snippets (12):**
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix adapter impl; relevance: the concrete Matrix channel-adapter code.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — Matrix connect/login; relevance: the Matrix channel connection path.
- [snippet_hermes_agent_gw_platform_matrix_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_normalize.md) — Matrix message normalize; relevance: how the Matrix channel normalizes inbound events.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix room ACL/access; relevance: the rooms-and-DMs access control of the Matrix channel.
- [snippet_hermes_agent_gw_platform_mattermost](../../code_snippets/snippet_hermes_agent_gw_platform_mattermost.md) — Mattermost adapter impl; relevance: the concrete Mattermost channel-adapter code.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — the abstract channel-adapter base class; relevance: the contract every `channels:` plugin (matrix/mattermost) implements.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel-adapter contract; relevance: the OpenClaw `channels:` contract these plugins satisfy.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: how a `channels:` plugin gets registered/normalized.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel-kernel dispatch; relevance: the engine that dispatches Matrix/Mattermost messages.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: routing a message to the right channel binding (room/DM).
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: resolving Matrix rooms / Mattermost conversations to sessions.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config; relevance: the per-channel install/config these cards summarize.


## Undigested Terms Plan (Step 4e)

Per master, OpenClaw vocabulary is digested as `oc_` doc notes (these install cards), NOT new `term_dictionary` entries; existing terms are linked. **Expected 0 new `term_dictionary` captures** for pl13.

| Term | Disposition |
|---|---|
| LiteLLM (provider/proxy) | Documented as config in note 1; link existing `term_provider_plugin` / `term_llm` / `term_third_party_genai_services`. Provider name not promoted (`term_litellm` confirmed MISSING — names-as-config rule). |
| Llama Cpp / node-llama-cpp / GGUF (local embedding provider) | Config in note 1; link `term_embedding` / `term_quantization` / `term_provider_plugin`. Not promoted (`term_llama_cpp` / `term_gguf` confirmed MISSING). |
| LM Studio (local model + embedding provider) | Config in note 1; link `term_llm` / `term_embedding` / `term_provider_plugin`. Not promoted (`term_lmstudio` MISSING). |
| `imageGenerationProviders` / `embeddingProviders` / `memoryEmbeddingProviders` (capability contracts) | OpenClaw capability-contract vocabulary → described in note 1 (and ultimately the `plugins/architecture` / `plugins/manifest` deep-dives owned by pl01/pl04); link `term_provider_plugin` / `term_embedding`. Not new terms. |
| LLM Task (JSON-only structured-task tool) | Config in note 2; link `term_function_calling` / `term_structured_output` / `term_tool_registry`. Not promoted. |
| Lobster (typed-pipeline workflow tool) | Config in note 2; link `term_orchestration` / `term_human_in_the_loop` / `term_idempotency`. Not promoted (`term_lobster` / `term_workflow` / `term_dsl` / `term_durable_execution` confirmed MISSING; the existing `digest_lobster_dsl_openclaw` is LINKED as the deep-dive). |
| `tools` (capability contract) | OpenClaw tool-contract vocabulary → described in note 2; link `term_function_calling` / `term_tool_registry`. Not a new term. |
| Matrix (channel) | Config in note 3; link `term_chatbot` / `term_bot` / `term_websocket`. Not promoted (`term_matrix` resolves only to unrelated math/role-matrix notes — NOT cited; the chat protocol gets no term). |
| Mattermost (channel) | Config in note 3; link `term_chatbot` / `term_bot`. Not promoted (`term_mattermost` MISSING). |
| `channels:` (capability surface) | OpenClaw channel-surface vocabulary → described in note 3; link `term_chatbot` / `term_webhook`. Not a new term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking a home appears in these 7 cards — all are provider/tool/channel *names* (documented as config) or OpenClaw-internal capability-contract ids (documented in the `oc_` notes). If augment's re-scan surfaces one, it would be captured via `/tessellum-capture-term-note` + added to `acronym_glossary_agentic_ai.md` (best-fit for agent/plugin vocabulary); not anticipated.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl13 authors zero `term_dictionary` notes (inherited from master). If augment proposes a new term, the master's multi-source-research + glossary-update requirement applies (research ≥2 independent sources, write full term-note format, add the glossary row).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (3 notes, P3). All gates must PASS before commit.

| Gate | Check | Tooling | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order/values valid (itemized keywords/topics, quoted years, no forbidden fields); `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; bold `**Source**`/`**Last Updated**`/`**Status**` footer. 0 ERROR/LINK-003. |
| G2 | Grounding | diff vs `inbox/openclaw_docs/plugins/reference/<page>.md` | Every package name, install route, and capability-surface id traces to source; no invented config. |
| G3 | Density + Coverage | `wc -w` / fence count | Each note ≤2500w / ≤6 code / ≤400L (all expected ≤290w, 0 code); all 19 H2 covered (Section Coverage Map). |
| G4 | Cross-Reference | link audit | ≥6 relevance-selected term links + repo/sibling/analog links per note, each with a relevance statement (indexed `[text](path.md)` format). |
| G6 | Broken-link | `/tessellum-fix-broken-links` | 0 broken relative paths after reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | `note_links` query | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + candidate inlinks below); in-degree ≥1, no island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_lm_model_providers oc_plugins_reference_lm_workflow_tools oc_plugins_reference_matrix_mattermost_channels"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for s in "## Overview" "## Related Notes"; do
    grep -qF "$s" "$f" || echo "MISSING SECTION [$s] in $n"
  done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density (frontmatter-stripped body word count + fence pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # sibling/discoverability: ≥1 oc_ sibling link
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) link in $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# post-write: incremental reindex + in-degree (G7/G8)
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  [ "${indeg:-0}" -ge 1 ] && echo "$n in-degree(outside-folder)=$indeg OK" || echo "G8 FAIL: $n has no outside-folder inbound link"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_lm_model_providers | procedure | 290 | 0 | ✅ |
| 2 | oc_plugins_reference_lm_workflow_tools | procedure | 230 | 0 | ✅ |
| 3 | oc_plugins_reference_matrix_mattermost_channels | procedure | 230 | 0 | ✅ |

No note approaches any cap (≤2500w / ≤6 code / ≤400L). Source has 0 code fences, so notes render package names and contract ids inline as `code`; the only borderline concern is the *opposite* (under-thin), addressed by consolidating same-class micro-stubs into 3 cluster notes and by enriching each note with Overview context + the cross-reference web.

## Entry Point Decision (inherited from master)

Contributes **3 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **Plugins → Reference (l\* / m\*)** cluster — one row per note (note 1 covers 3 source pages, notes 2 and 3 cover 2 each). Each note receives its entry-point back-link at finalization (satisfies G7/G8 in-degree). No new entry point is created by this sub-plan; it is a contributor to the master's `entry_openclaw_docs.md`.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfy G7/G8):

- `entry_openclaw_docs.md` → notes 1, 2, 3 (primary discoverability source — guaranteed ≥1 inbound each once W1 lands).
- `repo_openclaw_extensions_llm_providers.md` → note 1 (the provider-plugin package family litellm/llama-cpp/lmstudio ship in).
- `repo_openclaw_memory.md` → note 1 (consumes the `embeddingProviders`/`memoryEmbeddingProviders` these plugins register).
- `repo_openclaw_skills.md` → note 2 (the tool/skill-descriptor subsystem that loads `contracts: tools` plugins).
- `repo_openclaw_channels_messaging.md` → note 3 (the channel package family matrix/mattermost belong to).
- `term_provider_plugin.md` → notes 1, 2, 3 (canonical provider/plugin term; reciprocal back-link).
- `term_embedding.md` → note 1; `term_function_calling.md` → note 2; `term_chatbot.md` → note 3 (reciprocal back-links).
- `digest_lobster_dsl_openclaw.md` → note 2 (the Lobster deep-dive digest links its inventory card).
- `term_openclaw.md` → notes 1–3 (host term, reciprocal).

## Pacing Rules (inherited from master)

Single phase, 3 notes — well under the ~30-agent fan-out cap. Re-read each of the 7 source cards; reproduce package names / install routes / capability-surface ids verbatim (inline `code`, 0 fenced blocks). One BB per note (all procedure). `git pull --rebase --autostash origin main` before commit; commit+push the phase as one cycle; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + G8 in-degree ≥1 before commit.

## Augmentation Report (2026-06-21)


**Per-note locked counts (floors MET on all 3):**

| Note | Terms | Snippets | Docs (existing + planned) | Repos | Floors (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_lm_model_providers | 10 | 12 | 11 (8 + 3) | 4 | ✅ |
| oc_plugins_reference_lm_workflow_tools | 10 | 12 | 11 (8 + 3) | 4 | ✅ |
| oc_plugins_reference_matrix_mattermost_channels | 10 | 12 | 11 (9 + 2) | 4 | ✅ |

**New terms surfaced during the augment re-read (Step 2d / Step 10.5f).** None. The 7 source cards are 51–62-word micro-stubs whose only content is npm-package → capability-surface → deep-dive-page mappings; every concept is either a provider/tool/channel *name* (documented as config per the names-as-config rule, NOT promoted) or an OpenClaw-internal capability-contract id (`imageGenerationProviders`, `embeddingProviders`, `memoryEmbeddingProviders`, `tools`, `channels:`) digested inside the `oc_` notes. **New-term candidates: 0.** Best-fit glossary IF one ever surfaces: `acronym_glossary_agentic_ai.md` (agent/plugin vocabulary) — not anticipated, not needed for pl13.

**Collision/dedup audit (Step 10.5f generalized to ALL planned notes).** The 3 planned `oc_*` notes were synonym-searched against `term_dictionary/` AND `resources/documentation/openclaw/`: 0 existing `documentation/openclaw/` notes (confirmed empty subfolder — this is the first sub-plan to populate it); no planned `oc_*` note duplicates an existing substantive term note (the providers/tools/channels deep-dives are owned by `pr05`/`pl03`/`to04`/`ch03`, all LINKED not recreated; `digest_lobster_dsl_openclaw` is LINKED for Lobster). No too-general slug (the 3 filenames carry capability-cluster qualifiers `lm_model_providers` / `lm_workflow_tools` / `matrix_mattermost_channels`, none collide). No renames needed.

**Density re-read confirmation.** Re-measured all 7 source cards: 56/51/57/60/54/58/62 = 398 words, 0 code fences, 19 H2, 0 H3 — exactly matching the plan's Source table. The real risk remains under-thin (addressed by cluster consolidation + Overview + the locked cross-ref web), never over-dense; no further splits needed.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors, relevance + relevancy statement each) | **PASS** | Per-Note Related Notes Mapping present; all 3 notes = 10 terms / 12 snippets / 11 docs / 4 repos, every link rendered `- [Name](relpath.md) — what; relevance: why THIS note`. Exceeds the ≥8t/≥10s/≥10d floors. |
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7/G8 in-degree ≥1; Validation Scripts implement format + density + sibling + reindex + outside-folder in-degree check. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | "Entry Point Decision" inherits master W1 `entry_openclaw_docs.md` (contributes 3 rows under Plugins → Reference (l*/m*)); DB-confirmed `entry_openclaw_docs` not yet created (master pre-step, expected). |
| CP4 | Size (≤30 or split) | **PASS** | 3 notes — far under 30; single execution phase. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Format inherited from master Format Definition, itself derived from existing `claude_code/` + `pi/` doc corpora (`## Overview` / source-mirrored H2 / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer; forbidden-field list); `documentation/openclaw/` is empty so parent-corpus derivation is the correct basis. |
| CP6 | Density (borderline → split) | **PASS** | All 3 notes ≤290w, 0 code, single BB (procedure) — no borderline case; the only risk (under-thin) is mitigated by consolidation + cross-ref web. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 source cards re-read this session (`Read` on `inbox/openclaw_docs/plugins/reference/*.md`); measured 56/51/57/60/54/58/62 = 398w, 0 code, matching the plan's Source table exactly (ratio 1.0). |
| CP8 | Undigested terms + authoring reqs | **PASS** | "Undigested Terms Plan" present (10 rows, all dispositioned as config/link-existing, 0 promoted); "Term-Note Authoring Requirements" present (N/A — 0 new terms; master multi-source+glossary mandate applies if augment surfaces one). Re-scan surfaced 0 new terms. |
| CP8f | Slug specificity / collision audit (all notes, term + doc) | **PASS** | Step 10.5f run generalized to all 3 `oc_*` notes vs `term_dictionary/` AND `documentation/openclaw/` (empty); 0 duplicates of substantive vault notes, 0 too-general slugs, 0 renames; deep-dives owned elsewhere are LINKED not recreated. |
| CP9 | Discoverability / inlinks (G8, no island) | **PASS** | "Inlinks (existing → new)" maps every note to ≥1 outside-folder inbound source (`entry_openclaw_docs` → all 3; `repo_openclaw_extensions_llm_providers`/`repo_openclaw_memory` → note 1; `repo_openclaw_skills`/`digest_lobster_dsl_openclaw` → note 2; `repo_openclaw_channels_messaging` → note 3; reciprocal term back-links); G7/G8 in-degree ≥1 check in Validation Scripts. |


## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref locked at raised floors; 0 new terms) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY** (9/9 + CP8f PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |
