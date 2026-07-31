---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - release_validation
keywords:
  - openclaw full release validation
  - release-gate umbrella workflow
  - release_profile stable full
  - rerun_group focused rerun handles
  - docker release-path chunks
  - release_package_spec package acceptance
  - cross-os release checks
  - gh workflow run full-release-validation.yml
topics:
  - OpenClaw
  - Full Release Validation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/full-release-validation
access_control_group: ["general"]
---

# OpenClaw — Full Release Validation Release-Gate Workflow

## Overview

This note documents the OpenClaw **Full Release Validation** release-gate procedure: how an operator dispatches the release umbrella workflow, the top-level and release-check stages it fans out to, the Docker release-path chunks, the `minimum`/`stable`/`full` release profiles, the suites `full` adds over `stable`, the `rerun_group`/filter handles for focused reruns, the evidence artifacts to retain, and the backing `.github/workflows/*.yml` files. It mirrors the `reference/full-release-validation` source page. `Full Release Validation` is the release umbrella — the single manual entrypoint for pre-release proof — but most work happens in child workflows so a failed box can be rerun without restarting the whole release.

## Dispatch and Inputs

Run the umbrella from a trusted workflow ref, normally `main`, and pass the release branch, tag, or full commit SHA as `ref`:

```bash
gh workflow run full-release-validation.yml \
  --ref main \
  -f ref=release/YYYY.M.PATCH \
  -f provider=openai \
  -f mode=both \
  -f release_profile=stable
```

Child workflows use the trusted workflow ref for the harness and the input `ref` for the candidate under test, so new validation logic stays available when validating an older release branch or tag. `release_profile=stable` and `release_profile=full` always run the exhaustive live/Docker soak; pass `run_release_soak=true` to include the same soak lanes with the beta profile. Stable publication rejects a validation manifest without this soak and blocking product-performance evidence. Package Acceptance normally builds the candidate tarball from the resolved `ref`, including full-SHA runs dispatched with `pnpm ci:full-release`. After a beta publish, pass `release_package_spec=openclaw@YYYY.M.PATCH-beta.N` to reuse the shipped npm package across release checks, Package Acceptance, cross-OS, release-path Docker, and package Telegram; use `package_acceptance_package_spec` only when Package Acceptance should intentionally prove a different package. The Codex plugin live package lane follows the same state: published `release_package_spec` values derive `codex_plugin_spec=npm:@openclaw/codex@<version>`, SHA/artifact runs pack `extensions/codex` from the selected ref, and operators can set `codex_plugin_spec` directly for `npm:`, `npm-pack:`, or `git:` plugin sources — the lane grants the explicit Codex CLI install approval, then runs Codex CLI preflight and same-session OpenAI agent turns.

## Top-level Stages

The umbrella dispatches these top-level stages, each (where applicable) into a named child workflow with its own `rerun_group` handle:

- **Target resolution** — Job `Resolve target ref` (no child workflow); resolves the release branch, tag, or full commit SHA and records selected inputs; rerun the umbrella if this fails.
- **Vitest and normal CI** — Job `Run normal full CI`, child workflow `CI`; proves the manual full CI graph against the target ref (Linux Node lanes, bundled plugin shards, plugin and channel contract shards, Node 22 compatibility, `check-*`, `check-additional-*`, built-artifact smoke checks, docs checks, Python skills, Windows, macOS, Control UI i18n, and Android via the umbrella); rerun `rerun_group=ci`.
- **Plugin prerelease** — Job `Run plugin prerelease validation`, child workflow `Plugin Prerelease`; proves release-only plugin static checks, agentic plugin coverage, full extension batch shards, plugin prerelease Docker lanes, and a non-blocking `plugin-inspector-advisory` artifact for compatibility triage; rerun `rerun_group=plugin-prerelease`.
- **Release checks** — Job `Run release/live/Docker/QA validation`, child workflow `OpenClaw Release Checks`; proves install smoke, cross-OS package checks, Package Acceptance, QA Lab parity, live Matrix, and live Telegram (stable and full also run exhaustive live/E2E suites and Docker release-path chunks; beta can opt in with `run_release_soak=true`); rerun `rerun_group=release-checks` or a narrower release-checks handle.
- **Package Telegram** — Job `Run package Telegram E2E`, child workflow `NPM Telegram Beta E2E`; proves a focused published-package Telegram E2E when `release_package_spec` or `npm_telegram_package_spec` is set (full candidate validation uses the canonical Package Acceptance Telegram E2E instead); rerun `rerun_group=npm-telegram` with `release_package_spec` or `npm_telegram_package_spec`.
- **Umbrella verifier** — Job `Verify full validation` (no child workflow); re-checks recorded child run conclusions and appends slowest-job tables from child workflows; rerun only this job after rerunning a failed child to green.

For `ref=main` and `rerun_group=all`, a newer umbrella supersedes an older one. When the parent is cancelled, its monitor cancels any child workflow it already dispatched. Release branch and tag validation runs do not cancel each other by default.

## Release Checks Stages

`OpenClaw Release Checks` is the largest child workflow. It resolves the target once and prepares a shared `release-package-under-test` artifact when package or Docker-facing stages need it. Its stages (job · backing workflow · what it tests · rerun handle):

- **Release target** — `Resolve target ref`, no backing workflow; tests selected ref, optional expected SHA, profile, rerun group, and focused live suite filter; rerun `rerun_group=release-checks`.
- **Package artifact** — `Prepare release package artifact`, no backing workflow; packs or resolves one candidate tarball and uploads `release-package-under-test` for downstream package-facing checks; rerun the affected package, cross-OS, or live/E2E group.
- **Install smoke** — `Run install smoke`, backing workflow `Install Smoke`; tests the full install path with root Dockerfile smoke image reuse, QR package install, root and gateway Docker smokes, installer Docker tests, Bun global install image-provider smoke, and fast bundled-plugin install/uninstall E2E; rerun `rerun_group=install-smoke`.
- **Cross-OS** — `cross_os_release_checks`, backing workflow `OpenClaw Cross-OS Release Checks (Reusable)`; tests fresh and upgrade lanes on Linux, Windows, and macOS for the selected provider and mode using the candidate tarball plus a baseline package; rerun `rerun_group=cross-os`.
- **Repo and live E2E** — `Run repo/live E2E validation`, backing workflow `OpenClaw Live And E2E Checks (Reusable)`; tests repository E2E, live cache, OpenAI websocket streaming, native live provider and plugin shards, and Docker-backed live model/backend/gateway harnesses selected by `release_profile`; runs on `run_release_soak=true`, `release_profile=full`, or focused `rerun_group=live-e2e`; rerun `rerun_group=live-e2e` optionally with `live_suite_filter`.
- **Docker release path** — `Run Docker release-path validation`, backing workflow `OpenClaw Live And E2E Checks (Reusable)`; tests release-path Docker chunks against the shared package artifact; runs on `run_release_soak=true`, `release_profile=full`, or focused `rerun_group=live-e2e`; rerun `rerun_group=live-e2e`.
- **Package Acceptance** — `Run package acceptance`, backing workflow `Package Acceptance`; tests offline plugin package fixtures, plugin update, the canonical mock-OpenAI Telegram package E2E, and published-upgrade survivor checks against the same tarball (blocking release checks use the default latest published baseline; soak checks expand to every stable npm release at or after `2026.4.23` plus reported-issue fixtures); rerun `rerun_group=package`.
- **QA parity** — `Run QA Lab parity lane` and `Run QA Lab parity report`, direct jobs; tests candidate and baseline agentic parity packs, then the parity report; rerun `rerun_group=qa-parity` or `rerun_group=qa`.
- **QA live Matrix** — `Run QA Lab live Matrix lane`, direct job; tests the fast live Matrix QA profile in the `qa-live-shared` environment; rerun `rerun_group=qa-live` or `rerun_group=qa`.
- **QA live Telegram** — `Run QA Lab live Telegram lane`, direct job; tests live Telegram QA with Convex CI credential leases; rerun `rerun_group=qa-live` or `rerun_group=qa`.
- **Release verifier** — `Verify release checks`, no backing workflow; tests required release-check jobs for the selected rerun group; rerun after focused child jobs pass.

## Docker Release-Path Chunks

The Docker release-path stage runs these chunks when `live_suite_filter` is empty: `core` (core Docker release-path smoke lanes); `package-update-openai` (OpenAI package install/update behavior, Codex on-demand install, Codex plugin live turns, and Chat Completions tool calls); `package-update-anthropic` (Anthropic package install and update behavior); `package-update-core` (provider-neutral package and update behavior); `plugins-runtime-plugins` (plugin runtime lanes that exercise plugin behavior); `plugins-runtime-services` (service-backed and live plugin runtime lanes, including OpenWebUI when requested); and `plugins-runtime-install-a` through `plugins-runtime-install-h` (plugin install/runtime batches split for parallel release validation). Use targeted `docker_lanes=<lane[,lane]>` on the reusable live/E2E workflow when only one Docker lane failed; the release artifacts include per-lane rerun commands with package artifact and image reuse inputs when available.

## Release Profiles

`release_profile` mostly controls live/provider breadth inside release checks; it does not remove normal full CI, Plugin Prerelease, install smoke, package acceptance, or QA Lab. Stable and full profiles always run exhaustive repo/live E2E and Docker release-path soak coverage, and the beta profile can opt in with `run_release_soak=true`. Package Acceptance supplies the canonical package Telegram E2E for every full candidate, so the umbrella does not duplicate that live poller. The three profiles:

- **`minimum`** — fastest release-critical smoke; includes the OpenAI/core live path, Docker live models for OpenAI, native gateway core, the native OpenAI gateway profile, the native OpenAI plugin, and Docker live gateway OpenAI.
- **`stable`** — the default release approval profile; `minimum` plus Anthropic smoke, Google, MiniMax, backend, native live test harness, Docker live CLI backend, Docker ACP bind, Docker Codex harness, and an OpenCode Go smoke shard.
- **`full`** — a broad advisory sweep; `stable` plus advisory providers, plugin live shards, and media live shards.

## Full-only Additions

These suites are skipped by `stable` and included by `full`: **Docker live models** adds OpenCode Go, OpenRouter, xAI, Z.ai, and Fireworks; **Docker live gateway** splits advisory providers into DeepSeek/Fireworks, OpenCode Go/OpenRouter, and xAI/Z.ai shards; **Native gateway provider profiles** adds full Anthropic Opus and Sonnet/Haiku shards, Fireworks, DeepSeek, full OpenCode Go model shards, OpenRouter, xAI, and Z.ai; **Native plugin live shards** adds Plugins A-K, L-N, O-Z other, Moonshot, and xAI; **Native media live shards** adds Audio, Google music, MiniMax music, and video groups A-D. `stable` includes `native-live-src-gateway-profiles-anthropic-smoke` and `native-live-src-gateway-profiles-opencode-go-smoke`, while `full` uses the broader Anthropic and OpenCode Go model shards instead; focused reruns can still use the aggregate `native-live-src-gateway-profiles-anthropic` or `native-live-src-gateway-profiles-opencode-go` handles.

## Focused Reruns

Use `rerun_group` to avoid repeating unrelated release boxes: `all` (all stages); `ci` (manual full CI child only); `plugin-prerelease` (Plugin Prerelease child only); `release-checks` (all OpenClaw Release Checks stages); `install-smoke` (Install Smoke through release checks); `cross-os` (Cross-OS release checks); `live-e2e` (Repo/live E2E and Docker release-path validation); `package` (Package Acceptance); `qa` (QA parity plus QA live lanes); `qa-parity` (QA parity lanes and report only); `qa-live` (QA live Matrix/Telegram plus gated Discord, WhatsApp, and Slack lanes when enabled); and `npm-telegram` (published-package Telegram E2E, requires `release_package_spec` or `npm_telegram_package_spec`). Use `live_suite_filter` with `rerun_group=live-e2e` when one live suite failed — valid filter ids are defined in the reusable live/E2E workflow, including `docker-live-models`, `live-gateway-docker`, `live-gateway-anthropic-docker`, `live-gateway-google-docker`, `live-gateway-minimax-docker`, `live-gateway-advisory-docker`, `live-cli-backend-docker`, `live-acp-bind-docker`, and `live-codex-harness-docker`. The `live-gateway-advisory-docker` handle is an aggregate that still fans out to all advisory Docker gateway jobs. Use `cross_os_suite_filter` with `rerun_group=cross-os` when one cross-OS lane failed — the filter accepts an OS id, a suite id, or an OS/suite pair, for example `windows/packaged-upgrade`, `windows`, or `packaged-fresh`; cross-OS summaries include per-phase timings for packaged upgrade lanes, and long-running commands print heartbeat lines so a stuck Windows update is visible before the job timeout. QA release-check failures block normal release validation, and required OpenClaw dynamic tool drift in the standard tier also blocks the release-check verifier; Tideclaw alpha runs may still treat non-package-safety release-check lanes as advisory. When `live_suite_filter` explicitly requests a gated QA live lane such as Discord, WhatsApp, or Slack, the matching `OPENCLAW_RELEASE_QA_*_LIVE_CI_ENABLED` repo variable must be enabled, otherwise input capture fails instead of silently skipping the lane; rerun `rerun_group=qa`, `qa-parity`, or `qa-live` when you need fresh QA evidence.

## Evidence to Keep

Keep the `Full Release Validation` summary as the release-level index: it links child run ids and includes slowest-job tables. For failures, inspect the child workflow first, then rerun the smallest matching handle above. Useful artifacts to retain: `release-package-under-test` from `OpenClaw Release Checks`; Docker release-path artifacts under `.artifacts/docker-tests/`; Package Acceptance `package-under-test` and Docker acceptance artifacts; cross-OS release-check artifacts for each OS and suite; and QA parity, Matrix, and Telegram artifacts.

## Workflow Files

The release gate is backed by these workflow files: `.github/workflows/full-release-validation.yml`, `.github/workflows/openclaw-release-checks.yml`, `.github/workflows/openclaw-live-and-e2e-checks-reusable.yml`, `.github/workflows/plugin-prerelease.yml`, `.github/workflows/install-smoke.yml`, `.github/workflows/openclaw-cross-os-release-checks-reusable.yml`, and `.github/workflows/package-acceptance.yml`.

**Source**: OpenClaw documentation — `reference/full-release-validation` (mirror `inbox/openclaw_docs/reference/full-release-validation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
