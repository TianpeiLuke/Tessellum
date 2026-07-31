---
title: Hermes Agent Docs Digestion — Sub-Plan 10 — Dashboard & Runtimes
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/web-dashboard.md
  - user-guide/features/extending-the-dashboard.md
  - user-guide/features/codex-app-server-runtime.md
---

# Sub-Plan 10: Dashboard & Runtimes

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP10's note
> filenames/BBs/coverage are defined.

## Scope

The browser-based admin surface and the alternate execution runtime: the `hermes dashboard` web UI
(pages, REST API, gated-mode auth providers, Hermes-Desktop remote-backend wiring), the theme + plugin
extension system layered on top of it, and the opt-in Codex app-server runtime that hands `openai/*`
turns to the Codex CLI's own tool loop. Source = 3 mirrored pages in `inbox/hermes_agent_docs/` (all
substantive). **P3 / features** — LINK-heavy: nearly every concept these pages touch is already an
existing term note or is owned by another sub-plan, so SP10 links rather than recreates. Downstream
SPs link back to `hermes_web_dashboard_overview` and `hermes_codex_app_server_runtime`.

## Content Strategy

- **One BB per note.** `web-dashboard.md` mixes a feature-tour procedure, a REST API model, and a
  gated-auth procedure → split into 3 notes. `extending-the-dashboard.md` mixes a theming procedure with
  a plugin-authoring procedure (+ a stable API/SDK reference model) → split into 3 notes.
  `codex-app-server-runtime.md` mixes a tool-availability model with an enable/operate procedure → split
  into 2 notes. **8 notes total.**
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the auth
  gate's OAuth/PKCE internals + Nous Portal billing (SP09/SP14), the dashboard's per-page features
  (sessions SP02, cron SP06, skills/memory SP05, channels/pairing SP11-13, webhooks SP12,
  credential-pool SP09, checkpoints/security/shell-hooks SP03/SP06), the CLI/TUI it embeds (SP02), the
  config fields it edits (SP02), the kanban/goal/delegation workflows the Codex runtime hosts (SP06),
  and the media/browser tools the Codex callback re-exposes (SP08).
- **Collision (augment): no `term_web_dashboard` / `term_dashboard` / `term_admin_panel` exists in
  `term_dictionary/`, and no `hermes_agent/` doc note exists yet** (DB scan 2026-06-15). The planned
  doc notes are NEW; the reusable concepts they touch are existing terms or owned by other SPs.
- **Owned captures: 0.** "Web dashboard" is a Hermes-specific feature surface, not a cross-domain
  reusable concept that survives the specificity audit (master directive: owned captures only if a
  genuinely new reusable concept survives collision audit; otherwise 0 + link existing). The Codex
  app-server runtime is a product-integration concept (Codex CLI ↔ Hermes) owned conceptually by the
  existing `term_agentcore_runtime` analogue + Hermes' own implementation snippets, not a new owned term.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/web-dashboard.md | 9537 | 27 | MIXED procedure+model+auth-procedure | 3 (split) |
| user-guide/features/extending-the-dashboard.md | 5324 | 32 | MIXED procedure(theme)+procedure(plugin)+model(API) | 3 (split) |
| user-guide/features/codex-app-server-runtime.md | 3959 | 14 | MIXED model(tools)+procedure(enable/operate) | 2 (split) |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **8 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_web_dashboard_overview.md` | procedure | web-dashboard §Quick Start (+Options), §Managing multiple profiles, §Prerequisites, §Pages (Status, Chat, Connecting Desktop to remote backend (tour-level), Config, API Keys, Sessions, Logs, Analytics, Cron, Profiles, Skills, MCP, Webhooks, Pairing, Channels, System), §`/reload` Slash Command, §Themes & plugins (summary) | ~1700 | Launching + using the local admin UI: `hermes dashboard` flags, the machine-level profile switcher, the `web`/`pty` extras, the embedded TUI Chat tab over xterm.js, and a one-line tour of all 16 admin pages (Status…System) with link-outs to each feature's owning page. |
| 2 | `hermes_dashboard_rest_api.md` | model | web-dashboard §REST API (profile-scoped endpoints note, GET/PUT/DELETE families: status, sessions(+search/messages/stats/export/prune/rename), config(+defaults/schema), env, logs, analytics, cron, skills, tools/toolsets, §Admin endpoints table: mcp/messaging/pairing/webhooks/credentials/memory/gateway/ops/system/hermes-update/curator/portal), §CORS, §Development, §Automatic Build on Update | ~1500 | The dashboard's HTTP surface as a model: profile-scoped `?profile=` query param, the read/write endpoint families the SPA consumes, the admin-endpoints table behind the auth gate, localhost-only CORS, the Vite dev proxy, and the on-update frontend rebuild. |
| 3 | `hermes_dashboard_auth_remote.md` | procedure | web-dashboard §Authentication (gated mode) (+when the gate engages, fail-closed, Nous provider+register+worked example, Username/password provider+worked example+writing your own, Self-hosted OIDC+Keycloak worked example, Public URL override, OAuth flow, Cookies, Logout, Audit log, Custom providers, Verifying the gate), §Connecting Hermes Desktop to a remote backend (+backend/desktop setup, env override, troubleshooting) | ~1700 | Securing a non-loopback dashboard: when the auth gate engages, fail-closed bind, the three bundled `DashboardAuthProvider`s (Nous OAuth / username-password / self-hosted OIDC) + register/login recipes, `public_url` override behind a proxy, session cookies/TTL/logout/audit log, and wiring Hermes Desktop to a remote backend. |
| 4 | `hermes_dashboard_themes.md` | procedure | extending §Themes (Quick start, Palette/typography/layout, Layout variants, Theme assets, Component chrome overrides, Color overrides, Raw customCSS, Built-in themes, Full theme YAML reference) | ~1400 | Reskinning the dashboard with a drop-in YAML theme: the 3-layer palette `color-mix()` cascade, typography + UI font picker, layout/density, `layoutVariant` (standard/cockpit/tiled), image assets as CSS vars, component-chrome overrides, color overrides, raw 32-KiB-capped `customCSS`, and the 7 built-ins. |
| 5 | `hermes_dashboard_plugins.md` | procedure | extending §Plugins (Quick start, Directory layout, Manifest reference (+icons), Plugin SDK, Shell slots (+catalogue, page-scoped slots, HMR), Replacing built-in pages (tab.override), Augmenting pages (page-scoped slots), Slot-only plugins (tab.hidden), Backend API routes (+accessing internals), Custom CSS per plugin, Plugin discovery & reload (+load lifecycle)), §Combined theme + plugin demo, §Troubleshooting | ~1700 | Authoring a drop-in dashboard plugin: the `manifest.json` + IIFE bundle, the `window.__HERMES_PLUGIN_SDK__` (no bundled React), shell + page-scoped slots, `tab.override`/`tab.hidden`, FastAPI backend routes under `/api/plugins/<name>/`, per-plugin CSS, 3-dir discovery + rescan + load lifecycle, the Strike-Freedom demo, and troubleshooting. |
| 6 | `hermes_dashboard_extension_api.md` | model | extending §The Plugin SDK (surface), §API reference (Theme endpoints, Plugin endpoints, SDK on `window`) | ~700 | The stable extension contract as a model: the `window.__HERMES_PLUGIN_SDK__` surface (React/hooks/components/api/fetchJSON/utils), the `__HERMES_PLUGINS__.register`/`registerSlot` globals, and the theme/plugin REST endpoints (`/api/dashboard/themes`, `/plugins`, `/plugins/rescan`, static asset serving). |
| 7 | `hermes_codex_runtime_tools.md` | model | codex §Why, §What tools the model actually has (Codex built-ins, native Codex plugins, Hermes tool callback, What's NOT available), §Workflow features (`/goal`, Kanban, Cron), §Trade-offs table, §Architecture (diagram), §Hermes tool callback (the MCP server) | ~1700 | The Codex app-server runtime as a model: three independent tool sources (Codex built-ins shell/apply_patch/update_plan/view_image/web_search; auto-migrated native Codex plugins; the `hermes-tools` MCP callback for web/browser/vision/image/skills/TTS), the four agent-loop tools that are unavailable, workflow-feature compatibility, and the JSON-RPC-over-stdio architecture. |
| 8 | `hermes_codex_runtime_setup.md` | procedure | codex §Prerequisites, §Enabling, §Self-improvement loop (memory + skill nudges), §How approvals work, §Permission profiles, §Auxiliary tasks and ChatGPT subscription token cost, §Editing `~/.codex/config.toml` safely, §Multi-profile / multi-tenant setups, §HOME passthrough, §MCP server migration, §Native Codex plugin migration, §Disabling, §Limitations | ~1700 | Enabling + operating the Codex runtime: `/codex-runtime codex_app_server`, the codex-CLI + `codex login` prereqs, the managed `~/.codex/config.toml` block (MCP/plugin migration), Codex's three sandbox permission profiles, dangerous-command approvals, the downgraded `codex_responses` review fork, subscription-token cost of aux tasks, per-profile `CODEX_HOME`, and the opt-in-beta limitations. |

**SP10 totals:** 8 notes · procedure 5 · model 3 · concept 0 (concepts owned by existing term notes / other SPs).
3 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 8 · procedure 5 · model 3 · concept 0 (dashboard/runtime concepts are existing terms or other-SP-owned).
- Source: 3 digested pages (~18.8K words) → ~12.4K words of notes (compression via heavy link-outs to feature pages).
- BB mix: procedure 62.5%, model 37.5%.
- New term notes owned: **0**; existing terms linked: see Per-Note Mapping; forward-ref `[own]` terms: SP06/SP09/SP14.

## Section Coverage Map

```
web-dashboard.md (9537w)
├── Quick Start (+Options table) ──────────────────────────── → Note 1
├── Managing multiple profiles ───────────────────────────── → Note 1 (profiles deep→SP04)
├── Prerequisites (web/pty extras) ───────────────────────── → Note 1
├── Pages › Status / Chat / Connecting Desktop (tour) ────── → Note 1 (Chat=TUI→SP02; Desktop deep→Note 3)
├── Pages › Config / API Keys / Sessions / Logs / Analytics → Note 1 (config→SP02; sessions→SP02)
├── Pages › Cron / Profiles / Skills / MCP / Webhooks ────── → Note 1 (cron→SP06; skills→SP05; mcp→SP09; webhooks→SP12)
├── Pages › Pairing / Channels / System ──────────────────── → Note 1 (pairing/channels→SP11-13; credential-pool→SP09; hooks→SP06)
├── /reload Slash Command ────────────────────────────────── → Note 1
├── Themes & plugins (summary at page tail) ──────────────── → Note 1 (full→Notes 4/5/6)
├── REST API (+profile-scoped note, all endpoint families) ─ → Note 2
├── Admin endpoints table ────────────────────────────────── → Note 2
├── CORS / Development / Automatic Build on Update ───────── → Note 2 (update→SP01)
├── Authentication (gated mode) (+all sub-sections) ──────── → Note 3 (OAuth/PKCE/portal→SP09/SP14)
└── Connecting Hermes Desktop to a remote backend (full) ─── → Note 3 (Desktop app→SP03 desktop)
extending-the-dashboard.md (5324w)
├── intro 3 layers / How the pieces compose ──────────────── → Note 4 (intro) + Note 5 (intro)
├── Table of contents ────────────────────────────────────── → (navigation aid; covered by Notes 4/5)
├── Themes › Quick start … Full theme YAML reference ─────── → Note 4 (CLI skins→SP08)
├── Plugins › Quick start … Plugin discovery & reload ───── → Note 5 (CLI/gateway plugins→SP06)
├── The Plugin SDK (surface enumeration) ─────────────────── → Note 6 (also referenced by Note 5)
├── Combined theme + plugin demo ─────────────────────────── → Note 5
├── API reference (Theme / Plugin / SDK-on-window) ───────── → Note 6
└── Troubleshooting ──────────────────────────────────────── → Note 5
codex-app-server-runtime.md (3959w)
├── intro / Why / What tools the model actually has (3 sources + NOT-available) → Note 7
├── Workflow features (/goal, Kanban, Cron) ──────────────── → Note 7 (kanban/goal→SP06)
├── Trade-offs table / Architecture diagram ──────────────── → Note 7
├── Hermes tool callback (the new MCP server) ────────────── → Note 7 (mcp→SP09; media tools→SP08)
├── Prerequisites / Enabling / Disabling ─────────────────── → Note 8
├── Self-improvement loop / How approvals work / Permission profiles → Note 8 (memory/skills→SP05)
├── Auxiliary tasks + ChatGPT token cost / Editing config.toml safely → Note 8 (aux config→SP02)
├── Multi-profile/multi-tenant / HOME passthrough ────────── → Note 8 (profiles→SP04)
├── MCP server migration / Native Codex plugin migration ── → Note 8 (mcp→SP09)
└── Limitations ──────────────────────────────────────────── → Note 8
```

No source H2/H3 orphaned. All 3 pages fully covered; feature-page detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| web-dashboard.md (9537w, 27 code, MIXED) | Note 1 (overview+pages, proc) + Note 2 (REST API, model) + Note 3 (auth+remote, proc) | >4000w → ≥3 notes; the feature tour (procedure), the HTTP surface (model), and the gated-auth setup (procedure) are three distinct BBs. |
| extending-the-dashboard.md (5324w, 32 code, MIXED) | Note 4 (themes, proc) + Note 5 (plugins, proc) + Note 6 (SDK + API reference, model) | >4000w → 3 notes; theming and plugin-authoring are two independent drop-in procedures, and the stable SDK/REST contract is a reference model (BB atomicity). |
| codex-app-server-runtime.md (3959w, 14 code, MIXED) | Note 7 (tool model + architecture, model) + Note 8 (enable/operate, proc) | 2500–4000w → 2 notes; the tool-availability/architecture is a model, enabling/approvals/migration/limitations is a procedure. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_web_dashboard_overview` | `term_mo_impact_dashboard`, `term_genai_adoption_dashboard` (BI dashboards); `cc_analytics_dashboards`, `cc_agent_view_monitor` (Claude Code admin) | **NOT a dup** — those are unrelated BI/metrics dashboards or a different product's admin UI; no `term_web_dashboard`/`term_dashboard`/`term_admin_panel` exists | CREATE; link `cc_analytics_dashboards`/`cc_agent_view_monitor` as analogous existing docs. |
| `hermes_dashboard_rest_api` | no `term_rest_api`/`term_api` note; `term_api_gateway` (active, different concept) | **NOT a dup** — REST surface has no term note; `term_api_gateway` is a component concept | CREATE; LINK `term_api_gateway`/`term_websocket`/`term_reverse_proxy`. |
| `hermes_dashboard_auth_remote` | `term_oauth`, `term_oauth_token`, `term_authentication` (active); no `term_oidc`/`term_pkce`/`term_oauth2` | **NOT a dup** — those are component concepts the note uses | CREATE; LINK `term_oauth`/`term_oauth_token`/`term_authentication`. (`term_pkce`→SP09 [own].) |
| `hermes_dashboard_themes` | `cc_terminal_themes` (Claude Code CLI skins); `term_design_system`/`term_theming` MISSING | **NOT a dup** — `cc_terminal_themes` is a *different product's CLI* skin system (the page itself says dashboard themes are unrelated to CLI skins) | CREATE; link `cc_terminal_themes` only as a contrast analogue. |
| `hermes_dashboard_plugins`, `hermes_dashboard_extension_api` | `term_plugin_sdk`, `term_plugin_manifest` (active); `cc_plugin_sources` | **NOT a dup** — `term_plugin_sdk`/`term_plugin_manifest` are component concepts; `hermes_plugin` (CLI/gateway) is owned by SP06 [own] | CREATE; LINK `term_plugin_sdk`/`term_plugin_manifest`/`term_react`. |
| `hermes_codex_runtime_tools`, `hermes_codex_runtime_setup` | `term_agentcore_runtime` (active, different runtime); no `term_codex`/`term_openai`/`term_chatgpt` | **NOT a dup** — `term_agentcore_runtime` is AWS Bedrock AgentCore (a different runtime concept); Codex runtime is product-integration, no term note exists | CREATE; LINK `term_agentcore_runtime` as a runtime-concept analogue, `term_sandbox`/`term_mcp`/`term_seatbelt`(MISSING→drop). |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the dashboard/runtime/theme hits are unrelated BI dashboards,
a different product's admin/CLI-skin docs, or component-concept terms confirmed by reading). New
`hermes_agent/` folder → no doc-doc collisions (SP01/SP02/etc. not yet executed; intra-series links
resolve at finalization). Adversarial dedup-verify pass: re-read `term_agentcore_runtime` and
`cc_terminal_themes` titles/scope to confirm they are different concepts — confirmed.

## Per-Note Related Notes Mapping (FINALIZED — FOUR FLOORS: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Cross-ref floor RAISED 2026-06-19 to the FOUR-FLOOR STANDARD (user directive — supersedes every prior
> floor):** each note's `## Related Notes` now carries FOUR COUNTED floors, all relevancy-selected to that
> note's actual content and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   the Hermes SOURCE-CODE repo notes whose modules IMPLEMENT what the doc note documents.
>   the 517-note Hermes implementation corpus; pick the ≥10 whose CODE this note documents (the code paths
>   the page describes). **This is now a COUNTED floor — promoted from the prior "bonus" group and raised
>   from the earlier ≥8 to ≥10.**
>   sibling `hermes_*` notes in THIS series (allowed to not-yet-exist; resolve at finalization per G5/G8) +
>   existing doc notes. **Docs floor RE-EXPANDED 2026-06-19** beyond the bare ≥10 to a comfortable margin so no
>   note sits on the floor: Note 1 now carries 13 docs and Notes 2–8 each carry 12 (minimum = 12). Every added
>
> The PRIOR floor (2026-06-19 first pass) was ≥8 term + ≥5 code-repo + ≥10 doc with snippets as a non-counted
> bonus; the floor BEFORE that was ≥8 term + ≥8 snippet + ≥5 doc. The snippet group is **NO LONGER a bonus** —
> it is a fully COUNTED fourth floor at ≥10. **Relevancy first, never pad.** All term IDs, all code-repo IDs,
> Intra-series `hermes_*` doc links resolve at finalization (G5/G8). Hermes-specific terms owned by other SPs
> are ADDITIONAL forward-refs `[own] (+fin …)`, EXCLUDED from the ≥8 term floor.

**Note 1 `hermes_web_dashboard_overview`** (procedure)
- Terms (8): term_autonomous_coding_agents, term_agent_harness, term_react, term_websocket, term_session_persistence, term_authentication, term_reverse_proxy, term_subagent — relevance: the dashboard is the agent-harness's React-SPA web admin surface fronting a FastAPI server (`hermes dashboard`); the Chat tab opens a `/api/pty` WebSocket to a spawned `hermes --tui`; the 16 admin pages read/write per-profile session history, the auth gate engages on non-loopback binds, and remote-backend wiring runs behind a reverse proxy. (+fin: term_nous_portal [own] SP14, term_hermes_profile [own] SP04, term_messaging_gateway [own] SP11)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `cli_web_*` FastAPI app, dashboard CLI flags, and the `/reload` slash command live here; relevance: this repo IS the `hermes dashboard` server the page documents. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the embedded TUI Chat pane (xterm.js over PTY/WebSocket) and gateway-status surface; relevance: the Chat tab renders the real TUI binary's ANSI output and the Status page mirrors gateway state. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the config/session/profile stores the Config, Sessions, Analytics, Profiles pages edit; relevance: every management page reads/writes core agent state. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level architecture tying the CLI, gateway, and dashboard extras (`web`/`pty`) together; relevance: the Prerequisites/extras section maps to this packaging. [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the theme/plugin extension surface the page's "Themes & plugins" tail summarizes; relevance: the dashboard's drop-in theming/plugin tabs come from this repo.
- Docs (13): hermes_dashboard_rest_api (sibling — the HTTP surface the SPA consumes; relevance: Note 1's pages call these endpoints), hermes_dashboard_auth_remote (sibling — the gated-mode + remote-backend deep dive; relevance: Note 1's Status/Desktop sections link here for the auth detail), hermes_dashboard_themes (sibling — theming the SPA; relevance: the "Themes & plugins" page tail), hermes_dashboard_plugins (sibling — plugin tabs; relevance: same page tail), hermes_session_search_storage (sibling SP02 — the session DB the Sessions/Chat pages browse; relevance: per-profile session history), hermes_configuring_models_dashboard (sibling SP02 — the Config page's model fields; relevance: the form-based `config.yaml` editor), hermes_features_overview (sibling SP01 — the feature catalog each page surfaces; relevance: the 16-page tour link-outs), hermes_cli_interface (sibling SP02 — the `hermes` CLI the dashboard mirrors; relevance: full-parity pages like Pairing/Channels), [cc_analytics_dashboards](../claude_code/cc_analytics_dashboards.md) — Claude Code's admin analytics surface; relevance: closest existing analogue to the Analytics page, [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — Claude Code's admin/monitoring panel; relevance: analogous live-status admin UI to the Status/System pages, [cc_desktop_overview_and_sessions](../claude_code/cc_desktop_overview_and_sessions.md) — Claude Code's desktop app + sessions; relevance: analogue to the Hermes Desktop remote-backend tie-in, [cc_web_overview](../claude_code/cc_web_overview.md) — Claude Code's browser-based admin/web surface; relevance: closest analogue to the whole `hermes dashboard` browser admin surface (SPA over a server) this note tours, [cc_remote_control](../claude_code/cc_remote_control.md) — Claude Code's remote-control surface; relevance: analogous remote-driven admin used by the Desktop-to-remote-backend tour-level section.
- Snippets (10): cli_web_app, cli_web_websocket, cli_web_config_schema, cli_web_reveal_oauth, gw_pairing, gw_session_lifecycle, gw_session_state, tui_server_render, tui_server_input, cli_hermescli_session_handlers, cli_hermescli_chat, core_hermes_state — relevance: the FastAPI dashboard app (`cli_web_app`), the `/api/pty` PTY/WS Chat pane (`cli_web_websocket`/`tui_server_render`/`tui_server_input`), the config-schema-driven Config form (`cli_web_config_schema`), the secret-reveal helper behind API Keys (`cli_web_reveal_oauth`), the Pairing page (`gw_pairing`), the per-profile session history the Sessions/Status pages read (`gw_session_lifecycle`/`gw_session_state`/`cli_hermescli_session_handlers`/`cli_hermescli_chat`), and the agent state schema the management pages mirror (`core_hermes_state`).

**Note 2 `hermes_dashboard_rest_api`** (model)
- Terms (8): term_api_gateway, term_websocket, term_rate_limiting, term_authentication, term_oauth_token, term_session_persistence, term_idempotency, term_reverse_proxy — relevance: the model is an HTTP API surface (REST endpoint families + the `/api/pty` and `/api/ws` WebSockets) behind the same auth gate, profile-scoped via `?profile=`, rate-limited on the login route, with idempotent `PUT /api/config`/`/api/env` writes, served localhost-only CORS and behind a reverse proxy when remote. (+fin: term_nous_portal [own] SP14)
- Code-Repos (5): [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the API-server route/middleware/connect code that defines these endpoints; relevance: this repo serves the REST + WS surface the model catalogs. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the dashboard `cli_web_*` app + `config/schema` endpoints + the Vite dev proxy / on-update rebuild; relevance: the `hermes dashboard` server mounts these routes. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the session/config/env stores the read/write endpoints touch; relevance: the sessions/config/analytics endpoint families read core state. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the cron CRUD behind `/api/cron/jobs*`; relevance: the cron endpoint family proxies this scheduler. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — the MCP-server registry behind the `/api/mcp/*` admin endpoints; relevance: the admin-endpoints table drives MCP add/test/enable.
- Docs (12): hermes_web_dashboard_overview (sibling — the pages that consume this API; relevance: each page maps to an endpoint family), hermes_dashboard_auth_remote (sibling — the gate the admin endpoints sit behind; relevance: all `/api/` is gated when remote), hermes_dashboard_extension_api (sibling — the theme/plugin REST endpoints `/api/dashboard/*`; relevance: extends the same HTTP surface), hermes_session_search_storage (sibling SP02 — the session store the `/api/sessions*` family reads; relevance: search/messages/stats/export/prune), hermes_api_server_endpoints (sibling SP12 — the standalone API server's endpoint surface; relevance: same FastAPI stack, different entrypoint), hermes_api_server_setup_auth (sibling SP12 — auth on the API server; relevance: shared auth-gate pattern), hermes_cron (sibling SP06 — the cron model behind `/api/cron`; relevance: the cron endpoint family), [cc_analytics_dashboards](../claude_code/cc_analytics_dashboards.md) — Claude Code's analytics surface; relevance: analogue to the `/api/analytics/usage` model, [cc_remote_control](../claude_code/cc_remote_control.md) — Claude Code's HTTP control surface; relevance: analogous REST-driven remote admin, [cc_web_session_management](../claude_code/cc_web_session_management.md) — Claude Code's web session API; relevance: analogous session REST endpoints, [cc_web_overview](../claude_code/cc_web_overview.md) — Claude Code's web/server architecture; relevance: analogous SPA-over-HTTP-API surface the REST families back, [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code's proxy/gateway config; relevance: analogue to the localhost-only CORS + reverse-proxy fronting this model documents.
- Snippets (10): gw_platform_api_server_routes, gw_platform_api_server_middleware, gw_platform_api_server_connect, cli_web_app, cli_web_config_schema, cli_web_websocket, core_hermes_state_schema, core_hermes_state_writes, cron_job_crud, gw_session_lifecycle — relevance: the API-server route/middleware/connect code that defines the REST + WS endpoint families (`gw_platform_api_server_*`), the dashboard app mounting them + the `config/schema` endpoint (`cli_web_app`/`cli_web_config_schema`), the `/api/pty`/`/api/ws` socket (`cli_web_websocket`), the session-store schema + write path behind `/api/sessions*` (`core_hermes_state_schema`/`core_hermes_state_writes`/`gw_session_lifecycle`), and the cron CRUD behind `/api/cron/jobs*` (`cron_job_crud`).

**Note 3 `hermes_dashboard_auth_remote`** (procedure)
- Terms (8): term_oauth, term_oauth_token, term_authentication, term_reverse_proxy, term_websocket, term_session_persistence, term_idempotency, term_api_gateway — relevance: gated mode is an OAuth/OIDC/username-password auth procedure that fails closed on a non-loopback bind, mints HMAC/JWT session tokens with a TTL, sets HttpOnly cookies, derives its OAuth callback behind a reverse proxy via `public_url`/`X-Forwarded-*`, and gates the `/api/ws` + `/api/pty` chat sockets the Desktop reuses. (+fin: term_pkce [own] SP09, term_nous_portal [own] SP14)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `cli_auth_*` OAuth-callback server, provider state/resolution, token storage, login/logout, and `dashboard register`; relevance: the three bundled `DashboardAuthProvider`s and the gate live here. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the API-server auth middleware + peer-IP/Host (DNS-rebind) guards on `/api/ws`; relevance: the socket-layer checks the Desktop section debugs (4401/4403). [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the `plugins/dashboard_auth/{nous,basic,self_hosted}` provider plugins + custom-provider extension point; relevance: providers ship as auto-loaded plugins. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the Nous Portal OAuth contract v1 / OIDC verification adapter; relevance: token exchange + JWKS verification. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `config.yaml`/`.env` precedence the `dashboard.*` auth settings read from; relevance: env-wins-over-config resolution for client_id/secret/credentials.
- Docs (12): hermes_web_dashboard_overview (sibling — the surface being secured; relevance: when the gate engages), hermes_dashboard_rest_api (sibling — the gated `/api/` surface; relevance: every admin endpoint sits behind this gate), hermes_security_command_approval (sibling SP06 — the dangerous-command/consent model; relevance: the dashboard's shell-hook consent + write-to-`.env` risk), hermes_security_isolation_credentials (sibling SP03b — credential isolation; relevance: the `.env` secrets the gate protects), hermes_config_files_precedence (sibling SP02 — env-over-config precedence; relevance: every `dashboard.*` auth knob follows it), hermes_oauth_over_ssh (sibling SP09 — Hermes' OAuth flow over remote links; relevance: analogous remote auth path), hermes_setup_with_nous_portal (sibling SP14 — Nous Portal OAuth wiring; relevance: the Nous provider's `register` flow), [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — Claude Code's admin/enterprise enforcement; relevance: analogous gate-on-non-local-access policy, [cc_authentication](../claude_code/cc_authentication.md) — Claude Code's auth model; relevance: analogous OAuth/credential login, [cc_remote_vs_web_and_deep_links](../claude_code/cc_remote_vs_web_and_deep_links.md) — Claude Code remote/web access + deep links; relevance: analogue to the Hermes Desktop remote-backend connection, [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — Claude Code's network/TLS/access policy; relevance: analogue to the non-loopback bind + `public_url`/`X-Forwarded-*` reverse-proxy access the gate enforces, [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — Claude Code's login/auth troubleshooting; relevance: analogue to the gate's 4401/4403 + remote-connect troubleshooting recipes this procedure debugs.
- Snippets (10): cli_auth_oauth_callback_server, cli_auth_provider_state, cli_auth_resolve_provider, cli_auth_storage, cli_web_reveal_oauth, cli_auth_login_logout, cli_doctor_api_connectivity, cli_doctor_auth_dirs, gw_platform_api_server_middleware, gw_platform_api_server_connect — relevance: the OAuth-callback server the gate uses (`cli_auth_oauth_callback_server`), provider state/resolution for the three bundled providers (`cli_auth_provider_state`/`cli_auth_resolve_provider`), token storage + login/logout cookies (`cli_auth_storage`/`cli_auth_login_logout`), the `.env` secret reveal the gate protects (`cli_web_reveal_oauth`), the connectivity + auth-dir doctor used to debug remote connects (`cli_doctor_api_connectivity`/`cli_doctor_auth_dirs`), and the API-server auth middleware + peer-IP/Host guards on `/api/ws` (`gw_platform_api_server_middleware`/`gw_platform_api_server_connect`).

**Note 4 `hermes_dashboard_themes`** (procedure)
- Terms (8): term_react, term_plugin_sdk, term_plugin_manifest, term_persona, term_autonomous_coding_agents, term_agent_harness, term_caching, term_idempotency — relevance: a drop-in YAML theme repaints the React design-system token cascade (3-layer palette → shadcn tokens via `color-mix()`), typography/layout/`layoutVariant`, `componentStyles`, `colorOverrides`, and 32-KiB-capped `customCSS`; lives alongside plugins under the SDK/manifest extension surface; the live switcher persists theme/font choices idempotently to `config.yaml` (`dashboard.theme`/`dashboard.font`).
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the theme loader, `~/.hermes/dashboard-themes/` discovery, palette/token cascade, and `/api/dashboard/theme[s]` endpoints; relevance: this repo IS the theming engine the page documents. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `cli_web_app` dashboard server that serves the theme CSS vars + the `config_set`/`config_schema` persistence; relevance: theme selection writes through here. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `config.yaml` store the theme/font choice persists to; relevance: `dashboard.theme`/`dashboard.font` are config fields. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the CLI skin engine (skins) the page explicitly contrasts with dashboard themes; relevance: "the CLI skin system is unrelated to dashboard themes". [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level packaging tying the dashboard front-end build to the install; relevance: themes ship with the built SPA.
- Docs (12): hermes_dashboard_plugins (sibling — the co-located plugin system; relevance: a combined theme+plugin demo), hermes_dashboard_extension_api (sibling — the stable theme/plugin REST + SDK contract; relevance: theme endpoints + CSS vars), hermes_web_dashboard_overview (sibling — the dashboard the theme reskins; relevance: live switcher in the header), hermes_skins (sibling SP08 — the CLI skin system; relevance: the explicit contrast analogue inside Hermes), hermes_features_overview (sibling SP01 — the feature catalog; relevance: theming is a listed dashboard feature), [cc_terminal_themes](../claude_code/cc_terminal_themes.md) — Claude Code's CLI skin/theme system; relevance: contrast analogue (different product's terminal skin, not a web theme), [cc_output_styles](../claude_code/cc_output_styles.md) — Claude Code's output-style customization; relevance: analogous user-driven appearance config, [cc_statusline_setup](../claude_code/cc_statusline_setup.md) — Claude Code statusline theming; relevance: analogous CSS-var-style chrome customization, [cc_fullscreen_rendering](../claude_code/cc_fullscreen_rendering.md) — Claude Code's rendering layer; relevance: analogous render/layout-variant concept, [cc_settings_files](../claude_code/cc_settings_files.md) — Claude Code's settings persistence; relevance: analogue to persisting the theme choice in `config.yaml`, [cc_settings_scopes_and_precedence](../claude_code/cc_settings_scopes_and_precedence.md) — Claude Code's settings scope/precedence; relevance: analogue to the `dashboard.theme`/`dashboard.font` config-vs-live-switcher precedence the theme persists through, [cc_terminal_configuration](../claude_code/cc_terminal_configuration.md) — Claude Code's terminal appearance config; relevance: analogous appearance/typography/font configuration surface (contrast to the web design-system cascade).
- Snippets (10): plugins_web, plugins_example_dashboard, cli_web_app, cli_web_config_schema, cli_config_set, cli_config_schema, cli_config_load, cli_skin_engine, cli_skin_apply, plugins_namespace_init — relevance: the dashboard web-plugin/theme surface (`plugins_web`) and the example combined theme+plugin demo (`plugins_example_dashboard`); the dashboard app + config-schema endpoint that serves theme CSS vars (`cli_web_app`/`cli_web_config_schema`); the `dashboard.theme`/`dashboard.font` config persistence path (`cli_config_set`/`cli_config_schema`/`cli_config_load`); the CONTRAST CLI skin engine/apply the page says is unrelated to dashboard themes (`cli_skin_engine`/`cli_skin_apply`); and the plugin/theme namespace init (`plugins_namespace_init`).

**Note 5 `hermes_dashboard_plugins`** (procedure)
- Terms (8): term_plugin_sdk, term_plugin_manifest, term_react, term_websocket, term_api_gateway, term_authentication, term_idempotency, term_autonomous_coding_agents — relevance: a dashboard plugin is a `manifest.json` + IIFE JS bundle using `window.__HERMES_PLUGIN_SDK__` (no bundled React), registering a tab / shell slots / page-scoped slots / `tab.override`/`tab.hidden`, optionally exposing FastAPI routes under `/api/plugins/<name>/` that (by default, localhost) bypass the same auth gate the rest of `/api/` sits behind; 3-dir discovery + rescan is idempotent. (+fin: term_hermes_plugin [own] SP06)
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the plugin registry, SDK-on-`window` exposure, slot system, discovery/rescan, and `/api/dashboard/plugins*` endpoints; relevance: this repo IS the dashboard plugin host the page documents. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `cli_web_app` dashboard server that injects the SDK, loads bundles, and mounts plugin backend routers; relevance: `App.tsx`/`main.tsx` load lifecycle. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the FastAPI server the plugin `router` mounts into; relevance: `/api/plugins/<name>/` routes run inside the dashboard process. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `SessionDB`/`load_config` internals backend plugin routes import directly; relevance: the "Accessing Hermes internals" recipe. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level package the `~/.hermes/plugins/<name>/dashboard/` layout extends without a fork; relevance: drop-in-at-runtime install.
- Docs (12): hermes_dashboard_themes (sibling — the co-located theming layer; relevance: combined theme+plugin demo), hermes_dashboard_extension_api (sibling — the stable SDK + REST contract; relevance: `register`/`registerSlot` globals + endpoints), hermes_web_dashboard_overview (sibling — the dashboard a plugin extends; relevance: tabs appear in its nav), hermes_dashboard_rest_api (sibling — the HTTP surface plugin routes extend; relevance: `SDK.fetchJSON`/`SDK.api` reach it), hermes_plugins_system (sibling SP06 — the CLI/gateway plugin system sharing the directory; relevance: one plugin dir extends CLI + dashboard), hermes_build_plugin_tutorial (sibling SP17 — the plugin-authoring guide; relevance: end-to-end authoring walkthrough), [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — Claude Code's plugin source model; relevance: analogous plugin discovery/sources, [cc_plugin_components](../claude_code/cc_plugin_components.md) — Claude Code plugin component types; relevance: analogue to tab/slot/api plugin parts, [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — Claude Code's plugin manifest schema; relevance: analogous `manifest.json` field reference, [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — Claude Code's extension overview; relevance: analogue to "Extending the Dashboard", [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code's plugin-system overview; relevance: analogue to the whole drop-in dashboard-plugin model (manifest + bundle + discovery) this note authors, [cc_plugin_directory_structure](../claude_code/cc_plugin_directory_structure.md) — Claude Code's plugin directory layout; relevance: analogue to the `~/.hermes/plugins/<name>/dashboard/` 3-dir layout + discovery this note describes.
- Snippets (10): plugins_example_dashboard, plugins_web, plugins_sdk_architecture, plugins_manifest_schema, plugins_interfaces_abcs, plugins_namespace_init, cli_plugins_discover, cli_plugins_cmd_list_info, cli_web_app, gw_platform_api_server_routes — relevance: the example dashboard plugin (`plugins_example_dashboard`), the web-plugin surface + SDK-on-`window` (`plugins_web`/`plugins_sdk_architecture`), the `manifest.json` schema + plugin ABCs/namespace (`plugins_manifest_schema`/`plugins_interfaces_abcs`/`plugins_namespace_init`), the 3-dir discovery + rescan + list/info (`cli_plugins_discover`/`cli_plugins_cmd_list_info`), the dashboard app that injects the SDK and mounts plugin backend routers (`cli_web_app`), and the FastAPI route layer the `/api/plugins/<name>/` routes mount into (`gw_platform_api_server_routes`).

**Note 6 `hermes_dashboard_extension_api`** (model)
- Terms (8): term_plugin_sdk, term_plugin_manifest, term_react, term_api_gateway, term_websocket, term_idempotency, term_authentication, term_reverse_proxy — relevance: the stable contract is the `window.__HERMES_PLUGIN_SDK__` surface (React/hooks/components/api/fetchJSON/utils/useI18n), the `window.__HERMES_PLUGINS__.register`/`registerSlot` globals, and the theme/plugin REST endpoints (`/api/dashboard/themes`, `/theme`, `/plugins`, `/plugins/rescan`, static asset serving) served by the gated API. (+fin: term_hermes_plugin [own] SP06)
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — `registry.ts` defines the SDK surface + the `register`/`registerSlot` globals + the theme/plugin endpoints; relevance: this repo IS the contract the model formalizes. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `cli_web_app` server + `plugins cmd list/info` that serve `/api/dashboard/*` and the static `/dashboard-plugins/<name>/<path>`; relevance: where the endpoints live. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — the FastAPI route/middleware layer behind the dashboard endpoints; relevance: the gated HTTP plumbing. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the config/theme persistence the PUT endpoints write; relevance: `dashboard.theme` round-trip. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the shadcn/ui component set + React instance the SDK re-exports; relevance: `SDK.components`/`SDK.React` provenance.
- Docs (12): hermes_dashboard_plugins (sibling — the consumer of this contract; relevance: plugins call the SDK + endpoints), hermes_dashboard_themes (sibling — the theme half of the contract; relevance: theme endpoints + CSS vars), hermes_dashboard_rest_api (sibling — the broader HTTP surface this extends; relevance: `/api/dashboard/*` is part of the same server), hermes_web_dashboard_overview (sibling — the host SPA; relevance: the SDK is exposed by `main.tsx`), hermes_plugins_system (sibling SP06 — the CLI/gateway plugin contract; relevance: parallel plugin-ABC contract), hermes_build_plugin_tutorial (sibling SP17 — using the contract; relevance: authoring against the SDK), [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — Claude Code plugin sources; relevance: analogous plugin registration model, [cc_plugin_components](../claude_code/cc_plugin_components.md) — Claude Code plugin component contract; relevance: analogue to the SDK component surface, [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — Claude Code manifest schema; relevance: analogous stable manifest contract, [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — Claude Code extension API overview; relevance: analogous extension-contract reference, [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code's plugin-system overview; relevance: analogue to the stable plugin/SDK extension surface this model formalizes, [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — Claude Code's managed plugin policy/registration settings; relevance: analogue to the `register`/`registerSlot` globals + gated `/api/dashboard/plugins[/rescan]` endpoints governing what loads.
- Snippets (10): plugins_sdk_architecture, plugins_manifest_schema, plugins_interfaces_abcs, plugins_web, plugins_example_dashboard, plugins_namespace_init, cli_plugins_cmd_list_info, cli_plugins_discover, gw_platform_api_server_routes, cli_web_app — relevance: the `window.__HERMES_PLUGIN_SDK__` surface + `register`/`registerSlot` globals (`plugins_sdk_architecture`), the stable `manifest.json` schema (`plugins_manifest_schema`), the plugin ABCs/namespace defining the contract (`plugins_interfaces_abcs`/`plugins_namespace_init`), the web-plugin + example-dashboard consumers (`plugins_web`/`plugins_example_dashboard`), the `plugins list/info` + discovery that serve `/api/dashboard/plugins[/rescan]` (`cli_plugins_cmd_list_info`/`cli_plugins_discover`), and the FastAPI route + dashboard app where `/api/dashboard/*` and the static `/dashboard-plugins/<name>/<path>` are served (`gw_platform_api_server_routes`/`cli_web_app`).

**Note 7 `hermes_codex_runtime_tools`** (model)
- Terms (8): term_mcp, term_sandbox, term_subagent, term_kanban, term_agentcore_runtime, term_autonomous_coding_agents, term_multi_agent_systems, term_agent_orchestration — relevance: the model routes `openai/*` turns to Codex's seatbelt/landlock-sandboxed tool loop over JSON-RPC-over-stdio; three independent tool sources (Codex built-ins; auto-migrated native plugins; the `hermes-tools` MCP callback); the four unavailable tools are agent-loop (delegate_task/subagent, memory, session_search, todo) ones; kanban/goal multi-agent workflows still run via the MCP callback. (+fin: term_code_execution_tool [own] SP06, term_delegate_task [own] SP06, term_kanban_multi_agent [own] SP06)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the `core_codex_runtime` / `CodexAppServerSession` + the `openai-codex` provider plugin; relevance: this repo IS the runtime the model diagrams (JSON-RPC client, item/* projection). [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent.run_conversation` api-mode resolution that forks to `CodexAppServerSession`; relevance: the architecture's branch point. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — the `hermes_tools_mcp_server` + `model_tools.handle_function_call()` dispatch; relevance: the MCP callback exposing web/browser/vision/image/skills/TTS. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the Hermes tool implementations re-exposed via the callback and the four agent-loop tools that are NOT available; relevance: the tool-availability matrix. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the kanban dispatcher + `/goal` Ralph-loop continuation the runtime hosts; relevance: workflow-feature compatibility (worker handoff tools via callback).
- Docs (12): hermes_codex_runtime_setup (sibling — enabling/operating the same runtime; relevance: the procedure companion to this model), hermes_mcp (sibling SP09 — the MCP protocol the callback speaks; relevance: `hermes-tools` is an MCP server), hermes_kanban_multi_agent_board (sibling SP06 — the kanban worker/orchestrator tools; relevance: which run via the callback on this runtime), hermes_subagent_delegation (sibling SP06 — delegate_task subagents; relevance: the agent-loop tool that is unavailable here), hermes_code_execution (sibling SP08 — the code-exec/sandbox tool concept; relevance: Codex's `shell`/`apply_patch` sandboxed exec), hermes_persistent_goals (sibling SP06 — the `/goal` Ralph loop; relevance: works on this runtime via run_conversation), hermes_tools_reference_core (sibling SP08 — the core tool catalog; relevance: the tools the callback re-exposes), [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — Claude Code's sandbox profiles; relevance: analogue to Codex's `:read-only`/`:workspace`/`:danger-no-sandbox`, [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — Claude Code's built-in toolset; relevance: analogue to Codex's shell/apply_patch/update_plan/view_image, [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — Claude Code's MCP model; relevance: analogous MCP-server tool callback, [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — Claude Code's full tool catalog; relevance: analogue to the tool-availability matrix (three sources + the four agent-loop tools NOT available) this model tabulates, [cc_goal_command](../claude_code/cc_goal_command.md) — Claude Code's goal command; relevance: analogue to the `/goal` Ralph-loop workflow feature still hosted on this runtime via the MCP callback.
- Snippets (10): core_codex_runtime, core_agent_init_api_mode_resolution, core_agent_init_runtime_state, mcp_serve_hermes_as_server, mcp_serve_tool_surface, model_tools_introspection, plugins_provider_codex, tools_code_exec_sandbox, tools_delegate_spawn, tools_memory — relevance: the `CodexAppServerSession` runtime + JSON-RPC/item projection (`core_codex_runtime`), the `AIAgent.run_conversation` api-mode/runtime-state branch point (`core_agent_init_api_mode_resolution`/`core_agent_init_runtime_state`), the `hermes-tools` MCP callback server + the web/browser/vision/image/skills/TTS tool surface it re-exposes (`mcp_serve_hermes_as_server`/`mcp_serve_tool_surface`/`model_tools_introspection`), the `openai-codex` provider plugin (`plugins_provider_codex`), Codex's `shell`/`apply_patch` sandboxed exec analogue (`tools_code_exec_sandbox`), and the two agent-loop tools the matrix marks UNAVAILABLE on this runtime (`tools_delegate_spawn`=delegate_task subagents, `tools_memory`=persistent memory).

**Note 8 `hermes_codex_runtime_setup`** (procedure)
- Terms (8): term_mcp, term_sandbox, term_oauth_token, term_authentication, term_idempotency, term_progressive_summarization, term_skill_manifest, term_subagent — relevance: `/codex-runtime codex_app_server` idempotently migrates MCP servers + native plugins into the `# managed by hermes-agent` block of `~/.codex/config.toml`, uses ChatGPT/`codex login` OAuth tokens, sets `default_permissions = ":workspace"` sandboxing, projects events so memory/skill (skill_manage) nudges fire, and aux compression + the downgraded `codex_responses` review fork (which needs agent-loop tools) tie in. (+fin: term_code_execution_tool [own] SP06, term_hermes_profile [own] SP04)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `/codex-runtime` slash command (`cli_codex_switch`) + `codex-runtime migrate` (`cli_codex_migrate`) + `config_set` persistence; relevance: this is the enable/disable + migration entrypoint. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — `core_codex_runtime`, the runtime client-switch/recovery helpers, and the `codex_responses` adapter the review fork downgrades to; relevance: the runtime lifecycle the procedure drives. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — the `hermes-tools` MCP server registered in `config.toml` + the `mcp_servers`→TOML translation; relevance: the MCP-migration table. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `_current_main_runtime()`, the self-improvement counters, `CODEX_HOME`/`HOME` env passthrough (`os.environ.copy()`), and per-profile state; relevance: multi-profile isolation + the review-fork downgrade. [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the skill-nudge/`skill_manage` path the projected items trigger; relevance: skill review keeps working on the runtime.
- Docs (12): hermes_codex_runtime_tools (sibling — the tool/architecture model companion; relevance: what the enabled runtime can do), hermes_mcp (sibling SP09 — MCP config + the migration target; relevance: `mcp_servers`→codex `config.toml`), hermes_mcp_config_reference (sibling SP09 — the MCP config schema migrated; relevance: command/args/url/timeout translation table), hermes_model_aux_provider_config (sibling SP14/02 — the `auxiliary.*` overrides; relevance: routing aux tasks off the subscription), hermes_config_files_precedence (sibling SP02 — env-over-config + managed-block precedence; relevance: editing `config.toml`/`config.yaml` safely), hermes_security_command_approval (sibling SP06 — the Dangerous-Command approval prompt; relevance: Codex exec/apply_patch approvals route through it), hermes_security_skill_memory_settings (sibling SP05 — memory/skill nudge settings; relevance: counters that keep firing on this runtime), hermes_profiles_multi_agent (sibling SP04 — per-profile isolation; relevance: per-profile `CODEX_HOME`), [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — Claude Code sandbox modes; relevance: analogue to Codex's three permission profiles, [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — Claude Code's tool-approval handling; relevance: analogous dangerous-command approval flow, [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — Claude Code's permission-modes overview; relevance: analogue to enabling/selecting Codex's `:read-only`/`:workspace`/`:danger-no-sandbox` `default_permissions` this procedure sets, [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — Claude Code's managed MCP configuration; relevance: analogue to the `mcp_servers`→`~/.codex/config.toml` managed-block MCP-server migration this procedure regenerates.
- Snippets (10): cli_codex_switch, cli_codex_migrate, core_codex_runtime, core_runtime_helpers_switch_client, core_runtime_helpers_recovery, core_codex_responses_adapter_init, core_auxiliary_codex_adapter, cli_config_set, mcp_serve_hermes_as_server, tools_skill_manager — relevance: the `/codex-runtime` switch + `codex-runtime migrate` (`cli_codex_switch`/`cli_codex_migrate`), the runtime session + client-switch/recovery lifecycle the procedure drives (`core_codex_runtime`/`core_runtime_helpers_switch_client`/`core_runtime_helpers_recovery`), the downgraded `codex_responses` review-fork adapter (`core_codex_responses_adapter_init`) and the aux-task codex adapter for ChatGPT-subscription routing (`core_auxiliary_codex_adapter`), the `config_set` persistence of `model.openai_runtime` (`cli_config_set`), the `hermes-tools` MCP callback registered in `config.toml` (`mcp_serve_hermes_as_server`), and the `skill_manage` nudge path projected items keep firing (`tools_skill_manager`).

> **Note-4 term floor fix (finalization):** two earlier candidate slugs (`term_user_interface`,
> `term_design_system`) were caught as NON-EXISTENT at finalization (DB scan 2026-06-15) and replaced inline
> already clean.


- Note 1 Terms (8): term_autonomous_coding_agents, term_agent_harness, term_react, term_websocket, term_session_persistence, term_authentication, term_reverse_proxy, term_subagent
- Note 2 Terms (8): term_api_gateway, term_websocket, term_rate_limiting, term_authentication, term_oauth_token, term_session_persistence, term_idempotency, term_reverse_proxy
- Note 3 Terms (8): term_oauth, term_oauth_token, term_authentication, term_reverse_proxy, term_websocket, term_session_persistence, term_idempotency, term_api_gateway
- Note 4 Terms (8): term_react, term_plugin_sdk, term_plugin_manifest, term_persona, term_autonomous_coding_agents, term_agent_harness, term_caching, term_idempotency
- Note 5 Terms (8): term_plugin_sdk, term_plugin_manifest, term_react, term_websocket, term_api_gateway, term_authentication, term_idempotency, term_autonomous_coding_agents
- Note 6 Terms (8): term_plugin_sdk, term_plugin_manifest, term_react, term_api_gateway, term_websocket, term_idempotency, term_authentication, term_reverse_proxy
- Note 7 Terms (8): term_mcp, term_sandbox, term_subagent, term_kanban, term_agentcore_runtime, term_autonomous_coding_agents, term_multi_agent_systems, term_agent_orchestration
- Note 8 Terms (8): term_mcp, term_sandbox, term_oauth_token, term_authentication, term_idempotency, term_progressive_summarization, term_skill_manifest, term_subagent


- Note 1 Code-Repos (5): repo_hermes_agent_cli, repo_hermes_agent_tui_gateway, repo_hermes_agent_agent_core, repo_hermes_agent, repo_hermes_agent_plugins
- Note 2 Code-Repos (5): repo_hermes_agent_tui_gateway, repo_hermes_agent_cli, repo_hermes_agent_agent_core, repo_hermes_agent_cron, repo_hermes_agent_mcp_toolsets
- Note 3 Code-Repos (5): repo_hermes_agent_cli, repo_hermes_agent_tui_gateway, repo_hermes_agent_plugins, repo_hermes_agent_providers_adapters, repo_hermes_agent_agent_core
- Note 4 Code-Repos (5): repo_hermes_agent_plugins, repo_hermes_agent_cli, repo_hermes_agent_agent_core, repo_hermes_agent_tui_gateway, repo_hermes_agent
- Note 5 Code-Repos (5): repo_hermes_agent_plugins, repo_hermes_agent_cli, repo_hermes_agent_tui_gateway, repo_hermes_agent_agent_core, repo_hermes_agent
- Note 6 Code-Repos (5): repo_hermes_agent_plugins, repo_hermes_agent_cli, repo_hermes_agent_tui_gateway, repo_hermes_agent_agent_core, repo_hermes_agent
- Note 7 Code-Repos (5): repo_hermes_agent_providers_adapters, repo_hermes_agent_agent_core, repo_hermes_agent_mcp_toolsets, repo_hermes_agent_tools, repo_hermes_agent_cron
- Note 8 Code-Repos (5): repo_hermes_agent_cli, repo_hermes_agent_providers_adapters, repo_hermes_agent_mcp_toolsets, repo_hermes_agent_agent_core, repo_hermes_agent_skills


- Note 1 Snippets (10): cli_web_app, cli_web_websocket, cli_web_config_schema, cli_web_reveal_oauth, gw_pairing, gw_session_lifecycle, gw_session_state, tui_server_render, tui_server_input, cli_hermescli_session_handlers, cli_hermescli_chat, core_hermes_state
- Note 2 Snippets (10): gw_platform_api_server_routes, gw_platform_api_server_middleware, gw_platform_api_server_connect, cli_web_app, cli_web_config_schema, cli_web_websocket, core_hermes_state_schema, core_hermes_state_writes, cron_job_crud, gw_session_lifecycle
- Note 3 Snippets (10): cli_auth_oauth_callback_server, cli_auth_provider_state, cli_auth_resolve_provider, cli_auth_storage, cli_web_reveal_oauth, cli_auth_login_logout, cli_doctor_api_connectivity, cli_doctor_auth_dirs, gw_platform_api_server_middleware, gw_platform_api_server_connect
- Note 4 Snippets (10): plugins_web, plugins_example_dashboard, cli_web_app, cli_web_config_schema, cli_config_set, cli_config_schema, cli_config_load, cli_skin_engine, cli_skin_apply, plugins_namespace_init
- Note 5 Snippets (10): plugins_example_dashboard, plugins_web, plugins_sdk_architecture, plugins_manifest_schema, plugins_interfaces_abcs, plugins_namespace_init, cli_plugins_discover, cli_plugins_cmd_list_info, cli_web_app, gw_platform_api_server_routes
- Note 6 Snippets (10): plugins_sdk_architecture, plugins_manifest_schema, plugins_interfaces_abcs, plugins_web, plugins_example_dashboard, plugins_namespace_init, cli_plugins_cmd_list_info, cli_plugins_discover, gw_platform_api_server_routes, cli_web_app
- Note 7 Snippets (10): core_codex_runtime, core_agent_init_api_mode_resolution, core_agent_init_runtime_state, mcp_serve_hermes_as_server, mcp_serve_tool_surface, model_tools_introspection, plugins_provider_codex, tools_code_exec_sandbox, tools_delegate_spawn, tools_memory
- Note 8 Snippets (10): cli_codex_switch, cli_codex_migrate, core_codex_runtime, core_runtime_helpers_switch_client, core_runtime_helpers_recovery, core_codex_responses_adapter_init, core_auxiliary_codex_adapter, cli_config_set, mcp_serve_hermes_as_server, tools_skill_manager

All 8 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (FOUR-FLOOR standard) — Docs floor RE-EXPANDED
2026-06-19 to a comfortable margin (Note 1 = 13 docs; Notes 2–8 = 12 docs each; minimum across all notes = 12, ≥10 met).
`resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by G5/G8). All 34 distinct
`cc_*` doc links cited (`cc_analytics_dashboards`, `cc_agent_view_monitor`, `cc_desktop_overview_and_sessions`,
`cc_web_overview`, `cc_remote_control`, `cc_web_session_management`, `cc_proxy_and_gateway_config`,
`cc_admin_enforcement_controls`, `cc_authentication`, `cc_remote_vs_web_and_deep_links`, `cc_network_tls_and_access`,
`cc_login_authentication_troubleshooting`, `cc_terminal_themes`, `cc_output_styles`, `cc_statusline_setup`,
`cc_fullscreen_rendering`, `cc_settings_files`, `cc_settings_scopes_and_precedence`, `cc_terminal_configuration`,
`cc_plugin_sources`, `cc_plugin_components`, `cc_plugin_manifest_schema`, `cc_extending_claude_code`,
`cc_plugins_overview`, `cc_plugin_directory_structure`, `cc_managed_plugin_policy_settings`, `cc_sandbox_modes`,
`cc_built_in_tools`, `cc_mcp_overview`, `cc_tools_catalog`, `cc_goal_command`, `cc_sdk_tool_approval_handling`,

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 3 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 web-dashboard-overview | procedure | 1700 | ≤6 (curate from quickstart/profile/extras blocks; 16 page tour in prose tables) | ✓ |
| 2 dashboard-rest-api | model | 1500 | ≤6 (endpoint families as tables; ≤6 canonical request/response blocks) | ✓ |
| 3 dashboard-auth-remote | procedure | 1700 | ≤6 (curate from systemd/.env/curl/keycloak blocks; one canonical per provider) | ✓ |
| 4 dashboard-themes | procedure | 1400 | ≤6 (one canonical theme YAML + palette/typography snippets; rest in prose tables) | ✓ |
| 5 dashboard-plugins | procedure | 1700 | ≤6 (manifest + IIFE + slot + FastAPI canonical blocks; rest summarized) | ✓ |
| 6 dashboard-extension-api | model | 700 | ≤6 (SDK surface + endpoint tables) | ✓ |
| 7 codex-runtime-tools | model | 1700 | ≤6 (architecture ASCII + trade-offs table; ≤6 config/toml blocks) | ✓ |
| 8 codex-runtime-setup | procedure | 1700 | ≤6 (curate from enable/migrate/config.toml/aux blocks) | ✓ |

No further splits needed — all 8 notes are ≤2500w. The code-heavy pages (web-dashboard 27, extending 32,
codex 14 source blocks) are curated to ≤6 load-bearing blocks per note (kept verbatim), with the rest
summarized in prose tables. Borderline notes (1/3/5/7/8 at ~1700w) checked for further split: each is one
topically-cohesive BB cluster with no BB mixing → KEEP (review CP6 default-to-keep justification). If any
note exceeds 350 lines during writing, STOP and split. The ASCII architecture diagram in Note 7 is kept
verbatim but uses safe characters (per Mermaid/Obsidian guidance it is a fenced code block, not Mermaid).

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_analytics_dashboards.md`): YAML field order `tags → keywords → topics → language → date of note →
status → building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading
with what it IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **FOUR FLOORS: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**
— floor raised 2026-06-19) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP10)

**SP10 owns 0 new term captures.** Per the master's corpus-wide ownership sweep and the SP10 scope
directive ("owned captures only if a genuinely new reusable concept survives a collision audit; otherwise 0
captures and link existing"), every Hermes-specific concept SP10 touches is either an existing verified term,
a generic concept already covered, or owned by another sub-plan (link at finalization). The collision +
specificity audit on the one borderline owned candidate (`term_web_dashboard`) rejected it: it is a
product-specific feature surface, not a cross-domain reusable concept. Augment re-read surfaced **0 new**
undigested terms that SP10 should own.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_web_dashboard` (candidate) | **NOT captured** (specificity audit) | — | Product-specific feature surface, not a reusable cross-domain concept; doc note `hermes_web_dashboard_overview` covers it. No `term_dashboard`/`term_admin_panel` to collide with. |
| `term_codex_app_server_runtime` (candidate) | **NOT captured** (specificity audit) | — | Product-integration (Codex CLI ↔ Hermes); doc notes 7/8 cover it; `term_agentcore_runtime` is the linkable runtime-concept analogue. |
| `term_pkce` | LINK only (forward-ref, +fin `[own]`) | SP09 | OAuth 2.1 PKCE flow; SP10's auth note uses it, concept home is SP09 protocols. |
| `term_hermes_plugin` | LINK only (+fin `[own]`) | SP06 | CLI/gateway plugin system; the dashboard plugin shares the directory, concept home is SP06. |
| `term_code_execution_tool`, `term_delegate_task`, `term_kanban_multi_agent` | LINK only (+fin `[own]`) | SP06 | Codex runtime hosts these workflows; concept homes are SP06 automation/multi-agent. |
| `term_nous_portal`, `term_tool_gateway` | LINK only (+fin `[own]`) | SP14 / SP05 | Portal OAuth + billing referenced in dashboard/runtime tips; captured by owners. |
| `term_messaging_gateway`, `term_hermes_profile` | LINK only (+fin `[own]`) | SP11 / SP04 | Channels/pairing pages + profile switcher; concept homes are SP11/SP04. |

### Renamed (general → specific)

— (audit performed; SP10 owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the two owned candidates above — both REJECTED as product-specific, not renamed — and to the
master's forward-ref slugs SP10 links; all forward-refs are already scope-qualified by their owners.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_web_dashboard` / dashboard concept | none substantive (`term_mo_impact_dashboard`/`term_genai_adoption_dashboard` are unrelated BI dashboards) | No removal — SP10 owns 0; doc note `hermes_web_dashboard_overview` created instead. |
| `term_dashboard_theme` (would be too general) | none; `cc_terminal_themes` is a different product's CLI skin | Not captured — doc note `hermes_dashboard_themes`; link `cc_terminal_themes` as contrast. |
| `term_codex_app_server_runtime` | none; `term_agentcore_runtime` (active) is a DIFFERENT runtime (AWS Bedrock AgentCore) | Not captured — link `term_agentcore_runtime` as a runtime-concept analogue from doc notes 7/8. |

## Term-Note Authoring Requirements

N/A (inherited) — SP10 owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP04/05/06/09/11/14). The full Term-Note
MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12, backlink expansion,
>200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (dashboard core, pilot):** Notes 1, 2, 3. Pilot Note 1 (`hermes_web_dashboard_overview`) first
  → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (extension system):** Notes 4, 5, 6. GATE G1–G8.
- **Phase 3 (Codex runtime):** Notes 7, 8. GATE G1–G8.

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
for n in hermes_web_dashboard_overview hermes_dashboard_rest_api hermes_dashboard_auth_remote hermes_dashboard_themes hermes_dashboard_plugins hermes_dashboard_extension_api hermes_codex_runtime_tools hermes_codex_runtime_setup; do
```

## Entry Point Decision (inherited)

Contributes 8 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Dashboard & Runtimes" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP10 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_cli.md` | → `hermes_web_dashboard_overview`, `hermes_dashboard_rest_api`, `hermes_dashboard_auth_remote` | the `cli_web_*`/`cli_auth_*` code lives in the CLI repo |
| `repo_hermes_agent_tui_gateway.md` | → `hermes_dashboard_rest_api`, `hermes_web_dashboard_overview` | gateway API-server + embedded-TUI Chat pane ↔ dashboard usage |
| `repo_hermes_agent_plugins.md` | → `hermes_dashboard_plugins`, `hermes_dashboard_extension_api`, `hermes_dashboard_themes` | plugin/theme system repo ↔ dashboard-extension docs |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_codex_runtime_tools`, `hermes_codex_runtime_setup` | the codex provider/runtime adapter ↔ Codex-runtime docs |
| `repo_hermes_agent_agent_core.md` | → `hermes_codex_runtime_tools` | agent-core runtime/api-mode resolution ↔ Codex tool model |
| `term_plugin_sdk.md` | → `hermes_dashboard_plugins`, `hermes_dashboard_extension_api` | concept term → dashboard plugin/SDK docs |
| `term_agentcore_runtime.md` | → `hermes_codex_runtime_tools` | runtime concept → the Codex-runtime model (analogue cross-link) |
| `entry_code_snippets_hermes_agent.md` | → `hermes_web_dashboard_overview`, `hermes_codex_runtime_setup` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 8 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_web_dashboard_overview`) → reindex → verify format/ghost/in-degree BEFORE authoring
the rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing
each note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6
load-bearing blocks, summarize the rest in prose tables. If a note exceeds 350 lines during writing, STOP
and split. If multi-agent: agents return note content, master writes serially where there is
write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP10 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 8 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_plugin_sdk` / `term_agentcore_runtime`
  inlinks (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After the P2 wave (SP06/SP09/SP11/SP14) lands: backfill the `[own]` forward-refs (`term_pkce`,
  `term_hermes_plugin`, `term_code_execution_tool`, `term_delegate_task`, `term_kanban_multi_agent`,
  `term_nous_portal`, `term_messaging_gateway`, `term_hermes_profile`) into the relevant notes' Related Notes.
- Cross-link the dashboard pages to the feature pages they surface (sessions SP02, cron SP06, skills SP05,
  channels SP11-13) once those SPs land — bidirectional dashboard↔feature links.
- Consider one `thought_` note comparing Hermes' two execution runtimes (native vs Codex app-server) against
  the code-digestion findings in `snippet_hermes_agent_core_codex_*`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (no dashboard/runtime/theme term or doc duplicates — BI
  dashboards / a different product's docs / component-concept terms confirmed by reading), finalized Per-Note
  active 2026-06-19), Doc-Note Authoring Spec (derived from `cc_*.md`), Density Re-Assessment (re-read confirmed),
  G5 ghost + G8 scripts, Inlinks.
- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  codex 3959w) at mirror c253b07 to ground every relevance clause; PROMOTED the snippet group from a non-counted
  "bonus" to a fully COUNTED fourth floor and RAISED it from the earlier ≥8 to ≥10, picking the ≥10 per note by
  the code paths the page documents; kept the NEW Code-Repos (≥5) line and the ≥10-Docs line on each of the 8
  notes. All 13 `repo_hermes_agent_*` notes, all cited terms, all cited `snippet_hermes_agent_*` snippets, and
  (G5/G8). No new undigested term or density breach surfaced on re-read; no gate weakened, `status:` unchanged.
- **Docs floor RE-EXPANDED 2026-06-19 (this fix pass):** an independent audit flagged the Documentation floor as
  at-risk of sitting exactly on the bare ≥10 (Notes 2–8 had exactly 10, Note 1 had 11). Re-read the 3 owned source
  each with a specific `relevance:` clause tied to the page's content — lifting Note 1 to **13 docs** and Notes 2–8
  to **12 docs each (minimum = 12)**. Added IDs: Note 1 `cc_web_overview`/`cc_remote_control`; Note 2
  `cc_web_overview`/`cc_proxy_and_gateway_config`; Note 3 `cc_network_tls_and_access`/`cc_login_authentication_troubleshooting`;
  Note 4 `cc_settings_scopes_and_precedence`/`cc_terminal_configuration`; Note 5 `cc_plugins_overview`/`cc_plugin_directory_structure`;
  Note 6 `cc_plugins_overview`/`cc_managed_plugin_policy_settings`; Note 7 `cc_tools_catalog`/`cc_goal_command`;
  active 2026-06-19 (0 missing). Terms/Code-Repos/Snippets lines UNTOUCHED; no existing doc link dropped; `status:` unchanged.
- Density re-read: counts match measured (web-dashboard 9537, extending 5324, codex 3959); **no additional
  splits** beyond the planned 8 (web-dashboard→3, extending→3, codex→2). All 8 notes ≤2500w; code-heavy pages
  curated to ≤6 blocks.
- Collision audit: **0 removals** — `term_mo_impact_dashboard`/`term_genai_adoption_dashboard` (BI),
  `cc_analytics_dashboards`/`cc_agent_view_monitor` (different product), `cc_terminal_themes` (CLI skin),
  `term_agentcore_runtime` (AWS runtime) are all LINK-not-dup; no doc note duplicates an existing term/doc note.
- Term placeholder catch: **2 non-existent term slugs caught at finalization** (`term_user_interface`,
  `term_plugin_manifest`) before lock-in; the clean Terms lines are authoritative.
- Owned-term specificity audit: **2 owned candidates REJECTED** (`term_web_dashboard`,
  `term_codex_app_server_runtime`) as product-specific surfaces, not reusable concepts → SP10 owns 0.
- Undigested terms surfaced at augment: **0 new** (SP10 owns 0 captures; all concepts owned by other SPs or
  existing).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (FOUR FLOORS:
✓ Inlinks (all 8) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (2 owned candidates
audited + rejected) ✓ Slug Collision (BI-dashboard/other-product/runtime-analogue LIKE hits + 2 placeholders
caught) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every
phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓). Term-capture items are N/A-pass (SP10 owns 0
captures); dedup/collision items are substantively PASS (audit performed on all 8 doc notes + 2 owned candidates).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**
**Re-reviewed 2026-06-19 (independent, FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost (Script 4, DB-verify every ref) + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (8 rows under a Dashboard & Runtimes section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 8 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_analytics_dashboards.md`); four-floor minimum (≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) stated in the spec; not invented. |
| CP6 | Borderline density → split | PASS | web-dashboard→3, extending→3, codex→2; all notes ≤2500w; code-heavy notes curated ≤6; borderline ~1700w notes (1/3/5/7/8) checked → cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Independently re-measured 2026-06-19 from `inbox/hermes_agent_docs/` (leading-YAML-stripped body words): web-dashboard 9537, extending-the-dashboard 5324, codex-app-server-runtime 3959 — measured == plan (ratio 1.00). Code-fence counts drift trivially (26–27 / 32 / 11–14) due to fence-heuristic, immaterial to word-driven split tiers. |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP10 owns 0 term captures (2 owned candidates rejected by specificity audit; all other concepts existing or owned by SP04/05/06/09/11/14); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 8 doc notes (term_dictionary AND documentation/); BI-dashboard/other-product/runtime-analogue LIKE hits confirmed = LINK not dup; 2 placeholder term slugs caught + replaced; 2 owned candidates audited + rejected; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 8 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION** (re-confirmed 2026-06-19 under the FOUR-FLOOR standard; 0 DB-unverified cited term/repo/snippet/cc IDs).

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from NousResearch/hermes-agent `website/docs/` at main HEAD `c253b07` (was pinned
`95715dc`); inbox is byte-identical to upstream main. Re-measured all 3 SP10-owned pages with the ledger
convention (body words after stripping YAML frontmatter; code blocks = `^\s*```` lines ÷ 2). One owned page
grew:

- user-guide/features/web-dashboard.md — 9392w/27code -> 9537w/27code
- user-guide/features/extending-the-dashboard.md — 5324w/32code -> 5324w/32code (unchanged, spot-re-measured stable)
- user-guide/features/codex-app-server-runtime.md — 3959w/14code -> 3959w/14code (unchanged, spot-re-measured stable)

My fresh measurements match the manifest's NEW numbers exactly (no discrepancy). The +145-word growth on
web-dashboard.md is immaterial to its split decision: the page was already >4000w → ≥3 notes (Notes 1/2/3,
proc+model+proc), and at 9537w it remains comfortably so. The per-note ~Words estimates (Note 1 ~1700, Note 2
~1500, Note 3 ~1700) absorb +145w split across 3 notes without breaching the ≤2500w cap; no ~estimate moved
materially. **Density re-decision: none** (no-split; no cap breach, no new split added). Cross-ref floor at
the 2026-06-19 re-sync was ≥8 term + ≥8 snippet + ≥5 doc per note; **subsequently RAISED 2026-06-19 (user
directive) to the FOUR-FLOOR standard ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note — snippets
promoted from the interim "bonus" group to a fully COUNTED fourth floor at ≥10** (see the Per-Note Related
Notes Mapping preamble + Augmentation Report). Plan remains **READY FOR EXECUTION**.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 to FOUR-FLOOR) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed 2026-06-19, 9/9 READY under FOUR-FLOOR) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/features/{web-dashboard,extending-the-dashboard,codex-app-server-runtime}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
