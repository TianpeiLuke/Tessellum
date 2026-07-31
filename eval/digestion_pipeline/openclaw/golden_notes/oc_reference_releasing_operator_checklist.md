---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - release
keywords:
  - openclaw release operator checklist
  - openclaw release publish
  - pnpm release prep release candidate
  - openclaw npm release preflight
  - stable main closeout
  - npm dist-tag beta latest
  - windows node installer digests
  - release publish automation order
topics:
  - OpenClaw
  - Release Operations
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/RELEASING
access_control_group: ["general"]
---

# OpenClaw — Release Operator Checklist and Publish Automation

## Overview

This note is the procedure for executing an OpenClaw release in its public shape: the 11-step **release operator checklist**, the **Release publish automation** (`OpenClaw Release Publish`) order, the **NPM workflow inputs**, the **Stable npm release sequence**, and the **Stable main closeout** evidence requirements — mirroring the operator-facing sections of `reference/RELEASING`. The version-naming / lane / cadence **policy** behind these steps is in [oc_reference_releasing_policy](oc_reference_releasing_policy.md); the pre-release validation boxes (preflight, `Full Release Validation`, Vitest/Docker/QA Lab/Package) that steps 6–7 invoke are in [oc_reference_releasing_validation](oc_reference_releasing_validation.md). Private credentials, signing, notarization, dist-tag recovery, and emergency rollback stay in the maintainer-only runbook.

## Release Operator Checklist (public shape)

The checklist is the public shape of the release flow; the eleven steps run in order:

1. **Start from current `main`**: pull latest, confirm the target commit is pushed, and confirm `main` CI is green enough to branch from it.
2. **Generate the top `CHANGELOG.md` section** from merged PRs and all direct commits since the last reachable release tag. Keep entries user-facing, dedupe overlapping PR/direct-commit entries, commit the rewrite, push, and rebase/pull once more before branching.
3. **Review release compatibility records** in `src/plugins/compat/registry.ts` and `src/commands/doctor/shared/deprecation-compat.ts`. Remove expired compatibility only when the upgrade path stays covered, or record why it is kept.
4. **Create `release/YYYY.M.PATCH` from current `main`**; do not do release work directly on `main`.
5. **Bump every required version location** for the intended tag, then run `pnpm release:prep` (it refreshes plugin versions, plugin inventory, config schema, bundled channel config metadata, config docs baseline, plugin SDK exports, and plugin SDK API baseline in order). Commit any generated drift before tagging, then run the local deterministic preflight: `pnpm check:test-types`, `pnpm check:architecture`, `pnpm build && pnpm ui:build`, and `pnpm release:check`.
6. **Run `OpenClaw NPM Release` with `preflight_only=true`.** Before a tag exists, a full 40-character release-branch SHA is allowed for validation-only preflight. The preflight generates dependency release evidence for the exact checked-out dependency graph and stores it in the npm preflight artifact. **Save the successful `preflight_run_id`.**
7. **Kick off all pre-release tests with `Full Release Validation`** for the release branch, tag, or full commit SHA — the one manual entrypoint for the four release test boxes (Vitest, Docker, QA Lab, Package; see [oc_reference_releasing_validation](oc_reference_releasing_validation.md)).
8. **If validation fails**, fix on the release branch and rerun the smallest failed file, lane, workflow job, package profile, provider, or model allowlist that proves the fix; rerun the full umbrella only when the changed surface makes prior evidence stale.
9. **For a tagged beta candidate**, run `pnpm release:candidate -- --tag vYYYY.M.PATCH-beta.N` from the matching `release/YYYY.M.PATCH` branch (for stable, also pass `--windows-node-tag vX.Y.Z`). The helper runs the local generated-release checks, dispatches/verifies the full release validation and npm preflight evidence, runs Parallels fresh/update proof against the exact prepared tarball plus Telegram package proof, records plugin npm and ClawHub plans, and prints the exact `OpenClaw Release Publish` command only once the evidence bundle is green. Then run post-publish package acceptance against the published `openclaw@YYYY.M.PATCH-beta.N` or `openclaw@beta` package. If a pushed/published prerelease needs a fix, cut the next matching prerelease number; do not delete or rewrite the old one.
10. **For stable**, continue only after the vetted beta or release candidate has the required validation evidence. Stable npm publish also goes through `OpenClaw Release Publish`, reusing the successful preflight artifact via `preflight_run_id`. Stable macOS readiness requires the packaged `.zip`, `.dmg`, `.dSYM.zip`, and updated `appcast.xml` on `main` (the macOS publish workflow commits the signed appcast to public `main` automatically after assets verify, or opens an appcast PR when push is blocked). Stable Windows Hub readiness requires the signed `OpenClawCompanion-Setup-x64.exe`, `OpenClawCompanion-Setup-arm64.exe`, and `OpenClawCompanion-SHA256SUMS.txt` assets on the GitHub release; pass the exact signed `openclaw/openclaw-windows-node` tag as `windows_node_tag` and its candidate-approved installer digest map as `windows_node_installer_digests`.
11. **After publish**, run the npm post-publish verifier, optional standalone published-npm Telegram E2E for channel proof, dist-tag promotion when needed, verify the generated GitHub release page, run the release announcement steps, then complete the Stable main closeout before calling a stable release finished.

## Release Publish Automation

`OpenClaw Release Publish` is the normal **mutating** publish entrypoint, dispatched after the tag exists from `release/YYYY.M.PATCH` (or `main` for a main-reachable tag), passing the release tag, the successful OpenClaw npm `preflight_run_id`, and the `full_release_validation_run_id`. It orchestrates the trusted-publisher workflows in order:

1. Check out the release tag and resolve its commit SHA.
2. Verify the tag is reachable from `main` or `release/*`.
3. Run `pnpm plugins:sync:check`.
4. Dispatch `Plugin NPM Release` with `publish_scope=all-publishable` and `ref=<release-sha>`.
5. Dispatch `Plugin ClawHub Release` with the same scope and SHA.
6. Dispatch `OpenClaw NPM Release` with the release tag, npm dist-tag, and saved `preflight_run_id` after verifying the saved `full_release_validation_run_id`.
7. For stable releases, create/update the GitHub release as a draft, dispatch `Windows Node Release` with the explicit `windows_node_tag` and candidate-approved `windows_node_installer_digests`, and verify the canonical installer/checksum assets before publishing the draft.

The workflow **serializes** plugin npm publish, plugin ClawHub publish, and OpenClaw npm publish so the core package is not published before its externalized plugins. Once plugin npm publish succeeds it promotes the prepared OpenClaw npm preflight artifact with the matching dist-tag; after the OpenClaw npm publish child succeeds it creates/updates the matching GitHub release page from the complete `CHANGELOG.md` section, uploads the preflight dependency evidence, full-validation manifest, and postpublish registry-verification evidence, auto-approves release-environment gates the workflow token may approve, waits for ClawHub when OpenClaw npm is publishing, then runs `pnpm release:verify-beta` and uploads postpublish evidence. Stable releases on npm `latest` become the GitHub latest release; stable maintenance releases kept on `beta` are created with GitHub `latest=false`.

The beta publish, the stable publish to the default `beta` dist-tag, and the explicit stable promotion directly to `latest` are reproduced verbatim:

```bash
# Beta publish
gh workflow run openclaw-release-publish.yml \
  --ref release/YYYY.M.PATCH \
  -f tag=vYYYY.M.PATCH-beta.N \
  -f preflight_run_id=<successful-openclaw-npm-preflight-run-id> \
  -f full_release_validation_run_id=<successful-full-release-validation-run-id> \
  -f npm_dist_tag=beta
```

```bash
# Stable publish to the default beta dist-tag
gh workflow run openclaw-release-publish.yml \
  --ref release/YYYY.M.PATCH \
  -f tag=vYYYY.M.PATCH \
  -f windows_node_tag=vX.Y.Z \
  -f windows_node_installer_digests='{"OpenClawCompanion-Setup-x64.exe":"sha256:<approved-x64-sha256>","OpenClawCompanion-Setup-arm64.exe":"sha256:<approved-arm64-sha256>"}' \
  -f preflight_run_id=<successful-openclaw-npm-preflight-run-id> \
  -f full_release_validation_run_id=<successful-full-release-validation-run-id> \
  -f npm_dist_tag=beta
```

```bash
# Stable promotion directly to latest (explicit)
gh workflow run openclaw-release-publish.yml \
  --ref release/YYYY.M.PATCH \
  -f tag=vYYYY.M.PATCH \
  -f windows_node_tag=vX.Y.Z \
  -f windows_node_installer_digests='{"OpenClawCompanion-Setup-x64.exe":"sha256:<approved-x64-sha256>","OpenClawCompanion-Setup-arm64.exe":"sha256:<approved-arm64-sha256>"}' \
  -f preflight_run_id=<successful-openclaw-npm-preflight-run-id> \
  -f full_release_validation_run_id=<successful-full-release-validation-run-id> \
  -f npm_dist_tag=latest
```

`OpenClaw Release Publish` rejects `plugin_publish_scope=selected` when `publish_openclaw_npm=true` so the core package cannot ship without every publishable official plugin, including `@openclaw/diffs-language-pack`. For a selected plugin repair, set `publish_openclaw_npm=false` with `plugin_publish_scope=selected` and `plugins=@openclaw/name`, or dispatch the child workflow directly; use the lower-level `Plugin NPM Release`/`Plugin ClawHub Release` workflows only for focused repair.

## NPM Workflow Inputs

`OpenClaw NPM Release` accepts: `tag` (required tag such as `v2026.4.2`, `v2026.4.2-1`, or `v2026.4.2-beta.1`; when `preflight_only=true` it may also be the current full 40-character workflow-branch commit SHA for validation-only preflight); `preflight_only` (`true` for validation/build/package only, `false` for the real publish path); `preflight_run_id` (required on the real publish path so the workflow reuses the prepared tarball); and `npm_dist_tag` (defaults to `beta`).

`OpenClaw Release Publish` accepts: `tag` (must already exist); `preflight_run_id` (successful `OpenClaw NPM Release` preflight run id; required when `publish_openclaw_npm=true`); `full_release_validation_run_id` (required when `publish_openclaw_npm=true`); `windows_node_tag` (exact non-prerelease `openclaw/openclaw-windows-node` tag; required for stable); `windows_node_installer_digests` (candidate-approved compact JSON map of current Windows installer names to pinned `sha256:` digests; required for stable); `npm_dist_tag`; `plugin_publish_scope` (defaults `all-publishable`; use `selected` only for plugin-only repair with `publish_openclaw_npm=false`); `plugins` (comma-separated `@openclaw/*` names when scope is `selected`); `publish_openclaw_npm` (defaults `true`); and `wait_for_clawhub` (defaults `false` so npm availability is not blocked by the ClawHub sidecar; set `true` only when completion must include ClawHub).

`OpenClaw Release Checks` accepts `ref` (branch, tag, or full commit SHA; secret-bearing checks require the resolved commit reachable from an OpenClaw branch or release tag) and `run_release_soak` (opt into exhaustive live/E2E, Docker release-path, and all-since upgrade-survivor soak for beta checks; forced on by `release_profile=stable`/`full`).

The governing rules: stable and correction tags may publish to either `beta` or `latest`; beta prerelease tags may publish only to `beta`; for `OpenClaw NPM Release`, full commit SHA input is allowed only when `preflight_only=true`; `OpenClaw Release Checks` and `Full Release Validation` are always validation-only; and the real publish path must use the same `npm_dist_tag` used during preflight (verified before publish continues).

## Stable npm Release Sequence

When cutting a stable npm release:

1. Run `OpenClaw NPM Release` with `preflight_only=true` (before a tag exists, you may use the current full workflow-branch commit SHA for a validation-only run).
2. Choose `npm_dist_tag=beta` for the normal beta-first flow, or `latest` only for a direct stable publish.
3. Run `Full Release Validation` on the release branch/tag/SHA for normal CI plus live prompt cache, Docker, QA Lab, Matrix, and Telegram coverage from one manual workflow.
4. If you only need the deterministic normal test graph, run the manual `CI` workflow on the release ref.
5. Select the exact non-prerelease `openclaw/openclaw-windows-node` tag whose signed x64 and ARM64 installers should ship; save it as `windows_node_tag` and their validated digest map as `windows_node_installer_digests` (the release-candidate helper records both).
6. Save the successful `preflight_run_id` and `full_release_validation_run_id`.
7. Run `OpenClaw Release Publish` with the same `tag` and `npm_dist_tag`, the selected `windows_node_tag` and its digest map, and the saved run ids; it publishes externalized plugins to npm and ClawHub before promoting the OpenClaw npm package.
8. If the release landed on `beta`, use the `openclaw/releases/.github/workflows/openclaw-npm-dist-tags.yml` workflow to promote that version from `beta` to `latest`.
9. If it published directly to `latest` and `beta` should follow immediately, use that same workflow to point both dist-tags at the stable version, or let its scheduled self-healing sync move `beta` later.

The dist-tag mutation lives in the release ledger repo (`openclaw/releases`) because it still requires `NPM_TOKEN`, while the source repo keeps OIDC-only publish. If a maintainer must fall back to local npm authentication, run any 1Password CLI (`op`) commands only inside a dedicated tmux session — not from the main agent shell — so prompts, alerts, and OTP handling stay observable.

## Stable Main Closeout

Stable publication is not complete until `main` carries the actual shipped release state. The closeout is a six-step procedure: (1) start from fresh latest `main`, audit `release/YYYY.M.PATCH` against it and forward-port real fixes absent from `main` (do not blindly merge release-only compatibility/test/validation adapters into newer `main`); (2) set `main` to the shipped stable version (not a speculative next train), run `pnpm release:prep` after the root version change, then `pnpm deps:shrinkwrap:generate`; (3) make `CHANGELOG.md`'s `## YYYY.M.PATCH` section on `main` exactly match the tagged release branch, including the stable `appcast.xml` update when the mac release published one; (4) do not add a `+1`, beta, or empty future changelog section to `main` until the operator explicitly starts that train; (5) run `pnpm release:generated:check`, `pnpm deps:shrinkwrap:check`, and `OPENCLAW_TESTBOX=1 pnpm check:changed`, then push and verify `origin/main` carries the shipped version and changelog; (6) keep the repository variables `RELEASE_ROLLBACK_DRILL_ID` and `RELEASE_ROLLBACK_DRILL_DATE` current after each private rollback drill.

`OpenClaw Stable Main Closeout` starts from the `main` push carrying the shipped version, changelog, and appcast. It reads immutable postpublish evidence to bind the shipped tag to its Full Release Validation and Publish runs, verifies the stable main state, release, mandatory stable soak, and blocking performance evidence, and attaches an immutable closeout manifest and checksum to the GitHub release. The automatic push trigger skips legacy releases predating immutable postpublish evidence but never treats that skip as a completed closeout. A complete closeout requires both assets and a matching checksum: a partial manifest replays its recorded `main` SHA and rollback drill to regenerate identical bytes then attaches the missing checksum, while an invalid pair (or a checksum without a manifest) stays blocking. A missing or >90-day-old drill record blocks a new evidence-backed closeout; use manual dispatch only to repair or replay one. A legacy fallback correction tag may reuse base-package evidence only when it resolves to the same source commit as the base stable tag; a correction with a different source must publish and verify its own package evidence.

**Source**: OpenClaw documentation — `reference/RELEASING` (mirror `inbox/openclaw_docs/reference/RELEASING.md`)
**Last Updated**: 2026-06-22
**Status**: Active
