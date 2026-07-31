---
tags:
  - resource
  - documentation
  - claude_code
  - adoption
  - champion
keywords:
  - champion kit
  - claude code adoption
  - thirty-day playbook
  - share what you discover
  - answer with a prompt
  - grow the circle
  - show-and-tell thread
  - team onboarding
topics:
  - Claude Code
  - Adoption
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/champion-kit
access_control_group: ["general"]
---

# Claude Code — Champion Playbook

## Overview

The **champion kit** is a playbook for an individual engineer who already uses Claude Code and wants to help their team adopt it. Its core argument is that developer-tool adoption rarely follows from a rollout announcement — it follows from one person using the tool well, talking about it openly, and making it easy for others to follow. The champion is a **multiplier for their team, not a help desk**: every shared example shortens the learning curve for the next engineer, and every question answered in public turns one person's experience into something the whole team can build on.

This note digests the proactive-advocacy half of the kit — the champion role and its weekly time budget, what/where/how to share discoveries, answering questions with prompts rather than explanations, the recurring habits that grow the circle, the thirty-day sequence, and the quick-reference technique sheet. The reactive skeptic-response material (questions you will hear, common concerns) lives in the sibling note [Adoption Objection Handling](cc_adoption_objection_handling.md).

## The Champion Role

The role consists of **three behaviors that reinforce one another**:

- **Share what you discover** — post the prompts, screenshots, and small wins from your own work where your team already reads (an engineering channel, a standup thread, a PR description). Examples drawn from your own codebase are more persuasive than external documentation because colleagues see exactly how the tool applies to problems they share with you.
- **Be the person people ask** — when a colleague asks how you accomplished something, respond with the actual prompt you used so they can apply it directly. A concrete, runnable example removes the gap between curiosity and a first successful use, which is where most adoption efforts stall.
- **Grow the circle** — establish a small number of lightweight, recurring habits (a dedicated channel, a weekly thread) so momentum continues even when your attention is elsewhere. Adoption that depends on a single person is fragile; adoption carried by shared habits compounds on its own.

Most of this fits inside work you are already doing; the difference is a small amount of intention about where discoveries are posted and how answers travel.

### What this should cost you

The role is meant to fit inside a normal working week and remain a multiplier on existing work rather than an added support responsibility:

| Activity | Time per week | Guidance |
|---|---|---|
| Posting wins and prompts | ~15 min | Capture in the moment with a screenshot and one or two sentences; avoid formal write-ups. |
| Answering questions in a shared channel | ~20 min | Answer publicly once, then link back when the question recurs. |
| Hosting a weekly show-and-tell thread | ~5 min | You post the opening prompt; the team supplies the content. |
| Optional pairing or walkthroughs | 0–30 min | Reserve for genuinely blocked colleagues; offer the Quickstart link before scheduling time. |

## Share What You Discover

Your own experience is the most persuasive material colleagues will encounter because it is specific to the shared codebase, workflows, and problems. Documentation says what is *possible*; your posts show what is *actually working* in your environment.

- **What is worth sharing** — the most useful posts describe a *technique a colleague can reuse tomorrow* rather than a completed outcome. Techniques compound as they spread; status updates do not. Examples: that `@`-mentioning a directory surfaces files missing tests, that plan mode (`Shift+Tab`) shows which files will be touched before any edit, that a Stop hook can send a desktop notification when a long task completes, or that `/init` generates a `CLAUDE.md` so the assistant stops re-asking about conventions.
- **Where to share it** — post wherever your team already reads, placing examples in the path of normal work rather than building a destination: a `#claude-code` or general engineering channel (discoveries and "today I learned" moments), pull-request descriptions (the approach on real code reviewers already see), standups/weekly updates (normalizing usage with leads), and the team wiki (durable patterns, custom skills, `CLAUDE.md` examples).
- **The format that works** — a screenshot plus a single line of context, or a brief before-and-after, is the right level of detail. A long write-up tends to be saved and forgotten; a short post with a screenshot tends to be copied and tried.

The example posts in the source illustrate tone and length and are meant to be adapted, not copied verbatim — for instance:

```text
Plan mode is the reason I am comfortable using this on code that matters.
Press Shift+Tab until you see "plan"; it lays out exactly which files it
intends to touch before changing anything.
```

## Be the Person People Ask

Once you have shared a few examples, questions follow — and this is where the role has the greatest leverage, because a good answer to one person frequently unblocks several others watching the same channel. Two tactics:

- **Answer with a prompt rather than an explanation** — the most useful response to "how did you do that?" is the prompt you actually used. Colleagues learn more from running it against their own problem than from any description, and it gives them something to act on immediately.
- **Point at the feature rather than the documentation** — "Try plan mode, press `Shift+Tab` until you see it" is more useful in the moment than a doc link. If the person needs more depth later they will find it; right now they need the single thing that unblocks them.

The specific "questions you are likely to hear" and "common concerns" response tables are covered in [Adoption Objection Handling](cc_adoption_objection_handling.md).

## Grow the Circle

The objective is not to build a program or own a rollout — it is to establish a small number of lightweight habits that let momentum continue after you stop actively driving it. When channel questions are being answered by people *other than you*, the role has done its job.

### Patterns that tend to work

| Pattern | How to run it | Effort |
|---|---|---|
| A dedicated channel | Create a `#claude-code` channel (or recurring thread), pin the Quickstart and one strong example, answer publicly. | ~5 min to set up, then ambient |
| A weekly show-and-tell thread | Each Friday post "What did Claude help you with this week?" No prep or meeting required. | ~2 min/week |
| Share a custom skill | Post your most useful `.claude/skills/<name>/SKILL.md` (e.g. a `/ship` skill that runs tests and lint before committing) with a one-line description. Skills are plain Markdown, so colleagues adopt them immediately. | ~5 min/skill |
| Generate a setup guide from your own usage | Run `/team-onboarding` in a project you have spent real time in; Claude scans your recent sessions, commands, and MCP servers and produces a guide a new teammate can paste as their first message to replay your setup. | ~2 min |
| Pair on a first task | Offer a single 15-minute pairing session to anyone getting started. One success on their own code beats any presentation. | ~15 min/person |
| Identify the next champion | The colleague who asks the most questions is usually ready; forward them this page and divide channel duties. | Negligible |

### Thirty-day playbook

A loose week-by-week sequence, each with a **"signal that it is working"** marker:

- **Week 1 — Seed the channel.** Create the channel, pin the Quickstart, and post two or three of your own examples with prompts included. *Signal:* a few colleagues react or reply, and at least one question is asked.
- **Week 2 — Start the rhythm.** Begin the weekly show-and-tell thread, answer every question publicly, and share one custom skill or `CLAUDE.md` snippet. *Signal:* someone other than you posts an example of their own.
- **Week 3 — Pair and consolidate.** Offer two or three short pairing sessions and consolidate common questions into a pinned FAQ message. *Signal:* repeat usage, with the same colleagues returning rather than trying once and stopping.
- **Week 4 — Hand off.** Identify a second champion and share a brief summary of what is and is not working with your lead or administrator. *Signal:* questions in the channel are being answered by people other than you.

### When someone wants to go deeper

You are the **warm introduction, not the onboarding program**. When a colleague moves past "should I try this" into "how do I become effective with it," point them to the Quickstart and Common workflows pages, which cover the genuinely useful but hard-to-discover features. (Both pages own other sub-plans: see https://code.claude.com/docs/en/quickstart and https://code.claude.com/docs/en/common-workflows.)

## Quick-Reference Sheet

The techniques that most reliably move someone from a first trial to daily use — pin this in a channel or share it on its own:

| Technique | How to apply it |
|---|---|
| Provide the right context | Use `@file` or `@directory/` references, or paste the error/log output directly. Supplying relevant context beats elaborate prompting. |
| Review the plan before the edit | Press `Shift+Tab` to enter plan mode; Claude describes the intended changes for approval before executing. |
| Teach it your repository | Run `/init` to generate a `CLAUDE.md`, then add conventions, test commands, and directories that should not be modified. |
| Reuse a workflow | Save a `SKILL.md` in `.claude/skills/<name>/` to create a `/name` skill the whole team can use. |
| Stay informed during long tasks | Configure a Stop hook to receive a desktop notification when a long-running task completes. |
| Recover from an incorrect result | Rather than rephrasing, paste the failing test or stack trace back to Claude and ask it to address that specific failure. |
| Keep edits surgical | Ask for a diff, or specify "only change X." Claude respects scope when scope is stated. |

The source closes with a reminder that Claude Code is updated frequently, so version-specific details should be verified against the documentation home page before distributing material internally.

**Source**: https://code.claude.com/docs/en/champion-kit
**Last Updated**: 2026-06-13
**Status**: Active
