---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - troubleshooting
keywords:
  - clawhub publish fails
  - clawhub sync no skills found
  - clawhub update force local changes
  - publish required metadata missing
  - github owner source error
  - namespace claimed or reserved
  - openclaw.compat.pluginapi
  - clawhub package publish dry-run
topics:
  - OpenClaw
  - ClawHub Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — ClawHub Troubleshooting: Publish, Sync, and Update Failures

## Overview

This note is the procedural half of the ClawHub `troubleshooting` page covering **publish, sync, and update** failures — the recipes a publisher runs when `clawhub package publish`, `clawhub sync`, or `clawhub update` does not behave as expected. It diagnoses five failure clusters in source order: a publish blocked because required metadata is missing, a publish rejected with a GitHub owner or source error, a publish refused because a namespace is claimed or reserved, `sync` reporting that no skills were found, and `update` refusing to proceed because of local changes. The sibling note [oc_clawhub_troubleshooting_auth_install](oc_clawhub_troubleshooting_auth_install.md) covers the sign-in, install, and public-API access half of the same page; this note covers only the publish/sync/update recipes assigned to it by the cw03 Section Coverage Map.

## Publish fails because required metadata is missing

A publish is blocked when the package does not declare the metadata that ClawHub (and its scanners) need to understand it. The fix differs by package family:

- **For skills**, check the `SKILL.md` frontmatter. Required environment variables and tools should be declared so users and scanners can understand the package. (The frontmatter / `metadata.openclaw` field reference is documented in [oc_clawhub_skill_frontmatter](oc_clawhub_skill_frontmatter.md).)
- **For plugins**, check the `package.json` compatibility metadata. Code-plugin publishes need OpenClaw compatibility fields such as `openclaw.compat.pluginApi` and `openclaw.build.openclawVersion`.

Before publishing, preview the publish payload first to confirm what will be sent:

```bash
clawhub package publish <source> --family code-plugin --dry-run
```

## Publish fails with a GitHub owner or source error

ClawHub uses GitHub identity and source attribution to connect packages to their publishers. When a publish is rejected with an owner or source error, work through these checks:

- Make sure you are signed in with the GitHub account that owns or can publish the package.
- Check that the source URL is public or accessible to ClawHub.
- For GitHub sources, use `owner/repo`, `owner/repo@ref`, or a full GitHub URL.

## Publish fails because a namespace is claimed or reserved

If a publish fails because the owner handle, org namespace, package scope, skill slug, or package name is already claimed or reserved, first confirm that you are publishing with the owner that matches the namespace. For plugin packages, scoped names such as `@example-org/example-plugin` must be published as the matching `example-org` owner.

If you believe your org, project, or brand is the rightful namespace owner but you cannot manage the current ClawHub owner, open an Org / Namespace Claim issue with public, non-sensitive proof. The source links the issue template at `https://github.com/openclaw/clawhub/issues/new?template=org-namespace-claim.yml`, and points to the Org and Namespace Claims page at `/clawhub/namespace-claims` (owned by cw02) for evidence guidance and what to keep out of public issues.

## `sync` says no skills were found

`sync` looks for folders containing `SKILL.md` or `skill.md`. If it reports that no skills were found, the roots it scanned do not contain such a folder. Point it at the roots you want to scan:

```bash
clawhub sync --root /path/to/skills
```

If you are unsure what will publish, preview first:

```bash
clawhub sync --all --dry-run --no-input
```

## `update` refuses because of local changes

`update` refuses when the local files do not match any version ClawHub knows about. The source gives three choices:

- Keep local edits and skip the update.
- Overwrite with the published version:

```bash
clawhub update @openclaw/demo --force
```

- Publish your edited copy as a new slug or fork.

**Source**: OpenClaw documentation — `clawhub/troubleshooting` (mirror `inbox/openclaw_docs/clawhub/troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
