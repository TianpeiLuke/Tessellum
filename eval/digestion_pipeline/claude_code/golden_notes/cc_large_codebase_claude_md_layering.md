---
tags:
  - resource
  - documentation
  - claude_code
  - large_codebases
  - claude_md
keywords:
  - per-directory claude.md
  - layer claude.md files
  - root claude.md
  - claudemdexcludes
  - path-scoped rules
  - on-demand load
  - settings scope merge
  - monorepo conventions
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

# Layer CLAUDE.md Files by Directory in a Large Codebase

## Overview

In a large codebase, a single `CLAUDE.md` at the repository root tends to either grow to cover every subsystem's conventions — costing context on instructions unrelated to the current task — or stay too generic to be useful. The fix is to **split instructions across per-directory files**: Claude Code loads repository-wide rules from the root plus only the conventions for the code you're working in. This note covers the layering mechanism (root + per-subdirectory `CLAUDE.md`), how to keep those files current, when to choose per-directory `CLAUDE.md` versus path-scoped rules, and how the `claudeMdExcludes` setting skips files you never work in.

For how CLAUDE.md files load and interact internally, see [Memory and project instructions](https://code.claude.com/docs/en/memory).

## Layer CLAUDE.md files by directory

Claude Code loads every `CLAUDE.md` file from your working directory and every parent directory at launch, then loads each subdirectory's file on demand when it reads files there. A root file sets repository-wide rules and each subdirectory adds its own.

A common split is two levels:

- **Root `CLAUDE.md`**: instructions that apply everywhere, such as coding standards, commit conventions, and repository layout.
- **Per-subdirectory `CLAUDE.md`**: conventions specific to that area's stack. In a monorepo that's one per package. In a large single tree it's one per subsystem such as `src/db/` or `src/api/`.

Commit these files to the repository so teammates inherit them. Each directory's owner typically maintains its file.

The root `CLAUDE.md` orients Claude to the repository structure:

```markdown CLAUDE.md theme={null}
This is a monorepo with three packages under packages/:

- packages/api: Node.js REST API with Express, TypeScript, and PostgreSQL
- packages/web: React frontend with Vite, TypeScript, and TailwindCSS
- packages/shared: shared TypeScript utilities used by both api and web

Run commands from the package directory, not the monorepo root.
Each package has its own tsconfig.json, package.json, and test suite.
```

Each subdirectory's `CLAUDE.md`, here `packages/api/CLAUDE.md`, adds context specific to that area's stack:

```markdown packages/api/CLAUDE.md theme={null}
This package is the REST API server.

- Run tests: `npm test` (uses Vitest)
- Run dev server: `npm run dev` (port 3001)
- Database migrations: `npm run migrate`
- Environment variables: copy `.env.example` to `.env`

API routes are in src/routes/. Each route file exports an Express router.
Database queries use Knex in src/db/. Never write raw SQL strings in route handlers.
```

When you start Claude from `packages/api/`, it loads both `packages/api/CLAUDE.md` and the root `CLAUDE.md`. Claude sees the local instructions alongside the repository-wide rules, with no instructions from `packages/web/` in context. The same holds for any subdirectory in a non-monorepo tree.

### Keep the files current

A few ways to keep the files current as the codebase and models change:

- **Review in pull requests**: treat CLAUDE.md edits like any other documentation change so conventions track the code.
- **Revisit after major model releases**: instructions that worked around an older model's limitation may become overhead once a newer model handles the case on its own. For example, a rule that forces single-file refactors can be deleted once the limitation is gone.
- **Add a Stop hook that proposes updates**: a [`Stop` hook](https://code.claude.com/docs/en/hooks#stop) receives the path to the session transcript when Claude finishes responding, so a script can review the session and propose CLAUDE.md updates while the gap it exposed is fresh.

## Choose between per-directory CLAUDE.md and path-scoped rules

Per-directory `CLAUDE.md` files and [path-scoped rules](https://code.claude.com/docs/en/memory#path-specific-rules) under `.claude/rules/` both let you target instructions to part of the tree. They differ in where the file lives and when it loads.

| Approach | File location | Loads when | Use when |
| :--- | :--- | :--- | :--- |
| Per-directory `CLAUDE.md` | Inside the directory, alongside its code | At launch when started from that directory, or on demand when Claude reads a file there | Directory owners maintain their own conventions; instructions are versioned with the code |
| Path-scoped rule in `.claude/rules/` | Central `.claude/` at the repo root | When Claude works with a file matching the rule's `paths:` glob | You want all conventions in one place, or the same rule applies to many scattered paths |

For a comparison that also covers skills, see [Compare similar features](https://code.claude.com/docs/en/features-overview#compare-similar-features).

## Exclude irrelevant CLAUDE.md files

When you start Claude from the repository root, each subdirectory's CLAUDE.md loads as soon as Claude reads a file in that directory. The `claudeMdExcludes` setting skips specific files by path or glob pattern so they never load.

Use this for directories you never work in, such as other teams' packages, legacy code, or vendored subtrees. The exclusion list is static, not a per-task switch. To focus on one package today and another tomorrow, start Claude from that package's directory instead of editing exclusions.

If you only want these exclusions for yourself, put the setting in `.claude/settings.local.json`. Claude Code gitignores that file when it creates it; since you're creating it by hand here, add it to your gitignore. Patterns use glob syntax matched against **absolute file paths**, so start relative-style patterns with `**/` to match anywhere in the tree. The example below excludes packages owned by other teams:

```json .claude/settings.local.json theme={null}
{
  "claudeMdExcludes": [
    "**/packages/admin-dashboard/**",
    "**/packages/legacy-*/**"
  ]
}
```

This skips every CLAUDE.md and rules file under those packages. The root CLAUDE.md and the packages you do work in still load normally.

Other common patterns: `"**/packages/*/CLAUDE.md"` excludes every package's CLAUDE.md while keeping the root; `"**/packages/web/**"` excludes everything under the web package, including rules; and `"/home/user/monorepo/legacy/CLAUDE.md"` excludes one specific file by absolute path.

Managed policy CLAUDE.md files **cannot be excluded**, so organization-wide instructions always apply. You can set `claudeMdExcludes` at any [settings scope](https://code.claude.com/docs/en/settings#configuration-scopes): user, project, local, or managed. **Arrays merge across scopes**, so a team can set project-level defaults while individuals add local overrides.

For the full exclusion documentation, see [Exclude specific CLAUDE.md files](https://code.claude.com/docs/en/memory#exclude-specific-claude-md-files).

**Source**: https://code.claude.com/docs/en/large-codebases
**Last Updated**: 2026-06-13
**Status**: Active
