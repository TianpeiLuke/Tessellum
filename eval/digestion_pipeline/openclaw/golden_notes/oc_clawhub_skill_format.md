---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - skill_format
keywords:
  - clawhub skill folder format
  - skill.md required file
  - clawhubignore publish
  - github importer rules
  - allowed text files 50mb
  - clawhub slug publisher handle
  - semver versioning tags latest
  - mit-0 license no paid skills
topics:
  - OpenClaw
  - ClawHub Skill Format
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/skill-format
access_control_group: ["general"]
---

# OpenClaw — ClawHub On-Disk Skill Folder Format

## Overview

This note is the procedure for the **on-disk ClawHub skill folder format** — the layout, required and optional files, GitHub import rules, allowed file types and size limits, slug/publisher-handle rules, versioning, and licensing/pricing constraints a publisher must satisfy. It mirrors the `clawhub/skill-format` source page sections **On disk**, **GitHub import**, **`SKILL.md`**, **Allowed files**, **Slugs**, **Versioning + tags**, **License**, and **Paid skills**. The `SKILL.md` **frontmatter / `metadata.openclaw` schema** (basic fields, runtime metadata, install specs, env-var declarations) is split into the sibling note [oc_clawhub_skill_frontmatter](oc_clawhub_skill_frontmatter.md); this note covers everything around the file, not the frontmatter field reference.

## On disk

A skill is a folder. The folder layout has exactly one required file plus a set of optional supporting files:

- **Required:** `SKILL.md` (or `skill.md`; the legacy name `skills.md` is also accepted).
- **Optional:** any supporting **text-based** files (see "Allowed files" below), a `.clawhubignore` file holding ignore patterns for publishing (legacy name `.clawdhubignore`), and a `.gitignore` (also honored for publish ignores).

There is no other mandatory file in the folder — a single `SKILL.md` is a valid, publishable skill.

## GitHub import

The web GitHub importer is **stricter than local publish/sync**. The rules for what the web importer will discover and import:

- It only discovers `SKILL.md` or legacy `skills.md` files in **public, non-fork repositories owned by the signed-in GitHub account**.
- It does **not** import private repos, forks, archived/disabled repos, or third-party public repos.

The CLI writes install metadata to the local filesystem in two places:

- **Local install metadata** (written by the CLI): `<skill>/.clawhub/origin.json` (legacy directory `.clawdhub`).
- **Workdir install state** (written by the CLI): `<workdir>/.clawhub/lock.json` (legacy directory `.clawdhub`).

## `SKILL.md`

The single required file is Markdown with optional YAML frontmatter, processed at publish time:

- It is Markdown with **optional** YAML frontmatter.
- The server **extracts metadata from the frontmatter during publish** (the field schema itself is documented in the sibling frontmatter note).
- The frontmatter `description` is used as the **skill summary in the UI/search**.

## Allowed files

Only **text-based** files are accepted by publish. The allowlist and detection rules:

- The extension allowlist lives in `packages/schema/src/textFiles.ts` (the `TEXT_FILE_EXTENSIONS` constant).
- Script files are still **scanned after upload**; PowerShell `.ps1`, `.psm1`, and `.psd1` files are accepted as text.
- Content types starting with `text/` are treated as text, plus a small allowlist (JSON / YAML / TOML / JS / TS / Markdown / SVG).

Server-side limits apply to the published bundle:

- **Total bundle size:** 50MB.
- **Embedding text** includes `SKILL.md` + up to **~40 non-`.md` files** (a best-effort cap).

## Slugs

Slugs and scopes identify the published package, and must match the publisher's claimed handle:

- The slug is **derived from the folder name by default**.
- Package **scopes** must match the ClawHub **publisher handle exactly**. Publisher handles can use lowercase letters, numbers, hyphens, dots, and underscores; they must **start and end with a lowercase letter or number**.
- Package **slugs must be lowercase and npm-safe**, for example `@example.tools/demo-plugin` or `demo-plugin`.

## Versioning + tags

Each publish is versioned, and tags are movable pointers to a version:

- Each publish creates a **new version** (semver).
- **Tags** are string pointers to a version; `latest` is commonly used.

## License

ClawHub fixes the license for every published skill; per-skill overrides are not allowed:

- All skills published on ClawHub are licensed under **`MIT-0`**.
- Anyone may use, modify, and redistribute published skills, **including commercially**.
- **Attribution is not required.**
- Do **not** add conflicting license terms in `SKILL.md`; ClawHub does **not support per-skill license overrides**.

## Paid skills

ClawHub does not monetize skills, and pricing metadata in the folder is inert:

- ClawHub does **not** support paid skills, per-skill pricing, paywalls, or revenue sharing.
- Do **not** add pricing metadata to `SKILL.md`; it is not part of the skill format and **will not make a published skill paid**.
- If your skill integrates with a paid third-party service, **document the external cost and required account clearly** in the skill instructions and env declarations — `requires.env` for required variables, or `envVars` with `required: false` for optional variables.

**Source**: OpenClaw documentation — `clawhub/skill-format` (mirror `inbox/openclaw_docs/clawhub/skill-format.md`)
**Last Updated**: 2026-06-22
**Status**: Active
