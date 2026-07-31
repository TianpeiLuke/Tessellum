---
tags:
  - resource
  - documentation
  - claude_code
  - automation
  - routines
keywords:
  - routine
  - saved claude code configuration
  - schedule trigger
  - api trigger
  - github trigger
  - anthropic-managed cloud infrastructure
  - daily run cap
  - one-off run
  - example use cases
topics:
  - Claude Code
  - Automation & Scheduling
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/routines
access_control_group: ["general"]
---

# Claude Code — Routines Overview

## Overview

A **routine** is a saved Claude Code configuration — a prompt, one or more repositories, and a set of [connectors](https://code.claude.com/docs/en/mcp) — packaged once and run automatically. Routines execute on **Anthropic-managed cloud infrastructure**, so they keep working when your laptop is closed. Routines are in research preview; behavior, limits, and the API surface may change.

Each routine can have one or more **triggers** attached, and a single routine can combine trigger types. For example, a PR review routine can run nightly, trigger from a deploy script, and also react to every new PR. This note covers what a routine is, the trigger types, the example workloads they suit, and how usage limits apply; the dedicated procedure notes cover [creating a routine](cc_create_routine.md), [configuring triggers](cc_routine_triggers.md), and [managing routines](cc_manage_routines.md).

## What a routine is

A routine packages a Claude Code session to run unattended. The three trigger types are:

- **Scheduled** — run on a recurring cadence like hourly, nightly, or weekly, or once at a specific future time.
- **API** — trigger on demand by sending an HTTP POST to a per-routine endpoint with a bearer token.
- **GitHub** — run automatically in response to repository events such as pull requests or releases.

Routines are available on **Pro, Max, Team, and Enterprise** plans with [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) enabled. Create and manage them at `claude.ai/code/routines`, or from the CLI with `/schedule`. Team and Enterprise admins can disable routines for all members with the **Routines** toggle at `claude.ai/admin-settings/claude-code`; when disabled, existing routines stop running and members cannot create new ones.

Routines belong to your individual claude.ai account. They are not shared with teammates and count against your account's daily run allowance. Anything a routine does through your connected GitHub identity or connectors appears as you: commits and pull requests carry your GitHub user, and Slack messages, Linear tickets, or other connector actions use your linked accounts.

## Example use cases

Each example pairs a trigger type with the kind of work routines are suited to: unattended, repeatable, and tied to a clear outcome.

- **Backlog maintenance** — a schedule trigger runs every weeknight against your issue tracker via a connector, applies labels, assigns owners based on the area of code referenced, and posts a summary to Slack.
- **Alert triage** — your monitoring tool calls the routine's API endpoint when an error threshold is crossed (passing the alert body as `text`); the routine pulls the stack trace, correlates it with recent commits, and opens a draft pull request with a proposed fix.
- **Bespoke code review** — a GitHub trigger runs on `pull_request.opened`, applies your team's review checklist, and leaves inline comments for security, performance, and style issues plus a summary comment.
- **Deploy verification** — your CD pipeline calls the routine's API endpoint after each production deploy; the routine runs smoke checks, scans error logs for regressions, and posts a go or no-go to the release channel.
- **Docs drift** — a weekly schedule trigger scans merged PRs since the last run, flags documentation that references changed APIs, and opens update PRs against the docs repository.
- **Library port** — a GitHub trigger runs on `pull_request.closed` filtered to merged PRs in one SDK repository, ports the change to a parallel SDK in another language, and opens a matching PR.

## Usage and limits

Routines draw down subscription usage the same way interactive sessions do. In addition to the standard subscription limits, routines have a **daily cap** on how many runs can start per account. Check current consumption and remaining daily routine runs at `claude.ai/code/routines` or `claude.ai/settings/usage`.

When a routine hits the daily cap or your subscription usage limit, organizations with **usage credits** turned on can keep running routines on metered overage; without usage credits, additional runs are rejected until the window resets. **One-off runs** do not count against the daily routine cap — they draw down regular subscription usage like any other session but are exempt from the per-account daily routine run allowance.

**Source**: https://code.claude.com/docs/en/routines
**Last Updated**: 2026-06-13
**Status**: Active
