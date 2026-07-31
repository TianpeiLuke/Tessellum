---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - publishing
keywords:
  - clawhub publishing
  - clawhub skill publish
  - clawhub package publish
  - npm scoped package owner
  - skill-publish.yml workflow
  - trusted publishing github oidc
  - clawhub package trusted-publisher
  - package scope must match owner
  - clawhub package transfer
  - clawhub_token publish
topics:
  - OpenClaw
  - ClawHub Publishing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/publishing
access_control_group: ["general"]
---

# OpenClaw — Publishing Skills and Plugins to ClawHub

## Overview

This note is the step-by-step procedure for publishing to **ClawHub**, OpenClaw's registry for skills and plugins, mirroring the `clawhub/publishing` source page. Publishing sends a skill folder or a plugin package to ClawHub under an owner you choose; ClawHub checks that your token can publish for that owner, validates the metadata, name, version, files, and source information, then stores the release and starts automated security checks. If validation fails, nothing is published, and new releases may also stay out of normal install and download surfaces until review finishes. The note covers the skill-folder publish path (CLI plus the reusable `skill-publish.yml` GitHub workflow), npm-scoped plugin packages with the scope-must-match-owner rule, the pre-publish checklist for plugins, GitHub-OIDC trusted publishing setup and rollback for packages, and the FAQ for resolving scope/owner mismatches via republish or ownership transfer.

## Skills

The simplest publishing path is the CLI. Sign in, then publish a local skill folder:

```bash
clawhub login
clawhub skill publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --owner <owner>
```

Use `--owner <handle>` when publishing to an org owner; omit it to publish as the authenticated user. Publishing skips unchanged content. A new skill starts at `1.0.0`, and later changes automatically publish the next patch version. Pass `--version` only when you need an explicit version.

For catalog repos, use ClawHub's reusable `skill-publish.yml` workflow (hosted at `openclaw/clawhub/.github/workflows/skill-publish.yml`). It calls `skill publish` for each immediate skill folder under `root` (default: `skills`), or only the folder supplied as `skill_path`:

```yaml
jobs:
  publish:
    uses: openclaw/clawhub/.github/workflows/skill-publish.yml@main
    with:
      owner: <owner>
      dry_run: false
    secrets:
      clawhub_token: ${{ secrets.CLAWHUB_TOKEN }}
```

Use `dry_run: true` to preview new and changed skills without publishing.

## Plugins

Plugins use npm-style package names. Scoped package names include the owner in the first part of the name:

```text
@owner/package-name
```

The scope must match the selected publish owner. If your package is named `@openclaw/dronzer`, it can only be published as `@openclaw`; if you publish as `@vintageayu`, rename the package to `@vintageayu/dronzer`. This prevents a package from claiming an org namespace that the publisher does not control.

If you are the rightful owner of an org, brand, package scope, owner handle, or namespace that is already claimed or reserved on ClawHub, open an Org / Namespace Claim issue (GitHub issue template `org-namespace-claim.yml`) with public, non-sensitive proof. See [oc_clawhub_namespace_claims](oc_clawhub_namespace_claims.md) for what to include and what to keep out of public issues.

### Before Publishing a Plugin

Complete this checklist before a plugin publish:

- Pick an owner that matches the package scope.
- Include `openclaw.plugin.json`. Code plugins also need `package.json` with `openclaw.compat.pluginApi` and `openclaw.build.openclawVersion`.
- To show a custom plugin card icon, add `icon` to `openclaw.plugin.json` with any HTTPS image URL.
- Include source repository and exact commit metadata, or use the CLI from a GitHub-backed checkout so it can detect them.
- Run `clawhub package validate <source>` before publishing. For package, manifest, SDK import, or artifact findings, see [oc_clawhub_plugin_validation_fixes](oc_clawhub_plugin_validation_fixes.md).
- Run `clawhub package publish <source> --dry-run` before creating a release.
- Expect new releases to stay out of public install surfaces until automated security checks and verification finish.

### Trusted Publishing for Packages

Package trusted publishing is a two-step setup. First, publish the package once through normal manual or token-authenticated `clawhub package publish` — this creates the package row and establishes the package managers who can change its trusted publisher config. Second, a package manager sets the GitHub Actions trusted publisher config:

```bash
clawhub package trusted-publisher set @owner/package-name \
  --repository owner/repo \
  --workflow-filename package-publish.yml
```

After config is set, future supported GitHub Actions publishes can use OIDC/trusted publishing without storing a long-lived ClawHub token in the repository. The configured repository and workflow filename must match the GitHub Actions OIDC claim. If you also pass `--environment <name>`, the GitHub Actions environment claim must match that name exactly. Inspect or remove the config with `clawhub package trusted-publisher get @owner/package-name` and `clawhub package trusted-publisher delete @owner/package-name`.

ClawHub verifies the configured GitHub repository when trusted publisher config is set. Public repositories can be verified through public GitHub metadata. Private repositories require ClawHub to have GitHub access to that repository, for example through a future ClawHub GitHub App installation or another authorized GitHub integration.

The current reusable package publish workflow supports secretless trusted publishing for `workflow_dispatch` publishes when `id-token: write` is available. Tag-push real publishes still need `clawhub_token`, so keep `CLAWHUB_TOKEN` available for tag releases, first publishes, untrusted packages, or break-glass publishes. Deleting trusted publisher config is the rollback path: it disables future trusted publish token minting until a package manager sets config again.

## FAQ

### Package scope must match selected owner

If the package scope and selected owner do not match, ClawHub rejects the publish:

```text
Package scope "@openclaw" must match selected owner "@vintageayu".
Publish as "@openclaw" or rename this package to "@vintageayu/dronzer".
```

To fix it, either choose the owner named by the package scope, or rename the package so the scope matches the owner you can publish as. If the package name already has the right scope but the package is owned by the wrong publisher, transfer ownership instead:

```sh
clawhub package transfer @opik/opik-openclaw --to opik
```

Use package or skill transfer only when you have admin access to both the current owner and the destination publisher. Package transfer does not let you publish into a scope you cannot manage. If you do not have access to the current owner but believe your org, project, or brand is the rightful namespace owner, open an Org / Namespace Claim issue (GitHub template `org-namespace-claim.yml`) with public, non-sensitive proof for staff review; see [oc_clawhub_namespace_claims](oc_clawhub_namespace_claims.md) before filing. This protects org namespaces: a package named `@openclaw/dronzer` claims the `@openclaw` namespace, so only publishers with access to the `@openclaw` owner can publish it.

**Source**: OpenClaw documentation — `clawhub/publishing` (mirror `inbox/openclaw_docs/clawhub/publishing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
