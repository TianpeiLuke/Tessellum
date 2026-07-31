---
tags:
  - resource
  - documentation
  - claude_code
  - fast_mode
  - performance
keywords:
  - fast mode
  - /fast toggle
  - opus low latency
  - cost tradeoff
  - usage credits
  - rate limit fallback
  - per-session opt-in
  - research preview
topics:
  - Claude Code
  - Fast Mode
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/fast-mode
access_control_group: ["general"]
---

# Claude Code — Fast Mode

## Overview

**Fast mode** is a high-speed configuration for Claude Opus that makes the model **up to 2.5x faster at a higher cost per token**. Toggle it on with `/fast` when speed matters for interactive work like rapid iteration or live debugging, and toggle it off when cost matters more than latency. It is **not a different model**: fast mode runs Claude Opus with a different API configuration that prioritizes speed over cost efficiency, so you get identical quality and capabilities with faster responses.

Fast mode is supported on **Opus 4.8, Opus 4.7, and Opus 4.6** — not on Sonnet, Haiku, or other models — and is a **research preview** feature whose behavior, pricing, and availability may change. It requires Claude Code **v2.1.36 or later** (`claude --version`). Fast mode for Opus 4.6 is deprecated and will be removed approximately 30 days after the Opus 4.8 launch; after removal, fast mode on Opus 4.6 falls back to standard speed at standard pricing, so migrate to Opus 4.8 or Opus 4.7 to keep the speedup.

## Toggle fast mode

Toggle fast mode in either of these ways:

- Type `/fast` and press Tab to toggle on or off
- Set `"fastMode": true` in your [user settings file](https://code.claude.com/docs/en/settings)

By default, fast mode **persists across sessions**. Administrators can configure it to reset each session (see [Require per-session opt-in](#require-per-session-opt-in)). For the best cost efficiency, enable fast mode at the start of a session rather than switching mid-conversation.

When you enable fast mode:

- If you're on a different model, Claude Code automatically switches to Opus
- You'll see a confirmation message: "Fast mode ON"
- A small `↯` icon appears next to the prompt while fast mode is active
- Run `/fast` again at any time to check whether fast mode is on or off

When you disable fast mode with `/fast` again, you **remain on Opus** — the model does not revert to your previous model. To switch to a different model, use `/model`. Opus 4.8 is the fast mode default in Claude Code v2.1.154 and later; on v2.1.142 through v2.1.153, fast mode defaults to Opus 4.7.

## Understand the cost tradeoff

Fast mode has higher per-token pricing than standard Opus, with the multiplier varying by model:

| Model                 | Input (MTok) | Output (MTok) |
| --------------------- | ------------ | ------------- |
| Opus 4.8              | $10          | $50           |
| Opus 4.7 and Opus 4.6 | $30          | $150          |

Pricing is **flat across the full 1M token context window**. For Claude Code users on subscription plans (Pro/Max/Team/Enterprise), fast mode is available via **usage credits only** and is not included in the subscription rate limits.

The first time you enable fast mode in a conversation, you pay the full fast mode uncached input token price for the **entire conversation context**. The deeper into a conversation you are, the more this costs, so enabling fast mode from the start is cheaper. The cost applies **once per conversation** — toggling fast mode off and on again later does not repeat it. For the underlying mechanism, see [how fast mode interacts with the prompt cache](https://code.claude.com/docs/en/prompt-caching#turning-on-fast-mode).

## Decide when to use fast mode

Fast mode is best for **interactive work where response latency matters more than cost**:

- Rapid iteration on code changes
- Live debugging sessions
- Time-sensitive work with tight deadlines

Standard mode is better for:

- Long autonomous tasks where speed matters less
- Batch processing or CI/CD pipelines
- Cost-sensitive workloads

### Fast mode vs effort level

Fast mode and effort level both affect response speed, but differently:

| Setting                | Effect                                                                           |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Fast mode**          | Same model quality, lower latency, higher cost                                   |
| **Lower effort level** | Less thinking time, faster responses, potentially lower quality on complex tasks |

You can combine both: use fast mode with a lower [effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level) for maximum speed on straightforward tasks.

## Requirements

Fast mode requires all of the following:

- **Anthropic API or subscription only**: it is available through the Anthropic Console API and for Claude subscription plans using usage credits. It is **not** available on Amazon Bedrock, Google Vertex AI, Microsoft Azure Foundry, or Claude Platform on AWS.
- **Usage credits turned on**: your account must have usage credits turned on, which allows billing beyond your plan's included usage. Individual accounts turn this on in Console billing settings; for Team and Enterprise, an admin must turn on usage credits for the organization. Fast mode usage draws directly from usage credits even if you have remaining usage on your plan — fast mode tokens do not count against your plan's included usage and are charged at the fast mode rate from the first token.
- **Admin enablement for Team and Enterprise**: fast mode is disabled by default for Team and Enterprise organizations. An admin must explicitly enable it before users can access it. If your admin has not enabled it, the `/fast` command shows "Fast mode has been disabled by your organization."

### Enable fast mode for your organization

Admins can enable fast mode in:

- **Console** (API customers): Claude Code preferences
- **Claude AI** (Team and Enterprise): Admin Settings > Claude Code

Another option to disable fast mode entirely is to set `CLAUDE_CODE_DISABLE_FAST_MODE=1` (see [Environment variables](https://code.claude.com/docs/en/env-vars)).

### Require per-session opt-in

By default, if a user enables fast mode it stays on in future sessions. Administrators on Team or Enterprise plans can prevent this by setting `fastModePerSessionOptIn` to `true` in [managed settings](https://code.claude.com/docs/en/settings#settings-files) or [server-managed settings](https://code.claude.com/docs/en/server-managed-settings). This causes each session to start with fast mode off, requiring users to explicitly enable it with `/fast`.

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

This is useful for controlling costs where users run multiple concurrent sessions. Users can still enable fast mode with `/fast` when they need speed, but it resets at the start of each new session. The user's fast mode preference is still saved, so removing this setting restores the default persistent behavior.

## Handle rate limits

Fast mode has **separate rate limits** from standard Opus. Fast mode on Opus 4.8, Opus 4.7, and Opus 4.6 **shares the same rate limit pool** — usage on any of them draws from the same limits. When you hit the fast mode rate limit or run out of usage credits:

1. Fast mode automatically falls back to standard speed
2. The `↯` icon turns gray to indicate cooldown
3. You continue working at standard speed and pricing
4. When the cooldown expires, fast mode automatically re-enables

To disable fast mode manually instead of waiting for cooldown, run `/fast` again.

## Research preview

Fast mode is a research preview feature. This means:

- The feature may change based on feedback
- Availability and pricing are subject to change
- The underlying API configuration may evolve

Report issues or feedback through your usual Anthropic support channels.

**Source**: https://code.claude.com/docs/en/fast-mode
**Last Updated**: 2026-06-13
**Status**: Active
