---
tags:
  - resource
  - documentation
  - claude_code
  - memory
  - managed_settings
keywords:
  - managed policy claude.md
  - organization-wide claude.md
  - claudemd key
  - managed-settings.json
  - claudemdexcludes
  - managed settings vs claude.md
  - deploy claude code across teams
  - mdm group policy
topics:
  - Claude Code
  - Memory
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/memory
access_control_group: ["general"]
---

# Manage CLAUDE.md for Large Teams

## Overview

For organizations deploying Claude Code across teams, you can centralize instructions and control which `CLAUDE.md` files are loaded. This note covers the two team-scale management procedures: deploying an organization-wide **managed-policy CLAUDE.md** (a centrally managed file that applies to all users on a machine and cannot be excluded by individual settings), and **excluding** ancestor CLAUDE.md files that aren't relevant to your work via the `claudeMdExcludes` setting. It also covers the decision of when to put guidance in a managed CLAUDE.md versus when to enforce it through managed settings.

## Deploy organization-wide CLAUDE.md

Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings.

**Step 1 — Create the file at the managed policy location:**

- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux and WSL: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`

**Step 2 — Deploy with your configuration management system:**

Use MDM, Group Policy, Ansible, or similar tools to distribute the file across developer machines. (For other organization-wide configuration options, see [managed settings](https://code.claude.com/docs/en/permissions#managed-settings).)

### The `claudeMd` key

The `claudeMd` key lets you put managed CLAUDE.md content directly inside `managed-settings.json` instead of deploying a separate file:

```json
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
```

- **Scope**: every Claude Code session on the machine, in every repository. For repository-specific guidance, commit a project CLAUDE.md instead.
- **Precedence**: same as a managed CLAUDE.md file. Loads before user and project CLAUDE.md.
- **Where it's honored**: managed and policy settings only. Setting `claudeMd` in user, project, or local settings has no effect.

## Managed CLAUDE.md vs. managed settings

A managed CLAUDE.md and [managed settings](https://code.claude.com/docs/en/settings#settings-files) serve different purposes. Use settings for technical enforcement and CLAUDE.md for behavioral guidance. Settings rules are enforced by the client regardless of what Claude decides to do; CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer.

| Concern | Configure in |
| :--- | :--- |
| Block specific tools, commands, or file paths | Managed settings: `permissions.deny` |
| Enforce sandbox isolation | Managed settings: `sandbox.enabled` |
| Environment variables and API provider routing | Managed settings: `env` |
| Authentication method and organization lock | Managed settings: `forceLoginMethod`, `forceLoginOrgUUID` |
| Code style and quality guidelines | Managed CLAUDE.md |
| Data handling and compliance reminders | Managed CLAUDE.md |
| Behavioral instructions for Claude | Managed CLAUDE.md |

## Exclude specific CLAUDE.md files

In large monorepos, ancestor CLAUDE.md files may contain instructions that aren't relevant to your work. The `claudeMdExcludes` setting lets you skip specific files by path or glob pattern.

This example excludes a top-level CLAUDE.md and a rules directory from a parent folder. Add it to `.claude/settings.local.json` so the exclusion stays local to your machine:

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Patterns are matched against absolute file paths using glob syntax. You can configure `claudeMdExcludes` at any [settings layer](https://code.claude.com/docs/en/settings#settings-files) — user, project, local, or managed policy — and arrays merge across layers.

**Managed policy CLAUDE.md files cannot be excluded.** This ensures organization-wide instructions always apply regardless of individual settings.

**Source**: https://code.claude.com/docs/en/memory
**Last Updated**: 2026-06-13
**Status**: Active
