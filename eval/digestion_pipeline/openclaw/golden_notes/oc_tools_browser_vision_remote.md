---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - browser
keywords:
  - openclaw browser screenshot vision
  - text-only model image understanding
  - local vs remote browser control
  - node browser proxy
  - remote cdp browserless browserbase notte
  - direct websocket cdp
  - multi-browser profiles
  - browser selection auto-detect
topics:
  - OpenClaw
  - Browser Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/browser
access_control_group: ["general"]
---

# OpenClaw — Browser Vision and Remote Control

## Overview

This note is the procedure for OpenClaw's browser **vision** and **remote-control** surfaces: enabling screenshot description for text-only main models, choosing which Chromium-based browser launches, the local-vs-remote control model, the zero-config Node browser proxy, attaching to hosted remote-CDP providers (Browserless including same-host Docker, Browserbase, and Notte), the three accepted CDP URL shapes, multi-browser named profiles, and the local browser auto-detect order. It mirrors the `tools/browser` source page sections Screenshot vision, Use Brave or another Chromium-based browser, Local vs remote control, Node browser proxy, Browserless, Direct WebSocket CDP providers, Profiles (multi-browser), and Browser selection. Overview, plugin control, agent guidance, and core configuration live in the sibling [oc_tools_browser_overview](oc_tools_browser_overview.md); security/isolation and the loopback control API live in [oc_tools_browser_security_isolation](oc_tools_browser_security_isolation.md) and [oc_tools_browser_control](oc_tools_browser_control.md).

## Screenshot vision (text-only model support)

When the main model is text-only (no vision/multimodal support), browser screenshots return image blocks the model cannot read. Browser screenshots reuse the existing image-understanding configuration, so an image model configured for media understanding can describe screenshots as text without any browser-specific model settings. Configure fallback candidates under `tools.media.image.models` (first success wins); shared media models also work when tagged for image support, and existing image-model defaults are honored.

```json5
{
  tools: {
    media: {
      image: {
        models: [
          { provider: "bytedance", model: "doubao-seed-2.0-pro" },
          // Add fallback candidates; first success wins
          { provider: "openai", model: "gpt-4o" },
        ],
      },
      // Shared media models also work when tagged for image support.
      // models: [{ provider: "openai", model: "gpt-4o", capabilities: ["image"] }],
    },
  },
  agents: {
    defaults: {
      // Existing image-model defaults are also honored.
      // imageModel: { primary: "openai/gpt-4o" },
    },
  },
}
```

The flow is: (1) the agent calls `browser screenshot` and the image is captured to disk as usual; (2) the browser tool asks the existing image-understanding runtime whether it can describe the screenshot using configured media image models, shared media models, image-model defaults, or an auth-backed image provider; (3) the vision model returns a text description, which is wrapped with `wrapExternalContent` (prompt injection guard) and returned to the agent as a text block instead of an image block; (4) if image understanding is unavailable, skipped, or fails, the browser falls back to returning the original image block. Use the existing `tools.media.image` / `tools.media.models` fields for model fallbacks, timeouts, byte limits, profiles, and provider request settings. If the active main model already supports vision and no explicit image-understanding model is configured, OpenClaw keeps the normal image result so the main model can read the screenshot directly.

## Use Brave or another Chromium-based browser

If your **system default** browser is Chromium-based (Chrome/Brave/Edge/etc), OpenClaw uses it automatically. Set `browser.executablePath` to override auto-detection. Top-level and per-profile `executablePath` values accept `~` for your OS home directory. Set it via the CLI or in config:

```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set browser.profiles.work.executablePath "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

The per-platform config `executablePath` is `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser` on macOS, `C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe` on Windows, and `/usr/bin/brave-browser` on Linux. Per-profile `executablePath` only affects local managed profiles that OpenClaw launches: `existing-session` profiles attach to an already-running browser instead, and remote CDP profiles use the browser behind `cdpUrl`.

## Local vs remote control

OpenClaw distinguishes three control modes plus a node-host variant:

- **Local control (default):** the Gateway starts the loopback control service and can launch a local browser.
- **Remote control (node host):** run a node host on the machine that has the browser; the Gateway proxies browser actions to it.
- **Remote CDP:** set `browser.profiles.<name>.cdpUrl` (or `browser.cdpUrl`) to attach to a remote Chromium-based browser. In this case, OpenClaw will not launch a local browser.
- For externally managed CDP services on loopback (for example Browserless in Docker published to `127.0.0.1`), also set `attachOnly: true`. Loopback CDP without `attachOnly` is treated as a local OpenClaw-managed browser profile.

`headless` only affects local managed profiles that OpenClaw launches; it does not restart or change existing-session or remote CDP browsers. `executablePath` follows the same local-managed-profile rule — changing it on a running local managed profile marks that profile for restart/reconcile so the next launch uses the new binary. Stopping behavior also differs by profile mode: for local managed profiles, `openclaw browser stop` stops the browser process that OpenClaw launched; for attach-only and remote CDP profiles, `openclaw browser stop` closes the active control session and releases Playwright/CDP emulation overrides (viewport, color scheme, locale, timezone, offline mode, and similar state), even though no browser process was launched by OpenClaw.

Remote CDP URLs can include auth: query tokens (e.g., `https://provider.example?token=<token>`) or HTTP Basic auth (e.g., `https://user:pass@provider.example`). OpenClaw preserves the auth when calling `/json/*` endpoints and when connecting to the CDP WebSocket. Prefer environment variables or secrets managers for tokens instead of committing them to config files.

## Node browser proxy (zero-config default)

If you run a **node host** on the machine that has your browser, OpenClaw can auto-route browser tool calls to that node without any extra browser config. This is the default path for remote gateways. The node host exposes its local browser control server via a **proxy command**, and profiles come from the node's own `browser.profiles` config (same as local). `nodeHost.browserProxy.allowProfiles` is optional: leave it empty for the legacy/default behavior, where all configured profiles remain reachable through the proxy, including profile create/delete routes. If you set `nodeHost.browserProxy.allowProfiles`, OpenClaw treats it as a least-privilege boundary — only allowlisted profiles can be targeted, and persistent profile create/delete routes are blocked on the proxy surface. To disable it, set `nodeHost.browserProxy.enabled=false` on the node, or `gateway.nodes.browser.mode="off"` on the gateway.

## Browserless (hosted remote CDP)

[Browserless](https://browserless.io) is a hosted Chromium service that exposes CDP connection URLs over HTTPS and WebSocket. OpenClaw can use either form, but for a remote browser profile the simplest option is the direct WebSocket URL from Browserless' connection docs. Replace `<BROWSERLESS_API_KEY>` with your real Browserless token and choose the region endpoint that matches your account. If Browserless gives you an HTTPS base URL, you can either convert it to `wss://` for a direct CDP connection or keep the HTTPS URL and let OpenClaw discover `/json/version`.

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "wss://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

### Browserless Docker on the same host

When Browserless is self-hosted in Docker and OpenClaw runs on the host, treat Browserless as an externally managed CDP service: set `cdpUrl: "ws://127.0.0.1:3000"` plus `attachOnly: true` on the `browserless` profile. The address in `browser.profiles.browserless.cdpUrl` must be reachable from the OpenClaw process. Browserless must also advertise a matching reachable endpoint — set Browserless `EXTERNAL` to that same public-to-OpenClaw WebSocket base, such as `ws://127.0.0.1:3000`, `ws://browserless:3000`, or a stable private Docker network address. If `/json/version` returns `webSocketDebuggerUrl` pointing at an address OpenClaw cannot reach, CDP HTTP can look healthy while the WebSocket attach still fails. Do not leave `attachOnly` unset for a loopback Browserless profile: without `attachOnly`, OpenClaw treats the loopback port as a local managed browser profile and may report that the port is in use but not owned by OpenClaw.

## Direct WebSocket CDP providers

Some hosted browser services expose a **direct WebSocket** endpoint rather than the standard HTTP-based CDP discovery (`/json/version`). OpenClaw accepts three CDP URL shapes and picks the right connection strategy automatically:

- **HTTP(S) discovery** — `http://host[:port]` or `https://host[:port]`. OpenClaw calls `/json/version` to discover the WebSocket debugger URL, then connects. No WebSocket fallback.
- **Direct WebSocket endpoints** — `ws://host[:port]/devtools/<kind>/<id>` or `wss://...` with a `/devtools/browser|page|worker|shared_worker|service_worker/<id>` path. OpenClaw connects directly via a WebSocket handshake and skips `/json/version` entirely.
- **Bare WebSocket roots** — `ws://host[:port]` or `wss://host[:port]` with no `/devtools/...` path (e.g. Browserless, Browserbase). OpenClaw tries HTTP `/json/version` discovery first (normalising the scheme to `http`/`https`); if discovery returns a `webSocketDebuggerUrl` it is used, otherwise OpenClaw falls back to a direct WebSocket handshake at the bare root. If the advertised WebSocket endpoint rejects the CDP handshake but the configured bare root accepts it, OpenClaw falls back to that root as well. This lets a bare `ws://` pointed at a local Chrome still connect (Chrome only accepts WebSocket upgrades on the specific per-target path from `/json/version`), while hosted providers can still use their root WebSocket endpoint when their discovery endpoint advertises a short-lived URL that is not suitable for Playwright CDP.

`openclaw browser doctor` uses the same discovery-first, WebSocket-fallback logic as runtime attach, so a bare-root URL that connects successfully is not reported as unreachable by diagnostics.

### Browserbase and Notte

[Browserbase](https://www.browserbase.com) is a cloud platform for running headless browsers with built-in CAPTCHA solving, stealth mode, and residential proxies. Configure a profile with `cdpUrl: "wss://connect.browserbase.com?apiKey=<BROWSERBASE_API_KEY>"`; copy your **API Key** from the Overview dashboard, replace `<BROWSERBASE_API_KEY>`, and note that Browserbase auto-creates a browser session on WebSocket connect (no manual session creation step). The free tier allows one concurrent session and one browser hour per month.

[Notte](https://www.notte.cc) is a cloud platform for running headless browsers with built-in stealth, residential proxies, and a CDP-native WebSocket gateway. Configure `cdpUrl: "wss://us-prod.notte.cc/sessions/connect?token=<NOTTE_API_KEY>"` (with `remoteCdpTimeoutMs: 3000` / `remoteCdpHandshakeTimeoutMs: 5000` as in the Browserbase example); copy your **API Key** from the console settings page and replace `<NOTTE_API_KEY>`. Notte also auto-creates a session on WebSocket connect, and the session is destroyed when the WebSocket disconnects. The free tier allows five concurrent sessions and 100 lifetime browser hours.

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserbase",
    remoteCdpTimeoutMs: 3000,
    remoteCdpHandshakeTimeoutMs: 5000,
    profiles: {
      browserbase: {
        cdpUrl: "wss://connect.browserbase.com?apiKey=<BROWSERBASE_API_KEY>",
        color: "#F97316",
      },
    },
  },
}
```

## Profiles (multi-browser)

OpenClaw supports multiple named profiles (routing configs). Profiles can be **openclaw-managed** (a dedicated Chromium-based browser instance with its own user data directory + CDP port), **remote** (an explicit CDP URL — a Chromium-based browser running elsewhere), or **existing session** (your existing Chrome profile via Chrome DevTools MCP auto-connect). Defaults and behavior:

- The `openclaw` profile is auto-created if missing.
- The `user` profile is built-in for Chrome MCP existing-session attach.
- Existing-session profiles are opt-in beyond `user`; create them with `--driver existing-session`.
- Local CDP ports allocate from **18800-18899** by default.
- Deleting a profile moves its local data directory to Trash.

All control endpoints accept `?profile=<name>`; the CLI uses `--browser-profile`.

## Browser selection

When launching locally, OpenClaw picks the first available: (1) Chrome, (2) Brave, (3) Edge, (4) Chromium, (5) Chrome Canary. You can override with `browser.executablePath`. Per platform, it checks: macOS — `/Applications` and `~/Applications`; Linux — common Chrome/Brave/Edge/Chromium locations under `/usr/bin`, `/snap/bin`, `/opt/google`, `/opt/brave.com`, `/usr/lib/chromium`, and `/usr/lib/chromium-browser`, plus Playwright-managed Chromium under `PLAYWRIGHT_BROWSERS_PATH` or `~/.cache/ms-playwright`; Windows — common install locations.

**Source**: OpenClaw documentation — `tools/browser` (mirror `inbox/openclaw_docs/tools/browser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
