---
tags:
  - resource
  - documentation
  - hermes_agent
  - browser_automation
  - tools
keywords:
  - browser automation setup
  - browser provider configuration
  - Camofox local mode
  - browser connect CDP
  - hybrid cloud local routing
  - agent-browser install
topics:
  - Hermes Agent
  - Browser Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
access_control_group: ["general"]
---

# Hermes Browser Automation — Setup

## Overview

This is the per-backend **setup procedure** for the Hermes Agent browser-automation toolset — how to configure each of the supported browser providers, as distinct from what the backends and tool surface ARE (see [hermes_browser_automation_backends](hermes_browser_automation_backends.md)). The toolset can run against several mutually selectable backends: managed cloud browsers (Browserbase, Browser Use, Firecrawl), a self-hosted anti-detection local browser (Camofox), a local Chromium-family browser attached via the Chrome DevTools Protocol (`/browser connect`), and a pure-local mode driven by the `agent-browser` CLI. Setup is mostly a matter of writing the right `.env` keys and `~/.hermes/config.yaml` `browser:` block, then making sure the `browser` toolset is enabled. Nous Portal subscribers can skip per-provider API keys entirely and use browser automation through the Tool Gateway. This note walks each provider's configuration plus the worked end-to-end examples; the `config.yaml` web/browser block reference itself is owned by [hermes_messaging_media_settings](hermes_messaging_media_settings.md).

## Nous Subscribers — Tool Gateway (no API keys)

If you have a paid [Nous Portal](https://portal.nousresearch.com) subscription, you can use browser automation through the **Tool Gateway** without any separate API keys. New installs can run `hermes setup --portal` to log in and turn on every gateway tool at once; existing installs can pick
**Nous Subscription** as the browser provider via `hermes model` or `hermes tools`.

## Cloud Modes — Browserbase / Browser Use / Firecrawl

Each cloud provider is selected by setting credentials in `~/.hermes/.env`:

```bash
# Add to ~/.hermes/.env
BROWSERBASE_API_KEY=***
BROWSERBASE_PROJECT_ID=your-project-id-here
# Browser Use:
BROWSER_USE_API_KEY=***
# Firecrawl:
FIRECRAWL_API_KEY=fc-***
```

If both Browserbase and Browser Use credentials are set, **Browserbase takes priority**. Firecrawl is selected with the wizard (`hermes setup tools → Browser Automation → Firecrawl`) and accepts optional overrides: `FIRECRAWL_API_URL` (default `https://api.firecrawl.dev`, point at a self-hosted instance such as `http://localhost:3002`) and `FIRECRAWL_BROWSER_TTL` (session TTL in seconds, default `300`). Credentials are obtained from the providers' own portals (browserbase.com, browser-use.com, firecrawl.dev).

## Hybrid Routing — Cloud for Public URLs, Local for LAN

When a cloud provider is configured, Hermes auto-spawns a **local Chromium sidecar** for URLs that resolve to a private/loopback/LAN address (`localhost`, `127.0.0.1`, `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`, `*.local`, `*.lan`, `*.internal`, IPv6 loopback `::1`, link-local `169.254.x.x`). Public URLs continue to use the cloud provider in the same conversation — so the agent can screenshot a dashboard at `http://localhost:3000` and scrape `https://github.com` without switching providers; the cloud provider never sees the private URL. The feature is **on by default**. To disable it (all URLs go to the configured cloud provider), set `browser.auto_local_for_private_urls: false` under the `browser:` block in `~/.hermes/config.yaml` (alongside `browser.cloud_provider`). With auto-routing disabled, private URLs are rejected with `"Blocked: URL targets a private or internal address"` unless `browser.allow_private_urls: true` is also set (which lets the cloud provider attempt them — usually fails since cloud browsers can't reach your LAN). The sidecar uses the same `agent-browser` CLI as pure local mode, so it must be installed (`hermes setup tools → Browser Automation` auto-installs it). Post-navigation redirects from a public URL onto a private address are still blocked.

## Camofox Local Mode

[Camofox](https://github.com/jo-inc/camofox-browser) is a self-hosted Node.js server wrapping Camoufox (a Firefox fork with C++ fingerprint spoofing) for local anti-detection browsing with no cloud dependency. Clone and start it with Docker:

```bash
git clone https://github.com/jo-inc/camofox-browser
cd camofox-browser
make up                 # start default container (auto-detects arch)
make down               # stop and remove
make reset              # force a clean rebuild
make build              # build image without starting (for custom docker run)
```

For custom runtime settings (larger Node heap, VNC live view, persistent profile), build the image then run it yourself, publishing the control port `9377` and optional VNC ports (`6080` noVNC, `5901` native client), and mounting `~/.camofox-docker` for persistence. Then point Hermes at it by adding `CAMOFOX_URL=http://localhost:9377` to `~/.hermes/.env`. When `CAMOFOX_URL` is set, **all browser tools automatically route through Camofox** instead of Browserbase or agent-browser. Can also be configured via `hermes tools → Browser Automation → Camofox`.

**Docker loopback rewriting.** If Camofox runs in Docker and must open web apps served from the host, enable
`browser.camofox.rewrite_loopback_urls: true` (with `loopback_host_alias: host.docker.internal`, the default). This rewrites only page-navigation URLs with loopback hosts (`localhost`, `127.0.0.1`, `::1`) — it does not change `CAMOFOX_URL`. Leave it disabled for non-Docker installs.

**Persistent sessions.** By default each Camofox session gets a random identity (cookies/logins don't
survive). Set `browser.camofox.managed_persistence: true` (note the **nested path** — a top-level `managed_persistence` is silently ignored) and fully restart Hermes. Hermes then sends a deterministic profile-scoped `userId` so the server can reuse the same Firefox profile, and skips server-side context destruction on cleanup. Hermes derives the stable `userId` from `~/.hermes/browser_auth/camofox/`; the actual profile data lives on the Camofox server, keyed by that `userId`. Hermes only sends a stable `userId` — the server must implement userId-based profile persistence for this to work.

**Externally managed sessions.** When another app drives the visible Camofox browser, three knobs let Hermes
operate inside that identity (env vars take precedence over `config.yaml`):

| Setting | Env var | Effect |
|---------|---------|--------|
| `browser.camofox.user_id` | `CAMOFOX_USER_ID` | `userId` Hermes uses; setting it opts into "externally managed" mode |
| `browser.camofox.session_key` | `CAMOFOX_SESSION_KEY` | `sessionKey`/`listItemId` for matching a tab during adoption (defaults per-task) |
| `browser.camofox.adopt_existing_tab` | `CAMOFOX_ADOPT_EXISTING_TAB` | when true, `GET /tabs?userId=<user_id>` reuses an existing tab before creating one |

With `user_id` set, Hermes skips destructive cleanup and never calls `DELETE /sessions/<user_id>` (which would wipe the external app's session). With `adopt_existing_tab: true`, on the first browser tool call Hermes issues `GET /tabs?userId=<user_id>` (5s timeout), adopts the most recent tab matching `session_key` (else any recent tab), and falls back to creating a new tab if none exist. Adoption fires only until `tab_id` is populated. When Camofox runs headed, it exposes a VNC port in its health check; Hermes auto-discovers it and includes the VNC URL in navigation responses for live viewing.

## Local Chromium-family via CDP (`/browser connect`)

You can attach the browser tools to your own running Chrome, Brave, Chromium, or Edge instance via the Chrome DevTools Protocol ([term_cdp](../../term_dictionary/term_cdp.md)) — useful for watching the agent live, using your own cookies/sessions, or avoiding cloud costs. `/browser connect` is an **interactive-CLI slash command** — it is NOT dispatched by the gateway, so it must be run from the terminal (`hermes` / `hermes chat`), not inside a WebUI/Telegram/Discord chat.

```
/browser connect                 # Auto-launch/connect to a local Chromium-family browser at http://127.0.0.1:9222
/browser connect ws://host:port  # Connect to a specific CDP endpoint
/browser status                  # Check current connection
/browser disconnect              # Detach and return to cloud/local mode
```

If no browser is running with remote debugging, Hermes auto-launches a supported Chromium-family browser with `--remote-debugging-port=9222` (detection covers Brave, Chrome, Chromium, Edge, including Linux paths like `/opt/brave-bin/brave` and `/snap/bin/brave`). To start one manually with CDP enabled, use a **dedicated `--user-data-dir`** so the debug port actually opens even if the browser is already running:

```bash
# Linux — Brave (Chrome/Edge analogous; on macOS use the .app binary path)
brave-browser \
  --remote-debugging-port=9222 \
  --user-data-dir=$HOME/.hermes/chrome-debug \
  --no-first-run \
  --no-default-browser-check &
```

Without `--user-data-dir`, launching while a regular instance runs typically opens a new window on the existing process (which was not started with `--remote-debugging-port`), so port 9222 never opens; a dedicated dir forces a fresh process where the debug port listens. When connected via CDP, all browser tools operate on your live browser instead of a cloud session.

## WSL2 + Windows Chrome — Prefer MCP

If Hermes runs inside WSL2 but the Chrome window runs on the Windows host, `/browser connect` is often not the best path: it expects Hermes itself to reach a usable CDP endpoint, and modern Chrome live-debugging sessions often expose a host-local endpoint not directly reachable from WSL the way a classic `9222` port is. The cleanest integration is to let a Windows-side browser MCP server attach to Chrome and let Hermes talk to that MCP server. For that setup, prefer `chrome-devtools-mcp` through Hermes MCP support ([hermes_mcp](hermes_mcp_concept_config.md), §WSL2 bridge).

## Local Browser Mode, Env Vars, and Install

If you set **no** cloud credentials and don't use `/browser connect`, Hermes still uses the browser tools through a local Chromium install driven by `agent-browser`. Optional environment variables tune the local and Browserbase behavior: `BROWSERBASE_PROXIES` (default `true`), `BROWSERBASE_ADVANCED_STEALTH` (default `false`, Scale Plan), `BROWSERBASE_KEEP_ALIVE` (default `true`, paid plan), `BROWSERBASE_SESSION_TIMEOUT` (max 21600s), `BROWSER_INACTIVITY_TIMEOUT` (default 120s before auto-cleanup), and `AGENT_BROWSER_ARGS` (extra Chromium launch flags; Hermes auto-injects `--no-sandbox,--disable-dev-shm-usage` under root / AppArmor-restricted namespaces, so most users don't set this — setting it disables the auto-injection). Install the CLI and enable the toolset:

```bash
npm install -g agent-browser     # or: npm install (locally in the repo)
hermes config set toolsets '["hermes-cli", "browser"]'
```

The `browser` toolset must appear in your config's `toolsets` list (or be enabled via the command above) for any browser tool to be available.

## Practical Examples

```
User: Sign up for an account on example.com with my email john@example.com

Agent workflow:
1. browser_navigate("https://example.com/signup")
2. browser_snapshot()  → sees form fields with refs
3. browser_type(ref="@e3", text="john@example.com")
4. browser_type(ref="@e5", text="SecurePass123")
5. browser_click(ref="@e8")  → clicks "Create Account"
6. browser_snapshot()  → confirms success
```

For dynamic content, the pattern is `browser_navigate` → `browser_snapshot(full=true)` to read the rendered list (e.g. GitHub trending repos) → return formatted results.

**Source**: `inbox/hermes_agent_docs/user-guide/features/browser.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
**Last Updated**: 2026-06-19
**Status**: Active
