---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - heartbeat
keywords:
  - openclaw heartbeat
  - periodic agent turn
  - heartbeat_ok response contract
  - heartbeat.md checklist tasks
  - heartbeat cadence every
  - active hours timezone
  - isolated session light context
  - heartbeat cost awareness
  - manual wake system event
  - context overflow after heartbeat
topics:
  - OpenClaw
  - Heartbeat
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/heartbeat
access_control_group: ["general"]
---

# OpenClaw — Heartbeat Cadence, Response Contract, and Cost Controls

## Overview

This note is the configuration-and-contract half of the OpenClaw **heartbeat**: the periodic main-session agent turn that lets the model surface anything needing attention without spamming you. It mirrors the `gateway/heartbeat` source sections covering cadence (`every`, defaults, timeout), what the prompt is for, the `HEARTBEAT_OK` / `heartbeat_respond` response contract, the config schema with scope precedence (per-agent, active hours, 24/7, multi-account, field notes), the `HEARTBEAT.md` checklist and `tasks:` block, manual wake, reasoning delivery, cost controls, and context-overflow recovery. The delivery-routing and per-channel/per-account visibility half lives in the sibling note **[oc_gateway_heartbeat_delivery](oc_gateway_heartbeat_delivery.md)**. Heartbeat is a scheduled main-session turn — it does **not** create background task records (those are for detached work: ACP runs, subagents, isolated cron jobs).

## Quick start

Enable and tune heartbeat in four steps:

1. **Pick a cadence** — leave heartbeats enabled (default `30m`, or `1h` for Anthropic OAuth/token auth incl. Claude CLI reuse) or set your own.
2. **Add `HEARTBEAT.md` (optional)** — a tiny `HEARTBEAT.md` checklist or `tasks:` block in the agent workspace.
3. **Decide delivery** — `target: "none"` is the default; set `target: "last"` to route to the last contact.
4. **Optional tuning** — reasoning delivery for transparency; lightweight bootstrap context (only `HEARTBEAT.md`); isolated sessions (no full history per run); active-hours restriction (local time).

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // explicit delivery to last contact (default is "none")
        directPolicy: "allow", // default: allow direct/DM targets; set "block" to suppress
        lightContext: true, // optional: only inject HEARTBEAT.md from bootstrap files
        isolatedSession: true, // optional: fresh session each run (no conversation history)
        skipWhenBusy: true, // optional: also defer when this agent's subagent or nested lanes are busy
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // optional: send separate `Thinking` message too
      },
    },
  },
}
```

## Defaults

- **Interval**: `30m` (or `1h` when Anthropic OAuth/token auth is detected, including Claude CLI reuse). Set `agents.defaults.heartbeat.every` or per-agent `agents.list[].heartbeat.every`; use `0m` to disable.
- **Prompt body** (via `agents.defaults.heartbeat.prompt`): `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`
- **Timeout**: unset turns use `agents.defaults.timeoutSeconds` when set, otherwise the cadence capped at 600 seconds. Set `agents.defaults.heartbeat.timeoutSeconds` (or per-agent) for longer heartbeat work.
- The prompt is sent **verbatim** as the user message. The system prompt includes a "Heartbeat" section only when heartbeats are enabled for the default agent, and the run is flagged internally.
- When disabled with `0m`, normal runs also omit `HEARTBEAT.md` from bootstrap context so the model does not see heartbeat-only instructions.
- `heartbeat.activeHours` is checked in the configured timezone; outside the window, heartbeats skip until the next in-window tick.
- Heartbeats automatically defer while cron work is active or queued. `heartbeat.skipWhenBusy: true` also defers an agent on its own session-keyed subagent or nested command lanes; sibling agents no longer pause because another agent has subagent work in flight.

## What the heartbeat prompt is for

The default prompt is intentionally broad:

- **Background tasks**: "Consider outstanding tasks" nudges the agent to review follow-ups (inbox, calendar, reminders, queued work) and surface anything urgent.
- **Human check-in**: "Checkup sometimes on your human during day time" nudges an occasional lightweight "anything you need?" message, avoiding night-time spam via your configured local timezone.

Heartbeat can react to completed background tasks, but a run itself does not create a task record. For something specific (e.g. "check Gmail PubSub stats" or "verify gateway health"), set `agents.defaults.heartbeat.prompt` (or per-agent) to a custom body (sent verbatim).

## Response contract

- If nothing needs attention, reply with **`HEARTBEAT_OK`**.
- Tool-capable runs may instead call `heartbeat_respond` with `notify: false` (no visible update) or `notify: true` plus `notificationText` (alert). When present, the structured tool response takes precedence over the text fallback.
- During heartbeat runs, `HEARTBEAT_OK` is treated as an ack when it appears at the **start or end** of the reply. The token is stripped and the reply dropped if the remaining content is **≤ `ackMaxChars`** (default: 300).
- `HEARTBEAT_OK` in the **middle** of a reply is not treated specially. For alerts, **do not** include it; return only the alert text.
- Outside heartbeats, stray `HEARTBEAT_OK` at the start/end of a message is stripped and logged; a message that is only `HEARTBEAT_OK` is dropped.

## Config

Full heartbeat config block (defaults as inline comments):

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // default: 30m (0m disables)
        model: "anthropic/claude-opus-4-6",
        includeReasoning: false, // default: false (deliver separate Thinking message when available)
        lightContext: false, // default: false; true keeps only HEARTBEAT.md from workspace bootstrap files
        isolatedSession: false, // default: false; true runs each heartbeat in a fresh session (no conversation history)
        skipWhenBusy: false, // default: false; true also waits for this agent's subagent/nested lanes
        target: "last", // default: none | options: last | none | <channel id> (core or plugin, e.g. "imessage")
        to: "+15551234567", // optional channel-specific override
        accountId: "ops-bot", // optional multi-account channel id
        prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        ackMaxChars: 300, // max chars allowed after HEARTBEAT_OK
      },
    },
  },
}
```

### Scope and precedence

- `agents.defaults.heartbeat` sets global heartbeat behavior.
- `agents.list[].heartbeat` merges on top; if any agent has a `heartbeat` block, **only those agents** run heartbeats.
- `channels.defaults.heartbeat` sets visibility defaults for all channels.
- `channels.<channel>.heartbeat` overrides channel defaults.
- `channels.<channel>.accounts.<id>.heartbeat` (multi-account channels) overrides per-channel settings.

### Per-agent heartbeats

The per-agent block merges on top of `agents.defaults.heartbeat` (set shared defaults once, override per agent). In a two-agent example where only the `ops` agent runs heartbeats, the `ops` entry carries its own `heartbeat: { every: "1h", target: "whatsapp", to: "+15551234567", timeoutSeconds: 45, prompt: ... }` while `{ id: "main", default: true }` has none.

### Active hours

Restrict heartbeats with `activeHours` — `start` (HH:MM inclusive; `00:00` start-of-day), `end` (HH:MM exclusive; `24:00` end-of-day), optional `timezone`. Outside the window (e.g. before 9am or after 10pm Eastern for `09:00`–`22:00`), heartbeats are skipped; the next in-window tick runs normally:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // explicit delivery to last contact (default is "none")
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "America/New_York", // optional; uses your userTimezone if set, otherwise host tz
        },
      },
    },
  },
}
```

### 24/7 setup

For all-day heartbeats, either omit `activeHours` (the default) or set a full-day window `activeHours: { start: "00:00", end: "24:00" }`. Do **not** set the same `start` and `end` (e.g. `08:00` to `08:00`) — that zero-width window always skips heartbeats.

### Multi-account

Use `accountId` to target an account on multi-account channels like Telegram; `to` can route to a topic/thread via `<chatId>:topic:<messageThreadId>` (e.g. `to: "12345678:topic:42"`). Matching credentials live under `channels.telegram.accounts.<id>` (e.g. `"ops-bot": { botToken: "YOUR_TELEGRAM_BOT_TOKEN" }`).

### Field notes

Field details beyond the verbatim keys/defaults in the Config block above:

- `isolatedSession` uses the same isolation pattern as cron `sessionTarget: "isolated"`; delivery routing still uses the main session context.
- `skipWhenBusy` defers on the agent's own session-keyed subagent or nested command work; cron lanes always defer heartbeats even without this flag.
- `session` (string, default `main`) — explicit key copied from `openclaw sessions --json`; key formats follow Sessions and Groups.
- `target` options are `last`, an explicit channel/plugin id (`discord`, `matrix`, `telegram`, `whatsapp`), or `none` (default). `directPolicy` (`"allow" | "block"`, default `allow`) — `block` suppresses direct/DM delivery (`reason=dm-blocked`).
- `to` accepts E.164 (WhatsApp), a Telegram chat id, or `<chatId>:topic:<messageThreadId>`. `accountId`: with `target: "last"` it applies to the resolved channel if it supports accounts (else ignored); a non-matching id skips delivery.
- `prompt` is not merged (full override). `suppressToolErrorWarnings` (boolean) suppresses tool error warning payloads during heartbeat runs.
- `timeoutSeconds` (number, default = global timeout or `min(every, 600)`) — max seconds before the turn is aborted; unset uses `agents.defaults.timeoutSeconds`, else the cadence capped at 600s.
- `activeHours.timezone`: omitted/`"user"` uses `userTimezone` then host tz; `"local"` always host tz; any IANA id used directly (invalid → `"user"`).

## HEARTBEAT.md

If a `HEARTBEAT.md` file exists in the workspace, the default prompt tells the agent to read it — a "heartbeat checklist" that is small, stable, and safe to consider every 30 minutes. On normal runs it is only injected when heartbeat guidance is enabled for the default agent; disabling the cadence with `0m` or setting `includeSystemPromptSection: false` omits it. On the native Codex harness the content is not injected — if the file has non-whitespace content, the collaboration-mode instructions point Codex at the file to read before proceeding. If `HEARTBEAT.md` is effectively empty (only blank lines, comments, headings, fence markers, or empty checklist stubs), OpenClaw skips the run to save API calls (`reason=empty-heartbeat-file`); if missing, the heartbeat still runs and the model decides what to do. Keep it tiny to avoid prompt bloat, and do **not** put secrets (API keys, phone numbers, private tokens) into it — it becomes part of the prompt context.

### `tasks:` blocks

`HEARTBEAT.md` also supports a structured `tasks:` block for interval-based checks. Each entry carries a `name`, an `interval` (e.g. `30m`, `2h`), and a `prompt`:

```md
tasks:

- name: inbox-triage
  interval: 30m
  prompt: "Check for urgent unread emails and flag anything time sensitive."
- name: calendar-scan
  interval: 2h
  prompt: "Check for upcoming meetings that need prep or follow-up."

# Additional instructions

- Keep alerts short.
- If nothing needs attention after all due tasks, reply HEARTBEAT_OK.
```

Behavior: OpenClaw checks each task against its own `interval`; only **due** tasks enter the prompt for that tick. If no tasks are due, the run is skipped entirely (`reason=no-tasks-due`). Non-task content is preserved and appended after the due-task list. Last-run timestamps live in session state (`heartbeatTaskState`), so intervals survive normal restarts; timestamps advance only after a run completes its normal reply path (skipped `empty-heartbeat-file` / `no-tasks-due` runs do not mark tasks completed). Task mode lets one file hold several periodic checks without paying for all of them every tick.

### Can the agent update HEARTBEAT.md?

Yes — if you ask it to. `HEARTBEAT.md` is a normal workspace file, so you can tell the agent in chat "Update `HEARTBEAT.md` to add a daily calendar check." For proactive updates, include a line in your heartbeat prompt like "If the checklist becomes stale, update HEARTBEAT.md with a better one."

## Manual wake (on-demand)

Enqueue a system event and trigger an immediate heartbeat with:

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

If multiple agents have `heartbeat` configured, a manual wake runs each immediately. Use `--mode next-heartbeat` to wait for the next scheduled tick instead.

## Reasoning delivery (optional)

By default, heartbeats deliver only the final "answer" payload. Enabling `agents.defaults.heartbeat.includeReasoning: true` also delivers a separate message prefixed `Thinking` (same shape as `/reasoning on`). Useful when the agent manages multiple sessions/codexes and you want to see why it pinged you — but it can leak internal detail, so prefer keeping it off in group chats.

## Cost awareness

Heartbeats run full agent turns; shorter intervals burn more tokens. To reduce cost:

- `isolatedSession: true` avoids sending full conversation history (~100K tokens down to ~2-5K per run).
- `lightContext: true` limits bootstrap files to just `HEARTBEAT.md`.
- Set a cheaper `model` (e.g. `ollama/llama3.2:1b`).
- Keep `HEARTBEAT.md` small.
- `target: "none"` if you only want internal state updates.

## Context overflow after heartbeat

If a heartbeat previously left an existing session on a smaller local model — for example an Ollama model with a 32k window — and the next main-session turn reports context overflow, reset the session runtime model back to the configured primary model. OpenClaw's reset message calls this out when the last runtime model matches configured `heartbeat.model`. Current heartbeats preserve the shared session's existing runtime model after the run completes. You can still use `isolatedSession: true` for a fresh session, combine it with `lightContext: true` for the smallest prompt, or choose a heartbeat model with a large enough context window for the shared session.

**Source**: OpenClaw documentation — `gateway/heartbeat` (mirror `inbox/openclaw_docs/gateway/heartbeat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
