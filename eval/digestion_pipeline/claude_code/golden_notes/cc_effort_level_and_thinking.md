---
tags:
  - resource
  - documentation
  - claude_code
  - model_config
  - reasoning
keywords:
  - effort level
  - adaptive reasoning
  - extended thinking
  - ultrathink
  - ultracode
  - effortLevel setting
  - CLAUDE_CODE_EFFORT_LEVEL
  - thinking tokens
  - fixed thinking budget
  - max effort
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

# Claude Code — Effort Level and Extended Thinking

## Overview

**Effort levels** control **adaptive reasoning** in Claude Code: the model decides whether and how much to think on each step based on task complexity. Lower effort is faster and cheaper for straightforward tasks; higher effort provides deeper reasoning for complex problems. The available levels (`low` → `max`, plus the Claude-Code-only `ultracode`) depend on the model, and effort can be set five ways with a defined precedence. A related but separate control, **extended thinking**, governs whether the reasoning is emitted at all and how it displays — on adaptive-reasoning models the effort level is the primary dial for *how much* thinking happens, while the thinking controls turn it on/off.

This note documents the **Effort level** doc-concept (its assigned home in this sub-plan), the `ultrathink` keyword, adaptive vs. fixed thinking budgets, and the extended-thinking display/toggle controls.

## Adjust Effort Level

[Effort levels](https://platform.claude.com/docs/en/build-with-claude/effort) control adaptive reasoning, which lets the model decide whether and how much to think on each step based on task complexity. Lower effort is faster and cheaper for straightforward tasks, while higher effort provides deeper reasoning for complex problems.

The available effort levels depend on the model. Models not listed do not support effort:

| Model | Levels |
|---|---|
| Fable 5 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.8 and Opus 4.7 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 and Sonnet 4.6 | `low`, `medium`, `high`, `max` |

If you set a level the active model does not support, Claude Code falls back to the highest supported level at or below the one you set (for example, `xhigh` runs as `high` on Opus 4.6).

The **default effort is `high`** on Fable 5, Opus 4.8, Opus 4.6, and Sonnet 4.6, and **`xhigh` on Opus 4.7**. When you first run Fable 5, Opus 4.8, or Opus 4.7, Claude Code applies that model's default effort even if you previously set a different level for another model (`high` on Fable 5 and Opus 4.8, `xhigh` on Opus 4.7); run `/effort` again to choose a different level after switching.

`low`, `medium`, `high`, and `xhigh` persist across sessions. `max` provides the deepest reasoning with no constraint on token spending and applies to the **current session only**, except when set through the `CLAUDE_CODE_EFFORT_LEVEL` environment variable.

The effort scale is **calibrated per model**, so the same level name does not represent the same underlying value across models.

### Ultracode

The `/effort` menu also offers `ultracode`. Ultracode is a **Claude Code setting rather than a model effort level**: it sends `xhigh` to the model and additionally has Claude orchestrate dynamic workflows for substantive tasks. It applies to the current session only. Set it through `/effort`, or pass `"ultracode": true` via `--settings` or an Agent SDK control request. It is **not** part of the `effortLevel` setting, the `--effort` flag, or `CLAUDE_CODE_EFFORT_LEVEL`.

### Choose an Effort Level

Each level trades token spend against capability. The default suits most coding tasks; adjust when you want a different balance.

| Level | When to use it |
|---|---|
| `low` | Reserve for short, scoped, latency-sensitive tasks that are not intelligence-sensitive |
| `medium` | Reduces token usage for cost-sensitive work that can trade off some intelligence |
| `high` | Balances token usage and intelligence. Default on Fable 5, Opus 4.8, Opus 4.6, and Sonnet 4.6 |
| `xhigh` | Deeper reasoning at higher token spend. Default on Opus 4.7 |
| `max` | Can improve performance on demanding tasks but may show diminishing returns and is prone to overthinking. Test before adopting broadly |
| `ultracode` | A Claude Code setting that plans a dynamic workflow for each substantive task with `xhigh` per-message reasoning. Session-only |

### Use Ultrathink for One-Off Deep Reasoning

Include `ultrathink` anywhere in your prompt to request deeper reasoning on that turn without changing your session effort setting. Claude Code recognizes the keyword and adds an in-context instruction; the effort level sent to the API is unchanged. Other phrases such as "think", "think hard", and "think more" are passed through as ordinary prompt text and are **not** recognized as keywords.

### Set the Effort Level

You can change effort through any of the following, listed with their precedence below:

- **`/effort`** — run `/effort` with no arguments to open an interactive slider, `/effort` followed by a level name to set it directly, or `/effort auto` to reset to the model default.
- **In `/model`** — use left/right arrow keys to adjust the effort slider when selecting a model.
- **`--effort` flag** — pass a level name to set it for a single session when launching Claude Code.
- **Environment variable** — set `CLAUDE_CODE_EFFORT_LEVEL` to a level name or `auto`.
- **Settings** — set `effortLevel` to `low`, `medium`, `high`, or `xhigh` in your settings file. `max` and `ultracode` are session-only and are not accepted here.
- **Skill and subagent frontmatter** — set `effort` in a skill or subagent markdown file to override the effort level when that skill or subagent runs.

**Precedence:** the environment variable takes precedence over all other methods, then your configured level, then the model default. Frontmatter effort applies when that skill or subagent is active, overriding the session level but not the environment variable.

The effort slider appears in `/model` when a supported model is selected. The current effort level is also displayed next to the logo and spinner — for example "with low effort" — so you can confirm which setting is active without opening `/model`.

### Adaptive Reasoning and Fixed Thinking Budgets

Adaptive reasoning makes thinking optional on each step, so Claude can respond faster to routine prompts and reserve deeper thinking for steps that benefit from it. If you want Claude to think more or less often than the current level produces, you can say so directly in your prompt or in `CLAUDE.md`; the model responds to that guidance within its effort setting.

Opus 4.7 and later always use adaptive reasoning, as does Fable 5. The fixed thinking budget mode and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` do not apply to them. On Opus 4.6 and Sonnet 4.6, you can set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS` (see the [environment variables reference](https://code.claude.com/docs/en/env-vars)).

## Extended Thinking

Extended thinking is the reasoning Claude emits before responding. On models that support adaptive reasoning, **the effort level is the primary control for how much thinking happens**; the controls below turn thinking on or off and control how it displays.

| Control | How to set it |
|---|---|
| Toggle for the current session | Press `Option+T` on macOS or `Alt+T` on Windows and Linux |
| Set the global default | Run `/config` and toggle thinking mode. Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json` |
| Disable regardless of effort | Set `MAX_THINKING_TOKENS=0`, which turns thinking off on the Anthropic API except on Fable 5. On third-party providers this omits the `thinking` parameter instead, and adaptive-reasoning models may still think. Other values apply only with a fixed thinking budget |

Thinking **cannot be turned off on Fable 5**. The session toggle, `alwaysThinkingEnabled`, and `MAX_THINKING_TOKENS=0` have no effect there, and Fable 5 decides per step how much to think based on the effort level.

Thinking output is collapsed by default. Press `Ctrl+O` to toggle verbose mode and see the reasoning as gray italic text. Interactive sessions on the Anthropic API receive redacted thinking blocks by default, so set `showThinkingSummaries: true` in settings if you want the full summaries available when you expand. **You are charged for all thinking tokens generated, even when collapsed or redacted.**

**Source**: https://code.claude.com/docs/en/model-config
**Last Updated**: 2026-06-13
**Status**: Active
