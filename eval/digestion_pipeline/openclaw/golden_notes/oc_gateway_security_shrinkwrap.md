---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - supply_chain
keywords:
  - openclaw npm shrinkwrap
  - npm-shrinkwrap.json publish lockfile
  - pnpm-lock.yaml maintainer graph
  - supply-chain release reproducibility
  - bundledDependencies plugin tarball
  - deps:shrinkwrap:generate deps:shrinkwrap:check
  - package validators reject package-lock.json
  - inspect published openclaw package
topics:
  - OpenClaw
  - Gateway Security
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/security/shrinkwrap
access_control_group: ["general"]
---

# OpenClaw — npm Shrinkwrap as the Release-Reproducibility Boundary

## Overview

This note explains OpenClaw's use of **npm shrinkwrap** as a supply-chain and release-reproducibility boundary, mirroring the `gateway/security/shrinkwrap` source page. It covers the three lockfile roles (`pnpm-lock.yaml`, `npm-shrinkwrap.json`, `package-lock.json`), why OpenClaw ships a reviewed transitive dependency graph in published packages, and the maintainer generate/check commands plus package-inspection commands. The concept matters because OpenClaw is a gateway, plugin host, model router, and agent runtime, so a default install affects startup time, disk use, native package downloads, and supply-chain exposure — shrinkwrap gives release review a stable boundary over that graph.

## The easy version

Shrinkwrap is a receipt for the dependency tree that ships with an npm package: it tells npm which exact transitive package versions to install. OpenClaw source checkouts use `pnpm-lock.yaml`, while published OpenClaw npm packages use `npm-shrinkwrap.json` — npm's publishable dependency lockfile — so package installs use the dependency graph that was reviewed during release.

For OpenClaw releases, shipping that lockfile means the published package does not ask npm to invent a fresh dependency graph at install time; dependency changes become easier to review because they appear in a lockfile; release validation can test the same graph users will install; and package-size or native-dependency surprises are easier to spot before publishing.

Shrinkwrap is **not a sandbox**. It does not make a dependency safe by itself, and it does not replace host isolation, `openclaw security audit`, package provenance, or install smoke tests.

The short mental model from the source page:

| File | Where it matters | What it means |
| --------------------- | ------------------------ | --------------------------------- |
| `pnpm-lock.yaml` | OpenClaw source checkout | Maintainer dependency graph |
| `npm-shrinkwrap.json` | Published npm package | npm install graph for users |
| `package-lock.json` | Local npm apps | Not the OpenClaw publish contract |

## Why OpenClaw uses it

OpenClaw is a gateway, plugin host, model router, and agent runtime, so a default install can affect startup time, disk use, native package downloads, and supply-chain exposure. Shrinkwrap gives release review a stable boundary: reviewers can see transitive dependency movement; package validators can reject unexpected lockfile drift; package acceptance can test installs with the graph that will ship; and plugin packages can carry their own locked dependency graph instead of relying on the root package to own plugin-only dependencies. As the source states, the goal is not "more lockfiles" — the goal is reproducible release installs with clear ownership.

## Technical details

The root `openclaw` npm package and OpenClaw-owned npm plugin packages include `npm-shrinkwrap.json` when they publish. Suitable OpenClaw-owned plugin packages can also publish with explicit `bundledDependencies`, so their runtime dependency files are carried in the plugin tarball instead of depending only on install-time resolution.

Maintainers maintain the boundary with the standard generate/check pair:

```bash
pnpm deps:shrinkwrap:generate
pnpm deps:shrinkwrap:check
```

The generator resolves npm's publishable lock format but **rejects generated package versions that are not already present in `pnpm-lock.yaml`**, which keeps the pnpm dependency age, override, and patch-review boundary intact.

Root-only commands are used only when intentionally refreshing the root package without touching plugin packages:

```bash
pnpm deps:shrinkwrap:root:generate
pnpm deps:shrinkwrap:root:check
```

The source page calls out four artifacts to review as security-sensitive: `pnpm-lock.yaml`, `npm-shrinkwrap.json`, bundled plugin dependency payloads, and any `package-lock.json` diff.

On enforcement, OpenClaw **package validators require shrinkwrap in new root package tarballs**. The plugin npm publish path checks plugin-local shrinkwrap, installs package-local bundled dependencies, and then packs or publishes. Package validators **reject `package-lock.json` for published OpenClaw packages**.

To inspect a published **root** package and confirm the shrinkwrap is present in the tarball:

```bash
npm pack openclaw@<version> --json --pack-destination /tmp/openclaw-pack
tar -tf /tmp/openclaw-pack/openclaw-<version>.tgz | grep '^package/npm-shrinkwrap.json$'
```

To inspect an OpenClaw-owned **plugin** package, confirming both the plugin-local shrinkwrap and the bundled `node_modules`:

```bash
npm pack @openclaw/discord@<version> --json --pack-destination /tmp/openclaw-plugin-pack
tar -tf /tmp/openclaw-plugin-pack/openclaw-discord-<version>.tgz | grep '^package/npm-shrinkwrap.json$'
tar -tf /tmp/openclaw-plugin-pack/openclaw-discord-<version>.tgz | grep '^package/node_modules/'
```

**Source**: OpenClaw documentation — `gateway/security/shrinkwrap` (mirror `inbox/openclaw_docs/gateway/security/shrinkwrap.md`)
**Last Updated**: 2026-06-22
**Status**: Active
