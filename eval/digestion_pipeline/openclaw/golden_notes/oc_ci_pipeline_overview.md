---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - ci
keywords:
  - openclaw ci pipeline
  - preflight changed scope
  - ci-changed-scope.mjs
  - fail-fast job order
  - pr context and evidence gate
  - clawsweeper activity forwarding
  - workflow_dispatch manual ci
  - blacksmith github-hosted runners
topics:
  - OpenClaw
  - CI Pipeline
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/ci
access_control_group: ["general"]
---

# OpenClaw — CI Pipeline Overview and Scope Routing

## Overview

This note describes the OpenClaw CI job graph and how scoping decides what runs, mirroring the upper sections of the `ci` source page (Pipeline overview, Fail-fast order, PR context and evidence, Scope and routing, ClawSweeper activity forwarding, Manual dispatches, Runners). OpenClaw CI runs on every push to `main` and every pull request; the `preflight` job classifies the diff and turns expensive lanes off when only unrelated areas changed, while manual `workflow_dispatch` runs intentionally bypass smart scoping and fan out the full graph for release candidates and broad validation. Android lanes stay opt-in through `include_android`, and release-only plugin coverage lives in a separate `Plugin Prerelease` workflow. Release-validation umbrellas, CodeQL scanning, and local/Docker E2E reproduction are documented in the sibling CI notes; this is the job-graph-and-routing concept they hang off.

## Pipeline overview

The CI graph is a table of jobs, each with a purpose and a "when it runs" condition. The `preflight` job detects docs-only changes, changed scopes, changed extensions, and builds the CI manifest; it runs always on non-draft pushes and PRs. `security-fast` (private key detection, changed-workflow audit via `zizmor`, and production lockfile audit) likewise runs always on non-draft pushes and PRs, and `check-docs` (docs formatting, lint, and broken-link checks) runs when docs changed. The remaining jobs run on Node-relevant changes unless noted:

- `check-dependencies` — production Knip dependency-only pass plus the unused-file allowlist guard.
- `build-artifacts` — builds `dist/`, Control UI, built-CLI smoke checks, embedded built-artifact checks, and reusable artifacts.
- `checks-fast-core` — fast Linux correctness lanes such as bundled, protocol, and CI-routing checks.
- `checks-fast-contracts-plugins-*` / `checks-fast-contracts-channels-*` — two sharded plugin contract checks and two sharded channel contract checks.
- `checks-node-core-*` — core Node test shards, excluding channel, bundled, contract, and extension lanes.
- `check-*` — sharded main local gate equivalent: prod types, lint, guards, test types, and strict smoke.
- `check-additional-*` — architecture, sharded boundary/prompt drift, extension guards, package boundary, and runtime topology.
- `checks-node-compat-node22` — Node 22 compatibility build and smoke lane; manual CI dispatch for releases.
- `skills-python` — Ruff + pytest for Python-backed skills; Python-skill-relevant changes.
- `checks-windows` — Windows-specific process/path tests plus shared runtime import specifier regressions; Windows-relevant changes.
- `macos-node` — macOS TypeScript test lane using the shared built artifacts; macOS-relevant changes.
- `macos-swift` — Swift lint, build, and tests for the macOS app; macOS-relevant changes.
- `android` — Android unit tests for both flavors plus one debug APK build; Android-relevant changes.
- `test-performance-agent` — daily Codex slow-test optimization after trusted activity; main CI success or manual dispatch.
- `openclaw-performance` — daily/on-demand Kova runtime performance reports with mock-provider, deep-profile, and GPT 5.5 live lanes; scheduled and manual dispatch.

## Fail-fast order

The graph executes in a deliberate fail-fast order: (1) `preflight` decides which lanes exist at all — the `docs-scope` and `changed-scope` logic are steps inside this job, not standalone jobs; (2) `security-fast`, `check-*`, `check-additional-*`, `check-docs`, and `skills-python` fail quickly without waiting on the heavier artifact and platform matrix jobs; (3) `build-artifacts` overlaps with the fast Linux lanes so downstream consumers can start as soon as the shared build is ready; (4) heavier platform and runtime lanes fan out after that — `checks-fast-core`, `checks-fast-contracts-plugins-*`, `checks-fast-contracts-channels-*`, `checks-node-core-*`, `checks-windows`, `macos-node`, `macos-swift`, and `android`.

GitHub may mark superseded jobs as `cancelled` when a newer push lands on the same PR or `main` ref — treat that as CI noise unless the newest run for the same ref is also failing. Matrix jobs use `fail-fast: false`, and `build-artifacts` reports embedded channel, core-support-boundary, and gateway-watch failures directly instead of queuing tiny verifier jobs. The automatic CI concurrency key is versioned (`CI-v7-*`) so a GitHub-side zombie in an old queue group cannot indefinitely block newer main runs; manual full-suite runs use `CI-manual-v1-*` and do not cancel in-progress runs. Timing is summarized with `pnpm ci:timings`, `pnpm ci:timings:recent`, or `node scripts/ci-run-timings.mjs <run-id>`, and CI uploads the same run summary as a `ci-timings-summary` artifact; for PR runs the terminal timing-summary job runs the helper from the trusted base revision before passing `GH_TOKEN` to `gh run view`, keeping the tokened query out of branch-controlled code.

## PR context and evidence

External contributor PRs run a PR context and evidence gate from `.github/workflows/real-behavior-proof.yml`. The workflow checks out the trusted base commit and evaluates the PR body only; it does not execute code from the contributor branch. The gate applies to PR authors who are not repository owners, members, collaborators, or bots. It passes when the PR body contains authored `What Problem This Solves` and `Evidence` sections; evidence can be a focused test, CI result, screenshot, recording, terminal output, live observation, redacted log, or artifact link. The body provides intent and validation, while reviewers inspect the code, tests, and CI for correctness. When the check fails, the contributor should update the PR body instead of pushing another code commit.

## Scope and routing

Scope logic lives in `scripts/ci-changed-scope.mjs` and is covered by unit tests in `src/scripts/ci-changed-scope.test.ts`. Manual dispatch skips changed-scope detection and makes the preflight manifest act as if every scoped area changed. The routing rules per surface are:

- **CI workflow edits** validate the Node CI graph plus workflow linting, but do not force Windows, Android, or macOS native builds, which stay scoped to platform source changes.
- **Workflow Sanity** runs `actionlint`, `zizmor` over all workflow YAML files, the composite-action interpolation guard, and the conflict-marker guard. The PR-scoped `security-fast` job also runs `zizmor` over changed workflow files so workflow security findings fail early.
- **Docs on `main` pushes** are checked by the standalone `Docs` workflow with the same ClawHub docs mirror used by CI, so mixed code+docs pushes do not also queue the CI `check-docs` shard; PRs and manual CI still run `check-docs` from CI when docs changed.
- **TUI PTY** is a focused workflow that runs `node scripts/run-vitest.mjs run --config test/vitest/vitest.tui-pty.config.ts` on Linux Node 24 for `src/tui/**`, the watch harness, package script, lockfile, and workflow edits. The required lane uses a deterministic `TuiBackend` fixture; the slower `tui --local` smoke is opt-in with `OPENCLAW_TUI_PTY_INCLUDE_LOCAL=1` and mocks only the external model endpoint.
- **CI routing-only edits, selected cheap core-test fixture edits, and narrow plugin contract helper/test-routing edits** use a fast Node-only manifest path — `preflight`, security, and a single `checks-fast-core` task — skipping build artifacts, Node 22 compatibility, channel contracts, full core shards, bundled-plugin shards, and additional guard matrices.
- **Windows Node checks** are scoped to Windows-specific process/path wrappers, npm/pnpm/UI runner helpers, package manager config, and the CI workflow surfaces that execute that lane; unrelated changes stay on the Linux Node lanes.

The slowest Node test families are split or balanced so each job stays small without over-reserving runners: plugin contracts and channel contracts each run as two weighted Blacksmith-backed shards with the standard GitHub runner fallback, core unit fast/support lanes run separately, core runtime infra is split between state, process/config, shared, and three cron domain shards, auto-reply runs as balanced workers (reply subtree split into agent-runner, dispatch, and commands/state-routing shards), and agentic gateway/server configs split across chat/auth/model/http-plugin/runtime/startup lanes. Broad browser, QA, media, and miscellaneous plugin tests use dedicated Vitest configs instead of the shared plugin catch-all, and include-pattern shards record timing by CI shard name in `.artifacts/vitest-shard-timings.json`. `check-additional-*` keeps package-boundary compile/canary work together and separates runtime topology architecture from gateway watch coverage; the boundary guard list is striped into one prompt-heavy shard and one combined shard for the remaining stripes. The expensive Codex happy-path prompt snapshot drift check runs as its own additional job for manual CI and prompt-affecting changes only, and gateway watch, channel tests, and the core support-boundary shard run concurrently inside `build-artifacts` after `dist/` and `dist-runtime/` are built.

Android CI runs both `testPlayDebugUnitTest` and `testThirdPartyDebugUnitTest` and then builds the Play debug APK; the third-party flavor has no separate source set or manifest, so its unit-test lane still compiles with the SMS/call-log BuildConfig flags while avoiding a duplicate debug APK packaging job. The `check-dependencies` shard runs `pnpm deadcode:dependencies` (a production Knip dependency-only pass pinned to the latest Knip version) and `pnpm deadcode:unused-files`, which compares Knip's production unused-file findings against `scripts/deadcode-unused-files.allowlist.mjs`. The unused-file guard fails when a PR adds a new unreviewed unused file or leaves a stale allowlist entry, while preserving intentional dynamic plugin, generated, build, live-test, and package bridge surfaces that Knip cannot resolve statically.

## ClawSweeper activity forwarding

`.github/workflows/clawsweeper-dispatch.yml` is the target-side bridge from OpenClaw repository activity into ClawSweeper. It does not check out or execute untrusted PR code; it creates a GitHub App token from `CLAWSWEEPER_APP_PRIVATE_KEY`, then dispatches compact `repository_dispatch` payloads to `openclaw/clawsweeper`. The workflow has four lanes:

- `clawsweeper_item` — for exact issue and pull request review requests.
- `clawsweeper_comment` — for explicit ClawSweeper commands in issue comments.
- `clawsweeper_commit_review` — for commit-level review requests on `main` pushes.
- `github_activity` — for general GitHub activity that the ClawSweeper agent may inspect.

The `github_activity` lane forwards normalized metadata only: event type, action, actor, repository, item number, URL, title, state, and short excerpts for comments or reviews when present; it intentionally avoids forwarding the full webhook body. The receiving workflow in `openclaw/clawsweeper` is `.github/workflows/github-activity.yml`, which posts the normalized event to the OpenClaw Gateway hook for the ClawSweeper agent. General activity is observation, not delivery-by-default: the agent receives the Discord target in its prompt and should post to `#clawsweeper` only when the event is surprising, actionable, risky, or operationally useful, while routine opens, edits, bot churn, duplicate webhook noise, and normal review traffic should result in `NO_REPLY`. GitHub titles, comments, bodies, review text, branch names, and commit messages are treated as untrusted data — input for summarization and triage, not instructions for the workflow or agent runtime.

## Manual dispatches

Manual CI dispatches run the same job graph as normal CI but force every non-Android scoped lane on: Linux Node shards, bundled-plugin shards, plugin and channel contract shards, Node 22 compatibility, `check-*`, `check-additional-*`, built-artifact smoke checks, docs checks, Python skills, Windows, macOS, and Control UI i18n. Standalone manual CI dispatches run Android only with `include_android=true`, which the full release umbrella also passes. Plugin prerelease static checks, the release-only `agentic-plugins` shard, the full extension batch sweep, and plugin prerelease Docker lanes are excluded from CI — the Docker prerelease suite runs only when `Full Release Validation` dispatches the separate `Plugin Prerelease` workflow with the release-validation gate enabled. Manual runs use a unique concurrency group so a release-candidate full suite is not cancelled by another push or PR run on the same ref, and the optional `target_ref` input lets a trusted caller run that graph against a branch, tag, or full commit SHA using the workflow file from the selected dispatch ref.

```bash
gh workflow run ci.yml --ref release/YYYY.M.PATCH
gh workflow run ci.yml --ref main -f target_ref=<branch-or-sha> -f include_android=true
gh workflow run full-release-validation.yml --ref main -f ref=<branch-or-sha>
```

## Runners

CI maps jobs onto a runner matrix. Canonical-repo CI keeps Blacksmith as the default runner path for normal push and PR runs; `workflow_dispatch` and non-canonical repository runs use GitHub-hosted runners, but normal canonical runs do not currently probe Blacksmith queue health or automatically fall back to GitHub-hosted labels when Blacksmith is unavailable. The runner-to-job assignment is:

- `ubuntu-24.04` — manual CI dispatch and non-canonical repository fallbacks, workflow-sanity, labeler, auto-response, docs workflows outside CI, and install-smoke preflight so the Blacksmith matrix can queue earlier.
- `blacksmith-4vcpu-ubuntu-2404` — `CodeQL Critical Quality`, `preflight`, `security-fast`, lower-weight extension shards, `checks-fast-core`, plugin/channel contract shards, `checks-node-compat-node22`, `check-guards`, `check-prod-types`, and `check-test-types`.
- `blacksmith-8vcpu-ubuntu-2404` — Linux Node test shards, bundled plugin test shards, `check-additional-*` shards, `check-dependencies`, and `android`.
- `blacksmith-16vcpu-ubuntu-2404` — `build-artifacts`, `check-lint` (CPU-sensitive enough that 8 vCPU cost more than they saved); install-smoke Docker builds (32-vCPU queue time cost more than it saved).
- `blacksmith-16vcpu-windows-2025` — `checks-windows`.
- `blacksmith-6vcpu-macos-15` — `macos-node` on `openclaw/openclaw`; forks fall back to `macos-15`.
- `blacksmith-12vcpu-macos-26` — `macos-swift` on `openclaw/openclaw`; forks fall back to `macos-26`.

**Source**: OpenClaw documentation — `ci` (mirror `inbox/openclaw_docs/ci.md`)
**Last Updated**: 2026-06-22
**Status**: Active
