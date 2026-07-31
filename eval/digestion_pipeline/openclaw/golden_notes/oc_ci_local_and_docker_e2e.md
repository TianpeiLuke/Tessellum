---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - ci
keywords:
  - openclaw local ci equivalents
  - pnpm check changed local gate
  - test docker all aggregate
  - local docker e2e tunables
  - reusable live e2e workflow
  - release-path docker chunks
  - crabbox blacksmith testbox
  - docs agent test performance agent
  - duplicate prs after merge
topics:
  - OpenClaw
  - CI Local and Docker E2E
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/ci
access_control_group: ["general"]
---

# OpenClaw — Reproducing CI Locally and on Docker / Testbox

## Overview

This note is the procedure for reproducing OpenClaw CI outside the canonical GitHub Actions graph: the `pnpm` local-equivalent gate commands, the local Docker E2E aggregate (`pnpm test:docker:all`) with its tunables / reusable workflow / release-path chunks, the local changed-lane check gates, the Crabbox / Blacksmith Testbox remote-box maintainer proof flow, and the Codex maintenance workflows (Docs Agent, Test Performance Agent, Duplicate PRs After Merge). It mirrors the `Local equivalents`, `Local Docker E2E`, `Maintenance workflows`, `Local check gates and changed routing`, and `Testbox validation` sections of the `ci` source page. The sibling pipeline-overview note covers the CI job graph/scope/runners; the release-validation note covers release umbrellas and Package Acceptance.

## Local equivalents

These `pnpm`/`node` commands run the same correctness lanes locally that CI exercises, so a contributor can reproduce a CI gate before pushing (run from repo root). Separate CI-timing helpers (`pnpm ci:timings`, `node scripts/ci-run-timings.mjs <run-id>`) summarize wall/queue time and slowest jobs, and `pnpm test:perf:groups` / `test:startup:memory` / `perf:kova:summary` produce perf/memory reports.

```bash
pnpm changed:lanes                            # inspect the local changed-lane classifier for origin/main...HEAD
pnpm check:changed                            # smart local check gate: changed typecheck/lint/guards by boundary lane
pnpm check                                    # fast local gate: prod tsgo + sharded lint + parallel fast guards
pnpm check:test-types
pnpm check:timed                              # same gate with per-stage timings
pnpm build:strict-smoke
pnpm check:architecture
pnpm test:gateway:watch-regression
node scripts/run-vitest.mjs run --config test/vitest/vitest.tui-pty.config.ts
pnpm test                                     # vitest tests
pnpm test:changed                             # cheap smart changed Vitest targets
pnpm test:channels
pnpm test:contracts:channels
pnpm check:docs                               # docs format + lint + broken links
pnpm build                                    # build dist for CI artifact/smoke checks
```

## Local Docker E2E

`pnpm test:docker:all` prebuilds one shared live-test image, packs OpenClaw once as an npm tarball, and builds two shared `scripts/e2e/Dockerfile` images: a bare Node/Git runner for installer/update/plugin-dependency lanes, and a functional image that installs the same tarball into `/app` for normal functionality lanes. Lane definitions live in `scripts/lib/docker-e2e-scenarios.mjs`, planner logic in `scripts/lib/docker-e2e-plan.mjs`; the runner executes only the selected plan. The scheduler picks the image per lane with `OPENCLAW_DOCKER_E2E_BARE_IMAGE` / `OPENCLAW_DOCKER_E2E_FUNCTIONAL_IMAGE`, then runs lanes with `OPENCLAW_SKIP_DOCKER_BUILD=1`.

### Tunables

The local aggregate scheduler is controlled by these `OPENCLAW_DOCKER_ALL_*` variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENCLAW_DOCKER_ALL_PARALLELISM` | 10 | Main-pool slot count for normal lanes. |
| `OPENCLAW_DOCKER_ALL_TAIL_PARALLELISM` | 10 | Provider-sensitive tail-pool slot count. |
| `OPENCLAW_DOCKER_ALL_LIVE_LIMIT` | 9 | Concurrent live lane cap so providers do not throttle. |
| `OPENCLAW_DOCKER_ALL_NPM_LIMIT` | 5 | Concurrent npm install lane cap. |
| `OPENCLAW_DOCKER_ALL_SERVICE_LIMIT` | 7 | Concurrent multi-service lane cap. |
| `OPENCLAW_DOCKER_ALL_START_STAGGER_MS` | 2000 | Stagger between lane starts to avoid Docker daemon create storms; set `0` for no stagger. |
| `OPENCLAW_DOCKER_ALL_LANE_TIMEOUT_MS` | 7200000 | Per-lane fallback timeout (120 minutes); selected live/tail lanes use tighter caps. |
| `OPENCLAW_DOCKER_ALL_DRY_RUN` | unset | `1` prints the scheduler plan without running lanes. |
| `OPENCLAW_DOCKER_ALL_LANES` | unset | Comma-separated exact lane list; skips cleanup smoke so agents can reproduce one failed lane. |

A lane heavier than its effective cap can still start from an empty pool, then runs alone until it releases capacity. The local aggregate preflights Docker, removes stale OpenClaw E2E containers, emits active-lane status, persists lane timings for longest-first ordering, and stops scheduling new pooled lanes after the first failure.

### Reusable live/E2E workflow

The reusable live/E2E workflow asks `scripts/test-docker-all.mjs --plan-json` which package, image kind, live image, lane, and credential coverage is required; `scripts/docker-e2e.mjs` converts that plan into GitHub outputs and summaries. It either packs OpenClaw through `scripts/package-openclaw-for-docker.mjs`, downloads a current-run package artifact, or downloads one from `package_artifact_run_id`; validates the tarball inventory; builds and pushes package-digest-tagged bare/functional GHCR images through Blacksmith's Docker layer cache when the plan needs package-installed lanes; and reuses provided `docker_e2e_bare_image` / `docker_e2e_functional_image` inputs or existing package-digest images instead of rebuilding. Docker image pulls retry with a bounded 180-second per-attempt timeout so a stuck registry/cache stream retries quickly rather than consuming the CI critical path.

### Release-path chunks

Release Docker coverage runs smaller chunked jobs with `OPENCLAW_SKIP_DOCKER_BUILD=1` so each chunk pulls only the image kind it needs and executes multiple lanes through the same weighted scheduler, selected via `OPENCLAW_DOCKER_ALL_PROFILE=release-path` plus an `OPENCLAW_DOCKER_ALL_CHUNK` value: `core`, `package-update-openai`, `package-update-anthropic`, `package-update-core`, `plugins-runtime-plugins`, `plugins-runtime-services`, and `plugins-runtime-install-a` through `plugins-runtime-install-h`. `package-update-openai` includes the live Codex plugin package lane (installs the candidate package + Codex plugin from `codex_plugin_spec`, runs Codex CLI preflight, then multiple same-session OpenClaw agent turns against OpenAI). `plugins-runtime-core`/`plugins-runtime`/`plugins-integrations` remain aggregate aliases, and `install-e2e` is the aggregate manual rerun alias for both provider installer lanes.

Each chunk uploads `.artifacts/docker-tests/` with lane logs, `summary.json`, `failures.json`, phase timings, scheduler plan JSON, slow-lane tables, and per-lane rerun commands. The workflow `docker_lanes` input runs selected lanes against the prepared images instead of the chunk jobs, bounding failed-lane debugging to one targeted Docker job; generated rerun commands include `package_artifact_run_id`, `package_artifact_name`, and prepared image inputs so a failed lane reuses the exact package/images from the failed run. The scheduled live/E2E workflow runs the full release-path Docker suite daily. Helpers to fetch artifacts and re-derive rerun commands:

```bash
pnpm test:docker:rerun <run-id>      # download Docker artifacts and print combined/per-lane targeted rerun commands
pnpm test:docker:timings <summary>   # slow-lane and phase critical-path summaries
```

## Local check gates and changed routing

Local changed-lane logic lives in `scripts/changed-lanes.mjs`, executed by `scripts/check-changed.mjs`. That local check gate is stricter about architecture boundaries than the broad CI platform scope, routing by what changed:

- core production changes run core prod + core test typecheck plus core lint/guards; core test-only changes run only core test typecheck plus core lint;
- extension production changes run extension prod + extension test typecheck plus extension lint; extension test-only changes run extension test typecheck plus extension lint;
- public Plugin SDK or plugin-contract changes expand to extension typecheck because extensions depend on those core contracts;
- release metadata-only version bumps run targeted version/config/root-dependency checks; unknown root/config changes fail safe to all check lanes.

Local changed-test routing lives in `scripts/test-projects.test-support.mjs` and is intentionally cheaper than `check:changed`: direct test edits run themselves, source edits prefer explicit mappings, then sibling tests and import-graph dependents. One explicit mapping routes shared group-room delivery config (group visible-reply config, source reply delivery mode, or the message-tool system prompt) through the core reply tests plus Discord and Slack delivery regressions, so a shared-default change fails before the first PR push. Use `OPENCLAW_TEST_CHANGED_BROAD=1 pnpm test:changed` only when the change is harness-wide enough that the cheap mapped set is not a trustworthy proxy.

## Testbox validation (Crabbox / Blacksmith)

Crabbox is the repo-owned remote-box wrapper for maintainer Linux proof. Use it from the repo root when a check is too broad for a local edit loop, when CI parity matters, or when the proof needs secrets, Docker, package lanes, reusable boxes, or remote logs. The normal backend is `blacksmith-testbox`; owned AWS/Hetzner capacity is a fallback for Blacksmith outages, quota issues, or explicit owned-capacity testing. Crabbox-backed Blacksmith runs warm, claim, sync, run, report, and clean up one-shot Testboxes. The built-in sync sanity check fails fast when required root files such as `pnpm-lock.yaml` disappear or when `git status --short` shows at least 200 tracked deletions (set `OPENCLAW_TESTBOX_ALLOW_MASS_DELETIONS=1` for intentional large-deletion PRs). Crabbox also terminates a local Blacksmith CLI invocation stuck in the sync phase for more than five minutes without post-sync output (set `CRABBOX_BLACKSMITH_SYNC_TIMEOUT_MS=0` to disable).

Before a first run, check the wrapper with `pnpm crabbox:run -- --help`. The repo wrapper refuses a stale Crabbox binary that does not advertise `blacksmith-testbox`, so pass the provider explicitly even though `.crabbox.yaml` has owned-cloud defaults. In Codex worktrees or sparse checkouts, avoid the `pnpm crabbox:run` script (pnpm may reconcile dependencies first) and invoke `node scripts/crabbox-wrapper.mjs run ...` directly. Blacksmith-backed runs require Crabbox 0.22.0 or newer. The canonical Blacksmith proof invocation differs only in its trailing `corepack pnpm` command for the changed gate, a focused rerun, or the full suite:

```bash
# Changed gate (substitute the trailing command for a focused rerun or full suite):
pnpm crabbox:run -- --provider blacksmith-testbox \
  --blacksmith-org openclaw \
  --blacksmith-workflow .github/workflows/ci-check-testbox.yml \
  --blacksmith-job check --blacksmith-ref main \
  --idle-timeout 90m --ttl 240m --timing-json --shell -- \
  "corepack pnpm check:changed"   # or "corepack pnpm test <filter>" / "corepack pnpm test"
```

Read the final JSON summary (fields `provider`, `leaseId`, `syncDelegated`, `exitCode`, `commandMs`, `totalMs`). One-shot Blacksmith Crabbox runs stop the Testbox automatically; if a run is interrupted, inspect live boxes with `blacksmith testbox list --all` / `status --id <tbx_id>` and stop ONLY boxes you created with `blacksmith testbox stop --id <tbx_id>`. Use reuse (`--id <tbx_id> --no-sync`) only when you need multiple commands on the same hydrated box, then `pnpm crabbox:stop -- <tbx_id>`. If Crabbox is broken but Blacksmith works, use direct Blacksmith only for `list`/`status`/cleanup diagnostics. If warmups sit `queued` with no IP/Actions URL after a couple of minutes, treat it as Blacksmith provider/queue/billing/org-limit pressure: stop the queued ids you created and move proof to owned capacity.

Escalate to owned Crabbox capacity only when Blacksmith is down, quota-limited, missing the needed environment, or owned capacity is the goal:

```bash
CRABBOX_CAPACITY_REGIONS=eu-west-1,eu-west-2,eu-central-1,us-east-1,us-west-2 \
  pnpm crabbox:warmup -- --provider aws --class standard --market on-demand --idle-timeout 90m
pnpm crabbox:hydrate -- --id <cbx_id-or-slug>
pnpm crabbox:run -- --id <cbx_id-or-slug> --timing-json --shell -- "pnpm check:changed"
pnpm crabbox:stop -- <cbx_id-or-slug>
```

Under AWS pressure, avoid `class=beast` unless the task really needs 48xlarge-class CPU — a `beast` request starts at 192 vCPUs and is the easiest way to trip regional EC2 Spot/On-Demand Standard quota. `.crabbox.yaml` defaults to `standard`, multiple capacity regions, and `capacity.hints: true` (brokered AWS leases print region/market, quota pressure, Spot fallback, and high-pressure class warnings). Use `fast` for heavier broad checks, `large` only after standard/fast fall short, and `beast` only for exceptional CPU-bound lanes — never for `check:changed`, focused tests, docs work, lint/typecheck, or outage triage. Use `--market on-demand` for capacity diagnosis.

## Maintenance workflows

Three Codex-driven workflows keep the repo aligned after merges (none is a pure schedule).

### Docs Agent

The `Docs Agent` workflow is an event-driven Codex maintenance lane for keeping existing docs aligned with recently landed changes. A successful non-bot push CI run on `main` can trigger it, and manual dispatch can run it directly. Workflow-run invocations skip when `main` has moved on or when another non-skipped Docs Agent run was created in the last hour. When it runs, it reviews the commit range from the previous non-skipped Docs Agent source SHA to current `main`, so one hourly run covers all changes since the last docs pass.

### Test Performance Agent

The `Test Performance Agent` workflow is an event-driven Codex maintenance lane for slow tests. A successful non-bot push CI run on `main` can trigger it, but it skips if another workflow-run invocation already ran or is running that UTC day; manual dispatch bypasses that daily gate. The lane builds a full-suite grouped Vitest performance report (per-config wall time and max RSS on Linux and macOS), lets Codex make only small coverage-preserving fixes, then reruns the report and rejects changes that reduce the passing baseline test count. If the baseline has failing tests, Codex may fix only obvious failures, and the after-agent report must pass before anything is committed. When `main` advances before the bot push lands, the lane rebases the validated patch, reruns `pnpm check:changed`, and retries the push. It runs on GitHub-hosted Ubuntu, keeping the same drop-sudo safety posture as the docs agent.

### Duplicate PRs After Merge

The `Duplicate PRs After Merge` workflow is a manual maintainer workflow for post-land duplicate cleanup. It defaults to dry-run and only closes explicitly listed PRs when `apply=true`. Before mutating GitHub, it verifies the landed PR is merged and that each duplicate has either a shared referenced issue or overlapping changed hunks.

```bash
gh workflow run duplicate-after-merge.yml \
  -f landed_pr=70532 \
  -f duplicate_prs='70530,70592' \
  -f apply=true
```

**Source**: OpenClaw documentation — `ci` (mirror `inbox/openclaw_docs/ci.md`), sections: Local equivalents, Local Docker E2E, Local check gates and changed routing, Testbox validation, Maintenance workflows
**Last Updated**: 2026-06-22
**Status**: Active
