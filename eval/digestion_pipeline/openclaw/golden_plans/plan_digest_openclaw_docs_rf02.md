---
title: Sub-Plan rf02 — OpenClaw Docs: Reference (validation, memory config, caching, perf sweep, output/RPC protocols, secrets)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["reference/full-release-validation", "reference/memory-config", "reference/prompt-caching", "reference/release-performance-sweep", "reference/rich-output-protocol", "reference/rpc", "reference/secret-placeholder-conventions"]
---

# Sub-Plan rf02: Reference

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create,
> 9-GATE validation, undigested-terms policy (OpenClaw vocab → `oc_` notes, link existing terms), and
> cross-references are ALL inherited from the master; this file re-measures its 7 pages and locks notes.

## Scope

The 7 OpenClaw **Reference** pages in this slice — the operational reference material that the concepts /
gateway / CLI / providers docs point to for exact configuration and protocol detail: (1) the **Full Release
Validation** release-gate workflow, (2) the exhaustive **memory configuration** knob reference (embedding
providers, hybrid search, QMD backend, multimodal, dreaming), (3) the **prompt-caching** tuning reference
(cache retention, provider behavior, diagnostics), (4) the May-2026 **release performance sweep** evidence
(perf, package size, dependencies, shrinkwrap), (5) the **rich output protocol** (embed/media/audio render
directives), (6) the **RPC adapter** patterns for external CLIs (signal-cli, imsg), and (7) the
**secret-placeholder conventions** for docs. **Priority P2** (Phase B). The reference pages are leaf
documents the higher-priority concept/gateway notes link to; the heaviest single note (memory config) is
the operational counterpart of `repo_openclaw_memory` (LINKED, not recreated).

**Source**: OpenClaw docs, 7 pages, 10,574 measured words. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| full-release-validation | reference/full-release-validation | 1,942 | 1 | 8 | 0 | procedure |
| memory-config | reference/memory-config | 3,524 | 6 | 14 | 7 | procedure (split: search/providers vs storage/QMD/dreaming) |
| prompt-caching | reference/prompt-caching | 2,072 | 8 | 9 | 18 | procedure |
| release-performance-sweep | reference/release-performance-sweep | 2,278 | 0 | 8 | 4 | argument |
| rich-output-protocol | reference/rich-output-protocol | 445 | 3 | 3 | 0 | model |
| rpc | reference/rpc | 176 | 0 | 4 | 0 | model |
| secret-placeholder-conventions | reference/secret-placeholder-conventions | 137 | 1 | 3 | 0 | argument |

> Code counts are `grep -c '^```' / 2` (raw fence counts: 2 / 12 / 16 / 0 / 6 / 0 / 2). `memory-config`
> exceeds the 2,500-word cap and mixes two procedure clusters → split (see Split Decisions). All other pages
> are single-BB and within caps.

## Content Strategy

- **Prioritize:** the **memory configuration** reference (every memory-search deployment depends on it; it is
  the config surface behind `repo_openclaw_memory`) and the **prompt-caching** tuning reference (direct cost
  lever, the OpenClaw analog of the Claude Code caching docs). These are the two pages the rest of the corpus
  links to most.
- **Split:** `memory-config.md` (3,524w, 14 H2 / 7 H3, mixed config clusters) → a *search/embedding/provider*
  configuration note + a *storage/QMD-backend/dreaming* configuration note (word-cap + cohesion).
- **Reproduce selectively, link-out:** config snippets are reproduced verbatim but each note stays ≤6 fences
  (prompt-caching has 16 raw fences across many providers → keep the canonical knob + 2-3 provider examples,
  describe the rest in prose). Embedding-provider *credential* mechanics → link `oc_*` provider/gateway-secrets
  notes (rf03 `secretref-credential-surface`, gw `secrets`) and `term_secrets_manager`; do not redefine.
- **Do not redefine terms:** prompt caching / KV cache / embeddings / vector DB / RAG / JSON-RPC / OAuth token
  / compaction / cross-region inference / Converse API are LINKED to existing `term_dictionary` notes, never
  inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_reference_full_release_validation.md` | procedure | full-release-validation.md: all 8 H2 (Top-level stages, Release checks stages, Docker release-path chunks, Release profiles, Full-only additions, Focused reruns, Evidence to keep, Workflow files) | 650 | The Full Release Validation release-gate umbrella workflow: top-level + release-check stages, Docker release-path chunks, the smoke/stable/full release profiles, full-only additions, focused-rerun handles, evidence to retain, and the backing workflow files. |
| 2 | `oc_reference_memory_config_search.md` | procedure | memory-config.md: Provider selection, Remote endpoint config, Provider-specific config (Custom provider ids, API key resolution), Hybrid search config, Additional memory paths, Multimodal memory (Gemini), Embedding cache, Batch indexing, Session memory search (experimental), Inline embedding timeout | 750 | Configuring OpenClaw memory **search**: embedding provider/model/fallback selection, remote + provider-specific endpoint config, custom provider ids, API-key resolution, hybrid-search (FTS + vector + MMR + temporal decay), extra memory paths, multimodal (Gemini) indexing, embedding cache, batch indexing, and experimental session-memory search. |
| 3 | `oc_reference_memory_config_storage.md` | procedure | memory-config.md: SQLite vector acceleration (sqlite-vec), Index storage, QMD backend config (Full QMD example, User settings, Example), Dreaming | 600 | Configuring OpenClaw memory **storage and backends**: sqlite-vec vector acceleration, index storage location, the QMD local-first sidecar backend (full example, user settings), and the Dreaming background memory-consolidation config. |
| 4 | `oc_reference_prompt_caching.md` | procedure | prompt-caching.md: Primary knobs (cacheRetention, contextPruning.mode cache-ttl, Heartbeat keep-warm), Provider behavior (Anthropic/OpenAI/Vertex/Bedrock/OpenRouter/Gemini/others), System-prompt cache boundary, OpenClaw cache-stability guards, Tuning patterns (mixed traffic, cost-first), Cache diagnostics, Live regression tests, Quick troubleshooting | 750 | Tuning OpenClaw prompt caching: the primary knobs (`cacheRetention` global/model/per-agent, `contextPruning.mode: cache-ttl`, heartbeat keep-warm), per-provider cache behavior (Anthropic/OpenAI/Vertex/Bedrock/OpenRouter/Gemini), the system-prompt cache boundary, cache-stability guards, mixed-traffic vs cost-first tuning patterns, cache diagnostics, and quick troubleshooting. |
| 5 | `oc_reference_release_performance_sweep.md` | argument | release-performance-sweep.md: Snapshot, Install Footprint Timeline, What Changed In 5.28, Headline Numbers, Kova agent turn summary, Source probes, Install footprint audit, Supply-chain interpretation (Install footprint, npm package size, Shrinkwrap boundary) | 650 | Evidence behind the May-2026 OpenClaw performance, package-size, dependency, and shrinkwrap cleanup: the measurement snapshot and methodology, install-footprint timeline, what changed in v2026.5.28, headline perf numbers, agent-turn summary, source probes, install-footprint audit, and the supply-chain interpretation (npm size, shrinkwrap boundary). |
| 6 | `oc_reference_rich_output_protocol.md` | model | rich-output-protocol.md: intro (mediaUrl/mediaUrls, `[[audio_as_voice]]`, reply directives), `[embed ...]`, Stored rendering shape | 400 | The OpenClaw rich output protocol: the small set of delivery/render directives an assistant message can carry — structured `mediaUrl`/`mediaUrls` attachment fields, `[[audio_as_voice]]` audio-presentation hints, reply directives, the `[embed ...]` directive, and the stored rendering shape used by the Control UI. |
| 7 | `oc_reference_rpc_adapters.md` | model | rpc.md: Pattern A (HTTP daemon, signal-cli), Pattern B (stdio child process, imsg), Adapter guidelines | 350 | The two RPC adapter patterns OpenClaw uses to integrate external CLIs over JSON-RPC: Pattern A (long-running HTTP daemon, e.g. signal-cli) and Pattern B (stdio child process, e.g. imsg), plus the adapter guidelines for adding or changing a CLI integration. |
| 8 | `oc_reference_secret_placeholder_conventions.md` | argument | secret-placeholder-conventions.md: Recommended style, Avoid these patterns in docs, Example | 300 | Secret-scanner-safe placeholder conventions for OpenClaw docs and examples: the recommended human-readable placeholder style, the patterns to avoid (anything resembling a real token/key), and worked good/better examples for env-wiring docs. |

## Section Coverage Map

```
full-release-validation.md
├── Top-level stages ─────────────────────── → note 1 (oc_reference_full_release_validation)
├── Release checks stages ──────────────────── → note 1
├── Docker release-path chunks ─────────────── → note 1
├── Release profiles ───────────────────────── → note 1
├── Full-only additions ────────────────────── → note 1
├── Focused reruns ─────────────────────────── → note 1
├── Evidence to keep ───────────────────────── → note 1
└── Workflow files ─────────────────────────── → note 1
memory-config.md
├── Provider selection ─────────────────────── → note 2 (oc_reference_memory_config_search)
├── Remote endpoint config ─────────────────── → note 2
├── Provider-specific config ───────────────── → note 2
│   ├── Custom provider ids ────────────────── → note 2
│   └── API key resolution ─────────────────── → note 2
├── Hybrid search config ───────────────────── → note 2
│   └── Inline embedding timeout ───────────── → note 2
├── Additional memory paths ────────────────── → note 2
├── Multimodal memory (Gemini) ─────────────── → note 2
│   └── Full example ───────────────────────── → note 2
├── Embedding cache ────────────────────────── → note 2
├── Batch indexing ─────────────────────────── → note 2
├── Session memory search (experimental) ───── → note 2
├── SQLite vector acceleration (sqlite-vec) ── → note 3 (oc_reference_memory_config_storage)
├── Index storage ──────────────────────────── → note 3
├── QMD backend config ─────────────────────── → note 3
│   ├── Full QMD example ───────────────────── → note 3
│   ├── User settings ──────────────────────── → note 3
│   └── Example ────────────────────────────── → note 3
└── Dreaming ───────────────────────────────── → note 3
prompt-caching.md
├── Primary knobs (cacheRetention, cache-ttl,
│   Heartbeat keep-warm) ────────────────────── → note 4 (oc_reference_prompt_caching)
├── Provider behavior (Anthropic/OpenAI/Vertex/
│   Bedrock/OpenRouter/Gemini/Other/Gemini CLI) → note 4
├── System-prompt cache boundary ───────────── → note 4
├── OpenClaw cache-stability guards ────────── → note 4
├── Tuning patterns (Mixed traffic, Cost-first) → note 4
├── Cache diagnostics (cacheTrace, env toggles,
│   what to inspect) ────────────────────────── → note 4
├── Live regression tests (Anthropic/OpenAI) ─ → note 4
└── Quick troubleshooting ──────────────────── → note 4
release-performance-sweep.md
├── Snapshot ───────────────────────────────── → note 5 (oc_reference_release_performance_sweep)
├── Install Footprint Timeline ─────────────── → note 5
├── What Changed In 5.28 ───────────────────── → note 5
├── Headline Numbers ───────────────────────── → note 5
├── Kova agent turn summary ────────────────── → note 5
├── Source probes ──────────────────────────── → note 5
├── Install footprint audit (Install footprint,
│   npm package size) ───────────────────────── → note 5
└── Supply-chain interpretation (Shrinkwrap
    boundary) ───────────────────────────────── → note 5
rich-output-protocol.md
├── intro (mediaUrl/mediaUrls, audio_as_voice,
│   reply) ──────────────────────────────────── → note 6 (oc_reference_rich_output_protocol)
├── [embed ...] ────────────────────────────── → note 6
└── Stored rendering shape ─────────────────── → note 6
rpc.md
├── Pattern A: HTTP daemon (signal-cli) ─────── → note 7 (oc_reference_rpc_adapters)
├── Pattern B: stdio child process (imsg) ──── → note 7
├── Adapter guidelines ─────────────────────── → note 7
└── Related ────────────────────────────────── → note 7 (linked, not duplicated)
secret-placeholder-conventions.md
├── Recommended style ──────────────────────── → note 8 (oc_reference_secret_placeholder_conventions)
├── Avoid these patterns in docs ───────────── → note 8
└── Example ────────────────────────────────── → note 8
```
No orphaned sections. Each page's `## Related` block (where present) is rendered as `## Related Notes` links,
not duplicated content. Memory-search *credential* mechanics and gateway secrets link out to rf03 / gw notes.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| memory-config.md (3,524w, 14 H2 / 7 H3, 6 code) | note 2 (`oc_reference_memory_config_search`) + note 3 (`oc_reference_memory_config_storage`) | Exceeds the 2,500-word cap; the page covers two cohesive but distinct config clusters — (a) the *search/embedding* surface (provider selection, remote/provider config, hybrid search, multimodal, embedding cache, batch indexing) and (b) the *storage/backend* surface (sqlite-vec, index storage, QMD sidecar, Dreaming). Splitting keeps each note ≤750w, ≤6 code, single-task. |
| All other 6 pages | 1 note each | Each is single-BB and within caps (≤2,278w, fences reproduced selectively ≤6). prompt-caching (2,072w, 16 raw fences) stays one note but reproduces only the canonical knob + 2-3 provider examples; the remaining provider blocks are described in prose to stay ≤6 fences. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (10,574 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×4** (notes 1–4) · **argument ×2** (notes 5, 8) · **model ×2** (notes 6, 7).
- Est. digest words ~4,450 (avg ~556/note); all notes ≤750w, well under the 2,500w / 400-line cap.
- Source code fences: 33 raw (16.5 logical) distribute across the procedure notes; each note kept ≤6 by
  reproducing canonical config blocks verbatim and describing the rest in prose (per-provider caching blocks,
  per-provider embedding blocks).
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every note maps **≥8 relevance-selected
  `repo_openclaw*` / sibling `oc_*`. See [Per-Note Related Notes Mapping](#per-note-related-notes-mapping-locked--xref-augment-2026-06-21)
  marked "(planned, this series)" and never counted toward the ≥5-existing-docs sub-floor.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> note_id='<id>'"`). Relative paths are FROM `resources/documentation/openclaw/oc_X.md`: terms
> `../../term_dictionary/term_Y.md`; sibling oc docs (this series) `oc_Y.md`; other docs `../<folder>/<file>.md`;
> repos `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`; entry points
> `../../../0_entry_points/<file>.md`. Sibling `oc_*` docs in this series do NOT exist yet → cited as
> `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_reference_full_release_validation (8t · 10s · 10d)

**Terms**
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous-integration / continuous-delivery automation pipeline; relevance: Full Release Validation IS an orchestrated CI/CD release-gate umbrella over GitHub Actions workflows.
- [Docker](../../term_dictionary/term_docker.md) — OS-level container packaging/runtime; relevance: the release gate's Docker release-path chunks and install-smoke lanes run candidate tarballs inside Docker images.
- [npm](../../term_dictionary/term_npm.md) — Node package registry/manager; relevance: Package Acceptance packs and installs the candidate npm tarball (`release_package_spec=openclaw@…`) across the release checks.
- [DAG](../../term_dictionary/term_directed_acyclic_graph.md) — directed acyclic graph; relevance: the umbrella → child-workflow → stage structure is a DAG of jobs with rerun_group handles re-entering individual nodes.
- [SDLC](../../term_dictionary/term_sdlc.md) — software development lifecycle; relevance: full-release-validation is the pre-publish proof stage of OpenClaw's SDLC release process.
- [DevOps](../../term_dictionary/term_devops.md) — dev+ops release automation discipline; relevance: the workflow files, rerun handles, and evidence-retention are DevOps release-engineering practice.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: Docker release-path and cross-OS lanes execute the candidate in throwaway sandboxes per OS/provider.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding-agent systems; relevance: the gate validates live agent-turn behavior (Kova, Codex CLI preflight, OpenAI agent turns) of the coding agent under release.

**Docs**
- [cc_github_actions](../claude_code/cc_github_actions.md) — Claude Code GitHub Actions CI integration; relevance: closest existing analog — `gh workflow run` dispatch + workflow refs mirror full-release-validation's `gh workflow run full-release-validation.yml --ref main`.
- [cc_github_actions_cloud_providers](../claude_code/cc_github_actions_cloud_providers.md) — GitHub Actions wired to cloud providers; relevance: the release gate's provider lanes (OpenAI/Anthropic/Google/…) parallel CI matrices over providers.
- [cc_gitlab_ci_cd](../claude_code/cc_gitlab_ci_cd.md) — GitLab CI/CD pipeline integration; relevance: same release-gate pipeline shape on a different CI platform — useful contrast for the stage/rerun model.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install + post-install verification; relevance: the gate's Install Smoke / QR install / Bun global install lanes are install-verification jobs.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — container/sandbox runtime model; relevance: explains the container substrate the Docker release-path chunks run in.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/evidence collection; relevance: parallels "Evidence to keep" — release artifacts, slowest-job tables, per-lane rerun commands.
- [pi_packages](../pi/pi_packages.md) — Pi package/distribution model; relevance: candidate-package packing and published-package reuse (`pnpm ci:full-release`) is the same package-distribution concern.
- [pi_development](../pi/pi_development.md) — Pi development/build workflow; relevance: the dev→build→release pipeline this gate sits at the end of.
- [oc_reference_release_performance_sweep](oc_reference_release_performance_sweep.md) — (planned, this series) the May-2026 perf/package-size evidence; relevance: the perf-sweep numbers are produced BY this release gate's `OpenClaw Performance` workflow lanes.
- [oc_gateway_doctor](oc_gateway_doctor.md) — (planned, this series, gw slice) gateway health/doctor reference; relevance: install-smoke and source-probe `readyz`/CLI-health lanes use the doctor/health surface the gate asserts on.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw core monorepo; relevance: the `.github/workflows/*.yml` files this note documents live in this repo.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security module; relevance: release checks run security audits / dynamic-tool-drift gates that block the verifier.

**Snippets**
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security-audit probe runner; relevance: the security-audit lanes a release verifier blocks on.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — how audit checks are composed; relevance: the release-check audit composition the gate runs.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — CLI security-advisory surfacing; relevance: supply-chain advisory checks parallel the plugin-inspector-advisory artifact.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract/validation; relevance: Plugin Prerelease static checks + package fixtures validate the same contract.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/runtime lifecycle; relevance: plugins-runtime-install-a..h Docker chunks exercise this lifecycle.
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — CLI update command; relevance: package-update-{openai,anthropic,core} Docker lanes test install/update behavior.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — gateway startup/prewarm path; relevance: install-smoke + source-probe `readyz` lanes assert on startup readiness.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway health/status reporting; relevance: CLI-health and readyz probes the gate measures.
- [snippet_hermes_agent_cli_doctor_entry_early_checks](../../code_snippets/snippet_hermes_agent_cli_doctor_entry_early_checks.md) — doctor early-check entrypoint; relevance: smoke/doctor preflight before release lanes.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — install/setup wizard config; relevance: fresh-install and onboarding lanes in cross-OS/install-smoke depend on wizard setup.

### oc_reference_memory_config_search (10t · 10s · 10d)

**Terms**
- [Embedding](../../term_dictionary/term_embedding.md) — dense vector representation of text/media; relevance: this note configures the embedding provider/model/fallback that drives memory search.
- [Vector Database](../../term_dictionary/term_vector_database.md) — store + ANN query over embedding vectors; relevance: memory search runs vector queries (sqlite-vec) over embedded chunks.
- [Hybrid Search](../../term_dictionary/term_hybrid_search.md) — fused lexical (BM25) + vector retrieval; relevance: `memorySearch.query.hybrid` (vectorWeight/textWeight/candidateMultiplier) is the page's core search knob set.
- [MMR](../../term_dictionary/term_mmr.md) — Maximal Marginal Relevance re-ranking; relevance: `hybrid.mmr.enabled`/`mmr.lambda` is a directly-configured diversity re-ranker.
- [BM25](../../term_dictionary/term_bm25.md) — lexical ranking function; relevance: the `textWeight` BM25 leg of hybrid search and FTS-only fallback recall.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: memory search is the retrieval stage feeding context to the agent (covers the missing `term_semantic_search` sense).
- [Multimodal](../../term_dictionary/term_multimodal.md) — joint text/image/audio modeling; relevance: the Multimodal memory (Gemini Embedding 2) section indexes images and audio alongside Markdown.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: embedding providers (OpenAI/Gemini/Voyage/…) are LLM-vendor APIs the agent's recall depends on.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage/resolution; relevance: the API-key-resolution table (env var vs config key per provider) is the secret surface for remote embeddings.
- [Bedrock](../../term_dictionary/term_bedrock.md) — AWS Bedrock model service; relevance: the Bedrock embedding adapter (Titan/Cohere/Nova/TwelveLabs) uses the AWS SDK credential chain, a documented provider here.

**Docs**
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory model; relevance: conceptual peer of the memory surface this note configures.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory capture/recall; relevance: parallel to OpenClaw's memory_search auto-recall behavior.
- [cc_troubleshoot_memory](../claude_code/cc_troubleshoot_memory.md) — memory troubleshooting; relevance: the index-identity warning / fail-closed provider behavior here is the troubleshooting surface.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — Hermes memory-provider catalog; relevance: direct analog to the provider-selection (`provider`/`model`/`fallback`) table.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — pluggable memory-provider model; relevance: custom `models.providers.<id>` adapter resolution mirrors this plugin model.
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho memory provider; relevance: a concrete remote memory/embedding provider comparable to the remote-endpoint config.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — session search/index storage; relevance: experimental session-memory search (`sources: ["sessions"]`, deltaBytes/deltaMessages) is the same feature.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings/config reference; relevance: format peer for a config-knob reference note.
- [oc_reference_memory_config_storage](oc_reference_memory_config_storage.md) — (planned, this series) the storage/backend half of memory-config; relevance: same source page; this note links the storage knobs it splits from.
- [oc_concepts_memory_search](oc_concepts_memory_search.md) — (planned, this series, co slice) memory-search pipeline concept; relevance: the conceptual overview this config reference operationalizes.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory engine code; relevance: the code-side counterpart implementing every knob on this page.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM/embedding provider plugins; relevance: the embedding adapters (bedrock/gemini/voyage/ollama/local) live here.

**Snippets**
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent-side memory_search entry; relevance: the runtime surface this config drives.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — core memory engine; relevance: implements provider selection + hybrid query.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host embedding generation; relevance: implements the provider/model/fallback + remote-endpoint paths.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding input shaping; relevance: implements query/document `input_type` (asymmetric embeddings) config.
- [snippet_openclaw_memory_host_query_lexica](../../code_snippets/snippet_openclaw_memory_host_query_lexica.md) — lexical/FTS query path; relevance: the BM25/text leg + FTS-only fallback recall.
- [snippet_openclaw_memory_host_query_tokenizer](../../code_snippets/snippet_openclaw_memory_host_query_tokenizer.md) — query tokenizer; relevance: underlies the FTS5 tokenizer + text-weight scoring.
- [snippet_hermes_agent_core_agent_init_memory_ollama](../../code_snippets/snippet_hermes_agent_core_agent_init_memory_ollama.md) — Ollama memory init; relevance: the Ollama embedding provider + custom `models.providers.<id>` (multi-GPU host) example.

### oc_reference_memory_config_storage (8t · 10s · 10d)

**Terms**
- [sqlite-vec](../../term_dictionary/term_sqlite_vec.md) — SQLite vector-search extension; relevance: the "SQLite vector acceleration (sqlite-vec)" section configures exactly this (`store.vector.enabled/extensionPath`).
- [Vector Database](../../term_dictionary/term_vector_database.md) — vector store/ANN; relevance: the storage backend for embedding vectors this note configures.
- [FTS5](../../term_dictionary/term_fts5.md) — SQLite full-text search; relevance: `store.fts.tokenizer` (unicode61/trigram) is a configured index-storage knob.
- [QMD](../../term_dictionary/term_qmd.md) — OpenClaw QMD local-first memory sidecar; relevance: the entire QMD backend config section (command/searchMode/rerank/scope/limits/update) configures QMD.
- [Memory Dreaming](../../term_dictionary/term_memory_dreaming.md) — background memory-consolidation sweep; relevance: the Dreaming section configures the scheduled light/deep/REM consolidation.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session/transcript storage; relevance: QMD `sessions.{enabled,retentionDays,exportDir}` + index storage persist transcripts.
- [Cron](../../term_dictionary/term_cron.md) — scheduled-job cadence syntax; relevance: dreaming `frequency: "0 3 * * *"` and QMD `update.interval` schedule the sweeps.
- [Embedding](../../term_dictionary/term_embedding.md) — dense vectors; relevance: index storage holds the embeddings; QMD vsearch/query modes require embedding readiness.

**Docs**
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory model; relevance: conceptual peer for the storage/index surface.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory; relevance: `includeDefaultMemory` auto-indexing `MEMORY.md` + `memory/**` parallels auto-memory.
- [cc_sdk_session_store_setup](../claude_code/cc_sdk_session_store_setup.md) — SDK session-store setup; relevance: direct analog to QMD session-transcript indexing + retention.
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — Hermes session storage; relevance: per-agent SQLite session/index storage layout peer.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — persistent memory store; relevance: durable memory-index storage analog.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — session search index storage; relevance: parallels session-memory index storage + delta-reindex thresholds.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes↔OpenClaw migration; relevance: documents OpenClaw memory backend/storage shape being migrated.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — Band agent memories API; relevance: alternate memory-storage API for cross-ecosystem comparison.
- [oc_reference_memory_config_search](oc_reference_memory_config_search.md) — (planned, this series) the search/embedding half; relevance: same source page; reciprocal split sibling.
- [oc_concepts_memory_qmd](oc_concepts_memory_qmd.md) — (planned, this series, co slice) QMD engine concept; relevance: conceptual overview of the QMD backend this note configures.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory engine; relevance: implements sqlite-vec store, index storage, QMD manager, and dreaming.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agent runtime; relevance: owns per-agent `openclaw-agent.sqlite` index storage and QMD lifecycle.

**Snippets**
- [snippet_openclaw_memory_host_backend_config](../../code_snippets/snippet_openclaw_memory_host_backend_config.md) — memory backend selection; relevance: implements `memory.backend = "qmd"` vs builtin.
- [snippet_openclaw_memory_host_qmd_process](../../code_snippets/snippet_openclaw_memory_host_qmd_process.md) — QMD process manager; relevance: implements QMD command/lifecycle, startup, and update interval.
- [snippet_openclaw_memory_host_qmd_scope](../../code_snippets/snippet_openclaw_memory_host_qmd_scope.md) — QMD result scope rules; relevance: implements the `qmd.scope` allow/deny rules section.
- [snippet_openclaw_memory_host_qmd_query_parser](../../code_snippets/snippet_openclaw_memory_host_qmd_query_parser.md) — QMD query/searchMode parsing; relevance: implements `searchMode` (search/vsearch/query) + `rerank`.
- [snippet_openclaw_memory_dreaming_constants](../../code_snippets/snippet_openclaw_memory_dreaming_constants.md) — dreaming constants/phases; relevance: implements the light/deep/REM dreaming phase policy.
- [snippet_openclaw_memory_dreaming_resolvers](../../code_snippets/snippet_openclaw_memory_dreaming_resolvers.md) — dreaming config resolvers; relevance: implements `dreaming.{enabled,frequency,model}` resolution + subagent trust gate.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor dreaming preview; relevance: surfaces dreaming config/state for operators.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — memory SQLite schema; relevance: defines the index-storage schema this note configures.
- [snippet_openclaw_memory_host_internal_walker](../../code_snippets/snippet_openclaw_memory_host_internal_walker.md) — memory path/file walker; relevance: implements `extraPaths`/`includeDefaultMemory` directory scan.

### oc_reference_prompt_caching (11t · 10s · 10d)

**Terms**
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — provider reuse of unchanged prompt prefixes; relevance: the entire note tunes `cacheRetention` + cache reuse.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — transformer key/value attention cache; relevance: prompt caching reuses the provider-side KV cache; the system-prompt fingerprint shares KV across turns.
- [Context Window](../../term_dictionary/term_context_window.md) — model token budget; relevance: caching the stable prefix preserves window budget; pruning bounds it.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript history compression; relevance: `contextPruning.mode: cache-ttl` prunes old tool-result context after TTL.
- [Context Compression](../../term_dictionary/term_context_compression.md) — shrinking carried context; relevance: cache-ttl pruning + image-block markering are context-compression guards.
- [Inference Profile](../../term_dictionary/term_inference_profile.md) — Bedrock routing/throughput profile; relevance: Bedrock cache pass-through depends on the model ref / inference routing.
- [Cross-Region Inference](../../term_dictionary/term_cross_region_inference.md) — Bedrock multi-region routing; relevance: Bedrock/Vertex routing interacts with cache shaping per host.
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock unified Converse API; relevance: Bedrock Anthropic refs expose cache pass-through via the Converse path.
- [Bedrock](../../term_dictionary/term_bedrock.md) — AWS Bedrock; relevance: the page documents per-provider Bedrock cache behavior (Anthropic pass-through, non-Anthropic forced to none).
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic keep-alive turn; relevance: heartbeat keep-warm reduces repeated cache writes after idle gaps.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: per-provider cache behavior (Anthropic/OpenAI/Vertex/Gemini/OpenRouter) is an LLM-API concern.

**Docs**
- [cc_prompt_caching_mechanism](../claude_code/cc_prompt_caching_mechanism.md) — Claude Code prompt-caching mechanism; relevance: direct conceptual analog to OpenClaw's prefix-caching mechanism.
- [cc_cache_lifetime_and_scope](../claude_code/cc_cache_lifetime_and_scope.md) — cache TTL/scope; relevance: parallels `cacheRetention` short/long TTL (5-min vs 1-hour) + `prompt_cache_key` scope.
- [cc_cache_invalidation_actions](../claude_code/cc_cache_invalidation_actions.md) — what busts the cache; relevance: parallels the system-prompt cache-boundary "what lands above/below" invalidation rules.
- [cc_cache_preserving_actions](../claude_code/cc_cache_preserving_actions.md) — what keeps cache warm; relevance: parallels heartbeat keep-warm + cache-stability guards (deterministic tool ordering).
- [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — per-feature token cost; relevance: the cost lever this page tunes (lower token cost via reuse).
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — token-reduction techniques; relevance: cacheRetention + cache-ttl pruning are the OpenClaw token-reduction levers.
- [cc_amazon_bedrock_features](../claude_code/cc_amazon_bedrock_features.md) — Bedrock feature support; relevance: parallels Bedrock cache pass-through / forced-none behavior.
- [bedrock_converse_api_overview](../aws_bedrock/bedrock_converse_api_overview.md) — Bedrock Converse API; relevance: the API surface Bedrock Anthropic cache pass-through rides on.
- [bedrock_cross_region_overview](../aws_bedrock/bedrock_cross_region_overview.md) — Bedrock cross-region inference; relevance: cache shaping interacts with cross-region/host routing.
- [pi_compaction](../pi/pi_compaction.md) — Pi context compaction; relevance: peer of `contextPruning.mode: cache-ttl` history pruning.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: `cacheRetention` merge order + system-prompt cache boundary + live-cache regression live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: usage normalization (cacheRead/cacheWrite), heartbeat, and cache-trace diagnostics run in the gateway.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: per-provider cache markers (Anthropic cache_control, OpenAI prompt_cache_key, Gemini cachedContents) are implemented per provider.

**Snippets**
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — system-prompt cache-section split; relevance: implements the stable-prefix / volatile-suffix cache boundary.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt assembly modes; relevance: ordering of tool defs/skills/workspace above HEARTBEAT.md for prefix stability.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — context injection ordering; relevance: where volatile per-turn metadata lands relative to the cache boundary.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: implements cache-ttl pruning's safe-boundary chunking.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/cache-status reporting; relevance: implements cacheRead/cacheWrite normalization + `/status` transcript fallback.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile/cache respawn; relevance: cache-warming/respawn behavior tied to heartbeat keep-warm.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat buffered delta; relevance: implements heartbeat keep-warm cadence.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — Hermes prompt-caching core; relevance: parallel per-provider cache-marker injection implementation.
- [snippet_hermes_agent_core_conversation_loop_usage_accounting](../../code_snippets/snippet_hermes_agent_core_conversation_loop_usage_accounting.md) — usage/token accounting; relevance: parallel cacheRead/cacheWrite accounting in the conversation loop.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider adapter; relevance: implements `prompt_cache_key` + `prompt_cache_retention: "24h"` + cached_tokens mapping.

### oc_reference_release_performance_sweep (10t · 10s · 10d)

**Terms**
- [CI/CD](../../term_dictionary/term_ci_cd.md) — CI/CD pipeline; relevance: the sweep is produced by the `OpenClaw Performance` CI workflow across release tags.
- [npm](../../term_dictionary/term_npm.md) — npm registry/package; relevance: the npm-package-size sweep (`npm pack --dry-run`) and dependency-count audit are the core evidence.
- [Docker](../../term_dictionary/term_docker.md) — containers; relevance: install-footprint installs and Docker release lanes are part of the measured surface.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — supply-chain substitution attack; relevance: the supply-chain interpretation frames dependency count as a security/trust metric (maintainers, tarballs, transitive updates).
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — scoped npm package namespaces; relevance: plugin-extraction (`@openclaw/codex`, `@napi-rs/canvas`) moves cones to scoped plugin packages.
- [SDLC](../../term_dictionary/term_sdlc.md) — software lifecycle; relevance: the sweep is the release-gate evidence stage of the lifecycle.
- [Latency](../../term_dictionary/term_latency.md) — response time; relevance: cold/warm agent-turn ms and `readyz`/CLI-health p50 are latency metrics.
- [Throughput](../../term_dictionary/term_throughput.md) — work rate / capacity; relevance: repeat-3 sampling and agent-turn rate framing are throughput-adjacent perf evidence.
- [Scalability](../../term_dictionary/term_scalability.md) — efficient growth under load; relevance: peak RSS + install footprint reductions are scalability/efficiency outcomes.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated env; relevance: install-footprint sweeps run `npm install` into temporary/throwaway sandboxes.

**Docs**
- [cc_github_actions](../claude_code/cc_github_actions.md) — GitHub Actions CI; relevance: the perf workflow is a GitHub Actions performance lane.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/metrics; relevance: the sweep is a telemetry/measurement methodology (snapshots, probes, medians).
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure-deployment principles; relevance: the supply-chain interpretation (fewer default packages = less to trust) is a secure-deployment argument.
- [cc_sdk_observability_opentelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — observability/OTel; relevance: source-probe `readyz`/CLI-health p50 + RSS are observability metrics.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — monitoring setup; relevance: the runtime metric collection peer for these probes.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install verification; relevance: install-footprint audit (`du -sk node_modules`, package-instance counts) is install verification.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — container runtime; relevance: the install/Docker footprint substrate measured.
- [pi_packages](../pi/pi_packages.md) — package model; relevance: tarball/unpacked/file-count package metrics are the package-distribution surface.
- [oc_reference_full_release_validation](oc_reference_full_release_validation.md) — (planned, this series) the release gate; relevance: the perf sweep is produced BY this release gate's workflows.
- [oc_gateway_shrinkwrap](oc_gateway_shrinkwrap.md) — (planned, this series, gw slice) npm shrinkwrap explainer; relevance: the page's "Shrinkwrap boundary" section links the shrinkwrap maintainer-check doc directly.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core monorepo; relevance: the package shape, shrinkwrap, and dependency boundaries measured here are this repo's.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: dependency-count-as-security-metric + audit checks are this module's concern.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions/plugins; relevance: the `2026.5.12` plugin-extraction milestone moved cones into extension packages.

**Snippets**
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security audit probe runner; relevance: the supply-chain audit lane backing the dependency-trust framing.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit composition; relevance: how the dependency/supply-chain audits aggregate.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: maintainer/tarball trust surface the supply-chain argument cites.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — CLI security advisories; relevance: transitive-update/advisory surface in the supply-chain interpretation.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: plugin packages owning their own dependency graph is the cleanup direction.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: plugin-extraction install behavior (cones install with plugins, not core).
- [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy dependency loading; relevance: keeping heavy/optional capabilities outside the default install path.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — gateway startup prewarm; relevance: cold-turn / startup-readiness timing the sweep measures.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway health; relevance: `readyz`/CLI-health p50 probes in the source-probe table.
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — CLI update; relevance: package install/update footprint across versions is the audited behavior.

### oc_reference_rich_output_protocol (8t · 10s · 10d)

**Terms**
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: plain Markdown image syntax stays text by default; channels opt into `![alt](url)` → media at the outbound adapter.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image+audio; relevance: the protocol carries structured `mediaUrl`/`mediaUrls` image/audio attachments.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events; relevance: block streaming carries media on structured payload fields over the streamed event channel (covers missing `term_streaming`).
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS audio synthesis; relevance: `[[audio_as_voice]]` is the audio-presentation hint for synthesized/voice delivery.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — voice interaction surface; relevance: `[[audio_as_voice]]` and voice replies route into voice-mode presentation.
- [A2UI](../../term_dictionary/term_a2ui.md) — agent-to-UI rich rendering protocol; relevance: `[embed ...]` + the stored `canvas` shape are OpenClaw's agent-to-Control-UI rich-render protocol.
- [PII](../../term_dictionary/term_pii.md) — personal data; relevance: remote media must be public https + pass file-read/media-type policy (a redaction/exposure surface).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the directives are emitted in the assistant (LLM) output payload.

**Docs**
- [cc_output_styles](../claude_code/cc_output_styles.md) — Claude Code output styling; relevance: closest analog — controlling assistant output presentation/rendering.
- [cc_fullscreen_rendering](../claude_code/cc_fullscreen_rendering.md) — fullscreen/rich rendering; relevance: parallel rich-render surface for assistant output.
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — SDK streaming output; relevance: the block-streaming media-on-structured-fields rule + dedup-on-final behavior.
- [pi_tui_components](../pi/pi_tui_components.md) — Pi TUI rendering components; relevance: peer rendering-surface for structured output blocks.
- [pi_tui_custom_components](../pi/pi_tui_custom_components.md) — custom TUI components; relevance: the `canvas` stored block is a custom render component analog.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — messaging media settings; relevance: directly parallels outbound media-attachment delivery + per-channel media opt-in (Telegram).
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — image generation/delivery; relevance: produces the media delivered via `mediaUrl`/`mediaUrls`.
- [hermes_deliverable_mode](../hermes_agent/hermes_deliverable_mode.md) — structured deliverable output; relevance: structured rich-output deliverables peer to the canvas/embed shape.
- [oc_reference_rpc_adapters](oc_reference_rpc_adapters.md) — (planned, this series) RPC adapters; relevance: the page's own `## Related` links RPC adapters as a sibling reference.
- [oc_web_control_ui](oc_web_control_ui.md) — (planned, this series, wb slice) Control UI reference; relevance: `[embed ...]` is the web-only Control-UI rich render path this note describes.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: media pipeline, image lifecycle, and outbound rendering run in the gateway.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: per-channel outbound adapters decide Markdown-image→media opt-in.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel adapters; relevance: Telegram-style media-reply mapping lives here.

**Snippets**
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript media pipeline; relevance: implements structured-media delivery + streamed-vs-final dedup.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed image lifecycle; relevance: implements managed media-record handling for delivered attachments.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: implements media-type checks + size guards on attachments.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: enforces public-https / file-read policy on media directives.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — SSE session streaming; relevance: the streamed-block path media rides on.
- [snippet_openclaw_agents_btw_streamSimple_sanitize](../../code_snippets/snippet_openclaw_agents_btw_streamSimple_sanitize.md) — streaming output sanitize; relevance: normalizes streamed assistant output / strips duplicate media.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript event/stored shape; relevance: the normalized/stored `canvas` assistant content block.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound message runner; relevance: parallel outbound-delivery path for structured media + reply metadata.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — send-attachment tool; relevance: the structured `mediaUrl` payload from a message tool (valid message-tool payload example).
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media outbound; relevance: the exact channel that opts Markdown-image into a media reply.

### oc_reference_rpc_adapters (8t · 10s · 10d)

**Terms**
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON remote-procedure-call protocol; relevance: both adapter patterns integrate external CLIs over JSON-RPC.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events; relevance: Pattern A's signal-cli event stream is SSE (`/api/v1/events`).
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex socket transport; relevance: contrast transport for bidirectional RPC vs the HTTP-daemon / stdio patterns documented.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: the note's core subject — RPC adapter patterns.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting/forwarding proxy; relevance: the gateway fronting/owning the signal-cli HTTP daemon lifecycle is a reverse-proxy-adjacent pattern.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — API entry/routing layer; relevance: OpenClaw's gateway owns the adapter process lifecycle and routes RPC calls.
- [Function Calling](../../term_dictionary/term_function_calling.md) — structured tool/method invocation; relevance: the core methods (`watch.subscribe`, `send`, `chats.list`) are structured method calls.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated child process; relevance: Pattern B spawns `imsg rpc` as an isolated stdio child process.

**Docs**
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — Pi RPC protocol; relevance: direct analog to OpenClaw's JSON-RPC adapter protocol.
- [pi_rpc_commands](../pi/pi_rpc_commands.md) — Pi RPC commands; relevance: parallels the core methods (`send`, `watch.subscribe`, `chats.list`).
- [pi_rpc_events](../pi/pi_rpc_events.md) — Pi RPC events; relevance: parallels Pattern A's SSE event stream / Pattern B's `method: "message"` notifications.
- [band_websocket_agent_channels](../band/band_websocket_agent_channels.md) — Band WS agent channels; relevance: alternate socket-RPC channel transport for cross-ecosystem comparison.
- [band_websocket_agent_events](../band/band_websocket_agent_events.md) — Band WS agent events; relevance: parallels the RPC event/notification stream.
- [band_acp_overview](../band/band_acp_overview.md) — Band ACP overview; relevance: ACP is the agent-side RPC peer protocol comparison.
- [band_rest_api_introduction](../band/band_rest_api_introduction.md) — Band REST API; relevance: HTTP-transport contrast to the HTTP-daemon RPC pattern.
- [hermes_programmatic_integration](../hermes_agent/hermes_programmatic_integration.md) — Hermes programmatic/RPC integration; relevance: parallel external-integration RPC surface.
- [oc_reference_rich_output_protocol](oc_reference_rich_output_protocol.md) — (planned, this series) rich output protocol; relevance: reciprocal `## Related` link from the rich-output page.
- [oc_gateway_protocol](oc_gateway_protocol.md) — (planned, this series, gw slice) gateway protocol reference; relevance: the page's own `## Related` links Gateway protocol directly.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: the gateway owns adapter process start/stop tied to provider lifecycle.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: signal-cli and imsg integrations are channel adapters.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channels; relevance: phone/voice channels use similar external-CLI RPC daemons.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — Hermes messaging gateway; relevance: parallel messaging-gateway RPC/transport implementation.

**Snippets**
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC protocol envelope; relevance: the JSON-RPC request/response envelope both patterns use.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — RPC error codes/version; relevance: resilient-client error/version handling per the adapter guidelines.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the method/schema grouping behind `watch.*`/`send`/`chats.list`.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — TUI server JSON-RPC; relevance: parallel JSON-RPC server implementation (line-delimited stdio analog).
- [snippet_hermes_agent_tui_transport](../../code_snippets/snippet_hermes_agent_tui_transport.md) — TUI RPC transport; relevance: stdio/socket transport layer comparable to Pattern B.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway channel websocket; relevance: socket-transport RPC channel adapter peer.
- [snippet_hermes_agent_cli_web_websocket](../../code_snippets/snippet_hermes_agent_cli_web_websocket.md) — CLI web websocket; relevance: WS transport contrast to HTTP-daemon/stdio RPC.
- [snippet_hermes_agent_gw_platform_signal_sse](../../code_snippets/snippet_hermes_agent_gw_platform_signal_sse.md) — signal SSE event stream; relevance: implements Pattern A's signal-cli SSE event consumption.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: an agent-side RPC server implementation for comparison.

### oc_reference_secret_placeholder_conventions (10t · 10s · 10d)

**Terms**
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage/resolution; relevance: the conventions govern how secrets/keys appear (or don't) in docs and `${ENV}` wiring.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer access token; relevance: realistic-looking bearer tokens are exactly the "avoid" pattern.
- [PII](../../term_dictionary/term_pii.md) — sensitive personal/credential data; relevance: avoiding real-looking secrets is a sensitive-data-exposure hygiene rule.
- [Markdown](../../term_dictionary/term_markdown.md) — doc markup; relevance: the conventions apply to Markdown docs/examples and code fences.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: examples are scoped to provider/channel/auth type credentials.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — API auth/key surface; relevance: provider API keys (`OPENAI_API_KEY`) are the credentials being placeheld.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: the placeholder examples target provider keys (openai/discord/etc.).
- [PKCE](../../term_dictionary/term_pkce.md) — OAuth proof-key flow; relevance: OAuth credential examples should follow placeholder hygiene, not paste real flow secrets.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — AWS default credential resolution; relevance: AWS keys (`AKIA…`) are a named "avoid" prefix; chain-based auth avoids inline keys entirely.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/risk framing; relevance: secret-scanner-safe docs mitigate credential-leak-via-docs in the threat model.

**Docs**
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure-deployment principles; relevance: closest analog — handling secrets/keys safely in code and config.
- [cc_authentication](../claude_code/cc_authentication.md) — auth/credential setup; relevance: the env-var credential wiring the placeholders model.
- [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential/filesystem controls; relevance: governs how credentials are referenced vs inlined.
- [cc_plugin_user_config_and_env](../claude_code/cc_plugin_user_config_and_env.md) — plugin user config + env; relevance: `${OPENAI_API_KEY}` env-wiring style is this config surface.
- [hermes_secrets_bitwarden](../hermes_agent/hermes_secrets_bitwarden.md) — Hermes secret-store integration; relevance: secret-reference-not-inline pattern peer.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pools; relevance: referencing pooled credentials instead of literal tokens in docs/config.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars; relevance: the provider env-var names (`OPENAI_API_KEY`, …) the placeholders stand in for.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: the security framing for not leaking real credentials in examples.
- [oc_reference_memory_config_search](oc_reference_memory_config_search.md) — (planned, this series) memory API-key resolution; relevance: its API-key-resolution `${ENV}` snippets follow these placeholder conventions.
- [oc_gateway_secrets](oc_gateway_secrets.md) — (planned, this series, gw slice) gateway secrets reference; relevance: the runtime secret-handling counterpart these doc-hygiene rules protect.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: secret-scanner tooling + external-content safety live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: runtime credential/secret resolution the placeholders abstract.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — gateway credential/secret resolution; relevance: the runtime secret-resolution the `${ENV}` placeholders feed.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content safety; relevance: scanner/safety handling of doc + external content.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret-redaction patterns; relevance: the regex/patterns that detect token-like strings (`sk-…`, `xoxb-…`, `AKIA…`).
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: env-var-vs-config credential sourcing the conventions recommend.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: how external-CLI credentials are referenced, not inlined.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — Bedrock adapter credentials; relevance: AWS credential-chain usage that avoids inline keys (the `AKIA…` avoid case).
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — credential-pool seeding; relevance: seeding pooled credentials from env, not literals.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: provider key resolution the placeholders represent.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE OAuth flow; relevance: OAuth-secret handling that must not paste real tokens.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth authorize dispatch; relevance: the token/auth dispatch path that consumes resolved (non-placeholder) credentials.

> **DB-verify ledger (xref-augment 2026-06-21):** every EXISTING `note_id` cited above was verified with
> live under `claude_code/`, `pi/`, `hermes_agent/`, `band/`, `aws_bedrock/`; all snippets under
> `resources/code_snippets/`; all repos under `areas/code_repos/`. **Sibling `oc_*` docs (planned, this
> series)** cited toward the 10-doc floor — NOT yet in the DB, never counted toward the ≥5-existing sub-floor:
> `oc_reference_*` (this rf02 slice) + cross-slice `oc_gateway_doctor`, `oc_gateway_shrinkwrap`,
> `oc_gateway_protocol`, `oc_gateway_secrets`, `oc_web_control_ui`, `oc_concepts_memory_search`,
> `oc_concepts_memory_qmd` (other slices). **MISSING terms (do NOT cite; fallback used in-line):**
> `term_semantic_search` (→ `term_rag`), `term_attachment` (→ `term_multimodal`), `term_streaming` (→
> `term_sse`), `term_regular_expression` (→ `term_markdown`). **`entry_openclaw_docs` MISSING — created by
> master pre-step W1** before this sub-plan executes (G8 inbound source for all 8 notes).

## Undigested Terms Plan

| Term | Disposition |
|------|-------------|
| Full Release Validation, release profile (smoke/stable/full), focused rerun, Docker release-path chunk | OpenClaw release-engineering vocabulary → digested in note 1 (`oc_reference_full_release_validation`); not new term_dictionary entries. Link `term_ci_cd`, `term_docker`. |
| memory search, embedding provider, hybrid search, MMR, temporal decay, multimodal memory, embedding cache, batch indexing | OpenClaw memory-config vocabulary → digested in notes 2/3; link existing `term_embedding`, `term_vector_database`, `term_rag`, `term_multimodal`. |
| QMD backend, sqlite-vec, index storage, Dreaming | OpenClaw memory-backend vocabulary → digested in note 3; no new terms (link `term_vector_database`). |
| `cacheRetention`, `contextPruning.mode: cache-ttl`, heartbeat keep-warm, cache-stability guard, system-prompt cache boundary | OpenClaw prompt-caching config vocabulary → digested in note 4; link existing `term_prompt_caching`, `term_kv_cache`, `term_heartbeat`. |
| install footprint, npm package size, shrinkwrap boundary, supply-chain interpretation | OpenClaw release-evidence vocabulary → digested in note 5; link existing `term_npm`, `term_ci_cd`. |
| `[embed ...]`, `mediaUrl`/`mediaUrls`, `[[audio_as_voice]]`, stored rendering shape | OpenClaw output-protocol vocabulary → digested in note 6 (model); link existing `term_markdown`, `term_multimodal`. |
| RPC adapter Pattern A/B, stdio child process, HTTP daemon adapter | OpenClaw RPC-pattern vocabulary → digested in note 7 (model); link existing `term_json_rpc`, `term_websocket`. |
| secret placeholder conventions | OpenClaw docs-hygiene vocabulary → digested in note 8 (argument); link existing `term_secrets_manager`, `term_oauth_token`. |
| **New term_dictionary captures** | **0 expected.** No genuinely cross-cutting, vault-reusable term lacks an existing note AND a doc-page home. Augment Step 2d re-scans; if a true new term surfaces, capture via `/tessellum-capture-term-note` + add to its `acronym_glossary_*.md` (candidate glossary: `acronym_glossary_*` for agentic/LLM dev tooling). |

## Term-Note Authoring Requirements

**N/A (0 new terms).** rf02 authors zero `term_dictionary` notes; all OpenClaw vocabulary is digested as `oc_`
documentation concept/procedure notes, and existing terms are linked, not redefined (inherited from master).
If augment Step 2d surfaces a genuine new term, the master's Term-Note Authoring Requirements apply

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must pass before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format + YAML | `/tessellum-check-note-format` + `scripts/check_note_format.py` + `scripts/check_yaml_frontmatter.py` (fixed field order; `building_block` ∈ {concept, procedure, model, argument}; forbidden fields absent) |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/reference/<page>.md`; no invented config/numbers; word ratio within ±30% of plan |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one BB per note; every mapped H2/H3 present |
| G4 | Cross-Reference | ≥6 relevance-selected term links + repos/siblings/other-vault per note, each with a relevance statement |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references`; no link to a non-existent note (MISSING list above excluded) |
| G6 | Broken-link fix | `/tessellum-fix-broken-links`; 0 broken links after incremental reindex |
| G7 | Discoverability | Each new note carries outbound links; appears in `entry_openclaw_docs.md` |
| G8 | In-degree ≥1 (anti-island) | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks below) |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_reference_full_release_validation oc_reference_memory_config_search oc_reference_memory_config_storage oc_reference_prompt_caching oc_reference_release_performance_sweep oc_reference_rich_output_protocol oc_reference_rpc_adapters oc_reference_secret_placeholder_conventions"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format (flag errors / non-indexed-link LINK-003)
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density (exclude YAML frontmatter from word count)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w/${cb}cb/${lines}L)"
  # G4/G8 sibling-prefix presence sanity (≥1 oc_ or repo_openclaw link expected)
  grep -qE "\($SIBLING_PREFIX|repo_openclaw" "$f" || echo "NO SIBLING/REPO LINK: $n"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6cb / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_reference_full_release_validation | procedure | 650 | 1 | ✅ |
| 2 | oc_reference_memory_config_search | procedure | 750 | 4 | ✅ |
| 3 | oc_reference_memory_config_storage | procedure | 600 | 4 | ✅ |
| 4 | oc_reference_prompt_caching | procedure | 750 | 6 | ✅ (16 raw fences pruned to ≤6: canonical knob + 2-3 provider examples, rest in prose) |
| 5 | oc_reference_release_performance_sweep | argument | 650 | 0 | ✅ (source has 0 fences; tables/prose only) |
| 6 | oc_reference_rich_output_protocol | model | 400 | 3 | ✅ |
| 7 | oc_reference_rpc_adapters | model | 350 | 0 | ✅ |
| 8 | oc_reference_secret_placeholder_conventions | argument | 300 | 2 | ✅ |

No note approaches the caps. The only split is memory-config (3,524w → notes 2+3); prompt-caching is the only
single note needing fence pruning (16 raw → ≤6).

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as master pre-step W1, >30-note series) under a
**"Reference"** section / rf02 sub-cluster (validation + config + protocols). Each note receives its
entry-point back-link at finalization (G7/G8). No new entry point is created by this sub-plan; the master's

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + apply at execution; each new note must RECEIVE
≥1):

- `entry_openclaw_docs.md` → all 8 notes (primary anti-island source; created by master pre-step).
- `repo_openclaw_memory.md` → notes 2, 3 (the code-side counterpart of the memory-config reference).
- `repo_openclaw_security.md` → notes 1, 5, 8 (release-gate security audits, supply-chain, secret hygiene).
- `repo_openclaw_gateway.md` → notes 4, 6, 7 (caching/output/RPC live in the gateway runtime).
- `term_prompt_caching.md` → note 4; `term_kv_cache.md` → note 4.
- `term_embedding.md` → note 2; `term_vector_database.md` → notes 2, 3.
- `term_json_rpc.md` → note 7; `term_secrets_manager.md` → note 8; `term_ci_cd.md` → notes 1, 5.
- Reciprocal sibling inlinks within rf02: note 1 ↔ note 5 (release gate ↔ perf evidence); note 2 ↔ note 3
  (memory search ↔ storage); note 8 → note 2 (placeholder conventions referenced by API-key resolution).

## Pacing Rules (inherited from master)

One execution phase; 8 GATEs before commit. Re-read each source page; reproduce config snippets verbatim;
one BB per note; fan-out ≤30 agents/run; `git pull --rebase --autostash` first; no Claude co-author trailer;
incremental reindex per wave; verify `note_links` + 0 broken links + in-degree ≥1 before commit/push.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the PLAN-stage `## Candidate Cross-References` candidate pools with a
**raised floors: ≥8 terms · ≥10 snippets · ≥10 docs per note**. All 7 source pages were re-read in full from
(and a few cross-slice `oc_*`) are cited toward the 10-doc floor as "(planned, this series)"; **each note has

**Per-note counts (all floors met).**

| Note | Terms | Snippets | Docs (≥5 existing) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_reference_full_release_validation | 8 | 10 | 10 (9 existing + 1 planned) | 2 | ✅ |
| oc_reference_memory_config_search | 10 | 10 | 10 (9 existing + 1 planned) | 3 | ✅ |
| oc_reference_memory_config_storage | 8 | 10 | 10 (9 existing + 1 planned) | 3 | ✅ |
| oc_reference_prompt_caching | 11 | 10 | 10 (10 existing + 0 planned) | 4 | ✅ |
| oc_reference_release_performance_sweep | 10 | 10 | 10 (9 existing + 1 planned) | 3 | ✅ |
| oc_reference_rich_output_protocol | 8 | 10 | 10 (9 existing + 1 planned) | 3 | ✅ |
| oc_reference_rpc_adapters | 8 | 10 | 10 (9 existing + 1 planned) | 4 | ✅ |
| oc_reference_secret_placeholder_conventions | 10 | 10 | 10 (9 existing + 1 planned) | 2 | ✅ |

**Upgrades over the PLAN-stage candidates.** The original pools cited ≥6 terms / 0–8 snippets / ≤4 docs per
plan missed: terms `term_mmr`, `term_hybrid_search`, `term_fts5`, `term_sqlite_vec`, `term_bm25`, `term_qmd`,
`term_memory_dreaming`, `term_caching`, `term_context_compression`, `term_text_to_speech`, `term_voice_mode`,
`term_a2ui`, `term_rpc`, `term_dependency_confusion`, `term_npm_scoping`, `term_sdlc`, `term_devops`,
`term_latency`, `term_throughput`, `term_scalability`, `term_aws_sdk_credential_chain`, `term_pkce`,
`term_threat_model`; the full `snippet_openclaw_gateway_rpc_protocol_*`, security-audit, credential, media, and
QMD/dreaming snippet corpora; and docs `hermes_memory_provider_catalog`, `hermes_session_search_storage`,
`band_websocket_agent_*`, `band_acp_overview`, `hermes_messaging_media_settings`, `cc_authentication`,
`hermes_credential_pools`. Every fallback for a MISSING term was applied in-line (semantic_search→rag,
attachment→multimodal, streaming→sse, regular_expression→markdown).

**New-term candidates: 0 (confirmed, no change from plan Step 4e).** The augment re-read (Step 2d) surfaced no
genuinely cross-cutting, vault-reusable term that lacks BOTH an existing note AND a doc-page home. All OpenClaw
reference vocabulary (Full Release Validation, release profile, QMD backend, sqlite-vec, Dreaming,
`cacheRetention`, cache-ttl pruning, system-prompt cache boundary, `[embed ...]`, `[[audio_as_voice]]`, RPC
Pattern A/B, secret placeholder conventions, shrinkwrap boundary, install footprint) is digested as `oc_*`
documentation concept/procedure notes and links existing `term_dictionary` entries — never inlined as a new
term. If a true new term surfaces during execution, the master's Term-Note Authoring Requirements apply
(`/tessellum-capture-term-note` + glossary update; best-fit glossary candidate: the agentic/LLM-dev-tooling
`acronym_glossary_*`). No collision/specificity renames were needed (0 new `term_*` slugs authored).

**Issues / notes for execution.** (1) `entry_openclaw_docs` is still MISSING — it is the G7/G8 inbound source
for all 8 notes and MUST be created by master pre-step W1 before this sub-plan executes. (2) The 4 MISSING
terms above remain capture candidates for future slices but are NOT authored here. (3) Sibling/cross-slice
`oc_*` docs cited "(planned, this series)" will resolve as their owning sub-plans execute; until then they are
forward references (expected, not ghosts) and must be excluded from the G5 ghost gate's EXISTING-note check.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping` present; every note ≥8 terms · ≥10 snippets · ≥10 docs, each link carries a `relevance:` statement; counts table above. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost detect+redirect, G6 broken-link fix, G7 discoverability, G8 in-degree ≥1. |
| CP4 | Size | **PASS** | 8 planned notes ≤ 30; single execution phase; no split required for the sub-plan itself. |
| CP5 | Format derived | **PASS** | YAML/body format inherited verbatim from master Format Definition (derived from existing `claude_code/`+`pi/` doc corpora: `## Overview` opener, `## Related Notes`, fixed YAML field order, forbidden-field list); G1 enforces via `check_yaml_frontmatter.py`. |
| CP6 | Density | **PASS** | `## Density Re-Assessment` — every note ≤750w / ≤6cb / ≤400L; memory-config split (3,524w → notes 2+3) and prompt-caching fence pruning (16 raw → ≤6) already locked; no borderline note unaddressed. |
| CP7 | Sources measured | **PASS** | All 7 pages re-read from `inbox/openclaw_docs/reference/` at augment; measured byte sizes (full-release-validation 22.7KB, memory-config 33.3KB, prompt-caching 16.5KB, release-performance-sweep 17.8KB, rich-output 3.2KB, rpc 1.3KB, secret-placeholder 1.1KB) consistent with the plan's word table; rpc 176w / secret 137w confirmed thin → single notes. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` (all OpenClaw vocab → `oc_*` notes, link existing terms, 0 new captures) + `## Term-Note Authoring Requirements` (N/A — 0 new terms; master's reqs apply if one surfaces) present; augment Step 2d re-scan confirmed 0 new-term candidates. |
| CP8f | Slug/collision audit | **PASS** | 0 new `term_*` slugs authored → no specificity/collision renames; generalized dedup ran across `term_dictionary/` + `documentation/` (no planned `oc_*` note duplicates an existing term/doc; the memory-config reference deliberately LINKS, not recreates, `repo_openclaw_memory`). |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks (existing notes → new notes)` maps ≥1 outside-folder inbound link per note (entry_openclaw_docs → all 8; repo/term inlinks; reciprocal rf02 sibling inlinks); G8 in-degree ≥1 is a gated execution phase, not a recommendation. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`. Caveat carried to execution:
master pre-step W1 (`entry_openclaw_docs.md`) MUST exist before this sub-plan runs (G7/G8 inbound source);
"(planned, this series)" sibling `oc_*` doc citations are forward references excluded from the G5 EXISTING-note
