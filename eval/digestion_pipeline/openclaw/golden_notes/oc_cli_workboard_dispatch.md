---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - workboard
keywords:
  - openclaw workboard dispatch
  - workboard.cards.dispatch
  - dispatch loop
  - subagent worker run
  - conservative selection
  - data-only fallback
  - claim token
  - block on failure
topics:
  - OpenClaw
  - Workboard Dispatch
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/workboard
access_control_group: ["general"]
---

# OpenClaw — `openclaw workboard dispatch` Mechanics

## Overview

This note documents how the `openclaw workboard dispatch` subcommand turns ready Workboard cards into subagent worker runs, mirroring the `## dispatch` section of the `cli/workboard` source page. It covers the Gateway-RPC path (`workboard.cards.dispatch`), the seven-step dispatch loop, the conservative one-pass selection limits, claimed-card block-on-failure, the data-only local fallback when no live Gateway is reachable, and the text/JSON output shapes. The card-lifecycle usage commands (`list`/`create`/`show`), slash-command parity, and the full permission model are covered by the sibling note [oc_cli_workboard](oc_cli_workboard.md); this note focuses on dispatch mechanics only.

## Invocation and the Gateway-RPC Path

The synopsis is `openclaw workboard dispatch [--url <url>] [--token <token>] [--timeout <ms>] [--json]`. Source examples:

```bash
openclaw workboard dispatch
openclaw workboard dispatch --json
openclaw workboard dispatch --url http://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

`dispatch` first calls the running Gateway RPC method `workboard.cards.dispatch`. That path uses the same subagent runtime as the dashboard dispatch action, so ready cards become task-tracked worker runs with linked session keys. Cards with an assigned agent use agent-scoped subagent session keys; unassigned cards keep an unscoped subagent key so the Gateway's configured default agent is preserved. The CLI dispatch path calls Gateway RPC with `operator.read` and `operator.write` scopes (see [oc_cli_workboard](oc_cli_workboard.md) Permissions); a read-only Gateway token can inspect Workboard data through read methods but cannot create cards or dispatch workers.

## The Dispatch Loop (7 Steps)

Per the source page, the dispatch loop runs these steps in order:

1. Promotes dependency-ready children to `ready`.
2. Blocks expired claims or timed-out worker runs.
3. Records dispatch metadata on ready cards.
4. Selects a small batch of unclaimed ready cards.
5. Claims each selected card for the dispatcher or assigned agent.
6. Starts a subagent worker run with bounded card context and the card claim token.
7. Stores the worker run id, session key, task linkage when the Gateway task ledger reports it, execution status, and worker log on the card.

## Conservative Selection

Selection is intentionally conservative. One dispatch starts at most three workers by default, skips archived or already-claimed cards, and starts only one card per owner or agent in a single pass. Cards already owned by active running or review work are left for a later dispatch.

## Block-on-Failure for Claimed Cards

If worker start fails after a card is claimed, Workboard blocks that card, clears the claim, and records the failure in card execution and worker-log metadata. This keeps failed starts visible instead of silently returning the card to the queue.

## Data-Only Fallback

If no explicit Gateway target is provided and the local Gateway is unavailable or does not expose the Workboard dispatch method yet, the CLI falls back to data-only dispatch against local Workboard state. Data-only dispatch can still promote dependencies, clean stale claims, and block timed-out runs, but it does not start workers. Auth, permission, validation failures, and failures for an explicit `--url` or `--token` target are reported directly.

## Output: Text and JSON

Text output reports worker starts:

```text
dispatch complete: started=2 failures=0
```

Fallback output is explicit:

```text
gateway unavailable; data dispatch only: promoted=1 blocked=0
```

JSON output includes the dispatch result. Gateway-backed dispatch can include `started` and `startFailures`; data-only fallback includes `gatewayUnavailable: true`. Claim tokens are redacted from card JSON output. In the dashboard, the same dispatch result is shown as a short summary so an operator can see how many cards started, promoted, blocked, reclaimed, or failed without opening card details.

**Source**: OpenClaw documentation — `cli/workboard` (`## dispatch` section; mirror `inbox/openclaw_docs/cli/workboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
