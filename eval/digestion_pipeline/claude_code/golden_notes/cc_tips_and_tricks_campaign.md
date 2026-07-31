---
tags:
  - resource
  - documentation
  - claude_code
  - adoption
  - drip_campaign
keywords:
  - tips and tricks campaign
  - feature activation drip
  - try it now prompt
  - post-launch adoption
  - claude code communications kit
  - feature to message map
  - faq responses
  - prompt templates
topics:
  - Claude Code
  - Adoption
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/communications-kit
access_control_group: ["general"]
---

# Claude Code — Tips and Tricks Campaign

## Overview

The **tips-and-tricks campaign** is the post-launch half of the communications kit: a set of ready-to-paste Slack or Teams messages designed to **drive feature activation after launch**. Where the [launch communications](cc_launch_communications.md) get people installed, the drip campaign moves them from "installed" to "uses the features." Every message is **draft copy** — rewrite it in your org's voice and replace `[bracketed placeholders]` before sending — and the messages **stand alone with no required order**, so an admin drips one or two a week into `#claude-code` or picks the handful that match the team's gaps.

The argument is that activation does not happen all at once: each feature needs its own small, well-timed nudge. The campaign supplies those nudges plus a Quick reference (one-line FAQ replies and starter prompt templates) for the questions and blank-page moments engineers hit most.

## The shared message pattern

Every drip message follows the same four-beat structure, which is the reusable template behind all eight topic groups:

1. **A hook** — a relatable pain ("Telling Claude 'we use pnpm, not npm' for the fifth time?").
2. **The payoff** — the one feature that fixes it, in one or two sentences.
3. **A "try it now" prompt** — a concrete, immediately runnable action.
4. **A docs link** — the home page for that feature.

Keep the body short enough to copy straight into chat. One representative block, the project-memory tip, shows the shape:

```markdown
📁 *Tip: Stop re-explaining your repo every session*

Telling Claude "we use pnpm, not npm" for the fifth time? There is a
one-time fix.

Run `/init` once per repo. Claude reads your project structure and writes a
CLAUDE.md file with your build commands, architecture, and conventions.
Every future session in that repo starts from this file automatically. Keep
it under two screens. It is a cheat sheet, not documentation.

*Try it now:* open your main repo, run `claude`, type `/init`. Thirty
seconds, pays off every session after.

📖 CLAUDE.md and project memory → https://code.claude.com/docs/en/memory
```

## The eight topic groups (feature → activation message)

The campaign organizes its messages into eight groups. Each row below is a feature and the activation message that drives it; the full feature is owned by its home page (linked), not re-explained here.

| Group | Feature → "try it now" nudge | Home page |
|---|---|---|
| **Get started** | *Choosing the right model* — match the model to the moment (Opus for large refactors / gnarly debugging / high-stakes, Sonnet the workhorse default, Haiku for quick mechanical edits, Fable 5 opt-in for the hardest longest tasks via `/model fable`); switch mid-session. **Try:** type `/model`, pick Sonnet. | [model-config](https://code.claude.com/docs/en/model-config) |
| **Get started** | *Quick wins to try first* — three things in your first 10 minutes: fix something annoying, get oriented in unfamiliar code, sanity-check a diff. **Try:** paste the error from the bug you've been avoiding. | [quickstart](https://code.claude.com/docs/en/quickstart) |
| **Project memory** | *`/init` and CLAUDE.md* — run `/init` once per repo so Claude stops re-asking the basics; *@-references* — type `@file` to pull a file (or directory) into context instead of pasting it. | [memory](https://code.claude.com/docs/en/memory) · [common-workflows](https://code.claude.com/docs/en/common-workflows) |
| **Control and safety** | *Permission modes* — `Shift+Tab` cycles default / acceptEdits / plan; plan mode is "the trust-builder, so start there for anything touching multiple files." *Checkpointing and `/rewind`* — the undo button for the whole conversation (Esc twice or `/rewind`); checkpointing is automatic. | [permissions](https://code.claude.com/docs/en/permissions) · [checkpointing](https://code.claude.com/docs/en/checkpointing) |
| **Connect your tools** | *MCP connectors* — one `.mcp.json` at the project root wires Claude into GitHub / Jira / Linear. **Try:** ask Claude to "set up an MCP connector for [GitHub/Jira/Linear] in this repo." | [mcp](https://code.claude.com/docs/en/mcp) |
| **Automate your workflows** | *Skills* — a `SKILL.md` in `.claude/skills/<name>/` becomes a `/name` command; *Hooks* — a Stop hook fires a shell command (e.g. desktop notification) when a long task finishes. **Try:** "make me a /standup skill…" / "add a Stop hook that notifies me." | [skills](https://code.claude.com/docs/en/skills) · [hooks-guide](https://code.claude.com/docs/en/hooks-guide) |
| **Day-to-day development** | *Screenshots and images* — drag a screenshot in (or `Ctrl+V`, even on macOS) and ask "what's wrong here?"; *Git workflows* — hand off the whole git ceremony: "fix the off-by-one, commit with a conventional message, and open a PR." | [common-workflows](https://code.claude.com/docs/en/common-workflows) |
| **Share and scale** | *Plugins* — skills get bundled and shared as plugins; `/plugin` browses and installs in one step. **Try:** type `/plugin` and scroll. | [plugins](https://code.claude.com/docs/en/plugins) |
| **Security and admin** | *Security architecture* — the paste-ready "where does my code go?" answer (permission-first, talks only to Anthropic's API, no third-party servers, optional OS-level sandboxing, Enterprise no-training); *Best practices* — the 4 habits: plan mode for multi-file, `/init` early, review diffs, verify critical paths ("treat it like a sharp junior, not an oracle"). | [security](https://code.claude.com/docs/en/security) · [data-usage](https://code.claude.com/docs/en/data-usage) · [best-practices](https://code.claude.com/docs/en/best-practices) |

The accompanying **model table** (Fable 5 / Opus / Sonnet / Haiku and what each is best for) is reproduced on the model-config page; the campaign embeds it next to the "Choosing the right model" tip as the at-a-glance reference.

## Quick reference

Two tables back the campaign for the recurring questions and the blank-page moment.

**FAQ responses** — one-line replies for the most-asked questions, each ending in a docs link: *Does it work in VS Code?* (yes — VS Code extension + JetBrains plugin), *Do I have to configure anything first?* (no — install, `claude`, `/init` once), *Where does my code go?* (terminal → Anthropic's API, no third-party servers, Enterprise no-training), *Can it see my whole repo?* (only what you give it; reads inside the working dir don't prompt, edits/shell/outside do), *How is this different from Copilot?* (Copilot autocompletes lines; Claude Code is an agent that reads files, runs commands, makes multi-file edits), *What should I try first?* (a tedious bug you've been putting off).

**Prompt templates** — starter prompts phrased as you'd actually type them, for engineers who installed but aren't sure what to ask: fix a bug ("the tests in [file] are failing, figure out why and fix it"), understand code ("walk me through how [module] works…"), safe refactor ("…use plan mode so I can review first"), write tests, review before commit ("look at my working diff and tell me what looks risky"), open a PR ("…write a conventional commit, and open a PR with a summary"), make a skill ("make me a /ship skill…"), debug a stack trace ("…find the root cause, don't just paper over it").

> Claude Code ships frequently. Verify version-specific details against the documentation home page before distributing internally.

**Source**: https://code.claude.com/docs/en/communications-kit
**Last Updated**: 2026-06-13
**Status**: Active
