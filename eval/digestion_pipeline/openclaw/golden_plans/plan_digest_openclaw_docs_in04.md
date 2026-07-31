---
title: Sub-Plan in04 — OpenClaw Docs: Install (Migrating from Hermes, Nix, Node.js, Northflank, Oracle Cloud, Podman)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - install/migrating-hermes
  - install/nix
  - install/node
  - install/northflank
  - install/oracle
  - install/podman
---

# Sub-Plan in04: Install

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview`/`## Related Notes`/`## References`, density caps ≤400L/≤2500w/≤6 code), dedup (term + doc + `repo_openclaw*`), 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master and applied here.
> This file holds the measured source table, planned-notes table, section coverage map, candidate cross-references, and the single-phase gate — locked to a fresh re-read of the 6 assigned `install/` pages on 2026-06-20.

## Scope

The 6 install pages this sub-plan covers are the **alternative install / migration / self-host deployment paths** that the Install Overview links out to:

- **migrating-hermes** — importing existing Hermes state (model config, prompts, memory, skills, MCP, credentials) into a fresh OpenClaw via the bundled migration provider (`openclaw onboard --flow import` / `openclaw migrate`), with preview/backup/conflict handling.
- **nix** — declarative, reproducible, rollback-able install via the first-party `nix-openclaw` Home Manager module, plus Nix-mode runtime behavior (immutable config, state/config paths, service PATH discovery).
- **node** — the Node.js prerequisite (Node 22.19+ / Node 24 recommended): version check, per-OS install, version managers, and `openclaw: command not found` / `EACCES` PATH troubleshooting.
- **northflank** — one-click PaaS cloud deploy with the browser Control UI (the "no terminal on the server" path).
- **oracle** — full self-host runbook on Oracle Cloud's Always Free ARM tier: OCI instance, Tailscale SSH, gateway token-auth + Tailscale Serve, VCN lockdown, security posture, ARM notes, persistence/backups.
- **podman** — running the Gateway in a rootless Podman container managed from the host `openclaw` CLI: setup script, Quadlet/systemd auto-start, Tailscale, config/env/storage, useful commands, troubleshooting.

**Priority: P1 (Phase A)** per the master — install/deploy paths are operational-core (they gate every downstream channel/provider/CLI doc). Content type is overwhelmingly **procedure** (step-by-step install/deploy/migrate); `oracle` and `podman` carry a secondary security/hardening flavor but remain single-BB procedure (the hardening is steps + a "needed?" rationale table, not a standalone argument note).

**Source**: OpenClaw docs, 6 pages, **4,601 measured words**. **Planned: 6 notes** (one per page; no splits — all pages ≤ ~1,200w and single-BB).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Migrating from Hermes | install/migrating-hermes | 1,050 | 8 | 9 | 0 | procedure |
| Nix | install/nix | 545 | 4 | 4 | 3 | procedure |
| Node.js | install/node | 531 | 11 | 4 | 2 | procedure |
| Northflank | install/northflank | 248 | 0 | 4 | 0 | procedure |
| Oracle Cloud | install/oracle | 1,056 | 10 | 9 | 0 | procedure |
| Podman | install/podman | 1,171 | 8 | 8 | 0 | procedure |

Totals: **4,601 words**, **41 code fences**, **38 H2 / 5 H3**. Code-fence count = raw ```` ``` ```` count ÷ 2 (migrating-hermes 16/2=8, nix 8/2=4, node 22/2=11, northflank 0, oracle 20/2=10, podman 16/2=8).

## Content Strategy

- **Prioritize** the two most operationally load-bearing pages: **oracle** (the canonical free 24/7 self-host runbook combining VPS + Tailscale + gateway token-auth + VCN lockdown — the security posture other install pages defer to) and **migrating-hermes** (the upstream-migration path directly relevant to the FZ 15 OpenClaw↔Hermes ecosystem the vault already tracks). These get the richest cross-reference mapping into `repo_openclaw*`, `repo_hermes_agent*`, and the security/auth term cluster.
- **Split**: NONE. Every page is ≤ ~1,200 words and single-BB (procedure). `node.md` has the most fences (11) but is well under the 2,500-word and procedure-cohesion thresholds; its fences are tiny one-liners (`node -v`, `brew install node`, …) so the ≤6-code-block digest cap is met by reproducing only the load-bearing commands per OS (one tab each) rather than all 11 verbatim. `oracle.md` (10 fences) and `migrating-hermes.md`/`podman.md` (8 each) likewise stay ≤6 by reproducing representative commands and prosing the rest.
- **Link-out (do NOT re-digest here):** generic install overview/installer → `in01`/master Install Overview; Docker → `in02` (`oc_install_docker`); macOS-VM → `in03`; updating/uninstall/railway/render/raspberry-pi/upstash → `in05`; the `openclaw migrate` CLI reference → `cl05` (`oc_cli_migrate`); `openclaw onboard` → `cl05` (`oc_cli_onboard`); `openclaw doctor` → `gw02` (`oc_gateway_doctor`); Tailscale gateway config → `gw06` (`oc_gateway_tailscale`); gateway configuration → `gw02`; channels (Telegram/Discord/WhatsApp) → `ch0x`; agent-workspace (SOUL.md/AGENTS.md/memory) → `co01`; secrets/SecretRef → `gw05`/`rf02`. These are cross-linked as siblings/pointers, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_install_migrating_hermes.md` | procedure | install/migrating-hermes.md (all 9 H2: Two ways to import, What gets imported, What stays archive-only, Recommended flow, Conflict handling, Secrets, JSON output for automation, Troubleshooting, Related) | 650 | Migrating an existing Hermes setup into a fresh OpenClaw via the bundled migration provider: wizard vs `openclaw migrate` CLI, what imports (model config, MCP, workspace files, memory, skills, auth) vs archive-only, the preview→apply-with-backup→doctor→restart flow, conflict handling, secret-import flags, JSON/CI mode, and troubleshooting. |
| 2 | `oc_install_nix.md` | procedure | install/nix.md (What you get, Quick start, Nix-mode runtime behavior + 3 H3: What changes in Nix mode, Config and state paths, Service PATH discovery, Related) | 550 | Declarative, rollback-able OpenClaw install via the first-party `nix-openclaw` Home Manager module: what you get, the flake quick-start, and Nix-mode runtime behavior (`OPENCLAW_NIX_MODE=1`, immutable `openclaw.json`, `OPENCLAW_STATE_DIR`/`OPENCLAW_CONFIG_PATH`, launchd/systemd Nix-profile PATH discovery). |
| 3 | `oc_install_node.md` | procedure | install/node.md (Check your version, Install Node, Troubleshooting + 2 H3: `openclaw: command not found`, Permission errors on `npm install -g`, Related) | 500 | Installing the Node.js prerequisite for OpenClaw (Node 22.19+ required, Node 24 recommended): version check, per-OS install (Homebrew / nodesource / winget / version managers), and the two classic failures — `openclaw: command not found` (npm global bin not on PATH) and Linux `EACCES` (user-writable npm prefix). |
| 4 | `oc_install_northflank.md` | procedure | install/northflank.md (How to get started, What you get, Connect a channel, Next steps) | 350 | One-click cloud deploy of OpenClaw on Northflank with the browser Control UI (the "no terminal on the server" path): deploy-template steps, the required `OPENCLAW_GATEWAY_TOKEN`, persistent `/data` volume, connecting a channel via the Control UI or SSH `openclaw onboard`. |
| 5 | `oc_install_oracle.md` | procedure | install/oracle.md (Prerequisites, Setup 8 steps, Verify the security posture, ARM notes, Persistence and backups, Fallback: SSH tunnel, Troubleshooting, Next steps, Related) | 750 | Hosting a persistent OpenClaw Gateway free on Oracle Cloud's Always Free ARM tier: create the OCI ARM instance, install Tailscale SSH + OpenClaw, configure gateway loopback bind + token auth + Tailscale Serve, lock down the VCN to UDP 41641, verify the security posture (which traditional VPS hardening steps the lockdown removes), ARM/aarch64 notes, persistence/backups, and SSH-tunnel fallback. |
| 6 | `oc_install_podman.md` | procedure | install/podman.md (Prerequisites, Quick start, Podman and Tailscale, Systemd Quadlet optional, Config env and storage, Useful commands, Troubleshooting, Related) | 700 | Running the OpenClaw Gateway in a rootless Podman container managed from the host `openclaw` CLI: setup/run helper scripts, image build env vars, model auth in-container, host-CLI default (`OPENCLAW_CONTAINER`), Tailscale notes, Quadlet/systemd-user auto-start, config/env/storage bind-mounts + Podman env vars, and troubleshooting (EACCES, `gateway.mode=local`, SELinux). |

Filenames follow master convention `oc_ + full slug, "/" and "-" → "_"`: `install/migrating-hermes` → `oc_install_migrating_hermes.md`; `install/nix` → `oc_install_nix.md`; `install/node` → `oc_install_node.md`; `install/northflank` → `oc_install_northflank.md`; `install/oracle` → `oc_install_oracle.md`; `install/podman` → `oc_install_podman.md`. One BB (procedure) per note.

## Section Coverage Map

```
install/migrating-hermes.md
├── (intro: bundled migration provider, preview/redact/backup) ─ → note 1 (oc_install_migrating_hermes) Overview
├── Two ways to import (Onboarding wizard | CLI) ──────────────── → note 1
├── What gets imported (model config, MCP, workspace, memory,
│   skills, auth credentials) ───────────────────────────────── → note 1
├── What stays archive-only (plugins/sessions/logs/cron/...) ─── → note 1
├── Recommended flow (preview → apply+backup → doctor → restart) → note 1
├── Conflict handling ────────────────────────────────────────── → note 1
├── Secrets (interactive/--include-secrets/--no-auth-credentials) → note 1
├── JSON output for automation ───────────────────────────────── → note 1
├── Troubleshooting ──────────────────────────────────────────── → note 1
└── Related (→ cli/migrate, cli/onboard, install/migrating,
    gateway/doctor, concepts/agent-workspace) ─────────────────── → note 1 References (link-out, not re-digested)
install/nix.md
├── (intro: nix-openclaw Home Manager module) ────────────────── → note 2 (oc_install_nix) Overview
├── What you get ─────────────────────────────────────────────── → note 2
├── Quick start (5 steps) ────────────────────────────────────── → note 2
├── Nix-mode runtime behavior ────────────────────────────────── → note 2
│   ├── What changes in Nix mode ──────────────────────────────── → note 2
│   ├── Config and state paths (OPENCLAW_HOME/STATE_DIR/CONFIG) ── → note 2
│   └── Service PATH discovery (NIX_PROFILES) ─────────────────── → note 2
└── Related (nix-openclaw, setup wizard, docker, updating) ────── → note 2 References (link-out)
install/node.md
├── (intro: Node 22.19+ required, 24 recommended) ────────────── → note 3 (oc_install_node) Overview
├── Check your version ───────────────────────────────────────── → note 3
├── Install Node (macOS | Linux | Windows tabs + version mgrs) ── → note 3
├── Troubleshooting ──────────────────────────────────────────── → note 3
│   ├── `openclaw: command not found` (npm global bin / PATH) ──── → note 3
│   └── Permission errors on `npm install -g` (EACCES) ────────── → note 3
└── Related (install overview, updating, getting started) ─────── → note 3 References (link-out)
install/northflank.md
├── (intro: one-click template + Control UI) ─────────────────── → note 4 (oc_install_northflank) Overview
├── How to get started (8 deploy steps) ──────────────────────── → note 4
├── What you get (hosted gateway + Control UI, /data volume) ──── → note 4
├── Connect a channel ────────────────────────────────────────── → note 4
└── Next steps (channels, gateway config, updating) ──────────── → note 4 References (link-out)
install/oracle.md
├── (intro: Always Free ARM tier) ────────────────────────────── → note 5 (oc_install_oracle) Overview
├── Prerequisites (Oracle/Tailscale acct, SSH key) ───────────── → note 5
├── Setup (8 Steps: OCI instance, update, user/hostname,
│   Tailscale, install OpenClaw, gateway config, VCN lockdown,
│   verify) ──────────────────────────────────────────────────── → note 5
├── Verify the security posture (hardening "needed?" table) ───── → note 5
├── ARM notes (aarch64) ──────────────────────────────────────── → note 5
├── Persistence and backups (openclaw backup create) ─────────── → note 5
├── Fallback: SSH tunnel ─────────────────────────────────────── → note 5
├── Troubleshooting ──────────────────────────────────────────── → note 5
├── Next steps ───────────────────────────────────────────────── → note 5 References (link-out)
└── Related (install overview, gcp, vps) ─────────────────────── → note 5 References (link-out)
install/podman.md
├── (intro: rootless container, host CLI control plane) ──────── → note 6 (oc_install_podman) Overview
├── Prerequisites (Podman rootless, OpenClaw CLI, systemd) ────── → note 6
├── Quick start (4 Steps + setup/build env vars + auth) ──────── → note 6
├── Podman and Tailscale ─────────────────────────────────────── → note 6
├── Systemd (Quadlet, optional) ──────────────────────────────── → note 6
├── Config, env, and storage (bind-mounts, env vars) ─────────── → note 6
├── Useful commands ──────────────────────────────────────────── → note 6
├── Troubleshooting (EACCES, gateway.mode, SELinux) ──────────── → note 6
└── Related (docker, gateway/background-process, troubleshooting) → note 6 References (link-out)
```
No orphaned sections. Every page maps 1:1 to exactly one planned note; each page's "Related" / "Next steps" section becomes that note's `## References` link-out (to sibling `oc_*` planned notes and external URLs), never re-digested content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 6 pages are ≤ ~1,200 words (max = podman 1,171w, well under the 2,500w cap) and single-BB (procedure). No page is mixed-BB and none approaches the word/code caps after selective command reproduction. 1 page → 1 note. |

## Summary Statistics & Building Block Distribution

- **Source pages:** 6 (4,601 words, 41 code fences, 38 H2 / 5 H3).
- **New `oc_` notes:** **6** (one per page; no splits).
- **New `term_dictionary` notes:** **0** (see Undigested Terms Plan — OpenClaw install/deploy vocabulary is documented in these `oc_*` notes; existing terms are linked).
- **BB distribution:** procedure ×6 (all notes). No concept/model/argument notes.
- **Est. digest words:** ~3,500 (avg ~580/note; range 350–750). Source code fences (41) distribute across the 6 notes; each note keeps ≤6 by reproducing only load-bearing commands and prosing the rest (per Content Strategy).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### note 1 — oc_install_migrating_hermes (10t · 12s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: the migration target the page imports Hermes state into.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime that drives a coding-agent loop; relevance: both Hermes and OpenClaw are harnesses; the import moves harness config (model, MCP, skills).
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol for tool/server definitions; relevance: `mcp_servers`/`mcp.servers` definitions are imported during migration.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token credential for delegated auth; relevance: OpenCode OpenAI OAuth + Copilot entries are imported from `auth.json`.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: Hermes `auth.json` OAuth entries are legacy state surfaced for manual reauth.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the credential-import prompt and post-import doctor/reauth flow.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed-secret storage/reference; relevance: `--include-secrets`/`--no-auth-credentials` flags + SecretRef-managed credential post-import.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable-without-side-effects property; relevance: dry-run → preview → apply-with-backup → `--json` no-mutate is a repeatable migration contract.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's coding-agent CLI; relevance: sibling coding-agent whose state has an analogous migration path.

**Docs**
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — Claude Code login/auth failure recovery; relevance: post-migration reauth/doctor analog when imported credentials need repair.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth setup; relevance: the credential model the import populates (API keys, OAuth) in a sibling agent.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network error reference; relevance: troubleshooting "API keys did not import" / connectivity after migrate.
- [hermes_cli_commands_ops_maintenance_auth](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — Hermes CLI ops/auth commands; relevance: the source-side Hermes auth surface the migration reads from.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — Hermes credential-pool model; relevance: what the import maps from Hermes `auth.json`/credential storage into OpenClaw auth-profiles.
- [pi_provider_auth](../pi/pi_provider_auth.md) — pi agent provider-auth setup; relevance: cross-agent credential-import analog (third coding agent's auth model).
- [oc_cli_migrate](oc_cli_migrate.md) — `openclaw migrate` full CLI reference (planned, this series — cl05); relevance: the canonical CLI the page's scripted path invokes.
- [oc_cli_onboard](oc_cli_onboard.md) — `openclaw onboard` wizard/flags (planned, this series — cl05); relevance: the `--flow import`/`--import-secrets` wizard entry point.
- [oc_install_migrating](oc_install_migrating.md) — moving an OpenClaw install between machines (planned, this series — in03); relevance: the page's sibling "Migrating" Related link.
- [oc_gateway_doctor](oc_gateway_doctor.md) — `openclaw doctor` health check (planned, this series — gw02); relevance: the post-import "Run doctor" recommended-flow step.
- [oc_concepts_agent_workspace](oc_concepts_agent_workspace.md) — SOUL.md/AGENTS.md/memory workspace (planned, this series — co01); relevance: the destination for imported workspace files.
- [oc_gateway_secrets](oc_gateway_secrets.md) — SecretRef/secrets config (planned, this series — gw05); relevance: configuring the SecretRef source after import per the Secrets section.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product whose install/import path this documents.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard package; relevance: implements `openclaw migrate` + `onboard --flow import`.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: `MEMORY.md`/`USER.md` are appended on import.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: `skills/<name>/SKILL.md` + `skills.config` are copied.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions/state; relevance: `sessions/`/`state.db` are archive-only on import.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — Hermes agent repo; relevance: the migration source product.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — Hermes CLI; relevance: the source-side `claw migrate` two-phase preview implementation.

**Snippets**
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — OpenClaw wizard config-import flow + freshness gate; relevance: the exact `onboard --flow import` detect/import code the page describes.
- [snippet_hermes_agent_cli_claw_migrate](../../code_snippets/snippet_hermes_agent_cli_claw_migrate.md) — Hermes↔OpenClaw migrate with two-phase preview + conflict refusal; relevance: implements dry-run→apply→backup→conflict-skip exactly as the Recommended flow.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard setup-imports stage; relevance: the import-source selection the onboarding wizard runs.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config-write stage; relevance: where imported model/MCP/memory config lands.
- [snippet_hermes_agent_optional_skills_migration_openclaw](../../code_snippets/snippet_hermes_agent_optional_skills_migration_openclaw.md) — Hermes→OpenClaw skills migration; relevance: the `skills/` copy step of the import.
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — backup save with SQLite safe-copy + prune; relevance: the "verified backup before apply" guarantee the migration makes.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — auth-profile import from external CLI logins; relevance: importing OpenCode/Copilot OAuth entries from `auth.json`.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth credential portability across agents; relevance: moving OAuth credentials between Hermes and OpenClaw.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — Hermes auth login/logout; relevance: the source-side auth state the import reads + the reauth path for legacy entries.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential-source resolution order; relevance: which `.env`/`auth.json` sources the migration recognizes.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret redaction patterns; relevance: the plan output "redacts nested secret-looking keys" behavior.
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — doctor auth-directory checks; relevance: the post-import `openclaw doctor` reauth/repair step.

### note 2 — oc_install_nix (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the product installed declaratively via nix-openclaw.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable deterministic operation; relevance: the page's thesis (reproducible, pinned, rollback-able declarative install).
- [DevOps](../../term_dictionary/term_devops.md) — infra-as-code operations practice; relevance: Nix/Home Manager declarative-config management of the gateway.
- [Automation](../../term_dictionary/term_automation.md) — scripted/declarative operations; relevance: `home-manager switch` drives the whole install/config declaratively.
- [node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the runtime OpenClaw ships on, pinned by the Nix flake.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: the package format Nix wraps/pins instead of a global `npm install -g`.
- [Blue-Green Deployment](../../term_dictionary/term_blue_green_deployment.md) — instant-switch/rollback deploy pattern; relevance: `home-manager switch --rollback` is a generation-rollback analog.
- [CodeDeploy](../../term_dictionary/term_codedeploy.md) — managed deployment tooling; relevance: declarative deploy + rollback tooling analog.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed secret storage; relevance: plain-file secrets at `~/.secrets/` (bot token + provider key) the flake references.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated/immutable runtime; relevance: Nix-mode treats `openclaw.json` as immutable and disables self-mutation (read-only managed runtime).

**Docs**
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Hermes Nix quickstart; relevance: the closest existing declarative-Nix-install analog for a sibling agent.
- [hermes_install_nixos_module](../hermes_agent/hermes_install_nixos_module.md) — Hermes NixOS/Home-Manager module; relevance: directly parallels the `nix-openclaw` Home Manager module.
- [hermes_nixos_container_mode](../hermes_agent/hermes_nixos_container_mode.md) — Hermes NixOS container/runtime mode; relevance: the Nix-managed-service runtime-behavior analog (immutable config, service env).
- [cc_install](../claude_code/cc_install.md) — Claude Code install methods; relevance: alternative-install-method peer for a sibling coding agent.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — advanced install + verify; relevance: the "verify the service is running" final Nix step analog.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — environment configuration; relevance: the `OPENCLAW_NIX_MODE`/`OPENCLAW_STATE_DIR`/`OPENCLAW_CONFIG_PATH` env surface.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — env-var reference; relevance: documents the env-var convention the Nix-mode table uses.
- [oc_install_docker](oc_install_docker.md) — containerized non-Nix alternative (planned, this series — in02); relevance: the page's Related "Docker" link.
- [oc_install_updating](oc_install_updating.md) — updating Home-Manager-managed installs (planned, this series — in05); relevance: the page's Related "Updating" link.
- [oc_start_wizard](oc_start_wizard.md) — non-Nix CLI setup wizard (planned, this series — st02); relevance: the page's Related "Setup wizard" link.
- [oc_install_oracle](oc_install_oracle.md) — VPS self-host alternative (planned, this series — in04); relevance: sibling install path (immutable Nix vs imperative VPS).

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product installed via the Nix module.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the launchd/systemd service + immutable `openclaw.json` Nix-mode behavior.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS/desktop app; relevance: the macOS `defaults write ai.openclaw.mac openclaw.nixMode` path.

**Snippets**
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd user-linger + env-file + systemctl exec; relevance: the launchd/systemd service Nix mode manages, incl. service-env PATH.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: the systemd service the Nix module installs.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: the macOS launchd service that "survives reboots" per "What you get".
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: service lifecycle under the Nix-managed launchd agent.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: startup-derived defaults that stay runtime-only under immutable Nix config.
- [snippet_hermes_agent_gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — gateway config load; relevance: reading JSON5 config from a configurable path (the `OPENCLAW_CONFIG_PATH` analog).
- [snippet_hermes_agent_core_hermes_home](../../code_snippets/snippet_hermes_agent_core_hermes_home.md) — home/state-dir resolution; relevance: the `OPENCLAW_HOME`/`OPENCLAW_STATE_DIR` resolution analog.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — config-loading precedence; relevance: how config + state paths are resolved when set to Nix locations.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `config set` writer; relevance: the config-writer class refused in Nix mode (immutable `openclaw.json`).
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — gateway systemd integration; relevance: the systemd-service install/PATH-discovery the page's runtime-behavior section covers.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard; relevance: the non-Nix imperative setup the page contrasts with the declarative flake.

### note 3 — oc_install_node (8t · 11s · 11d)

**Terms**
- [node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the subject (Node 22.19+ required, 24 recommended).
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: `npm install -g`, `npm prefix -g`, global bin/PATH, `EACCES` prefix fix.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: the CLI whose `command not found` failure this troubleshoots.
- [DevOps](../../term_dictionary/term_devops.md) — toolchain/runtime ops; relevance: per-OS Node install + version-manager toolchain setup.
- [Idempotency](../../term_dictionary/term_idempotency.md) — reproducible pinned runtime; relevance: fnm/nvm/mise/asdf give a version-pinned reproducible Node runtime.
- [Automation](../../term_dictionary/term_automation.md) — CI/release workflows; relevance: Node 24 is "the default and recommended runtime for installs, CI, and release workflows".
- [Sandbox](../../term_dictionary/term_sandbox.md) — user-writable isolated prefix; relevance: switching the npm global prefix to a user-writable `~/.npm-global` to avoid root.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: Node version is a CI/release-workflow runtime requirement called out by the page.

**Docs**
- [cc_install](../claude_code/cc_install.md) — Claude Code install; relevance: Node-prereq + per-OS install analog for a sibling agent.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install + verification; relevance: `node -v` version-check + verify analog.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: the PATH/"command not found" diagnostic analog.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — install-failure reference; relevance: the EACCES/permission and PATH failure catalog analog.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — environment config; relevance: the shell-startup `export PATH=...` to `~/.zshrc`/`~/.bashrc` step.
- [hermes_faq_install_provider_terminal](../hermes_agent/hermes_faq_install_provider_terminal.md) — Hermes install/terminal FAQ; relevance: sibling-agent install-prereq + PATH FAQ analog.
- [hermes_installation](../hermes_agent/hermes_installation.md) — Hermes installation guide; relevance: Node/npm prerequisite install for a sibling coding agent.
- [oc_install_installer](oc_install_installer.md) — the auto-Node-detecting `install.sh` (planned, this series — in03); relevance: the installer the page says "will detect and install Node automatically".
- [oc_install_updating](oc_install_updating.md) — keeping OpenClaw up to date (planned, this series — in05); relevance: the page's Related "Updating" link.
- [oc_start_getting_started](oc_start_getting_started.md) — first steps after install (planned, this series — st01); relevance: the page's Related "Getting Started" link.
- [oc_install_nix](oc_install_nix.md) — declarative Nix-pinned runtime (planned, this series — in04); relevance: the Nix alternative that pins Node without manual version managers.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product whose Node runtime this provisions.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI package; relevance: the `openclaw` binary whose `command not found` PATH issue this fixes.

**Snippets**
- [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — POSIX bootstrap: 3-tier Node resolution + `npm install -g --prefix` no-sudo; relevance: directly mirrors the EACCES-avoiding user-prefix fix + Node version resolution.
- [snippet_hermes_agent_acp_bootstrap_ps1](../../code_snippets/snippet_hermes_agent_acp_bootstrap_ps1.md) — PowerShell bootstrap (Windows); relevance: the Windows winget/PATH install path of the page.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows `npm.cmd`→`node.exe` shim + PATH-hijack defense; relevance: Windows global-bin/PATH resolution behind the `openclaw` command.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: the entry point that fails when Node/PATH is misconfigured.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root/permission guard; relevance: the permission model behind `npm install -g` EACCES on Linux.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer that detects/installs Node; relevance: the auto-Node-detecting `install.sh` the page references.
- [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — `setup.sh` POSIX installer; relevance: per-OS Node install + PATH wiring analog.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verification; relevance: the `node -v` version-check + post-install verify step.
- [snippet_hermes_agent_lsp_servers_install](../../code_snippets/snippet_hermes_agent_lsp_servers_install.md) — npm-based server install; relevance: `npm install -g` global-package install + prefix behavior.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard; relevance: the first-run flow that surfaces Node-prereq failures.
- [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall handling global npm package; relevance: the npm global-prefix/bin lifecycle this troubleshoots.

### note 4 — oc_install_northflank (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: the product one-click-deployed on Northflank.
- [Serverless](../../term_dictionary/term_serverless.md) — managed-platform deploy model; relevance: Northflank is a managed PaaS one-click template deploy.
- [DevOps](../../term_dictionary/term_devops.md) — deploy operations; relevance: template-driven cloud deploy + env-var config.
- [Automation](../../term_dictionary/term_automation.md) — scripted/template deploy; relevance: "Deploy stack" builds and runs the template automatically.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/secret verification; relevance: connecting to `/openclaw` with the configured shared secret.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token shared secret; relevance: the required `OPENCLAW_GATEWAY_TOKEN` shared-secret auth.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed secret config; relevance: the strong-random gateway token set as a platform env var.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: "Connect a channel" wires a Telegram/Discord bot to the hosted gateway.

**Docs**
- [cc_cloud_environment](../claude_code/cc_cloud_environment.md) — Claude Code cloud environment; relevance: managed-cloud-runtime analog (gateway hosted, no terminal on server).
- [cc_execution_environments](../claude_code/cc_execution_environments.md) — execution-environment options; relevance: hosted vs local runtime choice analog.
- [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting/provisioning/scaling; relevance: the managed-PaaS hosting + persistent-volume provisioning analog.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes container run modes; relevance: the hosted-container deploy shape Northflank provides.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — pi cloud-provider hosting; relevance: cross-agent managed-cloud-deploy analog.
- [oc_gateway_configuration](oc_gateway_configuration.md) — gateway config reference (planned, this series — gw02); relevance: the page's "Configure the Gateway" next-step link.
- [oc_install_updating](oc_install_updating.md) — keeping OpenClaw up to date (planned, this series — in05); relevance: the page's "Updating" next-step link.
- [oc_channels](oc_channels.md) — channels overview (planned, this series — ch0x/rt01); relevance: the "Connect a channel" / "All channels" links.
- [oc_web_control_ui](oc_web_control_ui.md) — the browser Control UI at `/openclaw` (planned, this series — wb01); relevance: the no-terminal access surface the deploy exposes.
- [oc_install_oracle](oc_install_oracle.md) — VPS self-host alternative (planned, this series — in04); relevance: the self-host counterpart to managed PaaS.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product the template deploys.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the hosted Gateway the template runs with token auth.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — web/desktop apps; relevance: the browser Control UI at `/openclaw`.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels subsystem; relevance: the channel the deploy connects.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Telegram/Discord bot the Control UI / `onboard` connects.

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode schema + token/identity; relevance: the `OPENCLAW_GATEWAY_TOKEN` token-auth mode the template requires.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth authorize/dispatch; relevance: how the shared-secret token gates Control-UI requests.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — server runtime config; relevance: the hosted gateway runtime config behind the public URL.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: `openclaw onboard` over SSH for channel setup.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command policy table; relevance: the `openclaw onboard`/dashboard commands run on the hosted instance.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persistence; relevance: the `/data` volume keeps sessions/state surviving redeploys.
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — session-level overrides; relevance: per-agent `auth-profiles.json`/session state persisted on `/data`.
- [snippet_hermes_agent_cli_web_app](../../code_snippets/snippet_hermes_agent_cli_web_app.md) — web Control-UI app server; relevance: the browser Control UI served at `/openclaw`.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect; relevance: the "fastest — just a bot token" Telegram channel the deploy connects.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway lifecycle; relevance: the hosted Gateway start/run lifecycle Northflank manages.

### note 5 — oc_install_oracle (12t · 12s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: the persistent gateway hosted free on Oracle Cloud.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: SSH key pair + initial `ssh ubuntu@PUBLIC_IP` access.
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote shell access; relevance: Tailscale SSH replacing sshd for tailnet-only admin.
- [VPN](../../term_dictionary/term_vpn.md) — virtual private network; relevance: Tailscale tailnet/Serve is the sole ingress after lockdown.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end proxy; relevance: Tailscale Serve fronts the loopback-bound gateway.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — proxy/forwarded-IP handling; relevance: `gateway.trustedProxies=["127.0.0.1"]` for the local Serve proxy's forwarded-IP handling.
- [Security Group](../../term_dictionary/term_security_group.md) — network ingress firewall rules; relevance: the VCN Security List locked to only `0.0.0.0/0 UDP 41641`.
- [VPC](../../term_dictionary/term_vpc_virtual_private_cloud.md) — virtual private cloud network; relevance: the OCI VCN being locked down at the network edge.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: `gateway.auth.mode token` + generated gateway token.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/exposure analysis; relevance: the "which traditional hardening steps are still needed?" posture table.
- [Access Control](../../term_dictionary/term_access_control.md) — permission/identity gating; relevance: tailnet-identity admin access + credential file `chmod 700`.
- [Health Check](../../term_dictionary/term_health_check.md) — service-health verification; relevance: `openclaw doctor`/`gateway status`/`security audit`/`curl localhost:18789` verification.

**Docs**
- [aws_ec2_security_groups_concepts](../aws_ec2/aws_ec2_security_groups_concepts.md) — EC2 security-group model; relevance: the ingress-firewall concept the OCI VCN Security List implements.
- [aws_ec2_security_groups_procedures](../aws_ec2/aws_ec2_security_groups_procedures.md) — security-group rule procedures; relevance: the "remove all ingress except UDP 41641" rule-editing analog.
- [aws_ec2_overview](../aws_ec2/aws_ec2_overview.md) — EC2 instance/VPC overview; relevance: the cloud-VM-instance + VCN mental model behind the OCI ARM instance.
- [cc_cloud_environment](../claude_code/cc_cloud_environment.md) — cloud-environment setup; relevance: remote-host coding-agent runtime analog.
- [cc_execution_environments](../claude_code/cc_execution_environments.md) — execution environments; relevance: remote-VPS execution-environment choice analog.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — hardened-default environment; relevance: the security-posture/hardening-tradeoff analog of the "needed?" table.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth over SSH tunnel; relevance: the SSH-tunnel fallback (`ssh -L 18789:127.0.0.1:18789`) the page documents.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation/perms; relevance: the `chmod 700 ~/.openclaw` + credential-perms "still recommended" items.
- [oc_gateway_tailscale](oc_gateway_tailscale.md) — Tailscale gateway config (planned, this series — gw06); relevance: the canonical Tailscale Serve/SSH config the page applies.
- [oc_gateway_configuration](oc_gateway_configuration.md) — gateway config reference (planned, this series — gw02); relevance: the `gateway.bind`/`auth.mode`/`trustedProxies` settings.
- [oc_install_gcp](oc_install_gcp.md) — GCP self-host (planned, this series — in02); relevance: the page's Related "GCP" cloud alternative.
- [oc_vps](oc_vps.md) — generic VPS hosting (planned, this series — rt03); relevance: the page's Related "VPS hosting" link.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product self-hosted on the OCI instance.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: loopback bind + token auth + Tailscale Serve config.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: `openclaw security audit` posture check + credential perms.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions/state; relevance: `~/.openclaw` state/persistence that survives reboots.

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode schema + Tailscale identity stack; relevance: `auth.mode token` + Tailscale-identity verification the setup configures.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client-connect over proxy; relevance: Tailscale Serve reverse-proxy + `trustedProxies` forwarded-IP handling.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP bind; relevance: `gateway.bind loopback` the runbook sets.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security-audit composition + filesystem/gateway findings; relevance: the `openclaw security audit` posture check the page recommends.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe execution; relevance: what `openclaw security audit` actually probes for the posture verification.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — security fix/remediation; relevance: remediating findings (credential perms, exposure) the posture table calls out.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd user-linger; relevance: `loginctl enable-linger ubuntu` + `systemctl --user` gateway service.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — gateway systemd integration; relevance: `systemctl --user restart openclaw-gateway.service`.
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — backup save; relevance: the `openclaw backup create` persistence/snapshot step.
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — doctor primitives; relevance: `openclaw doctor --non-interactive` troubleshooting.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health; relevance: `systemctl --user status` + `openclaw --version`/gateway status verify.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — doctor API connectivity; relevance: `curl http://localhost:18789` + connectivity verification.

### note 6 — oc_install_podman (10t · 12s · 11d)

**Terms**
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: Podman is the rootless Docker alternative; the page's sibling is Docker.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: the gateway run inside the Podman container.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated container runtime; relevance: rootless `--userns=keep-id` user-namespace container isolation.
- [VPN](../../term_dictionary/term_vpn.md) — virtual private network; relevance: Tailscale Serve over the `127.0.0.1`-published gateway port.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end proxy; relevance: host-managed `tailscale serve` fronting the published container port.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/secret verification; relevance: `OPENCLAW_GATEWAY_TOKEN` + in-container model auth (device-code/OAuth Codex).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token credential; relevance: the gateway token in `~/.openclaw/.env` + OpenAI Codex OAuth.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage/allowlist; relevance: the `.env` token + Podman-key allowlist the launcher passes.
- [Health Check](../../term_dictionary/term_health_check.md) — service-health verification; relevance: `openclaw gateway status --deep` (RPC probe + service scan)/`doctor`.
- [DevOps](../../term_dictionary/term_devops.md) — service-management ops; relevance: Quadlet/systemd-user auto-start + linger boot persistence.

**Docs**
- [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — devcontainer setup; relevance: the container-runtime setup analog for a sibling agent.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — hardened container defaults; relevance: the Quadlet "fixed, hardened default shape" (127.0.0.1 publish, keep-id userns).
- [cc_sandbox_environments_comparison](../claude_code/cc_sandbox_environments_comparison.md) — sandbox-environment comparison; relevance: rootless-Podman vs Docker vs host sandbox tradeoff.
- [cc_execution_environments](../claude_code/cc_execution_environments.md) — execution environments; relevance: containerized vs host execution-environment choice.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes container run modes; relevance: the direct container-run analog (rootless, bind-mounts, ports).
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker volumes + supervision; relevance: the bind-mounted `~/.openclaw` state + systemd supervision analog.
- [pi_containerization](../pi/pi_containerization.md) — pi containerization; relevance: cross-agent containerized-gateway analog.
- [oc_install_docker](oc_install_docker.md) — Docker container install (planned, this series — in02); relevance: the page's primary "Docker" sibling/Related link.
- [oc_gateway_tailscale](oc_gateway_tailscale.md) — Tailscale gateway config (planned, this series — gw06); relevance: the "Podman and Tailscale" HTTPS/remote-access guidance.
- [oc_gateway_background_process](oc_gateway_background_process.md) — gateway background process (planned, this series — gw03); relevance: the page's Related "Gateway background process" link.
- [oc_gateway_troubleshooting](oc_gateway_troubleshooting.md) — gateway troubleshooting (planned, this series — gw07); relevance: the page's Related "Gateway troubleshooting" link (EACCES, mode, SELinux).

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the product run in the Podman container.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: `gateway.mode=local`/bind/controlUi inside the container.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — dashboard/Control UI; relevance: `openclaw dashboard --no-open` + the local dashboard on the published port.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions/state; relevance: bind-mounted `~/.openclaw` state surviving container replacement.

**Snippets**
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — container env (run/bind/userns); relevance: the rootless container run + bind-mount model Podman uses.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: the Quadlet `openclaw.container` systemd-user unit.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger + env-file; relevance: `loginctl enable-linger` boot persistence + `~/.openclaw/.env` EnvironmentFile.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — gateway systemd integration; relevance: `systemctl --user start/stop/status openclaw.service` Quadlet management.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode + token; relevance: `OPENCLAW_GATEWAY_TOKEN` token auth in `~/.openclaw/.env`.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets handling; relevance: the in-container model auth + `.env` token/allowlist.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — auth-profiles from external CLI; relevance: the note that host `~/.claude`/`~/.codex` are NOT mounted; keep auth in mounted `~/.openclaw`.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persistence; relevance: `openclaw.json`/`auth-profiles.json`/sessions surviving container replacement via bind-mount.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `openclaw --container <name> ...` host-CLI commands routed into the container.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health; relevance: `openclaw gateway status --deep` RPC probe + service scan.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — security audit exec runtime; relevance: SELinux/`:Z` bind-mount + hardened-runtime posture in the container.

## Undigested Terms Plan (Step 4e)

Per master design decision: OpenClaw install/deploy vocabulary is documented in these `oc_*` doc notes (the pages ARE the documentation of those concepts), NOT promoted to new `term_dictionary` entries. The only `term_dictionary` interaction is **linking existing** terms (verified above). No term definition is inlined in any `oc_*` note.

| Term (appears in source) | Disposition |
|---|---|
| OpenClaw / OpenClaw Gateway | Link existing `term_openclaw`; gateway specifics documented in `oc_*` + `repo_openclaw_gateway`. |
| migration provider / `openclaw migrate` / onboarding import | Documented as the procedure in `oc_install_migrating_hermes`; CLI ref is sibling `oc_cli_migrate` (cl05). No new term. |
| MCP servers | Link existing `term_mcp`. |
| Nix / NixOS / Home Manager / nix-openclaw / Nix mode | Documented in `oc_install_nix`; link `term_idempotency`/`term_devops`. No new `term_nix` (single-page niche install method; not vault-cross-cutting). If a reusable IaC term is later wanted, best-fit glossary is the gen-AI-dev / DevOps glossary — flagged, not captured here (expected 0). |
| Node.js / npm / nvm/fnm/mise/asdf | Link existing `term_node_js`, `term_npm`. No new term for version managers. |
| Tailscale / Tailscale Serve / tailnet / Tailscale SSH | Documented in `oc_install_oracle`/`oc_install_podman` + sibling `oc_gateway_tailscale` (gw06); link `term_vpn`, `term_ssh`/`term_remote_ssh`, `term_reverse_proxy`. No new `term_tailscale` (covered by the gateway/tailscale doc page + VPN term). |
| Podman / Quadlet / rootless / `--userns=keep-id` | Documented in `oc_install_podman`; link `term_docker` (the closest existing container term) + `term_sandbox`. No new `term_podman`/`term_quadlet` (single-page; container concept covered by `term_docker`). |
| Northflank / one-click PaaS template | Documented in `oc_install_northflank`; link `term_serverless`/`term_devops`. No new term. |
| Oracle Cloud / OCI / VCN / Security List / Always Free ARM (aarch64) | Documented in `oc_install_oracle`; link `term_vpc_virtual_private_cloud`, `term_security_group`, `term_aws`/`term_serverless` as cloud analogs. No new `term_oracle_cloud`/`term_arm` (single-page provider specifics). |
| gateway token auth / `OPENCLAW_GATEWAY_TOKEN` / SecretRef | Link existing `term_authentication`, `term_oauth_token`, `term_secrets_manager`; SecretRef detail is sibling `oc_gateway_secrets` (gw05). No new term. |
| `openclaw doctor` / `security audit` / backup | Documented as steps; link `term_health_check`; CLI refs are siblings (gw02/cl0x). No new term. |

**New `term_dictionary` captures from in04: 0 (expected, matches master corpus-wide near-0 forecast).** No genuinely cross-cutting, vault-reusable term lacking an existing note and a doc-page home was found. Augment Step 2d re-confirms.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order/forbidden-fields, `# OpenClaw — …` H1, `## Overview`, `## Related Notes`, `## References`, bold footer | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim/command traces to `inbox/openclaw_docs/install/<page>.md` (no invented flags/paths) | diff vs mirror source per note |
| G3 | Density + coverage: ≤400 lines, ≤2500 words, ≤6 code blocks, single BB; all source H2/H3 covered (coverage map) | word/fence count + section map check |
| G4 | Cross-reference: ≥8 relevance-selected terms + ≥10 snippets + ≥10 docs per note (LOCKED mapping above), each an indexed `[text](path.md)` link with a relevance statement | `## Related Notes` audit |
| G5 | Ghost-reference detect + redirect: every cited EXISTING target resolves in DB; planned siblings flagged `(planned)` | `note_links` + `sqlite3` existence check |
| G6 | Broken-link fix: relative paths resolve | `/tessellum-fix-broken-links` |
| G7 | Discoverability: each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | inlink wiring (below) |
| G8 | In-degree ≥1 / anti-island: satisfied via `entry_openclaw_docs.md` rows + repo/term inlinks | `in_degree` post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_install_migrating_hermes oc_install_nix oc_install_node oc_install_northflank oc_install_oracle oc_install_podman"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format + broken-link (LINK-003) sweep
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density caps (body only, excl. frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w ${cb}cb ${lines}L)"
  # sibling-prefix presence (G4 — at least one oc_ sibling link)
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING $SIBLING_PREFIX LINK in $n"
done

# YAML frontmatter validation across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference: every EXISTING cited target must resolve in the DB
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for f in $GATE_DIR/oc_install_{migrating_hermes,nix,node,northflank,oracle,podman}.md; do
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/^\]\(//; s/\)$//' | while read -r rel; do
    base=$(basename "$rel")
    case "$base" in oc_install_migrating_hermes.md|oc_install_nix.md|oc_install_node.md|oc_install_northflank.md|oc_install_oracle.md|oc_install_podman.md) continue;; esac
    [ -z "$r" ] && echo "GHOST or PLANNED-sibling: $base (in $(basename "$f"))"
  done
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Digest code (≤6) | Lines (≤400) | Within caps? |
|---|---|---|---:|---:|---:|---:|---|
| 1 | oc_install_migrating_hermes | procedure | 650 | 8 | ≤6 (wizard+CLI import, dry-run/apply, doctor, restart, json) | ~180 | ✅ |
| 2 | oc_install_nix | procedure | 550 | 4 | ≤4 (flake mkdir, switch, `OPENCLAW_NIX_MODE` export, macOS `defaults write`) | ~140 | ✅ |
| 3 | oc_install_node | procedure | 500 | 11 | ≤6 (node -v, one install cmd per OS, fnm example, PATH export, npm prefix fix) | ~150 | ✅ |
| 4 | oc_install_northflank | procedure | 350 | 0 | 0 | ~90 | ✅ |
| 5 | oc_install_oracle | procedure | 750 | 10 | ≤6 (instance ssh+update, Tailscale, install, gateway config block, VCN/verify, backup) | ~200 | ✅ |
| 6 | oc_install_podman | procedure | 700 | 8 | ≤6 (setup/launch, quadlet, OPENCLAW_CONTAINER export, host CLI cmds, env vars) | ~190 | ✅ |

No note approaches caps. The three code-heavier pages (node 11, oracle 10, podman 8 fences) stay ≤6 by reproducing only load-bearing commands (one tab/command per OS or per step) and prosing the remainder; full command catalogs are deferred to the verbatim mirror.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links to wire at execution (each satisfies G7/G8; DB-verify at execution). The `entry_openclaw_docs.md` row is the guaranteed inbound link for every note; the repo/term/entry inlinks below add reciprocal discoverability:

- `entry_openclaw_docs.md` (master pre-step) → all 6 notes (Install cluster rows). **Primary G8 satisfier.**
- `repo_openclaw.md` → notes 1, 2, 5, 6 (install/deploy/migrate of the product).
- `repo_openclaw_cli_wizard.md` → notes 1, 3 (`openclaw migrate`/`onboard`; `openclaw` CLI not-found).
- `repo_openclaw_gateway.md` → notes 2, 4, 5, 6 (gateway service/bind/token across Nix/PaaS/VPS/container).
- `repo_openclaw_security.md` → note 5 (`openclaw security audit` posture).
- `repo_hermes_agent.md` / `repo_hermes_agent_cli.md` → note 1 (migration source).
- `term_node_js.md` / `term_npm.md` → note 3; `term_docker.md` → note 6; `term_vpn.md` → notes 5, 6; `term_idempotency.md` → note 2 (reciprocal term backlinks where the term note benefits from the install example).

## Pacing Rules (inherited from master)

One execution phase (6 procedure notes, P1). Re-read each source page before authoring its note; reproduce commands verbatim (selectively, ≤6 fences/note). One BB per note. Run all 8 gates before commit; incremental reindex; verify `note_links` + 0 broken links + in-degree ≥1; `git pull --rebase --autostash` first, commit + push the wave (no Claude co-author trailer). Fan-out cap ~30 agents/run is not a constraint at 6 notes.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note Related Notes mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints pass) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**What was locked (per-note counts, all floors met):**

| Note | Terms | Snippets | Docs (existing / planned) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_install_migrating_hermes | 10 | 12 | 12 (6 existing / 6 planned) | 7 | ✅ |
| oc_install_nix | 10 | 11 | 11 (7 / 4) | 3 | ✅ |
| oc_install_node | 8 | 11 | 11 (7 / 4) | 2 | ✅ |
| oc_install_northflank | 8 | 10 | 10 (5 / 5) | 5 | ✅ |
| oc_install_oracle | 12 | 12 | 12 (8 / 4) | 4 | ✅ |
| oc_install_podman | 10 | 12 | 11 (7 / 4) | 4 | ✅ |

**Verification performed:**
- **≥5 existing docs per note:** confirmed (6/7/7/5/8/7); the balance to ≥10 is sibling `oc_*` docs flagged `(planned, this series / cross-series)`, authored by their own sub-plans (in02/in03/in05, cl05, gw02/gw03/gw05/gw06/gw07, co01, st01/st02, wb01, rt03, ch0x).

**Source re-read (CP7 measure):** body-only word counts measured 2026-06-21 — migrating-hermes 990w, nix 514w, node 482w, northflank 219w, oracle 1017w, podman 1147w (all 0.85–1.0× the plan Source-table estimates; none under-estimated; all single-BB procedure, comfortably within density caps).

**New-term candidates:** **0.** The augment re-read (Step 2d) surfaced no genuinely cross-cutting, vault-reusable term lacking BOTH an existing `term_dictionary` note AND a doc-page home — consistent with the master's corpus-wide near-0 forecast and the in04 Undigested Terms Plan. Install/deploy vocabulary (Nix/NixOS/Home-Manager, Podman/Quadlet/rootless, Tailscale/tailnet/Serve, Northflank, Oracle Cloud/OCI/VCN, `OPENCLAW_GATEWAY_TOKEN`/SecretRef, version managers) is documented in the `oc_*` doc notes themselves; existing terms are linked. If a reusable IaC term were ever wanted, best-fit glossary would be the **gen-AI-dev / DevOps glossary** (`entry_gen_ai_dev` cluster) — flagged, not captured here (expected 0). **No `/tessellum-capture-term-note` obligations for in04.**

**Issues:** none blocking. The 4 cited Tab/Step-embedded MDX fences cause a divergence between `grep '^```'` (counts only column-0 fences) and the plan's per-page fence totals (counts indented in-component fences too); the plan's higher counts are the conservative figure for density, so no caps are at risk either way.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_in04.md
Date: 2026-06-21
```

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + floors (≥10 snippets, ≥10 docs), each an indexed link with a relevance statement | **PASS** | Per-Note Related Notes Mapping (LOCKED) present; deterministic count: every note ≥8t/≥10s/≥10d (10·12·12 / 10·11·11 / 8·11·11 / 8·10·10 / 12·12·12 / 10·12·11); every line is `- [Name](relpath.md) — what; relevance: why`. |
| CP2 | ALL 8 GATEs present per batch (G1–G6 + G7/G8 discoverability) | **PASS** | Per-Phase Validation Gate table lists G1–G8 with check + tool/method; G4 updated to the raised ≥8t/≥10s/≥10d floor; G5 ghost + G6 broken-link present; Validation Scripts include G1/format, density caps, G5 ghost-resolve loop, YAML check. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at master W1) + size-decision matches threshold | **PASS** | Entry Point Decision section: contributes 6 rows to `entry_openclaw_docs.md` (created at master W1 pre-step); no new entry point (correct — 6 notes < 15 ⇒ UPDATE/contribute-rows; the >30 master hub is the master's responsibility). `entry_openclaw_docs` cited as `(planned)` consistently. |
| CP4 | Plan size (≤30 or split) | **PASS** | 6 planned notes, single execution phase. Well under 30. |
| CP5 | Note format derived from existing notes | **PASS** | Format Definition inherited from master (derived from existing `cc_*`/`pi_*` doc corpora): YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`; body `# OpenClaw — …` → `## Overview` → mirrored H2/H3 → `## Related Notes` → `## References` → bold footer; forbidden fields enumerated. Matches `resources/documentation/openclaw/` (folder exists) sibling-corpus convention. |
| CP6 | Density / borderline-split | **PASS** | Density Re-Assessment: max note = oracle 750w / podman 700w, all ≤~200 lines, all ≤6 code blocks, single-BB procedure. Measured source bodies (990/514/482/219/1017/1147w) confirm no note crosses caps. No borderline note requires a split; Split Decisions = NONE (justified). |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 6 pages re-read 2026-06-21 and measured: 990/514/482/219/1017/1147 body words — every page 0.85–1.0× the plan Source-table estimate (≤1.5× rule satisfied; none under-estimated). |
| CP8 | Undigested Terms Plan + Authoring Requirements present; multi-source language | **PASS** | Undigested Terms Plan table present (11 rows, every row dispositioned "link existing / documented in oc_* / No new term"); Term-Note Authoring Requirements = N/A (0 new terms) with the master's inherited `/tessellum-capture-term-note` multi-source mandate stated for the contingency. New-term captures: 0 (expected). |
| CP8f | Term-slug specificity + all-notes (term AND doc) dedup/collision audit | **PASS** | 0 new term slugs ⇒ no specificity rename needed. Dedup/collision: every planned `oc_*` doc note is a NEW filename (`oc_install_*`), and the dedup policy (link existing `term_*`/`repo_openclaw*`, never recreate) is applied — no planned note duplicates an existing term or doc note. The 6 `oc_install_*` slugs do not collide with any existing vault note (folder is new; DB has no `oc_install_*`). |
| CP9 | Discoverability / inlinks (G8 inbound, no graph islands) | **PASS** | Inlinks section maps outside-folder inbound links for all 6 notes: `entry_openclaw_docs.md` → all 6 (primary G8 satisfier) + repo/term/entry reciprocal inlinks; G7/G8 in the gate table; inlink wiring is an execution step, not "recommended". |

**RESULT: 9/9 (CP1–CP9, incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
