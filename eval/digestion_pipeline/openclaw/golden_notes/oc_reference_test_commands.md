---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - testing
keywords:
  - openclaw test commands
  - pnpm test changed force coverage
  - vitest scoped lanes shards
  - openclaw local pr gate
  - shared test state helper
  - onboarding e2e docker smoke
  - qr import smoke docker
  - test:docker lanes
topics:
  - OpenClaw
  - Testing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/test
access_control_group: ["general"]
---

# OpenClaw — Running the Local Test Suite (`pnpm test*`)

## Overview

This note is the procedure for running OpenClaw's own local Vitest test suite and its containerized smoke lanes, mirroring the command-catalog portion of the `reference/test` source page — the leading un-headed `pnpm test*` bullet block plus the `## Local PR gate`, `## Onboarding E2E (Docker)`, `## QR import smoke (Docker)`, and `## Related` sections. It covers the routine local test order, the `test` / `test:changed` / `test:force` / `test:coverage` lanes, scoped-vs-full-suite routing, the shared test-state helper and E2E/PTY/Docker helpers, the many `test:docker:*` smoke lanes, the local PR land/gate command set, and the two Docker onboarding/QR smokes. The four performance `bench-*` scripts on the same source page are a separate procedure documented in the split sibling `oc_reference_benchmarks`.

## Routine local test order

The page prescribes a three-step routine local test order so the cheapest scoped proof runs first and the full suite runs only when intentional:

1. `pnpm test:changed` for changed-scope Vitest proof.
2. `pnpm test <path-or-filter>` for one file, directory, or explicit target.
3. `pnpm test` only when you intentionally need the full local Vitest suite.

`pnpm test` routes explicit file/directory targets through scoped Vitest lanes; an untargeted run is full-suite proof — it uses fixed shard groups, expands to leaf configs for local parallel execution, and prints the expected local shard fanout before starting. The extension group always expands to the per-extension shard configs instead of one giant root-project process. Every test-wrapper run ends with a short `[test] passed|failed|skipped ... in ...` summary; Vitest's own duration line stays the per-shard detail.

## Changed-scope and check lanes

`pnpm test:changed` is the cheap smart changed test run: it runs precise targets from direct test edits, sibling `*.test.ts` files, explicit source mappings, and the local import graph. Broad/config/package changes are skipped unless they map to precise tests. `OPENCLAW_TEST_CHANGED_BROAD=1 pnpm test:changed` is the explicit broad changed run — use it when a test harness/config/package edit should fall back to Vitest's broader changed-test behavior. `pnpm changed:lanes` shows the architectural lanes triggered by the diff against `origin/main`.

`pnpm check:changed` delegates to Crabbox/Testbox by default outside CI, then runs the smart changed check gate for the diff against `origin/main` inside the remote child; it runs typecheck, lint, and guard commands for the affected architectural lanes but does NOT run Vitest tests — use `pnpm test:changed` or explicit `pnpm test <target>` for test proof. Source files with sibling tests map to that sibling before falling back to wider directory globs; helper edits under `src/channels/plugins/contracts/test-helpers`, `src/plugin-sdk/test-helpers`, and `src/plugins/contracts` use a local import graph to run importing tests instead of broad-running every shard when the dependency path is precise.

## Coverage, force, and isolation lanes

`pnpm test:force` kills any lingering gateway process holding the default control port, then runs the full Vitest suite with an isolated gateway port so server tests don't collide with a running instance — use it when a prior gateway run left port `18789` occupied. `pnpm test:coverage` runs the unit suite with V8 coverage (via `vitest.unit.config.ts`); this is a default-unit-lane coverage gate, not whole-repo all-file coverage, with thresholds of 70% lines/functions/statements and 55% branches. Because `coverage.all` is false and the default lane scopes coverage includes to non-fast unit tests with sibling source files, the gate measures source owned by this lane instead of every transitive import it happens to load. `pnpm test:coverage:changed` runs unit coverage only for files changed since `origin/main`.

`OPENCLAW_HEAVY_CHECK_LOCK_SCOPE=worktree <local-heavy-check command>` keeps heavy-check serialization inside the current worktree instead of the Git common dir for commands such as `pnpm check:changed` and targeted `pnpm test ...`; use it only on high-capacity local hosts when you intentionally run independent checks across linked worktrees.

## Shared test state and process helpers

To keep tests isolated, use the shared OpenClaw test state at `src/test-utils/openclaw-test-state.ts` from Vitest when a test needs an isolated `HOME`, `OPENCLAW_STATE_DIR`, `OPENCLAW_CONFIG_PATH`, config fixture, workspace, agent dir, or auth-profile store. `pnpm test:env-mutations:report` is a non-blocking report of tests and harnesses that mutate `HOME`, `OPENCLAW_STATE_DIR`, `OPENCLAW_CONFIG_PATH`, `OPENCLAW_WORKSPACE_DIR`, or related OpenClaw env keys directly — use it to find candidates for migration to the shared helper.

Process-level helpers cover the heavier lanes: use `test/helpers/openclaw-test-instance.ts` when a Vitest process-level E2E test needs a running Gateway, CLI env, log capture, and cleanup in one place. Docker/Bash E2E lanes that source `scripts/lib/docker-e2e-image.sh` can pass `docker_e2e_test_state_shell_b64 <label> <scenario>` into the container and decode it with `scripts/lib/openclaw-e2e-instance.sh`; multi-home scripts can pass `docker_e2e_test_state_function_b64` and call `openclaw_test_state_create <label> <scenario>` in each flow. Lower-level callers can use `scripts/lib/openclaw-test-state.mjs shell --label <name> --scenario <name>` for an in-container shell snippet, or `node scripts/lib/openclaw-test-state.mjs -- create --label <name> --scenario <name> --env-file <path> --json` for a sourceable host env file (the `--` before `create` keeps newer Node runtimes from treating `--env-file` as a Node flag).

## Scoped lanes, shards, and timing balance

Full, extension, and include-pattern shard runs update local timing data in `.artifacts/vitest-shard-timings.json`; later whole-config runs use those timings to balance slow and fast shards. Include-pattern CI shards append the shard name to the timing key, which keeps filtered shard timings visible without replacing whole-config timing data — set `OPENCLAW_TEST_PROJECTS_TIMINGS=0` to ignore the local timing artifact. Selected `plugin-sdk` and `commands` test files route through dedicated light lanes that keep only `test/setup.ts`, leaving runtime-heavy cases on their existing lanes. `auto-reply` splits into three dedicated configs (`core`, `top-level`, `reply`) so the reply harness does not dominate the lighter top-level status/token/helper tests. The base Vitest config defaults to `pool: "threads"` and `isolate: false`, with the shared non-isolated runner enabled across the repo configs.

Channel/extension lanes have their own entry points: `pnpm test:channels` runs `vitest.channels.config.ts`; `pnpm test:extensions` and `pnpm test extensions` run all extension/plugin shards (heavy channel plugins, the browser plugin, and OpenAI run as dedicated shards; other plugin groups stay batched), and `pnpm test extensions/<id>` runs one bundled plugin lane. Gateway integration is opt-in via `OPENCLAW_TEST_INCLUDE_GATEWAY=1 pnpm test` or `pnpm test:gateway`.

## E2E, UI, TUI, and import-profiling lanes

`pnpm test:e2e` runs the repo E2E aggregate: gateway end-to-end smoke tests plus the Control UI mocked browser E2E lane. `pnpm test:e2e:gateway` runs gateway end-to-end smoke tests (multi-instance WS/HTTP/node pairing); it defaults to `threads` + `isolate: false` with adaptive workers in `vitest.e2e.config.ts`, tunable with `OPENCLAW_E2E_WORKERS=<n>` and `OPENCLAW_E2E_VERBOSE=1` for verbose logs. Control UI mocked E2E uses `pnpm test:ui:e2e` for the Vitest + Playwright lane that starts the Vite Control UI and drives a real Chromium page against a mocked Gateway WebSocket (tests in `ui/src/**/*.e2e.test.ts`; shared mocks in `ui/src/test-helpers/control-ui-e2e.ts`), and `pnpm test:e2e` includes this lane. TUI PTY tests run via `node scripts/run-vitest.mjs run --config test/vitest/vitest.tui-pty.config.ts` for the fast fake-backend PTY lane; use `OPENCLAW_TUI_PTY_INCLUDE_LOCAL=1` or `pnpm tui:pty:test:watch --mode local` for the slower `tui --local` smoke (assert stable visible text or fixture calls, not raw ANSI snapshots). `pnpm test:live` runs provider live tests (minimax/zai) and requires API keys plus `LIVE=1` (or provider-specific `*_LIVE_TEST=1`) to unskip.

Import-profiling lanes: `pnpm test:perf:imports` enables Vitest import-duration + import-breakdown reporting while still scoping explicit targets, and `pnpm test:perf:imports:changed` profiles only files changed since `origin/main`.

## Codex worktrees and linked checkouts

In Codex worktrees and linked/sparse checkouts, avoid direct local `pnpm test*`, `pnpm check*`, and `pnpm crabbox:run` unless you have verified pnpm will not reconcile dependencies. For tiny explicit-file proof use `node scripts/run-vitest.mjs <path-or-filter>`; for changed gates or broad proof use `node scripts/crabbox-wrapper.mjs run --provider blacksmith-testbox ... -- env OPENCLAW_CHECK_CHANGED_REMOTE_CHILD=1 OPENCLAW_CHANGED_LANES_RAW_SYNC=1 corepack pnpm check:changed` so pnpm runs inside Testbox. For UI E2E in Codex worktrees, prefer `node scripts/run-vitest.mjs run --config test/vitest/vitest.ui-e2e.config.ts --configLoader runner ui/src/ui/e2e/chat-flow.e2e.test.ts` for tiny targeted proof after dependencies are installed, or Testbox/Crabbox for broader GUI proof.

## Docker smoke and install lanes (`test:docker:*`)

`pnpm test:docker:all` builds the shared live-test image, packs OpenClaw once as an npm tarball, builds/reuses a bare Node/Git runner image plus a functional image that installs that tarball into `/app`, then runs Docker smoke lanes with `OPENCLAW_SKIP_DOCKER_BUILD=1` through a weighted scheduler. The bare image (`OPENCLAW_DOCKER_E2E_BARE_IMAGE`) drives installer/update/plugin-dependency lanes (mounting the prebuilt tarball), and the functional image (`OPENCLAW_DOCKER_E2E_FUNCTIONAL_IMAGE`) drives normal built-app functionality lanes. `scripts/package-openclaw-for-docker.mjs` is the single local/CI package packer and validates the tarball plus `dist/postinstall-inventory.json` before Docker consumes it; lane definitions live in `scripts/lib/docker-e2e-scenarios.mjs`, planner logic in `scripts/lib/docker-e2e-plan.mjs`, and `scripts/test-docker-all.mjs` executes the selected plan (`node scripts/test-docker-all.mjs --plan-json` emits the scheduler-owned CI plan without building/running Docker). Parallelism/cap env knobs include `OPENCLAW_DOCKER_ALL_PARALLELISM` (default 10), `OPENCLAW_DOCKER_ALL_TAIL_PARALLELISM` (default 10), heavy-lane caps `OPENCLAW_DOCKER_ALL_LIVE_LIMIT=9` / `OPENCLAW_DOCKER_ALL_NPM_LIMIT=5` / `OPENCLAW_DOCKER_ALL_SERVICE_LIMIT=7`, per-provider caps `OPENCLAW_DOCKER_ALL_LIVE_CLAUDE_LIMIT=4` / `_CODEX_LIMIT=4` / `_GEMINI_LIMIT=4`, a 2-second lane stagger (`OPENCLAW_DOCKER_ALL_START_STAGGER_MS`), retry control `OPENCLAW_DOCKER_ALL_LIVE_RETRIES`, fail-fast (`OPENCLAW_DOCKER_ALL_FAIL_FAST=0` to disable), a 120-minute per-lane fallback timeout (`OPENCLAW_DOCKER_ALL_LANE_TIMEOUT_MS`), and a dry-run manifest (`OPENCLAW_DOCKER_ALL_DRY_RUN=1`). Per-lane logs, `summary.json`, `failures.json`, and phase timings are written under `.artifacts/docker-tests/<run-id>/`; use `pnpm test:docker:timings <summary.json>` to inspect slow lanes after a Docker all run and `pnpm test:docker:rerun <run-id|summary.json|failures.json>` to print cheap targeted rerun commands.

Focused Docker lanes include `pnpm test:docker:browser-cdp-snapshot` (Chromium source E2E with raw CDP + isolated Gateway, verifying `browser doctor --deep` snapshots), `pnpm test:docker:skill-install` (installs the packed tarball, resolves a live ClawHub skill slug, runs `openclaw skills install`, verifies `SKILL.md` / `.clawhub/origin.json` / `.clawhub/lock.json` / `skills info --json`), CLI-backend live probes such as `pnpm test:docker:live-cli-backend:claude` (with `:resume` and `:mcp` aliases for Claude and Gemini), `pnpm test:docker:openwebui` (Dockerized OpenClaw + Open WebUI proxied chat), `pnpm test:docker:mcp-channels` (seeded Gateway + a client spawning `openclaw mcp serve` over the real stdio bridge), `pnpm test:docker:upgrade-survivor` and `pnpm test:docker:published-upgrade-survivor` / `pnpm test:docker:update-migration` (install-over-existing-user upgrade survival, checking `/healthz`, `/readyz`, RPC status, and config survival), and `pnpm test:docker:plugins` (install/update smoke for local path, `file:`, npm registry packages, git moving refs, ClawHub fixtures, marketplace updates, and Claude-bundle enable/inspect).

## Local PR gate

For local PR land/gate checks, run the gate command set:

```bash
pnpm check:changed
pnpm check
pnpm check:test-types
pnpm build
pnpm test
pnpm check:docs
```

If `pnpm test` flakes on a loaded host, rerun once before treating it as a regression, then isolate with `pnpm test <path/to/test>`. For memory-constrained hosts, use `OPENCLAW_VITEST_MAX_WORKERS=1 pnpm test` or `OPENCLAW_VITEST_FS_MODULE_CACHE_PATH=/tmp/openclaw-vitest-cache pnpm test:changed`.

## Onboarding E2E (Docker)

Docker is optional and only needed for containerized onboarding smoke tests. The full cold-start flow in a clean Linux container is:

```bash
scripts/e2e/onboard-docker.sh
```

This script drives the interactive wizard via a pseudo-tty, verifies config/workspace/session files, then starts the gateway and runs `openclaw health`.

## QR import smoke (Docker)

The QR import smoke ensures the maintained QR runtime helper loads under the supported Docker Node runtimes (Node 24 default, Node 22 compatible):

```bash
pnpm test:docker:qr
```

**Source**: OpenClaw documentation — `reference/test` (mirror `inbox/openclaw_docs/reference/test.md`), command-catalog + Local PR gate + Onboarding E2E + QR import smoke sections
**Last Updated**: 2026-06-22
**Status**: Active
