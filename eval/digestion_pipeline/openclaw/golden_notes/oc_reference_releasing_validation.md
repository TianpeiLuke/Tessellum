---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - release_validation
keywords:
  - openclaw release validation
  - full release validation
  - release preflight
  - release test boxes
  - vitest docker qa lab package
  - package acceptance
  - rerun_group focused rerun
  - release_profile minimum stable full
  - qa otel prometheus smoke
  - release_package_spec
topics:
  - OpenClaw
  - Release Validation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/RELEASING
access_control_group: ["general"]
---

# OpenClaw — Release Pre-Release Validation (Preflight + Test Boxes)

## Overview

This note is the OpenClaw **pre-release validation procedure**: the deterministic release preflight run before any tag, and the four release test boxes (Vitest, Docker, QA Lab, Package) that `Full Release Validation` kicks off from one manual entrypoint. It mirrors the *Release preflight*, *Release test boxes*, and *Public references* sections of `reference/RELEASING`. Lane/version policy lives in `oc_reference_releasing_policy` and the publish sequence in `oc_reference_releasing_operator_checklist`; this note covers validation only.

## Release Preflight (Local Deterministic Gate)

Before release preflight, run the broader source checks outside the faster local `pnpm check` gate: `pnpm check:test-types` (test TypeScript) and `pnpm check:architecture` (import-cycle/architecture-boundary checks). Run `pnpm build && pnpm ui:build` before `pnpm release:check` so the `dist/*` artifacts and Control UI bundle exist for pack validation. Run `pnpm release:prep` after the root version bump and before tagging — it runs every deterministic release generator that commonly drifts after a version/config/API change (plugin versions/inventory, base config schema, bundled channel config metadata, config docs baseline, plugin SDK exports and API baseline). `pnpm release:check` re-runs those guards in check mode, reporting every generated-drift failure in one pass before package release checks; run it before every tagged release. Plugin version sync updates official plugin package versions and existing `openclaw.compat.pluginApi` floors to the release version by default; treat that field as the plugin SDK/runtime API floor (for plugin-only releases meant to stay compatible with older hosts, keep it at the oldest supported host API and document that in the plugin release proof).

The npm-side preflight has its own hard gate. `OpenClaw NPM Release` preflight generates dependency release evidence before packing the npm tarball; the **npm advisory vulnerability gate is release-blocking**, while the transitive manifest risk, dependency ownership/install-surface, and dependency-change reports (vs the previous reachable release tag) are evidence only. It uploads the evidence as `openclaw-release-dependency-evidence-<tag>` and embeds it under `dependency-evidence/` in the preflight artifact, which the real publish path reuses. The preflight **fails closed** unless the tarball includes both `dist/control-ui/index.html` and a non-empty `dist/control-ui/assets/` payload (so an empty browser dashboard cannot ship), and `pnpm test:install:smoke` enforces the npm pack `unpackedSize` budget so installer E2E catches pack bloat before publish.

### Telemetry Smoke Lanes

When validating release telemetry, run the smoke lanes:

- `pnpm qa:otel:smoke` — exercises QA-lab through a local OTLP/HTTP receiver and verifies trace/metric/log export plus bounded trace attributes and content/identifier redaction, without Opik, Langfuse, or another external collector.
- `pnpm qa:otel:collector-smoke` — routes the same QA-lab OTLP export through a real OpenTelemetry Collector Docker container before the local receiver assertions.
- `pnpm qa:prometheus:smoke` — exercises QA-lab, rejects unauthenticated scrapes, and verifies release-critical metric families stay free of prompt content, raw identifiers, auth tokens, and local paths.
- `pnpm qa:observability:smoke` — runs the OpenTelemetry and Prometheus smoke lanes together.

### The `Full Release Validation` Umbrella

Run the manual `Full Release Validation` workflow before release approval to kick off all pre-release test boxes from one entrypoint. It accepts a branch, tag, or full commit SHA, dispatches manual `CI`, and dispatches `OpenClaw Release Checks` for install smoke, package acceptance, cross-OS package checks, QA Lab parity, Matrix, and Telegram lanes. Package Acceptance provides the canonical package Telegram E2E, avoiding a second concurrent live poller. After publishing a beta, `release_package_spec` reuses the shipped package across release checks, Package Acceptance, and package Telegram E2E without rebuilding the tarball; `npm_telegram_package_spec` / `package_acceptance_package_spec` scope a different package to only Telegram or only Package Acceptance, and `evidence_package_spec` proves the validation matches a published package without forcing Telegram E2E.

`OpenClaw Release Checks` is the separate manual workflow that runs the slower live boxes (QA Lab, cross-OS, Docker live/E2E, Package Acceptance, Telegram). It accepts a branch, tag, or full commit SHA reachable from an OpenClaw branch or release tag; cross-OS install/upgrade runtime validation runs (here and in the umbrella) via the reusable `openclaw-cross-os-release-checks-reusable.yml`, and the live prompt-cache lane runs `OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_CACHE_TEST=1 pnpm test:live:cache` with both `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` secrets. The split keeps the real npm release path short, deterministic, and artifact-focused while slower live checks never block publish. Both workflows are always validation-only; secret-bearing checks should be dispatched through `Full Release Validation` or the `main`/release workflow ref.

### `Full Release Validation` Dispatch and `release_profile`

For release branch or tag validation, run the umbrella from the trusted `main` workflow ref and pass the release branch or tag as `ref`. Child workflows always dispatch from that trusted ref (normally `--ref main`) even when the target `ref` points at an older release branch or tag — there is no separate workflow-ref input. Do not use `--ref main -f ref=<sha>` for exact commit proof on moving `main` (raw SHAs cannot be dispatch refs); instead use `pnpm ci:full-release --sha <full-sha>`, which pushes a pinned `release-ci/<sha>-...` branch, dispatches the umbrella with `ref=<sha>`, verifies every child `headSha` matches, then deletes the branch.

```bash
gh workflow run full-release-validation.yml --ref main \
  -f ref=release/YYYY.M.PATCH -f provider=openai \
  -f mode=both -f release_profile=stable \
  -f release_package_spec=openclaw@YYYY.M.PATCH-beta.N
```

`release_profile` selects live/provider breadth: **`minimum`** = fastest release-critical OpenAI/core live and Docker path; **`stable`** = minimum plus stable provider/backend coverage for approval; **`full`** = stable plus broad advisory provider/media coverage. Stable and full validation always run the exhaustive live/E2E, Docker release-path, and bounded published upgrade-survivor sweep before promotion (`run_release_soak=true` requests that same sweep for a beta); the sweep covers the latest four stable packages plus pinned `2026.4.23`, `2026.5.2`, and `2026.4.15` baselines, each sharded into its own Docker runner job. With `release_package_spec`, release checks download the shipped beta once, extract its build source SHA from `dist/build-info.json`, and reuse that artifact across all package-facing lanes; cross-OS OpenAI install smoke uses `OPENCLAW_CROSS_OS_OPENAI_MODEL` when set, else `openai/gpt-5.4`.

## Release Test Boxes

`Full Release Validation` is the one manual entrypoint for the four boxes — **Vitest, Docker, QA Lab, and Package**. `OpenClaw Release Checks` resolves the target ref once as `release-package-under-test` so all package-facing boxes run on the same bytes. A full/all run is acceptable only when the umbrella summary shows `normal_ci`, `plugin_prerelease`, and `release_checks` successful (unless a focused rerun intentionally skipped the separate `Plugin Prerelease` child); the verifier summary includes slowest-job tables per child run. See [Full release validation](https://docs.openclaw.ai/reference/full-release-validation) for the complete stage matrix, job names, stable-versus-full differences, artifacts, and focused rerun handles.

### Vitest

The Vitest box is the manual `CI` child workflow. Manual CI intentionally bypasses changed scoping and forces the normal test graph for the release candidate: Linux Node shards, bundled-plugin shards, plugin and channel contract shards, Node 22 compatibility, `check-*`/`check-additional-*`, built-artifact smoke checks, docs checks, Python skills, Windows, macOS, and Control UI i18n. Android is included when `Full Release Validation` runs the box (the umbrella passes `include_android=true`); standalone manual CI requires `include_android=true`. This box answers "did the source tree pass the full normal test suite?" — not release-path product validation; keep as evidence the `CI` run green on the exact target SHA plus timing artifacts like `.artifacts/vitest-shard-timings.json`. Run manual CI directly only when the release needs deterministic normal CI but not the Docker, QA Lab, live, cross-OS, or package boxes:

```bash
gh workflow run ci.yml --ref main -f target_ref=release/YYYY.M.PATCH
gh workflow run ci.yml --ref main -f target_ref=release/YYYY.M.PATCH -f include_android=true
```

### Docker

The Docker box lives in `OpenClaw Release Checks` through `openclaw-live-and-e2e-checks-reusable.yml`, plus the release-mode `install-smoke` workflow, validating the candidate through packaged Docker environments instead of only source-level tests. Coverage includes: full install smoke (slow Bun global install smoke enabled); root Dockerfile smoke image preparation/reuse by target SHA (QR, root/gateway, installer/Bun smoke as separate shards); repository E2E lanes; release-path Docker chunks (`core`, `package-update-openai`/`-anthropic`/`-core`, `plugins-runtime-plugins`/`-services`, `plugins-runtime-install-a..h`); OpenWebUI coverage inside the `plugins-runtime-services` chunk when requested; split bundled-plugin lanes `bundled-plugin-install-uninstall-0..23`; and live/E2E provider suites plus Docker live model coverage when release checks include live suites. Use Docker artifacts before rerunning: the release-path scheduler uploads `.artifacts/docker-tests/` with lane logs, `summary.json`, `failures.json`, phase timings, scheduler plan JSON, and rerun commands. For focused recovery, use `docker_lanes=<lane[,lane]>` on the reusable workflow instead of rerunning all chunks; generated rerun commands include prior `package_artifact_run_id` and prepared image inputs so a failed lane reuses the same tarball and GHCR images.

### QA Lab

The QA Lab box is also part of `OpenClaw Release Checks` — the agentic-behavior and channel-level release gate, separate from Vitest and Docker package mechanics. Coverage: the mock parity lane comparing the OpenAI candidate lane against the Opus 4.6 baseline (agentic parity pack); the fast live Matrix QA profile (`qa-live-shared`); the live Telegram QA lane (Convex CI credential leases); and the telemetry smoke lanes above when needed. Use this box to answer "does the release behave correctly in QA scenarios and live channel flows?" — keep parity, Matrix, and Telegram artifact URLs when approving. Full Matrix coverage is available as a manual sharded `QA-Lab - All Lanes` run (`matrix_profile=all`, `matrix_shards=true`), not the default release-critical lane.

### Package

The Package box is the installable-product gate, backed by `Package Acceptance` and the resolver `scripts/resolve-openclaw-package-candidate.mjs`, which normalizes a candidate into the `package-under-test` tarball consumed by Docker E2E, validates the package inventory, records the version and SHA-256, and keeps the harness ref separate from the package source ref. Supported candidate sources: `source=npm` (`openclaw@beta`/`@latest`/exact version); `source=ref` (pack a trusted `package_ref` with the `workflow_ref` harness); `source=url` (public HTTPS `.tgz` with required `package_sha256`, rejecting URL credentials, non-default ports, private hosts, unsafe redirects); `source=trusted-url` (HTTPS `.tgz` with `package_sha256` + `trusted_source_id` from `.github/package-trusted-sources.json`, for maintainer-owned mirrors); and `source=artifact` (reuse a `.tgz` from another run).

`OpenClaw Release Checks` runs Package Acceptance with `source=artifact`, the prepared release package artifact, `suite_profile=custom`, a `docker_lanes` list (`doctor-switch update-channel-switch skill-install update-corrupt-plugin upgrade-survivor published-upgrade-survivor update-restart-auth plugins-offline plugin-update`), and `telegram_mode=mock-openai`, keeping migration, update, configured-auth update-restart, live ClawHub skill install, stale plugin-dependency cleanup, offline-plugin fixtures, plugin update, and Telegram package QA against the same tarball. Blocking release checks use the default latest-published-package baseline; `run_release_soak=true`, `release_profile=stable`, or `release_profile=full` expands to every stable npm-published baseline from `2026.4.23` through `latest` plus reported-issue fixtures. Package Acceptance is the GitHub-native replacement for most package/update coverage that previously required Parallels (cross-OS release checks still cover OS-specific onboarding/installer behavior). Exhaustive published update migration is a separate manual `Update Migration` workflow; see [Testing updates and plugins](https://docs.openclaw.ai/help/testing-updates-plugins).

Legacy package-acceptance leniency is intentionally time-boxed: packages through `2026.4.25` may use a compatibility path for metadata gaps already published to npm, the published `2026.4.26` package may warn for already-shipped build-metadata stamp files, and later packages must satisfy the modern package contracts (those same gaps fail release validation). When the release question is about an actual installable package, dispatch `package-acceptance.yml` directly (e.g. `-f source=npm -f package_spec=openclaw@beta -f suite_profile=product -f published_upgrade_survivor_baseline=openclaw@2026.4.26`). The `suite_profile` choices ascend **`smoke`** (quick install/channel/agent, gateway network, config-reload) → **`package`** (install/update/restart/plugin contracts plus live ClawHub skill install — the release-check default) → **`product`** (`package` plus MCP channels, cron/subagent cleanup, OpenAI web search, OpenWebUI) → **`full`** (Docker release-path chunks with OpenWebUI), with **`custom`** taking an exact `docker_lanes` list. For package Telegram proof, enable `telegram_mode=mock-openai` or `live-frontier`.

## Focused Rerun and Recovery (`rerun_group`)

Do not use the full umbrella as the first rerun after a focused fix. If one box fails, use the failed child workflow, job, Docker lane, package profile, model provider, or QA lane for the next proof; rerun the full umbrella only when the fix changed shared release orchestration or made earlier evidence stale. The verifier re-checks recorded child run ids, so after a child reruns successfully, rerun only the failed `Verify full validation` parent job. For bounded recovery, pass `rerun_group` to the umbrella: `all` (real run), `ci`, `plugin-prerelease`, `release-checks` (every box), and the narrower groups `install-smoke`, `cross-os`, `live-e2e`, `package`, `qa`, `qa-parity`, `qa-live`, `npm-telegram`. Focused `npm-telegram` reruns require `release_package_spec` or `npm_telegram_package_spec`; focused cross-OS reruns can add `cross_os_suite_filter=windows/packaged-upgrade`. QA release-check failures block normal release validation (including required OpenClaw dynamic tool drift in the standard tier), though Tideclaw alpha runs may treat non-package-safety lanes as advisory. When `live_suite_filter` requests a gated QA live lane (Discord, WhatsApp, Slack), the matching `OPENCLAW_RELEASE_QA_*_LIVE_CI_ENABLED` repo variable must be enabled, otherwise input capture fails rather than silently skipping.

**Source**: OpenClaw documentation — `reference/RELEASING` (mirror `inbox/openclaw_docs/reference/RELEASING.md`), sections Release preflight, Release test boxes (Vitest, Docker, QA Lab, Package), Public references
**Last Updated**: 2026-06-22
**Status**: Active
