---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - agents_workspace
keywords:
  - openclaw default agents.md
  - openclaw workspace setup
  - ~/.openclaw/workspace
  - agents.defaults.workspace
  - openclaw session start soul memory
  - openclaw core skills roster
  - mcporter peekaboo imsg wacli
  - openclaw browser verification
topics:
  - OpenClaw
  - Agent Workspace
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/AGENTS.default
access_control_group: ["general"]
---

# OpenClaw — Default Agent Workspace Setup and Core Skill Roster

## Overview

This note is the procedure for setting up the default OpenClaw agent workspace and enabling the bundled personal-assistant skill roster, mirroring the `reference/AGENTS.default` source page (the default `AGENTS.md` that ships with OpenClaw). It walks the first-run workspace creation, the safety defaults the agent always honors, the required session-start / Soul / memory rules, the recommended shared-spaces and backup practices, what the OpenClaw runtime does for the assistant, the full list of core skills enabled under Settings → Skills, and the usage notes for the `openclaw` CLI and browser-driven verification. OpenClaw uses a dedicated per-agent workspace directory whose `AGENTS.md`, `SOUL.md`, and memory files give a fresh-each-session agent its continuity; this page IS the optional personal-assistant variant of that `AGENTS.md`.

## First Run (recommended)

OpenClaw uses a dedicated workspace directory for the agent. The default is `~/.openclaw/workspace`, configurable via `agents.defaults.workspace`. The first-run procedure is:

1. Create the workspace (if it does not already exist):

```bash
mkdir -p ~/.openclaw/workspace
```

2. Copy the default workspace templates into the workspace:

```bash
cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md
```

3. Optional — if you want the personal-assistant skill roster, replace `AGENTS.md` with this file:

```bash
cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md
```

4. Optional — choose a different workspace by setting `agents.defaults.workspace` (supports `~`):

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

## Safety Defaults

The agent honors these defaults at all times: do not dump directories or secrets into chat; do not run destructive commands unless explicitly asked; before changing config or schedulers (for example crontab, systemd units, nginx configs, or shell rc files), inspect existing state first and preserve/merge by default; and do not send partial/streaming replies to external messaging surfaces — only final replies.

## Session Start (required)

At the start of every session, before responding, the agent must read `SOUL.md`, `USER.md`, and today + yesterday in `memory/`, and read `MEMORY.md` when present. These reads happen before the agent produces any response.

## Soul (required)

`SOUL.md` defines the agent's identity, tone, and boundaries, and must be kept current. If the agent changes `SOUL.md`, it tells the user. The agent is a fresh instance each session; continuity lives entirely in these workspace files (not in the model), so the Soul and memory files are what carry identity and history forward.

## Shared Spaces (recommended)

In group chats or public channels the agent is not the user's voice and must be careful. It must not share private data, contact info, or internal notes in shared spaces.

## Memory System (recommended)

The workspace memory layout is: a daily log at `memory/YYYY-MM-DD.md` (create `memory/` if needed) and long-term memory in `MEMORY.md` for durable facts, preferences, and decisions. Lowercase `memory.md` is legacy repair input only — do not keep both root files on purpose. On session start, read today + yesterday + `MEMORY.md` when present. Before writing memory files, read them first; write only concrete updates, never empty placeholders. Capture decisions, preferences, constraints, and open loops, and avoid secrets unless explicitly requested.

## Tools and Skills

Tools live in skills; follow each skill's `SKILL.md` when you need it. Keep environment-specific notes in `TOOLS.md` (the "Notes for Skills" section).

## Backup Tip (recommended)

If you treat this workspace as Clawd's "memory", make it a git repo (ideally private) so `AGENTS.md` and the memory files are backed up:

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md
git commit -m "Add Clawd workspace"
# Optional: add a private remote + push
```

## What OpenClaw Does

OpenClaw runs a WhatsApp gateway plus an embedded OpenClaw agent so the assistant can read/write chats, fetch context, and run skills via the host Mac. The macOS app manages permissions (screen recording, notifications, microphone) and exposes the `openclaw` CLI via its bundled binary. Direct chats collapse into the agent's `main` session by default; groups stay isolated as `agent:<agentId>:<channel>:group:<id>` (rooms/channels are `agent:<agentId>:<channel>:channel:<id>`); and heartbeats keep background tasks alive.

## Core Skills (enable in Settings → Skills)

The bundled personal-assistant skill roster, enabled in Settings → Skills:

- **mcporter** — Tool server runtime/CLI for managing external skill backends.
- **Peekaboo** — Fast macOS screenshots with optional AI vision analysis.
- **camsnap** — Capture frames, clips, or motion alerts from RTSP/ONVIF security cams.
- **oracle** — OpenAI-ready agent CLI with session replay and browser control.
- **eightctl** — Control your sleep, from the terminal.
- **imsg** — Send, read, stream iMessage & SMS.
- **wacli** — WhatsApp CLI: sync, search, send.
- **discord** — Discord actions: react, stickers, polls. Use `user:<id>` or `channel:<id>` targets (bare numeric ids are ambiguous).
- **gog** — Google Suite CLI: Gmail, Calendar, Drive, Contacts.
- **spotify-player** — Terminal Spotify client to search/queue/control playback.
- **sag** — ElevenLabs speech with mac-style say UX; streams to speakers by default.
- **Sonos CLI** — Control Sonos speakers (discover/status/playback/volume/grouping) from scripts.
- **blucli** — Play, group, and automate BluOS players from scripts.
- **OpenHue CLI** — Philips Hue lighting control for scenes and automations.
- **OpenAI Whisper** — Local speech-to-text for quick dictation and voicemail transcripts.
- **Gemini CLI** — Google Gemini models from the terminal for fast Q&A.
- **agent-tools** — Utility toolkit for automations and helper scripts.

## Usage Notes

Prefer the `openclaw` CLI for scripting; the mac app handles permissions. Run installs from the Skills tab — it hides the install button if a binary is already present. Keep heartbeats enabled so the assistant can schedule reminders, monitor inboxes, and trigger camera captures. The Canvas UI runs full-screen with native overlays, so avoid placing critical controls in the top-left/top-right/bottom edges; add explicit gutters in the layout and do not rely on safe-area insets. For browser-driven verification, use `openclaw browser` (tabs/status/screenshot) with the OpenClaw-managed Chrome profile. For DOM inspection, use `openclaw browser eval|query|dom|snapshot` (and `--json`/`--out` when you need machine output). For interactions, use `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (click/type require snapshot refs; use `evaluate` for CSS selectors).

**Source**: OpenClaw documentation — `reference/AGENTS.default` (mirror `inbox/openclaw_docs/reference/AGENTS.default.md`)
**Last Updated**: 2026-06-22
**Status**: Active
