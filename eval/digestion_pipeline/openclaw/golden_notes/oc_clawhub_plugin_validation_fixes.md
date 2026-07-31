---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - plugin_validation
keywords:
  - clawhub package validate
  - plugin validation findings
  - openclaw plugin metadata fix
  - package.json openclaw block
  - openclaw.plugin.json manifest
  - legacy-root-sdk-import migration
  - before_agent_start hook migration
  - npm pack entrypoint missing
  - openclaw.compat.pluginApi
  - security manifest schema
topics:
  - OpenClaw
  - ClawHub
  - Plugin Validation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/plugin-validation-fixes
access_control_group: ["general"]
---

# OpenClaw — ClawHub Plugin Validation Fixes

## Overview

This procedure note documents how a plugin author remediates the **author-facing findings** that `clawhub package validate` (and ClawHub's automated package scans) raise before a plugin package is published, mirroring the `clawhub/plugin-validation-fixes` source page. "Author-facing" means findings the author can fix in their own package metadata, manifest, SDK imports, or published artifact — it explicitly does **not** cover internal Plugin Inspector coverage findings, and any scanner maintenance codes that appear in a full report without author remediation guidance are for OpenClaw maintainers, not plugin authors. The page enumerates 23 finding codes grouped into five families: package metadata (9 codes), published artifact (3 codes), manifest metadata (3 codes), SDK and compatibility migration (6 codes), and security manifest (2 codes). The universal remediation loop is: apply the fix, then **rerun** `clawhub package validate <path-to-plugin>` until the finding clears.

## Rerun After Every Fix

After applying any fix described below, rerun the validator against the package directory:

```bash
clawhub package validate <path-to-plugin>
```

Every individual finding's remediation ends with this same rerun step. The validator both checks pre-publish package state and surfaces findings from automated package scans, so the fix → rerun cycle is repeated per finding until validation passes.

## Author-Facing Findings (Code → Start Here)

The page opens with a lookup table mapping each finding **code** to its remediation section. The 23 author-facing codes are: `package-json-missing`, `package-openclaw-metadata-missing`, `package-openclaw-entry-missing`, `package-entrypoint-missing`, `package-install-metadata-incomplete`, `package-plugin-api-compat-missing`, `package-min-host-version-drift`, `package-manifest-version-drift`, `package-openclaw-unsupported-metadata`, `package-npm-pack-unavailable`, `package-npm-pack-entrypoint-missing`, `package-npm-pack-metadata-missing`, `manifest-name-missing`, `manifest-unknown-fields`, `manifest-unknown-contracts`, `legacy-root-sdk-import`, `reserved-sdk-import`, `sdk-load-session-store`, `legacy-before-agent-start`, `provider-auth-env-vars`, `channel-env-vars`, `security-manifest-schema-unavailable`, and `unrecognized-security-manifest`. Each table row gives a "Start here" pointer to the matching remediation anchor on the page (for example, `package-json-missing` points to the *Add package metadata* anchor `#package-json-missing`).

## Package Metadata (9 codes)

These findings concern `package.json` and its `openclaw` block — the metadata ClawHub uses to identify the npm package, version, entrypoints, compatibility, and install behavior.

- **`package-json-missing`** — The package root has no `package.json`, so ClawHub cannot identify the npm package, version, entrypoints, or OpenClaw metadata. Add `package.json` with `name`, `version`, and `type`; add an `openclaw` block when the package ships an OpenClaw plugin (see *Building plugins* for a minimal example and *Plugin manifest* for the package-versus-manifest split).
- **`package-openclaw-metadata-missing`** — `package.json` exists but declares no OpenClaw package metadata. Add `package.json#openclaw`, include entrypoint metadata such as `openclaw.extensions` or `openclaw.runtimeExtensions`, and add compatibility and install metadata when the package will be published or installed through ClawHub.
- **`package-openclaw-entry-missing`** — Package metadata exists but declares no OpenClaw runtime entrypoint. Add `openclaw.extensions` for native plugin entrypoints, add `openclaw.runtimeExtensions` when the published package should load built JavaScript, and keep all entrypoint paths inside the package directory.
- **`package-entrypoint-missing`** — The package declares an OpenClaw entrypoint, but the referenced file is missing from the package being validated. Check each path in `openclaw.extensions`, `openclaw.runtimeExtensions`, `openclaw.setupEntry`, and `openclaw.runtimeSetupEntry`; build the package if the entrypoint is generated into `dist`; update the metadata if the entrypoint moved.
- **`package-install-metadata-incomplete`** — ClawHub cannot tell how the package should be installed or updated. Fill `openclaw.install` with the supported install source (`clawhubSpec`, `npmSpec`, or `localPath`), set `openclaw.install.defaultChoice` when more than one source is available, and use `openclaw.install.minHostVersion` for the minimum OpenClaw host version.
- **`package-plugin-api-compat-missing`** — The package does not declare the OpenClaw plugin API range it supports. Add `openclaw.compat.pluginApi` to `package.json`, using the OpenClaw plugin API version or semver floor you built and tested against. Keep this separate from the package version: the package version describes the plugin release, while `openclaw.compat.pluginApi` describes the host API contract.
- **`package-min-host-version-drift`** — The package minimum host version does not match the OpenClaw version metadata it was built against. Check `openclaw.install.minHostVersion`, check any OpenClaw build metadata in the package (such as the OpenClaw version used during release), and align the minimum host version with the host version range the package actually supports.
- **`package-manifest-version-drift`** — The package version and plugin manifest version disagree. Prefer `package.json#version` as the package release version; if `openclaw.plugin.json` also has `version`, update it to match or remove stale manifest version metadata when package metadata is authoritative; publish a new package version after changing published metadata.
- **`package-openclaw-unsupported-metadata`** — The `package.json#openclaw` block contains fields that are not supported OpenClaw package metadata. Remove unsupported fields such as `openclaw.bundle`, keep native plugin metadata in `openclaw.plugin.json`, and keep package entrypoints, compatibility, install, setup, and catalog metadata in the supported `package.json#openclaw` fields.

## Published Artifact (3 codes)

These findings concern the `npm pack` output — the artifact ClawHub inspects and publishes. The shared diagnostic is `npm pack --dry-run` from the package root.

- **`package-npm-pack-unavailable`** — The package cannot be packed into the artifact ClawHub would inspect or publish. Run `npm pack --dry-run` from the package root; fix invalid package metadata, broken lifecycle scripts, or `files` entries that make packing fail; remove `private: true` if the package is intended for public publishing.
- **`package-npm-pack-entrypoint-missing`** — The package packs, but the packed artifact does not include the entrypoint files declared in `package.json#openclaw`. Run `npm pack --dry-run` and inspect the included files, build generated entrypoints before packing, and update `files`, `.npmignore`, or build output so declared entrypoints are included.
- **`package-npm-pack-metadata-missing`** — The packed artifact is missing OpenClaw metadata that exists in your source package. Run `npm pack --dry-run` and inspect the included metadata files; ensure `package.json` includes the `openclaw` block in the packed artifact; ensure `openclaw.plugin.json` is included when the package is a native OpenClaw plugin; update `files` or `.npmignore` so package metadata is not excluded.

## Manifest Metadata (3 codes)

These findings concern the native plugin manifest `openclaw.plugin.json` and its supported fields.

- **`manifest-name-missing`** — The native plugin manifest does not include a display name. Add a non-empty `name` field to `openclaw.plugin.json`, keeping `name` human-readable and `id` as the stable machine id.
- **`manifest-unknown-fields`** — The plugin manifest has top-level fields OpenClaw does not support. Compare each top-level field with the manifest field reference, remove custom fields from `openclaw.plugin.json`, and move package or install metadata into supported `package.json#openclaw` fields instead of the manifest.
- **`manifest-unknown-contracts`** — The manifest declares unsupported keys inside `contracts`. Compare each key under `contracts` with the contracts reference, remove unsupported contract keys, and move runtime behavior into plugin registration code — keeping `contracts` limited to static capability-ownership metadata.

## SDK and Compatibility Migration (6 codes)

These findings flag deprecated or reserved SDK imports and legacy hooks. The recurring pattern is to replace a deprecated surface with the current public one, while keeping the legacy surface **only** as long as your declared compatibility range still supports older OpenClaw versions that require it.

- **`legacy-root-sdk-import`** — The plugin imports from the deprecated root SDK barrel `openclaw/plugin-sdk`. Replace root-barrel imports with focused public subpath imports: use `openclaw/plugin-sdk/plugin-entry` for `definePluginEntry` and `openclaw/plugin-sdk/channel-core` for channel entry helpers (see *Import conventions* and *Plugin SDK subpaths* to find the narrow import).
- **`reserved-sdk-import`** — The plugin imports an SDK path reserved for bundled plugins or internal compatibility. Replace reserved OpenClaw-internal SDK imports with documented public `openclaw/plugin-sdk/*` subpaths; if the behavior has no public SDK, keep the helper inside your package or request a public OpenClaw API (see *Plugin SDK subpaths* and *SDK migration*).
- **`sdk-load-session-store`** — The plugin still uses the deprecated whole-session-store helper `loadSessionStore`. Use `getSessionEntry(...)` or `listSessionEntries(...)` to read session state and `patchSessionEntry(...)` or `upsertSessionEntry(...)` to write it; avoid loading, mutating, and saving the whole session-store object; keep `loadSessionStore(...)` only while your declared compatibility range still supports older OpenClaw versions that require it.
- **`legacy-before-agent-start`** — The plugin still uses the legacy `before_agent_start` hook. Move model or provider override work to `before_model_resolve`, move prompt or context mutation work to `before_prompt_build`, and keep `before_agent_start` only while your declared compatibility range still supports older OpenClaw versions (see *Hooks* and *Plugin compatibility*).
- **`provider-auth-env-vars`** — The manifest still uses legacy `providerAuthEnvVars` provider-auth metadata. Mirror provider env-var metadata into `setup.providers[].envVars` and keep `providerAuthEnvVars` only as compatibility metadata while your supported OpenClaw range still needs it (see *setup reference* and *SDK migration*).
- **`channel-env-vars`** — The manifest uses legacy or older channel env-var metadata without the current setup or config metadata ClawHub expects. Keep channel env-var metadata declarative so OpenClaw can inspect setup status without loading channel runtime, mirror env-driven channel setup into the current setup / channel config / package channel metadata for your plugin shape, and keep `channelEnvVars` only as compatibility metadata while older supported OpenClaw versions still require it.

## Security Manifest (2 codes)

These findings concern an `openclaw.security.json` file whose schema or format ClawHub does not currently recognize, because OpenClaw has not yet published a versioned security-manifest contract.

- **`security-manifest-schema-unavailable`** — The package ships `openclaw.security.json` with a schema reference ClawHub does not recognize as available. Remove the schema URL if it is advisory-only, and use a documented versioned schema only after OpenClaw publishes one.
- **`unrecognized-security-manifest`** — The package ships an unsupported security-manifest file. Remove `openclaw.security.json` until OpenClaw documents a versioned security-manifest schema and ClawHub behavior, and keep security-sensitive behavior documented in your public package docs or README until the manifest contract exists.

**Source**: OpenClaw documentation — `clawhub/plugin-validation-fixes` (mirror `inbox/openclaw_docs/clawhub/plugin-validation-fixes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
