---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - browser_control
keywords:
  - openclaw browser control api
  - openclaw browser cli reference
  - act error contract
  - playwright requirement browser
  - snapshots and refs
  - wait power-ups browser
  - browser json output
  - OPENCLAW_EAGER_BROWSER_CONTROL_SERVER
  - browser ssrfpolicy
  - browser evaluateEnabled
topics:
  - OpenClaw
  - Browser Control
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/browser-control
access_control_group: ["general"]
---

# OpenClaw — Browser Control API and CLI Reference

## Overview

This note is the procedural reference for OpenClaw's browser control surface: the loopback HTTP control API, the `openclaw browser` CLI, and the scripting patterns (snapshots, refs, waits, debug flows, JSON output, state knobs) used to drive the agent browser. It mirrors the `tools/browser-control` source page — the reference companion to the setup/config/profiles/security page `tools/browser` (linked, not duplicated here) — and applies when scripting or debugging the agent browser or adding custom automation with snapshots and refs.

## Control API (optional)

For local integrations only, the Gateway exposes a small loopback HTTP API. This standalone server is opt-in: set `OPENCLAW_EAGER_BROWSER_CONTROL_SERVER=1` in the gateway service environment and restart the gateway before the HTTP endpoints become available. Without this variable the browser control runtime still works through the CLI and agent tools, but nothing listens on the loopback control port. The endpoint groups exposed are:

- Status/start/stop: `GET /`, `POST /start`, `POST /stop`
- Tabs: `GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, `DELETE /tabs/:targetId`
- Snapshot/screenshot: `GET /snapshot`, `POST /screenshot`
- Actions: `POST /navigate`, `POST /act`
- Hooks: `POST /hooks/file-chooser`, `POST /hooks/dialog`
- Downloads: `POST /download`, `POST /wait/download`
- Permissions: `POST /permissions/grant`
- Debugging: `GET /console`, `POST /pdf`
- Debugging: `GET /errors`, `GET /requests`, `POST /trace/start`, `POST /trace/stop`, `POST /highlight`
- Network: `POST /response/body`
- State: `GET /cookies`, `POST /cookies/set`, `POST /cookies/clear`
- State: `GET /storage/:kind`, `POST /storage/:kind/set`, `POST /storage/:kind/clear`
- Settings: `POST /set/offline`, `POST /set/headers`, `POST /set/credentials`, `POST /set/geolocation`, `POST /set/media`, `POST /set/timezone`, `POST /set/locale`, `POST /set/device`

All endpoints accept `?profile=<name>`. `POST /start?headless=true` requests a one-shot headless launch for local managed profiles without changing persisted browser config; attach-only, remote CDP, and existing-session profiles reject that override because OpenClaw does not launch those browser processes. For tab endpoints, `targetId` is the compatibility field name — prefer `suggestedTargetId` from `GET /tabs` or `POST /tabs/open`; labels and `tabId` handles such as `t1` are also accepted, while raw CDP target ids and unique raw prefixes work but are volatile diagnostic handles.

If shared-secret gateway auth is configured, browser HTTP routes require auth too: `Authorization: Bearer <gateway token>`, or `x-openclaw-password: <gateway password>` (or HTTP Basic auth with that password). This standalone loopback browser API does **not** consume trusted-proxy or Tailscale Serve identity headers; if `gateway.auth.mode` is `none` or `trusted-proxy`, these routes do not inherit those identity-bearing modes, so keep them loopback-only.

### `/act` error contract

`POST /act` uses a structured error response for route-level validation and policy failures:

```json
{ "error": "<message>", "code": "ACT_*" }
```

Current `code` values: `ACT_KIND_REQUIRED` (400) — `kind` missing/unrecognized; `ACT_INVALID_REQUEST` (400) — payload failed normalization/validation; `ACT_SELECTOR_UNSUPPORTED` (400) — `selector` used with an unsupported action kind; `ACT_EVALUATE_DISABLED` (403) — `evaluate` (or `wait --fn`) disabled by config; `ACT_TARGET_ID_MISMATCH` (403) — top-level or batched `targetId` conflicts with request target; `ACT_EXISTING_SESSION_UNSUPPORTED` (501) — action unsupported for existing-session profiles. Other runtime failures may still return `{ "error": "<message>" }` without a `code` field.

### Playwright requirement

Some features (navigate/act/AI snapshot/role snapshot, element screenshots, PDF) require Playwright; if it isn't installed, those endpoints return a clear 501 error. What still works **without** Playwright (when a per-tab CDP WebSocket is available): ARIA snapshots; role-style accessibility snapshots (`--interactive`, `--compact`, `--depth`, `--efficient`) as an inspection/ref-discovery fallback while Playwright remains the primary action engine; page screenshots for the managed `openclaw` browser; page screenshots for `existing-session` / Chrome MCP profiles; and `existing-session` ref-based screenshots (`--ref`) from snapshot output. What still **needs** Playwright: `navigate`, `act`, AI snapshots that depend on Playwright's native AI snapshot format, CSS-selector element screenshots (`--element`), and full browser PDF export. Element screenshots also reject `--full-page`; the route returns `fullPage is not supported for element screenshots`.

If you see `Playwright is not available in this gateway build`, the packaged Gateway is missing the core browser runtime dependency — reinstall or update OpenClaw, then restart the gateway. For Docker, also install the Chromium binaries; for custom images bake Chromium in with `OPENCLAW_INSTALL_BROWSER=1 ./scripts/docker/setup.sh`, and for an existing image install through the bundled CLI:

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

Avoid `npx playwright` in Docker (npm override conflicts). To persist browser downloads, set `PLAYWRIGHT_BROWSERS_PATH` (for example, `/home/node/.cache/ms-playwright`) and make sure `/home/node` is persisted via `OPENCLAW_HOME_VOLUME` or a bind mount; OpenClaw auto-detects the persisted Chromium on Linux.

## How it works (internal)

A small loopback control server accepts HTTP requests and connects to Chromium-based browsers via CDP. Advanced actions (click/type/snapshot/PDF) go through Playwright on top of CDP; when Playwright is missing, only non-Playwright operations are available. The agent sees one stable interface while local/remote browsers and profiles swap underneath.

## CLI quick reference

All commands accept `--browser-profile <name>` to target a profile, and `--json` for machine-readable output. The source groups commands into basics (status/tabs/open/focus/close), inspection (screenshot/snapshot/console/errors/requests), actions (navigate/click/type/drag/wait/evaluate), and state (cookies/storage/offline/headers/geo/device). Representative commands across those groups:

```bash
openclaw browser start --headless # one-shot local managed headless launch
openclaw browser stop            # also clears emulation on attach-only/remote CDP
openclaw browser open https://example.com
openclaw browser snapshot --selector "#main" --interactive --compact --depth 6
openclaw browser screenshot --ref 12        # or --ref e12
openclaw browser click 12 --double           # or e12 for role refs
openclaw browser click-coords 120 340        # viewport coordinates
openclaw browser type 23 "hello" --submit
openclaw browser upload media://inbound/file.pdf
openclaw browser fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'
openclaw browser evaluate --fn '(el) => el.textContent' --ref 7
openclaw browser responsebody "**/api" --max-chars 5000
openclaw browser cookies set session abc123 --url "https://example.com"
openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"
openclaw browser set device "iPhone 14"
```

Key CLI behavior notes: `upload` and `dialog` are **arming** calls — run them before the click/press that triggers the chooser/dialog. If an action opens a modal, the response includes `blockedByDialog` and `browserState.dialogs.pending` (pass that `dialogId` to respond), while dialogs handled outside OpenClaw appear under `browserState.dialogs.recent`. `click`/`type`/etc require a `ref` from `snapshot` (numeric `12`, role ref `e12`, or actionable ARIA ref `ax12`); CSS selectors are intentionally unsupported for actions, so use `click-coords` when the viewport position is the only reliable target. Download and trace paths are constrained to OpenClaw temp roots: `/tmp/openclaw{,/downloads}` (fallback `${os.tmpdir()}/openclaw/...`). `upload` accepts files from the temp uploads root and OpenClaw-managed inbound media (referenced as `media://inbound/<id>`, sandbox-relative `media/inbound/<id>`, or a resolved path inside the managed inbound media directory; nested refs, traversal, symlinks, hardlinks, and arbitrary local paths are rejected), and can set file inputs directly via `--input-ref` or `--element`. Stable tab ids and labels survive Chromium raw-target replacement when OpenClaw can prove the replacement tab (such as same URL, or one old tab becoming one new tab after form submission); raw target ids stay volatile, so prefer `suggestedTargetId` from `tabs` in scripts.

Snapshot flags at a glance: `--format ai` (default with Playwright) gives an AI snapshot with numeric refs (`aria-ref="<n>"`); `--format aria` gives an accessibility tree with `axN` refs (with Playwright, refs bind to backend DOM ids so follow-up actions work, otherwise inspection-only); `--efficient` (or `--mode efficient`) is a compact role snapshot preset that `browser.snapshotDefaults.mode: "efficient"` makes default; `--interactive`, `--compact`, `--depth`, `--selector` force a role snapshot with `ref=e12` refs, and `--frame "<iframe>"` scopes them to an iframe. With Playwright, `--labels` adds a screenshot with overlayed ref labels (prints `MEDIA:<path>`) plus an `annotations` array of bounding boxes — on `screenshot` labels work with `--full-page`/`--ref`/`--element`, while on `snapshot` the screenshot stays viewport-only; existing-session/chrome-mcp profiles render overlay labels but return no `annotations`, and without Playwright or chrome-mcp labeled screenshots are unavailable. Finally, `--urls` appends discovered link destinations to AI snapshots.

## Snapshots and refs

OpenClaw supports three snapshot styles. The **AI snapshot (numeric refs)** is the default — `openclaw browser snapshot` (`--format ai`) outputs text with numeric refs (actions `click 12` / `type 23 "hello"`), resolved internally via Playwright's `aria-ref`. The **role snapshot (role refs like `e12`)** comes from `--interactive` (or `--compact`, `--depth`, `--selector`, `--frame`): output is a role list/tree with `[ref=e12]` (and optional `[nth=1]`), actions `click e12` / `highlight e12`, resolved via `getByRole(...)` plus `nth()` for duplicates; add `--labels` for a screenshot with overlayed `e12` labels (Playwright profiles also return per-ref `annotations[]`), and `--urls` when link text is ambiguous. The **ARIA snapshot (ARIA refs like `ax12`)** comes from `--format aria`: output is the accessibility tree as structured nodes, and `click ax12` works when the snapshot path binds the ref through Playwright and Chrome backend DOM ids. If Playwright is unavailable, ARIA snapshots stay useful for inspection but refs may not be actionable — re-snapshot with `--format ai` or `--interactive` for action refs. The Docker proof for the raw-CDP fallback path is `pnpm test:docker:browser-cdp-snapshot`, which starts Chromium with CDP, runs `browser doctor --deep`, and verifies role snapshots include link URLs, cursor-promoted clickables, and iframe metadata.

Ref behavior is constrained: refs are **not stable across navigations**, so if something fails, re-run `snapshot` and use a fresh ref. `/act` returns the current raw `targetId` after action-triggered replacement when it can prove the replacement tab, but keep using stable tab ids/labels for follow-up commands. If the role snapshot was taken with `--frame`, role refs are scoped to that iframe until the next role snapshot. Unknown or stale `axN` refs fail fast instead of falling through to Playwright's `aria-ref` selector — run a fresh snapshot on the same tab.

## Wait power-ups

You can wait on more than just time/text: wait for URL (globs supported by Playwright) with `openclaw browser wait --url "**/dash"`; wait for load state with `openclaw browser wait --load networkidle` (supported on managed `openclaw` and raw/remote CDP profiles, while `user` and `existing-session` profiles reject `networkidle` — use `--url`, `--text`, a selector, or `--fn` there); wait for a JS predicate with `openclaw browser wait --fn "window.ready===true"`; and wait for a selector to become visible with `openclaw browser wait "#main"`. These can be combined into one wait:

```bash
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## Debug workflows

When an action fails (e.g. "not visible", "strict mode violation", "covered"): (1) `openclaw browser snapshot --interactive`; (2) use `click <ref>` / `type <ref>` (prefer role refs in interactive mode); (3) if it still fails, `openclaw browser highlight <ref>` to see what Playwright is targeting; (4) if the page behaves oddly, run `openclaw browser errors --clear` and `openclaw browser requests --filter api --clear`; (5) for deep debugging, record a trace with `openclaw browser trace start`, reproduce the issue, then `openclaw browser trace stop` (prints `TRACE:<path>`).

## JSON output

`--json` is for scripting and structured tooling — for example `openclaw browser status --json`, `openclaw browser snapshot --interactive --json`, `openclaw browser requests --filter api --json`, `openclaw browser cookies --json`. Role snapshots in JSON include `refs` plus a small `stats` block (lines/chars/refs/interactive) so tools can reason about payload size and density.

## State and environment knobs

These support "make the site behave like X" workflows: Cookies (`cookies`, `cookies set`, `cookies clear`); Storage (`storage local|session get|set|clear`); Offline (`set offline on|off`); Headers (`set headers --headers-json '{"X-Debug":"1"}'`, legacy `set headers --json '{...}'` still supported); HTTP basic auth (`set credentials user pass`, or `--clear`); Geolocation (`set geo <lat> <lon> --origin "https://example.com"`, or `--clear`); Media (`set media dark|light|no-preference|none`); Timezone/locale (`set timezone ...`, `set locale ...`); Device/viewport (`set device "iPhone 14"` Playwright presets, `set viewport 1280 720`).

## Security and privacy

The `openclaw` browser profile may contain logged-in sessions, so treat it as sensitive. `browser act kind=evaluate` / `openclaw browser evaluate` and `wait --fn` execute arbitrary JavaScript in the page context, which prompt injection can steer — disable it with `browser.evaluateEnabled=false` if unneeded. `openclaw browser evaluate --fn` accepts a function source, an expression, or a statement body (statement bodies are wrapped as async functions, so use `return` for the value); use `--timeout-ms <ms>` when the page-side function needs longer than the default evaluate timeout. Keep the Gateway/node host private (loopback or tailnet-only), and treat remote CDP endpoints as powerful — tunnel and protect them. A strict-mode example that blocks private/internal destinations by default:

```json5
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false,
      hostnameAllowlist: ["*.example.com", "example.com"],
      allowedHostnames: ["localhost"], // optional exact allow
    },
  },
}
```

**Source**: OpenClaw documentation — `tools/browser-control` (mirror `inbox/openclaw_docs/tools/browser-control.md`)
**Last Updated**: 2026-06-22
**Status**: Active
