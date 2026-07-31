---
title: Sub-Plan rt03 — OpenClaw Docs: Top-level (agent-runtime, platforms, prose, providers, tools, vps, web)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["openclaw-agent-runtime", "platforms", "prose", "providers", "tools", "vps", "web"]
status_history: "pending → ready (xref-augment + review 2026-06-21, 9/9 CP PASS)"
---

# Sub-Plan rt03: Top-level

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_*`), format, dedup-before-create, 9-GATE validation, cross-references, undigested-terms ownership, and entry-point decisions are ALL inherited from the master — read it first.

## Scope

The 7 **top-level (root-slug) hub/overview pages** of `docs.openclaw.ai` — the routing/landing pages that sit at the docs root, each summarizing a whole section and linking down into it:

- `openclaw-agent-runtime` — the developer build/test/live-validation workflow for the OpenClaw agent runtime (procedure).
- `platforms` — platform-support overview: OS picker, recommended Node runtime, companion apps, and the Gateway-service install matrix (procedure).
- `prose` — OpenProse: the markdown-first multi-agent `.prose` workflow format shipped as an OpenClaw plugin with a `/prose` slash command (procedure).
- `providers` — the model-provider directory: 50+ LLM/transcription/media providers and the `provider/model` default-model pattern (concept/index).
- `tools` — the Tools-vs-Skills-vs-Plugins capabilities routing page: built-in tool categories, plugin-provided tools, policy/approvals, and troubleshooting (concept).
- `vps` — running the Gateway on a Linux server / cloud VPS: provider picker, cloud architecture, admin hardening, nodes, and small-VM/ARM startup tuning (procedure).
- `web` — Gateway web surfaces: the browser Control UI, bind modes, Tailscale access (Serve / tailnet+token / Funnel), and security (procedure).

**Priority P1 (Phase A)** — these are conceptual/operational landing pages the rest of the OpenClaw corpus references and that an entry-point reader hits first. The code-side counterparts (`repo_openclaw*`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 4,119 measured words. **Planned: 7 notes (1 per page; no splits).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| openclaw-agent-runtime | /openclaw-agent-runtime | 328 | 2 | 6 | 0 | procedure |
| platforms | /platforms | 291 | 0 | 5 | 0 | procedure |
| prose | /prose | 641 | 4 | 9 | 0 | procedure |
| providers | /providers | 375 | 1 | 5 | 0 | concept (provider index) |
| tools | /tools | 1,244 | 0 | 8 | 0 | concept (capabilities routing) |
| vps | /vps | 698 | 3 | 6 | 1 | procedure |
| web | /web | 542 | 7 | 6 | 3 | procedure |

Total: **4,119 words · 17 code fences · 45 H2 · 4 H3.** All pages well under the 2,500-word / 6-code-block caps; the only page with >6 raw fences is `web` (7), reproduced selectively to stay ≤6 in the note.

## Content Strategy

- **Prioritize**: the operational/conceptual landing content each page leads with — `tools`' Tools/Skills/Plugins decision framework and built-in tool-category table; `web`'s bind-mode + Tailscale + auth security model; `vps`' cloud architecture + admin-hardening + startup tuning; `prose`'s `.prose` format, `/prose` command, and OpenClaw-primitive mapping; `platforms`' OS picker + Gateway-service-install matrix; `providers`' `provider/model` default-model pattern; `openclaw-agent-runtime`'s build/test/live gates and clean-slate reset.
- **Split**: none. Every page is small and single-BB; each becomes exactly one `oc_*` note. (`tools` is the largest at 1,244w but is one coherent capabilities-routing concept — no split.)
- **Link-out (do NOT re-digest)**: the dozens of down-links each hub page contains (`/providers/<name>`, `/platforms/<os>`, `/install/<host>`, `/tools/<tool>`, `/gateway/*`, `/channels`, `/nodes`, `/automation`) are owned by other sub-plans (pr*, pf*, in*, to*, gw*, ch*, nd01–02, au01). rt03 notes mirror the hub/routing content and link to those sibling `oc_*` notes as planned, NOT inline their content. Provider/OS/host names are config values, not new term notes. Existing terms (`term_openclaw`, `term_mcp`, `term_llm`, `term_tailscale`*, `term_node_js`, etc.) are linked, never redefined. (*`term_tailscale` does not exist — see Undigested Terms Plan.)

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_agent_runtime_workflow.md` | procedure | openclaw-agent-runtime.md: Type checking and linting, Running Agent Runtime Tests, Manual testing, Clean slate reset | 380 | Developer workflow for the OpenClaw agent runtime: `pnpm check`/`build`/`test` gates, the Vitest agent-runtime test set (incl. `OPENCLAW_LIVE_TEST=1`), manual gateway-dev/TUI testing, and the clean-slate reset of the `~/.openclaw` state directory (config, auth-profiles, credentials, sessions, workspace). |
| 2 | `oc_platforms_overview.md` | procedure | platforms.md: (intro), Choose your OS, VPS and hosting, Common links, Gateway service install (CLI) | 360 | Platform-support overview: OpenClaw core is TypeScript with Node as the recommended runtime (Bun not recommended for the Gateway); companion apps (Windows Hub, macOS menu-bar, iOS/Android nodes); the per-OS picker; and the four Gateway-service install paths (`onboard --install-daemon`, `gateway install`, `configure`, `doctor`) with their per-OS service targets (LaunchAgent / systemd user service / Scheduled Task). |
| 3 | `oc_openprose_workflow.md` | procedure | prose.md: (intro), Install, Slash command, What it can do, Example, OpenClaw runtime mapping, File locations, State backends, Security | 560 | OpenProse: the markdown-first multi-agent `.prose` workflow format shipped as an OpenClaw plugin. Enabling `open-prose`, the `/prose` slash command (run/compile/examples, handle/slug + URL resolution), the parallel-research example, how OpenProse concepts map to OpenClaw primitives (`sessions_spawn`/`read`/`write`/`web_fetch`), `.prose/` file layout, the four state backends (filesystem/in-context/sqlite/postgres), and treating `.prose` files as code. |
| 4 | `oc_provider_directory.md` | concept | providers.md: (intro), Quick start, Provider docs, Shared overview pages, Transcription providers, Community tools | 380 | The OpenClaw model-provider directory: the `provider/model` default-model pattern set in config after `openclaw onboard` auth, the catalog of 50+ LLM providers (Anthropic, Bedrock, OpenAI, Google, Groq, Mistral, OpenRouter, local Ollama/vLLM/LM Studio, etc.), shared media-generation overview pages, transcription providers, and the community Claude-Max proxy caveat. Indexes the `oc_providers_*` (pr*) series; does not redefine providers. |
| 5 | `oc_tools_overview.md` | concept | tools.md: Start here, Choose tools/skills/or plugins, Built-in tool categories, Plugin-provided tools, Configure access and approvals, Extend capabilities, Troubleshoot missing tools | 620 | The Capabilities routing page: tools (callable typed actions) vs skills (`SKILL.md` instruction packs) vs plugins (runtime capabilities); the built-in tool-category table (Runtime/Files/Web/Browser/Messaging/Sessions/Automation/Gateway/Media/Tool-Search); plugin-provided tools and `api.registerTool`; how tool policy (profile, allow/deny, provider restrictions, sandbox, channel, plugin availability) is enforced before the model call; extension paths; and the missing-tool troubleshooting checklist. |
| 6 | `oc_vps_linux_server.md` | procedure | vps.md: Pick a provider, How cloud setups work, Harden admin access first, Shared company agent on a VPS, Using nodes with a VPS, Startup tuning for small VMs and ARM hosts (+ systemd tuning checklist) | 620 | Running the OpenClaw Gateway on a Linux server / cloud VPS: the hosting-provider picker (Railway, DigitalOcean, Oracle, Fly, Hetzner, GCP, Azure, exe.dev, Raspberry Pi, AWS), the cloud architecture (Gateway owns state on the VPS; access via Control UI / Tailscale / SSH; back up state+workspace), admin-access hardening (Tailnet-only SSH), shared-company-agent trust boundaries, pairing local nodes to a cloud Gateway, and small-VM/ARM startup tuning (`NODE_COMPILE_CACHE`, `OPENCLAW_NO_RESPAWN`, systemd unit env + restart policy). |
| 7 | `oc_web_control_ui.md` | procedure | web.md: (intro), Webhooks, Admin HTTP RPC, Config, Tailscale access (Integrated Serve / Tailnet bind+token / Public Funnel), Security notes, Building the UI | 600 | The Gateway web surfaces: the browser Control UI (Vite + Lit) served on the Gateway WebSocket port (`:18789`), default-on config (`gateway.controlUi`), the webhook + Admin-HTTP-RPC endpoints, the three Tailscale access modes (Integrated Serve on loopback, tailnet bind + token auth, public Funnel + password), the auth/security model (token/password/trusted-proxy/Tailscale-identity, non-loopback always requires auth, `allowedOrigins`, TLS `wss://`), and building the UI (`pnpm ui:build`). |

## Section Coverage Map

```
openclaw-agent-runtime.md
├── (intro: "A sane workflow…")                       → note 1 (oc_agent_runtime_workflow)
├── Type checking and linting (pnpm check/build/test) → note 1
├── Running Agent Runtime Tests (Vitest + live test)  → note 1
├── Manual testing (gateway:dev / agent / tui)        → note 1
├── Clean slate reset (~/.openclaw state dir)         → note 1
├── References (Testing, Getting Started)             → note 1 (## References, external/link-out)
└── Related (agent-runtime-architecture)              → note 1 (link → oc_agent_runtime_architecture, rt01 planned)
platforms.md
├── (intro: TypeScript/Node, Bun caveat, companions)  → note 2 (oc_platforms_overview)
├── Choose your OS (macOS/iOS/Android/Windows/Linux)  → note 2 (link → pf* notes, planned)
├── VPS and hosting                                   → note 2 (link → oc_vps_linux_server + in* notes)
├── Common links                                      → note 2
└── Gateway service install (CLI) + service targets   → note 2
prose.md
├── (intro: OpenProse portable .prose format)         → note 3 (oc_openprose_workflow)
├── Install (enable open-prose, restart, verify)      → note 3
├── Slash command (/prose run/compile/examples/…)     → note 3
├── What it can do                                    → note 3
├── Example: parallel research and synthesis          → note 3
├── OpenClaw runtime mapping (sessions_spawn/read/…)  → note 3
├── File locations (.prose/ layout, ~/.prose/agents)  → note 3
├── State backends (filesystem/in-context/sqlite/pg)  → note 3
├── Security (treat .prose as code, allowlists)       → note 3
└── Related (skills/subagents/tts/slash-commands)     → note 3 (link → to* notes, planned)
providers.md
├── (intro: many LLM providers, provider/model)       → note 4 (oc_provider_directory)
├── Quick start (onboard auth + default model json5)  → note 4
├── Provider docs (50+ provider links)                → note 4 (index → pr* notes, planned; not inlined)
├── Shared overview pages (image/music/video gen)     → note 4 (link → to* notes, planned)
├── Transcription providers                           → note 4 (index → pr* notes, planned)
└── Community tools (Claude Max API Proxy caveat)     → note 4
tools.md
├── (intro: Tools/Skills/Plugins capabilities)        → note 5 (oc_tools_overview)
├── Start here (routing table)                        → note 5
├── Choose tools, skills, or plugins                  → note 5
├── Built-in tool categories (10-row table)           → note 5
├── Plugin-provided tools (api.registerTool)          → note 5
├── Configure access and approvals (policy layers)    → note 5 (link → gw config-tools, gw* planned)
├── Extend capabilities                               → note 5
├── Troubleshoot missing tools (6-step checklist)     → note 5
└── Related                                           → note 5 (link → to*/co*/gw* notes, planned)
vps.md
├── (intro: run Gateway on Linux/VPS)                 → note 6 (oc_vps_linux_server)
├── Pick a provider (10 host cards + AWS)             → note 6 (link → in* notes, planned)
├── How cloud setups work (Gateway owns state)        → note 6
├── Harden admin access first (Tailnet/SSH)           → note 6 (link → oc_web_control_ui + gw/tailscale)
├── Shared company agent on a VPS (trust boundary)    → note 6
├── Using nodes with a VPS                            → note 6 (link → nd01/nd02, cli/nodes, planned)
├── Startup tuning for small VMs and ARM hosts        → note 6
│   └── systemd tuning checklist (optional) [H3]      → note 6
└── Related (install/digitalocean/fly/hetzner)        → note 6
web.md
├── (intro: Control UI on Gateway WS port)            → note 7 (oc_web_control_ui)
├── Webhooks (hooks.enabled endpoint)                 → note 7
├── Admin HTTP RPC (POST /api/v1/admin/rpc)           → note 7 (link → admin-http-rpc, pl/gw planned)
├── Config (default-on, gateway.controlUi)            → note 7
├── Tailscale access [H2]                             → note 7
│   ├── Integrated Serve (recommended) [H3]           → note 7
│   ├── Tailnet bind + token [H3]                     → note 7
│   └── Public internet (Funnel) [H3]                 → note 7
├── Security notes (auth modes, allowedOrigins, TLS)  → note 7
└── Building the UI (pnpm ui:build)                   → note 7
```
No orphaned sections. All down-links (provider/OS/host/tool/gateway/channel/node detail pages) are owned by other sub-plans and linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are ≤1,244 words and single-BB hub/overview pages; each maps cleanly to one `oc_*` note. No page exceeds the 2,500-word cap or mixes building blocks, so no split is warranted. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (4,119 measured words, 17 code fences, 45 H2, 4 H3).
- New `oc_` notes: **7** (1 per page; no splits, no merges).
- New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×5** (notes 1 agent-runtime, 2 platforms, 3 OpenProse, 6 VPS, 7 web) · **concept ×2** (note 4 provider directory, note 5 tools/capabilities routing).
- Est. digest words ~3,520 (avg ~503/note); every note ≤620w and ≤6 code blocks — none near the 2,500w / 400-line / 6-code caps.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_agent_runtime_workflow (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway whose agent runtime this workflow builds/tests; relevance: the note is the developer workflow FOR this product.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the loop that drives an LLM with tools; relevance: OpenClaw's agent runtime IS the harness being unit-tested (`src/agents/*.test.ts`).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that plan/edit/run code; relevance: what the agent runtime executes when triggered via `pnpm openclaw agent`.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — automated build/test gates; relevance: `pnpm check`/`build`/`check && test` are the local landing gates this note codifies.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — per-agent model auth store (API keys + OAuth); relevance: clean-slate reset targets `agent/auth-profiles.json`.
- [LLM](../../term_dictionary/term_llm.md) — the model behind the agent; relevance: `OPENCLAW_LIVE_TEST=1` exercises a real provider/LLM.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary for tool execution; relevance: manual testing prompts `read`/`exec` tool calls whose payloads run under the sandbox.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — saved agent session history/index; relevance: reset deletes `sessions/` + `sessions.json` to wipe session state.

**Docs**
- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — the runtime architecture this workflow validates (planned, this series); relevance: the explicit `## Related` down-link on the source page.
- [oc_web_control_ui](oc_web_control_ui.md) — the gateway-dev web surface (note 7, this series); relevance: `pnpm gateway:dev` serves the Control UI exercised in manual testing.
- [oc_provider_directory](oc_provider_directory.md) — provider/model catalog (note 4, this series); relevance: the live-test step picks a real provider from this directory.
- [band_testing_agents](../band/band_testing_agents.md) — testing strategy for coding-agent adapters; relevance: direct cross-tool analog of the agent-runtime test set + live test.
- [pi_development](../pi/pi_development.md) — Pi local dev/build/test loop; relevance: the sibling coding-agent's equivalent build/test workflow.
- [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — Claude Code programmatic agent runs; relevance: analog of `pnpm openclaw agent --message` triggering the runtime directly.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway-side runtime internals; relevance: explains the `gateway:dev` surface used for manual runtime testing.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — session history storage model; relevance: the analog of the `sessions/`+`sessions.json` state cleared by the reset.
- [hermes_tui_interface](../hermes_agent/hermes_tui_interface.md) — TUI interactive debugging surface; relevance: analog of `pnpm tui` interactive runtime debugging.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — config/state directory + reset semantics; relevance: analog of the `~/.openclaw` state-dir / `OPENCLAW_STATE_DIR` clean-slate reset.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo these `pnpm` gates run in; relevance: the build/test commands operate on this repo.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the `src/agents/*` package; relevance: the exact test globs target this package.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `openclaw onboard`/`gateway`/`agent`/`tui` dev commands; relevance: the manual-testing CLI entry points live here.

**Snippets**
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env + state dir resolution; relevance: implements `OPENCLAW_STATE_DIR`/`~/.openclaw` used by clean-slate reset.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — gateway entry/dispatch; relevance: the `gateway:dev` boot path exercised in manual testing.
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — agent harness transcript handling; relevance: the harness behavior the agent-runtime tests assert.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — auth-profiles + external CLI auth; relevance: the `auth-profiles.json` cleared by reset and kept to preserve auth.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog assembly; relevance: the tools whose `read`/`exec` calls manual testing inspects.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt mode selection; relevance: `--thinking low` and agent modes the runtime tests cover.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — model fallback/cooldown; relevance: behavior the live-provider exercise touches.
- [snippet_hermes_agent_tui_server_agent_build](../../code_snippets/snippet_hermes_agent_tui_server_agent_build.md) — TUI server agent build; relevance: cross-tool analog of `pnpm tui` interactive runtime build.
- [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — code-exec tool result handling; relevance: analog of the `exec` tool streaming/payload manual test.

### oc_platforms_overview (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product whose platform support this page maps; relevance: the note IS OpenClaw's platform overview.
- [TypeScript](../../term_dictionary/term_typescript.md) — OpenClaw core language; relevance: "OpenClaw core is written in TypeScript" is the opening fact.
- [Node.js](../../term_dictionary/term_node_js.md) — the recommended runtime; relevance: "Node is the recommended runtime" (Bun not recommended for the Gateway).
- [npm](../../term_dictionary/term_npm.md) — the Node package ecosystem; relevance: the install/runtime stack behind the TypeScript/Node Gateway.
- [SSH](../../term_dictionary/term_ssh.md) — remote-host access; relevance: VPS/hosting install paths (Fly/Hetzner/GCP/Azure) are administered over SSH.
- [Docker](../../term_dictionary/term_docker.md) — containerized hosting; relevance: Hetzner (Docker) and EasyRunner (Podman+Caddy) hosting links.
- [ARM](../../term_dictionary/term_arm.md) — ARM hosts/companions; relevance: iOS/Android mobile nodes + ARM VPS targets in the OS/hosting picker.
- [Sandbox](../../term_dictionary/term_sandbox.md) — companion-app capability boundary; relevance: companion apps (Windows Hub, macOS menu-bar, mobile nodes) run with scoped local capabilities.

**Docs**
- [oc_vps_linux_server](oc_vps_linux_server.md) — the VPS/hosting hub (note 6, this series); relevance: the "VPS and hosting" section links straight to it.
- [oc_web_control_ui](oc_web_control_ui.md) — Gateway web surface (note 7, this series); relevance: cross-link from the Gateway runbook/configuration common-links.
- [oc_agent_runtime_workflow](oc_agent_runtime_workflow.md) — runtime build/test (note 1, this series); relevance: same TypeScript/Node toolchain the platform install delivers.
- [hermes_installation](../hermes_agent/hermes_installation.md) — sibling-tool install overview; relevance: direct analog of the OS picker + install paths.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — gateway service install/profiles; relevance: analog of the four Gateway-service install paths + per-OS service targets.
- [hermes_install_windows_wsl2](../hermes_agent/hermes_install_windows_wsl2.md) — Windows WSL2 install; relevance: the page's "WSL2 for the most Linux-compatible Gateway runtime" guidance.
- [hermes_windows_native_runtime](../hermes_agent/hermes_windows_native_runtime.md) — native Windows runtime; relevance: the page's "native PowerShell install" + Scheduled-Task service target.
- [hermes_desktop_app](../hermes_agent/hermes_desktop_app.md) — desktop companion app; relevance: analog of Windows Hub / macOS menu-bar companion apps.
- [pi_platform_windows_termux](../pi/pi_platform_windows_termux.md) — Pi platform/Termux runtime; relevance: sibling coding-agent's per-platform runtime picker.
- [band_adapter_setup](../band/band_adapter_setup.md) — adapter/runtime setup; relevance: cross-tool analog of choosing the runtime + install path.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — Windows Hub / macOS menu-bar companion apps; relevance: the companion apps this page lists.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `onboard`/`gateway install`/`configure`/`doctor`; relevance: the four service-install CLI paths.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — core TypeScript Gateway; relevance: the Node-runtime core the page recommends.

**Snippets**
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — renders/parses the systemd user unit; relevance: Linux/WSL2 service target `openclaw-gateway[-profile].service`.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger + env for the user service; relevance: the systemd user-service install path.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — macOS LaunchAgent restart; relevance: the macOS LaunchAgent service target `ai.openclaw.gateway`.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — Windows Scheduled-Task argv render; relevance: the native-Windows Scheduled-Task service target.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: `openclaw onboard --install-daemon` config flow.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: the `openclaw` CLI entry behind `gateway install`/`configure`/`doctor`.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root/privilege guard; relevance: service install permission handling per OS.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — sibling-tool systemd install; relevance: analog of the systemd user-service install.
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — doctor repair primitives; relevance: analog of `openclaw doctor` install/fix-service flow.

### oc_openprose_workflow (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: OpenProse ships as an OpenClaw plugin with a `/prose` command.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple coordinated agents; relevance: OpenProse is a markdown-first multi-agent workflow format.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: `.prose` programs spawn sub-agents via `sessions_spawn`.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agent control flow; relevance: `.prose` uses explicit parallel/sequential steps.
- [Orchestration](../../term_dictionary/term_orchestration.md) — workflow control-flow coordination; relevance: OpenProse orchestrates AI sessions with explicit control flow.
- [Markdown](../../term_dictionary/term_markdown.md) — the `.prose` source format; relevance: OpenProse is "markdown-first" — programs are markdown files.
- [Skills](../../term_dictionary/term_skills.md) — `SKILL.md` instruction packs; relevance: OpenProse installs an OpenProse skill pack.
- [PostgreSQL](../../term_dictionary/term_postgresql.md) — relational state backend; relevance: the postgres (experimental) state backend (credentials flow into sub-agent logs).
- [Fan-Out](../../term_dictionary/term_fan_out.md) — parallel task spread; relevance: the `parallel:` block fans research/writer agents out concurrently.

**Docs**
- [oc_tools_overview](oc_tools_overview.md) — tools/skills/plugins routing (note 5, this series); relevance: the tool allowlist that gates `sessions_spawn`/`read`/`write`/`web_fetch` for `.prose`.
- [oc_subagents](oc_subagents.md) — native multi-agent coordination (to* series, planned); relevance: the explicit `## Related` "Subagents" down-link.
- [oc_skills](oc_skills.md) — skill load/gating reference (to* series, planned); relevance: the `## Related` "Skills reference" down-link for how the OpenProse skill pack loads.
- [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — parallel agent runs; relevance: direct analog of the parallel-research-and-synthesis example.
- [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — orchestrating agent teams; relevance: analog of OpenProse's multi-agent control flow.
- [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — programmatic workflow definition; relevance: analog of authoring reusable `.prose` programs.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — sub-agent delegation; relevance: analog of `sessions_spawn` delegating to researcher/writer agents.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation/parallel patterns; relevance: analog of OpenProse parallel/sequential step patterns.
- [hermes_kanban_worker_orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — orchestrator over worker lanes; relevance: analog of the OpenProse orchestrator spawning parallel sub-agent lanes.
- [pi_sdk_overview](../pi/pi_sdk_overview.md) — sibling-tool SDK/plugin model; relevance: analog of OpenProse shipping as a plugin/extension on the host runtime.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — the skill-pack load path; relevance: where the OpenProse skill pack registers.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension host; relevance: OpenProse installs as the `open-prose` plugin.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/spawn model; relevance: `sessions_spawn` maps to this package.

**Snippets**
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn policy; relevance: enforces the `sessions_spawn` allowlist `.prose` depends on.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ACP sub-agent spawn; relevance: the spawn path behind OpenProse's `session:` steps.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — spawn capability caps; relevance: caps the tools a spawned `.prose` sub-agent may use.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — spawn thread binding; relevance: binds spawned `.prose` sub-agent sessions to threads.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — session handoff on spawn; relevance: hands findings/draft bindings between parallel `.prose` agents.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: how `open-prose` is enabled + loaded after gateway restart.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate/spawn tool; relevance: cross-tool analog of `sessions_spawn` sub-agent delegation.
- [snippet_hermes_agent_skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — multi-agent orchestrator skill; relevance: analog of an orchestrating `.prose` program.
- [snippet_wf_result_aggregation_summary](../../code_snippets/snippet_wf_result_aggregation_summary.md) — aggregating sub-agent results; relevance: analog of the final `session` merging `findings` + `draft`.

### oc_provider_directory (10t · 10s · 10d)

**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language models; relevance: the directory fronts 50+ LLM providers.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: the page is OpenClaw's provider catalog.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that adds a model provider; relevance: each catalog entry is a provider plugin.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — enumerated models per provider; relevance: this note indexes the per-provider model catalog.
- [Bedrock](../../term_dictionary/term_bedrock.md) — Amazon Bedrock; relevance: an explicit catalog entry (Amazon Bedrock + Bedrock Mantle).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic Claude models; relevance: the quick-start default `anthropic/claude-opus-4-6`.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio transcription; relevance: the Transcription providers section (Deepgram, ElevenLabs, …).
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — voice/media generation; relevance: shared media-generation overview pages (image/music/video + voice).
- [Model Router](../../term_dictionary/term_model_router.md) — unified multi-provider gateway; relevance: LiteLLM, OpenRouter, Vercel/Cloudflare AI Gateway entries route across providers.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming STT; relevance: the transcription-provider entries cover realtime audio.

**Docs**
- [oc_tools_overview](oc_tools_overview.md) — capabilities routing (note 5, this series); relevance: shared `image_generate`/`music_generate`/`video_generate` media tools live there.
- [oc_model_providers](oc_model_providers.md) — full provider catalog concept (co* series, planned); relevance: the page's "see Model providers" link for the full catalog.
- [oc_models](oc_models.md) — bundled provider variants (co* series, planned); relevance: the "Additional bundled variants" shared-overview link.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: direct analog of the cloud-LLM provider directory.
- [hermes_provider_aws_bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — Bedrock provider setup; relevance: analog of the Amazon Bedrock catalog entry.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text providers; relevance: analog of the Transcription providers section.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — provider failover; relevance: analog of provider selection + failover across the catalog.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — sibling-tool cloud providers; relevance: analog of choosing/authenticating a model provider.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider authentication; relevance: analog of the "authenticate via `openclaw onboard`" quick-start step.
- [pi_custom_models](../pi/pi_custom_models.md) — local/custom model registration; relevance: analog of the local providers (Ollama/vLLM/LM Studio/SGLang) entries.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-plugin implementations; relevance: the code behind every catalog entry.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — per-provider adapter layer; relevance: cross-tool analog of the provider adapters.

**Snippets**
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider impl; relevance: implements the default `anthropic/...` catalog entry.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider impl; relevance: implements the OpenAI (API + Codex) catalog entry.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: implements the OpenRouter unified-gateway entry.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: implements the local-models (Ollama) entry.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model-catalog manifest planner; relevance: builds the `provider/model` catalog this page indexes.
- [snippet_hermes_agent_core_bedrock_adapter_discovery](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_discovery.md) — Bedrock model discovery; relevance: analog of the Amazon Bedrock catalog entry.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: analog of the transcription-provider entries.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-generation dispatch; relevance: analog of the shared `image_generate` media overview.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: analog of community/custom provider registration.

### oc_tools_overview (10t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: the page is OpenClaw's capabilities routing surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — typed model function calls; relevance: "visible tools are sent to the model as structured function definitions".
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registered tool catalog; relevance: plugin authors wire tools via `api.registerTool` + manifest `contracts.tools`.
- [Skills](../../term_dictionary/term_skills.md) — `SKILL.md` instruction packs; relevance: the tools-vs-skills-vs-plugins decision framework.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin authoring surface; relevance: the page routes plugin-provided tools to the Plugin SDK.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest metadata; relevance: tools are declared in the manifest's `contracts.tools`.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the tool/capability protocol analog for callable typed actions.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: sandbox state is one policy layer that gates which tools the model sees.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: the Sessions-and-agents tool category (`subagents`, `sessions_*`).
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — driving a browser; relevance: the `browser` built-in tool category.

**Docs**
- [oc_openprose_workflow](oc_openprose_workflow.md) — markdown multi-agent workflow (note 3, this series); relevance: depends on the tool allowlist this page documents.
- [oc_config_tools](oc_config_tools.md) — canonical tool policy reference (gw* series, planned); relevance: the page's primary "Tools and custom providers" down-link.
- [oc_sandbox_vs_tool_policy](oc_sandbox_vs_tool_policy.md) — sandbox vs tool policy vs elevated (gw* series, planned); relevance: the "which layer controls access" down-link.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool categories; relevance: direct analog of the built-in tool-category table.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — MCP tool integration; relevance: analog of MCP-style typed callable actions.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin component surfaces; relevance: analog of plugin-provided tools/skills/channels/providers.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — permission precedence; relevance: analog of the allow/deny + profile policy stack enforced before the model call.
- [hermes_tools_reference_core](../hermes_agent/hermes_tools_reference_core.md) — core tools reference; relevance: analog of the representative built-in tools list.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin capability surfaces; relevance: analog of "plugins add tools/providers/channels/hooks/skills".
- [hermes_tools_toolsets](../hermes_agent/hermes_tools_toolsets.md) — toolset grouping/policy; relevance: analog of tool categories + allow/deny grouping.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — tool policy enforcement core; relevance: enforces profile/allow-deny/sandbox before the model call.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin-provided tools host; relevance: where `api.registerTool` plugins live.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill load path; relevance: how `SKILL.md` packs load into the agent prompt.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog assembly; relevance: builds the visible tool set sent to the model.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy; relevance: implements the profile/allow/deny policy this page describes.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny list; relevance: the deny-policy layer that removes a tool before the turn.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: plugin-availability gate on whether a plugin's tools are exposed.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: sandbox + exec-approval layer in the tool-policy stack.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — permission relay; relevance: relays tool approvals before a call proceeds.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: channel/runtime policy that can lose a tool for the turn.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: cross-tool analog of `api.registerTool`/`contracts.tools`.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — skills gating guard; relevance: analog of skill load gating in the capabilities stack.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: analog of the "configure access and approvals" exec-approval policy.

### oc_vps_linux_server (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the Gateway run on the VPS; relevance: the note is "run the OpenClaw Gateway on a Linux/VPS".
- [SSH](../../term_dictionary/term_ssh.md) — secure remote shell; relevance: SSH tunnel / Tailnet-only SSH is the admin-access hardening core.
- [ARM](../../term_dictionary/term_arm.md) — ARM CPU hosts; relevance: Oracle Always-Free ARM, Raspberry Pi, + the "ARM hosts" startup-tuning section.
- [Docker](../../term_dictionary/term_docker.md) — container hosting; relevance: Hetzner (Docker) host card + containerized deployment.
- [Node.js](../../term_dictionary/term_node_js.md) — the Gateway runtime; relevance: `NODE_COMPILE_CACHE` startup tuning targets Node's module compile cache.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/trust analysis; relevance: the shared-company-agent trust-boundary guidance.
- [Sandbox](../../term_dictionary/term_sandbox.md) — runtime isolation; relevance: "keep it on a dedicated runtime + dedicated OS user" isolation for shared agents.
- [LLM](../../term_dictionary/term_llm.md) — the model the agent runs; relevance: the cloud Gateway hosts the agent/LLM that owns state on the VPS.

**Docs**
- [oc_web_control_ui](oc_web_control_ui.md) — Control UI + Tailscale access (note 7, this series); relevance: the documented way to reach the cloud Gateway dashboard.
- [oc_platforms_overview](oc_platforms_overview.md) — platform/hosting hub (note 2, this series); relevance: the "Platforms hub" related link + hosting links.
- [oc_nodes](oc_nodes.md) — pairing local nodes (nd* series, planned); relevance: the "Using nodes with a VPS" section links to Nodes docs.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops on a server; relevance: analog of running/operating the Gateway on a Linux host.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation + credential hygiene; relevance: analog of the shared-company-agent dedicated-runtime isolation.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Docker run modes; relevance: analog of the Hetzner/containerized hosting path.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth over SSH tunnel; relevance: analog of SSH-tunnel access to a loopback-bound Gateway.
- [pi_containerization](../pi/pi_containerization.md) — sibling-tool containerized hosting; relevance: analog of running the agent in a container/VPS.
- [pi_terminal_setup](../pi/pi_terminal_setup.md) — terminal/server setup; relevance: analog of generic Linux-server setup for the agent.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents; relevance: cross-tool analog of deploying the agent runtime on a server.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service hardened/tuned here; relevance: the service this page runs on the VPS.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — trust-boundary/hardening model; relevance: the security model behind admin hardening + shared-agent boundaries.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `onboard --install-daemon` systemd unit; relevance: the standard install path the systemd tuning edits.

**Snippets**
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: the `openclaw-gateway.service` user unit the tuning checklist edits.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger + env; relevance: `Environment=OPENCLAW_NO_RESPAWN=1`/`NODE_COMPILE_CACHE` service env.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — restart handoff; relevance: the `OPENCLAW_NO_RESPAWN` in-process restart behavior on small hosts.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — gateway startup attach; relevance: the cold-start path the compile-cache tuning speeds up.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: the token/password auth required when binding to lan/tailnet.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: governs `system.run`/node capabilities when pairing nodes to a VPS.
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — restricted shell; relevance: the dedicated-runtime/least-privilege admin posture.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — sibling systemd install; relevance: analog of the systemd-managed Gateway with explicit restart policy.

### oc_web_control_ui (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the Gateway serving these surfaces; relevance: the note is OpenClaw's Gateway web surfaces.
- [WebSocket](../../term_dictionary/term_websocket.md) — the Gateway WS protocol; relevance: the Control UI is served from the same port as the Gateway WebSocket (`:18789`).
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP event endpoint; relevance: the `hooks.enabled` webhook endpoint on the same HTTP server.
- [Authentication](../../term_dictionary/term_authentication.md) — request auth; relevance: token/password/trusted-proxy/Tailscale-identity auth model (non-loopback always requires auth).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: Tailscale Serve + `trusted-proxy` identity-aware reverse proxy.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — control-plane HTTP surface; relevance: Admin HTTP RPC at `POST /api/v1/admin/rpc`.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: `gateway.tls.enabled` → `https://`/`wss://` URLs.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC method surface; relevance: Admin HTTP RPC's method-call surface vs the WebSocket.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer-style token auth; relevance: the shared-secret gateway token the wizard generates for Control UI auth.

**Docs**
- [oc_vps_linux_server](oc_vps_linux_server.md) — Linux/VPS hosting (note 6, this series); relevance: remote access to this Control UI from a cloud Gateway.
- [oc_agent_runtime_workflow](oc_agent_runtime_workflow.md) — runtime build/test (note 1, this series); relevance: `pnpm ui:build` builds the Control UI assets.
- [oc_tailscale](oc_tailscale.md) — Tailscale Gateway options (gw* series, planned); relevance: the `## Related` Tailscale down-link for Serve/tailnet/Funnel.
- [oc_admin_http_rpc](oc_admin_http_rpc.md) — Admin HTTP RPC reference (pl/gw series, planned); relevance: the Admin-HTTP-RPC auth model + allowed-methods down-link.
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — web dashboard/Control UI; relevance: direct analog of the browser Control UI.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: analog of token/password auth for non-loopback dashboard access.
- [hermes_api_server_setup_auth](../hermes_agent/hermes_api_server_setup_auth.md) — API server auth setup; relevance: analog of the Admin HTTP RPC + gateway auth surface.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS + network access; relevance: analog of `tls.enabled` → `wss://` + allowed-origins access control.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: analog of the trusted-proxy / reverse-proxy bind config.
- [band_websocket_overview](../band/band_websocket_overview.md) — websocket channel overview; relevance: cross-tool analog of the Gateway WebSocket the Control UI shares.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — serves the Control UI + auth + bind modes; relevance: the gateway implementing every surface on this page.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the Vite+Lit Control UI front-end; relevance: the UI built by `pnpm ui:build`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/origin/TLS security model; relevance: the security-notes model (allowedOrigins, host-header fallback, identity headers).

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: implements token/password/trusted-proxy/Tailscale auth modes.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: enforces "non-loopback binds require auth" on each request.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: the `connect.params.auth.token`/`password` flow the UI sends.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS; relevance: Tailscale/`trusted-proxy` identity-header auth + `wss://` TLS.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect via proxy; relevance: the Tailscale Serve / reverse-proxy connection path.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: serves Control UI, webhooks, and WS on the same `:18789` port.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method gating; relevance: gates the Admin-HTTP-RPC / control-plane methods.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup; relevance: the wizard-generated default shared-secret auth on startup.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — gateway TLS pinning; relevance: the TLS layer behind `https://`/`wss://`.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — webhook endpoint; relevance: cross-tool analog of the `hooks.enabled` webhook surface.


## Undigested Terms Plan

> Per master: OpenClaw vocabulary is digested as `oc_*` doc notes (its home is a doc page), NOT promoted to `term_dictionary`. The only `term_dictionary` interaction is **linking existing** terms. Expected new captures: **0**.

| Term / vocabulary item | Disposition |
|---|---|
| OpenProse, `.prose`, `/prose` slash command | Digested in note 3 (`oc_openprose_workflow`); OpenClaw-product vocabulary → `oc_*` doc note, not a term. Link `term_multi_agent`/`term_markdown`/`term_orchestration`. |
| Control UI, bind modes, Funnel/Serve | Digested in note 7 (`oc_web_control_ui`); product vocabulary → `oc_*` note. Link `term_websocket`/`term_authentication`/`term_reverse_proxy`. |
| Built-in tools, tool policy, skills-vs-plugins | Digested in note 5 (`oc_tools_overview`); routing-page vocabulary → `oc_*` note. Link `term_function_calling`/`term_tool_registry`/`term_skills`. |
| Provider directory, `provider/model` | Digested in note 4 (`oc_provider_directory`); product vocabulary → `oc_*` note. Provider names (Anthropic, Bedrock, Groq, …) are config values, NOT terms — link `term_llm`/`term_provider_plugin`/`term_bedrock`/`term_claude`. |
| Gateway service install (LaunchAgent/systemd/Scheduled Task) | Digested in note 2 (`oc_platforms_overview`); platform vocabulary → `oc_*` note. OS/service-target names are config, not terms. Link `term_node_js`/`term_typescript`. |
| Agent runtime, clean-slate reset, `~/.openclaw` state | Digested in note 1 (`oc_agent_runtime_workflow`); product vocabulary → `oc_*` note. Link `term_agent_harness`/`term_auth_profile`. |
| VPS hosting, nodes, ARM/startup tuning | Digested in note 6 (`oc_vps_linux_server`); host/product vocabulary → `oc_*` note. Host names (Railway, Hetzner, …) are config. Link `term_ssh`/`term_arm`/`term_docker`. |

**New `term_dictionary` captures planned: 0.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note was found. (If augment's Step 2d re-scan surfaces one — unlikely — the best-fit glossary would be `0_entry_points/acronym_glossary_tools.md` or `acronym_glossary_workflows.md`.)

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). Gate table inherited verbatim from the master 9-GATE definition.

| Gate | Check | Tool / Method | Pass criterion |
|------|-------|---------------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | YAML field order + forbidden-field absence; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` + `## References` + bold footer present; one `building_block`. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/<page>.md` | every claim traceable to the source page; no invented config/flags. |
| G3 | Density + Coverage | line/word/code count + Section Coverage Map | ≤400 lines, ≤2,500 words, ≤6 code blocks; every mapped H2/H3 covered, no orphan. |
| G4 | Cross-Reference | `## Related Notes` link audit | ≥6 relevance-selected term links + sibling `oc_*` + `repo_openclaw*` + other vault notes, each with a relevance statement; correct indexed `[text](path.md)` format. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + reindex | 0 broken links after incremental reindex. |
| G7/G8 | Discoverability / in-degree | `note_links` query | every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks); in-degree ≥1; anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_agent_runtime_workflow oc_platforms_overview oc_openprose_workflow oc_provider_directory oc_tools_overview oc_vps_linux_server oc_web_control_ui"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format + broken-link gate
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G1 required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density (strip frontmatter for word count)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4 sibling cross-ref present
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING $SIBLING_PREFIX LINK: $n"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference DB-verify (per note_id cited in Related Notes/References)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤400L / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_agent_runtime_workflow | procedure | 380 | 2 | ✅ |
| 2 | oc_platforms_overview | procedure | 360 | 0 | ✅ |
| 3 | oc_openprose_workflow | procedure | 560 | 4 | ✅ |
| 4 | oc_provider_directory | concept | 380 | 1 | ✅ |
| 5 | oc_tools_overview | concept | 620 | 0 | ✅ |
| 6 | oc_vps_linux_server | procedure | 620 | 3 | ✅ |
| 7 | oc_web_control_ui | procedure | 600 | ≤6 | ✅ (source has 7 fences; reproduce ≤6 — combine the two `openclaw gateway` start snippets / keep the json5 config blocks, drop one duplicate start command) |

No note approaches the caps. Only `web.md` has >6 raw fences (7); note 7 reproduces config blocks selectively to stay ≤6 (the two identical `openclaw gateway` start commands collapse to one).

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify exact paths at execution; all listed sources confirmed to exist 2026-06-20):

- `entry_openclaw_docs.md` (planned, master W1) → all 7 notes (primary discoverability path).
- `repo_openclaw.md` → notes 1, 5, 6, 7 (core runtime / tools / gateway).
- `repo_openclaw_gateway.md` → notes 6, 7 (VPS hosting + Control UI).
- `repo_openclaw_extensions_llm_providers.md` → note 4 (provider directory).
- `repo_openclaw_extensions.md` → notes 3, 5 (OpenProse plugin + plugin-provided tools).
- `repo_openclaw_apps.md` → notes 2, 7 (companion apps + Control UI).
- `repo_openclaw_skills.md` → notes 3, 5 (skill pack + skills).
- `term_openclaw.md` → all 7 notes (master W3 adds the docs-hub link; per-note links optional).
- `term_llm.md` → note 4; `term_function_calling.md` → note 5; `term_multi_agent.md` → note 3; `term_node_js.md` → notes 2, 6; `term_websocket.md` → note 7.

## Pacing Rules (inherited from master)

One execution phase (7 notes ≤30 fan-out cap). All 8 gates pass before commit. Re-read each source page during execution; reproduce config/CLI snippets verbatim. One BB per note. `git pull --rebase --autostash` first; commit + push after the phase; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (per-note Related mapping LOCKED at ≥8t · ≥10s · ≥10d) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 checkpoints PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Per-note locked counts (terms / snippets / docs / repos · floorsMet):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_agent_runtime_workflow | 8 | 10 | 10 (7 existing / 3 planned) | 3 | YES |
| oc_platforms_overview | 8 | 10 | 10 (7 existing / 3 planned) | 3 | YES |
| oc_openprose_workflow | 9 | 10 | 10 (7 existing / 3 planned) | 3 | YES |
| oc_provider_directory | 10 | 10 | 10 (7 existing / 3 planned) | 3 | YES |
| oc_tools_overview | 10 | 10 | 10 (7 existing / 3 planned) | 3 | YES |
| oc_vps_linux_server | 8 | 10 | 10 (7 existing / 3 planned) | 3 | YES |
| oc_web_control_ui | 9 | 10 | 10 (6 existing / 4 planned) | 3 | YES |


**New-term candidates + best-fit glossary.** **None.** Consistent with the master design decision (OpenClaw vocabulary is digested as `oc_*` doc notes, never promoted to `term_dictionary`). The augment re-read (Step 2d) surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. Intuitive slugs probed during xref selection and confirmed NONEXISTENT — `term_session`, `term_node`, `term_tailscale`, `term_workspace`, `term_systemd`, `term_bun`, `term_oauth`, `term_third_party_genai_services` — were NOT cited (verified alternatives substituted: e.g. `term_session_persistence` for session state, `term_oauth_token` for OAuth) and are already recorded in the Undigested Terms Plan. If a future re-scan surfaces a genuine cross-cutting term, the best-fit glossary would be `0_entry_points/acronym_glossary_tools.md` or `acronym_glossary_workflows.md`. **New `term_dictionary` captures planned: 0.**

**Dedup/collision audit (generalized to ALL planned notes).** Each planned `oc_*` slug was checked against `term_dictionary/` AND `resources/documentation/`. No planned `oc_*` doc note duplicates an existing term note or existing doc note — the 7 root-slug hub pages have no existing vault counterpart (the vault's 295 OpenClaw notes are code-side repos/snippets/FZ-15 analysis, complementary not duplicative). Term links are to EXISTING terms only (link, never recreate). No renames or removals required.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-stated) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 7 notes meet ≥8t·≥10s·≥10d; every link rendered `- [Name](relpath.md) — what; relevance: why` with a relevance statement (no bare links). Terms range 8–10/note. |
| CP2 | 9-GATE table present (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-detect+redirect, G6 Broken-link fix, G7/G8 Discoverability/in-degree; `## Validation Scripts` includes G5 ghost DB-verify + G6 + density. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at master W1) | **PASS** | `## Entry Point Decision` inherits master W1 CREATE of `0_entry_points/entry_openclaw_docs.md`; DB-confirmed it does NOT yet exist (correctly planned, not ghost-linked). rt03 contributes 7 rows under a "Top-level / Overview hubs" cluster; each note gets its back-link at finalization (G7/G8). |
| CP4 | Plan size (≤30 or split) | **PASS** | 7 notes — well under the 30-note cap; single execution phase within the ~30-agent fan-out cap. |
| CP5 | Format derived (not invented) | **PASS** | Format inherited from master `## Format Definition`, which is derived from the existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` opener, `## Related Notes` reference section, bold `**Source**`/`**Last Updated**`/`**Status**` footer, forbidden-field list, fixed YAML order). Matches existing target-sibling notes. |
| CP6 | Density / BB atomicity (promote borderline splits) | **PASS** | `## Density Re-Assessment` table: all 7 notes ≤620 words, ≤6 code blocks, single BB; none borderline (>300 est lines / >5 code / >5 H2 with mixed BB). web.md's 7 raw fences → note 7 reproduces ≤6 (collapse duplicate `openclaw gateway` start). No split needed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 2026-06-21 (`sed` strip frontmatter + `wc -w`): tools 1187 (plan 1244, 0.95×), vps 641 (698, 0.92×), web 508 (542, 0.94×), prose 578 (641, 0.90×), providers 344 (375, 0.92×). All within 0.7–1.3× — no under-estimation; no re-split triggered. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (all 7 vocabulary rows owned by their `oc_*` home note; 0 promotions). `## Term-Note Authoring Requirements` present (N/A — 0 new terms; inherits master `/tessellum-capture-term-note` mandate). New captures planned: 0 (consistent with master Pattern: OpenClaw vocab → doc notes). |
| CP8f | Term-slug specificity + all-notes collision/dedup audit | **PASS** | Probed-nonexistent intuitive slugs recorded in Undigested Terms Plan (not cited); collision audit run over ALL planned `oc_*` slugs against `term_dictionary/` AND `documentation/` — 0 duplicates of existing term/doc notes (hub pages have no vault counterpart). All cited terms are EXISTING (link-only). No renames/removals required. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
