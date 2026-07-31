---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - security
keywords:
  - openclaw diffs viewer
  - diffs output details contract
  - diffs artifact lifecycle ttl
  - diffs viewer url loopback
  - allowRemoteViewer security
  - diffs viewer csp hardening
  - diffs file mode chromium
  - diffs remote miss throttling 429
topics:
  - OpenClaw
  - Diffs Tool
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/tools/diffs
access_control_group: ["general"]
---

# OpenClaw — Diffs Viewer Artifact and Security Model

## Overview

This note models the output, artifact, and security contract of OpenClaw's `diffs` diff-viewer plugin tool — the half of the `tools/diffs` source page that describes what a call *returns* and how the resulting viewer/file artifacts are hardened. It covers the structured `details` output contract (viewer/file/compat field sets and per-mode behavior), collapsed-unchanged-section semantics, the artifact lifecycle (storage location, TTL, cleanup), viewer URL construction and network behavior, the `security.allowRemoteViewer` toggle, the viewer/file-render hardening model (loopback-only binding, CSP, tokenized routes, remote-miss throttling, deny-by-default file rendering), Chromium browser requirements for file mode, troubleshooting symptoms, and operational guidance. The install/enable/modes/tool-input/syntax-highlighting/defaults *usage* half is the sibling note **[oc_tools_diffs_usage](oc_tools_diffs_usage.md)**.

## Output Details Contract

The tool returns structured metadata under `details`. The field set depends on whether a viewer artifact, a rendered file, or both are produced.

**Viewer fields** — shared fields for modes that create a viewer: `artifactId`, `viewerUrl`, `viewerPath`, `title`, `expiresAt`, `inputKind`, `fileCount`, `mode`, and `context`. The `context` object carries `agentId`, `sessionId`, `messageChannel`, and `agentAccountId` when available.

**File fields** — returned when a PNG or PDF is rendered: `artifactId`, `expiresAt`, `filePath`, `path` (same value as `filePath`, provided for message-tool compatibility), `fileBytes`, `fileFormat`, `fileQuality`, `fileScale`, and `fileMaxWidth`.

**Compatibility aliases** — also returned for existing callers: `format` (same value as `fileFormat`), `imagePath` (same value as `filePath`), `imageBytes` (same value as `fileBytes`), `imageQuality` (same value as `fileQuality`), `imageScale` (same value as `fileScale`), and `imageMaxWidth` (same value as `fileMaxWidth`).

The returned fields vary by mode as follows:

| Mode     | What is returned                                                                                                       |
| -------- | ---------------------------------------------------------------------------------------------------------------------- |
| `"view"` | Viewer fields only.                                                                                                    |
| `"file"` | File fields only, no viewer artifact.                                                                                  |
| `"both"` | Viewer fields plus file fields. If file rendering fails, viewer still returns with `fileError` and `imageError` alias. |

## Collapsed Unchanged Sections

The viewer can show collapsed rows such as `N unmodified lines`. Expand controls on those rows are conditional and not guaranteed for every input kind. Expand controls appear when the rendered diff has expandable context data, which is typical for before-and-after input. For many unified-patch inputs the omitted context bodies are not available in the parsed patch hunks, so the row can appear without expand controls — this is expected behavior. The per-call `expandUnchanged` option applies only when expandable context exists.

## Artifact Lifecycle and Storage

Artifacts are stored under the temp subfolder `$TMPDIR/openclaw-diffs`. Viewer artifact metadata contains a random artifact ID (20 hex chars), a random token (48 hex chars), `createdAt` and `expiresAt` timestamps, and the path to the stored `viewer.html`. The default artifact TTL is 30 minutes when not specified (the `ttlSeconds` input default is `1800`), and the maximum accepted viewer TTL is 6 hours (input max `21600`). Cleanup runs opportunistically after artifact creation, expired artifacts are deleted, and a fallback cleanup removes stale folders older than 24 hours when metadata is missing.

## Viewer URL and Network Behavior

The viewer is served at the route `/plugins/diffs/view/{artifactId}/{token}`. Its assets are served at `/plugins/diffs/assets/viewer.js`, `/plugins/diffs/assets/viewer-runtime.js`, and `/plugins/diffs-language-pack/assets/viewer.js` (the last only when the diff uses a language from the Diff Viewer Language Pack). The viewer document resolves those assets relative to the viewer URL, so an optional `baseUrl` path prefix is preserved for the asset requests too.

URL construction follows a precedence order: if a tool-call `baseUrl` is provided it is used after strict validation; else if the plugin `viewerBaseUrl` is configured it is used; without either override the viewer URL defaults to loopback `127.0.0.1`; and if the gateway bind mode is `custom` and `gateway.customBindHost` is set, that host is used. The `baseUrl` rules require an `http://` or `https://` URL, reject any query or hash, and allow an origin plus an optional base path.

## Security Model

The `security.allowRemoteViewer` config flag (default `false`) governs remote access: `false` denies non-loopback requests to viewer routes, while `true` allows remote viewers only if the tokenized path is valid.

**Viewer hardening** — the viewer is loopback-only by default, uses tokenized viewer paths with strict ID and token validation, and serves a response Content-Security-Policy of `default-src 'none'`, scripts and assets only from self, and no outbound `connect-src`. When remote access is enabled, remote-miss throttling applies: 40 failures per 60 seconds triggers a 60-second lockout returning `429 Too Many Requests`.

**File rendering hardening** — screenshot browser request routing is deny-by-default; only local viewer assets from `http://127.0.0.1/plugins/diffs/assets/*` are allowed; and external network requests are blocked.

## Browser Requirements for File Mode

`mode: "file"` and `mode: "both"` need a Chromium-compatible browser. The browser executable is resolved in this order: (1) `browser.executablePath` in OpenClaw config; (2) the environment variables `OPENCLAW_BROWSER_EXECUTABLE_PATH`, `BROWSER_EXECUTABLE_PATH`, and `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`; (3) platform command/path discovery fallback. When no browser is found the common failure text is `Diff PNG/PDF rendering requires a Chromium-compatible browser...`; the fix is to install Chrome, Chromium, Edge, or Brave, or to set one of the executable-path options above.

## Troubleshooting

**Input validation errors** — `Provide patch or both before and after text.` means include both `before` and `after`, or provide `patch`; `Provide either patch or before/after input, not both.` means do not mix input modes; `Invalid baseUrl: ...` means use an `http(s)` origin with optional path and no query/hash; `{field} exceeds maximum size (...)` means reduce payload size; a large-patch rejection means reduce patch file count or total lines.

**Viewer accessibility** — the viewer URL resolves to `127.0.0.1` by default. For remote access scenarios, either set the plugin `viewerBaseUrl`, pass `baseUrl` per tool call, or use `gateway.bind=custom` and `gateway.customBindHost`. If `gateway.trustedProxies` includes loopback for a same-host proxy (for example Tailscale Serve), raw loopback viewer requests without forwarded client-IP headers fail closed by design; for that proxy topology, prefer `mode: "file"` or `mode: "both"` when you only need an attachment, or intentionally enable `security.allowRemoteViewer` and set the plugin `viewerBaseUrl` or pass a proxy/public `baseUrl` when you need a shareable viewer URL. Enable `security.allowRemoteViewer` only when you intend external viewer access.

**Unmodified-lines row has no expand button** — this can happen for patch input when the patch does not carry expandable context; it is expected and does not indicate a viewer failure. **Artifact not found** — caused by the artifact expiring due to TTL, the token or path changing, or cleanup removing stale data.

## Operational Guidance

Prefer `mode: "view"` for local interactive reviews in canvas, and `mode: "file"` for outbound chat channels that need an attachment. Keep `allowRemoteViewer` disabled unless your deployment requires remote viewer URLs. Set explicit short `ttlSeconds` for sensitive diffs, and avoid sending secrets in diff input when not required. If your channel compresses images aggressively (for example Telegram or WhatsApp), prefer PDF output (`fileFormat: "pdf"`). The diff rendering engine is powered by Diffs.

**Source**: OpenClaw documentation — `tools/diffs` (mirror `inbox/openclaw_docs/tools/diffs.md`), viewer-artifact + security half
**Last Updated**: 2026-06-22
**Status**: Active
