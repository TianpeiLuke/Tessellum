---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - testing
keywords:
  - openclaw docker test runners
  - test:docker:all weighted scheduler
  - test:docker:live-models live-gateway
  - container smoke runners
  - docker e2e image overrides
  - bind-mount cli auth home
  - openclaw_live env vars docker
  - gateway-network browser-cdp mcp-channels
topics:
  - OpenClaw
  - Testing
  - Docker Runners
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/testing
access_control_group: ["general"]
---

# OpenClaw — Docker Test Runners ("Works in Linux" Checks)

## Overview

This note is the procedure catalog for OpenClaw's optional Docker test runners — the `pnpm test:docker:*` lanes that pack the repo as an npm tarball, build/reuse Docker images, and run install/update/plugin/live/container-smoke checks inside Linux containers. It mirrors the `## Docker runners (optional "works in Linux" checks)` section of the `help/testing` source page only (the suite taxonomy, QA-lab runners, and live-model/credential details are sibling notes). It covers the two runner buckets (live-model vs functional/bare image), the weighted `test:docker:all` aggregate scheduler, the full container-smoke runner list, the shared-image override conventions, the read-only bind-mount + auth-home staging model, and the `OPENCLAW_*` env vars that narrow or tune Docker runs.

## Two Docker runner buckets

The Docker runners split into two buckets. **Live-model runners** — `test:docker:live-models` and `test:docker:live-gateway` — run only their matching profile-key live file inside the repo Docker image (`src/agents/models.profiles.live.test.ts` and `src/gateway/gateway-models.profiles.live.test.ts` respectively), mounting your local config dir, workspace, and optional profile env file; the matching local entrypoints are `test:live:models-profiles` and `test:live:gateway-profiles`. These live runners keep their own practical caps: `test:docker:live-models` defaults to the curated supported high-signal set, and `test:docker:live-gateway` defaults to `OPENCLAW_LIVE_GATEWAY_SMOKE=1`, `OPENCLAW_LIVE_GATEWAY_MAX_MODELS=8`, `OPENCLAW_LIVE_GATEWAY_STEP_TIMEOUT_MS=45000`, and `OPENCLAW_LIVE_GATEWAY_MODEL_TIMEOUT_MS=90000` — set `OPENCLAW_LIVE_MAX_MODELS` or the gateway env vars when you explicitly want a smaller cap or larger scan.

The live-model Docker runners also bind-mount only the needed CLI auth homes (or all supported ones when the run is not narrowed), then copy them into the container home before the run so external-CLI OAuth can refresh tokens without mutating the host auth store. The live-model entry scripts are:

- Direct models: `pnpm test:docker:live-models` (script: `scripts/test-live-models-docker.sh`).
- ACP bind smoke: `pnpm test:docker:live-acp-bind` (script: `scripts/test-live-acp-bind-docker.sh`; covers Claude, Codex, and Gemini by default, with strict Droid/OpenCode coverage via `pnpm test:docker:live-acp-bind:droid` and `pnpm test:docker:live-acp-bind:opencode`).
- CLI backend smoke: `pnpm test:docker:live-cli-backend` (script: `scripts/test-live-cli-backend-docker.sh`).
- Codex app-server harness smoke: `pnpm test:docker:live-codex-harness` (script: `scripts/test-live-codex-harness-docker.sh`).
- Gateway + dev agent: `pnpm test:docker:live-gateway` (script: `scripts/test-live-gateway-models-docker.sh`).

## The `test:docker:all` aggregate scheduler

`test:docker:all` builds the live Docker image once via `test:docker:live-build`, packs OpenClaw once as an npm tarball through `scripts/package-openclaw-for-docker.mjs`, then builds/reuses two `scripts/e2e/Dockerfile` images. The **bare image** is only the Node/Git runner for install/update/plugin-dependency lanes (those lanes mount the prebuilt tarball); the **functional image** installs the same tarball into `/app` for built-app functionality lanes. Docker lane definitions live in `scripts/lib/docker-e2e-scenarios.mjs`, planner logic lives in `scripts/lib/docker-e2e-plan.mjs`, and `scripts/test-docker-all.mjs` executes the selected plan.

The aggregate uses a weighted local scheduler: `OPENCLAW_DOCKER_ALL_PARALLELISM` controls process slots, while resource caps keep heavy live, npm-install, and multi-service lanes from all starting at once. If a single lane is heavier than the active caps, the scheduler can still start it when the pool is empty and then keeps it running alone until capacity is available again. Defaults are 10 slots, `OPENCLAW_DOCKER_ALL_LIVE_LIMIT=9`, `OPENCLAW_DOCKER_ALL_NPM_LIMIT=5`, and `OPENCLAW_DOCKER_ALL_SERVICE_LIMIT=7`; tune `OPENCLAW_DOCKER_ALL_WEIGHT_LIMIT` or `OPENCLAW_DOCKER_ALL_DOCKER_LIMIT` only when the Docker host has more headroom. The runner performs a Docker preflight by default, removes stale OpenClaw E2E containers, prints status every 30 seconds, stores successful lane timings in `.artifacts/docker-tests/lane-timings.json`, and uses those timings to start longer lanes first on later runs. Use `OPENCLAW_DOCKER_ALL_DRY_RUN=1` to print the weighted lane manifest without building or running Docker, or `node scripts/test-docker-all.mjs --plan-json` to print the CI plan for selected lanes, package/image needs, and credentials.

Two related lanes sit beside the aggregate. `Package Acceptance` is the GitHub-native package gate for "does this installable tarball work as a product?" — it resolves one candidate package from `source=npm`, `source=ref`, `source=url`, or `source=artifact`, uploads it as `package-under-test`, then runs the reusable Docker E2E lanes against that exact tarball instead of repacking the selected ref; profiles are ordered by breadth: `smoke`, `package`, `product`, and `full` (the package/update/plugin contract and failure triage live in the sibling updates-and-plugins note). Build and release checks run `scripts/check-cli-bootstrap-imports.mjs` after tsdown — the guard walks the static built graph from `dist/entry.js` and `dist/cli/run-main.js` and fails if pre-dispatch startup imports package dependencies such as Commander, prompt UI, undici, or logging before command dispatch, also keeping the bundled gateway run chunk under budget and rejecting static imports of known cold gateway paths; packaged CLI smoke also covers root help, onboard help, doctor help, status, config schema, and a model-list command. Package Acceptance legacy compatibility is capped at `2026.4.25` (`2026.4.25-beta.*` included): through that cutoff the harness tolerates only shipped-package metadata gaps (omitted private QA inventory entries, missing `gateway install --wrapper`, missing patch files in the tarball-derived git fixture, missing persisted `update.channel`, legacy plugin install-record locations, missing marketplace install-record persistence, and config metadata migration during `plugins update`); for packages after `2026.4.25`, those paths are strict failures.

Docker/Bash E2E lanes that install the packed OpenClaw tarball through `scripts/lib/openclaw-e2e-instance.sh` cap `npm install` at `OPENCLAW_E2E_NPM_INSTALL_TIMEOUT` (default `600s`; set `0` to disable the wrapper for debugging).

## Container smoke runners

A large family of container smoke runners boot one or more real containers and verify higher-level integration paths: `test:docker:openwebui`, `test:docker:onboard`, `test:docker:npm-onboard-channel-agent`, `test:docker:release-user-journey`, `test:docker:release-typed-onboarding`, `test:docker:release-media-memory`, `test:docker:release-upgrade-user-journey`, `test:docker:release-plugin-marketplace`, `test:docker:skill-install`, `test:docker:update-channel-switch`, `test:docker:upgrade-survivor`, `test:docker:published-upgrade-survivor`, `test:docker:session-runtime-context`, `test:docker:agents-delete-shared-workspace`, `test:docker:gateway-network`, `test:docker:browser-cdp-snapshot`, `test:docker:mcp-channels`, `test:docker:agent-bundle-mcp-tools`, `test:docker:cron-mcp-cleanup`, `test:docker:plugins`, `test:docker:plugin-update`, `test:docker:plugin-lifecycle-matrix`, and `test:docker:config-reload`.

Highlights of what each verifies (grounded in source):

- **Onboarding / release journeys** — `test:docker:npm-onboard-channel-agent` installs the packed tarball globally, configures OpenAI via env-ref onboarding plus Telegram by default, runs doctor, and runs one mocked OpenAI agent turn (switch channel with `OPENCLAW_NPM_ONBOARD_CHANNEL=discord` or `=slack`). `test:docker:release-user-journey` runs onboarding, mocked provider, an agent turn, plugin install/uninstall, ClickClack against a local fixture, outbound/inbound messaging, Gateway restart, and doctor. `test:docker:release-typed-onboarding` drives `openclaw onboard` through a real TTY and verifies no raw key persistence. `test:docker:release-media-memory` verifies PNG image understanding, OpenAI-compatible image generation output, and memory-search recall surviving a Gateway restart.
- **Upgrade survivors** — `test:docker:upgrade-survivor` installs over a dirty old-user fixture and runs package update plus non-interactive doctor without live keys. `test:docker:published-upgrade-survivor` installs `openclaw@latest` by default, seeds existing-user files, updates to the candidate tarball, runs doctor, writes `.artifacts/upgrade-survivor/summary.json`, then checks `/healthz`, `/readyz`, and RPC status budgets; override one baseline with `OPENCLAW_UPGRADE_SURVIVOR_BASELINE_SPEC`, expand exact local baselines with `OPENCLAW_UPGRADE_SURVIVOR_BASELINE_SPECS`, and expand issue-shaped fixtures with `OPENCLAW_UPGRADE_SURVIVOR_SCENARIOS` (the `reported-issues` set includes `configured-plugin-installs`).
- **Network / browser / MCP** — `test:docker:gateway-network` runs two containers checking WS auth + health. `test:docker:browser-cdp-snapshot` builds a Chromium layer, runs `browser doctor --deep`, and verifies CDP role snapshots cover link URLs, cursor-promoted clickables, iframe refs, and frame metadata. `test:docker:mcp-channels`, `test:docker:agent-bundle-mcp-tools`, and `test:docker:cron-mcp-cleanup` are deterministic stdio-MCP lanes (no live model key needed) that exercise the MCP channel bridge, embedded bundle-MCP tool allow/deny (`coding`/`messaging` keep `bundle-mcp`; `minimal` and `tools.deny: ["bundle-mcp"]` filter them), and stdio-MCP child teardown after cron + `sessions_spawn` one-shot subagent runs.
- **Plugin lanes** — `test:docker:plugins` covers install/update smoke for local path, `file:`, npm registry with hoisted dependencies, git moving refs, ClawHub fixtures, marketplace updates, and Claude-bundle enable/inspect (skip the ClawHub block with `OPENCLAW_PLUGINS_E2E_CLAWHUB=0`). `test:docker:plugin-update` covers unchanged update behavior; `test:docker:plugin-lifecycle-matrix` covers resource-tracked npm plugin install, enable, disable, upgrade, downgrade, and missing-code uninstall.

Adjacent non-`pnpm` smoke lanes include `bash scripts/e2e/bun-global-install-smoke.sh` (packs + `bun install -g` in an isolated home, verifies `openclaw infer image providers --json`) and `bash scripts/test-install-sh-docker.sh` (shares one npm cache across root/update/direct-npm containers; override the update baseline with `OPENCLAW_INSTALL_SMOKE_UPDATE_BASELINE=2026.4.22`). A manual, non-CI ACP plain-language thread smoke also exists: `bun scripts/dev/discord-acp-plain-language-smoke.ts --channel <discord-channel-id> ...` (kept for ACP thread-routing regression/debug — do not delete).

## Shared functional image overrides

To prebuild and reuse the shared functional image manually:

```bash
OPENCLAW_DOCKER_E2E_IMAGE=openclaw-docker-e2e-functional:local pnpm test:docker:e2e-build
OPENCLAW_DOCKER_E2E_IMAGE=openclaw-docker-e2e-functional:local OPENCLAW_SKIP_DOCKER_BUILD=1 pnpm test:docker:mcp-channels
```

Suite-specific image overrides such as `OPENCLAW_GATEWAY_NETWORK_E2E_IMAGE` still win when set. When `OPENCLAW_SKIP_DOCKER_BUILD=1` points at a remote shared image, the scripts pull it if it is not already local. The QR and installer Docker tests keep their own Dockerfiles because they validate package/install behavior rather than the shared built-app runtime.

The live-model Docker runners also bind-mount the current checkout read-only and stage it into a temporary workdir inside the container, keeping the runtime image slim while still running Vitest against your exact local source/config. The staging step skips large local-only caches and app build outputs such as `.pnpm-store`, `.worktrees`, `__openclaw_vitest__`, and app-local `.build` or Gradle output directories so Docker live runs do not spend minutes copying machine-specific artifacts. They also set `OPENCLAW_SKIP_CHANNELS=1` so gateway live probes do not start real Telegram/Discord/etc. channel workers inside the container; `test:docker:live-models` still runs `pnpm test:live`, so pass through `OPENCLAW_LIVE_GATEWAY_*` as well when you need to narrow or exclude gateway live coverage from that Docker lane.

## Bind-mounts, auth-home staging, and env vars

External CLI auth dirs/files under `$HOME` are mounted read-only under `/host-auth...`, then copied into `/home/node/...` before tests start. The default mounted dir is `.minimax`; the default files are `~/.codex/auth.json`, `~/.codex/config.toml`, `.claude.json`, `~/.claude/.credentials.json`, `~/.claude/settings.json`, `~/.claude/settings.local.json`. Narrowed provider runs mount only the needed dirs/files inferred from `OPENCLAW_LIVE_PROVIDERS` / `OPENCLAW_LIVE_GATEWAY_PROVIDERS`, and you can override manually with `OPENCLAW_DOCKER_AUTH_DIRS=all`, `OPENCLAW_DOCKER_AUTH_DIRS=none`, or a comma list like `OPENCLAW_DOCKER_AUTH_DIRS=.claude,.codex`. The useful Docker-runner env vars are:

```bash
OPENCLAW_CONFIG_DIR=...            # default ~/.openclaw → mounted to /home/node/.openclaw
OPENCLAW_WORKSPACE_DIR=...         # default ~/.openclaw/workspace → /home/node/.openclaw/workspace
OPENCLAW_PROFILE_FILE=...          # mounted and sourced before running tests
OPENCLAW_DOCKER_PROFILE_ENV_ONLY=1 # verify only env vars from OPENCLAW_PROFILE_FILE (temp dirs, no external CLI auth mounts)
OPENCLAW_DOCKER_CLI_TOOLS_DIR=...  # default ~/.cache/openclaw/docker-cli-tools → /home/node/.npm-global
OPENCLAW_LIVE_GATEWAY_MODELS=...   # / OPENCLAW_LIVE_MODELS=... narrow the run
OPENCLAW_LIVE_GATEWAY_PROVIDERS=...# / OPENCLAW_LIVE_PROVIDERS=... filter providers in-container
OPENCLAW_SKIP_DOCKER_BUILD=1       # reuse an existing openclaw:local-live image for reruns
OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1 # ensure creds come from the profile store (not env)
OPENCLAW_OPENWEBUI_MODEL=...       # model exposed by the gateway for the Open WebUI smoke
OPENCLAW_OPENWEBUI_PROMPT=...      # override the nonce-check prompt for the Open WebUI smoke
OPENWEBUI_IMAGE=...                # override the pinned Open WebUI image tag
```

The `test:docker:openwebui` lane is a higher-level compatibility smoke: it starts an OpenClaw gateway container with the OpenAI-compatible HTTP endpoints enabled, starts a pinned Open WebUI container against that gateway, signs in, verifies `/api/models` exposes `openclaw/default`, then sends a real chat request through Open WebUI's `/api/chat/completions` proxy (set `OPENWEBUI_SMOKE_MODE=models` for release-path CI checks that stop after sign-in and model discovery; this lane expects a usable live model key, provided via the process environment, staged auth profiles, or an explicit `OPENCLAW_PROFILE_FILE`).

**Source**: OpenClaw documentation — `help/testing` (mirror `inbox/openclaw_docs/help/testing.md`), `## Docker runners (optional "works in Linux" checks)` section
**Last Updated**: 2026-06-22
**Status**: Active
