---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - workboard
keywords:
  - openclaw workboard plugin
  - workboard card model
  - kanban card status
  - card executions tasks
  - workboard dispatch worker selection
  - worker prompt claim token
  - workboard agent tools
  - deterministic worker session key
topics:
  - OpenClaw
  - Workboard Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/workboard
access_control_group: ["general"]
---

# OpenClaw — The Workboard Data Model

## Overview

This note models the data side of the bundled OpenClaw **Workboard** plugin: the optional Kanban-style board of agent-owned work cards that the OpenClaw Control UI renders. It covers the plugin's default state, what each card stores, how card executions link to background tasks/runs/sessions, the `workboard_*` agent-tool surface, the SQLite persistence model, and the Gateway-local dispatch model (worker selection, worker prompt/lifecycle, and dispatch entry points) — mirroring the model-bearing sections of the `plugins/workboard` source page. Workboard is intentionally small: it tracks local operating work for one OpenClaw Gateway and is not a replacement for GitHub Issues, Linear, Jira, or other team project-management systems. The operational surface (CLI/slash command, session-lifecycle sync, dashboard workflow, permissions, configuration, troubleshooting) lives in the companion operations note.

## Default State

Workboard is a bundled plugin and is **disabled by default** unless you enable it in plugin config. Once enabled (and after a Gateway restart), the **Workboard tab** appears in the dashboard navigation. If the tab is visible but the plugin is disabled or blocked by `plugins.allow` / `plugins.deny`, the view shows a plugin-unavailable state instead of local card data — the board UI degrades gracefully rather than failing.

## What Cards Contain

A card is the atomic unit of the Workboard model. Each card stores:

- title and notes
- status: `triage`, `backlog`, `todo`, `scheduled`, `ready`, `running`, `review`, `blocked`, or `done`
- priority: `low`, `normal`, `high`, or `urgent`
- labels
- optional agent id
- optional linked task, run, session, or source URL
- optional execution metadata for a Codex or Claude run started from the card
- compact metadata for attempts, comments, links, proof, artifacts, automation, attachments, worker logs, worker protocol state, claims, diagnostics, notifications, templates, archive state, and stale-session detection
- recent card events such as created, moved, linked, claimed, heartbeat, attempt, proof, artifact, diagnostic, notification, dispatch, archive, stale, or agent-updated changes

Cards are stored in the plugin's Gateway state. They are local to the Gateway state directory and **move with the rest of that Gateway's OpenClaw state**. Workboard keeps compact per-card metadata so operators can see how a card moved through the board without opening the linked session; events, attempt summaries, proof snippets, related links, comments, archive markers, and stale-session markers are intentionally local metadata that do **not** replace session transcripts or GitHub issue history.

Durable board data lives in a plugin-owned relational **SQLite** database under the OpenClaw state directory. Boards, cards, labels, lifecycle events, run attempts, comments, dependency links, proof, artifact references, attachment metadata and blobs, diagnostics, notifications, worker logs, protocol state, and subscriptions are persisted in Workboard tables instead of plugin key-value entries. A card export still preserves the board narrative without inlining attachment blob contents. Installations that used Workboard in the `.28` release can run `openclaw doctor --fix` to migrate the shipped legacy plugin-state namespaces (`workboard.cards`, `workboard.boards`, and `workboard.notify`) into the relational database; if a legacy `workboard.attachments` namespace is present, doctor migrates those attachment blobs too.

## Card Executions and Tasks

Unlinked cards can start work directly from the card. Autonomous starts use the **Gateway's task-tracked agent run path**, then Workboard links the resulting task, run id, and session key back onto the card. Start uses the Gateway's configured default agent and model; Codex and Claude actions are optional explicit model choices:

- **Run Codex** or **Run Claude** starts a task-backed agent run, sends the card prompt, and marks the card `running`.
- **Open Codex** or **Open Claude** creates a linked dashboard session **without** sending the card prompt or moving the card, so you can work manually while it stays attached to the board.

Execution metadata stores the selected engine, mode, model ref, session key, run id, task id (when available), and lifecycle status on the card. Codex executions use `openai/gpt-5.5`; Claude executions use `anthropic/claude-sonnet-4-6`. Each linked execution also records an **attempt summary** on the same card record, keeping the engine, mode, model, run id, timestamps, status, and a rolling failure count so repeated failures remain visible on the board.

The dashboard refreshes task status from the Gateway **task ledger** and matches tasks back to cards by task id, run id, or linked session key. If a task is queued or running, the card lifecycle shows active task state. If the task finishes, fails, times out, or is cancelled, the card lifecycle moves toward `review` or `blocked` status using the same lifecycle sync as linked sessions.

## Agent Coordination — the `workboard_*` Tool Surface

Workboard exposes optional **agent tools** for board-aware workflows. They form the model's mutation/read surface that a running agent uses to coordinate work:

- `workboard_list` lists compact cards with claim and diagnostic state, with an optional board filter.
- `workboard_read` returns one card plus bounded worker context built from notes, attempts, comments, links, proof, artifacts, parent results, recent assignee work, and active diagnostics.
- `workboard_create` creates a card with optional parents, tenant, skills, board, workspace metadata, idempotency key, runtime limit, and retry budget.
- `workboard_link` links a parent card to a child card. Children stay in `todo` until **every** parent reaches `done`; then dispatch promotion moves them to `ready`.
- `workboard_claim` claims a card for the calling agent and moves backlog, todo, or ready cards into `running`.
- `workboard_heartbeat` refreshes the claim heartbeat during longer runs.
- `workboard_release` releases the claim after completion, pause, or handoff and can move the card to a next status.
- `workboard_complete` and `workboard_block` are structured lifecycle tools for final summaries, proof, artifacts, created-card manifests, and blocker reasons. Created-card manifests must reference cards linked back to the completed card, which keeps phantom children out of summaries.
- `workboard_attachment_add`, `workboard_attachment_read`, and `workboard_attachment_delete` store small card attachments in plugin SQLite state, index them on the card, and expose them in worker context.
- `workboard_worker_log` and `workboard_protocol_violation` record worker log lines and block cards when an automated worker stops without calling `workboard_complete` or `workboard_block`.
- `workboard_board_create`, `workboard_board_archive`, and `workboard_board_delete` manage persisted board metadata such as display name, description, archive state, and default workspace.
- `workboard_runs` returns the persisted run-attempt history stored on a card.
- `workboard_specify` turns a rough triage or backlog card into a clarified `todo` card and records the specification summary on the card.
- `workboard_decompose` fans a parent orchestration card into linked children, inherits board and tenant metadata, and can complete the parent with a created-card manifest.
- `workboard_notify_subscribe`, `workboard_notify_list`, `workboard_notify_events`, `workboard_notify_advance`, and `workboard_notify_unsubscribe` manage notification subscriptions in plugin state. Event reads are replay-safe; the advance tool moves the durable cursor so callers can resume without losing or double-reading completed, failed, or stale card events.
- `workboard_boards`, `workboard_stats`, `workboard_promote`, `workboard_reassign`, `workboard_reclaim`, `workboard_comment`, `workboard_proof`, `workboard_unblock`, and `workboard_dispatch` let an agent inspect board namespaces, view queue stats, recover stuck work, add handoff notes, attach proof or artifact references, move blocked work back to `todo`, and nudge dependency promotion or stale-claim cleanup.

Claimed cards **reject agent-tool mutations from other agents** unless the caller has the claim token returned by `workboard_claim`. Dashboard operators still use the normal Gateway RPC surface and can recover or reassign cards. Workboard diagnostics are computed from local card metadata: the built-in checks flag assigned cards that wait too long, running cards without recent heartbeat, blocked cards that need attention, repeated failures, done cards without proof, and running cards that only have a loose session link.

## The Dispatch Model

Dispatch is **intentionally Gateway-local**. It does not spawn arbitrary operating-system processes; normal OpenClaw subagent sessions still own execution. A dispatch action promotes dependency-ready cards, records dispatch metadata on `ready` cards, blocks expired claims or timed-out runs, marks board-configured triage cards as orchestration candidates, then claims a small batch of `ready` cards and starts worker runs through the Gateway **subagent runtime**. Assigned cards use `agent:<id>:subagent:workboard-*` worker session keys; unassigned cards use unscoped `subagent:workboard-*` keys so the Gateway still resolves the configured default agent. Workers receive bounded card context plus the claim token they need to heartbeat, complete, or block the card through the Workboard tools.

### Dispatch worker selection

Each dispatch pass starts **at most three workers by default**. Ready cards are ordered by **priority, position, and creation time**, then filtered to avoid duplicate active ownership: a dispatch starts only one card for a given owner or agent in the same pass, and it skips owners that already have running or review work on the board. Archived cards, cards with active claims, and cards without `ready` status are **not** selected for worker starts — though they can still be affected by the data side of dispatch when stale claims, dependency promotion, or timeout cleanup applies.

### Worker prompt and lifecycle

The worker prompt includes the card title, bounded notes and context, the assigned board, and the **Workboard worker protocol**. It also includes the claim owner and claim token so the worker can call `workboard_heartbeat`, `workboard_complete`, or `workboard_block` without another actor taking over the card. When a worker starts successfully, Workboard stores the session key, run id, engine, mode, model label, status, and worker log on the card. The session key is **deterministic for the board and card**, which makes repeated dispatches route back to the same worker lane instead of creating unrelated sessions. If a worker cannot be started after a card is claimed, Workboard blocks the card, clears the claim, records the run-start failure, and appends a worker log line; that failure is visible in the dashboard, CLI JSON, agent tools, and card diagnostics.

### Dispatch entry points

Ready-card worker starts can happen from the dashboard dispatch action, `openclaw workboard dispatch`, or `/workboard dispatch` on a command-capable channel. All three entry points use the Gateway subagent runtime when the Gateway is available. The CLI has one extra operator fallback: if the Gateway is offline or does not expose the Workboard dispatch method and no explicit `--url` or `--token` target was provided, it runs **data-only dispatch** against local SQLite state — that fallback can promote dependencies, clean stale claims, and block timed-out runs, but it **cannot start workers**. Board metadata can include orchestration settings such as `autoDecompose`, `autoDecomposePerDispatch`, `defaultAssignee`, and `orchestratorProfile`; OpenClaw records the orchestration intent and exposes it in worker context, but the actual specification and decomposition still happen through the normal Workboard tools.

**Source**: OpenClaw documentation — `plugins/workboard` (mirror `inbox/openclaw_docs/plugins/workboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
