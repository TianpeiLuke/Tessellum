---
tags:
  - resource
  - documentation
  - claude_code
  - cost
  - token_usage
keywords:
  - cost tracking
  - usage command
  - api token consumption
  - workspace spend limit
  - rate limit recommendations
  - agent team token costs
  - background token usage
  - claude code workspace
topics:
  - Claude Code
  - Cost
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/costs
access_control_group: ["general"]
---

# Claude Code — Track and Manage Costs

## Overview

Claude Code charges by **API token consumption** (subscription plan pricing is separate — see [claude.com/pricing](https://claude.com/pricing)). Per-developer cost varies widely with model selection, codebase size, and usage patterns such as running multiple instances or automation. Across enterprise deployments the average is around **$13 per developer per active day** and **$150-250 per developer per month**, staying below $30 per active day for 90% of users. The recommended way to estimate spend for your own team is to start with a small pilot group and use the tracking tools to establish a baseline before wider rollout.

This note covers the *tracking and team-management* procedure: inspecting session cost with `/usage`, setting team spend and rate limits, accounting for agent-team token scaling, background token usage, and checking your Claude Code version when behavior changes. The complementary *cost-reduction strategies* (manage context, choose the model, offload to hooks/skills, etc.) live in [cc_reduce_token_usage.md](cc_reduce_token_usage.md).

## Track your costs

### Using the `/usage` command

The **Session block** at the top of `/usage` shows detailed token usage statistics for your current session. The dollar figure is an estimate computed locally from token counts and may differ from your actual bill; for authoritative billing, see the Usage page in the Claude Console.

```text theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

The Session block reports API token usage and is intended for API users. Claude Max and Pro subscribers have usage included in their subscription, so the session cost figure is not relevant for billing — subscribers instead see plan usage bars, activity stats, and a usage breakdown on the same screen.

On a Pro, Max, Team, or Enterprise plan, `/usage` also shows a breakdown of what counts against your plan limits. It **attributes recent usage to skills, subagents, plugins, and individual MCP servers**, each shown as a percentage of the total. Press `d` or `w` to switch between the last 24 hours and the last 7 days. The figures are approximate and computed from local session history on this machine, so usage from other devices or claude.ai is not included. The same breakdown appears in the VS Code extension's Account & usage dialog (Day/Week toggle), which requires Claude Code v2.1.174 or later.

## Managing costs for teams

When using the Claude API, you can set **workspace spend limits** on total Claude Code workspace spend, and admins can view cost and usage reporting in the Console. On Pro and Max plans, set a monthly spend limit on usage credits with the `/usage-credits` command; if you reach the limit while usage credits remain, Claude Code prompts you to raise or remove the limit so you can continue without leaving the CLI. Changing the limit requires billing access on the account.

When you first authenticate Claude Code with your Claude Console account, a workspace called **"Claude Code"** is automatically created. It provides centralized cost tracking and management for all Claude Code usage in your organization. You cannot create API keys for this workspace — it is exclusively for Claude Code authentication and usage. For organizations with custom rate limits, Claude Code traffic in this workspace counts toward the organization's overall API rate limits; you can set a workspace rate limit on its Limits page to cap Claude Code's share and protect other production workloads.

On Bedrock, Vertex, and Foundry, Claude Code does **not** send cost metrics from your cloud. To get cost metrics, several large enterprises reported using LiteLLM, an open-source tool that helps companies track spend by key. (This project is unaffiliated with Anthropic and has not been audited for security.)

### Rate limit recommendations

When setting up Claude Code for teams, consider these Token Per Minute (TPM) and Request Per Minute (RPM) per-user recommendations based on organization size:

| Team size     | TPM per user | RPM per user |
| ------------- | ------------ | ------------ |
| 1-5 users     | 200k-300k    | 5-7          |
| 5-20 users    | 100k-150k    | 2.5-3.5      |
| 20-50 users   | 50k-75k      | 1.25-1.75    |
| 50-100 users  | 25k-35k      | 0.62-0.87    |
| 100-500 users | 15k-20k      | 0.37-0.47    |
| 500+ users    | 10k-15k      | 0.25-0.35    |

For example, with 200 users you might request 20k TPM per user, or 4 million total TPM (200 × 20,000). The TPM-per-user figure decreases as team size grows because fewer users tend to use Claude Code concurrently in larger organizations. These rate limits apply **at the organization level, not per individual user**, so individual users can temporarily consume more than their calculated share when others are not actively using the service. If you anticipate unusually high concurrent usage (such as live training sessions with large groups), you may need higher TPM allocations per user.

### Agent team token costs

[Agent teams](https://code.claude.com/docs/en/agent-teams) spawn multiple Claude Code instances, **each with its own context window**, so token usage scales with the number of active teammates and how long each one runs. To keep agent-team costs manageable:

- Use Sonnet for teammates — it balances capability and cost for coordination tasks.
- Keep teams small — each teammate runs its own context window, so token usage is roughly proportional to team size.
- Keep spawn prompts focused — teammates load CLAUDE.md, MCP servers, and skills automatically, but everything in the spawn prompt adds to their context from the start.
- Clean up teams when work is done — active teammates continue consuming tokens even when idle.
- Agent teams are disabled by default; set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json or your environment to enable them.

## Background token usage

Claude Code uses tokens for some background functionality even when idle:

- **Conversation summarization** — background jobs that summarize previous conversations for the `claude --resume` feature.
- **Command processing** — some commands like `/usage` may generate requests to check status.

These background processes consume a small amount of tokens (typically under $0.04 per session) even without active interaction.

## Understanding changes in Claude Code behavior

Claude Code regularly receives updates that may change how features work, including cost reporting. Run `claude --version` to check your current version. For specific billing questions, contact Anthropic support through your Console account.

**Source**: https://code.claude.com/docs/en/costs
**Last Updated**: 2026-06-13
**Status**: Active
