---
title: Sub-Plan in02 — OpenClaw Docs: Install (Docker, Docker VM Runtime, exe.dev, Fly.io, GCP, Hetzner)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["install/docker", "install/docker-vm-runtime", "install/exe-dev", "install/fly", "install/gcp", "install/hetzner"]
---

# Sub-Plan in02: Install

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References` → bold footer; ≤400L/≤2500w/≤6 code, one BB per note), dedup-before-create (term_dictionary AND documentation/ AND repo_openclaw*), 9-GATE validation, cross-refs, entry-point (`entry_openclaw_docs.md`), and Undigested-Terms policy are ALL inherited from the master.

## Scope

The six **container / cloud-VM deployment** install guides: the generic containerized-gateway flow
(`install/docker`), the shared VM-Docker runtime steps (`install/docker-vm-runtime`), and four
provider-specific always-on Gateway deployments — exe.dev (`install/exe-dev`), Fly.io (`install/fly`),
GCP Compute Engine (`install/gcp`), and Hetzner VPS (`install/hetzner`). These are the "run OpenClaw 24/7 on
a server" half of the Install section (in01 covers the local/package installers: ansible, azure, bun,
clawdock, development-channels, digitalocean). **P1 (Phase A)** — operational core: the deployment
substrate every gateway/channel/provider doc assumes exists. The code-side counterparts `repo_openclaw`,
`repo_openclaw_gateway`, `repo_openclaw_security` are **LINKED, not recreated**.

**Source**: OpenClaw docs, 6 pages, 8,627 measured words. **Planned: 7 notes** (docker.md splits 1→2; all
others 1 note each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| docker | /install/docker | 2,871 | 23 | 6 | 11 | procedure + concept (split: containerized gateway vs agent sandbox) |
| docker-vm-runtime | /install/docker-vm-runtime | 681 | 7 | 5 | 0 | procedure |
| exe-dev | /install/exe-dev | 808 | 11 | 13 | 0 | procedure |
| fly | /install/fly | 1,838 | 27 | 9 | 13 | procedure |
| gcp | /install/gcp | 1,423 | 22 | 7 | 0 | procedure |
| hetzner | /install/hetzner | 1,006 | 10 | 7 | 0 | procedure |

(Totals: 8,627 words; 100 source code fences. H2/H3 counts are exact `grep '^## '` / `grep '^### '` from
the mirror; `<Steps>/<Step>` MDX blocks inside docker/fly are nested ordered steps, not extra H2s.)

## Content Strategy

- **Prioritize**: the generic **containerized-gateway procedure** (`docker.md` Containerized gateway →
  build image, airgapped/offline rerun, onboarding, env vars, observability, health checks, LAN/loopback,
  host-local providers, Bonjour/mDNS, storage/persistence, shell helpers) — every VM guide (gcp, hetzner,
  docker-vm-runtime) reuses it. Second priority: the **VM-Docker runtime contract** (`docker-vm-runtime.md`:
  bake binaries at build time, persist `~/.openclaw`, update flow) shared verbatim by gcp/hetzner.
- **Split**: `docker.md` (2,871w > 2,500w cap, mixed BB) → (a) the containerized-gateway **procedure** note +
  (b) the **agent-sandbox** Docker-backend **concept** note (when/how the Docker sandbox backend isolates
  tool execution). The four provider guides (exe-dev, fly, gcp, hetzner) are each <2,500w, single-procedure
  BB, and stay as **1 note each** (their Troubleshooting/Private-deployment/Cost/Service-account H3s are
  sub-aspects of the one deploy procedure, not a second BB).
- **Skip / link-out**: deep sandbox config → link `/gateway/sandboxing`, `repo_openclaw_security`,
  `snippet_openclaw_security_openshell_*` (not redefined here); gateway config-after-install → link
  `/gateway/configuration` + future `gw*` notes; generic Docker concepts → link `term_docker`; updating →
  link `/install/updating` (in05). Provider names (Fly.io, GCP, Hetzner, exe.dev) documented as deploy
  targets, NOT promoted to term notes.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_install_docker_containerized_gateway.md` | procedure | docker.md: Is Docker right for me?, Prerequisites, Containerized gateway (Build image / Airgapped rerun / Onboarding / Manual flow), Environment variables, Observability, Health checks, LAN vs loopback, Host Local Providers, Bonjour/mDNS, Storage and persistence, Shell helpers, Running on a VPS?, Troubleshooting | 700 | Running the OpenClaw Gateway as a Docker container: choose-or-skip Docker, prerequisites, build/pre-built/airgapped image, onboarding, env vars, observability + health checks, LAN-vs-loopback exposure, host-local providers, Bonjour/mDNS, persistent storage, shell helpers, and troubleshooting. |
| 2 | `oc_install_docker_agent_sandbox.md` | concept | docker.md: Agent sandbox (scope/workspace/policy), Quick enable | 350 | The Docker-backend agent sandbox: how `agents.defaults.sandbox` runs agent tool execution in isolated Docker containers (per-agent/session/shared scope, `/workspace` mount, tool policy, network/resource limits) while the gateway stays on the host; quick-enable config. |
| 3 | `oc_install_docker_vm_runtime.md` | procedure | docker-vm-runtime.md: Bake required binaries into the image, Build and launch, What persists where, Updates | 450 | Shared Docker-on-VM runtime contract reused by GCP/Hetzner/VPS installs: bake all external skill binaries at image-build time (never at runtime), build and launch, what persists where (`~/.openclaw` host mount), and the update flow. |
| 4 | `oc_install_exe_dev.md` | procedure | exe-dev.md: Beginner quick path, What you need, Automated install with Shelley, Manual installation (1 Create VM → 5 Access + grant privileges), Remote channel setup, Remote access, Updating | 500 | Deploying the OpenClaw Gateway on an exe.dev VM reachable at `https://<vm-name>.exe.xyz`: Shelley automated install, manual VM-create + prerequisites + nginx HTTPS proxy (port 18789), device pairing, remote channel setup, and updating. |
| 5 | `oc_install_fly.md` | procedure | fly.md: What you need, Beginner quick path (fly.toml / volumes / secrets / first-run config), Troubleshooting, Updates, Private deployment (hardened), Notes, Cost, Next steps | 700 | Deploying OpenClaw on Fly.io with persistent volumes, secrets, and automatic HTTPS: `fly.toml` setup, beginner quick path, troubleshooting (listen address, health checks, OOM, gateway lock, config-read, SSH config writes, state persistence), updates, hardened private deployment, and cost. |
| 6 | `oc_install_gcp.md` | procedure | gcp.md: What are we doing?, Quick path, What you need, (VM create → Docker → persistence → .env/compose → bake/build/launch → SSH tunnel), Troubleshooting, Service accounts (security best practice), Next steps | 650 | Running a 24/7 OpenClaw Gateway on a GCP Compute Engine VM (Docker): project/billing, Compute Engine VM, Docker install, persistent `~/.openclaw` host mounts, `.env` + `docker-compose.yml`, baked binaries, SSH-tunnel Control UI access, troubleshooting, and service-account least-privilege setup. |
| 7 | `oc_install_hetzner.md` | procedure | hetzner.md: Goal, What are we doing?, Quick path, What you need, (provision → Docker → persistence → compose → bake → up → verify), Infrastructure as Code (Terraform), Next steps | 550 | Running a 24/7 OpenClaw Gateway on a cheap Hetzner VPS (Docker): security/trust-boundary model, provision VPS, Docker install, persistent `~/.openclaw` host mounts, `.env` + `docker-compose.yml`, baked binaries, `docker compose up -d`, verification, and Terraform Infrastructure-as-Code. |

## Section Coverage Map

```
docker.md (2,871w → SPLIT notes 1 + 2)
├── Is Docker right for me? ──────────────────────── → note 1 (oc_install_docker_containerized_gateway)
├── Prerequisites ────────────────────────────────── → note 1
├── Containerized gateway ────────────────────────── → note 1
│   ├── (Step: Build image / Airgapped rerun / Onboarding) → note 1
│   ├── ### Manual flow ───────────────────────────── → note 1
│   ├── ### Environment variables ─────────────────── → note 1
│   ├── ### Observability ─────────────────────────── → note 1
│   ├── ### Health checks ─────────────────────────── → note 1
│   ├── ### LAN vs loopback ───────────────────────── → note 1
│   ├── ### Host Local Providers ──────────────────── → note 1
│   ├── ### Bonjour / mDNS ────────────────────────── → note 1
│   ├── ### Storage and persistence ──────────────── → note 1
│   ├── ### Shell helpers (optional) ──────────────── → note 1
│   └── ### Running on a VPS? ─────────────────────── → note 1
├── Agent sandbox ────────────────────────────────── → note 2 (oc_install_docker_agent_sandbox)
│   └── ### Quick enable ──────────────────────────── → note 2
├── Troubleshooting ──────────────────────────────── → note 1
└── Related ──────────────────────────────────────── → Related Notes / References (notes 1 + 2)
docker-vm-runtime.md (681w → note 3)
├── Bake required binaries into the image ─────────── → note 3 (oc_install_docker_vm_runtime)
├── Build and launch ─────────────────────────────── → note 3
├── What persists where ──────────────────────────── → note 3
├── Updates ──────────────────────────────────────── → note 3
└── Related ──────────────────────────────────────── → Related Notes / References
exe-dev.md (808w → note 4)
├── Beginner quick path ──────────────────────────── → note 4 (oc_install_exe_dev)
├── What you need ────────────────────────────────── → note 4
├── Automated install with Shelley ───────────────── → note 4
├── Manual installation (1 Create VM … 5 Access/privileges) → note 4
├── Remote channel setup ─────────────────────────── → note 4
├── Remote access ────────────────────────────────── → note 4
├── Updating ─────────────────────────────────────── → note 4
└── Related ──────────────────────────────────────── → Related Notes / References
fly.md (1,838w → note 5)
├── What you need ────────────────────────────────── → note 5 (oc_install_fly)
├── Beginner quick path ──────────────────────────── → note 5
├── Troubleshooting (### listen addr / health / OOM / lock / config / SSH writes / state) → note 5
├── Updates (### Updating machine command) ────────── → note 5
├── Private deployment (### when / setup / accessing / webhooks / security benefits) → note 5
├── Notes / Cost / Next steps ────────────────────── → note 5
└── Related ──────────────────────────────────────── → Related Notes / References
gcp.md (1,423w → note 6)
├── What are we doing (simple terms)? ────────────── → note 6 (oc_install_gcp)
├── Quick path (experienced operators) ───────────── → note 6
├── What you need (+ inline VM-create … launch steps) → note 6
├── Troubleshooting ──────────────────────────────── → note 6
├── Service accounts (security best practice) ─────── → note 6
├── Next steps ───────────────────────────────────── → note 6
└── Related ──────────────────────────────────────── → Related Notes / References
hetzner.md (1,006w → note 7)
├── Goal ─────────────────────────────────────────── → note 7 (oc_install_hetzner)
├── What are we doing (simple terms)? ────────────── → note 7
├── Quick path (experienced operators) ───────────── → note 7
├── What you need (+ inline provision … verify steps) → note 7
├── Infrastructure as Code (Terraform) ───────────── → note 7
├── Next steps ───────────────────────────────────── → note 7
└── Related ──────────────────────────────────────── → Related Notes / References
```
No orphaned sections. Sandbox deep-config → `/gateway/sandboxing` + `repo_openclaw_security` (link-out);
post-install gateway config → `/gateway/configuration` (link-out); updating → `/install/updating` (in05).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| docker.md (2,871w, 6 H2 / 11 H3, 23 code) | notes 1 + 2 | Exceeds the 2,500-word cap AND mixes two building blocks: the containerized-gateway deploy **procedure** (build/run/configure the gateway container) vs the agent-**sandbox** **concept** (the Docker backend that isolates *agent tool execution*, a distinct architectural feature gated by `agents.defaults.sandbox`, not a deploy step). Split per word-cap + one-BB rule; keeps each ≤6 code blocks and one BB. |
| docker-vm-runtime.md (681w) | note 3 | (no split) single shared-runtime procedure; small + focused. |
| exe-dev.md (808w) | note 4 | (no split) single deploy procedure; 13 H2s are short numbered manual-install steps, not separate BBs. |
| fly.md (1,838w) | note 5 | (no split) <2,500w, single deploy procedure; Troubleshooting/Private-deployment/Cost are sub-aspects of the one Fly.io deploy task. 27 source fences reproduced selectively to stay ≤6. |
| gcp.md (1,423w) | note 6 | (no split) <2,500w, single deploy procedure; Service-accounts is a security sub-step of the deploy. |
| hetzner.md (1,006w) | note 7 | (no split) <2,500w, single deploy procedure; Terraform IaC is an alternate-provisioning sub-aspect of the same deploy. |

## Summary Statistics & Building Block Distribution

- Source pages: **6** (8,627 words, 100 source code fences). New `oc_` notes: **7**. New `term_dictionary`
  notes: **0**.
- BB distribution: **procedure ×6** (notes 1, 3, 4, 5, 6, 7) · **concept ×1** (note 2, agent sandbox).
- Est. digest words ~3,900 (avg ~557/note; range 350–700). The 100 source fences distribute across the 7
  notes; each note keeps **≤6 code blocks** (config/CLI snippets reproduced selectively + verbatim; the
  docker/fly/gcp pages' many short fences are summarized to representative blocks with link-outs to the
  source page for the full sequence).
- Cross-refs **LOCKED at augment (xref-augment 2026-06-21)** — see `## Per-Note Related Notes Mapping`:
  relevant `repo_openclaw*` + sibling `oc_*`. Per-note counts: note1 8t/11s/11d · note2 8t/11s/11d · note3
  8t/10s/10d · note4 8t/10s/10d · note5 8t/11s/10d · note6 8t/11s/10d · note7 8t/11s/10d. Snippets are ALL
  aws_ec2/aws_cdk/aws_cloudformation/aws_bedrock_agentcore corpora). Sibling `oc_*` docs are "(planned, this
  series)". Note count locks at 7 here (master estimated 10 for in02; actual measured split count is 7).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> (plus relevant `repo_openclaw*` + sibling `oc_*` as additional). RELEVANCE is the selection criterion
> `claude_code/cc_*`, `hermes_agent/hermes_*`, `pi/pi_*`, `aws_ec2/`, `aws_cdk/`, `aws_cloudformation/`,
> `aws_bedrock_agentcore/` coding-agent + cloud-deploy corpora). Relative paths FROM a note at
> `resources/documentation/openclaw/oc_X.md`: term `../../term_dictionary/term_Y.md`; sibling oc `oc_Y.md`;
> other doc `../<folder>/<file>.md`; repo `../../../areas/code_repos/repo_Y.md`; snippet
> `../../code_snippets/snippet_Y.md`; analysis `../../analysis_thoughts/<file>.md`; entry point
> `../../../0_entry_points/entry_openclaw_docs.md`. Render each link in the note's `## Related Notes` as:
> `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_install_docker_containerized_gateway (8t · 11s · 11d)

**Terms**
- [Docker](../../term_dictionary/term_docker.md) — OS-level container runtime/engine; relevance: the gateway image this whole note builds, runs, and persists via `scripts/docker/setup.sh` + Compose.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to AI coding agents; relevance: the product being containerized here.
- [DevOps](../../term_dictionary/term_devops.md) — build/release/run/operate practices; relevance: the `.env` sync → image build → Compose up → onboarding ops loop this note codifies.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probing; relevance: the `/healthz`/`/readyz` probes + built-in Docker `HEALTHCHECK` this note configures.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server fronting an upstream service; relevance: LAN-vs-loopback exposure + the "Running on a VPS?" proxy-fronting pattern.
- [nginx](../../term_dictionary/term_nginx.md) — HTTP server/reverse proxy; relevance: the proxy in front of the published gateway port on a VPS host.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating multi-container/service startup; relevance: Docker Compose multi-container (gateway + cli sidecar) start/restart this note drives.
- [Observability of Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — telemetry for agent runtimes; relevance: the OpenTelemetry/OTLP + Prometheus metrics export this note's Observability section sets up.

**Docs**
- [oc_install_docker_agent_sandbox](oc_install_docker_agent_sandbox.md) — the Docker-backend agent sandbox concept (planned, this series); relevance: the `OPENCLAW_SANDBOX=1` enable-sandbox accordion in this note points here.
- [oc_install_docker_vm_runtime](oc_install_docker_vm_runtime.md) — shared VM-Docker runtime contract (planned, this series); relevance: the "Running on a VPS?" section defers binary-bake/persistence/updates to it.
- [oc_install_gcp](oc_install_gcp.md) — GCP Compute Engine deploy (planned, this series); relevance: a provider deploy that reuses this generic containerized flow.
- [oc_install_hetzner](oc_install_hetzner.md) — Hetzner VPS deploy (planned, this series); relevance: another provider deploy reusing this image flow.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — how Claude Code runs tools in container runtimes; relevance: closest precedent for a coding-agent container runtime + persistence model.
- [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — Claude Code devcontainer setup; relevance: parallel "run the coding agent in a container" install procedure.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OpenTelemetry monitoring for Claude Code; relevance: directly mirrors this note's OTLP/OTEL export config.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes Docker run modes; relevance: sibling coding-agent gateway's containerized run patterns.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Hermes Docker volumes + supervision; relevance: parallel host-volume persistence + restart-supervision model.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway operations; relevance: sibling gateway day-2 ops (start/stop/health) for the containerized gateway.
- [aws_ec2_connect_methods](../aws_ec2/aws_ec2_connect_methods.md) — methods for reaching an EC2 instance; relevance: cross-domain anchor for host-vs-loopback/SSH access to a containerized service on a VM.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: source of `scripts/docker/setup.sh`, `Dockerfile`, and `docker-compose.yml` this note drives.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the gateway process that runs inside the container.

**Snippets**
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image record lifecycle; relevance: code behind the build/pre-built/airgapped image flow.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway startup + auth; relevance: what the container runs on `docker compose up`.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen bind; relevance: the `gateway.bind` lan/loopback exposure this note configures.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env resolution; relevance: the `OPENCLAW_*` env vars table this note documents.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: the `config set --batch-json` manual-flow config writes.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP binding; relevance: the LAN-vs-loopback / host-local-providers (`host.docker.internal`) networking.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — device/node pairing; relevance: the Control-UI device-approve pairing in troubleshooting.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor/repair routine; relevance: the `dashboard --no-open` / doctor recovery steps in troubleshooting.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token vs password auth modes; relevance: the Control-UI shared-secret/token auth at first open.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: the `openclaw-cli` sidecar commands run after the gateway exists.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — Hermes gateway lifecycle CLI; relevance: cross-system parallel for container start/stop/restart lifecycle.

### oc_install_docker_agent_sandbox (8t · 11s · 11d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: the core concept — agent tool execution isolated in per-scope Docker containers.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the default sandbox backend container engine (`agents.defaults.sandbox.docker`).
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — scope of damage from a compromise; relevance: the "hard wall around untrusted/multi-tenant sessions" the sandbox limits.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/attack-surface modeling; relevance: why multi-tenant/untrusted-agent isolation is needed.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the gateway whose agents are sandboxed while the gateway stays on the host.
- [Access Control](../../term_dictionary/term_access_control.md) — allow/deny authorization; relevance: the allow/deny tool policies + network isolation configured per sandbox.
- [DevOps](../../term_dictionary/term_devops.md) — build/operate practices; relevance: building the default sandbox image (`scripts/sandbox-setup.sh`) + custom-image ops.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating containers; relevance: per-agent/per-session/shared scope orchestration of sandbox containers + `/workspace` mounts.

**Docs**
- [oc_install_docker_containerized_gateway](oc_install_docker_containerized_gateway.md) — the containerized-gateway deploy (planned, this series); relevance: the deploy note that enables this sandbox via `OPENCLAW_SANDBOX=1`.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — Claude Code sandbox modes; relevance: directly parallel `off/non-main/all` sandbox-mode taxonomy.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — filesystem + network isolation; relevance: the `/workspace` mount + network-isolation + resource-limit model this note describes.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox container runtime; relevance: the Docker-backed sandbox container runtime mechanics.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission model; relevance: sandbox-isolation vs tool-policy distinction echoed by OpenClaw's sandbox-vs-tool-policy split.
- [cc_sandbox_settings](../claude_code/cc_sandbox_settings.md) — sandbox config settings; relevance: parallel `agents.defaults.sandbox` config-key reference.
- [cc_sandbox_limitations_and_troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — sandbox limits/troubleshooting; relevance: mirrors the "image missing / permission errors / custom tools not found" sandbox troubleshooting.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — coding-agent security architecture; relevance: the trust-boundary / untrusted-input isolation rationale.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: cross-system coding-agent isolation/trust-boundary precedent.
- [bedrock_agentcore_identity_inbound_auth](../aws_bedrock_agentcore/bedrock_agentcore_identity_inbound_auth.md) — AgentCore inbound auth/isolation; relevance: cross-domain managed-agent-runtime isolation analog.
- [oc_install_docker_vm_runtime](oc_install_docker_vm_runtime.md) — VM runtime contract (planned, this series); relevance: VM deploys that may layer the sandbox on top.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/sandbox subsystem; relevance: implements the Docker sandbox backend + tool/filesystem policy.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the agent tool execution that gets sandboxed.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session subsystem; relevance: the per-session sandbox scope.

**Snippets**
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec + filesystem allow/deny policy; relevance: the allow/deny tool + filesystem policy the sandbox enforces.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — OpenShell sandbox backend; relevance: the OpenShell sandbox-backend alternative mentioned in this note.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny list; relevance: the deny side of sandbox tool policy.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: auditing sandboxed exec for the untrusted-session boundary.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external/untrusted content handling; relevance: the untrusted/multi-tenant input the sandbox walls off.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill/plugin scanner; relevance: the sandbox-image skill-binary trust surface.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope resolution; relevance: the per-agent/session/shared sandbox scope this note documents.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — agent tool policy; relevance: the tool allow/deny policy attached to each sandbox.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: the `agents.defaults.sandbox` runtime-config wiring.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node/command policy gating; relevance: command gating that complements sandbox isolation.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security audit probe/execute; relevance: verifying the sandbox boundary holds at runtime.

### oc_install_docker_vm_runtime (8t · 10s · 10d)

**Terms**
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the VM container runtime baked + launched here.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the long-lived gateway deployed on the VM.
- [DevOps](../../term_dictionary/term_devops.md) — build/operate practices; relevance: the image-bake → build+launch → persist → update operations loop.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable, drift-free operations; relevance: bake-at-build-time so restarts are reproducible ("anything installed at runtime is lost on restart").
- [Health Check](../../term_dictionary/term_health_check.md) — liveness verification; relevance: the `which gog` / `docker compose logs` verify-after-launch steps.
- [Orchestration](../../term_dictionary/term_orchestration.md) — multi-container coordination; relevance: `docker compose build` + `up -d` launch/restart of the gateway service.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the `node:24-bookworm` base image + `pnpm install/build` build chain.
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — operating/monitoring a long-running agent service; relevance: the `docker compose logs` / `which gog` verify + `git pull → build → up -d` update loop is how you observe and operate the deployed gateway over time.

**Docs**
- [oc_install_docker_containerized_gateway](oc_install_docker_containerized_gateway.md) — generic containerized flow (planned, this series); relevance: the base flow this VM-runtime contract extends.
- [oc_install_gcp](oc_install_gcp.md) — GCP deploy (planned, this series); relevance: a concrete VM deploy that imports this runtime contract via shared-steps links.
- [oc_install_hetzner](oc_install_hetzner.md) — Hetzner deploy (planned, this series); relevance: another concrete VM deploy importing this contract.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Hermes Docker volumes + supervision; relevance: the closest analog for the "what persists where" host-volume map.
- [hermes_docker_tools_local_inference](../hermes_agent/hermes_docker_tools_local_inference.md) — Hermes Docker tools/inference image; relevance: parallel bake-tools-into-the-image pattern.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — devcontainer hardening; relevance: reproducible/hardened coding-agent container image precedent.
- [aws_ec2_ami_overview](../aws_ec2/aws_ec2_ami_overview.md) — EC2 AMI overview; relevance: cross-domain "bake everything into the image, treat the host as ephemeral" analog.
- [aws_ec2_instance_lifecycle](../aws_ec2/aws_ec2_instance_lifecycle.md) — EC2 instance lifecycle; relevance: the ephemeral-container-vs-persistent-host lifecycle distinction.
- [cdk_cli_deploy_destroy](../aws_cdk/cdk_cli_deploy_destroy.md) — CDK deploy/destroy; relevance: cross-domain rebuild-and-relaunch reproducible-deploy analog for the update flow.
- [bedrock_agentcore_cli_quickstart_deploy](../aws_bedrock_agentcore/bedrock_agentcore_cli_quickstart_deploy.md) — AgentCore CLI build+deploy; relevance: cross-domain build-image → deploy-runtime parallel.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the image source + Compose files baked here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the long-lived gateway process this runtime hosts.

**Snippets**
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: the image build/record/persistence behind the bake step.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: config persistence/reload across container restarts.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: the apply-on-restart side of the persistence contract.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: the `OPENCLAW_*` / `XDG_CONFIG_HOME` env baked into the image.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — graceful shutdown; relevance: safe `restart: unless-stopped` restart behavior.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — config + plugin load; relevance: plugin-package roots that must persist on the mount.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persistence; relevance: the session/state that must survive restarts (host volume).
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — auth-profile OAuth portability; relevance: the `auth-profiles.json` that persists on the host mount.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — Hermes systemd gateway; relevance: cross-system always-on/restart-supervision analog.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — Hermes gateway lifecycle; relevance: cross-system build/launch/restart lifecycle parallel.

### oc_install_exe_dev (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the gateway deployed on the exe.dev VM at `https://<vm-name>.exe.xyz`.
- [nginx](../../term_dictionary/term_nginx.md) — HTTP server/reverse proxy; relevance: the `sites-enabled/default` proxy from port 8000/80 → `127.0.0.1:18789` with WebSocket upgrade.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting an upstream; relevance: the proxy pattern + forwarded-header hardening this note configures.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption / HTTPS; relevance: the HTTPS termination exe.dev provides at the `<vm-name>.exe.xyz` URL.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: token/password `gateway.auth.mode` + device pairing + exe.dev email auth.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: `ssh exe.dev new` / `ssh <vm-name>.exe.xyz` provisioning and remote `config patch` over SSH.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex protocol over HTTP; relevance: the nginx `Upgrade`/`Connection: upgrade` headers required for the gateway WS.
- [DevOps](../../term_dictionary/term_devops.md) — provision/configure/update practices; relevance: the Shelley auto-install → manual VM-create → proxy → update ops loop.

**Docs**
- [oc_install_docker_containerized_gateway](oc_install_docker_containerized_gateway.md) — containerized alternative (planned, this series); relevance: the container path vs this bare-VM install.
- [oc_install_fly](oc_install_fly.md) — Fly.io deploy (planned, this series); relevance: sibling remote-access always-on deploy with managed HTTPS.
- [oc_install_gcp](oc_install_gcp.md) — GCP deploy (planned, this series); relevance: sibling VM deploy with SSH-tunnel access (vs exe.dev proxy URL).
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes remote dashboard auth; relevance: closest analog for remote Control-UI auth + pairing.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — Hermes OAuth over SSH; relevance: parallel SSH-mediated remote auth/config for a VM-hosted gateway.
- [hermes_messaging_matrix_proxy_mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — Hermes proxy-mode messaging; relevance: cross-system reverse-proxy-fronting pattern.
- [hermes_api_server_setup_auth](../hermes_agent/hermes_api_server_setup_auth.md) — Hermes API server setup + auth; relevance: parallel "expose the agent server behind auth on a VM" setup.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code proxy/gateway config; relevance: cross-system proxy-in-front-of-the-agent config precedent.
- [aws_ec2_connect_methods](../aws_ec2/aws_ec2_connect_methods.md) — EC2 connect methods; relevance: cross-domain SSH-into-a-cloud-VM access analog.
- [pi_terminal_setup](../pi/pi_terminal_setup.md) — Pi terminal/CLI setup; relevance: cross-system CLI install + first-run auth precedent.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the gateway + device-pairing flow this VM runs.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI wizard/onboarding; relevance: `openclaw devices approve <requestId>` pairing CLI + onboarding.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the `install.sh` install target on the VM.

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token vs password auth modes; relevance: the `gateway.auth.mode` token/password modes this note sets.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: pasting the shared secret into Control UI at `<vm-name>.exe.xyz`.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS; relevance: TLS/identity for the reachable HTTPS client.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy; relevance: the gateway behind the nginx reverse proxy + forwarded headers.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — device/node pairing; relevance: the `devices list`/`devices approve` pairing this note runs.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth authorize dispatch; relevance: the gateway-side auth check on remote access.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: the remote `config patch --stdin` apply + `gateway restart`.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode; relevance: the remote-channel-setup Slack `mode: "socket"` patch.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord channel intents; relevance: the Discord channel config in the remote patch.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — Hermes OAuth callback server; relevance: cross-system headless/remote OAuth-redirect handling analog.

### oc_install_fly (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the gateway deployed on a Fly.io machine.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: Fly builds + runs the OpenClaw `Dockerfile` image (under `tini`).
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: `OPENCLAW_GATEWAY_TOKEN` / `gateway.auth.password` non-loopback auth + channel credentials.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the model/channel API-key secrets (`fly secrets set ...`) injected at runtime.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption / HTTPS; relevance: Fly's automatic HTTPS + `force_https` on the public URL.
- [DevOps](../../term_dictionary/term_devops.md) — deploy/operate practices; relevance: the `fly deploy` / secrets / volumes / machine-update ops loop.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — exposure scope; relevance: the hardened private-deployment (no public IP, hidden from scanners) isolation.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness probing; relevance: Fly `internal_port` health checks + the "health checks failing" troubleshooting.

**Docs**
- [oc_install_docker_containerized_gateway](oc_install_docker_containerized_gateway.md) — containerized image flow (planned, this series); relevance: the image flow Fly machines run.
- [oc_install_hetzner](oc_install_hetzner.md) — Hetzner VPS deploy (planned, this series); relevance: sibling self-managed VPS deploy (cross-linked in source Related).
- [oc_install_gcp](oc_install_gcp.md) — GCP VM deploy (planned, this series); relevance: sibling cloud-VM deploy.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes Docker run modes; relevance: parallel managed-host containerized run with persistent volume.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — Hermes env-var provider/auth config; relevance: closest analog for env-var-over-config-file secret injection.
- [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — Claude Code Bedrock setup; relevance: cross-system model-provider API-key/secret setup precedent.
- [cc_enterprise_deployment_options](../claude_code/cc_enterprise_deployment_options.md) — Claude Code deployment options; relevance: cross-system managed-host vs self-host deploy-option comparison.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure-deployment principles; relevance: the secrets-out-of-config + minimize-public-exposure hardening this note teaches.
- [bedrock_agentcore_cli_quickstart_deploy](../aws_bedrock_agentcore/bedrock_agentcore_cli_quickstart_deploy.md) — AgentCore quick deploy; relevance: cross-domain managed-runtime deploy parallel.
- [aws_ec2_enhanced_networking](../aws_ec2/aws_ec2_enhanced_networking.md) — EC2 networking; relevance: cross-domain public-vs-private network exposure analog (Fly public IP vs private IPv6/WireGuard).

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the gateway + the gateway-lock behavior in Fly troubleshooting.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the cloned repo + `fly.toml` / `deploy/fly.private.toml`.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels subsystem; relevance: the Discord/Telegram channel access this deploy enables.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials/secrets; relevance: the secret/credential injection `fly secrets` backs.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persistence; relevance: the state-persistence the Fly volume (`/data`) backs (state-not-persisting troubleshooting).
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen bind; relevance: the `--bind lan` / `internal_port` listen-address troubleshooting.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — startup + auth; relevance: the `--allow-unconfigured` startup guard + gateway-token requirement.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token/password auth modes; relevance: the `OPENCLAW_GATEWAY_TOKEN` vs password auth choice.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — graceful shutdown; relevance: the gateway-lock / PID-lock-file-on-restart troubleshooting.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: writing `/data/openclaw.json` then restarting to apply.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: the Discord channel config (`channels.discord`) this deploy sets.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM/guild allowlist; relevance: the `groupPolicy: "allowlist"` guild allowlist in the config.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — call method gating; relevance: the webhook/`webhookSecurity.allowedHosts` gating in the private-deployment voice-call example.
- [snippet_hermes_agent_gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — Hermes gateway config load; relevance: cross-system gateway config-file load + first-run bootstrap analog.

### oc_install_gcp (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the 24/7 gateway deployed on a GCP Compute Engine VM.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the isolated app runtime installed + run on the VM.
- [IAM](../../term_dictionary/term_iam.md) — identity + access management; relevance: GCP IAM + the dedicated service-account least-privilege section.
- [DevOps](../../term_dictionary/term_devops.md) — provision/operate practices; relevance: the project → VM → Docker → persist → launch → update ops loop.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: `gcloud compute ssh ... -- -L 18789:127.0.0.1:18789` SSH-tunnel Control-UI access.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness verification; relevance: the verify-after-launch + OOM/`exit 137` build troubleshooting.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — exposure scope; relevance: service-account least-privilege (avoid Owner role) limits blast radius.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization; relevance: the loopback-only port mapping + IAM role binding controlling who can reach the gateway.

**Docs**
- [oc_install_docker_vm_runtime](oc_install_docker_vm_runtime.md) — shared VM runtime contract (planned, this series); relevance: the bake/build/persist/update steps this note imports via shared-steps links.
- [oc_install_docker_containerized_gateway](oc_install_docker_containerized_gateway.md) — generic Docker flow (planned, this series); relevance: the base containerized flow referenced for the generic path.
- [oc_install_hetzner](oc_install_hetzner.md) — Hetzner deploy (planned, this series); relevance: the near-identical sibling VM deploy (same `.env`/compose/tunnel).
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes Docker run modes; relevance: parallel cloud-VM containerized always-on run.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway operations; relevance: day-2 ops for a self-managed cloud-VM gateway.
- [cc_google_vertex_ai](../claude_code/cc_google_vertex_ai.md) — Claude Code on Google Vertex AI; relevance: cross-system Google-Cloud project/billing/auth setup precedent.
- [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — Claude Code Bedrock setup; relevance: cross-system cloud-provider VM/credential setup analog.
- [aws_ec2_instance_lifecycle](../aws_ec2/aws_ec2_instance_lifecycle.md) — EC2 instance lifecycle; relevance: cross-domain create/stop/change-machine-type VM lifecycle (mirrors `gcloud compute instances` OOM remediation).
- [aws_cfn_iam_overview](../aws_cloudformation/aws_cfn_iam_overview.md) — IAM in CloudFormation; relevance: cross-domain least-privilege IAM role/binding analog for the service-account section.
- [bedrock_agentcore_identity_outbound_providers](../aws_bedrock_agentcore/bedrock_agentcore_identity_outbound_providers.md) — AgentCore outbound identity/providers; relevance: cross-domain agent-runtime service-identity + outbound-credential parallel.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the long-lived gateway process on the VM.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the cloned image source + `docker-compose.yml`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: the least-privilege / service-account security guidance.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials/secrets; relevance: the `.env` / auth-profile secret persistence on the host mount.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: the `OPENCLAW_GATEWAY_*` / `XDG_CONFIG_HOME` `.env` env vars this note sets.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen bind; relevance: the `--bind lan` + loopback `127.0.0.1:` port mapping.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP binding; relevance: the loopback-only-on-VM + SSH-tunnel access pattern.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: the `config set gateway.controlUi.allowedOrigins` trusted-origin write.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: pasting the token/password into Control UI over the tunnel.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — device/node pairing; relevance: the `devices list`/`devices approve` after `pairing required (1008)`.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — graceful shutdown; relevance: `restart: unless-stopped` safe-restart behavior.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential order; relevance: the `agents/<id>/agent/auth-profiles.json` on the persistent mount.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: the custom-image build for binary persistence.
- [snippet_hermes_agent_cli_gateway_pid_discovery](../../code_snippets/snippet_hermes_agent_cli_gateway_pid_discovery.md) — Hermes gateway PID discovery; relevance: cross-system always-on gateway process management analog.

### oc_install_hetzner (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the 24/7 gateway deployed on a cheap Hetzner VPS.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the isolated app runtime installed + run on the VPS.
- [DevOps](../../term_dictionary/term_devops.md) — provision/operate practices; relevance: the provision → Docker → persist → compose-up → verify ops loop.
- [Terraform](../../term_dictionary/term_terraform.md) — declarative infrastructure-as-code; relevance: the community Terraform/cloud-init Infrastructure-as-Code provisioning section.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: `ssh root@VPS` provisioning + `ssh -N -L 18789:...` tunnel (with `AllowTcpForwarding local`).
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/attack-surface modeling; relevance: the security-model reminder (dedicated VPS, no personal profiles, split adversarial users).
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — exposure scope; relevance: the trust-boundary separation (dedicated runtime/account) limiting blast radius.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness verification; relevance: the "verify persistence and Gateway access" step.

**Docs**
- [oc_install_docker_vm_runtime](oc_install_docker_vm_runtime.md) — shared VM runtime contract (planned, this series); relevance: the bake/build/persist/update steps this note imports.
- [oc_install_gcp](oc_install_gcp.md) — GCP deploy (planned, this series); relevance: the near-identical sibling VM deploy (same compose/tunnel pattern).
- [oc_install_fly](oc_install_fly.md) — Fly.io deploy (planned, this series); relevance: sibling deploy (cross-linked in source Related).
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Hermes Docker volumes/supervision; relevance: parallel host-volume persistence + restart supervision on a self-managed host.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Hermes Nix/IaC quickstart; relevance: cross-system reproducible/declarative install analog for the Terraform section.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — devcontainer hardening; relevance: the trust-boundary/hardening posture for an exposed coding-agent host.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — coding-agent security architecture; relevance: the adversarial-multi-user trust-boundary rationale.
- [cdk_getting_started](../aws_cdk/cdk_getting_started.md) — AWS CDK getting started; relevance: cross-domain infrastructure-as-code provisioning analog for Terraform.
- [aws_cfn_best_practices_templates](../aws_cloudformation/aws_cfn_best_practices_templates.md) — CloudFormation template best practices; relevance: cross-domain IaC reproducible-provisioning + remote-state best-practice analog.
- [aws_ec2_connect_methods](../aws_ec2/aws_ec2_connect_methods.md) — EC2 connect methods; relevance: cross-domain SSH-into-VPS / TCP-forwarding access analog.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the long-lived gateway process on the VPS.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the cloned image source + `docker-compose.yml`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: the security/trust-boundary model this note references.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials/secrets; relevance: the host-mounted `.env` / auth secrets (`GOG_KEYRING_PASSWORD`, gateway token).
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: the `OPENCLAW_*` `.env` env vars this note configures.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen bind; relevance: the loopback-only `127.0.0.1:` port mapping + `--bind lan`.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP binding; relevance: the loopback-only-on-VPS + SSH-tunnel access pattern.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: the dedicated-runtime / no-personal-profiles trust-boundary posture.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: the business-only / adversarial-user separation guidance.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applying `gateway.controlUi.allowedOrigins` / config after launch.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — graceful shutdown; relevance: `restart: unless-stopped` safe-restart behavior.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: the custom-image build for binary persistence.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — Hermes systemd gateway; relevance: cross-system always-on/restart-supervision analog on a VPS.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root guard; relevance: the run-as-root vs uid-1000 ownership (`chown -R 1000:1000`) consideration.

**Analysis (additional)**

### Cross-cutting (every note)

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| OpenClaw, gateway, agent sandbox | LINK existing `term_openclaw`; sandbox concept → digested as `oc_install_docker_agent_sandbox` (oc_ doc note) + link `term_sandbox`; gateway → link `repo_openclaw_gateway`. No new term. |
| Docker, Docker Compose, image, Dockerfile, container, airgapped/offline rerun | LINK existing `term_docker`. Compose/image/container are Docker sub-concepts → no separate term notes; documented inline as deploy mechanics. No new term. |
| baked binaries / bake-at-build-time / persistence (`~/.openclaw`) | OpenClaw-specific deploy mechanics → digested in `oc_install_docker_vm_runtime` (oc_ doc note); link `term_idempotency`. No new term. |
| nginx, reverse proxy, HTTPS/TLS, LAN vs loopback, SSH tunnel, port forwarding | LINK existing `term_nginx`, `term_reverse_proxy`, `term_tls`, `term_ssh`. `term_https`/`term_port_forwarding` MISSING but are thin generic networking concepts already covered by `term_tls`/`term_reverse_proxy` — link those, do NOT create. No new term. |
| Fly.io, GCP, Compute Engine, Hetzner, exe.dev, VPS, cloud VM | Provider/host names — documented as deploy targets in their `oc_install_*` notes, NOT promoted to term notes (per master policy). `term_vps`/`term_gcp`/`term_azure` MISSING — generic and not vault-reusable cross-cutting; do NOT create. No new term. |
| service account, IAM, least privilege, trust boundary, threat model | LINK existing `term_iam`, `term_threat_model`, `term_blast_radius`. `term_least_privilege`/`term_service_account` MISSING — covered by `term_iam` + `term_blast_radius`; do NOT create. No new term. |
| Terraform / Infrastructure as Code | LINK existing `term_terraform`. No new term. |
| health checks, observability, Bonjour/mDNS, gateway auth modes, device pairing | LINK existing `term_health_check`; Bonjour/mDNS + auth-modes + pairing are OpenClaw gateway features → documented inline + linked to `repo_openclaw_gateway` / `snippet_openclaw_gateway_auth_modes_helpers`. `term_bonjour`/`term_mdns`/`term_observability` MISSING — feature-specific, not promoted. No new term. |

**Expected new `term_dictionary` captures: 0.** No genuinely cross-cutting, vault-reusable term lacks an
existing note here — all install/deploy/networking/security vocabulary either has an existing term to LINK or
is an OpenClaw-specific deploy mechanic digested into an `oc_` doc note. (Augment Step 2d re-scans.) If a
new term were ever proposed, the best-fit acronym glossary for this section's vocabulary is
`0_entry_points/acronym_glossary_systems.md` (deployment/infra) or `acronym_glossary_security.md`
(sandbox/trust-boundary).

## Term-Note Authoring Requirements

**N/A (0 new terms).** in02 authors zero `term_dictionary` notes (inherited from master: OpenClaw vocab →
`oc_` doc notes; existing terms linked, never redefined; no term definition inlined in an `oc_*` note). If a
new term were proposed at augment, the master requirement applies: research it across ≥2 sources, write via
`/tessellum-capture-term-note`, and add it to its `acronym_glossary_*.md` (W5).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). All gates must pass before commit.

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean on all 7 notes (YAML field order, `## Overview`/`## Related Notes`, bold footer, no forbidden YAML fields). |
| G2 | Grounding | Each note diffs faithfully against `inbox/openclaw_docs/install/<page>.md` (no invented config/flags; split notes 1+2 together cover docker.md with no omission). |
| G3 | Density + Coverage | Each note ≤400L / ≤2,500w / ≤6 code blocks, one BB; every source H2/H3 mapped (Section Coverage Map) with no orphan. |
| G4 | Cross-Reference | Each note has ≥6 relevancy-selected `term_dictionary` terms + relevant `repo_openclaw*` + sibling `oc_*` + other vault notes in `## Related Notes`, each an indexed link with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after incremental reindex. |
| G7 | Discoverability (inbound) | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 | `note_links` confirms in-degree ≥1 per new note (anti-island). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_install_docker_containerized_gateway oc_install_docker_agent_sandbox oc_install_docker_vm_runtime oc_install_exe_dev oc_install_fly oc_install_gcp oc_install_hetzner"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + LINK-003
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # density caps (body words excl. frontmatter; code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # sibling-prefix sanity: at least one sibling oc_ link expected
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n: no sibling ${SIBLING_PREFIX}* link"
done

# YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_install_docker_containerized_gateway | procedure | 700 | 23 src → ≤6 kept | ✅ (selective fences + link-out to source for full sequence) |
| 2 | oc_install_docker_agent_sandbox | concept | 350 | 2 src → ≤2 | ✅ |
| 3 | oc_install_docker_vm_runtime | procedure | 450 | 7 src → ≤6 | ✅ |
| 4 | oc_install_exe_dev | procedure | 500 | 11 src → ≤6 | ✅ |
| 5 | oc_install_fly | procedure | 700 | 27 src → ≤6 kept | ✅ (representative fly.toml/secrets/troubleshoot blocks; link-out for the rest) |
| 6 | oc_install_gcp | procedure | 650 | 22 src → ≤6 kept | ✅ (representative VM/compose/tunnel blocks) |
| 7 | oc_install_hetzner | procedure | 550 | 10 src → ≤6 | ✅ |

No digest note approaches the word cap. The split of docker.md (2,871w) plus selective fence reproduction on
the code-heavy fly/gcp/docker pages keeps every note ≤6 code blocks and ≤700 words.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `0_entry_points/entry_openclaw_docs.md` (created as the master W1 pre-step) under
the **Install** section, "Container / Cloud-VM deployment" cluster. Each new note gets its entry-point
back-link at finalization (satisfies G7/G8: ≥1 inbound link from outside `documentation/openclaw/`). No new
is handled once at the master level (W2).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; needed for G7/G8 — each new note ≥1):

- `entry_openclaw_docs` (master W1 hub) → all 7 notes (Install section rows).
- `repo_openclaw` → notes 1, 3, 5, 6, 7 (the deploy targets that drive its Docker/Compose scripts).
- `repo_openclaw_gateway` → notes 1, 2, 3, 4, 5, 6, 7 (the gateway each deploy runs / sandboxes).
- `repo_openclaw_security` → note 2 (agent sandbox), notes 6, 7 (service-account / trust-boundary security).
- `repo_openclaw_agents` / `repo_openclaw_sessions` → note 2 (sandbox scope per agent/session).
- `repo_openclaw_cli_wizard` → note 4 (`openclaw devices approve` pairing CLI).
- `repo_openclaw_channels` → note 5 (Discord/Telegram channel access on Fly).
- `term_docker` → notes 1, 2, 3, 5, 6, 7; `term_sandbox` → note 2; `term_terraform` → note 7;
  `term_iam` → note 6; `term_nginx` → note 4; `term_threat_model` → notes 2, 7.
- `thought_openclaw_drives_dks_runtime` → notes 1, 6 (the runtime these host).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page at execution; reproduce config/CLI
snippets verbatim but cap at ≤6 per note (link-out to the source page for full sequences on the code-heavy
docker/fly/gcp guides). One BB per note. Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest
in the script; `git pull --rebase --autostash` first, commit+push after the phase, no Claude co-author
trailer; reindex incrementally and verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note Related mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY** (9/9 CP pass) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass (xref-augment):** locked the per-note `## Related Notes` mapping at the RAISED
re-reading all 6 source pages under `inbox/openclaw_docs/install/` and selecting only relevance-matched
existing vault notes. The plan already carried the augment-mandatory sections from upstream (Section
Coverage Map, Split Decisions, Density Re-Assessment, Validation Scripts, Per-Phase G1–G8 gate table,
Undigested Terms Plan, Entry Point Decision, Inlinks, Pacing Rules) — those were verified, not rewritten.
The legacy `## Candidate Cross-References` (≥6-term PLAN-stage pool) was replaced by the LOCKED mapping.

**Source re-read (measured 2026-06-21, matches plan Source table exactly):** docker 2,871w · docker-vm-runtime
681w · exe-dev 808w · fly 1,838w · gcp 1,423w · hetzner 1,006w = 8,627w. No density surprises; the docker.md
1→2 split (containerized-gateway procedure vs agent-sandbox concept) holds.

**Per-note locked counts (all floors met):**

| Note | Terms | Snippets | Docs (≥5 existing) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_install_docker_containerized_gateway | 8 | 11 | 11 (7 existing + 4 planned sibling) | 2 | ✅ |
| oc_install_docker_agent_sandbox | 8 | 11 | 11 (9 existing + 2 planned sibling) | 3 | ✅ |
| oc_install_docker_vm_runtime | 8 | 10 | 10 (7 existing + 3 planned sibling) | 2 | ✅ |
| oc_install_exe_dev | 8 | 10 | 10 (7 existing + 3 planned sibling) | 3 | ✅ |
| oc_install_fly | 8 | 11 | 10 (7 existing + 3 planned sibling) | 3 | ✅ |
| oc_install_gcp | 8 | 11 | 10 (7 existing + 3 planned sibling) | 3 | ✅ |
| oc_install_hetzner | 8 | 11 | 10 (7 existing + 3 planned sibling, +1 analysis additional) | 3 | ✅ |

**DB-verification (G5, 2026-06-21):** all cited EXISTING note_ids confirmed present via
section: 227 `.md` links → 204 existing-verified OK · 22 planned (sibling `oc_*` this series + the
`entry_openclaw_docs` master-W1 hub) · 1 non-citation (`relpath.md`, the render-format example in the
devcontainer, install, llm_gateway, proxy, opentelemetry, security, bedrock/vertex, secure-deployment),
`hermes_agent/hermes_*` (docker run-modes/volumes/tools, install/nix, gateway ops/internals, env-vars,
oauth-over-ssh, dashboard-auth-remote, api-server-auth, matrix-proxy, discord/slack), `pi/pi_*`
(security-model, provider-auth, terminal-setup), `aws_ec2/`, `aws_cdk/`, `aws_cloudformation/`,
`aws_bedrock_agentcore/` (cross-domain VM-lifecycle, IaC, IAM least-privilege, managed-runtime deploy/identity).

**New-term candidates:** **0.** The re-read (augment Step 2d) surfaced no genuinely cross-cutting,
vault-reusable term lacking an existing note. The MISSING slugs noted in the Undigested Terms Plan
(`term_https`, `term_vps`, `term_gcp`, `term_azure`, `term_secret`, `term_service_account`,
`term_least_privilege`, `term_port_forwarding`, `term_observability`, `term_environment_variables`,
`term_self_hosted`, `term_bonjour`, `term_mdns`) are confirmed thin/generic networking-or-provider concepts
already covered by existing terms LINKED in the mapping (`term_tls`, `term_reverse_proxy`, `term_iam`,
`term_blast_radius`, `term_devops`, `term_ssh`, `term_observability_agent_systems`, `term_orchestration`),
OR OpenClaw-specific deploy mechanics digested into the `oc_*` doc notes. Best-fit glossary (if ever needed):
`0_entry_points/acronym_glossary_systems.md` (deploy/infra) or `acronym_glossary_security.md`
(sandbox/trust-boundary). **in02 authors 0 `term_dictionary` notes** (master policy inherited).

**Issues / notes for execution:**
  (CREATE before the first sub-plan executes). It is cited in every note's mapping (hub backlink, G7/G8) and
  in the Inlinks table; the executor must ensure W1 lands before/at finalization so each note ends with the
  outside-folder inbound link. Marked "(planned, master W1 pre-step)" — NOT a ghost (it is a planned target,
  satisfied at execution time).
- Sibling `oc_install_*` docs in this series do not exist yet (this sub-plan creates them) — counted toward
  the 10-doc floor as "(planned, this series)" per the augment standard; each note still carries ≥7 EXISTING

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance + relevance statements) | **PASS** | LOCKED `## Per-Note Related Notes Mapping` present; every note ≥8 terms · ≥10 snippets · ≥10 docs; each link rendered `- [Name](relpath.md) — what; relevance: why THIS note`. Per-note: 8t/11s/11d, 8t/11s/11d, 8t/10s/10d, 8t/10s/10d, 8t/11s/10d, 8t/11s/10d, 8t/11s/10d. |
| CP2 | 9-GATE present per batch (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7 Discoverability(inbound), G8 In-degree≥1 for the single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at master W1) | **PASS** | `## Entry Point Decision` states 7 rows contribute to `0_entry_points/entry_openclaw_docs.md` (master W1 pre-step, CREATE — series >30 notes); no new entry point created by this sub-plan; parent-hub wiring at master W2. Each note's hub backlink satisfies G7/G8. |
| CP4 | Size (≤30 notes / split) | **PASS** | 7 planned notes (well under 30); single execution phase. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Shared Format Definition inherited from master, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (same source type): `# OpenClaw — Title` → `## Overview` → source-mirrored H2/H3 → `## Related Notes` → `## References` → bold footer; YAML field order + forbidden fields specified; density caps ≤400L/≤2500w/≤6 code. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment` table: every note ≤700w / ≤6 code blocks / ≤400L; docker.md (2,871w, mixed BB) split 1→2 per word-cap + one-BB rule; no further splits needed. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-read 2026-06-21 (`wc -w`): docker 2,871 · docker-vm-runtime 681 · exe-dev 808 · fly 1,838 · gcp 1,423 · hetzner 1,006 = 8,627w — matches the plan Source table exactly (ratio 1.00). |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (8 rows, all dispositioned LINK-existing or digest-into-`oc_*`, 0 TBD); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; master multi-source mandate applies if any proposed). Expected new captures: 0. |
| CP9 | Discoverability / inlinks (G7/G8 executed, no islands) | **PASS** | `## Inlinks (existing notes → new notes)` table maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` hub → all 7; plus `repo_openclaw*`, `term_*`, `thought_*` inlinks). G7/G8 in the gate table require in-degree ≥1 per new note, executed (not "recommended"). |

**RESULT: 9/9 CP PASS → READY FOR EXECUTION.** All checkpoints pass and all 7 notes meet the raised floors
