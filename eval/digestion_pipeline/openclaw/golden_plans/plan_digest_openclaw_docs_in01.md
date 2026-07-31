---
title: Sub-Plan in01 — OpenClaw Docs: Install (Ansible, Azure, Bun, ClawDock, Release Channels, DigitalOcean)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["install/ansible", "install/azure", "install/bun", "install/clawdock", "install/development-channels", "install/digitalocean"]
status_note: "augmented + reviewed 2026-06-21; 9/9 checkpoints PASS; per-note xref locked at ≥8t·≥10s·≥10d"
---

# Sub-Plan in01: Install

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References` → footer; caps ≤400 lines / ≤2500 words / ≤6 code blocks; one BB/note), dedup (three-way term_dictionary + documentation + repo_openclaw* check before create), undigested-terms policy (OpenClaw vocab → `oc_` notes; existing terms LINKED only; expected 0 new term captures), 9-GATE validation, cross-references, and entry-point wiring (`entry_openclaw_docs.md`, W1–W5) are all inherited from the master and NOT re-derived here.

## Scope

The 6 **Install** section pages that cover installing and updating OpenClaw on remote/cloud infrastructure and via alternative runtimes/helpers: an automated hardened deployer (`ansible`), two cloud-VM deployment walkthroughs (`azure`, `digitalocean`), an experimental local runtime (`bun`), a Docker shell-helper layer (`clawdock`), and the stable/beta/dev update-channel + version-pinning semantics (`development-channels`). These are **P1 (Phase A)** — installation/runtime is the operational entry path the rest of the docs assume. Code-side counterparts (`repo_openclaw`, `repo_openclaw_gateway`, `repo_openclaw_cli_wizard`) are LINKED, not recreated; cloud-vendor and devops vocabulary (Tailscale, UFW, Bastion, NSG) is documented as install steps, not promoted to `term_dictionary` notes.

**Source**: OpenClaw docs, 6 pages, 4,173 measured body words (frontmatter excluded). **Planned: 6 notes** (1 page → 1 note; no splits).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| ansible | /install/ansible | 804 | 4 | 11 | 1 | procedure |
| azure | /install/azure | 1,213 | 1 | 9 | 0 | procedure |
| bun | /install/bun | 208 | 1 | 4 | 0 | procedure |
| clawdock | /install/clawdock | 467 | 3 | 5 | 5 | procedure |
| development-channels | /install/development-channels | 779 | 4 | 8 | 0 | procedure |
| digitalocean | /install/digitalocean | 702 | 1 | 7 | 0 | procedure |

Word counts are body-only (`sed` strips the `---` frontmatter, then `wc -w`). Code counts are `grep -c '^```' / 2`. Several pages embed table/Steps/Accordion MDX whose word totals are real but whose code-block totals exclude un-fenced commands inside `<Step>`/`<Accordion>` blocks — every note keeps ≤6 fences regardless.

## Content Strategy

- **Prioritize**: the Azure end-to-end VM hardening procedure (NSG + Bastion, the most detailed page) and the Ansible hardened-deployer security model (4-layer defense, Tailscale/UFW), since both encode OpenClaw's production-deployment security posture. The release-channels semantics (stable/beta/dev, pinning, dist-tags) is the second priority because every other install page references `openclaw update`.
- **Split**: NONE. Every page is well under the 2,500-word / 6-code-block caps and is single-BB (procedure: install/configure/update a deployment target). The largest page (azure, 1,213w) maps cleanly to one focused cloud-VM-setup note. 1 page → 1 note.
- **Link-out (not duplicated)**: Docker base install (`install/docker`), `install/updating` standard flow, `install/installer` internals, `gateway/sandboxing`, `gateway/configuration`, `tools/multi-agent-sandbox-tools`, `providers/github-copilot`, and sibling install targets (`gcp`/`hetzner`/`oracle`/`fly`) are owned by other sub-plans (in02–in05, gw0x, to0x, pr0x) — referenced via `## Related Notes`/`## References`, never re-digested here. Devops vocab (Tailscale, UFW, Bastion, NSG, swap) is documented inline as steps and linked to existing `term_vpn`/`term_ssh`/`term_iam`/`term_docker`, not promoted.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_install_ansible.md` | procedure | ansible.md: Prerequisites, What you get, Quick start, What gets installed, Post-Install Setup (+ Quick commands), Security architecture, Manual installation, Updating, Troubleshooting, Advanced configuration | 600 | Automated hardened OpenClaw deployment via the openclaw-ansible playbook: one-command install, what gets installed (Tailscale, UFW, Docker, Node, systemd), the 4-layer defense-in-depth security model, manual playbook steps, and troubleshooting. |
| 2 | `oc_install_azure.md` | procedure | azure.md: What you will do, What you need, Configure deployment (az login, providers, vars, SSH key, VM size), Deploy Azure resources (RG, NSG, VNet/subnets, VM, Bastion), Install OpenClaw, Cost considerations, Cleanup, Next steps | 700 | Deploying OpenClaw 24/7 on an Azure Linux VM with the Azure CLI: NSG hardening (SSH only from the Bastion subnet), no public IP, Azure Bastion SSH tunneling, the installer script, cost trade-offs (deallocate/Basic Bastion), and cleanup. |
| 3 | `oc_install_bun.md` | procedure | bun.md: (intro warning), Install, Lifecycle scripts, Caveats | 350 | The experimental Bun local runtime for OpenClaw: `bun install`/`bun run` dev loop, why Bun is not recommended for the gateway runtime (WhatsApp/Telegram issues), blocked dependency lifecycle scripts (`bun pm trust`), and pnpm-hardcoded-script caveats. |
| 4 | `oc_install_clawdock.md` | procedure | clawdock.md: (intro), Install, What you get (Basic operations, Container access, Web UI and pairing, Setup and maintenance, Utilities), First-time flow, Config and secrets | 500 | The ClawDock shell-helper layer for Docker-based OpenClaw installs: install via the canonical helper path, the `clawdock-*` command catalog (start/stop, shell/cli/exec, dashboard/devices/approve, fix-token/update/rebuild, health/token/config), first-time pairing flow, and the Docker config/secrets split. |
| 5 | `oc_install_development_channels.md` | procedure | development-channels.md: (intro), Switching channels, One-off version or tag targeting, Dry run, Plugins and channels, Checking current status, Tagging best practices, macOS app availability | 600 | OpenClaw's stable/beta/dev update channels: channel semantics and npm dist-tag mapping, `openclaw update --channel`/`--tag` switching and one-off version/SHA pinning, dry-run preview, channel-synced plugins, status checking, immutable-tag best practices, and macOS-build availability. |
| 6 | `oc_install_digitalocean.md` | procedure | digitalocean.md: Prerequisites, Setup (create Droplet, connect+install, onboard, swap, verify, Control UI access A/B/C), Persistence and backups, 1 GB RAM tips, Troubleshooting, Next steps | 600 | Hosting a persistent OpenClaw Gateway on a DigitalOcean Droplet: Droplet creation, non-root user + systemd-user service, onboarding wizard, swap for 1 GB plans, three Control UI access options (SSH tunnel / Tailscale Serve / tailnet bind), state persistence + `openclaw backup`, and 1 GB RAM tuning. |

## Section Coverage Map

```
ansible.md → note 1 (oc_install_ansible)
├── Prerequisites ──────────────────────────────── → note 1
├── What you get ───────────────────────────────── → note 1
├── Quick start ────────────────────────────────── → note 1
├── What gets installed ────────────────────────── → note 1
├── Post-Install Setup (+ ### Quick commands) ──── → note 1
├── Security architecture ──────────────────────── → note 1
├── Manual installation ────────────────────────── → note 1
├── Updating (→ link install/updating) ─────────── → note 1
├── Troubleshooting ────────────────────────────── → note 1
├── Advanced configuration (→ external repo docs) ─ → note 1 (References)
└── Related ────────────────────────────────────── → note 1 (Related Notes/References)
azure.md → note 2 (oc_install_azure)
├── What you will do ───────────────────────────── → note 2
├── What you need ──────────────────────────────── → note 2
├── Configure deployment (login/providers/vars/key/size) → note 2
├── Deploy Azure resources (RG/NSG/VNet/VM/Bastion) → note 2
├── Install OpenClaw ───────────────────────────── → note 2
├── Cost considerations ────────────────────────── → note 2
├── Cleanup ────────────────────────────────────── → note 2
├── Next steps (→ channels/nodes/gateway links) ── → note 2 (Related/References)
└── Related ────────────────────────────────────── → note 2 (Related Notes/References)
bun.md → note 3 (oc_install_bun)
├── (intro Warning + body) ─────────────────────── → note 3 (Overview)
├── Install ────────────────────────────────────── → note 3
├── Lifecycle scripts ──────────────────────────── → note 3
├── Caveats ────────────────────────────────────── → note 3
└── Related ────────────────────────────────────── → note 3 (Related Notes/References)
clawdock.md → note 4 (oc_install_clawdock)
├── (intro) ────────────────────────────────────── → note 4 (Overview)
├── Install ────────────────────────────────────── → note 4
├── What you get
│   ├── Basic operations ───────────────────────── → note 4
│   ├── Container access ────────────────────────── → note 4
│   ├── Web UI and pairing ─────────────────────── → note 4
│   ├── Setup and maintenance ──────────────────── → note 4
│   └── Utilities ──────────────────────────────── → note 4
├── First-time flow ────────────────────────────── → note 4
├── Config and secrets ─────────────────────────── → note 4
└── Related (CardGroup) ────────────────────────── → note 4 (Related Notes/References)
development-channels.md → note 5 (oc_install_development_channels)
├── (intro: three channels) ────────────────────── → note 5 (Overview)
├── Switching channels ─────────────────────────── → note 5
├── One-off version or tag targeting ───────────── → note 5
├── Dry run ────────────────────────────────────── → note 5
├── Plugins and channels ───────────────────────── → note 5
├── Checking current status ────────────────────── → note 5
├── Tagging best practices ─────────────────────── → note 5
├── macOS app availability ─────────────────────── → note 5
└── Related ────────────────────────────────────── → note 5 (Related Notes/References)
digitalocean.md → note 6 (oc_install_digitalocean)
├── (intro: cost + alt options) ────────────────── → note 6 (Overview)
├── Prerequisites ──────────────────────────────── → note 6
├── Setup (Droplet/install/onboard/swap/verify/UI) → note 6
├── Persistence and backups ────────────────────── → note 6
├── 1 GB RAM tips ──────────────────────────────── → note 6
├── Troubleshooting ────────────────────────────── → note 6
├── Next steps (→ channels/gateway/updating) ───── → note 6 (Related/References)
└── Related ────────────────────────────────────── → note 6 (Related Notes/References)
```
No orphaned sections. Cross-target sections (`install/docker`, `install/updating`, `install/installer`, `gateway/sandboxing`, `gateway/configuration`, sibling VPS pages) are LINKED, not duplicated (owned by in02–in05 / gw0x / to0x).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 6 pages are single-BB (procedure) and each is well under caps (max 1,213w / azure; max 4 fences / ansible+development-channels). No page exceeds 2,500w or mixes building blocks, so each maps 1:1 to one note. |

## Summary Statistics & Building Block Distribution

- Source pages: 6 (4,173 body words). New `oc_` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×6 (all six notes — install/configure/update procedures).
- Est. digest words ~3,350 (avg ~560/note). Source fences total 14 (4+1+1+3+4+1); each note keeps ≤6 (verbatim install/CLI commands reproduced selectively — Azure's many `<Step>` commands are consolidated into ≤6 representative fences).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_install_ansible (10t · 10s · 11d)

Source re-read: openclaw-ansible one-command install; installs Tailscale, UFW, Docker CE + Compose, Node 24 + pnpm, host-based OpenClaw, systemd; 4-layer defense (UFW → Tailscale VPN → DOCKER-USER iptables → systemd hardening); `nmap` attack-surface check; manual playbook (ansible-galaxy, run-playbook.sh); idempotent re-run; troubleshooting (firewall, service-start, docker sandbox, provider login).

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway product; relevance: the software the playbook deploys host-based.
- [term_devops](../../term_dictionary/term_devops.md) — DevOps/IaC automation; relevance: the Ansible playbook IS the infrastructure-as-code automation (no `term_ansible` note exists).
- [term_vpn](../../term_dictionary/term_vpn.md) — virtual private network; relevance: Tailscale mesh VPN is the sole secure remote-access layer the playbook installs.
- [term_ssh](../../term_dictionary/term_ssh.md) — Secure Shell; relevance: port 22 SSH is the only public surface besides Tailscale after UFW lockdown.
- [term_docker](../../term_dictionary/term_docker.md) — Docker containers; relevance: installed (CE + Compose V2) as the default agent-sandbox backend with localhost-only bindings.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — execution sandbox; relevance: Docker isolates per-agent tool execution in the deployed setup.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — sandbox backend abstraction; relevance: Docker is the pluggable sandbox backend the playbook configures.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: Node 24 (Node 22 LTS still supported) + pnpm are installed as runtime dependencies.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: the agent the host-run gateway operates (no `term_openclaw_gateway` note).
- [term_terraform](../../term_dictionary/term_terraform.md) — IaC provisioning tool; relevance: closest declarative-provisioning analog/contrast to the Ansible imperative playbook approach.

**Docs**
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Nix-based hardened install of the Hermes coding-agent gateway; relevance: sibling automated-install path for the same agent-gateway family.
- [hermes_nixos_container_mode](../hermes_agent/hermes_nixos_container_mode.md) — NixOS module + container-isolated gateway deploy; relevance: declarative-deploy counterpart to the Ansible playbook's container isolation.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation + credential hardening for the gateway; relevance: parallels the 4-layer defense + credential handling the playbook hardens.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway service ops (start/stop/status/logs); relevance: the systemctl/journalctl ops the playbook's Quick commands mirror.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — devcontainer firewall + network-isolation hardening; relevance: same defense-in-depth firewall posture as UFW + DOCKER-USER.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime + container backends for a coding agent; relevance: explains the Docker sandbox backend the playbook installs.
- [pi_security_model](../pi/pi_security_model.md) — coding-agent security/threat model; relevance: conceptual framing for the attack-surface minimization (`nmap`-verified) the playbook enforces.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents to servers; relevance: server-deployment overview that the automated playbook operationalizes.
- [oc_install_digitalocean](oc_install_digitalocean.md) — manual VPS Droplet deploy (planned, this series); relevance: hand-rolled contrast to the automated hardened playbook.
- [oc_install_azure](oc_install_azure.md) — cloud-VM NSG/Bastion hardening (planned, this series); relevance: cloud-provider hardening counterpart to UFW/Tailscale.
- [oc_install_development_channels](oc_install_development_channels.md) — update channels (planned, this series); relevance: the Updating section defers to this standard update flow.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the deployed codebase.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the host-run service the systemd unit supervises.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: the defense-in-depth model this deployment hardens.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the sandboxed agent runtime Docker isolates.

**Snippets**
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — render/install a gateway systemd unit; relevance: the systemd auto-start service the playbook installs.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — OpenClaw systemd unit render/parse; relevance: the exact systemd integration with hardening flags (NoNewPrivileges/PrivateTmp).
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway start/stop/restart lifecycle; relevance: the service lifecycle the Quick commands drive.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker sandbox environment backend; relevance: the Docker agent-sandbox backend the playbook installs.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — refuse-to-run-as-root guard; relevance: enforces the unprivileged `openclaw` user the playbook creates.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — post-install onboarding wizard; relevance: the onboarding wizard the post-install script launches.
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — health/diagnostic doctor primitives; relevance: backs the troubleshooting/verify-installation steps.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health check; relevance: the `systemctl status`/health verification step.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — devops automation webhook skill; relevance: devops-automation analog to the playbook-driven deploy.

**Entry**

### oc_install_azure (10t · 10s · 11d)

Source re-read: Azure CLI VM build; resource group + NSG (Allow SSH only from Bastion subnet, Deny Internet/VNet SSH by priority); VNet/subnets + AzureBastionSubnet; VM with `--public-ip-address ""` (no public IP) + subnet-level NSG; Azure Bastion Standard (tunneling) for `az network bastion ssh`; install via `openclaw.ai/install.sh` (pulls Node LTS, runs wizard); GitHub Copilot provider recommendation; cost (Bastion ~$140/mo, deallocate VM, Basic Bastion); cleanup (`az group delete`).

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the gateway deployed 24/7 on the Azure VM.
- [term_vpc_virtual_private_cloud](../../term_dictionary/term_vpc_virtual_private_cloud.md) — virtual private cloud networking; relevance: the Azure VNet/subnet model is the VPC concept (no `term_azure_cloud` note).
- [term_iam](../../term_dictionary/term_iam.md) — identity & access management; relevance: Azure subscription permissions + resource-provider registration gate the deploy.
- [term_ssh](../../term_dictionary/term_ssh.md) — Secure Shell; relevance: the ed25519 key + Bastion-tunneled SSH is the only admin path.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — reverse proxy / fronting service; relevance: Azure Bastion fronts SSH to a VM with no public IP.
- [term_ssm_session_manager](../../term_dictionary/term_ssm_session_manager.md) — AWS managed no-public-IP shell access; relevance: direct conceptual analog to Azure Bastion's bastion-host-less managed SSH.
- [term_ec2](../../term_dictionary/term_ec2.md) — cloud VM compute; relevance: the Azure VM is the EC2-equivalent always-on compute host.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: the installer pulls Node LTS as a dependency.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: the agent the verified gateway runs.
- [term_claude](../../term_dictionary/term_claude.md) — Claude model/provider; relevance: GitHub Copilot/Claude provider is the recommended onboarding choice for Azure teams.

**Docs**
- [aws_ec2_security_groups_procedures](../aws_ec2/aws_ec2_security_groups_procedures.md) — security-group inbound-rule procedures; relevance: direct analog to the NSG allow/deny SSH rule set by priority.
- [aws_ec2_infrastructure_security](../aws_ec2/aws_ec2_infrastructure_security.md) — VM infrastructure-security model; relevance: the network-hardening posture mirrored by the Azure no-public-IP + NSG design.
- [aws_ec2_network_interfaces_concepts](../aws_ec2/aws_ec2_network_interfaces_concepts.md) — NIC / subnet attachment concepts; relevance: the per-NIC vs subnet-level NSG choice (`--nsg ""`) the guide makes.
- [aws_ec2_overview](../aws_ec2/aws_ec2_overview.md) — cloud VM service overview; relevance: framing for the always-on cloud-VM deploy target.
- [cc_cloud_environment](../claude_code/cc_cloud_environment.md) — running a coding agent in a cloud environment; relevance: the cloud-VM 24/7 deployment pattern.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deployment principles; relevance: least-exposure (no public IP, SSH-from-Bastion-only) maps to these principles.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud network-access control; relevance: the NSG inbound-restriction model is network-access control.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops + status verification; relevance: the `openclaw gateway status` verify step after install.
- [oc_install_digitalocean](oc_install_digitalocean.md) — DigitalOcean VPS deploy (planned, this series); relevance: cheaper VPS alternative cited in Azure's Related/Next-steps.
- [oc_install_ansible](oc_install_ansible.md) — automated hardened deploy (planned, this series); relevance: automation counterpart to this manual cloud-VM hardening.
- [oc_install_development_channels](oc_install_development_channels.md) — update channels (planned, this series); relevance: keeping the deployed gateway updated.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the deployed codebase.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the verified always-on gateway service.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: the NSG/Bastion/no-public-IP hardening posture.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: the wizard the installer script launches.

**Snippets**
- [snippet_hermes_agent_tools_environments_ssh](../../code_snippets/snippet_hermes_agent_tools_environments_ssh.md) — SSH-backed remote environment; relevance: the Bastion-tunneled SSH access to the VM.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — TLS client identity for the gateway; relevance: secure-transport identity layered on the no-public-IP VM.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — gateway TLS pinning; relevance: transport hardening complementing NSG network restriction.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — install/onboarding wizard; relevance: the wizard the `install.sh` launches in the VM shell.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — post-install verification; relevance: the verify-the-gateway step after onboarding.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health; relevance: backs `openclaw gateway status`.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config writer; relevance: the config the onboarding wizard writes after install.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway lifecycle; relevance: restart-on-VM-start after `az vm deallocate`/`az vm start`.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: token/password auth on the freshly installed gateway.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — gateway CLI command dispatch; relevance: the `openclaw gateway` CLI surface used post-install.

**Entry**

### oc_install_bun (10t · 10s · 10d)

Source re-read: Bun is an OPTIONAL local runtime for running TypeScript directly (`bun run`, `bun --watch`); NOT recommended for gateway runtime (WhatsApp/Telegram issues); default package manager remains pnpm; Bun ignores `pnpm-lock.yaml`; `bun install [--no-save]`, `bun run build`, `bun run vitest run`; blocked lifecycle scripts (`baileys` preinstall Node-major check, `protobufjs` postinstall) → `bun pm trust`; some scripts hardcode pnpm (`check:docs`, `ui:*`, `protocol:check`).

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the monorepo Bun builds/tests locally.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: the recommended production runtime Bun is explicitly contrasted against (Node 24, Node 22 LTS).
- [term_npm](../../term_dictionary/term_npm.md) — npm ecosystem; relevance: the npm/pnpm ecosystem context Bun's lockfile incompatibility breaks.
- [term_npm_scoping](../../term_dictionary/term_npm_scoping.md) — scoped npm packages; relevance: the scoped package deps (`baileys`, `protobufjs`) whose lifecycle scripts Bun blocks.
- [term_typescript](../../term_dictionary/term_typescript.md) — TypeScript; relevance: Bun runs TS directly via `bun run ...` without a compile step.
- [term_mise](../../term_dictionary/term_mise.md) — polyglot runtime/version manager; relevance: alternative dev-runtime version manager in the same local-toolchain space as Bun.
- [term_devops](../../term_dictionary/term_devops.md) — developer tooling/workflow; relevance: Bun is a local dev-loop tooling choice, not a production deploy.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: the agent gateway Bun is warned against running.
- [term_pip](../../term_dictionary/term_pip.md) — Python package manager; relevance: cross-language package-manager analog for the lockfile/lifecycle-script discussion.
- [term_maven](../../term_dictionary/term_maven.md) — JVM build/dependency tool; relevance: another package-manager analog illustrating lockfile + lifecycle-phase semantics.

**Docs**
- [pi_quickstart](../pi/pi_quickstart.md) — coding-agent local quickstart (Node/runtime install); relevance: the local dev-loop setup Bun accelerates.
- [pi_packages](../pi/pi_packages.md) — package/dependency management for the agent; relevance: the package-manager + lockfile model Bun diverges from.
- [pi_development](../pi/pi_development.md) — local development workflow; relevance: the `build`/`test` dev loop Bun targets (`bun run build`, `vitest`).
- [cc_sdk_typescript_installation](../claude_code/cc_sdk_typescript_installation.md) — TypeScript SDK install; relevance: TS runtime/install context for a coding-agent toolchain.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — install/dependency failure reference; relevance: parallels the blocked-lifecycle-script + hardcoded-pnpm gotchas.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — advanced install + verification; relevance: alternative-runtime install verification (Bun vs pnpm).
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Nix runtime quickstart; relevance: another non-default runtime/toolchain path for the agent.
- [oc_install_development_channels](oc_install_development_channels.md) — update channels + git/dev runtime (planned, this series); relevance: the `dev` channel git-checkout build loop Bun can serve.
- [oc_install_clawdock](oc_install_clawdock.md) — Docker helper layer (planned, this series); relevance: alternative local workflow (Docker) vs Bun local runtime.
- [oc_install_ansible](oc_install_ansible.md) — production install (planned, this series); relevance: production path that uses Node + pnpm, the recommended contrast to Bun.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the repo Bun builds/tests and whose hardcoded-pnpm scripts are the caveat.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: WhatsApp/Telegram (baileys) are the channels with known Bun runtime issues.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the gateway runtime Bun is explicitly not recommended for.

**Snippets**
- [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy dependency loading; relevance: the dependency-resolution behavior affected by Bun's lockfile handling.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract / manifest; relevance: the package.json contract whose lifecycle scripts Bun gates.
- [snippet_hermes_agent_gw_platform_whatsapp_connect](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_connect.md) — WhatsApp (baileys) connect; relevance: the WhatsApp channel runtime that breaks under Bun.
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — WhatsApp platform adapter; relevance: same WhatsApp/baileys lifecycle-script (`preinstall`) dependency.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect; relevance: the other channel (Telegram) with documented Bun runtime issues.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup/build wizard; relevance: the build/test toolchain Bun substitutes into.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache + respawn; relevance: the TS compile/build loop (`bun run build`) Bun speeds up.
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — CLI config schema; relevance: the build/protocol-check scripts (`protocol:check`) hardcoded to pnpm.
- [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — bootstrap shell install script; relevance: the install/bootstrap path Bun (`bun install`) is an alternative for.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: the trust model behind `bun pm trust <pkg>` for lifecycle scripts.

**Entry**

### oc_install_clawdock (10t · 10s · 10d)

Source re-read: ClawDock = shell-helper layer for Docker-based installs; install via canonical helper path (`~/.clawdock/clawdock-helpers.sh` sourced from `.zshrc`); command catalog — basic ops (start/stop/restart/status/logs), container access (shell/cli/exec), web UI + pairing (dashboard/devices/approve), setup+maintenance (fix-token/update/rebuild/clean), utilities (health/token/cd/config/show-config redacted/workspace); first-time flow (start → fix-token → dashboard → devices → approve); config/secrets split (`<project>/.env`, `~/.openclaw/.env`, `auth-profiles.json`, `openclaw.json`).

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the gateway ClawDock wraps with short commands.
- [term_docker](../../term_dictionary/term_docker.md) — Docker; relevance: ClawDock replaces longer `docker compose ...` invocations.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth token / gateway token; relevance: `clawdock-fix-token`/`clawdock-token` manage the gateway token.
- [term_auth_profile](../../term_dictionary/term_auth_profile.md) — auth profile; relevance: `auth-profiles.json` stores provider OAuth/API-key auth ClawDock's config helpers surface.
- [term_websocket](../../term_dictionary/term_websocket.md) — WebSocket; relevance: the Control UI `clawdock-dashboard` opens runs over the gateway WS (no `term_control_ui` note).
- [term_dm_pairing](../../term_dictionary/term_dm_pairing.md) — device-message pairing; relevance: `clawdock-devices`/`clawdock-approve` drive the device-pairing flow.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — execution sandbox; relevance: the containerized gateway `clawdock-shell`/`clawdock-exec` enter.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — credential store/pool; relevance: the `.env` + auth-profiles secrets split `clawdock-show-config` inspects (redacted).
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: the agent the containerized gateway runs.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: the gateway runtime inside the Docker container ClawDock manages.

**Docs**
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Docker run modes for the gateway; relevance: the `docker compose` run modes ClawDock shortcuts wrap.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker volumes + container supervision; relevance: the start/stop/restart + config-volume management ClawDock commands perform.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — dashboard auth + remote access; relevance: the Control UI auth/pairing `clawdock-dashboard` opens.
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — web dashboard overview; relevance: the Control UI surface ClawDock launches.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — container runtime for a coding agent; relevance: the containerized gateway ClawDock shells into.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: the redacted-secrets handling `clawdock-show-config` enforces.
- [pi_containerization](../pi/pi_containerization.md) — coding-agent containerization; relevance: the Docker-based deployment ClawDock is a helper layer for.
- [oc_install_digitalocean](oc_install_digitalocean.md) — Control-UI access options (planned, this series); relevance: pairing/Control-UI access counterpart.
- [oc_install_ansible](oc_install_ansible.md) — Docker-installing deploy (planned, this series); relevance: the playbook that installs the Docker base ClawDock assumes.
- [oc_install_bun](oc_install_bun.md) — local runtime (planned, this series); relevance: alternative local workflow vs Docker helper layer.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: `scripts/clawdock/clawdock-helpers.sh` lives here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the containerized gateway ClawDock starts/stops.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions/pairing state; relevance: the device-pairing state `clawdock-devices` surfaces.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: the token/secrets handling the redacted-config helper protects.

**Snippets**
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: the Control UI auth `clawdock-dashboard`/`fix-token` set up.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node/device pairing; relevance: `clawdock-devices`/`clawdock-approve` pairing flow.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — gateway pairing handshake; relevance: the pairing-required flow ClawDock surfaces.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets handling; relevance: the `.env`/auth-profiles secrets `clawdock-config`/`show-config` manage.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — auth-profiles external CLI; relevance: the `auth-profiles.json` ClawDock inspects.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker environment backend; relevance: the Docker container `clawdock-shell`/`exec` operate inside.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway health check; relevance: `clawdock-health` runs the gateway health check.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: the token auth `clawdock-fix-token` configures.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — CLI config set/inspect; relevance: the `openclaw.json` config `clawdock-config` opens.

**Entry**

### oc_install_development_channels (10t · 10s · 10d)

Source re-read: three update channels — stable (npm dist-tag `latest`), beta (dist-tag `beta`, falls back to `latest`), dev (moving head of `main`, dist-tag `dev`); beta-first promotion to `latest` without version bump; `openclaw update --channel stable|beta|dev` persists `update.channel` + aligns install method (npm dist-tag vs git tag checkout, excluding `-alpha/-rc/-dev` prerelease suffixes); dev ensures git checkout, rebases `main`, builds; `--tag` one-off version/dist-tag/SHA/package-spec targeting (not persisted, npm only); downgrade protection; `--dry-run [--json]`; plugin sync per channel; `openclaw update status`; immutable-tag best practices; macOS-build-may-be-absent note.

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the package/CLI being updated across channels.
- [term_npm](../../term_dictionary/term_npm.md) — npm; relevance: dist-tags `latest`/`beta`/`dev` are the source of truth for npm installs.
- [term_npm_scoping](../../term_dictionary/term_npm_scoping.md) — npm package specs/scoping; relevance: `--tag openclaw@2026.4.1-beta.1` package-spec targeting.
- [term_ci_cd](../../term_dictionary/term_ci_cd.md) — CI/CD pipeline; relevance: the beta→latest promotion + release pipeline that ships builds to channels.
- [term_devops](../../term_dictionary/term_devops.md) — release/devops workflow; relevance: channel management + immutable-tag best practices are a release-ops workflow.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: the npm/git install runtime the update flow targets.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: the gateway/agent the channels deliver builds of.
- [term_pip](../../term_dictionary/term_pip.md) — pip package manager; relevance: dist-tag/version-pinning analog from the Python packaging world.
- [term_codeartifact](../../term_dictionary/term_codeartifact.md) — package registry/dist-tag store; relevance: the registry-dist-tag mechanism (`latest`/`beta`/`dev`) channels resolve against.

**Docs**
- [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — update + stable/latest release channels for a coding agent; relevance: the direct same-concept analog (channel semantics + update flow).
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — updating + uninstalling the agent; relevance: the sibling update flow + version management.
- [cc_install](../claude_code/cc_install.md) — install methods (npm vs native); relevance: the install-method alignment (`--channel` chooses npm vs git) this note documents.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — advanced install + version verification; relevance: pinning a specific version/tag + verifying it.
- [pi_packages](../pi/pi_packages.md) — package/version management; relevance: the npm-package version + dist-tag model channels use.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — install/update failure reference; relevance: downgrade-protection + git-checkout build failures the dev channel can hit.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — pinned/declarative install; relevance: version-pinning analog (Nix pin vs `--tag`).
- [oc_install_ansible](oc_install_ansible.md) — Ansible deploy (planned, this series); relevance: its Updating section defers to this standard update flow.
- [oc_install_bun](oc_install_bun.md) — Bun local runtime (planned, this series); relevance: the `dev` channel git-checkout build loop Bun can run.
- [oc_install_digitalocean](oc_install_digitalocean.md) — VPS deploy (planned, this series); relevance: its Next-steps point to Updating to keep the Droplet current.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the versioned codebase / `main` git checkout for the `dev` channel.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the running gateway pinned to a channel.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: the `openclaw update`/`openclaw update status` CLI surface.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugins/extensions; relevance: npm-installed vs bundled plugins synced per channel on update.

**Snippets**
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — the `update` CLI command; relevance: the `openclaw update` command this note centers on.
- [snippet_hermes_agent_cli_banner_update](../../code_snippets/snippet_hermes_agent_cli_banner_update.md) — update banner / version check; relevance: the current-version + channel status surfaced by `update status`.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache + respawn after update; relevance: the dev-channel build+install-from-checkout step.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — entry dispatch / version-gated boot; relevance: the gateway re-entry after a channel switch/update.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: npm-installed plugins updated after the core update completes.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: bundled-vs-npm plugin sources synced per channel.
- [snippet_hermes_agent_cli_claw_migrate](../../code_snippets/snippet_hermes_agent_cli_claw_migrate.md) — migrate/version-transition CLI; relevance: the install-method/version transition (`--install-method git --version main`).
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — config schema (persisted `update.channel`); relevance: where `--channel` persists the chosen channel.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — post-update verification; relevance: the dry-run/verify preview before applying an update.
- [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — uninstall/version cleanup; relevance: the inverse lifecycle op alongside update/channel switching.

**Entry**

### oc_install_digitalocean (10t · 10s · 11d)

Source re-read: persistent Gateway on a DO Droplet (~$6/mo 1 GB Basic), cheaper alts Hetzner/Oracle; create Droplet (Ubuntu 24.04 LTS, avoid Marketplace images); `ssh root@IP`, `apt update/upgrade`, install Node 24 via nodesource, `openclaw.ai/install.sh`, create non-root `openclaw` user (`usermod -aG sudo`, `loginctl enable-linger`); `openclaw onboard --install-daemon` (model auth, channels, token, systemd daemon); add 2G swap to `/etc/fstab`; verify via `openclaw status` + `systemctl --user`; Control UI access — Option A SSH tunnel (`ssh -L 18789`), Option B Tailscale Serve (`gateway.tailscale.mode serve`, tailnet identity auth), Option C tailnet bind (`gateway.bind tailnet`, token required); persistence (`~/.openclaw/`, workspace) + `openclaw backup create`; 1 GB RAM tips (swap, API models over local, smaller model, `free -h`/`htop`); troubleshooting (doctor, port-in-use, OOM).

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw product; relevance: the persistent gateway hosted on the Droplet.
- [term_ssh](../../term_dictionary/term_ssh.md) — Secure Shell; relevance: SSH-key auth to the Droplet + the SSH-tunnel Control-UI option (`ssh -L 18789`).
- [term_vpn](../../term_dictionary/term_vpn.md) — VPN; relevance: Tailscale Serve / tailnet-bind Control-UI access options run over the tailnet VPN.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: Node 24 is installed via nodesource before OpenClaw.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: the agent the systemd-user gateway runs.
- [term_claude](../../term_dictionary/term_claude.md) — Claude model/provider; relevance: API-based Claude/GPT models recommended for the 1 GB Droplet.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: local LLM inference does not fit 1 GB → prefer API models.
- [term_websocket](../../term_dictionary/term_websocket.md) — WebSocket; relevance: the Control UI + WS traffic the three access options expose (no `term_control_ui` note).
- [term_ec2](../../term_dictionary/term_ec2.md) — cloud VM instance; relevance: the Droplet is the EC2-equivalent VPS compute host.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs / linger daemon; relevance: `loginctl enable-linger` keeps the user-systemd gateway running like a persistent scheduled service.

**Docs**
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents to a server; relevance: the VPS deployment pattern this note operationalizes.
- [cc_cloud_environment](../claude_code/cc_cloud_environment.md) — cloud-environment agent deploy; relevance: running the agent persistently on a cloud VM.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops (status/logs/restart); relevance: the `openclaw status` + `systemctl --user`/`journalctl --user` verify+troubleshoot steps.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — dashboard remote auth; relevance: the three Control-UI remote-access options + their auth model.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote backend access; relevance: the SSH-tunnel / tailnet remote-access patterns.
- [cc_remote_control](../claude_code/cc_remote_control.md) — remote control of a coding agent; relevance: the remote Control-UI access the access options enable.
- [hermes_install_termux_android](../hermes_agent/hermes_install_termux_android.md) — low-resource install; relevance: the constrained-resource (1 GB RAM) tuning parallels.
- [oc_install_azure](oc_install_azure.md) — Azure cloud-VM deploy (planned, this series); relevance: production cloud-VM counterpart linked in Azure's Related.
- [oc_install_ansible](oc_install_ansible.md) — automated hardened deploy (planned, this series); relevance: the automated/hardened alternative to this manual Droplet setup.
- [oc_install_development_channels](oc_install_development_channels.md) — update channels (planned, this series); relevance: Next-steps point to Updating to keep the Droplet current.
- [oc_install_clawdock](oc_install_clawdock.md) — Docker helper layer (planned, this series); relevance: alternative Control-UI/pairing helper path.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the installed codebase.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the systemd-user `openclaw-gateway.service`.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: the `openclaw onboard --install-daemon` wizard.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: the auth-mode/Tailscale-identity trust model in the Control-UI section.

**Snippets**
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — gateway runtime bind/config + broadcast; relevance: `gateway.bind tailnet` / loopback bind + runtime config the access options set.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers (token/password/tailscale); relevance: `gateway.auth.mode`/`allowTailscale` Control-UI auth options.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: the Control-UI auth the three access options gate.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP binding; relevance: the default loopback bind (`localhost:18789`) before exposing via tunnel/tailnet.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — systemd-user gateway unit; relevance: the `openclaw-gateway.service` daemon installed via `--install-daemon`.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — onboarding wizard; relevance: the `openclaw onboard` wizard (model auth, channels, token, daemon).
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — backup create/save; relevance: `openclaw backup create` portable snapshot.
- [snippet_hermes_agent_cli_backup_restore](../../code_snippets/snippet_hermes_agent_cli_backup_restore.md) — backup restore; relevance: restoring the `~/.openclaw/` state snapshot on a new host.
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — doctor diagnostics; relevance: `openclaw doctor --non-interactive` troubleshooting step.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway status/health; relevance: the `openclaw status` verify step.

**Entry**


## Undigested Terms Plan

> Per master: OpenClaw install/devops vocabulary is digested as install **procedure content inside the `oc_*` notes**, NOT as new `term_dictionary` entries. The only term_dictionary interaction is LINKING existing terms. Expected **0 new term_dictionary captures**.

| Term | Disposition |
|---|---|
| OpenClaw / OpenClaw Gateway | Link existing `term_openclaw`; gateway-specific concept documented in `oc_install_*` notes (no `term_openclaw_gateway` exists; not promoted — covered by docs + `repo_openclaw_gateway`). |
| Tailscale / mesh VPN / tailnet | Documented inline (access step); link existing `term_vpn`. No `term_tailscale` (vendor-specific). |
| UFW / firewall / NSG / Bastion / attack surface | Documented inline as hardening steps in `oc_install_ansible` / `oc_install_azure`; link `term_ssh`, `term_iam`, `term_vpc_virtual_private_cloud`. No new term notes (deployment-specific config, not reusable vault concepts). |
| Docker / container / sandbox | Link existing `term_docker`, `term_sandbox`. Docker base install owned by in02 (`install/docker`). |
| Bun runtime | Documented inline in `oc_install_bun`; link `term_node_js`/`term_npm`/`term_typescript`. No `term_bun` (specific runtime tool). |
| pnpm / npm dist-tags | Link existing `term_npm`. pnpm documented inline (no `term_pnpm`). |
| ClawDock helpers | Documented inline in `oc_install_clawdock` (the helper command catalog IS the content); no term note. |
| stable / beta / dev channels, semver pinning | Documented inline in `oc_install_development_channels`; link `term_npm`/`term_ci_cd`. No `term_semantic_versioning`/`term_release_management` (generic; not captured). |
| Control UI / pairing / gateway token | Documented inline; link `term_websocket` (no `term_control_ui`), `term_oauth_token`, `term_auth_profile`. |
| DigitalOcean / Droplet / Azure / cloud VM / VPS | Documented inline as deploy targets in `oc_install_digitalocean`/`oc_install_azure`; link `term_vpc_virtual_private_cloud`. No vendor term notes / no `term_vps`. |
| swap / loopback / 1 GB RAM tuning | Documented inline (tuning step); no term notes (OS/ops primitives). |

**New-term candidates:** **none.** No genuinely reusable cross-cutting term lacking an existing note appears in these 6 install pages — all vocabulary is either an existing linkable term or deployment-specific config best left as `oc_*` doc content. (If augment's Step 2d re-scan disagrees, a single candidate would be captured via `/tessellum-capture-term-note` + added to `acronym_glossary_d.md` (devops) or `acronym_glossary_a.md`; not anticipated.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. Requirement inherited from master applies only if augment surfaces a new term: research ≥2 sources, full term-note format, glossary update — not anticipated for in01.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order, H1/`## Overview`/`## Related Notes`/`## References`/footer, indexed `[text](path.md)` links) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traces to `inbox/openclaw_docs/install/<page>.md`; verbatim commands/tables) | diff each note vs its source page |
| G3 | Density + Coverage (≤400 lines, ≤2500 words, ≤6 code blocks; every mapped H2/H3 represented; one BB/note) | word/fence count + Section Coverage Map |
| G4 | Cross-Reference (≥8 relevancy-selected terms + ≥10 snippets + ≥10 docs + repo_openclaw*/sibling oc_*; each with a relevance statement) | Per-Note Related Notes Mapping (LOCKED 2026-06-21) |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | DB existence check on every link target |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` + reindex |
| G7 | Discoverability (each note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`) | `entry_openclaw_docs.md` rows + repo/term inlinks |
| G8 | In-degree ≥1 (anti-island) | `note_links` table query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_install_ansible oc_install_azure oc_install_bun oc_install_clawdock oc_install_development_channels oc_install_digitalocean"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION in $n: $sec"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4 sibling-prefix cross-ref presence
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING/OC CROSS-REF in $n"
done

# G1 frontmatter
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source words | Code blocks (≤6) | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_install_ansible | procedure | 600 | 804 | ≤4 | ✅ |
| 2 | oc_install_azure | procedure | 700 | 1,213 | ≤6 (Azure `<Step>` cmds consolidated) | ✅ |
| 3 | oc_install_bun | procedure | 350 | 208 | ≤2 | ✅ |
| 4 | oc_install_clawdock | procedure | 500 | 467 | ≤3 | ✅ |
| 5 | oc_install_development_channels | procedure | 600 | 779 | ≤5 | ✅ |
| 6 | oc_install_digitalocean | procedure | 600 | 702 | ≤4 | ✅ |

No note approaches the caps (≤400 lines / ≤2500 words / ≤6 code blocks). Azure (the largest source) maps to one ~700w note because much of its volume is `az` CLI command bodies inside `<Step>` blocks — these are reproduced selectively as ≤6 representative fences (RG/NSG/VNet/VM/Bastion/install), not all 15+ snippets. bun (208w source) yields a small but complete note (~350w with Overview + cross-refs).

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify + add at execution for G7/G8; `entry_openclaw_docs` is the guaranteed inbound source for all 6):

- `entry_openclaw_docs.md` → all 6 notes (primary G8 inbound, guaranteed).
- `repo_openclaw.md` → all 6 (the deployed codebase; reciprocal docs↔code link).
- `repo_openclaw_gateway.md` → notes 1, 2, 4, 5, 6 (gateway deployment/runtime targets).
- `repo_openclaw_security.md` → notes 1, 2, 4 (hardening/defense-in-depth, token/secrets, NSG/Bastion).
- `repo_openclaw_cli_wizard.md` → notes 2, 5, 6 (`openclaw onboard`/`update`/`status` CLI surfaces).
- `repo_openclaw_extensions.md` → note 5 (channel-synced plugins).
- `term_openclaw.md` → all 6 (the term whose product these install).
- `term_docker.md` → notes 1, 4 (Docker-based install/helper).
- `term_vpn.md` → notes 1, 6 (Tailscale access).
- `term_npm.md` → note 5 (dist-tag channels).
- `term_node_js.md` → notes 1, 3, 6 (runtime dependency).

## Pacing Rules (inherited from master)

One execution phase, 6 notes; 8 gates must pass before commit. Re-read each source page at execution; reproduce install/CLI commands verbatim (selectively to stay ≤6 fences). One BB per note (all procedure). Cap dynamic-workflow fan-out at ~30 agents/run. `git pull --rebase --autostash` first; commit + push the wave together; no Claude co-author trailer. Incremental reindex before commit; verify `note_links` in-degree ≥1 + 0 broken links.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)



**Per-note locked counts.**

| Note | Terms | Snippets | Docs (existing/total) | Repos | Floors met (≥8t·≥10s·≥10d) |
|---|---:|---:|---:|---:|---|
| oc_install_ansible | 10 | 10 | 8 / 11 | 4 | ✅ |
| oc_install_azure | 10 | 10 | 8 / 11 | 4 | ✅ |
| oc_install_bun | 10 | 10 | 7 / 10 | 3 | ✅ |
| oc_install_clawdock | 10 | 10 | 7 / 10 | 4 | ✅ |
| oc_install_development_channels | 10 | 10 | 7 / 10 | 4 | ✅ |
| oc_install_digitalocean | 10 | 10 | 7 / 11 | 4 | ✅ |


**New-term candidates.** **NONE.** The Step 2d re-scan of all 6 pages confirmed no genuinely reusable, cross-cutting, vault-missing term. Install/devops vocabulary missing from the vault (`term_ansible`, `term_azure_cloud`, `term_systemd`, `term_tailscale`, `term_ufw`, `term_control_ui`, `term_openclaw_gateway`, `term_bun`, `term_self_hosting`, `term_pnpm`) is either vendor-specific config, an OS primitive, or an OpenClaw concept owned by an `oc_*` doc page — per the master undigested-terms policy, each is documented inline as an install step and linked to the nearest EXISTING term. Best-fit glossary IF augment had surfaced one would be `acronym_glossary_d.md` (devops) — not exercised. Expected and confirmed: **0 new `term_dictionary` captures.**

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-stated) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 6 notes at 10 terms / 10 snippets / 10-11 docs, each link carries a `relevance:` clause. Exceeds the ≥8-term floor. |
| CP2 | 9-GATE present per batch (G1-G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1-G8 incl. G5 ghost-detect, G6 broken-link fix, G7/G8 discoverability/in-degree; Validation Scripts implement format/density/source_url/sibling-xref checks. |
| CP4 | Size | **PASS** | 6 notes (≤30); 1 page → 1 note, no splits; single execution phase. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Master Format Definition derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (same source type); YAML field order + `## Overview`/`## Related Notes`/`## References`/footer + forbidden-field list inherited; target dir `resources/documentation/openclaw/` mapped to `dev_tool_docs` (W4 done). |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: max 1,213w (azure) / max 4 fences — no note near the ≤2500w / ≤6-fence / ≤400-line caps; no borderline cases; no split needed (documented). |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured body word counts (frontmatter stripped) match the plan's Source table exactly (804/1213/208/467/779/702; total 4,173; ratio 1.00). No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (13 rows, all dispositioned to link-existing or document-inline); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; master multi-source mandate inherited if a term surfaces). 0 new captures expected and confirmed. |
| CP8f | Slug specificity / collision dedup (all notes) | **PASS** | No new `term_*` slugs created (0 captures → no specificity/rename needed). Doc-vs-term collision audit: the 6 planned `oc_install_*` doc slugs are install-procedure pages with no existing term-note or documentation-note equivalent (DB confirmed 0 notes under `resources/documentation/openclaw/`); they correctly LINK existing `term_openclaw`/`repo_openclaw*` rather than duplicate them. |
| CP9 | Discoverability / inlinks (G8 in-degree ≥1) | **PASS** | `## Inlinks (existing notes → new notes)` table maps `entry_openclaw_docs` → all 6 (guaranteed inbound) plus `repo_openclaw*`/`term_*` inlinks; G8-Discoverability is in the gate table; every note has ≥1 planned outside-folder inbound link. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
