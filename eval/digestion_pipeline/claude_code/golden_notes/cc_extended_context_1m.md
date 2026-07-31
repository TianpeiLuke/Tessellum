---
tags:
  - resource
  - documentation
  - claude_code
  - model_config
  - extended_context
keywords:
  - extended context
  - 1m token context window
  - 1m suffix
  - claude_code_disable_1m_context
  - usage credits
  - automatic upgrade
  - opus 1m
  - sonnet 1m
topics:
  - Claude Code
  - Model Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/model-config
access_control_group: ["general"]
---

# Claude Code — Extended Context (1M Token Window)

## Overview

**Extended context** is the **1 million token context window** available on Claude Code's newer models for long sessions over large codebases. Whether you get it depends on both the model and your plan: some configurations include it with the subscription, some auto-upgrade Opus to it for free, and some require **usage credits**. This note covers which models support the 1M window, the plan-by-plan availability matrix, the auto-upgrade-versus-credits split, how to disable it (`CLAUDE_CODE_DISABLE_1M_CONTEXT`), its pricing, and how to request it explicitly with the `[1m]` suffix. The underlying context-window concept itself is covered in the [context-windows docs](https://code.claude.com/docs/en/build-with-claude/context-windows).

## Which Models Support 1M Context

**Fable 5, Opus 4.6 and later, and Sonnet 4.6** support the 1M token context window for long sessions with large codebases.

## Availability by Model and Plan

Availability varies by model and plan:

- On **Max, Team, and Enterprise** plans, **Opus is automatically upgraded** to 1M context with no additional configuration — this applies to both Team Standard and Team Premium seats.
- On the **Anthropic API**, Fable 5, Opus 4.8, and Opus 4.7 **always run with the 1M window**.
- **Sonnet with 1M context is not part of the automatic upgrade** and requires **usage credits** on every subscription plan, including Max.

| Plan | Opus with 1M context | Sonnet with 1M context |
| --- | --- | --- |
| Max, Team, and Enterprise | Included with subscription | Requires usage credits |
| Pro | Requires usage credits | Requires usage credits |
| API and pay-as-you-go | Full access | Full access |

## Disabling Extended Context

To disable 1M context entirely, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. This removes 1M model variants from the model picker. (See the full [environment variables list](https://code.claude.com/docs/en/env-vars).)

## Pricing

The 1M context window **uses standard model pricing with no premium for tokens beyond 200K**. For plans where extended context is included with your subscription, usage remains covered by your subscription. For plans that access extended context through usage credits, tokens are billed to usage credits.

## Selecting Extended Context

If your account supports 1M context, the option appears in the model picker (`/model`) in the latest versions of Claude Code. If you don't see it, try restarting your session.

You can also use the **`[1m]` suffix** with model aliases or full model names:

```bash
# Use the opus[1m] or sonnet[1m] alias
/model opus[1m]
/model sonnet[1m]

# Or append [1m] to a full model name
/model claude-opus-4-8[1m]
```

For **pinned models on third-party providers**, append `[1m]` to the model ID in `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_SONNET_MODEL`. That suffix applies the 1M window to all usage of the `opus` and `sonnet` aliases, including the plan-mode Opus phase of `opusplan`. Claude Code strips the suffix before sending the model ID to the provider; only append it when the underlying model supports 1M context; and the suffix is read per variable, not per model. (See [Model selection](cc_model_selection.md) for alias resolution and [Fallback models](cc_fallback_models.md) for the `opusplan` hybrid.)

**Source**: https://code.claude.com/docs/en/model-config
**Last Updated**: 2026-06-13
**Status**: Active
