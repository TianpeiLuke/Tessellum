---
tags:
  - resource
  - documentation
  - hermes_agent
  - dashboard
  - plugins
keywords:
  - hermes dashboard plugin
  - plugin manifest.json
  - window.__HERMES_PLUGIN_SDK__
  - shell slots page-scoped slots
  - tab.override tab.hidden
  - backend FastAPI plugin routes
  - plugin discovery and reload
topics:
  - Hermes Agent
  - Dashboard Extension
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
access_control_group: ["general"]
---

# Hermes Dashboard Plugins

## Overview

A dashboard plugin is a **drop-in directory** that extends the Hermes web dashboard (`hermes dashboard`) without forking the codebase — a `manifest.json`, a pre-built JavaScript bundle, and optionally a CSS file and a Python file with FastAPI routes. Plugins live next to other Hermes plugins in `~/.hermes/plugins/<name>/`; the dashboard extension is a `dashboard/` subfolder inside that plugin directory, so a single install can extend both the CLI/gateway and the dashboard at once.

Plugins **do not bundle React or UI components**. They consume the Plugin SDK exposed on `window.__HERMES_PLUGIN_SDK__`, which keeps bundles tiny (typically a few KB) and avoids version conflicts. A plugin can add a whole new tab, replace a built-in page (`tab.override`), augment an existing page via page-scoped slots, inject components into named shell slots, register slot-only (`tab.hidden`), and expose backend routes mounted under `/api/plugins/<name>/`. This note is the procedure for authoring such a plugin; the co-located theming layer is covered separately (see [hermes_dashboard_themes](hermes_dashboard_themes.md)) and the stable contract is formalized as a model in [hermes_dashboard_extension_api](hermes_dashboard_extension_api.md).

## Quick start — your first plugin

Create the directory structure (note the `dashboard/` subdirectory and `dist/`):

```bash
mkdir -p ~/.hermes/plugins/my-plugin/dashboard/dist
```

Write the manifest and a plain-IIFE JS bundle (no build step needed). The bundle pulls everything it needs from `SDK` and registers its main component via `window.__HERMES_PLUGINS__.register`:

```javascript
// ~/.hermes/plugins/my-plugin/dashboard/dist/index.js
(function () {
  "use strict";

  const SDK = window.__HERMES_PLUGIN_SDK__;
  const { React } = SDK;
  const { Card, CardHeader, CardTitle, CardContent } = SDK.components;

  function MyPage() {
    return React.createElement(Card, null,
      React.createElement(CardHeader, null,
        React.createElement(CardTitle, null, "My Plugin"),
      ),
      React.createElement(CardContent, null,
        React.createElement("p", { className: "text-sm text-muted-foreground" },
          "Hello from my custom dashboard tab.",
        ),
      ),
    );
  }

  window.__HERMES_PLUGINS__.register("my-plugin", MyPage);
})();
```

Refresh the dashboard — the tab appears in the nav bar (here, after **Skills** because the manifest's `tab.position` is `after:skills`). If you prefer JSX, use any bundler (esbuild, Vite, rollup) with React as an external and IIFE output; the only hard requirement is a single JS file loadable via `<script>`, and React is never bundled — it comes from `SDK.React`.

## Directory layout

A single plugin directory carries three orthogonal extensions; include only the layers you need:

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml              # optional — existing CLI/gateway plugin manifest
├── __init__.py              # optional — existing CLI/gateway hooks
└── dashboard/               # dashboard extension
    ├── manifest.json        # required — tab config, icon, entry point
    ├── dist/
    │   ├── index.js         # required — pre-built JS bundle (IIFE)
    │   └── style.css        # optional — custom CSS
    └── plugin_api.py        # optional — backend API routes (FastAPI)
```

`plugin.yaml` + `__init__.py` is the CLI/gateway plugin; `dashboard/manifest.json` + `dashboard/dist/index.js` is the dashboard UI plugin; `dashboard/plugin_api.py` is the dashboard backend routes. None are required.

## Manifest reference

The manifest declares the tab, icon, entry point, and optional CSS/API. Full field surface:

```json
{
  "name": "my-plugin",
  "label": "My Plugin",
  "description": "What this plugin does",
  "icon": "Sparkles",
  "version": "1.0.0",
  "tab": {
    "path": "/my-plugin",
    "position": "after:skills",
    "override": "/",
    "hidden": false
  },
  "slots": ["sidebar", "header-left"],
  "entry": "dist/index.js",
  "css": "dist/style.css",
  "api": "plugin_api.py"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens ok). Used in URLs and registration. |
| `label` | Yes | Display name shown in the nav tab. |
| `description` | No | Short description shown in dashboard admin surfaces. |
| `icon` | No | Lucide icon name. Defaults to `Puzzle`; unknown names fall back to `Puzzle`. |
| `version` | No | Semver string. Defaults to `0.0.0`. |
| `tab.path` | Yes | URL path for the tab (e.g. `/my-plugin`). |
| `tab.position` | No | `"end"` (default), `"after:<path>"`, or `"before:<path>"` — value after the colon is the target tab's path **segment** (no leading slash). |
| `tab.override` | No | A built-in route path (`"/"`, `"/sessions"`, ...) to **replace** that page instead of adding a tab. |
| `tab.hidden` | No | When true, register the component and slots without adding a nav tab (slot-only plugins). |
| `slots` | No | Named shell slots populated — **documentation aid only**; actual binding is in the bundle via `registerSlot()`. |
| `entry` | Yes | Path to the JS bundle relative to `dashboard/`. Defaults to `dist/index.js`. |
| `css` | No | Path to a CSS file injected as a `<link>` tag. |
| `api` | No | Path to a Python file with FastAPI routes. Mounted at `/api/plugins/<name>/`. |

Icons are Lucide names mapped by `web/src/App.tsx`'s `ICON_MAP` (currently mapped: `Activity`, `BarChart3`, `Clock`, `Code`, `Database`, `Eye`, `FileText`, `Globe`, `Heart`, `KeyRound`, `MessageSquare`, `Package`, `Puzzle`, `Settings`, `Shield`, `Sparkles`, `Star`, `Terminal`, `Wrench`, `Zap`); adding one is a pure additive PR.

## The Plugin SDK and calling backends

Everything a plugin needs is on `window.__HERMES_PLUGIN_SDK__` (`SDK.React`, `SDK.hooks.*`, `SDK.components.*` shadcn/ui primitives, `SDK.api` typed client, `SDK.fetchJSON` raw fetcher, `SDK.utils.*`, `SDK.useI18n`). Plugins should never import React directly — the full surface is enumerated in [hermes_dashboard_extension_api](hermes_dashboard_extension_api.md). To call your own backend, `SDK.fetchJSON` injects the session auth token, surfaces errors as thrown exceptions, and parses JSON automatically:

```javascript
SDK.fetchJSON("/api/plugins/my-plugin/data")
  .then((data) => console.log(data))
  .catch((err) => console.error("API call failed:", err));

// Built-in Hermes endpoints via the typed client:
SDK.api.getStatus().then((s) => console.log("Version:", s.version));
SDK.api.getSessions(10).then((resp) => console.log(resp.sessions.length));
```

See [hermes_dashboard_rest_api](hermes_dashboard_rest_api.md) for the full endpoint list `SDK.api` wraps.

## Shell slots and page-scoped slots

Slots inject components into named locations of the app shell without claiming a whole tab. Multiple plugins can populate the same slot; they render stacked in registration order. Register from inside the bundle: `window.__HERMES_PLUGINS__.registerSlot("my-plugin", "sidebar", MySidebar)`.

**Shell-wide slots** (render anywhere in the chrome): `backdrop`, `header-left`, `header-right`, `header-banner`, `sidebar` (**only rendered when `layoutVariant === "cockpit"`**), `pre-main`, `post-main`, `footer-left`, `footer-right`, `overlay`.

**Page-scoped slots** (render only on the named built-in page) come as `<page>:top` / `<page>:bottom` pairs for: `sessions`, `analytics`, `logs`, `cron`, `skills`, `config`, `env` (Keys), `docs`, `chat` (chat only when embedded chat is enabled). Use these to add a banner, card, or toolbar to an existing page without overriding the whole route — the built-in page keeps working and your component renders alongside it. Combine with `tab.hidden: true` if your plugin only augments existing pages. The shell only renders `<PluginSlot name="..." />` for the catalogued slots; extra names are accepted by the registry for nested plugin UIs (via `SDK.components.PluginSlot`). If the same `(plugin, slot)` pair registers twice, the later call replaces the earlier one — matching React HMR re-mount behavior.

## tab.override and tab.hidden

`tab.override` set to a built-in route path makes the plugin's component replace that page instead of adding a new tab — useful for a custom home page (`/`) while keeping the rest intact. With `override` set, the original page component is removed from the router, your plugin renders at that path, and no nav tab is added for `tab.path`. Only one plugin can override a given path; on conflict the first wins and the second is ignored with a dev-mode warning. Full replacement is heavy (your plugin then owns the whole page, including future updates we ship) — prefer page-scoped slots when you only need to add a card or toolbar.

`tab.hidden: true` registers the component (for direct URL visits) and any slots, but never adds a nav tab — used by plugins that only inject into slots (a header crest, a sidebar HUD, an overlay). Best practice is to still call `register()` with a placeholder component in case the URL is hit directly, then `registerSlot()` for the real work.

## Backend API routes

Set `api` in the manifest and export a module-level `router = APIRouter()`. Routes mount under `/api/plugins/<name>/`, and because they run inside the dashboard process they can import the hermes-agent codebase directly:

```python
# ~/.hermes/plugins/my-plugin/dashboard/plugin_api.py
from fastapi import APIRouter
from hermes_state import SessionDB
from hermes_cli.config import load_config

router = APIRouter()

@router.get("/data")
async def get_data():
    return {"items": ["one", "two", "three"]}

@router.get("/session-count")
async def session_count():
    db = SessionDB()
    try:
        return {"count": len(db.list_sessions(limit=9999))}
    finally:
        db.close()
```

The above exposes `GET /api/plugins/my-plugin/data` and `GET /api/plugins/my-plugin/session-count`. Plugin API routes **bypass session-token authentication** since the dashboard server binds to localhost by default — **do not expose the dashboard on a public interface with `--host 0.0.0.0` if you run untrusted plugins**, because their routes become reachable too. (See [hermes_dashboard_auth_remote](hermes_dashboard_auth_remote.md) for the gate the rest of `/api/` sits behind.) Per-plugin CSS is injected as a `<link>` on load when `"css": "dist/style.css"` is set; reference the dashboard's `--color-*` / `--theme-asset-*` / `--component-<bucket>-*` / `--radius` / `--spacing-mul` CSS vars so the plugin reskins automatically with the active theme.

## Plugin discovery, reload & load lifecycle

The dashboard scans three directories for `dashboard/manifest.json`:

| Priority | Directory | Source label |
|----------|-----------|--------------|
| 1 (wins on conflict) | `~/.hermes/plugins/<name>/dashboard/` | `user` |
| 2 | `<repo>/plugins/memory/<name>/dashboard/` | `bundled` |
| 2 | `<repo>/plugins/<name>/dashboard/` | `bundled` |
| 3 | `./.hermes/plugins/<name>/dashboard/` | `project` — only when `HERMES_ENABLE_PROJECT_PLUGINS` is set |

Discovery results are cached per dashboard process. After adding a plugin, force a rescan without restart (`curl http://127.0.0.1:9119/api/dashboard/plugins/rescan`) or restart `hermes dashboard`. The **load lifecycle**: (1) `main.tsx` exposes the SDK on `window.__HERMES_PLUGIN_SDK__` and the registry on `window.__HERMES_PLUGINS__`; (2) `App.tsx` calls `usePlugins()` → `GET /api/dashboard/plugins`; (3) per manifest a CSS `<link>` (if declared) then a `<script>` tag loads the bundle; (4) the IIFE runs and calls `register(name, Component)` plus optional `registerSlot(...)`; (5) the dashboard resolves the component, adds the tab (unless `hidden`), and mounts the route. Plugins have up to **2 seconds** after their script loads to call `register()`; later registrations still appear (the nav is reactive). A failed script (404, syntax error, IIFE exception) logs a browser-console warning and the dashboard continues without it.

## Combined theme + plugin demo

The `strike-freedom-cockpit` plugin (companion repo `hermes-example-plugins`) is a complete reskin demo pairing a theme YAML with a slot-only plugin to produce a cockpit-style HUD without forking. It demonstrates a full theme (palette, typography, `fontUrl`, `layoutVariant: cockpit`, `assets`, `componentStyles`, `colorOverrides`, `customCSS`) plus a `tab.hidden: true` plugin registering three slots: `sidebar` (an MS-STATUS panel with live telemetry bars driven by `SDK.api.getStatus()`), `header-left` (a crest reading `--theme-asset-crest`), and `footer-right` (a tagline). Install by cloning the repo, copying the theme YAML into `~/.hermes/dashboard-themes/` and the plugin dir into `~/.hermes/plugins/`, then picking **Strike Freedom** in the theme switcher (the `sidebar` slot only renders under the `cockpit` variant). The `example-dashboard` reference plugin in the same repo ships a simpler `sessions:top` banner demo.

## Troubleshooting

- **Plugin tab doesn't show up.** Confirm the manifest is at `~/.hermes/plugins/<name>/dashboard/manifest.json` (note the `dashboard/` subdir); `curl .../api/dashboard/plugins/rescan`; check Network for 404s on `manifest.json`/`index.js`/CSS; check Console for IIFE errors or `window.__HERMES_PLUGINS__ is undefined` (usually an earlier React render crash); verify the bundle's `register(...)` name matches `manifest.json:name`.
- **Slot-registered components don't render.** The `sidebar` slot only renders under `layoutVariant: cockpit`; other slots always render. Add a `console.log` in `registerSlot` to confirm the bundle ran.
- **Backend routes return 404.** Confirm `"api": "plugin_api.py"` points to an existing file inside `dashboard/`; **restart** `hermes dashboard` (plugin API routes mount once at startup, **not** on rescan); ensure a module-level `router = APIRouter()` is exported; tail `~/.hermes/logs/errors.log` for `Failed to load plugin <name> API routes`.
- **Shipping on PyPI.** Dashboard plugins install by directory layout, not pip entry point; the cleanest path today is a git repo cloned into `~/.hermes/plugins/`.

**Source**: `inbox/hermes_agent_docs/user-guide/features/extending-the-dashboard.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
**Last Updated**: 2026-06-19
**Status**: Active
