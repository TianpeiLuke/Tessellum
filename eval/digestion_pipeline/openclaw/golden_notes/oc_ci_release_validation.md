---
tags:
  - resource
  - documentation
  - openclaw
  - ci
  - release_validation
keywords:
  - openclaw release validation
  - full release validation umbrella
  - package acceptance docker e2e
  - gh workflow run release
  - openclaw release publish
  - live and e2e shards
  - install smoke plugin prerelease qa lab
  - openclaw performance benchmark
topics:
  - OpenClaw
  - CI Release Validation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/ci
access_control_group: ["general"]
---

# OpenClaw — CI Release Validation (Full Release Validation, Package Acceptance, and Release Workflows)

## Overview

This note is the **procedure** for running an OpenClaw release-validation pass and the release-only CI workflows that hang off it, mirroring the second half of the `ci` source page. It covers the `OpenClaw Performance` benchmark workflow, the `Full Release Validation` umbrella plus the mutating `OpenClaw Release Publish`, the live/E2E shards, `Package Acceptance` (its jobs, candidate sources, suite profiles, legacy-compatibility windows, and `gh workflow run` examples), `Install Smoke`, `Plugin Prerelease`, and `QA Lab`. These lanes are dispatched manually or on a schedule (not on every PR), and the page's verbatim `gh workflow run` invocations are reproduced as the canonical recipes.

## OpenClaw Performance

`OpenClaw Performance` is the product/runtime performance workflow. It runs daily on `main` and can be dispatched manually:

```bash
gh workflow run openclaw-performance.yml --ref main -f profile=diagnostic -f repeat=3
gh workflow run openclaw-performance.yml --ref main -f profile=smoke -f repeat=1 -f deep_profile=true -f live_openai_candidate=true
gh workflow run openclaw-performance.yml --ref main -f target_ref=v2026.5.2 -f profile=diagnostic -f repeat=3
```

Manual dispatch normally benchmarks the workflow ref; set `target_ref` to benchmark a release tag or another branch with the current workflow implementation. Published report paths and latest pointers are keyed by the tested ref, and each `index.md` records the tested ref/SHA, workflow ref/SHA, Kova ref, profile, lane auth mode, model, repeat count, and scenario filters. The workflow installs OCM from a pinned release and Kova from `openclaw/Kova` at the pinned `kova_ref` input, then runs three lanes: `mock-provider` (Kova diagnostic scenarios against a local-build runtime with deterministic fake OpenAI-compatible auth), `mock-deep-profile` (CPU/heap/trace profiling for startup, gateway, and agent-turn hotspots), and `live-openai-candidate` (a real OpenAI `openai/gpt-5.5` agent turn, skipped when `OPENAI_API_KEY` is unavailable). The `mock-provider` lane also runs OpenClaw-native source probes after the Kova pass (gateway boot timing/memory across default, hook, and 50-plugin startup cases; bundled-plugin import RSS; mock-OpenAI `channel-chat-baseline` hello loops; CLI startup commands; SQLite state smoke), comparing current RSS/heap against the previous published baseline and marking large RSS increases as `watch`. Every lane uploads GitHub artifacts; when `CLAWGRIT_REPORTS_TOKEN` is configured the workflow also commits `report.json`, `report.md`, bundles, `index.md`, and source-probe artifacts into `openclaw/clawgrit-reports` under `openclaw-performance/<tested-ref>/<run-id>-<attempt>/<lane>/`, writing the current pointer as `openclaw-performance/<tested-ref>/latest-<lane>.json`.

## Full Release Validation and OpenClaw Release Publish

`Full Release Validation` is the manual umbrella workflow for "run everything before release." It accepts a branch, tag, or full commit SHA, dispatches the manual `CI` workflow with that target, dispatches `Plugin Prerelease` for release-only plugin/package/static/Docker proof, and dispatches `OpenClaw Release Checks` for install smoke, package acceptance, cross-OS package checks, QA Lab parity, Matrix, and Telegram lanes. Stable and full profiles always include exhaustive live/E2E and Docker release-path soak coverage; the beta profile can opt in with `run_release_soak=true`. The canonical package Telegram E2E runs inside Package Acceptance, so a full candidate does not start a duplicate live poller. After publishing, pass `release_package_spec` to reuse the shipped npm package across release checks, Package Acceptance, Docker, cross-OS, and Telegram without rebuilding; use `npm_telegram_package_spec` only for a focused published-package Telegram rerun. `release_profile` controls live/provider breadth: `minimum` keeps the fastest OpenAI/core release-critical lanes, `stable` adds the stable provider/backend set, and `full` runs the broad advisory provider/media matrix (the manual release workflows default to `stable`).

`OpenClaw Release Publish` is the manual mutating release workflow. Dispatch it from `release/YYYY.M.PATCH` or `main` after the release tag exists and after the OpenClaw npm preflight has succeeded. It verifies `pnpm plugins:sync:check`, dispatches `Plugin NPM Release` for all publishable plugin packages, dispatches `Plugin ClawHub Release` for the same release SHA, and only then dispatches `OpenClaw NPM Release` with the saved `preflight_run_id`. Stable publish also requires an exact `windows_node_tag`; the workflow verifies the Windows source release and compares its x64/ARM64 installers with the candidate-approved `windows_node_installer_digests` input before any publish child, then promotes and verifies those pinned installer digests plus the exact companion asset/checksum contract before publishing the GitHub release draft.

```bash
gh workflow run openclaw-release-publish.yml \
  --ref release/YYYY.M.PATCH \
  -f tag=vYYYY.M.PATCH-beta.N \
  -f preflight_run_id=<successful-openclaw-npm-preflight-run-id> \
  -f full_release_validation_run_id=<successful-full-release-validation-run-id> \
  -f npm_dist_tag=beta
```

GitHub workflow-dispatch refs must be branches or tags, not raw commit SHAs. For pinned-commit proof on a fast-moving branch, use the helper `pnpm ci:full-release --sha <full-sha>` instead of `gh workflow run ... --ref main -f ref=<sha>`: it pushes a temporary `release-ci/<sha>-...` branch at the target SHA, dispatches `Full Release Validation` from that pinned ref, verifies every child workflow `headSha` matches the target, and deletes the branch when done (the umbrella verifier also fails if any child ran at a different SHA). For recovery, both `Full Release Validation` and `OpenClaw Release Checks` accept `rerun_group`: `all` for a candidate, `ci` for the normal full CI child, `plugin-prerelease`, `release-checks`, or a narrower group (`install-smoke`, `cross-os`, `live-e2e`, `package`, `qa`, `qa-parity`, `qa-live`, `npm-telegram`). For one failed cross-OS lane, combine `rerun_group=cross-os` with `cross_os_suite_filter` such as `windows/packaged-upgrade`. `OpenClaw Release Checks` resolves the selected ref once into a `release-package-under-test` tarball and passes that artifact to cross-OS checks and Package Acceptance so package bytes stay consistent across release boxes.

## Live and E2E shards

The release live/E2E child keeps broad native `pnpm test:live` coverage, but runs it as named shards through `scripts/test-live-shard.mjs` instead of one serial job: `native-live-src-agents`, `native-live-src-gateway-core`, provider-filtered `native-live-src-gateway-profiles`, `native-live-src-gateway-backends`, `native-live-test`, `native-live-extensions-a-k`, `native-live-extensions-l-n`, `native-live-extensions-openai`, `native-live-extensions-o-z-other`, `native-live-extensions-xai`, plus split media audio/video and provider-filtered music shards. The aggregate shard names `native-live-extensions-o-z`, `native-live-extensions-media`, and `native-live-extensions-media-music` remain valid for manual one-shot reruns. Native live media shards run in `ghcr.io/openclaw/openclaw-live-media-runner:ubuntu-24.04` (preinstalls `ffmpeg`/`ffprobe`). Docker-backed live model/backend shards use a separate shared `ghcr.io/openclaw/openclaw-live-test:<sha>` image per commit, built and pushed once, after which the Docker live model, provider-sharded gateway, CLI backend, ACP bind, and Codex harness shards run with `OPENCLAW_SKIP_DOCKER_BUILD=1`; gateway Docker shards carry explicit script-level `timeout` caps below the workflow job timeout so a stuck container fails fast.

## Package Acceptance

Use `Package Acceptance` when the question is "does this installable OpenClaw package work as a product?" Normal CI validates the source tree; package acceptance validates a single tarball through the same Docker E2E harness users exercise after install or update.

### Jobs

1. `resolve_package` checks out `workflow_ref`, resolves one package candidate, writes `.artifacts/docker-e2e-package/openclaw-current.tgz` and `.artifacts/docker-e2e-package/package-candidate.json`, uploads both as the `package-under-test` artifact, and prints the source, workflow ref, package ref, version, SHA-256, and profile in the step summary.
2. `docker_acceptance` calls `openclaw-live-and-e2e-checks-reusable.yml` with `ref=workflow_ref` and `package_artifact_name=package-under-test`; the reusable workflow downloads the artifact, validates the tarball inventory, prepares package-digest Docker images when needed, and runs the selected Docker lanes against that package (fanning multiple `docker_lanes` out as parallel targeted jobs).
3. `package_telegram` optionally calls `NPM Telegram Beta E2E`, running when `telegram_mode` is not `none`.
4. `summary` fails the workflow if package resolution, Docker acceptance, or the optional Telegram lane failed.

### Candidate sources

- `source=npm` accepts only `openclaw@beta`, `openclaw@latest`, or an exact release version such as `openclaw@2026.4.27-beta.2`.
- `source=ref` packs a trusted `package_ref` branch/tag/SHA via `scripts/package-openclaw-for-docker.mjs` after verifying the commit is reachable.
- `source=url` downloads a public HTTPS `.tgz` (`package_sha256` required; rejects URL credentials, non-default HTTPS ports, private/internal hostnames or IPs, and outside-policy redirects).
- `source=trusted-url` downloads from a named policy in `.github/package-trusted-sources.json` (`package_sha256` and `trusted_source_id` required; bearer auth uses the fixed `OPENCLAW_TRUSTED_PACKAGE_TOKEN` secret).
- `source=artifact` downloads one `.tgz` from `artifact_run_id`/`artifact_name` (`package_sha256` optional but recommended).

Keep `workflow_ref` (trusted harness code) and `package_ref` (the packed source commit for `source=ref`) separate so the current harness can validate older trusted source commits.

### Suite profiles

- `smoke` — `npm-onboard-channel-agent`, `gateway-network`, `config-reload`
- `package` — `npm-onboard-channel-agent`, `doctor-switch`, `update-channel-switch`, `skill-install`, `update-corrupt-plugin`, `upgrade-survivor`, `published-upgrade-survivor`, `update-restart-auth`, `plugins-offline`, `plugin-update`
- `product` — `package` plus `mcp-channels`, `cron-mcp-cleanup`, `openai-web-search-minimal`, `openwebui`
- `full` — full Docker release-path chunks with OpenWebUI
- `custom` — exact `docker_lanes`; required when `suite_profile=custom`

The `package` profile uses offline plugin coverage so published-package validation is not gated on live ClawHub availability. Release checks call Package Acceptance with `source=artifact`, the prepared release-package artifact, `suite_profile=custom`, an explicit `docker_lanes` list, and `telegram_mode=mock-openai`. The `published-upgrade-survivor` lane validates one published baseline per run (`published_upgrade_survivor_baseline` defaults to `openclaw@latest`); `run_release_soak=true` or `release_profile=full` expands `published_upgrade_survivor_baselines='last-stable-4 2026.4.23 2026.5.2 2026.4.15'` with `published_upgrade_survivor_scenarios=reported-issues`.

### Legacy compatibility windows

Packages through `2026.4.25` (including `2026.4.25-beta.*`) may use the compatibility path: known private QA entries in `dist/postinstall-inventory.json` may point at tarball-omitted files; `doctor-switch` may skip the `gateway install --wrapper` persistence subcase; `update-channel-switch` may prune missing pnpm `patchedDependencies` and log missing persisted `update.channel`; plugin smokes may read legacy install-record locations; and `plugin-update` may allow config metadata migration while keeping the install record and no-reinstall behavior unchanged. The published `2026.4.26` package may also warn for already-shipped local build metadata stamp files. Later packages must satisfy the modern contracts; the same conditions fail instead of warn or skip.

### Examples

```bash
# Validate the current beta package with product-level coverage.
gh workflow run package-acceptance.yml \
  --ref main -f workflow_ref=main -f source=npm \
  -f package_spec=openclaw@beta -f suite_profile=product -f telegram_mode=mock-openai

# Validate a tarball URL. SHA-256 is mandatory for source=url.
gh workflow run package-acceptance.yml \
  --ref main -f workflow_ref=main -f source=url \
  -f package_url=https://example.com/openclaw-current.tgz \
  -f package_sha256=<64-char-sha256> -f suite_profile=smoke
```

When debugging a failed run, start at the `resolve_package` summary to confirm source/version/SHA-256, then inspect the `docker_acceptance` child run and its Docker artifacts (`.artifacts/docker-tests/**/summary.json`, `failures.json`, lane logs, phase timings, rerun commands). Prefer rerunning the failed package profile or exact Docker lanes over rerunning full release validation.

## Install smoke

The separate `Install Smoke` workflow reuses the same scope script through its own `preflight` job and splits coverage into `run_fast_install_smoke` and `run_full_install_smoke`. The **fast path** runs for PRs touching Docker/package surfaces, bundled-plugin package/manifest changes, or core plugin/channel/gateway/Plugin SDK surfaces: it builds the root Dockerfile image once, checks the CLI, runs the agents delete shared-workspace CLI smoke and the container `gateway-network` e2e, verifies a bundled-extension build arg, and runs the bounded bundled-plugin Docker profile under a 240-second aggregate timeout. The **full path** keeps QR package install and installer Docker/update coverage for nightly scheduled runs, manual dispatches, workflow-call release checks, and PRs that truly touch installer/package/Docker surfaces. `main` pushes (including merge commits) do not force the full path. The slow Bun global-install image-provider smoke is separately gated by `run_bun_global_install_smoke` (nightly + release checks; PRs and `main` pushes do not run it).

## Plugin Prerelease

`Plugin Prerelease` is more expensive product/package coverage, so it is a separate workflow dispatched by `Full Release Validation` or by an explicit operator; normal PRs, `main` pushes, and standalone manual CI dispatches keep that suite off. It balances bundled-plugin tests across eight extension workers, each running up to two plugin config groups at a time with one Vitest worker per group and a larger Node heap. The release-only Docker prerelease path batches targeted Docker lanes in small groups to avoid reserving dozens of runners for one-to-three-minute jobs. The workflow also uploads an informational `plugin-inspector-advisory` artifact from `@openclaw/plugin-inspector`; inspector findings are triage input and do not change the blocking gate.

## QA Lab

QA Lab has dedicated CI lanes outside the main smart-scoped workflow; agentic parity is nested under the broad QA and release harnesses, not a standalone PR workflow (use `Full Release Validation` with `rerun_group=qa-parity` to ride parity with a broad validation run). The `QA-Lab - All Lanes` workflow runs nightly on `main` and on manual dispatch, fanning out the mock parity lane, live Matrix lane, and live Telegram and Discord lanes as parallel jobs (live jobs use the `qa-live-shared` environment; Telegram/Discord use Convex leases). Release checks run Matrix and Telegram live transport lanes with the deterministic mock provider and mock-qualified models (`mock-openai/gpt-5.5` and `mock-openai/gpt-5.5-alt`) so the channel contract is isolated from live model latency; the live transport gateway disables memory search because QA parity covers memory separately. Matrix uses `--profile fast` for scheduled and release gates (adding `--fail-fast` when the CLI supports it); manual `matrix_profile=all` always shards full Matrix coverage into `transport`, `media`, `e2ee-smoke`, `e2ee-deep`, and `e2ee-cli` jobs. `OpenClaw Release Checks` also runs the release-critical QA Lab lanes before approval: its QA parity gate runs candidate and baseline packs as parallel lane jobs, then compares both artifacts in a small report job.

**Source**: OpenClaw documentation — `ci` (mirror `inbox/openclaw_docs/ci.md`), release-validation sections
**Last Updated**: 2026-06-22
**Status**: Active
