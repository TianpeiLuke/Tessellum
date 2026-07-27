---
title: Hermes Agent Docs Digestion — Sub-Plan 01 — Getting Started & Install
date: 2026-06-14
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/
pages:
  - index.mdx
  - getting-started/quickstart.md
  - getting-started/installation.md
  - getting-started/learning-path.md
  - getting-started/updating.md
  - getting-started/termux.md
  - getting-started/nix-setup.md
  - user-stories.mdx
---

# Sub-Plan 01: Getting Started & Install

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED 2026-06-14. Inherits shared Routing,
> Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP01's note
> filenames/BBs/coverage are defined.

## Scope

The entry/onboarding surface of the Hermes Agent docs: install across all platforms (one-line,
Desktop, Termux/Android, Nix/NixOS), the first-chat quickstart, the learning-path router, and
updating/uninstalling. Source = 8 mirrored pages in `inbox/hermes_agent_docs/` (7 substantive + 1
stub). **P1 / foundational** — downstream sub-plans link back to `hermes_quickstart_*` and the
existing `term_hermes_agent`.

## Content Strategy

- **One BB per note.** quickstart and nix-setup mix BBs + exceed density caps → split (see Split Decisions).
- **Do NOT duplicate**: the provider catalog (SP14 `providers`), per-feature teasers (SP05/06/08/09),
  messaging setup (SP11-13) → **link-outs**, not copied content.
- **Collision (augment): the "what is Hermes Agent" concept is already owned by the substantive
  `term_hermes_agent.md` (85 lines, active).** The planned `hermes_overview.md` was DROPPED; `index.mdx`'s
  conceptual content is covered by enriching/linking `term_hermes_agent` + the navigation entry point.
  `index.mdx` install snippets → installation note; quick-links → learning-path note + entry point.
- `user-stories.mdx` is a 6-word stub/redirect → **NOT digested** (recorded in coverage map).

## Source Pages (Measured 2026-06-14, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| index.mdx | 894 | 2 | concept | 0 (→ link/enrich `term_hermes_agent` + entry point) |
| getting-started/quickstart.md | 2576 | 19 | procedure | 2 (split) |
| getting-started/installation.md | 1049 | 10 | procedure | 1 |
| getting-started/learning-path.md | 955 | 0 | navigation | 1 |
| getting-started/updating.md | 1708 | 21 | procedure | 1 |
| getting-started/termux.md | 923 | 19 | procedure | 1 |
| getting-started/nix-setup.md | 5482 | 44 | MIXED concept+procedure | 3 (split) |
| user-stories.mdx | 6 | 0 | — (stub) | 0 (skip) |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_quickstart_first_chat.md` | procedure | quickstart §The fastest path, §1 Install, §2 Choose a Provider, §3 First Chat, §4 Verify Sessions, §Quick Reference | ~1200 | Zero-to-working-chat: install, choose provider (incl. `setup --portal`), run first chat (CLI vs TUI), verify resume; 64K-context rule; secrets-vs-config storage. |
| 2 | `hermes_quickstart_next_layer.md` | procedure | quickstart §5 Try Key Features, §6 Add the Next Layer, §Common Failure Modes, §Recovery Toolkit | ~1100 | After base chat: terminal/slash/multiline/interrupt; layering gateway, sandboxed terminal, voice, skills, MCP, ACP (link-outs); failure-mode table + recovery toolkit. |
| 3 | `hermes_installation.md` | procedure | installation.md (Quick Install, Install Layout/FHS, Prerequisites, Non-Sudo/Service-User, Troubleshooting, auto-detection) | ~1050 | Full install reference: one-line/Desktop install, per-user vs root FHS layout, auto-handled prerequisites, unprivileged/service-user installs, install-method auto-detection. |
| 4 | `hermes_learning_path.md` | navigation | learning-path.md (By Experience Level, By Use Case, Key Features at a Glance) | ~900 | Reader router: reading order by experience tier and use case (CLI assistant, bot, automation, custom tools, RL, Python library) + feature directory. |
| 5 | `hermes_updating_uninstalling.md` | procedure | updating.md (Updating git/pip, update internals, --branch/--check/--backup, Windows lock, post-update validation, rollback, Nix note, Uninstalling) | ~1700 | Update + uninstall: `hermes update` internals (auto-rollback, gateway restart), flags, SIGHUP survival, rollback, platform `/update`, uninstall per install type. |
| 6 | `hermes_install_termux_android.md` | procedure | termux.md (supported/unsupported, one-line + manual install, follow-up, troubleshooting, limitations) | ~900 | Android/Termux install: tested `.[termux]` bundle vs unsupported extras (voice/Docker/browser), manual steps, `ANDROID_API_LEVEL`, troubleshooting, phone limits. |
| 7 | `hermes_install_nix_quickstart.md` | procedure | nix-setup §Quick Start, §Prerequisites, messaging/full variants, non-NixOS workflow | ~900 | Non-NixOS Nix install: `nix run`/`nix profile install`, `#messaging`/`#full` variants, why on-demand messaging libs need a variant, post-install workflow. |
| 8 | `hermes_install_nixos_module.md` | procedure | nix-setup §NixOS Module, Declarative Settings, Secrets (sops-nix/agenix), OAuth seeding, MCP Servers, Plugins | ~1400 | NixOS declarative deploy: flake input + module, declarative config (CLI config blocked), secrets via sops-nix/agenix, MCP-server transports, plugins. |
| 9 | `hermes_nixos_container_mode.md` | model | nix-setup §Managed/Container Architecture, What Persists, GC Root Protection, Options Reference, Updating, Troubleshooting | ~1300 | NixOS container deployment model: persistent Ubuntu container for self-modifying agents, persistence/GC-root semantics, native vs container layout, options ref. |

**SP01 totals:** 9 notes · procedure 6 · navigation 1 · model 1 (+0 concept — the concept is `term_hermes_agent`).
7 source pages digested, 1 skipped, index.mdx routed to link/enrich.

## Summary Statistics & Building Block Distribution

- Notes: 9 · procedure 6 · navigation 1 · model 1 · concept 0 (owned by existing `term_hermes_agent`).
- Source: 7 digested pages (~13.6K words) → ~10.5K words of notes (compression via link-outs).

## Section Coverage Map

```
index.mdx (894w)
├── # Hermes Agent / What is Hermes Agent? / Key Features ── → LINK/ENRICH term_hermes_agent (existing concept)
├── ## Install (snippets) ───────────────────────────────── → LINK-OUT to Note 3 (installation)
└── ## Quick Links / For LLMs (llms.txt) ────────────────── → Note 4 (router) + entry_hermes_agent_docs
quickstart.md (2576w)
├── Who this is for / The fastest path / 1 Install / 2 Provider (+table) / settings / 3 First Chat / 4 Verify / Quick Ref → Note 1 (table=LINK-OUT to SP14)
├── 5 Try Key Features / 6 Add the Next Layer ───────────── → Note 2 (LINK-OUTs SP05/08/09/11)
└── Common Failure Modes / Recovery Toolkit ─────────────── → Note 2
installation.md (1049w) ── all sections ──────────────────── → Note 3 (nix tip→Note 7/8; manual→SP19 contributing)
learning-path.md (955w) ── all sections ──────────────────── → Note 4 (indexed link-outs across SPs)
updating.md (1708w) ────── all sections ──────────────────── → Note 5 (checkpoints→SP03; nix→Note 8)
termux.md (923w) ───────── all sections ──────────────────── → Note 6
nix-setup.md (5482w)
├── intro 3-levels / Prerequisites / Quick Start ────────── → Note 7
├── NixOS Module / Declarative / Secrets / OAuth / MCP / Plugins / Dev shell → Note 8
└── Managed/Container Architecture / Persists / GC / Options Ref / Updating / Troubleshooting → Note 9
user-stories.mdx (6w) ──── stub redirect ─────────────────── → SKIP (recorded; not a note)
```

No source H2/H3 orphaned. index.mdx's concept content intentionally routed to the existing term note.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| quickstart.md (2576w, 19 code) | Note 1 (first-chat) + Note 2 (next-layer+failure modes) | >2500w; two distinct procedural arcs. |
| nix-setup.md (5482w, 44 code, MIXED) | Note 7 (nix quickstart, proc) + Note 8 (NixOS module, proc) + Note 9 (container mode, model) | >4000w → 3 notes; separates non-NixOS install / declarative module / container architecture (BB atomicity). |

## Collision & Dedup Audit (Step 10.5f — generalized to doc notes)

| Planned note | Verdict | Action |
|---|---|---|
| `hermes_overview.md` | **DUP** of substantive `term_hermes_agent.md` (85L, active) | **REMOVED.** Link/enrich `term_hermes_agent`; concept owned there. |
| `hermes_quickstart_*`, `hermes_installation`, `hermes_updating_uninstalling`, `hermes_install_termux_android`, `hermes_install_nix*`, `hermes_nixos_container_mode`, `hermes_learning_path` | NEW (no term/doc note covers these procedures) | Create. |

DB synonym scan run across `term_dictionary/` for each planned slug's keywords; only `hermes_overview`
collided. New `hermes_agent/` folder → no doc-doc collisions.

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19** (user directive — supersedes the earlier 2026-06-19 three-floor
> wording of ≥8 term + ≥5 code-repo + ≥10 doc with snippets as a bonus, and the original 2026-06-14 master
> floor of ≥8 term + ≥8 snippet + ≥5 doc). Each note's `## Related Notes` now carries FOUR COUNTED groups,
> all relevancy-selected and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
> - **≥8 TERM notes** (`../../term_dictionary/term_*.md`, DB-verified active ✓),
> - **≥5 CODE-REPO notes** (`../../../areas/code_repos/repo_*.md`, DB-verified active ✓) — primarily the 13
>   `repo_hermes_agent_*` notes that digest the Hermes SOURCE CODE; pick the modules that IMPLEMENT what this
>   doc note describes,
> - **≥10 SNIPPET notes** (`../../code_snippets/snippet_hermes_agent_*.md`, DB-verified active ✓) — the
>   517-note Hermes implementation corpus; pick by the page's content — the actual code paths it documents.
>   This is now a COUNTED floor, promoted from the prior "bonus" group and raised from ≥8 to ≥10,
> - **≥10 DOCUMENTATION notes** (`../../documentation/`) — sibling `hermes_*` in this series (resolve at
>   finalization per G5/G8) + analogous `claude_code/cc_*` agent-tool docs (DB-verified active ✓) + other
>   relevant existing doc notes.
>
> The four COUNTED floors are term(8) / code-repo(5) / snippet(10) / doc(10). Relevancy first, never pad. Every
> `term_*` ID, every `repo_*` ID, and every `snippet_hermes_agent_*` ID below is DB-verified active (sqlite
> checks run 2026-06-19). Existing `cc_*` doc IDs are DB-verified active. Sibling `hermes_*` doc IDs (this
> series) are allowed un-verified — they land at finalization. New Hermes-specific terms owned by other SPs
> are ADDITIONAL (+fin), not counted.

**Note 1 `hermes_quickstart_first_chat`** (procedure — install→provider→first chat→resume)
- Terms (8): [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the agent this page onboards; relevance: page's whole purpose is a first working chat. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: §The fastest path frames Hermes as autonomous, not a copilot. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: `hermes setup --portal`/Codex/Anthropic OAuth login covered in §2. [term_context_window](../../term_dictionary/term_context_window.md) — model context size; relevance: the 64K-token minimum-context caution. [term_model_catalog](../../term_dictionary/term_model_catalog.md) — provider/model list; relevance: §2 provider table + `hermes model` picker. [term_llm](../../term_dictionary/term_llm.md) — underlying model; relevance: every provider row selects an LLM. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — saved sessions; relevance: §4 `hermes --continue` resume verification. [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapter; relevance: each catalog row is a provider plugin. (+fin: term_nous_portal, term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI entrypoints; relevance: implements `hermes`, `hermes setup`, `hermes model`, `--tui`, `--continue` invoked throughout. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters + OAuth; relevance: backs the §2 provider catalog and `setup --portal` login. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — conversation loop + session store; relevance: runs the §3 first chat and §4 resume. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — TUI front-end; relevance: implements `hermes --tui` offered in §3. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level repo; relevance: the installed package this quickstart drives end-to-end.
- Docs (10): [hermes_installation](hermes_installation.md) — full install ref; relevance: §1 link-out. [hermes_quickstart_next_layer](hermes_quickstart_next_layer.md) — sibling part 2; relevance: continues after first chat. [hermes_learning_path](hermes_learning_path.md) — reader router; relevance: next-steps. [hermes_configuration](hermes_configuration.md) (SP02) — config/secrets split; relevance: §How settings are stored. [hermes_cli_interface](hermes_cli_interface.md) (SP02) — CLI/TUI guide; relevance: §3 interface choice. [hermes_providers](hermes_providers.md) (SP14) — full provider catalog; relevance: §2 table link-out. [cc_quickstart](../claude_code/cc_quickstart.md) — analogous agent-tool quickstart; relevance: same zero-to-working-chat arc. [cc_install](../claude_code/cc_install.md) — analogous install; relevance: parallel one-line install step. [cc_model_selection](../claude_code/cc_model_selection.md) — analogous model picker; relevance: maps to `hermes model`. [cc_authentication](../claude_code/cc_authentication.md) — analogous auth/OAuth; relevance: maps to `setup --portal` login.
- Snippets (10): [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — `hermes setup` wizard; relevance: §1/§2 the wizard `setup --portal` invokes. [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: §1 one-line install. [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — OAuth login; relevance: §2 portal/Codex/Anthropic OAuth login. [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — `hermes model` entry; relevance: §2 provider picker. [snippet_hermes_agent_cli_models_picker](../../code_snippets/snippet_hermes_agent_cli_models_picker.md) — interactive model list; relevance: §2 model selection UI. [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: backs the §2 provider catalog rows. [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `hermes config set`; relevance: §How settings are stored (right file routing). [snippet_hermes_agent_cli_hermescli_session_handlers](../../code_snippets/snippet_hermes_agent_cli_hermescli_session_handlers.md) — session handlers; relevance: §4 `--continue` resume. [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — session persistence; relevance: §4 saved-session verification. [snippet_hermes_agent_cli_main_cmd_chat](../../code_snippets/snippet_hermes_agent_cli_main_cmd_chat.md) — `hermes` chat command; relevance: §3 first chat (`hermes`/`--tui`).

**Note 2 `hermes_quickstart_next_layer`** (procedure — features + failure modes + recovery)
- Terms (8): [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: §MCP servers config block. [term_cron](../../term_dictionary/term_cron.md) — scheduled tasks; relevance: §Automation lists cron. [term_subagent](../../term_dictionary/term_subagent.md) — spawned sub-agents; relevance: delegation feature in this layer. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal isolation backend; relevance: §Sandboxed terminal (`terminal.backend docker/ssh`). [term_voice_wake](../../term_dictionary/term_voice_wake.md) — voice activation; relevance: §Voice mode (`/voice on`, Ctrl+B). [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — `SKILL.md` spec; relevance: §Skills describes SKILL.md docs. [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — parallel agents; relevance: layering delegation/parallelism. [term_skills](../../term_dictionary/term_skills.md) — installable skill packages; relevance: §Skills browse/install/use. (+fin: term_acp, term_voice_mode, term_skills_hub, term_messaging_gateway)
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — toolset config; relevance: `hermes tools` per-platform tuning. [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills system; relevance: `hermes skills browse/search/install` + slash-command skills. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP client/toolsets; relevance: §MCP servers `config.yaml` block. [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — ACP editor integration; relevance: §Editor integration (`hermes acp`). [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway + platforms; relevance: §Bot/shared assistant (`hermes gateway setup/status`, recovery toolkit).
- Docs (10): [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — sibling part 1; relevance: prerequisite base chat. [hermes_skills](hermes_skills.md) (SP05) — skills deep-dive; relevance: §Skills link-out. [hermes_mcp](hermes_mcp.md) (SP09) — MCP feature; relevance: §MCP servers link-out. [hermes_voice_mode](hermes_voice_mode.md) (SP08) — voice feature; relevance: §Voice mode link-out. [hermes_messaging_overview](hermes_messaging_overview.md) (SP11) — gateway setup; relevance: §Bot/assistant link-out. [hermes_acp](hermes_acp.md) (SP06) — ACP feature; relevance: §Editor integration link-out. [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — analogous MCP setup; relevance: parallels §MCP servers. [cc_skills_overview](../claude_code/cc_skills_overview.md) — analogous skills; relevance: parallels §Skills. [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — analogous delegation; relevance: parallels subagent spawning. [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — analogous scheduling; relevance: parallels the cron layering note.
- Snippets (10): [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — `hermes tools`; relevance: §Automation per-platform tool tuning. [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — `hermes skills install`; relevance: §Skills browse/search/install. [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config; relevance: §MCP servers `config.yaml` block. [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — `hermes acp` entry; relevance: §Editor integration (ACP). [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — serve-as-MCP; relevance: MCP surface the §MCP-servers layer rides on. [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron CRUD; relevance: §Automation "Cron — only after stable". [snippet_hermes_agent_cli_plugins_install](../../code_snippets/snippet_hermes_agent_cli_plugins_install.md) — plugin install; relevance: extending the feature layer with plugins. [snippet_hermes_agent_acp_server_prompt](../../code_snippets/snippet_hermes_agent_acp_server_prompt.md) — ACP server prompt; relevance: ACP editor session backing §Editor integration. [snippet_hermes_agent_cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — `/voice on` command; relevance: §Voice mode (record via Ctrl+B). [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — `hermes gateway` dispatch; relevance: §Bot/shared assistant (`gateway setup/status`) + recovery toolkit.

**Note 3 `hermes_installation`** (procedure — full install reference)
- Terms (8): [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the package being installed; relevance: page's subject. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing of what you install. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal/Playwright backend; relevance: §Non-Sudo install handles Chromium/Playwright deps. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: §Nous Portal `setup --portal` login. [term_docker](../../term_dictionary/term_docker.md) — container runtime; relevance: install enables Docker terminal backend. [term_llm](../../term_dictionary/term_llm.md) — model the installer configures; relevance: "by the end you're ready to chat" sets up a provider. [term_model_catalog](../../term_dictionary/term_model_catalog.md) — provider list; relevance: §After Installation `hermes model`. [term_authentication](../../term_dictionary/term_authentication.md) — provider auth; relevance: §Troubleshooting `API key not set`. (+fin: term_nous_portal, term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI + `hermes doctor`/`config`; relevance: implements `hermes`, `doctor`, `config check/migrate`, `desktop`, `setup --portal`. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level repo + installer; relevance: `install.sh`/`install.ps1`, FHS layout, install-method auto-detection. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — bootstrap/startup imports; relevance: the critical files compiled at startup the installer prepares. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider config; relevance: post-install `hermes model` provider setup. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway service; relevance: service-user install + `hermes gateway setup`.
- Docs (10): [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: what to do after install. [hermes_install_termux_android](hermes_install_termux_android.md) — Android path; relevance: alternative install platform. [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — Nix path; relevance: §Nix users tip link-out. [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — update/uninstall; relevance: lifecycle continuation. [hermes_learning_path](hermes_learning_path.md) — router; relevance: where to go next. [hermes_configuration](hermes_configuration.md) (SP02) — config; relevance: §After Installation config commands. [cc_install](../claude_code/cc_install.md) — analogous install; relevance: same per-OS install flow. [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — analogous advanced install + verify; relevance: parallels FHS layout + `hermes doctor`. [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — analogous diagnostics; relevance: parallels §Troubleshooting/`doctor`. [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — analogous failure reference; relevance: parallels the troubleshooting table.
- Snippets (10): [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — `install.sh`; relevance: §Quick Install one-line installer. [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: §Quick Install/Desktop install. [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verify; relevance: §After Installation readiness check. [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — `hermes doctor` checks; relevance: §Troubleshooting diagnostics. [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — doctor auth/dir checks; relevance: §Troubleshooting `API key not set` + FHS dirs. [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migration; relevance: install-method auto-detection / config layout migration. [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall; relevance: lifecycle counterpart of install. [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — startup bootstrap; relevance: the critical files compiled at startup the installer prepares. [snippet_hermes_agent_cli_doctor_entry_early_checks](../../code_snippets/snippet_hermes_agent_cli_doctor_entry_early_checks.md) — doctor early checks; relevance: §Troubleshooting prerequisite auto-detection. [snippet_hermes_agent_core_hermes_home](../../code_snippets/snippet_hermes_agent_core_hermes_home.md) — `~/.hermes` home resolution; relevance: §Install Layout/FHS per-user vs root layout.

**Note 4 `hermes_learning_path`** (navigation — reader router)
- Terms (8): [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the documented agent; relevance: every track routes into Hermes docs. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — "CLI coding assistant" track; relevance: indexes that use case. [term_subagent](../../term_dictionary/term_subagent.md) — delegation; relevance: §automate-tasks Delegation track. [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — SKILL.md; relevance: §build custom tools/skills track. [term_cron](../../term_dictionary/term_cron.md) — scheduling; relevance: §automate-tasks Cron track. [term_mcp](../../term_dictionary/term_mcp.md) — MCP; relevance: §custom tools MCP track. [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — delegation/parallelism; relevance: advanced/automation tiers. [term_rl](../../term_dictionary/term_rl.md) — reinforcement learning; relevance: §"I want to train models" (Atropos) track. (+fin: term_agentic_ai already verified below)
- Code-Repos (5): [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level repo; relevance: the codebase the Advanced/Contributing track points at. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI; relevance: Beginner CLI-usage track. [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills; relevance: Intermediate/Advanced skills track. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools; relevance: Tools track + Adding Tools. [repo_hermes_agent_trajectory_research](../../../areas/code_repos/repo_hermes_agent_trajectory_research.md) — RL/trajectory; relevance: "train models" / Atropos track.
- Docs (10): [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — quickstart; relevance: §Start Here + Beginner step 2. [hermes_installation](hermes_installation.md) — install; relevance: §Start Here + every track step 1. [hermes_cli_interface](hermes_cli_interface.md) (SP02) — CLI; relevance: Beginner CLI-usage step. [hermes_skills](hermes_skills.md) (SP05) — skills; relevance: Intermediate/Advanced skills step. [hermes_mcp](hermes_mcp.md) (SP09) — MCP; relevance: custom-tools track step. [hermes_architecture](hermes_architecture.md) (SP18) — architecture; relevance: Advanced track entry. [cc_feature_selection_guide](../claude_code/cc_feature_selection_guide.md) — analogous router; relevance: same "find the right doc" purpose. [cc_commands_by_workflow](../claude_code/cc_commands_by_workflow.md) — analogous workflow index; relevance: parallels By-Use-Case tables. [cc_overview](../claude_code/cc_overview.md) — analogous overview; relevance: parallels Key-Features-at-a-glance. [cc_quickstart](../claude_code/cc_quickstart.md) — analogous quickstart; relevance: the "just finished installing → quickstart" hand-off.
- Snippets (10): [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard; relevance: §Start Here "run setup" entry. [snippet_hermes_agent_cli_models_picker](../../code_snippets/snippet_hermes_agent_cli_models_picker.md) — model picker; relevance: Beginner CLI-usage track. [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skills install; relevance: Intermediate/Advanced skills track. [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tools config; relevance: Tools track + Adding Tools. [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — ACP entry; relevance: custom-tools/editor track. [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron CRUD; relevance: §automate-tasks Cron track. [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — serve-as-MCP; relevance: custom-tools MCP track. [snippet_hermes_agent_tui_entry](../../code_snippets/snippet_hermes_agent_tui_entry.md) — TUI entry; relevance: Beginner CLI/TUI track. [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — subagent spawn; relevance: §automate-tasks Delegation track. [snippet_hermes_agent_trajectory_schema](../../code_snippets/snippet_hermes_agent_trajectory_schema.md) — RL trajectory schema; relevance: §"I want to train models" (Atropos) track.

**Note 5 `hermes_updating_uninstalling`** (procedure — update internals + uninstall)
- Terms (8): [term_regular_checkpointing](../../term_dictionary/term_regular_checkpointing.md) — pre-update snapshot; relevance: §pairing-data snapshot + `--backup`. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — preserved sessions; relevance: backup covers sessions, uninstall keeps `~/.hermes/`. [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — package being updated; relevance: `hermes update` subject. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing of the updated tool. [term_cron](../../term_dictionary/term_cron.md) — scheduled checks; relevance: §`--check` in scripts/cron jobs. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — preserved auth; relevance: `--backup` covers auth tokens. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — gateway service; relevance: §Gateway auto-restart (systemd/launchd). [term_checkpoint](../../term_dictionary/term_checkpoint.md) — rollback point; relevance: §auto-rollback `git reset --hard <pre-pull-sha>` + §Rollback. (+fin: term_shadow_git_checkpoint, term_hermes_profile)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — update/uninstall commands; relevance: implements `hermes update` (flags `--check`/`--branch`/`--backup`/`--force`), `config migrate`, `hermes uninstall`. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — git/pip install + installer; relevance: git-pull/auto-rollback, install-method auto-detection, PyPI tagged releases. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — startup-critical files; relevance: §post-pull syntax validation compiles the eight startup imports. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway restart + `/update`; relevance: §Gateway auto-restart and §Updating from Messaging Platforms. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — scheduled update checks; relevance: `hermes update --check` gating in cron jobs.
- Docs (10): [hermes_installation](hermes_installation.md) — install ref; relevance: install-method auto-detection drives the update command. [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — Nix install; relevance: §Note for Nix users (`nix flake update`/`profile upgrade`/`rollback`). [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: post-update plain-chat re-validation. [hermes_nixos_container_mode](hermes_nixos_container_mode.md) — container update; relevance: cross-ref for NixOS container update path. [hermes_install_nixos_module](hermes_install_nixos_module.md) — NixOS module; relevance: declarative update vs CLI update. [hermes_checkpoints](hermes_checkpoints.md) (SP03) — checkpoints/rollback; relevance: §Snapshots and rollback link-out. [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — analogous update; relevance: parallels git vs tagged-release update. [cc_uninstall](../claude_code/cc_uninstall.md) — analogous uninstall; relevance: parallels §Uninstalling per install type. [cc_checkpointing](../claude_code/cc_checkpointing.md) — analogous rollback; relevance: parallels auto-rollback/snapshot. [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — analogous post-install verify; relevance: parallels §Recommended Post-Update Validation (`doctor`/`--version`).
- Snippets (10): [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — `hermes update` command; relevance: the update internals (git-pull, auto-rollback). [snippet_hermes_agent_cli_banner_update](../../code_snippets/snippet_hermes_agent_cli_banner_update.md) — startup update banner; relevance: §`--check` available-update detection. [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migrate; relevance: post-update `config migrate`. [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validate; relevance: §Post-Update Validation. [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall; relevance: §Uninstalling per install type. [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — `hermes doctor`; relevance: §Post-Update Validation `doctor`. [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verify; relevance: post-update plain-chat re-validation. [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup; relevance: update/rollback diagnostics output. [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — `--backup` snapshot; relevance: §pre-update pairing-data snapshot. [snippet_hermes_agent_cli_backup_restore](../../code_snippets/snippet_hermes_agent_cli_backup_restore.md) — backup restore; relevance: §Rollback / auto-rollback restore.

**Note 6 `hermes_install_termux_android`** (procedure — Android/Termux install)
- Terms (8): [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — package installed on phone; relevance: page's subject. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — phone-native CLI agent; relevance: framing of the Android use case. [term_mcp](../../term_dictionary/term_mcp.md) — MCP; relevance: §supported — MCP works in `.[termux]`. [term_cron](../../term_dictionary/term_cron.md) — cron; relevance: §supported — cron in the tested bundle. [term_voice_wake](../../term_dictionary/term_voice_wake.md) — voice; relevance: §unsupported — voice blocked by ctranslate2 (no Android wheels). [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — Honcho memory; relevance: §supported — Honcho memory in `.[termux]`. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal backend; relevance: §limitations — Docker backend unavailable on phones. [term_python](../../term_dictionary/term_python.md) — runtime + venv; relevance: manual path builds a `python -m venv` + `pip install -e '.[termux]'`. (+fin: term_acp, term_honcho)
- Code-Repos (5): [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — installer + extras; relevance: Termux-aware `install.sh`, `.[termux]`/`.[termux-all]` extras, `pkg`/`pyproject` paths. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI + doctor; relevance: `hermes version`, `hermes doctor`, `hermes setup` post-install. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP support; relevance: MCP is in the tested Termux path. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — cron support; relevance: cron is a supported Termux extra. [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — ACP support; relevance: ACP listed as supported in the tested bundle.
- Docs (10): [hermes_installation](hermes_installation.md) — main install; relevance: Termux is the Android variant of it. [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: post-install `hermes model`/chat. [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — Nix install; relevance: sibling alternative-platform install. [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — update; relevance: keeping the phone install current. [hermes_mcp](hermes_mcp.md) (SP09) — MCP; relevance: the supported Termux MCP extra. [hermes_honcho](hermes_honcho.md) (SP05) — Honcho memory; relevance: the supported Termux memory extra. [cc_install](../claude_code/cc_install.md) — analogous install; relevance: parallel per-platform install flow. [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — analogous failure ref; relevance: parallels §Troubleshooting (`No solution found`, build failures). [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — analogous diagnostics; relevance: parallels `hermes doctor` verify. [cc_execution_environments](../claude_code/cc_execution_environments.md) — analogous constrained runtime; relevance: parallels the narrower phone-native capability set.
- Snippets (10): [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — Termux-aware `install.sh`; relevance: one-line install path on Android. [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer + extras; relevance: `.[termux]`/`.[termux-all]` extras selection. [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — startup bootstrap; relevance: phone-native venv startup. [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — `hermes doctor`; relevance: §Troubleshooting verify. [snippet_hermes_agent_cli_memory_setup](../../code_snippets/snippet_hermes_agent_cli_memory_setup.md) — memory setup; relevance: §supported Honcho memory in the tested bundle. [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — ACP entry; relevance: §supported — ACP works in `.[termux]`. [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — cron helpers; relevance: §supported — cron in the tested extra. [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — MCP surface; relevance: §supported — MCP works on Termux. [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy optional deps; relevance: §unsupported — voice/Docker deps skipped (no Android wheels). [snippet_hermes_agent_honcho_session_lifecycle](../../code_snippets/snippet_hermes_agent_honcho_session_lifecycle.md) — Honcho sessions; relevance: §supported Honcho memory extra runtime.

**Note 7 `hermes_install_nix_quickstart`** (procedure — non-NixOS Nix install)
- Terms (8): [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — package installed via Nix; relevance: page's subject. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth login; relevance: post-install `hermes setup` works identically. [term_mcp](../../term_dictionary/term_mcp.md) — MCP; relevance: standard MCP workflow available after `nix profile install`. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal backend; relevance: messaging libs moved to on-demand, hence `#messaging`/`#full` variants. [term_llm](../../term_dictionary/term_llm.md) — model; relevance: §Prerequisites need an OpenRouter/Anthropic key. [term_model_catalog](../../term_dictionary/term_model_catalog.md) — provider list; relevance: `hermes setup` provider selection post-install. [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapters; relevance: provider selection identical to standard install. (+fin: term_nous_portal, term_messaging_gateway)
- Code-Repos (5): [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — flake + packaging; relevance: the Nix flake, `nix run`/`profile install`, `#messaging`/`#full` variants are part of the repo. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI; relevance: post-install workflow (`hermes setup`/`gateway install`) is identical CLI code. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — providers; relevance: `hermes setup` provider config works identically post-install. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — messaging adapters; relevance: why messaging libs need the `#messaging` variant in Nix's read-only env. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP; relevance: standard MCP config works after Nix install.
- Docs (10): [hermes_installation](hermes_installation.md) — standard install; relevance: §Quick Start says workflow is identical after Nix. [hermes_install_nixos_module](hermes_install_nixos_module.md) — sibling NixOS module; relevance: next level up (declarative). [hermes_nixos_container_mode](hermes_nixos_container_mode.md) — sibling container; relevance: third Nix integration level. [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: post-`nix profile install` first chat. [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — Nix update; relevance: `nix flake update`/`profile upgrade`/`rollback`. [hermes_configuration](hermes_configuration.md) (SP02) — config; relevance: config in `~/.hermes/` post-install. [cc_install](../claude_code/cc_install.md) — analogous install; relevance: alternative-channel install parallel. [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — analogous advanced install; relevance: parallels building from a local clone + verify. [cc_quickstart](../claude_code/cc_quickstart.md) — analogous quickstart; relevance: post-install first run. [cc_enterprise_deployment_options](../claude_code/cc_enterprise_deployment_options.md) — analogous deployment channels; relevance: parallels per-environment install channels (Nix as one).
- Snippets (10): [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — installer (non-Nix); relevance: the standard install Nix mirrors. [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: post-`nix profile install` setup path. [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — `hermes setup`; relevance: §Quick Start "workflow identical after Nix". [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: provider selection identical post-install. [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — `hermes model`; relevance: §Prerequisites provider/model selection. [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — ACP bootstrap; relevance: optional extras built on demand under Nix. [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config; relevance: standard MCP config works after Nix install. [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `config set`; relevance: config in `~/.hermes/` post-install. [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — gateway dispatch; relevance: why messaging libs need the `#messaging` variant. [snippet_hermes_agent_gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — gateway config load; relevance: `#messaging`/`#full` on-demand messaging variants.

**Note 8 `hermes_install_nixos_module`** (procedure — NixOS declarative deploy)
- Terms (8): [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — service being deployed; relevance: `services.hermes-agent` module. [term_mcp](../../term_dictionary/term_mcp.md) — MCP; relevance: §MCP Servers declarative `mcpServers` (stdio/HTTP/OAuth/sampling). [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth seeding + MCP OAuth; relevance: §OAuth Seeding (`authFile`) + MCP `auth = "oauth"` PKCE. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — hardened systemd service; relevance: §Native mode (`NoNewPrivileges`, `ProtectSystem=strict`). [term_authentication](../../term_dictionary/term_authentication.md) — secrets/provider auth; relevance: §Secrets Management (sops-nix/agenix `.env`). [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — the deployed agent; relevance: framing. [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider config; relevance: `settings.model` + provider key in env file. [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP server transports; relevance: stdio vs HTTP transport options in `mcpServers`. (+fin: term_hermes_plugin, term_credential_pool)
- Code-Repos (5): [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — flake + `nixosModules.default`; relevance: the declarative module, `settings`→`config.yaml` generation, managed-mode guards live here. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP transports; relevance: the `mcpServers` stdio/HTTP/OAuth/sampling surface the module maps onto. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/secret loading; relevance: `.env`-merged provider keys consumed at startup. [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin discovery; relevance: §Plugins (`extraPlugins`/`extraPythonPackages` entry-point discovery). [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway systemd service; relevance: the long-running service the module manages + `extraDependencyGroups [ "messaging" ]`.
- Docs (10): [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — sibling non-NixOS Nix; relevance: the simpler tier this builds on. [hermes_nixos_container_mode](hermes_nixos_container_mode.md) — sibling container; relevance: `container.enable` mode of the same module. [hermes_mcp](hermes_mcp.md) (SP09) — MCP feature; relevance: declarative `mcpServers` link-out. [hermes_configuration](hermes_configuration.md) (SP02) — config; relevance: `settings`/`config.yaml` keys map 1:1. [hermes_security](hermes_security.md) (SP03) — security; relevance: secrets-not-in-store, hardened systemd, managed-mode guards. [hermes_plugins](hermes_plugins.md) (SP04) — plugins; relevance: §Plugins declarative install link-out. [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — analogous managed MCP; relevance: parallels declarative `mcpServers` provisioning. [cc_managed_settings](../claude_code/cc_managed_settings.md) — analogous managed config; relevance: parallels blocked CLI config + declarative source of truth. [cc_server_managed_settings](../claude_code/cc_server_managed_settings.md) — analogous enterprise-managed settings; relevance: parallels `HERMES_MANAGED`/`.managed` enforcement. [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — analogous declarative env; relevance: parallels reproducible declarative deployment.
- Snippets (10): [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config; relevance: §MCP Servers declarative `mcpServers` maps onto this. [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — config schema; relevance: `settings`→`config.yaml` keys the module generates. [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `config set`; relevance: the CLI config path the module BLOCKS (declarative only). [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: `.env`-merged provider key consumed at startup. [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest; relevance: declarative plugin/extras discovery analogue. [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — auth storage; relevance: §OAuth Seeding `authFile`. [snippet_hermes_agent_cli_config_load](../../code_snippets/snippet_hermes_agent_cli_config_load.md) — config load; relevance: managed-mode config load (CLI config blocked). [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init; relevance: `settings.model` + provider boot. [snippet_hermes_agent_tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — MCP OAuth/PKCE; relevance: MCP `auth = "oauth"` PKCE in `mcpServers`. [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery; relevance: §Plugins `extraPlugins` entry-point discovery.

**Note 9 `hermes_nixos_container_mode`** (model — NixOS container deployment architecture)
- Terms (8): [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — container isolation; relevance: persistent Ubuntu container as the terminal/runtime backend. [term_docker](../../term_dictionary/term_docker.md) — Docker/Podman runtime; relevance: `container.backend = docker|podman`, root-vs-rootful access. [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — agent inside container; relevance: the bind-mounted Nix binary runs the agent. [term_self_evolving_agent](../../term_dictionary/term_self_evolving_agent.md) — self-modifying agent; relevance: container mode exists so the agent can `apt`/`pip`/`npm install` at runtime. [term_regular_checkpointing](../../term_dictionary/term_regular_checkpointing.md) — persistence semantics; relevance: §What Persists Across What table + GC-root protection. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — `/data` state; relevance: sessions/memories persist in the `/data` bind mount across rebuilds. [term_iframe_sandbox](../../term_dictionary/term_iframe_sandbox.md) — isolation model; relevance: contrast with native hardened-systemd isolation in §Deployment Mode table. (+fin: term_hermes_profile)
- Code-Repos (5): [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — flake/module + container entrypoint; relevance: container identity hash, `/data/current-package` symlink, GC-root preStart script. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — runtime startup; relevance: the bound Nix binary brings its own interpreter to bootstrap inside Ubuntu. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway service; relevance: container entrypoint runs `hermes gateway run --replace`. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — container-aware CLI; relevance: host `hermes` commands transparently `exec` into the container. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP token store; relevance: `mcp-tokens/` persist in `/data` across recreation.
- Docs (10): [hermes_install_nixos_module](hermes_install_nixos_module.md) — sibling module; relevance: container mode is `container.enable` on that module. [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — sibling Nix install; relevance: the base Nix integration. [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — update; relevance: §Updating (symlink update, no recreation, package loss rules). [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: chatting against a container deployment. [hermes_docker](hermes_docker.md) (SP03) — Docker backend; relevance: the container runtime concept link-out. [hermes_architecture](hermes_architecture.md) (SP18) — architecture; relevance: native-vs-container runtime layout. [hermes_security](hermes_security.md) (SP03) — security; relevance: container isolation vs hardened-systemd trade-off. [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — analogous container runtime; relevance: parallels persistent-container deployment model. [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — analogous hardened container; relevance: parallels native hardened-systemd vs container security. [cc_execution_environments](../claude_code/cc_execution_environments.md) — analogous execution env; relevance: parallels self-modifying mutable-environment choice.
- Snippets (10): [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — installer; relevance: container entrypoint runs the bound Nix binary's install/bootstrap. [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — startup bootstrap; relevance: bound Nix binary brings its own interpreter to bootstrap inside Ubuntu. [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — config schema; relevance: §Options Reference container settings. [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base; relevance: provider runtime inside the container. [snippet_hermes_agent_acp_server_module_helpers](../../code_snippets/snippet_hermes_agent_acp_server_module_helpers.md) — server helpers; relevance: agent process running in the persistent container. [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: container identity hash / `/data/current-package` symlink. [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup; relevance: container runtime diagnostics. [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — cron tick; relevance: scheduled work persisting via `/data` across recreation. [snippet_hermes_agent_gw_start_gateway_main](../../code_snippets/snippet_hermes_agent_gw_start_gateway_main.md) — gateway main; relevance: container entrypoint `hermes gateway run --replace`. [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker/Podman backend; relevance: `container.backend = docker|podman` isolation runtime.

All 9 notes meet the FOUR-FLOOR standard **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (all counted).
Every `term_*` ID, every `repo_*` ID, and every `snippet_hermes_agent_*` ID above is DB-verified active
(sqlite checks 2026-06-19). `cc_*` doc IDs are DB-verified active. Sibling `hermes_*` doc IDs (e.g.
`hermes_configuration`, `hermes_cli_interface`, `hermes_skills`, `hermes_mcp`, `hermes_voice_mode`,
`hermes_messaging_overview`, `hermes_acp`, `hermes_checkpoints`, `hermes_architecture`, `hermes_docker`,
`hermes_security`, `hermes_plugins`, `hermes_providers`, `hermes_honcho`) are owned by other SPs in this
series and land at finalization (verified by G5/G8). Snippet IDs live under `resources/code_snippets/` with
the `snippet_hermes_agent_` prefix and are now a COUNTED floor (≥10), no longer a bonus group.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-14)

Re-read all 7 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 quickstart-first-chat | procedure | 1200 | 5 | ✓ |
| 2 quickstart-next-layer | procedure | 1100 | 6 | ✓ |
| 3 installation | procedure | 1050 | 6 | ✓ |
| 4 learning-path | navigation | 900 | 0 | ✓ |
| 5 updating | procedure | 1700 | ≤6 (curate from 21 short cmd blocks; summarize rest in prose) | ✓ |
| 6 termux | procedure | 900 | ≤6 (from 19) | ✓ |
| 7 nix-quickstart | procedure | 900 | 6 | ✓ |
| 8 nixos-module | procedure | 1400 | ≤6 (curate) | ✓ |
| 9 container-mode | model | 1300 | 4 | ✓ |

No further splits needed. Code-heavy pages (updating/termux/nixos-module): keep ≤6 essential command
blocks, summarize the rest in prose (verbatim for the kept blocks).

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`):
YAML field order `tags → keywords → topics → language → date of note → status → building_block →
source_url → access_control_group`; body `# Title → ## Overview → source-mirrored H2s → ## Related Notes
→ footer **Source**/**Last Updated**/**Status**`. **Related Notes minimum (FOUR-FLOOR, set 2026-06-19): ≥8
term + ≥5 code-repo + ≥10 snippet + ≥10 doc links, each with a relevance clause, all counted** — supersedes
the prior ≥6-term floor and the interim three-floor wording (snippets are now a counted floor, not a bonus).
One BB/note; caps ≤2500w/≤6 code/≤400 lines. Forbidden YAML fields per master. Not invented — matches
existing `cc_` notes.

## Undigested Terms Plan (SP01)

**SP01 owns 0 new term captures.** It references concepts owned by other sub-plans (link at finalization)
and links existing verified terms. Augment re-read surfaced **0 new** undigested terms beyond the master
inventory.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_nemotron` | LINK only (capture owned elsewhere) | SP15 | First *use* in quickstart/portal; home is SP15. |
| forward refs (`term_nous_portal`, `term_tool_gateway`, `term_voice_mode`, `term_skills_hub`, `term_messaging_gateway`, `term_hermes_profile`, `term_shadow_git_checkpoint`, `term_hermes_plugin`, `term_credential_pool`, `term_honcho`) | LINK only | SP14/05/08/11/04/03/06/09 | Added to notes at finalization once captured. |
| existing verified (`term_hermes_agent`, `term_autonomous_coding_agents`, `term_mcp`, `term_acp`, `term_cron`, `term_context_window`, `term_oauth_token`, `term_sandbox_backend`, `term_subagent`, `term_session_persistence`, `term_regular_checkpointing`, `term_model_catalog`, `term_llm`, `term_voice_wake`, `term_skill_manifest`, `term_multi_agent_systems`, `term_authentication`, `term_provider_plugin`, `term_docker`, `term_self_evolving_agent`) | LINK (do NOT recreate) | — | Used in mappings above. |

## Term-Note Authoring Requirements

N/A (inherited) — SP01 owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (router + enrich, P1-hub):** Note 4 (learning-path) + enrich `term_hermes_agent` with a
  docs-series link. GATE G1–G8.
- **Phase 2 (core install + quickstart):** Notes 1, 2, 3, 5, 6. GATE G1–G8.
- **Phase 3 (Nix family):** Notes 7, 8, 9. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` · G3
density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4)** · **G6 broken-links
(`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB · **G8 in-degree ≥1 from
outside the folder**.

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
  nid=$(echo "$r"|sed "s|$VAULT/||"); [ -z "$(sqlite3 "$DB_PATH" "SELECT 1 FROM notes WHERE note_id=?" "$nid")" ]&&echo "GHOST $(basename $f): $l"; done; done
# G8: in-degree ≥1 from outside the folder
for n in hermes_quickstart_first_chat hermes_quickstart_next_layer hermes_installation hermes_learning_path hermes_updating_uninstalling hermes_install_termux_android hermes_install_nix_quickstart hermes_install_nixos_module hermes_nixos_container_mode; do
  echo -n "$n indeg(ext): "; sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM note_links l JOIN notes s ON l.source_id=s.note_id WHERE l.target_id='resources/documentation/hermes_agent/$n.md' AND s.note_id NOT LIKE 'resources/documentation/hermes_agent/%';"; done
```

## Entry Point Decision (inherited)

Contributes 9 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Getting Started & Install" section. Parent hub back-link in
`entry_research_and_ai_hub.md` (master-level).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `term_hermes_agent.md` | → `hermes_quickstart_first_chat`, `hermes_installation` | concept term → user-facing install/quickstart docs |
| `entry_code_snippets_hermes_agent.md` | → `hermes_installation`, `hermes_learning_path` | code layer ↔ docs layer |
| `repo_hermes_agent.md` | → `hermes_quickstart_first_chat` | implementation ↔ usage |
| `repo_hermes_agent_cli.md` | → `hermes_quickstart_first_chat` | CLI repo ↔ CLI quickstart |
| `thought_hermes_agent_vs_openclaw.md` | → `hermes_learning_path` | comparison → docs router |
| `entry_hermes_agent_docs.md` (new) | → all 9 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8).

## Pacing Rules (inherited)

Pilot Note 4 + the `term_hermes_agent` enrich → reindex → verify format/ghost/in-degree BEFORE
authoring the rest. Commit per phase. If multi-agent: agents return note content, master writes
serially; ≤30 agents/run; embed manifest.

## Follow-up Recommendations

- After SP01 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; create the entry point; backfill the `term_hermes_agent` / `repo_*` inlinks (G8).
- `user-stories.mdx` (262-story client-rendered showcase): if wanted later, ONE `empirical_observation` note summarizing use-case categories — not 262 notes.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit, finalized Per-Note Mapping (FOUR-FLOOR ≥8 term / ≥5
  code-repo / ≥10 snippet / ≥10 doc, all DB-verified), Doc-Note Authoring Spec, Density Re-Assessment
  (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match; **no additional splits** beyond the 2 planned.
- Collision audit: **1 removal** (`hermes_overview` → `term_hermes_agent`); note count 10→9.
- Undigested terms surfaced at augment: **0 new** (SP01 owns 0 captures).
- Entry-point decision: CREATE (inherited, >30-note series) — matches threshold.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  relevancy-selected, DB-verified). This levels up the earlier interim three-floor wording (≥8 term / ≥5
  code-repo / ≥10 doc, snippets as bonus) and the original 2026-06-14 floor (≥8 term / ≥8 snippet / ≥5 doc):
  each of the 9 notes now lists ≥8 DB-verified term notes, ≥5 `repo_hermes_agent_*` source-code repos, a
  PROMOTED Snippets (≥10) line drawn from the 517-note `snippet_hermes_agent_*` corpus (was a bonus group,
  raised from 8/9 to ≥10 and now counted), and an expanded Docs (≥10) line mixing sibling `hermes_*` (series)
  + DB-verified `cc_*` analogues; all 8 source pages re-read from `inbox/hermes_agent_docs/` to ground every
  relevance clause. No floor weakened, no cross-ref removed (additive), `status:` unchanged.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source ✓ Content Strategy ✓ Coverage Map ✓ Split Decisions ✓
Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs ✓ [FOUR-FLOOR set
2026-06-19 to ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note, all counted; all term/repo/snippet IDs DB-verified] Entry
Points ✓ Inlinks ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def ✓ Validation Scripts ✓ Pacing ✓
Density Re-Assessment ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture Phase per term ✓ best-fit glossary
✓ Term-Note Auth Reqs ✓ invokes capture-term-note ✓ Entry-Point Decision ✓ matches size threshold ✓
Slug Specificity ✓ Slug Collision ✓ dedup generalized to doc notes ✓ G8 in every phase ✓ Doc-Note
Authoring Spec derived ✓). Note: term-capture items are N/A-pass (SP01 owns 0 captures).

## Review Sign-Off

**Re-reviewed 2026-06-19 (independent, FOUR-FLOOR) — READY FOR EXECUTION (9/9 checkpoints pass).** Supersedes the
2026-06-14 sign-off below. CP1 evaluated against the FOUR-FLOOR standard (≥8 term / ≥5 code-repo / ≥10 snippet /
≥10 doc per note). Measured counts (script): all 9 notes = term 8 / repo 5 / snippet 10 / doc 10 (Note 9 doc = 7
hermes + 3 cc). 298 mapping links, 0 missing a `relevance:` clause. Anti-fabrication: all 120 unique verifiable IDs
(term + repo + snippet + cc) DB-verified PRESENT & active (0 missing, 0 inactive) against `vault_unified.db`.
Sibling `hermes_*` doc IDs correctly absent (created at finalization, exempt). CP7 re-measure: quickstart 2576w/19c,
nix-setup 5482w/44c, updating 1708w/21c — all match plan (ratio 1.00). Source headers re-read (quickstart, learning-path,
nix-setup) ground every relevance clause.

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes step (FOUR-FLOOR) | PASS | Per-note mapping ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc each (ALL counted), every link a relevance clause; measured 9/9 notes = 8/5/10/10; 120/120 cited term+repo+snippet+cc IDs DB-verified active (0 missing). |
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability (G5×6, G8×13 mentions). |
| CP3 | Entry point specified | PASS | CREATE `entry_hermes_agent_docs.md` + parent hub `entry_research_and_ai_hub.md` (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 9 notes ≤30; master holds the sub-plan split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from 339 existing `cc_*.md`; not invented. |
| CP6 | Borderline density → split | PASS | quickstart→2, nix-setup→3; all notes within caps; code-heavy pages curated ≤6. |
| CP7 | Source counts measured | PASS | Spot-check: quickstart 2576, nix-setup 5482, updating 1708 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP01 owns 0 term captures; authoring spec inherited by owning SPs; sections present. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table; 1 doc-vs-term dup removed (`hermes_overview`→`term_hermes_agent`). |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 notes (entry point + term_hermes_agent + repo_* outside folder). |

**RESULT: 9/9 → READY FOR EXECUTION.**

---

**Prior sign-off (2026-06-14 — preserved for history):** Reviewed 2026-06-14 — READY (9/9), pre-FOUR-FLOOR
(then ≥8 term + ≥5 code-repo + ≥10 doc with snippets as bonus). Superseded by the 2026-06-19 independent
re-review above.

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-synced from upstream `NousResearch/hermes-agent`
`website/docs/` — moving the pin from `95715dc` to `c253b07` (now byte-identical to upstream main). All of
this sub-plan's owned pages were independently re-measured with the ledger's convention (BODY words only,
frontmatter stripped; code-block count = lines matching `^\s*` fences ÷ 2) and the word/code counts are
**UNCHANGED**:

- `index.mdx` — 894w/2code (unchanged)
- `getting-started/quickstart.md` — 2576w/19code (unchanged)
- `getting-started/installation.md` — 1049w/10code (unchanged)
- `getting-started/learning-path.md` — 955w/0code (unchanged)
- `getting-started/updating.md` — 1708w/21code (unchanged)
- `getting-started/termux.md` — 923w/19code (unchanged)
- `getting-started/nix-setup.md` — 5482w/44code (unchanged)
- `user-stories.mdx` — 6w/0code (unchanged, stub — skipped)

No planned-note, split, density, or cross-ref decision is affected by the re-sync. The 9-note plan, the 2
splits (quickstart→2, nix-setup→3), and all density caps (≤2500w/≤6 code/≤400 lines) stand exactly as
written. (The cross-ref floor was subsequently set on 2026-06-19 to the FOUR-FLOOR standard ≥8 term + ≥5
code-repo + ≥10 snippet + ≥10 doc per note — all counted, snippets promoted from bonus — see the Per-Note
Related Notes Mapping and Augmentation Report.) Plan remains **READY**.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-14, 31/31; re-augmented 2026-06-19 FOUR-FLOOR) · Review: **DONE** (re-reviewed 2026-06-19, 9/9 READY, FOUR-FLOOR; prior 2026-06-14 9/9) · Execute: pending · Re-synced 2026-06-19 (counts unchanged)

**Source**: `inbox/hermes_agent_docs/getting-started/`, `index.mdx`, `user-stories.mdx`
**Last Updated**: 2026-06-14 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented; awaiting review)
