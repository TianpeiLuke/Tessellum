---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - quickstart
keywords:
  - clawhub quickstart
  - openclaw skills install
  - openclaw plugins install clawhub
  - clawhub login github token
  - clawhub skill publish
  - clawhub package publish
  - clawhub inspect package
  - clh_ api token
topics:
  - OpenClaw
  - ClawHub
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/quickstart
access_control_group: ["general"]
---

# OpenClaw — ClawHub Quickstart (Find, Install, Publish Skills and Plugins)

## Overview

This note is the step-by-step ClawHub quickstart procedure: how to find and install skills and plugins, sign in for publishing, publish a skill folder or a plugin package, and inspect a listing before installing. It mirrors the `clawhub/quickstart` source page in full. ClawHub is OpenClaw's registry for skills and plugins; the operative rule throughout is which CLI to use — **use OpenClaw when you are installing things into OpenClaw, and use the `clawhub` CLI when you are signing in, publishing, managing your own listings, or using registry-specific workflows**. The flows below assume an installed OpenClaw and, for publishing, an installed `clawhub` CLI.

## Find and install a skill

Skills are installed *into OpenClaw*, so the skill commands run through the `openclaw` CLI rather than the `clawhub` CLI. Search the registry, install a specific skill by slug, then update installed skills:

```bash
openclaw skills search "calendar"
openclaw skills install @openclaw/demo
openclaw skills update --all
```

`openclaw skills search "calendar"` searches the registry; `openclaw skills install @openclaw/demo` installs a skill by its slug (here the scoped `@openclaw/demo`); `openclaw skills update --all` updates all installed skills. OpenClaw records where the skill came from so later updates can continue to resolve through ClawHub.

## Find and install a plugin

Plugin discovery and install also run through OpenClaw. Search for plugins, install a ClawHub-hosted plugin with an explicit ClawHub source, then update installed plugins:

```bash
openclaw plugins search "calendar"
openclaw plugins install clawhub:<package>
openclaw plugins update --all
```

Use the `clawhub:` prefix (as in `openclaw plugins install clawhub:<package>`) when you want OpenClaw to resolve the package through ClawHub rather than npm or another source. `openclaw plugins update --all` updates all installed plugins.

## Sign in for publishing

Publishing, sign-in, and listing management use the separate `clawhub` CLI, which you install globally first, then sign in with GitHub and confirm your identity:

```bash
npm i -g clawhub
# or
pnpm add -g clawhub

clawhub login
clawhub whoami

# Headless environments: use an API token from the ClawHub web UI instead
clawhub login --token clh_...
```

`clawhub login` performs a GitHub sign-in; `clawhub whoami` confirms the signed-in identity. Headless environments can use an API token from the ClawHub web UI instead of the interactive GitHub flow: `clawhub login --token clh_...` passes a ClawHub API token (prefixed `clh_`) generated from the ClawHub web UI, which is the appropriate path for headless/CI environments where the interactive GitHub login is not available.

## Publish a skill

A skill is a folder with a required `SKILL.md` file and optional supporting files. Publish the folder by pointing `clawhub skill publish` at it and supplying the slug, display name, and changelog:

```bash
clawhub skill publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --changelog "Initial release"
```

The command skips unchanged content. New skills start at `1.0.0`; later changes automatically publish the next patch version. Use `--dry-run` to preview or `--version` to choose an explicit version. Before publishing, check the metadata in `SKILL.md` — declare required environment variables, tools, and permissions so users can understand what the skill needs before they install it (see the Skill format page, linked under References / Related Notes).

For repositories containing multiple skills, the reusable GitHub workflow calls `skill publish` for each immediate skill folder under `skills/`:

```yaml
jobs:
  preview:
    uses: openclaw/clawhub/.github/workflows/skill-publish.yml@main
    with:
      dry_run: true
```

## Publish a plugin

Plugin publishing uses `clawhub package publish`, which accepts a local folder, a GitHub repo, a GitHub ref, or an existing archive as `<source>`. Preview with `--dry-run` first, then publish for real:

```bash
clawhub package publish <source> --family code-plugin --dry-run
clawhub package publish <source> --family code-plugin
```

Use `--dry-run` first to preview the resolved package metadata, compatibility fields, source attribution, and upload plan without publishing. Code plugins must include OpenClaw compatibility metadata in `package.json`, including `openclaw.compat.pluginApi` and `openclaw.build.openclawVersion`.

## Inspect before installing

Before installing, use the ClawHub web page or CLI detail commands to inspect metadata, source links, versions, changelogs, and scan status. The CLI detail commands are `clawhub inspect @openclaw/demo` (inspects a skill listing) and `clawhub package inspect <package>` (inspects a plugin/package listing). Public listings show the latest scan state, and releases that are held or blocked by moderation may be hidden from search and install surfaces until resolved.

**Source**: OpenClaw documentation — `clawhub/quickstart` (mirror `inbox/openclaw_docs/clawhub/quickstart.md`)
**Last Updated**: 2026-06-22
**Status**: Active
