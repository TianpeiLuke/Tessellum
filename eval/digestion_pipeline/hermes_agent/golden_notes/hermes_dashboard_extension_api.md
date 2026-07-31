---
tags:
  - resource
  - documentation
  - hermes_agent
  - dashboard
  - extension_api
keywords:
  - hermes plugin sdk
  - window __HERMES_PLUGIN_SDK__
  - register registerSlot
  - dashboard theme endpoints
  - dashboard plugin endpoints
  - stable extension contract
topics:
  - Hermes Agent
  - Dashboard Extension
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
access_control_group: ["general"]
---

# Hermes Dashboard Extension API

## Overview

The Hermes dashboard extension API is the **stable contract** a dashboard theme or UI plugin programs against — the single surface Hermes promises not to break under you. It has two halves that together let you reskin and extend the web dashboard without forking it or bundling your own React: a **client-side SDK** exposed on the browser `window`, and a small set of **REST endpoints** for theme/plugin discovery and asset serving. As a model (not a how-to), this note catalogs *what the contract is* — the named globals, the SDK members, and the HTTP routes — rather than walking through authoring a plugin (that procedure lives in [hermes_dashboard_plugins](hermes_dashboard_plugins.md)).

The two `window` globals are the heart of it. `window.__HERMES_PLUGIN_SDK__` hands a plugin everything it needs (the shared React instance, hooks, shadcn/ui components, the typed API client, a raw JSON fetcher, and utilities) so plugin bundles stay tiny — "typically a few KB" — and never version-skew against the dashboard's own React. `window.__HERMES_PLUGINS__.register` / `.registerSlot` are the registration entry points a plugin's IIFE calls to mount a component as a route or inject into a named shell/page slot. Both globals are provided by the dashboard front-end's `registry.ts` and `main.tsx`. The REST half (`/api/dashboard/themes`, `/api/dashboard/theme`, `/api/dashboard/plugins`, `/api/dashboard/plugins/rescan`, static `/dashboard-plugins/<name>/<path>`) is served by the same FastAPI dashboard server documented in [hermes_dashboard_rest_api](hermes_dashboard_rest_api.md) and sits behind the same auth gate when the dashboard is bound non-locally.

## The Plugin SDK Surface

Everything a plugin needs is on `window.__HERMES_PLUGIN_SDK__`. Plugins should never import React directly — the React instance comes from the SDK, which is what keeps bundles small and avoids version conflicts. The full surface, verbatim from the source enumeration:

```javascript
const SDK = window.__HERMES_PLUGIN_SDK__;

// React + hooks
SDK.React                    // the React instance
SDK.hooks.useState
SDK.hooks.useEffect
SDK.hooks.useCallback
SDK.hooks.useMemo
SDK.hooks.useRef
SDK.hooks.useContext
SDK.hooks.createContext

// UI components (shadcn/ui primitives)
SDK.components.Card
SDK.components.CardHeader
SDK.components.CardTitle
SDK.components.CardContent
SDK.components.Badge
SDK.components.Button
SDK.components.Input
SDK.components.Label
SDK.components.Select
SDK.components.SelectOption
SDK.components.Separator
SDK.components.Tabs
SDK.components.TabsList
SDK.components.TabsTrigger
SDK.components.PluginSlot    // render a named slot (useful for nested plugin UIs)

// Hermes API client + raw fetcher
SDK.api                      // typed client — getStatus, getSessions, getConfig, ...
SDK.fetchJSON                // raw fetch for custom endpoints (plugin-registered routes)

// Utilities
SDK.utils.cn                 // Tailwind class merger (clsx + twMerge)
SDK.utils.timeAgo            // "5m ago" from unix timestamp
SDK.utils.isoTimeAgo         // "5m ago" from ISO string

// Hooks
SDK.useI18n                  // i18n hook for multi-language plugins
```

Three contract guarantees follow from this surface:

- **`SDK.api`** is the typed client for built-in Hermes endpoints (`getStatus`, `getSessions`, `getConfig`, …). **`SDK.fetchJSON`** is the escape hatch for custom endpoints — notably a plugin's own backend routes; it injects the session auth token, surfaces errors as thrown exceptions, and parses JSON automatically.
- **`SDK.components.PluginSlot`** lets a plugin render a named slot, including slots a plugin exposes for its own nested UIs — the registry accepts slot names beyond the shell's built-in catalogue for exactly this.
- **`SDK.React`** is the single source of React. Because React is never bundled by the plugin, a plugin authored with JSX must mark React as an external and emit a single IIFE file loadable via `<script>`.

## The Registration Globals

The second global, `window.__HERMES_PLUGINS__`, is the registry a plugin's bundle calls into. Two functions form the registration contract:

```javascript
// Register a plugin's main component (mounted as a route / nav tab).
window.__HERMES_PLUGINS__.register("my-plugin", MyPage);

// Register a component into a named shell or page-scoped slot.
window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sidebar", MySidebar);
window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sessions:top", Banner);
```

Contract semantics the model fixes:

- `register(name, Component)` registers a plugin's main component; the dashboard resolves it against the manifest and mounts it as a route (adding a nav tab unless `tab.hidden`).
- `registerSlot(name, slot, Component)` registers into a named slot; multiple plugins can populate the same slot and render stacked in registration order.
- Re-registering the same `(plugin, slot)` pair **replaces** the earlier registration — this matches how React HMR expects plugin re-mounts to behave.
- A plugin's IIFE has up to **2 seconds** after its script loads to call `register()`; later registrations still appear because the nav is reactive.

## API Reference — Endpoints

The REST half of the contract is three endpoint groups served by the dashboard FastAPI server. The first two tables are verbatim from the source's API reference.

### Theme endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/themes` | GET | List available themes + active name. Built-ins return `{name, label, description}`; user themes also include a `definition` field with the full normalised theme object. |
| `/api/dashboard/theme` | PUT | Set active theme. Body: `{"name": "midnight"}`. Persists to `config.yaml` under `dashboard.theme`. |

### Plugin endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/plugins` | GET | List discovered plugins (with manifests, minus internal fields). |
| `/api/dashboard/plugins/rescan` | GET | Force re-scan the plugin directories without restarting. |
| `/dashboard-plugins/<name>/<path>` | GET | Serve static assets from a plugin's `dashboard/` directory. Path traversal is blocked. |
| `/api/plugins/<name>/*` | * | Plugin-registered backend routes. |

The `definition` field on `GET /api/dashboard/themes` is the normalised theme object documented in [hermes_dashboard_themes](hermes_dashboard_themes.md); `PUT /api/dashboard/theme` is the persistence write the theme switcher performs. `GET /api/dashboard/plugins` is the discovery feed `App.tsx` fetches on load, and `/api/dashboard/plugins/rescan` re-runs the 3-directory discovery without a restart. Static plugin assets are served read-only under `/dashboard-plugins/<name>/<path>` with path traversal blocked; the `/api/plugins/<name>/*` family is the plugin's own FastAPI router mount point.

## API Reference — SDK on `window`

The two globals and the SDK object are the named providers of the client contract, verbatim from the source:

| Global | Type | Provider |
|--------|------|----------|
| `window.__HERMES_PLUGIN_SDK__` | object | `registry.ts` — React, hooks, UI components, API client, utils. |
| `window.__HERMES_PLUGINS__.register(name, Component)` | function | Register a plugin's main component. |
| `window.__HERMES_PLUGINS__.registerSlot(name, slot, Component)` | function | Register into a named shell slot. |

`main.tsx` is what exposes `window.__HERMES_PLUGIN_SDK__` and `window.__HERMES_PLUGINS__` at dashboard load; `registry.ts` is the module that defines the SDK surface and the `register`/`registerSlot` globals. This provenance is what makes the surface a *stable contract* rather than an internal detail — a plugin authored against these globals keeps working across dashboard updates that change internal implementation.

**Source**: `inbox/hermes_agent_docs/user-guide/features/extending-the-dashboard.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
**Last Updated**: 2026-06-19
**Status**: Active
