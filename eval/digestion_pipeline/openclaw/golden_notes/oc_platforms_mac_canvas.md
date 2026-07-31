---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - canvas
keywords:
  - openclaw macos canvas panel
  - wkwebview canvas
  - openclaw-canvas custom url scheme
  - canvas agent api present navigate eval snapshot
  - a2ui v0.8 in canvas
  - openclaw://agent deep link
  - canvas directory traversal block
  - gateway websocket canvas host
topics:
  - OpenClaw
  - Platforms
  - Canvas
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms/mac/canvas
access_control_group: ["general"]
---

# OpenClaw — macOS Agent-Controlled Canvas Panel

## Overview

This note models the OpenClaw **Canvas panel** on macOS: a lightweight, agent-controlled visual workspace that the macOS app embeds using `WKWebView` for HTML/CSS/JS, A2UI, and small interactive UI surfaces. It covers where Canvas content lives (the `openclaw-canvas://` custom URL scheme over per-session Application-Support storage), the panel's runtime behavior and disable switch, the Gateway-WebSocket agent API (present/navigate/eval/snapshot), how A2UI v0.8 is hosted and pushed into the panel, the `openclaw://agent` deep-link trigger for new agent runs, and the scheme's traversal/external-URL security properties — mirroring the `platforms/mac/canvas` source page.

## Where Canvas Lives — Custom URL Scheme and Storage

Canvas state is stored under macOS Application Support at `~/Library/Application Support/OpenClaw/canvas/<session>/...`, so each session has its own canvas root. The Canvas panel serves those files via a **custom URL scheme** of the form `openclaw-canvas://<session>/<path>`. The source gives three resolution examples: `openclaw-canvas://main/` maps to `<canvasRoot>/main/index.html`; `openclaw-canvas://main/assets/app.css` maps to `<canvasRoot>/main/assets/app.css`; and `openclaw-canvas://main/widgets/todo/` maps to `<canvasRoot>/main/widgets/todo/index.html`. If no `index.html` exists at the root, the app shows a **built-in scaffold page** instead of failing.

## Panel Behavior

The Canvas panel is a borderless, resizable panel anchored near the menu bar (or the mouse cursor). It remembers its size and position **per session**, and it auto-reloads when local canvas files change. Only one Canvas panel is visible at a time — the session is switched as needed rather than showing multiple panels simultaneously. Canvas can be disabled from Settings → **Allow Canvas**; when disabled, canvas node commands return `CANVAS_DISABLED`.

## Agent API Surface — Gateway WebSocket

Canvas is exposed via the **Gateway WebSocket**, which lets the agent drive the panel programmatically. Through that surface the agent can show/hide the panel, navigate to a path or URL, evaluate JavaScript, and capture a snapshot image. The source documents these as `openclaw nodes canvas` CLI commands:

```bash
openclaw nodes canvas present --node <id>
openclaw nodes canvas navigate --node <id> --url "/"
openclaw nodes canvas eval --node <id> --js "document.title"
openclaw nodes canvas snapshot --node <id>
```

For navigation, `canvas.navigate` accepts **local canvas paths**, `http(s)` URLs, and `file://` URLs. If you pass `"/"`, the Canvas shows the local scaffold or `index.html`.

## A2UI in Canvas (v0.8)

A2UI is hosted by the Gateway canvas host and rendered inside the Canvas panel. When the Gateway advertises a Canvas host, the macOS app auto-navigates to the A2UI host page on first open. The default A2UI host URL is:

```
http://<gateway-host>:18789/__openclaw__/a2ui/
```

Canvas currently accepts **A2UI v0.8** server→client messages: `beginRendering`, `surfaceUpdate`, `dataModelUpdate`, and `deleteSurface`. The newer `createSurface` (v0.9) message is **not supported**. The source provides a JSONL push example that defines a `surfaceUpdate` (a `Column` with `title` and `content` `Text` components) followed by `beginRendering`, pushed with the `a2ui push --jsonl` command:

```bash
cat > /tmp/a2ui-v0.8.jsonl <<'EOFA2'
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":{"explicitList":["title","content"]}}}},{"id":"title","component":{"Text":{"text":{"literalString":"Canvas (A2UI v0.8)"},"usageHint":"h1"}}},{"id":"content","component":{"Text":{"text":{"literalString":"If you can read this, A2UI push works."},"usageHint":"body"}}}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
EOFA2

openclaw nodes canvas a2ui push --jsonl /tmp/a2ui-v0.8.jsonl --node <id>
```

A quick smoke variant pushes inline text instead of a JSONL file: `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

## Triggering Agent Runs from Canvas — Deep Links

Canvas can trigger new agent runs via deep links of the form `openclaw://agent?...`. From inside the Canvas web content, JavaScript navigates to the deep link to launch a run, e.g.:

```js
window.location.href = "openclaw://agent?message=Review%20this%20design";
```

The app prompts for confirmation unless a valid key is provided.

## Security Notes

The Canvas scheme enforces three security properties per the source. First, the Canvas scheme **blocks directory traversal** — files must live under the session root. Second, local Canvas content uses a custom scheme (`openclaw-canvas://`), so **no loopback server is required** to serve it. Third, external `http(s)` URLs are allowed **only when explicitly navigated** (not loaded implicitly), constraining what the panel can reach without an intentional `canvas.navigate`.

**Source**: OpenClaw documentation — `platforms/mac/canvas` (mirror `inbox/openclaw_docs/platforms/mac/canvas.md`)
**Last Updated**: 2026-06-22
**Status**: Active
