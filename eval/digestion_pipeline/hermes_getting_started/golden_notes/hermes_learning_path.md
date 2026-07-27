---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - navigation
keywords:
  - hermes learning path
  - documentation reading order
  - by experience level
  - by use case
  - beginner intermediate advanced
  - key features at a glance
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/learning-path
access_control_group: ["general"]
---

# Hermes Agent — Learning Path

## Overview

The Learning Path is the **reader router** for the Hermes Agent documentation: it points a new reader at the right pages based on experience level and goal, rather than asking them to read the docs linearly. Hermes Agent spans a wide surface — interactive CLI assistant, messaging-platform bot, task automation, and RL training — so this page exists to turn "where do I start?" into a concrete ordered reading list. It assumes a working install (everything routes through [Installation](hermes_installation.md) → [Quickstart](hermes_quickstart_first_chat.md) first) and, for first-time provider setup, nudges toward `hermes setup --portal` (one OAuth covers a model plus the four Tool Gateway tools). This note is a navigation index, not a feature deep-dive: each track links out to the page that actually teaches it.

## How to Use This Page

Three entry strategies, mirroring the source:

- **Know your level?** Use the By Experience Level table and follow the reading order for your tier.
- **Have a specific goal?** Use By Use Case and pick the scenario that matches what you want to build.
- **Just browsing?** Skim Key Features at a Glance for the full capability map.

The reading order always starts from a working install — `hermes setup --portal` is the recommended first-time provider setup (see [Inference Providers / Nous Portal](hermes_setup_with_nous_portal.md)).

## By Experience Level

| Level | Goal | Recommended reading order |
|---|---|---|
| **Beginner** | Get running, hold basic conversations, use built-in tools | Installation → Quickstart → [CLI Usage](hermes_cli_interface.md) → Configuration |
| **Intermediate** | Messaging bots; memory, cron, and skills | Sessions → Messaging → Tools → [Skills](hermes_skills_system.md) → Memory → [Cron](hermes_cron_scheduling.md) |
| **Advanced** | Build custom tools/skills, train models with RL, contribute | [Architecture](hermes_architecture.md) → Adding Tools → Creating Skills → Contributing |

Time estimates in the source: Beginner ~1 hour, Intermediate ~2–3 hours, Advanced ~4–6 hours.

## By Use Case

Each scenario is an ordered reading list into the relevant docs:

- **"I want a CLI coding assistant"** — Installation → Quickstart → CLI Usage → Code Execution → Context Files → Tips & Tricks. Pass files in via context files; Hermes reads, edits, and runs code in your projects.
- **"I want a Telegram/Discord bot"** — Installation → Configuration → Messaging Overview → Telegram Setup → Discord Setup.
- **"I want to automate tasks"** — Cron (scheduling), Delegation ([subagents](../../term_dictionary/term_subagent.md) for parallel workstreams), Goals (standing objectives), Code Execution.
- **"I want to build custom tools/skills"** — Tools → Skills → [MCP](hermes_mcp_concept_config.md) (connect external tool servers) → Adding Tools / Creating Skills (developer guide).
- **"I want to train models"** — the trajectory/RL track (Atropos): batch trajectory generation feeds RL pipelines; see the trajectory format + research repo.

## Key Features at a Glance

The source closes with a capability directory — CLI/TUI, messaging gateway (20+ platforms), skills + memory, cron + delegation + goals, MCP/ACP protocols, browser/voice/vision media, and provider routing — each a pointer into its dedicated page. Use it as the "everything Hermes can do" map when you don't yet have a specific track in mind.

## Related Notes

**Terms** (concepts each track routes into):
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the agent these docs document; relevance: every track routes into Hermes.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — terminal coding agent; relevance: indexes the "CLI coding assistant" use case.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated child agent; relevance: the automate-tasks Delegation track.
- [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — SKILL.md manifest; relevance: the build-custom-tools/skills track.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the automate-tasks Cron track.
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the custom-tools MCP track.
- [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — multi-agent coordination; relevance: advanced/automation tiers.
- [term_rl](../../term_dictionary/term_rl.md) — reinforcement learning; relevance: the "I want to train models" (Atropos) track.

**Code-Repos** (the implementation each track points at):
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level package; relevance: the Advanced/Contributing track's codebase.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI package; relevance: the Beginner CLI-usage track.
- [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills subsystem; relevance: the Intermediate/Advanced skills track.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: the Tools track + Adding Tools.
- [repo_hermes_agent_trajectory_research](../../../areas/code_repos/repo_hermes_agent_trajectory_research.md) — trajectory/RL; relevance: the "train models" / Atropos track.

**Docs** (where each track lands):
- [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first-chat quickstart; relevance: §Start Here + Beginner step 2.
- [hermes_installation](hermes_installation.md) — install reference; relevance: §Start Here + every track step 1.
- [hermes_cli_interface](hermes_cli_interface.md) — CLI usage; relevance: the Beginner CLI-usage step.
- [hermes_skills](hermes_skills_system.md) — skills system; relevance: the Intermediate/Advanced skills step.
- [hermes_mcp](hermes_mcp_concept_config.md) — MCP integration; relevance: the custom-tools track step.
- [hermes_architecture](hermes_architecture.md) — architecture; relevance: the Advanced track entry.
- [cc_feature_selection_guide](../claude_code/cc_feature_selection_guide.md) — analogous Claude Code feature router; relevance: same "find the right doc" purpose.
- [cc_commands_by_workflow](../claude_code/cc_commands_by_workflow.md) — analogous workflow index; relevance: parallels the By-Use-Case tables.
- [cc_overview](../claude_code/cc_overview.md) — analogous product overview; relevance: parallels Key Features at a Glance.
- [cc_quickstart](../claude_code/cc_quickstart.md) — analogous quickstart; relevance: the "installed → quickstart" hand-off.

**Snippets** (representative implementations of the tracks):
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard; relevance: §Start Here "run setup" entry.
- [snippet_hermes_agent_cli_models_picker](../../code_snippets/snippet_hermes_agent_cli_models_picker.md) — model picker; relevance: the Beginner CLI-usage track.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skills install; relevance: the skills track.
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tools config; relevance: the Tools track.
- [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — ACP entry; relevance: the custom-tools/editor track.
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron CRUD; relevance: the automate-tasks Cron track.
- [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — serve-as-MCP; relevance: the custom-tools MCP track.
- [snippet_hermes_agent_tui_entry](../../code_snippets/snippet_hermes_agent_tui_entry.md) — TUI entry; relevance: the Beginner CLI/TUI track.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — subagent spawn; relevance: the Delegation track.
- [snippet_hermes_agent_trajectory_schema](../../code_snippets/snippet_hermes_agent_trajectory_schema.md) — RL trajectory schema; relevance: the "train models" (Atropos) track.

**Source**: `inbox/hermes_agent_docs/getting-started/learning-path.md` · https://hermes-agent.nousresearch.com/docs/getting-started/learning-path
**Last Updated**: 2026-06-19
**Status**: Active
