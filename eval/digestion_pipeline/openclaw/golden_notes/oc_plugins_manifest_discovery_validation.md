---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - manifest
keywords:
  - openclaw plugin discovery
  - manifest vs package.json
  - openclaw.plugin.json validation
  - discovery precedence duplicate plugin ids
  - configSchema json schema
  - plugins.entries plugins.slots validation
  - minHostVersion compat.pluginApi
  - openclaw.install npmSpec clawhubSpec
topics:
  - OpenClaw
  - Plugin Manifest Discovery and Validation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/manifest
access_control_group: ["general"]
---

# OpenClaw — Plugin Manifest Discovery and Validation

## Overview

This note documents the procedure OpenClaw follows to **discover** and **validate** a native plugin manifest (`openclaw.plugin.json`) before it loads plugin code, mirroring the back half of the `plugins/manifest` source page (sections "Manifest versus package.json", "Discovery precedence (duplicate plugin ids)", "JSON Schema requirements", "Validation behavior", and "Notes"). It covers the division of labor between `openclaw.plugin.json` and `package.json`, the `package.json#openclaw` fields that participate in discovery and install gating, how OpenClaw breaks ties when two discoveries share the same `id`, the mandatory JSON Schema requirement and strict config validation, and the error/warning behavior surfaced through `openclaw doctor`. Every native OpenClaw plugin **must** ship a `openclaw.plugin.json` in the plugin root; OpenClaw uses this manifest to validate configuration **without executing plugin code**, and missing or invalid manifests are treated as plugin errors that block config validation.

## Manifest versus package.json

OpenClaw reads two files per plugin, each with a distinct job. The first step in reasoning about where metadata belongs is to split it by these two roles:

| File | Use it for |
| --- | --- |
| `openclaw.plugin.json` | Discovery, config validation, auth-choice metadata, and UI hints that must exist before plugin code runs |
| `package.json` | npm metadata, dependency installation, and the `openclaw` block used for entrypoints, install gating, setup, or catalog metadata |

When unsure where a piece of metadata belongs, the source gives a decision rule: if OpenClaw must know it **before loading plugin code**, put it in `openclaw.plugin.json`; if it is about packaging, entry files, or npm install behavior, put it in `package.json`.

### package.json fields that affect discovery

Some pre-runtime plugin metadata intentionally lives in `package.json` under the `openclaw` block instead of `openclaw.plugin.json`. `openclaw.bundle` and `openclaw.bundle.json` are **not** OpenClaw plugin contracts; native plugins must use `openclaw.plugin.json` plus the supported `package.json#openclaw` fields below. The important examples (verbatim):

| Field | What it means |
| --- | --- |
| `openclaw.extensions` | Declares native plugin entrypoints. Must stay inside the plugin package directory. |
| `openclaw.runtimeExtensions` | Declares built JavaScript runtime entrypoints for installed packages. Must stay inside the plugin package directory. |
| `openclaw.setupEntry` | Lightweight setup-only entrypoint used during onboarding, deferred channel startup, and read-only channel status/SecretRef discovery. Must stay inside the plugin package directory. |
| `openclaw.runtimeSetupEntry` | Declares the built JavaScript setup entrypoint for installed packages. Requires `setupEntry`, must exist, and must stay inside the plugin package directory. |
| `openclaw.channel` | Cheap channel catalog metadata like labels, docs paths, aliases, and selection copy. |
| `openclaw.channel.commands` | Static native command and native skill auto-default metadata used by config, audit, and command-list surfaces before channel runtime loads. |
| `openclaw.channel.configuredState` | Lightweight configured-state checker metadata answering "does env-only setup already exist?" without loading the full channel runtime. |
| `openclaw.channel.persistedAuthState` | Lightweight persisted-auth checker metadata answering "is anything already signed in?" without loading the full channel runtime. |
| `openclaw.install.clawhubSpec` / `openclaw.install.npmSpec` / `openclaw.install.localPath` | Install/update hints for bundled and externally published plugins. |
| `openclaw.install.defaultChoice` | Preferred install path when multiple install sources are available. |
| `openclaw.install.minHostVersion` | Minimum supported OpenClaw host version, using a semver floor like `>=2026.3.22` or `>=2026.5.1-beta.1`. |
| `openclaw.compat.pluginApi` | Minimum OpenClaw plugin API range required by this package, using a semver floor like `>=2026.5.27`. |
| `openclaw.install.expectedIntegrity` | Expected npm dist integrity string such as `sha512-...`; install and update flows verify the fetched artifact against it. |
| `openclaw.install.allowInvalidConfigRecovery` | Allows a narrow bundled-plugin reinstall recovery path when config is invalid. |
| `openclaw.install.requiredPlatformPackages` | npm package aliases that must materialize when their lockfile platform constraints match the current host. |
| `openclaw.startup.deferConfiguredChannelFullLoadUntilAfterListen` | Lets setup-runtime channel surfaces load before listen, then defers the full configured channel plugin until post-listen activation. |

Manifest metadata decides which provider/channel/setup choices appear in onboarding before runtime loads; `package.json#openclaw.install` tells onboarding how to fetch or enable that plugin when the user picks one of those choices. The source is explicit: **do not move install hints into `openclaw.plugin.json`.**

The install/compat gating is enforced during install and manifest registry loading. `openclaw.install.minHostVersion` is enforced for non-bundled plugin sources — invalid values are rejected, and newer-but-valid values skip external plugins on older hosts; bundled source plugins are assumed co-versioned with the host checkout. `openclaw.compat.pluginApi` is enforced during package install for non-bundled sources and is the floor for the plugin SDK/runtime API the package was built against; it can be stricter than `minHostVersion`. The source warns to **not use the package version alone as the compatibility contract**: `peerDependencies.openclaw` remains npm metadata, while OpenClaw uses the `openclaw.compat.pluginApi` contract for install compatibility decisions.

For install sources, official install-on-demand metadata should use `clawhubSpec` when published on ClawHub (the preferred remote source, recording ClawHub artifact facts after install), with `npmSpec` as the compatibility fallback for packages not yet on ClawHub. Exact npm version pinning lives in `npmSpec` (for example `"npmSpec": "@wecom/wecom-openclaw-plugin@1.2.3"`); official external catalog entries should pair exact specs with `expectedIntegrity` so update flows fail closed if the fetched artifact no longer matches the pinned release. When `expectedIntegrity` is present, install/update flows enforce it; when omitted, the registry resolution is recorded without an integrity pin. `openclaw.install.requiredPlatformPackages` lists bare npm package names for platform-specific native-binary aliases — during npm install OpenClaw verifies only the declared alias whose lockfile constraints match the host, and if npm reports success but omits that alias it retries once with a fresh cache and rolls back if the alias is still missing. `openclaw.install.allowInvalidConfigRecovery` is intentionally narrow: it does not make arbitrary broken configs installable, only recovering from specific stale bundled-plugin upgrade failures (a missing bundled plugin path or a stale `channels.<id>` entry for that same bundled plugin), while unrelated config errors still block install and route operators to `openclaw doctor --fix`.

Channel plugins should provide `openclaw.setupEntry` when status, channel list, or SecretRef scans need to identify configured accounts without loading the full runtime; the setup entry exposes channel metadata plus setup-safe config/status/secrets adapters, keeping network clients, gateway listeners, and transport runtimes in the main extension entrypoint. Runtime entrypoint fields do not override package-boundary checks for source entrypoint fields — for example, `openclaw.runtimeExtensions` cannot make an escaping `openclaw.extensions` path loadable. The cheap channel checker modules are declared as small metadata blocks; `openclaw.channel.persistedAuthState` points at a tiny export that reads persisted state only:

```json
{
  "openclaw": {
    "channel": {
      "id": "whatsapp",
      "persistedAuthState": {
        "specifier": "./auth-presence",
        "exportName": "hasAnyWhatsAppAuth"
      }
    }
  }
}
```

`openclaw.channel.configuredState` follows the same shape for cheap env-only configured checks; if the check needs full config resolution or the real channel runtime, that logic belongs in the plugin `config.hasConfiguredState` hook instead.

## Discovery precedence (duplicate plugin ids)

OpenClaw discovers plugins from several roots (for the raw filesystem scan order, see the configuration reference's plugin scan order). When two discoveries share the same `id`, only the **highest-precedence** manifest is kept and lower-precedence duplicates are dropped instead of loading beside it. Precedence, highest to lowest:

1. **Config-selected** — a path explicitly pinned in `plugins.entries.<id>`
2. **Bundled** — plugins shipped with OpenClaw
3. **Global install** — plugins installed into the global OpenClaw plugin root
4. **Workspace** — plugins discovered relative to the current workspace

The implications follow directly from this order: a forked or stale copy of a bundled plugin sitting in the workspace will **not** shadow the bundled build; to actually override a bundled plugin with a local one, pin it via `plugins.entries.<id>` so it wins by precedence rather than relying on workspace discovery; duplicate drops are logged so Doctor and startup diagnostics can point at the discarded copy; and config-selected duplicate overrides are worded as explicit overrides in diagnostics but still warn so stale forks and accidental shadows stay visible.

## JSON Schema requirements

Every plugin must ship a JSON Schema, even if it accepts no config. An empty schema is acceptable (for example, `{ "type": "object", "additionalProperties": false }`). Schemas are validated at **config read/write time, not at runtime**. When extending or forking a bundled plugin with new config keys, update that plugin's `openclaw.plugin.json` `configSchema` at the same time — bundled plugin schemas are strict, so adding `plugins.entries.<id>.config.myNewKey` in user config without adding `myNewKey` to `configSchema.properties` will be rejected before the plugin runtime loads. Example schema extension (verbatim):

```json
{
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "myNewKey": {
        "type": "string"
      }
    }
  }
}
```

## Validation behavior

After discovery and schema resolution, OpenClaw applies these validation rules, classifying each problem as an **error** or a **warning**:

- Unknown `channels.*` keys are **errors**, unless the channel id is declared by a plugin manifest.
- `plugins.entries.<id>`, `plugins.allow`, `plugins.deny`, and `plugins.slots.*` must reference **discoverable** plugin ids. Unknown ids are **errors**.
- If a plugin is installed but has a broken or missing manifest or schema, validation fails and Doctor reports the plugin error.
- If plugin config exists but the plugin is **disabled**, the config is kept and a **warning** is surfaced in Doctor + logs.

For the full `plugins.*` schema, the source points to the gateway Configuration reference.

## Notes

The source page closes with operational notes that constrain how the manifest loader reads and validates manifests:

- The manifest is **required for native OpenClaw plugins**, including local filesystem loads. Runtime still loads the plugin module separately; the manifest is only for discovery + validation.
- Native manifests are parsed with **JSON5**, so comments, trailing commas, and unquoted keys are accepted as long as the final value is still an object.
- Only documented manifest fields are read by the manifest loader. Avoid custom top-level keys.
- `channels`, `providers`, `cliBackends`, and `skills` can all be omitted when a plugin does not need them.
- `providerCatalogEntry` must stay lightweight and should not import broad runtime code; use it for static provider catalog metadata or narrow discovery descriptors, not request-time execution.
- Exclusive plugin kinds are selected through `plugins.slots.*`: `kind: "memory"` via `plugins.slots.memory`, `kind: "context-engine"` via `plugins.slots.contextEngine` (default `legacy`). Declare the exclusive plugin kind in the manifest; the runtime-entry `OpenClawPluginDefinition.kind` is deprecated and remains only as a compatibility fallback for older plugins.
- Env-var metadata (`setup.providers[].envVars`, deprecated `providerAuthEnvVars`, and `channelEnvVars`) is declarative only. Status, audit, cron delivery validation, and other read-only surfaces still apply plugin trust and effective activation policy before treating an env var as configured.
- If your plugin depends on native modules, document the build steps and any package-manager allowlist requirements (for example, pnpm `allow-build-scripts` + `pnpm rebuild <package>`).

**Source**: OpenClaw documentation — `plugins/manifest` (Manifest versus package.json · Discovery precedence · JSON Schema requirements · Validation behavior · Notes); mirror `inbox/openclaw_docs/plugins/manifest.md`
**Last Updated**: 2026-06-22
**Status**: Active
