---
tags:
  - resource
  - documentation
  - claude_code
  - code_review
  - customization
keywords:
  - code review setup
  - review behavior
  - claude review trigger
  - review.md
  - claude.md review
  - severity recalibration
  - nit cap
  - skip rules
  - spend cap troubleshooting
topics:
  - Claude Code
  - Code Review
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/code-review
access_control_group: ["general"]
---

# Claude Code — Code Review Setup and Customization

## Overview

This note is the operator procedure for turning Claude Code's managed **Code Review** service on for a repository, triggering reviews on demand, and tuning what it flags. An admin enables Code Review once for the organization, picks repositories, and chooses a per-repo **Review Behavior** (once after PR creation / after every push / manual). Reviewers can then start a review at any time with the `@claude review` and `@claude review once` comment commands. Two repository files steer the reviewer's behavior: `CLAUDE.md` (shared project context, whose newly introduced violations become nits) and `REVIEW.md` (review-only instructions injected as the highest-priority block into every agent in the pipeline). The note closes with usage monitoring and the troubleshooting paths for failed, spend-capped, or invisible reviews.

The reviewer mechanics this configures — the parallel agent fleet, verification step, severity levels, and check-run output — are covered in [Code Review (reviewer mechanics)](cc_code_review.md); the no-GitHub-App local equivalent is [the local /code-review command](cc_code_review_local_command.md).

## Set up Code Review

An admin enables Code Review once for the organization and selects which repositories to include. The setup flow has five steps:

1. **Open Claude Code admin settings** — Go to `claude.ai/admin-settings/claude-code` and find the Code Review section. You need admin access to your Claude organization and permission to install GitHub Apps in your GitHub organization.
2. **Start setup** — Click **Setup** to begin the GitHub App installation flow.
3. **Install the Claude GitHub App** — Install it to your GitHub organization. The app requests these repository permissions: **Contents** (read and write), **Issues** (read and write), and **Pull requests** (read and write). Code Review itself uses read access to contents and write access to pull requests; the broader set also supports [GitHub Actions](https://code.claude.com/docs/en/github-actions) if enabled later.
4. **Select repositories** — Choose which repositories to enable. A repository that does not appear was not granted GitHub App access during installation; more repositories can be added later.
5. **Set review triggers per repo** — After setup, the Code Review section lists your repositories in a table with a **Review Behavior** dropdown per repo (see below).

After setup, the repositories table also shows the **average cost per review** for each repo based on recent activity, and a row actions menu to turn Code Review on or off per repository or remove a repository entirely.

To verify setup, open a test PR. With an automatic trigger, a **Claude Code Review** check run appears within a few minutes; with Manual, comment `@claude review` to start the first review. If no check run appears, confirm the repository is listed in admin settings and the Claude GitHub App has access to it.

### Review Behavior options

The per-repo **Review Behavior** dropdown chooses when reviews run:

- **Once after PR creation** — review runs once when a PR is opened or marked ready for review.
- **After every push** — review runs on every push to the PR branch, catching new issues as the PR evolves and auto-resolving threads when flagged issues are fixed.
- **Manual** — reviews start only when someone comments `@claude review` or `@claude review once` on a PR; `@claude review` also subscribes the PR to reviews on subsequent pushes.

Reviewing on every push runs the most reviews and costs the most. Manual mode is useful for high-traffic repos where you want to opt specific PRs into review, or to only start reviewing PRs once they are ready.

## Manually trigger reviews

Two comment commands start a review on demand. Both work regardless of the repository's configured trigger, so they can opt specific PRs into review in Manual mode or get an immediate re-review in other modes:

- `@claude review` — starts a review **and** subscribes the PR to push-triggered reviews going forward.
- `@claude review once` — starts a **single** review without subscribing the PR to future pushes.

Use `@claude review once` when you want feedback on a PR's current state but don't want every subsequent push to incur a review (long-running PRs with frequent pushes, or a one-off second opinion without changing the PR's review behavior).

For either command to trigger a review:

- Post it as a **top-level PR comment**, not an inline comment on a diff line.
- Put the command at the **start** of the comment, with `once` on the same line for the one-shot form.
- You must have owner, member, or collaborator access to the repository.
- The PR must be open.

Unlike automatic triggers, manual triggers run on **draft PRs**, since an explicit request signals you want the review now regardless of draft status. If a review is already running on that PR, the request is queued until the in-progress review completes; monitor progress via the check run on the PR.

## Customize reviews

Code Review reads two repository files to guide what it flags. They differ in how strongly they influence the review:

- **`CLAUDE.md`** — shared project instructions Claude Code uses for all tasks, not just reviews. Code Review reads it as project context and flags **newly introduced violations as nits**.
- **`REVIEW.md`** — review-only instructions, injected directly into every agent in the review pipeline as **highest priority**. Use it to change what gets flagged, at what severity, and how findings are reported.

### CLAUDE.md

Code Review reads your repository's `CLAUDE.md` files and treats newly introduced violations as nit-level findings. This works **bidirectionally**: if your PR changes code in a way that makes a `CLAUDE.md` statement outdated, Claude flags that the docs need updating too. Claude reads `CLAUDE.md` files at every level of the directory hierarchy, so rules in a subdirectory's `CLAUDE.md` apply only to files under that path. For review-specific guidance you don't want applied to general Claude Code sessions, use `REVIEW.md` instead. (See [Agentic Memory](../../term_dictionary/term_agentic_memory.md) for how `CLAUDE.md` works.)

### REVIEW.md

`REVIEW.md` is a file at the repository root that overrides how Code Review behaves. Its contents are injected into the system prompt of every agent in the review pipeline as the highest-priority instruction block, taking precedence over the default review guidance. Because it is **pasted verbatim**, `REVIEW.md` is plain instructions: `@` import syntax is not expanded and referenced files are not read into the prompt — put the rules you want enforced directly in the file.

`REVIEW.md` is freeform markdown; anything expressible as a review instruction is in scope. The patterns with the most impact in practice:

- **Severity** — redefine what 🔴 Important means for your repo. The default calibration targets production code; a docs, config, or prototype repo might want a narrower definition. State explicitly which classes of finding are Important and which are Nit at most. You can also escalate (e.g. treat any `CLAUDE.md` violation as Important rather than the default nit).
- **Nit volume** — cap how many 🟡 Nit comments a single review posts, e.g. "report at most five nits, mention the rest as a count in the summary."
- **Skip rules** — list paths, branch patterns, and finding categories where Claude should post no findings (generated code, lockfiles, vendored deps, machine-authored branches, and anything CI already enforces like linting or spellcheck). For paths warranting some review but not full scrutiny, set a higher bar instead of skipping: "in `scripts/`, only report if near-certain and severe."
- **Repo-specific checks** — add rules to flag on every PR (e.g. "new API routes must have an integration test"). Because `REVIEW.md` is injected as highest priority, these land more reliably than the same rules in a long `CLAUDE.md`.
- **Verification bar** — require evidence before a class of finding is posted, e.g. "behavior claims need a `file:line` citation in the source, not an inference from naming."
- **Re-review convergence** — tell Claude how to behave when a PR has already been reviewed, e.g. "after the first review, suppress new nits and post Important findings only."
- **Summary shape** — ask the review body to open with a one-line tally such as `2 factual, 4 style`, and to lead with "no factual issues" when that's the case.

Keep `REVIEW.md` focused: length has a cost, and a long file dilutes the rules that matter most. Keep it to instructions that change review behavior, and leave general project context in `CLAUDE.md`.

#### Example REVIEW.md

This `REVIEW.md` recalibrates severity for a backend service, caps nits, skips generated files, and adds repo-specific checks:

```markdown theme={null}
# Review instructions

## What Important means here

Reserve Important for findings that would break behavior, leak data,
or block a rollback: incorrect logic, unscoped database queries, PII
in logs or error messages, and migrations that aren't backward
compatible. Style, naming, and refactoring suggestions are Nit at
most.

## Cap the nits

Report at most five Nits per review. If you found more, say "plus N
similar items" in the summary instead of posting them inline. If
everything you found is a Nit, lead the summary with "No blocking
issues."

## Do not report

- Anything CI already enforces: lint, formatting, type errors
- Generated files under `src/gen/` and any `*.lock` file
- Test-only code that intentionally violates production rules

## Always check

- New API routes have an integration test
- Log lines don't include email addresses, user IDs, or request bodies
- Database queries are scoped to the caller's tenant
```

## View usage

Go to `claude.ai/analytics/code-review` to see Code Review activity across the organization. The dashboard shows **PRs reviewed** (daily count over the selected range), **Cost weekly** (weekly spend), **Feedback** (count of review comments auto-resolved because a developer addressed the issue), and a **Repository breakdown** (per-repo counts of PRs reviewed and comments resolved). The admin-settings repositories table also shows average cost per review per repo. Dashboard cost figures are estimates for monitoring; for invoice-accurate spend, refer to your Anthropic bill. The full analytics surface is documented in the [Analytics docs](https://code.claude.com/docs/en/analytics).

## Troubleshooting

Review runs are best-effort: a failed run never blocks your PR, but it also does not retry on its own.

- **Retrigger a failed or timed-out review** — When the infrastructure hits an internal error or exceeds its time limit, the check run completes with the title **Code review encountered an error** or **Code review timed out** (conclusion still neutral, so merges aren't blocked, but no findings are posted). To run it again, comment `@claude review once` on the PR (a fresh review without subscribing to future pushes); if the PR is already subscribed, pushing a new commit also starts a new review. The **Re-run** button in GitHub's Checks tab does **not** retrigger Code Review — use the comment command or a new push instead.
- **Review didn't run and the PR shows a spend-cap message** — When the organization's monthly spend cap is reached, Code Review posts a single comment explaining the review was skipped. Reviews resume automatically at the start of the next billing period, or immediately when an admin raises the cap at `claude.ai/admin-settings/usage`.
- **Find issues that aren't showing as inline comments** — If the check run title says issues were found but no inline comments appear, look in the **Check run Details** (severity table with every finding's file/line/summary), the **Files changed annotations** (findings attached directly to diff lines), or the **Review body** (findings on lines that no longer exist appear under an **Additional findings** heading).

**Source**: https://code.claude.com/docs/en/code-review
**Last Updated**: 2026-06-13
**Status**: Active
