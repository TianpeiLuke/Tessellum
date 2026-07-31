---
title: Sub-Plan in05 — OpenClaw Docs: Install (Railway, Raspberry Pi, Render, Uninstall, Updating, Upstash)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["install/railway", "install/raspberry-pi", "install/render", "install/uninstall", "install/updating", "install/upstash"]
---

# Sub-Plan in05: Install

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML field order, body H2/H3, `## Overview` + `## Related Notes` + `## References`), dedup-before-create (term_dictionary AND documentation/ AND repo_openclaw*), the 9-GATE table, cross-references, undigested-terms ownership, and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master and not restated here.

## Scope

The 6 Install-section pages that cover the **remaining install/lifecycle surface** after the core installer/Docker/cloud-provider pages (handled by in01–in04): three managed-cloud one-click deploy paths (**Railway**, **Render**, **Upstash Box**), one bare-metal always-on path (**Raspberry Pi / ARM**), and the two cross-cutting lifecycle operations every deployment eventually needs — **Updating** (update command, channel switching, manual package update, auto-updater, rollback) and **Uninstall** (CLI uninstaller + manual launchd/systemd/schtasks service removal). Priority **P1 (Phase A)**: these are operational-core docs the rest of the corpus references (gateway, channels, providers all assume an installed, up-to-date, persistently-running Gateway). The code-side counterparts (`repo_openclaw_gateway`, `repo_openclaw_cli_wizard`, the `snippet_openclaw_daemon_*` launchd/systemd/schtasks renderers) are LINKED, not recreated.

**Source**: OpenClaw docs, 6 pages, **4,299 measured body words**, 92 code fences. **Planned: 7 notes** (one split: `updating` → procedure + auto-updater model).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Railway | install/railway | 328 | 1 | 7 | 3 | procedure |
| Raspberry Pi | install/raspberry-pi | 1,016 | 12 | 10 | 0 | procedure |
| Render | install/render | 763 | 4 | 10 | 9 | procedure |
| Uninstall | install/uninstall | 499 | 12 | 4 | 5 | procedure |
| Updating | install/updating | 1,405 | 18 | 9 | 6 | procedure (split: update/rollback procedure vs auto-updater model) |
| Upstash Box | install/upstash | 288 | 7 | 8 | 0 | procedure |

> Word counts are body-only (`sed` strips YAML frontmatter, then `wc -w`). Code counts are fence-pairs (`grep -c '^```' / 2`): railway 2/2=1, raspberry-pi 24/2=12, render 8/2=4, uninstall 24/2=12, updating 36/2=18, upstash 14/2=7. Total: 4,299 body words, 54 fence-pairs.

## Content Strategy

- **Prioritize**: the lifecycle pages (Updating, Uninstall) — they are referenced by every other deploy path's "Next steps / Related" and are the highest-traffic operational docs. The required-state-persistence pattern (`OPENCLAW_STATE_DIR=/data/.openclaw`, `OPENCLAW_WORKSPACE_DIR`, attached volume / disk so config + `auth-profiles.json` + sessions survive redeploys) recurs across Railway/Render/Upstash/Pi and is the load-bearing concept to capture faithfully in each.
- **Split**: only `updating.md` (1,405w, 18 fences) splits — its 18 code fences exceed the ≤6 cap and it mixes a hands-on **procedure** (update command, npm↔git channel switch, re-run installer, manual npm/pnpm/bun, post-update doctor/restart/verify, rollback/pin) with a distinct **configuration model** (the `update.auto` JSON5 schema + the stable/beta/dev channel-behavior table + `OPENCLAW_NO_AUTO_UPDATE`/`update.checkOnStart` flags + control-plane handoff semantics). The other 5 pages are ≤1,016w / ≤12 fences each and stay 1 note (a deploy how-to per host).
- **Link-out (do not duplicate)**: channel setup (`/channels/*`) → ch01–ch06 sub-plans; gateway configuration / remote / security / tailscale / doctor / health (`/gateway/*`) → gw01–gw07; CLI command pages (`/cli/backup`, `/cli/update`, `/cli/uninstall`, `/cli/onboard`, `/cli/gateway`, `/cli/doctor`) → cl01–cl09; `/install/development-channels`, `/install/installer`, `/install/docker`, `/install/migrating*` → in01–in04 siblings; `/vps` + `/platforms` → rt02/rt03/pf*. Container/cloud vocabulary links existing `term_docker`, `term_blue_green_deployment`, `term_secrets_manager`, `term_node_js`, `term_npm`, `term_arm` — never redefined inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_install_railway.md` | procedure | railway.md: Quick checklist, One-click deploy, What you get, Required Railway settings (Public Networking / Volume / Variables), Connect a channel, Backups & migration, Next steps | 420 | One-click OpenClaw deploy on Railway: deploy template, attach a `/data` volume, set the required Variables (`OPENCLAW_GATEWAY_PORT`, `OPENCLAW_GATEWAY_TOKEN`, state/workspace dirs), enable HTTP Proxy on port 8080, then reach the Control UI at `/openclaw` and back up via `openclaw backup create`. |
| 2 | `oc_install_raspberry_pi.md` | procedure | raspberry-pi.md: Hardware compatibility, Prerequisites, Setup (9-step), Performance tips, Recommended model setup, ARM binary notes, Persistence and backups, Troubleshooting, Next steps, Related | 620 | Always-on self-hosted OpenClaw Gateway on a Raspberry Pi: hardware/RAM matrix, the 9-step headless setup (flash 64-bit OS → SSH → Node 24 → swap → install → onboard → verify → tunnel to Control UI), ARM64 binary caveats, low-RAM performance tuning, cloud-model config, and Pi-specific troubleshooting. |
| 3 | `oc_install_render.md` | procedure | render.md: Prerequisites, Deploy with a Render Blueprint, Understanding the Blueprint, Choosing a plan, After deployment (Control UI), Render Dashboard features (Logs / Shell / Env / Auto-deploy), Custom domain, Scaling, Backups and migration, Troubleshooting, Next steps | 560 | Infrastructure-as-Code OpenClaw deploy on Render: the `render.yaml` Blueprint (docker runtime, `/health` check, auto-generated `OPENCLAW_GATEWAY_TOKEN`, persistent `/data` disk), plan/spin-down/disk trade-offs, dashboard logs/shell/env, custom domain + TLS, scaling guidance, and deploy/health/data-loss troubleshooting. |
| 4 | `oc_install_uninstall.md` | procedure | uninstall.md: Easy path (CLI installed), Manual service removal (macOS launchd / Linux systemd / Windows schtasks), Normal install vs source checkout, Related | 470 | Completely removing OpenClaw: the `openclaw uninstall` path (`--dry-run`/`--all`/`--yes --non-interactive`, workspace preservation), the equivalent manual steps (stop + uninstall gateway service, delete state/config/workspace, remove the CLI per package manager), and the CLI-gone fallback that boots out the launchd/systemd/schtasks service directly, with profile and remote-mode notes. |
| 5 | `oc_install_updating.md` | procedure | updating.md: Recommended `openclaw update`, Switch between npm and git installs, Alternative: re-run the installer, Alternative: manual npm/pnpm/bun (+ Advanced npm install topics), After updating (doctor / restart / verify), Rollback (pin version / pin commit), If you are stuck, Related | 680 | Updating OpenClaw safely: `openclaw update` (install-type detection, channel/version targeting, dry-run/json diagnostics, npm↔git switch), re-running the installer for recovery, supervised manual npm/pnpm/bun updates (stop-Gateway-first, staged temp-prefix swap, EACCES recovery), post-update doctor/restart/health verify, and rollback by pinning a version or commit. |
| 6 | `oc_install_updating_auto_updater.md` | model | updating.md: Auto-updater (`update.auto` config schema, stable/beta/dev channel-behavior table, `update.checkOnStart`, `OPENCLAW_NO_AUTO_UPDATE`, control-plane detached-handoff semantics) | 380 | The OpenClaw auto-updater configuration model: the `update.auto` JSON5 block (`enabled`, `stableDelayHours`, `stableJitterHours`, `betaCheckIntervalHours`), the per-channel apply behavior (stable jittered rollout / beta hourly / dev manual), startup update hints, the `OPENCLAW_NO_AUTO_UPDATE` and `update.checkOnStart` overrides, and how live control-plane update requests use a detached handoff rather than swapping the package in-process. |
| 7 | `oc_install_upstash.md` | procedure | upstash.md: Prerequisites, Create a Box, Connect with an SSH tunnel, Install OpenClaw, Run onboarding, Start the Gateway, Auto-restart, Troubleshooting, Related | 380 | Hosting OpenClaw on an Upstash Box (keep-alive managed Linux): create a keep-alive Box, forward the dashboard port over an SSH tunnel (with keepalive options), `npm install -g openclaw`, `openclaw onboard --install-daemon`, bind the Gateway to LAN and run it backgrounded, set the Box init script for auto-restart, and recover frozen SSH tunnels with a clean config. |

## Section Coverage Map

```
railway.md
├── Quick checklist (new users) ───────────────────── → note 1 (oc_install_railway)
├── One-click deploy ──────────────────────────────── → note 1
├── What you get ──────────────────────────────────── → note 1
├── Required Railway settings
│   ├── Public Networking (HTTP Proxy port 8080) ──── → note 1
│   ├── Volume (required, /data) ──────────────────── → note 1
│   └── Variables (PORT/TOKEN/STATE_DIR/WORKSPACE) ── → note 1
├── Connect a channel ─────────────────────────────── → note 1 (link-out /channels/*)
├── Backups & migration (openclaw backup create) ──── → note 1 (link-out /cli/backup)
└── Next steps ────────────────────────────────────── → note 1 (link-out /channels, /gateway/configuration, /install/updating)
raspberry-pi.md
├── Hardware compatibility (Pi-model RAM matrix) ──── → note 2 (oc_install_raspberry_pi)
├── Prerequisites ─────────────────────────────────── → note 2
├── Setup (9 Steps: flash / SSH / update / Node 24 /
│   swap / install / onboard / verify / Control UI) ─ → note 2
├── Performance tips (USB SSD / compile cache /
│   gpu_mem / systemd drop-in / linger) ───────────── → note 2
├── Recommended model setup (cloud API models JSON) ─ → note 2
├── ARM binary notes ──────────────────────────────── → note 2
├── Persistence and backups ───────────────────────── → note 2
├── Troubleshooting (OOM / slow / service / ARM /
│   WiFi drops) ───────────────────────────────────── → note 2
├── Next steps ────────────────────────────────────── → note 2 (link-out)
└── Related ───────────────────────────────────────── → note 2 (link-out /install, /vps, /platforms)
render.md
├── Prerequisites ─────────────────────────────────── → note 3 (oc_install_render)
├── Deploy with a Render Blueprint ────────────────── → note 3
├── Understanding the Blueprint (render.yaml + table) → note 3
├── Choosing a plan (Free/Starter/Standard table) ── → note 3
├── After deployment → Access the Control UI ──────── → note 3
├── Render Dashboard features
│   ├── Logs ──────────────────────────────────────── → note 3
│   ├── Shell access ──────────────────────────────── → note 3
│   ├── Environment variables ─────────────────────── → note 3
│   └── Auto-deploy ───────────────────────────────── → note 3
├── Custom domain ─────────────────────────────────── → note 3
├── Scaling (vertical / horizontal) ───────────────── → note 3
├── Backups and migration ─────────────────────────── → note 3 (link-out /cli/backup)
├── Troubleshooting (won't-start / cold-start /
│   data-loss / health-check ×4) ──────────────────── → note 3
└── Next steps ────────────────────────────────────── → note 3 (link-out)
uninstall.md
├── Easy path (CLI still installed) — uninstall /
│   dry-run / non-interactive / 6 manual steps ────── → note 4 (oc_install_uninstall)
├── Manual service removal (CLI not installed)
│   ├── macOS (launchd bootout + plist rm) ────────── → note 4
│   ├── Linux (systemd user unit disable + rm) ────── → note 4
│   └── Windows (schtasks /Delete + Remove-Item) ──── → note 4
├── Normal install vs source checkout
│   ├── Normal install (install.sh/npm/pnpm/bun) ──── → note 4
│   └── Source checkout (git clone) ──────────────── → note 4
└── Related ───────────────────────────────────────── → note 4 (link-out /install, /install/migrating)
updating.md
├── Recommended: openclaw update (channels/version/
│   dry-run/json diagnostics) ─────────────────────── → note 5 (oc_install_updating)
├── Switch between npm and git installs ───────────── → note 5
├── Alternative: re-run the installer ─────────────── → note 5
├── Alternative: manual npm/pnpm/bun ──────────────── → note 5
│   └── Advanced npm install topics (read-only tree /
│       hardened systemd / disk-space preflight) ──── → note 5
├── After updating (Run doctor / Restart / Verify) ── → note 5
├── Rollback (Pin a version npm / Pin a commit src) ─ → note 5
├── If you are stuck ──────────────────────────────── → note 5 (link-out /gateway/troubleshooting)
├── Auto-updater (update.auto schema + channel table +
│   checkOnStart / NO_AUTO_UPDATE / handoff) ──────── → note 6 (oc_install_updating_auto_updater)
└── Related ───────────────────────────────────────── → notes 5 + 6 (link-out /install, /gateway/doctor, /install/migrating)
upstash.md
├── Prerequisites ─────────────────────────────────── → note 7 (oc_install_upstash)
├── Create a Box ──────────────────────────────────── → note 7
├── Connect with an SSH tunnel ────────────────────── → note 7
├── Install OpenClaw (npm -g) ─────────────────────── → note 7
├── Run onboarding (--install-daemon) ─────────────── → note 7
├── Start the Gateway (bind lan / nohup) ──────────── → note 7
├── Auto-restart (Box init script) ────────────────── → note 7
├── Troubleshooting (frozen SSH / clean config) ──── → note 7
└── Related ───────────────────────────────────────── → note 7 (link-out /gateway/remote, /gateway/security, /install/updating)
```
No orphaned sections. All `/channels/*`, `/gateway/*`, `/cli/*`, `/install/*` sibling, `/vps`, `/platforms` references are link-outs to their owning sub-plans, not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| updating.md (1,405w, 18 fence-pairs, 9 H2 / 6 H3, mixed BB) | notes 5 (`oc_install_updating`, procedure) + 6 (`oc_install_updating_auto_updater`, model) | 18 code fences exceeds the ≤6-per-note cap, and the page mixes a hands-on update/rollback **procedure** with a distinct auto-updater **configuration model** (`update.auto` JSON5 schema + channel-behavior table + flags + control-plane handoff). Splitting keeps each note one BB, ≤6 fences, and ≤700w. |
| railway.md / raspberry-pi.md / render.md / uninstall.md / upstash.md | 1 note each (no split) | Each is ≤1,016 body words (well under 2,500) and a single coherent deploy/lifecycle **procedure** for one host/operation; uninstall's 12 fences and raspberry-pi's 12 fences are reproduced selectively (≤6 verbatim per note, the rest summarized) so no fence-cap split is needed. |

## Summary Statistics & Building Block Distribution

- Source pages: **6** (4,299 body words, 54 fence-pairs). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×6** (notes 1–5, 7) · **model ×1** (note 6, auto-updater config schema).
- Est. digest words ~3,510 (avg ~500/note); all notes ≤700w, ≤6 code fences, ≤400 lines, one building_block each (within master density caps).
- Source code fences (54 pairs) distribute across the procedure notes; each note reproduces only the load-bearing snippets verbatim (deploy env vars, SSH-tunnel command, `render.yaml` Blueprint, service-removal commands, `update.auto` JSON5) and summarizes the rest to stay ≤6.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Sibling `oc_install_*` docs in THIS series are marked **(planned, this series)** and count toward the 10-doc
> corpora). `entry_openclaw_docs` is created as a master pre-step (W1) and is the G7/G8 inbound-link source
> note at `resources/documentation/openclaw/oc_*.md`. No padding — terms/snippets/docs discarded if not used by
> the source page.

### oc_install_railway (9t · 11s · 12d · 2r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product; relevance: this is the product Railway one-click-deploys.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the always-on service that bridges chat platforms to agents; relevance: the Railway service runs the OpenClaw Gateway.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential for authenticated access; relevance: `OPENCLAW_GATEWAY_TOKEN` is the admin token the Control UI authenticates with.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secure storage/injection of credentials; relevance: the gateway token + provider keys are set as Railway Variables (treated as admin secrets).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end that routes external traffic to a backend; relevance: Railway HTTP Proxy fronts port 8080 and exposes the public domain.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — keeping config/sessions across restarts; relevance: the `/data` Railway Volume preserves `openclaw.json`, `auth-profiles.json`, channel state, and sessions across redeploys.
- [Blue-Green Deployment](../../term_dictionary/term_blue_green_deployment.md) — redeploy-without-state-loss release pattern; relevance: Railway redeploys swap the service while the attached volume keeps state.
- [Docker](../../term_dictionary/term_docker.md) — container image runtime; relevance: Railway builds and runs OpenClaw as a container image.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: the Control UI reaches the hosted Gateway over its WebSocket protocol behind the HTTP Proxy.

**Docs**
- [oc_install_render](oc_install_render.md) (planned, this series) — Render IaC deploy; relevance: the parallel managed-cloud deploy sharing the `/data`-disk state-persistence pattern.
- [oc_install_upstash](oc_install_upstash.md) (planned, this series) — Upstash Box deploy; relevance: the other one-click/managed self-host alternative.
- [oc_install_updating](oc_install_updating.md) (planned, this series) — update lifecycle; relevance: railway.md "Next steps" links here to keep the deployed instance current.
- [cc_enterprise_deployment_options](../claude_code/cc_enterprise_deployment_options.md) — hosted-agent deployment options; relevance: analogous managed/hosted coding-agent deploy choices.
- [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting + provisioning + scaling; relevance: same hosted-agent provisioning/persistence concerns.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — always-on hosted sessions; relevance: the hosted-on-cloud always-running pattern Railway provides.
- [hermes_installation](../hermes_agent/hermes_installation.md) — Hermes install overview; relevance: sibling coding-agent install baseline the deploy paths mirror.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway architecture; relevance: explains the messaging-gateway service Railway hosts.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: analog of Control-UI-over-public-domain + token auth.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — gateway services + profiles; relevance: the gateway-as-a-managed-service model Railway runs.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: the HTTP-proxy-fronts-gateway pattern (port 8080).

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service codebase; relevance: the exact service Railway hosts.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level product/CLI repo; relevance: the product/CLI being deployed.

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — shared-secret/token/password auth-mode selection; relevance: `OPENCLAW_GATEWAY_TOKEN` selects the token auth mode.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — gateway credential/secret handling; relevance: how the gateway loads the token + provider secrets set as Variables.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config loader; relevance: the runtime config the `OPENCLAW_*` env vars populate.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env resolution; relevance: resolves `OPENCLAW_GATEWAY_PORT`/`STATE_DIR`/`WORKSPACE_DIR` at boot.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WebSocket listener; relevance: the server that binds port 8080 behind Railway's HTTP Proxy.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: how `/openclaw` Control UI authenticates with the shared secret.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup wiring; relevance: server boot path that enforces the token on first request.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect through a proxy; relevance: connecting to the gateway behind Railway's HTTP Proxy.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: channels reconnect after each Railway redeploy.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applying the Variables-driven config without a full rebuild.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding/setup config writer; relevance: `openclaw onboard` via Railway's shell writes the same config.

### oc_install_raspberry_pi (9t · 12s · 12d · 3r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the Pi runs an always-on OpenClaw Gateway.
- [ARM](../../term_dictionary/term_arm.md) — ARM64/aarch64 CPU architecture; relevance: Pi is ARM64; the note covers `linux-arm64`/`aarch64` binary caveats.
- [Node.js](../../term_dictionary/term_node_js.md) — JavaScript runtime; relevance: Node 24 install via NodeSource is step 4 of setup.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell remote access; relevance: headless setup is entirely over SSH, plus the Control-UI tunnel.
- [Tunneling](../../term_dictionary/term_tunneling.md) — port-forward over an encrypted channel; relevance: the `ssh -N -L 18789:127.0.0.1:18789` tunnel reaches the Control UI.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the bridge service; relevance: the Pi runs only the Gateway (models run in the cloud).
- [Model Failover](../../term_dictionary/term_model_failover.md) — falling back to an alternate model; relevance: the recommended `model.fallbacks` cloud-model config.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — state across restarts; relevance: `~/.openclaw` state + workspace survive reboots.
- [Cron](../../term_dictionary/term_cron.md) — time-based scheduling; relevance: the timezone is set because it is "important for cron and reminders."

**Docs**
- [oc_install_upstash](oc_install_upstash.md) (planned, this series) — Upstash Box deploy; relevance: the other Linux/SSH-tunnel self-host path.
- [oc_install_updating](oc_install_updating.md) (planned, this series) — update lifecycle; relevance: raspberry-pi.md "Next steps" links here.
- [oc_install_uninstall](oc_install_uninstall.md) (planned, this series) — uninstall lifecycle; relevance: removes the Pi's systemd user unit + state.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install + verify; relevance: the headless install-then-verify pattern (status/logs).
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: analog of the Pi troubleshooting (service-won't-start, doctor).
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — always-on hosting; relevance: the cheap always-on personal-AI pattern.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Linux/Nix install; relevance: sibling bare-metal Linux install path.
- [hermes_install_termux_android](../hermes_agent/hermes_install_termux_android.md) — ARM/Android install; relevance: the closest ARM-device self-host analog.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — local vs cloud models; relevance: the "do not run local LLMs on a Pi, use cloud API" guidance.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops (status/logs/restart); relevance: the verify/troubleshoot operations on the Pi service.
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — model/provider config; relevance: the cloud-API model JSON config the Pi uses.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service + systemd drop-in; relevance: the user systemd service the Pi runs.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the onboarding wizard; relevance: `openclaw onboard --install-daemon` is the wizard.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level product/CLI; relevance: the `install.sh` CLI installed on the Pi.

**Snippets**
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — renders/parses the systemd unit; relevance: the `openclaw-gateway.service` user unit the Pi installs.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — linger + env for the user service; relevance: exactly the Pi's `loginctl enable-linger` step so the service survives logout.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config loader; relevance: where the cloud-model JSON config lives.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ordering; relevance: implements the `model.fallbacks` ladder in the Pi config.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: the failover behavior for the Pi's cloud models.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache + respawn; relevance: the `NODE_COMPILE_CACHE` + `OPENCLAW_NO_RESPAWN=1` low-power Pi tuning.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: `openclaw onboard` writes the Pi's config.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway env resolution; relevance: resolves the `~/.openclaw` state/workspace dirs.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: channels reconnect after Pi reboots.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the `Restart=always` supervised-service behavior.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: the `openclaw` CLI entry the Pi invokes (status/onboard).
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling; relevance: how the Pi's cloud-provider API keys are loaded.

### oc_install_render (10t · 11s · 11d · 2r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: deployed on Render via Blueprint.
- [Blue-Green Deployment](../../term_dictionary/term_blue_green_deployment.md) — redeploy-without-state-loss; relevance: declarative Blueprint redeploys with the persistent `/data` disk.
- [CloudFormation](../../term_dictionary/term_cloudformation.md) — declarative IaC stack definition; relevance: Render's `render.yaml` Blueprint is the same declarative-stack/IaC concept.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: `runtime: docker` builds from the repo Dockerfile.
- [Health Check](../../term_dictionary/term_health_check.md) — endpoint probe driving restart; relevance: `healthCheckPath: /health` restarts unhealthy instances.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage/generation; relevance: `generateValue: true` auto-generates a secure `OPENCLAW_GATEWAY_TOKEN`.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the auto-generated gateway token the Control UI uses.
- [DNS](../../term_dictionary/term_dns.md) — domain name resolution; relevance: custom-domain setup via CNAME to `*.onrender.com`.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption / certificates; relevance: Render auto-provisions a TLS certificate for the custom domain.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — state across redeploys; relevance: the persistent `/data` disk (paid plans) keeps state; free tier resets it.
- [Load Balancer](../../term_dictionary/term_load_balancer.md) — traffic distribution across instances; relevance: horizontal scaling needs sticky sessions / external state behind a balancer.

**Docs**
- [oc_install_railway](oc_install_railway.md) (planned, this series) — Railway deploy; relevance: parallel managed-cloud deploy.
- [oc_install_upstash](oc_install_upstash.md) (planned, this series) — Upstash Box deploy; relevance: parallel managed self-host.
- [oc_install_updating](oc_install_updating.md) (planned, this series) — update lifecycle; relevance: Render uses a manual Blueprint sync to update; render.md "Next steps" links here.
- [cc_enterprise_deployment_options](../claude_code/cc_enterprise_deployment_options.md) — deployment options; relevance: IaC/managed deploy analogs.
- [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting/provisioning/scaling; relevance: the vertical/horizontal scaling guidance analog.
- [cc_install](../claude_code/cc_install.md) — baseline install; relevance: the install the Blueprint automates.
- [hermes_installation](../hermes_agent/hermes_installation.md) — install overview; relevance: sibling coding-agent install baseline.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway architecture; relevance: the gateway service the Blueprint provisions.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: Control UI + auto-generated-token auth analog.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops (logs/shell/restart); relevance: the Render Dashboard logs/shell/env operations analog.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service; relevance: the service the `render.yaml` provisions.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — product/CLI + Dockerfile + `render.yaml`; relevance: the repo Render deploys from.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling; relevance: how the gateway loads the Blueprint-generated token.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode selection; relevance: the token-vs-password auth the Blueprint configures.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config; relevance: the runtime config populated by `OPENCLAW_*` envVars.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env resolution; relevance: resolves `OPENCLAW_GATEWAY_PORT`/`STATE_DIR`/`WORKSPACE_DIR` from the Blueprint envVars.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: binds the port Render's health check probes.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect/health error codes; relevance: maps to the `/health` failures Render reports.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup; relevance: the "missing token" startup failure the troubleshooting covers.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: how the onrender.com Control UI authenticates.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — TLS client identity; relevance: the TLS-fronted custom-domain access.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: env-var changes trigger an automatic redeploy/reload.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: channels reconnect after each Render redeploy.

### oc_install_uninstall (9t · 11s · 12d · 3r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product being removed; relevance: the whole note is uninstalling OpenClaw.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway service; relevance: `openclaw gateway stop` + `gateway uninstall` removes the service.
- [Cron](../../term_dictionary/term_cron.md) — time-triggered scheduler; relevance: the Windows `schtasks` Scheduled Task is a cron-like trigger removed here.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the global CLI was installed under a Node global prefix.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: `npm rm -g openclaw` (and pnpm/bun) removes the CLI.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — state/workspace storage; relevance: the state-dir + workspace deletion semantics (`--workspace`, profile state dirs).
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage; relevance: deleting `auth-profiles.json` + credentials in the state dir.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the gateway token stored in state is cleared on removal.
- [SSH](../../term_dictionary/term_ssh.md) — remote shell; relevance: in remote mode the state dir lives on the gateway host, so removal runs there over SSH.

**Docs**
- [oc_install_updating](oc_install_updating.md) (planned, this series) — update lifecycle; relevance: the lifecycle counterpart to uninstall.
- [oc_install_raspberry_pi](oc_install_raspberry_pi.md) (planned, this series) — Pi self-host; relevance: whose systemd user unit this uninstall removes.
- [oc_install_upstash](oc_install_upstash.md) (planned, this series) — Upstash self-host; relevance: whose backgrounded gateway this tears down.
- [cc_uninstall](../claude_code/cc_uninstall.md) — sibling-tool uninstall; relevance: the direct cross-tool uninstall reference.
- [cc_install](../claude_code/cc_install.md) — sibling-tool install; relevance: the install this reverses.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: diagnosing a service still running after uninstall.
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update + uninstall; relevance: the direct sibling-tool uninstall procedure (service + state).
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: `gateway stop`/`uninstall` service operations analog.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — profiles + services; relevance: the per-profile state-dir removal (`--profile`/`OPENCLAW_PROFILE`).
- [hermes_install_windows_native](../hermes_agent/hermes_install_windows_native.md) — Windows install; relevance: the Windows Scheduled Task / state-dir removal analog.
- [hermes_installation](../hermes_agent/hermes_installation.md) — install overview; relevance: the install methods (install.sh/npm/pnpm/bun) this enumerates removing.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the launchd/systemd/schtasks service lifecycle; relevance: the service being uninstalled.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the CLI uninstaller; relevance: `openclaw uninstall` lives here.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the wizard/CLI; relevance: the CLI that ran the install being reversed.

**Snippets**
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — renders the launchd plist; relevance: the `ai.openclaw.gateway.plist` label + plist removed on macOS.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — renders/parses the systemd unit; relevance: the `openclaw-gateway.service` user unit disabled + removed on Linux.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — renders the schtasks argv; relevance: the Windows `OpenClaw Gateway` Scheduled Task removed.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — kills the Windows process tree; relevance: stopping the still-running gateway before task deletion.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart/handoff; relevance: the `launchctl bootout` lifecycle this removal undoes.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process-tree termination; relevance: ensuring the gateway process actually stops on uninstall.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the supervised service being torn down.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the `uninstall`/`gateway stop`/`gateway uninstall` subcommands.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential handling; relevance: the `auth-profiles.json` credentials deleted with state.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env resolution; relevance: resolves `OPENCLAW_STATE_DIR`/`OPENCLAW_CONFIG_PATH` the manual `rm -rf` targets.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration/import helper; relevance: the workspace-preserve-vs-delete decision before migrating away.

### oc_install_updating (10t · 12s · 12d · 3r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product being updated; relevance: `openclaw update` is the subject.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: npm package update + temp-prefix staged swap + EACCES recovery + `min-release-age` quarantine.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the managed-service Node-path/engine check before replacing the package.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway service; relevance: stop/restart the Gateway around the package swap.
- [Health Check](../../term_dictionary/term_health_check.md) — readiness probe; relevance: `openclaw health` / `curl /readyz` post-update verify.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential preservation; relevance: the updater preserves state/config/credentials in `~/.openclaw`.
- [Blue-Green Deployment](../../term_dictionary/term_blue_green_deployment.md) — staged swap + rollback; relevance: temp-prefix clean-tree swap, retry-once with `--omit=optional`, and rollback pinning.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — state across updates; relevance: workspace/sessions preserved across the update.
- [Failover](../../term_dictionary/term_failover.md) — fallback/recovery path; relevance: re-run the installer to recover a partially-updated npm install; rollback to a pinned version.
- [Cron](../../term_dictionary/term_cron.md) — scheduling; relevance: bridges to the auto-updater's scheduled-apply model (note 6).

**Docs**
- [oc_install_updating_auto_updater](oc_install_updating_auto_updater.md) (planned, this series) — auto-updater model; relevance: the config-model half split off from this same page.
- [oc_install_uninstall](oc_install_uninstall.md) (planned, this series) — uninstall; relevance: the lifecycle counterpart.
- [oc_install_railway](oc_install_railway.md) (planned, this series) — Railway deploy; relevance: railway.md "Next steps" links here to keep current.
- [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — update + release channels; relevance: the direct sibling-tool update/channel (stable/beta/dev) doc.
- [cc_install](../claude_code/cc_install.md) — install baseline; relevance: re-running the installer for recovery.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install + verify; relevance: the post-update doctor/restart/verify pattern.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — install-failure recovery; relevance: recovering from a failed update (EACCES, half-swapped tree).
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update + uninstall; relevance: the direct sibling-tool update procedure.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: stop/restart/status the Gateway around the swap.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — config precedence; relevance: the updater preserves `~/.openclaw` config across the swap.
- [hermes_faq_install_provider_terminal](../hermes_agent/hermes_faq_install_provider_terminal.md) — install/terminal FAQ; relevance: the "if you are stuck" pnpm/corepack-bootstrap troubleshooting analog.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the supervised service the updater coordinates; relevance: the managed Gateway stopped/restarted around the swap.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the `openclaw update` CLI; relevance: where the update/channel/rollback logic lives.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the wizard/CLI; relevance: the installer re-run path for recovery.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup/config writer; relevance: post-update `openclaw doctor` config migration.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: channels reconnect after the gateway restart.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart/handoff; relevance: the managed-service restart + installed-but-unloaded LaunchAgent recovery the updater performs.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: refreshing service metadata (`gateway install --force`) on update.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the supervised swap-and-restart coordination.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: running the staged npm install in a temp prefix then swapping.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache + respawn; relevance: the respawn behavior after the package tree swaps.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: `--dry-run` previews the planned update actions.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: applying the post-update config without a restart where possible.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the `update`/`update status`/`doctor`/`health` subcommands + flags.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect/health error codes; relevance: the `/readyz` + `gateway status --deep` post-update verification.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env resolution; relevance: resolving the managed-service Node path / package root the updater targets.

### oc_install_updating_auto_updater (9t · 11s · 11d · 2r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the `update.auto` config governs OpenClaw's self-update.
- [Blue-Green Deployment](../../term_dictionary/term_blue_green_deployment.md) — staged spread rollout; relevance: the stable channel applies with deterministic jitter across `stableJitterHours` (spread rollout).
- [Cron](../../term_dictionary/term_cron.md) — periodic scheduling; relevance: `betaCheckIntervalHours` + `stableDelayHours` define the periodic/delayed apply schedule.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the npm engine the detached handoff swaps.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway service; relevance: the control-plane handoff exits + restarts the Gateway out-of-process.
- [Health Check](../../term_dictionary/term_health_check.md) — readiness verify; relevance: post-apply Gateway version + reachability verification.
- [Failover](../../term_dictionary/term_failover.md) — downgrade/recovery override; relevance: `OPENCLAW_NO_AUTO_UPDATE=1` blocks automatic applies for downgrade/incident recovery.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential preservation; relevance: the auto-apply preserves state/credentials like the manual updater.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — state across auto-apply; relevance: sessions/workspace survive the detached-handoff swap.

**Docs**
- [oc_install_updating](oc_install_updating.md) (planned, this series) — manual update procedure; relevance: the procedural half of the same source page.
- [oc_install_railway](oc_install_railway.md) (planned, this series) — Railway deploy; relevance: a deployment that benefits from enabling auto-update.
- [oc_install_render](oc_install_render.md) (planned, this series) — Render deploy; relevance: a deployment that benefits from auto-update.
- [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — update + release channels; relevance: the channel-behavior model analog (stable/beta/latest semantics).
- [cc_enterprise_deployment_options](../claude_code/cc_enterprise_deployment_options.md) — deployment options; relevance: managed-rollout controls analog.
- [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting/scaling; relevance: spread-rollout across hosted fleets.
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update mechanics; relevance: sibling-tool update/channel behavior.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: the control-plane handler + detached-handoff internals analog.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: the restart/verify the auto-apply triggers.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — config precedence; relevance: where the `update.auto` JSON5 block sits in `~/.openclaw/openclaw.json`.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the control-plane `update.run` handler + detached handoff; relevance: where the auto-apply handoff is implemented.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the `update.auto` config + CLI apply path; relevance: where the auto-updater config schema + apply logic live.

**Snippets**
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config loader; relevance: where the `update.auto` JSON5 block is read.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart/handoff; relevance: the detached control-plane handoff (exit + restart) the auto-updater triggers.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: the managed-service metadata refreshed on auto-apply.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron/service notifications; relevance: the periodic update-check + startup update-hint scheduling.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the detached-handoff exit-and-respawn lifecycle.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache + respawn; relevance: `OPENCLAW_NO_RESPAWN` interplay with the auto-apply respawn.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: the planned-apply (`update --yes --json`) the handoff runs.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: applying the new release config after swap.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect/health error codes; relevance: the post-apply reachability verify.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the `update --yes --json` CLI path the detached handoff invokes.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env resolution; relevance: reads `OPENCLAW_NO_AUTO_UPDATE` / `update.checkOnStart` overrides.

### oc_install_upstash (9t · 11s · 12d · 3r)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: hosted on an Upstash Box.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: SSH tunnel for dashboard access + the keepalive/clean-config troubleshooting.
- [Tunneling](../../term_dictionary/term_tunneling.md) — port-forward over SSH; relevance: the `-L 18789:127.0.0.1:18789` port-forward tunnel to the dashboard.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: `sudo npm install -g openclaw` inside the Box.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway service; relevance: `openclaw gateway` bound to LAN, run backgrounded with nohup.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the Node runtime the Box's npm global install requires.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — persistent state; relevance: the keep-alive Box preserves state/config across restarts.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the dashboard token in the URL fragment + the Box API key used as the SSH password.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage; relevance: the Box API key + gateway token are the access secrets.

**Docs**
- [oc_install_raspberry_pi](oc_install_raspberry_pi.md) (planned, this series) — Pi self-host; relevance: the other Linux/SSH-tunnel self-host path.
- [oc_install_railway](oc_install_railway.md) (planned, this series) — Railway deploy; relevance: a managed-cloud alternative.
- [oc_install_render](oc_install_render.md) (planned, this series) — Render deploy; relevance: a managed-cloud alternative.
- [oc_install_updating](oc_install_updating.md) (planned, this series) — update lifecycle; relevance: upstash.md "Related" links here.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — backgrounded hosting; relevance: the backgrounded always-on gateway pattern (nohup).
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install + verify; relevance: the npm-global install + verify pattern.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: the frozen-SSH/clean-config troubleshooting analog.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth over SSH; relevance: the closest SSH-tunneled remote-access auth analog.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: dashboard URL + token access over the tunnel.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Linux install; relevance: the managed-Linux npm-global install path.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: backgrounding/restarting the gateway on the Box.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service + LAN bind; relevance: the backgrounded Gateway run on the Box.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: `openclaw onboard --install-daemon` on the Box.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — product/CLI; relevance: the `openclaw` CLI npm-installed on the Box.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: the `openclaw onboard` flow that writes the Box config.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: the backgrounded gateway re-establishes channels on Box restart.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: the auto-restart init-script analog (vs the Box init script).
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway env resolution; relevance: `gateway.bind lan` + state-dir resolution on the Box.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: the gateway bound to the LAN port 18789 the tunnel forwards.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect through proxy; relevance: the dashboard connecting over the SSH-forwarded local port.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: the `#token=<...>` dashboard auth.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode selection; relevance: the token auth the Box dashboard uses.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: the `openclaw gateway`/`onboard` CLI entry run on the Box.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: the nohup-backgrounded auto-restart behavior.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential handling; relevance: the gateway token + Box API key as access secrets.

## Undigested Terms Plan

| Term | Disposition |
|------|-------------|
| OpenClaw, Gateway, Control UI, Box, Blueprint, Volume/Disk, state dir, workspace | OpenClaw product vocabulary — digested as `oc_*` doc content (subjects of these pages); link `term_openclaw`, `term_messaging_gateway`. No new term_dictionary capture. |
| `OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_PORT`, `OPENCLAW_STATE_DIR`, `OPENCLAW_WORKSPACE_DIR`, `OPENCLAW_NO_AUTO_UPDATE`, `OPENCLAW_NO_RESPAWN` | OpenClaw config/env vars — documented as config inside `oc_*` notes, NOT promoted to term notes. The general concept links existing `term_secrets_manager` / `term_oauth_token`. |
| Railway, Render, Upstash Box, Raspberry Pi, NodeSource | Vendor/host names — documented as deploy targets inside `oc_*` notes; not term notes. |
| Auto-updater, update channel (stable/beta/dev), release channel, rollback, IaC/Blueprint, blue-green / spread rollout | Update/deploy concepts — `update channel` + auto-updater behavior digested in note 6 (model); link existing `term_blue_green_deployment`, `term_cloudformation` (IaC analog), `term_failover` (rollback/incident recovery). No new captures. |


## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). All gates must pass before commit.

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean on all 7 notes (YAML field order, `## Overview`/`## Related Notes`/`## References`, `**Source**`/`**Last Updated**`/`**Status**` footer, no forbidden YAML fields). |
| G2 | Grounding | Each note's claims diff-verified against `inbox/openclaw_docs/install/<page>.md`; commands/env vars/JSON reproduced verbatim; no invented behavior. |
| G3 | Density + Coverage | Each note ≤2,500w / ≤6 code fences / ≤400 lines / one building_block; every source H2/H3 from the Section Coverage Map maps to a note (no orphans, no over-compression). |
| G4 | Cross-Reference | Each note's `## Related Notes` has ≥6 relevance-selected `term_dictionary` terms (each with a relevance statement) + relevant `repo_openclaw*` + sibling `oc_*` + `cc_*`/`pi_*` docs + `snippet_openclaw_*`. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken relative links post-reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + the inlinks below). |
| G8 | In-degree ≥1 | `note_links` query confirms in-degree ≥1 for all 7 notes (anti-island). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_install_railway oc_install_raspberry_pi oc_install_render oc_install_uninstall oc_install_updating oc_install_updating_auto_updater oc_install_upstash"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_ cross-link
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING $SIBLING_PREFIX LINK in $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code fences (cap 6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_install_railway | procedure | 420 | ≤2 | ✅ |
| 2 | oc_install_raspberry_pi | procedure | 620 | ≤6 (12 source → reproduce load-bearing only) | ✅ |
| 3 | oc_install_render | procedure | 560 | ≤4 | ✅ |
| 4 | oc_install_uninstall | procedure | 470 | ≤6 (12 source → reproduce load-bearing only) | ✅ |
| 5 | oc_install_updating | procedure | 680 | ≤6 (of updating's 18 — auto-updater fences move to note 6) | ✅ |
| 6 | oc_install_updating_auto_updater | model | 380 | ≤2 (the `update.auto` JSON5 + handoff snippet) | ✅ |
| 7 | oc_install_upstash | procedure | 380 | ≤6 (7 source → reproduce load-bearing only) | ✅ |

No note approaches the 2,500w / 400-line caps. The only fence-cap pressure is on raspberry-pi (12), uninstall (12), upstash (7), and updating (18 → split): each note reproduces only the load-bearing commands verbatim and summarizes the remainder; updating's split keeps both halves ≤6.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all listed existing sources verified present 2026-06-20):

- `entry_openclaw_docs.md` (created W1) → **all 7 notes** (primary anti-island source).
- `repo_openclaw_gateway.md` → notes 1, 2, 3, 4, 5, 6, 7 (the Gateway service every install/lifecycle note operates).
- `repo_openclaw.md` → notes 1, 3, 4, 5 (top-level product/CLI install + update + uninstall).
- `repo_openclaw_cli_wizard.md` → notes 2, 4, 7 (the `openclaw onboard` wizard these run).
- `term_openclaw.md` → notes 5, 4 (canonical lifecycle ops for the product).
- `term_arm.md` → note 2; `term_ssh.md` / `term_tunneling.md` → notes 2, 7; `term_npm.md` → notes 4, 5.
- `cc_uninstall.md` → note 4; `cc_update_and_release_channels.md` → notes 5, 6 (reciprocal sibling-tool cross-links).

## Pacing Rules (inherited from master)

One execution phase, 7 notes (within the ~30-agent fan-out cap). Re-read each source page before authoring; reproduce commands/env vars/JSON verbatim; one BB per note. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. Commit + push the sub-plan as one wave (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment — per-note mapping LOCKED at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — 9/9 PASS → READY** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the draft `## Candidate Cross-References` with `## Per-Note Related Notes
**raised floors (≥8 terms · ≥10 snippets · ≥10 docs per note)**, grouped **Terms / Docs / Repos / Snippets**,
each link rendered with a relative path + a `relevance:` statement. All 7 notes re-grounded against a fresh
re-read of the 6 source pages under `inbox/openclaw_docs/install/`.

relative-path resolution from `resources/documentation/openclaw/` + `SELECT 1 FROM notes WHERE note_id=…`).
The only non-existing targets are intentional **(planned, this series)** references: the 6 sibling `oc_install_*`
docs and `entry_openclaw_docs.md` (created at master pre-step W1) — these count toward the 10-doc floor but

**Per-note counts (terms · snippets · docs · repos; floors met).**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_install_railway | 9 | 11 | 12 (8/4) | 2 | ✅ |
| oc_install_raspberry_pi | 9 | 12 | 12 (8/4) | 3 | ✅ |
| oc_install_render | 11 | 11 | 11 (7/4) | 2 | ✅ |
| oc_install_uninstall | 9 | 11 | 12 (8/4) | 3 | ✅ |
| oc_install_updating | 10 | 12 | 12 (8/4) | 3 | ✅ |
| oc_install_updating_auto_updater | 9 | 11 | 11 (7/4) | 2 | ✅ |
| oc_install_upstash | 9 | 11 | 12 (7/5) | 3 | ✅ |

**New-term candidates: 0.** Re-read surfaced no new vault-reusable cross-cutting term lacking both a doc-page
home and an existing note. Best-fit-glossary check is N/A (no captures). The init-system primitives
(`systemd`/`launchd`/`daemon`/`swap`/`node_compile_cache`) were re-confirmed DB-MISSING and remain
documented in prose inside the `oc_*` notes). The existing-term link set is rich enough that the floors are met

**Density unchanged.** Re-read confirmed the measured word counts in the Source table are exact (updating
1,405w / raspberry-pi 1,016w / render 763w / railway 328w / uninstall 499w / upstash 288w). The single split
(`updating` → procedure + auto-updater model) remains correct; no further splits needed.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 Format · G2 Grounding · G3 Density+Coverage · G4 Cross-Reference · G5 Ghost · G6 Broken-link · G7 Discoverability · G8 in-degree≥1, all with pass criteria. |
| CP4 | Plan size manageable | **PASS** | 7 planned notes (1 split), single execution phase — well under the ≤30 cap. |
| CP5 | Note format aligned + DERIVED | **PASS** | Format inherited from master `## Format Definition (Shared)`, itself derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora; `## Overview` / `## Related Notes` / `## References` + bold `**Source**`/`**Last Updated**`/`**Status**` footer; forbidden-field list inherited. |
| CP6 | Borderline density → split | **PASS** | Density Re-Assessment: every note ≤700w / ≤6 fences / ≤400 lines; only `updating` (1,405w, 18 fences) split into procedure + model; no other borderline note. |
| CP7 | Source word counts measured | **PASS** | Re-measured 6/6 pages (`sed` strip frontmatter + `wc -w`): updating 1,405 · raspberry-pi 1,016 · render 763 · railway 328 · uninstall 499 · upstash 288 — exact match to the Source table (ratio 1.00). |
| CP8 | Undigested Terms Plan + Authoring Reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned, 0 TBD); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, multi-source mandate inherited from master W5, applies only if a capture is added). |
| CP8f | Slug specificity + all-notes dedup/collision | **PASS** | 0 new `term_*` slugs (no specificity audit targets). Doc-note collision audit: all 7 `oc_install_*` slugs are install/lifecycle host-specific (railway/raspberry_pi/render/uninstall/updating/auto_updater/upstash) — none duplicates an existing term or doc note; `term_systemd`/`term_launchd`/`term_daemon`/`term_swap_memory`/`term_node_compile_cache` re-confirmed DB-MISSING (correctly not created). |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` covers all 7 notes with outside-folder sources (`entry_openclaw_docs`, `repo_openclaw_gateway`, `repo_openclaw`, `repo_openclaw_cli_wizard`, `term_*`, `cc_uninstall`, `cc_update_and_release_channels`); G7/G8 in the gate table mark in-degree≥1 as a gated execution check (anti-island). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
