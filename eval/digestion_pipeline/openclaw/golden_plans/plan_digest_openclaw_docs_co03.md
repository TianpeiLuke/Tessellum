---
title: Sub-Plan co03 — OpenClaw Docs: Concepts (Features, Mantis QA, Markdown Formatting, Memory)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - concepts/features
  - concepts/mantis
  - concepts/mantis-slack-desktop-runbook
  - concepts/markdown-formatting
  - concepts/memory
  - concepts/memory-builtin
  - concepts/memory-honcho
---

# Sub-Plan co03: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, prefix `oc_*`), format (YAML + `## Overview` … `## Related Notes` … `## References` + bold footer), dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), 9-GATE validation, cross-refs, and entry-point wiring are ALL inherited from the master and applied per note below.

## Scope

The seven Concepts pages in this slice cover two distinct conceptual clusters plus a capabilities index:

1. **Capabilities index** — `features.md` (the one-page "what OpenClaw supports" surface across channels, agent, providers, media, apps, tools).
2. **Live visual QA (Mantis)** — `mantis.md` (the end-to-end before/after verification system: goals, ownership, the full CLI command surface across Discord/Slack/Telegram desktop lanes, run lifecycle, evidence schema, machines/secrets) and its operator companion `mantis-slack-desktop-runbook.md` (the Slack-desktop GitHub-dispatch + local-CLI + warm-lease + hydrate-mode + timing operator runbook).
3. **Outbound formatting** — `markdown-formatting.md` (the shared IR → per-channel render/chunk pipeline for Slack/Telegram/Signal).
4. **Memory** — `memory.md` (the workspace-Markdown memory model: `MEMORY.md`/daily notes/`DREAMS.md`, action-sensitive memories, tools, search, backends, dreaming, flush), `memory-builtin.md` (the default SQLite + FTS5/vector/hybrid backend with embedding-provider setup), and `memory-honcho.md` (the AI-native cross-session memory plugin).

**Priority: P1 (Phase A — conceptual core).** Memory and markdown-formatting define vocabulary the CLI (`cli/memory`), reference (`reference/memory-config`), and channels (`channels/slack`) docs reference; Mantis defines the QA vocabulary referenced by `help/testing` and `concepts/qa-e2e-automation`. The code-side counterparts (`repo_openclaw_memory`, `repo_openclaw_channels_messaging`) are LINKED, not recreated.

**Source: 7 pages, 9,691 measured words. Planned: 9 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| features | concepts/features | 449 | 0 | 3 | 0 | concept |
| mantis | concepts/mantis | 4,505 | 15 | 16 | 0 | concept + procedure + model (SPLIT ×3) |
| mantis-slack-desktop-runbook | concepts/mantis-slack-desktop-runbook | 1,088 | 8 | 8 | 0 | procedure |
| markdown-formatting | concepts/markdown-formatting | 711 | 3 | 11 | 0 | procedure |
| memory | concepts/memory | 1,604 | 6 | 14 | 0 | concept |
| memory-builtin | concepts/memory-builtin | 674 | 4 | 8 | 0 | procedure |
| memory-honcho | concepts/memory-honcho | 660 | 3 | 10 | 0 | procedure |

Totals: 9,691 words · 39 code fences · 70 H2 · 0 H3.

## Content Strategy

- **Prioritize**: the memory mental model (`MEMORY.md`/daily/`DREAMS.md`, action-sensitive boundaries, tools, dreaming, flush) and the Mantis architecture (before/after-on-live-transport with a deterministic oracle + visual evidence) — these are the load-bearing concepts the rest of the docs reference. Reproduce config/CLI snippets verbatim (selectively, ≤6 per note).
- **Split**: `mantis.md` (4,505 w, 15 code fences, 16 H2, mixed BB) → THREE notes — (a) the architecture/design concept (goals, non-goals, ownership, run lifecycle, browser/VNC, machines, secrets, provider expansion, open questions), (b) the CLI/scenario procedure (Command shape, Discord MVP, existing QA pieces, adding a scenario), and (c) the evidence/artifact data model (`mantis-evidence.json` schema, supported artifact kinds, evidence model, PR-comment shape, GitHub artifacts). This satisfies the >2,500-word and mixed-BB SPLIT rules.
- **Keep 1:1** (≤1 note each): `features.md`, `mantis-slack-desktop-runbook.md`, `markdown-formatting.md`, `memory.md`, `memory-builtin.md`, `memory-honcho.md` — each ≤1,604 w and single-BB after the memory-overview-vs-backend separation (overview concept vs builtin/honcho backend procedures is satisfied by the page boundary itself, no intra-page split needed).
- **Link-out (do NOT redefine)**: dreaming detail → `concepts/dreaming` (co02, planned); memory search pipeline → `concepts/memory-search` (co04, planned); QMD backend → `concepts/memory-qmd` (co04, planned); compaction → `concepts/compaction` (co02, planned); commitments → `concepts/commitments` (co02, planned); streaming/chunking → `concepts/streaming` (co07, planned); memory config reference → `reference/memory-config` (rf02, planned); Memory Wiki / LanceDB plugins → `plugins/memory-wiki`/`plugins/memory-lancedb` (pl04/pl14, planned); QA-E2E overview → `concepts/qa-e2e-automation` (co05, planned). Existing vault terms (`term_llm`, `term_claude`, `term_markdown`, `term_bedrock`, `term_honcho`, …) are linked, never redefined inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_features.md` | concept | features.md: Highlights, Full list, Related | 350 | OpenClaw's capability surface at a glance: built-in + bundled-plugin channels, embedded multi-agent runtime, 35+ model providers with subscription/custom auth, media in/out + generation, apps/UI (WebChat, Control UI, macOS app, iOS/Android nodes), and tools/automation (browser, exec, sandbox, web search, cron, skills, Lobster). |
| 2 | `oc_concepts_mantis_architecture.md` | concept | mantis.md: intro, Goals, Non goals, Ownership, Run lifecycle, Browser and VNC, Machines, Secrets, Private deployment notes, Provider expansion, Open questions | 700 | The Mantis live visual-QA system design: reproduce a bug on a real transport against a known-bad baseline, capture before/after evidence with a deterministic oracle plus screenshots, and publish to a PR. Covers the goals/non-goals, the OpenClaw/QA-Lab/Crabbox/GitHub-Actions/ClawSweeper ownership split, the 15-step run lifecycle, headless-vs-VNC browser modes, VM requirements, secret-handling rules, and provider-expansion roadmap. |
| 3 | `oc_concepts_mantis_cli_scenarios.md` | procedure | mantis.md: Command shape, Discord MVP, Existing QA pieces, Adding a scenario | 700 | Running and authoring Mantis scenarios: the `pnpm openclaw qa mantis` command surface (discord-smoke, before/after `run`, desktop-browser-smoke, slack-desktop-smoke with `--gateway-setup`, telegram-desktop-builder), the GitHub workflows and `@openclaw-mantis`/`@clawsweeper` PR-comment triggers, the Discord status-reactions MVP scenario YAML, and the scenario-declaration checklist (id, transport, oracle, captures, cleanup). |
| 4 | `oc_concepts_mantis_evidence_model.md` | model | mantis.md: Evidence model, GitHub artifacts and PR comments, the `mantis-evidence.json` schema + supported artifact kinds + publisher | 600 | The Mantis evidence/artifact data model: the stable `.artifacts/qa-e2e/mantis/<run-id>/` directory layout, the machine-readable `mantis-summary.json` fields, the `mantis-evidence.json` schema (schemaVersion/comparison/artifacts) that hands off scenario code to GitHub comments, the supported artifact kinds (timeline/desktopScreenshot/motionPreview/motionClip/fullVideo/metadata/report), and the reusable PR-evidence publisher + redaction discipline. |
| 5 | `oc_concepts_mantis_slack_desktop_runbook.md` | procedure | mantis-slack-desktop-runbook.md: all 8 H2 (Storage model, GitHub dispatch, Local CLI, Hydrate modes, Timing interpretation, Evidence checklist, Failure handling, Related) | 600 | Operator runbook for the Mantis Slack-desktop QA lane: the three-layer storage model (provider image vs warm lease vs artifacts), GitHub dispatch via `gh workflow run`, the local `pnpm openclaw qa mantis slack-desktop-smoke` invocations (cold source / keep-lease / warm-lease / approval-checkpoints), `source` vs `prehydrated` hydrate modes, phase-timing interpretation, the PR evidence checklist, and failure-handling/VNC-rescue steps. |
| 6 | `oc_concepts_markdown_formatting.md` | procedure | markdown-formatting.md: all 11 H2 (Goals, Pipeline, IR example, Where it is used, Table handling, Chunking rules, Link policy, Spoilers, How to add/update a channel formatter, Common gotchas, Related) | 550 | OpenClaw's outbound-Markdown formatting pipeline: parse Markdown into a shared IR (text + UTF-16 style/link spans), chunk on the IR before rendering, then render per channel (Slack mrkdwn, Telegram HTML, Signal style ranges). Covers table handling (`markdown.tables` code/bullets/off), chunking rules, per-channel link policy, spoilers, the add-a-channel-formatter steps (`markdownToIR`/`renderMarkdownWithMarkers`/`chunkMarkdownIR`), and common gotchas. |
| 7 | `oc_concepts_memory.md` | concept | memory.md: How it works, What goes where, Action-sensitive memories, Inferred commitments, Memory tools, Memory Wiki companion, Memory search, Memory backends, Knowledge wiki layer, Automatic memory flush, Dreaming, Grounded backfill and live promotion, CLI, Further reading, Related | 750 | How OpenClaw remembers across sessions: durable `MEMORY.md` + daily `memory/YYYY-MM-DD.md` + optional `DREAMS.md`, all plain Markdown in the agent workspace. Covers what-goes-where + bootstrap-budget truncation, action-sensitive memories, inferred commitments, the `memory_search`/`memory_get` tools, the four backends (builtin/QMD/Honcho/LanceDB), automatic pre-compaction memory flush, dreaming (opt-in background promotion), and grounded backfill. |
| 8 | `oc_concepts_memory_builtin.md` | procedure | memory-builtin.md: What it provides, Getting started, Supported embedding providers, How indexing works, When to use, Troubleshooting, Configuration, Related | 550 | The default SQLite memory backend: per-agent SQLite with FTS5 keyword (BM25), vector, and hybrid search plus CJK trigram tokenization and optional sqlite-vec. Covers getting started with OpenAI-default or local-GGUF embeddings, the supported embedding-provider table, indexing mechanics (~400-token chunks, debounced reindex, `memory index --force`), when to use vs QMD/Honcho, and troubleshooting (`memory status --deep`). |
| 9 | `oc_concepts_memory_honcho.md` | procedure | memory-honcho.md: What it provides, Available tools, Getting started, Configuration, Migrating existing memory, How it works, Honcho vs builtin memory, CLI commands, Further reading, Related | 500 | The Honcho AI-native cross-session memory plugin: conversations persisted to a dedicated (local or hosted) service that builds user/agent models, with semantic search and parent/child multi-agent awareness. Covers the registered tools (`honcho_context`/`honcho_search_*`/`honcho_session`/`honcho_ask`), plugin install + `openclaw honcho setup`, config under `plugins.entries`, non-destructive migration, the `before_prompt_build` injection, and the Honcho-vs-builtin comparison. |

## Section Coverage Map

```
features.md
├── Highlights (Columns cards) ─────────────────────────── → note 1 (oc_concepts_features)
├── Full list (Channels/Agent/Auth/Media/Apps/Tools) ───── → note 1
└── Related ───────────────────────────────────────────── → note 1 (links → notes 2-9 + co02 dreaming/experimental)

mantis.md
├── intro (live e2e verification, Discord-first) ───────── → note 2 (oc_concepts_mantis_architecture)
├── Goals ─────────────────────────────────────────────── → note 2
├── Non goals ─────────────────────────────────────────── → note 2
├── Ownership ─────────────────────────────────────────── → note 2
├── Command shape (CLI surface, GH workflows, triggers) ── → note 3 (oc_concepts_mantis_cli_scenarios)
├── Run lifecycle (15 steps + two failure modes) ──────── → note 2
├── Discord MVP (seed scenario + YAML + qa discord cmd) ── → note 3
├── Existing QA pieces ────────────────────────────────── → note 3
├── Evidence model (artifact dir + summary fields) ─────── → note 4 (oc_concepts_mantis_evidence_model)
├── Browser and VNC ───────────────────────────────────── → note 2
├── Machines (VM requirements) ────────────────────────── → note 2
├── Secrets (secret names + redaction rules) ──────────── → note 2
├── GitHub artifacts and PR comments (publisher + comment) → note 4
├── Private deployment notes ──────────────────────────── → note 2
├── Adding a scenario (declaration checklist + oracles) ── → note 3
├── Provider expansion ────────────────────────────────── → note 2
├── Open questions ────────────────────────────────────── → note 2
└── mantis-evidence.json schema + artifact kinds (in Command shape body) → note 4

mantis-slack-desktop-runbook.md
├── (intro) ───────────────────────────────────────────── → note 5 (oc_concepts_mantis_slack_desktop_runbook)
├── Storage model ─────────────────────────────────────── → note 5
├── GitHub dispatch ───────────────────────────────────── → note 5
├── Local CLI ─────────────────────────────────────────── → note 5
├── Hydrate modes ─────────────────────────────────────── → note 5
├── Timing interpretation ─────────────────────────────── → note 5
├── Evidence checklist ────────────────────────────────── → note 5
├── Failure handling ──────────────────────────────────── → note 5
└── Related ───────────────────────────────────────────── → note 5

markdown-formatting.md
├── (intro IR description) ────────────────────────────── → note 6 (oc_concepts_markdown_formatting)
├── Goals / Pipeline / IR example ─────────────────────── → note 6
├── Where it is used / Table handling / Chunking rules ─── → note 6
├── Link policy / Spoilers ────────────────────────────── → note 6
├── How to add or update a channel formatter ──────────── → note 6
├── Common gotchas / Related ──────────────────────────── → note 6

memory.md
├── (intro) / How it works / What goes where ──────────── → note 7 (oc_concepts_memory)
├── Action-sensitive memories / Inferred commitments ──── → note 7
├── Memory tools / Memory Wiki companion plugin ───────── → note 7
├── Memory search / Memory backends / Knowledge wiki ──── → note 7
├── Automatic memory flush / Dreaming ─────────────────── → note 7
├── Grounded backfill and live promotion / CLI ────────── → note 7
└── Further reading / Related ─────────────────────────── → note 7

memory-builtin.md
├── (intro) / What it provides / Getting started ──────── → note 8 (oc_concepts_memory_builtin)
├── Supported embedding providers / How indexing works ── → note 8
├── When to use / Troubleshooting / Configuration ─────── → note 8
└── Related ───────────────────────────────────────────── → note 8

memory-honcho.md
├── (intro) / What it provides / Available tools ──────── → note 9 (oc_concepts_memory_honcho)
├── Getting started / Configuration / Migrating ───────── → note 9
├── How it works / Honcho vs builtin memory ───────────── → note 9
├── CLI commands / Further reading / Related ──────────── → note 9
```
No orphaned sections. Detail-only sections delegated to other sub-plans (dreaming, memory-search, QMD, compaction, commitments, streaming, qa-e2e-automation, memory-config, plugin pages) are LINKED from notes 2-9, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `mantis.md` (4,505 w, 15 code fences, 16 H2, mixed BB) | notes 2 + 3 + 4 | Far exceeds the 2,500-word cap AND mixes three building blocks: an architecture/design **concept** (goals/ownership/lifecycle/machines/secrets), an operational **procedure** (CLI commands, scenario authoring, Discord MVP), and a structured **model** (the `mantis-evidence.json` schema + artifact-kinds taxonomy + evidence directory). Split per word-cap + mixed-BB + one-BB-per-note rules; the 15 code fences distribute so each note stays ≤6. |
| `features`, `mantis-slack-desktop-runbook`, `markdown-formatting`, `memory`, `memory-builtin`, `memory-honcho` | 1 note each | All ≤1,604 w with ≤8 code fences and a single coherent BB; no intra-page split needed. (Memory overview vs the two backend pages are already separate source pages → separate single-BB notes.) |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (9,691 measured words, 39 code fences, 70 H2). New `oc_*` notes: **9**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×3** (notes 1, 2, 7) · **procedure ×4** (notes 3, 5, 6, 8, 9 → procedure count = 5) · **model ×1** (note 4). Final tally: concept 3, procedure 5, model 1.
- Estimated digest words ≈ 5,300 (avg ~590/note). The 39 source code fences distribute across the procedure/model notes; each note kept ≤6 (Mantis split keeps the code-heavy `mantis.md` fences spread; memory/markdown snippets reproduced selectively, verbatim).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_concepts_features (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to AI coding agents; relevance: this note IS OpenClaw's capability index, so the product hub term anchors it.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that plan and execute coding tasks with minimal supervision; relevance: the embedded agent runtime feature is exactly an autonomous coding agent surface.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the runtime wrapper that drives an LLM agent loop with tools; relevance: "embedded agent runtime with tool streaming" is the harness the features page lists.
- [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — coordination of multiple agents with isolated state; relevance: the page's "multi-agent routing with isolated sessions" highlight.
- [term_chatbot](../../term_dictionary/term_chatbot.md) — conversational agent on a messaging channel; relevance: the Channels capability (Discord/Slack/Telegram/WhatsApp) is the chatbot surface.
- [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) — single gateway fronting many chat platforms; relevance: "all channels with a single Gateway" is the core features claim.
- [term_voice_bot](../../term_dictionary/term_voice_bot.md) — voice-interface conversational agent; relevance: the Media section's voice-note transcription + TTS + voice nodes capabilities.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control as an agent tool; relevance: listed first under Tools and automation.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — handling images/audio/video alongside text; relevance: the Media in/out + generation capability surface.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: the tools/exec/web-search/skills surface is implemented via function calling.

**Docs**
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes (OpenClaw fork) capability overview; relevance: direct sibling-product feature index, the closest existing analogue to this note.
- [hermes_integrations_overview](../hermes_agent/hermes_integrations_overview.md) — Hermes channels/providers/tools integration map; relevance: mirrors the channels/providers/media/tools grouping of this page.
- [hermes_tool_gateway](../hermes_agent/hermes_tool_gateway.md) — the tool-gateway runtime that exposes agent tools; relevance: backs the "tools and automation" capability cluster.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform + media tool reference; relevance: the media-in/out + generation capability surfaces.
- [hermes_nous_portal_subscription](../hermes_agent/hermes_nous_portal_subscription.md) — subscription/OAuth provider auth; relevance: the "subscription auth via OAuth" provider capability.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — Claude Code channel connectors setup; relevance: parallels the Channels capability list.
- [cc_computer_use](../claude_code/cc_computer_use.md) — agentic computer/browser use; relevance: maps to the browser-automation tool capability.
- [pi_quickstart](../pi/pi_quickstart.md) — Pi coding-agent quickstart and capability surface; relevance: peer coding-agent product for the capabilities-index framing.
- [oc_concepts_memory](oc_concepts_memory.md) (planned, this series) — OpenClaw memory model; relevance: the agent runtime's memory capability detailed here.
- [oc_concepts_mantis_architecture](oc_concepts_mantis_architecture.md) (planned, this series) — OpenClaw live-QA system; relevance: the QA/tooling capability the features page links onward to.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo root; relevance: the codebase behind every listed capability.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — built-in channel adapters; relevance: implements the Channels capability list.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — WebChat/Control-UI/macOS/mobile apps; relevance: the Apps and interfaces capability cluster.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter interface contract; relevance: the single-gateway many-channels feature in code.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel→agent binding/routing; relevance: the multi-agent routing highlight in code.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord gateway intents; relevance: the Discord built-in channel capability.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack Socket Mode connect; relevance: the Slack built-in channel capability.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime configuration; relevance: the embedded agent runtime feature.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn policy; relevance: the multi-agent routing / isolated sessions capability.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — multi-provider aggregation; relevance: the "35+ model providers" capability.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: the auth-and-providers capability cluster.
- [snippet_hermes_agent_gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — cron/heartbeat scheduler; relevance: the "cron jobs and heartbeat scheduling" automation capability.
- [snippet_hermes_agent_skills_hermes_agent](../../code_snippets/snippet_hermes_agent_skills_hermes_agent.md) — skills runtime; relevance: the "skills, plugins, and workflow pipelines" automation capability.

### oc_concepts_mantis_architecture (10t · 10s · 11d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway/agent product; relevance: Mantis is OpenClaw's QA stack, so the product term anchors the architecture note.
- [term_canary_testing](../../term_dictionary/term_canary_testing.md) — pre-release verification against a candidate vs known-good baseline; relevance: Mantis's before/after baseline-vs-candidate comparison is canary-style verification.
- [term_qa](../../term_dictionary/term_qa.md) — quality-assurance practice; relevance: Mantis lives in the OpenClaw QA stack and owns the QA evidence schema.
- [term_test_plan](../../term_dictionary/term_test_plan.md) — structured plan of test scenarios + oracles; relevance: the Goals/Non-goals/scenario-declaration framing is a test plan for live transports.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the Browser-and-VNC section (headless CDP capture) is core to the architecture.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: Crabbox warmed Linux VMs are the isolated machine sandbox Mantis runs in.
- [term_slack](../../term_dictionary/term_slack.md) — Slack messaging platform; relevance: a primary live transport Mantis targets after Discord.
- [term_chatbot](../../term_dictionary/term_chatbot.md) — conversational bot on a channel; relevance: the bot-auth/driver-SUT-bot live transport shape Mantis reproduces.
- [term_ci_cd](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: Mantis is the GitHub-Actions-driven (but slower-than-CI) verification lane.
- [term_cdp](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: the VM requires CDP access for browser automation.

**Docs**
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — browser automation backend choices; relevance: the headless-vs-VNC browser mode design.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — browser-process supervision/recovery; relevance: VNC-rescue and stuck-state handling parallels.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome automation for an agent; relevance: the desktop Chrome + CDP capture model.
- [cc_verification_loop](../claude_code/cc_verification_loop.md) — agentic verify-the-fix loop; relevance: Mantis's reproduce-on-baseline / verify-on-candidate is the same loop.
- [cc_computer_use](../claude_code/cc_computer_use.md) — agent computer/browser use; relevance: the agent-driven (Codex) Mantis setup/debug path.
- [band_testing_agents](../band/band_testing_agents.md) — testing AI agents end-to-end; relevance: peer framing of live agent e2e verification.
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — gateway session lifecycle; relevance: the run-lifecycle child-gateway start/stop steps.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway transport architecture; relevance: the live-transport-shape reproduction the architecture targets.
- [oc_concepts_mantis_cli_scenarios](oc_concepts_mantis_cli_scenarios.md) (planned, this series) — Mantis CLI/scenario procedure; relevance: the operational companion to this architecture.
- [oc_concepts_mantis_evidence_model](oc_concepts_mantis_evidence_model.md) (planned, this series) — Mantis evidence schema; relevance: the data model produced by this architecture.
- [oc_concepts_mantis_slack_desktop_runbook](oc_concepts_mantis_slack_desktop_runbook.md) (planned, this series) — Slack-desktop operator runbook; relevance: a concrete lane of this architecture.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: hosts the Mantis scenario runtime + local CLI.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway daemon; relevance: the child OpenClaw Gateway Mantis starts per run.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel transport adapters; relevance: the transport adapters Mantis verifies.

**Snippets**
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session manager; relevance: the persistent observer browser profile model.
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — CDP connection; relevance: the CDP-enabled headless automation mode.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: the visual-evidence capture path.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — browser supervisor lifecycle; relevance: VM browser launch/teardown in the run lifecycle.
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — browser crash recovery; relevance: the VNC-rescue / stuck-state recovery design.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — gateway startup/prewarm; relevance: the run-lifecycle child-gateway start step.
- [snippet_hermes_agent_gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — session lifecycle; relevance: baseline/candidate gateway start-and-stop ordering.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config; relevance: configuring provider/model/transport per scenario.
- [snippet_hermes_agent_cli_worktree_isolation](../../code_snippets/snippet_hermes_agent_cli_worktree_isolation.md) — git worktree isolation; relevance: detached baseline/candidate worktrees per run.

### oc_concepts_mantis_cli_scenarios (10t · 11s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product/CLI; relevance: every command here is `pnpm openclaw qa mantis ...`.
- [term_canary_testing](../../term_dictionary/term_canary_testing.md) — baseline-vs-candidate verification; relevance: the `run --baseline --candidate` before/after invocation.
- [term_test_on_demand](../../term_dictionary/term_test_on_demand.md) — operator-triggered ad-hoc test runs; relevance: PR-comment / `gh workflow run` on-demand scenario dispatch.
- [term_qa](../../term_dictionary/term_qa.md) — quality assurance; relevance: the `qa mantis` / `qa discord` QA command surface.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — browser control; relevance: desktop-browser-smoke / VNC browser captures.
- [term_slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: the slack-desktop-smoke scenario with `--gateway-setup`.
- [term_test_plan](../../term_dictionary/term_test_plan.md) — scenario declaration spec; relevance: the id/transport/oracle/captures/cleanup scenario checklist (Adding a scenario).
- [term_cron](../../term_dictionary/term_cron.md) — scheduled job triggers; relevance: GitHub workflow + ClawSweeper dispatch automation.
- [term_chatbot](../../term_dictionary/term_chatbot.md) — channel bot; relevance: driver-bot / SUT-bot Discord scenario shape.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — shared credential broker (Convex); relevance: `--credential-source convex` scenario auth.

**Docs**
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser automation setup; relevance: the desktop/browser smoke command prerequisites.
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — headless agent CLI mode; relevance: the non-interactive CLI invocation shape.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome automation; relevance: the visible-browser desktop smoke captures.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — channel command triggers; relevance: `@openclaw-mantis` / `@clawsweeper` PR-comment commands.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram bot setup; relevance: the telegram-desktop-builder / telegram-live scenarios.
- [cc_verification_loop](../claude_code/cc_verification_loop.md) — verify-the-fix loop; relevance: the run/compare workflow each scenario drives.
- [band_testing_agents](../band/band_testing_agents.md) — agent test authoring; relevance: the add-a-scenario declaration discipline.
- [oc_concepts_mantis_architecture](oc_concepts_mantis_architecture.md) (planned, this series) — Mantis system design; relevance: the architecture these commands operate.
- [oc_concepts_mantis_evidence_model](oc_concepts_mantis_evidence_model.md) (planned, this series) — evidence schema; relevance: artifacts these scenarios emit.
- [oc_concepts_mantis_slack_desktop_runbook](oc_concepts_mantis_slack_desktop_runbook.md) (planned, this series) — the Slack-desktop operator runbook; relevance: deep-dive of the slack-desktop-smoke command.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: hosts the `qa mantis` CLI surface.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel transports; relevance: Discord/Slack/Telegram scenario transports.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway daemon; relevance: the `openclaw gateway run` started by `--gateway-setup`.

**Snippets**
- [snippet_hermes_agent_cli_main_entry_point](../../code_snippets/snippet_hermes_agent_cli_main_entry_point.md) — CLI entry point; relevance: how `pnpm openclaw qa ...` subcommands dispatch.
- [snippet_hermes_agent_cli_main_argparse_root](../../code_snippets/snippet_hermes_agent_cli_main_argparse_root.md) — root arg parsing; relevance: the rich flag surface (`--transport`/`--scenario`/`--baseline`).
- [snippet_hermes_agent_cli_worktree_isolation](../../code_snippets/snippet_hermes_agent_cli_worktree_isolation.md) — worktree isolation; relevance: detached baseline/candidate worktrees the runner creates.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session; relevance: the visible-browser desktop-browser-smoke.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — navigate to URL; relevance: `--browser-url` / `--slack-url` opening pages.
- [snippet_hermes_agent_gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — scheduled runner; relevance: GitHub-workflow dispatched runs.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — job handoff; relevance: PR-comment trigger → workflow dispatch handoff.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: the Discord status-reactions MVP scenario.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack Socket Mode; relevance: `--gateway-setup` patches Slack Socket Mode config.

### oc_concepts_mantis_evidence_model (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the `mantis-evidence.json` schema is OpenClaw-owned.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — JSON message contracts; relevance: the schema is a JSON handoff between scenario code and GitHub comments.
- [term_event_ledger](../../term_dictionary/term_event_ledger.md) — append-only structured record of events; relevance: `mantis-summary.json` is the machine-readable source-of-truth ledger of a run.
- [term_qa](../../term_dictionary/term_qa.md) — quality assurance; relevance: the evidence artifacts are the QA proof bundle.
- [term_test_plan](../../term_dictionary/term_test_plan.md) — declared expected oracles + captures; relevance: the schema's comparison/expected fields encode the test plan outcome.
- [term_markdown](../../term_dictionary/term_markdown.md) — Markdown output; relevance: `mantis-report.md` + the Markdown PR-comment shape.
- [term_canary_testing](../../term_dictionary/term_canary_testing.md) — baseline/candidate comparison; relevance: the schema's `comparison.baseline`/`comparison.candidate` pass field.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — browser-captured media; relevance: desktopScreenshot/motionPreview/fullVideo artifact kinds.
- [term_computer_vision](../../term_dictionary/term_computer_vision.md) — visual evidence interpretation; relevance: the screenshot/timeline visual-proof artifact kinds.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — credential source field; relevance: the summary records "credential source without secret values."

**Docs**
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — structured RPC/JSON protocol; relevance: the typed-schema handoff modeled like an RPC contract.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — browser capture supervision; relevance: how desktopScreenshot/video artifacts are produced.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome capture; relevance: the screenshot/timeline artifact sources.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media artifact handling/redaction; relevance: redaction discipline for screenshots/metadata.
- [cc_verification_loop](../claude_code/cc_verification_loop.md) — verify-result reporting; relevance: the pass/fail comparison the evidence encodes.
- [band_human_api_messages_memories](../band/band_human_api_messages_memories.md) — structured message/artifact API; relevance: peer framing of a typed evidence object.
- [hermes_webhooks_routing_delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — delivery/publish routing; relevance: the reusable PR-evidence publisher upserts the comment.
- [oc_concepts_mantis_architecture](oc_concepts_mantis_architecture.md) (planned, this series) — Mantis design; relevance: the system that emits this evidence.
- [oc_concepts_mantis_cli_scenarios](oc_concepts_mantis_cli_scenarios.md) (planned, this series) — scenario authoring; relevance: scenario code writes `mantis-evidence.json`.
- [oc_concepts_mantis_slack_desktop_runbook](oc_concepts_mantis_slack_desktop_runbook.md) (planned, this series) — Slack-desktop lane; relevance: produces the same evidence artifacts.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: owns the evidence schema + publisher script.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/redaction code; relevance: the secret-free / path-traversal-rejecting publisher discipline.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: per-transport evidence (timeline screenshots) originate in channel code.

**Snippets**
- [snippet_hermes_agent_core_hermes_state_schema](../../code_snippets/snippet_hermes_agent_core_hermes_state_schema.md) — typed state schema; relevance: the schemaVersion'd typed evidence object.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — config schema validation; relevance: typed/validated artifact-manifest fields.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot artifact; relevance: the timeline/desktopScreenshot artifact kinds.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — attaching media to a message; relevance: inline media attached to the PR comment.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — outbound delivery; relevance: the publisher delivering the upserted PR comment.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — webhook publish; relevance: GitHub-Actions artifact upload + comment publish.
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — attachment evidence; relevance: the thread-reply attachment artifact proof.

### oc_concepts_mantis_slack_desktop_runbook (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product/CLI; relevance: the runbook drives `pnpm openclaw qa mantis slack-desktop-smoke`.
- [term_slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: the whole runbook is the Slack-desktop QA lane.
- [term_socket_mode](../../term_dictionary/term_socket_mode.md) — Slack Socket Mode connection; relevance: `--gateway-setup` patches Slack Socket Mode config for the channel.
- [term_canary_testing](../../term_dictionary/term_canary_testing.md) — candidate-ref verification; relevance: `candidate_ref` cold-source proof against a trusted ref.
- [term_test_on_demand](../../term_dictionary/term_test_on_demand.md) — operator-triggered runs; relevance: `gh workflow run` dispatch + local CLI invocations.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — browser control; relevance: Slack Web opened in the VNC browser for capture.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolated VM; relevance: the Crabbox warm-lease Linux desktop and its storage layers.
- [term_qa](../../term_dictionary/term_qa.md) — quality assurance; relevance: the real-UI lane for Slack-class bug proof.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — Convex credential broker; relevance: `--credential-source convex --credential-role maintainer`.
- [term_mttr](../../term_dictionary/term_mttr.md) — time-to-recover diagnosis; relevance: the phase-timing interpretation + failure-handling triage.

**Docs**
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser setup; relevance: the VNC-browser Slack Web capture prerequisites.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — browser supervision/recovery; relevance: VNC rescue and chrome.log failure triage.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome automation; relevance: the Slack Web screenshot/video capture.
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — Slack channel config; relevance: channel allowlist / bot+app token setup for gateway-setup.
- [cc_verification_loop](../claude_code/cc_verification_loop.md) — verify-result reporting; relevance: the evidence-checklist pass/fail PR comment.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — desktop UI capture; relevance: the desktop-UI proof discipline.
- [band_testing_agents](../band/band_testing_agents.md) — agent test runs; relevance: the operator runbook framing of a live test lane.
- [oc_concepts_mantis_architecture](oc_concepts_mantis_architecture.md) (planned, this series) — Mantis design; relevance: the storage model + machine ownership this runbook operates.
- [oc_concepts_mantis_cli_scenarios](oc_concepts_mantis_cli_scenarios.md) (planned, this series) — the slack-desktop-smoke command surface; relevance: the CLI flags this runbook invokes.
- [oc_concepts_mantis_evidence_model](oc_concepts_mantis_evidence_model.md) (planned, this series) — evidence schema; relevance: the artifacts (png/mp4/gif/summary) the runbook checklist verifies.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: hosts the slack-desktop-smoke CLI + workflow.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Slack messaging transport; relevance: the Slack QA lane under test.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway daemon; relevance: the `openclaw gateway run` started inside the VM.

**Snippets**
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack Socket Mode; relevance: `--gateway-setup` Socket Mode patch for the channel.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack platform adapter; relevance: the SUT Slack gateway started in the VM.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session/profile; relevance: the persistent logged-in Slack Web Chrome profile on a warm lease.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: `slack-desktop-smoke.png` capture.
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — browser recovery; relevance: VNC-rescue repair of expired Slack login.
- [snippet_hermes_agent_cli_worktree_isolation](../../code_snippets/snippet_hermes_agent_cli_worktree_isolation.md) — worktree isolation; relevance: the candidate-ref checkout prepared before the VM run.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — gateway startup; relevance: the `crabbox.remote_run` gateway-startup timing phase.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — job dispatch handoff; relevance: `gh workflow run` GitHub-dispatch handoff.
- [snippet_hermes_agent_gw_runner_init](../../code_snippets/snippet_hermes_agent_gw_runner_init.md) — gateway runner init; relevance: the disposable OpenClaw home + gateway boot in the VM.

### oc_concepts_markdown_formatting (10t · 10s · 10d)

**Terms**
- [term_markdown](../../term_dictionary/term_markdown.md) — Markdown markup language; relevance: this note IS the outbound-Markdown formatting pipeline.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the IR→render pipeline is OpenClaw's outbound adapter behavior.
- [term_slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: the Slack mrkdwn renderer + `<url|label>` link policy.
- [term_block_kit](../../term_dictionary/term_block_kit.md) — Slack rich-message blocks; relevance: Slack-specific outbound rendering target.
- [term_chatbot](../../term_dictionary/term_chatbot.md) — channel bot output; relevance: outbound formatting is what the bot sends to a channel.
- [term_channel_kernel](../../term_dictionary/term_channel_kernel.md) — per-channel adapter abstraction; relevance: per-channel renderer/chunker wiring (the add-a-formatter steps).
- [term_tokenization](../../term_dictionary/term_tokenization.md) — splitting text into units (UTF-16 offsets); relevance: UTF-16 code-unit offsets + IR text chunking.
- [term_context_window](../../term_dictionary/term_context_window.md) — output length budget; relevance: chunk limits applied to the IR before rendering.
- [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway fronting channels; relevance: the shared parse-once / multi-render pipeline lives in the gateway.
- [term_silence_token](../../term_dictionary/term_silence_token.md) — control marker in outbound text; relevance: preserved-token handling (Slack `<@U123>`/`<#C123>` angle-bracket tokens).

**Docs**
- [hermes_guide_pipe_script_output](../hermes_agent/hermes_guide_pipe_script_output.md) — formatting script output for channels; relevance: the outbound-rendering-per-channel concern.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway transport architecture; relevance: where the shared IR + per-channel renderers sit.
- [hermes_adding_platform_adapter_builtin](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — adding a built-in channel adapter; relevance: the "how to add/update a channel formatter" steps.
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — adding a plugin channel adapter; relevance: wiring a new renderer/chunker into an adapter.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram channel; relevance: the Telegram HTML renderer (`<b>`/`<a href>`).
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — per-channel message settings; relevance: per-channel/per-account `markdown.tables` config.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel connectors; relevance: the multi-channel outbound target set.
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — Slack config; relevance: the Slack mrkdwn outbound formatting target.
- [oc_concepts_features](oc_concepts_features.md) (planned, this series) — capability index; relevance: "streaming and chunking for long responses" capability.
- [oc_concepts_memory](oc_concepts_memory.md) (planned, this series) — memory model; relevance: shared workspace/system-prompt content also flows through outbound rendering.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel adapters; relevance: hosts the Slack/Telegram/Signal outbound renderers.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: the shared IR/chunk/render pipeline base.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the `markdownToIR`/`renderMarkdownWithMarkers`/`chunkMarkdownIR` helpers.

**Snippets**
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound message formatting; relevance: the parse→IR→render formatting step.
- [snippet_hermes_agent_gw_platform_telegram_markdown](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_markdown.md) — Telegram HTML markdown render; relevance: the Telegram HTML renderer target.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound runner; relevance: the per-channel render-each-chunk dispatch.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — stream chunk consumer; relevance: chunk-the-IR-before-render rule.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — stream backpressure/chunking; relevance: chunk-limit application before rendering.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — channel delivery; relevance: delivering each rendered chunk per channel.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch by channel; relevance: routing the rendered output to the right channel adapter.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the channel-outbound-adapter the new formatter wires into.

### oc_concepts_memory (10t · 10s · 11d)

**Terms**
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — an agent's durable cross-session memory; relevance: this note IS OpenClaw's agent memory model.
- [term_memory_dreaming](../../term_dictionary/term_memory_dreaming.md) — background promotion of short-term to long-term memory; relevance: the Dreaming + grounded-backfill sections.
- [term_episodic_memory](../../term_dictionary/term_episodic_memory.md) — time-stamped event memory; relevance: the daily `memory/YYYY-MM-DD.md` working layer.
- [term_workflow_memory](../../term_dictionary/term_workflow_memory.md) — action/procedure memory; relevance: the action-sensitive memories + inferred commitments.
- [term_memory_information_density](../../term_dictionary/term_memory_information_density.md) — keeping memory high-signal; relevance: `MEMORY.md` is the "compact, curated" layer with bootstrap-budget truncation.
- [term_compaction](../../term_dictionary/term_compaction.md) — conversation summarization to free context; relevance: the automatic pre-compaction memory flush.
- [term_context_window](../../term_dictionary/term_context_window.md) — model prompt budget; relevance: the bootstrap file budget + injected-context truncation.
- [term_knowledge_base](../../term_dictionary/term_knowledge_base.md) — maintained structured knowledge store; relevance: the Memory Wiki companion knowledge layer.
- [term_zettelkasten](../../term_dictionary/term_zettelkasten.md) — linked atomic-note knowledge method; relevance: the plain-Markdown-files-as-memory model with wiki-style linking.
- [term_hybrid_search](../../term_dictionary/term_hybrid_search.md) — combined vector+keyword retrieval; relevance: `memory_search` uses hybrid search when an embedding provider is set.

**Docs**
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes persistent memory model; relevance: closest sibling-product memory-overview note.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory backend catalog; relevance: the builtin/QMD/Honcho/LanceDB backend cards.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — memory provider plugin model; relevance: the active memory plugin (`memory-core`) ownership.
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory overview; relevance: peer agent's file-based memory model.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory capture; relevance: the automatic memory flush + distill-to-MEMORY.md behavior.
- [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — CLAUDE.md memory files; relevance: direct analogue of `MEMORY.md` durable memory file.
- [hermes_prompt_assembly](../hermes_agent/hermes_prompt_assembly.md) — prompt/context assembly; relevance: which memory files are injected at session bootstrap.
- [band_overview](../band/band_overview.md) — Band agent-memory API overview; relevance: peer cross-session memory framing.
- [oc_concepts_memory_builtin](oc_concepts_memory_builtin.md) (planned, this series) — default SQLite backend; relevance: the builtin backend card detailed.
- [oc_concepts_memory_honcho](oc_concepts_memory_honcho.md) (planned, this series) — Honcho backend; relevance: the Honcho backend card detailed.
- [oc_concepts_features](oc_concepts_features.md) (planned, this series) — capability index; relevance: memory is an agent-runtime capability surfaced there.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory subsystem; relevance: implements MEMORY.md/daily/dreaming/flush.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the agent workspace that owns the memory files.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the `openclaw memory` CLI surface.

**Snippets**
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory engine; relevance: the active memory plugin owning recall/promotion.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory events/triggers; relevance: file-watch debounced reindex + memory-flush turn.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — `memory_search` tool; relevance: the `memory_search`/`memory_get` tools.
- [snippet_brp_agent_memory_system](../../code_snippets/snippet_brp_agent_memory_system.md) — agent memory system; relevance: peer durable-vs-working memory architecture.
- [snippet_openclaw_memory_runtime_re_exports](../../code_snippets/snippet_openclaw_memory_runtime_re_exports.md) — memory runtime surface; relevance: the memory subsystem's public runtime API.

### oc_concepts_memory_builtin (10t · 10s · 10d)

**Terms**
- [term_in_memory_database](../../term_dictionary/term_in_memory_database.md) — embedded local database; relevance: the per-agent SQLite memory store.
- [term_fts5](../../term_dictionary/term_fts5.md) — SQLite FTS5 full-text index; relevance: keyword search via FTS5 (BM25 scoring).
- [term_bm25](../../term_dictionary/term_bm25.md) — BM25 ranking function; relevance: the FTS5 BM25 keyword scoring.
- [term_hybrid_search](../../term_dictionary/term_hybrid_search.md) — combined vector+keyword retrieval; relevance: the engine's hybrid-search mode.
- [term_embedding](../../term_dictionary/term_embedding.md) — dense vector representation; relevance: vector search via embeddings from any provider.
- [term_vector_database](../../term_dictionary/term_vector_database.md) — vector index/store; relevance: sqlite-vec in-database vector queries.
- [term_sqlite_vec](../../term_dictionary/term_sqlite_vec.md) — SQLite vector extension; relevance: the optional sqlite-vec acceleration + fallback.
- [term_similarity_search](../../term_dictionary/term_similarity_search.md) — nearest-neighbor lookup; relevance: cosine-similarity vector search over chunks.
- [term_tokenization](../../term_dictionary/term_tokenization.md) — text→tokens (CJK trigram); relevance: CJK trigram tokenization + ~400-token chunking.
- [term_bedrock](../../term_dictionary/term_bedrock.md) — AWS Bedrock embedding provider; relevance: a supported embedding provider (AWS credential chain).

**Docs**
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory backend catalog; relevance: the builtin-vs-QMD-vs-Honcho choice.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — memory provider plugin; relevance: the embedding-provider plugin model (e.g. llama.cpp local).
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — peer memory backend overview; relevance: file-indexed memory retrieval framing.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — persistent memory model; relevance: the indexed `MEMORY.md`/`memory/*.md` source files.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — pluggable backend selection; relevance: builtin-vs-alternative backend selection model.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — agent memory store API; relevance: peer indexed-memory store with search.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env/keys; relevance: `OPENAI_API_KEY` / provider apiKey setup for embeddings.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth config; relevance: the supported embedding-provider auth (OpenAI/Bedrock/Gemini/etc.).
- [oc_concepts_memory](oc_concepts_memory.md) (planned, this series) — memory overview; relevance: this is the default backend it links to.
- [oc_concepts_memory_honcho](oc_concepts_memory_honcho.md) (planned, this series) — Honcho backend; relevance: the when-to-use alternative.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory subsystem; relevance: implements the SQLite builtin engine + indexing.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM/embedding provider plugins; relevance: the supported embedding-provider integrations.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the `openclaw memory status/index` CLI.

**Snippets**
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — SQLite memory schema; relevance: the per-agent SQLite memory index layout.
- [snippet_openclaw_memory_host_query_lexica](../../code_snippets/snippet_openclaw_memory_host_query_lexica.md) — FTS5 keyword query; relevance: the FTS5 BM25 keyword search path.
- [snippet_openclaw_memory_host_query_tokenizer](../../code_snippets/snippet_openclaw_memory_host_query_tokenizer.md) — query tokenizer (CJK trigram); relevance: CJK trigram tokenization for keyword search.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding generation; relevance: vector search via provider embeddings.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs/chunks; relevance: the ~400-token / 80-overlap chunking before embedding.
- [snippet_openclaw_memory_host_internal_chunking](../../code_snippets/snippet_openclaw_memory_host_internal_chunking.md) — internal chunking; relevance: the chunked indexing mechanics.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search tool; relevance: hybrid search exposed to the agent.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory engine; relevance: the builtin engine that ties index + search together.

### oc_concepts_memory_honcho (10t · 10s · 10d)

**Terms**
- [term_honcho](../../term_dictionary/term_honcho.md) — Honcho AI-native memory service; relevance: this note IS the Honcho backend plugin.
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — agent cross-session memory; relevance: Honcho is an agentic-memory backend.
- [term_personalization](../../term_dictionary/term_personalization.md) — per-user adaptation; relevance: Honcho builds per-user profiles (preferences/facts/style).
- [term_similarity_search](../../term_dictionary/term_similarity_search.md) — semantic nearest-neighbor; relevance: Honcho's semantic search over observations.
- [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — multi-agent coordination; relevance: parent/child multi-agent awareness with observers.
- [term_subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: parents auto-track spawned sub-agents as observers.
- [term_episodic_memory](../../term_dictionary/term_episodic_memory.md) — conversation/event memory; relevance: per-turn conversation persistence across sessions.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: Honcho is an OpenClaw plugin (`openclaw honcho setup`).
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin extension framework; relevance: Honcho registers tools via the plugin system + `plugins.entries`.
- [term_context_engine](../../term_dictionary/term_context_engine.md) — plugin context-injection engine; relevance: Honcho injects context in the `before_prompt_build` phase.

**Docs**
- [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho memory provider (Hermes); relevance: the direct sibling-product Honcho integration note.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory backend catalog; relevance: Honcho-vs-builtin backend selection.
- [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — memory provider plugin model; relevance: Honcho as a plugin-installed backend.
- [hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — plugin install/management; relevance: `openclaw plugins install @honcho-ai/openclaw-honcho`.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin types + hook surfaces; relevance: the `before_prompt_build` hook + registered tools.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-agent profiles; relevance: parent/child multi-agent awareness.
- [pi_extensions_context](../pi/pi_extensions_context.md) — context extension plugins; relevance: the context-engine plugin pattern Honcho uses.
- [band_agent_api_memories](../band/band_agent_api_memories.md) — service-backed agent memory API; relevance: peer dedicated-service memory model.
- [oc_concepts_memory](oc_concepts_memory.md) (planned, this series) — memory overview; relevance: the backend card Honcho is detailed from.
- [oc_concepts_memory_builtin](oc_concepts_memory_builtin.md) (planned, this series) — builtin backend; relevance: the Honcho-vs-builtin comparison.

**Repos**
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — OpenClaw memory subsystem; relevance: the memory plugin surface Honcho plugs into.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: how the Honcho plugin registers tools + config.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: parent/child sub-agent observer tracking.

**Snippets**
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — pluggable memory engine; relevance: the swappable backend Honcho replaces.
- [snippet_openclaw_memory_runtime_re_exports](../../code_snippets/snippet_openclaw_memory_runtime_re_exports.md) — memory runtime surface; relevance: the memory plugin contract Honcho implements.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: how the installed Honcho plugin is loaded.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — sub-agent registry; relevance: parent-tracks-child observer model.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn; relevance: parents added as observers in child sessions.
- [snippet_brp_agent_memory_system](../../code_snippets/snippet_brp_agent_memory_system.md) — agent memory system; relevance: peer cross-session memory architecture.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory event hooks; relevance: the after-every-turn persistence trigger.


## Undigested Terms Plan

Per master: OpenClaw vocabulary that is the subject of a doc page is digested as the `oc_*` doc note itself, NOT as a new `term_dictionary` entry. The only `term_dictionary` interaction is **linking existing** terms. Re-ran the Step-2d new-term scan over all 7 pages; outcome below.

| Term (as it appears) | Disposition |
|---|---|
| Mantis (live visual e2e QA system) | OpenClaw product vocab → covered by `oc_concepts_mantis_architecture` + `_cli_scenarios` + `_evidence_model`; no new term note. |
| Crabbox / warm lease / VNC rescue | OpenClaw-internal infra vocab → described inline in the Mantis notes; not vault-reusable; no new term note. (`term_sandbox` linked for the isolated-VM concept.) |
| ClawSweeper / `@openclaw-mantis` / `@clawsweeper` triggers | OpenClaw-internal tooling → inline in note 3; no new term note. |
| `mantis-evidence.json` / artifact kinds (timeline/motionPreview/…) | OpenClaw schema vocab → covered by `oc_concepts_mantis_evidence_model` (note 4); no new term note. |
| Markdown IR (intermediate representation) / `markdownToIR` / chunking | OpenClaw formatting-pipeline vocab → covered by `oc_concepts_markdown_formatting`; link existing `term_markdown`, `term_tokenization`; no new term note. |
| `MEMORY.md` / `DREAMS.md` / daily notes / action-sensitive memory | OpenClaw memory-model vocab → covered by `oc_concepts_memory`; link existing `term_agentic_memory`, `term_episodic_memory`, `term_workflow_memory`, `term_memory_information_density`; no new term note. |
| Dreaming / grounded backfill / live promotion | OpenClaw memory-consolidation vocab → linked to existing `term_memory_dreaming`; full detail digested by `concepts/dreaming` (co02, planned); no new term note. |
| Builtin engine / FTS5 / sqlite-vec / hybrid search / CJK trigram | retrieval vocab → link existing `term_in_memory_database`, `term_fts5`, `term_sqlite_vec`, `term_bm25`, `term_hybrid_search`, `term_vector_database`, `term_embedding`, `term_similarity_search`, `term_tokenization` (xref-augment 2026-06-21 confirmed `term_fts5` + `term_sqlite_vec` ALSO exist — link, do not create); no new term note. |
| Honcho / user modeling / cross-session memory | third-party plugin → link existing `term_honcho`, `term_personalization`, `term_agentic_memory`; no new term note. |
| Embedding providers (Voyage, DeepInfra, Gemini, …), backends (QMD, LanceDB) | provider/backend names → linked where an existing term exists; backend pages owned by co04/pl04/pl14; no new term note. |

**New `term_dictionary` captures: 0.** No genuinely cross-cutting, vault-reusable term lacking an existing note appeared (the agentic/memory/retrieval/QA glossary is already rich — `term_agentic_memory`, `term_memory_dreaming`, `term_hybrid_search`, `term_vector_database`, `term_canary_testing`, `term_honcho`, etc. all exist). No new-term candidate proposed; no `acronym_glossary_*.md` edit required.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9)

Single execution phase (9 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order + forbidden-field absence; `## Overview`/`## Related Notes` present; bold footer; 0 LINK-003 |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/concepts/<page>.md` | every claim/snippet traceable to source; no invented config keys |
| G3 | Density + Coverage | per-note `wc -w` + code-fence count; section-coverage map | ≤400 lines, ≤2500 words, ≤6 code blocks, one BB; every source H2 mapped |
| G4 | Cross-Reference | `## Related Notes` ≥6 relevance-selected terms + repos/siblings, each indexed `[text](path.md)` with relevance statement | floor met per note; all links indexed format |
| G6 | Broken-link | `/tessellum-fix-broken-links` after incremental reindex | 0 broken links |
| G7 | Discoverability | each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | satisfied via `entry_openclaw_docs.md` + repo/term inlinks |
| G8 | In-degree ≥1 | query `note_links`/`in_degree` after reindex | every new note in_degree ≥1 (anti-island) |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_features oc_concepts_mantis_architecture oc_concepts_mantis_cli_scenarios oc_concepts_mantis_evidence_model oc_concepts_mantis_slack_desktop_runbook oc_concepts_markdown_formatting oc_concepts_memory oc_concepts_memory_builtin oc_concepts_memory_honcho"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (body only, excl. frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
done

# YAML frontmatter sweep over the whole subfolder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost / G8 in-degree (after incremental reindex)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  indeg=$(sqlite3 "$DB" "SELECT in_degree FROM notes WHERE note_name='$n'")
  echo "$n in_degree=${indeg:-NOT_INDEXED}"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences (page) | Within caps? |
|---|---|---|---:|---|---|
| 1 | oc_concepts_features | concept | 350 | 0 | ✅ |
| 2 | oc_concepts_mantis_architecture | concept | 700 | (mantis 15, split) ≤6 | ✅ |
| 3 | oc_concepts_mantis_cli_scenarios | procedure | 700 | (mantis 15, split) ≤6 | ✅ |
| 4 | oc_concepts_mantis_evidence_model | model | 600 | (mantis 15, split) ≤6 | ✅ |
| 5 | oc_concepts_mantis_slack_desktop_runbook | procedure | 600 | 8 → keep ≤6 (drop redundant log-cat fences) | ✅ |
| 6 | oc_concepts_markdown_formatting | procedure | 550 | 3 | ✅ |
| 7 | oc_concepts_memory | concept | 750 | 6 | ✅ |
| 8 | oc_concepts_memory_builtin | procedure | 550 | 4 | ✅ |
| 9 | oc_concepts_memory_honcho | procedure | 500 | 3 | ✅ |

No note approaches the 2,500-word / 400-line caps. The two code-fence watch-items: `mantis.md` (15 fences) is split three ways so each note holds ≤6; `mantis-slack-desktop-runbook.md` (8 fences) — note 5 reproduces the GitHub-dispatch + 2 key local-CLI invocations + hydrate table and collapses the redundant `cat *.log` failure-handling block into prose to stay ≤6.

## Entry Point Decision (inherited from master)

Contributes **9 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step; >30 master total → dedicated hub required), grouped under a **"Concepts"** section with two clusters: *Capabilities & Formatting* (notes 1, 6) and *Mantis QA* (notes 2-5) and *Memory* (notes 7-9). Each note receives its entry-point back-link at finalization (this is the primary G7/G8 inbound-link source). No separate child entry point is created for this slice.

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (planned, master pre-step) → **all 9 notes** (primary inbound source).
- `repo_openclaw_memory` → notes 7, 8, 9 (memory model + backends).
- `repo_openclaw_channels_messaging` → notes 3, 5, 6 (Mantis transport QA + outbound markdown formatting).
- `repo_openclaw` → notes 1, 2 (capabilities index + Mantis system overview).
- `term_openclaw` → notes 1, 7 (capabilities + memory model — high-traffic hub term).
- `term_agentic_memory` → note 7; `term_honcho` → note 9; `term_canary_testing` → notes 2, 3, 5.
- `term_markdown` → note 6; `term_hybrid_search` / `term_vector_database` → note 8.
- Reciprocal: each new note's `## Related Notes` links back to these, and to its sibling `oc_concepts_*` notes (in-series in-degree).

## Pacing Rules (inherited from master)

One execution phase; all 8 gates PASS before commit. Re-read each source page during execution; reproduce config/CLI/YAML snippets verbatim (selectively, ≤6 per note). One BB per note. Cap dynamic-workflow fan-out at ~30 agents/run. `git pull --rebase --autostash` first; commit+push per wave; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + in_degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 checkpoints PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Per-note counts (all exceed every floor).**

| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|:--:|
| oc_concepts_features | 10 | 10 | 10 (8 / 2) | 3 | ✅ |
| oc_concepts_mantis_architecture | 10 | 10 | 11 (8 / 3) | 3 | ✅ |
| oc_concepts_mantis_cli_scenarios | 10 | 11 | 10 (7 / 3) | 3 | ✅ |
| oc_concepts_mantis_evidence_model | 10 | 10 | 10 (7 / 3) | 3 | ✅ |
| oc_concepts_mantis_slack_desktop_runbook | 10 | 10 | 10 (7 / 3) | 3 | ✅ |
| oc_concepts_markdown_formatting | 10 | 10 | 10 (8 / 2) | 3 | ✅ |
| oc_concepts_memory | 10 | 10 | 11 (8 / 3) | 3 | ✅ |
| oc_concepts_memory_builtin | 10 | 10 | 10 (8 / 2) | 3 | ✅ |
| oc_concepts_memory_honcho | 10 | 10 | 10 (8 / 2) | 3 | ✅ |


**New-term candidates: NONE.** The re-read Step-2d new-term scan surfaced no genuinely cross-cutting, vault-reusable term lacking an existing note. The augment additionally discovered that `term_fts5` and `term_sqlite_vec` already exist (updated the Undigested Terms Plan builtin-engine row to LINK them, not create). Best-fit glossary: N/A (0 new terms; were one ever proposed it would go to `acronym_glossary_*.md` via `/tessellum-capture-term-note`).

**Issues / notes.** None blocking. The original draft `## Candidate Cross-References` cited a few non-existent labels for note 6 (`cc_output_styles` exists but is a Claude-styles doc of marginal relevance — replaced with on-topic channel/markdown docs) and used the ≥6-term floor; the LOCKED mapping raises every note to 10 terms / 10+ snippets / 10+ docs. No source section omitted (Section Coverage Map re-confirmed against the 7 re-read pages).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|:--:|---|
| CP1 | Related Notes step ≥8 terms + floors (≥10 snippets, ≥10 docs), each with relevance statement | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)`: all 9 notes at 10t / 10–11s / 10–11d; every link is `[Name](path.md) — desc; relevance: …`. Deterministic count + floor check passed for all 9. |
| CP2 | 9-GATE table present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7 Discoverability, G8 In-degree≥1 with tools + pass criteria; `## Validation Scripts` implements format/density/YAML/ghost/in-degree checks. |
| CP3 | Entry point inherited (`entry_openclaw_docs` planned at master W1) | **PASS** | `## Entry Point Decision (inherited from master)`: 9 rows contributed to `entry_openclaw_docs.md` (master W1 pre-step; >30 master total → dedicated hub REQUIRED); per-note back-link is the primary G7/G8 inbound source. |
| CP4 | Size manageable | **PASS** | 9 planned notes (≤30); single execution phase. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Format inherited from master `## Format Definition` (derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora — `## Overview` opener, `## Related Notes` reference section, bold `**Source**`/`**Last Updated**`/`**Status**` footer, fixed YAML field order, forbidden-field list). Matches existing target-dir convention, not invented. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: no note approaches 2,500w/400L; `mantis.md` (4,433w measured, 15 fences, mixed BB) split ×3 (concept/procedure/model) per `## Split Decisions`; each resulting note ≤6 fences. No unaddressed borderline. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 7/7 pages 2026-06-21 (frontmatter-stripped `wc -w`): features 425, mantis 4,433, runbook 1,024, markdown 668, memory 1,573, builtin 636, honcho 627 — all within ±10% of the plan's Source table (ratios 0.90–0.95), well inside the 0.7–1.3 band. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements present | **PASS** | `## Undigested Terms Plan` (10-row disposition table, 0 new captures) + `## Term-Note Authoring Requirements` (N/A — 0 new terms; inherited multi-source mandate stated). Re-ran Step-2d on the 7 re-read pages: no new term. |
| CP8f | Slug specificity / all-notes (term AND doc) collision audit | **PASS** | All 9 planned `oc_*` slugs are specific (page-scoped, no too-general one-word slugs). Collision audit across `term_dictionary/` AND `resources/documentation/`: no planned `oc_*` doc duplicates an existing term OR doc note (no `oc_*` notes exist yet; the memory/QA/markdown concepts are owned as docs, with existing terms LINKED not recreated). `term_fts5`/`term_sqlite_vec` discovered + rerouted to LINK. 0 new term slugs to dedup. |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` covers all 9 notes with ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 9, plus `repo_openclaw*` / `term_*` inlinks); G7+G8 are gated phase entries (`## Per-Phase Validation Gate`), not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.**
