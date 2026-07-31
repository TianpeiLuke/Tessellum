---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - cli
keywords:
  - clawhub package cli
  - clawhub package publish
  - clawpack npm-pack tarball
  - package trusted-publisher oidc
  - publisher create org
  - package verify sha256 npm integrity
  - package validate plugin inspector
  - package moderation-status readiness
  - clawhub install telemetry
topics:
  - OpenClaw
  - ClawHub
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/cli
access_control_group: ["general"]
---

# OpenClaw — ClawHub CLI: Package (Plugin) Workflows

## Overview

This note is the package/plugin half of the `clawhub` CLI reference — the procedures for browsing, inspecting, downloading, verifying, validating, publishing, and governing ClawHub **packages** (the plugin family, including code plugins and bundle plugins, packaged as ClawPack npm-pack tarballs). It mirrors the `clawhub/cli` source page from the `package …`, `publisher`, and `package trusted-publisher` command sections through Install telemetry. The skill-side commands (`install`/`search`/`pin`/`skill publish`/`scan`/lifecycle) and the shared global flags, HTTP proxy, and config-file behavior live in the sibling note [oc_clawhub_cli_skills](oc_clawhub_cli_skills.md); this note assumes that setup (the CLI binary is `clawhub`, installed via `npm i -g clawhub`) and an established `clawhub login`. All endpoints, flags, and digests below are reproduced verbatim from the source.

## Browse, Inspect, and Download Packages

`package explore [query...]` browses or searches the unified package catalog via `GET /api/v1/packages` and `GET /api/v1/packages/search` (e.g. `clawhub package explore --family code-plugin`, `clawhub package explore episodic-claw --family code-plugin`). Use it for plugins and other package-family entries (top-level `search` remains the skill search surface). Its flags filter by family (`--family skill|code-plugin|bundle-plugin`), `--official`, `--executes-code`, host targeting (`--target <target>`, `--os <os>`, `--arch <arch>`, `--libc <libc>`), capability requirements (`--requires-browser`, `--requires-desktop`, `--requires-native-deps`, `--requires-external-service`, `--external-service <name>`), `--binary <name>`, `--os-permission <name>`, `--artifact-kind legacy-zip|npm-pack`, `--npm-mirror`, `--limit <n>` (1-100, default: 25), and `--json`.

`package inspect <name>` fetches package metadata without installing — use it for plugin metadata, compatibility, verification, source, and version/file inspection. Its flags mirror the skill `inspect`: `--version <version>` (default: latest), `--tag <tag>` (e.g. `latest`), `--versions` (list version history, first page), `--limit <n>` (max versions to list, 1-100), `--files` (list files for the selected version), `--file <path>` (fetch raw file content; text files only; 200KB limit), and `--json`.

`package download <name>` resolves a package version through `GET /api/v1/packages/{name}/versions/{version}/artifact` and downloads the artifact from the resolver's `downloadUrl`. It verifies the ClawHub **SHA-256** for all artifacts; for ClawPack npm-pack artifacts it additionally verifies npm `sha512` integrity, the npm shasum, and the tarball's `package.json` name/version. Legacy ZIP versions download through the legacy ZIP route. Flags: `--version <version>`, `--tag <tag>` (default: `latest`), `-o, --output <path>` (output file or directory), `--force` (overwrite an existing output file), `--json`.

```bash
clawhub package download @openclaw/example-plugin --tag latest
clawhub package download @openclaw/example-plugin --version 1.2.3 -o artifacts/
```

## Verify and Validate

`package verify <file>` computes the ClawHub SHA-256, npm `sha512` integrity, and npm shasum for a local artifact. With `--package`, it resolves expected metadata from ClawHub and compares the local file against the published artifact metadata; with direct digest flags it verifies without a network lookup. Flags: `--package <name>` (resolve expected artifact metadata), `--version <version>` or `--tag <tag>` (expected package version), `--sha256 <hex>` (expected ClawHub SHA-256), `--npm-integrity <sri>` (expected npm integrity), `--npm-shasum <sha1>` (expected npm shasum), `--json`.

```bash
clawhub package verify ./example-plugin-1.2.3.tgz --package @openclaw/example-plugin --version 1.2.3
clawhub package verify ./example-plugin-1.2.3.tgz --sha256 <hex>
```

`package validate <source>` runs the ClawHub CLI's bundled **Plugin Inspector** against a local plugin package folder (e.g. `clawhub package validate ./example-plugin`). It defaults to offline/static validation, without locating or importing a local OpenClaw checkout. Hard compatibility errors exit non-zero; warning-only findings are printed but exit zero. Flags: `--out <dir>` (write Plugin Inspector reports to this directory), `--openclaw <path>` (inspect against an explicit local OpenClaw checkout), `--runtime` (enable runtime capture; imports plugin code), `--allow-execute` (allow runtime capture in an isolated workspace), `--no-mock-sdk` (disable mocked OpenClaw SDK during runtime capture), `--json`. If validation reports a package, manifest, SDK import, or artifact finding, see the Plugin validation fixes page (`/clawhub/plugin-validation-fixes`), then rerun the command.

## Package Lifecycle: Delete, Undelete, Transfer, Report

`package delete <name>` without `--version` soft-deletes a package and all releases (requires the package owner, an org publisher owner/admin, platform moderator, or platform admin). `--version <version>` permanently deletes one owned non-latest release through a fail-closed, version-specific route — deleted versions cannot be restored or republished, so publish a replacement before deleting the current latest version; this version-only flow requires the package owner or an org publisher admin and platform staff do not bypass package ownership. Flags: `--version <version>`, `--yes` (skip confirmation), `--json`.

`package undelete <name>` restores a soft-deleted package and releases (there is no version undelete — permanently deleted versions cannot be restored). It requires the package owner, an org publisher owner/admin, platform moderator, or platform admin, and calls `POST /api/v1/packages/{name}/undelete`. Flags: `--yes`, `--json`.

`package transfer <name>` transfers a package to another publisher. It requires admin access to both the current package owner and destination publisher (unless performed by a platform admin), and scoped package names must transfer to the matching scope owner. It calls `POST /api/v1/packages/{name}/transfer`. Flags: `--to <owner>` (destination publisher handle), `--reason <text>` (optional audit reason), `--json`.

`package report` is an authenticated command for reporting a package to moderators via `POST /api/v1/packages/{name}/report` (e.g. `clawhub package report @openclaw/example-plugin --version 1.2.3 --reason "suspicious native payload"`). Reports are package-level, optionally tied to a version, and become visible to moderators for review; they do not auto-hide packages or block downloads by themselves. Flags: `--version <version>` (optional version to attach), `--reason <text>` (required report reason), `--json`. Example soft-delete and transfer invocations are `clawhub package delete @openclaw/example-plugin --version 1.2.3 --yes` and `clawhub package transfer @openclaw/example-plugin --to openclaw`.

## Moderation, Readiness, and Migration Status

`package moderation-status` is an owner command for checking package moderation visibility via `GET /api/v1/packages/{name}/moderation`. It shows the current package scan state, open report count, latest release manual moderation state, download block state, and moderation reasons (`--json` for machine-readable output).

`package readiness <name>` checks whether a package is ready for future OpenClaw consumption via `GET /api/v1/packages/{name}/readiness`. It reports blockers for official status, ClawPack availability, artifact digest, source provenance, OpenClaw compatibility, host targets, environment metadata, and scan state (`--json`).

`package migration-status <name>` shows operator-oriented migration status for a package that may replace a bundled OpenClaw plugin. It calls the same computed readiness endpoint as `package readiness`, but prints migration-focused status, latest version, official-package state, checks, and blockers (`--json`).

## Publishers and Package Publish

`publisher create <handle>` creates an org publisher owned by the authenticated user. The handle is normalized to lowercase and may be passed with or without `@`; newly created org publishers are not trusted/official by default; the command fails if the handle is already used by an existing publisher, user, or reserved route.

```bash
clawhub publisher create opik --display-name "Opik"
```

`package publish <source>` publishes a code plugin or bundle plugin via `POST /api/v1/packages`. `<source>` accepts a local folder path (`./my-plugin`), a local ClawPack npm-pack tarball (`./my-plugin-1.2.3.tgz`), a GitHub repo (`owner/repo` or `owner/repo@ref`), or a GitHub URL (`https://github.com/owner/repo`). Metadata is auto-detected from `package.json`, `openclaw.plugin.json`, and real OpenClaw bundle markers such as `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.cursor-plugin/plugin.json`. `.tgz` sources are treated as ClawPack — the CLI uploads the exact npm-pack bytes and uses the extracted `package/` contents only for validation and metadata prefill — while code-plugin folders are packed into a ClawPack npm tarball before upload (so OpenClaw installs can verify the exact artifact) and bundle-plugin folders still use the extracted-file publish path. For GitHub sources, source attribution is auto-populated from the repo, resolved commit, ref, and subpath; for local folders it is auto-detected from local git when the origin remote points at GitHub. External code plugins must declare `openclaw.compat.pluginApi` and `openclaw.build.openclawVersion` explicitly — top-level `package.json.version` is not used as a fallback for publish validation. Flags: `--dry-run` (preview the resolved publish payload without uploading), `--json` (machine-readable output for CI), `--owner <handle>` (publish under a user or org publisher handle when the actor has publisher access; scoped package names must match the selected owner — see `docs/publishing.md`), plus the override flags `--family`, `--name`, `--version`, `--source-repo`, `--source-commit`, `--source-ref`, `--source-path`. Private GitHub repos require `GITHUB_TOKEN`. The recommended local flow uses `--dry-run` first to confirm resolved metadata and source attribution before creating a live release.

```bash
npm pack
clawhub package publish ./my-plugin-1.2.3.tgz --family code-plugin --dry-run
clawhub package publish ./my-plugin --family code-plugin
```

### Minimal `package.json` for `--family code-plugin`

External code plugins need a small amount of OpenClaw metadata in `package.json`. The required fields are `openclaw.compat.pluginApi` and `openclaw.build.openclawVersion`. `package.json.version` is your package release version but is not used as a fallback for OpenClaw compatibility/build validation; `openclaw.hostTargets` and `openclaw.environment` are optional metadata (ClawHub may surface them when present, but they are not required); `openclaw.compat.minGatewayVersion` and `openclaw.build.pluginSdkVersion` are optional extras for more detailed compatibility metadata. Upgrade an older `clawhub` CLI before publishing so the local preflight checks run before upload; if validation reports a remediation code, see the Plugin validation fixes page (`/clawhub/plugin-validation-fixes`).

```json
{
  "name": "@myorg/openclaw-my-plugin",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "compat": {
      "pluginApi": ">=2026.3.24-beta.2"
    },
    "build": {
      "openclawVersion": "2026.3.24-beta.2"
    }
  }
}
```

### GitHub Actions

ClawHub ships an official reusable workflow at `/.github/workflows/package-publish.yml` for plugin repos. The reusable workflow defaults `source` to the caller repo; for monorepos pass `source_path` so the workflow publishes the plugin package folder (e.g. `source_path: extensions/codex`). Pin the reusable workflow to a stable tag or full commit SHA (do not run release publishing from `@main`); `pull_request` should use `dry_run: true` so CI stays non-polluting, and real publishes should be limited to trusted events such as `workflow_dispatch` or tag pushes. Trusted publishing without a secret only works on `workflow_dispatch` — tag pushes still need `clawhub_token` — so keep `clawhub_token` available for first publish, untrusted packages, or break-glass publishes; the publish job requires `permissions: contents: read` + `id-token: write`. The workflow uploads the JSON result as an artifact and exposes it as workflow outputs.

## Trusted Publisher (OIDC)

The `package trusted-publisher` subcommands manage GitHub Actions OIDC/trusted-publishing configuration, which lets future supported GitHub Actions publishes run without a long-lived ClawHub token. `package trusted-publisher get <name>` shows the configured repository, workflow filename, and optional environment pin (`--json`). `package trusted-publisher set <name>` attaches or replaces the config for an existing package (the package must be created first through normal manual or token-authenticated `clawhub package publish`): `--repository <repo>` must be `owner/repo`, `--workflow-filename <file>` must match the workflow file name in `.github/workflows/`, and `--environment <name>` is optional but, when configured, the GitHub Actions environment in the OIDC claim must match exactly. ClawHub verifies the configured GitHub repository when this command runs — public repositories can be verified through public GitHub metadata, while private repositories require ClawHub to have GitHub access to that repository (for example through a future ClawHub GitHub App installation or another authorized GitHub integration). `package trusted-publisher delete <name>` removes the config as a rollback if the workflow, repository, or environment pin needs to be disabled or re-created; future real publishes must then use normal authenticated publishing until config is set again. All three accept `--json`.

```bash
clawhub package trusted-publisher set @openclaw/example-plugin \
  --repository openclaw/example-plugin \
  --workflow-filename package-publish.yml \
  --environment release
```

## Install Telemetry

Install telemetry is sent after `clawhub install <slug>` when logged in, unless `CLAWHUB_DISABLE_TELEMETRY=1` is set. Reporting is best-effort — install commands do not fail if telemetry is unavailable. Further detail lives in `docs/telemetry.md` (ClawHub telemetry page, owned by sub-plan cw03).

**Source**: OpenClaw documentation — `clawhub/cli` (package/plugin command family; mirror `inbox/openclaw_docs/clawhub/cli.md`)
**Last Updated**: 2026-06-22
**Status**: Active
