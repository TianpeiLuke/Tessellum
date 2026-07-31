---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - qa
keywords:
  - openclaw personal agent benchmark pack
  - personal-agent qa scenario pack
  - qa suite --pack personal-agent
  - qa-channel mock-openai
  - scenario-packs.ts
  - QA_PERSONAL_AGENT_SCENARIO_IDS
  - fake-data privacy model
  - qa/scenarios/personal
topics:
  - OpenClaw
  - Personal Agent Benchmark Pack
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/personal-agent-benchmark-pack
access_control_group: ["general"]
---

# OpenClaw — Personal Agent Benchmark Pack

## Overview

This note covers the OpenClaw **Personal Agent Benchmark Pack**: a small, repo-backed QA scenario pack for checking local personal-assistant workflow reliability, as documented on the `concepts/personal-agent-benchmark-pack` source page. The pack is explicitly NOT a generic model benchmark and does not require a new runner — it reuses OpenClaw's private QA stack, the synthetic `qa-channel`, and the existing `qa/scenarios` YAML catalog. This note describes what the pack is, its intentionally narrow first scenario set, how to invoke it via `--pack personal-agent`, the fake-data privacy model that keeps it off live services, and how to extend the catalog.

## What the Pack Is

The Personal Agent Benchmark Pack is a small repo-backed QA scenario pack for local personal-assistant workflows. The source page is emphatic about what it is *not*: it is **not a generic model benchmark** and it **does not require a new runner**. Instead it reuses three pieces that already exist in OpenClaw's QA stack — the private QA stack described in the QA overview (`concepts/qa-e2e-automation`), the synthetic QA channel (`channels/qa-channel`), and the existing `qa/scenarios` YAML catalog. Because it rides on existing infrastructure, adopting the pack adds no new transport, plugin, dependency, or model judge.

## Scenarios

The first pack is intentionally narrow. Its scenarios exercise these personal-assistant behaviors against fake data:

- fake personal reminders through local cron delivery
- fake DM and thread reply routing through `qa-channel`
- fake preference recall from the temporary QA workspace memory files
- fake secret no-echo checks
- safe read-backed tool followthrough after a short approval-style turn
- approval denial stop behavior for a sensitive local read request
- proof-backed task status reporting that keeps pending, blocked, and done separate
- share-safe diagnostics artifacts that keep useful status while omitting raw personal content
- proof-backed completion claims that avoid fake progress before local evidence exists
- failure recovery that reports partial status and keeps retry boundaries clear

The machine-readable pack metadata lives in `extensions/qa-lab/src/scenario-packs.ts`. The pack is run with the `--pack personal-agent` flag against a local provider lane:

```bash
OPENCLAW_ENABLE_PRIVATE_QA_CLI=1 pnpm openclaw qa suite \
  --provider-mode mock-openai \
  --pack personal-agent \
  --concurrency 1
```

`--pack` is additive with repeated `--scenario` flags: explicit scenarios run first, then the pack scenarios run in `QA_PERSONAL_AGENT_SCENARIO_IDS` order with duplicates removed. The pack is designed for `qa-channel` with `mock-openai` (or another local QA provider lane) and should not be pointed at live chat services or real personal accounts.

## Privacy Model

The scenarios use only **fake users, fake preferences, fake secrets**, and the temporary QA gateway workspace created by the suite. They must not read or write real OpenClaw user memory, sessions, credentials, launch agents, global configs, or live gateway state. Artifacts stay under the existing QA suite artifact directory and should be treated like test output. Redaction checks use **fake markers** so that failures are safe to inspect and to file in issues — there is no risk of leaking real personal content when a redaction scenario fails.

## Extending The Pack

To add coverage, drop new `.yaml` cases under `qa/scenarios/personal/`, then add the scenario id to `QA_PERSONAL_AGENT_SCENARIO_IDS`. Each case should be kept small, local, deterministic in `mock-openai`, and focused on one personal-assistant behavior. The source page lists two good follow-up candidates: **redacted trajectory export checks** and **local-only plugin workflow checks**. It also sets an explicit guardrail — avoid adding a new runner, plugin, dependency, live transport, or model judge until the scenario catalog has enough stable cases to justify that surface.

**Source**: OpenClaw documentation — `concepts/personal-agent-benchmark-pack` (mirror `inbox/openclaw_docs/concepts/personal-agent-benchmark-pack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
