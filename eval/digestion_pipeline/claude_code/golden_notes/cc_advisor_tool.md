---
tags:
  - resource
  - documentation
  - claude_code
  - advisor
  - model_pairing
keywords:
  - advisor tool
  - stronger advisor model
  - consult at decision points
  - server tool
  - decision-point guidance
  - advising transcript line
  - prompt cache intact
  - second opinion
topics:
  - Claude Code
  - Advisor
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/advisor
access_control_group: ["general"]
---

# Claude Code — The Advisor Tool

## Overview

The **advisor tool** lets Claude consult a second, typically stronger model at key moments during a task — for example before committing to an approach, when stuck on a recurring error, or before declaring a task complete. The advisor receives the **full conversation** (every tool call and result) and returns guidance that Claude applies before continuing. It runs **server-side** on Anthropic's infrastructure as a [server tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool), available to both subscription and API-billed accounts. You choose which model acts as the advisor, and **Claude decides when to call it**.

The advisor is experimental and requires Claude Code v2.1.98 or later with the Anthropic API; it is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry, and behavior, pricing, and availability may change. This note covers what the advisor is, when it fits, the model-driven consultation behavior, the in-session UX, its effect on prompt caching, and how it compares with related features. For how to enable it, choose a model pairing, and turn it off, see [Configure the Advisor Model](cc_configure_advisor_model.md).

## When to use the advisor

The advisor fits **long, multi-step tasks where most turns are routine but plan quality determines the outcome**. Examples include large refactors, debugging sessions where an error keeps recurring, and tasks you want independently checked before Claude declares them done.

It adds less value on short tasks where there is little to plan, or on work where every turn needs the strongest model. For those, [switch the main model](https://code.claude.com/docs/en/model-config) instead, or see the comparison below for other ways to get a second opinion.

## When Claude consults the advisor

Claude decides when to call the advisor. It tends to consult **before committing to an approach**, **when an error keeps recurring**, and **before declaring a task done**, but the timing is **model-driven rather than rule-based**.

You can ask for a consultation in your prompt the same way you would request any tool, for example `consult the advisor before you continue`. There is **no setting to cap or force** advisor calls; if you want Claude to consult more or less often during a task, say so in your instructions.

## What you see during a session

When Claude calls the advisor, the transcript shows an `Advising` line with the advisor model name while the call is in progress. When the result returns, the line confirms that the advisor has reviewed the conversation. Press `Ctrl+O` to expand it and read the advisor's full guidance.

Claude generally follows the advisor's guidance, but **adapts when its own evidence contradicts a specific claim**: if a recommended step fails when tried, or the file contents contradict the advice, Claude surfaces the conflict rather than following the guidance unconditionally.

The advisor always receives the full conversation, and Claude controls the timing. For more control or a different configuration, see the comparison below.

## Impact on prompt caching

Enabling or disabling the advisor mid-session **does not invalidate** your main model's [prompt cache](https://code.claude.com/docs/en/prompt-caching). Unlike changing model or effort level, toggling `/advisor` keeps the cached prefix intact, and the advisor's returned guidance is cached as part of the transcript on later turns.

The advisor model's own read of the conversation is **not cached**. Each advisor call processes the full transcript anew, with no reuse between calls.

## Compare with related features

The advisor is one of several ways to combine model strengths. Pick based on when you want a second model involved.

| Approach | When the stronger model runs | How it starts |
| --- | --- | --- |
| Advisor tool | At decision points mid-task | Claude calls it when it needs guidance |
| `opusplan` | During plan mode, then switches to Sonnet for execution | You enter plan mode |
| Subagents with `model` set | For the entire delegated subtask | Claude delegates, or you invoke the subagent |
| `/model` | For all subsequent turns | You switch models |

So the advisor gives **decision-point guidance** that Claude requests as needed, whereas [`opusplan`](https://code.claude.com/docs/en/model-config) scopes the stronger model to plan mode, a [subagent](../../term_dictionary/term_subagent.md) with a `model` set delegates an entire subtask to a chosen model, and [`/model`](https://code.claude.com/docs/en/model-config) switches the model for all subsequent turns.

**Source**: https://code.claude.com/docs/en/advisor
**Last Updated**: 2026-06-13
**Status**: Active
