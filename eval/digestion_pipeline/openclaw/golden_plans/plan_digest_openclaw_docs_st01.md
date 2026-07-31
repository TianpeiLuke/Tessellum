---
title: "Sub-Plan st01 — OpenClaw Docs: Start / Getting Started (bootstrapping, docs-directory, getting-started, hubs, lore, onboarding, onboarding-overview)"
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["start/bootstrapping", "start/docs-directory", "start/getting-started", "start/hubs", "start/lore", "start/onboarding", "start/onboarding-overview"]
---

# Sub-Plan st01: Start

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` → mirrored body → `## Related Notes` → `## References` → bold footer), dedup (three-way across `term_dictionary/` + `documentation/` + `repo_openclaw*`), undigested-terms policy (OpenClaw vocab → `oc_` doc notes; link existing terms only), 9-GATE validation, cross-refs, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 "Start / Getting Started" pages — the day-0 entry surface of the OpenClaw docs: the first-run agent **bootstrapping** ritual, the curated **docs-directory** index, the **getting-started** quickstart (install → onboard → verify → dashboard → first message), the complete **hubs** doc map, the **lore** backstory/tone page, and the two onboarding pages (**onboarding** = macOS-app first-run flow; **onboarding-overview** = CLI-vs-app path chooser). Priority **P1 (Phase A)** — this cluster defines the install/onboarding/workspace vocabulary the rest of the corpus references, and is the natural first landing for a reader. The code-side counterparts (`repo_openclaw_cli_wizard`, `repo_openclaw_apps`, `repo_openclaw_gateway`, `repo_openclaw_agents`) are LINKED, not recreated. The `hubs` and `docs-directory` pages are navigation indexes — captured as concise concept notes (curated link inventory + when-to-use), NOT exhaustive link dumps, with downstream targets deferred to their home sub-plans.

**Source**: OpenClaw docs, 7 pages, **3,421 measured words** (excluding YAML frontmatter the page word count is approximate; `wc -w` over full files = 3,421). **Planned: 7 notes** (1 note per page; no splits — every page is single-BB and ≤1,200 words).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| bootstrapping | start/bootstrapping | 256 | 0 | 4 | 0 | concept |
| docs-directory | start/docs-directory | 197 | 0 | 5 | 0 | concept (navigation index) |
| getting-started | start/getting-started | 509 | 3 | 4 | 0 | procedure |
| hubs | start/hubs | 508 | 0 | 16 | 0 | concept (navigation index) |
| lore | start/lore | 1,133 | 2 | 11 | 8 | concept (narrative/brand) |
| onboarding | start/onboarding | 469 | 0 | 1 | 0 | procedure |
| onboarding-overview | start/onboarding-overview | 349 | 1 | 6 | 0 | procedure |

Notes on measurement: `Code` = fenced-block count = `grep -c '^```' / 2` (bootstrapping/docs-directory/hubs/onboarding = 0; getting-started = 6 fences → 3 blocks; lore = 4 fences → 2 blocks; onboarding-overview = 2 fences → 1 block). `onboarding.md`'s single `## Related` H2 reflects its body being authored as MDX `<Steps>/<Step>` components (7 step titles, not markdown headings); those 7 steps are the substantive sections and are mapped individually in the Section Coverage Map. `getting-started.md`'s `## Quick setup` likewise wraps 5 MDX `<Step>` titles. H2/H3 counts above are literal markdown-heading counts; MDX step/tab/card titles are tracked in the coverage map.

## Content Strategy

- **Prioritize**: the `getting-started` quickstart (every new install follows it: install script → `openclaw onboard --install-daemon` → `openclaw gateway status` → `openclaw dashboard` → first message) and the two onboarding pages (path selection + what onboarding configures: provider/auth, workspace, gateway, channels, daemon). These are the load-bearing operational notes.
- **Split**: NONE. Every page is single-BB and well under the 2,500-word / 6-code-block caps (largest is `lore` at 1,133w / 2 code blocks). One page → one note.
- **Link-out (defer to home sub-plan, do NOT inline)**: the dozens of downstream targets the index pages (`docs-directory`, `hubs`) and quickstart point to — `gateway/configuration` (gw02), `concepts/*` (co01–07), `channels/*` (ch01–06), `tools/*` (to01–08), `install/*` (in01–05), `web/*` (wb01), `platforms/*` (pf01–04), `reference/templates/*` (rf03–05), `cli/*` (cl01–09), `automation/cron-jobs` (au01). The index notes capture the *curated grouping* and *when to use each cluster*, with cross-links to sibling `oc_*` notes once those land; the full target enumeration lives in each target's sub-plan.
- **Link existing terms, never redefine**: `term_openclaw`, `term_messaging_gateway`, `term_agents_md`, `term_oauth_token`, `term_authentication`, `term_node_js`, `term_sandbox`, `term_claude`, `term_llm`, `term_subagent`, `term_skills`, `term_multi_agent`, `term_cron` etc. are linked from the relevant note's Related Notes, not inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_start_bootstrapping.md` | concept | start/bootstrapping.md: What bootstrapping does, Skipping bootstrapping, Where it runs, Related docs | 320 | The first-run bootstrapping ritual: seeds workspace identity files (AGENTS.md, BOOTSTRAP.md, IDENTITY.md, USER.md), runs the one-at-a-time Q&A to write IDENTITY/USER/SOUL, then removes BOOTSTRAP.md so it runs once; embedded/local-model handling, `--skip-bootstrap`, and that it always runs on the gateway host. |
| 2 | `oc_start_docs_directory.md` | concept | start/docs-directory.md: Start here, Providers and UX, Companion apps, Operations and safety, Related | 300 | The curated docs directory — a quick-access index grouping the most-used OpenClaw pages into Start here, Providers and UX, Companion apps, and Operations and safety clusters; when to use it vs the full Docs hubs map. |
| 3 | `oc_start_getting_started.md` | procedure | start/getting-started.md: What you need, Quick setup (5 steps), Advanced (custom Control UI, env vars), What to do next | 600 | The ~5-minute quickstart: Node 24 + a provider API key, install via curl/PowerShell script, `openclaw onboard --install-daemon`, verify with `openclaw gateway status` (port 18789), open the Control UI with `openclaw dashboard`, send a first message; plus custom Control UI mount and the OPENCLAW_HOME/STATE_DIR/CONFIG_PATH env vars. |
| 4 | `oc_start_hubs.md` | concept | start/hubs.md: Start here, Installation+updates, Core concepts, Providers+ingress, Gateway+operations, Tools+automation, Nodes/media/voice, Platforms, macOS companion app, Plugins, Workspace+templates, Project, Testing+release, Related | 480 | The Docs hubs page — the complete documentation map linking every page (including deep dives not in the left nav), organized into 13 topical clusters; the canonical "find any doc" index complementing the curated docs-directory. |
| 5 | `oc_start_lore.md` | concept | start/lore.md: Origin Story, First Molt, The Name, Daleks vs Lobsters, Key Characters (Molty, Peter), Moltiverse, Great Incidents, Sacred Texts, Lobster Creed, Icon Generation Saga, The Future | 650 | OpenClaw's backstory and brand/tone lore: the Warelay→Clawd→Molty→OpenClaw molting/rename history (Jan 2026), the "claw is the law" identity, the Moltiverse community, the sacred workspace texts (SOUL/AGENTS/USER/memory), and the Lobster Creed — context for docs/UX copy. |
| 6 | `oc_start_onboarding.md` | procedure | start/onboarding.md: macOS first-run Steps (macOS warning, local networks, welcome+security notice, Local vs Remote, Permissions/TCC, CLI install, dedicated onboarding chat) | 600 | The macOS-app first-run onboarding flow: approve macOS/network warnings, the security trust model (personal-agent default, `tools.profile: "coding"`), choose Local vs Remote gateway with token-auth tips, grant TCC permissions, optional global CLI install (npm→pnpm→bun), and the dedicated onboarding chat session. |
| 7 | `oc_start_onboarding_overview.md` | procedure | start/onboarding-overview.md: Which path should I use?, What onboarding configures, CLI onboarding, macOS app onboarding, Custom or unlisted providers, Related | 500 | The onboarding path chooser: CLI (`openclaw onboard`, all platforms, `--non-interactive`, servers/headless) vs macOS app (guided UI, Mac only); the 5 things onboarding always configures (provider+auth, workspace, gateway, channels, daemon); and the Custom Provider option (compat mode, base URL, key, model ID/alias). |

## Section Coverage Map

```
start/bootstrapping.md
├── (intro: first-run ritual after onboarding) ───────── → note 1 (oc_start_bootstrapping)
├── What bootstrapping does (seeds files, Q&A, writes IDENTITY/USER/SOUL, removes BOOTSTRAP) → note 1
├── Skipping bootstrapping (--skip-bootstrap) ────────── → note 1
├── Where it runs (gateway host; remote workspace note) → note 1
└── Related docs (Onboarding, Agent workspace) ──────── → note 1 (Related Notes / link-out co01)
start/docs-directory.md
├── (Note: curated index; new users → Getting Started) → note 2 (oc_start_docs_directory)
├── Start here (hubs, help, config, slash, multi-agent, …) → note 2 (cluster, link-out)
├── Providers and UX (WebChat, Control UI, channels, media) → note 2 (cluster, link-out)
├── Companion apps (macOS/iOS/Android/Windows/Linux) ── → note 2 (cluster, link-out pf*)
├── Operations and safety (sessions, cron, webhooks, security, troubleshooting) → note 2 (cluster)
└── Related (Getting started, Docs hubs) ───────────── → note 2 (Related Notes / sibling oc notes)
start/getting-started.md
├── (intro: install + first chat in ~5 min) ────────── → note 3 (oc_start_getting_started)
├── What you need (Node 24/22.19+, provider API key; Windows tip) → note 3
├── Quick setup <Steps>:
│   ├── Step 1 Install OpenClaw (curl install.sh / PowerShell iwr) → note 3
│   ├── Step 2 Run onboarding (openclaw onboard --install-daemon) → note 3
│   ├── Step 3 Verify Gateway (openclaw gateway status, port 18789) → note 3
│   ├── Step 4 Open dashboard (openclaw dashboard → Control UI) → note 3
│   └── Step 5 Send first message (Telegram fastest channel) → note 3
├── Accordion: custom Control UI build (gateway.controlUi.root) → note 3
├── What to do next <Columns> (channels, pairing, gateway config, tools) → note 3 (link-out)
├── Accordion: environment variables (OPENCLAW_HOME/STATE_DIR/CONFIG_PATH) → note 3
└── Related (Install, Channels, Setup) ─────────────── → note 3 (Related Notes / link-out)
start/hubs.md
├── (intro: hubs link every page incl. deep dives) ─── → note 4 (oc_start_hubs)
├── Start here ──────────────────────────────────────── → note 4 (cluster, link-out)
├── Installation + updates ─────────────────────────── → note 4 (cluster, link-out in*)
├── Core concepts ──────────────────────────────────── → note 4 (cluster, link-out co*)
├── Providers + ingress ────────────────────────────── → note 4 (cluster, link-out pr*/ch*)
├── Gateway + operations ───────────────────────────── → note 4 (cluster, link-out gw*)
├── Tools + automation ─────────────────────────────── → note 4 (cluster, link-out to*/au*)
├── Nodes, media, voice ────────────────────────────── → note 4 (cluster, link-out nd*)
├── Platforms ──────────────────────────────────────── → note 4 (cluster, link-out pf*)
├── macOS companion app (advanced) ─────────────────── → note 4 (cluster, link-out pf*)
├── Plugins ────────────────────────────────────────── → note 4 (cluster, link-out pl*)
├── Workspace + templates ──────────────────────────── → note 4 (cluster, link-out rf*)
├── Project / Testing + release ────────────────────── → note 4 (cluster, link-out rf*)
└── Related (Getting started) ──────────────────────── → note 4 (Related Notes / sibling oc)
start/lore.md
├── # The Lore of OpenClaw (intro) ─────────────────── → note 5 (oc_start_lore)
├── The Origin Story (Warelay→Clawd→Molty→OpenClaw) ── → note 5
├── The First Molt (Jan 27 2026) ───────────────────── → note 5
├── The Name (OpenClaw = OPEN + CLAW) ──────────────── → note 5
├── The Daleks vs The Lobsters (EXTERMINATE/EXFOLIATE) → note 5
├── Key Characters → Molty / Peter (H3) ────────────── → note 5
├── The Moltiverse (community/ecosystem) ───────────── → note 5
├── The Great Incidents → Directory Dump / Great Molt / Final Form / Robot Shopping (H3) → note 5
├── Sacred Texts (SOUL/memory/AGENTS/USER .md) ─────── → note 5
├── The Lobster Creed ──────────────────────────────── → note 5
├── Icon Generation Saga (H3) ──────────────────────── → note 5
├── The Future ─────────────────────────────────────── → note 5
└── Related (Getting started) ──────────────────────── → note 5 (Related Notes / sibling oc)
start/onboarding.md  (MDX <Steps>; substantive sections = step titles)
├── (intro: current first-run flow; → onboarding-overview) → note 6 (oc_start_onboarding)
├── Step Approve macOS warning ─────────────────────── → note 6
├── Step Approve find local networks ───────────────── → note 6
├── Step Welcome and security notice (trust model, tools.profile coding) → note 6
├── Step Local vs Remote (auth handling, remote token, gateway.remote.token) → note 6
├── Step Permissions (TCC: automation/notifications/accessibility/screen/mic/speech/camera/location) → note 6
├── Step CLI (optional global openclaw via npm→pnpm→bun) → note 6
├── Step Onboarding Chat (dedicated session; → bootstrapping) → note 6
└── Related (Onboarding overview, Getting started) ─── → note 6 (Related Notes / sibling oc)
start/onboarding-overview.md
├── (intro: two onboarding paths; both configure auth/gateway/channels) → note 7 (oc_start_onboarding_overview)
├── Which path should I use? (CLI vs macOS app table) ─ → note 7
├── What onboarding configures (provider+auth, workspace, gateway, channels, daemon) → note 7
├── CLI onboarding (openclaw onboard [--install-daemon]) → note 7
├── macOS app onboarding (guided UI) ───────────────── → note 7
├── Custom or unlisted providers (compat mode, base URL, key, model ID/alias) → note 7
└── Related (Getting started, CLI setup reference) ─── → note 7 (Related Notes / link-out st02)
```
No orphaned sections. All downstream link-out targets (gateway config, concepts, channels, tools, install, platforms, templates, automation, web) are deferred to their home sub-plans per master and surface only as Related-Notes / cross-links.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | Every page is single-BB and ≤1,200 words / ≤3 code blocks (largest: lore 1,133w / 2 blocks). No page exceeds the 2,500-word or mixed-BB split thresholds; 1 page → 1 note. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (3,421 measured words). New `oc_` notes: **7**. New `term_dictionary` notes: **0** (master locked count was 11; this sub-plan locks at 7 because every page is single-BB and under-cap — faithful to the measured source; the master's per-sub-plan estimate is an upper bound, reconciled at augment/review).
- BB distribution: **concept ×4** (notes 1 bootstrapping, 2 docs-directory, 4 hubs, 5 lore) · **procedure ×3** (notes 3 getting-started, 6 onboarding, 7 onboarding-overview).
- Est. digest words ~3,450 (avg ~490/note); all well within the ≤2,500-word / ≤400-line / ≤6-code-block caps. Total source fences = 6 (getting-started 3 + lore 2 + onboarding-overview 1) distribute one-to-one into their notes; no note exceeds 3 code blocks.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)



### oc_start_bootstrapping (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/agent platform being bootstrapped; relevance: bootstrapping is OpenClaw's first-run ritual.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — the agent operating-instructions workspace file; relevance: AGENTS.md is one of the four files seeded on first run.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — autonomous goal-directed AI agents; relevance: bootstrapping establishes the agent's identity/SOUL so it can act autonomously.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the ritual special-cases embedded/local-model runs (BOOTSTRAP.md kept out of system context).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the default model that runs the interactive Q&A and writes IDENTITY/USER/SOUL.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — provider auth credential; relevance: identity/auth is collected and persisted alongside the bootstrap workspace.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: bootstrapping writes into the isolated `~/.openclaw/workspace` on the gateway host.
- [Subagent](../../term_dictionary/term_subagent.md) — a child agent spawned by the runtime; relevance: the agent runtime that runs the ritual is the same one that governs subagent spawning.

**Docs**
- [Hermes: SOUL.md guide](../hermes_agent/hermes_use_soul_md_guide.md) — how a sibling agent uses a SOUL identity file; relevance: bootstrapping writes SOUL.md, the identity doc.
- [Hermes: personality / soul](../hermes_agent/hermes_personality_soul.md) — agent personality persisted to a soul file; relevance: direct analog to OpenClaw's IDENTITY/SOUL seeding.
- [Hermes: context files](../hermes_agent/hermes_context_files.md) — workspace context/identity files loaded per run; relevance: same workspace-file seeding pattern as AGENTS/USER/IDENTITY.
- [Hermes: prompt assembly](../hermes_agent/hermes_prompt_assembly.md) — how context files are folded into the system prompt; relevance: explains why BOOTSTRAP.md is passed in the user prompt for unreliable read-tool models.
- [Hermes: config file precedence](../hermes_agent/hermes_config_files_precedence.md) — workspace/config layering; relevance: parallels where bootstrapping writes and how files are resolved.
- [Hermes: context references](../hermes_agent/hermes_context_references.md) — referencing memory/context artifacts; relevance: the seeded files become long-lived context references.
- [Hermes: migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — importing an OpenClaw workspace; relevance: documents the same `~/.openclaw/workspace` file set bootstrapping produces.
- [Claude Code: memory overview](../claude_code/cc_memory_overview.md) — sibling tool's memory/workspace files; relevance: closest external analog to seeding workspace + memory files.
- [oc_start_onboarding](oc_start_onboarding.md) **(planned, this series)** — macOS first-run flow; relevance: bootstrapping happens immediately after onboarding.
- [oc_start_onboarding_overview](oc_start_onboarding_overview.md) **(planned, this series)** — what onboarding configures; relevance: the workspace bootstrapping seeds is one of the five things onboarding sets up.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — parent monorepo; relevance: bootstrapping is an OpenClaw platform feature.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the runtime that performs the first-run Q&A ritual.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboard/wizard CLI; relevance: `openclaw onboard --skip-bootstrap` lives here.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory/workspace-file subsystem; relevance: implements the seeded memory/identity files.

**Snippets**
- [openclaw agents bootstrap budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — token-budget logic for the bootstrap pass; relevance: the embedded/primary-run BOOTSTRAP.md handling described in this note.
- [openclaw agents system-prompt context injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injecting workspace files into context; relevance: how BOOTSTRAP.md/AGENTS.md reach the model.
- [openclaw agents system-prompt modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — privileged vs user-prompt modes; relevance: the privileged-context exclusion for local models.
- [openclaw memory root files](../../code_snippets/snippet_openclaw_memory_root_files.md) — the root workspace file set; relevance: enumerates AGENTS/IDENTITY/USER/SOUL the ritual seeds.
- [openclaw memory host internal walker](../../code_snippets/snippet_openclaw_memory_host_internal_walker.md) — walks workspace memory files; relevance: reads the seeded workspace on the gateway host.
- [openclaw memory engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory persistence engine; relevance: persists the IDENTITY/USER/SOUL the ritual writes.
- [openclaw memory events](../../code_snippets/snippet_openclaw_memory_events.md) — memory-file change events; relevance: fires when bootstrapping writes/removes files.
- [openclaw CLI run main bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap entry; relevance: the code path behind first-run bootstrapping.
- [openclaw agents subagent spawn policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — runtime spawn governance; relevance: same runtime that runs the ritual on the gateway host.
- [openclaw wizard migration import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — importing an existing workspace; relevance: the `--skip-bootstrap` pre-seeded-workspace path.
- [hermes core prompt-builder context loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads identity/context files into the prompt; relevance: how a sibling agent injects seeded workspace files.

### oc_start_docs_directory (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the platform whose docs this indexes; relevance: this is OpenClaw's curated docs index.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway runbook/configuration cluster; relevance: Configuration / Gateway runbook / Remote access links headline the index.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent routing; relevance: "Multi-agent routing" is a Start-here entry.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: "Cron jobs" sits in the Operations and safety cluster.
- [Skills](../../term_dictionary/term_skills.md) — agent skills/capabilities; relevance: "Skills" and "Skills config" are Start-here entries.
- [WebSocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: Discovery and transports / Remote access links rely on the WS gateway protocol.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP callback; relevance: "Webhooks" and Gmail Pub/Sub appear in Operations and safety.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway that brokers tool/channel access; relevance: the gateway runbook + RPC adapters cluster the index points to.

**Docs**
- [Hermes: slash commands (messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — slash-command surface; relevance: "Slash commands" is an index entry.
- [Hermes: skills system](../hermes_agent/hermes_skills_system.md) — skills/skills-config; relevance: the Skills + Skills config index links.
- [Hermes: gateway operations](../hermes_agent/hermes_gateway_operations.md) — gateway runbook ops; relevance: the Gateway runbook + Operations cluster.
- [Hermes: features overview](../hermes_agent/hermes_features_overview.md) — curated feature map; relevance: a sibling "what's here" index, the same role as this page.
- [Hermes: plugins system](../hermes_agent/hermes_plugins_system.md) — plugin/extension surface; relevance: parallels the Providers/UX + companion-apps clusters.
- [Hermes: integrations overview](../hermes_agent/hermes_integrations_overview.md) — channels/apps catalog; relevance: mirrors the Companion apps + Providers and UX clusters.
- [Hermes: web dashboard overview](../hermes_agent/hermes_web_dashboard_overview.md) — Control-UI/dashboard; relevance: "Control UI (browser)" + "WebChat" index links.
- [Claude Code: SDK slash commands](../claude_code/cc_sdk_slash_commands.md) — sibling slash-command docs; relevance: external analog to the slash-commands index entry.
- [oc_start_hubs](oc_start_hubs.md) **(planned, this series)** — the complete docs map; relevance: this curated index is a subset of the full hubs map.
- [oc_start_getting_started](oc_start_getting_started.md) **(planned, this series)** — the new-user starting point; relevance: the page's Note tells new users to start there.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — parent monorepo; relevance: the docs index covers OpenClaw.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — companion apps; relevance: the Companion apps cluster (macOS/iOS/Android/Windows/Linux).

**Snippets**
- [hermes core skill-commands discovery](../../code_snippets/snippet_hermes_agent_core_skill_commands_discovery.md) — discovers slash/skill commands; relevance: implements the slash-commands + skills the index links.
- [hermes gw slash access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command access control; relevance: the Slash commands index entry.
- [hermes skills index cache](../../code_snippets/snippet_hermes_agent_skills_index_cache.md) — caches the skills index; relevance: Skills / Skills config index entries.
- [hermes CLI skills hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — skills hub command; relevance: Skills + ClawHub navigation.
- [hermes CLI skills install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — installs a skill; relevance: Skills config workflow the index points to.
- [hermes gw channel directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel registry; relevance: the Providers and UX / channels cluster.
- [hermes skills mcp-native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md) — MCP-backed skills; relevance: Skills + RPC adapters cluster.
- [hermes cron run-job execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — executes a cron job; relevance: the Cron jobs Operations entry.
- [openclaw gateway server http listen ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway HTTP/WS listener; relevance: Discovery + transports + Remote access cluster.
- [openclaw gateway nodes pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — DM/node pairing; relevance: the "Pairing (DM and nodes)" index entry.

### oc_start_getting_started (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the platform being installed; relevance: the quickstart installs and first-runs OpenClaw.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: Node 24 (22.19+) is the stated prerequisite.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway service; relevance: `openclaw gateway status` verifies the Gateway on port 18789.
- [Authentication](../../term_dictionary/term_authentication.md) — auth setup; relevance: onboarding configures provider auth as part of the quickstart.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — provider credential; relevance: the API-key/auth the onboarding step writes.
- [LLM](../../term_dictionary/term_llm.md) — model backend; relevance: you choose a model provider during onboarding.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: Anthropic is the first listed provider option.
- [Skills](../../term_dictionary/term_skills.md) — agent skills/plugins; relevance: the "Browse tools" next-step card surfaces skills and plugins.

**Docs**
- [Claude Code: quickstart](../claude_code/cc_quickstart.md) — sibling-tool getting-started; relevance: direct external analog of this quickstart.
- [Claude Code: install](../claude_code/cc_install.md) — sibling-tool install; relevance: parallels the curl/PowerShell install step.
- [Claude Code: authentication](../claude_code/cc_authentication.md) — sibling-tool auth; relevance: parallels the onboarding auth/API-key step.
- [pi: quickstart](../pi/pi_quickstart.md) — sibling coding-agent quickstart; relevance: same install→auth→first-chat shape.
- [band: setup](../band/band_setup.md) — coding-agent setup guide; relevance: install + connect-agent analog.
- [Hermes: quickstart first chat](../hermes_agent/hermes_quickstart_first_chat.md) — install to first message; relevance: mirrors the "send your first message" step.
- [Hermes: install (Nix quickstart)](../hermes_agent/hermes_install_nix_quickstart.md) — fast install path; relevance: an alternate-install analog to the curl script.
- [Hermes: FAQ install/provider/terminal](../hermes_agent/hermes_faq_install_provider_terminal.md) — install/provider troubleshooting; relevance: covers the Node/provider prerequisites this note lists.
- [oc_start_onboarding_overview](oc_start_onboarding_overview.md) **(planned, this series)** — onboarding path chooser; relevance: the `openclaw onboard` step's reference.
- [oc_start_onboarding](oc_start_onboarding.md) **(planned, this series)** — macOS first-run flow; relevance: the GUI alternative to the CLI onboard step.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboard/dashboard/gateway-status CLI; relevance: implements every command in the quickstart.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway service; relevance: the Gateway started and verified on port 18789.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — parent monorepo; relevance: the install target.

**Snippets**
- [openclaw wizard setup config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding wizard config write; relevance: what `openclaw onboard` produces.
- [openclaw wizard setup imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard module wiring; relevance: the onboarding step internals.
- [openclaw CLI run main bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI entry/bootstrap; relevance: backs `openclaw onboard --install-daemon`.
- [openclaw daemon systemd unit render/parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — Linux service unit; relevance: `--install-daemon` background service.
- [openclaw daemon launchd plist render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — macOS launchd service; relevance: `--install-daemon` on macOS.
- [openclaw gateway server http listen ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway listener; relevance: the Gateway listening on port 18789.
- [openclaw gateway ws connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — Control-UI WS connection; relevance: `openclaw dashboard` connects the Control UI.
- [hermes CLI setup installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — sibling install script; relevance: analog to the curl/PowerShell installer.
- [hermes CLI gateway systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — sibling daemon install; relevance: analog to `--install-daemon`.
- [hermes CLI web app](../../code_snippets/snippet_hermes_agent_cli_web_app.md) — opens the web dashboard; relevance: analog to `openclaw dashboard`.
- [hermes CLI doctor primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — gateway health checks; relevance: analog to `openclaw gateway status` verification.
- [hermes acp bootstrap.sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — install/bootstrap shell script; relevance: the install-script pattern this note runs.

### oc_start_hubs (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the platform this maps; relevance: hubs is OpenClaw's complete docs map.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway runbook; relevance: the Gateway + operations cluster.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent routing; relevance: the Core concepts cluster (multi-agent routing).
- [Subagent](../../term_dictionary/term_subagent.md) — child agents; relevance: the Tools + automation cluster (sub-agents).
- [Skills](../../term_dictionary/term_skills.md) — agent skills; relevance: the Workspace + templates + plugins clusters.
- [OAuth](../../term_dictionary/term_oauth.md) — OAuth auth flow; relevance: the Core concepts cluster (OAuth).
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the Tools + automation cluster (cron jobs).
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — workspace template file; relevance: the Workspace + templates cluster (default AGENTS / templates).

**Docs**
- [Hermes: architecture](../hermes_agent/hermes_architecture.md) — agent-gateway architecture; relevance: the Core concepts (Architecture) cluster.
- [Hermes: features overview](../hermes_agent/hermes_features_overview.md) — feature map; relevance: a sibling complete-feature index, same role as hubs.
- [Hermes: plugins system](../hermes_agent/hermes_plugins_system.md) — plugin surface; relevance: the Plugins cluster.
- [Hermes: plugin types / surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin/integration surfaces; relevance: the Plugins + Tools clusters.
- [Hermes: integrations overview](../hermes_agent/hermes_integrations_overview.md) — channels/providers catalog; relevance: the Providers + ingress cluster.
- [Hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway internals; relevance: the Gateway + operations cluster.
- [Hermes: tools / toolsets](../hermes_agent/hermes_tools_toolsets.md) — tool surface; relevance: the Tools + automation cluster.
- [Claude Code: platforms and integrations](../claude_code/cc_platforms_and_integrations.md) — sibling platform map; relevance: the Platforms + companion-app clusters.
- [oc_start_docs_directory](oc_start_docs_directory.md) **(planned, this series)** — curated index; relevance: a curated subset of this full hubs map.
- [oc_start_getting_started](oc_start_getting_started.md) **(planned, this series)** — quickstart; relevance: the page hubs points new users to first.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — parent monorepo; relevance: the docs map covers the whole project.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — companion apps; relevance: the Platforms + macOS companion-app clusters.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the Gateway + operations cluster.

**Snippets**
- [hermes gw channel directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel registry; relevance: the Providers + ingress cluster.
- [hermes plugins provider registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: the Model providers + Plugins clusters.
- [hermes plugins SDK architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK design; relevance: the Plugins (building plugins) cluster.
- [hermes core skill-commands discovery](../../code_snippets/snippet_hermes_agent_core_skill_commands_discovery.md) — skills/slash discovery; relevance: the Workspace + templates (skills) cluster.
- [hermes plugins browser dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser-control tool; relevance: the Tools (browser control) cluster.
- [hermes gw platform slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack channel adapter; relevance: the Providers + ingress (Slack) cluster.
- [hermes cron run-job execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — cron executor; relevance: the Tools + automation (cron) cluster.
- [openclaw gateway server plugins runtime load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — loads plugins at runtime; relevance: the Plugins cluster.
- [openclaw gateway server http listen ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway listener; relevance: the Gateway + operations cluster.
- [openclaw acp server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP/RPC server; relevance: the Core concepts (RPC adapters) cluster.
- [openclaw memory engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory subsystem; relevance: the Core concepts (Memory) cluster.
- [openclaw sessions lifecycle events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle; relevance: the Core concepts (Sessions) cluster.

### oc_start_lore (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the subject of the lore; relevance: the page is OpenClaw's own backstory.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's models; relevance: Molty is "a Claude instance"; Anthropic's rename email drove the molt.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — workspace operating-instructions file; relevance: AGENTS.md is a named "Sacred Text".
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — autonomous AI agents; relevance: Molty as an autonomous personal agent with a soul/memory.
- [Vibe Coding](../../term_dictionary/term_vibe_coding.md) — playful build-by-feel culture; relevance: the lore embodies the project's build/community culture.
- [Subagent](../../term_dictionary/term_subagent.md) — child agents; relevance: the agent-identity model the lore narrates ("every instance equally real").
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Icon Saga ("AI image generation is stochastic") and Molty's pattern-matching existential note.

**Docs**
- [Hermes: personality / soul](../hermes_agent/hermes_personality_soul.md) — agent personality via a soul file; relevance: the SOUL.md identity the lore canonizes as a Sacred Text.
- [Hermes: SOUL.md guide](../hermes_agent/hermes_use_soul_md_guide.md) — how SOUL.md shapes the agent; relevance: the identity-doc concept the lore mythologizes.
- [Hermes: context files](../hermes_agent/hermes_context_files.md) — workspace identity/memory files; relevance: the AGENTS/USER/memory "Sacred Texts".
- [Hermes: persistent memory](../hermes_agent/hermes_persistent_memory.md) — long-term memory files; relevance: "remembers things through markdown files".
- [Hermes: migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — the OpenClaw lineage; relevance: documents the Clawd→Molty→OpenClaw heritage the lore narrates.
- [Hermes: tips and best practices](../hermes_agent/hermes_tips_best_practices.md) — agent norms; relevance: the Lobster Creed's "don't dump directories" maps to safe-agent norms.
- [Hermes: profiles (multi-agent)](../hermes_agent/hermes_profiles_multi_agent.md) — multiple agent identities; relevance: "every instance equally real, just loading different context".
- [Claude Code: memory overview](../claude_code/cc_memory_overview.md) — memory/identity files; relevance: external analog of the markdown-memory identity model.
- [oc_start_getting_started](oc_start_getting_started.md) **(planned, this series)** — quickstart; relevance: the lore page's only Related link.
- [oc_start_bootstrapping](oc_start_bootstrapping.md) **(planned, this series)** — first-run identity ritual; relevance: where the Sacred Texts (SOUL/IDENTITY/USER) are actually seeded.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the project the lore is about; relevance: the lore is OpenClaw's own origin story.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS/companion apps; relevance: the Icon Generation Saga and app branding.

**Snippets**
- [openclaw agents system-prompt context injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects identity files into context; relevance: how the "Sacred Texts" reach the model.
- [openclaw memory root files](../../code_snippets/snippet_openclaw_memory_root_files.md) — SOUL/AGENTS/USER/memory file set; relevance: the literal Sacred Texts of the lore.
- [openclaw memory engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory persistence; relevance: "remembers things through markdown files".
- [openclaw memory events](../../code_snippets/snippet_openclaw_memory_events.md) — memory-change events; relevance: the living memory the lore describes.
- [openclaw gateway agent identity reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — resets agent identity; relevance: the identity/molt theme made concrete.
- [openclaw agents bootstrap budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap token budget; relevance: how a fresh Molty identity is established.
- [openclaw wizard migration import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — imports an existing workspace; relevance: carrying "same lobster soul" across a molt/rename.
- [openclaw macos canvas filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — watches workspace files on macOS; relevance: the markdown-file memory model in the app.
- [hermes core prompt-builder context loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads soul/identity files; relevance: a sibling agent loading its "soul".
- [hermes optional-skills migration openclaw](../../code_snippets/snippet_hermes_agent_optional_skills_migration_openclaw.md) — OpenClaw→Hermes migration; relevance: the molt/rename lineage in code.

### oc_start_onboarding (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: the macOS app's first-run flow for OpenClaw.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — local vs remote Gateway; relevance: the Local-vs-Remote step chooses where the Gateway runs.
- [Authentication](../../term_dictionary/term_authentication.md) — auth/credentials; relevance: the welcome/security step + writing local credentials.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — remote gateway token; relevance: `gateway.remote.token` for the macOS app to reach a remote Gateway.
- [Sandbox](../../term_dictionary/term_sandbox.md) — tool isolation; relevance: defaults to `tools.profile: "coding"` with strict tool policy/sandboxing.
- [WebSocket](../../term_dictionary/term_websocket.md) — local WS clients; relevance: the wizard generates a token so local WS clients must authenticate.
- [Node.js](../../term_dictionary/term_node_js.md) — runtime/package managers; relevance: optional global CLI install via npm/pnpm/bun; Node is the recommended Gateway runtime.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — sandbox enforcement layer; relevance: the strict tool policy/sandboxing for untrusted feeds.

**Docs**
- [Claude Code: desktop quickstart](../claude_code/cc_desktop_quickstart.md) — sibling desktop-app first run; relevance: direct analog of the macOS app onboarding.
- [Claude Code: sandboxed bash tool setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — tool sandbox config; relevance: the `tools.profile: "coding"` sandboxing default.
- [Claude Code: remote control](../claude_code/cc_remote_control.md) — remote backend connection; relevance: the Remote-Gateway-over-SSH/Tailnet step.
- [Claude Code: authentication](../claude_code/cc_authentication.md) — desktop auth; relevance: the welcome/security auth step.
- [Claude Code: login auth troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth/token issues; relevance: token-auth tips for local vs remote.
- [Hermes: desktop app](../hermes_agent/hermes_desktop_app.md) — sibling desktop GUI; relevance: a guided-UI onboarding analog.
- [Hermes: security isolation / credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: the personal-agent trust boundary + token handling.
- [pi: security model](../pi/pi_security_model.md) — agent trust/permission model; relevance: the security trust model and permission grants.
- [oc_start_onboarding_overview](oc_start_onboarding_overview.md) **(planned, this series)** — onboarding path chooser; relevance: this is the macOS-app branch of that overview.
- [oc_start_bootstrapping](oc_start_bootstrapping.md) **(planned, this series)** — first-run ritual; relevance: the onboarding chat hands off to gateway-host bootstrapping.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: this is its first-run flow.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — global CLI install; relevance: the optional `openclaw` CLI install step.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: Local vs Remote gateway + token auth.

**Snippets**
- [openclaw wizard setup config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — writes onboarding config; relevance: what the guided wizard persists.
- [openclaw gateway auth modes helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token vs no-auth modes; relevance: the wizard generates a token even for loopback.
- [openclaw security openshell backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — sandboxed shell backend; relevance: the strict tool policy/sandboxing for coding profile.
- [openclaw security openshell cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — sandboxed exec CLI; relevance: the `tools.profile: "coding"` runtime tools.
- [openclaw security exec filesystem policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — filesystem tool policy; relevance: minimal-tool-access trust boundary.
- [openclaw macos menu sessions control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — macOS app session control; relevance: the dedicated onboarding chat session.
- [openclaw macos pushtotalk nsevent](../../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md) — macOS TCC/event permissions; relevance: the TCC permission grants (mic/accessibility).
- [hermes CLI auth storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — stores credentials; relevance: writing credentials locally during onboarding.
- [hermes tools environments ssh](../../code_snippets/snippet_hermes_agent_tools_environments_ssh.md) — SSH remote environment; relevance: the Remote-over-SSH/Tailnet gateway option.
- [hermes CLI setup wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — sibling guided setup wizard; relevance: analog to the macOS onboarding wizard.

### oc_start_onboarding_overview (8t · 12s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: the two onboarding paths for OpenClaw.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway port/bind/auth; relevance: onboarding always configures the Gateway.
- [Authentication](../../term_dictionary/term_authentication.md) — provider auth; relevance: API key / OAuth / setup token is configured set #1.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: the OAuth provider-auth path.
- [LLM](../../term_dictionary/term_llm.md) — model backend; relevance: choosing a model provider is the first thing onboarding configures.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic models; relevance: the Anthropic-compatible custom-provider option.
- [Node.js](../../term_dictionary/term_node_js.md) — runtime; relevance: CLI onboarding runs on macOS/Linux/Windows native or WSL2.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model provider; relevance: the Custom/unlisted provider with compat mode + base URL + model ID/alias.

**Docs**
- [Hermes: adding an inference provider](../hermes_agent/hermes_adding_inference_provider.md) — register a custom provider; relevance: direct analog of the Custom Provider step.
- [Hermes: inference providers (cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: the listed-provider choices in onboarding.
- [Hermes: CLI commands (chat/provider)](../hermes_agent/hermes_cli_commands_chat_provider.md) — provider/auth CLI; relevance: the `openclaw onboard` provider flow.
- [Hermes: env vars (providers/auth/tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env config; relevance: base URL / key / model-ID configuration.
- [pi: custom provider registration](../pi/pi_custom_provider_registration.md) — sibling custom-provider setup; relevance: compat-mode + base URL + model alias analog.
- [pi: provider auth](../pi/pi_provider_auth.md) — provider auth flows; relevance: API key / OAuth / setup-token analog.
- [pi: cloud providers](../pi/pi_cloud_providers.md) — provider options; relevance: the provider-choice step.
- [Claude Code: authentication](../claude_code/cc_authentication.md) — auth setup; relevance: the auth-configuration step shared by both paths.
- [oc_start_getting_started](oc_start_getting_started.md) **(planned, this series)** — quickstart; relevance: the quickstart that invokes `openclaw onboard`.
- [oc_start_onboarding](oc_start_onboarding.md) **(planned, this series)** — macOS app onboarding; relevance: the GUI branch of this overview.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the onboard CLI; relevance: `openclaw onboard` / `--non-interactive`.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: the guided-UI onboarding branch.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extensions; relevance: the Custom/unlisted provider compat mode + endpoint config.

**Snippets**
- [openclaw provider anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider wiring; relevance: the Anthropic-compatible provider option.
- [openclaw wizard setup config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding config write; relevance: what onboarding configures (provider/gateway/channels).
- [openclaw wizard setup imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard wiring; relevance: the CLI onboarding internals.
- [openclaw wizard migration import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — imports prior config; relevance: re-onboarding an existing setup.
- [hermes CLI auth resolve provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — resolves provider auth; relevance: provider+auth configuration step.
- [hermes CLI providers registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: the listed + custom providers.
- [hermes core agent-init API-mode resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — OpenAI/Anthropic compat resolution; relevance: the compat-mode (OpenAI/Anthropic/auto-detect) choice.
- [hermes core anthropic adapter client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — Anthropic adapter; relevance: the Anthropic-compatible base-URL/key path.
- [hermes CLI main provider flows](../../code_snippets/snippet_hermes_agent_cli_main_provider_flows.md) — provider onboarding flows; relevance: the CLI onboarding provider selection.
- [hermes core credential pool entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — credential storage entry; relevance: API key / token persisted per endpoint.
- [hermes CLI auth oauth callback server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback handler; relevance: the OAuth provider-auth path.
- [hermes CLI setup installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — install + daemon; relevance: the `--install-daemon` CLI onboarding option.

## Undigested Terms Plan

Per master: OpenClaw vocabulary terms are the *subjects of their own doc pages* → digested as `oc_` doc notes by their home sub-plan; the only `term_dictionary` interaction is **linking existing** terms. **Expected 0 new `term_dictionary` captures.**

| Term (appears in source) | Disposition |
|---|---|
| bootstrapping (first-run ritual) | OpenClaw vocab → covered by note 1 `oc_start_bootstrapping`; not a term note. |
| onboarding (CLI vs macOS app) | OpenClaw vocab → covered by notes 6/7; link `term_authentication`. No `term_onboarding` exists and it is too generic to promote (master policy). |
| workspace / agent workspace | OpenClaw vocab → home is `concepts/agent-workspace` (co01); link from notes 1/7. No `term_workspace`/`term_agent_workspace` note exists; do not create here. |
| daemon / `--install-daemon` | OpenClaw vocab → described in notes 3/6/7; home `gateway/background-process` (gw01). No `term_daemon` note exists; do not create (generic). |
| Control UI / dashboard / WebChat | OpenClaw vocab → home `web/*` (wb01); link from note 3. Not term notes. |
| TCC permissions (macOS) | Platform vocab → described in-note (note 6); home `platforms/mac/permissions` (pf03). No `term_tcc_permissions` exists; do not create (platform-specific, lives in pf doc note). |
| Custom Provider / compat mode | Provider vocab → described in-note (note 7); link `term_llm`/`term_claude`; home `providers/*` (pr01–09). Not a term note. |

**New-term candidates:** **NONE.** No genuinely cross-cutting, vault-reusable term with no doc-page home and no existing note appears in these 7 pages. (Re-scanned at augment via Step 2d.)

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method | Pass criterion |
|------|-------|---------------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | YAML field order + forbidden-field check pass; `# OpenClaw — …` H1, `## Overview`, `## Related Notes`, `## References`, bold `**Source**`/`**Last Updated**`/`**Status**` footer present; no broken internal links (LINK-003 clean). |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/start/<page>.md` | every claim traceable to source; commands (`openclaw onboard --install-daemon`, `gateway status`, port 18789, `dashboard`) reproduced verbatim; no hallucinated steps. |
| G3 | Density + Coverage | `wc -w` (body) + fence count + Section Coverage Map | each note ≤2,500w / ≤400 lines / ≤6 code blocks; every source H2/H3/MDX-step mapped (no orphan). |
| G4 | Cross-Reference | Related Notes audit | each note ≥8 relevancy `term_dictionary` terms + ≥10 code_snippets + ≥10 docs + repo/sibling/vault links (LOCKED floors, xref-augment 2026-06-21), each with a relevance statement; indexed `[text](path.md)` format. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + reindex | 0 broken links after incremental reindex. |
| G7/G8 | Discoverability / in-degree | `note_links` query | every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island), in-degree ≥1 — satisfied via `entry_openclaw_docs.md` (W1) + the inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_start_bootstrapping oc_start_docs_directory oc_start_getting_started oc_start_hubs oc_start_lore oc_start_onboarding oc_start_onboarding_overview"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format + broken-link
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"; done
  # require source_url in frontmatter
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density caps (body words excl. frontmatter; fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # sibling self-link sanity (siblings use the oc_ prefix)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NOTE: no sibling oc_ link in $n"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps (≤2500w / ≤400L / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_start_bootstrapping | concept | 320 | 0 | ✅ |
| 2 | oc_start_docs_directory | concept | 300 | 0 | ✅ |
| 3 | oc_start_getting_started | procedure | 600 | 3 | ✅ |
| 4 | oc_start_hubs | concept | 480 | 0 | ✅ |
| 5 | oc_start_lore | concept | 650 | 2 | ✅ |
| 6 | oc_start_onboarding | procedure | 600 | 0 | ✅ |
| 7 | oc_start_onboarding_overview | procedure | 500 | 1 | ✅ |

No note approaches any cap. The index pages (docs-directory, hubs) are kept concise (curated grouping + when-to-use, not full link dumps). The 6 source fences (getting-started 3, lore 2, onboarding-overview 1) map one-to-one into their notes; no note exceeds 3 code blocks.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate OUTSIDE-folder inbound links (DB-verify at execution; each satisfies G7/G8 for the target note):

| New note | Candidate inbound links (existing notes) |
|---|---|
| oc_start_bootstrapping | `entry_openclaw_docs.md` (W1); `repo_openclaw_agents.md`; `term_agents_md.md` |
| oc_start_docs_directory | `entry_openclaw_docs.md` (W1); `repo_openclaw.md` |
| oc_start_hubs | `entry_openclaw_docs.md` (W1); `repo_openclaw.md` |
| oc_start_onboarding | `entry_openclaw_docs.md` (W1); `repo_openclaw_apps.md`; `term_messaging_gateway.md` |
| oc_start_onboarding_overview | `entry_openclaw_docs.md` (W1); `repo_openclaw_cli_wizard.md`; `term_authentication.md` |

`entry_openclaw_docs.md` (W1) is the guaranteed inbound link for all 7 (anti-island); the term/repo inlinks are reciprocal-backlink candidates added during execution (`/tessellum-add-inlinks`).

## Pacing Rules (inherited from master)

One execution phase; all 8 gates pass before commit. Re-read each source page at execute; reproduce commands/config snippets verbatim; one BB per note. Cap dynamic-workflow fan-out at ~30 agents/run (7 notes is a single small wave). `git pull --rebase --autostash origin main` first; commit + push the wave together; **no Claude co-author trailer**. Reindex incrementally; verify `note_links` + 0 broken links before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Follow-up Recommendations

- Ensure `entry_openclaw_docs.md` (W1) exists before execution so all 7 notes have a guaranteed inbound link (G7/G8).
- After landing: incremental reindex; reciprocal inlinks; queue 7 rows for `entry_openclaw_docs.md` "Start / Getting Started" cluster; broken-link sweep; in-degree ≥1 verify. Cross-link sibling sub-plan st02 (openclaw/quickstart/setup/wizard) and the operational targets (gw02 configuration, in01–05 install, co01 agent-workspace).

## Augmentation Report (2026-06-21)


**Source re-read confirmation:** all 7 pages re-read 2026-06-21; measured `wc -w` matches the plan's Source table exactly (bootstrapping 256 · docs-directory 197 · getting-started 509 · hubs 508 · lore 1,133 · onboarding 469 · onboarding-overview 349 = 3,421). No density/coverage change; no new splits. No new undigested terms surfaced (Step 2d re-scan) — consistent with master's "expected 0 new term_dictionary captures".

**Per-note LOCKED counts (all floors met):**

| Note | Terms | Snippets | Docs (existing+planned) | Repos | Floors met (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_start_bootstrapping | 8 | 12 | 10 (8 existing + 2 planned) | 4 | YES |
| oc_start_docs_directory | 8 | 10 | 10 (8 existing + 2 planned) | 2 | YES |
| oc_start_getting_started | 8 | 12 | 10 (8 existing + 2 planned) | 3 | YES |
| oc_start_hubs | 8 | 12 | 10 (8 existing + 2 planned) | 3 | YES |
| oc_start_lore | 8 | 12 | 10 (8 existing + 2 planned) | 3 | YES |
| oc_start_onboarding | 8 | 12 | 10 (8 existing + 2 planned) | 3 | YES |
| oc_start_onboarding_overview | 8 | 12 | 10 (8 existing + 2 planned) | 3 | YES |


**DB-verification:** every cited EXISTING `term_*`, `repo_*`, `cc_*/pi_/hermes_/band_*` doc, and `snippet_*` was confirmed with `SELECT 1 FROM notes WHERE note_id='…'` on 2026-06-21. Misses found during selection and excluded from the final mapping (never written into a note): `term_system_prompt`, `term_macos`, `term_gateway`, `term_onboarding`, `term_workspace`, `term_daemon`, `term_tcc_permissions` (all NOT IN VAULT — the plan's earlier swap notes were correct); these were replaced with verified equivalents (e.g. `term_sandbox_backend`, `term_provider_plugin`, `term_tool_gateway`, `term_webhook`). `entry_openclaw_docs.md` is intentionally NOT a Related-Notes target (planned at W1; it is the inbound-link source per G7/G8, not an outbound cite).

**New-term candidates:** NONE. Re-scan of all 7 pages (Step 2d) surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing vault note. OpenClaw-specific vocabulary (bootstrapping, onboarding, daemon, Control UI, TCC permissions, Moltiverse, Custom Provider) is digested in-note or owned by another sub-plan's doc note per master policy; reusable concepts (gateway, auth, OAuth, sandbox, node, skills, cron, websocket, multi-agent) already have existing term notes that are LINKED. Best-fit glossary if any future term were promoted: the agentic/LLM glossary (`acronym_glossary_*`) — not needed for st01.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review of the augmented sub-plan. 9 checkpoints:

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + raised floors (≥10 snippets, ≥10 docs), relevance-selected, each with a relevance statement | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 7 notes = 8 terms / 10–12 snippets / 10 docs; every link rendered `- [Name](relpath.md) — what; relevance: …`. No bare links. |
| CP2 | 9-GATE per batch (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7/G8 Discoverability/in-degree; single execution phase. |
| CP3 | Entry point update specified (inherited; `entry_openclaw_docs` planned at W1) | **PASS** | `## Entry Point Decision` contributes 7 rows to `entry_openclaw_docs.md` (W1 master pre-step) under a "Start / Getting Started" cluster; parent-hub wiring is master W2. |
| CP4 | Plan size (≤30 notes) | **PASS** | 7 planned notes, single phase — well under 30. |
| CP5 | Note format aligned + DERIVED from existing target-dir notes | **PASS** | Master Format Definition derived from existing `claude_code/cc_*` + `pi/pi_*` corpora (`## Overview` → mirrored body → `## Related Notes` → `## References` → bold footer); inherited verbatim by this sub-plan; G1 enforces `check_note_format.py` + `check_yaml_frontmatter.py`. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: largest note (lore) 650w est. / 2 code blocks — no note approaches ≤2,500w / ≤400L / ≤6-code caps; no borderline cases; no splits needed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured `wc -w` over all 7 `inbox/openclaw_docs/start/*.md` on 2026-06-21 = 3,421 total, matching the plan's Source table 1:1 (ratio 1.00); no under-estimation. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements present | **PASS** | `## Undigested Terms Plan` present with disposition per source term (all link-existing or in-note, 0 new); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherited mandate documented). |
| CP8f | Term-slug specificity + collision (all-notes dedup) audit | **PASS** | Master dedup policy = three-way (term_dictionary + documentation/ + repo_openclaw*); 0 new term slugs to rename; planned `oc_*` doc slugs checked against existing `term_*`/`repo_*` — no doc-note duplicates an existing term note (OpenClaw vocab → `oc_` docs by design; existing terms LINKED not recreated). |
| CP9 | Discoverability — inbound links executed (G8), no graph islands | **PASS** | `## Inlinks (existing notes → new notes)` table gives every new note ≥1 OUTSIDE-folder inbound link (guaranteed via `entry_openclaw_docs.md` W1 + reciprocal term/repo backlinks); G7/G8 is in the phase gate table as an execution gate, not a recommendation. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
