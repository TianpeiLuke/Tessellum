---
title: Sub-Plan to07 — OpenClaw Docs: Tools (Skills, Slash Commands, Steer, Sub-agents, Tavily, Thinking)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/skills", "tools/skills-config", "tools/slash-commands", "tools/steer", "tools/subagents", "tools/tavily", "tools/thinking"]
---

# Sub-Plan to07: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML order, `## Overview`/`## Related Notes`/`## References` body, density caps), dedup-before-create (term_dictionary + documentation/ + repo_openclaw*), 9-GATE validation, cross-references, and the entry-point/wiring (W1–W5) decisions are ALL inherited from the master.

## Scope

The 7 **Tools** pages that document how an OpenClaw agent's behavior surface is taught, invoked, steered, and parallelized: **skills** (markdown instruction files that teach tool use), **skills-config** (the `skills.*` config schema), **slash-commands** (the chat command/directive/shortcut catalog), **steer** (`/steer` injecting guidance into an active run), **sub-agents** (background `sessions_spawn` runs with announce-back, thread-binding, and nesting), **tavily** (the Tavily search/extract tool), and **thinking** (the `/think`/`/fast`/`/verbose`/`/trace`/`/reasoning` directive system). Priority **P2 (Phase B)** per master — these are the agent-control feature pages that the concepts/CLI/gateway core (Phase A) reference. The code-side counterparts (`repo_openclaw_skills`, `repo_openclaw_agents`, `repo_openclaw_extensions`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **14,918 measured words**. **Planned: 10 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| skills | tools/skills | 2,802 | 8 | 14 | 2 | procedure (split: loading/lifecycle vs SKILL.md format+gating) |
| skills-config | tools/skills-config | 1,704 | 9 | 10 | 0 | procedure (config reference) |
| slash-commands | tools/slash-commands | 2,774 | 9 | 12 | 4 | procedure (split: types/config vs catalog/surfaces) |
| steer | tools/steer | 396 | 2 | 5 | 0 | procedure |
| subagents | tools/subagents | 4,334 | 6 | 17 | 22 | concept+procedure (split: spawn/tools vs orchestration/lifecycle) |
| tavily | tools/tavily | 842 | 0 | 5 | 2 | procedure |
| thinking | tools/thinking | 2,066 | 0 | 11 | 0 | procedure (directive system) |

Total: 14,918 words · 34 code fences · 74 H2 + 30 H3.

## Content Strategy

- **Prioritize**: the sub-agent spawn/delegation contract (`sessions_spawn`/`sessions_yield`/`subagents`, context modes, tool policy by depth — the most operationally dense, FZ-15-relevant content) and the skill loading-precedence + gating model (how OpenClaw decides which skills an agent sees). These are the two largest pages and the core of "how an OpenClaw agent's capability surface is assembled."
- **Split** (4 of 7 pages): `subagents.md` (4,334w / mixed concept+procedure) → spawn/tool-surface note + orchestration/lifecycle note; `skills.md` (2,802w) → loading/lifecycle note + SKILL.md-format/gating note; `slash-commands.md` (2,774w) → command-model/config note + command-catalog/per-surface note. All exceed the 2,500w cap or mix BBs (see Split Decisions). The remaining 4 pages stay 1 note each.
- **Link-out (do NOT redefine)**: thinking levels reference per-provider mapping → link `term_chain_of_thought`/`term_reasoning_model` analogs and `oc_*` providers series (planned); sandboxing/secrets referenced by skills → link `term_sandbox`/`oc_gateway_*` (planned); ClawHub install → link `oc_clawhub_*` (planned); ACP/queue/compaction referenced by steer/subagents → link `term_acp_agent_client_protocol` + `oc_concepts_queue`/`oc_concepts_compaction` (planned). Provider names in thinking.md (Anthropic/OpenAI/Gemini/DeepSeek/MiniMax/Z.AI/Moonshot/Ollama) are documented as config behavior, NOT promoted to term notes (link `term_claude`/`term_llm`).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_skills_loading.md` | procedure | skills.md: Loading order, Per-agent vs shared skills, Agent allowlists, Plugins and skills, Skill Workshop, Installing from ClawHub, Security, Environment injection, Snapshots and refresh, Token impact | 700 | How OpenClaw discovers, prioritizes, and scopes skills: the 6-level loading-precedence order, per-agent vs shared roots, agent allowlists, ClawHub/Git/local install, security/path-containment, env injection, session snapshot/refresh, and the deterministic token-impact formula. |
| 2 | `oc_tools_skills_format_gating.md` | procedure | skills.md: SKILL.md format (Optional frontmatter keys), Gating (Installer specs), Config overrides | 600 | Authoring a SKILL.md: required/optional frontmatter keys (user-invocable, command-dispatch, command-tool), the `metadata.openclaw` gating block (requires.bins/anyBins/env/config, os, primaryEnv, install specs), installer-selection rules, and `skills.entries` config overrides (enabled/apiKey/env/config). |
| 3 | `oc_tools_skills_config.md` | procedure | skills-config.md: Loading, Install, Operator Install Policy, Bundled skill allowlist, Per-skill entries, Agent allowlists, Workshop, Symlinked skill roots, Sandboxed skills and env vars, Loading order reminder | 650 | The full `skills.*` config schema: `skills.load` (extraDirs/symlink/watch), `skills.install` (preferBrew/nodeManager/uploads), `security.installPolicy` (the trusted-command allow/block protocol), `allowBundled`, `skills.entries`, agent allowlists, `skills.workshop` limits, symlinked-root containment, and passing secrets into a sandbox. |
| 4 | `oc_tools_slash_commands_model.md` | procedure | slash-commands.md: header (ACP routing), Three command types, Configuration, Surface notes, Provider usage and status | 650 | The slash-command model: the three types (commands / directives / inline shortcuts) and their persist-vs-inline semantics, the `commands.*` config schema (native/nativeSkills/text/bash/owner gating/allowFrom/useAccessGroups), per-surface session scoping (Discord/Slack/Telegram), and provider usage/status reporting in `/status`. |
| 5 | `oc_tools_slash_commands_catalog.md` | procedure | slash-commands.md: Command list (Core commands, Dock commands, Bundled plugin commands, Skill commands), `/tools`, `/model`, `/config`, `/mcp`, `/debug`, `/plugins`, `/trace`, `/btw` | 700 | The slash-command catalog: core built-ins (sessions/runs, model/run controls, discovery/status, skills/allowlists/approvals, subagents/ACP, owner-only writes, voice/TTS), dock commands, bundled-plugin and skill commands, plus the owner-only `/config` `/mcp` `/debug` `/plugins` write surfaces and `/tools` `/model` `/btw` runtime commands. |
| 6 | `oc_tools_steer.md` | procedure | steer.md: header, Current session, Steer vs queue, Sub-agents, ACP sessions | 400 | The `/steer` (alias `/tell`) command for injecting guidance into an already-active run: current-session targeting, fallback to a normal prompt when steering is unavailable, `/steer` vs `/queue steer`/`collect`/`followup`/`interrupt` mode comparison, sub-agent visibility, and `/acp steer` for ACP harness sessions. |
| 7 | `oc_tools_subagents_spawn.md` | procedure | subagents.md: header, Slash command (Thread binding controls, Spawn behavior), Context modes, Tool: `sessions_spawn` (Delegation prompt mode, Tool parameters, Task names and targeting), Tool: `sessions_yield`, Tool: `subagents`, Tool policy, Concurrency | 750 | The sub-agent spawn/delegate contract: `/subagents` inspection, non-blocking push-based `sessions_spawn` (defaults, all parameters, taskName targeting, delegation modes), `isolated` vs `fork` context modes, `sessions_yield` as the wait primitive (no polling), the `subagents` lister, the sub-agent tool-restriction policy, and the `subagent` concurrency lane. |
| 8 | `oc_tools_subagents_orchestration.md` | concept | subagents.md: Thread-bound sessions (Thread supporting channels, Quick flow, Manual controls, Config switches, Allowlist, Discovery, Auto-archive), Nested sub-agents (Depth levels, Announce chain, Tool policy by depth, Per-agent spawn limit, Cascade stop), Authentication, Announce (Announce context, Stats line, Why prefer sessions_history), Liveness and recovery, Stopping, Limitations | 800 | Sub-agent orchestration and lifecycle: persistent thread-bound sessions (`/focus`/`/unfocus`, channel adapters, idle/max-age), nested orchestrator depth (`maxSpawnDepth`, depth-level tool policy, announce chain, cascade stop), per-agent-id auth resolution, the announce step (context block, stats line, `sessions_history` recall safety), liveness/orphan-recovery, stopping, and limitations. |
| 9 | `oc_tools_tavily.md` | procedure | tavily.md: header, Getting started, Tool reference (`tavily_search`, `tavily_extract`), Choosing the right tool, Advanced configuration | 500 | The Tavily search/extract tool: enabling it as the `web_search` provider or via the bundled `tavily_search`/`tavily_extract` tools, API-key setup and resolution order, the full parameter tables (search_depth/topic/time_range/domains, extract_depth/chunks_per_source), and how to choose between `web_search`, `tavily_search`, and `tavily_extract`. |
| 10 | `oc_tools_thinking.md` | procedure | thinking.md: What it does, Resolution order, Setting a session default, Application by agent, Fast mode (/fast), Verbose directives (/verbose), Plugin trace directives (/trace), Reasoning visibility (/reasoning), Heartbeats, Web chat UI, Provider profiles | 800 | OpenClaw's thinking/output directive system: the `/think` level ladder (off→max) and its per-provider mapping, the 5-layer resolution order, setting a session default, `/fast` (priority/service-tier mapping), `/verbose`, `/trace`, and `/reasoning` directives, heartbeat/web-chat behavior, and the provider-profile hooks that declare per-model level sets. |

## Section Coverage Map

```
tools/skills.md
├── Loading order ───────────────────────────────── → note 1 (oc_tools_skills_loading)
├── Per-agent vs shared skills ───────────────────── → note 1
├── Agent allowlists ─────────────────────────────── → note 1
├── Plugins and skills ───────────────────────────── → note 1
├── Skill Workshop ───────────────────────────────── → note 1 (→ oc_tools_skill_workshop, to06 planned)
├── Installing from ClawHub ──────────────────────── → note 1 (→ oc_clawhub_* planned)
├── Security ─────────────────────────────────────── → note 1
├── SKILL.md format / Optional frontmatter keys ──── → note 2 (oc_tools_skills_format_gating)
├── Gating / Installer specs ─────────────────────── → note 2
├── Config overrides ─────────────────────────────── → note 2
├── Environment injection ────────────────────────── → note 1
├── Snapshots and refresh ────────────────────────── → note 1
└── Token impact ─────────────────────────────────── → note 1
tools/skills-config.md
├── Loading (skills.load) ────────────────────────── → note 3 (oc_tools_skills_config)
├── Install (skills.install) ─────────────────────── → note 3
├── Operator Install Policy (security.installPolicy) → note 3
├── Bundled skill allowlist ──────────────────────── → note 3
├── Per-skill entries (skills.entries) ───────────── → note 3
├── Agent allowlists (agents) ────────────────────── → note 3
├── Workshop (skills.workshop) ───────────────────── → note 3
├── Symlinked skill roots ────────────────────────── → note 3
├── Sandboxed skills and env vars ────────────────── → note 3
└── Loading order reminder ───────────────────────── → note 3
tools/slash-commands.md
├── header (ACP routing, ! bash) ─────────────────── → note 4 (oc_tools_slash_commands_model)
├── Three command types ──────────────────────────── → note 4
├── Configuration ────────────────────────────────── → note 4
├── Command list (Core commands) ─────────────────── → note 5 (oc_tools_slash_commands_catalog)
├── Command list (Dock commands) ─────────────────── → note 5
├── Command list (Bundled plugin commands) ───────── → note 5
├── Command list (Skill commands) ────────────────── → note 5
├── /tools, /model, /config, /mcp, /debug ────────── → note 5
├── /plugins, /trace, /btw ───────────────────────── → note 5
├── Surface notes ────────────────────────────────── → note 4
└── Provider usage and status ────────────────────── → note 4
tools/steer.md
├── header ───────────────────────────────────────── → note 6 (oc_tools_steer)
├── Current session ──────────────────────────────── → note 6
├── Steer vs queue ───────────────────────────────── → note 6
├── Sub-agents ───────────────────────────────────── → note 6
└── ACP sessions ─────────────────────────────────── → note 6
tools/subagents.md
├── header / Primary goals / Cost note ───────────── → note 7 (oc_tools_subagents_spawn)
├── Slash command (+ Thread binding controls, Spawn behavior) → note 7
├── Context modes ────────────────────────────────── → note 7
├── Tool: sessions_spawn (Delegation prompt mode,
│   Tool parameters, Task names and targeting) ───── → note 7
├── Tool: sessions_yield ─────────────────────────── → note 7
├── Tool: subagents ──────────────────────────────── → note 7
├── Tool policy (+ Override via config) ──────────── → note 7
├── Concurrency ──────────────────────────────────── → note 7
├── Thread-bound sessions (all H3) ───────────────── → note 8 (oc_tools_subagents_orchestration)
├── Nested sub-agents (all H3) ───────────────────── → note 8
├── Authentication ───────────────────────────────── → note 8
├── Announce (Announce context, Stats line, Why
│   prefer sessions_history) ─────────────────────── → note 8
├── Liveness and recovery ────────────────────────── → note 8
├── Stopping ─────────────────────────────────────── → note 8
└── Limitations ──────────────────────────────────── → note 8
tools/tavily.md
├── header / property table ──────────────────────── → note 9 (oc_tools_tavily)
├── Getting started ──────────────────────────────── → note 9
├── Tool reference (tavily_search, tavily_extract) ─ → note 9
├── Choosing the right tool ──────────────────────── → note 9
└── Advanced configuration ───────────────────────── → note 9
tools/thinking.md
├── What it does (level ladder + provider notes) ─── → note 10 (oc_tools_thinking)
├── Resolution order ─────────────────────────────── → note 10
├── Setting a session default ────────────────────── → note 10
├── Application by agent ──────────────────────────── → note 10
├── Fast mode (/fast) ────────────────────────────── → note 10
├── Verbose directives (/verbose) ────────────────── → note 10
├── Plugin trace directives (/trace) ─────────────── → note 10
├── Reasoning visibility (/reasoning) ────────────── → note 10
├── Heartbeats ───────────────────────────────────── → note 10
├── Web chat UI ──────────────────────────────────── → note 10
└── Provider profiles ────────────────────────────── → note 10
```

No orphaned sections. Cross-page pointers (Skill Workshop → to06, ClawHub → cw01–03, queue/compaction → co02/co06, ACP → to01) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `subagents.md` (4,334w, 17 H2 / 22 H3, concept+procedure) | notes 7 + 8 | Far exceeds the 2,500w cap and mixes the spawn/tool-surface **procedure** (how to call `sessions_spawn`/`sessions_yield`, parameters, tool policy) with the orchestration/lifecycle **concept** (thread-binding, nesting depth model, announce/recovery semantics). Split by word-cap + mixed-BB; each half stays ≤800w / ≤4 code blocks. |
| `skills.md` (2,802w, 14 H2 / 2 H3) | notes 1 + 2 | Exceeds 2,500w; cleanly separates the skill-**lifecycle** procedure (discovery, precedence, allowlists, install, snapshot/refresh, env injection) from the SKILL.md-**authoring**/gating procedure (frontmatter keys, `metadata.openclaw` gating, installer specs, `skills.entries`). Two distinct task clusters; each ≤700w. |
| `slash-commands.md` (2,774w, 12 H2 / 4 H3) | notes 4 + 5 | Exceeds 2,500w; separates the command-**model**/config (command types, persist-vs-inline semantics, `commands.*` schema, per-surface scoping) from the command-**catalog** (the full per-command tables + the owner-only write surfaces). Each ≤700w. |

The remaining 4 pages (`skills-config` 1,704w, `steer` 396w, `tavily` 842w, `thinking` 2,066w) are each below the cap and single-BB → 1 note each.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (14,918 words). New `oc_` notes: **10**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×9** (notes 1–7, 9, 10) · **concept ×1** (note 8, sub-agent orchestration model).
- Est. digest words ~**6,550** (avg ~655/note). 34 source code fences (mostly JSON5 config + `<ParamField>` schema) distribute across notes; each note kept ≤6 (config snippets reproduced selectively + verbatim; thinking.md/tavily.md/steer.md are prose/tables with 0–2 fences).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)



### oc_tools_skills_loading (8t · 10s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: skill loading is OpenClaw's capability-injection mechanism.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime wrapper that drives an LLM agent's tool loop; relevance: the harness resolves the effective skill list at session start.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed code-writing agents; relevance: skills teach these agents how/when to use tools.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK plugins use to ship skills/tools; relevance: plugin skills merge at the extraDirs precedence level.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: untrusted skills are run sandboxed and bin checks differ host vs container.
- [Homebrew](../../term_dictionary/term_homebrew.md) — the macOS/Linux package manager; relevance: `requires.bins` install gates resolve through brew.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization/visibility control; relevance: agent allowlists scope which skills an agent can see.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing what enters the model context; relevance: the per-session skill snapshot + token-impact formula are context-budget controls.

**Docs**
- [oc_tools_skills_format_gating](oc_tools_skills_format_gating.md) — SKILL.md authoring + gating (planned, this series, note 2); relevance: the authoring half of the same skills page.
- [oc_tools_skills_config](oc_tools_skills_config.md) — full `skills.*` config schema (planned, this series, note 3); relevance: config overrides referenced by loading/allowlists.
- [oc_tools_skill_workshop](oc_tools_skill_workshop.md) — proposal queue for agent-drafted skills (planned, this series, to06); relevance: Workshop section points here.
- [oc_clawhub_quickstart](oc_clawhub_quickstart.md) — installing community skills from ClawHub (planned, this series, cw01); relevance: ClawHub install path.
- [cc_skills_overview](../claude_code/cc_skills_overview.md) — Claude Code skills model; relevance: closest existing analog for skill discovery/precedence.
- [cc_skill_invocation_and_lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — when/how Claude Code loads skills; relevance: parallel to OpenClaw snapshot/refresh lifecycle.
- [cc_large_codebase_skills_and_plugins](../claude_code/cc_large_codebase_skills_and_plugins.md) — scaling skills/plugins; relevance: plugin-shipped skills + token impact parallel.
- [pi_skills](../pi/pi_skills.md) — Pi coding agent skills system; relevance: a second independent coding-agent skill-loading precedent.
- [hermes_skills_system](../hermes_agent/hermes_skills_system.md) — Hermes skill loading/precedence; relevance: ecosystem-sibling loading model to contrast.
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — using/installing Hermes skills; relevance: parallel install/scope guide.
- [hermes_security_skill_memory_settings](../hermes_agent/hermes_security_skill_memory_settings.md) — Hermes skill security/scoping; relevance: parallel to OpenClaw's untrusted-skill security warning.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents with capability surfaces; relevance: cross-framework view of agent capability assembly.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — the skills subsystem this documents; relevance: code home of the loading/precedence logic.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent workspace + snapshot; relevance: env injection + snapshot live here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin-shipped skills; relevance: plugin skill directories.

**Snippets**
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill discovery/planning; relevance: implements the loading-order scan.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — gating/eligibility evaluation; relevance: load-time filtering by env/config/bins.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — untrusted-skill scanning; relevance: the Security section's scan path.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — per-agent scoping; relevance: agent allowlist application.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config resolution; relevance: effective skill list per agent run.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injecting blocks into the system prompt; relevance: the compact skill XML block + token impact.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable/disable lifecycle; relevance: plugin skills load when the plugin is enabled.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — `openclaw.plugin.json` contract; relevance: plugins list `skills` directories here.
- [snippet_hermes_agent_skills_canonical_loading_runtime](../../code_snippets/snippet_hermes_agent_skills_canonical_loading_runtime.md) — Hermes runtime skill loading; relevance: parallel precedence/snapshot logic.
- [snippet_hermes_agent_core_prompt_builder_skills_snapshot](../../code_snippets/snippet_hermes_agent_core_prompt_builder_skills_snapshot.md) — building the skills snapshot into the prompt; relevance: parallel to OpenClaw's session snapshot.

### oc_tools_skills_format_gating (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: SKILL.md is OpenClaw's skill-authoring format.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — declarative plugin metadata file; relevance: SKILL.md frontmatter is a manifest-like declaration.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin/skill SDK; relevance: installer specs + skill packaging use it.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-invocation mechanism; relevance: `command-dispatch: tool` routes a slash command directly to a registered tool.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated runtime; relevance: `requires.bins` must also exist inside the container; setupCommand notes.
- [Homebrew](../../term_dictionary/term_homebrew.md) — package manager; relevance: brew installer kind + preference order.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: sandboxed skill installs via `sandbox.docker.setupCommand`.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization/scoping; relevance: secret-injection scope is host-only per agent turn.

**Docs**
- [oc_tools_skills_loading](oc_tools_skills_loading.md) — skill discovery/precedence (planned, this series, note 1); relevance: lifecycle half of the same page.
- [oc_tools_skills_config](oc_tools_skills_config.md) — `skills.*` config schema (planned, this series, note 3); relevance: `skills.entries` overrides referenced here.
- [oc_tools_creating_skills](oc_tools_creating_skills.md) — author a custom skill from scratch (planned, this series, to02); relevance: the page links here for authoring.
- [cc_skill_frontmatter_reference](../claude_code/cc_skill_frontmatter_reference.md) — Claude Code SKILL.md frontmatter keys; relevance: direct analog of OpenClaw's frontmatter spec.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — authoring a Claude Code skill; relevance: parallel SKILL.md authoring procedure.
- [cc_plugin_install_hints](../claude_code/cc_plugin_install_hints.md) — install hints for plugins; relevance: parallel to OpenClaw installer specs.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin security guidance; relevance: gating + secret-injection security boundary.
- [pi_skills](../pi/pi_skills.md) — Pi skills frontmatter/format; relevance: independent SKILL.md-style precedent.
- [hermes_skill_md_format_bundles](../hermes_agent/hermes_skill_md_format_bundles.md) — Hermes SKILL.md format + bundles; relevance: closest ecosystem SKILL.md format analog.
- [hermes_creating_skill_format](../hermes_agent/hermes_creating_skill_format.md) — authoring a Hermes skill; relevance: parallel frontmatter + gating authoring.
- [cc_skill_invocation_and_lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — model-vs-command invocation; relevance: `user-invocable`/`disable-model-invocation`/`command-dispatch` keys.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: frontmatter parsing + gating live here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/installer integration; relevance: installer specs + plugin skill gating.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — SKILL.md frontmatter/manifest parsing; relevance: the exact format this note documents.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — command-tool dispatch descriptor; relevance: `command-dispatch: tool` + `command-tool` keys.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — gating evaluation; relevance: `metadata.openclaw.requires` checks.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanning; relevance: untrusted SKILL.md inspection.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: installer/metadata schema parallel.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entry points; relevance: how installer specs surface to the UI.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret resolution; relevance: `skills.entries.*.env`/`apiKey` host injection scope.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog assembly; relevance: command-dispatch resolves a registered tool.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — Hermes frontmatter parsing; relevance: parallel single-line-key frontmatter parsing.
- [snippet_hermes_agent_skills_canonical_format](../../code_snippets/snippet_hermes_agent_skills_canonical_format.md) — Hermes canonical SKILL format; relevance: ecosystem SKILL.md format analog.
- [snippet_hermes_agent_tools_skill_manager](../../code_snippets/snippet_hermes_agent_tools_skill_manager.md) — Hermes skill manager + gating; relevance: parallel gating/installer handling.

### oc_tools_skills_config (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `skills.*` is OpenClaw's skill config tree.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — structured config schema concept; relevance: the page is a full config-schema reference.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization control; relevance: `security.installPolicy` is an operator allow/block protocol.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated runtime; relevance: sandboxed-skills section + env passing.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: passing secrets via `sandbox.docker.env`.
- [Homebrew](../../term_dictionary/term_homebrew.md) — package manager; relevance: `skills.install.preferBrew`.
- [DevOps](../../term_dictionary/term_devops.md) — install/automation tooling discipline; relevance: nodeManager/preferBrew/upload knobs are install-tooling controls.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret storage/resolution; relevance: SecretRef `apiKey` + sandbox secret delivery.

**Docs**
- [oc_tools_skills_loading](oc_tools_skills_loading.md) — loading order/precedence (planned, this series, note 1); relevance: config repeats the loading-order reminder.
- [oc_tools_skills_format_gating](oc_tools_skills_format_gating.md) — gating + `skills.entries` (planned, this series, note 2); relevance: entries/gating defined together.
- [oc_clawhub_publishing](oc_clawhub_publishing.md) — publish/sync via ClawHub (planned, this series, cw02); relevance: install sources covered by install policy.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — managed plugin/install policy; relevance: direct analog of `security.installPolicy`.
- [cc_plugin_user_config_and_env](../claude_code/cc_plugin_user_config_and_env.md) — per-plugin config + env injection; relevance: analog of `skills.entries` config/env.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin security guidance; relevance: operator install-policy security framing.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings/config reference; relevance: independent config-schema reference precedent.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: install/trust policy parallel.
- [hermes_security_skill_memory_settings](../hermes_agent/hermes_security_skill_memory_settings.md) — Hermes skill/memory security settings; relevance: parallel skill-config security knobs.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — Hermes command/install approval; relevance: analog of the trusted install-policy command.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: config consumer.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — install policy + scanner; relevance: `security.installPolicy` implementation.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin install paths; relevance: policy applies to plugin install/update too.

**Snippets**
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — install-policy gating path; relevance: the `security.installPolicy` exec protocol.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanning; relevance: staged-source inspection before install.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: install-policy decision plumbing.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — trust findings reporting; relevance: block/allow decision output.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: `apiKey` SecretRef + sandbox secret delivery.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — manifest format; relevance: `skills.entries` keys match skill name/`skillKey`.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — eligibility evaluation; relevance: `allowBundled` + agent allowlists application.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard writes config; relevance: `openclaw setup --node-manager` config flow.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: config changes take effect on next session/turn.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload planning; relevance: applying `skills.load.watch` changes.

### oc_tools_slash_commands_model (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the Gateway handles `/...` standalone messages.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — protocol binding a conversation to a harness; relevance: ACP-bound text routes to the harness while `/acp` stays local.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization control; relevance: `allowFrom`/`useAccessGroups`/owner gating decide who can run commands/directives.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — guiding an active run; relevance: `/steer` and `/queue` are directives covered by the model.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — tool/server protocol; relevance: owner-only `/mcp` reads/writes `mcp.servers` config.
- [Message Queue](../../term_dictionary/term_message_queue.md) — queued message handling; relevance: directives include `/queue` modes; command-only messages bypass the queue.
- [Function Calling](../../term_dictionary/term_function_calling.md) — direct tool dispatch; relevance: skill commands can route directly to a tool.
- [Slash Command (Steering Files)](../../term_dictionary/term_steering_files.md) — agent control/instruction surface; relevance: directives/inline shortcuts are agent-control surfaces (closest existing concept).

**Docs**
- [oc_tools_slash_commands_catalog](oc_tools_slash_commands_catalog.md) — the full command catalog (planned, this series, note 5); relevance: the catalog half of the same page.
- [oc_tools_steer](oc_tools_steer.md) — `/steer` deep-dive (planned, this series, note 6); relevance: a directive documented in detail.
- [oc_tools_thinking](oc_tools_thinking.md) — `/think`/`/fast`/`/verbose` directives (planned, this series, note 10); relevance: directive type defined here.
- [oc_concepts_queue](oc_concepts_queue.md) — command queue model (planned, this series, co06); relevance: `/queue` directive semantics.
- [cc_commands_reference](../claude_code/cc_commands_reference.md) — Claude Code slash-command reference; relevance: direct analog of the command model.
- [cc_sdk_slash_commands](../claude_code/cc_sdk_slash_commands.md) — programmatic slash-command registration; relevance: parallel command registration/dispatch.
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managed MCP config; relevance: analog of owner-only `/mcp` writes.
- [pi_rpc_commands](../pi/pi_rpc_commands.md) — Pi command/RPC surface; relevance: independent command-routing precedent.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — Hermes messaging-surface slash commands; relevance: per-surface command scoping analog.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — Hermes interactive CLI commands; relevance: command-type model parallel.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — Hermes command authorization/approval; relevance: parallel to `allowFrom`/owner gating.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — auto-reply command registry; relevance: core built-ins live here.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — per-surface native command registration; relevance: native/Slack/Discord/Telegram command surfaces.

**Snippets**
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — command catalog/registry; relevance: the command sources + availability flags.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — command authorization policy; relevance: `allowFrom`/owner/access-group gating.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send-policy gating; relevance: `/send` owner control + command authorization.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: ACP-bound text routes to harness while management commands stay local.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method gating; relevance: owner-only `/config`/`/mcp`/`/debug`/`/plugins` write gating.
- [snippet_openclaw_acp_translator_prompt](../../code_snippets/snippet_openclaw_acp_translator_prompt.md) — ACP prompt translation; relevance: normal text routed to the ACP harness.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key derivation; relevance: per-surface native-command session scoping.
- [snippet_hermes_agent_core_skill_commands_discovery](../../code_snippets/snippet_hermes_agent_core_skill_commands_discovery.md) — skill-command discovery; relevance: how skill commands register as slash commands.
- [snippet_hermes_agent_cli_hermescli_process_command](../../code_snippets/snippet_hermes_agent_cli_hermescli_process_command.md) — command processing pipeline; relevance: parallel command parse/dispatch.

### oc_tools_slash_commands_catalog (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this catalogs OpenClaw's built-in commands.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — harness protocol; relevance: the `/acp ...` subcommand family.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — tool/server protocol; relevance: the owner-only `/mcp` write command.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — run guidance; relevance: `/steer`/`/queue` run-control commands.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple cooperating agents; relevance: `/subagents`, `/agents`, `/focus`/`/unfocus` thread-binding commands.
- [Compaction](../../term_dictionary/term_compaction.md) — context compression; relevance: the `/compact` command.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization; relevance: owner-only `/config`/`/mcp`/`/plugins`/`/debug` write surfaces + `/allowlist`/`/approve`.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: `/tasks` lists background tasks.

**Docs**
- [oc_tools_slash_commands_model](oc_tools_slash_commands_model.md) — command model/config (planned, this series, note 4); relevance: the model half of the same page.
- [oc_tools_subagents_spawn](oc_tools_subagents_spawn.md) — `/subagents` + spawn (planned, this series, note 7); relevance: subagent/ACP commands target this.
- [oc_tools_steer](oc_tools_steer.md) — `/steer` (planned, this series, note 6); relevance: command listed in the catalog.
- [oc_tools_thinking](oc_tools_thinking.md) — `/think`/`/fast`/etc. (planned, this series, note 10); relevance: model/run-control commands.
- [oc_concepts_compaction](oc_concepts_compaction.md) — compaction model (planned, this series, co02); relevance: `/compact` semantics.
- [cc_commands_reference](../claude_code/cc_commands_reference.md) — Claude Code command reference; relevance: direct catalog analog.
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI commands; relevance: parallel built-in command catalog.
- [cc_commands_by_workflow](../claude_code/cc_commands_by_workflow.md) — commands grouped by workflow; relevance: parallel grouping of session/model/discovery commands.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI command reference; relevance: independent command-catalog precedent.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — Hermes interactive CLI command list; relevance: ecosystem command-catalog analog.
- [hermes_profile_commands_reference](../hermes_agent/hermes_profile_commands_reference.md) — Hermes profile command reference; relevance: parallel owner/admin command surface.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — core built-in command registry; relevance: catalog source.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — dock + native commands; relevance: dock-command + per-surface registration.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard surface; relevance: `/config`/`/doctor`-adjacent command surfaces.

**Snippets**
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — the command catalog; relevance: enumerates core/dock/plugin/skill commands.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — command policy; relevance: owner-only write-command gating.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: `/config`/`/mcp`/`/debug` require their config flags.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — abort handling; relevance: `/stop` aborts the active run.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compact/reset; relevance: `/compact`, `/reset`, `/new` session commands.
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — ACP control application; relevance: the `/acp ...` control subcommands.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: `/send on|off|inherit`.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reactions surface; relevance: `/status` discovery output.
- [snippet_hermes_agent_cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — Hermes CLI command set; relevance: parallel built-in command catalog.

### oc_tools_steer (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `/steer` is an OpenClaw run-control command.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — guiding an active run; relevance: this IS the steering command's home concept.
- [Steering Files](../../term_dictionary/term_steering_files.md) — files that steer agent behavior; relevance: closest sibling concept — runtime steering vs file-based steering.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — harness protocol; relevance: `/acp steer` targets ACP harness sessions.
- [Message Queue](../../term_dictionary/term_message_queue.md) — queued messages; relevance: `/steer` vs `/queue steer`/`collect`/`followup`/`interrupt` comparison.
- [Queue Processing](../../term_dictionary/term_queue_processing.md) — queue-mode handling; relevance: steering independence from the stored `/queue` mode.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — cooperating agents; relevance: sub-agents report to parent; `/subagents` is visibility-only.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating runs; relevance: steering injects guidance at runtime boundaries during orchestration.

**Docs**
- [oc_tools_slash_commands_catalog](oc_tools_slash_commands_catalog.md) — command catalog (planned, this series, note 5); relevance: `/steer` listed there.
- [oc_tools_slash_commands_model](oc_tools_slash_commands_model.md) — directive model (planned, this series, note 4); relevance: `/steer` is a directive.
- [oc_tools_subagents_spawn](oc_tools_subagents_spawn.md) — sub-agents (planned, this series, note 7); relevance: sub-agent steering visibility.
- [oc_concepts_queue](oc_concepts_queue.md) — command queue (planned, this series, co06); relevance: `/queue` mode comparison.
- [oc_tools_acp_agents](oc_tools_acp_agents.md) — ACP agents (planned, this series, to01); relevance: `/acp steer` session selection.
- [cc_commands_reference](../claude_code/cc_commands_reference.md) — Claude Code commands; relevance: closest analog for a mid-run control command.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — Hermes messaging commands; relevance: parallel mid-run control surface.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation/run-guidance patterns; relevance: steering vs queue decision parallel.
- [band_acp_overview](../band/band_acp_overview.md) — Band ACP model; relevance: ACP-session steering analog.
- [band_agents](../band/band_agents.md) — Band agent model; relevance: cross-framework active-run guidance context.
- [pi_interactive_usage](../pi/pi_interactive_usage.md) — Pi interactive run control; relevance: independent mid-run guidance precedent.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — active-run steering path; relevance: where `/steer` injects guidance.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/run state; relevance: targets the current session's active run.

**Snippets**
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — ACP session handoff; relevance: `/acp steer` session targeting.
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — ACP control apply; relevance: applying steer to an ACP harness session.
- [snippet_openclaw_acp_translator_cancel](../../code_snippets/snippet_openclaw_acp_translator_cancel.md) — ACP cancel/interrupt; relevance: interrupt-vs-steer boundary behavior.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — abort handling; relevance: interrupt mode replacing the active run.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: steering at the next supported runtime boundary.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — inbound message dispatch; relevance: fallback to a normal prompt when steering unavailable.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable message kernel; relevance: queue-mode message handling alongside steer.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key resolution; relevance: targeting the current session's active run.
- [snippet_hermes_agent_core_aiagent_orchestrator](../../code_snippets/snippet_hermes_agent_core_aiagent_orchestrator.md) — run orchestration; relevance: parallel active-run guidance injection.

### oc_tools_subagents_spawn (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: sub-agents are OpenClaw background agent runs.
- [Subagent](../../term_dictionary/term_subagent.md) — a delegated child agent run; relevance: this note documents the spawn contract for subagents.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — cooperating agents; relevance: `sessions_spawn` parallelizes work across agents.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agent runs; relevance: spawn/yield/subagents are the delegation primitives.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — harness protocol; relevance: `runtime: "acp"` spawns into external harnesses.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated runtime; relevance: `sandbox: "require"` + sandboxed-requester spawn rejection.
- [Message Queue](../../term_dictionary/term_message_queue.md) — queued lane; relevance: spawns run on the `subagent` concurrency lane.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `sessions_spawn`/`sessions_yield`/`subagents` are agent tools.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing child context; relevance: `isolated` vs `fork` context modes.

**Docs**
- [oc_tools_subagents_orchestration](oc_tools_subagents_orchestration.md) — orchestration/lifecycle (planned, this series, note 8); relevance: the lifecycle half of the same page.
- [oc_tools_steer](oc_tools_steer.md) — `/steer` (planned, this series, note 6); relevance: steering vs sub-agent visibility.
- [oc_tools_acp_agents](oc_tools_acp_agents.md) — ACP agents (planned, this series, to01); relevance: `runtime: "acp"` delivery model.
- [oc_automation_tasks](oc_automation_tasks.md) — background tasks (planned, this series, au01); relevance: each spawn is tracked as a background task.
- [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — Claude Code subagents; relevance: direct analog of the spawn/delegation model.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — defining a subagent; relevance: parallel subagent configuration.
- [cc_forked_subagents](../claude_code/cc_forked_subagents.md) — forked subagents; relevance: direct analog of `context: "fork"`.
- [cc_sdk_subagents_definition](../claude_code/cc_sdk_subagents_definition.md) — programmatic subagent definition; relevance: parallel spawn parameters/tool policy.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — Hermes subagent delegation; relevance: ecosystem delegation-tool analog.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation patterns; relevance: when to delegate vs reply directly (delegationMode parallel).
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents; relevance: cross-framework background/parallel agent runs.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — subagent spawn + run manager; relevance: `sessions_spawn` implementation.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session keys/forking; relevance: child session-key shape + fork branching.

**Snippets**
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — spawn policy/tool gating; relevance: which profiles expose `sessions_spawn`.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — spawn caps; relevance: `maxChildrenPerAgent`/`maxConcurrent` defaults.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ACP spawn path; relevance: `runtime: "acp"` spawn behavior.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — run manager; relevance: non-blocking run-id return + tracking.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy resolution; relevance: sub-agent tool-restriction layer.
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — ACP spawn gating; relevance: `runtime: "acp"` visibility conditions.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key utils; relevance: `agent:<id>:subagent:<uuid>` key shape + `taskName` targeting.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — Hermes delegate-spawn; relevance: parallel non-blocking spawn primitive.
- [snippet_hermes_agent_tools_delegate_prompt](../../code_snippets/snippet_hermes_agent_tools_delegate_prompt.md) — delegate task prompt; relevance: parallel to the `[Subagent Task]` delegation prompt.
- [snippet_hermes_agent_tools_delegate_anti_recursion](../../code_snippets/snippet_hermes_agent_tools_delegate_anti_recursion.md) — delegation recursion guard; relevance: depth/nesting safety parallel.

### oc_tools_subagents_orchestration (10t · 11s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: orchestration is OpenClaw's nested-subagent runtime.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated child run; relevance: thread-binding, nesting, announce all govern subagents.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — cooperating agents; relevance: orchestrator → worker depth model.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agents; relevance: the orchestrator pattern + announce chain.
- [Hyperorchestrator](../../term_dictionary/term_hyperorchestrator.md) — multi-level orchestration controller; relevance: depth-2 orchestrator coordinating worker children.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedupe key for delivery; relevance: completions handed back with a stable idempotency key.
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — retry pacing; relevance: announce retried with short exponential backoff.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — harness protocol; relevance: nested/ACP runtime delivery paths.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — credential token; relevance: sub-agent auth merged per agent id from agentDir.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential resolution; relevance: auth resolved by agent id, main profiles as fallback.

**Docs**
- [oc_tools_subagents_spawn](oc_tools_subagents_spawn.md) — spawn/tool surface (planned, this series, note 7); relevance: the spawn half of the same page.
- [oc_automation_tasks](oc_automation_tasks.md) — background tasks (planned, this series, au01); relevance: auto-archive + liveness tie to task records.
- [oc_concepts_multi_agent](oc_concepts_multi_agent.md) — multi-agent model (planned, this series, co05); relevance: the orchestration concept's home.
- [oc_concepts_session](oc_concepts_session.md) — session model (planned, this series, co06); relevance: thread-bound session keys + lifecycle.
- [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — orchestrating agent teams; relevance: direct analog of orchestrator/worker chains.
- [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — subagent model; relevance: parallel nesting/announce semantics.
- [cc_sdk_subagents_lifecycle](../claude_code/cc_sdk_subagents_lifecycle.md) — subagent lifecycle; relevance: analog of liveness/auto-archive/recovery.
- [cc_work_with_subagents](../claude_code/cc_work_with_subagents.md) — working with subagents; relevance: parallel orchestration usage guide.
- [hermes_kanban_worker_orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — Hermes orchestrator/worker board; relevance: ecosystem orchestrator-pattern analog.
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent board; relevance: nested multi-agent coordination parallel.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-agent profiles; relevance: per-agent auth/profile resolution parallel.
- [band_a2a_overview](../band/band_a2a_overview.md) — agent-to-agent protocol; relevance: cross-framework announce/handback model.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — subagent registry lifecycle/liveness; relevance: orchestration runtime.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session state; relevance: depth-keyed session metadata + recovery.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — thread-binding adapters; relevance: Discord/Matrix/Telegram/Feishu bindings.

**Snippets**
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — announce step; relevance: the announce chain + context block.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — registry lifecycle; relevance: auto-archive + depth tracking.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — liveness checks; relevance: stale-run pruning + orphan recovery.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — thread binding on spawn; relevance: thread-bound subagent sessions.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: `threadBindings` enablement/timeouts.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — run manager; relevance: cascade stop + concurrency tracking.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering; relevance: agent-id auth merge with main fallback.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: stopping/cascade + recovery events.
- [snippet_hermes_agent_tools_delegate_aggregate](../../code_snippets/snippet_hermes_agent_tools_delegate_aggregate.md) — aggregating child results; relevance: orchestrator synthesizing announces.
- [snippet_hermes_agent_core_aiagent_orchestrator](../../code_snippets/snippet_hermes_agent_core_aiagent_orchestrator.md) — orchestrator core; relevance: parallel nested-orchestration runtime.

**Other vault**

### oc_tools_tavily (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: OpenClaw exposes Tavily as a search/extract tool + provider.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `tavily_search`/`tavily_extract` are callable tools.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — retrieving relevant documents; relevance: Tavily is an IR/search API for agents.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Tavily returns results structured for LLM consumption + AI answer summaries.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: third-party API with key + per-request caps (20 results/URLs).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: Tavily is an external API keyed by `TAVILY_API_KEY`.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — managing context; relevance: query-focused chunking feeds only relevant content into context.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret resolution; relevance: API key resolved via SecretRef then env (resolution order).

**Docs**
- [oc_tools_web](oc_tools_web.md) — web-search overview/providers (planned, this series, to08); relevance: Tavily as the `web_search` provider.
- [oc_tools_exa_search](oc_tools_exa_search.md) — Exa neural search (planned, this series, to03); relevance: alternative search-with-extraction provider.
- [oc_tools_firecrawl](oc_tools_firecrawl.md) — Firecrawl search+scrape (planned, this series, to03); relevance: alternative extraction provider.
- [oc_tools_parallel_search](oc_tools_parallel_search.md) — parallel search tool (planned, this series, to05); relevance: sibling search tool.
- [cc_web_overview](../claude_code/cc_web_overview.md) — Claude Code web search/fetch; relevance: direct analog of the web_search provider model.
- [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — MCP tool search; relevance: tool-discovery analog for search tooling.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — Hermes web search + extract; relevance: ecosystem analog of `tavily_search`/`tavily_extract`.
- [hermes_tool_search](../hermes_agent/hermes_tool_search.md) — Hermes tool search; relevance: parallel search-tool surface.
- [hermes_tools_reference_core](../hermes_agent/hermes_tools_reference_core.md) — Hermes core tools (incl. web); relevance: parallel web-tool reference.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — Pi custom tools; relevance: independent custom-tool-as-provider precedent.
- [band_mcp_ai_assistant_setup](../band/band_mcp_ai_assistant_setup.md) — Band tool/assistant setup; relevance: cross-framework tool-provider config analog.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled Tavily plugin; relevance: the plugin home.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — `web_search` routing; relevance: provider selection + tool dispatch.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: how `tavily_search`/`tavily_extract` register as tools.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent search query path; relevance: search-result feeding into context.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin contract; relevance: the Tavily plugin `entries`/config schema.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential resolution; relevance: `TAVILY_API_KEY` resolution order.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: bundled-tool registration.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — Hermes web tools; relevance: ecosystem search/extract tool analog.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — Hermes web plugin; relevance: parallel web-provider plugin.
- [snippet_hermes_agent_skills_research_arxiv](../../code_snippets/snippet_hermes_agent_skills_research_arxiv.md) — research/search skill; relevance: search-driven research flow analog.
- [snippet_slipbot_unified_retrieval](../../code_snippets/snippet_slipbot_unified_retrieval.md) — unified retrieval; relevance: search-depth/relevance ranking parallel (basic vs advanced).

### oc_tools_thinking (9t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `/think` is OpenClaw's directive/output-control system.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — step-by-step reasoning; relevance: thinking levels control reasoning effort / extended thinking.
- [Reasoning Agent](../../term_dictionary/term_reasoning_agent.md) — agent that reasons before answering; relevance: `/reasoning` visibility + reasoning-capable model fallbacks.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: per-provider mapping (Opus 4.7+ effort, adaptive thinking, `--effort`).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: levels map across OpenAI/Gemini/DeepSeek/Ollama/MiniMax/Z.AI/Moonshot.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — caching prompt prefixes; relevance: provider profiles + Anthropic prefix interact with thinking/cache.
- [Model Router](../../term_dictionary/term_model_router.md) — routing across providers/models; relevance: provider profiles drive per-model level sets + service tiers.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: tool plugins validate thinking overrides via runtime APIs.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — runtime guidance; relevance: `/think`/`/fast`/`/verbose`/`/trace`/`/reasoning` are session-control directives.

**Docs**
- [oc_tools_slash_commands_model](oc_tools_slash_commands_model.md) — directive model (planned, this series, note 4); relevance: thinking commands are directives.
- [oc_concepts_models](oc_concepts_models.md) — model model/config (planned, this series, co04); relevance: per-model thinking params.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — model providers (planned, this series, co04); relevance: provider profiles declare level sets.
- [oc_tools_elevated](oc_tools_elevated.md) — elevated mode (planned, this series, to03); relevance: the page links to Elevated mode docs.
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — Claude Code effort/thinking levels; relevance: direct analog of the `/think` ladder + `--effort`.
- [pi_custom_models](../pi/pi_custom_models.md) — Pi custom-model config; relevance: per-model reasoning/effort config precedent.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — Pi model override/compat; relevance: `compat.supportedReasoningEfforts` opt-in parallel.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — Hermes model config; relevance: per-model thinking/fast-mode config analog.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — Hermes provider routing; relevance: provider-profile mapping parallel.
- [band_adapter_anthropic](../band/band_adapter_anthropic.md) — Band Anthropic adapter; relevance: Anthropic thinking/effort mapping analog.
- [band_adapter_catalog](../band/band_adapter_catalog.md) — Band adapter catalog; relevance: cross-provider capability/level declarations.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — thinking resolution; relevance: the 5-layer resolution order lives here.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider thinking profiles; relevance: `resolveThinkingProfile` per provider.

**Snippets**
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — Anthropic prefix/effort handling; relevance: Opus 4.7+ effort + adaptive thinking mapping.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: provider-profile level sets + compat metadata.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: `service_tier` + thinking payload mapping.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: Responses `reasoning.effort` + `service_tier=priority`.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama provider; relevance: `think` effort string mapping (`max` → `high`).
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — session-level overrides; relevance: directive-set session thinking/fast/verbose overrides.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: `compat.supportedReasoningEfforts` normalization.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config resolution; relevance: per-agent/global `thinkingDefault` resolution.
- [snippet_hermes_agent_core_think_scrubber](../../code_snippets/snippet_hermes_agent_core_think_scrubber.md) — reasoning-tag scrubbing; relevance: `/reasoning` hiding/streaming + malformed `<think>` handling.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — prompt/verbose modes; relevance: `/verbose`/`/trace` output-shape control.


## Undigested Terms Plan

Per master, OpenClaw vocabulary on these pages is digested as `oc_*` doc concepts in their home note, NOT as new `term_dictionary` entries; the only term_dictionary interaction is **linking existing** terms. **Expected: 0 new `term_dictionary` captures.**

| Term (page vocabulary) | Disposition |
|---|---|
| skill / SKILL.md / skill loading order / skill snapshot | → note 1/2 (`oc_tools_skills_*`); link `term_openclaw`, `term_plugin_manifest`, `term_plugin_sdk` |
| skill gating (`metadata.openclaw.requires`) / installer spec | → note 2; documented as config, link `term_homebrew`/`term_docker`/`term_sandbox` |
| `security.installPolicy` (operator install policy) | → note 3; documented as config, link `term_access_control` |
| Skill Workshop / proposal queue | → note 1 pointer; home note is `oc_tools_skill_workshop` (to06, planned) |
| slash command / directive / inline shortcut | → note 4 (`oc_tools_slash_commands_model`); link `term_openclaw` |
| dock command / native command / skill command | → note 5 (`oc_tools_slash_commands_catalog`) |
| `/steer` / steering boundary / runtime boundary | → note 6 (`oc_tools_steer`); link existing `term_agent_steering` |
| sub-agent / `sessions_spawn` / `sessions_yield` / announce | → note 7/8 (`oc_tools_subagents_*`); link `term_multi_agent`, `term_agent_orchestration` |
| isolated vs fork context mode | → note 7; documented as a parameter, link `term_context_engineering` |
| orchestrator pattern / `maxSpawnDepth` / depth levels | → note 8; link `term_agent_orchestration`, `term_multi_agent` |
| Tavily / `tavily_search` / `tavily_extract` | → note 9 (`oc_tools_tavily`); tool/provider, NOT promoted (no `term_tavily` exists; link `term_information_retrieval`, `term_function_calling`) |
| thinking level / `/think` / `/fast` / `/verbose` / `/trace` / `/reasoning` | → note 10 (`oc_tools_thinking`); link existing `term_chain_of_thought`, `term_model_router` |
| provider profile / `resolveThinkingProfile` / service tier | → note 10; documented as provider behavior, link `term_claude`, `term_llm` |
| provider names (Anthropic, OpenAI, Gemini, DeepSeek, MiniMax, Z.AI, Moonshot, Ollama) | NOT promoted to term notes; link `term_claude`/`term_llm`/`term_third_party_genai_services` |

**New-term candidates (genuinely cross-cutting, no existing note, no doc-page home):** none identified. The agentic/LLM glossary already covers steering, orchestration, CoT, prompt caching, etc. If augment's Step 2d re-scan surfaces a genuinely reusable term with no home (low probability), it would be captured via `/tessellum-capture-term-note` and added to its best-fit `acronym_glossary_*.md` (likely `acronym_glossary_a_e.md` or `acronym_glossary_p_t.md`) — not expected here.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (10 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order + body sections (`## Overview` … `## Related Notes` … `## References` + bold footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traceable to `inbox/openclaw_docs/tools/<page>` (no hallucination; config snippets verbatim) | diff vs mirror source |
| G3 | Density + Coverage: ≤400 lines / ≤2,500 words / ≤6 code blocks; one building_block per note; every mapped H2/H3 covered | density script (below) + Section Coverage Map |
| G4 | Cross-Reference: ≥6 relevance-selected term links + repo_openclaw*/sibling oc_*/sibling docs, each with a relevance statement; indexed `[text](path.md)` format | `note_links` query post-reindex |
| G6 | Broken-link fix: 0 broken relative paths | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability: each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` + term/repo inlinks | `notes.in_degree` query |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_skills_loading oc_tools_skills_format_gating oc_tools_skills_config oc_tools_slash_commands_model oc_tools_slash_commands_catalog oc_tools_steer oc_tools_subagents_spawn oc_tools_subagents_orchestration oc_tools_tavily oc_tools_thinking"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G1 required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density: ≤2500 words (body, frontmatter excluded) and ≤6 code fences
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # sibling-prefix sanity (this-series links use oc_)
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n: no $SIBLING_PREFIX sibling link"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
bash scripts/update_notes_database.sh --force   # reindex, then verify note_links + in_degree + 0 broken
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_tools_skills_loading | procedure | 700 | ≤4 | ✅ |
| 2 | oc_tools_skills_format_gating | procedure | 600 | ≤4 | ✅ |
| 3 | oc_tools_skills_config | procedure | 650 | ≤5 | ✅ |
| 4 | oc_tools_slash_commands_model | procedure | 650 | ≤2 | ✅ |
| 5 | oc_tools_slash_commands_catalog | procedure | 700 | ≤4 | ✅ |
| 6 | oc_tools_steer | procedure | 400 | ≤2 | ✅ |
| 7 | oc_tools_subagents_spawn | procedure | 750 | ≤3 | ✅ |
| 8 | oc_tools_subagents_orchestration | concept | 800 | ≤2 | ✅ |
| 9 | oc_tools_tavily | procedure | 500 | ≤1 | ✅ |
| 10 | oc_tools_thinking | procedure | 800 | 0 | ✅ |

No note approaches caps. The three split pages (subagents 4,334w / skills 2,802w / slash-commands 2,774w) each became 2 notes well under 2,500w. Code-heavy `skills-config.md` (9 fences) → note 3 keeps ≤5 by reproducing the most load-bearing JSON5 blocks (`security.installPolicy.exec`, `skills.entries`) and summarizing the rest as a `<ParamField>` table.

## Entry Point Decision (inherited from master)

Per master W1, `0_entry_points/entry_openclaw_docs.md` is CREATED as a pre-step before any sub-plan executes (>30 notes corpus-wide). This sub-plan contributes **10 rows** to that hub under a **"Tools — Agent Control & Skills"** cluster (one row per note, with sub-plan id `to07`). Each new note receives its entry-point back-link at finalization (satisfies G7/G8 anti-island). No standalone entry point is created for this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; every new note needs in-degree ≥1):
- `entry_openclaw_docs.md` (created pre-step) → all 10 notes (guaranteed anti-island floor).
- `repo_openclaw_skills.md` → notes 1, 2, 3.
- `repo_openclaw_agents.md` → notes 4, 5, 6, 7, 8, 10.
- `repo_openclaw_extensions.md` → notes 2, 3, 9.
- `repo_openclaw_sessions.md` → notes 6, 7, 8.
- `term_agent_steering.md` → notes 4, 6, 10.
- `term_multi_agent.md` / `term_agent_orchestration.md` → notes 7, 8.
- `term_chain_of_thought.md` → note 10.
- `term_information_retrieval.md` → note 9.
- `term_plugin_manifest.md` / `term_plugin_sdk.md` → notes 1, 2.

## Pacing Rules (inherited from master)

One execution phase (10 notes); 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run (well under). Re-read each source page during enrich; reproduce config snippets verbatim. One BB per note. Reindex incrementally after the wave; verify `note_links` + `in_degree ≥1` + 0 broken links before commit. `git pull --rebase --autostash origin main` first; commit + push per wave; **no Claude co-author trailer**.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment)** |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21 (9/9 CP)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Source re-read + measurement (CP7).** All 7 pages re-read and `wc -w`-measured: skills 2,802w · skills-config 1,704w · slash-commands 2,774w · steer 396w · subagents 4,334w · tavily 842w · thinking 2,066w = **14,918w** — matches the plan's Source table exactly (ratio 1.00). No density under-estimation; no re-splits needed.

**Per-note counts (all floors MET).**

|---|---:|---:|---:|---:|---|
| oc_tools_skills_loading | 8 | 11 | 12 (8 existing / 4 planned) | 3 | MET |
| oc_tools_skills_format_gating | 8 | 11 | 11 (8 / 3) | 2 | MET |
| oc_tools_skills_config | 8 | 10 | 10 (7 / 3) | 3 | MET |
| oc_tools_slash_commands_model | 8 | 10 | 11 (7 / 4) | 2 | MET |
| oc_tools_slash_commands_catalog | 8 | 10 | 11 (6 / 5) | 3 | MET |
| oc_tools_steer | 8 | 10 | 11 (6 / 5) | 2 | MET |
| oc_tools_subagents_spawn | 9 | 11 | 11 (7 / 4) | 2 | MET |
| oc_tools_subagents_orchestration | 10 | 11 | 12 (8 / 4) | 3 | MET |
| oc_tools_tavily | 8 | 10 | 11 (7 / 4) | 2 | MET |
| oc_tools_thinking | 9 | 10 | 11 (7 / 4) | 2 | MET |



**New-term candidates + best-fit glossary.** **None.** This sub-plan authors 0 new `term_dictionary` notes (per master: OpenClaw page vocabulary is digested as `oc_*` doc concepts, only existing terms are linked). The re-read (augment Step 2d) surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. The agentic/LLM glossary already covers steering, orchestration, subagent, CoT, prompt caching, idempotency, backoff, etc. If execution unexpectedly surfaces one, it would be captured via `/tessellum-capture-term-note` into `acronym_glossary_a_e.md` or `acronym_glossary_p_t.md` (not expected).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE per batch (G1–G6 + G7/G8 + G9) present | **PASS** | `## Per-Phase Validation Gate (G1–G9) — inherited from master` lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7/G8 discoverability with tools per gate. |
| CP4 | Size manageable | **PASS** | 10 notes (≤30 cap); single execution phase. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited from master, derived from `cc_*`/`pi_*`; verified `cc_skills_overview.md` uses `# Title → ## Overview → source H2 → ## Related Notes → ## References` and YAML `tags → keywords → topics → …` — matches the plan's Format Definition exactly. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 10 notes ≤800w / ≤6 code, none near caps; the 3 over-cap source pages (subagents 4,334w, skills 2,802w, slash-commands 2,774w) already split 2-way each (Split Decisions table). No unaddressed borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 pages re-read + `wc -w`-measured 2026-06-21; total 14,918w matches plan Source table exactly (ratio 1.00); 0 pages >1.5× estimate. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + must-language | **PASS** | `## Undigested Terms Plan` present (every row dispositioned to an `oc_*` home + existing-term link; "Expected: 0 new term_dictionary captures"); `## Term-Note Authoring Requirements` present (N/A 0 new terms; master multi-source/glossary mandate inherited verbatim if a term unexpectedly arises). |
| CP9 | Discoverability / inlinks executed (G8, anti-island) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` + repo_openclaw* + term backlinks); G7/G8 in the gate table requires in-degree ≥1 verified post-reindex; reciprocal FZ-15 analysis backlinks planned for notes 7/8. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.**
