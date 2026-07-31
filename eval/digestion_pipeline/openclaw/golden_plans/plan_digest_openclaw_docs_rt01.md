---
title: Sub-Plan rt01 — OpenClaw Docs: Top-level (runtime, auth, automation, channels, CI, ClawHub, CLI)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["agent-runtime-architecture", "auth-credential-semantics", "automation", "channels", "ci", "clawhub", "cli"]
---

# Sub-Plan rt01: Top-level

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`) · format · dedup (3-way vs term_dictionary +
> documentation + `repo_openclaw*`) · 9-GATE · cross-refs · entry-point (`entry_openclaw_docs.md`) are ALL
> inherited from the master; this file is authored from a fresh re-read + `wc -w`/grep measurement of its 7
> assigned top-level pages and carries `## Candidate Cross-References` (locked per-note mapping is done at augment).

## Scope

The 7 top-level (un-prefixed) OpenClaw doc pages — the cross-cutting index/overview pages that the deeper
sections (cli/, gateway/, channels/, automation/, clawhub/, concepts/) hang off. They cover: the built-in
**agent runtime architecture** (module layout, boundaries, manifests, runtime selection), the canonical
**auth credential eligibility + resolution semantics** (auth-profile probe/resolution contract), the
**automation** mechanism chooser (cron / heartbeat / tasks / hooks / standing orders / commitments / Task
Flow), the **chat channels** overview (supported messaging platforms), the **CI pipeline** (job graph, scope
gates, release-validation umbrellas, CodeQL, local/Docker equivalents — by far the largest page), the public
**ClawHub** registry (discovery/install/publish/security/CLI), and the **CLI reference index** (command tree,
global flags, output modes). **Priority: P1 (Phase A, Top-level)** — these are the architecture/runtime/CLI
vocabulary the rest of the corpus references. The code-side `repo_openclaw*` notes (15) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 12,752 measured words. **Planned: 10 notes** (ci.md splits 4-way).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| agent-runtime-architecture | /agent-runtime-architecture | 280 | 1 | 5 | 0 | concept |
| auth-credential-semantics | /auth-credential-semantics | 702 | 0 | 10 | 2 | model |
| automation | /automation | 1,013 | 1 | 4 | 8 | concept |
| channels | /channels | 574 | 0 | 3 | 0 | concept |
| ci | /ci | 8,419 | 18 | 21 | 14 | mixed (concept + procedure + argument → split ×4) |
| clawhub | /clawhub | 771 | 8 | 7 | 0 | procedure |
| cli | /cli | 993 | 1 | 7 | 0 | model (command-tree reference index) |

Code counts = fence lines / 2 (`grep -c '^\`\`\`'` ÷ 2). Total source = 12,752 words, 29 code blocks.

## Content Strategy

- **Prioritize**: the auth credential eligibility/resolution semantics (a hard runtime contract every model
  call depends on; stable probe reason codes) and the CI pipeline structure + release-validation flow (the
  page is enormous and operationally load-bearing for contributors/release coordinators).
- **Split**: `ci.md` (8,419w / 18 code / 21 H2 / 14 H3, mixed BB) SPLITS 4-way along task clusters —
  (a) pipeline structure/scoping/runners (concept+model), (b) release-validation umbrellas + acceptance/smoke/
  QA/perf (procedure), (c) CodeQL security + critical-quality scanning (argument/model), (d) local + Docker E2E
  + Testbox/Crabbox + maintenance workflows (procedure). No other page exceeds caps; each of the other 6 = 1 note.
- **Link-out (do NOT redefine here)**: per-command CLI pages (`cli/*` → cl01–cl09), per-channel pages
  (`channels/*` → ch01–ch06), per-automation pages (`automation/*` → au01), per-ClawHub pages (`clawhub/*` →
  cw01–cw03), gateway secrets/oauth/heartbeat (gw0x / co0x), provider/model config (`providers/models` → pr05);
  existing terms (`term_openclaw`, `term_mcp`, `term_acp_agent_client_protocol`, `term_ci_cd`,
  `term_authentication`, `term_oauth`, `term_cron`, `term_docker`, `term_devops`, …) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_agent_runtime_architecture.md` | concept | agent-runtime-architecture.md: Runtime Layout, Boundaries, Manifests, Runtime Selection | 420 | The built-in OpenClaw agent runtime: module layout (`src/agents/*`, `packages/agent-core`, `src/llm/*`), core-vs-plugin boundaries and SDK barrels, resource-package manifests (extensions/skills/prompts/themes), and runtime-id selection (`openclaw`/`auto`/plugin harnesses). |
| 2 | `oc_auth_credential_semantics.md` | model | auth-credential-semantics.md: Stable probe reason codes, Token credentials (eligibility/resolution), Agent copy portability, Config-only auth routes, Explicit auth order filtering, Probe target resolution, External CLI credential discovery, OAuth SecretRef Policy Guard, Legacy-Compatible Messaging | 700 | The canonical auth-profile credential contract shared by `resolveAuthProfileOrder` / `resolveApiKeyForProfile` / `models status --probe` / `doctor-auth`: stable probe reason codes, token eligibility/resolution + `expires` validation, agent copy portability, config-only (`aws-sdk`) routes, explicit `auth.order` filtering, external-CLI discovery modes, and the OAuth SecretRef policy guard. |
| 3 | `oc_automation_overview.md` | concept | automation.md: Quick decision guide (+ Cron-vs-Heartbeat table), Core concepts (cron, tasks, commitments, Task Flow, standing orders, hooks, heartbeat), How they work together | 650 | OpenClaw's automation mechanism chooser: when to use scheduled tasks (cron), heartbeat, background tasks, inferred commitments, Task Flow, hooks, and standing orders; the cron-vs-heartbeat comparison; and how the seven mechanisms compose for background work. |
| 4 | `oc_channels_overview.md` | concept | channels.md: Delivery notes, Supported channels, Notes | 500 | The chat-channels overview: how OpenClaw connects messaging platforms through the Gateway, cross-channel delivery notes (Telegram media conversion, Slack MPIM group routing, WhatsApp install-on-demand, bot-loop protection, ambient room events), the ~30 supported-channel matrix, and setup/group/pairing notes. |
| 5 | `oc_ci_pipeline_overview.md` | concept | ci.md: Pipeline overview, Fail-fast order, PR context and evidence, Scope and routing, ClawSweeper activity forwarding, Manual dispatches, Runners | 700 | The OpenClaw CI job graph and how scoping decides what runs: the `preflight`-classified job table, fail-fast ordering, the external-contributor PR-evidence gate, changed-scope routing (`ci-changed-scope.mjs`), ClawSweeper activity forwarding, manual `workflow_dispatch` fan-out, and the runner matrix (Blacksmith / GitHub-hosted). |
| 6 | `oc_ci_release_validation.md` | procedure | ci.md: OpenClaw Performance, Full Release Validation, Live and E2E shards, Package Acceptance (Jobs, Candidate sources, Suite profiles, Legacy compatibility windows, Examples), Install smoke, Plugin Prerelease, QA Lab | 750 | Running a release-validation pass: the `Full Release Validation` umbrella + `OpenClaw Release Publish`, live/E2E shards, `Package Acceptance` (jobs, candidate sources, suite profiles, legacy windows, `gh workflow run` examples), install smoke, Plugin Prerelease, QA Lab, and the OpenClaw Performance benchmark workflow. |
| 7 | `oc_ci_codeql_scanning.md` | argument | ci.md: CodeQL (Security categories, Platform-specific security shards, Critical Quality categories) | 550 | OpenClaw's CodeQL strategy — a deliberately narrow first-pass security scanner over highest-risk JS/TS surfaces plus a separate `Critical Quality` non-security shard: the security category map, Android/macOS platform security shards, the critical-quality category map, and why quality is kept separate from security signal. |
| 8 | `oc_ci_local_and_docker_e2e.md` | procedure | ci.md: Local equivalents, Local Docker E2E (Tunables, Reusable live/E2E workflow, Release-path chunks), Maintenance workflows (Docs Agent, Test Performance Agent, Duplicate PRs After Merge), Local check gates and changed routing, Testbox validation | 750 | Reproducing CI locally and on remote boxes: the `pnpm` local-equivalent gate commands, the local Docker E2E aggregate (tunables, reusable live/E2E workflow, release-path chunks), the changed-lane local check gates, the Crabbox/Blacksmith Testbox proof flow, and the Codex maintenance workflows (Docs Agent, Test Performance Agent, Duplicate-PR cleanup). |
| 9 | `oc_clawhub.md` | procedure | clawhub.md: Quick start, What ClawHub hosts, Native OpenClaw flows, ClawHub CLI, Publishing, Security and moderation, Telemetry and environment | 650 | Using ClawHub, OpenClaw's public skill/plugin registry: searching/installing/updating via native `openclaw` commands vs the registry-authenticated `clawhub` CLI, what it hosts (skills, code plugins, bundle plugins), native install/compat resolution, publishing skills and plugins (options, dry-run, required compat metadata), security/moderation, and telemetry/env overrides. |
| 10 | `oc_cli.md` | model | cli.md: setup-command intents, Command pages, Global flags, Output modes, Command tree, Chat slash commands, Usage tracking | 600 | The `openclaw` CLI reference index: the setup-by-intent guidance (`setup`/`onboard`/`configure`/`channels add`), the command-pages map by area, global flags, output modes (ANSI/OSC-8/`--json`), the full command tree, chat slash-command highlights, and provider usage tracking. |

Filename rule applied: top-level slug → `oc_<slug-with-/-and---as-_>.md`; `ci` (split) → `oc_ci_<aspect>.md`.

## Section Coverage Map

```
agent-runtime-architecture.md
├── (intro) ─────────────────────────────────────── → note 1 (oc_agent_runtime_architecture)
├── Runtime Layout ──────────────────────────────── → note 1
├── Boundaries ──────────────────────────────────── → note 1
├── Manifests ───────────────────────────────────── → note 1
├── Runtime Selection ───────────────────────────── → note 1
└── Related (link-out) ──────────────────────────── → note 1 References / Related Notes

auth-credential-semantics.md
├── (intro: resolveAuthProfileOrder etc.) ───────── → note 2 (oc_auth_credential_semantics)
├── Stable probe reason codes ───────────────────── → note 2
├── Token credentials ├ Eligibility rules ├ Resolution rules → note 2
├── Agent copy portability ──────────────────────── → note 2
├── Config-only auth routes ─────────────────────── → note 2
├── Explicit auth order filtering ───────────────── → note 2
├── Probe target resolution ─────────────────────── → note 2
├── External CLI credential discovery ───────────── → note 2
├── OAuth SecretRef Policy Guard ────────────────── → note 2
├── Legacy-Compatible Messaging ─────────────────── → note 2
└── Related (link-out: gateway/secrets, concepts/oauth) → note 2 Related Notes

automation.md
├── Quick decision guide (+ table) ──────────────── → note 3 (oc_automation_overview)
│   └── Scheduled Tasks (Cron) vs Heartbeat (table) → note 3
├── Core concepts (cron/tasks/commitments/Task Flow/standing orders/hooks/heartbeat) → note 3
├── How they work together ──────────────────────── → note 3
└── Related (link-out: cron-jobs, tasks, taskflow, hooks, heartbeat …) → note 3 Related Notes

channels.md
├── (intro) ─────────────────────────────────────── → note 4 (oc_channels_overview)
├── Delivery notes ──────────────────────────────── → note 4
├── Supported channels (~30) ────────────────────── → note 4
└── Notes (simultaneous, fastest setup, groups, pairing) → note 4

ci.md
├── (intro) ─────────────────────────────────────── → note 5 (oc_ci_pipeline_overview)
├── Pipeline overview ───────────────────────────── → note 5
├── Fail-fast order ─────────────────────────────── → note 5
├── PR context and evidence ─────────────────────── → note 5
├── Scope and routing ───────────────────────────── → note 5
├── ClawSweeper activity forwarding ─────────────── → note 5
├── Manual dispatches ───────────────────────────── → note 5
├── Runners ─────────────────────────────────────── → note 5
├── OpenClaw Performance ────────────────────────── → note 6 (oc_ci_release_validation)
├── Full Release Validation ─────────────────────── → note 6
├── Live and E2E shards ─────────────────────────── → note 6
├── Package Acceptance (Jobs/Candidate sources/Suite profiles/Legacy windows/Examples) → note 6
├── Install smoke ───────────────────────────────── → note 6
├── Plugin Prerelease ───────────────────────────── → note 6
├── QA Lab ──────────────────────────────────────── → note 6
├── CodeQL (Security categories/Platform shards/Critical Quality categories) → note 7 (oc_ci_codeql_scanning)
├── Local equivalents ───────────────────────────── → note 8 (oc_ci_local_and_docker_e2e)
├── Local Docker E2E (Tunables/Reusable workflow/Release-path chunks) → note 8
├── Maintenance workflows (Docs Agent/Test Performance Agent/Duplicate PRs After Merge) → note 8
├── Local check gates and changed routing ───────── → note 8
├── Testbox validation ──────────────────────────── → note 8
└── Related (link-out: install, development-channels) → notes 5–8 References

clawhub.md
├── # ClawHub (intro) ───────────────────────────── → note 9 (oc_clawhub)
├── Quick start ─────────────────────────────────── → note 9
├── What ClawHub hosts ──────────────────────────── → note 9
├── Native OpenClaw flows ───────────────────────── → note 9
├── ClawHub CLI ─────────────────────────────────── → note 9
├── Publishing ──────────────────────────────────── → note 9
├── Security and moderation ─────────────────────── → note 9
└── Telemetry and environment ───────────────────── → note 9

cli.md
├── (intro + setup-by-intent) ───────────────────── → note 10 (oc_cli)
├── Command pages (area map) ────────────────────── → note 10
├── Global flags ────────────────────────────────── → note 10
├── Output modes ────────────────────────────────── → note 10
├── Command tree (Accordion) ────────────────────── → note 10
├── Chat slash commands ─────────────────────────── → note 10
├── Usage tracking ──────────────────────────────── → note 10
└── Related (link-out: slash-commands, configuration, environment) → note 10 Related Notes
```
No orphaned sections. `Related` blocks become Related-Notes/References link-outs to the dedicated per-area sub-plans.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| ci.md (8,419w · 18 code · 21 H2 / 14 H3, mixed BB) | notes 5 + 6 + 7 + 8 | >3× the 2,500w cap and 3× the 6-code cap; mixes a CI-graph concept/model (pipeline/scope/runners), a release-validation procedure (umbrellas/acceptance/smoke/QA/perf), a security argument (CodeQL strategy), and a local-reproduction procedure (local+Docker E2E+Testbox+maintenance). Split by task cluster + word/code-cap + one-BB-per-note rules; each child stays ≤750w / ≤6 code. |

All 6 other pages are ≤1,013w / ≤8 code and stay 1 note each (clawhub's 8 fences trim to ≤6 by reproducing only
the load-bearing `openclaw`/`clawhub` command blocks; cli's single big command-tree fence reproduced verbatim once).

## Summary Statistics & Building Block Distribution

- Source pages: **7** (12,752 words, 29 code blocks). New `oc_` notes: **10**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×4** (notes 1, 3, 4, 5) · **model ×2** (notes 2, 10) · **procedure ×3** (notes 6, 8, 9)
  · **argument ×1** (note 7). One building_block per note.
- Est. digest words ~6,270 (avg ~627/note). The 18 source fences of ci.md distribute across notes 5–8 (each
  ≤6 — most are `gh workflow run` / `pnpm` command blocks, reproduced selectively, verbatim); clawhub's 8 and
  cli's 1 trim/keep ≤6.
- Cross-refs (LOCKED at xref-augment 2026-06-21 — see `## Per-Note Related Notes Mapping`): every note maps
  **≥8 relevance-selected `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`**
  `entry_openclaw_docs` (master W1). ALL cited existing targets (terms/snippets/repos/cross-folder docs) are
  (probed MISSING) are deliberately NOT cited.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: term `../../term_dictionary/term_Y.md`;
snippet `../../code_snippets/snippet_Y.md`; cross-folder doc `../<folder>/<file>.md`; repo
`../../../areas/code_repos/repo_Y.md`; entry `../../../0_entry_points/entry_Y.md`; sibling `oc_Y.md` (this series,

### oc_agent_runtime_architecture (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway whose built-in agent runtime this documents; relevance: the runtime under `src/agents/*` IS OpenClaw's owned runtime.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the loop that drives an LLM agent's tool calls/turns; relevance: the built-in runtime is the default harness and `auto` selects plugin harnesses.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class that edits code/runs tools autonomously; relevance: the class this runtime hosts (`embedded-agent-runner` attempt loop).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — protocol for external agent harnesses; relevance: plugin runtime ids register additional harnesses selected via `auto`.
- [MCP](../../term_dictionary/term_mcp.md) — tool/context contract exposed to agents; relevance: tool/extension contracts surface through `openclaw/plugin-sdk/*` barrels.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool-invocation schemas; relevance: `agent-tools*.ts` defines tool schemas, policy, and before/after hook adapters.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the documented plugin entrypoints; relevance: plugins use `openclaw/plugin-sdk/*` and must not import `src/**` internals (the Boundaries rule).
- [Compaction](../../term_dictionary/term_compaction.md) — transcript-shrinking for context limits; relevance: the runner does compaction + `agent-hooks/` carries compaction safeguards.
- [Context Engine](../../term_dictionary/term_context_engine.md) — pluggable context-assembly layer; relevance: `packages/agent-core` compaction helpers + context pruning are the context-engine surface.

**Docs**
- [pi: Extensions Overview](../pi/pi_extensions_overview.md) — pi's runtime extension/manifest model; relevance: directly analogous resource-package manifest + extension barrel pattern.
- [pi: SDK Overview](../pi/pi_sdk_overview.md) — pi agent SDK + runtime types; relevance: sibling coding-agent SDK with the same core/plugin boundary split.
- [pi: Compaction](../pi/pi_compaction.md) — pi compaction internals; relevance: parallels the runner's compaction + context-pruning hooks.
- [band: SDK Architecture](../band/band_sdk_architecture.md) — band agent SDK module layout; relevance: another coding-agent's module-layout/boundary contract for comparison.
- [band: Agent Lifecycle](../band/band_agent_lifecycle.md) — agent attempt/turn lifecycle; relevance: maps to the `embedded-agent-runner` attempt loop and runtime selection.
- [Claude Code: Plugins Overview](../claude_code/cc_plugins_overview.md) — CC plugin model; relevance: the canonical core-vs-plugin runtime-extension precedent for this folder's format.
- [Claude Code: Plugin Components](../claude_code/cc_plugin_components.md) — what a plugin ships (commands/agents/hooks); relevance: parallels resource-package manifests (extensions/skills/prompts/themes).
- [Claude Code: SDK Plugins](../claude_code/cc_sdk_plugins.md) — programmatic plugin/harness registration; relevance: analog of registering additional runtime ids.
- [Hermes: Context-Engine Plugin](../hermes_agent/hermes_context_engine_plugin.md) — Hermes pluggable context engine; relevance: sibling context-engine/runtime-hook surface.
- `oc_cli.md` (planned, this series) — CLI surface that exposes runtime selection; relevance: `openclaw` runtime-id selection is invoked through the CLI.
- `oc_ci_pipeline_overview.md` (planned, this series) — CI runtime-topology architecture checks; relevance: `check-additional-*` validates runtime topology / package boundary documented here.

- [oc_auth_credential_semantics](oc_auth_credential_semantics.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the `src/agents/*` runtime this page documents; relevance: source of truth for the runner/sessions/tools/hooks layout.
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level repo / module layout; relevance: the `src/agents`, `src/llm`, `packages/agent-core` tree.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin-sdk barrels + manifests; relevance: the `openclaw/plugin-sdk/*` contract surface.
- [repo: openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session persistence + resource discovery; relevance: `src/agents/sessions/` skills/prompts/themes discovery.

**Snippets**
- [snippet: agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config assembly; relevance: the runtime-selection/config the page describes.
- [snippet: agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model registry; relevance: `src/llm/` provider/model registry.
- [snippet: agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool definitions; relevance: `agent-tools*.ts` tool catalog.
- [snippet: agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy + hook adapters; relevance: before/after hook adapters + policy in agent-tools.
- [snippet: agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope wiring; relevance: runtime/session scope plumbing.
- [snippet: agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity; relevance: runtime/session identity wiring.
- [snippet: agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — prompt-template modes; relevance: `packages/agent-core` prompt templates.
- [snippet: plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-sdk barrel entries; relevance: the documented `openclaw/plugin-sdk/*` entrypoints (Boundaries).
- [snippet: plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: resource-package/extension discovery.
- [snippet: skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest parsing; relevance: the `skills`/`prompts`/`themes` manifest discovery.
- [snippet: context_engine_registry_factories](../../code_snippets/snippet_openclaw_context_engine_registry_factories.md) — context-engine factory registry; relevance: `agent-hooks/` context pruning + compaction substrate.

### oc_auth_credential_semantics (9t · 11s · 11d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller/credential identity; relevance: this page IS the canonical auth-profile credential contract.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — a named credential routing entry; relevance: the entire eligibility/resolution semantics operate on `auth.profiles` entries.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: `oauth` profiles + the OAuth SecretRef policy guard.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — access/refresh tokens; relevance: refresh-token rotation sensitivity drives non-portable defaults.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — managed set of provider credentials; relevance: read-through inheritance + per-agent profile stores parallel a credential pool.
- [PKCE](../../term_dictionary/term_pkce.md) — OAuth proof-key flow; relevance: provider-owned OAuth flows that may opt into `copyToAgents`.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — AWS default credential resolution; relevance: `mode: "aws-sdk"` config-only routes are routing metadata, not stored secrets.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: probe targets resolve per provider from profiles/env/`models.json`.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: a first-class auth provider whose key/token profiles flow through this contract.

**Docs**
- [pi: Provider Auth](../pi/pi_provider_auth.md) — pi credential/provider auth model; relevance: closest sibling auth-profile/credential-routing precedent.
- [Claude Code: Authentication](../claude_code/cc_authentication.md) — CC auth setup; relevance: API-key/OAuth credential routing analog.
- [Claude Code: Login & Auth Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — CC auth failure modes; relevance: parallels the stable probe reason codes / `doctor-auth`.
- [Claude Code: Auth & Network Errors](../claude_code/cc_authentication_and_network_errors.md) — CC credential error taxonomy; relevance: analog of `missing_credential`/`expired`/`unresolved_ref` reason codes.
- [Claude Code: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock auth via AWS SDK; relevance: the `auth: "aws-sdk"` config-only route concretely.
- [Claude Code: Agent SDK Install & Auth](../claude_code/cc_agent_sdk_install_and_auth.md) — SDK credential bootstrap; relevance: programmatic credential resolution analog.
- [Claude Code: SDK Credential & Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential scoping; relevance: parallels external-CLI discovery modes + keychain-prompt gating.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — Hermes credential pooling; relevance: read-through/portability inheritance analog.
- [Hermes: Provider MiniMax OAuth](../hermes_agent/hermes_provider_minimax_oauth.md) — per-provider OAuth profile; relevance: concrete OAuth profile portability/rotation example.
- `oc_cli.md` (planned, this series) — `models status --probe` / auth subcommands; relevance: the CLI surface that exercises this contract.
- `oc_clawhub.md` (planned, this series) — registry auth (`clawhub login`); relevance: adjacent but separate auth surface to disambiguate.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/secret resolution + policy guards; relevance: the SecretRef policy guard + secret resolution live here.
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — runtime auth resolution; relevance: `resolveAuthProfileOrder`/`resolveApiKeyForProfile` live in the runtime.
- [repo: openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins + auth modes; relevance: per-provider `auth` mode (`aws-sdk`, oauth, api_key).
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — startup/reload auth resolution paths; relevance: SecretRef guard violations are hard failures in gateway startup/reload.

**Snippets**
- [snippet: agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth order + credential resolution; relevance: directly implements `resolveAuthProfileOrder`/eligibility.
- [snippet: agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth copy portability; relevance: the agent copy portability rules verbatim.
- [snippet: agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI credential discovery; relevance: the `none`/`existing`/`scoped` discovery modes.
- [snippet: gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: `mode: aws-sdk` config-only route handling.
- [snippet: gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: runtime auth resolution path.
- [snippet: gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution at call time; relevance: SecretRef/`keyRef`/`tokenRef` material resolution.
- [snippet: provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider auth; relevance: a concrete provider probe target.
- [snippet: provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider auth; relevance: another concrete probe target.
- [snippet: model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model candidate discovery; relevance: `no_model` reason code when no probeable candidate resolves.
- [snippet: security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security probe execution; relevance: probe execution + reason-code surfacing.
- [snippet: gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias/probe lookup; relevance: probe target resolution from `models.json`.

### oc_automation_overview (9t · 10s · 11d)

**Terms**
- [Cron](../../term_dictionary/term_cron.md) — time-based scheduler; relevance: Scheduled Tasks (Cron) is the precise-timing mechanism.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — recurring-schedule syntax; relevance: cron recurring expressions / one-shot `--at`.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic main-session turn; relevance: the cron-vs-heartbeat comparison core mechanism.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — durable multi-step agent orchestration; relevance: Task Flow is durable multi-step flow orchestration.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating multi-step work; relevance: Task Flow + "how they work together" composition.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP trigger; relevance: cron inbound webhook triggers + channel/webhook delivery.
- [Persistent Goal](../../term_dictionary/term_persistent_goal.md) — long-lived agent objective; relevance: standing orders + inferred commitments are persistent follow-up state.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: these are OpenClaw's background-work mechanisms.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent doing the work; relevance: heartbeat/cron/Task-Flow all drive the autonomous agent in the background.

**Docs**
- [Claude Code: Scheduled Task Execution Model](../claude_code/cc_scheduled_task_execution_model.md) — CC scheduled-task model; relevance: direct analog of cron isolated/fresh-context execution.
- [Claude Code: Scheduling Options Comparison](../claude_code/cc_scheduling_options_comparison.md) — CC mechanism chooser; relevance: parallels the cron-vs-heartbeat decision table.
- [Claude Code: Loop / Scheduled Tasks](../claude_code/cc_loop_scheduled_tasks.md) — CC recurring loop; relevance: recurring/one-shot scheduled work analog.
- [Claude Code: Hook Events Catalog](../claude_code/cc_hook_events_catalog.md) — CC lifecycle hook events; relevance: maps to OpenClaw hooks on `/new`,`/reset`,`/stop`, compaction, startup.
- [Hermes: Cron Internals](../hermes_agent/hermes_cron_internals.md) — Hermes scheduler internals; relevance: sibling Gateway-built-in scheduler behavior.
- [Hermes: Cron Scheduling](../hermes_agent/hermes_cron_scheduling.md) — Hermes cron config; relevance: recurring/one-shot job config analog.
- [Hermes: Event Hooks](../hermes_agent/hermes_event_hooks.md) — Hermes event-driven hooks; relevance: analog of internal hooks discovered from directories.
- [Hermes: Persistent Goals](../hermes_agent/hermes_persistent_goals.md) — Hermes long-lived goals; relevance: standing-orders / inferred-commitments analog.
- [Hermes: Subagent Delegation](../hermes_agent/hermes_subagent_delegation.md) — Hermes detached work tracking; relevance: the background-tasks ledger (ACP/subagent runs) analog.
- `oc_cli.md` (planned, this series) — `openclaw cron/tasks/hooks` commands; relevance: the CLI that drives every automation mechanism.
- `oc_ci_release_validation.md` (planned, this series) — scheduled CI workflows; relevance: scheduled release/perf workflows are an analogous automation surface.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — heartbeat/commitments/hooks runtime; relevance: where the background-work mechanisms run.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway built-in scheduler; relevance: cron persists jobs + wakes the agent via the Gateway.
- [repo: openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session lifecycle; relevance: hooks fire on session-lifecycle/compaction events.

**Snippets**
- [snippet: gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + notifications; relevance: the built-in cron scheduler + channel/webhook delivery.
- [snippet: gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — scheduled cron repair job; relevance: a concrete recurring cron job.
- [snippet: gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat turn handling; relevance: heartbeat periodic main-session turn implementation.
- [snippet: gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hook config payload; relevance: hook discovery/configuration.
- [snippet: gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hook request handling; relevance: event-driven hook dispatch.
- [snippet: gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session-reset hooks; relevance: hooks firing on `/reset`/session lifecycle.
- [snippet: agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: detached background work tracked in the tasks ledger.
- [snippet: agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent registry lifecycle; relevance: background-tasks audit of detached work.
- [snippet: sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: the lifecycle events hooks react to.
- [snippet: memory_dreaming_constants](../../code_snippets/snippet_openclaw_memory_dreaming_constants.md) — scheduled "dreaming" maintenance; relevance: a heartbeat/cron-driven background maintenance example.

### oc_channels_overview (8t · 12s · 11d)

**Terms**
- [Slack](../../term_dictionary/term_slack.md) — Slack messaging platform; relevance: Bolt-SDK channel + MPIM group routing called out in Delivery notes.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack/WS inbound transport; relevance: WebSocket-based channels (Feishu/Mattermost/Slack socket mode).
- [Block Kit](../../term_dictionary/term_block_kit.md) — Slack rich-message format; relevance: media/reactions vary by channel — Slack rich content surface.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: Feishu/Mattermost/WebChat connect over WebSocket.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP trigger; relevance: Google Chat/Synology/SMS channels via webhooks.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — OpenClaw channel dispatch core; relevance: each channel connects via the Gateway channel kernel/routing.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — direct-message pairing/allowlist; relevance: DM pairing and allowlists enforced for safety.
- [Bot](../../term_dictionary/term_bot.md) — automated chat account; relevance: bot-authored inbound + bot-loop protection.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the ~30-channel matrix is OpenClaw's connectivity surface.

**Docs**
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — Hermes channel-via-gateway model; relevance: direct analog of "each channel connects via the Gateway".
- [Hermes: Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack channel; relevance: Slack Bolt/MPIM group routing analog.
- [Hermes: Messaging Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — Slack channel config; relevance: per-channel group/mention behavior.
- [Hermes: Telegram Setup](../hermes_agent/hermes_telegram_setup.md) — Telegram bot channel; relevance: "fastest setup is Telegram (simple bot token)".
- [Hermes: Messaging Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel; relevance: downloadable Matrix plugin channel analog.
- [Hermes: Discord Advanced](../hermes_agent/hermes_discord_advanced.md) — Discord channel features; relevance: Discord Bot API + Gateway servers/channels/DMs.
- [Hermes: Messaging WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp Baileys channel; relevance: WhatsApp QR pairing + Baileys called out verbatim.
- [Hermes: Photon iMessage](../hermes_agent/hermes_photon_imessage.md) — iMessage bridge channel; relevance: native macOS iMessage integration analog.
- [Claude Code: Channels Setup](../claude_code/cc_channels_setup.md) — CC chat-channel setup; relevance: multi-platform channel onboarding precedent.
- `oc_cli.md` (planned, this series) — `openclaw channels add/list/status`; relevance: the CLI that configures channels.
- `oc_automation_overview.md` (planned, this series) — channel delivery for cron output; relevance: cron output delivers to a chat channel.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel framework; relevance: the adapter/binding/routing core for all channels.
- [repo: openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text/media channel impls; relevance: Telegram media conversion, Slack MPIM, etc.
- [repo: openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — Voice Call channel; relevance: the Voice Call (Plivo/Twilio) channel entry.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway connection layer; relevance: every channel connects via the Gateway.

**Snippets**
- [snippet: channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the shared interface every channel implements.
- [snippet: channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — per-chat routing; relevance: "configure multiple and OpenClaw routes per chat".
- [snippet: channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: group vs DM routing resolution.
- [snippet: channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: the Discord Bot API channel.
- [snippet: channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: DM pairing + allowlists enforced for safety.
- [snippet: channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: inbound message dispatch core.
- [snippet: channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry; relevance: the supported-channel matrix registry.
- [snippet: channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket mode; relevance: Slack Bolt SDK + socket transport.
- [snippet: channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reactions; relevance: "media and reactions vary by channel".
- [snippet: channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport (grammY); relevance: Telegram Bot API via grammY + media reply conversion.
- [snippet: channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: group-session rules / MPIM thread routing.
- [snippet: channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — channel match resolver; relevance: ambient-room-event vs mention routing.

### oc_ci_pipeline_overview (8t · 10s · 11d)

**Terms**
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: this page IS the CI job graph.
- [DevOps](../../term_dictionary/term_devops.md) — build/test/release ops practice; relevance: preflight scoping, runners, fail-fast ordering are DevOps concerns.
- [Code Review](../../term_dictionary/term_code_review.md) — PR review gate; relevance: the external-contributor PR context-and-evidence gate.
- [Docker](../../term_dictionary/term_docker.md) — container build/test; relevance: build-artifacts + install-smoke Docker lanes.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/build-trust security; relevance: `security-fast` lockfile audit + `zizmor` changed-workflow audit.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — malicious package substitution risk; relevance: `check-dependencies` Knip + unused-file/dependency guard.
- [DAG](../../term_dictionary/term_dag.md) — directed acyclic job graph; relevance: the CI job graph with fail-fast ordering is a DAG.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the repo; relevance: the repository this CI validates.

**Docs**
- [Claude Code: GitHub Actions](../claude_code/cc_github_actions.md) — CC GitHub Actions integration; relevance: same Actions substrate / job-graph precedent.
- [Claude Code: GitHub Actions Cloud Providers](../claude_code/cc_github_actions_cloud_providers.md) — Actions provider/runner config; relevance: runner-matrix + cloud-runner analog (Blacksmith/GitHub-hosted).
- [Claude Code: GitLab CI/CD](../claude_code/cc_gitlab_ci_cd.md) — GitLab pipeline integration; relevance: cross-platform CI pipeline scoping analog.
- [Claude Code: Code Review](../claude_code/cc_code_review.md) — automated PR review; relevance: the PR context-and-evidence gate analog.
- [Claude Code: Code Review Setup & Customization](../claude_code/cc_code_review_setup_and_customization.md) — review gating config; relevance: PR-gate configuration analog.
- [Claude Code: GitHub Enterprise Server](../claude_code/cc_github_enterprise_server.md) — self-hosted Actions; relevance: runner/dispatch routing on self-hosted infra.
- [Hermes: GitHub PR Review Webhook](../hermes_agent/hermes_guide_github_pr_review_webhook.md) — PR-review webhook bot; relevance: ClawSweeper activity-forwarding analog.
- [pi: Development](../pi/pi_development.md) — pi CI/dev workflow; relevance: sibling coding-agent CI/dev-loop precedent.
- `oc_ci_release_validation.md` (planned, this series) — release-validation umbrellas; relevance: the release child of the same ci.md graph.
- `oc_ci_codeql_scanning.md` (planned, this series) — CodeQL security lane; relevance: one lane of this job graph.
- `oc_ci_local_and_docker_e2e.md` (planned, this series) — local equivalents; relevance: local mirror of these CI gates.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.
- [oc_auth_credential_semantics](oc_auth_credential_semantics.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — the repository this CI validates; relevance: the source tree preflight/scoping classifies.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin shards; relevance: changed-extension scope + plugin contract shards.

**Snippets**
- [snippet: cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `pnpm`/`gh` lane commands map to CLI surfaces validated in CI.
- [snippet: gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: CI-env/runner env classification.
- [snippet: gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config-reload planning; relevance: `config-reload` smoke lane behavior.
- [snippet: gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config/plugins startup; relevance: plugin/config boundary checks in `check-additional-*`.
- [snippet: gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: bundled-plugin/contract shards.
- [snippet: gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC protocol envelope; relevance: protocol checks in `checks-fast-core`.
- [snippet: gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — protocol error/version; relevance: versioned-concurrency / protocol regression coverage.
- [snippet: model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: provider/model contract shards.
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security audit composition; relevance: `security-fast` private-key/audit lane.
- [snippet: opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — workflow/rule validation; relevance: `zizmor`/workflow-sanity changed-workflow audit analog.

### oc_ci_release_validation (8t · 10s · 11d)

**Terms**
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous delivery; relevance: Full Release Validation umbrella + Release Publish are the release CI.
- [DevOps](../../term_dictionary/term_devops.md) — release coordination ops; relevance: stage matrix, rerun groups, child-run verification.
- [Docker](../../term_dictionary/term_docker.md) — container release validation; relevance: Package Acceptance runs the Docker E2E harness against a tarball.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: npm candidate sources (`openclaw@beta`), `OpenClaw NPM Release`.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — package-trust security; relevance: SHA-256-pinned tarball sources, trusted-mirror policy, installer-digest verification.
- [Code Review](../../term_dictionary/term_code_review.md) — release-gate review; relevance: candidate approval / installer-digest contract before publish.
- [Threat Model](../../term_dictionary/term_threat_model.md) — release-surface risk; relevance: trusted-url policy rejects credentials/private hosts/redirects.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product being released; relevance: the package under validation.

**Docs**
- [Claude Code: Advanced Install & Verification](../claude_code/cc_advanced_install_and_verification.md) — install verification; relevance: package install-smoke / acceptance analog.
- [Claude Code: GitHub Actions](../claude_code/cc_github_actions.md) — Actions release workflows; relevance: `gh workflow run` release dispatch analog.
- [Claude Code: GitHub Actions Cloud Providers](../claude_code/cc_github_actions_cloud_providers.md) — release runner/provider config; relevance: live provider/E2E shard credentials.
- [Claude Code: Plugin Dependencies](../claude_code/cc_plugin_dependencies.md) — plugin dependency/compat; relevance: Plugin Prerelease compatibility coverage.
- [band: Coding Agents Deployment](../band/band_coding_agents_deployment.md) — agent deploy/release E2E; relevance: published-upgrade-survivor / cross-OS release-box deployment analog.
- [pi: Development](../pi/pi_development.md) — pi release/dev workflow; relevance: sibling coding-agent release-validation precedent.
- [pi: Packages](../pi/pi_packages.md) — pi package model; relevance: package candidate-source/versioning analog.
- [Hermes: Updating / Uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — Hermes update/migration; relevance: update-survivor / migration acceptance analog.
- `oc_ci_pipeline_overview.md` (planned, this series) — the CI graph; relevance: release dispatch forces the full CI graph on.
- `oc_ci_local_and_docker_e2e.md` (planned, this series) — local Docker E2E; relevance: the same Docker E2E harness run locally.
- `oc_clawhub.md` (planned, this series) — Plugin ClawHub Release; relevance: release publish dispatches `Plugin ClawHub Release`.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.
- [oc_auth_credential_semantics](oc_auth_credential_semantics.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — release source; relevance: the source/tarball under release validation.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — Plugin Prerelease coverage; relevance: bundled-plugin release-only shards.
- [repo: openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — live provider shards; relevance: `native-live-extensions-openai`/provider-filtered E2E shards.

**Snippets**
- [snippet: gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config/plugins startup; relevance: package-acceptance gateway boot + config-reload lane.
- [snippet: gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth startup; relevance: `update-restart-auth` acceptance lane.
- [snippet: gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: `plugins-offline`/`plugin-update`/`update-corrupt-plugin` lanes.
- [snippet: gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config-reload apply; relevance: the `config-reload` smoke-profile lane.
- [snippet: gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache respawn; relevance: upgrade-survivor restart behavior.
- [snippet: provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: Anthropic package-update Docker chunk lane.
- [snippet: provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: `package-update-openai` live Codex/OpenAI agent-turn lane.
- [snippet: provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: broad provider/media matrix in `full` profile.
- [snippet: agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: live-provider shard resilience under release validation.
- [snippet: cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `openclaw config set` recipe steps probed in published-upgrade lanes.

### oc_ci_codeql_scanning (8t · 10s · 11d)

**Terms**
- [CI/CD](../../term_dictionary/term_ci_cd.md) — pipeline integration; relevance: CodeQL + Critical Quality run as CI workflows.
- [Threat Model](../../term_dictionary/term_threat_model.md) — risk-prioritized security scope; relevance: "narrow first-pass scanner over the highest-risk surfaces" with high/critical severity.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/plugin-trust security; relevance: `plugin-trust-boundary` install/loader/registry/package-manager surfaces.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side request-forgery defense; relevance: `network-ssrf-boundary` SSRF/IP-parsing/web-fetch CodeQL category.
- [DevOps](../../term_dictionary/term_devops.md) — pipeline security ops; relevance: scheduling/disabling/expanding quality vs security shards.
- [Code Review](../../term_dictionary/term_code_review.md) — PR security guard; relevance: the non-draft PR CodeQL guard gating high-risk changes.
- [Deny First](../../term_dictionary/term_deny_first.md) — default-deny security posture; relevance: the auth/secrets/sandbox `core-auth-secrets` boundary CodeQL targets.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the scanned repo; relevance: the JS/TS surface CodeQL scans.

**Docs**
- [Claude Code: Sandbox Filesystem/Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — sandbox/isolation security; relevance: the sandbox/exec boundary CodeQL `core-auth-secrets` targets.
- [Claude Code: Security Guidance Plugin](../claude_code/cc_security_guidance_plugin.md) — security scanning guidance; relevance: analog of a security-focused scan lane.
- [Claude Code: GitHub Actions Cloud Providers](../claude_code/cc_github_actions_cloud_providers.md) — Actions security/runner config; relevance: CodeQL runs as a scheduled/PR Actions job on Blacksmith runners.
- [Claude Code: Code Review](../claude_code/cc_code_review.md) — automated review/security; relevance: PR-guard security gating analog.
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — exec/command security; relevance: `mcp-process-tool-boundary` process-exec/tool-gate surface.
- [pi: Development](../pi/pi_development.md) — pi dev/security workflow; relevance: sibling coding-agent's security-scanning posture.
- [Claude Code: GitHub Actions](../claude_code/cc_github_actions.md) — Actions workflow code; relevance: CodeQL scans Actions workflow code too.
- [Hermes: GitHub PR Review Webhook](../hermes_agent/hermes_guide_github_pr_review_webhook.md) — PR security automation; relevance: PR-time security signal analog.
- `oc_ci_pipeline_overview.md` (planned, this series) — the CI graph; relevance: CodeQL is one lane of the documented graph.
- `oc_ci_release_validation.md` (planned, this series) — release validation; relevance: platform CodeQL shards run on release/scheduled cadence.
- `oc_auth_credential_semantics.md` (planned, this series) — auth/secrets contract; relevance: `core-auth-secrets` is the auth/secret boundary CodeQL targets.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.
- [oc_auth_credential_semantics](oc_auth_credential_semantics.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/secrets/sandbox/audit boundary; relevance: the security surface CodeQL category-maps over.
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — the JS/TS source; relevance: the highest-risk JS/TS surface scanned.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway protocol/server-method; relevance: `gateway-runtime-boundary` quality category surface.

**Snippets**
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composed security audit; relevance: the multi-category security-scan composition analog.
- [snippet: security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: `mcp-process-tool-boundary` process-exec gate.
- [snippet: security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denial; relevance: agent tool-execution gate CodeQL targets.
- [snippet: security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted-content handling; relevance: SSRF/web-fetch network boundary.
- [snippet: security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: sandbox/exec `core-auth-secrets` boundary.
- [snippet: security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin-trust resolution; relevance: `plugin-trust-boundary` install/loader/registry surface.
- [snippet: security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin-trust findings; relevance: plugin-trust scan findings analog.
- [snippet: opengrep_compile_collect](../../code_snippets/snippet_openclaw_opengrep_compile_collect.md) — rule compile/collect; relevance: a code-scanning rule pipeline (CodeQL analog).
- [snippet: opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — rule validation; relevance: scan-rule validation analog.
- [snippet: gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — call-method gating; relevance: `gateway-runtime-boundary` server-method contract surface.

### oc_ci_local_and_docker_e2e (8t · 11s · 11d)

**Terms**
- [Docker](../../term_dictionary/term_docker.md) — container build/run; relevance: `pnpm test:docker:all` aggregate + bare/functional E2E images.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — pipeline gates; relevance: `pnpm check`/`check:changed` are local equivalents of CI gates.
- [DevOps](../../term_dictionary/term_devops.md) — maintainer proof/ops; relevance: Crabbox/Blacksmith Testbox remote-box maintainer proof.
- [npm](../../term_dictionary/term_npm.md) — Node package tooling; relevance: `pnpm` tarball pack + npm install lanes.
- [Code Review](../../term_dictionary/term_code_review.md) — changed-routing/PR cleanup; relevance: changed-lane local checks + Duplicate-PR maintenance workflow.
- [DAG](../../term_dictionary/term_dag.md) — lane dependency graph; relevance: the Docker E2E weighted scheduler/lane plan.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — dependency-resolution risk; relevance: installer/update/plugin-dependency lanes + Knip changed routing.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the repo; relevance: the repository whose tests these run.

**Docs**
- [Claude Code: Devcontainer Setup](../claude_code/cc_devcontainer_setup.md) — containerized dev/test env; relevance: direct analog of local Docker E2E images.
- [Hermes: Docker Run Modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes Docker run modes; relevance: bare vs functional image selection analog.
- [Hermes: Docker Volumes & Supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — Docker volumes/supervision; relevance: container lane supervision/cleanup analog.
- [Hermes: Docker Tools & Local Inference](../hermes_agent/hermes_docker_tools_local_inference.md) — local Docker tooling; relevance: local-equivalent Docker test tooling.
- [band: Testing Agents](../band/band_testing_agents.md) — agent test harness; relevance: sibling agent local-test methodology.
- [band: Coding Agents Deployment](../band/band_coding_agents_deployment.md) — agent deploy/E2E; relevance: container deploy/E2E parity analog.
- [Claude Code: Advanced Install & Verification](../claude_code/cc_advanced_install_and_verification.md) — install verification; relevance: install-smoke local reproduction.
- [pi: Development](../pi/pi_development.md) — pi local dev loop; relevance: sibling local check-gate workflow.
- `oc_ci_pipeline_overview.md` (planned, this series) — CI graph; relevance: these are the local mirror of the CI gates.
- `oc_ci_release_validation.md` (planned, this series) — release Docker chunks; relevance: release-path Docker E2E chunks documented there run via this harness.
- `oc_ci_codeql_scanning.md` (planned, this series) — CodeQL lane; relevance: another lane reproduced/scoped via changed routing.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.
- [oc_auth_credential_semantics](oc_auth_credential_semantics.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — the repo whose tests run; relevance: `scripts/e2e/*`, `scripts/test-docker-all.mjs` live here.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/runtime Docker chunks; relevance: `plugins-runtime-*` Docker lanes.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway E2E; relevance: `gateway-network` Docker E2E lane.

**Snippets**
- [snippet: daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: install/update local lane behavior (macOS service install).
- [snippet: daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: Linux install/update Docker lane behavior.
- [snippet: daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — Windows schtasks render; relevance: Windows packaged/installer lane behavior.
- [snippet: process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: lane process spawn/scheduling.
- [snippet: process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: per-lane timeout/cleanup supervision.
- [snippet: process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — kill-tree on timeout; relevance: stuck-container/timeout cleanup.
- [snippet: gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache respawn; relevance: image build / respawn in E2E.
- [snippet: gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config-reload plan; relevance: `config-reload` Docker lane.
- [snippet: gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config-reload apply; relevance: `update-channel-switch` lane.
- [snippet: gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: `OPENCLAW_*` tunables/env for Docker lanes.
- [snippet: cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `pnpm`/CLI smoke commands run in lanes.

### oc_clawhub (9t · 10s · 11d)

**Terms**
- [npm](../../term_dictionary/term_npm.md) — Node registry/CLI; relevance: `npm i -g clawhub`, npm-resolved plugin specs, npm-pack `.tgz` artifacts.
- [NPM Scoping](../../term_dictionary/term_npm_scoping.md) — scoped package names; relevance: `@openclaw/demo` scoped skills + `clawhub:`/`npm:` spec resolution.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: native `openclaw skills/plugins` install flows.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — package-trust security; relevance: pluginApi/minGatewayVersion compat gate + digest-verified ClawPack `.tgz`.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — registry substitution risk; relevance: `clawhub:` vs `npm:` explicit source resolution during cutovers.
- [Authentication](../../term_dictionary/term_authentication.md) — registry auth; relevance: `clawhub login`/`whoami` registry-authenticated workflows.
- [Skills Hub](../../term_dictionary/term_skills_hub.md) — agent-skill registry; relevance: ClawHub IS the skill/plugin registry (skills hub analog).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin metadata contract; relevance: required `openclaw.compat.pluginApi`/`openclaw.build.openclawVersion` metadata.
- [Threat Model](../../term_dictionary/term_threat_model.md) — abuse/moderation risk; relevance: upload gate, scan-held releases, reporting/moderation/account bans.

**Docs**
- [Claude Code: Plugin Marketplaces & Install](../claude_code/cc_plugin_marketplaces_and_install.md) — CC marketplace install; relevance: the canonical registry discovery/install precedent.
- [Claude Code: Marketplace JSON Schema](../claude_code/cc_marketplace_json_schema.md) — marketplace metadata schema; relevance: analog of ClawHub compat/metadata requirements.
- [Claude Code: Host & Manage Marketplaces](../claude_code/cc_host_and_manage_marketplaces.md) — publishing/hosting a registry; relevance: ClawHub publishing/moderation analog.
- [Claude Code: Plugin Marketplace Walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — end-to-end publish/install; relevance: native install + publish-flow analog.
- [Claude Code: Plugin CLI Commands](../claude_code/cc_plugin_cli_commands.md) — plugin install/update CLI; relevance: `openclaw plugins`/`clawhub` CLI analog.
- [Claude Code: Plugin Sources](../claude_code/cc_plugin_sources.md) — source resolution; relevance: `clawhub:`/`npm:`/bare-spec resolution analog.
- [Hermes: Skills Hub (Agent-Managed)](../hermes_agent/hermes_skills_hub_agent_managed.md) — Hermes skill registry; relevance: sibling skill-registry install/publish surface.
- [Hermes: Creating Skill Publish](../hermes_agent/hermes_creating_skill_publish.md) — Hermes skill publishing; relevance: `clawhub skill publish` analog.
- [pi: Packages](../pi/pi_packages.md) — pi package model; relevance: package versioning/install precedent.
- `oc_cli.md` (planned, this series) — `openclaw skills/plugins` commands; relevance: native install/update CLI surface.
- `oc_ci_release_validation.md` (planned, this series) — Plugin ClawHub Release; relevance: release publish dispatches the ClawHub release.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: skills are a primary ClawHub surface.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — code/bundle plugins; relevance: plugins published/installed via ClawHub.
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — native install commands; relevance: `openclaw skills/plugins install` live in core.

**Snippets**
- [snippet: skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill planning/resolution; relevance: skill install/availability resolution.
- [snippet: skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability; relevance: installed-skill resolution after `skills install`.
- [snippet: skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — `SKILL.md` manifest; relevance: skill bundle format ClawHub hosts.
- [snippet: skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: skill/plugin capability metadata.
- [snippet: plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: required `package.json` compat metadata for code plugins.
- [snippet: plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install lifecycle; relevance: archive-install + compat validation flow.
- [snippet: plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-sdk entries; relevance: plugin entrypoints published to ClawHub.
- [snippet: security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin-trust resolution; relevance: scan/trust gate before install.
- [snippet: security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanning; relevance: automated scan checks on published skills.
- [snippet: model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest planning; relevance: compat/manifest resolution at install.

### oc_cli (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw` is the main CLI entry point.
- [DevOps](../../term_dictionary/term_devops.md) — ops surface; relevance: gateway/health/logs/system/sessions ops subcommands.
- [Cron](../../term_dictionary/term_cron.md) — scheduler; relevance: the `openclaw cron` command tree.
- [MCP](../../term_dictionary/term_mcp.md) — tool/context protocol; relevance: `openclaw mcp serve|list|show|set` subcommands.
- [Authentication](../../term_dictionary/term_authentication.md) — auth surface; relevance: `secrets`/`security`/`infer auth` subcommands.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — model providers; relevance: usage-tracking providers (Anthropic/Copilot/Gemini/Codex/MiniMax/Xiaomi/z.ai).
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `infer`/tool/`browser` subcommands invoke agent tools.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool capability metadata; relevance: `skills`/`plugins`/`mcp` surface tool descriptors via CLI.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin entrypoints; relevance: plugins can add top-level commands (`workboard`, `voicecall`).

**Docs**
- [Claude Code: CLI Commands](../claude_code/cc_cli_commands.md) — CC command reference; relevance: the closest CLI-index precedent (command tree + areas).
- [Claude Code: CLI Flags](../claude_code/cc_cli_flags.md) — CC global flags; relevance: analog of `--dev`/`--profile`/`--json`/`--no-color` global flags.
- [Claude Code: Headless Examples](../claude_code/cc_headless_examples.md) — non-interactive CLI; relevance: `--json`/`--plain` scriptable output modes.
- [Claude Code: SDK Slash Commands](../claude_code/cc_sdk_slash_commands.md) — slash-command surface; relevance: `/status`,`/config`,`/debug` chat slash commands.
- [Claude Code: Cost Tracking](../claude_code/cc_cost_tracking.md) — usage/cost surfacing; relevance: `openclaw status --usage` provider quota tracking.
- [pi: CLI Reference](../pi/pi_cli_reference.md) — pi CLI index; relevance: sibling coding-agent CLI command-tree precedent.
- [pi: Interactive Usage](../pi/pi_interactive_usage.md) — interactive CLI/TUI; relevance: `tui`/`chat`/`terminal` interactive surfaces.
- [Hermes: CLI Commands (Chat/Provider)](../hermes_agent/hermes_cli_commands_chat_provider.md) — Hermes CLI commands; relevance: sibling-agent CLI command reference analog.
- `oc_clawhub.md` (planned, this series) — `openclaw skills/plugins`; relevance: registry subcommands documented here.
- `oc_automation_overview.md` (planned, this series) — `openclaw cron/tasks/hooks`; relevance: automation subcommands.
- `oc_auth_credential_semantics.md` (planned, this series) — `models status --probe`; relevance: auth/probe subcommands.

- [oc_agent_runtime_architecture](oc_agent_runtime_architecture.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.
- [oc_auth_credential_semantics](oc_auth_credential_semantics.md) — sibling top-level page (planned, this series); relevance: same top-level cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo: openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the CLI/onboard wizard impl; relevance: `setup`/`onboard`/`configure` guided flows.
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level CLI entry; relevance: `openclaw` root command + global flags.
- [repo: hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — sibling-agent CLI; relevance: FZ 15 cross-agent CLI comparison.

**Snippets**
- [snippet: cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the command-tree/area map this page indexes.
- [snippet: cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: subcommand dispatch to area handlers.
- [snippet: cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — root command guard; relevance: global-flag parsing/guards at the root.
- [snippet: cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: `openclaw` entry-point bootstrap.
- [snippet: cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — primary run path; relevance: main command execution path.
- [snippet: wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config wizard; relevance: `openclaw setup`/`configure` intent.
- [snippet: wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup imports; relevance: onboarding/setup module wiring.
- [snippet: wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive prompter; relevance: guided `onboard`/`channels add` prompts.
- [snippet: wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: `migrate`/`backup` setup commands.
- [snippet: gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage cost summary; relevance: `openclaw status --usage` usage tracking.
- [snippet: gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency status; relevance: provider usage/quota normalized to `X% left`.

> Note: `term_codeql`, `term_static_analysis`, `term_sast`, `term_semver`, `term_telemetry`, `term_cli`,
> `term_messaging_platform`, `term_voice_agent`, `term_qr_code` were probed and are **MISSING** — they are NOT

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes (their home is this/other sub-plans), NOT new
`term_dictionary` entries. The only `term_dictionary` interaction is **linking existing** terms. **Expected new
term_dictionary captures: 0.** Augment re-runs the Step 2d new-term scan.

| Term (appears on these pages) | Disposition |
|---|---|
| agent runtime / runtime layout / runtime selection (`openclaw`/`auto`) | → note 1 (`oc_agent_runtime_architecture`); link `term_agent_harness`, `term_autonomous_coding_agents`. Not a new term. |
| auth profile / credential eligibility / resolution / probe reason codes | → note 2 (`oc_auth_credential_semantics`); link `term_authentication`, `term_oauth`, `term_oauth_token`. Not a new term. |
| SecretRef / keyRef / tokenRef | → note 2 (config concept); link `term_oauth_token` / `term_authentication`. Not promoted (OpenClaw-specific config token). |
| cron / heartbeat / Task Flow / standing orders / inferred commitments / hooks | → note 3; link `term_cron`, `term_heartbeat`, `term_agentic_workflow`, `term_webhook`. Not new terms. |
| channel / messaging platform (Telegram/Slack/Discord/WhatsApp/iMessage/Matrix/…) | → note 4; link `term_slack`, `term_chatbot`, `term_bot`, `term_websocket`, `term_webhook`. Individual platforms documented as config in ch01–ch06, not promoted. |
| CI lanes / preflight / changed-scope / runners / ClawSweeper | → note 5; link `term_ci_cd`, `term_devops`, `term_docker`. Not new terms. |
| Full Release Validation / Package Acceptance / install smoke / QA Lab | → note 6; link `term_ci_cd`, `term_docker`, `term_npm`. Not new terms. |
| CodeQL / Critical Quality / security severity | → note 7; link `term_ci_cd`, `term_threat_model`, `term_supply_chain`. **`term_codeql` / `term_static_analysis` candidates** below. |
| Crabbox / Blacksmith / Testbox | → note 8 (OpenClaw-specific tooling); link `term_docker`, `term_devops`. Not promoted (vendor/tool names → tool docs if ever, not term_dictionary). |
| ClawHub / skill bundle / code plugin / bundle plugin / semver tags | → note 9; link `term_npm`, `term_supply_chain`, `term_openclaw`. Not new terms. |
| CLI / command tree / global flags / output modes / usage tracking | → note 10; link `term_openclaw`, `term_mcp`, `term_devops`. Not new terms. |

**New-term candidates (probed MISSING, cross-cutting, reusable beyond OpenClaw):**
- `term_codeql` — GitHub's CodeQL static security analysis engine. Cross-cutting (any repo's CI). **Disposition:
  do NOT create in this sub-plan** (note 7 links `term_threat_model`/`term_ci_cd` instead); flag to master for a
  corpus-wide decision. If ever captured: `/tessellum-capture-term-note` → glossary `acronym_glossary_d_to_f.md` (or
  the dev-tooling glossary). Collision-checked: no `term_codeql` / `term_static_analysis` / `term_sast` exists.
- `term_static_analysis` — same disposition (link, do-not-create here). Collision-checked: MISSING.

No genuinely vault-reusable term with no doc-page home AND no existing note is created by rt01. **Net new
term_dictionary notes: 0.**

## Term-Note Authoring Requirements

**N/A (0 new terms).** rt01 authors zero `term_dictionary` notes (inherited from master: OpenClaw vocab → `oc_*`
doc notes; existing terms linked, never inlined). If augment's Step 2d promotes `term_codeql`/`term_static_analysis`
at the corpus level, the master's multi-source-research + glossary-update requirement applies — not rt01's job.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single phase (10 notes, P1). All 8 gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order, H1/`## Overview`/`## Related Notes`/`## References`/footer; ≤400L/≤2500w/≤6 code; 1 BB) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traceable to `inbox/openclaw_docs/<page>.md`; no invented facts) | diff vs mirror source page |
| G3 | Density + Coverage (within caps; every mapped H2/H3 present; no over-compression of ci.md splits) | word/code count + Section Coverage Map |
| G4 | Cross-Reference (≥8 relevance-selected terms + ≥10 snippets + ≥10 docs + repo/sibling/entry, each indexed link with relevance per `## Per-Note Related Notes Mapping`) | manual + `note_links` query |
| G5 | Ghost-reference detect + redirect (0 links to non-existent notes) | `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix (0 wrong relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability (every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`) | `entry_openclaw_docs.md` + inlinks below |
| G8 | In-degree ≥1 (anti-island) | `note_links` in-degree query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
# gate sweep
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_agent_runtime_architecture oc_auth_credential_semantics oc_automation_overview oc_channels_overview oc_ci_pipeline_overview oc_ci_release_validation oc_ci_codeql_scanning oc_ci_local_and_docker_e2e oc_clawhub oc_cli"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density caps (strip frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w ${cb}cb)"
  # sibling-prefix link sanity (informational)
  grep -oE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" >/dev/null 2>&1 && echo "$n has sibling oc_ links"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

```bash
# DB existence verification for cited EXISTING targets (must all print 1; run before locking xrefs at augment)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for id in \
  resources/term_dictionary/term_openclaw.md resources/term_dictionary/term_authentication.md \
  resources/term_dictionary/term_oauth.md resources/term_dictionary/term_oauth_token.md \
  resources/term_dictionary/term_aws_sdk_credential_chain.md resources/term_dictionary/term_cron.md \
  resources/term_dictionary/term_heartbeat.md resources/term_dictionary/term_agentic_workflow.md \
  resources/term_dictionary/term_webhook.md resources/term_dictionary/term_slack.md \
  resources/term_dictionary/term_chatbot.md resources/term_dictionary/term_bot.md \
  resources/term_dictionary/term_websocket.md resources/term_dictionary/term_ci_cd.md \
  resources/term_dictionary/term_devops.md resources/term_dictionary/term_docker.md \
  resources/term_dictionary/term_npm.md resources/term_dictionary/term_supply_chain.md \
  resources/term_dictionary/term_threat_model.md resources/term_dictionary/term_code_review.md \
  resources/term_dictionary/term_mcp.md resources/term_dictionary/term_function_calling.md \
  resources/term_dictionary/term_third_party_genai_services.md resources/term_dictionary/term_agent_harness.md \
  resources/term_dictionary/term_autonomous_coding_agents.md resources/term_dictionary/term_acp_agent_client_protocol.md \
  resources/term_dictionary/term_sandbox.md resources/term_dictionary/term_llm.md \
  resources/term_dictionary/term_claude.md \
  areas/code_repos/repo_openclaw.md areas/code_repos/repo_openclaw_agents.md \
  areas/code_repos/repo_openclaw_security.md areas/code_repos/repo_openclaw_channels.md \
  areas/code_repos/repo_openclaw_channels_messaging.md areas/code_repos/repo_openclaw_channels_voice_phone.md \
  areas/code_repos/repo_openclaw_gateway.md areas/code_repos/repo_openclaw_extensions.md \
  areas/code_repos/repo_openclaw_extensions_llm_providers.md areas/code_repos/repo_openclaw_skills.md \
done
# NOTE: entry_openclaw_docs.md is created as a master pre-step (W1) — expected MISSING until then; cited as planned.
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w/≤6cb/≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_agent_runtime_architecture | concept | 420 | 1 | ✅ |
| 2 | oc_auth_credential_semantics | model | 700 | 0 | ✅ |
| 3 | oc_automation_overview | concept | 650 | 1 (mermaid optional / tables) | ✅ |
| 4 | oc_channels_overview | concept | 500 | 0 | ✅ |
| 5 | oc_ci_pipeline_overview | concept | 700 | ≤3 (gh dispatch) | ✅ |
| 6 | oc_ci_release_validation | procedure | 750 | ≤6 (gh workflow run examples, trimmed) | ✅ |
| 7 | oc_ci_codeql_scanning | argument | 550 | ≤1 (profile enum) | ✅ |
| 8 | oc_ci_local_and_docker_e2e | procedure | 750 | ≤6 (pnpm / crabbox blocks, trimmed) | ✅ |
| 9 | oc_clawhub | procedure | 650 | ≤6 (openclaw / clawhub blocks, trimmed from 8) | ✅ |
| 10 | oc_cli | model | 600 | ≤2 (command-tree fence verbatim) | ✅ |

No note approaches caps after the ci.md 4-way split. ci.md's 18 fences distribute ≤6 per child; clawhub trims
8→≤6; cli reproduces the one large command-tree fence once. Mermaid decision-guide in note 3 follows the
master/Obsidian safe-char rule (no pipes/brackets/Unicode-arrows in node labels) or is rendered as the prose
+ decision table instead.

## Entry Point Decision (inherited from master)

Contributes **10 rows** to `0_entry_points/entry_openclaw_docs.md` (CREATED as master pre-step W1; >30 master
total ⇒ required) under a **"Top-level"** cluster (shared with rt02/rt03). Each note gets its entry-point
back-link at finalization (satisfies G7/G8). No separate entry point for rt01 alone.

## Inlinks (existing notes → new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify at execution; each satisfies G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (planned, master W1) → **all 10** notes (primary anti-island guarantor).
- `repo_openclaw_agents.md` → notes 1, 2, 3 (runtime/auth/automation impl).
- `repo_openclaw_security.md` → notes 2, 7 (auth contract / CodeQL security boundary).
- `repo_openclaw_channels.md` (+ `_messaging`, `_voice_phone`) → note 4 (channel framework).
- `repo_openclaw.md` → notes 5, 6, 8 (the repo whose CI/release/local-E2E these document).
- `repo_openclaw_skills.md` / `repo_openclaw_extensions.md` → note 9 (ClawHub skill/plugin surfaces).
- `repo_openclaw_cli_wizard.md` → note 10 (CLI/onboard impl).
- `term_openclaw.md` → notes 1, 9, 10; `term_ci_cd.md` → notes 5, 6, 7, 8; `term_cron.md` → note 3;
  `term_authentication.md` → note 2 (reciprocal Related-Notes backlinks).

## Pacing Rules (inherited from master)

One phase (10 notes ≤ 30-agent fan-out cap). Re-read each source page; reproduce command/config snippets
verbatim and selectively. One BB per note. Reindex incrementally; verify `note_links` + 0 broken links + G8
in-degree ≥1 before commit. `git pull --rebase --autostash` first; commit+push after the phase; no Claude
co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** per-note Related-Notes mapping raised to the locked floors (≥8 `term_dictionary`
terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/` per note), relevance-selected from a
fresh re-read of all 7 source pages (`inbox/openclaw_docs/{agent-runtime-architecture,auth-credential-semantics,
replaced by `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

**What was locked — per-note counts (all floors met):**

| # | Note | Terms | Snippets | Docs (existing/planned-sibling) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| 1 | oc_agent_runtime_architecture | 9 | 11 | 11 (9 existing + 2 sibling) | 5 | ✅ 8/10/10 |
| 2 | oc_auth_credential_semantics | 9 | 11 | 11 (9 + 2) | 4 | ✅ |
| 3 | oc_automation_overview | 9 | 10 | 11 (9 + 2) | 3 | ✅ |
| 4 | oc_channels_overview | 9 | 12 | 11 (9 + 2) | 4 | ✅ |
| 5 | oc_ci_pipeline_overview | 8 | 10 | 11 (8 + 3) | 3 | ✅ |
| 6 | oc_ci_release_validation | 8 | 10 | 11 (8 + 3) | 3 | ✅ |
| 7 | oc_ci_codeql_scanning | 8 | 10 | 11 (8 + 3) | 3 | ✅ |
| 8 | oc_ci_local_and_docker_e2e | 8 | 11 | 11 (8 + 3) | 3 | ✅ |
| 9 | oc_clawhub | 9 | 10 | 11 (9 + 2) | 3 | ✅ |
| 10 | oc_cli | 9 | 11 | 11 (8 + 3) | 3 | ✅ |

Every cited term (≥8/note), snippet (≥10/note, ALL from the existing `snippet_openclaw_*` corpus), repo, and
non-CI notes cite 2 planned siblings + ≥9 existing. `entry_openclaw_docs` (master W1) is the sole intentionally
"planned" cross-ref for discoverability.

**New corpora leveraged (vs the plan-stage candidate list):** the rich `snippet_openclaw_*` corpus (253 snippets)
supplied every snippet; the `claude_code/` (339), `hermes_agent/` (226), `pi/` (42), `band/` (59) doc corpora
supplied all existing docs. Additional relevant existing terms surfaced and added beyond the plan-stage set:
`term_auth_profile`, `term_credential_pool`, `term_pkce`, `term_cron_expression`, `term_orchestration`,
`term_persistent_goal`, `term_socket_mode`, `term_block_kit`, `term_channel_kernel`, `term_dm_pairing`,
`term_plugin_sdk`, `term_compaction`, `term_context_engine`, `term_dependency_confusion`, `term_npm_scoping`,
`term_skills_hub`, `term_plugin_manifest`, `term_tool_descriptor`, `term_deny_first`, `term_ssrf_guard`,

**New-term candidates (probed MISSING, NOT created — corpus decision deferred to master):**
- `term_codeql` — GitHub CodeQL static security-analysis engine. Best-fit glossary if ever captured:
  `0_entry_points/acronym_glossary_a_to_c.md` (alpha "C") or the dev-tooling glossary. Disposition: link
  `term_threat_model`/`term_ci_cd` in note 7 instead; do NOT create in rt01.
- `term_static_analysis` / `term_sast` — same disposition. Best-fit glossary: `acronym_glossary_s_to_z.md`.
- `term_semver` / `term_telemetry` / `term_cli` / `term_messaging_platform` — generic dev terms; OpenClaw vocab is
  digested as `oc_*` docs per master design, not new term_dictionary entries. **Net new term_dictionary notes: 0.**

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_rt01.md
Date: 2026-06-21
```

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6 + G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (now ≥8t/≥10s/≥10d), G5 ghost-detect (`/tessellum-fix-ghost-references`), G6 broken-link (`/tessellum-fix-broken-links`), G7+G8 discoverability/in-degree — all 8 in the single-phase table. |
| CP4 | Plan size ≤30 or split | **PASS** | 10 planned notes (≤30); ci.md correctly split 4-way (notes 5–8) by task cluster + caps. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited from master, derived from `claude_code/` (`cc_*`) + `pi/` (`pi_*`) corpora: `# OpenClaw — Title` → `## Overview` → mirrored H2/H3 → `## Related Notes` → `## References` → bold `**Source**`/`**Last Updated**`/`**Status**` footer; YAML field order + forbidden-fields list match existing notes (verified `cc_*`/`pi_*` use `## Overview`/`## Related Notes`, not `## Definition`). |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 10 notes ≤750w / ≤6 code / ≤400L after the ci.md split; no borderline note unaddressed; mermaid in note 3 follows the Obsidian safe-char rule or renders as prose+table. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages (`sed -n '/^---$/,/^---$/!p' \| wc -w`): agent-runtime 261 (plan 280), auth 668 (702), automation 967 (1013), channels 541 (574), ci 8358 (8419), clawhub 721 (771), cli 959 (993). Every ratio 0.93–0.95 — within the 0.7–1.3 band; ci.md confirmed >3× cap (split is correct). |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (10 disposition rows, all → `oc_*` doc home + link existing terms; net new term_dictionary = 0); `## Term-Note Authoring Requirements` present (N/A justified — 0 new terms, master inherits the multi-source-research mandate if `term_codeql`/`term_static_analysis` ever promoted corpus-wide). |
| CP8f | Term-slug + all-notes dedup/collision audit | **PASS** | Slug specificity: no too-general slugs created (rt01 creates 0 term slugs). Collision/dedup audit generalized to ALL planned notes across term_dictionary AND documentation/: each `oc_*` doc note checked against `term_*` (e.g. `oc_cli` vs `term_cli` MISSING; `oc_clawhub` vs `term_skills_hub` — distinct concept, linked not duplicated) and against existing `repo_openclaw*` (15 — LINKED, not recreated). No doc-note duplicates a substantive existing note. Candidate new terms re-probed MISSING. |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
</content>
</invoke>
