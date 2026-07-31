---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - security
keywords:
  - openclaw browser security
  - browser isolation guarantees
  - ssrf policy navigation block
  - chrome devtools mcp existing session
  - loopback browser shared-secret auth
  - dangerouslyAllowPrivateNetwork
  - dedicated user data dir ports
  - cdp startup vs ssrf block
  - browser agent tool target sandbox host
topics:
  - OpenClaw
  - Browser Security and Isolation
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/browser
access_control_group: ["general"]
---

# OpenClaw — Browser Security and Isolation Model

## Overview

This note models the **security and isolation contract** of the OpenClaw-managed browser, mirroring the Security, Existing session via Chrome DevTools MCP (Custom Chrome MCP launch), Isolation guarantees, Control API (pointer), Troubleshooting › CDP startup failure vs navigation SSRF block, and Agent tools + how control works sections of the `tools/browser` source page. It explains why the agent browser is safe to expose: it runs as a dedicated profile with its own user data directory and dedicated CDP ports, its loopback HTTP control plane authenticates only with shared-secret credentials, page navigation is SSRF-guarded, and the higher-risk path of attaching to your real signed-in Chrome via Chrome DevTools MCP requires explicit consent. The companion notes cover setup/config ([oc_tools_browser_overview](oc_tools_browser_overview.md)), vision/remote control ([oc_tools_browser_vision_remote](oc_tools_browser_vision_remote.md)), and the loopback HTTP/CLI control reference ([oc_tools_browser_control](oc_tools_browser_control.md)).

## Loopback control plane and shared-secret auth

Browser control is **loopback-only**: access flows through the Gateway's auth or node pairing, and the control service binds to loopback on a port derived from `gateway.port`. The standalone loopback browser HTTP API uses **shared-secret auth only** — one of gateway token bearer auth, the `x-openclaw-password` header, or HTTP Basic auth with the configured gateway password. Critically, **Tailscale Serve identity headers and `gateway.auth.mode: "trusted-proxy"` do NOT authenticate this standalone loopback browser API**: identity-bearing proxy modes are not honored for the browser control plane, so a shared secret is always required.

When browser control is enabled and no shared-secret auth is configured, OpenClaw **generates a runtime-only gateway token for that startup**. That token is ephemeral; to give clients a stable secret across restarts, configure `gateway.auth.token`, `gateway.auth.password`, `OPENCLAW_GATEWAY_TOKEN`, or `OPENCLAW_GATEWAY_PASSWORD` explicitly. OpenClaw does **not** auto-generate that token when `gateway.auth.mode` is already `password`, `none`, or `trusted-proxy`. Operationally, keep the Gateway and any node hosts on a private network (Tailscale) and avoid public exposure, and treat remote CDP URLs/tokens as secrets — prefer environment variables or a secrets manager. For remote CDP specifically, prefer encrypted endpoints (HTTPS or WSS) and short-lived tokens where possible, and avoid embedding long-lived tokens directly in config files.

## Isolation guarantees

The managed `openclaw` browser is isolated from your personal browser along three dimensions:

- **Dedicated user data dir** — the managed profile never touches your personal browser profile.
- **Dedicated ports** — the managed profile avoids `9222` specifically to prevent collisions with developer workflows; local CDP ports allocate from the `18800-18899` family by default.
- **Deterministic tab control** — `tabs` returns `suggestedTargetId` first, then stable `tabId` handles such as `t1`, optional labels, and the raw `targetId`. Agents should reuse `suggestedTargetId`; raw ids remain available for debugging and compatibility.

These guarantees are what make the agent browser a "safe, isolated surface" rather than your daily-driver browser, and they hold for the managed `openclaw`-managed profile mode (as opposed to the existing-session attach mode below).

## Existing session via Chrome DevTools MCP (higher-risk attach)

OpenClaw can also attach to a running Chromium-based browser through the official **Chrome DevTools MCP server**, reusing the tabs and login state already open in that browser profile. This is exposed through the built-in `user` profile (and optional custom existing-session profiles). The built-in `user` profile uses Chrome MCP auto-connect, which targets the default local Google Chrome profile; set `userDataDir` to attach to Brave, Edge, Chromium, or a non-default Chrome profile (`~` expands to your OS home directory). The driver is selected with `driver: "existing-session"`, which uses Chrome DevTools MCP instead of raw CDP; it can attach through Chrome MCP auto-connect, or through `cdpUrl` when you already have a DevTools endpoint for the running browser.

This path is explicitly **higher-risk than the isolated `openclaw` profile** because it can act inside your signed-in browser session — so it is gated on human presence and consent. Choose this mode only when the user is at the computer to approve the attach prompt. The operator workflow is: open the browser's inspect page for remote debugging, enable remote debugging, keep the browser running, and approve the connection prompt when OpenClaw attaches (common inspect pages are `chrome://inspect/#remote-debugging`, `brave://inspect/#remote-debugging`, and `edge://inspect/#remote-debugging`). OpenClaw does **not** launch the browser for this driver; it only attaches, and it uses the official Chrome DevTools MCP `--autoConnect` flow (passing `userDataDir` through when set). If attach does not work, verify the target browser is version `144+`, remote debugging is enabled, the consent prompt was accepted, and — if Chrome was started with an explicit `--remote-debugging-port` — that `browser.profiles.<name>.cdpUrl` points at that DevTools endpoint instead of relying on Chrome MCP auto-connect. `openclaw doctor` migrates old extension-based browser config and checks that Chrome is installed, but it **cannot enable browser-side remote debugging for you**.

### Custom Chrome MCP launch

You can override the spawned Chrome DevTools MCP server per profile when the default `npx chrome-devtools-mcp@latest` flow is not what you want (offline hosts, pinned versions, vendored binaries):

| Field        | What it does                                                                                                               |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `mcpCommand` | Executable to spawn instead of `npx`. Resolved as-is; absolute paths are honored.                                          |
| `mcpArgs`    | Argument array passed verbatim to `mcpCommand`. Replaces the default `chrome-devtools-mcp@latest --autoConnect` arguments. |

When `cdpUrl` is set on an existing-session profile, OpenClaw **skips `--autoConnect`** and forwards the endpoint to Chrome MCP automatically: `http(s)://...` becomes `--browserUrl <url>` (DevTools HTTP discovery endpoint) and `ws(s)://...` becomes `--wsEndpoint <url>` (direct CDP WebSocket). Endpoint flags and `userDataDir` cannot be combined: when `cdpUrl` is set, `userDataDir` is ignored for Chrome MCP launch, since Chrome MCP attaches to the running browser behind the endpoint rather than opening a profile directory. Existing-session drivers are also more feature-constrained than the managed profile — CSS selectors are unavailable (actions require snapshot refs), `wait --load networkidle` is unsupported, and batch actions, PDF export, download interception, and `responsebody` still require the managed browser path.

## The SSRF / navigation safety boundary

Page navigation is protected independently of the control-plane health. **Browser navigation and open-tab are SSRF-guarded before navigation and best-effort re-checked on the final `http(s)` URL afterwards.** In strict SSRF mode, remote CDP endpoint discovery and `/json/version` probes (`cdpUrl`) are checked too. The browser config **defaults to a fail-closed SSRF policy object even when you do not configure `browser.ssrfPolicy`** — the safety boundary is on by default. The escape hatches are deliberately named to signal risk: `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` is off by default and should be enabled only when private-network browser access is intentionally trusted (`browser.ssrfPolicy.allowPrivateNetwork` remains supported as a legacy alias), and the narrower `hostnameAllowlist` / `allowedHostnames` exceptions are preferred over broad private-network access.

A subtle but important carve-out: for the local loopback `openclaw` managed profile, CDP health checks **intentionally skip browser SSRF reachability enforcement for OpenClaw's own local control plane** — but navigation protection is separate, so a successful `start` or `tabs` result does not mean a later `open` or `navigate` target is allowed. Operator proxy variables (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY`) do not automatically proxy the managed browser: managed Chrome launches direct by default so provider proxy settings do not weaken browser SSRF checks, and routing the managed browser through a proxy requires explicit Chrome proxy flags via `browser.extraArgs` (which strict SSRF mode blocks unless private-network browser access is intentionally enabled).

### CDP startup failure vs navigation SSRF block

These are **two different failure classes** that point to different code paths, and conflating them sends you to the wrong fix:

- **CDP startup or readiness failure** means OpenClaw cannot confirm that the browser control plane is healthy. Examples: `Chrome CDP websocket for profile "openclaw" is not reachable after start`, `Remote CDP for profile "<name>" is not reachable at <cdpUrl>`, and `Port <port> is in use for profile "<name>" but not by openclaw` (a loopback external CDP service configured without `attachOnly: true`).
- **Navigation SSRF block** means the browser control plane is healthy, but a page navigation target is rejected by policy — `open`, `navigate`, snapshot, or tab-opening flows fail with a browser/network policy error while `start` and `tabs` still work.

Use this minimal sequence to separate the two:

```bash
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw tabs
openclaw browser --browser-profile openclaw open https://example.com
```

Read the results as a decision tree: if `start` fails with `not reachable after start`, troubleshoot CDP readiness first; if `start` succeeds but `tabs` fails, the control plane is still unhealthy (treat as a CDP reachability problem, not a navigation problem); if `start` and `tabs` succeed but `open`/`navigate` fails, the control plane is up and the failure is in navigation policy or the target page; if all three succeed, the basic managed-browser control path is healthy. Security guidance: do **not** relax browser SSRF policy by default, prefer narrow host exceptions over broad private-network access, and use `dangerouslyAllowPrivateNetwork: true` only in intentionally trusted, reviewed environments.

## Control API (pointer) and how the agent tool maps to control

For scripting and debugging, the Gateway exposes a small **loopback-only HTTP control API** plus a matching `openclaw browser` CLI (snapshots, refs, wait power-ups, JSON output, debug workflows); the full reference is the companion note [oc_tools_browser_control](oc_tools_browser_control.md). From the agent's side, the surface is intentionally narrow: the agent gets **one tool**, `browser`, exposing `doctor/status/start/stop/tabs/open/focus/close/snapshot/screenshot/navigate/act`. It maps to the control plane as: `browser snapshot` returns a stable UI tree (AI or ARIA), `browser act` uses the snapshot `ref` IDs to click/type/drag/select, `browser screenshot` captures pixels (full page, element, or labeled refs), and `browser doctor` checks Gateway, plugin, profile, browser, and tab readiness. This single-tool, snapshot-then-act design keeps the agent deterministic and avoids brittle selectors.

The `browser` tool accepts a `profile` parameter (choose a named profile — `openclaw`, `chrome`, or remote CDP) and a `target` parameter (`sandbox` | `host` | `node`) selecting where the browser lives. The placement rules are security-relevant: in sandboxed sessions, `target: "host"` requires `agents.defaults.sandbox.browser.allowHostControl=true`; if `target` is omitted, sandboxed sessions default to `sandbox` while non-sandbox sessions default to `host`; and if a browser-capable node is connected, the tool may auto-route to it unless you pin `target="host"` or `target="node"`.

**Source**: OpenClaw documentation — `tools/browser` (mirror `inbox/openclaw_docs/tools/browser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
