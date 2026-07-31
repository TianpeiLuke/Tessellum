---
title: Documentation Digestion Plan (Master) — Hermes Agent Docs
date: 2026-06-14
revised: 2026-06-19
status: completed
source_url: https://hermes-agent.nousresearch.com/docs/
source_mirror: inbox/hermes_agent_docs/
master_plan: self
mirror_commit: c253b07
mirror_resynced: 2026-06-19
---

# Plan: Digest the Hermes Agent Documentation into Vault Notes (Master Index)

> **This is a pure index hub** (canonical Step 1e). It defines the shared routing,
> format, cross-references, gates, pacing, entry-point decision, and the undigested-term
> ownership sweep. **Per-note tables live in the sub-plans, never here.** Each sub-plan is
> independently augmentable + executable.

## Objective

Digest the **Hermes Agent** user-facing documentation (Nous Research) into BB-atomic vault
notes under `resources/documentation/hermes_agent/`, mirroring how the Claude Code docs were
organized. Hermes Agent is "the self-improving AI agent built by Nous Research" — a
terminal-native autonomous coding/task agent with persistent memory, agent-created skills, a
messaging gateway spanning 20+ platforms, and broad provider support.

**Relationship to existing vault content (decided 2026-06-14):** the vault already holds **535
Hermes notes that digest the SOURCE CODE** (`areas/code_repos/repo_hermes_agent_*` ×13,
`resources/code_snippets/snippet_hermes_agent_*`, entry `entry_code_snippets_hermes_agent.md`,
plus `thought_hermes_agent_vs_*`/`coe_hermes_*`). These docs notes are the **user-facing
concept/procedure/how-to layer**: they capture *how to use* Hermes, and **cross-link down** to
the existing code/repo/snippet notes for *how it is implemented*. Concepts already captured as
term notes are **linked, not recreated**.

## Source & Mirror

- **Live source:** `https://hermes-agent.nousresearch.com/docs/` (Next.js SPA; no `.md`/`llms-full.txt` endpoints).
- **Authoritative index:** `https://hermes-agent.nousresearch.com/docs/llms.txt` (curated; under-lists messaging + dev/guide pages).
- **Local mirror (committed):** `inbox/hermes_agent_docs/` — the docs markdown source from the
  open-source repo `NousResearch/hermes-agent` at `website/docs/`, extracted verbatim. Mirror committed
  (matches the `inbox/claude_code_docs/` precedent) so execution agents re-read from disk and word counts
  are exact.
  - **Re-synced 2026-06-19** from `main` HEAD commit `c253b07` (was pinned `95715dc`). The fresh pull is
    **348 `.md`/`.mdx` files** (was 343): **+6 new pages** (`user-guide/managed-scope.md`,
    `user-guide/messaging/raft.md`, and 4 skill-catalog source files under
    `user-guide/skills/optional/{payments/*,productivity/productivity-shop}`), **1 rename**
    (`productivity-shop-app.md` → `productivity-shop.md`), and **33 content-modified** pages. The full-tree
    `diff -rq` against the fresh source is empty (byte-identical to upstream `main`). All sub-plan word/code
    counts and the Source-Coverage Ledger below are re-measured from this fresh mirror.
- **Measurement:** word/code/heading counts in the sub-plans and the Source-Coverage Ledger
  below are **measured from the local files** (`wc`-equivalent), NOT WebFetch estimates.
  (WebFetch over-counted by 50–100% — e.g. env-variables reported 18,847 vs actual 9,223 — because
  it included sidebar/nav; do not reuse those figures.)

**Page accounting:**

| Set | Files | Treatment |
|---|---|---|
| Rendered doc pages (digestible) | **174** (~401K words) | → ~233 BB-atomic notes across 21 sub-plans |
| Per-skill catalog source files (`user-guide/skills/bundled/*`, `optional/*`) | 174 (~293K words) | NOT individually digested — aggregated into the 2 rendered catalog pages (`reference/skills-catalog.md`, `reference/optional-skills-catalog.md`), owned by SP21 |
| **Total mirrored** | **348** | all retained on disk |

> **Re-sync delta (2026-06-19, `95715dc`→`c253b07`):** rendered pages 172→**174** (+2: `managed-scope.md`
> → SP03b, `messaging/raft.md` → SP12b); skill-catalog sources 171→**174** (+3 payments + rename); total
> 343→**348**. 28 ledger pages gained words (largest: `multi-profile-gateways.md` 1283→2113w; `honcho.md`
> 2128→2505w crossed the 2500w cap; `docker.md` 5815→6013w). The 2 new rendered pages add ~2 planned notes
> (~231→~233). Per-sub-plan deltas are recorded in each sub-plan's Re-Sync Note.

This is a **>30-note job → master + sub-plans** (canonical Step 1e). Scale is comparable to the
Claude Code docs digestion (134 pages → 339 notes).

## Routing Decision (shared)

- **Target directory:** `resources/documentation/hermes_agent/` (NEW subfolder — justified: a
  cohesive >200-note external open-source-docs series; 3-criterion rule = 3/3 novel).
- **File prefix:** `hermes_<topic>_*.md` (e.g. `hermes_cli_interface.md`, `hermes_gateway_telegram.md`).
- **One BB per note**; density caps ≤2500w / ≤6 code blocks / ≤400 lines — split before writing.
- **Do NOT duplicate** existing code-digestion notes (see Dedup Policy); link to them instead.

## Note Format Definition (shared — derived from `resources/documentation/claude_code/cc_*.md`)

Use the established documentation-note format **verbatim** (derived from
`cc_admin_enforcement_controls.md` and siblings):

```yaml
---
tags:
  - resource
  - documentation
  - hermes_agent
  - <topic-tag>
  - <one area tag>
keywords:        # 4–8 lowercase search phrases, itemized list (never inline array)
  - <phrase>
topics:
  - Hermes Agent
  - <specific area>
language: markdown
date of note: 2026-06-14
status: active
building_block: <concept|procedure|model|argument|empirical_observation|navigation>
source_url: https://hermes-agent.nousresearch.com/docs/<path>
access_control_group: ["general"]
---
```

Body: `# <Title>` → `## Overview` (2–4 sentence opener leading with what it IS) →
**source-mirrored H2 sections** → `## Related Notes` (indexed markdown links, each with a
one-line description + relevance) → footer `**Source**` / `**Last Updated**` / `**Status**`.

**Forbidden YAML fields:** `title`, `category`, `created`, `updated`, `source`, `parent`,
`author`, `related_wiki`, `note_second_category`. Year tags quoted. No wiki/markdown links in YAML.

## Dedup Policy & Cross-References (shared)

**Three-way dedup before creating any note** (bm25 + dense + filename) across BOTH
`term_dictionary/` AND `documentation/`. Substantive existing coverage → **link/enrich, do not recreate.**

**Existing code-digestion notes to cross-link (the implementation layer):**
`repo_hermes_agent.md`, `repo_hermes_agent_agent_core.md`, `repo_hermes_agent_cli.md`,
`repo_hermes_agent_gateway_messaging.md`, `repo_hermes_agent_mcp_toolsets.md`,
`repo_hermes_agent_tools.md`, `repo_hermes_agent_skills.md`, `repo_hermes_agent_plugins.md`,
`repo_hermes_agent_providers_adapters.md`, `repo_hermes_agent_cron.md`,
`repo_hermes_agent_acp.md`, `repo_hermes_agent_trajectory_research.md`,
`repo_hermes_agent_tui_gateway.md`; entry `entry_code_snippets_hermes_agent.md`;
`thought_hermes_agent_vs_openclaw.md`, `thought_hermes_agent_vs_dks_slipbox.md`.

**Existing term notes to LINK not recreate** (verify per-note relevance at augmentation):
`term_mcp_gateway`, `term_subagent`, `term_context_window`, `term_cron`, `term_skill_manifest`,
`term_agent_harness`, `term_autonomous_coding_agents`, `term_sandbox_backend`,
`term_prompt_injection`, `term_oauth_token`, `term_fts5`, `term_sqlite_vec`.

**Per-note Related Notes minimums (RAISED 2026-06-19 per user directive — elevated floor) — applies to
EVERY sub-plan:** each planned note's `## Related Notes` must include, **all relevancy-selected to that
note's content, each with a relevance clause** — FOUR counted floors:
- **≥5 code-repo notes** (`areas/code_repos/repo_*` — primarily the 13 `repo_hermes_agent_*` notes that
  digest the Hermes SOURCE CODE: `repo_hermes_agent`, `_agent_core`, `_cli`, `_gateway_messaging`,
  `_mcp_toolsets`, `_tools`, `_skills`, `_plugins`, `_providers_adapters`, `_cron`, `_acp`,
  `_trajectory_research`, `_tui_gateway`; plus genuinely-analogous external repo notes where relevant);
  pick the repo notes whose modules implement what THIS doc note describes;
- **≥10 snippet notes** (`resources/code_snippets/snippet_hermes_agent_*` — the 517-note implementation
- **≥10 documentation notes** (`resources/documentation/` — sibling `hermes_*` notes in this series, the
  analogous `claude_code/cc_*` agent-tool docs, plus other genuinely-relevant existing doc notes);
  intra-series `hermes_*` doc links resolve at finalization (G5/G8).

> **Floor history:** 2026-06-14 = ≥8 term + ≥8 snippet + ≥5 doc. 2026-06-19 directive (current) =
> ≥8 term + **≥5 code-repo** + **≥10 snippet** + **≥10 doc** — snippets RAISED 8→10 and remain a counted
> floor; code-repo added; docs raised 5→10. All four are mandatory, relevancy-selected.

Selection is by **content relevancy**, never padding. Augmentation DB-verifies every listed term, code-repo,
and snippet target exists and is active, and records the relevance clause per link. If a niche note genuinely
cannot reach a floor, justify per-note (broaden keywords / check adjacent concepts first — only fall short
with explicit reason).

## Sub-Plans Index

Priority: **P1** = foundational concepts P2/P3 reference · **P2** = features/messaging ·
**P3** = guides/developer/reference. Status: pending → ready → in_progress → complete.
Sub-plans marked **(split a/b)** exceed the 15-note heuristic and split during augmentation.

| ID | Sub-plan file | Topic | Pages | ~Notes | Pri | Status |
|----|---------------|-------|------:|------:|:--:|:--:|
| 01 | `plan_digest_hermes_agent_docs_01_getting_started.md` | Getting Started & Install (install, quickstart, learning-path, updating, termux, nix, landing) | 8 | 9 | P1 | **ready** |
| 02 | `plan_digest_hermes_agent_docs_02_cli_config.md` | CLI, TUI, Sessions & Configuration | 5 | 12 | P1 | **ready** |
| 03a | `plan_digest_hermes_agent_docs_03a_deployment_platforms.md` | Deployment & Platforms (docker, windows-native, desktop, wsl2, git-worktrees) | 5 | 9 | P1 | **ready** |
| 03b | `plan_digest_hermes_agent_docs_03b_security_secrets.md` | Security, Secrets, Checkpoints & Managed Scope (security, checkpoints-and-rollback, bitwarden, **managed-scope**) | 5 | 5 | P1 | **ready** |
| 04 | `plan_digest_hermes_agent_docs_04_profiles.md` | Profiles & Multi-Profile Ops | 3 | 4 | P2 | **ready** |
| 05 | `plan_digest_hermes_agent_docs_05_knowledge_memory_skills.md` | Knowledge, Memory & Skills (tools, tool-gateway, memory(+providers), honcho, context files/refs, skills, curator, personality) | 11 | 13 | P1 | **ready** |
| 06a | `plan_digest_hermes_agent_docs_06a_automation.md` | Automation & Multi-Agent (cron, delegation, code-exec, goals, batch) | 5 | 6 | P2 | **ready** |
| 06b | `plan_digest_hermes_agent_docs_06b_plugins_hooks_kanban.md` | Plugins, Hooks & Kanban (plugins, built-in-plugins, hooks, kanban(+tutorial)) | 5 | 9 | P2 | **ready** |
| 08a | `plan_digest_hermes_agent_docs_08a_media.md` | Media (voice-mode, tts/stt, vision, image-gen, spotify, deliverable) | 6 | 8 | P2 | **ready** |
| 08b | `plan_digest_hermes_agent_docs_08b_web_tools.md` | Web & Tool Surface (browser, web/x-search, computer-use, lsp, skins, tool-search, features-overview, kanban-worker-lanes) | 9 | 10 | P2 | **ready** |
| 09 | `plan_digest_hermes_agent_docs_09_protocols_providers.md` | Protocols & Provider Integration (mcp, acp, api-server, provider-routing, fallback, credential-pools, subscription-proxy) | 7 | 9 | P1 | **ready** |
| 10 | `plan_digest_hermes_agent_docs_10_dashboard_runtimes.md` | Dashboard & Runtimes (web-dashboard, extending-the-dashboard, codex-app-server-runtime) | 3 | 8 | P2 | **ready** |
| 11a | `plan_digest_hermes_agent_docs_11a_messaging_gateway_telegram_discord.md` | Messaging: Gateway concepts + Telegram + Discord | 3 | 6 | P2 | **ready** |
| 11b | `plan_digest_hermes_agent_docs_11b_messaging_slack_matrix_teams.md` | Messaging: Slack, Matrix, Mattermost, Teams, Google Chat | 6 | 9 | P2 | **ready** |
| 12a | `plan_digest_hermes_agent_docs_12a_messaging_consumer.md` | Messaging: WhatsApp(+Cloud), Signal, SMS, Email, LINE, ntfy | 7 | 8 | P2 | **ready** |
| 12b | `plan_digest_hermes_agent_docs_12b_messaging_webhooks_home.md` | Messaging: SimpleX, BlueBubbles, Photon, Home Assistant, Open WebUI, Webhooks, MS-Graph, **Raft** | 8 | 9 | P2 | **ready** |
| 13 | `plan_digest_hermes_agent_docs_13_messaging_china.md` | Messaging: Chinese Platforms (feishu, weixin, wecom(+callback), dingtalk, yuanbao, qqbot) | 7 | 8 | P2 | **ready** |
| 14 | `plan_digest_hermes_agent_docs_14_inference_providers.md` | Inference Providers & Integrations (providers, nous-portal, integrations index) | 3 | 5 | P1 | **ready** |
| 15 | `plan_digest_hermes_agent_docs_15_guides_providers_setup.md` | Guides: Providers & Setup (local-llm/ollama, gemini, grok, minimax, bedrock, azure, nemotron, nous-portal, oauth-over-ssh) | 10 | 11 | P3 | **ready** |
| 16 | `plan_digest_hermes_agent_docs_16_guides_automation_bots.md` | Guides: Automation & Bots (briefing bot, cron patterns, PR review, team telegram, teams pipeline, delegation patterns) | 10 | 10 | P3 | **ready** |
| 17 | `plan_digest_hermes_agent_docs_17_guides_build_extend.md` | Guides: Build & Extend (build-plugin, automation-blueprints, use-mcp/voice/soul, work-with-skills, python-library, migrate-from-openclaw, tips, msgraph reg) | 10 | 13 | P3 | **ready** |
| 18 | `plan_digest_hermes_agent_docs_18_dev_internals.md` | Developer: Internals (architecture, agent-loop, prompt-assembly, compression, gateway/session/provider/tools/cron/acp internals, trajectory, browser-supervisor, plugin-llm-access) | 13 | 13 | P3 | **ready** |
| 19a | `plan_digest_hermes_agent_docs_19a_dev_core_extension.md` | Developer: Core Extension (adding tools/providers/platform-adapters, creating-skills, extend-cli, programmatic, contributing) | 7 | 9 | P3 | **ready** |
| 19b | `plan_digest_hermes_agent_docs_19b_dev_provider_plugins.md` | Developer: Provider/Engine Plugin Authoring (model/web-search/image-gen/memory/video-gen/context-engine plugins) | 6 | 6 | P3 | **ready** |
| 20 | `plan_digest_hermes_agent_docs_20_ref_commands.md` | Reference: Commands (cli-commands, slash-commands, profile-commands) | 3 | 6 | P3 | **ready** |
| 21 | `plan_digest_hermes_agent_docs_21_ref_env_tools_catalogs.md` | Reference: Env Vars, Tools/Toolsets, Skills Catalogs, MCP-config, Model-catalog, FAQ, Automation-blueprints | 9 | 14 | P3 | **ready** |

**Totals:** 21 sub-plans · **174 rendered pages** · **~233 notes** (pre-augmentation estimate;
word-driven, finalized per sub-plan; +2 pages / +2 notes from the 2026-06-19 re-sync — SP03b +1, SP12b +1).

## Execution Order

- **Wave P1 (foundations — concepts P2/P3 link to):** 01, 02, 05, 09, 14, 03
- **Wave P2 (features & messaging):** 04, 06, 08, 11, 12, 13, 10
- **Wave P3 (guides, developer, reference):** 15, 16, 17, 18, 19, 20, 21
- **Wave F (Finalization — entry points, glossaries, discoverability):** runs AFTER all 21 sub-plans land
  and reindex. This is a **scheduled execution phase, not a recommendation** — see the Finalization Phase
  (Entry Points + Glossaries + G8) section below for the per-step contract.

Sub-plans within a wave are parallel-safe (no execution cross-dependency; cross-links added in Wave F).
Each sub-plan creates its term notes' glossary entries inline (Pattern B, per its Undigested Terms Plan);
the **series-level** entry point CREATE + parent/sibling-hub UPDATEs + glossary reconciliation happen in Wave F.

## Entry Point Decision (CREATE — required, >30 notes per Step 4c)

The ~233-note series is **>30 notes → CREATE a dedicated entry point REQUIRED**, plus UPDATE every relevant
below — these are scheduled, gated steps, not recommendations.

**CREATE — new series entry point:**
- **`0_entry_points/entry_hermes_agent_docs.md`** (`building_block: navigation`) — mirrors this master's
  Sub-Plans Index, grouped by section (Getting Started · CLI/Config · Deployment/Security · Profiles ·
  Knowledge/Memory/Skills · Automation/Plugins · Media/Web · Protocols/Providers · Dashboard/Runtimes ·
  Messaging · Inference Providers · Guides · Developer · Reference), **one row per planned note** (≈233 rows).
  Required body sections: `## Quick Stats` (note count, source, sub-plan count), per-section link tables,
  `## Related Entry Points`, `## References`. Sibling to `entry_claude_code_docs.md`.

- **`entry_research_and_ai_hub.md`** — PRIMARY parent hub for AI-agent/tooling doc series: add a row pointing
  to `entry_hermes_agent_docs.md`.
- **`entry_platform_docs.md`** — the documentation master index: add a `hermes_agent/ → entry_hermes_agent_docs.md`
  row to the "Developer Tools & AI" group + the folder→entry-point quick-reference table (mirrors the `band/` and
  `claude_code/` precedent).
- **`entry_gen_ai_dev.md`** — GenAI-development hub: add a back-link row (agent-framework / autonomous-agent docs).
- **Cross-link (bidirectional)** `entry_hermes_agent_docs.md` ↔ `entry_code_snippets_hermes_agent.md` (the
  CODE layer this docs series links down to) and ↔ `entry_claude_code_docs.md` (sibling external-agent-tool docs).

## Glossary Updates (term-note best-fit `acronym_glossary_*` entries)

Each of the ~32 undigested terms (see the Undigested Terms Plan) gets a glossary entry in its best-fit
`acronym_glossary_*.md` **as part of its `/tessellum-capture-term-note` run** (the capture skill's Step 5 — the
owning sub-plan does this inline when it captures the term, NOT a separate phase). All six target glossaries are
(12), `acronym_glossary_systems` (5), `acronym_glossary_security` (2), `acronym_glossary_workflows` (2). The
**Finalization Phase reconciles** that every captured term landed a glossary row (no term note without a glossary
entry) — a gated check, since a missed glossary row is a common Pattern-B slip.

## Finalization Phase (Entry Points + Glossaries + G8 — runs as Wave F, gated)

After all 21 sub-plans land + `/tessellum-run-incremental-update` reindexes, run these steps **in order**; each is
gated (do not mark the series complete until all pass):

1. **CREATE `entry_hermes_agent_docs.md`** with all ≈233 note rows grouped by section. Verify row count ==
   on-disk `hermes_*.md` count in `resources/documentation/hermes_agent/` via a reconciliation diff
   (`comm -23` of planned-rows vs actual files) — zero orphans, zero missing.
2. **UPDATE the hubs** `entry_research_and_ai_hub.md`, `entry_platform_docs.md`, `entry_gen_ai_dev.md` with the
   new-entry-point row; **bidirectional cross-link** with `entry_code_snippets_hermes_agent.md` and
   `entry_claude_code_docs.md`.
3. **Glossary reconciliation:** for every captured Hermes term, confirm a matching `acronym_glossary_*` row exists
   (query the term notes created vs glossary entries); fill any miss via the capture skill's Step 5 template.
4. **G8 / discoverability:** confirm every new `hermes_*` doc note has DB in-degree ≥1 from OUTSIDE
   `resources/documentation/hermes_agent/` (the new entry point + the per-SP Inlinks tables guarantee this);
   run `/tessellum-add-inlinks` and re-check in-degree.
5. **Broken-link sweep:** `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` across the new entry point +
   all `hermes_*` notes (the ≈233-row entry point is the most link-dense artifact).
6. **Reindex + commit** the entry point, hub updates, and glossary updates.

Each sub-plan's own `## Entry Point Decision (inherited)` section records how many rows it contributes to
`entry_hermes_agent_docs.md` and which glossaries its owned terms update — those are the inputs Wave F reconciles.

## Undigested Terms Plan (corpus-wide ownership sweep — Pattern B, interleaved)

>10 undigested terms → **Pattern B**: each sub-plan captures the terms it introduces (via
`/tessellum-capture-term-note`, NOT inline) BEFORE writing its digest notes. Every term has an
**owner** below (no term is owned by "no sub-plan"). Each sub-plan re-runs the three-way
existence check at augmentation (stub vs substantive vs absent) and may reassign.

**Extraction method (data-driven, 2026-06-14):** candidate terms were extracted from the mirror
by document-frequency (acronyms + backticked identifiers across the (then) 172 pages — cross-page spread
= shared importance), then run through a three-way DB check. (The 2026-06-19 re-sync added 2 rendered
pages — `managed-scope.md`, `messaging/raft.md`; their terms are owned by SP03b/SP12b below, no change
to the corpus-wide sweep outcome.) **The `LIKE` check produced false
corrected; see the caution list. This replaces the earlier hand-curated guess.

### Existing terms → LINK, do NOT recreate (confirmed real matches)

`term_mcp`, `term_mcp_gateway`, `term_acp`, `term_kanban`, `term_context_engine`, `term_cdp`,
`term_regular_checkpointing`, `term_subagent`, `term_cron`, `term_skill_manifest`,
`term_agent_harness`, `term_autonomous_coding_agents`, `term_sandbox_backend`,
`term_prompt_injection`, `term_oauth_token`, `term_context_window`, `term_fts5`, `term_sqlite_vec`.

### ⚠ False-positive caution (LIKE-matched a DIFFERENT concept → these ARE undigested, DO capture)

`AGENTS.md` ≠ `term_agentspace` · `progressive disclosure` ≠ `term_progressive_summarization` ·
`credential pool` ≠ `term_credential_stuffing` · `messaging gateway` ≠ `term_api_gateway` ·
`voice mode` ≠ `term_voice_wake` · `browser tool` ≠ `term_code_browser` ·
`hermes profile` ≠ `term_auth_profile` · `batch processing` ≠ `term_aws_batch` ·
Hermes `vision` ≠ generic `term_computer_vision`. **Each sub-plan must VISUALLY confirm LIKE hits,
never trust them** (this is the canonical false-dup lesson, reproduced here at plan time).

### Capture inventory (data-driven; DF = pages the term appears in)

| Candidate term slug | Concept | DF | Owner SP | Best-fit glossary |
|---|---|---:|:--:|---|
| `term_nous_portal` | Nous Portal subscription + Tool Gateway billing | 25+ | 14 | acronym_glossary_tools |
| `term_tool_gateway` | Nous Tool Gateway (managed tool proxy) | 12 | 05 | acronym_glossary_tools |
| `term_soul_md` | SOUL.md personality file | 24 | 05 | acronym_glossary_developer |
| `term_agents_md` | AGENTS.md project context file (≠ agentspace) | 18 | 05 | acronym_glossary_developer |
| `term_progressive_disclosure` | on-demand skill loading (≠ summarization) | 8 | 05 | acronym_glossary_llm |
| `term_skills_hub` | multi-source skill registry | 9 | 05 | acronym_glossary_tools |
| `term_skill_curator` | background skill maintenance loop | 6 | 05 | acronym_glossary_llm |
| `term_honcho` | AI-native memory provider | 7 | 05 | acronym_glossary_tools |
| `term_text_to_speech` | TTS subsystem + providers | 43 | 08 | acronym_glossary_llm |
| `term_speech_to_text` | STT / voice transcription | 17 | 08 | acronym_glossary_llm |
| `term_voice_mode` | real-time voice conversation mode (≠ voice_wake) | 12 | 08 | acronym_glossary_llm |
| `term_browser_automation` | Hermes browser tool/modes (≠ code_browser) | 13 | 08 | acronym_glossary_tools |
| `term_code_execution_tool` | `execute_code` RPC Python sandbox | 19 | 06 | acronym_glossary_developer |
| `term_delegate_task` | subagent spawn tool (links term_subagent) | 24 | 06 | acronym_glossary_llm |
| `term_kanban_multi_agent` | Hermes multi-profile task board (extends term_kanban) | 13 | 06 | acronym_glossary_workflows |
| `term_persistent_goal` | standing-objective loop (Ralph loop) | 6 | 06 | acronym_glossary_llm |
| `term_gateway_hooks` | gateway/plugin/shell lifecycle hooks | 9 | 06 | acronym_glossary_developer |
| `term_hermes_plugin` | plugin system (tools/hooks/providers; ≠ plugin_sdk) | 14 | 06 | acronym_glossary_developer |
| `term_agent_trajectory` | ShareGPT-format run trace | 9 | 06 | acronym_glossary_llm |
| `term_provider_routing` | OpenRouter underlying-provider selection | 7 | 09 | acronym_glossary_llm |
| `term_fallback_provider` | primary/aux provider failover chain | 8 | 09 | acronym_glossary_llm |
| `term_credential_pool` | multi-key rotation (≠ credential_stuffing) | 6 | 09 | acronym_glossary_systems |
| `term_pkce` | OAuth 2.1 PKCE auth flow | 12 | 09 | acronym_glossary_security |
| `term_messaging_gateway` | platform↔agent bridge (≠ api_gateway) | 30+ | 11 | acronym_glossary_systems |
| `term_dm_pairing` | gateway user-authorization handshake | 8 | 11 | acronym_glossary_systems |
| `term_silence_token` | `[SILENT]` intentional non-reply | 6 | 11 | acronym_glossary_workflows |
| `term_hermes_profile` | isolated agent instance (≠ auth_profile) | 16 | 04 | acronym_glossary_systems |
| `term_tirith` | pre-exec security scanner | 4 | 03 | acronym_glossary_security |
| `term_shadow_git_checkpoint` | rollback via shadow git repo | 5 | 03 | acronym_glossary_systems |
| `term_git_worktree_agents` | parallel agents via git worktrees | 6 | 03 | acronym_glossary_developer |
| `term_context_compression` | dual-threshold context compaction | 8 | 18 | acronym_glossary_llm |
| `term_nemotron` | NVIDIA Nemotron 3 Ultra model | 4 | 15 | acronym_glossary_llm |

> ~32 capture candidates (up from the 24-term hand-curated guess; +8 surfaced by the corpus scan,
> several of which the loose DB check had falsely marked "exists"). This is the **starting set** —
> each sub-plan's augmentation runs the authoritative per-page scan, finalizes the stub/full +
> capture-phase decision in its own Undigested Terms table, and VISUALLY confirms every DB match.
> Low-value product names (Camofox, Piper, NeuTTS, signal-cli, Baileys) are treated as link-only
> references inside notes, not standalone term captures, unless a sub-plan finds recurring conceptual use.

## Shared Validation Gates (8-GATE, applied per execution phase in every sub-plan)

G1-Format (`/tessellum-check-note-format`) · G2-Grounding (diff vs `inbox/hermes_agent_docs/` source) ·
G3-Density+Coverage · G4-CrossRef · **G5-Ghost (DB-verify every ref; redirect ghosts)** ·
**G6-Broken (`/tessellum-check-broken-links` → `/tessellum-fix-broken-links`)** · G7-BB-atomicity ·
**G8-Discoverability (each new note gets ≥1 inbound link from outside the folder; in-degree ≥1).**

## Pacing Rules

- Execute by sub-plan; commit per sub-plan (per-wave commits for the multi-agent runs).
- Dedup-before-create is intrinsic, not optional. Pilot 1 note → reindex → verify before fan-out.
- Multi-agent execution caps fan-out at ~30 agents/run; agents return data, the master writes
  serially where there is write-contention; embed the manifest in the workflow script (args unreliable).

## Summary Statistics

- Rendered pages: **174** · Estimated notes: **~233** · Sub-plans: **21** (several split a/b).
- BB mix (estimated from page classification): procedure ~45%, concept ~22%, model ~18%,
  navigation ~9%, argument/empirical ~6%.
- New term notes (data-driven corpus sweep starting set): **~32**; existing terms linked: **18**.

## Follow-up Recommendations

1. Author sub-plans in priority order; each gets full Steps 2–8 + augmentation + review.
2. After P1 lands, backfill cross-links from existing `repo_hermes_agent_*` notes → new doc notes (G8).
3. Run the **Finalization Phase (Wave F)** above once all 21 sub-plans land: CREATE `entry_hermes_agent_docs.md`,
   UPDATE the parent/sibling hubs (`entry_research_and_ai_hub`, `entry_platform_docs`, `entry_gen_ai_dev`,
   `entry_code_snippets_hermes_agent`, `entry_claude_code_docs`), reconcile glossaries, run G8 + broken-link sweep.
4. Consider a short `thought_` note comparing Hermes' docs-stated design vs the code-digestion findings.

## Source-Coverage Ledger (every rendered page → sub-plan; no orphans)

> Measured words/code from `inbox/hermes_agent_docs/`. `[SPLIT]` = exceeds a density cap
> (>2500w or >6 code blocks) → ≥2 notes. This guarantees complete coverage at master level; the
> sub-plan's own Section Coverage Map maps each page's H2/H3 to specific notes.

<!-- LEDGER_START -->
#### Sub-plan 01 Getting Started & Install
  - getting-started/nix-setup.md  (5482w, 44code) [SPLIT]
  - getting-started/quickstart.md  (2576w, 19code) [SPLIT]
  - getting-started/updating.md  (1708w, 21code) [SPLIT]
  - getting-started/installation.md  (1049w, 10code) [SPLIT]
  - getting-started/learning-path.md  (955w, 0code)
  - getting-started/termux.md  (923w, 19code) [SPLIT]
  - index.mdx  (894w, 2code)
  - user-stories.mdx  (6w, 0code)
#### Sub-plan 02 CLI, TUI & Configuration
  - user-guide/configuration.md  (14128w, 92code) [SPLIT]
  - user-guide/sessions.md  (3462w, 24code) [SPLIT]
  - user-guide/cli.md  (2802w, 21code) [SPLIT]
  - user-guide/tui.md  (2514w, 8code) [SPLIT]
  - user-guide/configuring-models.md  (1993w, 9code) [SPLIT]
#### Sub-plan 03 Deployment, Sandboxing & Security
  - user-guide/docker.md  (6013w, 36code) [SPLIT]
  - user-guide/security.md  (4577w, 26code) [SPLIT]
  - user-guide/windows-native.md  (3343w, 9code) [SPLIT]
  - user-guide/desktop.md  (3271w, 9code) [SPLIT]
  - user-guide/windows-wsl-quickstart.md  (2928w, 16code) [SPLIT]
  - user-guide/checkpoints-and-rollback.md  (1321w, 15code) [SPLIT]
  - user-guide/secrets/bitwarden.md  (1256w, 4code)
  - user-guide/managed-scope.md  (870w, 6code)
  - user-guide/git-worktrees.md  (803w, 7code) [SPLIT]
  - user-guide/secrets/index.md  (97w, 0code)
#### Sub-plan 04 Profiles & Multi-Profile Ops
  - user-guide/profile-distributions.md  (3043w, 29code) [SPLIT]
  - user-guide/multi-profile-gateways.md  (2113w, 23code) [SPLIT]
  - user-guide/profiles.md  (1881w, 21code) [SPLIT]
#### Sub-plan 05 Knowledge, Memory & Skills
  - user-guide/features/skills.md  (5194w, 43code) [SPLIT]
  - user-guide/features/memory-providers.md  (3407w, 18code) [SPLIT]
  - user-guide/features/honcho.md  (2505w, 5code) [SPLIT]
  - user-guide/features/curator.md  (2356w, 10code) [SPLIT]
  - user-guide/features/memory.md  (2103w, 11code) [SPLIT]
  - user-guide/features/tool-gateway.md  (1455w, 9code) [SPLIT]
  - user-guide/features/context-files.md  (1310w, 7code) [SPLIT]
  - user-guide/features/personality.md  (1200w, 9code) [SPLIT]
  - user-guide/features/tools.md  (975w, 9code) [SPLIT]
  - user-guide/skills/google-workspace.md  (868w, 12code) [SPLIT]
  - user-guide/features/context-references.md  (729w, 4code)
#### Sub-plan 06 Automation, Plugins & Multi-Agent
  - user-guide/features/kanban.md  (10308w, 29code) [SPLIT]
  - user-guide/features/hooks.md  (6903w, 62code) [SPLIT]
  - user-guide/features/cron.md  (3861w, 37code) [SPLIT]
  - user-guide/features/kanban-tutorial.md  (2840w, 12code) [SPLIT]
  - user-guide/features/plugins.md  (2802w, 10code) [SPLIT]
  - user-guide/features/built-in-plugins.md  (2589w, 9code) [SPLIT]
  - user-guide/features/delegation.md  (2007w, 11code) [SPLIT]
  - user-guide/features/code-execution.md  (1661w, 10code) [SPLIT]
  - user-guide/features/goals.md  (1601w, 5code)
  - user-guide/features/batch-processing.md  (1176w, 7code) [SPLIT]
#### Sub-plan 08 Media & Web Tools
  - user-guide/features/tts.md  (4341w, 20code) [SPLIT]
  - user-guide/features/browser.md  (4121w, 33code) [SPLIT]
  - user-guide/features/voice-mode.md  (2850w, 18code) [SPLIT]
  - user-guide/features/spotify.md  (2198w, 12code) [SPLIT]
  - user-guide/features/web-search.md  (2102w, 29code) [SPLIT]
  - user-guide/features/skins.md  (1642w, 6code)
  - user-guide/features/vision.md  (1606w, 8code) [SPLIT]
  - user-guide/features/kanban-worker-lanes.md  (1447w, 1code)
  - user-guide/features/lsp.md  (1392w, 5code)
  - user-guide/features/image-generation.md  (1309w, 9code) [SPLIT]
  - user-guide/features/x-search.md  (1153w, 2code)
  - user-guide/features/computer-use.md  (1088w, 4code)
  - user-guide/features/tool-search.md  (1044w, 4code)
  - user-guide/features/overview.md  (921w, 0code)
  - user-guide/features/deliverable-mode.md  (850w, 1code)
#### Sub-plan 09 Protocols & Provider Integration
  - user-guide/features/mcp.md  (3868w, 42code) [SPLIT]
  - user-guide/features/api-server.md  (2608w, 22code) [SPLIT]
  - user-guide/features/fallback-providers.md  (2582w, 18code) [SPLIT]
  - user-guide/features/credential-pools.md  (1351w, 12code) [SPLIT]
  - user-guide/features/acp.md  (1292w, 14code) [SPLIT]
  - user-guide/features/subscription-proxy.md  (865w, 11code) [SPLIT]
  - user-guide/features/provider-routing.md  (649w, 15code) [SPLIT]
#### Sub-plan 10 Dashboard & Runtimes
  - user-guide/features/web-dashboard.md  (9537w, 27code) [SPLIT]
  - user-guide/features/extending-the-dashboard.md  (5324w, 32code) [SPLIT]
  - user-guide/features/codex-app-server-runtime.md  (3959w, 14code) [SPLIT]
#### Sub-plan 11 Messaging: Team Chat
  - user-guide/messaging/telegram.md  (9147w, 56code) [SPLIT]
  - user-guide/messaging/discord.md  (6685w, 27code) [SPLIT]
  - user-guide/messaging/matrix.md  (5393w, 45code) [SPLIT]
  - user-guide/messaging/index.md  (4350w, 25code) [SPLIT]
  - user-guide/messaging/slack.md  (3626w, 23code) [SPLIT]
  - user-guide/messaging/google_chat.md  (2107w, 6code)
  - user-guide/messaging/mattermost.md  (1982w, 14code) [SPLIT]
  - user-guide/messaging/teams.md  (1343w, 14code) [SPLIT]
  - user-guide/messaging/teams-meetings.md  (935w, 12code) [SPLIT]
#### Sub-plan 12 Messaging: Consumer & Webhooks
  - user-guide/messaging/whatsapp-cloud.md  (3439w, 9code) [SPLIT]
  - user-guide/messaging/webhooks.md  (2756w, 17code) [SPLIT]
  - user-guide/messaging/open-webui.md  (1898w, 16code) [SPLIT]
  - user-guide/messaging/whatsapp.md  (1700w, 8code) [SPLIT]
  - user-guide/messaging/signal.md  (1504w, 7code) [SPLIT]
  - user-guide/messaging/line.md  (1258w, 8code) [SPLIT]
  - user-guide/messaging/homeassistant.md  (1227w, 12code) [SPLIT]
  - user-guide/messaging/email.md  (1173w, 4code)
  - user-guide/messaging/photon.md  (1123w, 11code) [SPLIT]
  - user-guide/messaging/msgraph-webhook.md  (1094w, 5code)
  - user-guide/messaging/ntfy.md  (1046w, 9code) [SPLIT]
  - user-guide/messaging/sms.md  (896w, 10code) [SPLIT]
  - user-guide/messaging/bluebubbles.md  (833w, 9code) [SPLIT]
  - user-guide/messaging/simplex.md  (738w, 7code) [SPLIT]
  - user-guide/messaging/raft.md  (480w, 2code)
#### Sub-plan 13 Messaging: Chinese Platforms
  - user-guide/messaging/feishu.md  (3934w, 21code) [SPLIT]
  - user-guide/messaging/weixin.md  (2657w, 7code) [SPLIT]
  - user-guide/messaging/wecom.md  (1862w, 7code) [SPLIT]
  - user-guide/messaging/dingtalk.md  (1649w, 12code) [SPLIT]
  - user-guide/messaging/yuanbao.md  (1451w, 14code) [SPLIT]
  - user-guide/messaging/wecom-callback.md  (952w, 4code)
  - user-guide/messaging/qqbot.md  (638w, 4code)
#### Sub-plan 14 Inference Providers & Integrations
  - integrations/providers.md  (9458w, 87code) [SPLIT]
  - integrations/nous-portal.md  (2030w, 14code) [SPLIT]
  - integrations/index.md  (929w, 1code)
#### Sub-plan 15 Guides: Providers & Setup
  - guides/azure-foundry.md  (2798w, 13code) [SPLIT]
  - guides/xai-grok-oauth.md  (1911w, 13code) [SPLIT]
  - guides/run-hermes-with-nous-portal.md  (1608w, 20code) [SPLIT]
  - guides/oauth-over-ssh.md  (1570w, 10code) [SPLIT]
  - guides/local-ollama-setup.md  (1567w, 19code) [SPLIT]
  - guides/google-gemini.md  (1443w, 18code) [SPLIT]
  - guides/local-llm-on-mac.md  (1380w, 11code) [SPLIT]
  - guides/minimax-oauth.md  (1066w, 14code) [SPLIT]
  - guides/aws-bedrock.md  (712w, 7code) [SPLIT]
  - guides/run-nemotron-3-ultra-free.md  (668w, 7code) [SPLIT]
#### Sub-plan 16 Guides: Automation & Bots
  - guides/webhook-github-pr-review.md  (2018w, 12code) [SPLIT]
  - guides/team-telegram-assistant.md  (1983w, 29code) [SPLIT]
  - guides/daily-briefing-bot.md  (1586w, 20code) [SPLIT]
  - guides/cron-script-only.md  (1525w, 7code) [SPLIT]
  - guides/automate-with-cron.md  (1460w, 11code) [SPLIT]
  - guides/delegation-patterns.md  (1438w, 8code) [SPLIT]
  - guides/cron-troubleshooting.md  (1414w, 9code) [SPLIT]
  - guides/github-pr-review-agent.md  (1344w, 17code) [SPLIT]
  - guides/pipe-script-output.md  (1256w, 7code) [SPLIT]
  - guides/operate-teams-meeting-pipeline.md  (1152w, 17code) [SPLIT]
#### Sub-plan 17 Guides: Build & Extend
  - guides/build-a-hermes-plugin.md  (6087w, 57code) [SPLIT]
  - guides/automation-blueprints.md  (2535w, 21code) [SPLIT]
  - guides/migrate-from-openclaw.md  (1949w, 2code)
  - guides/tips.md  (1806w, 6code)
  - guides/use-mcp-with-hermes.md  (1693w, 33code) [SPLIT]
  - guides/use-voice-mode-with-hermes.md  (1499w, 24code) [SPLIT]
  - guides/work-with-skills.md  (1310w, 16code) [SPLIT]
  - guides/python-library.md  (1237w, 15code) [SPLIT]
  - guides/microsoft-graph-app-registration.md  (1160w, 5code)
  - guides/use-soul-with-hermes.md  (1090w, 10code) [SPLIT]
#### Sub-plan 18 Developer: Internals
  - developer-guide/plugin-llm-access.md  (2219w, 10code) [SPLIT]
  - developer-guide/context-compression-and-caching.md  (2049w, 14code) [SPLIT]
  - developer-guide/cron-internals.md  (1820w, 6code)
  - developer-guide/prompt-assembly.md  (1777w, 5code)
  - developer-guide/architecture.md  (1622w, 6code)
  - developer-guide/session-storage.md  (1555w, 17code) [SPLIT]
  - developer-guide/gateway-internals.md  (1526w, 6code)
  - developer-guide/agent-loop.md  (1361w, 5code)
  - developer-guide/tools-runtime.md  (1247w, 4code)
  - developer-guide/browser-supervisor.md  (1135w, 2code)
  - developer-guide/provider-runtime.md  (1135w, 0code)
  - developer-guide/trajectory-format.md  (1012w, 8code) [SPLIT]
  - developer-guide/acp-internals.md  (672w, 3code)
#### Sub-plan 19 Developer: Extending & Plugin Authoring
  - developer-guide/adding-platform-adapters.md  (3454w, 20code) [SPLIT]
  - developer-guide/creating-skills.md  (2753w, 21code) [SPLIT]
  - developer-guide/adding-providers.md  (2193w, 6code)
  - developer-guide/model-provider-plugin.md  (1600w, 9code) [SPLIT]
  - developer-guide/web-search-provider-plugin.md  (1366w, 9code) [SPLIT]
  - developer-guide/contributing.md  (1316w, 13code) [SPLIT]
  - developer-guide/image-gen-provider-plugin.md  (1302w, 7code) [SPLIT]
  - developer-guide/memory-provider-plugin.md  (1137w, 11code) [SPLIT]
  - developer-guide/video-gen-provider-plugin.md  (1000w, 4code)
  - developer-guide/context-engine-plugin.md  (847w, 9code) [SPLIT]
  - developer-guide/programmatic-integration.md  (809w, 3code)
  - developer-guide/adding-tools.md  (796w, 5code)
  - developer-guide/extending-the-cli.md  (767w, 8code) [SPLIT]
#### Sub-plan 20 Reference: Commands
  - reference/cli-commands.md  (10819w, 73code) [SPLIT]
  - reference/slash-commands.md  (3598w, 4code) [SPLIT]
  - reference/profile-commands.md  (2358w, 31code) [SPLIT]
#### Sub-plan 21 Reference: Env, Tools, Catalogs & FAQ
  - reference/environment-variables.md  (9291w, 2code) [SPLIT]
  - reference/faq.md  (4699w, 44code) [SPLIT]
  - reference/tools-reference.md  (3235w, 0code) [SPLIT]
  - reference/optional-skills-catalog.md  (2911w, 3code) [SPLIT]
  - reference/toolsets-reference.md  (1493w, 6code)
  - reference/skills-catalog.md  (1420w, 0code)
  - reference/mcp-config-reference.md  (1044w, 15code) [SPLIT]
  - reference/model-catalog.md  (500w, 5code)
  - reference/automation-blueprints-catalog.mdx  (189w, 0code)
<!-- LEDGER_END -->

**Source**: `inbox/hermes_agent_docs/` (mirror of `NousResearch/hermes-agent` `website/docs/`, commit `c253b07`, re-synced 2026-06-19; previously `95715dc`) · live `https://hermes-agent.nousresearch.com/docs/`
**Last Updated**: 2026-06-19 (mirror re-synced `95715dc`→`c253b07`; ledger + page accounting re-measured)
**Status**: Approved 2026-06-14 (re-synced 2026-06-19) — authoring sub-plans (P1 first)

## Pilot + Gate Calibration (2026-06-19)

- **Pilot note (hand-built):** `resources/documentation/hermes_agent/hermes_learning_path.md` (SP01 Note 4, navigation — chosen for max cross-ref stress: 33 links). Built from `inbox/hermes_agent_docs/getting-started/learning-path.md` (955w source).
- **Gate config (calibrated, `scripts/digest_note_gate.sh`):** `REQ_SECTIONS="## Overview|## Related Notes"`, `ORDER_BEFORE="## Overview"`, `ORDER_AFTER="## Related Notes"`, `BB_ALLOW` adds `navigation`, `MIN_LINKS=8`, `XREF_SECTION="## Related Notes"`, `REQUIRE_SOURCE_URL=1`, `SIBLING_PREFIX="hermes_"`, `EXEMPT_SLUGS=<owned in-flight term captures per wave>`. Footer is bold `**Source**`/`**Last Updated**`/`**Status**` (NOT an H2) per the `cc_*.md` anchor.
- **Known-bad calibration:** a version with `## Related Notes` stripped correctly FAILed (coverage + crossref<8). Gate rejects placeholder/dropped-section notes.
- **Format anchor:** `resources/documentation/claude_code/cc_admin_enforcement_controls.md` (YAML field order + bold-footer convention).

## Execution Report (2026-06-19/20)

| Metric | Value |
|---|---|
| Doc notes created | 226 / 226 planned |
| Term notes captured (owned, Pattern B) | 32 / 32 (each with glossary row + reciprocal backlinks) |
| Waves | P1 (62 docs + 15 terms) · P2 (85 docs + 15 terms) · P3 (79 docs + 2 terms) · F (finalization) |
| Sub-plans passed | 26 / 26 (0 still-failing across all waves) |
| Pilot | hermes_learning_path (hand-built, gate-calibrated PASS; known-bad FAIL) |
| Gate | scripts/digest_note_gate.sh — full corpus ALL PASS (8 term / 5 repo / 10 snippet / 10 doc cross-ref floor; bb/density/format/order) |
| Ghost references from new notes | 0 (vault-wide) |
| Broken links | 0 |
| Graph-island notes (G8, 0 outside-inbound) | 0 (entry point provides 226 inbound links) |
| Entry point | CREATE entry_hermes_agent_docs.md (226 rows, reconciled planned==on-disk) |
| Hubs updated | entry_platform_docs, entry_gen_ai_dev, entry_research_and_ai_hub + cross-links to entry_code_snippets_hermes_agent / entry_claude_code_docs |
| Glossary reconciliation | 32/32 owned terms have acronym_glossary_* rows |
| Agents (capture + validate + fix across waves) | ~290 |

## Status

Execution complete. Master + all 26 sub-plans move from `ready`/`approved` → `completed`.
