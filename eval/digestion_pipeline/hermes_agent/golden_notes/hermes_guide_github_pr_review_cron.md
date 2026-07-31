---
tags:
  - resource
  - documentation
  - hermes_agent
  - guides
  - automation
keywords:
  - github pr review agent
  - cron poller
  - code-review skill
  - gh cli
  - repo conventions memory
  - github rate limits
  - works behind nat
topics:
  - Hermes Agent
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent
access_control_group: ["general"]
---

# Hermes Agent — GitHub PR Review Agent (Cron)

## Overview

This is the end-to-end recipe for a **cron-polling AI pull-request reviewer**: a Hermes Agent that wakes on a schedule (default every 2 hours), lists newly opened/updated PRs via the GitHub CLI (`gh`), reviews each diff for bugs, security issues, and code quality, and delivers a structured summary — hands-free. Because it *polls* on a timer rather than receiving pushed events, it needs **no public endpoint and no server**: it works behind NAT and firewalls, which is the key difference from the real-time [webhook variant](hermes_guide_github_pr_review_webhook.md). The guide composes four already-built primitives — [cron](../../term_dictionary/term_cron.md) (the scheduler), a `code-review` [skill](../../term_dictionary/term_skills.md) (consistent review guidelines), the agent's persistent [memory](../../term_dictionary/term_agentic_memory.md) (your repo conventions), and the `gh` terminal tool (fetch diffs, post reviews) — into one job. The payoff: a reviewer that runs around the clock and surfaces only the PRs that actually need human judgment (APPROVE / REQUEST_CHANGES / COMMENT verdicts).

## Prerequisites

The recipe needs three things in place before the job runs:

- **Hermes Agent installed**, and the **gateway running** — cron jobs only fire while the gateway ticker is alive. Install it as a background service with `hermes gateway install`, or run it in the foreground with `hermes gateway`.
- **GitHub CLI (`gh`) installed and authenticated** — `brew install gh` (macOS) or `sudo apt install gh` (Ubuntu/Debian), then `gh auth login`. The `gh` token must carry `repo` scope so the agent can read diffs and (optionally) post reviews back; reviews are posted as whoever `gh` is authenticated as.
- **Messaging configured (optional)** — Telegram or Discord for delivery. Without a messaging platform, set `deliver: "local"` to write reviews to `~/.hermes/cron/output/`, which is ideal for testing before wiring up notifications.

## Step 1: Verify the Setup

Confirm Hermes can reach GitHub before automating anything. Start a chat (`hermes`) and run a single read-only command — listing a few open PRs:

```
Run: gh pr list --repo NousResearch/hermes-agent --state open --limit 3
```

If you get a list of open PRs back, the `gh` integration works and you're ready to proceed.

## Step 2: Try a Manual Review

Still in the chat, ask Hermes to review one real PR — fetch its diff, then read it for bugs, security issues, and code quality, being specific about line numbers and quoting problematic code (`Run: gh pr diff 3888 --repo NousResearch/hermes-agent`). Under the hood the agent executes `gh pr diff` to pull the changes, reads the entire diff, and produces a structured review with specific findings. Once the manual review quality is acceptable, it's worth automating.

## Step 3: Create a Review Skill

A [skill](../../term_dictionary/term_skills.md) gives Hermes **consistent review guidelines that persist across sessions and cron runs** — without one, review quality varies run to run. Create the skill folder (`mkdir -p ~/.hermes/skills/code-review`) and author `~/.hermes/skills/code-review/SKILL.md`. The [manifest](../../term_dictionary/term_skill_manifest.md) frontmatter (`name`/`description`) plus a checklist body define the reviewer's persona:

```markdown
---
name: code-review
description: Review pull requests for bugs, security issues, and code quality
---

# Code Review Guidelines

When reviewing a pull request:

## What to Check
1. **Bugs** — Logic errors, off-by-one, null/undefined handling
2. **Security** — Injection, auth bypass, secrets in code, SSRF
3. **Performance** — N+1 queries, unbounded loops, memory leaks
4. **Style** — Naming conventions, dead code, missing error handling
5. **Tests** — Are changes tested? Do tests cover edge cases?

## Output Format
For each finding:
- **File:Line** — exact location
- **Severity** — Critical / Warning / Suggestion
- **What's wrong** — one sentence
- **Fix** — how to fix it

## Rules
- Be specific. Quote the problematic code.
- Don't flag style nitpicks unless they affect readability.
- If the PR looks good, say so. Don't invent problems.
- End with: APPROVE / REQUEST_CHANGES / COMMENT
```

Verify it loaded: start `hermes` and `code-review` should appear in the skills list at startup.

## Step 4: Teach It Your Conventions

This is what makes the reviewer genuinely useful. In a chat session, teach Hermes your team's standards with `Remember:` statements — e.g., "In our backend repo we use Python with FastAPI; all endpoints must have type annotations and Pydantic models; no raw SQL, only SQLAlchemy ORM; test files go in `tests/` and must use pytest fixtures," and analogously for a frontend repo ("TypeScript with React, no `any` types, all components have props interfaces, React Query for data fetching, never `useEffect` for API calls"). These memories ([agentic memory](../../term_dictionary/term_agentic_memory.md)) persist forever and survive across cron runs, so the reviewer enforces your conventions on every poll without being re-told.

## Step 5: Create the Automated Cron Job

Now wire it together as a [cron job](../../term_dictionary/term_cron.md). The [schedule expression](../../term_dictionary/term_cron_expression.md) `0 */2 * * *` runs it every 2 hours; the prompt itself is the self-contained instruction set, `--name` labels the job, `--deliver telegram` routes the summary, and `--skill code-review` loads the Step 3 persona into the fresh cron session:

```bash
hermes cron create "0 */2 * * *" \
  "Check for new open PRs and review them.

Repos to monitor:
- myorg/backend-api
- myorg/frontend-app

Steps:
1. Run: gh pr list --repo REPO --state open --limit 5 --json number,title,author,createdAt
2. For each PR created or updated in the last 4 hours:
   - Run: gh pr diff NUMBER --repo REPO
   - Review the diff using the code-review guidelines
3. Format output as:

## PR Reviews — today

### [repo] #[number]: [title]
**Author:** [name] | **Verdict:** APPROVE/REQUEST_CHANGES/COMMENT
[findings]

If no new PRs found, say: No new PRs to review." \
  --name "pr-review" \
  --deliver telegram \
  --skill code-review
```

Confirm it scheduled with `hermes cron list`. Other useful schedule expressions: `0 */2 * * *` (every 2 hours), `0 9,13,17 * * 1-5` (three times a day, weekdays only), `0 9 * * 1` (weekly Monday morning roundup), and `30m` (every 30 minutes, for high-traffic repos).

## Step 6: Run It On Demand

You don't have to wait for the schedule. Trigger the job immediately from the shell with `hermes cron run pr-review`, or from inside a chat session with the slash command `/cron run pr-review`.

## Going Further

**Post reviews directly to GitHub.** Instead of delivering to Telegram, have the agent comment on
the PR itself by appending posting instructions to the cron prompt — `gh pr review NUMBER --repo REPO --comment --body "YOUR_REVIEW"` for issues, `--request-changes --body "…"` for critical problems, and `--approve --body "Looks good"` for clean PRs. (Reminder: `gh` needs a token with `repo` scope; reviews are posted as whoever `gh` is authenticated as.)

**Weekly PR dashboard.** Add a second `0 9 * * 1` (Monday morning) cron job that, per repo, reports
open-PR count and oldest-PR age, PRs merged this week, stale PRs (older than 5 days), and PRs with no reviewer assigned — formatted as a clean summary and `--deliver telegram`.

**Multi-repo monitoring.** Scale up simply by adding more repos to the prompt; the agent processes
them sequentially, no extra setup needed.

## Troubleshooting

- **"gh: command not found"** — the gateway runs in a minimal environment; ensure `gh` is on the system PATH and restart the gateway.
- **Reviews are too generic** — add the `code-review` skill (Step 3) and teach Hermes your conventions via memory (Step 4); the more context it has about your stack, the better the reviews.
- **Cron job doesn't run** — check `hermes gateway status` (is the gateway running?) and `hermes cron list` (is the job enabled?).
- **[Rate limits](../../term_dictionary/term_rate_limiting.md)** — GitHub allows 5,000 API requests/hour for authenticated users; each PR review uses ~3-5 requests (list + diff + optional comments), so even reviewing 100 PRs/day stays well within limits.

## What's Next?

The [webhook-based variant](hermes_guide_github_pr_review_webhook.md) gives *instant* reviews when PRs open (requires a public endpoint); the [Daily Briefing Bot](hermes_guide_daily_briefing_bot.md) combines PR reviews with a morning news digest; Profiles can run a dedicated reviewer profile with its own memory and config; and Fallback Providers keep reviews running even when one model provider is down.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent
**Last Updated**: 2026-06-19
**Status**: Active
