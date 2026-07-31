---
tags:
  - resource
  - documentation
  - claude_code
  - large_codebases
  - skills
keywords:
  - per-directory skills
  - paths-scoped skill
  - keep skills discoverable
  - skill descriptions shortened
  - centralize conventions plugin
  - sessionstart hook plugin recommender
  - skill_activated otel event
  - layering stops scaling
topics:
  - Claude Code
  - Large Codebases
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/large-codebases
access_control_group: ["general"]
---

# Large Codebases — Per-Directory Skills and Centralizing Conventions

## Overview

As a monorepo or large single-tree codebase grows, two scaling problems appear: per-directory instructions multiply faster than any one developer can govern them, and the set of skills Claude must choose from grows large enough to crowd context. This note is the procedure for the last layer of large-codebase configuration — giving each subdirectory **skills scoped to its own stack** that load only on demand, keeping that skill list discoverable, and — when per-directory CLAUDE.md files stop scaling — **centralizing conventions** into skills, plugins, or MCP servers that a platform team owns. It closes with the combined `packages/api/` configuration that pulls every large-codebase setting together.

This note covers only the skills/plugins/MCP layer. The read-reduction and worktree settings it sits on top of are in [`cc_large_codebase_reduce_reads_and_worktrees`](cc_large_codebase_reduce_reads_and_worktrees.md), the CLAUDE.md layering it eventually replaces is in [`cc_large_codebase_claude_md_layering`](cc_large_codebase_claude_md_layering.md), and the strategic framing is in [`cc_large_codebase_strategy`](cc_large_codebase_strategy.md). The skills and plugins systems themselves are referenced via their own pages, not re-digested here.

## Add per-directory skills

Any subdirectory can define [skills](https://code.claude.com/docs/en/skills) scoped to its own stack. A skill loads on demand when Claude determines it's relevant, so API-specific tooling doesn't consume context during frontend work.

Skills live under `.claude/skills/` inside the directory. Commit them alongside that area's code so anyone who clones the repository gets them. In a monorepo this can be one set of skills per package. In a large single-tree codebase it's one set per subsystem such as `src/db/.claude/skills/`.

Create a skill directory inside the subdirectory:

```bash
mkdir -p packages/api/.claude/skills/api-testing
```

Then write `SKILL.md` inside that directory, here `packages/api/.claude/skills/api-testing/SKILL.md`. The frontmatter carries the `name` and `description` that always load; the body holds the procedure that loads only when the skill is chosen:

```markdown
---
name: api-testing
description: Testing patterns for the API package. Use when writing or modifying tests in packages/api/.
---

## Test structure

Tests are in `src/__tests__/` mirroring the `src/` directory structure.
Each route file has a corresponding `.test.ts` file.
```

A different subdirectory holds different skills the same way: `packages/web/.claude/skills/component-patterns/` describes the frontend's component conventions instead of testing. When Claude works on a file in `packages/api/`, it loads the api-testing skill; when it works in `packages/web/`, it loads component-patterns instead. Neither directory's skills load during the other's tasks.

You can also scope a skill by file pattern instead of by placement. The [`paths` frontmatter field](https://code.claude.com/docs/en/skills#frontmatter-reference) takes glob patterns, and Claude loads the skill automatically only when it works with matching files. Use this for a skill that lives in the repository root's `.claude/skills/` but applies only to certain files wherever they appear, such as a database-migration skill scoped to `**/migrations/**`.

### Keep skills discoverable

With skills spread across many directories, the list Claude chooses from can grow large. Claude picks a skill by reading every discovered skill's name and description, and only the chosen skill's full content loads into context. Keeping that list small and writing descriptions that survive shortening keeps the choice accurate.

Which skills are in scope depends on where you start Claude:

- **From a subdirectory such as `packages/api/`**: skills from that directory, every parent up to the
  repository root, and the user and enterprise levels.
- **From the repository root**: skills from every subdirectory Claude touches during the session, which can
  accumulate into the hundreds.
- **After adding a sibling with `--add-dir`**: that sibling's skills load too. The `additionalDirectories`
  setting grants file access only and does not load skills.

Names always load, but [descriptions are shortened when there are many](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short), which can strip the keywords Claude uses to decide whether a skill applies. Keep descriptions short and lead with words a request would contain, like "writing or modifying tests in `packages/api/`".

For skills that many directories share, such as PR conventions or a deploy checklist, place them in the repository root's `.claude/skills/` so they load from any starting directory. When shared skills need their own version history or must work across repositories, package them as a [plugin](https://code.claude.com/docs/en/plugins) instead. Plugin skills use a `plugin-name:skill-name` namespace, so they never collide with per-directory skills, and a platform team can version and update them in one place.

To find which skills go unused, enable the OpenTelemetry [logs exporter](https://code.claude.com/docs/en/monitoring-usage) and set `OTEL_LOG_TOOL_DETAILS=1` so skill names are recorded verbatim instead of redacted. The [`skill_activated` event](https://code.claude.com/docs/en/monitoring-usage#skill-activated-event) records every invocation in its `skill.name` attribute, and `invocation_trigger` records whether a command, Claude, or a nested skill invoked it, which tells you what to consolidate or retire.

## Centralize conventions when layering stops scaling

Per-directory CLAUDE.md files can become hard to govern as the codebase grows. Conventions drift, files go stale, and no one owns the root. Solving that typically falls to the team that maintains the repository's Claude Code setup rather than to each developer working in their own area.

Move conventions and reference content out of always-loaded CLAUDE.md and into mechanisms that load on demand:

- **[Skills](https://code.claude.com/docs/en/skills)**: reference material Claude loads only when relevant to
  the task.
- **[Plugins](https://code.claude.com/docs/en/plugins)**: versioned bundles of skills, hooks, and commands
  that a platform team owns centrally.
- **[MCP servers](https://code.claude.com/docs/en/mcp)**: if your organization already runs a code search or RAG index over the repository, expose it as an MCP tool so Claude queries it instead of reading files directly.

See [server-managed or endpoint-managed settings](https://code.claude.com/docs/en/server-managed-settings#choose-between-server-managed-and-endpoint-managed-settings) for how platform teams can enforce these centrally.

### Recommend the right plugin at session start

Once conventions live in plugins, a teammate starting Claude in an unfamiliar part of the tree has no signal about which plugin that area's owners maintain. A [`SessionStart` hook](https://code.claude.com/docs/en/hooks#sessionstart) can close that gap, since anything the hook prints to stdout is added to Claude's context before the first prompt.

For example, you can write a script that reads the launch directory from the [hook input](https://code.claude.com/docs/en/hooks#common-input-fields), looks it up in a path-to-plugin map committed to the repository, and prints the recommendation for Claude to relay in its first reply. See [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) to write and register the hook.

## Put it together

The combined configuration below uses the monorepo layout. The same files work for any subdirectory in a large single tree. Project settings load only from the directory you start Claude in, so each subdirectory's `.claude/settings.json` must be self-contained rather than layered on a root file.

The example commits `worktree`, `additionalDirectories`, and the `Read` deny rules in `.claude/settings.json` so every developer in `packages/api/` gets the same sibling access, sparse paths, and exclusions. The file below is the committed per-area settings for `packages/api/`:

```json
{
  "worktree": {
    "sparsePaths": [
      ".claude",
      "packages/api",
      "packages/shared"
    ],
    "symlinkDirectories": [
      "node_modules"
    ]
  },
  "permissions": {
    "additionalDirectories": [
      "../shared"
    ],
    "deny": [
      "Read(./**/dist/**)",
      "Read(./**/build/**)"
    ]
  }
}
```

Because this session starts from `packages/api/`, sibling packages' CLAUDE.md files are already out of scope, so `claudeMdExcludes` is not needed here. The `additionalDirectories` entry applies when you start Claude from `packages/api/` directly; inside a worktree created from this session, the working directory is the worktree root, so this settings file does not load. The sibling packages are already reachable inside the worktree, but the deny rules need a second copy in the repository root's `.claude/settings.json` so worktree sessions pick them up.

After setup, the repository has this layout:

```text
monorepo/
  CLAUDE.md
  .claude/settings.json                           # deny rules for worktree sessions
  packages/
    api/
      CLAUDE.md
      .claude/settings.json                       # worktree, additionalDirectories, deny rules
      .claude/skills/api-testing/SKILL.md
    web/
      CLAUDE.md
      .claude/skills/component-patterns/SKILL.md
    shared/
      CLAUDE.md
```

With this setup, starting Claude from `packages/api/` loads the root CLAUDE.md and `packages/api/CLAUDE.md` while skipping `packages/web/CLAUDE.md`; can read and edit files in `packages/api/` and `packages/shared/`; skips reads of build output under `dist/` and `build/`; has the api-testing skill available on demand; and creates worktrees containing `.claude/`, `packages/api/`, `packages/shared/`, and root-level files, with the deny rules applied across the worktree from the root settings file.

**Source**: https://code.claude.com/docs/en/large-codebases
**Last Updated**: 2026-06-13
**Status**: Active
