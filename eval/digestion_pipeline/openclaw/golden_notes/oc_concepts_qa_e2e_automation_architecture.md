---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - automation
keywords:
  - openclaw qa stack architecture
  - qa-lab transport seam
  - repo-backed yaml scenarios
  - mock-openai aimock provider lanes
  - transport adapter runner plugin
  - adding a channel qa
  - scenario helper names
  - qa markdown evidence report
topics:
  - OpenClaw
  - QA E2E Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/concepts/qa-e2e-automation
access_control_group: ["general"]
---

# OpenClaw — QA E2E Automation Architecture (Seeds, Provider Mocks, Transport Adapters, Reporting)

## Overview

This note models the internal architecture of the OpenClaw private QA stack: the repo-backed YAML scenario seeds that are the source of truth per test run, the two local provider mock lanes (`mock-openai` and `aimock`), the qa-lab-host versus transport-runner contract (the generic seam, the strict "adding a channel" two-step, the decision rule, and the preferred scenario helper names), and the Markdown evidence reporting assembled from the observed bus timeline. It mirrors the `Repo-backed seeds`, `Provider mock lanes`, `Transport adapters` (with `### Adding a channel` and `### Scenario helper names`), and `Reporting` sections of the `concepts/qa-e2e-automation` source page. The command surface, operator flow, and coverage matrix are modeled in `oc_concepts_qa_e2e_automation_overview`; the live-transport lanes (Telegram/Discord/Slack/WhatsApp + Convex pool) are modeled in `oc_concepts_qa_e2e_automation_live_transports`.

## Repo-Backed Scenario Seeds

Seed assets live in `qa/`, intentionally kept in git so the QA plan is visible to both humans and the agent: `qa/scenarios/index.yaml` plus per-theme files at `qa/scenarios/<theme>/*.yaml`. The design principle is that `qa-lab` should stay a generic YAML scenario runner — each scenario YAML file is the source of truth for one test run.

A scenario YAML file should define:

- top-level `title`
- `scenario` metadata
- optional category, capability, lane, and risk metadata in `scenario`
- docs and code refs in `scenario`
- optional plugin requirements in `scenario`
- optional gateway config patch in `scenario`
- executable top-level `flow` for flow scenarios, or `scenario.execution.kind` / `scenario.execution.path` for Vitest and Playwright scenarios

The reusable runtime surface that backs `flow` is allowed to stay generic and cross-cutting — for example, YAML scenarios can combine transport-side helpers with browser-side helpers that drive the embedded Control UI through the Gateway `browser.request` seam without adding a special-case runner. Scenario files should be grouped by product capability rather than source-tree folder; scenario IDs must stay stable when files move, with `docsRefs` and `codeRefs` used for implementation traceability.

The baseline list should stay broad enough to cover DM and channel chat, thread behavior, message action lifecycle, cron callbacks, memory recall, model switching, subagent handoff, repo-reading and docs-reading, and one small build task such as Lobster Invaders.

## Provider Mock Lanes

`qa suite` has two local provider mock lanes that decouple deterministic test runs from real model calls:

- `mock-openai` is the scenario-aware OpenClaw mock. It remains the default deterministic mock lane for repo-backed QA and parity gates.
- `aimock` starts an AIMock-backed provider server for experimental protocol, fixture, record/replay, and chaos coverage. It is additive and does not replace the `mock-openai` scenario dispatcher.

Provider-lane implementation lives under `extensions/qa-lab/src/providers/`. Each provider owns its defaults, local server startup, gateway model config, auth-profile staging needs, and live/mock capability flags. Shared suite and gateway code should route through the provider registry instead of branching on provider names.

## Transport Adapters — qa-lab Host vs Runner Plugin Contract

`qa-lab` owns a generic transport seam for YAML QA scenarios. `qa-channel` is the first adapter on that seam, but the design target is wider: future real or synthetic channels should plug into the same suite runner instead of adding a transport-specific QA runner. At the architecture level the responsibility split is:

- `qa-lab` owns generic scenario execution, worker concurrency, artifact writing, and reporting.
- The transport adapter owns gateway config, readiness, inbound and outbound observation, transport actions, and normalized transport state.
- YAML scenario files under `qa/scenarios/` define the test run; `qa-lab` provides the reusable runtime surface that executes them.

### Adding a Channel

Adding a channel to the YAML QA system requires exactly two things: (1) a transport adapter for the channel, and (2) a scenario pack that exercises the channel contract. Do not add a new top-level QA command root when the shared `qa-lab` host can own the flow.

`qa-lab` owns the shared host mechanics:

- the `openclaw qa` command root
- suite startup and teardown
- worker concurrency
- artifact writing
- report generation
- scenario execution
- compatibility aliases for older `qa-channel` scenarios

Runner plugins own the transport contract: how `openclaw qa <runner>` is mounted beneath the shared `qa` root, how the gateway is configured for that transport, how readiness is checked, how inbound events are injected, how outbound messages are observed, how transcripts and normalized transport state are exposed, how transport-backed actions are executed, and how transport-specific reset or cleanup is handled.

The minimum adoption bar for a new channel:

1. Keep `qa-lab` as the owner of the shared `qa` root.
2. Implement the transport runner on the shared `qa-lab` host seam.
3. Keep transport-specific mechanics inside the runner plugin or channel harness.
4. Mount the runner as `openclaw qa <runner>` instead of registering a competing root command. Runner plugins should declare `qaRunners` in `openclaw.plugin.json` and export a matching `qaRunnerCliRegistrations` array from `runtime-api.ts`. Keep `runtime-api.ts` light; lazy CLI and runner execution should stay behind separate entrypoints.
5. Author or adapt YAML scenarios under the themed `qa/scenarios/` directories.
6. Use the generic scenario helpers for new scenarios.
7. Keep existing compatibility aliases working unless the repo is doing an intentional migration.

The decision rule is strict: if behavior can be expressed once in `qa-lab`, put it in `qa-lab`; if behavior depends on one channel transport, keep it in that runner plugin or plugin harness; if a scenario needs a new capability that more than one channel can use, add a generic helper instead of a channel-specific branch in `suite.ts`; if a behavior is only meaningful for one transport, keep the scenario transport-specific and make that explicit in the scenario contract.

### Scenario Helper Names

Preferred generic helpers for new scenarios are `waitForTransportReady`, `waitForChannelReady`, `injectInboundMessage`, `injectOutboundMessage`, `waitForTransportOutboundMessage`, `waitForChannelOutboundMessage`, `waitForNoTransportOutbound`, `getTransportSnapshot`, `readTransportMessage`, `readTransportTranscript`, `formatTransportTranscript`, and `resetTransport`. Compatibility aliases remain available for existing scenarios — `waitForQaChannelReady`, `waitForOutboundMessage`, `waitForNoOutbound`, `formatConversationTranscript`, `resetBus` — but new scenario authoring should use the generic names. The aliases exist to avoid a flag-day migration, not as the model going forward.

## Reporting — Markdown Evidence from the Observed Bus

`qa-lab` exports a Markdown protocol report from the observed bus timeline. The report should answer what worked, what failed, what stayed blocked, and what follow-up scenarios are worth adding. For the inventory of available scenarios — useful when sizing follow-up work or wiring a new transport — run `pnpm openclaw qa coverage` (add `--json` for machine-readable output). When choosing focused proof for a touched behavior or file path, run `pnpm openclaw qa coverage --match <query>`; the match report searches scenario metadata, docs refs, code refs, coverage IDs, plugins, and provider requirements, then prints matching `qa suite --scenario ...` targets. Treat it as a discovery aid, not a gate replacement — the selected scenario still needs the right provider mode, live transport, Multipass, Testbox, or release lane for the behavior under test.

Every `qa suite` run writes top-level `qa-evidence.json`, `qa-suite-summary.json`, and `qa-suite-report.md` artifacts for the selected scenario set. Scenarios that declare `execution.kind: vitest` or `execution.kind: playwright` run the matching test path and also write per-scenario logs. Scenarios that declare `execution.kind: script` run the evidence producer at `execution.path` through `node --import tsx` (with `${outputDir}` and `${scenarioId}` expanded in `execution.args`); the producer writes its own `qa-evidence.json`, whose entries are imported into the suite output and whose artifact paths are resolved relative to that producer `qa-evidence.json`. When `qa suite` is reached through `qa run --qa-profile`, the same `qa-evidence.json` also includes the profile scorecard summary for the selected taxonomy categories.

For character and style checks, the same scenario is run across multiple live model refs and written into a judged Markdown report:

```bash
pnpm openclaw qa character-eval \
  --model openai/gpt-5.5,thinking=medium,fast \
  --model anthropic/claude-opus-4-8,thinking=high \
  --judge-model openai/gpt-5.5,thinking=xhigh,fast \
  --judge-model anthropic/claude-opus-4-8,thinking=high \
  --blind-judge-models \
  --concurrency 16 \
  --judge-concurrency 16
```

`qa character-eval` runs local QA gateway child processes (not Docker). Character eval scenarios set the persona through `SOUL.md`, then run ordinary user turns such as chat, workspace help, and small file tasks; the candidate model is not told it is being evaluated. The command preserves each full transcript, records basic run stats, then asks the judge models in fast mode with `xhigh` reasoning where supported to rank the runs by naturalness, vibe, and humor. Use `--blind-judge-models` when comparing providers: the judge prompt still gets every transcript and run status, but candidate refs are replaced with neutral labels such as `candidate-01`, and the report maps rankings back to real refs after parsing. Candidate runs default to `high` thinking (with `medium` for GPT-5.5 and `xhigh` for older OpenAI eval refs that support it); candidate and judge model runs both default to concurrency 16, and judge prompts explicitly say not to rank by speed.

**Source**: OpenClaw documentation — `concepts/qa-e2e-automation` (mirror `inbox/openclaw_docs/concepts/qa-e2e-automation.md`), sections Repo-backed seeds / Provider mock lanes / Transport adapters / Reporting
**Last Updated**: 2026-06-22
**Status**: Active
