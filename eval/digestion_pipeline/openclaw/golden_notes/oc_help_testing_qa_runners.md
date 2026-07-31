---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - qa_runners
keywords:
  - openclaw qa lab runners
  - pnpm openclaw qa suite
  - qa coverage matrix telegram
  - convex credential broker lease
  - mantis pr evidence wrapper
  - shared telegram credentials convex
  - qa-evidence json scorecard
  - adding a channel to qa
topics:
  - OpenClaw
  - QA Lab Runners
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/testing
access_control_group: ["general"]
---

# OpenClaw — QA-Lab Runners and the Convex Credential Broker

## Overview

This note is the operator procedure for OpenClaw's **QA-lab runner surface**: the `pnpm openclaw qa …` commands that exercise OpenClaw under live (or mock) transport realism, the `Mantis` PR-evidence wrappers, and the Convex-backed shared-credential broker that leases channel credentials for live transport QA. It mirrors the `QA-specific runners`, `Shared Telegram credentials via Convex (v1)`, and `Adding a channel to QA` sections of the `help/testing` source page (the sibling `oc_help_testing_suites.md` covers the Vitest suite taxonomy, `oc_help_testing_docker_runners.md` the Docker catalog). QA Lab ships only in a source checkout — packaged installs do not ship `qa-lab`.

## Where QA runs in CI

CI runs QA Lab in dedicated workflows; agentic parity is nested under `QA-Lab - All Lanes` and release validation, not a standalone PR workflow. Broad validation uses `Full Release Validation` with `rerun_group=qa-parity` or the release-checks QA group, and exhaustive live/Docker soak stays behind `run_release_soak=true` (the `full` profile forces soak on). `QA-Lab - All Lanes` runs nightly on `main` and from manual dispatch with the mock parity lane, live Matrix lane, and Convex-managed live Telegram and Discord lanes as parallel jobs. Scheduled QA and release checks pass Matrix `--profile fast` (the CLI/manual default stays `all`, shardable into `transport`/`media`/`e2ee-smoke`/`e2ee-deep`/`e2ee-cli`). `OpenClaw Release Checks` runs parity plus the fast Matrix and Telegram lanes using `mock-openai/gpt-5.5` so release transport checks stay deterministic; these live transport gateways disable memory search (covered by QA parity suites). Full release live-media shards use `ghcr.io/openclaw/openclaw-live-media-runner:ubuntu-24.04`; Docker live model/backend shards use the shared `ghcr.io/openclaw/openclaw-live-test:<sha>` image built once per commit, then pulled with `OPENCLAW_SKIP_DOCKER_BUILD=1`.

## QA-lab runner commands

These commands sit beside the main test suites when you need QA-lab realism:

- `pnpm openclaw qa suite` — runs repo-backed QA scenarios directly on the host, writing top-level `qa-evidence.json`, `qa-suite-summary.json`, and `qa-suite-report.md` for the selected scenario set (mixed flow, Vitest, Playwright). When dispatched by `pnpm openclaw qa run --qa-profile <profile>` it embeds the selected taxonomy profile scorecard in the same `qa-evidence.json` (`smoke-ci` writes slim evidence, `evidenceMode: "slim"`). It runs selected scenarios in parallel by default with isolated gateway workers — `qa-channel` defaults to concurrency 4 (tune with `--concurrency <count>`, or `--concurrency 1` for serial). It exits non-zero on any failure (`--allow-failures` for artifacts without a failing exit), and supports provider modes `live-frontier`, `mock-openai`, and `aimock` (`aimock` starts a local AIMock-backed provider server for experimental fixture/protocol-mock coverage without replacing the scenario-aware `mock-openai` lane).
- `pnpm openclaw qa coverage --match <query>` — searches scenario IDs, titles, surfaces, coverage IDs, docs refs, code refs, plugins, and provider requirements, then prints matching suite targets. Use it before a run when you know the touched behavior but not the smallest scenario; it is advisory only — still pick mock/live/Multipass/Matrix/transport proof from the behavior being changed.
- `pnpm openclaw qa suite --runner multipass` — runs the same QA suite inside a disposable Multipass Linux VM, keeping the same scenario-selection and provider/model flags as `qa suite`. Live runs forward the QA auth inputs practical for the guest (env-based provider keys, the QA live provider config path, `CODEX_HOME` when present); output dirs must stay under the repo root so the guest can write back through the mounted workspace. Writes the normal QA report + summary plus Multipass logs under `.artifacts/qa-e2e/...`.
- `pnpm openclaw qa aimock` — starts only the local AIMock provider server for direct protocol smoke testing.
- `pnpm openclaw qa matrix` — runs the Matrix live QA lane against a disposable Docker-backed Tuwunel homeserver (source-checkout only). Full CLI, profile/scenario catalog, env vars, and artifact layout live in [Matrix QA](https://docs.openclaw.ai/concepts/qa-matrix).
- `pnpm qa:lab:up` — starts the Docker-backed QA site for operator-style QA.

### Telegram live QA lane

`pnpm openclaw qa telegram` runs the Telegram live QA lane against a real private group using the driver and SUT bot tokens from env. It requires `OPENCLAW_QA_TELEGRAM_GROUP_ID`, `OPENCLAW_QA_TELEGRAM_DRIVER_BOT_TOKEN`, and `OPENCLAW_QA_TELEGRAM_SUT_BOT_TOKEN` (group id must be the numeric Telegram chat id), and supports `--credential-source convex` for shared pooled credentials (default env mode, or `OPENCLAW_QA_CREDENTIAL_SOURCE=convex` to opt into pooled leases). Defaults cover canary, mention gating, command addressing, `/status`, bot-to-bot mentioned replies, and core native command replies; `mock-openai` defaults add deterministic reply-chain and Telegram final-message streaming regressions (`--list-scenarios` for optional probes such as `session_status`). It exits non-zero on any failure (`--allow-failures` for artifacts without a failing exit), requires two distinct bots in the same private group with the SUT bot exposing a Telegram username, and needs Bot-to-Bot Communication Mode enabled in `@BotFather` for stable bot-to-bot observation. It writes a Telegram QA report, summary, and `qa-evidence.json` under `.artifacts/qa-e2e/...`; replying scenarios include RTT from driver send to observed SUT reply.

### Mantis PR-evidence wrappers

`Mantis Telegram Live` is the PR-evidence wrapper around the Telegram lane. It runs the candidate ref with Convex-leased Telegram credentials, renders the redacted QA report/evidence bundle in a Crabbox desktop browser, records MP4 evidence, generates a motion-trimmed GIF, uploads the bundle, and posts inline PR evidence through the Mantis GitHub App when `pr_number` is set. Maintainers start it from the Actions UI through `Mantis Scenario` (`scenario_id: telegram-live`) or from a PR comment:

```text
@openclaw-mantis telegram
@openclaw-mantis telegram scenario=telegram-status-command
@openclaw-mantis telegram scenarios=telegram-status-command,telegram-mentioned-message-reply
```

`Mantis Telegram Desktop Proof` is the agentic native Telegram Desktop before/after wrapper for PR visual proof, started from the Actions UI with freeform `instructions`, through `Mantis Scenario` (`scenario_id: telegram-desktop-proof`), or from the PR comment `@openclaw-mantis telegram desktop proof`. The Mantis agent reads the PR, decides what Telegram-visible behavior proves the change, runs the real-user Crabbox Telegram Desktop proof lane on baseline and candidate refs, iterates until the native GIFs are useful, writes a paired `motionPreview` manifest, and posts the same 2-column GIF table through the Mantis GitHub App when `pr_number` is set.

`pnpm openclaw qa mantis telegram-desktop-builder` leases or reuses a Crabbox Linux desktop, installs native Telegram Desktop, configures OpenClaw with a leased Telegram SUT bot token, starts the gateway, and records screenshot/MP4 evidence from the visible VNC desktop. It defaults to `--credential-source convex`; use `--credential-source env` with the same `OPENCLAW_QA_TELEGRAM_*` variables. Telegram Desktop still needs a user login/profile (the bot token configures OpenClaw only) — use `--telegram-profile-archive-env <name>` for a base64 `.tgz` profile archive, or `--keep-lease` and log in manually through VNC once. It writes `mantis-telegram-desktop-builder-report.md`, `mantis-telegram-desktop-builder-summary.json`, `telegram-desktop-builder.png`, and `telegram-desktop-builder.mp4` under the output directory.

### Kitchen-sink, CPU, and packaged-install QA lanes

- `pnpm test:plugins:kitchen-sink-live` — runs the live OpenAI Kitchen Sink plugin gauntlet through QA Lab: installs the external Kitchen Sink package, verifies the plugin SDK surface inventory, probes `/healthz` and `/readyz`, records gateway CPU/RSS evidence, runs a live OpenAI turn, and checks adversarial diagnostics. It requires live OpenAI auth such as `OPENAI_API_KEY` (in hydrated Testbox sessions it auto-sources the Testbox live-auth profile when `openclaw-testbox-env` is present).
- `pnpm test:gateway:cpu-scenarios` — runs the gateway startup bench plus a small mock QA Lab scenario pack (`channel-chat-baseline`, `memory-failure-fallback`, `gateway-restart-inflight-run`) and writes a combined CPU summary under `.artifacts/gateway-cpu-scenarios/`. It flags only sustained hot CPU observations by default (`--cpu-core-warn` plus `--hot-wall-warn-ms`) so short startup bursts stay metrics, not the minutes-long gateway peg regression. It uses built `dist` artifacts (build first when the checkout lacks fresh runtime output).
- `pnpm test:docker:npm-telegram-live` — installs an OpenClaw package candidate in Docker, runs installed-package onboarding, configures Telegram through the installed CLI, then reuses the live Telegram QA lane with that installed package as the SUT Gateway (mounting only the `qa-lab` harness source; the installed package owns `dist`/`openclaw/plugin-sdk`/bundled plugin runtime). It defaults to `OPENCLAW_NPM_TELEGRAM_PACKAGE_SPEC=openclaw@beta` (override with `OPENCLAW_NPM_TELEGRAM_PACKAGE_TGZ` / `OPENCLAW_CURRENT_PACKAGE_TGZ`) and emits repeated RTT in `qa-evidence.json` via `OPENCLAW_NPM_TELEGRAM_RTT_SAMPLES=20` (default check `telegram-mentioned-message-reply`). It shares the same env/Convex credential source as `pnpm openclaw qa telegram` (`OPENCLAW_NPM_TELEGRAM_CREDENTIAL_SOURCE=convex` plus `OPENCLAW_QA_CONVEX_SITE_URL` and a role secret for CI). GitHub Actions exposes it as the manual maintainer workflow `NPM Telegram Beta E2E` (does not run on merge).

Live transport lanes share one standard contract so new transports do not drift; the per-lane coverage matrix lives in [QA overview → Live transport coverage](https://docs.openclaw.ai/concepts/qa-e2e-automation#live-transport-coverage). `qa-channel` is the broad synthetic suite, not part of that matrix.

## Shared Telegram credentials via Convex (v1)

When `--credential-source convex` (or `OPENCLAW_QA_CREDENTIAL_SOURCE=convex`) is enabled for live transport QA, QA lab acquires an exclusive lease from a Convex-backed pool, heartbeats that lease while the lane runs, and releases it on shutdown. The section name predates Discord, Slack, and WhatsApp support; the lease contract is shared across kinds. Reference Convex project scaffold: `qa/convex-credential-broker/`.

Required env vars: `OPENCLAW_QA_CONVEX_SITE_URL` (e.g. `https://your-deployment.convex.site`); one role secret — `OPENCLAW_QA_CONVEX_SECRET_MAINTAINER` for `maintainer` or `OPENCLAW_QA_CONVEX_SECRET_CI` for `ci`; and role selection via CLI `--credential-role maintainer|ci` or env `OPENCLAW_QA_CREDENTIAL_ROLE` (defaults to `ci` in CI, `maintainer` otherwise). Optional env vars: `OPENCLAW_QA_CREDENTIAL_LEASE_TTL_MS` (default `1200000`), `OPENCLAW_QA_CREDENTIAL_HEARTBEAT_INTERVAL_MS` (default `30000`), `OPENCLAW_QA_CREDENTIAL_ACQUIRE_TIMEOUT_MS` (default `90000`), `OPENCLAW_QA_CREDENTIAL_HTTP_TIMEOUT_MS` (default `15000`), `OPENCLAW_QA_CONVEX_ENDPOINT_PREFIX` (default `/qa-credentials/v1`), `OPENCLAW_QA_CREDENTIAL_OWNER_ID` (optional trace id), and `OPENCLAW_QA_ALLOW_INSECURE_HTTP=1` (allows loopback `http://` Convex URLs for local-only dev). `OPENCLAW_QA_CONVEX_SITE_URL` should use `https://` in normal operation, and admin commands (pool add/remove/list) require `OPENCLAW_QA_CONVEX_SECRET_MAINTAINER` specifically.

CLI helpers for maintainers:

```bash
pnpm openclaw qa credentials doctor
pnpm openclaw qa credentials add --kind telegram --payload-file qa/telegram-credential.json
pnpm openclaw qa credentials list --kind telegram
pnpm openclaw qa credentials remove --credential-id <credential-id>
```

Use `doctor` before live runs to check the Convex site URL, broker secrets, endpoint prefix, HTTP timeout, and admin/list reachability without printing secret values (`--json` for machine-readable output in scripts/CI).

### Broker endpoint contract

The default endpoint contract is `OPENCLAW_QA_CONVEX_SITE_URL` + `/qa-credentials/v1`:

- `POST /acquire` — `{ kind, ownerId, actorRole, leaseTtlMs, heartbeatIntervalMs }` → `{ status: "ok", credentialId, leaseToken, payload, leaseTtlMs?, heartbeatIntervalMs? }`; exhausted/retryable → `{ status: "error", code: "POOL_EXHAUSTED" | "NO_CREDENTIAL_AVAILABLE", ... }`.
- `POST /payload-chunk` — `{ kind, ownerId, actorRole, credentialId, leaseToken, index }` → `{ status: "ok", index, data }`.
- `POST /heartbeat` — `{ kind, ownerId, actorRole, credentialId, leaseToken, leaseTtlMs }` → `{ status: "ok" }` (or empty `2xx`).
- `POST /release` — `{ kind, ownerId, actorRole, credentialId, leaseToken }` → `{ status: "ok" }` (or empty `2xx`).
- `POST /admin/add` (maintainer secret only) — `{ kind, actorId, payload, note?, status? }` → `{ status: "ok", credential }`.
- `POST /admin/remove` (maintainer secret only) — `{ credentialId, actorId }` → `{ status: "ok", changed, credential }`; active lease guard → `{ status: "error", code: "LEASE_ACTIVE", ... }`.
- `POST /admin/list` (maintainer secret only) — `{ kind?, status?, includePayload?, limit? }` → `{ status: "ok", credentials, count }`.

### Per-channel payload shapes

Telegram kind: `{ groupId: string, driverToken: string, sutToken: string }` (`groupId` numeric chat id; `admin/add` validates this shape for `kind: "telegram"` and rejects malformed payloads). Telegram real-user kind: `{ groupId: string, sutToken: string, testerUserId: string, testerUsername: string, telegramApiId: string, telegramApiHash: string, tdlibDatabaseEncryptionKey: string, tdlibArchiveBase64: string, tdlibArchiveSha256: string, desktopTdataArchiveBase64: string, desktopTdataArchiveSha256: string }` — `groupId`/`testerUserId`/`telegramApiId` numeric strings, `tdlibArchiveSha256`/`desktopTdataArchiveSha256` SHA-256 hex; `kind: "telegram-user"` is reserved for the Mantis Telegram Desktop proof workflow (generic QA Lab lanes must not acquire it).

Broker-validated multi-channel payloads — Discord: `{ guildId: string, channelId: string, driverBotToken: string, sutBotToken: string, sutApplicationId: string, voiceChannelId?: string }`; WhatsApp: `{ driverPhoneE164: string, sutPhoneE164: string, driverAuthArchiveBase64: string, sutAuthArchiveBase64: string, groupJid?: string }`. Slack lanes can also lease from the pool, but Slack payload validation currently lives in the Slack QA runner rather than the broker — use `{ channelId: string, driverBotToken: string, sutBotToken: string, sutAppToken: string }`.

## Adding a channel to QA

The architecture and scenario-helper names for new channel adapters live in [QA overview → Adding a channel](https://docs.openclaw.ai/concepts/qa-e2e-automation#adding-a-channel). Minimum bar: implement the transport runner on the shared `qa-lab` host seam, declare `qaRunners` in the plugin manifest, mount as `openclaw qa <runner>`, and author scenarios under `qa/scenarios/`.

**Source**: OpenClaw documentation — `help/testing` (QA-specific runners · Shared Telegram credentials via Convex (v1) · Adding a channel to QA) (mirror `inbox/openclaw_docs/help/testing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
