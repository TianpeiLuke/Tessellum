---
title: Hermes Agent Docs Digestion — Sub-Plan 20 — Reference: Commands
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/reference/
pages:
  - reference/cli-commands.md
  - reference/slash-commands.md
  - reference/profile-commands.md
---

# Sub-Plan 20: Reference: Commands

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP20's note
> filenames/BBs/coverage are defined.

## Scope

The **command-reference catalogs** of the Hermes Agent docs: the authoritative `hermes <command>`
terminal-command reference, the interactive-CLI + messaging slash-command reference, and the
profile-command reference. These are pure reference catalogs — they enumerate every command, its
subcommands, flags, and options — so each note is a `navigation`/reference table that maps directly
down to the existing `cli_*` snippet corpus (the implementation layer) and links the concept terms
(MCP, ACP, cron, OAuth, kanban, …) the commands act on. Source = 3 mirrored pages in
`inbox/hermes_agent_docs/reference/` (all substantive). **P3 / reference** — downstream sub-plans link
back here for "what command does X". SP20 owns **0 term captures** (reference catalogs introduce no new
concept the command pages are the home for — every command's concept-term is owned by its feature SP).

## Content Strategy

- **One reference catalog per note.** `cli-commands.md` (10819w / 73 code) is the largest reference
  page in the corpus and far exceeds the density caps → **split into 3** by command family
  (chat/model/gateway/setup · session/config/skills/tools · ops/maintenance/auth). `slash-commands.md`
  (3598w / 4 code) → **split into 2** (interactive CLI slash · messaging slash). `profile-commands.md`
  (2358w / 31 code) → **1**. **6 notes.**
- **Do NOT duplicate** the feature pages each command drives → **link-outs**, not copied content: the
  feature behavior of cron (SP06), kanban (SP06), skills/curator/memory (SP05), MCP/ACP/fallback/
  credential-pools/proxy/portal (SP09/SP14), voice/tts/browser (SP08), profiles concept (SP04),
  checkpoints/security/secrets/worktrees (SP03), dashboard (SP10), sessions/config (SP02), each
  messaging platform (SP11–13). The reference note lists the command surface; the feature note explains
  the behavior.
- **Collision (augment): no Hermes command term/doc note exists.** `term_command_pattern.md` is the GoF
  design pattern (unrelated); `term_ada_cli`/`term_kiro_cli`/`term_sam_cli`/`term_bones_cli` are other
  tools' CLIs — all LIKE false-positives, do NOT link. The Claude Code command-reference notes
  (`cc_cli_commands`, `cc_commands_reference`, `cc_sdk_slash_commands`) are the closest **analogous**
  existing doc notes (sibling agent-tool command refs) → LINK as cross-folder analogues, not dups.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| reference/cli-commands.md | 10819 | 73 | navigation (command reference) | 3 (split) |
| reference/slash-commands.md | 3598 | 4 | navigation (command reference) | 2 (split) |
| reference/profile-commands.md | 2358 | 31 | navigation (command reference) | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **6 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_cli_commands_chat_provider.md` | navigation | cli-commands §Global entrypoint (+Global options), §Top-level commands (chat/model/fallback/gateway/proxy/lsp/setup/portal partial), §`hermes chat` (+`-z` scripted one-shot), §`hermes model` (+`/model` mid-session contrast), §`hermes gateway`, §`hermes lsp`, §`hermes setup`, §`hermes portal`, §`hermes proxy`, §`hermes fallback`, §`hermes security` | ~1500 | Reference for the chat/provider/gateway command family: the global `hermes [opts] <cmd>` entrypoint + global flags, the top-level command index, and detailed flag tables for `chat`(+`-z`)/`model`(vs `/model`)/`gateway`/`lsp`/`setup`(+`--portal`)/`portal`/`proxy`/`fallback`/`security`. |
| 2 | `hermes_cli_commands_session_ops.md` | navigation | cli-commands §`hermes status`, §`hermes sessions`, §`hermes insights`, §`hermes config`, §`hermes skills`, §`hermes bundles`, §`hermes curator`, §`hermes memory`, §`hermes tools`, §`hermes kanban`, §`hermes prompt-size`, §`hermes doctor`, §`hermes dump`, §`hermes debug` | ~1500 | Reference for the session/config/skills/tools command family: `status`/`sessions`/`insights` analytics, `config` subcommands, `skills`+`bundles`+`curator`+`memory`+`tools` management, the full `kanban` board surface (boards/tasks/dispatch), and the `prompt-size`/`doctor`/`dump`/`debug` diagnostics. |
| 3 | `hermes_cli_commands_ops_maintenance_auth.md` | navigation | cli-commands §`hermes auth` (+login/logout deprecated), §`hermes secrets`, §`hermes migrate`, §`hermes cron`, §`hermes webhook`, §`hermes hooks`, §`hermes mcp`, §`hermes acp`, §`hermes plugins`, §`hermes pairing`, §`hermes computer-use`, §`hermes claw`, §`hermes backup`/`import`, §`hermes checkpoints`, §`hermes logs`, §`hermes dashboard`, §`hermes whatsapp`/`slack`/`send`, §`hermes completion`, §`hermes update`, §Maintenance commands (version/postinstall/uninstall) | ~1700 | Reference for the ops/maintenance/auth command family: credential + secret commands (`auth`/`secrets`/`pairing`), event/automation surfaces (`cron`/`webhook`/`hooks`/`mcp`/`acp`/`plugins`), backup/checkpoint/log/migrate ops, messaging ops (`send`/`whatsapp`/`slack`), and lifecycle (`update`/`postinstall`/`uninstall`/`completion`/`dashboard`/`computer-use`/`claw`). |
| 4 | `hermes_slash_commands_interactive_cli.md` | navigation | slash-commands §intro (two surfaces, COMMAND_REGISTRY), §Permissions and admin/user split, §Interactive CLI slash commands (Session/Configuration/Tools&Skills/Info/Exit), §Dynamic CLI slash commands, §Quick Commands, §Custom model aliases, §Alias Resolution | ~1300 | Reference for the in-chat **interactive CLI** slash commands: the `COMMAND_REGISTRY`-driven autocomplete surface grouped Session/Config/Tools&Skills/Info/Exit, dynamic `/<skill-name>` commands, user-defined quick commands + custom model aliases (config YAML), and prefix alias-resolution rules; plus the admin/user `user_allowed_commands` split. |
| 5 | `hermes_slash_commands_messaging.md` | navigation | slash-commands §Messaging slash commands, §Notes (CLI-only vs messaging-only vs both surface matrix), §Confirmation prompts for destructive commands | ~1100 | Reference for the **messaging-gateway** slash commands (Telegram/Discord/Slack/Signal/Email/Teams/…): the built-in messaging command table, the surface matrix (which commands are CLI-only / messaging-only / both), and the destructive-command confirmation modal (`/clear`,`/new`,`/undo`,`/exit --delete`) + inline-skip + `approvals.destructive_slash_confirm`. |
| 6 | `hermes_profile_commands_reference.md` | navigation | profile-commands §`hermes profile` (+list/use/create/describe/delete/show/alias/rename/export/import), §Distribution commands (install/update/info, private distributions, distribution.yaml manifest, publishing), §`hermes -p`/`--profile`, §`hermes completion` (profile completions) | ~1300 | Reference for the profile-command surface: every `hermes profile` subcommand (create/clone/describe/alias/export/import) and arguments, the distribution commands (install/update/info from a git repo, `distribution.yaml` manifest, private distributions, publishing), the `-p`/`--profile` global override, and profile-aware shell completions. |

**SP20 totals:** 6 notes · navigation 6 · concept 0 (command concepts owned by feature SPs; no new term notes).
3 source pages digested (all substantive), 0 skipped. Owned captures: **0**.

## Summary Statistics & Building Block Distribution

- Notes: 6 · navigation 6 · concept 0 · procedure 0.
- Source: 3 digested pages (~16.7K words) → ~8.4K words of notes (heavy compression: reference tables
  condense to scannable command/flag tables + link-outs to the feature pages that explain behavior).
- BB mix: navigation 100% (pure command-reference catalogs — the master's "BB navigation/model — command
  reference tables" classification resolves to navigation for all 6, since each note is a routing/index
  surface over the command corpus, not an architecture/data-model description).

## Section Coverage Map

```
cli-commands.md (10819w, 73 code)
├── Global entrypoint (+Global options table) ─────────────── → Note 1
├── Top-level commands (master index table) ───────────────── → Note 1 (links forward to Notes 2/3 for the ops/session families)
├── hermes chat (+options, examples) / hermes -z (scripted) ─ → Note 1
├── hermes model (+/model mid-session contrast) ───────────── → Note 1 (provider setup→SP14; /model slash→Note 4)
├── hermes gateway / hermes lsp / hermes setup / hermes portal → Note 1 (gateway behavior→SP11; lsp→SP08; portal→SP14)
├── hermes proxy / hermes fallback / hermes security ──────── → Note 1 (proxy/fallback→SP09; security audit→SP03)
├── hermes status / hermes sessions / hermes insights ─────── → Note 2 (sessions detail→SP02; insights→SP21)
├── hermes config ─────────────────────────────────────────── → Note 2 (config.yaml ref→SP02)
├── hermes skills / hermes bundles / hermes curator / hermes memory → Note 2 (skills/curator/memory feature→SP05)
├── hermes tools / hermes kanban ──────────────────────────── → Note 2 (kanban feature→SP06; tools→SP05)
├── hermes prompt-size / hermes doctor / hermes dump / hermes debug → Note 2
├── hermes auth (+login/logout deprecated) ────────────────── → Note 3 (credential-pools→SP09; OAuth→SP09)
├── hermes secrets / hermes migrate / hermes pairing ──────── → Note 3 (bitwarden→SP03; pairing→SP11)
├── hermes cron / hermes webhook / hermes hooks ───────────── → Note 3 (cron/hooks feature→SP06; webhook→SP12)
├── hermes mcp / hermes acp / hermes plugins ──────────────── → Note 3 (mcp/acp→SP09; plugins→SP06)
├── hermes computer-use / hermes claw ─────────────────────── → Note 3 (computer-use→SP08; claw migrate→SP17)
├── hermes backup / hermes import / hermes checkpoints / hermes logs → Note 3 (checkpoints→SP03)
├── hermes dashboard / hermes whatsapp / hermes slack / hermes send → Note 3 (dashboard→SP10; messaging→SP11-13)
├── hermes completion / hermes update / Maintenance (version/postinstall/uninstall) → Note 3 (update detail→SP01)
└── See also (link list) ──────────────────────────────────── → Notes 1-3 footer (resolved as Related Notes)
slash-commands.md (3598w, 4 code)
├── intro (two surfaces, COMMAND_REGISTRY, skills as slash) ─ → Note 4
├── Permissions and admin/user split ──────────────────────── → Note 4 (per-platform ACL→SP11)
├── Interactive CLI slash commands (Session/Config/Tools&Skills/Info/Exit) → Note 4 (goals→SP06; voice→SP08)
├── Dynamic CLI slash commands ────────────────────────────── → Note 4 (skills→SP05)
├── Quick Commands / Custom model aliases / Alias Resolution ─ → Note 4 (config→SP02)
├── Messaging slash commands ──────────────────────────────── → Note 5 (per-platform→SP11-13)
├── Notes (CLI-only / messaging-only / both surface matrix) ─ → Note 5
└── Confirmation prompts for destructive commands ─────────── → Note 5 (dangerous-cmd approval→SP03)
profile-commands.md (2358w, 31 code)
├── hermes profile (+list/use/create/describe/delete/show/alias/rename/export/import) → Note 6 (profiles concept→SP04)
├── Distribution commands (install/update/info, private, distribution.yaml, publishing) → Note 6 (profile-distributions→SP04)
├── hermes -p / hermes --profile ──────────────────────────── → Note 6
├── hermes completion (profile completions) ───────────────── → Note 6 (full completion→Note 3)
└── See also (link list) ──────────────────────────────────── → Note 6 footer (resolved as Related Notes)
```

No source H2/H3 orphaned. All 3 pages fully covered; feature-page behavior intentionally routed to owning
SPs as link-outs (reference lists the command, feature SP explains it).

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| cli-commands.md (10819w, 73 code) | Note 1 (chat/model/gateway/setup) + Note 2 (session/config/skills/tools) + Note 3 (ops/maintenance/auth) | >4000w → 3+ notes mandatory; the page's own structure (master index → per-command sections) splits cleanly by command family with no behavior duplication; each note curates ≤6 load-bearing code/usage blocks from the 73 source blocks (rest summarized as command/flag tables). |
| slash-commands.md (3598w, 4 code) | Note 4 (interactive CLI slash) + Note 5 (messaging slash) | >2500w; the page explicitly documents two surfaces (`cli.py` dispatch vs `gateway/run.py` dispatch) with a surface matrix in §Notes — natural split between the two slash-command surfaces. |
| profile-commands.md (2358w, 31 code) | Note 6 (single) | <2500w single cohesive reference catalog; 31 short usage blocks curated to ≤6 load-bearing examples, rest as subcommand/flag tables. KEEP as 1. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_cli_commands_chat_provider`, `..._session_ops`, `..._ops_maintenance_auth` | `term_command_pattern.md` (GoF design pattern); `term_ada_cli`/`term_kiro_cli`/`term_sam_cli`/`term_bones_cli` (other tools' CLIs); `cc_cli_commands.md`, `cc_commands_reference.md` (Claude Code command refs) | **NOT a dup** — term hits are unrelated concepts/other tools (LIKE false-positives, confirmed by reading); the `cc_*` notes are sibling-tool command refs (analogues), not Hermes | CREATE; do NOT link the unrelated terms; LINK the `cc_*` refs as cross-folder analogues. |
| `hermes_slash_commands_interactive_cli`, `hermes_slash_commands_messaging` | `cc_sdk_slash_commands.md` (Claude Code SDK slash commands) | **NOT a dup** — Claude Code's slash surface, a sibling-tool analogue | CREATE; LINK `cc_sdk_slash_commands` as analogue. |
| `hermes_profile_commands_reference` | `term_auth_profile` (master false-positive caution — `hermes profile` ≠ auth profile); `term_hermes_profile` (forward-ref, owned by SP04, not yet created) | **NOT a dup** — `term_auth_profile` is a different concept; `term_hermes_profile` is a forward-ref captured by SP04 | CREATE; do NOT link `term_auth_profile`; `term_hermes_profile` is a (+fin) forward-ref. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords (queried
2026-06-15); **0 substantive same-concept duplicates** (all LIKE hits are unrelated concepts / other-tool
CLIs / sibling-tool analogues, confirmed by reading). `resources/documentation/hermes_agent/` currently holds
0 notes → no intra-series doc-doc collisions (SP01/SP02 not yet executed; intra-series links resolve at
finalization). Adversarial dedup-verify pass: re-read `term_command_pattern` (design pattern) and
`term_auth_profile` headers — both confirmed different-concept, no merge.

## Per-Note Related Notes Mapping (FINALIZED — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> Standard raised 2026-06-19 (master FOUR-FLOOR directive, supersedes the prior ≥8 term/≥8 snippet/≥5 doc):
> each note's `## Related Notes` carries **four counted, relevancy-selected groups** —
> digest the Hermes SOURCE CODE; pick the modules that IMPLEMENT the command surface this note documents),
> bucket since commands map directly to `cli_*` snippets; also core/gw/cron/tools/acp — snippets are NO LONGER a
> bonus group, they are a COUNTED floor raised from the prior 8 to ≥10),
> **≥10 documentation notes** (`../../documentation/`, sibling `hermes_*` in this series + genuinely-analogous
> each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`. **All term, code-repo, and
> Forward-ref Hermes terms owned by other SPs (`term_messaging_gateway`→SP11, `term_credential_pool`→SP09,
> `term_provider_routing`/`term_fallback_provider`→SP09, `term_voice_mode`→SP08, `term_hermes_profile`→SP04)
> are ADDITIONAL `(+fin …)` forward-refs, **EXCLUDED from the ≥8 term floor** (they don't exist yet).

**Note 1 `hermes_cli_commands_chat_provider`**
- Terms (8): term_autonomous_coding_agents, term_agent_harness, term_model_catalog, term_provider_plugin, term_oauth_token, term_oauth, term_authentication, term_failover — relevance: this family launches the agent (`chat`/`-z`), selects providers/models (`model`/`fallback`/`proxy`), runs OAuth flows (`hermes model`, `setup --portal`), and authenticates via API key; `term_failover`/`term_model_failover` cover the `fallback` chain; the gateway is the harness' messaging front-end. (+fin: term_provider_routing, term_fallback_provider)
- Code-Repos (5): repo_hermes_agent_cli — implements the `hermes chat`/`model`/`gateway`/`setup`/`proxy`/`fallback` command entrypoints (`hermes_cli/`); repo_hermes_agent_providers_adapters — the provider/model registry + OAuth adapters that `hermes model`/`--provider` drive; repo_hermes_agent_agent_core — the chat loop launched by `hermes chat -q`/`-z`; repo_hermes_agent_gateway_messaging — the `hermes gateway` service this command starts/stops; repo_hermes_agent — top-level package the global `hermes [opts] <cmd>` entrypoint lives in.
- Snippets (10): cli_hermescli_chat, cli_main_cmd_chat, cli_oneshot, cli_model_switch_entry, cli_models_picker, cli_model_catalog, cli_providers_registry, cli_main_provider_flows, core_chat_helpers_activate_fallback, cli_gateway_lifecycle — relevance: the chat/one-shot launch, model-switch picker + catalog, provider registry/flow, fallback-chain activation, and gateway-lifecycle code these commands drive.
- Docs (10): hermes_cli_commands_session_ops, hermes_cli_commands_ops_maintenance_auth, hermes_slash_commands_interactive_cli, hermes_configuring_models_dashboard (sibling, +fin), cc_cli_commands, cc_commands_reference, cc_cli_flags, cc_model_selection, cc_fallback_models, cc_authentication — relevance: the sibling CLI/slash reference notes plus Claude Code's analogous command/flag refs, model-selection, fallback, and auth docs (cross-tool analogues for `model`/`fallback`/`auth`).

**Note 2 `hermes_cli_commands_session_ops`**
- Terms (8): term_session_persistence, term_skills, term_skill_manifest, term_atomic_skill, term_kanban, term_context_window, term_multi_agent_systems, term_agent_orchestration — relevance: this family manages sessions, skills/bundles/curator (`term_atomic_skill` = the bundle's unit), the multi-profile kanban board (orchestrator routing), and inspects the prompt/context budget (`prompt-size`). (+fin: term_messaging_gateway)
- Code-Repos (5): repo_hermes_agent_cli — implements `hermes sessions`/`config`/`skills`/`bundles`/`curator`/`tools`/`kanban`/`doctor`/`dump` command code; repo_hermes_agent_skills — the skills/bundles/curator install + management subsystem these commands operate; repo_hermes_agent_tools — the toolset registry `hermes tools` configures; repo_hermes_agent_agent_core — the prompt builder `hermes prompt-size` inspects + session store `hermes sessions` browses; repo_hermes_agent — the kanban board + insights store these subcommands query.
- Snippets (10): cli_hermescli_session_handlers, cli_skills_install, cli_skills_hub, core_skill_commands_discovery, cli_tools_config, cli_kanban_commands, cli_kanban_crud, cli_kanban_query, cli_doctor_primitives, cli_inventory — relevance: the session-handler, skills-install/hub + skill-command discovery, tools-config, kanban command/CRUD/query, doctor-diagnostics, and prompt-inventory code these commands drive.
- Docs (10): hermes_cli_commands_chat_provider, hermes_cli_commands_ops_maintenance_auth, hermes_session_search_storage (sibling, +fin), hermes_slash_commands_interactive_cli, cc_commands_reference, cc_cli_commands, cc_sessions, cc_manage_your_session, cc_skills_overview, cc_commands_by_workflow — relevance: the sibling reference notes plus Claude Code's command/session/skills analogues for `sessions`/`config`/`skills`.

**Note 3 `hermes_cli_commands_ops_maintenance_auth`**
- Terms (8): term_oauth_token, term_authentication, term_mcp, term_acp_agent_client_protocol, term_cron, term_webhook, term_regular_checkpointing, term_prompt_injection — relevance: this family manages credentials/secrets (`auth`/`secrets`), MCP/ACP/cron/webhook/hooks automation surfaces, backup+checkpoint ops, and the supply-chain `security audit` (prompt-injection-adjacent supply-chain risk). (+fin: term_credential_pool, term_messaging_gateway)
- Code-Repos (5): repo_hermes_agent_cli — implements `hermes auth`/`secrets`/`cron`/`mcp`/`acp`/`plugins`/`backup`/`checkpoints`/`logs`/`update` command code; repo_hermes_agent_cron — the cron scheduler `hermes cron` ticks/creates jobs against; repo_hermes_agent_mcp_toolsets — the MCP server config/serve subsystem `hermes mcp` manages; repo_hermes_agent_acp — the ACP server `hermes acp` starts for editor integration; repo_hermes_agent_plugins — the plugin install/enable/disable subsystem `hermes plugins` drives.
- Snippets (10): cli_auth_login_logout, cli_auth_storage, cli_cron, cron_tick, cli_mcp_config, mcp_serve_hermes_as_server, cli_plugins_install, cli_backup_save, cli_security_advisories, cli_main_cmd_update — relevance: the auth-storage, cron command + scheduler tick, MCP-config + serve, plugin-install, backup, security-advisory, and update code these commands drive.
- Docs (10): hermes_cli_commands_chat_provider, hermes_cli_commands_session_ops, hermes_profile_commands_reference, hermes_updating_uninstalling (sibling, +fin), cc_cli_commands, cc_commands_reference, cc_mcp_server_management, cc_checkpointing, cc_update_and_release_channels, cc_plugin_cli_commands — relevance: the sibling reference notes plus Claude Code's analogous MCP-management, checkpointing, update, and plugin-CLI docs for `mcp`/`checkpoints`/`update`/`plugins`.

**Note 4 `hermes_slash_commands_interactive_cli`**
- Terms (8): term_skills, term_skill_manifest, term_persona, term_session_persistence, term_context_window, term_progressive_summarization, term_subagent, term_human_in_the_loop — relevance: the CLI slash surface drives session/personality/skill commands, manual context compression (`/compress` = progressive summarization), goal-loop subagents (`/goal`,`/background`), and write-approval gates (`/skills approve`,`/memory approve` — human-in-the-loop). (+fin: term_voice_mode)
- Code-Repos (5): repo_hermes_agent_cli — implements the `cli.py` slash dispatch + `COMMAND_REGISTRY` (`hermes_cli/commands.py`) this surface is built on; repo_hermes_agent_skills — the installed skills exposed as dynamic `/<skill-name>` commands; repo_hermes_agent_tools — the toolsets `/tools`/`/toolsets`/`/browser` enable/disable; repo_hermes_agent_agent_core — the conversation/compression engine `/compress` + the goal loop `/goal` drive; repo_hermes_agent_tui_gateway — the TUI REPL that renders `/sessions`/`/switch` and the autocomplete menu.
- Snippets (10): cli_hermescli_process_command, cli_hermescli_callbacks, cli_hermescli_init_repl, cli_skin_apply, cli_skin_engine, tools_voice_mode, cli_tools_enable, cli_goals, core_conversation_compression_entry, cli_kanban_commands — relevance: the REPL command-dispatch/callbacks/init, skin engine/apply, voice-mode, tools-enable, goal-loop, manual-compression, and kanban-slash code these slash commands invoke.
- Docs (10): hermes_slash_commands_messaging, hermes_cli_commands_chat_provider, hermes_cli_interface (sibling, +fin), hermes_cli_commands_session_ops, cc_sdk_slash_commands, cc_interactive_mode_keyboard_shortcuts, cc_goal_command, cc_commands_reference, cc_manage_your_session, cc_voice_dictation — relevance: the sibling slash/CLI notes plus Claude Code's slash-command, interactive-mode, goal-command, session, and voice-dictation analogues for `/goal`/`/voice`/the autocomplete surface.

**Note 5 `hermes_slash_commands_messaging`**
- Terms (8): term_session_persistence, term_human_in_the_loop, term_persona, term_subagent, term_context_window, term_skills, term_prompt_injection, term_authentication — relevance: messaging slash drives session/personality/model commands, dangerous-command approval (`/approve`,`/deny` — human-in-the-loop, prompt-injection guard), background subagents (`/background`), and skill/memory write-approval review. (+fin: term_messaging_gateway, term_voice_mode)
- Code-Repos (5): repo_hermes_agent_gateway_messaging — implements the `gateway/run.py` messaging-slash dispatch, per-platform menus, and the destructive-command confirmation modal; repo_hermes_agent_cli — owns the shared `COMMAND_REGISTRY` both surfaces dispatch from + the `cli_send_cmd`; repo_hermes_agent_agent_core — the message-sanitization + background-session engine messaging slash runs through; repo_hermes_agent_tools — the `send` delivery + media tools `hermes send`/`/<media>` use; repo_hermes_agent — the gateway service + platform adapters this surface ships in.
- Snippets (10): gw_slash_access, cli_gateway_dispatch, gw_platform_discord_slash, cli_send_cmd, tools_send_dispatch, gw_delivery, gw_runner_router, gw_runner_acl, core_message_sanitization, cli_hermescli_process_command — relevance: the gateway slash-access ACL, dispatch/per-platform-slash (Discord), send command + delivery dispatch, delivery/router, runner ACL, message-sanitization, and shared command-dispatch code these messaging slash commands run through.
- Docs (10): hermes_slash_commands_interactive_cli, hermes_cli_commands_chat_provider, hermes_messaging_media_settings (sibling, +fin), hermes_cli_commands_session_ops, cc_sdk_slash_commands, cc_commands_reference, cc_claude_code_in_slack, cc_slack_setup_and_routing, cc_channel_permission_relay, cc_fast_mode — relevance: the sibling slash/CLI notes plus Claude Code's slash-command, Slack-integration, channel-permission, and fast-mode analogues for the messaging surface (`/fast`, per-platform ACL).

**Note 6 `hermes_profile_commands_reference`**
- Terms (8): term_authentication, term_oauth_token, term_session_persistence, term_skills, term_kanban, term_agent_orchestration, term_multi_agent_systems, term_skill_manifest — relevance: profiles are isolated agent instances (own config/sessions/skills/auth); distributions ship a versioned profile (skills/SOUL.md/cron) via git; the kanban orchestrator routes tasks by profile `describe` description (multi-agent orchestration). (+fin: term_hermes_profile)
- Code-Repos (5): repo_hermes_agent_cli — implements the `hermes profile`/`-p`/`completion` command code (`cli_main_cmd_profile`, `cli_profiles_switch`); repo_hermes_agent — the profile home-directory + state isolation + distribution install/update machinery; repo_hermes_agent_skills — the skills a distribution ships and `--clone`/`--no-skills` copies/omits; repo_hermes_agent_cron — the cron jobs a distribution bundles + warns about on install; repo_hermes_agent_agent_core — the per-profile config/state runtime the profile commands switch between.
- Snippets (10): cli_main_cmd_profile, cli_profiles_switch, cli_profiles_schema, cli_completion, cli_config_load, cli_config_schema, core_hermes_home, core_hermes_state, toolset_distributions, cli_skills_install — relevance: the profile command/switch/schema, completion, config-load/schema, Hermes-home + state isolation, toolset-distributions, and skills-install code the profile + distribution commands drive.
- Docs (10): hermes_cli_commands_ops_maintenance_auth, hermes_cli_commands_chat_provider, hermes_cli_commands_session_ops, hermes_slash_commands_interactive_cli, cc_cli_commands, cc_commands_reference, cc_cli_flags, cc_settings_reference, cc_sessions, cc_uninstall — relevance: the sibling reference notes plus Claude Code's command/flag/settings/session/uninstall analogues for the `-p`/`--profile` override and profile-aware config/completion surface.

All 6 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc. Term IDs are under `resources/term_dictionary/`;
code-repo IDs are under `areas/code_repos/` (the 13 `repo_hermes_agent_*` source-code notes); snippet IDs are
sibling `hermes_*` doc links resolve in `resources/documentation/hermes_agent/` (intra-series, land at
finalization, verified by G5/G8 — flagged `(sibling, +fin)`). Every `- Terms / - Code-Repos / - Snippets`
confined to the `(+fin …)` parenthetical and excluded from the ≥8 term floor.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; re-measured 2026-06-19, mirror c253b07)

Re-read all 3 source pages from `inbox/hermes_agent_docs/reference/`; measured counts match the Source Pages
table (cli-commands 10819w/73code is the largest reference page; slash 3598w/4code; profile 2358w/31code —
ratio 1.00, no >50% estimate miss). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 cli-chat-provider | navigation | 1500 | ≤6 (curate from ~25 chat/model/gateway usage blocks; flag tables in prose) | ✓ |
| 2 cli-session-ops | navigation | 1500 | ≤6 (curate from ~25 session/skills/kanban blocks) | ✓ |
| 3 cli-ops-maint-auth | navigation | 1700 | ≤6 (curate from ~23 auth/cron/backup/update blocks) | ✓ |
| 4 slash-interactive | navigation | 1300 | ≤6 (quick-commands + model-aliases YAML; command tables in prose) | ✓ |
| 5 slash-messaging | navigation | 1100 | ≤6 (surface matrix + destructive table in prose; few code blocks) | ✓ |
| 6 profile-reference | navigation | 1300 | ≤6 (curate from 31 short usage blocks; distribution.yaml manifest kept verbatim) | ✓ |

No further splits needed — all 6 notes ≤2500w. The cli-commands.md 73 source code blocks are short
command-usage snippets; each note curates ≤6 load-bearing examples (kept verbatim) and renders the rest as
scannable command/subcommand/flag tables in prose (a reference catalog's natural form). If any note exceeds
350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md` —
verified field order against `cc_cli_commands.md`/`cc_commands_reference.md`, the closest sibling agent-tool
command-reference notes): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it
IS, NOT ## Definition) → source-mirrored H2s (per command / command-group) → ## Related Notes (indexed
markdown links, each `- [Name](path.md) — what-it-is; relevance: …`; ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. `building_block: navigation`
for all 6 (command-reference catalogs). One BB/note; caps ≤2500w / ≤6 code / ≤400 lines. Forbidden YAML fields
per master (`title`, `category`, `created`, `updated`, `source`, `parent`, `author`, `related_wiki`,
`note_second_category`). Year tags quoted. No wiki/markdown links in YAML. Not invented — matches existing
`cc_cli_commands.md`.

## Undigested Terms Plan (SP20)

**SP20 owns 0 new term captures.** Per the master's corpus-wide ownership sweep, command-reference catalogs
introduce no new concept they are the home for — every command acts on a concept whose term is owned by the
command's feature sub-plan (link at finalization) or is an existing verified term. Augment re-read surfaced
**0 new** undigested terms that SP20 should own.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_messaging_gateway` | LINK only (forward-ref, +fin) | SP11 | `gateway`/`send`/messaging-slash commands reference it; concept home is SP11. |
| `term_credential_pool` | LINK only (+fin) | SP09 | `hermes auth` manages credential pools; concept home is SP09 credential-pools. |
| `term_provider_routing`, `term_fallback_provider` | LINK only (+fin) | SP09 | `model`/`fallback`/`proxy` commands; conceptually owned by SP09. |
| `term_voice_mode` | LINK only (+fin) | SP08 | `/voice` slash command; concept home is SP08 media. |
| `term_hermes_profile` | LINK only (+fin) | SP04 | `hermes profile` family operates on this; concept home is SP04 profiles. |

### Renamed (general → specific)

— (audit performed; SP20 owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP20 links; all are already scope-qualified by their owners.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_hermes_command` / CLI-command concept | none substantive (`term_command_pattern.md` is the UNRELATED GoF design pattern) | No removal — SP20 was never going to capture this; the 3 `hermes_cli_commands_*` reference notes are created instead. |
| `term_slash_command` (would-be) | none substantive | Not captured — reference covered by `hermes_slash_commands_*` doc notes; no standalone term warranted (link `cc_sdk_slash_commands` analogue). |
| `term_profile_command` (would-be) | `term_hermes_profile.md` (forward-ref, SP04) covers the *profile* concept | Not captured — `hermes_profile_commands_reference` is the command surface; concept term owned by SP04. |

## Term-Note Authoring Requirements

N/A (inherited) — SP20 owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP04/08/09/11). The full Term-Note Authoring
fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12, backlink expansion,
>200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (CLI command-reference cluster, pilot):** Notes 1, 2, 3. Pilot Note 1 first
  (`hermes_cli_commands_chat_provider`) → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (slash command-reference):** Notes 4, 5. GATE G1–G8.
- **Phase 3 (profile command-reference):** Note 6. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/reference/<page>` (code
verbatim for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4,
DB-verify every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** ·
G7 single-BB (navigation) · **G8 in-degree ≥1 from outside the folder**.

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
for n in hermes_cli_commands_chat_provider hermes_cli_commands_session_ops hermes_cli_commands_ops_maintenance_auth hermes_slash_commands_interactive_cli hermes_slash_commands_messaging hermes_profile_commands_reference; do
```

## Entry Point Decision (inherited)

Contributes 6 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Reference: Commands" section. Parent hub back-link in `entry_research_and_ai_hub.md`
is handled at master level. SP20 does NOT create a separate entry point — the >30-note corpus shares the
single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_cli.md` | → `hermes_cli_commands_chat_provider`, `hermes_cli_commands_session_ops`, `hermes_cli_commands_ops_maintenance_auth` | CLI repo ↔ CLI command reference |
| `repo_hermes_agent.md` | → `hermes_cli_commands_chat_provider`, `hermes_profile_commands_reference` | implementation ↔ command/profile reference |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_slash_commands_messaging` | gateway repo ↔ messaging slash reference |
| `repo_hermes_agent_cron.md` | → `hermes_cli_commands_ops_maintenance_auth` | cron repo ↔ `hermes cron` reference |
| `repo_hermes_agent_mcp_toolsets.md` | → `hermes_cli_commands_ops_maintenance_auth` | MCP toolsets repo ↔ `hermes mcp` reference |
| `repo_hermes_agent_acp.md` | → `hermes_cli_commands_ops_maintenance_auth` | ACP repo ↔ `hermes acp` reference |
| `repo_hermes_agent_skills.md` | → `hermes_cli_commands_session_ops`, `hermes_slash_commands_interactive_cli` | skills repo ↔ `hermes skills` / `/<skill>` reference |
| `repo_hermes_agent_plugins.md` | → `hermes_cli_commands_ops_maintenance_auth` | plugins repo ↔ `hermes plugins` reference |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_cli_commands_chat_provider` | provider adapters ↔ `model`/`fallback` reference |
| `entry_code_snippets_hermes_agent.md` | → `hermes_cli_commands_chat_provider`, `hermes_slash_commands_interactive_cli` | code layer ↔ command-reference docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 6 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_cli_commands_chat_provider`) → reindex → verify format/ghost/in-degree BEFORE authoring
the rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing
each note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code/usage-heavy notes to
≤6 load-bearing examples and render the rest as command/flag tables. If a note exceeds 350 lines during
writing, STOP and split. If multi-agent: agents return note content, master writes serially where there is
write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP20 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 6 rows to the
  master-created entry point; backfill the `repo_hermes_agent_*` / `entry_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After the messaging wave (SP11–13) lands: cross-link `hermes_slash_commands_messaging` from each platform
  doc note (per-platform slash ACL); add the `term_messaging_gateway` / `term_voice_mode` /
  `term_credential_pool` forward-refs once those SPs capture them.
- After SP04 lands: cross-link `hermes_profile_commands_reference` ↔ the SP04 profiles/distributions feature
  notes (command surface ↔ behavior) and add the `term_hermes_profile` forward-ref.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (LIKE false-positives confirmed by reading — design-pattern
  term, other-tool CLIs, sibling-tool `cc_*` analogues), finalized Per-Note Mapping (≥8 term + ≥5 code-repo +
  Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  counted ≥10 floor, added a ≥5 code-repo floor drawn from the 13 `repo_hermes_agent_*` source-code notes (the cli
  repo + the feature repos each command family implements), and raised the doc floor from 5 to ≥10 (sibling
- Density re-read: counts match measured; **no additional splits** beyond the planned 5 (cli→3, slash→2,
  profile→1). All 6 notes ≤2500w; reference catalogs curated to ≤6 code blocks each.
- Collision audit: **0 removals** — all LIKE hits are unrelated concepts / other-tool CLIs / sibling-tool
  analogues; no doc note duplicates an existing term/doc note.
- Term placeholder catch: cited IDs re-grepped against the DB — **0 failing verification**; no
  `CORRECTED:`/`PLACEHOLDER`/dual-list cruft on any Terms/Snippets line.
- Undigested terms surfaced at augment: **0 new** (SP20 owns 0 captures; command concepts owned by feature SPs).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (≥8 term /
G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (N/A — 0 owned;
audit noted) ✓ Slug Collision (LIKE false-positives caught; 0 dups) ✓ dedup generalized to ALL notes incl doc,
searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec
derived ✓). Term-capture items are N/A-pass (SP20 owns 0 captures); dedup/collision items are substantively
PASS (audit performed on all 6 doc notes).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass). Independently RE-REVIEWED 2026-06-19
against the FOUR-FLOOR standard (≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note) — 9/9 pass, READY.**

Re-review 2026-06-19 (FOUR-FLOOR): CP1 — all 6 notes carry exactly 8 counted terms (forward `(+fin …)` refs
excluded), 5 code-repos, 10 snippets, and 10 docs (6 `cc_*` + 4 sibling `hermes_*`); every group line carries
per-item relevance clauses (Terms/Snippets/Docs via a shared `relevance:`; Code-Repos via per-repo `id — why`).
Anti-fabrication spot-check FAR exceeded the ≥8 minimum: ALL 26 cited terms, 12 code-repos, 57 unique snippets,
fresh mirror: cli-commands 10819w/73code, slash-commands 3598w/4code, profile-commands 2358w/31code — exact
match to the plan. CP8f dedup false-positives (`term_command_pattern` GoF, `term_auth_profile`) confirmed active
and correctly excluded; no `resources/documentation/hermes_agent/` notes exist yet (no intra-series dup). CP9
fixes required — the plan already carries four-floor wording throughout (mapping preamble, Authoring Spec,
Augmentation Report, 31-item checklist, CP1 evidence below).

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (6 rows under a Reference: Commands section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 6 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_cli_commands.md`/`cc_commands_reference.md` (sibling command refs); not invented. |
| CP6 | Borderline density → split | PASS | cli-commands→3, slash→2, profile→1; all notes ≤2500w; reference catalogs curated ≤6 code blocks; single-BB navigation, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15; re-measured 2026-06-19 (mirror c253b07): cli-commands 10819 (largest reference page), slash-commands 3598, profile-commands 2358 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP20 owns 0 term captures (command concepts owned by SP04/08/09/11); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 6 doc notes (term_dictionary AND documentation/); LIKE false-positives confirmed (GoF design pattern / other-tool CLIs / sibling-tool `cc_*` analogues = LINK or skip, not dup); Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 6 notes from repo_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION (re-confirmed 2026-06-19, FOUR-FLOOR).**

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from NousResearch/hermes-agent `website/docs/` at main HEAD `c253b07` (was pinned
`95715dc`); byte-identical to upstream main. SP20 is in the **COUNTS** class — one owned page grew, no page
added/removed, no section structure changed. Independently re-measured each owned page against the fresh mirror
(BODY-only word count after stripping YAML frontmatter; code-block count = `^\s*``` ` lines ÷ 2):

- reference/cli-commands.md — 10745w/73code -> 10819w/73code (+74w, code unchanged; my measurement matches the manifest)

Unchanged pages spot-re-measured and confirmed stable: slash-commands.md 3598w/4code ✓, profile-commands.md
2358w/31code ✓.

**Density re-decision: none.** The +74w delta on cli-commands.md is immaterial — at 10819w the page still
vastly exceeds the 2500w cap (as it did at 10745w), so the existing **3-way split** (Note 1 chat/provider +
Note 2 session/ops + Note 3 ops/maintenance/auth) stands with no change to per-note ~Word estimates
(~1500/~1500/~1700, each well under cap). slash→2 and profile→1 unaffected. **No split added; no split removed.**

Cross-ref floor subsequently raised 2026-06-19 to the FOUR-FLOOR standard (≥8 term + ≥5 code-repo + ≥10 snippet
+ ≥10 doc per note — see Per-Note Related Notes Mapping). No planned-note filename, BB type, or gate altered.
Plan remains **READY FOR EXECUTION**.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 to FOUR-FLOOR) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed 2026-06-19, 9/9 READY against FOUR-FLOOR) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/reference/{cli-commands,slash-commands,profile-commands}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
</content>
</invoke>
