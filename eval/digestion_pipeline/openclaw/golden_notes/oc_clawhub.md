---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - registry
keywords:
  - clawhub registry
  - openclaw skills install
  - openclaw plugins install
  - clawhub cli publish
  - clawhub login whoami
  - clawpack tgz digest
  - pluginapi mingatewayversion compat
  - clawhub disable telemetry
topics:
  - OpenClaw
  - ClawHub
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub
access_control_group: ["general"]
---

# OpenClaw — Using ClawHub (the skill/plugin registry)

## Overview

This note is the procedure for using **ClawHub**, OpenClaw's public registry for skills and plugins, mirroring the `clawhub` source page. ClawHub splits into two command surfaces: native `openclaw` commands search, install, and update skills and install plugins from the registry, while the separate `clawhub` CLI handles registry auth, publishing, and delete/undelete workflows. This note walks through the quick-start install flows, what the registry hosts, native install/compat resolution, the `clawhub` CLI commands, publishing skills and plugins (with options, dry-run, and required compat metadata), security/moderation, and the telemetry/environment overrides. The registry site is [clawhub.ai](https://clawhub.ai).

## Quick start

Search and install **skills** with the native OpenClaw CLI:

```bash
openclaw skills search "calendar"
openclaw skills install @openclaw/demo
openclaw skills update --all
```

Search and install **plugins** with the native OpenClaw CLI:

```bash
openclaw plugins search "calendar"
openclaw plugins install clawhub:<package>
openclaw plugins update --all
```

Install the `clawhub` CLI when you want registry-authenticated workflows such as publish or delete/undelete:

```bash
npm i -g clawhub
# or
pnpm add -g clawhub
```

## What ClawHub hosts

ClawHub hosts three surfaces, each with a typical command:

| Surface | What it stores | Typical command |
| --- | --- | --- |
| Skills | Versioned text bundles with `SKILL.md` plus supporting files | `openclaw skills install @openclaw/demo` |
| Code plugins | OpenClaw plugin packages with compatibility metadata | `openclaw plugins install clawhub:<package>` |
| Bundle plugins | Packaged plugin bundles for OpenClaw distribution | `clawhub package publish <source>` |

ClawHub tracks semver versions, tags such as `latest`, changelogs, files, installs, stars, and security scan summaries. Public pages show current registry state so users can inspect a skill or plugin before installing it.

## Native OpenClaw flows

Native OpenClaw commands install into the active OpenClaw workspace and persist source metadata so later update commands can stay on ClawHub. Use `clawhub:<package>` when a plugin install should resolve through ClawHub; bare npm-safe plugin specs may resolve through npm during launch cutovers, and `npm:<package>` stays npm-only when a source must be explicit. Plugin installs validate advertised `pluginApi` and `minGatewayVersion` compatibility before archive install runs. When a package version publishes a **ClawPack** artifact, OpenClaw prefers the exact uploaded npm-pack `.tgz`, verifies the ClawHub digest header and downloaded bytes, and records artifact metadata for later updates.

## ClawHub CLI

The `clawhub` CLI is for registry-authenticated work — auth, search, and publishing:

```bash
clawhub login
clawhub whoami
clawhub search "postgres backups"
clawhub skill publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0
clawhub package explore --family code-plugin
clawhub package inspect episodic-claw
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
```

The CLI also has skill install/update commands for direct registry workflows:

```bash
clawhub install @openclaw/demo
clawhub update @openclaw/demo
clawhub update --all
clawhub list
```

Those commands install skills into `./skills` under the current working directory and record installed versions in `.clawhub/lock.json`.

## Publishing

Publish **skills** from a local folder containing `SKILL.md` with `clawhub skill publish <path>`. The common publish options are:

- `--slug <slug>`: published skill URL name.
- `--name <name>`: display name.
- `--version <version>`: semver version.
- `--changelog <text>`: changelog text.
- `--tags <tags>`: comma-separated tags, defaulting to `latest`.

Publish **plugins** from a local folder, `owner/repo`, `owner/repo@ref`, or a GitHub URL with `clawhub package publish <source>`. Use `--dry-run` to build the exact publish plan without uploading, and `--json` for CI-friendly output. Code plugins must include the required OpenClaw compatibility metadata in `package.json`, including `openclaw.compat.pluginApi` and `openclaw.build.openclawVersion`. See the CLI reference for the full command reference and the skill-format page for skill metadata.

## Security and moderation

ClawHub is open by default: anyone can upload, but publishing requires a GitHub account old enough to pass the upload gate. Public detail pages summarize the latest scan state before install or download. ClawHub runs automated checks on published skills and plugin releases; scan-held or blocked releases may disappear from public catalog and install surfaces while remaining visible to their owner in `/dashboard`. Signed-in users can report skills and packages, and moderators can review reports, hide or restore content, and ban abusive accounts. Policy and enforcement details live on the Security, Security Audits, Moderation and Account Safety, and Acceptable-usage pages.

## Telemetry and environment

When you run `clawhub install` while logged in, the CLI may send a best-effort install event so ClawHub can compute aggregate install counts. Disable this with `export CLAWHUB_DISABLE_TELEMETRY=1`. The useful environment overrides are:

| Variable | Effect |
| --- | --- |
| `CLAWHUB_SITE` | Override the site URL used for browser login. |
| `CLAWHUB_REGISTRY` | Override the registry API URL. |
| `CLAWHUB_CONFIG_PATH` | Override where the CLI stores token/config state. |
| `CLAWHUB_WORKDIR` | Override the default working directory. |
| `CLAWHUB_DISABLE_TELEMETRY=1` | Disable install telemetry. |

See the Telemetry, HTTP API, and Troubleshooting pages for deeper reference material.

**Source**: OpenClaw documentation — `clawhub` (mirror `inbox/openclaw_docs/clawhub.md`)
**Last Updated**: 2026-06-22
**Status**: Active
