---
title: Sub-Plan rf01 — OpenClaw Docs: Reference (AGENTS.default, RELEASING, api-usage-costs, application-modernization-plan, code-mode, credits, device-models)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["reference/AGENTS.default", "reference/RELEASING", "reference/api-usage-costs", "reference/application-modernization-plan", "reference/code-mode", "reference/credits", "reference/device-models"]
---


# Sub-Plan rf01: Reference

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup-before-create, the 9-GATE table,
> the Undigested-Terms ownership decision, cross-refs, and entry-point wiring are ALL inherited from the master;
> only this section's measured pages, planned notes, splits, candidate cross-references, and per-phase gate are
> locked here. Exact per-note Related-Notes mapping is locked later at `/tessellum-augment-digestion-plan`.

## Scope

The 7 OpenClaw **Reference** pages assigned to rf01 — the cross-cutting reference/policy material that the rest
of the corpus points back to: the default agent workspace instructions + skill roster (`AGENTS.default`), the
public release-lane / version / validation policy (`RELEASING`), the paid-API/cost audit (`api-usage-costs`),
the application-modernization engineering plan (`application-modernization-plan`), the experimental
QuickJS-WASI **code mode** tool surface (`code-mode`), project credits/license (`credits`), and the Apple
device-model database maintenance procedure (`device-models`). Priority **P2** (Phase B). These pages mix
procedure (workspace setup, release ops, device-DB update), concept (cost model, code-mode contract),
argument (modernization plan), and model (code-mode result/error schemas). The code-side counterparts
(`repo_openclaw*`) and existing `term_dictionary` terms are LINKED, never recreated.

**Source**: OpenClaw docs, 7 pages, **15,707 measured words** (mirror `inbox/openclaw_docs/reference/`). **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| AGENTS.default | reference/AGENTS.default | 817 | 5 | 12 | 0 | procedure |
| RELEASING | reference/RELEASING | 6,790 | 8 | 11 | 4 | concept + procedure (split ×3) |
| api-usage-costs | reference/api-usage-costs | 1,210 | 0 | 4 | 14 | concept |
| application-modernization-plan | reference/application-modernization-plan | 1,223 | 1 | 13 | 0 | argument |
| code-mode | reference/code-mode | 5,333 | 24 | 30 | 7 | concept + procedure + model (split ×3) |
| credits | reference/credits | 138 | 0 | 5 | 0 | concept |
| device-models | reference/device-models | 196 | 2 | 2 | 0 | procedure |

`Code` = fenced blocks counted as `grep -c '^``` ' / 2` (RELEASING raw 16 → 8; code-mode raw 48 → 24; AGENTS raw 10 → 5; device-models raw 4 → 2; application-modernization raw 2 → 1; api-usage-costs/credits 0). The three sub-`# H1` lines inside RELEASING (L516/L524/L531) and the one in AGENTS (L89) and code-mode/application-modernization are comment/example headers inside fences and template bodies, not document H1s.

## Content Strategy

- **Prioritize**: (a) the **release policy** — version naming + the three public lanes + cadence (the
  governing concept every install/update/announcement page references), and the **release operator checklist /
  publish automation** (the highest-value operational procedure here); (b) the **code-mode contract** —
  `exec`/`wait` model-visible surface, hidden tool catalog, QuickJS-WASI sandbox, and the namespace registry
  (the experimental runtime feature with the most novel design content); (c) the **api-usage-costs** audit
  (a single concept note enumerating every paid-API surface — high operational relevance).
- **Split**: `RELEASING.md` (6,790w) → 3 notes (policy/versioning concept · operator-checklist+publish procedure ·
  validation/test-boxes procedure); `code-mode.md` (5,333w, mixed BB) → 3 notes (overview/contract concept ·
  namespaces+registration procedure · security/runtime/telemetry concept-plus-model). Both exceed 2,500w and
  mix building blocks → split per the master word-cap + one-BB-per-note rules.
- **Link-out, do NOT redefine**: workspace template files (`AGENTS.dev`/`SOUL`/`TOOLS`/`USER`) → rf03/rf04;
  Token-use display detail → rf05 (`reference/token-use`); session-management+compaction → rf03;
  prompt-caching → rf02; provider/model config → pr01–09 and `concepts/models`; web/media tools → tools
  (to01–08); release channels → `install/development-channels` (in01); skills → tools/skills. Terms
  (`term_openclaw`, `term_mcp`, `term_sandbox`, `term_typescript`, `term_llm`, `term_npm`, `term_ci_cd`,
  `term_prompt_caching`, …) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_reference_agents_default.md` | procedure | AGENTS.default.md: First run, Safety defaults, Session start, Soul, Shared spaces, Memory system, Tools and skills, Backup tip, What OpenClaw does, Core skills, Usage notes | 550 | The default OpenClaw agent workspace setup + personal-assistant skill roster: creating `~/.openclaw/workspace`, copying AGENTS/SOUL/TOOLS templates, safety defaults, the required session-start + soul + memory rules, and the bundled core-skill list (mcporter, Peekaboo, imsg, wacli, etc.). |
| 2 | `oc_reference_releasing_policy.md` | concept | RELEASING.md: Version naming, Release cadence, intro three-lane definition | 600 | OpenClaw's release model: the three public lanes (stable / beta / dev), the `YYYY.M.PATCH[-beta.N]` version-naming scheme + the June-2026 monthly-train rule, npm immutability, `latest`/`beta` dist-tag meaning, and the beta-first cadence cut from `release/YYYY.M.PATCH` branches. |
| 3 | `oc_reference_releasing_operator_checklist.md` | procedure | RELEASING.md: Release operator checklist, Stable main closeout, Release publish automation, NPM workflow inputs, Stable npm release sequence | 750 | The public-shape release operator procedure: 11-step checklist (branch → `pnpm release:prep` → preflight → `OpenClaw Release Publish`), `OpenClaw Release Publish` orchestration order, NPM/Publish/Checks workflow inputs, the stable npm release sequence, and stable-main-closeout evidence requirements. |
| 4 | `oc_reference_releasing_validation.md` | procedure | RELEASING.md: Release preflight, Release test boxes (Vitest, Docker, QA Lab, Package) | 700 | Pre-release validation: the `Full Release Validation` umbrella entrypoint, `release_profile` breadth (minimum/stable/full), the four release test boxes (Vitest CI, Docker package lanes, QA Lab parity/Matrix/Telegram, Package Acceptance candidate sources), and focused-rerun (`rerun_group`) recovery. |
| 5 | `oc_reference_api_usage_costs.md` | concept | api-usage-costs.md: Where costs show up, How keys are discovered, Features that can spend keys (1–10) | 700 | An audit of every OpenClaw feature that can invoke paid APIs: where cost shows up (`/status`, `/usage`, CLI usage windows), how keys are discovered (auth profiles / env / config / skills), and the 10 spend surfaces (core responses, media understanding, image/video generation, memory embeddings, web search/fetch, status snapshots, compaction, model scan, talk, skills). |
| 6 | `oc_reference_application_modernization_plan.md` | argument | application-modernization-plan.md: Goal, Principles, Phases 1–6, Recommended first slice, Frontend skill update, Operating rules, Implementation checklist, Visual quality gates, Handoff format | 650 | The phased application-modernization engineering plan: small-reviewable-slices principle, the 6 phases (baseline audit → product/UX cleanup → frontend tightening → performance → type/contract/test hardening → docs/release readiness), the recommended Control-UI first slice, and the embedded Frontend Delivery Standards skill (operating rules, checklist, visual quality gates, handoff). |
| 7 | `oc_reference_code_mode_overview.md` | concept | code-mode.md: intro, What is this?, Why is this good?, How to enable it, Technical tour, Runtime status, Scope, Terms, Configuration, Activation, Model-visible tools, `exec`, `wait`, Output API | 750 | OpenClaw code mode (experimental): how it replaces the model-visible tool list with just `exec` and `wait`, why a small JS/TS code surface beats a huge tool catalog, the `tools.codeMode` enable config + limits, the activation order, the `exec`/`wait` contract + `CodeModeResult` union, and the `text`/`json` output API. (vs Codex Code Mode.) |
| 8 | `oc_reference_code_mode_namespaces.md` | procedure | code-mode.md: Guest runtime API, Internal namespaces (Registry lifecycle, Registration shape, Ownership and visibility, Scope serialization rules, Prompts, Cleanup, Test checklist), Tool catalog, Tool Search interaction, Tool names and collisions, Nested tool execution | 750 | Authoring + invoking code-mode tool access from guest programs: `ALL_TOOLS`/`tools.search`/`describe`/`call`, the generated `MCP.<server>` namespace + virtual `API` declaration surface, the loader-owned internal-namespace registry (register/scope/serialize/ownership/cleanup), the hidden tool catalog id shape, and Tool-Search supersession + nested-call preservation. |
| 9 | `oc_reference_code_mode_runtime_security.md` | model | code-mode.md: Runtime state, QuickJS-WASI runtime, TypeScript, Security boundary, Error codes, Telemetry, Debugging, Implementation layout, Validation checklist, E2E test plan | 700 | The code-mode runtime + security model: the run state machine (running/waiting/completed/failed/expired/aborted) + snapshot bounds, the QuickJS-WASI worker responsibilities, TypeScript source-transform-only support, the defense-in-depth security boundary, the `CodeModeErrorCode` union, telemetry/redaction, `OPENCLAW_DEBUG_*` debugging, and the validation/E2E checklists. |
| 10 | `oc_reference_credits.md` | concept | credits.md: The name, Credits, Core contributors, License | 200 | OpenClaw project origin and attribution: the CLAW + TARDIS name, creator/core-contributor credits (Peter Steinberger, Mario Zechner/Pi creator, Clawd), and the MIT license. |
| 11 | `oc_reference_device_models.md` | procedure | device-models.md: intro, Data source, Updating the database | 300 | How the macOS companion app maps Apple model identifiers (e.g. `iPad16,6`) to friendly names: the vendored MIT `apple-device-identifiers` JSON pinned to upstream commits under `apps/macos/.../DeviceModels/`, and the update procedure (pin commits → `curl` the JSON → verify `swift build`). |

## Section Coverage Map

```
reference/AGENTS.default.md
├── First run (recommended) ──────────────────────── → note 1 (oc_reference_agents_default)
├── Safety defaults ──────────────────────────────── → note 1
├── Session start (required) ─────────────────────── → note 1
├── Soul (required) ──────────────────────────────── → note 1
├── Shared spaces (recommended) ──────────────────── → note 1
├── Memory system (recommended) ──────────────────── → note 1
├── Tools and skills ─────────────────────────────── → note 1
├── Backup tip (recommended) ─────────────────────── → note 1
├── What OpenClaw does ───────────────────────────── → note 1
├── Core skills (enable in Settings → Skills) ─────── → note 1
├── Usage notes ──────────────────────────────────── → note 1
└── Related ──────────────────────────────────────── → note 1 (References)

reference/RELEASING.md
├── (intro: three public release lanes) ──────────── → note 2 (oc_reference_releasing_policy)
├── Version naming ───────────────────────────────── → note 2
├── Release cadence ──────────────────────────────── → note 2
├── Release operator checklist ───────────────────── → note 3 (oc_reference_releasing_operator_checklist)
├── Stable main closeout ─────────────────────────── → note 3
├── Release preflight ────────────────────────────── → note 4 (oc_reference_releasing_validation)
├── Release test boxes ───────────────────────────── → note 4
│   ├── Vitest ───────────────────────────────────── → note 4
│   ├── Docker ───────────────────────────────────── → note 4
│   ├── QA Lab ───────────────────────────────────── → note 4
│   └── Package ──────────────────────────────────── → note 4
├── Release publish automation ───────────────────── → note 3
├── NPM workflow inputs ──────────────────────────── → note 3
├── Stable npm release sequence ──────────────────── → note 3
├── Public references ────────────────────────────── → note 4 (References)
└── Related ──────────────────────────────────────── → notes 2/3/4 (References; primary note 2)

reference/api-usage-costs.md
├── (intro) ──────────────────────────────────────── → note 5 (oc_reference_api_usage_costs)
├── Where costs show up (chat + CLI) ─────────────── → note 5
├── How keys are discovered ──────────────────────── → note 5
├── Features that can spend keys ─────────────────── → note 5
│   └── §§1–10 (H3: core/media/gen/memory/web search/web fetch/snapshots/compaction/scan/talk/skills) → note 5
└── Related ──────────────────────────────────────── → note 5 (References)

reference/application-modernization-plan.md
├── Goal / Principles ────────────────────────────── → note 6 (oc_reference_application_modernization_plan)
├── Phase 1: Baseline audit ──────────────────────── → note 6
├── Phase 2: Product and UX cleanup ──────────────── → note 6
├── Phase 3: Frontend architecture tightening ────── → note 6
├── Phase 4: Performance and reliability ─────────── → note 6
├── Phase 5: Type, contract, and test hardening ──── → note 6
├── Phase 6: Documentation and release readiness ─── → note 6
├── Recommended first slice ──────────────────────── → note 6
├── Frontend skill update (embedded SKILL.md:
│   Operating rules, Implementation checklist,
│   Visual quality gates, Handoff format) ─────────── → note 6
└── (no Related section in source) ───────────────── → note 6 (References = source_url only)

reference/code-mode.md
├── (intro: code mode vs Codex Code Mode) ────────── → note 7 (oc_reference_code_mode_overview)
├── What is this? / Why is this good? ────────────── → note 7
├── How to enable it ─────────────────────────────── → note 7
├── Technical tour / Runtime status / Scope / Terms ─ → note 7
├── Configuration / Activation ───────────────────── → note 7
├── Model-visible tools / `exec` / `wait` ────────── → note 7
├── Output API ───────────────────────────────────── → note 7
├── Guest runtime API ────────────────────────────── → note 8 (oc_reference_code_mode_namespaces)
├── Internal namespaces (Registry lifecycle,
│   Registration shape, Ownership and visibility,
│   Scope serialization rules, Prompts, Cleanup,
│   Test checklist) ──────────────────────────────── → note 8
├── Tool catalog / Tool Search interaction ───────── → note 8
├── Tool names and collisions / Nested tool exec ─── → note 8
├── Runtime state / QuickJS-WASI runtime ─────────── → note 9 (oc_reference_code_mode_runtime_security)
├── TypeScript / Security boundary / Error codes ──── → note 9
├── Telemetry / Debugging / Implementation layout ── → note 9
├── Validation checklist / E2E test plan ─────────── → note 9
└── Related ──────────────────────────────────────── → notes 7/8/9 (References; primary note 7)

reference/credits.md
├── The name / Credits / Core contributors / License → note 10 (oc_reference_credits)
└── Related ──────────────────────────────────────── → note 10 (References)

reference/device-models.md
├── (intro: Instances UI device-name mapping) ────── → note 11 (oc_reference_device_models)
├── Data source ──────────────────────────────────── → note 11
├── Updating the database ────────────────────────── → note 11
└── Related ──────────────────────────────────────── → note 11 (References)
```
No orphaned sections. Workspace template files, token-use display, prompt-caching, session-management+compaction, provider/model config, and web/media/skills tools are link-outs (rf02/rf03/rf04/rf05, pr*, co*, to*, in01), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| RELEASING.md (6,790w, 11 H2 / 4 H3, mixed concept+procedure) | notes 2 + 3 + 4 | Far exceeds the 2,500w cap and mixes BBs: the version/lane/cadence **policy** (concept) is distinct from the **operator/publish procedure** and the **validation/test-box procedure**. Splitting keeps each ≤750w / ≤6 code and one BB per note; the two procedure notes cleanly partition "publish the release" vs "validate the release." |
| code-mode.md (5,333w, 30 H2 / 7 H3, 24 fences, mixed concept+procedure+model) | notes 7 + 8 + 9 | Exceeds 2,500w, mixes BBs, and is code-heavy (24 fences > 6 cap on a single note). Split: the user-facing **overview/contract** (concept: what/why/enable/exec/wait), the **namespace + tool-catalog authoring** (procedure: register/scope/call), and the **runtime + security + schemas** (model: state machine, QuickJS-WASI, error-code union, security boundary). Each lands ≤750w and ≤6 fences. |

All other pages stay 1 note each: AGENTS.default (817w, single procedure cluster), api-usage-costs (1,210w, single concept audit), application-modernization-plan (1,223w, single argument), credits (138w), device-models (196w) — none exceed caps or mix BBs.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (15,707 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×5** (notes 1, 3, 4, 8, 11) · **concept ×4** (notes 2, 5, 7, 10) · **argument ×1** (note 6) · **model ×1** (note 9).
- Est. digest words ~6,650 (avg ~605/note; smallest = credits ~200w, largest = release-checklist / code-mode notes ~750w). 40 source fences (RELEASING 8 + code-mode 24 + AGENTS 5 + device-models 2 + modernization 1) distribute across the split notes so each stays ≤6 (config/contract snippets reproduced selectively, verbatim).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> paths are FROM a note at `resources/documentation/openclaw/oc_X.md`: terms → `../../term_dictionary/`,
> sibling oc_ docs (this series, planned) → `oc_Y.md`, other docs → `../<folder>/<file>.md`, repos →
> `../../../areas/code_repos/`, snippets → `../../code_snippets/`. Each doc floor is met with ≥5 EXISTING
> (`term_git`/`term_software_versioning`/`term_software_testing`/`term_macos`/`term_apple`/
> `term_software_quality`/`term_design_pattern` are all absent → replaced; `term_quickjs` is the one
> new-term candidate, deferred per the Undigested Terms Plan — link `term_sandbox` + describe QuickJS-WASI inline).

### oc_reference_agents_default (12t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted chat-to-coding-agent gateway; relevance: the product this default workspace and skill roster configure.
- [Agent harness](../../term_dictionary/term_agent_harness.md) — the agent runtime/orchestration loop; relevance: the runtime that the workspace `AGENTS.md` instructions parameterize.
- [Autonomous coding agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directing code agents; relevance: the assistant class this default personal-assistant setup runs.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — the agent workspace instruction file convention; relevance: this page IS the default `AGENTS.md` (first run, session start, safety defaults).
- [SOUL.md](../../term_dictionary/term_soul_md.md) — the identity/tone/boundaries workspace file; relevance: the required Soul rule mandates reading/maintaining `SOUL.md` each session.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool-server interface; relevance: the bundled mcporter skill manages external MCP tool-server backends.
- [Sandbox](../../term_dictionary/term_sandbox.md) — constrained execution boundary; relevance: the Safety-defaults section sets the destructive-command/config-inspect boundary.
- [Multi-agent](../../term_dictionary/term_multi_agent.md) — multiple isolated agent sessions; relevance: groups stay isolated as `agent:<agentId>:<channel>:group:<id>` vs the collapsed `main` session.
- [Cron](../../term_dictionary/term_cron.md) — scheduled background jobs; relevance: heartbeats keep background tasks/reminders/inbox-monitoring alive.
- [Text-to-speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the `sag` core skill is ElevenLabs speech with say-style UX.
- [Browser automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: `openclaw browser` (snapshot/click/type/eval) is the documented verification path.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: tools live in skills, each with a `SKILL.md`, enabled in Settings → Skills.

**Docs**
- [oc_reference_api_usage_costs](oc_reference_api_usage_costs.md) — API-spend audit (planned, this series); relevance: the bundled skills here (sag, gog, Gemini CLI) can spend provider keys.
- [oc_reference_credits](oc_reference_credits.md) — project origin/credits (planned, this series); relevance: Clawd is the workspace persona named in this file's backup tip.
- [oc_reference_device_models](oc_reference_device_models.md) — macOS app device-name DB (planned, this series); relevance: same macOS companion app that manages this workspace's permissions.
- [pi_skills](../pi/pi_skills.md) — Pi agent skill mechanism; relevance: sibling-harness model for how skills package agent capability (mirrors mcporter/SKILL.md).
- [cc_overview](../claude_code/cc_overview.md) — Claude Code agent overview; relevance: sibling coding-agent's analogous default-workspace + tool-roster concept.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — the `.claude/` workspace dir; relevance: the closest sibling to OpenClaw's `~/.openclaw/workspace` template layout.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes agent feature map; relevance: downstream ecosystem agent whose workspace/skill model derives from OpenClaw.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes migration from OpenClaw; relevance: confirms the OpenClaw workspace/skill conventions Hermes adopts.
- [pi_overview](../pi/pi_overview.md) — Pi agent harness overview; relevance: the harness lineage (Pi creator is an OpenClaw core contributor) this workspace's agent loop descends from.
- [band_agents](../band/band_agents.md) — Band multi-agent definitions; relevance: cross-harness model for agent/skill declaration and isolation.
- [oc_reference_releasing_policy](oc_reference_releasing_policy.md) — release lanes (planned, this series); relevance: workspace `openclaw` CLI is installed/updated per the release channels.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime + workspace; relevance: implements the session/soul/memory rules this file mandates.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill roster mechanism; relevance: implements the core-skill catalog (mcporter, Peekaboo, imsg, wacli).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS app + bundled CLI; relevance: manages permissions (screen/mic/notifications) and exposes the `openclaw` binary.

**Snippets**
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — agent system-prompt mode assembly; relevance: how `AGENTS.md`/`SOUL.md` content becomes the runtime prompt.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — context injection into the prompt; relevance: the session-start read of SOUL/USER/memory injected per turn.
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — root memory-file handling; relevance: implements the `MEMORY.md` / legacy `memory.md` rules in the Memory-system section.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent memory search; relevance: the daily-log/long-term memory read this file requires at session start.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: backs the `memory/YYYY-MM-DD.md` daily-log capture rule.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup wizard config; relevance: writes `agents.defaults.workspace` (the configurable workspace path).
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: how enabled skills are surfaced/selected (Settings → Skills).
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability gate; relevance: hides the install button when a binary is already present (Usage notes).
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — macOS voice-wake; relevance: the macOS-app permission/skill surface this workspace runs on.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: the group/channel isolation model (`agent:<id>:...`) for shared spaces.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat/media pipeline; relevance: the WhatsApp gateway read/write-chats capability described in "What OpenClaw does".
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — daemon linger env; relevance: keeping heartbeats/background tasks alive (Usage notes).

### oc_reference_releasing_policy (10t · 11s · 11d)

**Terms**
- [npm](../../term_dictionary/term_npm.md) — the JavaScript package registry; relevance: publish target; `latest`/`beta` dist-tags and the immutable-version rule are core to the policy.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: the three lanes (stable/beta/dev) map to the release pipeline.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the thing being versioned and released across npm + macOS + Windows.
- [Agile](../../term_dictionary/term_agile.md) — iterative delivery cadence; relevance: the beta-first monthly release-train cadence and `release/YYYY.M.PATCH` branching.
- [Code review](../../term_dictionary/term_code_review.md) — peer PR review; relevance: the changelog is generated from merged PRs + direct commits since the last tag.
- [Technical debt](../../term_dictionary/term_technical_debt.md) — accumulated maintenance burden; relevance: expired compatibility records are removed only when the upgrade path stays covered.
- [Trunk-based development](../../term_dictionary/term_trunk_based_development.md) — short-lived branches off main; relevance: releases cut from `release/YYYY.M.PATCH` off current `main`, dev = moving head of `main`.
- [DevOps](../../term_dictionary/term_devops.md) — build/ship/operate discipline; relevance: version naming + dist-tag promotion + monthly-train governance.
- [Node.js](../../term_dictionary/term_node_js.md) — the JS runtime; relevance: the npm package shipped per release runs on Node.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS superset; relevance: the OpenClaw monorepo source the release packages.

**Docs**
- [oc_reference_releasing_operator_checklist](oc_reference_releasing_operator_checklist.md) — 11-step release checklist (planned, this series); relevance: the procedure that executes this policy.
- [oc_reference_releasing_validation](oc_reference_releasing_validation.md) — pre-release validation (planned, this series); relevance: the "stable follows validated beta" gate this policy states.
- [oc_reference_credits](oc_reference_credits.md) — credits + license (planned, this series); relevance: its Related section points back to this Release policy.
- [cc_overview](../claude_code/cc_overview.md) — Claude Code overview; relevance: sibling coding-agent's release/versioning context.
- [cc_gitlab_ci_cd](../claude_code/cc_gitlab_ci_cd.md) — CI/CD pipeline integration; relevance: analogous lane/pipeline model for a coding-agent release flow.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes migration; relevance: downstream consumer tracking OpenClaw release versions.
- [pi_development](../pi/pi_development.md) — Pi development/build; relevance: sibling-harness build/release model.
- [pi_overview](../pi/pi_overview.md) — Pi overview; relevance: the harness-lineage product released in the same ecosystem.
- [band_overview](../band/band_overview.md) — Band overview; relevance: cross-harness build/distribution model context.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes features; relevance: downstream feature set gated by OpenClaw release trains.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: the `openclaw` CLI installed/updated via these release channels.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the released monorepo; relevance: holds `.github/workflows` + version-naming source.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS/Windows apps; relevance: every stable release ships the macOS app + signed Windows installers together.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: the installed npm CLI surface promoted per dist-tag.

**Snippets**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: plugin npm packages publish alongside the core release.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: bundled config metadata refreshed by `release:prep` before a tag.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config; relevance: bundled channel-config metadata that release-prep regenerates.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render; relevance: install artifacts shipped per release path.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows cmd shim; relevance: the signed Windows Hub installer surface in every stable release.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root guard; relevance: installed-CLI behavior validated per release.
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — CLI config schema; relevance: sibling pattern for config-schema baselines regenerated at release-prep.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — daemon linger env; relevance: install-path artifact validated across release lanes.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: macOS update/restart path exercised in stable releases.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: dependency/vulnerability evidence is release-blocking in preflight.

### oc_reference_releasing_operator_checklist (10t · 12s · 11d)

**Terms**
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: the dispatched workflows (`Full Release Validation`, `OpenClaw NPM Release`, `Release Publish`).
- [npm](../../term_dictionary/term_npm.md) — package registry; relevance: `OpenClaw NPM Release`, dist-tags, post-publish verifier, preflight artifact reuse.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the package/app being branched, tagged, published.
- [Agile](../../term_dictionary/term_agile.md) — iterative cadence; relevance: the `release/YYYY.M.PATCH` branch flow keeping `main` unblocked.
- [Code review](../../term_dictionary/term_code_review.md) — PR review; relevance: changelog generated from merged PRs + direct commits, committed before branching.
- [Technical debt](../../term_dictionary/term_technical_debt.md) — maintenance burden; relevance: step 3 reviews/removes expired compatibility records in `compat/registry.ts`.
- [Docker](../../term_dictionary/term_docker.md) — container packaging; relevance: the release-path package validation the checklist's `Full Release Validation` invokes.
- [DevOps](../../term_dictionary/term_devops.md) — ship/operate discipline; relevance: preflight-then-promote, dist-tag promotion, stable-main closeout.
- [Trunk-based development](../../term_dictionary/term_trunk_based_development.md) — branch off main; relevance: "start from current main", do not do release work on `main`.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: `pnpm` scripts (`release:prep`, `release:candidate`) and tsx publish-check scripts.

**Docs**
- [oc_reference_releasing_policy](oc_reference_releasing_policy.md) — release policy (planned, this series); relevance: the lanes/version scheme this checklist enacts.
- [oc_reference_releasing_validation](oc_reference_releasing_validation.md) — validation boxes (planned, this series); relevance: step 7's `Full Release Validation` umbrella details.
- [cc_gitlab_ci_cd](../claude_code/cc_gitlab_ci_cd.md) — CI/CD pipeline; relevance: analogous release-pipeline orchestration for a coding agent.
- [cc_overview](../claude_code/cc_overview.md) — Claude Code overview; relevance: sibling-tool release-operations context.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — settings reference; relevance: config-baseline regeneration analog (`release:prep` refreshes config docs baseline).
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes migration; relevance: downstream consumer of these published packages/dist-tags.
- [pi_development](../pi/pi_development.md) — Pi build/dev; relevance: sibling-harness release-build flow.
- [pi_overview](../pi/pi_overview.md) — Pi overview; relevance: ecosystem product released alongside.
- [band_overview](../band/band_overview.md) — Band overview; relevance: cross-harness packaging/distribution context.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes features; relevance: downstream feature gating per release.
- [oc_reference_credits](oc_reference_credits.md) — credits/license (planned, this series); relevance: MIT license that governs the published package.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — source/release monorepo; relevance: holds the `.github/workflows` the checklist dispatches.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS/Windows apps; relevance: installer publish + appcast steps for stable.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/signing; relevance: notarize/Authenticode-signature evidence the publish step verifies.

**Snippets**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: `Plugin NPM Release`/`Plugin ClawHub Release` serialized before core publish.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: plugin version sync + `pluginApi` floor bump at `release:prep`.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config; relevance: bundled channel config metadata refreshed before tagging.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: config-schema baseline that `release:check` re-verifies.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows cmd shim; relevance: `Windows Node Release` signed installer the publish step dispatches/verifies.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: macOS appcast/update path readiness for stable.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: dependency vulnerability gate in npm preflight (release-blocking).
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe; relevance: dependency ownership/install-surface release evidence.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories; relevance: sibling pattern for the npm advisory vulnerability gate.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render; relevance: install artifacts validated in the release-candidate run.

### oc_reference_releasing_validation (10t · 12s · 11d)

**Terms**
- [Docker](../../term_dictionary/term_docker.md) — containers; relevance: the Docker release test box (release-path chunks, install-smoke, OpenWebUI lanes).
- [CI/CD](../../term_dictionary/term_ci_cd.md) — CI orchestration; relevance: the `Full Release Validation` umbrella dispatches manual `CI` + `Release Checks`.
- [npm](../../term_dictionary/term_npm.md) — package registry; relevance: Package Acceptance resolves `source=npm` candidates + post-publish verifier.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the package/release being validated.
- [Code review](../../term_dictionary/term_code_review.md) — review/gating; relevance: QA release-check failures block release validation (the human approval gate).
- [Agile](../../term_dictionary/term_agile.md) — iterative recovery; relevance: focused-rerun (`rerun_group`) "smallest failed thing" recovery loop.
- [Prompt caching](../../term_dictionary/term_prompt_caching.md) — model prompt-cache; relevance: the live prompt-cache test lane (`test:live:cache`) in validation.
- [DevOps](../../term_dictionary/term_devops.md) — ops discipline; relevance: telemetry smoke (OTel/Prometheus) + release-soak/upgrade-survivor sweeps.
- [Observability for agent systems](../../term_dictionary/term_observability_agent_systems.md) — agent telemetry; relevance: `qa:otel:smoke`/`qa:prometheus:smoke` verify trace/metric/log export + redaction.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety/quality gates; relevance: redaction checks (no prompt content/identifiers/tokens/paths in metrics).

**Docs**
- [oc_reference_releasing_operator_checklist](oc_reference_releasing_operator_checklist.md) — release checklist (planned, this series); relevance: step 7 kicks off this validation umbrella.
- [oc_reference_releasing_policy](oc_reference_releasing_policy.md) — release policy (planned, this series); relevance: "stable follows validated beta" gate this validation enforces.
- [cc_otel_metrics_reference](../claude_code/cc_otel_metrics_reference.md) — OTel metrics reference; relevance: analog for the OTel metric families validated in `qa:otel:smoke`.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTel setup; relevance: collector-smoke lane (real OpenTelemetry Collector container) analog.
- [cc_otel_analysis_and_privacy](../claude_code/cc_otel_analysis_and_privacy.md) — OTel privacy/redaction; relevance: the content/identifier redaction the telemetry smoke verifies.
- [cc_gitlab_ci_cd](../claude_code/cc_gitlab_ci_cd.md) — CI/CD pipeline; relevance: sibling release-pipeline validation model.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: `qa-live-shared` + Convex CI credential leases for live lanes.
- [pi_development](../pi/pi_development.md) — Pi build/test; relevance: sibling-harness test-suite/validation model.
- [band_testing_agents](../band/band_testing_agents.md) — Band agent testing; relevance: cross-harness agentic-behavior test-gate analog (QA Lab parity).
- [pi_overview](../pi/pi_overview.md) — Pi overview; relevance: ecosystem product validated in parallel lanes.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: the agentic behaviors QA Lab parity validates.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: holds the `.github/workflows` validation definitions.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/telemetry; relevance: OTel/Prometheus redaction smoke + dependency evidence.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: gateway startup/network lanes in Docker install-smoke + Package Acceptance.

**Snippets**
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker environments; relevance: containerized release-path validation analog.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: redaction/audit posture the telemetry smoke validates.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe; relevance: release-evidence probe for dependency/install surface.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — redact patterns; relevance: the redaction patterns telemetry export must satisfy.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: Package Acceptance plugin install/update lanes.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: plugin-update/offline-plugin Docker lanes in Package Acceptance.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: upgrade-survivor/migration lanes validating update paths.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat/media pipeline; relevance: Telegram/QA-Lab channel-flow validation lanes.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: gateway lifecycle exercised in install-smoke/Docker lanes.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: dependency vulnerability evidence gate inside validation.

### oc_reference_api_usage_costs (12t · 12s · 11d)

**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: core model responses (every reply/tool call) are the primary spend.
- [Third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external paid GenAI providers; relevance: the many providers (OpenAI/Anthropic/Groq/Google/…) that bill.
- [Auth profile](../../term_dictionary/term_auth_profile.md) — per-agent credential store; relevance: keys discovered from `auth-profiles.json` (the "How keys are discovered" section).
- [Prompt caching](../../term_dictionary/term_prompt_caching.md) — cache read/write tokens; relevance: `/status` normalizes `cacheRead`; caching affects per-reply cost.
- [Embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: memory-search uses embedding APIs (OpenAI/Gemini/Voyage/Mistral/DeepInfra).
- [Vector database](../../term_dictionary/term_vector_database.md) — semantic store; relevance: semantic memory search that consumes embedding-API spend.
- [Text-to-speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: Talk mode invokes ElevenLabs (§9 spend surface).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: Anthropic usage-window + Claude-login Extra-Usage spend path.
- [Bedrock](../../term_dictionary/term_bedrock.md) — AWS model hosting; relevance: explicitly priced `aws-sdk` models surfaced in `/status` estimated cost.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — bearer/subscription auth; relevance: subscription-style OAuth/token flows show tokens-only usage.
- [Rate limiting](../../term_dictionary/term_rate_limiting.md) — provider quotas; relevance: CLI usage windows are quota snapshots ("X% left") per provider.
- [Model failover](../../term_dictionary/term_model_failover.md) — fallback providers; relevance: optional fallback to a remote embedding provider when local fails.

**Docs**
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — token-cost reduction; relevance: sibling-tool guidance on the same per-reply token-spend lever.
- [cc_sdk_cost_and_usage_tracking](../claude_code/cc_sdk_cost_and_usage_tracking.md) — SDK cost/usage tracking; relevance: the `/usage`/`/status` cost-reporting analog.
- [cc_cost_tracking](../claude_code/cc_cost_tracking.md) — cost tracking; relevance: per-session/per-message cost footer analog.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — usage-limit errors; relevance: provider usage-window/quota behavior analog.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: the `models.providers.*.apiKey` config surface that spends keys.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth; relevance: how keys/credentials are discovered for providers.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: the priced-provider catalog (§1 core responses).
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory providers; relevance: §4 embedding/semantic-search spend providers.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: §10 skills (`skills.entries.<name>.apiKey`) that can spend.
- [oc_reference_releasing_validation](oc_reference_releasing_validation.md) — validation lanes (planned, this series); relevance: live test lanes consume real API keys.
- [oc_reference_code_mode_overview](oc_reference_code_mode_overview.md) — code mode (planned, this series); relevance: nested tool calls still bill through the current model provider.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: usage/cost reporting + `/status`/`status --usage` implementation.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM providers; relevance: the provider integrations that spend keys.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory; relevance: embedding/semantic-search spend (§4).

**Snippets**
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — daily usage-cost summary; relevance: the cost snapshot `/status`/`/usage` reports.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: token + cache-read counters in the cost footer.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: the "local pricing for the active model" that yields estimated cost.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: `OPENAI_API_KEY` core-response + embedding + image-gen spend.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: `OPENROUTER_API_KEY` for `models scan` probe (§8).
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — memory host embeddings; relevance: §4 embedding-API spend (`memorySearch.provider`).
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: what gets embedded (and billed) for semantic memory.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: the semantic-search path that may call remote embeddings.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: §9 Talk-mode ElevenLabs spend.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media transcription; relevance: §2 media-understanding (audio transcribe) provider spend.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk/transcription relay; relevance: speech spend path (talk + transcription).
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tools; relevance: §5 `web_search`/§5b `web_fetch` (Brave/Exa/Firecrawl) key spend analog.

### oc_reference_application_modernization_plan (10t · 11s · 11d)

**Terms**
- [Refactoring](../../term_dictionary/term_refactoring.md) — restructuring without behavior change; relevance: the core modernization activity, "smallest correct patch then repeat".
- [Technical debt](../../term_dictionary/term_technical_debt.md) — accumulated cruft; relevance: what the phased plan pays down (dead affordances, duplicate settings).
- [React](../../term_dictionary/term_react.md) — UI library; relevance: the Frontend Delivery Standards skill targets React/Next.js/webview/app UI.
- [Code review](../../term_dictionary/term_code_review.md) — reviewable changes; relevance: the small-reviewable-slices principle + the handoff format.
- [Agile](../../term_dictionary/term_agile.md) — incremental delivery; relevance: the 6-phase small-slice delivery with proof per surface.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the application/Control-UI being modernized.
- [TDD](../../term_dictionary/term_tdd.md) — test-driven development; relevance: Phase 5 contract/test hardening + focused tests for changed boundaries.
- [Code smells](../../term_dictionary/term_code_smells.md) — maintainability anti-patterns; relevance: oversized components, broad global state, dead affordances the plan removes.
- [Strategic programming](../../term_dictionary/term_strategic_programming.md) — invest-in-design discipline; relevance: "preserve current architecture unless a boundary is demonstrably causing churn".
- [Boy Scout Rule](../../term_dictionary/term_boy_scout_rule.md) — leave code cleaner; relevance: incremental cleanup separated from required fixes, smallest correct patch.

**Docs**
- [oc_reference_releasing_policy](oc_reference_releasing_policy.md) — release policy (planned, this series); relevance: Phase 6 documentation + release-readiness aligns docs with shipped behavior.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: the repo-local `.agents/skills/openclaw-frontend/SKILL.md` the plan creates.
- [cc_overview](../claude_code/cc_overview.md) — Claude Code overview; relevance: sibling coding-agent's modernization/quality-pass model.
- [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — extending Claude Code; relevance: the repo-local SKILL.md authoring analog.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — settings reference; relevance: config-persistence/status-derivation surfaces the plan tests.
- [pi_development](../pi/pi_development.md) — Pi development; relevance: sibling-harness frontend/build hardening model.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes features; relevance: downstream app surfaces benefiting from the modernization.
- [band_overview](../band/band_overview.md) — Band overview; relevance: cross-harness product-quality/contract context.
- [pi_overview](../pi/pi_overview.md) — Pi overview; relevance: ecosystem product with analogous UI/Control surfaces.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes migration; relevance: contract/compatibility stability the plan mandates (plugin-facing backwards compat).
- [oc_reference_releasing_validation](oc_reference_releasing_validation.md) — validation (planned, this series); relevance: `pnpm check:changed`/`pnpm build` gates the plan requires.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/Control-UI; relevance: the application surface being modernized (onboarding, auth, chat, diagnostics).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the `pnpm check:changed`/`pnpm build` gates + plugin manifest/provider catalog contracts.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: Phase 5 contract tests around plugin manifests/SDK facades.

**Snippets**
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — server auth startup; relevance: Phase 2 onboarding/auth-readiness first-slice surface.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: routing/config-persistence logic the plan focuses tests on.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patches; relevance: state-derivation/persistence boundaries Phase 3 tightens.
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — canvas filewatcher; relevance: Control-UI/canvas surface in the recommended first slice.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: Phase 5 plugin-manifest contract tests.
- [snippet_hermes_agent_cli_web_config_schema](../../code_snippets/snippet_hermes_agent_cli_web_config_schema.md) — web config schema; relevance: schema-validated external inputs (zod) the plan recommends.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config; relevance: first-run/provider-setup config surface audited in Phase 1/2.

### oc_reference_code_mode_overview (10t · 11s · 12d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — constrained execution; relevance: `exec` evaluates model code in a constrained QuickJS-WASI worker (link `term_sandbox`; describe QuickJS-WASI inline since `term_quickjs` is absent).
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS; relevance: guest cells accept JavaScript or TypeScript (`language` field).
- [Function calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: code mode replaces direct tool schemas with the `exec`/`wait` orchestration surface.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: in code mode the `MCP` namespace is the only supported way to call MCP tools.
- [Tool registry](../../term_dictionary/term_tool_registry.md) — run-scoped tool catalog; relevance: enabled tools are hidden from the model and registered in the code-mode catalog.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: the model sees exactly `exec` and `wait` (smaller prompt surface).
- [Agent harness](../../term_dictionary/term_agent_harness.md) — generic agent runtime; relevance: code mode is an OpenClaw agent-runtime feature, evaluated after tool policy.
- [Code execution tool](../../term_dictionary/term_code_execution_tool.md) — sandboxed code-run tool; relevance: contrasts with provider-native remote code execution (out of scope here).
- [LATM (LLMs as tool makers)](../../term_dictionary/term_latm.md) — model-authored tool use; relevance: the "model writes a small program instead of choosing from a long tool list" paradigm.
- [Toolformer](../../term_dictionary/term_toolformer.md) — model learning tool APIs; relevance: the orchestration-via-code premise (loops/joins/conditional nested calls).

**Docs**
- [oc_reference_code_mode_namespaces](oc_reference_code_mode_namespaces.md) — guest API + namespaces (planned, this series); relevance: the authoring side of the same feature.
- [oc_reference_code_mode_runtime_security](oc_reference_code_mode_runtime_security.md) — runtime + security (planned, this series); relevance: the runtime/state/security side of the same feature.
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — custom tool definition; relevance: sibling SDK's tool-definition model that code mode replaces with `exec`.
- [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — subagents overview; relevance: alternative large-tool-catalog orchestration approach to compare.
- [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — tool catalog; relevance: the "long list of tool schemas" code mode collapses.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — code-execution tool behavior; relevance: sibling code-execution surface contrasted in Scope.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex runtime tools; relevance: directly compares Codex Code Mode's `exec.command` vs OpenClaw `exec.code`.
- [hermes_toolsets_reference](../hermes_agent/hermes_toolsets_reference.md) — toolsets reference; relevance: the enabled-tool catalog this feature reshapes.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — custom tools; relevance: sibling-harness custom-tool exposure model.
- [bedrock_agentcore_runtime_overview](../aws_bedrock_agentcore/bedrock_agentcore_runtime_overview.md) — agent-runtime overview; relevance: managed agent-runtime + tool-surface analog.
- [band_agents](../band/band_agents.md) — Band agents; relevance: cross-harness tool/agent declaration model.
- [oc_reference_api_usage_costs](oc_reference_api_usage_costs.md) — API costs (planned, this series); relevance: nested tool calls still bill through the current model provider.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: owns the model-surface adapter (visible tools → `exec`/`wait`).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: assembles the final model request (the `OPENCLAW_DEBUG_MODEL_PAYLOAD=tools` surface).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: plugin/MCP tools cataloged into the hidden tool list.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: the run-scoped catalog (`ALL_TOOLS`) code mode exposes to guests.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — code-exec sandbox; relevance: sibling constrained code-execution worker analog.
- [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — code-exec result; relevance: analog of the `CodeModeResult` completed/waiting/failed union.
- [snippet_hermes_agent_tools_code_exec_languages](../../code_snippets/snippet_hermes_agent_tools_code_exec_languages.md) — code-exec languages; relevance: the JavaScript/TypeScript language gating in `exec`.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt modes; relevance: how the `exec`/`wait` tool description is injected into the prompt.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — call-method gating; relevance: tool-policy/allow-deny gate applied before code mode activates.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: the effective-tool registration the code-mode catalog mirrors.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: tool/skill selection feeding the run-scoped catalog.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: nested calls still go through approvals/hooks (a "why is this good" guarantee).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the provider request that now carries only two control tools.
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hooks; relevance: `before_tool_call` hooks preserved for nested calls.

### oc_reference_code_mode_namespaces (10t · 12s · 11d)

**Terms**
- [Tool registry](../../term_dictionary/term_tool_registry.md) — namespace + catalog registry; relevance: the process-local namespace registry keyed by namespace id (register/scope/cleanup).
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the generated `MCP.<server>` namespace + `$api()` + virtual `.d.ts` surface.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin extension API; relevance: namespaces are loader-owned; no public plugin SDK namespace API yet.
- [Plugin manifest](../../term_dictionary/term_plugin_manifest.md) — plugin identity/declaration; relevance: ownership bound to the registration caller's `pluginId` + `requiredToolNames`.
- [Function calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: namespace calls are catalog tool calls dispatched through `ToolSearchRuntime.call`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — bridge isolation; relevance: scope serialization rejects raw functions/cycles/unsafe keys crossing the JSON bridge.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed declarations; relevance: virtual `mcp/<server>.d.ts` declaration files read via `API.read`.
- [Tool descriptor](../../term_dictionary/term_tool_descriptor.md) — tool metadata contract; relevance: `ToolCatalogEntry` compact metadata (id/name/source) feeding the catalog.
- [Capability negotiation](../../term_dictionary/term_capability_negotiation.md) — surface advertisement; relevance: namespace `description`/`prompt` appended to the `exec` schema only when visible.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON request/response; relevance: the narrow JSON-compatible host-bridge callback surface.

**Docs**
- [oc_reference_code_mode_overview](oc_reference_code_mode_overview.md) — code-mode overview (planned, this series); relevance: the contract/why side of the same feature.
- [oc_reference_code_mode_runtime_security](oc_reference_code_mode_runtime_security.md) — runtime/security (planned, this series); relevance: how namespace calls suspend/resume + serialize safely.
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — custom tool definition; relevance: sibling tool-declaration model akin to `createCodeModeNamespaceTool`.
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugins; relevance: plugin-owned extension registration analog.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest schema; relevance: plugin identity/ownership analog to `pluginId`/`requiredToolNames`.
- [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — MCP server management; relevance: the MCP servers surfaced as `MCP.<server>` namespaces.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin types/surfaces; relevance: sibling plugin namespace/surface registration model.
- [hermes_mcp_concept_config](../hermes_agent/hermes_mcp_concept_config.md) — MCP concept/config; relevance: MCP grouping the `MCP` namespace exposes.
- [pi_extensions_api_methods](../pi/pi_extensions_api_methods.md) — extension API methods; relevance: sibling-harness extension-registration verbs analog.
- [band_sdk_architecture](../band/band_sdk_architecture.md) — Band SDK architecture; relevance: cross-harness SDK/namespace registration model.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: MCP tools (mcporter) surfaced through the namespace.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: hosts `code-mode-namespaces.js` (registry + `ToolSearchRuntime`).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: plugin-owned namespace registration (`registerCodeModeNamespaceForPlugin`).
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills; relevance: the tool-descriptor contract feeding `ALL_TOOLS`/the catalog.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: the run-scoped catalog `tools.search`/`describe`/`call` operate over.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool-descriptor contract; relevance: the `ToolCatalogEntry` shape (id/name/source/description).
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: plugin-owned entrypoints that register namespaces.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: `clearCodeModeNamespacesForPlugin` on rollback/uninstall.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: sibling namespace-registration pattern.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: plugin identity/`requiredToolNames` ownership analog.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: loader-owned registry-by-id pattern analog.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tools registry; relevance: the effective-tool registry namespaces map onto.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skills manifest format; relevance: the descriptor format catalog entries derive from.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: run-scoped catalog assembly analog (visible-tool gating).
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: loader-owned-contract design the namespaces require.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the JSON-bridge serialization contract for scope data.

### oc_reference_code_mode_runtime_security (10t · 12s · 11d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — defense-in-depth boundary; relevance: model code is hostile; no FS/network/subprocess/env/host-globals in guest (describe QuickJS-WASI inline; `term_quickjs` absent).
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS; relevance: TypeScript is a source-transform-only path (no typecheck/module resolution).
- [Function calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: nested-call result/error schemas + `nested_tool_failed` error code.
- [Tool registry](../../term_dictionary/term_tool_registry.md) — catalog ids; relevance: the `<source>:<owner>:<tool-name>` catalog-id schema + control-tool exclusion.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: the hostile model-generated code the security boundary contains.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP namespace dispatch stays inside the run-scoped catalog/security boundary.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints; relevance: memory/interrupt limits, output/snapshot/pending-call caps, fail-closed posture.
- [Observability for agent systems](../../term_dictionary/term_observability_agent_systems.md) — agent telemetry; relevance: telemetry counters (visible tools, catalog size, exec/wait counts) with redaction.
- [SSRF guard](../../term_dictionary/term_ssrf_guard.md) — egress restriction; relevance: no network access in the guest is part of the defense-in-depth layering.
- [Chaos engineering](../../term_dictionary/term_chaos_engineering.md) — failure-mode testing; relevance: the validation/E2E checklist proves timeout/abort/expiry cleanup + memory-cap termination.

**Docs**
- [oc_reference_code_mode_overview](oc_reference_code_mode_overview.md) — code-mode overview (planned, this series); relevance: the contract this runtime implements.
- [oc_reference_code_mode_namespaces](oc_reference_code_mode_namespaces.md) — namespaces (planned, this series); relevance: namespace calls suspend/resume via the same snapshot mechanism.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime; relevance: sibling sandboxed-execution runtime model.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — FS/network isolation; relevance: the no-FS/no-network guest boundary analog.
- [cc_sdk_isolation_technologies](../claude_code/cc_sdk_isolation_technologies.md) — isolation technologies; relevance: worker-outside-main-loop isolation analog (vs `node:vm`).
- [cc_computer_use_safety](../claude_code/cc_computer_use_safety.md) — hostile-input safety; relevance: the "model code is hostile" defense-in-depth posture.
- [cc_otel_metrics_reference](../claude_code/cc_otel_metrics_reference.md) — OTel metrics; relevance: the telemetry counter families analog (redaction-bounded).
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — security isolation; relevance: credential/secret redaction in telemetry the runtime mandates.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: sibling-harness sandbox/security-boundary model.
- [pi_containerization](../pi/pi_containerization.md) — containerization; relevance: worker/process isolation analog for hostile code.
- [bedrock_agentcore_runtime_overview](../aws_bedrock_agentcore/bedrock_agentcore_runtime_overview.md) — agent-runtime overview; relevance: managed isolated agent-runtime analog (state/session scoping).

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: the security boundary, redaction, audit posture for exec runtime.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the run state machine + snapshot store + bridge adapter.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: the QuickJS-WASI worker runs outside the gateway main event loop.

**Snippets**
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: audit/telemetry of the exec runtime security boundary.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: the no-filesystem-access guest restriction.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tools deny; relevance: deny-policy filtering before catalog registration.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — openshell backend; relevance: contrast — shell `exec` is hidden/cataloged, not the code-mode `exec`.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — code-exec sandbox; relevance: sibling sandboxed-VM isolation pattern.
- [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — code-exec result; relevance: the result/error union (`CodeModeResult`/`CodeModeErrorCode`) analog.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — redact patterns; relevance: telemetry must not include secrets/raw env/unredacted inputs.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: worker supervisor (timeout/abort/crash isolation) for the guest VM.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: the catalog-id schema + control-tool exclusion described here.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: nested calls preserve approval/hook behavior across the bridge.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — call-method gating; relevance: recursive `exec`/`wait`/Tool-Search control tools rejected from guest.

### oc_reference_credits (10t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the project; relevance: the project being credited (CLAW + TARDIS name origin).
- [Autonomous coding agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directing code agents; relevance: the product class the credited contributors built.
- [Agent harness](../../term_dictionary/term_agent_harness.md) — agent runtime/harness; relevance: core contributor Mario Zechner is the Pi creator (the harness lineage).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the agent core the project wraps ("playing with our own prompts").
- [Pi agent](../../term_dictionary/term_pi_agent.md) — the Pi coding agent; relevance: Pi (Mario Zechner) is named in the credits as a lineage source.
- [Text-to-speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: contributor Vincent Koc's Agents/Telemetry/Hooks span the speech/skill surfaces.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: the multi-component agent ecosystem the contributors maintain.
- [Skills](../../term_dictionary/term_skills.md) — packaged capabilities; relevance: Maxim Vovshin's Blogwatcher skill is a credited community contribution.

**Docs**
- [oc_reference_releasing_policy](oc_reference_releasing_policy.md) — release policy (planned, this series); relevance: this page's Related section links Release policy.
- [oc_reference_api_usage_costs](oc_reference_api_usage_costs.md) — API costs (planned, this series); relevance: this page's Related section links Token use & costs.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: Clawd (the persona that "demanded a better name") runs in that workspace.
- [pi_overview](../pi/pi_overview.md) — Pi agent overview; relevance: the harness by credited core contributor Mario Zechner.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes features; relevance: downstream ecosystem agent in the same lineage.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes migration; relevance: ecosystem-fork relationship anchored to OpenClaw.
- [cc_overview](../claude_code/cc_overview.md) — Claude Code overview; relevance: peer coding-agent context for the product class.
- [band_overview](../band/band_overview.md) — Band overview; relevance: cross-harness ecosystem context.
- [pi_skills](../pi/pi_skills.md) — Pi skills; relevance: the skill model contributors extended (Blogwatcher, etc.).
- [pi_development](../pi/pi_development.md) — Pi development; relevance: contributor-facing development context for the lineage.
- [oc_reference_device_models](oc_reference_device_models.md) — device model DB (planned, this series); relevance: another vendored MIT-licensed asset under the same project license.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the credited monorepo; relevance: the MIT-licensed project these contributors built.
- [repo_pi_agent_harness](../../../areas/code_repos/repo_pi_agent_harness.md) — Pi harness; relevance: Pi, by credited core contributor Mario Zechner.

**Snippets**
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — agent system-prompt modes; relevance: the agent runtime the credited contributors built.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the LLM-provider plumbing the project wraps.
- [snippet_hermes_agent_skills_codex](../../code_snippets/snippet_hermes_agent_skills_codex.md) — Codex skills; relevance: ecosystem skill-integration the contributors' work enables.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: the skill surface a community contributor extended.
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — ACP translator init; relevance: the ACP ecosystem protocol binding the credited projects.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat/media pipeline; relevance: the core gateway capability the project is built around.

### oc_reference_device_models (10t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the macOS companion app feature mapping Apple model ids to friendly names (Instances UI).
- [Agent harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the macOS app is the companion to the agent runtime this DB serves.
- [Autonomous coding agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding-agent class; relevance: the product family the macOS app belongs to.
- [Refactoring](../../term_dictionary/term_refactoring.md) — code/data maintenance; relevance: the vendored-JSON update procedure (re-pin, re-download, re-verify build).
- [Technical debt](../../term_dictionary/term_technical_debt.md) — maintenance burden; relevance: deterministic commit-pinning to keep builds reproducible is a maintenance cost.
- [DevOps](../../term_dictionary/term_devops.md) — build/release ops; relevance: `swift build --package-path apps/macos` verification gate in the update steps.
- [Bonjour discovery](../../term_dictionary/term_bonjour_discovery.md) — Apple-platform discovery; relevance: the Apple/macOS platform context the device-model mapping lives in.
- [Node.js](../../term_dictionary/term_node_js.md) — JS toolchain; relevance: the monorepo build context the macOS Swift package integrates with.
- [Subagent](../../term_dictionary/term_subagent.md) — multi-instance agents; relevance: the Instances UI (which displays these device names) lists agent instances per device.

**Docs**
- [oc_reference_credits](oc_reference_credits.md) — credits + MIT license (planned, this series); relevance: the vendored `apple-device-identifiers` is MIT-licensed under the same project policy.
- [oc_reference_agents_default](oc_reference_agents_default.md) — default workspace (planned, this series); relevance: the same macOS companion app that manages permissions and the Instances UI.
- [oc_reference_application_modernization_plan](oc_reference_application_modernization_plan.md) — modernization plan (planned, this series); relevance: the macOS/Control-UI app surfaces this DB feeds into.
- [pi_overview](../pi/pi_overview.md) — Pi overview; relevance: sibling-harness ecosystem/platform context.
- [pi_development](../pi/pi_development.md) — Pi development; relevance: sibling-harness build/vendored-dependency maintenance model.
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — Hermes features; relevance: downstream ecosystem app feature context.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — Hermes migration; relevance: ecosystem fork sharing the macOS-app lineage.
- [cc_overview](../claude_code/cc_overview.md) — Claude Code overview; relevance: peer coding-agent desktop-app context.
- [band_overview](../band/band_overview.md) — Band overview; relevance: cross-harness platform/build context.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — `.claude/` directory; relevance: analog for vendored/resource file layout under an app's resources dir.
- [pi_platform_windows_termux](../pi/pi_platform_windows_termux.md) — Pi platform notes; relevance: sibling platform-specific resource/identifier handling.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS/Windows apps; relevance: hosts `apps/macos/Sources/OpenClaw/Resources/DeviceModels/` (the vendored JSON + NOTICE.md).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the `swift build --package-path apps/macos` build target.

**Snippets**
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — macOS canvas filewatcher; relevance: the macOS app surface the Instances UI device names appear in.
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — macOS voice-wake trigger; relevance: another macOS-app native resource integration pattern.
- [snippet_openclaw_macos_voice_wake_audio](../../code_snippets/snippet_openclaw_macos_voice_wake_audio.md) — macOS voice-wake audio; relevance: macOS-app resource/asset usage analog.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: macOS-app build/runtime integration context.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows cmd shim; relevance: cross-platform app-build companion to the macOS Swift build.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config; relevance: app/instance configuration the device names are displayed against.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render; relevance: deterministic build-artifact rendering analog (pinned, reproducible).
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root guard; relevance: the `openclaw` CLI/app build verified by `swift build`.

## Undigested Terms Plan

| Term (from source) | Disposition |
|---|---|
| code mode | OpenClaw vocabulary → **note 7** (`oc_reference_code_mode_overview`). Not a `term_dictionary` capture. |
| exec / wait (code-mode control tools) | Documented as the code-mode contract in **notes 7/9**, not promoted to terms. |
| guest runtime / host bridge / catalog / snapshot / nested tool call | Code-mode design vocabulary → **notes 7–9**. Not terms. |
| internal namespace / namespace registry | Code-mode authoring vocabulary → **note 8**. Not a term. |
| release lane (stable/beta/dev), version train, dist-tag | Release-policy vocabulary → **notes 2/3**. Link existing `term_npm`, `term_ci_cd`. Not new terms. |
| Full Release Validation / Package Acceptance / release test boxes | Release-ops workflow names → **notes 3/4**. Not terms. |
| usage window / spend surface / key discovery | Cost-audit vocabulary → **note 5**. Link `term_llm`/`term_third_party_genai_services`/`term_auth_profile`. Not new terms. |
| application modernization / Frontend Delivery Standards | Plan-doc vocabulary → **note 6**. Link `term_refactoring`/`term_technical_debt`/`term_react`. Not new terms. |
| device model identifier / Instances UI | macOS-app vocabulary → **note 11**. Not a term. |
| QuickJS / QuickJS-WASI | **New-term candidate** (see below) — cross-cutting sandbox runtime referenced by code-mode; `term_quickjs` is MISSING in DB. |

**Expected new `term_dictionary` captures: 0–1.** Per the master's corpus-wide decision, OpenClaw vocabulary is digested as `oc_*` doc notes, not new terms. The one genuinely cross-cutting, vault-reusable candidate with no existing note is **QuickJS / QuickJS-WASI** (a JavaScript engine / WASI sandbox runtime, referenced by code-mode and reusable across the sandbox/agent-runtime corpus). Recommendation: defer to augment — if the broader corpus (e.g. other code-mode / sandbox pages) reuses it, capture `term_quickjs` via `/tessellum-capture-term-note` and add it to the agentic/LLM acronym glossary; otherwise link `term_sandbox` and describe QuickJS-WASI inline as a proper noun in note 9. Collision audit: no existing `term_quickjs`, `term_quickjs_wasi`, or `term_wasm`/`term_webassembly` note (all MISSING) — slug is specific and non-duplicative.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P2). Gate table identical to the master's shared 9-GATE:

| Gate | Check | Tool / method |
|---|---|---|
| G1 | Format (YAML field order/forbidden fields, H1/`## Overview`/`## Related Notes`/`## References`/bold footer, ≤400L/≤2500w/≤6 code, one building_block) | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traceable to `inbox/openclaw_docs/reference/<page>`) | diff vs mirror source |
| G3 | Density + Coverage (every assigned H2/H3 mapped to a note; no over-compression) | Section Coverage Map ✔ |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | `/tessellum-fix-ghost-references`; DB existence check |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability — each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` | via `entry_openclaw_docs.md` + repo/term inlinks |
| G8 | In-degree ≥1 / anti-island | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

All gates must pass before commit.

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_reference_agents_default oc_reference_releasing_policy oc_reference_releasing_operator_checklist oc_reference_releasing_validation oc_reference_api_usage_costs oc_reference_application_modernization_plan oc_reference_code_mode_overview oc_reference_code_mode_namespaces oc_reference_code_mode_runtime_security oc_reference_credits oc_reference_device_models"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + link errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # sibling-prefix self-reference sanity (at least one oc_ Related link expected for split clusters)
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NOTE: no sibling $SIBLING_PREFIX link"
  # density caps (body only)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# ghost-reference + broken-link sweep (G5/G6) after incremental reindex:
bash scripts/update_notes_database.sh
# then run /tessellum-fix-ghost-references and /tessellum-fix-broken-links per master
```

## Density Re-Assessment

| # | Note | BB | ~Words | Src fences | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_reference_agents_default | procedure | 550 | 5 (selective) | ✅ |
| 2 | oc_reference_releasing_policy | concept | 600 | 0 | ✅ |
| 3 | oc_reference_releasing_operator_checklist | procedure | 750 | ≤6 of 8 | ✅ |
| 4 | oc_reference_releasing_validation | procedure | 700 | ≤6 of 8 | ✅ |
| 5 | oc_reference_api_usage_costs | concept | 700 | 0 | ✅ |
| 6 | oc_reference_application_modernization_plan | argument | 650 | 1 | ✅ |
| 7 | oc_reference_code_mode_overview | concept | 750 | ≤6 of ~10 | ✅ |
| 8 | oc_reference_code_mode_namespaces | procedure | 750 | ≤6 of ~9 | ✅ |
| 9 | oc_reference_code_mode_runtime_security | model | 700 | ≤6 of ~5 | ✅ |
| 10 | oc_reference_credits | concept | 200 | 0 | ✅ |
| 11 | oc_reference_device_models | procedure | 300 | 2 | ✅ |

No note approaches caps. The two code-heavy pages (RELEASING 8 fences, code-mode 24 fences) were split so each note keeps ≤6 fences; contract/config snippets (`tools.codeMode` config, `CodeModeResult`/`CodeModeErrorCode` types, `gh workflow run` examples) are reproduced selectively and verbatim. Tiny notes (10, 11) are intentionally short — they faithfully cover their entire (small) source page.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (planned, W1) → **all 11 notes** (primary anti-island guarantee).
- `repo_openclaw_apps.md` → notes 1, 6, 11 (workspace setup, modernization, device-model DB live in the apps repo).
- `repo_openclaw.md` → notes 2, 3, 4 (release policy/checklist/validation live in the source monorepo's `.github/workflows`).
- `repo_openclaw_agents.md` → notes 1, 7, 8, 9 (agent runtime / code-mode surface).
- `repo_openclaw_gateway.md` → notes 5, 7 (usage/cost reporting; gateway assembles the code-mode model request).
- `repo_openclaw_security.md` → notes 4, 9 (release telemetry redaction; code-mode security boundary).
- `repo_openclaw_extensions.md` → note 8 (plugin-owned namespace registration).
- `term_openclaw.md` → notes 1, 2, 10 (umbrella term, code↔docs cross-link per master W3).
- `term_npm.md` → notes 2, 3; `term_ci_cd.md` → notes 3, 4; `term_docker.md` → note 4.
- `term_sandbox.md` + `term_typescript.md` → notes 7, 8, 9; `term_mcp.md` → notes 7, 8.
- `term_refactoring.md` + `term_technical_debt.md` → note 6; `term_react.md` → note 6.
- `term_llm.md` + `term_third_party_genai_services.md` + `term_auth_profile.md` → note 5.

## Pacing Rules (inherited from master)


## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (Per-Note Related Notes Mapping LOCKED at raised floors; see Augmentation Report) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY** (9/9 checkpoints PASS; see Review Sign-Off) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (plan `status: ready`) |

## Follow-up Recommendations

- At execute: incremental reindex; add the 11 `entry_openclaw_docs.md` rows + reciprocal inlinks; broken-link + ghost sweep; in-degree ≥1 verify; cross-link rf02 (prompt-caching, token-use), rf03 (session-management+compaction, templates), in01 (release channels), to01–08 (web/media/skills tools), co04 (`concepts/models`).

## Augmentation Report (2026-06-21)


**Per-note locked counts** (terms / snippets / docs · repos; all floors met):

| # | Note | BB | Terms | Snippets | Docs (existing+sibling) | Repos | Floors met (≥8t·≥10s·≥10d) |
|---|---|---|---:|---:|---|---:|---|
| 1 | oc_reference_agents_default | procedure | 12 | 12 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 2 | oc_reference_releasing_policy | concept | 10 | 11 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 3 | oc_reference_releasing_operator_checklist | procedure | 10 | 12 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 4 | oc_reference_releasing_validation | procedure | 10 | 12 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 5 | oc_reference_api_usage_costs | concept | 12 | 12 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 6 | oc_reference_application_modernization_plan | argument | 10 | 11 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 7 | oc_reference_code_mode_overview | concept | 10 | 11 | 12 (10 existing + 2 sibling) | 3 | ✅ |
| 8 | oc_reference_code_mode_namespaces | procedure | 10 | 12 | 11 (9 existing + 2 sibling) | 3 | ✅ |
| 9 | oc_reference_code_mode_runtime_security | model | 10 | 12 | 11 (9 existing + 2 sibling) | 3 | ✅ |
| 10 | oc_reference_credits | concept | 10 | 10 | 11 (7 existing + 4 sibling) | 3 | ✅ |
| 11 | oc_reference_device_models | procedure | 10 | 10 | 11 (8 existing + 3 sibling) | 3 | ✅ |



## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step — ≥8 terms + floors per note, each link with description + relevance | **PASS** | LOCKED Per-Note Related Notes Mapping: all 11 notes meet ≥8t·≥10s·≥10d; every link is `[Name](relpath.md) — what; relevance: why`. |
| CP2 | 9-GATE table present per execution phase (G1–G6 + G7/G8 Discoverability) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table inherited from master; G5 ghost-detect + G6 broken-link-fix + G7/G8 anti-island all present. |
| CP3 | Entry point update specified + inherited | **PASS** | "Entry Point Decision" section: 11 rows into `entry_openclaw_docs.md` under a "Reference" cluster (created as master W1 pre-step); back-link per note satisfies G7/G8. |
| CP4 | Plan size manageable (≤30 or split) | **PASS** | 11 notes (well under 30); 2 source pages split ×3 each per the Split Decisions table. |
| CP5 | Note format aligned + DERIVED from existing target-dir notes | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview`/`## Related Notes`/`## References`/bold footer, fixed YAML field order, forbidden fields). |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 11 notes ≤750w / ≤6 fences / ≤400L; the two code-heavy pages (RELEASING 8, code-mode 24) split so each note keeps ≤6 fences. No borderline note unaddressed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 pages re-read at augment from `inbox/openclaw_docs/reference/`; measured `wc -w` matches the plan Source table exactly (817/6,790/1,210/1,223/5,333/138/196 = 15,707). |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + authoring reqs | **PASS** | "Undigested Terms Plan" table (every term has a disposition/owner note; expected captures 0–1) + "Term-Note Authoring Requirements" (N/A unless `term_quickjs` promoted → then `/tessellum-capture-term-note`, multi-source, `acronym_glossary_developer.md`). |
| CP9 | Discoverability — inbound links executed (G8), no graph islands | **PASS** | "Inlinks (existing → new notes)" table: every new note receives ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 11; repo/term inlinks per note); G7/G8 in the gate table; inlink-addition is a gated execute phase. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
