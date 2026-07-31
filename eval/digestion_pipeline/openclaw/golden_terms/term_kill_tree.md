---
tags:
  - resource
  - terminology
  - kill-tree
  - process-management
  - cross-platform-termination
  - openclaw
keywords:
  - Kill-tree
  - process tree termination
  - taskkill /T
  - SIGTERM SIGKILL pgroup
  - tree-kill
  - process group leader
topics:
  - Process management
  - Cross-platform OS
  - OpenClaw process subsystem
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Process_group
access_control_group: ["general"]
---

# Kill-Tree

## Definition

**Kill-tree** is the operation of terminating a parent process **plus every descendant process it spawned** in a single best-effort sweep, typically followed by a force-kill escalation if a member of the tree refuses to exit within a grace window. It exists as a named concept because no single cross-platform system call delivers it: on POSIX systems the kernel only guarantees signal delivery to a single PID (`kill(2)`) or to an explicit process group (`killpg(3)`), and on Windows the per-process `TerminateProcess` API has no notion of descendants at all. A portable kill-tree must therefore enumerate or group children itself and dispatch the right primitive per platform.

In Node.js specifically, the standard library's `child.kill()` only sends a signal to the **direct** child PID — any grandchildren the child spawned (a shell pipeline, a compiler, a debounced worker pool) are orphaned and reparented to PID 1 rather than terminated. This gap is precisely what the npm `tree-kill` package (the canonical industry reference) and OpenClaw's `src/process/kill-tree.ts` (124 LOC) fill, and why every long-running Node agent runtime ships its own variant of this logic.

## Context

Two operating-system mechanisms underpin every kill-tree implementation. On Linux/macOS the convention is **POSIX process groups**: when a child is spawned with `setsid()` (Node exposes this as the `detached: true` option on `child_process.spawn`), it becomes the leader of a new process group, and any further descendants inherit that group ID, so `killpg(pgid, SIGTERM)` (equivalently `process.kill(-pid, "SIGTERM")` from Node) hits the whole subtree in one syscall — followed by `SIGKILL` after a grace period for stragglers, exactly as Docker and Kubernetes pod-shutdown do. On Windows the equivalent is **`taskkill /T`** (Microsoft Learn's `taskkill` reference: "ends the specified process and any child processes started by it"), optionally combined with **`/F`** to force-kill processes that ignore the polite shutdown. Win32 Job Objects offer a more authoritative grouping mechanism, but `taskkill /T /F` is the universally portable shell entry point and what every Node-side library actually invokes.

The npm `tree-kill` package by Peteris Krumins (1,299+ dependents, the de facto industry standard) wires both sides: on Linux it walks `ps -o pid --ppid <pid>`, on macOS it walks `pgrep -P <pid>`, on Windows it shells out to `taskkill /pid <PID> /T /F`. Python's `psutil` exposes the same pattern via `Process.children(recursive=True)` plus `send_signal()`. OpenClaw's `kill-tree.ts` mirrors `tree-kill`'s shape but specializes for an **agent-runtime** caller — it adds a graceful-first-then-force ladder, a `detached: false` guard against accidentally SIGTERMing the gateway's own process group, and a `.unref()` escalation timer so a pending force-kill never holds the Node event loop open past intended exit. Inside OpenClaw, it's invoked on subagent exec timeout, on gateway daemon stop (`launchd`/`systemd`/`schtasks` lifecycle), and on the ACP `Cancel` method when a user aborts a long-running tool call.

## Key Characteristics

- **Single platform-dispatch entry point**: one `killProcessTree(pid, opts)` call branches on `process.platform === "win32"`; callers never touch OS primitives directly.
- **Unix path — process-group SIGTERM with direct-PID fallback**: prefers `process.kill(-pid, "SIGTERM")` to hit the whole pgroup; on `EPERM`/`ESRCH` falls back to `process.kill(pid, "SIGTERM")` so non-`setsid` children (spawned without `detached: true`) still get a chance.
- **Detached-flag guard**: when the child was NOT spawned detached (service-managed runtime case), `process.kill(-pid, ...)` would target the **gateway's own pgroup** — the caller passes `detached: false` to skip group-kill entirely (Node issue #71662 in OpenClaw's notes).
- **Grace-period timer with escalate-to-SIGKILL**: after `graceMs` (default 3000, clamped to `[0, 60_000]`), checks `process.kill(pid, 0)` liveness; only if still alive does it send `SIGKILL` — avoiding unconditional force-kills that race with clean exit.
- **Windows path — graceful taskkill then force taskkill**: first `taskkill /T /PID <pid>` (no `/F`, so descendants get WM_CLOSE/console CTRL_BREAK), then on grace-window expiry and liveness re-check, `taskkill /F /T /PID <pid>`.
- **Detached, fire-and-forget spawn semantics**: each `taskkill` invocation uses `spawn("taskkill", args, { detached: true, stdio: "ignore", windowsHide: true })` and swallows spawn failures — the kill-tree caller never blocks on or awaits the OS tool.
- **Idempotent over already-dead PIDs**: every step is wrapped in `try`/`catch` against `ESRCH`; calling kill-tree on a zombie or already-reaped PID is a no-op rather than an error.
- **Non-blocking timer via `.unref()`**: the escalation `setTimeout` is unrefed so a pending hard-kill never holds Node alive past the agent's intended exit.

## Related Terms


## Related Code Snippets

- [snippet_openclaw_process_kill_tree.md](../code_snippets/snippet_openclaw_process_kill_tree.md): the 124-LOC `killProcessTree` implementation — platform dispatch, Unix pgroup SIGTERM with direct-pid fallback, escalate-only-if-alive timer, fire-and-forget detached `taskkill` spawn.

## References

- [taskkill — Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/taskkill)
- [signal(7) — Linux manual page](https://man7.org/linux/man-pages/man7/signal.7.html)
- [Process group — Wikipedia](https://en.wikipedia.org/wiki/Process_group)
- [node-tree-kill (pkrumins) — canonical npm reference](https://github.com/pkrumins/node-tree-kill)
- [Node.js `child_process` documentation](https://nodejs.org/api/child_process.html)
