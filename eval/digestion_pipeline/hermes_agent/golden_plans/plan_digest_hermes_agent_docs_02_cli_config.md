---
title: Hermes Agent Docs Digestion — Sub-Plan 02 — CLI, TUI, Sessions & Configuration
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/
pages:
  - user-guide/cli.md
  - user-guide/tui.md
  - user-guide/sessions.md
  - user-guide/configuring-models.md
  - user-guide/configuration.md
---

# Sub-Plan 02: CLI, TUI, Sessions & Configuration

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP02's note
> filenames/BBs/coverage are defined.

## Scope

The day-to-day operating surface of Hermes Agent: the classic CLI/REPL, the modern TUI, session
lifecycle (resume / search / storage), interactive model configuration from the dashboard, and the
full `~/.hermes/config.yaml` reference. Source = 5 mirrored pages in `inbox/hermes_agent_docs/`
(all substantive). **P1 / foundational** — `configuration.md` is the single largest page in the whole
corpus (~14K words, 92 code blocks) and is referenced by nearly every downstream sub-plan; it MUST
split into BB-atomic notes by section cluster. Downstream sub-plans link back to
`hermes_config_files_precedence`, `hermes_terminal_backends`, and `hermes_cli_interface`.

## Content Strategy

- **One BB per note.** `configuration.md` mixes a procedural config workflow, a model/architecture
  description of the 6 terminal backends, and many independent setting blocks → split into 6 notes by
  section cluster (see Split Decisions). `sessions.md` → 2, `cli.md` → 2, `tui.md` → 1,
  `configuring-models.md` → 1.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content:
  provider catalog + fallback/credential-pool/provider-routing internals (SP09/SP14), the feature
  pages each setting block configures (skills SP05, memory SP05, cron SP06, delegation SP06, voice/tts/
  browser/web-search/vision SP08, checkpoints/security/worktrees SP03, profiles SP04, context-compression
  developer internals SP18).
- **Collision (augment): `term_configuration_model.md` (129L, active) is a NETWORK-SCIENCE
  random-graph model, NOT Hermes `config.yaml`** — a textbook LIKE false-positive. The planned
  `hermes_config_files_precedence` is NOT a duplicate; create it and do NOT link the unrelated term.
- **Collision: `term_session_persistence.md` (131L, active) covers the generic "sticky sessions"
  concept** — the planned `hermes_sessions_lifecycle_resume` documents Hermes' user-facing
  resume/title/handoff CLI procedure, a different BB scope → LINK, do not drop.
- **Collision: `term_sandbox_backend.md` (88L, active) covers the generic concept** — the planned
  `hermes_terminal_backends` is a model note enumerating Hermes' 6 concrete backends → LINK, not dup.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/configuration.md | 14128 | 92 | MIXED procedure+model+settings | 6 (split) |
| user-guide/sessions.md | 3462 | 24 | procedure | 2 (split) |
| user-guide/cli.md | 2802 | 21 | procedure | 2 (split) |
| user-guide/tui.md | 2514 | 8 | procedure | 1 |
| user-guide/configuring-models.md | 1993 | 9 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **12 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_cli_interface.md` | procedure | cli §Running the CLI, §Interface Layout (+Status Bar, color coding, Resume Display), §Keybindings, §Slash Commands, §Quick Commands, §Preloading Skills, §Skill Slash Commands, §Personalities, §Multi-line Input (+Shift+Enter compat), §Interrupting (+Busy Input Mode, Suspend), §Tool Progress Display, §Quiet Mode | ~1500 | The classic terminal REPL: launch flags, status-bar anatomy + context color thresholds, keybindings, slash/quick/skill commands, personalities, multiline + Shift+Enter compatibility matrix, interrupt/steer/queue + Ctrl+Z suspend, tool-progress feed. |
| 2 | `hermes_cli_session_background.md` | procedure | cli §Session Management (Resuming Sessions, Session Storage, Context Compression), §Background Sessions (How It Works, Results, Use Cases) | ~900 | CLI-side session ops: `--continue`/`--resume` by id/title, SQLite `state.db` storage, the inline compression knobs, and `/background` isolated daemon sessions (config inheritance, non-blocking, multiple tasks). |
| 3 | `hermes_tui_interface.md` | procedure | tui §Launch, §Why the TUI, §Collapsible banner, §Requirements (+External prebuild), §Keybindings, §Slash commands, §Live session switcher, §LaTeX rendering, §Light-terminal detection, §Busy indicator, §Auto-resume, §Status line, §Configuration, §How TUI talks to its gateway, §Reverting | ~1500 | The modern TUI front-end: launch/env/config selection, overlays + collapsible banner, TUI-owned slash commands, live multi-session switcher, LaTeX render, light-theme + indicator config, status line, in-process gateway wiring, fallback to classic CLI. |
| 4 | `hermes_sessions_lifecycle_resume.md` | procedure | sessions §How Sessions Work (+What Counts Toward Context, Session Sources), §CLI Session Resume (Continue/Name/Specific/Recap), §Cross-Platform Handoff, §Session Naming (auto/manual/rules/lineage), §Session Management Commands (list/export/delete/rename/prune/stats) | ~1700 | Session lifecycle: what a session is + what enters context, CLI resume by id/title/lineage + recap panel, `/handoff` cross-platform transfer, titling rules + auto-lineage on compression, and the full `hermes sessions` command set. |
| 5 | `hermes_session_search_storage.md` | model | sessions §Session Search Tool (3 shapes, FTS5 syntax, params, when used), §Per-Platform Session Tracking (gateway keys, shared vs isolated, reset policies), §Storage Locations (+DB Schema), §Session Expiry and Cleanup (auto/manual) | ~1500 | Session data model: the `session_search` FTS5 tool (discovery/scroll/browse shapes), gateway session-key scheme + shared-vs-isolated group sessions + reset policies, `state.db` storage layout/schema (WAL), and auto-prune/vacuum cleanup. |
| 6 | `hermes_configuring_models_dashboard.md` | procedure | configuring-models §The Models page, §Setting the main model, §Setting auxiliary models (+override patterns, per-task, reset), §The "Use as" shortcut, §What gets written, §When does it take effect, §Troubleshooting, §Alternative methods (slash/aliases/`hermes model`/direct edit/REST) | ~1500 | Assigning main + 11 auxiliary model slots from the dashboard: picker columns, common override patterns, the "Use as" shortcut, the `config.yaml` written shape, when changes apply, and CLI/alias/`hermes model`/REST alternatives. |
| 7 | `hermes_config_files_precedence.md` | procedure | configuration §Directory Structure, §Managing Configuration, §Configuration Precedence, §Environment Variable Substitution, §Update Behavior, §Working Directory | ~1300 | Config foundations: the `~/.hermes/` layout, `hermes config` commands, the 4-level precedence chain (CLI > config.yaml > .env > defaults), `${VAR}` substitution rules, `updates.*` behavior, and working-directory resolution per context. |
| 8 | `hermes_terminal_backends.md` | model | configuration §Terminal Backend Configuration (+Backend Overview, Local incl. home_mode, Docker incl. lifecycle/hardening/env-overrides/volumes/cred-forward/host-user/mount-cwd, SSH, Modal, Daytona, Singularity, Common Issues, Remote-to-Host File Sync, Persistent Shell) | ~2400 | The six terminal backends model: where shell commands execute (local/docker/ssh/modal/daytona/singularity), per-backend isolation + setup, Docker container lifecycle/labels/hardening, `home_mode`, remote-to-host file sync on teardown, persistent shell. |
| 9 | `hermes_model_aux_provider_config.md` | procedure | configuration §Provider Timeouts, §Credential Pool Strategies, §Prompt caching, §Auxiliary Models (+interactive, universal pattern, full reference, OpenRouter routing, vision change, provider options, common setups, env legacy), §Reasoning Effort, §Tool-Use Enforcement | ~2300 | Model/provider tuning in config.yaml: provider/model timeouts, credential-pool rotation strategies, always-on prompt caching, the universal provider/model/base_url pattern for the 11 auxiliary slots, reasoning-effort levels, and tool-use enforcement. |
| 10 | `hermes_runtime_context_settings.md` | procedure | configuration §Context Compression (+full ref, common setups, three knobs), §Context Engine, §Iteration Budget Pressure (+API Timeouts), §Context Pressure Warnings, §File Read Safety, §Tool Output Truncation Limits, §Global Toolset Disable, §Git Worktree Isolation | ~2200 | Runtime + context-window knobs: compression thresholds/summarizer model, pluggable context engine, iteration-budget pressure + API timeout layers, context-pressure warnings, file-read/tool-output caps, global toolset disable, and worktree isolation. |
| 11 | `hermes_messaging_media_settings.md` | procedure | configuration §TTS Configuration, §Display Settings (+file-mutation verifier, UI language, runtime footer, per-platform overrides), §Speech-to-Text, §Voice Mode (CLI), §Streaming (CLI + Gateway), §Group Chat Session Isolation, §Unauthorized DM Behavior, §Quick Commands, §Human Delay, §Discord, §Timezone, §Browser, §Web Search Backends | ~2400 | Messaging/media/display config: TTS+STT+voice knobs, display/streaming/footer/UI-language, group-session isolation + unauthorized-DM behavior, quick commands, human delay, Discord/browser/web-search backends, timezone. |
| 12 | `hermes_security_skill_memory_settings.md` | procedure | configuration §Skill Settings (+guard, write approval), §Memory Configuration, §Privacy, §Code Execution, §Security (+tirith), §Website Blocklist, §Smart Approvals, §Checkpoints, §Delegation, §Clarify, §Context Files (SOUL.md/AGENTS.md) | ~2200 | Safety + agency config: skill-write guards/approval, memory limits + write approval, PII privacy redaction, `execute_code` mode, Tirith security scanning + secret redaction, website blocklist, smart approvals, checkpoints, delegation width/depth, clarify, SOUL.md/AGENTS.md context files. |

**SP02 totals:** 12 notes · procedure 10 · model 2 · concept 0 (concepts owned by existing term notes).
5 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 12 · procedure 10 · model 2 · concept 0 (configuration/session/sandbox concepts are existing term notes).
- Source: 5 digested pages (~24.7K words) → ~21.4K words of notes (modest compression via link-outs to feature pages).
- BB mix: procedure 83%, model 17%.

## Section Coverage Map

```
cli.md (2802w)
├── intro + tips (setup --portal, --tui) ───────────────── → Note 1 (link-out TUI=Note 3)
├── Running the CLI / Interface Layout (Status Bar, color, Resume Display) → Note 1 (resume detail→Note 4)
├── Keybindings / Slash Commands / Quick Commands ──────── → Note 1 (full lists→SP20 slash ref)
├── Preloading Skills / Skill Slash Commands / Personalities → Note 1 (skills→SP05)
├── Multi-line Input (+Shift+Enter compat) / Interrupting (Busy/Suspend) → Note 1
├── Tool Progress Display (+Preview Length) / Quiet Mode ── → Note 1
├── Session Management (Resuming, Storage, Context Compression) → Note 2
└── Background Sessions (How It Works / Results / Use Cases) → Note 2
tui.md (2514w) ── ALL sections ──────────────────────────── → Note 3 (web-dashboard→SP10; skins/personality→SP05/08)
sessions.md (3462w)
├── How Sessions Work (What Counts Toward Context, Sources) → Note 4
├── CLI Session Resume (Continue / Name / Specific / Recap) → Note 4
├── Cross-Platform Handoff ─────────────────────────────── → Note 4 (per-platform threading→SP11-13)
├── Session Naming (auto / manual / rules / lineage / messaging) → Note 4
├── Session Management Commands (list/export/delete/rename/prune/stats) → Note 4 (insights→SP21)
├── Session Search Tool (3 shapes / FTS5 / params / when used) → Note 5
├── Per-Platform Session Tracking (keys / shared-vs-isolated / reset) → Note 5
├── Storage Locations (+Database Schema) ───────────────── → Note 5
└── Session Expiry and Cleanup (Automatic / Manual) ────── → Note 5
configuring-models.md (1993w) ── ALL sections ──────────── → Note 6 (Nous Portal→SP14; provider list→SP09/14)
configuration.md (14128w)
├── Directory Structure / Managing Configuration / Configuration Precedence → Note 7
├── Environment Variable Substitution / Update Behavior / Working Directory → Note 7 (providers→SP14; updating→SP01)
├── Terminal Backend Configuration (Overview + 6 backends + lifecycle/hardening/sync/persistent shell) → Note 8 (code-exec→SP08; tools README→SP05)
├── Provider Timeouts / Credential Pool Strategies / Prompt caching → Note 9 (credential-pools/fallback→SP09; providers→SP14)
├── Auxiliary Models (all sub-sections) / Reasoning Effort / Tool-Use Enforcement → Note 9 (minimax/xai/oauth guides→SP15)
├── Context Compression / Context Engine / Iteration Budget / API Timeouts → Note 10 (compression internals→SP18; memory-providers→SP05)
├── Context Pressure Warnings / File Read Safety / Tool Output Truncation / Global Toolset Disable / Git Worktree Isolation → Note 10 (worktrees deep→SP03)
├── TTS / Display Settings (verifier, language, footer, per-platform) / STT / Voice Mode / Streaming → Note 11 (voice/tts→SP08)
├── Group Chat Session Isolation / Unauthorized DM / Quick Commands / Human Delay / Discord / Timezone / Browser / Web Search Backends → Note 11 (browser/web-search→SP08; discord→SP11)
├── Skill Settings (guard, write approval) / Memory Configuration / Privacy / Code Execution → Note 12 (skills→SP05; memory→SP05; code-exec→SP08)
├── Security (tirith) / Website Blocklist / Smart Approvals / Checkpoints → Note 12 (security→SP03; checkpoints→SP03)
└── Delegation / Clarify / Context Files (SOUL.md, AGENTS.md) → Note 12 (delegation→SP06; SOUL/AGENTS→SP05)
```

No source H2/H3 orphaned. All 5 pages fully covered; feature-page detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| cli.md (2802w, 21 code) | Note 1 (interface) + Note 2 (sessions+background) | >2500w; two arcs — interactive REPL surface vs session/background lifecycle. |
| sessions.md (3462w, 24 code) | Note 4 (lifecycle/resume/naming/commands, proc) + Note 5 (search/tracking/storage model) | >2500w; separates the procedural session workflow from the data-model (FTS5 tool + session-key scheme + DB schema). |
| configuration.md (14128w, 92 code, MIXED) | Note 7 (files/precedence) + Note 8 (terminal backends, model) + Note 9 (model/aux/provider) + Note 10 (runtime/context) + Note 11 (messaging/media/display) + Note 12 (security/skill/memory/agency) | >4000w → 6 notes by section cluster; backend section is a distinct `model` BB; each cluster keeps ≤6 curated code blocks (92 source blocks → curate the load-bearing YAML per note). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_config_files_precedence` | `term_configuration_model.md` (129L active) | **NOT a dup** — that term is a *network-science random-graph model* (stub-matching, degree sequence), unrelated to `config.yaml` (classic LIKE false-positive, master caution list) | CREATE; do NOT link the unrelated term. |
| `hermes_terminal_backends` | `term_sandbox_backend.md` (88L active), `term_sandbox`, `term_iframe_sandbox` | **NOT a dup** — those are the generic *concept*; this is a model note enumerating Hermes' 6 concrete backends | CREATE; LINK `term_sandbox_backend`/`term_docker` as related. |
| `hermes_sessions_lifecycle_resume` | `term_session_persistence.md` (131L active, "sticky sessions") | **NOT a dup** — term is the generic concept; this is Hermes' user-facing resume/title/handoff procedure | CREATE; LINK `term_session_persistence`. |
| `hermes_session_search_storage` | `term_fts5`, `term_sqlite_vec` (active) | **NOT a dup** — those are component concepts the note uses | CREATE; LINK both. |
| `hermes_configuring_models_dashboard`, `hermes_model_aux_provider_config` | `term_model_catalog`, `term_provider_plugin`, `term_configuration_model` | **NOT a dup** — `term_configuration_model` is the unrelated graph model; the others are component concepts | CREATE; LINK the two component terms. |
| `hermes_cli_interface`, `hermes_cli_session_background`, `hermes_tui_interface`, `hermes_runtime_context_settings`, `hermes_messaging_media_settings`, `hermes_security_skill_memory_settings` | no substantive term/doc note covers these procedures; no `hermes_agent/` doc notes exist yet | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0 substantive same-concept duplicates** (the 3 LIKE hits are false-positives confirmed by reading the notes). New `hermes_agent/` folder → no doc-doc collisions (SP01 not yet executed; intra-series links resolve at finalization).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Four-floor standard set 2026-06-19 (user directive — supersedes the 2026-06-14 master floor AND the earlier
> 2026-06-19 three-floor wording).** Each note's `## Related Notes` carries FOUR COUNTED groups, all
> relevancy-selected to the note's actual content and each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>     `repo_hermes_agent_*` notes that digest the Hermes SOURCE CODE; for each doc note we pick the repos whose
>     modules implement what the doc documents.
>     Hermes implementation corpus; for each doc note we pick the ≥10 snippets whose CODE this note documents. This
>     is now a COUNTED floor (promoted from the prior labeled "bonus" group and raised from 8 to ≥10) — it is NO
>     LONGER a bonus group.
>   • **≥10 documentation notes** (`../../documentation/`) — sibling `hermes_*` notes in this series (resolve at
>     relevant existing doc notes.
> The prior floor was ≥8 term + ≥8 snippet + ≥5 doc; the intermediate 2026-06-19 wording was ≥8 term + ≥5 code-repo
> (re-verified 2026-06-19; relevance clauses regrounded on the 2026-06-19 re-read of all 5 owned source pages).
> Intra-series doc links (sibling `hermes_*`) resolve at finalization (G5/G8). New Hermes-specific terms owned by
> other SPs (e.g. `term_context_compression`→SP18, `term_credential_pool_rotation`→SP09, `term_voice_mode`→SP08,
> `term_nous_portal`→SP14) are ADDITIONAL forward-refs (+fin), NOT counted to the ≥8 floor (they don't exist yet).

**Note 1 `hermes_cli_interface`**
- Terms (9): term_autonomous_coding_agents — the CLI is the day-to-day surface of an autonomous coding agent; term_agent_harness — the REPL launch/turn loop IS the harness surface; term_persona — `/personality pirate|kawaii|...` + the built-in personality list are CLI-set; term_skills — installed skills auto-register as slash commands and preload via `-s`; term_skill_manifest — skill SKILL.md frontmatter is what becomes a `/skill` command; term_context_window — the status bar shows tokens-used/max with color thresholds; term_session_persistence — the resume display + `--continue`/`--resume` flags surface here; term_subagent — `/background` and the tool-progress feed reflect delegated work; term_markdown — the CLI strips verbose markdown from final replies and previews multi-line pastes. (+fin: term_voice_mode — `/voice on`/`Ctrl+B` recording)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes_cli` package implements the classic REPL, argparse, slash-command dispatch, status bar, keybindings, and personalities this page documents; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the top-level package wiring the `hermes`/`hermes chat` entry points and launch flags; [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skill loading/registration behind `-s` preload and skill slash commands; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the turn loop + interrupt/steer/queue (`busy_input_mode`) the CLI drives; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tool layer whose progress feed and previews the CLI renders.
- Docs (11): [hermes_tui_interface](hermes_tui_interface.md) — sibling: the modern front-end that shares keybindings/slash commands with this REPL; [hermes_cli_session_background](hermes_cli_session_background.md) — sibling: the CLI session/`/background` ops split out of this page; [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — sibling: `/model` + model display in the status bar; [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — sibling: voice/quick-commands/display knobs the CLI reads; [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: where `display.*`/`personalities`/`quick_commands` live; [cc_interactive_mode_keyboard_shortcuts](../claude_code/cc_interactive_mode_keyboard_shortcuts.md) — analogous agent-tool keybinding reference; [cc_interactive_session_features](../claude_code/cc_interactive_session_features.md) — analogous interactive REPL feature surface; [cc_input_modes_and_editing](../claude_code/cc_input_modes_and_editing.md) — analogous multi-line/paste/external-editor input; [cc_cli_commands](../claude_code/cc_cli_commands.md) — analogous CLI command/slash surface; [cc_statusline_setup](../claude_code/cc_statusline_setup.md) — analogous status-line anatomy + customization; [cc_output_styles](../claude_code/cc_output_styles.md) — analogous output-formatting/markdown handling.
- Snippets (12): cli_hermescli_run — the classic REPL entry/main loop the page documents; cli_hermescli_init_repl — REPL init (banner/status-bar/keybinding wiring); cli_hermescli_process_command — the slash/quick-command dispatcher behind `/help`,`/model`,`/skills`,…; cli_hermescli_chat — the per-turn chat handler the prompt drives; cli_hermescli_callbacks — interrupt/steer/queue (`busy_input_mode`) + tool-progress callbacks; cli_main_argparse_root — the `hermes`/`hermes chat` argparse with the launch flags (`-q/--model/--provider/--toolsets/-s/-c/-r/-w/--verbose`); cli_main_cmd_chat — the `chat` subcommand handler; cli_completion — Tab autocomplete / ghost-text autosuggest; cli_skin_apply — applies the active CLI skin used by the status bar + banner; cli_voice — `/voice on`/`Ctrl+B` recording the keybindings table lists; cli_banner_update — the welcome-banner render (model/backend/cwd/tools/skills); cli_attachment_input_bindings — multi-line paste preview + image-paste bindings (`Alt+V`/`Ctrl+V`).

**Note 2 `hermes_cli_session_background`**
- Terms (8): term_session_persistence — `--continue`/`--resume` restore full history from `state.db`; term_subagent — each `/background` prompt spawns a completely separate agent session in a daemon thread; term_multi_agent_systems — multiple background tasks run simultaneously, numbered, non-blocking; term_context_window — the inline compression knobs keep the running session inside the window; term_progressive_summarization — middle turns summarized while first-3/last-20 are preserved; term_fts5 — `state.db` keeps the FTS5 indexes used by `session_search`; term_autonomous_coding_agents — background sessions inherit the agent's model/toolsets/reasoning; term_agent_orchestration — the foreground REPL orchestrates queued/background work. (+fin: term_context_compression)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the CLI session handlers (`--continue`/`--resume`, exit resume hint) and `/background` dispatch; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the conversation loop, `state.db` persistence, and compression entry/strategy this page configures; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the daemon-thread spawn + state-store wiring for isolated background sessions; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway/session-store shared by CLI resume and background results; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the toolset a background agent inherits and runs.
- Docs (10): [hermes_cli_interface](hermes_cli_interface.md) — sibling: the interactive REPL these session ops attach to; [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md) — sibling: the full session lifecycle/resume/lineage model; [hermes_session_search_storage](hermes_session_search_storage.md) — sibling: the `state.db` schema + FTS5 store CLI resume reads; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: the compression thresholds/summarizer the inline knobs reference; [hermes_tui_interface](hermes_tui_interface.md) — sibling: the TUI shares the same `state.db` sessions; [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — analogous background-session hosting; [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — analogous fire-and-forget background dispatch; [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — analogous parallel-agent execution; [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — analogous resume/continue session patterns; [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — analogous account of what survives summarization.
- Snippets (11): cli_hermescli_session_handlers — `--continue`/`--resume` CLI handlers + exit resume hint this page documents; core_conversation_loop_session_persist — the loop that persists each turn to `state.db` so resume can restore it; core_hermes_state — the SQLite `state.db` store backing CLI sessions; core_hermes_state_schema — the sessions/messages/messages_fts schema CLI resume reads; core_conversation_compression_entry — the inline-compression entry point the page's knobs configure; core_conversation_compression_strategy — first-3/last-20 protect + middle summarization the page describes; core_run_agent_cli — spawns the agent run a `/background` daemon session inherits; cli_logs — `agent.log`/`gateway.log` where background results/errors surface; cli_hermescli_callbacks — the `▶ N` background-task tracking + non-blocking foreground callbacks; cli_main_argparse_root — `-c`/`-r`/`--continue`/`--resume` flag parsing; cli_send_cmd — the foreground send path that queues/dispatches while background tasks run.

**Note 3 `hermes_tui_interface`**
- Terms (9): term_agent_harness — the TUI is an alternate front-end backed by the same Python runtime/harness; term_autonomous_coding_agents — it is the recommended way to run the agent interactively; term_persona — `/personality` repaints live and the banner honors persona; term_skills — the Skills banner section + skill slash commands carry over; term_session_persistence — TUI + CLI share `~/.hermes/state.db`, auto-resume via `HERMES_TUI_RESUME`; term_subagent — the `/agents` overlay shows the live subagent tree with kill/pause; term_multi_agent_systems — the live session switcher dispatches several TUI sessions at once; term_context_window — the status line shows the context-compression count + pressure; term_json_rpc — the embedded-dashboard child attaches over a loopback `/api/ws` JSON-RPC control channel. (+fin: term_voice_mode)
- Code-Repos (5): [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the in-process `tui_gateway` + `/api/ws` JSON-RPC transport, render/input/slash workers this page documents; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the Python CLI that launches the Node TUI subprocess and shares slash commands/skins; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `hermes --tui` launch flags, `HERMES_TUI*` env handling, fallback-to-CLI; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway abstraction the in-process TUI gateway specializes; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent turn loop the TUI status line tracks (`starting agent…`/`thinking…`/`running…`).
- Docs (10): [hermes_cli_interface](hermes_cli_interface.md) — sibling: the classic REPL whose keybindings/slash commands the TUI matches; [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md) — sibling: the resume/lineage model shared via `state.db`; [hermes_session_search_storage](hermes_session_search_storage.md) — sibling: the shared session store the switcher lists from; [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — sibling: `display.*` keys (skin/streaming/indicator) the TUI surface reads; [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: there is no TUI-specific config file — it reads standard `config.yaml`; [cc_fullscreen_navigation_and_mouse](../claude_code/cc_fullscreen_navigation_and_mouse.md) — analogous alternate-screen + mouse-driven UI; [cc_fullscreen_rendering](../claude_code/cc_fullscreen_rendering.md) — analogous differential alternate-screen rendering; [cc_interactive_session_features](../claude_code/cc_interactive_session_features.md) — analogous rich interactive session surface; [cc_keybindings_action_reference](../claude_code/cc_keybindings_action_reference.md) — analogous keybinding action map; [cc_statusline_setup](../claude_code/cc_statusline_setup.md) — analogous status-line tracking of agent state.
- Snippets (12): tui_entry — the TUI launch/`--tui`/env-gate entry the page documents; tui_server_render — alternate-screen differential rendering (no-flicker streaming) the "Why the TUI" section cites; tui_server_input — non-blocking input/queue-before-ready composer; tui_server_slash — the TUI-owned slash overlays (`/help`,`/sessions`,`/model`,`/agents`); tui_slash_worker — the worker that runs slash commands as overlays vs inline; tui_transport — the `/api/ws` loopback transport to the in-process gateway; tui_server_jsonrpc — the JSON-RPC control channel the dashboard child attaches over; tui_server_session_boundary — auto-resume / live-session-switcher session boundaries; tui_server_agent_build — builds the agent the status line tracks (`starting agent…`/`thinking…`/`running…`); tui_server_interrupt — the interrupt/cancel path (`interrupted` status); tui_event_publisher — pushes render/status events (compression `🗜️`, background `▶`, YOLO badge); tui_ws_primitives — the loopback WebSocket primitives `HERMES_TUI_GATEWAY_URL` injects into.

**Note 4 `hermes_sessions_lifecycle_resume`**
- Terms (8): term_session_persistence — every conversation is auto-saved; resume by id/title/lineage is the core procedure; term_fts5 — `state.db` carries FTS5 indexes that power resume listing + search; term_subagent — delegated tool calls are part of the stored transcript a resume restores; term_context_window — "What Counts Toward Context" governs what a resumed turn re-sends; term_autonomous_coding_agents — sessions span CLI + 20 messaging sources for one agent; term_progressive_summarization — `/compress` creates the numbered continuation lineage (`#2`/`#3`); term_multi_agent_systems — cross-platform `/handoff` transfers one session across platform adapters; term_agent_orchestration — `hermes sessions` list/export/prune/stats orchestrate the session set. (+fin: term_messaging_gateway)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes sessions` command set (list/export/delete/rename/prune/stats), `/title`, `/handoff`, recap panel; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `state.db` reads/writes, auto-titling thread, compression lineage; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway watcher that claims `/handoff` and re-binds the destination key to the CLI session; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level session-source tagging (cli/telegram/discord/...); [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — the `acp` editor-integration session source listed among platforms.
- Docs (10): [hermes_session_search_storage](hermes_session_search_storage.md) — sibling: the data-model half (FTS5 tool + DB schema + reset policy); [hermes_cli_session_background](hermes_cli_session_background.md) — sibling: CLI-side resume/background ops; [hermes_cli_interface](hermes_cli_interface.md) — sibling: the REPL flags (`-c`/`-r`) + exit resume hint; [hermes_tui_interface](hermes_tui_interface.md) — sibling: the TUI shares the same session store + recap; [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — sibling: auto-titling uses an auxiliary model slot; [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — analogous session-management surface; [cc_sessions](../claude_code/cc_sessions.md) — analogous session lifecycle doc; [cc_sdk_sessions_overview](../claude_code/cc_sdk_sessions_overview.md) — analogous session model overview; [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — analogous list/resume/rename API surface; [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — analogous continue/resume patterns.
- Snippets (11): cli_hermescli_session_handlers — `hermes sessions` list/export/delete/rename/prune/stats + `/title`/`/handoff`/recap the page documents; core_conversation_loop_session_persist — the per-turn persistence that makes a session resumable; core_hermes_state — the `state.db` store holding every session; core_hermes_state_schema — sessions/messages schema (parent_session_id lineage, unique-title index); core_hermes_state_writes — the title/rename/lineage writes auto-titling + `#2`/`#3` lineage perform; cli_send_cmd — the CLI send path resume re-enters; cli_gateway_dispatch — the gateway dispatch that claims `/handoff` and re-binds the destination key; core_run_agent_cli — runs the resumed agent with restored history; core_insights_collection — feeds `hermes sessions stats` + `hermes insights`; cli_hermescli_callbacks — the recap-panel render on resume; cli_main_argparse_root — `-c`/`-r` continue/resume flag parsing.

**Note 5 `hermes_session_search_storage`** (model)
- Terms (9): term_fts5 — the `session_search` tool runs SQLite FTS5 with phrase/boolean/prefix syntax over `messages_fts`; term_information_retrieval — discovery/scroll/browse shapes + bookends reconstruct goal→match→resolution; term_session_persistence — `state.db` is the canonical store for all session messages; term_idempotency — deterministic gateway session keys map a source to a stable session; term_caching — WAL mode + last-prune timestamp shared across processes; term_context_window — bookends+window avoid paying for the whole transcript; term_multi_agent_systems — shared-vs-isolated group sessions + per-platform tracking across adapters; term_subagent — tool-role messages can be searched/excluded via `role_filter`; term_sqlite_vec — the vector-search companion to FTS5 in the SQLite session layer. (+fin: term_messaging_gateway)
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `state.db` schema (sessions/messages/messages_fts), WAL store, and `session_search` tool implementation; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `session_search` is an agent tool exposed in the toolset; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the deterministic gateway session-key scheme + reset policies; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes sessions` storage commands + prune/vacuum on `state.db`; [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the `cron` session source + startup auto-prune sweep this page describes.
- Docs (10): [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md) — sibling: the procedural half this model underpins; [hermes_cli_session_background](hermes_cli_session_background.md) — sibling: CLI resume reads this store; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: compression lineage writes new continuation rows; [hermes_tui_interface](hermes_tui_interface.md) — sibling: the TUI switcher lists from this store; [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling: pre-reset memory save + `sessions.auto_prune` retention; [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — analogous session-store model; [cc_sdk_session_store_setup](../claude_code/cc_sdk_session_store_setup.md) — analogous store setup/schema; [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — analogous session query/management API; [cc_claude_application_data](../claude_code/cc_claude_application_data.md) — analogous on-disk application-data layout; [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — analogous local data-storage/privacy framing.
- Snippets (10): core_hermes_state_schema — the sessions/messages/messages_fts FTS5 schema this model note documents; core_hermes_state — the WAL-mode `state.db` store + `session_search` query layer; core_hermes_state_writes — message inserts that keep FTS5 indexes current; cli_hermescli_session_handlers — `hermes sessions` storage commands (prune/export) + vacuum-after-prune; core_conversation_loop_session_persist — writes each turn that becomes searchable; cli_gateway_dispatch — the deterministic gateway session-key scheme + reset policies the page tabulates; cli_kanban_schema — a sibling SQLite-schema example for the same `state.db`-style store; core_insights_collection — reads the session store for analytics (stats); cli_cron — the `cron` session source + startup auto-prune sweep this page describes; cli_logs — where auto-prune/vacuum sweeps and FTS-insert slowdowns are logged.

**Note 6 `hermes_configuring_models_dashboard`**
- Terms (8): term_model_catalog — the picker's right column is the curated agentic-model list (not the raw `/models` dump); term_provider_plugin — the left column is authenticated providers; per-task `provider` routes the slot; term_llm — main vs the 11 auxiliary model slots; term_multimodal — the Vision aux slot needs a vision-capable model; term_computer_vision — image analysis is the Vision task's job; term_progressive_summarization — the Compression aux slot summarizes context cheaply; term_authentication — a provider shows up only with a working credential; term_oauth_token — OAuth flows (Codex/MiniMax/xAI) open a browser to authenticate the provider. (+fin: term_nous_portal, term_provider_routing)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the provider registry + curated catalog + auxiliary auth resolution the picker reads; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes_cli/model_switch.py` (the shared loader for `/model`, aliases, dashboard Change), `hermes model` picker; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the dashboard web server + `/api/model/*` REST endpoints + `config.yaml` write; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the auxiliary-task dispatch (`auto` → main model → fallback chain) this page assigns; [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — the MCP aux slot routes MCP tool dispatch.
- Docs (10): [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — sibling: the `config.yaml` auxiliary/provider schema the dashboard writes; [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: where `model:`/`auxiliary:` resolve in precedence; [hermes_cli_interface](hermes_cli_interface.md) — sibling: `/model` hot-swaps the running CLI session; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: the compression aux slot pairs with compression knobs; [hermes_terminal_backends](hermes_terminal_backends.md) — sibling: shares the same `config.yaml` settings surface; [cc_model_selection](../claude_code/cc_model_selection.md) — analogous main-model selection; [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — analogous provider/model governance; [cc_fallback_models](../claude_code/cc_fallback_models.md) — analogous fallback-chain behavior the aux `auto` path uses; [cc_authentication](../claude_code/cc_authentication.md) — analogous provider credential/OAuth setup; [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — analogous aggregator/gateway-fronted provider routing.
- Snippets (12): cli_model_switch_entry — `hermes_cli/model_switch.py` shared loader for `/model`/aliases/dashboard Change this page documents; cli_model_switch_swap — the in-place hot-swap `/model` does mid-session; cli_model_switch_validate — validates provider+model before writing `config.yaml`; cli_model_switch_verify — verifies the picked model is reachable/authenticated; cli_models_picker — the two-column provider/model picker (left=auth providers, right=curated list); cli_models_fetch — fetches the per-provider model list (filters the raw `/models` dump); cli_models_normalize — normalizes bare names within an aggregator (the "switched providers on me" case); cli_model_catalog — the curated agentic-model catalog the right column shows; core_auxiliary_auth_resolution — resolves the 11 aux-slot provider/model/auth (`auto`→main→fallback); cli_providers_registry — the authenticated-providers registry the left column reads; cli_main_provider_flows — the OAuth/API-key provider auth flows (`hermes model`); cli_web_app — the dashboard web server + `/api/model/*` REST endpoints + config write.

**Note 7 `hermes_config_files_precedence`**
- Terms (8): term_authentication — `.env` holds secrets (API keys/tokens) and `auth.json` holds OAuth credentials; term_oauth_token — `~/.hermes/auth.json` stores Nous Portal etc. OAuth tokens; term_provider_plugin — `config.yaml` resolves which provider serves model/aux slots; term_model_catalog — `hermes config set model ...` selects from the catalog; term_sandbox_backend — `terminal.backend` is part of the resolved config; term_idempotency — `hermes config migrate`/`check` add missing options idempotently; `${VAR}` left verbatim when unset; term_autonomous_coding_agents — the `~/.hermes/` layout (SOUL.md/skills/cron/sessions) is the agent's home; term_agent_harness — the harness reads the 4-level precedence chain (CLI > config.yaml > .env > defaults).
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes config` commands (view/edit/set/check/migrate) + config loader/schema/validator this page documents; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `HERMES_HOME` resolution, the `~/.hermes/` directory layout, `updates.*` behavior; [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — credential-source resolution (`.env`/`auth.json`) the precedence chain feeds; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent runtime that consumes the resolved config + working-directory rules; [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — `skills.config` namespace + `config migrate` scanning skill settings.
- Docs (10): [hermes_terminal_backends](hermes_terminal_backends.md) — sibling: `terminal.*` is the biggest config cluster; [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — sibling: `model:`/`auxiliary:` settings resolved here; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: `compression`/`agent`/`context` keys; [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling: `security`/`skills`/`memory` keys + SOUL.md/AGENTS.md context files; [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — sibling: the dashboard writes back into this precedence; [cc_settings_files](../claude_code/cc_settings_files.md) — analogous settings-file layout; [cc_settings_scopes_and_precedence](../claude_code/cc_settings_scopes_and_precedence.md) — analogous settings precedence chain; [cc_environment_variables](../claude_code/cc_environment_variables.md) — analogous env-var substitution + override surface; [cc_managed_settings](../claude_code/cc_managed_settings.md) — analogous org-pinned managed config (Hermes Managed Scope); [cc_claude_application_data](../claude_code/cc_claude_application_data.md) — analogous home-directory data layout.
- Snippets (11): cli_config_load — loads `config.yaml` applying the 4-level precedence this page documents; cli_config_loading — the loader internals incl. `${VAR}` substitution rules (kept verbatim when unset); cli_config_schema — the config schema + defaults layer (lowest precedence); cli_config_set — `hermes config set` routing API keys→`.env`, everything else→`config.yaml`; cli_config_migrate — `hermes config migrate`/`check` idempotently adding missing options; cli_config_validate — validates the resolved config; core_hermes_home — `HERMES_HOME` resolution + the `~/.hermes/` directory layout; core_credential_sources — `.env`/`auth.json` credential-source resolution the precedence chain feeds; cli_main_cmd_update — `hermes update` + `updates.*` behavior (stash/discard) this page covers; cli_backup_save — `updates.pre_update_backup` HERMES_HOME zip before updates; cli_dump — `hermes config`/`config show` rendering the resolved config.

**Note 8 `hermes_terminal_backends`** (model)
- Terms (8): term_sandbox_backend — the note enumerates the six concrete backends (local/docker/ssh/modal/daytona/singularity); term_docker — the Docker backend's single persistent container, hardening (`--cap-drop ALL`, `no-new-privileges`, pids-limit), labels, lifecycle, volumes; term_sandbox — cloud sandboxes (Modal/Daytona) snapshot/restore filesystem state; term_ssh — the SSH backend uses ControlMaster + persistent `bash -l` shell; term_iframe_sandbox — the generic sandbox-isolation concept these backends instantiate; term_authentication — backend creds (`MODAL_TOKEN_*`, `DAYTONA_API_KEY`, SSH host/user/key); term_idempotency — label-keyed reuse re-attaches to the same container deterministically; term_autonomous_coding_agents — backends define where the agent's shell commands actually execute. (+fin: term_credential_pool_rotation)
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the `terminal`/file/`execute_code` tools and the backend abstraction that routes each backend; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the `terminal.*` config schema, container lifecycle/orphan-reaper, remote-to-host file sync; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `delegate_task` subagents sharing one container + per-task env overrides; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes doctor`/`hermes config set terminal.backend` + the Common Issues checks; [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — `docker_forward_env` credential forwarding + skill `required_environment_variables` merge.
- Docs (10): [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: `terminal.backend` is set in `config.yaml`; [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling: Docker sandboxing complements the security/approval posture; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: worktree isolation + file-read/tool-output caps; [hermes_cli_interface](hermes_cli_interface.md) — sibling: the banner shows the active terminal backend; [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — sibling: same `config.yaml` settings surface; [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — analogous container-runtime sandboxing; [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — analogous filesystem/network isolation model; [cc_sandbox_environments_comparison](../claude_code/cc_sandbox_environments_comparison.md) — analogous backend comparison matrix; [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — analogous containerized execution setup; [cc_execution_environments](../claude_code/cc_execution_environments.md) — analogous "where commands run" model.
- Snippets (10): cli_config_schema — the `terminal.*` backend config schema (backend/cwd/timeout/home_mode/docker_*/…) this model note enumerates; cli_config_set — `hermes config set terminal.backend docker` etc.; core_credential_sources — backend creds (`MODAL_TOKEN_*`,`DAYTONA_API_KEY`,`GITHUB_TOKEN` forwarding) resolution; cli_doctor_api_connectivity — `hermes doctor` backend connectivity checks (Docker/Modal/SSH) the Common Issues section cites; cli_doctor_primitives — the doctor check primitives behind those backend probes; cli_doctor_auth_dirs — doctor checks for backend auth dirs/files (`~/.modal.toml`, SSH key); core_shell_hooks_allowlist — the command allowlist gating what runs in the backend shell; core_shell_hooks_callback — the shell-hook callback wrapping terminal execution; core_file_safety — file-read safety + remote-to-host file sync the SSH/Modal/Daytona teardown performs; cli_worktree_isolation — worktree isolation pairs with backend isolation for parallel agents.

**Note 9 `hermes_model_aux_provider_config`**
- Terms (8): term_provider_plugin — the universal `provider`/`model`/`base_url` pattern selects/auths a provider per slot; term_model_catalog — aux slots pick from provider catalogs (and the OpenRouter Pareto-Code router); term_llm — the 11 auxiliary slots offload side-jobs from the main LLM; term_prompt_caching — always-on cross-session caching with 1h `cache_control` breakpoints; term_multimodal — the vision aux slot must be a multimodal model; term_computer_vision — `vision_analyze` + browser-screenshot analysis is the vision task; term_round_robin — a credential-pool rotation strategy (`round_robin`/`least_used`/`fill_first`/`random`); term_failover — `api_max_retries` then `fallback_providers` failover; provider/model `*_timeout_seconds`. (+fin: term_credential_pool_rotation, term_provider_routing, term_fallback_provider, term_nous_portal)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — auxiliary-model resolution/normalization/headers/proxy-url, provider timeouts, credential-pool rotation, the universal provider/model/base_url pattern; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — reasoning-effort + tool-use-enforcement injection, the auxiliary-task dispatch; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — prompt-caching breakpoint wiring + `config.yaml` schema for `auxiliary:`/`providers:`; [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — the MCP aux slot routes MCP tool dispatch through a configured model; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes model → Configure auxiliary models` interactive picker.
- Docs (10): [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — sibling: the dashboard front-end for these same aux slots; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: the compression aux slot pairs with compression thresholds + API timeouts; [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: secrets in `.env`, model/aux in `config.yaml`; [hermes_terminal_backends](hermes_terminal_backends.md) — sibling: same `config.yaml` cluster; [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling: the approval aux slot scores dangerous commands; [cc_fallback_models](../claude_code/cc_fallback_models.md) — analogous fallback-chain behavior; [cc_model_selection](../claude_code/cc_model_selection.md) — analogous main/aux model selection; [cc_prompt_caching_mechanism](../claude_code/cc_prompt_caching_mechanism.md) — analogous always-on prompt-caching mechanism; [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — analogous reasoning-effort levels; [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — analogous OpenAI-compatible aggregator/proxy routing.
- Snippets (12): core_auxiliary_auth_resolution — resolves each aux slot's provider/model/auth (the universal pattern + `auto`→main→fallback) this page documents; core_auxiliary_normalization — normalizes the aux `provider`/`model`/`base_url` config shape; core_auxiliary_headers — provider-specific headers for aux calls; core_auxiliary_proxy_url — `base_url` override (custom OpenAI-compatible endpoint) handling; core_credential_pool_selection — the `round_robin`/`least_used`/`fill_first`/`random` rotation strategy selection; core_credential_pool_seeding — seeds the credential pool from multiple keys/tokens; core_credential_pool_dataclass — the credential-pool entry model; core_prompt_caching — always-on `cache_control` 1h-TTL breakpoints this page describes; core_runtime_helpers_reasoning — `reasoning_effort` → `verbosity`/`output_config.effort` mapping; core_chat_helpers_activate_fallback — `api_max_retries` → `fallback_providers` failover the page covers; core_runtime_helpers_switch_client — rebuilds the client on credential rotation / provider timeouts; cli_main_provider_flows — the interactive `hermes model → Configure auxiliary models` picker.

**Note 10 `hermes_runtime_context_settings`**
- Terms (8): term_context_window — compression threshold/`protect_first_n`/`protect_last_n` + file-read/tool-output caps protect the window; term_progressive_summarization — the `compressor` engine is lossy summarization with a summary-model context requirement; term_context_engine — `context.engine: compressor|lcm` is a single-select pluggable engine; term_rate_limiting — `api_max_retries` retries transient rate-limit/5xx before fallback; term_failover — dropping retries to 0 hands off to fallback providers faster; term_caching — read dedup + `_budget_warning` injected into the last tool result to preserve prompt cache; term_autonomous_coding_agents — `agent.max_turns` (iteration budget) + budget-pressure warnings keep the agent productive; term_agent_harness — `agent.disabled_toolsets` + worktree isolation are harness-level runtime knobs. (+fin: term_context_compression)
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — compression entry/strategy, the context-engine ABC, iteration-budget pressure, context-overflow handling; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the `compression`/`context`/`agent`/`tool_output` config schema + API-timeout layers; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — file-read safety, tool-output truncation, concurrent tool executor, global toolset disable; [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the Provider-Plugins context-engine slot (`lcm` etc.) browsed via `hermes plugins`; [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/stale timeouts + retry-then-fallback the API-timeout layers drive.
- Docs (10): [hermes_cli_session_background](hermes_cli_session_background.md) — sibling: the CLI inline compression knobs reference these settings; [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — sibling: the compression aux slot/model + provider timeouts; [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: all these keys live in `config.yaml`; [hermes_terminal_backends](hermes_terminal_backends.md) — sibling: worktree isolation pairs with backend isolation; [hermes_session_search_storage](hermes_session_search_storage.md) — sibling: compression lineage writes continuation sessions; [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — analogous context-window anatomy; [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — analogous compaction-survival rules; [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — analogous token-budget management; [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — analogous per-feature context-cost accounting; [cc_worktree_isolation](../claude_code/cc_worktree_isolation.md) — analogous git-worktree isolation for parallel agents.
- Snippets (12): core_conversation_compression_entry — the `compression.*` threshold/protect_first_n/protect_last_n entry this note's knobs configure; core_conversation_compression_strategy — the lossy-summarization strategy + summary-model context requirement; core_manual_compression_feedback — `/compress` manual-compression path; core_context_engine_abc — the pluggable `context.engine: compressor|lcm` ABC; core_iteration_budget — `agent.max_turns` budget pressure (`_budget_warning` injection at 70%/90%); core_conversation_loop_context_overflow — context-overflow handling when compaction can't keep up; core_file_safety — `file_read_max_chars` read safety + read-dedup; core_tool_executor_concurrent — concurrent tool executor whose output `tool_output.*` caps; core_tool_executor_sequential — the sequential executor path + truncation; core_conversation_loop_rate_limit_recovery — `api_max_retries` retry-before-fallback the API-timeout layers drive; core_rate_limit_tracker — tracks rate-limit/5xx state feeding retry/fallback decisions; core_prompt_builder_environment — injects the env/runtime context the engine manages.

**Note 11 `hermes_messaging_media_settings`**
- Terms (8): term_multimodal — TTS/STT/voice convert across audio/text modalities; term_session_persistence — `group_sessions_per_user` + per-platform session isolation shape stored sessions; term_pii — `privacy.redact_pii` hashes phone/user/chat IDs before the LLM; term_computer_vision — STT/vision aux paths feed multimodal turns; term_persona — `display.personality`/`skin` cosmetic display knobs; term_autonomous_coding_agents — `human_delay`/`unauthorized_dm_behavior` shape gateway agent behavior; term_context_window — `runtime_footer` reports `context_pct`; term_agent_harness — display/streaming/quick-commands are the gateway surface of the harness. (+fin: term_voice_mode, term_text_to_speech, term_messaging_gateway)
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — per-platform display/streaming overrides, group-session isolation, unauthorized-DM, Discord, human-delay, message sanitization; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI voice mode (`/voice`), `display.*` rendering, quick commands; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the `text_to_speech`, web-search backends, and browser toolset these settings configure; [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — TTS/STT provider selection (edge/elevenlabs/openai/...); [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the `tts`/`stt`/`voice`/`display`/`web`/`browser`/`timezone` config schema + privacy redaction.
- Docs (10): [hermes_cli_interface](hermes_cli_interface.md) — sibling: CLI voice/display surface (`/voice`, `/verbose`); [hermes_tui_interface](hermes_tui_interface.md) — sibling: the TUI reads `display.*` (skin/indicator/streaming); [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling: privacy/redaction sits beside security/website-blocklist; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: streaming/display overlap with runtime knobs; [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: all these blocks live in `config.yaml`; [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — analogous voice/dictation input; [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — analogous browser-automation config; [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — analogous web-search/web-extract tool surface; [cc_statusline_json_fields](../claude_code/cc_statusline_json_fields.md) — analogous status/footer field set; [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — analogous PII/data-handling framing.
- Snippets (11): cli_voice — CLI voice mode (`/voice`, `voice.record_key`) the page configures; core_think_scrubber — strips reasoning from streamed/display output (`show_reasoning`/`/verbose`); core_message_sanitization — gateway message sanitization + markdown handling for per-platform display; cli_gateway_dispatch — per-platform display/streaming overrides, group-session isolation, unauthorized-DM, human-delay dispatch; core_redact_patterns — the `privacy.redact_pii` hashing patterns (phone/user/chat IDs); cli_web_app — the web/dashboard display surface + web-search/browser tool wiring; cli_tools_config — the `tts`/`stt`/`web`/`browser` toolset config these blocks set; core_prompt_builder_environment — injects `runtime_footer` fields (`model`/`context_pct`/`cwd`); cli_tools_enable — enables/disables the TTS/STT/web/browser toolsets per platform; cli_tools_policy — the per-platform toolset policy the display overrides layer on; cli_send_cmd — the send path that applies streaming/footer/sanitization to outgoing replies.

**Note 12 `hermes_security_skill_memory_settings`**
- Terms (8): term_prompt_injection — `skills.guard_agent_created` scans skill writes for prompt-injection/exfil patterns; term_pii — `security.redact_secrets` + Tirith secret redaction in tool output/logs; term_skill_manifest — skill SKILL.md frontmatter declares `skills.config` settings; term_skills — `skills.write_approval` gates every agent skill write; term_human_in_the_loop — smart approvals + memory/skill write approval stage changes for review; term_subagent — `delegation.max_concurrent_children`/`max_spawn_depth` bound spawned subagents; term_multi_agent_systems — the delegation tree (orchestrator/leaf, up to 27 leaves) is a multi-agent topology; term_sandbox_backend — `code_execution.mode`/Tirith + Docker sandboxing form the execution-safety posture. (+fin: term_credential_pool_rotation, term_context_compression)
- Code-Repos (5): [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — `skill_manage` write guards, `skills.write_approval` staging, skill frontmatter/config; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — memory config/limits, SOUL.md/AGENTS.md context-file loading, smart-approval scoring, clarify, and the delegation tree (width/depth/orchestrator); [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — Tirith pre-execution scanning, secret redaction, website blocklist, `execute_code` mode, checkpoints; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the `security`/`skills`/`memory`/`privacy`/`approvals`/`delegation` config schema; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `/skills pending|approve` and `/memory pending|approve` review commands.
- Docs (10): [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling: all these blocks resolve in `config.yaml`/`.env`; [hermes_terminal_backends](hermes_terminal_backends.md) — sibling: Docker/sandbox backends are the execution-isolation half of safety; [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — sibling: privacy/PII redaction sits beside the gateway display settings; [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling: the approval aux model + iteration-budget guardrails; [hermes_session_search_storage](hermes_session_search_storage.md) — sibling: pre-reset memory save persists to the session store; [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — analogous prompt-injection defenses; [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — analogous approval/permission rule system; [cc_security_architecture](../claude_code/cc_security_architecture.md) — analogous overall security architecture; [cc_memory_overview](../claude_code/cc_memory_overview.md) — analogous persistent-memory model; [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — analogous project context files (SOUL.md/AGENTS.md/CLAUDE.md).
- Snippets (12): core_redact_patterns — `security.redact_secrets` + Tirith secret redaction in tool output/logs; cli_security_advisories — the security-advisory/website-blocklist surface; core_skill_utils_frontmatter — skill SKILL.md frontmatter declaring `skills.config` settings; core_skill_commands_discovery — skill discovery behind `skills.guard_agent_created` write scanning; core_skill_preprocessing — skill-content preprocessing the write-guard inspects; cli_skills_hub — the `/skills pending|approve` review surface for staged skill writes; cli_memory_setup — `memory.*` limits + `memory.write_approval` (`/memory pending|approve`); core_shell_hooks_allowlist — the command allowlist behind `code_execution.mode`/smart approvals; core_tool_guardrails_schema — the tool-guardrail/approval schema (smart approvals, checkpoints); core_credential_sources — `.env`/`auth.json` secrets the security posture protects; core_tool_dispatch_helpers — the dispatch guardrails that route `delegate_task` width/depth limits; core_prompt_builder_context_loaders — loads SOUL.md/AGENTS.md context files this section configures.

All 12 notes meet the FOUR-FLOOR standard: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc. **Term IDs (8-9/note)**
regrounded on the 2026-06-19 re-read). **Code-repo IDs (5/note)** are under `areas/code_repos/` — drawn from the 13
under `resources/code_snippets/` with the `snippet_hermes_agent_` prefix are now a COUNTED floor (promoted from the
mix sibling `hermes_*` notes in this series (resolve at finalization per G5/G8) with analogous `claude_code/cc_*`
**Two placeholder term slugs were caught at finalization (`term_environment_variable_substitution_*`,

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; re-measured 2026-06-19 mirror c253b07)

Re-read all 5 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 cli-interface | procedure | 1500 | ≤6 (curate from 21 short blocks; tables in prose) | ✓ |
| 2 cli-session-background | procedure | 900 | ≤6 (from cli session/bg blocks) | ✓ |
| 3 tui-interface | procedure | 1500 | 6 | ✓ |
| 4 sessions-lifecycle | procedure | 1700 | ≤6 (curate from sessions resume/naming/command blocks) | ✓ |
| 5 session-search-storage | model | 1500 | ≤6 (from 3-shape + schema blocks) | ✓ |
| 6 configuring-models | procedure | 1500 | 6 | ✓ |
| 7 config-files-precedence | procedure | 1300 | 6 | ✓ |
| 8 terminal-backends | model | 2400 | ≤6 (curate from ~30 backend YAML blocks; one canonical block per backend) | ✓ |
| 9 model-aux-provider | procedure | 2300 | ≤6 (curate from ~25 aux YAML blocks) | ✓ |
| 10 runtime-context | procedure | 2200 | ≤6 (curate from compression/budget/output blocks) | ✓ |
| 11 messaging-media | procedure | 2400 | ≤6 (curate from tts/display/streaming/web blocks) | ✓ |
| 12 security-skill-memory | procedure | 2200 | ≤6 (curate from skill/memory/security/delegation blocks) | ✓ |

No further splits needed — all 12 notes are ≤2500w. Notes 8-12 (the configuration.md cluster) are
dense but each is a single BB cluster ≤2500w; the 92 source code blocks are curated to ≤6 load-bearing
YAML examples per note, with the rest summarized in prose (kept blocks verbatim). Borderline notes (8/9/10/11/12
at ~2200-2400w) were checked for further split: each is one topically-cohesive cluster with no BB mixing
→ KEEP (per review CP6 default-to-keep justification). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** — all four COUNTED, four-floor standard set 2026-06-19) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP02)

**SP02 owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every Hermes-specific
concept SP02 touches is owned by another sub-plan (link at finalization) or is an existing verified term.
Augment re-read surfaced **0 new** undigested terms that SP02 should own — the config page's settings each
configure a feature whose concept-term is owned by the feature's home sub-plan.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_context_compression` | LINK only (forward-ref, +fin) | SP18 | dual-threshold compaction is a developer-internals concept; SP02 configures it, SP18 owns it. |
| `term_credential_pool` (rotation) | LINK only (+fin) | SP09 | SP02 sets the rotation *strategy* knob; concept home is SP09 credential-pools. |
| `term_provider_routing`, `term_fallback_provider` | LINK only (+fin) | SP09 | configured in config.yaml but conceptually owned by SP09 protocols/providers. |
| `term_voice_mode`, `term_text_to_speech`, `term_speech_to_text`, `term_browser_automation` | LINK only (+fin) | SP08 | SP02 holds the config blocks; concept homes are SP08 media/web tools. |
| `term_nous_portal`, `term_tool_gateway` | LINK only (+fin) | SP14 / SP05 | referenced in setup/model pages; captured by their owners. |
| `term_messaging_gateway` | LINK only (+fin) | SP11 | gateway session/streaming settings; concept owned by SP11. |

### Renamed (general → specific)

— (audit performed; SP02 owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP02 links; all are already scope-qualified by their owners.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_hermes_config` / config-files concept | none substantive (`term_configuration_model` is an UNRELATED graph model, 129L) | No removal — SP02 was never going to capture this; doc note `hermes_config_files_precedence` created instead. |
| `term_terminal_backend` (would duplicate) | `term_sandbox_backend.md` (88L, active) | Not captured — link the existing term from the `hermes_terminal_backends` doc note. |
| `term_session` (would duplicate) | `term_session_persistence.md` (131L, active) | Not captured — link the existing term from the sessions doc notes. |

## Term-Note Authoring Requirements

N/A (inherited) — SP02 owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP05/08/09/11/14/18). The full
diversity, MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12,
backlink expansion, >200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (CLI/TUI surface, P1-hub pilot):** Notes 1, 2, 3. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (sessions + models):** Notes 4, 5, 6. GATE G1–G8.
- **Phase 3 (configuration cluster):** Notes 7, 8, 9, 10, 11, 12. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_cli_interface hermes_cli_session_background hermes_tui_interface hermes_sessions_lifecycle_resume hermes_session_search_storage hermes_configuring_models_dashboard hermes_config_files_precedence hermes_terminal_backends hermes_model_aux_provider_config hermes_runtime_context_settings hermes_messaging_media_settings hermes_security_skill_memory_settings; do
```

## Entry Point Decision (inherited)

Contributes 12 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "CLI, TUI, Sessions & Configuration" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP02 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_cli.md` | → `hermes_cli_interface`, `hermes_cli_session_background` | CLI repo ↔ CLI usage docs |
| `repo_hermes_agent_tui_gateway.md` | → `hermes_tui_interface` | TUI/gateway repo ↔ TUI usage doc |
| `repo_hermes_agent.md` | → `hermes_config_files_precedence`, `hermes_terminal_backends` | implementation ↔ config/backend usage |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_model_aux_provider_config`, `hermes_configuring_models_dashboard` | provider adapters ↔ model/provider config docs |
| `repo_hermes_agent_agent_core.md` | → `hermes_runtime_context_settings`, `hermes_session_search_storage` | agent core (compression/sessions) ↔ runtime/session docs |
| `term_session_persistence.md` | → `hermes_sessions_lifecycle_resume`, `hermes_session_search_storage` | concept term → user-facing session docs |
| `term_sandbox_backend.md` | → `hermes_terminal_backends` | concept term → the 6-backend model doc |
| `term_configuration_model.md` | (NO inlink — unrelated graph model) | confirmed false-positive; do NOT link |
| `entry_code_snippets_hermes_agent.md` | → `hermes_cli_interface`, `hermes_config_files_precedence` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 12 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_cli_interface`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note —
do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6 load-bearing
YAML examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split.
If multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP02 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 12 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1 wave: cross-link the configuration.md cluster (Notes 7-12) from the feature pages they configure
  once those SPs land (SP05/06/08/09/18) — bidirectional config↔feature links.
- Consider one `thought_` note comparing Hermes' docs-stated config model vs the code-digestion findings in
  `snippet_hermes_agent_cli_config_*`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (3 LIKE false-positives confirmed by reading the notes),
  finalized Per-Note Mapping (now FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc, all counted +
  G5 ghost + G8 scripts, Inlinks.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  intermediate 2026-06-19 three-floor wording (≥8 term / ≥5 code-repo / ≥10 doc with snippets as bonus): the snippet
  group is PROMOTED from bonus to a counted floor and raised from 8 to ≥10. Re-read all 5 owned source pages
  (`inbox/hermes_agent_docs/user-guide/{cli,tui,sessions,configuring-models,configuration}.md`) to reground every
  relevance clause; the Code-Repos (5/note) group is from the 13 `repo_hermes_agent_*` source-code notes and Docs are
  ≥10/note (sibling `hermes_*` + analogous `claude_code/cc_*`). Every cited term ID, code-repo ID, snippet ID, and
  `cc_*` doc ID re-verified DB-active 2026-06-19 (sibling `hermes_*` resolve at finalization).
- Density re-read: counts match measured; **no additional splits** beyond the planned 10 (cli→2, sessions→2,
  config→6). All 12 notes ≤2500w; code-heavy config notes curated to ≤6 blocks.
- Collision audit: **0 removals** — `term_configuration_model` (graph model), `term_session_persistence`,
  `term_sandbox_backend` are all LINK-not-dup; no doc note duplicates an existing term/doc note.
- Term placeholder catch: **2 non-existent term slugs caught at finalization** (`term_environment_variable_substitution_*`,
- Undigested terms surfaced at augment: **0 new** (SP02 owns 0 captures; all concepts owned by other SPs).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (FOUR-FLOOR:
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (N/A — 0 owned;
audit noted) ✓ Slug Collision (3 LIKE false-positives + 2 placeholders caught) ✓ dedup generalized to ALL
notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓ Doc-Note
Authoring Spec derived ✓). Term-capture items are N/A-pass (SP02 owns 0 captures); dedup/collision items are
substantively PASS (audit performed on all 12 doc notes).

## Review Sign-Off

**Re-reviewed 2026-06-19 (FOUR-FLOOR independent review) — READY FOR EXECUTION (9/9 checkpoints pass).**
(Prior: Reviewed 2026-06-15 — READY 9/9. Re-augmented to the four-floor standard 2026-06-19, then independently
re-reviewed: CP1 evaluated against ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note. Floor audit — all 12
notes counted: terms 8-9 ✓, code-repos 5 ✓, snippets 10-12 ✓, docs 10-11 ✓. Anti-fabrication DB spot-check —
active 2026-06-19; the only term slugs not in the DB are the 8 explicitly-labeled `(+fin: …)` forward-refs
owned by other SPs, which are correctly NOT counted to the floor. Source re-measure — configuration 14129/92,
configuring-models 1993/9, cli 2802/21, tui 2514/8, sessions 3462/~23: measured == plan. No fabricated links found.)

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes step (FOUR-FLOOR) | PASS | Per-note mapping FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc each (all counted), every link carries a relevance clause (no bare links). Independent floor count 2026-06-19: terms 8-9/note, code-repos 5/note, snippets 10-12/note, docs 10-11/note — all ≥ floor. Anti-fab DB spot-check: 102 cited snippet ids + 46 counted term slugs + 12 code-repo ids + 52 `cc_*` doc ids ALL DB-active 2026-06-19; 8 non-DB term slugs are all `(+fin)` forward-refs, NOT counted. Four-floor set 2026-06-19 (snippets promoted from bonus to a counted ≥10 floor; supersedes the original ≥8 term + ≥8 snippet + ≥5 doc and the intermediate three-floor wording), exceeds the master ≥6 floor. |
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (12 rows under a CLI/TUI/Config section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 12 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | configuration.md→6, sessions→2, cli→2; all notes ≤2500w; code-heavy notes curated ≤6; dense config notes (8-12) checked → cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15; re-measured 2026-06-19 (mirror c253b07): configuration 14128 (largest in corpus), sessions 3462, cli 2802, tui 2514, configuring-models 1993 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP02 owns 0 term captures (all concepts owned by SP05/08/09/11/14/18); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 12 doc notes (term_dictionary AND documentation/); 3 LIKE false-positives confirmed (graph-model/session-persistence/sandbox-backend = LINK not dup); 2 placeholder term slugs caught + replaced; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 12 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from NousResearch/hermes-agent `website/docs/` at main HEAD `c253b07` (was pinned
`95715dc`); SP02's owned pages independently re-measured (body-word + code-fence/2 convention). Two of
SP02's five pages grew upstream:

- user-guide/configuring-models.md — 1911w/8code → 1993w/9code
- user-guide/configuration.md — 13991w/90code → 14128w/92code

The other three pages re-measured stable (unchanged): cli.md 2802w/21code, tui.md 2514w/8code,
sessions.md 3462w/24code. All five fresh-file measurements match the re-sync manifest exactly (no discrepancy).

**Density re-decision: none.** configuring-models.md (+82w/+1code) still maps to a single ~1500w
procedure note (Note 6) capped at ≤6 curated code — comfortably under the 2500w/6code/400line caps.
configuration.md (+137w/+2code) was already split into 6 section-cluster notes (Notes 7–12); the small
growth touches no single cluster's cap, and the +2 code blocks remain inside the "curate to ≤6 load-bearing
YAML per note" budget. **No new split added; no planned-note filename, BB, or section-cluster boundary changed.**

Cross-ref floor was ≥8 term + ≥8 snippet + ≥5 doc per planned note at re-sync; **subsequently set 2026-06-19 to
the FOUR-FLOOR standard — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per planned note, all counted** (snippets
promoted from bonus to a counted ≥10 floor) — see the Per-Note Related Notes Mapping and Augmentation Report. Plan
remains **READY** for execution.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented to FOUR-FLOOR 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed FOUR-FLOOR 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/{cli,tui,sessions,configuring-models,configuration}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
