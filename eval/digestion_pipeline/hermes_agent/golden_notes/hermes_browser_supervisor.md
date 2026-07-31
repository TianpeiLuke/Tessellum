---
tags:
  - resource
  - documentation
  - hermes_agent
  - browser_automation
  - dev_internals
keywords:
  - browser cdp supervisor
  - native js dialog
  - cross-origin iframe oopif
  - cdpsupervisor websocket
  - browser_dialog tool
  - browser_snapshot extension
topics:
  - Hermes Agent
  - Browser Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/browser-supervisor
access_control_group: ["general"]
---

# Hermes Browser CDP Supervisor

## Overview

The Browser CDP Supervisor is the runtime subsystem that lets a Hermes browser session detect and respond to native JavaScript dialogs and interact with cross-origin iframes — the two gaps plain CDP `Runtime.evaluate` cannot reach. Both are blind spots in ordinary browser tooling: native dialogs (`alert`/`confirm`/`prompt`/`beforeunload`) freeze the page's JS thread so the agent has no signal a dialog is open (subsequent tool calls hang or throw opaque errors), and cross-origin iframes (OOPIFs) are invisible to top-level `Runtime.evaluate` — the agent sees the iframe node in a DOM snapshot but cannot click, type, or eval inside it without a CDP session attached to the child target.

The supervisor closes both gaps by holding **one persistent WebSocket per browser `task_id`** to the backend's Chrome DevTools Protocol (CDP) endpoint, surfacing pending dialogs and frame structure into the existing `browser_snapshot` output, and exposing a response-only `browser_dialog` tool. It is a behavior layer over the CDP connection; the model never sees a new schema for snapshot fields, and availability is gated on whether a CDP endpoint is actually reachable so Camofox / no-backend sessions incur no schema bloat.

## Backend support

Three browser backends, three levels of CDP capability:

| Backend | Dialog detect | Dialog respond | Frame tree | OOPIF `Runtime.evaluate` via `browser_cdp(frame_id=...)` |
|---|---|---|---|---|
| Local Chrome (`--remote-debugging-port`) / `/browser connect` | ✓ | ✓ full workflow | ✓ | ✓ |
| Browserbase | ✓ (via bridge) | ✓ full workflow (via bridge) | ✓ | ✓ |
| Camofox | ✗ no CDP (REST-only) | ✗ | partial via DOM snapshot | ✗ |

**Browserbase quirk.** Browserbase's CDP proxy uses Playwright internally and auto-dismisses native dialogs within ~10ms, so `Page.handleJavaScriptDialog` can't keep up. The supervisor instead injects a bridge script via `Page.addScriptToEvaluateOnNewDocument` that overrides `window.alert`/`confirm`/`prompt` with a synchronous XHR to a magic host (`hermes-dialog-bridge.invalid`). `Fetch.enable` intercepts those XHRs before they touch the network — the dialog becomes a `Fetch.requestPaused` event the supervisor captures, and `respond_to_dialog` fulfills via `Fetch.fulfillRequest` with a JSON body the injected script decodes. From the page's perspective `prompt()` still returns the agent-supplied string; from the agent's perspective it is the same `browser_dialog(action=...)` API either way. Camofox is unsupported — no CDP surface, REST-only.

## Architecture

### CDPSupervisor

One `asyncio.Task` running in a background daemon thread per Hermes `task_id`, holding a persistent WebSocket to the backend's CDP endpoint. It maintains four pieces of state:

- **Dialog queue** — `List[PendingDialog]` of `{id, type, message, default_prompt, session_id, opened_at}`.
- **Frame tree** — `Dict[frame_id, FrameInfo]` with parent relationships, URL, origin, and whether the entry is a cross-origin child session.
- **Session map** — `Dict[session_id, SessionInfo]` so interaction tools can route to the right attached session for OOPIF operations.
- **Recent console errors** — a ring buffer of the last 50 for diagnostics.

On attach it subscribes to: `Page.enable` (`javascriptDialogOpening`, `frameAttached`, `frameNavigated`, `frameDetached`); `Runtime.enable` (`executionContextCreated`, `consoleAPICalled`, `exceptionThrown`); and `Target.setAutoAttach {autoAttach: true, flatten: true}`, which surfaces child OOPIF targets — the supervisor then enables `Page`+`Runtime` on each. State access is thread-safe via a snapshot lock; the (synchronous) tool handlers read a frozen snapshot without awaiting.

### Lifecycle

Get-or-start lifecycle keyed by `task_id`:

- **Start:** `SupervisorRegistry.get_or_start(task_id, cdp_url)` — called by `browser_navigate`, Browserbase session create, and `/browser connect`. **Idempotent.**
- **Stop:** session teardown or `/browser disconnect` — cancels the asyncio task, closes the WebSocket, discards state.
- **Rebind:** if the CDP URL changes (user reconnects to a new Chrome), the old supervisor is stopped and a fresh one started — state is never reused across endpoints.

### Dialog policy

Configurable in `config.yaml` under `browser.dialog_policy`, per-task (no per-dialog overrides):

- **`must_respond`** (default) — capture, surface in `browser_snapshot`, and wait for an explicit `browser_dialog(action=...)` call. After a 300s safety timeout with no response, auto-dismiss and log — preventing a buggy agent from stalling forever.
- `auto_dismiss` — record and dismiss immediately; the agent sees it after the fact via `browser_state` inside `browser_snapshot`.
- `auto_accept` — record and accept (useful for `beforeunload` where the workflow wants to navigate away cleanly).

## Agent surface

### `browser_dialog` tool

```
browser_dialog(action, prompt_text=None, dialog_id=None)
```

- `action="accept"` / `"dismiss"` → responds to the specified or sole pending dialog (required).
- `prompt_text=...` → text to supply to a `prompt()` dialog.
- `dialog_id=...` → disambiguate when multiple dialogs are queued (rare).

The tool is **response-only**: the agent reads pending dialogs from `browser_snapshot` output before calling.

### `browser_snapshot` extension

When a supervisor is attached, the snapshot gains three optional fields:

```json
{
  "pending_dialogs": [
    {"id": "d-1", "type": "alert", "message": "Hello", "opened_at": 1650000000.0}
  ],
  "recent_dialogs": [
    {"id": "d-1", "type": "alert", "message": "...", "opened_at": 1650000000.0,
     "closed_at": 1650000000.1, "closed_by": "remote"}
  ],
  "frame_tree": {
    "top": {"frame_id": "FRAME_A", "url": "https://example.com/", "origin": "https://example.com"},
    "children": [
      {"frame_id": "FRAME_B", "url": "about:srcdoc", "is_oopif": false},
      {"frame_id": "FRAME_C", "url": "https://ads.example.net/", "is_oopif": true, "session_id": "SID_C"}
    ],
    "truncated": false
  }
}
```

- **`pending_dialogs`** — dialogs currently blocking the page's JS thread; the agent must call `browser_dialog(action=...)` to respond. Empty on Browserbase because their CDP proxy auto-dismisses within ~10ms.
- **`recent_dialogs`** — ring buffer of up to 20 recently-closed dialogs with a `closed_by` tag: `"agent"`, `"auto_policy"`, `"watchdog"` (must_respond timeout), or `"remote"` (browser/backend closed it, e.g. Browserbase). This is how Browserbase agents still get visibility.
- **`frame_tree`** — frame structure including cross-origin (OOPIF) children, capped at 30 entries + OOPIF depth 2 to bound snapshot size on ad-heavy pages. `truncated: true` surfaces when limits were hit; agents needing the full tree use `browser_cdp` with `Page.getFrameTree`.

There is **no new tool schema** for any of these — the agent reads the snapshot it already requests.

### Availability gating

Both surfaces gate on `_browser_cdp_check` (the supervisor can only run when a CDP endpoint is reachable). On Camofox / no-backend sessions the dialog tool is hidden and the snapshot omits the new fields — no schema bloat.

## Cross-origin iframe interaction

`browser_cdp(frame_id=...)` routes CDP calls (notably `Runtime.evaluate`) through the supervisor's already-connected WebSocket using the OOPIF's child `sessionId`. Agents pick `frame_id`s out of `browser_snapshot.frame_tree.children[]` where `is_oopif=true`. For same-origin iframes (no dedicated CDP session) the agent uses `contentWindow`/`contentDocument` from a top-level `Runtime.evaluate` instead — the supervisor surfaces an error pointing at that fallback when a `frame_id` belongs to a non-OOPIF. On Browserbase this is the **only** reliable path for iframe interaction: stateless CDP connections (opened per `browser_cdp` call) hit signed-URL expiry, while the supervisor's long-lived connection keeps a valid session.

## File layout

- `tools/browser_supervisor.py` — `CDPSupervisor`, `SupervisorRegistry`, `PendingDialog`, `FrameInfo`.
- `tools/browser_dialog_tool.py` — the `browser_dialog` tool handler.
- `tools/browser_tool.py` — `browser_navigate` start-hook, `browser_snapshot` merge, `/browser connect` reattach, `_cleanup_browser_session` teardown.
- `toolsets.py` — registers `browser_dialog` in `browser`, `hermes-acp`, `hermes-api-server`, and core toolsets (gated on CDP reachability).
- `hermes_cli/config.py` — `browser.dialog_policy` and `browser.dialog_timeout_s` defaults.

## Non-goals

Explicitly out of scope: detection/interaction for Camofox (upstream gap, tracked separately); streaming dialog/frame events live to the user (would require gateway hooks); persisting dialog history across sessions (in-memory only); per-iframe dialog policies (the agent can express this via `dialog_id`); and replacing `browser_cdp` — it stays as the escape hatch for the long tail (cookies, viewport, network throttling).

## Testing

Unit tests (`tests/tools/test_browser_supervisor.py`) use an asyncio mock CDP server that speaks enough of the protocol to exercise all state transitions: attach, enable, navigate, dialog fire, dialog dismiss, frame attach/detach, child target attach, session teardown. Real-backend E2E (Browserbase + a local Chromium-family browser) is manual — exercised via `/browser connect` to a live browser and running the dialog/frame cases above.

**Source**: `inbox/hermes_agent_docs/developer-guide/browser-supervisor.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/browser-supervisor
**Last Updated**: 2026-06-19
**Status**: Active
