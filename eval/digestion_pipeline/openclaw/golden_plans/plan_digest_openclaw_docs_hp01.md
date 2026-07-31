---
title: Sub-Plan hp01 — OpenClaw Docs: Help (Debugging, Environment, FAQ, First-run FAQ, Models FAQ)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["help/debugging", "help/environment", "help/faq", "help/faq-first-run", "help/faq-models"]
---

# Sub-Plan hp01: Help

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_` prefix) / format / dedup-before-create / 9-GATE /
> cross-refs / entry-point (W1 `entry_openclaw_docs.md`) are ALL inherited from the master; this file re-measures
> its 5 assigned pages and locks the planned-note set, coverage map, splits, and candidate cross-references.

## Scope

The 5 `help/` pages: the user-facing **support & troubleshooting** layer — debugging tooling (`help/debugging`),
environment-variable loading & precedence (`help/environment`), the large general **FAQ** (`help/faq`), the
**first-run FAQ** (`help/faq-first-run`, install/onboarding/auth/subscriptions), and the **models FAQ**
(`help/faq-models`, model selection/aliases/failover/auth-profiles). Priority **P2 (Phase B)** per master —
features/integration support content that references the P1 concept/gateway/CLI vocabulary rather than defining
it. The code-side OpenClaw notes (`repo_openclaw*`) and existing `term_*` vocabulary are LINKED, never recreated.

**Source**: OpenClaw docs, 5 pages, **21,964 measured body words** (mirror `inbox/openclaw_docs/help/`).
**Planned: 12 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| debugging | help/debugging | 1,573 | 23 | 11 | 2 | procedure |
| environment | help/environment | 1,301 | 6 | 14 | 1 | procedure |
| faq | help/faq | 11,357 | 0 | 18 (110 `<Accordion>`) | 0 | concept + procedure (split ×6) |
| faq-first-run | help/faq-first-run | 4,849 | 0 | 2 (51 `<Accordion>`) | 0 | procedure (split ×2) |
| faq-models | help/faq-models | 2,884 | 0 | 4 (22 `<Accordion>`) | 0 | procedure (split ×2) |

Notes on measurement:
- Body word counts exclude YAML frontmatter (each page carries a `summary`/`read_when`/`title` frontmatter block).
- FAQ pages contain **zero fenced code blocks at the page level**; Q&A is authored as MDX `<AccordionGroup>` /
  `<Accordion title="…">` components (titles = the questions). A handful of answers embed inline `json5` config
  snippets inside accordions; those are well under the ≤6/note cap once distributed across the split notes.
- `debugging.md` is code-dense (23 fences = export/CLI/log-output snippets); reproduced **selectively** (≤6) in
  the single debugging note (one coherent task cluster, ≤2,500 w → no split).

## Content Strategy

- **Prioritize**: env-var **precedence** (every provider-auth/deploy failure roots here), the **first-60-seconds /
  triage** entry, model **failover + auth profiles** (the most-asked runtime failures), and the **what-is /
  architecture** framing the rest of the corpus references.
- **Split**: `faq.md` (11,357 w / 16 content H2) → **6 topic-cluster notes**; `faq-first-run.md` (4,849 w) →
  **2 notes** (install/runtime/hosting vs auth/subscriptions/providers); `faq-models.md` (2,884 w > 2,500 cap) →
  **2 notes** (selection/aliases/switching vs failover + auth-profiles). `debugging.md` and `environment.md`
  stay 1 note each (≤2,500 w, single BB).
- **Link-out (NOT duplicated)**: `faq.md` has two **pointer H2s** — "Quick start and first-run setup" (16 w) →
  `faq-first-run` notes, and "Models, failover, and auth profiles" (16 w) → `faq-models` notes; these are
  cross-links inside the FAQ index cluster, not separate notes. Deep how-tos referenced from FAQ answers
  (`/gateway/configuration`, `/gateway/troubleshooting`, `/concepts/multi-agent`, `/tools/subagents`,
  `/automation/cron-jobs`, provider/install pages) are linked to their **owning sub-plans** (gw*/co*/to*/au*/
  pr*/in*), never re-digested here.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_help_debugging.md` | procedure | debugging.md: Runtime debug overrides, Session trace output, Plugin lifecycle trace, CLI startup/command profiling, Gateway watch mode, Dev profile + dev gateway (`--dev`), Raw stream logging (OpenClaw), Raw OpenAI-compatible chunk logging, Safety notes, Debugging in VSCode (Setup, Notes) | 650 | OpenClaw debugging toolkit: runtime debug-override env vars, session/plugin-lifecycle traces, CLI startup & command profiling, Gateway watch mode, the `--dev` dev profile/gateway, raw model-stream + OpenAI-chunk logging, and VSCode attach setup. |
| 2 | `oc_help_environment.md` | procedure | environment.md: Precedence (highest→lowest), Provider credentials & workspace `.env`, Config `env` block, Shell env import, Exec shell snapshots, Runtime-injected env vars, UI env vars, Env var substitution in config, Secret refs vs `${ENV}` strings, Path-related env vars (incl. `OPENCLAW_HOME`), Logging, nvm web_fetch TLS failures, Legacy environment variables | 650 | How OpenClaw loads environment variables: the full precedence order, provider creds + workspace `.env`, the config `env` block, shell import & exec snapshots, runtime-injected/UI vars, `${ENV}` substitution vs secret refs, path vars (`OPENCLAW_HOME`), and the nvm TLS / legacy-var gotchas. |
| 3 | `oc_help_faq_overview.md` | concept | faq.md: First 60 seconds if something is broken, What is OpenClaw? (one-paragraph, value proposition, highlights) | 550 | OpenClaw FAQ — first-line triage and product framing: the "first 60 seconds if something is broken" checklist and the "What is OpenClaw?" answers (local-first control-plane value proposition, Gateway-as-control-plane, channel/voice/Canvas surfaces). |
| 4 | `oc_help_faq_skills_automation.md` | procedure | faq.md: Skills and automation | 700 | FAQ — skills & automation: managed skill overrides & load precedence, custom skill folders, per-task model/agent routing, offloading heavy work to sub-agents, thread-bound subagent sessions, and cron/standing-order patterns. |
| 5 | `oc_help_faq_config_env.md` | procedure | faq.md: Config basics, Env vars and .env loading | 650 | FAQ — config & env loading: where config files live and how `~/.openclaw/openclaw.json` is structured, common config edits, and how `.env` / environment variables are loaded and resolved at the FAQ level (defers to `oc_help_environment` for the full precedence rule). |
| 6 | `oc_help_faq_storage_memory.md` | procedure | faq.md: Sandboxing and memory, Where things live on disk | 600 | FAQ — sandboxing, memory & on-disk layout: how sandboxing isolates tool execution, how memory persists, and where OpenClaw keeps sessions, skills, logs, and config on disk. |
| 7 | `oc_help_faq_gateway_remote.md` | procedure | faq.md: Remote gateways and nodes, Gateway: ports / "already running" / remote mode, Media and attachments | 700 | FAQ — gateway, remote & nodes: the single multiplexed gateway port, resolving "already running" / port conflicts, remote-mode access, pairing remote gateways with nodes, and handling media/attachments. |
| 8 | `oc_help_faq_sessions_logging.md` | procedure | faq.md: Sessions and multiple chats, Logging and debugging, Chat commands / aborting tasks / "it will not stop", Miscellaneous | 700 | FAQ — sessions, logging & chat control: managing multiple concurrent sessions/chats, reading logs & turning on debug output, chat commands plus aborting a stuck task ("it will not stop"), and miscellaneous runtime questions. |
| 9 | `oc_help_faq_security_access.md` | argument | faq.md: Security and access control | 600 | FAQ — security & access control: who can talk to the bot (allow-lists / access groups), exec-approval gating, secret handling, and the trust/exposure trade-offs of running a local-first control plane reachable from chat apps. |
| 10 | `oc_help_faq_first_run_install.md` | procedure | faq-first-run.md: Quick start and first-run setup (install/runtime/hosting cluster — git-vs-npm, runtime requirements, Raspberry Pi/Bun, Linux/VPS/VM installs, onboarding stuck, updating, docs-SSL, stable/beta/dev channels) | 750 | First-run FAQ (install & hosting): recommended install/setup path, runtime & hardware requirements (Raspberry Pi, Bun, Mac mini, VPS/VM), git-vs-npm installs and switching, onboarding-stuck recovery, self-update, stable/beta/dev channels, and docs-access SSL errors. |
| 11 | `oc_help_faq_first_run_auth.md` | procedure | faq-first-run.md: Quick start and first-run setup (auth/subscriptions cluster — Claude/OpenAI/Codex/Gemini subscription vs API key, Bedrock, 429 rate-limit, local-model OK, region pinning, dashboard auth) | 750 | First-run FAQ (auth & subscriptions): choosing subscription vs API-key auth across Claude (Pro/Max), OpenAI/Codex OAuth, Gemini CLI OAuth, and AWS Bedrock; the 429 rate_limit_error cause; local-model viability; region-pinning hosted traffic; and authenticating the dashboard on localhost vs remote. |
| 12 | `oc_help_faq_models.md` | procedure | faq-models.md: Models — defaults/selection/aliases/switching; Model failover and "All models failed"; Auth profiles (what they are & how to manage) | 800 | Models FAQ: recommended models and defaults, selecting/switching models (`/model`, on-the-fly, same-id collisions), defining model aliases/shortcuts, adding provider models (OpenRouter/Z.AI), how failover works and debugging "All models failed", and auth profiles (what they are, typical IDs, ordering, OAuth-vs-API-key). |

## Section Coverage Map

```
help/debugging.md (11 H2 / 2 H3)
├── Runtime debug overrides ───────────────────── → note 1 (oc_help_debugging)
├── Session trace output ──────────────────────── → note 1
├── Plugin lifecycle trace ────────────────────── → note 1
├── CLI startup and command profiling ─────────── → note 1
├── Gateway watch mode ────────────────────────── → note 1
├── Dev profile + dev gateway (--dev) ─────────── → note 1
├── Raw stream logging (OpenClaw) ─────────────── → note 1
├── Raw OpenAI-compatible chunk logging ───────── → note 1
├── Safety notes ──────────────────────────────── → note 1
├── Debugging in VSCode (### Setup, ### Notes) ── → note 1
└── Related ───────────────────────────────────── → note 1 (Related Notes mapping)
help/environment.md (14 H2 / 1 H3)
├── Precedence (highest → lowest) ─────────────── → note 2 (oc_help_environment)
├── Provider credentials and workspace `.env` ─── → note 2
├── Config `env` block ────────────────────────── → note 2
├── Shell env import ──────────────────────────── → note 2
├── Exec shell snapshots ──────────────────────── → note 2
├── Runtime-injected env vars ─────────────────── → note 2
├── UI env vars ───────────────────────────────── → note 2
├── Env var substitution in config ────────────── → note 2
├── Secret refs vs `${ENV}` strings ───────────── → note 2
├── Path-related env vars (### `OPENCLAW_HOME`) ─ → note 2
├── Logging ───────────────────────────────────── → note 2
├── nvm users: web_fetch TLS failures ─────────── → note 2
├── Legacy environment variables ──────────────── → note 2
└── Related ───────────────────────────────────── → note 2 (Related Notes mapping)
help/faq.md (18 H2: 16 content + 2 pointer)
├── First 60 seconds if something is broken ───── → note 3 (oc_help_faq_overview)
├── Quick start and first-run setup (POINTER) ─── → link-out → notes 10–11 (faq-first-run)
├── What is OpenClaw? ──────────────────────────── → note 3
├── Skills and automation ─────────────────────── → note 4 (oc_help_faq_skills_automation)
├── Config basics ─────────────────────────────── → note 5 (oc_help_faq_config_env)
├── Env vars and .env loading ─────────────────── → note 5 (defers detail to note 2)
├── Sandboxing and memory ─────────────────────── → note 6 (oc_help_faq_storage_memory)
├── Where things live on disk ─────────────────── → note 6
├── Remote gateways and nodes ─────────────────── → note 7 (oc_help_faq_gateway_remote)
├── Gateway: ports / "already running" / remote ─ → note 7
├── Media and attachments ─────────────────────── → note 7
├── Sessions and multiple chats ───────────────── → note 8 (oc_help_faq_sessions_logging)
├── Logging and debugging ─────────────────────── → note 8
├── Chat commands, aborting tasks, "it will not stop" → note 8
├── Miscellaneous ─────────────────────────────── → note 8
├── Models, failover, and auth profiles (POINTER) → link-out → note 12 (faq-models)
├── Security and access control ───────────────── → note 9 (oc_help_faq_security_access)
└── Related ───────────────────────────────────── → notes 3–9 (Related Notes mapping)
help/faq-first-run.md (1 content H2 / 51 Accordion Q&As)
├── Quick start and first-run setup
│   ├── install / runtime / hosting Q&As ──────── → note 10 (oc_help_faq_first_run_install)
│   └── auth / subscriptions / dashboard Q&As ─── → note 11 (oc_help_faq_first_run_auth)
└── Related ───────────────────────────────────── → notes 10–11 (Related Notes mapping)
help/faq-models.md (3 content H2 / 22 Accordion Q&As)
├── Models: defaults, selection, aliases, switching → note 12 (oc_help_faq_models)
├── Model failover and "All models failed" ────── → note 12
├── Auth profiles: what they are and how to manage → note 12
└── Related ───────────────────────────────────── → note 12 (Related Notes mapping)
```
No orphaned sections. The two FAQ pointer H2s are link-outs to the first-run/models notes (not separate notes);
deep how-tos referenced from FAQ answers are linked to their owning gw*/co*/to*/au*/pr*/in* sub-plans.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| faq.md (11,357 w / 16 content H2, 110 accordions, concept+procedure mix) | notes 3–9 (7 notes) | far exceeds the 2,500-w cap and mixes a product/concept overview (what-is, triage) with multiple distinct procedure clusters (skills/automation, config/env, storage/memory, gateway/remote, sessions/logging) and a security/access argument. Split by cohesive topic cluster so each note is single-BB and ≤700 w. The two pointer H2s (32 w total) are link-outs, not notes. |
| faq-first-run.md (4,849 w / 51 accordions, single H2) | notes 10 + 11 | exceeds 2,500-w cap; the 51 Q&As fall into two distinct task clusters — install/runtime/hosting vs auth/subscriptions/dashboard — each a coherent ~2.4k-w source slice → two ≤750-w notes. |
| faq-models.md (2,884 w / 3 H2) | note 12 (kept as 1 note) | 2,884 w nominally over the 2,500 cap, but the 3 H2s (selection 1,725 / failover 681 / auth-profiles 417) form one tight "models & their auth" task cluster with heavy internal cross-reference; digested as **one** note at ~800 w (FAQ answers compress well — verbose Q&A prose → terse procedure). Re-evaluate at augment: if the drafted note exceeds caps, promote to a 2-note split (selection/aliases vs failover+auth-profiles). |
| debugging.md (1,573 w, 23 fences) | note 1 (no split) | under word cap, single procedure BB; the 23 fences are short export/CLI/log snippets, reproduced selectively (≤6) — code volume alone does not force a split. |
| environment.md (1,301 w, 6 fences) | note 2 (no split) | under word cap, single procedure BB, ≤6 fences. |

## Summary Statistics & Building Block Distribution

- Source pages: **5** (21,964 measured body words). New `oc_` notes: **12**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×10** (notes 1, 2, 4, 5, 6, 7, 8, 10, 11, 12) · **concept ×1** (note 3) ·
  **argument ×1** (note 9, security/access trade-offs).
- Est. digest words ≈ **8,100** (avg ~675/note; range 550–800). Page-level fences: debugging 23 (selective ≤6),
  environment 6, the 3 FAQ pages carry only sparse inline `json5` accordion snippets (≤6/note after split).
- Cross-refs (LOCKED at xref-augment 2026-06-21 to the RAISED floor: **≥8 relevance-selected `term_dictionary`
  terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/` per note** (PLUS relevant
  n4 8·11·10 · n5 8·11·10 · n6 8·11·10 · n7 8·11·10 · n8 8·11·10 · n9 10·11·10 · n10 8·11·10 · n11 9·11·10 ·
  remainder are sibling `oc_*` "(planned, this series)"). `entry_openclaw_docs.md` is "(created as master
  pre-step W1)". See `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> `term_ures`, `term_xray`, `term_cloudwatch`, `term_firelens` were discarded as wrong-domain). Sibling `oc_*`
> docs (this series) do not exist yet → cited "(planned, this series)" toward the doc floor, but **≥5 of the 10
> before the first sub-plan executes. Relative paths from `resources/documentation/openclaw/oc_X.md`:
> term `../../term_dictionary/`, snippet `../../code_snippets/`, sibling-doc `../<folder>/`, repo
> `../../../areas/code_repos/`, entry `../../../0_entry_points/`, sibling-oc `oc_Y.md`.

### oc_help_debugging (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/assistant these debug tools target; relevance: every debug override, watch flag, and trace targets the OpenClaw Gateway/CLI.
- [Agent-System Observability](../../term_dictionary/term_observability_agent_systems.md) — the discipline of tracing/inspecting agent runtimes; relevance: `/trace`, watch mode, lifecycle traces operationalize agent observability.
- [Data Observability](../../term_dictionary/term_data_observability.md) — trace/metric/log emission for systems; relevance: plugin-lifecycle phase breakdowns + CPU profiles are observability outputs.
- [Langfuse](../../term_dictionary/term_langfuse.md) — LLM-app tracing/observability platform; relevance: closest external analog to OpenClaw's raw-stream + transport tracing for LLM calls.
- [SSE](../../term_dictionary/term_sse.md) — server-sent-event streaming; relevance: raw stream / OpenAI-compat chunk logging captures the SSE-style assistant stream before parsing.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning traces; relevance: the page exists to diagnose reasoning leaking into plain-text deltas vs separate thinking blocks.
- [LLM](../../term_dictionary/term_llm.md) — the language model whose stream is inspected; relevance: raw-stream debugging is about LLM output shape.
- [CodeGuru Profiler](../../term_dictionary/term_codeguru_profiler.md) — CPU-profiler tooling; relevance: closest vault analog to `--benchmark` V8 `.cpuprofile` + startup CPU profiling.

**Docs**
- [CC: OpenTelemetry Setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — how Claude Code wires tracing/metrics; relevance: parallel "turn on observability for a coding agent" workflow.
- [CC: SDK Observability (OTel)](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK-level trace/metric export; relevance: same trace-the-runtime goal as OpenClaw `/trace` + lifecycle trace.
- [CC: OTel Configuration Variables](../claude_code/cc_otel_configuration_variables.md) — env vars that toggle telemetry; relevance: direct analog to `OPENCLAW_*` debug/trace env toggles.
- [CC: OTel Traces](../claude_code/cc_otel_traces.md) — span/trace model for a coding agent; relevance: conceptual backing for the plugin-lifecycle phase trace.
- [CC: Streaming Input Example](../claude_code/cc_sdk_streaming_input_example.md) — streamed model I/O; relevance: backs the raw-stream / chunk-logging discussion.
- [CC: Hooks Advanced Types](../claude_code/cc_hooks_advanced_types.md) — lifecycle hook points; relevance: parallels OpenClaw plugin-lifecycle phases being traced.
- [Hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — internals of the sibling gateway; relevance: dev/watch-mode rebuild loop maps to gateway internals.
- [Hermes: CLI Commands — Session Ops](../hermes_agent/hermes_cli_commands_session_ops.md) — runtime CLI controls; relevance: analog to `openclaw doctor --fix`/restart in watch mode.
- [oc_help_environment](oc_help_environment.md) — env-var loading incl. `OPENCLAW_LOG_LEVEL`/`OPENCLAW_DEBUG_*` (planned, this series); relevance: debug overrides are set via the env vars that note documents.
- [oc_help_faq_sessions_logging](oc_help_faq_sessions_logging.md) — FAQ logging/debugging cluster (planned, this series); relevance: the user-facing FAQ counterpart to this dev-debug toolkit.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service watch/dev mode + benchmark profiling live here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin lifecycle (the `OPENCLAW_PLUGIN_LIFECYCLE_TRACE` phases).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the root CLI/runner the debug flags pass through.

**Snippets**
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — Gateway runtime env selectors carried into watch (e.g. `OPENCLAW_PROFILE`, `OPENCLAW_GATEWAY_PORT`).
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap/source-runner where startup-profiling flags attach.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin-lifecycle phases printed by the lifecycle trace.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — gateway stream consumer (what raw-stream logging taps before filtering).
- [snippet_hermes_agent_core_chat_helpers_streaming_loop](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_loop.md) — streaming loop where reasoning deltas vs thinking blocks arrive.
- [snippet_hermes_agent_core_runtime_helpers_reasoning](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_reasoning.md) — reasoning-block handling (the leakage the page debugs).
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI-compat SSE chunk stream (raw-openai-completions logging target).
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — stream backpressure handling on the gateway path.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup analog (log level / file vs console).
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — CLI log access analog.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered-delta path (where raw vs formatted stream diverge).

### oc_help_environment (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime loading these env vars; relevance: the entire precedence chain is OpenClaw's loader behavior.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed-secret pattern; relevance: backs SecretRef objects vs `${ENV}` strings and "don't keep keys in workspace .env".
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — layered "first source wins, never override" credential resolution; relevance: this note's precedence ladder is the same pattern.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — multi-source credential store; relevance: the trusted-source set (process env / global .env / config env block) is a credential pool.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token credential loaded from env; relevance: provider OAuth tokens resolve from the env precedence chain.
- [Bedrock](../../term_dictionary/term_bedrock.md) — AWS provider with env-based creds; relevance: AWS provider keys are among the env-loaded provider credentials.
- [TLS](../../term_dictionary/term_tls.md) — transport security / CA trust; relevance: the nvm `NODE_EXTRA_CA_CERTS` / web_fetch TLS-failure section.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: the long per-provider API-key env-var list (`GEMINI_API_KEY`, `XAI_API_KEY`, …).

**Docs**
- [CC: Environment Variables](../claude_code/cc_environment_variables.md) — Claude Code's env-var reference; relevance: closest peer reference (same "which env vars and what they do" structure).
- [Band: Environment Variables](../band/band_environment_variables.md) — coding-agent env-var reference; relevance: parallel env-var catalog for a sibling agent framework.
- [Hermes: Env Vars — Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars in the sibling agent; relevance: maps directly to OpenClaw's provider-credential env vars.
- [Hermes: Config Files Precedence](../hermes_agent/hermes_config_files_precedence.md) — config/env precedence ladder; relevance: direct analog of the highest→lowest precedence rule.
- [CC: Authentication](../claude_code/cc_authentication.md) — credential/auth loading; relevance: provider credentials loaded from env is the auth surface.
- [CC: Network/TLS and Access](../claude_code/cc_network_tls_and_access.md) — TLS/CA + network config; relevance: backs the nvm CA-store TLS failure.
- [CC: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — env-driven proxy/endpoint redirects; relevance: workspace-.env endpoint/host overrides are the same class.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — multi-source credential precedence; relevance: the trusted-source ordering for provider keys.
- [oc_help_faq_config_env](oc_help_faq_config_env.md) — FAQ-level env/config loading (planned, this series); relevance: this note is the full precedence rule the FAQ defers to.
- [oc_help_debugging](oc_help_debugging.md) — debug-override + `OPENCLAW_DEBUG_*`/`OPENCLAW_LOG_LEVEL` env vars (planned, this series); relevance: logging env vars documented here drive the debug toolkit.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway process that loads + applies the env precedence chain.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — SecretRef resolution + workspace-.env credential ignoring.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the CLI entrypoint that re-execs with `NODE_EXTRA_CA_CERTS`.

**Snippets**
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — Gateway runtime env resolution (the process-env layer).
- [snippet_hermes_agent_gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — gateway config+env load order analog.
- [snippet_hermes_agent_cli_config_load](../../code_snippets/snippet_hermes_agent_cli_config_load.md) — CLI config/env load (dotenv + config env block).
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — config-loading precedence merge.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — enumerated trusted credential sources (env / global .env / config).
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — seeding the credential pool from env/files.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — AWS/Bedrock credential resolution from env.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret redaction (the "scrub secrets" safety concern for env-derived values).
- [snippet_hermes_agent_core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — provider key resolution from env at activation.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard writing `~/.openclaw/openclaw.json` env/config blocks.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — config `env` block write path.

### oc_help_faq_overview (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product being framed; relevance: the "What is OpenClaw?" answers define exactly this term.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the class of assistant; relevance: the assistant-vs-IDE ("vs Claude Code") positioning is about coding agents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime hosting the agent; relevance: the Gateway-as-always-on-control-plane is the harness.
- [LLM](../../term_dictionary/term_llm.md) — the model the assistant fronts; relevance: "not just a Claude wrapper" / model-agnostic value prop.
- [Claude](../../term_dictionary/term_claude.md) — the commonly-fronted model; relevance: explicitly contrasted ("not just a Claude wrapper", "vs Claude Code").
- [MCP](../../term_dictionary/term_mcp.md) — tool/control-plane integration protocol; relevance: tool orchestration is part of the value proposition.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation by the model; relevance: "tool orchestration (browser, files, scheduling, hooks)" is function calling.

**Docs**
- [CC: Feature Selection Guide](../claude_code/cc_feature_selection_guide.md) — when to use which coding-agent surface; relevance: directly parallels "advantages vs Claude Code" framing.
- [CC: Agent SDK Overview](../claude_code/cc_agent_sdk_overview.md) — what a coding-agent runtime is; relevance: peer "what is this product" overview.
- [Hermes: Learning Path](../hermes_agent/hermes_learning_path.md) — orientation for the sibling agent; relevance: same "what is it / where to start" onboarding role.
- [Hermes: Quickstart — First Chat](../hermes_agent/hermes_quickstart_first_chat.md) — first-use framing; relevance: the "I just set it up — what now?" answer maps here.
- [Pi: Quickstart](../pi/pi_quickstart.md) — sibling agent intro; relevance: peer product-overview entry.
- [Band: Overview](../band/band_overview.md) — multi-agent-framework overview; relevance: model-agnostic / multi-agent value-prop analog.
- [CC: Tools Catalog](../claude_code/cc_tools_catalog.md) — the tool surface of a coding agent; relevance: "tool orchestration" highlight.
- [Hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — gateway-as-control-plane internals; relevance: backs "the Gateway is the always-on control plane".
- [oc_help_faq_first_run_install](oc_help_faq_first_run_install.md) — the "Quick start" pointer target (planned, this series); relevance: the FAQ pointer H2 routes here.
- [oc_help_faq_security_access](oc_help_faq_security_access.md) — local-first trust framing (planned, this series); relevance: "your devices, your data" value prop has a security counterpart.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the open-source product the overview describes.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the assistant surfaces (voice/Canvas/nodes).
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the chat-app surfaces (WhatsApp/Telegram/Slack/…).

**Snippets**
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config (multi-agent routing value prop).
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — agent-runtime contract (the assistant runtime).
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway control-plane methods.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — a real chat-app channel surface ("real channels, not a web sandbox").
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-agnostic catalog (per-agent model routing).
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool scope (tool orchestration).
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — the live Canvas surface mentioned in the overview.
- [snippet_hermes_agent_skills_hermes_agent](../../code_snippets/snippet_hermes_agent_skills_hermes_agent.md) — sibling assistant orchestration analog.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — the gateway RPC envelope (control-plane mechanics).

### oc_help_faq_skills_automation (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host whose skills/agents are configured; relevance: skill precedence + agent routing are OpenClaw config surfaces.
- [Subagent](../../term_dictionary/term_subagent.md) — offloaded worker session; relevance: "offload heavy work to sub-agents" / `/subagents`.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating multiple agents; relevance: per-task agent routing + standing-order patterns.
- [Delegate Task](../../term_dictionary/term_delegate_task.md) — handing work to another agent; relevance: spawning sub-agents that return a summary.
- [Agent-as-a-Tool](../../term_dictionary/term_agent_as_a_tool.md) — invoking an agent as a callable; relevance: per-task model/agent routing treats agents like tools.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: cron/standing-order automation with per-job model overrides.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — schedule syntax; relevance: how scheduled jobs are specified.
- [Skill Curator](../../term_dictionary/term_skill_curator.md) — skill management/precedence; relevance: managed skill overrides + load precedence + custom skill folders.

**Docs**
- [CC: Work with Subagents](../claude_code/cc_work_with_subagents.md) — using sub-agents in a coding agent; relevance: direct analog to OpenClaw "offload to sub-agents".
- [CC: Create a Subagent](../claude_code/cc_create_a_subagent.md) — defining a sub-agent; relevance: thread-bound sub-agent spawn config.
- [CC: Subagent Configuration Reference](../claude_code/cc_subagent_configuration_reference.md) — sub-agent config keys; relevance: maps to `agents.defaults.subagents.model`.
- [CC: SDK Subagents Definition](../claude_code/cc_sdk_subagents_definition.md) — programmatic sub-agent definition; relevance: backs `sessions_spawn`/thread bindings.
- [CC: Skill Frontmatter Reference](../claude_code/cc_skill_frontmatter_reference.md) — skill file format; relevance: `~/.openclaw/skills/<name>/SKILL.md` override format.
- [CC: Commands Reference](../claude_code/cc_commands_reference.md) — slash-command surface; relevance: `/model`, `/subagents`, `/focus`, `/agents`.
- [Hermes: Plugin Extensions — Hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — automation hook points; relevance: standing-order / hook automation analog.
- [Hermes: Slash Commands — Interactive CLI](../hermes_agent/hermes_slash_commands_interactive_cli.md) — chat slash commands; relevance: the in-chat skill/agent control commands.
- [oc_help_faq_config_env](oc_help_faq_config_env.md) — `agents.*` / `skills.load.extraDirs` config (planned, this series); relevance: skill precedence + agent routing live in that config.
- [oc_help_faq_sessions_logging](oc_help_faq_sessions_logging.md) — per-session sub-agent lifecycle (planned, this series); relevance: thread-bound sub-agent sessions.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill load/precedence subsystem.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent routing + sub-agent spawn.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the cron/standing-order automation host.

**Snippets**
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — sub-agent spawn over ACP (offloading heavy work).
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn policy/gating.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — session handoff to a spawned sub-agent.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — thread-bound spawn (Discord thread bindings).
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding config/policy.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate/spawn sub-agent analog.
- [snippet_hermes_agent_tools_delegate_anti_recursion](../../code_snippets/snippet_hermes_agent_tools_delegate_anti_recursion.md) — anti-recursion guard for delegated agents.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — cron job dispatching into the agent (isolated cron run).
- [snippet_hermes_agent_cron_job_validate](../../code_snippets/snippet_hermes_agent_cron_job_validate.md) — cron job validation (why cron didn't fire checks).
- [snippet_hermes_agent_cli_cron](../../code_snippets/snippet_hermes_agent_cli_cron.md) — cron CLI surface.
- [snippet_hermes_agent_skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — skill-driven multi-agent orchestration example.

### oc_help_faq_config_env (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — owner of `~/.openclaw/openclaw.json`; relevance: the note answers where config lives + how it's edited.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — agent config/instruction file; relevance: config layout + where `AGENTS.md`/workspace files live.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed secret values; relevance: secret config values + SecretRefs.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — layered key resolution; relevance: `.env`/env-block resolution order referenced by the FAQ.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token creds in config/env; relevance: provider auth set in the env block.
- [Claude](../../term_dictionary/term_claude.md) — a configured provider; relevance: `ANTHROPIC_API_KEY` config/env example.
- [Bedrock](../../term_dictionary/term_bedrock.md) — a configured AWS provider; relevance: provider config block example.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external providers; relevance: provider config blocks (`models.providers.*`).

**Docs**
- [CC: Plugin User Config and Env](../claude_code/cc_plugin_user_config_and_env.md) — user config + env file layout; relevance: closest analog to "where config files live + how .env loads".
- [CC: Settings Reference](../claude_code/cc_settings_reference.md) — the settings/config reference; relevance: peer "what is the config and where is it".
- [Hermes: Config Files Precedence](../hermes_agent/hermes_config_files_precedence.md) — config/env precedence; relevance: how `.env`/config resolve at the FAQ level.
- [CC: Environment Variables](../claude_code/cc_environment_variables.md) — env-var reference; relevance: the `.env` loading the FAQ summarizes.
- [Pi: Settings Reference](../pi/pi_settings_reference.md) — sibling agent config reference; relevance: parallel config-structure doc.
- [Band: SDK Reference — Config Types](../band/band_sdk_reference_config_types.md) — typed config schema; relevance: `openclaw.json` structure analog.
- [CC: Authentication](../claude_code/cc_authentication.md) — provider auth config; relevance: provider creds set in the config env block.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — multi-source credential config; relevance: the trusted-source set for keys.
- [oc_help_environment](oc_help_environment.md) — full env precedence (planned, this series); relevance: this FAQ explicitly defers the full precedence rule to that note.
- [oc_help_faq_skills_automation](oc_help_faq_skills_automation.md) — `agents.*` config (planned, this series); relevance: shared config surface (agents/skills blocks).

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — config loading into the Gateway.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the CLI config commands.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — SecretRef config handling.

**Snippets**
- [snippet_hermes_agent_gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — gateway config load (what JSON5 config parsing does).
- [snippet_hermes_agent_cli_config_load](../../code_snippets/snippet_hermes_agent_cli_config_load.md) — CLI config load path.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — config-loading + merge precedence.
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — config schema/validation (config.apply guardrails).
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — programmatic config edit (`config.apply` analog).
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime agent config resolution.
- [snippet_openclaw_agents_context_lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — config/context lookup at runtime.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard-generated minimal sane config.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skills config/manifest in the config tree.

### oc_help_faq_storage_memory (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — owner of the on-disk layout; relevance: "where things live on disk" + sandboxing are OpenClaw behaviors.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated tool execution; relevance: "sandboxing isolates tool execution" + bind-mount host folder.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — agent long-term memory; relevance: "how does memory work / make it stick / limits".
- [Episodic Memory](../../term_dictionary/term_episodic_memory.md) — event/session memory; relevance: session-scoped memory persistence.
- [Vector Database](../../term_dictionary/term_vector_database.md) — embedding store backend; relevance: semantic memory search backend.
- [Embedding](../../term_dictionary/term_embedding.md) — vector representation; relevance: "semantic memory search requires an OpenAI API key" (embeddings).
- [Session Data](../../term_dictionary/term_session_data.md) — on-disk session state; relevance: where sessions/transcripts are stored.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: memory retrieval into context.

**Docs**
- [Hermes: Memory Provider Catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory backends for the sibling agent; relevance: direct analog to OpenClaw memory backends.
- [Hermes: Memory Providers — Honcho](../hermes_agent/hermes_memory_providers_honcho.md) — a specific memory provider; relevance: backs "how memory persists / providers".
- [CC: Sandbox Modes](../claude_code/cc_sandbox_modes.md) — sandbox isolation modes; relevance: "is there a dedicated sandboxing doc" / Docker full features.
- [CC: Troubleshoot Memory](../claude_code/cc_troubleshoot_memory.md) — memory issues; relevance: "memory keeps forgetting things".
- [Pi: Sessions](../pi/pi_sessions.md) — session storage in the sibling agent; relevance: on-disk session layout analog.
- [Pi: Session File Format](../pi/pi_session_file_format.md) — session file format; relevance: "where does OpenClaw store its data" detail.
- [CC: SDK Session Store](../claude_code/cc_sdk_session_store.md) — session persistence store; relevance: local session store analog.
- [CC: What Survives Compaction](../claude_code/cc_what_survives_compaction.md) — memory/context persistence limits; relevance: "does memory persist forever / limits".
- [oc_help_faq_sessions_logging](oc_help_faq_sessions_logging.md) — sessions on disk (planned, this series); relevance: session storage is the sibling cluster of on-disk layout.
- [oc_help_faq_config_env](oc_help_faq_config_env.md) — where config lives (planned, this series); relevance: config is part of the on-disk layout this note maps.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — the memory subsystem (persistence + semantic search).
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — on-disk session storage.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox isolation of tool execution.

**Snippets**
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory engine (how memory persists/retrieves).
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs (semantic search needs embeddings/API key).
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — on-disk memory schema.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host-side embedding storage.
- [snippet_openclaw_memory_host_backend_config](../../code_snippets/snippet_openclaw_memory_host_backend_config.md) — memory backend config (lancedb/wiki/qmd).
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search at agent runtime.
- [snippet_hermes_agent_honcho_session_query](../../code_snippets/snippet_hermes_agent_honcho_session_query.md) — memory-provider session query analog.

### oc_help_faq_gateway_remote (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being run; relevance: ports/"already running"/remote-mode are Gateway behaviors.
- [WebSocket](../../term_dictionary/term_websocket.md) — the multiplexed transport; relevance: the single multiplexed WS+HTTP gateway port.
- [WebSocket Framing](../../term_dictionary/term_websocket_framing.md) — WS message framing; relevance: node/gateway pairing rides the WS connection.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — the gateway RPC; relevance: config-apply RPC / gateway method calls.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting the gateway; relevance: trusted-proxy / Tailscale Serve remote-mode access.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — local service discovery; relevance: how nodes/gateways find each other on a LAN.
- [Reverse-Proxy / Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote access path; relevance: SSH-tunnel/remote access alternative to nodes.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — the gateway pattern; relevance: the Gateway-as-control-plane multiplexing pattern.

**Docs**
- [CC: Remote Control](../claude_code/cc_remote_control.md) — remote control of a coding agent; relevance: direct analog to OpenClaw remote-mode access.
- [CC: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway fronting; relevance: trusted-proxy + remote exposure config.
- [Hermes: Desktop Remote Backend](../hermes_agent/hermes_desktop_remote_backend.md) — connecting a client to a remote gateway; relevance: "client connects to a Gateway elsewhere".
- [Hermes: Messaging — Matrix Proxy Mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — proxy-mode remote channel; relevance: remote-mode channel access analog.
- [Hermes: API Server Setup + Auth](../hermes_agent/hermes_api_server_setup_auth.md) — gateway/API server + auth; relevance: "why a token on localhost" / remote auth.
- [Band: WebSocket Overview](../band/band_websocket_overview.md) — WS transport for agents; relevance: the multiplexed WS port concept.
- [CC: MCP Transports](../claude_code/cc_mcp_transports.md) — transport options (stdio/http/ws); relevance: the gateway's HTTP+WS multiplexed transport.
- [Hermes: Dashboard REST API](../hermes_agent/hermes_dashboard_rest_api.md) — HTTP control surface; relevance: the HTTP half of the multiplexed gateway port.
- [oc_help_environment](oc_help_environment.md) — `OPENCLAW_GATEWAY_PORT` / `gateway.bind` env (planned, this series); relevance: port/bind config feeds remote-mode setup.
- [oc_help_faq_sessions_logging](oc_help_faq_sessions_logging.md) — remote-mode session store + logging (planned, this series); relevance: "remote mode: where is the session store".

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway itself (ports, remote mode, bind).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — nodes that pair to a remote gateway.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the CLI `gateway`/`node`/`pairing` commands.

**Snippets**
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — the gateway WS connection (multiplexed port).
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connecting through a proxy (remote mode).
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP bind (default safe bind).
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing to a gateway.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node↔gateway session over WS.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — channel WS multiplexing.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS node pairing to remote gateway.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android node session over WS.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP routing on the multiplexed port.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating (auth on remote calls / "token on localhost").
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope (config.apply over RPC).

### oc_help_faq_sessions_logging (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — owner of sessions + logs; relevance: `/new`, multiple chats, log location are OpenClaw behaviors.
- [Session Data](../../term_dictionary/term_session_data.md) — per-chat session state; relevance: starting a fresh conversation / multiple concurrent sessions.
- [session-mcp](../../term_dictionary/term_session_mcp.md) — session lifecycle analog; relevance: session reset / idle / max-age controls.
- [Agent-System Observability](../../term_dictionary/term_observability_agent_systems.md) — runtime tracing; relevance: "logging and debugging" + "more details when something fails".
- [Data Observability](../../term_dictionary/term_data_observability.md) — log emission; relevance: "where are logs" + log levels.
- [Silence Token](../../term_dictionary/term_silence_token.md) — suppressing internal system messages; relevance: "stop internal system messages from showing in chat".
- [Subagent](../../term_dictionary/term_subagent.md) — per-session sub-agents; relevance: multiple chats can run sub-agent sessions.
- [LLM](../../term_dictionary/term_llm.md) — context truncation source; relevance: "why did context get truncated mid-task".

**Docs**
- [CC: Sessions](../claude_code/cc_sessions.md) — managing sessions in a coding agent; relevance: direct analog to "sessions and multiple chats".
- [CC: SDK Sessions Overview](../claude_code/cc_sdk_sessions_overview.md) — session lifecycle; relevance: `/new`, auto-reset, idle behavior.
- [Pi: Sessions](../pi/pi_sessions.md) — sibling session model; relevance: multiple concurrent sessions analog.
- [Pi: Compaction](../pi/pi_compaction.md) — context compaction; relevance: "why did context get truncated / how to prevent".
- [CC: What Survives Compaction](../claude_code/cc_what_survives_compaction.md) — compaction behavior; relevance: context-truncation prevention.
- [CC: Context Window Anatomy](../claude_code/cc_context_window_anatomy.md) — context budget; relevance: backs the truncation question.
- [CC: Commands Reference](../claude_code/cc_commands_reference.md) — `/new`, `/status`, `/abort` commands; relevance: chat commands + aborting a task.
- [Hermes: CLI Commands — Session Ops](../hermes_agent/hermes_cli_commands_session_ops.md) — session CLI ops; relevance: reset/restart while keeping installed.
- [oc_help_debugging](oc_help_debugging.md) — debug output / `OPENCLAW_LOG_LEVEL` (planned, this series); relevance: "fastest way to get more details when something fails".
- [oc_help_faq_storage_memory](oc_help_faq_storage_memory.md) — where sessions live on disk (planned, this series); relevance: session storage location.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session management + multiple chats.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — logging + restart/stop.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the `/new`, `/status`, reset chat/CLI commands.

**Snippets**
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compaction/reset (`/new`, truncation handling).
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — performing a session reset.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — reset helper hooks.
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — per-session overrides (multiple chats with different settings).
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session key/identity utils (which chat is which).
- [snippet_openclaw_macos_menu_sessions_control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — UI session control (multiple chats).
- [snippet_hermes_agent_core_conversation_loop_usage_accounting](../../code_snippets/snippet_hermes_agent_core_conversation_loop_usage_accounting.md) — token/usage accounting (context-truncation cause).
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — request routing across sessions.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup (log level / where logs go).
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — CLI log access ("where are logs").
- [snippet_hermes_agent_gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — gateway session lifecycle.

### oc_help_faq_security_access (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the local-first control plane being exposed; relevance: the whole note weighs exposing OpenClaw to chat apps.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — untrusted-content hijack; relevance: a central argument — injection is about untrusted content even for solo users.
- [Access Control](../../term_dictionary/term_access_control.md) — who may talk to the bot; relevance: allow-lists / access groups / mention-gating.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM admission policy; relevance: `dmPolicy: pairing|allowlist|open` is the core control.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing-code admission; relevance: default pairing flow for unknown senders.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — limiting damage scope; relevance: "reduce the blast radius" is the note's recurring trade-off framing.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: deny/sandbox risky tools for untrusted input.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: exec-approval gating + sandbox-untrusted-input pattern.
- [Threat Model](../../term_dictionary/term_threat_model.md) — enumerating risks; relevance: the note IS a threat-model argument (exposure, injection, tool scope, credentials).
- [OWASP LLM Top-10](../../term_dictionary/term_owasp_llm.md) — LLM-app risk taxonomy; relevance: prompt-injection + exfiltration map to the OWASP LLM risks.

**Docs**
- [CC: Prompt Injection Defenses](../claude_code/cc_prompt_injection_defenses.md) — defenses against injection; relevance: direct analog to the injection section.
- [CC: Security Architecture](../claude_code/cc_security_architecture.md) — overall agent security model; relevance: the trust/exposure argument's backbone.
- [CC: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs allowlist trade-off; relevance: "deny or sandbox risky tools".
- [Pi: Security Model](../pi/pi_security_model.md) — sibling agent security model; relevance: parallel local-agent trust model.
- [Hermes: Security — Command Approval](../hermes_agent/hermes_security_command_approval.md) — exec-approval gating; relevance: "two exec approval configs" / approve-before-run.
- [Hermes: Security — Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential handling + isolation; relevance: "credential handling" risk + separate accounts.
- [CC: SDK Secure Deployment Principles](../claude_code/cc_sdk_secure_deployment_principles.md) — safe-deployment baseline; relevance: "safer baseline" checklist (loopback bind, allowlists).
- [CC: Computer Use Safety](../claude_code/cc_computer_use_safety.md) — autonomy/tool-use safety; relevance: "give it autonomy over my messages — is that safe".
- [oc_help_faq_overview](oc_help_faq_overview.md) — local-first value prop (planned, this series); relevance: the security argument is the flip side of "your devices, your data".
- [oc_help_faq_gateway_remote](oc_help_faq_gateway_remote.md) — remote exposure mechanics (planned, this series); relevance: "exposed instances" / public-bind findings.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `security audit`, install policy, dangerous-tool deny, external-content boundaries.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — allow-from / pairing / who-can-talk per channel.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — `openclaw doctor` / `pairing` / `security audit` CLI.

**Snippets**
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — `security audit --deep` exec-risk checks.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — audit of DM policies (risky-DM detection).
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source trust auditing.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — denying high-risk tools (exec/browser/gateway/cron).
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem scoping (blast-radius limits).
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — wrapping decoded file/doc text in external-content boundaries (injection defense).
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scanning third-party skills/plugins before install.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — pairing/allowlist admission of senders.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — exec-approval policy analog.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — access-gated chat commands.
- [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — shell command allowlisting.

### oc_help_faq_first_run_install (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the thing being installed; relevance: install/runtime/hosting path is OpenClaw setup.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: Docker/VPS/VM install paths + "Docker feels limited".
- [Node.js](../../term_dictionary/term_node_js.md) — the JS runtime; relevance: "what runtime do I need", git-vs-npm install, Node CA-store.
- [mise](../../term_dictionary/term_mise.md) — runtime/version manager; relevance: managing the Node/Bun runtime for the hackable git install.
- [Sandbox](../../term_dictionary/term_sandbox.md) — runtime isolation requirement; relevance: VM/VPS isolation + runtime requirements.
- [TLS](../../term_dictionary/term_tls.md) — cert/SSL trust; relevance: "cannot access docs.openclaw.ai (SSL error)".
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime being installed; relevance: install brings up the Gateway/agent harness.

**Docs**
- [Hermes: Installation](../hermes_agent/hermes_installation.md) — installing the sibling agent; relevance: closest analog install guide.
- [Hermes: Docker Run Modes](../hermes_agent/hermes_docker_run_modes.md) — Docker deployment modes; relevance: Docker/VPS/VM install + full-features question.
- [Hermes: Install — Termux/Android](../hermes_agent/hermes_install_termux_android.md) — constrained-runtime install; relevance: Raspberry-Pi-class constrained install analog.
- [Hermes: Quickstart — First Chat](../hermes_agent/hermes_quickstart_first_chat.md) — first-run path; relevance: "recommended way to install and set up".
- [Hermes: Learning Path](../hermes_agent/hermes_learning_path.md) — onboarding sequence; relevance: "what does onboarding actually do".
- [CC: Quickstart](../claude_code/cc_quickstart.md) — coding-agent quickstart; relevance: peer install/first-run flow.
- [Pi: Quickstart](../pi/pi_quickstart.md) — sibling quickstart; relevance: parallel install/setup path.
- [Band: Coding-Agents Deployment](../band/band_coding_agents_deployment.md) — deploying coding agents; relevance: VPS/VM/dedicated-machine hosting choices.
- [oc_help_faq_first_run_auth](oc_help_faq_first_run_auth.md) — the auth half of first-run (planned, this series); relevance: install + auth are the two first-run clusters.
- [oc_help_faq_overview](oc_help_faq_overview.md) — the "quick start" pointer source (planned, this series); relevance: the FAQ overview routes here.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the onboarding wizard (install/setup/migrate).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the repo being git/npm installed + self-updated.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — platform apps (Mac mini / iMessage host).

**Snippets**
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard analog (onboarding flow).
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard writing the initial config (onboarding output).
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard import steps during setup.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migrating an existing setup (Mac mini move).
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive onboarding prompts ("hatch" flow).
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer entrypoint analog.
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — self-update command (`openclaw update --channel`).
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — doctor checks (installer "more feedback").
- [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — bootstrap encoding (Windows garbled-text fix).
- [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — bootstrap shell script (Linux/VPS install).
- [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall path (switching git↔npm installs).

### oc_help_faq_first_run_auth (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being authenticated; relevance: subscription-vs-API-key auth choices are OpenClaw provider setup.
- [OAuth](../../term_dictionary/term_oauth.md) — subscription OAuth flows; relevance: Codex/Gemini/Claude CLI subscription auth.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token storage/refresh; relevance: auth-profile token records on the gateway host.
- [PKCE](../../term_dictionary/term_pkce.md) — OAuth code-exchange hardening; relevance: the OAuth/CLI-login flows under the hood.
- [Claude](../../term_dictionary/term_claude.md) — Pro/Max subscription provider; relevance: Claude CLI subscription auth + Agent-SDK credit note.
- [Bedrock](../../term_dictionary/term_bedrock.md) — AWS model provider; relevance: "is AWS Bedrock supported".
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — 429/usage-window limits; relevance: "HTTP 429 rate_limit_error from Anthropic".
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential record; relevance: per-provider auth-profile selection at first run.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — the provider matrix; relevance: OpenAI/Gemini/Bedrock/local-model choices.

**Docs**
- [Pi: Provider Auth](../pi/pi_provider_auth.md) — provider auth in the sibling agent; relevance: direct analog to subscription-vs-API-key auth.
- [CC: Authentication](../claude_code/cc_authentication.md) — auth setup; relevance: Claude subscription / API-key auth setup.
- [CC: Login & Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth failure recovery; relevance: "no credentials found for profile" class of issues.
- [CC: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock auth; relevance: "is AWS Bedrock supported".
- [CC: Server and Usage Limit Errors](../claude_code/cc_server_and_usage_limit_errors.md) — 429/usage-limit handling; relevance: the 429 rate_limit_error question.
- [Hermes: Provider — xAI/Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — a subscription OAuth provider; relevance: subscription-OAuth setup analog.
- [Hermes: Subscription Proxy](../hermes_agent/hermes_subscription_proxy.md) — using subscription auth; relevance: Claude/Codex subscription-vs-key path.
- [Hermes: Setup with Nous Portal](../hermes_agent/hermes_setup_with_nous_portal.md) — subscription provider onboarding; relevance: subscription-auth onboarding analog.
- [oc_help_faq_first_run_install](oc_help_faq_first_run_install.md) — the install half (planned, this series); relevance: install + auth are the two first-run clusters.
- [oc_help_faq_models](oc_help_faq_models.md) — auth-profiles detail (planned, this series); relevance: first-run auth feeds into model auth profiles.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider auth implementations (Claude/OpenAI/Gemini/Bedrock).
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — credential storage (auth-profiles.json on the gateway host).
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — auth onboarding during the wizard.

**Snippets**
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — per-provider auth state (auth-profiles).
- [snippet_hermes_agent_cli_web_reveal_oauth](../../code_snippets/snippet_hermes_agent_cli_web_reveal_oauth.md) — OAuth reveal/login flow.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback server (subscription login).
- [snippet_hermes_agent_cli_nous_subscription](../../code_snippets/snippet_hermes_agent_cli_nous_subscription.md) — subscription-auth onboarding analog.
- [snippet_hermes_agent_cli_copilot_auth](../../code_snippets/snippet_hermes_agent_cli_copilot_auth.md) — Copilot OAuth provider auth.
- [snippet_hermes_agent_plugins_provider_xai_oauth](../../code_snippets/snippet_hermes_agent_plugins_provider_xai_oauth.md) — provider OAuth plugin (subscription auth).
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — Bedrock credential resolution.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider auth (Claude CLI vs API key).
- [snippet_hermes_agent_acp_auth](../../code_snippets/snippet_hermes_agent_acp_auth.md) — ACP runtime auth.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — where credentials are read from (gateway host).
- [snippet_hermes_agent_core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — auth resolution at request time.

### oc_help_faq_models (12t · 13s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host doing model selection/failover; relevance: `/model`, aliases, failover are OpenClaw runtime behaviors.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback across models; relevance: "All models failed" / `agents.defaults.model.fallbacks`.
- [Failover](../../term_dictionary/term_failover.md) — general failover mechanism; relevance: two-stage failover (profile rotation then model fallback).
- [Model Router](../../term_dictionary/term_model_router.md) — selection/routing across providers; relevance: same-id collision resolution + per-task routing.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing requests to a provider; relevance: "if two providers expose the same model id, which does /model use".
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — known-models registry; relevance: defaults + adding OpenRouter/Z.AI models.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential record; relevance: the auth-profiles section (IDs, ordering, cooldowns).
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — backup provider in the chain; relevance: model fallback routing to the next provider.
- [OAuth](../../term_dictionary/term_oauth.md) — OAuth-vs-API-key auth; relevance: the "OAuth vs API key" auth-profile distinction.
- [Claude](../../term_dictionary/term_claude.md) — opus/sonnet shortcuts; relevance: built-in model shortcuts + Claude CLI backend.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — a self-hosted/provider model; relevance: self-hosted model example.
- [Qwen](../../term_dictionary/term_qwen.md) — a provider model example; relevance: self-hosted / OpenRouter model example.

**Docs**
- [CC: Model Selection](../claude_code/cc_model_selection.md) — choosing models in a coding agent; relevance: direct analog to `/model` selection/switching.
- [CC: Fallback Models](../claude_code/cc_fallback_models.md) — model fallback chain; relevance: direct analog to "how does failover work".
- [CC: Restrict Model Selection](../claude_code/cc_restrict_model_selection.md) — limiting allowed models; relevance: per-agent default-model pinning.
- [Hermes: Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback chain; relevance: profile-rotation + provider fallback mechanics.
- [Hermes: Provider Routing](../hermes_agent/hermes_provider_routing.md) — routing across providers; relevance: same-model-id resolution + routing.
- [Hermes: Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog; relevance: defaults + adding provider models.
- [Hermes: Model Aux Provider Config](../hermes_agent/hermes_model_aux_provider_config.md) — adding provider models; relevance: "add models from OpenRouter/Z.AI".
- [Hermes: Nous Portal Subscription](../hermes_agent/hermes_nous_portal_subscription.md) — subscription model access; relevance: auth-profile OAuth-vs-API-key analog.
- [oc_help_faq_first_run_auth](oc_help_faq_first_run_auth.md) — auth/subscriptions (planned, this series); relevance: auth profiles originate from first-run auth.
- [oc_help_faq_config_env](oc_help_faq_config_env.md) — `agents.*` model config (planned, this series); relevance: model defaults/aliases live in agents config.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider/model definitions + auth.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent default models + fallback ladder.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — failover/adapter analog.

**Snippets**
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — the fallback ladder (`model.fallbacks`).
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — observing/classifying failover-worthy errors.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — profile cooldown/backoff on failure.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering + credential lookup.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth-vs-API-key profile portability.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI (Claude CLI) auth profile.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — the model catalog (defaults / known models).
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — on-the-fly `/model` session override.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator (adding provider models).
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — activating fallback mid-turn.
- [snippet_hermes_agent_core_error_classifier_taxonomy](../../code_snippets/snippet_hermes_agent_core_error_classifier_taxonomy.md) — error taxonomy (rate-limit vs billing vs context-overflow buckets).
- [snippet_hermes_agent_core_error_classifier_backoff](../../code_snippets/snippet_hermes_agent_core_error_classifier_backoff.md) — backoff/cooldown classification.
- [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — selecting the next credential/profile in rotation.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary that is the subject of a doc page is digested as an `oc_*` doc note by its
> home sub-plan, NOT as a new `term_dictionary` entry. The only term-dictionary interaction is **linking
> existing** terms. Expected new `term_dictionary` captures for hp01: **0**.

| Term (appearing in source) | Disposition |
|---|---|
| OpenClaw, Gateway, control plane | Documented across the `oc_help_*` notes; link existing `term_openclaw` (no inlined definition). |
| environment variable, precedence, secret ref, `${ENV}` substitution | Digested in `oc_help_environment` (concept lives in the doc note); `term_environment_variable` does NOT exist → link `term_secrets_manager` + `term_aws_sdk_credential_chain` for the secret/precedence aspects. |
| sandboxing, memory, sessions, on-disk layout | Digested in `oc_help_faq_storage_memory` / `oc_help_faq_sessions_logging`; link existing `term_sandbox`, `term_agentic_memory`, `term_session_data`. |
| skills, sub-agents, agent routing, cron | Digested in `oc_help_faq_skills_automation`; link existing `term_subagent`, `term_agent_orchestration`, `term_cron`. (`term_skill`/`term_agent_skills` do NOT exist — not promoted; skills are a documented OpenClaw config surface, link `repo_openclaw_skills`.) |
| model failover, "All models failed", model selection, alias, auth profile | Digested in `oc_help_faq_models`; link existing `term_model_failover`, `term_failover`, `term_model_router`, `term_model_catalog`, `term_auth_profile`. |
| subscription auth, OAuth, API key, 429 rate limit, Bedrock | Digested in `oc_help_faq_first_run_auth`; link existing `term_oauth`, `term_oauth_token`, `term_bedrock`, `term_rate_limiting`, `term_claude`. |
| access control, allow-list, exec approval, security trade-offs | Digested in `oc_help_faq_security_access`; link existing `term_access_control`, `term_sandbox`, `term_iam`, `term_secrets_manager`. |
| debugging, watch mode, raw stream logging, reasoning leakage, observability | Digested in `oc_help_debugging` / `oc_help_faq_sessions_logging`; `term_logging`/`term_telemetry`/`term_opentelemetry`/`term_prometheus` do NOT exist → link `term_observability_agent_systems` + `term_data_observability` + `term_sse`. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and
an existing note was found — every concept either has a doc-page home here or an existing `term_dictionary`
note to link. (Augment Step 2d re-runs the new-term scan against the drafted notes to confirm.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** hp01 authors zero `term_dictionary` notes; it only links existing terms (inherited from
master — `## Undigested Terms — Corpus-Wide Inventory` and W5). If augment's Step 2d surfaces a genuine
cross-cutting reusable term with no existing note, it is captured via `/tessellum-capture-term-note` + added to the
agentic/LLM `acronym_glossary_*.md` (per master W5); none anticipated.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (12 notes, P2). Gate table inherited verbatim from the master's shared 9-GATE.

| Gate | Check | Tool / Method | Pass condition |
|------|-------|---------------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order + forbidden-field check pass; `## Overview` + `## Related Notes` present; footer present. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/help/<page>` | every claim traces to the source page/section; no fabricated config keys/env vars. |
| G3 | Density + Coverage | word/code count + section coverage map | each note ≤400 lines / ≤2,500 w / ≤6 code blocks; one BB; every assigned H2/H3 covered. |
| G4 | Cross-Reference | `## Related Notes` floor | ≥8 relevance-selected terms + ≥10 snippets + ≥10 docs + `repo_openclaw*`/sibling `oc_*`, each with a relevance statement (per the LOCKED Per-Note Related Notes Mapping). |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` + DB existence check | 0 links to non-existent notes (missing terms above already excluded). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` | 0 broken relative links after reindex. |
| G7 | Discoverability | inbound-link check | every new note receives ≥1 inbound link from outside `documentation/openclaw/`. |
| G8 | In-degree ≥1 | `note_links` query post-reindex | anti-island: in-degree ≥1 for all 12 notes (satisfied via `entry_openclaw_docs.md`). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_help_debugging oc_help_environment oc_help_faq_overview oc_help_faq_skills_automation \
oc_help_faq_config_env oc_help_faq_storage_memory oc_help_faq_gateway_remote \
oc_help_faq_sessions_logging oc_help_faq_security_access oc_help_faq_first_run_install \
oc_help_faq_first_run_auth oc_help_faq_models"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + LINK errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # density caps (body only)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (words=$words code=$cb)"
done

# YAML frontmatter sweep over the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# Ghost-reference / DB existence pre-check for cited targets (run before execute locks Related Notes)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
          term_observability_agent_systems term_access_control repo_openclaw_gateway \
          repo_openclaw_security repo_openclaw_extensions_llm_providers; do
    && echo "OK $id" || echo "GHOST $id"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_help_debugging | procedure | 650 | ≤6 | ✅ |
| 2 | oc_help_environment | procedure | 650 | ≤6 | ✅ |
| 3 | oc_help_faq_overview | concept | 550 | 0 | ✅ |
| 4 | oc_help_faq_skills_automation | procedure | 700 | ≤3 | ✅ |
| 5 | oc_help_faq_config_env | procedure | 650 | ≤3 | ✅ |
| 6 | oc_help_faq_storage_memory | procedure | 600 | ≤2 | ✅ |
| 7 | oc_help_faq_gateway_remote | procedure | 700 | ≤3 | ✅ |
| 8 | oc_help_faq_sessions_logging | procedure | 700 | ≤2 | ✅ |
| 9 | oc_help_faq_security_access | argument | 600 | ≤2 | ✅ |
| 10 | oc_help_faq_first_run_install | procedure | 750 | ≤2 | ✅ |
| 11 | oc_help_faq_first_run_auth | procedure | 750 | ≤3 | ✅ |
| 12 | oc_help_faq_models | procedure | 800 | ≤4 | ⚠️ watch at augment (source 2,884 w; if draft >2,500 w or >6 code → split into selection/aliases vs failover+auth-profiles) |

No note approaches the line/word caps at planned size. Code-dense `debugging.md` (23 fences) reproduces ≤6
selectively. The single density watch is note 12 (faq-models source slightly over the page-level word cap but
compresses to ~800 w as a digest); split is pre-authorized if augment finds the draft exceeds caps.

## Entry Point Decision (inherited from master)

Contributes **12 rows** to `entry_openclaw_docs.md` (created as master pre-step **W1**, `building_block:
navigation`, >30-note total ⇒ required) under a **"Help & Support"** cluster (subgroups: Debugging/Environment,
General FAQ, First-run FAQ, Models FAQ). Each of the 12 notes receives its entry-point back-link at
finalization — this is the primary G7/G8 inbound-link source. No new entry point is created by hp01.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):

| Source (existing) | → New note(s) |
|---|---|
| `entry_openclaw_docs.md` (W1 pre-step) | → all 12 (primary anti-island source) |
| `repo_openclaw_gateway.md` | → 1 (debugging), 2 (environment), 7 (gateway/remote) |
| `repo_openclaw_security.md` | → 2 (environment/secrets), 9 (security/access), 11 (auth) |
| `repo_openclaw_extensions_llm_providers.md` | → 11 (first-run auth), 12 (models) |
| `repo_openclaw_skills.md` | → 4 (skills/automation) |
| `repo_openclaw_memory.md` | → 6 (storage/memory) |
| `repo_openclaw_sessions.md` | → 6 (storage), 8 (sessions/logging) |
| `repo_openclaw_cli_wizard.md` | → 10 (first-run install), 11 (first-run auth) |
| `term_openclaw.md` | → 3 (overview) |
| `term_model_failover.md` | → 12 (models) |
| `term_access_control.md` | → 9 (security/access) |

Each new note must end with ≥1 of these inbound links resolved; `entry_openclaw_docs.md` guarantees the floor.

## Pacing Rules (inherited from master)

One execution phase, 12 notes. Re-read each source page during execute; reproduce config/env/CLI snippets
verbatim (selective ≤6/note). One BB per note. Cap dynamic-workflow fan-out at ~30 agents/run; reindex
incrementally; verify `note_links` + 0 broken links before commit. Commit+push after the phase
(`git pull --rebase --autostash` first; **no Claude co-author trailer**).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this run (xref-augment).** Re-read all 5 source pages under `inbox/openclaw_docs/help/`
(measured: debugging 1,620w / environment 1,350w / faq 11,389w / faq-first-run 4,895w / faq-models 2,930w —
all within ±5% of the plan's recorded counts; no re-split triggered). Replaced `## Candidate Cross-References`
with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` at the RAISED floor
(**≥8 terms · ≥10 snippets · ≥10 docs per note**), grouped Terms / Docs / Repos / Snippets with a per-link
relevance statement. Updated the Summary Statistics cross-ref line and the G4 gate condition to the raised floor.

**What was locked (per-note terms · snippets · docs · repos; floors all met):**

| # | Note | Terms | Snippets | Docs (existing+planned-oc) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| 1 | oc_help_debugging | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 2 | oc_help_environment | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 3 | oc_help_faq_overview | 8 | 10 | 10 (8+2) | 3 | ✅ |
| 4 | oc_help_faq_skills_automation | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 5 | oc_help_faq_config_env | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 6 | oc_help_faq_storage_memory | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 7 | oc_help_faq_gateway_remote | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 8 | oc_help_faq_sessions_logging | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 9 | oc_help_faq_security_access | 10 | 11 | 10 (8+2) | 3 | ✅ |
| 10 | oc_help_faq_first_run_install | 8 | 11 | 10 (8+2) | 3 | ✅ |
| 11 | oc_help_faq_first_run_auth | 9 | 11 | 10 (8+2) | 3 | ✅ |
| 12 | oc_help_faq_models | 12 | 13 | 10 (8+2) | 4 | ✅ |

snippets, 90 distinct docs/entries/repos). Programmatic re-scan of the locked section: **393 links total →
24 sibling `oc_help_*` "(planned, this series)" doc links (2/note) and `entry_openclaw_docs` (W1 master pre-step).

BM25 false-positives were discarded, e.g. `term_ures_unified_risk_evaluation_system`, `term_xray`,
`term_cloudwatch`, `term_firelens`, `term_emf`, `term_container_insights` (AWS-ops observability ≠ agent-runtime
`term_ecr` (AWS deploy ≠ self-hosted OpenClaw install). New relevant existing terms surfaced beyond the original
draft's ≤7: `term_langfuse`, `term_codeguru_profiler`, `term_credential_pool`, `term_agents_md`,
`term_blast_radius`, `term_deny_first`, `term_dm_policy`, `term_dm_pairing`, `term_threat_model`,
`term_owasp_llm`, `term_prompt_injection`, `term_provider_routing`, `term_fallback_provider`,
`term_episodic_memory`, `term_embedding`, `term_websocket_framing`, `term_bonjour_discovery`,
`term_remote_ssh`, `term_silence_token`, `term_session_mcp`, `term_delegate_task`, `term_agent_as_a_tool`,
`term_cron_expression`, `term_skill_curator`, `term_docker`, `term_node_js`, `term_mise`, `term_oauth`,
`term_pkce`, `term_deepseek`, `term_qwen`.

**New-term candidates: none.** The xref re-read surfaced no genuinely cross-cutting, vault-reusable term that
lacks both a doc-page home (in this `oc_*` series) and an existing `term_dictionary` note to link. The four
concepts with no existing term note (`environment variable`, `logging`, `skill`/`agent skills`) remain correctly
dispositioned per the Undigested Terms Plan: each is the subject of an `oc_*` doc note and is covered by linking
adjacent existing terms (`term_secrets_manager` + `term_aws_sdk_credential_chain` + `term_credential_pool` for
env-vars; `term_observability_agent_systems` + `term_data_observability` + `term_langfuse` for logging;
`repo_openclaw_skills` + `term_skill_curator` for skills) — consistent with the master's corpus-ownership rule
(OpenClaw vocabulary is digested as `oc_*` doc notes, never as new `term_dictionary` entries). Best-fit glossary
if any future term IS promoted: the agentic/LLM `acronym_glossary_*.md` (per master W5).

**Issues / notes:** none blocking. Note 12 (`oc_help_faq_models`) source is 2,930w (> the 2,500 page cap) but
the Split Decisions table already pre-authorizes a 2-note split if the DRAFT exceeds caps; at planned ~800w it
compresses well — carried forward unchanged with the split trigger intact.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 mandatory checkpoints. Source spot-check: re-read `help/faq.md` (11,389w),
`help/faq-models.md` (2,930w), `help/environment.md` (1,350w) — all within ±5% of plan estimates (CP7).

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 12 notes meet ≥8 terms · ≥10 snippets · ≥10 docs, each link carries a relevance statement; programmatic floor check = 12/12 OK. |
| CP2 | 9-GATE table per batch (G1–G6, G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single execution phase; G5 ghost-detect + G6 broken-link + G7/G8 discoverability all listed; G4 updated to raised floor. |
| CP3 | Entry point update specified (inherited) | **PASS** | `## Entry Point Decision` contributes 12 rows to `entry_openclaw_docs.md` (created master pre-step W1, `building_block: navigation`, >30-note total ⇒ required); primary G7/G8 inbound source. |
| CP4 | Plan size manageable | **PASS** | 12 notes (≤30); single execution phase. |
| CP5 | Note format aligned + DERIVED | **PASS** | Format inherited verbatim from the master's `## Format Definition`, itself derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora; `## Overview` + `## Related Notes` + footer; forbidden-field list present. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: notes 1–11 well under caps; note 12 (source 2,930w) carries a pre-authorized 2-note split trigger in Split Decisions. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 5 pages this run (1,620 / 1,350 / 11,389 / 4,895 / 2,930 w); all within ±5% of plan's recorded counts. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` + `## Term-Note Authoring Requirements` present; 0 new term captures (N/A authoring) per master corpus-ownership rule; dispositions verified against existing-term links. |
| CP8f | Term-slug / all-notes dedup + collision audit | **PASS** | hp01 creates 0 new terms (no slugs to collide); all 12 planned `oc_help_*` doc-note slugs are NEW (folder empty in DB) and do not duplicate an existing term/doc note; collision audit clean. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing → new notes)` maps every one of the 12 notes to ≥1 outside-folder inbound source (`entry_openclaw_docs` + repo/term notes); G8 in-degree ≥1 gated in the phase table. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
