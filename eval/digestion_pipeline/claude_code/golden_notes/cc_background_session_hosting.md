---
tags:
  - resource
  - documentation
  - claude_code
  - agent_view
  - background_sessions
keywords:
  - background session hosting
  - supervisor process
  - per-user daemon
  - where state is stored
  - daemon.log roster.json jobs
  - claude_job_dir
  - claude daemon status
  - turn off agent view
  - session state persistence
topics:
  - Claude Code
  - Agent View
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-view
access_control_group: ["general"]
---

# Claude Code — How Background Sessions Are Hosted

## Overview

Every session listed in [agent view](cc_agent_view_monitor.md) is a **background session**, whether or not you are currently attached to it. Unlike a session started by running `claude` directly — which is tied to that terminal and ends when it closes — a background session keeps running with no terminal attached. This is made possible by a **per-user supervisor process** that hosts the sessions out-of-band, persists each session's state on disk, and restarts sessions from where they left off after they are stopped to free resources.

This note explains how that hosting works: the supervisor's lifecycle (auto-start, ~1-hour idle stop, pinned exemption, low-memory eviction, auto-updater restart), the on-disk state layout that makes sessions durable across restarts, and how to inspect or turn off the whole mechanism.

## The supervisor process

Background sessions are hosted by a **per-user supervisor process**, separate from your terminal and from agent view. The supervisor starts automatically the first time you background a session or open agent view, and you don't manage it directly. The supervisor and its sessions authenticate with the same credentials as your interactive sessions and make no additional network connections beyond the model API.

**Each background session is its own Claude Code process**, managed by the supervisor rather than tied to your terminal. A session stays alive (process running) when it is:

- Actively working,
- Waiting for your input, or
- Has a terminal attached.

A running **background shell command, [subagent](cc_dispatch_background_agents.md), dynamic workflow, or monitor counts as active work**, so a long-running process such as a dev server keeps the session alive.

**Idle stop and restore.** Once a session finishes and sits unattached for about an hour, the supervisor stops its process to free resources. A session you have pinned with `Ctrl+T` is exempt and keeps its process running while idle. The transcript and state stay on disk either way, and the next time you attach, peek, or reply to a stopped session, the supervisor **starts a fresh process from where it left off**. When every session has finished and no terminal is connected, the supervisor itself exits and starts again the next time you need it.

An empty row left over from pressing `←` that was never given a prompt is removed entirely after about five minutes so the list clears on its own. Sessions started with `claude --bg` and sessions waiting on a setup prompt such as a trust dialog are *not* removed this way.

**Low-memory eviction.** When the host runs low on memory, the supervisor stops idle non-pinned sessions first, and stops idle pinned ones only if that freed nothing.

**Auto-updater restart.** The supervisor watches the installed Claude Code binary on disk and restarts into the new version after the regular auto-updater replaces it. This is a local file watch, not a network check. Background sessions are detached processes, so they **keep running through the restart** and the new supervisor reconnects to them. An idle pinned session is also restarted in place onto the new version so it picks up the update without you reattaching.

## Where state is stored

Session state is stored under your Claude Code config directory. If you set `CLAUDE_CONFIG_DIR`, the supervisor uses that directory instead of `~/.claude` and runs as a **separate instance with its own sessions**.

| Path | Contents |
| :--- | :--- |
| `~/.claude/daemon.log` | Supervisor log |
| `~/.claude/daemon/roster.json` | List of running background sessions, used to reconnect after a restart |
| `~/.claude/jobs/<id>/state.json` | Per-session state shown in agent view |
| `~/.claude/jobs/<id>/tmp/` | Per-session scratch directory. Writes here don't prompt for permission. Removed when the session is deleted |

Each background session has the `CLAUDE_JOB_DIR` environment variable set to its `~/.claude/jobs/<id>` directory, so shell commands the session runs can write temporary files to `$CLAUDE_JOB_DIR/tmp` without colliding with parallel sessions.

To inspect this state without reading the files directly, run `claude daemon status`. It reports whether the supervisor is reachable, its process ID and version, the socket directory, and how many background sessions are live. `/doctor` includes a summary of the same check. On Windows, `claude daemon status` surfaces the underlying file error when the daemon's pipe-key file is locked or unreadable instead of reporting a generic connection failure.

## Persistence across sleep, shutdown, and stalls

Background sessions don't need any terminal open to keep working — a session state persists on disk through auto-updates and supervisor restarts. Sessions are also preserved when your machine **sleeps**: their processes resume on wake and the supervisor reconnects to them instead of treating the time gap as idle.

**Shutting down** the machine still stops running sessions, so they show as failed when you next open agent view. To recover them, attach, peek, or reply to any of them and the session restarts from where it left off. (Sleep alone does not cause this.)

If attaching, peeking, or `claude logs` reports that the background service did not respond, the supervisor process has likely stalled. Stop it and let the next `claude agents` start a fresh one; to keep your background sessions running through the restart, pass `--keep-workers`:

```bash
claude daemon stop --any --keep-workers
```

The new supervisor reconnects to the running sessions. Without `--keep-workers`, the command ends the background sessions too. The `--any` flag confirms you want to stop a supervisor that started on demand rather than as an installed service, which is the default. On Windows, if the supervisor does not respond to the stop request, the command prints its process ID; end that process with `taskkill /PID <pid>` to finish the recovery (background sessions are still preserved when you passed `--keep-workers`).

## Turn off agent view

To turn off background agents and agent view entirely, set the `disableAgentView` setting to `true` or set the `CLAUDE_CODE_DISABLE_AGENT_VIEW` environment variable. Administrators can enforce this through managed settings.

**Source**: https://code.claude.com/docs/en/agent-view
**Last Updated**: 2026-06-13
**Status**: Active
