---
title: Sub-Plan pf02 — OpenClaw Docs: Platforms (macOS App — Lifecycle, Dev, Health, UI, Logging)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["platforms/mac/child-process", "platforms/mac/dev-setup", "platforms/mac/health", "platforms/mac/icon", "platforms/mac/logging", "platforms/mac/menu-bar"]
---

# Sub-Plan pf02: Platforms

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`) / format (YAML field order, `## Overview` … `## Related Notes` … `## References`) / dedup (3-way across term_dictionary + documentation + repo_openclaw*) / 9-GATE / cross-ref / entry-point decisions are ALL inherited from the master — not restated. This file adds only what is specific to the 6 assigned macOS-platform pages.

## Scope

These 6 pages document the **OpenClaw macOS desktop app** (`apps/macos`): how it manages the Gateway
lifecycle (launchd vs attach/remote/child-process), how a developer builds/runs it from source, how it
surfaces channel/Gateway health, the menu-bar status UI and animated icon state model, and how to capture
macOS logs (rolling diagnostics file + unified-logging private-data flag). All are macOS-app-specific
operational/UI references — the mac client side of the OpenClaw gateway. **Priority P2 (Phase B)** — these
reference the architecture/gateway/CLI vocabulary defined by the Phase-A sub-plans (concepts, gateway, CLI,
install), so they digest after that core. The code-side counterpart `repo_openclaw_apps` (the desktop apps)
and the `snippet_openclaw_macos_*` snippets are LINKED, not recreated.

**Source**: OpenClaw docs, 6 pages, 2,236 measured words. **Planned: 6 notes (1:1, no splits).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| child-process | platforms/mac/child-process | 350 | 2 | 6 | 0 | procedure |
| dev-setup | platforms/mac/dev-setup | 435 | 6 | 6 | 3 | procedure |
| health | platforms/mac/health | 238 | 0 | 5 | 0 | procedure |
| icon | platforms/mac/icon | 291 | 0 | 1 | 0 | model |
| logging | platforms/mac/logging | 347 | 1 | 5 | 0 | procedure |
| menu-bar | platforms/mac/menu-bar | 575 | 0 | 9 | 2 | model |

Notes on counts: H2/H3 include the trailing `## Related` link block on every page (mapped to `## Related
Notes`, not a body section). Code-block counts are raw ```` ``` ```` fences ÷ 2. `icon.md` has only the
`## Related` H2 — its body is a bullet/prose enum under the page H1 (`# Menu Bar Icon States`); it is a
state-model reference, captured as one note. `menu-bar.md` is the largest (575w) but stays well under the
2,500w cap, so it remains a single note.

## Content Strategy

- **Prioritize**: the **Gateway-lifecycle decision** (child-process.md — launchd default vs attach-only vs
  remote vs child-process modes; this is the load-bearing operational model for the mac app) and the
  **menu-bar status/icon state models** (menu-bar.md + icon.md — the event-driven IconState/ActivityKind
  taxonomy the UI renders), since these are the conceptual cores other mac pages reference.
- **1 note per page (no splits)**: every page is < 600 words and single-BB; none approaches the 2,500w /
  6-code-block caps. Splitting would create sub-atomic fragments — disallowed by the master density rules.
- **Keep BB clean**: child-process / dev-setup / health / logging are **procedure** notes (do-X steps,
  commands, settings paths); icon / menu-bar are **model** notes (state enums + visual/state mappings, not
  a procedure). One `building_block` per note.
- **Link-out, don't duplicate**: the generic macOS-app page (`platforms/macos`) is owned by **pf04**
  (`platforms/macos`); the Gateway runbook / Gateway health / Gateway logging targets (`/gateway`,
  `/gateway/health`, `/gateway/logging`) are owned by **gw01–gw07** — referenced as planned siblings /
  External References, never re-digested here. Voice-wake mechanics (icon "big ears") link to the voice/wake
  pages owned by **nd02** (`nodes/voicewake`) and **pf04** (`platforms/mac/voicewake`); `launchd`/CLI
  background-process details link to the install/CLI sub-plans. No `term_dictionary` definition is inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_platforms_mac_child_process.md` | procedure | child-process.md: intro, Default behavior (launchd), Unsigned dev builds, Attach-only mode, Remote mode, Why we prefer launchd | 420 | How the macOS app manages the Gateway lifecycle: launchd `ai.openclaw.gateway` LaunchAgent is the default (attach-then-start), with `--no-sign` dev-build override, attach-only (`--attach-only`/`--no-launchd`) and remote (SSH-tunnel) modes; child-process spawning is not in use. |
| 2 | `oc_platforms_mac_dev_setup.md` | procedure | dev-setup.md: Prerequisites, 1. Install Dependencies, 2. Build and Package the App, 3. Install the CLI, Troubleshooting (toolchain/SDK, TCC permission crash, gateway stuck "Starting...") | 460 | Building/running the OpenClaw macOS app from source: Xcode 26.2 + Node/pnpm prerequisites, `pnpm install`, `package-mac-app.sh` (ad-hoc signing), installing the global `openclaw` CLI, and three troubleshooting recipes (SDK mismatch, TCC reset, zombie-port). |
| 3 | `oc_platforms_mac_health.md` | procedure | health.md: intro, Menu bar (status dot), Settings (Health card, Channels tab), How the probe works (`openclaw health --json` via ShellExecutor ~60s), When in doubt (CLI fallback) | 300 | How the macOS app reports linked-channel/Baileys health: menu-bar status-dot colors + secondary line, the General-tab Health card and Channels-tab controls, the periodic `openclaw health --json` probe with cached snapshot, and the CLI fallback flow. |
| 4 | `oc_platforms_mac_icon.md` | model | icon.md: Idle/Paused/Voice-trigger/Working states, Wiring points, Shapes & sizes, Behavioral notes | 320 | The menu-bar critter-icon **state model** and animations: idle blink/wiggle, paused (`appearsDisabled`), voice-trigger "big ears" (`triggerVoiceEars`/`stopVoiceEars`, earScale 1.9), and working scurry (`isWorking`), plus the `CritterIconRenderer` wiring/sizing and short-TTL guidance. |
| 5 | `oc_platforms_mac_logging.md` | procedure | logging.md: Rolling diagnostics file log (Debug pane), Unified logging private data on macOS, Enable for OpenClaw (`ai.openclaw` plist), Disable after debugging | 360 | Capturing macOS app logs: the off-by-default rolling JSONL diagnostics file (`~/Library/Logs/OpenClaw/diagnostics.jsonl`) and the unified-logging private-data override (install/remove the `ai.openclaw` Subsystems plist) — including the sensitivity warning that private payloads can include phone numbers / message bodies. |
| 6 | `oc_platforms_mac_menu_bar.md` | model | menu-bar.md: What is shown, State model (sessions/priority/activity kinds), IconState enum (ActivityKind→glyph, Visual mapping), Context submenu, Status row text, Event ingestion, Debug override, Testing checklist | 520 | The menu-bar status **state model**: what is surfaced (work state, Context/Nodes/Usage), the session priority/activity-kind model, the `IconState` enum + ActivityKind→glyph/visual mapping, Context submenu, status-row text, control-channel `agent` event ingestion, the debug icon-override, and the testing checklist. |

Filename rule applied (master Step-6): `oc_` + full slug with `/` and `-` → `_` (e.g.
`platforms/mac/child-process` → `oc_platforms_mac_child_process.md`). No split-aspect suffixes (no splits).

## Section Coverage Map

```
platforms/mac/child-process.md
├── (intro: launchd-managed, attach-first) ───────────── → note 1 (oc_platforms_mac_child_process)
├── ## Default behavior (launchd) ───────────────────── → note 1
├── ## Unsigned dev builds ──────────────────────────── → note 1
├── ## Attach-only mode ─────────────────────────────── → note 1
├── ## Remote mode ──────────────────────────────────── → note 1
├── ## Why we prefer launchd ────────────────────────── → note 1
└── ## Related (links) ──────────────────────────────── → note 1 ## Related Notes

platforms/mac/dev-setup.md
├── # macOS developer setup (intro) ─────────────────── → note 2 (oc_platforms_mac_dev_setup)
├── ## Prerequisites ────────────────────────────────── → note 2
├── ## 1. Install Dependencies ──────────────────────── → note 2
├── ## 2. Build and Package the App ─────────────────── → note 2
├── ## 3. Install the CLI ───────────────────────────── → note 2
├── ## Troubleshooting ──────────────────────────────── → note 2
│   ├── ### Build fails: toolchain or SDK mismatch ──── → note 2
│   ├── ### App crashes on permission grant ─────────── → note 2
│   └── ### Gateway "Starting..." indefinitely ──────── → note 2
└── ## Related (links) ──────────────────────────────── → note 2 ## Related Notes

platforms/mac/health.md
├── # Health Checks on macOS (intro) ────────────────── → note 3 (oc_platforms_mac_health)
├── ## Menu bar ─────────────────────────────────────── → note 3
├── ## Settings ─────────────────────────────────────── → note 3
├── ## How the probe works ──────────────────────────── → note 3
├── ## When in doubt ────────────────────────────────── → note 3
└── ## Related (links) ──────────────────────────────── → note 3 ## Related Notes

platforms/mac/icon.md
├── # Menu Bar Icon States (Idle/Paused/Voice/Working) → note 4 (oc_platforms_mac_icon)
├── (Wiring points) ─────────────────────────────────── → note 4
├── (Shapes & sizes) ────────────────────────────────── → note 4
├── (Behavioral notes) ──────────────────────────────── → note 4
└── ## Related (links) ──────────────────────────────── → note 4 ## Related Notes

platforms/mac/logging.md
├── # Logging (macOS) ───────────────────────────────── → note 5 (oc_platforms_mac_logging)
├── ## Rolling diagnostics file log (Debug pane) ────── → note 5
├── ## Unified logging private data on macOS ────────── → note 5
├── ## Enable for OpenClaw (`ai.openclaw`) ──────────── → note 5
├── ## Disable after debugging ──────────────────────── → note 5
└── ## Related (links) ──────────────────────────────── → note 5 ## Related Notes

platforms/mac/menu-bar.md
├── ## What is shown ────────────────────────────────── → note 6 (oc_platforms_mac_menu_bar)
├── ## State model ──────────────────────────────────── → note 6
├── ## IconState enum (Swift) ───────────────────────── → note 6
│   ├── ### ActivityKind → glyph ────────────────────── → note 6
│   └── ### Visual mapping ───────────────────────────── → note 6
├── ## Context submenu ──────────────────────────────── → note 6
├── ## Status row text (menu) ───────────────────────── → note 6
├── ## Event ingestion ──────────────────────────────── → note 6
├── ## Debug override ───────────────────────────────── → note 6
├── ## Testing checklist ────────────────────────────── → note 6
└── ## Related (links) ──────────────────────────────── → note 6 ## Related Notes
```
No orphaned sections. The `## Related` link blocks become each note's `## Related Notes`; their external
targets (`/platforms/macos`, `/gateway`, `/gateway/health`, `/gateway/logging`, `/platforms/mac/menu-bar`,
`/platforms/mac/icon`) map to planned-sibling `oc_*` notes (this/other sub-plans) or External References,
not re-digested content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 6 pages are ≤575 words and single-BB; none nears the 2,500w / 6-code-block caps. 1 note per page; splitting would produce sub-atomic fragments. |

## Summary Statistics & Building Block Distribution

- Source pages: **6** (2,236 measured words total; range 238–575). New `oc_*` notes: **6** (1:1).
  New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×4** (notes 1, 2, 3, 5) · **model ×2** (notes 4, 6). No argument/concept
  notes (these pages are operational/UI reference, not design rationale or first-principles concepts).
- Est. digest words ~2,380 (avg ~395/note); all notes ≤520w. Source code fences (9 total, mostly in
  dev-setup.md) distribute into notes 1/2/5; each note kept ≤6 code blocks (verbatim shell/plist snippets
  reproduced selectively).
- Cross-refs (LOCKED at xref-augment 2026-06-21): each note maps **≥8 relevancy-selected `term_dictionary`
  terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (≥5 of the 10 docs EXISTING +
  series)"), PLUS relevant `repo_openclaw*`. ALL cited snippets and all non-planned terms/docs/repos are
  per-note mapping is in `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard (raised floors):** **≥8 terms · ≥10 snippets · ≥10 docs per note**, relevance-selected,
> 2026-06-21); sibling `oc_*` of this/other OpenClaw sub-plans are "(planned, this series)" / "(planned, <sp>)"
> and count toward the 10-doc floor. Relative paths are from a note at `resources/documentation/openclaw/`:
> term → `../../term_dictionary/`, sibling `oc_*` → same dir, other doc → `../<folder>/`, snippet →
> `../../code_snippets/`, repo → `../../../areas/code_repos/`.

### oc_platforms_mac_child_process (10t · 11s · 11d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: this page is the macOS app's piece of OpenClaw's gateway-lifecycle story.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — runtime that drives an LLM coding agent; relevance: the Gateway being launched/attached is the harness backing the mac app.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled/managed-service mechanism; relevance: launchd LaunchAgent (`ai.openclaw.gateway`) is the macOS scheduled-service analog driving auto-start.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — components react to events; relevance: launchd KeepAlive restarts the Gateway on crash (event-driven supervision).
- [term_failover](../../term_dictionary/term_failover.md) — automatic switch to standby on failure; relevance: launchd's "restart on crashes" / KeepAlive is the local high-availability failover the page prefers.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: the app "first tries to attach to an already-running Gateway" — an attach/reachability probe before starting one.
- [term_kill_tree](../../term_dictionary/term_kill_tree.md) — terminate a process plus all descendants; relevance: `launchctl bootout` / not-spawning-as-child contrasts with child-process supervision that would need kill-tree cleanup.
- [term_remote_ssh](../../term_dictionary/term_remote_ssh.md) — operating a remote host over SSH; relevance: Remote mode uses an SSH tunnel to a remote host and never starts a local Gateway.
- [term_ssh](../../term_dictionary/term_ssh.md) — secure shell tunneling; relevance: the SSH tunnel transport behind Remote mode.
- [term_agent_lifecycle_event](../../term_dictionary/term_agent_lifecycle_event.md) — signal of an agent state transition; relevance: load/start/bootout transitions of the Gateway service are lifecycle events the app drives.

**Docs**
- [oc_platforms_mac_dev_setup](oc_platforms_mac_dev_setup.md) — (planned, this series) `--no-sign` dev build / `disable-launchagent` override; relevance: sibling that documents the unsigned-build escape hatch referenced here.
- [oc_platforms_mac_health](oc_platforms_mac_health.md) — (planned, this series) attach/health probe; relevance: the attach-then-probe flow before starting the Gateway.
- [oc_platforms_mac_logging](oc_platforms_mac_logging.md) — (planned, this series) launchd gateway log path; relevance: "Logs are written to the launchd gateway log path (visible in Debug Settings)".
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, pf04) generic macOS app; relevance: parent macOS-app reference this lifecycle page sits under.
- [oc_gateway](oc_gateway.md) — (planned, rt02/gw) Gateway runbook; relevance: the `## Related` link target for managing the Gateway itself.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway start/stop/restart operations; relevance: sibling coding-agent gateway-lifecycle operations (cross-stack analog).
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — per-profile gateway services; relevance: `ai.openclaw.<profile>` per-profile LaunchAgent labeling parallels Hermes profile-scoped services.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — container supervision/restart; relevance: supervisor/restart-on-crash analog to launchd KeepAlive on another platform.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting an agent session as a background process; relevance: the "run the Gateway as a managed background process" pattern from a sibling tool.
- [band_agent_lifecycle](../band/band_agent_lifecycle.md) — agent start/stop/restart lifecycle states; relevance: vocabulary for the attach/start/remote lifecycle modes.
- [pi_development](../pi/pi_development.md) — Pi coding-agent dev/run modes; relevance: cross-stack "run the agent manually in a terminal vs managed service" framing the page's child-process fallback echoes.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS desktop app code home; relevance: the app that installs/manages the `ai.openclaw.gateway` LaunchAgent.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway runtime; relevance: the process being attached-to / launched / supervised.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the external `openclaw` CLI; relevance: the app enables the launchd service "via the external `openclaw` CLI (no embedded runtime)".

**Snippets**
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — renders the LaunchAgent plist; relevance: produces the `ai.openclaw.gateway` plist this page's default behavior installs.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — KeepAlive/restart handoff; relevance: the "built-in restart/KeepAlive semantics" the page cites for preferring launchd.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: cross-platform supervision analog to the macOS LaunchAgent.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger/auto-start env; relevance: "auto-start at login" analog on Linux.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — PID kill-tree on Windows; relevance: the descendant-process teardown a real child-process mode would need (page defers it).
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the supervision layer launchd replaces for the mac app.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap entry; relevance: the `openclaw` CLI bootstrap that enables the launchd service.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — post-attach runtime startup; relevance: what runs once the app attaches to an existing Gateway.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — gateway shutdown impl; relevance: `launchctl bootout` / stop path for the managed Gateway.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — Hermes gateway lifecycle CLI; relevance: attach/start/stop lifecycle analog on a sibling stack.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — Hermes systemd gateway integration; relevance: the systemd counterpart of macOS launchd-managed gateway.

### oc_platforms_mac_dev_setup (8t · 10s · 11d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway/agent platform; relevance: this is how to build/run its macOS app from source.
- [term_npm](../../term_dictionary/term_npm.md) — Node package manager / global installs; relevance: `npm/pnpm/bun install -g openclaw@<version>` installs the global CLI in Step 3.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — coding-agent runtime; relevance: the Gateway runtime built/started during setup and troubleshooting.
- [term_health_check](../../term_dictionary/term_health_check.md) — status probe; relevance: troubleshooting uses `openclaw gateway status` to detect a stuck "Starting..." gateway.
- [term_authentication](../../term_dictionary/term_authentication.md) — verifying identity/permissions; relevance: the TCC permission grant (Speech Recognition / Microphone) and signature checks.
- [term_pii](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: TCC governs privacy-scoped permissions (mic/speech) the dev build must grant.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled/managed service; relevance: the LaunchAgent the dev-build setup may disable via `--no-sign`.
- [term_kill_tree](../../term_dictionary/term_kill_tree.md) — kill a process and descendants; relevance: the zombie-port troubleshooting (`lsof -iTCP:18789`, stop/kill the listener PID).

**Docs**
- [oc_platforms_mac_child_process](oc_platforms_mac_child_process.md) — (planned, this series) launchd / `--no-sign` / disable-launchagent; relevance: the lifecycle override the dev build relies on.
- [oc_platforms_mac_logging](oc_platforms_mac_logging.md) — (planned, this series) capturing logs while debugging; relevance: enable diagnostics while a dev build misbehaves.
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, pf04) generic macOS app; relevance: parent macOS-app page this dev-setup belongs under.
- [oc_install](oc_install.md) — (planned, rt02/in) install overview; relevance: the `## Related` "Install overview" link target.
- [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — reproducible build-from-source dev environment; relevance: closest sibling-tool "build/run from source" setup analog.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install + toolchain/version verification; relevance: the `xcodebuild -version` / `xcrun swift --version` SDK-match checks parallel this.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — diagnosing install failures; relevance: the three troubleshooting recipes (SDK mismatch, TCC crash, zombie-port) mirror install-failure diagnosis.
- [cc_sandboxed_bash_tool_setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — local toolchain/shell setup; relevance: shell-command setup steps (`pnpm install`, package script) analog.
- [hermes_contributing_dev_setup](../hermes_agent/hermes_contributing_dev_setup.md) — contributor build-from-source setup; relevance: sibling coding-agent's dev-environment prerequisites + build steps.
- [hermes_installation](../hermes_agent/hermes_installation.md) — Hermes install (deps, CLI, runtime); relevance: parallel prerequisites + global-CLI install flow.
- [pi_development](../pi/pi_development.md) — Pi coding-agent development setup; relevance: cross-stack dev-setup precedent for build/run-from-source.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the Swift macOS app; relevance: the `apps/macos` codebase being built and packaged.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the `openclaw` CLI; relevance: the global CLI installed in Step 3 ("Install CLI").
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway runtime; relevance: started via the CLI during the "Starting..." troubleshooting.

**Snippets**
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: entry point of the global `openclaw` CLI this page installs.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — LaunchAgent plist render; relevance: the launchd binding `--no-sign` writes `disable-launchagent` to bypass.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the supervisor managing the Gateway dev build.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway HTTP/WS listener bind; relevance: the port (`:18789`) the zombie-port troubleshooting frees with `lsof`.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — gateway shutdown; relevance: `openclaw gateway stop` path in the stuck-startup recipe.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — PID kill-tree; relevance: "kill the PID you found above" last-resort step analog.
- [snippet_hermes_agent_cli_gateway_pid_discovery](../../code_snippets/snippet_hermes_agent_cli_gateway_pid_discovery.md) — discover gateway PID; relevance: the `lsof -iTCP:18789 -sTCP:LISTEN` listener-discovery analog.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway start/stop lifecycle CLI; relevance: `openclaw gateway status/stop` lifecycle commands analog.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — doctor/connectivity check; relevance: a sibling "doctor"-style verification for a misbehaving install.
- [snippet_hermes_agent_lsp_manager_lifecycle](../../code_snippets/snippet_hermes_agent_lsp_manager_lifecycle.md) — toolchain/subprocess lifecycle; relevance: toolchain (Swift/SDK) lifecycle analog to the SDK-mismatch recipe.

### oc_platforms_mac_health (10t · 11s · 11d)

**Terms**
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: the page's core `openclaw health --json` probe surfaced in the menu bar / Health card.
- [term_heartbeat](../../term_dictionary/term_heartbeat.md) — periodic liveness signal; relevance: tail `web-heartbeat` / `web-reconnect` log lines in the "When in doubt" CLI fallback.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway/agent platform; relevance: the system whose linked-channel health this page reports.
- [term_anomaly_detection](../../term_dictionary/term_anomaly_detection.md) — detect abnormal/failed state; relevance: the probe flags logged-out / probe-failed (red status dot).
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — event/state-driven design; relevance: cached snapshot + on-demand + ~60s periodic probe drive the UI state.
- [term_websocket](../../term_dictionary/term_websocket.md) — persistent socket connection; relevance: "linked + socket opened recently" (Baileys socket) is the green-health signal.
- [term_channel_kernel](../../term_dictionary/term_channel_kernel.md) — substrate channel adapters compose against; relevance: the Channels tab surfaces per-channel (WhatsApp/Telegram) status the kernel mediates.
- [term_channel_adapter](../../term_dictionary/term_channel_adapter.md) — adapter for a messaging platform; relevance: WhatsApp/Telegram adapters whose login/logout/probe/disconnect the Channels tab controls.
- [term_failover](../../term_dictionary/term_failover.md) — fall back on failure; relevance: "falls back gracefully when offline" using the cached good snapshot.
- [term_ttl_time_to_live](../../term_dictionary/term_ttl_time_to_live.md) — bounded data lifetime; relevance: the cached snapshot + last-check timestamp are time-bounded staleness windows.

**Docs**
- [oc_gateway_health](oc_gateway_health.md) — (planned, gw03) the CLI health flow; relevance: the `## Related` "Gateway health" target (`openclaw status`, `status --deep`, `health --json`).
- [oc_platforms_mac_menu_bar](oc_platforms_mac_menu_bar.md) — (planned, this series) menu state model; relevance: "Health row reappears when all sessions idle" links the two UIs.
- [oc_platforms_mac_child_process](oc_platforms_mac_child_process.md) — (planned, this series) attach-then-start lifecycle; relevance: health probing precedes / follows the attach decision.
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, pf04) generic macOS app; relevance: parent macOS-app page.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — (planned, ch05) channel disconnect/error; relevance: the "last disconnect/error" the Channels tab shows.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway status/health operations; relevance: sibling stack's gateway status/health command surface.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — Baileys WhatsApp channel; relevance: the exact Baileys channel whose socket health this page reports.
- [hermes_lsp_diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — diagnostics/health surfacing; relevance: a sibling "health card"-style diagnostics surface.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — background session health/status; relevance: monitoring a long-running hosted agent process analog.
- [band_agent_api_context_activity](../band/band_agent_api_context_activity.md) — agent activity/status API; relevance: status-surface vocabulary for linked-channel/agent state.
- [aws_bedrock_agentcore_observability_overview](../aws_bedrock_agentcore/bedrock_agentcore_observability_overview.md) — agent health/observability overview; relevance: framing for periodic-probe + cached-snapshot health monitoring of an agent runtime.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: surfaces the status dot, Health card, and Channels tab.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Baileys/WhatsApp channel code; relevance: the channel whose linked/auth/socket health is probed.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the target of the `openclaw status` CLI fallback.

**Snippets**
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/health on startup; relevance: the connecting/retrying (orange) state and channel restart path.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel-status surfacing; relevance: the Channels-tab status + controls this page describes.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat/buffered delta; relevance: the `web-heartbeat` signal tailed in "When in doubt".
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — on-demand probe execution; relevance: the "Run Health Check" on-demand probe pattern.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — cached status/latency snapshot; relevance: the cached good snapshot + last-error separation that avoids flicker.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — gateway shutdown/teardown; relevance: the logged-out / probe-failed (red) terminal state.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health command; relevance: the `openclaw status`/`health --json` fallback flow analog.
- [snippet_hermes_agent_gw_status_snapshot](../../code_snippets/snippet_hermes_agent_gw_status_snapshot.md) — gateway status snapshot; relevance: the cached-snapshot pattern the Health card uses.
- [snippet_hermes_agent_gw_platform_whatsapp_connect](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_connect.md) — WhatsApp connect/login; relevance: the login-QR / connect path the Channels tab exposes for WhatsApp.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — connectivity doctor check; relevance: deep-probe connectivity check analog to `openclaw status --deep`.
- [snippet_hermes_agent_gw_memory_monitor](../../code_snippets/snippet_hermes_agent_gw_memory_monitor.md) — periodic health/resource monitor; relevance: the ~60s periodic probe loop analog.

### oc_platforms_mac_icon (9t · 11s · 11d)

**Terms**
- [term_voice_wake](../../term_dictionary/term_voice_wake.md) — wake-word activation; relevance: the "big ears" voice-trigger state fired by `AppState.triggerVoiceEars` on wake.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — transcription pipeline; relevance: the in-app voice pipeline that captures the utterance while ears are boosted.
- [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — streaming transcription; relevance: ears stay boosted for the capture window the live transcription occupies.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — state driven by signals/events; relevance: icon states are driven by AppState signals (`isWorking`, `earBoostActive`) and TTLs.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the agent platform; relevance: the OpenClaw mac app whose menu-bar critter this state model renders.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the "Working (agent running)" scurry state reflects an in-flight harness run.
- [term_ttl_time_to_live](../../term_dictionary/term_ttl_time_to_live.md) — bounded lifetime; relevance: "Keep TTLs short (<10s) so the icon returns to baseline" if a job hangs.
- [term_observer_pattern](../../term_dictionary/term_observer_pattern.md) — one-to-many state-change notification; relevance: the icon observes AppState signal changes (working/voice) to re-render.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the voice subsystem pairing (STT/TTS) the ear-boost feature belongs to.

**Docs**
- [oc_platforms_mac_menu_bar](oc_platforms_mac_menu_bar.md) — (planned, this series) the IconState enum + Working state; relevance: the state model this critter icon renders (direct `## Related` link).
- [oc_platforms_mac_voicewake](oc_platforms_mac_voicewake.md) — (planned, pf04) voice-wake detector; relevance: the detector that calls `triggerVoiceEars(ttl: nil)` / `stopVoiceEars()`.
- [oc_nodes_voicewake](oc_nodes_voicewake.md) — (planned, nd02) node-side voice-wake; relevance: the wake-word mechanics feeding the in-app trigger.
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, pf04) generic macOS app; relevance: parent macOS-app page.
- [oc_platforms_mac_health](oc_platforms_mac_health.md) — (planned, this series) idle/health behavior; relevance: idle blink/wiggle baseline returns when no work/voice is active.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode activation/CLI; relevance: sibling stack's voice-trigger model behind the ears state.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT transcription pipeline; relevance: the capture-window transcription the ear boost visually matches.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — using voice mode; relevance: end-to-end voice-trigger UX the "big ears" affordance signals.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation/mic capture; relevance: sibling-tool mic-capture-during-utterance analog to ear-boost capture window.
- [cc_desktop_workspace_panes](../claude_code/cc_desktop_workspace_panes.md) — desktop UI state/affordances; relevance: desktop-app UI-state-rendering precedent for an activity-driven indicator.
- [pi_extensions_custom_ui](../pi/pi_extensions_custom_ui.md) — custom UI state rendering; relevance: cross-stack "render UI state from agent activity signals" framing for the icon states.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the Swift app + `CritterIconRenderer`; relevance: the code home of `makeIcon(...)`, `triggerVoiceEars`, `setWorking`.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech subsystem; relevance: the in-app voice pipeline that fires the ears.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice pipeline/phone; relevance: voice-capture cross-reference for the ear-boost capture window.

**Snippets**
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — the `triggerVoiceEars` path; relevance: exact wake-trigger call that boosts the ears.
- [snippet_openclaw_macos_voice_wake_state](../../code_snippets/snippet_openclaw_macos_voice_wake_state.md) — voice-wake state machine; relevance: the `earBoostActive` state driving ear scale/holes.
- [snippet_openclaw_macos_voice_wake_audio](../../code_snippets/snippet_openclaw_macos_voice_wake_audio.md) — audio capture window; relevance: the ~1s-silence capture window `stopVoiceEars()` matches.
- [snippet_openclaw_macos_pushtotalk_overlay](../../code_snippets/snippet_openclaw_macos_pushtotalk_overlay.md) — push-to-talk overlay; relevance: related in-app voice UI affordance alongside the ear-boost state.
- [snippet_openclaw_macos_pushtotalk_nsevent](../../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md) — push-to-talk key event; relevance: another internal voice-trigger signal source (page warns: keep triggers internal).
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — gateway-side voice-wake tracking; relevance: the wake event the app reacts to with ears.
- [snippet_openclaw_macos_menu_sessions_preview](../../code_snippets/snippet_openclaw_macos_menu_sessions_preview.md) — menu-bar session preview UI; relevance: the menu-bar surface the icon sits in.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the speech pipeline whose activity the ears reflect.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local TTS; relevance: the speech-synthesis half of the voice subsystem the icon pairs with.
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — macOS UI component lifecycle; relevance: short-TTL / reset-in-`defer` lifecycle pattern the page mandates to avoid stuck animations.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — voice-event dedup; relevance: avoids the "accidental flapping" the page warns about for ears/working signals.

### oc_platforms_mac_logging (9t · 10s · 10d)

**Terms**
- [term_pii](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: private payloads "can include phone numbers and message bodies" — the page's core sensitivity warning.
- [term_personal_data](../../term_dictionary/term_personal_data.md) — personal data category; relevance: the message bodies / phone numbers exposed by `Enable-Private-Data`.
- [term_sensitive_personal_data](../../term_dictionary/term_sensitive_personal_data.md) — sensitive personal data; relevance: the heightened-sensitivity payloads the plist override unredacts.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: the `ai.openclaw` subsystem whose logs this page captures.
- [term_observability_agent_systems](../../term_dictionary/term_observability_agent_systems.md) — agent monitoring/tracing/logging; relevance: rolling diagnostics + unified logging are this app's observability surface.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — subsystem/event opt-in; relevance: unified-logging private-data is a per-subsystem opt-in that only affects new log entries.
- [term_anomaly_detection](../../term_dictionary/term_anomaly_detection.md) — investigating failures; relevance: logs are captured to investigate failures (enable before reproducing the issue).
- [term_voice_wake](../../term_dictionary/term_voice_wake.md) — wake/session lifecycle; relevance: `read_when` calls out "debugging voice wake/session lifecycle issues" as the logging use case.
- [term_health_check](../../term_dictionary/term_health_check.md) — health diagnostics; relevance: "Reveal Logs" / log capture supports debugging health-probe failures.

**Docs**
- [oc_gateway_logging](oc_gateway_logging.md) — (planned, gw03) Gateway-side logging; relevance: the `## Related` "Gateway logging" link target.
- [oc_logging](oc_logging.md) — (planned, rt02) top-level logging; relevance: the umbrella logging reference this mac page specializes.
- [oc_platforms_mac_dev_setup](oc_platforms_mac_dev_setup.md) — (planned, this series) debugging build/runtime; relevance: enable logging while debugging a dev build.
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, pf04) generic macOS app; relevance: parent macOS-app page.
- [oc_platforms_mac_health](oc_platforms_mac_health.md) — (planned, this series) "Reveal Logs" from Health card; relevance: the Health card's Reveal-Logs button surfaces these logs.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — telemetry/observability config; relevance: enabling/opting-into richer telemetry analog to the private-data plist toggle.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — data-usage / telemetry / privacy; relevance: the private-data-in-logs sensitivity tradeoff is the same class of concern.
- [cc_otel_analysis_and_privacy](../claude_code/cc_otel_analysis_and_privacy.md) — telemetry analysis + privacy; relevance: privacy controls over what payloads logging exposes (phone numbers / message bodies).
- [hermes_lsp_diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — diagnostics/log capture; relevance: rolling-diagnostics-file capture analog on a sibling stack.
- [aws_bedrock_agentcore_observability_telemetry](../aws_bedrock_agentcore/bedrock_agentcore_observability_telemetry.md) — agent telemetry/log capture; relevance: capturing agent-runtime logs/telemetry for debugging analog.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: emits swift-log / unified logging and writes the rolling JSONL diagnostics file.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — privacy/sensitive-data handling; relevance: the private-data-exposure concern (`Enable-Private-Data`) is a security/privacy surface.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: Gateway logs cross-reference (`/tmp/openclaw/openclaw-*.log`).

**Snippets**
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency logging signal; relevance: the kind of operational signal the diagnostics log captures.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat log line; relevance: the `web-heartbeat`/`web-reconnect` lines tailed when debugging.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security/audit probe execution; relevance: the security-sensitive surface that motivates the private-data warning.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — shutdown logging path; relevance: shutdown/forensic log lines captured in diagnostics.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor logs; relevance: supervisor lifecycle log lines the diagnostics file collects.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup/verbosity; relevance: the "App logging → Verbosity" / log-routing setup analog.
- [snippet_hermes_agent_core_auxiliary_diagnostics](../../code_snippets/snippet_hermes_agent_core_auxiliary_diagnostics.md) — auxiliary diagnostics capture; relevance: rolling diagnostics-file capture analog.
- [snippet_hermes_agent_plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — observability/telemetry plugin; relevance: opt-in richer-observability analog to the private-data plist.
- [snippet_hermes_agent_gw_shutdown_forensics](../../code_snippets/snippet_hermes_agent_gw_shutdown_forensics.md) — shutdown forensics logging; relevance: forensic post-issue log capture the rolling file enables.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — doctor connectivity logging; relevance: connectivity-diagnostic logging analog (`clawlog.sh` richer output).

### oc_platforms_mac_menu_bar (10t · 11s · 11d)

**Terms**
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — event-ingestion-driven state; relevance: control-channel `agent` events (`ControlChannel.handleAgentEvent`) drive the whole state model.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation with name+args; relevance: the `tool` activity kind (`phase: start|result`, `toolName`, `meta/args`: exec/read/write/edit).
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime/command execution; relevance: the `job` activity kind = high-level command execution (started|streaming|done|error).
- [term_health_check](../../term_dictionary/term_health_check.md) — health summary; relevance: "When idle, falls back to the health summary" in the status row.
- [term_heartbeat](../../term_dictionary/term_heartbeat.md) — periodic/debounced signal; relevance: "TTL grace on tool results" prevents badge flicker on rapid tool bursts.
- [term_ttl_time_to_live](../../term_dictionary/term_ttl_time_to_live.md) — bounded lifetime; relevance: the tool-result TTL grace window that stabilizes the badge.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: the OpenClaw mac app whose menu/status logic this models.
- [term_event_ledger](../../term_dictionary/term_event_ledger.md) — per-session append-only ACP event log; relevance: the `runId`/`sessionKey` agent events the menu ingests are the same SessionUpdate stream.
- [term_agent_lifecycle_event](../../term_dictionary/term_agent_lifecycle_event.md) — agent state-transition signal; relevance: job start/streaming/done/error transitions drive the icon/status state.
- [term_observer_pattern](../../term_dictionary/term_observer_pattern.md) — one-to-many change notification; relevance: the menu UI observes agent-event state changes and re-renders the icon/status row.

**Docs**
- [oc_platforms_mac_icon](oc_platforms_mac_icon.md) — (planned, this series) the IconState/critter rendering; relevance: the icon this state model drives (direct `## Related` link).
- [oc_platforms_macos](oc_platforms_macos.md) — (planned, pf04) generic macOS app; relevance: parent macOS-app page.
- [oc_concepts_session](oc_concepts_session.md) — (planned, co06) session/runId model; relevance: the per-`sessionKey`/`runId` session model the menu prioritizes.
- [oc_platforms_mac_health](oc_platforms_mac_health.md) — (planned, this series) health row; relevance: "Health row reappears once all sessions idle".
- [oc_concepts_streaming](oc_concepts_streaming.md) — (planned, co07) streaming events; relevance: `stream: "job"/"tool"` streaming-event parsing the menu performs.
- [band_agent_api_context_activity](../band/band_agent_api_context_activity.md) — agent context/activity API; relevance: the activity-kind / context model the menu surfaces (work state, Context, Usage).
- [pi_extensions_events_agent_tools](../pi/pi_extensions_events_agent_tools.md) — agent events + tool events; relevance: the `job`/`tool` event taxonomy (exec/read/write/edit) the menu parses.
- [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — event hook/ingestion; relevance: control-channel event-ingestion analog feeding UI state.
- [hermes_tui_interface](../hermes_agent/hermes_tui_interface.md) — TUI status/activity surface; relevance: sibling status-UI that renders session/activity state.
- [cc_desktop_workspace_panes](../claude_code/cc_desktop_workspace_panes.md) — desktop UI session/activity panes; relevance: desktop-app session-status-rendering precedent.
- [cc_web_session_management](../claude_code/cc_web_session_management.md) — multi-session management; relevance: the "main vs most-recently-active non-main session" priority model analog.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the Swift menu-bar UI; relevance: code home of `ControlChannel.handleAgentEvent`, `IconState`, `@AppStorage("iconOverride")`.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session model; relevance: the per-`sessionKey`/`runId` session state the menu prioritizes and previews.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the control-channel `agent` events source.

**Snippets**
- [snippet_openclaw_macos_menu_sessions_submenu](../../code_snippets/snippet_openclaw_macos_menu_sessions_submenu.md) — the Context submenu; relevance: the "Context" submenu of recent sessions this page specifies.
- [snippet_openclaw_macos_menu_sessions_control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — session-row controls; relevance: per-session reset/compact/delete/preview actions in the submenu.
- [snippet_openclaw_macos_menu_sessions_preview](../../code_snippets/snippet_openclaw_macos_menu_sessions_preview.md) — session preview/token bar; relevance: "token bar, age, preview, thinking/verbose" each session row keeps.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent-event dispatch; relevance: the `agent` event dispatch the menu's `handleAgentEvent` ingests.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persist/lifecycle; relevance: the `runId`/`sessionKey` session lifecycle the menu tracks.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patches; relevance: session state transitions (active/idle) that switch main-vs-other priority.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered delta/debounce; relevance: the TTL-grace / no-flicker buffering on rapid tool bursts.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — event dedup; relevance: avoids flip-flopping/flicker mid-activity the state model prohibits.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — run manager / runId tracking; relevance: the per-`runId` run state the menu reflects.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog (exec/read/write/edit); relevance: the toolName→glyph mapping (💻/📄/✍️/📝) the ActivityKind enum renders.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — control-channel request handler; relevance: the control-channel handler path delivering `agent` events to the UI.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary on these pages is operational/UI macOS-app terminology, NOT cross-cutting
> reusable concepts — it is captured in the `oc_*` doc notes themselves (this is the page subject), and
> existing `term_dictionary` terms are LINKED, never redefined. **Expected new `term_dictionary` captures: 0.**

| Term (from pages) | Disposition |
|---|---|
| launchd / LaunchAgent (`ai.openclaw.gateway`) | macOS-OS mechanism, app-operational; documented in `oc_platforms_mac_child_process` (note 1). Link `term_cron` (scheduled/managed-service analog); no new term. |
| attach-only / remote / child-process modes | OpenClaw mac-app lifecycle vocabulary; documented in note 1. No new term. |
| ad-hoc signing / Apple Developer ID / TCC | macOS-OS dev/security mechanics; documented in `oc_platforms_mac_dev_setup` (note 2). No standalone vault term warranted (mac-specific, not cross-cutting). |
| Baileys health / status dot / Health card | OpenClaw mac-app health UI vocabulary; documented in `oc_platforms_mac_health` (note 3). Link `term_health_check`, `term_heartbeat`, `term_websocket`; no new term. |
| IconState / ActivityKind / earBoost / scurry | OpenClaw mac-app UI state-model vocabulary; documented in `oc_platforms_mac_icon` + `oc_platforms_mac_menu_bar` (notes 4, 6). Link `term_voice_wake`, `term_event_driven_architecture`; no new term. |
| rolling diagnostics JSONL / unified logging private-data | macOS logging mechanics; documented in `oc_platforms_mac_logging` (note 5). Link `term_pii` (private payloads). No new term — `term_logging`/`term_observability`/`term_structured_logging` are MISSING but are NOT introduced by this sub-plan (cross-cutting term candidate, deferred to a logging-core sub-plan if it ever arises; not reusable enough from these 6 mac-app pages alone). |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and
an existing note. (`term_logging`/`term_observability` are absent from the vault but are deliberately NOT
promoted here — these macOS-app pages are not the right home; flagged for a future logging/observability
core sub-plan, per master's near-0 expectation.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** Inherited from master: any new `term_dictionary` note (none here) would be authored
`acronym_glossary_*.md`. No term definitions are inlined in `oc_*` notes; existing terms are linked only.

## Per-Phase Validation Gate (G1–G9)

Single execution phase (6 notes). All 8 gates inherited from master; run before commit.

| Gate | Check | Tool / Method | Pass condition |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `python3 scripts/check_yaml_frontmatter.py --path <note>` | YAML field order correct; H1 `# OpenClaw — …`; `## Overview`/`## Related Notes`/`## References`; bold `**Source**`/`**Last Updated**`/`**Status**` footer; no forbidden YAML fields. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/platforms/mac/<page>.md` | Every claim traces to source; commands/paths/labels (`ai.openclaw.gateway`, `~/Library/Logs/OpenClaw/diagnostics.jsonl`, `triggerVoiceEars`, `IconState`) reproduced verbatim; no invented behavior. |
| G3 | Density + Coverage | `wc -w` (body, frontmatter excluded) + code-fence count + Section Coverage Map | Each note ≤2,500w / ≤400 lines / ≤6 code blocks; one `building_block`; every mapped H2/H3 present; 0 orphan sections. |
| G4 | Cross-Reference | Count Related-Notes links + relevance statements | ≥6 relevancy-selected `term_dictionary` terms per note + ≥1 `repo_openclaw*` + sibling `oc_*` + relevant docs/snippets, each with a relevance statement (indexed `[text](path.md)` format). |
| G5 | Ghost-reference | DB existence check on every cited EXISTING id; redirect planned `oc_*` | 0 ghost links to non-existent notes; planned siblings labeled "(planned)" until created. |
| G6 | Broken-link | `/tessellum-fix-broken-links` after incremental reindex | 0 broken relative links from the 6 new notes. |
| G7/G8 | Discoverability | `note_links` in-degree query per new note | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md`); in-degree ≥1; anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
# Run from repo root. Resolve config-driven paths (single source of truth).
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"

NOTES="oc_platforms_mac_child_process oc_platforms_mac_dev_setup oc_platforms_mac_health oc_platforms_mac_icon oc_platforms_mac_logging oc_platforms_mac_menu_bar"

# --- G1 format + density sweep (per note) ---
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $f"; continue; }
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  echo "$REQ_SECTIONS" | tr '|' '\n' | while read -r sec; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # require source_url in frontmatter when REQUIRE_SOURCE_URL=1
  [ "$REQUIRE_SOURCE_URL" -eq 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # density caps (body only, frontmatter stripped)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb cb / $lines L)"
  # sibling-prefix sanity: at least one oc_ sibling link
  grep -q "($SIBLING_PREFIX" "$f" || echo "$n NOTE: no $SIBLING_PREFIX sibling link found"
done

# --- YAML frontmatter validation (whole folder) ---
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# --- G5 ghost-reference: every cited EXISTING note_id must resolve ---
# (run after authoring; extracts [..](path.md) targets, strips ../ , verifies in DB)
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  grep -oE '\]\([^)]+\.md\)' "$f" | sed -E 's/^\]\(//; s/\)$//' | while read -r rel; do
    stem=$(basename "$rel"); [ "$stem" = "$n.md" ] && continue
    case "$stem" in oc_*) continue;; esac   # planned siblings skipped
  done
done

# --- G6 broken links + reindex (delegate to skill) ---
bash scripts/update_notes_database.sh --force
# then: /tessellum-fix-broken-links   (and re-verify 0 broken_links rows for the 6 notes)

# --- G7/G8 in-degree ≥1 (anti-island) ---
for n in ${=NOTES}; do
  echo "$n in_degree=${d:-0}"; [ "${d:-0}" -ge 1 ] || echo "ISLAND: $n (needs entry_openclaw_docs inbound)"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps (≤2500w / ≤400L / ≤6 cb)? |
|---|---|---|---:|---:|---|
| 1 | oc_platforms_mac_child_process | procedure | 420 | 2 | ✅ |
| 2 | oc_platforms_mac_dev_setup | procedure | 460 | 5 | ✅ |
| 3 | oc_platforms_mac_health | procedure | 300 | 0 | ✅ |
| 4 | oc_platforms_mac_icon | model | 320 | 0 | ✅ |
| 5 | oc_platforms_mac_logging | procedure | 360 | 1 | ✅ |
| 6 | oc_platforms_mac_menu_bar | model | 520 | 0 | ✅ |

No note approaches caps (largest 520w vs 2,500w cap; max 5 code blocks in dev-setup vs 6 cap — the 6 raw
fences in dev-setup.md fold into ≤5 reproduced blocks, the rest summarized). No promotion-to-split needed.

## Entry Point Decision (inherited from master)

Per master W1, `0_entry_points/entry_openclaw_docs.md` is CREATED as a pre-step before the first sub-plan
**6 rows** to that entry point under a **"Platforms — macOS App"** cluster (one row per note: child-process,
dev-setup, health, icon, logging, menu-bar), each with the entry-point back-link added at finalization. No
new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution; satisfies in-degree ≥1):

- `entry_openclaw_docs.md` (pre-created per W1) → **all 6** notes (primary anti-island guarantee).
- `repo_openclaw_apps.md` → notes 1, 2, 3, 4, 5, 6 (the desktop-app repo is the code home of every page).
- `repo_openclaw_gateway.md` → notes 1, 3, 5 (Gateway lifecycle / health / logging).
- `repo_openclaw_cli_wizard.md` → notes 1, 2 (the external `openclaw` CLI install/launchd enable).
- `repo_openclaw_extensions_voice_speech.md` → note 4 (voice-wake "ears" trigger).
- `repo_openclaw_sessions.md` → note 6 (session/runId model behind the menu state).
- `term_voice_wake.md` → notes 4, 6; `term_health_check.md` → notes 1, 3; `term_pii.md` → note 5;
  `term_heartbeat.md` → notes 3, 6 (reciprocal term back-links added at augment/execute).

## Pacing Rules (inherited from master)

One execution phase, 6 notes (well under the ~30-agent fan-out cap). Re-read each source page during
execution; reproduce shell/plist snippets verbatim (G2). One BB per note. `git pull --rebase --autostash`
before committing; commit+push the sub-plan as one wave; no Claude co-author trailer. Reindex incrementally
and verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note Related mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (status: ready) |

## Augmentation Report (2026-06-21)

Related Notes Mapping at RAISED floors (**≥8 terms · ≥10 snippets · ≥10 docs per note**), replacing the
prior `## Candidate Cross-References` (which used the ≥6-terms floor). All 6 source pages were re-read from

**What was LOCKED (per-note counts; floors met = ✅):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_platforms_mac_child_process | 10 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| oc_platforms_mac_dev_setup | 8 | 10 | 11 (7 existing / 4 planned) | 3 | ✅ |
| oc_platforms_mac_health | 10 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| oc_platforms_mac_icon | 9 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| oc_platforms_mac_logging | 9 | 10 | 10 (5 existing / 5 planned) | 3 | ✅ |
| oc_platforms_mac_menu_bar | 10 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |

  siblings counting toward the 10-doc floor): rich use of `claude_code/cc_*`, `hermes_agent/hermes_*`,
  `pi/pi_*`, `band/band_*`, `aws_bedrock_agentcore/*` coding-agent corpora.
  list: `term_failover`, `term_kill_tree`, `term_remote_ssh`, `term_ssh`, `term_agent_lifecycle_event`,
  `term_ttl_time_to_live`, `term_channel_kernel`, `term_channel_adapter`, `term_observer_pattern`,
  `term_event_ledger`, `term_observability_agent_systems`, `term_realtime_transcription`,
  `term_personal_data`, `term_sensitive_personal_data`. Candidate-list false positives confirmed and dropped:
  `term_reverse_proxy`, `term_voice_wake` for note 1, `term_socket_mode`, `term_bonjour_discovery`,
  `term_phoenix_channels`, `term_sessionid`, `term_flyweight_pattern` (verified non-relevant by reading defs).

**New-term candidates.** None promoted by this sub-plan (consistent with master near-0 expectation and the
Undigested Terms Plan). DB-confirmed MISSING cross-cutting term candidates surfaced during the re-read:
`term_logging`, `term_observability`, `term_structured_logging`, `term_usage_tracking` — all deliberately
NOT captured here (these 6 macOS-app pages are not the right home). Best-fit glossary if ever promoted:
`acronym_glossary_software_engineering.md` (logging/observability/structured-logging) and
`acronym_glossary_agentic_ai.md` (usage-tracking). Flagged for a future logging/observability-core sub-plan.
Existing substitute in use now: `term_observability_agent_systems` (note 5).

**Source re-read confirmation (CP7).** Measured (body words, frontmatter excluded) vs plan estimates:
child-process 350 (plan src 350), dev-setup 435 (435), health 238 (238), icon 291 (291), logging 347 (347),
menu-bar 575 (575). Ratios all 1.0 — no under-estimation; no further splits needed.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (min 8 on dev-setup), ≥10 snippets, ≥10 docs, each link carries `relevance:` statement; indexed `[text](path.md)` format. |
| CP2 | 9-GATE per batch (G1-G6, G7/G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7/G8 discoverability; one execution phase. |
| CP4 | Plan size | **PASS** | 6 notes (≤30); single execution phase; well under fan-out cap. |
| CP6 | Density / borderline split | **PASS** | `## Density Re-Assessment`: largest note 575w (vs 2,500w cap), max 5 reproduced code blocks (vs 6 cap); no borderline; 1 BB per note; no split warranted. |
| CP7 | Sources measured | **PASS** | All 6 pages re-read 2026-06-21; measured words match plan src table exactly (350/435/238/291/347/575); ratio 1.0; no under-estimation. |
| CP8 | Undigested Terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned, 0 new term captures, must-language); `## Term-Note Authoring Requirements` present (N/A 0 terms — inherited from master, capture via `/tessellum-capture-term-note` + glossary if any term ever surfaces). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs (no `term_*` to rename/dedup); collision audit run for the 6 planned doc slugs — `oc_platforms_mac_*` are unique (0 existing `resources/documentation/openclaw/*`); no doc-note duplicates an existing term note (each links existing `term_*` rather than redefining). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks` maps every new note → ≥1 outside-folder inbound (entry_openclaw_docs + repo_openclaw_apps for all 6, plus topical repo/term back-links); G7/G8 in-degree≥1 check in the gate table + validation script. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
