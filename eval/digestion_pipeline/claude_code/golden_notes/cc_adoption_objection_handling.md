---
tags:
  - resource
  - documentation
  - claude_code
  - adoption
  - objection_handling
keywords:
  - objection handling
  - common concerns
  - questions you are likely to hear
  - acknowledge reframe demonstrate
  - skeptic response
  - plan mode trust
  - it hallucinated context problem
  - champion adoption
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

# Claude Code — Adoption Objection Handling

## Overview

When a Claude Code champion shares examples, two kinds of pushback follow: practical **questions** ("what should I try first?", "how do I trust it?") and deeper **concerns** ("I don't trust AI on production code", "it will weaken juniors"). This note is the reactive companion to the proactive [champion playbook](cc_champion_playbook.md): a skeptic-response argument for converting curiosity and doubt into a first successful use.

The champion-kit's governing move for concerns is **acknowledge → reframe → propose one concrete demonstration on the person's own code**. Healthy skepticism is expected — engineers should be cautious about tools that touch their code — and arguing the general case rarely works. Most concerns are resolved by a single successful experience, so every response below ends in an offer to try one real task rather than a debate.

## Questions you are likely to hear

These are first-contact, practical questions. The champion answers in the moment, then points at one follow-up resource (not a long doc) so the person can go deeper on their own later.

| Question | Response in brief | Follow-up resource |
| --- | --- | --- |
| "What should I try it on first?" | Recommend a real but contained task — ideally a bug or chore postponed because it is tedious, not difficult. | Common workflows |
| "How do I trust it with my code?" | Introduce plan mode (`Shift+Tab` cycles into it): Claude proposes exactly what it intends to change, and nothing is modified until the user approves. | Permissions |
| "Is the setup worth the effort?" | Installation takes ~two minutes, runs in the terminal, needs no IDE extension; running `/init` once is enough to begin. | Quickstart |
| "It produced an incorrect result." | Have them give the failure back to Claude — pasting the error message or failing test beats rephrasing the original request. | Common workflows |
| "It doesn't understand our conventions." | Run `/init` to generate a `CLAUDE.md`, then add conventions, test commands, and directories to avoid. | Memory |
| "Is this just autocomplete?" | Offer a brief demo where Claude explains an unfamiliar file, traces a bug across services, or drafts a migration plan — tasks that require reasoning across the repository, not completing one line. | A two-minute live demonstration |
| "What about security and data handling?" | Refer this to the administrator. The org's deployment and data-handling policy is already configured, and champions should not improvise this answer. | Security · Data usage |

The security question is deliberately routed away from the champion: the standard advice is to hand it to the admin (whose rollout comms cover it — see [Security](https://code.claude.com/docs/en/security) and [Data usage](https://code.claude.com/docs/en/data-usage)) rather than guess at org policy.

## Respond to common concerns

These are deeper objections to the practice of AI-assisted coding itself. For each, acknowledge the legitimate part, offer a short reframe, then propose one concrete piece of evidence the skeptic can produce on their own code.

| Concern | Suggested reframe | Evidence to offer |
| --- | --- | --- |
| "I am faster without it." | Likely true for routine code; suggest trying it on the work they avoid — legacy files, unfamiliar services, test scaffolding — where leverage is highest. | Time one tedious task both ways and compare. |
| "I don't trust AI to touch production code." | Agree no change should land unread. Plan mode plus normal diff review means nothing is applied that wasn't inspected — the same standard as any pull request. | Demonstrate plan mode on a real file. |
| "It will make junior engineers weaker." | Used well it is an effective explainer; encourage juniors to ask Claude to explain a file and its call sites before changing anything. | Run "Explain @file and where it is called from" together. |
| "I tried it once and it hallucinated." | Usually a context problem, not a model problem — @-mentioning the relevant files, running `/init`, and providing the actual error output typically resolves it. | Re-run their original prompt with proper `@`-context. |
| "We don't have time to learn another tool." | Claude Code is a terminal command, not a platform; if it doesn't return value within the first session it is reasonable to set aside. | A two-minute install followed by one real bug. |

Two reframes do the most work. The **trust** objection collapses to plan mode plus diff review — review discipline the team already practices. The **hallucination** objection is recast as a context-supply problem the user can fix immediately, not a verdict on the model.

**Source**: https://code.claude.com/docs/en/champion-kit
**Last Updated**: 2026-06-13
**Status**: Active
