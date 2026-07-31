---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk
keywords:
  - openclaw plugin packaging
  - package.json openclaw field
  - openclaw.plugin.json manifest
  - openclaw.channel metadata
  - openclaw.install metadata
  - deferred full load
  - setupEntry defineSetupPluginEntry
  - narrow setup helper imports
  - single-account promotion
  - clawhub package publish
topics:
  - OpenClaw
  - Plugin SDK
  - Plugin Packaging
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-setup
access_control_group: ["general"]
---

# OpenClaw — Packaging a Plugin (package.json, Manifest, ClawHub Publish, Setup Entry)

## Overview

This note is the packaging procedure for an OpenClaw plugin, covering the four packaging concerns of the `plugins/sdk-setup` source page that precede config-schema authoring: the `package.json` `openclaw` field (`extensions`, `setupEntry`, `channel`, `providers`, `install`, `startup`, and the `deferConfiguredChannelFullLoadUntilAfterListen` deferred-load flag), the mandatory `openclaw.plugin.json` manifest, the `clawhub package publish` command, and the `setup-entry.ts` setup entry (its narrow setup-helper import seams and the channel-owned single-account promotion contract). It deliberately stops at the page's "Config schema" / "Setup wizards" / "Publishing and installing" sections, which are documented separately in **[oc_plugins_sdk_setup_config_schema_wizards](oc_plugins_sdk_setup_config_schema_wizards.md)**.

## Package metadata (`package.json` `openclaw` field)

Every OpenClaw plugin's `package.json` carries an `openclaw` field that tells the plugin system what the plugin provides. A channel plugin declares its entry, setup entry, and channel catalog metadata; a provider plugin / ClawHub-published baseline additionally declares `compat` and `build` version gates:

```json
{
  "name": "@myorg/openclaw-my-channel",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "channel": {
      "id": "my-channel",
      "label": "My Channel",
      "blurb": "Short description of the channel."
    }
  }
}
```

For a provider plugin or any externally published ClawHub package, add the `compat` and `build` gates (these fields are **required** when publishing on ClawHub; the canonical publish snippets live in `docs/snippets/plugin-publish/`):

```json openclaw-clawhub-package.json
{
  "name": "@myorg/openclaw-my-plugin",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "compat": {
      "pluginApi": ">=2026.3.24-beta.2",
      "minGatewayVersion": "2026.3.24-beta.2"
    },
    "build": {
      "openclawVersion": "2026.3.24-beta.2",
      "pluginSdkVersion": "2026.3.24-beta.2"
    }
  }
}
```

The top-level `openclaw` fields are: **`extensions`** (`string[]`) — entry point files relative to package root; **`setupEntry`** (`string`) — optional lightweight setup-only entry; **`channel`** (`object`) — channel catalog metadata for setup, picker, quickstart, and status surfaces; **`providers`** (`string[]`) — provider ids registered by this plugin; **`install`** (`object`) — install hints (`npmSpec`, `localPath`, `defaultChoice`, `minHostVersion`, `expectedIntegrity`, `allowInvalidConfigRecovery`); and **`startup`** (`object`) — startup behavior flags.

### `openclaw.channel`

`openclaw.channel` is cheap package metadata for channel discovery and setup surfaces before runtime loads. Its fields: `id` (canonical channel id), `label` (primary label), `selectionLabel` (picker/setup label when it should differ from `label`), `detailLabel` (secondary detail label for richer catalogs and status surfaces), `docsPath` (docs path for setup/selection links), `docsLabel` (override label for docs links), `blurb` (short onboarding/catalog description), `order` (`number` sort order in catalogs), `aliases` (`string[]` extra lookup aliases), `preferOver` (`string[]` lower-priority ids this channel outranks), `systemImage` (optional icon/system-image name), `selectionDocsPrefix` (prefix text before docs links in selection surfaces), `selectionDocsOmitLabel` (`boolean` — show the docs path directly instead of a labeled link), `selectionExtras` (`string[]` extra short strings appended in selection copy), `markdownCapable` (`boolean` — marks the channel markdown-capable for outbound formatting), `exposure` (`object` visibility controls), `quickstartAllowFrom` (`boolean` — opt into the standard quickstart `allowFrom` flow), `forceAccountBinding` (`boolean` — require explicit account binding even when only one account exists), and `preferSessionLookupForAnnounceTarget` (`boolean` — prefer session lookup when resolving announce targets). The `exposure` object supports `configured` (include in configured/status listings), `setup` (include in interactive setup/configure pickers), and `docs` (mark public-facing in docs/navigation surfaces). The legacy aliases `showConfigured` and `showInSetup` remain supported, but `exposure` is preferred.

### `openclaw.install`

`openclaw.install` is package metadata, not manifest metadata. Its fields: `clawhubSpec` (`string`) — canonical ClawHub spec for install/update and onboarding install-on-demand flows; `npmSpec` (`string`) — canonical npm spec for install/update fallback flows; `localPath` (`string`) — local development or bundled install path; `defaultChoice` (`"clawhub" | "npm" | "local"`) — preferred install source when multiple are available; `minHostVersion` (`string`) — minimum supported OpenClaw version in the form `>=x.y.z` or `>=x.y.z-prerelease`; `expectedIntegrity` (`string`) — expected npm dist integrity, usually `sha512-...`, for pinned installs; `allowInvalidConfigRecovery` (`boolean`) — lets bundled-plugin reinstall flows recover from specific stale-config failures; and `requiredPlatformPackages` (`string[]`) — required platform-specific npm aliases verified during npm install.

Interactive onboarding also uses `openclaw.install` for install-on-demand surfaces: if a plugin exposes provider auth choices or channel setup/catalog metadata before runtime loads, onboarding can show that choice, prompt for ClawHub, npm, or local install, install or enable the plugin, then continue the selected flow. ClawHub onboarding choices use `clawhubSpec` and are preferred when present; npm choices require trusted catalog metadata with a registry `npmSpec`; exact versions and `expectedIntegrity` are optional npm pins, and if `expectedIntegrity` is present install/update flows enforce it for npm. The guidance is to keep the "what to show" metadata in `openclaw.plugin.json` and the "how to install it" metadata in `package.json`. If `minHostVersion` is set, both install and non-bundled manifest-registry loading enforce it — older hosts skip external plugins and invalid version strings are rejected (bundled source plugins are assumed co-versioned with the host checkout). For pinned npm installs, keep the exact version in `npmSpec` and add the artifact integrity via `expectedIntegrity` alongside `defaultChoice: "npm"`. Finally, `allowInvalidConfigRecovery` is **not** a general bypass for broken configs — it is for narrow bundled-plugin recovery only (so reinstall/setup can repair known upgrade leftovers like a missing bundled plugin path or a stale `channels.<id>` entry for that same plugin); if config is broken for unrelated reasons, install still fails closed and tells the operator to run `openclaw doctor --fix`.

### Deferred full load

Channel plugins can opt into deferred loading via the `startup.deferConfiguredChannelFullLoadUntilAfterListen` flag:

```json
{
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "startup": {
      "deferConfiguredChannelFullLoadUntilAfterListen": true
    }
  }
}
```

When enabled, OpenClaw loads only `setupEntry` during the pre-listen startup phase, even for already-configured channels, and the full entry loads after the gateway starts listening. Only enable deferred loading when `setupEntry` registers everything the gateway needs before it starts listening (channel registration, HTTP routes, gateway methods); if the full entry owns required startup capabilities, keep the default behavior. If a setup or full entry registers gateway RPC methods, keep them on a plugin-specific prefix — the reserved core admin namespaces `config.*`, `exec.approvals.*`, `wizard.*`, and `update.*` stay core-owned and always resolve to `operator.admin`.

## Plugin manifest (`openclaw.plugin.json`)

Every native plugin must ship an `openclaw.plugin.json` in the package root; OpenClaw uses it to validate config without executing plugin code. A minimal manifest declares `id`, `name`, `description`, and a `configSchema`:

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "description": "Adds My Plugin capabilities to OpenClaw",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "webhookSecret": {
        "type": "string",
        "description": "Webhook verification secret"
      }
    }
  }
}
```

For channel plugins, add `kind: "channel"` and a `channels` array (e.g. `"channels": ["my-channel"]`). Even plugins with no config must ship a schema; an empty schema (`{ "type": "object", "additionalProperties": false }`) is valid. The full schema reference lives on the OpenClaw `plugins/manifest` page (digested in `oc_plugins_manifest`, pl04; see References).

## ClawHub publishing

For plugin packages, use the package-specific ClawHub command (run a `--dry-run` first):

```bash
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
```

The legacy skill-only publish alias is for skills; plugin packages should always use `clawhub package publish`.

## Setup entry (`setup-entry.ts`)

The `setup-entry.ts` file is a lightweight alternative to `index.ts` that OpenClaw loads when it only needs setup surfaces (onboarding, config repair, disabled-channel inspection). It is defined with `defineSetupPluginEntry` from the narrow `openclaw/plugin-sdk/channel-core` subpath:

```typescript
// setup-entry.ts
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/channel-core";
import { myChannelPlugin } from "./src/channel.js";

export default defineSetupPluginEntry(myChannelPlugin);
```

Using a setup entry avoids loading heavy runtime code (crypto libraries, CLI registrations, background services) during setup flows. Bundled workspace channels that keep setup-safe exports in sidecar modules can use `defineBundledChannelSetupEntry(...)` from `openclaw/plugin-sdk/channel-entry-contract` instead of `defineSetupPluginEntry(...)`; that bundled contract also supports an optional `runtime` export so setup-time runtime wiring stays lightweight and explicit. OpenClaw uses `setupEntry` instead of the full entry when the channel is disabled but needs setup/onboarding surfaces, when the channel is enabled but unconfigured, or when deferred loading is enabled. The setup entry **must** register the channel plugin object (via `defineSetupPluginEntry`), any HTTP routes required before gateway listen, and any gateway methods needed during startup (which should still avoid reserved core admin namespaces such as `config.*` or `update.*`); it should **not** include CLI registrations, background services, heavy runtime imports (crypto, SDKs), or gateway methods only needed after startup.

### Narrow setup helper imports

For hot setup-only paths, prefer the narrow setup-helper seams over the broader `plugin-sdk/setup` umbrella when you only need part of the setup surface. The three seams: `plugin-sdk/setup-runtime` — setup-time runtime helpers that stay available in `setupEntry` / deferred channel startup (key exports `createSetupTranslator`, `createPatchedAccountSetupAdapter`, `createEnvPatchedAccountSetupAdapter`, `createSetupInputPresenceValidator`, `noteChannelLookupFailure`, `noteChannelLookupSummary`, `promptResolvedAllowFrom`, `splitSetupEntries`, `createAllowlistSetupWizardProxy`, `createDelegatedSetupWizardProxy`); `plugin-sdk/setup-adapter-runtime` — a deprecated compatibility alias (use `plugin-sdk/setup-runtime`; exports `createEnvPatchedAccountSetupAdapter`); and `plugin-sdk/setup-tools` — setup/install CLI/archive/docs helpers (key exports `formatCliCommand`, `detectBinary`, `extractArchive`, `resolveBrewExecutable`, `formatDocsLink`, `CONFIG_DIR`). Use the broader `plugin-sdk/setup` seam when you want the full shared setup toolbox, including config-patch helpers such as `moveSingleAccountChannelSectionToDefaultAccount(...)`. Use `createSetupTranslator(...)` for fixed setup wizard copy — it follows the CLI wizard locale (`OPENCLAW_LOCALE`, then system locale variables) and falls back to English; keep plugin-specific setup text in plugin-owned code and use shared catalog keys only for common setup labels, status text, and official bundled plugin setup copy. The setup patch adapters stay hot-path safe on import: their bundled single-account promotion contract-surface lookup is lazy, so importing `plugin-sdk/setup-runtime` does not eagerly load bundled contract-surface discovery before the adapter is actually used.

### Channel-owned single-account promotion

When a channel upgrades from a single-account top-level config to `channels.<id>.accounts.*`, the default shared behavior is to move promoted account-scoped values into `accounts.default`. Bundled channels can narrow or override that promotion through their setup contract surface using `singleAccountKeysToMove` (extra top-level keys that should move into the promoted account), `namedAccountPromotionKeys` (when named accounts already exist, only these keys move into the promoted account; shared policy/delivery keys stay at the channel root), and `resolveSingleAccountPromotionTarget(...)` (choose which existing account receives promoted values). Matrix is the current bundled example: if exactly one named Matrix account already exists, or if `defaultAccount` points at an existing non-canonical key such as `Ops`, promotion preserves that account instead of creating a new `accounts.default` entry.

**Source**: OpenClaw documentation — `plugins/sdk-setup` (mirror `inbox/openclaw_docs/plugins/sdk-setup.md`)
**Last Updated**: 2026-06-22
**Status**: Active
