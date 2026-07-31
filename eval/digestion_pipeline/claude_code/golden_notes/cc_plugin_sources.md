---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - marketplace
keywords:
  - plugin source
  - marketplace.json source field
  - github source
  - git-subdir source
  - npm plugin source
  - ref and sha pinning
  - relative path source
  - plugin cache
  - marketplace source vs plugin source
topics:
  - Claude Code
  - Plugin Marketplaces
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/plugin-marketplaces
access_control_group: ["general"]
---

# Claude Code — Plugin Sources

## Overview

A **plugin source** tells Claude Code where to fetch each individual plugin listed in a marketplace. Sources are set in the `source` field of each plugin entry in `marketplace.json`, and there are five kinds: a **relative path** (a string), or one of four object-typed sources — `github`, `url`, `git-subdir`, and `npm`. Once a plugin is cloned or copied onto the local machine, it is copied into the local **versioned plugin cache** at `~/.claude/plugins/cache`.

Sources are distinct from the **marketplace source** (where the `marketplace.json` catalog itself is fetched): a marketplace source supports `ref` but not `sha`, while a plugin source supports both. The git-based source types (`github`, `url`, `git-subdir`) accept optional `ref` (branch/tag) and `sha` (exact commit) pins; when both are set, the `sha` is the effective pin, so installation succeeds even if the branch or tag named by `ref` was deleted upstream, as long as the commit is still reachable.

## The five source types

| Source        | Type                            | Fields                             | Notes                                                                                                                                             |
| ------------- | ------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relative path | `string` (e.g. `"./my-plugin"`) | none                               | Local directory within the marketplace repo. Must start with `./`. Resolved relative to the marketplace root, not the `.claude-plugin/` directory |
| `github`      | object                          | `repo`, `ref?`, `sha?`             |                                                                                                                                                   |
| `url`         | object                          | `url`, `ref?`, `sha?`              | Git URL source                                                                                                                                    |
| `git-subdir`  | object                          | `url`, `path`, `ref?`, `sha?`      | Subdirectory within a git repo. Clones sparsely to minimize bandwidth for monorepos                                                               |
| `npm`         | object                          | `package`, `version?`, `registry?` | Installed via `npm install`                                                                                                                       |

### Relative paths

For plugins in the same repository, use a path starting with `./`. Paths resolve relative to the **marketplace root** (the directory containing `.claude-plugin/`), so `./plugins/my-plugin` points to `<repo>/plugins/my-plugin` even though `marketplace.json` lives at `<repo>/.claude-plugin/marketplace.json`. Do not use `../` to reference paths outside the marketplace root. Relative paths only work when users add the marketplace via Git (GitHub, GitLab, or git URL) — if a user adds the marketplace via a direct URL to the `marketplace.json` file, relative paths will not resolve (use GitHub, npm, or git URL sources for URL-based distribution).

### GitHub repositories

The `github` source requires `repo` in `owner/repo` format; `ref` (branch or tag, defaults to the repository default branch) and `sha` (full 40-character commit SHA) are optional. You can pin to a specific branch, tag, or commit:

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

### Git repositories

The `url` source requires `url` — a full git repository URL (`https://` or `git@`); the `.git` suffix is optional, so Azure DevOps and AWS CodeCommit URLs without the suffix work. It also accepts optional `ref` and `sha` pins:

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

### Git subdirectories

Use `git-subdir` to point to a plugin that lives inside a subdirectory of a git repo. Claude Code uses a **sparse, partial clone** to fetch only the subdirectory, minimizing bandwidth for large monorepos. It requires `url` (a git URL, GitHub `owner/repo` shorthand, or SSH URL like `git@github.com:owner/repo.git`) and `path` (the subdirectory containing the plugin, e.g. `"tools/claude-plugin"`); `ref` and `sha` are optional.

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

### npm packages

Plugins distributed as npm packages are installed using `npm install`, working with any package on the public npm registry or a private registry. The `npm` source requires `package` (a package name or scoped package like `@org/plugin`); optional `version` is a version or version range (`2.1.0`, `^2.0.0`, `~1.5.0`) and optional `registry` is a custom npm registry URL (defaults to the system npm registry, typically npmjs.org).

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

## Advanced plugin entries

A plugin entry can combine a source with many optional fields, including custom paths for `commands`, `agents`, `hooks`, and `mcpServers`:

```json theme={null}
{
  "name": "enterprise-tools",
  "source": { "source": "github", "repo": "company/enterprise-plugin" },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit", "hooks": [
        { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh" }
      ] }
    ]
  },
  "strict": false
}
```

Key things to notice:

- **`commands` and `agents`**: you can specify multiple directories or individual files; paths are relative to the plugin root.
- **`${CLAUDE_PLUGIN_ROOT}`**: use this variable in hooks and MCP server configs to reference files within the plugin's installation directory — necessary because plugins are copied to a cache location when installed. For dependencies or state that should survive plugin updates, use `${CLAUDE_PLUGIN_DATA}` instead (see [Plugins reference — persistent data directory](https://code.claude.com/docs/en/plugins-reference)).
- **`strict: false`**: the plugin does not need its own `plugin.json` — the marketplace entry defines everything (the `strict` field is covered in [Marketplace JSON Schema](cc_marketplace_json_schema.md)).

## Marketplace sources vs plugin sources

These are different concepts that control different things:

- **Marketplace source** — where to fetch the `marketplace.json` catalog itself. Set when users run `/plugin marketplace add` or in `extraKnownMarketplaces` settings. Supports `ref` (branch/tag) but **not** `sha`.
- **Plugin source** — where to fetch an individual plugin listed in the marketplace. Set in the `source` field of each plugin entry inside `marketplace.json`. Supports both `ref` (branch/tag) and `sha` (exact commit).

A marketplace hosted at `acme-corp/plugin-catalog` (marketplace source) can list a plugin fetched from `acme-corp/code-formatter` (plugin source). The two point to different repositories and are pinned independently.

**Source**: https://code.claude.com/docs/en/plugin-marketplaces
**Last Updated**: 2026-06-13
**Status**: Active
