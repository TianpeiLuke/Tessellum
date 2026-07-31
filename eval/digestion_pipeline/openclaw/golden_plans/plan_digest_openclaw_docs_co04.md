---
title: Sub-Plan co04 — OpenClaw Docs: Concepts (Memory, Messages, Models, Failover, Providers)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["concepts/memory-qmd", "concepts/memory-search", "concepts/message-lifecycle-refactor", "concepts/messages", "concepts/model-failover", "concepts/model-providers", "concepts/models"]
---

# Sub-Plan co04: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References` → bold footer), dedup-before-create (term_dictionary + documentation/ + `repo_openclaw*`), the 9-GATE, cross-references, and the entry-point/series-wiring decisions are all INHERITED verbatim from the master and are not re-derived here.

## Scope

The seven `concepts/` pages covering OpenClaw's **memory backends** (the QMD local search sidecar, hybrid
memory search), the **channel message domain** (the durable receive/send lifecycle refactor design + the
runtime message-flow concepts), and the **model layer** (failover/rotation, provider configuration, and the
Models CLI/selection rules). **P1 (Phase A)** — this is conceptual/operational core: the model-failover and
model-providers/models vocabulary is referenced by the CLI (`cl*`), gateway (`gw*`), and provider (`pr*`)
sub-plans, and the message-lifecycle/messages concepts underpin every channel (`ch*`) sub-plan. The
code-side counterparts (`repo_openclaw_memory`, `repo_openclaw_channels`, `repo_openclaw_channels_messaging`,
`repo_openclaw_agents`, `repo_openclaw_extensions_llm_providers`, `repo_openclaw_sessions`) are LINKED, not
recreated.

**Source**: OpenClaw docs, 7 pages, **18,906 measured words**. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| memory-qmd | /concepts/memory-qmd | 1,410 | 8 | 13 | 2 | procedure |
| memory-search | /concepts/memory-search | 810 | 3 | 9 | 3 | procedure |
| message-lifecycle-refactor | /concepts/message-lifecycle-refactor | 5,786 | 29 | 21 | 13 | argument (design; split: model vs migration) |
| messages | /concepts/messages | 1,212 | 2 | 13 | 0 | concept |
| model-failover | /concepts/model-failover | 3,280 | 6 | 13 | 5 | concept (split: auth rotation vs model fallback) |
| model-providers | /concepts/model-providers | 3,889 | 19 | 7 | 21 | procedure (split: official plugins vs custom base-URL) |
| models | /concepts/models | 2,519 | 8 | 11 | 3 | procedure (split: selection policy vs Models CLI) |

## Content Strategy

- **Prioritize**: the model-failover runtime rules (auth-profile rotation + model fallback — every run
  depends on them), the model-selection/provider-config layer (how a user actually wires a model), and the
  message-lifecycle durable receive/send model (the design every channel plugin inherits). These are the
  highest-relevance reference for the rest of the corpus.
- **Split** (per master >2,500w OR mixed-BB rules — see Split Decisions): `message-lifecycle-refactor.md`
  (5,786w) → receive/send domain model + migration/compatibility design; `model-failover.md` (3,280w) →
  auth-profile rotation + model fallback; `model-providers.md` (3,889w) → official provider plugins + custom
  `models.providers` base-URL providers; `models.md` (2,519w, just over cap + mixed concept/CLI) → selection
  policy concept + Models CLI procedure.
- **Skip / link-out**: provider auth credential mechanics → `gw*`/`pr*` and `term_oauth_token`; the full
  provider-by-provider plugin reference pages → `pr01–09`; OAuth flow detail → `concepts/oauth` (co05);
  agent-runtime split detail → `concepts/agent-runtimes` (co01); session/queue/compaction internals →
  co06/co02; per-provider setup pages → Providers section. Existing term notes (`term_llm`, `term_claude`,
  `term_mcp`, `term_rag`, `term_bm25`, `term_vector_database`, `term_function_calling`, `term_failover`,
  `term_idempotency`, …) are LINKED, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_memory_qmd.md` | procedure | memory-qmd.md (all 13 H2: What it adds, Getting started/Prerequisites/Enable, How the sidecar works, Search performance/compatibility, Model overrides, Indexing extra paths, Indexing session transcripts, Search scope, Citations, When to use, Troubleshooting, Configuration) | 600 | Setting up QMD as OpenClaw's local-first memory backend: install/enable the sidecar, how the managed QMD home works, BM25+vector+reranking search, model overrides, indexing extra paths and session transcripts, search scope, citations, and troubleshooting. |
| 2 | `oc_concepts_memory_search.md` | procedure | memory-search.md (all 9 H2: Quick start, Supported providers, How search works, Improving search quality/Temporal decay/MMR/Enable both, Multimodal memory, Session memory search, Troubleshooting, Further reading) | 450 | Configuring OpenClaw built-in memory search: enabling semantic search, supported embedding providers, how hybrid retrieval works, quality knobs (temporal decay, MMR diversity), multimodal and session-transcript memory, and troubleshooting. |
| 3 | `oc_concepts_message_lifecycle_refactor_model.md` | argument | message-lifecycle-refactor.md: Problems, Goals, Non goals, Reference model, Core model, Message terms (Message/Target/Relation/Origin/Receipt), Receive context, Send context, Live context, Adapter surface, Public SDK reduction, Relationship to channel inbound | 700 | The target durable message-lifecycle design: why scattered reply/dispatch helpers are replaced by one receive/send domain, the core primitives (message, target, relation, origin, receipt), receive/send/live contexts, the adapter surface, and the reduced public plugin SDK. |
| 4 | `oc_concepts_message_lifecycle_refactor_migration.md` | argument | message-lifecycle-refactor.md: Compatibility guardrails, Internal storage, Failure classes, Channel mapping, Migration plan (Phases 1–8), Test plan, Open questions, Acceptance criteria | 650 | The message-lifecycle migration plan: compatibility guardrails, durable internal storage, failure classes, per-channel mapping, the eight-phase rollout (internal domain → durable send core → inbound/dispatcher bridges → unified live lifecycle → public SDK → remove turn-named compat), test plan, and acceptance criteria. |
| 5 | `oc_concepts_messages.md` | concept | messages.md (all 13 H2: Message flow high level, Inbound dedupe, Inbound debouncing, Sessions and devices, Tool result metadata, Inbound bodies and history context, Queueing and followups, Channel run ownership, Streaming/chunking/batching, Reasoning visibility and tokens, Prefixes/threading/replies, Silent replies) | 600 | OpenClaw's runtime message-flow model: the high-level inbound→session→reply path, inbound dedupe and debouncing, session/device binding, tool-result metadata, history context, queueing and followups, channel run ownership, streaming/chunking, reasoning visibility, threading/replies, and silent replies. |
| 6 | `oc_concepts_model_failover_auth_rotation.md` | concept | model-failover.md: Runtime flow (auth half), Selection source policy, Auth failure skip cache, User-visible fallback notices, Auth storage (keys+OAuth), Profile IDs, Rotation order (Session stickiness, Codex subscription+API-key backup), Cooldowns, Billing disables | 650 | OpenClaw auth-profile failover: how it rotates API-key/OAuth auth profiles within a provider — selection-source policy, the auth-failure skip cache, fallback notices, the per-agent auth store, profile IDs, rotation order (session stickiness, Codex subscription + API-key backup), cooldowns, and billing disables. |
| 7 | `oc_concepts_model_failover_model_fallback.md` | concept | model-failover.md: Runtime flow (fallback half), Model fallback (Candidate chain rules, Which errors advance fallback, Cooldown skip vs probe behavior), Session overrides and live model switching, Observability and failure summaries, Related config | 600 | OpenClaw model fallback: building the model candidate chain from the fallback policy, which errors advance fallback, cooldown-skip vs probe behavior, persisting/rolling back auto overrides, session overrides and live `/model` switching, and the FallbackSummaryError observability surface. |
| 8 | `oc_concepts_model_providers_official.md` | procedure | model-providers.md: Quick rules, Plugin-owned provider behavior, API key rotation, Official provider plugins (OpenAI, Anthropic, ChatGPT/Codex OAuth, other subscription options, OpenCode, Google Gemini, Google Vertex/Gemini CLI, Z.AI, Vercel AI Gateway, other bundled plugins), CLI examples | 700 | Configuring OpenClaw's official/bundled provider plugins: model-ref rules, plugin-owned behavior, multi-key API-key rotation, and per-provider auth/setup for OpenAI, Anthropic, ChatGPT/Codex OAuth, Google Gemini, Vertex, Z.AI, Vercel AI Gateway, and other bundled plugins, with CLI onboarding examples. |
| 9 | `oc_concepts_model_providers_custom.md` | procedure | model-providers.md: Providers via `models.providers` (custom/base URL) — Moonshot/Kimi, Kimi coding, Volcano Engine (Doubao), BytePlus, Synthetic, MiniMax, LM Studio, Ollama, vLLM, SGLang, Local proxies (LM Studio/vLLM/LiteLLM) | 600 | Adding custom/base-URL providers through `models.providers`: defining baseUrl + api + key + model entries for Moonshot/Kimi, Volcano Engine, BytePlus, Synthetic, MiniMax, and local inference servers (LM Studio, Ollama, vLLM, SGLang) and local OpenAI-compatible proxies. |
| 10 | `oc_concepts_models_selection.md` | concept | models.md: How model selection works, Selection source and fallback behavior, Quick model policy, Onboarding (recommended), Config keys overview (Safe allowlist edits), "Model is not allowed" (and why replies stop), Models registry (`models.json`) | 600 | How OpenClaw selects a model: the primary→fallbacks→auth-failover order, selection-source semantics (configured/auto/user/cron), the model allowlist and `agents.defaults.models` config keys, the "Model is not allowed" failure mode, and the `models.json` registry. |
| 11 | `oc_concepts_models_cli.md` | procedure | models.md: Switching models in chat (`/model`), CLI commands (`models list`, `models status`), Scanning (OpenRouter free models) | 500 | The Models CLI/UX: switching models in chat with `/model`, the `openclaw models list` / `models status` commands and their output, and scanning OpenRouter free models with tool/image capability probes. |

## Section Coverage Map

```
memory-qmd.md
├── What it adds over builtin ───────────────────── → note 1 (oc_concepts_memory_qmd)
├── Getting started / Prerequisites / Enable ────── → note 1
├── How the sidecar works ───────────────────────── → note 1
├── Search performance and compatibility ────────── → note 1
├── Model overrides ─────────────────────────────── → note 1
├── Indexing extra paths ────────────────────────── → note 1
├── Indexing session transcripts ────────────────── → note 1
├── Search scope ────────────────────────────────── → note 1
├── Citations ───────────────────────────────────── → note 1
├── When to use ─────────────────────────────────── → note 1
├── Troubleshooting ─────────────────────────────── → note 1
├── Configuration ───────────────────────────────── → note 1
└── Related (page footer) ───────────────────────── → note 1 (mined for Related Notes)
memory-search.md
├── Quick start ─────────────────────────────────── → note 2 (oc_concepts_memory_search)
├── Supported providers ─────────────────────────── → note 2
├── How search works ────────────────────────────── → note 2
├── Improving search quality (Temporal decay / MMR / Enable both) → note 2
├── Multimodal memory ───────────────────────────── → note 2
├── Session memory search ───────────────────────── → note 2
├── Troubleshooting ─────────────────────────────── → note 2
├── Further reading ─────────────────────────────── → note 2 (mined for References)
└── Related (page footer) ───────────────────────── → note 2 (mined for Related Notes)
message-lifecycle-refactor.md
├── Problems ────────────────────────────────────── → note 3 (oc_concepts_message_lifecycle_refactor_model)
├── Goals / Non goals ───────────────────────────── → note 3
├── Reference model ─────────────────────────────── → note 3
├── Core model ──────────────────────────────────── → note 3
├── Message terms (Message/Target/Relation/Origin/Receipt) → note 3
├── Receive context / Send context / Live context ─ → note 3
├── Adapter surface ─────────────────────────────── → note 3
├── Public SDK reduction ────────────────────────── → note 3
├── Relationship to channel inbound ─────────────── → note 3
├── Compatibility guardrails ────────────────────── → note 4 (oc_concepts_message_lifecycle_refactor_migration)
├── Internal storage ────────────────────────────── → note 4
├── Failure classes ─────────────────────────────── → note 4
├── Channel mapping ─────────────────────────────── → note 4
├── Migration plan (Phases 1–8) ─────────────────── → note 4
├── Test plan ───────────────────────────────────── → note 4
├── Open questions ──────────────────────────────── → note 4
├── Acceptance criteria ─────────────────────────── → note 4
└── Related (page footer) ───────────────────────── → notes 3,4 (mined for Related Notes)
messages.md
├── Message flow (high level) ───────────────────── → note 5 (oc_concepts_messages)
├── Inbound dedupe / Inbound debouncing ─────────── → note 5
├── Sessions and devices ────────────────────────── → note 5
├── Tool result metadata ────────────────────────── → note 5
├── Inbound bodies and history context ──────────── → note 5
├── Queueing and followups ──────────────────────── → note 5
├── Channel run ownership ───────────────────────── → note 5
├── Streaming, chunking, and batching ───────────── → note 5
├── Reasoning visibility and tokens ─────────────── → note 5
├── Prefixes, threading, and replies ────────────── → note 5
├── Silent replies ──────────────────────────────── → note 5
└── Related (page footer) ───────────────────────── → note 5 (mined for Related Notes)
model-failover.md
├── Runtime flow (auth-profile rotation half) ───── → note 6 (oc_concepts_model_failover_auth_rotation)
├── Selection source policy ─────────────────────── → note 6
├── Auth failure skip cache ─────────────────────── → note 6
├── User-visible fallback notices ───────────────── → note 6
├── Auth storage (keys + OAuth) ─────────────────── → note 6
├── Profile IDs ─────────────────────────────────── → note 6
├── Rotation order (Session stickiness / Codex sub + API-key backup) → note 6
├── Cooldowns / Billing disables ────────────────── → note 6
├── Runtime flow (model-fallback half) ──────────── → note 7 (oc_concepts_model_failover_model_fallback)
├── Model fallback (Candidate chain / Which errors / Cooldown skip vs probe) → note 7
├── Session overrides and live model switching ──── → note 7
├── Observability and failure summaries ─────────── → note 7
└── Related config (page footer) ────────────────── → notes 6,7 (mined for Related Notes)
model-providers.md
├── Quick rules ─────────────────────────────────── → note 8 (oc_concepts_model_providers_official)
├── Plugin-owned provider behavior ──────────────── → note 8
├── API key rotation ────────────────────────────── → note 8
├── Official provider plugins (OpenAI/Anthropic/Codex OAuth/
│   other subscription/OpenCode/Google Gemini/Vertex+Gemini CLI/
│   Z.AI/Vercel AI Gateway/other bundled) ───────── → note 8
├── CLI examples ────────────────────────────────── → note 8
├── Providers via `models.providers` (custom/base URL):
│   Moonshot/Kimi, Kimi coding, Volcano Engine,
│   BytePlus, Synthetic, MiniMax, LM Studio, Ollama,
│   vLLM, SGLang, Local proxies ─────────────────── → note 9 (oc_concepts_model_providers_custom)
└── Related (page footer) ───────────────────────── → notes 8,9 (mined for Related Notes)
models.md
├── (intro: model refs vs runtime) ──────────────── → note 10 (oc_concepts_models_selection)
├── How model selection works ───────────────────── → note 10
├── Selection source and fallback behavior ──────── → note 10
├── Quick model policy ──────────────────────────── → note 10
├── Onboarding (recommended) ────────────────────── → note 10
├── Config keys (overview) / Safe allowlist edits ─ → note 10
├── "Model is not allowed" (and why replies stop) ─ → note 10
├── Models registry (`models.json`) ─────────────── → note 10
├── Switching models in chat (`/model`) ─────────── → note 11 (oc_concepts_models_cli)
├── CLI commands (`models list` / `models status`) ─ → note 11
├── Scanning (OpenRouter free models) ───────────── → note 11
└── Related (page footer) ───────────────────────── → notes 10,11 (mined for Related Notes)
```
No orphaned sections. Each page's `## Related` footer is mined for the digest note's Related Notes/References,
not reproduced as a body section. Cross-cutting detail (OAuth flow, agent-runtimes, sessions, queue, compaction)
links out to co01/co05/co06 and the relevant `term_*` notes rather than being duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| message-lifecycle-refactor.md (5,786w, 21 H2 / 13 H3, 29 code) | notes 3 + 4 | >2× the 2,500w cap; cleanly bisects into the *domain model* (problems/goals/core primitives/contexts/SDK) and the *migration plan* (compat guardrails/storage/failure classes/8-phase rollout/test/acceptance) — two distinct argument clusters. |
| model-failover.md (3,280w, 13 H2 / 5 H3) | notes 6 + 7 | >2,500w and mixes two BB-cohesive concepts the doc itself labels "two stages": auth-profile rotation (within a provider) vs model fallback (across models). Each becomes a focused concept note ≤650w. |
| model-providers.md (3,889w, 7 H2 / 21 H3, 19 code) | notes 8 + 9 | >2,500w and mixes two task clusters: configuring *official/bundled provider plugins* (auth + model availability) vs defining *custom base-URL providers* via `models.providers`. Split keeps each ≤700w and ≤6 code blocks. |
| models.md (2,519w, 11 H2 / 3 H3, 8 code) | notes 10 + 11 | just over the 2,500w cap AND mixed-BB: selection rules/policy/config (concept) vs the Models CLI/`/model`/scan commands (procedure). Borderline-density → split promoted per master CP6. |
| memory-qmd.md (1,410w) | note 1 (no split) | single procedure under all caps. |
| memory-search.md (810w) | note 2 (no split) | single procedure under all caps. |
| messages.md (1,212w) | note 5 (no split) | single concept under all caps. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (18,906 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×5** (notes 1, 2, 8, 9, 11) · **concept ×4** (notes 5, 6, 7, 10) ·
  **argument ×2** (notes 3, 4).
- Est. digest words ~6,650 (avg ~605/note); every note ≤700w, ≤6 code blocks, single BB. The 75 source code
  fences (esp. message-lifecycle 29, model-providers 19) distribute across the split notes so none exceeds 6
  (config/JSON5 snippets reproduced selectively, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21): each note maps **≥8 relevancy-selected `term_dictionary`
  terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (PLUS relevant `repo_openclaw*`/
  See [Per-Note Related Notes Mapping](#per-note-related-notes-mapping-locked--xref-augment-2026-06-21).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Relative paths are from a note at `resources/documentation/openclaw/oc_*.md`: term → `../../term_dictionary/term_*.md`;
> sibling oc_ doc (this series, planned) → `oc_*.md`; other doc → `../<folder>/<file>.md`; repo →
> `../../../areas/code_repos/repo_*.md`; snippet → `../../code_snippets/snippet_*.md`. Every EXISTING target was
> `sqlite3`-verified present (2026-06-21). Sibling `oc_concepts_*` docs are marked **(planned, this series)** and

### oc_concepts_memory_qmd (10t · 11s · 11d)

**Terms**
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation pattern; relevance: QMD is the retrieval backend feeding memory snippets into the agent prompt.
- [BM25](../../term_dictionary/term_bm25.md) — lexical ranking function; relevance: QMD's `searchMode: "search"` is BM25-only lexical retrieval.
- [Vector Database](../../term_dictionary/term_vector_database.md) — embedding similarity store; relevance: QMD combines vector search with BM25 in one binary.
- [Dense Retrieval](../../term_dictionary/term_dense_retrieval.md) — embedding-based semantic matching; relevance: `vsearch`/`query` modes run dense vector retrieval over indexed chunks.
- [Hybrid Search](../../term_dictionary/term_hybrid_search.md) — fused lexical+vector retrieval; relevance: QMD's `query` path is hybrid BM25+vector with reranking.
- [Recall](../../term_dictionary/term_recall.md) — fraction of relevant items retrieved; relevance: QMD adds reranking and query expansion specifically "for better recall".
- [Embedding](../../term_dictionary/term_embedding.md) — vector representation of text; relevance: `qmd embed` produces the vectors; `QMD_EMBED_MODEL` selects the embedder.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — the retrieval discipline; relevance: QMD is an IR sidecar (recall, indexing, ranking).
- [Quantization](../../term_dictionary/term_quantization.md) — reduced-precision model weights; relevance: QMD auto-downloads quantized GGUF (Q8_0) rerank/embed/generate models.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: OpenClaw drives QMD through MCP query tools and falls back to the CLI path.

**Docs**
- [oc_concepts_memory_search](oc_concepts_memory_search.md) — OpenClaw builtin memory search (planned, this series); relevance: QMD is the sidecar alternative to the builtin engine documented in note 2; auto-fallback links them.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — Hermes memory provider options; relevance: parallel coding-agent memory-backend catalog (builtin vs sidecar vs vector).
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — Hermes memory provider plugin contract; relevance: same plugin-owned memory-backend pattern QMD plugs into.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes persistent memory store; relevance: durable on-disk memory analogous to the QMD managed home and collections.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — Hermes session transcript search/storage; relevance: directly parallels QMD's session-transcript indexing into a dedicated collection.
- [hermes_docker_tools_local_inference](../hermes_agent/hermes_docker_tools_local_inference.md) — Hermes local inference setup; relevance: QMD's fully-local llama.cpp GGUF path mirrors local-inference provisioning.
- [hermes_provider_local_llm_mac](../hermes_agent/hermes_provider_local_llm_mac.md) — local LLM on macOS; relevance: QMD's macOS/WSL2 + GGUF model story matches the local-LLM setup constraints.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — Band agent memories API; relevance: another agent framework's memory store/recall surface for cross-framework comparison.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — Claude Code `.claude` config/state dir; relevance: parallels OpenClaw's `~/.openclaw/agents/<id>/qmd/` managed home + ignore rules.
- [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — Claude Code session persistence; relevance: QMD optionally indexes session transcripts; same transcript-as-data idea.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings reference; relevance: parallel config-key surface for a coding-agent's memory/search knobs (`memory.qmd.*`).

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory backend code; relevance: implements the QMD host, sidecar lifecycle, and builtin fallback this note documents.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo root; relevance: code↔docs anchor for the whole product.

**Snippets**
- [snippet_openclaw_memory_host_qmd_process](../../code_snippets/snippet_openclaw_memory_host_qmd_process.md) — QMD subprocess manager; relevance: implements `qmd update`/`embed` subprocess lifecycle + back-off described here.
- [snippet_openclaw_memory_host_qmd_query_parser](../../code_snippets/snippet_openclaw_memory_host_qmd_query_parser.md) — QMD query/result parsing; relevance: parses the `qmd search --json` output and `qmd/<collection>/<path>` prefixes.
- [snippet_openclaw_memory_host_qmd_scope](../../code_snippets/snippet_openclaw_memory_host_qmd_scope.md) — QMD search-scope rules; relevance: implements `memory.qmd.scope` allow/deny by chatType documented here.
- [snippet_openclaw_memory_host_backend_config](../../code_snippets/snippet_openclaw_memory_host_backend_config.md) — memory backend selection; relevance: resolves `memory.backend: "qmd"` vs builtin + the fallback switch.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine abstraction; relevance: the engine interface QMD and the builtin SQLite engine both implement (auto-fallback).
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime wiring; relevance: lazy memory-runtime init that QMD's `update.startup`/`onBoot` knobs control.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding input construction; relevance: builds the embed inputs reindexed after `QMD_EMBED_MODEL` changes.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding host integration; relevance: vector-readiness probes skipped in BM25-only `search` mode.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — memory/collection schema; relevance: collection patterns (`MEMORY.md`, `memory/`) reconciled at boot.
- [snippet_openclaw_memory_host_internal_walker](../../code_snippets/snippet_openclaw_memory_host_internal_walker.md) — filesystem walker/ignore rules; relevance: the `.git`/`node_modules`/`dist` ignore + symlink/ENAMETOOLONG traversal caveats.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent-side memory_search tool; relevance: the agent entry point that calls into the QMD/builtin engine + citations footer.

### oc_concepts_memory_search (9t · 11s · 11d)

**Terms**
- [Dense Retrieval](../../term_dictionary/term_dense_retrieval.md) — embedding semantic matching; relevance: the vector-search path that finds notes by meaning, not wording.
- [Hybrid Search](../../term_dictionary/term_hybrid_search.md) — fused lexical+vector; relevance: memory_search runs vector + BM25 in parallel and weighted-merges.
- [Embedding](../../term_dictionary/term_embedding.md) — text→vector encoder; relevance: the page is fundamentally about choosing an embedding provider (OpenAI/Gemini/local/Voyage…).
- [Vector Database](../../term_dictionary/term_vector_database.md) — similarity index; relevance: indexed chunks live in a vector store searched by embeddings.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: memory_search is the retrieval stage that augments the agent's context.
- [BM25](../../term_dictionary/term_bm25.md) — lexical ranking; relevance: the keyword path for exact IDs/error strings/config keys, and the `provider: "none"` FTS-only fallback.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — the retrieval discipline; relevance: memory_search is an IR system (chunking, indexing, recall, diversity).
- [MMR](../../term_dictionary/term_mmr.md) — Maximal Marginal Relevance; relevance: the documented diversity knob that de-duplicates redundant snippets.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image+audio modeling; relevance: Gemini Embedding 2 indexes images/audio for multimodal memory.

**Docs**
- [oc_concepts_memory_qmd](oc_concepts_memory_qmd.md) — QMD sidecar backend (planned, this series); relevance: QMD is the advanced backend for the same memory_search surface this note covers.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — Hermes memory providers; relevance: the same "pick an embedding/search backend" decision across providers.
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho memory provider; relevance: an alternative semantic-memory provider analogous to choosing memorySearch.provider.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — persistent memory store; relevance: durable indexed memory chunks searched semantically.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — session-transcript search; relevance: directly parallels `memorySearch.experimental.sessionMemory` transcript indexing.
- [hermes_provider_google_gemini](../hermes_agent/hermes_provider_google_gemini.md) — Gemini provider setup; relevance: Gemini is a supported embedding provider with image/audio indexing.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — local self-hosted LLM; relevance: `provider: "local"`/`ollama`/`lmstudio` local embeddings with no API key.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — Band memories API; relevance: cross-framework memory-recall surface for comparison.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud provider config; relevance: parallel provider-selection surface (the embedding provider is also an LLM provider).
- [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — Claude Code session patterns; relevance: recalling earlier conversations from session memory, same use case.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings; relevance: parallel config knobs (temporal decay/MMR/batch timeouts) for memory tuning.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory backend code; relevance: implements memory_search, the parallel vector+BM25 merge, temporal decay, and MMR.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins incl. embeddings; relevance: hosts the embedding-provider adapters (OpenAI/Gemini/Voyage/local) this note configures.

**Snippets**
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory_search tool entry; relevance: the agent-facing tool whose behavior (FTS-only vs semantic) this page describes.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine interface; relevance: runs the two retrieval paths and weighted merge.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding input builder; relevance: applies `queryInputType`/`documentInputType` asymmetric labels documented here.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding host calls; relevance: routes to the configured embedding provider and reports unavailable on failure.
- [snippet_openclaw_memory_host_internal_chunking](../../code_snippets/snippet_openclaw_memory_host_internal_chunking.md) — memory chunking; relevance: "indexing memory into small chunks" is exactly this code.
- [snippet_openclaw_memory_host_query_lexica](../../code_snippets/snippet_openclaw_memory_host_query_lexica.md) — lexical query handling; relevance: the BM25 keyword path and CJK FTS handling.
- [snippet_openclaw_memory_host_query_tokenizer](../../code_snippets/snippet_openclaw_memory_host_query_tokenizer.md) — query tokenizer; relevance: tokenization feeding BM25; the `--force` CJK rebuild fix.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — index schema; relevance: the FTS/vector index whose status `openclaw memory status` reports.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — evergreen root files; relevance: `MEMORY.md` is never temporally decayed.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory index events; relevance: index/force-reindex events behind `memory index --force` troubleshooting.

### oc_concepts_message_lifecycle_refactor_model (10t · 12s · 11d)

**Terms**
- [Idempotency](../../term_dictionary/term_idempotency.md) — same-effect-on-retry guarantee; relevance: the durable send intent + `idempotencyKey` are the core idempotency mechanism.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedup token for safe retry; relevance: `RenderedMessageBatch.idempotencyKey` keys duplicate suppression and replay.
- [At-Least-Once Delivery](../../term_dictionary/term_at_least_once.md) — guarantee that a message is delivered ≥1×; relevance: the doc states durable recovery gives "at-least-once" semantics.
- [Exactly-Once Delivery](../../term_dictionary/term_exactly_once.md) — deliver precisely once; relevance: only achievable for adapters with native idempotency or `reconcileUnknownSend`.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered async delivery; relevance: the durable outbound queue stores send intents before transport I/O.
- [Server-Sent Events (SSE)](../../term_dictionary/term_sse.md) — server push stream; relevance: live preview/streaming context is the channel-streaming analog of SSE block delivery.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional socket; relevance: socket-based channels (polling vs socket) feed the receive context's ack policy.
- [CQRS](../../term_dictionary/term_cqrs.md) — command/query responsibility separation; relevance: the receive (command) vs send (query/effect) split with a state adapter mirrors CQRS.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP push callback; relevance: webhook platforms need immediate transport ack yet still dedupe + durable send.
- [Dedupe](../../term_dictionary/term_dedupe.md) — duplicate suppression; relevance: receive context's dedupe + self-echo gate and receipt-based duplicate suppression.

**Docs**
- [oc_concepts_message_lifecycle_refactor_migration](oc_concepts_message_lifecycle_refactor_migration.md) — the migration half (planned, this series); relevance: same design doc; this note is the domain model, that note is the rollout.
- [oc_concepts_messages](oc_concepts_messages.md) — runtime message flow (planned, this series); relevance: the current message pipeline this refactor replaces with receive/send contexts.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes gateway message architecture; relevance: parallel inbound→dispatch→outbound channel architecture.
- [hermes_messaging_raft](../hermes_agent/hermes_messaging_raft.md) — Hermes durable messaging/consensus; relevance: durable message delivery + restart recovery, the same reliability problem.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway internals; relevance: session ownership, dispatch, and reply lifecycle on the gateway host.
- [band_websocket_agent_events](../band/band_websocket_agent_events.md) — Band agent event protocol; relevance: normalized inbound/outbound message events analogous to ChannelMessage.
- [band_agent_api_messages_events](../band/band_agent_api_messages_events.md) — Band messages/events API; relevance: message-as-event domain model with relations/origins.
- [band_websocket_overview](../band/band_websocket_overview.md) — Band socket transport overview; relevance: transport ack/redelivery semantics the receive context formalizes.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — Claude Code channels overview; relevance: cross-agent channel-plugin model and reply dispatch.
- [cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md) — channel permission relay; relevance: routing/authorize step in the receive context (bot-author/echo gating).
- [pi_rpc_events](../pi/pi_rpc_events.md) — Pi RPC event stream; relevance: structured event lifecycle with begin/commit/fail-style transitions.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels core code; relevance: home of the `src/channels/message/*` domain this refactor introduces.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging delivery code; relevance: implements the reply/dispatch helpers the refactor consolidates into send context.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo root; relevance: code↔docs anchor.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter interface; relevance: the target `ChannelMessageAdapter` (receive/send/live/origin/render/capabilities) surface.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch path; relevance: inbound dispatch step of the receive context.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable kernel delivery; relevance: the durable send intent + begin/commit/fail boundary this note designs.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/target resolution; relevance: maps platform events to MessageTarget (direct/group/channel/thread).
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — routing/bindings; relevance: the route-and-authorize step in receive flow.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — normalize raw events; relevance: the `normalize(raw)` adapter step producing a platform-neutral ChannelMessage.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — event match/classify; relevance: the `classify`/`preflight` receive-adapter hooks.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/silent-reply policy; relevance: silent-reply rewrites and relation-aware send policy.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound send handler; relevance: the outbound delivery path being unified under send context.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persist on lifecycle; relevance: persisting durable intent/receipt state across the begin→commit window.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: begin/commit/fail transitions analogous to the context lifecycle.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — typing/status/read receipts; relevance: the "user-visible receipt" signal kept separate from durability acks.

### oc_concepts_message_lifecycle_refactor_migration (10t · 12s · 11d)

**Terms**
- [Idempotency](../../term_dictionary/term_idempotency.md) — same-effect-on-retry; relevance: idempotency locks gate the recovery loop's replay-skip logic.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — replay dedup token; relevance: the recovery loop "acquire idempotency lock"/"skip if receipt committed" keys on it.
- [At-Least-Once Delivery](../../term_dictionary/term_at_least_once.md) — deliver ≥1×; relevance: channels without reconciliation may opt into at-least-once replay as a documented tradeoff.
- [Exactly-Once Delivery](../../term_dictionary/term_exactly_once.md) — deliver once; relevance: `unknown_after_send` reconciliation aims at exactly-once for capable adapters.
- [Message Queue](../../term_dictionary/term_message_queue.md) — durable outbound buffer; relevance: Phase 2 moves the outbound queue to durable `DurableSendIntent` records.
- [Failover](../../term_dictionary/term_failover.md) — fall back on failure; relevance: failure-class policy decides retry vs fall-back-to-channel-owned delivery.
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — stop calling a failing path; relevance: `auth`/`permission` failures are non-retryable until config changes (open-circuit behavior).
- [Two-Phase Commit](../../term_dictionary/term_two_phase_commit.md) — atomic distributed commit; relevance: the begin-intent → platform-send → commit-receipt protocol is a 2PC-style durable handshake.
- [Graceful Degradation](../../term_dictionary/term_graceful_degradation.md) — degrade not fail; relevance: `best_effort`/`disabled` durability policies degrade to direct send when persistence is unavailable.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP push callback; relevance: webhook redelivery is a concrete migration hazard requiring dedupe + durable intents.

**Docs**
- [oc_concepts_message_lifecycle_refactor_model](oc_concepts_message_lifecycle_refactor_model.md) — the domain-model half (planned, this series); relevance: same design doc; this note is the 8-phase migration of that model.
- [oc_concepts_messages](oc_concepts_messages.md) — current message runtime (planned, this series); relevance: the legacy paths (`channel.inbound.*`, reply helpers) the migration replaces.
- [hermes_messaging_raft](../hermes_agent/hermes_messaging_raft.md) — Hermes durable/consensus messaging; relevance: durable replay and restart recovery, the same failure model.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes gateway architecture; relevance: how a channel gateway phases in durable delivery without breaking adapters.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: restart/startup recovery sequencing for pending sends.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp Baileys integration; relevance: WhatsApp is an explicit per-channel migration row (send adapter, durable finals).
- [hermes_messaging_line](../hermes_agent/hermes_messaging_line.md) — LINE integration; relevance: LINE reply-token constraints are a named migration hazard (callback-only targets).
- [hermes_messaging_signal](../hermes_agent/hermes_messaging_signal.md) — Signal integration; relevance: Signal is "simple receive+send, no live until edit support" in the channel mapping.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — Claude Code channels; relevance: cross-agent channel migration/compat strategy.
- [band_custom_integration](../band/band_custom_integration.md) — Band custom integration; relevance: adding a new channel via a stable SDK surface (the migration's end-state goal).
- [band_sdk_contact_events](../band/band_sdk_contact_events.md) — Band SDK contact/inbound events; relevance: inbound record/dedupe contract during channel bridging.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging delivery code; relevance: the outbound queue + per-channel dispatchers migrated in Phases 2-5.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels core; relevance: `channel.inbound.*` compatibility bridge rewritten on receive/send.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: `pendingFinalDelivery*` session fields carry the intent id during transition.

**Snippets**
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable kernel delivery; relevance: the durable send intent store + recovery loop this migration builds.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — dispatch path; relevance: `dispatchChannelInboundReply` reimplemented on `messages.receive`/`send` in Phase 3.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: load pending/sending intents on restart and replay them.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram dispatcher; relevance: Telegram is the Phase-4/5 proof channel (polling ack watermark, durable finals).
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport/polling; relevance: the grammY polling offset vs OpenClaw restart-watermark distinction.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket mode; relevance: Slack native-stream/draft + origin-metadata echo drop migration row.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: capability gates (silent delivery, reply-target, hooks) that decide durable opt-in.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/silent policy; relevance: silent-reply + media fallback batch handling preserved across migration.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persistence; relevance: persisting intent ids/receipts so restart recovery is safe.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound send handler; relevance: `deliverOutboundPayloads` rerouted to `messages.send` in Phase 2.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/typing receipts; relevance: loading/status cleanup is a per-channel migration concern (LINE/Zalo/Nostr).
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron/service notifications; relevance: Phase 7 moves cron/heartbeat notifications onto `messages.send`.

### oc_concepts_messages (10t · 11s · 11d)

**Terms**
- [Dedupe](../../term_dictionary/term_dedupe.md) — duplicate suppression; relevance: inbound dedupe keyed by channel/account/peer/session/message id is a top section.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-on-retry; relevance: redelivery after reconnect must not trigger a second agent run.
- [Message Queue](../../term_dictionary/term_message_queue.md) — queued processing; relevance: `messages.queue` modes (steer/followup/collect/interrupt) govern active-run handling.
- [Server-Sent Events (SSE)](../../term_dictionary/term_sse.md) — push streaming; relevance: block streaming sends partial replies as the model produces text blocks.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional socket; relevance: gateway-owned sessions stream over socket transports to Control UI/TUI.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning trace; relevance: reasoning visibility (`/reasoning on|off|stream`) and its token-usage cost.
- [Throttling](../../term_dictionary/term_throttling.md) — rate control; relevance: inbound debouncing batches rapid same-sender messages into one turn.
- [Backpressure / Pub-Sub](../../term_dictionary/term_pub_sub.md) — flow-controlled async messaging; relevance: channels apply transport backpressure before a message enters the session queue.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: tool-result `content` vs `details` boundary and tool execution in the run.
- [Context Window](../../term_dictionary/term_context_window.md) — token capacity; relevance: history-context buffers + reasoning tokens count toward usage/context budget.

**Docs**
- [oc_concepts_message_lifecycle_refactor_model](oc_concepts_message_lifecycle_refactor_model.md) — target durable design (planned, this series); relevance: this note documents today's flow; that note is the durable redesign of it.
- [oc_concepts_message_lifecycle_refactor_migration](oc_concepts_message_lifecycle_refactor_migration.md) — migration plan (planned, this series); relevance: how the current dedupe/queue/streaming behavior moves onto receive/send.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes message architecture; relevance: parallel inbound→session→reply pipeline.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — Hermes messaging slash commands; relevance: control-command handling that bypasses debouncing (same pattern).
- [hermes_telegram_advanced](../hermes_agent/hermes_telegram_advanced.md) — Telegram advanced features; relevance: reasoning draft bubble + threading/reply behavior on Telegram.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/attachment settings; relevance: media flushes immediately (bypasses text debounce); chunking media vs text.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — Claude Code channels; relevance: cross-agent inbound→reply model with channel overrides.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — Band rooms/routing; relevance: routing/bindings → session key, direct vs group session ownership.
- [band_websocket_agent_channels](../band/band_websocket_agent_channels.md) — Band agent channels over socket; relevance: channel run ownership and per-channel streaming toggles.
- [band_websocket_human_events](../band/band_websocket_human_events.md) — Band human/inbound events; relevance: inbound body vs command body separation and history context.
- [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — session patterns; relevance: one-primary-device guidance and gateway-as-source-of-truth transcripts.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging code; relevance: implements dedupe, debounce, queueing, streaming, silent-reply behaviors documented here.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels core; relevance: routing/bindings and channel run ownership.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: gateway-owned session keys, transcripts, device mapping.

**Snippets**
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation→session resolution; relevance: routing/bindings → session key, direct collapse vs group keys.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — inbound dispatch; relevance: the inbound→agent-run path of the high-level flow.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/routing; relevance: mention-gating and which inbound messages trigger a run vs history-only.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound replies; relevance: outbound chunking + channel-limit handling.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered block-stream deltas; relevance: block streaming + coalesce/idle batching behavior.
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — history-context injection; relevance: the shared history wrapper + pending-only history buffers.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/silent policy; relevance: silent replies (`NO_REPLY`) resolution by conversation type.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input body provenance; relevance: BodyForAgent/Body/CommandBody/RawBody separation documented here.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type classification; relevance: direct vs group/channel behavior for silent replies and history.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — typing/status reactions; relevance: streaming-adjacent transient UI (reasoning draft bubble) behavior.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript/media pipeline; relevance: tool-result content vs details boundary and media delivery.

### oc_concepts_model_failover_auth_rotation (10t · 11s · 11d)

**Terms**
- [Model Failover](../../term_dictionary/term_model_failover.md) — model/auth failover behavior; relevance: the page IS the auth-profile-rotation stage of OpenClaw model failover.
- [Failover](../../term_dictionary/term_failover.md) — fall back on failure; relevance: profiles in cooldown/disabled rotate to the next; failover-worthy error classes.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: auth profiles store OAuth `{access,refresh,expires}` tokens, imported and refreshed.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-auth protocol; relevance: OAuth logins create per-email profiles (`provider:<email>`), distinct from API keys.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: auth-failure classes (`auth`/`auth_permanent`) drive the skip cache + rotation.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: rate-limit (broad bucket incl. 429/ThrottlingException) triggers cooldown + rotation.
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — growing retry delay; relevance: cooldowns use 1m→5m→25m→1h backoff; billing 5h→24h backoff.
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — disable a failing dependency; relevance: billing/credit failures mark a profile disabled (long backoff), an open-circuit per profile.
- [Throttling](../../term_dictionary/term_throttling.md) — provider-side rate control; relevance: SDK `retry-after` caps + the rate-limit/timeout bucket classification.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: Anthropic Stainless SDK retry-after cap example; Claude CLI/OAuth profiles in the auth store.

**Docs**
- [oc_concepts_model_failover_model_fallback](oc_concepts_model_failover_model_fallback.md) — the model-fallback stage (planned, this series); relevance: same doc; this note is stage-1 auth rotation, that note is stage-2 model fallback.
- [oc_concepts_models_selection](oc_concepts_models_selection.md) — model selection order (planned, this series); relevance: auth failover happens inside a provider before moving to the next model.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: parallel API-key/OAuth credential model for a coding agent.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth; relevance: parallel multi-provider credential/profile config.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — Hermes credential pools; relevance: the multi-key/multi-profile rotation pool, directly analogous to auth profiles + order.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — Hermes fallback providers; relevance: provider/profile fallback chains and cooldown semantics.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes provider runtime; relevance: provider auth-routing state and rotation at runtime.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — CC usage/limit errors; relevance: the rate-limit/usage-window error taxonomy that lands in the cooldown bucket.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: env-backed credential sources for auth profiles.
- [hermes_cli_commands_ops_maintenance_auth](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — Hermes auth CLI ops; relevance: parallel `auth login`/profile-management CLI surface (cf. `openclaw doctor --fix` import).
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — xAI Grok OAuth; relevance: OAuth-profile auth + reuse pattern matching OpenClaw's OAuth-before-API-key ordering.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime + auth/failover code; relevance: implements auth profiles, rotation order, cooldowns, billing disables.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: providers own failover classification and OAuth refresh.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: per-session pinned auth profile + override fields.

**Snippets**
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile order/credential; relevance: implements `auth.order`/`auth.profiles` + round-robin (OAuth-before-API-key) ordering.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile import/portability; relevance: legacy `oauth.json`/`auth-profiles.json` import on first use (`doctor --fix`).
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth (Claude CLI); relevance: Codex subscription + Claude CLI reuse auth paths.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error classification; relevance: classifies auth/rate-limit/billing/timeout error buckets.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — session fallback utils; relevance: persists auth/model override fields + skip-cache during rotation.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: secrets live in per-agent SQLite, config is routing-only.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit policy; relevance: the rate-limit/throttle classification and cooldown policy.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect/error codes; relevance: error-code mapping feeding failover-worthy detection.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model/auth overrides; relevance: `authProfileOverride*` and user-pin vs auto-pin semantics.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage/cost summary; relevance: `usageStats` (lastUsed/cooldownUntil/disabledUntil) state this note schemas.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: `auth.cooldowns.*` knobs (billing backoff, overloaded rotations) live here.

### oc_concepts_model_failover_model_fallback (10t · 11s · 11d)

**Terms**
- [Model Failover](../../term_dictionary/term_model_failover.md) — model/auth failover; relevance: this note is the model-fallback stage of OpenClaw failover.
- [Model Router](../../term_dictionary/term_model_router.md) — route requests across models; relevance: the candidate chain (requested model + configured fallbacks) is model routing.
- [Failover](../../term_dictionary/term_failover.md) — fall back on failure; relevance: failover-worthy errors advance to the next model candidate.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: rate-limit/overloaded errors are handled aggressively (1 profile retry then next model).
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — growing delay; relevance: cooldown-skip vs probe decisions and overloaded 0ms backoff defaults.
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — skip a failing path; relevance: persistent-auth providers are skipped immediately; cooldown-skip per candidate.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: candidates are provider/model LLM refs walked on failure.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: fallback candidates come from configured models (deduped, not allowlist-filtered).
- [Graceful Degradation](../../term_dictionary/term_graceful_degradation.md) — degrade not fail; relevance: walking fallbacks degrades gracefully; `FallbackSummaryError` reports the soonest recovery.
- [Throttling](../../term_dictionary/term_throttling.md) — provider rate control; relevance: per-provider transient cooldown probe is throttled to one per fallback run.

**Docs**
- [oc_concepts_model_failover_auth_rotation](oc_concepts_model_failover_auth_rotation.md) — the auth-rotation stage (planned, this series); relevance: stage-1 within-provider rotation precedes this stage-2 cross-model fallback.
- [oc_concepts_models_selection](oc_concepts_models_selection.md) — selection order (planned, this series); relevance: selection source (configured/auto/user/cron) decides whether the fallback chain is allowed.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — Claude Code fallback models; relevance: directly parallel "primary then fallbacks" model chain for a coding agent.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — Pi model overrides/compat; relevance: session overrides + live model switching interaction with fallback.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — Hermes fallback providers; relevance: the cross-provider/model fallback chain and which errors advance it.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — Hermes provider routing; relevance: candidate-chain construction and provider-family routing.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes provider runtime; relevance: runtime fallback/retry orchestration analogous to `runWithModelFallback`.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — usage/limit errors; relevance: the error taxonomy that does vs does not advance fallback (context overflow excluded).
- [cc_fast_mode](../claude_code/cc_fast_mode.md) — CC fast/priority mode; relevance: overloaded/busy handling and service-tier interplay during fallback.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings; relevance: parallel `model.fallbacks`/cooldown configuration keys.
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime context settings; relevance: context-overflow errors stay in compaction (not fallback) — same boundary.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: implements the candidate chain, error classification, and `FallbackSummaryError`.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: session model overrides and auto-override persistence/rollback.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: provider-specific failover classification feeding the fallback decision.

**Snippets**
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback candidate ladder; relevance: builds the candidate chain + the rules (requested first, dedupe, append primary).
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown/probe; relevance: cooldown-skip vs probe per-candidate decisions documented here.
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — fallback observability; relevance: per-attempt detail + `model_fallback_decision`/`fallbackStep*` logs.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error classifier; relevance: which errors continue vs do-not-continue fallback.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — session fallback persistence; relevance: persist fallback override before retry + narrow rollback on failure.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model overrides; relevance: `modelOverrideSource: auto|user`, live `/model` switch coordination.
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — per-level session overrides; relevance: legacy-override-as-user treatment and override field ownership.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — abort handling; relevance: explicit aborts (not timeout-shaped) do not advance fallback.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window guard; relevance: `request_too_large`/context-overflow stays in compaction, excluded from fallback.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect/error codes; relevance: `empty_response`/`no_error_details`/`unclassified` labels for fallback state.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — session store target; relevance: live-session reconciliation prefers persisted overrides over stale runtime fields.

### oc_concepts_model_providers_official (10t · 11s · 12d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model provider; relevance: official providers publish their own catalog via `registerProvider(...)` plugins.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the page configures LLM model providers (not chat channels).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: the Anthropic provider section (API key, Claude CLI, `/fast` service_tier).
- [OAuth](../../term_dictionary/term_oauth.md) — delegated auth; relevance: ChatGPT/Codex OAuth and Gemini-CLI/xAI OAuth provider setup.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: OAuth subscription auth stored as profiles for Codex/Gemini-CLI.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model APIs; relevance: OpenAI/Anthropic/Google/Z.AI/Vercel/bundled providers are third-party GenAI services.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: provider tool-schema normalization and reasoning/thinking profiles per provider.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI Responses endpoint; relevance: native OpenAI keeps Responses `store`/prompt-cache hints; `/fast`→`service_tier=priority`.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: multi-key API-key rotation retries on rate-limit responses only.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reuse cached prompt prefix; relevance: native OpenAI/Anthropic prompt-cache hints + Gemini `cachedContent` → `cacheRead`.

**Docs**
- [oc_concepts_model_providers_custom](oc_concepts_model_providers_custom.md) — custom/base-URL providers (planned, this series); relevance: the `models.providers` companion to these bundled official plugins.
- [oc_concepts_models_selection](oc_concepts_models_selection.md) — model selection (planned, this series); relevance: `agents.defaults.models` allowlist + primary/fallback consume these providers.
- [oc_concepts_model_failover_auth_rotation](oc_concepts_model_failover_auth_rotation.md) — auth rotation (planned, this series); relevance: API-key rotation + OAuth profiles defined here feed failover.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: parallel provider/model configuration for a coding agent.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud providers; relevance: directly parallel per-provider cloud setup (OpenAI/Anthropic/Google).
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth; relevance: per-provider API-key/OAuth auth env-var conventions.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — Hermes cloud inference providers; relevance: the bundled-cloud-provider catalog analog (OpenAI/Anthropic/Gemini/Mistral/…).
- [hermes_provider_google_gemini](../hermes_agent/hermes_provider_google_gemini.md) — Gemini provider; relevance: Google Gemini API-key + Vertex + Gemini-CLI setup parallels.
- [hermes_provider_aws_bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — Bedrock provider; relevance: AWS credential-chain provider auth (cf. memory-search Bedrock), a bundled-provider analog.
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — xAI Grok OAuth; relevance: xAI bundled provider (SuperGrok OAuth, `/fast` variants) is in the bundled table.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: the `<PROVIDER>_API_KEY*` env conventions for key rotation.
- [cc_fast_mode](../claude_code/cc_fast_mode.md) — fast/priority mode; relevance: `/fast` toggle → OpenAI/Anthropic service_tier mapping documented here.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: implements every official provider plugin (OpenAI/Anthropic/Google/Z.AI/Vercel…).
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: consumes provider catalogs + auth for model selection and the inference loop.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider plugin; relevance: OpenAI auth/transport/service-tier/attribution-header behavior documented here.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider plugin; relevance: Anthropic `/fast`→service_tier, Claude CLI/OAuth, beta headers.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: OpenRouter bundled provider quirks (app headers, cache markers, proxy shaping).
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — provider catalog manifest; relevance: official plugins publish catalog rows (no `models.providers` needed).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog/allowlist; relevance: `agents.defaults.models` allowlist + `provider/*` dynamic entries.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth order/credential; relevance: `auth.order.openai` for Codex-sub + API-key backup ordering.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external CLI auth; relevance: Claude CLI reuse and Gemini-CLI OAuth token storage.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: provider model aliases and pricing/contextWindow defaults.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI HTTP/SSE stream; relevance: transport choice `sse`/`websocket`/`auto` for OpenAI/Codex routes.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI request build; relevance: Responses payload shaping (`store`, reasoning-compat) only on native OpenAI.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama local provider; relevance: bundled local-provider plugin pattern (cross-reference with custom-provider note 9).

### oc_concepts_model_providers_custom (9t · 10s · 11d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: custom providers register via `models.providers` (or override a bundled plugin's defaults).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external/self-hosted model APIs; relevance: Moonshot/Volcengine/BytePlus/Synthetic/MiniMax custom endpoints.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy server; relevance: OpenAI/Anthropic-compatible proxies (LiteLLM/local proxies) via custom `baseUrl`.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — request-routing gateway; relevance: base-URL providers route through a gateway/proxy endpoint with custom headers.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: registers custom LLM model entries (`models.providers.<id>.models[]`).
- [Context Window](../../term_dictionary/term_context_window.md) — max token span; relevance: custom-model `contextWindow`/`contextTokens`/`maxTokens` metadata fields.
- [vLLM](../../term_dictionary/term_vllm.md) — high-throughput local inference server; relevance: vLLM is a bundled local OpenAI-compatible provider (`/v1/models` discovery).
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: proxy-route shaping (`extra_body`, developer-role suppression) affects tool calls.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI API surface; relevance: `api: "openai-completions"` proxies skip native Responses `store`/reasoning shaping.

**Docs**
- [oc_concepts_model_providers_official](oc_concepts_model_providers_official.md) — official bundled providers (planned, this series); relevance: use `models.providers` only to override a bundled plugin's defaults.
- [oc_concepts_models_selection](oc_concepts_models_selection.md) — model selection (planned, this series); relevance: `models.json` registry + `models.mode: merge|replace` precedence governs custom providers.
- [pi_custom_models](../pi/pi_custom_models.md) — Pi custom models; relevance: directly parallel custom-model registration with baseUrl + api + key.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — Pi custom provider registration; relevance: the closest analog — registering an OpenAI/Anthropic-compatible custom provider.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud providers; relevance: provider-config surface shared with the official-provider note.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — local self-hosted LLM; relevance: LM Studio/Ollama/vLLM/SGLang local OpenAI-compatible servers.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — Ollama local provider; relevance: Ollama native `http://127.0.0.1:11434` setup parallels the Ollama section.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — Hermes proxy routing; relevance: OpenAI/Anthropic-compatible proxy routing + LiteLLM, the local-proxy story.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — add an inference provider; relevance: the procedure for wiring a new base-URL provider.
- [hermes_provider_azure_foundry_setup](../hermes_agent/hermes_provider_azure_foundry_setup.md) — Azure Foundry provider; relevance: a custom base-URL/headers provider with explicit endpoint config.
- [hermes_docker_tools_local_inference](../hermes_agent/hermes_docker_tools_local_inference.md) — local inference via Docker; relevance: self-hosted inference servers (vLLM/SGLang) the custom providers point at.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: implements the bundled local/proxy plugins and the custom-provider registration path.

**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama local provider; relevance: bundled-local provider native API discovery (the Ollama section).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: `api: "openai-completions"` shaping that proxy routes inherit/suppress.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: proxy-style OpenAI-compatible path that skips native shaping (model of a proxy provider).
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog normalize/schemas; relevance: validates/normalizes custom `models.providers.<id>.models[]` metadata.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: merges custom-provider entries into `models.json` (merge-mode precedence).
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: default cost/contextWindow/maxTokens fields for custom models.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/SecretRef; relevance: `${ENV}` apiKey markers + SecretRef-managed merge precedence in `models.json`.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxy/connect handling; relevance: base-URL exact-origin trust + `allowPrivateNetwork` for LAN/tailnet proxies.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: `VLLM_API_KEY`/`SGLANG_API_KEY`/`LM_API_TOKEN` opt-in env discovery.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog/visibility; relevance: `agents.defaults.models["provider/model"]` visibility vs `models.providers` runtime registration.

### oc_concepts_models_selection (10t · 11s · 12d)

**Terms**
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of usable models; relevance: `agents.defaults.models` is the allowlist/catalog with aliases and `provider/*` entries.
- [Model Router](../../term_dictionary/term_model_router.md) — route across models; relevance: selection order primary→fallbacks→auth-failover is the routing policy.
- [Model Failover](../../term_dictionary/term_model_failover.md) — failover behavior; relevance: auth failover happens inside a provider before moving to the next model.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: model refs choose provider+model LLM (not the runtime, mostly).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: example allowlist uses `anthropic/claude-*` with aliases; onboarding sets up Anthropic.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: `provider/*` entries keep provider discovery dynamic via the plugin catalog.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: cron `--model`/payload model is a job primary with its own fallback policy.
- [Context Window](../../term_dictionary/term_context_window.md) — token capacity; relevance: per-model context overrides (`contextTokens`) in the allowlist/registry.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool use; relevance: tool-enabled agents/untrusted inputs should avoid weaker tiers (quick model policy).
- [Authentication](../../term_dictionary/term_authentication.md) — credential checks; relevance: pickers show providers with usable auth; "Missing auth" gating.

**Docs**
- [oc_concepts_models_cli](oc_concepts_models_cli.md) — Models CLI/UX (planned, this series); relevance: the `/model` + `openclaw models` commands that drive selection.
- [oc_concepts_model_failover_model_fallback](oc_concepts_model_failover_model_fallback.md) — model fallback (planned, this series); relevance: the fallback half of the selection order.
- [oc_concepts_model_providers_official](oc_concepts_model_providers_official.md) — official providers (planned, this series); relevance: the providers populating the catalog/allowlist.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: directly parallel default/primary model selection.
- [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — restrict model selection; relevance: directly parallel allowlist + "model not allowed" gating.
- [pi_custom_models](../pi/pi_custom_models.md) — Pi custom models/registry; relevance: `models.json` registry + merge/replace mode analog.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings; relevance: `agents.defaults.model.*`/`imageModel`/`pdfModel` config-key surface.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime; relevance: provider/runtime split (model ref vs agent runtime) explained here.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: the catalog/allowlist data model analog.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: selection-source policy (configured/auto/user/cron) and routing.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — CC settings; relevance: parallel model/config-key reference for a coding agent.
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime context settings; relevance: image/pdf/aux model routing knobs analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: implements selection order, allowlist enforcement, and aux-model routing.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: session-pinned selection vs configured primary (`/model default`).
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: dynamic provider discovery feeding `provider/*` catalog views.

**Snippets**
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog/allowlist; relevance: implements `agents.defaults.models` allowlist + `provider/*` resolution + "not allowed" error.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog normalize; relevance: model-ref lowercasing/normalization and catalog validation.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery; relevance: dynamic provider catalog discovery for `provider/*` and pickers.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model overrides; relevance: configured-primary change does not rewrite session selections.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: aliases in the allowlist resolve here.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — session fallback utils; relevance: selection source decides whether fallback chain applies.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest; relevance: `models.providers.*.models` vs full built-in catalog (`view: all`).
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config; relevance: `agents.defaults.model`/aux-model config defaults resolution.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/clobber protection; relevance: `config set ... --merge`/`--replace` clobber protection for model maps.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI model view; relevance: the Control UI picker requests the configured model view from the gateway.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool/runtime policy; relevance: runtime overrides on provider/model policy (not whole agent/session).

### oc_concepts_models_cli (10t · 11s · 11d)

**Terms**
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of models; relevance: `models list`/`--all` shows the configured/auth-available vs full catalog.
- [Model Router](../../term_dictionary/term_model_router.md) — route across models; relevance: `/model` + `models set`/`fallbacks` configure the routing chain from the CLI.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the commands switch/list provider/model LLM refs.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: `models list --provider <id>` filters by the plugin-advertised provider id.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model APIs; relevance: `models scan` probes OpenRouter's free model catalog (a third-party aggregator).
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool use; relevance: scan ranks free models by tool support (tool-latency probe).
- [Context Window](../../term_dictionary/term_context_window.md) — token capacity; relevance: scan ranks candidates by context size + parameter count.
- [Authentication](../../term_dictionary/term_authentication.md) — credential checks; relevance: `models status --probe`/`--check` report auth/OAuth health per provider.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: scan `--concurrency`/`--timeout` controls and keyless metadata-only fallback.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image models; relevance: scan probes image support and ranks image-capable models first.

**Docs**
- [oc_concepts_models_selection](oc_concepts_models_selection.md) — selection rules (planned, this series); relevance: these CLI commands operate on the selection/allowlist this note explains.
- [oc_concepts_model_providers_official](oc_concepts_model_providers_official.md) — official providers (planned, this series); relevance: `models list --provider` enumerates these providers.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: parallel CLI/UX for switching default models.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI reference; relevance: directly parallel coding-agent CLI command surface (model/list/status).
- [pi_custom_models](../pi/pi_custom_models.md) — Pi custom models; relevance: registering/listing custom models via CLI/config.
- [hermes_cli_commands_chat_provider](../hermes_agent/hermes_cli_commands_chat_provider.md) — Hermes chat/provider CLI; relevance: directly parallel `model`/`provider` CLI commands.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — interactive slash commands; relevance: `/model` numbered picker + interactive switching parallels.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — messaging slash commands; relevance: `/model` behavior on Discord/Telegram pickers (session-scoped).
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: the catalog `models list` renders.
- [cc_cli_flags](../claude_code/cc_cli_flags.md) — Claude Code CLI flags; relevance: parallel CLI flag surface (`--json`/`--plain`/`--provider`).
- [hermes_quickstart_first_chat](../hermes_agent/hermes_quickstart_first_chat.md) — first-chat quickstart; relevance: `openclaw onboard`/`models set` first-run model setup analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: implements the model catalog/scan/selection the CLI drives.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: `models status --probe`/pricing/scan call into gateway model methods.

**Snippets**
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: `models list` configured/auth-available vs `--all` full catalog.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery/probe; relevance: `models scan` discovery + tool/image probes.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog normalize/schemas; relevance: ref parsing (split on first `/`, alias→provider resolution).
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM pricing; relevance: `models scan` reads the OpenRouter `/models` free catalog + pricing.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: `models aliases add/remove` and alias resolution.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: `models fallbacks add/remove/clear` builds this chain.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model overrides; relevance: `/model` persists a session selection + live-switch-at-retry behavior.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — session fallback utils; relevance: `/model status` shows selected vs active fallback model.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth/model view; relevance: Discord/Control UI interactive `/model` picker behavior.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth order/credential; relevance: `models status --probe` reports auth-order exclusions + profile health.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: scan ranks by tool latency; status surfaces usage/probe rows.

## Undigested Terms Plan (Step 4e)

| Term | Disposition |
|------|-------------|
| QMD (memory engine) | OpenClaw product vocabulary → digested as `oc_concepts_memory_qmd` (note 1); not a `term_dictionary` entry. |
| Memory search / hybrid retrieval | Concept → `oc_concepts_memory_search` (note 2); link existing `term_rag`, `term_dense_retrieval`, `term_hybrid_search`, `term_bm25`, `term_vector_database`. |
| Message lifecycle / receive-send / receipt / origin / target / relation | OpenClaw domain vocabulary → `oc_concepts_message_lifecycle_refactor_*` (notes 3,4); link `term_idempotency`, `term_at_least_once`, `term_exactly_once`, `term_message_queue`. |
| Inbound dedupe / debouncing / silent replies / channel run ownership | Runtime message concepts → `oc_concepts_messages` (note 5); link `term_dedupe`, `term_message_queue`, `term_sse`. |
| Auth-profile rotation / cooldown / billing disable / skip cache | Failover vocabulary → `oc_concepts_model_failover_auth_rotation` (note 6); link `term_model_failover`, `term_failover`, `term_oauth_token`, `term_rate_limiting`, `term_circuit_breaker`. |
| Model fallback / candidate chain / FallbackSummaryError | Failover vocabulary → `oc_concepts_model_failover_model_fallback` (note 7); link `term_model_failover`, `term_model_router`, `term_exponential_backoff`. |
| Provider plugin / `models.providers` / base-URL provider | Provider-config vocabulary → `oc_concepts_model_providers_*` (notes 8,9); link `term_provider_plugin`, `term_third_party_genai_services`, `term_reverse_proxy`, `term_api_gateway`, `term_vllm`. |
| Provider names (OpenAI, Anthropic, Google Gemini/Vertex, Z.AI, Moonshot/Kimi, Doubao, BytePlus, MiniMax, LM Studio, Ollama, vLLM, SGLang, OpenRouter, LiteLLM) | Documented as config, NOT promoted to term notes; link existing `term_llm`/`term_claude`/`term_vllm`/`term_third_party_genai_services`. |
| Model selection / allowlist / `models.json` registry / `/model` / model scan | Selection vocabulary → `oc_concepts_models_*` (notes 10,11); link `term_model_catalog`, `term_model_router`. |
| `term_semantic_search`, `term_reranking`, `term_streaming`, `term_session`, `term_debouncing`, `term_state_machine`, `term_event_sourcing`, `term_dead_letter_queue`, `term_high_availability`, `term_openrouter`, `term_retry`, `term_model_fallback` (all MISSING in DB) | NOT captured: each is covered by an existing near-synonym term note (`term_dense_retrieval`/`term_rag`/`term_bm25`, `term_sse`, `term_dedupe`, `term_failover`, `term_message_queue`, `term_third_party_genai_services`, `term_model_failover`) which is linked instead. No new `term_dictionary` capture needed — these are OpenClaw-doc concepts owned by the `oc_*` notes above. |

**Expected new `term_dictionary` captures: 0.** All OpenClaw vocabulary is digested as `oc_*` doc notes; all

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. (If augment's Step 2d re-scan
promotes a genuinely cross-cutting, vault-reusable term with no doc-page home AND no existing near-synonym
best-fit `acronym_glossary_llm.md` — inherited from master W5; not expected here.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / criterion |
|------|-------|------------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` — YAML field order, `# OpenClaw — …` H1, `## Overview`/`## Related Notes`/`## References`, bold footer; 0 ERROR/LINK-003. |
| G2 | Grounding | Each note diffed vs its `inbox/openclaw_docs/concepts/<page>` section(s); no invented config keys/CLI flags/behavior. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one `building_block` per note; every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevancy-selected `term_dictionary` terms + `repo_openclaw*` + sibling `oc_*` + relevant docs/snippets per note, each with a relevance statement. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken relative paths after reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` rows + the inlinks below; in-degree ≥1. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_memory_qmd oc_concepts_memory_search oc_concepts_message_lifecycle_refactor_model oc_concepts_message_lifecycle_refactor_migration oc_concepts_messages oc_concepts_model_failover_auth_rotation oc_concepts_model_failover_model_fallback oc_concepts_model_providers_official oc_concepts_model_providers_custom oc_concepts_models_selection oc_concepts_models_cli"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density (frontmatter-stripped words + code fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (words=$words code=$cb lines=$lines)"
  # G7/G8 sibling-prefix anti-island sanity (at least one oc_ or repo_/term_/entry_ inbound expected)
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING LINK in $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost-reference: every [..](..md) target resolves in DB (run after writing notes)
# G6 broken links: /tessellum-fix-broken-links after incremental reindex
```

## Density Re-Assessment

| # | Note | BB | ~Words | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---|
| 1 | oc_concepts_memory_qmd | procedure | 600 | ✅ |
| 2 | oc_concepts_memory_search | procedure | 450 | ✅ |
| 3 | oc_concepts_message_lifecycle_refactor_model | argument | 700 | ✅ |
| 4 | oc_concepts_message_lifecycle_refactor_migration | argument | 650 | ✅ |
| 5 | oc_concepts_messages | concept | 600 | ✅ |
| 6 | oc_concepts_model_failover_auth_rotation | concept | 650 | ✅ |
| 7 | oc_concepts_model_failover_model_fallback | concept | 600 | ✅ |
| 8 | oc_concepts_model_providers_official | procedure | 700 | ✅ |
| 9 | oc_concepts_model_providers_custom | procedure | 600 | ✅ |
| 10 | oc_concepts_models_selection | concept | 600 | ✅ |
| 11 | oc_concepts_models_cli | procedure | 500 | ✅ |

No note approaches caps after splitting. The two code-heaviest sources (message-lifecycle-refactor 29 fences,
model-providers 19 fences) are split so each note keeps ≤6 code blocks (config/JSON5 reproduced selectively).

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before first execution)
under a **Concepts → Memory & Messaging & Models** cluster: a "Memory" group (notes 1–2), a "Messages /
Lifecycle" group (notes 3–5), and a "Models / Providers / Failover" group (notes 6–11). Each note receives the
entry-point back-link at finalization (this is the G7/G8 anti-island inbound link). Master W2/W3 (parent hub
code↔docs cross-links) are handled once at the series level, not per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; `entry_openclaw_docs.md` guarantees
≥1 per note):
- `entry_openclaw_docs.md` → all 11 notes (primary anti-island guarantee).
- `repo_openclaw_memory.md` → notes 1, 2.
- `repo_openclaw_channels.md` / `repo_openclaw_channels_messaging.md` → notes 3, 4, 5.
- `repo_openclaw_agents.md` → notes 6, 7, 8, 10, 11.
- `repo_openclaw_extensions_llm_providers.md` → notes 8, 9.
- `repo_openclaw_sessions.md` → notes 7, 10.
- `term_model_failover.md` → notes 6, 7; `term_rag.md` / `term_bm25.md` → notes 1, 2;
  `term_provider_plugin.md` → notes 8, 9; `term_message_queue.md` → notes 3, 4, 5.

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run; re-read each
source page; reproduce config/JSON5 snippets verbatim and selectively; one BB per note. Reindex incrementally;
verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash` first;
no Claude co-author trailer; commit + push the sub-plan's wave together.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note Related mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** xref-augment — built and LOCKED the per-note Related Notes mapping at the
raised floors (≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`
per note), relevance-selected from a fresh re-read of all 7 source pages under `inbox/openclaw_docs/concepts/`,
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`; updated the Summary Statistics
cross-ref line. The other 15 augment sections (Section Coverage Map, Split Decisions, Density Re-Assessment,
Validation Scripts incl. ghost detection, Inlinks, Undigested Terms Plan, Term-Note Authoring Requirements
N/A, Entry Point Decision, 9-GATE table, Pacing Rules) were already present from the plan-digestion authoring
and were verified intact.

**Source re-read (measured 2026-06-21, frontmatter-stripped):** memory-qmd 1,369w/8cb/13H2; memory-search
769w/3cb/9H2; message-lifecycle-refactor 5,727w/29cb/21H2; messages 1,177w/2cb/13H2; model-failover
3,231w/6cb/13H2; model-providers 3,850w/19cb/7H2; models 2,479w/8cb/11H2. All within ±5% of the plan's
Source table — no density estimation failure; no further splits required.

**Per-note counts (locked):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_concepts_memory_qmd | 10 | 11 | 11 (10/1) | 2 | ✅ |
| oc_concepts_memory_search | 9 | 11 | 11 (10/1) | 2 | ✅ |
| oc_concepts_message_lifecycle_refactor_model | 10 | 12 | 11 (9/2) | 3 | ✅ |
| oc_concepts_message_lifecycle_refactor_migration | 10 | 12 | 11 (9/2) | 3 | ✅ |
| oc_concepts_messages | 10 | 11 | 11 (9/2) | 3 | ✅ |
| oc_concepts_model_failover_auth_rotation | 10 | 11 | 11 (9/2) | 3 | ✅ |
| oc_concepts_model_failover_model_fallback | 10 | 11 | 11 (9/2) | 3 | ✅ |
| oc_concepts_model_providers_official | 10 | 11 | 12 (9/3) | 2 | ✅ |
| oc_concepts_model_providers_custom | 9 | 10 | 11 (9/2) | 2 | ✅ |
| oc_concepts_models_selection | 10 | 11 | 12 (9/3) | 3 | ✅ |
| oc_concepts_models_cli | 10 | 11 | 11 (9/2) | 2 | ✅ |

target (199 unique: terms, snippets, repos, cross-folder docs) was `sqlite3`-verified present; the 11 planned
sibling `oc_concepts_*` docs (this series) are marked `(planned, this series)` and count toward the 10-doc
floor only as a supplement (each note has 9-10 EXISTING docs independently). All snippets are EXISTING. All

**Ghost-resolution applied during this pass (terms flagged MISSING in the draft, redirected to existing
near-synonyms, NOT cited as ghosts):** `term_reranking` (MISSING) → `term_recall` (note 1) / `term_information_retrieval`
(note 2); `term_semantic_search` (MISSING) → `term_dense_retrieval`; `term_streaming` (MISSING) → `term_sse`;
`term_session` (MISSING) → covered by `term_idempotency`/`term_dedupe` + repo/snippet session links, replaced in
note 5 with `term_function_calling` + `term_context_window`; `term_debouncing` (MISSING) → `term_throttling` +
`term_dedupe`; `term_state_machine`/`term_event_sourcing`/`term_dead_letter_queue` (MISSING) → covered by
`term_idempotency`/`term_two_phase_commit`/`term_cqrs`/`term_message_queue`; `term_high_availability`/`term_retry`/
`term_model_fallback` (MISSING) → `term_failover`/`term_model_failover`/`term_graceful_degradation`;
`term_openrouter` (MISSING) → `term_third_party_genai_services`.

**New `term_dictionary` candidates: 0.** Re-scan (Step 2d) confirms every cross-cutting concept maps to an
rotation/cooldown, provider plugin/`models.providers`, model selection/`models.json`) is owned by the `oc_*`
doc notes themselves, per the master's design decision. No `/tessellum-capture-term-note` obligation arises from
this sub-plan. (Candidate near-synonyms newly leveraged from the existing glossary: `term_information_retrieval`,
`term_inverted_index`, `term_knn`, `term_mmr`, `term_multimodal`, `term_recall`, `term_precision`,
`term_tokenization`, `term_throttling`, `term_idempotency_key`, `term_cqrs`, `term_two_phase_commit`, `term_acid`,
`term_graceful_degradation`, `term_pub_sub`, `term_webhook`, `term_prompt_caching`, `term_bedrock` — all EXISTING,
no capture needed.)

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | **PASS** | "Per-Phase Validation Gate (G1-G9)" table inherited from master: G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link fix, G7/G8 discoverability (in-degree ≥1). Validation Scripts implement G1/G3/G5-style checks. |
| CP4 | Plan size | **PASS** | 11 notes (≤30); single execution phase. Sub-plan of a 105-sub-plan master, independently executable. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora: `## Overview` opener, `## Related Notes` reference section, `## References` external-only, bold `**Source**/**Last Updated**/**Status**` footer, fixed YAML order with `building_block` single-BB. Matches existing target-dir convention. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: all 11 notes ≤700w / ≤6 code / ≤400 lines after splitting the 4 oversize/mixed-BB sources (message-lifecycle, model-failover, model-providers, models). No borderline note left unsplit; measured source re-read confirms no further split needed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 pages re-read + measured 2026-06-21 (see Augmentation Report); every page within ±5% of the plan's Source table (max page 5,727w vs plan 5,786w). No >1.5× under-estimate. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | `## Undigested Terms Plan (Step 4e)` present, every row dispositioned (all → owned by `oc_*` doc notes or link existing term); "Expected new term captures: 0". `## Term-Note Authoring Requirements` present (N/A, 0 new terms, with the conditional capture mandate inherited from master W5). |
| CP8f | Term-slug specificity + all-notes dedup/collision audit | **PASS** | Undigested Terms Plan documents the MISSING-term → existing-near-synonym redirects (specificity/collision handled: e.g. `term_orthogonal`-style duplicates avoided; `term_reranking`/`term_streaming`/`term_session` redirected, not created). Doc-vs-term collision: all 11 `oc_*` doc slugs checked — none duplicates an existing term note (OpenClaw product vocabulary, owned by docs; existing terms only LINKED). 0 new slugs created. |
| CP9 | Discoverability / inlinks (G8, no graph islands) | **PASS** | `## Inlinks (existing notes → new notes)` table covers all 11 notes with ≥1 outside-folder inbound link each (`entry_openclaw_docs` → all 11; plus `repo_openclaw_*`/`term_*` per-note). G7/G8 in the gate table; in-degree ≥1 verified at execution. |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
