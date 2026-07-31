---
tags:
  - resource
  - documentation
  - claude_code
  - skills
  - lifecycle
keywords:
  - skill invocation control
  - disable-model-invocation
  - user-invocable
  - skill content lifecycle
  - compaction re-attach budget
  - skilloverrides
  - skill permission rules
  - restrict skill access
topics:
  - Claude Code
  - Skills
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/skills
access_control_group: ["general"]
---

# Claude Code — Skill Invocation Control & Content Lifecycle

## Overview

By default both you and Claude can invoke any skill — you type `/skill-name`, and Claude loads it automatically when relevant. This note covers the two frontmatter fields that restrict *who* invokes a skill (`disable-model-invocation`, `user-invocable`), the **content lifecycle** of an invoked skill (how it enters context as one message, stays for the session, and is re-attached after auto-compaction within a token budget), the `skillOverrides` setting that controls visibility from settings instead of frontmatter, and the permission rules (`Skill`, `Skill(name)`, `Skill(name *)`) that govern which skills Claude may call through the Skill tool.

These mechanisms are how you keep a side-effecting skill like `/deploy` under manual control, how you expose background-knowledge skills to Claude but hide them from the menu, and how you reason about the recurring token cost a loaded skill imposes.

## Control who invokes a skill

By default, both you and Claude can invoke any skill. You can type `/skill-name` to invoke it directly, and Claude can load it automatically when relevant to your conversation. Two frontmatter fields let you restrict this:

- **`disable-model-invocation: true`**: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don't want Claude deciding to deploy because your code looks ready.
- **`user-invocable: false`**: Only Claude can invoke the skill. Use this for background knowledge that isn't actionable as a command. A `legacy-system-context` skill explains how an old system works — Claude should know this when relevant, but `/legacy-system-context` isn't a meaningful action for users to take.

The two fields affect invocation and context loading as follows:

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |
| :--- | :--- | :--- | :--- |
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context, full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when invoked |

In a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked. Subagents with preloaded skills work differently: the full skill content is injected at startup.

## Skill content lifecycle

When you or Claude invoke a skill, the rendered `SKILL.md` content enters the conversation as a **single message and stays there for the rest of the session**. Claude Code does not re-read the skill file on later turns, so write guidance that should apply throughout a task as standing instructions rather than one-time steps.

Auto-compaction carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, **keeping the first 5,000 tokens of each**. Re-attached skills share a **combined budget of 25,000 tokens**. Claude Code fills this budget starting from the most recently invoked skill, so older skills can be dropped entirely after compaction if you have invoked many in one session.

If a skill seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches. Strengthen the skill's `description` and instructions so the model keeps preferring it, or use hooks to enforce behavior deterministically. If the skill is large or you invoked several others after it, re-invoke it after compaction to restore the full content.

> The skill *listing* (descriptions Claude sees to decide what's available) has its own budget, separate from the loaded-content budget above: descriptions are shortened to fit a budget scaling at 1% of the model's context window, and each entry's combined `description` + `when_to_use` text is capped at 1,536 characters. Run `/doctor` to see whether that listing budget is overflowing. (Configured via `skillListingBudgetFraction` / `maxSkillDescriptionChars` — see [settings](https://code.claude.com/docs/en/settings).)

## Restrict Claude's skill access

By default, Claude can invoke any skill that doesn't have `disable-model-invocation: true` set. Skills that define `allowed-tools` grant Claude access to those tools without per-use approval when the skill is active; your permission settings still govern baseline approval behavior for all other tools. A few built-in commands are also available through the **Skill tool**, including `/init`, `/review`, and `/security-review`. Other built-in commands such as `/compact` are not.

Three ways to control which skills Claude can invoke:

**Disable all skills** by denying the Skill tool in `/permissions` — add `Skill` to the deny rules.

**Allow or deny specific skills** using permission rules:

```text
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Permission syntax: `Skill(name)` for exact match, `Skill(name *)` for prefix match with any arguments.

**Hide individual skills** by adding `disable-model-invocation: true` to their frontmatter. This removes the skill from Claude's context entirely.

The `user-invocable` field only controls menu visibility, not Skill tool access. Use `disable-model-invocation: true` to block programmatic invocation.

## Override skill visibility from settings

The `skillOverrides` setting controls skill visibility from your settings instead of the skill's own frontmatter. Use it for skills whose `SKILL.md` you don't want to edit, such as ones checked into a shared project repo or provided by an MCP server. The `/skills` menu writes it for you: highlight a skill and press `Space` to cycle states, then `Enter` to save to `.claude/settings.local.json`.

Each key is a skill name and each value is one of four states:

| Value | Listed to Claude | In `/` menu |
| :--- | :--- | :--- |
| `"on"` | Name and description | Yes |
| `"name-only"` | Name only | Yes |
| `"user-invocable-only"` | Hidden | Yes |
| `"off"` | Hidden | Hidden |

A skill that is absent from `skillOverrides` is treated as `"on"`. The example below collapses one skill to its name and turns another off entirely:

```json
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

Plugin skills are not affected by `skillOverrides`. Manage those through `/plugin` instead.

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
