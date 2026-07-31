---
tags:
  - resource
  - documentation
  - claude_code
  - adoption
  - launch_communications
keywords:
  - launch communications
  - rollout announcement
  - pre-send checklist
  - executive sponsor variant
  - pilot group variant
  - champion recruitment dm
  - org-wide adoption
  - install snippet
topics:
  - Claude Code
  - Adoption
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/communications-kit
access_control_group: ["general"]
---

# Claude Code — Launch Communications

## Overview

This note is the org-wide **rollout-comms playbook** from the communications kit: the copy an administrator or engineering lead sends to introduce Claude Code to a team. It pairs a **pre-send checklist** (six items, each closing a gap that would otherwise become a launch-day support thread) with **one announcement in two formats** plus **three template variants** — an executive-sponsor send, a pilot-group send, and a post-launch champion-recruitment DM. The argument running through all of them is the same: lead with what Claude Code *is* (an agent that edits files, runs commands, and asks permission — not autocomplete and not a chat window), give a two-minute install path, hand the reader one concrete task on their own repo, and answer "where does my code go?" before anyone has to ask.

Everything in the kit is **draft copy, not finished copy** — the source instructs you to rewrite each message in your organization's voice, swap the example tasks for real bugs and modules from your own codebase, and replace the `[bracketed placeholders]` before sending. The announcements that drive adoption are the ones that read like someone at your company wrote them.

## Before you send (pre-send checklist)

Work through this checklist before the announcement goes out. Each item closes a gap that otherwise turns into a launch-day support thread:

| Item | Why it matters |
|------|----------------|
| `#claude-code` channel created and linked in the message | Gives questions one place to land |
| Install command tested on at least one machine in your environment | Catches proxy or firewall issues before everyone hits them at once |
| Security and data-handling link ready ([Data usage](https://code.claude.com/docs/en/data-usage) or your internal equivalent) | "Where does my code go?" will be the first reply |
| One concrete first task chosen — a real bug or file in your codebase | Generic examples don't convert; "fix the flaky test in `auth_test.go`" does |
| A named owner for the channel for the first 48 hours | Unanswered launch-day questions kill momentum |
| A C-suite sponsor lined up to send or co-sign the announcement | Exec-sent launches consistently see higher first-week adoption than admin-sent ones |

## The announcement

The standard org-wide rollout message follows a fixed structure: it covers **what Claude Code is**, gives a **two-minute install path**, hands readers **one concrete task to try**, and answers **"where does my code go?"** before anyone has to ask. It ships in two formats (Email and Slack/Teams) carrying the same content at different lengths. The install snippet at the center of both is:

```text theme={null}
curl -fsSL https://claude.ai/install.sh | bash
cd <your-repo>
claude
```

The email version opens with what the tool is ("an AI coding agent that runs in your terminal, reads your actual codebase, and works through real tasks end to end... It is not autocomplete and it is not a chat window. It edits files, runs your commands, and asks permission before anything risky"), then walks the reader from install → run `/init` once (Claude reads the project and writes a `CLAUDE.md` so they stop re-explaining the basics) → try one of three sample tasks ("the test in [file] is flaky," "walk me through how [module] handles [X]," "look at my working diff and tell me what's risky"). It closes with the **"where your code goes"** paragraph (runs in your terminal, talks directly to Anthropic's API with no third-party servers, asks before editing files or running commands, and under the Enterprise agreement Anthropic does not use your code or prompts to train its models), the `#claude-code` channel with its named owner, and a P.S. pointing to the VS Code extension and JetBrains plugin. The Slack/Teams version compresses the same four beats into a scannable post with the install one-liner inline, the security note, a links block (Quickstart · VS Code · the free one-hour course), and "Questions → this thread."

## Executive sponsor variant

Send this from your sponsoring executive (CTO, CIO, or SVP Engineering) under their name and from their account. Per the source, launches that go out under an exec's name consistently see higher open rates and faster first-week activation than the same message from an admin or tooling team — it signals a company priority rather than an optional experiment.

This version is deliberately stripped to **one ask**: install it and run it on one real task. The exec's job is to make the ask land; the standard announcement and `#claude-code` handle the *how*. The email opens "We have turned on Claude Code for all of engineering... the early results from teams already using it are strong enough that I want everyone on it this week," asks for ten minutes (the same install snippet), and hands the reader one real task ("the bug you have been putting off, or 'walk me through how [module] works'"), then points to the channel owner. The Slack/Teams variant carries the identical message in two short lines.

## Pilot group variant

Use this for a **phased rollout**, sent to the pilot cohort only. The frame is explicitly truth-seeking: "We picked this group because you will put it on real problems and tell us the truth about it." The ask is to use it on at least one real task that week and then drop a note in `#claude-code-pilot` covering "what worked, what was annoying, and what surprised you" — feedback that decides how the tool rolls out to everyone else. The body reuses the "Get running in two minutes" install block from the standard announcement.

The pilot variant adds **one extra thing for pilots**, verbatim from source:

```text theme={null}
One extra thing for pilots: on your first multi-file change, press Shift+Tab
until you see "plan". Claude will lay out exactly what it intends to do
before it touches a file. It is the fastest way to calibrate how much to
trust it.
```

This is the graduated-trust calibration step — plan mode as the fastest way to learn how much to trust the agent on a real change.

## Champion recruitment DM

After launch, DM the two or three people who are most active in `#claude-code` — the source observes that their posts "are doing more for adoption than my announcement did." The recruitment ask is deliberately **low lift**: mostly keep posting what they are already posting, plus first crack at new features and a direct line to the Anthropic team. The DM offers to share "a short playbook if you're in" — that playbook is the champion role described in the companion note ([Champion playbook](cc_champion_playbook.md)). This closes the loop between the two adoption kits: the comms kit recruits champions, and the champion kit is the playbook handed to them.

**Source**: https://code.claude.com/docs/en/communications-kit
**Last Updated**: 2026-06-13
**Status**: Active
