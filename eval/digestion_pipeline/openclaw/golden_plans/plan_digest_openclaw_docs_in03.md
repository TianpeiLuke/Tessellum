---
title: Sub-Plan in03 — OpenClaw Docs: Install (Hostinger, Installer Internals, Kubernetes, macOS VM, Migration, Migrating from Claude)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["install/hostinger", "install/installer", "install/kubernetes", "install/macos-vm", "install/migrating", "install/migrating-claude"]
---

# Sub-Plan in03: Install

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` + source-mirrored body + `## Related Notes` + `## References` + bold footer), dedup-before-create (term_dictionary AND documentation/ AND repo_openclaw*), the 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master and are NOT re-derived here.

## Scope

The six Install pages that cover OpenClaw's **deployment-target** and **migration** surface: a managed/1-click
host (Hostinger), the internals of the three official installer scripts (`install.sh` / `install-cli.sh` /
`install.ps1`), a Kubernetes/Kustomize deployment recipe, a sandboxed macOS VM path (Lume + hosted Mac
providers, the iMessage use case), the migration hub (cross-system import, machine-to-machine move, in-place
plugin upgrade), and the Claude-specific import provider. This is **Phase A, Priority P1**: getting OpenClaw
running and moving an existing install are first-run / day-2 operational tasks, and these pages establish the
state-directory / installer-flag / migration-flow vocabulary that the rest of the Install section (in01, in02,
in04, in05) and the Gateway / CLI sub-plans reference.

These pages are almost entirely **procedural** (deploy/migrate/install runbooks). The code-side counterparts —
`repo_openclaw`, `repo_openclaw_cli_wizard` (the installer/onboarding wizard), `repo_openclaw_gateway`,
`repo_openclaw_sessions`, `repo_openclaw_channels`, `repo_openclaw_extensions` (migration providers live here) —
are LINKED, not recreated (master dedup policy). The migration content overlaps conceptually with the
existing Claude Code docs corpus (`cc_install`, `cc_devcontainer_setup`, `cc_github_actions`,
`cc_migrate*`-style imports), which are cross-linked rather than duplicated.

**Source**: OpenClaw docs, 6 pages, **5,991 measured words**. **Planned: 6 notes** (no split — see Split Decisions).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Hostinger | install/hostinger | 507 | 0 | 7 | 0 | procedure |
| Installer internals | install/installer | 2,052 | 27 | 7 | 7 | procedure |
| Kubernetes | install/kubernetes | 842 | 15 | 12 | 8 | procedure |
| macOS VMs | install/macos-vm | 958 | 15 | 16 | 2 | procedure |
| Migration guide | install/migrating | 789 | 4 | 4 | 3 | procedure |
| Migrating from Claude | install/migrating-claude | 843 | 8 | 9 | 0 | procedure |

Word counts via `wc -w` on the mirror; code-block counts via `grep -cE '^\s*```' / 2` (counts MDX-indented
fences inside `<Tab>`/`<Step>` components). Hostinger has 0 code fences (its `<Steps>` are prose). Installer is
the densest at 2,052w / 27 fences but stays a single coherent procedure (see Split Decisions).

## Content Strategy

- **Prioritize**: (1) the **machine-to-machine move** runbook (state directory layout `~/.openclaw/`,
  auth-profiles, sessions, channel state — the most reusable migration knowledge), (2) the **installer-script
  internals** (flags, env vars, npm-vs-git, CI/headless), and (3) the **Claude import** provider (what gets
  imported vs archive-only, dry-run → apply → doctor flow) — these three are the highest operational value.
- **Split**: none. Each page maps cleanly to one procedure note ≤2,500w / ≤6 code blocks. The installer page
  (2,052w / 27 fences) is the only borderline case; it stays a single note by reproducing only the
  representative `curl | bash` invocation + the flags/env-var tables, NOT every per-script example tab
  (see Density Re-Assessment). One BB per note (all `procedure`).
- **Link-out (not duplicated)**: generic Install overview + Docker + DigitalOcean + VPS + Node troubleshooting +
  uninstall/updating pages belong to in01/in02/in04/in05 (linked as siblings, planned); `openclaw migrate`,
  `openclaw onboard`, `openclaw doctor`, `openclaw status`, `openclaw channels` CLI references belong to the
  CLI sub-plans (cl01–cl09); channel setup (Telegram/WhatsApp/iMessage) belongs to the Channels sub-plans
  (ch01–ch06); gateway configuration / remote / Tailscale belong to the Gateway sub-plans (gw01–gw07). These
  are referenced by relative link, never inlined. Hermes import (`migrating-hermes`) is in04.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_install_hostinger.md` | procedure | hostinger.md: Prerequisites, Option A 1-Click, Option B VPS, Verify, Troubleshooting, Next steps | 480 | Host a persistent OpenClaw Gateway on Hostinger via the 1-Click managed deployment (instant Ready-to-Use AI credits) or a Docker-on-VPS install managed through hPanel's Docker Manager; channel selection, verification, and troubleshooting. |
| 2 | `oc_install_installer.md` | procedure | installer.md: install.sh, install-cli.sh, install.ps1 (flow + flags + env vars), CI and automation, Troubleshooting | 640 | How the three official installer scripts work — `install.sh` (macOS/Linux/WSL global npm/git), `install-cli.sh` (local-prefix `~/.openclaw`, pinned Node, no root), `install.ps1` (Windows) — their flow, flags, environment variables, and non-interactive CI usage. |
| 3 | `oc_install_kubernetes.md` | procedure | kubernetes.md: Why not Helm, What you need, Quick start, Kind, Step by step, What gets deployed, Customization, Re-deploy, Teardown, Architecture notes, File structure | 600 | Deploy the OpenClaw Gateway to a Kubernetes cluster with Kustomize: `deploy.sh` flow, local Kind testing, the deployed resources (Deployment/Service/PVC/ConfigMap/Secret), provider-key and namespace customization, security hardening, and exposing beyond port-forward. |
| 4 | `oc_install_macos_vm.md` | procedure | macos-vm.md: Recommended default, VM options (Lume / hosted Mac), Quick path, steps 1–8, iMessage integration, golden image, 24/7, Troubleshooting | 600 | Run OpenClaw in a sandboxed macOS VM (local Lume on Apple Silicon or a hosted Mac provider) for isolation and macOS-only capabilities: create/SSH/install/configure the VM, run it headless, the iMessage (`imsg`) integration, and saving a resettable golden image. |
| 5 | `oc_install_migrating.md` | procedure | migrating.md: Import from another agent system, Move OpenClaw to a new machine (state dir, steps, pitfalls, checklist), Upgrade a plugin in place | 560 | The OpenClaw migration hub: the three migration paths (cross-system import, machine-to-machine move, in-place plugin upgrade), the state-directory layout to copy (`~/.openclaw/` config/auth/sessions/channel-state/workspace), tar/scp/doctor steps, common pitfalls, and a verification checklist. |
| 6 | `oc_install_migrating_claude.md` | procedure | migrating-claude.md: Two ways to import, What gets imported, What stays archive-only, Source selection, Recommended flow, Conflict handling, JSON output, Troubleshooting | 580 | Importing local Claude Code / Claude Desktop state into OpenClaw via the bundled Claude migration provider: onboarding-wizard vs `openclaw migrate` CLI, what is auto-imported (CLAUDE.md → AGENTS.md/USER.md, MCP servers, skills/commands) vs archive-only, source selection, the dry-run → apply-with-backup → doctor flow, conflict handling, and JSON-for-automation. |

## Section Coverage Map

```
hostinger.md (507w)
├── Prerequisites ───────────────────────────────────── → note 1 (oc_install_hostinger)
├── Option A: 1-Click OpenClaw (purchase, channel, finish) → note 1
├── Option B: OpenClaw on VPS (purchase, configure, deploy) → note 1
├── Verify your setup ───────────────────────────────── → note 1
├── Troubleshooting ─────────────────────────────────── → note 1
├── Next steps (Channels, Gateway config) ───────────── → note 1 (link-out)
└── Related (Install overview, VPS, DigitalOcean) ───── → note 1 (References / siblings)
installer.md (2,052w)
├── Quick commands (install.sh / install-cli.sh / install.ps1) → note 2 (oc_install_installer)
├── install.sh (Flow, Source checkout detection, Examples,
│     Flags reference, Env vars reference) ──────────── → note 2
├── install-cli.sh (Flow, Examples, Flags, Env vars) ── → note 2
├── install.ps1 (Flow, Examples, Flags, Env vars) ───── → note 2
├── CI and automation ───────────────────────────────── → note 2
├── Troubleshooting ─────────────────────────────────── → note 2
└── Related (Install overview, Updating, Uninstall) ─── → note 2 (References / siblings)
kubernetes.md (842w)
├── Why not Helm? ───────────────────────────────────── → note 3 (oc_install_kubernetes)
├── What you need ───────────────────────────────────── → note 3
├── Quick start ─────────────────────────────────────── → note 3
├── Local testing with Kind ─────────────────────────── → note 3
├── Step by step (1 Deploy A/B, 2 Access) ────────────── → note 3
├── What gets deployed ──────────────────────────────── → note 3
├── Customization (Agent instructions, Gateway config,
│     Add providers, Custom namespace/image, Expose) ── → note 3
├── Re-deploy / Teardown ────────────────────────────── → note 3
├── Architecture notes ──────────────────────────────── → note 3
├── File structure ──────────────────────────────────── → note 3
└── Related (Docker, Docker VM runtime, Install) ────── → note 3 (References / siblings)
macos-vm.md (958w)
├── Recommended default (most users: VPS / dedicated / hybrid) → note 4 (oc_install_macos_vm)
├── macOS VM options (Local Lume, Hosted Mac providers) → note 4
├── Quick path (Lume) ───────────────────────────────── → note 4
├── What you need (Lume) ────────────────────────────── → note 4
├── Steps 1–8 (Install Lume → Create VM → Setup Assistant
│     → IP → SSH → Install OpenClaw → Configure channels
│     → Run headlessly) ──────────────────────────────── → note 4
├── Bonus: iMessage integration ─────────────────────── → note 4
├── Save a golden image / Running 24/7 ──────────────── → note 4
├── Troubleshooting ─────────────────────────────────── → note 4
└── Related docs (VPS, Nodes, Gateway remote, iMessage) → note 4 (References / siblings)
migrating.md (789w)
├── Import from another agent system (Claude / Hermes cards,
│     openclaw migrate, onboard --flow import) ───────── → note 5 (oc_install_migrating)
├── Move OpenClaw to a new machine (state dir contents) → note 5
│   ├── Migration steps (stop+backup, install, copy, doctor) → note 5
│   ├── Common pitfalls (profile mismatch, partial copy,
│   │     permissions, remote mode, secrets) ──────────── → note 5
│   └── Verification checklist ───────────────────────── → note 5
├── Upgrade a plugin in place (Matrix migration pointer) → note 5
└── Related (openclaw migrate, Install, Doctor, Uninstall) → note 5 (References / siblings)
migrating-claude.md (843w)
├── Two ways to import (Onboarding wizard / CLI) ─────── → note 6 (oc_install_migrating_claude)
├── What gets imported (instructions/memory, MCP, skills/cmds) → note 6
├── What stays archive-only ─────────────────────────── → note 6
├── Source selection (--from project vs global home) ── → note 6
├── Recommended flow (preview → apply+backup → doctor → restart) → note 6
├── Conflict handling (--overwrite) ─────────────────── → note 6
├── JSON output for automation ──────────────────────── → note 6
├── Troubleshooting ─────────────────────────────────── → note 6
└── Related (migrate, migrating, migrating-hermes, onboard,
      doctor, agent-workspace) ───────────────────────── → note 6 (References / siblings)
```
No orphaned sections. Every H2/H3 maps to exactly one note. Cross-cutting CLI commands (`openclaw migrate`,
`onboard`, `doctor`, `status`, `channels`), channel-setup details, and gateway-config / remote pages are
link-outs to the CLI / Channels / Gateway sub-plans (not duplicated).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 6 pages are single-BB procedures ≤2,052w. The densest, `installer.md` (2,052w / 27 fences), stays ONE note: it is a single coherent "how the installers work" reference, well under the 2,500w cap, and density is controlled by reproducing one representative `curl \| bash` invocation per script plus the flags/env-var tables (verbatim) rather than every per-script example tab (≤6 code blocks; see Density Re-Assessment). No page mixes building blocks. |

## Summary Statistics & Building Block Distribution

- Source pages: **6** (5,991 measured words). New `oc_` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×6** (notes 1–6). No concept/model/argument notes (Install pages are runbooks).
- Est. digest words **~3,460** (avg ~577/note); all ≤640w, well under the 2,500w cap.
- Source code fences total **69** (0 / 27 / 15 / 15 / 4 / 8) — distributed across 6 notes; each note keeps
  **≤6** fences by reproducing only representative invocations + verbatim config/secret snippets and pointing
  to the source for exhaustive example tabs.
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** every note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (with ≥5 EXISTING
  relevance statements + DB-verification of every EXISTING target are in
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` below. Achieved per-note:
  n1 9t·11s·11d · n2 8t·12s·11d · n3 9t·11s·11d · n4 10t·11s·11d · n5 11t·12s·11d · n6 10t·12s·11d.
  snippet corpus.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (re-read source 2026-06-21;
> Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms
> `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`; snippets
> `../../code_snippets/snippet_Y.md`; repos `../../../areas/code_repos/repo_Y.md`; entry points
> `../../../0_entry_points/entry_Y.md`. Render each link as `- [Name](relpath.md) — what; relevance: why THIS note`.

### note 1 — oc_install_hostinger (9t · 11s · 11d)

**Terms (9)**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: the product Hostinger hosts (1-Click managed or Docker-on-VPS).
- [Docker](../../term_dictionary/term_docker.md) — OS-level containerization; relevance: Hostinger deploys OpenClaw as a Docker container managed through hPanel's Docker Manager (logs/restart/update).
- [LLM](../../term_dictionary/term_llm.md) — large language model behind the agent; relevance: "Ready-to-Use AI" credits front an LLM, or you BYO an Anthropic/OpenAI/Gemini/xAI key at setup.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: one of the BYO provider keys offered during Hostinger checkout.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the layer binding a chat platform to the gateway; relevance: Hostinger setup connects WhatsApp (QR) and Telegram (BotFather token) channels.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed secret storage; relevance: the auto-generated Gateway token + provider API keys must be stored/handled securely.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime that drives an LLM agent's tool loop; relevance: OpenClaw is the harness/gateway being stood up on Hostinger.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — one-time pairing-code handshake to authorize a DM user; relevance: the Telegram troubleshooting step (send the pairing code inside the OpenClaw chat) is exactly this handshake.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-applying an op leaves state unchanged; relevance: hPanel "Update" re-pulls the latest image / re-deploys safely without reconfiguration.

**Docs (11; ≥5 existing)**
- [cc_install](../claude_code/cc_install.md) — Claude Code install overview; relevance: sibling-tool managed-install precedent for a coding agent.
- [pi_quickstart](../pi/pi_quickstart.md) — Pi agent first-run; relevance: parallel "purchase/host → connect → say hi" quick-start flow for a coding-agent gateway.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents on hosted infra; relevance: same managed-host deployment surface as Hostinger.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp QR-login adapter; relevance: the WhatsApp QR channel Hostinger connects.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/channel architecture; relevance: explains the gateway+channel model Hostinger packages.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — channel concepts for a coding agent; relevance: backs the "select a messaging channel" step.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker volumes + container supervision; relevance: the Docker-Manager-on-VPS persistence/restart model.
- [oc_install_installer](oc_install_installer.md) — installer-script internals (planned, this series); relevance: the non-managed alternative to a 1-Click host.
- [oc_install_kubernetes](oc_install_kubernetes.md) — k8s deploy (planned, this series); relevance: alternative always-on deploy target.
- [oc_install_macos_vm](oc_install_macos_vm.md) — macOS VM deploy (planned, this series); relevance: alternative deploy target.
- [oc_install_migrating](oc_install_migrating.md) — migration hub (planned, this series); relevance: day-2 op (move a Hostinger install elsewhere).

**Repos (4)**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product being hosted (code↔docs).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway process; relevance: the Docker-run process Hostinger manages.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: WhatsApp/Telegram connect.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: the WhatsApp/Telegram adapters configured at setup.

**Snippets (11)**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard writes openclaw.json; relevance: the VPS "Configure OpenClaw" fields land in this config.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap/first-run; relevance: what runs when the container starts.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway auth startup with the gateway token; relevance: the auto-generated Gateway token guards the dashboard.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: accessing the hPanel-launched dashboard.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — provider-key/secret resolution; relevance: BYO API keys vs Ready-to-Use credits.
- [snippet_hermes_agent_gw_platform_whatsapp_connect](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_connect.md) — WhatsApp connect/QR; relevance: the WhatsApp channel step.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram bot-token connect; relevance: the Telegram BotFather-token step.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram message dispatch; relevance: the pairing-code/troubleshooting flow.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker run-environment wiring; relevance: the Docker-on-VPS execution model.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime config reload/broadcast; relevance: applying the configured tokens/keys at deploy.


### note 2 — oc_install_installer (8t · 12s · 11d)

**Terms (8)**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway/agent product; relevance: what the three installer scripts install.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: installers ensure Node 24 by default (Node 22.19+ supported), via Homebrew/NodeSource/apk/winget/portable zip.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: the default `npm` global install method; EACCES-prefix handling.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: the "CI and automation" section's non-interactive flags/env vars.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-runnable without side effects; relevance: `--dry-run`/`OPENCLAW_DRY_RUN`, re-run-safe gateway `install --force` + restart.
- [AppConfig](../../term_dictionary/term_appconfig.md) — runtime configuration management; relevance: install method/version/prefix selected via `OPENCLAW_*` env vars (config-as-deployment analogy).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the agent runtime installed; relevance: the post-install `openclaw doctor`/gateway-service is the harness.
- [DevOps](../../term_dictionary/term_devops.md) — automation/operations practice; relevance: scripted/headless installs (no-prompt, JSON events) are a DevOps onboarding path.

**Docs (11; ≥5 existing)**
- [cc_install](../claude_code/cc_install.md) — Claude Code install; relevance: sibling-tool install-script precedent.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — advanced install + verify; relevance: parallel post-install verification (doctor analog).
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: parallels OpenClaw installer troubleshooting (PATH/spawn-git).
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — install failure reference; relevance: EACCES/ENOENT-style failure catalog parallel.
- [cc_github_actions](../claude_code/cc_github_actions.md) — running a coding agent in GitHub Actions; relevance: the CI install path.
- [cc_gitlab_ci_cd](../claude_code/cc_gitlab_ci_cd.md) — coding agent in GitLab CI; relevance: non-interactive install in CI.
- [hermes_install_windows_native](../hermes_agent/hermes_install_windows_native.md) — native Windows install; relevance: the `install.ps1` winget/Choco/Scoop/portable-node path.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Nix install quickstart; relevance: alternative reproducible install method.
- [oc_install_hostinger](oc_install_hostinger.md) — managed host (planned, this series); relevance: the no-script managed alternative.
- [oc_install_kubernetes](oc_install_kubernetes.md) — k8s deploy (planned, this series); relevance: install-into-cluster sibling.
- [oc_install_migrating_claude](oc_install_migrating_claude.md) — Claude import (planned, this series); relevance: installer can run onboarding/import after install.

**Repos (3)**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the package the installer fetches (npm or git checkout).
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — install/onboarding wizard; relevance: the installer invokes onboarding when a TTY is available.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway process; relevance: post-install `gateway install --force` + restart.

**Snippets (12)**
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: the entry the installer hands off to.
- [snippet_openclaw_cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — primary CLI run path; relevance: post-install `openclaw` invocation.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard setup imports; relevance: the onboarding the installer attempts.
- [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — `setup.sh`-style installer; relevance: direct shell-installer parallel to `install.sh`.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — CLI setup/installer; relevance: install-method/version selection parallel.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard; relevance: interactive vs `--no-onboard` flow.
- [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — POSIX bootstrap script; relevance: `install.sh`/`install-cli.sh` shell-bootstrap parallel.
- [snippet_hermes_agent_acp_bootstrap_ps1](../../code_snippets/snippet_hermes_agent_acp_bootstrap_ps1.md) — PowerShell bootstrap; relevance: `install.ps1` MinGit/portable-node bootstrap parallel.
- [snippet_hermes_agent_cli_gateway_windows](../../code_snippets/snippet_hermes_agent_cli_gateway_windows.md) — Windows gateway path handling; relevance: `install.ps1` PATH/`.cmd` wrapper specifics.
- [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — bootstrap encoding/PATH setup; relevance: cross-platform installer environment prep.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — config/env-var loading; relevance: how `OPENCLAW_*` env vars drive install behavior.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — service restart handoff; relevance: post-install gateway service refresh + restart.

**Entry points (inbound):** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (W1 hub, planned).

### note 3 — oc_install_kubernetes (9t · 11s · 11d)

**Terms (9)**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the single container deployed to the cluster.
- [Docker](../../term_dictionary/term_docker.md) — container image format; relevance: the single image `ghcr.io/openclaw/openclaw` Kustomize deploys.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage; relevance: the Kubernetes `Secret/openclaw-secrets` holds the gateway token + provider API keys.
- [AppConfig](../../term_dictionary/term_appconfig.md) — runtime configuration management; relevance: `openclaw.json` + AGENTS.md live in `ConfigMap/openclaw-config` (config-as-deployment).
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — the agent-instruction file; relevance: AGENTS.md is mounted from the ConfigMap.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-runnable deploy; relevance: `deploy.sh` preserves the existing token on re-run; re-deploy is an apply+rollout-restart.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the agent runtime; relevance: the gateway pod is the harness running in-cluster.
- [LLM](../../term_dictionary/term_llm.md) — model behind the agent; relevance: "an API key for at least one model provider" is required.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — token that makes a retried op a no-op; relevance: the preserved gateway token plays this role across re-deploys.

**Docs (11; ≥5 existing)**
- [pi_containerization](../pi/pi_containerization.md) — running a coding agent in a container; relevance: closest dev-tool precedent for container-deploying an agent.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox/container runtime; relevance: containerized coding-agent runtime model.
- [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — devcontainer setup; relevance: container config/mount parallel to ConfigMap/PVC.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — container hardening; relevance: maps to readOnlyRootFilesystem / drop-ALL-caps / non-root UID 1000.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — volumes + supervision; relevance: the 10Gi PVC for agent state + pod supervision.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: keeping secrets out of the repo checkout, temp-dir secret apply.
- [aws_ecr_docker_setup](../aws_ecr/aws_ecr_docker_setup.md) — container-image registry/deploy; relevance: the `ghcr.io` image + pin-by-version + custom-image swap parallel.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — coding-agent deployment patterns; relevance: cluster/managed deploy surface.
- [oc_install_hostinger](oc_install_hostinger.md) — managed host (planned, this series); relevance: simpler managed alternative to a cluster.
- [oc_install_installer](oc_install_installer.md) — installer scripts (planned, this series); relevance: the non-cluster install path.
- [oc_install_migrating](oc_install_migrating.md) — migration hub (planned, this series); relevance: PVC state is what you'd back up/move.

**Repos (3)**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the container image's source.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway process; relevance: the gateway bound to loopback inside the pod.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: the pod security hardening (caps/UID/read-only FS).

**Snippets (11)**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret/provider-key resolution; relevance: how the Secret's provider keys are consumed at runtime.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway auth startup; relevance: the gateway token from the Secret guards the Control UI.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers (token auth); relevance: deploy.sh creates token auth by default.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener bind; relevance: loopback bind in-pod vs non-loopback for Ingress.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime config reload; relevance: ConfigMap changes applied on rollout-restart.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker run environment; relevance: the container execution model.
- [snippet_hermes_agent_tools_environments_modal](../../code_snippets/snippet_hermes_agent_tools_environments_modal.md) — serverless/managed container env; relevance: a cloud cluster-runtime parallel.
- [snippet_hermes_agent_tools_environments_singularity](../../code_snippets/snippet_hermes_agent_tools_environments_singularity.md) — rootless container runtime; relevance: non-root/hardened pod parallel.
- [snippet_cdk_fargate_alb_basic](../../code_snippets/snippet_cdk_fargate_alb_basic.md) — Fargate service behind an ALB; relevance: the "expose beyond port-forward" Ingress/LB parallel.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload planning; relevance: applying ConfigMap edits without rebuilding.

**Entry points (inbound):** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (W1 hub, planned) · [entry_code_repos](../../../0_entry_points/entry_code_repos.md).

### note 4 — oc_install_macos_vm (10t · 11s · 11d)

**Terms (10)**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: what runs inside the macOS VM.
- [SSH](../../term_dictionary/term_ssh.md) — secure remote shell; relevance: enable Remote Login, SSH into the VM, run headless `openclaw status` over ssh.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: prerequisite for `npm install -g openclaw@latest` inside the VM.
- [npm](../../term_dictionary/term_npm.md) — package manager; relevance: the in-VM install command.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — chat-platform binding; relevance: configure WhatsApp/Telegram/iMessage channels in the VM.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable to the same state; relevance: golden-image clone → reset-to-clean (`lume clone`/`delete`/`clone`).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the agent runtime; relevance: OpenClaw's daemon keeps the gateway running headlessly.
- [LLM](../../term_dictionary/term_llm.md) — model behind the agent; relevance: onboarding sets the model provider (Anthropic/OpenAI).
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: the VM gives strict isolation from the host Mac.
- [Cron](../../term_dictionary/term_cron.md) — time-based scheduling; relevance: keeping the VM running 24/7 (sleep-disable, `caffeinate`, always-on daemon).

**Docs (11; ≥5 existing)**
- [cc_install](../claude_code/cc_install.md) — Claude Code install; relevance: the in-VM install-a-coding-agent step.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup for a coding agent; relevance: the configure-channels step in the VM.
- [hermes_messaging_bluebubbles_imessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — iMessage via BlueBubbles; relevance: the iMessage integration (alt path to `imsg`).
- [hermes_photon_imessage](../hermes_agent/hermes_photon_imessage.md) — iMessage bridge; relevance: the `imsg` Full-Disk-Access/Automation iMessage setup.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — isolated runtime; relevance: VM-as-sandbox isolation rationale.
- [hermes_install_termux_android](../hermes_agent/hermes_install_termux_android.md) — install on a constrained device; relevance: parallel "install the agent on a non-primary host" pattern.
- [pi_security_model](../pi/pi_security_model.md) — agent isolation/security model; relevance: why you sandbox the agent away from your daily Mac.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote backend over SSH; relevance: VM-as-node / Gateway-remote hybrid model.
- [oc_install_hostinger](oc_install_hostinger.md) — managed host (planned, this series); relevance: the recommended-default VPS alternative.
- [oc_install_installer](oc_install_installer.md) — installer scripts (planned, this series); relevance: the in-VM install mechanism.
- [oc_install_migrating](oc_install_migrating.md) — migration hub (planned, this series); relevance: golden image is a state-reset/restore form.

**Repos (3)**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product installed in the VM.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway process; relevance: the daemon/headless gateway kept running.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: iMessage/WhatsApp/Telegram adapters (iMessage is messaging, not voice).

**Snippets (11)**
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: the macOS daemon keeping the gateway alive headlessly.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist rendering; relevance: `openclaw onboard --install-daemon` on macOS.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard writes openclaw.json; relevance: the `~/.openclaw/openclaw.json` channel edits.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram dispatch; relevance: the Telegram channel config block.
- [snippet_hermes_agent_gw_platform_whatsapp_connect](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_connect.md) — WhatsApp QR connect; relevance: `openclaw channels login` WhatsApp QR scan.
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — iMessage/BlueBubbles adapter; relevance: the iMessage integration RPC path.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect; relevance: the Telegram bot-token channel.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway startup; relevance: the gateway the daemon keeps running.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health; relevance: `openclaw status` over SSH.


### note 5 — oc_install_migrating (11t · 12s · 11d)

**Terms (11)**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the install being migrated/moved.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage; relevance: the state dir holds auth-profiles.json keys + `credentials/`; encrypt backups, rotate on exposure.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer/refresh credential; relevance: `auth-profiles.json` stores OAuth tokens migrated with state.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — multi-provider credential store; relevance: per-agent provider/channel state under `credentials/`.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — per-agent auth config; relevance: `agents/<agentId>/agent/auth-profiles.json` is the file you must carry.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable repair; relevance: `openclaw doctor` applies config migrations / repairs services re-runnably.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — chat-platform binding; relevance: channel state (WhatsApp login, Telegram session) is migrated to avoid re-pairing.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — workspace instruction file; relevance: `MEMORY.md`/`USER.md`/`AGENTS.md` workspace files move with the install.
- [Skills](../../term_dictionary/term_skills.md) — agent skill modules; relevance: skills + prompts in the workspace are migrated.
- [Compaction](../../term_dictionary/term_compaction.md) — session-history management; relevance: sessions/conversation history in the state dir are preserved across the move.
- [AppConfig](../../term_dictionary/term_appconfig.md) — runtime configuration management; relevance: `openclaw.json` + gateway settings copied (not just the config file alone).

**Docs (11; ≥5 existing)**
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — migrate an OpenClaw install to Hermes; relevance: the inverse cross-system move; same state-dir/auth/skills surface.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — per-agent credential pools; relevance: explains the `credentials/` multi-provider state you migrate.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation/handling; relevance: encrypt backups, secure transfer, rotate on exposure.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — config-file precedence/state layout; relevance: what "the entire state directory" actually contains.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-profile/agent state; relevance: the `--profile` / `OPENCLAW_STATE_DIR` mismatch pitfall.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — the `.claude` state directory; relevance: parallel "where the coding agent keeps state on disk".
- [cc_install](../claude_code/cc_install.md) — install on the new machine; relevance: step 2 (install OpenClaw + Node on the target).
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth over SSH/remote; relevance: the remote-mode pitfall (migrate the gateway host, not the laptop).
- [oc_install_migrating_claude](oc_install_migrating_claude.md) — Claude import (planned, this series); relevance: the cross-system-import migration path.
- [oc_install_installer](oc_install_installer.md) — installer scripts (planned, this series); relevance: install on the new machine (step 2).
- [oc_install_kubernetes](oc_install_kubernetes.md) — k8s deploy (planned, this series); relevance: PVC is the cluster analog of the state dir to migrate.

**Repos (5)**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product being moved.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions subsystem; relevance: conversation history/agent state in the state dir.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway process; relevance: `gateway stop`/`restart`, doctor.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: MEMORY.md / workspace memory migrated.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions/providers; relevance: migration providers are bundled extensions.

**Snippets (12)**
- [snippet_hermes_agent_cli_claw_migrate](../../code_snippets/snippet_hermes_agent_cli_claw_migrate.md) — `migrate` CLI from OpenClaw; relevance: the cross-system import command surface.
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — backup/archive state; relevance: stop+`tar -czf openclaw-state.tgz .openclaw`.
- [snippet_hermes_agent_cli_backup_restore](../../code_snippets/snippet_hermes_agent_cli_backup_restore.md) — restore from backup; relevance: `tar -xzf` extract on the new machine.
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — doctor checks auth dirs; relevance: `openclaw doctor` repairs/verifies migrated auth state.
- [snippet_hermes_agent_cli_profiles_switch](../../code_snippets/snippet_hermes_agent_cli_profiles_switch.md) — profile/state-dir switch; relevance: the `--profile`/`OPENCLAW_STATE_DIR` mismatch pitfall.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: auth-profiles + credentials/ consumed after migration.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — status/health; relevance: the verification checklist (`openclaw status`).
- [snippet_hermes_agent_optional_skills_migration_openclaw](../../code_snippets/snippet_hermes_agent_optional_skills_migration_openclaw.md) — skills migration from OpenClaw; relevance: migrating workspace skills.


### note 6 — oc_install_migrating_claude (10t · 12s · 11d)

**Terms (10)**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the import target; relevance: the gateway receiving the imported Claude state.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's CLI coding agent; relevance: the import source (CLAUDE.md, `.claude/`, `.mcp.json`).
- [Claude](../../term_dictionary/term_claude.md) — the model/product family; relevance: Claude Code / Claude Desktop are the two import sources.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP server definitions imported from `.mcp.json` / `~/.claude.json` / `claude_desktop_config.json`.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — workspace instruction file; relevance: project/user CLAUDE.md is appended into AGENTS.md / USER.md.
- [Skills](../../term_dictionary/term_skills.md) — agent skill modules; relevance: Claude skills with SKILL.md are copied; commands → skills with `disable-model-invocation: true`.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — the SKILL.md frontmatter contract; relevance: SKILL.md is the imported skill's manifest that drives the conversion.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe re-runs; relevance: dry-run preview → apply-with-verified-backup → conflict refusal unless `--overwrite`.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — automation pipelines; relevance: `--json` with no `--yes` is the safe no-mutate mode for CI / shared scripts.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret handling; relevance: secrets are redacted in plans/reports; OAuth/Desktop credential state stays archive-only (not auto-decoded).

**Docs (11; ≥5 existing)**
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — cross-system import (OpenClaw→Hermes); relevance: same migration-provider preview→apply→backup contract.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — authoring a Claude skill (SKILL.md); relevance: the skill format that gets copied into OpenClaw's skills dir.
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — CLAUDE.md memory model; relevance: what's appended into AGENTS.md / USER.md.
- [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — CLAUDE.md file structure; relevance: project vs user CLAUDE.md source mapping.
- [cc_mcp_installation_scopes](../claude_code/cc_mcp_installation_scopes.md) — MCP server config scopes; relevance: where `.mcp.json` / `~/.claude.json` MCP servers come from.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — the `.claude` directory; relevance: `--from` project-root import reads `.claude/commands/`, `.claude/skills/`, `settings.json`.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — Claude subagents under `.claude/agents/`; relevance: subagents are explicitly archive-only on import.
- [cc_settings_scopes_and_precedence](../claude_code/cc_settings_scopes_and_precedence.md) — Claude settings/permissions; relevance: permissions/allowlists/hooks stay archive-only (OpenClaw refuses to trust them).
- [oc_install_migrating](oc_install_migrating.md) — migration hub (planned, this series); relevance: the parent page listing all migration paths.
- [oc_install_installer](oc_install_installer.md) — installer scripts (planned, this series); relevance: a fresh OpenClaw install is the precondition for onboarding import.
- [oc_install_macos_vm](oc_install_macos_vm.md) — macOS VM deploy (planned, this series); relevance: a common target environment to import Claude state into.

**Repos (4)**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the import target product.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions/providers; relevance: the bundled Claude migration provider lives here.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: imported skills land in the workspace skills dir.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway process; relevance: post-import `openclaw doctor` + gateway restart.

**Snippets (12)**
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — wizard migration import; relevance: `openclaw onboard --flow import` / `--import-from claude`.
- [snippet_hermes_agent_cli_claw_migrate](../../code_snippets/snippet_hermes_agent_cli_claw_migrate.md) — `migrate` CLI; relevance: `openclaw migrate claude --dry-run` / `apply claude --yes`.
- [snippet_hermes_agent_skills_claude_code](../../code_snippets/snippet_hermes_agent_skills_claude_code.md) — importing Claude Code skills; relevance: copying SKILL.md skills + converting commands.
- [snippet_hermes_agent_core_skill_commands_discovery](../../code_snippets/snippet_hermes_agent_core_skill_commands_discovery.md) — command/skill discovery; relevance: `.claude/commands/` → skills with `disable-model-invocation`.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — skill frontmatter parsing; relevance: editing imported-skill frontmatter to re-enable model invocation.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — OpenClaw skill manifest format; relevance: the target SKILL.md shape imported skills land in.
- [snippet_hermes_agent_skills_mcp_native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md) — native MCP server wiring; relevance: imported MCP server definitions.
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — backup before mutate; relevance: apply creates and verifies a backup first.
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — doctor checks auth dirs; relevance: `openclaw doctor` after import.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — status/health; relevance: restart + `openclaw status` verification step.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validation; relevance: conflict detection in the dry-run plan.

**Entry points (inbound):** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (W1 hub, planned) · [entry_claude_code_docs](../../../0_entry_points/entry_claude_code_docs.md).

## Undigested Terms Plan

| Term (as it appears in source) | Disposition |
|---|---|
| OpenClaw, OpenClaw Gateway | Link existing `term_openclaw`; documented operationally in these `oc_install_*` notes. No new term. |
| state directory (`~/.openclaw/`), profile, `OPENCLAW_STATE_DIR` | OpenClaw operational vocab → described in `oc_install_migrating`; not a reusable cross-cutting term. Link `term_configuration_model`. No new term. |
| auth-profiles.json, credentials/, gateway token | Link existing `term_secrets_manager` / `term_credential_pool` / `term_oauth_token`. No new term. |
| install.sh / install-cli.sh / install.ps1, `--install-method`, dist-tag, `OPENCLAW_*` env vars | Installer-script operational detail → documented in `oc_install_installer`; link `term_npm` / `term_node_js` / `term_appconfig`. No new term. |
| Kustomize, ConfigMap, Secret, PVC, Deployment, Service, namespace, Kind | Kubernetes platform vocab. `term_kubernetes` / `term_kustomize` / `term_persistent_volume` do NOT exist in the vault. Per master design (OpenClaw vocab → oc_ notes; generic infra terms not promoted from a single doc page), describe inline in `oc_install_kubernetes`; link existing `term_docker`. NOT promoted (single-page, generic-infra, not OpenClaw-specific cross-cutting). No new term. |
| Lume, hosted Mac providers, golden image, headless VM | macOS-VM operational detail → documented in `oc_install_macos_vm`; `term_virtual_machine` / `term_apple_silicon` do NOT exist but are generic single-page infra terms, not promoted. Link `term_ssh`. No new term. |
| iMessage / `imsg`, WhatsApp, Telegram, BotFather | Channel platform names → documented as config; link `term_channel_adapter`. Channel-specific deep dives are owned by the Channels sub-plans (ch01–ch06). `term_imessage` / `term_whatsapp` / `term_telegram` do NOT exist; not promoted here (Channels section owns them). No new term. |
| Claude migration provider, CLAUDE.md, AGENTS.md, USER.md, SKILL.md, .mcp.json, claude_desktop_config.json | Link existing `term_claude_code` / `term_agents_md` / `term_skills` / `term_skill_manifest` / `term_mcp`. No new term. |
| `openclaw migrate` / `onboard` / `doctor` / `status` / `channels` (CLI) | CLI commands → owned by CLI sub-plans (cl01–cl09); referenced by link from these notes. No new term. |

**Expected new `term_dictionary` captures: 0.** No genuinely cross-cutting, vault-reusable term lacking an
existing home appears in this set. (If augment's Step 2d re-scan surfaces one, capture via
`/tessellum-capture-term-note` + add to the best-fit glossary — most likely `acronym_glossary_agentic_ai.md`
or `acronym_glossary_dev_tools.md` — and record it here as a new-term candidate.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. Requirement inherited from master:
should augment surface a genuinely reusable term with no existing note and no doc-page home, capture it via
definition in an `oc_*` note), add the acronym-glossary entry (W5), and DB-verify before linking.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P1). Gate table inherited verbatim from the master 9-GATE.

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean; required `## Overview` + `## Related Notes` present; `source_url: https://docs.openclaw.ai/<slug>` present; forbidden YAML fields absent. |
| G2 | Grounding | Each note diffs faithfully against `inbox/openclaw_docs/install/<page>` (no invented flags/commands/resources; flags, env vars, resource names, file paths reproduced verbatim). |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks per note; one `building_block`; every mapped section present. |
| G4 | Cross-Reference | ≥8 relevance-selected term links + ≥10 code_snippets + ≥10 docs (≥5 EXISTING) + relevant `repo_openclaw*` + ≥1 sibling `oc_*`, each with a relevance statement (per `## Per-Note Related Notes Mapping (LOCKED)`). |
| G5 | Ghost-reference | Every cited EXISTING note_id resolves in the DB (sibling `oc_*` planned-OK pre-reindex); detect + redirect. |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after reindex. |
| G7 | Discoverability | Every new note carries ≥1 sibling/inbound cross-link; anti-island. |
| G8 | In-degree ≥1 | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (satisfied via `entry_openclaw_docs.md` + repo/term inlinks). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

All gates must PASS before commit.

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_install_hostinger oc_install_installer oc_install_kubernetes oc_install_macos_vm oc_install_migrating oc_install_migrating_claude"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "G1 MISSING SECTION '$sec': $n"; done
  # G1: source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "G1 MISSING source_url: $n"; }
  # G1: format check
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G3: density (exclude frontmatter from word count)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4: at least one sibling oc_ cross-link
  grep -q "($SIBLING_PREFIX" "$f" || echo "G4 no sibling $SIBLING_PREFIX link: $n"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference: verify every cited note stem resolves in the DB
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
grep -rhoE '\]\(([.][.]/)+[^)]+\.md\)' "$GATE_DIR"/oc_install_*.md | sed -E 's#.*/([^/)]+)\.md\)#\1#' | sort -u | \
while read -r stem; do
  [ -z "$stem" ] && continue
  [ "$r" = "1" ] || echo "G5 GHOST (pre-reindex; OK if sibling oc_ planned): $stem"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Src code fences | Planned fences | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_install_hostinger | procedure | 480 | 0 | 0 | ✅ |
| 2 | oc_install_installer | procedure | 640 | 27 | ≤6 (1 repr. invocation/script + flag/env tables) | ✅ |
| 3 | oc_install_kubernetes | procedure | 600 | 15 | ≤6 (deploy/port-forward/secret/resource-tree) | ✅ |
| 4 | oc_install_macos_vm | procedure | 600 | 15 | ≤6 (create/ssh/install/channels+iMessage config) | ✅ |
| 5 | oc_install_migrating | procedure | 560 | 4 | ≤6 (tar/extract/doctor/env-check) | ✅ |
| 6 | oc_install_migrating_claude | procedure | 580 | 8 | ≤6 (dry-run/apply/doctor/json) | ✅ |

No note approaches the 2,500w / 400-line caps. The two fence-heavy source pages (`installer.md` 27 fences,
`kubernetes.md`/`macos-vm.md` 15 each) are reduced to ≤6 representative fences per note by reproducing one
canonical invocation per script/step plus the verbatim flags / env-vars / resource-tree tables (which are
markdown tables, not code fences), and pointing readers at the source for the full example-tab matrix.

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (the W1 hub, CREATED as a master pre-step before the first
cluster. Each of the 6 new notes receives its `entry_openclaw_docs.md` back-link at finalization (this is the
primary G8 inbound-link source). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify + add at execution; primary source for
G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` → all 6 notes (Install cluster rows; primary inbound).
- `repo_openclaw.md` → notes 1, 2, 3, 4, 5, 6 (the deployed/installed/migrated product; code↔docs link).
- `repo_openclaw_cli_wizard.md` → note 2 (installer ↔ install/onboarding wizard).
- `repo_openclaw_gateway.md` → notes 3, 4, 5 (gateway deploy / headless / restart).
- `repo_openclaw_security.md` → note 3 (k8s security hardening).
- `repo_openclaw_sessions.md` + `repo_openclaw_memory.md` → note 5 (sessions / workspace memory migration).
- `repo_openclaw_extensions.md` + `repo_openclaw_skills.md` → note 6 (Claude migration provider / imported skills).
- `term_openclaw.md` → notes 1–6 (W3 code↔docs cross-link); `term_claude_code.md` → note 6;
  `term_docker.md` → notes 1, 3; `term_node_js.md` / `term_npm.md` → note 2.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates PASS before commit. Re-read each source page during execution; reproduce
flags / env vars / commands / config / resource names verbatim (G2). One `building_block` per note. Reindex
incrementally; verify `note_links` populated + 0 broken links + in-degree ≥1 before commit.
`git pull --rebase --autostash origin main` first; commit + push the wave (no Claude co-author trailer).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** (9/9 PASS → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of sub-plan in03 (Install). Re-read all 6 source pages under
`inbox/openclaw_docs/install/` (hostinger, installer, kubernetes, macos-vm, migrating, migrating-claude) and
LOCKED the per-note Related Notes mapping at the raised floors **≥8 terms · ≥10 code_snippets · ≥10 docs**
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`; updated the Summary-Statistics cross-ref
line and the G4 gate criterion to the raised floors.

**What was locked (achieved counts; floors met for all 6):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_install_hostinger | 9 | 11 | 11 (7 existing / 4 planned oc_) | 4 | ✅ |
| oc_install_installer | 8 | 12 | 11 (8 existing / 3 planned oc_) | 3 | ✅ |
| oc_install_kubernetes | 9 | 11 | 11 (8 existing / 3 planned oc_) | 3 | ✅ |
| oc_install_macos_vm | 10 | 11 | 11 (8 existing / 3 planned oc_) | 3 | ✅ |
| oc_install_migrating | 11 | 12 | 11 (8 existing / 3 planned oc_) | 5 | ✅ |
| oc_install_migrating_claude | 10 | 12 | 11 (8 existing / 3 planned oc_) | 4 | ✅ |

**DB-verification (2026-06-21):** every cited EXISTING note_id was confirmed present via
non-sibling docs exist; ALL 14 cited repos exist. Sibling `oc_install_*` docs (this series) and the W1 hub
`entry_openclaw_docs.md` are correctly NOT in the DB (planned, created on execution). Ghost sweep of the
LOCKED section: **0 real ghosts** (only the literal `relpath.md` placeholder in the section's render-format
instruction matched, which is not a citation). Relative-path spot-check from
`resources/documentation/openclaw/` confirmed all path forms resolve (term/snippet/repo/doc/entry/sibling).

- **`term_configuration_model` REMOVED everywhere** — DB read shows it is a *random-graph model* (prescribed
  degree sequence / stub-matching), NOT a config-file concept. The prior candidate list cited it for
  "openclaw.json config" in notes 2/3/4/5; replaced with **`term_appconfig`** (AWS dynamic-configuration-
  management — genuine config-as-deployment analogy) where the config-deployment sense applies.
  are data-pipeline / generic-architecture / Brazil-CDK-specific → discarded as off-sense.
- Added genuinely-relevant terms surfaced by re-read + search that the prior pool missed: `term_dm_pairing`
  (Telegram pairing-code troubleshooting), `term_idempotency_key` (preserved gateway token across re-deploys),
  `term_devops` (scripted installs), `term_sandbox` + `term_cron` (macOS-VM isolation + 24/7), `term_auth_profile`
  + `term_compaction` (migration state contents), `term_credential_pool` (credentials/).

**New-term candidates (Step 2d re-scan):** **0.** The re-read surfaced no genuinely cross-cutting,
vault-reusable term lacking an existing home. Confirmed MISSING-and-correctly-not-promoted (generic single-page
infra / channel-platform vocab owned elsewhere): `term_kubernetes`, `term_kustomize`, `term_persistent_volume`,
`term_virtual_machine`, `term_apple_silicon`, `term_powershell`, `term_imessage`, `term_whatsapp`,
`term_telegram`, `term_agent_workspace`, `term_devcontainer`. This matches the plan's Undigested Terms Plan
(**expected new term captures: 0**) — no change required. Best-fit glossary IF one ever surfaces:
`acronym_glossary_agentic_ai.md` or `acronym_glossary_dev_tools.md` (per the plan's Step 2d note).

**Step 2 density re-confirmation:** raw `wc -w` on the 6 mirror pages = 507 / 2052 / 842 / 958 / 789 / 843,
matching the plan's Source table exactly (CP7 measured, not guessed). Body-only word counts (frontmatter +
MDX tags stripped) are 478 / 798 / 807 / 490 / 742 / 789 — every planned note lands ≪ 2,500w. No new splits
needed; the installer page's 2,052 raw words are inflated by the verbatim flags/env-var markdown tables (not
prose), and the plan already caps each note at ≤6 representative fences. Density Re-Assessment unchanged.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_in03.md` · Reviewed: 2026-06-21 · READ-ONLY review of the augmented plan.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 6 notes meet ≥8 terms / ≥10 snippets / ≥10 docs; every link carries a `relevance:` statement; ≥1 entry-point inbound each (`entry_openclaw_docs` W1 hub + a second hub). Counts: 9·11·11 / 8·12·11 / 9·11·11 / 10·11·11 / 11·12·11 / 10·12·11. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | Single execution phase; gate table lists G1–G8 incl. G5-Ghost (detect+redirect) + G6-Broken (`/tessellum-fix-broken-links`) + G7/G8-Discoverability (in-degree ≥1). Validation Scripts implement G1/G3/G5. |
| CP4 | Plan size | **PASS** | 6 planned notes (≤30); single phase. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/`+`pi/` doc corpora (`## Overview` + source-mirrored body + `## Related Notes` + `## References` + bold footer; fixed YAML field order; forbidden fields enumerated). Matches existing `cc_*`/`pi_*` notes. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: all 6 notes ≤640 est. words (≪2,500w cap), ≤6 fences, ≤400 lines; installer (2,052 raw w) stays one note (table-inflated, single coherent procedure). No borderline note left unaddressed. |
| CP7 | Source word counts measured | **PASS** | Re-measured raw `wc -w` 2026-06-21 = 507/2052/842/958/789/843 — exact match to the plan's Source table (ratio 1.00, well within 0.7–1.3). No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present, all rows dispositioned (link-existing / not-promoted), 0 new captures; `## Term-Note Authoring Requirements` present as N/A (0 new terms) with the inherited multi-source mandate should one surface. Augment Step 2d re-scan: 0 new terms. |
| CP8f | Slug specificity / collision (all-notes dedup) | **PASS** | Collision audit run across `term_dictionary/` AND `resources/documentation/`: no `oc_install_*` note duplicates an existing term/doc (they document operations, terms are linked). Specificity fix applied: `term_configuration_model` (random-graph model) removed as an off-sense collision; replaced with `term_appconfig`. MISSING generic-infra slugs correctly not promoted. |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | `## Inlinks (existing → new)` maps outside-folder inbound links for all 6 notes (`entry_openclaw_docs`, `repo_openclaw*`, term/`cc_*` inlinks); G8-Discoverability (in-degree ≥1 from outside the folder) is in the gate table as a gated execution step, not a recommendation. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
