---
tags:
  - resource
  - documentation
  - claude_code
  - code_review
  - multi_agent
keywords:
  - code review
  - multi-agent pr review
  - severity levels
  - verification step
  - check run output
  - false positive filtering
  - inline comments
  - research preview
topics:
  - Claude Code
  - Code Review
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/code-review
access_control_group: ["general"]
---

# Claude Code — Code Review

## Overview

**Code Review** is Claude Code's managed pull-request reviewer: it analyzes your GitHub PRs and posts findings as inline comments on the exact lines where it found issues. A **fleet of specialized agents** examines the code changes in the context of your full codebase, each looking for a different class of issue — logic errors, security vulnerabilities, broken edge cases, and subtle regressions. Findings are tagged by severity and **do not approve or block** your PR, so existing review workflows stay intact.

Code Review is in **research preview**, available for Team and Enterprise subscriptions, and is **not available for organizations with [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention) enabled**. To run Claude in your own CI infrastructure instead of this managed service, use [GitHub Actions](cc_github_actions.md) or [GitLab CI/CD](cc_gitlab_ci_cd.md); for self-hosted GitHub, see [GitHub Enterprise Server](cc_github_enterprise_server.md). This note covers the reviewer mechanics and pricing; enabling/customizing the service is in [Code Review setup and customization](cc_code_review_setup_and_customization.md) and the terminal command is in [the local `/code-review` command](cc_code_review_local_command.md).

## How reviews work

Once an admin enables Code Review for the organization, reviews trigger when a PR opens, on every push, or when manually requested, depending on the repository's configured behavior. (Commenting `@claude review` starts reviews on a PR in any mode — see [setup and customization](cc_code_review_setup_and_customization.md).)

When a review runs, **multiple agents analyze the diff and surrounding code in parallel on Anthropic infrastructure**. Each agent looks for a different class of issue, then a **verification step checks candidates against actual code behavior to filter out false positives**. The results are deduplicated, ranked by severity, and posted as inline comments on the specific lines where issues were found, with a summary in the review body. If no issues are found, Code Review updates the GitHub check run to show that no issues were detected, and Claude may post a short confirmation comment on the PR.

Reviews scale in cost with PR size and complexity, completing in **20 minutes on average**. Admins can monitor review activity and spend via the analytics dashboard (see [setup and customization](cc_code_review_setup_and_customization.md)).

### Severity levels

Each finding is tagged with a severity level:

| Marker | Severity     | Meaning                                                             |
| :----- | :----------- | :------------------------------------------------------------------ |
| 🔴     | Important    | A bug that should be fixed before merging                           |
| 🟡     | Nit          | A minor issue, worth fixing but not blocking                        |
| 🟣     | Pre-existing | A bug that exists in the codebase but was not introduced by this PR |

Findings include a collapsible extended reasoning section you can expand to understand why Claude flagged the issue and how it verified the problem.

### Rate and reply to findings

Each review comment from Claude arrives with 👍 and 👎 already attached so both buttons appear in the GitHub UI for one-click rating. Click 👍 if the finding was useful or 👎 if it was wrong or noisy. Anthropic collects reaction counts after the PR merges and uses them to tune the reviewer. **Reactions do not trigger a re-review** or change anything on the PR.

Replying to an inline comment does not prompt Claude to respond or update the PR. To act on a finding, fix the code and push. If the PR is subscribed to push-triggered reviews, the next run resolves the thread when the issue is fixed. To request a fresh review without pushing, comment `@claude review once` as a top-level PR comment.

### Check run output

Beyond the inline review comments, each review populates the **Claude Code Review** check run that appears alongside your CI checks. Expanding its **Details** link shows a summary of every finding in one place, sorted by severity (each row giving severity, `File:Line`, and the issue description). Each finding also appears as an **annotation in the Files changed tab**, marked directly on the relevant diff lines: Important findings render with a red marker, nits with a yellow warning, and pre-existing bugs with a gray notice. Annotations and the severity table are written to the check run **independently of inline review comments**, so they remain available even if GitHub rejects an inline comment on a line that moved.

The check run **always completes with a neutral conclusion** so it never blocks merging through branch protection rules. If you want to gate merges on Code Review findings, read the severity breakdown from the check run output in your own CI. The last line of the Details text is a machine-readable comment your workflow can parse with `gh` and jq:

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

This returns a JSON object with counts per severity, for example `{"normal": 2, "nit": 1, "pre_existing": 0}`. The `normal` key holds the count of Important findings; a non-zero value means Claude found at least one bug worth fixing before merge.

### What Code Review checks

By default, Code Review focuses on **correctness**: bugs that would break production, not formatting preferences or missing test coverage. You can expand what it checks by adding guidance files to your repository — see [Code Review setup and customization](cc_code_review_setup_and_customization.md).

## Pricing

Code Review is billed based on token usage. Each review averages **$15-25 in cost**, scaling with PR size, codebase complexity, and how many issues require verification. Code Review usage is billed separately through usage credits and **does not count against your plan's included usage**.

The review trigger you choose affects total cost:

- **Once after PR creation**: runs once per PR
- **After every push**: runs on each push, multiplying cost by the number of pushes
- **Manual**: no reviews until someone comments `@claude review` on a PR

In any mode, commenting `@claude review` opts the PR into push-triggered reviews, so additional cost accrues per push after that comment. To run a single review without subscribing to future pushes, comment `@claude review once` instead.

Costs appear on your Anthropic bill regardless of whether your organization uses Amazon Bedrock or Google Vertex AI for other Claude Code features. To set a monthly spend cap for Code Review, configure the limit for the Claude Code Review service in admin usage settings. Monitor spend via the weekly cost chart in analytics or the per-repo average cost column in admin settings.

**Source**: https://code.claude.com/docs/en/code-review
**Last Updated**: 2026-06-13
**Status**: Active
