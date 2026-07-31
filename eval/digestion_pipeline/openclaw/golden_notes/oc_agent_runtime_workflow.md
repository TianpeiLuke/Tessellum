---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - agent_runtime
keywords:
  - openclaw agent runtime workflow
  - pnpm check build test
  - vitest agent runtime tests
  - openclaw_live_test live provider
  - gateway dev tui manual testing
  - clean slate reset openclaw state dir
  - auth-profiles.json sessions reset
topics:
  - OpenClaw
  - Agent Runtime Workflow
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/openclaw-agent-runtime
access_control_group: ["general"]
---

# OpenClaw — Agent Runtime Developer Workflow

## Overview

This note is the developer build/test/live-validation workflow for the OpenClaw **agent runtime** — the "sane workflow" the `openclaw-agent-runtime` root-slug hub page prescribes for working on agent-runtime code. It is a procedure covering the local landing gates (`pnpm check` / `pnpm build` / `pnpm check && pnpm test`), the Vitest agent-runtime test set (including the opt-in `OPENCLAW_LIVE_TEST=1` live provider exercise), the manual gateway-dev / `agent` / TUI testing flow, and the clean-slate reset of the `~/.openclaw` state directory (config, auth profiles, credentials, sessions, workspace). It mirrors the `openclaw-agent-runtime` source page; the runtime architecture itself is documented separately and linked, not recreated here.

## Type checking and linting

Three local gates progressively widen scope:

- **Default local gate** — `pnpm check`.
- **Build gate** — `pnpm build`, run when the change can affect build output, packaging, or lazy-loading/module boundaries.
- **Full landing gate for agent-runtime changes** — `pnpm check && pnpm test`.

## Running Agent Runtime Tests

Run the agent-runtime test set directly with Vitest by passing the test globs to `pnpm test`:

```bash
pnpm test \
  "src/agents/agent-*.test.ts" \
  "src/agents/embedded-agent-*.test.ts" \
  "src/agents/agent-tools*.test.ts" \
  "src/agents/agent-settings.test.ts" \
  "src/agents/agent-tool-definition-adapter*.test.ts" \
  "src/agents/agent-hooks/**/*.test.ts"
```

To include the live provider exercise, set `OPENCLAW_LIVE_TEST=1` and run the live test file:

```bash
OPENCLAW_LIVE_TEST=1 pnpm test src/agents/embedded-agent-runner-extraparams.live.test.ts
```

Per the source page, this covers the main agent-runtime unit suites: `src/agents/agent-*.test.ts`, `src/agents/embedded-agent-*.test.ts`, `src/agents/agent-tools*.test.ts`, `src/agents/agent-settings.test.ts`, `src/agents/agent-tool-definition-adapter.test.ts`, and `src/agents/agent-hooks/*.test.ts`.

## Manual testing

The recommended manual flow runs the gateway in dev mode and then drives the agent directly:

- Run the gateway in dev mode — `pnpm gateway:dev`.
- Trigger the agent directly — `pnpm openclaw agent --message "Hello" --thinking low`.
- Use the TUI for interactive debugging — `pnpm tui`.

For tool-call behavior, prompt for a `read` or `exec` action so you can see tool streaming and payload handling.

## Clean slate reset

State lives under the OpenClaw state directory. The default is `~/.openclaw`; if `OPENCLAW_STATE_DIR` is set, use that directory instead. To reset everything, clear these paths:

- `openclaw.json` — for config.
- `agents/<agentId>/agent/auth-profiles.json` — for model auth profiles (API keys + OAuth).
- `credentials/` — for provider/channel state that still lives outside the auth-profile store.
- `agents/<agentId>/sessions/` — for agent session history.
- `agents/<agentId>/sessions/sessions.json` — for the session index.
- `sessions/` — if legacy paths exist.
- `workspace/` — if you want a blank workspace.

Two narrower resets are documented: to reset only sessions, delete `agents/<agentId>/sessions/` for that agent; to keep auth, leave `agents/<agentId>/agent/auth-profiles.json` and any provider state under `credentials/` in place.

**Source**: OpenClaw documentation — `openclaw-agent-runtime` (mirror `inbox/openclaw_docs/openclaw-agent-runtime.md`)
**Last Updated**: 2026-06-22
**Status**: Active
