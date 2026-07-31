---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - plugins
keywords:
  - openclaw plugins install
  - plugin source auto-detection
  - clawhub npm git archive marketplace
  - plugins install force pin link
  - plugins uninstall update
  - plugin index sqlite
  - npm artifact integrity drift
  - dangerously-force-unsafe-install
topics:
  - OpenClaw
  - Plugins CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/plugins
access_control_group: ["general"]
---

# OpenClaw — Installing and Lifecycle-Managing Plugins (`openclaw plugins install/uninstall/update`)

## Overview

This note is the install/lifecycle half of the `openclaw plugins` CLI — managing Gateway plugins, hook packs, and compatible bundles — mirroring the install-related sections of the `cli/plugins` source page (`Commands` install subset, `Install`, `Plugin index`, `Uninstall`, `Update`). It covers the install sources and their auto-detection (ClawHub / npm / git / archive / marketplace), the `--force` / `--pin` / `--link` flags, bare-name and `@openclaw/*` resolution during the launch cutover, the SQLite plugin index, and the uninstall/update lifecycle including npm artifact integrity drift. The authoring (`init`/`build`/`validate`), list/search, inspect, doctor, registry, and marketplace-list verbs are covered in [oc_cli_plugins_manage](oc_cli_plugins_manage.md). Deep plugin manifest, architecture, and bundle-compatibility models are linked, not redefined here.

## Install Commands (Source Resolution)

`openclaw plugins install <path-or-spec>` installs from a path or source-prefixed spec; the source is auto-detected from the spec form, or stated explicitly with a prefix:

```bash
openclaw plugins install <package>                      # source auto-detection
openclaw plugins install clawhub:<package>              # ClawHub only
openclaw plugins install npm:<package>                  # npm only
openclaw plugins install npm-pack:<path.tgz>            # local npm pack through npm install semantics
openclaw plugins install git:github.com/<owner>/<repo>  # git repo
openclaw plugins install git:github.com/<owner>/<repo>@<ref>
openclaw plugins install <package> --force              # overwrite existing install
openclaw plugins install <package> --pin                # pin version
openclaw plugins install <package> --dangerously-force-unsafe-install
openclaw plugins install <path>                         # local path
openclaw plugins install <plugin>@<marketplace>         # marketplace
openclaw plugins install <plugin> --marketplace <name>  # marketplace (explicit)
openclaw plugins install <plugin> --marketplace https://github.com/<owner>/<repo>
```

`plugins install` is also the install surface for hook packs that expose `openclaw.hooks` in `package.json`; use `openclaw hooks` for hook visibility and per-hook enablement, not package installation. Maintainers testing setup-time installs can override automatic install sources with guarded environment variables ([Plugin install overrides](https://docs.openclaw.ai/plugins/install-overrides)). For slow install/uninstall/registry-refresh investigation, run with `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1` — the trace writes phase timings to stderr and keeps JSON output parseable. In Nix mode (`OPENCLAW_NIX_MODE=1`), plugin lifecycle mutators (`plugins install`, `update`, `uninstall`, `enable`, `disable`) are disabled — use the Nix source instead.

### Bare-name, npm, and `@openclaw/*` resolution

Bare package names install from npm by default during the launch cutover, unless they match an official plugin id, in which case OpenClaw installs the catalog entry directly (for example `diffs`); to install an npm package with the same name use an explicit scoped spec (`@scope/diffs`). Use `npm:<package>` for npm-only resolution and `clawhub:<package>` for ClawHub. ClawHub is the primary distribution and discovery surface for most plugins, with npm a supported fallback and direct-install path. Raw `@openclaw/*` specs that match bundled plugins resolve to the **image-owned bundled copy** of the current OpenClaw build *before* npm fallback — e.g. `openclaw plugins install @openclaw/discord@2026.5.20 --pin` uses the bundled Discord plugin, while `npm:@openclaw/discord@2026.5.20` forces the external npm package. OpenClaw treats plugin installs like running code and recommends pinned versions.

Npm specs are **registry-only** (package name + optional exact version or dist-tag); git/URL/file specs and semver ranges are rejected. Dependency installs run in one managed npm project per plugin with `--ignore-scripts` for safety even when the shell has global npm install settings, and managed plugin npm projects inherit OpenClaw's package-level npm `overrides` so host security pins apply to hoisted dependencies. Bare specs and `@latest` stay on the stable track (date-stamped correction versions such as `2026.5.3-1` count as stable); if npm resolves either to a prerelease, OpenClaw stops and asks you to opt in with a prerelease tag (`@beta`/`@rc`) or exact prerelease version (`@1.2.3-beta.4`). For npm installs without an exact version, OpenClaw checks resolved package metadata first: if the latest stable package requires a newer plugin API or host version, it installs the newest *compatible* older stable release instead, whereas exact versions and explicit dist-tags stay strict and fail when incompatible.

### `--force`, `--pin`, and `--link`

`--force` reuses the existing install target and overwrites an already-installed plugin or hook pack in place — use it when intentionally reinstalling the same id from a new local path, archive, ClawHub package, or npm artifact. If you run `plugins install` for an id that is already installed, OpenClaw stops and points you at `plugins update <id-or-npm-spec>` for a normal upgrade or `plugins install <package> --force` to overwrite from a different source. `--pin` applies to **npm installs only** (it saves the resolved exact `name@version` spec in the managed plugin index while default behavior stays unpinned); it is not supported with `git:` installs (use an explicit ref such as `git:github.com/acme/plugin@v1.2.3`) nor with `--marketplace` (marketplace installs persist marketplace source metadata instead of an npm spec). `--link` (`-l`, e.g. `openclaw plugins install -l ./my-plugin`) avoids copying a local plugin directory and instead adds it to `plugins.load.paths`; `--force` is **not supported with `--link`** because linked installs reuse the source path instead of copying over a managed install target. The deprecated `--dangerously-force-unsafe-install` flag is now a no-op (OpenClaw no longer runs built-in install-time dangerous-code blocking); for host-specific install policy use the operator-owned `security.installPolicy` surface, since plugin `before_install` hooks are plugin-runtime lifecycle hooks, not the primary CLI-install policy boundary. If a ClawHub-published plugin is blocked by a registry scan, `--dangerously-force-unsafe-install` does not ask ClawHub to rescan or unblock it.

## Install Sources by Kind

### ClawHub

ClawHub installs use an explicit `clawhub:<package>` locator:

```bash
openclaw plugins install clawhub:openclaw-codex-app-server
openclaw plugins install clawhub:openclaw-codex-app-server@1.2.3
```

OpenClaw checks the advertised plugin API / minimum gateway compatibility before install. When the selected ClawHub version publishes a ClawPack artifact, OpenClaw downloads the versioned npm-pack `.tgz`, verifies the ClawHub digest header and the artifact digest, then installs through the normal archive path; older versions without ClawPack metadata install through the legacy package archive verification path. Recorded installs keep their ClawHub source metadata, artifact kind, npm integrity, npm shasum, tarball name, and ClawPack digest facts for later updates. Unversioned ClawHub installs keep an unversioned recorded spec so `openclaw plugins update` can follow newer releases, while explicit selectors such as `clawhub:pkg@1.2.3` and `clawhub:pkg@beta` remain pinned.

### npm and git

Bare npm-safe specs install from npm by default during the launch cutover (unless they match an official plugin id); use `npm:` to make npm-only resolution explicit:

```bash
openclaw plugins install npm:openclaw-codex-app-server
openclaw plugins install npm:@openclaw/discord@2026.5.20
openclaw plugins install npm:@scope/plugin-name@1.0.1
```

Use `git:<repo>` to install directly from a git repository; supported forms include `git:github.com/owner/repo`, `git:owner/repo`, full `https://`, `ssh://`, `git://`, `file://`, and `git@host:owner/repo.git` clone URLs, with `@<ref>` or `#<ref>` to check out a branch, tag, or commit before install. Git installs clone into a temporary directory, check out the requested ref, then use the normal plugin directory installer — so manifest validation, operator install policy, and install records behave like npm installs. Recorded git installs include the source URL/ref plus the resolved commit so `openclaw plugins update` can re-resolve the source later; verify runtime registrations with `openclaw plugins inspect <id> --runtime --json`.

### Archives, marketplace, and local-path auto-detection

Supported archives are `.zip`, `.tgz`, `.tar.gz`, `.tar`. Native OpenClaw plugin archives must contain a valid `openclaw.plugin.json` at the extracted plugin root; archives containing only `package.json` are rejected before install records are written. Use `npm-pack:<path.tgz>` for an npm-pack tarball to get the same per-plugin managed npm project path as registry installs (`package-lock.json` verification, hoisted dependency scanning, npm install records); plain archive paths install as local archives under the plugin extensions root. Use `plugin@marketplace` shorthand when the marketplace name exists in Claude's local registry cache at `~/.claude/plugins/known_marketplaces.json`, or `--marketplace` to pass the source explicitly:

```bash
openclaw plugins install <plugin-name> --marketplace <marketplace-name>
openclaw plugins install <plugin-name> --marketplace <owner/repo>
openclaw plugins install <plugin-name> --marketplace https://github.com/<owner>/<repo>
openclaw plugins install <plugin-name> --marketplace ./my-marketplace
```

Marketplace sources may be a Claude known-marketplace name, a local marketplace root or `marketplace.json` path, a GitHub repo shorthand (`owner/repo`), a GitHub repo URL, or a git URL. For remote marketplaces loaded from GitHub or git, plugin entries must stay inside the cloned marketplace repo: OpenClaw accepts relative path sources from that repo and rejects HTTP(S), absolute-path, git, GitHub, and other non-path plugin sources from remote manifests. For local paths and archives, OpenClaw auto-detects native OpenClaw plugins (`openclaw.plugin.json`), Codex-compatible bundles (`.codex-plugin/plugin.json`), Claude-compatible bundles (`.claude-plugin/plugin.json` or the default Claude component layout), and Cursor-compatible bundles (`.cursor-plugin/plugin.json`). Managed local installs must be plugin directories or archives — standalone `.js`, `.mjs`, `.cjs`, and `.ts` files are not copied into the managed root and must be listed in `plugins.load.paths` instead. Compatible bundles install into the normal plugin root and join the same list/info/enable/disable flow.

### Config includes and invalid-config repair

If your `plugins` section is backed by a single-file `$include`, `plugins install/update/enable/disable/uninstall` write through to that included file and leave `openclaw.json` untouched; root includes, include arrays, and includes with sibling overrides fail closed instead of flattening. If config is invalid during install, `plugins install` normally fails closed and tells you to run `openclaw doctor --fix` first, which can quarantine the invalid plugin entry. The only documented install-time exception is a narrow bundled-plugin recovery path for plugins that explicitly opt into `openclaw.install.allowInvalidConfigRecovery`. Workspace-origin plugins discovered from a workspace extensions root are not imported or executed until explicitly enabled — for local development run `openclaw plugins enable <plugin-id>` or set `plugins.entries.<plugin-id>.enabled: true` (and include the id in `plugins.allow` if your config uses it).

## Plugin Index

Plugin install metadata is machine-managed state, not user config: installs and updates write it to the shared SQLite state database under the active OpenClaw state directory. The `installed_plugin_index` row stores durable `installRecords` metadata — including records for broken or missing plugin manifests — plus a manifest-derived cold registry cache used by `openclaw plugins update`, uninstall, diagnostics, and the cold plugin registry. Shipped legacy `plugins.installs` records in config are read as compatibility input without rewriting `openclaw.json`; explicit plugin writes and `openclaw doctor --fix` move them into the plugin index and remove the config key when writes are allowed. If either write fails, the config records are kept so install metadata is not lost.

## Uninstall

```bash
openclaw plugins uninstall <id>
openclaw plugins uninstall <id> --dry-run
openclaw plugins uninstall <id> --keep-files
```

`uninstall` removes plugin records from `plugins.entries`, the persisted plugin index, plugin allow/deny list entries, and linked `plugins.load.paths` entries when applicable. Unless `--keep-files` is set, uninstall also removes the tracked managed install directory when it is inside OpenClaw's plugin extensions root. For active memory plugins, the memory slot resets to `memory-core`. `--keep-config` is a deprecated alias for `--keep-files`.

## Update

```bash
openclaw plugins update <id-or-npm-spec>
openclaw plugins update --all
openclaw plugins update <id-or-npm-spec> --dry-run
openclaw plugins update @openclaw/voice-call
openclaw plugins update openclaw-codex-app-server --dangerously-force-unsafe-install
```

Updates apply to tracked plugin installs in the managed plugin index and tracked hook-pack installs in `hooks.internal.installs`. Passing a plugin id reuses the recorded install spec (stored dist-tags such as `@beta` and exact pinned versions keep being used on later `update <id>` runs); passing an explicit npm spec (with dist-tag or exact version) resolves back to the tracked record, updates it, and records the new spec for future id-based updates, while passing the package name with no version or tag moves a pinned plugin back to the registry's default release line. `openclaw update` additionally knows the active update channel — on the beta channel, default-line npm and ClawHub records try `@beta` first, falling back to the recorded default/latest spec if no beta release exists (a non-fatal warning); exact versions and explicit tags stay pinned. Before a live npm update OpenClaw checks the installed version against npm registry metadata, and skips the update without downloading or rewriting `openclaw.json` if the installed version and recorded artifact identity already match the target. When a stored integrity hash exists and the fetched artifact hash changes, OpenClaw treats that as **npm artifact drift**: interactive `plugins update` prints expected vs actual hashes and asks for confirmation, while non-interactive helpers fail closed unless given an explicit continuation policy. `--dangerously-force-unsafe-install` is accepted here for compatibility but is deprecated and no longer changes behavior; operator `security.installPolicy` can still block updates.

**Source**: OpenClaw documentation — `cli/plugins` (mirror `inbox/openclaw_docs/cli/plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
