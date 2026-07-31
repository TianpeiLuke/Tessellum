---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - faq
keywords:
  - openclaw faq first 60 seconds
  - what is openclaw
  - openclaw value proposition
  - local-first control plane
  - gateway control plane
  - openclaw status doctor triage
  - openclaw vs claude code
  - model-agnostic multi-agent routing
topics:
  - OpenClaw
  - Help & Support FAQ
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — FAQ: First-Line Triage and Product Framing

## Overview

This note covers the opening of the OpenClaw general FAQ (`help/faq`): the **"First 60 seconds if something is broken"** triage checklist and the **"What is OpenClaw?"** product-framing answers. It explains the first thing to run when a setup misbehaves and the conceptual answer to what OpenClaw *is* — a local-first, model-agnostic personal assistant whose **Gateway** is the always-on control plane and whose assistant is the product. The remaining FAQ sections (skills/automation, config/env, storage/memory, gateway/remote, sessions/logging, security/access) are split into sibling `oc_help_faq_*` notes, and the FAQ's two pointer H2s route to the first-run and models FAQ notes; this note holds only the triage entry and the value-proposition framing.

## First 60 Seconds If Something Is Broken

When a setup misbehaves, the FAQ's first-line triage is an ordered checklist of read-only diagnostic commands — run top-down until one surfaces the problem. The page sequences them as a fast-to-deep escalation:

1. **Quick status (first check)** — `openclaw status` gives a fast local summary: OS + update state, gateway/service reachability, agents/sessions, and provider config + runtime issues (the latter only when the gateway is reachable).
2. **Pasteable report (safe to share)** — `openclaw status --all` produces a read-only diagnosis with a log tail and tokens redacted, so it is safe to paste into a support thread.
3. **Daemon + port state** — `openclaw gateway status` shows supervisor runtime vs RPC reachability, the probe target URL, and which config the service likely used.
4. **Deep probes** — `openclaw status --deep` runs a live gateway health probe, including channel probes when supported (this requires a reachable gateway).
5. **Tail the latest log** — `openclaw logs --follow`; if RPC is down, fall back to tailing the newest file log directly (file logs are separate from service logs).
6. **Run the doctor (repairs)** — `openclaw doctor` repairs/migrates config/state and runs health checks.
7. **Gateway snapshot** — `openclaw health --json` (or `openclaw health --verbose`, which additionally shows the target URL + config path on errors) asks the running gateway for a full snapshot over WS-only.

The verbatim triage commands and their fallbacks are:

```bash
openclaw status
openclaw status --all
openclaw gateway status
openclaw status --deep
openclaw logs --follow
tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)"
openclaw doctor
openclaw health --json
openclaw health --verbose   # shows the target URL + config path on errors
```

The page cross-links each step to its own deep doc (`/gateway/troubleshooting`, `/gateway/health`, `/logging`, `/gateway/doctor`), which this digest series links to their owning sub-plans rather than re-digesting here.

## What Is OpenClaw?

**One paragraph.** OpenClaw is a personal AI assistant you run on your own devices. It replies on the messaging surfaces you already use — WhatsApp, Telegram, Slack, Mattermost, Discord, Google Chat, Signal, iMessage, WebChat, and bundled channel plugins such as QQ Bot — and can also do voice plus a live **Canvas** on supported platforms. The **Gateway** is the always-on control plane; the assistant is the product.

**Value proposition.** OpenClaw is not "just a Claude wrapper." It is a **local-first control plane** that lets you run a capable assistant on **your own hardware**, reachable from the chat apps you already use, with stateful sessions, memory, and tools — without handing control of your workflows to a hosted SaaS. The page lists the highlights as:

- **Your devices, your data** — run the Gateway wherever you want (Mac, Linux, VPS) and keep the workspace + session history local.
- **Real channels, not a web sandbox** — WhatsApp/Telegram/Slack/Discord/Signal/iMessage/etc, plus mobile voice and Canvas on supported platforms.
- **Model-agnostic** — use Anthropic, OpenAI, MiniMax, OpenRouter, etc., with per-agent routing and failover.
- **Local-only option** — run local models so **all data can stay on your device** if you want.
- **Multi-agent routing** — separate agents per channel, account, or task, each with its own workspace and defaults.
- **Open source and hackable** — inspect, extend, and self-host without vendor lock-in.

**First things to do.** The FAQ suggests good first projects for a freshly set-up instance: build a website (WordPress, Shopify, or a simple static site), prototype a mobile app (outline, screens, API plan), organize files and folders (cleanup, naming, tagging), or connect Gmail and automate summaries or follow-ups. It can handle large tasks, but works best when they are split into phases and use sub-agents for parallel work.

**Everyday use cases.** The page frames the top five everyday wins as: **personal briefings** (summaries of inbox, calendar, and news); **research and drafting** (quick research, summaries, first drafts for emails or docs); **reminders and follow-ups** (cron- or heartbeat-driven nudges and checklists); **browser automation** (filling forms, collecting data, repeating web tasks); and **cross-device coordination** (send a task from your phone, let the Gateway run it on a server, and get the result back in chat). For SaaS lead-gen/outreach/ads/blogs the answer is "yes for research, qualification, and drafting," with the recurring guidance to keep a human in the loop — let OpenClaw draft and you approve.

**Advantages vs Claude Code.** OpenClaw is positioned as a **personal assistant and coordination layer, not an IDE replacement**. The page advises using Claude Code or Codex for the fastest direct coding loop inside a repo, and using OpenClaw when you want durable memory, cross-device access, and tool orchestration. Its stated advantages are: **persistent memory + workspace** across sessions; **multi-platform access** (WhatsApp, Telegram, TUI, WebChat); **tool orchestration** (browser, files, scheduling, hooks); an **always-on Gateway** (run on a VPS, interact from anywhere); and **Nodes** for local browser/screen/camera/exec.

**Source**: OpenClaw documentation — `help/faq` (First 60 seconds, What is OpenClaw?) (mirror `inbox/openclaw_docs/help/faq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
