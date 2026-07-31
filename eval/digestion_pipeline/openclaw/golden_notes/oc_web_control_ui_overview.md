---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - control_ui
keywords:
  - openclaw control ui
  - vite lit single-page app
  - gateway control ui basepath
  - control-ui-config.json runtime config
  - control ui appearance themes tweakcn
  - control ui language support locales
  - what the control ui can do capability map
  - pnpm ui:build ui:dev
  - blank control ui recovery panel
  - control ui dev server gatewayUrl
topics:
  - OpenClaw
  - Control UI
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/web/control-ui
access_control_group: ["general"]
---

# OpenClaw — The Control UI (Browser Front-End) Overview

## Overview

This note describes what the OpenClaw **Control UI** is: a small **Vite + Lit** single-page app (SPA) served by the Gateway that speaks directly to the Gateway WebSocket on the same port, giving an operator a browser front-end to chat, channels, sessions, dreams, cron, skills, nodes, exec approvals, config, MCP, and debug/logs/update. It mirrors the conceptual and build/dev/recovery sections of the `web/control-ui` source page — what the UI is and where it is served, how to open it locally, its runtime-config endpoint, localization, appearance/theme/text-size, the full capability map, how to build and run a dev server, and how to recover a blank page. The auth + device-pairing + security surface (handshake auth, pairing, Tailnet, insecure-HTTP, CSP, route auth) is documented in [oc_web_control_ui_auth_security](oc_web_control_ui_auth_security.md), and the chat/talk/MCP/embeds/PWA contract is documented in [oc_web_control_ui_chat_talk](oc_web_control_ui_chat_talk.md).

## What the Control UI Is and Where It Is Served

The Control UI is a small **Vite + Lit** single-page app served by the Gateway. By default it is served at `http://<host>:18789/`, and an optional path prefix can be set via `gateway.controlUi.basePath` (e.g. `/openclaw`). It speaks **directly to the Gateway WebSocket** on the same port — there is no separate API server. The dashboard (the same Control UI served at `/`) and the native WebChat app share this Gateway-WS-backed model; this note covers only the Control UI's identity, capabilities, and build/dev surface.

## Quick Open (Local)

If the Gateway is running on the same computer, open `http://127.0.0.1:18789/` (or `http://localhost:18789/`). If the page fails to load, start the Gateway first with `openclaw gateway`. Auth is supplied during the WebSocket handshake (via `connect.params.auth.token`, `connect.params.auth.password`, Tailscale Serve identity headers, or trusted-proxy identity headers) — the handshake-auth modes and device-pairing flow are documented in full in [oc_web_control_ui_auth_security](oc_web_control_ui_auth_security.md). The dashboard settings panel keeps a token for the current browser tab session and selected gateway URL; passwords are not persisted. Onboarding usually generates a gateway token for shared-secret auth on first connect, but password auth works too when `gateway.auth.mode` is `"password"`.

## Runtime Config Endpoint

The Control UI fetches its runtime settings from `/control-ui-config.json`, resolved relative to the Gateway's Control UI base path (for example `/__openclaw__/control-ui-config.json` when the UI is served under `/__openclaw__/`). That endpoint is gated by the same gateway auth as the rest of the HTTP surface: unauthenticated browsers cannot fetch it, and a successful fetch requires either an already valid gateway token/password, Tailscale Serve identity, or a trusted-proxy identity.

## Language Support

The Control UI can localize itself on first load based on your browser locale. To override it later, open **Overview -> Gateway Access -> Language**; the locale picker lives in the Gateway Access card, not under Appearance. Supported locales are `en`, `zh-CN`, `zh-TW`, `pt-BR`, `de`, `es`, `ja-JP`, `ko`, `fr`, `ar`, `it`, `tr`, `uk`, `id`, `pl`, `th`, `vi`, `nl`, `fa`. Non-English translations are lazy-loaded in the browser, the selected locale is saved in browser storage and reused on future visits, and missing translation keys fall back to English. Docs translations are generated for the same non-English locale set, but the docs site's built-in Mintlify language picker is limited to the locale codes Mintlify accepts — Thai (`th`) and Persian (`fa`) docs are still generated in the publish repo and may not appear in that picker until Mintlify supports those codes.

## Appearance Themes

The Appearance panel keeps the built-in **Claw**, **Knot**, and **Dash** themes, plus one browser-local tweakcn import slot. To import a theme, open the tweakcn editor, choose or create a theme, click **Share**, and paste the copied theme link into Appearance. The importer also accepts `https://tweakcn.com/r/themes/<id>` registry URLs, editor URLs like `https://tweakcn.com/editor/theme?theme=amethyst-haze`, relative `/themes/<id>` paths, raw theme IDs, and default theme names such as `amethyst-haze`. Appearance also includes a browser-local **Text size** setting: it is stored with the rest of Control UI preferences, applies to chat text, composer text, tool cards, and chat sidebars, and keeps text inputs at least 16px so mobile Safari does not auto-zoom on focus. Imported themes are stored only in the current browser profile — they are not written to gateway config and do not sync across devices; replacing the imported theme updates the one local slot, and clearing it switches the active theme back to Claw if the imported theme was selected.

## What It Can Do (Today) — Capability Map

The source page enumerates the Control UI's capabilities as accordion groups, each backed by named Gateway RPC methods. The Chat and Talk surface (chat via Gateway WS — `chat.history`, `chat.send`, `chat.abort`, `chat.inject` — plus browser realtime Talk, streamed tool cards, and the Activity tab) is summarized here but documented in full in [oc_web_control_ui_chat_talk](oc_web_control_ui_chat_talk.md). The remaining capability clusters are:

- **Channels, instances, sessions, dreams** — channel status, QR login, and per-channel config (`channels.status`, `web.login.*`, `config.patch`), keeping the previous snapshot visible while slow provider probes finish; instance presence list + refresh (`system-presence`); sessions list with per-session model/thinking/fast/verbose/trace/reasoning overrides (`sessions.list`, `sessions.patch`); and dreaming status, enable/disable toggle, and a Dream Diary reader (`doctor.memory.status`, `doctor.memory.dreamDiary`, `config.patch`).
- **Cron, skills, nodes, exec approvals** — cron jobs list/add/edit/run/enable/disable + run history (`cron.*`); skills status, enable/disable, install, API key updates (`skills.*`); nodes list + caps (`node.list`); and exec approvals editing gateway or node allowlists + ask policy for `exec host=gateway/node` (`exec.approvals.*`).
- **Config** — view/edit `~/.openclaw/openclaw.json` (`config.get`, `config.set`); a dedicated MCP settings page; apply + restart with validation (`config.apply`) and waking the last active session; writes carry a base-hash guard to prevent clobbering concurrent edits and preflight active SecretRef resolution (`config.set`/`config.apply`/`config.patch`); schema/form rendering (`config.schema` / `config.schema.lookup`); and a Raw JSON editor available only when the snapshot has a safe raw round-trip (otherwise Form mode is forced).
- **Debug, logs, update** — status/health/models snapshots + event log + manual RPC calls (`status`, `health`, `models.list`); an event log including Control UI refresh/RPC timings and browser responsiveness entries; a live tail of gateway file logs with filter/export (`logs.tail`); and an update path that runs a package/git update + restart (`update.run`) then polls `update.status` after reconnect.
- **Cron jobs panel notes** — for isolated jobs, delivery defaults to announce summary (switchable to none); channel/target fields appear when announce is selected; webhook mode uses `delivery.mode = "webhook"` with `delivery.to` set to a valid HTTP(S) webhook URL; advanced edit controls include delete-after-run, clear agent override, cron exact/stagger options, agent model/thinking overrides, and best-effort delivery toggles; setting `cron.webhookToken` sends a dedicated bearer token; and the deprecated fallback `openclaw doctor --fix` migrates stored legacy jobs with `notify: true` from `cron.webhook` to explicit per-job webhook or completion delivery.

## Building the UI

The Gateway serves static files from `dist/control-ui`. Build them with:

```bash
pnpm ui:build
```

To produce fixed asset URLs, set an optional absolute base path on the build:

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

For local development with a separate dev server, run `pnpm ui:dev`, then point the UI at your Gateway WS URL (e.g. `ws://127.0.0.1:18789`).

## Blank Control UI Page (Recovery)

If the browser loads a blank dashboard and DevTools shows no useful error, an extension or early content script may have prevented the JavaScript module app from evaluating. The static page includes a plain HTML recovery panel that appears when `<openclaw-app>` is not registered after startup. Use the panel's **Try again** action after changing the browser environment, or reload manually after disabling extensions that inject into all pages (especially extensions with `<all_urls>` content scripts), trying a private window / clean browser profile / another browser, and verifying the same dashboard URL after the browser change while keeping the Gateway running.

## Debugging / Testing: Dev Server + Remote Gateway

The Control UI is static files; the WebSocket target is configurable and can differ from the HTTP origin, which is handy when you want the Vite dev server locally but the Gateway runs elsewhere. Start the UI dev server with `pnpm ui:dev`, then open it with a `gatewayUrl` query param:

```text
http://localhost:5173/?gatewayUrl=ws%3A%2F%2F<gateway-host>%3A18789
```

Optional one-time auth passes the token via the URL fragment (`#token=...`), which is not sent to the server (avoiding request-log and Referer leakage):

```text
http://localhost:5173/?gatewayUrl=wss%3A%2F%2F<gateway-host>%3A18789#token=<gateway-token>
```

Key behaviors: `gatewayUrl` is stored in localStorage after load and removed from the URL, and must be URL-encoded when a full `ws://`/`wss://` endpoint is passed; legacy `?token=` query params are imported once for compatibility but stripped immediately after bootstrap; `password` is kept in memory only; when `gatewayUrl` is set the UI does not fall back to config or environment credentials (missing explicit credentials is an error); use `wss://` when the Gateway is behind TLS; and `gatewayUrl` is only accepted in a top-level window (not embedded) to prevent clickjacking. Public non-loopback deployments must set `gateway.controlUi.allowedOrigins` explicitly (full origins), while private same-origin LAN/Tailnet loads from loopback, RFC1918/link-local, `.local`, `.ts.net`, or Tailscale CGNAT hosts are accepted without enabling Host-header fallback; do not use `gateway.controlUi.allowedOrigins: ["*"]` except for tightly controlled local testing, and `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` is a dangerous security mode. Example origins config:

```json5
{
  gateway: {
    controlUi: {
      allowedOrigins: ["http://localhost:5173"],
    },
  },
}
```

**Source**: OpenClaw documentation — `web/control-ui` (mirror `inbox/openclaw_docs/web/control-ui.md`)
**Last Updated**: 2026-06-22
**Status**: Active
