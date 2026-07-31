---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - dependency_resolution
keywords:
  - openclaw plugin dependency resolution
  - plugin install roots
  - per-plugin npm project root
  - bundled vs local plugins
  - npm-shrinkwrap bundledDependencies
  - openclaw peer dependency
  - startup reload plugin loading
  - doctor fix legacy cleanup
topics:
  - OpenClaw
  - Plugin Dependencies
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/dependency-resolution
access_control_group: ["general"]
---

# OpenClaw — Plugin Dependency Resolution Model

## Overview

This note captures OpenClaw's plugin **dependency/loading model** as documented on the `plugins/dependency-resolution` source page: which layer owns dependency work versus runtime, the stable per-source install roots, how local (path) plugins resolve, how startup and config reload re-load plugins without installing, how bundled plugins ship, and how doctor cleans up legacy install state. The governing principle is that OpenClaw keeps all plugin dependency work at **install/update time**: runtime loading does not run package managers, repair dependency trees, or mutate the OpenClaw package directory. This note is a `concept` (the resolution model); the everyday CLI surface (`openclaw plugins install/update`) and the native-dependency plugin examples link out to sibling notes.

## Responsibility Split

OpenClaw and the plugin package own distinct halves of dependency work. **Plugin packages own their dependency graph**:

- runtime dependencies live in the plugin package `dependencies` or `optionalDependencies`
- SDK/core imports are peer or supplied OpenClaw imports
- local development plugins bring their own already-installed dependencies
- npm and git plugins are installed into OpenClaw-owned package roots

**OpenClaw owns only the plugin lifecycle**: discover the plugin source, install or update the package when explicitly requested, record the install metadata, load the plugin entrypoint, and fail with an actionable error when dependencies are missing. The split means a missing dependency is reported as an actionable load failure pointing the operator to an explicit install/update/doctor fix, rather than OpenClaw silently attempting a dependency repair at runtime.

## Install Roots

OpenClaw uses **stable per-source roots** so each plugin's dependency tree stays inside a known cleanup boundary:

- npm packages install into per-plugin projects under `~/.openclaw/npm/projects/<encoded-package>`
- git packages clone under `~/.openclaw/git`
- local/path/archive installs are copied or referenced without dependency repair

npm installs run in that per-plugin project root with a strict, script-free command:

```bash
cd ~/.openclaw/npm/projects/<encoded-package>
npm install --omit=dev --omit=peer --legacy-peer-deps --ignore-scripts --no-audit --no-fund
```

`openclaw plugins install npm-pack:<path.tgz>` uses that same per-plugin npm project root for a local npm-pack tarball: OpenClaw reads the tarball's npm metadata, adds it to the managed project as a copied `file:` dependency, runs the normal npm install, and then verifies the installed lockfile metadata before trusting the plugin. This is intended for **package-acceptance and release-candidate proof**, where a local pack artifact should behave like the registry artifact it simulates. npm may hoist transitive dependencies to the per-plugin project's `node_modules` beside the plugin package; OpenClaw scans the managed project root before trusting the install and removes that project during uninstall, so hoisted runtime dependencies stay inside that plugin's cleanup boundary.

### Lockfiles, bundling, and the host peer

Published npm plugin packages can ship `npm-shrinkwrap.json`, and npm uses that publishable lockfile during install; OpenClaw's managed npm project root supports it through the normal npm install path. OpenClaw-owned publishable plugin packages must include a package-local shrinkwrap generated from that plugin package's published dependency graph:

```bash
pnpm deps:shrinkwrap:generate
pnpm deps:shrinkwrap:check
```

The generator strips plugin `devDependencies`, applies the workspace override policy, and writes `extensions/<id>/npm-shrinkwrap.json` for each `publishToNpm` plugin. Third-party plugin packages may also ship shrinkwrap; OpenClaw does not require it for community packages, but npm will respect it when present. OpenClaw-owned npm plugin packages can also publish with explicit `bundledDependencies`: the npm publish path overlays the runtime dependency name list, removes dev-only workspace metadata from the published package manifest, runs a script-free npm install for package-local runtime dependencies, then packs or publishes the plugin tarball with those dependency files included. Native-heavy packages, including Codex and ACP runtimes, opt out with `openclaw.release.bundleRuntimeDependencies: false`; those packages still ship their shrinkwrap, but npm resolves runtime dependencies during install instead of embedding every platform binary in the plugin tarball. The root `openclaw` package does not bundle its full dependency tree.

Plugins that import `openclaw/plugin-sdk/*` declare `openclaw` as a **peer dependency**. OpenClaw does not let npm install a separate registry copy of the host package into a managed project, because stale host packages can affect npm peer resolution inside that plugin. Managed npm installs skip npm peer resolution/materialization, and OpenClaw reasserts plugin-local `node_modules/openclaw` links for installed packages that declare the host peer after install or update. git installs clone or refresh the repository, then run:

```bash
npm install --omit=dev --ignore-scripts --no-audit --no-fund
```

The installed plugin then loads from that package directory, so package-local and parent `node_modules` resolution works the same way it does for a normal Node package.

## Local Plugins

Local plugins are treated as **developer-controlled directories**. OpenClaw does not run `npm install`, `pnpm install`, or dependency repair for them — if a local plugin has dependencies, install them in that plugin before loading it. Third-party TypeScript local plugins can use the emergency **Jiti path**, while packaged JavaScript plugins and bundled internal plugins load through native import/require instead of Jiti.

## Startup and Reload

Gateway startup and config reload **never install plugin dependencies**. They read the plugin install records, compute the entrypoint, and load it. If a dependency is missing at runtime, the plugin fails to load, and the error should point the operator to an explicit fix:

```bash
openclaw plugins update <id>
openclaw plugins install <source>
openclaw doctor --fix
```

`doctor --fix` can clean legacy OpenClaw-generated dependency state and recover downloadable plugins that are missing from the local install records when config references them. Doctor does not repair dependencies for an already-installed local plugin.

## Bundled Plugins

Lightweight and core-critical bundled plugins are shipped as part of OpenClaw. They should either have no heavy runtime dependency tree or be moved out to a downloadable package on ClawHub/npm. (For the current generated list of plugins that ship in the core package, install externally, or stay source-only, the source page points to the Plugin inventory.) Bundled plugin manifests **must not request dependency staging**; large or optional plugin functionality should be packaged as a normal plugin and installed through the same npm/git/ClawHub path as third-party plugins.

In source checkouts, OpenClaw treats the repository as a **pnpm monorepo**. After `pnpm install`, bundled plugins load from `extensions/<id>` so package-local workspace dependencies are available and edits are picked up directly. Source checkout development is pnpm-only; plain `npm install` at the repository root is not a supported way to prepare bundled plugin dependencies. The three install shapes and their dependency owners:

| Install shape                    | Bundled plugin location               | Dependency owner                                                     |
| -------------------------------- | ------------------------------------- | -------------------------------------------------------------------- |
| `npm install -g openclaw`        | Built runtime tree inside the package | OpenClaw package and explicit plugin install/update/doctor flows     |
| Git checkout plus `pnpm install` | `extensions/<id>` workspace packages  | The pnpm workspace, including each plugin package's own dependencies |
| `openclaw plugins install ...`   | Managed npm project/git/ClawHub root  | The plugin install/update flow                                       |

## Legacy Cleanup

Older OpenClaw versions generated bundled-plugin dependency roots at startup or during doctor repair. Current doctor cleanup removes those stale directories and symlinks when `--fix` is used, including old `plugin-runtime-deps` roots, global Node-prefix package symlinks that point at pruned `plugin-runtime-deps` targets, `.openclaw-runtime-deps*` manifests, generated plugin `node_modules`, install stage directories, and package-local pnpm stores. Packaged postinstall also removes those global symlinks before pruning the legacy target roots so upgrades do not leave dangling ESM package imports. Older npm installs also used a shared `~/.openclaw/npm/node_modules` root; current install, update, uninstall, and doctor flows still recognize that legacy flat root only for recovery and cleanup, and new npm installs should create per-plugin project roots instead.

**Source**: OpenClaw documentation — `plugins/dependency-resolution` (mirror `inbox/openclaw_docs/plugins/dependency-resolution.md`)
**Last Updated**: 2026-06-22
**Status**: Active
