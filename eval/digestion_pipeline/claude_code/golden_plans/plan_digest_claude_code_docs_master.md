---
title: External Documentation Digestion Master Plan — Claude Code Docs (code.claude.com)
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
source_index: https://code.claude.com/docs/llms.txt
---

# Master Plan: Digest the Claude Code Documentation into Vault Notes

> **Index hub only** (per `/tessellum-plan-digestion` Step 1e). This file holds shared decisions and the
> sub-plan index. Per-note tables, section coverage maps, and gate tables live in each **self-contained
> sub-plan**, which is authored from a fresh re-read of its source pages and then run through
> `/tessellum-augment-digestion-plan` → `/tessellum-review-digestion-plan` before execution.

## Objective

Digest the official Claude Code documentation (`code.claude.com/docs/en`) — **134 leaf pages**
(104 core + 30 Agent SDK), **457,873 measured words** — into BB-atomic vault notes. Source is far over
the 30-note threshold, so this is a **master + sub-plans** divide-and-conquer: **40 sub-plans**,
**~326 estimated notes**. Out of scope (user, 2026-06-13): `changelog.md` + the 11 `whats-new/*`
weekly digests (release-note material; already excluded from the corpus).

## Source

- **Local mirror (digestion source, NOT vault notes):** `inbox/claude_code_docs/` (134 `.md`, verbatim).
- Re-fetch any page from `https://code.claude.com/docs/en/<slug>.md`.
- Per-page measured stats (words/code-blocks/H2/H3) recorded during planning; **each sub-plan MUST
  re-read its assigned pages** for the section coverage map (measured, not estimated — Step 1c/Step 8).

## Routing Decision (Shared)

- **Location:** `resources/documentation/claude_code/`  **Prefix:** `cc_<topic>_*.md`
- **Rationale (3-criterion):** vendor product documentation, analogous to AWS service docs →
  `resources/documentation/aws_<service>/` (Step 2b). Novelty HIGH (no `claude_code/` folder),
  operational relevance HIGH (team uses Claude Code daily), maintenance MEDIUM. >15-note series ⇒
  dedicated subfolder justified.
- **Undigested terms route to `term_dictionary/`** (Step 4e), NOT to the documentation folder.

## Dedup Policy (Shared) — REQUIRED before authoring ANY note

The vault already covers many agentic/LLM concepts. Before creating **any** planned note —
**documentation concept notes AND term notes alike** (this generalizes the canonical's term-only
Step 4e.2 / augment 10.5f check; a `cc_` *doc* note can duplicate an existing *term* note, which is
exactly the P0 failure) — each sub-plan MUST run the three-way existence check across **both**
`term_dictionary/` AND `resources/documentation/`:

1. **No note** → create.
2. **Stub** → fill-stub.
3. **Substantive note exists (term OR doc)** → **do NOT recreate**; link, or enrich it via `/tessellum-update-feedback`.

**Adversarial dedup-verify (bar-raiser, beyond the canonical):** every DUP verdict that would *delete or
merge* must be confirmed by an independent skeptic pass before applying (the match→2-diverse-verifier
pattern; the canonical does a single existence check, which let the P0 over-merges through).

Known substantive existing notes to link/enrich (not duplicate): `term_claude_code`, `term_mcp`,
`term_subagent`, `term_context_window`, `term_compaction`, `term_sandbox`, `term_skills`,
`term_agent_harness`, `term_autonomous_coding_agents`, `term_regular_checkpointing`,
`term_graduated_trust`, `term_context_engineering`, `term_chain_of_thought`, plus
`resources/documentation/tutorials/tutorial_claude_code_*`.

## Undigested Terms — Corpus-Wide Inventory + Ownership (Step 4e; bar-raiser G-E)

> **Bar-raiser beyond the canonical:** the canonical's Pattern B distributes term capture to each
> sub-plan and relies on per-sub-plan G5 to catch ghosts — which can leave a cross-cutting term owned by
> *no* sub-plan undetected until late. To close that, we ran a **corpus-wide term sweep at master time**
> (the source's own `glossary.md` is the authoritative 45-term vocabulary) and assigned **every** term an
> owner. **Result: 0 orphan terms.**

**Design decision (CC-specific):** Claude Code vocabulary terms are the *subjects of dedicated doc pages*,
so they are digested as **documentation concept notes (`cc_*`) by their home sub-plan**, NOT as
`term_dictionary` term notes. The only `term_dictionary` interaction is **linking existing** terms.
⇒ **0 new `term_dictionary` captures expected** across the whole digestion (each sub-plan's augment still
re-checks via Step 2d; if a genuine cross-cutting vocabulary term with no doc-page home AND no existing
note surfaces, that sub-plan captures it via `/tessellum-capture-term-note` — none found in the sweep).

**Link existing term note (do NOT create):** MCP→`term_mcp` · Subagent→`term_subagent` · Context
window→`term_context_window` · Compaction→`term_compaction` · Sandboxing→`term_sandbox` · Agentic
harness→`term_agent_harness` · Agentic coding→`term_autonomous_coding_agents` · Permission
mode→`term_graduated_trust` · Extended thinking→`term_chain_of_thought`.

**Doc-concept owner (term → home page → owning sub-plan):** Agentic loop/Tool/Turn→B01A · Surface→B01A ·
Verification loop→B01B · Auto memory/Checkpoint/.claude dir/CLAUDE.md/Project trust/Rules/Session→B02B ·
Settings layers→B03A · Effort level/Tool(ref)→B03B · Auto mode/Permission rule/Plan mode→B05A ·
Bundled skills/Command/Output style/Skill→B06 · Hook→B07A/B07B · MCP Tool Search→B08A · Channel→B08B ·
Plugin→B09A · Agent teams→B10A · Worktree isolation→B10B · Bare mode/Non-interactive mode→B11 ·
Dispatch→B12A · Remote Control/Teleport→B12B · Prompt injection→B16 · Managed settings→B14B.

Every sub-plan still runs Step 2d at augment to catch any NEW non-glossary term its pages introduce
(B01A did: surfaced "code intelligence/LSP" → owned by B03B/B09, 0 new captures). No term definition is
ever inlined in a digest note.

## Format Definition (Shared) — aligned to existing `resources/documentation/` notes

Derived from a survey of all **4,624** existing documentation notes (NOT invented). Match exactly.

### YAML frontmatter

**Field order is fixed** — the canonical order across 1,167 docs notes (and required by
`scripts/check_yaml_frontmatter.py`). All values are **itemized lists**, never inline `[...]` arrays
(except `access_control_group`). Year-like strings are quoted.

```yaml
---
tags:                       # itemized; first two ALWAYS resource, documentation
  - resource
  - documentation
  - claude_code
  - <area_tag>              # e.g. hooks, mcp, plugins, agent_sdk, permissions, surfaces
  - <subtopic_tag>          # 0–2 more, optional
keywords:                   # itemized; 5–12 lowercase search phrases (features, flags, commands, synonyms)
  - <feature / flag / command>
  - <concept>
  - <search synonym>
topics:                     # itemized
  - Claude Code
  - <specific area>
language: markdown          # always markdown (4,536/4,624)
date of note: 2026-06-13
status: active              # active (archived/proposal not used here)
building_block: <concept | procedure | model | argument | empirical_observation>
source_url: https://code.claude.com/docs/en/<slug>
access_control_group: ["general"]   # inline quoted list, exactly this
---
```

- **`last_updated` is NOT a YAML field here** — the most common docs ordering (1,167) omits it; the
  "last updated" string lives in the body footer instead (see below). (The 867 notes with a `last updated`
  YAML key are drift — do not copy.)
- **Forbidden fields:** title, category, created, updated, source, parent, author, related_wiki,
  note_second_category.

### Body structure (matches the dominant docs-note headings)

- `# <Descriptive Title>` — topic-based; may mirror the source page H1/section (e.g. `# Claude Code — The Agentic Loop`).
- `## Overview` — 1–2 paragraph summary (the standard opener used by 1,834 notes; **not** `## Definition`).
- **Source-mirrored body H2/H3** — name sections after the source content / standard docs headings:
  concept → `## How It Works`, `## Key Points`; procedure → `## Prerequisites`, `## Steps`/`## Step N`.
  One BB type per note.
- `## Related Notes` — the reference/cross-link section (1,925 notes). **≥6 relevancy-selected
  `term_dictionary/` term notes** (required) + other related notes, each an **indexed link with a term
  description AND its relevancy to this note**:
  `- [Term Name](relative_path.md) — <what the term is>; relevance: <why it matters to this note>`.
  Group sibling `cc_*` first, then `../../term_dictionary/term_*.md`, then other vault notes; correct
  relative depth; reciprocal inbound links added at finalization (G7/G8, anti-island). A bare link with no
  relevancy statement is incomplete.
- `## References` — OPTIONAL, external (non-source) URLs only.
- **Footer** (plain bold lines, NO heading), exactly:
  ```
  **Source**: https://code.claude.com/docs/en/<slug>
  **Last Updated**: 2026-06-13
  **Status**: Active
  ```

One BB type per note. Density caps: ≤400 lines, ≤2500 words, ≤6 code blocks. Validate every note with
`scripts/check_yaml_frontmatter.py` + `scripts/check_note_format.py` (G1).

> This Format Definition **is** the **Documentation-Note Authoring Spec** (G-D — the doc-note analog of
> the canonical's Term-Note Authoring Requirements) and was **derived by surveying existing target-dir
> notes** (G-A), not invented. Every sub-plan inherits it verbatim; do not redefine per sub-plan.

## Sub-Plans Index

| # | Sub-Plan File | Theme | Pages | Words | Notes (est.) | Priority | Status |
|---|---|---|---:|---:|---:|---|---|
| B01A | `plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md` | Foundations & mental model | 5 | 11,732 | 9 | P1 | not started |
| B01B | `plan_digest_claude_code_docs_b01b_working_effectively_and_workflows.md` | Working effectively & workflows | 3 | 9,171 | 8 | P1 | not started |
| B02A | `plan_digest_claude_code_docs_b02a_context_window_and_cost.md` | Context window & cost | 3 | 12,414 | 8 | P1 | not started |
| B02B | `plan_digest_claude_code_docs_b02b_memory_sessions_and_claude_dir.md` | Memory, sessions & .claude dir | 4 | 14,400 | 9 | P1 | not started |
| B03A | `plan_digest_claude_code_docs_b03a_settings_and_environment_variables.md` | Settings & environment variables | 2 | 21,168 | 10 | P1 | not started |
| B03B | `plan_digest_claude_code_docs_b03b_cli_model_and_tools_reference.md` | CLI, model & tools reference | 4 | 15,276 | 12 | P2 | not started |
| B04A | `plan_digest_claude_code_docs_b04a_interactive_mode_and_input.md` | Interactive mode & input | 5 | 12,677 | 9 | P2 | not started |
| B04B | `plan_digest_claude_code_docs_b04b_status_line_and_fullscreen.md` | Status line & fullscreen | 2 | 8,701 | 6 | P2 | not started |
| B05A | `plan_digest_claude_code_docs_b05a_permissions.md` | Permissions | 3 | 9,930 | 8 | P1 | not started |
| B05B | `plan_digest_claude_code_docs_b05b_sandboxing.md` | Sandboxing | 2 | 6,056 | 6 | P2 | not started |
| B06 | `plan_digest_claude_code_docs_b06_skills_commands_output_styles_and_prom.md` | Skills, commands, output styles & prompts | 4 | 18,469 | 11 | P1 | not started |
| B07A | `plan_digest_claude_code_docs_b07a_hooks_reference.md` | Hooks reference | 1 | 21,959 | 10 | P1 | not started |
| B07B | `plan_digest_claude_code_docs_b07b_hooks_guide.md` | Hooks guide | 1 | 6,580 | 4 | P1 | not started |
| B08A | `plan_digest_claude_code_docs_b08a_mcp.md` | MCP | 3 | 12,813 | 8 | P1 | not started |
| B08B | `plan_digest_claude_code_docs_b08b_channels.md` | Channels | 2 | 8,240 | 6 | P2 | not started |
| B09A | `plan_digest_claude_code_docs_b09a_plugins_core.md` | Plugins core | 3 | 14,190 | 9 | P2 | not started |
| B09B | `plan_digest_claude_code_docs_b09b_plugin_marketplaces_and_dependencies.md` | Plugin marketplaces & dependencies | 3 | 9,840 | 7 | P2 | not started |
| B10A | `plan_digest_claude_code_docs_b10a_subagents_and_agent_teams_view.md` | Subagents & agent teams/view | 4 | 20,317 | 12 | P1 | not started |
| B10B | `plan_digest_claude_code_docs_b10b_workflows_worktrees_goal_advisor.md` | Workflows, worktrees, goal, advisor | 4 | 7,076 | 6 | P2 | not started |
| B11 | `plan_digest_claude_code_docs_b11_automation_and_scheduling.md` | Automation & scheduling | 4 | 9,906 | 10 | P2 | not started |
| B12A | `plan_digest_claude_code_docs_b12a_ide_and_desktop_surfaces.md` | IDE & desktop surfaces | 4 | 16,531 | 11 | P2 | not started |
| B12B | `plan_digest_claude_code_docs_b12b_web_and_remote_surfaces.md` | Web & remote surfaces | 4 | 13,671 | 10 | P2 | not started |
| B13A | `plan_digest_claude_code_docs_b13a_chat_browser_and_computer_use.md` | Chat, browser & computer use | 3 | 5,286 | 6 | P2 | not started |
| B13B | `plan_digest_claude_code_docs_b13b_ci_cd_and_code_review.md` | CI/CD & code review | 6 | 12,807 | 9 | P2 | not started |
| B14A | `plan_digest_claude_code_docs_b14a_cloud_model_providers.md` | Cloud model providers | 5 | 9,424 | 8 | P3 | not started |
| B14B | `plan_digest_claude_code_docs_b14b_admin_network_and_auth.md` | Admin, network & auth | 5 | 7,016 | 8 | P3 | not started |
| B15A | `plan_digest_claude_code_docs_b15a_dev_containers_and_large_codebases.md` | Dev containers & large codebases | 2 | 6,376 | 6 | P3 | not started |
| B15B | `plan_digest_claude_code_docs_b15b_monitoring_and_analytics.md` | Monitoring & analytics | 2 | 11,448 | 7 | P3 | not started |
| B16 | `plan_digest_claude_code_docs_b16_security_data_and_compliance.md` | Security, data & compliance | 5 | 7,054 | 7 | P2 | not started |
| B17 | `plan_digest_claude_code_docs_b17_setup_troubleshooting_and_errors.md` | Setup, troubleshooting & errors | 4 | 16,370 | 11 | P2 | not started |
| B18 | `plan_digest_claude_code_docs_b18_adoption_kits.md` | Adoption kits | 2 | 6,121 | 4 | P3 | not started |
| B19A | `plan_digest_claude_code_docs_b19a_sdk_core_and_lifecycle.md` | SDK core & lifecycle | 5 | 11,899 | 11 | P2 | not started |
| B19B | `plan_digest_claude_code_docs_b19b_sdk_sessions_and_system_prompts.md` | SDK sessions & system prompts | 4 | 8,146 | 7 | P2 | not started |
| B19C | `plan_digest_claude_code_docs_b19c_sdk_streaming_and_i_o.md` | SDK streaming & I/O | 4 | 8,804 | 9 | P2 | not started |
| B20A | `plan_digest_claude_code_docs_b20a_sdk_custom_tools_and_mcp.md` | SDK custom tools & MCP | 3 | 7,726 | 7 | P2 | not started |
| B20B | `plan_digest_claude_code_docs_b20b_sdk_skills_commands_and_subagents.md` | SDK skills, commands & subagents | 4 | 8,101 | 6 | P2 | not started |
| B20C | `plan_digest_claude_code_docs_b20c_sdk_hooks_permissions_and_checkpointin.md` | SDK hooks, permissions & checkpointing | 3 | 9,625 | 8 | P2 | not started |
| B21A | `plan_digest_claude_code_docs_b21a_sdk_production_and_hosting.md` | SDK production & hosting | 4 | 9,512 | 8 | P3 | not started |
| B21B | `plan_digest_claude_code_docs_b21b_sdk_python_reference.md` | SDK Python reference | 1 | 15,226 | 7 | P3 | not started |
| B21C | `plan_digest_claude_code_docs_b21c_sdk_typescript_reference.md` | SDK TypeScript reference | 2 | 15,815 | 8 | P3 | not started |

**Total: 40 sub-plans, ~326 estimated notes.** Final counts lock during each sub-plan's augmentation.

## Page → Sub-Plan Assignment (exhaustive — all 134 pages, each assigned once)

- **B01A** (Foundations & mental model): overview.md, how-claude-code-works.md, features-overview.md, platforms.md, glossary.md
- **B01B** (Working effectively & workflows): quickstart.md, best-practices.md, common-workflows.md
- **B02A** (Context window & cost): context-window.md, prompt-caching.md, costs.md
- **B02B** (Memory, sessions & .claude dir): memory.md, sessions.md, checkpointing.md, claude-directory.md
- **B03A** (Settings & environment variables): settings.md, env-vars.md
- **B03B** (CLI, model & tools reference): cli-reference.md, model-config.md, tools-reference.md, debug-your-config.md
- **B04A** (Interactive mode & input): interactive-mode.md, keybindings.md, terminal-config.md, fast-mode.md, voice-dictation.md
- **B04B** (Status line & fullscreen): statusline.md, fullscreen.md
- **B05A** (Permissions): permissions.md, permission-modes.md, auto-mode-config.md
- **B05B** (Sandboxing): sandbox-environments.md, sandboxing.md
- **B06** (Skills, commands, output styles & prompts): skills.md, commands.md, output-styles.md, prompt-library.md
- **B07A** (Hooks reference): hooks.md
- **B07B** (Hooks guide): hooks-guide.md
- **B08A** (MCP): mcp.md, mcp-quickstart.md, managed-mcp.md
- **B08B** (Channels): channels.md, channels-reference.md
- **B09A** (Plugins core): plugins.md, plugins-reference.md, discover-plugins.md
- **B09B** (Plugin marketplaces & dependencies): plugin-marketplaces.md, plugin-dependencies.md, plugin-hints.md
- **B10A** (Subagents & agent teams/view): agents.md, sub-agents.md, agent-teams.md, agent-view.md
- **B10B** (Workflows, worktrees, goal, advisor): workflows.md, worktrees.md, goal.md, advisor.md
- **B11** (Automation & scheduling): routines.md, scheduled-tasks.md, desktop-scheduled-tasks.md, headless.md
- **B12A** (IDE & desktop surfaces): vs-code.md, jetbrains.md, desktop.md, desktop-quickstart.md
- **B12B** (Web & remote surfaces): claude-code-on-the-web.md, web-quickstart.md, remote-control.md, deep-links.md
- **B13A** (Chat, browser & computer use): slack.md, chrome.md, computer-use.md
- **B13B** (CI/CD & code review): github-actions.md, github-enterprise-server.md, gitlab-ci-cd.md, code-review.md, ultraplan.md, ultrareview.md
- **B14A** (Cloud model providers): amazon-bedrock.md, google-vertex-ai.md, microsoft-foundry.md, claude-platform-on-aws.md, llm-gateway.md
- **B14B** (Admin, network & auth): admin-setup.md, third-party-integrations.md, network-config.md, server-managed-settings.md, authentication.md
- **B15A** (Dev containers & large codebases): devcontainer.md, large-codebases.md
- **B15B** (Monitoring & analytics): monitoring-usage.md, analytics.md
- **B16** (Security, data & compliance): security.md, security-guidance.md, data-usage.md, zero-data-retention.md, legal-and-compliance.md
- **B17** (Setup, troubleshooting & errors): setup.md, troubleshoot-install.md, troubleshooting.md, errors.md
- **B18** (Adoption kits): champion-kit.md, communications-kit.md
- **B19A** (SDK core & lifecycle): agent-sdk/overview.md, agent-sdk/quickstart.md, agent-sdk/agent-loop.md, agent-sdk/claude-code-features.md, agent-sdk/migration-guide.md
- **B19B** (SDK sessions & system prompts): agent-sdk/sessions.md, agent-sdk/session-storage.md, agent-sdk/modifying-system-prompts.md, agent-sdk/todo-tracking.md
- **B19C** (SDK streaming & I/O): agent-sdk/streaming-output.md, agent-sdk/streaming-vs-single-mode.md, agent-sdk/structured-outputs.md, agent-sdk/user-input.md
- **B20A** (SDK custom tools & MCP): agent-sdk/custom-tools.md, agent-sdk/mcp.md, agent-sdk/tool-search.md
- **B20B** (SDK skills, commands & subagents): agent-sdk/skills.md, agent-sdk/slash-commands.md, agent-sdk/subagents.md, agent-sdk/plugins.md
- **B20C** (SDK hooks, permissions & checkpointing): agent-sdk/hooks.md, agent-sdk/permissions.md, agent-sdk/file-checkpointing.md
- **B21A** (SDK production & hosting): agent-sdk/hosting.md, agent-sdk/secure-deployment.md, agent-sdk/observability.md, agent-sdk/cost-tracking.md
- **B21B** (SDK Python reference): agent-sdk/python.md
- **B21C** (SDK TypeScript reference): agent-sdk/typescript.md, agent-sdk/typescript-v2-preview.md

## Execution Order (by priority)

- **Phase A (P1 — vocabulary/foundational cores):** B01A, B01B, B02A, B02B, B03A, B05A, B06, B07A, B07B, B08A, B10A — define the concepts (context, memory, settings, permissions, skills, hooks, MCP, subagents) later batches reference.
- **Phase B (P2 — features built on the cores):** B03B, B04A, B04B, B05B, B08B, B09A, B09B, B10B, B11, B12A, B12B, B13A, B13B, B16, B17, B19A, B19B, B19C, B20A, B20B, B20C.
- **Phase C (P3 — enterprise / specialized / SDK language refs):** B14A, B14B, B15A, B15B, B18, B21A, B21B, B21C.

Within a phase, sub-plans are independent and may run in parallel (no cross-sub-plan execution dependency; cross-references are added post-execution).

## Per-Sub-Plan Pipeline (every sub-plan)

1. **Author** via `/tessellum-plan-digestion` Steps 2-8 from a **fresh re-read** of the assigned source pages: derive note format from existing target-dir notes (G-A; already locked in Format Definition above), **dedup-before-create across term_dictionary AND documentation/** (G-B) + adversarial dedup-verify on any merge, section coverage map (every H2/H3 mapped), planned-notes table (filenames + BB + words), per-note Related mapping via `/tessellum-search-notes`, **inlinks (executed, in-degree ≥1 — G7)**, split decisions, Step 2d new-term scan, per-phase **8-GATE** table, density re-assessment.
2. `/tessellum-augment-digestion-plan` — 19-item augmentation checklist.
3. `/tessellum-review-digestion-plan` — 8 checkpoints → READY.
4. `/tessellum-execute-digestion-plan` — multi-agent enrich→validate→fix fleet + post-hoc verify + commit.

## Validation Gates (Shared — 8-GATE, per execution phase of each sub-plan)

G1 Format (`/tessellum-check-note-format`) · G2 Grounding (diff vs source) · G3 Density+Coverage ·
G4 Cross-Reference (links resolve, source_url, entry-point row, inlinks) · G5 Ghost-reference detect +
redirect (DB query per link target) · G6 Broken-link fix (`/tessellum-check-broken-links` →
`/tessellum-fix-broken-links`) ·
**G7 Discoverability (bar-raiser, G-C):** every new note RECEIVES ≥1 inbound link from an existing vault
note **outside** the digest folder — the Inlink Mapping is *executed*, not just planned, and verified by
DB in-degree ≥1. Prevents the graph-island failure (P0: cluster had 0 inbound links yet passed G1–G6).

## Cross-References (Shared — link from sub-plans across the corpus)

Existing vault notes every relevant sub-plan should link (verified present 2026-06-13; complements the
Dedup Policy's "link existing" list): `term_claude_code`, `term_mcp`, `term_subagent`,
`term_context_window`, `term_compaction`, `term_sandbox`, `term_skills`, `term_agent_harness`,
`term_autonomous_coding_agents`, `term_regular_checkpointing`, `term_graduated_trust`,
`term_context_engineering`, `term_chain_of_thought`, `term_react`, `repo_hermes_agent_tools`,
`documentation/tutorials/tutorial_claude_code_*`. Each sub-plan's augment (Step 8) verifies its subset in
the DB (G5) before locking.

## Entry Point Decision + Entry Points to Update (Step 4c)

>30 notes ⇒ **CREATE `0_entry_points/entry_claude_code_docs.md`** (REQUIRED): `building_block: navigation`;
Quick Stats; per-area/per-sub-plan tables mirroring the Sub-Plans Index; `## Related Entry Points`;
`## References` (source + this master). Built as a **pre-step before the first sub-plan executes** (so
each sub-plan can add its rows + each note gets its entry-point back-link), per G-G.

**Entry Points to Update:**
- **CREATE (required):** `0_entry_points/entry_claude_code_docs.md`.
- **UPDATE parent hub:** `0_entry_points/entry_gen_ai_dev.md` — add a back-link row (Claude Code is a
  gen-AI dev tool; confirm this is the best hub at creation, else use the docs index). Without this the
  new entry point is an orphan.
- **UPDATE** `resources/term_dictionary/term_claude_code.md` — add a link to the docs series.
- Each sub-plan **contributes its rows** to `entry_claude_code_docs.md` at execution (not its own entry point).

## Pacing Rules (Shared)

- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script; commit+push per
  sub-plan (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Reindex incrementally after each sub-plan; verify `note_links` + 0 broken links before commit.

## Summary Statistics

- Pages: 134 (104 core + 30 SDK). Words: 457,873. Sub-plans: 40. Est. notes: ~326.
- Building-block skew: concept (mental-model/glossary/architecture), procedure (setup/config/CLI/reference), with some model (agent loop, context window, sandbox isolation) and argument (best-practices/kits).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan (master + sub-plans) | `/tessellum-plan-digestion` | master DONE; B01A DONE; 39 sub-plans pending |
| 2. Augment (per sub-plan) | `/tessellum-augment-digestion-plan` | B01A DONE; 39 pending |
| 3. Review (per sub-plan) | `/tessellum-review-digestion-plan` | B01A READY (9/9); 39 pending |
| 4. Execute (per sub-plan) | `/tessellum-execute-digestion-plan` | pending all |

Per-sub-plan tracker (update as each advances):

| Sub-plan group | Augment | Review | Execute |
|---|---|---|---|
| **Phase A (P1, 11):** B01A, B01B, B02A, B02B, B03A, B05A, B06, B07A, B07B, B08A, B10A | ✅ | ✅ READY | pending |
| **Phase B (P2, 21):** B03B, B04A, B04B, B05B, B08B, B09A, B09B, B10B, B11, B12A, B12B, B13A, B13B, B16, B17, B19A, B19B, B19C, B20A, B20B, B20C | ✅ | ✅ READY | pending |
| **Phase C (P3, 8):** B14A, B14B, B15A, B15B, B18, B21A, B21B, B21C | ✅ | ✅ READY | pending |

**ALL 40 sub-plans READY** (authored → augmented → reviewed, each deterministically verified: ≥6
relevancy-selected term notes/note, 0 undeclared ghosts, all sections, status ready). One declared
Pattern-B new-term capture: `term_prompt_injection` (B16-owned, created at execute before its digest
note). Execute phase pending user greenlight.

## Follow-up Recommendations

- After all phases: full reindex, create `entry_claude_code_docs.md`, run broken-link sweep, update README/CHANGELOG stats, add reciprocal inlinks from related vault notes into the `cc_*` cluster (G7 — avoid the island failure mode).
