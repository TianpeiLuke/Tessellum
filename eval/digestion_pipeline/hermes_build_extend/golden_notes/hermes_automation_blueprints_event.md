---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - webhooks
keywords:
  - hermes webhook subscribe
  - github event automation
  - api webhook routes
  - multi-skill workflows
  - webhook template variables
  - config.yaml routes
topics:
  - Hermes Agent
  - Automation Blueprints
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
access_control_group: ["general"]
---

# Hermes Automation Blueprints — Event-Driven & Multi-Skill

## Overview

This is the **event-triggered half of the Hermes automation-blueprints cookbook**: copy-paste recipes where an external event — a GitHub webhook, a third-party API POST, or a CI result — fires an agent run, instead of a clock. Where the [scheduled blueprints](hermes_automation_blueprints_scheduled.md) use `hermes cron create`, these use the **webhook platform**: either a dynamic CLI subscription (`hermes webhook subscribe`) or a static `config.yaml` route under `platforms.webhook.extra.routes`. Each recipe templates fields out of the inbound JSON payload (e.g. `{pull_request.title}`) into an agent prompt, optionally pins one or more skills with `--skill`, and routes the result to a delivery target such as a GitHub PR comment or a Slack channel. The page groups recipes into automatic PR code review, GitHub event automations (issue labeling, CI-failure analysis, cross-repo auto-port), generic API webhooks (deploy verification, alert triage, Stripe payments), and multi-skill pipelines (security audit, content), and closes with the webhook template-variable reference. The `[SILENT]` convention from the scheduled half applies equally — a response containing `[SILENT]` suppresses delivery so a quiet event produces no notification spam.

## Automatic PR Code Review

Review every pull request automatically when it opens, posting a review comment on the PR. There are two equivalent route forms — a dynamic CLI subscription and a static `config.yaml` route.

**Option A — Dynamic subscription (CLI):**

```bash
hermes webhook subscribe github-pr-review \
  --events "pull_request" \
  --prompt "Review this pull request:
Repository: {repository.full_name}
PR #{pull_request.number}: {pull_request.title}
Author: {pull_request.user.login}
Action: {action}
Diff URL: {pull_request.diff_url}

Fetch the diff with: curl -sL {pull_request.diff_url}

Review for:
- Security issues (injection, auth bypass, secrets in code)
- Performance concerns (N+1 queries, unbounded loops, memory leaks)
- Code quality (naming, duplication, error handling)
- Missing tests for new behavior

Post a concise review. If the PR is a trivial docs/typo change, say so briefly." \
  --skill github-code-review \
  --deliver github_comment
```

**Option B — Static route (config.yaml):** the same prompt lives under `platforms.webhook.extra.routes.<name>`, with a per-route `secret`, `events`, `skills`, `deliver`, and `deliver_extra` block. The webhook platform listens on `extra.port` (e.g. `8644`), validates each event against the route `secret`, and routes by GitHub event type.

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "your-global-secret"
      routes:
        github-pr-review:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review PR #{pull_request.number}: {pull_request.title}
            Repository: {repository.full_name}
            Author: {pull_request.user.login}
            Diff URL: {pull_request.diff_url}
            Review for security, performance, and code quality.
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{pull_request.number}"
```

On the GitHub side, register the route under **Settings → Webhooks → Add webhook** with Payload URL `http://your-server:8644/webhooks/github-pr-review`, content type `application/json`, the matching `secret`, and the **Pull requests** event.

## GitHub Event Automations

Beyond PR review, the GitHub-event family covers issue triage, CI diagnostics, and cross-repo porting — all keyed off `{action}` so the recipe stays silent on irrelevant sub-events.

- **Issue Auto-Labeling** (`--events "issues"`, `--deliver github_comment`): on `action=opened`, read the issue title/body, suggest labels (bug, feature, docs, security, question), identify the affected component for bug reports, and post an acknowledging response; on a label/assignment change, respond `[SILENT]`.
- **CI Failure Analysis** (a `config.yaml` route on `["check_run"]`): when `{check_run.conclusion}` is `failure`, fetch the log from `{check_run.details_url}`, identify the likely cause, and suggest a fix on the PR (`#{check_run.pull_requests.0.number}`); on `success`, respond `[SILENT]`.
- **Auto-Port Changes Across Repos** (`--events "pull_request"`, `--skill github-pr-workflow`, `--deliver log`): when `action='closed'` and `pull_request.merged` is true, fetch the diff, analyze it, and — if the change should be ported to a sibling SDK — create a branch, apply the equivalent change, and open a PR on the target repo referencing the original.

```bash
hermes webhook subscribe github-issues \
  --events "issues" \
  --prompt "New GitHub issue received:
Repository: {repository.full_name}
Issue #{issue.number}: {issue.title}
Author: {issue.user.login}
Action: {action}
Body: {issue.body}
Labels: {issue.labels}

If this is a new issue (action=opened):
1. Read the issue title and body carefully
2. Suggest appropriate labels (bug, feature, docs, security, question)
3. If it's a bug report, check if you can identify the affected component from the description
4. Post a helpful initial response acknowledging the issue

If this is a label or assignment change, respond with [SILENT]." \
  --deliver github_comment
```

## Generic API Webhooks

Any service that can POST JSON can trigger a run. These recipes use `hermes webhook subscribe` with a payload-shaped prompt and no GitHub-specific events.

- **Deploy Verification** (`--events "deployment"`): a CI/CD pipeline POSTs `{service}`, `{environment}`, `{version}`, `{deployer}`, `{health_url}` on deploy completion; the agent curls the health endpoint, scans logs, verifies the version, and reports healthy/degraded/failed. The pipeline signs the POST with an `X-Hub-Signature-256` HMAC over the body using the route secret.
- **Alert Triage** (`--deliver slack`): a Datadog/PagerDuty/Grafana alert (`{alert.name}`, `{alert.severity}`, `{alert.service}`, `{alert.message}`) is correlated against recent deploys/config changes, web-searched for known issues, and turned into a concise on-call triage summary with a likely root cause and a P1–P4 escalation recommendation.
- **Stripe Payment Monitoring** (`--events "payment_intent.succeeded,payment_intent.payment_failed,charge.dispute.created"`, `--deliver slack`): branches on `{type}` — for a failed payment it reads `{data.object.last_payment_error}` and judges transient-vs-permanent; for a dispute it flags urgent; for a success it sends a brief confirmation.

```bash
hermes webhook subscribe alert-triage \
  --prompt "Monitoring alert received:
Alert: {alert.name}
Severity: {alert.severity}
Service: {alert.service}
Message: {alert.message}
Timestamp: {alert.timestamp}

Investigate:
1. Search the web for known issues with this error pattern
2. Check if this correlates with any recent deployments or config changes
3. Draft a triage summary with:
   - Likely root cause
   - Suggested first response steps
   - Escalation recommendation (P1-P4)

Be concise. This goes to the on-call channel." \
  --deliver slack
```

## Multi-Skill Workflows

Some blueprints chain several skills into one comprehensive run. These are scheduled (`hermes cron create`) here but exercise multiple skills per run rather than one.

- **Security Audit Pipeline** (`"0 3 * * 0"`, `--skill codebase-security-audit`): a weekly review that runs dependency audits (`pip audit`, `npm audit`), greps the codebase for anti-patterns (hardcoded secrets, SQL injection, path traversal, unsafe deserialization), reviews the last 7 days of commits, checks for undocumented new env vars, and writes a severity-categorized (Critical/High/Medium/Low) report.
- **Content Pipeline** (`"0 10 * * 3"`, `--deliver local`): a weekly run that web-searches trending AI-agent topics, picks one relevant to open-source agents, drafts a ~300-word outline (hook, 3–4 sections, conclusion), and saves it to `~/drafts/blog-$(date +%Y%m%d).md`.

```bash
hermes cron create "0 3 * * 0" \
  "Run a comprehensive security audit of the hermes-agent codebase.

1. Check for dependency vulnerabilities (pip audit, npm audit)
2. Search the codebase for common security anti-patterns:
   - Hardcoded secrets or API keys
   - SQL injection vectors (string formatting in queries)
   - Path traversal risks (user input in file paths without validation)
   - Unsafe deserialization (pickle.loads, yaml.load without SafeLoader)
3. Review recent commits (last 7 days) for security-relevant changes
4. Check if any new environment variables were added without being documented

Write a security report with findings categorized by severity (Critical, High, Medium, Low).
If nothing found, report a clean bill of health." \
  --skill codebase-security-audit \
  --name "Weekly security audit" \
  --deliver telegram
```

## Webhook Template Variables

Prompts template fields directly out of the inbound JSON payload using `{dotted.path}` syntax; missing fields render empty. The most common variables:

| Variable | Description |
|----------|-------------|
| `{pull_request.title}` | PR title |
| `{issue.number}` | Issue number |
| `{repository.full_name}` | `owner/repo` |
| `{action}` | Event action (opened, closed, etc.) |
| `{__raw__}` | Full JSON payload (truncated at 4000 chars) |
| `{sender.login}` | GitHub user who triggered the event |

Nested and indexed paths work too — e.g. `{check_run.pull_requests.0.number}` and `{data.object.last_payment_error}` in the CI-failure and Stripe recipes above. The fallback `{__raw__}` injects the entire (truncated) payload when no specific field map fits.

## Related Notes

**Terms**
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — event-trigger design; relevance: webhook routes are event-driven triggers that template the payload into an agent prompt.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the multi-skill pipelines here are still `cron create` runs, and event routes register cron-style jobs.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — terminal coding agent; relevance: each templated payload becomes a prompt the autonomous agent acts on.
- [term_skills](../../term_dictionary/term_skills.md) — on-demand procedural knowledge; relevance: recipes pin skills with `--skill` (github-code-review, codebase-security-audit).
- [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — multi-step agent coordination; relevance: multi-skill pipelines orchestrate several skills in one run.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated child agent; relevance: large pipelines can fan out per event into subagents.
- [term_access_control](../../term_dictionary/term_access_control.md) — permission gating; relevance: per-route `secret`/HMAC signatures gate which callers may fire an endpoint.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable-safe runs; relevance: the `[SILENT]` pattern keeps repeated quiet events from producing duplicate notifications.

**Code-Repos**
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — webhook platform routes + payload normalization; relevance: `hermes webhook subscribe` and the `config.yaml` route forms land here.
- [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — webhook→job registration + handoff; relevance: an event route registers a cron-style job that runs the agent.
- [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the devops/security/content skills the multi-skill pipelines chain; relevance: PR-review/labeling/CI-failure recipes invoke these skills.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent run each webhook fires; relevance: the templated payload becomes an agent prompt.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes webhook` command surface; relevance: the subscribe/route CLI the recipes type.

**Snippets**
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — webhook platform route handling; relevance: implements `hermes webhook subscribe` + route dispatch.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — MS-Graph webhook; relevance: the API-webhook surface for Teams/Graph events.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — devops webhook skill; relevance: the PR-review/CI-failure GitHub-event recipes lean on it.
- [snippet_hermes_agent_skills_devops_kanban_orchestrator](../../code_snippets/snippet_hermes_agent_skills_devops_kanban_orchestrator.md) — kanban orchestrator skill; relevance: the issue-labeling/triage multi-step flow.
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron CRUD; relevance: the multi-skill pipelines are `cron create` jobs registered here.
- [snippet_hermes_agent_tools_cronjob_register](../../code_snippets/snippet_hermes_agent_tools_cronjob_register.md) — cron-job registration; relevance: an event route registers a job through this path.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — cron-job handoff; relevance: the webhook→agent-run handoff for event-fired jobs.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — delivery routing; relevance: `--deliver github_comment`/`slack`/`log` route the result here.
- [snippet_hermes_agent_cli_cron](../../code_snippets/snippet_hermes_agent_cli_cron.md) — cron CLI; relevance: the `hermes cron create` recipes for the multi-skill pipelines.
- [snippet_hermes_agent_gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — gateway cron runner; relevance: runs the agent for both scheduled and event-registered jobs and delivers the output.

**Docs**
- [hermes_automation_blueprints_scheduled](hermes_automation_blueprints_scheduled.md) — schedule-triggered blueprints; relevance: the `cron`-triggered sibling to these webhook/event recipes.
- [hermes_msgraph_app_registration](hermes_msgraph_app_registration.md) — Azure app registration; relevance: the MS-Graph webhook prerequisite for the Teams-event pipeline.
- [hermes_plugin_extensions_hooks](hermes_plugin_extensions_hooks.md) — plugin hooks/commands; relevance: gateway/shell hooks are an alternate in-process event surface.
- [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: allowlist/secret security tips for public webhook endpoints.
- [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the MCP tools used inside the multi-skill pipelines.
- [cc_github_actions](../claude_code/cc_github_actions.md) — CC GitHub-event automation; relevance: closest analogue to the PR-review/labeling recipes.
- [cc_workflow_recipes](../claude_code/cc_workflow_recipes.md) — CC workflow cookbook; relevance: analogue to the blueprint recipes.
- [cc_create_and_run_workflows](../claude_code/cc_create_and_run_workflows.md) — building multi-step CC workflows; relevance: analogue to multi-skill pipelines.
- [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — CC dynamic/event-driven workflows; relevance: analogue to webhook-triggered runs.
- [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — dispatching background agents on events; relevance: analogue to event-fired agent runs.
- [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — CC parallel agent runs; relevance: analogue to multi-skill pipelines fanning out per event.
- [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — CC multi-agent orchestration; relevance: analogue to the security-audit/content multi-skill pipelines.

**Source**: `inbox/hermes_agent_docs/guides/automation-blueprints.md` · https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
**Last Updated**: 2026-06-19
**Status**: Active
