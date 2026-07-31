---
tags:
  - resource
  - documentation
  - hermes_agent
  - browser_automation
  - tools
keywords:
  - browser automation
  - browser backends
  - accessibility tree
  - browser tools
  - CDP passthrough
  - session isolation
topics:
  - Hermes Agent
  - Browser Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
access_control_group: ["general"]
---

# Hermes Agent — Browser Automation Backends & Tool Surface

## Overview

Browser automation in Hermes Agent is a **multi-backend browser-control model**: a single `browser_*` tool surface that the agent drives, sitting on top of any of six interchangeable browser backends. The model is what the backends ARE and what the tool surface exposes; the per-backend setup procedure (API keys, Docker, `/browser connect`, env knobs, worked examples) is the sibling [hermes_browser_automation_setup](hermes_browser_automation_setup.md).

The six backend modes are: **Browserbase cloud**, **Browser Use cloud**, and **Firecrawl cloud** (managed cloud browsers, no local browser needed); **Camofox local mode** (a self-hosted Firefox-based anti-detection browser); **Local Chromium-family CDP** (attach to your own running Chrome / Brave / Chromium / Edge via the Chrome DevTools Protocol with `/browser connect`); and **Local browser mode** (the `agent-browser` CLI driving a local Chromium install). In all modes the agent can navigate websites, interact with page elements, fill forms, and extract information.

The distinguishing design choice: pages are represented as **accessibility trees** (text-based snapshots) rather than pixels, so an LLM agent can reason over them directly. Interactive elements receive ref IDs (`@e1`, `@e2`, …) that the agent passes to `browser_click` and `browser_type`. A persistent CDP supervisor (one WebSocket per task) backs native-dialog detection and the cross-origin-iframe frame tree. Each task gets its own isolated session with automatic inactivity cleanup.

## Backend Modes

The model enumerates six backends with one tool surface across all of them:

- **Browserbase cloud mode** — managed cloud browsers with anti-bot tooling.
- **Browser Use cloud mode** — an alternative cloud browser provider (a cloud browser via its REST API). When both Browserbase and Browser Use credentials are set, **Browserbase takes priority**.
- **Firecrawl cloud mode** — cloud browsers with built-in scraping.
- **Camofox local mode** — a self-hosted Node.js server wrapping Camoufox (a Firefox fork with C++ fingerprint spoofing) for local anti-detection browsing without cloud dependencies. When `CAMOFOX_URL` is set, all browser tools automatically route through Camofox.
- **Local Chromium-family CDP** — attach to your own Chrome, Brave, Chromium, or Edge via CDP using `/browser connect`. When connected, all browser tools operate on the live browser instead of a cloud session.
- **Local browser mode** — with no cloud credentials and no `/browser connect`, Hermes drives a local Chromium install through the `agent-browser` CLI.

## Overview (Accessibility-Tree Representation)

Pages are represented as **accessibility trees** (text-based snapshots), making them ideal for LLM agents. Interactive elements get ref IDs (like `@e1`, `@e2`) that the agent uses for clicking and typing. Key capabilities of the model:

- **Multi-provider cloud execution** — Browserbase, Browser Use, or Firecrawl — no local browser needed.
- **Local Chromium-family integration** — attach to a running Chrome, Brave, Chromium, or Edge via CDP for hands-on browsing.
- **Built-in stealth** — random fingerprints, CAPTCHA solving, residential proxies (Browserbase).
- **Session isolation** — each task gets its own browser session.
- **Automatic cleanup** — inactive sessions are closed after a timeout.
- **Vision analysis** — screenshot + AI analysis for visual understanding.

## Available Tools

The agent drives twelve `browser_*` tools. `browser_navigate` must be called before any other browser tool — it initializes the session. The tools below are the model's full surface (concise text examples kept verbatim where load-bearing; tables rendered in prose):

- **`browser_navigate`** — navigate to a URL; must precede every other browser tool. The source steers users toward `web_search`/`web_extract` for simple retrieval and reserves browser tools for genuine page **interaction**.
- **`browser_snapshot`** — text snapshot of the current page's accessibility tree, returning interactive elements with ref IDs (`@e1`, `@e2`). `full=false` (default) shows only interactive elements; `full=true` gives complete page content. Snapshots over 8000 characters are automatically summarized by an LLM.
- **`browser_click`** — click an element by its ref ID from the snapshot.
- **`browser_type`** — type text into an input field (clears the field first, then types).
- **`browser_scroll`** — scroll the page up or down to reveal more content.
- **`browser_press`** — press a keyboard key (`Enter`, `Tab`, `Escape`, `ArrowDown`, `ArrowUp`, and more); useful for submitting forms or navigation.
- **`browser_back`** — navigate back to the previous page in browser history.
- **`browser_get_images`** — list all images on the page with URLs and alt text.
- **`browser_vision`** — take a screenshot and analyze it with vision AI; used when text snapshots miss visual information (CAPTCHAs, complex layouts, visual verification). The screenshot is saved persistently and its file path returned alongside the AI analysis; on messaging platforms it can be shared as a native photo via the `MEDIA:` mechanism. Screenshots are stored in `~/.hermes/cache/screenshots/` and cleaned up after 24 hours.
- **`browser_console`** — get console output (log/warn/error) and uncaught JS exceptions; `clear=True` clears after reading. Also evaluates JavaScript when given an `expression` argument — same shape as the DevTools console, with results parsed (JSON-serialized objects become dicts):

```
browser_console(expression="document.querySelector('h1').textContent")
browser_console(expression="JSON.stringify(performance.timing)")
```

When a CDP supervisor is active for the session, evaluation runs over the supervisor's persistent WebSocket (no subprocess startup cost), otherwise it falls through to the agent-browser CLI path; behaviour is identical, only latency changes.

- **`browser_cdp`** — raw Chrome DevTools Protocol passthrough, the escape hatch for operations not covered by the other tools (native dialog handling, iframe-scoped evaluation, cookie/network control, any CDP verb). **Only available when a CDP endpoint is reachable at session start** — i.e. `/browser connect` has attached to a running Chromium-family browser, or `browser.cdp_url` is set. Default local agent-browser mode, Camofox, and the cloud providers do not currently expose CDP to this tool. Browser-level methods (`Target.*`, `Browser.*`, `Storage.*`) omit `target_id`; page-level methods (`Page.*`, `Runtime.*`, `DOM.*`, `Emulation.*`) require a `target_id` from `Target.getTargets`. Common patterns:

```
# List tabs (browser-level, no target_id)
browser_cdp(method="Target.getTargets")

# Handle a native JS dialog on a tab
browser_cdp(method="Page.handleJavaScriptDialog",
            params={"accept": true, "promptText": ""},
            target_id="<tabId>")
```

For **cross-origin iframes**, pass `frame_id` (from `browser_snapshot.frame_tree.children[]` where `is_oopif=true`) to route the call through the supervisor's live session for that iframe — this is how `Runtime.evaluate` inside a cross-origin iframe works on Browserbase, where stateless CDP connections would hit signed-URL expiry. Same-origin iframes don't need `frame_id`.

- **`browser_dialog`** — respond to a native JS dialog (`alert` / `confirm` / `prompt` / `beforeunload`). Before this tool, dialogs silently blocked the page's JS thread and subsequent `browser_*` calls would hang; now pending dialogs appear in `browser_snapshot` output and the agent responds explicitly. Workflow: snapshot (a blocking dialog shows as `pending_dialogs: [{"id": "d-1", "type": "alert", "message": "..."}]`), then `browser_dialog(action="accept")` or `action="dismiss"` (pass `prompt_text="..."` for `prompt()`), then re-snapshot to confirm `pending_dialogs` is empty.

**Native-dialog detection happens automatically** via a persistent CDP supervisor — one WebSocket per task subscribing to Page/Runtime/Target events. The supervisor also populates a `frame_tree` field in the snapshot (capped to 30 frames and OOPIF depth 2; a `truncated: true` flag surfaces when limits were hit). Dialog detection/response is available on local Chrome via `/browser connect` or `browser.cdp_url` and on Browserbase (via an injected XHR bridge), but not on Camofox or the default local agent-browser (no CDP endpoint). The dialog policy is configured under `browser.dialog_policy`: `must_respond` (default — capture, surface, wait, with a safety auto-dismiss after `browser.dialog_timeout_s`, default 300s), `auto_dismiss`, or `auto_accept`.

## Session Recording

Browser sessions can be recorded automatically as WebM video files via `browser.record_sessions: true` (default `false`). Recording starts on the first `browser_navigate` and saves to `~/.hermes/browser_recordings/` when the session closes. It works in both local and cloud (Browserbase) modes; recordings older than 72 hours are automatically cleaned up.

## Stealth Features

Browserbase provides automatic stealth capabilities: **Basic Stealth** (always on — random fingerprints, viewport randomization, CAPTCHA solving), **Residential Proxies** (on — routes through residential IPs for better access), **Advanced Stealth** (off — custom Chromium build, requires Scale Plan), and **Keep Alive** (on — session reconnection after network hiccups). If paid features aren't available on a plan, Hermes automatically falls back — first disabling `keepAlive`, then proxies — so browsing still works on free plans.

## Session Management

- Each task gets an isolated browser session via Browserbase.
- Sessions are automatically cleaned up after inactivity (default: 2 minutes).
- A background thread checks every 30 seconds for stale sessions.
- Emergency cleanup runs on process exit to prevent orphaned sessions.
- Sessions are released via the Browserbase API (`REQUEST_RELEASE` status).

## Limitations

- **Text-based interaction** — relies on the accessibility tree, not pixel coordinates.
- **Snapshot size** — large pages may be truncated or LLM-summarized at 8000 characters.
- **Session timeout** — cloud sessions expire based on the provider's plan settings.
- **Cost** — cloud sessions consume provider credits; sessions are cleaned up when the conversation ends or after inactivity. Use `/browser connect` for free local browsing.
- **No file downloads** — cannot download files from the browser.

**Source**: `inbox/hermes_agent_docs/user-guide/features/browser.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
**Last Updated**: 2026-06-19
**Status**: Active
