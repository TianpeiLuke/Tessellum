---
title: Sub-Plan hp02 — OpenClaw Docs: Help (Scripts, Testing & Troubleshooting)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["help/scripts", "help/testing", "help/testing-live", "help/testing-updates-plugins", "help/troubleshooting"]
status_history:
  - "pending -> ready (xref-augment + review 9/9 PASS, 2026-06-21)"
---

# Sub-Plan hp02: Help

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup-before-create, 9-GATE validation,
> cross-references, and the Undigested-Terms ownership rule are ALL inherited from the master (read + confirmed).

## Scope

The 5 Help pages covering OpenClaw's developer test/ops surface: the `scripts/` helper directory (scripts.md),
the test-runner map and suite taxonomy (testing.md), the live network-touching test suites (testing-live.md),
the update/plugin validation checklist (testing-updates-plugins.md), and the symptom-first troubleshooting hub
(troubleshooting.md). These are **procedure-dominant operator/maintainer references** — how to run, validate, and
debug OpenClaw. Priority **P2 (Phase B)**: not core architecture vocabulary, but high operational relevance
(every contributor/operator hits testing + triage). The code-side counterparts (`repo_openclaw*` repo notes)
are LINKED, not recreated.

**Source**: OpenClaw docs, 5 pages, **17,091 measured words** (scripts 239 + testing 9,047 + testing-live 3,803 +
testing-updates-plugins 1,615 + troubleshooting 2,387). **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| scripts | help/scripts | 239 | 0 | 5 | 0 | procedure |
| testing | help/testing | 9,047 | 11 | 13 | 13 | procedure (split ×3: suites · QA-lab runners · Docker runners) |
| testing-live | help/testing-live | 3,803 | 13 | 17 | 7 | procedure (split ×2: model/CLI/ACP/Codex · media + credentials) |
| testing-updates-plugins | help/testing-updates-plugins | 1,615 | 9 | 8 | 0 | procedure |
| troubleshooting | help/troubleshooting | 2,387 | 18 | 8 | 0 | procedure |

(Code counts = fence lines / 2. testing-live: `### Recommended live recipes` H3 sits under
`## Live: Codex app-server harness smoke`; troubleshooting's code includes a `mermaid` decision-tree fence and
seven `<Accordion>` symptom blocks each carrying a `bash` ladder.)

## Content Strategy

- **Prioritize**: the troubleshooting triage ladder + symptom-to-cause decision tree (the fastest operational
  payoff), the test-suite taxonomy (unit/integration/e2e/live + which-suite-to-run decision table), and the
  update/plugin validation contract (what package/upgrade tests protect).
- **Split**: `testing.md` (9,047w, far over the 2,500w cap, ≥3 distinct task clusters) → (a) suite taxonomy +
  quick-start + contract/offline/evals, (b) QA-lab / live-transport / Convex-credential runners, (c) Docker
  runners catalog. `testing-live.md` (3,803w, over cap, two clusters) → (a) live model/CLI/ACP/Codex smoke
  layers, (b) media-provider live suites + live-test credential resolution.
- **Link-out (do not redefine)**: QA-lab architecture → `concepts/qa-e2e-automation` (co05, planned) and
  `concepts/qa-matrix` (co06, planned); gateway/channel deep runbooks → `gateway/troubleshooting` (gw07,
  planned), `channels/troubleshooting` (ch05, planned), `nodes/troubleshooting` (nd02, planned),
  `gateway/doctor` (gw02, planned), `gateway/authentication` (gw01, planned); install/docker permissions →
  `install/docker` (in02, planned); tool/exec/browser deep pages → `tools/*` (to01–08, planned); plugin
  architecture/policy → `plugins/architecture` (pl01, planned), `tools/skills-config`/`tools/plugin` (to06/to07,
  planned); FAQ/debugging/environment → hp01 siblings. CI top-level → `ci` (rt01, planned). Provider/model
  vocabulary links existing `term_llm`/`term_claude`/`term_bedrock`/`term_mcp`, never redefined.
- **Code fences**: reproduce only the highest-signal commands verbatim (≤6/note); the long Docker-runner env-var
  lists and bash ladders are summarized as prose + a few representative snippets.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_help_scripts.md` | procedure | scripts.md (all: Conventions, Auth monitoring scripts, GitHub read helper, When adding scripts) | 280 | The repo `scripts/` helper directory: conventions (scripts optional, prefer CLI, host-specific), the auth-monitoring extras, and the `gh-read` GitHub-App read-token helper with its env + repo-resolution order. |
| 2 | `oc_help_testing_suites.md` | procedure | testing.md: Quick start, Test Temp Directories, Test suites (Unit/integration, Stability, E2E ×4, Live), Which suite should I run?, Docs sanity, Offline regression, Agent reliability evals, Contract tests, Adding regressions | 750 | OpenClaw's Vitest suite taxonomy — unit/integration, gateway stability, the four E2E lanes (aggregate, gateway smoke, Control-UI mocked browser, OpenShell), and live — plus quick-start commands, temp-dir helpers, the which-suite decision table, offline regressions, contract tests, and regression-adding guidance. |
| 3 | `oc_help_testing_qa_runners.md` | procedure | testing.md: QA-specific runners (qa suite / coverage / multipass / aimock / matrix / telegram, Mantis wrappers, kitchen-sink, cpu-scenarios), Shared Telegram credentials via Convex (v1), Adding a channel to QA | 700 | The QA-lab runner surface: `pnpm openclaw qa suite/coverage/matrix/telegram` and the live-transport lanes, the Mantis PR-evidence wrappers, and the Convex-backed shared-credential broker contract (lease/heartbeat/release endpoints, per-channel payload shapes) for live transport QA. |
| 4 | `oc_help_testing_docker_runners.md` | procedure | testing.md: Docker runners (optional "works in Linux" checks) — live-model runners, `test:docker:all` scheduler, container smoke runners, image overrides, env vars | 700 | The Docker test-runner catalog: live-model/gateway lanes, the weighted `test:docker:all` scheduler, the container smoke runners (onboard, release journeys, plugins, gateway-network, mcp-channels, browser-cdp), shared-image overrides, and the bind-mount auth/env-var conventions. |
| 5 | `oc_help_testing_live_models.md` | procedure | testing-live.md: Live local smoke commands, Android node sweep, Live model smoke (Layer 1 direct + Layer 2 gateway), CLI backend smoke, APNs proxy reachability, ACP bind smoke, Codex app-server harness smoke, Recommended live recipes, Live model matrix | 750 | Live network-touching model/agent smokes: the two-layer model probe (direct completion vs gateway+agent), CLI-backend, ACP-bind, and Codex app-server harness lanes, the `OPENCLAW_LIVE_*` model/provider selection knobs, recommended allowlist recipes, and the recommended model-coverage matrix. |
| 6 | `oc_help_testing_live_media_creds.md` | procedure | testing-live.md: Credentials (never commit), Deepgram live, BytePlus live, ComfyUI live, Image generation live, Music generation live, Video generation live, Media live harness | 650 | Live media-provider suites (Deepgram audio, BytePlus, ComfyUI, image/music/video generation, the media harness) and how live tests resolve credentials — profile store vs env fallbacks, the staged temp-home copy, and the `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS` enforcement. |
| 7 | `oc_help_testing_updates_plugins.md` | procedure | testing-updates-plugins.md (all: What we protect, Local proof, Docker lanes, Package Acceptance, Release default, Legacy compatibility, Adding coverage, Failure triage) | 650 | The update/plugin validation checklist: what package/upgrade/plugin contracts are protected, local proof commands, the Docker upgrade-survivor lanes, the GitHub-native Package Acceptance gate (npm/ref/url/trusted-url/artifact sources), the release default proof stack, legacy-compat cutoffs, and failure triage. |
| 8 | `oc_help_troubleshooting.md` | procedure | troubleshooting.md (all: First 60 seconds, Assistant feels limited, Anthropic 429, local OpenAI-compat backend, plugin-install/policy/ownership symptoms, Decision tree + 8 accordion symptom blocks) | 700 | Symptom-first triage hub: the First-60-seconds command ladder, the tool-profile and provider-compat fixes, plugin install/policy/ownership recovery, and the symptom-to-cause decision tree (no replies, Control UI, gateway, channel flow, cron/heartbeat, node tools, exec approval, browser) routing to deep runbooks. |

## Section Coverage Map

```
scripts.md
├── Conventions ──────────────────────────────── → note 1 (oc_help_scripts)
├── Auth monitoring scripts ──────────────────── → note 1
├── GitHub read helper (gh-read, env, resolution) → note 1
├── When adding scripts ──────────────────────── → note 1
└── Related ──────────────────────────────────── → note 1 (References)
testing.md
├── Quick start ──────────────────────────────── → note 2 (oc_help_testing_suites)
├── Test Temp Directories ────────────────────── → note 2
├── QA-specific runners (qa suite/coverage/multipass/
│   aimock/matrix/telegram, Mantis, kitchen-sink,
│   cpu-scenarios) ───────────────────────────── → note 3 (oc_help_testing_qa_runners)
│   ├── Shared Telegram credentials via Convex (v1) → note 3
│   └── Adding a channel to QA ────────────────── → note 3
├── Test suites (Unit/integration, Stability,
│   E2E repo/gateway/UI/OpenShell, Live) ──────── → note 2
├── Which suite should I run? ─────────────────── → note 2
├── Live (network-touching) tests (pointer) ───── → note 2 (links notes 5/6/7)
├── Docker runners (optional Linux checks) ────── → note 4 (oc_help_testing_docker_runners)
├── Docs sanity ──────────────────────────────── → note 2
├── Offline regression (CI-safe) ─────────────── → note 2
├── Agent reliability evals (skills) ─────────── → note 2
├── Contract tests (Commands, Channel/Provider) ─ → note 2
├── Adding regressions (guidance) ────────────── → note 2
└── Related ──────────────────────────────────── → notes 2/4 (References)
testing-live.md
├── Live: local smoke commands ───────────────── → note 5 (oc_help_testing_live_models)
├── Live: Android node capability sweep ──────── → note 5
├── Live: model smoke (Layer 1 + Layer 2) ────── → note 5
├── Live: CLI backend smoke ──────────────────── → note 5
├── Live: APNs HTTP/2 proxy reachability ─────── → note 5
├── Live: ACP bind smoke ─────────────────────── → note 5
├── Live: Codex app-server harness smoke ─────── → note 5
│   └── Recommended live recipes ─────────────── → note 5
├── Live: model matrix (what we cover) ───────── → note 5
├── Credentials (never commit) ───────────────── → note 6 (oc_help_testing_live_media_creds)
├── Deepgram / BytePlus / ComfyUI live ───────── → note 6
├── Image / Music / Video generation live ────── → note 6
├── Media live harness ───────────────────────── → note 6
└── Related ──────────────────────────────────── → notes 5/6 (References)
testing-updates-plugins.md
├── What we protect ──────────────────────────── → note 7 (oc_help_testing_updates_plugins)
├── Local proof during development ───────────── → note 7
├── Docker lanes ─────────────────────────────── → note 7
├── Package Acceptance ───────────────────────── → note 7
├── Release default ──────────────────────────── → note 7
├── Legacy compatibility ─────────────────────── → note 7
├── Adding coverage ──────────────────────────── → note 7
└── Failure triage ───────────────────────────── → note 7
troubleshooting.md
├── First 60 seconds ─────────────────────────── → note 8 (oc_help_troubleshooting)
├── Assistant feels limited or missing tools ─── → note 8
├── Anthropic long context 429 ───────────────── → note 8
├── Local OpenAI-compatible backend fails ────── → note 8
├── Plugin install / policy / ownership symptoms  → note 8
└── Decision tree + 8 accordion symptom blocks ── → note 8
```
No orphaned sections. Every H2/H3 maps to exactly one planned note; pointers (testing.md "Live tests",
"Custom Providers"-style cross-links) become References/Related links, not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| testing.md (9,047w, 13 H2 / 13 H3) | notes 2 + 3 + 4 | ~3.6× the 2,500w cap; three distinct task clusters — (2) suite taxonomy / how-we-test, (3) QA-lab runner surface + Convex credential broker, (4) Docker runner catalog. Each cluster is independently referenced and stays ≤750w / ≤6 code. |
| testing-live.md (3,803w, 17 H2 / 7 H3) | notes 5 + 6 | Over the 2,500w cap with two clusters — (5) live model/agent smoke layers (direct/gateway/CLI/ACP/Codex + recipes + matrix), (6) media-provider live suites + credential resolution. Keeps each ≤750w / ≤6 code. |
| scripts.md (239w) | note 1 (no split) | Tiny single-topic reference; one note. |
| testing-updates-plugins.md (1,615w) | note 7 (no split) | Under cap, single coherent checklist (one task cluster). |
| troubleshooting.md (2,387w) | note 8 (no split) | Under the 2,500w cap and a single tightly-coupled symptom-triage flow; selectively reproduce ≤6 of the 18 fences (First-60-seconds ladder + 2–3 representative symptom blocks), summarize the rest as prose. |

## Summary Statistics & Building Block Distribution

- Source pages: **5** (17,091 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0** (expected).
- BB distribution: **procedure ×8** (all eight notes are operator/maintainer how-to references). No concept/model/argument
  notes — these Help pages are uniformly task-oriented.
- Est. digest words ~5,180 (avg ~648/note); each note ≤750w, well under the 2,500w / 400-line cap.
- Source code fences (51 total across the 5 pages) distribute across the procedure notes; each note reproduces
  only its highest-signal commands (≤6 verbatim fences/note), summarizing the long env-var/runner lists as prose.
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every note meets the raised floor — **>=8
  ghosts; sibling `oc_*` + `entry_openclaw_docs` marked "(planned, this series)/(planned hub)". The rich
  `claude_code/` + `pi/` + `hermes_agent/` + `band/` coding-agent corpora + 253 `snippet_openclaw_*` provide
  the existing-note coverage.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

`term_dictionary/`, snippets in `code_snippets/` — ALL existing, repos in `areas/code_repos/`, docs in
`resources/documentation/`). Sibling `oc_*` docs (this hp02 series) and `entry_openclaw_docs` do not exist
yet → cited as "(planned, this series)"/"(planned hub)" toward the 10-doc floor; >=5 of each note's 10 docs
Relative paths are from a note at `resources/documentation/openclaw/oc_*.md`. Each link carries what-it-is +
relevance-to-THIS-note. Executor copies the link + description + relevance verbatim into `## Related Notes`.

### oc_help_scripts (8t · 10s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product whose monorepo this `scripts/` dir serves; relevance: the page documents repo helper scripts for OpenClaw ops.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — short-lived bearer credential; relevance: `gh-read` mints a GitHub-App installation token for repo-scoped read calls.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: the script splits App-token reads from personal-login writes.
- [OAuth 2.0](../../term_dictionary/term_oauth.md) — delegated-authorization framework; relevance: GitHub-App installation tokens are an OAuth-style scoped grant.
- [Cron](../../term_dictionary/term_cron.md) — time-based job scheduler; relevance: the auth-monitoring extras target systemd/Termux phone cron workflows.
- [npm](../../term_dictionary/term_npm.md) — Node package manager / registry; relevance: repo tooling + release-checklist context for when scripts are referenced.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: scripts are optional unless referenced in docs or release checklists (a CI concern).
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the repo scripts run on the Node toolchain that hosts OpenClaw.

**Docs**
- [CC: Web Setup Scripts](../claude_code/cc_web_setup_scripts.md) — helper-scripts doc for a sibling coding-agent tool; relevance: direct parallel to OpenClaw's optional repo helper scripts.
- [CC: GitHub Actions](../claude_code/cc_github_actions.md) — GitHub automation reference; relevance: parallels the `gh`/GitHub-App automation `gh-read` wraps.
- [CC: GitHub Actions Cloud Providers](../claude_code/cc_github_actions_cloud_providers.md) — CI cloud-credential wiring; relevance: parallels env-based token/credential injection for repo automation.
- [Hermes: Contributing / Dev Setup](../hermes_agent/hermes_contributing_dev_setup.md) — repo dev-environment + helper-script conventions; relevance: same "host-specific, read before running" script discipline.
- [Hermes: GitHub PR Review Webhook](../hermes_agent/hermes_guide_github_pr_review_webhook.md) — GitHub-App webhook automation guide; relevance: parallel GitHub-App installation-token usage pattern.
- [CC: Verification Loop](../claude_code/cc_verification_loop.md) — local proof / check workflow; relevance: scripts feed release-checklist verification flows.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) the test-runner map; relevance: the scripts page's own Related link to Testing.
- [oc_help_testing_live_models](oc_help_testing_live_models.md) — (planned, this series) live smoke commands; relevance: the page's own Related link to Testing-live.
- [oc_help_troubleshooting](oc_help_troubleshooting.md) — (planned, this series) triage hub; relevance: scripts back the auth-monitoring fixes troubleshooting routes to.
- [Pi: Development](../pi/pi_development.md) — coding-agent dev/build workflow; relevance: cross-tool parallel for repo dev scripts + checklists.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo hosting `scripts/`; relevance: this page documents that repo's helper-script directory.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/security subsystem; relevance: the auth-monitoring scripts + `gh-read` token discipline live in this surface.

- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: the page says "prefer the CLI" over scripts — this is the CLI surface.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: shows how `openclaw models status --check` (the CLI auth-monitor) dispatches.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — root/permission guard for CLI; relevance: host-specific script-vs-CLI safety the page warns about.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profile resolution; relevance: the App-token-vs-login split the scripts manage.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence ordering; relevance: env-var override order mirrors `gh-read`'s repo-resolution order.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: token-vs-password auth the auth-monitoring scripts surface.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe executor; relevance: code-level of the auth-monitoring probe the scripts wrap.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd service unit render; relevance: the systemd/Termux daemon workflows the phone auth scripts target.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — scheduled-task argv render; relevance: cross-platform scheduled-job analog of the cron auth-monitor.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — CLI doctor connectivity check; relevance: parallel CLI health/auth check the page prefers over a script.

### oc_help_testing_suites (9t · 12s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product under test; relevance: this is OpenClaw's "how we test" suite map.
- [Test Plan](../../term_dictionary/term_test_plan.md) — strategy mapping what runs where; relevance: the suite taxonomy + which-suite decision table IS a test plan.
- [Test-on-Demand](../../term_dictionary/term_test_on_demand.md) — on-demand/targeted test runs; relevance: the `pnpm test:changed` / scoped-lane targeted-run model.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: the CI-safe vs live distinction + offline regressions + contract tests run in CI.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: the gateway stability/e2e lanes drive `diagnostics.stability` over the Gateway WS RPC.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC over JSON; relevance: gateway RPC status + `wizard.start`/`wizard.next` WS RPC the suites assert.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: gateway tool-calling mock test + provider/channel contract tests.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP channel/tool contract + cron-MCP-cleanup coverage.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: the OpenShell backend e2e + exec/sandbox-policy boundaries.

**Docs**
- [CC: GitHub Actions](../claude_code/cc_github_actions.md) — CI workflow reference; relevance: parallels the CI lanes / scheduled live+e2e workflows the suites run under.
- [CC: GitLab CI/CD](../claude_code/cc_gitlab_ci_cd.md) — CI pipeline reference; relevance: cross-platform CI-pipeline analog for the offline-regression gate.
- [CC: Sandbox Limitations & Troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — sandbox e2e boundary notes; relevance: analog of the OpenShell/exec sandbox e2e boundary.
- [CC: Sandbox Runtime & Containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandboxed runtime model; relevance: parallels the OpenShell Docker-backed e2e sandbox.
- [CC: Verification Loop](../claude_code/cc_verification_loop.md) — local check/proof loop; relevance: the `pnpm build && pnpm check && pnpm test` full-gate workflow.
- [Hermes: Contributing / Dev Setup](../hermes_agent/hermes_contributing_dev_setup.md) — dev/test setup conventions; relevance: parallel coding-agent local test gate + scoped-run discipline.
- [oc_help_testing_qa_runners](oc_help_testing_qa_runners.md) — (planned, this series) QA-lab runner surface; relevance: the QA-runner sibling this page points to.
- [oc_help_testing_docker_runners](oc_help_testing_docker_runners.md) — (planned, this series) Docker runner catalog; relevance: the "works in Linux" Docker-lane sibling.
- [oc_help_testing_live_models](oc_help_testing_live_models.md) — (planned, this series) live model smokes; relevance: the page's "Live tests" pointer target.
- [oc_help_testing_updates_plugins](oc_help_testing_updates_plugins.md) — (planned, this series) update/plugin checklist; relevance: the page's "Testing updates and plugins" pointer.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo under test; relevance: the suites + Vitest configs live in this repo.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: gateway smoke / stability / e2e lanes target this surface.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension surface; relevance: the plugin/channel/provider contract tests iterate this.

- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WS connection setup; relevance: the WS RPC surface the stability/e2e lanes drive.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC request/response envelope; relevance: `diagnostics.stability` + gateway RPC status the suites assert.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — RPC error codes/version; relevance: contract-test assertions on RPC error shape.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: the gateway-network WS/HTTP surface e2e exercises.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env wiring; relevance: the loopback Gateway the stability/e2e suites boot.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — startup ACP prewarm; relevance: gateway boot-path the smoke lanes validate.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — OpenShell sandbox backend; relevance: the OpenShell e2e backend-smoke target.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — OpenShell fs bridge; relevance: the remote-canonical fs behavior the OpenShell e2e verifies.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the channel contract tests assert this shape.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: provider/plugin contract tests verify package shape.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method gating; relevance: gateway auth/routing integration tests.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup/config write; relevance: the e2e wizard flow (`wizard.start`/`wizard.next` writes config + auth).

### oc_help_testing_qa_runners (9t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the QA-lab runners exercise OpenClaw under live transport.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: Telegram/Discord bot tokens + Convex lease tokens the broker hands out.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: the lease/heartbeat/release broker auth contract.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared rotating credential set; relevance: the Convex-backed shared-credential broker IS a credential pool with leases.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: the gateway lanes the QA suites drive run over WS.
- [Data Quality](../../term_dictionary/term_data_quality.md) — output correctness/evidence; relevance: `qa-evidence.json` / scorecard / summary artifacts the runners emit.
- [Canary Testing](../../term_dictionary/term_canary_testing.md) — small pre-rollout probe; relevance: Telegram canary + mention-gating + command-addressing default scenarios.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-rate control; relevance: lease pool exhaustion / `POOL_EXHAUSTED` retry semantics + provider retry on 429.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback; relevance: the Mantis GitHub-App PR-evidence posting path.

**Docs**
- [CC: Slack Setup & Routing](../claude_code/cc_slack_setup_and_routing.md) — Slack channel transport config; relevance: parallels the Slack live-transport QA lane payload.
- [CC: Channels Setup](../claude_code/cc_channels_setup.md) — channel onboarding/config; relevance: analog of "adding a channel to QA" + per-channel credential shapes.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — rotating credential pool design; relevance: direct analog of the Convex lease/heartbeat credential broker.
- [Hermes: GitHub PR Review Webhook](../hermes_agent/hermes_guide_github_pr_review_webhook.md) — GitHub-App PR webhook automation; relevance: parallel of the Mantis GitHub-App PR-evidence path.
- [CC: GitHub Actions](../claude_code/cc_github_actions.md) — CI workflow reference; relevance: QA-Lab All-Lanes nightly + release-checks dispatch run as workflows.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) suite taxonomy; relevance: the parent "how we test" page these runners sit beside.
- [oc_help_testing_docker_runners](oc_help_testing_docker_runners.md) — (planned, this series) Docker runner catalog; relevance: the Docker QA lanes the runners hand off to.
- [oc_help_troubleshooting](oc_help_troubleshooting.md) — (planned, this series) channel-flow triage; relevance: channel-connected-but-no-flow QA failures route here.
- [oc_help_testing_live_media_creds](oc_help_testing_live_media_creds.md) — (planned, this series) live credential resolution; relevance: the same env-vs-Convex credential source the QA lanes use.
- [Band: Testing Agents](../band/band_testing_agents.md) — cross-tool agent-testing harness/runner doc; relevance: direct analog of the QA-lab test-runner harness that drives agents through live channels and captures evidence.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo hosting `qa-lab`; relevance: the QA runner harness lives in this repo (source-checkout only).
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: the live-transport channel lanes (Telegram/Discord/Slack/WhatsApp/Matrix).
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: the transport runners + credential payload shapes per channel.

- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport; relevance: the Telegram live QA lane + canary/mention scenarios.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram inbound dispatch; relevance: bot-to-bot mentioned-reply QA scenarios.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode transport; relevance: the Slack QA lane payload (`channelId`/bot/app tokens).
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord gateway intents; relevance: the Convex-managed live Discord QA lane.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist gating; relevance: the pairing/allowlist checks QA scenarios assert.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status/reactions; relevance: `channels status --probe` evidence the QA report captures.
- [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — credential pool selection; relevance: code-level analog of the Convex lease acquire/select.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — credential pool seeding; relevance: analog of broker `admin/add` pool population.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential-source resolution; relevance: env-vs-Convex credential-source selection the lanes use.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit gating; relevance: lease-exhaustion / retry-later semantics analog.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: the `chat.send` surface QA reply scenarios drive (RTT measurement).

### oc_help_testing_docker_runners (9t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the Docker runners install/update real OpenClaw packages in containers.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the entire runner family runs inside Linux Docker containers.
- [OCI](../../term_dictionary/term_oci.md) — Open Container Initiative image standard; relevance: the prebuilt `ghcr.io/openclaw/...` images the lanes build/pull.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: tarball pack + `npm install`-timeout-capped install lanes.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — `@scope/*` package namespaces; relevance: the `@openclaw/*` scoped plugin packages the lanes install.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: mcp-channels / agent-bundle-mcp-tools / cron-mcp-cleanup lanes.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: the gateway-network lane checks WS auth + `/healthz`/`/readyz`.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: the bare Node/Git runner image + bun global-install smoke.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the browser-cdp-snapshot Chromium-CDP lane.

**Docs**
- [CC: Devcontainer Setup](../claude_code/cc_devcontainer_setup.md) — containerized dev/test environment; relevance: direct analog of the Docker dev/test container model.
- [CC: Sandbox Filesystem & Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — container isolation controls; relevance: parallels the bind-mount/isolation conventions of the runners.
- [CC: Sandbox Runtime & Containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox container runtime; relevance: analog of the OpenShell/exec container isolation.
- [Hermes: Docker Volumes & Supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker bind-mount + process supervision; relevance: direct analog of the runner bind-mount/auth-home conventions.
- [Hermes: Terminal Backends](../hermes_agent/hermes_terminal_backends.md) — exec/terminal sandbox backends; relevance: parallel of the container exec/OpenShell backend.
- [Band: Coding Agents Deployment](../band/band_coding_agents_deployment.md) — coding-agent container deployment; relevance: cross-tool parallel for container-based agent test/deploy.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) suite taxonomy; relevance: the "works in Linux" Docker bucket of the parent test map.
- [oc_help_testing_updates_plugins](oc_help_testing_updates_plugins.md) — (planned, this series) update/plugin checklist; relevance: the Docker upgrade-survivor/plugin lanes documented in detail there.
- [oc_help_testing_live_media_creds](oc_help_testing_live_media_creds.md) — (planned, this series) live media + creds; relevance: the live-media Docker shards + auth-home staging.
- [in02: install/docker](oc_install_docker.md) — (planned in02) Docker install + permissions; relevance: the page's own permissions/EACCES reference.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo packed into Docker; relevance: the lanes pack/install this repo's tarball.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: gateway-network/healthz/readyz + live-gateway lanes.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — Control-UI / app surfaces; relevance: the Open WebUI / Control-UI compatibility smoke lanes.

- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: the gateway-network WS-auth + health-probe lane target.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: the env-var/bind-mount conventions the runners set in-container.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP HTTP loopback; relevance: the mcp-channels / bundle-mcp-tools stdio-MCP lanes.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service notifications; relevance: the cron-mcp-cleanup teardown lane.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — OpenShell container backend; relevance: container exec/sandbox isolation the lanes exercise.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/enable/disable lifecycle; relevance: the plugin-lifecycle-matrix Docker lane.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitize; relevance: the release-media-memory image-attachment Docker smoke.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the mocked-OpenAI onboarding + agent-turn Docker lanes.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboard wizard config; relevance: the onboard/typed-onboarding Docker journeys.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker exec environment; relevance: direct analog of the containerized test-runner environment.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process kill-tree; relevance: container teardown / stale-container cleanup the scheduler performs.

### oc_help_testing_live_models (10t · 12s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the live smokes drive OpenClaw's gateway+agent pipeline.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: every direct/gateway probe targets a real model.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: Claude CLI/ACP/Codex defaults + `anthropic/claude-opus-4-6` in the matrix.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client bind protocol; relevance: the ACP bind smoke + embedded `acpx` backend.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent execution wrapper; relevance: the Codex app-server harness lane (`agentRuntime.id: "codex"`).
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: the read / exec+read tool probes asserted per model.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP cron-tool loopback probes in the harness/ACP lanes.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: the OpenAI/Gemini/DeepSeek/Z.AI/MiniMax/Grok provider matrix.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: Codex/Antigravity OAuth auth + Claude subscription OAuth for live runs.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider/model registry; relevance: `discoverModels` / `openclaw models list` selects which models the suite probes.

**Docs**
- [CC: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — cloud model-provider auth; relevance: analog of cloud-provider live-auth/key resolution.
- [Pi: Provider Auth](../pi/pi_provider_auth.md) — model-provider key resolution; relevance: parallels `getApiKeyForModel` / profile-vs-env key selection.
- [CC: Login & Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth-failure debug; relevance: the "no creds" live-test debug flow.
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — multi-provider cloud inference; relevance: direct analog of the provider/model live matrix.
- [Hermes: Provider XAI/Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — OAuth provider auth; relevance: parallel of Antigravity/Codex OAuth-bridge live auth.
- [Pi: Provider Auth (cross-tool)](../pi/pi_quickstart.md) — provider/model quickstart auth; relevance: cross-tool parallel of selecting a provider/model with keys.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) parent test map; relevance: the "Live tests" pointer originates there.
- [oc_help_testing_live_media_creds](oc_help_testing_live_media_creds.md) — (planned, this series) media live + creds; relevance: the sibling live page sharing credential resolution.
- [oc_help_testing_docker_runners](oc_help_testing_docker_runners.md) — (planned, this series) Docker runners; relevance: the live-model Docker lanes (`test:docker:live-*`).
- [Band: Codex Adapter](../band/band_adapter_codex.md) — cross-tool Codex agent-runtime adapter; relevance: direct analog of the Codex app-server harness smoke lane (`agentRuntime.id: "codex"`) the live test drives.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo under live test; relevance: the live test files (`*.live.test.ts`) live here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/model profiles; relevance: `models.profiles.live.test.ts` direct-model probes.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the Layer-2 gateway+dev-agent smoke.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: per-provider live tests (Z.AI/Ollama/etc.).

- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: the ACP bind smoke target.
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — `acpx` runtime contract; relevance: the embedded `acpx` backend the bind smoke uses.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — `/acp spawn --bind here` thread bind; relevance: exactly the bind flow the live test validates.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ACP subagent spawn; relevance: the harness/ACP sub-agent probe.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: the Claude direct/gateway model probes.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: `openai/gpt-5.5` direct + Codex-routed gateway probes.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: the `openrouter/...` aggregator matrix coverage.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: the small-model Ollama local/cloud live smoke.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog/discovery; relevance: `getApiKeyForModel` / model enumeration the suite drives.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalize; relevance: `discoverModels(...)` the matrix authoritatively reads.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image attach validate; relevance: the image probe (PNG cat+code) in the gateway live smoke.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — `chat.send` handler; relevance: the gateway `agent`/`chat.send` surface the live smoke turns through.

### oc_help_testing_live_media_creds (9t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: media live suites run through OpenClaw's bundled provider runtime.
- [LLM](../../term_dictionary/term_llm.md) — large/foundation model; relevance: media providers are model-backed generation services.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: live-test credential resolution (profile store vs env fallbacks).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: external-CLI OAuth refresh staged into the temp home during live runs.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — per-agent stored credentials; relevance: `auth-profiles.json` profile-key store the live tests read.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external providers; relevance: Deepgram/BytePlus/ComfyUI/FAL/Runway/Vydra/MiniMax media providers.
- [Function Calling](../../term_dictionary/term_function_calling.md) — capability dispatch; relevance: provider `generate`/`edit` capability dispatch in the shared media runtime.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: the staged temp-home isolation that keeps probes off the real workspace.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model/media provider; relevance: each media provider is a bundled provider plugin.

**Docs**
- [Pi: Provider Auth](../pi/pi_provider_auth.md) — provider credential-source resolution; relevance: direct parallel of profile-store-vs-env live-test key resolution.
- [CC: SDK Credential & Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — secure credential store + fs controls; relevance: the never-commit credential discipline + staged temp-home isolation.
- [CC: Agent SDK Install & Auth](../claude_code/cc_agent_sdk_install_and_auth.md) — env-vs-profile key selection; relevance: how live tests pick env keys ahead of stale profile keys.
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — multi-provider cloud inference + auth; relevance: analog of the bundled media-provider sweep.
- [Hermes: Security / Isolation / Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation discipline; relevance: parallels the staged-home + never-commit credential model.
- [CC: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — provider key/auth setup; relevance: cross-provider live-auth setup analog.
- [oc_help_testing_live_models](oc_help_testing_live_models.md) — (planned, this series) live model smokes; relevance: the sibling live page sharing the credential-resolution rules.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) parent test map; relevance: the live-suite pointer originates there.
- [oc_help_testing_docker_runners](oc_help_testing_docker_runners.md) — (planned, this series) Docker runners; relevance: the live-media Docker shards + auth-home staging.
- [Hermes: Image Generation](../hermes_agent/hermes_image_generation.md) — image-generation provider integration; relevance: direct analog of the image-generation media live suite (the `infer image generate` provider sweep).

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo under live test; relevance: the media live test files live here.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: Deepgram/TTS/audio live lanes.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: image/music/video generation providers.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/credential surface; relevance: the never-commit credential discipline.

- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram speech-to-text; relevance: the Deepgram audio live lane.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs text-to-speech; relevance: TTS media-provider live coverage.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: the safe local `infer tts convert --local` media smoke.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the media-provider generate/transcribe pipeline.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: the `voicecall setup/smoke` readiness live check.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — voice webhook signature; relevance: the Twilio/Telnyx/Plivo public-webhook readiness requirement.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: staging external-CLI OAuth auth into the live temp home.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence; relevance: env-keys-ahead-of-profile resolution the media tests use.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential-source resolution; relevance: analog of profile-store-vs-env credential discovery.
- [snippet_hermes_agent_tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — MCP/tool OAuth; relevance: external-service OAuth credential handling parallel.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider auth/dispatch; relevance: the provider-plugin generate-capability dispatch pattern.

### oc_help_testing_updates_plugins (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product/package; relevance: the checklist proves the installable OpenClaw package can update real user state.
- [npm](../../term_dictionary/term_npm.md) — Node package manager/registry; relevance: tarball pack / registry install / managed-npm dependency lanes.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — `@scope/*` namespaces; relevance: `@openclaw/*` owned-plugin update-sync compatibility.
- [Version Set](../../term_dictionary/term_version_set.md) — pinned build/version collection; relevance: Package Acceptance baselines (`last-stable-4`, `2026.4.23` boundary) + version pinning.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: Package Acceptance is the GitHub-native release/package gate.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider/channel; relevance: plugin install/load/update/uninstall contracts the lanes protect.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `package.json` plugin descriptor; relevance: the `openclaw.extensions` manifest shape package acceptance validates.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the upgrade-survivor / published-upgrade-survivor Docker lanes.
- [Blue-Green Deployment](../../term_dictionary/term_blue_green_deployment.md) — old→new cutover with rollback; relevance: analog of published-baseline → candidate-tarball upgrade migration.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — repeat-safe operation marker; relevance: the "unchanged plugin update is a stable no-op" contract.

**Docs**
- [CC: Plugin Marketplaces & Install](../claude_code/cc_plugin_marketplaces_and_install.md) — plugin install-source model; relevance: parallels local/git/npm/ClawHub install-source lanes.
- [CC: Managed Plugin Policy Settings](../claude_code/cc_managed_plugin_policy_settings.md) — install-policy controls; relevance: analog of `security.installPolicy` + trusted `@openclaw/*` exceptions.
- [CC: Plugin Dependencies](../claude_code/cc_plugin_dependencies.md) — managed plugin npm dependencies; relevance: the managed-npm-per-plugin dependency cleanup the migration lane proves.
- [CC: Update & Release Channels](../claude_code/cc_update_and_release_channels.md) — update/release-candidate channels; relevance: the update-channel-switch + release-default proof stack.
- [CC: Plugin Caching & Troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin install-failure triage; relevance: the failure-triage / artifact-identity section.
- [CC: Plugin Manifest Schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest schema; relevance: parallel of the `package.json` `openclaw.extensions` contract.
- [oc_help_testing_docker_runners](oc_help_testing_docker_runners.md) — (planned, this series) Docker runner catalog; relevance: the upgrade-survivor / plugin Docker lanes referenced here.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) parent test map; relevance: the broader runner map this checklist points back to.
- [oc_help_troubleshooting](oc_help_troubleshooting.md) — (planned, this series) triage hub; relevance: install-policy / suspicious-ownership symptoms cross-link here.
- [in02: install/docker](oc_install_docker.md) — (planned in02) Docker install + permissions; relevance: the Docker-lane host permissions context.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo/package; relevance: the package tarball + update command under test.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension surface; relevance: plugin lifecycle install/update/uninstall the lanes assert.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/install-policy; relevance: install-policy / suspicious-ownership gates.

- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/enable/disable/uninstall; relevance: exactly the lifecycle the plugin-lifecycle-matrix lane asserts.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the `dist/postinstall-inventory.json` / package-completeness contract.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: the `openclaw.extensions` runtime-file entries package acceptance checks.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust scan findings; relevance: dependencies "scanned before trust" during install.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: install-policy fail-closed + trusted `@openclaw/*` resolution.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — install-policy gating; relevance: `security.installPolicy` blocked/failed-closed behavior.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — config migration import; relevance: the doctor-owned legacy cleanup / upgrade-survivor state migration.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair flow; relevance: `doctor --fix --non-interactive` legacy-state repair the lanes require.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: analog of `openclaw plugins install` from local/git/npm/registry.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor/repair; relevance: parallel of post-update plugin dependency cleanup.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: analog of the `package.json` extensions-shape acceptance check.

### oc_help_troubleshooting (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the symptom-first triage hub for "OpenClaw is not working".
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: browser/MCP tool failures + "assistant feels limited / missing tools".
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: the tool-profile / missing-tools triage (messaging vs coding vs full).
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-rate control; relevance: Anthropic long-context 429 + "too many failed authentication attempts" lockout.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the device-token retry + `AUTH_TOKEN_MISMATCH` Control-UI path.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: origin-not-allowed / unauthorized / device-identity-required symptoms.
- [Cron](../../term_dictionary/term_cron.md) — time-based scheduler; relevance: the cron/heartbeat-did-not-fire symptom block.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: `exec host=sandbox requires a sandbox runtime` / approval symptoms.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the browser-tool / CDP failure signatures block.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider/plugin; relevance: plugin install / policy / suspicious-ownership recovery.

**Docs**
- [CC: Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — config-triage workflow; relevance: direct analog of the `status`/`doctor` first-60-seconds config triage.
- [CC: Login & Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth-failure debug; relevance: analog of the unauthorized / token-mismatch / lockout symptoms.
- [CC: Chrome Setup & Troubleshooting](../claude_code/cc_chrome_setup_and_troubleshooting.md) — browser-tool failure fixes; relevance: parallel of the browser/CDP failure-signature block.
- [CC: Request & Quality Errors](../claude_code/cc_request_and_quality_errors.md) — request/quality error triage; relevance: analog of provider-compat / agent-turn failure fixes.
- [CC: Server & Usage Limit Errors](../claude_code/cc_server_and_usage_limit_errors.md) — usage-limit/429 errors; relevance: direct analog of the Anthropic long-context 429 symptom.
- [CC: Plugin Caching & Troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin-blocked triage; relevance: analog of install-policy / blocked-plugin recovery.
- [oc_help_testing_suites](oc_help_testing_suites.md) — (planned, this series) test map; relevance: the FAQ/testing cross-links from the triage hub.
- [oc_help_testing_updates_plugins](oc_help_testing_updates_plugins.md) — (planned, this series) update/plugin checklist; relevance: install-policy / ownership recovery references it.
- [gw07: gateway/troubleshooting](oc_gateway_troubleshooting.md) — (planned gw07) gateway deep runbook; relevance: the page's own deep-link target for gateway symptoms.
- [nd02: nodes/troubleshooting](oc_nodes_troubleshooting.md) — (planned nd02) node tools deep runbook; relevance: the node-paired-but-tool-fails deep link.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo; relevance: the CLI triage commands (`status`/`doctor`/`gateway probe`) live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: gateway-start / connectivity-probe / bind-refused symptoms.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: channel-connected-but-no-flow / mention-gating symptoms.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/install-policy; relevance: install-policy / suspicious-ownership recovery.

- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — gateway connect error codes; relevance: `gateway connect failed` / connectivity-probe symptom signatures.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth authorize dispatch; relevance: unauthorized / `AUTH_TOKEN_MISMATCH` / origin-not-allowed paths.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticket; relevance: the device-token retry / Control-UI-will-not-connect symptoms.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit + install policy; relevance: the failed-auth-attempt lockout + blocked-plugin-install symptoms.
- [snippet_openclaw_acp_translator_rate_limit](../../code_snippets/snippet_openclaw_acp_translator_rate_limit.md) — rate-limit handling; relevance: analog of the Anthropic long-context 429 handling.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: `SYSTEM_RUN_DENIED: approval required` / exec-asks-for-approval symptoms.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: node-paired-but-tool-fails permission/capability symptoms.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: `pairing request` / allowlist / mention-required no-reply symptoms.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: blocked-by-install-policy / suspicious-ownership recovery.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service notifications; relevance: the cron/heartbeat-did-not-fire / skipped-reason symptoms.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair flow; relevance: `openclaw doctor --fix` recovery the triage ladder runs.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| OpenClaw test suites (unit / integration / e2e / live / stability) | Documented as procedure in notes 2/5 (`oc_help_testing_*`); link existing `term_test_plan`/`term_test_on_demand`. No new term. |
| QA Lab / qa-channel / qa-matrix / live-transport lanes | Subjects of dedicated concept doc pages (co05/co06/ch04) — link those (planned); covered as runner procedure in note 3. No new term. |
| Convex credential broker (lease/heartbeat/release) | OpenClaw-specific QA infra → documented inline in note 3; link `term_authentication`/`term_oauth_token`. No new term. |
| Package Acceptance / upgrade-survivor / install policy | OpenClaw release/plugin vocabulary → notes 7/8; link `term_ci_cd`/`term_version_set`/`term_provider_plugin`. No new term. |
| ACP bind / Codex app-server harness | Agent-runtime vocabulary → note 5; link existing `term_acp_agent_client_protocol`/`term_agent_harness`. No new term. |
| gh-read / GitHub App installation token | Tooling detail in note 1; link `term_oauth_token`/`term_authentication`. No new term. |
| Provider/model names (OpenAI, Gemini, DeepSeek, Z.AI, MiniMax, Grok, Deepgram, BytePlus, ComfyUI, FAL, Runway, Vydra) | Documented as config/coverage, NOT promoted to term notes; link `term_llm`/`term_claude`/`term_third_party_genai_services`. No new term. |
| Triage symptoms (no-replies, gateway-down, browser/exec/cron failures) | Note 8 procedure; link `term_mcp`/`term_cron`/`term_sandbox`/`term_rate_limiting`. No new term. |

**Net: 0 new `term_dictionary` captures expected.** No genuinely cross-cutting reusable term lacks an existing
note — testing/CI/plugin/Docker/OAuth/sandbox vocabulary is already covered (`term_test_plan`, `term_ci_cd`,
`term_docker`, `term_npm`, `term_provider_plugin`, `term_oauth_token`, `term_sandbox`, `term_mcp`, …, all

## Term-Note Authoring Requirements

**N/A (0 new terms).** Inherited from master: if augment's Step 2d re-scan surfaces a genuinely reusable
cross-cutting term with no doc-page home AND no existing note, it is captured via `/tessellum-capture-term-note`
in an `oc_*` digest note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single phase (8 notes, P2). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` (YAML field order, itemized lists, quoted year tags, `## Overview` + `## Related Notes` present) |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/help/<page>.md`; every claim/command traceable to source, no invented behavior |
| G3 | Density + Coverage | ≤2,500w / ≤400 lines / ≤6 code blocks per note; every mapped H2/H3 covered; one BB per note |
| G4 | Cross-Reference | ≥6 relevance-selected term links + repo/doc/sibling links per note, each with a relevance statement (indexed `[text](path.md)` format) |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken links after incremental reindex |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island) |
| G8 | In-degree ≥1 | `note_links` confirms in-degree ≥1 per new note (satisfied via `entry_openclaw_docs.md` + term/repo backlinks) |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_help_scripts oc_help_testing_suites oc_help_testing_qa_runners oc_help_testing_docker_runners oc_help_testing_live_models oc_help_testing_live_media_creds oc_help_testing_updates_plugins oc_help_troubleshooting"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format + LINK errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION ($sec): $n"; done
  # source_url present (REQUIRE_SOURCE_URL)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density: words + code-block caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # sibling-prefix self-reference sanity (SIBLING_PREFIX)
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING LINK: $n"
done

# G5 ghost / G6 broken links after reindex
bash scripts/update_notes_database.sh --force
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences (page) | Reproduced ≤6? | Within caps? |
|---|---|---|---:|---|---|---|
| 1 | oc_help_scripts | procedure | 280 | 0 | n/a (0) | ✅ |
| 2 | oc_help_testing_suites | procedure | 750 | ~5 (of testing.md 11) | ≤6 (quick-start + temp-dir + contract cmds) | ✅ |
| 3 | oc_help_testing_qa_runners | procedure | 700 | ~4 | ≤6 (qa suite/telegram + Convex endpoint snippet) | ✅ |
| 4 | oc_help_testing_docker_runners | procedure | 700 | ~3 | ≤6 (representative `test:docker:*` + override snippet) | ✅ |
| 5 | oc_help_testing_live_models | procedure | 750 | ~6 (of testing-live.md 13) | ≤6 (model select + ACP/Codex recipes) | ✅ |
| 6 | oc_help_testing_live_media_creds | procedure | 650 | ~5 | ≤6 (tts/voicecall + image-infer + narrowing env) | ✅ |
| 7 | oc_help_testing_updates_plugins | procedure | 650 | ~5 (of 9) | ≤6 (local proof + Package Acceptance + update-migration) | ✅ |
| 8 | oc_help_troubleshooting | procedure | 700 | ~5 (of 18) | ≤6 (First-60s ladder + 2–3 symptom blocks) | ✅ |

No note approaches the 2,500w / 400-line cap. Code-heavy pages (testing.md 11, testing-live.md 13,
troubleshooting.md 18) are split / selectively reproduced so each note keeps ≤6 verbatim fences; the long
Docker-runner env lists and remaining symptom ladders are summarized as prose.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as the W1 master pre-step) under a **"Help"** section
cluster (scripts · testing suites · QA runners · Docker runners · live models · live media+creds · updates &
plugins · troubleshooting). Each note receives its entry-point back-link at finalization (this satisfies G7/G8
inbound discoverability). No standalone entry point for hp02 (it is one section of the 665-page docs hub).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all sources below confirmed to exist
2026-06-20):
- `entry_openclaw_docs.md` (planned hub) → all 8 notes (primary anti-island guarantee).
- `repo_openclaw.md` → notes 1, 2, 4, 7, 8 (monorepo ↔ its test/scripts/troubleshooting docs).
- `repo_openclaw_gateway.md` → notes 2, 4, 5, 8 (gateway smoke/stability/network/triage).
- `repo_openclaw_extensions.md` → notes 2, 7 (plugin/channel contract + lifecycle tests).
- `repo_openclaw_extensions_llm_providers.md` → notes 5, 6 (provider/media live tests).
- `repo_openclaw_security.md` → notes 1, 6, 7, 8 (auth scripts, never-commit creds, install policy, ownership).
- `repo_openclaw_channels.md` → notes 3, 8 (live-transport QA + channel-flow triage).
- `term_openclaw.md` → notes 2, 8 (product ↔ how-we-test + triage).
- `term_docker.md` → note 4; `term_mcp.md` → notes 5, 8; `term_acp_agent_client_protocol.md` → note 5.

## Pacing Rules (inherited from master)

One execution phase, 8 notes (≤ fan-out cap; no sub-batching needed). Re-read each source page at execute;
reproduce commands verbatim; one BB per note; 8 gates before commit. `git pull --rebase --autostash origin main`
first; incremental reindex; verify `note_links` + 0 broken links; commit + push the phase (no Claude co-author
trailer).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment; floors raised + per-note mapping LOCKED) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope.** xref-augment pass on sub-plan hp02 (Help: scripts, testing, testing-live, testing-updates-plugins,
troubleshooting). Re-read all 5 source pages under `inbox/openclaw_docs/help/` (measured: scripts 239w /
testing 9,047w / testing-live 3,803w / testing-updates-plugins 1,615w / troubleshooting 2,387w = 17,091w,
matching the plan's Source table). Replaced `## Candidate Cross-References` with `## Per-Note Related Notes
Mapping (LOCKED — xref-augment 2026-06-21)` at RAISED FLOORS: **>=8 terms · >=10 existing snippets · >=10

**What was locked (per-note counts; floors met for all 8):**

| # | Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| 1 | oc_help_scripts | 8 | 10 | 11 (7 existing / 4 planned) | 2 | ✅ |
| 2 | oc_help_testing_suites | 9 | 12 | 11 (6 existing / 5 planned) | 3 | ✅ |
| 3 | oc_help_testing_qa_runners | 9 | 11 | 10 (5 existing / 5 planned) | 3 | ✅ |
| 4 | oc_help_testing_docker_runners | 9 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| 5 | oc_help_testing_live_models | 10 | 12 | 10 (6 existing / 4 planned) | 4 | ✅ |
| 6 | oc_help_testing_live_media_creds | 9 | 11 | 10 (6 existing / 4 planned) | 4 | ✅ |
| 7 | oc_help_testing_updates_plugins | 10 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| 8 | oc_help_troubleshooting | 10 | 11 | 11 (6 existing / 5 planned) | 4 | ✅ |

note_id=…"` on 2026-06-21: 68 distinct terms/repos checked (all OK), 100+ snippet ids checked (all OK —
(all OK except `pi_provider` and `snippet_openclaw_credential_pool`, which were dropped and NOT cited). The
253-snippet `snippet_openclaw_*` corpus + the `claude_code/`/`pi/`/`hermes_agent/`/`band/` doc corpora supply
the existing-note coverage. Sibling `oc_*` docs (hp02 series + gw07/nd02/in02) and `entry_openclaw_docs` do

**New-term candidates: NONE.** Re-read confirmed the master Undigested-Terms ownership rule holds — all
testing/CI/Docker/plugin/OAuth/sandbox/MCP/credential/provider/browser vocabulary already has existing term
notes (`term_test_plan`, `term_test_on_demand`, `term_ci_cd`, `term_docker`, `term_oci`, `term_npm`,
`term_npm_scoping`, `term_node_js`, `term_provider_plugin`, `term_plugin_manifest`, `term_oauth_token`,
`term_authentication`, `term_credential_pool`, `term_sandbox`, `term_mcp`, `term_function_calling`,
`term_websocket`, `term_json_rpc`, `term_canary_testing`, `term_rate_limiting`, `term_webhook`,
`term_data_quality`, `term_version_set`, `term_blue_green_deployment`, `term_idempotency_key`,
`term_third_party_genai_services`, `term_acp_agent_client_protocol`, `term_agent_harness`,
`term_model_catalog`, `term_browser_automation`, `term_auth_profile`, `term_cron`, `term_llm`, `term_claude`,
ACP-bind/Codex-harness, gh-read) are doc-page subjects covered as `oc_*` procedure content + linked to
existing terms — never inlined, never promoted to new term notes. **Best-fit glossary (if a term ever
surfaces): `acronym_glossary_generative_ai.md` / `acronym_glossary_engineering.md`.** Net: 0 new
`term_dictionary` captures.

**Issues:** none. Plan was already structurally complete (Section Coverage Map, Split Decisions, Density
Re-Assessment, 9-GATE table, Validation Scripts, Undigested Terms Plan, Entry Point Decision, Inlinks,
Pacing — all present and inherited from the master). This pass only raised the cross-reference floors and
locked the per-note mapping.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_hp02.md   Date: 2026-06-21
```

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step — >=8 terms + floors, relevance-selected, with relevance statements | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 8 notes meet >=8 terms / >=10 snippets / >=10 docs; every link rendered `- [Name](relpath.md) — what-it-is; relevance: …`. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present (G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7 Discoverability, G8 in-degree>=1) — single phase, all 8 gates. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)`: contributes 8 rows to `entry_openclaw_docs.md` (W1 master pre-step) under a "Help" section cluster; no standalone hp02 entry point (1 section of 665-page hub). |
| CP4 | Size — plan manageable (≤30) | **PASS** | 8 notes, single phase, well under the 30-note cap / fan-out cap. |
| CP5 | Format derived from existing target-dir notes | **PASS** | YAML field order + `# OpenClaw — …` → `## Overview` → source-mirrored H2/H3 → `## Related Notes` → `## References` → footer, derived from the `cc_*`/`pi_*` doc corpora per the master Format Definition (not invented). |
| CP6 | Density — borderline → split promoted | **PASS** | Density Re-Assessment: all 8 notes ≤750w / ≤6 code; testing.md (9,047w) split ×3, testing-live.md (3,803w) split ×2 at task-cluster/H2 boundaries; no note approaches the 2,500w/400-line cap. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-read all 5 pages 2026-06-21; measured words match the plan's Source table (17,091w total) within ±0%; code-fence counts confirmed (testing 11, testing-live 13, troubleshooting 18). |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (8 rows, all dispositioned "No new term" with owner note + existing-term link); `## Term-Note Authoring Requirements` present (N/A — 0 new terms — inherited from master, `/tessellum-capture-term-note` mandate if one ever surfaces). |
| CP8f | Slug specificity / collision (all-notes dedup) | **PASS** | 0 new term slugs → no specificity/collision risk. Dedup audit: all 8 `oc_help_*` doc slugs are NEW (no existing `oc_*` in DB) and do NOT duplicate any existing term/doc note (the concepts are OpenClaw-specific procedure pages, distinct from the generic `term_*` they link). |
| CP9 | Discoverability / inlinks (G7/G8 executed, no islands) | **PASS** | `## Inlinks (existing notes → new notes)` table maps outside-folder inbound links for all 8 notes (`entry_openclaw_docs` → all 8, plus repo_openclaw* / term backlinks); G7+G8 in the gate table; every new note ends with in-degree >=1. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
