---
title: Hermes Agent Docs Digestion — Sub-Plan 03a — Deployment & Platforms
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/
pages:
  - user-guide/docker.md
  - user-guide/windows-native.md
  - user-guide/desktop.md
  - user-guide/windows-wsl-quickstart.md
  - user-guide/git-worktrees.md
---

# Sub-Plan 03a: Deployment & Platforms

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Part **a** of the
> deploy/security split of master SP03 (SP03b owns security.md, checkpoints-and-rollback.md, secrets/*).
> Inherits shared Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP03a's note
> filenames/BBs/coverage are defined.

## Scope

How and where you run Hermes Agent across deployment surfaces: running Hermes **in** Docker (gateway /
dashboard / CLI modes, the `/opt/data` volume, multi-profile s6 supervision, installing tools, local
inference networking), native Windows (PowerShell install + Git Bash + UTF-8 console + Scheduled-Task
gateway), the cross-platform Desktop app (Electron shell + remote-backend connection), the Windows WSL2
path (filesystem/networking boundaries), and git-worktree isolation for parallel agents. Source = 5
mirrored pages in `inbox/hermes_agent_docs/` (all substantive). **P1 / foundational** — downstream
sub-plans link back to `hermes_docker_run_modes`, `hermes_install_windows_native`, and
`term_git_worktree_agents`.

## Content Strategy

- **One BB per note.** `docker.md` mixes run-mode procedures, a volume/supervision model, and a
  tool-install/networking procedure → split into 3 notes (see Split Decisions). `windows-native.md` → 2,
  `desktop.md` → 2, `windows-wsl-quickstart.md` → 1, `git-worktrees.md` → 1.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the
  `terminal.backend: docker` config block + the 6-backend model (SP02 `hermes_terminal_backends`,
  config block detail), the API server feature (SP09 `hermes_api_server`), the web dashboard feature +
  its auth providers (SP10 `hermes_web_dashboard`), voice mode (SP08), checkpoints/rollback + security +
  secrets (SP03b), profiles (SP04 `hermes_profiles`), the providers catalog + WSL2 networking deep-dive
  (SP14/SP15), installation/updating base pages (SP01).
- **Collision (augment): `term_docker.md` (active) is the generic container concept** — the planned
  `hermes_docker_run_modes` etc. are Hermes-specific operational procedures, a different BB scope → LINK,
  do not recreate.
- **Collision: `term_sandbox_backend.md` (active) is the generic concept** — the Docker/SSH/Modal
  execution backends are owned as a model note by SP02 (`hermes_terminal_backends`); SP03a links both,
  recreates neither.
- **Owned NEW term:** `term_git_worktree_agents` (parallel agents via git worktrees) — captured Phase 0
  BEFORE the `hermes_git_worktree_isolation` doc note (Pattern B). Specificity + collision audit performed
  below (no existing `term_worktree`/`term_git_worktree*`; only unrelated `term_git_*`/`term_*_parallelism`).

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/docker.md | 6013 | 36 | MIXED procedure+model+procedure | 3 (split) |
| user-guide/windows-native.md | 3343 | 9 | procedure | 2 (split) |
| user-guide/desktop.md | 3271 | 9 | procedure | 2 (split) |
| user-guide/windows-wsl-quickstart.md | 2928 | 14 | procedure | 1 |
| user-guide/git-worktrees.md | 803 | 7 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_docker_run_modes.md` | procedure | docker §Quick start, §Running in gateway mode, §Running the dashboard, §Running interactively (CLI chat), §Environment variable forwarding, §Docker Compose example, §Upgrading, §Resource limits | ~1500 | Running Hermes IN Docker: first-run `setup` wizard against a mounted `~/.hermes`, persistent `gateway run` (port 8642 API + `--restart unless-stopped`), `HERMES_DASHBOARD=1` (port 9119) with the auth-gate providers (link-out SP10), interactive CLI chat, `-e` env forwarding, the canonical `docker-compose.yaml`, image-pull upgrade with auto config migration, resource sizing. |
| 2 | `hermes_docker_volumes_supervision.md` | model | docker §Persistent volumes, §Multi-profile support (+Reaching profiles from outside, Why one container, When separate, Per-profile supervision), §Where the logs go, §What the Dockerfile does (+`docker exec` drops to hermes user), §Skills and credential files | ~1900 | The Docker runtime model: the single `/opt/data` volume as source of truth (config/keys/sessions/skills/SOUL.md/home), s6-overlay as PID 1 supervising per-profile gateway services with state-persistent auto-restart, the four log surfaces + boot reconciler, the non-root `hermes` UID-10000 privilege model + `docker exec` shim, and per-profile vs per-container tradeoffs. |
| 3 | `hermes_docker_tools_local_inference.md` | procedure | docker §Installing more tools in the container (npx/uvx, apt, derived image, sidecar, upstream PR), §Connecting to local inference servers (Compose, standalone, verifying, Ollama), §Optional: Linux desktop audio bridge, §Troubleshooting | ~1500 | Extending a Docker deployment: five tool-install strategies (`npx`/`uvx` → apt-remember → derived image → sidecar container → upstream), reaching vLLM/Ollama by container-name vs `host.docker.internal` vs `--network host`, the PulseAudio voice-mode audio bridge, and the container troubleshooting matrix (exits, permissions, `--shm-size`, reconnect). |
| 4 | `hermes_install_windows_native.md` | procedure | windows-native §Quick install (+Desktop installer, dep_ensure), §What the installer actually does, §Running the gateway at Windows login (install/manage/why not a service), §Data layout, §Uninstall, §Where to go next | ~1500 | Native Windows install: the PowerShell `irm | iex` one-liner (no admin), installer parameters, the 10-step bootstrap (`uv`/Python 3.11/Node 22/PortableGit/tiered pip/messaging SDKs/PATH), `dep_ensure` lazy non-Python deps, the gateway as a `schtasks /SC ONLOGON` task spawned detached via `pythonw.exe`, the `%LOCALAPPDATA%\hermes` data layout, and clean uninstall. |
| 5 | `hermes_windows_native_runtime.md` | procedure | windows-native §Feature matrix, §How Hermes runs shell commands on Windows (Git Bash resolution), §UTF-8 console on Windows, §The editor, §`Ctrl+Enter` for newline, §Browser tool, §Running Hermes on Windows — practical notes (PATH/env/Windows-specific env), §Process management internals, §Common pitfalls | ~1500 | The native-Windows runtime surface: the native-vs-WSL2 feature matrix (only the dashboard PTY terminal is WSL-only), Git Bash `bash.exe` resolution order, the `configure_windows_stdio` UTF-8/CP65001 shim + `EDITOR=notepad` default, `Ctrl+Enter` newline, `agent-browser` `.cmd` resolution, Windows env vars, the `os.kill(pid,0)`→`CTRL_C_EVENT` footgun (use `psutil.pid_exists`), and the common-pitfalls table. |
| 6 | `hermes_desktop_app.md` | procedure | desktop §(intro), §Install, §What's in the app (Chat/status bar/file browser/voice/settings/management/keyboard/sessions), §Updating, §Uninstalling, §CLI reference `hermes desktop`, §How it works, §Building from source, §See also | ~1500 | The cross-platform Desktop app: a native Electron front-end over the **same** agent core (shared config/keys/sessions/skills), `hermes desktop` launch + flags, the chat-first window (streaming, preview rail, inline model picker, per-session YOLO), Skills/Cron/Profiles/Agents panes, three-tier uninstall, `HERMES_HOME` first-launch runtime install, and the dev/build-from-source workflow. |
| 7 | `hermes_desktop_remote_backend.md` | procedure | desktop §Connecting to a remote backend (pick a provider, On the backend, In the app, Troubleshooting), §Troubleshooting (boot logs, Electron download/mirror, resets) | ~1300 | Pointing the Desktop app at a remote `hermes dashboard` backend: the auth gate engaged by a non-loopback bind, OAuth (Nous Portal) for public hosts vs username/password (`HERMES_DASHBOARD_BASIC_AUTH_*` + stable `_SECRET`) for trusted LAN/Tailscale, the in-app Remote-URL + sign-in flow, per-profile remote hosts, the `desktop.log` + Electron-mirror (`ELECTRON_MIRROR`) troubleshooting, and 401/connection-refused triage. |
| 8 | `hermes_install_windows_wsl2.md` | procedure | windows-wsl-quickstart §(intro/when to pick), §Why WSL2, §Install WSL2 (distro/systemd), §Install Hermes inside WSL, §Filesystem boundary (two directions/where to put/getting files/line endings/clone), §Networking (Case 1/Case 2 subcases), §Running long-term (shortcut/systemd/login), §GPU passthrough, §Common pitfalls | ~1700 | The Windows WSL2 path: when to pick WSL2 (dashboard PTY terminal, POSIX dev) vs native, `wsl --install` + WSL2 verification + systemd enablement, installing Hermes as plain Linux, the Windows↔WSL filesystem boundary (keep everything Linux-side; 9P perf/permission/inotify costs), bidirectional networking (mirrored vs NAT, `netsh portproxy`), keeping the gateway alive (systemd user unit + Task Scheduler), NVIDIA GPU passthrough, and the pitfalls table. |
| 9 | `hermes_git_worktree_isolation.md` | procedure | git-worktrees §(intro), §Why Use Worktrees with Hermes, §Quick Start: Creating a Worktree, §Running Multiple Agents in Parallel, §Cleaning Up Worktrees Safely, §Best Practices, §Using `hermes -w` (Automatic Worktree Mode), §Putting It All Together | ~800 | Running multiple Hermes agents safely on one repo via git worktrees: each worktree gives an agent its own branch, working dir, and shadow-repo checkpoint history (hash derived from the worktree path); `git worktree add` for manual isolation, `hermes -w` for a disposable auto-worktree under `.worktrees/`, parallel agents in separate terminals, safe cleanup, and worktree + branch + checkpoint best practices. |

**SP03a totals:** 9 notes · procedure 8 · model 1 · concept 0 (concepts owned by existing/owned term notes).
5 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 9 · procedure 8 · model 1 · concept 0 (the container/sandbox/worktree concepts are term notes —
  `term_docker`, `term_sandbox_backend` existing; `term_git_worktree_agents` owned by this SP).
- Source: 5 digested pages (~15.9K words) → ~13.2K words of notes (modest compression via link-outs).
- BB mix: procedure 89%, model 11%.
- New term notes owned: **1** (`term_git_worktree_agents`). Existing terms linked: many (see mapping).

## Section Coverage Map

```
docker.md (6013w)
├── intro (two ways docker intersects) ────────────────────── → Note 1 (terminal-backend block→SP02)
├── Quick start / Running in gateway mode / Running the dashboard → Note 1 (dashboard auth providers→SP10)
├── Running interactively (CLI chat) / Environment variable forwarding → Note 1
├── Docker Compose example / Upgrading / Resource limits ───── → Note 1 (updating base→SP01)
├── Persistent volumes ────────────────────────────────────── → Note 2
├── Multi-profile support (+reach from outside, why one, when separate, per-profile supervision) → Note 2 (profiles→SP04)
├── Where the logs go ─────────────────────────────────────── → Note 2
├── What the Dockerfile does (+docker exec drops to hermes user) → Note 2
├── Skills and credential files ───────────────────────────── → Note 2 (skills→SP05)
├── Installing more tools in the container (5 strategies) ──── → Note 3
├── Connecting to local inference servers (Compose/standalone/verify/Ollama) → Note 3 (providers→SP14)
├── Optional: Linux desktop audio bridge ──────────────────── → Note 3 (voice mode→SP08)
└── Troubleshooting ───────────────────────────────────────── → Note 3
windows-native.md (3343w)
├── intro / Quick install (+Desktop installer, dep_ensure) ── → Note 4
├── What the installer actually does ──────────────────────── → Note 4
├── Running the gateway at Windows login (install/manage/why-not-service) → Note 4
├── Data layout / Uninstall / Where to go next ────────────── → Note 4 (installation base→SP01)
├── Feature matrix ────────────────────────────────────────── → Note 5 (dashboard PTY→SP10; WSL→Note 8)
├── How Hermes runs shell commands (Git Bash resolution) ──── → Note 5
├── UTF-8 console / The editor / Ctrl+Enter newline ───────── → Note 5
├── Browser tool / Practical notes (PATH/env/Windows env) ──── → Note 5 (browser→SP08)
├── Process management internals ──────────────────────────── → Note 5
└── Common pitfalls ───────────────────────────────────────── → Note 5
desktop.md (3271w)
├── intro / which interface is which ──────────────────────── → Note 6 (TUI→SP02; web-dashboard→SP10)
├── Install / What's in the app (Chat/status bar/file browser/voice/settings/management/keyboard/sessions) → Note 6 (voice→SP08; skills→SP05; cron→SP06; profiles→SP04)
├── Updating / Uninstalling / CLI reference `hermes desktop` ── → Note 6 (updating→SP01)
├── How it works / Building from source / See also ────────── → Note 6
├── Connecting to a remote backend (provider/backend/app/troubleshoot) → Note 7 (dashboard auth→SP10; env vars→SP21)
└── Troubleshooting (boot logs/Electron download/resets) ───── → Note 7
windows-wsl-quickstart.md (2928w) ── ALL sections ─────────────── → Note 8 (providers WSL2 networking→SP14; MCP chrome→SP17; webhooks→SP12; api-server→SP09; tool-gateway→SP05)
git-worktrees.md (803w) ── ALL sections ──────────────────────── → Note 9 (checkpoints/rollback→SP03b)
```

No source H2/H3 orphaned. All 5 pages fully covered; feature-page detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| docker.md (6013w, 36 code, MIXED) | Note 1 (run modes, proc) + Note 2 (volumes/supervision/Dockerfile, model) + Note 3 (tool installs/local inference/audio/troubleshoot, proc) | >4000w → 3 notes; the volume layout + s6 supervision + privilege model is a distinct `model` BB, separate from the run-mode procedure and the tool-extension procedure; 36 source code blocks curated to ≤6 per note. |
| windows-native.md (3343w, 9 code) | Note 4 (install + gateway-at-login + data layout + uninstall) + Note 5 (runtime: feature matrix/Git Bash/UTF-8/editor/browser/pitfalls/internals) | >2500w; two arcs — the install/deploy procedure vs the day-to-day runtime/troubleshooting surface. |
| desktop.md (3271w, 9 code) | Note 6 (app overview: install/UI/uninstall/build) + Note 7 (remote-backend connection + troubleshooting) | >2500w; the local app surface vs the distinct remote-`hermes dashboard` connection + auth procedure. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note / slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_docker_run_modes`, `hermes_docker_volumes_supervision`, `hermes_docker_tools_local_inference` | `term_docker` (active) | **NOT a dup** — `term_docker` is the generic container concept; these are Hermes-specific deploy procedures + a runtime model | CREATE; LINK `term_docker`. |
| `hermes_docker_volumes_supervision`, `hermes_install_windows_native` | `term_sandbox_backend` (active); SP02 `hermes_terminal_backends` (model, planned) | **NOT a dup** — the execution-backend model is owned by SP02; these document the *deployment* surface | CREATE; LINK `term_sandbox_backend` + (at finalization) `hermes_terminal_backends`. |
| `hermes_install_windows_native`, `hermes_windows_native_runtime`, `hermes_install_windows_wsl2`, `hermes_desktop_app`, `hermes_desktop_remote_backend`, `hermes_git_worktree_isolation` | no substantive term/doc note covers these procedures; no `hermes_agent/` doc notes exist yet (DB confirmed empty) | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0 substantive
same-concept duplicates** (the `term_docker`/`term_sandbox_backend` hits are LINK-not-dup; the git-term hits are
different concepts, confirmed by reading the slugs). New `hermes_agent/` folder → no doc-doc collisions (intra-series
links resolve at finalization). Owned-slug pre-flight: `term_git_worktree_agents` absent → CREATE (full note).

## Per-Note Related Notes Mapping (FINALIZED — FOUR FLOORS: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Four-floor standard set 2026-06-19 (user directive — supersedes both the 2026-06-14 master floor and the
> intermediate 3-floor wording).** Each note's `## Related Notes` carries FOUR COUNTED floors, all
> relevancy-selected and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   the Hermes SOURCE-CODE modules that IMPLEMENT what this doc note documents (the 13 `repo_hermes_agent_*` notes).
>   snippet-level implementation corpus (517 Hermes snippets); pick the ≥10 whose CODE this note documents. This is
>   now a COUNTED floor (promoted 2026-06-19 from the prior "bonus" group and raised from 8 to ≥10 — NO LONGER a bonus).
> - **≥10 documentation notes** (`../../documentation/`) — sibling `hermes_*` notes in THIS series (resolve at
>   active 2026-06-19) + other relevant existing doc notes.
>
> Other-SP / not-yet-existing terms are marked `[own]` in a `(+fin …)` tail and are EXCLUDED from the floor.
> Intra-series sibling `hermes_*` doc links resolve at finalization (G5/G8) and count toward the doc floor;

**Note 1 `hermes_docker_run_modes`**
- Terms (9): term_docker, term_sandbox_backend, term_autonomous_coding_agents, term_agent_harness, term_oauth_token, term_authentication, term_reverse_proxy, term_idempotency, term_health_check — relevance: Hermes-in-Docker is the agent harness packaged as a container; `gateway run` exposes port 8642 (the OpenAI-compatible API server + health endpoint) and the `:9119` dashboard sits behind the OAuth auth gate / reverse-proxy; `hermes setup --portal` does the OAuth login; on-upgrade config-schema migration is idempotent. (+fin: term_nous_portal [own], term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent — the monorepo whose `docker/` tree, Dockerfile, and `main-wrapper.sh` define the `docker run` arg-routing this page drives; repo_hermes_agent_cli — implements `hermes setup` (the first-run wizard), `gateway run`, and the on-upgrade `config` migrations; repo_hermes_agent_gateway_messaging — the `gateway/` package that `gateway run` boots (chat platforms + the API server on 8642); repo_hermes_agent_plugins — the `dashboard_auth/*` `DashboardAuthProvider` plugins (`HERMES_DASHBOARD=1` auth gate); repo_hermes_agent_tui_gateway — the dashboard/web surface reached on `:9119`.
- Docs (11): hermes_docker_volumes_supervision — the `/opt/data` volume + s6 model these run modes persist into; hermes_docker_tools_local_inference — extending the same container; hermes_install_windows_native — the non-Docker deploy alternative; hermes_desktop_remote_backend — points the Desktop app at this container's `:9119` dashboard; hermes_git_worktree_isolation — agent isolation on the same host; hermes_install_windows_wsl2 — sibling deploy surface; cc_sandbox_runtime_and_containers — Claude Code's analogous container-runtime model; cc_devcontainer_setup — analogous container-based agent deploy; cc_execution_environments — analogous run-surface taxonomy; cc_install — analogous first-run install/auth procedure; cc_proxy_and_gateway_config — analogous reverse-proxy / gateway fronting.
- Snippets (11): tools_environments_docker, gw_start_gateway_main, gw_runner_supervisor, cli_setup_wizard, cli_config_migrate, plugins_example_dashboard, gw_platform_api_server_routes, core_logging_setup, gw_status_health, cli_gateway_lifecycle, cli_main_argparse_root — relevance: the docker-backend env, `gateway run` boot + s6 supervisor, first-run `setup` wizard, on-upgrade config-schema migration, the `:9119` dashboard auth plugin, the port-8642 API-server routes + its `/health` endpoint, the `gateway start`/`run` lifecycle, and the `docker run`→`main-wrapper.sh` arg-routing (`main_argparse_root`) that turns `nousresearch/hermes-agent gateway run` into the right subcommand.

**Note 2 `hermes_docker_volumes_supervision`** (model)
- Terms (8): term_docker, term_sandbox_backend, term_session_persistence, term_autonomous_coding_agents, term_agent_harness, term_idempotency, term_multi_agent_systems, term_self_evolving_agent — relevance: the `/opt/data` volume is the single-source-of-truth persistence model (config/keys/sessions/skills/home); s6-overlay (PID 1) supervises per-profile gateways with state-persistent auto-restart for multi-profile self-evolving agents (self-improvement scoped to skills/memory/config under `/opt/data`); the boot reconciler is idempotent. (+fin: term_hermes_profile [own])
- Code-Repos (5): repo_hermes_agent — the Dockerfile/`docker/stage2-hook.sh`/s6-overlay `/init` + UID-10000 privilege model + `main-wrapper.sh` this note documents; repo_hermes_agent_cli — `hermes_cli.container_boot` (the `02-reconcile-profiles` reconciler), profile create/delete, and `gateway start/stop/restart`→`s6-svc` routing; repo_hermes_agent_agent_core — owns `hermes_state.py`/`sessions/` that the `/opt/data/sessions` + `memories/` directories persist; repo_hermes_agent_gateway_messaging — the per-profile `gateway` services s6 supervises and tees to `logs/gateways/<profile>/current`; repo_hermes_agent_skills — the `skills/` packs bind-mounted from `/opt/data/skills`.
- Docs (11): hermes_docker_run_modes — the run modes that write into this volume; hermes_docker_tools_local_inference — extends the same container; hermes_install_windows_native — the `%LOCALAPPDATA%\hermes` data-layout analogue; hermes_desktop_remote_backend — one dashboard backend serves every co-located profile; hermes_git_worktree_isolation — per-agent isolation contrast; hermes_install_windows_wsl2 — the WSL `~/.hermes` data root analogue; cc_sandbox_runtime_and_containers — analogous container persistence/runtime model; cc_checkpointing — analogous state-persistence/recovery model; cc_claude_application_data — analogous on-disk data-layout doc; cc_devcontainer_hardening — analogous non-root container privilege model; cc_background_session_hosting — analogous long-running supervised-session model.
- Snippets (11): tools_environments_docker, gw_runner_supervisor, gw_start_gateway_main, cli_main_cmd_profile, cli_profiles_schema, tools_credential_files, core_credential_sources, core_logging_setup, core_hermes_state, gw_runner_init, cli_gateway_lifecycle — relevance: the docker backend, s6 gateway supervisor + per-profile gateway boot (`gw_runner_init`), `profile create/delete` commands + per-profile schema, the credential-file/`auth.json` mount + credential sources, the `sessions/` state (`core_hermes_state`) that `/opt/data` persists, the four log surfaces (`core_logging_setup`), and the `gateway start/stop/restart`→`s6-svc` lifecycle (`cli_gateway_lifecycle`) the supervision model routes.

**Note 3 `hermes_docker_tools_local_inference`**
- Terms (9): term_docker, term_sandbox_backend, term_vllm, term_llm, term_model_catalog, term_provider_plugin, term_reverse_proxy, term_multimodal, term_health_check — relevance: extending the container reaches vLLM/Ollama (LLM/model-catalog/`provider: custom`) by container-name vs `host.docker.internal` vs `--network host`; `docker exec ... curl /v1/models` is the connectivity health check; the PulseAudio bridge enables multimodal voice. (+fin: term_voice_mode [own])
- Code-Repos (5): repo_hermes_agent_tools — the `tools/` effector layer (terminal/exec, the bash tool that runs `npx`/`uvx`/`apt` installs inside the container); repo_hermes_agent_providers_adapters — the `provider: custom` / `base_url` wiring that points Hermes at vLLM/Ollama/TGI; repo_hermes_agent_cli — `hermes doctor` connectivity checks + `config` for the `model.base_url` block; repo_hermes_agent_mcp_toolsets — the sidecar-container pattern (reach a tool over the shared Docker network like an MCP server); repo_hermes_agent — the Dockerfile's `docker-cli` + derived-image build path this note's five install strategies use.
- Docs (11): hermes_docker_run_modes — the base run modes this extends; hermes_docker_volumes_supervision — where `/opt/data`-persisted tool config lives; hermes_install_windows_wsl2 — the WSL local-inference networking analogue; hermes_install_windows_native — native local-model reach; hermes_desktop_app — front-end over the same providers; hermes_git_worktree_isolation — sibling deploy concern; cc_llm_gateway — analogous routing-to-a-model-endpoint doc; cc_llm_gateway_litellm — analogous self-hosted inference-server proxy; cc_cloud_network_access — analogous container-to-service networking; cc_sandboxed_bash_tool_setup — analogous in-sandbox tool-install model; cc_mcp_server_management — analogous sidecar/external-service tool extension.
- Snippets (11): tools_environments_docker, cli_providers_registry, cli_config_set, cli_voice, gw_start_gateway_main, core_credential_sources, cli_doctor_api_connectivity, tools_terminal_exec, plugins_provider_custom, tools_voice_mode, core_agent_init_memory_ollama — relevance: the docker-backend env, provider-registry + the `provider: custom`/`base_url` adapter (`plugins_provider_custom`) that points Hermes at vLLM, `config set` for the `model.base_url` block, the `docker exec ... curl /v1/models` connectivity check (`cli_doctor_api_connectivity`), the terminal-exec path that runs `npx`/`uvx`/`apt` installs, the Ollama memory/embedding wiring (`core_agent_init_memory_ollama`), and the voice-mode/PulseAudio bridge (`cli_voice` + `tools_voice_mode`) the audio-bridge step enables.

**Note 4 `hermes_install_windows_native`**
- Terms (9): term_hermes_agent, term_autonomous_coding_agents, term_agent_harness, term_oauth_token, term_authentication, term_idempotency, term_self_evolving_agent, term_reverse_proxy, term_oauth — relevance: the PowerShell `irm | iex` installer provisions the harness on Windows (uv/Python 3.11/Node 22/PortableGit/tiered pip), wires User PATH + `HERMES_HOME`, and registers the gateway as a `schtasks /SC ONLOGON` task; `hermes setup --portal` does the OAuth (Nous Portal) login; `hermes gateway status` is idempotent. (+fin: term_nous_portal [own])
- Code-Repos (5): repo_hermes_agent_cli — `hermes setup`, `hermes_cli/dep_ensure.py`, `gateway install` (schtasks/Startup), `hermes uninstall`, `hermes doctor`; repo_hermes_agent — `scripts/install.ps1` + the repo checkout the installer clones to `%LOCALAPPDATA%\hermes\hermes-agent`; repo_hermes_agent_gateway_messaging — the gateway the login task spawns detached via `pythonw.exe`; repo_hermes_agent_providers_adapters — the provider/OAuth registration `setup --portal` wires; repo_hermes_agent_skills — the messaging-SDK / skill bootstrap keyed off `.env`.
- Docs (11): hermes_windows_native_runtime — the day-to-day runtime surface this install produces; hermes_install_windows_wsl2 — the alternative Windows path (shared coexistence under separate data roots); hermes_docker_run_modes — the containerized deploy alternative; hermes_desktop_app — the GUI installer that calls `install.ps1` under the hood; hermes_git_worktree_isolation — agent isolation post-install; hermes_desktop_remote_backend — sibling deploy surface; cc_install — analogous CLI install procedure; cc_advanced_install_and_verification — analogous installer-internals + verification; cc_uninstall — analogous clean-uninstall procedure; cc_configure_your_environment — analogous PATH/env/data-dir setup; cc_authentication — analogous OAuth/portal login.
- Snippets (11): cli_setup_installer, cli_setup_wizard, cli_setup_verify, cli_gateway_windows, cli_gateway_lifecycle, cli_gateway_pid_discovery, cli_uninstall, cli_doctor_primitives, cli_gateway_dispatch, cli_auth_login_logout, cli_logs — relevance: the `install.ps1`-driven installer (`cli_setup_installer`), the `hermes setup` wizard/verify, the Windows `schtasks /SC ONLOGON` gateway install (`cli_gateway_windows`) + its dispatch (`cli_gateway_dispatch`) and lifecycle/PID code, the `hermes uninstall` cleanup, the `setup --portal` OAuth login (`cli_auth_login_logout`), and the doctor primitives + `hermes logs` the install / login-task / uninstall / troubleshooting steps document.

**Note 5 `hermes_windows_native_runtime`**
- Terms (8): term_hermes_agent, term_autonomous_coding_agents, term_agent_harness, term_context_window, term_persona, term_idempotency, term_multi_agent_systems, term_subagent — relevance: the runtime surface (Git Bash `bash.exe` resolution for the terminal tool, the `configure_windows_stdio` UTF-8/CP65001 shim, `EDITOR=notepad`, `Ctrl+Enter` newline, the idempotent `gateway status`, the `os.kill(pid,0)`→`CTRL_C_EVENT` footgun) is how the harness actually runs commands on native Windows. (+fin: term_voice_mode [own], term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_cli — `hermes_cli/stdio.py::configure_windows_stdio()`, `gateway.status._pid_exists()` (psutil), and `hermes doctor`; repo_hermes_agent_tools — the terminal tool that shells out through Git Bash + the `agent-browser` `.cmd` resolution; repo_hermes_agent — `scripts/check-windows-footguns.py` (the CI guard) + the `os.kill(pid,0)` migration across 11 files; repo_hermes_agent_tui_gateway — the TUI / Rich panels whose Unicode the UTF-8 shim protects; repo_hermes_agent_mcp_toolsets — the MCP servers (stdio + HTTP) the feature matrix marks native.
- Docs (11): hermes_install_windows_native — the install that produces this runtime; hermes_install_windows_wsl2 — the WSL alternative for the WSL-only dashboard PTY pane; hermes_docker_run_modes — the containerized alternative; hermes_desktop_app — the GUI front-end over the same Windows runtime; hermes_git_worktree_isolation — parallel-agent isolation on Windows; hermes_desktop_remote_backend — sibling surface; cc_terminal_configuration — analogous terminal/shell-runtime config; cc_interactive_mode_keyboard_shortcuts — analogous key-binding (Ctrl+Enter) surface; cc_input_modes_and_editing — analogous editor/`/edit` integration; cc_built_in_tools — analogous terminal/browser tool surface; cc_authentication_and_network_errors — analogous common-pitfalls/troubleshooting table.
- Snippets (11): cli_stdio_windows, core_bootstrap_utf8, cli_gateway_windows, cli_gateway_pid_discovery, cli_doctor_primitives, cli_doctor_api_connectivity, tools_terminal_exec, cli_setup_verify, gw_status_snapshot, tools_terminal_session, gw_status_health — relevance: the `configure_windows_stdio` UTF-8/CP65001 shim (`cli_stdio_windows` + `core_bootstrap_utf8`), the `gateway status` snapshot (`gw_status_snapshot`) + psutil PID-existence check (`cli_gateway_pid_discovery`) that replaced the `os.kill(pid,0)`→`CTRL_C_EVENT` footgun, the Git-Bash terminal tool + its session (`tools_terminal_exec` + `tools_terminal_session`) that shells out through `bash.exe`, and the doctor checks the runtime + pitfalls sections describe.

**Note 6 `hermes_desktop_app`**
- Terms (8): term_hermes_agent, term_autonomous_coding_agents, term_agent_harness, term_session_persistence, term_persona, term_skills, term_subagent, term_multi_agent_systems — relevance: the Desktop app is a native Electron front-end over the SAME agent core (shared config/keys/sessions/skills/memory), with a chat-first window, an inline model picker, concurrent multi-profile sessions, and Skills/Cron/Profiles/Agents orchestration panes; first launch installs the runtime into `HERMES_HOME`. (+fin: term_voice_mode [own], term_hermes_profile [own])
- Code-Repos (5): repo_hermes_agent_tui_gateway — the TUI the desktop backend explicitly reuses ("the modern terminal UI the desktop backend reuses"); repo_hermes_agent_cli — the `hermes desktop` subcommand + flags (`--skip-build`/`--source`/`--cwd`) and the Electron-main install/backend-resolution/self-update logic; repo_hermes_agent_providers_adapters — the provider/model catalog the in-app model picker and Providers pane surface; repo_hermes_agent_skills — the Skills management pane; repo_hermes_agent_cron — the Cron (scheduled-jobs) pane.
- Docs (11): hermes_desktop_remote_backend — pointing this app at a remote `hermes dashboard`; hermes_install_windows_native — the native-Windows install the GUI installer wraps; hermes_windows_native_runtime — the runtime the app drives on Windows; hermes_install_windows_wsl2 — sibling Windows path; hermes_docker_run_modes — the backend the app can attach to; hermes_git_worktree_isolation — sibling deploy concern; cc_desktop_overview_and_sessions — analogous desktop-app overview/sessions; cc_desktop_quickstart — analogous desktop install/first-run; cc_desktop_workspace_panes — analogous management/UI panes; cc_desktop_environments_extend_and_enterprise — analogous build/extend/enterprise surface; cc_vs_code_extension — analogous GUI front-end over the same agent core.
- Snippets (11): cli_models_picker, cli_model_switch_entry, cli_skin_apply, cli_voice, cli_main_cmd_profile, cli_profiles_switch, tui_entry, tui_server_session_boundary, tui_server_render, cli_main_cmd_chat, cli_model_catalog — relevance: the inline composer model-picker/switch (`cli_models_picker` + `cli_model_switch_entry`) over the full `cli_model_catalog` the Providers pane surfaces, the voice mode, profile create/switch (`cli_main_cmd_profile` + `cli_profiles_switch`) behind the concurrent multi-profile sessions, and the TUI entry/render/session-boundary code (`tui_entry`/`tui_server_render`/`tui_server_session_boundary` + the chat-session loop `cli_main_cmd_chat`) the Electron front-end's chat-first window reuses ("the desktop backend reuses the TUI").

**Note 7 `hermes_desktop_remote_backend`**
- Terms (9): term_oauth_token, term_authentication, term_reverse_proxy, term_websocket, term_session_persistence, term_hermes_agent, term_autonomous_coding_agents, term_api_gateway, term_oauth — relevance: the remote backend is a `hermes dashboard` whose non-loopback bind engages an auth gate (OAuth/Nous for public hosts vs `HERMES_DASHBOARD_BASIC_AUTH_*` username/password for trusted LAN/Tailscale) reached over the `/api/ws` WebSocket, optionally fronted by a reverse proxy (path prefixes like `/hermes`); the stable `_SECRET` keeps sessions persistent across restarts. (+fin: term_nous_portal [own], term_pkce [own])
- Code-Repos (5): repo_hermes_agent_tui_gateway — the WebSocket-backed dashboard/gateway the app attaches to over `/api/ws`; repo_hermes_agent_plugins — the `plugins/dashboard_auth/basic` (`hash_password`) + Nous-OAuth `DashboardAuthProvider`s; repo_hermes_agent_gateway_messaging — the `hermes dashboard` server process + `/api/status` (`auth_required`/`auth_providers`); repo_hermes_agent_cli — `hermes dashboard register`, per-profile remote-host config, `hermes logs gui`; repo_hermes_agent_providers_adapters — the Nous Portal OAuth provider/flow the public-host path uses.
- Docs (11): hermes_desktop_app — the local-app surface this extends; hermes_docker_run_modes — the dashboard `:9119` this connects to in a container; hermes_install_windows_native — sibling deploy; hermes_install_windows_wsl2 — exposing a WSL-hosted dashboard across the boundary; hermes_docker_volumes_supervision — one dashboard serves every co-located profile; hermes_git_worktree_isolation — sibling deploy concern; cc_remote_control — analogous remote-backend control; cc_remote_vs_web_and_deep_links — analogous remote-vs-local connection model; cc_authentication — analogous OAuth/basic-auth sign-in; cc_authentication_and_network_errors — analogous 401 / connection-refused triage; cc_proxy_and_gateway_config — analogous reverse-proxy fronting.
- Snippets (11): plugins_example_dashboard, gw_platform_api_server_connect, gw_platform_api_server_middleware, gw_platform_api_server_routes, cli_profiles_switch, cli_main_cmd_profile, core_credential_sources, cli_doctor_api_connectivity, cli_web_reveal_oauth, cli_auth_oauth_callback_server, gw_status_health — relevance: the `DashboardAuthProvider` plugin (`plugins_example_dashboard`) + the `/api/ws`-backed API-server connect/middleware/routes the non-loopback bind gates, the Nous-OAuth browser flow (`cli_web_reveal_oauth` + `cli_auth_oauth_callback_server`) for public hosts, the per-profile remote-host config (`cli_profiles_switch` + `cli_main_cmd_profile`), the basic-auth `_SECRET`/credential sources, and the `/api/status` (`gw_status_health`) + connectivity-check code the remote-backend sign-in + 401 triage document.

**Note 8 `hermes_install_windows_wsl2`**
- Terms (9): term_hermes_agent, term_autonomous_coding_agents, term_vllm, term_llm, term_reverse_proxy, term_oauth_token, term_authentication, term_self_evolving_agent, term_agent_harness — relevance: WSL2 runs the Hermes harness as plain Linux (`install.sh`) for the WSL-only dashboard PTY terminal and POSIX dev; the networking sections bridge Windows-hosted vLLM/Ollama/local-LLM servers (mirrored vs NAT, `netsh portproxy`) and expose the gateway/dashboard across the WSL↔Windows boundary; OAuth/HTTPS APIs break on WSL clock drift. (+fin: term_messaging_gateway [own], term_nous_portal [own])
- Code-Repos (5): repo_hermes_agent_cli — the Linux `install.sh` path + `hermes gateway setup` (the systemd-user-unit wizard); repo_hermes_agent — the installer scripts + `~/.hermes` Linux layout WSL inherits; repo_hermes_agent_gateway_messaging — the long-running gateway + API server exposed across the boundary; repo_hermes_agent_providers_adapters — the `provider: custom`/`base_url` wiring for the Windows-hosted local-inference servers; repo_hermes_agent_tools — the terminal tool / `rg`/file-watcher behavior that motivates keeping repos Linux-side.
- Docs (11): hermes_install_windows_native — the native alternative (both coexist under separate data roots); hermes_windows_native_runtime — the Git-Bash runtime WSL replaces with real POSIX; hermes_docker_tools_local_inference — the analogous container local-inference networking; hermes_desktop_app — a Windows GUI front-end onto a WSL backend; hermes_docker_run_modes — sibling deploy surface; hermes_desktop_remote_backend — reaching a WSL-hosted dashboard; cc_devcontainer_setup — analogous Linux-VM/dev-container deploy; cc_cloud_network_access — analogous host↔VM networking/port-forwarding; cc_network_tls_and_access — analogous network/TLS/firewall access; cc_install — analogous Linux install procedure; cc_configure_your_environment — analogous PATH/env/systemd-service setup.
- Snippets (11): setup_hermes_sh, cli_setup_installer, gw_start_gateway_main, gw_runner_supervisor, cli_providers_registry, cli_config_set, cli_doctor_api_connectivity, tools_terminal_exec, cli_gateway_systemd, plugins_provider_custom, core_agent_init_memory_ollama — relevance: the Linux `install.sh` (`setup_hermes_sh` + `cli_setup_installer`) WSL runs as plain Linux, the long-running gateway + supervisor exposed across the boundary, the `hermes gateway setup` systemd-user-unit wizard (`cli_gateway_systemd`), the `provider: custom`/`base_url` adapter (`plugins_provider_custom`) + Ollama wiring (`core_agent_init_memory_ollama`) for the Windows-hosted local-inference servers, the `curl /v1/models` connectivity check, and the terminal/`rg` behavior (`tools_terminal_exec`) that motivates keeping repos Linux-side.

**Note 9 `hermes_git_worktree_isolation`**
- Terms (8): term_git_worktree_agents, term_autonomous_coding_agents, term_multi_agent_systems, term_subagent, term_agent_harness, term_regular_checkpointing, term_hermes_agent, term_self_evolving_agent — relevance: worktrees give each parallel agent its own branch + working dir + a separate Checkpoint-Manager `/rollback` history under a shadow-repo hash derived from the worktree path; `hermes -w` auto-creates a disposable worktree under `.worktrees/`; this is the multi-agent isolation primitive (Hermes treats cwd as project root). (+fin: term_shadow_git_checkpoint [own])
- Code-Repos (5): repo_hermes_agent_cli — the `hermes -w` automatic-worktree-mode flag + `-z` query and CLI cwd→project-root resolution; repo_hermes_agent_tools — the Checkpoint Manager (per-worktree shadow-repo checkpoints, `/rollback`) and the terminal tool scoped to the worktree dir; repo_hermes_agent_skills — the git/github skill used for branch/merge workflows; repo_hermes_agent_agent_core — the per-session agent state/history each isolated worktree runs; repo_hermes_agent — the monorepo `.worktrees/` + `~/.hermes/checkpoints/` layout this note documents.
- Docs (11): hermes_docker_run_modes — running agents in a container vs worktrees; hermes_install_windows_native — the host these worktrees run on; hermes_windows_native_runtime — the terminal/cwd runtime worktrees scope; hermes_desktop_app — concurrent multi-session UI alternative; hermes_install_windows_wsl2 — Linux-side repos worktrees prefer; hermes_docker_volumes_supervision — multi-profile vs multi-worktree isolation contrast; cc_worktree_isolation — Claude Code's directly-analogous git-worktree isolation; cc_large_codebase_reduce_reads_and_worktrees — analogous worktree-for-large-repos guidance; cc_run_agents_in_parallel — analogous parallel-agent workflow; cc_checkpointing — analogous checkpoint/rollback safety net; cc_sdk_file_checkpointing_concepts — analogous per-session checkpoint model.
- Snippets (11): cli_worktree_isolation, tools_checkpoint_save, tools_checkpoint_resume, skills_github, tools_terminal_exec, cli_main_cmd_profile, core_hermes_home, core_logging_setup, core_hermes_state, cli_main_argparse_root, gw_runner_session_key — relevance: the `hermes -w` automatic-worktree code (`cli_worktree_isolation`), checkpoint save/resume under a per-worktree shadow-repo hash (`tools_checkpoint_save`/`tools_checkpoint_resume`), the git/github skill (`skills_github`) for branch/merge, the cwd→project-root resolution (`cli_main_argparse_root`) that makes each worktree its own root, the terminal tool scoped to the worktree dir (`tools_terminal_exec`), per-session agent state + session keying (`core_hermes_state` + `gw_runner_session_key`) each isolated worktree runs, and the `~/.hermes/checkpoints/`/`HERMES_HOME` + logging layout (`core_hermes_home` + `core_logging_setup`) this note documents.

All 9 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (the four counted floors). Code-repo IDs are under
modules that implement each doc note). Snippet IDs are under `resources/code_snippets/` with the
`snippet_hermes_agent_` prefix (a now-COUNTED floor of ≥10, promoted 2026-06-19 from the prior 8-item bonus group;
active 2026-06-19; sibling `hermes_*` doc links resolve in `resources/documentation/hermes_agent/` (intra-series links
`term_git_worktree_agents`; `[own]` forward-refs (`term_nous_portal`, `term_messaging_gateway`, `term_voice_mode`,
`term_hermes_profile`, `term_shadow_git_checkpoint`, `term_pkce`) are excluded from the floor and added at
finalization once their owning SPs capture them. Smallest per-note counts: term 8, code-repo 5, snippet 11, doc 11.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; re-measured 2026-06-19, mirror c253b07)

Re-read all 5 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). 2026-06-19 re-sync: docker.md 5815→6013w (+198) and desktop.md 3093→3271w (+178)
both grew marginally (+3.4% / +5.8%, code unchanged) — within link-out compression headroom, ~Words estimates
remain sensible, no per-note cap approached, no re-split triggered. Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 docker-run-modes | procedure | 1500 | ≤6 (curate from gateway/dashboard/compose/upgrade blocks; one canonical `docker run` + the compose YAML) | ✓ |
| 2 docker-volumes-supervision | model | 1900 | ≤6 (curate from profile lifecycle / log table / entrypoint blocks; tables in prose) | ✓ |
| 3 docker-tools-local-inference | procedure | 1500 | ≤6 (curate from npx/derived-image/sidecar/vLLM-compose/Ollama blocks) | ✓ |
| 4 install-windows-native | procedure | 1500 | ≤6 (from install one-liner / scriptblock / schtasks / uninstall blocks) | ✓ |
| 5 windows-native-runtime | procedure | 1500 | ≤6 (from Git-Bash / EDITOR / pitfalls blocks) | ✓ |
| 6 desktop-app | procedure | 1500 | ≤6 (from `hermes desktop` / flag table / build blocks) | ✓ |
| 7 desktop-remote-backend | procedure | 1300 | ≤6 (from `.env` creds / dashboard-bind / curl-status blocks) | ✓ |
| 8 install-windows-wsl2 | procedure | 1700 | ≤6 (curate from wsl.conf / portproxy / wslpath blocks; networking tables in prose) | ✓ |
| 9 git-worktree-isolation | procedure | 800 | ≤6 (from `git worktree add` / `hermes -w` blocks) | ✓ |

No further splits needed — all 9 notes ≤2500w. Code-heavy `docker.md` (36 blocks) is curated to ≤6
load-bearing examples per note, the rest summarized in prose (kept blocks verbatim). Borderline note 2 (~1900w,
model) and note 8 (~1700w) were checked for further split: each is one topically-cohesive cluster with no BB
mixing → KEEP (review CP6 default-to-keep). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
verified field order against `cc_admin_enforcement_controls.md` and `cc_sandbox_modes.md`): YAML field order
`tags → keywords → topics → language → date of note → status → building_block → source_url → access_control_group`;
body `# Title → ## Overview (opener leading with what it IS, NOT ## Definition) → source-mirrored H2s →
## Related Notes (indexed markdown links, each `- [Name](path.md) — what-it-is; relevance: …`; FOUR counted floors
≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc — floor set 2026-06-19) → footer **Source** / **Last Updated** /
**Status: Active** (plain bold, no heading)`. One
BB/note; caps ≤2500w/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`,
`updated`, `source`, `parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown
links in YAML. Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP03a)

**SP03a owns 1 new term capture: `term_git_worktree_agents`** (Pattern B — captured Phase 0, BEFORE the
`hermes_git_worktree_isolation` doc note). Every other Hermes-specific concept SP03a touches is owned by another
sub-plan (link at finalization) or is an existing verified term. Augment re-read surfaced **0 additional** undigested
terms beyond the master inventory that SP03a should own.

| Term | Concept | DF | Capture Phase | Stub or Full | Best-fit glossary | Decision / Owner |
|------|---------|---:|---------------|--------------|-------------------|------------------|
| `term_git_worktree_agents` | parallel agents via git worktrees (own branch + dir + shadow-repo checkpoint history) | 6 | Phase 0 (before Note 9) | full | acronym_glossary_developer | **CAPTURE (owned)** — pre-flight: absent → create full note via `/tessellum-capture-term-note`. |
| `term_tirith` | pre-exec security scanner | — | LINK only ([own], +fin) | — | acronym_glossary_security | Owned by SP03b (security.md) — SP03a does not touch it. |
| `term_shadow_git_checkpoint` | rollback via shadow git repo | — | LINK only ([own], +fin) | — | acronym_glossary_systems | Owned by SP03b (checkpoints) — Note 9 forward-refs it; added at finalization. |
| `term_nous_portal`, `term_messaging_gateway`, `term_voice_mode`, `term_hermes_profile`, `term_pkce` | — | — | LINK only ([own], +fin) | — | — | Owned by SP14 / SP11 / SP08 / SP04 / SP09 respectively; forward-refs added at finalization. |

### Renamed (general → specific)

The owned slug was specificity-audited: a bare `term_worktree` would be too general (collides with the generic
git-worktree concept, which is not Hermes-specific). The owned concept is *parallel Hermes agents via worktrees* →
`term_git_worktree_agents` (scope-qualified: git-domain prefix + agents suffix). No further renames (SP03a owns 1 slug).

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_docker` (would duplicate) | `term_docker.md` (active) | Not captured — LINK the existing term from the Docker doc notes. |
| `term_terminal_backend` / `term_sandbox_backend` (would duplicate) | `term_sandbox_backend.md` (active) | Not captured — LINK the existing term; the 6-backend model is owned by SP02 `hermes_terminal_backends`. |
| `term_worktree` (would-be, too general) | none (no `term_worktree`/`term_git_worktree*` exists) | Renamed to `term_git_worktree_agents` (specificity audit) and CAPTURED. |

## Term-Note Authoring Requirements (Per Owned Term — Inherited from `/tessellum-capture-term-note` canonical)

`term_git_worktree_agents` MUST be authored via **`/tessellum-capture-term-note "git worktree agents"`** (NOT
inline-authored within Note 9). The capture skill enforces the requirements below; this plan invokes them.

- **YAML**: `tags: [resource, terminology, <developer/agents domain tag>, version_control]`; `keywords`
  (git worktree agents, parallel agents, isolated checkout); `topics`; `language: markdown`; `status: active`;
  `building_block: concept`; `access_control_group: ["general"]`; `related_wiki: null` (open-source-docs term).
  No forbidden fields.
- **H1/H2 order**: `# Git Worktree Agents` → `## Definition` → `## Context` → `## Key Characteristics` →
  (optional) `## Performance / Metrics` → `## Related Terms` (8-15 indexed bold links) → `## References`
  (external URLs only — the Hermes git-worktrees doc URL + git-worktree docs; NO `term_*.md` here).
  documentation, the autonomous-coding-agent parallelism literature (1-2 external sources), plus vault cross-refs
  (`/tessellum-search-notes` + DB) for in-domain (`term_autonomous_coding_agents`, `term_multi_agent_systems`,
  `term_subagent`, `term_regular_checkpointing`) AND cross-domain (`term_*_parallelism` as a structural analogy,
  `term_sandbox_backend` as a contrast isolation mechanism) related terms.
- **Cross-domain diversity**: ≥3 in-domain (agents/version-control) + ≥3 cross-domain (parallelism analogy,
  sandboxing contrast) = ≥8-15 verified links. Depth tier: simple→moderate (40-150 lines) → **8-10** Related Terms.
- **MathJax / fleeting-content / glossary template / >200-line decomposition**: per canonical (no math expected;
  no fleeting content; 4-5-sentence glossary Description, bold the most-important fact; decompose if >200 lines).
- **Backlink expansion (Step 6e)**: add `term_git_worktree_agents` to the `## Related Terms` of 5-10 existing
  in/cross-domain term notes (`term_autonomous_coding_agents`, `term_multi_agent_systems`, `term_subagent`,
  `term_sandbox_backend`, `term_regular_checkpointing`). Plus Note 9 backlinks it (Step 6a-6d).
- **Glossary**: add the entry to `0_entry_points/acronym_glossary_developer.md` using the exact
  `**Full Name** / **Description** / **Documentation** / **Wiki** / **Related**` template.
- **Acceptance fails** if single-source, <8 Related Terms, no cross-domain diversity, no inlink expansion,
  References contains `term_*.md`, Related Terms contains external URLs, ordering violated, forbidden YAML field,
  `building_block` ≠ concept, or non-canonical filename. (Full acceptance list per canonical Step 10.5d.)

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (owned term capture):** `/tessellum-capture-term-note "git worktree agents"` → `term_git_worktree_agents`
  (full) + glossary entry + 5-10 inlink expansions. Reindex. GATE G1, G5, G6, G8.
- **Phase 1 (Docker cluster, P1-hub pilot):** Notes 1, 2, 3. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (Windows + Desktop):** Notes 4, 5, 6, 7. GATE G1–G8.
- **Phase 3 (WSL2 + worktrees):** Notes 8, 9 (Note 9 after Phase 0 term exists). GATE G1–G8.
- **Phase 3b (inlinks):** add the Inlinks-table backlinks (existing → new); verify DB in-degree ≥1 per note (G8).

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for kept
blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every ref)** ·
**G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
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
for n in hermes_docker_run_modes hermes_docker_volumes_supervision hermes_docker_tools_local_inference hermes_install_windows_native hermes_windows_native_runtime hermes_desktop_app hermes_desktop_remote_backend hermes_install_windows_wsl2 hermes_git_worktree_isolation; do
```

## Entry Point Decision (inherited)

Contributes 9 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c, >30-note series)
under a "Deployment & Platforms" section. Parent hub back-link in `entry_research_and_ai_hub.md` is handled at master
level. SP03a does NOT create a separate entry point — the >30-note corpus shares the single master-created
`entry_hermes_agent_docs.md` (matches the >30 threshold). The owned term gets a glossary row in
`acronym_glossary_developer.md` (Phase 0).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent.md` | → `hermes_docker_run_modes`, `hermes_docker_volumes_supervision` | implementation ↔ Docker deployment docs |
| `repo_hermes_agent_tools.md` | → `hermes_docker_tools_local_inference`, `hermes_git_worktree_isolation` | tools/terminal repo ↔ tool-install + worktree docs |
| `repo_hermes_agent_cli.md` | → `hermes_install_windows_native`, `hermes_windows_native_runtime` | CLI repo ↔ Windows install/runtime docs |
| `repo_hermes_agent_tui_gateway.md` | → `hermes_desktop_app`, `hermes_desktop_remote_backend` | TUI/gateway repo ↔ Desktop app docs (backend reuses TUI) |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_install_windows_wsl2` | gateway repo ↔ WSL2 long-running gateway doc |
| `term_docker.md` | → `hermes_docker_run_modes`, `hermes_docker_volumes_supervision` | concept term → Hermes-in-Docker docs |
| `term_sandbox_backend.md` | → `hermes_docker_volumes_supervision`, `hermes_docker_tools_local_inference` | backend concept → Docker execution docs |
| `term_git_worktree_agents.md` (new, Phase 0) | → `hermes_git_worktree_isolation` | owned term → its user-facing worktree procedure |
| `term_regular_checkpointing.md` | → `hermes_git_worktree_isolation` | checkpoint concept → per-worktree shadow-repo history |
| `entry_code_snippets_hermes_agent.md` | → `hermes_docker_run_modes`, `hermes_install_windows_native` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 9 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution phase
(Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_docker_run_modes`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Phase 0 (owned term) runs first so Note 9's `term_git_worktree_agents` link is not a ghost. Commit per phase
(per-wave commits for multi-agent runs). Re-read the source page before writing each note — do NOT work from memory.
Code blocks verbatim for kept blocks; curate code-heavy `docker.md` notes to ≤6 load-bearing examples, summarize the
rest in prose. If a note exceeds 350 lines during writing, STOP and split. If multi-agent: agents return note
content, master writes serially where there is write-contention; ≤30 agents/run; embed the manifest in the workflow
script.

## Follow-up Recommendations

- After SP03a lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 9 rows to the
  master-created entry point + the glossary row; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After SP03b lands: cross-link the Docker/Windows/Desktop notes to `hermes_checkpoints_rollback`,
  `hermes_security`, and `hermes_secrets_*`; add the `term_shadow_git_checkpoint` / `term_tirith` forward-refs.
- After P1 wave: bidirectional config↔deployment links — link `hermes_terminal_backends` (SP02) ↔
  `hermes_docker_volumes_supervision` once SP02 lands.
- Consider one `thought_` note comparing Hermes' docs-stated Docker/supervision model vs the code-digestion
  findings in `snippet_hermes_agent_gw_runner_supervisor` / `snippet_hermes_agent_tools_environments_docker`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (term_docker/term_sandbox_backend LINK-not-dup confirmed; owned slug
  collision-clear), finalized Per-Note Mapping (≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc, all term/repo/snippet/cc_*
  confirmed), Undigested Terms Plan + Term-Note Authoring Requirements (owned `term_git_worktree_agents`), G5 ghost +
  G8 scripts, Inlinks.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  ≥10 doc + 8-item bonus snippets state):** the snippet group was promoted from "bonus" to a COUNTED floor and raised
  from 8 to ≥10 on every note; the 5 owned source pages were re-read from `inbox/hermes_agent_docs/` (mirror c253b07)
  to ground every added snippet relevance clause against the actual code paths each page documents. No existing
  relevant term/repo/snippet/doc cross-ref was dropped (additive only). Smallest per-note counts after the re-augment:
  term 8, code-repo 5, snippet 11, doc 11.
- Density re-read: counts match measured (docker 6013, windows-native 3343, desktop 3271, wsl 2928, worktrees 803;
  re-measured 2026-06-19, mirror c253b07); **no additional splits** beyond the planned 5 (docker→3, windows-native→2,
  desktop→2). All 9 notes ≤2500w.
- Collision audit: **0 removals** — `term_docker`/`term_sandbox_backend` are LINK-not-dup; no doc note duplicates an
  existing term/doc note; owned slug `term_git_worktree_agents` is collision-clear (no `term_worktree`/`term_git_worktree*`).
- Owned-term capture: 1 (`term_git_worktree_agents`); specificity audit renamed would-be `term_worktree` → scope-qualified.
- Undigested terms surfaced at augment: **0 new** beyond the master inventory (SP03a owns exactly the master-assigned slug).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (≥8 term /
Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓ Validation
Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture Phase per term (1
owned, Phase 0) ✓ best-fit glossary (acronym_glossary_developer) ✓ Term-Note Auth Reqs (owned slug) ✓ invokes
capture-term-note ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (term_worktree→term_git_worktree_agents)
✓ Slug Collision (owned slug clear; term_docker/term_sandbox_backend LINK-not-dup) ✓ dedup generalized to ALL notes
incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓ Doc-Note Authoring
Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**
**Re-reviewed 2026-06-19 (FOUR-FLOOR standard, independent) — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence (2026-06-19 four-floor re-review) |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Execution Phases 0–3b, each lists G1 format · G2 grounding · G3 density · G4 cross-ref · G5 ghost (DB-verify) · G6 broken-links · G7 single-BB · G8 in-degree ≥1. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 rows, Deployment & Platforms section) + glossary row in `acronym_glossary_developer.md`; parent hub at master level (>30-note threshold). |
| CP4 | Plan size manageable | PASS | 9 notes ≤30; master holds the corpus-level split (SP03 a/b). |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (field order verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); ## Related Notes spec updated to the four counted floors; not invented. |
| CP6 | Borderline density → split | PASS | docker→3, windows-native→2, desktop→2; all 9 notes ≤2500w; code-heavy docker notes curated ≤6; borderline notes 2 (~1900w) and 8 (~1700w) re-checked → cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Independently re-measured 2026-06-19 against the live mirror (HEAD `751c7b03e`): docker 6013w/36, desktop 3271w/9, windows-native 3343w/9, windows-wsl 2928w/14, git-worktrees 803w/7. All word counts == plan ledger (ratio 1.00). One minor fix applied: windows-wsl code-fence count corrected 16→14 (word-only metric unchanged; no density decision affected). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP03a owns 1 term capture (`term_git_worktree_agents`, Phase 0, full); Undigested Terms Plan + Term-Note Authoring Requirements present; multi-source mandate + cross-domain diversity + backlink expansion specified. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 9 doc notes + the owned slug (term_dictionary AND documentation/); `term_docker`/`term_sandbox_backend` LINK-not-dup; would-be `term_worktree` renamed (too general) → `term_git_worktree_agents`; owned slug DB-confirmed absent. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 notes from repo_*/term_*/entry_* outside the folder; `entry_hermes_agent_docs → all 9` guarantees in-degree ≥1; inlink addition is gated Phase 3b. |

**RESULT (2026-06-15): 9/9 → READY FOR EXECUTION.**
**RESULT (2026-06-19, FOUR-FLOOR re-review): 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

Local mirror `inbox/hermes_agent_docs/` re-downloaded from upstream main HEAD `c253b07` (was `95715dc`); SP03a's
5 owned pages independently re-measured (body word count, code-fence pairs). Two owned pages grew:

- user-guide/docker.md — 5815w/36code → 6013w/36code
- user-guide/desktop.md — 3093w/9code → 3271w/9code

Unchanged pages spot-re-measured and confirmed stable: windows-native.md 3343w/9code, windows-wsl-quickstart.md
2928w/14code, git-worktrees.md 803w/7code (word counts == prior ledger; windows-wsl code-fence count corrected
16→14 at the 2026-06-19 review re-measure against the live mirror, HEAD `751c7b03e` — word-only metric unchanged,
no density decision affected since code is well within the per-note ≤6 cap).

**Density re-decision: none.** Both growths are word-only (code-fence counts identical) and marginal (+198w / +3.4%
on docker, +178w / +5.8% on desktop). docker.md was already split 3-ways and desktop.md 2-ways; the +198w/+178w
distribute across notes already compressed via link-outs, no planned note approaches the 2500w / 6-code / 400-line
caps, so no planned-note density decision changed: docker stays 3 notes (no-split delta), desktop stays 2 notes
(no-split delta). **No split added.**

**Cross-ref floor unchanged at the 2026-06-19 re-sync** (then ≥8 term + ≥8 snippet + ≥5 doc per note). **Note —
subsequently set 2026-06-19 (see Augmentation Report) to the FOUR-floor standard ≥8 term / ≥5 code-repo / ≥10 snippet /
≥10 doc per note, all counted (snippets promoted from bonus to a counted ≥10 floor).** No planned-note filename, BB
type, or gate altered. **Plan remains READY for execution.**

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; four-floor re-augment 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; FOUR-FLOOR re-review 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/{docker,windows-native,desktop,windows-wsl-quickstart,git-worktrees}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
