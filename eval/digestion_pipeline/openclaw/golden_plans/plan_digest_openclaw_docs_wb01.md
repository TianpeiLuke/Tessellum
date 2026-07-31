---
title: Sub-Plan wb01 — OpenClaw Docs: Web (Control UI, Dashboard, TUI, WebChat)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["web/control-ui", "web/dashboard", "web/tui", "web/webchat"]
---


# Sub-Plan wb01: Web

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared

## Scope

The 4 **Web surfaces** pages — the human-facing front-ends to the OpenClaw Gateway: the browser **Control UI**
(Vite + Lit SPA served by the Gateway, speaking the Gateway WebSocket directly), the **Dashboard** alias/auth
view of that Control UI, the **TUI** (terminal client, Gateway or local/embedded mode), and **WebChat** (native
macOS/iOS SwiftUI chat UI over the same Gateway WS). These pages define the WebSocket-handshake auth model
(token / password / Tailscale Serve identity / trusted-proxy), device pairing, the `chat.*` RPC + display-projection
contract, browser realtime Talk, and the operator security surface (CSP, embeds, insecure-HTTP toggles, PWA/Web
Push). **Priority P2 (Phase B)** — these consume the gateway/auth/session vocabulary defined by Phase A
(gw01–07, cl01–09, co01–07) and are linked, not redefined. The code-side counterparts (`repo_openclaw_gateway`,

**Source**: OpenClaw docs, 4 pages, **8,339 measured words**. **Planned: 6 notes** (control-ui splits into 3).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Control UI | web/control-ui | 5,056 | 6 | 20 | 0 | mixed (split: concept + procedure + model) |
| Dashboard | web/dashboard | 757 | 0 | 4 | 0 | procedure |
| TUI | web/tui | 1,423 | 7 | 16 | 2 | procedure |
| WebChat | web/webchat | 1,103 | 0 | 7 | 1 | model (concept) |

(Measured via `wc -w` and `grep -c '^```'`/2 on the local mirror at `inbox/openclaw_docs/web/`.)

## Content Strategy

- **Prioritize**: (1) the WebSocket-handshake **auth + device-pairing** model — shared verbatim across control-ui,
  dashboard, and webchat (token / password / Tailscale Serve identity / trusted-proxy + one-time pairing approval),
  the gate every web surface depends on; (2) the **`chat.*` RPC + display-projection contract** (`chat.history`
  bounding/truncation, `chat.send` non-blocking acks, `chat.inject`, `chat.message.get`, directive/tool-XML
  stripping) — the behavioral model both Control UI and WebChat implement; (3) the **operator security surface**
  (admin-surface warning, CSP, embed sandbox modes, insecure-HTTP break-glass toggles, avatar/media route auth).
- **Split**: `control-ui.md` (5,056 w, 20 H2, mixed BB) → 3 notes by building-block cluster — a **concept**
  overview/capabilities note, an **auth + security procedure** note, and a **chat/talk model** note (see Split
  Decisions). The other three pages are each a single note.
- **Skip / link-out**: gateway auth config internals → `gw01` (`gateway/authentication`) / `gw05`
  (`gateway/security`); Tailscale Serve/Funnel setup → `gw06` (`gateway/tailscale`); device-token rotation/revocation
  → `cl03` (`cli/devices`); the top-level `web` bind-mode/security overview → `rt03` (`web`); slash-command
  catalog → `to07` (`tools/slash-commands`); goal state → `to04` (`tools/goal`). These are referenced, not
  duplicated. Term concepts (`term_websocket`, `term_oauth_token`, `term_tls`, `term_sse`, `term_compaction`,
  `term_reverse_proxy`) are LINKED, never redefined inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_web_control_ui_overview.md` | concept | control-ui.md: intro, Quick open (local), Runtime config endpoint, Language support, Appearance themes, What it can do (today), Building the UI, Blank Control UI page, Debugging/testing (dev server + remote Gateway) | 650 | What the Control UI is (Vite + Lit SPA served by the Gateway over its WebSocket), how to open it locally, its runtime-config endpoint, localization, appearance/theme/text-size, the full capability map (chat, channels, sessions, dreams, cron, skills, nodes, exec approvals, config, MCP, debug/logs/update), and how to build/dev/recover the UI. |
| 2 | `oc_web_control_ui_auth_security.md` | procedure | control-ui.md: WS-handshake auth, Device pairing (first connection), Personal identity (browser-local), Tailnet access, Insecure HTTP, Content security policy, Avatar route auth, Assistant media route auth | 720 | Securing and connecting to the Control UI: WebSocket-handshake auth (token / password / Tailscale Serve identity / trusted-proxy), one-time device pairing + scope-upgrade approvals, browser-local personal/assistant identity, Tailnet (Serve vs bind+token) access, insecure-HTTP break-glass toggles, the fixed `img-src` CSP, and authenticated avatar/assistant-media routes. |
| 3 | `oc_web_control_ui_chat_talk.md` | model | control-ui.md: What it can do (Chat and Talk excerpt), MCP page, Activity tab, Chat behavior (send/history semantics, talk mode, stop/abort, abort retention), Hosted embeds, Chat message width, PWA install and web push | 720 | The Control UI chat/talk contract: non-blocking `chat.send`/`chat.history` bounding + display normalization + `chat.message.get`, `chat.inject`, idempotency, browser realtime Talk (WebRTC vs Gateway relay vs Live constrained token), stop/abort + partial retention, the MCP operator page, the browser-local Activity tab, hosted `[embed]` sandbox modes, chat width, and PWA install + Web Push (VAPID). |
| 4 | `oc_web_dashboard.md` | procedure | dashboard.md: intro + Quick open, Fast path (recommended), Auth basics (local vs remote), If you see "unauthorized" / 1008 | 480 | The Gateway dashboard (the Control UI served at `/`): the `openclaw dashboard` fast-path link/launch, local-vs-remote auth basics (localhost, TLS `wss://`, shared-secret token/password, SecretRef non-tokenized URLs, Tailscale/trusted-proxy identity), and the unauthorized/1008 + scope-mismatch troubleshooting checklist. |
| 5 | `oc_web_tui.md` | procedure | tui.md: Quick start (Gateway/Local mode), What you see, Mental model (agents+sessions), Sending+delivery, Pickers+overlays, Keyboard shortcuts, Slash commands, Local shell commands, Repair configs from local TUI, Tool output, Terminal colors, History+streaming, Connection details, Options, Troubleshooting | 760 | The terminal UI: Gateway mode (`openclaw tui`) vs local/embedded mode (`openclaw chat`), the agents+sessions mental model and footer, delivery toggle, pickers/overlays, keyboard shortcuts, the slash-command set, `!`-prefixed local shell exec, the config-repair loop (Crestodian), tool-output/colors/streaming, CLI options, and connection troubleshooting. |
| 6 | `oc_web_webchat.md` | model | webchat.md: What it is, Quick start, How it works (behavior), Transcript and delivery model, Control UI agents tools panel, Remote use, Configuration reference (WebChat) | 620 | WebChat (native macOS/iOS chat UI over the Gateway WS): the `chat.history`/`chat.send`/`chat.inject`/`chat.message.get` behavior + display projection, the two-path transcript-vs-delivery model (durable JSONL session log vs live `ReplyPayload` projection), the `/agents` Tools panel (`tools.effective` vs `tools.catalog`), remote tunneling, and the (config-less) global gateway options that govern it. |

## Section Coverage Map

```
control-ui.md (20 H2 → notes 1, 2, 3)
├── (intro: Vite+Lit SPA / basePath / Gateway WS) ──────── → note 1 (oc_web_control_ui_overview)
├── Quick open (local) ─────────────────────────────────── → note 1   [auth lines (handshake params) cross-cut → note 2]
├── Device pairing (first connection) ──────────────────── → note 2 (oc_web_control_ui_auth_security)
├── Personal identity (browser-local) ──────────────────── → note 2
├── Runtime config endpoint ────────────────────────────── → note 1
├── Language support ───────────────────────────────────── → note 1
├── Appearance themes ──────────────────────────────────── → note 1
├── What it can do (today) ─────────────────────────────── → note 1   [Chat and Talk accordion → also summarized in note 3]
├── MCP page ───────────────────────────────────────────── → note 3 (oc_web_control_ui_chat_talk)
├── Activity tab ───────────────────────────────────────── → note 3
├── Chat behavior (send/history, talk, stop/abort, retention) → note 3
├── PWA install and web push ───────────────────────────── → note 3
├── Hosted embeds ──────────────────────────────────────── → note 3
├── Chat message width ─────────────────────────────────── → note 3
├── Tailnet access (recommended) ───────────────────────── → note 2
├── Insecure HTTP ──────────────────────────────────────── → note 2
├── Content security policy ────────────────────────────── → note 2
├── Avatar route auth ──────────────────────────────────── → note 2
├── Assistant media route auth ─────────────────────────── → note 2
├── Building the UI ────────────────────────────────────── → note 1
├── Blank Control UI page ──────────────────────────────── → note 1
├── Debugging/testing: dev server + remote Gateway ─────── → note 1
└── Related (link list) ────────────────────────────────── → notes 1/2/3 References (external) + Related Notes
dashboard.md (4 H2 → note 4)
├── (intro: dashboard = Control UI at / ; quick open ; key refs ; WS auth ; security note) → note 4 (oc_web_dashboard)
├── Fast path (recommended) ────────────────────────────── → note 4
├── Auth basics (local vs remote) ──────────────────────── → note 4
└── If you see "unauthorized" / 1008 ───────────────────── → note 4
tui.md (16 H2 / 2 H3 → note 5)
├── Quick start (### Gateway mode / ### Local mode) ─────── → note 5 (oc_web_tui)
├── What you see ───────────────────────────────────────── → note 5
├── Mental model: agents + sessions ────────────────────── → note 5
├── Sending + delivery ─────────────────────────────────── → note 5
├── Pickers + overlays ─────────────────────────────────── → note 5
├── Keyboard shortcuts ─────────────────────────────────── → note 5
├── Slash commands ─────────────────────────────────────── → note 5
├── Local shell commands ───────────────────────────────── → note 5
├── Repair configs from the local TUI ──────────────────── → note 5
├── Tool output / Terminal colors / History + streaming ── → note 5
├── Connection details / Options ───────────────────────── → note 5
├── Troubleshooting / Connection troubleshooting ───────── → note 5
└── Related (link list) ────────────────────────────────── → note 5 References + Related Notes
webchat.md (7 H2 / 1 H3 → note 6)
├── (intro: macOS/iOS SwiftUI chat UI → Gateway WS) ─────── → note 6 (oc_web_webchat)
├── What it is ─────────────────────────────────────────── → note 6
├── Quick start ────────────────────────────────────────── → note 6
├── How it works (behavior) ────────────────────────────── → note 6
│   └── ### Transcript and delivery model ───────────────── → note 6
├── Control UI agents tools panel ──────────────────────── → note 6
├── Remote use ─────────────────────────────────────────── → note 6
└── Configuration reference (WebChat) ──────────────────── → note 6
```
No orphaned sections. Gateway auth internals (gw01/gw05), Tailscale setup (gw06), `cli/devices` token rotation
(cl03), top-level `web` overview (rt03), slash-command catalog (to07) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| control-ui.md (5,056 w, 20 H2, 6 code, mixed BB) | notes 1 (concept) + 2 (procedure) + 3 (model) | 2× the 2,500-word cap and spans three building blocks: a conceptual "what the UI is + capability map + build/dev" cluster, an auth/security **procedure** cluster (handshake auth, pairing, Tailnet, insecure-HTTP, CSP, route auth), and a chat/talk **contract/model** cluster (`chat.*` semantics, Talk transport model, embeds, PWA/push). Splitting per word-cap + mixed-BB + one-BB-per-note rules keeps each note ≤720 w, ≤6 code blocks, single BB. |
| dashboard.md (757 w) | note 4 (no split) | single procedure, well under caps. |
| tui.md (1,423 w) | note 5 (no split) | single procedure (one terminal client with two run modes); under caps; 7 code fences exceed the 6-cap so config snippets are reproduced selectively (≤6 kept). |
| webchat.md (1,103 w) | note 6 (no split) | single model/concept (chat-over-WS behavior + transcript model); under caps; 0 code. |

## Summary Statistics & Building Block Distribution

- Source pages: **4** (8,339 measured words). New `oc_*` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: concept ×1 (note 1) · procedure ×3 (notes 2, 4, 5) · model ×2 (notes 3, 6).
- Est. digest words ~3,950 (avg ~660/note); all ≤ caps (≤2,500 w / ≤6 code / ≤400 lines). 13 source code fences
  (control-ui 6, tui 7, dashboard 0, webchat 0) distribute across notes; each kept ≤6 (config/CLI snippets
  reproduced selectively, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21): each planned note maps **≥8 relevance-selected `term_dictionary`
  counts: overview 11t·11s·12d · auth_security 12t·12s·13d · chat_talk 12t·12s·12d · dashboard 10t·11s·12d ·
  tui 11t·11s·13d · webchat 12t·11s·12d (all meet ≥8t/≥10s/≥10d floors).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

54 snippets+docs+repos checked; 0 missing). Sibling `oc_*` docs are `(planned, this series)` and count toward
snippets are EXISTING. Relative paths from `resources/documentation/openclaw/`: terms `../../term_dictionary/`;
sibling oc docs `oc_*`; cc/pi/hermes/band docs `../claude_code/` / `../pi/` / `../hermes_agent/` / `../band/`;
repos `../../../areas/code_repos/`; snippets `../../code_snippets/`; entry `../../../0_entry_points/`.

### oc_web_control_ui_overview (11t · 11s · 12d)

**Terms** (relevance-selected, EXISTING):
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: the Control UI is OpenClaw's first-party browser front-end served by the Gateway.
- [term_websocket](../../term_dictionary/term_websocket.md) — full-duplex browser↔server transport; relevance: the SPA speaks directly to the Gateway WebSocket on the same port.
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol for tool/server integration; relevance: the capability map includes a dedicated MCP operator page.
- [term_skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: the UI's Skills panel lists/enables/installs skills (`skills.*`).
- [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the UI's Cron panel lists/adds/edits/runs jobs (`cron.*`).
- [term_tool_registry](../../term_dictionary/term_tool_registry.md) — catalog of agent-callable tools; relevance: the UI streams tool calls + tool cards and edits exec approvals.
- [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — operator approval in the agent loop; relevance: the Exec-approvals panel edits gateway/node allowlists + ask policy.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: the Control UI is the human operator surface over OpenClaw's agent runtime.
- [term_context_window](../../term_dictionary/term_context_window.md) — model token budget; relevance: the chat composer shows a compact context-usage indicator with compaction prompts.
- [term_iframe_sandbox](../../term_dictionary/term_iframe_sandbox.md) — sandboxed embedded-content frame; relevance: hosted `[embed]` content in the UI uses the controlUi embedSandbox policy.

- [cc_web_overview](../claude_code/cc_web_overview.md) — Claude Code's browser-based agent surface; relevance: direct cross-tool analog of OpenClaw's browser Control UI.
- [cc_web_quickstart](../claude_code/cc_web_quickstart.md) — opening/using the Claude Code web app; relevance: parallels the Control UI quick-open + first-connect flow.
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — Hermes Agent's web dashboard surface; relevance: closest ecosystem analog (a coding-agent gateway's browser dashboard).
- [hermes_dashboard_themes](../hermes_agent/hermes_dashboard_themes.md) — theming the Hermes dashboard; relevance: parallels the Control UI Appearance themes (Claw/Knot/Dash + tweakcn) + text-size.
- [cc_terminal_themes](../claude_code/cc_terminal_themes.md) — Claude Code theme configuration; relevance: cross-tool analog of the appearance/theme capability.
- [pi_quickstart](../pi/pi_quickstart.md) — Pi coding-agent quick start; relevance: sibling coding-agent first-run, parallels Control UI quick open.
- [pi_themes](../pi/pi_themes.md) — Pi theming; relevance: cross-tool analog of Control UI appearance/theme import.
- [oc_web_control_ui_auth_security](oc_web_control_ui_auth_security.md) (planned, this series) — securing/connecting the Control UI; relevance: the overview's quick-open/handshake lines hand off to this auth note.
- [oc_web_control_ui_chat_talk](oc_web_control_ui_chat_talk.md) (planned, this series) — the chat/talk contract; relevance: the "What it can do" Chat/Talk accordion is fully documented here.
- [oc_web_dashboard](oc_web_dashboard.md) (planned, this series) — the Gateway dashboard (Control UI at `/`); relevance: the dashboard IS this Control UI under an auth/launch lens.
- [oc_web_tui](oc_web_tui.md) (planned, this series) — the terminal client; relevance: sibling Web surface, the non-browser operator front-end.
- [oc_web_webchat](oc_web_webchat.md) (planned, this series) — native chat UI over the same WS; relevance: sibling Web surface sharing the chat contract.

**Repos** (EXISTING):
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the OpenClaw apps/UI surfaces; relevance: implements the Control UI SPA and build pipeline (`ui:build`/`ui:dev`).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway server; relevance: serves the static Control UI + the runtime-config endpoint and WS.

**Snippets** (ALL EXISTING):
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WS connection setup; relevance: the transport the SPA opens on the same port.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP listener + WS upgrade; relevance: how the Gateway serves the static UI and upgrades to WS.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime config broadcast; relevance: backs the `/control-ui-config.json` runtime-settings endpoint.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config apply/restart; relevance: the UI's Config panel calls `config.apply` + restart.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — assorted server RPC methods; relevance: backs status/health/models/logs/update panels.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: the Exec approvals panel (`exec.approvals.*`).
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP loopback transport; relevance: the MCP capability/page operator view.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — dreaming status/preview; relevance: the Dreams panel (`doctor.memory.*`).
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + notifications; relevance: backs the Cron jobs panel.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent dispatch handler; relevance: backs the sessions/agents the UI lists and drives.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the `openclaw gateway` launch path that serves the UI.


### oc_web_control_ui_auth_security (12t · 12s · 13d)

**Terms** (relevance-selected, EXISTING):
- [term_websocket](../../term_dictionary/term_websocket.md) — the browser↔gateway transport; relevance: auth is supplied during the WebSocket handshake (`connect.params.auth.*`).
- [term_websocket_framing](../../term_dictionary/term_websocket_framing.md) — WS message/close-frame structure; relevance: pairing failures surface as `disconnected (1008)` close codes.
- [term_authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the whole note is the handshake auth + device-pairing model.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer-style shared secret; relevance: token auth (`gateway.auth.token`) is the default shared-secret mode.
- [term_oauth](../../term_dictionary/term_oauth.md) — delegated-auth protocol family; relevance: contextualizes token/identity auth modes vs shared-secret.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: `trusted-proxy` auth admits operator sessions via an identity-aware non-loopback proxy.
- [term_proxy_pattern](../../term_dictionary/term_proxy_pattern.md) — proxy design pattern; relevance: Tailscale Serve proxies HTTPS to a loopback gateway.
- [term_tls](../../term_dictionary/term_tls.md) — transport encryption; relevance: insecure-HTTP block-glass exists because non-secure contexts disable WebCrypto; HTTPS is the fix.
- [term_access_control](../../term_dictionary/term_access_control.md) — scoped permission enforcement; relevance: pairing scope-upgrade approvals + CSP + route auth gate access.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: failed Serve-auth attempts for the same `{scope, ip}` are serialized before the failed-auth limiter records them.
- [term_session_hijacking](../../term_dictionary/term_session_hijacking.md) — stolen-credential session theft; relevance: device pairing + `mediaTicket` short-lived tokens + URL-fragment token handling defend against it.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: these are OpenClaw's gateway auth modes.

- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — Claude Code web security model; relevance: cross-tool analog of the Control UI admin-surface security posture.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: parallels shared-secret/token vs identity-bearing auth.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network error troubleshooting; relevance: parallels the unauthorized/1008/scope-mismatch checklist.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — authenticating MCP servers; relevance: same bearer/identity auth family the Control UI's MCP page operates within.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS + network access; relevance: parallels the `wss://`/insecure-HTTP/secure-context requirements.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: parallels trusted-proxy + Tailscale Serve fronting.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes dashboard remote auth; relevance: closest ecosystem analog of remote dashboard WS auth.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi credential/auth flow; relevance: sibling coding-agent auth-profile model.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: cross-tool analog of the operator security surface.
- [oc_web_dashboard](oc_web_dashboard.md) (planned, this series) — dashboard access + auth basics; relevance: shares the verbatim handshake-auth + 1008 troubleshooting model.
- [oc_web_control_ui_overview](oc_web_control_ui_overview.md) (planned, this series) — what the UI is; relevance: the overview hands off quick-open handshake lines to this note.
- [oc_web_control_ui_chat_talk](oc_web_control_ui_chat_talk.md) (planned, this series) — chat/talk + embeds; relevance: CSP/embed-sandbox here governs the embed feature there.
- [oc_web_webchat](oc_web_webchat.md) (planned, this series) — native chat UI; relevance: shares the same shared-secret/Tailscale/trusted-proxy auth options.

**Repos** (EXISTING):
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway server; relevance: implements handshake auth, device pairing, CSP, and route auth.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security module; relevance: implements the auth/CSP/route-auth surface this note documents.

**Snippets** (ALL EXISTING):
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: token/password/Tailscale/trusted-proxy mode resolution.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: the handshake authorization decision path.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — failed-auth rate-limit policy; relevance: serialized same-`{scope,ip}` retries / `retry later`.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: short-lived auth/media tickets used by the UI.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — device pairing flow; relevance: the one-time pairing approval + scope-upgrade flow.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error/close codes; relevance: `1008 pairing required`, `AUTH_TOKEN_MISMATCH`, `AUTH_SCOPE_MISMATCH`.
- [snippet_openclaw_gateway_control_ui_avatar_resolve](../../code_snippets/snippet_openclaw_gateway_control_ui_avatar_resolve.md) — avatar resolution; relevance: authenticated `GET /avatar/<agentId>` route auth.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS; relevance: device-identity + secure-context (`wss://`) requirements.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method scope gating; relevance: scope-upgrade approvals + operator-vs-node admittance.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup wiring; relevance: how configured auth mode is installed at gateway start.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy; relevance: trusted-proxy / Serve connection path.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: CSP `img-src` + remote-avatar stripping rationale.

**Entry:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1 pre-step) — Web section back-link.

### oc_web_control_ui_chat_talk (12t · 12s · 12d)

**Terms** (relevance-selected, EXISTING):
- [term_websocket](../../term_dictionary/term_websocket.md) — the chat/talk transport; relevance: `chat.*` and Talk relay RPCs ride the Gateway WS.
- [term_idempotency_key](../../term_dictionary/term_idempotency_key.md) — dedup key for retried requests; relevance: re-sending with the same `idempotencyKey` returns `in_flight`/`ok`.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe operation property; relevance: in-flight submit coalescing + Gateway request dedup.
- [term_compaction](../../term_dictionary/term_compaction.md) — transcript summarization to fit context; relevance: the composer's compaction button at recommended levels.
- [term_context_window](../../term_dictionary/term_context_window.md) — model token budget; relevance: the context-usage indicator that drives compaction prompts.
- [term_sse](../../term_dictionary/term_sse.md) — server-streamed events; relevance: `chat.send` is non-blocking and the response streams via `chat` events.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: streamed tool calls + live tool-output cards in chat.
- [term_voice_mode](../../term_dictionary/term_voice_mode.md) — realtime voice interaction; relevance: browser Talk (WebRTC / Live constrained token / Gateway relay).
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — audio→text; relevance: Talk streams microphone PCM through `talk.session.appendAudio`.
- [term_voice_call](../../term_dictionary/term_voice_call.md) — realtime voice session; relevance: the Talk relay transport keeps provider credentials server-side.
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the dedicated MCP operator page lives in this note's cluster.
- [term_agent_steering](../../term_dictionary/term_agent_steering.md) — injecting guidance into a running turn; relevance: Steer a queued follow-up into the active run; `talk.client.steer`.

- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — Claude Code voice dictation; relevance: cross-tool analog of browser realtime Talk/voice input.
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — streaming model output; relevance: parallels non-blocking `chat.send` + streamed `chat` events.
- [cc_sdk_stream_text_and_tool_calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — streamed text + tool calls; relevance: parallels streamed tool-call cards in chat.
- [cc_interactive_session_features](../claude_code/cc_interactive_session_features.md) — interactive chat features; relevance: parallels stop/abort, model picker, idempotent send.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — MCP concept overview; relevance: backs the Control UI MCP operator page.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — Pi streaming API; relevance: sibling coding-agent streaming contract.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — Hermes voice mode; relevance: closest ecosystem analog of browser Talk.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — Hermes STT pipeline; relevance: analog of the Talk transcription relay.
- [oc_web_webchat](oc_web_webchat.md) (planned, this series) — native chat UI; relevance: implements the same `chat.*` contract + display projection.
- [oc_web_control_ui_overview](oc_web_control_ui_overview.md) (planned, this series) — capability map; relevance: the Chat/Talk accordion is summarized there, detailed here.
- [oc_web_control_ui_auth_security](oc_web_control_ui_auth_security.md) (planned, this series) — embeds/CSP; relevance: hosted embed sandbox policy governs in-chat `[embed]`.
- [oc_web_tui](oc_web_tui.md) (planned, this series) — terminal client; relevance: shares stop/abort + steer + delivery semantics in a non-browser surface.

**Repos** (EXISTING):
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway server; relevance: implements `chat.*`, Talk relay, and display projection.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: realtime voice providers behind Talk.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the UI surfaces; relevance: the Chat/Talk UI components and PWA/Web-Push wiring.

**Snippets** (ALL EXISTING):
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — `chat.send` handler; relevance: non-blocking ack + run streaming + idempotency.
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — `chat.history`/`chat.inject`; relevance: bounded history + display normalization + inject.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — `chat.abort` handler; relevance: stop/abort by runId or sessionKey + partial retention.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat/buffered deltas; relevance: streamed delta delivery + NO_REPLY/HEARTBEAT_OK handling.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: chat uploads (images + non-video files) handling.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: assistant/generated images persisted as managed media references.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — Talk transcription relay; relevance: the Gateway relay transport for realtime voice.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — voice exec dedup; relevance: voice tool-call routing through `talk.client.toolCall`.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP loopback; relevance: the MCP operator page transport.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method scope gating; relevance: scope-gated `push.web.*` and `talk.*` methods.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: backend STT provider behind Talk.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: realtime audio pipeline for browser Talk.

**Entry:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1 pre-step) — Web section back-link.

### oc_web_dashboard (10t · 11s · 12d)

**Terms** (relevance-selected, EXISTING):
- [term_websocket](../../term_dictionary/term_websocket.md) — the dashboard transport; relevance: auth is enforced at the WebSocket handshake.
- [term_websocket_framing](../../term_dictionary/term_websocket_framing.md) — WS close frames; relevance: the `unauthorized / 1008` failure is a WS close code.
- [term_authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the note is dashboard auth basics (local vs remote).
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — shared-secret token; relevance: `gateway.auth.token` / `OPENCLAW_GATEWAY_TOKEN` URL-fragment bootstrap.
- [term_tls](../../term_dictionary/term_tls.md) — transport encryption; relevance: with `gateway.tls.enabled`, links use `https://`/`wss://`.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: trusted-proxy identity satisfies WS auth for remote dashboards.
- [term_access_control](../../term_dictionary/term_access_control.md) — scoped access; relevance: `AUTH_SCOPE_MISMATCH` requires re-pairing/approving the dashboard scope contract.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — keeping state across reloads; relevance: the UI keeps the token in sessionStorage for the tab session.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: the async Serve path serializes failed `{scope, ip}` attempts → `retry later`.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw dashboard` is the launch fast-path.

- [cc_web_quickstart](../claude_code/cc_web_quickstart.md) — Claude Code web quickstart; relevance: parallels the dashboard fast-path open.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: parallels shared-secret vs identity auth.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/auth troubleshooting; relevance: direct analog of the unauthorized/1008 checklist.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network errors; relevance: parallels token-drift/scope-mismatch recovery.
- [cc_remote_vs_web_and_deep_links](../claude_code/cc_remote_vs_web_and_deep_links.md) — remote vs web + deep links; relevance: parallels the non-tokenized clean dashboard link + remote access.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes dashboard remote auth; relevance: closest ecosystem analog of remote dashboard auth + SSH tunnel.
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — Hermes web dashboard; relevance: analog of the gateway dashboard surface.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi auth flow; relevance: sibling coding-agent shared-secret/identity auth.
- [oc_web_control_ui_overview](oc_web_control_ui_overview.md) (planned, this series) — what the Control UI is; relevance: the dashboard IS the Control UI served at `/`.
- [oc_web_control_ui_auth_security](oc_web_control_ui_auth_security.md) (planned, this series) — full auth/security model; relevance: shares the verbatim handshake-auth modes + device pairing.
- [oc_web_webchat](oc_web_webchat.md) (planned, this series) — native chat UI; relevance: sibling Web surface sharing shared-secret WS auth.
- [oc_web_tui](oc_web_tui.md) (planned, this series) — terminal client; relevance: alternative operator front-end with the same connection/auth options.

**Repos** (EXISTING):
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway server; relevance: serves the dashboard, enforces handshake auth, prints the clean link.

**Snippets** (ALL EXISTING):
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: local-vs-remote shared-secret/Tailscale/trusted-proxy resolution.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: `1008`, `AUTH_TOKEN_MISMATCH`, `AUTH_SCOPE_MISMATCH`.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup; relevance: installs the configured dashboard auth mode at start.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: the auth-precedence order (token → deviceToken → bootstrap).
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — failed-auth limiter; relevance: serialized `{scope,ip}` retries → `retry later`.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: sessionStorage token + clean-URL bootstrap.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect via proxy; relevance: SSH tunnel / trusted-proxy remote dashboard path.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the `wss://127.0.0.1:18789` endpoint the dashboard opens.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets resolution; relevance: SecretRef-managed token → non-tokenized URL behavior.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI catalog; relevance: the `openclaw dashboard` / `openclaw status` / `openclaw doctor` commands.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: routes `openclaw dashboard` to the launch+link handler.

**Entry:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1 pre-step) — Web section back-link.

### oc_web_tui (11t · 11s · 13d)

**Terms** (relevance-selected, EXISTING):
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw tui` / `openclaw chat` are its terminal clients.
- [term_websocket](../../term_dictionary/term_websocket.md) — the gateway-mode transport; relevance: the TUI registers with the Gateway as `mode: "tui"` over WS.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: the TUI drives OpenClaw agents from a terminal.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the agent execution wrapper; relevance: local mode uses the embedded agent runtime directly.
- [term_subagent](../../term_dictionary/term_subagent.md) — child agent under a parent; relevance: the agents+sessions mental model the footer surfaces.
- [term_agent_steering](../../term_dictionary/term_agent_steering.md) — steering a running turn; relevance: queued follow-ups + abort/steer semantics in the TUI.
- [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — operator gating; relevance: `/elevated` + once-per-session local-exec approval prompt.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: `!`-prefixed local shell exec runs in a fresh non-interactive shell.
- [term_session_features](../../term_dictionary/term_session_features.md) — per-session controls; relevance: `/think`/`/fast`/`/verbose`/`/trace`/`/reasoning` session overrides.
- [term_sessionid](../../term_dictionary/term_sessionid.md) — session key identity; relevance: `agent:<agentId>:<sessionKey>` resolution + session picker.
- [term_context_window](../../term_dictionary/term_context_window.md) — token budget; relevance: footer token counts + `/usage` display.

- [cc_terminal_configuration](../claude_code/cc_terminal_configuration.md) — Claude Code terminal config; relevance: cross-tool analog of TUI terminal setup/options.
- [cc_terminal_themes](../claude_code/cc_terminal_themes.md) — terminal theming; relevance: parallels `OPENCLAW_THEME=light/dark` + terminal colors.
- [cc_interactive_mode_keyboard_shortcuts](../claude_code/cc_interactive_mode_keyboard_shortcuts.md) — interactive keyboard shortcuts; relevance: direct analog of the TUI keyboard-shortcut set.
- [cc_quickstart](../claude_code/cc_quickstart.md) — Claude Code quickstart; relevance: parallels the TUI quick-start (gateway vs local mode).
- [cc_interactive_session_features](../claude_code/cc_interactive_session_features.md) — interactive session features; relevance: parallels slash commands, pickers, deliver toggle.
- [pi_terminal_setup](../pi/pi_terminal_setup.md) — Pi terminal setup; relevance: sibling coding-agent terminal client setup.
- [pi_interactive_usage](../pi/pi_interactive_usage.md) — Pi interactive TUI usage; relevance: sibling TUI usage model (pickers/commands).
- [pi_keybindings](../pi/pi_keybindings.md) — Pi keybindings; relevance: analog of the TUI keyboard shortcuts.
- [hermes_tui_interface](../hermes_agent/hermes_tui_interface.md) — Hermes TUI; relevance: closest ecosystem analog of the OpenClaw terminal UI.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — Hermes interactive slash commands; relevance: analog of the TUI slash-command set.
- [oc_web_control_ui_overview](oc_web_control_ui_overview.md) (planned, this series) — the browser front-end; relevance: sibling Web surface (browser vs terminal).
- [oc_web_dashboard](oc_web_dashboard.md) (planned, this series) — dashboard auth/launch; relevance: the TUI shares `--url/--token/--password` connection + troubleshooting.
- [oc_web_control_ui_chat_talk](oc_web_control_ui_chat_talk.md) (planned, this series) — chat/stop/steer semantics; relevance: the TUI implements the same abort/steer/delivery model.

**Repos** (EXISTING):
- [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — Hermes TUI+gateway; relevance: closest ecosystem analog (TUI-over-gateway client).
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — OpenClaw CLI/wizard; relevance: `openclaw configure`/`doctor --fix` repair-loop the TUI invokes.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway server; relevance: the gateway-mode TUI connects to it as `mode: "tui"`.

**Snippets** (ALL EXISTING):
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `openclaw tui/chat/terminal/configure/doctor` commands.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: routes `tui`/`chat`/`crestodian` aliases.
- [snippet_openclaw_cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — CLI main run path; relevance: the local/embedded vs gateway TUI entry decision.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy; relevance: `--url/--token/--password` remote connection.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the gateway-mode TUI WS registration.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: `disconnected` connection troubleshooting.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key utilities; relevance: `agent:<agentId>:<sessionKey>` expansion in `/session`.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: resuming the last selected session per gateway/agent/scope.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: the local-TUI config-repair loop (`config set`/`validate`).
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: `openclaw doctor --fix` migration the repair loop runs.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: Crestodian local setup/repair backend startup.

**Entry:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1 pre-step) — Web section back-link.

### oc_web_webchat (12t · 11s · 12d)

**Terms** (relevance-selected, EXISTING):
- [term_websocket](../../term_dictionary/term_websocket.md) — the chat transport; relevance: the native UI talks directly to the Gateway WebSocket.
- [term_idempotency_key](../../term_dictionary/term_idempotency_key.md) — dedup key; relevance: the Gateway dedupes repeated `chat.send` runs reusing the same idempotency key.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe property; relevance: Control UI coalesces duplicate in-flight submits.
- [term_compaction](../../term_dictionary/term_compaction.md) — transcript summarization; relevance: compaction entries render as an explicit compacted-history divider.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: the JSONL session file is the durable model/runtime transcript.
- [term_sessionid](../../term_dictionary/term_sessionid.md) — backing session identity; relevance: Control UI remembers the Gateway `sessionId` across reconnects.
- [term_sse](../../term_dictionary/term_sse.md) — streamed events; relevance: `ReplyPayload` events are the live delivery projection vs durable log.
- [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: the `/agents` Tools panel shows `tools.effective` vs `tools.catalog`.
- [term_tool_descriptor](../../term_dictionary/term_tool_descriptor.md) — per-tool capability record; relevance: the read-only effective-tools projection per session.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: tool-call XML is stripped from display-normalized history.
- [term_ios](../../term_dictionary/term_ios.md) — Apple mobile OS; relevance: WebChat is a native macOS/iOS SwiftUI app.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: WebChat is an OpenClaw-managed internal source surface.

- [cc_web_session_management](../claude_code/cc_web_session_management.md) — Claude Code web session management; relevance: cross-tool analog of the transcript/delivery + session continuation model.
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — streaming output; relevance: parallels live `ReplyPayload` projection vs durable transcript.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — background session hosting; relevance: parallels gateway-owned durable session log fetched remotely.
- [cc_interactive_session_features](../claude_code/cc_interactive_session_features.md) — interactive session features; relevance: parallels history/inject/abort-partial behavior.
- [pi_sessions](../pi/pi_sessions.md) — Pi sessions; relevance: sibling coding-agent session model.
- [pi_session_file_format](../pi/pi_session_file_format.md) — Pi session JSONL format; relevance: direct analog of the durable JSONL session transcript.
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — Hermes session lifecycle/resume; relevance: analog of continuing a stored conversation across reconnects.
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — Hermes session storage; relevance: analog of the durable session-log path.
- [oc_web_control_ui_chat_talk](oc_web_control_ui_chat_talk.md) (planned, this series) — the chat/talk contract; relevance: WebChat implements the same `chat.*` + display projection.
- [oc_web_control_ui_overview](oc_web_control_ui_overview.md) (planned, this series) — capability map; relevance: the Control UI chat tab is the browser sibling of WebChat.
- [oc_web_dashboard](oc_web_dashboard.md) (planned, this series) — dashboard auth basics; relevance: WebChat uses the same shared-secret WS auth (even on loopback).
- [oc_web_tui](oc_web_tui.md) (planned, this series) — terminal client; relevance: both are internal source surfaces (not generic outbound channels).

**Repos** (EXISTING):
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the apps/UI surfaces; relevance: the native macOS/iOS WebChat SwiftUI app + Control UI agents Tools panel.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — the sessions module; relevance: the durable JSONL transcript + session manager WebChat reads.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway server; relevance: serves `chat.history/send/inject/message.get` + `tools.effective/catalog`.

**Snippets** (ALL EXISTING):
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — `chat.history`/`chat.inject`; relevance: bounded history + display projection + inject.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat lifecycle persistence; relevance: persisting model-visible user/assistant/toolResult messages.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript media pipeline; relevance: WebChat-managed media transcript supplements.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — `chat.send` handler; relevance: idempotency-keyed run dedup on send.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — `chat.abort` handler; relevance: aborted partial output persisted with abort metadata.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: append-only active-branch transcript the history follows.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — session chat type; relevance: WebChat as an internal source surface (not outbound channel).
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: continuing the same stored conversation by `sessionId`.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: `tools.catalog` behind the Tool Configuration view.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy precedence; relevance: effective access follows allow/deny + per-agent overrides.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compaction/reset; relevance: the compacted-history checkpoint divider WebChat renders.

**Entry:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1 pre-step) — Web section back-link.

**DB-verification (2026-06-21):** every EXISTING `note_id` above was verified by exact-id query against `notes`
docs. Verified-MISSING candidates EXCLUDED (would be ghosts), per master Undigested-Terms policy →
LINKED to existing terms instead: `term_pwa`/`term_service_worker`/`term_web_push`/`term_vapid` →
`term_websocket`+`term_openclaw`; `term_tailscale` → `term_reverse_proxy`+`term_proxy_pattern`;
`term_content_security_policy`/`term_csp` → `term_access_control`+`term_iframe_sandbox`;
`term_webrtc`/`term_realtime_voice` → `term_voice_mode`+`term_voice_call`+`term_speech_to_text`;
`term_secretref` → `term_oauth_token`; `term_single_page_app`/`term_vite`/`term_lit` → `term_openclaw`;
`term_terminal_ui`/`term_tui` → `term_session_features`+coding-agent terms; `term_dashboard`/`term_gateway` →
`term_openclaw`. `entry_openclaw_docs` is the master W1 pre-step (created before any wb01 note executes).

## Undigested Terms Plan

Per master: OpenClaw web-surface vocabulary is digested as `oc_*` doc concept notes by THIS sub-plan, NOT
promoted to `term_dictionary`. Existing terms are LINKED, never redefined inline. Expected **0 new
`term_dictionary` captures**.

| Term (from source) | Disposition |
|---|---|
| Control UI / Dashboard / WebChat / TUI | Subjects of this sub-plan's `oc_web_*` doc notes (notes 1–6); not term entries. |
| Gateway WebSocket / WS handshake | Link `term_websocket`; the handshake-auth procedure lives in note 2. |
| Device pairing / pairing approval / device identity | Documented in note 2 (procedure); link `term_authentication` / `term_access_control`. No `term_pairing` (MISSING) created — concept is OpenClaw-specific UI flow, home is note 2. |
| Tailscale Serve / Tailnet / trusted-proxy / token / password auth | Auth modes documented in notes 2/4; link `term_reverse_proxy`, `term_oauth_token`, `term_tls`, `term_authentication`. Tailscale setup → gw06 (link-out). |
| `chat.send` / `chat.history` / `chat.inject` / `chat.message.get` | The chat RPC contract documented in notes 3/6 (model); link `term_websocket`, `term_idempotency_key`, `term_compaction`, `term_sse`. |
| Talk mode / realtime voice / WebRTC / Live constrained token | Documented in note 3 (model); link `term_voice_mode`, `term_speech_to_text`, `term_text_to_speech`. No `term_webrtc`/`term_realtime_voice` (MISSING) created. |
| PWA / service worker / Web Push / VAPID | Documented in note 3; link `term_websocket` / `term_openclaw`. No `term_pwa`/`term_service_worker`/`term_web_push`/`term_vapid` (MISSING) created — install-channel detail, home is note 3. |
| Content Security Policy / embed sandbox / `img-src` | Documented in note 2 (CSP) + note 3 (embeds); link `term_access_control`, `term_reverse_proxy`. No `term_csp`/`term_content_security_policy` (MISSING) created. |
| MCP page / MCP servers | Operator view documented in note 3; link `term_mcp` (EXISTING). |
| Skills / Cron / Exec approvals / Dreams panels | Capability map in note 1; link `term_skills`, `term_cron`, `term_human_in_the_loop`. |
| Idempotency key / in-flight dedup | Documented in notes 3/6; link `term_idempotency_key` (EXISTING). |
| Agents + sessions / session keys / scope | TUI/WebChat mental model in notes 5/6; link `term_agent_harness`, `term_autonomous_coding_agents`. |
| Steer / queue follow-ups | Documented in notes 3/5; link `term_agent_steering` (EXISTING). |

**New-term candidates:** none. No genuinely cross-cutting, vault-reusable term with no existing note AND no
doc-page home appears in these 4 pages — all web-surface vocabulary either has a doc-note home (`oc_web_*`) or
maps to an existing `term_dictionary` entry. (Augment Step 2d re-runs this scan against a fresh re-read.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** wb01 authors zero `term_dictionary` notes; it only LINKS existing terms. If augment's
Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no existing note, the master requirement
best-fit `acronym_glossary_*.md` (web/UI vocabulary → the agentic/dev-tool glossary), and W5 in master.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order + body structure + footer) | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2 | Grounding (no claim absent from source) | diff each note vs `inbox/openclaw_docs/web/<page>.md` |
| G3 | Density + Coverage (≤2,500 w / ≤6 code / ≤400 L; every mapped H2/H3 covered) | `wc -w` + `grep -c '^```'`/2 + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected terms + repos + sibling oc_* + cc/pi docs, each with relevance statement) | manual + DB existence of every cited target |
| G5 | Ghost-reference detect + redirect (0 links to non-existent notes) | `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix (0 wrong relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability — every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` | via `entry_openclaw_docs.md` + repo/term inlinks |
| G8 | In-degree ≥1 (anti-island) per new note | `note_links` query after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
OC=the vault/resources/documentation/openclaw
GATE_DIR="$OC"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_web_control_ui_overview oc_web_control_ui_auth_security oc_web_control_ui_chat_talk oc_web_dashboard oc_web_tui oc_web_webchat"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # sibling cross-link present (≥1 oc_ link beyond self)
  grep -oE "\]\(${SIBLING_PREFIX}[a-z0-9_]+\.md\)" "$f" | grep -v "$n.md" >/dev/null || echo "NO SIBLING oc_ LINK in $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5/G6 (run as skills): /tessellum-fix-ghost-references ; /tessellum-fix-broken-links
# Reindex + G7/G8 in-degree:
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  echo "$n in_degree=${ind:-0}"; [ "${ind:-0}" -lt 1 ] && echo "ISLAND: $n (G8 fail)"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code (kept ≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_web_control_ui_overview | concept | 650 | 4 (build/dev + quick-open) | ✅ |
| 2 | oc_web_control_ui_auth_security | procedure | 720 | 4 (pairing CLI + insecure-auth/break-glass JSON5 + tailscale) | ✅ |
| 3 | oc_web_control_ui_chat_talk | model | 720 | 3 (embedSandbox + chatMessageMaxWidth JSON5 + RPC list) | ✅ |
| 4 | oc_web_dashboard | procedure | 480 | 1 (SSH tunnel) | ✅ |
| 5 | oc_web_tui | procedure | 760 | 6 (quick-start + remote + local + repair-loop + showRemoteHost) | ✅ |
| 6 | oc_web_webchat | model | 620 | 0 | ✅ |

No note approaches the 2,500-word / 400-line cap. control-ui.md (5,056 w / 6 code, 20 H2, mixed BB) is split
3-way so each child stays single-BB and ≤720 w. tui.md's 7 source fences are reproduced selectively (≤6 kept).

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (master W1 pre-step, `building_block: navigation`,
created before any wb01 note executes) under a **"Web" section / "Web surfaces" cluster** (notes 1–6). Each
note RECEIVES its entry-point back-link at finalization (satisfies G7/G8). No new entry point is created by
wb01 (the section hub already exists per master); master W2/W3 (parent-hub back-link + code↔docs cross-links)
are master-level pre-steps, not repeated here.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; each new note needs ≥1):

- `entry_openclaw_docs.md` (EXISTING, master pre-step) → all 6 notes (Web section rows) — primary anti-island source.
- `repo_openclaw_gateway.md` (EXISTING) → notes 1, 2, 3, 4, 5, 6 (the Gateway serves the Control UI / TUI / WebChat WS).
- `repo_openclaw_apps.md` (EXISTING) → notes 1, 3, 6 (the apps/UI surfaces).
- `repo_hermes_agent_tui_gateway.md` (EXISTING) → note 5 (TUI/gateway analog).
- `repo_openclaw_security.md` (EXISTING) → note 2 (auth/CSP/route-auth surface).
- `term_websocket.md` (EXISTING) → notes 2, 3, 4, 6 (the WS handshake/RPC transport).
- `term_voice_mode.md` (EXISTING) → note 3 (browser realtime Talk).
- `term_mcp.md` (EXISTING) → notes 1, 3 (MCP operator page).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run (well under for 6
notes). Re-read each source page; config/CLI snippets reproduced verbatim. One BB per note. Reindex
incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase
--autostash` first; commit + push per wave; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21 (9/9 checkpoints PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the draft `## Candidate Cross-References` with a **Per-Note Related Notes Mapping
(LOCKED — xref-augment 2026-06-21)** at raised floors: **≥8 term_dictionary terms · ≥10 EXISTING code_snippets ·
`[Name](relpath.md) — what it is; relevance: why THIS note`. Source pages re-measured (CP7): control-ui 5,018 w
(plan 5,056), dashboard 737 w (757), tui 1,383 w (1,423), webchat 1,080 w (1,103) — all within ±3%, no
re-split needed.

**Per-note counts (deterministically computed from the file; all meet floors):**

| Note | BB | Terms | Snippets (all EXISTING) | Docs (EXISTING + planned oc_*) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| oc_web_control_ui_overview | concept | 11 | 11 | 12 (7 existing + 5 planned) | 3 | ✅ |
| oc_web_control_ui_auth_security | procedure | 12 | 12 | 13 (9 existing + 4 planned) | 2 | ✅ |
| oc_web_control_ui_chat_talk | model | 12 | 12 | 12 (8 existing + 4 planned) | 3 | ✅ |
| oc_web_dashboard | procedure | 10 | 11 | 12 (8 existing + 4 planned) | 2 | ✅ |
| oc_web_tui | procedure | 11 | 11 | 13 (10 existing + 3 planned) | 3 | ✅ |
| oc_web_webchat | model | 12 | 11 | 12 (8 existing + 4 planned) | 3 | ✅ |

**DB-verification.** 134 distinct EXISTING `note_id` targets verified by exact-id query against `notes`
pre-step) cited as `(planned)`. New corpora pulled into the mapping beyond the draft: `hermes_agent/hermes_*`
(dashboard/auth-remote/TUI/voice/sessions analogs — closest ecosystem siblings), `band/band_*` (WebSocket/ACP/
REST analogs), additional `cc_*`/`pi_*` (interactive/streaming/session/terminal), and a far deeper
`openclaw_gateway`/`openclaw_sessions`/`openclaw_agents`/`openclaw_speech` snippet pool.

**New-term candidates (Step 2d re-scan against fresh re-read): NONE.** Consistent with the master Undigested-Terms
policy and the draft's own scan. Every web-surface concept either (a) is the subject of an `oc_web_*` doc note
(Control UI / Dashboard / WebChat / TUI), or (b) maps to an existing `term_dictionary` entry that is LINKED, not
redefined. Verified-MISSING vocabulary remains EXCLUDED to avoid ghosts and routed to existing terms:
`term_pwa`/`term_service_worker`/`term_web_push`/`term_vapid` → best-fit `term_websocket` + `term_openclaw`;
`term_tailscale` → `term_reverse_proxy` + `term_proxy_pattern`; `term_content_security_policy`/`term_csp` →
`term_access_control` + `term_iframe_sandbox`; `term_webrtc`/`term_realtime_voice` → `term_voice_mode` +
`term_voice_call` + `term_speech_to_text`; `term_secretref` → `term_oauth_token`. **Expected new
`term_dictionary` captures: 0** (so Term-Note Authoring Requirements stays N/A; if a future re-read ever surfaces
a genuinely cross-cutting reusable term with no doc-home, the master W5 path applies: `/tessellum-capture-term-note`
+ best-fit agentic/dev-tool acronym glossary).

**Issues found / fixed during augment:** none material — two cosmetic link display-text typos were corrected
(stray placeholder line in overview Terms; `config_reload_plan` display text aligned to its `note_id`).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)


| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance statements) | **PASS** | Per-Note Related Notes Mapping (LOCKED) present; every note ≥8 terms (10–12), ≥10 snippets (11–12), ≥10 docs (12–13), each link carries `relevance:`; counts computed from file. |
| CP2 | 9-GATE present per batch (G1–G6 + G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link-fix, G7/G8 discoverability/in-degree; Validation Scripts implement reindex + in-degree check. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` cites `entry_openclaw_docs.md` (master W1 pre-step, `building_block: navigation`); wb01 contributes 6 Web-section rows, creates no new entry point; size-rule satisfied (master >30-note series → CREATE handled at master). |
| CP4 | Plan size | **PASS** | 6 notes (≤30); single execution phase. |
| CP6 | Density / borderline splits | **PASS** | Density Re-Assessment: all 6 notes ≤760 w / ≤6 code / ≤400 L; control-ui split 3-way (concept/procedure/model) per word-cap + mixed-BB; no borderline note left unsplit. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured from `inbox/openclaw_docs/web/` (frontmatter stripped): control-ui 5,018 / dashboard 737 / tui 1,383 / webchat 1,080 — all within 0.97–1.0× plan estimates (≤±3%); no >1.5× under-estimate. |
| CP8 | Undigested terms + Term-Note Authoring reqs | **PASS** | `## Undigested Terms Plan` present (disposition per term, 0 new captures); `## Term-Note Authoring Requirements` present (N/A justified for 0 new terms, with master W5 fallback if Step 2d surfaces one). Step 2d re-scan = 0 new candidates. |
| CP8f | Slug specificity / collision audit (term AND doc) | **PASS** | 0 new term slugs → no specificity renames needed. Doc-vs-term collision audit: all `oc_web_*` planned slugs are surface-specific (Control UI / Dashboard / WebChat / TUI), none duplicate an existing term or doc note; `oc_*` folder is empty (0 collisions in `resources/documentation/openclaw/`). |
| CP9 | Discoverability / inlinks (G8, no islands) | **PASS** | `## Inlinks (existing → new)` maps ≥1 outside-folder inbound link to every note (entry_openclaw_docs + repo_openclaw_gateway → all 6; per-note repo/term inlinks); G8 in-degree check in Validation Scripts; inlink addition is a gated execution step, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
