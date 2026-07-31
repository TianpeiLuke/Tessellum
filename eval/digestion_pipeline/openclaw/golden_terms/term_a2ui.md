---
tags:
  - resource
  - terminology
  - a2ui
  - agent-to-ui
  - generative-ui
  - canvas
  - openclaw
keywords:
  - A2UI
  - Agent to UI
  - agent-rendered UI
  - generative UI
  - Canvas
  - openclaw-canvas
  - WKScriptMessageHandler
topics:
  - Agent interfaces
  - Generative UI
  - OpenClaw Canvas
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://a2ui.org/introduction/what-is-a2ui/
access_control_group: ["general"]
---

# A2UI - Agent-to-UI

## Definition

**A2UI (Agent-to-UI)** is an emerging protocol class for agent-driven user interfaces — the pattern in which an LLM-backed agent produces UI artifacts (a declarative component tree, a JSON spec, or rendered HTML/JS) that a host application displays as a live surface, while user interactions inside that surface are returned to the agent as structured action messages. A2UI sits next to other agent interaction protocols in the same emerging stack: [MCP](term_mcp.md) governs the agent-to-tool boundary, A2A governs the agent-to-agent boundary, and A2UI governs the agent-to-UI boundary. Google's public A2UI specification (launched December 2025) defines a *declarative* variant in which the agent emits a JSON component tree against a host-maintained component catalog so the client can render natively without executing arbitrary code; the broader pattern (as practiced by Anthropic Computer Use, OpenAI Canvas, Vercel AI SDK generative UI, and OpenClaw Canvas) includes both declarative and HTML/JS-emission flavors.

A2UI differs from a traditional chat UI in three ways: (1) the agent's *output* is a first-class UI artifact, not just text; (2) the host owns the rendering pipeline and the security boundary; (3) user actions in the rendered surface flow back as structured messages (typically carrying an idempotency key) rather than as new chat turns. The pattern preserves accessibility, styling, and security control on the host side while letting the agent compose interfaces that would be tedious to elicit through sequential chat questions (forms, calendars, multi-step pickers, dashboards).

## Context

A2UI is shorthand for a family of industry implementations, not a single product. Representative examples:

- **Google A2UI (open spec, December 2025)** — declarative protocol; agent emits JSON `createSurface` / `updateComponents` / `updateDataModel` messages; client renders from a pre-approved component catalog. Apache 2.0 licensed; transport-agnostic (works over A2A, AG-UI, SSE, WebSockets). The reference specification at [a2ui.org](https://a2ui.org/introduction/what-is-a2ui/).
- **Anthropic Computer Use** — agent observes screenshots and emits click/keystroke coordinates against an existing desktop UI; the host (a sandbox VM) executes the actions. A *pixel-level* A2UI variant rather than a declarative one.
- **OpenAI Canvas (ChatGPT)** — opens a side workspace beside the chat where ChatGPT writes/edits documents and code; the user edits in-place and ChatGPT sees those edits as the next turn.
- **Vercel AI SDK — generative UI** — the agent streams React components (or component descriptions) that the Next.js host renders inline in the chat.
- **OpenClaw Canvas (local-first)** — the macOS app hosts a floating `NSPanel` with a `WKWebView`. The agent writes HTML/JS/CSS into a per-session directory under `~/Library/Application Support/OpenClaw/canvas/<session>/`; a custom `openclaw-canvas://<session>/<path>` URL scheme serves the files; a `CanvasFileWatcher` (FSEvents + 0.25 s polling fallback) triggers reload on every agent write; in-canvas JS sends user actions back via `window.webkit.messageHandlers.openclawCanvasA2UIAction.postMessage({...})`. Each action carries an idempotency key (caller-provided trimmed `id` or a fresh UUID) used by the gateway to dedupe retries.

The OpenClaw implementation lives in `apps/macos/Sources/OpenClaw/CanvasA2UIActionMessageHandler.swift` (145 LOC) and `CanvasFileWatcher.swift` (102 LOC); these are surfaced via the [openclaw-canvas:// URL scheme](../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) and the [A2UI action bridge](../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) snippets in the vault.

## Key Characteristics

- **Agent-emitted UI artifact as primary output** — declarative JSON component tree (Google A2UI), raw HTML/JS files (OpenClaw Canvas), React component stream (Vercel AI SDK), or pixel-level screenshot-and-coordinate exchange (Anthropic Computer Use). The artifact, not text, is the interaction surface.
- **Host-owned rendering and security boundary** — the host application maintains the component catalog (declarative variants) or the file-serving scheme handler (file-emission variants), so an agent cannot execute arbitrary code on the user's machine even though it can ask for arbitrary UI. OpenClaw enforces this via a custom `openclaw-canvas://` scheme with session-root containment under symlink resolution.
- **Host-provided message bus from UI back to agent** — `WKScriptMessageHandler` (WebKit), `window.postMessage` (web), platform channels (Flutter), React Native bridge, or a typed action callback (declarative A2UI). The bus is registered under a stable name (`openclawCanvasA2UIAction` in OpenClaw) and scheme-gated to reject HTTP origins.
- **Idempotency-keyed action envelopes** — each `userAction` carries a caller-provided id or a generated UUID; the host computes the [idempotency key](term_idempotency_key.md) exactly once at the entry point so retries, double-clicks, and replays collapse server-side.
- **File-watcher or stream-driven reload** — for file-emission variants (OpenClaw), the host watches the per-session directory and reloads the panel on every agent write; a kernel-event watcher (FSEvents/inotify) is paired with a polling fallback so a dropped notification cannot leave the surface stale.
- **Sandboxed origin with custom URL scheme** — file-emission variants (OpenClaw) use a non-HTTP scheme so a typical browser cannot reach the surface; declarative variants (Google A2UI) avoid the iframe sandboxing problem entirely by never sending executable code in the first place.

## Related Terms


## Related Code Snippets

- **[OpenClaw macOS Canvas — File Watcher + A2UI Action Bridge](../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md)** (#700): the `CanvasA2UIActionMessageHandler` (`WKScriptMessageHandler` for `openclawCanvasA2UIAction`), `userAction` envelope unwrap, idempotency-key derivation, async `GatewayConnection.sendAgent` with JS status callback, and the file-watcher pair (FSEvents + polling fallback) that drive live reload.
- **[OpenClaw macOS Canvas — Panel Lifecycle + Custom URL Scheme](../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md)** (#699): the `CanvasManager` panel lifecycle, gateway-push observer with idempotent auto-navigate gate, and the `CanvasSchemeHandler` (custom `openclaw-canvas://` URL scheme with session-root containment under symlink resolution) — the rendering substrate the A2UI bridge sits on top of.

## References

- [A2UI — What is A2UI?](https://a2ui.org/introduction/what-is-a2ui/) — Google's public A2UI specification documentation; declarative component-tree protocol, host catalog model, transport options.
- [Introducing A2UI: An open project for agent-driven interfaces (Google Developers Blog)](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/) — launch announcement (December 2025); contrast with HTML/JavaScript-emission approaches; rationale for the declarative + catalog model.
- [google/a2ui (GitHub)](https://github.com/google/a2ui) — Apache 2.0 reference implementation and protocol artifacts.
- [Anthropic — Computer Use tool documentation](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) — pixel-level A2UI variant; Claude observes screenshots and emits action coordinates that the host executes.
- [Vercel AI SDK — Generative User Interfaces](https://sdk.vercel.ai/docs/ai-sdk-ui/generative-user-interfaces) — React component streaming variant; agent emits component descriptions that the Next.js host renders inline.
