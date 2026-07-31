---
tags:
  - resource
  - documentation
  - claude_code
  - skills
  - bundled_skills
keywords:
  - bundled skills
  - prompt-based skill
  - disableBundledSkills
  - code-review batch debug loop claude-api
  - run verify run-skill-generator
  - bundled workflow
  - built-in command vs skill
topics:
  - Claude Code
  - Skills
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/skills
access_control_group: ["general"]
---

# Claude Code — Bundled Skills

## Overview

**Bundled skills** are skills that ship with Claude Code and are available in every session unless disabled. They include `/code-review`, `/batch`, `/debug`, `/loop`, and `/claude-api`. Unlike most built-in commands — which execute fixed logic coded into the CLI — bundled skills are **prompt-based**: they hand Claude detailed instructions and let it orchestrate the work using its own tools. You invoke them the same way as any other skill, by typing `/` followed by the skill name, and Claude can also invoke them automatically when relevant.

This note covers what bundled skills are, how they differ from fixed-logic built-ins, the `disableBundledSkills` toggle, and the run/verify trio that confirms changes against a running app. Bundled skills are listed alongside built-in commands in the commands reference, marked **Skill** in the Purpose column (see [Commands Reference](cc_commands_reference.md)). The internals of specific bundled skills and workflows are owned elsewhere — deep agent and workflow mechanics link out to their dedicated pages.

## Prompt-Based Skills vs Fixed-Logic Built-Ins

A bundled skill works exactly like a skill you write yourself: a prompt handed to Claude, which Claude can also invoke automatically when relevant. This is the key distinction from ordinary built-in commands such as `/help` or `/compact`, whose behavior is coded directly into the CLI. Because a bundled skill is just instructions plus Claude's tool use, it can adapt to the situation rather than running a fixed procedure.

The commands reference marks two kinds of entries beyond plain built-ins:

- **Skill** — a bundled skill (prompt-based; Claude can also invoke it automatically). Examples in the catalogue include `/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`, `/simplify`, `/fewer-permission-prompts`, and the run/verify trio below.
- **Workflow** — a bundled [dynamic workflow](https://code.claude.com/docs/en/workflows) that fans work out across many subagents and runs in the background (e.g. `/deep-research`). Workflow internals are documented on the workflows page.

`/batch` illustrates the orchestration pattern: it decomposes a large change into independent units and spawns one background subagent per unit in its own git worktree — Claude coordinates the fan-out rather than following hardcoded logic.

## Disabling Bundled Skills

Bundled skills are available in every session unless disabled with the `disableBundledSkills` setting (see [settings](https://code.claude.com/docs/en/settings#available-settings)). Bundled and managed skills are also not affected by the `disableSkillShellExecution` policy that disables shell preprocessing for user, project, and plugin skills.

## Run and Verify Your App

Three bundled skills work together to launch your app and confirm changes against the running app instead of just relying on tests:

| Skill | Purpose |
| :--- | :--- |
| `/run` | Launch and drive your app to see a change working |
| `/verify` | Build and run your app to confirm a code change does what it should, without falling back to tests or type checks |
| `/run-skill-generator` | Teach `/run` and `/verify` how to build and launch your project |

All three require Claude Code v2.1.145 or later. `/run` and `/verify` work without setup: they infer the launch from your project type (CLI, server, TUI, browser-driven) and from what's in your README, `package.json`, or `Makefile`. That inference gets unreliable for projects needing anything beyond a standard launch — a database, an env file, a graphical session, a multi-step build.

`/run-skill-generator` records the recipe instead. It gets your app running from a clean environment, captures what worked (install commands, env vars, launch script), and commits it as a per-project skill at `.claude/skills/run-<name>/`. After that, `/run`, `/verify`, and any other agent in the repo follow the recorded recipe instead of rediscovering it. Run it once per project, and again if the build or launch process changes.

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
