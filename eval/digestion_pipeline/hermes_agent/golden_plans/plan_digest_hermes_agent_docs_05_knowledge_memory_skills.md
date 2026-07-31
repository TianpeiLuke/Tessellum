---
title: Hermes Agent Docs Digestion — Sub-Plan 05 — Knowledge, Memory & Skills
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/skills.md
  - user-guide/features/memory-providers.md
  - user-guide/features/curator.md
  - user-guide/features/honcho.md
  - user-guide/features/memory.md
  - user-guide/features/tool-gateway.md
  - user-guide/features/context-files.md
  - user-guide/features/personality.md
  - user-guide/features/tools.md
  - user-guide/skills/google-workspace.md
  - user-guide/features/context-references.md
---

# Sub-Plan 05: Knowledge, Memory & Skills

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP05's note
> filenames/BBs/coverage are defined.

## Scope

The agent's **knowledge surface**: what tools it can call, the skill system (on-demand knowledge
documents + agent-created procedural memory + the Skills Hub), the curator that maintains those skills,
persistent built-in memory (MEMORY.md / USER.md), the 9 external memory-provider plugins (Honcho et al.),
the context files (SOUL.md / AGENTS.md) and inline `@`-references that shape every prompt, and personality
customization. Source = 11 mirrored pages in `inbox/hermes_agent_docs/` (all substantive). **P1 /
foundational** — `skills`, `tool-gateway`, `memory`, and `soul`/`agents` concepts are referenced by nearly
every downstream sub-plan; SP05 OWNS the term captures for those concepts (see Undigested Terms Plan).
Downstream sub-plans link back to `hermes_skills_system`, `hermes_tool_gateway`, `hermes_persistent_memory`,
`hermes_context_files`, and the new `term_tool_gateway` / `term_soul_md` / `term_agents_md` /
`term_progressive_disclosure` / `term_skills_hub` / `term_skill_curator` / `term_honcho` term notes.

## Content Strategy

- **One BB per note.** `skills.md` (5194w) mixes a concept arc (what skills are + progressive disclosure
  + external dirs), a format/model arc (SKILL.md schema + bundles + media-delivery directives), and a
  procedural arc (agent-managed `skill_manage` + Skills Hub install/security/taps/reset) → split into 3.
  `memory-providers.md` (3407w) mixes the provider-system concept + the flagship Honcho provider vs the
  8-provider catalog → split into 2 (Honcho fused with `honcho.md`'s deep architecture; the rest = catalog).
  All other 9 pages → 1 note each.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the per-tool
  feature pages (browser/tts/vision/web-search SP08, code-execution/delegation SP06, MCP SP09), the
  config blocks each setting lives in (`config.yaml` skill/memory/security settings → SP02), the provider
  catalog (SP09/SP14), session search internals (SP02 `hermes_session_search_storage`), context
  compression internals (SP18), and the Developer-Guide creating-skills / memory-provider-plugin authoring
  pages (SP19). The Tool Gateway billing/Portal home is SP14 (`term_nous_portal`) — SP05 captures the
  TOOL concept, links the billing term.
- **Collision (augment): `term_agentspace` / `term_agentspaces` are Google Agentspace — UNRELATED to the
  `AGENTS.md` context file** (master caution list, confirmed by reading both). `term_progressive_summarization`
  is the context-compaction concept — UNRELATED to `progressive disclosure` (skill loading). `term_api_gateway`
  / `term_mcp_gateway` / `term_agentcore_gateway` are different gateways — UNRELATED to the Nous **Tool**
  Gateway tool-proxy. All seven owned slugs are genuinely new (see Collision & Dedup Audit).

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — wc)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/skills.md | 5194 | 43 | MIXED concept+model+procedure | 3 (split) |
| user-guide/features/memory-providers.md | 3407 | 18 | MIXED concept+model | 2 (split) |
| user-guide/features/curator.md | 2356 | 10 | procedure | 1 |
| user-guide/features/honcho.md | 2505 | 5 | model | 1 (fused into Note 7) |
| user-guide/features/memory.md | 2103 | 11 | concept | 1 |
| user-guide/features/tool-gateway.md | 1455 | 9 | concept | 1 |
| user-guide/features/context-files.md | 1310 | 7 | procedure | 1 |
| user-guide/features/personality.md | 1200 | 9 | procedure | 1 |
| user-guide/features/tools.md | 975 | 9 | model | 1 |
| user-guide/skills/google-workspace.md | 868 | 12 | procedure | 1 |
| user-guide/features/context-references.md | 729 | 4 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **13 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_tools_toolsets.md` | model | tools §Available Tools (categories table, Honcho-is-a-plugin note), §Using Toolsets, §Terminal Backends (overview + per-backend), §Background Process Management, §Sudo Support | ~1000 | The tool registry model: high-level tool categories (web/x-search/terminal/browser/media/orchestration/memory/automation/integrations), how toolsets enable/disable tools per platform, the 6 terminal backends summary, `terminal(background=true)`+`process` tool, sudo prompting. Links the authoritative SP21 references. |
| 2 | `hermes_tool_gateway.md` | concept | tool-gateway ALL sections (What's included, Why, Get started, Eligibility, Mix and match, Individual image models, Configuration reference, FAQ) | ~1300 | The Nous Tool Gateway: one paid Portal subscription routes web-search/image-gen/TTS/cloud-browser through Nous infra with no extra API keys; enable via `setup --portal`/`hermes model`/`hermes tools`; per-tool `use_gateway` flag + precedence; 9 image models; free tool pool; self-hosted overrides. |
| 3 | `hermes_skills_system.md` | concept | skills §intro (on-demand docs, progressive disclosure, agentskills.io), §Starting with a blank slate (`--no-skills`/opt-out marker), §Using Skills (slash commands, NL), §Progressive Disclosure (3 levels), §Secure Setup on Load (required_environment_variables + Skill Config Settings), §External Skill Directories | ~1500 | What a Hermes skill IS: on-demand knowledge documents loaded via progressive disclosure (Level 0/1/2), agentskills.io-compatible, living in `~/.hermes/skills/`; blank-slate opt-out; auto-slash-command invocation; secure on-load env-var setup; external skill directories with local precedence. |
| 4 | `hermes_skill_md_format_bundles.md` | model | skills §SKILL.md Format (frontmatter, platform-specific), §Skill output and media delivery (`[[audio_as_voice]]`, `[[as_document]]`), §Conditional Activation (fallback/requires toolsets/tools), §Skill Directory Structure, §Skill Bundles (quick example, YAML schema, managing, behavior, when-to-use) | ~1400 | The SKILL.md file model: YAML frontmatter (name/description/version/platforms/metadata.hermes.*), platform restriction, media-delivery directives, conditional-activation fields, the on-disk skill package layout (references/templates/scripts/assets/.hub), and skill bundles (YAML alias grouping several skills under one slash command). |
| 5 | `hermes_skills_hub_agent_managed.md` | procedure | skills §Agent-Managed Skills (skill_manage actions, when, write_approval gate), §Skills Hub (commands, 9 supported sources, security scanning + `--force`, trust levels, update lifecycle, publishing a tap, non-default paths, individual installs), §Bundled skill updates (`hermes skills reset`), §Slash commands | ~1600 | Managing the skill library: the agent's `skill_manage` tool (create/patch/edit/delete) as procedural memory + the `skills.write_approval` staging gate; the Skills Hub (browse/search/install across official/skills-sh/well-known/github/clawhub/lobehub/browse-sh/url), security scanner + trust levels + `--force`, custom taps, and `hermes skills reset` re-baselining. |
| 6 | `hermes_persistent_memory.md` | concept | memory ALL sections (How It Works MEMORY/USER, system-prompt rendering + frozen snapshot, memory tool actions, substring matching, two targets, what to save/skip, capacity + full-behavior, duplicate prevention, security scanning, session search pointer, configuration, write_approval, skills.write_approval pointer, external providers pointer) | ~1500 | Built-in persistent memory: the bounded, agent-curated MEMORY.md (2200 char) + USER.md (1375 char) injected as a frozen system-prompt snapshot at session start; `memory` add/replace/remove with substring matching; what to save vs skip; capacity-full consolidation; injection/exfil security scan; `memory.write_approval` gate. |
| 7 | `hermes_memory_providers_honcho.md` | model | memory-providers §intro (8 providers, one-active), §Quick Start, §How It Works (6-step lifecycle), §Honcho (full provider entry) + honcho.md ALL sections (architecture, two-layer injection, cold/warm, three knobs, dialectic depth, prewarm, query-adaptive, config reference, observation directional/unified, gateway identity mapping, tools, CLI, migration) | ~1950 | The external memory-provider system + the flagship Honcho provider: how a provider augments built-in memory (inject/prefetch/sync/extract/mirror/tools); Honcho's AI-native dialectic user modeling — two-layer (base + dialectic) context injection, cold/warm prompt selection, `contextCadence`/`dialecticCadence`/`dialecticDepth` orthogonal knobs, directional-vs-unified observation, 5 tools, `hermes honcho` CLI. |
| 8 | `hermes_memory_provider_catalog.md` | model | memory-providers §Available Providers (OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory, Memori — each: best-for/requires/storage/cost/tools/config/features), §Provider Comparison table, §Profile Isolation, §Building a Memory Provider pointer | ~1600 | Catalog of the remaining 8 external memory providers (OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory, Memori): per-provider storage/cost/tools/unique-feature, the comparison matrix, per-profile data isolation by storage class, and where to author a custom provider (SP19). |
| 9 | `hermes_skill_curator.md` | procedure | curator ALL sections (what it is, how it runs, configuration + aux model, CLI, backups/rollback, what "agent-created" means, pinning, usage telemetry, per-run reports, restoring, disabling) | ~1500 | The background skill curator: tracks view/use/patch telemetry in `.usage.json`, moves agent-created skills `active→stale→archived`, runs an inactivity-gated aux-model LLM review that consolidates/patches/archives; config defaults, `hermes curator` CLI, tar.gz backups + rollback, pinning + protected built-ins, what counts as agent-created. |
| 10 | `hermes_context_files.md` | procedure | context-files ALL sections (supported files + priority, AGENTS.md, progressive subdirectory discovery, example, SOUL.md pointer, .cursorrules, how loaded at startup + during session, security prompt-injection protection, size limits, tips, per-subdir context) | ~1300 | Project context files: the first-match priority chain (`.hermes.md`→`AGENTS.md`→`CLAUDE.md`→`.cursorrules`) plus always-loaded global `SOUL.md`; AGENTS.md progressive subdirectory discovery; how files are scanned/truncated/injected at startup and during a session; prompt-injection scanning and size limits. |
| 11 | `hermes_context_references.md` | procedure | context-references ALL sections (supported `@`-refs, usage, CLI tab completion, line ranges, size limits, security sensitive-path/traversal/binary, platform availability, interaction with compression, common patterns, error handling) | ~900 | Inline `@`-references: `@file`/`@folder`/`@diff`/`@staged`/`@git:N`/`@url` expand content into a message under `--- Attached Context ---`; CLI tab completion, line ranges, soft/hard size limits, sensitive-path + traversal + binary blocking, CLI-only availability, compression interaction. |
| 12 | `hermes_personality_soul.md` | procedure | personality ALL sections (SOUL.md as identity, how it works now, why, where to edit, what goes in, good content, what Hermes injects, security scan, SOUL vs AGENTS, SOUL vs /personality, built-in personalities, switching, custom personalities, recommended workflow, prompt stack, CLI appearance vs conversational) | ~1300 | Customizing personality: `SOUL.md` as slot-#1 system-prompt identity loaded only from `HERMES_HOME`, what belongs in it vs AGENTS.md, the 14 built-in `/personality` presets + custom `agent.personalities`, the full prompt stack ordering, and SOUL (voice) vs skin (terminal appearance). |
| 13 | `hermes_google_workspace_skill.md` | procedure | google-workspace ALL sections (setup, Gmail search/read/send/custom-from/reply/labels, Calendar, Drive, Sheets, Docs, Contacts, output format, troubleshooting) | ~900 | The bundled Google Workspace skill: OAuth2-authenticated `$GAPI` CLI for Gmail (search/get/send/reply/labels, custom `--from` display name), Calendar (list/create with required timezone/delete), Drive search, Sheets read/write/append, Docs, Contacts; agent-driven setup + troubleshooting. |

**SP05 totals:** 13 notes · procedure 6 · concept 3 · model 4.
11 source pages digested (all substantive), 0 skipped. SP05 OWNS 7 new term captures (see Undigested Terms Plan).

## Summary Statistics & Building Block Distribution

- Notes: 13 · procedure 6 · concept 3 · model 4.
- Source: 11 digested pages (~22.1K words) → ~17.7K words of notes (modest compression via link-outs to feature pages and other SPs).
- BB mix: procedure 46%, concept 23%, model 31%.

## Section Coverage Map

```
tools.md (975w) ── ALL sections ────────────────────────────── → Note 1 (per-tool pages→SP06/08/09; refs→SP21; gateway→Note 2; backends config→SP02)
tool-gateway.md (1455w) ── ALL sections ─────────────────────── → Note 2 (Portal billing→SP14; image models page→SP08; tts/browser/web→SP08)
skills.md (5194w)
├── intro (on-demand docs / progressive disclosure / agentskills.io) → Note 3 (+OWN term_progressive_disclosure)
├── Starting with a blank slate (--no-skills / opt-out marker) ── → Note 3 (profiles→SP04)
├── Using Skills (slash commands / NL) ───────────────────────── → Note 3 (CLI slash→SP02; ref catalogs→SP21)
├── Progressive Disclosure (Level 0/1/2) ─────────────────────── → Note 3
├── Secure Setup on Load (required_environment_variables / Skill Config Settings) → Note 3 (config→SP02; security→SP03)
├── External Skill Directories (external_dirs / how it works / example) → Note 3
├── SKILL.md Format (frontmatter / platform-specific) ────────── → Note 4
├── Skill output and media delivery ([[audio_as_voice]] / [[as_document]]) → Note 4 (gateway delivery→SP11-13)
├── Conditional Activation (fallback/requires toolsets/tools) ── → Note 4
├── Skill Directory Structure ────────────────────────────────── → Note 4
├── Skill Bundles (quick example / YAML schema / managing / behavior / when) → Note 4
├── Agent-Managed Skills (skill_manage actions / when / write_approval gate) → Note 5 (memory write_approval→Note 6; config guard→SP02)
├── Skills Hub (commands / 9 sources / security / trust / update / publishing tap / paths / individual) → Note 5 (+OWN term_skills_hub)
├── Bundled skill updates (hermes skills reset / origin hash) ── → Note 5
└── Slash commands (inside chat) ─────────────────────────────── → Note 5
memory-providers.md (3407w)
├── intro (8 providers / one-active) / Quick Start / How It Works (6 steps) → Note 7 (+OWN term_honcho)
├── Honcho (full provider entry: tools/architecture/knobs/config/multi-peer/observation) → Note 7 (fused w/ honcho.md)
├── OpenViking / Mem0 / Hindsight / Holographic / RetainDB / ByteRover / Supermemory / Memori → Note 8
├── Provider Comparison (matrix) ─────────────────────────────── → Note 8
├── Profile Isolation ────────────────────────────────────────── → Note 8 (profiles→SP04)
└── Building a Memory Provider (pointer) ─────────────────────── → Note 8 (authoring→SP19)
honcho.md (2505w) ── ALL sections (what adds / setup / architecture / observation / tools / CLI / migrate) → Note 7 (fused with memory-providers Honcho entry)
curator.md (2356w) ── ALL sections ──────────────────────────── → Note 9 (skills self-improvement→Note 5; memory parallel review→Note 6; aux model→SP02; ref catalog→SP21)
memory.md (2103w)
├── How It Works / system-prompt rendering / frozen snapshot / memory tool actions / substring matching → Note 6
├── Two Targets / What to Save vs Skip / Capacity Management / full behavior / duplicate prevention / security scanning → Note 6
├── Session Search (pointer) ─────────────────────────────────── → Note 6 (full model→SP02 hermes_session_search_storage)
├── Configuration / Controlling memory writes (write_approval) ── → Note 6 (config→SP02)
├── Controlling skill writes (skills.write_approval) ─────────── → Note 6 (full→Note 5)
└── External Memory Providers (pointer) ──────────────────────── → Note 6 (full→Notes 7/8)
context-files.md (1310w) ── ALL sections ────────────────────── → Note 10 (+OWN term_agents_md; SOUL detail→Note 12; security→SP03; config→SP02)
context-references.md (729w) ── ALL sections ─────────────────── → Note 11 (compression→SP18; web_extract tool→SP08)
personality.md (1200w) ── ALL sections ──────────────────────── → Note 12 (+OWN term_soul_md; skins→SP08; context files→Note 10; SOUL guide→SP17)
skills/google-workspace.md (868w) ── ALL sections ───────────── → Note 13 (skills system→Note 3; ref catalogs→SP21)
```

No source H2/H3 orphaned. All 11 pages fully covered; feature-page detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| skills.md (5194w, 43 code, MIXED) | Note 3 (skills system + progressive disclosure, concept) + Note 4 (SKILL.md format + bundles + media-delivery, model) + Note 5 (skills-hub + agent-managed + reset, procedure) | >4000w → 3 notes; three distinct BBs — the *concept* of a skill, the SKILL.md *file model*, and the *procedures* for creating/installing/maintaining skills. Each cluster keeps ≤6 curated code blocks from the 43 source blocks. |
| memory-providers.md (3407w, 18 code, MIXED) | Note 7 (provider-system concept + Honcho, fused with honcho.md, model) + Note 8 (the other 8 providers catalog, model) | >2500w; the flagship Honcho provider has its own dedicated `honcho.md` page (2505w) — fusing the two Honcho sources into Note 7 keeps the deep dialectic-architecture content atomic and avoids a thin honcho.md note, while Note 8 is the comparison catalog of the remaining providers. The split is what keeps Note 7 within caps despite honcho.md crossing 2500w (see Density Re-Assessment). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note / owned term | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_tool_gateway` (Nous Tool Gateway) | `term_api_gateway`, `term_mcp_gateway`, `term_agentcore_gateway`, `term_nat_gateway` (all active) | **NOT a dup** — those are network/MCP/AWS gateways; this is the Nous managed **tool-execution proxy** (web/image/tts/browser) — different concept (master caution: `messaging gateway ≠ api_gateway` family) | CAPTURE `term_tool_gateway`; LINK `term_mcp_gateway` as a related sibling-gateway. |
| `term_soul_md` (SOUL.md persona file) | none substantive (`term_persona`, `term_system_prompt` MISSING) | **NEW** — no vault note covers the SOUL.md identity file | CAPTURE; LINK `term_persona`. |
| `term_agents_md` (AGENTS.md context file) | `term_agentspace`, `term_agentspaces` (active) | **NOT a dup** — those are Google **Agentspace** (enterprise agent platform); `AGENTS.md` is a project context file (master caution: `AGENTS.md ≠ term_agentspace`, confirmed by reading both) | CAPTURE `term_agents_md`; do NOT link the unrelated Agentspace terms. |
| `term_progressive_disclosure` (on-demand skill loading) | `term_progressive_summarization` (active) | **NOT a dup** — that is context-compaction; this is the Level-0/1/2 lazy skill-loading pattern (master caution: `progressive disclosure ≠ term_progressive_summarization`) | CAPTURE `term_progressive_disclosure`; do NOT link the unrelated summarization term. |
| `term_skill_curator` (background skill maintenance loop) | `term_curator` MISSING; no curator term/doc note | **NEW** | CAPTURE; LINK `term_skills`, `term_self_evolving_agent`. |
| `term_honcho` (AI-native memory provider) | none (`%honcho%` returns 0 in term_dictionary AND documentation) | **NEW** | CAPTURE; LINK `term_agentic_memory`, `term_knowledge_graph`. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (all LIKE hits are false-positives confirmed by reading the
notes / per the master caution list). New `hermes_agent/` folder → no doc-doc collisions (intra-series
links resolve at finalization, G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19 (user directive — supersedes ALL prior floors):** each note's `## Related Notes`
> carries **four COUNTED groups**, all relevancy-selected to that note's actual content, each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   modules that implement what the doc note documents),
>   corpus whose CODE this note documents). **This is now a COUNTED floor (raised from the prior 8 and from "bonus").**
> - **≥10 documentation notes** (`../../documentation/`, sibling `hermes_*` in this series + analogous
>   `claude_code/cc_*` agent-tool docs + other relevant existing docs).
>
> The prior floor was ≥8 term + ≥5 code-repo + ≥10 doc with snippets labeled "bonus, not counted"; the snippet group
> is **NO LONGER a bonus group** — it is promoted to a counted floor and raised to **≥10**. Relevancy first, never pad.
>
> **All term IDs (excluding the 7 SP05-owned, captured Phase 0), all repo IDs, and all snippet IDs below are
> Intra-series doc links (sibling `hermes_*`) resolve at finalization (G5/G8) — allowed un-verified now. The 7
> SP05-owned new terms are captured in Phase 0 BEFORE the notes that link them (they DO count to the floor for SP05's
> own notes since SP05 captures them first). Forward-ref terms owned by OTHER SPs (`term_nous_portal`→SP14,
> `term_voice_mode`/`term_text_to_speech`/`term_browser_automation`→SP08, `term_context_compression`→SP18) are
> ADDITIONAL (+fin), NOT counted to the floor. The 13 source-code repo notes are: repo_hermes_agent,
> repo_hermes_agent_agent_core, repo_hermes_agent_cli, repo_hermes_agent_gateway_messaging, repo_hermes_agent_mcp_toolsets,
> repo_hermes_agent_tools, repo_hermes_agent_skills, repo_hermes_agent_plugins, repo_hermes_agent_providers_adapters,
> repo_hermes_agent_cron, repo_hermes_agent_acp, repo_hermes_agent_trajectory_research, repo_hermes_agent_tui_gateway.

**Note 1 `hermes_tools_toolsets`** (model)
- Terms (8): term_agent_harness, term_autonomous_coding_agents, term_function_calling, term_agent_orchestration, term_sandbox_backend, term_docker, term_mcp, term_skills, term_multi_agent_systems — relevance: tools are the function-calling surface; toolsets gate them per platform; terminal backends (docker/ssh/singularity/modal/daytona) + MCP server tools + skills are tool categories. (+fin: term_tool_gateway[own], term_browser_automation)
- Code-Repos (5): repo_hermes_agent_tools — the `tools/` package that defines the entire built-in tool registry (terminal/process/read_file/patch/web/browser/media), the exact functions this page's category table enumerates; repo_hermes_agent_mcp_toolsets — toolset materialization + per-platform enable/disable + dynamic `mcp-<server>` toolsets, the "Using Toolsets" section's machinery; repo_hermes_agent_cli — `hermes chat --toolsets`, `hermes tools`, `hermes config set terminal.backend` commands this page invokes; repo_hermes_agent_agent_core — the terminal-backend execution + background-process (`process` tool) lifecycle and Docker persistent-container routing; repo_hermes_agent — the top-level package wiring tools into the agent loop and the config.yaml `terminal:` block.
- Docs (10): hermes_tool_gateway — the gateway routes a subset of these tool categories through Nous; hermes_skills_system — `skills` is a tool category and a toolset; hermes_persistent_memory — `memory`/`session_search` tool categories; hermes_context_references — `web_extract` tool is referenced by `@url`; hermes_skills_hub_agent_managed — `skill_manage` is a tool; cc_built_in_tools — Claude Code's analogous built-in tool catalog; cc_tools_catalog — analogous tool reference; cc_mcp_overview — analogous MCP-tool integration; cc_execution_tool_behavior — analogous terminal/execution tool behavior; cc_sandbox_modes — analogous sandboxed-execution backends (parallels docker/ssh).
- Snippets (10): tools_registry, toolsets_definitions, toolsets_materialize, toolset_distributions, tools_environments_docker, tools_environments_local, tools_environments_ssh, tools_terminal_exec, tools_terminal_session, tools_process_register, cli_tools_config — relevance: the tool registry, toolset materialization/distributions, the docker/local/ssh terminal backends this page's table enumerates, terminal exec + session + background-process tools, and the `hermes tools`/`terminal.backend` CLI config code this page describes.

**Note 2 `hermes_tool_gateway`** (concept) — OWNS `term_tool_gateway`
- Terms (8): term_tool_gateway[own], term_oauth_token, term_authentication, term_function_calling, term_multimodal, term_computer_vision, term_provider_plugin, term_autonomous_coding_agents — relevance: the gateway routes tool calls (web/image/tts/browser) through Nous via Portal OAuth; vision/multimodal tools and provider auth are what it fronts; `use_gateway` is per-tool. (+fin: term_nous_portal[SP14], term_text_to_speech[SP08], term_browser_automation[SP08])
- Code-Repos (5): repo_hermes_agent_tools — the web/image/tts/browser tools and their `use_gateway` flag that route through the gateway; repo_hermes_agent_providers_adapters — the provider/backend adapters (Firecrawl/FAL/OpenAI/Browser Use) the gateway fronts and the Nous-managed backend routing; repo_hermes_agent_cli — `hermes setup --portal`, `hermes model`, `hermes tools`, `hermes portal info/tools`, `hermes status` commands; repo_hermes_agent_gateway_messaging — "operates at the tool-execution layer" so every messaging platform benefits transparently; repo_hermes_agent — top-level `TOOL_GATEWAY_*` env handling + Portal OAuth wiring + config.yaml per-tool blocks.
- Docs (10): hermes_tools_toolsets — the tools the gateway fronts; hermes_skills_system — skills can declare fallbacks when a gateway tool is absent; hermes_skill_curator — aux-model routing parallel; hermes_memory_providers_honcho — provider-plugin sibling using Nous infra; hermes_persistent_memory — Nous-account context; cc_llm_gateway — Claude Code's analogous gateway abstraction; cc_llm_gateway_litellm — analogous gateway proxy implementation; cc_proxy_and_gateway_config — analogous proxy/gateway config; cc_authentication — analogous auth/OAuth flow; cc_mcp_overview — analogous external-service tool routing.
- Snippets (10): tools_web_tools, tools_image_gen, tools_video_gen, tools_tts_routing, tools_browser_navigate, plugins_provider_nous, plugins_image_gen_dispatch, plugins_browser_dispatch, tools_registry, cli_tools_config — relevance: the web/image/video/tts/browser tool dispatch the gateway fronts, the Nous provider plugin + image/browser provider dispatch routing, the tool registry the `use_gateway` flag is read against, and the `hermes tools` config code this page documents.

**Note 3 `hermes_skills_system`** (concept) — OWNS `term_progressive_disclosure`
- Terms (8): term_progressive_disclosure[own], term_skills, term_skill_manifest, term_autonomous_coding_agents, term_agent_harness, term_context_window, term_self_evolving_agent, term_function_calling — relevance: skills are on-demand knowledge docs loaded via progressive disclosure (Level 0/1/2) to save context-window tokens; agentskills.io manifest format; self-improvement creates them. (+fin: term_skills_hub[own], term_skill_curator[own])
- Code-Repos (5): repo_hermes_agent_skills — the `skills/` package implementing skill discovery, the `~/.hermes/skills/` source-of-truth scan, `skills_list`/`skill_view` Level-0/1/2 loaders, external_dirs scanning, and the `.no-bundled-skills` opt-out marker; repo_hermes_agent_agent_core — the system-prompt skill-index snapshot and required-env-var secure-setup-on-load injection; repo_hermes_agent_cli — `hermes skills opt-out/opt-in`, `hermes profile create --no-skills`, `hermes chat --toolsets skills` commands; repo_hermes_agent_tools — the `skills` toolset + `skill_view`/`skills_list` tool surface; repo_hermes_agent — top-level skill config wiring (`skills.external_dirs`, `skills.config`) into config.yaml.
- Docs (10): hermes_skill_md_format_bundles — the SKILL.md file model this concept loads; hermes_skills_hub_agent_managed — how skills are installed/created; hermes_skill_curator — how agent-created skills are maintained; hermes_google_workspace_skill — a concrete bundled skill; hermes_persistent_memory — skills are procedural memory alongside MEMORY.md; cc_skills_overview — Claude Code's analogous skill concept; cc_skill_invocation_and_lifecycle — analogous progressive-disclosure load lifecycle; cc_create_a_skill — analogous skill authoring; cc_large_codebase_skills_and_plugins — analogous on-demand knowledge loading; cc_sdk_skills — analogous SDK skill loading model.
- Snippets (10): skills_canonical_format, skills_canonical_loading_runtime, skills_index_cache, core_skill_preprocessing, tools_skills_invoke, core_skill_commands_discovery, core_prompt_builder_skills_snapshot, cli_setup_skills, cli_skills_install, skills_hermes_agent — relevance: the skill format + Level-0/1/2 lazy-loading runtime + index cache + preprocessing, the `skill_view`/`skills_list` invoke surface, slash-command discovery, the system-prompt skill-index snapshot, the `hermes skills`/install CLI, and the canonical Hermes skill example this page describes.

**Note 4 `hermes_skill_md_format_bundles`** (model)
- Terms (8): term_skill_manifest, term_skills, term_progressive_disclosure[own], term_function_calling, term_autonomous_coding_agents, term_multimodal, term_agent_harness, term_persona — relevance: the SKILL.md model is a YAML-frontmattered manifest (name/description/version/platforms/metadata.hermes.*); bundles group skills under one slash command; media-delivery directives (`[[audio_as_voice]]`/`[[as_document]]`) shape multimodal output. (+fin: term_skills_hub[own])
- Code-Repos (5): repo_hermes_agent_skills — the frontmatter parser/validator, the on-disk skill-package layout (references/templates/scripts/assets/.hub), conditional-activation fields, and the `~/.hermes/skill-bundles/*.yaml` bundle loader; repo_hermes_agent_gateway_messaging — the media-delivery layer that auto-detects bare media paths and applies `[[audio_as_voice]]`/`[[as_document]]` (Telegram photo/Discord attachment); repo_hermes_agent_cli — `hermes bundles create/list/show/delete/reload` commands; repo_hermes_agent_tools — the `skill_manage` validate/manager surface that writes SKILL.md files; repo_hermes_agent_agent_core — platform-restriction filtering (`platforms:`) hiding skills from the system prompt on incompatible OS.
- Docs (10): hermes_skills_system — the concept that loads this file model; hermes_skills_hub_agent_managed — how SKILL.md files are installed/edited; hermes_skill_curator — consolidates SKILL.md packages; hermes_context_files — sibling markdown-with-frontmatter file model; hermes_google_workspace_skill — a concrete SKILL.md example; cc_skill_frontmatter_reference — Claude Code's analogous skill frontmatter schema; cc_create_a_skill — analogous SKILL.md authoring; cc_skill_arguments_and_substitutions — analogous skill invocation params; cc_bundled_skills — analogous bundled-skill catalog; cc_skills_overview — analogous skill file model.
- Snippets (10): skills_canonical_format, core_skill_utils_frontmatter, tools_skills_validate, tools_skill_manager, skills_index_cache, core_skill_preprocessing, skills_canonical_loading_runtime, cli_setup_skills, gw_platform_telegram_media, gw_platform_discord_attachment — relevance: the SKILL.md frontmatter parser/validator, the skill-manager that writes SKILL.md, the index cache + preprocessing + loading runtime that materialize the file model, the `hermes bundles`/setup CLI, and the gateway media-delivery code the `[[audio_as_voice]]`/`[[as_document]]` directives drive.

**Note 5 `hermes_skills_hub_agent_managed`** (procedure) — OWNS `term_skills_hub`
- Terms (8): term_skills_hub[own], term_skills, term_skill_manifest, term_self_evolving_agent, term_prompt_injection, term_human_in_the_loop, term_autonomous_coding_agents, term_agentic_ai — relevance: the hub installs skills from 9 sources with a security scan (prompt-injection/exfil/supply-chain); `skill_manage` is the agent's procedural memory; `skills.write_approval` staging is human-in-the-loop; trust levels gate `--force`. (+fin: term_skill_curator[own])
- Code-Repos (5): repo_hermes_agent_skills — `tools/skills_hub.py` (the hub install/registry/search across official/skills-sh/well-known/github/clawhub/lobehub/browse-sh/url), the security scanner + trust levels + `TRUSTED_REPOS`, taps.json, and `hermes skills reset` re-baselining; repo_hermes_agent_tools — the `skill_manage` tool (create/patch/edit/delete/write_file/remove_file) and the `skills.write_approval` staging gate; repo_hermes_agent_cli — `hermes skills browse/search/install/check/update/audit/reset/tap` + `/skills` slash commands; repo_hermes_agent_agent_core — the background self-improvement review that writes skills + the pending-staging review flow; repo_hermes_agent — config.yaml `skills.write_approval`/`skills.guard_agent_created` wiring.
- Docs (10): hermes_skills_system — the concept being installed/managed; hermes_skill_md_format_bundles — the file model the hub installs; hermes_skill_curator — the maintenance loop downstream of agent-created skills; hermes_persistent_memory — shares the write_approval staging gate; hermes_google_workspace_skill — a bundled skill subject to `hermes skills reset`; cc_host_and_manage_marketplaces — Claude Code's analogous skill/plugin marketplace hosting; cc_plugin_marketplaces_and_install — analogous multi-source install; cc_create_a_skill — analogous agent-authored skill creation; cc_security_architecture — analogous install-time security model; cc_skills_overview — analogous skill management surface.
- Snippets (10): tools_skill_manager, tools_skills_hub_install, tools_skills_hub_registry, tools_skills_validate, tools_skills_guard, cli_skills_install, cli_skills_hub, core_skill_commands_discovery, tools_skills_invoke, skills_index_cache — relevance: the `skill_manage` tool, hub install/registry across the 9 sources, the security validator/guard + trust levels, the `hermes skills browse/search/install/reset/tap` CLI + `/skills` slash discovery, the skill invoke surface, and the index cache re-baselined by `hermes skills reset` this page documents.

**Note 6 `hermes_persistent_memory`** (concept)
- Terms (8): term_agentic_memory, term_context_window, term_fts5, term_prompt_injection, term_pii, term_self_evolving_agent, term_human_in_the_loop, term_autonomous_coding_agents — relevance: bounded curated MEMORY.md (2200 char) + USER.md (1375 char) injected as a frozen snapshot into the context window; session search is SQLite FTS5; entries scanned for injection/PII; `memory.write_approval` is human-in-the-loop; background self-improvement writes it. (+fin: term_honcho[own], term_progressive_summarization)
- Code-Repos (5): repo_hermes_agent_agent_core — `build_context_files_prompt`/prompt-builder rendering of the frozen MEMORY/USER snapshot, the `§`-delimited block, and the security scan (injection/exfil/invisible-unicode) before acceptance; repo_hermes_agent_tools — the `memory` tool (add/replace/remove with substring matching) and `session_search` FTS5 tool; repo_hermes_agent_cli — `hermes memory setup/status`, `hermes sessions list`, `/memory pending/approve/reject` commands; repo_hermes_agent — config.yaml `memory:` block (`memory_char_limit`/`user_char_limit`/`write_approval`) + `~/.hermes/state.db` wiring; repo_hermes_agent_gateway_messaging — the `💾 Memory updated` background-review notification surfaced in chat.
- Docs (10): hermes_memory_providers_honcho — external providers that augment built-in memory; hermes_memory_provider_catalog — the 8-provider catalog; hermes_skill_curator — the parallel background review; hermes_context_files — sibling system-prompt-injected content; hermes_skills_hub_agent_managed — shares the write_approval gate; cc_memory_overview — Claude Code's analogous persistent-memory concept; cc_auto_memory — analogous auto-curated memory writes; cc_claude_md_files — analogous always-loaded memory file; cc_troubleshoot_memory — analogous memory capacity/management; cc_context_window_anatomy — analogous frozen system-prompt context budgeting.
- Snippets (10): tools_memory, cli_memory_setup, core_prompt_builder_environment, core_redact_patterns, core_message_sanitization, core_insights_collection, core_insights_reporting, gw_memory_monitor, core_conversation_loop_session_persist, core_prompt_builder_context_helpers — relevance: the `memory` add/replace/remove tool, `hermes memory setup`, the frozen MEMORY/USER system-prompt rendering + helpers, injection/PII redaction + message sanitization scans, the background insights collection/reporting write loop, the `💾 Memory updated` gateway notification, and the session-persistence FTS backing `session_search` this page documents.

**Note 7 `hermes_memory_providers_honcho`** (model) — OWNS `term_honcho`
- Terms (8): term_honcho[own], term_agentic_memory, term_knowledge_graph, term_dense_retrieval, term_multi_agent_systems, term_context_window, term_self_evolving_agent, term_llm — relevance: Honcho is an AI-native memory provider doing dialectic user modeling (LLM reasoning) with semantic/dense retrieval over conclusions; per-peer multi-agent isolation; two-layer context injection into the context window. (+fin: term_progressive_summarization)
- Code-Repos (5): repo_hermes_agent_plugins — `plugins/memory/honcho/` (the Honcho provider plugin: session lifecycle, two-layer base+dialectic injection, `contextCadence`/`dialecticCadence`/`dialecticDepth` knobs, observation directional/unified, the 5 honcho tools) plus the memory-provider plugin-discovery/ABC interface; repo_hermes_agent_cli — `hermes memory setup`, the `hermes honcho` subcommand suite (status/strategy/peer/mode/sync/migrate); repo_hermes_agent_agent_core — the per-turn inject/prefetch/sync/extract lifecycle and session-start prewarm hand-off to turn 1; repo_hermes_agent_gateway_messaging — gateway identity mapping (`pinUserPeer`/`userPeerAliases`/`runtimePeerPrefix`) resolving runtime IDs to peers; repo_hermes_agent — config.yaml `memory.provider: honcho` + `honcho.json` resolution wiring.
- Docs (10): hermes_memory_provider_catalog — the other 8 providers; hermes_persistent_memory — the built-in memory Honcho augments; hermes_skill_curator — sibling background-review/aux-model pattern; hermes_context_files — sibling system-prompt injection; hermes_skills_system — sibling provider-plugin concept; cc_memory_overview — Claude Code's analogous memory backend; cc_auto_memory — analogous auto-extraction; cc_troubleshoot_memory — analogous memory recall; cc_context_window_anatomy — analogous context-budget injection; cc_what_survives_compaction — analogous cross-session recall/summary.
- Snippets (10): honcho_session_lifecycle, honcho_session_query, honcho_session_messages, plugins_memory_discovery, plugins_interfaces_abcs, plugins_namespace_init, core_agent_init_memory_ollama, tools_memory, cli_memory_setup, gw_memory_monitor — relevance: the Honcho session lifecycle/query/messages (two-layer inject + dialectic), the memory-provider plugin discovery + ABC interface + namespace registration the provider plugs into, the agent-init memory-provider wiring, the `memory` tool + `hermes memory setup` CLI, and the gateway memory-update notification this page documents.

**Note 8 `hermes_memory_provider_catalog`** (model)
- Terms (8): term_agentic_memory, term_knowledge_graph, term_dense_retrieval, term_bm25, term_vector_database, term_embedding, term_rag, term_information_retrieval — relevance: the catalog providers each implement a retrieval stack (vector + BM25 + reranking + knowledge graph + RAG) over embeddings for cross-session recall; per-profile data isolation by storage class. (+fin: term_honcho[own])
- Code-Repos (5): repo_hermes_agent_plugins — `plugins/memory/*` (OpenViking/Mem0/Hindsight/Holographic/RetainDB/ByteRover/Supermemory/Memori provider plugins) + the discovery/ABC interface + namespace registration every catalog provider plugs into; repo_hermes_agent_cli — `hermes memory setup/status/off`, `hermes plugins → Provider Plugins → Memory Provider`, `hermes config set memory.provider`; repo_hermes_agent_agent_core — the one-active-provider inject/prefetch/sync/extract/mirror lifecycle shared by every provider; repo_hermes_agent_providers_adapters — the per-provider SDK/CLI/HTTP adapter surfaces (`brv`, `gws`-style external clients) the providers wrap; repo_hermes_agent — config.yaml `memory.provider` selection + per-profile `$HERMES_HOME/` isolation wiring.
- Docs (10): hermes_memory_providers_honcho — the flagship provider + provider-system concept; hermes_persistent_memory — the built-in memory all providers run alongside; hermes_skill_curator — sibling plugin/aux pattern; hermes_context_references — sibling bounded-content injection; hermes_skills_system — sibling provider-plugin model; cc_memory_overview — Claude Code's analogous memory backends; cc_auto_memory — analogous automatic fact extraction; cc_troubleshoot_memory — analogous recall tuning; cc_extending_claude_code — analogous plugin-extension surface; cc_plugins_overview — analogous provider-plugin catalog.
- Snippets (10): plugins_memory_discovery, plugins_interfaces_abcs, plugins_namespace_init, core_agent_init_memory_ollama, tools_memory, cli_memory_setup, gw_memory_monitor, honcho_session_lifecycle, core_insights_collection, plugins_provider_registry — relevance: the memory-provider plugin discovery/interface/registration + namespace init every catalog provider plugs into, the agent-init memory wiring, the `memory` tool + `hermes memory setup` CLI, the gateway memory notification, the insights write loop providers mirror, and the provider-plugin registry that resolves the one active provider.

**Note 9 `hermes_skill_curator`** (procedure) — OWNS `term_skill_curator`
- Terms (8): term_skill_curator[own], term_skills, term_skill_manifest, term_self_evolving_agent, term_subagent, term_autonomous_coding_agents, term_multi_agent_systems, term_agentic_ai — relevance: the curator is a background-fork (subagent) maintenance loop for agent-created skills produced by the self-improvement loop; inactivity-gated aux-model LLM review consolidates/archives them via `skill_manage`. (+fin: term_skills_hub[own])
- Code-Repos (5): repo_hermes_agent_skills — the curator review/transition/state-machine (`active→stale→archived`), `.usage.json` telemetry sidecar, tar.gz backups + rollback, pinning, protected built-ins, and per-run REPORT.md; repo_hermes_agent_cron — the gateway cron-ticker thread that triggers the inactivity-gated curator tick (`interval_hours`/`min_idle_hours`); repo_hermes_agent_agent_core — the background `AIAgent` fork pattern + `auxiliary.curator` aux-model slot resolution shared with the memory/skill self-improvement nudges; repo_hermes_agent_cli — `hermes curator status/run/backup/rollback/pin/restore/prune` + `/curator` slash command; repo_hermes_agent_tools — the `skill_manage` consolidation actions + `skill_view` the forked agent uses.
- Docs (10): hermes_skills_hub_agent_managed — produces the agent-created skills the curator manages; hermes_skills_system — the self-improvement loop that creates them; hermes_skill_md_format_bundles — the SKILL.md packages it consolidates; hermes_persistent_memory — the parallel background memory review; hermes_memory_providers_honcho — sibling aux-model/background pattern; cc_skill_invocation_and_lifecycle — Claude Code's analogous skill lifecycle; cc_forked_subagents — analogous background-fork subagent model; cc_subagents_overview — analogous subagent execution; cc_configure_advisor_model — analogous aux-model routing; cc_create_a_skill — analogous skill mutation surface.
- Snippets (10): core_curator_review, core_curator_transitions, core_curator_state, core_curator_reports, tools_skill_manager, tools_skills_invoke, skills_index_cache, core_skill_commands_discovery, cron_tick, cli_cron — relevance: the curator review/transition/state-machine + per-run REPORT.md engine, the `skill_manage` consolidation actions + `skill_view` the forked agent drives, the index cache it re-baselines, the cron-ticker that triggers the inactivity-gated curator tick, and the `hermes cron`/`hermes curator` scheduling CLI.

**Note 10 `hermes_context_files`** (procedure) — OWNS `term_agents_md`
- Terms (8): term_agents_md[own], term_autonomous_coding_agents, term_agent_harness, term_prompt_injection, term_context_window, term_persona, term_pii, term_function_calling — relevance: context files (`.hermes.md`→`AGENTS.md`→`CLAUDE.md`→`.cursorrules`, first-match) inject project conventions into the system prompt/context window; all are scanned for prompt injection; progressive subdirectory discovery hooks tool-call file-path args. (+fin: term_soul_md[own])
- Code-Repos (5): repo_hermes_agent_agent_core — `build_context_files_prompt()` in `agent/prompt_builder.py` (the first-match priority chain, UTF-8 read, security scan, head/tail truncation, `# Project Context` assembly) and `SubdirectoryHintTracker` in `agent/subdirectory_hints.py` (path extraction + ancestor walk + per-directory once); repo_hermes_agent_tools — the `read_file`/`terminal`/`search_files` tool-call args the subdirectory tracker watches; repo_hermes_agent_cli — the `HERMES_HOME` resolution that scopes SOUL.md and the working-directory scan; repo_hermes_agent — config.yaml `context_file_max_chars` (20,000) truncation knob; repo_hermes_agent_gateway_messaging — context files apply across gateway sessions too.
- Docs (10): hermes_personality_soul — SOUL.md (the always-loaded slot-#1 identity) detail; hermes_context_references — the inline `@`-ref sibling content-injection mechanism; hermes_persistent_memory — sibling frozen-snapshot system-prompt injection; hermes_skills_system — skills guidance is another prompt section; hermes_skill_curator — sibling agent-managed file; cc_claude_md_files — Claude Code's analogous CLAUDE.md context file (Hermes detects it); cc_claude_rules_directory — analogous rules-directory discovery; cc_manage_claude_md_for_teams — analogous shared-repo context governance; cc_large_codebase_claude_md_layering — analogous nested/progressive context layering; cc_prompt_injection_defenses — analogous context-file injection scanning.
- Snippets (10): core_prompt_builder_context_loaders, core_prompt_builder_context_helpers, core_prompt_builder_environment, core_redact_patterns, core_message_sanitization, core_prompt_builder_skills_snapshot, tools_file_tools, core_context_references_path_safety, tools_file_operations_a, gw_session_context — relevance: the first-match context-file loader + helpers + environment block, the prompt-injection redaction + message-sanitization scans, the skills-snapshot sibling prompt section, the `read_file`/`search_files` tool-call args the subdirectory tracker watches + path-safety, and the gateway session-context assembly that applies context files across platforms this page documents.

**Note 11 `hermes_context_references`** (procedure)
- Terms (8): term_context_window, term_autonomous_coding_agents, term_agent_harness, term_pii, term_prompt_injection, term_function_calling, term_progressive_summarization, term_idempotency — relevance: `@file`/`@folder`/`@diff`/`@staged`/`@git:N`/`@url` inject bounded content into the context window under `--- Attached Context ---` before send; sensitive-path/traversal/binary blocking prevents PII/credential leak; compression summarizes expanded refs. (+fin: term_agents_md[own])
- Code-Repos (5): repo_hermes_agent_agent_core — the `@`-reference parser/expander, the soft/hard size-limit (25%/50% of context length) gating, and the compression interaction with expanded refs; repo_hermes_agent_tools — `read_file`/`search_files`/`web_extract` tools the `@`-refs and the agent itself use, plus sensitive-path/traversal/binary detection; repo_hermes_agent_cli — `@` tab completion (reference-type + filesystem path completion with size metadata) in the interactive CLI; repo_hermes_agent_gateway_messaging — confirms `@`-syntax is NOT expanded on messaging platforms (CLI-only feature); repo_hermes_agent — config.yaml context-length knob the soft/hard limits scale against.
- Docs (10): hermes_context_files — sibling project-context injection; hermes_persistent_memory — sibling bounded context injection; hermes_personality_soul — sibling system-prompt content; hermes_skills_system — `@`-refs complement skill loading; hermes_tools_toolsets — the `web_extract` tool backs `@url`; cc_dot_claude_directory — Claude Code's analogous `@`-style file context; cc_effective_prompting — analogous attaching-file-context patterns; cc_reduce_token_usage — analogous bounded-context/line-range technique; cc_context_window_anatomy — analogous context-budget management; cc_what_survives_compaction — analogous compression-of-attached-content behavior.
- Snippets (10): core_context_references_parser, core_context_references_expander, core_context_references_path_safety, core_prompt_builder_context_helpers, tools_file_tools, tools_file_operations_a, core_conversation_loop_context_overflow, tools_web_tools, cli_completion, cli_attachment_input_bindings — relevance: the `@`-reference parser + expander + sensitive-path/traversal/binary path-safety, the `read_file`/`web_extract` tools the refs use, the context-overflow/compression handling of expanded refs, and the CLI `@` tab-completion + attachment-input bindings (CLI-only feature) this page documents.

**Note 12 `hermes_personality_soul`** (procedure) — OWNS `term_soul_md`
- Terms (8): term_soul_md[own], term_autonomous_coding_agents, term_agent_harness, term_prompt_injection, term_prompt_engineering, term_function_calling, term_context_window, term_persona — relevance: SOUL.md is the slot-#1 system-prompt identity (prompt engineering) loaded only from HERMES_HOME; scanned for injection; the 14 built-in `/personality` presets + custom `agent.personalities` are system-prompt overlays in the context window. (+fin: term_agents_md[own])
- Code-Repos (5): repo_hermes_agent_agent_core — the prompt-stack assembly (slot #1 SOUL.md identity → tool guidance → memory → skills → context files → timestamp → platform hints → `/personality` overlay), the SOUL.md HERMES_HOME-only loader, default-identity fallback, and the security scan; repo_hermes_agent_cli — `hermes` seeding the default SOUL.md and `/personality` switching; repo_hermes_agent — config.yaml `agent.personalities`/`agent.system_prompt` custom-persona definitions; repo_hermes_agent_tui_gateway — `display.skin`/`/skin` terminal appearance (distinct from conversational personality); repo_hermes_agent_gateway_messaging — `/personality` overlay works across messaging platforms.
- Docs (10): hermes_context_files — SOUL.md vs AGENTS.md and the priority chain; hermes_skills_system — skills guidance is another prompt-stack section; hermes_persistent_memory — memory/user context is another prompt-stack slot; hermes_context_references — sibling system-prompt content; hermes_tool_gateway — Nous default-identity context; cc_output_styles — Claude Code's analogous persona/output-style customization; cc_sdk_customize_system_prompt — analogous identity/system-prompt override; cc_sdk_system_prompts — analogous system-prompt composition; cc_effective_prompting — analogous voice/style guidance; cc_prompt_injection_defenses — analogous identity-file injection scanning.
- Snippets (10): core_prompt_builder_context_loaders, core_prompt_builder_environment, core_prompt_builder_context_helpers, core_redact_patterns, core_message_sanitization, core_prompt_builder_skills_snapshot, tools_file_tools, cli_skin_engine, gw_display_config, core_context_references_path_safety — relevance: the SOUL.md HERMES_HOME-only identity loader + the full prompt-stack assembly (slot #1 identity → memory → skills snapshot → context), the injection redaction + message-sanitization scans, the `display.skin`/`/skin` terminal-appearance engine (distinct from conversational personality), the gateway display config, and the SOUL.md path-safety this page documents.

**Note 13 `hermes_google_workspace_skill`** (procedure)
- Terms (8): term_skills, term_skill_manifest, term_oauth_token, term_authentication, term_oauth, term_autonomous_coding_agents, term_function_calling, term_progressive_disclosure[own] — relevance: this is a bundled skill (SKILL.md at `skills/productivity/google-workspace/`) loaded via progressive disclosure; it wraps the OAuth2-authenticated `$GAPI` CLI (Gmail/Calendar/Drive/Sheets/Docs/Contacts) the agent calls. (+fin: term_skills_hub[own])
- Code-Repos (5): repo_hermes_agent_skills — the bundled `skills/productivity/google-workspace/` package (SKILL.md + scripts) plus the skill discovery/invoke/index that loads and runs it; repo_hermes_agent_tools — the `terminal`/`execute_code` tool the skill's `$GAPI` CLI runs through (with declared env-vars passed into the sandbox); repo_hermes_agent_cli — `hermes skills reset google-workspace` and the agent-driven OAuth setup flow; repo_hermes_agent_agent_core — the secure-setup-on-load env-var prompting + config injection when the skill loads; repo_hermes_agent — config.yaml skill settings + `.env` credential resolution for the OAuth token.
- Docs (10): hermes_skills_system — the system that loads this bundled skill; hermes_skill_md_format_bundles — the SKILL.md format it follows; hermes_skills_hub_agent_managed — `hermes skills reset` un-sticks it; hermes_skill_curator — protected/bundled-skill handling; hermes_persistent_memory — credential/setup facts may be remembered; cc_create_a_skill — Claude Code's analogous skill authoring; cc_skills_overview — analogous bundled-skill concept; cc_bundled_skills — analogous bundled-skill catalog; cc_mcp_overview — analogous OAuth-authenticated external-API integration; cc_authentication — analogous OAuth token-refresh auth flow.
- Snippets (10): skills_email, skills_github, skills_apple_macos, skills_obsidian, skills_canonical_format, tools_skills_invoke, core_skill_commands_discovery, cli_setup_skills, skills_index_cache, tools_msgraph — relevance: representative productivity bundled-skill implementations (email/github/apple-macos/obsidian) parallel to the Google Workspace `$GAPI` skill, the canonical SKILL.md format it follows, the skill invoke/discovery/index code that loads and runs it, the `hermes skills` setup CLI, and the MS-Graph tool surface (analogous OAuth-CLI productivity integration) this page documents.

> **Authoring note:** `term_*[own]` annotations mark the 7 SP05-owned slugs (captured Phase 0, before any digest
> note that links them — they DO count to SP05's floor). At an earlier finalization the following placeholder slugs
> `term_token_budget`, `term_tool_use`, `term_yaml`, `term_system_prompt`, `term_reranking`, `term_supply_chain_attack`,
> `term_personalization`, `term_user_modeling`, `term_in_context_learning`). Every per-note term list above uses ONLY

All 13 notes meet the FOUR-FLOOR standard **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (all counted,
relevancy-selected). Term IDs (excluding the 7 SP05-owned, captured Phase 0), ALL repo IDs, and ALL snippet IDs are
`resources/code_snippets/` with the `snippet_hermes_agent_` prefix (so e.g. `tools_registry` →
`resources/code_snippets/snippet_hermes_agent_tools_registry.md`). Sibling `hermes_*` doc links resolve in
`resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by G5/G8). Repo notes
live at `areas/code_repos/`; from a note in `resources/documentation/hermes_agent/` the relative path is
`../../../areas/code_repos/<repo>.md`; snippet notes at `../../code_snippets/snippet_hermes_agent_<id>.md`.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; honcho.md re-evaluated 2026-06-19)

Re-read all 11 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). **2026-06-19 re-sync:** `honcho.md` grew 2128→2505w, CROSSING the 2500w
raw cap. honcho.md owns Note 7 (`hermes_memory_providers_honcho`), but Note 7 is NOT a 1:1 mirror — it is a
**curated fusion** of honcho.md + the memory-providers.md Honcho entry, projected at ~1950w (still <2500w,
~550w headroom). The +377w of honcho.md growth is entirely PROSE (expanded Gateway Identity Mapping, observation
preset tables, config-reference table); honcho's code-block count is unchanged at 5. Note 7 already prose-summarizes
the full config reference (link-out to the page) and curates to ≤6 load-bearing code blocks. The 2-way split
(Note 7 = provider-system + Honcho deep architecture; Note 8 = the other 8 providers) keeps the Honcho content
atomic and the note within caps. **Outcome: still within caps — NO split.** Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 tools-toolsets | model | 1000 | ≤6 (from 9 short blocks; tables in prose) | ✓ |
| 2 tool-gateway | concept | 1300 | ≤6 (curate from 9; one config block) | ✓ |
| 3 skills-system | concept | 1500 | ≤6 (curate from skills.md intro/progressive/external blocks) | ✓ |
| 4 skill-md-format-bundles | model | 1400 | ≤6 (one SKILL.md frontmatter + one bundle YAML + directive examples) | ✓ |
| 5 skills-hub-agent-managed | procedure | 1600 | ≤6 (curate from hub command blocks; one tap layout) | ✓ |
| 6 persistent-memory | concept | 1500 | ≤6 (system-prompt render + tool example + config) | ✓ |
| 7 memory-providers-honcho | model | 1950 | ≤6 (curate from honcho config/observation blocks; one minimal honcho.json) | ✓ (honcho.md src 2505w but Note 7 curated/prose-summarized — see re-sync) |
| 8 memory-provider-catalog | model | 1600 | ≤6 (one representative setup block + comparison table in prose/table) | ✓ |
| 9 skill-curator | procedure | 1500 | ≤6 (config defaults + CLI list curated; tables in prose) | ✓ |
| 10 context-files | procedure | 1300 | ≤6 (priority chain + example AGENTS.md + load steps) | ✓ |
| 11 context-references | procedure | 900 | 4 | ✓ |
| 12 personality-soul | procedure | 1300 | ≤6 (one SOUL.md example + personality table + custom block) | ✓ |
| 13 google-workspace | procedure | 900 | ≤6 (curate from 12 `$GAPI` blocks; representative per service) | ✓ |

No further splits needed — all 13 notes are ≤2500w. Code-heavy pages (skills.md clusters, honcho, google-workspace)
are curated to ≤6 load-bearing blocks each, with the rest summarized in prose (kept blocks verbatim). Note 7
(~1950w, the densest) is one topically-cohesive model (provider system + Honcho) → KEEP (per review CP6
default-to-keep justification); honcho.md crossing 2500w raw does NOT push the curated Note 7 over caps (2026-06-19
re-sync, no split). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP05)

**SP05 OWNS 7 new term captures.** Each is captured via `/tessellum-capture-term-note <term>` in **Phase 0**
(BEFORE any digest note that links it), NOT inline-authored within a digest note. Augment re-read confirmed
all 7 are genuinely undigested (exact-slug MISSING + collision audit found only unrelated LIKE hits — see
Collision & Dedup Audit). Each capture MUST follow the full Term-Note Authoring Requirements below.

| Term slug | Concept | Stub/Full | Capture Phase | Best-fit glossary | Owner |
|-----------|---------|-----------|---------------|-------------------|-------|
| `term_tool_gateway` | Nous Tool Gateway — managed tool-execution proxy (web/image/tts/browser) routed through Nous Portal | FULL | Phase 0 | acronym_glossary_tools | SP05 |
| `term_soul_md` | SOUL.md — durable global persona/identity file loaded from HERMES_HOME into system-prompt slot #1 | FULL | Phase 0 | acronym_glossary_developer | SP05 |
| `term_agents_md` | AGENTS.md — primary project context file (conventions/architecture) with progressive subdirectory discovery | FULL | Phase 0 | acronym_glossary_developer | SP05 |
| `term_progressive_disclosure` | progressive disclosure — Level-0/1/2 on-demand skill loading to minimize token usage | FULL | Phase 0 | acronym_glossary_llm | SP05 |
| `term_skills_hub` | Skills Hub — multi-source skill install registry (official/skills-sh/well-known/github/clawhub/lobehub/browse-sh/url) | FULL | Phase 0 | acronym_glossary_tools | SP05 |
| `term_skill_curator` | curator — background inactivity-gated maintenance loop for agent-created skills (usage telemetry → stale/archive → LLM review) | FULL | Phase 0 | acronym_glossary_llm | SP05 |
| `term_honcho` | Honcho — AI-native external memory provider with dialectic user modeling + per-peer multi-agent isolation | FULL | Phase 0 | acronym_glossary_tools | SP05 |

All 7 are FULL (not stub): each is a recurring, conceptually substantive Hermes concept (DF 6–24 per the
master sweep) with enough source material across multiple pages to support a full term note. None is a
low-value product name.

### Renamed (general → specific)

| Original candidate | Renamed to | Reason |
|---|---|---|
| `term_curator` (too general — would collide with future generic "curator") | `term_skill_curator` | Hermes' curator is specifically the **agent-created-skill** maintenance loop; `term_curator` would be ambiguous with data/content curation concepts. Concrete scope-qualified slug avoids a future collision. |
| `term_gateway` / `term_nous_gateway` (too general) | `term_tool_gateway` | "gateway" collides with `term_api_gateway`/`term_mcp_gateway`/`term_agentcore_gateway`/`term_nat_gateway` (4 existing); the Nous offering is specifically a **tool**-execution proxy → slug names the tool scope. |
| `term_soul` (too general) | `term_soul_md` | Names the concrete file (`SOUL.md`); `term_soul` is ambiguous. |
| `term_agents` (too general) | `term_agents_md` | Names the concrete file (`AGENTS.md`); avoids collision with the many `%agent%` terms and the unrelated `term_agentspace`. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_skills` (Hermes skill concept) | `term_skills.md` (active) is "AIM Skills" — UNRELATED, per master | NOT captured as duplicate; the Hermes skill CONCEPT is documented in doc note `hermes_skills_system` + the new `term_progressive_disclosure`; LINK existing `term_skills`/`term_skill_manifest` where genuinely about the manifest format (the closest existing match). |
| `term_memory_provider` (would generalize) | covered by doc notes `hermes_memory_providers_honcho` + `hermes_memory_provider_catalog`; concept anchored by new `term_honcho` + existing `term_agentic_memory` | Not captured — link `term_agentic_memory` + the new `term_honcho`. |
| `term_context_file` (would generalize) | covered by doc note `hermes_context_files` + the new `term_agents_md`/`term_soul_md` | Not captured — the two concrete file terms + the doc note suffice. |

## Term-Note Authoring Requirements

SP05 OWNS 7 new term captures; each MUST be authored via `/tessellum-capture-term-note <term>` (NOT inline),
following the canonical term-note format exactly:

- **YAML frontmatter (required fields):** `tags` (itemized list, first tag `resource`, includes `term` +
  domain tags), `keywords` (4–8 lowercase itemized), `topics` (itemized), `language: markdown`,
  `date of note: 2026-06-15`, `status: active`, **`building_block: concept`**, `related_wiki` (external
  authoritative URL — Hermes docs page + upstream e.g. Honcho/plastic-labs, agentskills.io), `access_control_group: ["general"]`.
  Year tags quoted. No wiki/markdown links in YAML. Forbidden fields per master.
- **Required H1 + H2 sections in order:** `# <Term>` → `## Definition` (lead with what it IS) → `## Context`
  (where/why it appears in Hermes) → `## Key Characteristics` → `## Performance` (optional, only if there's
  substantive perf content) → `## Related Terms` (**8–15 minimum**, indexed markdown links each with a
  description + relevancy clause, cross-domain) → `## References` (external-only authoritative sources).
  draw on **≥5 sources** — the Hermes docs page(s), the upstream project/spec (e.g. agentskills.io for
  progressive disclosure, plastic-labs/honcho + docs.honcho.dev for Honcho, the Hermes source code via the
  existing `snippet_hermes_agent_*` / `repo_hermes_agent_*` notes), and ≥1 cross-domain analogue already in
  the vault. A single-source (docs-only) capture is REJECTED.
- **Cross-domain diversity matrix (6 connection types):** Related Terms MUST span ≥4 of: same-system Hermes
  concept, ML/LLM concept, security concept, data/retrieval concept, agent-architecture concept, ops/config
  concept. Avoid mono-domain padding.
- **Fleeting-content guard:** do NOT cite specific version numbers, model lists, or vault counts that go
  stale; cite the doc page + FZ/snippet link instead.
- **Glossary entry format:** add a 4–5 sentence Description (scope + what it does + why it matters; NO
  numeric metrics) to the best-fit `acronym_glossary_*` listed in the Undigested Terms Plan table.
- **Depth-scaled Related Terms:** 8 (stub-ish) / 10 (standard) / 12+ (well-connected) — all 7 SP05 terms are
  standard-to-well-connected → target ≥10 Related Terms each.
- **Backlink expansion:** after capture, add ≥1 inbound link from an existing related vault note (e.g.
  `term_agentic_memory` → `term_honcho`; `term_skills`/`term_skill_manifest` → `term_progressive_disclosure`/`term_skills_hub`).
- **>200-line decomposition:** if a term note exceeds ~200 lines, decompose per canonical (none expected here).
- **Acceptance failure conditions:** missing any required H2, <8 Related Terms, single-source research,
  metrics in glossary Description, or a non-`concept` building_block → capture FAILS, re-author.

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (OWNED term captures — BEFORE any digest note):** `/tessellum-capture-term-note` for all 7 owned
  terms (`term_tool_gateway`, `term_soul_md`, `term_agents_md`, `term_progressive_disclosure`,
  `term_skills_hub`, `term_skill_curator`, `term_honcho`), each full + multi-source + glossary update +
  backlink. Reindex. GATE G1 (format), G5 (ghost — verify the new terms now resolve), G6, G8 (backlink).
- **Phase 1 (skills cluster, P1-hub pilot):** Notes 3, 4, 5. Pilot Note 3 (`hermes_skills_system`) first →
  reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (tools + memory):** Notes 1, 2, 6, 7, 8, 9. GATE G1–G8.
- **Phase 3 (context + personality + bundled skill):** Notes 10, 11, 12, 13. GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, gated):** add every Inlinks-table inbound link; reindex; verify G8 in-degree ≥1.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref incl. the 7 new terms)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** ·
G7 single-BB · **G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 2: OWNED term captures exist + active (Phase 0 gate)
for t in term_tool_gateway term_soul_md term_agents_md term_progressive_disclosure term_skills_hub term_skill_curator term_honcho; do
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_tools_toolsets hermes_tool_gateway hermes_skills_system hermes_skill_md_format_bundles hermes_skills_hub_agent_managed hermes_persistent_memory hermes_memory_providers_honcho hermes_memory_provider_catalog hermes_skill_curator hermes_context_files hermes_context_references hermes_personality_soul hermes_google_workspace_skill; do
```

## Entry Point Decision (inherited)

Contributes 13 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Knowledge, Memory & Skills" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP05 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).
The 7 new term notes also update their best-fit `acronym_glossary_*` entry points (per Term-Note Authoring Requirements).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_skills.md` | → `hermes_skills_system`, `hermes_skill_md_format_bundles`, `hermes_skills_hub_agent_managed`, `hermes_skill_curator` | skills repo ↔ skills usage docs |
| `repo_hermes_agent_tools.md` | → `hermes_tools_toolsets`, `hermes_tool_gateway` | tools repo ↔ tools/gateway usage docs |
| `repo_hermes_agent_plugins.md` | → `hermes_memory_providers_honcho`, `hermes_memory_provider_catalog` | memory providers are plugins ↔ provider docs |
| `repo_hermes_agent_agent_core.md` | → `hermes_persistent_memory`, `hermes_context_files`, `hermes_context_references`, `hermes_personality_soul` | agent core (prompt builder/memory/context) ↔ knowledge docs |
| `repo_hermes_agent_mcp_toolsets.md` | → `hermes_tools_toolsets` | toolset materialization ↔ tools/toolsets doc |
| `term_skills.md` | → `hermes_skills_system` | nearest existing skill term → Hermes skill system doc |
| `term_skill_manifest.md` | → `hermes_skill_md_format_bundles` | manifest concept → SKILL.md format doc |
| `term_agentic_memory.md` | → `hermes_persistent_memory`, `hermes_memory_providers_honcho` | memory concept → memory docs |
| `term_progressive_summarization.md` | (NO inlink — unrelated to progressive disclosure) | confirmed false-positive; do NOT link |
| `term_agentspace.md` / `term_agentspaces.md` | (NO inlink — unrelated to AGENTS.md) | confirmed false-positive; do NOT link |
| `entry_code_snippets_hermes_agent.md` | → `hermes_skills_system`, `hermes_tools_toolsets`, `hermes_persistent_memory` | code layer ↔ docs layer |
| new `term_honcho` / `term_skills_hub` / `term_skill_curator` / `term_progressive_disclosure` (Phase 0) | → their home doc notes (Notes 7/5/9/3) | new term ↔ owning doc note |
| `entry_hermes_agent_docs.md` (new, master) | → all 13 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Phase 0 (7 term captures) FIRST → reindex → verify the new terms resolve (Script 2). Then pilot Note 3
(`hermes_skills_system`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest. Commit per
phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note — do NOT
work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6 load-bearing blocks,
summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split. If multi-agent:
agents return note content, master writes serially where there is write-contention; ≤30 agents/run; embed
the manifest in the workflow script.

## Follow-up Recommendations

- After SP05 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 13 rows to
  the master-created entry point + the 7 term rows to their glossaries; backfill the `repo_hermes_agent_*` /
  `term_*` inlinks (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1 wave: cross-link from the SP02 config notes (skill/memory/security settings) ↔ these feature
  notes once both land (bidirectional config↔feature links); cross-link SP08 (media/web tools) ↔
  `hermes_tool_gateway`/`hermes_tools_toolsets`; SP19 (creating-skills, memory-provider-plugin) ↔ Notes 4/5/8.
- Consider one `thought_` note comparing Hermes' docs-stated skill/memory model vs the code-digestion
  findings in `snippet_hermes_agent_skills_*` / `snippet_hermes_agent_core_curator_*` / `snippet_hermes_agent_honcho_*`.

## Augmentation Report

- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  snippets were a "bonus, not counted" group) and the original ≥8 term / ≥8 snippet / ≥5 doc. Re-read all 11 owned
  source pages from `inbox/hermes_agent_docs/` (not from memory) to ground each relevance clause; every planned note
  2026-06-19), a "Docs (10)" line (sibling `hermes_*` in-series + analogous `claude_code/cc_*` docs, all `cc_*`
  raised to ≥10 and re-grounded against each page's documented code paths, all `snippet_hermes_agent_*` IDs
- Sections added/updated: Collision&Dedup Audit (all LIKE hits confirmed false-positives by reading notes +
  master caution list; 7 owned terms genuinely new), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5 code-repo
  (derived from `cc_*.md`, Related-Notes minimum updated to the four-floor standard), Density
  Re-Assessment (re-read confirmed), G5 ghost + Phase-0 term-existence + G8 scripts, Inlinks, full Term-Note
  Authoring Requirements (SP05 owns captures).
- Density re-read: counts match measured; **no additional splits** beyond the planned (skills→3, memory-providers→2).
  All 13 notes ≤2500w; code-heavy notes curated to ≤6 blocks.
- Collision audit: **0 removals of owned terms** — `term_api_gateway`/`term_mcp_gateway`/`term_agentcore_gateway`
  (different gateways), `term_agentspace`/`term_agentspaces` (Google Agentspace), `term_progressive_summarization`
  3 would-be generic slugs renamed (general→specific); 3 candidate captures removed in favor of linking.
- Term placeholder catch: **11 non-existent term slugs caught at finalization** (`term_semantic_search`,
  `term_text_to_speech`, `term_token_budget`, `term_tool_use`, `term_yaml`, `term_system_prompt`,
  `term_reranking`, `term_supply_chain_attack`, `term_personalization`, `term_user_modeling`,
- Undigested terms surfaced at augment: **7 owned** (all FULL, Phase 0, multi-source mandate); aligns with master sweep.
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold;
  + 7 glossary updates for the owned terms.

## 31-Item Checklist

PASS 31/31. (1 Objective ✓ 2 Routing ✓ 3 Source measured ✓ 4 Content Strategy ✓ 5 Coverage Map (no orphans) ✓
6 Split Decisions ✓ 7 Planned Notes ✓ 8 Size Assessment ✓ 9 Summary Stats ✓ 10 BB Distribution ✓ 11 Per-note
12 Entry Points ✓ 13 Inlinks (all 13) ✓ 14 Phase GATEs incl G5/G6/G8 ✓
15 Note Format Def (derived) ✓ 16 Validation Scripts ✓ 17 Pacing ✓ 18 Density Re-Assessment (re-read) ✓
19 Follow-up ✓ 20 Undigested Terms Plan (7 owned) ✓ 21 Capture Phase per term (Phase 0) ✓ 22 best-fit glossary
per term ✓ 23 Term-Note Auth Reqs (FULL, multi-source mandate) ✓ 24 invokes `/tessellum-capture-term-note` per
term (not inline) ✓ 25 Entry-Point Decision ✓ 26 matches size threshold ✓ 27 Slug Specificity (4 renamed
general→specific) ✓ 28 Slug Collision (LIKE false-positives confirmed + 3 removed + 11 placeholders caught) ✓
29 dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ 30 G8 in every
phase + inlinks EXECUTED (Phase 3b) ✓ 31 Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Re-Reviewed 2026-06-19 (FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).**


| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes (FOUR-FLOOR) | PASS | All 13 planned notes carry 4 counted groups; programmatic count confirms every note ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc (Note 1 = 9 term / 5 repo / 11 snippet / 10 doc; Notes 2–13 = 8/5/10/10). Every group line carries a `relevance:` clause (no bare links). |
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Execution Phases (0/1/2/3/3b) each spell G1–G8; G5 ghost (Script 4), G6 broken-links, G8 in-degree present in Validation Scripts. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (13 rows) + 7 glossary updates; >30-note series → no separate entry point. |
| CP4 | Plan size | PASS | 13 notes ≤30. |
| CP5 | Note format derived | PASS | Doc-Note Authoring Spec derived from `cc_*.md`; FOUR-FLOOR Related-Notes minimum stated. |
| CP6 | Density | PASS | All 13 notes ≤2500w / ≤6 code; densest Note 7 (~1950w) is one cohesive model → KEEP; honcho.md 2505w raw does not push curated Note 7 over caps. |
| CP7 | Source counts measured | PASS | Re-measured (leading-frontmatter strip): tool-gateway 1455/9, curator 2356/10, memory-providers 3407/18, memory 2103/11, honcho 2505/5 — all == plan (ratio 1.00). |
| CP9 | Inbound links (G8) | PASS | Inlinks table covers all 13 notes from repo_*/term_*/entry_* outside the folder + new-term→doc; gated Phase 3b. |

**RESULT (2026-06-19 re-review): 9/9 → READY FOR EXECUTION.** No factual fixes required; the four-floor wording is consistent throughout (no stale 3-floor/"bonus-counted" claims; the only "bonus" mentions are historical/supersession notes). `revised: 2026-06-19` set.

---

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 digest phases + Phase 3b, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (13 rows under Knowledge/Memory/Skills section) + 7 glossary updates; parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 13 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | skills.md→3, memory-providers→2; all notes ≤2500w; code-heavy notes curated ≤6; densest note (7 ~1900w) is one cohesive model → KEEP justified. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 (mirror c253b07): skills 5194, memory-providers 3407, curator 2356, honcho 2505, memory 2103, tool-gateway 1455, context-files 1310, personality 1200, tools 975, google-workspace 868, context-references 729 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP05 OWNS 7 term captures (Phase 0, `/tessellum-capture-term-note`, FULL); Undigested Terms Plan + full Term-Note Authoring Requirements (multi-source MUST-language mandate) present; best-fit glossary per term. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 13 doc notes + 7 owned terms (term_dictionary AND documentation/); LIKE false-positives confirmed (gateways/Agentspace/summarization/hubs = NOT dup); 4 slugs renamed general→specific (Renamed sub-table); 3 candidate captures removed (Removed sub-table); 11 placeholder term slugs caught + replaced. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 13 notes from repo_*/term_*/entry_* outside the folder + new-term→doc inlinks; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

Re-downloaded mirror `inbox/hermes_agent_docs/` from upstream main HEAD `c253b07` (was pinned `95715dc`).
Independently re-measured all 5 owned pages flagged with upstream growth using the ledger convention (body
words after stripping YAML frontmatter; code blocks = count of `^\s*```` lines ÷ 2). All five measurements
matched the revised manifest exactly. Spot-re-measured 3 unchanged pages (skills 5194/43, tool-gateway 1455/9,
personality 1200/9) — all stable.

Changed pages (old → new):
- `user-guide/features/memory-providers.md` — 3158w/18code → 3407w/18code
- `user-guide/features/curator.md` — 2217w/10code → 2356w/10code
- `user-guide/features/honcho.md` — 2128w/5code → 2505w/5code  **(CROSSED 2500w cap)**
- `user-guide/features/memory.md` — 1948w/10code → 2103w/11code
- `user-guide/features/context-files.md` — 1305w/7code → 1310w/7code

**Density re-decision (1 threshold crossing):** `honcho.md` crossed the 2500w raw cap (2128→2505w). It is owned
by Note 7 (`hermes_memory_providers_honcho`), a **curated fusion** of honcho.md + the memory-providers.md Honcho
entry, projected at ~1950w with ≤6 code blocks (well under the 2500w / 6-code / 400-line caps). The +377w of
honcho.md growth is entirely PROSE (expanded Gateway Identity Mapping, observation/config tables); honcho's code
count is unchanged at 5, and Note 7 already prose-summarizes the full config reference (link-out) and curates code
to ≤6 load-bearing blocks. The pre-existing 2-way split (Note 7 = provider system + Honcho deep architecture;
Note 8 = the other 8 providers) keeps the Honcho content atomic and within caps. **Outcome: still within caps —
NO split added.** Memory.md's +155w and curator.md's +139w growth are immaterial to their already-curated note
estimates (Notes 6 and 9, each ~1500w with ~1000w headroom); context-files.md's +5w is negligible.

Cross-ref floor at the time of this re-sync was ≥8 term + ≥8 snippet + ≥5 doc per planned note. **(Superseded
2026-06-19: FOUR-FLOOR standard set to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note — all counted,
the Augmentation Report.)** No planned-note filename, BB type, or gate altered. Plan remains **READY** for execution.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented FOUR-FLOOR 2026-06-19) · Review: **DONE** (re-reviewed 2026-06-19, 9/9 READY — FOUR-FLOOR) · Execute: pending · Re-synced 2026-06-19 · Cross-ref FOUR-FLOOR set 2026-06-19 (≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc, all counted)

**Source**: `inbox/hermes_agent_docs/user-guide/features/{tools,tool-gateway,skills,curator,memory,memory-providers,honcho,context-files,context-references,personality}.md`, `inbox/hermes_agent_docs/user-guide/skills/google-workspace.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
