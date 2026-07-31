---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - registry
keywords:
  - clawhub registry layer
  - clawhub how it works
  - registry record owner slug versions
  - skill skill.md bundle listing
  - plugin package compatibility metadata
  - immutable version publishing clawhub
  - installs and updates package source
  - security scan moderation status
  - clawhub public read api
topics:
  - OpenClaw
  - ClawHub
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/clawhub/how-it-works
access_control_group: ["general"]
---

# OpenClaw — How ClawHub Works (The Registry Layer)

## Overview

This note explains the **ClawHub** concept as documented on the `clawhub/how-it-works` source page: ClawHub is the registry layer for OpenClaw skills and plugins. It gives users a place to discover packages, gives publishers a place to release versions, and gives OpenClaw enough metadata to install and update those packages safely. The page walks the full conceptual surface — what a registry record holds, what skills and plugins are as registry records, how publishing creates immutable version records, how installs and updates resolve back to a registry package, what security state a listing carries, and that ClawHub exposes public read APIs. This note covers all seven H2 sections plus the intro; the CLI workflows, the public REST API contract, and the marketplace policy that this concept references are documented in their own sibling notes (see Related Notes).

## Registry records

Each public listing is a registry record. The page enumerates exactly what a record holds: an owner and slug or package name; one or more published versions; metadata, summary, files, and source attribution; changelog and tag information such as `latest`; download, install, and star signals; and security scan and moderation status. The listing page is the canonical place for users to inspect what a skill or plugin claims to do before installing it.

## Skills

A skill is a versioned text bundle centered on `SKILL.md`. It can include supporting files, examples, templates, and scripts. ClawHub reads the `SKILL.md` frontmatter to understand the skill name, description, requirements, environment variables, and metadata. The page notes that accurate metadata matters because it helps users decide whether to install the skill and helps automated scans detect mismatches between declared and observed behavior. The page links out to the dedicated skill-format reference (`/clawhub/skill-format`, owned by cw03).

## Plugins

Plugins are packaged OpenClaw extensions. ClawHub stores package metadata, compatibility information, source links, artifacts, and version records. When OpenClaw installs a plugin from ClawHub, it checks advertised compatibility metadata before installing. Per the source, package records can include API compatibility, minimum gateway version, host targets, environment requirements, and artifact digests. To make the registry the source of truth, the page shows using an explicit ClawHub install source:

```bash
openclaw plugins install clawhub:<package>
```

## Publishing

Publishing creates a new immutable version record. Publishers use the `clawhub` CLI for authenticated registry workflows. The page reproduces the publish entry points (a skill publish and the dry-run/real package publish pair):

```bash
clawhub skill publish ./my-skill
clawhub package publish <source> --family code-plugin --dry-run
clawhub package publish <source> --family code-plugin
```

The page recommends using dry runs to preview the resolved payload before upload. After publishing, public pages surface the published metadata, files, source attribution, and scan status. The owner/review/trusted-publishing mechanics behind this are detailed in the publishing reference (`/clawhub/publishing`, owned by cw02).

## Installs and updates

OpenClaw install commands use ClawHub as a package source. The page shows the two install entry points (a skill install by `@owner/slug` and a plugin install by ClawHub source):

```bash
openclaw skills install @openclaw/demo
openclaw plugins install clawhub:<package>
```

OpenClaw records install source metadata so that updates can resolve the same registry package later — install source is the persisted source of truth for later resolution. The page also notes that the ClawHub CLI itself supports direct skill install and update workflows for users who want registry-managed skill folders outside a full OpenClaw workspace.

## Security state

ClawHub is open to publishing, but releases are still subject to upload gates, automated checks, user reports, and moderator action. Public pages show scan summaries when available. Content that is held, hidden, or blocked may disappear from public search and install flows while remaining visible to the owner for diagnostics. The page links to the security, security-audits, moderation/account-safety, and acceptable-usage references for the detail behind these states (`/clawhub/security` and `/clawhub/security-audits` → cw03; `/clawhub/moderation` → cw02; `/clawhub/acceptable-usage`).

## API access

ClawHub exposes public read APIs for discovery, search, package details, and downloads. The page sets the reuse condition: third-party catalogs may use these APIs when they link back to the canonical ClawHub listing, respect rate limits, and avoid implying endorsement. It links to the public API overview (`/clawhub/api`) and the HTTP API deep dive (`/clawhub/http-api` → cw02).

**Source**: OpenClaw documentation — `clawhub/how-it-works` (mirror `inbox/openclaw_docs/clawhub/how-it-works.md`)
**Last Updated**: 2026-06-22
**Status**: Active
