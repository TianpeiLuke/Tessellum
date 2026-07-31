---
tags:
  - resource
  - documentation
  - hermes_agent
  - web_dashboard
  - administration
keywords:
  - hermes dashboard
  - browser admin panel
  - profile switcher
  - embedded TUI chat
  - admin pages tour
  - reload slash command
topics:
  - Hermes Agent
  - Web Dashboard
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
access_control_group: ["general"]
---

# Hermes Agent — Web Dashboard Overview

## Overview

The web dashboard is the **browser-based administration surface** for a Hermes Agent installation: instead of editing `config.yaml` or running CLI commands, an operator launches `hermes dashboard` and manages configuration, API keys, sessions, MCP servers, messaging, cron, skills, and host operations from a React single-page app fronting a local FastAPI server. By default it binds to `http://127.0.0.1:9119` and runs entirely on the machine — no data leaves localhost. It is a **machine-level** surface: one server manages every [profile](hermes_profiles_multi_agent.md) on the host, and a sidebar profile switcher decides which profile the management pages read and write. This note is the operator-level tour — launching the server, the profile switcher, the `web`/`pty` extras, the embedded TUI Chat tab, and a one-line walkthrough of all 16 admin pages. The HTTP surface the SPA consumes is documented separately in [hermes_dashboard_rest_api](hermes_dashboard_rest_api.md); securing a non-loopback dashboard (the auth gate, remote-backend wiring) is in [hermes_dashboard_auth_remote](hermes_dashboard_auth_remote.md); theming and plugins are in [hermes_dashboard_themes](hermes_dashboard_themes.md) / [hermes_dashboard_plugins](hermes_dashboard_plugins.md).

## Quick Start

```bash
hermes dashboard
```

This starts a local web server and opens `http://127.0.0.1:9119` in your browser. The dashboard runs entirely on your machine — no data leaves localhost.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `9119` | Port to run the web server on |
| `--host` | `127.0.0.1` | Bind address |
| `--no-open` | — | Don't auto-open the browser |
| `--insecure` | off | Allow binding to non-localhost hosts (**DANGEROUS** — exposes API keys on the network; pair with a firewall and strong auth) |
| `--isolated` | off | When launched from a named profile (`worker dashboard`), run a dedicated per-profile server instead of routing to the machine dashboard |

```bash
# Custom port
hermes dashboard --port 8080

# Bind to all interfaces (use with caution on shared networks)
hermes dashboard --host 0.0.0.0

# Start without opening browser
hermes dashboard --no-open
```

Binding to anything other than loopback engages the auth gate — see [hermes_dashboard_auth_remote](hermes_dashboard_auth_remote.md) for the gated-mode setup.

## Managing multiple profiles

The dashboard is a **machine-level** management surface: one server manages every profile on the machine. A profile switcher in the sidebar (visible whenever more than one profile exists) decides which profile the management pages read and write — Config, API Keys, Skills, MCP, Models, and the Chat tab all follow it. While a profile other than the dashboard's own is selected, an amber banner names the managed profile so the write target is never ambiguous.

The selection lives in the URL (`?profile=<name>`), so deep links like `http://127.0.0.1:9119/skills?profile=worker` land with the switcher preselected and survive refresh.

Launching the dashboard from a profile alias routes to the machine dashboard instead of starting a second server:

```bash
worker dashboard
# → already running: opens the browser at ?profile=worker
# → not running:     starts the machine dashboard with "worker" preselected
```

Pass `--isolated` to opt out and run a dedicated server scoped to that profile. The **Chat** tab follows the switcher too: a scoped chat spawns its PTY child with the selected profile's `HERMES_HOME`, so the conversation runs with that profile's model, skills, memory, and session history. What stays per-profile and is *not* absorbed by the switcher: gateway processes, each profile's session database, and cron schedulers (the Cron page already aggregates across profiles with its own filter).

## Prerequisites

The default `hermes-agent` install does not ship the HTTP stack or PTY helper — those are optional extras. The **web dashboard** needs FastAPI and Uvicorn (`web` extra). The **Chat** tab also needs `ptyprocess` to spawn the embedded TUI behind a pseudo-terminal (`pty` extra on POSIX). Install both with:

```bash
pip install 'hermes-agent[web,pty]'
```

The `web` extra pulls in FastAPI/Uvicorn; `pty` pulls in `ptyprocess` (POSIX) or `pywinpty` (native Windows — the embedded TUI itself still requires WSL). `pip install hermes-agent[all]` includes both. When you run `hermes dashboard` without the dependencies, it tells you what to install. If the frontend hasn't been built yet and `npm` is available, it builds automatically on first launch. The Chat tab is part of every launch — no extra flag required.

## Pages

The dashboard has 16 admin pages. This note tours each at the operator level; per-feature detail lives on each feature's own page (linked).

| Page | What it does | Deep dive |
|------|-------------|-----------|
| **Status** | Live overview: agent version, gateway status (PID, connected platforms), active-session count, the 20 most recent sessions. Auto-refreshes every 5s. | — |
| **Chat** | Embeds the full Hermes TUI (same as `hermes --tui`) in the browser via [xterm.js](https://xtermjs.org/) WebGL rendering. `/api/pty` opens a session-token-authenticated WebSocket; the server spawns `hermes --tui` behind a POSIX PTY; keystrokes and ANSI output stream both ways. A right-rail session switcher and **New chat** control sit beside the terminal. | [hermes_cli_interface](hermes_cli_interface.md) |
| **Config** | Form-based editor for `config.yaml` — all 150+ fields auto-discovered from `DEFAULT_CONFIG`, organized into tabbed categories (model, terminal, display, agent, delegation, memory, approvals, …). Save / Reset to defaults / Export / Import. | [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) |
| **API Keys** | Manage the `.env` file where API keys/credentials live, grouped by category (LLM providers, tool keys, messaging platforms, agent settings). Shows set/unset + redacted preview; advanced keys hidden behind a toggle. | — |
| **Sessions** | Browse/inspect all sessions (title, source icon, model, message + tool-call counts). FTS5 full-text search, stats bar, expand-to-history, rename, export, prune, delete. | [hermes_session_search_storage](hermes_session_search_storage.md) |
| **Logs** | View `agent` / `errors` / `gateway` log files with level/component/lines filters, color-coding, and live tailing. | — |
| **Analytics** | Usage + cost analytics from session history over 7/30/90 days: summary cards, daily token chart, per-day and per-model breakdown tables. | — |
| **Cron** | Create/manage scheduled cron jobs (name, prompt, cron expression, delivery target); job list with state badges; pause/resume, edit, trigger-now, delete. | [hermes_cron](hermes_cron_scheduling.md) |
| **Profiles** | Create/manage isolated profiles (own config, skills, sessions); profile cards, clone options, set-active, inline model/description/SOUL editors. | — |
| **Skills** | Browse/search/toggle installed skills and toolsets; category filter; "Browse hub" view installs from the skill hub with a live log. | [hermes_skills](hermes_skills_system.md) |
| **MCP** | Manage MCP servers (the same `mcp_servers` block `hermes mcp` reads): add HTTP/SSE or stdio servers, enable/disable, test, remove; install from the Nous-approved catalog. | [hermes_mcp](hermes_mcp_concept_config.md) |
| **Webhooks** | Manage dynamic webhook subscriptions (create with one-time HMAC secret, enable/disable, list, delete); platform must be enabled in messaging first. | — |
| **Pairing** | Approve/revoke messaging users without the CLI (full parity with `hermes pairing`); pending requests, approved users, clear-pending. | — |
| **Channels** | Connect Hermes to any messaging platform (Telegram, Discord, Slack, Matrix, …) — per-platform config forms, enable/disable, test, restart gateway. | — |
| **System** | Consolidated admin panel: host stats + update badge, Nous Portal status + Tool Gateway routing, skill curator, gateway lifecycle, memory provider, credential pool, operations (doctor/audit/backup/restore/dump/migrate), `/rollback` checkpoints, and consent-gated shell hooks. | [hermes_security_command_approval](hermes_security_command_approval.md) |

The Chat tab's PTY is reaped cleanly when the browser tab closes. To point [Hermes Desktop](hermes_dashboard_auth_remote.md) at a dashboard running on another machine, see the remote-backend section in the auth/remote note. A security warning on the System page reiterates: the dashboard reads/writes `.env` (API keys, secrets), binds to `127.0.0.1` by default, and has no authentication of its own on a loopback bind.

## `/reload` Slash Command

The dashboard adds a `/reload` slash command to the interactive CLI. After changing API keys via the web dashboard (or editing `.env` directly), use `/reload` in an active CLI session to pick up the changes without restarting:

```
You → /reload
  Reloaded .env (3 var(s) updated)
```

This re-reads `~/.hermes/.env` into the running process's environment — useful when you've added a new provider key via the dashboard and want to use it immediately.

## Themes & plugins (summary)

The dashboard ships with six (seven, including a large variant) built-in themes and can be extended with user-defined themes, plugin tabs, and backend API routes — all drop-in, no repo clone needed. **Switch themes live** from the header bar (palette icon); the selection persists to `config.yaml` under `dashboard.theme`. **Change the font independently** from the same picker (`dashboard.font`). Built-in themes include Hermes Teal (`default`), Hermes Teal Large (`default-large`), Midnight, Ember, Mono, Cyberpunk, and Rosé. The full schema (palette, typography, layout, layout variants, assets, `componentStyles`, `colorOverrides`, `customCSS`) and plugin authoring (manifest, SDK, shell slots, page-scoped slots, FastAPI routes) live in [hermes_dashboard_themes](hermes_dashboard_themes.md), [hermes_dashboard_plugins](hermes_dashboard_plugins.md), and [hermes_dashboard_extension_api](hermes_dashboard_extension_api.md).

**Source**: `inbox/hermes_agent_docs/user-guide/features/web-dashboard.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
**Last Updated**: 2026-06-19
**Status**: Active
