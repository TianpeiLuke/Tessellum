---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - control_ui
keywords:
  - openclaw control ui chat
  - chat.send chat.history chat.inject
  - chat.message.get display normalization
  - browser realtime talk webrtc relay
  - talk.client.create talk.session.create
  - stop abort steer chat.abort
  - hosted embeds embedSandbox
  - pwa install web push vapid
  - mcp operator page
  - chat message width
topics:
  - OpenClaw
  - Control UI Chat and Talk
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/web/control-ui
access_control_group: ["general"]
---

# OpenClaw — Control UI Chat and Talk Contract

## Overview

This note models the **chat and Talk behavioral contract** of the OpenClaw Control UI — the browser SPA's interaction model over the Gateway WebSocket — mirroring the chat/Talk sections of the `web/control-ui` source page. It covers the non-blocking `chat.send` ack model, `chat.history` size-bounding + display normalization + on-demand `chat.message.get`, `chat.inject`, idempotency-keyed coalescing, browser realtime **Talk** (WebRTC vs Google Live constrained token vs Gateway relay), stop/abort/steer and abort-partial retention, the MCP operator page, the Activity tab, hosted `[embed]` sandbox modes, chat message width, and PWA install + Web Push (VAPID). The Control UI's auth/security model, CSP, and route auth live in the sibling auth/security note; what-it-is/build/dev live in the overview note.

## Chat behavior: send and history semantics

`chat.send` is **non-blocking**: it acks immediately with `{ runId, status: "started" }` and the response streams via `chat` events (trusted Control UI clients may also receive optional ACK timing metadata for local diagnostics). Re-sending with the same `idempotencyKey` returns `{ status: "in_flight" }` while running, and `{ status: "ok" }` after completion. Chat uploads accept images plus non-video files: images keep the native image path; other files are stored as managed media and shown in history as attachment links. Assistant/generated images are persisted as managed media references and served back through authenticated Gateway media URLs, so reloads do not depend on raw base64 image payloads in the chat history response.

`chat.history` responses are **size-bounded** for UI safety: chat history refreshes request a bounded recent window with per-message text caps so large sessions do not force the browser to render a full transcript payload before the chat becomes usable. When transcript entries are too large, the Gateway may truncate long text fields, omit heavy metadata blocks, and replace oversized messages with a placeholder (`[chat.history omitted: message too large]`). When a visible assistant message was truncated in `chat.history`, the side reader can fetch the full display-normalized transcript entry on demand through `chat.message.get` by `sessionKey`, active `agentId` when needed, and transcript `messageId`. If the Gateway still cannot return more, the reader shows an explicit unavailable state instead of silently repeating the truncated preview.

When rendering `chat.history`, the Control UI **display-normalizes** visible assistant text — it strips display-only inline directive tags (for example `[[reply_to_*]]` and `[[audio_as_voice]]`), plain-text tool-call XML payloads (including `<tool_call>...</tool_call>`, `<function_call>...</function_call>`, `<tool_calls>...</tool_calls>`, `<function_calls>...</function_calls>`, and truncated tool-call blocks), and leaked ASCII/full-width model control tokens, and omits assistant entries whose whole visible text is only the exact silent token `NO_REPLY` / `no_reply` or the heartbeat acknowledgement token `HEARTBEAT_OK`. Live `chat` events are delivery state, while `chat.history` is rebuilt from the durable session transcript; after tool-final events the Control UI reloads history and merges only a small optimistic tail (the transcript boundary is documented in WebChat). During an active send and the final history refresh, the chat view keeps local optimistic user/assistant messages visible if `chat.history` briefly returns an older snapshot; the canonical transcript replaces those local messages once the Gateway history catches up. `chat.inject` appends an assistant note to the session transcript and broadcasts a `chat` event for UI-only updates (no agent run, no channel delivery).

The chat header shows the agent filter before the session picker, scoped by the selected agent — switching agents shows only that agent's sessions and falls back to its main session when it has no saved dashboard sessions yet. The header model and thinking pickers patch the active session immediately through `sessions.patch`; they are **persistent session overrides**, not one-turn-only send options. If you send while a model-picker change for the same session is still saving, the composer waits for that session patch before calling `chat.send` so the send uses the selected model. The model picker requests the Gateway's configured model view: if `agents.defaults.models` is present, that allowlist drives the picker (including `provider/*` entries that keep provider-scoped catalogs dynamic); otherwise it shows explicit `models.providers.*.models` entries plus providers with usable auth, while the full catalog stays available through the debug `models.list` RPC with `view: "all"`. Typing `/new` creates/switches to a fresh dashboard session as New Chat, except when `session.dmScope: "main"` is configured and the current parent is the agent's main session (then it resets the main session in place); `/reset` keeps the Gateway's explicit in-place reset for the current session. When fresh Gateway session usage reports include current context tokens, the composer shows a compact context-usage indicator that switches to warning styling at high context pressure and, at recommended compaction levels, shows a compact button that runs the normal session compaction path (stale token snapshots are hidden until usage is fresh again).

## Browser realtime Talk

The Control UI can chat with the model via Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`), stream tool calls + live tool output cards in Chat (agent events), and **Talk** through browser realtime sessions. Talk mode uses a registered realtime voice provider with three distinct transports: **OpenAI uses direct WebRTC**, **Google Live uses a constrained one-use browser token over WebSocket**, and **backend-only realtime voice plugins use the Gateway relay transport**. Client-owned provider sessions start with `talk.client.create`; Gateway relay sessions start with `talk.session.create`. The relay keeps provider credentials on the Gateway while the browser streams microphone PCM through `talk.session.appendAudio`, forwards `openclaw_agent_consult` provider tool calls through `talk.client.toolCall` for Gateway policy and the larger configured OpenClaw model, and routes active-run voice steering through `talk.client.steer` or `talk.session.steer`.

The browser **never receives a standard provider API key**: OpenAI receives an ephemeral Realtime client secret for WebRTC; Google Live receives a one-use constrained Live API auth token for a browser WebSocket session, with instructions and tool declarations locked into the token by the Gateway; backend-realtime-bridge providers run through the relay so credentials and vendor sockets stay server-side. The Realtime session prompt is assembled by the Gateway — `talk.client.create` does not accept caller-provided instruction overrides. Configure OpenAI with `talk.realtime.provider: "openai"` plus an `openai` API-key auth profile, `talk.realtime.providers.openai.apiKey`, or `OPENAI_API_KEY` (OpenAI OAuth profiles do not configure Realtime voice); configure Google with `talk.realtime.provider: "google"` plus `talk.realtime.providers.google.apiKey`.

In the Chat composer, the Talk control is the waves button next to the microphone dictation button, with a Talk options button that applies to the next session and can override provider, transport, model, voice, reasoning effort, VAD threshold, silence duration, and prefix padding (a blank option uses configured defaults or the provider default). Selecting Gateway relay forces the backend relay path; selecting WebRTC keeps the session client-owned and **fails instead of silently falling back to relay** if the provider cannot create a browser session. When Talk starts, the composer status row shows `Connecting Talk...`, then `Talk live` while audio is connected, or `Asking OpenClaw...` while a realtime tool call consults the configured larger model through `talk.client.toolCall`.

## Stop, abort, steer, and abort-partial retention

Stopping a run: click **Stop** (calls `chat.abort`); type `/stop` (or standalone abort phrases like `stop`, `stop action`, `stop run`, `stop openclaw`, `please stop`) to abort out-of-band. `chat.abort` supports `{ sessionKey }` (no `runId`) to abort all active runs for that session. While a run is active, normal follow-ups **queue**; click **Steer** on a queued message to inject it into the running turn. When a run is aborted, partial assistant text can still be shown in the UI: the Gateway persists buffered aborted partial text into transcript history with abort metadata, so transcript consumers can tell abort partials from normal completion output.

## MCP operator page

The dedicated MCP page is an **operator view** for OpenClaw-managed MCP servers under `mcp.servers`. It does **not** start MCP transports by itself; use it to inspect/edit saved config, then `openclaw mcp doctor --probe` for live server proof. The typical workflow: open **MCP** from the sidebar; check the summary cards for total, enabled, OAuth, and filtered server counts; review each server row for transport, enablement, auth, filters, timeouts, and command hints; toggle enablement when a server should stay configured but out of runtime discovery; edit the scoped `mcp` config section for server definitions, headers, TLS/mTLS paths, OAuth metadata, tool filters, and Codex projection metadata; use **Save** for a config write or **Save & Publish** to have the running Gateway apply it; and run `openclaw mcp status --verbose`, `openclaw mcp doctor --probe`, or `openclaw mcp reload` from a terminal for static diagnostics, live proof, or cached-runtime disposal. The page redacts credential-bearing URL-like values before rendering and quotes server names in command snippets so copied commands still work with spaces or shell metacharacters.

## Activity tab

The Activity tab is an **ephemeral browser-local observer** for live tool activity, derived from the same Gateway `session.tool` / tool event stream that powers Chat tool cards; it does not add another Gateway event family, endpoint, durable activity store, metrics feed, or external observer stream. Activity entries keep only sanitized summaries and redacted, truncated output previews: tool argument values are not stored (the UI shows arguments are hidden and records only the argument field count). The in-memory list follows the current browser tab, survives navigation within the Control UI, and resets on page reload, session switch, or **Clear**.

## Hosted embeds

Assistant messages can render hosted web content inline with the `[embed ...]` shortcode. The iframe sandbox policy is controlled by `gateway.controlUi.embedSandbox` with three modes: **strict** disables script execution inside hosted embeds; **scripts (default)** allows interactive embeds while keeping origin isolation (usually enough for self-contained browser games/widgets); **trusted** adds `allow-same-origin` on top of `allow-scripts` for same-site documents that intentionally need stronger privileges. Use `trusted` only when the embedded document genuinely needs same-origin behavior — for most agent-generated games and interactive canvases, `scripts` is the safer choice. Absolute external `http(s)` embed URLs stay blocked by default; to intentionally let `[embed url="https://..."]` load third-party pages, set `gateway.controlUi.allowExternalEmbedUrls: true`.

```json5
{
  gateway: {
    controlUi: {
      embedSandbox: "scripts",
    },
  },
}
```

## Chat message width

Grouped chat messages use a readable default max-width. Wide-monitor deployments can override it without patching bundled CSS by setting `gateway.controlUi.chatMessageMaxWidth`. The value is validated before it reaches the browser; supported values include plain lengths and percentages such as `960px` or `82%`, plus constrained `min(...)`, `max(...)`, `clamp(...)`, `calc(...)`, and `fit-content(...)` expressions.

```json5
{
  gateway: {
    controlUi: {
      chatMessageMaxWidth: "min(1280px, 82%)",
    },
  },
}
```

## PWA install and Web Push

The Control UI ships a `manifest.webmanifest` and a service worker, so modern browsers can install it as a standalone **PWA**. **Web Push** lets the Gateway wake the installed PWA with notifications even when the tab or browser window is not open. If the page shows **Protocol mismatch** right after an update, reopen the dashboard with `openclaw dashboard` and hard-refresh; if it still fails, clear site data for the dashboard origin or test in a private window, since an old service-worker cache can keep a pre-update bundle running against the newer Gateway. The PWA/push surfaces are: `ui/public/manifest.webmanifest` (PWA manifest — browsers offer "Install app" once reachable); `ui/public/sw.js` (service worker handling `push` events and notification clicks); `push/vapid-keys.json` under the OpenClaw state dir (auto-generated VAPID keypair signing Web Push payloads); and `push/web-push-subscriptions.json` (persisted browser subscription endpoints).

Override the VAPID keypair through env vars on the Gateway process when you want to pin keys (for multi-host deployments, secrets rotation, or tests): `OPENCLAW_VAPID_PUBLIC_KEY`, `OPENCLAW_VAPID_PRIVATE_KEY`, and `OPENCLAW_VAPID_SUBJECT` (defaults to `https://openclaw.ai`). The Control UI uses these **scope-gated Gateway methods** to register and test browser subscriptions: `push.web.vapidPublicKey` fetches the active VAPID public key; `push.web.subscribe` registers an `endpoint` plus `keys.p256dh`/`keys.auth`; `push.web.unsubscribe` removes a registered endpoint; `push.web.test` sends a test notification to the caller's subscription. Web Push is independent of the iOS APNS relay path and the existing `push.test` method, which target native mobile pairing.

**Source**: OpenClaw documentation — `web/control-ui` (mirror `inbox/openclaw_docs/web/control-ui.md`)
**Last Updated**: 2026-06-22
**Status**: Active
