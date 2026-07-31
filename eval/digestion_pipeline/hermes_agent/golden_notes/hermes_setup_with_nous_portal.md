---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - nous_portal
keywords:
  - hermes setup --portal
  - Nous Portal subscription
  - Tool Gateway routing
  - hermes portal info
  - OAuth refresh token
  - single-token provider
topics:
  - Hermes Agent
  - Providers & Setup
  - Nous Portal
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/run-hermes-with-nous-portal
access_control_group: ["general"]
---

# Run Hermes Agent with Nous Portal

## Overview

This is the **end-to-end task script** for running Hermes Agent on a [Nous Portal](https://portal.nousresearch.com) subscription — from signing up to verifying that the model and every tool route correctly. The defining idea is **one credential replaces five**: a single OAuth refresh token gives you a frontier inference model plus the four Tool-Gateway tools (web search/extract, image generation, text-to-speech, browser automation), so you do **not** need an OpenAI key, an Anthropic key, a Firecrawl account, a FAL account, a Browser Use account, or any other per-vendor credential. The entire setup is the one-shot `hermes setup --portal`, which opens a browser for OAuth, stores the refresh token at `~/.hermes/auth.json`, sets `model.provider: nous`, picks a default agentic model, and turns on the Tool Gateway — about five minutes start to finish.

This page is the *procedure*; the conceptual overview of what the Portal is and what the subscription includes lives on the Nous Portal integration page (link-out), and the gateway routing internals live on the Tool Gateway page. The walkthrough below mirrors the source's eight numbered steps plus profiles, troubleshooting, and the "in plain numbers" comparison.

## Prerequisites

- Hermes Agent installed (Quickstart).
- A web browser on the machine you're setting up — **or** SSH port forwarding (see [OAuth over SSH](hermes_oauth_over_ssh.md) for remote/headless hosts).
- About 5 minutes.

You do **not** need per-vendor keys (OpenAI, Anthropic, Firecrawl, FAL, Browser Use). Replacing those is the whole point of the subscription.

## 1–2. Subscribe and Run the One-Shot Setup

Sign up and pick a plan at `portal.nousresearch.com/manage-subscription` (skip if already subscribed), then run the single setup command:

```bash
hermes setup --portal
```

This one command does five things: (1) opens your browser to portal.nousresearch.com for OAuth login, (2) stores the refresh token at `~/.hermes/auth.json`, (3) sets `model.provider: nous` in `~/.hermes/config.yaml`, (4) picks a default agentic model (`anthropic/claude-sonnet-4.6` or similar), and (5) turns on the Tool Gateway for web search, image generation, TTS, and browser automation. When it finishes you're back at the terminal ready to chat.

**SSH'd into a server?** OAuth needs a browser, but the loopback callback runs on the machine where Hermes is running. Two options:

```bash
# Option A: SSH port forwarding (preferred)
ssh -N -L 8642:127.0.0.1:8642 user@remote-host    # in a local terminal
hermes setup --portal                              # on the remote, open the printed URL in your local browser

# Option B: manual paste (for Cloud Shell, Codespaces, EC2 Instance Connect)
hermes auth add nous --type oauth --manual-paste
# Then re-run `hermes setup --portal` to wire the provider + gateway
```

See [OAuth over SSH](hermes_oauth_over_ssh.md) for ProxyJump chains, mosh/tmux, and ControlMaster gotchas.

## 3–4. Verify It Worked, Then Run Your First Conversation

Confirm routing with `hermes portal info`:

```
$ hermes portal info

  Nous Portal
  ───────────
  Auth:    ✓ logged in
  Portal:  https://portal.nousresearch.com
  Model:   ✓ using Nous as inference provider

  Tool Gateway
  ────────────
  Web search & extract  via Nous Portal
  Image generation      via Nous Portal
  Text-to-speech        via Nous Portal
  Browser automation    via Nous Portal
```

If any line shows something other than "via Nous Portal", or the auth line says "not logged in", jump to Troubleshooting. Then start `hermes chat` and try a prompt that exercises both the model and the gateway (e.g. *"search the web for 'Hermes Agent release notes' and summarize the top 3 hits"*). Hermes calls `web_search` (Firecrawl-backed, through the gateway) and responds with a summary — if that runs sensibly, the Portal is wired end to end.

## 5. Pick the Model You Actually Want

`hermes setup --portal` lets you pick a model during setup, but the point of the subscription is access to the full catalog. Switch any time mid-session with `/model`, or run `/model` with no argument to pop the picker:

```bash
/model anthropic/claude-sonnet-4.6     # best general-purpose agentic
/model openai/gpt-5.4                  # strong reasoning + tool calling
/model google/gemini-2.5-pro           # huge context window
/model deepseek/deepseek-v3.2          # cost-effective coder
hermes config set model.default anthropic/claude-sonnet-4.6   # change the default permanently
```

**Don't pick Hermes-4 for agent work.** Hermes-4-70B and Hermes-4-405B are available on the Portal at deep discounts, but they are **chat/reasoning models, not tool-call-tuned** — they struggle with multi-step agent loops. Use them via Nous Chat for conversation/research, or through the subscription proxy from non-agent tools; for Hermes Agent itself, stick to the frontier agentic models above. The Portal's own info page carries the same warning — it is official Nous guidance, not just a Hermes-side opinion.

## 6–8. Customize Gateway Routing, Voice, and Cron

The gateway is **opt-in per tool**, not all-or-nothing. If you already have, say, a Browserbase account, you can keep it for browser automation while routing web search, image generation, and TTS through Nous:

```bash
hermes tools
# → Web search       → "Nous Subscription"     (recommended)
# → Image generation → "Nous Subscription"     (recommended)
# → Browser          → "Browserbase"           (your existing key)
# → TTS              → "Nous Subscription"     (recommended)
```

These rows appear in `hermes tools` even before you've logged into Nous Portal — picking "Nous Subscription" without an active session makes Hermes run the Portal login inline (without changing your inference provider or other tools). Verify the mix with `hermes portal tools`, which shows per-tool routing (`via Nous Portal` for subscription-routed tools, the partner name like `browserbase`/`firecrawl` for your own keys).

Because the gateway includes OpenAI TTS, **voice mode** works without a separate OpenAI key (`hermes setup voice` → pick "Nous Subscription" for TTS, then a speech-to-text backend such as the free local faster-whisper). And the subscription works for **cron jobs and batch processing** the same way it works for interactive chat — the OAuth refresh token is reused automatically, no extra setup; scheduled jobs simply bill against your subscription:

```bash
hermes cron create "every day at 9am" \
  "Search the web for top AI news and summarize the 5 most important stories" \
  --name "Daily AI news"
```

## Profiles and Multi-User Setups

If you use Hermes profiles (e.g. a separate config per project), the Portal refresh token is automatically shared across all profiles via a **shared token store** — sign in once on any profile and the rest pick it up. For team setups where multiple humans share a machine, each human has their own Portal account, so each home directory holds its own `~/.hermes/auth.json` with **no token sharing across users**. That is the right security boundary.

## Troubleshooting

The failure modes are almost all **provider-routing drift** — the OAuth succeeded but `model.provider` or per-tool config points elsewhere:

- **`hermes portal info` shows "not logged in"** after setup → the OAuth flow didn't complete; re-run `hermes portal`. If the browser doesn't open / the callback fails, you're on a remote/headless host — use the SSH port-forward or `--manual-paste` workarounds.
- **"Model: currently openrouter" (or another provider)** instead of "using Nous" → local config drifted; fix with `hermes config set model.provider nous` (or interactively via `hermes model` → pick Nous Portal), then re-verify.
- **Gateway tools show partner names instead of "via Nous Portal"** → per-tool config is overriding the gateway; run `hermes tools` and pick "Nous Subscription" for any tool you want gateway-routed (leave intentional mixes alone).
- **"Re-authentication required" mid-session** → the refresh token was invalidated (password change, manual revoke, expiry) and is now **quarantined locally** so Hermes won't replay it endlessly; just `hermes auth add nous` and the quarantine clears on successful re-login.
- **A model isn't in the `/model` picker** → the Portal catalog mirrors OpenRouter's list (300+); type the OpenRouter-style slug directly (e.g. `/model anthropic/claude-opus-4.6`), or open a GitHub issue if genuinely unavailable.
- **Billing not appearing** → `hermes portal info` tells you whether you're actually routing through the Portal; common causes are a non-`nous` `model.provider`, an OAuth refresh failure that fell back to another provider, or the wrong profile (`hermes profile current`).
- **Revoke and start clean** → `hermes auth remove nous` wipes the local refresh token; then re-run setup or remove the subscription in the Portal web UI.

## What This Gets You

The subscription collapses many per-vendor credentials and dashboards into one OAuth token and one invoice:

| Without Portal | With Portal |
|----------------|-------------|
| 1× OpenRouter / Anthropic / OpenAI key in `.env` | 1× OAuth refresh token, no `.env` keys |
| 1× Firecrawl key for web | Web routed through gateway |
| 1× FAL key for image gen | Image gen routed through gateway |
| 1× Browser Use / Browserbase key for browser | Browser routed through gateway |
| 1× OpenAI key for TTS / voice mode | TTS routed through gateway |
| 5 separate dashboards, top-ups, invoices | 1 subscription, 1 invoice |
| Cross-machine: replicate all 5 keys | Cross-machine: re-OAuth once |

If you're using more than two of those backends anyway, the subscription pays for itself.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/run-hermes-with-nous-portal
**Last Updated**: 2026-06-19
**Status**: Active
