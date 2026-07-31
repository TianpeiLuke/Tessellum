---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - dependencies
keywords:
  - plugin dependencies
  - version constraint
  - semver range
  - cross-marketplace dependency
  - git tag version resolution
  - range-conflict
  - claude plugin prune
  - dependency error
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/plugin-dependencies
access_control_group: ["general"]
---

# Constrain Plugin Dependency Versions

## Overview

A Claude Code plugin can depend on other plugins by listing them in `plugin.json` (or in its marketplace entry). By default a dependency tracks the **latest** available version, so an upstream release can change the dependency under a plugin without warning. **Version constraints** let a plugin author hold a dependency at a tested **semver range** until they choose to move, so the plugin keeps working when an upstream plugin ships a breaking change. This guide is for plugin authors who declare dependencies and for marketplace maintainers who tag releases.

When a plugin that declares dependencies is installed, Claude Code resolves and installs them automatically and lists which were added at the end of the install output. If a dependency later goes missing, `/reload-plugins` and the background auto-update reinstall it, provided its marketplace is already configured; re-running `claude plugin install` on the dependent plugin or adding a marketplace also resolves outstanding missing dependencies. Dependencies from a marketplace you have not added are left unresolved. Dependency version constraints require Claude Code v2.1.110 or later.

## Why Constrain Dependency Versions

Consider an internal marketplace where the platform team maintains `secrets-vault` (an MCP server wrapping a secrets backend) and the deploy team maintains `deploy-kit`, which calls `secrets-vault` during deploys. `deploy-kit` is tested against `secrets-vault` v2.1.0. **Without** a constraint, the next time the platform team tags a release that renames an MCP tool, auto-update moves every engineer's `secrets-vault` to the new version and `deploy-kit` breaks. **With** a constraint, `deploy-kit` declares it needs `secrets-vault` in the `~2.1.0` range; engineers stay on the highest matching `2.1.x` patch, and the deploy team upgrades on its own schedule by publishing a new `deploy-kit` version with a wider constraint.

## Declare a Dependency with a Version Constraint

List dependencies in the `dependencies` array of the plugin's `.claude-plugin/plugin.json`. Each entry is either a bare plugin name (string) or an object with a version constraint:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "deploy-kit",
  "version": "3.1.0",
  "dependencies": [
    "audit-logger",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

A bare string (`"audit-logger"`) depends on whatever version that plugin's marketplace provides. The object form accepts three fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | string | Plugin name. Resolves within the **same marketplace** as the declaring plugin. Required. |
| `version` | string | A [semver range](https://github.com/npm/node-semver#ranges) such as `~2.1.0`, `^2.0`, `>=1.4`, or `=2.1.0`. The dependency is fetched at the highest tagged version satisfying this range. |
| `marketplace` | string | A **different** marketplace to resolve `name` in. Cross-marketplace dependencies are blocked unless the target is listed in `allowCrossMarketplaceDependenciesOn`. |

The `version` field accepts any expression supported by Node's `semver` package — caret, tilde, hyphen, and comparator ranges. Pre-release versions like `2.0.0-beta.1` are excluded unless the range opts in with a pre-release suffix such as `^2.0.0-0`.

## Depend on a Plugin from Another Marketplace

By default Claude Code refuses to auto-install a dependency that lives in a different marketplace than the plugin declaring it — this prevents one marketplace from silently pulling in plugins from an unreviewed source. To allow it, the maintainer of the **root marketplace** (the one hosting the plugin the user is installing) adds the target marketplace name to `allowCrossMarketplaceDependenciesOn` in `marketplace.json`. Only the root's allowlist is consulted, so trust does not chain through intermediate marketplaces:

```json .claude-plugin/marketplace.json theme={null}
{
  "name": "acme-tools",
  "owner": { "name": "Acme" },
  "allowCrossMarketplaceDependenciesOn": ["acme-shared"],
  "plugins": [
    {
      "name": "deploy-kit",
      "source": "./deploy-kit",
      "dependencies": [
        { "name": "audit-logger", "marketplace": "acme-shared" }
      ]
    }
  ]
}
```

If the field is missing or omits the target, install fails with a `cross-marketplace` error naming the field to set. Users can still install the dependency manually first, which satisfies the constraint without changing the allowlist.

## Tag Plugin Releases for Version Resolution

Version constraints resolve against **git tags** on the marketplace repository. For Claude Code to find a dependency's available versions, the upstream plugin's releases must be tagged `{plugin-name}--v{version}`, where `{version}` matches the `version` field in that commit's `plugin.json`. From the plugin directory, running `claude plugin tag --push` derives the tag name from the plugin's manifest and the enclosing marketplace entry. Before tagging, it validates the plugin contents, checks that `plugin.json` and the marketplace entry agree on the version, requires a clean working tree under the plugin directory, and refuses if the tag already exists. `--dry-run` shows what would be tagged. Running `git tag secrets-vault--v2.1.0` directly is equivalent if you keep `plugin.json` and the marketplace entry in sync yourself.

The plugin-name prefix lets one marketplace repository host multiple plugins with independent version lines; the `--v` separator is parsed as a prefix match on the full plugin name, so names containing hyphens are handled correctly. When installing a plugin that declares `{ "name": "secrets-vault", "version": "~2.1.0" }`, Claude Code lists the marketplace's tags, filters to those starting with `secrets-vault--v`, and fetches the highest version satisfying `~2.1.0`. If no matching tag exists, the dependent plugin is disabled with an error listing the available versions.

The resolved tag's semver is recorded separately from `plugin.json`'s `version`, so constraint checks use the tag actually fetched even if `plugin.json` at that commit is stale. The cache directory name for a tag-resolved install includes a 12-character commit-SHA suffix, so if a maintainer force-moves a tag to a different commit, the next install gets a fresh cache directory instead of reusing stale content. For `npm` marketplace sources the constraint does **not** control which version is fetched (tag-based resolution applies only to git-backed sources); the constraint is still checked at load time, and the dependent plugin is disabled with `dependency-version-unsatisfied` if the installed version does not satisfy it.

## How Constraints Interact

When several installed plugins constrain the same dependency, Claude Code **intersects** their ranges and resolves the dependency to the highest version satisfying all of them:

| Plugin A requires | Plugin B requires | Result |
| :--- | :--- | :--- |
| `^2.0` | `>=2.1` | One install at the highest `2.x` tag at or above `2.1.0`. Both plugins load. |
| `~2.1` | `~3.0` | Install of plugin B fails with `range-conflict`. Plugin A and the dependency stay as they were. |
| `=2.1.0` | none | The dependency stays at `2.1.0`. Auto-update skips newer versions while plugin A is installed. |

Auto-update fetches a constrained dependency at the highest git tag satisfying every installed plugin's range (not the marketplace's latest), so the dependency keeps receiving updates within its allowed range. If no tag satisfies all ranges, the update is skipped and the skip appears in `/doctor` and the `/plugin` Errors tab, naming the constraining plugin. When you uninstall the last plugin that constrains a dependency, the dependency is no longer held and resumes tracking its marketplace entry on the next update.

## Enable or Disable a Plugin with Dependencies

Enabling a plugin also enables the plugins it depends on, and disabling a plugin is blocked if another enabled plugin still needs it. Both behaviors require Claude Code v2.1.143 or later (earlier versions enable/disable only the named plugin and surface a `dependency-unsatisfied` error on the next load). When you enable a plugin, Claude Code enables its dependencies at the same scope (and their dependencies transitively), and the success message lists what else was enabled. If a dependency can't be enabled, the command refuses and explains what's blocking it and how to fix it:

| Condition | Result |
| :--- | :--- |
| A dependency is not installed | Enable fails and prints the `claude plugin install` command for each missing dependency. |
| A dependency is blocked by the org's plugin policy | Enable fails and names the blocked dependency. |
| A dependency is set to `false` at a higher-precedence scope than the target | Enable fails. Enable the dependency at that scope, or pass `--scope` to write there. |
| All dependencies installed and allowed | Enable succeeds and writes `true` for the plugin and each not-already-enabled dependency. |

This holds even when a dependency sets `defaultEnabled: false` ([default-enablement](https://code.claude.com/docs/en/plugins-reference#default-enablement), B09A) in its manifest, because Claude Code writes an explicit `true`; the same applies at install. When you disable a plugin, Claude Code refuses if another enabled plugin still depends on it, naming the dependents and giving a chained command that disables them in the right order, ending with the one you asked for:

```text theme={null}
secrets-vault is still required by deploy-kit. Disable that plugin first, or
disable everything together: claude plugin disable deploy-kit@acme-tools && claude plugin disable secrets-vault@acme-tools
```

## Remove Orphaned Auto-Installed Dependencies

Auto-installed dependencies stay on disk after the plugins that installed them are uninstalled, in case you reinstall a dependent plugin or want to keep using the dependency directly. Running `claude plugin prune` (requires v2.1.121 or later) lists the auto-installed dependencies that no longer have any installed plugin requiring them and removes them after a confirmation prompt. By default prune operates at user scope; `--scope project` or `--scope local` targets a different scope, `--dry-run` lists what would be removed without changing anything, and `-y` skips the confirmation. When stdin or stdout is not a terminal, prune lists the orphans and exits without removing them unless `-y` is passed.

To prune as part of an uninstall, pass `--prune` to `claude plugin uninstall` (e.g. `claude plugin uninstall deploy-kit --prune`); after removing the named plugin, Claude Code scans for and removes any now-orphaned auto-installed dependencies. Plugins you installed yourself are **never** pruned — only those installed automatically through another plugin's `dependencies` array.

## Resolve Dependency Errors

Dependency problems surface in `claude plugin list`, in the `/plugin` interface, and in `/doctor`; the affected plugin is disabled until the error is resolved. The most common errors:

| Error | Meaning | How to resolve |
| :--- | :--- | :--- |
| `dependency-unsatisfied` | A declared dependency is not installed, or installed but disabled. | Run the `claude plugin install` command shown. If the marketplace is not configured, add it with `claude plugin marketplace add`; if disabled, enable it. |
| `range-conflict` | The version requirements cannot be combined (no version satisfies all ranges, invalid semver syntax, or combined ranges too complex to intersect). | Uninstall/update one conflicting plugin, fix any invalid `version` string, simplify long `\|\|` chains, or ask the upstream author to widen its constraint. |
| `dependency-version-unsatisfied` | The installed dependency's version is outside this plugin's declared range. | Run `claude plugin install <dependency>@<marketplace>` to re-resolve against all current constraints. |
| `no-matching-tag` | The dependency's repository has no `{name}--v*` tag satisfying the range. | Check that the upstream has tagged releases using the convention above, or relax the range. |

To check for these errors programmatically, run `claude plugin list --json` and read the `errors` field on each plugin.

**Source**: https://code.claude.com/docs/en/plugin-dependencies
**Last Updated**: 2026-06-13
**Status**: Active
