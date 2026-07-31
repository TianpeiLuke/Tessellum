---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - plugins
keywords:
  - openclaw plugins author
  - plugins init build validate
  - defineToolPlugin scaffold
  - plugins list search json
  - plugins inspect runtime
  - plugin shape classification
  - plugins doctor diagnostics
  - plugins registry refresh
  - plugins marketplace list
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

# OpenClaw — Authoring and Inspecting Plugins with `openclaw plugins`

## Overview

This note is the procedure half of the `openclaw plugins` CLI reference (`cli/plugins` source page): scaffolding, building, and validating a tool plugin, then listing, searching, inspecting, diagnosing, and discovering plugins. It mirrors the source page's **Author** (`init`/`build`/`validate`), **List** (`list`/`search` with flags), **Inspect** (`inspect`/`info`, shape classification, `--runtime`), **Doctor**, **Registry**, **Marketplace**, and runtime-hook debugging sections. The install/uninstall/update lifecycle and the SQLite plugin index are covered in the sibling note `oc_cli_plugins_install`. OpenClaw manages Gateway plugins, hook packs, and compatible bundles; `plugins list` shows `Format: openclaw` or `Format: bundle`, and verbose output adds the bundle subtype (`codex`, `claude`, or `cursor`) plus detected bundle capabilities.

## Author — `init` / `build` / `validate`

`openclaw plugins init <id>` creates a minimal TypeScript tool plugin that uses `defineToolPlugin`. The typical authoring flow scaffolds, builds, then validates, and the direct CLI forms (from the Commands block) follow:

```bash
openclaw plugins init stock-quotes --name "Stock Quotes"
cd stock-quotes
npm run plugin:build
npm run plugin:validate
# Direct CLI forms:
openclaw plugins init <id>
openclaw plugins init <id> --directory ./my-plugin --name "My Plugin"
openclaw plugins build --entry ./dist/index.js
openclaw plugins build --entry ./dist/index.js --check
openclaw plugins validate --entry ./dist/index.js
```

`plugins build` imports the entry, reads its static tool metadata, writes `openclaw.plugin.json`, and keeps `package.json` `openclaw.extensions` aligned. `plugins validate` checks that the generated manifest, package metadata, and current entry export still agree. The scaffold writes TypeScript source but generates metadata from the built `./dist/index.js` entry, so the workflow also works with the published CLI. Use `--entry <path>` when the entry is not the default package entry, and use `plugins build --check` in CI to fail when generated metadata is stale without rewriting files. Native OpenClaw plugins must ship `openclaw.plugin.json` with an inline JSON Schema (`configSchema`, even if empty); compatible bundles use their own bundle manifests instead. See `/plugins/tool-plugins` for the full authoring workflow.

## List and Search

```bash
openclaw plugins list
openclaw plugins list --enabled
openclaw plugins list --verbose
openclaw plugins list --json
openclaw plugins search <query>
openclaw plugins search <query> --limit 20
openclaw plugins search <query> --json
```

The `list` flags are: `--enabled` (boolean) shows only enabled plugins; `--verbose` (boolean) switches from the table view to per-plugin detail lines with source/origin/version/activation metadata; `--json` (boolean) emits a machine-readable inventory plus registry diagnostics and package dependency install state.

`plugins list` reads the persisted local plugin registry first, with a manifest-only derived fallback when the registry is missing or invalid. It checks whether a plugin is installed, enabled, and visible to cold startup planning, but it is **not** a live runtime probe of an already-running Gateway process. After changing plugin code, enablement, hook policy, or `plugins.load.paths`, restart the Gateway that serves the channel before expecting new `register(api)` code or hooks to run; for remote/container deployments, verify you are restarting the actual `openclaw gateway run` child, not only a wrapper process. `plugins list --json` includes each plugin's `dependencyStatus` from `package.json` `dependencies` and `optionalDependencies` — OpenClaw checks whether those package names are present along the plugin's normal Node `node_modules` lookup path; it does not import plugin runtime code, run a package manager, or repair missing dependencies.

`plugins search` is a remote ClawHub catalog lookup. It does not inspect local state, mutate config, install packages, or load plugin runtime code. It searches code-plugin and bundle-plugin packages (not skills — use `openclaw skills search` for ClawHub skills). Results include the ClawHub package name, family, channel, version, and summary, plus an install hint such as `openclaw plugins install clawhub:<package>`. For bundled plugin work inside a packaged Docker image, bind-mount the plugin source directory over the matching packaged source path (such as `/app/extensions/synology-chat`); OpenClaw discovers that mounted source overlay before `/app/dist/extensions/synology-chat`, while a plain copied source directory remains inert so normal packaged installs still use compiled dist.

## Inspect — `inspect` / `info`

```bash
openclaw plugins inspect <id>
openclaw plugins inspect <id> --runtime
openclaw plugins inspect <id> --json
```

`inspect` shows identity, load status, source, manifest capabilities, policy flags, diagnostics, install metadata, bundle capabilities, and any detected MCP or LSP server support, **without importing plugin runtime by default**. JSON output includes the plugin manifest contracts, such as `contracts.agentToolResultMiddleware` and `contracts.trustedToolPolicies`, so operators can audit trusted-surface declarations before enabling or restarting a plugin. Add `--runtime` to load the plugin module and include registered hooks, tools, commands, services, gateway methods, and HTTP routes. Runtime inspection reports missing plugin dependencies directly; installs and repairs stay in `openclaw plugins install`, `openclaw plugins update`, and `openclaw doctor --fix`.

Plugin-owned CLI commands are usually installed as root `openclaw` command groups, but plugins may also register nested commands under a core parent such as `openclaw nodes`. After `inspect --runtime` shows a command under `cliCommands`, run it at the listed path; for example a plugin that registers `demo-git` can be verified with `openclaw demo-git ping`.

Each plugin is classified by what it actually registers at runtime:

- **plain-capability** — one capability type (e.g. a provider-only plugin)
- **hybrid-capability** — multiple capability types (e.g. text + speech + images)
- **hook-only** — only hooks, no capabilities or surfaces
- **non-capability** — tools/commands/services but no capabilities

The `--json` flag outputs a machine-readable report suitable for scripting and auditing. `inspect --all` renders a fleet-wide table with shape, capability kinds, compatibility notices, bundle capabilities, and hook summary columns. `info` is an alias for `inspect`. See `/plugins/architecture#plugin-shapes` for more on the capability model.

## Doctor

```bash
openclaw plugins doctor
```

`doctor` reports plugin load errors, manifest/discovery diagnostics, compatibility notices, and stale plugin config references such as missing plugin slots. When the install tree and plugin config are clean it prints `No plugin issues detected.` If stale config remains but the install tree is otherwise healthy, the summary says so instead of implying full plugin health. If a configured plugin is present on disk but blocked by the loader's path-safety checks, config validation keeps the plugin entry and reports it as `present but blocked` — fix the preceding blocked-plugin diagnostic, such as path ownership or world-writable permissions, instead of removing the `plugins.entries.<id>` or `plugins.allow` config. For module-shape failures such as missing `register`/`activate` exports, rerun with `OPENCLAW_PLUGIN_LOAD_DEBUG=1` to include a compact export-shape summary in the diagnostic output.

## Registry

```bash
openclaw plugins registry
openclaw plugins registry --refresh
openclaw plugins registry --json
```

The local plugin registry is OpenClaw's persisted cold read model for installed plugin identity, enablement, source metadata, and contribution ownership. Normal startup, provider owner lookup, channel setup classification, and plugin inventory can read it without importing plugin runtime modules. Use `plugins registry` to inspect whether the persisted registry is present, current, or stale, and `--refresh` to rebuild it from the persisted plugin index, config policy, and manifest/package metadata — this is a repair path, not a runtime activation path. `openclaw doctor --fix` also repairs registry-adjacent managed npm drift: if an orphaned or recovered `@openclaw/*` package under a managed plugin npm project or the legacy flat managed npm root shadows a bundled plugin, doctor removes that stale package and rebuilds the registry so startup validates against the bundled manifest; doctor also relinks the host `openclaw` package into managed npm plugins that declare `peerDependencies.openclaw`, so package-local runtime imports such as `openclaw/plugin-sdk/*` resolve after updates or npm repairs. `OPENCLAW_DISABLE_PERSISTED_PLUGIN_REGISTRY=1` is a deprecated break-glass compatibility switch for registry read failures — prefer `plugins registry --refresh` or `openclaw doctor --fix`; the env fallback is only for emergency startup recovery while the migration rolls out.

## Marketplace List

```bash
openclaw plugins marketplace list <source>
openclaw plugins marketplace list <source> --json
```

`marketplace list` accepts a local marketplace path, a `marketplace.json` path, a GitHub shorthand like `owner/repo`, a GitHub repo URL, or a git URL. `--json` prints the resolved source label plus the parsed marketplace manifest and plugin entries. (The marketplace **install** path — `<plugin>@<marketplace>` shorthand and `--marketplace` source resolution — is covered in `oc_cli_plugins_install`.)

## Runtime-Hook Debugging

For runtime hook debugging the source page recommends three commands. `openclaw plugins inspect <id> --runtime --json` shows registered hooks and diagnostics from a module-loaded inspection pass; runtime inspection never installs dependencies — use `openclaw doctor --fix` to clean legacy dependency state or recover missing downloadable plugins that are referenced by config. `openclaw gateway status --deep --require-rpc` confirms the reachable Gateway URL/profile, service/process hints, config path, and RPC health. Non-bundled conversation hooks (`llm_input`, `llm_output`, `before_model_resolve`, `before_agent_reply`, `before_agent_run`, `before_agent_finalize`, `agent_end`) require `plugins.entries.<id>.hooks.allowConversationAccess=true`. For slow `inspect`, `uninstall`, or `registry`-refresh investigation, run the command with `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1`; the trace writes phase timings to stderr and keeps JSON output parseable.

**Source**: OpenClaw documentation — `cli/plugins` (mirror `inbox/openclaw_docs/cli/plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
