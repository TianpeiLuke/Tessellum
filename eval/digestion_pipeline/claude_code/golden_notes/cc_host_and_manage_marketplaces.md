---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - marketplaces
keywords:
  - host plugin marketplace
  - claude plugin marketplace add
  - private repository auth tokens
  - extraknownmarketplaces
  - enabledplugins
  - seed directory containers
  - version resolution release channels
  - marketplace cli subcommands
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/plugin-marketplaces
access_control_group: ["general"]
---

# Host and Manage Plugin Marketplaces

## Overview

Once a `marketplace.json` catalog exists, it is distributed by hosting it on a git service and managed through Claude Code's `claude plugin marketplace` CLI. This note covers the distribution half of the marketplace lifecycle: hosting on GitHub or any other git host, authenticating to private repositories, pushing marketplaces to teams via `extraKnownMarketplaces`/`enabledPlugins` settings, pre-populating plugins into containers with a seed directory, resolving plugin versions and running stable/latest release channels, the non-interactive `add`/`list`/`remove`/`update` subcommands, and a troubleshooting reference for common failures.

Authoring the catalog itself is covered by the [marketplace walkthrough](cc_plugin_marketplace_walkthrough.md) and the [marketplace JSON schema](cc_marketplace_json_schema.md); the admin-side `strictKnownMarketplaces` allowlist is summarized below under [Managed marketplace restrictions](#managed-marketplace-restrictions), with the full managed-settings reference at https://code.claude.com/docs/en/settings.

## Host and distribute marketplaces

### Host on GitHub (recommended)

GitHub is the easiest distribution method:

1. **Create a repository** for your marketplace.
2. **Add marketplace file**: create `.claude-plugin/marketplace.json` with your plugin definitions.
3. **Share with teams**: users add it with `/plugin marketplace add owner/repo`.

Benefits are built-in version control, issue tracking, and team collaboration features.

### Host on other git services

Any git host works (GitLab, Bitbucket, self-hosted servers). Users add it with the full repository URL, for example `/plugin marketplace add https://gitlab.com/company/plugins.git`.

### Private repositories

Claude Code can install plugins from private repositories. For **manual installation and updates**, it reuses your existing git credential helpers — HTTPS access via `gh auth login`, macOS Keychain, or `git-credential-store` works the same as in your terminal. SSH access works as long as the host is already in `known_hosts` and the key is loaded in `ssh-agent`, since Claude Code suppresses interactive SSH prompts for the host fingerprint and key passphrase.

**Background auto-updates** run at startup without credential helpers (interactive prompts would block startup). To enable auto-updates for private marketplaces, set an authentication token in your environment: GitHub uses `GITHUB_TOKEN` or `GH_TOKEN` (personal access token or GitHub App token), GitLab uses `GITLAB_TOKEN` or `GL_TOKEN`, and Bitbucket uses `BITBUCKET_TOKEN`. Set the token in your shell config (`.bashrc`, `.zshrc`) or pass it when running Claude Code:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

For CI/CD, configure the token as a secret environment variable; GitHub Actions automatically provides `GITHUB_TOKEN` for repositories in the same organization. (Full env-var reference: see https://code.claude.com/docs/en/settings.)

### Require marketplaces for your team

Configure a repository so team members are auto-prompted to install your marketplace when they trust the project folder. Add it to `.claude/settings.json` under `extraKnownMarketplaces`, and optionally pre-enable specific plugins with `enabledPlugins`:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

For full configuration options, see [Plugin settings](https://code.claude.com/docs/en/settings). If a local `directory` or `file` source uses a relative path, the path resolves against your repository's main checkout — when running from a git worktree the path still points at the main checkout, so all worktrees share the marketplace location. Marketplace state is stored once per user in `~/.claude/plugins/known_marketplaces.json`, not per project.

### Pre-populate plugins for containers

For container images and CI, pre-populate a plugins directory at build time so Claude Code starts with marketplaces and plugins already available without cloning at runtime. Set `CLAUDE_CODE_PLUGIN_SEED_DIR` to point at this directory. To layer multiple seed directories, separate paths with `:` (Unix) or `;` (Windows); Claude Code searches each in order and the first seed containing a given marketplace or plugin cache wins. The seed directory mirrors the structure of `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

To build a seed, run Claude Code once during image build, install the plugins you need, then copy the resulting `~/.claude/plugins` directory into the image. To skip the copy step, set `CLAUDE_CODE_PLUGIN_CACHE_DIR` to your target seed path during the build so plugins install directly there (e.g. `CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin marketplace add your-org/plugins`), then set `CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-seed` in the runtime environment.

Behavior details: the seed is **read-only** (auto-updates are disabled for seed marketplaces since `git pull` would fail on a read-only filesystem); **seed entries take precedence**, overwriting matching user entries on each startup (opt out of a seed plugin with `/plugin disable`, not by removing the marketplace); **path resolution** probes `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` at runtime rather than trusting paths stored in the seed's JSON, so the seed works even when mounted at a different path; **mutation is blocked** — `/plugin marketplace remove` or `update` against a seed-managed marketplace fails with guidance to ask the administrator to update the seed image; and it **composes with settings** (if `extraKnownMarketplaces`/`enabledPlugins` declare a marketplace already in the seed, Claude Code uses the seed copy). This works in interactive and non-interactive (`-p`) modes.

### Managed marketplace restrictions

Organizations requiring strict control over plugin sources can restrict which marketplaces users may add via the `strictKnownMarketplaces` setting in managed settings. The behavior depends on its value: **undefined** (the default) imposes no restrictions; an **empty array** `[]` is a complete lockdown (users cannot add any new marketplaces); a **list of sources** lets users add only marketplaces that match the allowlist exactly. Allow specific marketplaces with a list of source objects:

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

A `hostPattern` entry matches the marketplace host against a regex — the recommended approach for GitHub Enterprise Server or self-hosted GitLab; a `pathPattern` entry matches a filesystem path (use `".*"` to allow any path while still gating network sources). Restrictions are checked **before any network or filesystem operation** — on marketplace add and on plugin install, update, refresh, and auto-update — and the same enforcement applies to `blockedMarketplaces`; a marketplace added before the policy whose source no longer matches is refused for installs/updates. Matching is **exact** for most source types (GitHub `repo` plus any specified `ref`/`path`; the full URL for `url` sources) and is **not** normalized — a trailing slash, `.git` suffix, or `ssh://` vs `https://` count as different values, so prefer a `hostPattern` when one marketplace is cloneable by several URL forms. Because it lives in managed settings, individual users and project configs cannot override it. `strictKnownMarketplaces` only restricts what may be added; to also auto-register allowed marketplaces, pair it with `extraKnownMarketplaces` in the same `managed-settings.json`. Full reference (all source types, comparison with `extraKnownMarketplaces`): see https://code.claude.com/docs/en/settings.

### Version resolution and release channels

Plugin versions determine cache paths and update detection: if the resolved version matches what a user already has, `/plugin update` and auto-update skip the plugin. Claude Code resolves a plugin's version from the **first** of these that is set:

1. `version` in the plugin's `plugin.json`
2. `version` in the plugin's marketplace entry
3. The git commit SHA of the plugin's source

For git-based source types (`github`, `url`, `git-subdir`, and relative paths inside a git-hosted marketplace) you can omit `version` entirely and every new commit is treated as a new version — the simplest setup for internal or actively-developed plugins. **Warning**: setting `version` pins the plugin; pushing new commits without changing the string does nothing for existing users (Claude Code sees the same version and keeps the cached copy), so bump it on every release or omit it. Avoid setting `version` in both `plugin.json` and the marketplace entry — the `plugin.json` value always wins silently.

**Release channels**: to support "stable" and "latest" channels, set up two marketplaces pointing to different refs/SHAs of the same repo, then assign them to different user groups through managed settings. Each channel must resolve to a different version (distinct SHAs distinguish channels automatically; with explicit versions, `plugin.json` must declare a different `version` at each pinned ref). For example, a stable-tools marketplace pins a plugin to `"ref": "stable"` while latest-tools pins the same repo to `"ref": "latest"`:

```json
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

To **pin dependency versions** so updates to a dependency do not break the dependent plugin, a plugin can constrain its dependencies to a semver range — see [Plugin dependencies](cc_plugin_dependencies.md) for the `{plugin-name}--v{version}` git-tag convention and range syntax.

## Manage marketplaces from the CLI

Claude Code provides non-interactive `claude plugin marketplace` subcommands for scripting and automation, equivalent to the `/plugin marketplace` commands inside an interactive session.

**`add <source> [options]`** — add a marketplace from a GitHub `owner/repo` shorthand, git URL, remote URL to a `marketplace.json` file, or local directory path. Pin to a branch/tag by appending `@ref` to the GitHub shorthand or `#ref` to a git URL. Options: `--scope <scope>` (`user` default, `project`, or `local` — where the marketplace is declared) and `--sparse <paths...>` (limit checkout to specific directories via git sparse-checkout, useful for monorepos):

```bash
claude plugin marketplace add acme-corp/claude-plugins@v2.0
claude plugin marketplace add https://gitlab.example.com/team/plugins.git
claude plugin marketplace add ./my-marketplace --scope project
claude plugin marketplace add acme-corp/monorepo --sparse .claude-plugin plugins
```

**`list [--json]`** — list all configured marketplaces. With `--json`, each entry includes `name`, `source`, and source-specific fields (`repo` for GitHub, `url` for git/URL, `path` for local), plus a `ref` field for GitHub/git sources added with a pinned branch or tag.

**`remove <name> [options]`** (alias `rm`) — remove a configured marketplace by the `name` from `marketplace.json` (as shown by `list`), **not** the source passed to `add`. `--scope <scope>` restricts removal to one settings scope; when omitted the declaration is removed from every editable scope. **Warning**: removing a marketplace from its last remaining scope also uninstalls any plugins installed from it — to refresh without losing plugins, use `update` instead.

**`update [name]`** — refresh marketplaces from their sources to retrieve new plugins and version changes; updates all marketplaces if `[name]` is omitted. Both `remove` and `update` fail against a seed-managed (read-only) marketplace; when updating all, seed-managed entries are skipped and others still update.

## Troubleshooting

| Symptom | Cause / Solution |
| :------ | :--------------- |
| Marketplace not loading | Verify the URL is accessible; check `.claude-plugin/marketplace.json` exists at the path; validate JSON with `claude plugin validate`; for private repos confirm access. |
| Plugin installation failures | Verify plugin source URLs are accessible; check plugin directories contain required files; for GitHub sources ensure repos are public or you have access; if both `ref` and `sha` are pinned, a deleted upstream branch/tag does not block install — confirm the pinned commit still exists. |
| Private repository authentication fails | Manual: verify you are authenticated (`gh auth status`), check `git config --global credential.helper`, try cloning manually. Auto-updates: check `$GITHUB_TOKEN` is set with `repo` scope (GitHub) or `read_repository` (GitLab) and not expired. |
| Marketplace updates fail in offline environments | A failed `git pull` makes Claude Code wipe the stale clone and re-clone, which also fails offline. Set `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` to retain the last-known-good cache; for fully offline use the seed directory. |
| Git operations time out | Git operations use a 120-second timeout. Raise it with `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` (milliseconds, e.g. `300000` for 5 minutes). |
| Plugins with relative paths fail in URL-based marketplaces | URL-based marketplaces only download `marketplace.json`, not plugin files. Switch entries to GitHub/npm/git URL sources, or host the marketplace in a git repo (a git clone makes relative paths resolve). |
| Files not found after installation | Plugins are copied to a cache directory, so paths referencing files outside the plugin directory (e.g. `../shared-utils`) fail. See plugins-reference for symlink/restructuring workarounds. |

Validation errors surface from `claude plugin validate .`: a marketplace directory check covers schema, duplicate plugin names, source path traversal, and version mismatches against each `plugin.json`; pointing it at an individual plugin directory additionally checks frontmatter and `hooks/hooks.json`.

**Source**: https://code.claude.com/docs/en/plugin-marketplaces
**Last Updated**: 2026-06-13
**Status**: Active
