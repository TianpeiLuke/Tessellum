---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - release_channels
keywords:
  - openclaw release channels
  - openclaw update channel
  - stable beta dev channels
  - npm dist-tag latest beta dev
  - openclaw update tag pinning
  - openclaw update dry run
  - openclaw update status
  - immutable git tag best practices
topics:
  - OpenClaw
  - Release Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/development-channels
access_control_group: ["general"]
---

# OpenClaw — Release Channels (stable / beta / dev): Switching, Pinning, and Tagging

## Overview

This note is the procedure for selecting, switching, and pinning OpenClaw's three update channels via `openclaw update`, mirroring the `install/development-channels` source page. It covers the channel-to-npm-dist-tag mapping (`stable`→`latest`, `beta`→`beta`, `dev`→`main`), how `--channel` persists `update.channel` and aligns the install method (npm dist-tag vs git-tag checkout vs moving `main`), one-off non-persistent `--tag` version/SHA/package-spec targeting with downgrade protection, the `--dry-run` preview, per-channel plugin syncing, `openclaw update status`, immutable-tag best practices, and the caveat that beta/dev builds may omit a macOS app release. Every other install page (`oc_install_ansible`, `oc_install_azure`, `oc_install_digitalocean`) defers to this flow for keeping a deployed gateway current.

## The Three Update Channels

OpenClaw ships three update channels, each backed by an npm dist-tag and a release policy:

- **stable** — npm dist-tag `latest`. Recommended for most users.
- **beta** — npm dist-tag `beta` when it is current; if beta is missing or older than the latest stable release, the update flow falls back to `latest`.
- **dev** — the moving head of `main` (git). npm dist-tag: `dev` (when published). The `main` branch is for experimentation and active development; it may contain incomplete features or breaking changes, so it must not be used for production gateways.

The release policy is beta-first: stable builds usually ship to **beta** first, are tested there, then an explicit promotion step moves the vetted build to `latest` **without changing the version number**. Maintainers can also publish a stable release directly to `latest` when needed. Dist-tags are the source of truth for npm installs.

## Switching Channels

Switch channels with the `--channel` flag, which persists the choice in config (`update.channel`) and aligns the install method:

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

The install-method alignment per channel and install kind is:

- **`stable` (package installs)** — updates via npm dist-tag `latest`.
- **`beta` (package installs)** — prefers npm dist-tag `beta`, but falls back to `latest` when `beta` is missing or older than the current stable tag.
- **`stable` (git installs)** — checks out the latest stable git tag, excluding semver prerelease tags such as `-alpha.N`, `-beta.N`, `-rc.N`, `-dev.N`, `-next.N`, `-preview.N`, `-canary.N`, `-nightly.N`, and other prerelease suffixes.
- **`beta` (git installs)** — prefers the latest beta git tag, but falls back to the latest stable git tag when beta is missing or older.
- **`dev`** — ensures a git checkout (default `~/openclaw`, or `$OPENCLAW_HOME/openclaw` when `OPENCLAW_HOME` is set; override with `OPENCLAW_GIT_DIR`), switches to `main`, rebases on upstream, builds, and installs the global CLI from that checkout.

Per the source's Tip: to run stable and dev in parallel, keep two clones and point your gateway at the stable one.

## One-off Version or Tag Targeting

Use `--tag` to target a specific dist-tag, version, or package spec for a single update **without** changing the persisted channel:

```bash
# Install a specific version
openclaw update --tag 2026.4.1-beta.1

# Install from the beta dist-tag (one-off, does not persist)
openclaw update --tag beta

# Switch to the moving GitHub main checkout
openclaw update --channel dev

# Install a specific npm package spec
openclaw update --tag openclaw@2026.4.1-beta.1

# Install from GitHub main once without persisting the channel
openclaw update --tag main
```

The behavioral notes for `--tag` are:

- `--tag` applies to **package (npm) installs only**; git installs ignore it.
- The tag is not persisted — the next `openclaw update` uses the configured channel as usual.
- For package installs, OpenClaw pre-packs GitHub/git source specs into a temporary tarball before the staged npm install. Use `--channel dev` or `--install-method git --version main` when the moving `main` checkout should be the persistent install.
- Downgrade protection: if the target version is older than the current version, OpenClaw prompts for confirmation (skip with `--yes`).
- `--channel beta` differs from `--tag beta`: the channel flow can fall back to stable/`latest` when beta is missing or older, while `--tag beta` targets the raw `beta` dist-tag for that one run.

## Dry Run

Preview what `openclaw update` would do without making changes:

```bash
openclaw update --dry-run
openclaw update --channel beta --dry-run
openclaw update --tag 2026.4.1-beta.1 --dry-run
openclaw update --dry-run --json
```

The dry run shows the effective channel, target version, planned actions, and whether a downgrade confirmation would be required.

## Plugins and Channels

When you switch channels with `openclaw update`, OpenClaw also syncs plugin sources:

- `dev` prefers bundled plugins from the git checkout.
- `stable` and `beta` restore npm-installed plugin packages.
- npm-installed plugins are updated after the core update completes.

## Checking Current Status

Inspect the active channel and install state with:

```bash
openclaw update status
```

It shows the active channel, install kind (git or package), current version, and source (config, git tag, git branch, or default).

## Tagging Best Practices

For maintainers publishing releases that git checkouts land on:

- Tag releases you want git checkouts to land on (`vYYYY.M.PATCH` for stable, `vYYYY.M.PATCH-beta.N` for beta). Named semver prerelease suffixes such as `-alpha.N`, `-rc.N`, and `-next.N` are not stable targets.
- Legacy numeric stable tags such as `vYYYY.M.PATCH-1` and `v1.0.1-1` are still recognized as stable git tags for compatibility.
- `vYYYY.M.PATCH.beta.N` is also recognized for compatibility, but prefer `-beta.N`.
- Keep tags immutable: never move or reuse a tag.
- npm dist-tags remain the source of truth for npm installs: `latest` → stable, `beta` → candidate build or beta-first stable build, `dev` → main snapshot (optional).

## macOS App Availability

Beta and dev builds may **not** include a macOS app release, and the source notes that is OK: the git tag and npm dist-tag can still be published, and release notes or changelog should call out "no macOS build for this beta".

**Source**: OpenClaw documentation — `install/development-channels` (mirror `inbox/openclaw_docs/install/development-channels.md`)
**Last Updated**: 2026-06-22
**Status**: Active
