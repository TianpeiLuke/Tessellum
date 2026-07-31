---
tags:
  - resource
  - documentation
  - hermes_agent
  - desktop_app
  - deployment
keywords:
  - hermes desktop app
  - electron front end
  - same agent core
  - hermes desktop cli
  - chat-first window
  - building from source
topics:
  - Hermes Agent
  - Desktop App
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/desktop
access_control_group: ["general"]
---

# Hermes Desktop App

## Overview

The Hermes Desktop app is a native cross-platform (macOS, Windows, Linux) application built around the **same** agent you get from the CLI and the gateway — same config, same API keys, same sessions, same skills, same memory. It is not a separate product or a lightweight clone; it drives the same Hermes Agent core through a modern, purpose-built UI, so anything set up in the terminal is already here and anything done here shows up there. This note covers the local-app surface: launching it with `hermes desktop`, the chat-first window and management panes, updating, uninstalling, how it bootstraps, and building from source. (Pointing the app at a remote `hermes dashboard` backend is documented in [hermes_desktop_remote_backend](hermes_desktop_remote_backend.md).)

## Which Interface Is Which

Hermes has several front ends that all talk to the same agent and share state, so a session started in one resumes in another:

- **Desktop App** (this note) — a native application with a purpose-built UI for chat, configuration, and management.
- **CLI** (`hermes`) and **TUI** (`hermes --tui`) — terminal interfaces (the TUI backend is documented by SP02's `hermes_terminal_backends`).
- **Web Dashboard** (`hermes dashboard`) — a browser admin panel whose optional Chat tab embeds the TUI through a pseudo-terminal (owned by SP10's `hermes_web_dashboard`).

## Install

Follow the installation instructions for Hermes Desktop (installation base page owned by SP01). If you already have Hermes installed, simply run:

```bash
hermes desktop
```

That uses your current config, keys, sessions, and skills.

## What's in the App

The desktop app is organized as a chat-first window with a left sidebar for navigation. It is built to manage multiple simultaneous agent conversations, configure messaging providers, create artifacts, browse projects' folder structures, and work on multiple projects at once.

### Chat

The center of the app provides:

- **Streaming responses** with live tool activity and structured tool-call summaries as the agent works.
- **The same conversation history** as every other Hermes surface — sessions started here resume in the CLI/TUI and vice versa.
- **Drag-and-drop files** anywhere in the chat area to attach them to the next message.
- **A right-hand preview rail** — render web pages, files, and tool outputs side by side while chatting.
- **Composer history and queue editing** — press up/down arrows in an empty composer to recall and reuse previous prompts, and edit queued messages before they are sent.

#### Status bar

The bar along the bottom of the chat shows live session state and exposes quick controls without opening Settings, including a **per-session YOLO toggle** that flips YOLO on or off for just this session (matching the TUI). YOLO bypasses the dangerous-command approval prompts (see SP03b security).

#### Choosing a model

The model picker lives in the **composer**, just left of the microphone; click it to switch the model, reasoning effort, and fast mode from one dropdown.

- **The composer picker is sticky UI state and never touches your default.** It is remembered locally (per device) and **follows** across new chats and restarts instead of snapping back to the default — pick a model once and the next `Cmd/Ctrl+N` opens on it. With a live chat, switching models scopes the change to that current chat; either way the selection rides along when the session is created/switched and is never written to the profile default. (Switching profiles reseeds to that profile's own default.)
- **Set the default in Settings → Model.** That "main" model is your per-profile global default — what new chats, crons, subagents, and auxiliary tasks start from, and the only place that writes it. Each profile keeps its own default.
- **Per-model effort/fast presets.** Each model remembers its own reasoning effort and fast-mode choice in the desktop app, re-applied to the session whenever you pick that model. These presets are a desktop convenience and do not change crons or subagents.

### File browser

Explore and preview the working directory without leaving the app — useful for following along as the agent reads, writes, and edits files. Set the initial project directory with `hermes desktop --cwd <path>` (or the `HERMES_DESKTOP_CWD` environment variable).

### Voice

Talk to Hermes and hear it back, the same voice mode available elsewhere (voice mode owned by SP08). On macOS the OS prompts once for microphone access.

### Settings & onboarding

Manage providers, models, tools, and credentials from a real UI instead of editing YAML. First-run onboarding gets you to your first message in seconds; its panes cover providers/keys, model selection, toolset configuration, MCP servers, the gateway, and session management. Highlights:

- **Providers settings pane** — manage inference providers with an Accounts / API-keys UX for signing in and storing credentials per provider.
- **Every provider and model in the menus** — the GUI surfaces the full provider list and every model `hermes model` knows about, so you pick from the same catalog the CLI sees.
- **xAI Grok OAuth** — Grok is a first-class OAuth provider in the launcher; sign in through the browser flow like the other OAuth providers.
- **Tool-backend installs from the GUI** — run a tool backend's post-setup install steps directly from the app instead of dropping to a terminal.
- **Auxiliary-model warning** — if you switch the main model to a new provider while auxiliary tasks (titling, summarization, similar helpers) are still pinned to another, the app warns you so you do not unknowingly split work across two providers.

First-run onboarding uses a unified overlay design system, and **Choose provider later** lets you skip provider setup and get into the app first.

### Management panes

The app surfaces the broader Hermes management surface so you do not have to drop to a terminal:

- **Skills** — browse, install, and manage skills (skills detail owned by SP05).
- **Cron** — view and manage scheduled jobs (cron detail owned by SP06).
- **Profiles** — switch between Hermes profiles (isolated config/skills/sessions; profiles owned by SP04).
- **Messaging** — set up gateway channels.
- **Agents** and **Command Center** — orchestration surfaces for multi-agent work.

### Keyboard & navigation

- **Command palette** — press **Cmd+K** (Ctrl+K on Windows/Linux) to jump to actions and navigate from the keyboard.
- **Rebindable shortcuts** — a shortcuts panel in Settings remaps the app's keyboard shortcuts.
- **Custom zoom shortcuts** — zoom the interface in half-step increments for finer text-size control.
- **UI language switcher** — change the app's interface language in-app, including Simplified Chinese (zh-Hans).

### Sessions & profiles

- **Session-list overhaul** — a reworked session list with archiving and general session hygiene to keep the list manageable as it grows.
- **Search sessions by id** — find a specific session directly by its id.
- **Concurrent multi-profile sessions** — run sessions across multiple profiles at the same time, and reference a session in another profile with cross-profile `@session` links.

## Updating

The app checks for updates in the background and offers a one-click update when one is ready. The manual update process (owned by SP01) also works with the GUI.

## Uninstalling

Open **Settings → About → Danger zone** and pick how much to remove:

- **Uninstall Chat GUI only** — removes the desktop app and its data; the Hermes agent, your config, and your chats stay. (Same as `hermes uninstall --gui`.)
- **Uninstall GUI + agent, keep my data** — removes the app and the agent but keeps config, chats, and secrets for a future reinstall. (Same as `hermes uninstall`.)
- **Uninstall everything** — removes the app, the agent, and all user data. (Same as `hermes uninstall --full`.)

The app closes to finish the job (cleanup runs after it exits so it can remove the running app bundle and its own venv). The agent-removing options are hidden automatically when no local agent is installed (for example, a GUI-only "lite" client connected to a remote backend). You can do the same from the terminal — `hermes uninstall --gui` for the GUI alone, or `hermes uninstall` / `hermes uninstall --full` for the agent too. Running `hermes uninstall --gui` from a source checkout (a `hermes desktop` dev build) also removes the workspace `node_modules` and `apps/desktop/{dist,release}` build output, since those are GUI build artifacts (recoverable with `hermes desktop`).

## CLI Reference: `hermes desktop`

To launch via the CLI, run `hermes desktop`. By default it installs workspace Node dependencies, builds the current OS's unpacked Electron app, then launches that packaged artifact.

| Flag                 | Description                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------- |
| `--skip-build`       | Skip npm install/package and launch the existing unpacked app from `apps/desktop/release` |
| `--force-build`      | Force a full rebuild even if the content stamp matches                                    |
| `--build-only`       | Build the desktop app but do not launch it (used by `hermes update`)                      |
| `--source`           | Launch via `electron .` against `apps/desktop/dist` instead of the packaged app           |
| `--cwd PATH`         | Initial project directory for desktop chat sessions (sets `HERMES_DESKTOP_CWD`)           |
| `--hermes-root PATH` | Override the Hermes source root the app uses (sets `HERMES_DESKTOP_HERMES_ROOT`)          |
| `--ignore-existing`  | Force the app to ignore any `hermes` CLI already on `PATH` during backend resolution      |
| `--fake-boot`        | Enable deterministic boot delays for validating the startup UI                            |

## How It Works

The packaged app ships only the Electron shell. On first launch it installs the Hermes Agent runtime into `HERMES_HOME` (`~/.hermes`, or `%LOCALAPPDATA%\hermes` on Windows) — **the same layout a CLI install uses**, which is why the two are interchangeable. The React renderer talks to a `hermes dashboard` backend over the standard gateway APIs and reuses the agent rather than reimplementing it. Install, backend-resolution, and self-update logic live in the Electron main process.

## Building from Source

To hack on the app itself, install workspace deps from the repo root once, then run the dev server from `apps/desktop`:

```bash
npm install          # from repo root — links apps/desktop, web, apps/shared
cd apps/desktop
npm run dev          # Vite renderer + Electron, which boots the Python backend
```

Point the app at a specific checkout, or sandbox it from your real config:

```bash
HERMES_DESKTOP_HERMES_ROOT=/path/to/clone npm run dev
HERMES_HOME=/tmp/throwaway npm run dev
npm run dev:fake-boot   # exercise the startup overlay with deterministic delays
```

Build installers:

```bash
npm run dist:mac     # DMG + zip
npm run dist:win     # NSIS + MSI
npm run dist:linux   # AppImage + deb + rpm
npm run pack         # unpacked app under release/ (no installer)
```

macOS/Windows signing and notarization run automatically when the relevant credentials are present in the environment (`CSC_LINK` / `CSC_KEY_PASSWORD` / `APPLE_*` for macOS, `WIN_CSC_*` for Windows).

**Source**: `inbox/hermes_agent_docs/user-guide/desktop.md` · https://hermes-agent.nousresearch.com/docs/user-guide/desktop
**Last Updated**: 2026-06-19
**Status**: Active
