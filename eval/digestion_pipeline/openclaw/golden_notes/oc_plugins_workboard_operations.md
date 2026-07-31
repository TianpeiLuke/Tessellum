---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - workboard
keywords:
  - openclaw workboard cli
  - workboard dispatch
  - workboard slash command
  - workboard session lifecycle sync
  - workboard dashboard workflow
  - workboard operator permissions
  - workboard plugin enable disable
  - workboard troubleshooting unavailable
topics:
  - OpenClaw
  - Workboard plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/workboard
access_control_group: ["general"]
---

# OpenClaw — Operating the Workboard Plugin (CLI, Dashboard, Permissions, Config)

## Overview

This note is the **operator procedure** for the bundled OpenClaw **Workboard** plugin — the day-to-day commands and workflows for running a board, not its data model (the board/card/dispatch data model lives in the sibling note `oc_plugins_workboard_model.md`). It mirrors the operational sections of the `plugins/workboard` source page: the root `openclaw workboard` CLI and the `/workboard` slash command, session-lifecycle sync of linked cards, the Control-UI dashboard workflow, the `workboard.*` Gateway RPC permission scopes, plugin configuration (enable/disable), and the four troubleshooting cases (unavailable tab, cards not saving, card-start not opening the expected session, dispatch not starting a worker).

## CLI and Slash Command

The plugin registers a root CLI command, `openclaw workboard`. Representative invocations from the source:

```bash
openclaw workboard list
openclaw workboard create "Fix stale card lifecycle" --priority high --labels bug,workboard
openclaw workboard show <card-id>
openclaw workboard dispatch
```

`openclaw workboard dispatch` calls the running Gateway so worker starts use the same subagent runtime as the dashboard. If the Gateway is unavailable, it falls back to **data-only dispatch** so dependency promotion, stale-claim cleanup, and timeout blocking can still run (but no workers are started). Auth, permission, and validation failures still surface as command errors, as do failures for explicit `--url` or `--token` targets.

The `/workboard` slash command supports the same compact operator path on a command-capable channel: `/workboard list`, `/workboard show <card-id>`, `/workboard create <title>`, and `/workboard dispatch`. `list` and `show` are **read** operations for authorized command senders. `create` and `dispatch` require owner status on chat surfaces, or a Gateway client with `operator.write` or `operator.admin`.

The source defers command flags, JSON output, Gateway fallback behavior, unambiguous id-prefix handling, dispatch selection rules, and CLI troubleshooting to the separate **Workboard CLI** doc (`/cli/workboard`).

## Session Lifecycle Sync

Cards can be linked to existing dashboard sessions or to the session created when you start work from a card. Linked cards show the session lifecycle inline: **running, stale, linked idle, done, failed, or missing**.

If the linked session is **missing**, the card stays linked for context and still offers start controls so you can restart work into a fresh dashboard session. If an active linked session stops reporting recent activity, Workboard marks the card **stale** and stores the marker as card metadata until the lifecycle clears it.

You can also capture an existing dashboard session from the **Sessions** tab with **Add to Workboard**. The card is linked to that session, uses the session label or recent user prompt as the title, and seeds notes from the recent user prompt plus the latest assistant response when chat history is available.

While a card is still in an active work state, Workboard follows the linked session with these auto-transitions:

- active linked session → `running`
- completed linked session → `review`
- failed, killed, timed out, or aborted linked session → `blocked`

**Manual review states win.** If you move a card to `review`, `blocked`, or `done`, Workboard stops auto-moving that card until you move it back to `todo` or `running`.

## Dashboard Workflow

The Control-UI dashboard workflow, in order, is:

1. Open the Workboard tab in the Control UI.
2. Create a card with a title, notes, priority, labels, optional agent, and optional linked session.
3. Or open Sessions and choose **Add to Workboard** for an existing session.
4. Drag the card between columns, or focus the compact status control on the card and use its menu or ArrowLeft/ArrowRight.
5. Start work from the card to create or reuse a dashboard session.
6. Open the linked session from the card while the agent works.
7. Let lifecycle sync move running work into `review` or `blocked`, then manually move the card to `done` when accepted.

Starting a card uses normal Gateway sessions: the Workboard plugin only stores card metadata and links, while the conversation transcript, model selection, and run lifecycle stay owned by the regular session system. Use **Stop** on a live linked card to abort the active session run — Workboard marks that card `blocked` so it remains visible for follow-up. New cards can also start from Workboard **templates** for bugfixes, docs, releases, PR reviews, or plugin work; templates prefill title, notes, labels, and priority, and the selected template id is stored as card metadata.

## Permissions

The plugin registers Gateway RPC methods under the `workboard.*` namespace, gated by operator scopes:

- `workboard.cards.list` requires `operator.read`
- `workboard.cards.export` requires `operator.read`
- `workboard.cards.diagnostics` requires `operator.read`
- `workboard.cards.diagnostics.refresh` requires `operator.write`
- attachment list/get and notification event reads require `operator.read`
- notification cursor advancement requires `operator.write`
- create, update, move, delete, comment, link, dependency link, proof, artifact, attachment add/delete, worker log, protocol violation, claim, heartbeat, release, complete, block, unblock, dispatch, bulk, and archive methods require `operator.write`

Browsers connected with read-only operator access can inspect the board but cannot mutate cards.

## Configuration

Workboard has **no plugin-specific config today**. Enable or disable it with the standard plugin entry. Enable (then restart the Gateway):

```bash
openclaw plugins enable workboard
openclaw gateway restart
```

The equivalent config-file form is the standard plugin entry:

```json5
{
  plugins: {
    entries: {
      workboard: {
        enabled: true,
        config: {},
      },
    },
  },
}
```

Disable it again with:

```bash
openclaw plugins disable workboard
openclaw gateway restart
```

After enabling, open the dashboard with `openclaw dashboard`; the Workboard tab appears in the dashboard navigation.

## Troubleshooting

### The tab says Workboard is unavailable

Check plugin policy with:

```bash
openclaw plugins inspect workboard --runtime --json
```

If `plugins.allow` is configured, add `workboard` to that allowlist. If `plugins.deny` contains `workboard`, remove it before enabling the plugin.

### Cards do not save

Confirm the browser connection has `operator.write` access. Read-only operator sessions can list cards but cannot create, edit, move, or delete them.

### Starting a card does not open the expected session

Workboard creates links to normal dashboard sessions. Check the card's agent id and linked session, then open the Sessions or Chat view to inspect the actual run state.

### Dispatch does not start a worker

Confirm there is at least one `ready` card without an active claim:

```bash
openclaw workboard list --status ready
```

If the CLI reports data-only dispatch, start or restart the Gateway and retry — data-only dispatch updates local board state but cannot start subagent worker runs. Cards can also be skipped when another card for the same owner or agent is already running or waiting for review; complete, block, or release that active work before dispatching more work for the same owner.

**Source**: OpenClaw documentation — `plugins/workboard` (mirror `inbox/openclaw_docs/plugins/workboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
