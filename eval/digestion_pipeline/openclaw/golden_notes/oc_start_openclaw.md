---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - personal_assistant
keywords:
  - openclaw personal assistant setup
  - two-phone whatsapp assistant
  - openclaw 5-minute quick start
  - agents workspace bootstrap files
  - heartbeats proactive mode
  - sessions and memory openclaw
  - media in and out
  - openclaw operations checklist
topics:
  - OpenClaw
  - Personal Assistant Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/openclaw
access_control_group: ["general"]
---

# OpenClaw — Personal Assistant Setup Walkthrough

## Overview

This note is the end-to-end procedure for running OpenClaw as a "personal assistant": a dedicated WhatsApp number that behaves like an always-on AI assistant, mirroring the `start/openclaw` source page. OpenClaw is a self-hosted gateway that connects Discord, Google Chat, iMessage, Matrix, Microsoft Teams, Signal, Slack, Telegram, WhatsApp, Zalo, and more to AI agents; this guide covers the recommended two-phone WhatsApp pattern.

It walks the full first-contact flow in source order: the safety-first cautions, prerequisites, the recommended two-phone topology, the 5-minute quick start (pair → gateway → minimal config), seeding the agent workspace (`AGENTS`) and bootstrap files, the config that turns it "into an assistant", sessions and memory, heartbeats (proactive mode), inbound/outbound media, and the operations checklist. The retired `start/quickstart` redirect is folded here as a References pointer.

## Safety first

You are putting an agent in a position to **run commands on your machine** (depending on your tool policy), **read/write files in your workspace**, and **send messages back out** via WhatsApp/Telegram/Discord/Mattermost and other bundled channels. Start conservative: always set `channels.whatsapp.allowFrom` (never run open-to-the-world on your personal Mac); use a dedicated WhatsApp number for the assistant; and note that heartbeats now default to every 30 minutes — disable them until you trust the setup by setting `agents.defaults.heartbeat.every: "0m"`.

## Prerequisites

- OpenClaw installed and onboarded — see Getting Started (`/start/getting-started`) if you have not done this yet.
- A second phone number (SIM/eSIM/prepaid) for the assistant.

## The two-phone setup (recommended)

The recommended topology (source mermaid diagram) routes your personal phone's WhatsApp (`+1-555-YOU`) by message to a second "assistant" phone whose WhatsApp (`+1-555-ASSIST`) is linked via QR to OpenClaw on your Mac, where the AI agent runs. If you link your personal WhatsApp to OpenClaw, every message to you becomes "agent input" — that is rarely what you want, which is why a dedicated second number is recommended.

## 5-minute quick start

The three quick-start steps are: (1) pair WhatsApp Web with `openclaw channels login` (shows a QR; scan it with the assistant phone); (2) start the Gateway and leave it running with `openclaw gateway --port 18789`; (3) put a minimal config in `~/.openclaw/openclaw.json`:

```json5
{
  gateway: { mode: "local" },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Now message the assistant number from your allowlisted phone. When onboarding finishes, OpenClaw auto-opens the dashboard and prints a clean (non-tokenized) link. If the dashboard prompts for auth, paste the configured shared secret into Control UI settings. Onboarding uses a token by default (`gateway.auth.token`), but password auth works too if you switched `gateway.auth.mode` to `password`. To reopen later, run `openclaw dashboard`.

## Give the agent a workspace (AGENTS)

OpenClaw reads operating instructions and "memory" from its workspace directory. By default it uses `~/.openclaw/workspace` as the agent workspace and will create it — plus starter `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, and `HEARTBEAT.md` — automatically on setup/first agent run. `BOOTSTRAP.md` is only created when the workspace is brand new (it should not come back after you delete it). `MEMORY.md` is optional (not auto-created); when present, it is loaded for normal sessions. Subagent sessions only inject `AGENTS.md` and `TOOLS.md`. Treat this folder like OpenClaw's memory and make it a git repo (ideally private) so your `AGENTS.md` and memory files are backed up; if git is installed, brand-new workspaces are auto-initialized.

Run the workspace bootstrap step with `openclaw setup`. The full workspace layout + backup guide is at `/concepts/agent-workspace`, and the memory workflow is at `/concepts/memory`. Optionally, choose a different workspace with `agents.defaults.workspace: "~/.openclaw/workspace"` (the field supports `~`). If you already ship your own workspace files from a repo, you can disable bootstrap file creation entirely with `agents.defaults.skipBootstrap: true`.

## The config that turns it into "an assistant"

OpenClaw defaults to a good assistant setup, but you will usually want to tune persona/instructions in `SOUL.md` (`/concepts/soul`), thinking defaults (if desired), and heartbeats (once you trust it). The worked example sets the primary model to `anthropic/claude-opus-4-6`, a 1800s `timeoutSeconds`, `thinkingDefault: "high"`, starts heartbeat at `"0m"`, defines a default agent `main` with group-chat `mentionPatterns`, restricts WhatsApp with `allowFrom` plus `requireMention: true` in groups, and uses a `per-sender` session scope with `/new` and `/reset` reset triggers and a daily reset:

```json5
{
  logging: { level: "info" },
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      workspace: "~/.openclaw/workspace",
      thinkingDefault: "high",
      timeoutSeconds: 1800,
      // Start with 0; enable later.
      heartbeat: { every: "0m" },
    },
    list: [
      {
        id: "main",
        default: true,
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw"],
        },
      },
    ],
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  session: {
    scope: "per-sender",
    resetTriggers: ["/new", "/reset"],
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 10080,
    },
  },
}
```

## Sessions and memory

Session files live at `~/.openclaw/agents/<agentId>/sessions/{{SessionId}}.jsonl`, and session metadata (token usage, last route, etc.) at `~/.openclaw/agents/<agentId>/sessions/sessions.json` (legacy: `~/.openclaw/sessions/sessions.json`). Sending `/new` or `/reset` starts a fresh session for that chat (configurable via `resetTriggers`); if sent alone, OpenClaw acknowledges the reset without invoking the model. Sending `/compact [instructions]` compacts the session context and reports the remaining context budget.

## Heartbeats (proactive mode)

By default, OpenClaw runs a heartbeat every 30 minutes with the prompt: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.` Set `agents.defaults.heartbeat.every: "0m"` to disable. The behavior rules are: if `HEARTBEAT.md` exists but is effectively empty (only blank lines, Markdown/HTML comments, Markdown headings like `# Heading`, fence markers, or empty checklist stubs), OpenClaw skips the run to save API calls; if the file is missing, the heartbeat still runs and the model decides what to do; if the agent replies `HEARTBEAT_OK` (optionally with short padding, bounded by `agents.defaults.heartbeat.ackMaxChars`), OpenClaw suppresses outbound delivery for that heartbeat; heartbeat delivery to DM-style `user:<id>` targets is allowed by default, but `agents.defaults.heartbeat.directPolicy: "block"` suppresses direct-target delivery while keeping runs active. Heartbeats run full agent turns, so shorter intervals burn more tokens:

```json5
{
  agents: {
    defaults: {
      heartbeat: { every: "30m" },
    },
  },
}
```

## Media in and out

Inbound attachments (images/audio/docs) can be surfaced to your command via templates: `{{MediaPath}}` (local temp file path), `{{MediaUrl}}` (pseudo-URL), and `{{Transcript}}` (if audio transcription is enabled). Outbound attachments from the agent use structured media fields on the message tool or reply payload, such as `media`, `mediaUrl`, `mediaUrls`, `path`, or `filePath`. Example message-tool arguments:

```json
{
  "message": "Here's the screenshot.",
  "mediaUrl": "https://example.com/screenshot.png"
}
```

OpenClaw sends structured media alongside the text. Legacy final assistant replies may still be normalized for compatibility, but tool output, browser output, streaming blocks, and message actions do not parse text as attachment commands. Local-path behavior follows the same file-read trust model as the agent: if `tools.fs.workspaceOnly` is `true`, outbound local media paths stay restricted to the OpenClaw temp root, the media cache, agent workspace paths, and sandbox-generated files; if `tools.fs.workspaceOnly` is `false`, outbound local media can use host-local files the agent is already allowed to read. Local paths can be absolute, workspace-relative, or home-relative with `~/`. Host-local sends still only allow media and safe document types (images, audio, video, PDF, Office documents, and validated text documents such as Markdown/MD, TXT, JSON, YAML, and YML); this is an extension of the existing host-read trust boundary, not a secret scanner — if the agent can read a host-local `secret.txt` or `config.json`, it can attach that file when the extension and content validation match. That means generated images/files outside the workspace can now send when your fs policy already allows those reads, while arbitrary host-local text extensions remain blocked; keep sensitive files outside the agent-readable filesystem, or keep `tools.fs.workspaceOnly=true` for stricter local-path sends.

## Operations checklist

```bash
openclaw status          # local status (creds, sessions, queued events)
openclaw status --all    # full diagnosis (read-only, pasteable)
openclaw status --deep   # asks the gateway for a live health probe with channel probes when supported
openclaw health --json   # gateway health snapshot (WS; default can return a fresh cached snapshot)
```

Logs live under `/tmp/openclaw/` (default: `openclaw-YYYY-MM-DD.log`). Next steps from the source page link out to WebChat (`/web/webchat`), the Gateway runbook (`/gateway`), Cron jobs (`/automation/cron-jobs`), the macOS/iOS/Android/Windows/Linux platform apps (`/platforms/*`), and Security (`/gateway/security`).

**Source**: OpenClaw documentation — `start/openclaw` (+ folded `start/quickstart` redirect) (mirror `inbox/openclaw_docs/start/openclaw.md`, `inbox/openclaw_docs/start/quickstart.md`)
**Last Updated**: 2026-06-22
**Status**: Active
