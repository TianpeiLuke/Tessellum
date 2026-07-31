---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - browser
keywords:
  - openclaw managed browser
  - openclaw browser profile
  - agent browser automation
  - openclaw vs user profile
  - browser plugin enable
  - tools.alsoAllow browser
  - browser ssrfPolicy config
  - browser-automation skill
  - cdp loopback control service
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

# OpenClaw — Managed Browser: Overview, Quick Start, and Configuration

## Overview

This note is the operator/agent procedure for the **OpenClaw-managed browser**: a dedicated Chrome/Brave/Edge/Chromium profile the agent controls, isolated from your personal browser and managed through a small loopback-only control service inside the Gateway. It mirrors the front of the `tools/browser` source page — the beginner view, what you get, the quick-start CLI, plugin control + re-enable troubleshooting, agent tool-profile guidance, the `openclaw` vs `user` profile split, and the core `browser.*` configuration block (with its Ports/reachability, SSRF-policy, and Profile-behavior knobs). Screenshot-vision and remote/multi-browser control are split into [oc_tools_browser_vision_remote](oc_tools_browser_vision_remote.md); the security/isolation model into [oc_tools_browser_security_isolation](oc_tools_browser_security_isolation.md); the HTTP/CLI control reference into [oc_tools_browser_control](oc_tools_browser_control.md).

## What the managed browser is (beginner view)

OpenClaw can run a **dedicated Chrome/Brave/Edge/Chromium profile** that the agent controls; it is isolated from your personal browser and managed through a small local control service inside the Gateway (loopback only). The beginner mental model: think of it as a **separate, agent-only browser**; the `openclaw` profile does **not** touch your personal browser profile; the agent can **open tabs, read pages, click, and type** in a safe lane; and the built-in `user` profile attaches to your real signed-in Chrome session via Chrome MCP.

## What you get

- A separate browser profile named **openclaw** (orange accent by default).
- Deterministic tab control (list/open/focus/close).
- Agent actions (click/type/drag/select), snapshots, screenshots, PDFs.
- A bundled `browser-automation` skill that teaches agents the snapshot, stable-tab, stale-ref, and manual-blocker recovery loop when the browser plugin is enabled.
- Optional multi-profile support (`openclaw`, `work`, `remote`, ...).

This browser is **not** your daily driver. It is a safe, isolated surface for agent automation and verification.

## Quick start

Each command targets a named profile via `--browser-profile`. The standard probe-then-use sequence is:

```bash
openclaw browser --browser-profile openclaw doctor
openclaw browser --browser-profile openclaw doctor --deep
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

If you get "Browser disabled", enable it in config (see [Configuration](#configuration)) and restart the Gateway. If `openclaw browser` is missing entirely, or the agent says the browser tool is unavailable, jump to [Missing browser command or tool](#missing-browser-command-or-tool).

## Plugin control

The default `browser` tool is a bundled plugin. Disable it to replace it with another plugin that registers the same `browser` tool name:

```json5
{
  plugins: {
    entries: {
      browser: {
        enabled: false,
      },
    },
  },
}
```

Defaults need both `plugins.entries.browser.enabled` **and** `browser.enabled=true`. Disabling only the plugin removes the `openclaw browser` CLI, `browser.request` gateway method, agent tool, and control service as one unit; your `browser.*` config stays intact for a replacement. Browser config changes require a Gateway restart so the plugin can re-register its service.

## Missing browser command or tool

If `openclaw browser` is unknown after an upgrade, `browser.request` is missing, or the agent reports the browser tool as unavailable, the usual cause is a `plugins.allow` list that omits `browser` and no root `browser` config block exists. Add it:

```json5
{
  plugins: {
    allow: ["telegram", "browser"],
  },
}
```

An explicit root `browser` block — for example `browser.enabled=true` or `browser.profiles.<name>` — activates the bundled browser plugin even under a restrictive `plugins.allow`, matching channel config behavior. `plugins.entries.browser.enabled=true` and `tools.alsoAllow: ["browser"]` do not substitute for allowlist membership by themselves. Removing `plugins.allow` entirely also restores the default.

## Agent guidance

Tool-profile note: `tools.profile: "coding"` includes `web_search` and `web_fetch`, but it does **not** include the full `browser` tool. If the agent or a spawned sub-agent should use browser automation, add browser at the profile stage:

```json5
{
  tools: {
    profile: "coding",
    alsoAllow: ["browser"],
  },
}
```

For a single agent, use `agents.list[].tools.alsoAllow: ["browser"]`. `tools.subagents.tools.allow: ["browser"]` alone is not enough because sub-agent policy is applied after profile filtering.

The browser plugin ships two levels of agent guidance: the `browser` tool description carries the compact always-on contract (pick the right profile, keep refs on the same tab, use `tabId`/labels for tab targeting, and load the browser skill for multi-step work); and the bundled `browser-automation` skill carries the longer operating loop (check status/tabs first, label task tabs, snapshot before acting, resnapshot after UI changes, recover stale refs once, and report login/2FA/captcha or camera/microphone blockers as manual action instead of guessing). Plugin-bundled skills are listed in the agent's available skills when the plugin is enabled; the full skill instructions are loaded on demand, so routine turns do not pay the full token cost.

## Profiles: `openclaw` vs `user`

- `openclaw`: managed, isolated browser (no extension required).
- `user`: built-in Chrome MCP attach profile for your **real signed-in Chrome** session.

For agent browser tool calls: by default, use the isolated `openclaw` browser; prefer `profile="user"` when existing logged-in sessions matter and the user is at the computer to click/approve any attach prompt; and `profile` is the explicit override when you want a specific browser mode. Set `browser.defaultProfile: "openclaw"` if you want managed mode by default.

## Configuration

Browser settings live in `~/.openclaw/openclaw.json`. The core `browser.*` block (illustrative defaults and multi-profile examples) is:

```json5
{
  browser: {
    enabled: true, // default: true
    ssrfPolicy: {
      // dangerouslyAllowPrivateNetwork: true, // opt in only for trusted private-network access
      // allowPrivateNetwork: true, // legacy alias
      // hostnameAllowlist: ["*.example.com", "example.com"],
      // allowedHostnames: ["localhost"],
    },
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    remoteCdpTimeoutMs: 1500, // remote CDP HTTP timeout (ms)
    remoteCdpHandshakeTimeoutMs: 3000, // remote CDP WebSocket handshake timeout (ms)
    localLaunchTimeoutMs: 15000, // local managed Chrome discovery timeout (ms)
    localCdpReadyTimeoutMs: 8000, // local managed post-launch CDP readiness timeout (ms)
    actionTimeoutMs: 60000, // default browser act timeout (ms)
    tabCleanup: {
      enabled: true, // default: true
      idleMinutes: 120, // set 0 to disable idle cleanup
      maxTabsPerSession: 8, // set 0 to disable the per-session cap
      sweepMinutes: 5,
    },
    defaultProfile: "openclaw",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC", headless: true },
      user: { driver: "existing-session", attachOnly: true, color: "#00AA00" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

The `### Screenshot vision (text-only model support)` sub-section of Configuration is covered in [oc_tools_browser_vision_remote](oc_tools_browser_vision_remote.md). The remaining Configuration knobs are documented below.

### Ports and reachability

- The control service binds to loopback on a port derived from `gateway.port` (default `18791` = gateway + 2). Overriding `gateway.port` or `OPENCLAW_GATEWAY_PORT` shifts the derived ports in the same family.
- Local `openclaw` profiles auto-assign `cdpPort`/`cdpUrl`; set those only for remote CDP profiles or existing-session endpoint attach. `cdpUrl` defaults to the managed local CDP port when unset.
- `remoteCdpTimeoutMs` applies to remote and `attachOnly` CDP HTTP reachability checks and tab-opening HTTP requests; `remoteCdpHandshakeTimeoutMs` applies to their CDP WebSocket handshakes.
- `localLaunchTimeoutMs` is the budget for a locally launched managed Chrome process to expose its CDP HTTP endpoint. `localCdpReadyTimeoutMs` is the follow-up budget for CDP websocket readiness after the process is discovered. Raise these on Raspberry Pi, low-end VPS, or older hardware where Chromium starts slowly. Values must be positive integers up to `120000` ms; invalid config values are rejected.
- Repeated managed Chrome launch/readiness failures are circuit-broken per profile. After several consecutive failures, OpenClaw pauses new launch attempts briefly instead of spawning Chromium on every browser tool call. Fix the startup problem, disable the browser if it is not needed, or restart the Gateway after repair.
- `actionTimeoutMs` is the default budget for browser `act` requests when the caller does not pass `timeoutMs`. The client transport adds a small slack window so long waits can finish instead of timing out at the HTTP boundary.
- `tabCleanup` is best-effort cleanup for tabs opened by primary-agent browser sessions. Subagent, cron, and ACP lifecycle cleanup still closes their explicit tracked tabs at session end; primary sessions keep active tabs reusable, then close idle or excess tracked tabs in the background.

### SSRF policy

- Browser navigation and open-tab are SSRF-guarded before navigation and best-effort re-checked on the final `http(s)` URL afterwards. In strict SSRF mode, remote CDP endpoint discovery and `/json/version` probes (`cdpUrl`) are checked too.
- Gateway/provider `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and `NO_PROXY` environment variables do not automatically proxy the OpenClaw-managed browser. Managed Chrome launches direct by default so provider proxy settings do not weaken browser SSRF checks.
- OpenClaw-managed local CDP readiness probes and DevTools WebSocket connections bypass the managed network proxy for the exact launched loopback endpoint, so `openclaw browser start` still works when an operator proxy blocks loopback egress.
- To proxy the managed browser itself, pass explicit Chrome proxy flags through `browser.extraArgs`, such as `--proxy-server=...` or `--proxy-pac-url=...`. Strict SSRF mode blocks explicit browser proxy routing unless private-network browser access is intentionally enabled.
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` is off by default; enable only when private-network browser access is intentionally trusted. `browser.ssrfPolicy.allowPrivateNetwork` remains supported as a legacy alias.

### Profile behavior

- `attachOnly: true` means never launch a local browser; only attach if one is already running.
- `headless` can be set globally or per local managed profile. Per-profile values override `browser.headless`, so one locally launched profile can stay headless while another remains visible.
- `POST /start?headless=true` and `openclaw browser start --headless` request a one-shot headless launch for local managed profiles without rewriting `browser.headless` or profile config. Existing-session, attach-only, and remote CDP profiles reject the override because OpenClaw does not launch those browser processes.
- On Linux hosts without `DISPLAY` or `WAYLAND_DISPLAY`, local managed profiles default to headless automatically when neither the environment nor profile/global config explicitly chooses headed mode. `openclaw browser status --json` reports `headlessSource` as `env`, `profile`, `config`, `request`, `linux-display-fallback`, or `default`.
- `OPENCLAW_BROWSER_HEADLESS=1` forces local managed launches headless for the current process. `OPENCLAW_BROWSER_HEADLESS=0` forces headed mode for ordinary starts and returns an actionable error on Linux hosts without a display server; an explicit `start --headless` request still wins for that one launch.
- `executablePath` can be set globally or per local managed profile. Per-profile values override `browser.executablePath`, so different managed profiles can launch different Chromium-based browsers. Both forms accept `~` for your OS home directory.
- `color` (top-level and per-profile) tints the browser UI so you can see which profile is active.
- Default profile is `openclaw` (managed standalone). Use `defaultProfile: "user"` to opt into the signed-in user browser.
- Auto-detect order: system default browser if Chromium-based; otherwise Chrome → Brave → Edge → Chromium → Chrome Canary.
- `driver: "existing-session"` uses Chrome DevTools MCP instead of raw CDP. It can attach through Chrome MCP auto-connect, or through `cdpUrl` when you already have a DevTools endpoint for the running browser.
- Set `browser.profiles.<name>.userDataDir` when an existing-session profile should attach to a non-default Chromium user profile (Brave, Edge, etc.). This path also accepts `~` for your OS home directory.

**Source**: OpenClaw documentation — `tools/browser` (mirror `inbox/openclaw_docs/tools/browser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
