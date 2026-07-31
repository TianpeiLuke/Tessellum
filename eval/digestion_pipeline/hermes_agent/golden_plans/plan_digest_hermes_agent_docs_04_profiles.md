---
title: Hermes Agent Docs Digestion — Sub-Plan 04 — Profiles & Multi-Profile Ops
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/
pages:
  - user-guide/profiles.md
  - user-guide/profile-distributions.md
  - user-guide/multi-profile-gateways.md
---

# Sub-Plan 04: Profiles & Multi-Profile Ops

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP04's note
> filenames/BBs/coverage are defined.

## Scope

"Profiles & Multi-Profile Ops" — running multiple independent Hermes agents on one machine. A **profile**
is a separate Hermes home directory (`HERMES_HOME`-scoped `config.yaml`/`.env`/`SOUL.md`/memory/sessions/
skills/cron/state.db), each becoming its own command alias. This sub-plan covers: the profile lifecycle
(create/clone/use/`-p`/delete/manage), running and supervising per-profile gateways collectively as
services, and packaging a whole profile as a shareable git-repo **distribution** (author/install/update +
its ownership/security model). Source = 3 mirrored pages in `inbox/hermes_agent_docs/user-guide/`
(all substantive). **P2 / features.** Downstream link-outs: kanban worker routing (SP06), Honcho memory
peers (SP05), the messaging platforms whose bot tokens each profile isolates (SP11-13), Docker s6-overlay
gateway supervision (SP03), the dashboard profile switcher (SP10), and the `hermes profile` command
reference (SP20).

## Content Strategy

- **One BB per note.** `profiles.md` (procedure) → 2 notes (lifecycle vs gateway/service ops, the latter
  merged with `multi-profile-gateways.md`); `profile-distributions.md` is the master's `[SPLIT 2]` page —
  its procedural author→install→update lifecycle (1 note) is a distinct BB from its ownership/security
  **model** (1 note). 4 notes total.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: kanban
  orchestrator auto/manual routing (SP06), Honcho multi-agent peer creation (SP05), per-platform bot-token
  setup (SP11-13), Docker per-profile s6 supervision (SP03), the web-dashboard profile switcher (SP10), the
  full `hermes profile` flag-by-flag reference (SP20 `profile-commands`), terminal `cwd`/`home_mode` config
  blocks (SP02 `hermes_terminal_backends`/`hermes_config_files_precedence`), `hermes update` internals (SP01).
- **Owned NEW term capture:** `term_hermes_profile` (isolated agent-instance config — `HERMES_HOME`-scoped
  state directory). See Collision audit: `term_auth_profile` is an UNRELATED false LIKE hit (it is a
  per-agent credential/OAuth-refresh concept, NOT a Hermes agent instance) → DB-confirmed, do NOT link/merge.
- **Collision (augment): `term_auth_profile.md` (active) is a credential/auth-profile concept** (keywords:
  "auth profile", "per-agent credential", "OAuth refresh queue", "credential expiry state machine") — a
  textbook LIKE false-positive vs the Hermes-instance "profile." The planned `term_hermes_profile` is NOT a
  duplicate; capture it and do NOT link the unrelated term.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/profile-distributions.md | 3043 | 29 | MIXED procedure+model | 2 (split) |
| user-guide/profiles.md | 1881 | 21 | procedure | 2 (split) |
| user-guide/multi-profile-gateways.md | 2113 | 23 | procedure | 0 (merged into Note 2) |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **4 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_profiles_multi_agent.md` | procedure | profiles §What are profiles, §Quick start, §Creating a profile (Blank, `--clone`, `--clone-all`, `--clone-from`), §Using profiles (Command aliases, `-p` flag, `hermes profile use`, Knowing where you are), §Profiles vs workspaces vs sandboxing, §Configuring profiles (+dashboard), §Updating, §Managing profiles, §Deleting, §Tab completion, §How it works (`HERMES_HOME`/`HOME`/`home_mode`) | ~1500 | The profile lifecycle: a profile is a separate `HERMES_HOME` directory that auto-becomes a command alias; create blank/`--clone`/`--clone-all`/`--clone-from`, target via alias/`-p`/`profile use`, the profile-vs-workspace-vs-sandbox distinction, per-profile config, update skill-sync, manage/rename/export/import/delete, tab completion, and the `HERMES_HOME` vs OS `HOME`/`home_mode: profile` boundary. |
| 2 | `hermes_profile_gateways_services.md` | procedure | profiles §Running gateways (Different bot tokens, Safety token locks, Persistent services), §Configuring profiles (dashboard switcher); multi-profile-gateways ALL sections (When to use, Quick start, Start/stop/restart all, Manage one, Service files, Viewing logs, Identify running, Editing config, Keeping host awake, Token-conflict safety, Updating code, Troubleshooting) | ~1700 | Running many per-profile gateways as managed services on one machine: each profile = its own gateway process + bot token + LaunchAgent/systemd unit; the `hermes-gateways` wrapper loop to start/stop/restart all; per-profile service-file paths + logs; identifying what's running; token-conflict locks (Telegram/Discord/Slack/WhatsApp/Signal); `caffeinate`/`systemd-inhibit`/`loginctl` keep-awake; and the launchd/stale-PID troubleshooting recipes. |
| 3 | `hermes_profile_distributions.md` | procedure | profile-distributions §What this means, §Why git, §When should you use a distribution, §The lifecycle, §For authors (Step 1-4 + What the repo looks like), §For installers (Install, Source types, Override name, Fill in env, Check, Update, Remove), §Use cases and patterns (personal/team/community/product/ephemeral), §Recipes (pin/check-version/keep-config/clean-reinstall/fork/test) | ~1700 | Packaging a whole profile as a shareable git-repo distribution: the `distribution.yaml` manifest + `.env.EXAMPLE` flow, why git (zero build, tags = versions, fetch updates, private repos free), `hermes profile install <git-url> --alias` / `update` / `info` / `--name`, the author publish steps, the installer flow, five use-case patterns, and the recipes (version pinning status, fork, local test). |
| 4 | `hermes_profile_distribution_model.md` | model | profile-distributions §The lifecycle (distribution-owned vs user-owned table), §Distribution-owned vs user-owned, §What's NOT in a distribution (ever), §Security and trust, §Under the hood, §See also | ~1100 | The distribution data + trust model: the distribution-owned vs config-override vs user-owned path partition (what gets replaced vs preserved on update; `distribution_owned` manifest override), the hard-excluded never-shipped paths (`auth.json`/`.env`/`memories/`/`sessions/`/`state.db*`/`logs/`/`workspace/`/`plans/`/`home/`/`*_cache/`/`local/`), the unsigned-by-default trust boundary (git host + author; cron not auto-scheduled; SOUL/skills active on first chat), and under-the-hood internals (`.git/` stripped, reserved-name rejection, YAML `name`-only schema). |

**SP04 totals:** 4 notes · procedure 3 · model 1 · concept 0 (the profile concept is the owned `term_hermes_profile`).
3 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 4 · procedure 3 · model 1 · concept 0 (concept owned by the new `term_hermes_profile`).
- Source: 3 digested pages (~7.0K words) → ~6.0K words of notes (modest compression via link-outs to feature pages).
- BB mix: procedure 75%, model 25%.
- New term notes owned: **1** (`term_hermes_profile`); existing terms linked: 7 (named in scope) + supporting.

## Section Coverage Map

```
profiles.md (1881w)
├── What are profiles? / Quick start ───────────────────────────── → Note 1 (concept→term_hermes_profile)
├── Creating a profile (Blank / --clone / --clone-all / --clone-from) → Note 1 (kanban --description→SP06; honcho peer→SP05)
├── Using profiles (Command aliases / -p flag / profile use / Knowing where you are) → Note 1
├── Profiles vs workspaces vs sandboxing ───────────────────────── → Note 1 (terminal.cwd/sandbox→SP02 backends)
├── Configuring profiles (config.yaml/.env/SOUL.md + From the dashboard) → Note 1 (dashboard switcher→SP10)
├── Updating / Managing / Deleting / Tab completion ────────────── → Note 1 (update internals→SP01)
├── How it works (HERMES_HOME / HOME / home_mode / HERMES_REAL_HOME) → Note 1 (home_mode config→SP02)
├── Running gateways (intro + Docker s6 note) ──────────────────── → Note 2 (Docker s6 supervision→SP03)
├── Running gateways → Different bot tokens / Safety token locks / Persistent services → Note 2 (per-platform tokens→SP11-13)
└── Sharing profiles as distributions (teaser) ─────────────────── → Note 3 (link-out)
multi-profile-gateways.md (2113w) ── ALL sections (When to use, Quick start, Start/stop/restart all, Manage one, Service files, Viewing logs, Identify running, Editing config, Keeping host awake, Token-conflict safety, Updating code, Troubleshooting) → Note 2 (logs viewer→SP02 cli; update→SP01)
profile-distributions.md (3043w)
├── intro / What this means / Why git / When should you use ───── → Note 3
├── The lifecycle (intro) / For authors (Step 1-4 + repo layout) → Note 3
├── For installers (Install / Source types / Override name / Fill env / Check / Update / Remove) → Note 3
├── Use cases and patterns (personal / team / community / product / ephemeral) → Note 3
├── Recipes (pin / check-version / keep-config / clean-reinstall / fork / test) → Note 3 (export/import→SP20)
├── Distribution-owned vs user-owned (the ownership table) ─────── → Note 4
├── What's NOT in a distribution (ever) ────────────────────────── → Note 4
├── Security and trust ─────────────────────────────────────────── → Note 4 (prompt-injection/SOUL→SP05)
└── Under the hood / See also ──────────────────────────────────── → Note 4 (profile-commands ref→SP20)
```

No source H2/H3 orphaned. All 3 pages fully covered; feature-page detail intentionally routed to owning SPs as link-outs. `profile-distributions §The lifecycle` ownership table is the natural seam between the procedural lifecycle (Note 3) and the data/trust model (Note 4) — the [SPLIT 2] boundary.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| profiles.md (1881w, 21 code) | Note 1 (lifecycle, proc) + Note 2 (gateway/service ops, proc — merged w/ multi-profile-gateways) | Two arcs: the per-profile lifecycle (create/clone/use/config/delete) vs collectively operating per-profile gateway services; the gateway arc is topically identical to `multi-profile-gateways.md` → merge to avoid a thin note + a near-duplicate. |
| multi-profile-gateways.md (2113w, 23 code) | merged into Note 2 | <2500w on its own and the same BB/topic as profiles §Running gateways; merging keeps one cohesive "operate N gateways as services" procedure rather than two overlapping notes. |
| profile-distributions.md (3043w, 29 code, MIXED) | Note 3 (author→install→update lifecycle, proc) + Note 4 (ownership + security + internals, model) | >2500w (master `[SPLIT 2]`); separates the step-by-step distribution workflow (procedure) from the distribution-owned/user-owned partition + never-shipped invariant + trust boundary (a distinct `model` BB). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note / slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_hermes_profile` (owned NEW capture) | `term_auth_profile.md` (active — "auth profile", "per-agent credential", "OAuth refresh queue", "credential expiry state machine") | **NOT a dup** — that term is a *credential/OAuth auth-profile* concept, unrelated to a Hermes agent-instance home directory (classic LIKE false-positive, master caution list, DB-confirmed by reading its keywords) | CREATE `term_hermes_profile`; do NOT link/merge the unrelated `term_auth_profile`. |
| `hermes_profiles_multi_agent`, `hermes_profile_gateways_services`, `hermes_profile_distributions`, `hermes_profile_distribution_model` | doc-folder LIKE hits: `bedrock_inference_profiles*`, `aws_ec2_iam_roles_profiles`, `redshift_distribution_styles`, `sagemaker_distribution_image`, `tutorial_cradle_*profile*` | **NOT dups** — all unrelated domains (AWS Bedrock inference profiles, EC2 IAM instance profiles, Redshift distribution styles, Cradle/Andes config profiles); none cover Hermes agent profiles/distributions | CREATE all 4; do NOT link the unrelated AWS/Cradle doc notes. |
| all 4 doc notes vs existing `hermes_agent/` | none — `resources/documentation/hermes_agent/` has 0 notes (folder not yet created) | NEW | CREATE; intra-series links resolve at finalization (G5/G8). |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the term LIKE hit + the doc LIKE hits are false-positives
confirmed by reading note keywords/domains). New `hermes_agent/` folder → no doc-doc collisions.

## Per-Note Related Notes Mapping (FINALIZED — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note) — revised 2026-06-19

> **FOUR-FLOOR standard set 2026-06-19 (user directive — supersedes BOTH the 2026-06-14 master floor of ≥8 term +
> ≥8 snippet + ≥5 doc AND the earlier-same-day 3-floor wording that demoted snippets to "bonus").** Each note's
> `## Related Notes` now carries, ALL relevancy-selected to that note's actual content and each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`, FOUR counted groups:
> digest the Hermes source code; pick the modules that IMPLEMENT what this doc note documents), ≥10 SNIPPET notes
> pick the ≥10 whose CODE this note documents), and ≥10 DOCUMENTATION notes (`../../documentation/`, sibling
> `hermes_*` in this series + analogous `claude_code/cc_*` agent-tool docs + other relevant existing doc notes).**
> **Snippets are now a COUNTED floor (raised from the prior 8 and from the interim "bonus" label) — NO LONGER a
> links (sibling `hermes_*`) resolve at finalization (G5/G8) and are allowed un-verified. The owned
> `term_hermes_profile` is a Phase-0 capture (exists by the time notes are written) and counts toward the ≥8 term
> floor; other-SP not-yet-existing terms are marked `[own]` in a `(+fin …)` tail and are EXCLUDED from the floor.
> Every note's term floor is independently satisfied by ≥8 already-active terms even if `term_hermes_profile` is
> set aside.

**Note 1 `hermes_profiles_multi_agent`** (procedure)
- Terms (10): term_hermes_profile, term_autonomous_coding_agents, term_agent_harness, term_session_persistence, term_sandbox_backend, term_sandbox, term_idempotency, term_authentication, term_self_evolving_agent, term_multi_agent_systems — relevance: a profile is the `HERMES_HOME`-scoped state directory the harness runs from (§What are profiles / §How it works); `--clone`/`--clone-all`/`export`/`import` are idempotent copies; the §Profiles vs workspaces vs sandboxing section explicitly contrasts a profile (does NOT sandbox the agent) with a sandbox/sandbox_backend; per-profile `.env` holds auth keys; running separate coder/personal/research agents = multi-agent operation. (+fin: term_kanban_multi_agent [own] — `--description` worker routing; term_honcho [own] — per-profile AI peer on clone)
- Code-Repos (6): repo_hermes_agent_cli — the `hermes profile create/use/list/show/rename/export/import/delete` command tree + `-p` flag + tab completion this page drives; repo_hermes_agent — `get_hermes_home()` / `HERMES_HOME` path-resolution layer (119+ files) that makes state scope to a profile; repo_hermes_agent_agent_core — the per-profile config/SOUL/session/memory state the harness loads from `HERMES_HOME`; repo_hermes_agent_skills — bundled-skill seeding into a new profile (`create` seeds skills, `hermes update` syncs them); repo_hermes_agent_tui_gateway — `coder gateway start` / per-profile gateway-state scoping referenced by §Running gateways; repo_hermes_agent_cron — per-profile `cron/` directory isolated by `HERMES_HOME`.
- Docs (12): hermes_profile_gateways_services [sibling], hermes_profile_distributions [sibling], hermes_profile_distribution_model [sibling], hermes_config_files_precedence [sibling — `config.yaml`/`.env` precedence], hermes_terminal_backends [sibling — `terminal.cwd`/`home_mode: profile` boundary], cc_settings_files — analogous per-scope settings file layout (user/project/local) vs profile config; cc_settings_scopes_and_precedence — analogous config-scope precedence vs `HERMES_HOME` vs `HOME`; cc_environment_variables — analogous env-var-driven state (`HERMES_HOME`/`HERMES_REAL_HOME`); cc_sandbox_vs_permissions — analogous "isolation ≠ permission boundary" framing for "a profile does not sandbox"; cc_claude_application_data — analogous per-install data directory layout vs the profile state dir; cc_dot_claude_directory — analogous `~/.claude` home dir vs `~/.hermes/profiles/<name>`; cc_uninstall — analogous teardown vs `hermes profile delete`.
- Snippets (11): cli_main_cmd_profile — the `hermes profile create/use/list/show/rename/export/import/delete` command tree (§Creating/§Using/§Managing/§Deleting); cli_profiles_schema — profile-record schema (name/path/model/alias/description) backing `profile list`/`show`; cli_profiles_switch — `hermes profile use` sticky-default switch (§Sticky default); core_hermes_home — `get_hermes_home()` `HERMES_HOME` path resolution (§How it works); cli_config_set — per-profile `coder config set model.default`/`terminal.cwd` (§Configuring profiles); cli_config_load — per-profile `config.yaml`/`.env` load from the profile home; cli_setup_wizard — `coder setup` API-key/model configure step (§Quick start); core_skill_preprocessing — bundled-skill seeding into a new profile on `create`; cli_main_cmd_update — `hermes update` code-once + per-profile skill-sync (§Updating); cli_skills_hub — bundled-skill catalog seeded/synced per profile; cli_uninstall — `hermes uninstall`/`profile delete` teardown of profile data + alias + service (§Deleting).

**Note 2 `hermes_profile_gateways_services`** (procedure)
- Terms (10): term_hermes_profile, term_session_persistence, term_authentication, term_oauth_token, term_slack, term_webhook, term_idempotency, term_cron, term_autonomous_coding_agents, term_agent_harness — relevance: each profile runs an isolated gateway process + per-platform bot token (Telegram/Discord/Slack/WhatsApp/Signal — §Different bot tokens / §Token-conflict safety); §Alternative: multiplexing routes webhook/HTTP-inbound platforms via `/p/<profile>/` URL prefixes; per-profile `.env` holds auth/OAuth tokens; sessions namespace per profile (`agent:<profile>:…`); start/stop/restart-all services are idempotent; cron-driven bots are one of the listed multi-gateway use cases. (+fin: term_messaging_gateway [own] — per-profile gateway concept owned by SP11)
- Code-Repos (6): repo_hermes_agent_tui_gateway — the gateway process + `gateway run/start/stop/restart/install/uninstall` LaunchAgent/systemd service lifecycle + multiplexer this page operates; repo_hermes_agent_gateway_messaging — per-platform bot-token binding, token-conflict locks, and `/p/<profile>/` webhook routing for Telegram/Discord/Slack/WhatsApp/Signal; repo_hermes_agent_cli — `hermes -p <profile> gateway`, `hermes logs`, `hermes status`, `hermes-gateways` wrapper dispatch; repo_hermes_agent — `HERMES_HOME` per-profile PID/lock/log/`runtime_status.json` placement; repo_hermes_agent_cron — cron-driven bot profiles supervised alongside gateways; repo_hermes_agent_agent_core — per-profile session-store namespacing (`agent:<profile>:…`) and provider-key resolution per turn.
- Docs (11): hermes_profiles_multi_agent [sibling — the base profile concept], hermes_profile_distributions [sibling], hermes_profile_distribution_model [sibling], hermes_cli_interface [sibling — `hermes logs`/`status` viewer], hermes_messaging_media_settings [sibling — per-platform token config], hermes_config_files_precedence [sibling — per-profile `.env`/`config.yaml`], cc_background_session_hosting — analogous long-running managed background-agent hosting; cc_loop_scheduled_tasks — analogous scheduled/always-on task supervision; cc_scheduled_task_execution_model — analogous service execution/restart model; cc_slack_setup_and_routing — analogous platform bot-token setup + routing; cc_environment_variables — analogous per-process env/token isolation.
- Snippets (11): cli_gateway_lifecycle — `gateway run/start/stop/restart/install/uninstall` lifecycle (§Manage one profile); cli_gateway_dispatch — `coder gateway <action>` → `hermes -p coder gateway` dispatch + the `hermes-gateways` wrapper loop; cli_gateway_systemd — LaunchAgent/`.plist` + systemd-user `.service` file install (§Service files); cli_gateway_pid_discovery — `gateway.pid` discovery + stale-PID recovery (§Stale PID / §Troubleshooting); cli_gateway_windows — the `launchctl unload`/501-domain reload recovery surface (§"Could not find service…"); cli_logs — the `hermes logs -f`/`-p` structured log viewer (§Viewing logs); core_hermes_home — per-profile PID/lock/log/`runtime_status.json` placement under `HERMES_HOME`; cli_main_cmd_profile — `hermes profile list`/`-p <profile> gateway` targeting (§Identify what's running); gw_runner_router — the multiplexer that enumerates profiles and routes each inbound message to its owning profile (§Alternative: multiplexing); gw_runner_session_key — `agent:<profile>:…` session-key namespacing keeping multiplexed sessions from colliding (§Session keys namespaced); gw_status_health — `hermes status` reporting the multiplexer + the profiles it serves / per-profile `runtime_status.json` (§One PID/lock and one status surface).

**Note 3 `hermes_profile_distributions`** (procedure)
- Code-Repos (5): repo_hermes_agent_cli — the `hermes profile install/update/info/--alias/--name/--force-config` command surface + `.env.EXAMPLE` writing + reserved-name rejection this lifecycle exercises; repo_hermes_agent — clone-into-temp, `.git/`-stripping, distribution-owned copy + `HERMES_HOME` placement internals; repo_hermes_agent_skills — `skills/` packaged + synced into the installed profile; repo_hermes_agent_cron — `cron/` jobs shipped in the repo (not auto-scheduled on install); repo_hermes_agent_mcp_toolsets — `mcp.json` MCP-server connections bundled in the distribution.
- Docs (11): hermes_profile_distribution_model [sibling — the ownership/trust model this lifecycle assumes], hermes_profiles_multi_agent [sibling — the base profile being packaged], hermes_profile_gateways_services [sibling — the gateway an installed distribution can run], hermes_installation [sibling — `hermes profile install` git-clone install flow], hermes_config_files_precedence [sibling — preserved `config.yaml` on update], cc_plugin_marketplaces_and_install — analogous shareable-bundle install-from-source flow; cc_plugin_sources — analogous git/URL/local source-type handling; cc_plugin_dependencies — analogous manifest version/dependency declaration vs `distribution.yaml`; cc_plugin_user_config_and_env — analogous installer-supplied env/config vs `.env.EXAMPLE`; cc_update_and_release_channels — analogous tagged-version update/release semantics; cc_bundled_skills — analogous bundled-skill packaging vs `skills/` in the repo.
- Snippets (11): cli_main_cmd_profile — the `hermes profile install/update/info/--alias/--name` command surface (§Install/§Update/§Check); cli_profiles_schema — the `distribution.yaml`-backed profile/distribution record (name/version/source/installed) shown by `profile info`/`list`; cli_config_load — preserved `config.yaml` load on update; cli_config_schema — `distribution.yaml`/`config.yaml` schema parsing (`env_requires`, `distribution_owned`); cli_setup_installer — the clone→read-manifest→check-env→copy→write-`.env.EXAMPLE` install flow (§Install steps); cli_skills_install — `skills/` packaged + installed into the profile; core_skill_preprocessing — bundled-skill seeding/preprocess on install; core_hermes_home — distribution-owned copy + `HERMES_HOME` placement of the installed profile; cli_mcp_config — `mcp.json` MCP-server connections bundled in the distribution; cli_cron — `cron/` jobs shipped in the repo (printed, not auto-scheduled); cli_main_cmd_update — the `hermes profile update` re-clone-and-replace-distribution-owned semantics (§Update).

**Note 4 `hermes_profile_distribution_model`** (model)
- Terms (10): term_hermes_profile, term_prompt_injection, term_oauth_token, term_pii, term_authentication, term_idempotency, term_session_persistence, term_human_in_the_loop, term_graduated_trust, term_supply_chain — relevance: the model partitions distribution-owned (replaced on update) vs config-override (preserved) vs user-owned (never touched: `auth.json`/`.env`/`memories/`/`sessions/`/`state.db*`) paths idempotently; the unsigned-by-default trust boundary (you trust the git host + author) is a supply-chain/graduated-trust posture where a malicious SOUL/skills could prompt-inject, so cron is human-approved-not-auto-scheduled (human-in-the-loop) while SOUL/skills go active on first chat; `auth.json` (OAuth tokens)/`.env`/PII memories/sessions are hard-excluded never-shipped invariants. (+fin: term_skills_hub [own])
- Code-Repos (5): repo_hermes_agent — the regression-tested never-shipped hard-exclude invariant (`auth.json`/`.env`/`memories/`/`sessions/`/`state.db*`/`logs/`/`workspace/`/`plans/`/`home/`/`*_cache/`/`local/`), `.git/`-stripping, and reserved-name rejection this model documents; repo_hermes_agent_cli — `distribution_owned` manifest override, `--force-config`, and the delete-preview surfacing distribution provenance; repo_hermes_agent_skills — SOUL/skills become active on first chat (the trust surface); repo_hermes_agent_cron — cron jobs explicitly NOT auto-scheduled (human-approved enablement); repo_hermes_agent_mcp_toolsets — `mcp.json` server connections that ship and the credentials they don't.
- Docs (11): hermes_profile_distributions [sibling — the lifecycle this model governs], hermes_profiles_multi_agent [sibling — the profile state being partitioned], hermes_profile_gateways_services [sibling — per-profile credential isolation], hermes_security_skill_memory_settings [sibling — SOUL/skill/memory trust settings], hermes_terminal_backends [sibling — `home/` mount excluded path], cc_security_architecture — analogous agent-tool security/trust model; cc_prompt_injection_defenses — analogous malicious-content (SOUL/skill) injection threat framing; cc_what_claude_can_access — analogous data-access/never-shared boundary; cc_claude_application_data — analogous user-data vs shipped-config partition; cc_managed_settings — analogous owned-vs-overridable settings partition; cc_authentication — analogous credential (OAuth `auth.json`) handling that is deliberately not shipped.
- Snippets (11): cli_profiles_schema — the profile/distribution record + `distribution_owned`/version provenance the delete-preview surfaces; cli_config_schema — the `distribution.yaml` minimal `name`-only schema + reserved-name rejection (§Under the hood); core_credential_sources — credential-source resolution showing what is NOT shipped (`auth.json`/`.env`); cli_config_load — config-override (preserved-on-update) vs distribution-owned partition load; core_skill_utils_frontmatter — SOUL/skill frontmatter parsing for content that becomes active on first chat (the trust surface); core_skill_commands_discovery — skill discovery making shipped skills active (trust boundary); core_hermes_home — `HERMES_HOME` placement + the never-shipped user-owned paths under it; cli_uninstall — `profile delete` teardown that surfaces distribution provenance; tools_credential_files — the credential files (`auth.json`/`.env`) deliberately excluded as never-shipped invariants; cli_cron — cron jobs explicitly NOT auto-scheduled (human-approved enablement, §Security and trust); cli_mcp_config — `mcp.json` server connections that ship while their credentials do not.

All 4 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc. Term IDs are under
`resources/term_dictionary/`, code-repo IDs under `areas/code_repos/`, and snippet IDs under
active. `hermes_*` doc links resolve in `resources/documentation/hermes_agent/` (intra-series sibling links land
at finalization, verified by G5/G8) and are allowed un-verified. Snippet IDs (`snippet_hermes_agent_*`, buckets
cli/core/gw/tools) are now a COUNTED floor (≥10 per note), no longer a bonus group. The owned `term_hermes_profile`
is captured in Phase 0 (BEFORE the notes), so it counts toward the ≥8 term floor; each note ALSO has ≥8
already-active terms independent of it.
`[own]` forward-refs to other SPs (`term_kanban_multi_agent`, `term_honcho`, `term_messaging_gateway`,
`term_skills_hub`) are ADDITIONAL `(+fin)` tails, EXCLUDED from the floor.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 3 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 profiles-multi-agent | procedure | 1500 | ≤6 (curate from 21 short cmd blocks; one canonical create/clone/use block + `terminal.cwd` YAML; rest in prose) | ✓ |
| 2 profile-gateways-services | procedure | 1700 | ≤6 (curate from profiles §gateways + multi-profile-gateways 23 blocks; keep the `hermes-gateways` wrapper + caffeinate/systemd-inhibit + service-file table) | ✓ |
| 3 profile-distributions | procedure | 1700 | ≤6 (curate from 29 blocks; keep `distribution.yaml` manifest + author publish + `profile install`/`update` + `.env.EXAMPLE`) | ✓ |
| 4 profile-distribution-model | model | 1100 | ≤6 (keep distribution-owned table block + `distribution_owned` override + never-shipped list) | ✓ |

No further splits needed — all 4 notes ≤2500w. Notes 1/2/3 are dense (~1500-1700w) but each is one
topically-cohesive single-BB cluster; the 21+23+29 source code blocks are curated to ≤6 load-bearing blocks
per note, with the rest summarized in prose (kept blocks verbatim). Borderline check (per review CP6
default-to-keep): each is one arc with no BB mixing → KEEP. If any note exceeds 350 lines during writing,
STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it
IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** — FOUR-FLOOR standard set 2026-06-19, was ≥8 term + ≥8 snippet + ≥5 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP04)

**SP04 owns 1 new term capture: `term_hermes_profile`.** Captured in **Phase 0** (BEFORE any digest note),
via `/tessellum-capture-term-note`, NOT inline. Every other Hermes-specific concept SP04 touches is owned by
another sub-plan (link at finalization) or is an existing verified term. Augment re-read surfaced **0
additional new** undigested terms SP04 should own.

| Term | Decision | Owner | Capture Phase | Stub or Full | Best-fit glossary | Source page | Note |
|------|----------|-------|---------------|--------------|-------------------|-------------|------|
| `term_hermes_profile` | **CAPTURE (NEW)** | **SP04** | **Phase 0** | full | `acronym_glossary_systems` | profiles.md | Isolated Hermes agent instance = a `HERMES_HOME`-scoped state directory (config/.env/SOUL/memory/sessions/skills/cron/state.db) that auto-becomes a command alias. DB pre-flight: NO matching note (`term_hermes_profile` absent); `term_auth_profile` is an UNRELATED false LIKE hit (credential/OAuth concept). → create full. |
| `term_kanban_multi_agent` | LINK only (forward-ref, +fin) | SP06 | — | — | acronym_glossary_workflows | profiles.md | `--description` profile role for kanban worker routing; concept home is SP06. |
| `term_honcho` | LINK only (+fin) | SP05 | — | — | acronym_glossary_tools | profiles.md | clone creates a Honcho AI peer per profile; concept home is SP05. |
| `term_messaging_gateway` | LINK only (+fin) | SP11 | — | — | acronym_glossary_systems | profiles.md / multi-profile-gateways.md | per-profile gateway processes/tokens; gateway concept owned by SP11. |
| `term_skills_hub` | LINK only (+fin) | SP05 | — | — | acronym_glossary_tools | profiles.md / profile-distributions.md | bundled-skill seeding/sync into profiles; concept home is SP05. |

### Renamed (general → specific)

| Original (would-be) slug | Renamed to | Reason |
|---|---|---|
| `term_profile` | `term_hermes_profile` | Bare "profile" is a one-word common-English noun colliding with AWS instance/IAM/inference profiles, Cradle config profiles, and the unrelated `term_auth_profile` credential concept. The Hermes-scoped name disambiguates the agent-instance meaning. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_auth_profile` (would-be merge target) | `resources/term_dictionary/term_auth_profile.md` (active — credential/OAuth-refresh concept) | **NOT removed/merged** — it is an UNRELATED concept (false LIKE hit), NOT the same as a Hermes agent profile. SP04 captures the distinct `term_hermes_profile` and does NOT link/merge `term_auth_profile`. |
| `term_profile_distribution` | none substantive (no matching note) | Not captured as a standalone term — the distribution concept is fully carried by the two distribution doc notes (procedure + model); no extra term needed (low conceptual reuse outside SP04). |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

`term_hermes_profile` MUST be authored via **`/tessellum-capture-term-note "Hermes Profile"`** (interactive or
via ENRICHER_INPUTS + SOURCE CONTENT), NOT inline-authored within a digest note. The capture skill enforces:

- **YAML**: `tags` (resource, terminology, systems-domain tags), `keywords` (Hermes profile, HERMES_HOME,
  multi-agent instance, profile alias), `topics`, `language: markdown`, `date of note`, `status: active`,
  `building_block: concept` (MUST be concept), `access_control_group: ["general"]`, `related_wiki: null`
  (no internal wiki for external OSS docs). Forbidden fields per master.
- **H1/H2 order**: `# Hermes Profile` → `## Definition` (what it is: a `HERMES_HOME`-scoped agent-instance
  state directory; problem it solves: run multiple isolated agents on one machine) → `## Context`
  (Hermes Agent; multi-agent operators; CLI/gateway/dashboard) → `## Key Characteristics` (separate
  config/.env/SOUL/memory/sessions/skills/cron/state.db; auto command alias; NOT a sandbox; `HERMES_HOME`
  vs OS `HOME`/`home_mode`; clone variants; distributions) → `## Related Terms` (8-15 vault links;
  in-domain + cross-domain) → `## References` (external URLs ONLY — the profiles/distributions/
  multi-profile-gateways docs pages; NO `term_*.md` here).
  `https://hermes-agent.nousresearch.com/docs/user-guide/profiles.md`, plus ≥1 external orthogonal source
  (e.g. analogous multi-tenant agent-instance / `kubectl config use-context` analogy the docs cite). Run
- **Cross-domain diversity** (≥3 in-domain + ≥3 cross-domain): in-domain → `term_autonomous_coding_agents`,
  `term_agent_harness`, `term_session_persistence`, `term_sandbox_backend`; cross-domain (contrast/component)
  → `term_authentication`/`term_oauth_token` (per-profile creds), `term_multi_agent_systems` (operating many),
  `term_idempotency` (clone/export). Forward-ref `[own]` terms added at finalization.
- **MathJax**: N/A (no math in this term).
- **Fleeting-content guard**: strip person aliases / bare ETAs / dollar amounts (none expected).
- **Glossary**: update `acronym_glossary_systems` — 4-5 sentence Description max, bold the single
  distinguishing fact (**a profile is a separate `HERMES_HOME` directory, not a sandbox**), NO metrics, exact
  `**Full Name** / **Description** / **Documentation** / **Wiki** / **Related**` template.
- **Depth-scaled Related Terms**: target Simple/Moderate (40-150 lines) → **8-10** Related Terms minimum.
- **Backlink expansion** (Step 6e, REVERSE): add `term_hermes_profile` to the `## Related Terms` of in-domain
  + cross-domain existing term notes that should reference it (target 5-10), e.g. `term_autonomous_coding_agents`,
  `term_agent_harness`, `term_session_persistence`, `term_sandbox_backend`, `term_multi_agent_systems`.
- **>200-line decomposition**: if the note exceeds 200 lines, decompose per Step 7 (procedure → `sop_*`,
  model/argument → `thought_*`); expected to stay well under, so unlikely.
- **Pre-flight outcome routing**: DB pre-flight returned NO matching note → proceed to create full
  (`term_auth_profile` is a different concept, not a stub of this one — do NOT overwrite it).

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (term capture):** Capture `term_hermes_profile` via `/tessellum-capture-term-note` → reindex →
  verify it exists in DB BEFORE writing any digest note (so the ≥8-floor citations resolve, not ghosts). GATE
  G1 (format) + G5 (DB-verify) on the new term note.
- **Phase 1 (profile lifecycle + ops, P2 pilot):** Notes 1, 2. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE Note 2. GATE G1–G8.
- **Phase 2 (distributions):** Notes 3, 4. GATE G1–G8.
- **Phase 1b/2b (inlinks):** Add the inlink-table edges (G8) AFTER the notes in each phase land; gated, not a recommendation.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for
kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every
ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
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
# G8: in-degree ≥1 from outside the folder (incl. the owned term note)
for n in hermes_profiles_multi_agent hermes_profile_gateways_services hermes_profile_distributions hermes_profile_distribution_model; do
echo -n "term_hermes_profile indeg: "; sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM note_links WHERE target_id='resources/term_dictionary/term_hermes_profile.md';"
```

## Entry Point Decision (inherited)

Contributes 4 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Profiles & Multi-Profile Ops" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP04 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).
The new `term_hermes_profile` is glossed in `acronym_glossary_systems` (Phase 0 capture).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_cli.md` | → `hermes_profiles_multi_agent`, `hermes_profile_distributions` | CLI repo (`hermes profile` command tree) ↔ profile usage docs |
| `repo_hermes_agent_tui_gateway.md` | → `hermes_profile_gateways_services` | gateway repo ↔ per-profile gateway/service ops |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_profile_gateways_services` | messaging gateway repo ↔ per-profile bot-token/gateway ops |
| `repo_hermes_agent.md` | → `hermes_profile_distribution_model` | implementation ↔ distribution ownership/security model |
| `term_hermes_profile.md` (new, Phase 0) | → `hermes_profiles_multi_agent`, `hermes_profile_gateways_services`, `hermes_profile_distributions`, `hermes_profile_distribution_model` | concept term → all 4 user-facing profile docs |
| `term_auth_profile.md` | (NO inlink — unrelated credential concept) | confirmed false-positive; do NOT link |
| `entry_code_snippets_hermes_agent.md` | → `hermes_profiles_multi_agent`, `hermes_profile_distributions` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 4 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 1b/2b), not a recommendation.

## Pacing Rules (inherited)

Phase 0: capture `term_hermes_profile` + reindex + DB-verify FIRST (so floor citations are not ghosts). Then
pilot Note 1 (`hermes_profiles_multi_agent`) → reindex → verify format/ghost/in-degree BEFORE authoring the
rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each
note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6
load-bearing blocks, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split.
If multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP04 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 4 rows to the
  master-created entry point; backfill the `repo_hermes_agent_*` / `term_hermes_profile` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After the relevant SPs land: cross-link `hermes_profiles_multi_agent` ↔ SP06 kanban worker routing, ↔ SP05
  Honcho multi-agent peers, ↔ SP03 Docker s6 per-profile supervision, ↔ SP10 dashboard profile switcher.
- Backlink-expand `term_hermes_profile` into in-domain + cross-domain existing term notes (Step 6e target 5-10).

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (1 term LIKE false-positive + 4 doc LIKE false-positives,
  all DB-confirmed by reading keywords/domains), finalized Per-Note Mapping (≥8 term + ≥5 code-repo + ≥10 snippet
  sub-tables), Term-Note Authoring Requirements (full spec for `term_hermes_profile`), Doc-Note Authoring
  Spec (derived from `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match measured; **no additional splits** beyond the planned (profiles→2,
  profile-distributions→2, multi-profile-gateways merged into Note 2). All 4 notes ≤2500w; code-heavy notes
  curated to ≤6 blocks.
- Collision audit: **0 removals** — `term_auth_profile` is an UNRELATED concept (NOT merged), the AWS/Cradle
  doc-folder hits are unrelated domains; no doc note duplicates an existing term/doc note. **1 specificity
  rename** recorded (`term_profile` → `term_hermes_profile`).
- Owned-term capture: **1** (`term_hermes_profile`, Phase 0); DB pre-flight = NO matching note → create full.
- Undigested terms surfaced at augment: **0 additional new** beyond the 1 owned capture.
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.
- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  to a "bonus" group; snippets are now a COUNTED floor raised to ≥10 (was 8). Code-Repos line (primarily
  `repo_hermes_agent_*` modules that implement each documented surface) and Docs line (≥10: sibling `hermes_*` +
  2026-06-19; cited `cc_*` docs verified active. Per-note achieved: 10 term / 5–6 repo / 11 snippet / 11–12 doc —
  all clear the four-floor standard.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (≥8 term/
Points ✓ Inlinks (all 4 + term) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived)
✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (Phase 0) ✓ best-fit glossary (acronym_glossary_systems) ✓ Term-Note Auth Reqs (full for
`term_hermes_profile`) ✓ invokes capture-term-note ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug
Specificity (`term_profile`→`term_hermes_profile` renamed + reason) ✓ Slug Collision (1 term + 4 doc LIKE
false-positives caught, DB-confirmed) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND
documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**
**Re-reviewed 2026-06-19 (independent, FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).** Independent
absent — the justified Phase-0 owned capture, excluded from the floor); all 8 cited code-repos active; all 29 distinct
cited snippet IDs (`snippet_hermes_agent_*`) active; all 22 distinct cited `cc_*` doc IDs active. Per-note measured tally:
Note1 10t/6r/11s/12d, Note2 10t/6r/11s/11d, Note3 10t/5r/11s/11d, Note4 10t/5r/11s/11d — every note clears
≥8t/≥5r/≥10s/≥10d with a relevance clause on every entry (no bare links). CP7 source re-measure matches ledger exactly
(profiles 1881w/21c, profile-distributions 3043w/29c, multi-profile-gateways 2113w/23c; ratio 1.00). CP8 dedup re-confirmed:
`term_auth_profile` keywords ("per-agent credential", "OAuth refresh queue", "credential expiry state machine") are a
LIKE false-positive, NOT the Hermes agent-instance profile. No stale 3-floor/"bonus" wording remains as the current
standard (all such phrases are framed historically). No factual fixes required.

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 (G1/G5 on term) + 2 note phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (4 rows under a Profiles section); parent hub at master level (matches >30 threshold); term glossed in `acronym_glossary_systems`. |
| CP4 | Plan size manageable | PASS | 4 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | profiles→2, profile-distributions→2, multi-profile-gateways merged; all notes ≤2500w; code-heavy notes curated ≤6; dense notes (1/2/3) checked → cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15, re-measured 2026-06-19 (mirror c253b07): profile-distributions 3043, profiles 1881, multi-profile-gateways 2113 — measured == master ledger (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP04 owns 1 capture (`term_hermes_profile`, Phase 0, full, `acronym_glossary_systems`); Undigested Terms Plan + full Term-Note Authoring Reqs present; multi-source/dry-fall mandate stated; `/tessellum-capture-term-note` invoked. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers the 1 owned term + all 4 doc notes (term_dictionary AND documentation/); `term_auth_profile` LIKE false-positive DB-confirmed (NOT merged); 4 doc LIKE hits unrelated domains; `### Renamed` (`term_profile`→`term_hermes_profile`) + `### Removed` sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 4 notes + the term from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 1b/2b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.** (Independent re-review 2026-06-19, FOUR-FLOOR standard: 9/9 → READY.)

## Re-Sync Note (2026-06-19)

Re-downloaded the local doc mirror (`inbox/hermes_agent_docs/`) from upstream `main` at HEAD `c253b07`
(was pinned `95715dc`) and independently re-measured this sub-plan's owned page using the ledger
convention (body-only word count after stripping YAML frontmatter; code blocks = `^\s*```` lines ÷ 2):

- user-guide/multi-profile-gateways.md — 1283w/18code -> 2113w/23code (my fresh re-measurement == manifest, no discrepancy)

Unchanged owned pages spot-re-measured and confirmed stable: profiles.md (1881w/21code), profile-distributions.md (3043w/29code).

**Density re-decision:** Note 2 (`hermes_profile_gateways_services`) is the only note materially affected —
multi-profile-gateways.md merges wholesale into it and grew +830w/+5code. Re-evaluated against the
≤2500w/≤6code/≤400-line caps: the note compresses via link-outs (per-platform bot-token setup→SP11-13,
Docker s6 supervision→SP03, logs viewer→SP02, update internals→SP01) and curates the now-23 source blocks
to ≤6 load-bearing ones, so it stays under the 2500w cap. **Outcome: no split** — bumped the ~Words
estimate 1500→1700 and the code-block source count 18→23 in the Planned Notes / Density / Split tables. No
other planned note is touched.

**Cross-ref floor (superseded later same day):** as of this 2026-06-19 re-sync the floor was ≥8 term + ≥8
snippet + ≥5 doc; it was subsequently **set 2026-06-19 to the FOUR-FLOOR standard** — ≥8 term + ≥5 code-repo +
master floor and an interim 3-floor wording that had demoted snippets to "bonus"; snippets are now a counted ≥10
floor) — see the Per-Note Related Notes Mapping and Augmentation Report. No planned-note filename, BB type, or
gate was altered.

**Plan remains READY** for execution (9/9 review checkpoints still hold; no cap breach forced a split).

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 to FOUR-FLOOR) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed 2026-06-19 FOUR-FLOOR, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/{profiles,profile-distributions,multi-profile-gateways}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
