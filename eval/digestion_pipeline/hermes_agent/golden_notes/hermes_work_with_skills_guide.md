---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - how_to
keywords:
  - working with skills
  - skills hub install
  - progressive disclosure
  - skill_view
  - create your own skill
  - skills vs memory
topics:
  - Hermes Agent
  - Skills
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
access_control_group: ["general"]
---

# Working with Skills

## Overview

This is the day-to-day **how-to for skills** in Hermes Agent — the procedural guide for finding, installing, using, and authoring skills, where a *skill* is an on-demand knowledge document (a `SKILL.md` plus optional reference files) that teaches Hermes how to handle one specific task, from generating ASCII art to managing GitHub PRs. It is the usage companion to the Skills System concept reference: that page covers the full technical model, while this page walks the operator through the commands they actually type. The through-line is that **every installed skill is automatically a slash command** and skills cost zero tokens until they are actually loaded, thanks to a three-tier progressive-disclosure loading pattern. This note documents the practical surface only; the underlying skill-loading concepts (Skills Hub, progressive disclosure, the skill curator) are owned by the feature/concept layer and linked, not re-explained here.

## Finding Skills

Every Hermes installation ships with bundled skills. List them from a chat session with `/skills` or from the CLI with `hermes skills list`, which prints a compact `name → description` table (e.g. `ascii-art`, `arxiv`, `github-pr-workflow`, `plan`, `excalidraw`).

### Searching for a Skill

Filter the list by keyword with `/skills search <keyword>` (for example `/skills search docker` or `/skills search music`).

### The Skills Hub

Official optional skills — heavier or niche skills not active by default — live in the Hub. Browse them with `/skills browse` and search the Hub with `/skills search <keyword>`.

## Using a Skill

Every installed skill is automatically a slash command — just type its name, optionally with a task:

```bash
# Load a skill and give it a task
/ascii-art Make a banner that says "HELLO WORLD"
/plan Design a REST API for a todo app
/github-pr-workflow Create a PR for the auth refactor

# Just the skill name (no task) loads it and lets you describe what you need
/excalidraw
```

You can also trigger skills through natural conversation — ask Hermes to use a specific skill and it loads it via the `skill_view` tool.

### Progressive Disclosure

Skills use a token-efficient three-tier loading pattern; the agent does not load everything at once:

1. **`skills_list()`** — compact list of all skills (~3k tokens), loaded at session start.
2. **`skill_view(name)`** — full `SKILL.md` content for one skill, loaded when the agent decides it needs that skill.
3. **`skill_view(name, file_path)`** — a specific reference file within the skill, loaded only if needed.

Skills therefore do not cost tokens until they are actually used.

## Installing from the Hub

Official optional skills ship with Hermes but are not active by default — install them explicitly. You can install an official optional skill by its catalog path, or a single-file `SKILL.md` directly from any HTTP(S) URL:

```bash
# Install an official optional skill (official/<category>/<name>)
hermes skills install official/research/arxiv
/skills install official/creative/songwriting-and-ai-music

# Install a single-file SKILL.md directly from any HTTP(S) URL
hermes skills install https://sharethis.chat/SKILL.md
/skills install https://example.com/SKILL.md --name my-skill
```

On install, the skill directory is copied to `~/.hermes/skills/`, appears in your `skills_list` output, and becomes available as a slash command. Installed skills take effect in **new** sessions; to use one in the current session, run `/reset` to start fresh, or add `--now` to invalidate the prompt cache immediately (which costs more tokens on the next turn).

### Verifying Installation

Confirm a skill landed with `hermes skills list | grep arxiv` from the CLI, or `/skills search arxiv` in chat.

## Plugin-Provided Skills

Plugins can bundle their own skills under namespaced names (`plugin:skill`), which prevents collisions with built-in skills. Load a plugin skill by its qualified name; a built-in skill with the same base name is unaffected:

```bash
# Load a plugin skill by its qualified name
skill_view("superpowers:writing-plans")

# Built-in skill with the same base name is unaffected
skill_view("writing-plans")
```

Plugin skills are **not** listed in the system prompt and do not appear in `skills_list` — they are opt-in, loaded explicitly when you know a plugin provides one. When loaded, the agent sees a banner listing sibling skills from the same plugin. To ship skills in your own plugin, see the bundled-skills step of the plugin build guide.

## Configuring Skill Settings

Some skills declare configuration they need in their frontmatter under `metadata.hermes.config`:

```yaml
metadata:
  hermes:
    config:
      - key: tenor.api_key
        description: "Tenor API key for GIF search"
        prompt: "Enter your Tenor API key"
        url: "https://developers.google.com/tenor/guides/quickstart"
```

When a skill with config is first loaded, Hermes prompts you for the values and stores them in `config.yaml` under `skills.config.*`. Manage skill config from the CLI with `hermes skills config <skill>` (interactive) or inspect it with `hermes config show | grep '^skills\.config'`.

## Creating Your Own Skill

Skills are just markdown files with YAML frontmatter, so creating one takes under five minutes. The four steps are:

1. **Create the directory** — `mkdir -p ~/.hermes/skills/my-category/my-skill`.
2. **Write `SKILL.md`** — frontmatter (`name`, `description`, `version`, `metadata.hermes.tags`/`category`) followed by the body sections that teach the workflow:

```markdown title="~/.hermes/skills/my-category/my-skill/SKILL.md"
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
metadata:
  hermes:
    tags: [my-tag, automation]
    category: my-category
---

# My Skill

## When to Use
Use this skill when the user asks about [specific topic] or needs to [specific task].

## Procedure
1. First, check if [prerequisite] is available
2. Run `command --with-flags`
3. Parse the output and present results

## Pitfalls
- Common failure: [description]. Fix: [solution]

## Verification
Run `check-command` to confirm the result is correct.
```

3. **Add reference files (optional)** — supporting `references/`, `templates/`, and `scripts/` files the agent loads on demand, referenced from `SKILL.md` via `skill_view("my-skill", "references/api-docs.md")`.
4. **Test it** — start a new session and try it: `hermes chat -q "/my-skill help me with the thing"`. The skill appears automatically — no registration needed; drop it in `~/.hermes/skills/` and it is live.

The agent can also create and update skills itself using `skill_manage` — after solving a complex problem, Hermes may offer to save the approach as a skill for next time.

## Per-Platform Skill Management

Run `hermes skills` to open an interactive TUI that enables or disables skills per platform (CLI, Telegram, Discord, etc.). This is useful when you want certain skills available only in specific contexts — for example keeping development skills off Telegram.

## Skills vs Memory

Both skills and memory persist across sessions but serve different purposes:

| | Skills | Memory |
|---|---|---|
| **What** | Procedural knowledge — how to do things | Factual knowledge — what things are |
| **When** | Loaded on demand, only when relevant | Injected into every session automatically |
| **Size** | Can be large (hundreds of lines) | Should be compact (key facts only) |
| **Cost** | Zero tokens until loaded | Small but constant token cost |
| **Who creates** | You, the agent, or installed from Hub | The agent, based on conversations |

**Rule of thumb:** if you would put it in a reference document, it is a skill; if you would put it on a sticky note, it is memory.

## Tips

Keep skills **focused** (one specific task beats "all of DevOps"); **let the agent create skills** after complex multi-step tasks, since agent-authored skills capture the exact workflow including discovered pitfalls; **use categories** (subdirectories like `~/.hermes/skills/devops/`) to keep the list manageable; and **update skills when they go stale** — unmaintained skills become liabilities.

**Source**: `inbox/hermes_agent_docs/guides/work-with-skills.md` · https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
**Last Updated**: 2026-06-19
**Status**: Active
