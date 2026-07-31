---
tags:
  - resource
  - documentation
  - claude_code
  - analytics
  - pr_attribution
keywords:
  - pr attribution
  - claude-code-assisted
  - contribution metrics
  - github app integration
  - conservative matching
  - 21-day time window
  - excluded files
  - effective lines
  - roi measurement
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

# Claude Code — PR Attribution & Contribution Metrics

## Overview

When contribution metrics are enabled, Claude Code analyzes merged pull requests to determine which code was written with Claude Code assistance, matching session activity against the code in each PR. Enabling these metrics requires connecting a GitHub organization via the Claude GitHub app; the attribution engine then tags qualifying merged PRs as `claude-code-assisted` in GitHub. The matching is deliberately conservative — only code where there is high confidence in Claude Code's involvement is counted — so the resulting figures underestimate actual impact.

This note covers the GitHub-app setup that enables contribution metrics, the conservative attribution algorithm (extract → match → normalize), its 21-day time window and auto-generated-file exclusions, and how to read the resulting data for ROI, adoption, and power-user signals. The dashboard surfaces that display these numbers are documented in the sibling [Analytics Dashboards](cc_analytics_dashboards.md) note.

## Enable contribution metrics

Usage and adoption data is available for all Claude for Teams and Claude for Enterprise accounts. **Contribution metrics require additional setup** to connect your GitHub organization. They are in public beta on the Teams and Enterprise plans and only cover users within your claude.ai organization — usage through the Claude Console API or third-party integrations is not included.

Roles: you need the **Owner** role to configure analytics settings, and a **GitHub admin** must install the GitHub app. Setup is four steps:

1. **Install the GitHub app** — a GitHub admin installs the Claude GitHub app on the organization's GitHub account at `github.com/apps/claude`.
2. **Enable Claude Code analytics** — a Claude Owner navigates to `claude.ai/admin-settings/claude-code` and enables the Claude Code analytics feature.
3. **Enable GitHub analytics** — on the same page, enable the "GitHub analytics" toggle.
4. **Authenticate with GitHub** — complete the GitHub authentication flow and select which GitHub organizations to include in the analysis.

Data typically appears within 24 hours after enabling, with daily updates. If no data appears you may see **"GitHub app required"** (install the GitHub app) or **"Data processing in progress"** (check back in a few days and confirm the GitHub app is installed). Contribution metrics support GitHub Cloud and GitHub Enterprise Server.

> Contribution metrics are **not available for organizations with [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention) enabled** — the dashboard shows usage metrics only.

## PR attribution

When contribution metrics are enabled, Claude Code analyzes merged pull requests to determine which code was written with Claude Code assistance, by matching Claude Code session activity against the code in each PR.

### Tagging criteria

PRs are tagged as "with Claude Code" if they contain **at least one line of code written during a Claude Code session**. The system uses conservative matching: only code where there is high confidence in Claude Code's involvement is counted as assisted.

### Attribution process

When a pull request is merged:

1. Added lines are extracted from the PR diff.
2. Claude Code sessions that edited matching files within a time window are identified.
3. PR lines are matched against Claude Code output using multiple strategies.
4. Metrics are calculated for AI-assisted lines and total lines.

Before comparison, lines are **normalized**: whitespace is trimmed, multiple spaces are collapsed, quotes are standardized, and text is converted to lowercase. Merged pull requests containing Claude Code-assisted lines are labeled as `claude-code-assisted` in GitHub.

### Time window

Sessions from **21 days before to 2 days after** the PR merge date are considered for attribution matching.

### Excluded files

Certain files are automatically excluded from analysis because they are auto-generated:

- **Lock files**: `package-lock.json`, `yarn.lock`, `Cargo.lock`, and similar
- **Generated code**: Protobuf outputs, build artifacts, minified files
- **Build directories**: `dist/`, `build/`, `node_modules/`, `target/`
- **Test fixtures**: snapshots, cassettes, mock data
- **Lines over 1,000 characters**, which are likely minified or generated

### Attribution notes

Keep these additional details in mind when interpreting attribution data:

- Code substantially rewritten by developers, with **more than 20% difference**, is not attributed to Claude Code.
- Sessions outside the 21-day window are not considered.
- The algorithm does not consider the PR source or destination branch when performing attribution.

## Get the most from analytics

Use contribution metrics to demonstrate ROI, identify adoption patterns, and find team members who can help others get started.

- **Monitor adoption** — track the Adoption chart and user counts to identify active users who can share best practices, overall adoption trends across the organization, and dips in usage that may indicate friction or issues.
- **Measure ROI** — contribution metrics help answer "Is this tool worth the investment?" with data from your own codebase: track changes in PRs per user over time as adoption increases; compare PRs and lines of code shipped with vs. without Claude Code; and use alongside DORA metrics, sprint velocity, or other engineering KPIs to understand changes from adopting Claude Code.
- **Identify power users** — the Leaderboard helps find team members with high Claude Code adoption who can share prompting techniques and workflows, provide feedback on what is working well, and help onboard new users.
- **Access data programmatically** — to query this data through GitHub, search for PRs labeled with `claude-code-assisted`.

**Source**: https://code.claude.com/docs/en/analytics
**Last Updated**: 2026-06-13
**Status**: Active
