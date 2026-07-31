---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - menu_bar
keywords:
  - openclaw menu bar status
  - iconstate enum swift
  - activitykind glyph mapping
  - control-channel agent event ingestion
  - main session priority
  - context submenu sessions
  - icon override debug
  - tool result ttl grace flicker
topics:
  - OpenClaw
  - macOS App Menu Bar
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/platforms/mac/menu-bar
access_control_group: ["general"]
---

# OpenClaw — macOS Menu Bar Status State Model

## Overview

This note models the **menu-bar status logic** of the OpenClaw macOS app: what work/health/context information is surfaced, how a single icon and status row are chosen from multiple concurrent sessions, the `IconState` enum and its `ActivityKind`→glyph/visual mappings, the Context submenu, the status-row text format, how control-channel `agent` events are ingested into this state, the debug icon-override, and the testing checklist. It mirrors the `platforms/mac/menu-bar` source page (mirror `inbox/openclaw_docs/platforms/mac/menu-bar.md`). The icon's own animation/critter rendering is modeled by the sibling [oc_platforms_mac_icon](oc_platforms_mac_icon.md); this note models the *status-selection and event-ingestion* state that drives it.

## What Is Shown

The menu bar surfaces the **current agent work state** in two places: the menu-bar icon and the **first status row** of the menu. Health status is **hidden while work is active** and returns once all sessions are idle. The root menu does not expand recent sessions directly; instead a root **"Context" submenu** contains them. The **"Nodes"** block in the root menu lists **devices only** (paired nodes via `node.list`), not client/presence entries. A root **"Usage"** section appears below Context when provider usage snapshots are available, followed by usage-cost details when available.

## State Model

The state model is driven by per-session events and a priority rule that selects exactly one session to surface at a time:

- **Sessions** — events arrive with `runId` (per-run) plus `sessionKey` in the payload. The "main" session is the key `main`; if `main` is absent, the model falls back to the **most recently updated session**.
- **Priority** — **main always wins**. If main is active, its state is shown immediately. If main is idle, the **most recently active non-main session** is shown. The model does **not flip-flop mid-activity**; it only switches when the current session goes idle or main becomes active.
- **Activity kinds** — each surfaced session has one of two activity kinds:
  - `job` — high-level command execution, with `state: started|streaming|done|error`.
  - `tool` — a tool invocation, with `phase: start|result`, a `toolName`, and `meta/args`.

## IconState Enum (Swift)

The icon state is a Swift enum with four cases; `workingMain`, `workingOther`, and `overridden` each carry an associated `ActivityKind`:

- `idle`
- `workingMain(ActivityKind)`
- `workingOther(ActivityKind)`
- `overridden(ActivityKind)` — the debug override case.

### ActivityKind → glyph

Each `ActivityKind` maps to a glyph used to badge the icon (and label the status row):

- `exec` → 💻
- `read` → 📄
- `write` → ✍️
- `edit` → 📝
- `attach` → 📎
- default → 🛠️

### Visual mapping

Each `IconState` case maps to a distinct visual treatment of the menu-bar critter:

- `idle` — normal critter.
- `workingMain` — badge with glyph, full tint, leg "working" animation.
- `workingOther` — badge with glyph, muted tint, no scurry.
- `overridden` — uses the chosen glyph/tint regardless of actual activity.

## Context Submenu

Recent sessions are presented in a submenu rather than the root menu, keeping the root glanceable:

- The root menu shows one **"Context"** row with a session count/status that opens a submenu.
- The Context submenu **header** shows the active session count for the **last 24 hours**.
- Each session row keeps its **token bar, age, preview, thinking/verbose, reset, compact, and delete** actions.
- **Loading, disconnected, and session-load error** messages appear inside the Context submenu.
- Provider **usage and usage-cost** details stay **root-level below Context** so they remain glanceable without opening the submenu.

## Status Row Text (Menu)

The first status row of the menu renders differently depending on whether work is active:

- **While work is active**: `<Session role> · <activity label>`.
  - Examples: `Main · exec: pnpm test`, `Other · read: apps/macos/Sources/OpenClaw/AppState.swift`.
- **When idle**: falls back to the **health summary**.

## Event Ingestion

The state model is fed entirely by control-channel events; the menu parses these into the activity kinds above:

- **Source** — control-channel `agent` events, handled by `ControlChannel.handleAgentEvent`.
- **Parsed fields**:
  - `stream: "job"` with `data.state` for start/stop.
  - `stream: "tool"` with `data.phase`, `name`, and optional `meta`/`args`.
- **Labels** — derived per kind:
  - `exec` — first line of `args.command`.
  - `read`/`write` — shortened path.
  - `edit` — path plus inferred change kind from `meta`/diff counts.
  - fallback — the tool name.

## Debug Override

A debug control lets a developer force the icon into a chosen state regardless of real activity, via **Settings ▸ Debug ▸ "Icon override"** picker:

- `System (auto)` — the default.
- `Working: main` — per tool kind.
- `Working: other` — per tool kind.
- `Idle`

The selection is stored via `@AppStorage("iconOverride")` and mapped to `IconState.overridden`.

## Testing Checklist

The page enumerates the behaviors to verify the state model end-to-end:

- **Trigger main session job** — verify the icon switches immediately and the status row shows the main label.
- **Trigger non-main session job while main idle** — icon/status shows non-main and stays stable until it finishes.
- **Start main while other active** — icon flips to main instantly.
- **Rapid tool bursts** — ensure the badge does not flicker (TTL grace on tool results).
- **Health row reappears** once all sessions idle.

**Source**: OpenClaw documentation — `platforms/mac/menu-bar` (mirror `inbox/openclaw_docs/platforms/mac/menu-bar.md`)
**Last Updated**: 2026-06-22
**Status**: Active
