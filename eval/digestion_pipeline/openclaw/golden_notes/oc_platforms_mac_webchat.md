---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - webchat
keywords:
  - openclaw mac webchat
  - embedded swiftui webchat view
  - gateway websocket chat methods
  - chat.history display-normalized transcript
  - local vs remote ssh tunnel mode
  - chat.send chat.abort chat.inject
  - main session switcher
  - webchatswiftui debug log
topics:
  - OpenClaw
  - macOS WebChat
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms/mac/webchat
access_control_group: ["general"]
---

# OpenClaw — macOS Embedded WebChat View

## Overview

This note describes the **macOS menu-bar app's embedded WebChat UI**: a native SwiftUI view that connects to the OpenClaw Gateway and defaults to the **main session** for the selected agent, with a session switcher for other sessions. It covers the two connection modes (local vs SSH-tunneled remote), the Gateway WebSocket data plane (the `chat.*` methods and `chat`/`agent`/`presence`/`tick`/`health` events), the display-normalized transcript returned by `chat.history`, session defaulting/switching plus the dedicated onboarding session, the remote-mode security surface, and the launch/debug entry points — mirroring the `platforms/mac/webchat` source page.

## What WebChat Is and Its Connection Modes

The macOS menu-bar app embeds the WebChat UI as a **native SwiftUI view** (not a full browser). It connects to the Gateway and defaults to the **main session** for the selected agent, exposing a session switcher to reach other sessions. The view supports two connection modes for how it reaches the Gateway:

- **Local mode** — connects directly to the local Gateway WebSocket.
- **Remote mode** — forwards the Gateway control port over SSH and uses that tunnel as the data plane.

## Launch and Debugging

WebChat can be opened manually or auto-opened for testing, and emits its own log subsystem/category:

- **Manual**: Lobster menu → "Open Chat".
- **Auto-open for testing**: launch the app binary with the `--webchat` flag.
- **Logs**: `./scripts/clawlog.sh` (subsystem `ai.openclaw`, category `WebChatSwiftUI`).

```bash
dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
```

## How It Is Wired

The WebChat view's **data plane is the Gateway WS**. It uses the WS methods `chat.history`, `chat.send`, `chat.abort`, and `chat.inject`, and consumes the events `chat`, `agent`, `presence`, `tick`, and `health`.

`chat.history` returns **display-normalized transcript rows** rather than raw transcript content. In the normalization: inline directive tags are stripped from visible text; plain-text tool-call XML payloads — including `<tool_call>...</tool_call>`, `<function_call>...</function_call>`, `<tool_calls>...</tool_calls>`, `<function_calls>...</function_calls>`, and truncated tool-call blocks — are stripped; leaked ASCII/full-width model control tokens are stripped; pure silent-token assistant rows such as the exact `NO_REPLY` / `no_reply` are omitted; and oversized rows can be replaced with placeholders.

For session selection, WebChat **defaults to the primary session** (`main`, or `global` when scope is global), and the UI can switch between sessions. **Onboarding uses a dedicated session** to keep first-run setup separate from regular conversation history.

## Security Surface

In remote mode the app forwards **only** the Gateway WebSocket control port over SSH — the SSH tunnel is the sole exposed data-plane path to the remote Gateway.

## Known Limitations

The UI is optimized for chat sessions and is **not a full browser sandbox**.

**Source**: OpenClaw documentation — `platforms/mac/webchat` (mirror `inbox/openclaw_docs/platforms/mac/webchat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
