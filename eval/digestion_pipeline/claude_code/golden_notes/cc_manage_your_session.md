---
tags:
  - resource
  - documentation
  - claude_code
  - session_management
  - context_discipline
keywords:
  - manage your session
  - course-correct early
  - clear between tasks
  - manage context aggressively
  - subagents for investigation
  - rewind checkpoints
  - resume conversations
  - common failure patterns
  - develop intuition
topics:
  - Claude Code
  - Session Management
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/best-practices
access_control_group: ["general"]
---

# Claude Code — Communicate Effectively and Manage Your Session

## Overview

Claude Code conversations are **persistent and reversible**, and the central argument of these best-practice sections is that managing the session well is mostly about protecting the context window — the fundamental constraint. The way you communicate (asking senior-engineer-style questions, letting Claude interview you into a spec) and the way you steer a session (course-correcting early, `/clear`-ing between tasks, compacting aggressively, delegating investigation to subagents, rewinding with checkpoints, resuming named sessions) all exist to keep the context clean so performance does not degrade.

This note also collects the five **common failure patterns** these habits prevent, and closes with the "develop your intuition" caveat that the patterns are starting points, not rules. Checkpoint and session mechanics are summarized here and detailed in their home pages ([Checkpointing](https://code.claude.com/docs/en/checkpointing), [Manage sessions](https://code.claude.com/docs/en/sessions)).

## Communicate Effectively

The way you communicate with Claude Code significantly impacts the quality of results.

### Ask codebase questions

When onboarding to a new codebase, use Claude Code for learning and exploration: ask the same questions you would ask another engineer — how logging works, how to make a new API endpoint, what `async move { ... }` does on a given line, what edge cases a class handles, why one function is called instead of another. No special prompting is required; ask directly. This is an effective onboarding workflow that improves ramp-up time and reduces load on other engineers. (Copy-paste prompt recipes for these tasks live in [Workflow recipes](cc_workflow_recipes.md).)

### Let Claude interview you

For larger features, have Claude interview you first. Start with a minimal prompt and ask Claude to interview you using the `AskUserQuestion` tool — it asks about technical implementation, UI/UX, edge cases, and tradeoffs you might not have considered:

```text
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is complete, start a **fresh session** to execute it: the new session has clean context focused entirely on implementation, and you have a written spec to reference. The most useful specs are self-contained — they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step. Time spent making the spec precise pays off more than time spent watching the implementation.

## Manage Your Session

Conversations are persistent and reversible — use this to your advantage.

### Course-correct early and often

The best results come from tight feedback loops. Though Claude occasionally solves a problem perfectly on the first attempt, correcting it quickly generally produces better solutions faster. The steering controls:

- **`Esc`** — stop Claude mid-action; context is preserved so you can redirect.
- **`Esc + Esc` or `/rewind`** — open the rewind menu to restore previous conversation and code state, or summarize from a selected message.
- **`"Undo that"`** — have Claude revert its changes.
- **`/clear`** — reset context between unrelated tasks.

If you have corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections.

### Manage context aggressively

Claude Code automatically compacts conversation history when you approach context limits, preserving important code and decisions while freeing space. During long sessions, the context window can fill with irrelevant conversation, file contents, and commands, which reduces performance and can distract Claude.

- Use `/clear` frequently between tasks to reset the context window entirely.
- When auto compaction triggers, Claude summarizes what matters most — code patterns, file states, and key decisions.
- For more control, run `/compact <instructions>`, e.g. `/compact Focus on the API changes`.
- To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose **Summarize from here** or **Summarize up to here**.
- Customize compaction behavior in CLAUDE.md with instructions like *"When compacting, always preserve the full list of modified files and any test commands"* to ensure critical context survives summarization.
- For quick questions that do not need to stay in context, use `/btw`: the answer appears in a dismissible overlay and never enters conversation history.

(The compaction mechanism and checkpointing are detailed in [Context window / costs](https://code.claude.com/docs/en/costs) and [Checkpointing](https://code.claude.com/docs/en/checkpointing).)

### Use subagents for investigation

Since context is the fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads many files, all of which consume your context. Subagents run in **separate context windows and report back summaries**, keeping the main conversation clean for implementation. Delegate research with `"use subagents to investigate X"`; you can also use a subagent for verification after Claude implements something (e.g. `use a subagent to review this code for edge cases`).

### Rewind with checkpoints

Every prompt you send creates a checkpoint, and Claude automatically snapshots files before each change so a checkpoint can restore them. Double-tap `Escape` or run `/rewind` to open the rewind menu; you can restore conversation only, code only, both, or summarize from a selected message. Because checkpoints make changes reversible, you can tell Claude to try something risky and rewind if it does not work. Checkpoints persist across sessions, so you can close your terminal and rewind later.

> **Warning:** Checkpoints only track changes made *by Claude*, not external processes. This is not a replacement for git.

### Resume conversations

Claude Code saves conversations locally, so when a task spans multiple sittings you do not have to re-explain context. Run `claude --continue` to pick up the most recent session, or `claude --resume` to choose from a list. Name sessions with `/rename` and treat them like branches — give each workstream a descriptive name like `oauth-migration` so you can find it later. See [Manage sessions](https://code.claude.com/docs/en/sessions) for the full set of resume, branch, and naming controls.

## Avoid Common Failure Patterns

Recognizing these common mistakes early saves time:

- **The kitchen sink session.** You start with one task, ask Claude something unrelated, then go back to the first task — context is full of irrelevant information. **Fix:** `/clear` between unrelated tasks.
- **Correcting over and over.** Claude does something wrong, you correct it, it is still wrong, you correct again — context is polluted with failed approaches. **Fix:** after two failed corrections, `/clear` and write a better initial prompt incorporating what you learned.
- **The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise. **Fix:** ruthlessly prune; if Claude already does something correctly without the instruction, delete it or convert it to a hook.
- **The trust-then-verify gap.** Claude produces a plausible-looking implementation that does not handle edge cases. **Fix:** always provide verification (tests, scripts, screenshots). If you cannot verify it, do not ship it.
- **The infinite exploration.** You ask Claude to "investigate" something without scoping it, and Claude reads hundreds of files, filling the context. **Fix:** scope investigations narrowly or use subagents so the exploration does not consume your main context.

## Develop Your Intuition

The patterns in this guide are not set in stone — they are starting points that work well in general but might not be optimal for every situation. Sometimes you *should* let context accumulate because you are deep in one complex problem and the history is valuable; sometimes you should skip planning because the task is exploratory; sometimes a vague prompt is exactly right because you want to see how Claude interprets the problem before constraining it.

Pay attention to what works. When Claude produces great output, notice what you did — the prompt structure, the context you provided, the mode you were in. When Claude struggles, ask why: was the context too noisy, the prompt too vague, the task too big for one pass? Over time you will develop intuition that no guide can capture about when to be specific and when to be open-ended, when to plan and when to explore, when to clear context and when to let it accumulate.

**Source**: https://code.claude.com/docs/en/best-practices
**Last Updated**: 2026-06-13
**Status**: Active
