---
title: Hermes Agent Docs Digestion — Sub-Plan 17 — Guides: Build & Extend
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/guides/
pages:
  - guides/build-a-hermes-plugin.md
  - guides/automation-blueprints.md
  - guides/use-mcp-with-hermes.md
  - guides/use-voice-mode-with-hermes.md
  - guides/work-with-skills.md
  - guides/python-library.md
  - guides/use-soul-with-hermes.md
  - guides/migrate-from-openclaw.md
  - guides/tips.md
  - guides/microsoft-graph-app-registration.md
---

# Sub-Plan 17: Guides: Build & Extend

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP17's note
> filenames/BBs/coverage are defined.

## Scope

The **build-and-extend how-to layer** of the Hermes Agent docs: the end-to-end plugin-building walkthrough
(tools, hooks, slash/CLI commands, data files, bundled skills, the five specialized plugin types, and
non-Python extension surfaces), the copy-paste automation blueprint cookbook (cron + webhook recipes),
the practical how-to companions for MCP, voice mode, skills, and SOUL.md, the Python-library embedding
guide, the OpenClaw migration reference, the tips/best-practices collection, and the Microsoft Graph app
registration prerequisite. Source = 10 mirrored pages in `inbox/hermes_agent_docs/guides/` (all substantive).
**P3 / guides** — these are the *how-to-use / how-to-build* surface; they cross-link down to the existing
`repo_hermes_agent_plugins` / `snippet_hermes_agent_plugins_*` implementation layer and forward-ref the
feature-page concept notes (MCP→SP09, voice/tts→SP08, skills/soul→SP05, plugins/hooks→SP06b, providers→SP14).

## Content Strategy

- **One BB per note.** Most guides are procedure. `build-a-hermes-plugin.md` (6087w / 57 code) mixes a
  tutorial arc, an extras reference, and a specialized-types catalog → split into 3 (see Split Decisions).
  `automation-blueprints.md` splits into scheduled vs event-driven+multi-skill. The code-dense how-tos
  (mcp 33 code, voice 24, skills 16, python 15) curate to ≤6 load-bearing blocks per note.
- **Do NOT duplicate** the feature-page CONCEPTS each how-to references → **link-outs**, not copied content:
  the MCP concept (SP09 `hermes_mcp` + existing `term_mcp`), voice/TTS/STT concepts (SP08), the skills/
  SOUL.md/personality concepts (SP05), the plugin/hook concepts (SP06b), the provider catalog (SP14), the
  cron/delegation/code-exec concepts (SP06a), the webhook messaging platform (SP12).
- **Owned NEW term captures: 0.** Collision audit (below) confirms every reusable concept SP17 touches is
  either an existing substantive term (LINK) or owned by another sub-plan (forward-ref `+fin`). The plugin
  guide's reusable concepts map to the EXISTING `term_plugin_manifest` / `term_plugin_sdk` /
  `term_provider_plugin` + the SP06b-owned `term_hermes_plugin` forward-ref; no new SP17 term survives the
  three-way existence check.

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| guides/build-a-hermes-plugin.md | 6087 | 57 | MIXED procedure+model | 3 (split) |
| guides/automation-blueprints.md | 2535 | 21 | procedure | 2 (split) |
| guides/use-mcp-with-hermes.md | 1693 | 33 | procedure | 1 (curate code) |
| guides/use-voice-mode-with-hermes.md | 1499 | 24 | procedure | 1 (curate code) |
| guides/work-with-skills.md | 1310 | 16 | procedure | 1 (curate code) |
| guides/python-library.md | 1237 | 15 | procedure | 1 (curate code) |
| guides/use-soul-with-hermes.md | 1090 | 10 | procedure | 1 |
| guides/migrate-from-openclaw.md | 1949 | 2 | procedure | 1 |
| guides/tips.md | 1806 | 6 | procedure | 1 |
| guides/microsoft-graph-app-registration.md | 1160 | 5 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **13 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_build_plugin_tutorial.md` | procedure | build-plugin §What you're building, §Step 1 Create dir, §Step 2 Manifest, §Step 3 Schemas, §Step 4 Handlers, §Step 5 Registration (+dispatch_tool), §Step 6 Test (+Debugging discovery), §Final structure | ~1400 | The end-to-end calculator-plugin walkthrough: `plugin.yaml` manifest, `schemas.py`, `tools.py` handlers (signature/return-JSON/never-raise rules), `__init__.py` `register(ctx)` wiring, `ctx.dispatch_tool`, testing + `HERMES_PLUGINS_DEBUG` discovery debugging, 4-file layout. |
| 2 | `hermes_plugin_extensions_hooks.md` | procedure | build-plugin §Ship data files, §Bundle skills, §Gate on env vars, §Lazy-install deps, §Thread-safe singletons, §Conditional tool availability, §Overriding built-in, §Register multiple hooks, §Hook reference, §pre_llm_call injection, §Register CLI commands, §Register slash commands, §Dispatch tools from slash, §Slack Block Kit handlers | ~1500 | The plugin extras surface: shipping data files + bundled read-only skills, `requires_env` gating, `lazy_deps.ensure` install allowlist, `lazy_singleton`/`SingletonSlot`, `check_fn`/`override=True`, the 8 lifecycle hooks + `pre_llm_call` context injection (cache-preserving, appended to user message), `register_cli_command`/`register_command`/`dispatch_tool`/`register_slack_action_handler`. |
| 3 | `hermes_plugin_types_surfaces.md` | model | build-plugin §Specialized plugin types (model-provider/platform/memory/context-engine/image-gen), §Non-Python surfaces (MCP/gateway-hooks/shell-hooks/skill-taps/TTS-STT), §Distribute via pip, §Distribute for NixOS, §Common mistakes (+ the intro routing map) | ~1500 | The extension-surface map: the five specialized Python plugin types (model-provider, platform adapter, memory provider, context engine, image-gen) and their `register_*` contracts, plus the config-driven / drop-in non-Python surfaces (MCP servers, gateway event hooks, shell hooks, skill taps, TTS/STT command templates), pip + NixOS distribution, and the common-mistakes checklist. |
| 4 | `hermes_automation_blueprints_scheduled.md` | procedure | automation-blueprints §intro (3 trigger types), §Nightly Backlog Triage, §Docs Drift Detection, §Dependency Security Audit, §Uptime Monitor (+script), §Competitive Repo Scout, §AI News Digest, §Paper Digest, §Daily Revenue Summary, §Quick Reference (cron syntax, delivery targets, [SILENT]) | ~1300 | Copy-paste schedule-triggered blueprints: `hermes cron create` recipes (backlog triage, docs-drift, dependency audit, uptime monitor with `--script`, competitor scout, news/paper digest, revenue summary), the cron-syntax + delivery-target tables, and the `[SILENT]` no-notification pattern. |
| 5 | `hermes_automation_blueprints_event.md` | procedure | automation-blueprints §Automatic PR Code Review (dynamic + static route), §Deploy Verification, §Alert Triage, §Issue Auto-Labeling, §CI Failure Analysis, §Auto-Port Changes, §Stripe Payment Monitoring, §Security Audit Pipeline, §Content Pipeline, §Webhook Template Variables | ~1200 | Event-driven + multi-skill blueprints: `hermes webhook subscribe` vs `config.yaml` route forms, GitHub-event recipes (PR review, issue labeling, CI-failure, auto-port), generic API-webhook recipes (deploy-verify, alert-triage, Stripe), multi-skill pipelines (security audit, content), and the `{...}` webhook template-variable table. |
| 6 | `hermes_use_mcp_guide.md` | procedure | use-mcp §When to use / Mental model, §Step 1 install, §Step 2 add one server, §Step 3 verify, §Step 4 filter, §What filtering affects, §Common patterns 1-4, §Tutorial phases 1-3, §Safe usage, §WSL2 bridge to Windows Chrome, §Troubleshooting, §Recommended first setups | ~1500 | Practical MCP how-to: when/when-not to use, install `.[mcp]`, add-one-safe-server-first, `/reload-mcp` verify, `tools.include`/`exclude`/`resources`/`prompts` filtering, the four usage patterns (local-fs, GitHub triage, internal-API, docs), the tight-whitelist tutorial, the WSL2→Windows-Chrome `chrome-devtools-mcp` stdio bridge, and symptom-based troubleshooting. |
| 7 | `hermes_use_voice_mode_guide.md` | procedure | use-voice §What it's good for, §Choose setup (3 modes), §Step 1 text first, §Step 2 extras, §Step 3 sysdeps, §Step 4 STT/TTS providers, §Step 5 config, §Use case 1 CLI (+tuning), §Use case 2 messaging replies, §Use case 3 Discord VC, §Quality recs, §Failure modes, §First-week setup | ~1500 | End-to-end voice-mode how-to: the three voice experiences (CLI mic loop / chat voice replies / Discord VC), `[voice]`/`[messaging]`/`[tts-premium]` extras, system deps (portaudio/ffmpeg/opus/espeak-ng), STT (local/groq/openai) + TTS (edge/neutts/elevenlabs) provider picks, the recommended `voice`/`stt`/`tts` YAML, `/voice` command set + silence tuning, Discord-VC permissions/intents, and failure-mode triage. |
| 8 | `hermes_work_with_skills_guide.md` | procedure | work-with-skills §Finding skills, §Searching, §Skills Hub, §Using a skill, §Progressive Disclosure, §Installing from Hub, §Verifying, §Plugin-provided skills, §Configuring skill settings, §Creating your own (4 steps), §Per-platform mgmt, §Skills vs Memory, §Tips | ~1300 | Day-to-day skills how-to: `/skills` list/search/browse, every installed skill is a slash command, the three-tier progressive-disclosure loading (`skills_list`/`skill_view(name)`/`skill_view(name,file)`), Hub install (`official/...` + HTTP(S) URL), namespaced `plugin:skill` loads, frontmatter `metadata.hermes.config`, the under-5-min create-your-own (`~/.hermes/skills/<cat>/<name>/SKILL.md`), per-platform TUI management, and skills-vs-memory routing. |
| 9 | `hermes_python_library_guide.md` | procedure | python-library §Installation, §Basic Usage (chat), §Full Conversation Control (run_conversation), §Configuring Tools, §Multi-turn, §Saving Trajectories, §Custom System Prompts, §Batch Processing, §Integration Examples (FastAPI/Discord/CI), §Key Constructor Parameters, §Important Notes | ~1300 | Embedding `AIAgent` as a Python library: `pip install git+…`, `agent.chat()` vs `run_conversation()` (returns `final_response`+`messages`), `enabled/disabled_toolsets`, multi-turn via `conversation_history`, `save_trajectories` (ShareGPT JSONL), `ephemeral_system_prompt`, `batch_runner.py` + per-thread instance rule, FastAPI/Discord/CI examples, the constructor-parameter table, and `quiet_mode`/`skip_memory`/thread-safety notes. |
| 10 | `hermes_use_soul_md_guide.md` | procedure | use-soul §What it's for / not for, §Where it lives, §First-run behavior, §How Hermes uses it, §A good first edit, §Example styles (4), §What makes a strong SOUL, §Suggested structure, §SOUL vs /personality, §SOUL vs AGENTS.md, §How to edit, §Practical workflow, §Troubleshooting | ~1100 | Using `SOUL.md` as the instance identity: it is system-prompt slot #1 (replaces the default identity), `~/.hermes/SOUL.md` / `$HERMES_HOME/SOUL.md`, auto-seeded starter (never overwrites yours), prompt-injection scan + truncation on load, four example voices, strong-vs-weak guidance, the SOUL-vs-`/personality` (durable vs temporary) and SOUL-vs-`AGENTS.md` (identity vs project) splits, and troubleshooting. |
| 11 | `hermes_migrate_from_openclaw.md` | procedure | migrate §Quick start, §Options, §What gets migrated (persona/memory, skills, model/provider, agent behavior, session reset, MCP, TTS, messaging, other), §Archived, §API key resolution, §SecretRef handling, §After migration, §Troubleshooting | ~1700 | The `hermes claw migrate` reference: dry-run/preview/`--preset`/`--migrate-secrets` flags, the full OpenClaw→Hermes config-key mapping tables (SOUL/MEMORY/AGENTS, the 4 skill sources, model/provider/behavior/session-reset/MCP/TTS/messaging-platform keys), archived-for-manual-review items, four-source API-key resolution, the three SecretRef formats, the post-migration checklist (re-pair WhatsApp, `claw cleanup`), and troubleshooting. |
| 12 | `hermes_tips_best_practices.md` | procedure | tips §Getting Best Results, §CLI Power User Tips, §Context Files (AGENTS.md/SOUL.md/.cursorrules/discovery), §Memory & Skills, §Performance & Cost, §Messaging Tips, §Security | ~1500 | The practical best-practices collection: prompt specificity + tool autonomy, CLI shortcuts (multiline keys, paste detection, `Ctrl+C` interrupt, `-c`/`-r` resume, clipboard image, `/` Tab autocomplete, `/verbose`), `AGENTS.md`/`SOUL.md`/`.cursorrules` context files, memory-vs-skills routing + capacity, cost levers (prompt-cache, `/compress`, `delegate_task`, `execute_code`, `/model`), messaging tips (`/sethome`, `/title`, DM pairing), and the security do's (Docker for untrusted, allowlists, review-before-"always"). |
| 13 | `hermes_msgraph_app_registration.md` | procedure | msgraph-app-reg §Prerequisites, §Step 1 App registration, §Step 2 Client secret, §Step 3 Graph API permissions (transcript/recording/delivery), §Step 4 Application Access Policy, §Step 5 Write env, §Step 6 Verify token flow, §Rotating secret, §Next steps | ~1100 | The Azure-portal app-registration prerequisite for the Teams meeting pipeline: app-only (client-credentials) registration, client-secret creation (`MSGRAPH_*` env vars), the minimum-viable Graph application permissions (`OnlineMeeting*.Read.All`, `CallRecords.Read.All`, `ChannelMessage.Send`) + admin consent, the PowerShell Application Access Policy scoping, the `MicrosoftGraphTokenProvider` smoke test + Azure error-code table, and secret rotation. |

**SP17 totals:** 13 notes · procedure 12 · model 1 · concept 0 (concepts owned by existing/other-SP term notes).
10 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 13 · procedure 12 · model 1 · concept 0 (plugin/MCP/voice/skill/SOUL concepts are existing or other-SP term notes).
- Source: 10 digested pages (~20.4K words) → ~17.7K words of notes (modest compression via link-outs to feature/concept pages).
- BB mix: procedure 92%, model 8%.

## Section Coverage Map

```
build-a-hermes-plugin.md (6087w)
├── intro routing map ("If you want to add…") ────────────── → Note 3 (extension-surface map)
├── What you're building / Step 1-6 (manifest/schemas/handlers/register/test/debug) → Note 1
├── Final structure ──────────────────────────────────────── → Note 1
├── Ship data files / Bundle skills / Gate env / Lazy deps / Singletons → Note 2
├── Conditional availability / Override / Register hooks / Hook reference / pre_llm_call injection → Note 2
├── Register CLI commands / slash commands / Dispatch tools / Slack handlers → Note 2
├── Specialized plugin types (5) ─────────────────────────── → Note 3
├── Non-Python surfaces (MCP/gateway-hooks/shell-hooks/skill-taps/TTS-STT) → Note 3 (each concept→owning SP)
├── Distribute via pip / Distribute for NixOS ────────────── → Note 3 (NixOS deep→SP01)
└── Common mistakes ──────────────────────────────────────── → Note 3
automation-blueprints.md (2535w)
├── intro (3 trigger types) / Quick Reference (cron/delivery/[SILENT]) → Note 4
├── Development Workflow (backlog triage, docs-drift, dep audit) → Note 4 (PR review→Note 5)
├── DevOps & Monitoring (deploy-verify, alert-triage, uptime) → mixed: uptime→Note 4; deploy/alert→Note 5
├── Research & Intelligence (repo scout, news digest, paper, revenue) → Note 4
├── Automatic PR Code Review / GitHub Event Automations (labeling, CI, auto-port) → Note 5
├── Business Operations (Stripe) ─────────────────────────── → Note 5
└── Multi-Skill Workflows (security audit, content) ──────── → Note 5 (cron concept→SP06a; webhook→SP12)
use-mcp-with-hermes.md (1693w) ── ALL sections ───────────── → Note 6 (MCP concept→SP09 hermes_mcp; WSL2 deep→SP03)
use-voice-mode-with-hermes.md (1499w) ── ALL sections ────── → Note 7 (voice/tts concept→SP08; discord→SP11)
work-with-skills.md (1310w) ── ALL sections ──────────────── → Note 8 (skills concept→SP05; bundle-skills→Note 2)
python-library.md (1237w) ── ALL sections ────────────────── → Note 9 (programmatic internals→SP19; batch→SP06a)
use-soul-with-hermes.md (1090w) ── ALL sections ──────────── → Note 10 (SOUL concept→SP05 personality; AGENTS.md→SP05)
migrate-from-openclaw.md (1949w) ── ALL sections ─────────── → Note 11 (nous-portal→SP14; honcho→SP05)
tips.md (1806w) ── ALL sections ──────────────────────────── → Note 12 (each tip's feature→owning SP)
microsoft-graph-app-registration.md (1160w) ── ALL sections → Note 13 (teams pipeline→SP11/SP12; oauth→SP09)
```

No source H2/H3 orphaned. All 10 pages fully covered; feature/concept detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| build-a-hermes-plugin.md (6087w, 57 code, MIXED) | Note 1 (tutorial, proc) + Note 2 (extras/hooks/commands, proc) + Note 3 (specialized types + surfaces, model) | >4000w → 3 notes; three distinct arcs — the step-by-step calculator tutorial, the extras/hooks/command-registration reference, and the extension-surface catalog (a distinct `model` BB enumerating plugin types + drop-in surfaces). 57 source code blocks curated to ≤6 load-bearing per note. |
| automation-blueprints.md (2535w, 21 code) | Note 4 (schedule-triggered + quick ref) + Note 5 (event-driven + multi-skill) | >2500w; two trigger families — `cron create` recipes vs `webhook subscribe`/route recipes. 21 blocks curated to ≤6 canonical recipes per note. |

Code-only splits (kept as 1 note each, code curated to ≤6 from the source count): mcp (33→≤6), voice (24→≤6),
skills (16→≤6), python-library (15→≤6) — each is a single topically-cohesive procedure ≤1500w, so no BB-split
is warranted; the load-bearing YAML/Python blocks are kept verbatim and the rest summarized in prose.

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_build_plugin_tutorial`, `hermes_plugin_extensions_hooks` | `term_plugin_manifest.md` (active), `term_plugin_sdk.md` (active), `term_hermes_plugin` (SP06b-owned, not yet existing) | **NOT a dup** — those terms are the plugin *concepts*; these are the build *procedures* | CREATE; LINK `term_plugin_manifest`/`term_plugin_sdk`; forward-ref `term_hermes_plugin`/`term_gateway_hooks` (+fin SP06b). |
| `hermes_plugin_types_surfaces` | `term_provider_plugin.md` (active), `term_mcp.md` (active), `term_skill_manifest` (active) | **NOT a dup** — model note enumerating the 5 plugin types + drop-in surfaces; component concepts only | CREATE; LINK the component terms. |
| `hermes_use_voice_mode_guide` | `term_voice_call.md` (active), `term_voice_wake.md` (active); `term_voice_mode`/`term_text_to_speech`/`term_speech_to_text` (SP08-owned, not yet existing) | **NOT a dup** — `voice_wake`/`voice_call` are different concepts (master false-positive caution `voice mode ≠ term_voice_wake`); this is the usage how-to | CREATE; LINK `term_voice_wake`; forward-ref SP08 terms (+fin). |
| `hermes_work_with_skills_guide` | `term_skills.md` (active), `term_skill_manifest.md` (active); `term_skills_hub`/`term_progressive_disclosure`/`term_skill_curator` (SP05-owned) | **NOT a dup** — terms are skill concepts; this is the day-to-day usage how-to | CREATE; LINK `term_skills`/`term_skill_manifest`; forward-ref SP05 terms (+fin). |
| `hermes_python_library_guide` | `term_plugin_sdk.md`, `term_strands_agents_sdk.md`, `term_aws_sdk_credential_chain.md` (all unrelated SDKs) | **NOT a dup** — none cover embedding `AIAgent`; no `term_python_library` / `term_python_sdk` exists | CREATE; LINK component concepts (`term_function_calling`, `term_agent_orchestration`). |
| `hermes_use_soul_md_guide` | none substantive (`term_soul_md` SP05-owned, not yet existing); `term_persona.md` (active) | **NOT a dup** — SOUL concept owned by SP05; this is the usage how-to | CREATE; LINK `term_persona`; forward-ref `term_soul_md`/`term_agents_md` (+fin SP05). |
| `hermes_migrate_from_openclaw` | `thought_hermes_agent_vs_openclaw.md` (active, a *comparison*) | **NOT a dup** — that is an analysis/argument note, not the migration procedure | CREATE; cross-link the thought note as related. |
| `hermes_tips_best_practices`, `hermes_automation_blueprints_scheduled`, `hermes_automation_blueprints_event`, `hermes_msgraph_app_registration` | no substantive term/doc note covers these procedures; no `hermes_agent/` doc notes exist yet | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the plugin/mcp/skills/voice term hits are component-concept LINKs,
not dups; `voice_wake`/`voice_call` are confirmed different concepts per the master caution list;
`thought_hermes_agent_vs_openclaw` is a comparison not a procedure). The `resources/documentation/hermes_agent/`
at finalization (G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Floor RAISED 2026-06-19 (master FOUR-FLOOR directive — supersedes the 2026-06-15 and prior floors):**
> each note's `## Related Notes` now carries FOUR COUNTED floors, all relevancy-selected to that note's
> actual content and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   the Hermes SOURCE-CODE modules that implement what THIS doc note documents (all 13 `repo_hermes_agent_*`
>   notes exist and are active; pick the ones whose modules implement the surface this note describes).
>   NOW A COUNTED FLOOR (promoted from the prior "bonus" group and raised from ≥8 to ≥10); the implementation
>   code paths THIS note documents, selected by the page's content.
> - **≥10 DOCUMENTATION notes** (`../../documentation/`, sibling `hermes_*` in this series + analogous
>   `claude_code/cc_*` agent-tool docs + other relevant existing doc notes) — relevancy-selected, **each
>   rendered as an indexed markdown link `- [Name](path.md) — what-it-is; relevance: …`** (NOT bare names).
>   Every note carries **12** such doc links (5 `hermes_*` siblings + 7 `cc_*`/`thought_*`), over the ≥10 floor.
>
> `snippet_hermes_agent_` prefix (shown without prefix per the SP01/SP02 exemplar convention). Intra-series
> `hermes_*` doc links resolve at finalization (G5/G8) — they are allowed un-verified here (created later).
> New Hermes-specific terms owned by other SPs (e.g. `term_hermes_plugin`→SP06b [own],
> `term_soul_md`/`term_skills_hub`→SP05 [own], `term_voice_mode`/`term_text_to_speech`→SP08 [own],
> `term_nous_portal`→SP14 [own]) are ADDITIONAL forward-refs (+fin), EXCLUDED from the ≥8 term floor (they
> don't exist yet). The prior floor was ≥8 term / ≥5 code-repo / ≥10 doc with snippets as a bonus group;
> snippets are NO LONGER a bonus — they are now a counted ≥10 floor.

**Note 1 `hermes_build_plugin_tutorial`**
- Terms (8): term_plugin_manifest, term_plugin_sdk, term_function_calling, term_event_driven_architecture, term_agent_harness, term_autonomous_coding_agents, term_skill_manifest, term_observer_pattern — relevance: the tutorial builds a `plugin.yaml` manifest + `schemas.py` tool schemas (function-calling descriptions the LLM reads) + `tools.py` handlers + `__init__.py` `register(ctx)`, wired into the harness; the `post_tool_call` hook the tutorial registers is an observer on the event bus; the bundled-skill step ships a SKILL.md manifest. (+fin: term_hermes_plugin [own SP06b])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — the plugin system (discovery, `register(ctx)` PluginContext, manifest loader); relevance: implements the exact `register_tool`/`register_hook` API the tutorial calls. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry + schema handling; relevance: `ctx.register_tool` lands a tool here and the LLM-facing schema is sanitized by this module. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent loop + tool dispatch; relevance: implements `ctx.dispatch_tool` and the tool-calling loop the calculator tools run in. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes plugins list/enable` + `HERMES_PLUGINS_DEBUG` discovery logs; relevance: the Step-6 testing + discovery-debugging commands live here. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level repo / `~/.hermes/plugins/` layout; relevance: the 4-file plugin directory layout and startup `register()` call are rooted here.
- Snippets (10): plugins_manifest_schema, plugins_namespace_init, plugins_sdk_architecture, plugins_interfaces_abcs, tools_registry, tools_schema_sanitizer, core_tool_dispatch_helpers, cli_plugins_discover, cli_plugins_install, cli_plugins_cmd_list_info — relevance: the manifest-schema loader, plugin-namespace `register(ctx)`, SDK architecture + interface ABCs, tool-registry registration + LLM-facing schema sanitizer, the `dispatch_tool` helper the calculator tools run through, and the `hermes plugins` discovery/install/list code paths this Step-1→6 tutorial drives.
- Docs (12): [hermes_plugin_extensions_hooks](hermes_plugin_extensions_hooks.md) — the plugin extras/hooks/commands surface; relevance: the immediate continuation of this tutorial (data files, hooks, CLI/slash commands the same plugin can add). · [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md) — the typed-plugin + drop-in surface map; relevance: the five specialized plugin types beyond the general calculator-plugin this tutorial builds. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills authoring/loading; relevance: the tutorial's bundled-skill (`register_skill`) step ships a SKILL.md documented here. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage how-to; relevance: the non-Python MCP extension surface as an alternative to a Python plugin. · [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: programmatic library route vs the CLI plugin this tutorial builds. · [cc_plugin_quickstart](../claude_code/cc_plugin_quickstart.md) — Claude Code's build-your-first-plugin walkthrough; relevance: closest analogue to this end-to-end tutorial. · [cc_plugin_components](../claude_code/cc_plugin_components.md) — CC plugin file/component layout; relevance: analogue to the 4-file plugin structure. · [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — CC plugin manifest fields; relevance: analogue to the `plugin.yaml` manifest step. · [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — defining a custom tool + schema in the CC SDK; relevance: analogue to `schemas.py`/`tools.py` handler authoring. · [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — CC extension-surface overview; relevance: analogue to "what else can plugins do". · [cc_plugin_directory_structure](../claude_code/cc_plugin_directory_structure.md) — CC plugin on-disk directory layout; relevance: analogue to the tutorial's `~/.hermes/plugins/<name>/` 4-file directory. · [cc_sdk_plugin_structure](../claude_code/cc_sdk_plugin_structure.md) — CC SDK plugin package structure + registration; relevance: analogue to the `__init__.py` `register(ctx)` wiring step.

**Note 2 `hermes_plugin_extensions_hooks`**
- Terms (8): term_observer_pattern, term_event_driven_architecture, term_plugin_manifest, term_singleton, term_prompt_caching, term_human_in_the_loop, term_function_calling, term_skill_manifest — relevance: the 8 lifecycle hooks are observers on an event bus; `pre_llm_call` injection preserves prompt cache; singletons guard thread-safe lazy state; bundled skills ship via the skill manifest. (+fin: term_gateway_hooks [own SP06b], term_skills_hub [own SP05])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin system + `register_*` API; relevance: hosts `register_cli_command`/`register_command`/`register_slack_action_handler` + the lazy-dep/singleton helpers this note documents. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway event-hook dispatch + Slack Block Kit; relevance: the gateway/shell hook firing and Slack button-click handler land here. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — conversation loop + `pre_llm_call`/`post_tool_call` hook points; relevance: implements the cache-preserving message injection this note describes. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry + lazy-deps; relevance: `lazy_deps.ensure` install allowlist + conditional `check_fn` tool availability live here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI subcommand registration; relevance: `register_cli_command` extends the `hermes` CLI from a plugin.
- Snippets (10): gw_hooks, core_shell_hooks_allowlist, core_shell_hooks_callback, conv_loop_post_api_hook, plugins_browser_dispatch, tools_lazy_deps, plugins_namespace_init, tools_registry, tools_send_dispatch, core_prompt_caching — relevance: the gateway hook dispatch, shell-hook allowlist/callback, post-API hook, plugin tool-dispatch, lazy-dep install, registry registration, Slack-action outbound send, and the prompt-cache boundary the `pre_llm_call` injection preserves.
- Docs (12): [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the calculator-plugin walkthrough; relevance: this note extends that tutorial with the extras/hooks/command-registration surface. · [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md) — typed-plugin + drop-in surfaces; relevance: the hooks/commands here are the general surface, the typed plugins are the specialized one. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills authoring/loading; relevance: the bundled read-only skills a plugin ships are documented here. · [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event-driven automation; relevance: gateway/shell hooks drive the event automations there. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the non-Python hook/tool alternative to these plugin extras. · [cc_hooks_overview](../claude_code/cc_hooks_overview.md) — CC hooks model; relevance: analogue to the 8 lifecycle hooks. · [cc_hook_events_catalog](../claude_code/cc_hook_events_catalog.md) — CC hook-event list; relevance: analogue to the hook reference. · [cc_prompt_and_agent_hooks](../claude_code/cc_prompt_and_agent_hooks.md) — CC pre-prompt/agent hooks; relevance: analogue to `pre_llm_call` injection. · [cc_cache_preserving_actions](../claude_code/cc_cache_preserving_actions.md) — CC cache-preserving edits; relevance: analogue to injection that doesn't break the prompt cache. · [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — CC extension surfaces; relevance: analogue to the plugin extras catalog. · [cc_async_hooks](../claude_code/cc_async_hooks.md) — CC async/non-blocking hook execution; relevance: analogue to thread-safe singleton + lazy-dep hook handlers. · [cc_hooks_common_recipes](../claude_code/cc_hooks_common_recipes.md) — CC hook recipe cookbook; relevance: analogue to the register-multiple-hooks + conditional-availability patterns.

**Note 3 `hermes_plugin_types_surfaces`** (model)
- Terms (8): term_provider_plugin, term_plugin_sdk, term_mcp, term_skill_manifest, term_event_driven_architecture, term_observer_pattern, term_function_calling, term_plugin_manifest — relevance: enumerates the five typed plugin contracts (provider/platform/memory/context-engine/image-gen) plus the config-driven/drop-in surfaces (MCP, hooks, skill taps, TTS/STT) and their registration model. (+fin: term_hermes_plugin [own SP06b], term_tool_gateway [own SP05])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin-type registries (provider/memory/context-engine/image-gen discovery); relevance: implements the five typed `register_*` contracts this model enumerates. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — model-provider + TTS/STT adapters; relevance: the model-provider plugin type and the config-driven TTS/STT command templates map here. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — platform adapters + gateway event hooks; relevance: the platform-plugin type and drop-in gateway hooks live here. · [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP-server toolset surface; relevance: the config-driven MCP non-Python surface in the map. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry + lazy-deps; relevance: every typed plugin lands tools through this registry, gated by `lazy_deps`.
- Snippets (10): plugins_interfaces_abcs, plugins_provider_registry, plugins_memory_discovery, plugins_context_engine_discovery, plugins_image_gen_dispatch, plugins_video_gen_dispatch, plugins_platform_irc, cli_mcp_config, core_shell_hooks_callback, tools_lazy_deps — relevance: the plugin-interface ABCs, provider/memory/context-engine/image/video discovery + dispatch, the IRC reference platform adapter, the MCP-server config surface, the shell-hook callback surface, and the lazy-dep gating this map enumerates.
- Docs (12): [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the general calculator-plugin walkthrough; relevance: the general plugin surface this model contrasts with the five specialized types. · [hermes_plugin_extensions_hooks](hermes_plugin_extensions_hooks.md) — the extras/hooks/commands layer; relevance: the registration extras every typed plugin can also use. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage how-to; relevance: the MCP non-Python drop-in surface enumerated in this map. · [hermes_use_voice_mode_guide](hermes_use_voice_mode_guide.md) — voice-mode setup; relevance: the TTS/STT command-template drop-in surface in this map. · [hermes_install_nixos_module](hermes_install_nixos_module.md) — NixOS install module; relevance: the NixOS plugin-distribution surface this model points to. · [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — CC extension-surface map; relevance: closest analogue to this surface catalog. · [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — CC plugin-type overview; relevance: analogue to the typed plugin contracts. · [cc_plugin_components](../claude_code/cc_plugin_components.md) — CC component types (commands/agents/hooks/MCP); relevance: analogue to the surface catalog. · [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — CC MCP-server surface; relevance: analogue to the MCP drop-in surface. · [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — CC SDK plugin loading; relevance: analogue to programmatic plugin registration. · [cc_model_selection](../claude_code/cc_model_selection.md) — CC model-provider selection; relevance: analogue to the model-provider plugin type in this map. · [cc_sdk_skills](../claude_code/cc_sdk_skills.md) — CC SDK skill taps; relevance: analogue to the skill-tap drop-in surface in the map.

**Note 4 `hermes_automation_blueprints_scheduled`**
- Terms (8): term_cron, term_autonomous_coding_agents, term_agent_orchestration, term_skills, term_agent_harness, term_subagent, term_function_calling, term_idempotency — relevance: each blueprint is a scheduled `cron create` job that runs the agent with skills/tools; the `[SILENT]` pattern makes runs idempotently quiet. (+fin: term_persistent_goal [own SP06a])
- Code-Repos (5): [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — cron scheduler/CRUD/tick + `--script` execution; relevance: every `hermes cron create` recipe in this note is implemented here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes cron` command surface; relevance: the CLI flags (`--schedule`/`--script`/`--deliver`) the recipes type. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — delivery-target routing + `[SILENT]`; relevance: cron runs deliver via the gateway to a channel/DM. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent run each cron job invokes; relevance: each blueprint prompt runs the AIAgent loop. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills the blueprints invoke (triage/digest/audit); relevance: blueprints lean on installed skills for repeatable work.
- Snippets (10): cron_job_crud, cron_job_schema, cron_job_validate, cli_cron, cron_run_job_execute, cron_run_job_setup, cron_tick, gw_runner_cron, gw_delivery, core_run_agent_cli — relevance: the cron CRUD/schema/validation/scheduler/tick/execute code, the gateway cron runner + delivery, and the agent-run entry point these `--script`/`--deliver` recipes drive.
- Docs (12): [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event-driven blueprints; relevance: the webhook-triggered sibling to these schedule-triggered recipes. · [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: cost/security tips for unattended cron runs. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: the installed skills (triage/digest/audit) the blueprints invoke. · [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: the programmatic batch alternative to a cron job. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the MCP tools the blueprint prompts use inside cron jobs. · [cc_routines_overview](../claude_code/cc_routines_overview.md) — CC scheduled-routine model; relevance: closest analogue to `hermes cron`. · [cc_create_routine](../claude_code/cc_create_routine.md) — creating a CC scheduled routine; relevance: analogue to `cron create`. · [cc_routine_triggers](../claude_code/cc_routine_triggers.md) — schedule/trigger config; relevance: analogue to cron syntax + delivery targets. · [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — how scheduled tasks execute; relevance: analogue to the cron `--script` run model. · [cc_automate_and_scale](../claude_code/cc_automate_and_scale.md) — CC automation patterns; relevance: analogue to the blueprint cookbook. · [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — CC recurring/loop scheduled tasks; relevance: analogue to the recurring nightly/daily cron blueprints. · [cc_manage_routines](../claude_code/cc_manage_routines.md) — CC routine CRUD/management; relevance: analogue to `hermes cron list/delete` lifecycle.

**Note 5 `hermes_automation_blueprints_event`**
- Terms (8): term_event_driven_architecture, term_cron, term_autonomous_coding_agents, term_skills, term_agent_orchestration, term_subagent, term_access_control, term_idempotency — relevance: webhook routes are event-driven triggers that template the payload into an agent prompt; multi-skill pipelines orchestrate skills; secret/allowlist gates protect endpoints. (+fin: term_messaging_gateway [own SP11], term_webhook [existing])
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — webhook platform routes + payload normalization; relevance: `hermes webhook subscribe` and the `config.yaml` route forms land here. · [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — webhook→job registration + handoff; relevance: an event route registers a cron-style job that runs the agent. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the devops/security/content skills the multi-skill pipelines chain; relevance: PR-review/labeling/CI-failure recipes invoke these skills. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent run each webhook fires; relevance: the templated payload becomes an agent prompt. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes webhook` command surface; relevance: the subscribe/route CLI the recipes type.
- Snippets (10): gw_platform_webhook, gw_platform_msgraph_webhook, skills_devops_webhook, skills_devops_kanban_orchestrator, cron_job_crud, tools_cronjob_register, tools_cronjob_handoff, gw_delivery, cli_cron, gw_runner_cron — relevance: the webhook platform route handling, MS-Graph webhook, devops-webhook + kanban-orchestrator skills, cron registration/handoff, and delivery code these GitHub-event/API-webhook/multi-skill recipes drive.
- Docs (12): [hermes_automation_blueprints_scheduled](hermes_automation_blueprints_scheduled.md) — schedule-triggered blueprints; relevance: the `cron`-triggered sibling to these webhook/event recipes. · [hermes_msgraph_app_registration](hermes_msgraph_app_registration.md) — Azure app registration; relevance: the MS-Graph webhook prerequisite for the Teams-event pipeline. · [hermes_plugin_extensions_hooks](hermes_plugin_extensions_hooks.md) — plugin hooks/commands; relevance: gateway/shell hooks are an alternate in-process event surface. · [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: allowlist/secret security tips for public webhook endpoints. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the MCP tools used inside the multi-skill pipelines. · [cc_github_actions](../claude_code/cc_github_actions.md) — CC GitHub-event automation; relevance: closest analogue to the PR-review/labeling recipes. · [cc_workflow_recipes](../claude_code/cc_workflow_recipes.md) — CC workflow cookbook; relevance: analogue to the blueprint recipes. · [cc_create_and_run_workflows](../claude_code/cc_create_and_run_workflows.md) — building multi-step CC workflows; relevance: analogue to multi-skill pipelines. · [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — CC dynamic/event-driven workflows; relevance: analogue to webhook-triggered runs. · [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — dispatching background agents on events; relevance: analogue to event-fired agent runs. · [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — CC parallel agent runs; relevance: analogue to multi-skill pipelines fanning out per event. · [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — CC multi-agent orchestration; relevance: analogue to the security-audit/content multi-skill pipelines.

**Note 6 `hermes_use_mcp_guide`**
- Code-Repos (5): [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP client/lifecycle/toolset surface; relevance: implements add-server, `/reload-mcp`, and the toolset-discovery this how-to drives. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — MCP call/OAuth/retry tool code; relevance: `tools_mcp_*` (call/oauth/retry/notifications) live here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `mcp_servers.*` config + `hermes tools` filtering; relevance: the `include`/`exclude`/`resources` filtering CLI and config parsing. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent loop that calls MCP-contributed tools; relevance: discovered MCP tools enter the tool-calling loop here. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level config/`.[mcp]` extras install; relevance: the `pip install .[mcp]` + WSL2 bridge setup is rooted here.
- Snippets (10): cli_mcp_config, tools_mcp_client, tools_mcp_call, tools_mcp_lifecycle, tools_mcp_notifications, tools_mcp_oauth, tools_mcp_oauth_manager, tools_mcp_retry, mcp_serve_tool_surface, skills_mcp_native — relevance: the MCP config, client/call/lifecycle/notification/OAuth(+manager)/retry code paths, the served tool surface, and the native MCP skill the `mcp_servers.*` declarations and `/reload-mcp` drive.
- Docs (12): [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the plugin walkthrough; relevance: MCP as a non-Python plugin surface alternative to a Python plugin. · [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md) — the surface map; relevance: MCP is one of the config-driven drop-in surfaces enumerated there. · [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the scoped-allowlist MCP security tips. · [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event automation; relevance: MCP tools invoked inside webhook-triggered pipelines. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: MCP-native skills the agent loads. · [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — CC MCP model; relevance: closest analogue to the MCP mental model. · [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — add-an-MCP-server walkthrough; relevance: analogue to Step 1–3. · [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — managing/reloading MCP servers; relevance: analogue to `/reload-mcp`. · [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — filtering MCP tools; relevance: analogue to `tools.include`/`exclude`. · [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — remote MCP OAuth; relevance: analogue to remote-server OAuth auth. · [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — CC MCP stdio/SSE/HTTP transports; relevance: analogue to the WSL2→Windows-Chrome stdio bridge transport. · [cc_mcp_installation_scopes](../claude_code/cc_mcp_installation_scopes.md) — CC MCP install scopes; relevance: analogue to per-server config placement (`mcp_servers.*`).

**Note 7 `hermes_use_voice_mode_guide`**
- Terms (8): term_voice_wake, term_multimodal, term_autonomous_coding_agents, term_agent_harness, term_session_persistence, term_function_calling, term_persona, term_computer_vision — relevance: voice mode is a multimodal STT→agent→TTS loop over the harness; the CLI mic loop and Discord-VC bot are alternate front-ends to the same session pipeline. (+fin: term_voice_mode, term_text_to_speech, term_speech_to_text [own SP08])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — voice-mode tool + transcription (STT) + TTS routing; relevance: `tools_voice_mode`/`tools_transcription`/`tools_tts_routing` (the STT/TTS provider picks) live here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `/voice` CLI command + mic loop + silence tuning; relevance: Use-case-1 CLI mic loop and the `/voice` command set are implemented here. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — Discord/Telegram voice replies + Discord-VC; relevance: Use-cases 2–3 (messaging voice replies, Discord voice channel) route through the gateway. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — STT/TTS provider adapters (groq/openai/edge/elevenlabs/neutts); relevance: the Step-4 provider-pick matrix maps to these adapters. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent run between STT and TTS; relevance: the transcribed prompt runs the AIAgent loop, then the reply is spoken.
- Snippets (10): cli_voice, tools_voice_mode, tools_transcription, tools_tts_routing, core_run_agent_cli, gw_delivery, gw_platform_discord_connect, cli_setup_skills, cli_setup_verify, core_conversation_loop_session_persist — relevance: the CLI voice command, voice-mode tool, transcription, TTS routing, agent-run/delivery, Discord connect (VC join), setup wizard/verify, and session-persist code the `/voice` commands and three voice experiences drive.
- Docs (12): [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the messaging/voice tips (`/sethome`, DM pairing) that apply to voice replies. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the MCP tools the agent calls inside a voice session. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: skills invoked by a voice command. · [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md) — the surface map; relevance: the TTS/STT command-template drop-in surface this guide configures. · [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: the programmatic alternative to the CLI mic loop. · [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — CC voice dictation (STT front-end); relevance: closest analogue to the CLI mic loop. · [cc_computer_use](../claude_code/cc_computer_use.md) — CC multimodal input; relevance: analogue to the multimodal STT→agent loop. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC tool catalog; relevance: analogue to the voice/transcription tools. · [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — front-ends sharing one agent session; relevance: analogue to the CLI/Discord/messaging front-ends over one pipeline. · [cc_effective_prompting](../claude_code/cc_effective_prompting.md) — spoken-prompt clarity; relevance: analogue to the voice quality/failure-mode guidance. · [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — CC full tool catalog; relevance: analogue to the STT/TTS provider/tool catalog this guide selects from. · [cc_input_modes_and_editing](../claude_code/cc_input_modes_and_editing.md) — CC input modes; relevance: analogue to the voice vs text input mode choice + silence tuning.

**Note 8 `hermes_work_with_skills_guide`**
- Terms (8): term_skills, term_skill_manifest, term_agentic_memory, term_progressive_summarization, term_autonomous_coding_agents, term_agent_harness, term_function_calling, term_few_shot_learning — relevance: skills are on-demand procedural knowledge loaded via `skill_view` (progressive disclosure ≈ token-efficient lazy load); the skills-vs-memory split distinguishes procedure from fact. (+fin: term_skills_hub, term_progressive_disclosure, term_skill_curator [own SP05])
- Code-Repos (5): [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skill loading/discovery/canonical-format + Hub taps; relevance: `/skills` list/search/browse, install, and the SKILL.md canonical format are implemented here. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `skill_view`/invoke + hub-install + skills guard; relevance: the three-tier progressive-disclosure loading tools live here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes skills install`/`hub` + per-platform mgmt; relevance: the install/hub CLI and TUI management. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin-provided skills; relevance: namespaced `plugin:skill` loads come from the plugin layer. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — skills snapshot in the system prompt + skills-vs-memory routing; relevance: the agent decides when to load a skill vs recall memory.
- Snippets (10): cli_skills_install, cli_skills_hub, tools_skills_invoke, tools_skill_manager, tools_skills_hub_install, tools_skills_guard, core_skill_commands_discovery, core_skill_utils_frontmatter, skills_canonical_format, skills_index_cache — relevance: the skills install/hub/invoke/manage/guard/discovery/frontmatter/canonical-format/index-cache code the `/skills` commands and SKILL.md authoring drive.
- Docs (12): [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the plugin walkthrough; relevance: the bundled-skill build step that ships a SKILL.md from a plugin. · [hermes_plugin_extensions_hooks](hermes_plugin_extensions_hooks.md) — plugin extras; relevance: plugin-provided skills loaded as `plugin:skill`. · [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the skills-vs-memory + when-to-create-a-skill tips. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: MCP-native skills the agent can load. · [hermes_use_soul_md_guide](hermes_use_soul_md_guide.md) — SOUL.md identity; relevance: SOUL (identity) vs skills (procedure) routing. · [cc_skills_overview](../claude_code/cc_skills_overview.md) — CC skills model; relevance: closest analogue. · [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — authoring a CC skill; relevance: analogue to the create-your-own SKILL.md. · [cc_skill_frontmatter_reference](../claude_code/cc_skill_frontmatter_reference.md) — CC skill frontmatter; relevance: analogue to `metadata.hermes.config`. · [cc_skill_invocation_and_lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — CC skill load/invoke; relevance: analogue to progressive disclosure. · [cc_bundled_skills](../claude_code/cc_bundled_skills.md) — CC plugin-bundled skills; relevance: analogue to plugin-provided skills. · [cc_skill_arguments_and_substitutions](../claude_code/cc_skill_arguments_and_substitutions.md) — CC skill argument substitution; relevance: analogue to invoking an installed skill as a slash command with args. · [cc_skill_dynamic_context_and_subagent](../claude_code/cc_skill_dynamic_context_and_subagent.md) — CC skill dynamic context loading; relevance: analogue to the three-tier `skill_view(name,file)` progressive-disclosure load.

**Note 9 `hermes_python_library_guide`**
- Terms (8): term_agent_orchestration, term_function_calling, term_autonomous_coding_agents, term_agent_harness, term_multi_agent_systems, term_session_persistence, term_context_window, term_idempotency — relevance: `AIAgent` is the programmatic harness — `run_conversation` runs the orchestration loop, `conversation_history` persists session state, `batch_runner` fans out isolated agents, `max_iterations` bounds the loop. (+fin: term_agent_trajectory [own SP06])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` orchestrator + `chat()`/`run_conversation()` + conversation loop; relevance: the entire library API surface (constructor params, `final_response`/`messages`) is implemented here. · [repo_hermes_agent_trajectory_research](../../../areas/code_repos/repo_hermes_agent_trajectory_research.md) — ShareGPT trajectory schema/canonicalize/export; relevance: `save_trajectories` writes via this module. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `enabled/disabled_toolsets` + tool registry; relevance: the Configuring-Tools section toggles toolsets here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `batch_runner.py` + per-thread instance rule; relevance: the batch-processing + thread-safety notes are rooted here. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `pip install git+…` package + FastAPI/Discord/CI integration; relevance: the install + embedding examples target this package.
- Snippets (10): core_aiagent_orchestrator, core_run_agent_cli, core_chat_helpers_max_iter, batch_runner, batch_runner_spawn, batch_runner_queue, batch_runner_aggregate, trajectory_schema, trajectory_canonicalize, core_conversation_loop_session_persist — relevance: the `AIAgent` orchestrator, agent-run entry, `max_iterations` bound, batch runner (spawn/queue/aggregate), trajectory schema/canonicalization, and session-persist conversation-loop code this library API exposes.
- Docs (12): [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the plugin walkthrough; relevance: the CLI-plugin route contrasted with the programmatic library route. · [hermes_automation_blueprints_scheduled](hermes_automation_blueprints_scheduled.md) — scheduled blueprints; relevance: `cron` jobs vs the `batch_runner` programmatic batch. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the toolsets the library enables/disables via `enabled/disabled_toolsets`. · [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the prompt-cache/cost levers that apply when embedding the agent. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: skills loaded through the embedded `AIAgent`. · [cc_agent_sdk_overview](../claude_code/cc_agent_sdk_overview.md) — CC Agent SDK overview; relevance: closest analogue to embedding the agent. · [cc_sdk_python_client](../claude_code/cc_sdk_python_client.md) — CC Python SDK client; relevance: analogue to `AIAgent`. · [cc_sdk_python_entry_points](../claude_code/cc_sdk_python_entry_points.md) — CC SDK entry functions; relevance: analogue to `chat()`/`run_conversation()`. · [cc_headless_mode](../claude_code/cc_headless_mode.md) — programmatic/headless runs; relevance: analogue to CI/batch embedding. · [cc_headless_examples](../claude_code/cc_headless_examples.md) — headless integration examples; relevance: analogue to the FastAPI/Discord/CI examples. · [cc_agent_sdk_agent_loop](../claude_code/cc_agent_sdk_agent_loop.md) — CC Agent SDK agent loop; relevance: analogue to the `run_conversation` orchestration loop (`final_response`+`messages`). · [cc_agent_sdk_install_and_auth](../claude_code/cc_agent_sdk_install_and_auth.md) — CC Agent SDK install/auth; relevance: analogue to `pip install git+…` + key resolution for the library.

**Note 10 `hermes_use_soul_md_guide`**
- Terms (8): term_persona, term_prompt_injection, term_autonomous_coding_agents, term_agent_harness, term_context_window, term_human_in_the_loop, term_progressive_summarization, term_skill_manifest — relevance: `SOUL.md` is system-prompt slot #1 (agent persona); Hermes scans it for prompt-injection and truncates it against the context window before loading. (+fin: term_soul_md, term_agents_md [own SP05])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — prompt builder (identity slot #1 + context loaders) + injection scrubber; relevance: SOUL.md loading, the prompt-injection scan, and context-window truncation are implemented here. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `~/.hermes/SOUL.md`/`$HERMES_HOME/SOUL.md` location + auto-seed; relevance: the first-run starter seeding and file location are rooted here. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — config/`/personality` command surface; relevance: the SOUL-vs-`/personality` split and config edit flows live here. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — SOUL-vs-skills/memory routing context; relevance: identity (SOUL) vs procedure (skills) routing referenced in this guide. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — system-prompt assembly per provider; relevance: SOUL.md as slot #1 is rendered into each provider's system prompt.
- Snippets (10): core_think_scrubber, core_prompt_builder_context_loaders, core_prompt_builder_context_helpers, core_prompt_builder_environment, core_prompt_builder_skills_snapshot, core_context_references_path_safety, core_message_sanitization, core_redact_patterns, cli_config_set, core_prompt_caching — relevance: the prompt-builder identity/context-loader/skills-snapshot, injection scrubber/sanitization + redact patterns, path-safety, config, and prompt-cache code SOUL.md loading flows through.
- Docs (12): [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the SOUL/AGENTS context-file tips. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: SOUL (identity) vs skills (procedure) routing. · [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the plugin walkthrough; relevance: identity (SOUL) vs extension (plugin) — what belongs where. · [hermes_migrate_from_openclaw](hermes_migrate_from_openclaw.md) — migration reference; relevance: SOUL/persona is migrated from OpenClaw's identity file. · [hermes_use_voice_mode_guide](hermes_use_voice_mode_guide.md) — voice setup; relevance: the persona SOUL.md sets shapes voice replies. · [cc_claude_md_files](../claude_code/cc_claude_md_files.md) — CC's CLAUDE.md project/identity file; relevance: closest analogue to SOUL.md/AGENTS.md. · [cc_output_styles](../claude_code/cc_output_styles.md) — CC personality/output style; relevance: analogue to SOUL-vs-`/personality`. · [cc_memory_overview](../claude_code/cc_memory_overview.md) — CC memory model; relevance: analogue to durable-identity vs memory. · [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — CC injection defenses; relevance: analogue to the SOUL.md injection scan on load. · [cc_effective_prompting](../claude_code/cc_effective_prompting.md) — writing strong instructions; relevance: analogue to the strong-SOUL guidance. · [cc_claude_rules_directory](../claude_code/cc_claude_rules_directory.md) — CC rules-directory layering; relevance: analogue to SOUL.md/AGENTS.md/.cursorrules context-file layering. · [cc_large_codebase_claude_md_layering](../claude_code/cc_large_codebase_claude_md_layering.md) — CC CLAUDE.md layering precedence; relevance: analogue to how SOUL.md (slot #1) layers ahead of AGENTS.md project context.

**Note 11 `hermes_migrate_from_openclaw`**
- Terms (8): term_persona, term_agentic_memory, term_skill_manifest, term_mcp, term_provider_plugin, term_model_catalog, term_session_persistence, term_oauth_token — relevance: migration maps OpenClaw's SOUL/MEMORY, skills, MCP servers, provider/model config, session-reset, and API-key secrets into the Hermes equivalents. (+fin: term_nous_portal [own SP14], term_honcho [own SP05])
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes claw migrate` command + config migrate/schema + auth storage; relevance: the dry-run/`--preset`/`--migrate-secrets` flags and key-mapping logic are implemented here. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `~/.hermes/` config layout + SOUL/MEMORY/AGENTS targets; relevance: the OpenClaw→Hermes file/key destinations are rooted here. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the 4 skill sources + openclaw migration skill; relevance: skill-source remapping is handled here. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — model/provider config + API-key resolution; relevance: the provider/model mapping + four-source key resolution. · [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP-server config mapping; relevance: OpenClaw MCP servers are remapped to `mcp_servers.*`.
- Snippets (10): cli_claw_migrate, optional_skills_migration_openclaw, cli_config_set, cli_config_migrate, cli_config_schema, cli_config_load, cli_auth_storage, core_credential_sources, core_auxiliary_auth_resolution, cli_mcp_config — relevance: the `claw migrate` command, openclaw migration skill, config set/migrate/schema/load, auth storage + credential-source/auth-resolution, and MCP-config mapping code the guide documents.

**Note 12 `hermes_tips_best_practices`**
- Terms (8): term_prompt_caching, term_context_window, term_subagent, term_progressive_summarization, term_agentic_memory, term_skills, term_sandbox_backend, term_access_control — relevance: the cost tips exploit prompt-cache + `/compress` (summarization) + `delegate_task` (subagents); the security tips use Docker sandbox + messaging allowlists; memory/skills tips route fact-vs-procedure. (+fin: term_messaging_gateway [own SP11], term_dm_pairing [own SP11])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — prompt cache + `/compress` compression + context-file loaders; relevance: the "don't break the prompt cache" and `/compress`-before-limits cost tips are implemented here. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `delegate_task` + `execute_code` + Docker sandbox; relevance: the parallel-delegate and batch-execute cost levers + untrusted-code Docker tip. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI power-user surface (`-c`/`-r`, paste, `/verbose`, autocomplete); relevance: the CLI shortcut tips type into this surface. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — `/sethome`/`/title`/DM-pairing + allowlists; relevance: the messaging tips + bot allowlist security live here. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills + memory routing; relevance: the memory-vs-skills "what goes where" tips.
- Snippets (10): core_prompt_caching, core_conversation_compression_entry, core_conversation_compression_strategy, tools_delegate_spawn, tools_delegate_prompt, tools_code_exec_sandbox, tools_environments_docker, cli_skills_install, core_prompt_builder_context_loaders, core_credential_sources — relevance: the prompt-caching, compression entry+strategy, delegate-spawn/prompt, code-exec sandbox, Docker backend, skills-install, context-file loader, and credential-source code these cost/security/memory tips exercise.
- Docs (12): [hermes_use_soul_md_guide](hermes_use_soul_md_guide.md) — SOUL.md identity; relevance: the SOUL/AGENTS context-file tips. · [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: the when-to-create-a-skill + memory-vs-skills routing tips. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the scoped MCP allowlist security tips. · [hermes_automation_blueprints_scheduled](hermes_automation_blueprints_scheduled.md) — scheduled blueprints; relevance: cost tips that apply to unattended cron runs. · [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: the cost levers (`delegate_task`/`execute_code`) used programmatically. · [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — CC cost-reduction; relevance: closest analogue to the cost tips. · [cc_prompt_caching_mechanism](../claude_code/cc_prompt_caching_mechanism.md) — CC prompt cache; relevance: analogue to "don't break the cache". · [cc_effective_prompting](../claude_code/cc_effective_prompting.md) — CC prompting best practices; relevance: analogue to "be specific / provide context". · [cc_security_architecture](../claude_code/cc_security_architecture.md) — CC security model; relevance: analogue to the security do's. · [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — CC sandbox; relevance: analogue to "Docker for untrusted code". · [cc_security_guidance_layers_and_rules](../claude_code/cc_security_guidance_layers_and_rules.md) — CC security guidance layers/rules; relevance: analogue to the allowlist/review-before-"always" security do's. · [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — CC per-feature context cost; relevance: analogue to the `/compress`-before-limits + prompt-cache cost levers.

**Note 13 `hermes_msgraph_app_registration`**
- Terms (8): term_oauth_token, term_authentication, term_access_control, term_oauth, term_pii, term_idempotency, term_autonomous_coding_agents, term_agent_harness — relevance: app-only client-credentials is an OAuth token flow; the minimal Graph permissions + Application Access Policy are least-privilege access control; transcripts carry PII; secret rotation keeps the token flow idempotent. (+fin: term_pkce [own SP09], term_messaging_gateway [own SP11])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — MS-Graph tool + credential files + token provider; relevance: `MicrosoftGraphTokenProvider` smoke test and the `MSGRAPH_*`-driven tool are implemented here. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — MS-Graph webhook platform + Teams adapter; relevance: the registered app feeds the Teams meeting pipeline gateway. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — auth storage + OAuth-callback server + env write; relevance: writing the `MSGRAPH_*` env vars and the token-flow verify live here. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — Teams pipeline plugin; relevance: the Teams meeting summary pipeline is a plugin consuming this app. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `~/.hermes/` env/secret layout; relevance: the env-file + secret-rotation destinations are rooted here.
- Snippets (10): tools_msgraph, gw_platform_msgraph_webhook, plugins_teams_pipeline, plugins_platform_teams, plugins_google_meet, cli_auth_storage, cli_auth_login_logout, core_credential_sources, tools_credential_files, cli_auth_oauth_callback_server — relevance: the MS-Graph tool/auth, msgraph webhook platform, Teams pipeline + adapter, the analogous Google-Meet pipeline, credential storage/login/sources/files, and OAuth-callback code the registered app feeds.
- Docs (12): [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event automation; relevance: the Teams/webhook meeting pipeline this app registration enables. · [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the allowlist/secret-rotation security tips. · [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the OAuth parallels for authenticating remote tools. · [hermes_migrate_from_openclaw](hermes_migrate_from_openclaw.md) — migration reference; relevance: the migrated secret/key (`SecretRef`) resolution this env-write reuses. · [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: programmatic use of the `MSGRAPH_*` token from the library. · [cc_authentication](../claude_code/cc_authentication.md) — CC auth/token model; relevance: closest analogue to the OAuth client-credentials flow. · [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — CC remote-service OAuth; relevance: analogue to the app-only token flow. · [cc_what_claude_can_access](../claude_code/cc_what_claude_can_access.md) — CC least-privilege access scoping; relevance: analogue to the minimal Graph permissions + Application Access Policy. · [cc_security_architecture](../claude_code/cc_security_architecture.md) — CC security model; relevance: analogue to the least-privilege/secret-rotation guidance. · [cc_settings_files](../claude_code/cc_settings_files.md) — CC env/secret config; relevance: analogue to writing the `MSGRAPH_*` env vars. · [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — CC secure-deployment principles; relevance: analogue to least-privilege app registration + secret-rotation hardening. · [cc_environment_variables](../claude_code/cc_environment_variables.md) — CC env-var configuration; relevance: analogue to persisting the `MSGRAPH_TENANT/CLIENT/SECRET` env vars.

All 13 notes meet the FOUR-FLOOR standard: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc. **Every note's Docs
line now carries 12 relevancy-selected, indexed-markdown-link doc entries (5 `hermes_*` siblings + 7
`cc_*`/`thought_*` md-links), each with its own `relevance:` clause** — comfortably over the ≥10 floor (the
prior rendering had the 5 sibling entries as bare names without per-link relevance clauses; they are now proper
`[Name](path.md) — what-it-is; relevance: …` links). Term, code-repo,
`resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by G5/G8). **Three
would-be term slugs were caught at finalization and
not yet existing), and `term_messaging_gateway` (SP11-owned) — none counted to the ≥8 floor; replaced inline
with `term_function_calling` / `term_voice_wake` / `term_access_control` respectively where a floor term was needed.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 10 source pages from `inbox/hermes_agent_docs/guides/`; measured counts match the Source Pages
table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 build-plugin-tutorial | procedure | 1400 | ≤6 (curate manifest/schema/handler/register blocks from 57) | ✓ |
| 2 plugin-extensions-hooks | procedure | 1500 | ≤6 (curate hook-reference + injection + command blocks) | ✓ |
| 3 plugin-types-surfaces | model | 1500 | ≤6 (one canonical block per plugin type / surface) | ✓ |
| 4 automation-scheduled | procedure | 1300 | ≤6 (curate canonical cron recipes) | ✓ |
| 5 automation-event | procedure | 1200 | ≤6 (curate canonical webhook recipes) | ✓ |
| 6 use-mcp-guide | procedure | 1500 | ≤6 (curate from 33 short YAML blocks) | ✓ |
| 7 use-voice-mode-guide | procedure | 1500 | ≤6 (curate from 24 install/config blocks) | ✓ |
| 8 work-with-skills-guide | procedure | 1300 | ≤6 (curate from 16 command blocks) | ✓ |
| 9 python-library-guide | procedure | 1300 | ≤6 (curate from 15 example blocks) | ✓ |
| 10 use-soul-md-guide | procedure | 1100 | ≤6 (from 10 example blocks) | ✓ |
| 11 migrate-from-openclaw | procedure | 1700 | 2 (mostly mapping tables) | ✓ |
| 12 tips-best-practices | procedure | 1500 | ≤6 (from 6) | ✓ |
| 13 msgraph-app-registration | procedure | 1100 | ≤6 (from 5) | ✓ |

No further splits needed beyond the planned 5 (build-plugin→3, automation→2). All 13 notes ≤2500w; the
code-dense how-tos (build-plugin clusters, mcp, voice, skills, python) curate the source blocks to ≤6
load-bearing examples per note, keeping kept blocks verbatim and summarizing the rest in prose. Borderline
note 11 (migrate, ~1700w) was checked for further split: it is one topically-cohesive config-mapping
procedure (the mapping tables are not BB-mixing) → KEEP (review CP6 default-to-keep justification). If any
note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP17)

**SP17 owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every Hermes-specific
concept SP17 touches is owned by another sub-plan (link at finalization as a forward-ref) or is an existing
verified term. Augment re-read of all 10 source pages surfaced **0 new** undigested terms that SP17 should own
— each guide is a *how-to-use/how-to-build* layer over a feature/concept whose term is owned by the feature's
home sub-plan. The collision audit confirmed the plugin guide's reusable concepts map to the EXISTING
`term_plugin_manifest`/`term_plugin_sdk`/`term_provider_plugin` (LINK) plus the SP06b-owned `term_hermes_plugin`
forward-ref — no genuinely-new reusable concept survives the three-way existence check.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_hermes_plugin`, `term_gateway_hooks` | LINK only (forward-ref, +fin [own]) | SP06b | the plugin-system + lifecycle-hook concepts; SP17 documents the build *procedure*, SP06b owns the concept. |
| `term_agent_trajectory` | LINK only (+fin [own]) | SP06 | ShareGPT trajectory format; SP17's python-library guide *uses* `save_trajectories`, concept home is SP06. |
| `term_mcp` *concept* (and SP09 `hermes_mcp` doc) | LINK existing `term_mcp` / forward-ref `hermes_mcp` (+fin) | SP09 | `term_mcp` is substantive+active → LINK; the MCP feature *doc* is SP09's. |
| `term_voice_mode`, `term_text_to_speech`, `term_speech_to_text`, `term_browser_automation` | LINK only (+fin [own]) | SP08 | SP17 holds the voice-mode *how-to*; concept homes are SP08 media/web tools. |
| `term_skills_hub`, `term_progressive_disclosure`, `term_skill_curator`, `term_soul_md`, `term_agents_md`, `term_honcho`, `term_tool_gateway` | LINK only (+fin [own]) | SP05 | SP17's skills/SOUL/migration guides *use* these; concept homes are SP05. |
| `term_nous_portal` | LINK only (+fin [own]) | SP14 | referenced in migrate/tips/voice/mcp tips; captured by SP14. |
| `term_persistent_goal` | LINK only (+fin [own]) | SP06a | automation blueprints touch standing-objective patterns; concept home SP06a. |
| `term_pkce`, `term_credential_pool`, `term_fallback_provider`, `term_provider_routing` | LINK only (+fin [own]) | SP09 | msgraph OAuth + provider tips reference these; concept homes SP09. |
| `term_messaging_gateway`, `term_dm_pairing` | LINK only (+fin [own]) | SP11 | tips/automation/msgraph reference gateway delivery + DM pairing; concept home SP11. |

### Renamed (general → specific)

— (audit performed; SP17 owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP17 links; all are already scope-qualified by their owners
— e.g. `term_hermes_plugin` (≠ generic `term_plugin_sdk`), `term_voice_mode` (≠ `term_voice_wake`), per the
master false-positive caution list.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_hermes_plugin` / general "plugin" concept | `term_plugin_manifest.md` (active), `term_plugin_sdk.md` (active); `term_hermes_plugin` owned by SP06b | Not captured by SP17 — LINK the two existing plugin terms + forward-ref `term_hermes_plugin` (SP06b). |
| `term_python_library` / `term_python_sdk` | none substantive (`term_plugin_sdk`/`term_strands_agents_sdk`/`term_aws_sdk_credential_chain` are unrelated SDKs) | No removal — SP17 was never going to capture this; doc note `hermes_python_library_guide` created instead, linking `term_function_calling`/`term_agent_orchestration`. |
| `term_soul_md` (would duplicate if captured here) | `term_soul_md` owned by SP05; `term_persona.md` (active) covers the persona concept | Not captured by SP17 — LINK `term_persona` + forward-ref `term_soul_md` (SP05). |
| `term_openclaw_migration` | `thought_hermes_agent_vs_openclaw.md` (active) is a *comparison*, not a migration term | No removal — doc note `hermes_migrate_from_openclaw` created; cross-link the thought note. |

## Term-Note Authoring Requirements

N/A (inherited) — SP17 owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP05/06/06a/06b/08/09/11/14). The full
diversity, MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12,
backlink expansion, >200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (plugin-building cluster, P3 pilot):** Notes 1, 2, 3. Pilot Note 1 (`hermes_build_plugin_tutorial`)
  first → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (automation + practical how-tos):** Notes 4, 5, 6, 7, 8. GATE G1–G8.
- **Phase 3 (library + identity + migration + tips + msgraph):** Notes 9, 10, 11, 12, 13. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/guides/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
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
for n in hermes_build_plugin_tutorial hermes_plugin_extensions_hooks hermes_plugin_types_surfaces hermes_automation_blueprints_scheduled hermes_automation_blueprints_event hermes_use_mcp_guide hermes_use_voice_mode_guide hermes_work_with_skills_guide hermes_python_library_guide hermes_use_soul_md_guide hermes_migrate_from_openclaw hermes_tips_best_practices hermes_msgraph_app_registration; do
```

## Entry Point Decision (inherited)

Contributes 13 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Guides: Build & Extend" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP17 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_plugins.md` | → `hermes_build_plugin_tutorial`, `hermes_plugin_extensions_hooks`, `hermes_plugin_types_surfaces` | plugin repo ↔ plugin-building how-tos |
| `repo_hermes_agent_mcp_toolsets.md` | → `hermes_use_mcp_guide` | MCP toolsets repo ↔ MCP usage how-to |
| `repo_hermes_agent_skills.md` | → `hermes_work_with_skills_guide` | skills repo ↔ skills usage how-to |
| `repo_hermes_agent_cron.md` | → `hermes_automation_blueprints_scheduled`, `hermes_automation_blueprints_event` | cron repo ↔ automation blueprints |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_msgraph_app_registration`, `hermes_automation_blueprints_event` | gateway/webhook repo ↔ msgraph + event automation |
| `repo_hermes_agent_agent_core.md` | → `hermes_python_library_guide`, `hermes_use_soul_md_guide` | agent core (AIAgent/prompt-assembly) ↔ library + SOUL docs |
| `repo_hermes_agent.md` | → `hermes_tips_best_practices`, `hermes_migrate_from_openclaw` | implementation ↔ tips + migration usage |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_use_voice_mode_guide` | provider/TTS adapters ↔ voice-mode setup |
| `term_plugin_manifest.md` | → `hermes_build_plugin_tutorial` | concept term → build how-to |
| `term_plugin_sdk.md` | → `hermes_plugin_types_surfaces` | concept term → plugin-types model |
| `term_mcp.md` | → `hermes_use_mcp_guide` | concept term → MCP usage how-to |
| `term_persona.md` | → `hermes_use_soul_md_guide` | concept term → SOUL.md identity how-to |
| `thought_hermes_agent_vs_openclaw.md` | → `hermes_migrate_from_openclaw` | comparison → migration procedure |
| `entry_code_snippets_hermes_agent.md` | → `hermes_build_plugin_tutorial`, `hermes_python_library_guide` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 13 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_build_plugin_tutorial`) → reindex → verify format/ghost/in-degree BEFORE authoring the
rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each
note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6
load-bearing examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split.
If multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP17 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 13 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1/P2 waves land: backfill the forward-ref doc links (`hermes_mcp`→SP09, `hermes_voice_mode`→SP08,
  `hermes_skills`→SP05, `hermes_plugins`→SP06b) and the forward-ref term links (`term_hermes_plugin`,
  `term_soul_md`, `term_voice_mode`, `term_nous_portal`, etc.) once those SPs capture them.
- Consider one `thought_` note comparing Hermes' docs-stated plugin/extension model vs the code-digestion
  findings in `snippet_hermes_agent_plugins_*`.

## Augmentation Report

- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
- **Docs-floor FIX 2026-06-19:** an audit flagged that the 5 `hermes_*` sibling entries on each Docs line were
  rendered as bare names without per-link `relevance:` clauses (only the 5 `cc_*`/`thought_*` bracket-links were
  properly-rendered → effectively short of the ≥10 doc floor). FIXED: every note's Docs line reformatted so ALL
  entries are indexed markdown links with a per-link `relevance:` clause, AND each line expanded from 10 to **12**
  notes now carry 12 properly-rendered doc links (5 siblings + 7 `cc_*`/`thought_*`), all 79 unique non-sibling
  Snippets lines untouched.
- Sections added/updated: Collision&Dedup Audit (plugin/mcp/skills/voice term hits confirmed as
  component-LINKs not dups; `voice_wake`/`voice_call` confirmed different concepts; `thought_..._vs_openclaw`
  confirmed comparison-not-procedure), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5 code-repo +
  bonus to a counted ≥10 floor; docs raised to 12 properly-rendered markdown-link entries for every note —
  over the ≥10 floor), Doc-Note Authoring Spec (derived from
  `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match measured; **no additional splits** beyond the planned 5 (build-plugin→3,
  automation→2). All 13 notes ≤2500w; code-heavy how-tos curated to ≤6 blocks.
- Collision audit: **0 removals from a planned-notes count change** — every planned doc note is NEW; the
  plugin/mcp/skills/soul term hits are LINK-not-dup (existing component concepts) or other-SP forward-refs;
  no doc note duplicates an existing term/doc note. `resources/documentation/hermes_agent/` holds 0 notes
- Term placeholder catch: **3 non-existent / wrongly-scoped term slugs caught at finalization**
  (`term_python_library`, `term_voice_mode` [SP08-owned], `term_messaging_gateway` [SP11-owned]) and replaced
- Undigested terms surfaced at augment: **0 new** (SP17 owns 0 captures; all concepts owned by other SPs or
  existing — the plugin guide's reusable concepts map to existing `term_plugin_manifest`/`term_plugin_sdk`).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs
Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (N/A — 0 owned;
audit noted) ✓ Slug Collision (plugin/mcp/skills/voice LIKE hits + 3 placeholders caught) ✓ dedup generalized
to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓
Doc-Note Authoring Spec derived ✓). Term-capture items are N/A-pass (SP17 owns 0 captures); dedup/collision
items are substantively PASS (audit performed on all 13 doc notes).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

**RE-REVIEWED 2026-06-19 (independent, FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence (2026-06-19 independent re-review) |
|----|-------|--------|----------|
| CP1 | Related Notes step (FOUR-FLOOR) | PASS | All 13 notes machine-counted (2026-06-19 docs-floor fix): every note = 8 term / 5 code-repo / 10 snippet / **12 doc** (5 hermes_* siblings + 7 cc_*/thought_* md-links) — meets ≥8/≥5/≥10/≥10 with the doc line OVER floor at 12. **Every doc entry — including the 5 sibling `hermes_*` entries — is now a proper indexed markdown link `[Name](path.md) — …; relevance: …` carrying its own per-link `relevance:` clause** (the prior rendering had the siblings as bare names; reformatted 2026-06-19). Each repo link also carries a per-link `relevance:`/`—` clause; term & snippet groups carry one group `relevance:` clause (SP01/SP02 exemplar convention). No note below floor. |
| CP2 | 8-GATE per batch (G1-G8) | PASS | 3 phases, each enumerates G1 format / G2 grounding-diff / G3 density+coverage / G4 cross-ref+entry-row / G5 ghost (Script 4, DB-verify) / G6 broken-links / G7 single-BB / G8 in-degree≥1; Validation Scripts implement Script 1 (format+density), Script 4 (ghost), G8 in-degree query. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (13 rows under a Guides: Build & Extend section); parent hub at master level (matches >30-note threshold). |
| CP4 | Plan size manageable | PASS | 13 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); FOUR-FLOOR minimum stated in the spec; not invented. |
| CP6 | Borderline density → split | PASS | build-plugin→3, automation→2; all notes ≤2500w; code-heavy how-tos curated ≤6; borderline migrate (~1700w) checked → cohesive single-BB config-mapping, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 from `inbox/hermes_agent_docs/guides/`: build-plugin 6087w/57c (==plan), migrate 1949w/2c (==plan), use-mcp 1694w/33c (plan 1693 — 1-word rounding, ratio 1.00). All 10 source pages present on disk. |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP17 owns 0 term captures (all concepts owned by SP05/06/06a/06b/08/09/11/14 or existing); Undigested Terms Plan + Authoring Reqs (N/A-inherited) sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 13 doc notes (searched term_dictionary AND documentation/); plugin/mcp/skills/voice LIKE hits confirmed LINK-not-dup; `voice_wake`/`voice_call` confirmed different concepts; 3 placeholder term slugs caught + replaced; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 13 notes from repo_*/term_*/thought_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |


## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-downloaded from NousResearch/hermes-agent
`website/docs/` and re-pinned from commit `95715dc` to `c253b07` on 2026-06-19 (now byte-identical to
upstream `main` HEAD). All 10 of this sub-plan's owned pages were independently re-measured against the
fresh mirror using the ledger convention (body words after stripping YAML frontmatter; code blocks =
count of `^\s*```` lines ÷ 2). **Word/code counts are UNCHANGED** for every owned page:

- `guides/build-a-hermes-plugin.md` — 6087w / 57code (unchanged)
- `guides/automation-blueprints.md` — 2535w / 21code (unchanged)
- `guides/use-mcp-with-hermes.md` — 1693w / 33code (unchanged)
- `guides/use-voice-mode-with-hermes.md` — 1499w / 24code (unchanged)
- `guides/work-with-skills.md` — 1310w / 16code (unchanged)
- `guides/python-library.md` — 1237w / 15code (unchanged)
- `guides/use-soul-with-hermes.md` — 1090w / 10code (unchanged)
- `guides/migrate-from-openclaw.md` — 1949w / 2code (unchanged)
- `guides/tips.md` — 1806w / 6code (unchanged)
- `guides/microsoft-graph-app-registration.md` — 1160w / 5code (unchanged)

Because every count is identical to the manifest, **no planned-note, split, density, or cross-ref decision
is affected** — the 13 planned notes, the two splits (build-plugin→3, automation→2), and the ≤6-code curation
targets all stand as locked. (The cross-ref floor was subsequently RAISED 2026-06-19 to the FOUR-FLOOR standard
≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note — see the Per-Note Related Notes Mapping; the count
re-sync does not affect that floor.) The plan remains **READY** for execution.

## Pipeline Status (Per-Sub-Plan)


**Source**: `inbox/hermes_agent_docs/guides/{build-a-hermes-plugin,automation-blueprints,use-mcp-with-hermes,use-voice-mode-with-hermes,work-with-skills,python-library,use-soul-with-hermes,migrate-from-openclaw,tips,microsoft-graph-app-registration}.md`
**Last Updated**: 2026-06-15 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
