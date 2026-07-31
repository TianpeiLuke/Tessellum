---
tags:
  - resource
  - documentation
  - claude_code
  - advisor
  - configuration
keywords:
  - advisor model
  - advisorModel setting
  - advisor command
  - advisor flag
  - accepted advisor pairings
  - opus sonnet fable aliases
  - turn the advisor off
  - advisor requirements
topics:
  - Claude Code
  - Advisor
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/advisor
access_control_group: ["general"]
---

# Configure the Advisor Model

## Overview

This note is the operational procedure for setting up the Claude Code advisor tool: how to enable it (three ways), which main-model/advisor pairings the API accepts, what the common pairings are, what it costs, what it requires, and how to turn it off. For what the advisor *is* and *when* Claude consults it, see the sibling concept note [cc_advisor_tool](cc_advisor_tool.md).

The advisor pairs your main model with a second, typically stronger model that Claude consults at decision points. The rule that governs every configuration choice below is simple: **the advisor must be at least as capable as the main model.**

## Enable the advisor

You can set the advisor model in three ways:

- **`/advisor` command** — set or change the advisor mid-session and save it as your default.
- **`advisorModel` setting** — configure a persistent default in your [settings file](https://code.claude.com/docs/en/settings).
- **`--advisor` flag** — set the advisor for a single session at launch.

If any of these sets an advisor model, the advisor is enabled for sessions whose main model supports it (see [Choose an advisor model](#choose-an-advisor-model)). To stop using it, see [Turn the advisor off](#turn-the-advisor-off).

> To use Fable 5 as the advisor, you need Claude Code v2.1.170 or later and Fable 5 access for your organization. Fable does not appear in the picker that `/advisor` opens, so pass it directly as `/advisor fable`, `--advisor fable`, or `"advisorModel": "fable"`.

### Use the `/advisor` command

Run `/advisor` without arguments to open a picker listing the available advisor models, or pass the model directly:

```
/advisor opus
```

Your selection is saved to `advisorModel` in your user settings and persists across sessions. If your current main model does not support the advisor, the selection is still saved and activates when you switch to a compatible main model with `/model`.

### Set `advisorModel` in settings

To configure the advisor as a default without opening a session, set it in your settings file:

```json
{
  "advisorModel": "opus"
}
```

### Use the `--advisor` flag

To set the advisor for a single session without changing your saved setting, launch with the flag:

```bash
claude --advisor opus
```

The flag takes precedence over the `advisorModel` setting for that session. Unlike `/advisor`, which saves an inactive selection, the flag exits with an error if the session's main model does not support the advisor.

## Choose an advisor model

The advisor must be at least as capable as the main model. The accepted advisors for each main model are:

| Main model | Accepted advisors | Notes |
|---|---|---|
| Haiku 4.5 | Fable, Opus, Sonnet | Haiku can call the advisor but cannot act as one |
| Sonnet 4.6 | Fable, Opus, Sonnet | |
| Opus 4.6 or later | Fable, Opus at or above the main model's version | An Opus 4.7 main with an Opus 4.6 advisor is rejected |
| Fable 5 (v2.1.170+) | Fable | An Opus or Sonnet advisor is rejected |

Fable 5 requires Claude Code v2.1.170 or later and Fable 5 access, whether it acts as the main model or the advisor. The `fable` option does not appear in the `/advisor` picker.

Set the advisor as `opus`, `sonnet`, or `fable`. These aliases resolve to the latest version of each model. You can also pass a full model ID such as `claude-opus-4-8`.

The API enforces the pairing, not Claude Code. Setting a rejected pairing succeeds, then surfaces as a `cannot be used as an advisor when the request model is` error on the next request.

### Common model pairings

Any accepted pairing works. These combinations balance cost against capability in different ways:

| Pairing | When to use |
|---|---|
| Sonnet main + Opus advisor | Sonnet handles routine work and escalates planning, ambiguous failures, and completion checks to Opus |
| Sonnet main + Fable advisor | Fable 5 guidance at decision points without running Fable 5 throughout. Requires v2.1.170 or later and Fable 5 access |
| Haiku main + Opus advisor | Lowest-cost main model with strong planning. Expect higher cost than Haiku alone but lower than switching the main model to Sonnet or Opus |
| Opus main + Opus advisor | A second Opus reviews the first. Useful for high-stakes tasks where an independent check matters more than cost |
| Fable main + Fable advisor | Highest-capability pairing when Fable 5 is available (v2.1.170+). Fable is a higher tier than Opus and Sonnet, so it is the only accepted advisor for a Fable main model |
| Sonnet main + Sonnet advisor | A lower-cost second opinion for catching routine oversights |

## Cost

Each advisor call sends the conversation to the advisor model, so it consumes tokens at the advisor model's rates in addition to your main model's usage. With API billing, advisor tokens are charged at the advisor model's input and output rates. On subscription plans, advisor usage counts toward your plan's usage limits.

Claude calls the advisor at decision points rather than on every turn, so pairing a faster main model with a stronger advisor typically costs less than running the stronger model throughout. Advisor usage counts toward the session totals shown by [`/usage`](https://code.claude.com/docs/en/costs).

## Requirements

The advisor tool requires all of the following:

- **Claude Code v2.1.98 or later** — run `claude update` to upgrade.
- **Anthropic API only** — the advisor is a server-executed tool. It is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. Through an [LLM gateway](https://code.claude.com/docs/en/llm-gateway) configured with `ANTHROPIC_BASE_URL`, availability depends on whether the gateway forwards the request intact to the Anthropic API.
- **Supported main model** — Opus 4.6 or later, Sonnet 4.6, or Haiku 4.5. Fable 5 also qualifies on Claude Code v2.1.170 or later.

## Turn the advisor off

To stop using the advisor and clear your saved `advisorModel`, run `/advisor off` or choose **No advisor** in the `/advisor` picker:

```
/advisor off
```

To disable the advisor tool entirely, including the `/advisor` command and the `--advisor` flag, set `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1`. See [Environment variables](https://code.claude.com/docs/en/env-vars).

**Source**: https://code.claude.com/docs/en/advisor
**Last Updated**: 2026-06-13
**Status**: Active
