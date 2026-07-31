---
tags:
  - resource
  - documentation
  - claude_code
  - analytics
  - dashboards
keywords:
  - analytics dashboard
  - team and enterprise dashboard
  - api console dashboard
  - usage metrics
  - contribution metrics
  - suggestion accept rate
  - lines of code accepted
  - team insights
  - daily active users
topics:
  - Claude Code
  - Analytics
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/analytics
access_control_group: ["general"]
---

# Claude Code — Analytics Dashboards

## Overview

Claude Code ships two hosted analytics dashboards that let an organization understand developer usage patterns, track contribution, and measure how Claude Code affects engineering velocity — no telemetry setup required (unlike the self-hosted [OpenTelemetry pipeline](https://code.claude.com/docs/en/monitoring-usage)). Which dashboard you use depends on your plan: **Claude for Teams / Enterprise** users go to `claude.ai/analytics/claude-code` (usage + contribution metrics + leaderboard + CSV export), while **API (Claude Console)** customers go to `platform.claude.com/claude-code` (usage + spend tracking + team insights).

This note documents the two dashboard surfaces: who can see them, the summary metrics each defines, and the trend charts. The contribution-metric setup (GitHub app) and the PR-attribution algorithm that powers "with Claude Code" tagging are covered separately in [PR Attribution](cc_pr_attribution.md).

## Dashboard access by plan

| Plan | Dashboard URL | Includes |
|---|---|---|
| Claude for Teams / Enterprise | `claude.ai/analytics/claude-code` | Usage metrics, contribution metrics with GitHub integration, leaderboard, data export |
| API (Claude Console) | `platform.claude.com/claude-code` | Usage metrics, spend tracking, team insights |

## Team and Enterprise dashboard

Navigate to `claude.ai/analytics/claude-code`. **Admins and Owners** can view the dashboard. It includes four feature areas:

- **Usage metrics**: lines of code accepted, suggestion accept rate, daily active users and sessions.
- **Contribution metrics**: PRs and lines of code shipped with Claude Code assistance, via GitHub integration (setup + attribution algorithm in [PR Attribution](cc_pr_attribution.md)).
- **Leaderboard**: top contributors ranked by Claude Code usage.
- **Data export**: download contribution data as CSV for custom reporting.

For per-user token counts and cost estimates, the source directs operators to configure [OpenTelemetry export](https://code.claude.com/docs/en/monitoring-usage) instead.

### Review summary metrics

The dashboard displays these summary metrics at the top. The source notes these metrics are deliberately conservative and represent an underestimate of Claude Code's actual impact — only lines and PRs where there is high confidence in Claude Code's involvement are counted.

- **PRs with CC**: total count of merged pull requests that contain at least one line of code written with Claude Code.
- **Lines of code with CC**: total lines of code across all merged PRs that were written with Claude Code assistance. Only "effective lines" are counted — lines with more than 3 characters after normalization, excluding empty lines and lines with only brackets or trivial punctuation.
- **PRs with Claude Code (%)**: percentage of all merged PRs that contain Claude Code-assisted code.
- **Suggestion accept rate**: percentage of times users accept Claude Code's code editing suggestions, including Edit, Write, and NotebookEdit tool usage.
- **Lines of code accepted**: total lines of code written by Claude Code that users have accepted in their sessions. This excludes rejected suggestions and does not track subsequent deletions.

### Explore the charts

The dashboard includes several charts to visualize trends over time.

- **Track adoption** — the Adoption chart shows daily usage trends: **users** (daily active users) and **sessions** (number of active Claude Code sessions per day).
- **Measure PRs per user** — this chart displays individual developer activity over time: **PRs per user** (total number of PRs merged per day divided by daily active users) and **users** (daily active users). Use it to understand how individual productivity changes as Claude Code adoption increases.
- **View pull requests breakdown** — the Pull requests chart shows a daily breakdown of merged PRs: **PRs with CC** vs **PRs without CC**. Toggle to **Lines of code** view to see the same breakdown by lines of code rather than PR count.
- **Find top contributors** — the Leaderboard shows the top 10 users ranked by contribution volume. Toggle between **Pull requests** (PRs with Claude Code vs All PRs per user) and **Lines of code** (lines with Claude Code vs All lines per user). Click **Export all users** to download complete contribution data for all users as a CSV file — the export includes all users, not just the top 10 displayed.

## API customers (Claude Console) dashboard

API customers using the Claude Console can access analytics at `platform.claude.com/claude-code`. You need the **UsageView permission** to access the dashboard, which is granted to **Developer, Billing, Admin, Owner, and Primary Owner** roles. Per the source, contribution metrics with GitHub integration are not currently available for API customers — the Console dashboard shows usage and spend metrics only.

The Console dashboard displays:

- **Lines of code accepted**: total lines of code written by Claude Code that users have accepted in their sessions. This excludes rejected suggestions and does not track subsequent deletions.
- **Suggestion accept rate**: percentage of times users accept code editing tool usage, including Edit, Write, and NotebookEdit tools.
- **Activity**: daily active users and sessions shown on a chart.
- **Spend**: daily API costs in dollars alongside user count.

### View team insights

The team insights table shows per-user metrics:

- **Members**: all users who have authenticated to Claude Code. API key users display by key identifier; OAuth users display by email address.
- **Spend this month**: per-user total API costs for the current month.
- **Lines this month**: per-user total of accepted code lines for the current month.

The source notes that spend figures in the Console dashboard are estimates for analytics purposes; for actual costs it directs users to their billing page.

**Source**: https://code.claude.com/docs/en/analytics
**Last Updated**: 2026-06-13
**Status**: Active
