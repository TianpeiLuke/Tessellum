---
title: Sub-Plan rf05 — OpenClaw Docs: Reference (USER.dev template, tests, token-use, transcript-hygiene, wizard)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["reference/templates/USER.dev", "reference/test", "reference/token-use", "reference/transcript-hygiene", "reference/wizard"]
---

# Sub-Plan rf05: Reference

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format/YAML, dedup-before-create, 9-GATE, cross-references,
> Undigested-Terms ownership, and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master.
> This file maps its 5 assigned Reference pages (measured below) to BB-atomic `oc_*` notes; the exact per-note Related

## Scope

The five "tail" Reference pages of the OpenClaw docs (Phase B, P2): the dev-agent `USER.dev` workspace template stub,
the developer **test-runner / benchmark reference** (`reference/test`), the **token-use & cost** reference
(`reference/token-use`), the **transcript-hygiene** provider-sanitization reference (`reference/transcript-hygiene`),
and the **onboarding wizard reference** (`reference/wizard`). These pages are reference material the conceptual
(`concepts/*`), gateway (`gateway/*`), CLI (`cli/*`), and start (`start/*`) sub-plans point at: token accounting,
context-window composition, the onboarding flag/step contract, and the per-provider transcript-repair matrix.
Priority **P2** — they document operational/contract detail rather than core architecture, but token-use and
transcript-hygiene are heavily cross-referenced by the concepts corpus. The code side
(`repo_openclaw_sessions`, `repo_openclaw_gateway`, `repo_openclaw_cli_wizard`, `repo_openclaw_agents`) is **LINKED,
not recreated**.

**Source**: OpenClaw docs, 5 pages, **8,009 measured words**. **Planned: 7 notes** (master estimate 8; locks to 7 here —
the 99-word `USER.dev` stub is one thin note, `test` splits 2, `wizard` splits 2, `token-use` + `transcript-hygiene`
1 each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| USER.dev template | reference/templates/USER.dev | 99 | 0 | 1 | 0 | model (config/template artifact) |
| Tests | reference/test | 3,187 | 2 | 8 | 0 | procedure (split: test-running vs benchmarks) |
| Token use and costs | reference/token-use | 1,573 | 4 | 7 | 3 | concept |
| Transcript hygiene | reference/transcript-hygiene | 1,521 | 0 | 9 | 0 | model (provider sanitization-rule reference) |
| Onboarding reference | reference/wizard | 1,629 | 3 | 6 | 1 | procedure (split: flow/steps vs outputs+RPC+signal) |

H2/H3 inventory (measured):
- `USER.dev` H2: Related.
- `test` H2: Local PR gate · Model latency bench (local keys) · CLI startup bench · Gateway startup bench · Gateway restart bench · Onboarding E2E (Docker) · QR import smoke (Docker) · Related. (Plus a leading un-headed bullet block of `pnpm test*` commands above the first H2.)
- `token-use` H2: How the system prompt is built · What counts in the context window · How to see current token usage · Cost estimation (when shown) · Cache TTL and pruning impact · Tips for reducing token pressure · Related. H3 (under Cache TTL): Example: keep 1h cache warm with heartbeat · Example: mixed traffic with per-agent cache strategy · Anthropic 1M context.
- `transcript-hygiene` H2: Global rule: runtime context is not user transcript · Where this runs · Global rule: image sanitization · Global rule: malformed tool calls · Global rule: incomplete reasoning-only turns · Global rule: inter-session input provenance · Provider matrix (current behavior) · Historical behavior (pre-2026.1.22) · Related.
- `wizard` H2: Flow details (local mode) · Non-interactive mode · Gateway wizard RPC · Signal setup (signal-cli) · What the wizard writes · Related docs. H3 (under Non-interactive mode): Add agent (non-interactive).

## Content Strategy

- **Prioritize**: `token-use` (context-window composition + `/status`/`/usage` + cost/cache — referenced across
  concepts/gateway) and `transcript-hygiene` (the per-provider sanitization matrix — the single source of truth for
  provider-specific transcript repair). Both kept atomic, one BB each.
- **Split** (word-cap + mixed-BB): `test.md` (3,187w > 2,500) → `oc_reference_test_commands` (the `pnpm test*` lane
  catalog + Local PR gate + Docker smokes — a test-running procedure) and `oc_reference_benchmarks` (the four
  `bench-*` scripts: model-latency, CLI-startup, gateway-startup, gateway-restart — a benchmarking procedure with
  distinct task cluster). `wizard.md` (1,629w; two distinct task clusters) → `oc_reference_onboarding_flow` (the
  10-step interactive flow + non-interactive flags + add-agent) and `oc_reference_onboarding_outputs`
  (What the wizard writes + Gateway wizard RPC + Signal setup). Splitting keeps each ≤6 code fences and one BB.
- **Thin note**: `USER.dev` (99w) → a single small `model`-BB template note documenting the dev-agent (C-3PO)
  identity artifact; it links the USER template (owned by rf04) rather than restating it.
- **Link-out (do NOT duplicate)**: `/help/testing`, `/help/testing-live`, `/help/testing-updates-plugins` (Help
  sub-plans hp01/hp02) · `/concepts/system-prompt`, `/concepts/context`, `/concepts/session-pruning`,
  `/concepts/usage-tracking`, `/concepts/session` (Concepts co01–07) · `/reference/prompt-caching`,
  `/reference/api-usage-costs`, `/reference/session-management-compaction`, `/reference/secret-placeholder-conventions`
  (Reference rf01–rf03) · `/gateway/configuration` (Gateway gw02) · `/start/wizard`, `/start/onboarding`,
  `/start/wizard-cli-automation`, `/start/wizard-cli-reference` (Start st02) · `/concepts/oauth`, `/concepts/agent-workspace`
  (Concepts) · provider/channel pages (providers/channels sub-plans). These are cross-references, not re-digests.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_reference_templates_user_dev.md` | model | reference/templates/USER.dev (whole page) | 220 | The dev-gateway `USER.dev` template: the default dev-agent user profile ("The Clawdributors", workspace tz Europe/Vienna) that seeds the C-3PO dev agent's identity; documents the template's role and fields and links the base USER template. |
| 2 | `oc_reference_test_commands.md` | procedure | test.md: leading `pnpm test*` command catalog, Local PR gate, Onboarding E2E (Docker), QR import smoke (Docker), Related | 650 | Running OpenClaw's local test suite: the `pnpm test` / `test:changed` / `test:force` / `test:coverage` lane catalog, scoped vs full-suite routing, shared test-state helpers, Docker E2E lanes, and the local PR land/gate command set. |
| 3 | `oc_reference_benchmarks.md` | procedure | test.md: Model latency bench, CLI startup bench, Gateway startup bench, Gateway restart bench | 600 | Running OpenClaw's performance benchmarks: the `bench-model`, `bench-cli-startup`, `bench-gateway-startup`, and `bench-gateway-restart` scripts — usage, presets/case ids, `/healthz`-vs-`/readyz` semantics, and built-entry-vs-source-runner baseline discipline. |
| 4 | `oc_reference_token_use.md` | concept | token-use.md (whole page incl. 3 H3) | 700 | How OpenClaw builds the system prompt, what counts toward the context window, how to read token usage (`/status`, `/usage`, `openclaw status --usage`), cost estimation from model pricing, and cache-TTL/pruning + heartbeat cache-warming + Anthropic 1M context. |
| 5 | `oc_reference_transcript_hygiene.md` | model | transcript-hygiene.md (whole page) | 700 | The provider-specific transcript sanitization/repair contract: the global rules (runtime-context separation, image/tool-call/reasoning-turn cleanup, inter-session provenance) and the per-provider matrix (OpenAI/Codex, Chat-Completions, Google/Gemini, Anthropic/Minimax, Bedrock Converse, Mistral, OpenRouter) plus historical pre-2026.1.22 behavior. |
| 6 | `oc_reference_onboarding_flow.md` | procedure | wizard.md: Flow details (local mode) 10 steps, Non-interactive mode + Add agent (non-interactive) | 700 | The full `openclaw onboard` reference: the 10-step interactive flow (config detection/reset, model/auth, workspace, gateway, channels, web search, daemon install, health check, skills, finish) and non-interactive automation flags including `agents add`. |
| 7 | `oc_reference_onboarding_outputs.md` | procedure | wizard.md: What the wizard writes, Gateway wizard RPC, Signal setup (signal-cli), Related docs | 450 | What onboarding writes to `~/.openclaw/openclaw.json` and the state dir (agents/gateway/channels/skills config fields, auth-profiles, sessions, WhatsApp creds), the Gateway `wizard.*` RPC surface, and the `signal-cli` install flow. |

## Section Coverage Map

```
reference/templates/USER.dev.md
├── (frontmatter + USER profile body: Name/Address/Pronouns/Timezone/Notes) → note 1 (oc_reference_templates_user_dev)
└── ## Related (USER template) ─────────────────────────────────────────── → note 1 (links rf04 USER)

reference/test.md
├── (leading un-headed `pnpm test*` command catalog: test/changed/force/coverage,
│    shards/lanes, shared test-state, Docker E2E lanes, plugins smoke) ────── → note 2 (oc_reference_test_commands)
├── ## Local PR gate ──────────────────────────────────────────────────── → note 2
├── ## Onboarding E2E (Docker) ────────────────────────────────────────── → note 2
├── ## QR import smoke (Docker) ───────────────────────────────────────── → note 2
├── ## Model latency bench (local keys) ───────────────────────────────── → note 3 (oc_reference_benchmarks)
├── ## CLI startup bench ──────────────────────────────────────────────── → note 3
├── ## Gateway startup bench ──────────────────────────────────────────── → note 3
├── ## Gateway restart bench ──────────────────────────────────────────── → note 3
└── ## Related (Testing / Testing live / Testing updates) ─────────────── → note 2 (References link-out → hp01/hp02)

reference/token-use.md
├── (intro: tokens not characters, ~4 chars/token) ────────────────────── → note 4 (oc_reference_token_use)
├── ## How the system prompt is built ─────────────────────────────────── → note 4
├── ## What counts in the context window ──────────────────────────────── → note 4
├── ## How to see current token usage ─────────────────────────────────── → note 4
├── ## Cost estimation (when shown) ───────────────────────────────────── → note 4
├── ## Cache TTL and pruning impact ───────────────────────────────────── → note 4
│   ├── ### Example: keep 1h cache warm with heartbeat ────────────────── → note 4
│   ├── ### Example: mixed traffic with per-agent cache strategy ──────── → note 4
│   └── ### Anthropic 1M context ──────────────────────────────────────── → note 4
├── ## Tips for reducing token pressure ───────────────────────────────── → note 4
└── ## Related (api-usage-costs / prompt-caching / usage-tracking) ────── → note 4 (References link-out)

reference/transcript-hygiene.md
├── (intro: provider-specific in-memory fixes + session-file repair + .bak) → note 5 (oc_reference_transcript_hygiene)
├── ## Global rule: runtime context is not user transcript ─────────────── → note 5
├── ## Where this runs ────────────────────────────────────────────────── → note 5
├── ## Global rule: image sanitization ────────────────────────────────── → note 5
├── ## Global rule: malformed tool calls ──────────────────────────────── → note 5
├── ## Global rule: incomplete reasoning-only turns ───────────────────── → note 5
├── ## Global rule: inter-session input provenance ────────────────────── → note 5
├── ## Provider matrix (current behavior) ─────────────────────────────── → note 5
├── ## Historical behavior (pre-2026.1.22) ────────────────────────────── → note 5
└── ## Related (session / session-pruning) ────────────────────────────── → note 5 (References link-out)

reference/wizard.md
├── ## Flow details (local mode) [10 <Step> blocks] ───────────────────── → note 6 (oc_reference_onboarding_flow)
├── ## Non-interactive mode ───────────────────────────────────────────── → note 6
│   └── ### Add agent (non-interactive) ───────────────────────────────── → note 6
├── ## Gateway wizard RPC ─────────────────────────────────────────────── → note 7 (oc_reference_onboarding_outputs)
├── ## Signal setup (signal-cli) ──────────────────────────────────────── → note 7
├── ## What the wizard writes ─────────────────────────────────────────── → note 7
└── ## Related docs ───────────────────────────────────────────────────── → note 7 (References link-out → st02 etc.)
```

No orphaned sections. All link-out targets (Help, Concepts, Start, other Reference, Gateway, providers/channels) are
cross-references owned by other sub-plans, NOT re-digested here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| test.md (3,187w, 8 H2, 2 code) | note 2 (`oc_reference_test_commands`) + note 3 (`oc_reference_benchmarks`) | Exceeds the 2,500-word cap and mixes two distinct procedural task clusters: running the test suite (lanes/PR-gate/Docker smokes) vs running the four performance benchmarks (`bench-*` scripts). Splitting keeps each ≤700w, one BB, ≤6 code fences. |
| wizard.md (1,629w, 6 H2, 3 code) | note 6 (`oc_reference_onboarding_flow`) + note 7 (`oc_reference_onboarding_outputs`) | Two distinct procedures: the interactive/non-interactive onboarding *flow* (10 steps + flags) vs the *outputs/integration* surface (config fields written, `wizard.*` RPC, signal-cli install). Split keeps each focused, ≤6 fences, and lets the flow note carry the step contract without diluting the config-output reference. |
| USER.dev.md (99w) | note 1 only (no split) | Far below caps; a single thin template artifact note. Not merged into rf04's USER note (separate page, separate slug); links it instead. |
| token-use.md (1,573w) | note 4 only (no split) | Single coherent concept (token accounting / context composition / cost / cache), ≤2,500w, 4 fences; keep atomic. |
| transcript-hygiene.md (1,521w) | note 5 only (no split) | Single coherent reference model (sanitization rules + provider matrix), ≤2,500w, 0 fences; keep atomic — the provider matrix is the note's reason to exist and must stay together. |

## Summary Statistics & Building Block Distribution

- Source pages: **5** (8,009 measured words). New `oc_` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×4 (notes 2, 3, 6, 7) · concept ×1 (note 4) · model ×2 (notes 1, 5).
- Est. digest words ~**4,020** (avg ~574/note); all notes ≤700w (well under the 2,500w cap).
- Source code fences: 9 total (USER.dev 0 · test 2 · token-use 4 · transcript-hygiene 0 · wizard 3) distribute across
  the procedure/concept notes; each note kept ≤6 (config/command snippets reproduced selectively, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21, see **Per-Note Related Notes Mapping**): each note carries
  note; remainder sibling `oc_*` Reference docs planned this series) + 4 `repo_openclaw*` + `entry_openclaw_docs`,
  note 5 = 10 · note 6 = 10 · note 7 = 9. All 7 notes meet the raised floors.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

rendered `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`. Every EXISTING note_id below was
remainder are sibling `oc_*` Reference docs marked **(planned, this series)** toward the 10-doc floor. Relative paths
are FROM `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`, sibling oc_ → `oc_*.md`, other
doc → `../<folder>/`, repo → `../../../areas/code_repos/`, snippet → `../../code_snippets/`, entry →
`../../../0_entry_points/`. `term_observability` / `term_system_prompt` / `term_streaming` / `term_telemetry` /
`term_pricing` / `term_daemon` / `term_systemd` are **NOT in the DB** and are excluded from every set (no ghosts).

### oc_reference_templates_user_dev (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: USER.dev is the dev-gateway identity artifact for this harness.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime scaffold that drives an LLM agent; relevance: C-3PO "lives in" the OpenClaw harness this template seeds.
- [Persona](../../term_dictionary/term_persona.md) — configured agent identity/voice; relevance: the file IS the dev agent's persona (name, pronouns, notes).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed code agents; relevance: C-3PO is the OpenClaw dev coding agent the profile bootstraps.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — durable agent memory across sessions; relevance: USER.md is part of the workspace/bootstrap files framing agent continuity.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: the dev agent commonly runs on a Claude model in the harness.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — agent task workflow; relevance: USER.dev is a workspace-bootstrap file the agent loads to do work.
- [Idempotency](../../term_dictionary/term_idempotency.md) — same-input-same-result reruns; relevance: re-seeding workspace templates is idempotent (onboarding does not wipe on re-run).

**Docs**
- [oc_reference_templates_user](oc_reference_templates_user.md) — base USER profile template (rf04); relevance: USER.dev is the dev variant that mirrors this base template (planned, rf04 sibling sub-plan).
- [oc_reference_onboarding_flow](oc_reference_onboarding_flow.md) — onboarding flow; relevance: the Workspace step seeds these template files (planned, this series).
- [oc_reference_onboarding_outputs](oc_reference_onboarding_outputs.md) — onboarding outputs; relevance: `agents.defaults.workspace` points at where this file lives (planned, this series).
- [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — CLAUDE.md memory/identity files; relevance: closest Claude-Code analog of the AGENTS/USER bootstrap-file convention.
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory model; relevance: USER.md/MEMORY.md continuity is the same bootstrap-memory pattern.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory capture; relevance: dev-agent identity persists via the same auto-memory mechanism.
- [hermes_personality_soul](../hermes_agent/hermes_personality_soul.md) — SOUL.md persona file; relevance: Hermes' personality file is the direct cross-harness analog of USER.dev persona.
- [hermes_context_files](../hermes_agent/hermes_context_files.md) — Hermes context/bootstrap files; relevance: same workspace-context-file injection pattern.
- [pi_prompt_templates](../pi/pi_prompt_templates.md) — pi prompt templates; relevance: cross-harness template-artifact precedent.
- [band_agent_lifecycle](../band/band_agent_lifecycle.md) — Band agent lifecycle/identity; relevance: cross-framework agent-identity bootstrap precedent.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: ships the dev-gateway templates.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents runtime; relevance: loads workspace/bootstrap files (incl. USER.md) into the prompt.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: seeds the workspace template files at the Workspace step.

**Snippets**
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity resolution; relevance: how the runtime derives the dev agent's identity the template feeds.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope/config; relevance: per-agent scoping that the dev profile participates in.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — bootstrap-file context injection; relevance: USER.md is injected via this path.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap char budget; relevance: caps how much of the template files gets injected.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config write; relevance: writes the workspace path the template lives under.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — root memory files (MEMORY.md); relevance: sibling bootstrap-file handling alongside USER.md.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: agentic-memory framing of the dev profile's notes.
- [snippet_openclaw_gateway_agent_identity_reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — agent identity reset; relevance: re-seeds/resets the dev agent identity artifact.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — wizard prompter; relevance: prompts that drive workspace template seeding.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime agent config; relevance: resolves `agents.defaults.workspace` where USER.dev resides.

**Entry**

### oc_reference_test_commands (8t · 10s · 10d)

**Terms**
- [Test Plan](../../term_dictionary/term_test_plan.md) — structured test strategy; relevance: the page is the local Vitest test-running plan (changed/force/coverage lanes).
- [TDD](../../term_dictionary/term_tdd.md) — test-driven development; relevance: `test:changed` + sibling-test mapping support the edit-then-test loop.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: `check:changed`/`check`/`build`/`test` is the local PR-land gate mirroring CI.
- [Canary Testing](../../term_dictionary/term_canary_testing.md) — smoke/canary validation; relevance: Docker QR-import + onboarding E2E are containerized smoke lanes.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: onboarding E2E + QR smoke + `test:docker:*` lanes run in Docker.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable runs; relevance: `test:force` isolates port/state so reruns are deterministic.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the system under test; relevance: this is OpenClaw's own test suite reference.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: pnpm/Vitest/tsx run on Node (Node 24 default, 22 compatible).

**Docs**
- [oc_reference_benchmarks](oc_reference_benchmarks.md) — the `bench-*` half of the same page; relevance: split sibling, continues this page (planned, this series).
- [oc_reference_onboarding_flow](oc_reference_onboarding_flow.md) — onboarding flow; relevance: the onboarding E2E lane drives the wizard documented there (planned, this series).
- [cc_github_actions](../claude_code/cc_github_actions.md) — Claude Code CI workflow; relevance: closest analog of the PR-gate/CI command set.
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — non-interactive CC runs; relevance: scripted PTY-driven E2E test mode parallel.
- [cc_devcontainer_setup](../claude_code/cc_devcontainer_setup.md) — devcontainer testing; relevance: containerized test-env precedent for Docker E2E.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — sandboxed execution; relevance: isolated test-state HOME/STATE_DIR parallels sandboxing.
- [hermes_contributing_dev_setup](../hermes_agent/hermes_contributing_dev_setup.md) — Hermes dev/test setup; relevance: cross-harness local dev/test command analog.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Hermes Docker modes; relevance: Docker E2E lane analog in a sibling harness.
- [pi_development](../pi/pi_development.md) — pi development workflow; relevance: cross-harness local-build-and-test precedent.
- [pi_containerization](../pi/pi_containerization.md) — pi containerization; relevance: Docker-based test image precedent.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: owns the Vitest configs/lanes and `scripts/*`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: gateway E2E + integration lanes start a real Gateway.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — wizard; relevance: onboard-docker / QR smoke exercise the wizard.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels; relevance: channel/plugin shards and `test:channels`/`test:extensions`.

**Snippets**
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: the surface the startup/health test cases exercise.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: routing under test for command lanes.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: cold-start path the onboarding E2E covers.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway listen/WS; relevance: the port-binding server tests collide with (`test:force`).
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel startup; relevance: gateway-startup E2E and channel shards.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — process exec; relevance: spawns the test child processes / Docker lanes.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process kill-tree; relevance: `test:force` kills lingering gateway holding the port.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config load; relevance: plugin-install/manifest smoke lanes.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: `test:docker:plugins` install/update smoke.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket channel; relevance: representative channel shard under the channels test lane.

**Entry**

### oc_reference_benchmarks (8t · 10s · 10d)

**Terms**
- [Latency](../../term_dictionary/term_latency.md) — response time; relevance: `bench-model` measures per-model median/min/max latency.
- [Throughput](../../term_dictionary/term_throughput.md) — work per unit time; relevance: startup/restart benches report rate and CPU-core ratio.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: benches read `/healthz` (liveness) vs `/readyz` (readiness).
- [CI/CD](../../term_dictionary/term_ci_cd.md) — pipeline gating; relevance: bench fixtures + `*:check` compare against checked-in baselines like a perf gate.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable runs; relevance: built-entry-vs-source-runner baseline discipline keeps runs comparable.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — system under measurement; relevance: these are OpenClaw's own perf scripts.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: `pnpm tsx` / `node --import tsx` run the bench scripts.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: timing artifacts / lane scheduling overlap with Docker bench/test infra.

**Docs**
- [oc_reference_test_commands](oc_reference_test_commands.md) — test-running half of the page; relevance: split sibling, same source page (planned, this series).
- [oc_reference_token_use](oc_reference_token_use.md) — token/cost reference; relevance: model-latency relates to model choice/cost tradeoff (planned, this series).
- [cc_performance_and_stability](../claude_code/cc_performance_and_stability.md) — CC perf/stability; relevance: closest analog of agent-tool perf measurement.
- [cc_fast_mode](../claude_code/cc_fast_mode.md) — latency-optimized mode; relevance: model-latency-vs-quality tradeoff parallel to `bench-model`.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: latency results inform model selection.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — startup/install diagnostics; relevance: CLI-startup-bench analog (cold-start timing).
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — Hermes gateway ops; relevance: gateway startup/restart operational analog.
- [hermes_faq_messaging_perf_profiles_workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — Hermes perf profiles; relevance: cross-harness perf-profiling precedent.
- [pi_cli_reference](../pi/pi_cli_reference.md) — pi CLI; relevance: CLI-startup surface analog for startup bench.
- [pi_development](../pi/pi_development.md) — pi dev/build; relevance: built-vs-source runner distinction parallel.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: hosts `scripts/bench-*.ts` and fixtures.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: gateway-startup/restart benches target the Gateway process.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI; relevance: CLI-startup bench measures the CLI entry.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents; relevance: model-latency bench exercises the model/provider runner.

**Snippets**
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — latency/cache status; relevance: runtime latency surfacing parallel to bench-model.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP listen/WS; relevance: gateway-startup bench times the HTTP listen log.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — post-attach startup; relevance: `/readyz` settles after this post-attach work the bench measures.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache respawn; relevance: built-entry vs source-runner baseline the bench distinguishes.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: `OPENCLAW_GATEWAY_STARTUP_TRACE`/`RESTART_TRACE` env the benches set.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: the cold-start path CLI-startup bench times.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root guard; relevance: early-startup branch counted in startup timing.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: restart bench uses SIGUSR1 in-process restart/handoff.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — server shutdown; relevance: restart bench measures close/drain phases.
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — model fallback observation; relevance: per-model timing/observation parallel to bench-model output.

**Entry**

### oc_reference_token_use (10t · 12s · 10d)

**Terms**
- [Context Window](../../term_dictionary/term_context_window.md) — model input budget; relevance: the page is "what counts in the context window" + 1M-context sizing.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — provider prompt cache; relevance: cache TTL/pruning + cacheRead/cacheWrite cost is a core section.
- [Tokenization](../../term_dictionary/term_tokenization.md) — text→token split; relevance: opens with "tokens not characters, ~4 chars/token".
- [KV Cache](../../term_dictionary/term_kv_cache.md) — key-value attention cache; relevance: prompt-cache reads/writes are the KV-cache mechanism behind the cost.
- [Compaction](../../term_dictionary/term_compaction.md) — session summarization; relevance: `/compact` + cache-ttl pruning reduce token pressure.
- [Context Engine](../../term_dictionary/term_context_engine.md) — context assembly system; relevance: "how the system prompt is built" / bootstrap injection is context-engine work.
- [Context Compression](../../term_dictionary/term_context_compression.md) — shrinking context; relevance: image downscale + pruning + tool-result caps compress context.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: token accounting is per-model (OpenAI-style ~4 chars/token).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: Anthropic 1M context + cache-read/write pricing called out specifically.
- [Multimodal](../../term_dictionary/term_multimodal.md) — image/audio inputs; relevance: vision-token usage from image payloads counts toward the window.

**Docs**
- [oc_reference_transcript_hygiene](oc_reference_transcript_hygiene.md) — transcript sanitization; relevance: image sanitization controls token pressure documented here (planned, this series).
- [oc_reference_benchmarks](oc_reference_benchmarks.md) — perf benches; relevance: per-model latency relates to cost/model choice (planned, this series).
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — CC context-window breakdown; relevance: direct analog of "what counts in the context window".
- [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — per-feature context cost; relevance: parallels per-section system-prompt cost accounting.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — token-reduction tips; relevance: direct analog of "tips for reducing token pressure".
- [cc_cost_tracking](../claude_code/cc_cost_tracking.md) — CC cost tracking; relevance: analog of `/usage cost` + model-pricing cost estimation.
- [cc_cache_lifetime_and_scope](../claude_code/cc_cache_lifetime_and_scope.md) — cache TTL/scope; relevance: analog of cache-TTL window + heartbeat keep-warm.
- [cc_extended_context_1m](../claude_code/cc_extended_context_1m.md) — 1M context; relevance: direct analog of the Anthropic 1M context section.
- [pi_compaction](../pi/pi_compaction.md) — pi compaction; relevance: cross-harness compaction/pruning precedent.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — Hermes context/cache; relevance: cross-harness context-compression + caching analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents runtime; relevance: assembles system prompt + cache sections + bootstrap budgets.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: session pruning + cache-TTL pruning live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: `/status`/`/usage`, pricing bootstrap, cost summaries.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: top-level config knobs (contextLimits, bootstrapMaxChars).

**Snippets**
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — system-prompt cache sections; relevance: how cacheable prompt prefixes are built.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — context injection; relevance: bootstrap-file injection counted in the window.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window guard; relevance: enforces the runtime context-share guard / tool-result caps.
- [snippet_openclaw_agents_context_lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — context lookup; relevance: resolves `context.used` from the latest prompt snapshot.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — Anthropic cache prefix; relevance: cache-prefix construction for Anthropic cache reads.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap budget; relevance: `bootstrapMaxChars`/`bootstrapTotalMaxChars` caps.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — daily cost summary; relevance: backs `/usage cost` local cost summary.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/cache status; relevance: `/status` token + cacheRead/cacheWrite display.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing lookup; relevance: resolves `models.providers.*.models[].cost`.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM pricing; relevance: the background pricing-catalog bootstrap.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunking; relevance: compaction summaries that prune the window.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compact/reset; relevance: cache-TTL pruning resets the cache window.

**Entry**

### oc_reference_transcript_hygiene (10t · 12s · 10d)

**Terms**
- [Session Sanitization](../../term_dictionary/term_session_sanitization.md) — cleaning persisted turns; relevance: the page IS the transcript sanitization/repair contract.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-call protocol; relevance: tool-call id sanitization + tool-result pairing repair.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning; relevance: thinking/thought-signature cleanup + reasoning-only turn dropping.
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock Converse; relevance: empty assistant error-turn repair for Bedrock Converse replay.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — Responses transport; relevance: `rs_*`/`call_*|fc_*` reasoning-item pairing rules.
- [Compaction](../../term_dictionary/term_compaction.md) — session summarization; relevance: pre-compaction thinking-signature stripping (signatures bound to prefix).
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — per-provider dispatch; relevance: the provider matrix selects rules by provider/modelApi/modelId.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial input; relevance: inter-session provenance marks foreign-session output vs end-user instructions.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — model route switch; relevance: drop replayable OpenAI reasoning after a model route switch.
- [Multimodal](../../term_dictionary/term_multimodal.md) — image inputs; relevance: image payload sanitization is a global hygiene rule.

**Docs**
- [oc_reference_token_use](oc_reference_token_use.md) — token/cost; relevance: image sanitization ↔ token pressure cross-link (planned, this series).
- [oc_reference_onboarding_outputs](oc_reference_onboarding_outputs.md) — onboarding outputs; relevance: sessions storage path the repair pass rewrites (planned, this series).
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — pi stream contract; relevance: the event/content/tool stream shape these rules repair.
- [pi_session_file_format](../pi/pi_session_file_format.md) — pi JSONL session format; relevance: the on-disk JSONL the session-file repair pass rewrites.
- [pi_compaction](../pi/pi_compaction.md) — pi compaction; relevance: post-compaction prefix change motivating signature stripping.
- [cc_agent_sdk_message_types](../claude_code/cc_agent_sdk_message_types.md) — message/turn types; relevance: turn validation/ordering and content-block shape parallels.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — provider errors; relevance: malformed-tool-call drops prevent rate-limit-induced provider rejections.
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — injection defenses; relevance: inter-session provenance is an anti-injection guard.
- [bedrock_converse_api_content_blocks](../aws_bedrock/bedrock_converse_api_content_blocks.md) — Converse content blocks; relevance: Bedrock rejects `content: []`, driving empty-turn repair.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — Hermes provider routing; relevance: cross-harness per-provider transcript-handling analog.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: session-file repair + replay history + provenance live here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents; relevance: embedded runner + `transcript-policy.ts` + `replay-history.ts`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: history display projection for legacy runtime-wrapper turns.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: top-level `agents.defaults.imageMaxDimensionPx` and policy wiring.

**Snippets**
- [snippet_openclaw_agents_btw_streamSimple_sanitize](../../code_snippets/snippet_openclaw_agents_btw_streamSimple_sanitize.md) — stream sanitize; relevance: in-memory replay sanitization the page describes.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitize; relevance: image/attachment payload sanitization global rule.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — transcript scan; relevance: locating session files for the repair pass.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance; relevance: `message.provenance.kind = "inter_session"` tagging.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: the persisted-turn shape sanitized/repaired.
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript; relevance: transcript-facing vs runtime-enriched prompt separation.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: downscale/recompress oversized base64 images.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — image record lifecycle; relevance: managed-image handling behind image sanitization.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: Anthropic/Minimax thinking-signature + turn-merge rules.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: OpenAI/Codex reasoning-item + `call_id|fc_id` pairing rules.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript media pipeline; relevance: media/attachment normalization before replay.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle; relevance: when repair/load (`run/attempt.ts`, `compact.ts`) fires.

**Entry**

### oc_reference_onboarding_flow (10t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the system; relevance: this is the full `openclaw onboard` flow reference.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/auth; relevance: the Model/Auth step + Gateway auth-mode (token/password/SecretRef).
- [OAuth](../../term_dictionary/term_oauth.md) — delegated auth; relevance: Codex/xAI/Ollama subscription OAuth + device-pairing flows.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: `sk-ant-oat-*` / auth-profiles store OAuth tokens during onboarding.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: provider selection (Anthropic/OpenAI/Ollama/MiniMax/...).
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage; relevance: `--secret-input-mode ref` / SecretRef-backed gateway token.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable runs; relevance: re-running onboarding does not wipe unless `--reset`.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding agents; relevance: onboarding sets up the coding agent + workspace.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: Anthropic API key / setup-token / Claude CLI reuse paths.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic coding CLI; relevance: the canonical onboarding-wizard precedent for a coding-agent CLI.

**Docs**
- [oc_reference_onboarding_outputs](oc_reference_onboarding_outputs.md) — onboarding outputs; relevance: the config this flow writes — direct continuation (planned, this series).
- [oc_reference_templates_user_dev](oc_reference_templates_user_dev.md) — dev user template; relevance: Workspace step seeds these template files (planned, this series).
- [cc_authentication](../claude_code/cc_authentication.md) — CC auth; relevance: direct analog of the Model/Auth subscription-vs-API-key choice.
- [cc_amazon_bedrock_setup](../claude_code/cc_amazon_bedrock_setup.md) — Bedrock setup; relevance: provider-credential setup analog (aws-sdk provider path).
- [cc_google_vertex_ai](../claude_code/cc_google_vertex_ai.md) — Vertex provider; relevance: alternate-provider onboarding analog.
- [cc_install](../claude_code/cc_install.md) — CC install; relevance: install/daemon-equivalent first-run setup.
- [pi_quickstart](../pi/pi_quickstart.md) — pi quickstart; relevance: cross-harness first-run onboarding precedent.
- [pi_provider_auth](../pi/pi_provider_auth.md) — pi provider auth; relevance: provider auth-choice analog (API key vs OAuth).
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — Hermes headless OAuth; relevance: the headless/server "complete OAuth elsewhere, copy auth-profiles" tip.
- [hermes_installation](../hermes_agent/hermes_installation.md) — Hermes install; relevance: daemon (systemd/LaunchAgent) install analog.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — wizard; relevance: the `onboard` implementation itself.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: Gateway step (port/bind/auth/tailscale) + daemon-token validation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents; relevance: `agents add` + auth-profiles write.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels; relevance: Channels step (WhatsApp/Telegram/Discord/Signal/iMessage).

**Snippets**
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — wizard prompter; relevance: drives the interactive `<Step>` prompts.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: writes the per-step config decisions.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard setup imports; relevance: step module wiring of the flow.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: existing-config detection/reset/import branch.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential order; relevance: how the Model/Auth step stores/orders credentials.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth; relevance: Claude CLI reuse path during Anthropic auth.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: Gateway step token/password/disable auth-mode logic.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: gateway-token SecretRef resolution at onboarding.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — LaunchAgent render; relevance: macOS daemon-install step.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger; relevance: Linux daemon-install `loginctl enable-linger`.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: Channels step DM-security pairing default.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama local; relevance: Ollama Cloud/Local onboarding sub-flow.

**Entry**

### oc_reference_onboarding_outputs (9t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the system; relevance: the page lists what onboarding writes to `~/.openclaw/openclaw.json` + state dir.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage; relevance: WhatsApp creds + auth-profiles + SecretRef-backed token layout.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: auth-profiles.json stores API keys + OAuth tokens.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/auth; relevance: `gateway.auth.*` mode/bind/token fields written.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC protocol; relevance: the `wizard.start/next/cancel/status` RPC surface.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: sessions stored under `~/.openclaw/agents/<agentId>/sessions/`.
- [Idempotency](../../term_dictionary/term_idempotency.md) — preserve-on-rerun; relevance: existing explicit `tools.profile` values preserved, not overwritten.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: `models.providers` / `agents.defaults.model` provider config fields written.
- [Cron](../../term_dictionary/term_cron.md) — scheduled-run metadata; relevance: `wizard.lastRunAt`/`lastRunVersion`/`lastRunCommit` run-metadata fields the wizard records.

**Docs**
- [oc_reference_onboarding_flow](oc_reference_onboarding_flow.md) — onboarding flow; relevance: the flow that produces these outputs — direct continuation (planned, this series).
- [oc_reference_templates_user_dev](oc_reference_templates_user_dev.md) — dev user template; relevance: `agents.defaults.workspace` points where this file lives (planned, this series).
- [cc_settings_files](../claude_code/cc_settings_files.md) — CC settings files; relevance: direct analog of "what the wizard writes" config-file layout.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env vars; relevance: env-backed credential refs (`keyRef.source = env`) analog.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — CC auth files; relevance: auth-profiles/credentials directory + legacy-import analog.
- [pi_settings_reference](../pi/pi_settings_reference.md) — pi settings; relevance: config-field reference analog.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — pi RPC; relevance: the `wizard.*` RPC surface analog (RPC over the gateway).
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — Hermes config precedence; relevance: cross-harness config-file write/precedence analog.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — Hermes credentials; relevance: credential/secret storage layout analog.
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — Hermes session storage; relevance: sessions/credentials directory layout analog.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — wizard; relevance: what the wizard writes (config + state dir).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: exposes the `wizard.*` RPC + reloads written config.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents; relevance: `agents.list[]` / auth-profiles / sessions dirs.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels; relevance: `channels.*` token/allowlist config fields.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config write; relevance: the actual write of `openclaw.json` fields.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: applies the written config at runtime.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: diff/plan of config changes onboarding makes.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime agent config; relevance: resolves `agents.defaults.*` / `agents.list[]`.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — config/plugins load; relevance: plugin-channel install prompt + config load.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — auth-profile portability; relevance: the "copy auth-profiles.json to gateway host" output behavior.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: SecretRef resolution of written gateway token.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session id resolution; relevance: sessions dir layout written under each agent.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: the `wizard.*` JSON-RPC request/response shape.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the `wizard.*` method group registration.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — session fs index; relevance: sessions/credentials directory read layout.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: channel allowlist name→ID resolution written to config.

**Entry**

> DB-verification (2026-06-21): every EXISTING term/snippet/doc/repo/entry note_id above resolved in
> each note has ≥5 EXISTING docs), and (b) `entry_openclaw_docs` (planned, master pre-step W1). Intentionally EXCLUDED
> because absent from the DB: `term_observability`, `term_system_prompt`, `term_streaming`, `term_telemetry`,
> `term_pricing`, `term_daemon`, `term_systemd`, `term_secret_management`, `term_configuration_management`,
> `term_api_key`, `term_credentials`, `term_benchmark`, `term_unit_testing`, `term_smoke_test` — every term link above

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, NOT promoted to new
`term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms. No term definitions
are inlined in `oc_*` notes.

| Term (page vocabulary) | Disposition |
|---|---|
| token / token use / cost estimation / context window | Documented in note 4 (`oc_reference_token_use`); link existing `term_context_window`, `term_tokenization`, `term_prompt_caching`, `term_kv_cache`. No new term. |
| prompt cache / cache TTL / cacheRead/cacheWrite / cache-ttl pruning | Documented in note 4; link existing `term_prompt_caching`, `term_kv_cache`, `term_compaction`. No new term. |
| system prompt assembly / bootstrap injection | Documented in note 4 (and `/concepts/system-prompt` link-out, Concepts co07). Link existing `term_context_engine`. `term_system_prompt` does NOT exist; not created here (cross-cutting; defer to a Concepts sub-plan if ever needed). No new term. |
| transcript hygiene / sanitization / tool-call repair / thinking-signature cleanup | Documented in note 5 (`oc_reference_transcript_hygiene`); link existing `term_session_sanitization`, `term_function_calling`, `term_chain_of_thought`. No new term. |
| provider matrix / Converse replay / Responses reasoning / turn alternation | Documented in note 5; link existing `term_converse_api`, `term_openai_responses_api`, `term_provider_routing`. No new term. |
| inter-session provenance / inter_session marker | Documented in note 5; link existing `term_prompt_injection` (foreign-session-output guard). No new term. |
| onboarding / wizard / onboard flags / non-interactive mode | Documented in notes 6–7 (`oc_reference_onboarding_*`); link existing `term_idempotency`, `term_authentication`. No new term. |
| SecretRef / auth profiles / gateway token | Documented in notes 6–7; link existing `term_secrets_manager`, `term_oauth_token`, `term_authentication`. No new term. |
| Vitest / test lanes / shards / Docker E2E / bench scripts | Documented in notes 2–3 (`oc_reference_test_commands` / `oc_reference_benchmarks`); link existing `term_test_plan`, `term_canary_testing`, `term_ci_cd`, `term_docker`, `term_latency`. No new term. |
| C-3PO / Clawdributors / dev-agent identity | Documented in note 1 (`oc_reference_templates_user_dev`); link existing `term_persona`, `term_agent_harness`. No new term. |
| provider names (Anthropic, OpenAI/Codex, Gemini, Mistral, MiniMax, Ollama, Bedrock, …) | Documented as config/behavior in the relevant notes; NOT promoted to term notes — link existing `term_llm`/`term_claude`/`term_bedrock`/`term_third_party_genai_services`. No new term. |

**New-term candidates: 0.** No genuinely cross-cutting, vault-reusable term lacking a doc-page home AND an existing note
appears in these 5 pages. (`term_system_prompt` and `term_observability` are absent from the DB but are cross-cutting
concepts whose home is Concepts/other corpora, not this Reference sub-plan; they are intentionally NOT created here.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** rf05 authors zero `term_dictionary` notes. Inherited from master: any new term (none here)
`acronym_glossary_*.md`; no term definition is ever inlined in an `oc_*` note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). All 8 gates must PASS before commit.

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` per note (YAML field order/forbidden fields, H1/H2, indexed `[text](path.md)` links). |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/reference/<page>.md`; no invented commands/flags/config keys; verbatim snippets faithful. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one `building_block` per note; every mapped H2/H3 covered (Section Coverage Map). |
| G5 | Ghost-reference detect + redirect | No link to a non-existent note; DB-verify all targets (drop/redirect `term_observability`/`term_system_prompt`-type ghosts). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after incremental reindex; 0 broken links. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` + the Inlinks section below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_reference_templates_user_dev oc_reference_test_commands oc_reference_benchmarks oc_reference_token_use oc_reference_transcript_hygiene oc_reference_onboarding_flow oc_reference_onboarding_outputs"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  echo "$REQ_SECTIONS" | tr '|' '\n' | while read -r sec; do
    grep -qF "$sec" "$f" || echo "  MISSING SECTION in $n: $sec"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "  MISSING source_url in $n"; }
  # density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "  DENSITY WARNING: $n (words=$words code=$cb lines=$lines)"
  # sibling-prefix cross-ref presence (G4)
  grep -q "($SIBLING_PREFIX" "$f" || grep -q "repo_openclaw" "$f" || echo "  WARN: $n has no oc_/repo_openclaw sibling link"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference DB-verify of every cited target (path note_id form)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
# (augment locks the exact target list; spot-verify e.g.)
for id in resources/term_dictionary/term_context_window.md resources/documentation/claude_code/cc_context_window_anatomy.md areas/code_repos/repo_openclaw_sessions.md 0_entry_points/entry_openclaw_docs.md; do
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences avail. | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_reference_templates_user_dev | model | 220 | 0 | ✅ |
| 2 | oc_reference_test_commands | procedure | 650 | ~2 (from test.md, selective) | ✅ |
| 3 | oc_reference_benchmarks | procedure | 600 | 0–2 (command lists, not fenced in source) | ✅ |
| 4 | oc_reference_token_use | concept | 700 | ≤4 (the 4 token-use yaml fences, selective) | ✅ |
| 5 | oc_reference_transcript_hygiene | model | 700 | 0 | ✅ |
| 6 | oc_reference_onboarding_flow | procedure | 700 | ≤3 (non-interactive + add-agent bash) | ✅ |
| 7 | oc_reference_onboarding_outputs | procedure | 450 | 0–1 | ✅ |

No note approaches the caps. Code-heavy `test.md` split (notes 2/3) and `wizard.md` split (notes 6/7) keep each note
≤6 fences. token-use's 4 YAML examples reproduced selectively in note 4 (still ≤6).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master pre-step W1; `building_block: navigation`)
under the **Reference** section / a "Reference — tail pages (rf05)" cluster. Each new note receives its entry-point
back-link at finalization (satisfies G7/G8). No separate entry point for this sub-plan (the master series hub covers
all 105 sub-plans).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; ≥1 per new note guaranteed via
`entry_openclaw_docs.md`):

- `entry_openclaw_docs.md` → all 7 notes (primary anti-island guarantee).
- `repo_openclaw_sessions` → note 5 (transcript hygiene) , note 4 (token/cache pruning).
- `repo_openclaw_agents` → note 4 (system-prompt/cache), note 5 (embedded runner sanitization).
- `repo_openclaw_cli_wizard` → notes 6, 7 (onboarding flow/outputs), note 2 (onboard-docker E2E).
- `repo_openclaw_gateway` → note 3 (gateway benches), note 7 (`wizard.*` RPC), note 2 (gateway E2E lanes).
- `term_context_window` → note 4; `term_prompt_caching` → note 4; `term_session_sanitization` → note 5;
  `term_test_plan` → note 2; `term_latency` → note 3; `term_authentication`/`term_oauth_token` → notes 6, 7;
  `term_persona` → note 1.
- Existing docs: `cc_context_window_anatomy`/`cc_reduce_token_usage` → note 4; `pi_compaction` → notes 4, 5;
  `pi_custom_streaming_api` → note 5; `cc_authentication` → note 6.

## Pacing Rules (inherited from master)

One execution phase, 7 notes (≤30 fan-out cap). Re-read each source page before authoring; reproduce command/config
snippets verbatim; one BB per note. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before
commit. `git pull --rebase --autostash origin main` first; commit + push the wave together; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** The `## Candidate Cross-References` section was replaced by `## Per-Note Related Notes Mapping
(LOCKED — xref-augment 2026-06-21)` at the RAISED floors (**≥8 terms · ≥10 snippets · ≥10 docs per note**,
note`. Source pages were re-read in full from `inbox/openclaw_docs/reference/` before mapping; the measured word counts
(USER.dev 99 · test 3187 · token-use 1573 · transcript-hygiene 1521 · wizard 1629 = **8009 total**) and code-fence
counts (0/2/4/0/3 = 9) were re-measured with `wc` and match the plan EXACTLY (CP7). Summary Statistics cross-ref line
and the G4 gate row were updated to the raised floors.

**Per-note counts (all floors met).**

| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_reference_templates_user_dev | 8 | 10 | 10 (7 existing / 3 sibling) | 3 | ✅ |
| oc_reference_test_commands | 8 | 10 | 10 (8 existing / 2 sibling) | 4 | ✅ |
| oc_reference_benchmarks | 8 | 10 | 10 (8 existing / 2 sibling) | 4 | ✅ |
| oc_reference_token_use | 10 | 12 | 10 (8 existing / 2 sibling) | 4 | ✅ |
| oc_reference_transcript_hygiene | 10 | 12 | 10 (8 existing / 2 sibling) | 4 | ✅ |
| oc_reference_onboarding_flow | 10 | 12 | 10 (8 existing / 2 sibling) | 4 | ✅ |
| oc_reference_onboarding_outputs | 9 | 12 | 10 (8 existing / 2 sibling) | 4 | ✅ |

`entry_openclaw_docs` (master pre-step W1) are the only non-existent targets, each marked `(planned, this series)` /
planned and counted toward the 10-doc floor only after ≥5 EXISTING docs per note are present.

**Term-set tightening (re-read Step 2d).** No new term candidates surfaced. Candidate terms found absent from the DB
and therefore EXCLUDED (no ghosts): `term_observability`, `term_system_prompt`, `term_streaming`, `term_telemetry`,
`term_pricing`, `term_daemon`, `term_systemd`, `term_secret_management`, `term_configuration_management`,
`term_api_key`, `term_credentials`, `term_benchmark`, `term_benchmarking`, `term_unit_testing`, `term_smoke_test`,
`term_health_check`(present)/... — see the Issues list for the full excluded set. The leanest notes (testing/benchmark)
were brought to 8 verified terms by adding relevance-checked verified terms (`term_tdd`, `term_throughput`,
`term_health_check`, `term_api_gateway` were probed; testing/benchmark notes use the strongest 8). internal

**New-term candidates + best-fit glossary.** **0 new terms.** Consistent with the master's corpus-ownership decision:
OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, not promoted to `term_dictionary`. The
two cross-cutting absent concepts (`term_system_prompt`, `term_observability`) have their home in a Concepts /
diagnostics sub-plan, not this Reference sub-plan; best-fit glossary if ever created would be
`0_entry_points/acronym_glossary_gen_ai.md` (system prompt) — explicitly NOT created here.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review run after xref-augment. 2 source pages spot-re-read for CP7 (token-use, wizard) plus all 5 re-measured.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors | **PASS** | Per-Note Related Notes Mapping present; every note ≥8 terms (8/8/8/10/10/10/9), ≥10 snippets, ≥10 docs (≥5 existing); each link has a relevance statement; 0 bare links. |
| CP2 | 9-GATE present (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (raised floor), G5 Ghost-detect+redirect, G6 Broken-link fix, G7/G8 Discoverability; G5 ghost-DB-verify script present in Validation Scripts. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision` inherits master: 7 rows into `entry_openclaw_docs.md` (`building_block: navigation`), created master pre-step W1; per-note back-link at finalization satisfies G7/G8; no separate entry point (master hub covers all 105 sub-plans). |
| CP4 | Size | **PASS** | 7 notes ≤ 30 fan-out cap; single execution phase. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Format Definition inherited verbatim from master (derived from `claude_code/` `cc_*` + `pi/` `pi_*` corpora — same source type); `## Overview` + `## Related Notes` body, fixed YAML field order, forbidden-field list; verified against existing `cc_context_window_anatomy.md` (building_block model, same convention). |
| CP6 | Density | **PASS** | All 7 notes ≤700w / ≤6 fences / ≤400 lines (Density Re-Assessment table); test.md (3187w) split 2/3, wizard.md (1629w) split 6/7; no borderline note unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured with `wc -w`: USER.dev 99 · test 3187 · token-use 1573 · transcript-hygiene 1521 · wizard 1629 = 8009; code fences 0/2/4/0/3 = 9 — EXACT match to plan (ratio 1.00). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present, all rows dispositioned to "link existing term, no new term"; **0 new terms** (corpus-ownership decision); `## Term-Note Authoring Requirements` = N/A (0 new terms), inheriting master multi-source mandate for any future term. |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to audit. Doc-note collision audit: all 7 planned `oc_reference_*` slugs are NEW (DB count for `resources/documentation/openclaw/%` = 0); none duplicates an existing `term_*` (e.g. no `oc_*` collides with `term_session_sanitization`/`term_compaction` — those are LINKED, not recreated). USER.dev is a separate page/slug from rf04's USER (linked, not merged). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` table covers all 7 notes with ≥1 outside-folder inbound link (entry_openclaw_docs → all 7, plus repo_openclaw_*/term_* inbounds); G8-Discoverability is in the phase gate table; inlink addition is a gated execution phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
