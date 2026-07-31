---
tags:
  - resource
  - documentation
  - claude_code
  - skills
  - procedure
keywords:
  - create a skill
  - skill.md
  - first skill
  - skill directory
  - supporting files
  - dynamic context injection
  - personal skills folder
  - auto-trigger vs slash invoke
topics:
  - Claude Code
  - Skills
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/skills
access_control_group: ["general"]
---

# Claude Code — Create a Skill

## Overview

A skill is a `SKILL.md` file with two parts — YAML frontmatter between `---` markers that tells Claude when to use the skill, and markdown content with the instructions Claude follows when the skill runs. This note is the end-to-end procedure for authoring your first skill: make the directory, write `SKILL.md`, and test it (let Claude auto-trigger it, or invoke it directly with `/skill-name`). It then covers adding supporting files so a skill can carry reference material, examples, and scripts beyond the main `SKILL.md`.

The worked example builds `summarize-changes`, a skill that summarizes uncommitted git changes and flags anything risky. It pulls the live diff into the prompt before Claude reads it, so the response is grounded in the actual working tree rather than what Claude can guess from open files.

## Create your first skill

### Step 1 — Create the skill directory

Create a directory for the skill in your personal skills folder. Personal skills are available across all your projects. The directory name becomes the command you type.

```bash
mkdir -p ~/.claude/skills/summarize-changes
```

### Step 2 — Write SKILL.md

Every skill needs a `SKILL.md` with YAML frontmatter (when to use the skill) plus markdown content (the instructions Claude follows). The directory name becomes the command, and the `description` helps Claude decide when to load the skill automatically. Save this to `~/.claude/skills/summarize-changes/SKILL.md`:

```yaml
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullet points, then list any risks you notice such as missing error handling, hardcoded values, or tests that need updating. If the diff is empty, say there are no uncommitted changes.
```

The `` !`git diff HEAD` `` line uses dynamic context injection: Claude Code runs the command and replaces the line with its output before Claude sees the skill content, so the instructions arrive with the current diff already inlined.

### Step 3 — Test the skill

Open a git project, make a small edit to any file, and start Claude Code by running `claude`. There are two ways to test. Let Claude invoke it automatically by asking something that matches the description (for example, "What did I change?"), or invoke it directly with the skill name:

```text
/summarize-changes
```

Either way, Claude responds with a short summary of your edit and a list of risks.

## Add supporting files

A skill can include multiple files in its directory. This keeps `SKILL.md` focused on the essentials while letting Claude access detailed reference material only when needed — large reference docs, API specifications, or example collections don't need to load into context every time the skill runs. Each skill is a directory with `SKILL.md` as the required entrypoint:

```text
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

Reference supporting files from `SKILL.md` so Claude knows what each file contains and when to load it (for example, a line like *"For complete API details, see reference.md"* that points at the bundled `reference.md` file). The docs advise keeping `SKILL.md` under 500 lines and moving detailed reference material to separate files.

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
