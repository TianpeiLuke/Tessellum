---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - browser
keywords:
  - openclaw browser cli
  - browser control surface
  - browser profiles managed user cdp
  - openclaw browser snapshot screenshot
  - ref-based browser actions
  - existing chrome via mcp
  - remote browser node host proxy
  - navigation ssrf policy block
  - cdp readiness doctor
topics:
  - OpenClaw
  - CLI Browser Control
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/browser
access_control_group: ["general"]
---

# OpenClaw — `openclaw browser` CLI Browser Control

## Overview

This note is the procedure reference for `openclaw browser`, the CLI that manages OpenClaw's browser control surface and runs browser actions: lifecycle, profiles, tabs, snapshots/screenshots, ref-based UI automation, state emulation, cookies/storage, debugging, attaching to an existing Chrome via Chrome MCP, and proxying browser actions to a remote node host. It mirrors the `cli/browser` source page; the browser tool API, deeper SSRF/CDP troubleshooting, and remote security setup are linked out to `tools/browser`, `gateway/remote`, `gateway/tailscale`, and `gateway/security` rather than duplicated here.

## Common flags

The common flags that apply across `openclaw browser` subcommands are: `--url <gatewayWsUrl>` (Gateway WebSocket URL, defaults to config), `--token <token>` (Gateway token, if required), `--timeout <ms>` (request timeout in ms), `--expect-final` (wait for a final Gateway response), `--browser-profile <name>` (choose a browser profile, default from config), and `--json` (machine-readable output, where supported).

## Quick start, troubleshooting, and lifecycle

A minimal local startup sequence lists profiles, starts the managed profile, opens a page, and takes a snapshot; agents can run the same readiness check with `browser({ action: "doctor" })`. For troubleshooting: if `start` fails with `not reachable after start`, troubleshoot CDP readiness first; if `start` and `tabs` succeed but `open` or `navigate` fails, the browser control plane is healthy and the failure is usually navigation SSRF policy. Lifecycle subcommands cover status/health and start/stop. The quick-start, minimal-diagnostic, and lifecycle commands are:

```bash
# Quick start (local)
openclaw browser profiles
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
# Quick troubleshooting (minimal diagnostic sequence)
openclaw browser --browser-profile openclaw doctor
openclaw browser --browser-profile openclaw tabs
# Lifecycle
openclaw browser status
openclaw browser doctor --deep
openclaw browser start --headless
openclaw browser stop
openclaw browser --browser-profile openclaw reset-profile
```

Detailed troubleshooting guidance lives in the Browser tool troubleshooting section (linked under References). Lifecycle notes from the source: `doctor --deep` adds a live snapshot probe, useful when basic CDP readiness is green but you want proof that the current tab can be inspected. For `attachOnly` and remote CDP profiles, `openclaw browser stop` closes the active control session and clears temporary emulation overrides even when OpenClaw did not launch the browser process itself; for local managed profiles, `openclaw browser stop` stops the spawned browser process. `openclaw browser start --headless` applies only to that start request and only when OpenClaw launches a local managed browser — it does not rewrite `browser.headless` or profile config, and it is a no-op for an already-running browser. On Linux hosts without `DISPLAY` or `WAYLAND_DISPLAY`, local managed profiles run headless automatically unless `OPENCLAW_BROWSER_HEADLESS=0`, `browser.headless=false`, or `browser.profiles.<name>.headless=false` explicitly requests a visible browser.

## If the command is missing

If `openclaw browser` is an unknown command, check `plugins.allow` in `~/.openclaw/openclaw.json`. When `plugins.allow` is present, list the bundled browser plugin explicitly unless the config already has a root `browser` block:

```json5
{
  plugins: {
    allow: ["telegram", "browser"],
  },
}
```

An explicit root `browser` block — for example `browser.enabled=true` or `browser.profiles.<name>` — also activates the bundled browser plugin under a restrictive plugin allowlist.

## Profiles and tabs

Profiles are named browser routing configs. The three kinds are: `openclaw` (launches or attaches to a dedicated OpenClaw-managed Chrome instance with an isolated user data dir), `user` (controls your existing signed-in Chrome session via Chrome DevTools MCP), and custom CDP profiles (point at a local or remote CDP endpoint). Profile management and tab subcommands are:

```bash
# Profiles
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser create-profile --name chrome-live --driver existing-session
openclaw browser create-profile --name remote --cdp-url https://browser-host.example.com
openclaw browser delete-profile --name work
openclaw browser --browser-profile work tabs
# Tabs
openclaw browser tab new --label docs
openclaw browser tab label t1 docs
openclaw browser tab select 2
openclaw browser tab close 2
openclaw browser open https://docs.openclaw.ai --label docs
openclaw browser focus docs
openclaw browser close t1
```

`tabs` returns `suggestedTargetId` first, then the stable `tabId` such as `t1`, the optional label, and the raw `targetId`. Agents should pass `suggestedTargetId` back into `focus`, `close`, snapshots, and actions. You can assign a label with `open --label`, `tab new --label`, or `tab label`; labels, tab ids, raw target ids, and unique target-id prefixes are all accepted. The request field is still named `targetId` for compatibility, but it accepts these tab references. Treat raw target ids as diagnostic handles, not durable agent memory. When Chromium replaces the underlying raw target during a navigation or form submit, OpenClaw keeps the stable `tabId`/label attached to the replacement tab when it can prove the match; raw target ids remain volatile, so prefer `suggestedTargetId`.

## Snapshot / screenshot / actions

Snapshots and screenshots capture page state; `snapshot --urls` appends discovered link destinations to AI snapshots so agents can choose direct navigation targets instead of guessing from link text alone. Screenshot scope flags include `--full-page`, `--ref e12`, and `--labels`. Ref-based UI automation (navigate, click, type, and related actions) plus file/dialog helpers share the same surface; the snapshot, screenshot, action, and file/dialog commands are:

```bash
# Snapshot / screenshot
openclaw browser snapshot
openclaw browser snapshot --urls
openclaw browser screenshot --full-page
openclaw browser screenshot --ref e12
openclaw browser screenshot --labels
# Ref-based UI automation
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser click-coords 120 340
openclaw browser type <ref> "hello"
openclaw browser press Enter
openclaw browser hover <ref>
openclaw browser scrollintoview <ref>
openclaw browser drag <startRef> <endRef>
openclaw browser select <ref> OptionA OptionB
openclaw browser fill --fields '[{"ref":"1","value":"Ada"}]'
openclaw browser wait --text "Done"
openclaw browser evaluate --fn '(el) => el.textContent' --ref <ref>
# File + dialog helpers
openclaw browser upload media://inbound/file.pdf --ref <ref>
openclaw browser waitfordownload
openclaw browser download <ref> report.pdf
openclaw browser dialog --accept
openclaw browser dialog --dismiss --dialog-id d1
```

Screenshot notes from the source: `--full-page` is for page captures only and cannot be combined with `--ref` or `--element`. The `existing-session` / `user` profiles support page screenshots and `--ref` screenshots from snapshot output, but not CSS `--element` screenshots. `--labels` overlays current snapshot refs on the screenshot; on Playwright-backed profiles it works with `--full-page` (full-page label overlay), `--ref` (element-clip label overlay by ARIA ref), and `--element` (element-clip label overlay by CSS selector), with labels projected relative to the element in element-clip modes. The response also includes an `annotations` array with each ref's bounding box — each item has `ref`, `number`, `role`, optional `name`, and `box: {x, y, width, height}` in the captured image's space (viewport / fullpage / element-relative), and the field is omitted when empty. `existing-session` profiles render a chrome-mcp overlay on page screenshots but do not use the Playwright projection helper and do not include `annotations`, and CSS `--element` screenshots are unsupported there; without Playwright or chrome-mcp, labeled screenshots are not available. Prior releases ignored `--full-page`, `--ref`, and `--element` on labeled Playwright screenshots and always returned a viewport capture, but labeled screenshots now honor those scopes. `evaluate --fn` accepts a function source, an expression, or a statement body; statement bodies are wrapped as async functions, so use `return` for the value you want back, and use `evaluate --timeout-ms <ms>` (e.g. `--timeout-ms 30000`) when the page-side function may need longer than the default evaluate timeout. Action responses return the current raw `targetId` after action-triggered page replacement when OpenClaw can prove the replacement tab, but scripts should still store and pass `suggestedTargetId`/labels for long-lived workflows. For file helpers, managed Chrome profiles save ordinary click-triggered downloads into the OpenClaw downloads directory (`/tmp/openclaw/downloads` by default, or the configured temp root), and `waitfordownload` or `download <ref> report.pdf` lets the agent wait for a specific file and return its path — those explicit waiters own the next download. Uploads accept files from the OpenClaw temp uploads root and OpenClaw-managed inbound media, including `media://inbound/<id>` and sandbox-relative `media/inbound/<id>` references, while nested media refs, traversal, and arbitrary local paths remain rejected. When an action opens a modal dialog, the action response returns `blockedByDialog` with `browserState.dialogs.pending`; pass `--dialog-id` (e.g. `openclaw browser dialog --dismiss --dialog-id d1`) to answer it directly, and dialogs handled outside OpenClaw appear under `browserState.dialogs.recent`.

## State and storage

Viewport/emulation and cookies/storage are set with their own subcommands:

```bash
# Viewport + emulation
openclaw browser resize 1280 720
openclaw browser set viewport 1280 720
openclaw browser set offline on
openclaw browser set media dark
openclaw browser set timezone Europe/London
openclaw browser set locale en-GB
openclaw browser set geo 51.5074 -0.1278 --accuracy 25
openclaw browser set device "iPhone 14"
openclaw browser set headers '{"x-test":"1"}'
openclaw browser set credentials myuser mypass
# Cookies + storage
openclaw browser cookies set session abc123 --url https://example.com
openclaw browser cookies clear
openclaw browser storage local get
openclaw browser storage local set token abc123
openclaw browser storage session clear
```

## Debugging

Debugging subcommands surface console/network/trace diagnostics, and existing-Chrome control via Chrome MCP uses the built-in `user` profile or a custom `existing-session` profile:

```bash
# Debugging
openclaw browser console --level error
openclaw browser pdf
openclaw browser responsebody "**/api"
openclaw browser highlight <ref>
openclaw browser errors --clear
openclaw browser requests --filter api
openclaw browser trace start
openclaw browser trace stop --out trace.zip
# Existing Chrome via MCP
openclaw browser --browser-profile user tabs
openclaw browser create-profile --name chrome-live --driver existing-session
openclaw browser create-profile --name brave-live --driver existing-session --user-data-dir "~/Library/Application Support/BraveSoftware/Brave-Browser"
openclaw browser create-profile --name chrome-port --driver existing-session --cdp-url http://127.0.0.1:9222
openclaw browser --browser-profile chrome-live tabs
```

## Existing Chrome via MCP

The default existing-session path is host-only Chrome MCP auto-connect; if the browser is already running with a DevTools endpoint, pass `--cdp-url` so Chrome MCP attaches to that endpoint instead. For Docker, Browserless, or other remote setups where Chrome MCP semantics are not needed, use a CDP profile. Current existing-session limits from the source: snapshot-driven actions use refs, not CSS selectors; `browser.actionTimeoutMs` defaults supported `act` requests to 60000 ms when callers omit `timeoutMs` (per-call `timeoutMs` still wins); `click` is left-click only; `type` does not support `slowly=true`; `press` does not support `delayMs`; `hover`, `scrollintoview`, `drag`, `select`, `fill`, and `evaluate` reject per-call timeout overrides; `select` supports one value only; `wait --load networkidle` is not supported on existing-session profiles (works on managed and raw/remote CDP); file uploads require `--ref` / `--input-ref`, do not support CSS `--element`, and currently support one file at a time; dialog hooks do not support `--timeout`; screenshots support page captures and `--ref`, but not CSS `--element`; and `responsebody`, download interception, PDF export, and batch actions still require a managed browser or raw CDP profile.

## Remote browser control (node host proxy)

If the Gateway runs on a different machine than the browser, run a **node host** on the machine that has Chrome/Brave/Edge/Chromium; the Gateway will proxy browser actions to that node (no separate browser control server required). Use `gateway.nodes.browser.mode` to control auto-routing and `gateway.nodes.browser.node` to pin a specific node if multiple are connected. Security and remote setup are linked out (see References).

**Source**: OpenClaw documentation — `cli/browser` (mirror `inbox/openclaw_docs/cli/browser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
