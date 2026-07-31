---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - testing
keywords:
  - openclaw test suites
  - vitest unit integration e2e live
  - pnpm test gate
  - gateway stability suite
  - openshell backend e2e
  - which suite should i run
  - offline regression contract tests
  - adding regressions guidance
topics:
  - OpenClaw
  - Testing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/testing
access_control_group: ["general"]
---

# OpenClaw — Test Suite Taxonomy (Unit, Stability, E2E, Live)

## Overview

This note is the operator/maintainer procedure for OpenClaw's three Vitest suites (unit/integration, e2e, live) plus the gateway stability lane — the "how we test" map: which command runs where, what each suite covers (and deliberately does not), and how to choose. It mirrors the `help/testing` sections assigned here (Quick start through Adding regressions). The QA-lab runners (`pnpm openclaw qa …`), the Docker runner catalog (`test:docker:*`), and the deep live-model/media suites live in sibling notes and are linked, not duplicated here.

## Quick start

Most days run targeted iterations first, then widen. Recommended commands:

- Full gate (expected before push): `pnpm build && pnpm check && pnpm check:test-types && pnpm test`
- Faster local full-suite run on a roomy machine: `pnpm test:max`
- Direct Vitest watch loop: `pnpm test:watch`
- Direct file targeting routes extension/channel paths too: `pnpm test extensions/discord/src/monitor/message-handler.preflight.test.ts`
- Prefer targeted runs first when iterating on a single failure.
- Docker-backed QA site: `pnpm qa:lab:up`
- Linux VM-backed QA lane: `pnpm openclaw qa suite --runner multipass --scenario channel-chat-baseline`

When touching tests or wanting extra confidence: coverage gate `pnpm test:coverage`; E2E suite `pnpm test:e2e`. The QA-lab runners and live debugging commands are documented in their own pages (Related Notes).

## Test Temp Directories

Tests should use the shared helpers in `test/helpers/temp-dir.ts` for test-owned temporary directories — they make ownership explicit and keep cleanup in the same test lifecycle:

```ts
import { afterEach } from "vitest";
import { createTempDirTracker } from "../helpers/temp-dir.js";

const tempDirs = createTempDirTracker();

afterEach(tempDirs.cleanup);

it("uses a temp workspace", () => {
  const workspace = tempDirs.make("openclaw-example-");
  // use workspace
});
```

Use `makeTempDir(tempDirs, prefix)` and `cleanupTempDirs(tempDirs)` when a test already owns an array or set of paths. Avoid new bare `fs.mkdtemp*` calls unless a case explicitly verifies raw temp-dir behavior; when genuinely needed, add an auditable allow comment with a concrete reason — e.g. `// openclaw-temp-dir: allow verifies raw fs cleanup behavior` above the `fs.mkdtempSync(prefix)` call. For migration visibility, `node scripts/report-test-temp-creations.mjs` reports new bare temp-dir creation in added diff lines (non-blocking), and `check:changed` runs it for changed test paths as a warning-only CI signal.

## Test suites (what runs where)

The source frames the suites as "increasing realism" (and increasing flakiness/cost).

### Unit / integration (default)

- Command: `pnpm test`; Config: untargeted runs use the `vitest.full-*.config.ts` shard set and may expand multi-project shards into per-project configs for parallel scheduling.
- Files: core/unit inventories under `src/**/*.test.ts`, `packages/**/*.test.ts`, and `test/**/*.test.ts`; UI unit tests run in the dedicated `unit-ui` shard.
- Scope: pure unit tests, in-process integration tests (gateway auth, routing, tooling, parsing, config), and deterministic regressions. Runs in CI; no real keys required; fast and stable. Resolver and public-surface loader tests must prove broad `api.js` and `runtime-api.js` fallback behavior with generated tiny plugin fixtures, not real bundled plugin source APIs (real plugin API loads belong in plugin-owned contract/integration suites).

Native dependency policy: default test installs skip optional native Discord opus builds — Discord voice uses bundled `libopus-wasm` and `@discordjs/opus` stays disabled in `allowBuilds` so local tests and Testbox lanes do not compile the native addon. Compare native opus performance in the `libopus-wasm` benchmark repo, not in default OpenClaw install/test loops; do not set `@discordjs/opus` to `true` in the default `allowBuilds`.

The page expands several accordions for this lane. **Projects, shards, and scoped lanes:** untargeted `pnpm test` runs twelve smaller shard configs (`core-unit-fast`, `core-unit-src`, `core-unit-security`, `core-unit-ui`, `core-unit-support`, `core-support-boundary`, `core-contracts`, `core-bundled`, `core-runtime`, `agentic`, `auto-reply`, `extensions`) instead of one giant native root-project process; explicit file/directory targets route through scoped lanes first; `pnpm test:changed` expands changed git paths into cheap scoped lanes unless `OPENCLAW_TEST_CHANGED_BROAD=1`; `pnpm check:changed` is the smart local check gate (typecheck/lint/guard, not Vitest); import-light unit tests route through the `unit-fast` lane. **Vitest pool/isolation defaults:** base config defaults to `threads`, the shared config fixes `isolate: false` across root/e2e/live configs, and `scripts/run-vitest.mjs` adds `--no-maglev` by default and terminates explicit non-watch runs after 5 minutes with no output. **Iteration/perf:** `pnpm changed:lanes` shows triggered lanes, the pre-commit hook is formatting-only, `pnpm test:max` raises the worker cap, and `pnpm test:perf:*` lanes give import-duration/benchmark/CPU-heap profiling. **Embedded runner coverage:** keep the embedded-runner integration suites (`compact.hooks.test.ts`, `run.overflow-compaction.test.ts`, `run.overflow-compaction.loop.test.ts`) healthy — helper-only tests are not a sufficient substitute for the real `run.ts` / `compact.ts` paths.

### Stability (gateway)

- Command: `pnpm test:stability:gateway`; Config: `vitest.gateway.config.ts`, forced to one worker.
- Scope: starts a real loopback Gateway with diagnostics enabled by default, drives synthetic gateway message/memory/large-payload churn through the diagnostic event path, queries `diagnostics.stability` over the Gateway WS RPC, covers diagnostic stability bundle persistence helpers, and asserts the recorder stays bounded, synthetic RSS samples stay under the pressure budget, and per-session queue depths drain back to zero. CI-safe and keyless — a narrow lane for stability-regression follow-up, not a substitute for the full Gateway suite.

### E2E (repo aggregate)

- Command: `pnpm test:e2e`
- Scope: runs the gateway smoke E2E lane and the mocked Control UI browser E2E lane. CI-safe and keyless; requires Playwright Chromium to be installed.

### E2E (gateway smoke)

- Command: `pnpm test:e2e:gateway`; Config: `vitest.e2e.config.ts`; Files: `src/**/*.e2e.test.ts`, `test/**/*.e2e.test.ts`, and bundled-plugin E2E tests under `extensions/`.
- Runtime defaults: Vitest `threads` with `isolate: false`; adaptive workers (CI up to 2, local 1 by default); silent mode by default. Overrides: `OPENCLAW_E2E_WORKERS=<n>` (capped at 16) and `OPENCLAW_E2E_VERBOSE=1`.
- Scope: multi-instance gateway end-to-end behavior — WebSocket/HTTP surfaces, node pairing, and heavier networking. Runs in CI when enabled; no real keys required; can be slower than unit tests.

### E2E (Control UI mocked browser)

- Command: `pnpm test:ui:e2e`; Config: `test/vitest/vitest.ui-e2e.config.ts`; Files: `ui/src/**/*.e2e.test.ts`.
- Scope: starts the Vite Control UI, drives a real Chromium page through Playwright, and replaces the Gateway WebSocket with deterministic in-browser mocks. Runs in CI as part of `pnpm test:e2e`; no real Gateway/agents/provider keys; browser dependency must be present (`pnpm --dir ui exec playwright install chromium`).

### E2E: OpenShell backend smoke

- Command: `pnpm test:e2e:openshell`; File: `extensions/openshell/src/backend.e2e.test.ts`.
- Scope: starts an isolated OpenShell gateway on the host via Docker, creates a sandbox from a temporary local Dockerfile, exercises OpenClaw's OpenShell backend over real `sandbox ssh-config` + SSH exec, and verifies remote-canonical filesystem behavior through the sandbox fs bridge.
- Expectations: opt-in only (not part of the default `pnpm test:e2e` run); requires a local `openshell` CLI plus a working Docker daemon; uses isolated `HOME` / `XDG_CONFIG_HOME`, then destroys the test gateway and sandbox. Overrides: `OPENCLAW_E2E_OPENSHELL=1` (enable within the broader e2e suite) and `OPENCLAW_E2E_OPENSHELL_COMMAND=/path/to/openshell` (non-default CLI binary/wrapper).

### Live (real providers + real models)

- Command: `pnpm test:live` (enabled by default, sets `OPENCLAW_LIVE_TEST=1`); Config: `vitest.live.config.ts`; Files: `src/**/*.live.test.ts`, `test/**/*.live.test.ts`, and bundled-plugin live tests under `extensions/`.
- Scope: "Does this provider/model actually work today with real creds?" — catches provider format changes, tool-calling quirks, auth issues, and rate-limit behavior.
- Expectations: not CI-stable by design (real networks, provider policies, quotas, outages); costs money / uses rate limits; prefer narrowed subsets. Live runs use already-exported API keys and staged auth profiles, and by default isolate `HOME` by copying config/auth material into a temp test home so unit fixtures cannot mutate the real `~/.openclaw` (set `OPENCLAW_LIVE_USE_REAL_HOME=1` only when the real home is intentionally needed). `pnpm test:live` defaults to a quieter mode keeping `[live] ...` progress output (set `OPENCLAW_LIVE_TEST_QUIET=0` for full logs). API-key rotation is provider-specific (`*_API_KEYS` comma/semicolon, `*_API_KEY_1`/`*_API_KEY_2`, or per-live `OPENCLAW_LIVE_*_KEY`); tests retry on rate limits. Tune heartbeats with `OPENCLAW_LIVE_HEARTBEAT_MS` (direct model) and `OPENCLAW_LIVE_GATEWAY_HEARTBEAT_MS` (gateway/probe). The deep model/CLI/ACP/Codex and media live suites are in the sibling live notes.

## Which suite should I run?

The source's decision table:

- Editing logic/tests: run `pnpm test` (and `pnpm test:coverage` for large changes).
- Touching gateway networking / WS protocol / pairing: add `pnpm test:e2e`.
- Debugging "my bot is down" / provider-specific failures / tool calling: run a narrowed `pnpm test:live`.

## Live (network-touching) tests — pointer

For the live model matrix, CLI backend smokes, ACP smokes, the Codex app-server harness, and all media-provider live tests (Deepgram, BytePlus, ComfyUI, image, music, video, media harness) — plus credential handling — the page points to "Testing live suites" (`/help/testing-live`), and for the update/plugin checklist to "Testing updates and plugins" (`/help/testing-updates-plugins`). Both are captured in the sibling notes in Related Notes; this note does not duplicate them.

## Docs sanity

Run docs checks after doc edits: `pnpm check:docs`. Run full Mintlify anchor validation when in-page heading checks are needed: `pnpm docs:check-links:anchors`.

## Offline regression (CI-safe)

"Real pipeline" regressions without real providers, both in `src/gateway/gateway.test.ts`:

- Gateway tool calling (mock OpenAI, real gateway + agent loop) — case: "runs a mock OpenAI tool call end-to-end via gateway agent loop".
- Gateway wizard (WS `wizard.start`/`wizard.next`, writes config + auth enforced) — case: "runs wizard over ws and writes auth token config".

## Agent reliability evals (skills)

A few CI-safe tests already behave like "agent reliability evals": mock tool-calling through the real gateway + agent loop, and end-to-end wizard flows validating session wiring and config effects (both `src/gateway/gateway.test.ts`). Still missing for skills — **Decisioning** (does the agent pick the right skill / avoid irrelevant ones when skills are in the prompt?), **Compliance** (does it read `SKILL.md` before use and follow required steps/args?), and **Workflow contracts** (multi-turn scenarios asserting tool order, session-history carryover, and sandbox boundaries). Future evals should stay deterministic first: a mock-provider scenario runner asserting tool calls + order, skill file reads, and session wiring; a small suite of skill-focused scenarios (use vs avoid, gating, prompt injection); and optional live evals (opt-in, env-gated) only after the CI-safe suite is in place.

## Contract tests (plugin and channel shape)

Contract tests verify that every registered plugin and channel conforms to its interface contract, iterating over all discovered plugins with shape/behavior assertions. The default `pnpm test` unit lane intentionally skips these shared seam/smoke files; run the contract commands explicitly when touching shared channel or provider surfaces.

### Commands

- All contracts: `pnpm test:contracts`
- Channel contracts only: `pnpm test:contracts:channels`
- Provider contracts only: `pnpm test:contracts:plugins`

### Channel contracts

Located in `src/channels/plugins/contracts/*.contract.test.ts`: **plugin** (basic shape — id, name, capabilities), **setup** (setup wizard), **session-binding**, **outbound-payload** (message payload structure), **inbound** (inbound handling), **actions** (channel action handlers), **threading** (thread ID handling), **directory** (directory/roster API), and **group-policy** (group policy enforcement).

### Provider status contracts

Located in `src/plugins/contracts/*.contract.test.ts`: **status** (channel status probes) and **registry** (plugin registry shape).

### Provider contracts

Located in `src/plugins/contracts/*.contract.test.ts`: **auth** (auth flow), **auth-choice** (auth choice/selection), **catalog** (model catalog API), **discovery** (plugin discovery), **loader** (plugin loading), **runtime** (provider runtime), **shape** (plugin shape/interface), and **wizard** (setup wizard).

### When to run

After changing plugin-sdk exports/subpaths, adding or modifying a channel or provider plugin, or refactoring plugin registration or discovery. Contract tests run in CI and do not require real API keys.

## Adding regressions (guidance)

When fixing a provider/model issue found in live: add a CI-safe regression if possible (mock/stub provider, or capture the exact request-shape transformation); if inherently live-only (rate limits, auth policies), keep the live test narrow and opt-in via env vars; prefer the smallest layer that catches the bug — a provider request conversion/replay bug goes to a direct models test, a gateway session/history/tool pipeline bug to a gateway live smoke or CI-safe gateway mock test. SecretRef traversal guardrail: `src/secrets/exec-secret-ref-id-parity.test.ts` derives one sampled target per SecretRef class from registry metadata (`listSecretTargetRegistryEntries()`), then asserts traversal-segment exec ids are rejected; if you add a new `includeInPlan` SecretRef target family in `src/secrets/target-registry-data.ts`, update `classifyTargetClass` in that test (it fails on unclassified target ids so new classes cannot be skipped silently).

**Source**: OpenClaw documentation — `help/testing` (mirror `inbox/openclaw_docs/help/testing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
