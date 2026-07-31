---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - cron
keywords:
  - daily briefing bot
  - cron job recipe
  - self-contained prompt
  - parallel research delegation
  - web search summarization
  - telegram discord delivery
topics:
  - Hermes Agent
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot
access_control_group: ["general"]
---

# Hermes Agent — Tutorial: Build a Daily Briefing Bot

## Overview

The Daily Briefing Bot tutorial is an **end-to-end recipe** that composes four already-existing Hermes primitives — web search, cron scheduling, delegation, and messaging delivery — into a hands-free morning automation, with **no code required**. The finished bot wakes up on a schedule (e.g. 8:00 AM), spins up a fresh agent session, researches the topics you care about, distills them into a concise briefing, and delivers it to Telegram, Discord, or a local file. It is the entry-point "starter" guide of the automation/bots series: it teaches the create-test-customize-manage arc once, so the same pattern can be reused for competitor monitoring, repo summaries, server health checks, or any task you can describe in a prompt.

The recipe assumes a working install with the gateway daemon running (the gateway is what executes cron jobs), a `FIRECRAWL_API_KEY` for the web-search tool, and — optionally — a configured messaging platform. The fastest path to the web-search + summarization + optional-TTS bundle is `hermes setup --portal` (one Nous Portal subscription). The deeper feature references this guide *uses* (the full cron schedule grammar, the delegation model, messaging-platform setup, memory) live in their own owning pages and are linked, not re-explained here.

## What We're Building

The flow runs entirely on a timer:

1. **8:00 AM** — the cron scheduler triggers the job.
2. **Hermes spins up** a fresh agent session seeded only with your prompt.
3. **Web search** pulls the latest news on your topics (Firecrawl-backed).
4. **Summarization** distills the results into a clean briefing format.
5. **Delivery** sends the briefing to Telegram / Discord / `local`.

The whole thing runs hands-free — you just read the briefing with your morning coffee.

## Prerequisites

Before starting:

- **Hermes Agent installed** (see the Installation guide).
- **Gateway running** — the gateway daemon handles cron execution. Install it as a persistent service for reliability:
  ```bash
  hermes gateway install        # Install as a user service
  sudo hermes gateway install --system   # Linux servers: boot-time system service
  # or
  hermes gateway                # Run in the foreground
  ```
- **Firecrawl API key** — set `FIRECRAWL_API_KEY` in your environment for web search.
- **Messaging configured** (optional but recommended) — Telegram or Discord with a home channel.

No messaging? You can still follow the tutorial with `deliver: "local"`: briefings are saved to `~/.hermes/cron/output/` and can be read anytime.

## Step 1: Test the Workflow Manually

Before automating anything, confirm the briefing works interactively. Start a chat session (`hermes`) and enter a self-contained prompt such as:

```
Search for the latest news about AI agents and open source LLMs.
Summarize the top 3 stories in a concise briefing format with links.
```

Hermes searches the web, reads through the results, and produces a formatted briefing (an emoji-headed title line, numbered stories with a short summary and source URL each, and a footer story/source count). Iterate on the prompt until you get output you love — add instructions like "use emoji headers" or "keep each summary under 2 sentences." Whatever you settle on becomes the cron prompt.

## Step 2: Create the Cron Job

There are two ways to schedule the tested briefing. **Before creating cron jobs, ensure Hermes has a default model and provider configured globally**; set explicit per-job model/provider overrides only if a job needs different values.

### Option A: Natural Language (in chat)

Just describe what you want in plain language — Hermes creates the job for you using the unified `cronjob` tool:

```
Every morning at 8am, search the web for the latest news about AI agents
and open source LLMs. Summarize the top 3 stories in a concise briefing
with links. Use a friendly, professional tone. Deliver to telegram.
```

### Option B: CLI Slash Command

Use the `/cron` command for more control. The first argument is the schedule expression, the second is the full prompt:

```
/cron add "0 8 * * *" "Search the web for the latest news about AI agents and open source LLMs. Find at least 5 recent articles from the past 24 hours. Summarize the top 3 most important stories in a concise daily briefing format. For each story include: a clear headline, a 2-sentence summary, and the source URL. Use a friendly, professional tone. Format with emoji bullet points and end with a total story count."
```

### The Golden Rule: Self-Contained Prompts

This is the **critical concept** of the whole guide. Cron jobs run in a **completely fresh session** — no memory of previous conversations, no context about what you "set up earlier." The prompt must contain **everything** the agent needs to do the job in one shot. A prompt like "Do my usual morning briefing." fails, because the fresh session has no "usual." A good prompt is explicit about *what to search*, *how many articles*, *what format*, and *what tone* — every parameter spelled out inline.

## Step 3: Customize the Briefing

Once the basic briefing works, the same `/cron add` shape supports richer variants:

- **Multi-topic briefings** — one prompt covers several areas (e.g. AI/ML, cryptocurrency, space exploration), instructing the agent to search recent news per topic and combine them into one briefing with section headers and emoji.
- **Delegation for parallel research** — for faster briefings, tell Hermes to delegate each topic to a sub-agent. Each sub-agent searches independently and in parallel, then the main agent combines all results into one polished briefing. (See the Delegation reference / the delegation-patterns guide for how this works.)
- **Weekday-only schedule** — target Monday–Friday with the cron expression `0 8 * * 1-5`.
- **Twice-daily briefings** — schedule a morning overview (`0 8 * * *`) and an evening recap (`0 18 * * *`) as two separate jobs.
- **Adding personal context with memory** — because cron jobs run in fresh sessions *without conversational memory*, you cannot rely on stored chat context; instead, **bake the persona directly into the prompt**. Describe who the briefing is *for* (role, interests, what to skip) — e.g. "You are creating a briefing for a senior ML engineer who cares about: PyTorch ecosystem, transformer architectures, open-weight models, and AI regulation in the EU. Skip product launches or funding rounds unless they involve open source." Including the audience persona dramatically improves relevance.

## Step 4: Manage Your Jobs

List, inspect, and remove jobs from chat or the terminal:

```bash
hermes cron list      # list all scheduled jobs (also `/cron list` in chat)
hermes cron status    # confirm the gateway scheduler is actually running
```

`hermes cron list` prints a table of each job's ID, Name, Schedule, Next Run, and Deliver target. To remove a job, use `/cron remove <id>` in chat or ask conversationally ("Remove my morning briefing cron job.") — Hermes uses `cronjob(action="list")` to find it and `cronjob(action="remove")` to delete it. If the gateway isn't running, jobs won't execute, so install it as a background service (`hermes gateway install`, or `sudo hermes gateway install --system` on Linux servers) for reliability.

## Going Further

You now have a working daily briefing bot. The same cron + fresh-session + delivery pattern generalizes to anything you can describe in a prompt — competitor monitoring, GitHub repo summaries, weather forecasts, portfolio tracking, server health checks, even a daily joke. Natural next steps: the full Scheduled Tasks (Cron) reference for schedule formats, repeat limits, and delivery options; the Delegation deep dive for parallel sub-agent workflows; the Messaging Platforms setup for Telegram/Discord delivery targets; Memory for persistent context; and the five reusable cron patterns in the companion automate-with-cron guide.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot
**Last Updated**: 2026-06-19
**Status**: Active
