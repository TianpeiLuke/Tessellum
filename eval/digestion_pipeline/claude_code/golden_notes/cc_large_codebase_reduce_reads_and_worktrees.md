---
tags:
  - resource
  - documentation
  - claude_code
  - large_codebases
  - context_management
keywords:
  - reduce file reads
  - read deny rules
  - code intelligence plugin
  - language server lookups
  - worktree sparsepaths
  - symlinkdirectories
  - additionaldirectories
  - add-dir
  - subagent worktree isolation
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

# Reduce File Reads and Scope Worktrees in a Large Codebase

## Overview

In a large codebase, instructions are only part of what fills Claude's context; **file reads** are a second cost that grows with the tree. This procedure covers the two `large-codebases` mechanism families that cut and scope reads: **reduce what Claude reads** (block reads of generated/vendored code, and replace exhaustive file scans with language-server lookups via a code intelligence plugin) and **scope worktrees and file access** (check out only the directories a task needs with `worktree.sparsePaths`, and grant cross-package/repository access with `additionalDirectories` or `--add-dir`).

Each setting is independent and layers with the others. Each section states whether a settings file is committed (`.claude/settings.json`) or personal (`.claude/settings.local.json`), and where it must live relative to where you start Claude. The examples refer to the example monorepo (`packages/api/`, `packages/web/`, `packages/shared/`); the same patterns apply to a subsystem directory such as `src/backend/` in a large single tree.

## Reduce what Claude reads

### Block reads of generated and vendored code

Claude's content searches respect `.gitignore` by default, so paths already listed there — such as `node_modules/`, `dist/`, and `build/` — stay out of search results with no additional configuration.

For paths that are **checked in**, such as a vendored SDK or committed generated code, add `Read` deny rules in `permissions.deny` to block Claude from opening those files even when a search lists them. The example below blocks build artifacts and a vendored SDK:

```json .claude/settings.json theme={null}
{
  "permissions": {
    "deny": [
      "Read(./**/dist/**)",
      "Read(./**/build/**)",
      "Read(./**/*.generated.*)",
      "Read(./vendor/**)"
    ]
  }
}
```

To apply these exclusions for everyone, commit them to `.claude/settings.json`; to keep them personal, use `.claude/settings.local.json`. Like other project settings on this page, these files load only from your starting directory — place them at the repository root if you start Claude there, or in each package's `.claude/` if you start from subdirectories. To enforce the same deny rules in every session regardless of starting directory, set them in managed settings, which user and project settings cannot override.

Deny rules cover Claude's built-in file tools and recognized Bash file commands — including `cat`, `head`, `grep`, and `find` — when a denied path is passed as an argument. They do **not** filter denied paths out of a recursive search's output, and they do not cover arbitrary subprocesses that open files themselves. For the full pattern syntax, see [Read and Edit permission rules](https://code.claude.com/docs/en/permissions).

### Reduce file reads with code intelligence

In a large codebase, finding where a symbol is defined or used can cost many file reads and grep calls. A code intelligence plugin connects Claude to a **language server** so it can jump to definitions, find references, and surface type errors directly instead of scanning the tree. The official marketplace has plugins for TypeScript, Python, Go, Rust, and other common languages. The example below installs the TypeScript plugin:

```shell theme={null}
/plugin install typescript-lsp@claude-plugins-official
```

To enable a plugin for everyone in the repository rather than installing it yourself, add it to the `enabledPlugins` project setting. Code intelligence plugins require the language's language server binary on each developer's machine. Installing from the official marketplace requires network access to GitHub, where the marketplace is hosted; on a restricted network, add the marketplace from an internal Git host or local path instead (see [Discover plugins — code intelligence](https://code.claude.com/docs/en/discover-plugins)).

This pairs well with `claudeMdExcludes` and the `Read` deny rules above: those keep irrelevant content out of context, and code intelligence keeps Claude from reading through what remains to locate a definition.

## Scope worktrees and file access

These settings control what is on disk in worktrees and which directories Claude can read and write beyond your starting point.

### Check out only the directories you need

The `--worktree` flag starts a session in a new git worktree so changes stay isolated from your main checkout. By default it checks out the entire repository. In a large repository, the `worktree.sparsePaths` setting uses git sparse-checkout to write only the listed directories plus root-level files to disk, so worktrees start faster and use less space. To avoid duplicating large directories like `node_modules` across worktrees, pair `sparsePaths` with `symlinkDirectories` in the same `.claude/settings.json`:

```json .claude/settings.json theme={null}
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
  }
}
```

When Claude creates a worktree, it checks out only `.claude/`, `packages/api/`, and `packages/shared/` instead of the full tree, and creates a symlink from each worktree's `node_modules/` back to the main repository's copy rather than duplicating it on disk. If everyone working in this directory needs the same paths, commit the setting; to add paths for yourself, use `.claude/settings.local.json` — the lists merge across scopes, so a local file can add paths to the committed list but not remove them.

Rules that govern `sparsePaths`:

* Paths are **relative to the repository root**, regardless of which subdirectory you start Claude from. Any directory paths work here, not only package roots.
* **List directories, not individual files.** Root-level files like `package.json`, `tsconfig.base.json`, and lock files are always checked out alongside the directories you list. Root-level directories are not — so include `.claude` in the list if you want the repository root's `.claude/settings.json`, `.claude/rules/`, or `.claude/skills/` available inside the worktree.

This is particularly useful for **subagent worktree isolation**: subagents are parallel Claude instances spawned for subtasks, and each one that runs in a worktree gets a lightweight checkout instead of the full tree. All worktrees in a session share the same `sparsePaths`, so if one subagent needs `packages/api/` and another needs `packages/web/`, list both.

The `sparsePaths` and `symlinkDirectories` settings are read from your starting directory **before** the worktree is created. After creation, the session's working directory is the worktree root, not the subdirectory you launched from, so project settings inside the worktree load from the worktree root's `.claude/settings.json` (the checked-out copy of the repository root's file). Put any other settings you need inside worktrees, such as permission rules or hooks, in the repository root's `.claude/settings.json`. For the full reference, see [Worktree settings](https://code.claude.com/docs/en/settings).

### Grant access across packages or repositories

This section applies when you start Claude from a subdirectory, or when a task spans multiple checkouts. If you start from the repository root in a single large tree, Claude already has access to every file and you can skip this.

When you start Claude from `packages/api/`, it can read and write files within that directory. If a task requires changes across packages — such as updating a shared type that both `api` and `web` import — you must grant access to the sibling directory. The same mechanism grants access to a separately-checked-out repository. The `additionalDirectories` setting in `.claude/settings.json` gives Claude access to directories outside the working directory:

```json .claude/settings.json theme={null}
{
  "permissions": {
    "additionalDirectories": [
      "../shared",
      "../web"
    ]
  }
}
```

Relative paths resolve against the directory you start Claude from. With this configuration, Claude can read and edit files in `packages/shared/` and `packages/web/` while working from `packages/api/`. You can also grant access at runtime without editing settings by passing `--add-dir` when you start Claude:

```bash theme={null}
claude --add-dir ../shared
```

However you add a directory, Claude can read and edit files in it. Whether the directory's CLAUDE.md, `.claude/rules/`, and skills **also load** depends on how you added it:

| Added with | Loads CLAUDE.md and rules | Loads skills |
| :--- | :--- | :--- |
| `additionalDirectories` setting | Never | Never |
| `--add-dir` flag or `/add-dir` command | Only with the environment variable below | Yes |

To load CLAUDE.md and rules files from a directory added with `--add-dir` or `/add-dir`, set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` environment variable before the `claude --add-dir ../shared` invocation. The environment variable has no effect on directories listed in the `additionalDirectories` setting. For sibling directories that everyone in this area needs, commit `additionalDirectories` to `.claude/settings.json`; for a personal selection or one-off access, use `.claude/settings.local.json` or pass `--add-dir` at launch. See [Load from additional directories](https://code.claude.com/docs/en/memory) for details.

**Source**: https://code.claude.com/docs/en/large-codebases
**Last Updated**: 2026-06-13
**Status**: Active
