---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - releasing
keywords:
  - openclaw release lanes
  - stable beta dev release lane
  - version naming yyyy.m.patch
  - monthly release train number
  - npm latest beta dist-tag
  - npm version immutability
  - release/yyyy.m.patch branch
  - beta-first release cadence
topics:
  - OpenClaw
  - Release Policy
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/reference/RELEASING
access_control_group: ["general"]
---

# OpenClaw — Release Lanes, Version Naming, and Cadence

## Overview

This note captures OpenClaw's public **release model**: the three public release lanes (stable / beta / dev), the `YYYY.M.PATCH` version-naming scheme with its June-2026 monthly-train rule, the meaning of the npm `latest` and `beta` dist-tags, the npm-version-immutability rule, and the beta-first release cadence cut from `release/YYYY.M.PATCH` branches. It mirrors the intro, `Version naming`, and `Release cadence` sections of the `reference/RELEASING` source page. The operator checklist + publish automation procedure and the validation/test-box procedure on the same page are documented separately in the sibling notes linked below; this note is the governing policy/concept the install, update, and announcement surfaces point back to.

## The Three Public Release Lanes

OpenClaw has three public release lanes:

- **stable**: tagged releases that publish to npm `beta` by default, or to npm `latest` when explicitly requested.
- **beta**: prerelease tags that publish to npm `beta`.
- **dev**: the moving head of `main`.

So a stable release is not automatically the npm `latest` install target — the default publish destination for stable (and stable correction) releases is the npm `beta` dist-tag, with `latest` promotion being an explicit operator decision. The `dev` lane is not a tagged artifact at all; it is whatever `main` currently points at.

## Version Naming

Versions follow a calendar-style `YYYY.M.PATCH` scheme, with distinct forms for stable, stable-correction, and beta-prerelease releases, each carrying a matching `v`-prefixed git tag:

- **Stable release version**: `YYYY.M.PATCH` — git tag `vYYYY.M.PATCH`.
- **Stable correction release version**: `YYYY.M.PATCH-N` — git tag `vYYYY.M.PATCH-N`.
- **Beta prerelease version**: `YYYY.M.PATCH-beta.N` — git tag `vYYYY.M.PATCH-beta.N`.

The month and patch components are **not zero-padded**.

### The monthly release-train rule (June 2026)

Starting with the **June 2026 release process update**, the third component (`PATCH`) is a **sequential monthly release-train number, not a calendar day**. Stable and beta releases determine the current train; **alpha-only tags do not consume or advance the beta/stable patch number**. Pre-update tags and npm versions keep their existing names and remain valid; release automation continues to compare them by year, month, patch, channel, and prerelease or correction number.

Alpha/nightly builds use the next unreleased patch train and increment only `alpha.N` for repeated builds. Once that patch has a beta, new alpha builds move to the following patch. When selecting a beta or stable train, **ignore legacy alpha-only tags with higher patch numbers**.

### npm version immutability

**npm versions are immutable.** If a beta tag has already been published, do not delete, republish, or reuse it; cut the next beta number or the next monthly patch instead. Because `2026.6.5-beta.1` was already published during the transition, **June 2026 release trains must use patch `5` or higher** — do not publish new June 2026 stable or beta trains as `2026.6.2`, `2026.6.3`, or `2026.6.4`. After stable `2026.6.5`, the next new beta train is `2026.6.6-beta.1`, even if automated alpha-only tags with higher patch numbers already exist.

### dist-tag meanings and what ships per release

- `latest` means the **current promoted stable npm release**.
- `beta` means the **current beta install target**.
- Stable and stable correction releases publish to npm `beta` **by default**; release operators can target `latest` explicitly, or promote a vetted beta build later.

Every **stable** OpenClaw release ships the npm package, the macOS app, and signed Windows Hub installers **together**. **beta** releases normally validate and publish the npm/package path first, with native app build/sign/notarize/promote reserved for stable unless explicitly requested.

## Release Cadence

The cadence is **beta-first**, with stable gated behind a validated beta and release work isolated on a dedicated branch:

- Releases move beta-first.
- **Stable follows only after the latest beta is validated.**
- Maintainers normally cut releases from a `release/YYYY.M.PATCH` branch created from current `main`, so release validation and fixes do not block new development on `main`.
- If a beta tag has been pushed or published and needs a fix, maintainers **cut the next `-beta.N` tag** instead of deleting or recreating the old beta tag (consistent with the npm-immutability rule above).
- Detailed release procedure, approvals, credentials, and recovery notes are maintainer-only (the public-shape operator checklist is captured in the sibling note below).

**Source**: OpenClaw documentation — `reference/RELEASING` (mirror `inbox/openclaw_docs/reference/RELEASING.md`; intro + Version naming + Release cadence sections)
**Last Updated**: 2026-06-22
**Status**: Active
