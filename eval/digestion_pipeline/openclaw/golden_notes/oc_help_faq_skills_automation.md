---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - automation
keywords:
  - openclaw skills automation faq
  - skill load precedence
  - skills.load.extraDirs custom folder
  - per-task model agent routing
  - offload sub-agents subagents
  - thread-bound subagent sessions discord
  - cron standing order jobs
  - openclaw skills install linux
topics:
  - OpenClaw
  - Skills and Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — FAQ: Skills and Automation

## Overview

This note is the procedure layer for the **Skills and automation** H2 of the OpenClaw general FAQ (`help/faq`, mirror `inbox/openclaw_docs/help/faq.md`). It walks the supported patterns for customizing and loading skills without dirtying the repo, routing different models or settings per task, offloading heavy work to sub-agents, binding sub-agent sessions to Discord threads, debugging sub-agent completion delivery, scheduling cron / standing-order jobs, and installing skills on Linux. Every config key, env var, slash command, and CLI invocation below is copied verbatim from the FAQ accordions; deep how-tos the answers point to (`/automation/cron-jobs`, `/concepts/multi-agent`, `/tools/subagents`, `/tools/skills`) live in their owning sub-plans and are referenced, not re-digested.

## Customizing Skills Without a Dirty Repo

Use **managed overrides** instead of editing the bundled repo copy. Put changes in `~/.openclaw/skills/<name>/SKILL.md`, or add a folder via `skills.load.extraDirs` in `~/.openclaw/openclaw.json`. The skill **load precedence** (highest → lowest) is `<workspace>/skills` → `<workspace>/.agents/skills` → `~/.agents/skills` → `~/.openclaw/skills` → bundled → `skills.load.extraDirs`, so a managed override in `~/.openclaw/skills` still wins over a bundled skill without touching git. `skills.load.extraDirs` sits at the **lowest** precedence. Only upstream-worthy edits should live in the repo and ship as PRs.

To install a skill globally but expose it to only some agents, keep the shared copy in `~/.openclaw/skills` and control visibility with `agents.defaults.skills` and `agents.list[].skills`. `clawhub` installs into `./skills` by default, which OpenClaw treats as `<workspace>/skills` on the next session.

## Different Models or Settings per Task

Three patterns are supported today for varying model/settings per task: **cron jobs** (an isolated job can set a `model` override per job), **agents** (route tasks to separate agents with different default models, thinking levels, and stream params), and an **on-demand switch** (`/model` switches the current session model at any time). The example below uses the same model with different per-agent settings:

```json5
{
  agents: {
    list: [
      {
        id: "coder",
        model: "xiaomi/mimo-v2.5-pro",
        thinkingDefault: "high",
        params: { temperature: 0.1 },
      },
      {
        id: "chat",
        model: "xiaomi/mimo-v2.5-pro",
        thinkingDefault: "off",
        params: { temperature: 0.8 },
      },
    ],
  },
}
```

Put shared per-model defaults in `agents.defaults.models["provider/model"].params`, then put agent-specific overrides in flat `agents.list[].params`. Do **not** define separate nested `agents.list[].models["provider/model"].params` entries for the same model — `agents.list[].models` is for the per-agent model catalog and runtime overrides, not per-agent params.

## Offloading Heavy Work to Sub-Agents

When the bot freezes during long or parallel work, use **sub-agents**: they run in their own session, return a summary, and keep the main chat responsive. Ask the bot to "spawn a sub-agent for this task" or use `/subagents`. Use `/status` in chat to see what the Gateway is doing right now and whether it is busy. Long tasks and sub-agents both consume tokens; if cost is a concern, set a cheaper model for sub-agents via `agents.defaults.subagents.model`.

## Thread-Bound Sub-Agent Sessions on Discord

Bind a Discord thread to a sub-agent or session target so follow-up messages in that thread stay on the bound session. Basic flow:

- Spawn with `sessions_spawn` using `thread: true` (and optionally `mode: "session"` for persistent follow-up).
- Or manually bind with `/focus <target>`.
- Use `/agents` to inspect binding state.
- Use `/session idle <duration|off>` and `/session max-age <duration|off>` to control auto-unfocus.
- Use `/unfocus` to detach the thread.

Required config — global defaults: `session.threadBindings.enabled`, `session.threadBindings.idleHours`, `session.threadBindings.maxAgeHours`. Discord overrides: `channels.discord.threadBindings.enabled`, `channels.discord.threadBindings.idleHours`, `channels.discord.threadBindings.maxAgeHours`. Auto-bind on spawn: `channels.discord.threadBindings.spawnSessions` defaults to `true`; set it to `false` to disable thread-bound session spawns.

## Sub-Agent Completion Went to the Wrong Place

When a sub-agent finishes but the completion update went to the wrong place or never posted, check the resolved requester route first: completion-mode sub-agent delivery prefers any bound thread or conversation route when one exists; if the completion origin only carries a channel, OpenClaw falls back to the requester session's stored route (`lastChannel` / `lastTo` / `lastAccountId`) so direct delivery can still succeed; if neither a bound route nor a usable stored route exists, direct delivery can fail and the result falls back to queued session delivery instead of posting immediately to chat; invalid or stale targets can still force queue fallback or final delivery failure; if the child's last visible assistant reply is the exact silent token `NO_REPLY` / `no_reply`, or exactly `ANNOUNCE_SKIP`, OpenClaw intentionally suppresses the announce instead of posting stale earlier progress; and tool/toolResult output is not promoted into child result text — the result is the child's latest visible assistant reply. Debug with:

```bash
openclaw tasks show <runId-or-sessionKey>
```

## Cron and Standing-Order Automation

OpenClaw can run tasks on a schedule or continuously via the Gateway scheduler: **cron jobs** for scheduled or recurring tasks (they persist across restarts), **heartbeat** for "main session" periodic checks, and **isolated jobs** for autonomous agents that post summaries or deliver to chats.

**Cron or reminders do not fire.** Cron runs *inside* the Gateway process, so if the Gateway is not running continuously, scheduled jobs will not run. Checklist: confirm cron is enabled (`cron.enabled`) and that `OPENCLAW_SKIP_CRON` is not set; check the Gateway is running 24/7 (no sleep/restarts); verify timezone settings for the job (`--tz` vs host timezone). Debug:

```bash
openclaw cron run <jobId>
openclaw cron runs --id <jobId> --limit 50
```

**Cron fired, but nothing was sent to the channel.** Check the delivery mode first: `--no-deliver` / `delivery.mode: "none"` means no runner fallback send is expected; a missing or invalid announce target (`channel` / `to`) means the runner skipped outbound delivery; channel auth failures (`unauthorized`, `Forbidden`) mean the runner tried to deliver but credentials blocked it; a silent isolated result (`NO_REPLY` / `no_reply` only) is treated as intentionally non-deliverable, so the runner also suppresses queued fallback delivery. For isolated cron jobs the agent can still send directly with the `message` tool when a chat route is available; `--announce` only controls the runner fallback path for final text the agent did not already send.

**Why an isolated cron run switched models or retried once.** That is usually the live model-switch path, not duplicate scheduling. Isolated cron can persist a runtime model handoff and retry when the active run throws `LiveSessionModelSwitchError`; the retry keeps the switched provider/model, and if the switch carried a new auth profile override, cron persists that too before retrying. Selection rules in order: a Gmail hook model override wins first when applicable, then per-job `model`, then any stored cron-session model override, then the normal agent/default model selection. The retry loop is bounded — after the initial attempt plus 2 switch retries, cron aborts instead of looping forever.

## Installing Skills on Linux

On Linux, use the native `openclaw skills` commands or drop skills into your workspace (the macOS Skills UI is not available on Linux); browse skills at `https://clawhub.ai`:

```bash
openclaw skills search "calendar"
openclaw skills search --limit 20
openclaw skills install <skill-slug>
openclaw skills install <skill-slug> --version <version>
openclaw skills install <skill-slug> --force
openclaw skills install <skill-slug> --global
openclaw skills update --all
openclaw skills update --all --global
openclaw skills list --eligible
openclaw skills check
```

Native `openclaw skills install` writes into the active workspace `skills/` directory by default; add `--global` to install into the shared managed skills directory for all local agents. Install the separate `clawhub` CLI only if you want to publish or sync your own skills. Use `agents.defaults.skills` or `agents.list[].skills` to narrow which agents can see shared skills.

**macOS-only skills from Linux.** Not directly: macOS skills are gated by `metadata.openclaw.os` plus required binaries, and a skill only appears in the system prompt when it is eligible on the **Gateway host**, so `darwin`-only skills (e.g. `apple-notes`, `apple-reminders`, `things-mac`) will not load on Linux unless you override the gating. The three supported patterns are (A) run the Gateway on a Mac and connect from Linux in remote mode / over Tailscale; (B) run the Gateway on Linux and pair a macOS node (menubar app) with **Node Run Commands** set to "Always Ask" or "Always Allow", so OpenClaw treats macOS-only skills as eligible when the required binaries exist on the node and runs them via the `nodes` tool; or (C) proxy the required macOS CLI binaries over SSH wrappers on the Linux host and override the skill metadata (`os: ["darwin", "linux"]`) so it stays eligible, then start a new session so the skills snapshot refreshes.

**Source**: OpenClaw documentation — `help/faq` § Skills and automation (mirror `inbox/openclaw_docs/help/faq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
