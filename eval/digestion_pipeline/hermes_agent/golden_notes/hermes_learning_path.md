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

**Source**: `inbox/hermes_agent_docs/getting-started/learning-path.md` · https://hermes-agent.nousresearch.com/docs/getting-started/learning-path
**Last Updated**: 2026-06-19
**Status**: Active
