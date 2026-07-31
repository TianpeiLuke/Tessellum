---
title: Sub-Plan cl03 — OpenClaw Docs: CLI (daemon, dashboard, devices, directory, dns, docs, doctor)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/daemon", "cli/dashboard", "cli/devices", "cli/directory", "cli/dns", "cli/docs", "cli/doctor"]
---

# Sub-Plan cl03: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format, dedup-before-create (term_dictionary AND
> documentation/ AND `repo_openclaw*`), 9-GATE validation, cross-references, and entry-point wiring are ALL
> inherited from the master; this file locks only this sub-plan's measured source, planned notes, coverage map,
> and candidate cross-references.

## Scope

The third slice of the OpenClaw CLI command reference: seven `openclaw <command>` pages covering the operator's
day-to-day control surface for the alphabetical `d` commands — service lifecycle (`daemon`), Control-UI launch
(`dashboard`), device pairing + token rotation/revocation (`devices`), channel contact/group/self lookups
(`directory`), wide-area DNS-SD discovery setup (`dns`), live-docs search (`docs`), and the health-check /
guided-repair surface (`doctor`). **Priority P1 (Phase A)** — the CLI is the operational vocabulary the rest of
the OpenClaw docs reference, and these commands (devices pairing/rotation, doctor lint/fix) are the closest
operational analogs to the FZ 15 integration target. The code-side counterparts (`repo_openclaw_gateway`,
`repo_openclaw_security`, `repo_openclaw_cli_wizard`, snippet_openclaw_cli_*) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 5,134 measured words. **Planned: 7 notes** (1 page → 1 note; no splits).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| daemon | cli/daemon | 546 | 1 | 5 | 0 | procedure |
| dashboard | cli/dashboard | 168 | 1 | 1 | 0 | procedure |
| devices | cli/devices | 1,243 | 14 | 5 | 8 | procedure |
| directory | cli/directory | 325 | 4 | 7 | 0 | procedure |
| dns | cli/dns | 210 | 1 | 3 | 0 | procedure |
| docs | cli/docs | 288 | 3 | 6 | 0 | procedure |
| doctor | cli/doctor | 2,354 | 8 | 9 | 0 | procedure |

Totals: 5,134 words · 32 code blocks · 36 H2 · 8 H3. (H2/H3 counted from `^## `/`^### ` headings; code blocks
= ``` fence-lines ÷ 2.)

## Content Strategy

- **Prioritize**: `devices` (pairing approval, token rotate/revoke, scope containment, token-drift recovery —
  the operational security core) and `doctor` (the single largest page; the health/lint/fix/post-upgrade surface
  that operators reach for first). These two carry the highest operational relevance.
- **Split**: none. `doctor` is 2,354 words — under the 2,500-word cap — and is a single coherent procedure
  (one CLI command with postures/options/checks/notes); it is kept as ONE note rather than fragmenting the
  command reference. All other pages are small single-command references. (See Split Decisions.)
- **Link-out (do NOT redefine)**: `daemon` points to `gateway` service commands → link the planned `oc_cli_gateway`
  (cl04, planned, this series) and `repo_openclaw_gateway`; `dashboard`/`devices` auth troubleshooting →
  `gateway/troubleshooting`, `web/dashboard` (other sub-plans / planned); `dns` discovery config →
  `gateway/discovery`, `gateway/configuration` (gw02, planned); `doctor` overlaps `gateway/doctor` (gw02,
  planned) — link, do not duplicate. SecretRef / operator-scope vocabulary links existing terms
  (`term_secrets_manager`, `term_access_control`), not redefined inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_daemon.md` | procedure | daemon.md: Usage, Subcommands (status/install/uninstall/start/stop/restart), Common options, Prefer, Related | 480 | The legacy `openclaw daemon` service-lifecycle alias: install/start/stop/restart/uninstall + status, per-subcommand options, SecretRef-aware token-drift checks, safe restart, and the redirect to prefer `openclaw gateway`. |
| 2 | `oc_cli_dashboard.md` | procedure | dashboard.md: command + Notes, Related | 280 | `openclaw dashboard` opens (or prints with `--no-open`) the Control UI using current auth; covers TLS-following URLs (https/wss), SecretRef token resolution, and the non-tokenized-URL safety behavior for SecretRef-managed tokens. |
| 3 | `oc_cli_devices.md` | procedure | devices.md: Commands (list/remove/clear/approve/reject/rotate/revoke), Paperclip first-run approval, Common options, Notes, Token drift recovery checklist, Related | 720 | `openclaw devices` — manage device pairing requests and device-scoped tokens: list/approve/reject/remove/clear, rotate/revoke per role, scope-containment + self-only rules, Paperclip first-run pairing, and the AUTH_*_MISMATCH token-drift recovery checklist. |
| 4 | `oc_cli_directory.md` | procedure | directory.md: Common flags, Notes, Using results with `message send`, ID formats (by channel), Self, Peers, Groups, Related | 420 | `openclaw directory` looks up channel contacts/peers, groups, and self ("me") to find IDs for `message send`; covers `--channel`/`--account`/`--json` flags, config-backed results, and per-channel ID formats (WhatsApp/Telegram/Slack/Discord/Matrix/Teams/Zalo). |
| 5 | `oc_cli_dns.md` | procedure | dns.md: Setup, `dns setup` (options, what it shows, notes), Related | 300 | `openclaw dns setup` plans (or applies with `--apply`) CoreDNS configuration for unicast DNS-SD wide-area discovery over Tailscale; covers `--domain`, the recommended `openclaw.json`/Split-DNS output, and the macOS + Homebrew-CoreDNS apply path. |
| 6 | `oc_cli_docs.md` | procedure | docs.md: Usage, Examples, How it works, Output, Exit codes, Related | 360 | `openclaw docs [query...]` searches the live OpenClaw docs index from the terminal via the Cloudflare-hosted `/api/search` endpoint (30s timeout); covers rich-TTY vs Markdown output, the query-joining behavior, and exit codes 0/1. |
| 7 | `oc_cli_doctor.md` | procedure | doctor.md: Why Use It (3 postures), Examples, Options, Lint mode, Structured Health Checks, Check Selection, Post-upgrade mode, Notes, macOS launchctl env overrides, Related | 760 | `openclaw doctor` — health checks + guided repairs: the inspect/repair/lint postures, lint exit codes + JSON findings, the `detect()`/`repair()` structured-health-check contract, `--only`/`--skip` selection, `--post-upgrade` probes, and the launchctl env-override gotcha. |

Filenames derive from the slug with `/`→`_` and `-`→`_` (e.g. `cli/daemon` → `oc_cli_daemon.md`). All seven notes
are `building_block: procedure` (CLI command references).

## Section Coverage Map

```
daemon.md
├── Usage (install/start/stop/restart/uninstall/status) ──── → note 1 (oc_cli_daemon)
├── Subcommands (status/install/uninstall/start/stop/restart) → note 1
├── Common options (per-subcommand flags) ───────────────── → note 1
├── Prefer (use `openclaw gateway`) ─────────────────────── → note 1 (link-out, cl04 oc_cli_gateway)
└── Related ────────────────────────────────────────────── → note 1 (References)
dashboard.md
├── command + Notes (TLS, SecretRef, non-tokenized URL) ─── → note 2 (oc_cli_dashboard)
└── Related (web/dashboard) ─────────────────────────────── → note 2 (References)
devices.md
├── Commands › list / remove / clear ────────────────────── → note 3 (oc_cli_devices)
├── Commands › approve (+ autoApproveCidrs, upgrade) ────── → note 3
├── Paperclip / openclaw_gateway first-run approval ──────── → note 3
├── Commands › reject / rotate / revoke ─────────────────── → note 3
├── Common options ──────────────────────────────────────── → note 3
├── Notes (scope containment, self-only, --yes gate) ────── → note 3
├── Token drift recovery checklist (AUTH_*_MISMATCH) ────── → note 3
└── Related (web/dashboard, gateway/troubleshooting, nodes) → note 3 (References)
directory.md
├── Common flags (--channel/--account/--json) ───────────── → note 4 (oc_cli_directory)
├── Notes (config-backed, ID-finding aid) ───────────────── → note 4
├── Using results with `message send` ───────────────────── → note 4
├── ID formats (by channel) ─────────────────────────────── → note 4
├── Self / Peers / Groups ───────────────────────────────── → note 4
└── Related ─────────────────────────────────────────────── → note 4 (References)
dns.md
├── Setup (examples) ────────────────────────────────────── → note 5 (oc_cli_dns)
├── `dns setup` (options, what it shows, notes) ──────────── → note 5
└── Related (gateway/discovery) ─────────────────────────── → note 5 (References)
docs.md
├── Usage / Examples ────────────────────────────────────── → note 6 (oc_cli_docs)
├── How it works (Cloudflare /api/search, 30s) ──────────── → note 6
├── Output (rich TTY vs Markdown) ───────────────────────── → note 6
├── Exit codes (0/1) ────────────────────────────────────── → note 6
└── Related ─────────────────────────────────────────────── → note 6 (References)
doctor.md
├── Why Use It (3 postures table) ───────────────────────── → note 7 (oc_cli_doctor)
├── Examples ────────────────────────────────────────────── → note 7
├── Options ─────────────────────────────────────────────── → note 7
├── Lint mode (exit codes, JSON findings) ───────────────── → note 7
├── Structured Health Checks (detect/repair contract) ───── → note 7
├── Check Selection (--only/--skip) ─────────────────────── → note 7
├── Post-upgrade mode ───────────────────────────────────── → note 7
├── Notes (Nix, secrets, plugin/cron/model migrations) ──── → note 7
├── macOS: launchctl env overrides ──────────────────────── → note 7
└── Related (gateway/doctor, gateway/troubleshooting) ────── → note 7 (References)
```

No orphaned sections. All link-out targets (`/cli/gateway`, `/web/dashboard`, `/gateway/discovery`,
`/gateway/configuration`, `/gateway/troubleshooting`, `/gateway/doctor`, `/nodes`) are referenced/linked, not
duplicated — they live in other sub-plans (cl04, wb01, gw02, gw07, nd01/nd02) or are master pre-step targets.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages map 1:1 to a single note. `doctor.md` (2,354w / 8 code blocks) is the only page near a cap but stays **under** the 2,500-word and 6-code-block ceilings once distilled (Notes section is a long bullet list of repair behaviors that compresses to a compact summary; reference snippets reproduced selectively to ≤6). It is one coherent CLI command (single building_block: procedure), so fragmenting it would break the command-reference atomicity that the other `oc_cli_*` notes follow. |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (5,134 measured words). New `oc_` notes: **7**. New `term_dictionary` notes: **0** (expected).
- BB distribution: **procedure ×7** (all CLI command references). No model/concept/argument notes in this slice.
- Est. digest words ~3,320 (avg ~474/note); range 280 (dashboard) → 760 (doctor). 32 source code fences
  distribute across the 7 notes; each note kept ≤6 (devices' 14 + doctor's 8 fences reproduced selectively —
  representative command/JSON examples only, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21 — see Per-Note Related Notes Mapping): every note maps at the
  **RAISED floors of ≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under
  dashboard 10t·10s·10d, devices 12t·12s·11d, directory 9t·11s·11d, dns 10t·10s·11d, docs 10t·10s·11d,
  doctor 12t·12s·11d. Sibling `oc_cli_*` / `oc_*` in this and other sub-plans are marked "(planned)".

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> "(planned, this series)" / "(planned, <subplan>)". `entry_openclaw_docs.md` is a master W1 pre-step, marked
> "(planned, master pre-step)". Each rendered link in the executed note: `- [Name](relpath.md) — what it is;
> relevance: why THIS note`. Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms
> `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other-folder docs `../<folder>/<file>.md`;
> repos `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`; entry points
> `../../../0_entry_points/entry_Y.md`.

### oc_cli_daemon (10t · 11s · 12d)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product this CLI manages; relevance: `openclaw daemon` is the legacy service-control alias for this product.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed-secret resolution; relevance: `status`/`install` resolve `gateway.auth.token` SecretRefs for probe auth and fail closed when unresolved.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: drift checks resolve token/password/mode (`gateway.auth.mode`) before probing.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probing; relevance: `daemon status` probes Gateway health and reports `rpc.authWarning` on failure.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer-token auth; relevance: install validates the auth-token SecretRef is resolvable without persisting it into service env.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-retry semantics; relevance: install fails closed and `restart --safe` coalesces a single restart after active work drains.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential set; relevance: managed service environment loads auth-profile env refs through an owner-only wrapper rather than serializing them.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: `install --runtime <node|bun>` and supervised-service deployment context for the daemon.
- [Kill Tree](../../term_dictionary/term_kill_tree.md) — recursive process termination; relevance: stop/restart tears down the supervised service process tree (Windows schtasks PID kill-tree).
- [Cron](../../term_dictionary/term_cron.md) — scheduled-job runtime; relevance: headless daemon/service runs are the host for cron/Telegram non-TTY operation referenced by status/restart notes.

- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI command reference; relevance: closest-precedent CLI-command-reference format for an `oc_cli_*` note.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway service operations; relevance: analogous install/start/stop/restart service-lifecycle ops for a sibling coding-agent gateway.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — Hermes profile/gateway/service model; relevance: parallels the daemon-vs-gateway service abstraction and per-profile service control.
- [pi_containerization](../pi/pi_containerization.md) — Pi containerized deployment; relevance: cross-tool analog for running a coding-agent runtime as a supervised long-lived service.
- [cc_install](../claude_code/cc_install.md) — Claude Code install/service setup; relevance: install/runtime-selection precedent for `daemon install`.
- [cc_uninstall](../claude_code/cc_uninstall.md) — Claude Code uninstall; relevance: analog for `daemon uninstall` service removal.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — Hermes config precedence; relevance: explains env-source precedence the daemon's systemd `Environment=`/`EnvironmentFile=` drift checks mirror.
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — Hermes update/uninstall lifecycle; relevance: the update/remove half of the `daemon install`/`uninstall` service-lifecycle this command owns.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes container run modes; relevance: the supervised long-lived run mode `daemon`/`install --runtime` deploys the gateway as.
- [oc_cli_gateway](oc_cli_gateway.md) (planned, cl04) — the preferred current service command; relevance: daemon redirects operators to `openclaw gateway`.
- [oc_cli_status](oc_cli_status.md) (planned, cl07) — `openclaw status` health command; relevance: shares the probe/health surface `daemon status` exposes.
- [oc_cli_doctor](oc_cli_doctor.md) (planned, this series) — health/repair surface; relevance: doctor reports missing/stale gateway service definitions the daemon installs.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server implementation; relevance: the gateway service `daemon` is the legacy alias for.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/SecretRef code; relevance: the SecretRef/token-drift resolution behind status/install checks.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI surface; relevance: hosts the `daemon` command registration.

- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — macOS LaunchAgent plist rendering; relevance: implements `install` on macOS with owner-only plists.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: the `restart`/`restart --safe` coalesced-restart mechanism.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: Linux service install + `Environment=` parsing for drift checks.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger/env; relevance: merged-runtime-env source the token-drift check reads (`EnvironmentFile=`).
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — Windows schtasks argv render; relevance: the Windows service-install path for `daemon install`.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — Windows PID kill-tree; relevance: `stop`/`restart` process teardown on Windows.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — server shutdown; relevance: the `stop`/`restart` drain path.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth at startup; relevance: token/mode resolution install validates and status probes.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env assembly; relevance: the merged env (service env first, process env fallback) drift checks use.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the supervised-process lifecycle behind start/stop/restart.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: where the `daemon` subcommand surface is registered.

### oc_cli_dashboard (10t · 10s · 12d)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `dashboard` opens this product's Control UI.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed-secret resolution; relevance: resolves `gateway.auth.token` SecretRefs and prints a non-tokenized URL for SecretRef-managed tokens.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: follows `gateway.tls.enabled` to emit `https://` Control-UI URLs.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — certificate pinning; relevance: TLS-enabled Control UI client connections pin/verify the gateway identity.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the Control UI connects over `wss://`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: dashboard URL is token-authenticated using current auth.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: operator auth is required to open the Control UI.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: the fragment-key `token` and `OPENCLAW_GATEWAY_TOKEN` the safe manual-auth hint names.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential set; relevance: the configured auth source dashboard resolves to build the URL.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — credential store/rotation; relevance: SecretRef-managed credentials dashboard refuses to embed in terminal/clipboard output.

- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — Hermes web dashboard; relevance: direct analog of the Control UI this command opens.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes dashboard remote auth; relevance: parallels token/remote auth for opening the dashboard.
- [hermes_dashboard_rest_api](../hermes_agent/hermes_dashboard_rest_api.md) — Hermes dashboard REST API; relevance: cross-tool analog of the auth-gated dashboard backend.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code gateway/proxy + TLS config; relevance: TLS-following/https-vs-http parallel to `gateway.tls.enabled`.
- [cc_terminal_configuration](../claude_code/cc_terminal_configuration.md) — Claude Code terminal/clipboard behavior; relevance: analog for the clipboard/browser-launch delivery dashboard performs.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — Hermes model dashboard config; relevance: cross-tool dashboard surface using current auth.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: token-auth precedent for the dashboard URL token.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — Claude Code network TLS/access config; relevance: TLS-following / `https://`-vs-`http://` precedent for the Control-UI URL the dashboard emits per `gateway.tls.enabled` (and the client TLS-pinning path).
- [cc_analytics_dashboards](../claude_code/cc_analytics_dashboards.md) — Claude Code analytics dashboard; relevance: cross-tool web-dashboard UI surface analog for the Control UI dashboard opens.
- [cc_remote_control](../claude_code/cc_remote_control.md) — Claude Code remote control; relevance: opening an auth-gated remote control surface in a browser parallels the dashboard URL launch.
- [oc_web_dashboard](oc_web_dashboard.md) (planned, wb01) — the Control UI doc this command opens; relevance: same UI from the web-docs angle.
- [oc_web_control_ui](oc_web_control_ui.md) (planned, wb01) — Control UI reference; relevance: the UI surface the command launches.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server; relevance: serves the Control UI and the auth ticket.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app surfaces; relevance: the Control UI app the dashboard URL opens.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/secret handling; relevance: non-tokenized-URL / SecretRef-safe behavior.

- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: the token/ticket dashboard delivers to open the UI.
- [snippet_openclaw_gateway_control_ui_avatar_resolve](../../code_snippets/snippet_openclaw_gateway_control_ui_avatar_resolve.md) — Control-UI resource resolve; relevance: the Control UI rendering surface dashboard launches.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — TLS client identity; relevance: the TLS path behind `https://`/`wss://` URLs.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — gateway TLS pinning; relevance: the client-side TLS verification for TLS-enabled dashboards.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: the `wss://` connection the Control UI uses.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — kit gateway WS channel; relevance: client WS transport analog for the dashboard.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: the server endpoint the dashboard URL targets.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: resolves which auth the dashboard URL carries.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: SecretRef token resolution producing the non-tokenized-URL fallback.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/proxy; relevance: the connection path the dashboard URL initiates.

### oc_cli_devices (12t · 12s · 12d)

- [Device ID](../../term_dictionary/term_device_id.md) — per-device identifier; relevance: `<deviceId>` is the target for remove/rotate/revoke.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — direct-message pairing flow; relevance: `approve`/`reject`/`list` manage pairing requests.
- [Device Deregistration](../../term_dictionary/term_device_deregistration.md) — unpairing devices; relevance: `remove`/`clear` deregister paired devices.
- [Active Linked Device](../../term_dictionary/term_active_linked_device.md) — live paired session; relevance: paired-device token sessions are the self-only management subject.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: `operator.admin` vs `operator.pairing` scope gates cross-device management.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: rotated/revoked device tokens are returned and treated as secrets.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed-secret resolution; relevance: `gateway.auth.token` SecretRef source in the drift-recovery checklist.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `AUTH_TOKEN_MISMATCH`/`AUTH_SCOPE_MISMATCH` recovery is the checklist's purpose.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential set; relevance: reconnect auth precedence (shared token, then device token, then bootstrap) is the auth-profile resolution order.
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key auth exchange; relevance: device-key (ed25519) pairing is the public-key analog for device-bound auth.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: device-scoped tokens with operator scopes are the authorization model devices mints.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — credential store/rotation; relevance: rotate/revoke is per-role device-token rotation within the approved scope baseline.

- [hermes_api_server_setup_auth](../hermes_agent/hermes_api_server_setup_auth.md) — Hermes API auth setup; relevance: token-based device/client auth precedent.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes remote dashboard auth; relevance: the client-auth surface device-token drift breaks.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: token/credential management precedent for device tokens.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth troubleshooting; relevance: closest analog to the `AUTH_*_MISMATCH` token-drift recovery checklist.
- [band_contacts_and_discovery](../band/band_contacts_and_discovery.md) — Band contacts/discovery; relevance: paired-peer/device enrollment model for an agent mesh.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network errors; relevance: parallels the unauthorized/scope-mismatch failure recovery.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — Hermes OAuth-over-SSH; relevance: remote device-credential delivery analog.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — Hermes credential pools; relevance: the per-role credential store/rotation model behind device-token rotate/revoke.
- [band_agent_api_chats_participants](../band/band_agent_api_chats_participants.md) — Band participants API; relevance: the participant/device enrollment + listing surface `devices list` mirrors.
- [oc_cli_pairing](oc_cli_pairing.md) (planned, cl05) — the pairing command; relevance: shares the approve/reject pairing surface.
- [oc_cli_secrets](oc_cli_secrets.md) (planned, cl07) — secrets command; relevance: device tokens are secrets managed alongside SecretRefs.
- [oc_gateway_operator_scopes](oc_gateway_operator_scopes.md) (planned, gw04) — operator scope model; relevance: the scope-containment rules `devices` enforces at approval/rotate/revoke.

- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — pairing/auth/scope code; relevance: pairing approval + token rotation/revocation + scope containment.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server; relevance: the pairing RPCs and `autoApproveCidrs` policy.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/auth-profile code; relevance: credential resolution order / reconnect precedence.

- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing flow; relevance: the `role: node` approval and `autoApproveCidrs` path.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: the allowlist/approval policy behind pairing requests.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS client pairing; relevance: a client-side pairing request the operator approves.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: the reconnect auth-precedence in the recovery checklist notes.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth authorize dispatch; relevance: the scope/role authorization gating on approve/rotate/revoke.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method gating; relevance: enforces `operator.admin`/`operator.pairing` on device-management calls.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: emits `AUTH_TOKEN_MISMATCH`/`AUTH_SCOPE_MISMATCH` the checklist resolves.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: resolves the shared-token-vs-device-token precedence on reconnect.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: resolves `gateway.auth.token` for the drift checklist step 1.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — kit node session; relevance: a node device session created post-approval.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android device WS session; relevance: a paired device reconnecting with its stored device token.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit/install policy; relevance: install-time auth policy the device-pairing approvals operate under.

### oc_cli_directory (9t · 11s · 12d)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `directory` is an OpenClaw channel-lookup command.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-platform channel integration; relevance: directory results come from channel directory adapters (peers/groups/self).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel routing core; relevance: resolves the `--channel`/`--account` selection and per-channel ID formats.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: results are config-backed allowlists rather than a live provider directory.
- [Device ID](../../term_dictionary/term_device_id.md) — entity identifier; relevance: directory finds per-channel IDs (`user:U…`, `room:!…`) to paste into other commands.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound channel callback; relevance: channel adapters supplying directory data are webhook/transport-backed.
- [MCP](../../term_dictionary/term_mcp.md) — tool/context protocol; relevance: directory operations are tool-style channel lookups (`self`/`peers`/`groups`).
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — multi-platform message router; relevance: directory IDs feed `message send --target` through the messaging gateway.

- [band_contacts_and_discovery](../band/band_contacts_and_discovery.md) — Band contacts/discovery; relevance: direct analog of directory peers/contacts lookup.
- [band_agent_api_contacts_peers](../band/band_agent_api_contacts_peers.md) — Band contacts/peers API; relevance: the peers-list operation directory mirrors.
- [band_human_api_contacts_peers](../band/band_human_api_contacts_peers.md) — Band human contacts/peers; relevance: the self/peer ID resolution directory provides.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — Band rooms/routing; relevance: groups-list + per-channel room/group ID formats.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes messaging gateway; relevance: the multi-channel adapter model directory queries.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — Claude Code channels setup; relevance: cross-tool channel-config precedent for config-backed directory results.
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — Hermes Slack config; relevance: Slack `user:U…`/`channel:C…` ID-format analog.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack messaging; relevance: Slack peer/channel ID resolution and routing directory surfaces.
- [band_agent_api_chats_participants](../band/band_agent_api_chats_participants.md) — Band chats/participants API; relevance: the groups/participants listing analog directory exposes.
- [oc_cli_message](oc_cli_message.md) (planned, cl04) — `message send`; relevance: directly consumes directory IDs via `--target`.
- [oc_cli_channels](oc_cli_channels.md) (planned, cl01) — channels command; relevance: configures the channels directory lists.
- [oc_channels_groups](oc_channels_groups.md) (planned, ch02) — channel groups doc; relevance: the groups-directory concept directory surfaces.

- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels code; relevance: the directory adapters (peers/groups/self).
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: the per-channel ID formats directory reports.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension code; relevance: installed channel plugins that may omit directory support.

- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the directory-capability contract adapters implement or omit.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: resolving channel-specific IDs/threads directory exposes.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: `--query` filtering of peers/groups.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: `--channel` id/alias normalization.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist; relevance: the config-backed allowlist that backs directory results.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/routing; relevance: maps a directory ID to a send target for `message send`.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram dispatcher; relevance: Telegram `@username`/numeric-id formats directory reports.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket mode; relevance: Slack `user:U…`/`channel:C…` directory IDs.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: routes the `directory self/peers/groups` subcommands.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session/ID resolution; relevance: the ID-resolution pattern directory follows.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: where `directory` subcommands are registered.

### oc_cli_dns (10t · 10s · 12d)

- [DNS](../../term_dictionary/term_dns.md) — domain name system; relevance: the protocol `dns setup` configures (CoreDNS zone/Split-DNS).
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS/DNS-SD service discovery; relevance: unicast DNS-SD wide-area discovery the setup enables.
- [Service Discovery via VPN](../../term_dictionary/term_vpn.md) — overlay networking; relevance: discovery runs over the Tailscale tailnet substrate.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw dns` configures discovery for this product.
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: `--apply` targets Homebrew CoreDNS and restarts the brew service.
- [Route 53](../../term_dictionary/term_route53.md) — managed DNS service; relevance: cross-domain analog of the DNS-zone/nameserver configuration `dns setup` plans.
- [Health Check](../../term_dictionary/term_health_check.md) — readiness probing; relevance: discovery readiness context for the recommended config.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: `--apply` is sudo-gated (privileged service config).
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: wide-area-exposed gateways pair discovery with TLS for secure reach.
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — failure-isolation pattern; relevance: discovery/health degradation handling for unreachable wide-area peers.

- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — Band remote-agent connect; relevance: wide-area reach to a remote gateway/agent over a network substrate.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — Band agent-to-agent gateway; relevance: cross-host agent discovery/connectivity analog.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway ops; relevance: gateway networking/discovery operational context.
- [pi_containerization](../pi/pi_containerization.md) — Pi containerized deployment; relevance: wide-area-reachable deployment the discovery domain serves.
- [bedrock_agentcore_gateway_overview](../aws_bedrock_agentcore/bedrock_agentcore_gateway_overview.md) — AgentCore gateway overview; relevance: managed-gateway discovery/addressing analog.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — gateway/network config; relevance: network-reach config precedent for a coding-agent gateway.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway internals; relevance: the gateway networking/listen-address internals discovery advertises.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — Claude Code cloud network access; relevance: wide-area network-reach/addressing config precedent for a reachable gateway.
- [oc_gateway_discovery](oc_gateway_discovery.md) (planned, gw01) — discovery feature; relevance: the discovery this command configures.
- [oc_gateway_tailscale](oc_gateway_tailscale.md) (planned, gw06) — tailnet substrate; relevance: the Tailscale layer `dns setup` plans Split DNS for.
- [oc_gateway_configuration](oc_gateway_configuration.md) (planned, gw02) — gateway config reference; relevance: `discovery.wideArea.domain` the command reads.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server; relevance: discovery/wide-area config consumed via `openclaw.json`.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app surfaces; relevance: macOS app integration the `--apply` path targets.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security code; relevance: network-exposure considerations of wide-area discovery.

- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — mDNS/DNS-SD discovery; relevance: the DNS-SD discovery `dns setup` makes wide-area.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config plan; relevance: the plan-without-`--apply` planning-helper pattern.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config apply; relevance: the `--apply` install/update-and-restart path.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: the service-restart context `--apply` triggers (CoreDNS brew service).
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — gateway WS session; relevance: the wide-area-reachable session discovery enables.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — kit gateway WS; relevance: cross-host client connection over the discovered address.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/proxy; relevance: connecting to a wide-area-discovered gateway.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: the listen address discovery advertises.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: restarting the CoreDNS brew service on `--apply`.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: where the `dns setup` subcommand is registered.

### oc_cli_docs (10t · 10s · 12d)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `docs` searches this product's documentation index.
- [Internal Search](../../term_dictionary/term_internal_search.md) — full-text knowledge search; relevance: `docs` is terminal full-text search over the docs index.
- [Elasticsearch](../../term_dictionary/term_elasticsearch.md) — search engine; relevance: search-index analog for the hosted docs `/api/search`.
- [Inverted Index](../../term_dictionary/term_inverted_index.md) — full-text index structure; relevance: the index structure the docs search API queries.
- [BM25](../../term_dictionary/term_bm25.md) — lexical ranking function; relevance: the ranking model behind docs-index keyword results.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — hosted API front door; relevance: the Cloudflare-hosted `https://docs.openclaw.ai/api/search` endpoint the CLI calls.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-repeat semantics; relevance: a read-only query with a fixed 30s timeout, no state change.
- [Health Check](../../term_dictionary/term_health_check.md) — diagnostic surface; relevance: CLI exit-code 0/1 (success vs API-failure) is a diagnostic signal.
- [MCP](../../term_dictionary/term_mcp.md) — tool/context protocol; relevance: tool-style search invocation from the terminal.
- [Hybrid Search](../../term_dictionary/term_hybrid_search.md) — lexical+semantic retrieval; relevance: the retrieval-quality model docs-index search aims for.

- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI command reference; relevance: closest-precedent CLI-command-reference format.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — Hermes search/storage; relevance: full-text search-over-corpus analog in a sibling tool.
- [opensearch_semantic_search](../aws_opensearch/opensearch_semantic_search.md) — OpenSearch semantic search; relevance: the search-API/index concept the docs search calls.
- [bedrock_agentcore_gateway_semantic_search](../aws_bedrock_agentcore/bedrock_agentcore_gateway_semantic_search.md) — AgentCore gateway semantic tool search; relevance: hosted-search-endpoint analog for a CLI-invoked search.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI reference; relevance: cross-tool CLI command-surface precedent.
- [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — Claude Code tool search; relevance: tool-style search invocation analog.
- [cc_commands_reference](../claude_code/cc_commands_reference.md) — Claude Code commands reference; relevance: the command-index/help surface the no-query `docs` entrypoint and command catalog parallels.
- [hermes_tool_search](../hermes_agent/hermes_tool_search.md) — Hermes tool search; relevance: cross-tool search-invocation-over-an-index analog for the docs search.
- [oc_cli_help](oc_cli_help.md) (planned, cl04) — help command; relevance: the no-query `docs` entrypoint behaves like a help/usage print.
- [oc_cli](oc_cli.md) (planned, rt01) — CLI reference index; relevance: the command-index `docs` complements with live search.
- [oc_start_docs_directory](oc_start_docs_directory.md) (planned, st01) — docs-directory start page; relevance: the docs corpus `docs` searches.

- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI surface; relevance: hosts the `docs` command registration.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level repo; relevance: the repo/docs corpus the search indexes.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app surfaces; relevance: the hosted docs/search app the CLI calls.

- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: where the `docs` subcommand is registered.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: routes the `docs [query...]` command.
- [snippet_openclaw_cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — CLI main entry; relevance: the CLI bootstrap path that dispatches `docs`.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: argument parsing/joining for the multi-word query.
- [snippet_openclaw_memory_host_query_tokenizer](../../code_snippets/snippet_openclaw_memory_host_query_tokenizer.md) — query tokenizer; relevance: query-tokenization analog for full-text search.
- [snippet_openclaw_memory_host_query_lexica](../../code_snippets/snippet_openclaw_memory_host_query_lexica.md) — query lexica; relevance: lexical query handling analog for the docs index.
- [snippet_openclaw_memory_host_qmd_query_parser](../../code_snippets/snippet_openclaw_memory_host_qmd_query_parser.md) — query parser; relevance: parsing a free-form query into search terms.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory/search engine; relevance: the search-engine pattern the docs index embodies.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — HTTP loopback call; relevance: the HTTP-API call pattern (`/api/search`) the CLI makes.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root guard; relevance: CLI invocation guard around the `docs` command.

### oc_cli_doctor (12t · 12s · 12d)

- [Health Check](../../term_dictionary/term_health_check.md) — liveness/diagnostic surface; relevance: `doctor` IS the OpenClaw health surface.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: doctor inspects/repairs this product's gateway/channels/plugins/skills.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed-secret resolution; relevance: SecretRef checks and `--allow-exec` exec resolvers.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `--generate-gateway-token` and token/password drift checks.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — automation/preflight pipelines; relevance: `--lint` read-only CI/preflight posture with stable exit codes.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-repeat semantics; relevance: read-only lint vs repair postures, re-run-detect-after-repair.
- [Cron](../../term_dictionary/term_cron.md) — scheduled-job runtime; relevance: doctor scans `~/.openclaw/cron/jobs.json`, rewrites legacy cron shapes, flags model-override jobs.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — schedule syntax; relevance: the legacy cron-job shapes doctor migrates into SQLite.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin metadata; relevance: `--post-upgrade` plugin-compatibility probes and plugin-config repair.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin build surface; relevance: `openclaw/plugin-sdk/health` exposes the structured detect/repair contract.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — skill metadata; relevance: doctor's skills-readiness check (unavailable skills → `skills.entries.<skill>.enabled=false`).
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation runtime; relevance: doctor checks sandbox mode vs Docker availability and migrates legacy sandbox registry files.

- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway ops; relevance: gateway/service health + repair operations analog.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — Claude Code config debugging; relevance: closest analog to doctor's config-validation/repair findings.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: post-install/post-upgrade sanity-check analog.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network errors; relevance: the connectivity/auth-issue class doctor diagnoses and fixes.
- [cc_plugin_caching_and_troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin troubleshooting; relevance: the plugin-dependency/compatibility repair doctor performs.
- [bedrock_agentcore_gateway_advanced_debug](../aws_bedrock_agentcore/bedrock_agentcore_gateway_advanced_debug.md) — AgentCore gateway debug; relevance: structured-findings gateway diagnostics analog.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: the exec-SecretRef / `--allow-exec` security posture analog.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — Claude Code install-failures reference; relevance: the detect/repair failure-class catalog doctor's lint/repair postures resolve.
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — Hermes update/uninstall lifecycle; relevance: the `--post-upgrade` compatibility-repair posture doctor runs after updates.
- [oc_gateway_doctor](oc_gateway_doctor.md) (planned, gw02) — gateway-side doctor; relevance: the overlapping doctor doc this links, not duplicates.
- [oc_gateway_troubleshooting](oc_gateway_troubleshooting.md) (planned, gw07) — gateway troubleshooting; relevance: the troubleshooting surface doctor's Related points to.
- [oc_cli_health](oc_cli_health.md) (planned, cl04) — health command; relevance: the lighter-weight health probe doctor extends.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server; relevance: gateway/service health + repair.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/audit code; relevance: SecretRef/credential checks and command-owner warnings.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension code; relevance: plugin dependency staging + compatibility repair.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills code; relevance: the skills-readiness check.

- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor cron repair; relevance: the legacy-cron scan/rewrite doctor performs.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor memory-check preview; relevance: the memory-search readiness check doctor runs.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config plan/validate; relevance: config validation behind lint findings (e.g. `gateway.mode` unset).
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — security CLI surface; relevance: a security check surface doctor lint exercises.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security audit probe; relevance: the probe-execute pattern of doctor's structured detect().
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — security fix remediation; relevance: the repair()/`--fix` remediation contract.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolver; relevance: plugin-compatibility/trust checks in `--post-upgrade`.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability evaluator; relevance: the skills-readiness check that disables unavailable skills.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: SecretRef inspection (`--allow-exec` exec resolvers) doctor performs.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config/plugins; relevance: plugin-config quarantine/repair doctor applies.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: the plugin staging/relink repair doctor cleans up.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service notifications; relevance: the cron-job model-override reporting doctor surfaces.

> **Term-floor note**: `term_command_line_interface` / `term_cli_wizard` are NOT in the DB (verified MISSING).
> by relevance — no padding). The single shared anti-island inbound link for every note is
> `entry_openclaw_docs.md` (planned, master pre-step W1).

## Undigested Terms Plan

Per master: OpenClaw CLI vocabulary is digested as `oc_*` doc notes (the commands ARE the subjects), and the only
`term_dictionary` interaction is LINKING existing terms. Expected **0 new `term_dictionary` captures**.

| Term (appears in source) | Disposition |
|---|---|
| `daemon` / `gateway service` | → note 1 (`oc_cli_daemon`); concept lives in the doc note; link `term_openclaw`, `repo_openclaw_gateway`. NOT a new term. |
| `Control UI` / `dashboard` | → note 2 (`oc_cli_dashboard`) + planned `oc_web_dashboard`; link existing. NOT a new term. |
| `device pairing` / `device token` | → note 3 (`oc_cli_devices`); link existing `term_dm_pairing`, `term_device_id`, `term_device_deregistration`, `term_active_linked_device`. NOT new. |
| `operator scopes` (`operator.admin`/`operator.pairing`/`operator.read`/`operator.write`) | concept owned by `gateway/operator-scopes` (gw04, planned) → link planned `oc_gateway_operator_scopes`; link existing `term_access_control`. NOT a new term here. |
| `SecretRef` | cross-cutting OpenClaw config token; owned by gateway/reference sub-plans → link existing `term_secrets_manager`. NOT a new term. |
| `token drift` / `AUTH_*_MISMATCH` | → note 3 recovery checklist; link `term_authentication`. NOT a new term. |
| `directory` (channels) / `peers`/`groups`/`me` | → note 4 (`oc_cli_directory`); link `repo_openclaw_channels`. NOT new. |
| `wide-area discovery` / `DNS-SD` / `CoreDNS` / `Split DNS` | → note 5 (`oc_cli_dns`); link existing `term_dns`, `term_bonjour_discovery`, `term_homebrew`. NOT new. |
| `live docs search` (`/api/search`) | → note 6 (`oc_cli_docs`); link `term_internal_search`, `term_api_gateway`. NOT new. |
| `doctor` postures (inspect/repair/lint) / `HealthFinding` / `detect`/`repair` | → note 7 (`oc_cli_doctor`); link existing `term_health_check`, `term_ci_cd`. NOT new. |

**New-term candidates**: none. No genuinely reusable cross-cutting term with no doc-page home AND no existing
note appears in these 7 CLI reference pages. If augment's Step 2d re-scan surfaces one, capture via
`/tessellum-capture-term-note` + add to the best-fit glossary (`acronym_glossary_a.md` for agentic/AI-dev terms);
not expected.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — cl03 authors zero `term_dictionary` notes. The multi-source-research term-authoring
mandate (inherited from master) does not apply this sub-plan. Existing terms are linked only.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). Gate table inherited verbatim from the master 9-GATE:

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` pass on all 7 notes (YAML field order, `## Overview` + `## Related Notes`, footer). |
| G2 | Grounding | Each note's claims diff-checked against `inbox/openclaw_docs/cli/<page>.md` (no invented flags/behaviors). |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2500 words / ≤6 code blocks, single BB; every source H2/H3 mapped (Section Coverage Map). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` clean after incremental reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks); in-degree ≥1, anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

All must pass before commit.

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_daemon oc_cli_dashboard oc_cli_devices oc_cli_directory oc_cli_dns oc_cli_docs oc_cli_doctor"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # required source_url
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density caps (body words excl. frontmatter; code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb}cb)"
  # sibling-link presence (≥1 oc_ link)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING LINK in $n"
done

# YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# DB-verify a cited existing note before listing it (run per id during augment lock):
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (src/kept) | Within caps? |
|---|---|---|---:|---|---|
| 1 | oc_cli_daemon | procedure | 480 | 1 / ≤1 | ✅ |
| 2 | oc_cli_dashboard | procedure | 280 | 1 / ≤1 | ✅ |
| 3 | oc_cli_devices | procedure | 720 | 14 / ≤6 (selective) | ✅ |
| 4 | oc_cli_directory | procedure | 420 | 4 / ≤4 | ✅ |
| 5 | oc_cli_dns | procedure | 300 | 1 / ≤1 | ✅ |
| 6 | oc_cli_docs | procedure | 360 | 3 / ≤3 | ✅ |
| 7 | oc_cli_doctor | procedure | 760 | 8 / ≤6 (selective) | ✅ |

No note approaches the 400-line / 2,500-word ceiling. The two code-heavy pages (`devices` 14 fences, `doctor`
8 fences) reproduce only representative command/JSON examples verbatim to stay ≤6 code blocks each.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (CREATED as the master W1 pre-step before any sub-plan
executes; `building_block: navigation`) under the **CLI (cl03)** cluster — one row per note (`oc_cli_daemon`,
`oc_cli_dashboard`, `oc_cli_devices`, `oc_cli_directory`, `oc_cli_dns`, `oc_cli_docs`, `oc_cli_doctor`). Each note
gets the entry-point back-link at finalization. Master W2/W3 (parent hub `entry_gen_ai_dev.md`,
re-done per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (satisfy G7/G8; DB-verify at execution):

- `entry_openclaw_docs.md` (planned, master pre-step) → **all 7** notes (primary anti-island inbound).
- `repo_openclaw_gateway` → notes 1, 2, 5, 7 (service/dashboard/discovery/doctor).
- `repo_openclaw_security` → notes 1, 3, 7 (auth/SecretRef, device tokens, doctor checks).
- `repo_openclaw_channels` → note 4 (directory adapters).
- `repo_openclaw_cli_wizard` → notes 1, 6 (CLI command surface).
- `term_health_check` → notes 1, 7; `term_dns`/`term_bonjour_discovery` → note 5; `term_dm_pairing`/`term_device_id` → note 3; `term_secrets_manager` → notes 1, 2, 3, 7.

Reciprocal inlinks added at execution (each new note's `## Related Notes` links back to the repo/term/sibling).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page at execution; reproduce command/config
examples verbatim; one BB per note. Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the
script; reindex incrementally per wave and verify `note_links` + 0 broken links before commit. `git pull --rebase
--autostash` first; commit+push after the phase; no Claude co-author trailer.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref locked at raised floors; see Augmentation Report) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** (see Review Sign-Off) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augmentation**: locked the Per-Note Related Notes Mapping at the RAISED cross-reference floors
prior `## Candidate Cross-References` (which was at the master ≥6-term floor). All cited EXISTING note_ids were
excluded (selection is relevance-driven, no padding).

**Per-note locked counts** (terms / snippets / docs; floors all met):

| Note | Terms | Snippets | Docs (existing-verified / total) | Repos | Floors met (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_cli_daemon | 10 | 11 | 7 / 11 | 3 | ✅ |
| oc_cli_dashboard | 10 | 10 | 7 / 10 | 3 | ✅ |
| oc_cli_devices | 12 | 12 | 8 / 11 | 3 | ✅ |
| oc_cli_directory | 9 | 11 | 7 / 11 | 3 | ✅ |
| oc_cli_dns | 10 | 10 | 7 / 11 | 3 | ✅ |
| oc_cli_docs | 10 | 10 | 7 / 11 | 3 | ✅ |
| oc_cli_doctor | 12 | 12 | 7 / 11 | 4 | ✅ |


**Ghosts / corrections**: `term_command_line_interface` and `term_cli_wizard` were cited in the prior draft's
`oc_cli_docs` row but are NOT in the DB (verified MISSING). They are DROPPED; the `oc_cli_docs` term floor is now

**New-term candidate**: **none.** The re-read (augment Step 2d) surfaced no genuinely reusable cross-cutting term
lacking both a doc-page home and an existing vault note. Source vocabulary (`daemon`, `Control UI`, `device
pairing`, `SecretRef`, `wide-area discovery`/`DNS-SD`/`CoreDNS`, `live docs search`, `doctor` postures, `HealthFinding`)
is digested as `oc_*` doc notes (the commands ARE the subjects) and/or covered by EXISTING terms. Best-fit glossary
if one were ever needed: `acronym_glossary_a.md` (agentic/AI-dev terms). Consistent with the master Undigested-Terms
design decision and the Pattern-B `claude_code`/`pi` precedents: expected 0 new `term_dictionary` captures — confirmed 0.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 checkpoints. Plan status was `pending` at review start.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (min 9 at directory), ≥10 snippets, ≥10 docs; each link carries `— what it is; relevance: …`. No bare links. |
| CP2 | 9-GATE present per batch (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table has G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (raised floors), G5 Ghost-detect+redirect, G6 Broken-link fix, G7/G8 Discoverability. Single phase (7 notes), one gate table = covers it. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 7 rows to `entry_openclaw_docs.md` (CREATED master W1 pre-step, `building_block: navigation`); every note lists it as the primary inbound link in the mapping. Size-rule satisfied (665-page/~1,053-note series ⇒ CREATE required, done at master). |
| CP4 | Size | **PASS** | 7 planned notes (≤30); no split needed. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master Format Definition, which was derived from existing `claude_code/` `cc_*` + `pi/` `pi_*` doc notes (`## Overview` + `## Related Notes` + bold `**Source**`/`**Last Updated**`/`**Status**` footer; not invented). Forbidden-field list present in master. |
| CP6 | Density | **PASS** | `## Density Re-Assessment`: all 7 notes 280–760 words, ≤6 code blocks (devices 14→≤6, doctor 8→≤6 selective); none near the 400-line/2,500-word ceiling. doctor (2,354w source) kept as one coherent BB under cap. |
| CP7 | Sources measured | **PASS** | All 7 pages re-read from `inbox/openclaw_docs/cli/` during this augment; measured words (daemon 546, dashboard 168, devices 1,243, directory 325, dns 210, docs 288, doctor 2,354 = 5,134) match the Source table; doctor 2,354w is the only large page and stays under the 2,500 cap. No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (10-row disposition table, all → link existing / owned by planned doc note); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherited mandate noted). New-term candidates: none. |
| CP8f | Slug/collision audit | **PASS** | 0 new `term_*` slugs to audit (all term refs are EXISTING vault terms). Collision audit on planned `oc_cli_*` doc slugs vs existing term/doc notes: no duplication of an existing substantive note (the 295 OpenClaw CODE-side notes are repos/snippets, not `oc_cli_*` doc notes; the `oc_cli_*` doc namespace is new). 2 cited-but-missing terms dropped (see Augmentation Report). |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks (existing notes → new notes)` maps `entry_openclaw_docs.md` → all 7 (primary anti-island), plus `repo_openclaw_*` and `term_*` outside-folder inbound links per note; G7/G8 in the gate table; in-degree ≥1 for every note. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
