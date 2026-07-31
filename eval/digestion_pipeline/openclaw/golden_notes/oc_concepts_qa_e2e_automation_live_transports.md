---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - qa
keywords:
  - openclaw qa operator flow
  - qa lab dashboard
  - observability smoke otel prometheus
  - live transport coverage matrix
  - multipass qa runner
  - qa mantis visual task
  - qa credentials doctor
topics:
  - OpenClaw
  - QA Automation
language: markdown
date of note: 2026-06-23
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/qa-e2e-automation
access_control_group: ["general"]
---

# OpenClaw — QA Operator Flow, Observability & Live-Transport Coverage

## Overview

This note is the operator-flow procedure half of the `concepts/qa-e2e-automation` page: how to run the QA Lab two-pane site, the OpenTelemetry/Prometheus observability smokes, the Matrix/Multipass lanes, the Mantis desktop/visual runs, and the shared live-transport coverage matrix. The per-channel **Telegram/Discord/Slack/WhatsApp** env, scenario lists, app setup, and the Convex credential pool are split into [oc_concepts_qa_e2e_automation_transport_reference](oc_concepts_qa_e2e_automation_transport_reference.md). The command surface that launches these lanes is in [oc_concepts_qa_e2e_automation_overview](oc_concepts_qa_e2e_automation_overview.md); the adapter design is in [oc_concepts_qa_e2e_automation_architecture](oc_concepts_qa_e2e_automation_architecture.md).

## Operator Flow (QA Lab)

The current QA operator flow is a two-pane QA site — left: the Gateway dashboard (Control UI) with the agent; right: QA Lab, showing the Slack-ish transcript and scenario plan. Run it with:

```bash
pnpm qa:lab:up
```

That builds the QA site, starts the Docker-backed gateway lane, and exposes the QA Lab page where an operator or automation loop can give the agent a QA mission, observe real channel behavior, and record what worked, failed, or stayed blocked. For faster UI iteration without rebuilding the Docker image each time, start the stack with a bind-mounted QA Lab bundle:

```bash
pnpm openclaw qa docker-build-image
pnpm qa:lab:build
pnpm qa:lab:up:fast
pnpm qa:lab:watch
```

`qa:lab:up:fast` keeps the Docker services on a prebuilt image and bind-mounts `extensions/qa-lab/web/dist` into the `qa-lab` container; `qa:lab:watch` rebuilds that bundle on change and the browser auto-reloads when the QA Lab asset hash changes.

## Observability Smokes

For a local OpenTelemetry signal smoke, run `pnpm qa:otel:smoke`. It starts a local OTLP/HTTP receiver, runs the `otel-trace-smoke` scenario with the `diagnostics-otel` plugin enabled, then asserts traces, metrics, and logs are exported. It decodes the exported protobuf trace spans and checks the release-critical shape — `openclaw.run`, `openclaw.harness.run`, a latest GenAI semantic-convention model-call span, `openclaw.context.assembled`, and `openclaw.message.delivery` must be present. The smoke forces `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, so the model-call span must use the `{gen_ai.operation.name} {gen_ai.request.model}` name; model calls must not export `StreamAbandoned` on successful turns; and raw diagnostic IDs / `openclaw.content.*` attributes must stay out of the trace. The raw OTLP payloads must not contain the prompt sentinel, response sentinel, or QA session key. It writes `otel-smoke-summary.json` next to the QA suite artifacts.

For a collector-backed lane, `pnpm qa:otel:collector-smoke` puts a real OpenTelemetry Collector Docker container in front of the same receiver — use it when changing endpoint wiring, collector compatibility, or OTLP export behavior the in-process receiver could mask. For the protected Prometheus scrape smoke, `pnpm qa:prometheus:smoke` runs the `docker-prometheus-smoke` scenario with `diagnostics-prometheus` enabled, verifies unauthenticated scrapes are rejected, then checks the authenticated scrape includes release-critical metric families without prompt content, response content, raw diagnostic identifiers, auth tokens, or local paths. `pnpm qa:observability:smoke` runs both back to back; `pnpm qa:observability:collector-smoke` runs the collector OTel lane plus the protected Prometheus scrape. Observability QA stays source-checkout only — the npm tarball intentionally omits QA Lab, so package Docker release lanes do not run `qa` commands; use these `pnpm` aliases from a built source checkout when changing diagnostics instrumentation.

## Matrix and Multipass Lanes

For a transport-real Matrix smoke lane, run `pnpm openclaw qa matrix --profile fast --fail-fast`. The full CLI reference, profile/scenario catalog, env vars, and artifact layout live in the dedicated Matrix QA page; at a glance it provisions a disposable Tuwunel homeserver in Docker, registers temporary driver/SUT/observer users, runs the real Matrix plugin inside a child QA gateway scoped to that transport (no `qa-channel`), then writes a Markdown report, JSON summary, observed-events artifact, and combined output log under `.artifacts/qa-e2e/matrix-<timestamp>/`. The scenarios cover transport behavior unit tests cannot prove end to end: mention gating, allow-bot policies, allowlists, top-level and threaded replies, DM routing, reaction handling, inbound edit suppression, restart replay dedupe, homeserver interruption recovery, approval metadata delivery, media handling, and Matrix E2EE bootstrap/recovery/verification flows. CI uses the same command surface in `.github/workflows/qa-live-transports-convex.yml`; scheduled and default manual runs execute the fast Matrix profile with live frontier credentials, `--fast`, and `OPENCLAW_QA_MATRIX_NO_REPLY_WINDOW_MS=3000`, and manual `matrix_profile=all` fans out into five profile shards.

For a disposable Linux VM lane without bringing Docker into the QA path:

```bash
pnpm openclaw qa suite --runner multipass --scenario channel-chat-baseline
```

This boots a fresh Multipass guest, installs dependencies, builds OpenClaw inside the guest, runs `qa suite`, then copies the normal QA report and summary back into `.artifacts/qa-e2e/...` on the host. It reuses the same scenario-selection behavior as `qa suite` on the host. Host and Multipass runs execute multiple selected scenarios in parallel with isolated gateway workers by default (`qa-channel` defaults to concurrency 4, capped by selected scenario count; tune with `--concurrency <count>`, or `--concurrency 1` for serial). Use `--pack personal-agent` to run the personal-assistant benchmark pack (additive with repeated `--scenario`), or `--pack observability` when a custom runner already supplies the OTel collector. The command exits non-zero when any scenario fails; use `--allow-failures` for artifacts without a failing exit code. Live runs forward env-based provider keys, the QA live provider config path, and `CODEX_HOME` when present; keep `--output-dir` under the repo root so the guest can write back through the mounted workspace.

## Mantis Desktop and Visual Runs

For a full Slack desktop VM run with VNC rescue:

```bash
pnpm openclaw qa mantis slack-desktop-smoke \
  --gateway-setup \
  --scenario slack-canary \
  --keep-lease
```

That leases a Crabbox desktop/browser machine, runs the Slack live lane inside the VM, opens Slack Web in the VNC browser, captures the desktop, and copies `slack-qa/`, `slack-desktop-smoke.png`, and `slack-desktop-smoke.mp4` (when video capture is available) to the Mantis artifact directory. Mantis reports total and per-phase timings in `mantis-slack-desktop-smoke-report.md`. Reuse `--lease-id <cbx_...>` after logging into Slack Web via VNC; the default `--hydrate-mode source` verifies from a source checkout and installs/builds inside the VM, while `--hydrate-mode prehydrated` skips that step (and fails closed when the workspace is not ready). With `--gateway-setup`, Mantis leaves a persistent OpenClaw Slack gateway running inside the VM on port `38973`. The native-approval checkpoint mode (`--approval-checkpoints`, mutually exclusive with `--gateway-setup`) runs the Slack approval scenarios, waits at each pending/resolved state, renders the observed Slack message into `approval-checkpoints/<scenario>-pending.png` / `-resolved.png`, and fails if any checkpoint, evidence, acknowledgement, or screenshot is missing. The operator checklist, workflow dispatch command, evidence-comment contract, hydrate-mode decision table, timing interpretation, and failure handling live in the Mantis Slack Desktop Runbook.

For an agent/CV-style desktop task:

```bash
pnpm openclaw qa mantis visual-task \
  --browser-url https://example.net \
  --expect-text "Example Domain" \
  --vision-model openai/gpt-5.5
```

`visual-task` leases or reuses a Crabbox machine, starts `crabbox record --while`, drives the visible browser through a nested `visual-driver`, captures `visual-task.png`, optionally runs `openclaw infer image describe` (`--vision-mode image-describe`), and writes `visual-task.mp4` plus summary/driver-result/report JSON+MD. With `--expect-text`, the vision prompt asks for a structured JSON verdict and only passes on positive visible evidence (merely quoting the target text fails). `--vision-mode metadata` is a no-model smoke proving the desktop/browser/screenshot/video plumbing; recording is required (no non-empty `visual-task.mp4` fails the task). Before pooled-credential runs, `pnpm openclaw qa credentials doctor` checks Convex broker env, validates endpoint settings, and verifies admin/list reachability when the maintainer secret is present (reporting only set/missing status for secrets).

## Live Transport Coverage Matrix

Live transport lanes share one contract instead of each inventing its own scenario-list shape (`qa-channel` is the broad synthetic product-behavior suite, not part of this matrix). Live runners import the shared scenario ids, baseline coverage helpers, and scenario-selection helper from `openclaw/plugin-sdk/qa-live-transport-scenarios`.

| Lane | Canary | Mention gating | Bot-to-bot | Allowlist block | Top-level reply | Restart resume | Thread follow-up | Thread isolation | Reaction obs. | Help cmd | Native cmd reg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Matrix | x | x | x | x | x | x | x | x | x | | |
| Telegram | x | x | x | | | | | | | x | |
| Discord | x | x | x | | | | | | | | x |
| Slack | x | x | x | x | x | x | x | x | | | |
| WhatsApp | x | x | | x | x | x | | | x | x | |

This keeps `qa-channel` as the broad product-behavior suite while Matrix, Telegram, and other live transports share one explicit transport-contract checklist.

**Source**: OpenClaw documentation — `concepts/qa-e2e-automation` (operator-flow / observability / coverage half; mirror `inbox/openclaw_docs/concepts/qa-e2e-automation.md`)
**Last Updated**: 2026-06-23
**Status**: Active
