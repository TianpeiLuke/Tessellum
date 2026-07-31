---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - qa
keywords:
  - openclaw qa stack
  - qa-channel qa-lab qa-matrix
  - openclaw qa command surface
  - qa run qa suite qa coverage
  - smoke-ci release qa profile
  - qa lab two-pane operator flow
  - observability smoke otel prometheus
  - live transport coverage matrix
topics:
  - OpenClaw
  - QA E2E Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/qa-e2e-automation
access_control_group: ["general"]
---

# OpenClaw — QA End-to-End Automation Overview

## Overview

This note is the concept-level overview of OpenClaw's **private QA stack** — the test harness that exercises OpenClaw in a more realistic, channel-shaped way than a single unit test can. It covers the four moving pieces of the stack (`qa-channel`, `qa-lab`, `qa-matrix`/runner plugins, repo-backed `qa/` seeds, and Mantis), the unified `pnpm openclaw qa <subcommand>` command surface, the two-pane operator flow plus the observability smokes (OpenTelemetry + Prometheus), and the shared live-transport coverage matrix. It mirrors the intro, "Command surface", "Operator flow", and "Live transport coverage" sections of the `concepts/qa-e2e-automation` source page. The per-transport setup details (Telegram/Discord/Slack/WhatsApp lanes, Convex credential pool) live in the sibling live-transports note, and the qa-lab/runner architecture (seeds, provider mocks, transport adapters, reporting) lives in the sibling architecture note.

## What the QA stack is (current pieces)

The private QA stack exercises OpenClaw end to end through channel-shaped behavior rather than isolated units. Its current pieces are: `extensions/qa-channel`, a synthetic message channel with DM, channel, thread, reaction, edit, and delete surfaces; `extensions/qa-lab`, the debugger UI and QA bus for observing the transcript, injecting inbound messages, and exporting a Markdown report; `extensions/qa-matrix` plus future runner plugins, which are live-transport adapters that drive a real channel inside a child QA gateway; `qa/`, the repo-backed seed assets for the kickoff task and baseline QA scenarios; and Mantis, the before-and-after live verification path for bugs that need real transports, browser screenshots, VM state, and PR evidence. Together these let an operator (or an automation loop) give the agent a QA mission, observe real channel behavior, and record what worked, failed, or stayed blocked.

## Command surface

Every QA flow runs under `pnpm openclaw qa <subcommand>`. Many subcommands also have `pnpm qa:*` script aliases; both forms are supported. The core subcommands and their purpose:

- `qa run` — bundled QA self-check without `--qa-profile`; a taxonomy-backed maturity-profile runner with `--qa-profile smoke-ci` or `--qa-profile release`.
- `qa suite` — run repo-backed scenarios against the QA gateway lane (e.g. `pnpm openclaw qa suite --runner multipass` for a disposable Linux VM).
- `qa coverage` — print the YAML scenario-coverage inventory (`--json` for machine output).
- `qa parity-report` — compare two `qa-suite-summary.json` files and write the agentic parity report, or use `--runtime-axis --token-efficiency` for Codex-vs-OpenClaw runtime-parity and token-efficiency reports.
- `qa character-eval` — run the character QA scenario across multiple live models with a judged report.
- `qa manual` — run a one-off prompt against the selected provider/model lane.
- `qa ui` — start the QA debugger UI and local QA bus (alias `pnpm qa:lab:ui`).
- `qa docker-build-image` / `qa docker-scaffold` — build the prebaked QA Docker image / write a docker-compose scaffold for the QA dashboard + gateway lane.
- `qa up` — build the QA site, start the Docker-backed stack, and print the URL (alias `pnpm qa:lab:up`; the `:fast` variant adds `--use-prebuilt-image --bind-ui-dist --skip-ui-build`).
- `qa aimock` / `qa mock-openai` — start only the AIMock provider server / start only the scenario-aware `mock-openai` provider server.
- `qa credentials doctor` / `add` / `list` / `remove` — manage the shared Convex credential pool.
- `qa matrix` / `qa telegram` / `qa discord` / `qa slack` / `qa whatsapp` — live transport lanes (Matrix against a disposable Tuwunel homeserver; the others against pre-existing real transports).
- `qa mantis` — before-and-after verification runner for live transport bugs, with Discord status-reactions evidence, Crabbox desktop/browser smoke, and Slack-in-VNC smoke.

### Profile-backed `qa run`

Profile-backed `qa run` reads membership from `taxonomy.yaml`, then dispatches the resolved scenarios through `qa suite`. `--surface` and `--category` filter the selected profile instead of defining separate lanes. The resulting `qa-evidence.json` includes a profile scorecard summary with selected-category counts and missing coverage IDs; the individual evidence entries remain the source of truth for the tests, coverage roles, and results. Taxonomy feature coverage IDs are exact proof targets, not aliases — primary scenario coverage fulfills matching IDs while secondary coverage stays advisory. Coverage IDs use dotted `namespace.behavior` form with lowercase alphanumeric/dash segments; profile, surface, and category IDs may still use the existing dashed or dotted taxonomy IDs. Slim evidence omits per-entry `execution` and sets `evidenceMode: "slim"`; `smoke-ci` defaults to slim, and `--evidence-mode full` restores full entries. Use `smoke-ci` for deterministic no-live-service proof and `release` for the Stable/LTS proof lane. When a command also needs an OpenClaw root profile, put the root profile before the QA command:

```bash
pnpm openclaw qa run \
  --qa-profile smoke-ci \
  --category agent-runtime-and-provider-execution.agent-turn-execution \
  --provider-mode mock-openai \
  --output-dir .artifacts/qa-e2e/smoke-ci-profile-dispatch

pnpm openclaw --profile work qa run --qa-profile smoke-ci
```

## Operator flow

The current QA operator flow is a two-pane QA site: the **left** pane is the Gateway dashboard (Control UI) with the agent, and the **right** pane is QA Lab, showing the Slack-ish transcript and scenario plan. The site is launched with `pnpm qa:lab:up`, which builds the QA site, starts the Docker-backed gateway lane, and exposes the QA Lab page where an operator or automation loop can give the agent a QA mission, observe real channel behavior, and record what worked, failed, or stayed blocked. For faster QA Lab UI iteration without rebuilding the Docker image each time, the stack can be started with a bind-mounted QA Lab bundle: `qa:lab:up:fast` keeps the Docker services on a prebuilt image and bind-mounts `extensions/qa-lab/web/dist` into the `qa-lab` container, while `qa:lab:watch` rebuilds that bundle on change and the browser auto-reloads when the QA Lab asset hash changes.

```bash
pnpm qa:lab:up

pnpm openclaw qa docker-build-image
pnpm qa:lab:build
pnpm qa:lab:up:fast
pnpm qa:lab:watch
```

### Observability smokes

The operator flow includes dedicated observability smoke lanes. `pnpm qa:otel:smoke` starts a local OTLP/HTTP receiver, runs the `otel-trace-smoke` QA scenario with the `diagnostics-otel` plugin enabled, then asserts traces, metrics, and logs are exported. It decodes the exported protobuf trace spans and checks the release-critical shape — `openclaw.run`, `openclaw.harness.run`, a latest GenAI semantic-convention model-call span, `openclaw.context.assembled`, and `openclaw.message.delivery` must be present. The smoke forces `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, so the model-call span must use the `{gen_ai.operation.name} {gen_ai.request.model}` name; model calls must not export `StreamAbandoned` on successful turns; raw diagnostic IDs and `openclaw.content.*` attributes must stay out of the trace; and the raw OTLP payloads must not contain the prompt sentinel, response sentinel, or QA session key. It writes `otel-smoke-summary.json` next to the QA suite artifacts. `pnpm qa:otel:collector-smoke` puts a real OpenTelemetry Collector Docker container in front of the same local receiver — used when changing endpoint wiring, collector compatibility, or OTLP export behavior the in-process receiver could mask. `pnpm qa:prometheus:smoke` runs the `docker-prometheus-smoke` QA scenario with `diagnostics-prometheus` enabled, verifies unauthenticated scrapes are rejected, then checks the authenticated scrape includes release-critical metric families without prompt content, response content, raw diagnostic identifiers, auth tokens, or local paths. `pnpm qa:observability:smoke` runs both observability smokes back to back, and `pnpm qa:observability:collector-smoke` runs the collector-backed OpenTelemetry lane plus the protected Prometheus scrape smoke.

```bash
pnpm qa:otel:smoke
pnpm qa:prometheus:smoke
pnpm qa:observability:smoke
```

Observability QA stays source-checkout only: the npm tarball intentionally omits QA Lab, so package Docker release lanes do not run `qa` commands. Use `pnpm qa:otel:smoke`, `pnpm qa:prometheus:smoke`, or `pnpm qa:observability:smoke` from a built source checkout when changing diagnostics instrumentation. CI uses the same command surface in `.github/workflows/qa-live-transports-convex.yml`; scheduled and default manual runs execute the fast Matrix profile with live frontier credentials, `--fast`, and `OPENCLAW_QA_MATRIX_NO_REPLY_WINDOW_MS=3000`, and manual `matrix_profile=all` fans out into the five profile shards so the exhaustive catalog runs in parallel with one artifact directory per shard.

## Live transport coverage

Live transport lanes share **one contract** instead of each inventing their own scenario-list shape; `qa-channel` is the broad synthetic product-behavior suite and is *not* part of the live transport coverage matrix. Live transport runners should import the shared scenario ids, baseline coverage helpers, and scenario-selection helper from `openclaw/plugin-sdk/qa-live-transport-scenarios`. The shared transport-contract checklist (an `x` marks coverage) is:

| Lane | Canary | Mention gating | Bot-to-bot | Allowlist block | Top-level reply | Restart resume | Thread follow-up | Thread isolation | Reaction observation | Help command | Native command registration |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Matrix | x | x | x | x | x | x | x | x | x | | |
| Telegram | x | x | x | | | | | | | x | |
| Discord | x | x | x | | | | | | | | x |
| Slack | x | x | x | x | x | x | x | x | | | |
| WhatsApp | x | x | | x | x | x | | | x | x | |

This keeps `qa-channel` as the broad product-behavior suite while Matrix, Telegram, and the other live transports share one explicit transport-contract checklist. For a disposable Linux VM lane without bringing Docker into the QA path, `pnpm openclaw qa suite --runner multipass --scenario channel-chat-baseline` boots a fresh Multipass guest, installs dependencies, builds OpenClaw inside the guest, runs `qa suite`, then copies the normal QA report and summary back into `.artifacts/qa-e2e/...` on the host, reusing the same scenario-selection behavior as `qa suite` on the host. Host and Multipass suite runs execute multiple selected scenarios in parallel with isolated gateway workers by default (`qa-channel` defaults to concurrency 4, capped by the selected scenario count; tune with `--concurrency <count>` or `--concurrency 1` for serial). `--pack personal-agent` runs the personal-assistant benchmark pack (the pack selector is additive with repeated `--scenario` flags — explicit scenarios run first, then pack scenarios run in pack order with duplicates removed), and `--pack observability` selects the OpenTelemetry and Prometheus diagnostics smoke scenarios together when a custom runner already supplies the collector setup. The command exits non-zero when any scenario fails; use `--allow-failures` to get artifacts without a failing exit code.

**Source**: OpenClaw documentation — `concepts/qa-e2e-automation` (mirror `inbox/openclaw_docs/concepts/qa-e2e-automation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
