---
tags:
  - resource
  - documentation
  - claude_code
  - code_review
  - cloud
keywords:
  - ultrareview
  - code-review ultra
  - multi-agent code review
  - reviewer agents
  - remote sandbox
  - independent verification
  - claude ultrareview subcommand
  - usage credits
topics:
  - Claude Code
  - Code Review
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/ultrareview
access_control_group: ["general"]
---

# Find Bugs with Ultrareview

## Overview

**Ultrareview** is a deep, multi-agent code review that runs on Claude Code on the web infrastructure. When you run `/code-review ultra`, Claude Code launches a **fleet of reviewer agents in a remote sandbox** to find bugs in your branch or pull request before you merge. It is a research-preview feature available in Claude Code v2.1.86 and later (the command was previously `/ultraplan`'s counterpart `/ultrareview`, which remains as an alias); its feature set, pricing, and availability may change based on feedback.

Compared to a local `/review`, ultrareview's distinguishing property is **higher signal**: every reported finding is independently reproduced and verified, so results focus on real bugs rather than style suggestions. It also offers **broader coverage** (many reviewer agents explore the change in parallel, surfacing issues a single-pass review can miss) and **no local resource use** (the review runs entirely in a remote sandbox, so your terminal stays free for other work). Because it runs on Claude Code on the web, ultrareview requires authentication with a Claude.ai account; if you are signed in with an API key only, run `/login` and authenticate with Claude.ai first. Ultrareview is **not available** when using Claude Code with Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry, and it is not available to organizations that have enabled Zero Data Retention.

## Run Ultrareview from the CLI

Start a review from any git repository in the Claude Code CLI:

```text
/code-review ultra
```

Without arguments, ultrareview reviews the diff between your current branch and the default branch, including any uncommitted and staged changes in your working tree. Claude Code bundles the repository state and uploads it to a remote sandbox for the review.

To review a GitHub pull request instead, pass the PR number:

```text
/code-review ultra 1234
```

In **PR mode**, the remote sandbox clones the pull request directly from the host rather than bundling your local working tree. PR mode works with repositories on `github.com` and on [GitHub Enterprise Server](cc_github_enterprise_server.md) instances that an admin has connected to Claude Code. If your repository is too large to bundle, Claude Code prompts you to use PR mode instead — push your branch, open a draft PR, then run `/code-review ultra <PR-number>`.

Before launching, Claude Code shows a confirmation dialog with the review scope (including the file and line count when reviewing a branch), your remaining free runs, and the estimated cost. After you confirm, the review continues in the background and you can keep using your session. The command runs only when you invoke it with `/code-review ultra`; Claude does not start an ultrareview on its own.

## Pricing and Free Runs

Ultrareview is a premium feature that bills against usage credits rather than your plan's included usage. Pro and Max subscribers receive **three free runs** to try the feature — a one-time allotment per account that does not refresh. Team and Enterprise plans have no included free runs. After the free runs (or after the free-run period ends), each review is billed to usage credits and typically costs $5 to $20 depending on the size of the change. A run counts once the cloud session starts, so a review you stop early or that fails to complete still uses a free run; for a paid review, usage credits are billed only for the portion that ran.

Because ultrareview always bills as usage credits outside the free runs, your account or organization must have usage credits turned on before you can launch a paid review. If usage credits are not turned on, Claude Code blocks the launch and links you to the billing settings; you can also run `/usage-credits` to check or change your current setting. See [Manage costs effectively](https://code.claude.com/docs/en/costs) for tracking usage and setting spending limits.

## Track a Running Review

A review typically takes 5 to 10 minutes. It runs as a background task, so you can keep working in your session, start other commands, or close the terminal entirely. Use `/tasks` to see running and completed reviews, open the detail view for a review, or stop a review that is in progress. Stopping a review archives the cloud session, and partial findings are not returned. When the review finishes, the verified findings appear as a notification in your session; each finding includes the file location and an explanation of the issue so you can ask Claude to fix it directly.

## Run Ultrareview Non-Interactively

Use the `claude ultrareview` subcommand to start an ultrareview from CI or a script without an interactive session. The subcommand launches the same review as `/code-review ultra`, blocks until the remote review finishes, prints the findings to stdout, and exits with code 0 on success or 1 on failure:

```bash
claude ultrareview
claude ultrareview 1234
claude ultrareview origin/main
```

Without arguments, the subcommand reviews the diff between your current branch and the default branch. Pass a PR number to review a pull request, or pass a base branch to review the diff against that branch instead. Invoking the subcommand counts as consent for the billing and terms prompt that the interactive command shows. Progress messages and the live session URL go to stderr so stdout stays parseable. Two flags control output and timeout:

- `--json` — print the raw `bugs.json` payload instead of the formatted findings.
- `--timeout <minutes>` — maximum minutes to wait for the review to finish (defaults to 30).

Running `claude ultrareview` requires the same authentication and usage-credit configuration as `/code-review ultra`. **Exit codes:** the subcommand exits with code 0 when the review completes with or without findings, code 1 when the review fails to launch / the cloud session errors / the timeout elapses, and code 130 when interrupted with Ctrl-C. The remote review keeps running if you interrupt the subcommand — follow the session URL printed to stderr to watch it in the browser. For automatic reviews on GitHub pull requests, [Code Review](cc_code_review.md) integrates with your repository directly and posts findings as inline PR comments without a CLI step.

## How Ultrareview Compares to /review

Both commands review code, but they target different stages of your workflow.

|          | `/review`                      | `/code-review ultra`                                            |
| -------- | ------------------------------ | --------------------------------------------------------------- |
| Runs     | locally in your session        | remotely in a cloud sandbox                                     |
| Depth    | single-pass review             | multi-agent fleet with independent verification                 |
| Duration | seconds to a few minutes       | roughly 5 to 10 minutes                                         |
| Cost     | counts toward normal usage     | free runs, then roughly $5 to $20 per review as usage credits   |
| Best for | quick feedback while iterating | pre-merge confidence on substantial changes                     |

Use `/review` for fast feedback as you work. Use `/code-review ultra` before merging a substantial change when you want a deeper pass that catches issues a single review might miss. The local `/review` (and `/code-review`) command is documented in [the local code-review command](cc_code_review_local_command.md), which can escalate to ultrareview via `/code-review ultra`.

**Source**: https://code.claude.com/docs/en/ultrareview
**Last Updated**: 2026-06-13
**Status**: Active
